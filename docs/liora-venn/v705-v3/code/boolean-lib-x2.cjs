'use strict';

const x1 = require('./boolean-lib-x1.cjs');

const X2_OPERATIONS = Object.freeze([
  'partial_order_monotonicity',
  'variable_unateness',
  'canalizing_assignments',
  'permutation_symmetry_group',
  'mobius_roundtrip',
  'cofactor_restriction_pair',
  'boolean_derivative_influence',
  'affine_input_orbit_signature',
  'independent_boolean_reproduction_gap',
  'boolean_decision_authority_hold'
]);

function permutations(values) {
  if (values.length < 2) return [values.slice()];
  const output = [];
  for (let i = 0; i < values.length; i += 1) {
    const rest = values.slice(0, i).concat(values.slice(i + 1));
    for (const tail of permutations(rest)) output.push([values[i], ...tail]);
  }
  return output;
}

function permuteIndex(index, permutation) {
  let output = 0;
  for (let bit = 0; bit < permutation.length; bit += 1) output |= ((index >> permutation[bit]) & 1) << bit;
  return output;
}

function monotonicity(table) {
  const violations = [];
  for (let lower = 0; lower < table.length; lower += 1) {
    for (let upper = 0; upper < table.length; upper += 1) {
      if ((lower & ~upper) === 0 && table[lower] > table[upper]) violations.push([lower, upper]);
    }
  }
  return { monotone: violations.length === 0, violations };
}

function unateness(table, variables) {
  const coordinates = [];
  for (let bit = 0; bit < variables; bit += 1) {
    let positive = true;
    let negative = true;
    for (let index = 0; index < table.length; index += 1) {
      if (index & (1 << bit)) continue;
      const low = table[index], high = table[index | (1 << bit)];
      if (low > high) positive = false;
      if (low < high) negative = false;
    }
    coordinates.push({ variable: bit, positive, negative, classification: positive && negative ? 'independent' : positive ? 'positive' : negative ? 'negative' : 'neither' });
  }
  return { coordinates, unate: coordinates.every(row => row.classification !== 'neither') };
}

function canalizing(table, variables) {
  const assignments = [];
  for (let bit = 0; bit < variables; bit += 1) {
    for (const value of [0, 1]) {
      const outputs = new Set();
      for (let index = 0; index < table.length; index += 1) if (((index >> bit) & 1) === value) outputs.add(table[index]);
      if (outputs.size === 1) assignments.push({ variable: bit, input_value: value, output_value: [...outputs][0] });
    }
  }
  return assignments;
}

function symmetryGroup(table, variables) {
  const candidates = permutations(Array.from({ length: variables }, (_, index) => index));
  const automorphisms = candidates.filter(permutation => table.every((value, index) => value === table[permuteIndex(index, permutation)]));
  return { permutations_considered: candidates.length, automorphism_count: automorphisms.length, automorphisms };
}

function cofactors(table, variables) {
  const rows = [];
  for (let bit = 0; bit < variables; bit += 1) {
    for (const value of [0, 1]) {
      const values = [];
      for (let index = 0; index < table.length; index += 1) if (((index >> bit) & 1) === value) values.push(table[index]);
      rows.push({ variable: bit, value, cofactor: values });
    }
  }
  return rows;
}

function derivatives(table, variables) {
  return Array.from({ length: variables }, (_, bit) => {
    const values = table.map((value, index) => value ^ table[index ^ (1 << bit)]);
    const weight = values.reduce((sum, value) => sum + value, 0);
    return { variable: bit, derivative: values, weight, influence_numerator: weight, influence_denominator: table.length };
  });
}

function applyMatrix(rows, value) {
  let output = 0;
  for (let bit = 0; bit < rows.length; bit += 1) output |= x1.parity(rows[bit] & value) << bit;
  return output;
}

function invertibleMatrices(variables) {
  const limit = 1 << variables;
  const rows = Array(variables).fill(0);
  const output = [];
  function visit(position) {
    if (position === variables) {
      const images = new Set(Array.from({ length: limit }, (_, value) => applyMatrix(rows, value)));
      if (images.size === limit) output.push(rows.slice());
      return;
    }
    for (let row = 0; row < limit; row += 1) { rows[position] = row; visit(position + 1); }
  }
  visit(0);
  return output;
}

function affineOrbit(table, variables) {
  const matrices = invertibleMatrices(variables);
  const orbit = new Set();
  for (const matrix of matrices) {
    for (let translation = 0; translation < table.length; translation += 1) {
      const transported = Array.from({ length: table.length }, (_, index) => table[applyMatrix(matrix, index) ^ translation]);
      orbit.add(transported.join(''));
    }
  }
  const signatures = [...orbit].sort();
  return { orbit_size: signatures.length, canonical_signature: signatures[0], transformations_considered: matrices.length * table.length, linear_maps: matrices.length, translations_per_map: table.length, represented_scope: 'input-affine-bijections-only' };
}

function computeOperation(request) {
  const q = x1.validateRequest(request, X2_OPERATIONS);
  switch (q.operation) {
    case 'partial_order_monotonicity': return monotonicity(q.truth_table);
    case 'variable_unateness': return unateness(q.truth_table, q.variables);
    case 'canalizing_assignments': return { assignments: canalizing(q.truth_table, q.variables), declared_variables: q.variables };
    case 'permutation_symmetry_group': return symmetryGroup(q.truth_table, q.variables);
    case 'mobius_roundtrip': {
      const coefficients = x1.anfCoefficients(q.truth_table, q.variables);
      const twice = x1.anfCoefficients(coefficients, q.variables);
      return { coefficients, transformed_twice: twice, roundtrip: JSON.stringify(twice) === JSON.stringify(q.truth_table) };
    }
    case 'cofactor_restriction_pair': return { cofactors: cofactors(q.truth_table, q.variables), pair_count: q.variables };
    case 'boolean_derivative_influence': return { derivatives: derivatives(q.truth_table, q.variables), exact_rational_only: true };
    case 'affine_input_orbit_signature': return affineOrbit(q.truth_table, q.variables);
    case 'independent_boolean_reproduction_gap': return { state: 'open_gap', executed: false, missing: ['independent implementation', 'external SageMath execution', 'independent review'] };
    case 'boolean_decision_authority_hold': return { state: 'exact_gate', executed: false, held: ['cryptographic suitability', 'hardware safety', 'professional decision', 'legal and cultural authority', 'affected-party and Maori authority'] };
    default: throw new x1.BooleanContractError('OPERATION', 'Unsupported X2 operation.');
  }
}

module.exports = { X2_OPERATIONS, permutations, permuteIndex, monotonicity, unateness, canalizing, symmetryGroup, cofactors, derivatives, invertibleMatrices, affineOrbit, computeOperation };
