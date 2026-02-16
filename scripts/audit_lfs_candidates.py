#!/usr/bin/env python3
"""Audit tracked binary files and recommend Git LFS patterns."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REPORT = ROOT / "docs" / "lfs-candidate-report.md"

BINARY_EXTS = {
    ".pdf",
    ".zip",
    ".docx",
    ".png",
    ".jpg",
    ".jpeg",
    ".mp4",
    ".mov",
    ".bin",
}

LFS_PATTERNS = [
    "*.pdf",
    "*.zip",
    "*.docx",
    "*.png",
    "*.jpg",
    "*.jpeg",
    "docs/memory-archives/*.zip",
]


def tracked_files() -> list[Path]:
    out = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    return [ROOT / line.strip() for line in out.splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit git-tracked binary/LFS candidates")
    parser.add_argument("--min-bytes", type=int, default=5_000_000, help="Size threshold for high-priority LFS candidates")
    parser.add_argument("--report", default=str(DEFAULT_REPORT.relative_to(ROOT)))
    parser.add_argument("--write-gitattributes", action="store_true", help="Write suggested patterns to .gitattributes")
    args = parser.parse_args()

    rows = []
    for path in tracked_files():
        if not path.exists() or not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        ext = path.suffix.lower()
        size = path.stat().st_size
        if ext in BINARY_EXTS or size >= args.min_bytes:
            rows.append((str(rel).replace("\\", "/"), size, ext in BINARY_EXTS))

    rows.sort(key=lambda x: x[1], reverse=True)

    report_path = (ROOT / args.report).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Git LFS Candidate Audit",
        "",
        f"- Minimum size threshold: `{args.min_bytes}` bytes",
        f"- Tracked candidates found: **{len(rows)}**",
        "",
        "| Path | Size (bytes) | Binary extension |",
        "|---|---:|:---:|",
    ]
    for rel, size, ext_bin in rows:
        lines.append(f"| `{rel}` | {size} | {'yes' if ext_bin else 'no'} |")

    lines.extend([
        "",
        "## Suggested `.gitattributes` patterns",
        "",
    ])
    lines.extend([f"- `{p}`" for p in LFS_PATTERNS])

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {report_path}")

    if args.write_gitattributes:
        ga = ROOT / ".gitattributes"
        existing = ga.read_text(encoding="utf-8") if ga.exists() else ""
        add_lines = [f"{p} filter=lfs diff=lfs merge=lfs -text" for p in LFS_PATTERNS]
        missing = [l for l in add_lines if l not in existing]
        if missing:
            with ga.open("a", encoding="utf-8") as fh:
                if existing and not existing.endswith("\n"):
                    fh.write("\n")
                fh.write("\n".join(missing) + "\n")
            print(f"Updated {ga} with {len(missing)} LFS patterns")
        else:
            print(f"No .gitattributes updates needed in {ga}")


if __name__ == "__main__":
    main()
