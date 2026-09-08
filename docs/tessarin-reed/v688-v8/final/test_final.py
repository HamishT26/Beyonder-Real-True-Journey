import hashlib
import json
import pathlib
import re
import unittest
import ast
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ghc_family_dfa_canonical import privacy_candidates

P = pathlib.Path(__file__).resolve().parent.parent

def read(name):
    return json.loads((P / name).read_text(encoding='utf-8'))

class Final(unittest.TestCase):
    def test_outcomes(self):
        self.assertEqual(read('final/phase-truth.json')['outcomes'], {'completed': 170, 'represented': 17, 'open_gap': 3, 'exact_gate': 10})

    def test_truth_arithmetic(self):
        before = read('x1/phase-truth.json')['activation_baseline']
        after = read('final/phase-truth.json')['effective_counts']
        self.assertEqual({k: after[k] - before[k] for k in before}, {'proposals': 200, 'negatives': 380, 'methods': 50, 'failed_witnesses': 475, 'passing_witnesses': 115, 'open_gaps': 3, 'exact_gates': 10})

    def test_baton(self):
        index = read('final/baton-index.json')
        data = (P / 'handoffs/caelen-morrow-v689-v1-activation-baton.md').read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), index['sha256'])
        self.assertTrue(10000 <= len(data.decode().split()) <= 100000)
        self.assertEqual(len(re.findall(r'^## Module ', data.decode(), re.M)), 13)

    def test_no_send(self):
        self.assertEqual(read('final/terminal-route.json')['state'], 'PREPARED_NOT_SENT')
        self.assertEqual(read('final/phase-truth.json')['successor_contacts'], 0)

    def test_no_canonical_preclaim(self):
        self.assertEqual(read('final/phase-truth.json')['canonical_successes'], 0)
        self.assertEqual(read('final/phase-truth.json')['terminal_verdict'], 'NOT_READY_FOR_STAGE_20')

    def test_lifecycle_policy(self):
        policy = read('final/canonical-policy.json')
        self.assertEqual(sum(r['expected_tests'] for r in policy['test_modules']), 53)
        self.assertEqual(len(policy['test_modules']), 4)
        self.assertFalse(policy['full_repository_suite'])

    def test_portfolio(self):
        result = read('x2/portfolio-results.json')
        self.assertEqual(result['predicate_passes'], 850)
        self.assertTrue(all(not r['action_executed'] for r in result['records'] if r['group'] in ['exact_packets', 'blocked_packets']))

    def test_tools(self):
        result = read('x2/tool-promotion.json')
        self.assertEqual((result['skill_count'], result['runner_count'], result['overwrite_count']), (10, 5, 0))
        self.assertEqual(len(result['smokes']), 190)
        self.assertTrue(all(r['predicate_pass'] for r in result['smokes']))

    def test_packages(self):
        self.assertEqual(read('x2/package-smokes.json')['comparisons'], 420)
        self.assertEqual(len(read('x2/package-transaction.json')['verified_artifacts']), 7)

    def test_failure_retention(self):
        self.assertEqual(read('x2/retained-negatives.json')['erased_negative_count'], 0)
        self.assertFalse(read('x2/manifest-probe-v1.json')['valid'])
        self.assertTrue(read('x2/manifest-probe-v2.json')['valid'])

    def test_privacy_definition_boundary(self):
        text = (P / 'final/ghc_family_dfa_canonical.py').read_text()
        tree = ast.parse(text)
        patterns = next(ast.literal_eval(n.value) for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'patterns' for t in n.targets))
        hits, definitions = privacy_candidates('docs/tessarin-reed/v688-v8/final/ghc_family_dfa_canonical.py', text, patterns)
        self.assertEqual(hits, [])
        self.assertGreaterEqual(len(definitions), 1)
        payload = '<' + 'codex_delegation' + '>synthetic</' + 'codex_delegation' + '>'
        self.assertEqual(len(privacy_candidates('synthetic.json', payload, patterns)[0]), 1)

if __name__ == '__main__':
    unittest.main()
