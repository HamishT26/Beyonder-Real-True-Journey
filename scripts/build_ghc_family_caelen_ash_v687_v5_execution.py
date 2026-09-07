#!/usr/bin/env python3
"""Execute Caelen Ash v687-v5 frozen contracts in one isolated D-drive runtime."""

from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import sys

import gemmi
import networkx as nx
import numpy as np

from build_ghc_family_caelen_ash_v687_v5_x1 import BASE, BOUNDARY, GATES
from ghc_family_caelen_ash_v687_v5_core import mutated_results, run, strict_equal, strict_load


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / BASE
X2 = PHASE / "x2"


def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def write(relative: str, value) -> None:
    path = X2 / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(value.encode("utf-8") if isinstance(value, str) else encoded(value))


def write_or_verify(relative: str, value) -> None:
    path = X2 / relative
    expected = value.encode("utf-8") if isinstance(value, str) else encoded(value)
    if path.exists():
        if path.read_bytes() != expected:
            raise SystemExit("existing package receipt differs: " + relative)
        return
    write(relative, value)


def make_operational_ledger() -> dict:
    failures = [
        (
            "CA6875-X2-N001",
            "The first directory-setup wrapper used New-Item -LiteralPath, which this PowerShell runtime rejected; venv independently created the runtime while the cache remained absent.",
            "Audit both exact D-drive targets, retain the partial result, and create only the absent cache with New-Item -Path.",
        ),
        (
            "CA6875-X2-N002",
            "The first installation projection ended after the installing stream and did not expose its completion, dependency-check, or version tail, so it earned no pass credit at that point.",
            "Do not reinstall blindly; audit the exact environment with pip list, pip check, and importlib.metadata version bindings.",
        ),
        (
            "CA6875-X2-N003",
            "The first inline Gemmi smoke encoded Python newlines as literal backslash-n text and raised SyntaxError before the package operation.",
            "Move the smoke into this committed standalone builder and preserve a positive CIF parse beside an adverse missing-tag refusal.",
        ),
        (
            "CA6875-X2-N004",
            "The first inline NumPy smoke encoded Python newlines as literal backslash-n text and raised SyntaxError before the package operation.",
            "Move the smoke into this committed standalone builder and preserve matrix inversion beside singular-matrix refusal.",
        ),
        (
            "CA6875-X2-N005",
            "The first inline NetworkX smoke encoded Python newlines as literal backslash-n text and raised SyntaxError before the package operation.",
            "Move the smoke into this committed standalone builder and preserve deterministic DAG order beside cycle refusal.",
        ),
        (
            "CA6875-X2-N006",
            "The first standalone executor stopped with frozen contract mismatch because the copied structural core still exposed only its inherited operation names.",
            "Retain the failed aggregate and bind each crystallographic x1 operation name explicitly to its inspected structural implementation before rerunning only the owner-local execution.",
        ),
        (
            "CA6875-X2-N007",
            "The first mismatch diagnostic inherited the same missing operation-name binding and stopped at the first unknown crystallographic operation.",
            "Inspect the operation registry itself, add the explicit ten-name mapping, then rerun the bounded mismatch diagnostic before the executor.",
        ),
        (
            "CA6875-X2-N008",
            "The first successful OSV response projection treated each missing vulns property as a one-element null array and falsely reported one null advisory per package.",
            "Repeat only the three-version OSV batch with an explicit non-null filter and retain the corrected time-bounded snapshot separately from exhaustive-security claims.",
        ),
        (
            "CA6875-X2-N009",
            "The first skill-validation wrapper attempted to assign PowerShell's read-only Host variable, then passed no usable host-Python executable to quick validation.",
            "Retain the failed three-file runtime directory, prove zero promotion targets changed, and run the same validator once in a fresh r2 evidence directory with an explicit executable argument.",
        ),
        (
            "CA6875-X2-N010",
            "The first global-install validation receipt labeled five locally smoked interfaces as shared-interface smokes before the copied global interfaces had been executed.",
            "Preserve parity separately, directly smoke each of the five copied global interfaces once, and correct the receipt to distinguish local from global execution.",
        ),
    ]
    methods, witnesses, events = [], [], []
    for index, (negative_id, failure, recovery) in enumerate(failures, 1):
        method_id = f"CA6875-X2-OP-M{index:03d}"
        failed_id = method_id + "-W-FAIL"
        passed_id = method_id + "-W-PASS"
        methods.append(
            {
                "method_id": method_id,
                "title": "Retain and recover " + negative_id,
                "failure_signature": failure,
                "trigger_preconditions": ["Caelen v687-v5 owner-local x2 package or runtime operation"],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now",
                "candidate_workaround": recovery,
                "validation_witness_ids": [failed_id, passed_id],
                "recurrence_guard": recovery,
                "rollback": "Stop the affected owner-local operation without changing the host interpreter, source branch, sibling lane, or protected gate.",
                "recommendation_state": "preferred",
                "supersedes": [],
                "protected_gates": GATES,
                "retained_negative_ids": [negative_id],
                "scope_boundary": BOUNDARY,
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": failed_id,
                    "method_id": method_id,
                    "procedure": "Original bounded operation",
                    "scope": "Owner-local runtime setup or package smoke",
                    "expected": "Attributable bounded result",
                    "observed": failure,
                    "result": "fail",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [negative_id],
                    "boundary": BOUNDARY,
                },
                {
                    "witness_id": passed_id,
                    "method_id": method_id,
                    "procedure": "Exact bounded recovery",
                    "scope": "Owner-local runtime setup or package smoke",
                    "expected": recovery,
                    "observed": "Recovery passed in the exclusive owner runtime without host or sibling mutation.",
                    "result": "pass",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [negative_id],
                    "boundary": BOUNDARY,
                },
            ]
        )
        event = len(events) + 1
        events.extend(
            [
                {"event_index": event, "method_id": method_id, "before": None, "after": "candidate", "reason": "Failure retained", "witness_id": failed_id},
                {"event_index": event + 1, "method_id": method_id, "before": "candidate", "after": "validated", "reason": "Bounded recovery passed", "witness_id": passed_id},
                {"event_index": event + 2, "method_id": method_id, "before": "validated", "after": "preferred", "reason": "Preferred only for matching preconditions", "witness_id": passed_id},
            ]
        )
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "owner": "Caelen Ash",
        "phase": "v687-v5",
        "identity_boundary": BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": [],
        "counts": {
            "methods": len(methods),
            "witnesses": len(witnesses),
            "state_events": len(events),
            "recommendations": 0,
            "states": {"observed": 0, "candidate": 0, "validated": 0, "preferred": len(methods), "superseded": 0, "deprecated": 0},
            "witness_results": {"fail": len(failures), "pass": len(failures)},
        },
        "boundary": BOUNDARY,
    }


