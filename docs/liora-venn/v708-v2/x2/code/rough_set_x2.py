from __future__ import annotations

import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


X1_CODE = Path(__file__).resolve().parents[2] / "x1" / "code"
if str(X1_CODE) not in sys.path:
    sys.path.insert(0, str(X1_CODE))

import rough_set as x1


def consistency_census(table, attributes=None):
    x1.validate_table(table)
    by_object = {row["object"]: row for row in table["rows"]}
    records = []
    for block in x1.partition(table, attributes):
        decisions = sorted({by_object[label]["decision"] for label in block})
        records.append(
            {
                "objects": block,
                "decisions": decisions,
                "consistent": len(decisions) == 1,
            }
        )
    conflicts = [record for record in records if not record["consistent"]]
    return {
        "blocks": records,
        "consistent_blocks": len(records) - len(conflicts),
        "conflicting_blocks": len(conflicts),
        "conflicting_objects": sorted(
            {label for record in conflicts for label in record["objects"]}
        ),
    }


def _compatible(left, right, *, optimistic):
    if left == "?" or right == "?":
        return optimistic or left == right
    return left == right


def missing_neighborhoods(table, attributes=None, *, optimistic):
    attrs = x1.selected_attributes(table, attributes)
    rows = table["rows"]
    result = {}
    for row in rows:
        neighbors = []
        for other in rows:
            if all(
                _compatible(
                    row["conditions"][attr],
                    other["conditions"][attr],
                    optimistic=optimistic,
                )
                for attr in attrs
            ):
                neighbors.append(other["object"])
        result[row["object"]] = sorted(neighbors)
    return dict(sorted(result.items()))


def neighborhood_approximations(table, attributes=None, target=None, *, optimistic):
    x1.validate_table(table)
    target_set = set(table["target"] if target is None else target)
    universe = {row["object"] for row in table["rows"]}
    if not target_set <= universe:
        raise ValueError("invalid_target")
    neighborhoods = missing_neighborhoods(table, attributes, optimistic=optimistic)
    lower = sorted(
        label for label, neighbors in neighborhoods.items() if set(neighbors) <= target_set
    )
    upper = sorted(
        label for label, neighbors in neighborhoods.items() if set(neighbors) & target_set
    )
    lower_set, upper_set = set(lower), set(upper)
    return {
        "lower": lower,
        "upper": upper,
        "boundary": sorted(upper_set - lower_set),
        "negative": sorted(universe - upper_set),
        "semantics": "optimistic_wildcard" if optimistic else "pessimistic_explicit_missing",
    }


def _dominates(left, right, attributes):
    if left["object"] == right["object"]:
        return True
    values = [
        (left["conditions"][attr], right["conditions"][attr]) for attr in attributes
    ]
    if any(a == "?" or b == "?" for a, b in values):
        return False
    return all(a >= b for a, b in values)


def dominance_cones(table, attributes=None):
    attrs = x1.selected_attributes(table, attributes)
    rows = table["rows"]
    upward = {}
    downward = {}
    for row in rows:
        upward[row["object"]] = sorted(
            other["object"] for other in rows if _dominates(other, row, attrs)
        )
        downward[row["object"]] = sorted(
            other["object"] for other in rows if _dominates(row, other, attrs)
        )
    return {
        "upward": dict(sorted(upward.items())),
        "downward": dict(sorted(downward.items())),
        "missing_semantics": "self_only_plus_fully_numeric_comparisons",
    }


def dominance_approximations(table, threshold=1, attributes=None):
    x1.validate_table(table)
    target = {
        row["object"] for row in table["rows"] if row["decision"] >= threshold
    }
    cones = dominance_cones(table, attributes)
    lower = sorted(
        label
        for label, cone in cones["upward"].items()
        if set(cone) <= target
    )
    upper = sorted(
        label
        for label, cone in cones["downward"].items()
        if set(cone) & target
    )
    return {
        "threshold": threshold,
        "target": sorted(target),
        "lower": lower,
        "upper": upper,
        "boundary": sorted(set(upper) - set(lower)),
        "semantics": "finite_upward_union_with_pessimistic_missing_comparability",
    }


def correction_lineage(table, patch):
    x1.validate_table(table)
    required = {"object", "attribute", "old", "new"}
    if not isinstance(patch, dict) or set(patch) != required:
        raise ValueError("invalid_patch_shape")
    if patch["attribute"] not in table["condition_attributes"]:
        raise ValueError("unknown_patch_attribute")
    if not x1.ALLOWED_VALUE(patch["new"]):
        raise ValueError("invalid_patch_value")
    updated = copy.deepcopy(table)
    matches = [row for row in updated["rows"] if row["object"] == patch["object"]]
    if len(matches) != 1:
        raise ValueError("unknown_patch_object")
    row = matches[0]
    if row["conditions"][patch["attribute"]] != patch["old"]:
        raise ValueError("stale_patch_old_value")
    before = x1.digest(table)
    row["conditions"][patch["attribute"]] = patch["new"]
    x1.validate_table(updated)
    after = x1.digest(updated)
    return {
        "before_digest": before,
        "after_digest": after,
        "changed": before != after,
        "patch": patch,
        "original_preserved": x1.digest(table) == before,
        "updated_table": updated,
    }


