const definitions = [
  ['nexus.chats.list', 'chats', false, 'List selected public chat aliases.'],
  ['nexus.chats.resolve', 'chats', true, 'Resolve a selected alias without private chat metadata.'],
  ['nexus.chats.plan', 'chats', true, 'Describe a reviewed chat route without sending messages.'],
  ['nexus.lab.catalogue', 'labs', false, 'List selected public lab aliases.'],
  ['nexus.lab.plan', 'labs', true, 'Describe a selected lab plan without running it.'],
  ['nexus.identity.summary', null, false, 'Return technical capabilities without personal contact fields.'],
  ['nexus.sentinel.validate', 'sentinels', true, 'Validate a selected reference without executing research.'],
  ['nexus.sentinel.plan', 'sentinels', true, 'Describe a selected Sentinel plan without executing it.'],
  ['nexus.remote.plan', 'remotes', true, 'Describe a reviewed remote route without connecting.']
];

export const TOOL_SPECS = Object.freeze(definitions.map(([name, domain, needsAlias, description]) =>
  Object.freeze({name, domain, needsAlias, description})));
export const ALIAS_PATTERN = '^[a-z][a-z0-9_-]{0,63}$';
export const MAX_SELECTED_ITEMS = 128;
const reserved = new Set(['constructor', 'prototype', '__proto__']);
const domains = ['chats', 'labs', 'sentinels', 'remotes'];
const routes = ['local', 'cloud', 'manual', 'unavailable'];
const steps = ['select', 'validate', 'review', 'handoff'];
const issues = ['missing_input', 'unsupported_format', 'unverified_source', 'invalid_fields', 'unavailable'];

const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const aliasValid = value => typeof value === 'string' && new RegExp(ALIAS_PATTERN).test(value) && !reserved.has(value);
function requireThat(condition) { if (!condition) throw new TypeError('Invalid public contract'); }
function boolean(value) { requireThat(typeof value === 'boolean'); return value; }
function enumeration(value, values) { requireThat(values.includes(value)); return value; }

export function copyRegistry(selectors) {
  requireThat(object(selectors) && Object.keys(selectors).every(key => domains.includes(key)));
  return Object.freeze(Object.fromEntries(domains.map(domain => {
    const values = selectors[domain];
    requireThat(Array.isArray(values) && values.length <= MAX_SELECTED_ITEMS && values.every(aliasValid));
    requireThat(new Set(values).size === values.length);
    return [domain, Object.freeze([...values])];
  })));
}

export function inputSchema(spec) {
  return {
    $schema: 'https://json-schema.org/draft/2020-12/schema',
    type: 'object',
    properties: spec.needsAlias ? {alias: {type: 'string', pattern: ALIAS_PATTERN, minLength: 1, maxLength: 64}} : {},
    ...(spec.needsAlias ? {required: ['alias']} : {}),
    additionalProperties: false
  };
}

export function safeArguments(spec, args, registry) {
  requireThat(object(args));
  if (!spec.needsAlias) {
    requireThat(Object.keys(args).length === 0);
    return Object.freeze({});
  }
  requireThat(Object.keys(args).length === 1 && Object.hasOwn(args, 'alias'));
  requireThat(aliasValid(args.alias) && registry[spec.domain].includes(args.alias));
  return Object.freeze({alias: args.alias});
}

/** Explicit projection: dispatcher output is never spread into a public result. */
export function publicProjection(spec, data, args, registry) {
  requireThat(object(data));
  if (spec.name === 'nexus.chats.list' || spec.name === 'nexus.lab.catalogue') {
    requireThat(Array.isArray(data.items) && data.items.length <= MAX_SELECTED_ITEMS);
    const seen = new Set();
    return {items: data.items.map(item => {
      requireThat(object(item) && registry[spec.domain].includes(item.alias) && !seen.has(item.alias));
      seen.add(item.alias);
      return {alias: item.alias, available: boolean(item.available)};
    })};
  }
  if (spec.name === 'nexus.identity.summary') {
    requireThat(object(data.capabilities));
    return {component: 'nexus-hub', platform: enumeration(data.platform, ['linux', 'win32', 'darwin', 'unknown']),
      capabilities: Object.fromEntries(['chats', 'lab', 'sentinel', 'remote'].map(key => [key, boolean(data.capabilities[key])]))};
  }
  if (spec.name === 'nexus.sentinel.validate') {
    requireThat([true, false, null].includes(data.valid) && Array.isArray(data.issues) && data.issues.length <= 8);
    return {alias: args.alias, valid: data.valid, issues: data.issues.map(value => enumeration(value, issues)), executed: false};
  }
  if (spec.name === 'nexus.chats.resolve') {
    return {alias: args.alias, available: boolean(data.available), route: enumeration(data.route, routes)};
  }
  requireThat(Array.isArray(data.steps) && data.steps.length <= 8);
  return {alias: args.alias, available: boolean(data.available), route: enumeration(data.route, routes),
    steps: data.steps.map(value => enumeration(value, steps)), requiresReview: true, executed: false};
}

const messages = Object.freeze({
  invalid_arguments: 'Use the declared schema and a reviewed alias.',
  operation_failed: 'The read-only operation failed.',
  invalid_output: 'The operation returned unsupported public data.',
  busy: 'A read-only operation is still active.',
  rate_limited: 'The read-only call rate limit was reached.',
  cancelled: 'The read-only operation was cancelled.',
  timeout: 'The read-only operation exceeded its deadline.'
});
export function toolFailure(code) {
  return {isError: true, content: [{type: 'text', text: messages[code] ?? messages.operation_failed}]};
}
export function toolSuccess(data) {
  return {isError: false, content: [{type: 'text', text: JSON.stringify(data)}], structuredContent: data};
}
