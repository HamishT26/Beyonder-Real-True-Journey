import hashlib
import json
import pathlib
import re
import unittest

FINAL = pathlib.Path(__file__).resolve().parent
PHASE = FINAL.parent


def read(relative):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class Closeout(unittest.TestCase):
    def test_outcomes(self):
        self.assertEqual(read("final/phase-truth.json")["outcomes"], {"completed": 170, "represented": 17, "open_gap": 3, "exact_gate": 10})

    def test_effective_counts(self):
        self.assertEqual(read("final/phase-truth.json")["effective_counts"], {"proposals": 17230, "negatives": 86292, "methods": 94237, "failed_witnesses": 57265, "passing_witnesses": 86430, "open_gaps": 771, "exact_gates": 805})

    def test_method_flow_retention(self):
        summary = read("final/method-flow-summary.json")
        self.assertEqual((summary["effective_phase_methods"], summary["effective_phase_failed_witnesses"], summary["effective_phase_passing_witnesses"]), (61, 486, 126))
        self.assertTrue(summary["no_failure_erasure"])

    def test_negative_and_gate_counts(self):
        self.assertEqual(read("final/retained-negative-register.json")["phase_negative_count"], 486)
        gates = read("final/open-exact-gate-register.json")
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (771, 805))

    def test_package_evidence(self):
        summary = read("x2/package-smoke-summary.json")
        self.assertEqual((summary["comparison_count"], summary["comparison_passes"], summary["adverse_count"], summary["adverse_rejections"]), (420, 420, 3, 3))
        self.assertEqual(read("x2/package-transaction.json")["listed_vulnerability_count"], 0)

    def test_tool_and_deck_evidence(self):
        promotion = read("x2/tool-promotion.json")
        self.assertEqual((promotion["skill_count"], promotion["runner_count"], len(promotion["smokes"])), (10, 5, 190))
        self.assertTrue(all(row["predicate_pass"] for row in promotion["smokes"]))
        self.assertEqual(read("x2/deck/deck-index.json")["card_count"], 265)

    def test_lifecycle_policy(self):
        lifecycle = read("final/lifecycle.json")
        self.assertEqual((lifecycle["source"], lifecycle["x1"], lifecycle["x2"]), ("9968e60dab5393ed2629ed978c8d1128bb63a0b9", "3635cfeeb48b27540452eabf104a5ad3f491b82c", "a53b2ffc7020ad8d485878392793de7bd2722a7c"))
        policy = read("final/canonical-policy.json")
        self.assertEqual((len(policy["test_modules"]), policy["expected_total_tests"], policy["canonical_replay_limit"]), (4, 52, 0))

    def test_route_is_prepared_only(self):
        route = read("final/terminal-route.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual((route["send_count"], route["creation_count"]), (0, 0))
        self.assertEqual((route["prospective_target"], route["prospective_phase"], route["next_after_target"]), ("future-sibling-15-self-chosen", "v689-v2", "Eiren Kestrel v689-v3"))

    def test_baton_integrity(self):
        index = read("final/baton-index.json")
        baton = (PHASE.parents[2] / index["path"]).read_bytes()
        text = baton.decode("utf-8")
        self.assertEqual(hashlib.sha256(baton).hexdigest(), index["sha256"])
        self.assertEqual(len(re.findall(r"^## Module ", text, re.M)), 13)
        self.assertTrue(10000 <= len(text.split()) <= 100000)
        self.assertTrue(text.rstrip().endswith("EOF CAELEN MORROW v689-v1 BATON."))

    def test_boundaries_and_incomplete_work(self):
        checklist = read("final/complete-incomplete-checklist.json")
        self.assertEqual(checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(checklist["no_incomplete_safe_prototype_hidden"])
        overview = (FINAL / "integrated-overview.md").read_text(encoding="utf-8")
        self.assertIn("Same-owner", overview)
        self.assertIn("Maori concepts remain under Maori authority", overview)


if __name__ == "__main__":
    unittest.main()
