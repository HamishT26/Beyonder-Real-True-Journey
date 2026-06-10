#!/usr/bin/env python3
"""Build v471 THOS v7 tempdir-only repaired-content diff preview artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE_X1 = "v471-thos-v7-x1"
PHASE_X2 = "v471-thos-v7-x2"
MAX_SKILL_NAME_LENGTH = 64

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

APP_REQUESTS = [
    {"lane": "Cicero", "submission_id": "019e882f-fdc2-7230-aa7e-f9b446f9a27d", "status": "REQUEST_SENT"},
    {"lane": "Kierkegaard", "submission_id": "019e882f-fe07-7f63-b61a-1bd0ef4f72a4", "status": "REQUEST_SENT"},
    {"lane": "Aristotle", "submission_id": "019e882f-fe0a-7e73-b98d-d5108a280ded", "status": "REQUEST_SENT"},
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def safe_skill_name(seed: str, relative_path: str) -> str:
    stem = re.sub(r"[^a-zA-Z0-9_-]+", "-", seed.strip().lower()).strip("-")
    if not stem:
        stem = "plugin-cache-skill"
    if len(stem) <= MAX_SKILL_NAME_LENGTH:
        return stem
    digest = hashlib.sha256(relative_path.encode("utf-8")).hexdigest()[:8]
    return f"{stem[:MAX_SKILL_NAME_LENGTH - 9]}-{digest}"


def parse_frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].lstrip("\ufeff").strip() != "---":
        return {"description": None, "has_frontmatter": False, "malformed": False, "name": None}
    closing_index = None
    for index, line in enumerate(lines[1:], 1):
        if line.lstrip("\ufeff").strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        return {"description": None, "has_frontmatter": False, "malformed": True, "name": None}
    values: dict[str, str] = {}
    for line in lines[1:closing_index]:
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"').strip("'")
    return {
        "description": values.get("description"),
        "has_frontmatter": True,
        "malformed": False,
        "name": values.get("name"),
    }


def frontmatter_valid(text: str) -> bool:
    parsed = parse_frontmatter(text)
    return bool(parsed.get("has_frontmatter") and parsed.get("name") and parsed.get("description"))


def path_safe(value: str) -> bool:
    return not (
        value.startswith("/")
        or value.startswith("\\")
        or re.match(r"^[A-Za-z]:[\\/]", value)
        or ".." in Path(value).parts
    )


def build_candidate(relative_path: str, original_text: str, candidate_name: str) -> tuple[str, dict[str, str]]:
    proposed_frontmatter = {
        "name": candidate_name,
        "description": f"Body-preserving tempdir-only frontmatter repair candidate for {candidate_name}.",
    }
    prefix = (
        "---\n"
        f"name: {proposed_frontmatter['name']}\n"
        f"description: {proposed_frontmatter['description']}\n"
        "---\n\n"
        "<!-- THOS tempdir-only diff preview; original body follows unchanged. -->\n\n"
    )
    return prefix + original_text, proposed_frontmatter


def build_preview(manifest: dict[str, Any], plugin_cache_root: Path) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="thos-v471-diff-preview-") as temp_root:
        temp_root_path = Path(temp_root)
        for item in manifest.get("skills", []):
            relative_path = item["relative_path"]
            source_path = plugin_cache_root / relative_path
            before_text = read_text(source_path)
            before_hash = hash_text(before_text)
            candidate_name = safe_skill_name(item.get("candidate_name") or item.get("skill_dir") or "plugin-cache-skill", relative_path)
            after_text, proposed_frontmatter = build_candidate(relative_path, before_text, candidate_name)
            target = temp_root_path / item["path_id"] / "SKILL.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(after_text, encoding="utf-8")
            source_after_hash = hash_text(read_text(source_path))
            body_preserved = after_text.endswith(before_text)
            entries.append(
                {
                    "after_hash": hash_text(after_text),
                    "approval_status": "NOT_APPROVED",
                    "before_hash": before_hash,
                    "body_preserved_in_temp_candidate": body_preserved,
                    "candidate_frontmatter_valid": frontmatter_valid(after_text),
                    "entry_id": item["path_id"],
                    "line_delta": len(after_text.splitlines()) - len(before_text.splitlines()),
                    "path_safe": path_safe(relative_path),
                    "proposed_frontmatter": proposed_frontmatter,
                    "relative_path": relative_path,
                    "source_checksum_unchanged": before_hash == source_after_hash == item.get("sha256_before"),
                    "write_target": "tempdir_only",
                    "write_performed": False,
                }
            )
    failures = [
        entry
        for entry in entries
        if not entry["body_preserved_in_temp_candidate"]
        or not entry["candidate_frontmatter_valid"]
        or not entry["path_safe"]
        or not entry["source_checksum_unchanged"]
        or entry["write_performed"]
        or entry["approval_status"] != "NOT_APPROVED"
    ]
    return {
        "aggregate_status": "FAIL_BLOCKER" if failures else "PASS_SHAPE_ONLY",
        "entry_count": len(entries),
        "failure_count": len(failures),
        "entries": entries,
        "preview_mode": "tempdir_only_redacted_diff_metadata",
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_artifacts(output_root: Path, preview: dict[str, Any]) -> list[str]:
    written: list[str] = []

    preview_payload = {
        "aggregate_status": preview["aggregate_status"],
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "preview": preview,
        "rows": [
            row("tempdir_only", "PASS_SHAPE_ONLY", "Candidate files were written only in a temporary directory"),
            row("preview_validation", preview["aggregate_status"], "Diff-preview metadata validations completed", {"entry_count": preview["entry_count"], "failure_count": preview["failure_count"]}),
            row("raw_body_publication", "PASS_SHAPE_ONLY", "No raw plugin body text is included in curated artifacts"),
            row("live_write", "OPEN_GAP", "No live plugin-cache write occurred"),
        ],
    }
    path = output_root / f"{PHASE_X1}-tempdir-diff-preview-v1.json"
    write_json(path, preview_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X1}-tempdir-diff-preview-v1.md",
        f"""
