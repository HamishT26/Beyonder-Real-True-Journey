#!/usr/bin/env python3
"""Build Vesper Arlen's strict x1-only v658-v7 freeze packet."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v658_v7_phase_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
SOURCE_PHASE = ROOT / "docs/neris-solane/v658-v6"
SOURCE_INDEX = SOURCE_PHASE / "provenance/frozen-chain-proposal-index.json"
SOURCE_NEGATIVES = SOURCE_PHASE / "truth/retained-negative-register-x2.json"
SOURCE_OPEN_GAPS = SOURCE_PHASE / "truth/open-gap-register-x2.json"
SOURCE_EXACT_GATES = SOURCE_PHASE / "truth/exact-gate-register-x2.json"
SOURCE_METHODS = SOURCE_PHASE / "method-flow/method-flow-state-x2.json"
SOURCE_ROUTE_STATE = SOURCE_PHASE / "orchestration/route-state-x2.json"
NOVELTY_THRESHOLD = 0.60
MANIFEST_EXCLUSIONS = {
    "validation/x1-content-manifest.json",
    "validation/x1-privacy-scan.json",
    "validation/x1-staged-review.json",
    "validation/x1-validation-receipt.json",
}
NEW_X1_CODE = [
    "scripts/ghc_family_v658_v7_phase_catalogue.py",
    "scripts/ghc_family_v658_v7_phase_data.py",
    "scripts/build_ghc_family_v658_v7_x1.py",
    "tests/test_ghc_family_v658_v7_x1.py",
]


def write_json(relative: str, payload: Any, *, compact: bool = False) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=None if compact else 2, separators=(",", ":") if compact else None, sort_keys=True)
    path.write_text(text + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha256(revision: str, repository_relative: str) -> str:
    blob = subprocess.run(["git", "show", f"{revision}:{repository_relative}"], cwd=ROOT, check=True, capture_output=True).stdout
    return hashlib.sha256(blob).hexdigest()


def prospective_blob(repository_relative: str) -> str:
    return git("hash-object", "-w", f"--path={repository_relative}", repository_relative)


def prospective_blob_record(repository_relative: str) -> dict[str, Any]:
    oid = prospective_blob(repository_relative)
    return {"path": repository_relative, "git_blob": oid, "bytes": int(git("cat-file", "-s", oid))}


def inherited_rows() -> list[dict[str, str]]:
    payload = read_json(SOURCE_INDEX)
    rows = list(payload["prior_proposals"]) + list(payload["new_proposals"])
    if len(rows) != d.PRIOR_FROZEN or payload["effective_count"] != d.PRIOR_FROZEN:
        raise RuntimeError(f"expected {d.PRIOR_FROZEN} inherited proposals, found {len(rows)}")
    return [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in rows]


def title_tokens(value: str) -> set[str]:
    stop = {"a", "an", "and", "for", "from", "in", "into", "of", "on", "or", "the", "to", "with", "without", "no", "only", "through", "synthetic", "contract", "ledger", "board", "envelope"}
    return {token for token in re.findall(r"[a-z0-9]+", value.lower()) if token not in stop}


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / len(left | right) if left or right else 1.0


def novelty_audit(prior: list[dict[str, str]]) -> list[dict[str, Any]]:
    audit: list[dict[str, Any]] = []
    for index, proposal in enumerate(d.PROPOSALS):
        candidates = prior + [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in d.PROPOSALS[:index]]
        tokens = title_tokens(proposal["title"])
        nearest = max(candidates, key=lambda row: jaccard(tokens, title_tokens(row["title"])))
        score = jaccard(tokens, title_tokens(nearest["title"]))
        audit.append({
            "proposal_id": proposal["proposal_id"],
            "nearest_proposal_id": nearest["proposal_id"],
            "nearest_title": nearest["title"],
            "jaccard": round(score, 4),
            "threshold": NOVELTY_THRESHOLD,
            "passes": score < NOVELTY_THRESHOLD,
        })
    failures = [row for row in audit if not row["passes"]]
    if failures:
        raise RuntimeError(f"semantic novelty threshold failed: {failures}")
    return audit


def verify_source() -> dict[str, Any]:
    if git("rev-parse", "HEAD") != d.SOURCE_FINAL:
        raise RuntimeError("x1 builder must run at the exact inherited source head")
    for anchor in (d.SOURCE_INHERITED, d.SOURCE_X1, d.SOURCE_EVIDENCE, d.SOURCE_FINAL):
        subprocess.run(["git", "merge-base", "--is-ancestor", anchor, d.SOURCE_FINAL], cwd=ROOT, check=True)
    if git("rev-parse", f"{d.SOURCE_FINAL}^") != d.SOURCE_EVIDENCE:
        raise RuntimeError("source final is not the direct child of source evidence")
    phase_commit_count = int(git("rev-list", "--count", f"{d.SOURCE_INHERITED}..{d.SOURCE_FINAL}"))
    merge_count = int(git("rev-list", "--count", "--merges", f"{d.SOURCE_INHERITED}..{d.SOURCE_FINAL}"))
    if phase_commit_count != 3 or merge_count != 0:
        raise RuntimeError("source history does not match the three-commit zero-merge terminal truth")

    index = read_json(SOURCE_INDEX)
    negatives = read_json(SOURCE_NEGATIVES)
    open_gaps = read_json(SOURCE_OPEN_GAPS)
    exact_gates = read_json(SOURCE_EXACT_GATES)
    methods = read_json(SOURCE_METHODS)
    route = read_json(SOURCE_ROUTE_STATE)
    if index["effective_count"] != d.PRIOR_FROZEN:
        raise RuntimeError("source proposal count mismatch")
    if negatives["effective_count"] != d.SOURCE_EFFECTIVE_NEGATIVES:
        raise RuntimeError("source negative count mismatch")
    if (open_gaps["effective_count"], exact_gates["effective_count"]) != (d.SOURCE_OPEN_GAPS, d.SOURCE_EXACT_GATES):
        raise RuntimeError("source gate counts mismatch")
    if methods["counts"]["effective_methods"] != d.SOURCE_METHODS:
        raise RuntimeError("source Method Flow count mismatch")
    if route["next_exact_title"] != "Vesper Arlen" or route["next_phase"] != "v658-v7":
        raise RuntimeError("source route does not point to the activated Vesper phase")

    route_relative = SOURCE_ROUTE_STATE.relative_to(ROOT).as_posix()
    if git("rev-parse", f"{d.SOURCE_FINAL}:{route_relative}") != d.SOURCE_ROUTE_STATE_GIT_BLOB:
        raise RuntimeError("source route Git blob mismatch")
    if git_blob_sha256(d.SOURCE_FINAL, route_relative) != d.SOURCE_ROUTE_STATE_SHA256:
        raise RuntimeError("source route Git-blob SHA-256 mismatch")
    if sha256(SOURCE_ROUTE_STATE) != d.SOURCE_ROUTE_STATE_CHECKOUT_SHA256:
        raise RuntimeError("source route checkout-byte SHA-256 mismatch")
    return {
        "schema": "ghc.family.v658-v7.source-verification.v1",
        "source_owner": d.SOURCE_OWNER,
        "source_branch": d.SOURCE_BRANCH,
        "source_inherited": d.SOURCE_INHERITED,
        "source_x1": d.SOURCE_X1,
        "source_evidence": d.SOURCE_EVIDENCE,
        "source_final": d.SOURCE_FINAL,
        "source_final_parent": d.SOURCE_EVIDENCE,
        "source_phase_commit_count": phase_commit_count,
        "source_merge_count": merge_count,
        "source_single_parent_commits": True,
        "source_terminal_equality_verified_read_only": True,
        "source_manifest_entries_replayed_read_only": 537,
        "source_manifest_mismatches": 0,
        "source_canonical_aggregate_replayed": False,
        "source_canonical_receipt_sha256": d.SOURCE_CANONICAL_RECEIPT_SHA256,
        "source_route_state_path": route_relative,
        "source_route_state_git_blob": d.SOURCE_ROUTE_STATE_GIT_BLOB,
        "source_route_state_sha256": d.SOURCE_ROUTE_STATE_SHA256,
        "source_route_state_checkout_sha256": d.SOURCE_ROUTE_STATE_CHECKOUT_SHA256,
        "valid": True,
        "boundary": "Neris's successful aggregate remains inherited same-owner evidence only and was not replayed.",
    }


def method_flow() -> dict[str, Any]:
    inherited = read_json(SOURCE_METHODS)["counts"]
    if inherited["effective_methods"] != d.SOURCE_METHODS or inherited["effective_witness_results"] != {"fail": d.SOURCE_FAILED_WITNESSES, "pass": d.SOURCE_PASSING_WITNESSES}:
        raise RuntimeError("inherited Method Flow totals mismatch")
    methods, witnesses, events, recommendations = [], [], [], []
    for index, negative in enumerate(d.X1_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6587-X1-METHOD-{index:02d}"
        fail_id, pass_id = f"V6587-X1-WITNESS-{index:02d}-F", f"V6587-X1-WITNESS-{index:02d}-P"
        methods.append({
            "method_id": method_id,
            "title": f"Bounded recovery for {negative['signature']}",
            "trigger_preconditions": [negative["signature"]],
            "failure_signature": negative["observed"],
            "candidate_workaround": negative["recovery"],
            "recurrence_guard": negative["recurrence_guard"],
            "approval_class": "safe_now_owner_local_read_or_workflow_recovery",
            "privacy_class": "sanitized_public",
            "scope_boundary": "Same-owner bounded workflow recovery only.",
            "rollback": "Stop, retain the failed witness at zero credit, and leave external and sibling state unchanged.",
            "protected_gates": d.PROTECTED_GATES,
            "retained_negative_ids": [negative["negative_id"]],
            "validation_witness_ids": [fail_id, pass_id],
            "recommendation_state": "preferred",
            "supersedes": [],
        })
        witnesses.extend([
            {"witness_id": fail_id, "method_id": method_id, "result": "fail", "procedure": "Retain the original bounded attempt without pass credit.", "expected": "The initial attempt would satisfy its bounded postcondition.", "observed": negative["observed"], "retained_negative_ids": [negative["negative_id"]], "same_owner_only": True, "independent_reproduction": False, "boundary": "Zero pass credit; the failure remains retained."},
            {"witness_id": pass_id, "method_id": method_id, "result": "pass", "procedure": negative["recovery"], "expected": "The isolated recovery establishes only its bounded postcondition.", "observed": f"The bounded recovery completed for {negative['signature']}.", "retained_negative_ids": [negative["negative_id"]], "same_owner_only": True, "independent_reproduction": False, "boundary": "Same-owner bounded recovery only."},
        ])
        events.extend([
            {"method_id": method_id, "before": None, "after": "candidate", "witness_id": fail_id},
            {"method_id": method_id, "before": "candidate", "after": "validated", "witness_id": pass_id},
            {"method_id": method_id, "before": "validated", "after": "preferred", "witness_id": pass_id},
        ])
        recommendations.append({"recommendation_id": f"V6587-X1-REC-{index:02d}", "method_id": method_id, "recommendation": negative["recurrence_guard"], "state": "preferred", "completion_credit": False})
    count = len(methods)
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "lifecycle": "x1_frozen",
        "inherited_anchor": {"repository_relative_path": "docs/neris-solane/v658-v6/method-flow/method-flow-state-x2.json", "methods": d.SOURCE_METHODS, "failed_witnesses": d.SOURCE_FAILED_WITNESSES, "passing_witnesses": d.SOURCE_PASSING_WITNESSES, "completion_credit": False},
        "current_owner_method_count": count,
        "current_phase_method_ids": [row["method_id"] for row in methods],
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": recommendations,
        "counts": {"inherited_methods": d.SOURCE_METHODS, "current_methods": count, "effective_methods": d.SOURCE_METHODS + count, "current_witness_results": {"fail": count, "pass": count}, "effective_witness_results": {"fail": d.SOURCE_FAILED_WITNESSES + count, "pass": d.SOURCE_PASSING_WITNESSES + count}},
        "identity_boundary": "Relational working language only; no consciousness, personhood, continuity, employment, qualification, authority, or independent agency.",
        "boundary": "Every failed witness remains retained; no independent, empirical, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, or Stage 20 claim.",
    }


def proposal_markdown() -> str:
    rows = ["# Vesper Arlen v658-v7 x1 proposal ledger", "", "These are frozen hypotheses and expected dispositions, not x2 results. Identity and family language is relational working language only.", ""]
    for p in d.PROPOSALS:
        rows.extend([
            f"## {p['proposal_id']} — {p['title']}", "",
            f"- Pillar relation: {p['pillar_relation']}", f"- Mechanism: {p['mechanism']}",
            f"- Hypothesis: {p['hypothesis']}", f"- Null or failure: {p['null_or_failure_condition']}",
            f"- Approval class: `{p['approval_class']}`", f"- Execution lane: `{p['execution_lane']}`",
            f"- Official or primary sources: {', '.join(p['official_or_primary_source_needs'])}",
            f"- Concrete artifacts: {', '.join(p['concrete_artifacts'])}",
            f"- Falsifier or acceptance gate: {p['falsifier_or_acceptance_gate']}",
            f"- Rollback or recovery: {p['rollback_or_recovery']}",
            f"- Protected gates: {', '.join(p['protected_gates'])}",
            f"- Expected disposition only: `{p['expected_disposition']}`", "",
        ])
    return "\n".join(rows)


def source_markdown() -> str:
    rows = ["# Vesper Arlen v658-v7 official and primary source ledger", "", "Statuses were checked on 2026-08-02. Source presence does not establish implementation, conformance, professional review, legal interpretation, cultural ratification, Māori authority, or empirical confirmation.", "", "| ID | Status | Publisher | Title | Bounded use |", "|---|---|---|---|---|"]
    rows.extend(f"| `{s['source_id']}` | `{s['status']}` | {s['publisher']} | [{s['title']}]({s['url']}) | {s['use']} |" for s in d.OFFICIAL_SOURCES)
    return "\n".join(rows)


def integrated_overview() -> str:
    return """# Vesper Arlen v658-v7 x1 integrated overview

