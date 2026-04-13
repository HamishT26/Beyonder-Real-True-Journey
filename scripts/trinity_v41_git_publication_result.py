#!/usr/bin/env python3
"""Publish the V41 forward-only Git publication result and refresh git cleanup truth."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v41_common import ROOT, now_iso, read_json, write_json, write_text

RESULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v41-git-publication-result-v1.json"
RESULT_MD = ROOT / "docs" / "trinity-live-traces" / "v41-git-publication-result-v1.md"

RUNTIME_PATHS = [
    ROOT / "docs" / "trinity-runtime-model-resolution-v1.json",
    ROOT / "docs" / "v17-runtime-session-log-latest.json",
    ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json",
]

CLOSEOUT_JSON_PATHS = [
    ROOT / "docs" / "v41-beta-closeout-summary-v1.json",
    ROOT / "docs" / "v41-omega-closeout-summary-v1.json",
    ROOT / "docs" / "v42-beta-closeout-summary-v1.json",
]

HANDOFF_JSON_PATHS = [
    ROOT / "docs" / "v41-beta-handoff-policy-v1.json",
    ROOT / "docs" / "v41-omega-handoff-policy-v1.json",
    ROOT / "docs" / "v42-beta-handoff-policy-v1.json",
]

CONTINUITY_MD_PATHS = [
    ROOT / "docs" / "v41-beta-continuity-pack-v1.md",
    ROOT / "docs" / "v41-omega-continuity-pack-v1.md",
    ROOT / "docs" / "v42-beta-continuity-pack-v1.md",
]


def _md(payload: dict[str, Any]) -> str:
    pr_line = f"- PR reuse: `#{payload['pr_number']}` `{payload['pr_state']}` -> `{payload['pr_url']}`" if payload.get("pr_number") else "- PR reuse: `unverified`"
    return "\n".join(
        [
            "# V41 Git Publication Result",
            "",
            f"- Generated UTC: `{payload['generated_utc']}`",
            f"- Branch: `{payload['branch']}`",
            f"- Publication commit: `{payload['publication_commit_sha']}`",
            f"- Publication bookkeeping commit: `{payload['bookkeeping_commit_sha']}`",
            f"- Git cleanup state: `{payload['git_cleanup_state']}`",
            pr_line,
            "",
            "## Notes",
            "",
            "- The accidental main merge remains historical context only and was not rewritten.",
            "- Only the curated V41 allowlist was used for staging and publication.",
            "",
        ]
    ) + "\n"


def _rewrite_continuity_md(path: Path, git_cleanup_state: str, publication_commit_sha: str) -> None:
    if not path.exists():
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    updated: list[str] = []
    inserted_commit = False
    for line in lines:
        if line.startswith("- `git_cleanup_state`:"):
            updated.append(f"- `git_cleanup_state`: `{git_cleanup_state}`")
            continue
        updated.append(line)
        if not inserted_commit and line.startswith("- `git_cleanup_state`:"):
            inserted_commit = True
    if f"- `publication_commit_sha`: `{publication_commit_sha}`" not in updated:
        for index, line in enumerate(updated):
            if line.startswith("- `git_cleanup_state`:"):
                updated.insert(index + 1, f"- `publication_commit_sha`: `{publication_commit_sha}`")
                break
    write_text(path, "\n".join(updated).rstrip() + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish the V41 Git publication result.")
    parser.add_argument("--publication-commit", required=True, help="The commit SHA for the curated V41 publication commit.")
    parser.add_argument("--bookkeeping-commit", default="", help="Optional bookkeeping commit SHA when rerun after committing the result files.")
    parser.add_argument("--branch", default="codex/GHC-Family/beyonder-shared-omega-line")
    parser.add_argument("--pr-number", type=int)
    parser.add_argument("--pr-state", default="")
    parser.add_argument("--pr-url", default="")
    parser.add_argument("--git-cleanup-state", default="committed_pushed")
    args = parser.parse_args()

    payload = {
        "generated_utc": now_iso(),
        "phase": "v41_omega",
        "overall_status": "PASS",
        "branch": args.branch,
        "publication_commit_sha": args.publication_commit,
        "bookkeeping_commit_sha": args.bookkeeping_commit or args.publication_commit,
        "git_cleanup_state": args.git_cleanup_state,
        "pr_number": args.pr_number,
        "pr_state": args.pr_state,
        "pr_url": args.pr_url,
        "forward_only_cleanup": True,
        "accidental_merge_preserved": "2531562ec3",
    }
    write_json(RESULT_JSON, payload)
    write_text(RESULT_MD, _md(payload))

    for path in RUNTIME_PATHS:
        doc = read_json(path)
        if not doc:
            continue
        doc["git_cleanup_state"] = args.git_cleanup_state
        doc["publication_commit_sha"] = args.publication_commit
        doc["git_publication_result_path"] = "docs/trinity-live-traces/v41-git-publication-result-v1.json"
        write_json(path, doc)

    for path in CLOSEOUT_JSON_PATHS:
        doc = read_json(path)
        if not doc:
            continue
        core_states = doc.get("core_states")
        if isinstance(core_states, dict):
            core_states["git_cleanup_state"] = args.git_cleanup_state
        proof_paths = doc.get("proof_paths")
        if isinstance(proof_paths, dict):
            proof_paths["git_publication_result"] = "docs/trinity-live-traces/v41-git-publication-result-v1.json"
        doc["publication_commit_sha"] = args.publication_commit
        write_json(path, doc)

    for path in HANDOFF_JSON_PATHS:
        doc = read_json(path)
        if not doc:
            continue
        doc["git_cleanup_state"] = args.git_cleanup_state
        doc["publication_commit_sha"] = args.publication_commit
        doc["git_publication_result_path"] = "docs/trinity-live-traces/v41-git-publication-result-v1.json"
        write_json(path, doc)

    for path in CONTINUITY_MD_PATHS:
        _rewrite_continuity_md(path, args.git_cleanup_state, args.publication_commit)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
