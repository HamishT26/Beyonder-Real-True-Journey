#!/usr/bin/env python3
"""Read-only Git index-stage guard for GHC-family manifests and staged reviews."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


HEADER = re.compile(rb"^(?P<mode>[0-7]{6}) (?P<oid>[0-9a-fA-F]{40}|[0-9a-fA-F]{64}) (?P<stage>[0-3])$")


def parse_stage_records(data: bytes) -> list[dict[str, Any]]:
    """Parse NUL-delimited ``git ls-files --stage -z`` bytes without path decoding."""

    if not data:
        return []
    if not data.endswith(b"\0"):
        raise ValueError("stage stream is not NUL terminated")
    rows: list[dict[str, Any]] = []
    for ordinal, record in enumerate(data[:-1].split(b"\0"), 1):
        if b"\t" not in record:
            raise ValueError(f"record {ordinal} has no tab separator")
        header, path = record.split(b"\t", 1)
        match = HEADER.fullmatch(header)
        if not match:
            raise ValueError(f"record {ordinal} has malformed mode, object id, or stage")
        if not path:
            raise ValueError(f"record {ordinal} has an empty path")
        rows.append(
            {
                "ordinal": ordinal,
                "mode": match.group("mode").decode("ascii"),
                "object_id": match.group("oid").decode("ascii").lower(),
                "stage": int(match.group("stage")),
                "path_bytes_hex": path.hex(),
                "path_display": path.decode("utf-8", errors="backslashreplace"),
            }
        )
    return rows


def classify_stage_bytes(data: bytes) -> dict[str, Any]:
    """Return a deterministic refusal result; never mutate the index or worktree."""

    try:
        rows = parse_stage_records(data)
    except ValueError as error:
        return {
            "accepted": False,
            "classification": "malformed_stage_stream",
            "record_count": 0,
            "higher_stage_count": 0,
            "multiplicity_path_count": 0,
            "issues": [str(error)],
            "rows": [],
            "index_mutation_count": 0,
        }

    stages = Counter(row["stage"] for row in rows)
    paths = Counter(row["path_bytes_hex"] for row in rows)
    higher = [row for row in rows if row["stage"] != 0]
    multiplicity = sorted(path for path, count in paths.items() if count > 1)
    issues = []
    if higher:
        issues.append("one or more unresolved higher-stage entries exist")
    if multiplicity:
        issues.append("one or more paths have index-stage multiplicity")
    accepted = not issues
    return {
        "accepted": accepted,
        "classification": "stage_zero_only" if accepted else "unresolved_index_refused",
        "record_count": len(rows),
        "stage_counts": {str(key): value for key, value in sorted(stages.items())},
        "higher_stage_count": len(higher),
        "multiplicity_path_count": len(multiplicity),
        "multiplicity_path_hex": multiplicity,
        "issues": issues,
        "rows": rows,
        "index_mutation_count": 0,
    }


def inspect_repository(repo: Path) -> dict[str, Any]:
    before = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "--stage", "-z"],
        check=True,
        capture_output=True,
    ).stdout
    after = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "--stage", "-z"],
        check=True,
        capture_output=True,
    ).stdout
    result = classify_stage_bytes(before)
    before_digest = hashlib.sha256(before).hexdigest()
    after_digest = hashlib.sha256(after).hexdigest()
    result.update(
        {
            "index_stream_sha256_before": before_digest,
            "index_stream_sha256_after": after_digest,
            "index_stream_unchanged": before == after,
            "command_surface": "git ls-files --stage -z",
            "read_only": True,
            "boundary": "Acceptance proves only that the observed index stream parsed and contained stage-zero entries; it is not conflict resolution, exhaustive repository assurance, or authorization to mutate state.",
        }
    )
    if not result["index_stream_unchanged"]:
        result["accepted"] = False
        result["issues"].append("index stage stream was not stable across inspection")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = inspect_repository(args.repo.resolve())
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
