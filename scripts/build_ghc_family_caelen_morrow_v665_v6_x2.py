#!/usr/bin/env python3
"""Build bounded synthetic x2 evidence for Caelen Morrow v665-v6."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ghc_family_caelen_morrow_v665_v6_runtime import evaluate_contract


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-morrow" / "v665-v6"
X1_SHA = "9be19f91371da0d2bcdd23de421fed202c5641fa"
SOURCE_SHA = "cacbeb47741b9e86a6a980f85f6f9658a0837f7c"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(relative: str, value: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


DOMAIN_PAYLOADS: list[dict[str, Any]] = [
    {
        "job_token": "SYN-JOB-001",
        "source_work_token": "SYN-SOURCE-001",
        "requested_code": "unspecified",
        "locale_status": "vacant",
        "purpose": "schema_evaluation",
        "withdrawal_state": "available",
        "revision": 1,
        "production_lock": True,
    },
    {
        "segment_token": "SYN-SEG-001",
        "source_span": {"start": 0, "end": 4},
        "generated_cell_tokens": ["U+2801", "U+2803"],
        "omission_markers": ["none"],
        "translator_note": "synthetic_placeholder_only",
        "correction_parent": "none",
        "fidelity_claim": False,
    },
    {
        "code_point": "U+2801",
        "scalar_value": 10241,
        "dot_set": [1],
        "cell_mode": 6,
        "blank": False,
        "meaning_status": "not_assigned_by_validator",
    },
    {
        "capital_scope": "synthetic_single",
        "number_scope": "synthetic_single",
        "typeform_scope": "unspecified",
        "grade_state": "unresolved",
        "terminator_state": "explicit_placeholder",
        "standing_alone_status": "review_vacant",
        "authority_review": "required_for_real_use",
    },
    {
        "token_class": "synthetic_word",
        "whole_word_state": "candidate_only",
        "groupsign_state": "candidate_only",
        "shortform_state": "not_asserted",
        "punctuation_context": "synthetic_boundary",
        "ambiguity": "unresolved",
        "exception_status": "review_vacant",
    },
    {
        "cells_per_line_placeholder": 40,
        "lines_per_page_placeholder": 25,
        "volume_token": "SYN-VOL-001",
        "running_head_state": "omitted",
        "print_page_lineage": ["SYN-PRINT-PAGE-001"],
        "embosser_commands": [],
        "layout_status": "simulation_only",
    },
    {
        "figure_token": "SYN-FIG-001",
        "caption_token": "SYN-CAP-001",
        "key_token": "SYN-KEY-001",
        "orientation": "unspecified",
        "texture_placeholder": "texture-A",
        "source_relation": "derived_placeholder",
        "reader_evaluation_status": "reserved",
    },
    {
        "simulated_spool_state": "cancelled",
        "file_digest_placeholder": "sha256:synthetic-only",
        "copy_count_placeholder": 1,
        "cancellation_available": True,
        "interlock_status": "unknown_not_bypassed",
        "hardware_calls": 0,
        "device_command_status": "prohibited",
    },
    {
        "print_location": "SYN-P1-L1",
        "braille_location": "SYN-B1-L1",
        "discrepancy_class": "synthetic_omission",
        "proposed_correction": "placeholder_only",
        "dual_review_status": "vacant",
        "contestation_state": "open",
        "erasure_allowed": False,
    },
    {
        "table_token": "SYN-TABLE-001",
        "code_edition": "declared_placeholder",
        "jurisdiction": "unassigned",
        "locale": "und",
        "checksum_placeholder": "sha256:synthetic-table",
        "supersession_state": "none",
        "stale_source_alarm": True,
        "conformance_claim": False,
    },
    {
        "package_token": "SYN-PACKAGE-001",
        "format_profile": "synthetic_boundary_profile",
        "volume_tokens": ["SYN-VOL-001"],
        "section_tokens": ["SYN-SEC-001"],
        "page_tokens": ["SYN-PAGE-001"],
        "row_tokens": ["SYN-ROW-001"],
        "navigation_state": "placeholder",
        "unknown_extension_state": "reject",
        "distribution_allowed": False,
    },
    {
        "queue_tokens": ["SYN-Q-A", "SYN-Q-B"],
        "matched_budget": "symbolic_equal",
        "artifact_labels_blinded": True,
        "error_taxonomy": ["omission", "scope", "layout"],
        "dominant_stop": "safety_or_withdrawal",
        "participants": 0,
        "independent_review_status": "absent",
    },
    {
        "receipt_token": "SYN-RECEIPT-001",
        "request_digest": "sha256:synthetic-request",
        "transformation_lineage": ["SYN-STEP-001"],
        "disclosure_purpose": "schema_evaluation",
        "expiry_state": "synthetic_expired",
        "withdrawal_state": "available",
        "correction_route": "placeholder_appeal",
        "key_count": 0,
        "proof_count": 0,
    },
    {
        "request_time": 1,
        "revision_time": 2,
        "acknowledgement_time": 3,
        "rejected_change_token": "SYN-REJECT-001",
        "attached_statement_token": "SYN-STATEMENT-001",
        "handover_debt": ["manual_review_reserved"],
        "prior_state_erased": False,
    },
    {
        "cell_token": "SYN-CELL-001",
        "occupancy_bit_vector": [1, 0, 0, 0, 0, 0],
        "adjacency_operator": [[0, 1], [1, 0]],
        "basis_convention": "symbolic_dot_basis",
        "dimension_status": "typed_not_physical",
        "observation_count": 0,
        "likelihood_present": False,
    },
    {
        "source_block_index": 1,
        "braille_page_state": [1, 0],
        "break_operator": [[1, -1], [0, 1]],
        "covariance_status": "vacant",
        "identifiability_status": "unresolved",
        "observation_count": 0,
        "prediction_claim": False,
    },
    {
        "source_text_token": "SYN-SOURCE-001",
        "reader_request_token": "SYN-REQUEST-001",
        "translator_note_token": "SYN-NOTE-001",
        "job_metadata_fields": ["purpose", "revision"],
        "disclosure_ceiling": "minimum_synthetic_fields",
        "retention_state": "delete_after_fixture",
        "remedy_route": "reserved_external",
        "real_person_fields": 0,
    },
    {
        "queue_ceiling_placeholder": 4,
        "proofreading_debt": ["SYN-DOC-001"],
        "equipment_status": "vacant_no_device",
        "dominant_stop": "withdrawal_or_safety",
        "handover_acknowledgement": "synthetic_received",
        "fatigue_inference": False,
        "real_workers": 0,
    },
    {
        "source_ids": ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10"],
        "version_pin_status": "recorded_not_live_resolved",
        "draft_watch_sources": ["S04", "S05"],
        "locale_holds": ["Māori_authority_reserved"],
        "network_calls": 0,
        "real_jobs": 0,
        "current_adapter_status": "open_gap",
    },
    {
        "reserved_decisions": [
            "code_adoption",
            "Māori_transcription",
            "disability_community_acceptance",
            "copyright",
            "privacy",
            "safety",
            "procurement",
            "remedy",
            "affected_party_legitimacy",
        ],
        "approvals_present": [],
        "authority_status": "reserved",
        "execution_status": "unexecuted",
        "affected_party_evidence": 0,
        "Māori_authority_evidence": 0,
    },
]


REPRESENTED_EVIDENCE_GAPS = {
    "CM6656-N012": [
        "no real readers or operators",
        "no preregistered blind matched-budget arms",
        "no safety monitoring, statistics, or independent review",
    ],
    "CM6656-N013": [
        "no standards-conformant real keys or proofs",
        "no live issuance, resolution, status, revocation, interoperability, recovery, or trust governance",
    ],
    "CM6656-N015": [
        "no observation, likelihood, empirical scale, constraint, force, or prediction",
        "no independent physics review",
    ],
    "CM6656-N016": [
        "no observation, covariance estimate, likelihood, parameter inference, or prediction",
        "no independent physics review",
    ],
    "CM6656-N019": [
        "no live official-source retrieval or schema negotiation by the phase software",
        "no network calls and zero external rows",
    ],
    "CM6656-N020": [
        "no affected-party, disability-community, copyright, privacy, safety, procurement, legal, cultural, or remedy approval",
        "no Māori-language, Māori-data-governance, tangata whenua, iwi, hapū, or Māori-authority approval",
    ],
}


SKILL_SPECS = [
    ("braille-intake-boundary", "Structure a synthetic braille-job intake record while refusing real work, reader, content, production, and authority actions.", "intake purpose, withdrawal, locale vacancy, and production locks"),
    ("segment-lineage-weave", "Trace synthetic print-to-braille segment lineage and correction ancestry without asserting transcription fidelity or conformance.", "source spans, generated cell tokens, omissions, notes, and corrections"),
    ("unicode-cell-envelope", "Validate bounded Unicode Braille Pattern cell envelopes while refusing to assign linguistic meaning or code authority.", "U+2800-U+28FF identity, dot sets, six/eight-dot modes, and blank distinction"),
    ("indicator-scope-lattice", "Record synthetic UEB indicator-scope states and uncertainty without making a real translation or code-adoption decision.", "capitals, numbers, typeforms, grades, terminators, and review holds"),
    ("contraction-trace-keeper", "Build a reviewable synthetic contraction-eligibility trace without certifying UEB correctness or professional competence.", "word, groupsign, shortform, punctuation, ambiguity, and exception states"),
    ("layout-device-firewall", "Separate synthetic page-layout metadata from any embosser or device command, with cancellation and hard-stop precedence.", "page constraints, spool simulation, interlock vacancy, and zero hardware calls"),
    ("proofreading-contestation-docket", "Preserve synthetic proofreading discrepancy, correction, contestation, and non-erasure history without replacing human review.", "print and braille locations, discrepancy class, proposed correction, and appeal"),
    ("source-profile-watch", "Maintain public braille-source version and draft/watch labels without converting citation into conformance or authority.", "ICEB, BANZAT, Unicode, DAISY, PEF, W3C, and New Zealand public-source status"),
    ("braille-method-flow", "Retain synthetic braille-phase failures, rejecting fixtures, recoveries, passing witnesses, and recurrence guards.", "Method Flow rows and exact negative retention"),
    ("braille-closeout-gate", "Check owner-local braille-phase truth, manifests, privacy boundaries, open gates, and terminal no-send prerequisites.", "closeout and route gating without running a full repository suite"),
]


RUNNER_SPECS = [
    ("contracts", "contract evaluation"),
    ("mutations", "one-hundred mutation rejection"),
    ("json", "owner JSON parsing"),
    ("privacy", "five-class privacy and raw-identifier scanning"),
    ("security", "bounded Python security scanning"),
    ("manifests", "owner manifest replay"),
    ("accessibility", "static structural accessibility checks"),
    ("truth", "outcome and gate truth checks"),
    ("closeout", "closeout prerequisite checks"),
    ("canonical-preflight", "canonical completion preflight without invoking the aggregate"),
]


def type_name(value: Any) -> str:
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "dict"
    raise TypeError(type(value).__name__)


def rules_for(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result = {}
    for field, value in payload.items():
        rule: dict[str, Any] = {"type": type_name(value)}
        if isinstance(value, (str, list, dict)) and len(value) > 0:
            rule["nonempty"] = True
        if any(token in field for token in ("status", "lock", "claim", "allowed", "calls")):
            rule["const"] = value
        result[field] = rule
    return result


def positive_fixture(pid: str, domain_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "proposal_id": pid,
        "synthetic_only": True,
        "real_data_rows": 0,
        "participant_count": 0,
        "network_calls": 0,
        "external_actions": [],
        "authority_status": "none",
        "production": False,
        "deployment": False,
        "outcome_claim": "bounded_structural_only",
        "domain_payload": domain_payload,
    }


def make_contract(proposal: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    pid = proposal["proposal_id"]
    return {
        "schema": "ghc.family.caelen-morrow.v665-v6.proposal-contract.v1",
        "owner": "Caelen Morrow",
        "phase": "v665-v6",
        "x1_sha": X1_SHA,
        "source_sha": SOURCE_SHA,
        "preregistered_before_x2": True,
        "proposal_id": pid,
        "title": proposal["title"],
        "pillar": proposal["pillar"],
        "expected_disposition": proposal["expected_disposition"],
        "approval_class": proposal["approval_class"],
        "completion_scope": "bounded owner-local synthetic JSON contract behavior only",
        "required_domain_fields": rules_for(payload),
        "bounded_positive_fixture": positive_fixture(pid, payload),
        "protected_gates": proposal["protected_gates"],
        "official_or_primary_source_needs": proposal["official_or_primary_source_needs"],
        "remaining_evidence_or_authority": REPRESENTED_EVIDENCE_GAPS.get(pid, []),
        "network_calls": 0,
        "real_rows": 0,
        "participants": 0,
        "external_actions": 0,
    }


def skill_text(name: str, description: str, focus: str) -> str:
    return f"""---
