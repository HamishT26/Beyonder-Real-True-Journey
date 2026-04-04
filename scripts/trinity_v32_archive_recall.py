#!/usr/bin/env python3
"""Recall a bounded archive through the indexed V32 helper surface."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import now_iso, repo_rel, write_json, write_text
from trinity_zip_memory_converter import DEFAULT_INDEX, recall

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v32-archive-recall-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v32-archive-recall-proof-v1.md"


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V32 Archive Recall Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Selected label: `{payload.get('selected_label', '') or 'unknown'}`",
        f"- Selected archive: `{payload.get('selected_archive', '') or 'unknown'}`",
        f"- Recalled to: `{payload.get('recalled_to', '') or 'unknown'}`",
        "",
    ]
    if payload.get("blockers"):
        lines.append("## Blockers")
        lines.append("")
        for blocker in payload["blockers"]:
            lines.append(f"- {blocker}")
    write_text(OUTPUT_MD, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Recall a Trinity archive through the V32 wrapper.")
    parser.add_argument("--label-contains", default="")
    parser.add_argument("--latest", action="store_true")
    parser.add_argument("--dest", default="docs/memory-archives/recalled")
    parser.add_argument("--decrypt-passphrase", default="")
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v32_omega",
        "overall_status": "WARN",
        "blockers": [],
    }
    try:
        selected, out_path = recall(
            DEFAULT_INDEX,
            args.label_contains,
            args.latest,
            args.dest,
            args.decrypt_passphrase,
        )
        payload.update(
            {
                "overall_status": "PASS",
                "selected_label": selected.get("label", ""),
                "selected_archive": selected.get("archive", ""),
                "recalled_to": repo_rel(Path(out_path)),
                "file_count": selected.get("file_count", 0),
            }
        )
    except Exception as exc:  # pragma: no cover - bounded wrapper
        payload["blockers"].append(str(exc))
    write_outputs(payload)
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
