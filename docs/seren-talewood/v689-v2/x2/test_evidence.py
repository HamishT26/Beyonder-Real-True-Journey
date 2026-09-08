"""Verify owner evidence joins, retained failures, and content-addressed cards."""
import hashlib
import json
import sys
import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'x2/code'))
from execute_frozen import canonical, digest
from ghc_family_cfg_core import strict_loads


def load(relative):
    return strict_loads((ROOT / relative).read_text(encoding='utf-8'))


def ledgers():
    index = load('x2/method-flow-index.json')
    return [load(index['startup'])] + [load(path) for path in index['shards']]


class EvidenceJoins(unittest.TestCase):
    def test_source_seal_overlay_baseline_and_phase_arithmetic(self):
        source = load('x1/activation-baseline.json')
        counts = load('x2/count-reconciliation.json')
        self.assertEqual(counts['source_post_final_overlay'], source['external_activation_overlay'])
        for key, value in source['activation_baseline'].items():
            self.assertEqual(source['repository_sealed'][key] + source['external_activation_overlay'].get(key, 0), value)
            self.assertEqual(value + counts['owner_delta'][key], counts['represented_chain_after'][key])
        self.assertEqual(counts['owner_delta']['proposals'], 200)
        self.assertFalse(counts['aggregate_mapping_complete'])

    def test_contract_results_bind_all_frozen_inputs_and_envelopes(self):
        proposals = load('x1/new-proposals.json')['proposals']
        outcomes = Counter()
        for index, proposal in enumerate(proposals, 1):
            result = load(f'x2/contracts/{index:03}.json')
            for field in ['input', 'expected']:
                self.assertEqual(canonical(result[field]), canonical(proposal[field]))
                self.assertEqual(result[field + '_sha256'], digest(proposal[field]))
            self.assertEqual(result['expected_sha256'], result['observed_sha256'])
            self.assertTrue(result['whole_envelope_equal'] and result['input_unchanged'])
            outcomes[result['outcome']] += 1
        self.assertEqual(outcomes, {'completed': 190, 'represented': 10})

    def test_portfolio_completeness_and_refusal_separation(self):
        frozen = load('x1/approval-portfolio.json')
        results = load('x2/portfolio-results.json')
        for group in ['safe_now', 'candidates', 'clean_fix_refine']:
            self.assertEqual({r['task_id'] for r in frozen[group]}, {r['task_id'] for r in results[group]})
            self.assertTrue(all(r['validation_passed'] and r['novelty_credit'] == 0 for r in results[group]))
            for row in results[group]:
                if not row['observed_predicate']:
                    self.assertEqual(row['witness_result'], 'fail')
                    self.assertEqual(row['failed_witness_credit'], 0)
        self.assertEqual(Counter(r['category'] for r in results['clean_fix_refine']), {'CLEAN': 100, 'FIX': 100, 'REFINE': 100})

    def test_method_ids_and_witnesses_are_unique_and_bidirectionally_bound(self):
        all_ledgers = ledgers()
        methods = [m for ledger in all_ledgers for m in ledger['methods']]
        witnesses = [w for ledger in all_ledgers for w in ledger['witnesses']]
        self.assertEqual(len(methods), len({m['method_id'] for m in methods}))
        self.assertEqual(len(witnesses), len({w['witness_id'] for w in witnesses}))
        self.assertEqual(len(methods), 242)
        self.assertEqual(Counter(w['result'] for w in witnesses), {'fail': 616, 'pass': 726})
        for method in methods:
            linked = {w['witness_id'] for w in witnesses if w['method_id'] == method['method_id']}
            self.assertEqual(set(method['validation_witness_ids']), linked)
            self.assertTrue(any(w['result'] == 'pass' for w in witnesses if w['witness_id'] in linked))
        self.assertFalse(any(w['independent_reproduction'] for w in witnesses))

    def test_every_negative_is_retained_with_zero_success_credit(self):
        negatives = load('x2/retained-negatives.json')['negatives']
        failed = [w for ledger in ledgers() for w in ledger['witnesses'] if w['result'] == 'fail']
        expected = {n for w in failed for n in w['retained_negative_ids']}
        self.assertEqual(expected, {n['negative_id'] for n in negatives})
        self.assertEqual(len(negatives), len(expected))
        self.assertTrue(all(n['retained'] and n['success_credit'] == 0 for n in negatives))

    def test_open_gaps_and_exact_actions_remain_unexecuted(self):
        register = load('x2/open-and-exact-register.json')
        self.assertEqual(len(register['open_gaps']), 6)
        self.assertEqual(len(register['exact_gates']), 80)
        self.assertTrue(all(r['outcome'] == 'open_gap' and not r['closed'] for r in register['open_gaps']))
        self.assertTrue(all(r['outcome'] == 'exact_gate' and not r['executed'] for r in register['exact_gates']))
        self.assertFalse(register['successor_activation_authorized'])
        self.assertTrue(register['hold_for_hamish'])

    def test_exactly_three_packages_and_dialect_boundaries(self):
        review = load('x2/packages/review.json')
        smoke = load('x2/packages/smoke.json')
        self.assertEqual((review['direct_count'], review['dependency_closure_count']), (3, 3))
        self.assertTrue(all(p['artifact_hash_matches'] and p['wheel_compatible'] for p in review['packages']))
        self.assertEqual(len(smoke['membership_checks']), 51)
        self.assertTrue(smoke['passed'] and smoke['lark_explicit_ambiguity_seen'])
        self.assertFalse(smoke['general_grammar_equivalence'] or smoke['packages_are_independent_reproduction'])
        self.assertFalse(smoke['ordered_choice_counterexample']['tatsu_accepted'])
        self.assertFalse(smoke['ordered_choice_counterexample']['parsy_accepted'])

    def test_skill_runner_counts_and_local_core_parity(self):
        promotion = load('x2/tool-promotion.json')
        self.assertEqual((promotion['skills_promoted'], promotion['runners_promoted'], promotion['shared_dependencies_promoted']), (10, 5, 1))
        self.assertEqual(len(promotion['official_validations']), 20)
        self.assertTrue(all(row['exit_code'] == 0 for row in promotion['official_validations']))
        self.assertEqual(len(load('x2/cli-smoke-results.json')['smokes']), 190)
        core = (ROOT / 'x2/code/ghc_family_cfg_core.py').read_bytes()
        for path in (ROOT / 'x2/skills').glob('*/scripts/ghc_family_cfg_core.py'):
            self.assertEqual(path.read_bytes(), core)

    def test_card_hashes_and_exact_preceding_tier_parent(self):
        index = load('x2/deck/deck-index.json')
        cards = [load('x2/deck/cards/' + identifier + '.json') for identifier in index['order']]
        self.assertEqual(len(cards), 450)
        by_id = {c['card_id']: c for c in cards}
        self.assertEqual(len(by_id), len(cards))
        self.assertEqual(Counter(c['tier'] for c in cards), {1: 1, 2: 3, 3: 4, 4: 442})
        for card in cards:
            identifier = card['card_id']
            payload = {key: value for key, value in card.items() if key != 'card_id'}
            self.assertEqual(identifier, 'ghc-card-' + digest(payload))
            self.assertIn(card['outcome'], ['completed', 'represented', 'open_gap', 'exact_gate'])
            if card['tier'] == 1:
                self.assertEqual(card['parent_ids'], [])
            else:
                self.assertEqual(len(card['parent_ids']), 1)
                self.assertEqual(by_id[card['parent_ids'][0]]['tier'], card['tier'] - 1)

    def test_deck_manifest_covers_every_other_file_exactly(self):
        deck = ROOT / 'x2/deck'
        manifest = load('x2/deck/card-manifest.json')
        actual = {p.relative_to(deck).as_posix() for p in deck.rglob('*') if p.is_file() and p.name != 'card-manifest.json'}
        self.assertEqual(actual, {r['path'] for r in manifest['files']})
        for row in manifest['files']:
            raw = (deck / row['path']).read_bytes()
            self.assertEqual(len(raw), row['bytes'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'])

    def test_cards_cover_all_proposals_and_every_method(self):
        index = load('x2/deck/deck-index.json')
        cards = [load('x2/deck/cards/' + identifier + '.json') for identifier in index['order']]
        self.assertEqual({c['content']['proposal_id'] for c in cards if c['card_type'] == 'proposal_task'},
                         {r['proposal_id'] for r in load('x1/new-proposals.json')['proposals']})
        self.assertEqual({c['content']['method_id'] for c in cards if c['card_type'] == 'method_task'},
                         {m['method_id'] for ledger in ledgers() for m in ledger['methods']})
        stable = load('x2/deck/stable-prefix.json')['card_ids']
        volatile = load('x2/deck/volatile-index.json')['card_ids']
        self.assertEqual(stable + volatile, index['order'])

    def test_html_structure_and_local_links_without_conformance_claim(self):
        class Reader(HTMLParser):
            def __init__(self):
                super().__init__()
                self.tags = Counter()
                self.links = []
            def handle_starttag(self, tag, attrs):
                self.tags[tag] += 1
                if tag == 'a':
                    self.links.append(dict(attrs).get('href'))
        reader = Reader()
        reader.feed((ROOT / 'x2/deck/accessible-report.html').read_text())
        for tag in ['html', 'title', 'main', 'caption', 'thead', 'tbody']:
            self.assertEqual(reader.tags[tag], 1)
        self.assertEqual(reader.tags['tr'], 451)
        for link in reader.links:
            if not link.startswith('#'):
                self.assertTrue((ROOT / 'x2/deck' / link).is_file())


if __name__ == '__main__':
    unittest.main()