def accessible_projection(table):
    approximation = x1.approximations(table)
    projection = {
        "lower_cardinality": len(approximation["lower"]),
        "boundary_cardinality": len(approximation["boundary"]),
        "upper_cardinality": len(approximation["upper"]),
    }
    return {
        "projection": projection,
        "ordered_labels": list(projection),
        "dimensionless": True,
        "manual_accessibility_evaluation": False,
    }


def authority_boundary(table):
    projection = accessible_projection(table)
    return {
        "mathematical_projection": projection["projection"],
        "synthetic": True,
        "real_data_rows": 0,
        "classification_authority": False,
        "identity_authority": False,
        "remedy_authority": False,
        "legal_or_cultural_authority": False,
        "maori_authority": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def adviser_fixture():
    return {
        "fixture_id": "TEREN-BOUNDARY-ROWS",
        "condition_attributes": ["a", "b", "c"],
        "decision_attribute": "d",
        "rows": [
            {"object": "u1", "conditions": {"a": 0, "b": 0, "c": 0}, "decision": 0},
            {"object": "u2", "conditions": {"a": 0, "b": 0, "c": 0}, "decision": 1},
            {"object": "u3", "conditions": {"a": 0, "b": 1, "c": 0}, "decision": 0},
            {"object": "u4", "conditions": {"a": 1, "b": 0, "c": 1}, "decision": 1},
        ],
        "target": ["u1", "u3"],
        "synthetic": True,
        "real_data_rows": 0,
    }


def adviser_oracle():
    table = adviser_fixture()
    subsets = [[], ["a"], ["b"], ["c"], ["a", "b"], ["a", "c"], ["b", "c"], ["a", "b", "c"]]
    records = []
    for subset in subsets:
        result = x1.positive_dependency(table, subset)
        records.append(
            {
                "attributes": subset,
                "positive_region": result["positive_region"],
                "dependency": result["dependency"],
            }
        )
    return {
        "records": records,
        "reducts": x1.reducts(table)["reducts"],
        "core": x1.core(table)["core"],
    }


def adviser_mutant_claim():
    table = adviser_fixture()
    full_positive = set(x1.positive_dependency(table, table["condition_attributes"])["positive_region"])
    restricted = copy.deepcopy(table)
    restricted["rows"] = [row for row in restricted["rows"] if row["object"] in full_positive]
    restricted["target"] = [label for label in restricted["target"] if label in full_positive]
    restricted_result = x1.positive_dependency(restricted, ["a"])
    return {
        "candidate": ["a"],
        "working_universe": sorted(full_positive),
        "claimed_positive_region": restricted_result["positive_region"],
        "claimed_dependency_using_original_denominator": [len(restricted_result["positive_region"]), len(table["rows"])],
        "claimed_preserving": True,
        "claimed_minimal": True,
    }


def check_adviser_mutant(claim):
    table = adviser_fixture()
    correct = x1.positive_dependency(table, claim["candidate"])
    accepted = (
        claim.get("working_universe") == sorted(row["object"] for row in table["rows"])
        and claim.get("claimed_positive_region") == correct["positive_region"]
        and claim.get("claimed_dependency_using_original_denominator") == correct["dependency"]
    )
    return {
        "accepted": accepted,
        "correct_positive_region": correct["positive_region"],
        "correct_dependency": correct["dependency"],
        "counterexample": {"objects": ["u2", "u3"], "attribute": "a", "shared_value": 0, "different_decisions": [1, 0]},
    }


def dispatch(operation, table):
    x1.validate_table(table)
    operations = {
        "consistency_census": lambda: consistency_census(table),
        "pessimistic_neighborhoods": lambda: missing_neighborhoods(table, optimistic=False),
        "optimistic_neighborhoods": lambda: missing_neighborhoods(table, optimistic=True),
        "pessimistic_approximations": lambda: neighborhood_approximations(table, optimistic=False),
        "optimistic_approximations": lambda: neighborhood_approximations(table, optimistic=True),
        "dominance_cones": lambda: dominance_cones(table),
        "dominance_approximations": lambda: dominance_approximations(table),
        "correction_lineage": lambda: correction_lineage(
            table,
            {
                "object": table["rows"][0]["object"],
                "attribute": table["condition_attributes"][0],
                "old": table["rows"][0]["conditions"][table["condition_attributes"][0]],
                "new": 9 if table["rows"][0]["conditions"][table["condition_attributes"][0]] != 9 else 8,
            },
        ),
        "accessible_projection": lambda: accessible_projection(table),
        "authority_boundary": lambda: authority_boundary(table),
    }
    if operation not in operations:
        raise ValueError("unsupported_operation")
    return operations[operation]()


X2_OPERATIONS = [
    "consistency_census",
    "pessimistic_neighborhoods",
    "optimistic_neighborhoods",
    "pessimistic_approximations",
    "optimistic_approximations",
    "dominance_cones",
    "dominance_approximations",
    "correction_lineage",
    "accessible_projection",
    "authority_boundary",
]