# v471 THOS v7 x1 Tempdir Diff Preview

Status: `{preview["aggregate_status"]}`.

The preview generated `{preview["entry_count"]}` body-preserving candidate files in a temporary directory. Curated artifacts include relative paths, proposed frontmatter, before/after hashes, line deltas, and validation booleans only. They do not include raw plugin bodies and do not modify plugin-cache files.
""",
    )
    written.append((output_root / f"{PHASE_X1}-tempdir-diff-preview-v1.md").as_posix())

    approval_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("app_requests", "PASS_SHAPE_ONLY", "Existing app lanes were messaged for v7 advisory", APP_REQUESTS),
            row("approval_packet_needed", "OPEN_GAP", "Live repair still requires exact path-specific approval"),
            row("rollback_needed", "OPEN_GAP", "Future live write packet must include rollback plan and post-write verification"),
            row("claim_ceiling", "PASS_SHAPE_ONLY", "This preview is readiness evidence only"),
        ],
    }
    path = output_root / f"{PHASE_X1}-approval-delta-ledger-v1.json"
    write_json(path, approval_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X1}-approval-delta-ledger-v1.md",
        """
# v471 THOS v7 x1 Approval Delta Ledger

The tempdir preview narrows the future approval packet, but it is not itself approval. A live repair would still need exact path-specific permission, rollback plan, and post-write verification.
""",
    )
    written.append((output_root / f"{PHASE_X1}-approval-delta-ledger-v1.md").as_posix())

    run_payload = {
        "aggregate_status": "OPEN_GAP" if preview["aggregate_status"] == "PASS_SHAPE_ONLY" else "FAIL_BLOCKER",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("diff_preview", preview["aggregate_status"], "Tempdir diff preview generated", {"entry_count": preview["entry_count"]}),
            row("live_write", "OPEN_GAP", "No live plugin-cache write occurred"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = output_root / f"{PHASE_X1}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X1}-run-status-v1.md",
        """
# v471 THOS v7 x1 Run Status

v7 x1 generated a privacy-safe tempdir diff preview. Publication is deferred to x2 under the paired-phase cadence.
""",
    )
    written.append((output_root / f"{PHASE_X1}-run-status-v1.md").as_posix())

    handoff_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": PHASE_X2,
        "phase_slug": PHASE_X1,
        "rows": [
            row("x2_task_1", "OPEN_GAP", "Publish diff-preview claim ceiling"),
            row("x2_task_2", "OPEN_GAP", "Publish v8 handoff for closure audit or bounded retry"),
        ],
    }
    path = output_root / f"{PHASE_X1}-x2-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X1}-x2-handoff-v1.md",
        """
