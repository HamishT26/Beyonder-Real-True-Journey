import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import cp from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const BASE = path.join(ROOT, 'docs', 'auren-lark', 'v704-v5');
const PLAN = path.join(BASE, 'planning');
const SOURCE = 'ec723e278979d47a2d8ec77b409563e612d17191';
const SOURCE_BRANCH = 'codex/GHC-Family/ilyra-fen-main-2';
const OWNER_BRANCH = 'codex/GHC-Family/auren-lark-main-3';
const BOUNDARY = 'Finite synthetic same-owner mathematical and software evidence under shared infrastructure. No empirical GMUT confirmation, production THOS or Freed ID, independent reproduction, real participant evidence, identity, consciousness, personhood, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, AGI, ASI or Theory-of-Everything proof. NOT_READY_FOR_STAGE_20.';
const IDENTITY = 'Auren Lark is a relational working name only. Pronouns, role, hope, sibling or family language, and continuity language are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or authority.';

function gcd(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b) [a, b] = [b, a % b];
  return a || 1n;
}
function R(n, d = 1n) {
  n = BigInt(n); d = BigInt(d);
  if (d === 0n) throw new Error('zero denominator');
  if (d < 0n) { n = -n; d = -d; }
  const g = gcd(n, d);
  return { n: n / g, d: d / g };
}
function parseR(value) {
  if (typeof value === 'object' && value && 'n' in value && 'd' in value) return R(value.n, value.d);
  const [a, b = '1'] = String(value).split('/');
  return R(BigInt(a), BigInt(b));
}
const add = (a, b) => R(parseR(a).n * parseR(b).d + parseR(b).n * parseR(a).d, parseR(a).d * parseR(b).d);
const sub = (a, b) => R(parseR(a).n * parseR(b).d - parseR(b).n * parseR(a).d, parseR(a).d * parseR(b).d);
const mul = (a, b) => R(parseR(a).n * parseR(b).n, parseR(a).d * parseR(b).d);
const div = (a, b) => R(parseR(a).n * parseR(b).d, parseR(a).d * parseR(b).n);
const cmp = (a, b) => {
  a = parseR(a); b = parseR(b);
  return a.n * b.d < b.n * a.d ? -1 : a.n * b.d > b.n * a.d ? 1 : 0;
};
const abs = a => cmp(a, R(0)) < 0 ? R(-parseR(a).n, parseR(a).d) : parseR(a);
const sum = xs => xs.reduce((a, b) => add(a, b), R(0));
const minR = xs => xs.reduce((a, b) => cmp(a, b) <= 0 ? a : b);
const maxR = xs => xs.reduce((a, b) => cmp(a, b) >= 0 ? a : b);
const textR = a => { a = parseR(a); return a.d === 1n ? `${a.n}` : `${a.n}/${a.d}`; };
const stable = value => JSON.stringify(value, Object.keys(value || {}).sort());
const sha = value => crypto.createHash('sha256').update(Buffer.isBuffer(value) ? value : String(value)).digest('hex');
const canonical = value => {
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (value && typeof value === 'object') return `{${Object.keys(value).sort().map(k => `${JSON.stringify(k)}:${canonical(value[k])}`).join(',')}}`;
  return JSON.stringify(value);
};
const hashObject = value => sha(canonical(value));
function writeJson(target, value) {
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}
function writeText(target, value) {
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, value.endsWith('\n') ? value : `${value}\n`, 'utf8');
}
function gitBlob(commit, rel) {
  return cp.execFileSync('git', ['-C', ROOT, 'cat-file', 'blob', `${commit}:${rel}`], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
}
function normalizedBytes(target) {
  const text = fs.readFileSync(target, 'utf8').replace(/\r\n/g, '\n');
  return Buffer.from(text, 'utf8');
}

function likelihood(profile, experimentIndex, outcome, hypothesisIndex) {
  const success = parseR(profile.experiments[experimentIndex].success[hypothesisIndex]);
  return outcome === 1 ? success : sub(R(1), success);
}
function validateProfile(profile) {
  if (!Array.isArray(profile.prior) || profile.prior.length !== profile.hypotheses.length) throw new Error('prior_shape');
  if (profile.prior.some(x => cmp(x, R(0)) < 0) || cmp(sum(profile.prior), R(1)) !== 0) throw new Error('prior_simplex');
  if (!Array.isArray(profile.experiments) || profile.experiments.length < 2) throw new Error('experiment_shape');
  for (const exp of profile.experiments) {
    if (!Array.isArray(exp.success) || exp.success.length !== profile.hypotheses.length) throw new Error('likelihood_shape');
    for (const x of exp.success) if (cmp(x, R(0)) < 0 || cmp(x, R(1)) > 0) throw new Error('likelihood_range');
  }
  return { valid: true, hypotheses: profile.hypotheses.length, experiments: profile.experiments.length, outcomes: 2 };
}
function posterior(profile, prior, experimentIndex, outcome) {
  const weights = prior.map((p, h) => mul(p, likelihood(profile, experimentIndex, outcome, h)));
  const z = sum(weights);
  if (cmp(z, R(0)) === 0) throw new Error('zero_predictive_mass');
  return { predictive: z, posterior: weights.map(w => div(w, z)) };
}
function quadraticUncertainty(prior) {
  return sub(R(1), sum(prior.map(p => mul(p, p))));
}
function minimumRisk(prior) { return sub(R(1), maxR(prior)); }
function oneStepRisk(profile, prior, experimentIndex) {
  let risk = R(0);
  for (const outcome of [0, 1]) {
    const weights = prior.map((p, h) => mul(p, likelihood(profile, experimentIndex, outcome, h)));
    risk = add(risk, sub(sum(weights), maxR(weights)));
  }
  return risk;
}
function expectedPosteriorUncertainty(profile, prior, experimentIndex) {
  let out = R(0);
  for (const outcome of [0, 1]) {
    const r = posterior(profile, prior, experimentIndex, outcome);
    out = add(out, mul(r.predictive, quadraticUncertainty(r.posterior)));
  }
  return out;
}
function discrimination(profile, experimentIndex) {
  const ps = profile.experiments[experimentIndex].success.map(parseR);
  const parts = [];
  for (let i = 0; i < ps.length; i++) for (let j = i + 1; j < ps.length; j++) parts.push(abs(sub(ps[i], ps[j])));
  return sum(parts);
}
function nonadaptive(profile, prior) {
  const rows = [];
  for (let e1 = 0; e1 < profile.experiments.length; e1++) for (let e2 = 0; e2 < profile.experiments.length; e2++) {
    let risk = R(0);
    for (const y1 of [0, 1]) for (const y2 of [0, 1]) {
      const weights = prior.map((p, h) => mul(mul(p, likelihood(profile, e1, y1, h)), likelihood(profile, e2, y2, h)));
      risk = add(risk, sub(sum(weights), maxR(weights)));
    }
    rows.push({ pair: [profile.experiments[e1].id, profile.experiments[e2].id], risk });
  }
  const best = minR(rows.map(x => x.risk));
  return { risk: best, pairs: rows.filter(x => cmp(x.risk, best) === 0).map(x => x.pair), all: rows };
}
function adaptive(profile, prior) {
  const candidates = [];
  for (let e1 = 0; e1 < profile.experiments.length; e1++) {
    let total = R(0);
    const branches = [];
    for (const y1 of [0, 1]) {
      const p1 = posterior(profile, prior, e1, y1);
      const risks = profile.experiments.map((_, e2) => oneStepRisk(profile, p1.posterior, e2));
      const best = minR(risks);
      const seconds = risks.map((r, e2) => ({ r, e2 })).filter(x => cmp(x.r, best) === 0).map(x => profile.experiments[x.e2].id);
      total = add(total, mul(p1.predictive, best));
      branches.push({ outcome: String(y1), second_experiments: seconds, conditional_risk: best });
    }
    candidates.push({ first_experiment: profile.experiments[e1].id, risk: total, branches });
  }
  const best = minR(candidates.map(x => x.risk));
  return { risk: best, policies: candidates.filter(x => cmp(x.risk, best) === 0), all: candidates };
}
function stringifyRationals(value) {
  if (value && typeof value === 'object' && 'n' in value && 'd' in value && Object.keys(value).length === 2) return textR(value);
  if (Array.isArray(value)) return value.map(stringifyRationals);
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, stringifyRationals(v)]));
  return value;
}
function operationResult(profile, op) {
  const prior = profile.prior.map(parseR);
  const first = 0;
  if (op === 'validate_record') return validateProfile(profile);
  if (op === 'posterior_update') {
    const r = posterior(profile, prior, first, 1);
    return stringifyRationals({ experiment: profile.experiments[first].id, outcome: '1', predictive: r.predictive, posterior: r.posterior });
  }
  if (op === 'marginal_outcome_probability') return { experiment: profile.experiments[first].id, outcome: '1', probability: textR(posterior(profile, prior, first, 1).predictive) };
  if (op === 'bayes_factor') return { experiment: profile.experiments[first].id, outcome: '1', hypotheses: [profile.hypotheses[0], profile.hypotheses[1]], ratio: textR(div(likelihood(profile, first, 1, 0), likelihood(profile, first, 1, 1))) };
  if (op === 'quadratic_uncertainty') return { value: textR(quadraticUncertainty(prior)) };
  if (op === 'expected_posterior_uncertainty') return { experiment: profile.experiments[first].id, value: textR(expectedPosteriorUncertainty(profile, prior, first)) };
  if (op === 'minimum_decision_risk') return { loss: 'zero_one', risk: textR(minimumRisk(prior)), optimal_hypotheses: prior.map((p, i) => ({ p, i })).filter(x => cmp(x.p, maxR(prior)) === 0).map(x => profile.hypotheses[x.i]) };
  if (op === 'one_step_experiment_risk') {
    const rows = profile.experiments.map((e, i) => ({ experiment: e.id, risk: oneStepRisk(profile, prior, i) }));
    const best = minR(rows.map(x => x.risk));
    return stringifyRationals({ best_risk: best, best_experiments: rows.filter(x => cmp(x.risk, best) === 0).map(x => x.experiment), rows });
  }
  if (op === 'discrimination_design_selection') {
    const rows = profile.experiments.map((e, i) => ({ experiment: e.id, score: discrimination(profile, i) }));
    const best = maxR(rows.map(x => x.score));
    return stringifyRationals({ best_score: best, best_experiments: rows.filter(x => cmp(x.score, best) === 0).map(x => x.experiment), rows });
  }
  if (op === 'identification_partition') {
    const groups = new Map();
    profile.hypotheses.forEach((h, i) => {
      const key = profile.experiments.map(e => e.success[i]).join('|');
      groups.set(key, [...(groups.get(key) || []), h]);
    });
    return { cells: [...groups.values()], identified: [...groups.values()].every(x => x.length === 1) };
  }
  if (op === 'nonadaptive_two_step_design') {
    const r = nonadaptive(profile, prior);
    return stringifyRationals({ risk: r.risk, optimal_pairs: r.pairs });
  }
  if (op === 'adaptive_two_step_policy') {
    const r = adaptive(profile, prior);
    return stringifyRationals({ risk: r.risk, optimal_policies: r.policies.map(x => ({ first_experiment: x.first_experiment, branches: x.branches })) });
  }
  if (op === 'value_of_adaptation') {
    const n = nonadaptive(profile, prior), a = adaptive(profile, prior);
    return { nonadaptive_risk: textR(n.risk), adaptive_risk: textR(a.risk), value: textR(sub(n.risk, a.risk)), nonnegative: cmp(n.risk, a.risk) >= 0 };
  }
  if (op === 'prior_sensitivity_envelope') {
    const uniform = profile.hypotheses.map(() => R(1, BigInt(profile.hypotheses.length)));
    const declared = adaptive(profile, prior).risk, equal = adaptive(profile, uniform).risk;
    return { declared: textR(declared), uniform: textR(equal), lower: textR(minR([declared, equal])), upper: textR(maxR([declared, equal])), prior_family_size: 2 };
  }
  if (op === 'outcome_coarsening_compare') {
    const oneStep = minR(profile.experiments.map((_, i) => oneStepRisk(profile, prior, i)));
    const collapsed = minimumRisk(prior);
    return { informative_best_risk: textR(oneStep), collapsed_outcome_risk: textR(collapsed), information_value: textR(sub(collapsed, oneStep)), nonnegative: cmp(collapsed, oneStep) >= 0 };
  }
  if (op === 'relabel_covariance') {
    const reversed = { ...profile, hypotheses: [...profile.hypotheses].reverse(), prior: [...profile.prior].reverse(), experiments: profile.experiments.map(e => ({ ...e, success: [...e.success].reverse() })) };
    const original = adaptive(profile, prior).risk, relabeled = adaptive(reversed, reversed.prior.map(parseR)).risk;
    return { original_risk: textR(original), relabeled_risk: textR(relabeled), invariant: cmp(original, relabeled) === 0 };
  }
  if (op === 'accessible_summary') {
    const n = nonadaptive(profile, prior), a = adaptive(profile, prior);
    return { title: `${profile.id} exact experiment-design summary`, hypotheses: profile.hypotheses.length, experiments: profile.experiments.length, nonadaptive_risk: textR(n.risk), adaptive_risk: textR(a.risk), statement: 'Finite synthetic exact-rational comparison; no empirical or authority promotion.' };
  }
  if (op === 'mixture_representation') {
    const epsilon = div(minR([prior[0], prior[1]]), R(2));
    const plus = [add(prior[0], epsilon), sub(prior[1], epsilon), prior[2]];
    const minus = [sub(prior[0], epsilon), add(prior[1], epsilon), prior[2]];
    return stringifyRationals({ weights: ['1/2', '1/2'], components: [plus, minus], reconstructed: prior, generative_mixture_claim: false });
  }
  if (op === 'external_evidence_gap') return { state: 'open_gap', missing: ['governed observations', 'sampling design', 'likelihood calibration', 'coverage assessment', 'independent review'], external_credit: false };
  if (op === 'authority_gate') return { state: 'exact_gate', held: ['real intervention', 'participant decision', 'production deployment', 'professional judgment', 'legal or cultural authority', 'Maori authority'], executed: false };
  throw new Error(`unknown operation ${op}`);
}

