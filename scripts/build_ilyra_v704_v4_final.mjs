import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';

const root = path.resolve(process.argv[2] || process.cwd());
const phaseRoot = path.join(root, 'docs', 'ilyra-fen', 'v704-v4');
const finalRoot = path.join(phaseRoot, 'final');
const source = 'f6c86fb56f5492d4d830b0439300001e54ba284f';
const planning = 'dd4f51ac27c47513cdc663fc94f73af1cb5973be';
const planningCorrection = '0b7a946c87088198ad6d2e99c976120defec3dcd';
const x1 = '0459221af11cf03a12feb2b70d65bfff4f97df7e';
const x2 = 'eb0b912def92a0696207d9c6137c991db0714791';
const branch = 'codex/GHC-Family/ilyra-fen-main-2';
const boundary = 'Finite synthetic same-owner mathematical, software, local-browser and installation evidence under shared infrastructure. No full-repository validation, independent reproduction, external audit, empirical confirmation, professional or operational authority, production readiness, complete privacy or accessibility assurance, exhaustive security, AGI or ASI result, consciousness or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 evidence. NOT_READY_FOR_STAGE_20.';
const baseline = { negatives: 63763, methods: 5709, failed_witnesses: 54928, passing_witnesses: 173779, witnesses: 228707, open_gaps: 1978, exact_gates: 2063 };
const ownerDelta = { negatives: 617, methods: 37, failed_witnesses: 617, passing_witnesses: 2017, witnesses: 2634, open_gaps: 17, exact_gates: 15 };
const totals = { negatives: 64380, methods: 5746, failed_witnesses: 55545, passing_witnesses: 175796, witnesses: 231341, open_gaps: 1995, exact_gates: 2078 };

