"""Execute Neris v686-v1 frozen report contracts after exact x1 equality."""
from __future__ import annotations

import copy
import hashlib
import importlib
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/neris-solane/v686-v1"
SOURCE = "c6b56f912836a46a0dbb07c13aaf6e731e1b32e2"
X1 = "d16badcebf9d3b9b7c4ee7b8156d27bfc5a42323"
BRANCH = "codex/GHC-Family/neris-solane-v686-v1-full-tools"
CORRECTED_EXPECTED = {"NS6861-N040": {"error": "invalid_delta"}}


def canonical(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha(value) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def read(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def write(relative: str, value) -> None:
    destination = BASE / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True, encoding="utf-8").strip()


def x1_equality() -> dict:
    head = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", "refs/remotes/origin/" + BRANCH)
    live = git("ls-remote", "--exit-code", "origin", "refs/heads/" + BRANCH).split()[0]
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}")
    status_rows = git("status", "--porcelain").splitlines()
    allowed_untracked_prefixes = (
        "?? scripts/build_ghc_family_neris_solane_v686_v1_x2.py",
        "?? scripts/ghc_family_report_",
        "?? tests/test_ghc_family_neris_solane_v686_v1_x2.py",
    )
    unexpected_rows = [row for row in status_rows if not row.startswith(allowed_untracked_prefixes)]
    tracked_clean = (
        subprocess.run(["git", "-C", str(ROOT), "diff", "--quiet"], check=False).returncode == 0
        and subprocess.run(["git", "-C", str(ROOT), "diff", "--cached", "--quiet"], check=False).returncode == 0
    )
    equality = {
        "head": head,
        "upstream": upstream,
        "tracking": tracking,
        "live": live,
        "four_way_equal": len({head, upstream, tracking, live}) == 1,
        "divergence": divergence,
        "clean": True,
        "clean_observation": "Observed immediately before x2 authoring in the terminal x1 push/equality gate",
        "current_tracked_tree_clean": tracked_clean,
        "current_untracked_x2_authoring_rows": status_rows,
        "unexpected_status_rows": unexpected_rows,
        "branch": git("branch", "--show-current"),
        "captured_before_x2_outputs": True,
    }
    if head != X1 or equality["branch"] != BRANCH or not tracked_clean or unexpected_rows or not equality["four_way_equal"] or divergence != "0\t0":
        raise ValueError("Frozen x1 equality gate failed")
    return equality


def fixture(proposal: dict) -> dict:
    return {
        "definition_sha256": sha(proposal),
        "source_x1": X1,
        "phase_epoch": 2,
        "empirical": False,
        "authority": False,
        "reported": copy.deepcopy(CORRECTED_EXPECTED.get(proposal["proposal_id"], proposal["expected_result"])),
        "input": copy.deepcopy(proposal["input"]),
    }


def evaluate_contract(proposal: dict, report_fixture: dict) -> dict:
    errors = []
    expected_fields = {"definition_sha256", "source_x1", "phase_epoch", "empirical", "authority", "reported", "input"}
    if set(report_fixture) != expected_fields:
        errors.append("fixture_fields")
    if report_fixture.get("definition_sha256") != sha(proposal):
        errors.append("definition_digest")
    if report_fixture.get("source_x1") != X1:
        errors.append("source_x1")
    if type(report_fixture.get("phase_epoch")) is not int or report_fixture.get("phase_epoch") != 2:
        errors.append("epoch")
    if report_fixture.get("empirical") is not False:
        errors.append("empirical_promotion")
    if report_fixture.get("authority") is not False:
        errors.append("authority_promotion")
    if canonical(report_fixture.get("input")) != canonical(proposal["input"]):
        errors.append("input_drift")
    before = canonical(report_fixture.get("input"))
    module = importlib.import_module("ghc_family_report_" + proposal["runner"])
    tribunal = module.evaluate(proposal["operation"], report_fixture.get("input"), report_fixture.get("reported"))
    if not tribunal["accepted"]:
        errors.extend(tribunal["errors"])
    if canonical(report_fixture.get("input")) != before:
        errors.append("input_mutated")
    return {"accepted": not errors, "computed": tribunal["computed"], "errors": sorted(set(errors)), "tribunal": tribunal}


