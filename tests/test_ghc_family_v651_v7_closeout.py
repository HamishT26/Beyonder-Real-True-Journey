from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/vesper-arlen/v651-v7"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class VesperV651V7CloseoutTests(unittest.TestCase):
    def test_final_truth(self) -> None:
        truth = load("truth/final-phase-truth.json")
        self.assertEqual(
            truth["outcomes"],
            {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(
            (
                truth["effective_negatives"],
                truth["effective_open_gaps"],
                truth["effective_exact_gates"],
                truth["terminal_verdict"],
            ),
            (7454, 59, 60, "NOT_READY_FOR_STAGE_20"),
        )
        self.assertEqual(
            (
                truth["real_data_rows"],
                truth["participants"],
                truth["real_keys_or_tokens"],
                truth["authority_decisions"],
                truth["production_actions"],
                truth["future_cli_seats_named"],
                truth["future_cli_seats_launched"],
            ),
            (0, 0, 0, 0, 0, 0, 0),
        )
        self.assertFalse(truth["independent_reproduction"])

    def test_negative_and_gate_continuity(self) -> None:
        negative = load("truth/final-retained-negative-register.json")
        gates = load("gates/final-gate-register.json")
        self.assertEqual(
            (
                negative["inherited_effective"],
                negative["x1_operational"],
                negative["x2_operational"],
                negative["synthetic_rejecting_mutations"],
                negative["closeout_operational"],
                negative["effective_total"],
                negative["failures_erased"],
            ),
            (7338, 5, 9, 100, 2, 7454, 0),
        )
        self.assertEqual(
            (
                gates["effective_open_gaps"],
                gates["effective_exact_gates"],
                gates["silently_closed"],
            ),
            (59, 60, 0),
        )

    def test_route_is_prepared_not_sent(self) -> None:
        route = load("route/terminal-route.json")
        self.assertEqual(route["status"], "PREPARED_NOT_SENT")
        self.assertEqual(route["candidate_from_advisory_plan"], "Ilyra Fen")
        self.assertFalse(route["candidate_is_live_authority"])
        self.assertFalse(route["exact_successor_confirmed"])
        self.assertEqual(
            (
                route["future_cli_placeholders"],
                route["future_cli_names_chosen"],
                route["future_cli_launches"],
                route["task_messages_sent"],
            ),
            (8, 0, 0, 0),
        )

    def test_baton_contract(self) -> None:
        path = ROOT / "handoffs/authorized-successor-v651-v8-pending-confirmation.md"
        text = path.read_text(encoding="utf-8")
        words = len(text.split())
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        self.assertIn("PREPARED_NOT_SENT_AT_COMMIT = true", text)
        self.assertIn("candidate routing is not authority", text)

    def test_overview_contract(self) -> None:
        text = (ROOT / "overview/final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 3000)
        self.assertLessEqual(len(text.split()), 100000)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_accessible_static_report(self) -> None:
        text = (ROOT / "reports/final-accessible-static-report.html").read_text(
            encoding="utf-8"
        ).casefold()
        for token in (
            '<html lang="en">',
            "<main>",
            '<nav aria-label=',
            "<caption>",
            '<th scope="col">',
            "manual keyboard",
            "affected-user",
            "not_ready_for_stage_20",
        ):
            self.assertIn(token, text)
        self.assertNotIn("<script", text)

    def test_manifests_are_self_excluding(self) -> None:
        manifest = load("validation/final-staged-manifest.json")
        review = load("validation/final-staged-review.json")
        owner = load("validation/owner-manifest.json")
        self.assertEqual(
            manifest["entry_count"] + len(manifest["self_exclusions"]),
            review["intended_path_count"],
        )
        self.assertEqual(len(manifest["self_exclusions"]), 5)
        self.assertEqual(owner["entry_count"] + len(owner["self_exclusions"]), owner["owner_file_count"])
        self.assertTrue(owner["below_threshold"])
        self.assertLess(owner["owner_file_count"], 2000)

    def test_source_ledger_is_current_and_bounded(self) -> None:
        sources = load("sources/final-source-ledger.json")
        self.assertEqual(len(sources["sources"]), 5)
        self.assertTrue(all(row["url"].startswith("https://") for row in sources["sources"]))
        self.assertTrue(sources["source_use_is_not_outcome_credit"])

    def test_environment_was_verify_only(self) -> None:
        receipt = load("environment/final-version-receipt.json")
        self.assertTrue(receipt["verified_only"])
        for key in (
            "desktop_updated",
            "elevation",
            "host_security_weakened",
            "windows_feature_changed",
            "unrelated_software_installed",
            "rebooted",
            "sandbox_session_launched",
        ):
            self.assertFalse(receipt[key])

    def test_closeout_adds_no_result(self) -> None:
        closeout = load("closeout/closeout-receipt.json")
        seal = load("seal/seal-receipt.json")
        self.assertFalse(closeout["closeout_adds_scientific_result"])
        self.assertEqual(closeout["route"], "PREPARED_NOT_SENT")
        self.assertEqual(closeout["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(seal["combined_closeout_and_seal"])
        self.assertFalse(seal["full_repository_suite_run"])
        self.assertTrue(seal["canonical_success_may_be_credited_once"])

    def test_closeout_method_flow(self) -> None:
        flow = load("method-flow/closeout-summary.json")
        self.assertEqual(
            (
                flow["methods"],
                flow["failed_witnesses"],
                flow["passing_witnesses"],
                flow["preferred_methods"],
            ),
            (2, 2, 2, 2),
        )
        self.assertFalse(flow["failure_erased"])


if __name__ == "__main__":
    unittest.main()