# v471 THOS v7 x1 To x2 Handoff

x2 should publish the claim ceiling and v8 handoff. Do not convert this preview into live cache mutation.
""",
    )
    written.append((output_root / f"{PHASE_X1}-x2-handoff-v1.md").as_posix())

    claim_payload = {
        "aggregate_status": "OPEN_GAP" if preview["aggregate_status"] == "PASS_SHAPE_ONLY" else "FAIL_BLOCKER",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("preview_claim", preview["aggregate_status"], "May claim tempdir-only diff metadata preview result"),
            row("privacy_claim", "PASS_SHAPE_ONLY", "May claim no raw plugin bodies in curated artifacts"),
            row("repair_claim", "OPEN_GAP", "May not claim live plugin-cache repair"),
            row("browser_cli_claim", "OPEN_GAP", "May not claim Browser or CLI blockers fixed"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = output_root / f"{PHASE_X2}-diff-preview-claim-ceiling-v1.json"
    write_json(path, claim_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X2}-diff-preview-claim-ceiling-v1.md",
        """
# v471 THOS v7 x2 Diff Preview Claim Ceiling

This phase may claim only tempdir-only diff metadata readiness. It may not claim live plugin-cache repair, write approval, Browser availability, CLI recovery, or GMUT gate closure.
""",
    )
    written.append((output_root / f"{PHASE_X2}-diff-preview-claim-ceiling-v1.md").as_posix())

    run_payload = {
        "aggregate_status": "OPEN_GAP" if preview["aggregate_status"] == "PASS_SHAPE_ONLY" else "FAIL_BLOCKER",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("x1_x2_pair", "OPEN_GAP", "v7 published diff-preview readiness artifacts"),
            row("preview", preview["aggregate_status"], "Tempdir diff preview validation result"),
            row("live_write", "OPEN_GAP", "No live cache write occurred"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = output_root / f"{PHASE_X2}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X2}-run-status-v1.md",
        """
# v471 THOS v7 x2 Run Status

Status: `OPEN_GAP`.

v7 published a privacy-safe tempdir diff-preview packet and claim ceiling. It did not mutate plugin cache or external systems.
""",
    )
    written.append((output_root / f"{PHASE_X2}-run-status-v1.md").as_posix())

    handoff_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": "v471-thos-v8-x1",
        "phase_slug": PHASE_X2,
        "rows": [
            row("v8_task_1", "OPEN_GAP", "Audit v471 THOS v4-v7 closure boundaries"),
            row("v8_task_2", "OPEN_GAP", "Optionally retry Browser if iab becomes available"),
            row("v8_task_3", "OPEN_GAP", "Optionally prepare explicit live-write approval packet, without executing it"),
            row("v8_task_4", "OPEN_GAP", "Keep GMUT gates open"),
        ],
    }
    path = output_root / f"{PHASE_X2}-v471-thos-v8-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X2}-v471-thos-v8-handoff-v1.md",
        """
# v471 THOS v7 x2 To v8 Handoff

v8 should audit the v4-v7 THOS recovery chain and decide whether to prepare a specific live-write approval packet. It should not execute live plugin-cache repair without fresh path-specific approval.
""",
    )
    written.append((output_root / f"{PHASE_X2}-v471-thos-v8-handoff-v1.md").as_posix())

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Build v471 THOS v7 tempdir-only repaired-content diff preview artifacts.")
    parser.add_argument("--manifest", default="docs/trinity-live-traces/v471-thos-v5-x1-plugin-cache-affected-manifest-v1.json")
    parser.add_argument("--plugin-cache-root", default=str(Path.home() / ".codex" / "plugins" / "cache"))
    parser.add_argument("--output-dir", default="docs/trinity-live-traces")
    args = parser.parse_args()

    manifest = read_json(Path(args.manifest))
    preview = build_preview(manifest, Path(args.plugin_cache_root))
    written = write_artifacts(Path(args.output_dir), preview)
    print(json.dumps({"preview_status": preview["aggregate_status"], "entry_count": preview["entry_count"], "written": written}, indent=2, sort_keys=True))
    return 0 if preview["aggregate_status"] == "PASS_SHAPE_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
