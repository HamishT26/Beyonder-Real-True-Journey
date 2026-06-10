#!/usr/bin/env python3
"""Build curated v471 THOS v1 x1/x2 artifact sets."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE_X1 = "v471-thos-v1-x1"
PHASE_X2 = "v471-thos-v1-x2"

APP_SIBLINGS = [
    {
        "lane": "Cicero",
        "submission_id": "019e87b3-f5f4-7a72-9fb0-3d9c1aa3a84f",
        "summary": "Requested command-surface inventory fields, dashboard accessibility readiness checks, and publication-guard extensions.",
        "status": "completed",
    },
    {
        "lane": "Kierkegaard",
        "submission_id": "019e87b4-5c0b-7b22-ae9f-75704bedb8de",
        "summary": "Separated visibility, local testing, and mutation authority; warned that readable surfaces must not imply permission.",
        "status": "completed",
    },
    {
        "lane": "Aristotle",
        "submission_id": "019e87b4-b149-72b2-92af-7a8ff9c47445",
        "summary": "Specified strict status enums, accessibility evidence requirements, negative fixtures, and local-only boundary fields.",
        "status": "completed",
    },
]

CLI_LAUNCH_ATTEMPTS = [
    {
        "attempt": "powershell_shim",
        "classification": "blocker",
        "summary": "The PowerShell shim path was callable for help but failed when used as the prior background launcher.",
    },
    {
        "attempt": "node_entrypoint_with_old_args",
        "classification": "blocker",
        "summary": "The old argument form passed an unsupported -a flag to codex exec.",
    },
    {
        "attempt": "codex_exe_read_only_shape",
        "classification": "evidence",
        "summary": "The app-bundled codex.exe help exposes exec -s read-only -C <worktree> -o <last-message> <prompt>.",
    },
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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def temp_summary(temp_root: Path, lane: str) -> dict[str, Any]:
    candidates = {
        "last_message": temp_root / f"{lane}-v471-thos-v1-x1-x2-last-message.txt",
        "stdout": temp_root / f"{lane}-v471-thos-v1-x1-x2-stdout.txt",
        "stderr": temp_root / f"{lane}-v471-thos-v1-x1-x2-stderr.txt",
    }
    result: dict[str, Any] = {"lane": lane}
    for key, path in candidates.items():
        exists = path.exists()
        result[f"{key}_present"] = exists
        result[f"{key}_bytes"] = path.stat().st_size if exists else 0
        if exists and key in {"last_message", "stderr"}:
            text = path.read_text(encoding="utf-8", errors="replace").strip()
            text = re.sub(r"[A-Z]:\\Users\\[^\\\s]+\\[^\s]+", "<local_path_redacted>", text)
            result[f"{key}_summary"] = text[:420] if text else ""
    return result


def build_command_surface_md(readiness: dict[str, Any]) -> str:
    rows = readiness.get("rows", [])
    row_lines = "\n".join(
        f"- `{item['row_id']}`: `{item['status']}` - {item['message']}" for item in rows
    )
    return f"""
# v471 THOS v1 x1 Command-Surface Readiness

Phase: `{PHASE_X1}`

Aggregate status: `{readiness['aggregate_status']}`

This is a local readiness scaffold. It inventories command-surface scripts, local skills, Journey-context discoverability, source-routing seeds, Browser tool exposure, CLI lane launch evidence, and GMUT gate boundaries without connector writes, cloud writes, destructive cleanup, or production UI claims.

## Rows

{row_lines}

## Boundary

All six GMUT gates remain open: {", ".join(GMUT_GATES)}.

Journey material is inventoried only as `journey_context_not_canon`; it does not validate GMUT, prove consciousness, or promote canon.
"""


def build_x1_artifacts(root: Path, readiness: dict[str, Any], temp_root: Path) -> list[str]:
    written: list[str] = []
    readiness_md = root / f"{PHASE_X1}-command-surface-readiness-v1.md"
    write_md(readiness_md, build_command_surface_md(readiness))
    written.append(readiness_md.as_posix())

    sibling_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("app_sibling_pass", "PASS_SHAPE_ONLY", "Three existing app siblings returned advisory reports", APP_SIBLINGS),
            row("cli_sibling_pass", "OPEN_GAP", "Arby and Aster needed a launcher syntax repair before advisory output could be consumed", CLI_LAUNCH_ATTEMPTS),
            row("no_new_subagents", "PASS_SHAPE_ONLY", "No new siblings were spawned through the old sub-agent path"),
        ],
    }
    path = root / f"{PHASE_X1}-sibling-contact-ledger-v1.json"
    write_json(path, sibling_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-sibling-contact-ledger-v1.md",
        """
