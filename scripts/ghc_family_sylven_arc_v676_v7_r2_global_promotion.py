#!/usr/bin/env python3
"""Promote the five validated Sylven v676-v7-r2 skills without overwrites."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


PROMOTED = (
    "metadata-minimization-ledger",
    "freed-id-four-tier-deck",
    "content-addressed-flashcard-index",
    "flashcard-supersession-nonerasure",
    "gmut-book-metadata-analogy-firewall",
)


def digest_tree(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--global-root", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    global_root = args.global_root.resolve()
    local_root = repo / "docs/sylven-arc/v676-v7-r2/x2/skills"
    validation_path = repo / "docs/sylven-arc/v676-v7-r2/x2/skill-validation-receipt.json"
    receipt_path = repo / "docs/sylven-arc/v676-v7-r2/x2/global-promotion-receipt.json"

    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    positive = {row["skill"]: row for row in validation["positive"]}
    rejecting = {row["skill"]: row for row in validation["rejecting"]}
    rows: list[dict[str, object]] = []

    for name in PROMOTED:
        source = local_root / name
        destination = global_root / name
        if not source.is_dir() or not (source / "SKILL.md").is_file():
            raise SystemExit(f"missing validated source skill: {name}")
        if "TODO" in (source / "SKILL.md").read_text(encoding="utf-8"):
            raise SystemExit(f"unresolved skill template marker: {name}")
        if not positive.get(name, {}).get("quick_validate_passed"):
            raise SystemExit(f"missing quick-validation pass: {name}")
        if positive[name]["smoke"].get("accepted") is not True:
            raise SystemExit(f"missing positive smoke: {name}")
        if rejecting.get(name, {}).get("accepted") is not False:
            raise SystemExit(f"missing rejecting smoke: {name}")

        source_hashes = digest_tree(source)
        if destination.exists():
            destination_hashes = digest_tree(destination)
            if destination_hashes != source_hashes:
                raise SystemExit(f"collision without byte parity: {name}")
            disposition = "already_present_byte_equal"
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, destination)
            destination_hashes = digest_tree(destination)
            if destination_hashes != source_hashes:
                raise SystemExit(f"post-copy byte mismatch: {name}")
            disposition = "promoted_byte_equal"

        rows.append(
            {
                "skill": name,
                "disposition": disposition,
                "file_count": len(source_hashes),
                "source_tree_digest": hashlib.sha256(
                    json.dumps(source_hashes, sort_keys=True, separators=(",", ":")).encode("utf-8")
                ).hexdigest(),
                "destination_tree_digest": hashlib.sha256(
                    json.dumps(destination_hashes, sort_keys=True, separators=(",", ":")).encode("utf-8")
                ).hexdigest(),
                "byte_parity": True,
            }
        )

    receipt = {
        "schema": "ghc-family-global-skill-promotion-receipt/v1",
        "phase": "v676-v7-r2",
        "promoted_count": len(rows),
        "collision_policy": "fail_on_nonidentical_existing_destination",
        "validation_required": "quick_validate_plus_accepting_and_rejecting_smoke",
        "global_root_token": "CODEX_GLOBAL_SKILL_ROOT",
        "rows": rows,
        "rollback": "disable or supersede additively; do not destructively delete without new exact authority",
        "bounded_software_evidence_only": True,
    }
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PROMOTED_OR_CONFIRMED", "count": len(rows)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