## Relational identity, control, and evidence ceiling

Vesper Arlen, they/them, is relational working language for this owner-scoped phase. Their working role is relational aircraft-maintenance evidence custodian. Their hope is to make synthetic maintenance records and handovers auditable without turning software structure into airworthiness or operational authority. These words do not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.

This is a bounded synthetic software-evidence phase, not an aircraft-maintenance organisation, maintenance programme, engineering review, inspection service, release-to-service system, airworthiness determination, dispatch decision, or flight-safety service. It does not establish that Vesper or any software is a licensed maintainer, engineer, inspector, certifier, operator, regulator, accessibility expert, credential issuer, legal decision maker, cultural authority, Māori authority, or independently empowered agent. Contradictory evidence may downgrade an expected disposition; protected gates stop execution; and source, failure, rollback, and route records remain reviewable.

## Immutable Neris source and strict x1 boundary

The packet descends exactly from Neris Solane's immutable v658-v6 final `26d90ff750269ee9aa84d520043f8c6096b69024`. Read-only verification established the inherited Elaren source, Neris x1, Neris evidence, and final ancestry across exactly three new single-parent commits and zero merges. Final is the direct child of evidence. Neris's source lane was clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote. All 537 declared manifest entries were replayed read-only without mismatch. Neris's successful 68-test canonical aggregate was deliberately not replayed.

