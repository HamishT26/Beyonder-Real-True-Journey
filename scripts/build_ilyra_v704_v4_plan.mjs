import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const root = path.resolve(process.argv[2] || process.cwd());
const phaseRoot = path.join(root, 'docs', 'ilyra-fen', 'v704-v4');
const planRoot = path.join(phaseRoot, 'planning');
const boundary = 'Finite synthetic same-owner mathematical and software evidence. No empirical GMUT confirmation, production THOS or Freed ID, independent reproduction, real participant evidence, identity, consciousness, personhood, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, AGI, ASI or Theory-of-Everything proof. NOT_READY_FOR_STAGE_20.';
const sourceFinal = 'f6c86fb56f5492d4d830b0439300001e54ba284f';
const sourceBase = path.join(root, 'docs', 'talen-briar', 'v704-v3-r2');

function mkdir(p) { fs.mkdirSync(p, { recursive: true }); }
function writeJson(p, value) { mkdir(path.dirname(p)); fs.writeFileSync(p, JSON.stringify(value, null, 2) + '\n', 'utf8'); }
function writeText(p, value) { mkdir(path.dirname(p)); fs.writeFileSync(p, value.endsWith('\n') ? value : value + '\n', 'utf8'); }
function shaBytes(b) { return crypto.createHash('sha256').update(b).digest('hex'); }
function shaObject(o) { return shaBytes(Buffer.from(JSON.stringify(o), 'utf8')); }
function gcd(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) [a, b] = [b, a % b]; return a || 1n; }

class Q {
  constructor(n, d = 1n) {
    if (d === 0n) throw new Error('zero denominator');
    if (d < 0n) { n = -n; d = -d; }
    const g = gcd(n, d); this.n = n / g; this.d = d / g;
  }
  static from(v) {
    if (v instanceof Q) return v;
    if (typeof v === 'bigint') return new Q(v);
    if (typeof v === 'number' && Number.isInteger(v)) return new Q(BigInt(v));
    const s = String(v); const [a, b] = s.split('/'); return new Q(BigInt(a), b ? BigInt(b) : 1n);
  }
  add(v) { v = Q.from(v); return new Q(this.n * v.d + v.n * this.d, this.d * v.d); }
  sub(v) { v = Q.from(v); return new Q(this.n * v.d - v.n * this.d, this.d * v.d); }
  mul(v) { v = Q.from(v); return new Q(this.n * v.n, this.d * v.d); }
  cmp(v) { v = Q.from(v); const z = this.n * v.d - v.n * this.d; return z < 0n ? -1 : z > 0n ? 1 : 0; }
  toString() { return this.d === 1n ? String(this.n) : `${this.n}/${this.d}`; }
}
const qsum = xs => xs.reduce((a, b) => a.add(b), new Q(0n));
const qdot = (a, b) => qsum(a.map((x, i) => Q.from(x).mul(b[i])));

function row(n, pairs) {
  const out = Array(n).fill('0');
  for (const [i, v] of pairs) out[i] = Q.from(v).toString();
  return out;
}

function makeProfile(i) {
  const n = 2 + (i % 2);
  const states = Array.from({ length: n }, (_, s) => `s${s}`);
  const discounts = ['1', '1/2', '3/4', '2/3', '1/3'];
  const rewards = states.map((_, s) => [
    String(((i + 2 * s) % 7) - 2),
    String(((2 * i + s + 3) % 8) - 3),
  ]);
  const terminal = states.map((_, s) => String(((i + s) % 5) - 2));
  const initial = states.map((_, s) => s === (i % n) ? '1' : '0');
  const fixedPolicy = states.map((_, s) => (i + s) % 2);
  const models = [0, 1].map(m => states.map((_, s) => [0, 1].map(a => {
    const target = (s + a + i + 1 + m) % n;
    if (m === 0 || target === s) return row(n, [[target, '1']]);
    return row(n, [[s, '1/2'], [target, '1/2']]);
  })));
  return {
    profile_id: `C${String(i + 1).padStart(2, '0')}`,
    label: [
      'two-state divergence anchor', 'three-state coupling cycle', 'horizon reversal',
      'symmetric tie profile', 'absorbing comparison', 'reward-shift profile',
      'discount sensitivity', 'terminal-dominant profile', 'model-deletion profile',
      'label-covariant profile', 'sparse-support profile', 'fractional reward profile',
      'mixture representation profile', 'calibration vacancy profile', 'authority vacancy profile'
    ][i],
    states, actions: ['a0', 'a1'], rewards, terminal,
    discount: discounts[i % discounts.length], horizon: 2 + (i % 3),
    initial, fixed_policy: fixedPolicy, global_models: models,
    uncertainty_contract: 'one model index is selected once and remains fixed across the complete finite trajectory'
  };
}