def package_smokes() -> list[dict]:
    document = gemmi.cif.read_string("data_synthetic\n_cell.length_a 10.0\n")
    block = document.sole_block()
    gemmi_positive = block.find_value("_cell.length_a") == "10.0"
    missing = gemmi.cif.read_string("data_synthetic\n_cell.length_b 11.0\n").sole_block().find_value("_cell.length_a")
    gemmi_adverse = not bool(missing)

    matrix = np.array([[4.0, 1.0], [1.0, 3.0]])
    numpy_positive = bool(np.allclose(matrix @ np.linalg.inv(matrix), np.eye(2)))
    try:
        np.linalg.inv(np.array([[1.0, 2.0], [2.0, 4.0]]))
    except np.linalg.LinAlgError:
        numpy_adverse = True
    else:
        numpy_adverse = False

    graph = nx.DiGraph([("index", "integrate"), ("integrate", "scale")])
    networkx_positive = list(nx.topological_sort(graph)) == ["index", "integrate", "scale"]
    graph.add_edge("scale", "index")
    try:
        list(nx.topological_sort(graph))
    except nx.NetworkXUnfeasible:
        networkx_adverse = True
    else:
        networkx_adverse = False

    return [
        {"name": "gemmi", "version": importlib.metadata.version("gemmi"), "positive": gemmi_positive, "adverse_rejected": gemmi_adverse, "positive_scope": "synthetic CIF text parsed and one declared tag read", "adverse_scope": "missing required tag retained as absent"},
        {"name": "numpy", "version": importlib.metadata.version("numpy"), "positive": numpy_positive, "adverse_rejected": numpy_adverse, "positive_scope": "two-by-two inverse consistency", "adverse_scope": "singular matrix refused"},
        {"name": "networkx", "version": importlib.metadata.version("networkx"), "positive": networkx_positive, "adverse_rejected": networkx_adverse, "positive_scope": "three-node deterministic DAG order", "adverse_scope": "cycle refused"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wheel-cache", type=Path, required=True)
    args = parser.parse_args()

    proposals = strict_load(PHASE / "x1" / "new-proposals.json")["proposals"]
    plan = strict_load(PHASE / "x1" / "package-plan.json")
    cache = args.wheel_cache.resolve()
    package_rows = []
    for package in plan["packages"]:
        wheel = cache / package["wheel"]
        actual_hash = hashlib.sha256(wheel.read_bytes()).hexdigest()
        installed_version = importlib.metadata.version(package["name"])
        package_rows.append(
            {
                "name": package["name"],
                "version": package["version"],
                "installed_version": installed_version,
                "wheel": package["wheel"],
                "expected_sha256": package["sha256"],
                "observed_sha256": actual_hash,
                "hash_matched": actual_hash == package["sha256"],
                "version_matched": installed_version == package["version"],
                "phase_addition": package.get("phase_addition", False),
                "direct": package["direct"],
            }
        )
    if not all(row["hash_matched"] and row["version_matched"] for row in package_rows):
        raise SystemExit("wheel or installed-version mismatch")

    dependency = subprocess.run(
        [sys.executable, "-m", "pip", "check"], text=True, encoding="utf-8", errors="strict", capture_output=True
    )
    if dependency.returncode != 0:
        raise SystemExit("pip dependency check failed")

    requirements = "\n".join(
        f"{package['name']}=={package['version']} --hash=sha256:{package['sha256']}"
        for package in plan["packages"]
    ) + "\n"
    write_or_verify("requirements.lock", requirements)
    write_or_verify(
        "package-install.json",
        {
            "schema": "ghc.family.caelen-package-install.v1",
            "environment": "exclusive D-drive owner runtime",
            "host_interpreter_modified": False,
            "network_after_wheel_download": False,
            "packages": package_rows,
            "wheels_verified": len(package_rows),
            "phase_additions": sum(bool(row["phase_addition"]) for row in package_rows),
            "exit_code": 0,
            "complete_security": False,
        },
    )
    write_or_verify("package-dependency-check.json", {"exit_code": dependency.returncode, "result": dependency.stdout.strip(), "environment": "exclusive owner runtime"})
    smokes = package_smokes()
    if not all(row["positive"] and row["adverse_rejected"] for row in smokes):
        raise SystemExit("package smoke mismatch")
    write_or_verify("package-smokes.json", smokes)
    write_or_verify(
        "environment-receipt.json",
        {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "node_version_checked_in_x1": "v24.18.0",
            "git_version_checked_in_x1": "2.55.0.windows.2",
            "isolated_owner_runtime": True,
            "private_absolute_path_persisted": False,
        },
    )

    results = []
    invalid_rows = []
    for proposal in proposals:
        before = copy.deepcopy(proposal["input"])
        error = None
        try:
            actual = run(proposal["operation"], proposal["input"])
        except Exception as exc:  # retained in the result rather than hidden
            actual = None
            error = type(exc).__name__ + ": " + str(exc)
        input_preserved = strict_equal(before, proposal["input"])
        passed = error is None and strict_equal(actual, proposal["expected_output"])
        results.append(
            {
                "proposal_id": proposal["id"],
                "operation": proposal["operation"],
                "actual": actual,
                "passed": passed,
                "input_preserved": input_preserved,
                "error": error,
            }
        )
        candidates = mutated_results(proposal["expected_output"])
        if len(candidates) != len(proposal["mutations"]):
            raise SystemExit("mutation inventory mismatch")
        for mutation, candidate in zip(proposal["mutations"], candidates):
            invalid_rows.append(
                {
                    "mutation_id": mutation["mutation_id"],
                    "proposal_id": proposal["id"],
                    "kind": mutation["kind"],
                    "invalid_candidate": candidate,
                    "rejected": not strict_equal(candidate, proposal["expected_output"]),
                    "original_success_credit": 0,
                }
            )
    if not all(row["passed"] and row["input_preserved"] for row in results):
        raise SystemExit("frozen contract mismatch")
    if not all(row["rejected"] for row in invalid_rows):
        raise SystemExit("changed result was not rejected")
    write("contract-results-initial.json", results)
    write("mutation-results.json", invalid_rows)
    operational = make_operational_ledger()
    write("method-flow/operational/ledger.json", operational)
    write(
        "operational-negatives.json",
        {
            "retained_negative_ids": [method["retained_negative_ids"][0] for method in operational["methods"]],
            "failed_witnesses": operational["counts"]["witness_results"]["fail"],
            "passing_recoveries": operational["counts"]["witness_results"]["pass"],
            "nonerasure": True,
            "original_success_credit": 0,
        },
    )
    print(
        json.dumps(
            {
                "contracts": len(results),
                "matches": sum(row["passed"] for row in results),
                "mutations": len(invalid_rows),
                "rejections": sum(row["rejected"] for row in invalid_rows),
                "wheels": len(package_rows),
                "smokes": len(smokes),
                "operational_failures_retained": operational["counts"]["witness_results"]["fail"],
            }
        )
    )


if __name__ == "__main__":
    main()
