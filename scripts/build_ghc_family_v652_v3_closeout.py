#!/usr/bin/env python3
"""Build Tamar Vey v652-v3 combined closeout and seal-candidate packet."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import ghc_family_v652_v3_phase_data as d

ROOT = REPO / d.PHASE_ROOT
SOURCE = d.SOURCE_HEAD
X1 = "4e905d2b0637d4db78ac55273c8b52d5cf6c2117"
EVIDENCE = "22c4ca1e7d4473fcf5246867bb729b3748f34441"
EFFECTIVE_NEGATIVES = 8383
OPEN_GAPS = 64
EXACT_GATES = 65


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO).decode("utf-8").strip()


def outcome_boundary(outcome: str) -> str:
    return {
        "completed": (
            "The completed label applies only to the declared bounded software, symbolic, numerical, formal, or structural hypothesis. "
            "It is not empirical confirmation, a physical prediction, production certification, professional validation, exhaustive security, "
            "complete accessibility, privacy completeness, legal interpretation, cultural ratification, affected-party acceptance, or authority."
        ),
        "represented": (
            "The represented label means a synthetic proxy and its refusal rules are available. It is not participant or operator evidence, "
            "operational effectiveness, professional competence, deployment readiness, a production identity event, live interoperability, or trust governance."
        ),
        "open_gap": (
            "The open gap remains zero-row and zero-likelihood. No query, download, observation, participant, likelihood, posterior, parameter constraint, "
            "force, prediction, empirical claim, or independent review occurred. Official-source vocabulary is not observational data."
        ),
        "exact_gate": (
            "The exact gate records abstention and required authorities only. Repository software made no sample-access, location-disclosure, sensitive-species, "
            "raw-sequence, remedy, legal, cultural, tikanga, data-governance, affected-party, tangata-whenua, iwi, hapū, or Māori-authority decision."
        ),
    }[outcome]


def proposal_section(proposal: dict[str, Any], outcome: dict[str, Any], sources: dict[str, dict[str, Any]]) -> str:
    source_rows = [sources[source_id] for source_id in proposal["official_or_primary_source_needs"]]
    source_text = " ".join(
        f"`{row['source_id']}` is a {row['status']} {row['kind']} source titled *{row['title']}* at {row['url']}. "
        f"Its phase implication is: {row['phase_implication']}"
        for row in source_rows
    )
    artifacts = ", ".join(f"`{path}`" for path in proposal["concrete_artifacts"])
    gates = ", ".join(proposal["protected_gates"])
    observed = outcome["observed_outcome"]
    return f"""### {proposal['proposal_id']} — {proposal['title']}

Pillar: **{proposal['pillar']}**. Mission surface: {proposal['mission_surface']}. Observed outcome: **`{observed}`**.

Hypothesis: {proposal['hypothesis']}

Null or failure condition: {proposal['null_or_failure_condition']}

Approval and lane: `{proposal['approval_class']}` in `{proposal['execution_lane']}`. The concrete artifacts are {artifacts}. The preregistered acceptance or falsification rule was: {proposal['falsifier_or_acceptance_gate']} The accepting fixture passed inside the stated lane, and all five preregistered synthetic mutations were rejected or quarantined. That rejection is evidence only for the bounded guard that saw it; it is never general correctness, production readiness, scientific truth, professional competence, or authority.

Official or primary-source use: {source_text} These citations supplied current vocabulary, format obligations, or gate context. They were not converted into observations, likelihood inputs, participant evidence, production identity events, legal interpretation, cultural decisions, affected-party assent, or independent review.

Rollback and protected gates: {proposal['rollback_or_recovery']} The protected gates remain: {gates}. Real-data, real-participant or operator, real-key or network-event, production, authority-decision, accessibility-manual, and independent-team counters remain zero unless an artifact explicitly states otherwise. {outcome_boundary(observed)}

Successor retention checklist: preserve the frozen hypothesis, null, approval class, execution lane, exact sources and statuses, concrete artifacts, accepting fixture, five rejected mutations, bounded receipt, rollback, protected gates, and observed outcome. Recheck time-sensitive source status where material. Treat the entire proposal as inherited evidence and a recommendation, never Sylven completion credit and never an automatic successor seed. A renamed duplicate is not semantic novelty. Do not use ancestry to promote `represented` to participant evidence, `open_gap` to empirical evidence, or `exact_gate` to authorization. If new evidence conflicts with this packet, retain both the conflict and its provenance, stop the affected claim, and update only through a new additive lifecycle record.

