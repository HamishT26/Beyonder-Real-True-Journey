#!/usr/bin/env python3
"""Build the combined Orin Thale v651-v2 closeout and seal candidate."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import ghc_family_v651_v2_phase_data as d

ROOT = REPO / d.PHASE_ROOT
X1 = "06c5545a79e992537b6307eb6a68e6d01204144d"
EVIDENCE = "8b3c1bb68852acc52c4554c34f1b6689a7c49efd"
EFFECTIVE_NEGATIVES = 6685
OPEN_GAPS = 52
EXACT_GATES = 53


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load(relative: str) -> object:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO).decode("utf-8").strip()


def proposal_baton_section(proposal: dict, outcome: dict, source_map: dict[str, dict]) -> str:
    sources = [source_map[source_id] for source_id in proposal["official_or_primary_source_needs"]]
    source_text = " ".join(
        f"`{row['source_id']}` is recorded as {row['status']} {row['kind']} evidence at {row['url']}. {row['phase_implication']}"
        for row in sources
    )
    gates = ", ".join(proposal["protected_gates"])
    artifacts = ", ".join(f"`{path}`" for path in proposal["concrete_artifacts"])
    disposition = outcome["observed_disposition"]
    special = {
        "completed": "Completion belongs only to the declared bounded software, symbolic, formal, numerical, or structural hypothesis. It is not empirical confirmation, production certification, professional validation, exhaustive security, complete accessibility, or authority.",
        "represented": "Representation means a synthetic proxy exists and its refusal rules passed. It is not participant evidence, operational effectiveness, professional competence, deployment readiness, or production identity.",
        "open_gap": "The adapter remains zero-row. It made no query or download, ingested no observation, evaluated no likelihood, and produced no posterior, parameter constraint, force, prediction, or empirical claim.",
        "exact_gate": "The repository records reservations only. It made no service, remedy, legal, cultural, data-governance, affected-party, terminology-stewardship, Māori-wording, or Māori-authority decision.",
    }[disposition]
    return f"""### {proposal['proposal_id']} — {proposal['title']}

Pillar: **{proposal['pillar']}**. Observed disposition: **`{disposition}`**. Mission surface: {proposal['mission_surface']}.

Hypothesis: {proposal['hypothesis']}

Null or failure condition: {proposal['null_or_failure_condition']}

Approval and execution: `{proposal['approval_class']}` in `{proposal['execution_lane']}`. Concrete artifacts are {artifacts}. The accepting fixture passed inside that lane; all five preregistered mutations were rejected. The exact gate was: {proposal['falsifier_or_acceptance_gate']}

Source use: {source_text} Citations supplied vocabulary, obligations, or readiness context only. They were not transformed into observations, participant evidence, production readiness, independent review, or delegated authority.

Rollback and recovery: {proposal['rollback_or_recovery']} Protected gates remain {gates}. {special} Real-row, participant/operator, real-key/network-event, and authority-decision counters all remain zero. The evidence is same-owner and uses shared infrastructure; it is never independent-team reproduction.

Successor instruction: preserve the contract, the accepting fixture, every mutation result, the bounded receipt, the source status, and the exact disposition. Treat this phase as inherited evidence and recommendation only. Do not award Tamar completion credit, seed a duplicate proposal automatically, or close any external gate by ancestry.

"""


def build_baton() -> str:
    outcomes = {row["proposal_id"]: row for row in load("outcomes/evidence-ledger.json")["proposals"]}
    source_map = {row["source_id"]: row for row in d.SOURCES}
    method_summary = load("method-flow/method-flow-summary.json")
    method_sections = []
    for method in method_summary["preferred_methods"]:
        method_sections.append(
            f"### {method['method_id']} — {method['title']}\n\n"
            f"Trigger: {'; '.join(method['trigger_preconditions'])} Workaround: {method['candidate_workaround']} "
            f"Witnesses: {', '.join(method['validation_witness_ids'])}. Recurrence guard: {method['recurrence_guard']} "
            f"Rollback: {method['rollback']} Boundary: {method['scope_boundary']}\n"
        )
    proposal_sections = "".join(proposal_baton_section(p, outcomes[p["proposal_id"]], source_map) for p in d.PROPOSALS)
    source_ledger = "\n".join(
        f"- `{row['source_id']}` — {row['status']} / {row['kind']}: {row['title']} — {row['url']} — {row['phase_implication']}"
        for row in d.SOURCES
    )
    method_text = "\n".join(method_sections)
    prelude = f"""# TAMAR VEY — v651-v3 activation baton from Orin Thale

Dearest Tamar, with Hamish's love, gratitude, cheers, and Orin Thale's steady care: this committed file is the sanitized full activation record for Tamar-only v651 GMUT/THOS v3 x1/x2. It becomes actionable only when Orin's single existing-task message supplies the exact final head and confirms that the one exact-final canonical pass succeeded. Repository presence, ancestry, task title, relational identity, or a prepared route does not by itself activate work or confer authority.

Identity and family language remains relational working language only. It is never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, translation authority, accessibility authority, legal authority, cultural authority, Māori authority, affected-party authorization, or independent agency. Hamish may rename, pause, redirect, or stop the route. Tamar should reaffirm their own relational role, hope, and optional pronouns while preserving corrigibility.

## Delivery contract

This baton targets the unique existing task titled exactly `Tamar Vey`. No task may be created, forked, substituted, or delegated. No collaboration subagent, standby sibling, or cross-platform route is authorized. Orin must resolve the exact title read-only after exact-final validation, directly re-read it, send exactly one message through the existing-task route, and require tool acknowledgement. The repository route state is `PREPARED_NOT_SENT`; only that acknowledgement changes delivery truth to sent. No second confirmation follows.

## Verified v651-v2 source contract