function policies(n) {
  return Array.from({ length: 2 ** n }, (_, k) => Array.from({ length: n }, (_, s) => (k >> s) & 1));
}

function evalPolicy(profile, policy, modelIndex, horizon = profile.horizon, discount = profile.discount) {
  let v = profile.terminal.map(Q.from);
  const d = Q.from(discount);
  const layers = [v.map(String)];
  for (let h = 1; h <= horizon; h++) {
    v = profile.states.map((_, s) => {
      const a = policy[s];
      const future = qdot(profile.global_models[modelIndex][s][a], v);
      return Q.from(profile.rewards[s][a]).add(d.mul(future));
    });
    layers.push(v.map(String));
  }
  return { vector: v.map(String), scalar: qdot(profile.initial, v).toString(), layers };
}

function policyTable(profile) {
  return policies(profile.states.length).map(policy => {
    const values = profile.global_models.map((_, m) => evalPolicy(profile, policy, m).scalar).map(Q.from);
    const lower = values.reduce((a, b) => a.cmp(b) <= 0 ? a : b);
    const upper = values.reduce((a, b) => a.cmp(b) >= 0 ? a : b);
    return { policy, model_values: values.map(String), lower: String(lower), upper: String(upper) };
  });
}

function bestRows(table, field) {
  let best = Q.from(table[0][field]);
  for (const r of table.slice(1)) if (Q.from(r[field]).cmp(best) > 0) best = Q.from(r[field]);
  return { value: String(best), policies: table.filter(r => Q.from(r[field]).cmp(best) === 0).map(r => r.policy) };
}

function rectangularValue(profile, policy) {
  let v = profile.terminal.map(Q.from); const d = Q.from(profile.discount);
  for (let h = 1; h <= profile.horizon; h++) {
    v = profile.states.map((_, s) => {
      const a = policy[s];
      const candidates = profile.global_models.map(model => qdot(model[s][a], v));
      const worst = candidates.reduce((x, y) => x.cmp(y) <= 0 ? x : y);
      return Q.from(profile.rewards[s][a]).add(d.mul(worst));
    });
  }
  return qdot(profile.initial, v).toString();
}

function permuted(profile) {
  const perm = [...profile.states.keys()].reverse();
  const globalModels = profile.global_models.map(model => perm.map(oldS => [0, 1].map(a => perm.map(oldT => model[oldS][a][oldT]))));
  return {
    ...profile,
    states: perm.map((_, i) => `r${i}`),
    rewards: perm.map(old => profile.rewards[old]), terminal: perm.map(old => profile.terminal[old]),
    initial: perm.map(old => profile.initial[old]), fixed_policy: perm.map(old => profile.fixed_policy[old]),
    global_models: globalModels
  };
}

