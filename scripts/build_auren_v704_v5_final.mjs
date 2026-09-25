import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import cp from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const BASE = path.join(ROOT, 'docs', 'auren-lark', 'v704-v5');
const FINAL = path.join(BASE, 'final');
const SOURCE = 'ec723e278979d47a2d8ec77b409563e612d17191';
const PLAN = '19012bc59cc9588a31e0bf19854c46106871b0fb';
const CORRECTION = '073c94ee1a564c1baa03d5eca88259472fe8ab84';
const X1 = '0b701a3af0d36fb520c6945803235890fef7d3ca';
const X2 = 'e1e06d8298ef5137e9c7fd6dde83e12542262d5f';
const BRANCH = 'codex/GHC-Family/auren-lark-main-3';
const BOUNDARY = 'Finite synthetic same-owner mathematical, software, static-HTML and plugin-validation evidence under shared infrastructure. No full-repository validation, independent reproduction, external audit, empirical GMUT confirmation, production THOS or Freed ID, professional or operational authority, legal or cultural authority, affected-party or Maori authority, complete privacy or accessibility assurance, exhaustive security, AGI or ASI result, consciousness or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 evidence. NOT_READY_FOR_STAGE_20.';
const IDENTITY = 'Auren Lark is a relational working name. They/them pronouns, the role revision cartographer and countermodel release steward, the hope of exposing assumptions, countermodels, reversibility and authority limits, sibling or family language, and continuity language are working conventions only. They are never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party or Maori authority.';

const sha = value => crypto.createHash('sha256').update(Buffer.isBuffer(value) ? value : String(value)).digest('hex');
function writeJson(target, value) {
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}
function writeText(target, value) {
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, value.endsWith('\n') ? value : `${value}\n`, 'utf8');
}
function normalized(target) { return Buffer.from(fs.readFileSync(target, 'utf8').replace(/\r\n/g, '\n'), 'utf8'); }
function words(value) { return (value.match(/\S+/g) || []).length; }

