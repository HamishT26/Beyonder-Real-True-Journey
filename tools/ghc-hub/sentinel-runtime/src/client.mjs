import crypto from 'node:crypto';
import {LIMITS, SentinelError, requireThat, prepareRequest, normalizeQuote, upperCost, offlinePlan, uuid, sha256} from './contract.mjs';
import {createOpenAIHttp, abortRace, parseTextResponse} from './http.mjs';
export {fromHubSpec, createRequest, offlinePlan, providers} from './contract.mjs';
export {FileLedger} from './ledger.mjs';

const knownCodes = new Set(['aborted', 'redirect_rejected', 'http_status_unknown_cost', 'unexpected_content_type',
  'response_size_limit', 'missing_response_body', 'invalid_response_chunk', 'invalid_response_json', 'response_structure_limit',
  'invalid_response_schema', 'response_price_tier_mismatch', 'invalid_response_output', 'unsupported_response_item',
  'unsupported_response_content', 'output_size_limit', 'missing_text_output', 'usage_unknown', 'invalid_usage_total',
  'invalid_usage_details', 'credential_provider_required', 'credential_unavailable', 'wrong_credential_kind',
  'invalid_credential', 'credential_in_payload', 'explicit_execution_required', 'network_execution_not_authorized',
  'execution_mode_mismatch', 'reviewed_request_required', 'client_requires_review', 'operation_in_progress',
  'known_available_budget_required', 'ledger_overrun_requires_review', 'insufficient_local_budget', 'ledger_capacity',
  'ledger_busy_or_stale_lock', 'pricing_and_token_evidence_required', 'fixture_pricing_not_live', 'quote_request_mismatch',
  'incomplete_price_coverage', 'verified_input_bound_required', 'invalid_input_token_bound', 'quote_expired_or_invalid',
  'invalid_quote', 'invalid_quote_fields', 'invalid_price_source', 'invalid_fixture_source', 'invalid_usd_decimal']);
function safeCode(error, fallback) { return knownCodes.has(error?.code) ? error.code : fallback; }

