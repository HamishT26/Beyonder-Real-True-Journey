import crypto from 'node:crypto';

export const ORIGIN = 'https://api.openai.com';
export const ENDPOINT = ORIGIN + '/v1/responses';
export const LIMITS = Object.freeze({inputBytes: 65536, responseBytes: 262144, outputBytes: 65536,
  outputTokens: 32768, timeoutMs: 60000, ledgerRuns: 256, recordBytes: 16384});
export const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');
export class SentinelError extends Error { constructor(code) { super(code); this.name = 'SentinelError'; this.code = code; } }
export function requireThat(value, code) { if (!value) throw new SentinelError(code); }
export const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
export function shape(value, keys, code) {
  requireThat(object(value) && Object.keys(value).every(key => keys.includes(key)), code);
}
export const uuid = value => typeof value === 'string' && /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(value);
const modelId = value => typeof value === 'string' && /^[A-Za-z0-9][A-Za-z0-9._:-]{0,199}$/.test(value);
const slug = value => typeof value === 'string' && /^[a-z][a-z0-9-]{0,79}$/.test(value) && !/^(con|prn|aux|nul|com[1-9]|lpt[1-9])$/.test(value);
const credentialPattern = /-----BEGIN [A-Z ]*PRIVATE KEY-----|\bsk-(?:proj-)?[A-Za-z0-9_-]{16,}|\bBearer\s+[A-Za-z0-9._-]{16,}/i;
export const containsCredentialMaterial = value => typeof value === 'string' && credentialPattern.test(value);
export const providers = () => [{id: 'openai', implemented: true, endpoint: ENDPOINT, modalities: ['text']}];
export function createRequest(value) {
  shape(value, ['schema', 'sentinelId', 'provider', 'model', 'input', 'instructions', 'maxOutputTokens'], 'invalid_request_fields');
  requireThat(value.schema === 'ghc.sentinel.runtime.request.v1' && slug(value.sentinelId), 'invalid_request_schema');
  requireThat(value.provider === 'openai', 'unsupported_provider');
  requireThat(modelId(value.model), 'model_selection_required');
  requireThat(typeof value.input === 'string' && value.input.trim().length > 0, 'text_input_required');
  requireThat(value.instructions === undefined || typeof value.instructions === 'string', 'invalid_instructions');
  const instructions = value.instructions ?? '';
  requireThat(Buffer.byteLength(value.input) + Buffer.byteLength(instructions) <= LIMITS.inputBytes, 'input_limit');
  requireThat(!credentialPattern.test(value.model + '\n' + value.sentinelId + '\n' + value.input + '\n' + instructions), 'credential_material_in_input');
  requireThat(Number.isSafeInteger(value.maxOutputTokens) && value.maxOutputTokens >= 16 && value.maxOutputTokens <= LIMITS.outputTokens, 'invalid_output_token_limit');
  return Object.freeze({schema: value.schema, sentinelId: value.sentinelId, provider: value.provider,
    model: value.model, input: value.input, instructions, maxOutputTokens: value.maxOutputTokens});
}
export function fromHubSpec(spec, {input, instructions = '', provider = spec?.model?.provider,
  model = spec?.model?.id, maxOutputTokens = spec?.budget?.maxOutputTokens} = {}) {
  requireThat(spec?.schema === 'ghc.sentinel.spec.v1' && spec.stage === 'design' && spec.deployment?.enabled === false, 'unsupported_hub_spec');
  requireThat(spec.implementation === 'agent-orchestration' && spec.model?.weightsAvailable === false, 'unsupported_architecture_claim');
  requireThat(Array.isArray(spec.modalities) && spec.modalities.length === 1 && spec.modalities[0] === 'text', 'text_only_runtime');
  requireThat(spec.memory?.automaticExport === false && spec.memory?.classification === 'private', 'unsupported_memory_policy');
  requireThat(Number.isFinite(spec.budget?.maxUsd) && spec.budget.maxUsd >= 0 && spec.budget.maxUsd <= 50, 'invalid_design_budget');
  requireThat(Number.isInteger(spec.budget?.maxTurns) && spec.budget.maxTurns >= 1 && spec.budget.maxTurns <= 100, 'invalid_design_turns');
  requireThat(maxOutputTokens <= spec.budget.maxOutputTokens, 'design_output_limit');
  const allowedTools = ['nexus.chats.list', 'nexus.lab.catalogue', 'nexus.identity.summary', 'nexus.sentinel.validate', 'nexus.remote.plan'];
  requireThat(Array.isArray(spec.tools) && spec.tools.every(tool => allowedTools.includes(tool)), 'unsupported_declared_tool');
  return createRequest({schema: 'ghc.sentinel.runtime.request.v1', sentinelId: spec.id, provider, model, input, instructions, maxOutputTokens});
}
export function prepareRequest(raw) {
  const request = createRequest(raw);
  const body = {model: request.model, input: request.input, ...(request.instructions ? {instructions: request.instructions} : {}),
    max_output_tokens: request.maxOutputTokens, store: false, stream: false, background: false,
    service_tier: 'default', tools: [], tool_choice: 'none', text: {format: {type: 'text'}}, truncation: 'disabled'};
  const serialized = JSON.stringify(body);
  return {request, serialized, requestSha256: sha256(serialized)};
}
export function usdMicros(value) {
  requireThat(typeof value === 'string' && /^(0|[1-9][0-9]{0,5})(?:\.[0-9]{1,6})?$/.test(value), 'invalid_usd_decimal');
  const [whole, fractional = ''] = value.split('.');
  return BigInt(whole) * 1000000n + BigInt(fractional.padEnd(6, '0'));
}
export function integerMicros(value) {
  requireThat(typeof value === 'string' && /^(0|[1-9][0-9]{0,17})$/.test(value), 'invalid_micros');
  return BigInt(value);
}
export function normalizeQuote(raw, prepared, execution, now = Date.now()) {
  requireThat(raw !== null && raw !== undefined, 'pricing_and_token_evidence_required');
  shape(raw, ['schema', 'kind', 'provider', 'model', 'requestSha256', 'currency', 'serviceTier', 'inputTokensUpperBound',
    'inputCountVerified', 'inputCountSource', 'inputUsdPerMillion', 'outputUsdPerMillion', 'fixedFeeUsd', 'allChargesCovered',
    'source', 'verifiedAt', 'expiresAt', 'approvedResponseModels'], 'invalid_quote_fields');
  requireThat(raw.schema === 'ghc.sentinel.quote.v1' && ['verified', 'fixture'].includes(raw.kind), 'invalid_quote');
  requireThat(execution !== 'live' || raw.kind === 'verified', 'fixture_pricing_not_live');
  requireThat(raw.provider === prepared.request.provider && raw.model === prepared.request.model && raw.requestSha256 === prepared.requestSha256, 'quote_request_mismatch');
  const responseModels = raw.approvedResponseModels ?? [raw.model];
  requireThat(Array.isArray(responseModels) && responseModels.length >= 1 && responseModels.length <= 8 && responseModels.every(modelId) && responseModels.includes(raw.model), 'invalid_quote');
  requireThat(raw.currency === 'USD' && raw.serviceTier === 'default' && raw.allChargesCovered === true, 'incomplete_price_coverage');
  requireThat(raw.inputCountVerified === true && raw.inputCountSource === 'responses/input_tokens', 'verified_input_bound_required');
  requireThat(Number.isSafeInteger(raw.inputTokensUpperBound) && raw.inputTokensUpperBound >= 1 && raw.inputTokensUpperBound <= 10000000, 'invalid_input_token_bound');
  const iso = value => typeof value === 'string' && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/.test(value);
  requireThat(iso(raw.verifiedAt) && iso(raw.expiresAt), 'quote_expired_or_invalid');
  const verifiedAt = Date.parse(raw.verifiedAt), expiresAt = Date.parse(raw.expiresAt);
  requireThat(Number.isFinite(verifiedAt) && Number.isFinite(expiresAt) && verifiedAt <= now && expiresAt > now && expiresAt - verifiedAt <= 86400000, 'quote_expired_or_invalid');
  if (raw.kind === 'verified') {
    let url; try { url = new URL(raw.source); } catch { throw new SentinelError('invalid_price_source'); }
    requireThat(url.protocol === 'https:' && ['developers.openai.com', 'platform.openai.com'].includes(url.hostname) && !url.username && !url.password && !url.search && !url.hash, 'invalid_price_source');
  } else requireThat(raw.source === 'fixture://synthetic-prices-not-real', 'invalid_fixture_source');
  const quote = Object.freeze({kind: raw.kind, model: raw.model, inputBound: raw.inputTokensUpperBound,
    inputRate: usdMicros(raw.inputUsdPerMillion), outputRate: usdMicros(raw.outputUsdPerMillion), fee: usdMicros(raw.fixedFeeUsd),
    fingerprint: sha256(JSON.stringify(raw)), source: raw.source, responseModels: Object.freeze([...responseModels])});
  return quote;
}
export function upperCost(quote, inputTokens, outputTokens) {
  requireThat(Number.isSafeInteger(inputTokens) && inputTokens >= 0 && Number.isSafeInteger(outputTokens) && outputTokens >= 0, 'invalid_usage');
  const ceil = value => (value + 999999n) / 1000000n;
  return ceil(quote.inputRate * BigInt(inputTokens)) + ceil(quote.outputRate * BigInt(outputTokens)) + quote.fee;
}
export function offlinePlan(raw, {quote = null, budget = null, execution = 'live', now = Date.now()} = {}) {
  const prepared = prepareRequest(raw);
  const blockers = [];
  let reserveMicros = null;
  try { const price = normalizeQuote(quote, prepared, execution, now); reserveMicros = upperCost(price, price.inputBound, prepared.request.maxOutputTokens).toString(); }
  catch (error) { blockers.push(error.code ?? 'invalid_quote'); }
  if (!budget?.known) blockers.push('known_available_budget_required');
  else if (budget.overrun) blockers.push('ledger_overrun_requires_review');
  else if (reserveMicros !== null && BigInt(reserveMicros) > BigInt(budget.availableMicros)) blockers.push('insufficient_local_budget');
  return {schema: 'ghc.sentinel.runtime.plan.v1', provider: prepared.request.provider, model: prepared.request.model,
    sentinelId: prepared.request.sentinelId, method: 'POST', endpoint: ENDPOINT, requestSha256: prepared.requestSha256,
    inputBytes: Buffer.byteLength(prepared.request.input) + Buffer.byteLength(prepared.request.instructions),
    maxOutputTokens: prepared.request.maxOutputTokens, reserveMicros, blockers, eligibleForExplicitExecution: blockers.length === 0,
    networkCalls: 0, automaticRetries: 0, apiTools: [], maxRequests: 1, aggregateUsd50Enforced: false,
    modelAccessVerified: false, modelTrained: false, weightsAvailable: false, worldModelEstablished: false, multimodalImplemented: false};
}
