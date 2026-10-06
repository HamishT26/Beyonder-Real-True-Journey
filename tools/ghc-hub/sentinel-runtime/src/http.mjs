import {ENDPOINT, LIMITS, SentinelError, requireThat} from './contract.mjs';

export function abortRace(promise, signal) {
  if (signal.aborted) { Promise.resolve(promise).catch(() => {}); return Promise.reject(new SentinelError('aborted')); }
  return new Promise((resolve, reject) => {
    const abort = () => reject(new SentinelError('aborted'));
    signal.addEventListener('abort', abort, {once: true});
    Promise.resolve(promise).then(resolve, reject).finally(() => signal.removeEventListener('abort', abort)).catch(() => {});
  });
}
export function createOpenAIHttp({fetchImpl = globalThis.fetch, kind = 'live'} = {}) {
  requireThat(typeof fetchImpl === 'function' && ['live', 'fixture'].includes(kind), 'invalid_http_provider');
  if (kind === 'fixture') requireThat(fetchImpl !== globalThis.fetch, 'explicit_fake_http_required');
  return Object.freeze({kind, async request(serialized, {key, runId, signal, maxResponseBytes = LIMITS.responseBytes}) {
    const response = await abortRace(Promise.resolve().then(() => {
      requireThat(!signal.aborted, 'aborted');
      return fetchImpl(ENDPOINT, {
      method: 'POST', redirect: 'error', credentials: 'omit', cache: 'no-store', signal,
      headers: {'Content-Type': 'application/json', Authorization: `Bearer ${key}`, 'X-Client-Request-Id': runId}, body: serialized
      });
    }), signal);
    const cancelBody = () => { try { Promise.resolve(response.body?.cancel?.()).catch(() => {}); } catch {} };
    if (response.redirected || response.url !== ENDPOINT || response.status >= 300 && response.status < 400) {
      cancelBody(); throw new SentinelError('redirect_rejected');
    }
    if (response.status !== 200) { cancelBody(); throw new SentinelError('http_status_unknown_cost'); }
    const contentType = response.headers?.get('content-type') ?? '';
    if (!/^application\/json(?:\s*;|$)/i.test(contentType)) { cancelBody(); throw new SentinelError('unexpected_content_type'); }
    const length = response.headers?.get('content-length');
    if (length !== null && length !== undefined && (!/^\d+$/.test(length) || BigInt(length) > BigInt(maxResponseBytes))) {
      cancelBody(); throw new SentinelError('response_size_limit');
    }
    requireThat(response.body?.getReader, 'missing_response_body');
    const reader = response.body.getReader(); const chunks = []; let total = 0;
    try {
      while (true) {
        const part = await abortRace(reader.read(), signal);
        if (part.done) break;
        requireThat(part.value instanceof Uint8Array, 'invalid_response_chunk');
        total += part.value.byteLength;
        requireThat(total <= maxResponseBytes, 'response_size_limit');
        chunks.push(Buffer.from(part.value));
      }
      let parsed;
      try { parsed = JSON.parse(new TextDecoder('utf-8', {fatal: true}).decode(Buffer.concat(chunks))); }
      catch { throw new SentinelError('invalid_response_json'); }
      return {parsed, responseBytes: total};
    } finally {
      try { Promise.resolve(reader.cancel()).catch(() => {}); } catch {}
      try { reader.releaseLock(); } catch {}
    }
  }});
}

export function parseTextResponse(value, {approvedModels, maxOutputBytes, key}) {
  const stack = [[value, 0]]; let nodes = 0;
  while (stack.length) {
    const [item, depth] = stack.pop(); requireThat(++nodes <= 4096 && depth <= 32, 'response_structure_limit');
    if (item && typeof item === 'object') for (const child of Object.values(item)) stack.push([child, depth + 1]);
  }
  requireThat(value && value.object === 'response' && approvedModels.includes(value.model) && ['completed', 'incomplete'].includes(value.status) && !value.error, 'invalid_response_schema');
  requireThat(value.service_tier === undefined || value.service_tier === 'default', 'response_price_tier_mismatch');
  requireThat(Array.isArray(value.output) && value.output.length <= 32, 'invalid_response_output');
  const texts = []; let refusal = false, bytes = 0;
  for (const item of value.output) {
    if (item.type === 'reasoning') continue; // No chain-of-thought or summaries are exported.
    requireThat(item.type === 'message' && item.role === 'assistant' && Array.isArray(item.content) && item.content.length <= 64, 'unsupported_response_item');
    for (const content of item.content) {
      if (content.type === 'refusal') { refusal = true; continue; }
      requireThat(content.type === 'output_text' && typeof content.text === 'string', 'unsupported_response_content');
      bytes += Buffer.byteLength(content.text); requireThat(bytes <= maxOutputBytes, 'output_size_limit'); texts.push(content.text);
    }
  }
  requireThat(texts.length > 0 || refusal || value.status === 'incomplete', 'missing_text_output');
  const usage = value.usage;
  requireThat(usage && Number.isSafeInteger(usage.input_tokens) && usage.input_tokens >= 0 && Number.isSafeInteger(usage.output_tokens) && usage.output_tokens >= 0, 'usage_unknown');
  if (usage.total_tokens !== undefined) requireThat(usage.total_tokens === usage.input_tokens + usage.output_tokens, 'invalid_usage_total');
  for (const [amount, upper] of [[usage.input_tokens_details?.cached_tokens, usage.input_tokens], [usage.output_tokens_details?.reasoning_tokens, usage.output_tokens]]) {
    if (amount !== undefined) requireThat(Number.isSafeInteger(amount) && amount >= 0 && amount <= upper, 'invalid_usage_details');
  }
  const text = texts.join('\n').split(key).join('[REDACTED]').replace(/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f\u061c\u200e\u200f\u202a-\u202e\u2066-\u206f]/g, '');
  requireThat(Buffer.byteLength(text) <= maxOutputBytes, 'output_size_limit');
  return {text, reportedModel: value.model, outcome: refusal ? 'refused' : value.status, usage: {inputTokens: usage.input_tokens, outputTokens: usage.output_tokens}};
}
