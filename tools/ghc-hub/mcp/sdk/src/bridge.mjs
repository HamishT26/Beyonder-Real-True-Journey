import {McpServer, fromJsonSchema} from '@modelcontextprotocol/server';
import {serveStdio} from '@modelcontextprotocol/server/stdio';
import {BoundedStdioTransport} from './bounded-transport.mjs';
import {TOOL_SPECS, copyRegistry, inputSchema, safeArguments, publicProjection, toolFailure, toolSuccess} from './contract.mjs';

export const SERVER_INFO = Object.freeze({name: 'nexus-hub-readonly-sdk', version: '2.6.0'});

/** A trusted read-only dispatcher is injected; this library never imports private GHC state. */
export function serveNexusStdio({dispatch, selectors, input = process.stdin, output = process.stdout,
  limits = {}, callbackTimeoutMs = 2000, onEvent = () => {}, servingProfile = 'bounded', signalSource = process}) {
  if (typeof dispatch !== 'function' || typeof onEvent !== 'function') throw new TypeError('Explicit read-only bindings required');
  if (!Number.isSafeInteger(callbackTimeoutMs) || callbackTimeoutMs < 1 || callbackTimeoutMs > 2000) {
    throw new TypeError('Invalid callback deadline');
  }
  const registry = copyRegistry(selectors);
  const session = new AbortController();
  if (servingProfile === 'parent-owned' && (!signalSource?.once || !signalSource?.removeListener)) {
    throw new TypeError('Parent-owned signal source required');
  }
  const transport = new BoundedStdioTransport({input, output, limits, onEvent, servingProfile});
  let active = null;
  let windowStart = performance.now();
  let callsInWindow = 0;
  const emit = event => { try { onEvent(event); } catch {} };

  async function invoke(spec, supplied, sdkContext) {
    let args;
    try { args = safeArguments(spec, supplied, registry); }
    catch { return toolFailure('invalid_arguments'); }
    if (session.signal.aborted || sdkContext.mcpReq.signal.aborted) return toolFailure('cancelled');
    if (active) return toolFailure('busy');
    if (performance.now() - windowStart >= 1000) { windowStart = performance.now(); callsInWindow = 0; }
    if (++callsInWindow > 16) return toolFailure('rate_limited');

    const controller = new AbortController();
    const signal = AbortSignal.any([controller.signal, session.signal, sdkContext.mcpReq.signal]);
    const lease = {controller};
    active = lease;
    let timer;
    let abortHandler;
    const cancelled = new Promise(resolve => {
      abortHandler = () => resolve({kind: 'cancelled'});
      signal.addEventListener('abort', abortHandler, {once: true});
    });
    const timeout = new Promise(resolve => {
      timer = setTimeout(() => resolve({kind: 'timeout'}), callbackTimeoutMs);
    });
    const called = Promise.resolve().then(() => {
      if (signal.aborted) return {kind: 'cancelled'};
      return Promise.resolve(dispatch(spec.name, args, Object.freeze({signal, readOnly: true})))
        .then(data => ({kind: 'result', data}));
    }).catch(() => ({kind: 'failed'}));
    // Capacity is released by actual dispatcher settlement, never just by a deadline race.
    void called.finally(() => { if (active === lease) active = null; });
    try {
      const outcome = await Promise.race([called, cancelled, timeout]);
      if (outcome.kind === 'timeout') {
        controller.abort();
        emit({kind: 'operation', outcome: 'timeout'});
        return toolFailure('timeout');
      }
      if (outcome.kind === 'cancelled' || signal.aborted) return toolFailure('cancelled');
      if (outcome.kind === 'failed') return toolFailure('operation_failed');
      try { return toolSuccess(publicProjection(spec, outcome.data, args, registry)); }
      catch { return toolFailure('invalid_output'); }
    } finally {
      clearTimeout(timer);
      signal.removeEventListener('abort', abortHandler);
    }
  }

  const factory = ({era}) => {
    emit({kind: 'factory', era});
    const server = new McpServer(SERVER_INFO, {capabilities: {tools: {listChanged: false}}});
    for (const spec of TOOL_SPECS) {
      server.registerTool(spec.name, {
        description: spec.description,
        inputSchema: fromJsonSchema(inputSchema(spec)),
        annotations: {readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false}
      }, (args, context) => invoke(spec, args, context));
    }
    return server;
  };
  const handle = serveStdio(factory, {legacy: 'serve', transport, maxSubscriptions: 1,
    onerror: () => emit({kind: 'sdk_error'})});
  const done = transport.done.then(stats => {
    session.abort();
    if (servingProfile === 'parent-owned') {
      signalSource.removeListener('SIGINT', onSignal);
      signalSource.removeListener('SIGTERM', onSignal);
    }
    emit({kind: 'closed', reason: stats.reason});
    return stats;
  });
  const close = async () => { session.abort(); await handle.close(); await done; };
  const onSignal = () => { void close().catch(() => transport.fail('signal_shutdown_failure')); };
  if (servingProfile === 'parent-owned') {
    signalSource.once('SIGINT', onSignal);
    signalSource.once('SIGTERM', onSignal);
  }
  return Object.freeze({done, close});
}