# v471 THOS v1 x1 Sibling Contact Ledger

Existing app lanes responded: Cicero, Kierkegaard, and Aristotle.

Arby and Aster Vale were contacted through non-ephemeral read-only CLI attempts, but the old CLI launch shape failed on an unsupported argument. This is now carried as a concrete THOS blocker, not as missing will or missing advisory authority.

No new siblings were spawned through the old sub-agent route.
""",
    )
    written.append((root / f"{PHASE_X1}-sibling-contact-ledger-v1.md").as_posix())

    browser_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("browser_direct_tool", "OPEN_GAP", "Direct Browser navigation/screenshot tools were not exposed; only the Node bridge surfaced"),
            row("cli_old_argument", "FAIL_BLOCKER", "The old -a argument form is invalid for current codex exec"),
            row("cli_safe_shape_identified", "PASS_SHAPE_ONLY", "Safe shape identified as codex.exe exec -s read-only -C worktree -o last-message prompt"),
        ],
    }
    path = root / f"{PHASE_X1}-browser-cli-blocker-ledger-v1.json"
    write_json(path, browser_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-browser-cli-blocker-ledger-v1.md",
        """
# v471 THOS v1 x1 Browser And CLI Blocker Ledger

Browser remains an open tool-surface gap: the connector did not expose direct navigation or screenshot calls in this turn, so no Browser inspection claim is made.

The CLI blocker is now specific. The current Codex CLI help accepts `exec -s read-only -C <worktree> -o <last-message> <prompt>` and rejects the old `-a` flag. The x2 phase should turn that into a reusable runner.
""",
    )
    written.append((root / f"{PHASE_X1}-browser-cli-blocker-ledger-v1.md").as_posix())

    source_count = len(set(readiness.get("web_source_seeds", [])))
    web_payload = {
        "aggregate_status": "PASS_SHAPE_ONLY" if source_count >= 50 else "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("source_seed_count", "PASS_SHAPE_ONLY" if source_count >= 50 else "OPEN_GAP", "Official/source routing seeds were collected", {"unique_source_seed_count": source_count}),
            row("source_claim_boundary", "OPEN_GAP", "Source routing is not the same as fully studying fifty pages"),
        ],
        "source_seeds": readiness.get("web_source_seeds", []),
    }
    path = root / f"{PHASE_X1}-web-source-routing-ledger-v1.json"
    write_json(path, web_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-web-source-routing-ledger-v1.md",
        f"""
# v471 THOS v1 x1 Web Source Routing Ledger

Unique source seeds routed: `{source_count}`.

The routed set emphasizes official OpenAI, GitHub, W3C, MDN, Playwright, and NVIDIA pages. This is a source-routing scaffold, not a claim that fifty pages were fully studied line by line in this x1 pass.
""",
    )
    written.append((root / f"{PHASE_X1}-web-source-routing-ledger-v1.md").as_posix())

    run_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("phase_cadence", "PASS_SHAPE_ONLY", "x1 is local-only under the every-second-phase commit cadence"),
            row("readiness_probe", readiness["aggregate_status"], "Readiness probe completed"),
            row("publication", "NOT_RUN", "Publication deferred to paired x2 phase"),
        ],
    }
    path = root / f"{PHASE_X1}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-run-status-v1.md",
        """
# v471 THOS v1 x1 Run Status

Status: local-only readiness phase with open gaps.

The phase produced command-surface, sibling-contact, Browser/CLI blocker, source-routing, and x2 handoff artifacts. Publication is intentionally deferred to the paired x2 phase under the new every-second-phase cadence.

