'use strict';

const crypto = require('crypto');

function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === 'object') {
    const output = {};
    for (const key of Object.keys(value).sort()) output[key] = canonical(value[key]);
    return output;
  }
  return value;
}

function digest(value) {
  return crypto.createHash('sha256').update(JSON.stringify(canonical(value))).digest('hex');
}

function reject(code) {
  const error = new Error(code);
  error.code = code;
  throw error;
}

function context(request) {
  if (!request || typeof request !== 'object') reject('field_set');
  for (const key of ['op', 'profile_id', 'points', 'relation', 'map']) if (!(key in request)) reject('field_set');
  const points = request.points;
  if (!Array.isArray(points) || points.length < 3 || points.length > 5) reject('points_shape');
  if (points.some((point) => typeof point !== 'string') || new Set(points).size !== points.length) reject('points_unique');
  const index = new Map(points.map((point, position) => [point, position]));
  if (!Array.isArray(request.relation)) reject('relation_shape');
  const n = points.length;
  const matrix = Array.from({ length: n }, () => Array(n).fill(false));
  for (const pair of request.relation) {
    if (!Array.isArray(pair) || pair.length !== 2) reject('relation_shape');
    if (!index.has(pair[0]) || !index.has(pair[1])) reject('relation_member');
    matrix[index.get(pair[0])][index.get(pair[1])] = true;
  }
  for (let i = 0; i < n; i += 1) if (!matrix[i][i]) reject('relation_reflexive');
  for (let k = 0; k < n; k += 1) for (let i = 0; i < n; i += 1) for (let j = 0; j < n; j += 1) {
    if (matrix[i][k] && matrix[k][j] && !matrix[i][j]) reject('relation_transitive');
  }
  if (!request.map || typeof request.map !== 'object' || points.some((point) => !index.has(request.map[point]))) reject('map_shape');
  return { points: [...points], index, matrix, n };
}

function masks(n) {
  return Array.from({ length: 1 << n }, (_, mask) => mask);
}

function toSet(mask, points) {
  const out = [];
  for (let i = 0; i < points.length; i += 1) if (mask & (1 << i)) out.push(points[i]);
  return out;
}

function sortSets(sets) {
  return sets.sort((a, b) => a.length - b.length || a.join('|').localeCompare(b.join('|')));
}

function openMasks(matrix, n) {
  return masks(n).filter((mask) => {
    for (let i = 0; i < n; i += 1) {
      if (!(mask & (1 << i))) continue;
      for (let j = 0; j < n; j += 1) if (matrix[i][j] && !(mask & (1 << j))) return false;
    }
    return true;
  });
}

function bitCount(mask) {
  let value = mask;
  let count = 0;
  while (value) {
    count += value & 1;
    value >>>= 1;
  }
  return count;
}

function hist(open, n) {
  const out = Array(n + 1).fill(0);
  for (const mask of open) out[bitCount(mask)] += 1;
  return out;
}

function components(matrix, points) {
  const seen = new Set();
  const out = [];
  for (let start = 0; start < points.length; start += 1) {
    if (seen.has(start)) continue;
    const queue = [start];
    seen.add(start);
    const component = [];
    while (queue.length) {
      const i = queue.shift();
      component.push(points[i]);
      for (let j = 0; j < points.length; j += 1) {
        if (!seen.has(j) && (matrix[i][j] || matrix[j][i])) {
          seen.add(j);
          queue.push(j);
        }
      }
    }
    out.push(component.sort());
  }
  return out.sort((a, b) => a[0].localeCompare(b[0]));
}

function permute(values) {
  const result = [];
  function visit(prefix, remaining) {
    if (!remaining.length) {
      result.push(prefix);
      return;
    }
    for (let i = 0; i < remaining.length; i += 1) {
      visit(prefix.concat(remaining[i]), remaining.slice(0, i).concat(remaining.slice(i + 1)));
    }
  }
  visit([], values);
  return result;
}

