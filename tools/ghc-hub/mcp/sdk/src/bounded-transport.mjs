import {TextDecoder} from 'node:util';

export const DEFAULT_LIMITS = Object.freeze({
  lineBytes: 32768, outputLineBytes: 16384, queuedOutputBytes: 65536,
  sessionInputBytes: 1048576, sessionOutputBytes: 1048576, messages: 512,
  jsonDepth: 24, jsonNodes: 2048, writeTimeoutMs: 2000, sessionTimeoutMs: 120000,
  quotaWindowMs: 60000
});

export function boundedLimits(custom = {}) {
  if (!custom || typeof custom !== 'object' || Array.isArray(custom)) throw new TypeError('Invalid transport limits');
  const limits = {...DEFAULT_LIMITS};
  for (const [key, value] of Object.entries(custom)) {
    if (!Object.hasOwn(limits, key) || !Number.isSafeInteger(value) || value < 1 || value > limits[key]) {
      throw new TypeError('Invalid transport limits');
    }
    limits[key] = value;
  }
  if (limits.outputLineBytes > limits.queuedOutputBytes) throw new TypeError('Invalid output capacity');
  return Object.freeze(limits);
}

function finiteTree(root, limits) {
  const stack = [[root, 0]];
  let nodes = 0;
  while (stack.length) {
    const [value, depth] = stack.pop();
    if (++nodes > limits.jsonNodes || depth > limits.jsonDepth) return false;
    if (typeof value === 'number' && !Number.isFinite(value)) return false;
    if (value && typeof value === 'object') {
      for (const item of Object.values(value)) {
        if (stack.length + nodes >= limits.jsonNodes) return false;
        stack.push([item, depth + 1]);
      }
    }
  }
  return true;
}

/** At most 65 buckets; expiry is conservatively rounded, never earlier than admission. */
class RollingQuota {
  constructor(limits, now) {
    this.windowMs = limits.quotaWindowMs;
    this.quantum = Math.max(1, Math.ceil(this.windowMs / 64));
    this.caps = {input: limits.sessionInputBytes, output: limits.sessionOutputBytes, messages: limits.messages};
    this.totals = {input: 0, output: 0, messages: 0};
    this.buckets = [];
    this.now = now;
    this.lastTime = -Infinity;
    this.peakBuckets = 0;
  }
  reserve(kind, amount) {
    const time = this.now();
    if (!Number.isFinite(time) || time < this.lastTime) return false;
    this.lastTime = time;
    while (this.buckets.length && this.buckets[0].at + this.windowMs <= time) {
      const old = this.buckets.shift();
      for (const key of Object.keys(this.totals)) this.totals[key] -= old[key];
    }
    if (this.totals[kind] + amount > this.caps[kind]) return false;
    const at = Math.ceil(time / this.quantum) * this.quantum;
    let bucket = this.buckets.at(-1);
    if (!bucket || bucket.at !== at) {
      bucket = {at, input: 0, output: 0, messages: 0};
      this.buckets.push(bucket);
      this.peakBuckets = Math.max(this.peakBuckets, this.buckets.length);
    }
    bucket[kind] += amount;
    this.totals[kind] += amount;
    return true;
  }
}

/** Implements the official SDK Transport seam; no MCP handshake or method routing lives here. */
export class BoundedStdioTransport {
  constructor({input, output, limits = {}, onEvent = () => {}, servingProfile = 'bounded', now = () => performance.now()}) {
    if (!input?.on || !input?.destroy || !output?.write || !output?.destroy || typeof onEvent !== 'function') {
      throw new TypeError('Explicit owned Node streams required');
    }
    this.input = input;
    this.output = output;
    this.limits = boundedLimits(limits);
    if (!['bounded', 'parent-owned'].includes(servingProfile) || typeof now !== 'function') {
      throw new TypeError('Invalid trusted serving profile');
    }
    this.servingProfile = servingProfile;
    this.quota = servingProfile === 'parent-owned' ? new RollingQuota(this.limits, now) : null;
    this.onEvent = onEvent;
    this.stats = {inputBytes: 0, outputBytes: 0, messages: 0, peakQueuedBytes: 0, reason: null, servingProfile};
    this.frame = Buffer.alloc(this.limits.lineBytes);
    this.used = 0;
    this.decoder = new TextDecoder('utf-8', {fatal: true});
    this.queue = [];
    this.queuedBytes = 0;
    this.writing = null;
    this.started = false;
    this.closed = false;
    this.done = new Promise(resolve => { this.resolveDone = resolve; });
    this.dataHandler = chunk => this.acceptChunk(chunk);
    this.endHandler = () => this.close(this.used ? 'incomplete_line' : 'eof');
    this.inputError = () => this.fail('input_error');
    this.outputError = () => this.fail('output_error');
  }

  async start() {
    if (this.started || this.closed) throw new Error('Transport is not new');
    this.started = true;
    this.input.on('data', this.dataHandler);
    this.input.once('end', this.endHandler);
    this.input.on('error', this.inputError);
    this.output.on('error', this.outputError);
    this.input.once('close', () => this.close('input_closed'));
    this.output.once('close', () => this.close('output_closed'));
    if (this.servingProfile === 'bounded') {
      this.sessionTimer = setTimeout(() => this.fail('session_timeout'), this.limits.sessionTimeoutMs);
    }
  }

