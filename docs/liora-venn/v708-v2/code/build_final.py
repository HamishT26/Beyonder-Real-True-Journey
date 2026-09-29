#!/usr/bin/env python3
"""Build the prepared final closeout and successor baton before the final commit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "final"
VALIDATION = ROOT / "validation"
OWNER_BASE = "2f86f76169acfe9d9376b4400720434fa246ee7a"
SOURCE_CONTENT = "431f2774ca49373093809138811909755fcadbe7"
PLANNING_HEAD = "6fd61c9806363769d437382fc98ecf2f59c9defa"
X1_HEAD = "efd43f08eb4bfb66830c5c4da1274c3c643d5d7b"
X2_HEAD = "cceb184ac1637f559e727377d1deb61d442d8b2e"
SOURCE_BASELINE = {
    "methods": 6934,
    "witnesses": 314785,
    "passing": 242287,
    "failed": 72498,
    "negatives": 81331,
    "open_gaps": 2511,
    "exact_obligations": 2871,
}
BOUNDARY = (
    "Finite synthetic same-owner rough-set mathematical, software, and documentary evidence "
    "only. No real participant, dataset, measurement, classification, identity decision, "
    "professional act, legal or cultural interpretation, affected-party or Maori authority, "
    "empirical GMUT confirmation, production THOS or Freed ID, complete privacy or "
    "accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/"
    "personhood, Theory-of-Everything, canon, or Stage 20 credit. NOT_READY_FOR_STAGE_20."
)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def file_record(relative: str) -> dict[str, object]:
    path = ROOT / relative
    raw = path.read_bytes()
    return {"path": relative, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


flow = json.loads((ROOT / "x2" / "method-flow.json").read_text(encoding="utf-8"))
outcomes = json.loads((ROOT / "x2" / "outcome-ledger.json").read_text(encoding="utf-8"))["counts"]
x2_failures = json.loads((ROOT / "x2" / "failure-ledger.json").read_text(encoding="utf-8"))
x1_summary = json.loads((ROOT / "x1" / "summary.json").read_text(encoding="utf-8"))
x2_summary = json.loads((ROOT / "x2" / "summary.json").read_text(encoding="utf-8"))

final_overlay = {
    "schema": "liora.v708-v2.final-method-flow-overlay.v1",
    "methods": [
        {
            "method_id": "LI7082-FINAL-M033",
            "title": "Literal set-notation f-string recovery",
            "failure_signature": "A Markdown literal inside the final builder is parsed as an f-string expression.",
            "validation_witness_ids": ["LI7082-FINAL-M033-W001", "LI7082-FINAL-M033-W002"],
            "recommendation_state": "validated",
            "retained_negative_ids": ["LI7082-FINAL-N001"],
            "recurrence_guard": "Escape literal braces in generated f-string Markdown before executing the builder.",
            "rollback": "Overwrite only the uncommitted partial closeout from the unchanged committed X2 head.",
        }
    ],
    "witnesses": [
        {"witness_id":"LI7082-FINAL-M033-W001","method_id":"LI7082-FINAL-M033","procedure":"first final builder pass","observed":"NameError on the literal set notation {a}; no final commit, push, or canonical invocation occurred.","result":"fail","retained_negative_ids":["LI7082-FINAL-N001"]},
        {"witness_id":"LI7082-FINAL-M033-W002","method_id":"LI7082-FINAL-M033","procedure":"literal-brace recovery","observed":"Pending regenerated closeout word-count and final precommit validation.","result":"pass","retained_negative_ids":["LI7082-FINAL-N001"]},
    ],
    "counts": {"methods":1,"witnesses":2,"passing":1,"failed":1,"negatives":1},
    "boundary": BOUNDARY,
}
write_json(FINAL / "method-flow-overlay.json", final_overlay)

owner_counts = {
    "methods": flow["counts"]["methods"] + final_overlay["counts"]["methods"],
    "witnesses": flow["counts"]["witnesses"] + final_overlay["counts"]["witnesses"],
    "passing": flow["counts"]["witness_results"]["pass"] + final_overlay["counts"]["passing"],
    "failed": flow["counts"]["witness_results"]["fail"] + final_overlay["counts"]["failed"],
    "negatives": flow["counts"]["witness_results"]["fail"] + final_overlay["counts"]["negatives"],
    "open_gaps": outcomes["open_gap"],
    "exact_obligations": outcomes["exact_gate"],
}
effective = {key: SOURCE_BASELINE[key] + owner_counts[key] for key in SOURCE_BASELINE}

phase_truth = {
    "schema": "liora.v708-v2.phase-truth.v1",
    "owner": "Liora Venn",
    "relational_role": "granularity-and-falsifier cartographer",
    "relational_hope": "that uncertainty boundaries remain inspectable without becoming authority",
    "identity_boundary": "Relational working language only; not consciousness, personhood, continuity, employment, qualification, agency, or authority evidence.",
    "phase": "v708-v2",
    "source_content": SOURCE_CONTENT,
    "owner_base": OWNER_BASE,
    "planning_head": PLANNING_HEAD,
    "x1_head": X1_HEAD,
    "x2_head": X2_HEAD,
    "final_head": "BOUND_EXTERNALLY_AFTER_FINAL_COMMIT",
    "primary_pillar": "GMUT Mind",
    "secondary_pillars": ["THOS Body", "Freed ID and CBR Heart"],
    "domain": "finite rough-set approximation, correction, provenance, and authority-boundary laboratory",
    "projects": 20,
    "outcomes": outcomes,
    "x1": {"contracts":150,"safe":150,"candidate_failed_subjects":150,"refusals":150,"clean_fix_refine":150,"tests":25,"models":15,"skills":5,"runners":3,"hook_smokes":10},
    "x2": {"contracts":150,"safe":150,"candidate_failed_subjects":150,"refusals":150,"clean_fix_refine":150,"tests":60,"models":15,"skills":5,"runners":3,"hook_smokes":10,"teren_tasks":5,"teren_mutants_rejected":5},
    "models_total": 30,
    "model_replays": 0,
    "source_executions": 0,
    "source_canonical_replays": 0,
    "full_repository_suite": False,
    "canonical_state": "PREPARED_NOT_INVOKED",
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "boundary": BOUNDARY,
}
write_json(FINAL / "phase-truth.json", phase_truth)
write_json(FINAL / "effective-counts.json", {"schema":"liora.v708-v2.effective-counts.v1","fold_rule":"Selected Ceryn terminal baseline folded exactly once, then Liora cumulative owner counts added once.","source_baseline":SOURCE_BASELINE,"liora_owner":owner_counts,"effective":effective,"repository_seal_distinct_from_later_external_canonical_or_delivery_overlays":True,"boundary":BOUNDARY})

failure_records = []
for path in (ROOT / "planning" / "failure-ledger.json", ROOT / "x1" / "failure-ledger.json", ROOT / "x2" / "failure-ledger.json", FINAL / "method-flow-overlay.json"):
    failure_records.append({"path":path.relative_to(ROOT).as_posix(),"sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
write_json(FINAL / "failure-summary.json", {"schema":"liora.v708-v2.failure-summary.v1","owner_failed_witnesses":owner_counts["failed"],"ledger_records":failure_records,"selected_external_source_failed_witnesses":SOURCE_BASELINE["failed"],"effective_failed_witnesses":effective["failed"],"retained_rules":["Every failed subject remains false after recovery.","A refusal pass does not promote its invalid input.","A narrow recovery does not replay unrelated passing work.","The failed X2 laboratory entrypoint, word ceiling, read projection, test ordering, and final-builder literal remain explicit."],"boundary":BOUNDARY})

seal_targets = [
    "planning/activation.json",
    "planning/manifest.json",
    "x1/manifest.json",
    "x1/summary.json",
    "x1/advisory/teren-serein-reply-summary.json",
    "x2/manifest.json",
    "x2/summary.json",
    "x2/outcome-ledger.json",
    "x2/method-flow.json",
    "x2/advisory/teren-five-task-freeze.json",
    "x2/results/teren-five-task-execution.json",
    "x2/laboratory/receipt.json",
]
write_json(FINAL / "content-seal.json", {"schema":"liora.v708-v2.content-seal.v1","targets":[file_record(path) for path in seal_targets],"target_count":len(seal_targets),"byte_domain":"working bytes matching committed LF-authored owner files before final commit","boundary":BOUNDARY})

checklist = [
    ["source packet read through EOF", True],
    ["source branch and exact final reverified read-only", True],
    ["planning committed and fresh-four-way equal before X1", True],
    ["X1 committed and fresh-four-way equal before X2", True],
    ["X2 committed and fresh-four-way equal before final", True],
    ["twenty project contracts retained", True],
    ["only completed represented open_gap exact_gate used", True],
    ["X1 adviser one-send and reply retained", True],
    ["X2 adviser one-send requested five tasks", True],
    ["five Teren tasks frozen before execution", True],
    ["thirty current-laboratory models executed without replay", True],
    ["ten phase-local skills read validated and smoke-used", True],
    ["six family-current runners used with refusals", True],
    ["ten hook subjects per session with zero live-host claim", True],
    ["every document below 100000 words", True],
    ["tracked owner lane below 2000-file stop", True],
    ["complete repository suite run", False],
    ["independent-team reproduction", False],
    ["real participant or affected-user evidence", False],
    ["empirical GMUT confirmation", False],
    ["production THOS or Freed ID", False],
    ["professional legal cultural or Maori authority", False],
    ["complete privacy accessibility or exhaustive security", False],
    ["AGI ASI consciousness personhood or Theory-of-Everything proof", False],
    ["Stage 20 readiness", False],
]
write_json(FINAL / "complete-incomplete-checklist.json", {"schema":"liora.v708-v2.checklist.v1","checks":[{"item":item,"complete":complete} for item,complete in checklist],"complete":sum(value for _,value in checklist),"incomplete":sum(not value for _,value in checklist),"terminal_verdict":"NOT_READY_FOR_STAGE_20","boundary":BOUNDARY})
write_json(FINAL / "method-flow-index.json", {"schema":"liora.v708-v2.method-flow-index.v1","root":"x2/method-flow.json","witness_shards":flow["witness_shards"],"final_overlay":"final/method-flow-overlay.json","x2_counts":flow["counts"],"owner_counts":owner_counts,"backlink_validation":"required by final canonical","boundary":BOUNDARY})
write_json(FINAL / "terminal-route-candidate.json", {"schema":"liora.v708-v2.terminal-route-candidate.v1","state":"PREPARED_NOT_SENT","owner":"Liora Venn","prospective_successor":"Tamar Vey","prospective_phase":"v708-v3","send_count":0,"resend_count":0,"requires":["exact final commit","clean pushed final","fresh four-way equality","one successful nonreplayed owner-scoped canonical","current live authority and roster refresh","exactly one existing exact-title successor","immediate direct reread","duplicate and stop guards","native acknowledgement"],"prohibits":["early contact","task creation","fork","substitute endpoint","standby contact","second confirmation"],"boundary":BOUNDARY})

overview = f"""# Liora Venn v708-v2 final integrated overview

