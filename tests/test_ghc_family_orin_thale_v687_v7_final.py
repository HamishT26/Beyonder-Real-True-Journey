#!/usr/bin/env python3
"""Precommit and exact-final tests for Orin Thale v687-v7."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v687-v7"
FINAL = PHASE / "final"
VALIDATION = PHASE / "validation"
SOURCE = "28dfdf1a3e9a1023f1e83f19fb267e57878b9d0b"
X1 = "7aea73908f8f41ed38473d6e30e5f1bda36588a7"
FIRST_EVIDENCE = "a29be946caf963315a48f73055f0eb1cae85e482"
CORRECTED_EVIDENCE = "7f9d761e54475cf82945ef31e019d043aebde282"


def load(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def norm(path: Path): return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False)
    if result.returncode: raise RuntimeError(result.stderr)
    return result.stdout.strip()


class OrinThaleV687V7FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.truth=load(FINAL/"phase-truth.json"); cls.delta=load(VALIDATION/"final-delta-manifest.json"); cls.owner=load(VALIDATION/"final-owner-manifest.json")

    def test_precommit_parent_is_corrected_evidence(self): self.assertEqual(git("rev-parse","HEAD"),CORRECTED_EVIDENCE)
    def test_ancestry_before_final(self):
        self.assertEqual(git("rev-parse",f"{CORRECTED_EVIDENCE}^"),FIRST_EVIDENCE); self.assertEqual(git("rev-parse",f"{FIRST_EVIDENCE}^"),X1); self.assertEqual(git("rev-parse",f"{X1}^"),SOURCE)
    def test_truth_counts_and_outcomes(self):
        self.assertEqual(self.truth["outcomes"],{"completed":125,"represented":39,"open_gap":20,"exact_gate":16})
        self.assertEqual(self.truth["effective_counts"],{"negatives":82024,"methods":93197,"failed_witnesses":52872,"passing_witnesses":81998,"open_gaps":732,"exact_gates":711,"proposals":15230})
    def test_failures_retained(self):
        r=load(FINAL/"retained-negative-register.json"); self.assertEqual(r["erased_or_promoted"],0); self.assertEqual(r["orin_groups"]["startup_failures"],15); self.assertEqual(r["orin_groups"]["changed_output_candidates"],1000); self.assertEqual(r["orin_groups"]["root_runner_omission"],1); self.assertEqual(r["orin_groups"]["final_closeout_failures"],3)
    def test_holds_and_boundaries(self):
        c=load(FINAL/"complete-incomplete.json"); self.assertEqual(c["held_unexecuted"],{"exact_packets":50,"blocked_packets":30}); self.assertEqual(self.truth["terminal_verdict"],"NOT_READY_FOR_STAGE_20")
    def test_baton_index_and_eof(self):
        i=load(FINAL/"baton-index.json"); p=ROOT/i["path"]; b=norm(p); self.assertEqual(hashlib.sha256(b).hexdigest(),i["sha256"]); self.assertEqual(len(p.read_text(encoding="utf-8").split()),i["words"]); self.assertEqual(i["modules"],13); self.assertTrue(p.read_text(encoding="utf-8").rstrip().endswith(i["eof"])); self.assertGreaterEqual(i["words"],10000); self.assertLessEqual(i["words"],100000)
    def test_route_prepared_not_sent(self):
        r=load(FINAL/"terminal-route-plan.json"); self.assertEqual(r["recipient_placeholder"],"future-sibling-10-self-chosen"); self.assertEqual(r["recipient_phase"],"v687-v8"); self.assertEqual(r["following_owner"],"Liora Venn"); self.assertFalse(r["precontacted"]); self.assertEqual(r["task_creation_count"],0); self.assertEqual(r["message_count"],0)
    def test_content_seal(self):
        s=load(FINAL/"content-seal.json"); self.assertEqual(s["target_count"],len(s["targets"]));
        for e in s["targets"]: self.assertEqual(hashlib.sha256(norm(ROOT/e["path"])).hexdigest(),e["sha256"])
    def test_final_delta_manifest(self):
        actual=set(self.delta["declared_self_exclusions"])
        for e in self.delta["entries"]:
            b=norm(ROOT/e["path"]); self.assertEqual(len(b),e["bytes_normalized_lf"],e["path"]); self.assertEqual(hashlib.sha256(b).hexdigest(),e["sha256_normalized_lf"],e["path"]); actual.add(e["path"])
        self.assertEqual(actual,set(load(VALIDATION/"final-staged-review.json")["expected_paths"]))
    def test_final_owner_manifest(self):
        self.assertLess(self.owner["owner_path_count"],2000); self.assertEqual(self.owner["entry_count"],len(self.owner["entries"]));
        for e in self.owner["entries"]: self.assertEqual(hashlib.sha256(norm(ROOT/e["path"])).hexdigest(),e["sha256_normalized_lf"],e["path"])
    def test_privacy_security_json(self):
        self.assertEqual(load(VALIDATION/"final-privacy.json")["confirmed_count"],0); self.assertEqual(load(VALIDATION/"final-security.json")["finding_count"],0); self.assertGreater(load(VALIDATION/"final-json.json")["parsed"],250)
    def test_canonical_and_route_pending(self): self.assertEqual(self.truth["canonical_invocations"],0); self.assertEqual(self.truth["route_state"],"PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED")


if __name__=="__main__": unittest.main()
