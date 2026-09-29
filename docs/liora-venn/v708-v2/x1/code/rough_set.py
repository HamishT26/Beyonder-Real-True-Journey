from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from typing import Iterable


ALLOWED_VALUE = lambda value: value == "?" or (isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 9)


def canonical_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def validate_table(table):
    if not isinstance(table, dict):
        raise ValueError("table_not_object")
    attrs = table.get("condition_attributes")
    rows = table.get("rows")
    if not isinstance(attrs, list) or not 1 <= len(attrs) <= 4 or len(set(attrs)) != len(attrs):
        raise ValueError("invalid_attributes")
    if any(not isinstance(attr, str) or not attr for attr in attrs):
        raise ValueError("invalid_attribute_name")
    if not isinstance(rows, list) or not 1 <= len(rows) <= 16:
        raise ValueError("invalid_rows")
    labels = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("invalid_row")
        label = row.get("object")
        conditions = row.get("conditions")
        decision = row.get("decision")
        if not isinstance(label, str) or not label:
            raise ValueError("invalid_object")
        labels.append(label)
        if not isinstance(conditions, dict) or set(conditions) != set(attrs):
            raise ValueError("condition_shape_mismatch")
        if any(not ALLOWED_VALUE(value) for value in conditions.values()):
            raise ValueError("invalid_condition_value")
        if not isinstance(decision, int) or isinstance(decision, bool) or not 0 <= decision <= 9:
            raise ValueError("invalid_decision")
    if len(set(labels)) != len(labels):
        raise ValueError("duplicate_object")
    target = table.get("target", [])
    if not isinstance(target, list) or any(value not in labels for value in target) or len(set(target)) != len(target):
        raise ValueError("invalid_target")
    return table


def selected_attributes(table, attributes):
    validate_table(table)
    attrs = table["condition_attributes"] if attributes is None else list(attributes)
    if len(set(attrs)) != len(attrs) or any(attr not in table["condition_attributes"] for attr in attrs):
        raise ValueError("unknown_selected_attribute")
    return attrs


def partition(table, attributes=None):
    attrs = selected_attributes(table, attributes)
    groups = {}
    for row in table["rows"]:
        key = tuple(row["conditions"][attr] for attr in attrs)
        groups.setdefault(key, []).append(row["object"])
    return sorted((sorted(block) for block in groups.values()), key=lambda block: (block[0], len(block), block))


def partition_pairwise(table, attributes=None):
    attrs = selected_attributes(table, attributes)
    rows = table["rows"]
    remaining = {row["object"] for row in rows}
    by_label = {row["object"]: row for row in rows}
    blocks = []
    while remaining:
        seed = min(remaining)
        base = by_label[seed]
        block = sorted(
            label for label in remaining
            if all(by_label[label]["conditions"][attr] == base["conditions"][attr] for attr in attrs)
        )
        remaining.difference_update(block)
        blocks.append(block)
    return sorted(blocks, key=lambda block: (block[0], len(block), block))


def approximations(table, attributes=None, target=None):
    validate_table(table)
    chosen = set(table["target"] if target is None else target)
    universe = {row["object"] for row in table["rows"]}
    if not chosen <= universe:
        raise ValueError("invalid_target")
    lower, upper = set(), set()
    for block in partition(table, attributes):
        block_set = set(block)
        if block_set <= chosen:
            lower |= block_set
        if block_set & chosen:
            upper |= block_set
    return {
        "lower": sorted(lower),
        "upper": sorted(upper),
        "boundary": sorted(upper - lower),
        "negative": sorted(universe - upper),
    }


def approximations_neighborhood(table, attributes=None, target=None):
    attrs = selected_attributes(table, attributes)
    chosen = set(table["target"] if target is None else target)
    rows = table["rows"]
    universe = {row["object"] for row in rows}
    if not chosen <= universe:
        raise ValueError("invalid_target")
    lower, upper = set(), set()
    for row in rows:
        neighborhood = {
            other["object"] for other in rows
            if all(other["conditions"][attr] == row["conditions"][attr] for attr in attrs)
        }
        if neighborhood <= chosen:
            lower.add(row["object"])
        if neighborhood & chosen:
            upper.add(row["object"])
    return {"lower": sorted(lower), "upper": sorted(upper), "boundary": sorted(upper-lower), "negative": sorted(universe-upper)}