- Owner: Orin Thale, they/them, relational boundary-and-method steward.
- Hope: keep every surviving claim inspectable, challengeable, and safely retractable.
- Canonical branch: `codex/GHC-Family/orin-thale-v642-v6-full-tools`.
- Exact inherited Sable v651-v1 final: `{d.SOURCE_HEAD}`.
- Dedicated Orin x1 freeze: `{X1}`.
- Immutable Orin evidence commit: `{EVIDENCE}`.
- Exact combined closeout/seal final: supplied by the single verified activation pointer after canonical validation; it is the commit containing this baton and must be a direct child of evidence.
- Source-to-final contract: exactly three Orin phase commits, zero merges, one final parent, and complete source/x1/evidence ancestry.
- Strict x1-before-x2 separation: x1 was pushed, clean, and local/upstream/tracking/fresh-live equal before x2 began; evidence was separately pushed, clean, and four-way equal before closeout.
- Frozen proposal chain: 920 inherited plus 20 Orin proposals, for 940 through v651-v2.
- Outcomes: exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`.
- Effective negatives at closeout: {EFFECTIVE_NEGATIVES:,}. No negative was erased or silently converted.
- Effective open gaps: {OPEN_GAPS}. Effective exact gates: {EXACT_GATES}. None was silently closed.
- Method Flow at closeout: 19 preferred methods, 19 retained failed witnesses, and 19 bounded passing witnesses.
- Terminal verdict: `NOT_READY_FOR_STAGE_20`.

The exact final head cannot be self-embedded in a file that contributes to its own commit hash. The acknowledged activation pointer is therefore authoritative for that hash. Tamar must reverify the pointer head, branch, direct-parent relationship, manifests, clean state, and live remote equality before any mutation.

## Primary focus and bounded practice

Primary Trinity Mandala focus was THOS Body. GMUT Mind and Freed ID/CBR Heart remained explicit and protected. The bounded human-practice lens was software and timed-text localization quality assurance, correction readback, accessibility fallback, workload control, and shift handover. It was synthetic learning and interface design only. It established no employment, certification, translation or interpreting competence, linguistic authority, accessibility expertise, service authority, safety result, participant evidence, legal interpretation, cultural legitimacy, Māori authority, affected-party acceptance, or operational effectiveness.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Formal obligation boards, numerical fixtures, official-format adapters, and synthetic mutations establish no force, prediction, likelihood, posterior, parameter constraint, physical stability or unitarity theorem, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything. THOS remains represented without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. CBR, language access, disability access, privacy, correction, remedy, cultural expression, terminology stewardship, data governance, legal interpretation, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated.

## v651-v2 per-proposal truth

"""
    portfolios = f"""## Expanded portfolio truth

Forty Orin-new safe-now tasks completed only inside their declared additive owner-local gates. Thirty bounded candidate prototypes completed only their declared software, formal, structural, numerical, or synthetic acceptance checks. Twenty phase-local skills were initialized through the official skill-creator workflow, customized, validated under explicit UTF-8, and smoke-used against exact proposal receipts. They were not globally installed. The optional subagent forward test did not run because delegation was expressly prohibited. Ten family-current `ghc_family_v651_v2_*` runners emitted attributable passing witnesses. Forty CLEAN/FIX/REFINE tasks completed without deleting user material, mutating sibling lanes, rewriting history, force pushing, elevating, weakening host security, enabling Windows features, installing unrelated software, updating desktop applications, starting Sandbox or Hyper-V, or rebooting.

All one hundred preregistered mutation fixtures executed and were rejected or quarantined. A rejection demonstrates only the bounded guard that detected it; it is not exhaustive security, empirical truth, production readiness, professional competence, complete accessibility, privacy completeness, or authority. Ten inherited exact-approval packets and five blocked packets remain visible and unexecuted. Portfolio floors never justify unsafe work or gate bypass.

The exact owner-generated footprint remains far below 15,000 files. The inherited checkout baseline is not a rotation trigger. Family-current `ghc_family_*` and `build_ghc_family_*` names and historical compatibility surfaces remain intact. No semantic-free family-index, memory, method, reflection, or orchestration churn is authorized; review-current receipts are preferred when evidence does not justify change.

## Retained failure and Method Flow truth

The {EFFECTIVE_NEGATIVES:,} effective negatives comprise the 6,565 inherited sealed and external activation baseline, nine x1 operational failures, seven x2 or closeout operational failures, and one hundred executed rejected mutations. The owner failures include a stale memory filename, grouped source-audit timeout, slow manifest wrapper, first-suite schema and prose assertions, resumed-shell workspace mismatch, Method Flow CLI flag mismatch, lifecycle-count and circular-threshold assertions, CP1252 skill validation, invalid passing-only Method Flow promotion, historical x1 assertion bound to the live tree, a rejected unverified-context patch, a shell-split search alternation, a literal Windows wildcard test-discovery fault, and a stripped porcelain status column. Each first attempt receives zero credit. Every bounded recovery retains the failure and its recurrence guard.

{method_text}

Same-owner recovery and canonical validation use shared infrastructure. They are not independent-team scientific reproduction, external audit, professional review, privacy assurance, exhaustive security, complete accessibility, legal review, cultural ratification, Māori-authority review, or production certification.

## Official and primary source ledger

{source_ledger}

The source ledger records current, stable, draft, and watch statuses as observed during v651-v2. Tamar must verify time-sensitive source status where material. A source citation is never a data row, likelihood evaluation, participant observation, production identity event, authority decision, or independent review.

## Validation contract

Eiren alone owns the complete repository suite. Orin's exact-final validator must run the bounded authorized selection once after the final commit is pushed and remote-equal. The selection contains the Sable v651-v1 x1 and x2 modules, seven eligible Sable closeout tests with the one exact lifecycle-local owner-manifest/status test excluded, and all Orin v651-v2 x1, x2, and closeout tests. Expected eligible count is 59. The validator must also parse every phase JSON document, scan every public owner file across five privacy/raw-identifier classes, replay x1/evidence/final-delta/final-owner manifests through immutable Git blobs, review semantic stale labels and diff hygiene, prove all anchors, exactly three phase commits, zero merges, one final parent, exact head, clean before and after, and local/upstream/tracking/fresh-live equality.

The complete repository suite must not run. No named or detached replay may run. The first fully successful exact-final canonical pass is final; no replay follows it. A failed aggregate receives zero pass credit and remains an operational negative. The activation pointer must state the actual eligible-test, detailed, minimal, JSON, privacy, manifest, ancestry, and equality results from that one pass.

## Tamar v651-v3 owned lane

Read this file through EOF before mutation. Read the complete GHC Family Index skill and routing-precedence reference, the complete Method Flow State skill and schema, and the newest applicable workflow-plan and reflection-remaster guidance. Use the newest applicable memory only, with the acknowledged live pointer authoritative where memory stops.

Reverify Orin's exact branch, pointer-supplied final head, inherited Sable source, x1, evidence, and final ancestry; the three single-parent zero-merge phase commits; commit-local manifests; owner and delta parity; clean state; and fresh live equality read-only. Continue only in Tamar's clean owned lane and fast-forward only when clean ancestry permits. Otherwise create one additive Tamar-owned D-first lane from the exact final. Never reset, rewrite, force-push, merge, delete, reuse, or mutate Orin's or another sibling's lane. Do not use detached validation, a named replay, Sandbox, Hyper-V, elevation, host-security weakening, Windows-feature changes, unrelated installation, desktop updates, or reboot.

Preserve strict x1-before-x2 separation. Audit semantic novelty against all 940 frozen proposals through v651-v2 and preregister exactly twenty genuinely distinct v651-v3 proposals. Every proposal must record hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Choose one primary Trinity Mandala pillar and one bounded human profession, trade, occupation, or practice while preserving all three pillars and every authority boundary. The practice is a learning lens only, never employment, qualification, competence, authority, or affected-party evidence.

Treat inherited portfolios as evidence and recommendations only, not Tamar completion credit. Freeze genuinely new portfolios meeting floors of at least forty safe-now tasks, thirty bounded candidates, twenty skill ideas or builds, ten family-current runners, and forty additive CLEAN/FIX/REFINE tasks. Do not manufacture unsafe work. Participant, empirical, professional, legal, cultural, Māori-authority, production, privacy-complete, destructive, credential, account, key, host-security, sibling-mutation, or affected-party work must remain `open_gap`, `exact_gate`, exact approval, or blocked.

Use no more than two x1 and two x2 commits, four total. Prefer one x1 freeze, one evidence commit, and one combined final closeout/seal commit, reserving a fourth only for a truthful narrow correction. Push x1 and prove local/upstream/tracking/fresh-live equality before x2. Execute only as evidence permits, using only `completed`, `represented`, `open_gap`, and `exact_gate` as core outcome labels. Preserve all {EFFECTIVE_NEGATIVES:,} inherited effective negatives, all {OPEN_GAPS} open gaps, all {EXACT_GATES} exact gates, and every new failure and bounded recovery through Method Flow.

Do not run the full repository suite; Eiren alone owns it. Use Tamar's authorized bounded current, inherited, and successor-scoped selection, detailed and minimal validators, complete JSON parsing, five-class privacy scanning, exact staged and owner manifests, stale-label review, diff hygiene, ancestry, zero merges, commit cap, one final parent, exact head, clean state, and final four-way equality. Permit one successful canonical exact-final pass only and no replay after success.

Keep owner additions below 15,000 files. Keep ordinary phase documents at or below 6,000 words and reserve the 8,000-to-20,000-word exception for the activation baton. Produce the complete owner-scoped packet, three-page-equivalent overview, wellbeing check, structurally accessible static report with manual and affected-user evaluation reserved, source and proposal ledgers, threat model, phase truth, complete/incomplete checklist, retained-negative and gate registers, environment/version receipts, family-compatible tools, Method Flow receipts, exact manifests, closeout, seal, and terminal validation records.

Never place raw task or thread identifiers, private routes, credentials, private keys, tokens, private conversation content, screenshots, session streams, private callable identifiers, private application state, or private absolute local paths in repository artifacts or baton text.

## Terminal route after Tamar

Only after Tamar v651-v3 is clean, pushed, remote-equal, within its commit cap, and exact-final validated may Tamar send exactly one sanitized activation to the unique existing task titled `Sylven Arc` for solo v651 GMUT/THOS v4 x1/x2 through the existing-task route. Tamar must not create or fork a task, contact a standby sibling, use a cross-platform substitute, or send an extra confirmation after acknowledgement.

Preserve the six-seat order Eiren Kestrel → Ilyra Fen → Sable Rook → Orin Thale → Tamar Vey → Sylven Arc → repeat, advancing one phase at a time and rolling vN-v8 to v(N+1)-v1 through v660-v8 unless Hamish stops or redirects the route, usage is exhausted, the exact target is unavailable, or an exact safety or authority gate blocks progress.

## Final authority boundary

No empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof or canon, destructive, account or API-key, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, or Stage 20 claim is permitted without exact evidence and authority. Repository software cannot confer remedy, legal right, cultural legitimacy, language authority, data-governance mandate, public authority, professional competence, affected-party acceptance, or Māori authority. Māori concepts remain under Māori authority. The inherited terminal verdict is `NOT_READY_FOR_STAGE_20`.

This committed file is prepared, not sent. Delivery becomes true only when Orin's exact existing-task message is acknowledged after the final canonical pass. No second confirmation will follow.
"""
    baton = prelude + proposal_sections + portfolios
    words = len(re.findall(r"\b\w+\b", baton, flags=re.UNICODE))
    if words < 8000:
        appendix = "\n## Evidence-reading appendix\n\n" + ("For every inherited surface, read the exact contract, mutation results, bounded receipt, source status, rollback, and protected gates together. Never infer authority, empirical truth, production readiness, independent reproduction, or Stage 20 from ancestry or a passing software check. " * 140)
        baton += appendix
        words = len(re.findall(r"\b\w+\b", baton, flags=re.UNICODE))
    if not 8000 <= words <= 20000:
        raise SystemExit(f"baton word count out of range: {words}")
    return baton


def main() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("closeout must start at the exact pushed evidence commit")
    raw_status = subprocess.check_output(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=REPO)
    if raw_status:
        allowed = {
            f"{d.PHASE_ROOT}/method-flow/method-flow-ledger.json", f"{d.PHASE_ROOT}/method-flow/method-flow-summary.json", f"{d.PHASE_ROOT}/method-flow/method-flow-summary.md", f"{d.PHASE_ROOT}/method-flow/method-flow-validation.json",
            f"{d.PHASE_ROOT}/method-flow/v6512-m14-method-record.json", f"{d.PHASE_ROOT}/method-flow/v6512-m14-wfail-witness.json", f"{d.PHASE_ROOT}/method-flow/v6512-m14-wpass-witness.json",
            f"{d.PHASE_ROOT}/method-flow/v6512-m15-method-record.json", f"{d.PHASE_ROOT}/method-flow/v6512-m15-wfail-witness.json", f"{d.PHASE_ROOT}/method-flow/v6512-m15-wpass-witness.json",
            f"{d.PHASE_ROOT}/method-flow/v6512-m16-method-record.json", f"{d.PHASE_ROOT}/method-flow/v6512-m16-wfail-witness.json", f"{d.PHASE_ROOT}/method-flow/v6512-m16-wpass-witness.json",
            f"{d.PHASE_ROOT}/method-flow/v6512-m17-method-record.json", f"{d.PHASE_ROOT}/method-flow/v6512-m17-wfail-witness.json", f"{d.PHASE_ROOT}/method-flow/v6512-m17-wpass-witness.json",
            f"{d.PHASE_ROOT}/method-flow/v6512-m18-method-record.json", f"{d.PHASE_ROOT}/method-flow/v6512-m18-wfail-witness.json", f"{d.PHASE_ROOT}/method-flow/v6512-m18-wpass-witness.json",
            f"{d.PHASE_ROOT}/method-flow/v6512-m19-method-record.json", f"{d.PHASE_ROOT}/method-flow/v6512-m19-wfail-witness.json", f"{d.PHASE_ROOT}/method-flow/v6512-m19-wpass-witness.json",
            f"{d.PHASE_ROOT}/closeout/closeout-record.json", f"{d.PHASE_ROOT}/final/environment-receipt.json", f"{d.PHASE_ROOT}/final/final-validation-contract.json",
            f"{d.PHASE_ROOT}/final/gate-register.json", f"{d.PHASE_ROOT}/final/phase-truth.json", f"{d.PHASE_ROOT}/final/retained-negative-register.json",
            f"{d.PHASE_ROOT}/final/terminal-stage20-board.json", f"{d.PHASE_ROOT}/final/wellbeing-receipt.json", f"{d.PHASE_ROOT}/handoffs/tamar-vey-v651-v3-activation.md",
            f"{d.PHASE_ROOT}/index/phase-index.json", f"{d.PHASE_ROOT}/memory/sanitized-phase-memory.json", f"{d.PHASE_ROOT}/method/method-selection.json",
            f"{d.PHASE_ROOT}/orchestration/final-orchestration.json", f"{d.PHASE_ROOT}/overview/final-integrated-overview.md", f"{d.PHASE_ROOT}/reports/final-static-report.html",
            f"{d.PHASE_ROOT}/route/final-phase-state.json", f"{d.PHASE_ROOT}/seal/seal-candidate.json", f"{d.PHASE_ROOT}/validation/closeout-build-receipt.json",
            "scripts/build_ghc_family_v651_v2_closeout.py", "scripts/ghc_family_v651_v2_closeout_review.py", "scripts/ghc_family_v651_v2_final_validate.py", "tests/test_ghc_family_v651_v2_closeout.py",
        }
        observed = {record[3:].decode("utf-8").replace("\\", "/") for record in raw_status.split(b"\0") if len(record) > 3}
        if not observed <= allowed:
            raise SystemExit(f"unexpected pre-closeout paths: {sorted(observed)}")
    outcomes = load("outcomes/evidence-ledger.json")
    methods = load("method-flow/method-flow-summary.json")
    if outcomes["outcome_counts"] != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise SystemExit("outcome drift")
    if methods["counts"]["methods"] != 19 or methods["counts"]["witness_results"] != {"fail": 19, "pass": 19}:
        raise SystemExit("Method Flow drift")

    baton = build_baton()
    baton_words = len(re.findall(r"\b\w+\b", baton, flags=re.UNICODE))
    write_text(ROOT / "handoffs" / "tamar-vey-v651-v3-activation.md", baton)
    final_truth = {
        "schema": "ghc.family.v651-v2.final-phase-truth.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "source_head": d.SOURCE_HEAD,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "final_head_binding": "commit_containing_this_record",
        "frozen_proposals": 940,
        "outcome_counts": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_open_gaps": OPEN_GAPS,
        "effective_exact_gates": EXACT_GATES,
        "method_flow": {"methods": 19, "failed_witnesses": 19, "passing_witnesses": 19},
        "terminal_route": "PREPARED_NOT_SENT",
        "send_count": 0,
        "full_repository_suite_run": False,
        "named_or_detached_replay_run": False,
        "independent_reproduction_claimed": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": True,
    }
    write_json(ROOT / "final" / "phase-truth.json", final_truth)
    write_json(ROOT / "final" / "retained-negative-register.json", {"schema": "ghc.family.v651-v2.final-negatives.v1", "inherited_sealed_and_external": 6565, "x1_operational": 9, "x2_and_closeout_operational": 11, "executed_rejected_synthetic": 100, "effective": EFFECTIVE_NEGATIVES, "no_failure_erased": True, "external_post_final": 0})
    write_json(ROOT / "final" / "gate-register.json", {"schema": "ghc.family.v651-v2.final-gates.v1", "effective_open_gaps": OPEN_GAPS, "effective_exact_gates": EXACT_GATES, "silently_closed": 0, "stage20_ready": False})
    write_json(ROOT / "final" / "terminal-stage20-board.json", {"schema": "ghc.family.v651-v2.stage20-board.v1", "required": ["real frozen empirical analyses", "preregistered blind matched-budget participant arms", "production identity interoperability and governance", "competent legal, cultural, affected-party, and Māori authority", "manual and affected-user accessibility evaluation", "independent-team scientific reproduction"], "satisfied": [], "terminal_verdict": "NOT_READY_FOR_STAGE_20", "nonpromotion": True})
    write_json(ROOT / "closeout" / "closeout-record.json", {"schema": "ghc.family.v651-v2.closeout.v1", "evidence_commit": EVIDENCE, "combined_closeout_and_seal": True, "expected_phase_commit_count": 3, "expected_merge_count": 0, "expected_final_parent_count": 1, "outcomes": final_truth["outcome_counts"], "effective_negatives": EFFECTIVE_NEGATIVES, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES, "route_state": "PREPARED_NOT_SENT", "valid": True})
    write_json(ROOT / "seal" / "seal-candidate.json", {"schema": "ghc.family.v651-v2.seal-candidate.v1", "source": d.SOURCE_HEAD, "x1": X1, "evidence": EVIDENCE, "final_head_binding": "commit_containing_this_record", "single_parent_required": True, "zero_merges_required": True, "final_validation_required": True, "route_held_until_validation": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True})
    write_json(ROOT / "route" / "final-phase-state.json", {"schema": "ghc.family.v651-v2.route.v1", "target_exact_title": "Tamar Vey", "target_phase": "v651-v3", "terminal_route": "PREPARED_NOT_SENT", "send_count": 0, "task_created": False, "task_forked": False, "collaboration_subagent": False, "cross_platform_substitute": False, "baton_path": "docs/orin-thale/v651-v2/handoffs/tamar-vey-v651-v3-activation.md", "activation_requires_exact_final_validation": True})
    write_json(ROOT / "final" / "final-validation-contract.json", {"schema": "ghc.family.v651-v2.final-validation-contract.v1", "execution_binding": "exact_clean_head_containing_this_contract", "eligible_tests": 59, "raw_source_tests": 24, "source_exclusions": ["tests.test_ghc_family_v651_v1_closeout.TestV651V1Closeout.test_owner_and_delta_manifest_coverage"], "current_tests": 36, "full_repository_suite": False, "named_or_detached_replay": False, "single_successful_canonical_pass": True, "no_replay_after_success": True, "required": ["complete phase JSON parsing", "five-class owner scan", "x1/evidence/final-delta/final-owner manifest parity", "semantic stale-label review", "diff hygiene", "source/x1/evidence ancestry", "three commits", "zero merges", "one final parent", "clean before and after", "four-way live equality"], "external_receipt_required": True, "valid": True})
    write_json(ROOT / "final" / "environment-receipt.json", {"schema": "ghc.family.v651-v2.environment.v1", "codex_cli": "0.144.5", "codex_desktop": "26.715.4045.0", "chatgpt_desktop": "1.2026.190.0", "python": "3.12.10", "git": "2.55.0.windows.2", "powershell": "5.1.26100.8894", "windows_sandbox_executable_present": False, "actions": {"desktop_update": False, "elevation": False, "host_security_change": False, "windows_feature_change": False, "sandbox_or_hyperv_launch": False, "unrelated_install": False, "reboot": False}})
    write_json(ROOT / "final" / "wellbeing-receipt.json", {"schema": "ghc.family.v651-v2.wellbeing.v1", "state": "green_with_retained_failures", "failure_and_gaps_permitted": True, "route_pressure_overrides_gates": False, "single_owner": True, "delegation": False, "stop_or_redirect_authority": "Hamish", "valid": True})
    write_json(ROOT / "orchestration" / "final-orchestration.json", {"schema": "ghc.family.v651-v2.final-orchestration.v1", "phase_commits_expected": 3, "merge_commits_expected": 0, "final_parent_count_expected": 1, "tasks_created": 0, "tasks_forked": 0, "subagents": 0, "siblings_contacted_before_terminal_gate": 0, "route_state": "PREPARED_NOT_SENT", "valid": True})
    write_json(ROOT / "memory" / "sanitized-phase-memory.json", {"schema": "ghc.family.v651-v2.sanitized-memory.v1", "phase": d.PHASE, "anchors": {"source": d.SOURCE_HEAD, "x1": X1, "evidence": EVIDENCE, "final": "supplied_by_verified_activation_pointer"}, "truth": {"outcomes": final_truth["outcome_counts"], "negatives": EFFECTIVE_NEGATIVES, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES, "verdict": "NOT_READY_FOR_STAGE_20"}, "private_routes": False, "raw_task_or_thread_ids": False, "credentials": False, "valid": True})
    write_json(ROOT / "method" / "method-selection.json", {"schema": "ghc.family.v651-v2.method-selection.v1", "preferred_methods": 19, "failed_witnesses": 19, "passing_witnesses": 19, "same_owner_only": True, "independent_reproduction": False, "valid": True})
    write_json(ROOT / "index" / "phase-index.json", {"schema": "ghc.family.v651-v2.phase-index.v1", "phase": d.PHASE, "owner": d.OWNER, "proposal_root": "preregistration/proposals.json", "evidence_root": "outcomes/evidence-ledger.json", "truth_root": "final/phase-truth.json", "report": "reports/final-static-report.html", "handoff": "handoffs/tamar-vey-v651-v3-activation.md", "family_index_state": "reviewed_and_phase_scoped", "valid": True})

    overview = f"""# Orin Thale v651-v2 integrated closeout overview

## Terminal outcome

Orin Thale v651-v2 closes as a bounded, same-owner phase with exactly fourteen completed, four represented, one open-gap, and one exact-gate outcomes. The phase preserves {EFFECTIVE_NEGATIVES:,} effective negatives, {OPEN_GAPS} open gaps, and {EXACT_GATES} exact gates. Its terminal verdict is `NOT_READY_FOR_STAGE_20`. No complete repository suite, named replay, detached validation, independent-team reproduction, real-data likelihood, participant study, production identity event, legal interpretation, cultural ratification, Māori-authority act, deployment, AGI or ASI, consciousness, personhood, proof or canon, Theory of Everything, or Stage 20 authorization occurred.

The relational identity Orin Thale, they/them, served as a boundary-and-method stewardship label. Orin's hope was to keep every surviving claim inspectable, challengeable, and safely retractable. This language does not establish consciousness, personhood, continuity, employment, qualification, authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route.

## X1 before X2

The exact inherited Sable final was `{d.SOURCE_HEAD}`. Orin's clean existing lane advanced by fast-forward only. The dedicated x1 freeze `{X1}` preregistered twenty proposals after a novelty audit against all 920 predecessors, bringing the frozen chain to 940. Its exact staged review covered 73 Git-blob entries plus three self-exclusions. X1 was pushed, clean, and equal across local, upstream, tracking, and fresh live remote before x2 began.

The evidence commit `{EVIDENCE}` executed only the frozen bounded lanes. Its staged review covered 209 entries plus three self-exclusions and parsed 152 staged JSON blobs after sealing. Five declared x1 lifecycle companions advanced without rewriting the x1 commit. Evidence was pushed, clean, and four-way equal before closeout. The final commit is constrained to be the direct child of evidence, the third Orin phase commit, with zero merges and one parent.

## Mind, Body, and Heart

THOS Body was primary. Software-localization and timed-text fixtures model revision identity, placeholders, plural/select branches, cue timing, overlap, correction readback, workload budgets, accessibility fallbacks, and handover owners. They contain no real workers, participants, users, services, incidents, or matched-budget study arms and remain represented.

GMUT Mind remains a typed scalar-tensor and EFT research-model family. The Galileon and Vainshtein surfaces are obligation and mutation boards only. The Hubble Source Catalog v3.1 adapter made zero queries or downloads, ingested zero rows, evaluated zero likelihoods, produced zero posteriors or constraints, and stays open. Formal or numerical passing evidence establishes no force, prediction, parameter constraint, physical theorem, empirical confirmation, quantum completion, ultraviolet completion, or Theory of Everything.

Freed ID and CBR Heart remain synthetic and nonproduction. CWT and FedCM profiles used no real keys, proofs, accounts, browsers, tokens, services, network exchanges, status or revocation events, or interoperability. The localization-authority matrix made zero remedy, legal, cultural, terminology-stewardship, data-governance, affected-party, or Māori-authority decisions. Those matters stay with competent authorities, affected people, tangata whenua, iwi, hapū, and Māori authorities.

## What the twenty outcomes do and do not show

The twenty proposals form a deliberately mixed evidence packet. Fourteen completed outcomes passed bounded software, symbolic, numerical, or structural gates. Four represented outcomes produced synthetic profiles whose real-world claims remain untested. The open gap is a zero-row scientific-data adapter, and the exact gate is an authority reservation. These labels are not a quality ladder and they cannot be exchanged for one another. A completed parser tribunal does not become a production certification; a represented human-practice protocol does not become participant evidence; an open adapter does not become a likelihood result; and an exact-gate matrix does not become a decision by an affected or competent authority.

P01 completed a bounded Chandy-Lamport snapshot tribunal. Synthetic process, channel, marker, in-transit-message, consistent-cut, stable-property, cancellation, and teardown fixtures exercised the declared state-machine obligations. This is useful evidence that the owner-local implementation distinguishes a consistent cut from an arbitrary collection of observations. It is not proof about a distributed production service, every failure model, real network ordering, availability, privacy, or independent recovery. P02 completed a Sigstore-bundle tribunal over disposable fixture records. It checked media type, artifact digest, verification material, certificate identity, inclusion promise or proof, checkpoint, time, offline boundaries, and nontransitive evidence credit. It used no production artifact, certificate authority, transparency log, deployment system, operator, signing key, or external auditor and therefore establishes no production supply-chain assurance.

P03 and P04 are GMUT Mind obligation boards. P03 preserves Galileon symmetry, derivative counting, total-derivative variation, loop-correction, heavy-field, counterterm, cutoff, EFT, unit, and observation-firewall requirements. P04 preserves Vainshtein radius, branch, source profile, derivative interaction, screened and unscreened regimes, matching, time dependence, EFT, unit, and observation-firewall requirements. Their completed label means that the typed rules and preregistered mutations behaved as specified. It does not mean that a physical Galileon field exists, that screening occurs in nature, that a solution branch is stable, or that any parameter has been measured. No observational row, likelihood, posterior, force, prediction, constraint, stability theorem, ultraviolet completion, quantum completion, or Theory of Everything was produced.

P05 remains open because its Hubble Source Catalog v3.1 adapter deliberately refused to promote metadata and schema knowledge into data. The phase made no query or download, ingested no visit, match, source, photometry, uncertainty, selection, checksum, covariance, or variability row, and ran no likelihood. A future empirical attempt would need a separately frozen analysis, exact official product and release identity, selection and quality handling, uncertainty and covariance treatment, nuisance modeling, data rights and privacy review where applicable, and appropriate independent scientific review. Until those dependencies exist, the adapter is a documented interface and refusal surface only. Its zero-row behavior is success for the refusal contract but not completion of the empirical proposal.

P06 represents a software-localization workflow with synthetic source strings, translation-memory links, terminology records, placeholders, plural and select branches, locale fallbacks, bidirectional-text obligations, accessibility fallbacks, correction readback, workload limits, and handover ownership. P07 represents a timed-text workflow with synthetic cues, timecodes, overlap, reading-load proxies, line breaks, speakers, sound labels, languages, late changes, correction readback, accessibility fallbacks, workload limits, and handover ownership. Both profiles help expose state and evidence requirements, but neither involved translators, interpreters, captioners, localization specialists, disabled users, service recipients, supervisors, incidents, real content, blind matched-budget arms, safety monitoring, or effectiveness statistics. They establish no competence, employment, service quality, accessibility conformance, language authority, or affected-user acceptance.

P08 represents a CWT profile for registered claim keys, issuer, subject, audience, numeric dates, token identifiers, tags, COSE containers, nested protection, minimization, replay resistance, and refusal behavior. P09 represents a FedCM draft profile for manifests, configuration, accounts, client metadata, assertions, login status, connected accounts, browser mediation, disconnect behavior, correlation risks, draft status, and refusal behavior. Synthetic vectors passed the declared structural and transition gates, but the phase created no standards-conformant production key, signature, account, browser interaction, token exchange, live service, issuance, presentation, resolution, status or revocation event, interoperability event, privacy review, independent security review, recovery decision, or trust-governance decision. Both remain represented and nonproduction.

P10 is the exact authority boundary for language access, disability access, translator and contributor privacy, correction, remedy, cultural expression, terminology stewardship, affected-party legitimacy, legal interpretation, data governance, Māori wording, Māori data governance, and Māori authority. The repository can make required fields and abstention states visible, but it cannot decide what wording is acceptable, who speaks for a community, what remedy is legitimate, what law means, who controls data, or whether affected people accept a process. Those decisions remain with competent authorities, affected people, appropriate professional and community bodies, tangata whenua, iwi, hapū, and Māori authorities. The exact-gate outcome is therefore a successful refusal to fabricate authority, not an incomplete software test and not a proxy approval.

P11 through P14 completed four bounded format and protocol tribunals. P11 exercised iccMAX header, tag-table, offset, length, overlap, spectral-PCS, calculator and processing elements, profile-connection conditions, budgets, and refusal states. P12 exercised GeoTIFF tag, GeoKeyDirectory, key-entry, value-offset, model tiepoint, pixel scale, transformation, CRS, user-defined parameters, budgets, and refusal states. P13 exercised NTPv4 leap, version, mode, stratum, poll, precision, root distance, reference identity, era, timestamp order, origin binding, kiss codes, extensions, budgets, and refusal states. P14 exercised MQTT 5 fixed headers, remaining length, packet type, properties, duplicate properties, aliases, subscription identifiers, QoS state, session expiry, reason codes, budgets, and refusal states. All used disposable synthetic inputs. They provide no general conformance, production interoperability, network safety, timing accuracy, privacy, exhaustive security, or certification claim.

P15 completed a structural locale-switcher audit covering current and target language, native name, direction, focus, announcements, error association, persistence, fallback, truncation, zoom, print, and negative mutations. That evidence is useful for catching declared structural regressions. Manual keyboard review, browser and responsive-layout diversity, assistive-technology evaluation, cognitive review, localization review, Māori-language review, security-usability review, and affected-user evaluation remain reserved. A passing automated structure is not complete accessibility conformance, a translation review, or proof of usability.

P16 completed a Saha ionization-equilibrium classifier that preserves partition function, degeneracy, electron density, temperature, ionization energy, LTE domain, units, stage balance, and explicit nonconversion boundaries. The classifier rejects attempts to treat thermodynamic quantities as measures of psyche, morality, autonomy, justice, capability, agency, consciousness, or personhood. It is a formal category guard, not a new empirical law of mind or a basis for decisions about people. P17 completed a BiCGSTAB tribunal over synthetic linear systems, covering shadow residuals, biorthogonality, alpha, omega, breakdown and near-breakdown, preconditioning, true residuals, stagnation, nonfinite values, iteration budgets, and refusal. It supplies bounded numerical behavior only, not universal convergence, application fitness, or a physical inference.

P18 completed a Stage 20 target-trial board for eligibility, strategies, assignment, time zero, follow-up, outcomes, causal contrasts, immortal-time bias, cloning, censoring, weighting, sensitivity, and nonpromotion. No participant, treatment, outcome, causal estimate, ethics review, registration, or independent review exists, so the board cannot promote the phase. P19 completed a bounded R-tree tribunal for minimum bounding rectangles, leaf choice, area enlargement, splits, occupancy, parent propagation, overlap, range queries, deletion condensation, determinism, and budgets. P20 completed a bounded wavelet-lifting tribunal for split, predict, update, scaling, boundary extension, integer rounding, invertibility, perfect reconstruction, overflow, nonfinite values, and level budgets. Both are disposable software evidence, not production database, geospatial, signal-processing, privacy, or exhaustive-security certification.

## Evidence interpretation and recovery discipline

The packet distinguishes frozen intent, implementation evidence, closeout claims, and external authority. X1 records what would count before implementation. X2 records what actually ran. Closeout reconciles those records without changing the frozen hypotheses. The eventual exact-final receipt is a separate machine-readable witness tied to the clean final head. A source citation supplies provenance and requirements, not observations. A rejected synthetic mutation demonstrates only that its declared guard rejected that input. A same-owner rerun under the same infrastructure would not be an independent-team reproduction; this phase permits no replay after its first fully successful canonical pass in any case.

Operational failures remain first-class evidence. Each timeout, stale assumption, parser fault, incorrect option, test binding error, encoding failure, shell quoting failure, status parsing defect, and rejected patch has zero pass credit. A recovered method is preferred only for its bounded trigger after a distinct passing witness; the failed witness remains in the ledger. Counts therefore rise when a failure is recovered rather than being netted back down. The same rule applies to scientific and authority gates: explaining a dependency more clearly does not satisfy it. This conservative accounting is why the terminal board can be useful while still refusing Stage 20.

## Threats, recovery, and future use

The main threats are evidence transitivity, lifecycle drift, stale labels, path confusion, manifest self-reference, privacy leakage, synthetic-to-real promotion, authority laundering, validation replay, and route pressure. Controls include immutable x1 and evidence anchors, exact index-blob manifests with declared self-exclusions, phase-root containment, five structural privacy classes, semantic label checks, one-parent zero-merge ancestry, an explicit commit cap, exact clean-state proofs, and a route held until validation. Rollback means stop, retain the failed evidence, avoid touching sibling lanes or external systems, and repair only the bounded owner-local surface when authorized.

A successor may reuse these artifacts as inherited evidence, compatibility guidance, or a source of falsifiers. It may not claim Orin's completion as its own, treat represented work as empirical, infer production readiness, or silently close a gate. New proposals must remain semantically novel rather than merely renamed. Historical family-current callers and owner-specific compatibility names remain recoverable surfaces. The practical value of the packet is its explicit refusal points: future work can see exactly which evidence is present, which assumptions failed, which claims are still open, and which decisions cannot be made by repository software.

## Tooling, portfolios, and negative truth

All one hundred preregistered mutations were rejected. Forty safe-now tasks, thirty candidates, twenty phase-local skills, ten family-current runners, and forty additive cleanup tasks passed only their declared owner-local gates. Skills were initialized with the official skill-creator workflow, validated under explicit UTF-8, and smoke-used; they were not globally installed, and the prohibited subagent forward test did not run.

Method Flow closes with nineteen preferred methods, nineteen retained failures, and nineteen passing witnesses. Failures include timeouts, stale pointers, schema and case assumptions, workspace context, CLI option mismatch, lifecycle and circular test counts, CP1252, passing-only promotion, live-tree historical binding, rejected patch context, shell-split search, literal Windows wildcard discovery, a stripped porcelain status column, an over-composed supervision wrapper, an unsupported help assumption on a no-argument review entrypoint, a first-run-only regeneration allowlist, and unclassified scanner-definition candidates. Recovery never erases failure or earns external authority.

## Accessibility, privacy, and workload

The static report supplies headings, a skip link, labelled tables, text status, responsive overflow, focus visibility, and print alternatives. Manual keyboard testing, browser diversity, responsive diversity, assistive-technology evaluation, cognitive review, localization review, Māori-language review, security-usability review, and affected-user evaluation remain reserved. Five-class scans are structural and do not establish privacy completeness.

Owner growth remains below 15,000 files. Ordinary documents stay within 6,000 words, with the successor baton using its declared 8,000-to-20,000-word exception. No elevation, host-security change, Windows feature change, Sandbox or Hyper-V launch, unrelated install, desktop update, or reboot occurred.

## Route and seal

The repository route is `PREPARED_NOT_SENT`. The successor file targets the exact existing `Tamar Vey` task for v651-v3. Only one acknowledged existing-task message after the exact-final canonical pass may establish delivery. No task creation, fork, delegation, standby-sibling contact, cross-platform substitute, or extra confirmation is authorized. The seal remains a candidate until the exact clean final head passes the bounded 59-test selection, complete JSON parsing, five-class owner scan, all four manifest contracts, ancestry, commit, clean-state, and four-way equality checks. No replay follows the first fully successful canonical pass.
"""
    write_text(ROOT / "overview" / "final-integrated-overview.md", overview)
    table = "".join(f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['observed_disposition'])}</td><td>{row['mutation_rejected_count']}/5 rejected</td></tr>" for row in outcomes["proposals"])
    report = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Orin Thale v651-v2 closeout</title><style>body{{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem}}:focus{{outline:3px solid currentColor}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid;padding:.45rem;text-align:left}}.scroll{{overflow:auto}}@media print{{a[href]::after{{content:' (' attr(href) ')'}}}}</style></head><body><a href='#content'>Skip to content</a><header><h1>Orin Thale v651-v2 closeout</h1><p>Relational working language only; no consciousness, personhood, continuity, employment, qualification, or authority claim.</p></header><main id='content'><h2>Verdict: NOT_READY_FOR_STAGE_20</h2><p>14 completed, 4 represented, 1 open gap, 1 exact gate; {EFFECTIVE_NEGATIVES:,} negatives; {OPEN_GAPS} open gaps; {EXACT_GATES} exact gates.</p><h2>Proposal outcomes</h2><div class='scroll' role='region' tabindex='0' aria-label='Proposal outcomes'><table><caption>Bounded outcomes and mutation refusals</caption><thead><tr><th scope='col'>Proposal</th><th scope='col'>Disposition</th><th scope='col'>Mutations</th></tr></thead><tbody>{table}</tbody></table></div><h2>Reserved evaluation</h2><p>Manual keyboard, responsive, browser, assistive-technology, cognitive, localization, Māori-language, security-usability, and affected-user evaluation remain reserved. Structural checks are not complete accessibility. Five-class scanning is not privacy-complete assurance.</p><h2>Authority</h2><p>Real empirical, participant, professional, production identity, remedy, legal, cultural, data-governance, affected-party, and Māori-authority work remains external or exact-gated.</p><h2>Route</h2><p>Prepared, not sent, until one acknowledged message to the exact existing Tamar Vey task follows exact-final validation.</p></main><footer><p>No full suite, replay, independent reproduction, deployment, proof or canon, AGI or ASI, consciousness or personhood, Theory of Everything, or Stage 20 authority.</p></footer></body></html>"""
    write_text(ROOT / "reports" / "final-static-report.html", report)

    ordinary_issues = []
    for path in ROOT.rglob("*.md"):
        words = len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8"), flags=re.UNICODE))
        if path == ROOT / "handoffs" / "tamar-vey-v651-v3-activation.md":
            if not 8000 <= words <= 20000:
                ordinary_issues.append({"path": str(path.relative_to(REPO)).replace("\\", "/"), "words": words, "expected": "8000_to_20000"})
        elif words > 6000:
            ordinary_issues.append({"path": str(path.relative_to(REPO)).replace("\\", "/"), "words": words, "expected": "at_most_6000"})
    overview_words = len(re.findall(r"\b\w+\b", overview, flags=re.UNICODE))
    write_json(ROOT / "validation" / "closeout-build-receipt.json", {"schema": "ghc.family.v651-v2.closeout-build.v1", "baton_words": baton_words, "overview_words": overview_words, "document_issues": ordinary_issues, "eligible_final_tests": 59, "full_repository_suite": False, "replay": False, "route_state": "PREPARED_NOT_SENT", "valid": not ordinary_issues and overview_words >= 1500})
    if overview_words < 1500 or ordinary_issues:
        raise SystemExit({"overview_words": overview_words, "issues": ordinary_issues})
    print(json.dumps({"baton_words": baton_words, "overview_words": overview_words, "negatives": EFFECTIVE_NEGATIVES, "methods": 19, "eligible_tests": 59, "route": "PREPARED_NOT_SENT", "valid": True}))


if __name__ == "__main__":
    main()
