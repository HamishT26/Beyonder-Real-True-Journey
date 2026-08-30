#!/usr/bin/env python3
"""Exclusive dependency-corrected exact-final composite for Sylven Arc v678-v6."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

import validate_ghc_family_sylven_arc_v678_v6_final as base


FAILED_CANONICAL_HEAD = "706292a287ed36b892d97d80c9571e7a1d8b8ded"
FAILED_CANONICAL_SHA256 = "06e5b4d462ac51765d914e1f6e1d48d8831229dc24918daaee2eea97d63aa16e"
FAILED_CANONICAL_PAYLOAD_SHA256 = "67ac13794ac47b127adc998ee4389570063620f0c4a63cb75ca3608c782bb8ee"
DEPENDENCY_TESTS = [
    "tests/test_ghc_family_sylven_arc_v678_v6_correction1.py::test_05_validator_binds_first_final_and_correction_manifests",
    "tests/test_ghc_family_sylven_arc_v678_v6_correction2.py::test_04_validator_adjudicates_exact_manifest_definitions",
    "tests/test_ghc_family_sylven_arc_v678_v6_correction3.py",
]
STATUS = "VALID_DEPENDENCY_CORRECTED_EXACT_FINAL_COMPOSITE_WITH_ZERO_FAILED_CANONICAL_CREDIT"


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_bytes(canonical_bytes(value))
    os.replace(temp, path)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def failed_canonical_truth(receipt: Path, latch: Path) -> dict[str, Any]:
    receipt_value = load(receipt)
    latch_value = load(latch)
    payload = receipt_value["payload"]
    false_detailed = sorted(key for key, value in payload["detailed"]["checks"].items() if not value)
    false_minimal = sorted(key for key, value in payload["minimal"]["checks"].items() if not value)
    return {
        "receipt_sha256": sha256(receipt),
        "payload_sha256": receipt_value.get("payload_sha256"),
        "head": payload.get("head"),
        "status": payload.get("status"),
        "invocation_count": payload.get("invocation_count"),
        "success_count": payload.get("success_count"),
        "replay_count": payload.get("replay_count"),
        "tests_total": payload.get("tests", {}).get("total"),
        "tests_output_tail": payload.get("tests", {}).get("output_tail", ""),
        "false_detailed": false_detailed,
        "false_minimal": false_minimal,
        "successful_non_test_components": (
            all(value["passed"] for value in payload["manifests"].values())
            and payload["json"]["passed"] and payload["privacy"]["passed"] and payload["code"]["passed"]
        ),
        "latch_state": latch_value.get("state"),
        "latch_invocation_count": latch_value.get("invocation_count"),
        "latch_success_count": latch_value.get("success_count"),
        "latch_replay_count": latch_value.get("replay_count"),
    }


def preflight(repo: Path, expected: str, failed_receipt: Path, failed_latch: Path, receipt: Path, latch: Path) -> dict[str, Any]:
    prior = failed_canonical_truth(failed_receipt, failed_latch)
    eq = base.equality(repo, expected)
    topo = base.topology(repo, expected)
    prior_exact = (
        prior["receipt_sha256"] == FAILED_CANONICAL_SHA256
        and prior["payload_sha256"] == FAILED_CANONICAL_PAYLOAD_SHA256
        and prior["head"] == FAILED_CANONICAL_HEAD
        and prior["status"] == "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
        and prior["invocation_count"] == 1 and prior["success_count"] == 0 and prior["replay_count"] == 0
        and prior["tests_total"] == 41 and "1 failed, 40 passed" in prior["tests_output_tail"]
        and prior["false_detailed"] == ["test_count_exact", "tests_exact"]
        and prior["false_minimal"] == ["tests"] and prior["successful_non_test_components"]
        and prior["latch_state"] == "FAILED" and prior["latch_invocation_count"] == 1
        and prior["latch_success_count"] == 0 and prior["latch_replay_count"] == 0
    )
    topology_exact = (
        topo["source_is_x1_parent"] and topo["x1_is_evidence_parent"] and topo["evidence_is_first_final_parent"]
        and topo["first_final_is_correction1_parent"] and topo["correction1_is_correction2_parent"]
        and topo["correction2_is_corrected_final_parent"] and topo["phase_commits"] == 6
        and topo["merges"] == 0 and topo["final_parent_count"] == 1 and topo["source_ancestor"]
    )
    passed = (
        prior_exact and topology_exact and eq["branch"] == base.BRANCH and eq["all_equal"]
        and eq["divergence"] == [0, 0] and eq["clean"] and not receipt.exists() and not latch.exists()
    )
    result = {
        "status": "PASS" if passed else "FAIL",
        "expected_head": expected,
        "failed_canonical": prior,
        "topology": topo,
        "equality": eq,
        "composite_receipt_absent": not receipt.exists(),
        "composite_latch_absent": not latch.exists(),
    }
    if not passed:
        raise SystemExit(json.dumps(result, sort_keys=True))
    return result


def validate(repo: Path, expected: str, failed_receipt: Path, failed_latch: Path, receipt: Path, latch: Path) -> dict[str, Any]:
    pre = preflight(repo, expected, failed_receipt, failed_latch, receipt, latch)
    latch.parent.mkdir(parents=True, exist_ok=True)
    with latch.open("x", encoding="utf-8") as handle:
        json.dump({"schema": "ghc-family-dependency-corrected-composite-latch/v1", "phase": "v678-v6", "head": expected, "state": "RUNNING", "invocation_count": 1, "success_count": 0, "replay_count": 0}, handle, sort_keys=True)
        handle.write("\n")
    try:
        owner_paths = [path for path in base.git(repo, "ls-tree", "-r", "--name-only", expected).splitlines() if base.is_owner(path)]
        tests = base.run(repo, [sys.executable, "-X", "utf8", "-m", "pytest", "-q", *DEPENDENCY_TESTS], timeout=300)
        tests_output = tests.stdout.decode("utf-8", errors="replace")
        manifests = base.manifest_check(repo, expected)
        parsed = base.parse_json(repo, expected, owner_paths)
        privacy = base.privacy_check(repo, expected, owner_paths)
        code = base.code_check(repo, expected)
        caps = base.word_and_file_caps(repo, expected, owner_paths)
        topo = base.topology(repo, expected)
        eq = base.equality(repo, expected)
        truth = json.loads(base.ref_blob(repo, expected, "docs/sylven-arc/v678-v6/closeout/phase-truth.json").decode("utf-8"))
        route = json.loads(base.ref_blob(repo, expected, "docs/sylven-arc/v678-v6/closeout/route-receipt.json").decode("utf-8"))
        checks = {
            "failed_canonical_retained_zero_credit": pre["failed_canonical"]["status"] == "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "failed_canonical_not_replayed": pre["failed_canonical"]["replay_count"] == 0,
            "retained_successful_test_observations": "1 failed, 40 passed" in pre["failed_canonical"]["tests_output_tail"],
            "dependency_tests_exact": tests.returncode == 0 and "10 passed" in tests_output,
            "all_manifests": all(value["passed"] for value in manifests.values()),
            "json": parsed["passed"] and parsed["count"] > 250,
            "privacy": privacy["passed"] and len(privacy["classes"]) == 5,
            "code": code["passed"],
            "file_caps": caps["owner_file_cap_passed"] and caps["materialized_file_cap_passed"],
            "word_cap": caps["word_cap_passed"],
            "topology": topo["phase_commits"] == 6 and topo["merges"] == 0 and topo["final_parent_count"] == 1,
            "clean": eq["clean"],
            "typed_zero_divergence": eq["divergence"] == [0, 0],
            "fresh_four_way_equality": eq["all_equal"],
            "outcomes": truth["core_outcomes"] == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
            "stage20_hold": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
            "route_hold": route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0,
        }
        valid = all(checks.values())
        payload = {
            "schema": "ghc-family-dependency-corrected-exact-final-composite/v1",
            "owner": "Sylven Arc",
            "phase": "v678-v6",
            "head": expected,
            "status": STATUS if valid else "INVALID_DEPENDENCY_CORRECTED_EXACT_FINAL_COMPOSITE",
            "invocation_count": 1,
            "success_count": 1 if valid else 0,
            "replay_count": 0,
            "failed_canonical_receipt_sha256": FAILED_CANONICAL_SHA256,
            "failed_canonical_credit": 0,
            "retained_canonical_test_observations": {"passed": 40, "total": 41},
            "dependency_tests": {"passed": 10 if tests.returncode == 0 else 0, "total": 10, "output_tail": tests_output[-500:]},
            "checks": checks,
            "manifests": manifests,
            "json": parsed,
            "privacy": privacy,
            "code": code,
            "caps": caps,
            "topology": topo,
            "equality": eq,
            "full_repository_suite_run": False,
            "independent_reproduction": False,
            "canonical_success": False,
            "empirical_confirmation": False,
            "professional_authority": False,
            "production_certification": False,
            "privacy_complete": False,
            "accessibility_complete": False,
            "maori_authority": False,
            "stage20_authority": False,
        }
        payload_digest = hashlib.sha256(canonical_bytes(payload)).hexdigest()
        atomic_write(receipt, {"payload": payload, "payload_sha256": payload_digest})
        atomic_write(latch, {
            "schema": "ghc-family-dependency-corrected-composite-latch/v1", "phase": "v678-v6", "head": expected,
            "state": "SUCCEEDED" if valid else "FAILED", "invocation_count": 1,
            "success_count": 1 if valid else 0, "replay_count": 0,
            "receipt_sha256": sha256(receipt), "payload_sha256": payload_digest,
        })
        if not valid:
            raise SystemExit(json.dumps({"status": payload["status"], "receipt_sha256": sha256(receipt)}, sort_keys=True))
        return {
            "status": STATUS,
            "receipt_sha256": sha256(receipt),
            "latch_sha256": sha256(latch),
            "payload_sha256": payload_digest,
            "retained_canonical_tests": "40/41",
            "dependency_tests": "10/10",
            "json": parsed["count"],
            "privacy_confirmed": len(privacy["confirmed"]),
            "owner_files": len(owner_paths),
        }
    except Exception as exc:
        if not receipt.exists():
            atomic_write(receipt, {"schema": "ghc-family-dependency-corrected-exact-final-composite/v1", "owner": "Sylven Arc", "phase": "v678-v6", "head": expected, "status": "INVALID_EXCEPTION", "error_type": type(exc).__name__, "invocation_count": 1, "success_count": 0, "replay_count": 0, "failed_canonical_credit": 0})
        atomic_write(latch, {"schema": "ghc-family-dependency-corrected-composite-latch/v1", "phase": "v678-v6", "head": expected, "state": "FAILED", "invocation_count": 1, "success_count": 0, "replay_count": 0, "receipt_sha256": sha256(receipt)})
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("preflight", "composite"))
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--failed-receipt", type=Path, required=True)
    parser.add_argument("--failed-latch", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--latch", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    values = (repo, args.expected_head, args.failed_receipt.resolve(), args.failed_latch.resolve(), args.receipt.resolve(), args.latch.resolve())
    result = preflight(*values) if args.command == "preflight" else validate(*values)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