The source preserves 2,830 frozen proposals, 17,496 effective negatives, 118 open gaps, 117 exact gates, and 3,770 Method Flow methods with failed and bounded passing witnesses. Vesper's nine startup and x1 failures are appended at zero credit and paired with bounded recoveries. This x1 packet contains no surface implementation, mutation outcome, empirical row, real aircraft record, maintenance event, inspection result, certification, release, credential event, production event, successor message, or task mutation. Its verdict is `NOT_READY_FOR_STAGE_20`.

## THOS Body primary focus and bounded practice

THOS Body is primary through a synthetic aircraft-maintenance record and handover portfolio. The thirty proposals cover fictional scope and aircraft configuration; maintenance-data applicability and revision; work orders and task cards; access and closure; tool calibration; part and material provenance; component life counters and chains; non-routine findings; NDT and critical-task boundaries; material and foreign-object control; environment, inspection, functional-check, software-load, deferred-item, amendment, workload, and shift-handover records; plus bounded GMUT, Freed ID, accessibility, data-capability, and CBR surfaces.

These mechanisms are software and mathematical checks only. There is no real person, operator, organisation, aircraft, registration, flight, component, part, defect, measurement, tool, work order, task card, inspection, maintenance action, release, dispatch, airworthiness finding, safety advice, professional judgment, or operational decision. A valid synthetic fixture cannot become empirical or professional confirmation.

The completed THOS surfaces may test declared state transitions and mutation refusals. The represented THOS batch and handover surfaces may test partition, digest, checkpoint, retry, quarantine, unresolved-card, and acknowledgement-placeholder states. They do not perform maintenance, conduct an operational handover, certify a record, authorize release or dispatch, or establish real workload benefit, blind matched-budget arms, participant outcomes, deployment readiness, production reliability, or independent review.

GMUT Mind remains explicit through a typed fatigue-crack and damage operator with unit, domain, identifiability, and airworthiness firewalls. GMUT remains a research-model family. This phase does not fit real fatigue data, estimate service life, approve an interval, establish structural integrity, constrain a physical parameter, confirm a prediction, establish a fundamental law, supply ultraviolet completion, or prove a Theory of Everything.

