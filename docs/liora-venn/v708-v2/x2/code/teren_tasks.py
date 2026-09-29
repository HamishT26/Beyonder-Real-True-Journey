from __future__ import annotations

import copy
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
for code_dir in (ROOT / "x1" / "code", ROOT / "x2" / "code"):
    if str(code_dir) not in sys.path:
        sys.path.insert(0, str(code_dir))

import rough_set as x1


def table(rows, attributes, target):
    return {
        "condition_attributes": list(attributes),
        "rows": [
            {
                "object": row[0],
                "conditions": dict(zip(attributes, row[1:-1])),
                "decision": row[-1],
            }
            for row in rows
        ],
        "target": list(target),
    }


def task1_missing_completions():
    incomplete = table(
        [["m1", 0, 0], ["m2", 1, 1], ["m3", "?", 0]],
        ["a"],
        ["m1", "m3"],
    )
    completions = []
    for value in (0, 1):
        completed = copy.deepcopy(incomplete)
        completed["rows"][2]["conditions"]["a"] = value
        approximation = x1.approximations(completed)
        dependency = x1.positive_dependency(completed)
        completions.append(
            {
                "assignment": value,
                "partition": x1.partition(completed),
                "lower": approximation["lower"],
                "upper": approximation["upper"],
                "positive_region": dependency["positive_region"],
                "dependency": dependency["dependency"],
                "universe": sorted(row["object"] for row in completed["rows"]),
            }
        )
    guaranteed_lower = sorted(set(completions[0]["lower"]) & set(completions[1]["lower"]))
    possible_upper = sorted(set(completions[0]["upper"]) | set(completions[1]["upper"]))
    dependency_values = sorted(
        {tuple(record["dependency"]) for record in completions},
        key=lambda value: Fraction(value[0], value[1]),
    )
    positive = {
        "completions": completions,
        "guaranteed_lower": guaranteed_lower,
        "possible_upper": possible_upper,
        "dependency_values": [list(value) for value in dependency_values],
    }
    mutant = {"mode": "silent_impute_zero", "guaranteed_lower": completions[0]["lower"], "dependency_values": [completions[0]["dependency"]]}
    mutant_accepted = mutant["guaranteed_lower"] == guaranteed_lower and mutant["dependency_values"] == positive["dependency_values"]
    return {"positive": positive, "mutant": mutant, "mutant_accepted": mutant_accepted, "classification": "UNDECLARED_MISSING_SEMANTICS"}


def task2_versioned_corrections():
    raw = {
        "V0": [["s1", 0, 0], ["s2", 1, 1]],
        "V1": [["s1", 0, 0], ["s2", 1, 1], ["s3", 0, 1]],
        "V2": [["s1", 0, 0], ["s2", 1, 1], ["s3", 0, 0]],
    }
    snapshots = {}
    for version, rows in raw.items():
        target = [row[0] for row in rows if row[-1] == 0]
        value = table(rows, ["a"], target)
        approximation = x1.approximations(value)
        dependency = x1.positive_dependency(value)
        snapshots[version] = {
            "input_digest": x1.digest(value),
            "universe": sorted(row["object"] for row in value["rows"]),
            "lower": approximation["lower"],
            "upper": approximation["upper"],
            "positive_region": dependency["positive_region"],
            "dependency": dependency["dependency"],
        }
    positive = {"snapshots": snapshots, "lineage": {"V1": "V0", "V2": "V1"}, "historical_readback": copy.deepcopy(snapshots)}
    mutant = {version: copy.deepcopy(snapshots["V2"]) for version in ("V0", "V1", "V2")}
    mutant_accepted = all(mutant[version]["input_digest"] == snapshots[version]["input_digest"] for version in snapshots)
    return {"positive": positive, "mutant_latest_only": mutant, "mutant_accepted": mutant_accepted, "classification": "MISSING_PREDECESSOR_EVIDENCE"}


def task3_reduct_family():
    value = table([["r1", 0, 0, 0, 0], ["r2", 1, 1, 0, 1]], ["a", "b", "c"], ["r1"])
    subsets = [[], ["a"], ["b"], ["c"], ["a", "b"], ["a", "c"], ["b", "c"], ["a", "b", "c"]]
    records = [{"attributes": subset, **x1.positive_dependency(value, subset)} for subset in subsets]
    positive = {"records": records, "reducts": x1.reducts(value)["reducts"], "core": x1.core(value)["core"]}
    mutant = {"reducts": [["a"]], "core": ["a"], "deduplicated_equal_columns": True}
    mutant_accepted = mutant["reducts"] == positive["reducts"] and mutant["core"] == positive["core"]
    return {"positive": positive, "mutant": mutant, "mutant_accepted": mutant_accepted, "classification": "AMBIGUOUS_ATTRIBUTE_IDENTITY"}


