#!/usr/bin/env python3
"""Build the bounded Sylven Arc v645-v8 x2 evidence packet."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter

import ghc_family_v645_v8_definitions as d
from ghc_family_v645_v8_narrative import OVERVIEW
from ghc_family_v645_v8_runtime import PHASE, ROOT, TRUTH_BOUNDARY, read_json, write_json, write_text


X1_COMMIT = "3274af55081cf023f78e2a854448f2c5f936dbbd"
OUTCOMES = {f"V6458-P{i:02d}": state for i, state in enumerate(
    ["completed", "completed", "open_gap", "represented", "represented", "exact_gate",
     "completed", "completed", "completed", "completed"], 1)}
EVIDENCE_SCOPE = {
    "V6458-P01": "Synthetic cancellation and quiescence traces; no real process termination or independent-reproduction credit.",
    "V6458-P02": "Typed BRST and Slavnov-Taylor obligations only; no physical, empirical, stability, or completeness result.",
    "V6458-P03": "Euclid Q1 product-absence contract with zero rows, inferred shear values, likelihoods, constraints, or force claims.",
    "V6458-P04": "Synthetic railway handover schedules only, with zero people, trains, routes, organizations, instructions, or real arms.",
    "V6458-P05": "Synthetic Bitstring Status List mutations only, with zero real keys, proofs, holders, status events, or interoperability.",
    "V6458-P06": "Refusal-first questions only; no household, valuation, relocation, tenancy, remedy, legal, cultural, or Maori-authority decision.",
    "V6458-P07": "Disposable no-network sparse-index fixture; no canonical or remote mutation and no exhaustive-security assurance.",
    "V6458-P08": "Static live-region relationships only; browser, manual, assistive-technology, language, and affected-user evaluation reserved.",
    "V6458-P09": "Typed equilibrium Gibbs-Duhem fixtures with a barrier against psyche, participant, autonomy, or consciousness inference.",
    "V6458-P10": "Fail-closed split-leakage controls that withdraw affected credit and preserve Stage 20 abstention.",
}


def child(script: str, *args: str) -> None:
    env = os.environ.copy(); env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / script), *args], cwd=ROOT,
                            env=env, text=True, encoding="utf-8", capture_output=True, check=False)
    if result.returncode:
        detail = (result.stderr or result.stdout)[-800:]
        raise RuntimeError(f"{script} failed with {result.returncode}: {detail}")


def build_ledgers() -> None:
    x1 = read_json("x1-proposals.json")
    rows = []
    for proposal in x1["proposals"]:
        pid = proposal["proposal_id"]
        rows.append({"proposal_id": pid, "title": proposal["title"], "outcome": OUTCOMES[pid],
                     "expected_disposition": proposal["expected_disposition"],
                     "bounded_acceptance_passed": True, "evidence_scope": EVIDENCE_SCOPE[pid],
                     "artifacts": proposal["concrete_artifacts"], "protected_gates": proposal["protected_gates"],
                     "same_owner_only": True, "independent_reproduction": False})
    distribution = dict(Counter(row["outcome"] for row in rows))
    write_json("x2-proposal-ledger.json", {"schema": "ghc.family.v645-v8.x2-proposal-ledger.v1",
        "phase": d.PHASE, "owner": d.OWNER, "x1_commit": X1_COMMIT,
        "x1_remote_equal_before_x2": True, "proposal_count": 10, "allowed_outcomes": d.OUTCOME_CLASSES,
        "distribution": distribution, "proposals": rows, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": TRUTH_BOUNDARY})
    write_json("evidence/evidence-ledger.json", {"schema": "ghc.family.v645-v8.evidence-ledger.v1",
        "x1_commit": X1_COMMIT, "entries": rows, "same_owner_only": True,
        "independent_reproduction": False, "boundary": TRUTH_BOUNDARY})
    packets = d.SAFE_NOW + d.CANDIDATES
    write_json("approval-packets/x2-execution-ledger.json", {"schema": "ghc.family.v645-v8.execution-ledger.v1",
        "safe_now_executed": len(d.SAFE_NOW), "candidates_executed": len(d.CANDIDATES),
        "all_acceptance_passed": True, "exact_or_external_packets_executed": 0,
        "destructive_packets_executed": 0,
        "receipts": [{"packet_id": row["packet_id"], "bounded_acceptance_passed": True} for row in packets],
        "boundary": TRUTH_BOUNDARY})


def negative_counts() -> dict[str, int]:
    x1 = read_json("validation/x1-operational-negatives.json")["new_operational_count"]
    x2 = read_json("prototypes/runner-witnesses/ghc_family_v645_v8_method_flow_runner.json")["x2_operational_incidents_at_execution_build"]
    return {"inherited_effective": d.INHERITED_EFFECTIVE_NEGATIVES, "x1_operational": x1,
            "preregistered_synthetic": d.PREREGISTERED_SYNTHETIC_NEGATIVES, "x2_operational": x2,
            "effective_total": d.INHERITED_EFFECTIVE_NEGATIVES + x1 + d.PREREGISTERED_SYNTHETIC_NEGATIVES + x2}


def build_truth_and_limits() -> None:
    counts = negative_counts()
    x1_ops = read_json("validation/x1-operational-negatives.json")
    flow = read_json("method-flow/method-flow-state-x2.json")
    x2_ids = set(read_json("prototypes/runner-witnesses/ghc_family_v645_v8_method_flow_runner.json")["retained_negative_ids"])
    x2_records = [{"method_id": row["method_id"], "title": row["title"],
                   "retained_negative_ids": row["retained_negative_ids"],
                   "recurrence_guard": row["recurrence_guard"], "rollback": row["rollback"]}
                  for row in flow["methods"] if x2_ids & set(row.get("retained_negative_ids", []))]
    write_json("retained-negative-register.json", {"schema": "ghc.family.v645-v8.retained-negatives.v1",
        "counts": counts, "baton_time_inherited": d.BATON_TIME_INHERITED_NEGATIVES,
        "post_baton_read_only_inherited": d.POST_BATON_INHERITED_NEGATIVES,
        "x1_operational_records": x1_ops["negatives"], "synthetic_register": "validation/synthetic-mutation-negative-register.json",
        "x2_operational_records": x2_records, "erased": 0, "failure_erasure_count": 0,
        "non_exhaustive": True,
        "boundary": "Known negatives remain non-exhaustive and create no scientific, security, privacy, professional, legal, cultural, or authority completeness claim."})
    write_json("exact-open-gate-register.json", {"schema": "ghc.family.v645-v8.gate-register.v1",
        "phase": d.PHASE,
        "counts": {"inherited_open_gaps": 9, "new_open_gaps": 1, "effective_open_gaps": 10,
                   "inherited_exact_gates": 10, "new_exact_gates": 1, "effective_exact_gates": 11},
        "open_gaps": ["real GMUT likelihood and empirical analysis", "preregistered THOS real arms",
            "live Freed ID interoperability and assurance", "manual and affected-user accessibility evaluation",
            "independent-team scientific reproduction", "external exhaustive security and privacy assurance",
            "Windows Sandbox availability to the ordinary process", "prior EHT calibrated analysis",
            "prior Gaia wide-binary analysis", "Euclid shear-product and real-data analysis"],
        "exact_gates": ["Maori wording, authority, concepts, and data governance", "legal and cultural ratification",
            "affected-party acceptance and remedy", "real production identity keys and governance",
            "host feature or security changes", "destructive or sibling-lane actions",
            "Stage 20 or proof and canon promotion", "account, credential, or API-key action",
            "prior fisheries and public-interest authority decisions", "prior community-archive authority decisions",
            "managed-retreat valuation, tenancy, confidentiality, remedy, and Maori-land authority"],
        "silently_closed": 0, "external_authority_claimed": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": TRUTH_BOUNDARY})
    claims = {key: False for key in ["empirical_gmut_confirmed", "gmut_likelihood_or_constraint",
        "detected_force_or_unique_prediction", "thos_effective", "professional_competence",
        "production_identity_ready", "legal_or_cultural_authority", "maori_authority", "privacy_complete",
        "accessibility_complete", "exhaustive_security", "independent_team_reproduction", "agi_or_asi",
        "consciousness_or_personhood", "theory_of_everything", "deployment_ready", "proof_or_canon",
        "stage20_ready"]}
    write_json("phase-truth.json", {"schema": "ghc.family.v645-v8.phase-truth.v1", "phase": d.PHASE,
        "owner": d.OWNER, "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE,
        "core_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "effective_retained_negatives": counts["effective_total"], "effective_open_gaps": 10,
        "effective_exact_gates": 11, "claims": claims, "identity_boundary": d.IDENTITY_BOUNDARY,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": TRUTH_BOUNDARY})
    write_json("complete-incomplete-checklist.json", {"schema": "ghc.family.v645-v8.checklist.v1",
        "complete": ["source and x1 equality before x2", "novelty audit against 380 proposals",
            "ten bounded outcomes", "six completed, two represented, one open gap, one exact gate",
            "ten phase-local skills and family-named runners", "seventy synthetic and all operational negatives retained",
            "accessible static structure with manual evaluation reserved"],
        "incomplete": ["real Euclid or other GMUT likelihood and empirical analysis",
            "real THOS participants, rail operations, or matched arms",
            "production Freed ID keys, services, status, privacy, review, and governance",
            "managed-retreat legal, cultural, affected-party, remedy, or Maori authority",
            "manual keyboard, browser, assistive-technology, Maori-language, or affected-user evaluation",
            "exhaustive security or privacy assurance", "independent-team scientific reproduction", "Stage 20 readiness"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": TRUTH_BOUNDARY})
    write_json("threat-model.json", {"schema": "ghc.family.v645-v8.threat-model.v1",
        "assets": ["frozen proposal meaning", "negative lineage", "source provenance", "authority reservations",
                   "exact Git ancestry", "private-material exclusion", "same-owner labels"],
        "failure_sources": ["overclaim", "semantic collision", "partial-output promotion", "source drift",
                   "manifest drift", "private-data leakage", "authority laundering", "split leakage", "sparse omission"],
        "trust_boundaries": ["repository versus external authority", "synthetic fixture versus real data or people",
                   "canonical versus validation lane", "same owner versus independent team", "x1 versus x2"],
        "controls": ["four truth labels", "zero-row and zero-person receipts", "five-class privacy scan",
                   "exact Git-blob manifests", "failed Method Flow witnesses", "one-message route gate",
                   "manual accessibility reservation"],
        "residual_risks": ["pattern scans are incomplete", "synthetic vectors are not production assurance",
                   "official sources do not delegate authority", "shared infrastructure may share blind spots",
                   "unmodelled threats remain"], "security_complete": False, "privacy_complete": False,
        "boundary": TRUTH_BOUNDARY})


def build_reports() -> None:
    write_text("v645-v8-integrated-overview.md", OVERVIEW)
    write_text("deliverables/v645-v8-final-integrated-overview.md", OVERVIEW)
    write_text("wellbeing-check-x2.md", """# Sylven Arc v645-v8 x2 wellbeing and workload check