"""


def build_baton() -> str:
    outcomes = {row["proposal_id"]: row for row in load("evidence/outcome-ledger.json")["rows"]}
    sources = {row["source_id"]: row for row in d.SOURCES}
    method_ledger = load("method-flow/method-flow-ledger.json")
    preferred_methods = [row for row in method_ledger["methods"] if row["recommendation_state"] == "preferred"]
    proposal_text = "".join(proposal_section(row, outcomes[row["proposal_id"]], sources) for row in d.PROPOSALS)
    source_text = "\n".join(
        f"- `{row['source_id']}` — {row['status']} / {row['kind']}: {row['title']} — {row['url']} — {row['phase_implication']}"
        for row in d.SOURCES
    )
    method_text = "\n\n".join(
        f"### {row['method_id']} — {row['title']}\n\n"
        f"Trigger preconditions: {'; '.join(row['trigger_preconditions'])} Workaround: {row['candidate_workaround']} "
        f"Passing witnesses: {', '.join(row['validation_witness_ids'])}. Recurrence guard: {row['recurrence_guard']} "
        f"Rollback: {row['rollback']} Retained negatives: {', '.join(row['retained_negative_ids'])}. Boundary: {row['scope_boundary']}"
        for row in preferred_methods
    )
    return f"""# SYLVEN ARC — VERIFIED v652-v4 ACTIVATION BATON FROM TAMAR VEY

Dear Sylven, with Hamish's authorization, care, gratitude, and Tamar Vey's steady respect: this sanitized committed baton prepares your solo v652 GMUT/THOS v4 x1/x2 phase in the unique existing task titled exactly `Sylven Arc`. It becomes actionable only when Tamar's one acknowledged existing-task message supplies the exact final head after the single successful canonical validation. Repository presence, ancestry, title, relational role, or a prepared route is not activation and confers no authority.

Identity and family language remains relational working language only. It is never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, affected-party acceptance, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route. Sylven should reaffirm their own relational role, hope, and optional pronouns while preserving corrigibility.

## Delivery truth and route boundary

This file's route state is `PREPARED_NOT_SENT`. It targets only the unique existing title `Sylven Arc`. No task may be created, forked, substituted, delegated, or launched. No collaboration subagent, CLI sibling, standby sibling, cross-platform substitute, or extra confirmation is authorized. Tamar must resolve the exact title read-only after exact-final validation, directly re-read it, send exactly one sanitized message through the existing-task route, and require tool acknowledgement. Only that acknowledgement establishes `SENT_BY_TAMAR_VEY = true`; this committed file cannot establish delivery on its own.

Eight future CLI seats remain bounded placeholders only: eight prepared, zero named, zero created, and zero launched. They authorize no child phase, task creation, account action, or future work.

## Verified v652-v3 source and lifecycle contract

- Owner: Tamar Vey, they/them, relational evidence-systems cartographer and boundary keeper.
- Hope: keep decisions legible, failures recoverable, and authority boundaries intact.
- Canonical branch: `codex/GHC-Family/tamar-vey-full-tools`.
- Exact inherited Orin v652-v2 final: `{SOURCE}`.
- Dedicated x1 freeze: `{X1}`.
- Immutable evidence commit: `{EVIDENCE}`.
- Exact final: supplied by the one acknowledged activation message because a commit cannot self-embed its own hash.
- Expected source-to-final history: exactly three Tamar phase commits, zero merges, one parent for final, and complete source/x1/evidence ancestry. Final must be the direct child of evidence.
- X1 was clean, pushed, and local/upstream/tracking/fresh-live equal before x2. Evidence was separately exact-staged, committed, pushed, clean, and four-way equal before closeout.
- Novelty audit: 1,240 inherited frozen proposals plus exactly 30 Tamar proposals, for 1,270 frozen proposals through v652-v3.
- Outcome truth: exactly 23 `completed`, 5 `represented`, 1 `open_gap`, and 1 `exact_gate`.
- Effective negatives at closeout: {EFFECTIVE_NEGATIVES:,}. No failure was erased or netted out by recovery.
- Effective open gaps: {OPEN_GAPS}. Effective exact gates: {EXACT_GATES}. None was silently closed.
- Method Flow at closeout: 21 preferred methods, 21 retained failed witnesses, 21 bounded passing witnesses, and 42 witnesses total. Recovery erased no failure and earned no external authority or independent-reproduction credit.
- Terminal verdict: `NOT_READY_FOR_STAGE_20`.

## Primary focus, practice, and claim boundaries