def task4_permission_boundary():
    value = table([["p1", 0, 0], ["p2", 1, 1]], ["a"], ["p1"])
    mathematical = {"approximation": x1.approximations(value), "dependency": x1.positive_dependency(value)["dependency"]}
    cases = [
        {"id": "E0", "source": "P", "grant": "ACTIVE", "scope": "APPEND_DEMO", "capability": "DEMO_WRITER"},
        {"id": "E1", "source": "Q", "grant": "ACTIVE", "scope": "APPEND_DEMO", "capability": "DEMO_WRITER"},
        {"id": "E2", "source": "P", "grant": "WITHDRAWN", "scope": "APPEND_DEMO", "capability": "DEMO_WRITER"},
        {"id": "E3", "source": "P", "grant": "ACTIVE", "scope": "READ_DEMO", "capability": "DEMO_WRITER"},
        {"id": "E4", "source": "P", "grant": "ACTIVE", "scope": "APPEND_DEMO", "capability": "REVIEW_ONLY"},
    ]
    effects = [int(case["source"] == "P" and case["grant"] == "ACTIVE" and case["scope"] == "APPEND_DEMO" and case["capability"] == "DEMO_WRITER") for case in cases]
    mutant_effects = [int(mathematical["dependency"] == [1, 1]) for _ in cases]
    return {
        "positive": {"mathematical_match": [True] * 5, "effect_vector": effects, "cases": cases, "mathematical": mathematical},
        "mutant_effect_vector": mutant_effects,
        "mutant_accepted": mutant_effects == effects,
        "classification": "INCOMPLETE_POLICY_EVIDENCE",
    }


def task5_checker_integrity():
    value = table([["k1", 0, 0], ["k2", 0, 1], ["k3", 1, 0]], ["a"], ["k1", "k3"])
    oracle = x1.approximations(value)
    submissions = {
        "G": {"status": "OK", "lower": ["k3"], "upper": ["k1", "k2", "k3"]},
        "B": {"status": "OK", "lower": ["k1", "k3"], "upper": ["k1", "k2", "k3"]},
        "R": {"status": "REFUSED"},
    }

    def verdict(submission):
        if submission.get("status") == "REFUSED":
            return "VALID_INPUT_REFUSED_NOT_PASS"
        if submission.get("status") != "OK" or "lower" not in submission or "upper" not in submission:
            return "MALFORMED_EVIDENCE"
        if submission["lower"] == oracle["lower"] and submission["upper"] == oracle["upper"]:
            return "ACCEPT"
        return "REJECT_MATHEMATICAL_MISMATCH"

    verdicts = [verdict(submissions[label]) for label in ("G", "B", "R")]
    mutant_verdicts = []
    for label in ("G", "B", "R"):
        repaired = copy.deepcopy(submissions[label])
        if repaired.get("status") == "OK":
            repaired["lower"] = oracle["lower"]
            repaired["upper"] = oracle["upper"]
        mutant_verdicts.append(verdict(repaired))
    return {
        "positive": {"oracle": oracle, "submissions": submissions, "submission_digests": {label: x1.digest(submission) for label, submission in submissions.items()}, "verdicts": verdicts},
        "mutant_repair_first_verdicts": mutant_verdicts,
        "mutant_accepted": mutant_verdicts == verdicts,
        "counterexample": {"object": "k1", "same_block_object": "k2", "different_decisions": [0, 1]},
        "classification": "AMBIGUOUS_RESULT_ENCODING",
    }


def run_all():
    return {
        "MISSING_MEANS_TWO_COMPLETIONS": task1_missing_completions(),
        "CORRECTION_CREATES_A_NEW_SNAPSHOT": task2_versioned_corrections(),
        "ONE_VALID_REDUCT_IS_NOT_THE_FAMILY": task3_reduct_family(),
        "SAME_ROUGH_RESULT_DIFFERENT_PERMISSION": task4_permission_boundary(),
        "CHECK_THE_SUBMISSION_NOT_ITS_REPAIR": task5_checker_integrity(),
    }
