'use strict';

const crypto = require('crypto');

function stable(value) {
  if (Array.isArray(value)) return value.map(stable);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, stable(value[key])]));
  }
  return value;
}

function digest(value) {
  return crypto.createHash('sha256').update(JSON.stringify(stable(value))).digest('hex');
}

function fail(code) {
  const error = new Error(code);
  error.code = code;
  throw error;
}

function validate(request) {
  const required = ['op', 'profile_id', 'points', 'relation', 'map'];
  if (!request || typeof request !== 'object' || required.some((key) => !(key in request))) fail('field_set');
  if (!Array.isArray(request.points) || request.points.length < 3 || request.points.length > 5) fail('points_shape');
  if (request.points.some((point) => typeof point !== 'string') || new Set(request.points).size !== request.points.length) fail('points_unique');
  const pointSet = new Set(request.points);
  if (!Array.isArray(request.relation) || request.relation.some((pair) => !Array.isArray(pair) || pair.length !== 2)) fail('relation_shape');
  if (request.relation.some(([a, b]) => !pointSet.has(a) || !pointSet.has(b))) fail('relation_member');
  const pairs = new Set(request.relation.map(([a, b]) => `${a}\u0000${b}`));
  if (request.points.some((point) => !pairs.has(`${point}\u0000${point}`))) fail('relation_reflexive');
  for (const a of request.points) {
    for (const b of request.points) {
      for (const c of request.points) {
        if (pairs.has(`${a}\u0000${b}`) && pairs.has(`${b}\u0000${c}`) && !pairs.has(`${a}\u0000${c}`)) fail('relation_transitive');
      }
    }
  }
  if (!request.map || typeof request.map !== 'object' || request.points.some((point) => !pointSet.has(request.map[point]))) fail('map_shape');
  return { points: [...request.points], pairs };
}

function subsets(points) {
  const out = [];
  function visit(index, current) {
    if (index === points.length) {
      out.push([...current]);
      return;
    }
    visit(index + 1, current);
    current.push(points[index]);
    visit(index + 1, current);
    current.pop();
  }
  visit(0, []);
  return out.sort((a, b) => a.length - b.length || a.join('|').localeCompare(b.join('|')));
}

function openSets(points, pairs) {
  return subsets(points).filter((candidate) => {
    const held = new Set(candidate);
    for (const x of candidate) {
      for (const y of points) {
        if (pairs.has(`${x}\u0000${y}`) && !held.has(y)) return false;
      }
    }
    return true;
  });
}

function complements(points, sets) {
  return sets.map((set) => {
    const held = new Set(set);
    return points.filter((point) => !held.has(point));
  }).sort((a, b) => a.length - b.length || a.join('|').localeCompare(b.join('|')));
}

function union(sets, points) {
  const held = new Set();
  for (const set of sets) for (const point of set) held.add(point);
  return points.filter((point) => held.has(point));
}

function intersection(sets, points) {
  if (!sets.length) return [...points];
  return points.filter((point) => sets.every((set) => set.includes(point)));
}

function setKey(set) {
  return set.join('|');
}

function histogram(sets, n) {
  const bins = Array(n + 1).fill(0);
  for (const set of sets) bins[set.length] += 1;
  return bins;
}

function connectedComponents(points, pairs) {
  const remaining = new Set(points);
  const components = [];
  while (remaining.size) {
    const start = [...remaining].sort()[0];
    const queue = [start];
    const component = [];
    remaining.delete(start);
    while (queue.length) {
      const x = queue.shift();
      component.push(x);
      for (const y of [...remaining]) {
        if (pairs.has(`${x}\u0000${y}`) || pairs.has(`${y}\u0000${x}`)) {
          remaining.delete(y);
          queue.push(y);
        }
      }
    }
    components.push(component.sort());
  }
  return components.sort((a, b) => a[0].localeCompare(b[0]));
}

function permutations(items) {
  if (items.length < 2) return [items.slice()];
  const out = [];
  for (let i = 0; i < items.length; i += 1) {
    const head = items[i];
    const tail = items.slice(0, i).concat(items.slice(i + 1));
    for (const rest of permutations(tail)) out.push([head, ...rest]);
  }
  return out;
}

function canonicalRelation(points, pairs) {
  const encodings = [];
  let automorphisms = 0;
  const original = points.flatMap((a) => points.map((b) => pairs.has(`${a}\u0000${b}`) ? '1' : '0')).join('');
  for (const order of permutations(points)) {
    const mapping = Object.fromEntries(points.map((point, index) => [point, order[index]]));
    let bits = '';
    for (const a of points) for (const b of points) bits += pairs.has(`${mapping[a]}\u0000${mapping[b]}`) ? '1' : '0';
    encodings.push(bits);
    if (bits === original) automorphisms += 1;
  }
  encodings.sort();
  return { canonical_bits: encodings[0], automorphism_count: automorphisms };
}

function quotientClasses(points, pairs) {
  const unseen = new Set(points);
  const classes = [];
  while (unseen.size) {
    const point = [...unseen].sort()[0];
    const klass = points.filter((other) => pairs.has(`${point}\u0000${other}`) && pairs.has(`${other}\u0000${point}`));
    for (const member of klass) unseen.delete(member);
    classes.push(klass.sort());
  }
  return classes.sort((a, b) => a[0].localeCompare(b[0]));
}