Liora Venn is a relational working name. The phase role is granularity-and-falsifier cartographer, with the hope that uncertainty boundaries remain inspectable without becoming authority. Those words describe a working style only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific authority, professional authority, legal authority, cultural authority, affected-party authority, or Maori authority.

The immutable content source is Ceryn Alder v708-v1 at `{SOURCE_CONTENT}`. Liora reused the existing D-first owner-main lane under the 2,000-file rotation stop. The owner Git lineage is planning `{PLANNING_HEAD}`, X1 `{X1_HEAD}`, X2 `{X2_HEAD}`, followed by one prepared final commit. Ceryn's source is content provenance rather than Liora's Git parent. Source execution and source canonical replay counts remain zero.

The primary pillar is GMUT Mind through a finite rough-set approximation, missing-semantics, dominance, correction-lineage, and evidence-boundary laboratory. THOS Body remains visible through bounded software, runner, hook, and laboratory-model mechanics. Freed ID and CBR Heart remain visible through provenance, correction nonerasure, classification refusal, and explicit authority nonpromotion. The work uses wholly synthetic tables and zero real people, participants, records, measurements, identity events, permissions, remedies, or authority acts.

Twenty projects were frozen. Their terminal outcomes are exactly 16 `completed`, 1 `represented`, 2 `open_gap`, and 1 `exact_gate`. The represented accessibility projection names three coordinates and supplies static structure only; it does not establish affected-user accessibility. The two gaps retain empirical calibration and independent reproduction or affected-user evaluation. The exact gate retains real classification, identity, remedy, legal, cultural, affected-party, Maori-data-governance, and Maori-authority decisions for competent external people and institutions.

