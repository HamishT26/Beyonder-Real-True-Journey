#!/usr/bin/env python3
"""Build a privacy-minimizing evidence index for Journey text records.

The index records provenance, hashes, sizes, message-marker counts, and bounded
keyword counts.  It deliberately does not reproduce conversation excerpts or
machine-local absolute paths.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


VERSION_RE = re.compile(r"(?i)\bv(\d{1,3})\b")
MESSAGE_RE = re.compile(
    r"(?im)^\s*(?:message(?:\s+response)?|response)\s*(?:#|no\.?\s*)?\d+\b"
)

KEYWORDS = {
    "gmut": re.compile(r"(?i)\bGMUT\b|Grand Mandala Unified Theory"),
    "thos": re.compile(r"(?i)\bTHOS\b|Trinity Hybrid (?:OS|Operating System)"),
    "freed_id": re.compile(r"(?i)Freed\s*ID"),
    "cosmic_bill_of_rights": re.compile(r"(?i)Cosmic Bill of Rights"),
    "omega_term": re.compile(r"(?i)Omega[_\s-]*AB|Ω\s*[_\{]?AB|Mandala Field Equation"),
    "equation": re.compile(r"(?i)equation|tensor|Lagrangian|action functional"),
    "falsification": re.compile(r"(?i)falsif(?:y|iable|ication)|rejection rule|null limit"),
    "evidence_boundary": re.compile(r"(?i)not (?:yet )?(?:validated|verified|proven)|aspirational|candidate"),
    "consent": re.compile(r"(?i)consent|least authority|reversib"),
    "privacy": re.compile(r"(?i)privacy|private|redact|credential|secret"),
}


@dataclass(frozen=True)
class InputRecord:
    path: Path
    source_class: str
    source_id: str


def decode_bytes(raw: bytes) -> tuple[str, str, int]:
    """Decode common Journey exports while reporting replacement characters."""
    for encoding in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            text = raw.decode(encoding)
            return text, encoding, text.count("\ufffd")
        except UnicodeDecodeError:
            continue
    text = raw.decode("utf-8", errors="replace")
    return text, "utf-8-replace", text.count("\ufffd")


def parse_version(name: str) -> int | None:
    match = VERSION_RE.search(name)
    return int(match.group(1)) if match else None


def iter_repo_inputs(root: Path, start: int, end: int) -> Iterable[InputRecord]:
    for path in sorted(root.glob("*.txt"), key=lambda p: p.name.casefold()):
        version = parse_version(path.name)
        if version is None or not start <= version <= end:
            continue
        yield InputRecord(path, "repository_journey_export", path.name)


def external_input(path: Path) -> InputRecord:
    # External paths are intentionally reduced to a basename in committed output.
    return InputRecord(path, "user_supplied_journey_export", path.name)


def analyze(record: InputRecord) -> dict:
    raw = record.path.read_bytes()
    text, encoding, replacement_count = decode_bytes(raw)
    version = parse_version(record.path.name)
    lines = text.splitlines()
    nonempty = sum(1 for line in lines if line.strip())
    return {
        "version": version,
        "source_id": record.source_id,
        "source_class": record.source_class,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "line_count": len(lines),
        "nonempty_line_count": nonempty,
        "message_marker_count": len(MESSAGE_RE.findall(text)),
        "encoding_used": encoding,
        "decode_replacement_count": replacement_count,
        "keyword_counts": {name: len(pattern.findall(text)) for name, pattern in KEYWORDS.items()},
        "evidence_tier": "primary_project_record_not_external_scientific_validation",
        "content_embedded": False,
    }


def build_index(
    records: list[InputRecord], start: int, end: int, generated_at_utc: str
) -> dict:
    analyzed = [analyze(record) for record in records]
    by_version: dict[int, list[dict]] = defaultdict(list)
    by_hash: dict[str, list[dict]] = defaultdict(list)
    for item in analyzed:
        if item["version"] is not None:
            by_version[item["version"]].append(item)
        by_hash[item["sha256"]].append(item)

    version_rows = []
    for version in range(start, end + 1):
        variants = sorted(
            by_version.get(version, []),
            key=lambda item: (-item["bytes"], item["source_id"].casefold()),
        )
        if not variants:
            version_rows.append({"version": version, "status": "missing", "variants": []})
            continue
        canonical = variants[0]
        version_rows.append(
            {
                "version": version,
                "status": "indexed",
                "variant_count": len(variants),
                "canonical_source_id": canonical["source_id"],
                "canonical_selection_rule": "largest_byte_count_then_source_id",
                "variants": variants,
            }
        )

    exact_duplicate_groups = []
    for sha, items in sorted(by_hash.items()):
        if len(items) > 1:
            exact_duplicate_groups.append(
                {
                    "sha256": sha,
                    "source_ids": sorted(item["source_id"] for item in items),
                }
            )

    return {
        "schema": "ghc.family.journey-evidence-index.v2",
        "generated_at_utc": generated_at_utc,
        "scope": {"version_start": start, "version_end": end},
        "method": {
            "privacy": "hashes_and_counts_only_no_conversation_excerpts_no_absolute_paths",
            "canonical_rule": "largest byte count per version; every variant remains indexed",
            "message_marker_regex": MESSAGE_RE.pattern,
            "limitations": [
                "Message markers vary across exports, so counts are approximate.",
                "Keyword frequency measures mention volume, not truth or scientific support.",
                "Journey records establish project provenance, not independent validation.",
                "Largest-file canonical selection is deterministic, not a claim of completeness.",
            ],
        },
        "summary": {
            "input_file_count": len(analyzed),
            "indexed_version_count": sum(1 for row in version_rows if row["status"] == "indexed"),
            "missing_versions": [row["version"] for row in version_rows if row["status"] == "missing"],
            "exact_duplicate_group_count": len(exact_duplicate_groups),
            "source_class_counts": dict(Counter(item["source_class"] for item in analyzed)),
        },
        "versions": version_rows,
        "exact_duplicate_groups": exact_duplicate_groups,
    }


def markdown(index: dict) -> str:
    rows = [
        "# Journey Evidence Index (v36-v54)",
        "",
        "> Privacy-minimizing provenance index. No conversation excerpts or absolute machine paths are embedded.",
        "",
        "| Version | Status | Variants | Canonical record | Lines | Message markers | GMUT | THOS | Freed ID | CBR |",
        "|---:|---|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in index["versions"]:
        if row["status"] == "missing":
            rows.append(f"| {row['version']} | missing | 0 | - | - | - | - | - | - | - |")
            continue
        canonical = next(
            item for item in row["variants"] if item["source_id"] == row["canonical_source_id"]
        )
        counts = canonical["keyword_counts"]
        rows.append(
            "| {version} | indexed | {variants} | {source} | {lines} | {messages} | {gmut} | {thos} | {freed} | {cbr} |".format(
                version=row["version"],
                variants=row["variant_count"],
                source=row["canonical_source_id"].replace("|", "\\|"),
                lines=canonical["line_count"],
                messages=canonical["message_marker_count"],
                gmut=counts["gmut"],
                thos=counts["thos"],
                freed=counts["freed_id"],
                cbr=counts["cosmic_bill_of_rights"],
            )
        )
    rows += [
        "",
        "## Interpretation boundary",
        "",
        "The counts above establish corpus coverage and reproducible mention patterns. They do not establish that any scientific, engineering, legal, spiritual, or personhood claim is true. The accompanying synthesis applies separate evidence grades to those claims.",
        "",
        "## Rebuild",
        "",
        "Run `scripts/build_ghc_family_journey_evidence_index.py` with the repository text folder, any user-supplied exports, and a pinned `--generated-at-utc` value for byte-reproducible output. External source paths are reduced to basenames in output.",
        "",
    ]
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("docs/beyonder-real-true-journey/texts"),
        help="Repository directory containing Journey TXT exports.",
    )
    parser.add_argument("--start", type=int, default=36)
    parser.add_argument("--end", type=int, default=54)
    parser.add_argument("--external-file", action="append", type=Path, default=[])
    parser.add_argument(
        "--generated-at-utc",
        default=None,
        help="Pinned ISO-8601 build timestamp; omit only for an intentionally current build.",
    )
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    records = list(iter_repo_inputs(args.root, args.start, args.end))
    for path in args.external_file:
        if not path.is_file():
            parser.error(f"external file does not exist: {path}")
        records.append(external_input(path))
    if not records:
        parser.error("no inputs matched the requested scope")

    generated_at_utc = args.generated_at_utc or datetime.now(timezone.utc).replace(
        microsecond=0
    ).isoformat()
    index = build_index(records, args.start, args.end, generated_at_utc)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.output_md.write_text(markdown(index), encoding="utf-8")
    print(json.dumps(index["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
