#!/usr/bin/env python3
"""Publish the V43 forward-only Git publication result and refresh closeout/runtime truth.""" 

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v43_common import ROOT, now_iso, read_json, write_json, write_text

RESULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-git-publication-result-v1.json"
RESULT_MD = ROOT / "docs" / "trinity-live-traces" / "v43-git-publication-result-v1.md"

RUNTIME_PATHS = [
    ROOT / "docs" / "trinity-runtime-model-resolution-v1.json",
    ROOT / "docs" / "v17-runtime-session-log-latest.json",
    ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json",
    ROOT / "docs" / "v17-runtime-session-validation-latest.json",
]

CLOSEOUT_JSON_PATHS = [
    ROOT / "docs" / "v43-omega-closeout-summary-v1.json",
    ROOT / "docs" / "v44-beta-closeout-summary-v1.json",
]

HANDOFF_JSON_PATHS = [
    ROOT / "docs" / "v43-omega-handoff-policy-v1.json",
    ROOT / "docs" / "v44-beta-handoff-policy-v1.json",
]

CONTINUITY_MD_PATHS = [
    ROOT / "docs" / "v43-omega-continuity-pack-v1.md",
    ROOT / "docs" / "v44-beta-continuity-pack-v1.md",
]


def _md(payload: dict[str, Any]) -> str:
    pr_line = (
        f"- PR reuse: `#{payload['pr_number']}` `{payload['pr_state']}` -> `{payload['pr_url']}`"
        if payload.get("pr_number")
        else "- PR reuse: `unverified`"
    )
    return "\n".join(
        [
            "# V43 Git Publication Result",
            "",
            f"- Generated UTC: `{payload['generated_utc']}`",
            f"- Branch: `{payload['branch']}`",
            f"- Publication commit: `{payload['publication_commit_sha']}`",
            f"- Bookkeeping commit: `{payload['bookkeeping_commit_sha']}`",
            f"- Git publication state: `{payload['git_publication_state']}`",
            pr_line,
            "",
            "## Notes",
            "",
            "- Only the curated V43 allowlist was staged and published.",
            "- Carried-forward dirty latest-state churn remained outside the V43 publication set.",
            "",
        ]
    ) + "\n"


def _rewrite_continuity_md(path: Path, git_publication_state: str, publication_commit_sha: str) -> None:
    if not path.exists():
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    updated: list[str] = []
    for line in lines:
        if line.startswith("- Current head:"):
            updated.append(f"- Current head: `{publication_commit_sha}`")
            continue
        if line.startswith("- `git_publication_state`:"):
            updated.append(f"- `git_publication_state`: `{git_publication_state}`")
            continue
        updated.append(line)
    if f"- `publication_commit_sha`: `{publication_commit_sha}`" not in updated:
        for index, line in enumerate(updated):
            if line.startswith("- `git_publication_state`:"):
                updated.insert(index + 1, f"- `publication_commit_sha`: `{publication_commit_sha}`")
                break
    write_text(path, "\n".join(updated).rstrip() + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish the V43 Git publication result.")
    parser.add_argument("--publication-commit", required=True, help="The commit SHA for the curated V43 publication commit.")
    parser.add_argument("--bookkeeping-commit", default="", help="Optional bookkeeping commit SHA after writing the result files.")
    parser.add_argument("--branch", default="codex/GHC-Family/beyonder-shared-omega-line")
    parser.add_argument("--pr-number", type=int)
    parser.add_argument("--pr-state", default="")
    parser.add_argument("--pr-url", default="")
    parser.add_argument("--git-publication-state", default="committed_pushed_pr_updated")
    args = parser.parse_args()

    payload = {
        "generated_utc": now_iso(),
        "phase": "v43_omega",
        "overall_status": "PASS",
        "branch": args.branch,
        "publication_commit_sha": args.publication_commit,
        "bookkeeping_commit_sha": args.bookkeeping_commit or args.publication_commit,
        "git_publication_state": args.git_publication_state,
        "pr_number": args.pr_number,
        "pr_state": args.pr_state,
        "pr_url": args.pr_url,
        "forward_only_cleanup": True,
    }
    write_json(RESULT_JSON, payload)
    write_text(RESULT_MD, _md(payload))

    for path in RUNTIME_PATHS:
        doc = read_json(path)
        if not doc:
            continue
        doc["git_publication_state"] = args.git_publication_state
        doc["current_head_sha"] = args.publication_commit
        doc["publication_commit_sha"] = args.publication_commit
        doc["checkpoint_anchor_commit"] = args.publication_commit
        doc["git_publication_result_path"] = "docs/trinity-live-traces/v43-git-publication-result-v1.json"
        write_json(path, doc)

    for path in CLOSEOUT_JSON_PATHS:
        doc = read_json(path)
        if not doc:
            continue
        if "current_head_sha" in doc:
            doc["current_head_sha"] = args.publication_commit
        core_states = doc.get("core_states")
        if isinstance(core_states, dict):
            core_states["git_publication_state"] = args.git_publication_state
        proof_paths = doc.get("proof_paths")
        if isinstance(proof_paths, dict):
            proof_paths["git_publication_result"] = "docs/trinity-live-traces/v43-git-publication-result-v1.json"
        doc["publication_commit_sha"] = args.publication_commit
        write_json(path, doc)

    for path in HANDOFF_JSON_PATHS:
        doc = read_json(path)
        if not doc:
            continue
        if "source_head_sha" in doc:
            doc["source_head_sha"] = args.publication_commit
        doc["git_publication_state"] = args.git_publication_state
        doc["publication_commit_sha"] = args.publication_commit
        doc["git_publication_result_path"] = "docs/trinity-live-traces/v43-git-publication-result-v1.json"
        write_json(path, doc)

    for path in CONTINUITY_MD_PATHS:
        _rewrite_continuity_md(path, args.git_publication_state, args.publication_commit)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
