#!/usr/bin/env python3
"""Full bounded evidence tests for Eiren Kestrel v645-v3."""

from __future__ import annotations

import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v645-v3"


def load(rel: str):
    return json.loads((PHASE / rel).read_text(encoding="utf-8-sig"))


class V645V3EvidenceTests(unittest.TestCase):
    def test_proposal_outcomes(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(ledger["proposal_count"], 10)
        self.assertEqual(Counter(item["disposition"] for item in ledger["outcomes"]), Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}))

    def test_approval_execution_boundaries(self) -> None:
        ledger = load("approval-packets/x2-execution-ledger.json")
        self.assertEqual(ledger["counts"], {"safe_completed": 15, "candidate_prototypes_completed": 10, "successor_seed_only": 25, "exact_unexecuted": 10, "blocked_unexecuted": 5})
        self.assertTrue(all(item["state"] == "unexecuted_exact_gate" for item in ledger["exact_packets"]))
        self.assertTrue(all(item["state"] == "unexecuted_blocked" for item in ledger["blocked_packets"]))

    def test_all_principal_runner_receipts(self) -> None:
        for rel in ["validation/portfolio-validation.json", "sandbox/sandbox-blueprint-validation.json", "physics/eft-quotient-validation.json", "freed-id/deferred-issuance-validation.json", "stage20/anytime-evidence-validation.json", "security/git-acceleration-runner-receipt.json", "method-flow/runner-validation.json"]:
            self.assertTrue(load(rel)["valid"], rel)

    def test_skill_pack_is_ten_valid_nonplaceholder_skills(self) -> None:
        skills = sorted((PHASE / "prototypes/skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 10)
        for skill in skills:
            text = skill.read_text(encoding="utf-8")
            self.assertNotIn("TODO", text)
            self.assertRegex(text, r"(?s)^---\nname: [a-z0-9-]+\ndescription: .+?\n---")
            metadata = skill.parent / "agents/openai.yaml"
            self.assertTrue(metadata.is_file())
            self.assertIn(f"${skill.parent.name}", metadata.read_text(encoding="utf-8"))

    def test_sandbox_truth(self) -> None:
        lint = load("sandbox/sandbox-blueprint-validation.json")
        probe = load("environment/host-sandbox-version-probe.json")
        self.assertEqual((lint["template_count"], lint["valid_count"]), (6, 6))
        self.assertFalse(probe["windows_sandbox_executable_available"])
        self.assertFalse(probe["windows_sandbox_cli_available"])
        self.assertFalse(probe["sandbox_launched"])
        self.assertFalse(probe["host_changed"])

    def test_gmut_empirical_nonpromotion(self) -> None:
        readiness = load("empirical/slr-adapter-readiness.json")
        boundary = load("physics/eft-nonpromotion-boundary.json")
        self.assertEqual(readiness["real_rows"], 0)
        self.assertFalse(readiness["fit_permitted"])
        self.assertFalse(boundary["empirical_gmut_confirmation"])
        self.assertFalse(boundary["theory_of_everything_claim"])

    def test_thos_remains_proxy(self) -> None:
        reservation = load("thos/real-observatory-reservation.json")
        self.assertTrue(reservation["synthetic_proxy_only"])
        self.assertEqual(reservation["real_workers"], 0)
        self.assertFalse(reservation["effectiveness_claim"])

    def test_freed_id_remains_synthetic(self) -> None:
        reservation = load("freed-id/production-issuance-reservation.json")
        self.assertEqual(reservation["real_keys"], 0)
        self.assertEqual(reservation["real_credentials"], 0)
        self.assertFalse(reservation["production_complete"])

    def test_cbr_and_maori_authority_reserved(self) -> None:
        text = (PHASE / "cbr/geodetic-authority-reservation.md").read_text(encoding="utf-8")
        self.assertIn("Maori concepts remain under Maori authority", text)
        cases = load("cbr/cadastral-refusal-cases.json")["cases"]
        self.assertTrue(all(item["decision"] == "refuse_without_exact_authority" for item in cases))

    def test_jarzynski_fixture_and_nonconversion(self) -> None:
        fixture = load("thermo-psyche/jarzynski-fixtures.json")
        boundary = load("thermo-psyche/psyche-nonconversion-boundary.json")
        self.assertTrue(fixture["algebraic_fixture_pass"])
        self.assertLess(fixture["absolute_error"], 1e-12)
        self.assertFalse(boundary["dimensional_conversion_permitted"])
        self.assertFalse(boundary["clinical_claim"])

    def test_stage20_rejected(self) -> None:
        truth = load("phase-truth.json")
        board = load("stage20/terminal-evidence-board.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(board["promotion_permitted"])

    def test_method_flow_structural_counts(self) -> None:
        ledger = load("method-flow/method-flow-state.json")
        method_count = len(ledger["methods"])
        self.assertGreaterEqual(method_count, 17)
        self.assertEqual(ledger["counts"]["methods"], method_count)
        self.assertEqual(ledger["counts"]["witness_results"], {"pass": method_count, "fail": method_count})
        self.assertEqual(ledger["counts"]["states"]["preferred"], method_count)
        self.assertEqual(len({item["method_id"] for item in ledger["methods"]}), method_count)

    def test_negatives_and_gates(self) -> None:
        negatives = load("retained-negative-register.json")
        gates = load("exact-open-gate-register.json")
        self.assertEqual(negatives["negative_count"], 2003)
        new_ids = [item["negative_id"] for item in negatives["x1_operational"] + negatives["x2_operational"] + negatives["synthetic_negatives"]]
        self.assertEqual(len(new_ids), len(set(new_ids)))
        self.assertEqual((gates["open_gap_count"], gates["exact_gate_count"]), (5, 6))
        self.assertTrue(gates["none_silently_closed"])

    def test_static_report_structure(self) -> None:
        text = (PHASE / "deliverables/v645-v3-static-report.html").read_text(encoding="utf-8")
        for token in ("<title>", 'href="#main"', '<main id="main"', ":focus-visible", "<h1>", "<h2", "<table>", "<caption>", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(token, text)
        self.assertNotRegex(text.lower(), r"http-equiv\s*=\s*['\"]?refresh")
        reservation = load("validation/manual-accessibility-reservation.json")
        self.assertFalse(reservation["complete_accessibility_claim"])

    def test_overview_word_cap_and_minimum(self) -> None:
        words = (PHASE / "v645-v3-integrated-overview.md").read_text(encoding="utf-8").split()
        self.assertGreaterEqual(len(words), 1500)
        self.assertLessEqual(len(words), 6000)

    def test_no_raw_private_material_in_phase_text(self) -> None:
        patterns = [
            re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
            re.compile(r"[A-Za-z]:\\(?:Users|GHC-Archives)\\"),
            re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
            re.compile(r"\bsk-[A-Za-z0-9_-]{12,}"),
            re.compile("source_" + "thread_id", re.I),
        ]
        hits = []
        for path in PHASE.rglob("*"):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError:
                continue
            for pattern in patterns:
                if pattern.search(text):
                    hits.append((path.relative_to(PHASE).as_posix(), pattern.pattern))
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
