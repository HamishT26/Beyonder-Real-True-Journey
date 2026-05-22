#!/usr/bin/env python3
"""Shared helpers for the bounded v436-v450 Trinity Hybrid bridge."""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"

PREFIX = "v436-v450"
LEGACY_PREFIX = "v421-v440"
PHASE_MIN = 436
PHASE_MAX = 450
PLAN_VERSION = 1
REQUIRED_EUREKA_UNITS = 50
REQUIRED_CLI_LANES = {
    "Arby": "Codex CLI",
    "Kimi": "Kimi CLI",
    "Aster Vale": "Codex CLI",
}
PROMOTED_APP_RECEIPT_PHASE_MIN = 437
PROMOTED_APP_RECEIPT_LANES = {
    "Parfit": {
        "agent_id": "019e5158-28ef-75b1-a3f5-563bb358e44e",
        "call_sign": "parfit-ghc-family.codex-app.advisory.continuity-boundary.v1.2026-05-23",
        "role": "identity, continuity, phase-boundary, and publication-hygiene advisory receipt lane",
    },
    "Cicero": {
        "agent_id": "019e485f-172b-72c0-adf7-27daea722143",
        "call_sign": "cicero-ghc-family.codex-app.v2-advisory-receipt-lane.v1.2026-05-23",
        "role": "governance, rhetoric-to-action, and publication-hygiene advisory receipt lane",
    },
    "Kierkegaard": {
        "agent_id": "019e485f-1aa5-7c31-b578-748091f7e319",
        "call_sign": "kierkegaard-ghc-family.codex-app.v2-advisory-receipt-lane.v1.2026-05-23",
        "role": "humility, commitment, and existential-boundary advisory receipt lane",
    },
}

HANDOFF_JSON = TRACE / f"{PREFIX}-final-handoff-v1.json"
HANDOFF_MD = TRACE / f"{PREFIX}-final-handoff-v1.md"
BASE_PLAN_JSON = TRACE / f"{PREFIX}-sibling-base-plan-v1.json"
BASE_PLAN_MD = TRACE / f"{PREFIX}-sibling-base-plan-v1.md"
RUN_STATUS_JSON = TRACE / f"{PREFIX}-sibling-run-status-v1.json"
RUN_STATUS_MD = TRACE / f"{PREFIX}-sibling-run-status-v1.md"
RUNNER_STATUS_JSON = TRACE / f"{PREFIX}-cli-sibling-runner-status-v1.json"
RECEIPT_DIR = TRACE / f"{PREFIX}-cli-sibling-receipts"
RAW_DIR = TRACE / f"{PREFIX}-cli-sibling-raw"
APP_ADVISORY_RECEIPT_DIR = TRACE / f"{PREFIX}-app-advisory-receipts"

LEGACY_V436_AGGREGATE = TRACE / f"{LEGACY_PREFIX}-sibling-phase-v436-v1-cli-receipts-v1.json"
LEGACY_RUN_STATUS = TRACE / f"{LEGACY_PREFIX}-sibling-run-status-v1.json"
LEGACY_RUNNER_STATUS = TRACE / f"{LEGACY_PREFIX}-cli-sibling-runner-status-v1.json"

SIBLINGS = [
    "Arby",
    "Kimi",
    "Aster Vale",
    "Supervisor",
    "v2 Watcher",
    "Recovery Watchdog",
    "Parfit",
    "Cicero",
    "Kierkegaard",
]