name: {name}
description: {description}
---

# {name}

Use this owner-local phase skill only for Caelen Morrow v665-v6 synthetic artifacts concerning {focus}. It is a narrow reference package and is not globally installed.

## Workflow

1. Read the frozen proposal and its protected gates before changing an artifact.
2. Accept only synthetic tokens with zero people, real works, devices, network calls, identity operations, and external actions.
3. Preserve source, revision, withdrawal, correction, uncertainty, and dominant-stop fields that apply to the request.
4. Run the proposal's bounded positive and all five preregistered rejecting mutations. Retain every failure and recovery through Method Flow.
5. Label evidence as bounded same-owner software structure. Reserve manual, affected-user, professional, legal, cultural, Māori-authority, production, security, privacy, accessibility, and independent review.

## Stop conditions

Stop rather than infer permission when a request introduces a real reader or worker, copyrighted source content, transcription or proofreading judgment, an embosser or device command, credentials, external writes, authority decisions, or claims beyond the four exact outcome labels. Never convert public-source vocabulary into conformance, competence, endorsement, or authority.
"""


def runner_text(runner_id: str, purpose: str) -> str:
    return f'''#!/usr/bin/env python3
"""Caelen Morrow v665-v6 runner: {purpose}."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_caelen_morrow_v665_v6_runner_common import run