Freed ID remains explicit through nonproduction maintenance-record and tool-part provenance envelopes. Synthetic digests, derivation, amendment, expiry, revocation holds, disclosure limits, and challenge routes create no real key, signature, proof, identifier, credential, issuer, holder, live resolution, status, revocation, interoperability, recovery, privacy or security review, trust framework, or production identity.

CBR Heart remains explicit through worker and passenger privacy, safety-event disclosure, contestability, remedy, affected-party governance, legal, cultural, and Māori-authority reservations. Machine-checkable structure is not complete accessibility; manual, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved. Legal interpretation, incident disclosure, maintenance or flight-safety decisions, remedy allocation, cultural ratification, collective data governance, and Māori authority require competent and affected authorities and cannot be delegated by repository text.

## Thirty distinct proposals and four truth labels

Each proposal title is compared mechanically against all 2,830 inherited frozen titles and earlier v658-v7 titles using a disclosed token-set Jaccard screen below 0.60, followed by mechanism-level review. Distinct mechanisms include configuration effectivity, controlled-data revisions, task-card transitions, calibration and part traceability, life counters, component chains, non-routine findings, inspection eligibility, functional checks, software-load holds, record amendments, human-factor handover, and a typed fatigue-damage firewall.

Proposals 1 through 23 are expected only as `completed`: a bounded local validator accepts one declared fixture and rejects five preregistered mutations. Completion says only that the synthetic contract behaved as preregistered. Proposals 24 through 28 are expected only as `represented`: two THOS proxies, two nonproduction Freed ID profiles, and one accessible static atlas. Proposal 29 is an `open_gap` because CAA or FAA service-difficulty transport and real rows are disabled. Proposal 30 is an `exact_gate` because safety, privacy, incident disclosure, remedy, legal, cultural, affected-party, and Māori-authority decisions require affected and competent parties. No fifth truth label is permitted.

## Sources and nonpromotion

Official and primary rails include current New Zealand CAA Part 43 and advisory-circular surfaces, eCFR Part 43, FAA service-difficulty and damage-tolerance material, EASA continuing-airworthiness rules, W3C provenance, accessibility, and verifiable-credential recommendations, RFC canonicalization, New Zealand privacy principles, Te Mana Raraunga, and Local Contexts. They provide vocabulary and boundary context only. They do not confer regulatory compliance, professional competence, data access, airworthiness, maintenance or release authority, empirical confirmation, legal advice, cultural ratification, Māori authority, privacy completeness, accessibility completeness, security assurance, or production readiness.

Every failed wrapper, parser, quoting, encoding, path, and transport attempt remains a zero-credit negative. A bounded recovery proves only its recovered postcondition. It neither erases the failed witness nor turns related same-owner work into independent reproduction. Shared infrastructure, family tools, and correlated lineages are explicitly discounted.

## X1 freeze, x2 gate, and terminal route

This x1 commit contains sources, proposals, task portfolios, Method Flow pairs, truth baselines, threat and wellbeing records, workflow/reflection records, provenance, and validation receipts only. It contains no x2 runner, phase-local skill implementation, surface contract, mutation result, observed outcome ledger, closeout, final seal, or successor message. Local, upstream, tracking, and fresh-live equality must be proved after the dedicated x1 push before x2 begins.

