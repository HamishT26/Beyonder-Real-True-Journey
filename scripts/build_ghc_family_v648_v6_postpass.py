#!/usr/bin/env python3
"""Seal v648-v6 post-pass receipts without rerunning tests or canonical privacy."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v648-v6"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def status_paths() -> list[str]:
    paths = set(filter(None, git("diff", "--name-only").splitlines()))
    paths.update(filter(None, git("diff", "--cached", "--name-only").splitlines()))
    paths.update(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return sorted(path.replace("\\", "/") for path in paths)


def incremental_privacy(paths: list[str]) -> dict:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    confirmed = []
    parsed = 0
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if path.suffix.casefold() == ".json":
            json.loads(text)
            parsed += 1
        for pattern_class, pattern in patterns.items():
            if pattern.search(text) and relative != "docs/orin-thale/v648-v6/validation/final-staged-privacy.json":
                confirmed.append({"path":relative,"pattern_class":pattern_class})
    return {"pattern_classes":sorted(patterns),"confirmed_hits":confirmed,"json_parses":parsed}


def build() -> None:
    canonical = load("validation/canonical-pass-result.json")
    if canonical["successful_canonical_pass_number"] != 1 or canonical["tests_passed"] != 67:
        raise RuntimeError("successful canonical pass receipt is absent or invalid")
    plan = load("validation/final-validation-plan.json")
    plan["successful_passes_used"] = 1
    plan["canonical_pass_receipt"] = "validation/canonical-pass-result.json"
    plan["replay_used"] = False
    write_json("validation/final-validation-plan.json", plan)
    closeout = load("closeout/closeout-candidate.json")
    closeout["canonical_successful_pass_used"] = True
    closeout["canonical_pass_receipt"] = "validation/canonical-pass-result.json"
    write_json("closeout/closeout-candidate.json", closeout)
    method = load("method-flow/method-flow-summary.json")
    x2_method = load("method-flow/x2-method-flow-summary.json")
    write_json("method-flow/final-method-flow-receipt.json", {
        "schema":"ghc.family.v648-v6.method-flow.final.v1",
        "methods":method["counts"]["methods"] + x2_method["counts"]["methods"],
        "failed_witnesses":method["counts"]["witness_results"]["fail"] + x2_method["counts"]["witness_results"]["fail"],
        "passing_witnesses":method["counts"]["witness_results"]["pass"] + x2_method["counts"]["witness_results"]["pass"],
        "preferred_methods":method["counts"]["states"]["preferred"] + x2_method["counts"]["states"]["preferred"],
        "failure_erased":False,
        "independent_reproduction":False,
    })
    write_json("validation/final-validation-receipt.json", {
        "schema":"ghc.family.v648-v6.final-validation-receipt.v1",
        **canonical,
        "receipt_sealed_after_pass_without_test_rerun":True,
        "canonical_privacy_rerun_after_pass":False,
        "terminal_route":"PREPARED_NOT_SENT",
    })
    write_json("closeout/closeout-receipt.json", {
        "schema":"ghc.family.v648-v6.closeout-receipt.v1",
        "x1_commit":"3f6a64d239bdde1c38fea166db5eff0f2f3e1d89",
        "evidence_commit":git("rev-parse","HEAD"),
        "expected_total_phase_commits":3,
        "expected_merge_count":0,
        "expected_final_parent_count":1,
        "canonical_passes_used":1,
        "replays_used":0,
        "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    })
    write_json("closeout/seal-receipt.json", {
        "schema":"ghc.family.v648-v6.seal-receipt.v1",
        "seal_candidate_parent":git("rev-parse","HEAD"),
        "exact_final_head":"VERIFIED_EXTERNALLY_AFTER_COMMIT",
        "manifest_domain":"exact_git_blob_with_declared_self_exclusions",
        "remote_equality":"REQUIRED_AFTER_COMMIT",
        "terminal_route":"PREPARED_NOT_SENT",
    })
    write_json("environment/final-file-footprint-receipt.json", {
        "schema":"ghc.family.v648-v6.file-footprint.final.v1",
        "inherited_tracked_baseline":37396,
        "owner_generated_files":sum(path.is_file() for path in PHASE.rglob("*")),
        "rotation_threshold":15000,
        "rotation_triggered":False,
    })
    write_json("orchestration/terminal-route-receipt.json", {
        "schema":"ghc.family.v648-v6.terminal-route.v1",
        "target_title":"Tamar Vey",
        "target_phase":"v648-v7",
        "messages_sent":0,
        "state":"PREPARED_NOT_SENT",
        "send_gate":"exact final head clean, pushed, remote-equal, manifest-verified",
    })
    exclusions = [
        "docs/orin-thale/v648-v6/validation/final-staged-manifest.json",
        "docs/orin-thale/v648-v6/validation/final-staged-privacy.json",
        "docs/orin-thale/v648-v6/validation/final-staged-review.json",
    ]
    paths = [path for path in status_paths() if path not in exclusions]
    scan = incremental_privacy(paths + exclusions)
    if scan["confirmed_hits"]:
        raise RuntimeError(f"incremental privacy hits: {scan['confirmed_hits']}")
    entries = [
        {"path":relative,"git_blob":git("hash-object",f"--path={relative}",relative),"bytes":(ROOT/relative).stat().st_size}
        for relative in paths
        if (ROOT / relative).is_file()
    ]
    write_json("validation/final-staged-privacy.json", {
        "schema":"ghc.family.v648-v6.final-incremental-privacy.v1",
        "scanned_path_count":len(paths)+len(exclusions),
        "pattern_classes":scan["pattern_classes"],
        "confirmed_hit_count":0,
        "confirmed_hits":[],
        "canonical_scan_rerun":False,
        "boundary":"Incremental post-pass surface only; canonical privacy was not rerun and zero hits is not complete assurance.",
    })
    write_json("validation/final-staged-manifest.json", {
        "schema":"ghc.family.v648-v6.final-manifest.v1",
        "hash_domain":"git_hash_object_path_filtered_blob",
        "checkout_bytes_domain":"working_tree_after_checkout_filters",
        "entries":entries,
        "entry_count":len(entries),
        "self_exclusions":exclusions,
        "canonical_tests_rerun":False,
    })
    write_json("validation/final-staged-review.json", {
        "schema":"ghc.family.v648-v6.final-staged-review.v1",
        "intended_path_count":len(entries)+len(exclusions),
        "manifest_entry_count":len(entries),
        "self_exclusion_count":len(exclusions),
        "incremental_json_parses":scan["json_parses"],
        "privacy_confirmed_hits":0,
        "canonical_tests_rerun":False,
        "passed":True,
    })


if __name__ == "__main__":
    build()