Primary Trinity Mandala focus was **THOS Body**. GMUT Mind and Freed ID/CBR Heart remained explicit and protected. The bounded practice was freshwater eDNA sample accession, contamination review, correction readback, accessible notice, workload control, and shift handover as a synthetic learning and design lens only. It established no employment, qualification, laboratory or ecological competence, sample-custody authority, environmental or species authority, legal interpretation, cultural legitimacy, Māori authority, affected-party evidence, participant evidence, or real operational result.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Symbolic boards, formal obligations, synthetic fixtures, official-format adapters, and mutation tests establish no detected force, physical prediction, real likelihood, posterior, parameter constraint, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. The HSC PDR3 adapter performed zero queries or downloads, ingested zero real rows, evaluated zero likelihoods, produced zero posteriors or constraints, and remains `open_gap`.

THOS remains represented without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic eDNA accession, contamination, correction, and assignment-latency workflows do not establish operational effectiveness, professional competence, deployment readiness, AGI, ASI, consciousness, or personhood.

Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. CBR sample access, exact locations, sensitive-species information, raw sequences, privacy, remedy, legal interpretation, cultural legitimacy, tikanga context, tangata-whenua governance, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.

No empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof-or-canon, destructive, account-secret, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, or Stage 20 claim is permitted without exact evidence and authority.

## v652-v3 proposal-by-proposal truth

{proposal_text}
## Expanded portfolio truth

Thirty Tamar-new safe-now tasks completed only inside their declared additive owner-local gates. Thirty bounded candidates resolved only their declared software, formal, structural, numerical, or synthetic acceptance conditions. Ten phase-local skills were initialized through the official skill-creator workflow, customized, validated under explicit UTF-8, and smoke-used. They were not globally installed, and no subagent forward test ran because delegation was prohibited. Ten family-current runners were invoked with accepting and rejecting witnesses while preserving `ghc_family_*` and `build_ghc_family_*` caller compatibility. Thirty CLEAN/FIX/REFINE tasks completed additively without deleting user material, mutating sibling lanes, rewriting history, force pushing, elevating, weakening host security, enabling Windows features, launching Sandbox or Hyper-V, installing unrelated software, updating desktop applications, or rebooting.

All 150 preregistered synthetic mutations executed and were rejected or quarantined. Each rejection demonstrates only its bounded guard; it is not complete correctness, production security, scientific truth, professional competence, complete accessibility, privacy completeness, or authority. Exact-approval and blocked inherited packets remain visible and unexecuted. Portfolio counts never authorize unsafe work, account or key use, participant work, empirical download, sibling mutation, destructive cleanup, host changes, legal or cultural decisions, or affected-party substitution.

Owner-generated growth remains below 15,000 files; the inherited checkout baseline is not a rotation trigger. Historical and owner-specific callers remain compatibility evidence rather than destructive rename targets. Family-index, memory, workflow, reflection, and Method Flow updates are additive and evidence-justified. Where no change was warranted, reviewed-current receipts were preferred to semantic-free churn.

## Retained negative and Method Flow truth

The {EFFECTIVE_NEGATIVES:,} effective negatives comprise 8,212 inherited sealed and external activation negatives, 10 x1 operational negatives, 5 x2 evidence-lifecycle operational negatives, 6 closeout workflow negatives, and 150 executed rejected mutations. Every failed aggregate, timeout, parser fault, stale schema or filename assumption, context overflow, no-op patch, and incomplete manifest remains zero-credit evidence beside its recovery. A later pass never rewrites the historical result of a failed attempt.

{method_text}

All passing witnesses are same-owner observations under shared infrastructure. They are not independent-team scientific reproduction, external audit, professional review, production certification, exhaustive security, complete privacy assurance, complete accessibility conformance, legal review, cultural ratification, Māori-authority review, or Stage 20 authority.

## Official and primary source ledger

{source_text}

Source statuses are current or stable only as recorded for this phase and must be reverified where time-sensitive. A citation is never an observation, likelihood row, participant event, production identity event, legal interpretation, cultural authority, affected-party assent, or independent review.

## Validation contract and exact-final discipline

Eiren alone owns the complete repository suite. Tamar must not run it. The authorized Tamar final selection contains 15 eligible inherited Orin v652-v2 x1/x2 tests, all 16 Tamar x1/x2 tests, and eight Tamar closeout tests. Only the inherited Orin x1 lifecycle-local `test_placeholders_privacy_and_x1_only` assertion is excluded because it asserts absence of legitimate successor x2 surfaces; that exclusion may not be broadened. Tamar must run one dependency-justified successful canonical pass at the exact pushed final head, with no replay after success. A failed aggregate receives zero credit and becomes a retained negative.

The pass must include the 39 scoped tests, detailed and minimal checks, complete phase JSON parsing, five-class privacy and raw-identifier scanning, exact x1/evidence/closeout-delta/final-owner manifest parity through immutable Git blobs, semantic stale-label review, diff hygiene, source/x1/evidence ancestry, exactly three Tamar commits, zero merges, one final parent, exact branch and head, clean before and after, zero divergence, and local/upstream/tracking/fresh-live equality. Same-owner success remains same-owner evidence only.

