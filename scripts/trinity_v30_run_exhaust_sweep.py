#!/usr/bin/env python3
"""Archive and restore accidental run-exhaust churn from the shared branch tip."""

from __future__ import annotations

import json
import os
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from trinity_zip_memory_converter import archive as zip_archive

ROOT = Path(__file__).resolve().parent.parent
BASELINE_SHA = "714aca4893713b0aca32d3c5b3a2a730d4665c4b"
LOCAL_ARCHIVE_ROOT = ROOT / ".local-archives" / "v29-run-exhaust"
ARCHIVE_DIR = LOCAL_ARCHIVE_ROOT / "zips"
INDEX_PATH = LOCAL_ARCHIVE_ROOT / "index.jsonl"
MANIFEST_PATH = LOCAL_ARCHIVE_ROOT / "last-run-manifest.json"
PROOF_JSON = ROOT / "docs" / "trinity-live-traces" / "v30-run-exhaust-archive-proof-v1.json"
PROOF_MD = ROOT / "docs" / "trinity-live-traces" / "v30-run-exhaust-archive-proof-v1.md"

TARGET_PATHS = [
    "docs/aletheon-memory-runs",
    "docs/body-track-runs",
    "docs/freedid-compliance-bridge-runs",
    "docs/heart-track-runs",
    "docs/logs",
    "docs/mind-track-extraction-traces",
    "docs/mind-track-runs",
    "docs/trinity-agent-council-runs",
    "docs/trinity-api-board-runs",
    "docs/trinity-api-manifest-runs",
    "docs/trinity-command-book-runs",
    "docs/trinity-control-tower-runs",
    "docs/trinity-expansion-manifest-runs",
    "docs/trinity-expansion-result-runs",
    "docs/trinity-expansion-runs",
    "docs/trinity-extension-catalog-runs",
    "docs/trinity-journey-corpus-runs",
    "docs/trinity-mandala-runs",
    "docs/trinity-materialization-ladder-runs",
    "docs/trinity-materialization-ledger-runs",
    "docs/trinity-os-runtime-reference-runs",
    "docs/trinity-public-research-runs",
    "docs/trinity-public-signal-runs",
    "docs/trinity-supplemental-reflection-runs",
    "docs/v17-control-tower-runs",
    "docs/v17-standards-bridge-runs",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def existing_pathspecs() -> list[str]:
    return [pathspec for pathspec in TARGET_PATHS if (ROOT / pathspec).exists()]


def changed_paths(pathspecs: list[str]) -> list[str]:
    if not pathspecs:
        return []
    result = git("diff", "--name-only", f"{BASELINE_SHA}..HEAD", "--", *pathspecs)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git diff failed while collecting run-exhaust paths")
    paths = [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]
    return sorted(dict.fromkeys(paths))


def remaining_worktree_paths(pathspecs: list[str]) -> list[str]:
    if not pathspecs:
        return []
    result = git("diff", "--name-only", BASELINE_SHA, "--", *pathspecs)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git diff failed while verifying restored worktree paths")
    paths = [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]
    return sorted(dict.fromkeys(paths))


def family_for(path: str) -> str:
    for prefix in TARGET_PATHS:
        normalized = prefix.replace("\\", "/").rstrip("/") + "/"
        if path.startswith(normalized):
            return prefix.replace("\\", "/")
    return "unclassified"


def remove_empty_dirs(pathspecs: list[str]) -> None:
    for pathspec in sorted(pathspecs, key=len, reverse=True):
        root_path = ROOT / pathspec
        if not root_path.exists():
            continue
        for current, dirs, files in os.walk(root_path, topdown=False):
            current_path = Path(current)
            if current_path == root_path:
                continue
            if any(current_path.iterdir()):
                continue
            current_path.rmdir()


def build_payload(
    *,
    overall_status: str,
    message: str,
    pathspecs: list[str],
    candidate_paths: list[str],
    archived_files: list[str],
    archive_path: str,
    remaining_paths: list[str],
) -> dict:
    family_counts = Counter(family_for(path) for path in candidate_paths)
    return {
        "generated_utc": now_iso(),
        "phase": "v30_omega",
        "overall_status": overall_status,
        "baseline_sha": BASELINE_SHA,
        "active_branch": "codex/GHC-Family/beyonder-shared-omega-line",
        "target_pathspecs": pathspecs,
        "candidate_file_count": len(candidate_paths),
        "archived_file_count": len(archived_files),
        "remaining_file_count_in_scope": len(remaining_paths),
        "archive_root": str(LOCAL_ARCHIVE_ROOT.relative_to(ROOT)).replace("\\", "/"),
        "archive_dir": str(ARCHIVE_DIR.relative_to(ROOT)).replace("\\", "/"),
        "archive_index": str(INDEX_PATH.relative_to(ROOT)).replace("\\", "/"),
        "archive_path": archive_path,
        "family_counts": dict(sorted(family_counts.items())),
        "sample_paths": candidate_paths[:40],
        "remaining_sample_paths": remaining_paths[:20],
        "message": message,
        "notes": [
            "This sweep intentionally targets stamped run-exhaust families only.",
            "Stable latest/proof/handoff/runtime surfaces remain outside this cleanup scope.",
            "Mixed-risk council chat, memory-ledger, and role-contract families require separate policy review.",
        ],
        "recall": {
            "manifest_path": str(MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/"),
            "zip_converter_script": "scripts/trinity_zip_memory_converter.py",
            "example_recall_command": (
                "python scripts/trinity_zip_memory_converter.py recall "
                "--index .local-archives/v29-run-exhaust/index.jsonl "
                "--label-contains v30-run-exhaust-repair "
                "--latest --dest .local-archives/v29-run-exhaust/recalled"
            ),
        },
    }


def main() -> int:
    pathspecs = existing_pathspecs()
    already_clean = remaining_worktree_paths(pathspecs)
    if not already_clean and MANIFEST_PATH.exists():
        prior = read_json(MANIFEST_PATH)
        payload = {
            **prior,
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "remaining_file_count_in_scope": 0,
            "remaining_sample_paths": [],
            "message": "Configured run-exhaust families already match the curated V29 baseline; existing local archive proof retained.",
        }
        write_json(MANIFEST_PATH, payload)
        write_json(PROOF_JSON, payload)
        write_text(
            PROOF_MD,
            "\n".join(
                [
                    "# V30 Run Exhaust Archive Proof",
                    "",
                    "- overall_status: `PASS`",
                    f"- baseline_sha: `{BASELINE_SHA}`",
                    f"- candidate_file_count: `{payload.get('candidate_file_count', 0)}`",
                    f"- archived_file_count: `{payload.get('archived_file_count', 0)}`",
                    "- remaining_file_count_in_scope: `0`",
                    f"- archive_path: `{payload.get('archive_path') or 'n/a'}`",
                    "",
                    "## Message",
                    f"- {payload['message']}",
                    "",
                ]
            ),
        )
        print(json.dumps({"overall_status": "PASS", "candidate_file_count": payload.get("candidate_file_count", 0), "remaining_file_count_in_scope": 0}))
        return 0

    candidates = changed_paths(pathspecs)
    archive_sources = [path for path in candidates if (ROOT / path).is_file()]

    if not candidates:
        payload = build_payload(
            overall_status="PASS",
            message="No run-exhaust delta was found under the configured cleanup scope.",
            pathspecs=pathspecs,
            candidate_paths=[],
            archived_files=[],
            archive_path="",
            remaining_paths=[],
        )
        write_json(MANIFEST_PATH, payload)
        write_json(PROOF_JSON, payload)
        write_text(
            PROOF_MD,
            "\n".join(
                [
                    "# V30 Run Exhaust Archive Proof",
                    "",
                    "- overall_status: `PASS`",
                    "- message: `No run-exhaust delta was found under the configured cleanup scope.`",
                    f"- baseline_sha: `{BASELINE_SHA}`",
                    "",
                ]
            ),
        )
        print(json.dumps({"overall_status": payload["overall_status"], "candidate_file_count": 0}))
        return 0

    archive_path = zip_archive(
        label="v30-run-exhaust-repair",
        sources=archive_sources,
        archive_dir=ARCHIVE_DIR,
        index_path=INDEX_PATH,
    )

    restore = git("restore", f"--source={BASELINE_SHA}", "--worktree", "--", *pathspecs)
    if restore.returncode != 0:
        raise RuntimeError(restore.stderr.strip() or "git restore failed while reverting run-exhaust paths")

    remove_empty_dirs(pathspecs)
    remaining = remaining_worktree_paths(pathspecs)

    payload = build_payload(
        overall_status="PASS" if not remaining else "WARN",
        message=(
            "Run-exhaust families were archived into the local gitignored cache and restored to the curated V29 baseline."
            if not remaining
            else "The sweep archived and restored the configured families, but some in-scope paths still differ from the curated baseline."
        ),
        pathspecs=pathspecs,
        candidate_paths=candidates,
        archived_files=archive_sources,
        archive_path=str(archive_path.relative_to(ROOT)).replace("\\", "/"),
        remaining_paths=remaining,
    )

    write_json(MANIFEST_PATH, payload)
    write_json(PROOF_JSON, payload)
    write_text(
        PROOF_MD,
        "\n".join(
            [
                "# V30 Run Exhaust Archive Proof",
                "",
                f"- overall_status: `{payload['overall_status']}`",
                f"- baseline_sha: `{BASELINE_SHA}`",
                f"- candidate_file_count: `{payload['candidate_file_count']}`",
                f"- archived_file_count: `{payload['archived_file_count']}`",
                f"- remaining_file_count_in_scope: `{payload['remaining_file_count_in_scope']}`",
                f"- archive_path: `{payload['archive_path'] or 'n/a'}`",
                "",
                "## Families",
                *[f"- {family}: `{count}`" for family, count in payload["family_counts"].items()],
                "",
                "## Message",
                f"- {payload['message']}",
                "",
            ]
        ),
    )
    print(
        json.dumps(
            {
                "overall_status": payload["overall_status"],
                "candidate_file_count": payload["candidate_file_count"],
                "remaining_file_count_in_scope": payload["remaining_file_count_in_scope"],
            }
        )
    )
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
