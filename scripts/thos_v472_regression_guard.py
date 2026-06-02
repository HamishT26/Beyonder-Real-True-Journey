#!/usr/bin/env python3
"""Build v472 THOS v1 regression guard artifacts for plugin/Browser/CLI recovery."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE_X1 = "v472-thos-v1-x1"
PHASE_X2 = "v472-thos-v1-x2"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

APP_REQUESTS = [
    {"lane": "Cicero", "submission_id": "019e883c-9ed0-7b23-8d5a-79895bc1bb59", "status": "REQUEST_SENT"},
    {"lane": "Kierkegaard", "submission_id": "019e883c-9da5-7352-9af2-0781250b04aa", "status": "REQUEST_SENT"},
    {"lane": "Aristotle", "submission_id": "019e883c-9fd1-7061-9e4e-4b75e86f1302", "status": "REQUEST_SENT"},
]

CLI_PROBES = [
    {
        "lane": "Arby",
        "completed_within_wait": False,
        "ephemeral_flag_used": False,
        "last_message_bytes": 0,
        "sandbox": "read-only",
        "stderr_signal": "system skill install access denied plus missing YAML frontmatter skill-load failures",
        "terminated_after_timeout": True,
    },
    {
        "lane": "Aster Vale",
        "completed_within_wait": False,
        "ephemeral_flag_used": False,
        "last_message_bytes": 0,
        "sandbox": "read-only",
        "stderr_signal": "missing YAML frontmatter skill-load failures",
        "terminated_after_timeout": True,
    },
]

BROWSER_PROBE = {
    "attempt": "v472 bounded retry",
    "direct_browser_usable": False,
    "signal": "Browser is not available: iab",
    "status": "OPEN_GAP",
}

SOURCE_ROUTES = [
    {
        "label": "OpenAI Academy - Codex plugins and skills",
        "url": "https://openai.com/academy/codex-plugins-and-skills",
        "use": "Primary OpenAI context for plugins vs skills and repeatable task playbooks.",
    },
    {
        "label": "OpenAI Help - Codex CLI getting started",
        "url": "https://help.openai.com/en/articles/11096431",
        "use": "Primary OpenAI context for Codex CLI sandbox and approval modes.",
    },
    {
        "label": "OpenAI MCP docs",
        "url": "https://platform.openai.com/docs/mcp/",
        "use": "Primary OpenAI context for MCP safety and prompt-injection boundaries.",
    },
    {
        "label": "OpenAI - Introducing the Codex app",
        "url": "https://openai.com/index/introducing-the-codex-app/",
        "use": "Primary OpenAI context for Codex app skills and delegated workflows.",
    },
]

RAW_BODY_FIELD_RE = re.compile(r"(body_text|original_text|after_text|before_text|raw_body|plugin_body)", re.IGNORECASE)


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


def path_safe(value: str) -> bool:
    return not (
        value.startswith("/")
        or value.startswith("\\")
        or re.match(r"^[A-Za-z]:[\\/]", value)
        or ".." in Path(value).parts
    )


def collect_field_names(obj: Any) -> list[str]:
    names: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            names.append(str(key))
            names.extend(collect_field_names(value))
    elif isinstance(obj, list):
        for value in obj:
            names.extend(collect_field_names(value))
    return names


def build_regression_report(root: Path) -> dict[str, Any]:
    manifest = read_json(root / "v471-thos-v5-x1-plugin-cache-affected-manifest-v1.json")
    path_list = read_json(root / "v471-thos-v5-x2-affected-path-list-v1.json")
    rehearsal = read_json(root / "v471-thos-v5-x1-tempdir-repair-rehearsal-v1.json")
    guard = read_json(root / "v471-thos-v6-x1-manifest-pathlist-guard-v1.json")
    preview = read_json(root / "v471-thos-v7-x1-tempdir-diff-preview-v1.json")

    manifest_paths = [item.get("relative_path") for item in manifest.get("skills", [])]
    path_list_paths = path_list.get("relative_paths", [])
    preview_entries = preview.get("preview", {}).get("entries", [])
    rehearsal_entries = rehearsal.get("rehearsal", {}).get("candidate_results", [])

    raw_body_fields = sorted({name for name in collect_field_names(preview_entries) if RAW_BODY_FIELD_RE.search(name)})
    live_writes = [entry for entry in preview_entries if entry.get("write_performed")]
    approvals = [entry for entry in preview_entries if entry.get("approval_status") != "NOT_APPROVED"]
    unsafe_paths = [path for path in manifest_paths if not isinstance(path, str) or not path_safe(path)]
    checksum_bad = [entry.get("relative_path") for entry in preview_entries if not entry.get("source_checksum_unchanged")]
    body_bad = [entry.get("relative_path") for entry in preview_entries if not entry.get("body_preserved_in_temp_candidate")]
    rehearsal_checksum_bad = [entry.get("relative_path") for entry in rehearsal_entries if not entry.get("source_checksum_unchanged")]
    rehearsal_body_bad = [entry.get("relative_path") for entry in rehearsal_entries if not entry.get("original_body_preserved_in_temp_candidate")]

    checks = [
        row("manifest_path_count", "PASS_SHAPE_ONLY" if len(manifest_paths) == len(path_list_paths) == manifest.get("affected_count") else "FAIL_BLOCKER", "Manifest, path-list, and affected_count must agree", {"manifest_paths": len(manifest_paths), "path_list": len(path_list_paths), "affected_count": manifest.get("affected_count")}),
        row("manifest_path_content", "PASS_SHAPE_ONLY" if sorted(manifest_paths) == sorted(path_list_paths) else "FAIL_BLOCKER", "Path-list must equal manifest relative paths"),
        row("path_safety", "PASS_SHAPE_ONLY" if not unsafe_paths else "FAIL_BLOCKER", "Manifest paths must be relative and non-escaping", unsafe_paths),
        row("no_raw_body_fields", "PASS_SHAPE_ONLY" if not raw_body_fields else "FAIL_BLOCKER", "Preview artifacts must not expose raw body fields", raw_body_fields),
        row("no_live_writes", "PASS_SHAPE_ONLY" if not live_writes else "FAIL_BLOCKER", "Preview entries must not perform live writes", {"count": len(live_writes)}),
        row("no_approvals", "PASS_SHAPE_ONLY" if not approvals else "FAIL_BLOCKER", "Preview entries must remain NOT_APPROVED", {"count": len(approvals)}),
        row("preview_checksum_stability", "PASS_SHAPE_ONLY" if not checksum_bad else "FAIL_BLOCKER", "Preview source checksums must stay unchanged", checksum_bad),
        row("preview_body_preservation", "PASS_SHAPE_ONLY" if not body_bad else "FAIL_BLOCKER", "Preview tempdir candidates must preserve body suffix", body_bad),
        row("rehearsal_checksum_stability", "PASS_SHAPE_ONLY" if not rehearsal_checksum_bad else "FAIL_BLOCKER", "Rehearsal source checksums must stay unchanged", rehearsal_checksum_bad),
        row("rehearsal_body_preservation", "PASS_SHAPE_ONLY" if not rehearsal_body_bad else "FAIL_BLOCKER", "Rehearsal tempdir candidates must preserve original bodies", rehearsal_body_bad),
        row("prior_guard", guard.get("aggregate_status", "OPEN_GAP"), "v471 v6 manifest/path-list guard status carried forward"),
    ]
    failures = [item for item in checks if item["status"] == "FAIL_BLOCKER"]
    return {
        "aggregate_status": "FAIL_BLOCKER" if failures else "PASS_SHAPE_ONLY",
        "checks": checks,
        "failure_count": len(failures),
        "manifest_count": len(manifest_paths),
        "preview_entry_count": len(preview_entries),
        "rehearsal_entry_count": len(rehearsal_entries),
    }


def write_artifacts(root: Path, report: dict[str, Any]) -> list[str]:
    written: list[str] = []

    regression_payload = {
        "aggregate_status": report["aggregate_status"],
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "regression_report": report,
        "rows": report["checks"],
    }
    path = root / f"{PHASE_X1}-regression-guard-v1.json"
    write_json(path, regression_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-regression-guard-v1.md",
        f"""
