#!/usr/bin/env python3
"""Build v471 THOS v8 closure audit and v472 handoff artifacts."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE_X1 = "v471-thos-v8-x1"
PHASE_X2 = "v471-thos-v8-x2"

APP_REQUESTS = [
    {"lane": "Cicero", "submission_id": "019e8835-07df-76d0-9898-6c4a8bc60b0a", "status": "REQUEST_SENT"},
    {"lane": "Kierkegaard", "submission_id": "019e8835-0832-7d40-91de-cfbed9eb06b2", "status": "REQUEST_SENT"},
    {"lane": "Aristotle", "submission_id": "019e8835-0834-75e2-bf02-9e8919e2f1be", "status": "REQUEST_SENT"},
]

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]


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


def git_value(args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "UNKNOWN"


def build_summary(root: Path) -> dict[str, Any]:
    v4_run = read_json(root / "v471-thos-v4-x2-run-status-v1.json")
    v5_manifest = read_json(root / "v471-thos-v5-x1-plugin-cache-affected-manifest-v1.json")
    v5_rehearsal = read_json(root / "v471-thos-v5-x1-tempdir-repair-rehearsal-v1.json")
    v6_guard = read_json(root / "v471-thos-v6-x1-manifest-pathlist-guard-v1.json")
    v7_preview = read_json(root / "v471-thos-v7-x1-tempdir-diff-preview-v1.json")
    return {
        "browser_status": "OPEN_GAP",
        "cli_status": "OPEN_GAP",
        "current_head": git_value(["rev-parse", "HEAD"]),
        "gmut_gates": GMUT_GATES,
        "live_plugin_cache_repair": "OPEN_GAP",
        "plugin_cache": {
            "repair_candidate_count": v5_manifest.get("affected_count"),
            "legacy_head20_false_positive_count": len(v5_manifest.get("legacy_head20_false_positives", [])),
            "tempdir_rehearsal_status": v5_rehearsal.get("rehearsal", {}).get("aggregate_status"),
            "manifest_guard_status": v6_guard.get("aggregate_status"),
            "diff_preview_status": v7_preview.get("preview", {}).get("aggregate_status"),
            "diff_preview_entry_count": v7_preview.get("preview", {}).get("entry_count"),
            "diff_preview_failure_count": v7_preview.get("preview", {}).get("failure_count"),
        },
        "v4_run_status": v4_run.get("aggregate_status"),
    }


def write_artifacts(root: Path, summary: dict[str, Any]) -> list[str]:
    written: list[str] = []

    closure_rows = [
        row("browser", "OPEN_GAP", "Browser skill path was present, but direct iab surface remained unavailable"),
        row("cli_lanes", "OPEN_GAP", "Arby/Aster launches were bounded/read-only/non-ephemeral but did not return final advisories"),
        row("manifest_scope", "PASS_SHAPE_ONLY", "Plugin-cache affected manifest isolated 37 repair candidates and 5 legacy scanner false positives", summary["plugin_cache"]),
        row("tempdir_rehearsal", summary["plugin_cache"]["tempdir_rehearsal_status"], "Body-preserving tempdir repair rehearsal passed shape checks"),
        row("manifest_guard", summary["plugin_cache"]["manifest_guard_status"], "Manifest/path-list closed-world guard passed"),
        row("diff_preview", summary["plugin_cache"]["diff_preview_status"], "Privacy-safe tempdir diff preview passed"),
        row("live_repair", "OPEN_GAP", "No live plugin-cache write, repair, quarantine, or cleanup occurred"),
        row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
    ]
    closure_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": closure_rows,
        "summary": summary,
    }
    path = root / f"{PHASE_X1}-closure-audit-v1.json"
    write_json(path, closure_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-closure-audit-v1.md",
        """
# v471 THOS v8 x1 Closure Audit

Status: `OPEN_GAP`.