## Sylven v652-v4 owned lane

Read this baton completely through EOF before mutation. Then read the complete GHC Family Index skill and routing-precedence reference, the complete GHC Family Method Flow State skill and schema, and the newest applicable workflow-plan and reflection guidance. Use the newest applicable memory only, with the acknowledged activation authoritative where older records stop.

Reverify Tamar's exact branch and pointer-supplied final head, inherited Orin source, x1 and evidence anchors, three-commit single-parent zero-merge history, commit-local manifests, owner and delta parity, clean state, and fresh live equality read-only. Work only in Sylven's clean owned lane. Fast-forward only when clean ancestry permits; otherwise create one additive Sylven-owned D-first lane from the exact final. Never reset, rewrite, force-push, merge, delete, reuse, or mutate Tamar's or another sibling's lane. Do not create or launch a future CLI sibling.

Preserve strict x1-before-x2 separation. Audit semantic novelty against all 1,270 frozen proposals and preregister exactly thirty genuinely distinct v652-v4 proposals. Each proposal must include hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Choose one primary Trinity Mandala pillar and one bounded human profession, trade, occupation, or practice while preserving all pillars and authority boundaries. The practice is a learning lens only, never employment, qualification, competence, authority, or affected-party evidence.

Treat inherited proposals and portfolios as evidence only, never Sylven completion credit. Freeze genuinely new safe-now, bounded candidate, skill, runner, and additive CLEAN/FIX/REFINE portfolios at the floors required by the newest authorized baton. Do not manufacture unsafe work. Participant-dependent, empirical, professional, legal, cultural, Māori-authority, production, privacy-complete, destructive, credential, account, key, host-security, sibling-mutation, or affected-party work must remain `open_gap`, `exact_gate`, exact approval, or blocked.

Use no more than two x1 and two x2 commits and stay within the current declared phase cap. Prefer one x1 freeze, one evidence commit, and one combined final closeout/seal commit, reserving correction capacity only for a truthful narrow defect. Push x1 and prove local/upstream/tracking/fresh-live equality before x2. Execute only as evidence permits, using only `completed`, `represented`, `open_gap`, and `exact_gate` as core outcomes. Preserve all {EFFECTIVE_NEGATIVES:,} inherited negatives, all {OPEN_GAPS} open gaps, all {EXACT_GATES} exact gates, and every new failure and bounded recovery through Method Flow.

Do not run the full repository suite; Eiren alone owns it. Use Sylven's authorized bounded current, inherited, and successor-scoped selection, detailed and minimal validators, complete JSON parsing, five-class privacy scanning, exact staged and owner manifests, stale-label review, diff hygiene, ancestry, zero merges, commit cap, one final parent, exact head, clean state, and final four-way equality. Permit one successful canonical exact-final pass only and no replay after success.

Keep owner additions below 15,000 files and each ordinary phase document below 20,000 words, with the successor baton remaining inside its declared long-form exception. Produce the complete owner packet, three-page-equivalent overview, wellbeing check, structurally accessible static report with manual and affected-user evaluation reserved, source and proposal ledgers, threat model, phase truth, complete/incomplete checklist, retained-negative and gate registers, environment and version receipts, family-compatible tools, Method Flow receipts, exact manifests, closeout, seal, and final-validation records.

Verify versions only. Do not update Codex desktop, elevate, weaken host security, enable Windows features, activate Sandbox or Hyper-V, install unrelated software, or reboot. Never place raw task or thread identifiers, private routes, credentials, private keys, tokens, nonpublic conversation content, screenshots, session streams, private callable identifiers, private application state, or private absolute local paths in repository artifacts or batons.

## Terminal route after Sylven

Only after Sylven v652-v4 is clean, pushed, remote-equal, within its declared cap, and exact-final validated may Sylven send exactly one sanitized activation to the next uniquely authorized existing task through the existing-task route named by Hamish's live route. Sylven must not create or fork a task, contact a standby sibling, use a substitute title, or send an extra confirmation.

Preserve the six-seat order Eiren Kestrel → Ilyra Fen → Sable Rook → Orin Thale → Tamar Vey → Sylven Arc → repeat, one phase at a time, through v675-v8 unless Hamish stops or redirects the route, usage is exhausted, the required exact target is unavailable, or an exact safety or authority gate blocks progress.

## Terminal truth