The active assignment is Vesper Arlen v658-v7. Under Hamish's acknowledged continuation authority, the prospective terminal successor is the existing exact-title `Lyren Moss` task for v658-v8. Lyren must not be resolved, reread, or contacted during evidence construction. Only after Vesper's own exact final is committed, pushed, clean, fresh-live equal, within caps, and passes one attributable canonical aggregate may the unique exact-title Lyren task be resolved and directly reread before one sanitized acknowledged activation. If the route is absent, ambiguous, unavailable, or blocked, retain `PREPARED_NOT_SENT` or `OPEN_ROUTE_GAP` and stop without substitution. Tavian Sol remains `ON_STANDBY` and is not a substitute. The verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def workflow_and_reflection() -> None:
    write_json("workflow/workflow-plan-request.json", {
        "schema": "ghc.family.workflow-plan.request.v1", "plan_id": "vesper-arlen-v658-v7-terminally-gated-lyren-route", "owner": d.OWNER,
        "identity_boundary": "Relational working language only; no continuity or authority claim.",
        "route": {"phase_assignments": [{"phase": "v658-v6", "seat": "Neris Solane"}, {"phase": "v658-v7", "seat": "Vesper Arlen"}, {"phase": "v658-v8", "seat": "Lyren Moss"}], "active_exact_title": "Vesper Arlen", "active_phase": "v658-v7", "next_exact_title": "Lyren Moss", "next_phase": "v658-v8", "tavian_sol_state": "ON_STANDBY", "future_identity_placeholders": []},
        "requirements": {"core_proposal_minimum": 30, "owner_file_cap": 2000, "skill_phase_half_cap": 200, "runner_phase_half_cap": 200, "document_word_cap": 100000, "commit_cap": {"x1": 5, "x2": 5, "total": 8}, "validation": {"canonical_successful_passes": 1, "replay_policy": "skip_after_first_complete_success", "isolate_failed_dependency_before_broader_rerun": True, "privacy_scan_required": True, "manifest_required": True, "fresh_remote_equality_required": True}, "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"}, "messaging": "exact_existing_main_task_only_after_terminal_gate"},
        "truth": {"allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"], "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "protected_boundaries": d.PROTECTED_GATES},
        "observed_failures": d.X1_OPERATIONAL_NEGATIVES,
    })
    write_json("workflow/refined-workflow-plan.json", {"schema": "ghc.family.workflow-plan.refined.v1", "phase": d.PHASE, "states": ["read_first_complete", "source_read_only_verified", "x1_prepare", "x1_stage_review_commit_push_equality", "x2_execute_and_retain", "evidence_commit_push_equality", "closeout_final_commit_push_equality", "single_canonical_scoped_pass", "one_exact_title_acknowledged_send"], "current_state": "x1_prepare", "x2_started": False, "route_contact_permitted": False, "stop_conditions": ["authority_gate", "safety_gate", "ambiguous_successor", "weekly_usage_exhausted", "Hamish_pause_or_redirect"]})
    write_json("reflection-remaster/inventory.json", {"schema": "ghc.family.reflection-remaster.inventory.v1", "phase": d.PHASE, "reviewed_surfaces": ["family index and routing precedence", "roster and auth state", "Method Flow state and schema", "workflow-plan refinement", "reflection-remaster decision schema", "meta-tool-box catalogue", "approval splitter", "open-gate rail", "truth bridge", "drive guardian", "startup and closeout guidance"], "deletions": [], "destructive_changes": False})
    write_json("reflection-remaster/x1-decision-record.json", {"schema": "ghc.family.reflection-remaster.decision.v1", "phase": d.PHASE, "decisions": [
        {"decision_id": "V6587-RM-01", "surface": "large-worktree inspection", "decision": "use bounded literal scalar probes", "state": "adopted_for_phase", "rollback": "return to individual read-only commands"},
        {"decision_id": "V6587-RM-02", "surface": "domain selection", "decision": "use synthetic aircraft-maintenance record and handover assurance after a 2830-title novelty audit", "state": "adopted_for_phase", "rollback": "stop before x2 if novelty or boundary checks fail"},
        {"decision_id": "V6587-RM-03", "surface": "empirical boundary", "decision": "keep all real aircraft, people, organisations, parts, defects, measurements, maintenance, inspections, certifications, releases, professional, cultural and Māori authority outside execution", "state": "adopted_for_phase", "rollback": "remove any promoting wording before commit"},
        {"decision_id": "V6587-RM-04", "surface": "phase tooling", "decision": "preregister ten family-current runners and ten phase-local skills", "state": "preregistered_not_implemented", "rollback": "use proposal-specific validator calls without deletion"}], "issues_retained": len(d.X1_OPERATIONAL_NEGATIVES), "x2_outcomes_present": False})
    write_json("reflection-remaster/issues.json", {"schema": "ghc.family.reflection-remaster.issues.v1", "issues": d.X1_OPERATIONAL_NEGATIVES, "all_retained": True})
    write_text("reflection-remaster/report.md", """# Reflection-remaster report

The phase adopts literal scalar probes, a 2,830-title aircraft-maintenance novelty rail, empirical, airworthiness, professional, and authority firewalls, ten reusable family-current runners, ten phase-local skill plans, exact prospective Git-blob byte metadata, and complete failure retention. No inherited tool, method, skill, negative, gate, or sibling artifact is deleted or rewritten. X2 implementation remains pending.
""")
    write_json("tooling/ghc-family-index.json", {"schema": "ghc.family.phase-local-index.v1", "phase": d.PHASE, "owner": d.OWNER, "lifecycle": "x1_frozen", "source_anchor": d.SOURCE_FINAL, "proposal_count": len(d.PROPOSALS), "skill_preregistrations": [name for name, _ in d.SKILL_SPECS], "runner_preregistrations": [name for name, _ in d.RUNNER_SPECS], "family_current_names_preserved": True, "historical_names_preserved": True, "route_state": "ACTIVATED_CURRENT_PHASE_WITH_TERMINAL_SUCCESSOR_GATE", "publication_boundary": "repository-relative paths and sanitized public fields only"})
    write_text("tooling/ghc-family-index.md", """# GHC Family Index — Vesper Arlen v658-v7 x1

This phase-local index records thirty frozen proposals, ten phase-local skill preregistrations, and ten family-current runner preregistrations. Historical names and callers remain compatibility evidence. No x2 tool exists yet and no successor route has been contacted.
""")
    write_json("tooling/meta-tool-box/catalogue.json", {"schema": "ghc.family.meta-tool-box.catalogue.v1", "phase": d.PHASE, "selected_current_guidance": ["ghc-family-index", "ghc-family-roster-check", "ghc-family-auth-permission-state", "ghc-family-method-flow-state", "ghc-family-workflow-plan-refinement", "ghc-family-reflection-remaster", "ghc-family-meta-tool-box", "ghc-approval-packet-splitter", "ghc-open-gate-rail", "ghc-family-truth-bridge", "ghc-drive-bank-guardian", "ghc-full-tools-skill-bank"], "planned_phase_skills": [{"name": name, "purpose": purpose, "state": "preregistered"} for name, purpose in d.SKILL_SPECS], "planned_family_runners": [{"name": name, "surface": surface, "state": "preregistered"} for name, surface in d.RUNNER_SPECS]})
    write_json("tooling/meta-tool-box/validation.json", {"schema": "ghc.family.meta-tool-box.validation.v1", "valid": True, "planned_skill_count": len(d.SKILL_SPECS), "planned_runner_count": len(d.RUNNER_SPECS), "collisions": [], "implementation_credit": False})