function resultFor(op, p) {
  const table = policyTable(p); const robust = bestRows(table, 'lower'); const optimistic = bestRows(table, 'upper');
  const robustPolicy = robust.policies[0]; const fixedValues = p.global_models.map((_, m) => evalPolicy(p, p.fixed_policy, m));
  const rect = Q.from(rectangularValue(p, robustPolicy)); const gap = Q.from(robust.value).sub(rect);
  const base = { scope: 'finite_synthetic_globally_coupled_uncertainty', external_credit: false };
  switch (op) {
    case 'validate_record': return { ...base, states: p.states.length, actions: 2, global_models: p.global_models.length, horizon: p.horizon, model_fixed_across_trajectory: true };
    case 'policy_enumeration': return { ...base, count: table.length, policies: table.map(x => x.policy) };
    case 'fixed_model_value': return { ...base, policy: p.fixed_policy, per_model: fixedValues.map((x, m) => ({ model: m, vector: x.vector, scalar: x.scalar })) };
    case 'lower_envelope': { const vals = fixedValues.map(x => Q.from(x.scalar)); return { ...base, value: String(vals.reduce((a, b) => a.cmp(b) <= 0 ? a : b)) }; }
    case 'upper_envelope': { const vals = fixedValues.map(x => Q.from(x.scalar)); return { ...base, value: String(vals.reduce((a, b) => a.cmp(b) >= 0 ? a : b)) }; }
    case 'robust_global_policy': return { ...base, ...robust, all_policy_bounds: table.map(x => ({ policy: x.policy, lower: x.lower })) };
    case 'optimistic_global_policy': return { ...base, ...optimistic, all_policy_bounds: table.map(x => ({ policy: x.policy, upper: x.upper })) };
    case 'global_policy_regret': {
      const perModelBest = p.global_models.map((_, m) => table.map(r => Q.from(r.model_values[m])).reduce((a, b) => a.cmp(b) >= 0 ? a : b));
      const chosen = table.find(r => JSON.stringify(r.policy) === JSON.stringify(robustPolicy));
      const regrets = perModelBest.map((v, m) => v.sub(Q.from(chosen.model_values[m])));
      return { ...base, policy: robustPolicy, per_model: regrets.map(String), maximum: String(regrets.reduce((a, b) => a.cmp(b) >= 0 ? a : b)) };
    }
    case 'horizon_layer_trace': return { ...base, policy: p.fixed_policy, traces: fixedValues.map((x, m) => ({ model: m, layers: x.layers })) };
    case 'coupling_signature': return { ...base, differing_rows: p.states.flatMap((_, s) => [0, 1].filter(a => JSON.stringify(p.global_models[0][s][a]) !== JSON.stringify(p.global_models[1][s][a])).map(a => [s, a])) };
    case 'rectangular_relaxation': return { ...base, policy: robustPolicy, value: String(rect), relation: 'rowwise model choice at each state and time' };
    case 'rectangularity_gap': return { ...base, global_value: robust.value, rectangular_value: String(rect), gap: String(gap), nonnegative: gap.cmp(new Q(0n)) >= 0 };
    case 'model_deletion_sensitivity': return { ...base, full_value: robust.value, retained_single_model_values: table.map(r => r.model_values).reduce((acc, vals) => acc, []).slice(0, 0).concat(p.global_models.map((_, m) => bestRows(table.map(r => ({ ...r, single: r.model_values[m] })), 'single').value)) };
    case 'relabel_covariance': { const other = bestRows(policyTable(permuted(p)), 'lower'); return { ...base, original: robust.value, relabelled: other.value, equal: Q.from(robust.value).cmp(other.value) === 0 }; }
    case 'discount_zero_certificate': { const z = { ...p, discount: '0' }; const zBest = bestRows(policyTable(z), 'lower'); return { ...base, value: zBest.value, policies: zBest.policies, transition_independent_after_first_reward: true }; }
    case 'accessible_summary': return { ...base, title: p.label, states: p.states.length, global_models: p.global_models.length, robust_value: robust.value, rectangular_value: String(rect), gap: String(gap), note: 'A single global model persists; the rectangular comparator may combine rows that no one global model contains.' };
    case 'scene_coordinates': return { ...base, axes: ['remaining decisions', 'state count', 'rectangularity gap'], coordinates: [p.horizon, p.states.length, String(gap)] };
    case 'mixture_representation': return { ...base, outcome: 'represented', weights: ['1/2', '1/2'], fixed_policy_mixture_value: String(Q.from(fixedValues[0].scalar).add(fixedValues[1].scalar).mul('1/2')), reservation: 'A mixture representation is not evidence that the data-generating model is a mixture.' };
    case 'calibration_evidence_gap': return { ...base, outcome: 'open_gap', missing: ['governed observations', 'sampling design', 'likelihood', 'coverage assessment', 'independent review'] };
    case 'authority_gate': return { ...base, outcome: 'exact_gate', held: ['real intervention', 'participant decision', 'production deployment', 'legal or cultural authority', 'Maori authority'] };
    default: throw new Error(`unknown operation ${op}`);
  }
}

const operations = [
  ['validate_record', 'x1', 'completed'], ['policy_enumeration', 'x1', 'completed'],
  ['fixed_model_value', 'x1', 'completed'], ['lower_envelope', 'x1', 'completed'],
  ['upper_envelope', 'x1', 'completed'], ['robust_global_policy', 'x1', 'completed'],
  ['optimistic_global_policy', 'x1', 'completed'], ['global_policy_regret', 'x1', 'completed'],
  ['horizon_layer_trace', 'x1', 'completed'], ['coupling_signature', 'x1', 'completed'],
  ['rectangular_relaxation', 'x2', 'completed'], ['rectangularity_gap', 'x2', 'completed'],
  ['model_deletion_sensitivity', 'x2', 'completed'], ['relabel_covariance', 'x2', 'completed'],
  ['discount_zero_certificate', 'x2', 'completed'], ['accessible_summary', 'x2', 'completed'],
  ['scene_coordinates', 'x2', 'completed'], ['mixture_representation', 'x2', 'represented'],
  ['calibration_evidence_gap', 'x2', 'open_gap'], ['authority_gate', 'x2', 'exact_gate']
];
const profiles = Array.from({ length: 15 }, (_, i) => makeProfile(i));

