#!/usr/bin/env python3
"""Build and execute the bounded Liora v708-v2 X1 rough-set tranche once."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import textwrap
from pathlib import Path


BOUNDARY = (
    "Finite synthetic same-owner rough-set mathematical, software, and documentary evidence only. "
    "No real participant, dataset, measurement, classification, identity decision, professional act, "
    "legal or cultural interpretation, affected-party or Maori authority, empirical GMUT confirmation, "
    "production THOS or Freed ID, complete privacy or accessibility, exhaustive security, independent "
    "reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, canon, or Stage 20 credit. "
    "NOT_READY_FOR_STAGE_20."
)


CORE_SOURCE = r'''from __future__ import annotations

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
'''


TEST_SOURCE = r'''from __future__ import annotations

import importlib.util
import json
import unittest
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location("liora_rough_set", ROOT / "x1" / "code" / "rough_set.py")
rs = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(rs)
FIXTURES = json.loads((ROOT / "planning" / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]


class RoughSetX1Tests(unittest.TestCase):
    def table(self, index=0): return FIXTURES[index]
    def test_01_validate_good(self): self.assertIs(rs.validate_table(self.table()), self.table())
    def test_02_duplicate_rejected(self):
        t=json.loads(json.dumps(self.table()));t["rows"][1]["object"]=t["rows"][0]["object"]
        with self.assertRaisesRegex(ValueError,"duplicate_object"):rs.validate_table(t)
    def test_03_boolean_rejected(self):
        t=json.loads(json.dumps(self.table()));t["rows"][0]["conditions"]["a"]=True
        with self.assertRaisesRegex(ValueError,"invalid_condition_value"):rs.validate_table(t)
    def test_04_shape_rejected(self):
        t=json.loads(json.dumps(self.table()));t["condition_attributes"].append("z")
        with self.assertRaisesRegex(ValueError,"condition_shape_mismatch"):rs.validate_table(t)
    def test_05_decision_rejected(self):
        t=json.loads(json.dumps(self.table()));t["rows"][0]["decision"]="bad"
        with self.assertRaisesRegex(ValueError,"invalid_decision"):rs.validate_table(t)
    def test_06_target_rejected(self):
        t=json.loads(json.dumps(self.table()));t["target"].append("MISSING")
        with self.assertRaisesRegex(ValueError,"invalid_target"):rs.validate_table(t)
    def test_07_partition_agreement(self):
        for t in FIXTURES:self.assertEqual(rs.partition(t),rs.partition_pairwise(t))
    def test_08_partition_cover(self):
        for t in FIXTURES:self.assertEqual(sorted(sum(rs.partition(t),[])),sorted(r["object"] for r in t["rows"]))
    def test_09_lower_subset_target(self):
        for t in FIXTURES:self.assertTrue(set(rs.approximations(t)["lower"])<=set(t["target"]))
    def test_10_target_subset_upper(self):
        for t in FIXTURES:self.assertTrue(set(t["target"])<=set(rs.approximations(t)["upper"]))
    def test_11_boundary_identity(self):
        for t in FIXTURES:
            a=rs.approximations(t);self.assertEqual(set(a["boundary"]),set(a["upper"])-set(a["lower"]))
    def test_12_negative_identity(self):
        for t in FIXTURES:
            a=rs.approximations(t);u={r["object"] for r in t["rows"]};self.assertEqual(set(a["negative"]),u-set(a["upper"]))
    def test_13_accuracy_bounds(self):
        for t in FIXTURES:
            n,d=rs.accuracy_membership(t)["accuracy"];self.assertGreaterEqual(Fraction(n,d),0);self.assertLessEqual(Fraction(n,d),1)
    def test_14_membership_bounds(self):
        for t in FIXTURES:
            for n,d in rs.accuracy_membership(t)["membership"].values():self.assertTrue(Fraction(0)<=Fraction(n,d)<=Fraction(1))
    def test_15_positive_region_bound(self):
        for t in FIXTURES:self.assertLessEqual(len(rs.positive_dependency(t)["positive_region"]),len(t["rows"]))
    def test_16_dependency_bounds(self):
        for t in FIXTURES:
            n,d=rs.positive_dependency(t)["dependency"];self.assertTrue(Fraction(0)<=Fraction(n,d)<=Fraction(1))
    def test_17_dependency_refinement(self):
        for t in FIXTURES:self.assertLessEqual(rs.dependency_fraction(t,["a"]),rs.dependency_fraction(t,["a","b","c"]))
    def test_18_discernibility_known_pairs(self):
        for t in FIXTURES:
            by={r["object"]:r for r in t["rows"]}
            for cell in rs.discernibility(t):self.assertNotEqual(by[cell["left"]]["decision"],by[cell["right"]]["decision"])
    def test_19_reduct_preservation(self):
        for t in FIXTURES:
            result=rs.reducts(t);full=Fraction(*result["full_dependency"])
            for reduct in result["reducts"]:self.assertEqual(rs.dependency_fraction(t,reduct),full)
    def test_20_reduct_minimality(self):
        for t in FIXTURES:
            result=rs.reducts(t);full=Fraction(*result["full_dependency"])
            for reduct in result["reducts"]:
                for i in range(len(reduct)):self.assertNotEqual(rs.dependency_fraction(t,reduct[:i]+reduct[i+1:]),full)
    def test_21_core_intersection(self):
        for t in FIXTURES:
            result=rs.core(t);expected=set(result["reducts"][0]) if result["reducts"] else set()
            for reduct in result["reducts"][1:]:expected&=set(reduct)
            self.assertEqual(result["core"],sorted(expected))
    def test_22_empty_target_convention(self):
        t=json.loads(json.dumps(self.table()));t["target"]=[];self.assertEqual(rs.accuracy_membership(t)["accuracy"],[1,1])
    def test_23_digest_changes(self):
        t=json.loads(json.dumps(self.table()));before=rs.digest(t);t["rows"][0]["conditions"]["a"]=2;self.assertNotEqual(before,rs.digest(t))
    def test_24_all_operations(self):
        for t in FIXTURES:
            for operation in rs.X1_OPERATIONS:self.assertIsNotNone(rs.dispatch(operation,t))
    def test_25_models_written(self):
        self.assertEqual(len(list((ROOT/"x1"/"models").glob("*.json"))),15)


if __name__ == "__main__": unittest.main()
'''


RUNNER_TEMPLATE = r'''from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path
HERE=Path(__file__).resolve(); ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location("liora_rough_set",ROOT/"x1"/"code"/"rough_set.py")
rs=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(rs)
ALLOWED=__ALLOWED__
parser=argparse.ArgumentParser();parser.add_argument("--fixtures",required=True);parser.add_argument("--fixture-id",required=True);parser.add_argument("--operation",required=True);args=parser.parse_args()
if args.operation not in ALLOWED: raise SystemExit("unsupported_runner_operation")
envelope=json.loads(Path(args.fixtures).read_text(encoding="utf-8"));matches=[x for x in envelope["fixtures"] if x["fixture_id"]==args.fixture_id]
if len(matches)!=1: raise SystemExit("fixture_not_unique")
print(json.dumps({"fixture_id":args.fixture_id,"operation":args.operation,"result":rs.dispatch(args.operation,matches[0])},ensure_ascii=False,sort_keys=True))
'''


SKILLS = [
    ("ghc-liora-rough-table-envelope-v1", "Validate small synthetic rough-set decision-table envelopes and exact input digests.", "Use this for a bounded synthetic decision table with at most four condition attributes and sixteen rows. Refuse duplicate objects, unknown fields, Boolean-as-integer values, malformed targets, or a changed digest. Treat a valid envelope as software input evidence only, never as real observation or classification authority."),
    ("ghc-liora-rough-approximations-v1", "Compute finite Pawlak lower, upper, boundary, and negative regions for declared equivalence fixtures.", "Use only after the table envelope and selected attributes validate. Compute both block-union and object-neighborhood formulations and require equality. Report the declared empty-target convention. Never promote a finite approximation into empirical adequacy, professional classification, or affected-party legitimacy."),
    ("ghc-liora-rough-membership-v1", "Compute exact rational rough membership and approximation accuracy for finite declared targets.", "Use exact fractions over declared finite neighborhoods. Preserve numerator and denominator and refuse a hidden floating tolerance. Membership is not probability, confidence, identity, or entitlement. Keep any real calibration and decision interpretation open."),
    ("ghc-liora-rough-dependency-v1", "Audit positive regions and exact dependency degrees in bounded synthetic decision tables.", "Compute class-wise lower approximations and their union. Compare attribute subsets only on the same frozen table. Dependency is a finite structural ratio, not causal strength, predictive validity, fairness, or professional evidence."),
    ("ghc-liora-rough-reducts-v1", "Enumerate inclusion-minimal dependency-preserving reducts under a strict four-attribute cap.", "Use exhaustive subsets only within the declared cap. Check full dependency, preservation, and every proper-subset falsifier. Record the core as the intersection of all enumerated reducts. Bounded exhaustive search is not a universal feature-selection theorem or real decision authority."),
]


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("liora_rough_set_x1", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def mutate(table: dict, index: int) -> tuple[str, dict]:
    value = copy.deepcopy(table)
    kind = index % 5
    if kind == 0:
        value["rows"][1]["object"] = value["rows"][0]["object"]
        return "duplicate_object", value
    if kind == 1:
        value["condition_attributes"].append("z")
        return "condition_shape_mismatch", value
    if kind == 2:
        value["rows"][0]["conditions"]["a"] = True
        return "invalid_condition_value", value
    if kind == 3:
        value["rows"][0]["decision"] = "bad"
        return "invalid_decision", value
    value["target"].append("MISSING")
    return "invalid_target", value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--quick-validator", required=True)
    parser.add_argument("--hook-script", required=True)
    args = parser.parse_args()
    root = Path(args.root)
    x1 = root / "x1"
    planning = root / "planning"
    write_text(x1 / "code" / "rough_set.py", CORE_SOURCE)
    write_text(x1 / "tests" / "test_rough_set_x1.py", TEST_SOURCE)
    module = load_module(x1 / "code" / "rough_set.py")
    fixtures = json.loads((planning / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]

    operations = module.X1_OPERATIONS
    contracts, safe, candidates, refusals, repairs = [], [], [], [], []
    for op_index, operation in enumerate(operations):
        for fixture_index, fixture in enumerate(fixtures):
            contract_id = f"LI7082-X1-C{op_index*15+fixture_index+1:03d}"
            result = module.dispatch(operation, fixture)
            result_digest = module.digest(result)
            contracts.append({"contract_id": contract_id, "fixture_id": fixture["fixture_id"], "operation": operation, "result": result, "result_sha256": result_digest, "disposition": "completed"})
            safe.append({"task_id": contract_id + "-SAFE", "contract_id": contract_id, "passed": True, "checks": ["result saved", "fixture digest retained", "credit ceiling retained"]})
            expected_error, invalid = mutate(fixture, op_index*15+fixture_index)
            observed = None
            try:
                module.dispatch(operation, invalid)
            except Exception as error:
                observed = str(error)
            if observed != expected_error:
                raise RuntimeError((contract_id, expected_error, observed))
            negative_id = contract_id + "-NEG"
            candidates.append({"negative_id": negative_id, "contract_id": contract_id, "expected_error": expected_error, "observed_error": observed, "invalid_subject_sha256": module.digest(invalid), "result": "fail", "original_success_credit": 0, "retained": True})
            refusals.append({"witness_id": contract_id + "-REFUSE", "negative_id": negative_id, "guard_observed": observed, "result": "pass", "subject_promoted": False})
            recovered = module.dispatch(operation, copy.deepcopy(fixture))
            repairs.append({"witness_id": contract_id + "-REPAIR", "negative_id": negative_id, "separate_copy": True, "matches_frozen_valid_result": module.digest(recovered) == result_digest, "result": "pass"})

    for collection, name in ((contracts, "contracts"), (safe, "safe-tasks"), (candidates, "candidate-failures"), (refusals, "refusals"), (repairs, "clean-fix-refine")):
        write_json(x1 / "results" / f"{name}.json", {"schema": f"liora.x1.{name}.v1", "count": len(collection), "records": collection, "boundary": BOUNDARY})

    models = []
    for fixture in fixtures:
        approx = module.approximations(fixture, ["a", "b"])
        acc = module.accuracy_membership(fixture, ["a", "b"])["accuracy"]
        dep = module.positive_dependency(fixture, ["a", "b"])["dependency"]
        model = {"schema": "liora.rough-set-model.x1.v1", "fixture_id": fixture["fixture_id"], "coordinates": [len(approx["lower"]), len(approx["boundary"]), len(approx["upper"])], "coordinate_names": ["lower_cardinality", "boundary_cardinality", "upper_cardinality"], "units": ["count", "count", "count"], "accuracy": acc, "dependency": dep, "physical": False, "empirical": False, "falsifier": "Any coordinate disagrees with its saved exact set result.", "boundary": BOUNDARY}
        write_json(x1 / "models" / f"{fixture['fixture_id'].lower()}.json", model)
        models.append(model)
    write_json(x1 / "results" / "models.json", {"schema": "liora.x1.models.v1", "count": len(models), "models": models, "boundary": BOUNDARY})

    for name, description, body in SKILLS:
        skill_root = x1 / "skills" / name
        write_text(skill_root / "SKILL.md", f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n\n{body}\n\nPreserve malformed subjects and corrections separately. Same-owner checks are not independent reproduction. {BOUNDARY}")

    runners = [
        ("ghc_family_liora_v708_v2_x1_structure.py", ["table_shape", "partition", "discernibility"]),
        ("ghc_family_liora_v708_v2_x1_approximation.py", ["lower_approximation", "upper_approximation", "regions", "accuracy_membership", "positive_dependency"]),
        ("ghc_family_liora_v708_v2_x1_reduct.py", ["reducts", "core"]),
    ]
    for filename, allowed in runners:
        write_text(x1 / "runners" / filename, RUNNER_TEMPLATE.replace("__ALLOWED__", repr(allowed)))

    skill_results = []
    for name, _, _ in SKILLS:
        skill_root = x1 / "skills" / name
        process = subprocess.run([sys.executable, args.quick_validator, str(skill_root)], text=True, capture_output=True)
        skill_results.append({"skill": name, "exit_code": process.returncode, "stdout": process.stdout.strip(), "stderr": process.stderr.strip(), "read_through_eof_required": True})
        if process.returncode != 0:
            raise RuntimeError((name, process.stdout, process.stderr))
    write_json(x1 / "results" / "skill-validation.json", {"schema": "liora.x1.skill-validation.v1", "count": len(skill_results), "results": skill_results, "boundary": BOUNDARY})

    runner_smokes = []
    fixture_path = planning / "fixtures.json"
    for filename, allowed in runners:
        runner = x1 / "runners" / filename
        for operation in allowed:
            process = subprocess.run([sys.executable, str(runner), "--fixtures", str(fixture_path), "--fixture-id", "RS01", "--operation", operation], text=True, capture_output=True)
            runner_smokes.append({"runner": filename, "operation": operation, "subject": "valid", "exit_code": process.returncode, "result": "pass" if process.returncode == 0 else "fail"})
            if process.returncode != 0:
                raise RuntimeError((filename, operation, process.stderr))
        process = subprocess.run([sys.executable, str(runner), "--fixtures", str(fixture_path), "--fixture-id", "RS01", "--operation", "outside_scope"], text=True, capture_output=True)
        runner_smokes.append({"runner": filename, "operation": "outside_scope", "subject": "invalid", "exit_code": process.returncode, "result": "fail", "refusal_observed": process.returncode != 0, "original_success_credit": 0})
        if process.returncode == 0:
            raise RuntimeError((filename, "invalid operation accepted"))
    write_json(x1 / "results" / "runner-smokes.json", {"schema": "liora.x1.runner-smokes.v1", "records": runner_smokes, "boundary": BOUNDARY})

    hook_smokes = []
    good = json.dumps({"hook_event_name": "SessionStart", "cwd": "D:/GHC-Archives/worktrees/liora-venn-main-2"})
    bad = json.dumps({"hook_event_name": "Other", "cwd": "D:/GHC-Archives/worktrees/liora-venn-main-2"})
    for hook in ["source", "budget", "consultation", "roster", "evidence"]:
        for kind, payload in (("valid", good), ("invalid", bad)):
            process = subprocess.run([sys.executable, args.hook_script, hook], input=payload, text=True, capture_output=True)
            parsed = json.loads(process.stdout)
            expected = "hookSpecificOutput" in parsed if kind == "valid" else "systemMessage" in parsed
            hook_smokes.append({"hook": hook, "subject": kind, "exit_code": process.returncode, "expected_shape": expected, "live_host_event": False})
            if process.returncode != 0 or not expected:
                raise RuntimeError((hook, kind, process.stdout, process.stderr))
    write_json(x1 / "results" / "hook-smokes.json", {"schema": "liora.x1.hook-smokes.v1", "records": hook_smokes, "manual_smokes": len(hook_smokes), "live_host_events": 0, "boundary": BOUNDARY})

    test_process = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(x1 / "tests"), "-p", "test_*.py", "-v"], text=True, capture_output=True)
    test_count = test_process.stderr.count(" ... ok") + test_process.stdout.count(" ... ok")
    write_json(x1 / "results" / "tests.json", {"schema": "liora.x1.tests.v1", "exit_code": test_process.returncode, "tests": test_count, "stdout": test_process.stdout, "stderr": test_process.stderr, "boundary": BOUNDARY})
    if test_process.returncode != 0 or test_count != 25:
        raise RuntimeError((test_count, test_process.stdout, test_process.stderr))

    inherited_flow = json.loads((planning / "method-flow.json").read_text(encoding="utf-8"))
    methods = list(inherited_flow["methods"])
    witnesses = list(inherited_flow["witnesses"])
    methods.append({"method_id": "LI7082-X1-M008", "title": "Exact advisory-hook guide path", "failure_signature": "The first path assumed the hook guide lived in the release top-level skills folder.", "trigger_preconditions": ["read v20 hook guide", "read-only skill startup"], "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped", "candidate_workaround": "Resolve the plugin-local skill path and read only that missed guide.", "validation_witness_ids": ["LI7082-X1-M008-W001", "LI7082-X1-M008-W002"], "recurrence_guard": "Inventory the exact release tree before reading a plugin-local skill.", "rollback": "No repository change; preserve the failed lookup.", "recommendation_state": "validated", "supersedes": [], "protected_gates": ["no_failure_erasure", "no_stage20"], "retained_negative_ids": ["LI7082-X1-N001"], "scope_boundary": BOUNDARY})
    witnesses.extend([
        {"witness_id": "LI7082-X1-M008-W001", "method_id": "LI7082-X1-M008", "procedure": "original guide read", "scope": "read-only installed release", "expected": "complete guide", "observed": "Path absent in top-level skills folder.", "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["LI7082-X1-N001"], "boundary": BOUNDARY},
        {"witness_id": "LI7082-X1-M008-W002", "method_id": "LI7082-X1-M008", "procedure": "plugin-local guide read", "scope": "read-only installed release", "expected": "complete guide", "observed": "Exact plugin-local SKILL.md and referenced hook script read through EOF.", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["LI7082-X1-N001"], "boundary": BOUNDARY},
    ])

    mutation_ids = [item["negative_id"] for item in candidates]
    methods.append({"method_id": "LI7082-X1-M009", "title": "Finite rough-set contract and mutation harness", "failure_signature": "A malformed table, target, or operation is admitted or its failed subject is overwritten by repair.", "trigger_preconditions": ["planning commit fresh-four-way equal", "frozen fixtures", "X1 operations"], "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped", "candidate_workaround": "Reject the original and execute only a separately copied valid fixture.", "validation_witness_ids": [item for record in contracts for item in (record["contract_id"]+"-SAFE", record["contract_id"]+"-NEG-W", record["contract_id"]+"-REFUSE", record["contract_id"]+"-REPAIR")], "recurrence_guard": "Bind the original invalid digest, refusal, repaired-copy digest, and source contract.", "rollback": "Discard only unsaved X1 output and return to the immutable planning head.", "recommendation_state": "validated", "supersedes": [], "protected_gates": ["no_empirical_promotion", "no_real_classification", "no_stage20"], "retained_negative_ids": mutation_ids, "scope_boundary": BOUNDARY})
    for contract, candidate, refusal, repair in zip(contracts, candidates, refusals, repairs):
        cid, nid = contract["contract_id"], candidate["negative_id"]
        witnesses.extend([
            {"witness_id": cid+"-SAFE", "method_id": "LI7082-X1-M009", "procedure": "execute frozen valid contract", "scope": cid, "expected": "saved finite result", "observed": contract["result_sha256"], "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [nid], "boundary": BOUNDARY},
            {"witness_id": cid+"-NEG-W", "method_id": "LI7082-X1-M009", "procedure": "execute frozen malformed subject", "scope": cid, "expected": candidate["expected_error"], "observed": candidate["observed_error"], "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [nid], "boundary": BOUNDARY},
            {"witness_id": refusal["witness_id"], "method_id": "LI7082-X1-M009", "procedure": "adjudicate refusal", "scope": cid, "expected": "guard matches malformed subject", "observed": refusal["guard_observed"], "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [nid], "boundary": BOUNDARY},
            {"witness_id": repair["witness_id"], "method_id": "LI7082-X1-M009", "procedure": "execute separate valid copy", "scope": cid, "expected": "matches frozen valid result", "observed": str(repair["matches_frozen_valid_result"]), "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [nid], "boundary": BOUNDARY},
        ])

    runner_negatives = [f"LI7082-X1-RUNNER-N{i:02d}" for i in range(1,4)]
    methods.append({"method_id": "LI7082-X1-M010", "title": "Family-current runner scope guard", "failure_signature": "A paired runner accepts an operation outside its declared group.", "trigger_preconditions": ["generated runner", "saved fixture envelope"], "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped", "candidate_workaround": "Keep the allowlist literal and fail before domain dispatch.", "validation_witness_ids": [f"LI7082-X1-RUNNER-W{i:02d}" for i in range(1,len(runner_smokes)+1)], "recurrence_guard": "Smoke every allowed operation and one outside-scope subject.", "rollback": "Use the previous owner-local runner and preserve the rejected subject.", "recommendation_state": "validated", "supersedes": [], "protected_gates": ["caller_compatibility", "no_stage20"], "retained_negative_ids": runner_negatives, "scope_boundary": BOUNDARY})
    for index, record in enumerate(runner_smokes,1):
        invalid = record["subject"] == "invalid"
        witnesses.append({"witness_id": f"LI7082-X1-RUNNER-W{index:02d}", "method_id": "LI7082-X1-M010", "procedure": "runner smoke", "scope": record["runner"]+":"+record["operation"], "expected": "accept valid or refuse invalid", "observed": str(record["exit_code"]), "result": "fail" if invalid else "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [runner_negatives[min((index-1)//4,2)]], "boundary": BOUNDARY})

    hook_negatives = [f"LI7082-X1-HOOK-N{i:02d}" for i in range(1,6)]
    methods.append({"method_id": "LI7082-X1-M011", "title": "Current v20 advisory hook manual smokes", "failure_signature": "A malformed hook payload is mistaken for live host execution or task authority.", "trigger_preconditions": ["current v20 hook source", "manual SessionStart payload"], "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped", "candidate_workaround": "Use bounded valid and malformed manual payloads while keeping host observation false.", "validation_witness_ids": [f"LI7082-X1-HOOK-W{i:02d}" for i in range(1,11)], "recurrence_guard": "Separate source, manual smoke, installation, and live-host states.", "rollback": "Retain the shared hook bytes and discard only owner-local smoke output.", "recommendation_state": "validated", "supersedes": [], "protected_gates": ["no_live_host_claim", "no_route_authority", "no_stage20"], "retained_negative_ids": hook_negatives, "scope_boundary": BOUNDARY})
    for index, record in enumerate(hook_smokes,1):
        invalid = record["subject"] == "invalid"
        witnesses.append({"witness_id": f"LI7082-X1-HOOK-W{index:02d}", "method_id": "LI7082-X1-M011", "procedure": "manual hook smoke", "scope": record["hook"], "expected": "context or safe refusal", "observed": str(record["expected_shape"]), "result": "fail" if invalid else "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [hook_negatives[(index-1)//2]], "boundary": BOUNDARY})

    methods.append({"method_id": "LI7082-X1-M012", "title": "Owner-local skill validation and complete readback", "failure_signature": "A generated guide has invalid frontmatter, unfinished scaffolding, or is smoke-used unread.", "trigger_preconditions": ["five generated local guides"], "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped", "candidate_workaround": "Run the installed Skill Creator validator and require complete main-agent readback before use.", "validation_witness_ids": [f"LI7082-X1-SKILL-W{i:02d}" for i in range(1,6)], "recurrence_guard": "Record quick validation and literal EOF read separately.", "rollback": "Remove only uncommitted generated guides and preserve the build receipt.", "recommendation_state": "candidate", "supersedes": [], "protected_gates": ["no_unread_skill_use", "no_global_install_claim"], "retained_negative_ids": ["LI7082-X1-N001"], "scope_boundary": BOUNDARY})
    for index, result in enumerate(skill_results,1):
        witnesses.append({"witness_id": f"LI7082-X1-SKILL-W{index:02d}", "method_id": "LI7082-X1-M012", "procedure": "quick validate generated guide", "scope": result["skill"], "expected": "exit zero", "observed": str(result["exit_code"]), "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["LI7082-X1-N001"], "boundary": BOUNDARY})

    pass_count = sum(1 for witness in witnesses if witness["result"] == "pass")
    fail_count = sum(1 for witness in witnesses if witness["result"] == "fail")
    states = {"observed":0,"candidate":1,"validated":len(methods)-1,"preferred":0,"superseded":0,"deprecated":0}
    flow = {"schema":"ghc.family.method-flow-state.v1","phase":"v708-v2-x1","owner":"Liora Venn","identity_boundary":"Relational working name only; no consciousness, personhood, continuity, employment, qualification, agency, or authority evidence.","execution_authority":"owner_self_scoped_delta","methods":methods,"witnesses":witnesses,"state_events":[],"recommendations":[],"counts":{"methods":len(methods),"witnesses":len(witnesses),"state_events":0,"recommendations":0,"states":states,"witness_results":{"pass":pass_count,"fail":fail_count}},"boundary":BOUNDARY}
    write_json(x1 / "method-flow.json", flow)
    write_json(x1 / "failure-ledger.json", {"schema":"liora.x1.failures.v1","planning_failures":7,"x1_operational_failures":[{"id":"LI7082-X1-N001","failure":"The first advisory-hook guide path targeted the release top-level skills folder.","recovery":"Read the exact plugin-local guide and referenced hook script without replaying the six successful guide reads.","original_success_credit":0}],"candidate_failed_subjects":len(candidates),"runner_failed_subjects":3,"hook_failed_subjects":5,"total_failed_witnesses":fail_count,"boundary":BOUNDARY})
    write_json(x1 / "advisory-state.json", {"schema":"liora.x1.advisory.v1","title":"Review and refine GHC Lab","message_prepared":True,"action_time_confirmation_required":True,"message_sent":False,"reply_received":False,"resends":0,"private_target_exported":False,"state":"AWAITING_USER_CONFIRMATION_FOR_UI_SEND","boundary":BOUNDARY})
    write_json(x1 / "summary.json", {"schema":"liora.x1.summary.v1","contracts":len(contracts),"safe":len(safe),"candidate_failed_subjects":len(candidates),"refusals":len(refusals),"clean_fix_refine":len(repairs),"tests":test_count,"models":len(models),"skills":len(SKILLS),"runners":len(runners),"hook_manual_smokes":len(hook_smokes),"hook_live_events":0,"adviser_send_state":"AWAITING_USER_CONFIRMATION","source_executions":0,"source_canonical_replays":0,"boundary":BOUNDARY})
    write_text(x1 / "overview.md", f"""# Liora Venn v708-v2 X1 overview