function canonicalSignature(matrix, n) {
  const identity = Array.from({ length: n }, (_, index) => index);
  const encodings = [];
  let automorphismCount = 0;
  const original = matrix.flat().map(Boolean).map((value) => value ? '1' : '0').join('');
  for (const permutation of permute(identity)) {
    let bits = '';
    for (let i = 0; i < n; i += 1) for (let j = 0; j < n; j += 1) bits += matrix[permutation[i]][permutation[j]] ? '1' : '0';
    encodings.push(bits);
    if (bits === original) automorphismCount += 1;
  }
  encodings.sort();
  return { canonical_bits: encodings[0], automorphism_count: automorphismCount };
}

function classIndices(matrix, n) {
  const used = new Set();
  const classes = [];
  for (let i = 0; i < n; i += 1) {
    if (used.has(i)) continue;
    const klass = [];
    for (let j = 0; j < n; j += 1) if (matrix[i][j] && matrix[j][i]) {
      klass.push(j);
      used.add(j);
    }
    classes.push(klass);
  }
  return classes;
}

function evaluate(request) {
  const { points, index, matrix, n } = context(request);
  const allMasks = masks(n);
  const orderedMasks = [...allMasks].sort((a, b) => bitCount(a) - bitCount(b) || toSet(a, points).join('|').localeCompare(toSet(b, points).join('|')));
  const opensMasks = openMasks(matrix, n);
  const full = (1 << n) - 1;
  const closedMasks = opensMasks.map((mask) => full ^ mask).sort((a, b) => bitCount(a) - bitCount(b) || a - b);
  const opens = sortSets(opensMasks.map((mask) => toSet(mask, points)));
  const closed = sortSets(closedMasks.map((mask) => toSet(mask, points)));
  const interiorMasks = allMasks.map((mask) => opensMasks.reduce((value, candidate) => (candidate & ~mask) === 0 ? value | candidate : value, 0));
  const closureMasks = allMasks.map((mask) => closedMasks.reduce((value, candidate) => (mask & ~candidate) === 0 ? value & candidate : value, full));
  switch (request.op) {
    case 'topology_record':
      return { profile_id: request.profile_id, point_count: n, relation_pairs: request.relation.length, reflexive: true, transitive: true };
    case 'open_set_census':
      return { count: opens.length, cardinality_histogram: hist(opensMasks, n), open_sets: opens };
    case 'closed_set_census':
      return { count: closed.length, cardinality_histogram: hist(closedMasks, n), closed_sets: closed };
    case 'interior_signature': {
      const entries = orderedMasks.map((mask) => ({ subset: toSet(mask, points), value: toSet(interiorMasks[mask], points) }));
      return { entries, digest: digest(entries) };
    }
    case 'closure_signature': {
      const entries = orderedMasks.map((mask) => ({ subset: toSet(mask, points), value: toSet(closureMasks[mask], points) }));
      return { entries, digest: digest(entries) };
    }
    case 'boundary_signature': {
      const entries = orderedMasks.map((mask) => ({ subset: toSet(mask, points), value: toSet(closureMasks[mask] & ~interiorMasks[mask], points) }));
      return { entries, digest: digest(entries) };
    }
    case 'specialization_preorder':
      return { relation: request.relation, pair_count: request.relation.length };
    case 'minimal_neighborhoods': {
      const entries = points.map((point, i) => ({ point, neighborhood: toSet(opensMasks.filter((mask) => mask & (1 << i)).reduce((value, mask) => value & mask, full), points) }));
      return { entries, digest: digest(entries) };
    }
    case 'connected_components': {
      const list = components(matrix, points);
      return { components: list, count: list.length };
    }
    case 'basis_certificate': {
      const basisMasks = points.map((_, i) => opensMasks.filter((mask) => mask & (1 << i)).reduce((value, mask) => value & mask, full));
      const uniqueMasks = [...new Set(basisMasks)].sort((a, b) => bitCount(a) - bitCount(b) || a - b);
      const generated = new Set([0]);
      for (const basis of uniqueMasks) for (const present of [...generated]) generated.add(present | basis);
      const generatedSets = sortSets([...generated].map((mask) => toSet(mask, points)));
      return { minimal_basis: sortSets(uniqueMasks.map((mask) => toSet(mask, points))), reconstructs: digest(generatedSets) === digest(opens), topology_digest: digest(opens) };
    }
    case 'continuity_certificate': {
      const imageIndex = points.map((point) => index.get(request.map[point]));
      const openMaskSet = new Set(opensMasks);
      const violations = [];
      for (const targetOpen of opensMasks) {
        let preimage = 0;
        for (let i = 0; i < n; i += 1) if (targetOpen & (1 << imageIndex[i])) preimage |= 1 << i;
        if (!openMaskSet.has(preimage)) violations.push(toSet(targetOpen, points));
      }
      return { continuous: violations.length === 0, violating_open_sets: sortSets(violations) };
    }
    case 'homeomorphism_signature':
      return canonicalSignature(matrix, n);
    case 'subspace_topology': {
      const subMask = (1 << (n - 1)) - 1;
      const projectedMasks = [...new Set(opensMasks.map((mask) => mask & subMask))].sort((a, b) => bitCount(a) - bitCount(b) || a - b);
      return { points: points.slice(0, -1), open_sets: sortSets(projectedMasks.map((mask) => toSet(mask, points.slice(0, -1)))), count: projectedMasks.length };
    }
    case 'quotient_topology': {
      const classes = classIndices(matrix, n);
      const labels = classes.map((_, position) => `q${position + 1}`);
      const quotient = [];
      for (const classMask of masks(classes.length)) {
        let preimage = 0;
        for (let c = 0; c < classes.length; c += 1) if (classMask & (1 << c)) for (const member of classes[c]) preimage |= 1 << member;
        if (opensMasks.includes(preimage)) quotient.push(toSet(classMask, labels));
      }
      return { classes: classes.map((klass) => klass.map((i) => points[i])), open_sets: sortSets(quotient), count: quotient.length };
    }
    case 'product_sierpinski': {
      const productN = n * 2;
      const productMatrix = Array.from({ length: productN }, () => Array(productN).fill(false));
      for (let i = 0; i < n; i += 1) for (let j = 0; j < n; j += 1) if (matrix[i][j]) {
        productMatrix[i * 2][j * 2] = true;
        productMatrix[i * 2][j * 2 + 1] = true;
        productMatrix[i * 2 + 1][j * 2 + 1] = true;
      }
      const productOpen = openMasks(productMatrix, productN);
      return { point_count: productN, open_set_count: productOpen.length, open_set_histogram: hist(productOpen, productN) };
    }
    case 't0_quotient': {
      const classes = classIndices(matrix, n);
      const classLabels = classes.map((_, i) => `q${i + 1}`);
      const quotientRelation = [];
      for (let i = 0; i < classes.length; i += 1) for (let j = 0; j < classes.length; j += 1) if (matrix[classes[i][0]][classes[j][0]]) quotientRelation.push([classLabels[i], classLabels[j]]);
      return { is_t0: classes.every((klass) => klass.length === 1), classes: classes.map((klass) => klass.map((i) => points[i])), quotient_relation: quotientRelation };
    }
    case 'accessible_summary': {
      const list = components(matrix, points);
      return { text: `${request.profile_id}: ${n} points, ${opens.length} open sets, ${list.length} connected components; synthetic finite topology only.`, table_rows: n, manual_evaluation: 'open_gap' };
    }
    case 'uncertainty_annotation':
      return { state: 'not_estimated', reason: 'No observation or sampling model exists for this finite fixture.', promotion_forbidden: true };
    case 'external_evidence_gap':
      return { state: 'open_gap', missing: ['real wayfinding environment', 'affected-user evaluation', 'independent implementation'], zero_credit: true };
    case 'topology_authority_gate':
      return { state: 'exact_gate', held_actions: ['publish real route', 'claim accessibility conformance', 'make safety or cultural decision'], executed: false };
    default:
      reject('operation');
  }
}

module.exports = { evaluate, canonical, digest };