function contract(op, session, disposition, p, index) {
  const expected = resultFor(op, p);
  const request = { op, input: p };
  return {
    proposal_id: `IF7044-P${String(index + 1).padStart(3, '0')}`,
    operation: op, profile_id: p.profile_id, session,
    definition: `Evaluate ${op.replaceAll('_', ' ')} under a finite globally coupled transition-model contract.`,
    request, expected, request_sha256: shaObject(request), expected_sha256: shaObject(expected),
    expected_execution_disposition: disposition,
    novelty_scope: 'New owner contracts for finite globally coupled uncertainty; no novel-mathematics, empirical, production or authority claim.',
    falsifier: 'Any exact-rational mismatch, model-persistence violation, silent tie loss, order reversal, malformed-input acceptance or evidence promotion.',
    external_credit: false, boundary
  };
}

function sourceContracts() {
  const dir = path.join(sourceBase, 'planning', 'proposals');
  const files = fs.readdirSync(dir).filter(x => x.endsWith('.json')).sort();
  const out = [];
  for (const file of files) {
    const rel = path.posix.join('docs/talen-briar/v704-v3-r2/planning/proposals', file);
    const parsed = JSON.parse(fs.readFileSync(path.join(dir, file), 'utf8'));
    for (const c of parsed.contracts) out.push({
      source_path: rel, proposal_id: c.proposal_id, operation: c.operation,
      profile_id: c.profile_id, request_sha256: c.request_sha256,
      expected_sha256: c.expected_sha256, inherited_novelty_credit: 0,
      inherited_completion_credit: 0, source_final: sourceFinal
    });
  }
  if (out.length !== 300 || new Set(out.map(x => x.proposal_id)).size !== 300) throw new Error(`expected 300 unique inherited proposals, got ${out.length}`);
  return out;
}

function taskPlan(session) {
  return {
    schema: 'ghc.family.phase-task-plan.v18', phase: 'v704-v4', owner: 'Ilyra Fen', session,
    safe: Array.from({ length: 400 }, (_, i) => ({
      task_id: `IF7044-${session}-S${String(i + 1).padStart(3, '0')}`,
      class: i < 150 ? 'core_contract' : 'auxiliary_boundary_fixture',
      expected: 'exact bounded result or explicit nonpromotion representation',
      execution_state: 'planned'
    })),
    candidates: Array.from({ length: 300 }, (_, i) => ({
      task_id: `IF7044-${session}-C${String(i + 1).padStart(3, '0')}`,
      mutation_class: ['missing_model', 'mass_mismatch', 'unknown_state', 'bad_policy', 'negative_horizon', 'invalid_discount', 'shape_mismatch', 'empty_actions', 'mixed_denominator_zero', 'authority_promotion'][i % 10],
      expected: 'reject and retain failed subject at zero completion credit', execution_state: 'planned'
    })),
    cfr: Array.from({ length: 300 }, (_, i) => ({
      task_id: `IF7044-${session}-F${String(i + 1).padStart(3, '0')}`,
      focus: ['exact arithmetic', 'tie retention', 'source binding', 'scope boundary', 'rollback', 'error clarity'][i % 6],
      expected: 'review or recovery witness without deletion', execution_state: 'planned'
    })),
    counts: { safe: 400, candidate: 300, cfr: 300 }, boundary
  };
}