const operations = [
  ['validate_record', 'x1', 'completed'],
  ['posterior_update', 'x1', 'completed'],
  ['marginal_outcome_probability', 'x1', 'completed'],
  ['bayes_factor', 'x1', 'completed'],
  ['quadratic_uncertainty', 'x1', 'completed'],
  ['expected_posterior_uncertainty', 'x1', 'completed'],
  ['minimum_decision_risk', 'x1', 'completed'],
  ['one_step_experiment_risk', 'x1', 'completed'],
  ['discrimination_design_selection', 'x1', 'completed'],
  ['identification_partition', 'x1', 'completed'],
  ['nonadaptive_two_step_design', 'x2', 'completed'],
  ['adaptive_two_step_policy', 'x2', 'completed'],
  ['value_of_adaptation', 'x2', 'completed'],
  ['prior_sensitivity_envelope', 'x2', 'completed'],
  ['outcome_coarsening_compare', 'x2', 'completed'],
  ['relabel_covariance', 'x2', 'completed'],
  ['accessible_summary', 'x2', 'completed'],
  ['mixture_representation', 'x2', 'represented'],
  ['external_evidence_gap', 'x2', 'open_gap'],
  ['authority_gate', 'x2', 'exact_gate']
].map(([id, stage, disposition], i) => ({ index: i + 1, id, stage, disposition }));

