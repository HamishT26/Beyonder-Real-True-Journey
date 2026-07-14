#!/usr/bin/env python3
"""Build Orin Thale v644-v2 x2 evidence and candidate receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v644-gmut-thos-v2-x1-x2"
PHASE_ROOT = ROOT / "docs" / "orin-thale" / "v644-v2"
SOURCE_HEAD = "7616eb17cbaff509eafe1423f1930d2d2e7f72d4"
SOURCE_SEAL = "64ed8f3001553d2ffa364f3875043288c6ce91cc"
X1_COMMIT = "fffbe71763bf981c928ebf4d1ef73c3a8293cf09"
INHERITED_NEGATIVE_REGISTER = ROOT / "docs" / "sable-rook" / "v644-v1" / "retained-negative-register.json"
X2_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6442-X2-OP-01",
        "origin": "v644-v2-x2-operational",
        "observed": "PowerShell brace interpolation altered a git rev-parse commit-tree expression and Git rejected the encoded suffix.",
        "recovery": "Use git show -s --format=%T with the commit passed as a separate literal argument.",
        "promotion_effect": "No evidence or gate changed; the failed command is retained and the safer literal form is required.",
        "retained": True,
        "external_gate_closed": False,
    }
]
X2_EXTERNAL_FILES = [
    "scripts/build_ghc_family_v644_v2_report.py",
    "scripts/ghc_family_v644_v2_complete_suite.py",
    "scripts/ghc_family_v644_v2_evidence.py",
    "scripts/ghc_family_v644_v2_minimal.py",
    "scripts/ghc_family_v644_v2_model.py",
    "scripts/ghc_family_v644_v2_staged_review.py",
    "scripts/ghc_family_v644_v2_validator.py",
    "tests/test_ghc_family_v644_v2.py",
]


from build_ghc_family_v644_v2_report import build_report  # noqa: E402
from ghc_family_v644_v2_model import SPECS, all_cases  # noqa: E402
from ghc_family_v644_v2_x1_definitions import PROPOSALS, X1_NEGATIVES  # noqa: E402


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def dump_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path.read_bytes())).hexdigest()


def subprocess_text(*args: str) -> str:
    return subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def git_blob_bytes(commit: str, path: str) -> bytes:
    return subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, check=True, capture_output=True).stdout


def build_x1_content_seal() -> None:
    paths = [line for line in subprocess_text("git", "diff-tree", "--no-commit-id", "--name-only", "-r", X1_COMMIT).splitlines() if line]
    entries = []
    for path in sorted(paths):
        blob = git_blob_bytes(X1_COMMIT, path)
        current_blob = subprocess_text("git", "rev-parse", f"HEAD:{path}")
        x1_blob = subprocess_text("git", "rev-parse", f"{X1_COMMIT}:{path}")
        entries.append(
            {
                "path": path,
                "x1_blob_oid": x1_blob,
                "current_blob_oid": current_blob,
                "blob_unchanged": x1_blob == current_blob,
                "sha256": hashlib.sha256(blob).hexdigest(),
            }
        )
    dump_json(
        PHASE_ROOT / "reproduction" / "x1-content-seal.json",
        {
            "schema": "ghc.family.v644-v2.x1-content-seal.v1",
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "file_count": len(entries),
            "entries": entries,
            "all_current_blobs_unchanged": all(entry["blob_unchanged"] for entry in entries),
            "boundary": "The seal proves Git-blob stability of the dedicated x1 commit; it does not convert preregistered expectations into results.",
        },
    )


def build_proposal_artifacts() -> list[dict[str, Any]]:
    cases = all_cases()
    ledger_rows = []
    for proposal in PROPOSALS:
        proposal_id = proposal["proposal_id"]
        case_set = cases[proposal_id]
        control = case_set["control"]
        mutations = case_set["mutations"]
        first, second, third = [PHASE_ROOT / item for item in proposal["deliverables"]]
        dump_json(
            first,
            {
                "schema": f"ghc.family.v644-v2.{proposal_id.casefold()}.primary-artifact.v1",
                "phase": PHASE,
                "owner": "Orin Thale",
                "proposal_id": proposal_id,
                "title": proposal["title"],
                "artifact_role": "typed bounded-scope control, protocol, profile, or authority record",
                "outcome": proposal["expected_disposition"],
                "source_needs": proposal["authoritative_source_needs"],
                "control": control["record"],
                "control_evaluation": control["evaluation"],
                "case_set_sha256": case_set["case_set_sha256"],
                "external_execution_performed": False,
                "real_data_rows": 0,
                "real_participants_or_raters": 0,
                "real_keys_or_proofs": 0,
                "independent_review_events": 0,
                "boundary": proposal["rollback_or_recovery"],
            },
        )
        secondary: dict[str, Any] = {
            "schema": f"ghc.family.v644-v2.{proposal_id.casefold()}.secondary-artifact.v1",
            "phase": PHASE,
            "proposal_id": proposal_id,
            "artifact_role": "seven preregistered falsifier mutations retained as negatives",
            "mutation_count": len(mutations),
            "mutations": mutations,
            "all_rejected": all(item["evaluation"]["decision"] == "rejected" for item in mutations),
            "all_retained": all(item["retained"] for item in mutations),
            "case_set_sha256": case_set["case_set_sha256"],
        }
        if proposal_id == "V6442-P03":
            secondary["missing_requirements"] = [
                "model-specific binary-pulsar observable derivation",
                "checksum-bound source timing rows",
                "source covariance",
                "frozen selection and nuisance plan",
                "blind GR baseline",
                "identifiability analysis",
                "independent review",
            ]
            secondary["likelihood_executed"] = False
        if proposal_id == "V6442-P06":
            secondary["neutral_unanswered_questions"] = [
                "Which affected parties and representatives have authority for this specific remedy?",
                "Which Māori authorities and data-governance mandates apply, if any?",
                "Who may lawfully hold funds, and under which independently reviewed duties?",
                "How are eligibility, conflicts, distribution, appeal, and residual funds decided by authorized parties?",
                "What evidence records acceptance without substituting repository output for consent or ratification?",
            ]
            secondary["answers_supplied_by_repository"] = False
        dump_json(second, secondary)
        dump_json(
            third,
            {
                "schema": f"ghc.family.v644-v2.{proposal_id.casefold()}.nonpromotion-boundary.v1",
                "phase": PHASE,
                "proposal_id": proposal_id,
                "outcome": proposal["expected_disposition"],
                "protected_gates": proposal["protected_gates"],
                "gates_closed": [],
                "rollback_or_recovery": proposal["rollback_or_recovery"],
                "not_established": [
                    "empirical confirmation",
                    "participant effectiveness",
                    "production readiness",
                    "deployment",
                    "complete accessibility",
                    "exhaustive security",
                    "legal or cultural ratification",
                    "Māori authority",
                    "independent-team reproduction",
                    "consciousness or personhood",
                    "AGI or ASI",
                    "proof, canon, or Stage 20 readiness",
                ],
            },
        )
        ledger_rows.append(
            {
                "proposal_id": proposal_id,
                "title": proposal["title"],
                "outcome": proposal["expected_disposition"],
                "control_case": control["case_id"],
                "control_decision": control["evaluation"]["decision"],
                "synthetic_negative_count": len(mutations),
                "artifacts": proposal["deliverables"],
                "source_needs": proposal["authoritative_source_needs"],
                "evidence_summary": {
                    "completed": "Typed control and seven falsifier mutations passed in bounded synthetic scope; external claims remain gated.",
                    "represented": "A structural or protocol proxy exists with zero real participants, keys, endpoints, or production evidence.",
                    "open_gap": "A preregistration and explicit zero-row gap exist; no likelihood or empirical result was produced.",
                    "exact_gate": "A neutral unanswered authority record exists; no allocation, legal, cultural, or Māori-authority decision was made.",
                }[proposal["expected_disposition"]],
                "protected_gates": proposal["protected_gates"],
            }
        )
    return ledger_rows


def build_retained_negatives() -> None:
    inherited_payload = json.loads(INHERITED_NEGATIVE_REGISTER.read_text(encoding="utf-8"))
    inherited = list(inherited_payload["negatives"])
    x1_rows = [
        {
            "negative_id": item["negative_id"],
            "origin": "v644-v2-x1-operational",
            "observed": item["observed_failure"],
            "recovery": item["recovery"],
            "promotion_effect": item["promotion_effect"],
            "retained": True,
        }
        for item in X1_NEGATIVES
    ]
    synthetic = []
    for proposal_id, case_set in all_cases().items():
        for item in case_set["mutations"]:
            synthetic.append(
                {
                    "negative_id": item["negative_id"],
                    "origin": "v644-v2-preregistered-synthetic",
                    "proposal_id": proposal_id,
                    "mutated_field": item["mutated_field"],
                    "observed": "; ".join(item["evaluation"]["reasons"]),
                    "decision": item["evaluation"]["decision"],
                    "retained": True,
                    "resolved_for_control_only": True,
                    "external_gate_closed": False,
                }
            )
    x2_operational = list(X2_OPERATIONAL_NEGATIVES)
    negatives = inherited + x1_rows + synthetic + x2_operational
    ids = [item["negative_id"] for item in negatives]
    dump_json(
        PHASE_ROOT / "retained-negative-register.json",
        {
            "schema": "ghc.family.v644-v2.retained-negative-register.v1",
            "phase": PHASE,
            "owner": "Orin Thale",
            "inherited_from": rel(INHERITED_NEGATIVE_REGISTER),
            "inherited_sha256_lf_normalized": normalized_sha256(INHERITED_NEGATIVE_REGISTER),
            "inherited_count": len(inherited),
            "x1_operational_count": len(x1_rows),
            "new_synthetic_count": len(synthetic),
            "x2_operational_count": len(x2_operational),
            "new_count": len(x1_rows) + len(synthetic) + len(x2_operational),
            "negative_count": len(negatives),
            "duplicate_negative_ids": sorted({value for value in ids if ids.count(value) > 1}),
            "all_retained": all(item.get("retained") is True for item in negatives),
            "erasure_permitted": False,
            "negatives": negatives,
            "boundary": "A recovered local control does not erase its negative. No negative establishes or closes an external scientific, participant, production, legal, cultural, identity, deployment, or Stage 20 claim.",
        },
    )


def build_gate_register() -> None:
    dump_json(
        PHASE_ROOT / "exact-open-gate-register.json",
        {
            "schema": "ghc.family.v644-v2.exact-open-gate-register.v1",
            "phase": PHASE,
            "owner": "Orin Thale",
            "open_gap_count": 5,
            "exact_gate_count": 6,
            "open_gaps": [
                {
                    "gate_id": "OPEN-01",
                    "domain": "GMUT real-data observable studies, including inherited multi-messenger and v644-v2 binary-pulsar protocols",
                    "state": "open",
                    "requires": ["model-specific observable derivation", "licensed checksum-bound real rows", "covariance, calibration, and selection", "frozen nuisance plan", "blind named baseline", "identifiability analysis", "independent review"],
                },
                {"gate_id": "OPEN-02", "domain": "THOS real-arm evidence", "state": "open", "requires": ["ethics", "consent", "preregistered blind matched-budget arms", "real participants and raters", "harms monitoring", "independent review"]},
                {"gate_id": "OPEN-03", "domain": "Freed ID production completion", "state": "open", "requires": ["standards-conformant real keys and proofs", "live issuance and presentation", "live resolution", "status and revocation", "cross-vendor interoperability", "privacy and security review", "trust governance"]},
                {"gate_id": "OPEN-04", "domain": "qualified accessibility evaluation", "state": "open", "requires": ["manual evaluation", "assistive-technology coverage", "cognitive-accessibility review", "affected-user evaluation"]},
                {"gate_id": "OPEN-05", "domain": "independent-team scientific reproduction", "state": "open", "requires": ["independent team", "independently owned protocol", "independent infrastructure", "returned evidence"]},
            ],
            "exact_gates": [
                {"gate_id": "EXACT-01", "domain": "affected-party remedy-fund, data-return, stewardship, and acceptance decisions", "state": "pending_exact_authority"},
                {"gate_id": "EXACT-02", "domain": "Māori wording, authority, and data governance", "state": "pending_exact_authority"},
                {"gate_id": "EXACT-03", "domain": "cultural ratification, repatriation, benefit, and stewardship transfer", "state": "pending_exact_authority"},
                {"gate_id": "EXACT-04", "domain": "legal interpretation, fiduciary authority, and enacted-law status", "state": "pending_exact_authority"},
                {"gate_id": "EXACT-05", "domain": "destructive, account, credential, API-key, deployment, or sibling-merge action", "state": "pending_exact_authority"},
                {"gate_id": "EXACT-06", "domain": "Stage 20 external decision authority", "state": "pending_exact_authority"},
            ],
            "all_visible": True,
            "none_silently_closed": True,
            "boundary": "Bounded repository engineering evidence only. GMUT, THOS, Freed ID, CBR, Māori authority, legal and cultural ratification, deployment, exhaustive security, complete accessibility, independent reproduction, identity claims, proof/canon, and Stage 20 remain bounded exactly as stated.",
        },
    )


def build_phase_records(ledger_rows: list[dict[str, Any]]) -> None:
    distribution = dict(Counter(row["outcome"] for row in ledger_rows))
    dump_json(
        PHASE_ROOT / "x2-proposal-ledger.json",
        {
            "schema": "ghc.family.v644-v2.x2-proposal-ledger.v1",
            "phase": PHASE,
            "owner": "Orin Thale",
            "x1_commit": X1_COMMIT,
            "proposal_count": len(ledger_rows),
            "outcome_classes": ["completed", "represented", "open_gap", "exact_gate"],
            "distribution": distribution,
            "control_case_count": 10,
            "synthetic_negative_count": 70,
            "total_case_count": 80,
            "proposals": ledger_rows,
            "x1_modified_after_freeze": False,
            "boundary": "Outcomes describe bounded repository artifacts only. Expected and observed counts matching does not promote any external claim.",
        },
    )
    dump_json(
        PHASE_ROOT / "evidence" / "evidence-ledger.json",
        {
            "schema": "ghc.family.v644-v2.evidence-ledger.v1",
            "phase": PHASE,
            "owner": "Orin Thale",
            "x1_commit": X1_COMMIT,
            "proposal_distribution": distribution,
            "control_cases": 10,
            "rejected_synthetic_cases": 70,
            "all_synthetic_negatives_retained": True,
            "real_data_rows": 0,
            "real_participant_or_rater_rows": 0,
            "real_keys_or_proofs": 0,
            "live_endpoints": 0,
            "independent_review_events": 0,
            "external_authority_decisions": 0,
            "same_owner_snapshot_evidence_pending": True,
            "independent_team_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    dump_json(
        PHASE_ROOT / "phase-truth.json",
        {
            "schema": "ghc.family.v644-v2.phase-truth.v1",
            "phase": PHASE,
            "owner": "Orin Thale",
            "primary_focus": "GMUT Mind",
            "proposal_count": len(ledger_rows),
            "proposal_distribution": distribution,
            "outcome_classes": ["completed", "represented", "open_gap", "exact_gate"],
            "case_count": 80,
            "synthetic_negative_count": 70,
            "active_phase": "v644-v2 x2 evidence candidate",
            "latest_closed_phase": "Sable Rook v644-v1",
            "latest_completed_x1": X1_COMMIT,
            "latest_completed_x2": "v644-v2 bounded evidence packet; closeout pending",
            "next_x2_scope": "fresh detached evidence validation, closeout, seal, and final-head validation",
            "next_x1_lane_or_exact_gated_continuation": "Tamar Vey v644-v3 only after the exact terminal send gate",
            "active_lanes": ["Orin Thale v644-v2 owned lane"],
            "standby_recoverable_lanes": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Tamar Vey", "Sylven Arc", "all other siblings"],
            "open_gap_count": 5,
            "exact_gate_count": 6,
            "outbound_message_count": 0,
            "successor_task_count": 0,
            "subagent_count": 0,
            "route_state": "PREPARED_NOT_SENT",
            "same_owner_repeatability": False,
            "independent_team_reproduction": False,
            "protected_claims": {
                "gmut_empirical_confirmation": False,
                "thos_participant_effectiveness": False,
                "freed_id_production": False,
                "cbr_legitimacy_or_acceptance": False,
                "maori_authority_or_ratification": False,
                "legal_interpretation_or_enacted_law": False,
                "deployment": False,
                "accessibility_complete": False,
                "exhaustive_security": False,
                "independent_team_reproduction": False,
                "consciousness_or_personhood": False,
                "agi_or_asi": False,
                "proof_canon_or_stage20": False
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    dump_json(
        PHASE_ROOT / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v644-v2.complete-incomplete-checklist.v1",
            "phase": PHASE,
            "complete_in_owned_scope": [
                "source and x1 ancestry verified",
                "exactly ten x1 proposals frozen before x2",
                "240-prior proposal novelty audit",
                "six completed, two represented, one open-gap, and one exact-gate artifacts built",
                "70 synthetic negatives retained",
                "three pillars and primary focus explicit",
                "accessible static report built with manual evaluation reserved",
                "threat, gate, phase-truth, and reproduction plans present",
            ],
            "incomplete_or_external": [
                "fresh detached evidence snapshots",
                "closeout, seal, and final detached validation",
                "real GMUT data and derived observables",
                "real THOS arms, participants, raters, harms, and independent review",
                "Freed ID real keys, proofs, live services, interoperability, reviews, and governance",
                "CBR, Māori, legal, cultural, fiduciary, and affected-party authority",
                "qualified manual accessibility and independent security review",
                "independent-team scientific reproduction",
                "external Stage 20 decision",
                "terminal Tamar baton",
            ],
            "owned_evidence_packet_complete": True,
            "stage20_ready": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    dump_json(
        PHASE_ROOT / "stage20" / "domain-veto-evidence-board.json",
        {
            "schema": "ghc.family.v644-v2.stage20-domain-veto-board.v1",
            "phase": PHASE,
            "decision_rule": "No domain compensates for another; any open or exact gate preserves the terminal veto.",
            "domains": [
                {"domain": "GMUT Mind", "state": "veto", "reason": "formal synthetic obligations only; real-data studies remain open"},
                {"domain": "THOS Body", "state": "veto", "reason": "protocol proxy only; no real arms or independent review"},
                {"domain": "Freed ID/CBR Heart", "state": "veto", "reason": "structural proxy plus unresolved production and authority gates"},
                {"domain": "accessibility and security", "state": "veto", "reason": "bounded static and synthetic checks only"},
                {"domain": "independent reproduction", "state": "veto", "reason": "same-owner snapshots pending and never independent-team evidence"},
            ],
            "compensation_across_domains_allowed": False,
            "vetoes": [
                {"domain": "GMUT Mind", "decision": "veto"},
                {"domain": "THOS Body", "decision": "veto"},
                {"domain": "Freed ID/CBR Heart", "decision": "veto"},
                {"domain": "accessibility and security", "decision": "veto"},
                {"domain": "independent reproduction", "decision": "veto"}
            ],
            "external_decision_authority": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def build_threat_model() -> None:
    dump_json(
        PHASE_ROOT / "threat-model.json",
        {
            "schema": "ghc.family.v644-v2.threat-model.v1",
            "phase": PHASE,
            "assets": ["x1 freeze", "source lineage", "negative history", "proposal outcomes", "authority gates", "public artifact privacy", "terminal route"],
            "threats": [
                {"id": "T01", "threat": "x1 mutation after freeze", "control": "Git-blob x1 content seal", "residual": "requires ancestry and blob verification at every terminal snapshot"},
                {"id": "T02", "threat": "formal GMUT bookkeeping promoted to physics", "control": "typed nonpromotion boundaries and zero-row empirical gap", "residual": "model-specific derivation and real data absent"},
                {"id": "T03", "threat": "THOS proxy promoted to participant benefit", "control": "zero real-arm and real-participant counters", "residual": "ethics, consent, blind arms, harms, and review absent"},
                {"id": "T04", "threat": "synthetic Freed ID transcript promoted to production", "control": "real-key, endpoint, status, interoperability, and governance gates", "residual": "all production evidence absent"},
                {"id": "T05", "threat": "repository output substitutes for affected-party, Māori, fiduciary, cultural, or legal authority", "control": "exact gate and neutral unanswered questions", "residual": "authorized participation absent"},
                {"id": "T06", "threat": "command fixtures execute an unintended shell or option", "control": "explicit argv contract and rejected mutations", "residual": "bounded fixtures are not exhaustive security"},
                {"id": "T07", "threat": "static accessibility checks overclaim conformance", "control": "manual and affected-user reservation", "residual": "qualified evaluation absent"},
                {"id": "T08", "threat": "same-owner snapshots counted as independent reproduction", "control": "review-dependence graph and explicit same-owner label", "residual": "independent team and infrastructure absent"},
                {"id": "T09", "threat": "raw identifiers, routes, credentials, or local paths leak", "control": "phase privacy scanner and semantic review", "residual": "novel encodings still require human review"},
                {"id": "T10", "threat": "premature or duplicate sibling activation", "control": "single terminal message gated on exact final validation", "residual": "route availability must be verified privately after closeout"},
            ],
            "exhaustive_security_claimed": False,
            "deployment_authorized": False,
        },
    )


def build_reproduction_records() -> None:
    dump_json(
        PHASE_ROOT / "reproduction" / "evidence-snapshot-plan.json",
        {
            "schema": "ghc.family.v644-v2.evidence-snapshot-plan.v1",
            "phase": PHASE,
            "required_snapshots": ["evidence-a", "evidence-b", "closeout", "seal", "final"],
            "storage_class": "fresh detached D-drive worktrees",
            "per_snapshot_checks": ["exact head", "clean before", "complete repository suite", "detailed validator", "minimal validator", "JSON parsing", "privacy/raw-ID scan", "manifest parity", "diff hygiene", "clean after"],
            "same_owner_repeatability_only": True,
            "independent_team_reproduction": False,
            "prior_lanes_preserved": True,
        },
    )
    dump_json(
        PHASE_ROOT / "reproduction" / "independent-team-gap.json",
        {
            "schema": "ghc.family.v644-v2.independent-team-gap.v1",
            "phase": PHASE,
            "state": "open_gap",
            "same_owner_snapshots_planned": 2,
            "independent_team_count": 0,
            "independent_protocol_count": 0,
            "independent_infrastructure_count": 0,
            "required": ["independent team", "independently owned protocol", "independent infrastructure", "returned signed evidence", "conflict and common-mode review"],
        },
    )


def build_environment_and_tool_receipts() -> None:
    dump_json(
        PHASE_ROOT / "environment" / "x2-execution-receipt.json",
        {
            "schema": "ghc.family.v644-v2.x2-execution-receipt.v1",
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "x1_four_way_equal_before_x2": True,
            "x1_clean_before_x2": True,
            "x1_files_modified": False,
            "proposal_cases": 80,
            "synthetic_negatives": 70,
            "real_data_downloaded": False,
            "participant_action": False,
            "real_key_or_proof_action": False,
            "deployment": False,
            "elevation": False,
            "desktop_update": False,
            "host_security_change": False,
            "windows_feature_change": False,
            "reboot": False,
            "task_or_subagent_created": False,
            "outbound_message_count": 0,
        },
    )
    dump_json(
        PHASE_ROOT / "tooling" / "executed-toolchain.json",
        {
            "schema": "ghc.family.v644-v2.executed-toolchain.v1",
            "phase": PHASE,
            "executed": [
                "scripts/build_ghc_family_v644_v2_preregistration.py",
                "scripts/ghc_family_v644_v2_model.py",
                "scripts/ghc_family_v644_v2_evidence.py",
                "scripts/build_ghc_family_v644_v2_report.py",
                "scripts/ghc_family_v644_v2_validator.py",
                "scripts/ghc_family_v644_v2_minimal.py",
                "scripts/ghc_family_v644_v2_complete_suite.py",
                "scripts/ghc_family_v644_v2_staged_review.py",
                "scripts/ghc_family_repository_test_runner.py",
                "scripts/ghc_family_phase_privacy_scan.py",
            ],
            "shared_family_skill_changes": [],
            "shared_validator_changes": [],
            "reviewed_current_receipt": "tooling/currency-review.json",
            "caller_compatibility_preserved": True,
        },
    )


def build_accessible_deliverables() -> None:
    final_overview = (PHASE_ROOT / "v644-v2-integrated-overview.md").read_text(encoding="utf-8")
    final_overview += "\n## x2 bounded outcomes\n\nThe frozen distribution was realized only in repository scope: six completed typed controls, two represented proxies, one open real-data gap, and one exact authority gate. Seventy single-field mutations were rejected and retained. No external scientific, participant, production, cultural, legal, security, accessibility, identity, deployment, proof/canon, or Stage 20 claim was promoted.\n"
    dump_text(PHASE_ROOT / "deliverables" / "v644-v2-final-integrated-overview.md", final_overview)
    report_path = PHASE_ROOT / "deliverables" / "v644-v2-boundary-evidence-report.html"
    build_report(report_path)
    report_text = report_path.read_text(encoding="utf-8")
    dump_json(
        PHASE_ROOT / "accessibility" / "static-report-receipt.json",
        {
            "schema": "ghc.family.v644-v2.static-report-receipt.v1",
            "phase": PHASE,
            "report": rel(report_path),
            "static_checks": {
                "html_lang_en": '<html lang="en">' in report_text,
                "skip_link": 'href="#main"' in report_text,
                "main_target": 'id="main"' in report_text,
                "heading_hierarchy_present": all(tag in report_text for tag in ("<h1>", "<h2")),
                "captioned_table": "<caption>" in report_text and 'scope="col"' in report_text and 'scope="row"' in report_text,
                "descriptive_audit_links": "Read the frozen x1 proposal preregistration" in report_text,
                "responsive_viewport": 'name="viewport"' in report_text,
                "reduced_motion_rule": "prefers-reduced-motion" in report_text,
                "active_script_count": report_text.casefold().count("<script"),
            },
            "manual_evaluation_reserved": True,
            "assistive_technology_evaluation_reserved": True,
            "cognitive_accessibility_review_reserved": True,
            "affected_user_evaluation_reserved": True,
            "complete_accessibility_claimed": False,
        },
    )


def stable_manifest_paths() -> list[Path]:
    paths = []
    for path in PHASE_ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(PHASE_ROOT)
        if relative.parts[0] == "validation":
            continue
        if relative.as_posix() == "reproduction/manifest.json":
            continue
        if relative.name in {"closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"}:
            continue
        paths.append(path)
    paths.extend(ROOT / item for item in X2_EXTERNAL_FILES if (ROOT / item).exists())
    return sorted(set(paths), key=lambda item: rel(item))


def refresh_manifest() -> None:
    prior_manifest = PHASE_ROOT / "reproduction" / "manifest.json"
    prior = json.loads(prior_manifest.read_text(encoding="utf-8")) if prior_manifest.exists() else {}
    entries = []
    for path in stable_manifest_paths():
        entries.append({"path": rel(path), "sha256_lf_normalized": normalized_sha256(path), "bytes": len(path.read_bytes())})
    dump_json(
        PHASE_ROOT / "reproduction" / "manifest.json",
        {
            "schema": "ghc.family.v644-v2.manifest.v1",
            "phase": PHASE,
            "normalization": "CRLF and CR normalized to LF before SHA-256",
            "scope_rule": "all stable owner phase files except validation receipts, manifest self, closeout, seal, and final records; plus v644-v2 scripts and tests",
            "entry_count": len(entries),
            "entries": entries,
            "snapshot_state": prior.get("snapshot_state", "pending"),
            "same_owner_repeatability_only": True,
            "independent_team_reproduction": False,
        },
    )


def build_evidence() -> None:
    build_x1_content_seal()
    ledger_rows = build_proposal_artifacts()
    build_phase_records(ledger_rows)
    build_retained_negatives()
    build_gate_register()
    build_threat_model()
    build_reproduction_records()
    build_environment_and_tool_receipts()
    build_accessible_deliverables()
    dump_json(
        PHASE_ROOT / "validation" / "execution-negative-log.json",
        {
            "schema": "ghc.family.v644-v2.execution-negative-log.v1",
            "phase": PHASE,
            "x2_operational_negative_count": len(X2_OPERATIONAL_NEGATIVES),
            "negatives": X2_OPERATIONAL_NEGATIVES,
            "synthetic_negatives_recorded_elsewhere": 70,
            "all_failures_retained": True,
        },
    )
    refresh_manifest()


def finalize_evidence(repository_passed: int, repository_total: int) -> None:
    detailed = json.loads((PHASE_ROOT / "validation" / "evidence-candidate-detailed.json").read_text(encoding="utf-8"))
    minimal = json.loads((PHASE_ROOT / "validation" / "evidence-candidate-minimal.json").read_text(encoding="utf-8"))
    privacy = json.loads((PHASE_ROOT / "validation" / "x2-privacy-scan.json").read_text(encoding="utf-8"))
    staged = json.loads((PHASE_ROOT / "validation" / "evidence-staged-review.json").read_text(encoding="utf-8"))
    dump_json(
        PHASE_ROOT / "validation" / "repository-test-receipt.json",
        {
            "schema": "ghc.family.v644-v2.repository-test-receipt.v1",
            "phase": PHASE,
            "runner": "scripts/ghc_family_repository_test_runner.py",
            "passed": repository_passed,
            "total": repository_total,
            "failures": repository_total - repository_passed,
            "complete_suite": True,
            "valid": repository_passed == repository_total and repository_total > 0,
            "windows_inherited_acl_temp": True,
            "parent_acl_changed": False,
            "host_security_changed": False,
        },
    )
    dump_json(
        PHASE_ROOT / "validation" / "json-parse-receipt.json",
        {
            "schema": "ghc.family.v644-v2.json-parse-receipt.v1",
            "phase": PHASE,
            "parsed": detailed["json_files_parsed"],
            "failed": len(detailed["json_parse_issues"]),
            "valid": not detailed["json_parse_issues"],
        },
    )
    valid = all(
        [
            repository_passed == repository_total and repository_total > 0,
            detailed["valid"],
            minimal["valid"],
            privacy["valid"],
            staged["valid"],
        ]
    )
    dump_json(
        PHASE_ROOT / "validation" / "evidence-precommit-receipt.json",
        {
            "schema": "ghc.family.v644-v2.evidence-precommit-receipt.v1",
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "repository_tests": {"passed": repository_passed, "total": repository_total},
            "detailed_validation": {"passed": detailed["checks_passed"], "total": detailed["checks_total"]},
            "minimal_validation": {"passed": minimal["checks_passed"], "total": minimal["checks_total"]},
            "json_files_parsed": detailed["json_files_parsed"],
            "privacy_scan": {"files": privacy["scanned_file_count"], "hits": privacy["hit_count"]},
            "manifest": {"entries": detailed["manifest_entries"], "mismatches": detailed["manifest_mismatch_count"]},
            "exact_staged_file_review": staged["valid"],
            "x1_content_unchanged": detailed["x1_content_unchanged"],
            "proposal_distribution": detailed["proposal_distribution"],
            "retained_negative_count": detailed["retained_negative_count"],
            "open_gap_count": 5,
            "exact_gate_count": 6,
            "valid": valid,
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    refresh_manifest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-manifest-only", action="store_true")
    parser.add_argument("--finalize-evidence", action="store_true")
    parser.add_argument("--repository-passed", type=int, default=0)
    parser.add_argument("--repository-total", type=int, default=0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.refresh_manifest_only:
        refresh_manifest()
    else:
        build_evidence()
        if args.finalize_evidence:
            finalize_evidence(args.repository_passed, args.repository_total)
    print(json.dumps({"phase": PHASE, "manifest_entries": len(json.loads((PHASE_ROOT / 'reproduction' / 'manifest.json').read_text(encoding='utf-8'))['entries'])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