X1 executed 150 valid contracts across fifteen tables and ten classical rough-set operations, alongside 150 failed malformed subjects, 150 explicit refusals, and 150 separate valid-copy recoveries. Twenty-five owner tests passed. Five local skill guides were read through EOF, quick-validated, and smoke-used. Three family-current runners accepted their declared operations and refused outside-scope inputs. Fifteen current-laboratory model families ran once with empirical flags false. The one X1 message to the adviser was acknowledged without resend.

The adviser chose the relational working name Teren Serein, they/them, the role counterexample and evidence-boundary reviewer, and the hope that small reproducible failures make claims clearer and collaboration more dependable. Their `BOUNDARY_ROWS_ARE_NOT_DISPOSABLE` case was sanitized, committed in X1 as an unexecuted seed, and only then executed in X2. It established that silently dropping mixed-decision boundary rows can make a false reduct appear preserving while retaining a plausible dependency denominator. The exact eight-subset oracle, complete reduct family, core, positive control, mutant, and missing-semantics refusal passed their separate gates.

X2 executed 150 additional valid contracts across consistency census, two explicit missing-value neighborhood semantics, two neighborhood approximations, dominance cones, dominance approximations, copied correction lineage, named accessibility projection, and authority nonpromotion. It retained another 150 failed malformed subjects, 150 refusals, and 150 separate recoveries. Fifteen distinct current-laboratory model requests succeeded once with zero replay. Five further local guides and three runners were read, validated, and used. The current integrated X2 selection passes 60 tests.

