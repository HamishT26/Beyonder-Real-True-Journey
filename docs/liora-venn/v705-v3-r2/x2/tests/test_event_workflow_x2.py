from __future__ import annotations
import sys, unittest
from pathlib import Path
sys.dont_write_bytecode=True
X2=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(X2/"code")); import event_workflow_x2 as ew

class EventWorkflowX2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.fixtures=ew.load_fixtures(); cls.contracts=ew.load_contracts("x2"); cls.models=ew.load_models()

def add_operation_test(index, operation):
    def test(self):
        observation=ew.OPERATIONS[operation](self.fixtures["LEW-01"])
        self.assertIsInstance(observation,dict); self.assertTrue(ew.x1.sha256_json(observation))
    setattr(EventWorkflowX2Tests,f"test_{index:02d}_operation_{operation}",test)

for index, operation in enumerate(ew.X2_OPERATIONS,1): add_operation_test(index,operation)

def add_model_test(index):
    def test(self): self.assertTrue(ew.validate_model(self.models[index-1])["valid"])
    setattr(EventWorkflowX2Tests,f"test_{index+10:02d}_model_{index:02d}",test)

for index in range(1,16): add_model_test(index)

def test_26_contract_count(self): self.assertEqual(150,len(self.contracts))
def test_27_outcomes(self):
    from collections import Counter
    self.assertEqual(Counter({"completed":105,"represented":15,"open_gap":15,"exact_gate":15}),Counter(row["expected_disposition"] for row in self.contracts))
def test_28_gap_stays_open(self): self.assertTrue(ew.live_service_observation_gap(self.fixtures["LEW-01"])["gap_open"])
def test_29_authority_stays_held(self): self.assertTrue(ew.protected_authority_hold(self.fixtures["LEW-01"])["held"])
def test_30_no_external_actions(self): self.assertTrue(all(ew.execute_contract(row,self.fixtures[row["request"]["fixture_id"]])["external_actions"]==0 for row in self.contracts))
EventWorkflowX2Tests.test_26_contract_count=test_26_contract_count
EventWorkflowX2Tests.test_27_outcomes=test_27_outcomes
EventWorkflowX2Tests.test_28_gap_stays_open=test_28_gap_stays_open
EventWorkflowX2Tests.test_29_authority_stays_held=test_29_authority_stays_held
EventWorkflowX2Tests.test_30_no_external_actions=test_30_no_external_actions

if __name__=="__main__": unittest.main()