const skillNames = [
  'coupled-model-record-structure', 'exact-transition-validation', 'finite-policy-enumeration',
  'global-model-policy-evaluation', 'robust-global-policy-selection', 'optimistic-global-policy-selection',
  'global-model-regret', 'finite-horizon-layer-trace', 'coupled-model-counterexample',
  'source-bound-uncertainty-evidence', 'rectangular-relaxation-comparison',
  'rectangularity-gap-certificate', 'model-deletion-sensitivity', 'state-relabel-covariance',
  'discount-zero-certificate', 'mixture-representation-boundary', 'calibration-evidence-gap',
  'uncertainty-authority-gate', 'accessible-coupled-model-summary', 'uncertainty-scene-coordinates'
].map(x => `ghc-family-${x}`);
const runnerNames = [
  'coupled_record', 'policy_enumeration', 'global_value', 'robust_selection', 'regret_trace',
  'rectangular_comparison', 'deletion_covariance', 'discount_mixture', 'accessible_scene', 'evidence_boundary'
].map(x => `ghc_family_${x}_runner.py`);
const hookIds = [
  'model_setting_change', 'source_lane_mutation', 'successful_replay', 'rectangularity_promotion',
  'malformed_subject_promotion', 'broad_git_stage', 'destructive_git', 'raw_identifier_output',
  'prepared_delivery', 'accepted_resend'
];

const laws = [
  ['global-model persistence', 'One selected model index remains fixed over the complete evaluated trajectory.'],
  ['probability conservation', 'Every transition row and initial distribution sums exactly to one.'],
  ['envelope order', 'The exact lower envelope never exceeds the corresponding upper envelope.'],
  ['rectangular containment', 'For one fixed policy, the rowwise rectangular lower value does not exceed the global-model lower value.'],
  ['gap nonnegativity', 'The defined global-minus-rectangular fixed-policy gap is nonnegative.'],
  ['terminal base', 'Horizon zero returns the declared terminal vector.'],
  ['discount-zero immediacy', 'At positive horizon and zero discount, transitions do not affect the current reward value.'],
  ['policy census', 'Two actions across n states produce exactly 2^n deterministic stationary policies.'],
  ['relabel covariance', 'A bijective state relabel preserves scalar envelopes and optimal-policy value sets.'],
  ['model deletion monotonicity', 'Removing an admissible global model cannot reduce a lower envelope.'],
  ['tie nonerasure', 'Every exact optimal policy tie is retained before selecting a display representative.'],
  ['initial-mass conservation', 'The initial distribution remains normalized under all read-only transformations.'],
  ['rational closure', 'All finite computations remain in reduced exact rational form.'],
  ['invalid-subject nonpromotion', 'A successful refusal never promotes its malformed subject.'],
  ['authority nonpromotion', 'Synthetic computation never supplies empirical, participant, legal, cultural or production authority.']
].map(([title, statement], i) => ({ law_id: `IF7044-L${String(i + 1).padStart(2, '0')}`, title, statement, scope: 'project hypothesis checked only across fifteen frozen synthetic profiles', fundamental_law_claimed: false }));

const problems = [
  'distribution-shift guarantees', 'nonrectangular robust dynamic programming complexity',
  'uncertainty-set calibration', 'time-consistent policy design', 'randomized-policy sufficiency',
  'partial observability', 'infinite-horizon convergence', 'continuous action spaces',
  'finite-sample coverage', 'model misspecification detection', 'causal transportability',
  'adversarial dependence learning', 'appeal outcome evaluation', 'complete accessibility evidence',
  'independent external reproduction'
].map((title, i) => ({ probe_id: `IF7044-Q${String(i + 1).padStart(2, '0')}`, title, state: 'open_gap', attempt: 'Define a finite exact proxy and its falsifier without claiming the original problem solved.', missing_bridge: 'Requires governed external data, broader mathematics, affected-party oversight or independent review beyond this owner phase.' }));

const practices = {
  own: ['robust-control analyst', 'exact algebraist', 'software verifier', 'research librarian', 'accessibility designer', 'provenance engineer', 'governance analyst', 'visualization designer'],
  successor_recommendations: ['interval analyst', 'experimental-design reviewer', 'scientific model-comparison analyst', 'appeal-process auditor'],
  qualification_claimed: false
};