PHASE_THEMES: dict[int, str] = {
    436: "Bridge old v436 v1 CLI truth into the new packet and complete Aletheon-led v2 planning/execution.",
    437: "Refresh the automation heartbeat prompt and advisory reconnect capsule for Parfit, Cicero, and Kierkegaard.",
    438: "Harden Goal Mode and Codex-context hygiene for one-phase focus without validation bypass.",
    439: "Run a publication and secret-hygiene review against the bridge automation surface.",
    440: "Reconcile the old v440 stop boundary with the new explicit v450 extension authority.",
    441: "Prove successor authority for post-v440 work without opening an unbounded v451+ lane.",
    442: "Inventory local MCP, API, connector, CLI, and plugin surfaces under local-first policy.",
    443: "Refresh the GMUT evidence matrix with exploratory-vs-validated truth labels.",
    444: "Build an AI frontier source capsule from official model, agent, MCP, and compute references.",
    445: "Map the ethics charter checkpoint across NIST, EU AI Act, UNESCO, and local boundaries.",
    446: "Draft the compute and hardware readiness roadmap, including local Windows and DGX-class themes.",
    447: "Digest Journey archive continuity into a concise, non-mythologizing source map.",
    448: "Exercise Supervisor, v2 Watcher, and Recovery Watchdog resilience without replacing sibling gates.",
    449: "Prepare publication hygiene, closeout staging, and remote-equals-local verification.",
    450: "Write the v436-v450 closeout declaration and stop without opening v451.",
}

