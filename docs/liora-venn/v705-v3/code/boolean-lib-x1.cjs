'use strict';

class BooleanContractError extends Error {
  constructor(code, message) { super(message); this.code = code; }
}

const X1_OPERATIONS = Object.freeze([
  'truth_table_integrity',
  'essential_variable_support',
  'hamming_weight_balance',
  'algebraic_normal_form',
  'algebraic_degree',
  'walsh_hadamard_spectrum',
  'spectral_nonlinearity',
  'xor_autocorrelation',
  'correlation_immunity_order',
  'resilience_profile'
]);

function popcount(value) {
  let count = 0;
  for (let x = value >>> 0; x; x >>>= 1) count += x & 1;
  return count;
}

function parity(value) { return popcount(value) & 1; }

function bits(index, variables) {
  return Array.from({ length: variables }, (_, bit) => (index >> bit) & 1);
}

function validateRequest(request, allowedOperations = X1_OPERATIONS) {
  if (!request || typeof request !== 'object' || Array.isArray(request)) throw new BooleanContractError('REQUEST_OBJECT', 'Request must be an object.');
  if (request.real_authority || request.production || request.empirical_claim || request.participant_data) throw new BooleanContractError('AUTHORITY', 'Authority-bearing or real-world envelopes are refused.');
  const allowed = new Set(['schema', 'fixture_id', 'label', 'variables', 'truth_table', 'operation', 'purpose']);
  for (const key of Object.keys(request)) if (!allowed.has(key)) throw new BooleanContractError('UNKNOWN_FIELD', `Unknown field: ${key}`);
  if (request.schema !== 'ghc.family.boolean-function.request.v1') throw new BooleanContractError('SCHEMA', 'Unsupported schema.');
  if (request.purpose !== 'public_synthetic') throw new BooleanContractError('PURPOSE', 'Only public synthetic fixtures are accepted.');
  if (!Number.isInteger(request.variables) || request.variables < 1 || request.variables > 6) throw new BooleanContractError('VARIABLES', 'Variables must be an integer from 1 through 6.');
  if (!Array.isArray(request.truth_table)) throw new BooleanContractError('TRUTH_TABLE', 'Truth table must be an array.');
  if (request.truth_table.length !== (1 << request.variables)) throw new BooleanContractError('TABLE_LENGTH', 'Truth-table length must equal 2^variables.');
  if (request.truth_table.some(value => value !== 0 && value !== 1)) throw new BooleanContractError('BINARY', 'Truth-table values must be zero or one.');
  if (!allowedOperations.includes(request.operation)) throw new BooleanContractError('OPERATION', 'Operation is not admitted in this lifecycle stage.');
  return {
    fixture_id: request.fixture_id,
    label: request.label,
    variables: request.variables,
    truth_table: request.truth_table.slice(),
    operation: request.operation
  };
}

function anfCoefficients(table, variables) {
  const coefficients = table.slice();
  for (let bit = 0; bit < variables; bit += 1) {
    for (let mask = 0; mask < coefficients.length; mask += 1) {
      if (mask & (1 << bit)) coefficients[mask] ^= coefficients[mask ^ (1 << bit)];
    }
  }
  return coefficients;
}

function evaluateAnf(coefficients, index) {
  let value = 0;
  for (let mask = 0; mask < coefficients.length; mask += 1) {
    if (coefficients[mask] && (index & mask) === mask) value ^= 1;
  }
  return value;
}

function essentialVariables(table, variables) {
  const support = [];
  for (let bit = 0; bit < variables; bit += 1) {
    let essential = false;
    for (let index = 0; index < table.length; index += 1) {
      if (table[index] !== table[index ^ (1 << bit)]) { essential = true; break; }
    }
    if (essential) support.push(bit);
  }
  return support;
}