  acceptChunk(chunk) {
    if (this.closed) return;
    if (!Buffer.isBuffer(chunk)) return this.fail('input_type');
    this.stats.inputBytes += chunk.length;
    if (this.quota ? !this.quota.reserve('input', chunk.length) : this.stats.inputBytes > this.limits.sessionInputBytes) {
      return this.fail(this.quota ? 'input_quota' : 'input_limit');
    }
    for (let offset = 0; offset < chunk.length && !this.closed;) {
      const newline = chunk.indexOf(10, offset);
      const end = newline === -1 ? chunk.length : newline;
      const length = end - offset;
      if (this.used + length > this.frame.length) return this.fail('line_limit');
      chunk.copy(this.frame, this.used, offset, end);
      this.used += length;
      if (newline === -1) break;
      const size = this.used > 0 && this.frame[this.used - 1] === 13 ? this.used - 1 : this.used;
      ++this.stats.messages;
      if (this.quota ? !this.quota.reserve('messages', 1) : this.stats.messages > this.limits.messages) {
        return this.fail(this.quota ? 'message_quota' : 'message_limit');
      }
      let message;
      try { message = JSON.parse(this.decoder.decode(this.frame.subarray(0, size))); }
      catch { return this.fail('invalid_frame'); }
      this.used = 0;
      if (!finiteTree(message, this.limits)) return this.fail('json_limit');
      const methods = new Set(['initialize', 'notifications/initialized', 'server/discover', 'tools/list', 'tools/call', 'notifications/cancelled', 'subscriptions/listen', 'ping']);
      const method = methods.has(message?.method) ? message.method : 'other';
      try { this.onEvent({kind: 'input', method}); this.onmessage?.(message); }
      catch { return this.fail('receiver_error'); }
      offset = newline + 1;
    }
  }

  send(message) {
    if (this.closed) return Promise.reject(new Error('Transport closed'));
    let bytes;
    try {
      if (!finiteTree(message, this.limits)) throw new Error();
      bytes = Buffer.from(JSON.stringify(message) + '\n', 'utf8');
    } catch { this.fail('invalid_output'); return Promise.reject(new Error('Invalid output')); }
    if (bytes.length > this.limits.outputLineBytes || (!this.quota && this.stats.outputBytes + bytes.length > this.limits.sessionOutputBytes)) {
      this.fail('output_limit'); return Promise.reject(new Error('Output capacity exceeded'));
    }
    if (this.quota && !this.quota.reserve('output', bytes.length)) {
      this.fail('output_quota'); return Promise.reject(new Error('Output window capacity exceeded'));
    }
    if (this.queuedBytes + bytes.length > this.limits.queuedOutputBytes) {
      this.fail('queue_limit'); return Promise.reject(new Error('Output queue capacity exceeded'));
    }
    this.stats.outputBytes += bytes.length;
    this.queuedBytes += bytes.length;
    this.stats.peakQueuedBytes = Math.max(this.stats.peakQueuedBytes, this.queuedBytes);
    return new Promise((resolve, reject) => {
      this.queue.push({bytes, resolve, reject});
      this.pump();
    });
  }

  pump() {
    if (this.closed || this.writing || !this.queue.length) return;
    const item = this.queue.shift();
    this.writing = item;
    this.writeTimer = setTimeout(() => this.fail('output_timeout'), this.limits.writeTimeoutMs);
    try {
      this.output.write(item.bytes, error => {
        if (this.closed) return;
        clearTimeout(this.writeTimer);
        this.writing = null;
        this.queuedBytes -= item.bytes.length;
        if (error) { item.reject(new Error('Output write failed')); this.fail('output_error'); return; }
        item.resolve();
        this.pump();
      });
    } catch { this.fail('output_error'); }
  }

  fail(reason) {
    if (this.closed) return;
    try { this.onerror?.(new Error('Bounded stdio transport failure')); } catch {}
    void this.close(reason);
  }

  async close(reason = 'closed') {
    if (this.closed) return;
    this.closed = true;
    this.stats.reason = reason;
    clearTimeout(this.sessionTimer);
    clearTimeout(this.writeTimer);
    this.input.removeListener('data', this.dataHandler);
    this.input.removeListener('end', this.endHandler);
    this.input.pause?.();
    const error = new Error('Transport closed');
    this.writing?.reject(error);
    for (const item of this.queue) item.reject(error);
    this.queue.length = 0;
    this.writing = null;
    this.queuedBytes = 0;
    // Error guards remain through destruction; writable error callbacks may arrive later.
    this.input.destroy?.();
    // A closing connection discards in-flight responses. Keep stdin open until responses arrive.
    // Destroy also releases a sink whose write callback never completes.
    this.output.destroy();
    try { this.onclose?.(); } catch {}
    this.resolveDone(Object.freeze({...this.stats, ...(this.quota ? {
      quotaWindowMs: this.quota.windowMs, quotaPeakBuckets: this.quota.peakBuckets,
      quotaBucketCapacity: 65, quotaMaximumExpiryRoundingMs: this.quota.quantum
    } : {})}));
  }
}