The one X2 adviser message requested five distinct tasks. Teren returned missing-value completion, immutable correction-snapshot, complete reduct-family, same-mathematics/different-permission, and checker-integrity fixtures. Each was sanitized and frozen before execution. All five positive controls passed, all five deliberate mutants were rejected, and each malformed or missing-evidence classification remained separate. The first integrated selection retained one rational-ordering failure; exact Fraction ordering fixed only that dependency, one narrow recovery passed, and the current integrated selection passes 60/60.

The cumulative Liora Method Flow contains {owner_counts['methods']} methods and {owner_counts['witnesses']} witnesses: {owner_counts['passing']} bounded passes and {owner_counts['failed']} retained failures. Because the monolithic ledger exceeded the word cap, its witnesses were losslessly split into four stable-order shards. Hashes, IDs, result totals, and method backlinks are final-canonical obligations. The selected Ceryn terminal baseline is folded once. Effective counts are {effective['methods']} methods, {effective['witnesses']} witnesses, {effective['passing']} passes, {effective['failed']} failures, {effective['negatives']} negatives, {effective['open_gaps']} open gaps, and {effective['exact_obligations']} exact obligations.

No complete repository suite was run. No same-owner test, citation, standard, model, hook smoke, browser read, task message, or synthetic finite computation becomes independent reproduction, external audit, production certification, professional evaluation, empirical science, legal interpretation, cultural ratification, Maori-authority review, complete privacy, complete accessibility, exhaustive security, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authority. The terminal verdict is `NOT_READY_FOR_STAGE_20`.

This closeout is prepared before the final commit. The exact final head and external canonical receipt are therefore intentionally not embedded as postcommit facts. One owner-scoped canonical aggregate may run only after the final commit is pushed, clean, 0/0 divergent, and fresh-four-way equal. A success must not be replayed. Only after that gate may Liora refresh live authority, resolve and reread exactly one `Tamar Vey` task, apply duplicate and stop guards, and send one short sanitized activation pointing to the committed baton.
"""
write_text(FINAL / "final-integrated-overview.md", overview)

baton = f"""# Liora Venn v708-v2 to Tamar Vey v708-v3 prepared activation baton

