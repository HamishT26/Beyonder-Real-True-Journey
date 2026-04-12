#!/usr/bin/env python3
"""Write the V40 git publication result artifact after commit/push/PR."""

from __future__ import annotations

import argparse
from pathlib import Path

from trinity_v40_common import now_iso, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v40-git-publication-result-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v40-git-publication-result-v1.md"


def markdown(payload: dict) -> str:
    lines = [
        "# V40 Git Publication Result",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Git publication state: `{payload['git_publication_state']}`",
        f"- Head SHA: `{payload.get('current_head_sha', '') or 'unknown'}`",
        f"- Branch: `{payload.get('branch', '') or 'unknown'}`",
        f"- PR URL: `{payload.get('pull_request_url', '') or 'not_created'}`",
        "",
        "## Staged Files",
        "",
    ]
    lines.extend(f"- `{row}`" for row in payload.get("staged_files", []))
    if payload.get("bounded_residuals"):
        lines.extend(["", "## Bounded Residuals", ""])
        lines.extend(f"- {row}" for row in payload["bounded_residuals"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Write the V40 git publication result artifact.")
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--commit-sha", required=True)
    parser.add_argument("--commit-subject", required=True)
    parser.add_argument("--push-status", choices=["ok", "failed"], required=True)
    parser.add_argument("--pr-url", default="")
    parser.add_argument("--pr-status", choices=["created", "updated", "failed", "skipped"], default="skipped")
    parser.add_argument("--allowlist-path", default="docs/trinity-live-traces/v40-stage-allowlist-v1.json")
    parser.add_argument("--staged-file", action="append", default=[])
    parser.add_argument("--bounded-residual", action="append", default=[])
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    publication_ok = args.push_status == "ok" and args.pr_status in {"created", "updated"}
    payload = {
        "generated_utc": now_iso(),
        "phase": "v40_omega",
        "overall_status": "PASS" if publication_ok else "WARN",
        "git_publication_state": "commit_push_pr_updated" if publication_ok else "commit_push_or_pr_bounded",
        "current_head_sha": args.head_sha,
        "branch": args.branch,
        "commit_sha": args.commit_sha,
        "commit_subject": args.commit_subject,
        "push_status": args.push_status,
        "pull_request_status": args.pr_status,
        "pull_request_url": args.pr_url,
        "allowlist_path": args.allowlist_path,
        "staged_files": args.staged_file,
        "bounded_residuals": args.bounded_residual,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
