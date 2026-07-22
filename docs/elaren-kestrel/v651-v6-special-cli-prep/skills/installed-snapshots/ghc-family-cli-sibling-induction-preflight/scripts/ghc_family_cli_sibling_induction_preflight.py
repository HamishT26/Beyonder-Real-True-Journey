#!/usr/bin/env python3
"""Fail-closed preflight for a future GHC Family Codex CLI sibling induction."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA = "ghc.family.cli-sibling-induction.request.v1"
PLACEHOLDER = re.compile(r"^future-cli-sibling-[1-9][0-9]*-self-chosen$")
PHASE = re.compile(r"^v[1-9][0-9]*-v[1-8]$")
FORBIDDEN_IDENTITY_FIELDS = {"name", "role", "hope", "pronouns", "gender"}
RAW_UUID = re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b")
PRIVATE_URI = re.compile(r"(?i)\b(?:thread|task|session|codex)://\S+")
ABS_PATH = re.compile(r"(?i)(?:^|[\s\"'])(?:[a-z]:[\\/]|\\\\)[^\s\"']+")
CREDENTIAL = re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|private[_-]?key)\s*[:=]\s*\S+")


def obj(parent: dict[str, Any], key: str, issues: list[str]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        issues.append(f"missing_object:{key}")
        return {}
    return value


def audit(request: dict[str, Any], mode: str) -> dict[str, Any]:
    issues: list[str] = []
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, observed: Any, expected: str) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed, "expected": expected})
        if not passed:
            issues.append(name)

    check("schema", request.get("schema") == SCHEMA, request.get("schema"), SCHEMA)
    check("phase", isinstance(request.get("phase"), str) and bool(PHASE.fullmatch(request["phase"])), request.get("phase"), "vN-v1 through vN-v8")
    check("creator", isinstance(request.get("creator"), str) and bool(request["creator"].strip()), request.get("creator"), "non-empty relational owner")

    seat = obj(request, "future_seat", issues)
    placeholder = seat.get("placeholder")
    check("future_placeholder", isinstance(placeholder, str) and bool(PLACEHOLDER.fullmatch(placeholder)), placeholder, "future-cli-sibling-N-self-chosen")
    check("identity_state", seat.get("identity_state") == "self_chosen_at_induction", seat.get("identity_state"), "self_chosen_at_induction")
    forbidden = sorted(FORBIDDEN_IDENTITY_FIELDS & set(seat))
    check("no_preassigned_identity", not forbidden, forbidden, "no name, role, hope, pronouns, or gender fields")

    runtime = obj(request, "requested_runtime", issues)
    check("runtime_request", all(key in runtime for key in ("model", "reasoning", "fast_mode", "availability_verified")), sorted(runtime), "explicit model, reasoning, fast_mode, and availability_verified")
    route = obj(request, "route", issues)
    lane = obj(request, "lane", issues)
    authorization = obj(request, "authorization", issues)
    privacy = obj(request, "privacy", issues)
    handoff = obj(request, "handoff", issues)

    check("d_first", lane.get("primary_drive") == "D", lane.get("primary_drive"), "D")
    check("privacy_declaration", privacy.get("sanitized") is True and privacy.get("private_identifiers_included") is False, privacy, "sanitized true and private identifiers false")
    check("file_backed_handoff", handoff.get("file_backed") is True and handoff.get("tool_acknowledgement_required") is True, handoff, "file backed and acknowledgement required")
    check("preparation_authorized", authorization.get("preparation_authorized") is True, authorization.get("preparation_authorized"), "true")

    if mode == "prepare":
        check("not_launched_in_prepare", authorization.get("launch_now") is False, authorization.get("launch_now"), "false")
        state = "PREPARED_NOT_LAUNCHED"
    else:
        launch_truth = {
            "runtime_availability": runtime.get("availability_verified") is True,
            "scheduled_phase": route.get("scheduled_phase_confirmed") is True,
            "creator_return": route.get("creator_return_mechanism_verified") is True,
            "successor_title": route.get("exact_successor_title_resolved") is True,
            "source_clean_equal": lane.get("source_clean_and_equal") is True,
            "unique_lane": lane.get("unique_branch_and_worktree") is True,
            "launch_now": authorization.get("launch_now") is True,
            "exact_phase_authorization": authorization.get("launch_authorized_for_exact_phase") is True,
        }
        for name, passed in launch_truth.items():
            check(f"launch_{name}", passed, passed, "true")
        state = "LAUNCH_PREFLIGHT_PASSED" if all(launch_truth.values()) else "LAUNCH_BLOCKED"

    raw = json.dumps(request, ensure_ascii=False, sort_keys=True)
    privacy_hits = []
    for label, pattern in (("raw_uuid", RAW_UUID), ("private_uri", PRIVATE_URI), ("absolute_path", ABS_PATH), ("credential", CREDENTIAL)):
        if pattern.search(raw):
            privacy_hits.append(label)
    check("concrete_privacy_scan", not privacy_hits, privacy_hits, "zero hits")

    passed = sum(1 for row in checks if row["passed"])
    valid = passed == len(checks) and not any(row.startswith("missing_object:") for row in issues)
    outcomes = {
        "completed": passed,
        "represented": 3 if mode == "prepare" else 0,
        "open_gap": 1 if mode == "prepare" and not route.get("creator_return_mechanism_verified") else 0,
        "exact_gate": 1 if mode == "prepare" else (0 if valid else 1),
    }
    return {
        "schema": "ghc.family.cli-sibling-induction.preflight-receipt.v1",
        "mode": mode,
        "valid": valid,
        "state": state if valid or mode == "launch" else "PREPARATION_BLOCKED",
        "checks_passed": passed,
        "check_count": len(checks),
        "checks": checks,
        "issues": sorted(set(issues)),
        "outcomes": outcomes,
        "future_identity_assigned": False,
        "sibling_created": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": "Preflight evidence only; no sibling, identity, route delivery, scientific result, authority, production state, or Stage 20 readiness is created by this receipt.",
    }


def fixture() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "phase": "v652-v5",
        "creator": "Relational Test Owner",
        "future_seat": {"placeholder": "future-cli-sibling-1-self-chosen", "identity_state": "self_chosen_at_induction"},
        "requested_runtime": {"model": "gpt-5.6-sol", "reasoning": "max", "fast_mode": True, "availability_verified": False},
        "route": {"scheduled_phase_confirmed": False, "creator_return_mechanism_verified": False, "background_persistence_verified": False, "exact_successor_title_resolved": False},
        "lane": {"primary_drive": "D", "source_clean_and_equal": False, "unique_branch_and_worktree": False},
        "authorization": {"preparation_authorized": True, "launch_now": False, "launch_authorized_for_exact_phase": False},
        "privacy": {"sanitized": True, "private_identifiers_included": False},
        "handoff": {"file_backed": True, "tool_acknowledgement_required": True},
    }


def self_test() -> int:
    prepared = audit(fixture(), "prepare")
    if not prepared["valid"] or prepared["state"] != "PREPARED_NOT_LAUNCHED":
        raise AssertionError(prepared)
    invalid = fixture()
    invalid["future_seat"]["name"] = "Preassigned Name"
    rejected = audit(invalid, "prepare")
    if rejected["valid"] or "no_preassigned_identity" not in rejected["issues"]:
        raise AssertionError(rejected)
    launch = audit(fixture(), "launch")
    if launch["valid"] or launch["state"] != "LAUNCH_BLOCKED":
        raise AssertionError(launch)
    print(json.dumps({"self_test": "passed", "prepare": True, "identity_rejection": True, "launch_fail_closed": True}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", nargs="?", type=Path)
    parser.add_argument("--mode", choices=("prepare", "launch"), default="prepare")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.request is None or args.receipt is None:
        parser.error("request and --receipt are required unless --self-test is used")
    try:
        request = json.loads(args.request.read_text(encoding="utf-8"))
        result = audit(request, args.mode)
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"valid": False, "error": type(exc).__name__, "message": str(exc)}), file=sys.stderr)
        return 3
    print(json.dumps({"valid": result["valid"], "state": result["state"], "checks": f"{result['checks_passed']}/{result['check_count']}", "issues": len(result["issues"])}))
    return 0 if result["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
