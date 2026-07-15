#!/usr/bin/env python3
"""Build Sylven Arc v644-v4 x2 evidence and candidate receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v644-gmut-thos-v4-x1-x2"
PHASE_ROOT = ROOT / "docs" / "sylven-arc" / "v644-v4"
SOURCE_HEAD = "13b30aa133be3eb13b5da253deefd8830ac56781"
SOURCE_SEAL = "d2bb82e1c29d2c96dc3c00e374a376ffc455583c"
X1_COMMIT = "a33c6d53a37f3f86fe143bba81dcacf52b4e20c0"
INHERITED_NEGATIVE_REGISTER = ROOT / "docs" / "tamar-vey" / "v644-v3" / "retained-negative-register.json"
X2_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6444-X2-OP-01",
        "origin": "v644-v4-x2-operational",
        "observed": "The first Python report-source inspection stopped when the Windows cp1252 console could not encode the Māori macron.",
        "recovery": "Forced UTF-8 standard output and reran the same read to inspect the complete report source without changing it.",
        "promotion_effect": "The truncated inspection is retained and is not report-review evidence.",
        "retained": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6444-X2-OP-02",
        "origin": "v644-v4-x2-operational",
        "observed": "A broad inherited acronym-expansion search exceeded its bounded timeout before returning a usable result.",
        "recovery": "Kept the established project labels unchanged and added contextual glossary descriptions without inventing unverified long forms.",
        "promotion_effect": "The timed-out search is retained and is not abbreviation-completeness evidence.",
        "retained": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6444-X2-OP-03",
        "origin": "v644-v4-x2-operational",
        "observed": "The first semantic stale-label scan used an invalid PowerShell and rg quoting or wildcard combination, so its phase and owner value subchecks did not execute.",
        "recovery": "Retained the failed invocation and reran the review with explicit repository paths and literal fixed-string checks.",
        "promotion_effect": "The malformed scan is not stale-label review evidence; only the corrected bounded rerun is evidence.",
        "retained": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6444-X2-OP-04",
        "origin": "v644-v4-x2-operational",
        "observed": "A Git checkout-index attempt did not convert the inherited CRLF legacy-alias fixture to its repository LF bytes, and the complete suite therefore returned 599 of 600 with the known warning-count mismatch.",
        "recovery": "Retained the failed 599-of-600 run, applied an explicit reversible newline-only conversion to the inherited fixture, reran the complete suite, and restored the original clean CRLF worktree bytes afterward.",
        "promotion_effect": "The 599-of-600 run is a failure and is not counted as repository-suite evidence.",
        "retained": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6444-X2-OP-05",
        "origin": "v644-v4-x2-operational",
        "observed": "A semantic stale-label review traversed an unnecessarily broad recursive scope and timed out before producing a complete result.",
        "recovery": "Retained the timeout and reran fixed-string checks over only the current owner packet and the exact v644-v4 scripts and test module, excluding the inherited negative body where prior phase labels are expected evidence.",
        "promotion_effect": "The timed-out traversal is not stale-label review evidence.",
        "retained": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6444-X2-OP-06",
        "origin": "v644-v4-x2-operational",
        "observed": "A bounded fixed-string JSON-label scan lost its literal quote characters through PowerShell argument parsing and then stopped on an owner-field no-match.",
        "recovery": "Retained the failed invocation and constructed the JSON field needles from the quote character before rerunning the bounded review with explicit no-match handling.",
        "promotion_effect": "The quote-stripped output is not semantic label-review evidence.",
        "retained": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6444-X2-OP-07",
        "origin": "v644-v4-x2-operational",
        "observed": "A targeted fixed-string check showed that a JSON quote character constructed in a PowerShell variable was still removed by Windows native-command argument parsing, producing a no-match against a known phase field.",
        "recovery": "Retained the no-match and verified a PCRE hex-quote pattern against the same file before using that pattern for the bounded semantic review.",
        "promotion_effect": "The variable-constructed no-match is not semantic label-review evidence.",
        "retained": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6444-X2-OP-08",
        "origin": "v644-v4-post-evidence-operational",
        "observed": "The first post-evidence divergence display let PowerShell reinterpret the upstream revision token, so Git rejected the resulting invalid revision even though the separately captured local, upstream, tracking, and live heads were equal.",
        "recovery": "Retained the display failure and used separately quoted revision arguments for later divergence checks.",
        "promotion_effect": "The malformed divergence field is not 0/0 divergence evidence.",
        "retained": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6444-X2-OP-09",
        "origin": "v644-v4-post-evidence-operational",
        "observed": "A combined complete-suite help, attribute, and Git-configuration inspection exceeded its short timeout after returning only the help text.",
        "recovery": "Retained the timeout and used path-scoped detached-state and byte-hash checks with longer bounded windows.",
        "promotion_effect": "The partial help output is not checkout-configuration evidence.",
        "retained": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6444-X2-OP-10",
        "origin": "v644-v4-post-evidence-operational",
        "observed": "The first evidence-A worktree materialization exceeded its 120-second wrapper timeout before returning a receipt, although a later audit found the detached worktree fully registered at the exact evidence head.",
        "recovery": "Retained the timeout, audited the completed path directly, and used longer windows for later fresh snapshot materialization.",
        "promotion_effect": "The timed-out wrapper is not materialization evidence.",
        "retained": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6444-X2-OP-11",
        "origin": "v644-v4-post-evidence-operational",
        "observed": "A ten-second evidence-A hash, status, and head audit timed out without returning its receipt.",
        "recovery": "Retained the timeout and reran the same path-scoped audit with a longer bounded window.",
        "promotion_effect": "The short timed-out audit is not detached-state evidence.",
        "retained": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6444-X2-OP-12",
        "origin": "v644-v4-evidence-snapshot-operational",
        "observed": "The first evidence-A complete suite used an all-LF checkout and failed 599 of 600 because an inherited v641 equation-lineage fixture was generated from the normal Windows checkout byte form.",
        "recovery": "Retained the failed clean snapshot and created fresh hybrid snapshots using the normal checkout byte form with only the exact legacy-alias fixture normalized to repository LF bytes.",
        "promotion_effect": "The 599-of-600 snapshot is failed evidence and does not count toward repeatability.",
        "retained": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6444-X2-OP-13",
        "origin": "v644-v4-evidence-snapshot-operational",
        "observed": "The first hybrid snapshot retry wrapper used PowerShell backticks inside a JavaScript template literal and failed before invoking the shell.",
        "recovery": "Retained the wrapper failure, confirmed the target path remained absent, and resubmitted the same operation through a plain string wrapper.",
        "promotion_effect": "The syntax failure created no snapshot and is not validation evidence.",
        "retained": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6444-X2-OP-14",
        "origin": "v644-v4-closeout-operational",
        "observed": "The first read-only lifecycle-template lookup mixed PowerShell array syntax into the JavaScript wrapper and failed before reading any file.",
        "recovery": "Retained the wrapper failure and reran the bounded reference read through a plain PowerShell command.",
        "promotion_effect": "The syntax failure is not lifecycle-template review evidence.",
        "retained": True,
        "external_gate_closed": False,
    },
]
X2_EXTERNAL_FILES = [
    "scripts/build_ghc_family_v644_v4_report.py",
    "scripts/ghc_family_v644_v4_complete_suite.py",
    "scripts/ghc_family_v644_v4_evidence.py",
    "scripts/ghc_family_v644_v4_minimal.py",
    "scripts/ghc_family_v644_v4_model.py",
    "scripts/ghc_family_v644_v4_staged_review.py",
    "scripts/ghc_family_v644_v4_validator.py",
    "tests/test_ghc_family_v644_v4.py",
]


from build_ghc_family_v644_v4_report import build_report  # noqa: E402
from ghc_family_v644_v4_model import SPECS, all_cases  # noqa: E402
from ghc_family_v644_v4_x1_definitions import PROPOSALS, X1_NEGATIVES  # noqa: E402


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
            "schema": "ghc.family.v644-v4.x1-content-seal.v1",
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
                "schema": f"ghc.family.v644-v4.{proposal_id.casefold()}.primary-artifact.v1",
                "phase": PHASE,
                "owner": "Sylven Arc",
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
            "schema": f"ghc.family.v644-v4.{proposal_id.casefold()}.secondary-artifact.v1",
            "phase": PHASE,
            "proposal_id": proposal_id,
            "artifact_role": "seven preregistered falsifier mutations retained as negatives",
            "mutation_count": len(mutations),
            "mutations": mutations,
            "all_rejected": all(item["evaluation"]["decision"] == "rejected" for item in mutations),
            "all_retained": all(item["retained"] for item in mutations),
            "case_set_sha256": case_set["case_set_sha256"],
        }
        if proposal_id == "V6444-P03":
            secondary["missing_requirements"] = [
                "model-specific GMUT lunar-ranging signature derivation",
                "checksum-bound licensed lunar normal-point rows",
                "station and reflector provenance",
                "reference-frame and time-scale transforms",
                "source covariance, calibration, and nuisance model",
                "frozen selection plan with named baseline",
                "blind holdout",
                "identifiability analysis",
                "independent review",
            ]
            secondary["likelihood_executed"] = False
        if proposal_id == "V6444-P06":
            secondary["neutral_unanswered_questions"] = [
                "Which affected parties and representatives may set a remedy-fund sufficiency objective?",
                "Which Māori authorities and data-governance mandates apply, if any?",
                "Who may define priority classes when funds are scarce and how is beneficiary privacy preserved?",
                "Who is qualified and authorized to select actuarial, inflation, investment-risk, and distribution assumptions?",
                "How may present and future beneficiary interests be weighed without substituting repository output for consent, fiduciary direction, cultural ratification, or law?",
            ]
            secondary["answers_supplied_by_repository"] = False
        dump_json(second, secondary)
        dump_json(
            third,
            {
                "schema": f"ghc.family.v644-v4.{proposal_id.casefold()}.nonpromotion-boundary.v1",
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
            "origin": "v644-v4-x1-operational",
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
                    "origin": "v644-v4-preregistered-synthetic",
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
            "schema": "ghc.family.v644-v4.retained-negative-register.v1",
            "phase": PHASE,
            "owner": "Sylven Arc",
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
            "schema": "ghc.family.v644-v4.exact-open-gate-register.v1",
            "phase": PHASE,
            "owner": "Sylven Arc",
            "open_gap_count": 5,
            "exact_gate_count": 6,
            "open_gaps": [
                {
                    "gate_id": "OPEN-01",
                    "domain": "GMUT real-data observable studies, including inherited multi-messenger, Solar-System, binary-pulsar, and v644-v4 lunar-laser-ranging protocols",
                    "state": "open",
                    "requires": ["model-specific observable derivation", "licensed checksum-bound real rows", "covariance, calibration, and selection", "frozen nuisance plan", "blind named baseline", "identifiability analysis", "independent review"],
                },
                {"gate_id": "OPEN-02", "domain": "THOS real-arm evidence", "state": "open", "requires": ["ethics", "consent", "preregistered blind matched-budget arms", "real participants and raters", "harms monitoring", "independent review"]},
                {"gate_id": "OPEN-03", "domain": "Freed ID production completion", "state": "open", "requires": ["standards-conformant real keys and proofs", "live issuance and presentation", "live resolution", "status and revocation", "cross-vendor interoperability", "privacy and security review", "trust governance"]},
                {"gate_id": "OPEN-04", "domain": "qualified accessibility evaluation", "state": "open", "requires": ["manual evaluation", "assistive-technology coverage", "cognitive-accessibility review", "affected-user evaluation"]},
                {"gate_id": "OPEN-05", "domain": "independent-team scientific reproduction", "state": "open", "requires": ["independent team", "independently owned protocol", "independent infrastructure", "returned evidence"]},
            ],
            "exact_gates": [
                {"gate_id": "EXACT-01", "domain": "affected-party remedy-fund sufficiency, priority, audit, beneficiary privacy, data-return, stewardship, and acceptance decisions", "state": "pending_exact_authority"},
                {"gate_id": "EXACT-02", "domain": "Māori wording, authority, data governance, and intergenerational legitimacy", "state": "pending_exact_authority"},
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
            "schema": "ghc.family.v644-v4.x2-proposal-ledger.v1",
            "phase": PHASE,
            "owner": "Sylven Arc",
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
            "schema": "ghc.family.v644-v4.evidence-ledger.v1",
            "phase": PHASE,
            "owner": "Sylven Arc",
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
            "schema": "ghc.family.v644-v4.phase-truth.v1",
            "phase": PHASE,
            "owner": "Sylven Arc",
            "primary_focus": "GMUT Mind",
            "proposal_count": len(ledger_rows),
            "proposal_distribution": distribution,
            "outcome_classes": ["completed", "represented", "open_gap", "exact_gate"],
            "case_count": 80,
            "synthetic_negative_count": 70,
            "active_phase": "v644-v4 x2 evidence candidate",
            "latest_closed_phase": "Tamar Vey v644-v3",
            "latest_completed_x1": X1_COMMIT,
            "latest_completed_x2": "v644-v4 bounded evidence packet; closeout pending",
            "next_x2_scope": "fresh detached evidence validation, closeout, seal, and final-head validation",
            "next_x1_lane_or_exact_gated_continuation": "Eiren Kestrel v644-v5 only after the exact terminal send gate",
            "active_lanes": ["Sylven Arc v644-v4 owned lane"],
            "standby_recoverable_lanes": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "all other siblings"],
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
            "schema": "ghc.family.v644-v4.complete-incomplete-checklist.v1",
            "phase": PHASE,
            "complete_in_owned_scope": [
                "source and x1 ancestry verified",
                "exactly ten x1 proposals frozen before x2",
                "260-prior proposal novelty audit",
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
                "terminal Eiren Kestrel baton",
            ],
            "owned_evidence_packet_complete": True,
            "stage20_ready": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    dump_json(
        PHASE_ROOT / "stage20" / "domain-veto-evidence-board.json",
        {
            "schema": "ghc.family.v644-v4.stage20-domain-veto-board.v1",
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
            "schema": "ghc.family.v644-v4.threat-model.v1",
            "phase": PHASE,
            "assets": ["x1 freeze", "source lineage", "negative history", "proposal outcomes", "authority gates", "public artifact privacy", "terminal route"],
            "threats": [
                {"id": "T01", "threat": "x1 mutation after freeze", "control": "Git-blob x1 content seal", "residual": "requires ancestry and blob verification at every terminal snapshot"},
                {"id": "T02", "threat": "higher-derivative degeneracy bookkeeping promoted to a healthy GMUT theory", "control": "typed constraint-chain nonpromotion boundary and zero-row lunar-ranging gap", "residual": "model-specific Hamiltonian derivation, well-posedness, observables, and real data absent"},
                {"id": "T03", "threat": "THOS proxy promoted to participant benefit", "control": "zero real-arm and real-participant counters", "residual": "ethics, consent, blind arms, harms, and review absent"},
                {"id": "T04", "threat": "synthetic remote-context checks promoted to production Freed ID assurance", "control": "real-key, endpoint, status, interoperability, semantic-integrity, and governance gates", "residual": "all production evidence absent"},
                {"id": "T05", "threat": "repository output substitutes for affected-party, Māori, actuarial, fiduciary, privacy, cultural, or legal authority", "control": "exact sufficiency-and-priority gate with neutral unanswered questions", "residual": "authorized participation absent"},
                {"id": "T06", "threat": "Git replacement refs or alternate object stores hide ancestry or borrowed objects", "control": "bounded object-indirection contract and rejected mutations", "residual": "bounded fixtures are not exhaustive repository security"},
                {"id": "T07", "threat": "abbreviation structure checks overclaim accessibility or comprehension", "control": "manual, cognitive, assistive-technology, and affected-user reservation", "residual": "qualified evaluation absent"},
                {"id": "T08", "threat": "same-owner snapshots counted as independent reproduction", "control": "explicit same-owner label and independent-team gap", "residual": "independent team and infrastructure absent"},
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
            "schema": "ghc.family.v644-v4.evidence-snapshot-plan.v1",
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
            "schema": "ghc.family.v644-v4.independent-team-gap.v1",
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
            "schema": "ghc.family.v644-v4.x2-execution-receipt.v1",
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
            "schema": "ghc.family.v644-v4.executed-toolchain.v1",
            "phase": PHASE,
            "executed": [
                "scripts/build_ghc_family_v644_v4_preregistration.py",
                "scripts/ghc_family_v644_v4_model.py",
                "scripts/ghc_family_v644_v4_evidence.py",
                "scripts/build_ghc_family_v644_v4_report.py",
                "scripts/ghc_family_v644_v4_validator.py",
                "scripts/ghc_family_v644_v4_minimal.py",
                "scripts/ghc_family_v644_v4_complete_suite.py",
                "scripts/ghc_family_v644_v4_staged_review.py",
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
    final_overview = (PHASE_ROOT / "v644-v4-integrated-overview.md").read_text(encoding="utf-8")
    final_overview += "\n## x2 bounded outcomes\n\nThe frozen distribution was realized only in repository scope: six completed typed controls, two represented proxies, one open real-data gap, and one exact authority gate. Seventy single-field mutations were rejected and retained. No external scientific, participant, production, cultural, legal, security, accessibility, identity, deployment, proof/canon, or Stage 20 claim was promoted.\n"
    dump_text(PHASE_ROOT / "deliverables" / "v644-v4-final-integrated-overview.md", final_overview)
    report_path = PHASE_ROOT / "deliverables" / "v644-v4-boundary-evidence-report.html"
    build_report(report_path)
    report_text = report_path.read_text(encoding="utf-8")
    dump_json(
        PHASE_ROOT / "accessibility" / "static-report-receipt.json",
        {
            "schema": "ghc.family.v644-v4.static-report-receipt.v1",
            "phase": PHASE,
            "report": rel(report_path),
            "static_checks": {
                "html_lang_en": '<html lang="en">' in report_text,
                "skip_link": 'href="#main"' in report_text,
                "main_target": 'id="main"' in report_text,
                "heading_hierarchy_present": all(tag in report_text for tag in ("<h1>", "<h2")),
                "captioned_table": "<caption>" in report_text and 'scope="col"' in report_text and 'scope="row"' in report_text,
                "abbreviation_glossary": "<abbr" in report_text and "Project-label glossary" in report_text and "<dl>" in report_text,
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
            "schema": "ghc.family.v644-v4.manifest.v1",
            "phase": PHASE,
            "normalization": "CRLF and CR normalized to LF before SHA-256",
            "scope_rule": "all stable owner phase files except validation receipts, manifest self, closeout, seal, and final records; plus v644-v4 scripts and tests",
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
            "schema": "ghc.family.v644-v4.execution-negative-log.v1",
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
            "schema": "ghc.family.v644-v4.repository-test-receipt.v1",
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
            "schema": "ghc.family.v644-v4.json-parse-receipt.v1",
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
            "schema": "ghc.family.v644-v4.evidence-precommit-receipt.v1",
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
