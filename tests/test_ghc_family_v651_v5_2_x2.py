import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v651-v5-2-remaster"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def load_runner():
    path = REPO / "scripts/ghc_family_meta_tool_box.py"
    spec = importlib.util.spec_from_file_location("ghc_family_meta_tool_box_under_test", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class EirenV651V5RemasterX2Tests(unittest.TestCase):
    def test_core_outcomes(self):
        packet = load("outcomes/core-outcomes.json")
        self.assertEqual(packet["counts"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(len(packet["outcomes"]), 30)

    def test_portfolios_are_resolved_within_bounds(self):
        packet = load("portfolios/x2-portfolio-outcomes.json")
        self.assertEqual(packet["safe_now"]["completed"], 40)
        self.assertEqual(packet["candidate"]["bounded_completed"], 30)
        self.assertEqual(packet["skills"]["built"], 20)
        self.assertEqual(packet["runners"]["built"], 10)
        self.assertEqual(packet["clean_fix_refine"]["completed"], 40)
        self.assertFalse(packet["unsafe_work_manufactured"])

    def test_skill_packages_are_customized(self):
        for row in load("tooling/skill-build-receipt.json")["skills"]:
            text = (REPO / row["path"]).read_text(encoding="utf-8")
            self.assertNotIn("TODO", text)
            self.assertIn("## Boundaries", text)

    def test_family_current_runners_exist(self):
        for row in load("tooling/runner-build-receipt.json")["runners"]:
            self.assertTrue((REPO / row["path"]).is_file())

    def test_meta_toolbox_validator_rejects_one_hundred_mutations(self):
        module = load_runner()
        baseline = {"schema": module.SCHEMA, "cards": [{"card_id": "skill:one", "name": "one", "kind": "skill", "source_path": "docs/one/SKILL.md", "sha256": "0" * 64, "status": "current", "evidence_state": "observed", "owner_scope": "owner", "triggers": ["one"], "caller_paths": [], "rollback": "remove additive selection", "protected_gates": ["failure_retention"]}]}
        plan = load("validation/preregistered-mutations.json")
        rejected = 0
        for row in plan["mutations"]:
            candidate = json.loads(json.dumps(baseline))
            category = row["category"]
            if category == "missing_required_field":
                candidate["cards"][0].pop("kind")
            elif category == "absolute_private_path":
                candidate["cards"][0]["source_path"] = "C:/private/item"
            elif category == "unknown_enum":
                candidate["cards"][0]["status"] = "magical"
            elif category == "missing_rollback":
                candidate["cards"][0]["rollback"] = ""
            else:
                candidate["cards"].append(json.loads(json.dumps(candidate["cards"][0])))
            rejected += not module.validate(candidate)["valid"]
        self.assertEqual(rejected, 100)

    def test_gmut_is_typed_and_empirically_abstaining(self):
        coefficient = load("gmut/coefficient-identifiability-board.json")
        self.assertFalse(coefficient["identifiable_from_current_packet"])
        self.assertFalse(coefficient["theory_of_everything_claim"])
        adapter = load("gmut/spherex-qr2-zero-row-adapter.json")
        self.assertEqual(adapter["real_rows"], 0)
        self.assertEqual(adapter["outcome"], "open_gap")

    def test_thos_and_freed_id_are_synthetic(self):
        thos = load("thos/digital-preservation-handover.json")
        self.assertTrue(thos["synthetic"])
        self.assertEqual(thos["real_workers"], 0)
        identity = load("freed-id/tool-attestation-profile.json")
        self.assertEqual(identity["real_keys"], 0)
        self.assertFalse(identity["production"])

    def test_authority_and_stage20_remain_gated(self):
        authority = load("cbr/tool-lifecycle-authority-matrix.json")
        self.assertEqual(authority["state"], "exact_gate")
        self.assertEqual(authority["decisions_made"], 0)
        stage = load("truth/stage20-evidence-gradient-board.json")
        self.assertEqual(stage["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_accessible_report_reserves_manual_review(self):
        text = (ROOT / "reports/accessible-static-report.html").read_text(encoding="utf-8")
        for token in ('<html lang="en">', '<nav aria-label=', '<caption>', 'Manual keyboard'):
            self.assertIn(token, text)

    def test_no_cli_sibling_was_spawned(self):
        self.assertEqual(load("truth/evidence-phase-truth.json")["cli_siblings_spawned"], 0)


if __name__ == "__main__":
    unittest.main()