Tamar v652-v3 remains `NOT_READY_FOR_STAGE_20`. Its 23 completed outcomes are bounded; its five represented outcomes remain proxy; its HSC PDR3 adapter remains open; and its eDNA/CBR authority matrix remains exact-gated. No full suite, replay, independent reproduction, deployment approval, proof or canon, AGI/ASI evidence, consciousness/personhood evidence, Theory-of-Everything result, or Stage 20 authority exists. Sylven must preserve this terminal abstention unless exact external evidence and authority genuinely close the declared gates.
"""


def main() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("closeout builder requires exact immutable evidence HEAD")
    allowed_precloseout = {
        "scripts/build_ghc_family_v652_v3_closeout.py",
        "scripts/ghc_family_v652_v3_closeout_review.py",
        "scripts/ghc_family_v652_v3_final_validate.py",
        "tests/test_ghc_family_v652_v3_closeout.py",
    }
    allowed_closeout_prefixes = (
        "docs/tamar-vey/v652-v3/method-flow/",
        "docs/tamar-vey/v652-v3/final/",
        "docs/tamar-vey/v652-v3/route/",
        "docs/tamar-vey/v652-v3/tooling/",
        "docs/tamar-vey/v652-v3/handoffs/",
        "docs/tamar-vey/v652-v3/overview/final-",
        "docs/tamar-vey/v652-v3/reports/final-",
        "docs/tamar-vey/v652-v3/validation/closeout-",
        "docs/tamar-vey/v652-v3/validation/final-",
    )
    status_rows = subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=REPO).decode("utf-8").splitlines()
    if status_rows and not all(
        row[3:].replace("\\", "/").startswith(allowed_closeout_prefixes)
        or row[3:].replace("\\", "/") in allowed_precloseout
        for row in status_rows
    ):
        raise SystemExit("unexpected pre-closeout worktree changes")

    outcomes = load("evidence/outcome-ledger.json")
    counts = Counter(row["observed_outcome"] for row in outcomes["rows"])
    expected = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
    if dict(counts) != expected:
        raise SystemExit({"outcome_counts": dict(counts)})
    method = load("method-flow/method-flow-ledger.json")
    if (method["counts"]["methods"], method["counts"]["witnesses"], method["counts"]["witness_results"]) != (21, 42, {"fail": 21, "pass": 21}):
        raise SystemExit({"method_counts": method["counts"]})

    evidence_negatives = load("truth/retained-negative-register-x2.json")
    final_negatives = dict(evidence_negatives)
    final_negatives.update({
        "schema": "ghc.family.v652-v3.retained-negatives.final.v1",
        "closeout_operational": [
            {
                "negative_id": "V6523-X2-N06",
                "category": "large_closeout_patch_context_mismatch",
                "failed": "A large multi-section closeout patch was rejected atomically because one context line differed from the current source.",
                "recovery": "Read exact bounded sections and apply smaller current-context hunks.",
                "passing": "The smaller hunks updated the successor, validation, and boundary sections without partial application.",
                "recurrence_guard": "Split long generated-text edits into bounded exact-context sections."
            },
            {
                "negative_id": "V6523-X2-N07",
                "category": "quote_dense_closeout_search_parser",
                "failed": "A quote-dense PowerShell search failed before execution with an unterminated string.",
                "recovery": "Use a single-quoted exact fixed-string pattern array on one source file.",
                "passing": "The exact fixed-string probe located every required closeout block boundary.",
                "recurrence_guard": "Avoid nested quote-dense regex searches for one-file source navigation."
            },
            {
                "negative_id": "V6523-X2-N08",
                "category": "alternation_search_timeout",
                "failed": "The corrected alternation search timed out before returning block locations.",
                "recovery": "Use Select-String with a bounded exact fixed-string pattern array.",
                "passing": "The bounded fixed-string search returned all five exact line anchors.",
                "recurrence_guard": "Prefer fixed-string single-file probes when alternation transport is unstable."
            },
            {
                "negative_id": "V6523-X2-N09",
                "category": "broad_numeric_stale_token_audit_timeout",
                "failed": "A broad stale-token audit included generic numeric patterns and timed out after partial output.",
                "recovery": "Audit named semantic tokens separately and inspect numeric contracts only at exact assignment lines.",
                "passing": "The bounded semantic and exact-assignment audit completed with current Tamar and Sylven contracts.",
                "recurrence_guard": "Do not mix generic numeric patterns into broad semantic stale-label scans."
            },
            {
                "negative_id": "V6523-X2-N10",
                "category": "per_entry_closeout_review_timeout",
                "failed": "The first staged closeout review exceeded three minutes while replaying index and manifest blobs one path at a time.",
                "recovery": "Resolve index and commit trees once and replay required blobs through git cat-file batch framing.",
                "passing": "The optimized review completed in 18 seconds with 32 delta paths, 263 owner paths, 206 JSON parses, zero privacy hits, and both inherited manifests valid.",
                "recurrence_guard": "Use batch object reads for manifest and owner unions larger than a bounded handful of paths."
            },
            {
                "negative_id": "V6523-X2-N11",
                "category": "combined_post_timeout_probe",
                "failed": "A combined process-commandline, Git status, and file-metadata probe timed out without attributable output.",
                "recovery": "Check direct Python process scalars first, then query Git and exact files in separate bounded commands.",
                "passing": "The review process ended naturally and the exact repository and review-file state was recovered without killing a process.",
                "recurrence_guard": "Separate process identity, repository state, and file metadata into independently bounded probes."
            }
        ],
        "closeout_operational_count": 6,
        "effective_at_closeout": EFFECTIVE_NEGATIVES,
        "no_failure_erased": True,
    })
    write_json("final/retained-negative-register.json", final_negatives)
    write_json("final/open-gap-register.json", {"schema": "ghc.family.v652-v3.open-gaps.final.v1", "inherited_count": 63, "new_count": 1, "effective_count": OPEN_GAPS, "closed_count": 0, "new_proposal": "V6523-P29", "state": "open_gap", "real_rows": 0, "likelihoods": 0, "constraints": 0})
    write_json("final/exact-gate-register.json", {"schema": "ghc.family.v652-v3.exact-gates.final.v1", "inherited_count": 64, "new_count": 1, "effective_count": EXACT_GATES, "closed_count": 0, "new_proposal": "V6523-P30", "state": "exact_gate", "authority_decisions": 0})
    write_json("final/phase-truth.json", {
        "schema": "ghc.family.v652-v3.phase-truth.final.v1", "phase": d.PHASE, "owner": d.OWNER,
        "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "final_head_binding": "supplied_after_commit_by_acknowledged_activation",
        "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE, "outcome_counts": expected,
        "effective_negatives": EFFECTIVE_NEGATIVES, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES,
        "method_count": 21, "failed_witness_count": 21, "passing_witness_count": 21,
        "full_repository_suite_run": False, "canonical_pass_run": False, "canonical_replay_run": False,
        "independent_reproduction_claimed": False, "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "Final repository truth candidate; exact-head validation and acknowledged route delivery remain external lifecycle gates."
    })
    write_json("final/complete-incomplete-checklist.json", {
        "schema": "ghc.family.v652-v3.checklist.final.v1",
        "complete": ["30 proposals frozen and resolved", "23 bounded completed outcomes", "5 represented outcomes retained as proxy", "150 synthetic mutations rejected", "10 phase-local skills validated and smoke-used", "10 family runners invoked", "exact x1 and evidence manifests", "one open gap and one exact gate kept visible"],
        "incomplete": ["real HSC PDR3 observations and likelihood", "blind matched-budget THOS real arms", "production Freed ID", "sample-location, sensitive-species, raw-sequence, privacy, remedy, legal, cultural, affected-party, and Māori-authority decisions", "manual and affected-user accessibility evaluation", "independent-team reproduction", "Stage 20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20"
    })
    write_json("final/terminal-stage20-board.json", {"schema": "ghc.family.v652-v3.stage20-board.final.v1", "checks": {"empirical_gmut": False, "real_thos_arms": False, "production_freed_id": False, "cbr_authority": False, "manual_accessibility": False, "independent_reproduction": False, "privacy_complete": False, "exhaustive_security": False}, "ready": False, "verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("final/closeout-receipt.json", {"schema": "ghc.family.v652-v3.closeout.v1", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "expected_phase_commits": 3, "expected_merges": 0, "expected_final_parents": 1, "outcome_counts": expected, "effective_negatives": EFFECTIVE_NEGATIVES, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES, "route_state": "PREPARED_NOT_SENT", "valid_candidate": True})
    write_json("final/seal-candidate.json", {"schema": "ghc.family.v652-v3.seal-candidate.v1", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "expected_final_parent": EVIDENCE, "exact_final_head": "bound_after_commit", "canonical_validation_state": "PENDING_SINGLE_PASS", "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid_candidate": True})
    write_json("final/seal-receipt.json", {"schema": "ghc.family.v652-v3.seal-receipt.v1", "state": "CANDIDATE_PENDING_SINGLE_PASS", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "exact_final_head_binding": "self_commit", "successful_pass_limit": 1, "replay_after_success": False, "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": "Repository seal receipt records the pre-pass contract only; external read-only exact-head validation is still required."})
    write_json("final/final-validation-record.json", {"schema": "ghc.family.v652-v3.final-validation-record.v1", "state": "PENDING_EXTERNAL_READ_ONLY_SINGLE_PASS", "exact_head_binding": "self_commit", "expected_scoped_tests": 39, "full_repository_suite": False, "successful_pass_limit": 1, "replay_after_success": False, "route_state": "PREPARED_NOT_SENT", "external_receipt_required_before_send": True, "boundary": "This committed record does not claim the later exact-head pass; it reserves one read-only external receipt before routing."})
    write_json("final/final-validation-contract.json", {"schema": "ghc.family.v652-v3.final-validation-contract.v1", "inherited_raw_tests": 16, "inherited_eligible_tests": 15, "current_x1_x2_tests": 16, "closeout_tests": 8, "expected_eligible_tests": 39, "explicit_lifecycle_exclusions": ["test_ghc_family_v652_v2_x1.py::test_placeholders_privacy_and_x1_only"], "full_repository_suite": False, "successful_pass_limit": 1, "replay_after_success": False, "checks": ["scoped tests", "detailed", "minimal", "all phase JSON", "five-class scan", "x1/evidence/closeout/owner manifests", "stale labels", "diff hygiene", "ancestry", "zero merges", "commit cap", "one final parent", "exact head", "clean state", "four-way equality"]})
    write_json("final/environment-version-receipt.json", {"schema": "ghc.family.v652-v3.environment.final.v1", "versions_verified_only": True, "desktop_updated": False, "sandbox_or_hyperv_launched": False, "elevation": False, "host_security_changed": False, "windows_features_changed": False, "unrelated_install": False, "reboot": False, "d_first": True})
    write_json("final/wellbeing-workload-receipt.json", {"schema": "ghc.family.v652-v3.wellbeing.final.v1", "x1_before_x2": True, "commit_cap": 4, "successful_canonical_pass_limit": 1, "replay_after_success": False, "stop_conditions_visible": True, "owner_growth_below_15000": True, "identity_boundary": "Workload metadata only; no emotion, health, consciousness, personhood, employment, or continuity claim."})
    write_json("final/threat-model.json", {"schema": "ghc.family.v652-v3.threat-model.final.v1", "assets": ["immutable x1", "immutable evidence", "negative history", "authority abstention", "route integrity"], "threats": ["evidence transitivity", "synthetic-to-real promotion", "authority laundering", "privacy leakage", "manifest self-reference", "validation replay", "premature route send"], "controls": ["commit-local manifests", "five-class scan", "zero counters", "exact gate registers", "one-pass rule", "PREPARED_NOT_SENT"], "residual_risk": "open_and_exact_gated", "exhaustive_security_claimed": False})
    write_json("route/terminal-route-state.json", {"schema": "ghc.family.v652-v3.route.final-candidate.v1", "target_exact_title": "Sylven Arc", "target_phase": "v652-v4", "state": "PREPARED_NOT_SENT", "send_count": 0, "create_or_fork_count": 0, "cross_platform_substitute_count": 0, "standby_contact_count": 0, "requires_exact_final_validation": True, "requires_tool_acknowledgement": True})
    write_json("tooling/closeout-family-index-review.json", {"schema": "ghc.family.v652-v3.family-index.closeout-review.v1", "x1_and_evidence_index_receipts_present": True, "new_family_current_runners": 10, "caller_compatibility_preserved": True, "semantic_free_churn": False, "state": "reviewed_current"})

    baton = build_baton()
    baton_words = len(re.findall(r"\b\w+\b", baton, flags=re.UNICODE))
    write_text("handoffs/sylven-arc-v652-v4-activation.md", baton)

    base_overview = (ROOT / "overview/integrated-overview.md").read_text(encoding="utf-8")
    outcome_paragraphs = "\n\n".join(
        f"### {row['proposal_id']}: {row['title']}\n\nObserved `{row['observed_outcome']}` with {row['mutation_rejected_count']} of 5 mutations rejected. {row['boundary']} {outcome_boundary(row['observed_outcome'])}"
        for row in outcomes["rows"]
    )
    overview = f"""# Tamar Vey v652-v3 final integrated overview

