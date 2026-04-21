#!/usr/bin/env python3
"""Publish the V46 git publication result after push and PR update."""

from __future__ import annotations

import argparse
from pathlib import Path

from trinity_v46_common import PUBLICATION_BRANCH, ROOT, git_head, now_iso, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v46-git-publication-result-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v46-git-publication-result-v1.md"


def markdown(payload: dict[str, object]) -> str:
    lines = [
        "# V46 Git Publication Result",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Branch: `{payload['branch']}`",
        f"- Publication commit: `{payload['publication_commit_sha']}`",
        f"- Current local head: `{payload['current_local_head_sha']}`",
        f"- Git publication state: `{payload['git_publication_state']}`",
        f"- PR number: `{payload['pr_number']}`",
        f"- PR state: `{payload['pr_state']}`",
    ]
    if payload.get("pr_url"):
        lines.append(f"- PR URL: `{payload['pr_url']}`")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish the V46 git publication result.")
    parser.add_argument("--publication-commit", required=True)
    parser.add_argument("--branch", default=PUBLICATION_BRANCH)
    parser.add_argument("--pr-number", type=int, default=45)
    parser.add_argument("--pr-state", default="open")
    parser.add_argument("--pr-url", default="")
    parser.add_argument("--git-publication-state", default="committed_pushed_pr_updated")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    payload = {
        "generated_utc": now_iso(),
        "phase": "v46_omega",
        "branch": args.branch,
        "publication_commit_sha": args.publication_commit,
        "current_local_head_sha": git_head(),
        "git_publication_state": args.git_publication_state,
        "pr_number": args.pr_number,
        "pr_state": args.pr_state,
        "pr_url": args.pr_url,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
