"""Behavioral invariants beyond the frozen happy-path examples."""
import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import ghc_family_workflow_core as core

class WorkflowInvariants(unittest.TestCase):
    def test_nested_nonstring_enums_are_structured_refusals(self):
        templates=[
          {'op':'context_window','rows':[{'id':'a','ordinal':1,'state':[]}],'count':1},
          {'op':'witness_accounting','rows':[{'id':'a','subject':[],'check':'pass'}]},
          {'op':'tool_select','tools':[{'name':'a','triggers':['hash'],'status':[],'evidence':'validated'}],'trigger':'hash'}]
        for request in templates:
            self.assertEqual(core.evaluate(request),{'ok':False,'value':None,'error':'type'})

    def test_phase_advancement_composes_across_wraps(self):
        for initial in ['v1-v1','v689-v8','v725-v7']:
            first=core.phase_advance({'phase':initial,'delta':7})
            composed=core.phase_advance({'phase':first,'delta':23})
            direct=core.phase_advance({'phase':initial,'delta':30})
            self.assertEqual(composed,direct)

    def test_partition_preserves_total_and_bound(self):
        for total in range(40):
            for size in range(1,8):
                batches=core.quota_partition({'total':total,'batch':size})
                self.assertEqual(sum(batches),total)
                self.assertTrue(all(1<=x<=size for x in batches))

    def test_every_consumed_transport_refuses_a_second_submission(self):
        for terminal in ['acknowledged','opaque_accepted','rejected']:
            accepted=['prepared','submitted',terminal]
            self.assertTrue(core.evaluate({'op':'delivery_reduce','events':accepted})['ok'])
            self.assertEqual(core.evaluate({'op':'delivery_reduce','events':accepted+['submitted']})['error'],'sequence')

    def test_unavailable_transport_never_becomes_sent(self):
        observed=core.delivery_reduce({'events':['prepared','unavailable']})
        self.assertEqual(observed,'PREPARED_NOT_SENT_ROUTE_UNAVAILABLE')

    def test_overlay_changes_are_detached(self):
        request={'op':'overlay_fold','base':{'a':1},'events':[{'sequence':1,'changes':{'a':2},'reason':'explicit correction'}]}
        before=copy.deepcopy(request);output=core.evaluate(request)
        output['value']['current']['a']=3
        self.assertEqual(request,before)

    def test_manifest_differences_invert_added_and_removed(self):
        a=[{'path':'a','bytes':1,'sha256':'a'*64}]
        b=[{'path':'b','bytes':1,'sha256':'b'*64}]
        forward=core.manifest_diff({'before':a,'after':b})
        reverse=core.manifest_diff({'before':b,'after':a})
        self.assertEqual(forward['added'],reverse['removed'])
        self.assertEqual(forward['removed'],reverse['added'])

    def test_dependency_cycles_terminate_without_claiming_topological_order(self):
        self.assertEqual(core.dependency_closure({'graph':{'a':['b'],'b':['a']},'roots':['a']}),['a','b'])

    def test_deck_selection_is_ancestor_closed(self):
        cards=[{'id':str(i),'tier':i,'parent':str(i-1) if i>1 else None} for i in range(1,5)]
        self.assertEqual(core.card_selection({'cards':cards,'selected':['4']}),['1','2','3','4'])
        self.assertEqual(core.card_selection({'cards':cards,'selected':['2']}),['1','2'])

    def test_deck_cycles_and_budget_excess_are_refused(self):
        cycle=[{'id':'a','tier':1,'parent':None},{'id':'b','tier':2,'parent':'c'},{'id':'c','tier':3,'parent':'b'}]
        self.assertFalse(core.evaluate({'op':'deck_parents','cards':cycle})['ok'])
        self.assertFalse(core.evaluate({'op':'deck_parents','cards':[{'id':str(i),'tier':1,'parent':None} for i in range(2001)]})['ok'])

    def test_failed_subject_is_never_original_success_credit(self):
        result=core.witness_accounting({'rows':[{'id':'a','subject':'fail','check':'pass'},{'id':'b','subject':'pass','check':'fail'}]})
        self.assertEqual(result['original_success_credit'],0)

    def test_strict_json_rejects_duplicate_keys_and_nonfinite_values(self):
        for raw in ['{"op":"budget_check","op":"file_budget"}','{"x":NaN}','{"x":Infinity}']:
            with self.assertRaises(core.ContractError):core.strict_json(raw)

    def test_command_interface_returns_structured_refusal(self):
        script=ROOT/'scripts/ghc_family_workflow_core.py'
        for raw in [b'{"op":"budget_check","op":"file_budget"}',b'{"x":NaN}',b'\xff']:
            p=subprocess.run([sys.executable,'-X','utf8','-B',str(script)],input=raw,capture_output=True,timeout=10)
            self.assertEqual(p.returncode,2)
            self.assertFalse(json.loads(p.stdout)['ok'])

    def test_extra_root_fields_cannot_change_a_declared_operation(self):
        request={'op':'budget_check','count':100,'minimum':100,'maximum':500,'extra':True}
        self.assertEqual(core.evaluate(request),{'ok':False,'value':None,'error':'schema'})

    def test_path_prefixes_do_not_cross_owner_segments(self):
        self.assertFalse(core.path_scope({'path':'docs/seren-other/a','roots':['docs/seren']}))
        for path in ['../a','a//b','a/./b','a/../b','/a','a\\b']:
            self.assertFalse(core.evaluate({'op':'path_scope','path':path,'roots':['a']})['ok'])

if __name__=='__main__':unittest.main()