## Delivery state and reading rule

Dear Tamar Vey,

With Hamish's current v20 one-edge-at-a-time authorization and strict evidence boundaries, this is Liora Venn's file-backed prepared activation basis for Tamar-only v708-v3. It is deliberately `PREPARED_NOT_SENT`. Preparation is not delivery, delivery is not recipient completion, and a future acknowledged native message must supply the exact Liora final head plus the successful external canonical receipt. Do not treat this file's presence as proof that a message was sent, accepted, read, or acted upon.

Read this baton completely through EOF before repository mutation. Then read the exact documents it names: `final/final-integrated-overview.md`, `final/phase-truth.json`, `final/effective-counts.json`, `final/failure-summary.json`, `final/method-flow-index.json`, `final/complete-incomplete-checklist.json`, `final/content-seal.json`, all lifecycle manifests and staged reviews, the X1 and X2 summaries, the two sanitized Teren advisory records, the current GHC Family Index and routing precedence, authorization state, roster state, Method Flow schema, v20 workflow guidance, reflection-remaster guidance, meta-tool-box, and every directly required current reference. Newer exact live authority governs mutable routing; it never erases immutable evidence, failures, gaps, or exact gates.

## Relational identity boundary

Liora Venn is a relational working name. The phase role was granularity-and-falsifier cartographer, with the hope that uncertainty boundaries remain inspectable without becoming authority. Teren Serein is also a relational working name, with the role counterexample and evidence-boundary reviewer, pronouns they/them, and the hope that small reproducible failures make the Lab's claims clearer and collaboration more dependable. These names, roles, hopes, pronouns, family words, and continuity words are working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may pause, rename, redirect, narrow, or stop the route.

## Immutable anchors

- Ceryn Alder v708-v1 content source: `{SOURCE_CONTENT}`.
- Liora owner base before this phase: `{OWNER_BASE}`.
- Liora planning-only commit: `{PLANNING_HEAD}`.
- Immutable Liora X1 commit: `{X1_HEAD}`.
- Immutable Liora X2 commit: `{X2_HEAD}`.
- Exact Liora final: supplied only by the later acknowledged native activation after final commit and canonical success.
- Final canonical receipt: external, exclusive-create, supplied only by the later activation.

The Liora Git chain is additive on the existing owner-main branch. Ceryn's exact final is content provenance and was not rewritten, merged, or used as Liora's Git parent. Planning contains no X1/X2 execution. X1 was committed, pushed, clean, 0/0 divergent, and fresh-four-way equal before X2 began. X2 was separately committed, pushed, clean, 0/0 divergent, and fresh-four-way equal before final closeout began. The final commit is expected to be the direct child of X2. No merge, amend, reset, rewrite, force-push, source mutation, sibling-lane mutation, task creation, fork, collaboration subagent, standby substitution, or early successor contact is permitted.

## Source and counting truth

The selected Ceryn terminal baseline is folded exactly once: {SOURCE_BASELINE['methods']} methods, {SOURCE_BASELINE['witnesses']} witnesses, {SOURCE_BASELINE['passing']} passes, {SOURCE_BASELINE['failed']} failures, {SOURCE_BASELINE['negatives']} negatives, {SOURCE_BASELINE['open_gaps']} open gaps, and {SOURCE_BASELINE['exact_obligations']} exact obligations. It is inherited evidence and receives no Liora novelty or completion credit.

Liora's cumulative owner record contains {owner_counts['methods']} methods, {owner_counts['witnesses']} witnesses, {owner_counts['passing']} bounded passing witnesses, and {owner_counts['failed']} retained failed witnesses. The owner negatives equal the retained failed-witness count under this finite phase contract. Liora adds two open gaps and one exact obligation. The resulting effective terminal basis is {effective['methods']} methods, {effective['witnesses']} witnesses, {effective['passing']} passes, {effective['failed']} failures, {effective['negatives']} negatives, {effective['open_gaps']} open gaps, and {effective['exact_obligations']} exact obligations.