/** One reviewed request, no tools or retries. The parent owns the credential provider and live authorization. */
export function createSentinelRuntime({ledger, credentialProvider = null, httpProvider = createOpenAIHttp(),
  allowNetwork = false, now = () => Date.now(), timeoutMs = 15000,
  maxResponseBytes = LIMITS.responseBytes, maxOutputBytes = LIMITS.outputBytes} = {}) {
  requireThat(ledger?.beginRun && ledger?.receipt && ledger?.reserve && ledger?.snapshot && ledger?.settle, 'ledger_required');
  requireThat(typeof now === 'function' && ['live', 'fixture'].includes(httpProvider?.kind) && typeof httpProvider?.request === 'function', 'invalid_runtime_provider');
  requireThat(Number.isInteger(timeoutMs) && timeoutMs >= 10 && timeoutMs <= LIMITS.timeoutMs, 'invalid_request_timeout');
  requireThat(Number.isInteger(maxResponseBytes) && maxResponseBytes >= 1 && maxResponseBytes <= LIMITS.responseBytes &&
    Number.isInteger(maxOutputBytes) && maxOutputBytes >= 1 && maxOutputBytes <= LIMITS.outputBytes, 'invalid_output_bounds');
  let active = false, quarantined = false;

  function plan(request, quote = null, execution = 'live') {
    let budget;
    try { budget = ledger.snapshot(); } catch { budget = {known: false}; }
    return offlinePlan(request, {quote, budget, execution, now: now()});
  }

  async function runOnce({request: raw, quote: rawQuote = null, runId = crypto.randomUUID(),
    execute = false, execution = 'live', reviewedRequestSha256 = null, signal = null} = {}) {
    if (!uuid(runId)) return {status: 'denied', reason: 'invalid_run_id', receiptSaved: false, httpAttempts: 0};
    if (active || quarantined) return {status: 'denied', reason: active ? 'operation_in_progress' : 'client_requires_review', receiptSaved: false, httpAttempts: 0};
    active = true;
    const start = performance.now();
    let prepared, quote, reserve = null, reserved = false, attempted = false, key = null, timer = null, abortForward = null;
    let intentSaved = false, resultText = null, usage = null, accounted = null, outcome = 'denied', reason = null;
    let inputBoundExceeded = false, localAbort = null;
    const controller = new AbortController();
    const abort = cause => { localAbort ??= cause; controller.abort(); };
    try {
      prepared = prepareRequest(raw);
      ledger.beginRun(runId, {schema: 'ghc.sentinel.intent.v1', runId, sentinelId: prepared.request.sentinelId,
        provider: prepared.request.provider, model: prepared.request.model, requestSha256: prepared.requestSha256,
        requestedExecution: ['live', 'simulate'].includes(execution) ? execution : 'invalid', createdUtc: new Date(now()).toISOString(),
        inputBytes: Buffer.byteLength(prepared.request.input) + Buffer.byteLength(prepared.request.instructions),
        maxOutputTokens: prepared.request.maxOutputTokens, maxHttpRequests: 1, automaticRetries: 0});
      intentSaved = true;
      requireThat(execute === true, 'explicit_execution_required');
      requireThat(['live', 'simulate'].includes(execution) && (execution === 'simulate') === (httpProvider.kind === 'fixture'), 'execution_mode_mismatch');
      requireThat(execution !== 'live' || allowNetwork === true, 'network_execution_not_authorized');
      requireThat(reviewedRequestSha256 === prepared.requestSha256, 'reviewed_request_required');
      requireThat(!signal?.aborted, 'aborted');
      quote = normalizeQuote(rawQuote, prepared, execution, now());
      reserve = upperCost(quote, quote.inputBound, prepared.request.maxOutputTokens).toString();
      ledger.reserve(runId, prepared.requestSha256, reserve, quote.fingerprint);
      reserved = true;
      // A reservation exists and is fsynced before resolving credentials or invoking HTTP.
      timer = setTimeout(() => abort('timeout'), timeoutMs);
      if (signal) { abortForward = () => abort('cancelled'); signal.addEventListener('abort', abortForward, {once: true}); }
      requireThat(typeof credentialProvider === 'function', 'credential_provider_required');
      let credential;
      try { credential = await abortRace(Promise.resolve().then(() => credentialProvider(Object.freeze({provider: 'openai', signal: controller.signal}))), controller.signal); }
      catch (error) { if (controller.signal.aborted) throw new SentinelError('aborted'); throw new SentinelError('credential_unavailable'); }
      requireThat(credential?.kind === 'openai-api-key', 'wrong_credential_kind');
      requireThat(typeof credential.value === 'string' && /^[\x21-\x7e]{8,4096}$/.test(credential.value), 'invalid_credential');
      key = credential.value; credential = null;
      requireThat(!prepared.serialized.includes(key), 'credential_in_payload');
      requireThat(!controller.signal.aborted, 'aborted');
      ledger.markDispatch(runId);
      attempted = true; // Even a synchronous transport failure is conservatively unknown after this boundary.
      const response = await abortRace(httpProvider.request(prepared.serialized, {key, runId, signal: controller.signal, maxResponseBytes}), controller.signal);
      const parsed = parseTextResponse(response.parsed, {approvedModels: quote.responseModels, maxOutputBytes, key});
      usage = parsed.usage;
      inputBoundExceeded = usage.inputTokens > quote.inputBound || usage.outputTokens > prepared.request.maxOutputTokens;
      accounted = upperCost(quote, usage.inputTokens, usage.outputTokens).toString();
      outcome = inputBoundExceeded ? 'usage_bound_breached' : parsed.outcome;
      reason = inputBoundExceeded ? 'review_required' : null;
      if (!inputBoundExceeded) resultText = parsed.text;
      quarantined ||= inputBoundExceeded;
    } catch (error) {
      reason = controller.signal.aborted || signal?.aborted ? (localAbort === 'timeout' ? 'timeout' : 'cancelled') : safeCode(error, attempted ? 'transport_or_response_failure' : 'validation_or_storage_failure');
      outcome = attempted ? 'unknown' : 'not_sent';
      if (attempted) quarantined = true;
      resultText = null;
      if (error?.code === 'EEXIST') reason = 'run_or_record_already_exists';
    } finally {
      clearTimeout(timer);
      if (signal && abortForward) signal.removeEventListener('abort', abortForward);
      controller.abort();
      key = null; // Strings are not guaranteed to be zeroized; nothing logs or persists them.
    }

    let receiptSaved = false, accountingSaved = false, receiptReference = null;
    const record = {schema: 'ghc.sentinel.run-receipt.v1', runId,
      ...(prepared ? {sentinelId: prepared.request.sentinelId, provider: prepared.request.provider,
        model: prepared.request.model, requestSha256: prepared.requestSha256} : {}),
      execution: execution === 'simulate' ? 'simulate' : 'live', outcome, reason, httpAttempts: attempted ? 1 : 0,
      liveNetworkRequested: attempted && execution === 'live', remoteOutcomeConfirmed: attempted && execution === 'live' && ['completed', 'incomplete', 'refused'].includes(outcome),
      remoteCancellationConfirmed: false, requestedReservationMicros: reserve, reservedMicros: reserved ? reserve : null, usage,
      accountedUpperMicros: accounted, accountingBasis: accounted !== null ? 'provider-reported usage at supplied full rates, no cache discount' : attempted ? 'unknown; full reservation retained' : 'known not sent',
      billingInvoiceVerified: false, aggregateUsd50Enforced: false, automaticRetries: 0,
      outputBytes: resultText === null ? 0 : Buffer.byteLength(resultText), outputSha256: resultText === null ? null : sha256(resultText),
      elapsedMs: +(performance.now() - start).toFixed(3), completedUtc: new Date(now()).toISOString(),
      credentialRecorded: false, promptRecorded: false, responseTextRecorded: false};
    try {
      if (intentSaved) { receiptReference = ledger.receipt(runId, record); receiptSaved = true; }
      if (receiptSaved && reserved && (!attempted || accounted !== null)) {
        ledger.settle(runId, attempted ? accounted : '0', attempted ? 'reported_usage_upper_bound' : 'known_not_sent', {boundBreach: inputBoundExceeded});
        accountingSaved = true;
      }
    } catch { quarantined = true; reason = 'receipt_or_accounting_persistence_failure'; }
    active = false;
    return {schema: 'ghc.sentinel.runtime.result.v1', runId, execution, status: reason === 'receipt_or_accounting_persistence_failure' ? 'persistence_failure' : outcome,
      reason, text: receiptSaved ? resultText : null, receiptSaved, receiptReference,
      accounting: {reservedMicros: reserved ? reserve : null, accountedUpperMicros: accounted, settlementSaved: accountingSaved,
        reservationRetained: reserved && !accountingSaved, aggregateUsd50Enforced: false},
      httpAttempts: attempted ? 1 : 0, automaticRetries: 0, requiresReview: quarantined,
      modelAccessVerified: false, modelTrained: false, weightsAvailable: false, worldModelEstablished: false, multimodalImplemented: false};
  }
  return Object.freeze({plan, runOnce, get requiresReview() { return quarantined; }});
}
