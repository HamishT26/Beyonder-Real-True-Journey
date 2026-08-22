from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "vesper-arlen" / "v666-v2"
X1_SHA = "d327d6ca9f16dc6cf16f555aea1c9a41fc8f4969"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class VesperArlenV666V2X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = load("x2/proposal-ledger.json")
        cls.freeze = load("x1/proposal-freeze.json")
        cls.portfolio = load("x2/portfolio-execution.json")
        cls.flow = load("method-flow/x2-method-flow.json")
        cls.overlay = load("method-flow/x2-operational-overlay.json")
        cls.skill_catalog = load("x2/skill-catalog.json")
        cls.runner_catalog = load("x2/runner-catalog.json")

    def test_x1_commit_is_direct_parent_basis(self) -> None:
        self.assertEqual(self.ledger["x1_sha"], X1_SHA)
        self.assertEqual(
            subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"]).decode().strip(),
            X1_SHA,
        )

    def test_x1_bytes_are_unchanged(self) -> None:
        paths = [
            "docs/vesper-arlen/v666-v2/x1",
            "docs/vesper-arlen/v666-v2/identity",
            "docs/vesper-arlen/v666-v2/provenance",
            "docs/vesper-arlen/v666-v2/wellbeing/x1-wellbeing-check.json",
            "docs/vesper-arlen/v666-v2/validation/x1-content-manifest.json",
            "docs/vesper-arlen/v666-v2/validation/x1-staged-review.json",
        ]
        output = subprocess.check_output(
            ["git", "-C", str(ROOT), "diff", "--name-only", X1_SHA, "--", *paths]
        ).decode()
        self.assertEqual(output.strip(), "")

    def test_exact_core_outcomes(self) -> None:
        self.assertEqual(self.ledger["proposal_count"], 20)
        self.assertEqual(
            self.ledger["outcome_counts"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )
        allowed = {"completed", "represented", "open_gap", "exact_gate"}
        self.assertLessEqual({row["observed_disposition"] for row in self.ledger["rows"]}, allowed)

    def test_contract_and_mutation_totals(self) -> None:
        self.assertEqual(self.ledger["bounded_positive_count"], 20)
        self.assertEqual(self.ledger["mutation_count"], 100)
        self.assertEqual(self.ledger["rejected_mutation_count"], 100)
        self.assertEqual(self.ledger["accepted_mutation_count"], 0)
        proposal_dirs = sorted((PHASE / "x2" / "proposals").iterdir())
        self.assertEqual(len(proposal_dirs), 20)
        self.assertEqual(sum((path / "contract.json").is_file() for path in proposal_dirs), 20)
        self.assertEqual(sum((path / "mutation-results.json").is_file() for path in proposal_dirs), 20)
        self.assertEqual(sum((path / "bounded-receipt.json").is_file() for path in proposal_dirs), 20)

    def test_each_contract_keeps_zero_action_boundary(self) -> None:
        for path in sorted((PHASE / "x2" / "proposals").glob("*/contract.json")):
            contract = json.loads(path.read_text(encoding="utf-8"))
            fixture = contract["bounded_positive_fixture"]
            self.assertTrue(fixture["synthetic_only"])
            self.assertEqual(fixture["real_data_rows"], 0)
            self.assertEqual(fixture["participant_count"], 0)
            self.assertEqual(fixture["network_calls"], 0)
            self.assertEqual(fixture["external_actions"], [])
            self.assertEqual(fixture["authority_status"], "none")
            self.assertFalse(fixture["production"])
            self.assertFalse(fixture["deployment"])

    def test_each_mutation_is_retained_and_rejected(self) -> None:
        rows = []
        for path in sorted((PHASE / "x2" / "proposals").glob("*/mutation-results.json")):
            result = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(result["all_rejected"])
            self.assertEqual(result["mutation_count"], 5)
            self.assertEqual(result["rejected_mutation_count"], 5)
            self.assertEqual(result["accepted_mutation_count"], 0)
            rows.extend(result["mutations"])
        self.assertEqual(len(rows), 100)
        self.assertTrue(all(row["retained_negative"] and row["aggregate_credit"] == 0 for row in rows))

    def test_preregistered_and_observed_dispositions_match(self) -> None:
        expected = {row["proposal_id"]: row["expected_disposition"] for row in self.freeze["new_proposals"]}
        observed = {row["proposal_id"]: row["observed_disposition"] for row in self.ledger["rows"]}
        self.assertEqual(observed, expected)

    def test_source_adapter_remains_open_gap(self) -> None:
        adapter = load("x2/source-adapter-zero-call.json")
        self.assertEqual(adapter["outcome"], "open_gap")
        self.assertEqual(adapter["network_calls"], 0)
        self.assertEqual(adapter["real_rows"], 0)
        self.assertFalse(adapter["current_live_adapter_executed"])
        self.assertTrue(adapter["authority_nonconversion"])

    def test_trinity_representations_remain_bounded(self) -> None:
        trinity = load("x2/trinity-representations.json")
        self.assertEqual(trinity["freed_id"]["status"], "represented")
        self.assertEqual(trinity["freed_id"]["real_keys"], 0)
        self.assertEqual(trinity["thos"]["status"], "represented")
        self.assertEqual(trinity["thos"]["participants"], 0)
        self.assertEqual(trinity["gmut"]["observations"], 0)
        self.assertEqual(trinity["gmut"]["predictions"], 0)
        self.assertEqual(trinity["cbr"]["status"], "exact_gate")
        self.assertEqual(trinity["cbr"]["approvals"], 0)

    def test_phase_local_skills_validated_and_not_installed(self) -> None:
        self.assertEqual(self.skill_catalog["skill_count"], 10)
        self.assertFalse(self.skill_catalog["globally_installed"])
        for row in self.skill_catalog["skills"]:
            self.assertEqual(row["status"], "built_validated_smoke_used_owner_local")
            path = ROOT / row["path"]
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\nname: "))
            self.assertIn("\ndescription: ", text)
            self.assertIn("globally installed", text)

    def test_family_runners_validated_and_additive(self) -> None:
        self.assertEqual(self.runner_catalog["runner_count"], 10)
        self.assertFalse(self.runner_catalog["global_installation"])
        for row in self.runner_catalog["runners"]:
            self.assertEqual(row["status"], "built_validated_smoke_used_owner_local")
            self.assertTrue((ROOT / row["path"]).is_file())
            self.assertTrue(Path(row["path"]).name.startswith("ghc_family_"))

    def test_tooling_smoke_receipt(self) -> None:
        receipt = load("x2/tooling-smoke-receipt.json")
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["skill_quick_validation"], {
            **receipt["skill_quick_validation"],
            "passed": 10,
            "failed": 0,
        })
        self.assertEqual(receipt["runner_smoke"]["passed"], 10)
        self.assertEqual(receipt["runner_smoke"]["failed"], 0)
        self.assertFalse(receipt["globally_installed"])

    def test_portfolio_execution_and_unexecuted_gates(self) -> None:
        self.assertEqual(len(self.portfolio["safe_now"]), 30)
        self.assertEqual(len(self.portfolio["bounded_candidates"]), 15)
        self.assertEqual(len(self.portfolio["exact_approval_packets"]), 10)
        self.assertEqual(len(self.portfolio["blocked_packets"]), 5)
        self.assertEqual(len(self.portfolio["phase_local_skills"]), 10)
        self.assertEqual(len(self.portfolio["family_current_runners"]), 10)
        self.assertEqual(len(self.portfolio["clean_fix_refine"]), 30)
        self.assertTrue(all(row["x2_status"] == "unexecuted_exact_gate" for row in self.portfolio["exact_approval_packets"]))
        self.assertTrue(all(row["x2_status"] == "unexecuted_blocked" for row in self.portfolio["blocked_packets"]))

    def test_method_flow_counts(self) -> None:
        self.assertEqual(self.flow["proposal_method_count"], 120)
        self.assertEqual(self.flow["portfolio_method_count"], 95)
        self.assertEqual(self.flow["new_x2_methods"], 215)
        self.assertEqual(len(self.flow["methods"]), 215)
        self.assertEqual(self.flow["new_rejecting_mutation_negatives"], 100)
        self.assertEqual(self.flow["effective_negatives_before_later_operational_overlays"], 26275)
        self.assertEqual(self.flow["effective_methods_before_later_operational_overlays"], 10702)

    def test_x2_operational_failures_are_exactly_retained(self) -> None:
        self.assertEqual(self.overlay["new_operational_negative_count"], 2)
        self.assertEqual(self.overlay["new_operational_method_count"], 2)
        self.assertEqual(self.overlay["effective_negatives_after_this_overlay"], 26277)
        self.assertEqual(self.overlay["effective_methods_after_this_overlay"], 10704)
        self.assertEqual(len(self.overlay["rows"]), 2)
        self.assertTrue(all(row["aggregate_credit"] == 0 for row in self.overlay["rows"]))

    def test_bounded_runner_sequence_passes_without_becoming_canonical(self) -> None:
        receipt = load("x2/runtime-validation-receipt.json")
        self.assertEqual(receipt["aggregate_credit"], 1)
        self.assertFalse(receipt["canonical_aggregate"])
        self.assertEqual(receipt["selected_component_count"], 7)
        self.assertEqual(receipt["passed_component_count"], 7)
        self.assertEqual(receipt["failed_component_count"], 0)
        self.assertEqual(receipt["sequence_status"], "PASS_BOUNDED_X2_COMPONENT_SEQUENCE")

    def test_all_owner_json_parses(self) -> None:
        paths = sorted(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 80)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_no_real_rows_participants_network_or_actions(self) -> None:
        for key in ("real_rows", "participants", "network_calls", "external_actions"):
            self.assertEqual(self.ledger[key], 0)
        self.assertEqual(self.portfolio["real_rows"], 0)
        self.assertEqual(self.portfolio["participants"], 0)
        self.assertEqual(self.portfolio["external_writes"], 0)
        self.assertEqual(self.portfolio["destructive_actions"], 0)

    def test_private_values_absent(self) -> None:
        patterns = [
            re.compile("source_" + "thread_id", re.I),
            re.compile("thread" + "Id", re.I),
            re.compile("task" + "Id", re.I),
            re.compile(r"[A-Z]:" + r"\\Users\\", re.I),
            re.compile(r"[A-Z]:" + r"\\GHC-Archives", re.I),
            re.compile("Bearer" + r"\s+[A-Za-z0-9._~-]+", re.I),
        ]
        paths = [path for path in PHASE.rglob("*") if path.is_file()]
        paths += sorted(ROOT.glob("scripts/*v666_v2*.py"))
        paths += sorted(ROOT.glob("tests/*v666_v2*.py"))
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for pattern in patterns:
                self.assertIsNone(pattern.search(text), (path.relative_to(ROOT).as_posix(), pattern.pattern))

    def test_terminal_verdict_and_no_route_artifact(self) -> None:
        self.assertEqual(self.ledger["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse((PHASE / "handoffs").exists())
        self.assertFalse((PHASE / "closeout").exists())
        self.assertFalse((PHASE / "seal").exists())
        self.assertFalse((PHASE / "final").exists())


if __name__ == "__main__":
    unittest.main()