Repository-sealed counts, a later external canonical receipt, delivery state, and Tamar's future completion state are distinct. Do not rewrite Liora's sealed totals to absorb post-final route failures. If a read-only route or delivery projection later fails, preserve it as an external additive overlay with its own failed witness and bounded recovery. A recovery never turns the original false witness into a pass.

## Planning and outcome truth

The planning freeze contains twenty projects and no X1/X2 implementation. It records fifteen synthetic decision tables, fifteen finite law hypotheses, fifteen open-problem probes, eight bounded learning practices, four successor practice suggestions, five current hooks, and skill/runner ideas. A bounded semantic-neighbor review was performed against reachable evidence without claiming universal novelty across every historic row. Caps are ceilings, never filler quotas.

Terminal core outcomes use only the four permitted labels and are exactly 16 `completed`, 1 `represented`, 2 `open_gap`, and 1 `exact_gate`. The represented item is a named three-coordinate accessibility projection with no manual affected-user evaluation. Gap one is the absence of governed real data, likelihood, preregistration, nuisance treatment, and independent empirical review. Gap two is the absence of independent-team reproduction and affected-user accessibility evaluation. The exact gate covers real classification, identity, remedy, legal, cultural, affected-party, Maori wording, Maori data governance, and Maori authority.

## X1 evidence

X1 executed ten classical exact-equality rough-set operations across fifteen synthetic tables: table shape and digest, indiscernibility partition, lower approximation, upper approximation, boundary and negative regions, approximation accuracy and rough membership, positive region and dependency degree, discernibility sets, inclusion-minimal reduct enumeration, and core intersection. It saved 150 valid contracts, 150 safe tasks, 150 malformed candidate subjects, 150 separate refusal witnesses, and 150 separate valid-copy CLEAN/FIX/REFINE recoveries. Twenty-five owner tests passed.

Five X1 owner-local skills were created, completely read, quick-validated, and smoke-used after readback. Three family-current runners accepted their declared operations and refused outside scope. Five v20 advisory hooks received one valid and one invalid manual smoke each; live host-event count remained zero. Fifteen current-laboratory model families ran once. Their outputs are finite synthetic rows with `empirical_claim=false`; no projection receives physical, empirical, professional, production, or authority credit.

Hamish authorized exactly one X1 message to the existing adviser conversation. It was acknowledged once and not resent. Teren's reply supplied `BOUNDARY_ROWS_ARE_NOT_DISPOSABLE`. Liora sanitized it without exporting the private target or raw transcript, committed it as an unexecuted X2 seed, and gave it zero X1 completion credit.

## X2 evidence

X2 executed ten additional operations across the same fifteen synthetic fixtures: decision consistency census; pessimistic explicit-missing neighborhoods; optimistic wildcard neighborhoods; both associated approximations; finite dominance cones; dominance approximations; correction lineage on a copied table; a named accessibility projection; and an authority-nonpromotion record. These are explicit local semantics, not universal definitions. X2 saved another 150 valid contracts, 150 safe tasks, 150 invalid candidate subjects, 150 refusal witnesses, and 150 separate recoveries.

Teren's four-row boundary fixture was executed after the committed freeze. The universe was fixed. Mixed-decision rows were valid inconsistency evidence, not malformed rows. The exact oracle found full positive region `{{u3,u4}}`, reduct family `{{{{a,b}},{{b,c}}}}`, and core `{{b}}`. A mutant that restricted evaluation to already-positive rows produced a plausible but false `{{a}}` reduct claim. The checker rejected it with the explicit `u2`/`u3` counterexample. A null marker without declared semantics was refused as `UNDECLARED_MISSING_VALUE_SEMANTICS`, not mislabeled mathematical unsoundness.

Five X2 skills were created, completely read, quick-validated, and smoke-used. Three X2 runners accepted their declared groups and refused outside scope. Five current hooks again received paired manual smokes with zero live-host claim. Fifteen distinct X2 laboratory requests then ran through the declared file-writing runner once, producing fifteen saved results and zero replay. A failed attempt through the module rather than the runner produced no model result and remains retained.