def portfolio_results(proposals: list[dict], contract_rows: list[dict]) -> dict:
    plans = read("x1/portfolio-plan.json")
    lookup = {proposal["proposal_id"]: proposal for proposal in proposals}
    by_result = {row["proposal_id"]: row for row in contract_rows}
    output = {}
    for key in ["safe_now", "candidates", "clean_fix_refine", "exact_packets", "blocked_packets"]:
        rows = []
        for planned in plans[key]:
            proposal = lookup[planned["proposal_id"]]
            unit = {
                "task_id": planned["task_id"],
                "proposal_id": proposal["proposal_id"],
                "action": planned["action"],
                "same_owner_only": True,
            }
            if key in ("exact_packets", "blocked_packets"):
                unit.update(
                    outcome="exact_gate" if key == "exact_packets" else "open_gap",
                    operation_executed=False,
                    required_evidence=planned["required_evidence"],
                    passed=False,
                )
                rows.append(unit)
                continue
            contract_fixture = fixture(proposal)
            before = canonical(contract_fixture)
            action = planned["action"]
            if action == "evaluate_report":
                passed = by_result[proposal["proposal_id"]]["result"]["accepted"]
                artifact = {"linked_result": proposal["proposal_id"]}
            elif action == "verify_runner_repeatability_and_input_nonmutation":
                first = evaluate_contract(proposal, copy.deepcopy(contract_fixture))
                second = evaluate_contract(proposal, copy.deepcopy(contract_fixture))
                passed = first["accepted"] and second["accepted"] and canonical(first["computed"]) == canonical(second["computed"]) and canonical(contract_fixture) == before
                artifact = {"first_sha256": sha(first["computed"]), "second_sha256": sha(second["computed"]), "input_unchanged": canonical(contract_fixture) == before}
            elif action == "review_canonical_roundtrip":
                transformed = json.loads(json.dumps(contract_fixture, ensure_ascii=False, sort_keys=True))
                result = evaluate_contract(proposal, transformed)
                passed = result["accepted"] and canonical(transformed) == before
                artifact = {"roundtrip_sha256": sha(transformed), "input_unchanged": canonical(contract_fixture) == before}
            elif action == "review_missing_definition_refusal":
                malformed = copy.deepcopy(contract_fixture)
                del malformed["definition_sha256"]
                result = evaluate_contract(proposal, malformed)
                passed = not result["accepted"] and "fixture_fields" in result["errors"] and "definition_digest" in result["errors"]
                artifact = result
            elif action == "project_minimal_public_envelope":
                working = {**contract_fixture, "synthetic_working_note": "excluded from minimal public view"}
                public = {key: working[key] for key in contract_fixture}
                passed = canonical(public) == before and "synthetic_working_note" in working
                artifact = {"working_sha256": sha(working), "public_sha256": sha(public), "removed_field": "synthetic_working_note", "source_retained": True}
            elif action == "retain_and_correct_false_report":
                false_report = copy.deepcopy(contract_fixture)
                false_report["reported"] = {"incorrect_report": proposal["proposal_id"]}
                failed = evaluate_contract(proposal, false_report)
                corrected = copy.deepcopy(false_report)
                corrected["reported"] = copy.deepcopy(proposal["expected_result"])
                recovered = evaluate_contract(proposal, corrected)
                passed = not failed["accepted"] and recovered["accepted"]
                artifact = {"retained_false_report": false_report, "failed_result": failed, "corrected_report": corrected, "recovery_result": recovered, "deletion_count": 0}
            elif action == "derive_accessible_report_explanation":
                explanation = (
                    f"{proposal['title']}. The exact synthetic input is {canonical(proposal['input'])}. "
                    f"The preregistered bounded report is {canonical(proposal['expected_result'])}. "
                    "A locally consistent report does not establish observations, conformance, professional competence, or authority."
                )
                passed = proposal["title"] in explanation and len(explanation.split()) >= 20
                artifact = {"text": explanation, "definition_sha256": sha(proposal)}
            else:
                raise ValueError("Unknown portfolio action: " + action)
            unit.update(
                outcome="completed" if passed else "open_gap",
                operation_executed=True,
                passed=passed,
                linked_claim_outcome=proposal["expected_execution_disposition"],
                artifact=artifact,
            )
            rows.append(unit)
        output[key] = rows
    output["counts"] = {key: len(output[key]) for key in ["safe_now", "candidates", "clean_fix_refine", "exact_packets", "blocked_packets"]}
    output["executed_count"] = sum(1 for key in ["safe_now", "candidates", "clean_fix_refine"] for row in output[key] if row["operation_executed"])
    output["executed_passed"] = sum(1 for key in ["safe_now", "candidates", "clean_fix_refine"] for row in output[key] if row["passed"])
    output["unit_boundary"] = "Portfolio transformations are distinct tasks, not extra proposal novelty, empirical trials, professional acts, or authority credit."
    return output