function evaluate(request) {
  const { points, pairs } = validate(request);
  const opens = openSets(points, pairs);
  const closed = complements(points, opens);
  const all = subsets(points);
  const interiors = all.map((set) => ({ subset: set, value: union(opens.filter((open) => open.every((point) => set.includes(point))), points) }));
  const closures = all.map((set) => ({ subset: set, value: intersection(closed.filter((item) => set.every((point) => item.includes(point))), points) }));
  const op = request.op;
  if (op === 'topology_record') {
    return { profile_id: request.profile_id, point_count: points.length, relation_pairs: request.relation.length, reflexive: true, transitive: true };
  }
  if (op === 'open_set_census') return { count: opens.length, cardinality_histogram: histogram(opens, points.length), open_sets: opens };
  if (op === 'closed_set_census') return { count: closed.length, cardinality_histogram: histogram(closed, points.length), closed_sets: closed };
  if (op === 'interior_signature') return { entries: interiors, digest: digest(interiors) };
  if (op === 'closure_signature') return { entries: closures, digest: digest(closures) };
  if (op === 'boundary_signature') {
    const entries = all.map((set, index) => {
      const interior = new Set(interiors[index].value);
      return { subset: set, value: closures[index].value.filter((point) => !interior.has(point)) };
    });
    return { entries, digest: digest(entries) };
  }
  if (op === 'specialization_preorder') return { relation: request.relation, pair_count: request.relation.length };
  if (op === 'minimal_neighborhoods') {
    const entries = points.map((point) => ({ point, neighborhood: intersection(opens.filter((open) => open.includes(point)), points) }));
    return { entries, digest: digest(entries) };
  }
  if (op === 'connected_components') {
    const components = connectedComponents(points, pairs);
    return { components, count: components.length };
  }
  if (op === 'basis_certificate') {
    const basis = points.map((point) => intersection(opens.filter((open) => open.includes(point)), points));
    const unique = [...new Map(basis.map((set) => [setKey(set), set])).values()].sort((a, b) => a.length - b.length || setKey(a).localeCompare(setKey(b)));
    const reconstructed = [...new Map(subsets(unique).map((selection) => [setKey(union(selection, points)), union(selection, points)])).values()]
      .sort((a, b) => a.length - b.length || setKey(a).localeCompare(setKey(b)));
    return { minimal_basis: unique, reconstructs: digest(reconstructed) === digest(opens), topology_digest: digest(opens) };
  }
  if (op === 'continuity_certificate') {
    const violations = opens.filter((open) => {
      const preimage = points.filter((point) => open.includes(request.map[point]));
      return !opens.some((candidate) => setKey(candidate) === setKey(preimage));
    });
    return { continuous: violations.length === 0, violating_open_sets: violations };
  }
  if (op === 'homeomorphism_signature') return canonicalRelation(points, pairs);
  if (op === 'subspace_topology') {
    const subset = points.slice(0, -1);
    const projected = [...new Map(opens.map((open) => {
      const value = open.filter((point) => subset.includes(point));
      return [setKey(value), value];
    })).values()].sort((a, b) => a.length - b.length || setKey(a).localeCompare(setKey(b)));
    return { points: subset, open_sets: projected, count: projected.length };
  }
  if (op === 'quotient_topology') {
    const classes = quotientClasses(points, pairs);
    const classLabels = classes.map((_, index) => `q${index + 1}`);
    const quotientOpens = subsets(classLabels).filter((candidate) => {
      const preimage = candidate.flatMap((label) => classes[classLabels.indexOf(label)]).sort();
      return opens.some((open) => setKey(open) === setKey(preimage));
    });
    return { classes, open_sets: quotientOpens, count: quotientOpens.length };
  }
  if (op === 'product_sierpinski') {
    const product = points.flatMap((point) => [`${point}:0`, `${point}:1`]);
    const productPairs = new Set();
    for (const a of points) for (const b of points) {
      if (!pairs.has(`${a}\u0000${b}`)) continue;
      productPairs.add(`${a}:0\u0000${b}:0`);
      productPairs.add(`${a}:0\u0000${b}:1`);
      productPairs.add(`${a}:1\u0000${b}:1`);
    }
    const productOpens = openSets(product, productPairs);
    return { point_count: product.length, open_set_count: productOpens.length, open_set_histogram: histogram(productOpens, product.length) };
  }
  if (op === 't0_quotient') {
    const classes = quotientClasses(points, pairs);
    const relation = [];
    for (let i = 0; i < classes.length; i += 1) for (let j = 0; j < classes.length; j += 1) {
      if (pairs.has(`${classes[i][0]}\u0000${classes[j][0]}`)) relation.push([`q${i + 1}`, `q${j + 1}`]);
    }
    return { is_t0: classes.every((klass) => klass.length === 1), classes, quotient_relation: relation };
  }
  if (op === 'accessible_summary') {
    const components = connectedComponents(points, pairs);
    return { text: `${request.profile_id}: ${points.length} points, ${opens.length} open sets, ${components.length} connected components; synthetic finite topology only.`, table_rows: points.length, manual_evaluation: 'open_gap' };
  }
  if (op === 'uncertainty_annotation') return { state: 'not_estimated', reason: 'No observation or sampling model exists for this finite fixture.', promotion_forbidden: true };
  if (op === 'external_evidence_gap') return { state: 'open_gap', missing: ['real wayfinding environment', 'affected-user evaluation', 'independent implementation'], zero_credit: true };
  if (op === 'topology_authority_gate') return { state: 'exact_gate', held_actions: ['publish real route', 'claim accessibility conformance', 'make safety or cultural decision'], executed: false };
  fail('operation');
}

module.exports = { evaluate, stable, digest };