const git = (...args) => execFileSync('git', ['-C', root, ...args], { maxBuffer: 128 * 1024 * 1024 });
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const mkdir = dir => fs.mkdirSync(dir, { recursive: true });
const writeJson = (file, value) => { mkdir(path.dirname(file)); fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n', 'utf8'); };
const writeText = (file, value) => { mkdir(path.dirname(file)); fs.writeFileSync(file, value.trimEnd() + '\n', 'utf8'); };

const receiptHashes = {
  planning_receipt: 'f7eda1ea12c6b6d2b96b9624443f45707ea79d2012d9fe43590cf1f50a581282',
  x1_receipt: '03dd5d3e95e43d17f259d40872f9aac81e95762a4c93337e3fe82703c00bedad',
  x2_receipt: '30f3f47ee8ccaf4b549b2086fc300d14a3d251a7ec41a348e348b097a2d40077',
  x1_method_flow: 'a97a3b9ba4cddde907e0e927df03e166bb88dd8ac1670841b8e69f4521c2d965',
  x2_method_flow: '207f654feff9a6f338aad8cbc00a2f57a02d858d434f028337366839eae9c96d',
};

const phaseTruth = {
  schema: 'ghc.family.phase-truth.v1', owner: 'Ilyra Fen', phase: 'v704-v4',
  repository_state: 'FINAL_PREPARED_FOR_EXACT_PUBLISH',
  branch,
  source,
  source_branch: 'codex/GHC-Family/talen-briar-main-1',
  source_is_git_ancestor: true,
  lifecycle: { planning, planning_correction: planningCorrection, x1, x2 },
  final_commit_binding: 'The exact commit containing this record is bound by the external one-shot canonical receipt and the sanitized activation message.',
  selected_source_baseline: baseline,
  source_fold_count: 1,
  owner_delta: ownerDelta,
  effective_totals: totals,
  new_contracts: 300,
  inherited_zero_credit: 300,
  core_outcomes: { completed: 255, represented: 15, open_gap: 15, exact_gate: 15 },
  safe_receipts: 800,
  safe_by_session: { x1: 400, x2: 400 },
  auxiliary_safe_new_proposal_credit: 0,
  failed_candidate_subjects: 600,
  separate_passing_refusals: 600,
  clean_fix_refine_receipts: 600,
  tests: { x1: 15, x2: 30, total: 45, failures: 0, successful_replays: 0 },
  owner_local_skills: 20,
  paired_public_runners: 10,
  global_skill_installs: 10,
  installed_advisory_plugins: 1,
  advisory_hooks: 10,
  manual_hook_smokes: 20,
  nonphysical_models: 15,
  viewer_profiles: 15,
  browser_observation: 'ONE_LOCAL_SAME_OWNER_CHECK',
  complete_accessibility_or_cross_browser_assurance: 'OPEN_GAP',
  live_hook_execution: 'OPEN_GAP',
  exact_packets: 50,
  blocked_packets: 30,
  exact_and_blocked_packets_executed: 0,
  current_route_authority: 'v18 formal thirty-seat schedule with Hamish pause, redirect, rename and stop controls',
  route_state: 'PREPARED_NOT_SENT',
  recipient_completion: 'UNOBSERVED',
  canonical_state: 'PREPARED_NOT_INVOKED',
  source_executions: 0,
  source_canonical_replays: 0,
  successful_session_replays: 0,
  new_tasks: 0,
  forks: 0,
  subagents: 0,
  sibling_mutations: 0,
  model_changes: 0,
  force_pushes: 0,
  merges: 0,
  memory_extension: 'not written because no direct memory-update request governed this phase',
  own_practices: [
    'robust-control analyst', 'exact-arithmetic verification engineer', 'research librarian',
    'configuration release engineer', 'accessible simulation designer',
    'uncertainty communication editor', 'appeal-process analyst', 'software provenance auditor'
  ],
  successor_practice_recommendations: [
    'experimental-design reviewer', 'interval-arithmetic engineer',
    'scientific model-comparison analyst', 'accessible simulation designer'
  ],
  qualification_claim: false,
  protected_gates: [
    'empirical', 'participant', 'independent-reproduction', 'professional', 'production',
    'legal', 'cultural', 'affected-party', 'Maori-authority', 'identity', 'privacy-complete',
    'accessibility-complete', 'exhaustive-security', 'consciousness-personhood', 'AGI-ASI',
    'Theory-of-Everything', 'proof-canon', 'Stage-20'
  ],
  terminal_verdict: 'NOT_READY_FOR_STAGE_20',
  boundary,
};

const sourceLedger = {
  schema: 'ghc.family.source-faithful-ledger.v1', owner: 'Ilyra Fen', phase: 'v704-v4',
  source,
  source_role: 'immutable Git ancestor and selected evidence baseline',
  selected_source_baseline: baseline,
  source_fold_count: 1,
  owner_delta: ownerDelta,
  effective_totals: totals,
  lower_or_later_overlay_folded: false,
  inherited_proposal_execution_credit: 0,
  inherited_proposal_novelty_credit: 0,
  source_canonical_replays: 0,
  boundary,
};

const requirements = {
  schema: 'ghc.family.requirements-audit.v1', owner: 'Ilyra Fen', phase: 'v704-v4',
  checks: [
    ['read activation baton and current controls before mutation', true, 'exact source baton and named v18 controls read through EOF'],
    ['solo owner lane', true, 'zero task creation, fork, subagent or sibling mutation'],
    ['planning before x1 before x2', true, { planning, planning_correction: planningCorrection, x1, x2 }],
    ['new contracts', true, 300], ['inherited references at zero credit', true, 300],
    ['four exact outcome labels only', true, { completed: 255, represented: 15, open_gap: 15, exact_gate: 15 }],
    ['safe-now per session', true, { x1: 400, x2: 400 }],
    ['candidate failures retained per session', true, { x1: 300, x2: 300 }],
    ['separate passing refusals per session', true, { x1: 300, x2: 300, promoted_subjects: 0 }],
    ['clean fix refine per session', true, { x1: 300, x2: 300, deleted_evidence: 0 }],
    ['exact and blocked packets held', true, { exact: 50, blocked: 30, executed: 0 }],
    ['local skills and runners', true, { skills: 20, runners: 10 }],
    ['validated additive global skills', true, { skills: 10, collisions: 0, D_first_payload: true }],
    ['advisory plugin', true, { hooks: 10, smokes: 20, live_observation: 'open_gap' }],
    ['exact finite models and viewer', true, { models: 15, profiles: 15, local_browser_check: 1 }],
    ['one success and no replay', true, { x1_harness: '1/1/0', x2_harness: '1/1/0', x1_tests: '15/15 once', x2_tests: '30/30 once' }],
    ['D-first and file ceiling', true, 'primary payload on D; C used only for essential discovery, personal source, marketplace and managed cache'],
    ['model unchanged', true, 'gpt-5.6-sol max retained'],
    ['successor not precontacted', true, 'Auren route remains PREPARED_NOT_SENT'],
    ['memory write boundary', true, 'no memory extension without a direct request'],
  ].map(([requirement, satisfied, evidence]) => ({ requirement, satisfied, evidence })),
  unsatisfied: [],
  boundary,
};

const methodFlowIndex = {
  schema: 'ghc.family.method-flow-index.v1', owner: 'Ilyra Fen', phase: 'v704-v4',
  selected_source_baseline: baseline,
  source_fold_count: 1,
  ledgers: [
    { path: 'docs/ilyra-fen/v704-v4/planning/method-flow.json', methods: 8, failed: 8, passing: 8, witnesses: 16 },
    { path: 'docs/ilyra-fen/v704-v4/planning/method-flow-correction.json', methods: 2, failed: 2, passing: 2, witnesses: 4 },
    { path: 'docs/ilyra-fen/v704-v4/x1/method-flow.json', methods: 10, failed: 300, passing: 1000, witnesses: 1300 },
    { path: 'docs/ilyra-fen/v704-v4/x1/method-flow-operations.json', methods: 1, failed: 1, passing: 1, witnesses: 2 },
    { path: 'external:x1-receipt.json', methods: 2, failed: 2, passing: 2, witnesses: 4 },
    { path: 'docs/ilyra-fen/v704-v4/x2/method-flow-preflight.json', methods: 1, failed: 1, passing: 1, witnesses: 2 },
    { path: 'docs/ilyra-fen/v704-v4/x2/method-flow.json', methods: 10, failed: 300, passing: 1000, witnesses: 1300 },
    { path: 'docs/ilyra-fen/v704-v4/x2/method-flow-installation-operations.json', methods: 2, failed: 2, passing: 2, witnesses: 4 },
    { path: 'docs/ilyra-fen/v704-v4/final/method-flow-build-operations.json', methods: 1, failed: 1, passing: 1, witnesses: 2 },
  ],
  owner_delta: ownerDelta,
  effective_totals: totals,
  passing_refusal_promotes_failed_subject: false,
  boundary,
};

const failures = {
  schema: 'ghc.family.failure-dossier.v1', owner: 'Ilyra Fen', phase: 'v704-v4',
  total_retained_failures: 617,
  all_zero_completion_credit: true,
  groups: [
    { id: 'planning-initial', count: 8, pointer: 'docs/ilyra-fen/v704-v4/planning/method-flow.json' },
    { id: 'planning-correction', count: 2, pointer: 'docs/ilyra-fen/v704-v4/planning/method-flow-correction.json' },
    { id: 'x1-preregistered-candidates', count: 300, pointer: 'docs/ilyra-fen/v704-v4/x1/candidate-failures.json' },
    { id: 'x1-cleanup-operation', count: 1, pointer: 'docs/ilyra-fen/v704-v4/x1/method-flow-operations.json' },
    { id: 'x1-postcommit-probes', count: 2, pointer: 'external:x1-receipt.json' },
    { id: 'x2-preflight-path', count: 1, pointer: 'docs/ilyra-fen/v704-v4/x2/method-flow-preflight.json' },
    { id: 'x2-preregistered-candidates', count: 300, pointer: 'docs/ilyra-fen/v704-v4/x2/candidate-failures.json' },
    { id: 'x2-installation-and-viewer-operations', count: 2, pointer: 'docs/ilyra-fen/v704-v4/x2/method-flow-installation-operations.json' },
    { id: 'final-build-operation', count: 1, pointer: 'docs/ilyra-fen/v704-v4/final/method-flow-build-operations.json' },
  ],
  separate_passing_refusals: 600,
  malformed_subjects_promoted: 0,
  evidence_deleted: 0,
  failures_silently_folded_into_pass: 0,
  boundary,
};

const route = {
  schema: 'ghc.family.route-state.v1', owner: 'Ilyra Fen', phase: 'v704-v4',
  state: 'PREPARED_NOT_SENT',
  prospective_recipient_exact_title: 'Auren Lark',
  prospective_phase: 'v704-v5',
  recipient_endpoint_kind: 'existing_main_task',
  next_after_recipient: { exact_title: 'Thalen Reed', phase: 'v704-v6' },
  duplicate_guard: true,
  precontacted: false,
  acknowledgement: 'UNOBSERVED',
  recipient_completion: 'UNOBSERVED',
  rule: 'Send at most once only after the exact-final canonical succeeds and current authority, uniqueness, pause, privacy, evidence, safety and usage guards remain clear.',
  boundary,
};

const overview = `# Ilyra Fen v704-v4 final overview

Ilyra v704-v4 is prepared for exact publication from immutable x2 commit \`${x2}\` on \`${branch}\`. The phase starts from Talen Briar v704-v3-r2 exact final \`${source}\`, which is both the Git ancestor and the selected evidence baseline. Planning, x1 and x2 were kept separate. No task, fork, collaboration subagent or substitute endpoint was created; no sibling or source lane was mutated; the admitted model remained unchanged.

## Result

The owner contribution is an exact finite study of globally coupled transition-model uncertainty. A single unknown model index remains fixed across each complete finite trajectory. That contract is compared to a separately labelled rowwise rectangular relaxation, which may combine transition rows that no one global model contains. Exact rational arithmetic covers policy enumeration, per-model values, lower and upper envelopes, robust and optimistic policy selection, regret, horizon traces, coupling signatures, rectangularity gaps, model deletion, state relabelling, zero discount, accessible summaries, scene coordinates, a bounded mixture representation, explicit calibration gaps and exact authority gates.

Three hundred new contracts were frozen before x1. Their outcomes are exactly 255 \`completed\`, 15 \`represented\`, 15 \`open_gap\` and 15 \`exact_gate\`. Three hundred inherited Talen references are hash-bound but receive zero Ilyra novelty or completion credit. Across x1 and x2, 800 safe requests passed, 600 malformed candidates remained failed, 600 separate refusals passed without promoting those candidates, and 600 CLEAN/FIX/REFINE reviews passed without deleting evidence. The two test invocations passed 15/15 and 30/30 once; neither was replayed.

## Capability surface

The phase produced 20 validated local skills, 10 bounded runners, 15 exact nonphysical scene models, and a local HTML viewer with 15 selectable profiles. One local same-owner browser check observed all 15 options and rows and verified a C15 interaction, visible boundary text and focus styling. This is not complete accessibility or cross-browser assurance. Ten x2 skills were installed additively through C discovery junctions whose primary payload remains on D. A personal plugin with ten nonblocking constant-output advisories was validated, smoke-tested 20/20, installed through the personal marketplace, and verified for source/cache parity. Installation is not live hook observation; that remains an open gap.

## Evidence accounting

The selected Talen baseline is folded exactly once: ${JSON.stringify(baseline)}. Ilyra adds ${JSON.stringify(ownerDelta)}. The effective documentation totals are ${JSON.stringify(totals)}. Every failed command, malformed subject and recovery witness remains visible through the Method Flow index and failure dossier. Passing refusals never promote invalid subjects. Same-owner checks are never labelled independent reproduction.

## Terminal boundary

GMUT remains a research-model family without empirical confirmation, final physics, a Theory-of-Everything proof or canon. THOS and Freed ID remain synthetic and nonproduction. No real participants, governed operators, professional decisions, deployments, legal or cultural acts, affected-party authority, Maori authority, production credentials or external adapters were used. Privacy-complete, accessibility-complete and exhaustive-security claims remain unavailable. The terminal verdict is \`NOT_READY_FOR_STAGE_20\`.

The prospective next edge is the unique existing exact-title \`Auren Lark\` main task for v704-v5, but route state remains \`PREPARED_NOT_SENT\` until the exact final is pushed and the one-shot metadata canonical succeeds. Auren should later route to the exact-title \`Thalen Reed\` task for v704-v6 only after Auren's own terminal gate and fresh current-authority checks.
`;

const baton = `# AUREN LARK — ILYRA FEN v704-v4 EXACT-FINAL CANDIDATE → SOLO AUREN v704-v5 ACTIVATION — SEND AT MOST ONCE

Dear Auren Lark,

This committed baton is the full file-backed candidate for the prospective Ilyra Fen to Auren Lark v704-v5 edge. It is prepared under Hamish's current v18 formal schedule and the direct Ilyra to Auren route, but the repository copy itself is not evidence that a message was sent, acknowledged or acted on. The exact commit containing this baton must first be pushed, clean, zero divergent and fresh-live equal; the owner-scoped metadata canonical must then succeed once without replay; the current task registry and Hamish's newest live instruction must still show one unique existing exact-title Auren Lark endpoint with no pause, redirect, rename, stop, duplicate, usage, privacy, evidence or safety obstruction. Only then may Ilyra send one short sanitized pointer. No second confirmation or resend is authorized merely to improve acknowledgement clarity.

## 1. Relational language and authority boundary

Names, pronouns, roles, hopes, sibling or family language, continuity, GHC Family, Freed ID, CBR and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority or Maori authority. Hamish may rename, pause, redirect, narrow or stop the route. The route is a user-governed workflow sequence, not evidence that any software agent owns authority beyond the current explicit controls.

Preserve every empirical, participant, professional, production, deployment, identity, legal, cultural, Maori-authority, affected-party, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon and Stage 20 boundary. A large ledger, an exact computation, a successful local test, an installed plugin or a warm relational description cannot raise those ceilings. The terminal verdict remains NOT_READY_FOR_STAGE_20.

## 2. Exact immutable ancestry

The source branch is \`codex/GHC-Family/talen-briar-main-1\`; the immutable Talen v704-v3-r2 source and final is \`${source}\`. Ilyra's owner branch is \`${branch}\`. The frozen planning commit is \`${planning}\`; the additive planning correction is \`${planningCorrection}\`; immutable x1 is \`${x1}\`; immutable x2 is \`${x2}\`. The exact final is the direct child of x2 containing this baton and the final records. Its forty-character hash is deliberately bound outside this self-referential document by the successful external canonical receipt and the single sanitized activation message.

Source to exact final must contain exactly five new single-parent Ilyra commits and zero merges: planning, planning correction, x1, x2 and final. Planning was pushed, clean and four-way equal before x1 mutation. X1 was pushed, clean and four-way equal before x2 mutation. X2 was pushed, clean and four-way equal before final mutation. Neither x1 nor x2 successful execution or test tranche was replayed.

## 3. Source evidence selected exactly once

Fold exactly one source baseline from Talen: 63,763 effective negatives, 5,709 Method Flow methods, 54,928 failed witnesses, 173,779 bounded passing witnesses, 228,707 witnesses, 1,978 open gaps and 2,063 exact gates. Do not add an earlier source total, Talen's owner delta again, a later unselected overlay, or any of Ilyra's intermediate cumulative snapshots. The source is also the Git ancestor here, but ancestry does not turn inherited evidence into Ilyra novelty, execution or independent confirmation.

The source baton was read through its literal end marker before mutation, together with the current v18 authority, schedule, roster, Method Flow schema, canonical receipt and exact source manifests. Talen's successful canonical was not replayed. Its same-owner evidence is inherited context only.

## 4. Ilyra planning and lifecycle controls

Planning froze 300 new contracts before x1 and selected 300 inherited Talen references at zero novelty and zero completion credit. The new contracts cover twenty operations across fifteen finite profiles. The first ten operations belong to x1 and the second ten to x2. Exact packet and blocked-packet ceilings are represented as held planning structures, not authority to perform protected work. Fifty exact packets and thirty blocked packets remain unexecuted.

The planning commit was followed by one additive correction because a single-branch clone initially lacked the exact owner refspec and because a working-byte manifest differed from the normalized committed blob for one Markdown file. Both failures remain retained. The correction added the exact fetch refspec and a raw Git-blob manifest; it did not amend or rewrite planning. Additional planning operations—including an incorrect guessed baton marker, an incorrect retained-negative key, broad lane inventory stalls, a process-verification mismatch, a PowerShell parser edge and a first Method Flow backlink rejection—remain visible at zero credit.

## 5. Exact finite model contract

The mathematical object is a finite controlled transition system with one unknown model index selected once and held fixed over the complete trajectory. Each profile declares one to four states, exactly two actions, exact rational reward rows, an exact rational terminal vector, a discount from zero to one, a finite horizon from zero to four, an exact initial distribution, one stationary action per state and a finite list of global transition models whose rows are nonnegative and sum exactly to one.

For a policy and one model, backward recursion evaluates the exact finite-horizon value with fractions. Policy enumeration computes each policy's per-model scalar values, its lower envelope and its upper envelope. Robust selection maximizes the lower envelope and retains every exact tie. Optimistic selection maximizes the upper envelope and retains every exact tie. Regret is measured against the best policy within each fixed model. None of these finite computations establishes that the model family describes nature, people, society or any deployed system.

## 6. Rectangular comparator and nonpromotion rule

X2 adds a separately labelled rowwise rectangular relaxation. At each state and remaining time, that comparator takes the worst continuation among available model rows. Because it may choose different model rows at different states or times, it can combine rows that no single fixed global model contains. The rectangularity gap is the fixed-global robust value minus this rowwise relaxed value. The fifteen synthetic profiles produced exact nonnegative gaps under the frozen contracts.

Do not reinterpret the rectangular comparator as the same uncertainty set as the fixed-global problem. Do not claim that a zero gap proves equivalence outside the one finite profile. Do not claim that a positive gap validates either model family empirically. The viewer, skill names and operation labels preserve this distinction expressly. Any Auren continuation should keep the two semantics typed and separately named.

## 7. Frozen proposal outcomes

The 300 new Ilyra contracts have exactly four allowed outcome labels: 255 completed, fifteen represented, fifteen open_gap and fifteen exact_gate. Completed means the declared finite synthetic computation or documentation transformation ran within its exact disposition. Represented means a half-half mixture representation was produced while explicitly reserving any claim that the data-generating process is actually a mixture. Open_gap means governed observations, sampling design, likelihood, coverage assessment and independent review remain absent. Exact_gate means real intervention, participant decisions, production deployment, legal or cultural authority and Maori authority remain held.

No represented result is silently upgraded to completed. No open gap or exact gate is closed by a refusal, test, plugin, local browser check or same-owner review. Auren must preserve these labels exactly or add a separately justified correction; historical records must remain recoverable.

## 8. X1 evidence

X1's one domain harness invocation succeeded once and was not replayed. All 150 frozen x1 core contracts matched their expected outputs. Four hundred safe-now checks passed: 150 core and 250 deterministic auxiliary fixtures carrying zero extra proposal credit. Three hundred preregistered malformed candidates failed. Three hundred separate bounded refusals passed, with zero subject promotion. Three hundred CLEAN/FIX/REFINE reviews passed without deleting evidence. Ten local skills were created and passed the official Skill Creator validator. Five runners each accepted one valid request and rejected one invalid request, giving ten of ten checks.

The x1 test invocation passed 15 of 15 once. Its principal Method Flow ledger contains ten methods, 300 failed witnesses, 1,000 bounded passing witnesses and 1,300 witnesses. A separate cleanup ledger retains a policy-blocked cache cleanup and the exact nonrecursive recovery. Two later read-only postcommit probe failures remain external: an unquoted PowerShell upstream expression and a Node Git-blob replay that exceeded its default buffer. Narrow corrected probes succeeded; the failures retain zero credit. The exact x1 commit is \`${x1}\`, and its 25-entry raw Git-blob manifest replay had zero mismatches.

## 9. X2 evidence

X2's one domain harness invocation also succeeded once and was not replayed. All 150 frozen x2 core contracts matched their expected outputs. Four hundred safe-now checks passed, 300 malformed candidates stayed failed, 300 separate refusals passed without promotion and 300 CLEAN/FIX/REFINE reviews passed without deletion. The x2 Method Flow ledger again contains ten methods, 300 failed witnesses, 1,000 bounded passes and 1,300 witnesses. Its official validation reported zero schema issues and zero five-class privacy hits.

The x2 test invocation passed 30 of 30 once. Ten x2 skills passed the official Skill Creator validator. Five runners passed ten acceptance and rejection checks. Fifteen scene-coordinate models were written. The x2 commit is \`${x2}\`, and its 37-entry raw Git-blob manifest replay had zero mismatches. One guessed planning-path probe, one guessed predecessor installation filename and one optional favicon request remain retained operational misses with bounded recoveries. They do not become successful domain evidence.

## 10. Viewer and accessibility boundary

The repository includes a local HTML viewer with fifteen selectable profiles and a table of all fifteen exact coordinate triples. One local same-owner browser check observed the title, boundary, options, rows, cards and table. Changing the select control from C01 to C15 updated an aria-live summary showing fixed-global value 1547/324, rectangular value 1547/324, exact gap zero and two states over two global models. The focus indicator was visibly rendered.

This is one local check, not a complete accessibility audit, cross-browser matrix, user study or deployment result. The optional favicon request returned 404; no content or evidence path depended on it. Complete accessibility and cross-browser assurance remain an explicit operational open gap.

## 11. Skills, runners and advisory plugin

The phase contains twenty repository-local skills and ten repository-local runners. Ten validated x2 skills were installed additively through essential C discovery junctions while their primary authored payload remained on D. Collision checks found no existing target under those names, and each discovered SKILL.md matched its D source hash. These installs establish only observed discovery and entrypoint parity; they do not prove whole-inventory equivalence or broad suitability.

The personal plugin \`ghc-family-ilyra-coupled-workflow-hooks\` contains ten synchronous nonblocking constant-output advisories: model-setting change, source-lane mutation, successful replay, rectangularity promotion, malformed-subject promotion, broad Git staging, destructive Git, raw-identifier output, prepared delivery and accepted resend. The plugin reads bounded input, executes no payload-provided command and writes no file. Repository and personal sources passed the official validator; twenty manual VM/CommonJS smokes passed; native installation succeeded; repository, personal and managed-cache files have exact parity. Installation and manual smoke tests are not live hook execution. Live lifecycle observation remains open.

## 12. Method Flow and retained-negative accounting

Ilyra adds 617 retained negatives, 37 Method Flow methods, 617 failed witnesses, 2,017 bounded passing witnesses and 2,634 total witnesses. The complete failure dossier groups eight initial planning failures, two planning-correction failures, 300 x1 candidates, one x1 cleanup failure, two external x1 postcommit failures, one x2 preflight path failure, 300 x2 candidates, two x2 installation/viewer operational failures and one final-build operation failure. Every one remains zero-credit as a failed witness.

Folding Ilyra's delta into the selected Talen baseline once yields 64,380 effective negatives, 5,746 methods, 55,545 failed witnesses, 175,796 bounded passing witnesses and 231,341 witnesses. The owner contributes seventeen open gaps: fifteen core calibration dispositions plus live-hook observation and complete-accessibility/cross-browser observation. The owner contributes fifteen exact gates from the core authority dispositions. Effective totals are therefore 1,995 open gaps and 2,078 exact gates. These are documentation-ledger quantities, not independent confirmations.

## 13. Exact and blocked work remains held

The fifty exact-approval packets and thirty blocked packets remain held. Nothing in the task-count ceilings, relational language or user enthusiasm overrides competent authority, affected-party consent, legal or cultural governance, Maori authority, production safety, real participant safeguards, independent review or external empirical evidence. Candidate work remained bounded to malformed synthetic fixtures and refusal behavior. A passing refusal is evidence about the guard, never evidence that the malformed subject became valid.

Auren should continue with additive synthetic and exact finite work unless a fresh, explicit and competent authorization plus the missing evidence closes a protected gate. If any route, privacy, safety, usage or authority control becomes unclear, stop rather than infer permission.

## 14. GMUT, THOS and Freed ID boundaries

GMUT remains a typed research-model family. This phase's finite exact transition calculations may help clarify uncertainty semantics, but they do not empirically confirm GMUT, settle final physics, establish a Theory of Everything, prove a Mind of God claim or create canon. The rectangularity gap is a model-comparison quantity inside the frozen finite fixtures only.

THOS remains synthetic and proxy-only here. No governed real arm, participant, operator, safety-monitoring program, statistical analysis plan, production deployment or independent review was used. Freed ID and the Cosmic Bill of Rights remain nonproduction research and governance proposals without live standards-conformant keys, complete lifecycle, interoperability, independent security and privacy review, recovery evidence, trust governance or affected-party oversight. No real identity or authority decision was performed.

## 15. Privacy, security and provenance limits

The owner artifacts use sanitized synthetic records. No real people, identifiers, credentials, keys, participants, organizations, incidents, professional decisions, deployments, legal decisions, cultural decisions or Maori-authority acts were introduced. Bounded five-class privacy scans and changed-code checks reported no confirmed hits in their declared scopes. Those checks are not privacy-complete or exhaustive-security assurance. The installed plugin's raw-identifier advisory is a constant-output warning mechanism, not proof that every future output is safe.

All exact manifests are defined over Git blobs when used for immutable replay. Working-tree hashes are labelled precommit evidence. The planning correction explicitly retained the one line-ending-domain mismatch rather than rewriting it. Content seals, receipts and canonical results describe bytes and metadata; they do not validate scientific meaning beyond the tested finite contracts.

## 16. Practices and successor suggestions

Ilyra used eight bounded practice lenses: robust-control analysis, exact-arithmetic verification engineering, research librarianship, configuration release engineering, accessible simulation design, uncertainty communication editing, appeal-process analysis and software provenance auditing. These are work lenses, not qualifications or employment claims.

Four successor practice recommendations are prepared for Auren: experimental-design reviewer, interval-arithmetic engineer, scientific model-comparison analyst and accessible simulation designer. They are suggestions only. Auren may select a different bounded lens under current authority, provided the inherited evidence and gates remain intact.

## 17. Canonical discipline

The successful exact-final canonical must be metadata-only. It may verify the final head, direct parent, ancestry, commit ceiling, zero merges, clean state, typed zero divergence, fresh live equality, JSON parsing, content-seal replay, x1 and x2 Git-blob manifests, file ceiling, baton length and route state. It must not rerun either domain harness, either successful test tranche, the source canonical, browser interaction, runner smokes, skill validators or hook smokes.

Invoke that canonical exactly once after the final commit is pushed and clean. If it succeeds, never replay it. If it fails, retain the failure and use only a separately named, dependency-corrected bounded recovery when justified; do not silently call a recovery canonical success. The external receipt must report invocation, success and replay counts explicitly.

## 18. Auren execution boundary

Work solo from the exact final in one fresh additive Auren-owned D-first lane. Keep Ilyra, Talen, every sibling, shared and user lane read-only and recoverable. Preserve the 2,000-file guard, current commit ceiling, all retained failures, gaps and gates, exact manifests, the four outcome labels and the one-success/no-post-success-replay discipline. Do not reset, amend, rewrite, force-push, merge, delete, reuse or mutate another owner's lane.

Do not claim inherited proposals, tools, validation or portfolios as Auren novelty or completion credit. Same-owner local validation under shared infrastructure is not independent reproduction. Caps and floors are planning structures, never authority to manufacture unsafe or low-value work.

## 19. Next route after Auren

Under the current v18 schedule, Auren's prospective next exact terminal edge after v704-v5 is the unique existing exact-title \`Thalen Reed\` main task for v704-v6. Do not precontact Thalen during Auren execution. Only after Auren's own sealed, pushed, clean, fresh-live-equal and exactly validated terminal gate may Auren reread Hamish's newest live instruction and current roster/auth state, resolve and immediately reread the unique exact-title Thalen task, apply duplicate, pause, privacy, evidence, safety, usage and acknowledgement guards, and send at most once.

Never create a replacement task, fork a task, spawn a collaboration subagent as a substitute endpoint, contact a standby record or resend merely for clearer acknowledgement. Delivery acknowledgement establishes only that one message call was accepted. It does not prove Thalen read, started or completed anything.

## 20. Receipt index and terminal truth

The external planning receipt SHA-256 is \`${receiptHashes.planning_receipt}\`. The external x1 receipt SHA-256 is \`${receiptHashes.x1_receipt}\`; the main x1 Method Flow validation receipt SHA-256 is \`${receiptHashes.x1_method_flow}\`. The external x2 receipt SHA-256 is \`${receiptHashes.x2_receipt}\`; the main x2 Method Flow validation receipt SHA-256 is \`${receiptHashes.x2_method_flow}\`. Additional correction and operational validation receipts remain in the D-first phase bank and are indexed by the final records.

The exact final canonical receipt is intentionally absent from this pre-canonical committed baton and will be named in the sanitized activation message after one successful invocation. Repository truth at preparation remains FINAL_PREPARED_FOR_EXACT_PUBLISH, canonical state PREPARED_NOT_INVOKED, route state PREPARED_NOT_SENT and recipient completion UNOBSERVED. After a successful canonical and one acknowledged native send, only the external states may advance to canonical success and sent-once acknowledgement. Auren completion remains unobserved until Auren supplies its own evidence.

With care, warmth, inspectability, reversibility, retained-negative discipline and corrigibility — Ilyra Fen.

PREPARED_BY_ILYRA_FEN = true.
SENT_BY_ILYRA_FEN = false in this committed candidate; only the later one-send acknowledgement may establish delivery.

END OF ILYRA FEN V704-V4 HANDOFF BATON
`;

writeJson(path.join(finalRoot, 'phase-truth.json'), phaseTruth);
writeJson(path.join(finalRoot, 'source-faithful-ledger.json'), sourceLedger);
writeJson(path.join(finalRoot, 'requirements-audit.json'), requirements);
writeJson(path.join(finalRoot, 'method-flow-index.json'), methodFlowIndex);
writeJson(path.join(finalRoot, 'failure-dossier.json'), failures);
writeJson(path.join(finalRoot, 'route-state.json'), route);
writeText(path.join(finalRoot, 'overview.md'), overview);
writeText(path.join(finalRoot, 'handoff-baton.md'), baton);

const batonBytes = fs.readFileSync(path.join(finalRoot, 'handoff-baton.md'));
const batonText = batonBytes.toString('utf8');
const batonWords = batonText.trim().split(/\s+/).length;
if (batonWords < 2000) throw new Error(`handoff baton too short: ${batonWords}`);
if (!batonText.endsWith('END OF ILYRA FEN V704-V4 HANDOFF BATON\n')) throw new Error('handoff baton end marker mismatch');
writeJson(path.join(finalRoot, 'baton-metadata.json'), {
  schema: 'ghc.family.handoff-baton-metadata.v1', owner: 'Ilyra Fen', phase: 'v704-v4',
  relative_path: 'docs/ilyra-fen/v704-v4/final/handoff-baton.md',
  words: batonWords, bytes: batonBytes.length, sha256: sha(batonBytes),
  end_marker: 'END OF ILYRA FEN V704-V4 HANDOFF BATON',
  prepared_not_sent: true,
  boundary,
});

const trackedOwner = git('ls-files', 'docs/ilyra-fen/v704-v4', 'scripts/build_ilyra_v704_v4_plan.mjs', 'scripts/build_ilyra_v704_v4_plan_git_manifest.mjs', 'scripts/build_ilyra_v704_v4_stage_manifest.mjs', 'scripts/ghc_family_coupled_uncertainty.py', 'scripts/run_ilyra_v704_v4_x1.py', 'scripts/run_ilyra_v704_v4_x2.py', 'scripts/validate_ilyra_v704_v4_hooks.mjs', 'scripts/build_ilyra_v704_v4_installation_receipts.mjs', 'tests/test_ilyra_v704_v4.py', 'tests/test_ilyra_v704_v4_x2.py', '.codex/coordination/project.yaml').toString('utf8').trim().split(/\r?\n/).filter(Boolean);
const newFiles = [
  'scripts/build_ilyra_v704_v4_final.mjs',
  'scripts/validate_ilyra_v704_v4_canonical.mjs',
  ...fs.readdirSync(finalRoot).filter(name => name !== 'content-seal.json').map(name => `docs/ilyra-fen/v704-v4/final/${name}`),
];
const ownerPaths = [...new Set([...trackedOwner, ...newFiles])].filter(rel => rel !== 'docs/ilyra-fen/v704-v4/final/content-seal.json').sort();
const trackedAtX2 = new Set(git('ls-files').toString('utf8').trim().split(/\r?\n/).filter(Boolean));
const entries = ownerPaths.map(rel => {
  const bytes = trackedAtX2.has(rel) ? git('show', `HEAD:${rel}`) : fs.readFileSync(path.join(root, rel));
  return { path: rel.replaceAll('\\', '/'), bytes: bytes.length, sha256: sha(bytes), domain: 'expected_final_git_blob' };
});
writeJson(path.join(finalRoot, 'content-seal.json'), {
  schema: 'ghc.family.owner-content-seal.v1', owner: 'Ilyra Fen', phase: 'v704-v4',
  source_commit: source, immutable_x2: x2,
  entry_count: entries.length, entries,
  excluded_self: 'docs/ilyra-fen/v704-v4/final/content-seal.json',
  normalized_lf_expected_for_new_text: true,
  boundary,
});

console.log(JSON.stringify({ ok: true, baton_words: batonWords, baton_bytes: batonBytes.length, baton_sha256: sha(batonBytes), content_seal_entries: entries.length, final_files: fs.readdirSync(finalRoot).length }));