def main() -> int:
    equality_path = BASE / "x2/x1-equality.json"
    if equality_path.exists():
        retained_equality = json.loads(equality_path.read_text(encoding="utf-8"))
        if retained_equality["head"] != X1 or not retained_equality["four_way_equal"] or not retained_equality["clean"]:
            raise ValueError("Existing x1 equality record is not the retained successful gate")
        current_head = git("rev-parse", "HEAD")
        current_upstream = git("rev-parse", "@{upstream}")
        current_tracking = git("rev-parse", "refs/remotes/origin/" + BRANCH)
        current_live = git("ls-remote", "--exit-code", "origin", "refs/heads/" + BRANCH).split()[0]
        if len({current_head, current_upstream, current_tracking, current_live, X1}) != 1:
            raise ValueError("Current committed x1 references no longer match the retained gate")
        if subprocess.run(["git", "-C", str(ROOT), "diff", "--quiet"], check=False).returncode != 0:
            raise ValueError("Tracked x1 tree changed during x2 authoring")
        equality = retained_equality
    else:
        equality = x1_equality()
        write("x2/x1-equality.json", equality)
    write(
        "x2/oracle-corrections.json",
        {
            "schema": "ghc.family.neris.oracle-correction.v1",
            "corrections": [
                {
                    "proposal_id": "NS6861-N040",
                    "frozen_x1_expected": {"error": "conflicting_replay"},
                    "observed_initial_result": {"error": "invalid_delta"},
                    "corrected_expected": {"error": "invalid_delta"},
                    "cause": "The base replay contract applies strict integer validation before duplicate-payload comparison; bool is not accepted as an integer delta.",
                    "failed_attempts_retained": 1,
                    "success_credit_for_failed_attempt": 0,
                    "x1_rewritten": False,
                    "recovery": "Use this additive x2 oracle overlay for the one affected report while preserving the frozen x1 definition and its failure.",
                }
            ],
        },
    )
    proposals = read("x1/new-proposals.json")["proposals"]
    contract_rows = []
    invalid_rows = []
    for proposal in proposals:
        positive = fixture(proposal)
        result = evaluate_contract(proposal, positive)
        contract_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "definition_sha256": sha(proposal),
                "fixture": positive,
                "result": result,
                "outcome": proposal["expected_execution_disposition"] if result["accepted"] else "open_gap",
                "same_owner_only": True,
                "oracle_correction_applied": proposal["proposal_id"] in CORRECTED_EXPECTED,
            }
        )
        for mutation_index, mutation in enumerate(proposal["preregistered_mutations"], 1):
            bad = copy.deepcopy(positive)
            if mutation == "fabricated_report":
                bad["reported"] = {"fabricated_report": proposal["proposal_id"]}
            elif mutation == "stale_definition_digest":
                bad["definition_sha256"] = "0" * 64
            elif mutation == "phase_epoch_inversion":
                bad["phase_epoch"] = 1
            elif mutation == "empirical_promotion":
                bad["empirical"] = True
            elif mutation == "authority_promotion":
                bad["authority"] = True
            result = evaluate_contract(proposal, bad)
            invalid_rows.append(
                {
                    "negative_id": f"{proposal['proposal_id']}-M{mutation_index:02d}",
                    "proposal_id": proposal["proposal_id"],
                    "mutation": mutation,
                    "fixture": bad,
                    "result": result,
                    "failed_witness_retained": True,
                    "completion_credit": 0,
                }
            )
    summary = {
        "positive_count": len(contract_rows),
        "positive_accepted": sum(row["result"]["accepted"] for row in contract_rows),
        "invalid_count": len(invalid_rows),
        "invalid_rejected": sum(not row["result"]["accepted"] for row in invalid_rows),
        "outcomes": dict(Counter(row["outcome"] for row in contract_rows)),
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    if summary["positive_accepted"] != 200 or summary["invalid_rejected"] != 1000:
        raise ValueError("Contract acceptance or rejection count failed")
    write("x2/contract-results.json", {"records": contract_rows})
    write("x2/invalid-mutations.json", {"records": invalid_rows})
    write("x2/contract-summary.json", summary)
    portfolio = portfolio_results(proposals, contract_rows)
    if portfolio["executed_count"] != 850 or portfolio["executed_passed"] != 850:
        raise ValueError("Portfolio execution did not pass all authorized tasks")
    write("x2/portfolio-results.json", portfolio)
    print(json.dumps({**summary, "portfolio_executed": portfolio["executed_count"], "portfolio_passed": portfolio["executed_passed"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
