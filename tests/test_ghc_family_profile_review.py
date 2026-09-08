"""Protect the new live-profile route from concrete mutations."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from ghc_family_workflow_profile_review import validate

class ProfileReview(unittest.TestCase):
    def setUp(self):
        self.profile=json.loads((ROOT/'workflow/current-workflow.json').read_text())
        self.route=json.loads((ROOT/'workflow/thirty-seat-schedule.json').read_text())
    def test_current_profile_is_valid_but_does_not_prove_delivery(self):
        result=validate(self.profile,self.route)
        self.assertTrue(result['valid']);self.assertFalse(result['delivery_verified'] or result['permission_granted'])
    def test_changed_phase_owner_is_rejected(self):
        self.route['assignments'][1]['owner']='Eiren Kestrel'
        self.assertFalse(validate(self.profile,self.route)['valid'])
    def test_skipped_phase_is_rejected(self):
        self.route['assignments'][1]['phase']='v689-v5'
        self.assertFalse(validate(self.profile,self.route)['valid'])
    def test_wrong_outbound_target_is_rejected(self):
        self.route['current_outbound']['owner']='Rowan Ash'
        self.assertFalse(validate(self.profile,self.route)['valid'])
    def test_unconfirmed_route_is_rejected(self):
        self.route['user_confirmed_normalization']=False
        self.assertFalse(validate(self.profile,self.route)['valid'])
    def test_unsafe_capacity_is_rejected(self):
        self.profile['limits']['owner_file_ceiling']=2001
        self.assertFalse(validate(self.profile,self.route)['valid'])
    def test_out_of_range_workload_is_rejected(self):
        self.profile['phase_targets']['safe_now_x1']=99
        self.assertFalse(validate(self.profile,self.route)['valid'])
    def test_overlong_baton_policy_is_rejected(self):
        self.profile['limits']['baton_words'][1]=100001
        self.assertFalse(validate(self.profile,self.route)['valid'])
    def test_malformed_nested_metadata_is_a_refusal(self):
        self.profile['phase_targets']=[]
        self.assertFalse(validate(self.profile,self.route)['valid'])

if __name__=='__main__':unittest.main()