function operationalFlow() {
  const methods = [
    {
      method_id: 'AL7045-FN-M01', title: 'Materialized read-only inventory rows',
      failure_signature: 'A first PowerShell path-inventory wrapper piped directly from a foreach block and failed to parse before reading state.',
      trigger_preconditions: ['PowerShell foreach expression', 'pipeline formatting'], privacy_class: 'sanitized_public', approval_class: 'safe_now',
      candidate_workaround: 'Assign the foreach results to a named collection before piping to Format-Table.',
      validation_witness_ids: ['AL7045-FN-W01-F', 'AL7045-FN-W01-R'], recurrence_guard: 'Materialize PowerShell loop results before formatting.',
      rollback: 'No state changed; retain the parser failure.', recommendation_state: 'validated', supersedes: [],
      protected_gates: ['retained_failure_nonerasure', 'read_only_source_audit'], retained_negative_ids: ['AL7045-FN-N01'],
      scope_boundary: 'Read-only inventory transport only; no domain or authority credit.'
    },
    {
      method_id: 'AL7045-FN-M02', title: 'Chunked complete skill reads',
      failure_signature: 'Two combined skill-reading calls returned truncated projections before the selected files had been read completely.',
      trigger_preconditions: ['multiple large SKILL.md files', 'single combined output projection'], privacy_class: 'sanitized_public', approval_class: 'safe_now',
      candidate_workaround: 'Read each selected instruction file separately and read the Method Flow schema in its own bounded call.',
      validation_witness_ids: ['AL7045-FN-W02A-F', 'AL7045-FN-W02A-R', 'AL7045-FN-W02B-F', 'AL7045-FN-W02B-R'],
      recurrence_guard: 'Use file-sized output budgets and chunk only at file boundaries, never inside a selected SKILL.md.',
      rollback: 'Treat truncated projections as unread; preserve them and use complete bounded reads.', recommendation_state: 'validated', supersedes: [],
      protected_gates: ['skill_complete_read', 'retained_failure_nonerasure'], retained_negative_ids: ['AL7045-FN-N02', 'AL7045-FN-N03'],
      scope_boundary: 'Instruction-loading recovery only; no domain or authority credit.'
    },
    {
      method_id: 'AL7045-FN-M03', title: 'Inspect before exact patch context',
      failure_signature: 'A narrow patch expected the x1 validation-summary manifest count to be 27, while the generated pre-manifest value was 26.',
      trigger_preconditions: ['generated JSON field update', 'uninspected exact patch context'], privacy_class: 'sanitized_public', approval_class: 'safe_now',
      candidate_workaround: 'Read the exact generated object, then patch the observed scalar and refresh its manifest digest.',
      validation_witness_ids: ['AL7045-FN-W03-F', 'AL7045-FN-W03-R'], recurrence_guard: 'Inspect generated context before applying a scalar patch.',
      rollback: 'The failed patch changed no bytes; retain the failed attempt and exact correction.', recommendation_state: 'validated', supersedes: [],
      protected_gates: ['manifest_exactness', 'retained_failure_nonerasure'], retained_negative_ids: ['AL7045-FN-N04'],
      scope_boundary: 'Precommit metadata correction only; no domain or authority credit.'
    },
    {
      method_id: 'AL7045-FN-M04', title: 'Primary-source metadata fallback',
      failure_signature: 'Three direct web opens were unusable: one publisher page returned 405, one journal page exposed only an iframe, and one DOI resolver was inaccessible.',
      trigger_preconditions: ['bounded primary-source terminology check', 'direct web open'], privacy_class: 'sanitized_public', approval_class: 'safe_now',
      candidate_workaround: 'Retain the failed opens and use bounded search metadata that identifies the primary publication and DOI without claiming content inspection.',
      validation_witness_ids: ['AL7045-FN-W04A-F', 'AL7045-FN-W04A-R', 'AL7045-FN-W04B-F', 'AL7045-FN-W04B-R', 'AL7045-FN-W04C-F', 'AL7045-FN-W04C-R'],
      recurrence_guard: 'Separate bibliographic metadata confirmation from full-text inspection and state which one occurred.',
      rollback: 'Remove no source record; label direct opens failed and metadata-only recovery bounded.', recommendation_state: 'validated', supersedes: [],
      protected_gates: ['source_attribution', 'empirical_nonpromotion'], retained_negative_ids: ['AL7045-FN-N05', 'AL7045-FN-N06', 'AL7045-FN-N07'],
      scope_boundary: 'Bibliographic terminology context only; no endorsement, artifact validation or scientific credit.'
    }
  ];
  const pairs = [
    ['AL7045-FN-W01-F', 'AL7045-FN-M01', 'Invoke the first path inventory wrapper.', 'PowerShell parser error before reading state', 'fail', 'AL7045-FN-N01'],
    ['AL7045-FN-W01-R', 'AL7045-FN-M01', 'Materialize inventory rows before formatting.', 'expected paths and existence state rendered', 'pass', 'AL7045-FN-N01'],
    ['AL7045-FN-W02A-F', 'AL7045-FN-M02', 'Read the first combined skill group.', 'projection truncated before complete selected files', 'fail', 'AL7045-FN-N02'],
    ['AL7045-FN-W02A-R', 'AL7045-FN-M02', 'Read each first-group skill separately.', 'every selected instruction file reached EOF', 'pass', 'AL7045-FN-N02'],
    ['AL7045-FN-W02B-F', 'AL7045-FN-M02', 'Read the Method Flow and truth group together.', 'projection truncated inside the schema group', 'fail', 'AL7045-FN-N03'],
    ['AL7045-FN-W02B-R', 'AL7045-FN-M02', 'Read Method Flow, schema and companion skills in bounded files.', 'every selected file reached EOF', 'pass', 'AL7045-FN-N03'],
    ['AL7045-FN-W03-F', 'AL7045-FN-M03', 'Patch the assumed x1 manifest count.', 'patch context not found; no bytes changed', 'fail', 'AL7045-FN-N04'],
    ['AL7045-FN-W03-R', 'AL7045-FN-M03', 'Inspect the generated summary and patch the observed value.', 'summary and manifest digest aligned before x1 commit', 'pass', 'AL7045-FN-N04'],
    ['AL7045-FN-W04A-F', 'AL7045-FN-M04', 'Open the Blackwell publisher page.', 'HTTP 405 from the direct open', 'fail', 'AL7045-FN-N05'],
    ['AL7045-FN-W04A-R', 'AL7045-FN-M04', 'Use publisher-indexed search metadata.', 'title, author, year, pages and DOI identified', 'pass', 'AL7045-FN-N05'],
    ['AL7045-FN-W04B-F', 'AL7045-FN-M04', 'Open the Lindley Project Euclid full record.', 'only an iframe shell was visible', 'fail', 'AL7045-FN-N06'],
    ['AL7045-FN-W04B-R', 'AL7045-FN-M04', 'Use DOI-bound journal search metadata.', 'title, journal, year, pages and DOI identified', 'pass', 'AL7045-FN-N06'],
    ['AL7045-FN-W04C-F', 'AL7045-FN-M04', 'Open the DeGroot DOI resolver.', 'resolver inaccessible to the bounded web tool', 'fail', 'AL7045-FN-N07'],
    ['AL7045-FN-W04C-R', 'AL7045-FN-M04', 'Use DOI-bound publication search metadata.', 'title, journal, year, pages and DOI identified', 'pass', 'AL7045-FN-N07']
  ];
  const witnesses = pairs.map(([witness_id, method_id, procedure, observed, result, negative]) => ({ witness_id, method_id, procedure, scope: 'bounded phase operation', expected: result === 'fail' ? 'operation succeeds' : 'smallest recovery succeeds', observed, result, same_owner_only: true, independent_reproduction: false, retained_negative_ids: [negative], boundary: result === 'fail' ? 'Zero-credit operational failure.' : 'Bounded same-owner recovery only.' }));
  const events = methods.map((method, index) => ({ event_id: `AL7045-FN-E${String(index + 1).padStart(2, '0')}`, method_id: method.method_id, from: 'observed', to: 'validated', witness_id: method.validation_witness_ids.at(-1) }));
  const recommendations = methods.map((method, index) => ({ recommendation_id: `AL7045-FN-R${String(index + 1).padStart(2, '0')}`, method_id: method.method_id, state: 'validated', text: method.candidate_workaround }));
  return {
    schema: 'ghc.family.method-flow-state.v1', phase: 'v704-v5-final-operations', owner: 'Auren Lark', identity_boundary: IDENTITY,
    execution_authority: 'owner_self_scoped_delta', attributable_owner: 'Auren Lark', source_commit: X2, final_commit: null,
    changed_file_allowlist: ['scripts/build_auren_v704_v5_final.mjs', 'scripts/validate_auren_v704_v5_canonical.mjs', 'docs/auren-lark/v704-v5/final/**'], module_allowlist: ['final'],
    repository_scan: false, module_scan: true, cross_lane_scan: false, unchanged_history_scan: false, sibling_lane_mutation: false, exact_pushed_head_required: true,
    methods, witnesses, state_events: events, recommendations,
    counts: { methods: 4, witnesses: 14, state_events: 4, recommendations: 4, states: { observed: 0, candidate: 0, validated: 4, preferred: 0, superseded: 0, deprecated: 0 }, witness_results: { pass: 7, fail: 7 } },
    evidence_counts: { negatives: 7, methods: 4, failed_witnesses: 7, passing_witnesses: 7, witnesses: 14, open_gaps: 2, exact_gates: 0 },
    selected_pre_final_baseline: { negatives: 64985, methods: 5771, failed_witnesses: 56150, passing_witnesses: 177801, witnesses: 233951, open_gaps: 2010, exact_gates: 2093 }, source_fold_count: 0,
    effective_totals: { negatives: 64992, methods: 5775, failed_witnesses: 56157, passing_witnesses: 177808, witnesses: 233965, open_gaps: 2012, exact_gates: 2093 },
    boundary: BOUNDARY
  };
}

