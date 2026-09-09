import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_measurement_design_core as core

PHASE = ROOT / "docs/eiren-kestrel/v689-v3"

def read(path): return json.loads((PHASE / path).read_text(encoding="utf-8"))

def test_all_x1_frozen_contracts_match_and_preserve_inputs():
    proposals = read("plan/new-proposals.json")["proposals"][:100]
    for row in proposals:
        request = copy.deepcopy(row["request"]); original = copy.deepcopy(request)
        assert core.evaluate(request) == row["expected"]
        assert request == original

def test_all_x1_candidates_are_refused_before_operation():
    for row in read("plan/new-proposals.json")["proposals"][:100]:
        request = copy.deepcopy(row["request"]); request["execute"] = True
        assert core.evaluate(request) == {"ok": False, "value": None, "error": "E_FIELDS"}

def test_x1_results_and_outcome_vocabulary():
    result = read("x1/results.json")
    assert result["count"] == len(result["results"]) == 100
    assert all(row["exact_match"] and row["input_unchanged"] for row in result["results"])
    assert {row["outcome"] for row in result["results"]} <= {"completed", "represented", "open_gap", "exact_gate"}

def test_inherited_refinements_are_lossless_and_zero_credit():
    rows = read("x1/inherited-refinements.json")["records"]
    assert len(rows) == 100
    assert all(row["lossless"] and row["source_digest_match"] for row in rows)
    assert all(row["novelty_credit"] == row["source_execution_credit"] == 0 for row in rows)

def test_replicate_residuals_sum_to_zero():
    value = core.replicate_summary([1, 2, 4])
    from fractions import Fraction
    assert sum(map(Fraction, value["residuals"])) == 0

def test_weighted_mean_stays_inside_declared_range():
    from fractions import Fraction
    value = Fraction(core.weighted_mean([1, 5], [1, 3])["mean"])
    assert Fraction(1) <= value <= Fraction(5)

def test_uncertainty_variance_is_sum_of_squared_contributions():
    assert core.uncertainty_budget([["a", 1, 3], ["b", 1, 4]])["combined_variance"] == "25"

def test_randomized_block_contains_each_treatment_once_per_block():
    rows = core.randomized_block(["a", "b", "c"], 3, 1)["blocks"]
    assert all(sorted(row["order"]) == ["a", "b", "c"] for row in rows)

def test_latin_square_rows_and_columns_are_balanced():
    rows = core.latin_square(["a", "b", "c"], 0)["rows"]
    assert all(sorted(row) == ["a", "b", "c"] for row in rows)
    assert all(sorted(row[i] for row in rows) == ["a", "b", "c"] for i in range(3))

def test_factorial_design_has_complete_two_level_rows():
    value = core.factorial_design(["a", "b", "c"])
    assert value["run_count"] == 8 and len({tuple(row) for row in value["rows"]}) == 8

def test_sample_registry_distinguishes_empty_sample_and_census():
    assert core.sample_registry(3, [])["coverage"] == "0"
    assert core.sample_registry(3, [0, 1, 2])["complete_census"] is True

def test_x2_implementation_is_absent_at_x1():
    assert not (ROOT / "scripts/ghc_family_experiment_evidence_core.py").exists()
    assert not (PHASE / "x2").exists()