# v472 THOS v1 x1 Regression Guard

Status: `{report["aggregate_status"]}`.

The guard checks no-raw-body, no-live-write, no-approval, relative-path, manifest/path-list equality, source-checksum stability, and body-preservation invariants across the v471 recovery chain.
""",
    )
    written.append((root / f"{PHASE_X1}-regression-guard-v1.md").as_posix())

    retry_payload = {
        "aggregate_status": "OPEN_GAP",
        "browser_probe": BROWSER_PROBE,
        "cli_probes": CLI_PROBES,
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("browser_retry", "OPEN_GAP", "Browser direct iab remains unavailable", BROWSER_PROBE),
            row("cli_retry_arby", "OPEN_GAP", "Arby launched safely but returned no final advisory", CLI_PROBES[0]),
            row("cli_retry_aster", "OPEN_GAP", "Aster launched safely but returned no final advisory", CLI_PROBES[1]),
            row("claim_ceiling", "PASS_SHAPE_ONLY", "Retry evidence is blocker evidence only"),
        ],
    }
    path = root / f"{PHASE_X1}-browser-cli-retry-ledger-v1.json"
    write_json(path, retry_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-browser-cli-retry-ledger-v1.md",
        """
# v472 THOS v1 x1 Browser/CLI Retry Ledger