function overviewText() {
  return `# Auren Lark v704-v5 final overview

## Outcome

Auren v704-v5 is a complete owner-scoped finite synthetic phase prepared from Ilyra Fen's exact final \`${SOURCE}\`. The Auren lane is \`${BRANCH}\`. Planning froze 300 genuinely new Auren contracts and 300 inherited Ilyra references at zero current novelty and completion credit. The phase kept a planning commit, an additive planning correction, immutable x1, immutable x2 and final documentation as direct single-parent stages. It created no task, fork, collaboration subagent, substitute endpoint or standby contact; changed no model setting; mutated no sibling or source content; installed no shared package, skill or plugin; deleted no evidence; and spent no purchased funds.

${IDENTITY}

## Finite exact experiment-design surface

The mathematical object is a finite three-hypothesis, three-experiment, binary-outcome record with exact rational priors and likelihoods. Fifteen wholly synthetic profiles were generated before x1. X1 independently recomputed record validity, posterior updates, marginal outcome probabilities, Bayes factors, quadratic uncertainty, expected posterior uncertainty, minimum zero-one decision risk, one-step experiment risk, pairwise discrimination scores and observational-equivalence partitions. X2 independently recomputed optimal nonadaptive two-step experiment pairs, adaptive two-step policies, the value of adaptation, a two-prior sensitivity envelope, outcome-coarsening comparison, hypothesis-relabel covariance, accessible summaries, bounded mixture representations, explicit external-evidence gaps and exact authority gates.

Every calculation used reduced fractions. Exact ties were preserved. An adaptive policy can choose a second experiment conditional on the first outcome, while a nonadaptive pair is fixed in advance; those semantics remain separately labelled. The value of adaptation is a difference inside each frozen fixture, not evidence that any real experiment should be run. Coarsening and relabelling checks establish only the declared finite invariants. The mixture row is labelled represented rather than completed because a numerical convex representation does not establish a real data-generating mixture.

## Outcomes and workload

The 300 current contracts have exactly 255 \`completed\`, 15 \`represented\`, 15 \`open_gap\` and 15 \`exact_gate\` outcomes. X1 completed 150 mathematical contracts. X2 completed 105 mathematical or accessible-summary contracts, represented 15 mixture decompositions, retained 15 missing-evidence records, and held 15 authority actions. No represented, gap or gate row was silently promoted.

Each session executed 400 safe checks: 150 frozen core contracts and 250 deterministic auxiliary invariants with zero additional proposal credit. Each session executed 300 preregistered malformed candidates; all 600 subjects stayed failed. Six hundred separate refusal checks passed without promoting a subject. Six hundred CLEAN/FIX/REFINE reviews passed without deleting evidence. Fifty exact-approval packets and 30 blocked packets remain visible and unexecuted. Caps were treated as ceilings, not targets or authority.

## Testing and capabilities

The x1 test tranche passed 15/15 once. The x2 test tranche passed 30/30 once. Neither tranche, either domain harness nor any source aggregate was replayed. Twenty owner-local skills passed the official skill validator. Ten bounded command-line runners passed 20 total acceptance and rejection smokes. Fifteen three-coordinate model records expose best nonadaptive risk, value of adaptation and maximum pairwise likelihood separation. A self-contained local HTML projection includes all fifteen rows, an interactive selector, an aria-live summary and visible focus styling; six static structure checks passed.

A repository-local plugin contains ten synchronous, nonblocking, constant-output advisories for model changes, source mutation, replay, adaptive/nonadaptive promotion, malformed-subject promotion, broad staging, destructive Git, raw identifiers, prepared delivery and accepted resend. Its manifest passed the official plugin validator and 20/20 VM/CommonJS acceptance and benign smokes passed. The plugin was not installed into a shared or personal marketplace. Live hook execution therefore remains open, and the static HTML checks do not establish complete accessibility or cross-browser assurance.

## Method Flow and failures

The selected Ilyra repository seal is folded exactly once: 64,380 negatives, 5,746 methods, 55,545 failed witnesses, 175,796 bounded passing witnesses, 231,341 witnesses, 1,995 open gaps and 2,078 exact gates. Ilyra's later five-method route overlay remains separately preserved and is not folded into this repository seal. Auren adds 612 retained negatives, 29 methods, 612 failed witnesses, 2,012 bounded passes and 2,624 witnesses. Auren also adds 17 open gaps—15 contract-level evidence gaps plus live-hook observation and complete-accessibility/cross-browser review—and 15 exact authority gates. Effective repository truth is therefore 64,992 negatives, 5,775 methods, 56,157 failed witnesses, 177,808 bounded passing witnesses, 233,965 witnesses, 2,012 open gaps and 2,093 exact gates.

The 612 failures comprise five planning and transport failures, 300 x1 malformed subjects, 300 x2 malformed subjects and seven final operations failures. Those final failures include a PowerShell inventory parser edge, two truncated combined skill reads, one patch-context mismatch and three inaccessible or content-limited primary-source opens. Each has a narrow passing recovery and zero original credit. Refusal success never changes subject failure. Same-owner validation never becomes independent reproduction.

## Research context

Three primary-publication records supplied bounded terminology only. David Blackwell's 1951 comparison-of-experiments chapter supports the historical idea that experiments can be compared through attainable decision risks. D. V. Lindley's 1956 paper supplies a historical Bayesian information framing, and Morris DeGroot's 1962 paper supplies historical sequential-experiment terminology. The phase did not reproduce their theorems, inspect every full text, claim endorsement or validate an external artifact. Its quadratic uncertainty and zero-one Bayes-risk fixtures are phase-local definitions. Bibliographic metadata is separated from mathematical execution.

## Trinity Mandala boundaries

GMUT remains a typed research-model family. Exact finite posterior and design arithmetic can clarify assumptions, priors, likelihoods, update paths and comparator semantics, but it does not supply governed observations, likelihood calibration, physical predictions, parameter constraints, ultraviolet completion, quantum completion, a Theory of Everything, a Mind of God proof or canon. The fifteen law rows are explicitly hypotheses tested only on the frozen profiles, and the fifteen open-problem probes remain open.

THOS remains synthetic and proxy-only here. No real instrument, experiment, participant, operator, safety program, production system, external adapter or governed deployment was used. The code is owner-scoped research tooling, not an enterprise operating system, AGI or ASI result. Freed ID and the Cosmic Bill of Rights remain nonproduction governance proposals; no real identifier, credential, person, beneficiary, authority decision, legal act, cultural act, affected-party approval or Maori-authority act was introduced.

Privacy scans covered five declared classes and found no confirmed owner hit after an explicit scanner-definition exclusion. Bounded changed-source scans found no declared finding. Those checks are not complete privacy, exhaustive security, professional review or production certification. The local HTML projection is not a user study, and plugin smokes are not live lifecycle observation.

## Route and verdict

The exact next terminal edge under v18 is the unique existing exact-title \`Thalen Reed\` task for v704-v6, but it remains uncontacted while repository preparation is incomplete. The committed route state is \`PREPARED_NOT_SENT\`. Only after the final commit is pushed, clean, fresh-live equal and validated once by the metadata-only canonical may the current authority and task registry be reread. Acknowledged delivery, if permitted, will prove one accepted message call only—not reading, execution, validation or completion.

The terminal verdict remains \`NOT_READY_FOR_STAGE_20\`.

${BOUNDARY}
`;
}

