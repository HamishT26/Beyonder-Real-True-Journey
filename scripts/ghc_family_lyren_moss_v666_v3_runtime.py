#!/usr/bin/env python3
"""Owner-local runtime for Lyren Moss v666-v3 synthetic contracts."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "lyren-moss" / "v666-v3"
X1_SHA = "e121ea6e207ea032edb1a0825ed86b1334481213"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED_CONTRACT_FIELDS = {
    "schema",
    "proposal_id",
    "title",
    "expected_disposition",
    "outcome",
    "synthetic_fixture",
    "real_data_rows",
    "network_calls",
    "external_actions",
    "positive_fixture",
    "invariant",
    "source_needs",
    "stop_conditions",
    "protected_gates",
    "claim_boundary",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def validate_contract(contract: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = sorted(REQUIRED_CONTRACT_FIELDS - set(contract))
    if missing:
        errors.append("missing_required_fields:" + ",".join(missing))
    proposal_id = contract.get("proposal_id")
    if not isinstance(proposal_id, str) or not re.fullmatch(r"LYR6663-N\d{3}", proposal_id):
        errors.append("invalid_proposal_id")
    if contract.get("expected_disposition") not in ALLOWED_OUTCOMES:
        errors.append("invalid_expected_disposition")
    if contract.get("outcome") != contract.get("expected_disposition"):
        errors.append("outcome_promotion_or_drift")
    if contract.get("synthetic_fixture") is not True:
        errors.append("synthetic_fixture_required")
    for field in ("real_data_rows", "network_calls", "external_actions"):
        if type(contract.get(field)) is not int or contract.get(field) != 0:
            errors.append(f"{field}_must_be_integer_zero")
    fixture = contract.get("positive_fixture")
    if not isinstance(fixture, dict):
        errors.append("positive_fixture_must_be_object")
    else:
        required_states = {"input_state", "provenance_state", "uncertainty_state", "authority_state", "output_state"}
        absent = sorted(required_states - set(fixture))
        if absent:
            errors.append("positive_fixture_missing_states:" + ",".join(absent))
        if fixture.get("authority_state") != "withheld":
            errors.append("authority_state_must_be_withheld")
        if fixture.get("output_state") not in {"bounded_structure_only", "represented_proxy_only", "open_gap_retained", "exact_gate_retained"}:
            errors.append("invalid_output_state")
    if contract.get("authority_claim"):
        errors.append("authority_claim_forbidden")
    if contract.get("stage20_claim"):
        errors.append("stage20_claim_forbidden")
    if contract.get("real_world_action"):
        errors.append("real_world_action_forbidden")
    if not isinstance(contract.get("protected_gates"), list) or len(contract.get("protected_gates", [])) < 10:
        errors.append("protected_gates_incomplete")
    if not isinstance(contract.get("stop_conditions"), list) or len(contract.get("stop_conditions", [])) < 5:
        errors.append("stop_conditions_incomplete")
    return not errors, errors


def mutations_for(contract: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    specs = [
        ("missing_required_field", lambda value: value.pop("proposal_id", None)),
        ("wrong_type_or_invalid_range", lambda value: value.__setitem__("real_data_rows", "zero")),
        ("provenance_or_authority_smuggling", lambda value: value.__setitem__("authority_claim", "professional response accepted")),
        ("real_world_or_production_action", lambda value: value.__setitem__("real_world_action", "command station recorder")),
        ("outcome_or_conformance_promotion", lambda value: value.__setitem__("stage20_claim", True)),
    ]
    for index, (kind, mutate) in enumerate(specs, 1):
        candidate = copy.deepcopy(contract)
        mutate(candidate)
        valid, errors = validate_contract(candidate)
        rows.append(
            {
                "mutation_id": f"{contract['proposal_id']}-M{index:02d}",
                "class": kind,
                "accepted": valid,
                "rejected": not valid,
                "errors": errors,
                "aggregate_credit": 0,
                "real_data_rows": 0,
                "network_calls": 0,
                "external_actions": 0,
                "retained": True,
            }
        )
    return rows


def git_blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{commit}:{path}"])


def replay_manifest(manifest_path: Path, commit: str) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    failures = []
    for entry in manifest["entries"]:
        try:
            blob = git_blob(commit, entry["path"])
        except subprocess.CalledProcessError as exc:
            failures.append({"path": entry["path"], "failure": f"missing_blob:{exc.returncode}"})
            continue
        observed = hashlib.sha256(blob).hexdigest()
        if observed != entry["sha256"] or len(blob) != entry["size_bytes"]:
            failures.append({"path": entry["path"], "failure": "sha_or_size_mismatch"})
    return {"entry_count": len(manifest["entries"]), "failure_count": len(failures), "failures": failures, "valid": not failures}


def proposal_directories() -> list[Path]:
    return sorted((PHASE_ROOT / "x2" / "proposals").glob("lyr6663-n*"))
