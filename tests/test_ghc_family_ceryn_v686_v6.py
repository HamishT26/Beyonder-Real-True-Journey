"""Frozen independent oracles, nonmutation, report binding, and CLI contracts."""
import copy
import importlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/'scripts'))
from ghc_family_record_selection import (
    ContractError,bounded_json,canonical,make_report,strict_loads,verify_report,
)

PROPOSALS=json.loads((REPO/'docs/ceryn-alder/v686-v6/x1/new-proposals.json').read_text(encoding='utf-8'))['proposals']
CONTEXT={'owner':'Ceryn Alder','phase':'v686-v6',
         'source':'ce48906131524e073b5367a4360753f305086cc0',
         'x1':'5725313ddbc16e1b85c7ce778135f4cac5eab6ee'}
GROUPS={}
for proposal in PROPOSALS:
    GROUPS.setdefault(proposal['operation'],[]).append(proposal)


class FrozenContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.observed={}
        for p in PROPOSALS:
            module=importlib.import_module(Path(p['runner']).stem)
            value=copy.deepcopy(p['input']);before=canonical(value)
            actual=module.evaluate(p['operation'],value)
            cls.observed[p['proposal_id']]=(actual,before==canonical(value))


def oracle_test(operation):
    def test(self):
        for p in GROUPS[operation]:
            with self.subTest(proposal=p['proposal_id']):
                actual,_=self.observed[p['proposal_id']]
                self.assertEqual(canonical(actual),canonical(p['expected_result']))
    return test


def nonmutation_test(operation):
    def test(self):
        for p in GROUPS[operation]:
            with self.subTest(proposal=p['proposal_id']):
                self.assertTrue(self.observed[p['proposal_id']][1])
    return test


def binding_test(operation):
    def test(self):
        for p in GROUPS[operation]:
            actual,_=self.observed[p['proposal_id']]
            report=make_report(p,actual,CONTEXT)
            self.assertTrue(verify_report(p,report,CONTEXT))
            for key,value in [('definition_sha256','0'*64),('input_sha256','0'*64),
                              ('hash_domain','ambiguous'),('empirical',True),('authority',True)]:
                with self.subTest(proposal=p['proposal_id'],mutation=key):
                    changed=copy.deepcopy(report);changed[key]=value
                    self.assertFalse(verify_report(p,changed,CONTEXT))
    return test


for operation in GROUPS:
    setattr(FrozenContracts,'test_'+operation+'_oracle',oracle_test(operation))
    setattr(FrozenContracts,'test_'+operation+'_nonmutation',nonmutation_test(operation))
    setattr(FrozenContracts,'test_'+operation+'_report_binding',binding_test(operation))


class CallerContracts(unittest.TestCase):
    def check_cli(self,rows,runner):
        request={'requests':[{'operation':p['operation'],'input':p['input']} for p in rows]}
        result=subprocess.run([sys.executable,'-X','utf8',str(REPO/'scripts'/runner)],
                              input=canonical(request),capture_output=True,timeout=45,check=True)
        actual=strict_loads(result.stdout)['results']
        self.assertEqual(len(actual),len(rows))
        for p,r in zip(rows,actual):
            self.assertEqual(canonical(r['result']),canonical(p['expected_result']))
            self.assertEqual(r['operation'],p['operation'])
            self.assertIs(r['input_unchanged'],True)

    def test_dotted_literal_projection_cli_regression(self):
        p=next(p for p in PROPOSALS if p['proposal_id']=='CA6866-N118')
        self.check_cli([p],p['runner'])


def cli_test(runner):
    def test(self):
        self.check_cli([p for p in PROPOSALS[::2] if p['runner']==runner],runner)
    return test


for runner in sorted({p['runner'] for p in PROPOSALS}):
    setattr(CallerContracts,'test_cli_'+Path(runner).stem,cli_test(runner))


class InputGuards(unittest.TestCase):
    def test_duplicate_json_key_is_rejected(self):
        with self.assertRaisesRegex(ContractError,'DUPLICATE_KEY'):
            strict_loads('{"a":1,"a":2}')

    def test_nonfinite_value_is_rejected(self):
        with self.assertRaisesRegex(ContractError,'NONFINITE_VALUE'):
            bounded_json({'a':float('nan')})

    def test_nontext_mapping_key_is_rejected(self):
        with self.assertRaisesRegex(ContractError,'NON_TEXT_KEY'):
            bounded_json({1:'a'})

    def test_node_budget_is_enforced(self):
        with self.assertRaisesRegex(ContractError,'INPUT_BUDGET'):
            bounded_json([0]*1001)

    def test_depth_budget_is_enforced(self):
        value=0
        for _ in range(17):value=[value]
        with self.assertRaisesRegex(ContractError,'INPUT_BUDGET'):
            bounded_json(value)

    def test_unknown_operation_is_refused(self):
        for runner in {p['runner'] for p in PROPOSALS}:
            module=importlib.import_module(Path(runner).stem)
            self.assertEqual(module.evaluate('unknown',{}),{'ok':False,'reason':'UNKNOWN_OPERATION'})


if __name__=='__main__':
    unittest.main()
