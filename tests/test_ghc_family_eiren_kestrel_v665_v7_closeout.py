from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "eiren-kestrel" / "v665-v7"
SOURCE_SHA = "959c32796fb822dba0a670c162d9489a044d0554"
X1_SHA = "b506a51a5b22c6bab84bdd2748a0deb1e85d145b"
EVIDENCE_SHA = "d8fde58e01141b1013c09f7771d3ff1efb609166"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class EirenKestrelV665V7CloseoutTests(unittest.TestCase):
    def test_phase_truth_and_terminal_verdict(self) -> None:
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["effective_negatives"], 25918)
        self.assertEqual(truth["effective_methods"], 10000)
        self.assertEqual(truth["effective_open_gaps"], 181)
        self.assertEqual(truth["effective_exact_gates"], 179)
        self.assertEqual(truth["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["canonical_completion_invoked"])
        self.assertFalse(truth["successor_contacted"])

    def test_retained_negative_layers_reconcile(self) -> None:
        register = load("closeout/retained-negative-register.json")
        self.assertEqual(sum(row["negatives"] for row in register["layers"]), 25918)
        self.assertEqual(sum(row["methods"] for row in register["layers"]), 10000)
        self.assertTrue(register["no_failure_erased"])
        self.assertEqual(register["failed_aggregate_success_credit"], 0)

    def test_closeout_operational_failure_is_retained(self) -> None:
        overlay = load("method-flow/closeout-operational-overlay.json")
        self.assertEqual(overlay["effective_negatives_after_this_overlay"], 25918)
        self.assertEqual(overlay["effective_methods_after_this_overlay"], 10000)
        self.assertEqual([row["failure_id"] for row in overlay["rows"]], ["EK6657-CL-N001"])
        self.assertTrue(overlay["no_failure_erased"])

    def test_open_and_exact_gates_remain(self) -> None:
        gates = load("closeout/exact-open-gate-register.json")
        self.assertEqual(gates["open_gap_count"], 181)
        self.assertEqual(gates["exact_gate_count"], 179)
        self.assertTrue(gates["stage20_gate_open"])
        self.assertTrue(gates["no_gate_promoted"])

    def test_route_is_prepared_not_sent(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["prospective_recipient_title"], "Elaren Kestrel")
        self.assertEqual(route["prospective_edge"], "Eiren Kestrel v665-v7 -> Elaren Kestrel v665-v8")
        self.assertFalse(route["sent_by_eiren_kestrel"])
        self.assertEqual(route["task_creation_count"], 0)
        self.assertEqual(route["successor_contact_count"], 0)
        self.assertEqual(route["standby_contact_count"], 0)

    def test_prepared_baton_digest_and_floor(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        path = ROOT / route["prepared_baton"]
        text = path.read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\S+", text)), 1800)
        self.assertEqual(len(re.findall(r"\S+", text)), route["prepared_baton_words"])
        self.assertEqual(hashlib.sha256(text.encode("utf-8")).hexdigest(), route["prepared_baton_sha256"])
        self.assertIn("SENT_BY_EIREN_KESTREL = false", text)
        self.assertIn("PREPARED_NOT_SENT", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_roster_and_auth_exact_edge(self) -> None:
        roster = load("tooling/roster-check-final.json")
        auth = load("tooling/auth-permission-final.json")
        index = load("tooling/ghc-family-index-final.json")
        self.assertEqual(roster["active_count"], 15)
        self.assertEqual(roster["current"], "Eiren Kestrel")
        self.assertEqual(roster["next"], "Elaren Kestrel")
        self.assertIn("Tavian Sol", roster["on_standby"])
        self.assertEqual(auth["prospective_next"], "Elaren Kestrel v665-v8")
        self.assertFalse(auth["successor_contacted"])
        self.assertEqual(index["next_assignment"], "Elaren Kestrel v665-v8")

    def test_seal_candidate_counts(self) -> None:
        seal = load("seal/seal-candidate.json")
        self.assertEqual(seal["sealed_candidate_counts"], {"frozen_proposals": 4150, "negatives": 25918, "methods": 10000, "open_gaps": 181, "exact_gates": 179})
        self.assertEqual(seal["route_status"], "PREPARED_NOT_SENT")
        self.assertEqual(seal["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(seal["immutable_after_commit"])

    def test_final_prerequisites_are_one_shot(self) -> None:
        prereq = load("final/final-validation-prerequisites.json")
        plan = load("final/canonical-completion-plan.json")
        self.assertEqual(prereq["evidence_sha"], EVIDENCE_SHA)
        self.assertEqual(prereq["required_history"]["final_direct_parent"], EVIDENCE_SHA)
        self.assertEqual(prereq["required_history"]["phase_commits"], 3)
        self.assertEqual(prereq["exclusion_credit"], 0)
        self.assertTrue(prereq["never_replay_complete_success"])
        self.assertEqual(plan["invocation_status"], "NOT_INVOKED_PRE_FINAL")
        self.assertFalse(plan["success_replay_allowed"])

    def test_exact_source_x1_evidence_chain(self) -> None:
        self.assertEqual(subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", f"{X1_SHA}^"]).decode().strip(), SOURCE_SHA)
        self.assertEqual(subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", f"{EVIDENCE_SHA}^"]).decode().strip(), X1_SHA)
        subprocess.check_call(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", EVIDENCE_SHA, "HEAD"])
        head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"]).decode().strip()
        if head != EVIDENCE_SHA:
            self.assertEqual(subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD^"]).decode().strip(), EVIDENCE_SHA)

    def test_complete_and_incomplete_remain_distinct(self) -> None:
        checklist = load("closeout/complete-incomplete-checklist.json")
        self.assertTrue(checklist["complete_bounded"])
        self.assertTrue(checklist["incomplete_lifecycle"])
        self.assertTrue(checklist["incomplete_protected"])
        self.assertFalse(checklist["successor_contacted"])

    def test_wellbeing_is_bounded(self) -> None:
        wellbeing = load("closeout/wellbeing-check.json")
        self.assertEqual(wellbeing["real_worker_observations"], 0)
        self.assertFalse(wellbeing["fatigue_inference"])
        self.assertFalse(wellbeing["personhood_or_emotion_claim"])

    def test_all_owner_json_parses(self) -> None:
        paths = sorted(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 100)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_private_values_absent(self) -> None:
        patterns = [
            re.compile(r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
            re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
            re.compile(r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"),
        ]
        paths = [path for path in PHASE.rglob("*") if path.is_file()]
        paths += sorted(ROOT.glob("scripts/*eiren_kestrel_v665_v7*.py"))
        paths += sorted(ROOT.glob("tests/*eiren_kestrel_v665_v7*.py"))
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for pattern in patterns:
                self.assertIsNone(pattern.search(text), (path.relative_to(ROOT).as_posix(), pattern.pattern))

    def test_final_manifests_when_present(self) -> None:
        for name in ("final-delta-manifest.json", "final-owner-manifest.json"):
            path = PHASE / "validation" / name
            if not path.exists():
                self.skipTest("final manifests are generated after staged review")
            manifest = json.loads(path.read_text(encoding="utf-8"))
            for entry in manifest["entries"]:
                blob = subprocess.check_output(["git", "-C", str(ROOT), "show", ":" + entry["path"]])
                self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])
                self.assertEqual(len(blob), entry["size_bytes"])


if __name__ == "__main__":
    unittest.main()