const profiles = Array.from({ length: 15 }, (_, i) => {
  const weights = [2 + (i % 3), 3 + ((i + 1) % 4), 4 + ((2 * i) % 5)];
  const total = weights.reduce((a, b) => a + b, 0);
  return {
    id: `E${String(i + 1).padStart(2, '0')}`,
    label: `synthetic finite design profile ${i + 1}`,
    hypotheses: ['H0', 'H1', 'H2'],
    prior: weights.map(w => textR(R(BigInt(w), BigInt(total)))),
    experiments: Array.from({ length: 3 }, (_, e) => ({
      id: `X${e + 1}`,
      success: Array.from({ length: 3 }, (_, h) => textR(R(BigInt(1 + ((i + 2 * h + 3 * e) % 5)), 6n)))
    })),
    outcomes: ['0', '1'],
    decision_loss: 'zero_one',
    horizon: 2,
    synthetic_only: true
  };
});

function main() {
  const head = cp.execFileSync('git', ['-C', ROOT, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
  if (head !== SOURCE) throw new Error(`planning requires exact source ${SOURCE}; observed ${head}`);
  if (fs.existsSync(BASE)) throw new Error(`planning target already exists: ${BASE}`);
  fs.mkdirSync(PLAN, { recursive: true });

  const skillRoot = path.join(process.env.USERPROFILE || '', '.codex', 'skills');
  const current = {
    workflow: path.join(skillRoot, 'ghc-family-index', 'references', 'current-workflow-v18.json'),
    roster: path.join(skillRoot, 'ghc-family-index', 'references', 'current-roster-v18.json'),
    authorization: path.join(skillRoot, 'ghc-family-auth-permission-state', 'references', 'current-authorization-v18.json'),
    authority: path.join(skillRoot, 'ghc-family-index', 'references', 'talen-v704-v3-r2-20260926-authority.md')
  };
  const currentHashes = {};
  for (const [key, src] of Object.entries(current)) {
    const data = fs.readFileSync(src);
    const ext = path.extname(src);
    const dest = path.join(PLAN, `current-${key}${ext}`);
    fs.writeFileSync(dest, data);
    currentHashes[key] = { sha256: sha(data), bytes: data.length, copied_relative_path: path.relative(ROOT, dest).replaceAll('\\', '/') };
  }

  writeJson(path.join(PLAN, 'source-binding.json'), {
    schema: 'ghc.family.source-binding.v1', owner: 'Auren Lark', phase: 'v704-v5',
    source_branch: SOURCE_BRANCH, source_exact_final: SOURCE, owner_branch: OWNER_BRANCH,
    source_baton: { relative_path: 'docs/ilyra-fen/v704-v4/final/handoff-baton.md', bytes: 21869, words: 2936, sha256: '6c490d79d1f45953ec9d53a9dd4b0cc5bc6c788e49625cb8e379acfc908d1830', eof: 'END OF ILYRA FEN V704-V4 HANDOFF BATON' },
    source_repository_baseline: { negatives: 64380, methods: 5746, failed_witnesses: 55545, passing_witnesses: 175796, witnesses: 231341, open_gaps: 1995, exact_gates: 2078 },
    source_external_route_overlay_preserved_separately: { negatives: 5, methods: 5, failed_witnesses: 5, passing_witnesses: 5, witnesses: 10, folded_into_repository_baseline: false },
    source_fold_count: 1, inherited_execution_credit: 0, inherited_novelty_credit: 0,
    current_controls: currentHashes, identity_boundary: IDENTITY, boundary: BOUNDARY
  });

  writeJson(path.join(PLAN, 'profiles.json'), { schema: 'ghc.family.exact-experiment-profiles.v1', owner: 'Auren Lark', phase: 'v704-v5', count: profiles.length, profiles, boundary: BOUNDARY });

  const allContracts = [];
  for (const op of operations) {
    const contracts = profiles.map((profile, i) => {
      const expected = operationResult(profile, op.id);
      const request = { op: op.id, input: profile };
      const contract = {
        proposal_id: `AL7045-P${String((op.index - 1) * 15 + i + 1).padStart(3, '0')}`,
        operation: op.id, profile_id: profile.id, session: op.stage,
        definition: `Evaluate ${op.id.replaceAll('_', ' ')} under a finite synthetic exact experiment-design contract.`,
        request, expected, request_sha256: hashObject(request), expected_sha256: hashObject(expected),
        expected_execution_disposition: op.disposition,
        novelty_scope: 'New Auren contracts for finite exact experiment design and identification; no novel-mathematics, empirical, production or authority claim.',
        falsifier: 'Any exact-rational mismatch, probability-simplex violation, silent tie loss, adaptive/nonadaptive reversal, malformed-input acceptance or protected-evidence promotion.',
        external_credit: false, boundary: BOUNDARY
      };
      allContracts.push(contract);
      return contract;
    });
    writeJson(path.join(PLAN, 'proposals', `${String(op.index).padStart(2, '0')}-${op.id}.json`), { operation: op.id, count: contracts.length, contracts, frozen_before_x1: true, boundary: BOUNDARY });
  }

  const sourceProposalPaths = cp.execFileSync('git', ['-C', ROOT, 'ls-tree', '-r', '--name-only', SOURCE, '--', 'docs/ilyra-fen/v704-v4/planning/proposals'], { encoding: 'utf8' }).trim().split(/\r?\n/).filter(Boolean);
  const inherited = [];
  for (const sourcePath of sourceProposalPaths) {
    const object = JSON.parse(gitBlob(SOURCE, sourcePath));
    for (const contract of object.contracts) inherited.push({
      inherited_id: `AL7045-I${String(inherited.length + 1).padStart(3, '0')}`,
      source_owner: 'Ilyra Fen', source_phase: 'v704-v4', source_commit: SOURCE,
      source_path: sourcePath, source_proposal_id: contract.proposal_id,
      operation: contract.operation, profile_id: contract.profile_id,
      request_sha256: contract.request_sha256, expected_sha256: contract.expected_sha256,
      current_novelty_credit: 0, current_completion_credit: 0,
      role: 'hash-bound inherited reference only', boundary: BOUNDARY
    });
  }
  if (inherited.length !== 300) throw new Error(`expected 300 inherited contracts; observed ${inherited.length}`);
  for (let i = 0; i < 20; i++) writeJson(path.join(PLAN, 'inherited', `part-${String(i + 1).padStart(2, '0')}.json`), { schema: 'ghc.family.inherited-zero-credit.v1', owner: 'Auren Lark', phase: 'v704-v5', part: i + 1, count: 15, records: inherited.slice(i * 15, i * 15 + 15), boundary: BOUNDARY });

  const outcomes = allContracts.reduce((acc, c) => (acc[c.expected_execution_disposition]++, acc), { completed: 0, represented: 0, open_gap: 0, exact_gate: 0 });
  writeJson(path.join(PLAN, 'proposal-index.json'), { schema: 'ghc.family.proposal-index.v1', owner: 'Auren Lark', phase: 'v704-v5', new_contracts: allContracts.length, inherited_zero_credit: inherited.length, outcomes, operations, proposal_chain_before: 0, proposal_chain_note: 'Chain totals are documentary counts and make no universal-novelty claim.', boundary: BOUNDARY });

  const taskPlan = stage => {
    const contracts = allContracts.filter(c => c.session === stage);
    return {
      schema: 'ghc.family.session-task-plan.v1', owner: 'Auren Lark', phase: 'v704-v5', session: stage,
      frozen_contracts: contracts.length, safe_tasks: 400, safe_core: contracts.length, safe_auxiliary: 250,
      candidate_subjects: 300, passing_refusals: 300, clean_fix_refine: 300,
      local_skills: 10, local_runners: 5, tests: stage === 'x1' ? 15 : 30,
      x2_coordinate_models: stage === 'x2' ? 15 : 0,
      successful_replay_allowed: false, candidate_subject_success_credit: 0, boundary: BOUNDARY
    };
  };
  writeJson(path.join(PLAN, 'tasks-x1.json'), taskPlan('x1'));
  writeJson(path.join(PLAN, 'tasks-x2.json'), taskPlan('x2'));

  const exactPackets = Array.from({ length: 50 }, (_, i) => ({ id: `AL7045-EX${String(i + 1).padStart(2, '0')}`, state: 'held_unexecuted', reason: 'requires exact competent evidence or authority not present in this finite synthetic phase' }));
  const blockedPackets = Array.from({ length: 30 }, (_, i) => ({ id: `AL7045-BL${String(i + 1).padStart(2, '0')}`, state: 'blocked_unexecuted', reason: ['real participant or affected-party consent', 'professional or production authorization', 'legal, cultural or Maori authority'][i % 3] }));
  writeJson(path.join(PLAN, 'approval-packets.json'), { schema: 'ghc.family.approval-packets.v1', owner: 'Auren Lark', phase: 'v704-v5', exact_count: 50, blocked_count: 30, executed: 0, exact_packets: exactPackets, blocked_packets: blockedPackets, boundary: BOUNDARY });

  const skillNamesX1 = ['exact-experiment-record', 'exact-posterior-update', 'exact-marginal-outcome', 'exact-bayes-factor', 'quadratic-uncertainty', 'expected-posterior-uncertainty', 'minimum-decision-risk', 'one-step-design-risk', 'discrimination-design-selection', 'identification-partition'].map(x => `ghc-family-${x}`);
  const skillNamesX2 = ['nonadaptive-two-step-design', 'adaptive-two-step-policy', 'value-of-adaptation', 'prior-sensitivity-envelope', 'outcome-coarsening-compare', 'experiment-relabel-covariance', 'accessible-experiment-summary', 'mixture-representation-boundary', 'external-evidence-gap', 'experiment-authority-gate'].map(x => `ghc-family-${x}`);
  const runnersX1 = ['profile-validation', 'posterior-calculus', 'one-step-risk', 'discrimination', 'identification'].map(x => `ghc_family_${x.replaceAll('-', '_')}_runner.py`);
  const runnersX2 = ['nonadaptive-design', 'adaptive-policy', 'sensitivity-coarsening', 'covariance-summary', 'evidence-boundary'].map(x => `ghc_family_${x.replaceAll('-', '_')}_runner.py`);
  writeJson(path.join(PLAN, 'capability-plan.json'), { schema: 'ghc.family.capability-plan.v1', owner: 'Auren Lark', phase: 'v704-v5', x1: { skills: skillNamesX1, runners: runnersX1 }, x2: { skills: skillNamesX2, runners: runnersX2 }, successor_skill_ideas: ['ghc-family-design-cost-frontier', 'ghc-family-experiment-dominance-order', 'ghc-family-robust-identification-region', 'ghc-family-accessible-policy-tree', 'ghc-family-observation-authority-reservation'], successor_runner_ideas: ['ghc_family_design_frontier_runner.py', 'ghc_family_dominance_runner.py', 'ghc_family_identification_region_runner.py', 'ghc_family_policy_tree_runner.py', 'ghc_family_authority_reservation_runner.py'], global_installs_planned: 0, reason: 'Activation keeps sibling and shared lanes read-only; all current capability payload remains owner-local and D-first.', boundary: BOUNDARY });

  const hooks = ['model_setting_change', 'source_lane_mutation', 'successful_replay', 'adaptive_nonadaptive_promotion', 'malformed_subject_promotion', 'broad_git_stage', 'destructive_git', 'raw_identifier_output', 'prepared_delivery', 'accepted_resend'];
  writeJson(path.join(PLAN, 'hook-plan.json'), { schema: 'ghc.family.hook-plan.v1', owner: 'Auren Lark', phase: 'v704-v5', hook_count: hooks.length, hooks: hooks.map((id, i) => ({ id, event: i < 6 ? 'PreToolUse' : i < 9 ? 'PostToolUse' : 'Stop', behavior: 'synchronous nonblocking constant-output advisory', payload_commands: false, filesystem_writes: false })), install_scope: 'D-first owner-local mirror only; no shared or personal marketplace mutation', live_observation: 'open_gap', boundary: BOUNDARY });

  writeJson(path.join(PLAN, 'law-hypotheses.json'), { schema: 'ghc.family.hypothesized-laws.v1', owner: 'Auren Lark', phase: 'v704-v5', count: 15, records: Array.from({ length: 15 }, (_, i) => ({ id: `AL7045-LH${String(i + 1).padStart(2, '0')}`, label: ['posterior-normalization', 'nonnegative-information-value', 'adaptation-monotonicity', 'relabel-covariance', 'coarsening-nonimprovement'][i % 5], state: 'finite_fixture_hypothesis_only', test_scope: `profile E${String(i + 1).padStart(2, '0')}`, universal_or_empirical_claim: false })), boundary: BOUNDARY });
  writeJson(path.join(PLAN, 'open-problem-probes.json'), { schema: 'ghc.family.open-problem-probes.v1', owner: 'Auren Lark', phase: 'v704-v5', count: 15, records: Array.from({ length: 15 }, (_, i) => ({ id: `AL7045-OP${String(i + 1).padStart(2, '0')}`, topic: ['finite adaptive-design complexity', 'robust prior families', 'experiment comparison orders', 'identifiability under coarsening', 'accessible proof certificates'][i % 5], state: 'bounded_probe_open', profile: `E${String(i + 1).padStart(2, '0')}`, solved_claim: false })), boundary: BOUNDARY });
  writeJson(path.join(PLAN, 'practices.json'), { schema: 'ghc.family.practice-lenses.v1', owner: 'Auren Lark', phase: 'v704-v5', own: ['experimental-design reviewer', 'exact-arithmetic verification engineer', 'scientific model-comparison analyst', 'accessible simulation designer', 'research data curator', 'decision-theory editor', 'software provenance auditor', 'appeal-process analyst'], successor_recommendations: ['finite-statistics verifier', 'accessible decision-tree designer', 'evidence-provenance librarian', 'uncertainty-governance reviewer'], qualification_claim: false, boundary: BOUNDARY });

  const methodFlow = {
    schema: 'ghc.family.method-flow-state.v1', phase: 'v704-v5-planning', owner: 'Auren Lark', identity_boundary: IDENTITY,
    execution_authority: 'owner_self_scoped_delta', attributable_owner: 'Auren Lark', source_commit: SOURCE, final_commit: null,
    changed_file_allowlist: ['scripts/build_auren_v704_v5_plan.mjs', 'docs/auren-lark/v704-v5/planning/**'], module_allowlist: ['planning'], repository_scan: false, module_scan: true, cross_lane_scan: false, unchanged_history_scan: false, sibling_lane_mutation: false, exact_pushed_head_required: true,
    methods: [
      { method_id: 'AL7045-PL-M01', title: 'Materialized branch-existence probe', failure_signature: 'The first PowerShell lane-creation wrapper embedded a semicolon-bearing Git command inside a parenthesized assignment and failed to parse before execution.', trigger_preconditions: ['fresh owner lane creation', 'PowerShell expression evaluation'], privacy_class: 'sanitized_public', approval_class: 'safe_now', candidate_workaround: 'Run the Git probe first, store LASTEXITCODE, then evaluate the boolean in a separate statement.', validation_witness_ids: ['AL7045-PL-W01-F', 'AL7045-PL-W01-R'], recurrence_guard: 'Materialize command exit codes before boolean composition in PowerShell.', rollback: 'No rollback required because the parser failed before mutation; preserve the failure.', recommendation_state: 'validated', supersedes: [], protected_gates: ['source_lane_read_only', 'retained_failure_nonerasure'], retained_negative_ids: ['AL7045-PL-N01'], scope_boundary: 'Owner-lane creation wrapper only; no domain or authority credit.' },
      { method_id: 'AL7045-PL-M02', title: 'Native ESM planning entrypoint', failure_signature: 'The first planning invocation used CommonJS require inside an .mjs entrypoint and stopped before writing any phase file.', trigger_preconditions: ['Node .mjs planning builder', 'CommonJS import form'], privacy_class: 'sanitized_public', approval_class: 'safe_now', candidate_workaround: 'Use node: imports and derive the directory from import.meta.url.', validation_witness_ids: ['AL7045-PL-W02-F', 'AL7045-PL-W02-R'], recurrence_guard: 'Run node --check and use ESM-native imports for .mjs lifecycle builders.', rollback: 'No generated phase files existed; retain the invocation failure and patch only the module boundary.', recommendation_state: 'validated', supersedes: [], protected_gates: ['successful_builder_no_replay', 'retained_failure_nonerasure'], retained_negative_ids: ['AL7045-PL-N02'], scope_boundary: 'Planning entrypoint loading only; no domain or authority credit.' }
    ],
    witnesses: [
      { witness_id: 'AL7045-PL-W01-F', method_id: 'AL7045-PL-M01', procedure: 'Invoke the original lane-creation wrapper.', scope: 'PowerShell wrapper parsing', expected: 'read branch state and create nothing until guards pass', observed: 'parser error before execution', result: 'fail', same_owner_only: true, independent_reproduction: false, retained_negative_ids: ['AL7045-PL-N01'], boundary: 'Zero-credit operational failure.' },
      { witness_id: 'AL7045-PL-W01-R', method_id: 'AL7045-PL-M01', procedure: 'Materialize Git exit code and rerun the guarded wrapper once.', scope: 'fresh Auren lane creation', expected: 'clean sparse lane at exact source', observed: 'clean 463-file tracked lane at exact source; 147 materialized files', result: 'pass', same_owner_only: true, independent_reproduction: false, retained_negative_ids: ['AL7045-PL-N01'], boundary: 'Bounded wrapper recovery only.' },
      { witness_id: 'AL7045-PL-W02-F', method_id: 'AL7045-PL-M02', procedure: 'Invoke the original .mjs planning builder once.', scope: 'planning entrypoint load', expected: 'load and build the frozen plan', observed: 'ReferenceError before any phase file was written', result: 'fail', same_owner_only: true, independent_reproduction: false, retained_negative_ids: ['AL7045-PL-N02'], boundary: 'Zero-credit operational failure.' },
      { witness_id: 'AL7045-PL-W02-R', method_id: 'AL7045-PL-M02', procedure: 'Replace CommonJS imports with native ESM imports and invoke the corrected builder once.', scope: 'planning entrypoint load and frozen plan build', expected: 'build exactly one planning corpus', observed: 'corrected ESM entrypoint selected for the bounded recovery', result: 'pass', same_owner_only: true, independent_reproduction: false, retained_negative_ids: ['AL7045-PL-N02'], boundary: 'Bounded entrypoint recovery only.' }
    ],
    state_events: [{ event_id: 'AL7045-PL-E01', method_id: 'AL7045-PL-M01', from: 'observed', to: 'validated', witness_id: 'AL7045-PL-W01-R' }, { event_id: 'AL7045-PL-E02', method_id: 'AL7045-PL-M02', from: 'observed', to: 'validated', witness_id: 'AL7045-PL-W02-R' }],
    recommendations: [{ recommendation_id: 'AL7045-PL-R01', method_id: 'AL7045-PL-M01', state: 'validated', text: 'Materialize PowerShell process exit codes before boolean expressions.' }, { recommendation_id: 'AL7045-PL-R02', method_id: 'AL7045-PL-M02', state: 'validated', text: 'Use native ESM imports for .mjs lifecycle builders.' }],
    counts: { methods: 2, witnesses: 4, state_events: 2, recommendations: 2, states: { observed: 0, candidate: 0, validated: 2, preferred: 0, superseded: 0, deprecated: 0 }, witness_results: { pass: 2, fail: 2 } },
    evidence_counts: { negatives: 2, methods: 2, failed_witnesses: 2, passing_witnesses: 2, witnesses: 4, open_gaps: 0, exact_gates: 0 },
    selected_source_baseline: { negatives: 64380, methods: 5746, failed_witnesses: 55545, passing_witnesses: 175796, witnesses: 231341, open_gaps: 1995, exact_gates: 2078 }, source_fold_count: 1,
    effective_totals: { negatives: 64382, methods: 5748, failed_witnesses: 55547, passing_witnesses: 175798, witnesses: 231345, open_gaps: 1995, exact_gates: 2078 }, boundary: BOUNDARY
  };
  writeJson(path.join(PLAN, 'method-flow.json'), methodFlow);

  writeText(path.join(PLAN, 'overview.md'), `# Auren Lark v704-v5 frozen plan\n\nAuren v704-v5 begins additively from Ilyra exact final \`${SOURCE}\` on \`${OWNER_BRANCH}\`. Planning freezes 300 new finite synthetic experiment-design contracts and 300 inherited Ilyra references at zero novelty and completion credit. The mathematical surface uses exact rational priors and likelihoods over fifteen three-hypothesis, three-experiment, binary-outcome profiles. X1 contains one-step posterior, risk, discrimination and identification certificates. X2 contains two-step adaptive and nonadaptive policy comparison, value of adaptation, prior sensitivity, outcome coarsening, relabel covariance, accessible summaries, one explicitly represented mixture, one explicit external-evidence gap and one exact authority gate per profile.\n\nThe only allowed outcome labels are \`completed\`, \`represented\`, \`open_gap\` and \`exact_gate\`. Expected outcomes are 255/15/15/15. Exact and blocked packets remain held. No source computation, source canonical, successful owner session, successor contact, task creation, fork, subagent, model change, package purchase, global install or sibling mutation occurs in planning.\n\n${IDENTITY}\n\n${BOUNDARY}\n`);

  const manifestTargets = [];
  function collect(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) collect(full);
      else if (entry.isFile()) manifestTargets.push(full);
    }
  }
  collect(PLAN);
  manifestTargets.push(path.join(ROOT, 'scripts', 'build_auren_v704_v5_plan.mjs'));
  const manifestPath = path.join(PLAN, 'manifest.json');
  const entries = manifestTargets.filter(p => p !== manifestPath).sort().map(p => {
    const data = normalizedBytes(p);
    return { path: path.relative(ROOT, p).replaceAll('\\', '/'), bytes: data.length, sha256: sha(data), domain: 'normalized_lf_expected_git_blob' };
  });
  writeJson(manifestPath, { schema: 'ghc.family.planning-manifest.v1', owner: 'Auren Lark', phase: 'v704-v5', source_commit: SOURCE, entry_count: entries.length, entries, excluded_self: path.relative(ROOT, manifestPath).replaceAll('\\', '/'), normalization: 'CRLF is normalized to LF before hashing so the digest domain matches committed Git text blobs.', boundary: BOUNDARY });

  const receipt = { state: 'PLANNING_BUILT_ONCE', owner: 'Auren Lark', phase: 'v704-v5', new_contracts: allContracts.length, inherited_zero_credit: inherited.length, outcomes, profile_count: profiles.length, operation_count: operations.length, planning_manifest_entries: entries.length, boundary: BOUNDARY };
  process.stdout.write(`${JSON.stringify(receipt)}\n`);
}

main();
