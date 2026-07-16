from __future__ import annotations

import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_v647_v2_definitions import PROPOSALS, RUNNER_TITLES, SKILL_SPECS  # noqa: E402
from ghc_family_v647_v2_runtime import SURFACES  # noqa: E402


PHASE = ROOT / "docs" / "orin-thale" / "v647-v2"
SOURCE_FINAL = "c3025ff0d5c062ece7977b4df7f1a34db7d08afe"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V647V2EvidenceTests(unittest.TestCase):
    def test_x1_remains_ancestral_and_separate(self) -> None:
        current = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
        commits = subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-list", "--reverse", f"{SOURCE_FINAL}..{current}"], text=True
        ).splitlines()
        self.assertGreaterEqual(len(commits), 1)
        x1 = commits[0]
        for relative in (
            "docs/orin-thale/v647-v2/x2-proposal-ledger.json",
            "docs/orin-thale/v647-v2/evidence-receipt.json",
            "docs/orin-thale/v647-v2/closeout-receipt.json",
        ):
            probe = subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{x1}:{relative}"], capture_output=True)
            self.assertNotEqual(probe.returncode, 0, relative)

    def test_exact_outcome_vocabulary_and_distribution(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        counts = Counter(row["outcome"] for row in ledger["rows"])
        self.assertEqual(counts, Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}))
        self.assertEqual({row["proposal_id"] for row in ledger["rows"]}, {row["proposal_id"] for row in PROPOSALS})

    def test_all_core_surfaces_and_mutations(self) -> None:
        total = 0
        for proposal_id, spec in SURFACES.items():
            contract = load(spec["contract"])
            mutations = load(spec["mutations"])
            self.assertTrue(contract["positive_pass"], proposal_id)
            self.assertEqual(mutations["count"], 7, proposal_id)
            self.assertEqual(mutations["rejected"], 7, proposal_id)
            self.assertTrue(all(row["retained"] and not row["completion_credit"] for row in mutations["rows"]))
            total += mutations["rejected"]
        self.assertEqual(total, 70)

    def test_gmut_zero_row_and_formal_boundaries(self) -> None:
        bv = load("gmut/bv-master-equation-obligations.json")["positive_fixture"]
        self.assertFalse(bv["quantum_master_equation_proved"])
        self.assertFalse(bv["anomaly_freedom_proved"])
        kids = load("empirical/kids1000-study-contract.json")["positive_fixture"]
        for key in ("downloads", "catalogue_rows", "covariance_rows", "likelihood_calls", "posterior_samples", "parameter_constraints", "empirical_claims"):
            self.assertEqual(kids[key], 0, key)

    def test_thos_freed_id_and_authority_boundaries(self) -> None:
        thos = load("thos/rail-possession-contract.json")["positive_fixture"]
        self.assertEqual((thos["real_workers"], thos["real_infrastructure"], thos["real_possessions"], thos["real_movements"]), (0, 0, 0, 0))
        webauthn = load("freed-id/webauthn-context-profile.json")["positive_fixture"]
        self.assertFalse(webauthn["real_account"])
        self.assertFalse(webauthn["real_key"])
        self.assertFalse(webauthn["production"])
        authority = load("cbr/rail-authority-reservation.json")["positive_fixture"]
        self.assertTrue(all(value == "reserved" for key, value in authority.items() if key != "case_data"))
        self.assertEqual(authority["case_data"], "none")

    def test_tool_accessibility_and_domain_boundaries(self) -> None:
        oci = load("tooling/oci-layer-contract.json")["positive_fixture"]
        self.assertFalse(oci["real_image_pulled"])
        self.assertFalse(oci["host_filesystem_touched"])
        access = load("accessibility/reversible-action-contract.json")["positive_fixture"]
        self.assertTrue(access["manual_evaluation_reserved"])
        thermo = load("thermo-psyche/ruppeiner-contract.json")["positive_fixture"]
        self.assertFalse(thermo["psyche_conversion"])
        bayes = load("stage20/bayesian-model-comparison-contract.json")["positive_fixture"]
        self.assertFalse(bayes["stage20_ready"])

    def test_portfolio_skill_runner_and_negative_arithmetic(self) -> None:
        portfolio = load("approval-packets/x2-portfolio-execution.json")
        candidates = load("prototypes/x2-candidate-execution.json")
        skills = load("skills/skill-build-receipt.json")
        runners = load("tooling/runner-execution.json")
        cleanup = load("maintenance/x2-clean-refine-ledger.json")
        negatives = load("retained-negative-register.json")
        self.assertEqual((portfolio["count"], candidates["count"], skills["count"], len(RUNNER_TITLES), cleanup["count"]), (30, 20, 20, 10, 30))
        self.assertEqual((skills["quick_validated"], skills["smoke_used"]), (len(SKILL_SPECS), len(SKILL_SPECS)))
        self.assertEqual(runners["built_count"], 10)
        self.assertEqual(
            negatives["effective_total"],
            negatives["inherited_effective"] + negatives["x1_operational"] + negatives["preregistered_synthetic"] + negatives["x2_operational"],
        )

    def test_static_report_has_qualified_structure(self) -> None:
        report = (PHASE / "deliverables" / "v647-v2-static-report.html").read_text(encoding="utf-8")
        for token in ("Skip to main evidence", "<main", "<caption>", 'scope="col"', "Manual", "affected-user", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(token, report)


if __name__ == "__main__":
    unittest.main()