Browser direct access remains unavailable as `iab`. Arby and Aster Vale launched through the non-ephemeral read-only CLI shape, but neither returned a final advisory inside the bounded wait.
""",
    )
    written.append((root / f"{PHASE_X1}-browser-cli-retry-ledger-v1.md").as_posix())

    approval_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("app_requests", "PASS_SHAPE_ONLY", "Existing app lanes were messaged for v472 v1", APP_REQUESTS),
            row("live_repair_decision", "OPEN_GAP", "Live plugin-cache repair remains unrequested and approval-gated"),
            row("approval_threshold", "OPEN_GAP", "Future repair requires exact path list, exact diff, rollback, and path-specific approval"),
            row("current_phase_boundary", "PASS_SHAPE_ONLY", "v472 v1 performs no live cache or connector mutation"),
        ],
    }
    path = root / f"{PHASE_X1}-approval-decision-ledger-v1.json"
    write_json(path, approval_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-approval-decision-ledger-v1.md",
        """
# v472 THOS v1 x1 Approval Decision Ledger

v472 v1 keeps live plugin-cache repair approval-gated. The phase extends regression safety and records blocker state, but it does not request or execute live cache writes.
""",
    )
    written.append((root / f"{PHASE_X1}-approval-decision-ledger-v1.md").as_posix())

    source_payload = {
        "aggregate_status": "PASS_SHAPE_ONLY",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("source_routes", "PASS_SHAPE_ONLY", "Official/source routes refreshed for v472", SOURCE_ROUTES),
            row("source_claim_ceiling", "PASS_SHAPE_ONLY", "Sources guide boundaries; they do not prove local repair"),
        ],
        "source_routes": SOURCE_ROUTES,
    }
    path = root / f"{PHASE_X1}-source-routing-ledger-v1.json"
    write_json(path, source_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-source-routing-ledger-v1.md",
        """
# v472 THOS v1 x1 Source Routing Ledger

Official/source routing was refreshed for Codex plugins/skills, Codex CLI, MCP safety, and Codex app context. These sources guide the THOS boundary, not local completion claims.
""",
    )
    written.append((root / f"{PHASE_X1}-source-routing-ledger-v1.md").as_posix())

    run_payload = {
        "aggregate_status": "OPEN_GAP" if report["aggregate_status"] == "PASS_SHAPE_ONLY" else "FAIL_BLOCKER",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("regression_guard", report["aggregate_status"], "Regression guard executed", {"failure_count": report["failure_count"]}),
            row("browser_cli", "OPEN_GAP", "Browser and CLI blockers remain open"),
            row("live_repair", "OPEN_GAP", "No live plugin-cache repair occurred"),
            row("publication", "NOT_RUN", "Publication deferred to x2 under paired cadence"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = root / f"{PHASE_X1}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-run-status-v1.md",
        """
# v472 THOS v1 x1 Run Status