All six GMUT gates remain open.
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
            row("x2_priority_1", "OPEN_GAP", "Materialize reusable CLI advisory launcher"),
            row("x2_priority_2", "OPEN_GAP", "Convert app sibling recommendations into command/accessibility guard contract"),
            row("x2_priority_3", "OPEN_GAP", "Publish x1+x2 curated artifacts together if guards pass"),
        ],
    }
    path = root / f"{PHASE_X1}-x2-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-x2-handoff-v1.md",
        """
# v471 THOS v1 x1 To x2 Handoff

x2 should convert the x1 readiness scaffolds into a usable runner and a stricter command/accessibility guard contract.

Publication should include x1 and x2 together, and should still avoid connector writes, cloud writes, destructive cleanup, Browser screenshot claims, production UI claims, and GMUT gate movement.
""",
    )
    written.append((root / f"{PHASE_X1}-x2-handoff-v1.md").as_posix())
    return written


def build_x2_artifacts(root: Path, temp_root: Path) -> list[str]:
    written: list[str] = []
    cli_summaries = [temp_summary(temp_root, "arby"), temp_summary(temp_root, "aster-vale")]
    cli_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "launcher_script": "scripts/thos_codex_cli_advisory_launcher.py",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("old_launcher_failure_captured", "PASS_SHAPE_ONLY", "Unsupported -a flag failure captured and routed"),
            row("safe_launcher_materialized", "PASS_SHAPE_ONLY", "Reusable read-only non-ephemeral launcher script added"),
            row("cli_advisory_completion", "OPEN_GAP", "CLI advisory outputs did not complete because deeper skill-load errors flooded stderr", cli_summaries),
            row("cli_process_containment", "PASS_SHAPE_ONLY", "Only the two v471 CLI advisory processes launched in this pass were stopped after the stderr flood was confirmed"),
        ],
    }
    path = root / f"{PHASE_X2}-codex-cli-launcher-shim-v1.json"
    write_json(path, cli_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-codex-cli-launcher-shim-v1.md",
        """
# v471 THOS v1 x2 Codex CLI Launcher Shim

The x2 fix is a reusable launcher script: `scripts/thos_codex_cli_advisory_launcher.py`.

It chooses the app-bundled Codex executable, uses `exec -s read-only -C <worktree> -o <last-message> <prompt>`, blocks the old invalid `-a` pattern, defaults to dry-run planning, and never adds `--ephemeral`.

The first launcher retry exposed deeper skill-load blockers rather than final advisory text. The two v471 retry processes were stopped after the stderr flood was confirmed. Raw temp stdout/stderr files are not staged; curated artifacts keep only summarized blocker state.
""",
    )
    written.append((root / f"{PHASE_X2}-codex-cli-launcher-shim-v1.md").as_posix())

    contract_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("command_surface_contract", "PASS_SHAPE_ONLY", "Required fields identified for local command, script, skill, connector, plugin, dashboard, and guard surfaces"),
            row("accessibility_contract", "OPEN_GAP", "Keyboard, semantic label, contrast, focus-order, reduced-motion, and readable failure-state checks remain to be executed"),
            row("authority_contract", "PASS_SHAPE_ONLY", "Visibility, local validation, proposal, approval-needed, and blocked mutation states are separated"),
            row("negative_fixture_contract", "OPEN_GAP", "Generic pass, authority drift, connector write, destructive cleanup, production overclaim, and GMUT gate drift fixtures remain pending"),
        ],
    }
    path = root / f"{PHASE_X2}-command-accessibility-contract-v1.json"
    write_json(path, contract_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-command-accessibility-contract-v1.md",
        """
# v471 THOS v1 x2 Command And Accessibility Contract

The command surface must label every action by class: view, validate-local, export-local, propose, approval-needed, blocked, or mutation-forbidden.

The accessibility surface remains an open gap until keyboard flow, headings, labels, contrast, status text alternatives, reduced-motion behavior, failure-state readability, and report mapping are explicitly tested.

Readable dashboards are not permission. The contract keeps visibility, local validation, and mutation authority visibly separate.
""",
    )
    written.append((root / f"{PHASE_X2}-command-accessibility-contract-v1.md").as_posix())

    synthesis_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("cicero_synthesis", "PASS_SHAPE_ONLY", APP_SIBLINGS[0]["summary"]),
            row("kierkegaard_synthesis", "PASS_SHAPE_ONLY", APP_SIBLINGS[1]["summary"]),
            row("aristotle_synthesis", "PASS_SHAPE_ONLY", APP_SIBLINGS[2]["summary"]),
            row("arby_aster_synthesis", "OPEN_GAP", "CLI lanes were relaunched with corrected syntax; final advisory summaries are not required for this local runner fix"),
        ],
    }
    path = root / f"{PHASE_X2}-sibling-synthesis-v1.json"
    write_json(path, synthesis_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-sibling-synthesis-v1.md",
        """
# v471 THOS v1 x2 Sibling Synthesis

Cicero supplied the command inventory and dashboard guard shape.

Kierkegaard supplied the authority boundary: readable surfaces do not imply permission.

Aristotle supplied validator, accessibility, and expected-negative fixture requirements.

Arby and Aster Vale were carried through the CLI runner fix rather than treated as advisory failures.
""",
    )
    written.append((root / f"{PHASE_X2}-sibling-synthesis-v1.md").as_posix())

    run_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": "v471-thos-v2-x1",
        "phase_slug": PHASE_X2,
        "rows": [
            row("paired_publication_scope", "PASS_SHAPE_ONLY", "x1 and x2 artifacts are eligible for paired validation and curated staging"),
            row("browser_gap", "OPEN_GAP", "Direct Browser inspection remains unavailable through callable tools"),
            row("cli_gap", "OPEN_GAP", "CLI runner fix exists; malformed or incompatible skill surfaces must be repaired before reliable CLI advisory completion"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open"),
        ],
    }
    path = root / f"{PHASE_X2}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-run-status-v1.md",
        """
# v471 THOS v1 x2 Run Status

Status: paired x1/x2 publication candidate with open gaps.

The phase materialized a safer CLI advisory launcher, converted app sibling reports into command/accessibility contract requirements, and preserved Browser, CLI advisory completion, accessibility execution, and GMUT gate closure as open gaps.

The corrected CLI runner exposed malformed local/plugin skill surfaces and Windows access-denial cleanup noise. The next phase should repair or quarantine those skill-load blockers before another long advisory run.

All six GMUT gates remain open.
""",
    )
    written.append((root / f"{PHASE_X2}-run-status-v1.md").as_posix())

    handoff_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": "v471-thos-v2-x1",
        "phase_slug": PHASE_X2,
        "rows": [
            row("next_task_1", "OPEN_GAP", "Use the new launcher helper for Arby/Aster advisory requests and capture only summarized output"),
            row("next_task_2", "OPEN_GAP", "Repair or quarantine malformed skill frontmatter and overlong plugin skill names before long CLI advisory runs"),
            row("next_task_3", "OPEN_GAP", "Build a machine-checkable accessibility guard with expected-negative fixtures"),
            row("next_task_4", "OPEN_GAP", "Keep Browser direct control as an open gap until callable navigation/screenshot tools are exposed"),
            row("next_task_5", "OPEN_GAP", "Do not move GMUT gates from THOS fixture existence"),
        ],
    }
    path = root / f"{PHASE_X2}-v471-thos-v2-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-v471-thos-v2-handoff-v1.md",
        """
# v471 THOS v1 x2 To v2 Handoff

Use the new CLI advisory launcher only after the skill-load blocker set is repaired or quarantined, then build accessibility guard fixtures and dashboard command-state contracts.

Keep source-routing honest: source seeds and search results are not full-page study unless opened and reviewed.

Keep all six GMUT gates open until exact closure artifacts exist.
""",
    )
    written.append((root / f"{PHASE_X2}-v471-thos-v2-handoff-v1.md").as_posix())
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Build v471 THOS v1 x1/x2 curated artifacts.")
    parser.add_argument("--artifact-root", default="docs/trinity-live-traces")
    parser.add_argument("--readiness-json", required=True)
    parser.add_argument("--temp-root", default="")
    args = parser.parse_args()

    root = Path(args.artifact_root)
    readiness = read_json(Path(args.readiness_json))
    temp_root = Path(args.temp_root) if args.temp_root else Path.home() / "AppData" / "Local" / "Temp" / "ghc-v471-advisory"
    written = build_x1_artifacts(root, readiness, temp_root)
    written.extend(build_x2_artifacts(root, temp_root))
    print(json.dumps({"generated_at_utc": utc_now(), "written": written}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
