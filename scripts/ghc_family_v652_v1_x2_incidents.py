#!/usr/bin/env python3
"""Append-only Sable v652-v1 x2 operational incident records."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import ghc_family_v652_v1_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
LEDGER = ROOT / "method-flow/method-flow-ledger.json"
RUNNER = Path.home() / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"

INCIDENTS = [
    {
        "negative_id": "V6521-X2-N01",
        "method_id": "V6521-M03",
        "category": "powershell_foreach_pipeline_recurrence",
        "failed": "A runner-collision preflight repeated the known Windows PowerShell statement-level foreach pipeline parser fault before any probe or mutation ran.",
        "recovery": "Materialize the per-runner collision rows in an array and pipe only the completed array.",
        "passing": "The corrected bounded collision inventory returned one row per proposed family-current runner.",
        "recurrence_guard": "Apply the existing M03 array-before-pipeline rule to every statement-level foreach wrapper.",
    },
    {
        "negative_id": "V6521-X2-N02",
        "method_id": "V6521-M07",
        "category": "combined_status_file_probe_timeout",
        "failed": "A combined read-only branch-status and file-discovery wrapper timed out after returning the branch and two expected untracked closeout paths; it made no repository or external mutation.",
        "recovery": "Split large-worktree discovery into exact-path probes with a bounded timeout and materialize results before serialization.",
        "passing": "The corrected exact-path probe returned the five requested path and length rows inside the bounded timeout.",
        "recurrence_guard": "Prefer exact literal paths over recursive discovery in the large inherited checkout and keep status and file probes independently attributable.",
    },
    {
        "negative_id": "V6521-X2-N03",
        "method_id": "V6521-M03",
        "category": "powershell_foreach_pipeline_recurrence",
        "failed": "The first exact-path recovery wrapper again piped directly from a statement-level foreach block and failed in the Windows PowerShell parser before any command executed.",
        "recovery": "Accumulate exact-path rows in an array, then pipe the completed array to JSON serialization.",
        "passing": "The corrected array-first exact-path probe returned all five requested rows and identified both absent validator files.",
        "recurrence_guard": "Apply M03 before issuing any statement-level foreach wrapper, including recovery probes.",
    },
    {
        "negative_id": "V6521-X2-N04",
        "method_id": "V6521-M08",
        "category": "powershell_unicode_search_literal_parser_fault",
        "failed": "A source-audit wrapper embedded mojibake characters in a double-quoted PowerShell search pattern and failed at parse time before ripgrep launched.",
        "recovery": "Search count-bearing fields with an ASCII-only exact pattern and inspect Unicode content separately.",
        "passing": "The ASCII-only exact search returned every 8,013 and 8013 closeout occurrence without mutation.",
        "recurrence_guard": "Keep shell-level diagnostic patterns ASCII-only when Unicode content can be audited by code point in the target process.",
    },
    {
        "negative_id": "V6521-X2-N05",
        "method_id": "V6521-M08",
        "category": "powershell_unicode_python_literal_parser_recurrence",
        "failed": "A Python source-audit wrapper repeated the Unicode shell-literal parser fault before Python launched.",
        "recovery": "Express the Unicode audit with numeric code points in an ASCII-only Python command.",
        "passing": "The numeric code-point audit found five em dashes, eight a-macron characters, and zero Latin a-circumflex mojibake markers in the closeout builder.",
        "recurrence_guard": "Pass numeric Unicode code points through PowerShell rather than embedding suspect glyph sequences in nested command literals.",
    },
    {
        "negative_id": "V6521-X2-N06",
        "method_id": "V6521-M09",
        "category": "overbroad_x1_immutability_assertion",
        "failed": "The first staged closeout validator passed every other check but rejected eight append-only lifecycle surfaces because it treated every x1 path as immutable proposal content.",
        "recovery": "Preserve exact x1 Git-blob manifest validation while allowlisting only the declared append-only Method Flow, reflection, and family-index lifecycle surfaces.",
        "passing": "The corrected validator distinguishes the eight declared lifecycle updates from unexpected x1-frozen changes and retains the original failed receipt.",
        "recurrence_guard": "Bind x1 immutability to frozen proposal and preregistration content while naming every intentionally append-only lifecycle surface exactly.",
    },
    {
        "negative_id": "V6521-X2-N07",
        "method_id": "V6521-M10",
        "category": "historical_x1_self_state_in_final_selection",
        "failed": "The first exact-final aggregate stopped before a receipt because it ran an immutable x1 self-state test against the advanced x2 tree; an isolated diagnostic confirmed the expected surfaces-directory assertion with six of seven x1 tests passing.",
        "recovery": "Validate the x1 commit through its exact Git-blob manifest and ancestry, and run only the eligible x2 and closeout tests on the advanced final tree.",
        "passing": "The corrected advanced-tree diagnostic selection passed all fifteen eligible x2 and closeout tests without rerunning the successful final aggregate, which had not yet occurred.",
        "recurrence_guard": "Bind historical self-state tests to their immutable commit and exclude them explicitly from advanced-tree selections while preserving manifest and ancestry proof.",
    },
    {
        "negative_id": "V6521-X2-N08",
        "method_id": "V6521-M11",
        "category": "stale_correction_commit_count_assertion",
        "failed": "The first correction precommit validator stopped when the closeout test still required three phase commits; an isolated diagnostic confirmed that single stale assertion with six of seven tests passing.",
        "recovery": "Update the advanced lifecycle test to the additive four-commit correction contract while retaining the immutable closeout receipt and original three-commit history at its exact revision.",
        "passing": "The corrected closeout test selection passed all seven tests against the four-commit correction candidate.",
        "recurrence_guard": "Refresh lifecycle-count assertions whenever an authorized additive recovery commit changes the advanced-head contract, without rewriting historical commit-local receipts.",
    },
    {
        "negative_id": "V6521-X2-N09",
        "method_id": "V6521-M12",
        "category": "bulk_patch_context_mismatch",
        "failed": "A bulk additive correction patch failed closed because one expected builder context did not match the live source; apply_patch changed no file.",
        "recovery": "Read the exact live spans and apply smaller path-specific patches with minimal context.",
        "passing": "The split exact-context patches updated the correction truth, tests, validators, and failure receipts without touching unrelated files.",
        "recurrence_guard": "After a generated file has already advanced, inspect the live span and prefer small exact patches over a multi-file patch with copied stale context.",
    },
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def invoke(*args: str) -> None:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    subprocess.run([sys.executable, str(RUNNER), *args], cwd=REPO, env=env, check=True)


def record(stage: str) -> None:
    item = INCIDENTS[0]
    suffix = "fail2" if stage == "fail" else "pass2"
    witness_id = "V6521-M03-WFAIL2" if stage == "fail" else "V6521-M03-WPASS2"
    path = ROOT / f"method-flow/records/v6521-m03-{suffix}.json"
    payload = {
        "witness_id": witness_id,
        "method_id": item["method_id"],
        "procedure": "Retain the recurrence before retry." if stage == "fail" else "Apply the existing array-before-pipeline recovery to the isolated probe.",
        "scope": "Sable v652-v1 x2 runner-collision preflight",
        "expected": "The recurrence fails before execution." if stage == "fail" else "The corrected bounded probe returns exact collision rows.",
        "observed": item["failed"] if stage == "fail" else item["passing"],
        "result": "fail" if stage == "fail" else "pass",
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": [item["negative_id"]],
        "boundary": "The recovery validates only the isolated wrapper rule and never erases the recurrence.",
    }
    write_json(path, payload)
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if not any(row["witness_id"] == witness_id for row in ledger["witnesses"]):
        invoke("witness", "--ledger", str(LEDGER), "--witness-file", str(path))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["fail", "pass"])
    args = parser.parse_args()
    record(args.stage)


if __name__ == "__main__":
    main()
