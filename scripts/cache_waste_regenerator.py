#!/usr/bin/env python3
"""Cache/Waste Regenerator System.

Recycles cache-like and temporary artifacts into measurable reclaimed-bytes metrics
and estimates equivalent token/credit/energy value routed to reserve reporting.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REPORT = ROOT / "docs" / "cache-waste-regenerator-report.json"

DEFAULT_PATTERNS = [
    "docs/_tmp-*.json",
    "docs/_tmp-*.jsonl",
    "docs/memory-archives/_tmp*",
    "scripts/__pycache__",
]


def _repo_path(p: str) -> Path:
    rp = (ROOT / p).resolve()
    rp.relative_to(ROOT)
    return rp




def _tracked_paths() -> set[Path]:
    try:
        out = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    except Exception:
        return set()
    paths: set[Path] = set()
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        paths.add((ROOT / line).resolve())
    return paths

def _collect(paths_or_globs: list[str]) -> list[Path]:
    out: list[Path] = []
    for item in paths_or_globs:
        if any(ch in item for ch in "*?[]"):
            out.extend(sorted(ROOT.glob(item)))
        else:
            p = _repo_path(item)
            if p.exists():
                out.append(p)
    seen = set()
    uniq: list[Path] = []
    for p in out:
        if p in seen:
            continue
        seen.add(p)
        uniq.append(p)
    return uniq




def _purge_path(path: Path) -> None:
    if path.is_file() or path.is_symlink():
        path.unlink(missing_ok=True)
        return
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)


def _prune_empty_ancestors(path: Path, stop: Path) -> None:
    cur = path.parent
    while cur != stop and cur.exists():
        try:
            next(cur.iterdir())
            break
        except StopIteration:
            cur.rmdir()
            cur = cur.parent

def _size_bytes(path: Path) -> int:
    if path.is_file():
        return path.stat().st_size
    if path.is_dir():
        total = 0
        for sub in path.rglob("*"):
            if sub.is_file():
                total += sub.stat().st_size
        return total
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Run cache/waste regenerator")
    parser.add_argument("--path", action="append", default=[], help="Repo-relative file/dir/glob to include")
    parser.add_argument("--tokens-per-byte", type=float, default=0.02)
    parser.add_argument("--credits-per-1k-tokens", type=float, default=1.0)
    parser.add_argument("--energy-per-token", type=float, default=0.001)
    parser.add_argument("--out", default=str(DEFAULT_REPORT.relative_to(ROOT)))
    parser.add_argument("--purge", action="store_true", help="Delete reclaimed files/directories after measuring")
    parser.add_argument("--prune-empty-dirs", action="store_true", help="After purge, remove empty parent dirs up to repo root")
    parser.add_argument("--allow-purge-tracked", action="store_true", help="Allow purging files/directories that are git-tracked")
    args = parser.parse_args()

    targets = args.path or DEFAULT_PATTERNS
    entries = _collect(targets)

    tracked_paths = _tracked_paths()
    reclaimed_bytes = 0
    purged_bytes = 0
    purged_count = 0
    skipped_tracked_purge_count = 0
    item_rows: list[dict[str, object]] = []
    for p in entries:
        size = _size_bytes(p)
        if size <= 0:
            continue
        reclaimed_bytes += size
        is_tracked = p in tracked_paths
        row = {
            "path": p.relative_to(ROOT).as_posix(),
            "bytes": size,
            "purged": False,
            "tracked": is_tracked,
            "purge_skipped_reason": "",
        }
        if args.purge:
            if is_tracked and not args.allow_purge_tracked:
                row["purge_skipped_reason"] = "tracked_path"
                skipped_tracked_purge_count += 1
            else:
                _purge_path(p)
                row["purged"] = True
                purged_bytes += size
                purged_count += 1
                if args.prune_empty_dirs:
                    _prune_empty_ancestors(p, ROOT)
        item_rows.append(row)

    reclaimed_tokens = round(reclaimed_bytes * max(0.0, args.tokens_per_byte), 6)
    reclaimed_credits = round((reclaimed_tokens / 1000.0) * max(0.0, args.credits_per_1k_tokens), 6)
    reclaimed_energy_units = round(reclaimed_tokens * max(0.0, args.energy_per_token), 6)

    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "engine": "cache-waste-regenerator",
        "inputs": {
            "targets": targets,
            "tokens_per_byte": args.tokens_per_byte,
            "credits_per_1k_tokens": args.credits_per_1k_tokens,
            "energy_per_token": args.energy_per_token,
        },
        "outputs": {
            "reclaimed_bytes": reclaimed_bytes,
            "reclaimed_tokens": reclaimed_tokens,
            "reclaimed_credits": reclaimed_credits,
            "reclaimed_energy_units": reclaimed_energy_units,
            "purged_bytes": purged_bytes,
            "purged_count": purged_count,
            "skipped_tracked_purge_count": skipped_tracked_purge_count,
            "items": item_rows,
        },
    }

    out = _repo_path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