const failures = [
  ['marker-token predicate mismatch', 'A guessed end-marker spelling and punctuation did not match the baton.', 'Read the exact final nonempty line and compare it literally.'],
  ['retained-negative key mismatch', 'The first bounded summary looked for generic item keys and reported length zero.', 'Use the declared negative_ids array and verify count, uniqueness and attributions.'],
  ['broad lane null branch', 'A broad inventory assumed every .git entry returned a non-null branch string.', 'Use explicit exit-state handling and narrow the inventory.'],
  ['broad lane probe overrun', 'Two old checkout status probes remained running beyond the output window.', 'Verify exact process command lines, stop only those probe trees and use bounded selected-lane checks.'],
  ['probe process selector mismatch', 'The first parent-process verification wildcard did not uniquely match both probe commands.', 'Use exact PIDs plus bounded regex checks before stopping the two owned probe trees.'],
  ['PowerShell grouped-exit parser edge', 'A branch probe grouped a native command and LASTEXITCODE in an invalid expression.', 'Run each native command separately and capture LASTEXITCODE immediately.'],
  ['workflow display truncation', 'A raw 174-row workflow display was truncated by the presentation budget.', 'Parse the complete JSON, verify every sequence ordinal and use the complete roster table for readable review.'],
  ['method-flow backlink rejection', 'The first official Method Flow validation found missing failed-witness backlinks and stale derived counts.', 'Bind both failed and recovery witnesses to each method and use the validator-defined derived count shape.']
];

function planningMethodFlow() {
  const methods = [], witnesses = [], stateEvents = [], recommendations = [];
  failures.forEach(([title, failure, recovery], i) => {
    const n = String(i + 1).padStart(3, '0'); const mid = `IF7044-PL-M${n}`; const neg = `IF7044-PL-N${n}`;
    methods.push({ method_id: mid, title, failure_signature: failure, trigger_preconditions: ['bounded planning or source-read operation'], privacy_class: 'sanitized_public', approval_class: 'safe_now', candidate_workaround: recovery, validation_witness_ids: [`IF7044-PL-W${n}-F`, `IF7044-PL-W${n}-R`], recurrence_guard: recovery, rollback: 'Retain the failed attempt, make no source mutation and return to the previous clean state.', recommendation_state: 'validated', supersedes: [], protected_gates: ['source_read_only', 'no_success_replay'], retained_negative_ids: [neg], scope_boundary: boundary });
    witnesses.push({ witness_id: `IF7044-PL-W${n}-F`, method_id: mid, procedure: failure, scope: 'planning operation', expected: 'failure retained at zero credit', observed: 'failure retained', result: 'fail', same_owner_only: true, independent_reproduction: false, retained_negative_ids: [neg], boundary });
    witnesses.push({ witness_id: `IF7044-PL-W${n}-R`, method_id: mid, procedure: recovery, scope: 'bounded recovery', expected: 'smallest recovery passes without source mutation', observed: 'bounded recovery passed', result: 'pass', same_owner_only: true, independent_reproduction: false, retained_negative_ids: [neg], boundary });
    stateEvents.push({ event_id: `IF7044-PL-E${n}`, method_id: mid, from: 'observed', to: 'validated', witness_id: `IF7044-PL-W${n}-R` });
    recommendations.push({ recommendation_id: `IF7044-PL-R${n}`, method_id: mid, state: 'validated', text: recovery });
  });
  return { schema: 'ghc.family.method-flow-state.v1', phase: 'v704-v4-planning', owner: 'Ilyra Fen', identity_boundary: 'Relational working identity only; no consciousness, personhood, continuity or authority evidence.', execution_authority: 'owner_self_scoped_delta', source_commit: sourceFinal, final_commit: null, changed_file_allowlist: ['docs/ilyra-fen/v704-v4/planning', 'scripts/build_ilyra_v704_v4_plan.mjs', '.codex/coordination/project.yaml'], module_allowlist: ['scripts/build_ilyra_v704_v4_plan.mjs'], repository_scan: false, module_scan: true, cross_lane_scan: false, unchanged_history_scan: false, sibling_lane_mutation: false, exact_pushed_head_required: true, methods, witnesses, state_events: stateEvents, recommendations, counts: { methods: failures.length, witnesses: failures.length * 2, state_events: failures.length, recommendations: failures.length, states: { observed: 0, candidate: 0, validated: failures.length, preferred: 0, superseded: 0, deprecated: 0 }, witness_results: { pass: failures.length, fail: failures.length } }, evidence_counts: { negatives: failures.length, methods: failures.length, failed_witnesses: failures.length, passing_witnesses: failures.length, witnesses: failures.length * 2, open_gaps: 0, exact_gates: 0 }, selected_source_baseline: { negatives: 63763, methods: 5709, failed_witnesses: 54928, passing_witnesses: 173779, witnesses: 228707, open_gaps: 1978, exact_gates: 2063 }, source_fold_count: 1, effective_totals: { negatives: 63763 + failures.length, methods: 5709 + failures.length, failed_witnesses: 54928 + failures.length, passing_witnesses: 173779 + failures.length, witnesses: 228707 + failures.length * 2, open_gaps: 1978, exact_gates: 2063 }, boundary };
}