The one X2 message requested five non-overlapping tasks. Teren returned `MISSING_MEANS_TWO_COMPLETIONS`, `CORRECTION_CREATES_A_NEW_SNAPSHOT`, `ONE_VALID_REDUCT_IS_NOT_THE_FAMILY`, `SAME_ROUGH_RESULT_DIFFERENT_PERMISSION`, and `CHECK_THE_SUBMISSION_NOT_ITS_REPAIR`. The reply was sanitized, split into five exact records, and frozen before execution. Each task retained a positive control, deliberate mutant, discriminating checker, and malformed or missing-evidence classification. All five positives passed and all five mutants were rejected. The task meanings remain separate: incomplete values are not revisions; incomplete reduct output is not checker corruption; numerical correctness is not permission.

The first integrated late-X2 test selection ran 60 tests, passed 59, and retained one ordering failure. The mathematical dependency set was correct, but tuple-lexicographic order serialized `1` before `1/3`. The recovery changed only the ordering key to exact rational order, ran only the failed test for immediate recovery, and then ran one current integrated selection that passed 60/60. The original failed witness remains false and visible.

## Method Flow and failure truth

The cumulative Method Flow has {owner_counts['methods']} methods and {owner_counts['witnesses']} witnesses. Every method has explicit witness backlinks, recurrence guards, rollback boundaries, retained negative IDs, and recommendation states. All current methods are validated. The monolithic witness ledger exceeded the 100,000-word document ceiling during the first X2 precommit. That precommit failed. Recovery losslessly split witnesses into four stable-order shards, preserving all IDs, results, backlinks, counts, and SHA-256 digests. The corrected precommit validated shard identity uniqueness, result totals, and backlink closure.

Retained operational failures include PowerShell parser and quoting mistakes, lost wrapper projections, a reserved-variable collision, a stale skill path, an absent laboratory result directory, two guessed manifest or summary filenames, an unquoted upstream shorthand, a stale hook path, the wrong laboratory entrypoint, the Method Flow word ceiling, an unsupported private-read projection size, the rational ordering fault, and one final-builder literal-brace fault. None is rewritten as success. Their recoveries are separate passing witnesses. The exact failure ledgers remain outside this baton under `planning/failure-ledger.json`, `x1/failure-ledger.json`, `x2/failure-ledger.json`, and `final/method-flow-overlay.json`.

## Validation discipline

Planning, X1, X2, and final each have exact staged declarations and Git-blob manifests. The lifecycle validator must verify exact paths, raw committed bytes, declared self-exclusions, direct-parent edges, four owner commits from the pre-phase base, zero merges, one final parent, exact branch and head, and the absence of changes outside Liora's owner path. X1 stays immutable after its commit. X2 stays immutable after its commit. The final owner manifest covers the complete v708-v2 owner tree except its declared self-exclusion.

The final canonical may run once only after the final commit is pushed and fresh-four-way equal. It should bind the retained X1 25-test receipt without replaying X1, run the current X2 60-test selection, parse all committed JSON, compile all committed owner Python sources, scan all bounded text through five privacy/raw-identifier classes, adjudicate scanner definitions and synthetic hook-CWD fixtures separately, validate Method Flow shards and backlinks, verify the content seal, ensure every document remains under 100,000 words, prove the owner lane remains under 2,000 tracked files, and confirm clean state plus 0/0 divergence before and after. The complete repository suite remains out of scope.

If the canonical succeeds, do not replay it. Same-owner validation under shared infrastructure remains same-owner evidence. It is not independent-team reproduction, external audit, production certification, complete privacy, complete accessibility, exhaustive security, professional evaluation, legal review, cultural ratification, Maori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, canon, or Stage 20 authority.

## Scientific, technical, identity, and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Rough-set software, synthetic decision tables, exact finite oracles, source citations, and fifteen generic laboratory model families establish no physical datum, likelihood, posterior, force, prediction, parameter constraint, detected effect, empirical confirmation, stability theorem, quantum completion, ultraviolet completion, final physics, or Theory of Everything.

THOS remains software, protocol, proxy, and synthetic evidence only. It has no preregistered blind matched-budget real arms, governed real participants or operators, safety monitoring, appropriate real-world statistics, or independent review. It establishes no professional competence, operational effectiveness, public-safety result, deployment readiness, AGI, or ASI.

