import hashlib
import json
import pathlib
import unittest

X = pathlib.Path(__file__).resolve().parent
REPO = X.parents[3]
D = X / 'deck'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

class Deck(unittest.TestCase):
    def test_paths(self):
        for row in read(D / 'card-manifest.json')['entries']:
            self.assertTrue((REPO / row['path']).is_file(), row['path'])

    def test_fixity(self):
        for row in read(D / 'card-manifest.json')['entries']:
            data = (REPO / row['path']).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()), (row['bytes'], row['sha256']))

    def test_parent_tiers(self):
        cards = {c['card_id']: c for c in map(read, (D / 'cards').glob('*.json'))}
        for card in cards.values():
            self.assertEqual(len(card['parent_ids']), 0 if card['tier'] == 1 else 1)
            for parent in card['parent_ids']:
                self.assertEqual(cards[parent]['tier'], card['tier'] - 1)

    def test_content_addresses(self):
        for p in (D / 'cards').glob('*.json'):
            card = read(p)
            ident = card.pop('card_id')
            data = (json.dumps(card, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
            self.assertEqual(ident, 'ghc-card-' + hashlib.sha256(data).hexdigest())

    def test_failed_manifest_retained(self):
        self.assertFalse(read(X / 'manifest-probe-v1.json')['valid'])
        self.assertTrue(read(X / 'manifest-probe-v2.json')['valid'])
        self.assertEqual(read(X / 'retained-card-manifest-v1.json')['status'], 'INVALID_RETAINED_ZERO_CREDIT')

    def test_method_witness_binding(self):
        ledger = read(X / 'method-flow.json')
        by_id = {m['method_id']: m for m in ledger['methods']}
        for witness in ledger['witnesses']:
            self.assertIn(witness['witness_id'], by_id[witness['method_id']]['validation_witness_ids'])
        self.assertIn('TER6888-X2-N001', read(X / 'retained-negatives.json')['negative_ids'])

if __name__ == '__main__':
    unittest.main()