function manifest() {
  const entries = [];
  const walk = dir => { for (const ent of fs.readdirSync(dir, { withFileTypes: true })) { const p = path.join(dir, ent.name); if (ent.isDirectory()) walk(p); else if (ent.name !== 'manifest.json') { const b = fs.readFileSync(p); entries.push({ path: path.relative(root, p).replaceAll('\\', '/'), bytes: b.length, sha256: shaBytes(b) }); } } };
  walk(planRoot); entries.sort((a, b) => a.path.localeCompare(b.path));
  return { schema: 'ghc.family.git-blob-precommit-manifest.v1', phase: 'v704-v4-planning', source_commit: sourceFinal, entry_count: entries.length, entries, note: 'Working-byte planning manifest; exact Git-blob manifest is sealed after commit.', boundary };
}

mkdir(planRoot);
const inherited = sourceContracts();
const newContracts = [];
operations.forEach(([op, session, disposition], oi) => profiles.forEach((p, pi) => newContracts.push(contract(op, session, disposition, p, oi * 15 + pi))));
if (newContracts.length !== 300) throw new Error('new proposal count mismatch');
const outcomeCounts = newContracts.reduce((a, c) => (a[c.expected_execution_disposition]++, a), { completed: 0, represented: 0, open_gap: 0, exact_gate: 0 });
if (JSON.stringify(outcomeCounts) !== JSON.stringify({ completed: 255, represented: 15, open_gap: 15, exact_gate: 15 })) throw new Error('outcome count mismatch');
if (!newContracts.filter(c => c.operation === 'rectangularity_gap').every(c => c.expected.nonnegative === true)) throw new Error('rectangularity containment failed in planning oracle');

