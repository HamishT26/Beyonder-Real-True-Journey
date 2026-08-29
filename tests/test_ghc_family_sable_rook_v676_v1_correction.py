from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / "v676-v1"
CORRECTION = PHASE / "correction"
SOURCE = "0f330a562377a90c8c8eb31515a0ff02551fbdbf"
X1 = "18c4e98ead5d81875c1ffaf7cb2238c34d9b5407"
EVIDENCE = "bb04bce8a0f4b3f6d50d839b1ee237da817e369f"
SEALED_FINAL = "e75ca31a34c8569eee5b603fec2ab96a4ac1f77e"


def load(name: str): return json.loads((CORRECTION/name).read_text(encoding="utf-8"))


class SableRookV676V1CorrectionTests(unittest.TestCase):
    def test_failed_canonical_is_retained(self) -> None:
        row=load("failed-canonical-receipts.json")
        self.assertEqual(row["status"],"FAILED_ZERO_CANONICAL_SUCCESS_CREDIT")
        self.assertEqual(row["head"],SEALED_FINAL)
        self.assertEqual(len(row["failure_receipt_sha256"]),64)
        self.assertEqual(len(row["latch_receipt_sha256"]),64)
        self.assertFalse(row["repository_mutation"])
        self.assertFalse(row["task_contact"])

    def test_additive_counts(self) -> None:
        truth=load("terminal-correction.json")
        self.assertEqual((truth["effective_negatives"],truth["methods"],truth["failed_witnesses"],truth["bounded_passing_witnesses"]),(41660,30750,13321,18118))
        self.assertEqual((truth["open_gaps"],truth["exact_gates"]),(349,341))
        self.assertEqual(truth["terminal_verdict"],"NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["route_state"],"PREPARED_NOT_SENT")

    def test_method_flow_failure_and_recovery_are_distinct(self) -> None:
        flow=load("method-flow-correction.json")
        self.assertEqual(flow["failure"]["success_credit"],0)
        self.assertTrue(flow["failure"]["retained"])
        self.assertEqual(flow["recovery"]["state"],"bounded_passing_dependency_preflight")
        self.assertFalse(flow["recovery"]["old_head_replay"])
        self.assertFalse(flow["failure_erasure"])

    def test_process_local_import_root_is_bound(self) -> None:
        path=ROOT/"scripts"/"ghc_family_sable_rook_v676_v1_final_validator.py"
        text=path.read_text(encoding="utf-8")
        self.assertIn("sys.path.insert(0, str(REPO))",text)
        code="import sys;from pathlib import Path;root=Path.cwd();sys.path.insert(0,str(root));import tests.test_ghc_family_sable_rook_v676_v1_x1;print('ok')"
        result=subprocess.run([sys.executable,"-X","utf8","-c",code],cwd=ROOT,capture_output=True,text=True,encoding="utf-8")
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_history_candidate_or_correction(self) -> None:
        head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True,encoding="utf-8").strip()
        self.assertEqual(subprocess.check_output(["git","rev-parse",f"{SEALED_FINAL}^"],cwd=ROOT,text=True,encoding="utf-8").strip(),EVIDENCE)
        if head!=SEALED_FINAL:
            self.assertEqual(subprocess.check_output(["git","rev-parse","HEAD^"],cwd=ROOT,text=True,encoding="utf-8").strip(),SEALED_FINAL)
            self.assertEqual(int(subprocess.check_output(["git","rev-list","--count",f"{SOURCE}..HEAD"],cwd=ROOT,text=True,encoding="utf-8")),4)
            self.assertEqual(subprocess.check_output(["git","rev-list","--merges",f"{SOURCE}..HEAD"],cwd=ROOT,text=True,encoding="utf-8").splitlines(),[])

    def test_route_is_still_held(self) -> None:
        route=load("route-plan.json")
        self.assertEqual(route["state"],"PREPARED_NOT_SENT")
        self.assertFalse(route["old_head_replay_permitted"])
        self.assertFalse(route["message_sent"])

    def test_correction_receipts_when_present(self) -> None:
        base=PHASE/"validation"
        path=base/"correction-owner-manifest.json"
        if not path.exists(): self.skipTest("correction staged review not generated")
        owner=json.loads(path.read_text(encoding="utf-8")); delta=json.loads((base/"correction-delta-manifest.json").read_text(encoding="utf-8")); review=json.loads((base/"correction-staged-review.json").read_text(encoding="utf-8"))
        self.assertEqual(owner["entry_count"]+len(owner["declared_self_exclusions"]),owner["owner_path_count"])
        self.assertEqual(delta["entry_count"],review["delta_entries"])
        self.assertEqual(review["state"],"VALID_EXACT_CORRECTION_STAGED_REVIEW")
        self.assertEqual(review["confirmed_privacy_hits"],0)

    def test_all_correction_json_strict(self) -> None:
        for path in CORRECTION.glob("*.json"): json.loads(path.read_text(encoding="utf-8"))

    def test_diff_hygiene(self) -> None:
        result=subprocess.run(["git","diff","--check"],cwd=ROOT,capture_output=True,text=True,encoding="utf-8")
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)


if __name__=="__main__": unittest.main()