v471 THOS v4-v7 improved the recovery chain from blocker discovery to manifest, tempdir body-preserving rehearsal, closed-world guard, and privacy-safe diff preview. It did not repair plugin cache live, restore Browser direct access, restore CLI sibling final advisories, mutate external systems, or close any GMUT gate.
""",
    )
    written.append((root / f"{PHASE_X1}-closure-audit-v1.md").as_posix())

    contradiction_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("readiness_vs_repair", "PASS_SHAPE_ONLY", "Readiness evidence is explicitly separated from live repair"),
            row("permission_vs_approval", "PASS_SHAPE_ONLY", "Broad user permission is not treated as path-specific plugin-cache approval"),
            row("privacy_vs_exactness", "PASS_SHAPE_ONLY", "Diff preview records hashes/frontmatter/booleans, not raw plugin bodies"),
            row("source_vs_local_evidence", "PASS_SHAPE_ONLY", "Official docs and Journey context are not treated as proof of local success"),
            row("remaining_blockers", "OPEN_GAP", "Browser, CLI final advisory, live repair, rollback, post-write verification, and all GMUT gates remain open"),
        ],
    }
    path = root / f"{PHASE_X1}-contradiction-hunt-v1.json"
    write_json(path, contradiction_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-contradiction-hunt-v1.md",
        """
# v471 THOS v8 x1 Contradiction Hunt

The main contradiction risk is overclaiming readiness as repair. v8 keeps the boundary explicit: v4-v7 produced evidence and templates only. They did not authorize or perform live cache edits.
""",
    )
    written.append((root / f"{PHASE_X1}-contradiction-hunt-v1.md").as_posix())

    run_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("app_requests", "PASS_SHAPE_ONLY", "Existing app lanes were messaged for v8 audit", APP_REQUESTS),
            row("closure_audit", "OPEN_GAP", "v4-v7 closure audit completed with blockers preserved"),
            row("publication", "NOT_RUN", "Publication deferred to x2 under paired-phase cadence"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = root / f"{PHASE_X1}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-run-status-v1.md",
        """
# v471 THOS v8 x1 Run Status

x1 audited the v4-v7 THOS recovery chain and preserved open blockers. Publication is deferred to x2.
""",
    )
    written.append((root / f"{PHASE_X1}-run-status-v1.md").as_posix())

    x2_status = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("v471_closure", "OPEN_GAP", "v471 THOS closes as readiness/recovery evidence, not as blocker resolution"),
            row("browser", "OPEN_GAP", "Browser direct iab remains unavailable until live probe succeeds"),
            row("cli", "OPEN_GAP", "CLI sibling final advisory output remains unavailable until bounded probe returns final message"),
            row("plugin_cache", "OPEN_GAP", "Live plugin-cache repair remains unperformed and approval-gated"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = root / f"{PHASE_X2}-run-status-v1.json"
    write_json(path, x2_status)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-run-status-v1.md",
        """
# v471 THOS v8 x2 Run Status

Status: `OPEN_GAP`.

v471 THOS v4-v8 is publishable as a recovery/readiness chain with explicit open blockers. It is not a solved platform-health claim.
""",
    )
    written.append((root / f"{PHASE_X2}-run-status-v1.md").as_posix())

    handoff_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": "v472-thos-v1-x1",
        "phase_slug": PHASE_X2,
        "rows": [
            row("v472_task_1", "OPEN_GAP", "Decide whether to request explicit path-specific approval for live plugin-cache repair"),
            row("v472_task_2", "OPEN_GAP", "If not repairing, retry Browser direct capability or one CLI lane under bounded guard"),
            row("v472_task_3", "OPEN_GAP", "Extend THOS runner suite with no-raw-body and no-live-write regression fixtures"),
            row("v472_task_4", "OPEN_GAP", "Keep all GMUT gates open and avoid Journey/Solas canon promotion"),
        ],
    }
    path = root / f"{PHASE_X2}-v472-thos-v1-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-v472-thos-v1-handoff-v1.md",
        """
# v471 THOS v8 x2 To v472 THOS v1 Handoff

v472 should either ask for explicit path-specific approval for live plugin-cache repair, or stay non-mutating and focus on Browser/CLI retries plus regression fixtures. All GMUT gates remain open.
""",
    )
    written.append((root / f"{PHASE_X2}-v472-thos-v1-handoff-v1.md").as_posix())

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Build v471 THOS v8 closure audit artifacts.")
    parser.add_argument("--artifact-root", default="docs/trinity-live-traces")
    args = parser.parse_args()

    root = Path(args.artifact_root)
    summary = build_summary(root)
    written = write_artifacts(root, summary)
    print(json.dumps({"summary": summary, "written": written}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