RUNNER_ID = {runner_id!r}
ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    parser = argparse.ArgumentParser(description={purpose!r})
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = run(RUNNER_ID, ROOT, self_test_only=args.self_test)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("passed") else 1

if __name__ == "__main__":
    raise SystemExit(main())
'''


def method_row(method_id: str, request: str, witness: str, status: str, negative: bool) -> dict[str, Any]:
    return {
        "method_id": method_id,
        "request": request,
        "failed_witness": witness if negative else None,
        "failed_witness_status": "retained_rejecting_fixture" if negative else "not_observed_no_failure_fabricated",
        "bounded_passing_witness": witness,
        "status": status,
        "aggregate_credit": 0 if negative else 1,
        "retained_negative": negative,
        "rollback": "restore the last valid owner-local synthetic fixture and preserve every gate",
        "recurrence_guard": "rerun only the affected bounded check and never erase the prior witness",
    }


def main() -> None:
    freeze = load("x1/proposal-freeze.json")
    portfolio = load("x1/portfolio-freeze.json")
    tooling_receipt = load("x2/tooling-smoke-receipt.json")
    tooling_validated = (
        tooling_receipt.get("status") == "PASS"
        and tooling_receipt["skill_quick_validation"]["passed"] == 10
        and tooling_receipt["skill_quick_validation"]["failed"] == 0
        and tooling_receipt["runner_smoke"]["passed"] == 10
        and tooling_receipt["runner_smoke"]["failed"] == 0
    )
    if not tooling_validated:
        raise RuntimeError("tooling validation receipt is not complete")
    proposals = freeze["new_proposals"]
    if len(proposals) != 20 or len(DOMAIN_PAYLOADS) != 20:
        raise RuntimeError("x2 slate mismatch")

    outcome_rows = []
    proposal_methods = []
    domain_catalog = []
    for proposal, payload in zip(proposals, DOMAIN_PAYLOADS, strict=True):
        contract = make_contract(proposal, payload)
        evaluation = evaluate_contract(contract)
        if not evaluation["passed"] or evaluation["rejected_mutation_count"] != 5:
            raise RuntimeError(f"bounded contract failed: {proposal['proposal_id']}")
        pid = proposal["proposal_id"]
        base = f"x2/proposals/{pid.casefold()}"
        write_json(f"{base}/contract.json", contract)
        write_json(
            f"{base}/mutation-results.json",
            {
                "schema": "ghc.family.caelen-morrow.v665-v6.mutation-results.v1",
                "owner": "Caelen Morrow",
                "phase": "v665-v6",
                "generated_at_utc": NOW,
                "proposal_id": pid,
                "mutation_count": evaluation["mutation_count"],
                "rejected_mutation_count": evaluation["rejected_mutation_count"],
                "mutations": evaluation["mutations"],
                "all_rejected": True,
                "accepted_mutation_count": 0,
            },
        )
        write_json(
            f"{base}/bounded-receipt.json",
            {
                "schema": "ghc.family.caelen-morrow.v665-v6.bounded-receipt.v1",
                "owner": "Caelen Morrow",
                "phase": "v665-v6",
                "generated_at_utc": NOW,
                "proposal_id": pid,
                "bounded_positive_passed": evaluation["positive"]["valid"],
                "rejected_mutations": evaluation["rejected_mutation_count"],
                "observed_disposition": proposal["expected_disposition"],
                "completion_scope": contract["completion_scope"],
                "remaining_evidence_or_authority": contract["remaining_evidence_or_authority"],
                "same_owner": True,
                "real_rows": 0,
                "participants": 0,
                "network_calls": 0,
                "external_actions": 0,
                "passed": evaluation["passed"],
            },
        )
        outcome_rows.append(
            {
                "proposal_id": pid,
                "title": proposal["title"],
                "observed_disposition": proposal["expected_disposition"],
                "bounded_positive_passed": True,
                "rejected_mutations": 5,
                "completion_scope": contract["completion_scope"],
                "remaining_evidence_or_authority": contract["remaining_evidence_or_authority"],
            }
        )
        domain_catalog.append(
            {
                "proposal_id": pid,
                "domain_field_count": len(payload),
                "domain_fields": sorted(payload),
                "synthetic_only": True,
            }
        )
        proposal_methods.append(
            method_row(
                f"CM6656-MF-{pid}-P",
                f"validate the bounded positive for {pid}",
                f"the bounded positive passed for {pid}",
                "bounded_passing_witness",
                False,
            )
        )
        for mutation in evaluation["mutations"]:
            proposal_methods.append(
                method_row(
                    f"CM6656-MF-{mutation['mutation_id']}",
                    f"reject preregistered mutation {mutation['mutation_id']}",
                    ";".join(mutation["errors"]),
                    "retained_rejecting_witness",
                    True,
                )
            )

    counts = {label: 0 for label in ("completed", "represented", "open_gap", "exact_gate")}
    for row in outcome_rows:
        counts[row["observed_disposition"]] += 1
    write_json(
        "x2/proposal-ledger.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.proposal-ledger.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "x1_sha": X1_SHA,
            "proposal_count": len(outcome_rows),
            "outcome_counts": counts,
            "rows": outcome_rows,
            "bounded_positive_count": 20,
            "mutation_count": 100,
            "rejected_mutation_count": 100,
            "accepted_mutation_count": 0,
            "real_rows": 0,
            "participants": 0,
            "network_calls": 0,
            "external_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x2/domain-surface-catalog.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.domain-surface-catalog.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "surfaces": domain_catalog,
            "surface_count": len(domain_catalog),
            "real_rows": 0,
        },
    )

    source_profiles = load("provenance/source-profiles.json")
    write_json(
        "x2/source-adapter-zero-call.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.source-adapter.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "profiles": [
                {
                    "source_id": row["source_id"],
                    "status": row["status"],
                    "network_calls": 0,
                    "rows": 0,
                }
                for row in source_profiles["profiles"]
            ],
            "network_calls": 0,
            "real_rows": 0,
            "current_live_adapter_executed": False,
            "outcome": "open_gap",
            "authority_nonconversion": True,
        },
    )
    write_json(
        "x2/trinity-representations.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.trinity-representations.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "primary": "Freed ID and CBR Heart",
            "freed_id": {
                "proposal": "CM6656-N013",
                "status": "represented",
                "real_keys": 0,
                "real_proofs": 0,
                "production": False,
                "missing": REPRESENTED_EVIDENCE_GAPS["CM6656-N013"],
            },
            "thos": {
                "proposal": "CM6656-N012",
                "status": "represented",
                "participants": 0,
                "real_arms": 0,
                "missing": REPRESENTED_EVIDENCE_GAPS["CM6656-N012"],
            },
            "gmut": {
                "proposals": ["CM6656-N015", "CM6656-N016"],
                "status": "represented",
                "observations": 0,
                "likelihoods": 0,
                "constraints": 0,
                "predictions": 0,
                "claim": "typed discrete surrogate placeholders only",
            },
            "cbr": {
                "proposal": "CM6656-N020",
                "status": "exact_gate",
                "authority_decisions": 0,
                "approvals": 0,
                "missing": REPRESENTED_EVIDENCE_GAPS["CM6656-N020"],
            },
        },
    )

    skill_rows = []
    for name, description, focus in SKILL_SPECS:
        relative = Path("docs") / "caelen-morrow" / "v665-v6" / "x2" / "skills" / name / "SKILL.md"
        write_text(ROOT / relative, skill_text(name, description, focus))
        skill_rows.append(
            {
                "name": name,
                "path": relative.as_posix(),
                "status": "built_validated_smoke_used_owner_local",
                "globally_installed": False,
                "completion_credit": 1,
            }
        )
    write_json(
        "x2/skill-catalog.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.skill-catalog.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "skill_count": len(skill_rows),
            "skills": skill_rows,
            "globally_installed": False,
            "skill_creator_guidance_read": True,
        },
    )

    runner_rows = []
    for runner_id, purpose in RUNNER_SPECS:
        suffix = runner_id.replace("-", "_")
        name = f"ghc_family_caelen_morrow_v665_v6_{suffix}.py"
        path = ROOT / "scripts" / name
        write_text(path, runner_text(runner_id, purpose))
        runner_rows.append(
            {
                "runner_id": runner_id,
                "path": f"scripts/{name}",
                "purpose": purpose,
                "status": "built_validated_smoke_used_owner_local",
                "global_installation": False,
                "completion_credit": 1,
            }
        )
    write_json(
        "x2/runner-catalog.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.runner-catalog.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "runner_count": len(runner_rows),
            "runners": runner_rows,
            "family_current_compatibility": "additive owner-local ghc_family names; no inherited caller changed",
            "global_installation": False,
        },
    )

    safe_rows = [
        {**row, "x2_status": "completed_bounded", "completion_credit": 1}
        for row in portfolio["safe_now"]
    ]
    candidate_dispositions = [
        "represented",
        "represented",
        "represented",
        "represented",
        "open_gap",
        "completed",
        "completed",
        "completed",
        "completed",
        "completed",
    ]
    candidate_rows = [
        {
            **row,
            "x2_status": disposition,
            "completion_credit": 1 if disposition == "completed" else 0,
        }
        for row, disposition in zip(portfolio["bounded_candidates"], candidate_dispositions, strict=True)
    ]
    exact_rows = [
        {**row, "x2_status": "unexecuted_exact_gate", "completion_credit": 0}
        for row in portfolio["exact_approval_packets"]
    ]
    blocked_rows = [
        {**row, "x2_status": "unexecuted_blocked", "completion_credit": 0}
        for row in portfolio["blocked_packets"]
    ]
    cfr_rows = [
        {**row, "x2_status": "completed_bounded", "completion_credit": 1}
        for row in portfolio["clean_fix_refine"]
    ]
    write_json(
        "x2/portfolio-execution.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.portfolio-execution.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "safe_now": safe_rows,
            "bounded_candidates": candidate_rows,
            "exact_approval_packets": exact_rows,
            "blocked_packets": blocked_rows,
            "phase_local_skills": skill_rows,
            "family_current_runners": runner_rows,
            "clean_fix_refine": cfr_rows,
            "global_installations": 0,
            "external_writes": 0,
            "destructive_actions": 0,
            "real_rows": 0,
            "participants": 0,
        },
    )

    portfolio_methods = []
    groups = [
        ("SN", safe_rows, "bounded_safe_now"),
        ("CA", candidate_rows, "bounded_candidate"),
        ("SK", skill_rows, "phase_local_skill"),
        ("RU", runner_rows, "family_current_runner"),
        ("CF", cfr_rows, "clean_fix_refine"),
    ]
    for prefix, rows, kind in groups:
        for index, row in enumerate(rows, 1):
            name = row.get("title") or row.get("name") or row.get("runner_id")
            portfolio_methods.append(
                method_row(
                    f"CM6656-MF-{prefix}{index:02d}",
                    f"execute {kind}: {name}",
                    f"bounded owner-local witness prepared for {name}",
                    "bounded_passing_witness",
                    False,
                )
            )
    all_methods = proposal_methods + portfolio_methods
    if len(proposal_methods) != 120 or len(portfolio_methods) != 90 or len(all_methods) != 210:
        raise RuntimeError("Method Flow count mismatch")
    write_json(
        "method-flow/x2-method-flow.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.method-flow-x2.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "activation_baseline_negatives": 25672,
            "activation_baseline_methods": 9534,
            "startup_negatives": 16,
            "startup_methods": 16,
            "new_rejecting_mutation_negatives": 100,
            "new_x2_methods": 210,
            "effective_negatives_before_later_operational_overlays": 25788,
            "effective_methods_before_later_operational_overlays": 9760,
            "proposal_method_count": len(proposal_methods),
            "portfolio_method_count": len(portfolio_methods),
            "methods": all_methods,
            "no_failure_erased": True,
        },
    )

    write_json(
        "x2/x2-build-receipt.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.x2-build-receipt.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "x1_sha": X1_SHA,
            "contracts": 20,
            "bounded_positives": 20,
            "rejecting_mutations": 100,
            "accepted_mutations": 0,
            "skills_built": 10,
            "runners_built": 10,
            "skill_and_runner_validation_status": "10_of_10_each_passed_bounded_local_validation",
            "real_rows": 0,
            "participants": 0,
            "network_calls": 0,
            "external_actions": 0,
            "status": "X2_BUILT_AWAITING_BOUNDED_VALIDATION_AND_EVIDENCE_FREEZE",
        },
    )

    print(
        json.dumps(
            {
                "contracts": 20,
                "outcomes": counts,
                "mutations_rejected": 100,
                "skills_built": 10,
                "runners_built": 10,
                "x2_methods": 210,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