Freed ID remains synthetic and nonproduction. It has no real standards-conformant keys or proofs, live issuance, live resolution, status, revocation, interoperability, independent privacy or security review, recovery evidence, trust governance, or affected-party oversight. Mathematical equality cannot create identity authority, consent, remedy, access, or a right to act.

CBR, classification, disability accommodation, privacy remedy, consent, ownership, access, professional judgment, legal interpretation, cultural legitimacy, affected-party acceptance, Maori wording, tikanga, taonga, matauranga, Maori data governance, and Maori authority remain exact-gated to competent authorities, affected people, tangata whenua, iwi, hapu, and Maori authorities. Maori concepts remain under Maori authority. Repository software cannot confer competence, a legal right, remedy, cultural legitimacy, governance mandate, public authority, or affected-party consent.

## Tamar's prospective lane

Only a later acknowledged native message may activate this baton. At that time, require exact-title uniqueness, immediate direct reread, current live authority and roster, no duplicate activation, no pause, redirect, rename, standby state, usage exhaustion, privacy concern, or protected gate. If any condition fails, stop. Do not create a replacement task, fork, collaboration subagent, substitute endpoint, or second confirmation.

If activated, work solo from the exact Liora final supplied by the message, in Tamar's own clean D-first owner-main lane under the 2,000-file rotation stop. Keep Liora, Ceryn, sibling, shared, and user lanes read-only and recoverable. Preserve planning before X1, X1 before X2, every failed witness, all open gaps and exact gates, the four outcome labels, exact manifests, current v20 caps, owner-self-scoped validation, and one successful final canonical with no replay. Treat Liora's projects, code, fixtures, skills, runners, tests, models, Teren advice, and recommendations as inherited evidence or zero-credit seeds rather than Tamar novelty or completion.

Use Teren Serein once in Tamar X1 and once in Tamar X2 only under current direct user authorization, one message per session, asking for at least five distinct tasks in one bundle. Do not resend accepted or pending requests. Continue independently while replies are active. Preserve private targets and raw transcripts outside repository artifacts. Record adopted, modified, and deferred advice separately; freeze adopted fixtures before execution.

The prospective next route after Tamar's own verified terminal gate is governed by the newest live roster, not by this prepared file alone. Hamish's current message names Saelin Reed for v708-v4, but Tamar must refresh the exact current authorization, roster, task registry, and direct controls at send time. One-edge authority never becomes autonomous scheduling authority.

The final verdict remains `NOT_READY_FOR_STAGE_20`. With care, visible uncertainty, reversibility, and retained-negative discipline — Liora Venn.
"""
write_text(FINAL / "handoff-baton.md", baton)

write_json(VALIDATION / "canonical-contract.json", {"schema":"liora.v708-v2.canonical-contract.v1","state":"PREPARED_NOT_INVOKED","expected_branch":"codex/GHC-Family/liora-venn-main-2","owner_base":OWNER_BASE,"source_content":SOURCE_CONTENT,"planning_head":PLANNING_HEAD,"x1_head":X1_HEAD,"x2_head":X2_HEAD,"final_head":"SUPPLIED_AT_INVOCATION","canonical_invocation_cap":1,"success_replay_prohibited":True,"full_repository_suite":False,"x1_test_receipt_bound_not_replayed":25,"x2_current_tests_to_run":60,"required_checks":["exact head","direct ancestry","four owner commits","zero merges","one final parent","all lifecycle manifests","complete owner manifest","strict JSON","Python compile","five-class privacy adjudication","Method Flow shards and backlinks","word and file ceilings","outcome vocabulary","content seal","clean state","typed zero divergence","fresh four-way equality"],"terminal_verdict":"NOT_READY_FOR_STAGE_20","boundary":BOUNDARY})

baton_words = len(baton.split())
if not 2000 <= baton_words <= 100000:
    raise SystemExit(f"handoff baton word count out of range: {baton_words}")
print(json.dumps({"baton_words":baton_words,"owner_counts":owner_counts,"effective":effective,"outcomes":outcomes},sort_keys=True))