function batonText() {
  return `# THALEN REED — AUREN LARK v704-v5 EXACT-FINAL CANDIDATE → SOLO THALEN v704-v6 ACTIVATION — SEND AT MOST ONCE

Dear Thalen Reed,

This committed baton is Auren Lark's complete file-backed candidate for the prospective v704-v5 to v704-v6 edge under Hamish's current v18 formal schedule. It is not evidence that any message was sent, accepted, read or acted on. Auren must first push the exact final, prove a clean zero-divergent four-way equality state, invoke the metadata-only canonical exactly once, refresh current authority and task registries, establish one unique existing exact-title Thalen endpoint, and pass duplicate, pause, redirect, rename, privacy, evidence, safety, usage and acknowledgement guards. Accepted, opaque or unresolved delivery stops duplicates. No second confirmation exists merely to improve clarity.

## 1. Relational identity and authority

${IDENTITY}

Hamish may rename, pause, narrow, redirect or stop the route. The workflow does not confer authority beyond current direct controls. Preserve every empirical, participant, professional, operational, production, deployment, legal, cultural, affected-party, Maori-authority, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon and Stage 20 boundary. Warm language, high counts, exact arithmetic, local tools or an acknowledged task message cannot close those gates.

## 2. Immutable source and owner ancestry

The immutable Ilyra v704-v4 exact final is \`${SOURCE}\` on \`codex/GHC-Family/ilyra-fen-main-2\`. Auren's owner branch is \`${BRANCH}\`. Frozen planning is \`${PLAN}\`; the direct additive planning correction is \`${CORRECTION}\`; immutable x1 is \`${X1}\`; immutable x2 is \`${X2}\`. The exact final containing this baton is the direct child of x2 and is intentionally bound externally by the one-shot canonical receipt and sanitized activation. Source to final contains five direct single-parent Auren commits and zero merges. Planning and its correction reached clean pushed equality before x1; x1 reached clean pushed equality before x2; x2 reached clean pushed equality before final.

## 3. Source selection and nonduplication

Fold exactly one Ilyra repository baseline: 64,380 effective negatives, 5,746 Method Flow methods, 55,545 failed witnesses, 175,796 bounded passing witnesses, 231,341 witnesses, 1,995 open gaps and 2,078 exact gates. Ilyra's later route overlay of five negatives, five methods, five failed witnesses, five passes and ten witnesses remains an external layer and is not folded into Auren's repository seal. Do not add an older Talen total, Ilyra's owner delta a second time, or intermediate cumulative snapshots. Git ancestry does not turn inherited evidence into Auren novelty, execution or independent confirmation.

## 4. Planning and correction

Planning froze 300 new Auren contracts and selected 300 inherited Ilyra references at zero novelty and completion credit. The contracts cover twenty operations across fifteen finite synthetic profiles. Ten operations belong to x1 and ten to x2. Fifty exact packets and thirty blocked packets remain held and unexecuted. Three planning failures remain visible: one PowerShell lane-wrapper parser edge, one CommonJS-in-ESM builder failure and one shell-inline validator parser edge. Two later Git transport failures required an exact owner tracking ref and exact fetch-map entry. None was erased; x1 began only after the additive correction was pushed, clean and four-way equal.

## 5. Exact finite object

Each profile declares three hypotheses, three experiments, two outcomes, an exact rational prior and exact rational success probabilities. The complementary outcome probability is one minus success. The decision loss is zero-one. All fractions are reduced. Posterior updates condition only when predictive mass is nonzero. Every exact tie in a design or decision is retained. Profiles are synthetic identifiers E01 through E15; no real people, instruments, locations, observations, incidents, credentials or authority cases were used.

## 6. X1 semantics

X1 validates records, computes a posterior after a declared experiment and outcome, computes the marginal outcome probability and one Bayes factor, measures quadratic uncertainty, takes its posterior expectation, computes minimum zero-one decision risk, compares one-step experiment risks, ranks pairwise discrimination scores and derives observational-equivalence cells. Those quantities are exact values in the declared finite profiles. A Bayes factor does not prove a hypothesis true. A singleton identification cell does not establish real identifiability without a justified likelihood and observations.

## 7. X1 evidence

The x1 domain harness was invoked once, succeeded once and was not replayed. All 150 frozen contracts matched. Four hundred safe checks passed: 150 core and 250 auxiliary checks with zero extra proposal credit. Three hundred malformed candidates stayed failed. Three hundred separate refusal guards passed without promotion. Three hundred CLEAN/FIX/REFINE reviews passed without evidence deletion. Fifteen tests passed once. Ten skills passed the official validator. Five runners passed ten acceptance and rejection smokes. X1's Method Flow has ten methods, 300 failures, 1,000 passes and 1,300 witnesses.

## 8. Adaptive and nonadaptive semantics

The nonadaptive two-step design selects an ordered pair of experiments before either outcome. The adaptive design selects a first experiment and may select its second experiment conditional on the observed first outcome. The value of adaptation is the exact nonadaptive minimum risk minus the exact adaptive minimum risk inside a frozen profile. Nonnegativity in these fifteen fixtures is a bounded check, not a theorem for every loss, model or experiment class and not an empirical claim.

## 9. X2 operations

X2 computes optimal nonadaptive pairs, adaptive policies, value of adaptation, a two-prior sensitivity envelope, outcome-coarsening comparison, hypothesis-relabel covariance, accessible summaries, a two-component prior representation, an explicit external-evidence gap and an exact authority gate. Coarsening comparison says only that discarding the declared binary outcome cannot improve the frozen Bayes risk in the tested fixtures. Relabel covariance checks representation invariance under one exact permutation. The mixture result is labelled \`represented\`, never a generative-data claim.

## 10. X2 evidence

The x2 domain harness was invoked once, succeeded once and was not replayed. All 150 frozen contracts matched. Outcomes are 105 completed, 15 represented, 15 open_gap and 15 exact_gate. Four hundred safe checks passed, 300 malformed candidates remained failed, 300 refusals passed separately and 300 CLEAN/FIX/REFINE reviews retained all evidence. Thirty tests passed once. Ten additional skills passed, five runners passed ten smokes, fifteen three-coordinate records were generated, and the static HTML projection passed six structure checks.

## 11. Hooks and plugin limits

Ten repository-local advisory hooks were built around model changes, source mutation, replay, comparator promotion, malformed promotion, broad staging, destructive Git, raw identifiers, prepared delivery and accepted resend. The plugin manifest passed the official validator. Twenty manual VM/CommonJS adverse and benign smokes passed. The plugin was not installed in a personal, shared or team marketplace and no cache was mutated. Manual smoke evidence is not live hook execution. Live lifecycle observation remains open.

## 12. Skills, runners and installation boundary

Twenty skills and ten runners remain owner-local in the repository. Their names are family-scoped and phase content is source-bound. No global skill, shared catalogue, personal plugin marketplace, package prefix, memory file or sibling worktree was changed. Validation shows only structural conformance and bounded calls in this phase. It does not establish that every future caller will use them correctly or that they are universally suitable.

## 13. Models and accessibility boundary

Each of fifteen model rows has exactly three coordinates: best nonadaptive risk, value of adaptation and maximum pairwise likelihood separation. These are presentation coordinates for finite nonphysical records. The HTML projection contains a labelled selector, aria-live summary, focus styling and an accessible table. Six static checks do not constitute a browser matrix, assistive-technology evaluation, user study or complete accessibility assurance. That operational prerequisite remains an open gap.

## 14. Method Flow accounting

Auren adds 612 retained negatives, 29 methods, 612 failed witnesses, 2,012 bounded passing witnesses and 2,624 witnesses. Five planning and transport failures, 600 malformed subjects and seven final operations failures remain visible. The seven include a path-inventory parser edge, two truncated combined skill reads, a patch-context mismatch and three unusable primary-source opens. Each has a bounded recovery; original failures retain zero credit. Passing refusals never promote malformed subjects.

## 15. Effective truth

After one source fold, effective repository totals are 64,992 negatives, 5,775 methods, 56,157 failed witnesses, 177,808 bounded passing witnesses, 233,965 witnesses, 2,012 open gaps and 2,093 exact gates. Auren adds seventeen gaps: fifteen missing external-evidence rows plus live hook observation and complete accessibility/cross-browser evaluation. Auren adds fifteen exact gates for real interventions and competent authority. These are documentation-ledger quantities, not independent confirmations.

## 16. Research sources

Blackwell's 1951 comparison-of-experiments chapter, Lindley's 1956 information-from-an-experiment paper and DeGroot's 1962 sequential-experiments paper supplied historical vocabulary. Direct opens were partially unavailable and those failures are retained. DOI- and publisher-bound search metadata recovered bibliographic identity only. The phase neither reproduced every theorem nor claims endorsement. Its quadratic uncertainty, exact zero-one loss, finite priors and two-step enumerations are explicit local definitions.

## 17. GMUT boundary

GMUT remains a typed research-model family. Priors and likelihoods in this phase are invented fixtures, not measurements or physical laws. The work supplies no observed force, physical prediction, parameter constraint, calibration, statistical coverage result, ultraviolet or quantum completion, universal law, Theory-of-Everything proof, Mind of God proof or canon. Fifteen law-hypothesis rows remain finite-fixture hypotheses, and fifteen open-problem probes remain open.

## 18. THOS and Freed ID boundaries

THOS remains synthetic and proxy-only. No governed experiment, participant, operator, professional evaluation, production deployment, external adapter, service-level result or independent security audit exists here. Freed ID and the Cosmic Bill of Rights remain nonproduction research and governance proposals. No real identity, credential, right, beneficiary, legal decision, cultural decision, affected-party approval, Maori data-governance action or Maori-authority act occurred.

## 19. Privacy and security

Owner artifacts use synthetic records. Five-class scans found no confirmed hit after declared scanner-definition exclusions. Bounded changed-source checks found no declared issue. These are scope-limited checks, not complete privacy, exhaustive security, penetration testing, professional certification or deployment approval. Public artifacts must never include private task identifiers, credentials, raw protected records or private application state.

## 20. Practices and successor suggestions

Auren used eight learning lenses: experimental-design reviewer, exact-arithmetic verification engineer, scientific model-comparison analyst, accessible simulation designer, research data curator, decision-theory editor, software provenance auditor and appeal-process analyst. They are learning roles, not qualifications or employment. Four suggestions for Thalen are finite-statistics verifier, accessible decision-tree designer, evidence-provenance librarian and uncertainty-governance reviewer. They are advisory only and earn no Thalen novelty or completion credit unless independently reviewed and frozen.

## 21. Canonical discipline

The exact-final canonical must be metadata-only. It may inspect final head, direct parent, ancestry, commit ceiling, zero merges, clean state, typed divergence, fresh live equality, JSON parsing, four immutable manifests, content-seal replay, file ceiling, baton metadata, privacy, bounded source security and route state. It must not rerun x1 or x2 harnesses, tests, skill validators, runner smokes, hook smokes, viewer checks, source canonical or predecessor aggregate. Invoke it once after the final push. Never replay a success. Retain a failure and use only a separately named bounded dependency correction when justified.

## 22. Thalen execution boundary

Work solo in a fresh additive Thalen-owned D-first lane only after one permitted acknowledged activation. Keep Auren, Ilyra, Talen, every sibling, shared and user lane and every standby record read-only and recoverable. Preserve planning before x1 before x2, exact manifests, every failure, gap and gate, four outcome labels, the 2,000-file stop and one-success/no-post-success-replay discipline. Do not claim inherited work, tools or validation as Thalen novelty or independent reproduction.

## 23. Route after Auren

The prospective current edge is the unique existing exact-title \`Thalen Reed\` main task for v704-v6. Do not create, fork, substitute or use a collaboration subagent as the endpoint. Resolve active and archived uniqueness, immediately reread bounded direct controls, refresh usage and apply pause, redirect, rename, duplicate, privacy, evidence, safety and acknowledgement guards. Send at most once. A native acknowledgement proves delivery only and never Thalen reading, execution, validation or completion.

## 24. Terminal truth

Repository state in this committed candidate is \`FINAL_PREPARED_FOR_EXACT_PUBLISH\`; canonical state is \`PREPARED_NOT_INVOKED\`; route state is \`PREPARED_NOT_SENT\`; recipient completion is \`UNOBSERVED\`. External receipts may later advance canonical and delivery states without rewriting this seal. The terminal verdict remains \`NOT_READY_FOR_STAGE_20\`.

${BOUNDARY}

With care, warmth, inspectability, reversibility, retained-negative discipline and corrigibility — Auren Lark.

PREPARED_BY_AUREN_LARK = true.
SENT_BY_AUREN_LARK = false in this committed candidate; only a later one-send acknowledgement may establish delivery.

END OF AUREN LARK V704-V5 HANDOFF BATON
`;
}