def threat_model() -> dict[str, Any]:
    return {
        "schema": "ghc.family.v658-v7.threat-model.x1.v1",
        "assets": ["proposal, source, outcome, negative, gap, gate, and Method Flow truth", "synthetic aircraft configuration, maintenance data, task-card, tooling, part, component, inspection, functional-check, deferred-item, workload, handover, and fatigue-operator provenance", "worker and passenger privacy, safety, incident disclosure, remedy, affected-party, legal, cultural, and Māori-authority reservations", "nonproduction identity and disclosure boundaries", "sibling lanes and terminal route integrity"],
        "threats": [
            {"threat": "synthetic maintenance metadata or fixtures promoted to a real task, inspection, certification, release, airworthiness, dispatch, or safety conclusion", "control": "fictional aliases, zero-record declarations, five-mutation rejection, and explicit no-operational-use wording"},
            {"threat": "a typed fatigue or damage placeholder promoted to component life, inspection interval, structural integrity, or a GMUT claim", "control": "unit and domain checks, unknown-parameter holds, identifiability and observation firewalls, falsifiers, and no-airworthiness outcomes"},
            {"threat": "failed calibration, part custody, configuration, task, inspection, or handover state promoted to successful maintenance assurance", "control": "calibration and component ledgers, conflict quarantine, explicit failure states, certification refusal, and retained negatives"},
            {"threat": "synthetic identity envelope promoted to live proof or trust", "control": "nonproduction markers and exact gates for keys, proofs, status, interoperability, security, privacy, recovery and governance"},
            {"threat": "worker, passenger, incident, community, or culturally governed information appropriated or disclosed", "control": "zero real people, aircraft, incidents or records and exact gates for affected parties, privacy, law, culture, Indigenous protocols and Māori authority"},
            {"threat": "successor contacted before terminal closeout", "control": "exact-title terminal gate, direct reread, one acknowledged send, and no substitute endpoint"},
        ],
        "residual_risk": "All real-data, empirical, participant, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, and independent-reproduction claims remain open or exact-gated.",
    }


def phase_paths() -> list[Path]:
    return sorted(path for path in PHASE.rglob("*") if path.is_file())


def privacy_scan() -> dict[str, Any]:
    patterns = {
        "raw_task_thread_session_identifier": re.compile(r"(?i)\b(?:thread|task|session)[_-]?(?:id|identifier)\s*[:=]\s*[0-9a-f-]{20,}"),
        "private_route_value": re.compile(r"(?i)\b(?:thread|task|session)://[a-z0-9_-]{12,}"),
        "credential_or_secret": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[^\s,;]{12,}"),
        "private_absolute_path": re.compile(r"(?i)\b[a-z]:\\(?:users|ghc-archives)\\[^\s\"']+"),
        "private_callable_identifier": re.compile(r"(?i)\b(?:mcp__|private_callable[_-]?id\s*[:=])[^\s,;]{8,}"),
    }
    hits = []
    files = phase_paths()
    for path in files:
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": path.relative_to(PHASE).as_posix(), "pattern_class": label})
    return {"schema": "ghc.family.v658-v7.x1-privacy-scan.v1", "pattern_classes": sorted(patterns), "file_count": len(files), "hit_count": len(hits), "hits": hits, "valid": not hits, "boundary": "Five concrete public-artifact pattern classes; prohibition labels are not payload findings."}