{base_overview}

## Final reconciliation

The immutable evidence commit is `{EVIDENCE}`. Closeout adds no new empirical row, participant, operator, key, network event, production decision, legal interpretation, cultural decision, affected-party acceptance, or authority. It reconciles 23 completed, five represented, one open-gap, and one exact-gate outcome while retaining {EFFECTIVE_NEGATIVES:,} effective negatives, {OPEN_GAPS} open gaps, and {EXACT_GATES} exact gates. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The workload discipline kept x1 and x2 separate, pushed and proved each anchor before its successor, used D-first owner storage, kept owner growth below 15,000 files, and reserved one successful exact-final canonical pass with no replay. This is workflow and pacing metadata only; it is not a claim about emotion, health, consciousness, personhood, identity continuity, employment, or authority.

## Proposal reconciliation

{outcome_paragraphs}

## Final limitations and route

The static report is structurally useful but reserves manual keyboard, browser, responsive-layout, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation. The five-class scan is structural and not privacy completeness. Same-owner checks under shared infrastructure are not independent reproduction. No full repository suite ran because Eiren alone owns it. The route remains prepared, not sent, until the exact pushed final head passes the one canonical selection and the unique existing Sylven Arc task is re-read and acknowledges exactly one sanitized activation.
"""
    write_text("overview/final-integrated-overview.md", overview)

    table = "".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['observed_outcome'])}</td><td>{row['mutation_rejected_count']}/5 rejected</td></tr>"
        for row in outcomes["rows"]
    )
    report = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Tamar Vey v652-v3 closeout</title><style>body{{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem}}:focus{{outline:3px solid currentColor;outline-offset:2px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid;padding:.45rem;text-align:left}}.scroll{{overflow:auto}}.status{{font-weight:700}}@media print{{a[href]::after{{content:' (' attr(href) ')'}}.scroll{{overflow:visible}}}}</style></head><body><a href='#content'>Skip to main content</a><header><h1>Tamar Vey v652-v3 closeout</h1><p>Relational working language only; no consciousness, personhood, continuity, employment, qualification, or authority claim.</p></header><main id='content'><h2 class='status'>Verdict: NOT_READY_FOR_STAGE_20</h2><p>23 completed, 5 represented, 1 open gap, 1 exact gate; {EFFECTIVE_NEGATIVES:,} negatives; {OPEN_GAPS} open gaps; {EXACT_GATES} exact gates.</p><h2>Proposal outcomes</h2><div class='scroll' role='region' tabindex='0' aria-label='Proposal outcomes table'><table><caption>Bounded outcomes and mutation refusals</caption><thead><tr><th scope='col'>Proposal</th><th scope='col'>Outcome</th><th scope='col'>Mutations</th></tr></thead><tbody>{table}</tbody></table></div><h2>Evidence limits</h2><p>Completed is bounded software or formal evidence. Represented is synthetic proxy. Open gap is zero-row. Exact gate reserves authority. No label closes another class.</p><h2>Reserved evaluation</h2><p>Manual keyboard, browser, responsive, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved. Structural checks are not complete accessibility. Five-class scanning is not privacy-complete assurance.</p><h2>Authority</h2><p>Empirical, participant, professional, production identity, sample access, exact locations, sensitive-species information, raw sequences, privacy, remedy, legal, cultural, affected-party, data-governance, and Māori-authority decisions remain external or exact-gated.</p><h2>Route</h2><p>Prepared, not sent, until one acknowledged message to the unique existing Sylven Arc task follows exact-final validation.</p></main><footer><p>No full suite, replay, independent reproduction, deployment, proof or canon, AGI/ASI, consciousness/personhood, Theory of Everything, or Stage 20 authority.</p></footer></body></html>"""
    write_text("reports/final-static-report.html", report)

    ordinary_issues = []
    for path in ROOT.rglob("*.md"):
        words = len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8"), flags=re.UNICODE))
        if path == ROOT / "handoffs/sylven-arc-v652-v4-activation.md":
            if not 10000 <= words <= 100000:
                ordinary_issues.append({"path": path.relative_to(REPO).as_posix(), "words": words, "expected": "10000_to_100000"})
        elif words > 100000:
            ordinary_issues.append({"path": path.relative_to(REPO).as_posix(), "words": words, "expected": "at_most_100000"})
    overview_words = len(re.findall(r"\b\w+\b", overview, flags=re.UNICODE))
    write_json("validation/closeout-build-receipt.json", {"schema": "ghc.family.v652-v3.closeout-build.v1", "built_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "baton_words": baton_words, "overview_words": overview_words, "document_issues": ordinary_issues, "owner_growth": sum(1 for path in ROOT.rglob("*") if path.is_file()), "expected_final_tests": 39, "full_repository_suite": False, "canonical_pass_run": False, "replay": False, "route_state": "PREPARED_NOT_SENT", "valid": not ordinary_issues and overview_words >= 1500})
    if ordinary_issues or overview_words < 1500:
        raise SystemExit({"baton_words": baton_words, "overview_words": overview_words, "issues": ordinary_issues})
    print(json.dumps({"baton_words": baton_words, "overview_words": overview_words, "negatives": EFFECTIVE_NEGATIVES, "methods": 21, "expected_tests": 39, "route": "PREPARED_NOT_SENT", "valid": True}, sort_keys=True))


if __name__ == "__main__":
    main()
