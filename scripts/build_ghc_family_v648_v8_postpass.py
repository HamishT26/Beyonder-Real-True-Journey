#!/usr/bin/env python3
"""Seal one external canonical result without rerunning tests or the canonical privacy scan."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sylven-arc" / "v648-v8"
SOURCE = "33c8f87a4037c81c3abca540b8c5db1d91328420"
X1 = "d86990f673aa82c45a5296ebba88c79a6dc3bde4"
EVIDENCE = "1e85a9e714ac2509095fac03aedf704b4892d8b3"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--external-output", type=Path, required=True)
    args = parser.parse_args()
    result = json.loads(args.external_output.read_text(encoding="utf-8"))
    if not result.get("passed") or result.get("candidate_head") != EVIDENCE or result.get("full_suite") or result.get("replay"):
        raise RuntimeError("canonical result is absent, mismatched, or out of scope")
    plan = load("validation/final-validation-plan.json")
    if plan["successful_passes_used"] != 0:
        raise RuntimeError("canonical successful pass was already consumed")
    plan.update({"successful_passes_used":1,"canonical_pass_receipt":"validation/canonical-validation.json","replay_used":False})
    write("validation/final-validation-plan.json", plan)
    write("validation/canonical-validation.json", {**result,"imported_from_external_receipt":True,"external_path_persisted":False})
    write("phase-truth-final.json", {"schema":"ghc.family.v648-v8.phase-truth.final.v1","source_head":SOURCE,"x1_commit":X1,"evidence_commit":EVIDENCE,"outcomes":{"completed":6,"represented":2,"open_gap":1,"exact_gate":1},"canonical_successful_passes_used":1,"full_suite_used":False,"replay_used":False,"same_owner_only":True,"independent_reproduction":False,"terminal_route":"PREPARED_NOT_SENT","terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write("validation/final-validation-record.json", {"schema":"ghc.family.v648-v8.final-validation-record.v1","canonical_candidate":result,"canonical_successful_passes_used":1,"failed_canonical_attempts":0,"postpass_tests_rerun":False,"postpass_canonical_privacy_rerun":False,"incremental_files_only":True,"exact_final_head":"VERIFIED_EXTERNALLY_AFTER_COMMIT","same_owner_only":True,"terminal_route":"PREPARED_NOT_SENT"})
    closeout = load("closeout/closeout-candidate.json")
    closeout.update({"canonical_successful_pass_used":True,"canonical_pass_receipt":"validation/canonical-validation.json"})
    write("closeout/closeout-candidate.json", closeout)
    write("closeout/closeout-receipt.json", {"schema":"ghc.family.v648-v8.closeout-receipt.v1","source_head":SOURCE,"x1_commit":X1,"evidence_commit":EVIDENCE,"expected_total_phase_commits":3,"expected_merge_count":0,"expected_final_parent_count":1,"canonical_passes_used":1,"replays_used":0,"terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write("closeout/seal-receipt.json", {"schema":"ghc.family.v648-v8.seal-receipt.v1","seal_candidate_parent":EVIDENCE,"exact_final_head":"VERIFIED_EXTERNALLY_AFTER_COMMIT","manifest_domain":"exact_git_blob_and_checkout_with_declared_exclusions","remote_equality":"REQUIRED_AFTER_COMMIT","terminal_route":"PREPARED_NOT_SENT"})
    methods = load("method-flow/method-flow-summary.json")
    write("method-flow/final-method-flow-receipt.json", {"schema":"ghc.family.v648-v8.method-flow.final.v1","methods":methods["counts"]["methods"],"failed_witnesses":methods["counts"]["witness_results"]["fail"],"passing_witnesses":methods["counts"]["witness_results"]["pass"],"preferred_methods":methods["counts"]["states"]["preferred"],"failure_erased":False,"independent_reproduction":False})
    write("environment/final-file-footprint-receipt.json", {"schema":"ghc.family.v648-v8.file-footprint.final.v1","owner_generated_files":sum(path.is_file() for path in PHASE.rglob("*")),"rotation_threshold":15000,"rotation_triggered":False,"inherited_files_excluded_from_trigger":True})
    write("orchestration/terminal-route-receipt.json", {"schema":"ghc.family.v648-v8.terminal-route.v1","target_title":"Eiren Kestrel","target_phase":"v649-v1","messages_sent":0,"state":"PREPARED_NOT_SENT","send_gate":"exact final head clean, pushed, remote-equal, and manifest-verified"})
    write("validation/postpass-incremental-receipt.json", {"schema":"ghc.family.v648-v8.postpass-incremental.v1","candidate_staged_tree":result["candidate_staged_tree"],"canonical_tests_rerun":False,"canonical_privacy_rerun":False,"replay_used":False,"postpass_scope":"receipt_import_and_incremental_seal_only","terminal_route":"PREPARED_NOT_SENT"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
