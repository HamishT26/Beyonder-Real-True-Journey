"""Focused independent boundary tests for the new owner code."""
import json
import math
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ghc_family_claim_evidence_lab import evaluate, acyclic, holm, bh
from ghc_family_unit_fraction_witness import verify, witness
from ghc_family_thirty_seat_schedule import CYCLE, project, route_decision, rotation_decision, ordinal
from ghc_family_scoped_bundle_seal import safe_relative
from ghc_family_plan_contract import validate

class BoundaryTests(unittest.TestCase):
    def test_boolean_is_not_phase(self):
        with self.assertRaises(ValueError):
            ordinal(True, 1)

    def test_boolean_is_not_unique_match_count(self):
        self.assertEqual(route_decision({"current_hold":False,"acknowledgement":None,
            "guards_current":True,"unique_title_matches":True,"owner_terminal":True,
            "action":"activate"}), "HELD_ROUTE_GAP")

    def test_default_hold(self):
        self.assertEqual(route_decision({}), "HELD_CURRENT_INSTRUCTION")

    def test_old_acknowledgement_cannot_resend(self):
        self.assertEqual(route_decision({"current_hold":False,"acknowledgement":"opaque"}), "HELD_NO_RESEND")

    def test_controller_cannot_induct_someone_elses_seat(self):
        self.assertEqual(route_decision({"current_hold":False,"acknowledgement":None,"guards_current":True,
            "unique_title_matches":1,"owner_terminal":True,"action":"create","task_kind":"main",
            "model":"gpt-6-astra","thinking":"max","already_created":False,
            "controller":"Rowan Ash","future_seat":CYCLE[3]}), "HELD_CONTROLLER_MISMATCH")

    def test_existing_future_is_reused(self):
        self.assertEqual(route_decision({"current_hold":False,"guards_current":True,"unique_title_matches":1,
            "owner_terminal":True,"action":"create","task_kind":"main","model":"gpt-6-astra",
            "thinking":"max","already_created":True}), "REUSE_EXISTING_MAIN_TASK")

    def test_horizon(self):
        rows=project()
        self.assertEqual(len(rows),324)
        self.assertEqual(rows[2]["owner"],"Elaren Kestrel")
        self.assertEqual((rows[3]["version"],rows[3]["slot"]), (685,8))
        self.assertEqual((rows[4]["owner"],rows[4]["version"],rows[4]["slot"]), ("Neris Solane",686,1))
        self.assertEqual(rows[-1]["owner"],CYCLE[23])

    def test_file_ceiling_precedence(self):
        self.assertEqual(rotation_decision(2,2000),"REVIEW_ROTATION")

    def test_negative_workload_refused(self):
        with self.assertRaises(ValueError):
            rotation_decision(2,-1)

    def test_positive_and_distinct_variants(self):
        self.assertTrue(verify(2,[1,2,2],distinct=False))
        self.assertFalse(verify(2,[1,2,2],distinct=True))

    def test_boolean_denominator_refused(self):
        self.assertFalse(verify(3,[True,4,12]))

    def test_zero_denominator_refused(self):
        self.assertFalse(verify(3,[0,4,12]))

    def test_permuted_distinct_denominators_refused(self):
        self.assertFalse(verify(5,[20,4,2]))

    def test_wrong_rational_witness_refused(self):
        self.assertFalse(verify(5,[2,4,21]))

    def test_known_even_identity(self):
        self.assertEqual(witness(14)["denominators"],[7,8,56])

    def test_invalid_search_budget_refused(self):
        with self.assertRaises(ValueError):
            witness(7,seconds=float("nan"))

    def test_unknown_rule_refused(self):
        self.assertFalse(evaluate("imagined_family",0,{}))

    def test_boolean_rule_index_refused(self):
        self.assertFalse(evaluate("units",True,{}))

    def test_nonobject_payload_refused(self):
        self.assertFalse(evaluate("time",0,[]))

    def test_missing_fields_refused(self):
        self.assertFalse(evaluate("uncertainty",2,{}))

    def test_impossible_calendar_date_refused(self):
        self.assertFalse(evaluate("time",0,{"event":"2026-02-30T00:00:00Z"}))

    def test_infinite_uncertainty_refused(self):
        self.assertFalse(evaluate("uncertainty",0,{"u":float("inf")}))

    def test_three_node_cycle(self):
        self.assertFalse(acyclic(["a","b","c"],[["a","b"],["b","c"],["c","a"]]))

    def test_cycle_free_diamond(self):
        self.assertTrue(acyclic(["a","b","c","d"],[["a","b"],["a","c"],["b","d"],["c","d"]]))

    def test_holm_independent_example(self):
        self.assertEqual(holm([.1,.2,.3]),[.30000000000000004,.4,.4])

    def test_bh_monotonic_adjustment(self):
        actual=bh([.001,.01,.04,.2])
        expected=[.004,.02,.05333333333333334,.2]
        self.assertTrue(all(math.isclose(a,b) for a,b in zip(actual,expected)))

    def test_path_traversal_refused(self):
        self.assertFalse(safe_relative("docs/../private"))

    def test_absolute_path_refused(self):
        self.assertFalse(safe_relative("/outside"))

    def test_control_character_path_refused(self):
        self.assertFalse(safe_relative("docs/line\nbreak"))

    def test_owned_relative_path(self):
        self.assertTrue(safe_relative("docs/rowan-ash/report.json"))

    def test_nonobject_plan_refused(self):
        self.assertEqual(validate([]),["Expected an object"])

    def test_missing_workload_plan_refused(self):
        self.assertEqual(len(validate({})),6)

if __name__=="__main__":
    unittest.main(verbosity=2)
