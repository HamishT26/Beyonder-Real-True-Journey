import hashlib
import json
import pathlib
import unittest

X2 = pathlib.Path(__file__).resolve().parent
REPO = X2.parents[3]
DECK = X2 / "deck"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


class Deck(unittest.TestCase):
    def test_manifest_paths(self):
        for row in read(DECK / "card-manifest.json")["entries"]:
            self.assertTrue((REPO / row["path"]).is_file(), row["path"])

    def test_manifest_fixity(self):
        for row in read(DECK / "card-manifest.json")["entries"]:
            data = (REPO / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()), (row["bytes"], row["sha256"]))

    def test_parent_tiers(self):
        cards = {card["card_id"]: card for card in map(read, (DECK / "cards").glob("*.json"))}
        for card in cards.values():
            self.assertEqual(len(card["parent_ids"]), 0 if card["tier"] == 1 else 1)
            for parent in card["parent_ids"]:
                self.assertEqual(cards[parent]["tier"], card["tier"] - 1)

    def test_content_addresses(self):
        for path in (DECK / "cards").glob("*.json"):
            card = read(path)
            identifier = card.pop("card_id")
            data = (json.dumps(card, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
            self.assertEqual(identifier, "ghc-card-" + hashlib.sha256(data).hexdigest())

    def test_method_and_negative_binding(self):
        ledger = read(X2 / "method-flow.json")
        methods = {row["method_id"]: row for row in ledger["methods"]}
        negatives = set(read(X2 / "retained-negatives.json")["negative_ids"])
        for witness in ledger["witnesses"]:
            self.assertIn(witness["witness_id"], methods[witness["method_id"]]["validation_witness_ids"])
            if witness["result"] == "fail":
                self.assertTrue(witness["retained_negative_ids"])
                self.assertTrue(set(witness["retained_negative_ids"]) <= negatives)

    def test_card_and_method_counts(self):
        self.assertEqual(read(DECK / "deck-index.json")["card_count"], 265)
        validation = read(X2 / "method-flow-validation.json")
        self.assertTrue(validation["valid"])
        self.assertEqual(validation["method_count"], 57)
        self.assertEqual(validation["witness_count"], 604)


if __name__ == "__main__":
    unittest.main()
