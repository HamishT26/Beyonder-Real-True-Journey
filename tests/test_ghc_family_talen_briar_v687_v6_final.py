"""Final owner evidence bindings and truth-accounting invariants."""
import hashlib
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PREFIX = 'docs/talen-briar/v687-v6/'
def read(path):
    return json.loads((ROOT/(PREFIX+path)).read_text('utf-8'))

class FinalEvidence(unittest.TestCase):
    def test_method_flow_compatibility_and_nonerasure(self):
        index = read('final/method-flow-compatibility.json')
        path = ROOT / index['validator']['path']
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), index['validator']['normalized_lf_sha256'])
        spec = importlib.util.spec_from_file_location('owner_mf_validator', path)
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        for item in index['projections']:
            original = json.loads((ROOT/item['source_path']).read_text('utf-8'))
            corrected = json.loads((ROOT/item['path']).read_text('utf-8'))
            self.assertEqual(original['witnesses'], corrected['witnesses'])
            self.assertEqual(validator.validate_ledger(corrected)['issues'], [])
        self.assertEqual(validator.validate_ledger(json.loads((ROOT/index['repair_ledger']).read_text('utf-8')))['issues'], [])

    def test_outcomes(self):
        truth = read('final/phase-truth.json')
        self.assertEqual(truth['outcomes'], dict(completed=125, represented=39, open_gap=20, exact_gate=16))
        self.assertEqual(sum(truth['outcomes'].values()), 200)

    def test_accounting(self):
        reg = read('closeout/retained-negative-register.json')
        for key in ['methods', 'failed_witnesses', 'passing_witnesses']:
            self.assertEqual(sum(g[key] for g in reg['groups']), reg['owner_delta'][key])
        for key, value in reg['owner_delta'].items():
            self.assertEqual(reg['inherited_activation_baseline'][key]+value, reg['effective'][key])
        self.assertEqual(reg['erased_negative_count'], 0)

    def test_failure_retention(self):
        rows = read('x2/mutation-results.json')
        self.assertEqual(len(rows), 1000)
        self.assertEqual(len({r['negative_id'] for r in rows}), 1000)
        self.assertTrue(all(r['oracle_rejected'] and r['original_success_credit'] == 0 for r in rows))

    def test_baton_binding(self):
        index = read('handoffs/baton-index.json')
        raw = (ROOT/index['path']).read_bytes().replace(b'\r\n', b'\n')
        self.assertEqual(hashlib.sha256(raw).hexdigest(), index['sha256'])
        self.assertEqual(len(raw.split()), index['words'])
        self.assertEqual(index['modules'], 13)
        self.assertGreaterEqual(index['words'], 10000)
        self.assertLessEqual(index['words'], 100000)
        self.assertTrue(raw.decode().rstrip().endswith(index['eof']))

    def test_deck_graph(self):
        index = read('x2/deck/deck-index.json')
        cards = {c['card_id']:c for c in index['cards']}
        self.assertEqual(len(cards), 234)
        for c in cards.values():
            if c['tier'] == 1:
                self.assertEqual(c['parent_ids'], [])
            else:
                self.assertEqual(len(c['parent_ids']), 1)
                self.assertEqual(cards[c['parent_ids'][0]]['tier'], c['tier']-1)

    def test_promotion_source_bytes(self):
        proof = read('x2/promotion-receipt.json')
        self.assertEqual(len(proof['members']), 66)
        for member in proof['members']:
            self.assertEqual(hashlib.sha256((ROOT/member['source']).read_bytes()).hexdigest(), member['sha256'])
        self.assertEqual(proof['overwrites'], 0)

    def test_portfolio_held_actions(self):
        p = read('x2/portfolio-results.json')['portfolios']
        for name, number in [('safe_now',300),('candidates',250),('clean_fix_refine',300)]:
            self.assertEqual(len(p[name]), number)
            self.assertTrue(all(r['outcome'] == 'completed' and r['procedure_passed'] for r in p[name]))
        for name, number in [('exact_packets',50),('blocked_packets',30)]:
            self.assertEqual(len(p[name]), number)
            self.assertTrue(all(r['outcome'] == 'exact_gate' and not r['external_action_executed'] for r in p[name]))

    def test_package_transaction(self):
        receipt = read('x2/environment-receipt.json')
        self.assertEqual(len(receipt['wheels']), 8)
        self.assertTrue(all(w['verified'] for w in receipt['wheels']))
        self.assertEqual(receipt['direct_additions'], 3)
        smoke = read('x2/package-smokes.json')
        self.assertEqual((smoke['positive_passes'],smoke['adverse_rejections']), (3,3))

    def test_terminal_layers_separate(self):
        truth = read('final/phase-truth.json')
        self.assertEqual(truth['canonical_invocations'], 0)
        self.assertEqual(truth['canonical_replays'], 0)
        self.assertEqual(truth['successor_messages'], 0)
        self.assertEqual(truth['route_state'], 'PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED')
        self.assertEqual(truth['terminal_verdict'], 'NOT_READY_FOR_STAGE_20')
        self.assertEqual(truth['next_owner'], 'Orin Thale')

    def test_lifecycle_contract(self):
        c = read('closeout/canonical-contract.json')
        self.assertEqual(c['source'], 'f815c68a704065970717f8d88305489a0966cd9c')
        self.assertEqual(c['x1'], '1fd150a6de48f02d847b2c949e388345ee5d3f2f')
        self.assertEqual(c['evidence'], '42d003be1a62858084c8b38bdccfba629fae23ad')
        self.assertEqual(c['canonical_invocation_budget'], 1)
        self.assertFalse(c['full_repository_suite'])

if __name__ == '__main__':
    unittest.main()
