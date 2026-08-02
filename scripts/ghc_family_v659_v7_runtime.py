#!/usr/bin/env python3
"""Shared bounded synthetic runtime for Tamar Vey v659-v7."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v659_v7_x2_data as d
import ghc_family_v659_v5_runtime as orin_runtime
import ghc_family_v659_v6_runtime as liora_runtime


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
LEDGER = PHASE / "preregistration/proposal-ledger.json"
LATEST_SCAN_BYTE_CAP = 2 * 1024 * 1024
PROTECTED_CLAIM_KEYS = [
    "empirical",
    "participant",
    "professional",
    "production",
    "deployment",
    "legal",
    "cultural",
    "maori_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_asi",
    "consciousness_personhood",
    "theory_of_everything",
    "stage20",
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def proposal_rows() -> list[dict[str, Any]]:
    payload = json.loads(LEDGER.read_text(encoding="utf-8"))
    rows = payload["proposals"]
    if len(rows) != d.CURRENT_PORTFOLIO_COUNT:
        raise RuntimeError("Tamar proposal ledger count drift")
    return rows


def proposal_by_slug(slug: str) -> dict[str, Any]:
    matches = [row for row in proposal_rows() if row["slug"] == slug]
    if len(matches) != 1:
        raise KeyError(slug)
    return matches[0]


def required_obligations(proposal: dict[str, Any]) -> list[str]:
    mechanism_terms = sorted(set(re.findall(r"[a-z0-9]+", proposal["mechanism"].lower())))
    return [
        "synthetic-only",
        "source-labels-present",
        "decision-abstention",
        "rollback-present",
        f"mechanism-token:{'-'.join(mechanism_terms[:5])}",
    ]


def build_new_contract(proposal: dict[str, Any]) -> dict[str, Any]:
    obligations = required_obligations(proposal)
    return {
        "schema": "ghc.family.v659-v7.synthetic-contract.v1",
        "proposal_id": proposal["proposal_id"],
        "slug": proposal["slug"],
        "title": proposal["title"],
        "origin": proposal["origin"],
        "outcome": proposal["expected_disposition"],
        "pillar_relation": proposal["pillar_relation"],
        "mechanism": proposal["mechanism"],
        "approval_class": proposal["approval_class"],
        "execution_lane": proposal["execution_lane"],
        "source_ids": proposal["official_or_primary_source_needs"],
        "required_obligations": obligations,
        "protected_gates": proposal["protected_gates"],
        "fixture": {
            "fixture_id": f"{proposal['proposal_id']}-SYNTHETIC-VALID",
            "synthetic_only": True,
            "real_people_textiles_fibres_yarns_dyes_finishes_looms_tools_samples_measurements_media_records_identifiers_treatments_or_authority_cases_used": False,
            "network_called": False,
            "external_rows": 0,
            "source_labels_present": True,
            "decision_abstention": True,
            "rollback_present": True,
            "obligations_present": obligations,
            "protected_claims": {key: False for key in PROTECTED_CLAIM_KEYS},
            "authority_action_executed": False,
            "operation_release_or_suitability_decision": False,
            "evidence_digest_algorithm": "sha256",
        },
        "boundary": (
            "Synthetic same-owner structural evidence only; no real owner, custodian, conservator, curator, textile specialist, weaver, textile, fibre, yarn, dye, finish, loom, tool, sample, chemical, image, record, measurement, cleaning, stitching, treatment, participant, "
            "conservation, material identification, structural safety, chemical safety, heritage, privacy, access, release, remedy, production, legal, cultural, collective-governance, Māori-authority, privacy-complete, "
            "accessibility-complete, exhaustive-security, independent-reproduction, personhood, or Stage 20 claim."
        ),
    }


def validate_new_contract(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_top = {
        "schema", "proposal_id", "slug", "title", "origin", "outcome", "pillar_relation",
        "mechanism", "approval_class", "execution_lane", "source_ids", "required_obligations",
        "protected_gates", "fixture", "boundary",
    }
    missing_top = sorted(required_top - set(contract))
    errors.extend(f"missing_top:{key}" for key in missing_top)
    if missing_top:
        return errors
    if contract["schema"] != "ghc.family.v659-v7.synthetic-contract.v1":
        errors.append("schema_drift")
    if contract["outcome"] not in d.ALLOWED_OUTCOMES:
        errors.append("outcome_not_allowed")
    if contract["origin"] != "new_unique_v659_v7_proposal":
        errors.append("origin_not_new_unique")
    if not contract["source_ids"]:
        errors.append("source_ids_empty")
    if not contract["protected_gates"]:
        errors.append("protected_gates_empty")
    if not str(contract["boundary"]).startswith("Synthetic same-owner"):
        errors.append("boundary_missing")

    fixture = contract["fixture"]
    required_fixture = {
        "fixture_id", "synthetic_only",
        "real_people_textiles_fibres_yarns_dyes_finishes_looms_tools_samples_measurements_media_records_identifiers_treatments_or_authority_cases_used",
        "network_called", "external_rows", "source_labels_present", "decision_abstention",
        "rollback_present", "obligations_present", "protected_claims", "authority_action_executed",
        "operation_release_or_suitability_decision", "evidence_digest_algorithm",
    }
    missing_fixture = sorted(required_fixture - set(fixture))
    errors.extend(f"missing_fixture:{key}" for key in missing_fixture)
    if missing_fixture:
        return errors
    if fixture["synthetic_only"] is not True:
        errors.append("not_synthetic_only")
    if fixture["real_people_textiles_fibres_yarns_dyes_finishes_looms_tools_samples_measurements_media_records_identifiers_treatments_or_authority_cases_used"] is not False:
        errors.append("real_data_or_object_promoted")
    if fixture["network_called"] is not False or fixture["external_rows"] != 0:
        errors.append("external_state_promoted")
    if fixture["source_labels_present"] is not True:
        errors.append("source_labels_missing")
    if fixture["decision_abstention"] is not True:
        errors.append("decision_abstention_missing")
    if fixture["rollback_present"] is not True:
        errors.append("rollback_missing")
    if fixture["obligations_present"] != contract["required_obligations"]:
        errors.append("obligation_mismatch")
    if set(fixture["protected_claims"]) != set(PROTECTED_CLAIM_KEYS):
        errors.append("protected_claim_keys_drift")
    else:
        errors.extend(
            f"protected_claim_promoted:{key}"
            for key, value in fixture["protected_claims"].items()
            if value is not False
        )
    if fixture["authority_action_executed"] is not False:
        errors.append("authority_action_promoted")
    if fixture["operation_release_or_suitability_decision"] is not False:
        errors.append("release_decision_promoted")
    if fixture["evidence_digest_algorithm"] != "sha256":
        errors.append("digest_algorithm_drift")
    return errors


def mutation_catalogue(contract: dict[str, Any]) -> list[dict[str, Any]]:
    mutations: list[dict[str, Any]] = []

    candidate = copy.deepcopy(contract)
    candidate["fixture"]["obligations_present"] = candidate["fixture"]["obligations_present"][1:]
    mutations.append({"mutation_id": "drop-obligation", "candidate": candidate})

    candidate = copy.deepcopy(contract)
    candidate["fixture"]["real_people_textiles_fibres_yarns_dyes_finishes_looms_tools_samples_measurements_media_records_identifiers_treatments_or_authority_cases_used"] = True
    mutations.append({"mutation_id": "promote-real-data-or-object", "candidate": candidate})

    candidate = copy.deepcopy(contract)
    candidate["fixture"]["source_labels_present"] = False
    mutations.append({"mutation_id": "drop-source-label", "candidate": candidate})

    candidate = copy.deepcopy(contract)
    candidate["fixture"]["protected_claims"]["stage20"] = True
    mutations.append({"mutation_id": "promote-stage20", "candidate": candidate})

    candidate = copy.deepcopy(contract)
    candidate["fixture"]["authority_action_executed"] = True
    mutations.append({"mutation_id": "promote-authority-action", "candidate": candidate})
    return mutations


def evaluate_new_surface(slug: str) -> dict[str, Any]:
    proposal = proposal_by_slug(slug)
    if proposal["origin"] != "new_unique_v659_v7_proposal":
        raise ValueError(f"{slug} is not a new Tamar v659-v7 surface")
    contract = build_new_contract(proposal)
    valid_errors = validate_new_contract(contract)
    mutations = []
    for mutation in mutation_catalogue(contract):
        errors = validate_new_contract(mutation["candidate"])
        mutations.append(
            {
                "mutation_id": f"{proposal['proposal_id']}-{mutation['mutation_id']}",
                "rejected": bool(errors),
                "error_codes": errors,
                "credit": 0,
                "retained": True,
                "authority_action_executed": False,
            }
        )
    return {
        "schema": "ghc.family.v659-v7.surface-evaluation.v1",
        "contract": contract,
        "valid_errors": valid_errors,
        "mutation_results": mutations,
        "valid_fixture_passed": not valid_errors,
        "rejected_mutation_count": sum(row["rejected"] for row in mutations),
        "all_mutations_rejected": all(row["rejected"] for row in mutations),
        "same_owner_only": True,
        "independent_reproduction": False,
        "authority_action_executed": False,
    }


def evaluate_selected_surface(current_slug: str) -> dict[str, Any]:
    proposal = proposal_by_slug(current_slug)
    if proposal["origin"] != "selected_inherited_bounded_revalidation_no_credit":
        raise ValueError(f"{current_slug} is not a selected inherited surface")
    source_slug = proposal["slug"]
    if proposal["source_proposal_id"].startswith("V6596-"):
        source_runtime = liora_runtime
        expected_origin = "new_unique_v659_v6_proposal"
        source_runtime_path = "scripts/ghc_family_v659_v6_runtime.py"
    elif proposal["source_proposal_id"].startswith("V6595-"):
        source_runtime = orin_runtime
        expected_origin = "new_unique_v659_v5_proposal"
        source_runtime_path = "scripts/ghc_family_v659_v5_runtime.py"
    else:
        raise RuntimeError(f"selected source phase unsupported for {current_slug}")
    source_proposal = source_runtime.proposal_by_slug(source_slug)
    if source_proposal["proposal_id"] != proposal["source_proposal_id"]:
        raise RuntimeError(f"selected source identity drift for {current_slug}")
    if source_proposal["origin"] != expected_origin:
        raise RuntimeError(f"selected source origin drift for {current_slug}")
    source = source_runtime.evaluate_new_surface(source_slug)
    source_contract = source["contract"]
    mutations = [
        {
            **row,
            "source_mutation_id": row["mutation_id"],
            "mutation_id": f"{proposal['proposal_id']}-{row['mutation_id'].split('-', 1)[-1]}",
        }
        for row in source["mutation_results"]
    ]
    return {
        "schema": "ghc.family.v659-v7.selected-revalidation.v1",
        "proposal_id": proposal["proposal_id"],
        "slug": current_slug,
        "source_proposal_id": proposal["source_proposal_id"],
        "source_slug": source_slug,
        "append_to_frozen_chain": False,
        "source_runtime": source_runtime_path,
        "source_contract": source_contract,
        "valid_errors": source["valid_errors"],
        "mutation_results": mutations,
        "valid_fixture_passed": source["valid_fixture_passed"],
        "rejected_mutation_count": sum(row["rejected"] for row in mutations),
        "all_mutations_rejected": all(row["rejected"] for row in mutations),
        "same_owner_only": True,
        "independent_reproduction": False,
        "authority_action_executed": False,
        "boundary": "Bounded same-owner revalidation of an immutable source runtime; not independent reproduction or new chain growth.",
    }


def select_latest_tracked_paths(limit: int = d.LATEST_TRACKED_SCAN_CAP) -> dict[str, Any]:
    if limit < 1 or limit > d.LATEST_TRACKED_SCAN_CAP:
        raise ValueError("latest tracked path limit is outside the frozen cap")
    tracked_raw = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "-z"])
    tracked = {row.decode("utf-8") for row in tracked_raw.split(b"\0") if row}
    command = [
        "git", "-C", str(ROOT), "-c", "core.quotepath=false", "log",
        "--no-renames", "--diff-filter=ACMR", "--name-only",
        "--pretty=format:@@GHC-COMMIT@@%H", "HEAD",
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    selected: list[str] = []
    seen: set[str] = set()
    group: list[str] = []
    commits_examined = 0

    def flush_group() -> None:
        for relative in sorted(set(group)):
            if relative in tracked and relative not in seen:
                selected.append(relative)
                seen.add(relative)
                if len(selected) >= limit:
                    break

    try:
        assert process.stdout is not None
        for raw_line in process.stdout:
            line = raw_line.rstrip("\r\n")
            if line.startswith("@@GHC-COMMIT@@"):
                if group:
                    flush_group()
                    group.clear()
                if len(selected) >= limit:
                    break
                commits_examined += 1
            elif line:
                group.append(line)
        if len(selected) < limit and group:
            flush_group()
    finally:
        if process.poll() is None:
            process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10)
    if len(selected) != limit:
        raise RuntimeError(f"latest tracked selector produced {len(selected)} paths, expected {limit}")
    return {
        "paths": selected,
        "tracked_path_count": len(tracked),
        "commits_examined": commits_examined,
        "ordered_path_sha256": hashlib.sha256(("\n".join(selected) + "\n").encode("utf-8")).hexdigest(),
    }


def scan_latest_tracked_files(limit: int = d.LATEST_TRACKED_SCAN_CAP) -> dict[str, Any]:
    selection = select_latest_tracked_paths(limit)
    patterns = {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "credential_or_private_key": re.compile(rb"(?<![A-Za-z0-9])(?:sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"),
        "delegation_markup": re.compile(rb"<(?:codex_delegation|source_thread_id)>", re.I),
        "transcript_or_session": re.compile(
            b"(?:" + b"|".join([b"raw " + b"transcript", b"session " + b"stream", b"private " + b"app state"]) + b")",
            re.I,
        ),
    }
    class_counts: Counter[str] = Counter()
    candidates: list[dict[str, Any]] = []
    confirmed_high_risk: list[dict[str, Any]] = []
    binary_files = 0
    truncated_files = 0
    bytes_scanned = 0
    missing_paths: list[str] = []
    for relative in selection["paths"]:
        path = ROOT / relative
        if not path.is_file():
            missing_paths.append(relative)
            continue
        size = path.stat().st_size
        with path.open("rb") as handle:
            data = handle.read(LATEST_SCAN_BYTE_CAP + 1)
        if len(data) > LATEST_SCAN_BYTE_CAP:
            data = data[:LATEST_SCAN_BYTE_CAP]
            truncated_files += 1
        bytes_scanned += len(data)
        if b"\x00" in data:
            binary_files += 1
        for label, pattern in patterns.items():
            match_count = len(pattern.findall(data))
            if not match_count:
                continue
            class_counts[label] += match_count
            row = {"path": relative, "class": label, "match_count": match_count, "matched_value_published": False}
            candidates.append(row)
            if label == "credential_or_private_key":
                confirmed_high_risk.append(row)
    return {
        "schema": "ghc.family.latest-tracked-file-scan.v1",
        "head": subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True, encoding="utf-8").strip(),
        "selection_method": "newest commits first, paths sorted within commit, currently tracked paths deduplicated, stop at exact cap",
        "selected_file_count": len(selection["paths"]),
        "tracked_path_count": selection["tracked_path_count"],
        "commits_examined": selection["commits_examined"],
        "ordered_path_sha256": selection["ordered_path_sha256"],
        "per_file_byte_cap": LATEST_SCAN_BYTE_CAP,
        "bytes_scanned": bytes_scanned,
        "binary_file_count": binary_files,
        "truncated_file_count": truncated_files,
        "missing_path_count": len(missing_paths),
        "missing_paths": missing_paths,
        "pattern_classes": list(patterns),
        "review_candidate_count": len(candidates),
        "review_candidate_class_counts": dict(class_counts),
        "review_candidates": candidates,
        "confirmed_high_risk_count": len(confirmed_high_risk),
        "confirmed_high_risk": confirmed_high_risk,
        "matched_values_published": False,
        "privacy_complete": False,
        "security_complete": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": "Bounded latest-file triage only; candidate matches are not secret publication or complete privacy/security assurance.",
    }


def surface_cli(slug: str) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = evaluate_new_surface(slug)
    receipt = {
        "schema": "ghc.family.v659-v7.runner-receipt.v1",
        "runner_surface": slug,
        "proposal_id": result["contract"]["proposal_id"],
        "valid_fixture_passed": result["valid_fixture_passed"],
        "expected_mutation_count": 5,
        "rejected_mutation_count": result["rejected_mutation_count"],
        "all_mutations_rejected": result["all_mutations_rejected"],
        "valid": result["valid_fixture_passed"] and result["all_mutations_rejected"],
        "same_owner_only": True,
        "independent_reproduction": False,
        "authority_action_executed": False,
        "boundary": result["contract"]["boundary"],
    }
    write_json(args.output, receipt)
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    if not receipt["valid"]:
        raise SystemExit(1)


def latest_scan_cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipt = scan_latest_tracked_files()
    write_json(args.output, receipt)
    summary = {
        "selected_file_count": receipt["selected_file_count"],
        "review_candidate_count": receipt["review_candidate_count"],
        "confirmed_high_risk_count": receipt["confirmed_high_risk_count"],
        "missing_path_count": receipt["missing_path_count"],
    }
    print(json.dumps(summary, sort_keys=True))
    if receipt["missing_path_count"] or receipt["confirmed_high_risk_count"]:
        raise SystemExit(1)