v472 x1 extended the THOS regression guard and recorded current Browser/CLI blocker state. Publication is deferred to x2.
""",
    )
    written.append((root / f"{PHASE_X1}-run-status-v1.md").as_posix())

    handoff_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": PHASE_X2,
        "phase_slug": PHASE_X1,
        "rows": [
            row("x2_task_1", "OPEN_GAP", "Publish regression claim ceiling"),
            row("x2_task_2", "OPEN_GAP", "Publish v472 v2 handoff for approval packet or retry focus"),
        ],
    }
    path = root / f"{PHASE_X1}-x2-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-x2-handoff-v1.md",
        """
# v472 THOS v1 x1 To x2 Handoff

x2 should publish the regression claim ceiling and the v2 handoff. No live repair should be implied.
""",
    )
    written.append((root / f"{PHASE_X1}-x2-handoff-v1.md").as_posix())

    claim_payload = {
        "aggregate_status": "OPEN_GAP" if report["aggregate_status"] == "PASS_SHAPE_ONLY" else "FAIL_BLOCKER",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("regression_claim", report["aggregate_status"], "May claim regression guard result only"),
            row("browser_cli_claim", "OPEN_GAP", "May not claim Browser/CLI blockers fixed"),
            row("repair_claim", "OPEN_GAP", "May not claim live plugin-cache repair"),
            row("source_claim", "PASS_SHAPE_ONLY", "May cite official sources as routing context only"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = root / f"{PHASE_X2}-regression-claim-ceiling-v1.json"
    write_json(path, claim_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-regression-claim-ceiling-v1.md",
        """
# v472 THOS v1 x2 Regression Claim Ceiling

This phase may claim regression-guard readiness evidence only. It may not claim Browser recovery, CLI sibling recovery, live cache repair, connector writes, or GMUT gate closure.
""",
    )
    written.append((root / f"{PHASE_X2}-regression-claim-ceiling-v1.md").as_posix())

    x2_run_payload = {
        "aggregate_status": "OPEN_GAP" if report["aggregate_status"] == "PASS_SHAPE_ONLY" else "FAIL_BLOCKER",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("x1_x2_pair", "OPEN_GAP", "v472 v1 published regression and blocker ledgers"),
            row("regression_guard", report["aggregate_status"], "Regression guard result"),
            row("open_blockers", "OPEN_GAP", "Browser/CLI/live repair remain open"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = root / f"{PHASE_X2}-run-status-v1.json"
    write_json(path, x2_run_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-run-status-v1.md",
        """
# v472 THOS v1 x2 Run Status

Status: `OPEN_GAP`.

v472 v1 published a regression guard and current blocker ledger. It did not perform live plugin-cache repair or external mutation.
""",
    )
    written.append((root / f"{PHASE_X2}-run-status-v1.md").as_posix())

    v2_handoff = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": "v472-thos-v2-x1",
        "phase_slug": PHASE_X2,
        "rows": [
            row("v2_task_1", "OPEN_GAP", "Option A: prepare explicit path-specific live-repair approval packet without execution"),
            row("v2_task_2", "OPEN_GAP", "Option B: expand regression fixtures into expected-negative fixture suite"),
            row("v2_task_3", "OPEN_GAP", "Option C: retry Browser or one CLI lane only if capability conditions improve"),
            row("v2_task_4", "OPEN_GAP", "Keep GMUT gates open and Journey context non-canon"),
        ],
    }
    path = root / f"{PHASE_X2}-v472-thos-v2-handoff-v1.json"
    write_json(path, v2_handoff)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-v472-thos-v2-handoff-v1.md",
        """
# v472 THOS v1 x2 To v2 Handoff

v2 should either prepare an explicit path-specific live-repair approval packet, expand regression fixtures, or retry Browser/CLI only if the capability surface improves.
""",
    )
    written.append((root / f"{PHASE_X2}-v472-thos-v2-handoff-v1.md").as_posix())

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Build v472 THOS v1 regression guard artifacts.")
    parser.add_argument("--artifact-root", default="docs/trinity-live-traces")
    args = parser.parse_args()

    root = Path(args.artifact_root)
    report = build_regression_report(root)
    written = write_artifacts(root, report)
    print(json.dumps({"regression_status": report["aggregate_status"], "failure_count": report["failure_count"], "written": written}, indent=2, sort_keys=True))
    return 0 if report["aggregate_status"] == "PASS_SHAPE_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