function walshSpectrum(table, variables) {
  const spectrum = [];
  for (let mask = 0; mask < table.length; mask += 1) {
    let total = 0;
    for (let index = 0; index < table.length; index += 1) total += (table[index] ^ parity(mask & index)) ? -1 : 1;
    spectrum.push(total);
  }
  return spectrum;
}

function autocorrelation(table) {
  const values = [];
  for (let shift = 0; shift < table.length; shift += 1) {
    let total = 0;
    for (let index = 0; index < table.length; index += 1) total += (table[index] ^ table[index ^ shift]) ? -1 : 1;
    values.push(total);
  }
  return values;
}

function correlationImmunity(spectrum, variables) {
  let order = 0;
  for (let candidate = 1; candidate <= variables; candidate += 1) {
    let valid = true;
    for (let mask = 1; mask < spectrum.length; mask += 1) {
      if (popcount(mask) <= candidate && spectrum[mask] !== 0) { valid = false; break; }
    }
    if (!valid) break;
    order = candidate;
  }
  return order;
}

function common(request) {
  const q = validateRequest(request);
  const coefficients = anfCoefficients(q.truth_table, q.variables);
  const spectrum = walshSpectrum(q.truth_table, q.variables);
  const weight = q.truth_table.reduce((sum, value) => sum + value, 0);
  const support = essentialVariables(q.truth_table, q.variables);
  const degree = coefficients.reduce((maximum, coefficient, mask) => coefficient ? Math.max(maximum, popcount(mask)) : maximum, -1);
  const maxWalsh = Math.max(...spectrum.map(Math.abs));
  const immunity = correlationImmunity(spectrum, q.variables);
  return { q, coefficients, spectrum, weight, support, degree, maxWalsh, immunity };
}

function computeOperation(request) {
  const c = common(request);
  const { q } = c;
  switch (q.operation) {
    case 'truth_table_integrity':
      return { variables: q.variables, entries: q.truth_table.length, binary: true, power_of_two: true, input_preserved: q.truth_table };
    case 'essential_variable_support':
      return { essential_variables: c.support, essential_count: c.support.length, declared_variables: q.variables };
    case 'hamming_weight_balance':
      return { weight: c.weight, zeros: q.truth_table.length - c.weight, balanced: c.weight * 2 === q.truth_table.length };
    case 'algebraic_normal_form':
      return { coefficients: c.coefficients, monomial_masks: c.coefficients.map((value, mask) => value ? mask : null).filter(value => value !== null), roundtrip: c.coefficients.map((_, index) => evaluateAnf(c.coefficients, index)) };
    case 'algebraic_degree':
      return { degree: c.degree, convention: 'zero_function_degree_minus_one' };
    case 'walsh_hadamard_spectrum':
      return { spectrum: c.spectrum, parseval_sum: c.spectrum.reduce((sum, value) => sum + value * value, 0), zero_frequency: c.spectrum[0] };
    case 'spectral_nonlinearity':
      return { maximum_absolute_walsh: c.maxWalsh, nonlinearity: (q.truth_table.length - c.maxWalsh) / 2 };
    case 'xor_autocorrelation': {
      const values = autocorrelation(q.truth_table);
      return { autocorrelation: values, zero_shift: values[0], absolute_indicator_nonzero: Math.max(...values.slice(1).map(Math.abs), 0) };
    }
    case 'correlation_immunity_order':
      return { order: c.immunity, walsh_criterion: true };
    case 'resilience_profile': {
      const balanced = c.weight * 2 === q.truth_table.length;
      return { balanced, correlation_immunity_order: c.immunity, resilient_order: balanced ? c.immunity : -1 };
    }
    default:
      throw new BooleanContractError('OPERATION', 'Unsupported X1 operation.');
  }
}

module.exports = {
  BooleanContractError,
  X1_OPERATIONS,
  popcount,
  parity,
  bits,
  validateRequest,
  anfCoefficients,
  evaluateAnf,
  essentialVariables,
  walshSpectrum,
  autocorrelation,
  correlationImmunity,
  computeOperation
};
