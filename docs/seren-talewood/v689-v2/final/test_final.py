"""Exact final owner checks; synthetic latch fixtures never invoke a canonical."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'final/code'))
import canonical


def load(path):
    return canonical.strict_json((ROOT / path).read_bytes())


def structural_fixture():
    name = 'synthetic/owner-fixture.txt'
    raw = b'bounded synthetic fixture\n'
    oid = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    blobs = {name: {'oid': oid, 'raw': raw}}
    manifest = {'entries': [{'path': name, 'git_oid': oid, 'bytes': len(raw), 'sha256': canonical.sha(raw)}], 'self_exclusions': []}
    return manifest, blobs, {name}


def fixture_observations(directory):
    manifest, blobs, names = structural_fixture()
    canonical.verify_manifest(manifest, blobs, names)
    rows = []
    for mutation in ['wrong_digest', 'missing_entry', 'unexpected_path', 'wrong_byte_count']:
        changed = copy.deepcopy(manifest)
        if mutation == 'wrong_digest':
            changed['entries'][0]['sha256'] = '0' * 64
        elif mutation == 'missing_entry':
            changed['entries'] = []
        elif mutation == 'unexpected_path':
            changed['self_exclusions'] = ['synthetic/undeclared.txt']
        elif mutation == 'wrong_byte_count':
            changed['entries'][0]['bytes'] += 1
        rejected = False
        try:
            canonical.verify_manifest(changed, blobs, names)
        except (AssertionError, KeyError):
            rejected = True
        rows.append({'mutation': mutation, 'fixture': changed, 'rejected': rejected, 'subject_result': 'fail', 'success_credit': 0})
    latch = directory / 'synthetic-fixture-latch.json'
    canonical.write_once(latch, {'synthetic_fixture': True, 'canonical_invocation': False})
    original = latch.read_bytes()
    rejected = False
    try:
        canonical.write_once(latch, {'synthetic_fixture': True, 'replacement': True})
    except FileExistsError:
        rejected = True
    rows.append({'mutation': 'exclusive_latch_reopen', 'rejected': rejected,
                 'original_preserved': latch.read_bytes() == original, 'subject_result': 'fail', 'success_credit': 0})
    return {'valid_fixture_passed': True, 'negative_mutations': rows, 'all_rejected': all(row['rejected'] for row in rows),
            'actual_canonical_invocations': 0, 'independent_reproduction': False}


class FinalOwnerContract(unittest.TestCase):
    def test_manifest_positive_and_five_negative_fixtures(self):
        with tempfile.TemporaryDirectory(prefix='seren-fixture-') as directory:
            result = fixture_observations(Path(directory))
        self.assertTrue(result['valid_fixture_passed'] and result['all_rejected'])
        self.assertEqual(len(result['negative_mutations']), 5)
        self.assertEqual(result['actual_canonical_invocations'], 0)

    def test_final_fixture_receipt_retains_zero_credit(self):
        receipt = load('final/canonical-fixture-results.json')
        self.assertTrue(receipt['valid_fixture_passed'] and receipt['all_rejected'])
        self.assertTrue(all(row['subject_result'] == 'fail' and row['success_credit'] == 0 for row in receipt['negative_mutations']))

    def test_terminal_hold_supersedes_earlier_route(self):
        phase = load('final/phase-truth.json')
        self.assertFalse(phase['successor_activation_authorized'])
        self.assertEqual(phase['successor_contacts'], 0)
        self.assertEqual(phase['terminal_after_valid_canonical'], 'CLOSED_OWNER_SCOPE_HELD_FOR_HAMISH')
        self.assertEqual(phase['terminal_verdict'], 'NOT_READY_FOR_STAGE_20')
        self.assertEqual(load('x1/authority-correction.json')['terminal_route_state_target'], 'CLOSED_OWNER_SCOPE_HELD_FOR_HAMISH')

    def test_all_unique_counts_add_without_source_recredit(self):
        counts = load('final/count-reconciliation.json')
        self.assertEqual(counts['owner_delta'], {'proposals': 200, 'negatives': 621, 'methods': 243,
            'failed_witnesses': 621, 'passing_witnesses': 727, 'open_gaps': 6, 'exact_gates': 80})
        for key, value in counts['owner_delta'].items():
            self.assertEqual(counts['activation_baseline'][key] + value, counts['represented_chain_after'][key])
        self.assertEqual(counts['proposal_outcomes'], {'completed': 190, 'represented': 10})
        self.assertFalse(counts['aggregate_mapping_complete'])

    def test_final_method_and_deck_extension_are_additive(self):
        ledger = load('final/method-flow.json')
        self.assertEqual(len(ledger['methods']), 1)
        self.assertEqual(len(ledger['witnesses']), 6)
        index = load('final/deck/extension-index.json')
        self.assertEqual(index['base_cards'], 450)
        self.assertEqual(index['total_cards'], 451)
        self.assertEqual(len(index['new_card_ids']), 1)
        card = load('final/deck/cards/' + index['new_card_ids'][0] + '.json')
        payload = {key: value for key, value in card.items() if key != 'card_id'}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(',', ':')).encode()).hexdigest()
        self.assertEqual(card['card_id'], 'ghc-card-' + digest)
        parent = load('x2/deck/cards/' + card['parent_ids'][0] + '.json')
        self.assertEqual((parent['tier'], card['tier']), (3, 4))

    def test_baton_thirteen_modules_and_word_budget(self):
        baton = (ROOT / 'handoffs/held-for-hamish-closeout-baton.md').read_text(encoding='utf-8')
        self.assertGreaterEqual(len(baton.split()), 10000)
        self.assertLessEqual(len(baton.split()), 100000)
        self.assertEqual(sum(line.startswith('## Module ') for line in baton.splitlines()), 13)
        self.assertTrue(baton.rstrip().endswith('EOF SEREN TALEWOOD v689-v2 HELD BATON.'))
        self.assertIn('CLOSED_OWNER_SCOPE_HELD_FOR_HAMISH', baton)

    def test_three_page_overview_and_reserved_review(self):
        overview = (ROOT / 'final/overview.html').read_text(encoding='utf-8')
        self.assertEqual(overview.count('class="page"'), 3)
        self.assertIn('break-after:page', overview)
        self.assertIn('manual accessibility review remains open', overview)

    def test_complete_incomplete_checklist_names_remaining_gates(self):
        checklist = load('final/checklist.json')
        self.assertTrue(all(row['outcome'] in ['completed', 'represented', 'open_gap', 'exact_gate'] for row in checklist['items']))
        self.assertEqual(checklist['canonical_at_repository_seal'], 'prepared_not_invoked')
        self.assertEqual(len([r for r in checklist['items'] if r['outcome'] == 'open_gap']), 6)
        self.assertFalse(checklist['successor_contact_authorized'])

    def test_canonical_policy_names_every_lifecycle_module(self):
        policy = load('final/canonical-policy.json')
        self.assertEqual([s['stage'] for s in policy['test_stages']], ['x1', 'x2', 'final'])
        self.assertEqual([s['test_count'] for s in policy['test_stages']], [12, 39, 10])
        self.assertEqual(policy['canonical_invocations'], 1)
        self.assertFalse(policy['replay_authorized'] or policy['source_execution'])
        for stage in policy['test_stages']:
            for module in stage['modules']:
                self.assertEqual(canonical.sha((ROOT / module['relative_path']).read_bytes()), module['sha256'])

    def test_combined_deck_manifest_is_complete_and_exact(self):
        manifest = load('final/deck/complete-card-manifest.json')
        names = {p.relative_to(ROOT).as_posix() for folder in [ROOT / 'x2/deck', ROOT / 'final/deck']
                 for p in folder.rglob('*') if p.is_file() and p.name != 'complete-card-manifest.json'}
        self.assertEqual(names, {r['path'] for r in manifest['files']})
        for row in manifest['files']:
            self.assertEqual(canonical.sha((ROOT / row['path']).read_bytes()), row['sha256'])


if __name__ == '__main__':
    unittest.main()