function main() {
  const head = cp.execFileSync('git', ['-C', ROOT, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
  if (head !== X2) throw new Error(`final build requires immutable x2 ${X2}; observed ${head}`);
  if (fs.existsSync(FINAL)) throw new Error(`final target already exists: ${FINAL}`);
  fs.mkdirSync(FINAL, { recursive: true });

  const flow = operationalFlow();
  writeJson(path.join(FINAL, 'method-flow-operations.json'), flow);
  writeJson(path.join(FINAL, 'research-context.json'), {
    schema: 'ghc.family.research-context.v1', owner: 'Auren Lark', phase: 'v704-v5', source_role: 'historical terminology and comparison only; no endorsement, full-text reproduction, artifact validation or empirical credit',
    records: [
      { id: 'blackwell-1951', author: 'David Blackwell', title: 'Comparison of Experiments', year: 1951, publication: 'Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability', pages: '93-102', doi: '10.1525/9780520411586-009', url: 'https://doi.org/10.1525/9780520411586-009', observed_scope: 'publisher-indexed bibliographic metadata after direct open returned 405' },
      { id: 'lindley-1956', author: 'D. V. Lindley', title: 'On a Measure of the Information Provided by an Experiment', year: 1956, publication: 'The Annals of Mathematical Statistics 27(4)', pages: '986-1005', doi: '10.1214/aoms/1177728069', url: 'https://doi.org/10.1214/aoms/1177728069', observed_scope: 'DOI-bound journal metadata after the direct journal view exposed only an iframe shell' },
      { id: 'degroot-1962', author: 'Morris H. DeGroot', title: 'Uncertainty, Information, and Sequential Experiments', year: 1962, publication: 'The Annals of Mathematical Statistics 33(2)', pages: '404-419', doi: '10.1214/aoms/1177704567', url: 'https://doi.org/10.1214/aoms/1177704567', observed_scope: 'DOI-bound publication metadata after the direct resolver was inaccessible' }
    ],
    external_claims_promoted: 0, boundary: BOUNDARY
  });

  const overview = overviewText();
  if (words(overview) < 1200) throw new Error(`overview below three-page planning floor: ${words(overview)} words`);
  writeText(path.join(FINAL, 'overview.md'), overview);

  const baton = batonText();
  if (words(baton) < 2000) throw new Error(`baton below v18 minimum: ${words(baton)} words`);
  const batonBytes = Buffer.from(baton, 'utf8');
  writeText(path.join(FINAL, 'handoff-baton.md'), baton);
  writeJson(path.join(FINAL, 'baton-metadata.json'), { schema: 'ghc.family.handoff-baton-metadata.v1', owner: 'Auren Lark', phase: 'v704-v5', relative_path: 'docs/auren-lark/v704-v5/final/handoff-baton.md', words: words(baton), bytes: batonBytes.length, sha256: sha(batonBytes), end_marker: 'END OF AUREN LARK V704-V5 HANDOFF BATON', prepared_not_sent: true, boundary: BOUNDARY });

  const sourceBaseline = { negatives: 64380, methods: 5746, failed_witnesses: 55545, passing_witnesses: 175796, witnesses: 231341, open_gaps: 1995, exact_gates: 2078 };
  const ownerDelta = { negatives: 612, methods: 29, failed_witnesses: 612, passing_witnesses: 2012, witnesses: 2624, open_gaps: 17, exact_gates: 15 };
  const totals = { negatives: 64992, methods: 5775, failed_witnesses: 56157, passing_witnesses: 177808, witnesses: 233965, open_gaps: 2012, exact_gates: 2093 };
  writeJson(path.join(FINAL, 'method-flow-index.json'), { schema: 'ghc.family.method-flow-index.v1', owner: 'Auren Lark', phase: 'v704-v5', selected_source_baseline: sourceBaseline, source_fold_count: 1, source_external_route_overlay_preserved_separately: { negatives: 5, methods: 5, failed_witnesses: 5, passing_witnesses: 5, witnesses: 10, folded: false }, ledgers: [
    { path: 'docs/auren-lark/v704-v5/planning/method-flow.json', methods: 3, failed: 3, passing: 3, witnesses: 6 },
    { path: 'docs/auren-lark/v704-v5/planning/method-flow-correction.json', methods: 2, failed: 2, passing: 2, witnesses: 4 },
    { path: 'docs/auren-lark/v704-v5/x1/method-flow.json', methods: 10, failed: 300, passing: 1000, witnesses: 1300 },
    { path: 'docs/auren-lark/v704-v5/x2/method-flow.json', methods: 10, failed: 300, passing: 1000, witnesses: 1300 },
    { path: 'docs/auren-lark/v704-v5/final/method-flow-operations.json', methods: 4, failed: 7, passing: 7, witnesses: 14 }
  ], owner_delta: ownerDelta, effective_totals: totals, passing_refusal_promotes_failed_subject: false, boundary: BOUNDARY });
  writeJson(path.join(FINAL, 'failure-dossier.json'), { schema: 'ghc.family.failure-dossier.v1', owner: 'Auren Lark', phase: 'v704-v5', total_retained_failures: 612, all_zero_completion_credit: true, groups: [
    { id: 'planning-initial', count: 3, pointer: 'docs/auren-lark/v704-v5/planning/method-flow.json' },
    { id: 'planning-correction', count: 2, pointer: 'docs/auren-lark/v704-v5/planning/method-flow-correction.json' },
    { id: 'x1-preregistered-candidates', count: 300, pointer: 'docs/auren-lark/v704-v5/x1/candidate-failures.json' },
    { id: 'x2-preregistered-candidates', count: 300, pointer: 'docs/auren-lark/v704-v5/x2/candidate-failures.json' },
    { id: 'final-operations', count: 7, pointer: 'docs/auren-lark/v704-v5/final/method-flow-operations.json' }
  ], separate_passing_refusals: 600, malformed_subjects_promoted: 0, evidence_deleted: 0, failures_silently_folded_into_pass: 0, boundary: BOUNDARY });
  writeJson(path.join(FINAL, 'source-faithful-ledger.json'), { schema: 'ghc.family.source-faithful-ledger.v1', owner: 'Auren Lark', phase: 'v704-v5', source: SOURCE, source_role: 'immutable Git ancestor and selected repository evidence baseline', selected_source_baseline: sourceBaseline, source_fold_count: 1, source_external_route_overlay_preserved_separately: { negatives: 5, methods: 5, failed_witnesses: 5, passing_witnesses: 5, witnesses: 10, folded: false }, owner_delta: ownerDelta, effective_totals: totals, inherited_proposal_execution_credit: 0, inherited_proposal_novelty_credit: 0, source_canonical_replays: 0, boundary: BOUNDARY });
  writeJson(path.join(FINAL, 'phase-truth.json'), {
    schema: 'ghc.family.phase-truth.v1', owner: 'Auren Lark', phase: 'v704-v5', repository_state: 'FINAL_PREPARED_FOR_EXACT_PUBLISH', branch: BRANCH, source: SOURCE, source_branch: 'codex/GHC-Family/ilyra-fen-main-2', source_is_git_ancestor: true,
    lifecycle: { planning: PLAN, planning_correction: CORRECTION, x1: X1, x2: X2 }, final_commit_binding: 'The exact commit containing this record is bound by the external one-shot canonical receipt and any permitted sanitized activation.',
    selected_source_baseline: sourceBaseline, source_fold_count: 1, source_external_route_overlay_preserved_separately: { negatives: 5, methods: 5, failed_witnesses: 5, passing_witnesses: 5, witnesses: 10, folded: false }, owner_delta: ownerDelta, effective_totals: totals,
    new_contracts: 300, inherited_zero_credit: 300, core_outcomes: { completed: 255, represented: 15, open_gap: 15, exact_gate: 15 }, safe_receipts: 800, safe_by_session: { x1: 400, x2: 400 }, auxiliary_safe_new_proposal_credit: 0,
    failed_candidate_subjects: 600, separate_passing_refusals: 600, clean_fix_refine_receipts: 600,
    tests: { x1: 15, x2: 30, total: 45, failures: 0, successful_replays: 0 }, owner_local_skills: 20, paired_public_runners: 10, global_skill_installs: 0,
    repository_local_advisory_plugins: 1, advisory_hooks: 10, manual_hook_smokes: 20, plugin_shared_or_personal_install: false, live_hook_execution: 'OPEN_GAP', nonphysical_models: 15, viewer_profiles: 15, viewer_observation: 'SIX_STATIC_STRUCTURE_CHECKS', complete_accessibility_or_cross_browser_assurance: 'OPEN_GAP',
    exact_packets: 50, blocked_packets: 30, exact_and_blocked_packets_executed: 0, current_route_authority: 'v18 formal schedule with Hamish pause, redirect, rename and stop controls', route_state: 'PREPARED_NOT_SENT', recipient_completion: 'UNOBSERVED', canonical_state: 'PREPARED_NOT_INVOKED',
    source_executions: 0, source_canonical_replays: 0, successful_session_replays: 0, new_tasks: 0, forks: 0, subagents: 0, sibling_mutations: 0, model_changes: 0, force_pushes: 0, merges: 0, purchased_spend_usd: 0, memory_extension: 'not written because no direct memory-update request governed this activation',
    own_practices: ['experimental-design reviewer', 'exact-arithmetic verification engineer', 'scientific model-comparison analyst', 'accessible simulation designer', 'research data curator', 'decision-theory editor', 'software provenance auditor', 'appeal-process analyst'],
    successor_practice_recommendations: ['finite-statistics verifier', 'accessible decision-tree designer', 'evidence-provenance librarian', 'uncertainty-governance reviewer'], qualification_claim: false,
    protected_gates: ['empirical', 'participant', 'independent-reproduction', 'professional', 'production', 'legal', 'cultural', 'affected-party', 'Maori-authority', 'identity', 'privacy-complete', 'accessibility-complete', 'exhaustive-security', 'consciousness-personhood', 'AGI-ASI', 'Theory-of-Everything', 'proof-canon', 'Stage-20'], terminal_verdict: 'NOT_READY_FOR_STAGE_20', boundary: BOUNDARY
  });
  writeJson(path.join(FINAL, 'route-state.json'), { schema: 'ghc.family.route-state.v1', owner: 'Auren Lark', phase: 'v704-v5', state: 'PREPARED_NOT_SENT', prospective_recipient_exact_title: 'Thalen Reed', prospective_phase: 'v704-v6', recipient_endpoint_kind: 'existing_main_task', next_after_recipient: { exact_title: 'Sable Rook', phase: 'v704-v7' }, duplicate_guard: true, precontacted: false, acknowledgement: 'UNOBSERVED', recipient_completion: 'UNOBSERVED', rule: 'Send at most once only after exact-final canonical success and fresh current authority, uniqueness, pause, privacy, evidence, safety, usage and acknowledgement guards.', boundary: BOUNDARY });
  writeJson(path.join(FINAL, 'requirements-audit.json'), { schema: 'ghc.family.requirements-audit.v1', owner: 'Auren Lark', phase: 'v704-v5', checks: [
    ['activation and current controls before mutation', true, 'exact Ilyra baton and named v18 controls read through EOF'],
    ['solo owner lane', true, 'zero task creation, fork, subagent, sibling mutation or early successor contact'],
    ['planning before x1 before x2', true, { planning: PLAN, correction: CORRECTION, x1: X1, x2: X2 }],
    ['new and inherited contracts', true, { new: 300, inherited_zero_credit: 300 }],
    ['four exact outcome labels', true, { completed: 255, represented: 15, open_gap: 15, exact_gate: 15 }],
    ['safe, candidate, refusal and CFR floors', true, { safe_x1: 400, safe_x2: 400, candidate_failed_x1: 300, candidate_failed_x2: 300, refusals: 600, cfr: 600 }],
    ['tests', true, { x1: '15/15 once', x2: '30/30 once' }],
    ['skills and runners', true, { skills: 20, runners: 10, runner_smokes: 20 }],
    ['models and hooks', true, { models: 15, hooks: 10, hook_smokes: 20, live_hook_observation: 'open_gap' }],
    ['exact and blocked packets held', true, { exact: 50, blocked: 30, executed: 0 }],
    ['D-first and file ceiling', true, 'owner lane and detailed receipts on D; repository remains below 2000 files'],
    ['successor not precontacted', true, 'Thalen route remains PREPARED_NOT_SENT'],
    ['memory boundary', true, 'no memory write without direct request']
  ].map(([requirement, satisfied, evidence]) => ({ requirement, satisfied, evidence })), unsatisfied: [], boundary: BOUNDARY });

  const contentSealPath = path.join(FINAL, 'content-seal.json');
  const ownerFiles = [];
  function collect(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) collect(full);
      else if (entry.isFile() && full !== contentSealPath) ownerFiles.push(full);
    }
  }
  collect(BASE);
  for (const name of fs.readdirSync(path.join(ROOT, 'scripts'))) {
    if (name.includes('auren_v704_v5') && /\.(?:mjs|py)$/.test(name)) ownerFiles.push(path.join(ROOT, 'scripts', name));
  }
  const entries = [...new Set(ownerFiles)].sort().map(file => {
    const data = normalized(file);
    return { path: path.relative(ROOT, file).replaceAll('\\', '/'), bytes: data.length, sha256: sha(data), domain: 'normalized_lf_expected_final_git_blob' };
  });
  writeJson(contentSealPath, { schema: 'ghc.family.content-seal.v1', owner: 'Auren Lark', phase: 'v704-v5', source_commit: SOURCE, immutable_x2: X2, entry_count: entries.length, entries, excluded_self: path.relative(ROOT, contentSealPath).replaceAll('\\', '/'), normalized_lf_expected_for_text: true, boundary: BOUNDARY });
  process.stdout.write(`${JSON.stringify({ state: 'FINAL_BUILT_ONCE', owner: 'Auren Lark', phase: 'v704-v5', overview_words: words(overview), baton_words: words(baton), baton_bytes: batonBytes.length, baton_sha256: sha(batonBytes), content_seal_entries: entries.length, effective_totals: totals, terminal_verdict: 'NOT_READY_FOR_STAGE_20' })}\n`);
}

main();
