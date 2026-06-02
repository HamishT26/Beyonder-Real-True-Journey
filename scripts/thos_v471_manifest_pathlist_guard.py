#!/usr/bin/env python3
"""Validate v471 THOS manifest/path-list pairs and build v6 approval artifacts."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE_X1 = "v471-thos-v6-x1"
PHASE_X2 = "v471-thos-v6-x2"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

APP_REQUESTS = [
    {
        "lane": "Cicero",
        "submission_id": "019e882a-92eb-7b20-bc12-a3160a1cc1fe",
        "status": "REQUEST_SENT",
    },
    {
        "lane": "Kierkegaard",
        "submission_id": "019e882a-9310-7692-bc4d-8538989c9de1",
        "status": "REQUEST_SENT",
    },
    {
        "lane": "Aristotle",
        "submission_id": "019e882a-9316-7303-9192-0ce991d38aae",
        "status": "REQUEST_SENT",
    },
]

HEX_64 = re.compile(r"^[0-9a-f]{64}$")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def path_is_relative_safe(value: str) -> bool:
    return not (
        value.startswith("/")
        or value.startswith("\\")
        or re.match(r"^[A-Za-z]:[\\/]", value)
        or ".." in Path(value).parts
    )


def validate_manifest_pair(manifest: dict[str, Any], path_list: dict[str, Any]) -> dict[str, Any]:
    skills = manifest.get("skills", [])
    relative_paths = path_list.get("relative_paths", [])
    rows: list[dict[str, Any]] = []
    failures: list[str] = []

    manifest_paths = [item.get("relative_path") for item in skills]
    if len(skills) != manifest.get("affected_count"):
        failures.append("MANIFEST_COUNT_FIELD_MISMATCH")
    if len(relative_paths) != len(manifest_paths):
        failures.append("PATH_LIST_COUNT_MISMATCH")
    if sorted(relative_paths) != sorted(manifest_paths):
        failures.append("PATH_LIST_CONTENT_MISMATCH")

    duplicate_paths = sorted({value for value in manifest_paths if manifest_paths.count(value) > 1})
    if duplicate_paths:
        failures.append("MANIFEST_PATH_DUPLICATE")
    case_map: dict[str, list[str]] = {}
    for value in manifest_paths:
        if isinstance(value, str):
            case_map.setdefault(value.lower(), []).append(value)
    case_collisions = {key: values for key, values in case_map.items() if len(set(values)) > 1}
    if case_collisions:
        failures.append("MANIFEST_PATH_CASE_COLLISION")

    unsafe_paths = [value for value in manifest_paths if not isinstance(value, str) or not path_is_relative_safe(value)]
    if unsafe_paths:
        failures.append("MANIFEST_PATH_UNSAFE")
    unsafe_path_list = [value for value in relative_paths if not isinstance(value, str) or not path_is_relative_safe(value)]
    if unsafe_path_list:
        failures.append("PATH_LIST_PATH_UNSAFE")

    missing_hash_rows = [
        item.get("relative_path")
        for item in skills
        if not isinstance(item.get("sha256_before"), str) or not HEX_64.match(item["sha256_before"])
    ]
    if missing_hash_rows:
        failures.append("MANIFEST_SHA256_MISSING_OR_INVALID")

    missing_path_id = [
        item.get("relative_path")
        for item in skills
        if not isinstance(item.get("path_id"), str) or not item["path_id"]
    ]
    if missing_path_id:
        failures.append("MANIFEST_PATH_ID_MISSING")

    mutation_rows = [
        item.get("relative_path")
        for item in skills
        if item.get("mutation_status") != "none"
    ]
    if mutation_rows:
        failures.append("MANIFEST_MUTATION_STATUS_NOT_NONE")

    rows.extend(
        [
            row("count_equality", "PASS_SHAPE_ONLY" if "PATH_LIST_COUNT_MISMATCH" not in failures and "MANIFEST_COUNT_FIELD_MISMATCH" not in failures else "FAIL_BLOCKER", "Manifest affected count and path-list count must match", {"manifest_count": len(manifest_paths), "path_list_count": len(relative_paths), "affected_count": manifest.get("affected_count")}),
            row("path_content_match", "PASS_SHAPE_ONLY" if "PATH_LIST_CONTENT_MISMATCH" not in failures else "FAIL_BLOCKER", "Path-list must equal manifest relative paths as a closed-world set"),
            row("duplicate_guard", "PASS_SHAPE_ONLY" if not duplicate_paths else "FAIL_BLOCKER", "Manifest paths must not duplicate", duplicate_paths),
            row("case_collision_guard", "PASS_SHAPE_ONLY" if not case_collisions else "FAIL_BLOCKER", "Manifest paths must not collide by case", case_collisions),
            row("path_safety_guard", "PASS_SHAPE_ONLY" if not unsafe_paths and not unsafe_path_list else "FAIL_BLOCKER", "Paths must be relative and non-escaping", {"manifest": unsafe_paths, "path_list": unsafe_path_list}),
            row("checksum_guard", "PASS_SHAPE_ONLY" if not missing_hash_rows else "FAIL_BLOCKER", "Every manifest row needs a 64-character sha256_before", missing_hash_rows),
            row("path_id_guard", "PASS_SHAPE_ONLY" if not missing_path_id else "FAIL_BLOCKER", "Every manifest row needs a path_id", missing_path_id),
            row("mutation_guard", "PASS_SHAPE_ONLY" if not mutation_rows else "FAIL_BLOCKER", "Every manifest row must keep mutation_status none", mutation_rows),
        ]
    )
    return {
        "aggregate_status": "FAIL_BLOCKER" if failures else "PASS_SHAPE_ONLY",
        "failure_codes": sorted(set(failures)),
        "rows": rows,
    }


def build_diff_packet_template(manifest: dict[str, Any]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for item in manifest.get("skills", []):
        entries.append(
            {
                "approval_status": "NOT_APPROVED",
                "candidate_name": item.get("candidate_name"),
                "entry_id": item.get("path_id"),
                "proposed_action": "body_preserving_frontmatter_prefix_repair",
                "relative_path": item.get("relative_path"),
                "requires_exact_diff_review": True,
                "requires_live_write_approval": True,
                "sha256_before": item.get("sha256_before"),
                "write_performed": False,
            }
        )
    return {
        "diff_packet_mode": "future_approval_template_only",
        "entry_count": len(entries),
        "entries": entries,
        "live_write_authorized": False,
        "live_write_performed": False,
    }


def write_artifacts(
    output_root: Path,
    manifest: dict[str, Any],
    path_list: dict[str, Any],
    validation: dict[str, Any],
    diff_packet: dict[str, Any],
) -> list[str]:
    written: list[str] = []

    guard_payload = {
        "aggregate_status": validation["aggregate_status"],
        "failure_codes": validation["failure_codes"],
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": validation["rows"],
    }
    path = output_root / f"{PHASE_X1}-manifest-pathlist-guard-v1.json"
    write_json(path, guard_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X1}-manifest-pathlist-guard-v1.md",
        f"""