def fraction_pair(numerator, denominator):
    if denominator == 0:
        return [1, 1]
    value = Fraction(numerator, denominator)
    return [value.numerator, value.denominator]


def accuracy_membership(table, attributes=None, target=None):
    chosen = set(table["target"] if target is None else target)
    approx = approximations(table, attributes, sorted(chosen))
    blocks = partition(table, attributes)
    memberships = {}
    for block in blocks:
        numerator = len(set(block) & chosen)
        pair = fraction_pair(numerator, len(block))
        for label in block:
            memberships[label] = pair
    return {"accuracy": fraction_pair(len(approx["lower"]), len(approx["upper"])), "membership": dict(sorted(memberships.items()))}


def decision_classes(table):
    validate_table(table)
    classes = {}
    for row in table["rows"]:
        classes.setdefault(str(row["decision"]), []).append(row["object"])
    return {key: sorted(value) for key, value in sorted(classes.items())}


def positive_dependency(table, attributes=None):
    classes = decision_classes(table)
    positive = set()
    for labels in classes.values():
        positive.update(approximations(table, attributes, labels)["lower"])
    return {"positive_region": sorted(positive), "dependency": fraction_pair(len(positive), len(table["rows"]))}


def discernibility(table):
    validate_table(table)
    attrs = table["condition_attributes"]
    rows = table["rows"]
    cells = []
    for i, left in enumerate(rows):
        for right in rows[i+1:]:
            if left["decision"] == right["decision"]:
                continue
            diff = sorted(attr for attr in attrs if left["conditions"][attr] != right["conditions"][attr])
            cells.append({"left": left["object"], "right": right["object"], "attributes": diff})
    return cells


def dependency_fraction(table, attributes):
    pair = positive_dependency(table, attributes)["dependency"]
    return Fraction(pair[0], pair[1])


def reducts(table):
    validate_table(table)
    attrs = table["condition_attributes"]
    full = dependency_fraction(table, attrs)
    preserving = []
    for size in range(len(attrs)+1):
        for combo in itertools.combinations(attrs, size):
            combo_set = set(combo)
            if dependency_fraction(table, combo) != full:
                continue
            if any(set(previous) < combo_set for previous in preserving):
                continue
            preserving.append(list(combo))
    return {"full_dependency": [full.numerator, full.denominator], "reducts": preserving}


def core(table):
    result = reducts(table)
    reduct_list = result["reducts"]
    intersection = set(reduct_list[0]) if reduct_list else set()
    for reduct in reduct_list[1:]:
        intersection &= set(reduct)
    return {"reducts": reduct_list, "core": sorted(intersection)}


def dispatch(operation, table):
    validate_table(table)
    operations = {
        "table_shape": lambda: {"digest": digest(table), "rows": len(table["rows"]), "attributes": table["condition_attributes"]},
        "partition": lambda: {"direct": partition(table), "pairwise": partition_pairwise(table)},
        "lower_approximation": lambda: approximations(table)["lower"],
        "upper_approximation": lambda: approximations(table)["upper"],
        "regions": lambda: approximations(table),
        "accuracy_membership": lambda: accuracy_membership(table),
        "positive_dependency": lambda: positive_dependency(table),
        "discernibility": lambda: discernibility(table),
        "reducts": lambda: reducts(table),
        "core": lambda: core(table),
    }
    if operation not in operations:
        raise ValueError("unsupported_operation")
    return operations[operation]()


X1_OPERATIONS = ["table_shape", "partition", "lower_approximation", "upper_approximation", "regions", "accuracy_membership", "positive_dependency", "discernibility", "reducts", "core"]