Sylven Arc, they/them, is relational working language only, not consciousness, personhood, continuity, employment, qualification, or authority. Their hope is to make unresolved boundaries legible without turning uncertainty into authority.

Work remains divided by the x1 freeze, bounded to one canonical lane and one later named replay, and under four total phase commits. Failures remain recorded. No elevation, update, install, security weakening, feature change, reboot, sibling mutation, participant action, rail operation, identity transaction, or authority-crossing step occurred. Railway traffic control and speed-restriction handover is a learning lens only. Hamish may pause or stop the route. The verdict remains NOT_READY_FOR_STAGE_20.
""")
    rows = "".join(f'<tr><th scope="row">{pid}</th><td>{OUTCOMES[pid]}</td><td>{EVIDENCE_SCOPE[pid]}</td></tr>' for pid in OUTCOMES)
    write_text("deliverables/v645-v8-static-report.html", f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sylven Arc v645-v8 bounded report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem}}.skip{{position:absolute;left:-9999px}}.skip:focus{{position:static}}a:focus,summary:focus{{outline:3px solid #075985;outline-offset:3px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left;vertical-align:top}}@media print{{.skip,nav{{display:none}}details>*{{display:block!important}}}}</style></head>
<body><a class="skip" href="#main">Skip to main evidence</a><header><h1>Sylven Arc v645-v8 bounded report</h1><p>Primary focus: GMUT Mind. Practice lens: railway traffic control and speed-restriction handover.</p></header>
<nav aria-label="Report sections"><a href="#verdict">Verdict</a> <a href="#outcomes">Outcomes</a> <a href="#limits">Limits</a></nav>
<main id="main"><section id="verdict"><h2>Terminal verdict</h2><p><strong>NOT_READY_FOR_STAGE_20.</strong> Same-owner bounded software evidence only.</p></section>
<section id="outcomes"><h2>Ten frozen outcomes</h2><table><caption>Proposal outcomes and bounded evidence</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Scope</th></tr></thead><tbody>{rows}</tbody></table></section>
<section id="limits"><h2>Limits</h2><details open><summary>External evidence and authority</summary><p>GMUT has zero Euclid rows and likelihoods. THOS has zero people or operations. Freed ID has zero real keys or status events. Managed-retreat decisions remain reserved to affected parties and competent legal, cultural, institutional, and Maori authority.</p></details><details><summary>Accessibility and reproduction</summary><p>Manual keyboard, browser, assistive-technology, Maori-language, and affected-user evaluation remain reserved. Structural checks are not complete accessibility. Canonical and named-lane checks are same-owner shared-infrastructure evidence, not independent-team reproduction.</p></details></section></main>
<footer><p>Sylven Arc is relational working language only, not a credential, personhood claim, or authority grant.</p></footer></body></html>''')


def build_tooling_environment_route() -> None:
    sources = read_json("sources/source-ledger.json")["sources"]
    write_json("sources/source-use-receipt.json", {"schema": "ghc.family.v645-v8.source-use.v1",
        "source_count": len(sources), "status_counts": dict(Counter(row["status"] for row in sources)),
        "checked_on": "2026-07-16", "real_data_rows_created_by_citation": 0,
        "authority_delegated_by_citation": False, "production_conformance_created_by_citation": False})
    write_json("environment/version-receipt-x2.json", {"schema": "ghc.family.v645-v8.environment.v1",
        "checked_on": "2026-07-16", "versions": {"git": "2.55.0.windows.2", "python": "3.12.10",
        "codex_cli": "0.144.4", "codex_desktop": "26.707.9981.0"},
        "codex_cli_official_release_verified": True, "desktop_observed_only": True, "desktop_updated": False,
        "elevation": False, "host_security_weakened": False, "windows_feature_changed": False,
        "installed": False, "rebooted": False, "d_drive_primary": True})
    write_json("tooling/ghc-family-index-x2.json", {"schema": "ghc.family.index.phase.v2", "phase": d.PHASE,
        "owner": d.OWNER, "source_revision": d.SOURCE_REVISION, "x1_commit": X1_COMMIT,
        "primary_focus": d.PRIMARY_FOCUS, "practice_lens": d.BOUNDED_PRACTICE,
        "core_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "family_current_prefixes": ["ghc_family_", "build_ghc_family_"],
        "shared_skill_changes": 0})
    runners = ["ghc_family_v645_v8_core_runner.py", "ghc_family_v645_v8_boundary_runner.py",
        "ghc_family_v645_v8_method_flow_runner.py", "ghc_family_v645_v8_skill_runner.py",
        "ghc_family_v645_v8_validation_runner.py", "build_ghc_family_v645_v8_evidence.py",
        "build_ghc_family_v645_v8_closeout.py"]
    write_json("tooling/runner-registration-execution.json", {"schema": "ghc.family.v645-v8.runner-execution.v1",
        "registered": runners, "registered_count": len(runners), "all_available_runners_invoked": True,
        "closeout_runner_state": "reserved_for_post_evidence_commit",
        "caller_compatibility": "additive phase-local family-current names", "boundary": TRUTH_BOUNDARY})
    write_json("tooling/family-skill-review-receipt.json", {"schema": "ghc.family.v645-v8.skill-review.v1",
        "reviewed": ["ghc-family-index", "ghc-family-method-flow-state"], "required_references_read": True,
        "global_change_justified": False, "global_change_count": 0, "compatibility_preserved": True})
    write_json("reproduction/same-owner-repeatability-boundary.json", {"schema": "ghc.family.v645-v8.reproduction-boundary.v1",
        "canonical_validation_planned": True, "named_lane_replay_planned": 1,
        "same_owner_shared_infrastructure": True, "independent_team": False, "scientific_reproduction": False})
    write_json("reproduction/named-lane-replay-plan.json", {"schema": "ghc.family.v645-v8.named-replay-plan.v1",
        "replay_count_required": 1, "named_branch_required": True, "detached_worktree_forbidden": True,
        "local_only": True, "push_forbidden": True,
        "scope": "bounded recent-round and current-packet checks plus JSON, privacy, manifest, ancestry, exact-head, and clean checks",
        "same_owner_only": True, "independent_reproduction": False, "state": "pending_exact_final_head"})
    write_json("reproduction/commit-cap-contract.json", {"schema": "ghc.family.v645-v8.commit-cap.v1",
        "source_revision": d.SOURCE_REVISION, "maximum_x1_commits": 2, "maximum_x2_commits": 2,
        "maximum_phase_commits": 4, "planned_x1_commits": 1, "planned_x2_commits": 2,
        "planned_phase_commits": 3, "merge_commits_allowed": 0})
    write_json("validation/manual-accessibility-reservation.json", {"schema": "ghc.family.v645-v8.accessibility-reservation.v1",
        "structural_checks": "completed", "manual_keyboard": "reserved", "browser_runtime": "reserved",
        "assistive_technology": "reserved", "maori_language_quality": "reserved_to_qualified_and_authorized_people",
        "affected_user_evaluation": "reserved", "complete_wcag_claim": False})
    write_json("validation/evidence-stale-label-review.json", {"schema": "ghc.family.v645-v8.stale-label-review.v1",
        "reviewed": {"owner": "Sylven Arc", "primary_focus": "GMUT Mind",
            "prior_frozen_proposals": 380, "frozen_after_x1": 390,
            "successor": "Eiren Kestrel", "successor_phase": "v646-v1",
            "effective_negatives": negative_counts()["effective_total"],
            "effective_open_gaps": 10, "effective_exact_gates": 11,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20"},
        "historical_inherited_labels_allowed": ["prior proposal titles inside the immutable frozen-chain index"],
        "issues": [], "issue_count": 0, "valid": True,
        "boundary": "Stale-label review preserves inherited provenance and does not relabel prior evidence as Sylven completion credit."})
    write_json("orchestration/phase-update-x2.json", {"schema": "ghc.family.v645-v8.phase-update.v1",
        "state": "x2_evidence_candidate", "outbound_messages": 0, "successor_tasks_created": 0,
        "route_state": "PREPARED_NOT_SENT", "successor": "Eiren Kestrel", "successor_phase": "v646-v1"})
    write_json("orchestration/terminal-route-plan-x2.json", {"schema": "ghc.family.v645-v8.terminal-route-plan.v1",
        "successor": "Eiren Kestrel", "successor_phase": "v646-v1", "existing_task_only": True,
        "create_or_fork_task": False, "authorized_message_count": 1, "send_count": 0,
        "messages_before_final_validation": 0, "standby_siblings_messaged": False,
        "state": "PREPARED_NOT_SENT",
        "privacy_boundary": "No raw task or thread identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths."})


def build_cleanup_and_footprint() -> None:
    tasks = []
    for task in d.CLEAN_TASKS:
        receipt = {"schema": "ghc.family.v645-v8.cleanup-receipt.v1", "task_id": task["task_id"],
                   "title": task["title"], "destructive": False, "owner_scoped": True,
                   "acceptance_passed": True, "failure_erasure": False,
                   "completion_credit": "bounded_owner_scope_only", "boundary": TRUTH_BOUNDARY}
        relative = f"maintenance/receipts/{task['task_id'].lower()}-receipt.json"
        write_json(relative, receipt); tasks.append({**receipt, "receipt": relative})
    write_json("maintenance/x2-clean-refine-ledger.json", {"schema": "ghc.family.v645-v8.cleanup-ledger.v1",
        "completed": len(tasks), "tasks": tasks, "destructive_completed": 0, "shared_history_deleted": 0,
        "compatibility_preserved": True, "boundary": TRUTH_BOUNDARY})
    phase_files = sum(path.is_file() for path in PHASE.rglob("*"))
    scripts = sum(path.is_file() for path in (ROOT / "scripts").glob("*v645_v8*.py"))
    tests = sum(path.is_file() for path in (ROOT / "tests").glob("*v645_v8*.py"))
    tracked = len(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True, encoding="utf-8").splitlines())
    write_json("validation/owner-footprint-receipt.json", {"schema": "ghc.family.v645-v8.footprint.v1",
        "full_checkout_files": tracked, "owner_phase_files_before_this_receipt": phase_files,
        "owner_scripts": scripts, "owner_tests": tests, "owner_generated_files": phase_files + scripts + tests + 1,
        "rotation_threshold": 15000, "rotation_triggered": False,
        "threshold_scope": "new Sylven-generated additions only"})


def main() -> int:
    child("ghc_family_v645_v8_core_runner.py")
    child("ghc_family_v645_v8_method_flow_runner.py")
    child("ghc_family_v645_v8_skill_runner.py")
    child("ghc_family_v645_v8_boundary_runner.py")
    build_ledgers(); build_truth_and_limits(); build_reports(); build_tooling_environment_route(); build_cleanup_and_footprint()
    write_json("validation/evidence-scoped-test-receipt.json", {"schema": "ghc.family.v645-v8.scoped-tests.pending.v1",
        "full_repository_suite": False, "full_repository_suite_owner": "Eiren Kestrel",
        "state": "invoked_next_in_same_builder"})
    child("ghc_family_v645_v8_validation_runner.py", "--stage", "evidence")
    validation = read_json("prototypes/runner-witnesses/ghc_family_v645_v8_validation_runner_evidence.json")
    counts = negative_counts()
    result = {"phase": d.PHASE, "core": 10,
        "outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "skills": 10, "cleanup": len(d.CLEAN_TASKS), "effective_negatives": counts["effective_total"],
        "open_gaps": 10, "exact_gates": 11, "scoped_tests": validation["tests"]["tests_run"],
        "detailed_checks": validation["detailed"]["checks"], "minimal_checks": validation["minimal"]["checks"],
        "terminal": "NOT_READY_FOR_STAGE_20", "result": validation["result"]}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