# v471 THOS v6 x1 Manifest Path-List Guard

Status: `{validation["aggregate_status"]}`.

The guard validates the v5 affected manifest against the v5 affected path list as a closed-world pair: count equality, content equality, duplicate paths, case collisions, relative path safety, checksum presence, path ID presence, and mutation status.

This proves manifest/path-list consistency only. It does not repair plugin cache, authorize live writes, restore CLI sibling health, or prove Browser availability.
""",
    )
    written.append((output_root / f"{PHASE_X1}-manifest-pathlist-guard-v1.md").as_posix())

    diff_payload = {
        "aggregate_status": "OPEN_GAP",
        "diff_packet": diff_packet,
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("template_created", "PASS_SHAPE_ONLY", "Future approval diff-packet template was created", {"entry_count": diff_packet["entry_count"]}),
            row("live_write_authorization", "OPEN_GAP", "Live plugin-cache write is not authorized by this template"),
            row("exact_diff_review", "OPEN_GAP", "A future phase must include exact repaired content diff before approval"),
        ],
    }
    path = output_root / f"{PHASE_X1}-future-diff-packet-template-v1.json"
    write_json(path, diff_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X1}-future-diff-packet-template-v1.md",
        """
# v471 THOS v6 x1 Future Diff-Packet Template

