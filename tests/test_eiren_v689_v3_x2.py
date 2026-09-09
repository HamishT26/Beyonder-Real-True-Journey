import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_experiment_evidence_core as core

PHASE = ROOT / "docs/eiren-kestrel/v689-v3"

def read(path): return json.loads((PHASE / path).read_text(encoding="utf-8"))

def test_all_x2_frozen_contracts_match_and_preserve_inputs():
    for row in read("plan/new-proposals.json")["proposals"][100:]:
        request=copy.deepcopy(row["request"]); original=copy.deepcopy(request)
        assert core.evaluate(request)==row["expected"] and request==original

def test_all_x2_candidates_are_refused_before_operation():
    for row in read("plan/new-proposals.json")["proposals"][100:]:
        request=copy.deepcopy(row["request"]); request["execute"]=True
        assert core.evaluate(request)=={"ok":False,"value":None,"error":"E_FIELDS"}

def test_x2_results_and_outcome_vocabulary():
    rows=read("x2/results.json")["results"]
    assert len(rows)==100 and all(row["exact_match"] and row["input_unchanged"] for row in rows)
    assert {row["outcome"] for row in rows}<={"completed","represented","open_gap","exact_gate"}

def test_x2_inherited_refinements_are_lossless():
    rows=read("x2/inherited-refinements.json")["records"]
    assert len(rows)==100 and all(row["lossless"] and row["source_digest_match"] for row in rows)

def test_paired_effect_retains_signed_differences():
    assert core.paired_effect([1,4],[3,2])["deltas"]==["2","-2"]

def test_sign_test_ties_do_not_enter_denominator():
    assert core.sign_test([1,0,-1,0])=={"positive":1,"negative":1,"ties":2,"two_sided_p":"1","independence_verified":False}

def test_permutation_gap_enumerates_declared_group_size():
    assert core.permutation_gap([1,2,3,4],[0,1])["enumerated_assignments"]==6

def test_bootstrap_grid_is_explicit_not_stochastic():
    value=core.bootstrap_grid([1,3],[[0,0],[1,1]])
    assert value["means"]==["1","3"] and value["stochastic_claimed"] is False

def test_confusion_profile_keeps_undefined_rate_null():
    assert core.confusion_profile([0,0],[0,1])["sensitivity"] is None

def test_agreement_kappa_preserves_independence_boundary():
    assert core.agreement_kappa(["a","b"],["a","b"],["a","b"])["reviewer_independence_verified"] is False

def test_missingness_does_not_impute_and_provenance_has_frontier():
    assert core.missingness_map([{"a":None}], ["a"])["values_inferred"] is False
    a="a"*64; b="b"*64
    assert core.provenance_frontier([{"id":"a","parents":[],"digest":a},{"id":"b","parents":["a"],"digest":b}])["frontier"]==["b"]

def test_release_and_authority_operations_never_execute():
    grant={"artifact":"d","purposes":["review"],"expires":10,"revoked":False}
    assert core.release_scope(grant,5,"review","d")["release_executed"] is False
    assert core.authority_reservation("stage20_promotion",True)["executed"] is False