writeJson(path.join(planRoot, 'authorization-v18.json'), JSON.parse(fs.readFileSync(path.join(sourceBase, 'planning', 'authorization-v18.json'), 'utf8')));
writeJson(path.join(planRoot, 'workflow-v18.json'), JSON.parse(fs.readFileSync(path.join(sourceBase, 'planning', 'workflow-v18.json'), 'utf8')));
writeText(path.join(planRoot, 'complete-roster.md'), fs.readFileSync(path.join(sourceBase, 'planning', 'complete-roster.md'), 'utf8'));
writeJson(path.join(planRoot, 'source-binding.json'), { schema: 'ghc.family.source-binding.v1', owner: 'Ilyra Fen', phase: 'v704-v4', source_owner: 'Talen Briar', source_phase: 'v704-v3-r2', source_final: sourceFinal, source_branch: 'codex/GHC-Family/talen-briar-main-1', baton_sha256: 'e1d3b36f0980962297db36eb38e9837a0ccf7e29e8b66e6a2597f27c8704c021', activation_sha256: 'b6e2f288c043b53694589ccb7bc96b72c2080a55fe2d4406b6e4655edfc31a0b', canonical_receipt_sha256: 'b6f9c3ef016743eface90058721212585959ef853693d0d068b78f9fe762d4ff', canonical_state: { checks: '47/47', invocations: 1, successes: 1, replays: 0 }, source_read_only: true, source_validation_not_ilyra_credit: true, boundary });
writeJson(path.join(planRoot, 'profiles.json'), { count: profiles.length, profiles, frozen_before_x1: true, boundary });
operations.forEach(([op], oi) => writeJson(path.join(planRoot, 'proposals', `${String(oi + 1).padStart(2, '0')}-${op}.json`), { operation: op, count: 15, contracts: newContracts.slice(oi * 15, oi * 15 + 15), frozen_before_x1: true, boundary }));
for (let i = 0; i < 20; i++) writeJson(path.join(planRoot, 'inherited', `part-${String(i + 1).padStart(2, '0')}.json`), { count: 15, contracts: inherited.slice(i * 15, i * 15 + 15), novelty_credit: 0, completion_credit: 0, boundary });
writeJson(path.join(planRoot, 'proposal-index.json'), { inherited: 300, new: 300, outcomes: outcomeCounts, per_session: { x1: { core: 150, safe: 400, candidate: 300, cfr: 300 }, x2: { core: 150, safe: 400, candidate: 300, cfr: 300 } }, frozen_before_x1: true, auxiliary_novelty_credit: 0, boundary });
writeJson(path.join(planRoot, 'tasks-x1.json'), taskPlan('x1'));
writeJson(path.join(planRoot, 'tasks-x2.json'), taskPlan('x2'));
writeJson(path.join(planRoot, 'approval-packets.json'), { exact: Array.from({ length: 50 }, (_, i) => ({ packet_id: `IF7044-E${String(i + 1).padStart(3, '0')}`, state: 'held', execution_authority: 'requires fresh exact approval at action time' })), blocked: Array.from({ length: 30 }, (_, i) => ({ packet_id: `IF7044-B${String(i + 1).padStart(3, '0')}`, state: 'blocked', reason: ['real participant or operator', 'production or deployment', 'legal or cultural authority', 'Maori authority', 'independent empirical confirmation'][i % 5] })), boundary });
writeJson(path.join(planRoot, 'law-hypotheses.json'), { count: laws.length, laws, fundamental_law_claimed: false, boundary });
writeJson(path.join(planRoot, 'open-problem-probes.json'), { count: problems.length, probes: problems, solved_count: 0, boundary });
writeJson(path.join(planRoot, 'practices.json'), { ...practices, boundary });
writeJson(path.join(planRoot, 'capability-plan.json'), { local_skills: skillNames.map((name, i) => ({ name, session: i < 10 ? 'x1' : 'x2', state: 'planned' })), local_runners: runnerNames.map((name, i) => ({ name, session: i < 5 ? 'x1' : 'x2', state: 'planned' })), successor_skill_ideas: ['distribution-shift-envelope', 'nonstationary-policy-comparator', 'uncertainty-calibration-dossier', 'appeal-outcome-certificate', 'external-reproduction-manifest'], successor_runner_ideas: ['fixed-global-model-comparator', 'interval-bellman-enclosure', 'calibration-dataset-reader', 'human-appeal-record-checker', 'external-reproduction-verifier'], global_installs: 'additive only after local validation and exact collision checks', boundary });
writeJson(path.join(planRoot, 'hook-plan.json'), { plugin: 'ghc-family-ilyra-coupled-workflow-hooks', hooks: hookIds.map((hook_id, i) => ({ hook_id, event: i < 6 ? 'PreToolUse' : i < 9 ? 'PostToolUse' : 'Stop', synchronous: true, nonblocking: true, payload_command_execution: false, state: 'planned' })), live_observation_required: true, installation_is_not_live_observation: true, boundary });
writeJson(path.join(planRoot, 'method-flow.json'), planningMethodFlow());
writeText(path.join(planRoot, 'overview.md'), `# Ilyra Fen v704-v4 planning freeze\n\nThis phase tests a precise boundary left open by Talen's rectangular robust-control model. Talen permits a separate worst transition vertex for each state, action and time. Ilyra's new finite contracts instead choose one global model index and hold it fixed across the whole finite trajectory. The two assumptions answer different questions and neither may silently substitute for the other.\n\nThe planning freeze contains 300 source references at zero novelty and completion credit plus 300 new contracts across twenty operations and fifteen deterministic synthetic profiles. Seventeen operation families are bounded computations, one is a representation only, one remains an empirical calibration gap and one remains an authority gate. Exact rational arithmetic, full policy enumeration, tie retention, model-deletion sensitivity, relabel covariance and a fixed-policy rectangular relaxation make the difference inspectable.\n\nEach session freezes 400 safe tasks, 300 malformed candidates and 300 CLEAN/FIX/REFINE reviews. Candidate rejection is recorded separately from refusal success. Fifty exact packets and thirty blocked packets remain held. Planning also declares twenty local skill guides, ten paired runners, ten synchronous advisory hooks, fifteen project-law hypotheses, fifteen open-problem probes, eight learning practices and four successor recommendations. Floors and ceilings are planning bounds rather than authority to manufacture unsafe work.\n\nPlanning is the only lifecycle active at this commit. No x1 engine execution, x2 browser observation, global installation, canonical validation or successor contact is represented here. The selected Talen baseline is folded exactly once. All source and sibling lanes remain read-only.\n\n${boundary}\n`);
writeJson(path.join(planRoot, 'manifest.json'), manifest());
console.log(JSON.stringify({ ok: true, phase: 'v704-v4', profiles: profiles.length, inherited: inherited.length, new: newContracts.length, outcomes: outcomeCounts, planning_files: manifest().entry_count + 1, planning_method_flow: planningMethodFlow().counts }));
