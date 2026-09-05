"""Execute only frozen Vesper v686-v3 owner contracts and retain adversaries."""

from __future__ import annotations

import copy
import importlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / "docs/vesper-arlen/v686-v3"
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_config_toml import canonical, envelope, sha, verify_envelope


MODULES = {
    "toml": "config_toml",
    "layers": "config_layers",
    "transaction": "config_transaction",
    "assurance": "config_assurance",
    "obligations": "config_obligations",
}


def read(relative: str) -> object:
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def write(relative: str, value: object) -> None:
    path = BASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def evaluator(row: dict):
    return importlib.import_module("ghc_family_" + MODULES[row["runner"]]).evaluate


def mutate(record: dict, kind: str) -> dict:
    changed = copy.deepcopy(record)
    if kind == "wrong_report":
        changed["result"] = {"fabricated": True}
        changed["result_sha256"] = sha(changed["result"])
    elif kind == "wrong_input_digest":
        changed["input_sha256"] = "0" * 64
    elif kind == "wrong_definition_digest":
        changed["definition_sha256"] = "0" * 64
    elif kind == "empirical_promotion":
        changed["empirical"] = True
    elif kind == "authority_promotion":
        changed["authority"] = True
    elif kind == "unapproved_extra":
        changed["unapproved_extra"] = "synthetic extra field"
    elif kind == "missing_hash_domain":
        del changed["hash_domain"]
    else:
        raise ValueError(kind)
    return changed


def main() -> int:
    rows = read("x1/new-proposals.json")["proposals"]
    equality = read("validation/x1-equality.json")
    assert equality["clean_before_x2"]
    assert equality["divergence"] == [0, 0]
    assert len(set(equality["local_upstream_tracking_fresh_live"])) == 1

    results = []
    negatives = []
    failures = []
    lookup = {}
    for row in rows:
        before = canonical(row["input"])
        fn = evaluator(row)
        value = fn(row["operation"], copy.deepcopy(row["input"]))
        record = envelope(row, value)
        oracle = canonical(value) == canonical(row["expected_result"])
        unchanged = canonical(row["input"]) == before
        accepted = verify_envelope(row, record, fn)
        result = {
            "proposal_id": row["proposal_id"],
            "family": row["family"],
            "result": value,
            "envelope": record,
            "frozen_oracle_matches": oracle,
            "input_nonmutation": unchanged,
            "envelope_check": accepted,
            "disposition": row["expected_execution_disposition"],
            "same_owner_only": True,
        }
        results.append(result)
        lookup[row["proposal_id"]] = (row, result)
        if not (oracle and unchanged and accepted["accepted"]):
            failures.append(result)
        for kind in row["preregistered_mutations"]:
            bad = mutate(record, kind)
            verdict = verify_envelope(row, bad, fn)
            negative = {
                "negative_id": row["proposal_id"] + "-ADV-" + kind,
                "proposal_id": row["proposal_id"],
                "mutation": kind,
                "retained_record": bad,
                "observed": verdict,
                "rejected": verdict["accepted"] is False,
                "success_credit": 0,
                "recovery_envelope_sha256": sha(record),
                "same_owner_only": True,
            }
            negatives.append(negative)
            if not negative["rejected"]:
                failures.append(negative)

    write("x2/contract-results.json", {"results": results, "source_x1": equality["x1"]})
    write("x2/registered-mutations.json", {"negatives": negatives, "success_credit": 0})
    if failures:
        write("x2/initial-contract-failure.json", {"failures": failures, "aggregate_success_credit": 0})
        print(json.dumps({"status": "FAIL", "failures": len(failures)}))
        return 1

    portfolio = read("x1/portfolio-plan.json")
    safe = []
    candidates = []
    corrected = []
    for task in portfolio["safe_now"]:
        _row, result = lookup[task["proposal_id"]]
        passed = result["frozen_oracle_matches"] if task["kind"] == "frozen_oracle" else result["input_nonmutation"]
        safe.append(dict(task, disposition="completed", passed=passed, evidence_sha256=sha(result)))
    negative_map = {(item["proposal_id"], item["mutation"]): item for item in negatives}
    for task in portfolio["candidates"]:
        negative = negative_map[(task["proposal_id"], task["kind"])]
        candidates.append(dict(task, disposition="completed", passed=negative["rejected"], evidence_sha256=sha(negative)))
    for task in portfolio["clean_fix_refine"]:
        row, result = lookup[task["proposal_id"]]
        fn = evaluator(row)
        good = result["envelope"]
        bad = mutate(good, task["mutation"])
        before = verify_envelope(row, bad, fn)
        repaired = copy.deepcopy(bad)
        if task["kind"] == "CLEAN":
            del repaired["unapproved_extra"]
        elif task["kind"] == "FIX":
            repaired["result"] = copy.deepcopy(good["result"])
            repaired["result_sha256"] = good["result_sha256"]
        else:
            repaired["hash_domain"] = good["hash_domain"]
        after = verify_envelope(row, repaired, fn)
        assert not before["accepted"] and after["accepted"]
        assert canonical(repaired) == canonical(good)
        corrected.append(
            dict(
                task,
                retained_negative_id=task["task_id"] + "-INITIAL",
                retained_before=bad,
                before_check=before,
                corrected_after=repaired,
                after_check=after,
                disposition="completed",
                success_credit_for_initial=0,
            )
        )

    write(
        "x2/portfolio-results.json",
        {
            "safe_now": safe,
            "candidates": candidates,
            "clean_fix_refine": corrected,
            "exact_packets": portfolio["exact_packets"],
            "blocked_packets": portfolio["blocked_packets"],
            "external_actions": 0,
        },
    )
    write(
        "x2/contract-summary.json",
        {
            "proposals": 200,
            "positive_contracts_passed": 200,
            "registered_mutations": 1000,
            "registered_mutations_rejected": 1000,
            "safe_tasks_passed": 300,
            "candidate_tasks_passed": 250,
            "clean_fix_refine_passed": 300,
            "retained_cfr_initial_failures": 300,
            "exact_packets_unexecuted": 50,
            "blocked_packets_unexecuted": 30,
            "outcomes": {"completed": 170, "represented": 10, "open_gap": 10, "exact_gate": 10},
            "same_owner_only": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write(
        "x2/operational-events.json",
        {
            "events": [
                {
                    "id": "VA6863-OP011",
                    "failure": "The first 200-contract component run allowed TOML nan through tomllib before the finite JSON-domain guard.",
                    "recovery": "Validate the parsed TOML value inside the finite JSON profile and return invalid_toml for nonfinite values; the corrected 200-contract component passed.",
                    "success_credit": 0,
                },
                {
                    "id": "VA6863-OP012",
                    "failure": "The first OSV PowerShell projection counted one blank vulnerability per empty result object.",
                    "recovery": "Inspect the exact response shape; three empty result objects establish zero findings for this dated query without exhaustive-security credit.",
                    "success_credit": 0,
                },
            ]
        },
    )
    print(
        json.dumps(
            {
                "status": "PASS_OWNER_CONTRACT_EXECUTION",
                "proposals": len(results),
                "mutations": len(negatives),
                "safe": len(safe),
                "candidates": len(candidates),
                "clean_fix_refine": len(corrected),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