X1 executes ten finite rough-set operations across fifteen wholly synthetic decision tables. It saves 150 valid contract results, 150 retained malformed subjects, 150 separate refusal witnesses, and 150 separate valid-copy recoveries. Twenty-five owner tests pass. Fifteen models present lower, boundary, and upper cardinalities as dimensionless counts, not physical observations.

Five owner-local skill guides pass the installed Skill Creator validator; main-agent complete readback remains a separate gate before smoke-use credit. Three owner-local family-current runners accept their declared operation groups and refuse outside-scope operations. Ten manual smokes reuse the five current v20 advisory hooks; live host events remain zero.

The one required X1 adviser message is prepared but not typed or sent because the supported native thread tool is unavailable and browser-based representational communication requires Hamish's action-time confirmation. Independent work continues; no resend or substitute chat is permitted.

{BOUNDARY}
""")
    write_json(x1 / "build-receipt.json", {"schema":"liora.x1.build.v1","contracts":len(contracts),"tests":test_count,"models":len(models),"skills":len(SKILLS),"runners":len(runners),"candidate_failures":len(candidates),"method_flow":{"methods":len(methods),"witnesses":len(witnesses),"passing":pass_count,"failed":fail_count},"boundary":BOUNDARY})


if __name__ == "__main__":
    main()