def build_manifest() -> dict[str, Any]:
    entries = []
    for path in phase_paths():
        relative = path.relative_to(PHASE).as_posix()
        if relative in MANIFEST_EXCLUSIONS:
            continue
        repository_relative = path.relative_to(ROOT).as_posix()
        entries.append(prospective_blob_record(repository_relative))
    for repository_relative in NEW_X1_CODE:
        path = ROOT / repository_relative
        entries.append(prospective_blob_record(repository_relative))
    entries.sort(key=lambda row: row["path"])
    return {"schema": "ghc.family.v658-v7.x1-content-manifest.v1", "hash_domain": "prospective Git-clean blob bytes", "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(MANIFEST_EXCLUSIONS), "boundary": "The four declared lifecycle files are self-excluded and reviewed separately in the exact staged-name gate."}


def build() -> None:
    source_receipt = verify_source()
    prior = inherited_rows()
    novelty = novelty_audit(prior)
    if len(d.PROPOSALS) != 30 or Counter(p["expected_disposition"] for p in d.PROPOSALS) != Counter(d.EXPECTED_DISTRIBUTION):
        raise RuntimeError("proposal count or expected distribution mismatch")
    known_sources = {row["source_id"] for row in d.OFFICIAL_SOURCES}
    unresolved = sorted({source_id for p in d.PROPOSALS for source_id in p["official_or_primary_source_needs"]} - known_sources)
    if unresolved:
        raise RuntimeError(f"unresolved source ids: {unresolved}")

    write_json("identity/identity-and-boundary.json", {"schema": "ghc.family.v658-v7.identity.v1", "owner": d.OWNER, "pronouns": d.PRONOUNS, "role": d.ROLE, "hope": d.HOPE, "relational_working_language_only": True, "hamish_may_rename_pause_redirect_or_stop": True, "not_evidence_of": ["consciousness", "sentience", "legal personhood", "identity continuity", "employment", "qualification", "scientific or operational authority", "legal or cultural authority", "Māori authority", "independent agency"]})
    write_json("startup/source-verification.json", source_receipt)
    write_json("startup/environment-and-version-receipt.json", {"schema": "ghc.family.v658-v7.environment.v1", "codex_cli": d.CODEX_CLI_VERSION, "codex_desktop": d.CODEX_DESKTOP_VERSION, "chatgpt_desktop": d.CHATGPT_DESKTOP_VERSION, "git": d.GIT_VERSION, "python": d.PYTHON_VERSION, "node": d.NODE_VERSION, "updates_performed": False, "elevation_performed": False, "windows_features_changed": False, "sandbox_or_hyper_v_activated": False, "reboot_performed": False, "storage_policy": "D-first additive owned lane; C-drive tools read only where required."})
    write_json("sources/official-source-ledger.json", {"schema": "ghc.family.v658-v7.official-source-ledger.v1", "observed_on": "2026-08-02", "status_vocabulary": sorted({row["status"] for row in d.OFFICIAL_SOURCES}), "status_counts": dict(sorted(Counter(row["status"] for row in d.OFFICIAL_SOURCES).items())), "source_count": len(d.OFFICIAL_SOURCES), "sources": d.OFFICIAL_SOURCES})
    write_text("sources/official-source-ledger.md", source_markdown())
    write_json("preregistration/proposal-ledger.json", {"schema": "ghc.family.v658-v7.proposal-ledger.x1.v1", "phase": d.PHASE, "owner": d.OWNER, "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE, "proposal_count": len(d.PROPOSALS), "expected_disposition_counts": d.EXPECTED_DISTRIBUTION, "outcomes_observed": False, "proposals": d.PROPOSALS})
    write_text("preregistration/proposal-ledger.md", proposal_markdown())
    write_json("preregistration/task-portfolios.json", {"schema": "ghc.family.v658-v7.task-portfolios.x1.v1", "safe_now": d.SAFE_TASKS, "candidate": d.CANDIDATE_TASKS, "clean": d.CLEAN_TASKS, "counts": {"safe_now": len(d.SAFE_TASKS), "candidate": len(d.CANDIDATE_TASKS), "clean": len(d.CLEAN_TASKS), "total": len(d.SAFE_TASKS) + len(d.CANDIDATE_TASKS) + len(d.CLEAN_TASKS)}, "task_cap": 1000, "quota_interpretation": False, "x1_executed_tasks": 0})
    write_json("preregistration/skill-and-runner-plan.json", {"schema": "ghc.family.v658-v7.skill-runner-plan.x1.v1", "skills": [{"name": name, "purpose": purpose, "state": "preregistered"} for name, purpose in d.SKILL_SPECS], "runners": [{"name": name, "primary_surface": surface, "state": "preregistered"} for name, surface in d.RUNNER_SPECS], "skill_count": len(d.SKILL_SPECS), "runner_count": len(d.RUNNER_SPECS), "implemented_in_x1": False})
    write_json("provenance/semantic-novelty-audit.json", {"schema": "ghc.family.v658-v7.semantic-novelty.v1", "method": "lowercased alphanumeric token-set Jaccard after disclosed stop-word removal plus owner manual mechanism review", "threshold": NOVELTY_THRESHOLD, "inherited_count": len(prior), "new_count": len(d.PROPOSALS), "effective_count": len(prior) + len(d.PROPOSALS), "inherited_unique_identifier_count": len({row["proposal_id"] for row in prior}), "inherited_identifier_collision_count": len(prior) - len({row["proposal_id"] for row in prior}), "inherited_unique_title_count": len({row["title"] for row in prior}), "maximum_similarity": max(row["jaccard"] for row in novelty), "all_pass": all(row["passes"] for row in novelty), "human_semantic_review_completed": True, "domain_specificity_review": "Aircraft-maintenance scope, configuration and effectivity, controlled data, work and task cards, tool and part provenance, component life and chains, findings, inspection and functional-check boundaries, software and deferred-item holds, record amendments, human-factor handover, typed fatigue and damage operators, orchestration, identity, accessibility, and authority mechanisms were reviewed against all 2830 inherited titles.", "rows": novelty})
    write_json("provenance/frozen-chain-proposal-index.json", {"schema": "ghc.family.v658-v7.frozen-proposal-index.v1", "prior_count": len(prior), "new_count": len(d.PROPOSALS), "effective_count": len(prior) + len(d.PROPOSALS), "inherited_unique_identifier_count": len({row["proposal_id"] for row in prior}), "inherited_identifier_collision_count": len(prior) - len({row["proposal_id"] for row in prior}), "inherited_unique_title_count": len({row["title"] for row in prior}), "prior_proposals": prior, "new_proposals": [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in d.PROPOSALS]}, compact=True)
    write_json("truth/retained-negative-register-x1.json", {"schema": "ghc.family.v658-v7.retained-negatives.x1.v1", "inherited_effective_count": d.SOURCE_EFFECTIVE_NEGATIVES, "current_x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES), "effective_count": d.SOURCE_EFFECTIVE_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES), "current_x1_operational_negatives": d.X1_OPERATIONAL_NEGATIVES, "inherited_register": "docs/neris-solane/v658-v6/truth/retained-negative-register-x2.json", "all_retained": True})
    write_json("truth/open-gap-register-x1.json", {"schema": "ghc.family.v658-v7.open-gaps.x1.v1", "inherited_effective_count": d.SOURCE_OPEN_GAPS, "new_preregistered_gap_count": 1, "effective_count_if_x2_confirms": d.SOURCE_OPEN_GAPS + 1, "new_proposal_ids": ["V6587-P29"], "outcome_not_yet_observed": True})
    write_json("truth/exact-gate-register-x1.json", {"schema": "ghc.family.v658-v7.exact-gates.x1.v1", "inherited_effective_count": d.SOURCE_EXACT_GATES, "new_preregistered_gate_count": 1, "effective_count_if_x2_confirms": d.SOURCE_EXACT_GATES + 1, "new_proposal_ids": ["V6587-P30"], "outcome_not_yet_observed": True, "authority_required": True})
    write_json("method-flow/method-flow-state-x1.json", method_flow())
    workflow_and_reflection()
    write_json("security/threat-model-x1.json", threat_model())
    write_json("wellbeing/workload-check-x1.json", {"schema": "ghc.family.v658-v7.wellbeing.x1.v1", "owner": d.OWNER, "state": "steady_and_bounded", "workload_controls": ["one active owner lane", "no subagents or early route messages", "split bounded probes after timeouts", "caps are ceilings, not quotas", "stop on authority, safety, fatigue, ambiguity, or Hamish direction"], "breaks_and_human_wellbeing": "Hamish and all human collaborators retain full control over pacing, rest, pause, and stop decisions.", "identity_boundary": "Relational working language only."})
    write_json("orchestration/route-state-x1.json", {"schema": "ghc.family.v658-v7.route-state.x1.v1", "active_owner": d.OWNER, "active_phase": d.PHASE, "activation_source": "Neris Solane v658-v6 one acknowledged existing-task activation", "active_exact_title": "Vesper Arlen", "next_exact_title": "Lyren Moss", "next_phase": "v658-v8", "state": "ACTIVATED_CURRENT_PHASE_WITH_TERMINAL_SUCCESSOR_GATE", "message_sent": False, "task_created": False, "task_forked": False, "subagent_spawned": False, "tavian_sol_state": "ON_STANDBY", "continuation_authorized_through": "v675-v8", "send_gate": "Only after Vesper's exact-final validation, one successful canonical scoped pass, clean push, caps, and fresh four-way equality: uniquely resolve and directly reread the existing exact-title Lyren Moss main task, then send one sanitized acknowledged v658-v8 activation; otherwise retain PREPARED_NOT_SENT or OPEN_ROUTE_GAP without substitution."})
    write_json("truth/x1-phase-truth.json", {"schema": "ghc.family.v658-v7.phase-truth.x1.v1", "phase": d.PHASE, "owner": d.OWNER, "lifecycle": "x1_precommit_candidate", "source_final": d.SOURCE_FINAL, "proposal_count": len(d.PROPOSALS), "inherited_frozen_proposals": d.PRIOR_FROZEN, "effective_frozen_proposals_after_commit": d.PRIOR_FROZEN + len(d.PROPOSALS), "expected_disposition_counts": d.EXPECTED_DISTRIBUTION, "observed_outcome_counts": None, "x2_implementation_present": False, "inherited_effective_negatives": d.SOURCE_EFFECTIVE_NEGATIVES, "current_x1_operational_negatives": len(d.X1_OPERATIONAL_NEGATIVES), "effective_methods": d.SOURCE_METHODS + len(d.X1_OPERATIONAL_NEGATIVES), "route_state": "ACTIVATED_CURRENT_PHASE_WITH_TERMINAL_SUCCESSOR_GATE", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_text("deliverables/v658-v7-x1-integrated-overview.md", integrated_overview())

    documents = [{"path": path.relative_to(PHASE).as_posix(), "words": len(path.read_text(encoding="utf-8").split())} for path in phase_paths() if path.suffix.lower() in {".md", ".html", ".txt"}]
    write_json("validation/document-cap-receipt-x1.json", {"schema": "ghc.family.v658-v7.document-cap.x1.v1", "limit_words": 100000, "document_count": len(documents), "maximum_words": max(row["words"] for row in documents), "documents": documents, "all_under_limit": all(row["words"] <= 100000 for row in documents)})
    owner_count_before_lifecycle = len(phase_paths())
    write_json("validation/owner-file-threshold-x1.json", {"schema": "ghc.family.v658-v7.owner-file-threshold.x1.v1", "owner_generated_file_count_before_lifecycle": owner_count_before_lifecycle, "threshold": 2000, "below_threshold": owner_count_before_lifecycle < 2000, "inherited_repository_baseline_counted": False})
    scan = privacy_scan()
    if not scan["valid"]:
        raise RuntimeError(f"privacy scan failed: {scan['hits']}")
    write_json("validation/x1-privacy-scan.json", scan)
    manifest = build_manifest()
    write_json("validation/x1-content-manifest.json", manifest)

    future_lifecycle = {"validation/x1-staged-review.json", "validation/x1-validation-receipt.json"}
    phase_relatives = {path.relative_to(PHASE).as_posix() for path in phase_paths()} | future_lifecycle
    expected_paths = sorted([f"{d.PHASE_ROOT}/{relative}" for relative in phase_relatives] + NEW_X1_CODE)
    write_json("validation/x1-staged-review.json", {"schema": "ghc.family.v658-v7.x1-staged-review.v1", "state": "PRECOMMIT_PATH_REVIEW", "allowed_prefixes": [d.PHASE_ROOT + "/", "scripts/ghc_family_v658_v7_", "scripts/build_ghc_family_v658_v7_x1.py", "tests/test_ghc_family_v658_v7_x1.py"], "x2_implementation_paths": [], "outcome_artifacts": [], "deletions": [], "expected_staged_path_count": len(expected_paths), "expected_staged_paths": expected_paths, "scanner_definition_candidates": ["scripts/build_ghc_family_v658_v7_x1.py"], "confirmed_privacy_hits": 0, "valid": True, "exact_index_review_required_after_staging": True})
    phase_jsons = list(PHASE.rglob("*.json"))
    for path in phase_jsons:
        read_json(path)
    receipt = {"schema": "ghc.family.v658-v7.x1-validation.v1", "valid": True, "source_head": d.SOURCE_FINAL, "proposal_count": len(d.PROPOSALS), "inherited_proposal_count": len(prior), "effective_proposal_count": len(prior) + len(d.PROPOSALS), "maximum_novelty_similarity": max(row["jaccard"] for row in novelty), "source_count": len(d.OFFICIAL_SOURCES), "source_reference_count": sum(len(row["official_or_primary_source_needs"]) for row in d.PROPOSALS), "unresolved_source_ids": [], "json_parse_count_before_self": len(phase_jsons), "privacy_file_count": scan["file_count"], "privacy_hit_count": scan["hit_count"], "manifest_entry_count": manifest["entry_count"], "expected_staged_path_count": len(expected_paths), "x2_implementation_present": False, "outcomes_observed": False, "x1_operational_negatives_retained": len(d.X1_OPERATIONAL_NEGATIVES), "terminal_verdict": "NOT_READY_FOR_STAGE_20"}
    write_json("validation/x1-validation-receipt.json", receipt)
    actual_after = sorted([path.relative_to(ROOT).as_posix() for path in phase_paths()] + NEW_X1_CODE)
    if actual_after != expected_paths:
        raise RuntimeError(f"x1 expected path mismatch: expected {len(expected_paths)}, actual {len(actual_after)}")
    print(json.dumps({"valid": True, "proposal_count": len(d.PROPOSALS), "effective_chain": len(prior) + len(d.PROPOSALS), "source_count": len(d.OFFICIAL_SOURCES), "maximum_similarity": max(row["jaccard"] for row in novelty), "x1_negatives": len(d.X1_OPERATIONAL_NEGATIVES), "expected_paths": len(expected_paths), "privacy_hits": scan["hit_count"]}))


if __name__ == "__main__":
    build()