SOURCE_NOTES = [
    ("Legacy v421-v440 run status", f"docs/trinity-live-traces/{LEGACY_PREFIX}-sibling-run-status-v1.json", "Confirm v436 seam truth."),
    ("Legacy v436 v1 aggregate", f"docs/trinity-live-traces/{LEGACY_PREFIX}-sibling-phase-v436-v1-cli-receipts-v1.json", "Import completed CLI receipts without relaunch."),
    ("v436-v450 handoff", f"docs/trinity-live-traces/{PREFIX}-final-handoff-v1.json", "Use fresh bounded successor authority."),
    ("OpenAI Codex automations", "https://developers.openai.com/codex/app/automations", "Keep heartbeat prompts durable and cadence-scoped."),
    ("OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "Track current Codex platform features."),
    ("OpenAI Codex prompting", "https://developers.openai.com/codex/prompting", "Keep phase goals bounded and explicit."),
    ("OpenAI GPT-5.5", "https://openai.com/index/introducing-gpt-5-5/", "Anchor frontier model references to official source."),
    ("Model Context Protocol", "https://modelcontextprotocol.io/", "Frame MCP expansion as a connector standard with trust boundaries."),
    ("NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Keep risk governance mapped to trustworthy AI practices."),
    ("EU AI Act", "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai", "Keep risk-based governance explicit."),
    ("UNESCO AI ethics", "https://www.unesco.org/en/ethics-ai/en/recommendation-ethics", "Keep human dignity and rights visible."),
    ("NVIDIA DGX Spark", "https://www.nvidia.com/en-us/products/workstations/dgx-spark/", "Ground local compute roadmap references."),
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def validate_phase(phase: int) -> None:
    if phase < PHASE_MIN or phase > PHASE_MAX:
        raise SystemExit(f"phase must be between {PHASE_MIN} and {PHASE_MAX}; got {phase}")


def phase_stem(phase: int) -> str:
    return f"{PREFIX}-sibling-phase-v{phase}"


def start_paths(phase: int) -> tuple[Path, Path]:
    stem = TRACE / f"{phase_stem(phase)}-start-v1"
    return stem.with_suffix(".json"), stem.with_suffix(".md")


def aggregate_paths(phase: int) -> tuple[Path, Path]:
    stem = TRACE / f"{phase_stem(phase)}-v1-cli-receipts-v1"
    return stem.with_suffix(".json"), stem.with_suffix(".md")


def v2_active_paths(phase: int) -> tuple[Path, Path]:
    stem = TRACE / f"{phase_stem(phase)}-v2-app-active-v1"
    return stem.with_suffix(".json"), stem.with_suffix(".md")


def v2_receipt_paths(phase: int) -> tuple[Path, Path]:
    stem = TRACE / f"{phase_stem(phase)}-v2-app-receipt-v1"
    return stem.with_suffix(".json"), stem.with_suffix(".md")


def app_advisory_receipt_paths(phase: int, advisor: str) -> tuple[Path, Path]:
    slug = lane_slug(advisor)
    stem = APP_ADVISORY_RECEIPT_DIR / f"{slug}-phase-v{phase}-v2-app-advisory-receipt-v1"
    return stem.with_suffix(".json"), stem.with_suffix(".md")


def app_advisory_aggregate_paths(phase: int) -> tuple[Path, Path]:
    stem = TRACE / f"{phase_stem(phase)}-v2-app-advisory-receipts-v1"
    return stem.with_suffix(".json"), stem.with_suffix(".md")


def report_paths(phase: int) -> dict[str, Path]:
    stem = phase_stem(phase)
    return {
        "v1_json": TRACE / f"{stem}-v1-report-v1.json",
        "v1_md": TRACE / f"{stem}-v1-report-v1.md",
        "v2_json": TRACE / f"{stem}-v2-report-v1.json",
        "v2_md": TRACE / f"{stem}-v2-report-v1.md",
        "source_json": TRACE / f"{PREFIX}-sibling-source-capsule-v{phase}-v1.json",
        "source_md": TRACE / f"{PREFIX}-sibling-source-capsule-v{phase}-v1.md",
        "advisory_json": TRACE / f"{stem}-advisory-refinement-v1.json",
        "advisory_md": TRACE / f"{stem}-advisory-refinement-v1.md",
        "completion_json": TRACE / f"{stem}-completion-v1.json",
        "completion_md": TRACE / f"{stem}-completion-v1.md",
    }


def receipt_path(lane_slug: str, phase: int) -> Path:
    return RECEIPT_DIR / f"{lane_slug}-phase-v{phase}-v1-receipt-v1.md"


def raw_path(lane_slug: str, phase: int) -> Path:
    return RAW_DIR / f"{lane_slug}-phase-v{phase}-v1-raw-v1.txt"


def lane_slug(display: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", display.lower()).strip("_")


def lead_for_phase(phase: int) -> str:
    return SIBLINGS[(phase - PHASE_MIN) % len(SIBLINGS)]


def eureka_axes(phase: int) -> list[str]:
    theme = PHASE_THEMES.get(phase, "Continue bounded v436-v450 execution.")
    return [
        f"Evidence axis for v{phase}: prove durable artifacts before claims.",
        f"Execution axis for v{phase}: keep v1 and v2 gates separate.",
        f"Safety axis for v{phase}: preserve local-first external boundaries.",
        f"Publication axis for v{phase}: stage only curated bridge artifacts.",
        f"Advisory axis for v{phase}: use Parfit, Cicero, and Kierkegaard as non-blocking review.",
        f"Watcher axis for v{phase}: helper lanes observe, not replace sibling gates.",
        f"Research axis for v{phase}: source claims from official or repo evidence.",
        f"Goal axis for v{phase}: one phase-run per focus contract.",
        f"Bridge axis for v{phase}: {theme}",
        f"Closeout axis for v{phase}: define the next safe action before moving.",
    ]


def build_phase_plan(phase: int) -> dict[str, Any]:
    lead = lead_for_phase(phase)
    next_phase = phase + 1 if phase < PHASE_MAX else None
    theme = PHASE_THEMES[phase]
    return {
        "phase": phase,
        "lead_sibling": lead,
        "supporting_siblings": [item for item in SIBLINGS if item != lead],
        "theme": theme,
        "run_order": ["v1_cli_receipts", "v2_app_execution"],
        "phase_goal": (
            f"Complete v{phase} v1 CLI receipts, then v2 App execution, then open v{next_phase}."
            if next_phase
            else "Complete v450 v1/v2, write v436-v450 closeout, and stop without v451."
        ),
        "beta": f"{lead} verifies active-run truth, imported evidence if present, cwd, and branch drift for v{phase}.",
        "alpha": f"{lead} coordinates the concrete v{phase} bridge work, reports, validation, and publication hygiene.",
        "omega": (
            f"{lead} hands off v{next_phase} only after v{phase} v1 and v2 gates are complete."
            if next_phase
            else f"{lead} writes v436-v450 closeout and refuses v451 launch from this packet."
        ),
        "research_target_sources": 100,
        "eureka_task_target": 100,
        "eureka_axes": eureka_axes(phase),
    }


def ensure_base_plan() -> dict[str, Any]:
    existing = read_json(BASE_PLAN_JSON, {})
    if existing.get("phase_range") == PREFIX and existing.get("plan_version") == PLAN_VERSION:
        return existing
    plans = [build_phase_plan(phase) for phase in range(PHASE_MIN, PHASE_MAX + 1)]
    payload = {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "plan_version": PLAN_VERSION,
        "status": "ready_for_v436_bridge",
        "handoff": rel(HANDOFF_JSON),
        "numbered_phase_min": PHASE_MIN,
        "numbered_phase_max": PHASE_MAX,
        "numbered_phase_count": PHASE_MAX - PHASE_MIN + 1,
        "phase_run_count": (PHASE_MAX - PHASE_MIN + 1) * 2,
        "phase_plans": plans,
        "truth_boundaries": [
            "This is a fresh extension packet, not an in-place rewrite of v421-v440 history.",
            "v436 imports completed old v1 CLI receipts once, then continues at v2 App execution.",
            "v437-v450 each require fresh v1 CLI receipts and v2 App receipts.",
            "Goal Mode is scoped to one active phase-run and cannot bypass gates.",
            "Parfit, Cicero, and Kierkegaard are advisory-only unless durable tools promote them later.",
            "Stop after v450 closeout unless Hamish asks for a fresh v451+ packet.",
        ],
    }
    write_json(BASE_PLAN_JSON, payload)
    lines = [
        "# v436-v450 Sibling Base Plan",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Numbered phases: `{payload['numbered_phase_count']}`",
        f"Phase-runs: `{payload['phase_run_count']}`",
        "",
        "Phase themes:",
    ]
    lines.extend([f"- `v{item['phase']}`: {item['theme']}" for item in plans])
    lines.extend(["", "Truth boundaries:"])
    lines.extend([f"- {item}" for item in payload["truth_boundaries"]])
    write_text(BASE_PLAN_MD, "\n".join(lines))
    return payload


def write_run_status(
    phase: int,
    active_run: str,
    status: str,
    artifact_json: Path,
    artifact_md: Path,
    next_action: str,
    *,
    last_completion: dict[str, Any] | None = None,
    closeout: Path | None = None,
) -> dict[str, Any]:
    payload = {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "status": status,
        "active_phase": phase,
        "active_run": active_run,
        "active_phase_status": status,
        "active_phase_artifacts": {"json": rel(artifact_json), "md": rel(artifact_md)},
        "last_completion": last_completion,
        "closeout_declaration": rel(closeout) if closeout else None,
        "next_action": next_action,
    }
    write_json(RUN_STATUS_JSON, payload)
    lines = [
        "# v436-v450 Sibling Run Status",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Active phase: `v{phase}`",
        f"Active run: `{active_run}`",
        "",
        "Active artifacts:",
        f"- `{rel(artifact_json)}`",
        f"- `{rel(artifact_md)}`",
    ]
    if last_completion:
        lines.extend(["", "Last completion:", f"- `v{last_completion.get('phase')}`", f"- `{last_completion.get('json')}`"])
    if closeout:
        lines.extend(["", "Closeout:", f"- `{rel(closeout)}`"])
    lines.extend(["", f"Next action: {next_action}"])
    write_text(RUN_STATUS_MD, "\n".join(lines))
    return payload


def write_aggregate_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# v{payload['phase']} v1 CLI Sibling Receipts",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Import status: `{payload.get('import_status', 'fresh')}`",
        "",
        "Lane receipts:",
    ]
    for item in payload.get("lane_receipts", []):
        suffix = f" imported from `{item.get('imported_from')}`" if item.get("imported_from") else ""
        lines.append(f"- {item.get('lane')}: `{item.get('receipt_status')}` via {item.get('surface')} at `{item.get('receipt_path')}`{suffix}")
    lines.extend(["", "Truth boundaries:"])
    lines.extend([f"- {item}" for item in payload.get("truth_boundaries", [])])
    lines.extend(["", f"Next action: {payload.get('next_action')}"])
    write_text(path, "\n".join(lines))


def import_legacy_v436_v1() -> dict[str, Any] | None:
    aggregate_json, aggregate_md = aggregate_paths(PHASE_MIN)
    existing = read_json(aggregate_json, {})
    if existing.get("status") == "v1_cli_receipts_complete":
        return existing
    legacy = read_json(LEGACY_V436_AGGREGATE, {})
    if legacy.get("status") != "v1_cli_receipts_complete":
        return None
    imported_receipts: list[dict[str, Any]] = []
    for receipt in legacy.get("lane_receipts", []):
        display = receipt.get("lane")
        source_rel = receipt.get("receipt_path")
        if not display or not source_rel:
            continue
        source_path = ROOT / source_rel
        if not source_path.exists():
            continue
        target_path = RECEIPT_DIR / f"{lane_slug(display)}-phase-v436-v1-imported-receipt-v1.md"
        text = source_path.read_text(encoding="utf-8", errors="replace")
        header = "\n".join(
            [
                f"Imported-From: {source_rel}",
                "Import-Policy: v436-v450 bridge preserves old v436 v1 truth without relaunching the CLI lane.",
                "",
            ]
        )
        write_text(target_path, header + text)
        copied = dict(receipt)
        copied["receipt_path"] = rel(target_path)
        copied["imported_from"] = source_rel
        imported_receipts.append(copied)
    if {item.get("lane") for item in imported_receipts} != set(REQUIRED_CLI_LANES):
        return None
    payload = {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "phase": PHASE_MIN,
        "run": "v1_cli_receipts",
        "artifact_id": f"{PREFIX}-sibling-phase-v436-v1-cli-receipts-v1",
        "status": "v1_cli_receipts_complete",
        "import_status": "imported_from_v421_v440_v436",
        "imported_from": rel(LEGACY_V436_AGGREGATE),
        "requested_max_steps": legacy.get("requested_max_steps"),
        "required_eureka_units_per_lane": legacy.get("required_eureka_units_per_lane", REQUIRED_EUREKA_UNITS),
        "lane_receipts": imported_receipts,
        "truth_boundaries": [
            "These receipts were produced by the old v421-v440 v436 real CLI run and imported once.",
            "The import prevents duplicate Arby, Kimi, or Aster Vale execution for v436.",
            "This completes v436 v1 only; v436 v2 still requires Aletheon-led App execution.",
            "Raw transport output remains quarantined and is not copied into the curated bridge packet.",
        ],
        "next_action": f"Continue v436 v2 with scripts/trinity_v436_v450_app_phase_runner.py --phase 436 --start.",
    }
    write_json(aggregate_json, payload)
    write_aggregate_md(aggregate_md, payload)
    return payload


def cli_aggregate_complete(phase: int) -> bool:
    aggregate, _ = aggregate_paths(phase)
    return read_json(aggregate, {}).get("status") == "v1_cli_receipts_complete"


def write_v2_active(phase: int, *, imported_v1: bool = False) -> dict[str, Any]:
    active_json, active_md = v2_active_paths(phase)
    aggregate_json, _ = aggregate_paths(phase)
    payload = {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "phase": phase,
        "run": "v2_app_execution",
        "status": "v2_app_run_active",
        "v1_cli_receipts": rel(aggregate_json),
        "v1_imported_from_legacy": imported_v1,
        "execution_policy": {
            "authority": "Aletheon-led App execution with Parfit, Cicero, and Kierkegaard advisory input when available.",
            "external_policy": "local_first_only",
            "allowed": ["repo/doc/script work", "local validation", "local browser or security inspection", "curated git publication"],
            "not_allowed_without_new_scope": ["Notion writes", "Google Drive writes", "cloud/provider mutation", "paid external actions", "account mutation"],
        },
        "truth_boundaries": [
            "This starts v2; it does not mark v2 complete.",
            "Aletheon must record concrete v2 outcomes before phase completion.",
            "From v437 onward, Parfit, Cicero, and Kierkegaard are official v2 App advisory receipt lanes.",
            "Promoted App advisory receipts do not replace Arby, Kimi, Aster Vale, or Aletheon-led v2 execution.",
        ],
        "next_action": (
            f"Collect Parfit/Cicero/Kierkegaard App advisory receipts, then complete v{phase} v2 with scripts/trinity_v436_v450_app_phase_runner.py --phase {phase} --complete --summary \"...\" --validation \"...\"."
            if phase >= PROMOTED_APP_RECEIPT_PHASE_MIN
            else f"After real App-side work and validation, run scripts/trinity_v436_v450_app_phase_runner.py --phase {phase} --complete --summary \"...\" --validation \"...\"."
        ),
    }
    write_json(active_json, payload)
    lines = [
        f"# v{phase} v2 App Run Active",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Imported v1 from legacy: `{imported_v1}`",
        "",
        "Truth boundaries:",
    ]
    lines.extend([f"- {item}" for item in payload["truth_boundaries"]])
    lines.extend(["", f"Next action: {payload['next_action']}"])
    write_text(active_md, "\n".join(lines))
    return payload


def validate_cli_gate(phase: int) -> dict[str, Any]:
    aggregate_json, _ = aggregate_paths(phase)
    gate = {
        "path": rel(aggregate_json),
        "status": "blocked_missing_v1_cli_receipts",
        "blockers": [],
    }
    payload = read_json(aggregate_json, {})
    if payload.get("status") != "v1_cli_receipts_complete":
        gate["blockers"].append(f"v{phase} v1 CLI receipt aggregate is not complete.")
        return gate
    for lane, surface in REQUIRED_CLI_LANES.items():
        receipt = next((item for item in payload.get("lane_receipts", []) if item.get("lane") == lane), None)
        if not receipt:
            gate["blockers"].append(f"Missing {lane} receipt.")
            continue
        if receipt.get("surface") != surface:
            gate["blockers"].append(f"{lane} receipt surface mismatch: {receipt.get('surface')}.")
        if receipt.get("receipt_status") != "valid_cli_receipt" or not receipt.get("valid"):
            gate["blockers"].append(f"{lane} receipt is not valid.")
    gate["status"] = "blocked_missing_v1_cli_receipts" if gate["blockers"] else "v1_cli_receipts_complete"
    return gate


def validate_app_advisory_gate(phase: int) -> dict[str, Any]:
    aggregate_json, _ = app_advisory_aggregate_paths(phase)
    gate = {
        "required": phase >= PROMOTED_APP_RECEIPT_PHASE_MIN,
        "path": rel(aggregate_json),
        "status": "not_required_before_v437",
        "blockers": [],
    }
    if phase < PROMOTED_APP_RECEIPT_PHASE_MIN:
        return gate
    payload = read_json(aggregate_json, {})
    if payload.get("status") != "v2_app_advisory_receipts_complete":
        gate["blockers"].append(f"v{phase} promoted App advisory receipt aggregate is not complete.")
    for advisor, config in PROMOTED_APP_RECEIPT_LANES.items():
        receipt = next((item for item in payload.get("lane_receipts", []) if item.get("advisor") == advisor), None)
        if not receipt:
            gate["blockers"].append(f"Missing {advisor} App advisory receipt.")
            continue
        if receipt.get("agent_id") != config["agent_id"]:
            gate["blockers"].append(f"{advisor} App advisory receipt has unexpected agent id.")
        if receipt.get("status") != "valid_app_advisory_receipt":
            gate["blockers"].append(f"{advisor} App advisory receipt is not valid.")
    gate["status"] = "blocked_missing_app_advisory_receipts" if gate["blockers"] else "v2_app_advisory_receipts_complete"
    return gate


def validate_v2_gate(phase: int) -> dict[str, Any]:
    receipt_json, _ = v2_receipt_paths(phase)
    gate = {"path": rel(receipt_json), "status": "blocked_missing_v2_app_receipt", "blockers": []}
    payload = read_json(receipt_json, {})
    if payload.get("status") != "v2_app_complete":
        gate["blockers"].append(f"v{phase} v2 App receipt is not complete.")
    if not payload.get("validations"):
        gate["blockers"].append("v2 App receipt must include at least one validation.")
    if payload.get("spent_external_usd", 0) != 0:
        gate["blockers"].append("v2 App receipt records external spend under local-first policy.")
    advisory_gate = validate_app_advisory_gate(phase)
    gate["app_advisory_receipt_gate"] = advisory_gate
    gate["blockers"].extend(advisory_gate["blockers"])
    gate["status"] = "blocked_missing_v2_app_receipt" if gate["blockers"] else "v2_app_complete"
    return gate
