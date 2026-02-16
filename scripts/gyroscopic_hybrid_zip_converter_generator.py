#!/usr/bin/env python3
"""Gyroscopic Hybrid Zip Converter Generator.

Builds an indexed Trinity snapshot and reports compression/reuse metrics
("reclaimed_bytes") to support storage-efficiency tracking.
"""

from __future__ import annotations

import argparse
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REPORT = ROOT / "docs" / "gyroscopic-hybrid-zip-report.json"


def _repo_path(p: str) -> Path:
    rp = (ROOT / p).resolve()
    rp.relative_to(ROOT)
    return rp


def _load_zip_module():
    import importlib.util

    mod_path = ROOT / "scripts" / "trinity_zip_memory_converter.py"
    spec = importlib.util.spec_from_file_location("trinity_zip_memory_converter", mod_path)
    if spec is None or spec.loader is None:
        raise SystemExit("unable to load trinity_zip_memory_converter module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_default_sources() -> list[str]:
    module = _load_zip_module()
    return list(module.DEFAULT_SOURCES)


def _archive(label: str, sources: list[str], archive_dir: str, index_path: str) -> Path:
    module = _load_zip_module()
    return module.archive(
        label=label,
        sources=sources,
        archive_dir=module._resolve_repo_relative(archive_dir),
        index_path=module._resolve_repo_relative(index_path),
        encrypt_passphrase="",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run gyroscopic hybrid zip converter generator")
    parser.add_argument("--label", default="gyroscopic-hybrid-cycle")
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--out", default=str(DEFAULT_REPORT.relative_to(ROOT)))
    parser.add_argument("--archive-dir", default="docs/memory-archives")
    parser.add_argument("--index", default="docs/memory-archives/index.jsonl")
    args = parser.parse_args()

    sources = args.source or _load_default_sources()
    pre_total = 0
    existing = []
    for s in sources:
        p = _repo_path(s)
        if p.exists() and p.is_file():
            pre_total += p.stat().st_size
            existing.append(p)

    archive_path = _archive(args.label, sources, args.archive_dir, args.index)

    compressed_size = archive_path.stat().st_size if archive_path.exists() else 0
    reclaimed = max(0, pre_total - compressed_size)
    reuse_ratio = round((reclaimed / pre_total), 6) if pre_total else 0.0

    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "engine": "gyroscopic-hybrid-zip-converter-generator",
        "label": args.label,
        "archive": archive_path.relative_to(ROOT).as_posix(),
        "inputs": {
            "source_count_requested": len(sources),
            "source_count_found": len(existing),
            "uncompressed_bytes": pre_total,
        },
        "outputs": {
            "compressed_bytes": compressed_size,
            "reclaimed_bytes": reclaimed,
            "reuse_ratio": reuse_ratio,
        },
    }

    out = _repo_path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