This template lists future body-preserving frontmatter-prefix repair entries as `NOT_APPROVED` and `write_performed: false`.

It is not an approval and not a live edit. A later phase would still need exact repaired content, body-preservation proof, rollback plan, path-specific approval, and post-write verification before touching plugin-cache files.
""",
    )
    written.append((output_root / f"{PHASE_X1}-future-diff-packet-template-v1.md").as_posix())

    run_payload = {
        "aggregate_status": "OPEN_GAP" if validation["aggregate_status"] == "PASS_SHAPE_ONLY" else "FAIL_BLOCKER",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("app_requests", "PASS_SHAPE_ONLY", "Existing app lanes were messaged for v6 advisory", APP_REQUESTS),
            row("manifest_guard", validation["aggregate_status"], "Manifest/path-list guard executed", validation["failure_codes"]),
            row("diff_packet", "OPEN_GAP", "Future diff-packet remains approval-gated", {"entry_count": diff_packet["entry_count"]}),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = output_root / f"{PHASE_X1}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X1}-run-status-v1.md",
        """
# v471 THOS v6 x1 Run Status

v6 x1 executed a closed-world manifest/path-list guard and created a future diff-packet template. No live plugin-cache file was edited.

Publication is deferred to x2 under the paired-phase cadence.
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
            row("x2_task_1", "OPEN_GAP", "Publish guard claim ceiling"),
            row("x2_task_2", "OPEN_GAP", "Publish future approval criteria and no-write boundary"),
            row("x2_task_3", "OPEN_GAP", "Publish v7 handoff for exact diff rehearsal or Browser/CLI retry"),
        ],
    }
    path = output_root / f"{PHASE_X1}-x2-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X1}-x2-handoff-v1.md",
        """
# v471 THOS v6 x1 To x2 Handoff

x2 should publish the guard claim ceiling and future approval criteria. The x2 closeout must not claim plugin-cache repair or authorization.
""",
    )
    written.append((output_root / f"{PHASE_X1}-x2-handoff-v1.md").as_posix())

    claim_payload = {
        "aggregate_status": "OPEN_GAP" if validation["aggregate_status"] == "PASS_SHAPE_ONLY" else "FAIL_BLOCKER",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("guard_claim", validation["aggregate_status"], "May claim manifest/path-list guard result only"),
            row("diff_packet_claim", "OPEN_GAP", "May claim future template only, not approval or repair"),
            row("live_cache_repair", "OPEN_GAP", "No live plugin-cache repair occurred"),
            row("browser_cli", "OPEN_GAP", "Browser and CLI blockers remain open unless separately verified"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = output_root / f"{PHASE_X2}-guard-claim-ceiling-v1.json"
    write_json(path, claim_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X2}-guard-claim-ceiling-v1.md",
        """
# v471 THOS v6 x2 Guard Claim Ceiling

This phase may claim only that the v5 manifest/path-list pair was checked by a closed-world guard and that a future diff-packet template exists.

It may not claim live plugin-cache repair, write authorization, restored CLI sibling health, Browser direct availability, or any GMUT gate closure.
""",
    )
    written.append((output_root / f"{PHASE_X2}-guard-claim-ceiling-v1.md").as_posix())

    approval_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("required_approval_item_1", "OPEN_GAP", "Exact path-specific approval for each live cache file"),
            row("required_approval_item_2", "OPEN_GAP", "Exact body-preserving diff content and rollback plan"),
            row("required_approval_item_3", "OPEN_GAP", "Post-write verification plan and CLI retry criteria"),
            row("current_phase_boundary", "PASS_SHAPE_ONLY", "This phase performs none of those live-write actions"),
        ],
    }
    path = output_root / f"{PHASE_X2}-future-approval-criteria-v1.json"
    write_json(path, approval_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X2}-future-approval-criteria-v1.md",
        """
# v471 THOS v6 x2 Future Approval Criteria

Future live plugin-cache repair would need exact paths, exact repaired content, rollback plan, post-write verification, and path-specific approval. The current phase does not supply approval and does not perform a live write.
""",
    )
    written.append((output_root / f"{PHASE_X2}-future-approval-criteria-v1.md").as_posix())

    run_payload = {
        "aggregate_status": "OPEN_GAP" if validation["aggregate_status"] == "PASS_SHAPE_ONLY" else "FAIL_BLOCKER",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("x1_x2_pair", "OPEN_GAP", "v6 published guard and approval-boundary artifacts"),
            row("guard", validation["aggregate_status"], "Manifest/path-list closed-world guard result"),
            row("future_approval", "OPEN_GAP", "Live cache repair remains approval-gated"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = output_root / f"{PHASE_X2}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X2}-run-status-v1.md",
        """
# v471 THOS v6 x2 Run Status

Status: `OPEN_GAP`.

v6 published the manifest/path-list guard, future diff-packet template, guard claim ceiling, and approval criteria. It did not mutate plugin cache or external systems.
""",
    )
    written.append((output_root / f"{PHASE_X2}-run-status-v1.md").as_posix())

    handoff_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": "v471-thos-v7-x1",
        "phase_slug": PHASE_X2,
        "rows": [
            row("v7_task_1", "OPEN_GAP", "Option A: generate exact repaired-content diff preview in tempdir only"),
            row("v7_task_2", "OPEN_GAP", "Option B: retry Browser direct capability if iab surface becomes available"),
            row("v7_task_3", "OPEN_GAP", "Option C: retry one CLI sibling after skill-surface stability improves"),
            row("v7_task_4", "OPEN_GAP", "Keep GMUT and Journey canon boundaries open"),
        ],
    }
    path = output_root / f"{PHASE_X2}-v471-thos-v7-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X2}-v471-thos-v7-handoff-v1.md",
        """
# v471 THOS v6 x2 To v7 Handoff

v7 should either build an exact repaired-content diff preview in tempdir only, retry Browser if the `iab` surface becomes available, or retry one CLI sibling if the skill surface is stable enough. Do not live-edit plugin cache without path-specific approval.
""",
    )
    written.append((output_root / f"{PHASE_X2}-v471-thos-v7-handoff-v1.md").as_posix())

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate v471 THOS manifest/path-list pairs and build v6 approval artifacts.")
    parser.add_argument("--manifest", default="docs/trinity-live-traces/v471-thos-v5-x1-plugin-cache-affected-manifest-v1.json")
    parser.add_argument("--path-list", default="docs/trinity-live-traces/v471-thos-v5-x2-affected-path-list-v1.json")
    parser.add_argument("--output-dir", default="docs/trinity-live-traces")
    args = parser.parse_args()

    manifest = read_json(Path(args.manifest))
    path_list = read_json(Path(args.path_list))
    validation = validate_manifest_pair(manifest, path_list)
    diff_packet = build_diff_packet_template(manifest)
    written = write_artifacts(Path(args.output_dir), manifest, path_list, validation, diff_packet)
    print(json.dumps({"guard_status": validation["aggregate_status"], "diff_packet_entries": diff_packet["entry_count"], "written": written}, indent=2, sort_keys=True))
    return 0 if validation["aggregate_status"] == "PASS_SHAPE_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
