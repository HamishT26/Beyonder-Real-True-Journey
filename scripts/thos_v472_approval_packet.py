#!/usr/bin/env python3
"""Build v472 THOS v2 approval-packet artifacts without live cache mutation."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE_X1 = "v472-thos-v2-x1"
PHASE_X2 = "v472-thos-v2-x2"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

APP_ADVISORIES = [
    {
        "lane": "Cicero",
        "submission_id": "019e884a-c48d-74d1-b87b-3db6f7cb8bbc",
        "status": "ADVISORY_RETURNED",
        "incorporated_focus": [
            "approval packet is not approval",
            "broad budget permission is not plugin-cache mutation consent",
            "exact path IDs and rollback evidence required before future live write",
        ],
    },
    {
        "lane": "Kierkegaard",
        "submission_id": "019e884b-1078-72b2-b356-760a36297196",
        "status": "ADVISORY_RETURNED",
        "incorporated_focus": [
            "tempdir preview is rehearsal only",
            "future write plan is not current write",
            "THOS tooling does not close GMUT gates",
        ],
    },
    {
        "lane": "Aristotle",
        "submission_id": "019e884b-5ab1-72e2-b7ea-f078143c4af3",
        "status": "ADVISORY_RETURNED",
        "incorporated_focus": [
            "37-entry schema",
            "relative path safety",
            "write_performed false and requires_path_specific_approval true",
            "rollback and post-write verification refs",
        ],
    },
]

CLI_LANES = [
    {
        "lane": "Arby",
        "path": "D:/GHC-Archives/agent-worktrees/v461-round-robin/arby-advisory",
        "status": "NO_FINAL_ADVISORY",
        "sandbox": "read-only",
        "ephemeral_flag_used": False,
        "completed_within_wait": False,
        "terminated_after_timeout": True,
        "stderr_signal": "missing YAML frontmatter skill-load failures",
    },
    {
        "lane": "Aster Vale",
        "path": "D:/GHC-Archives/agent-worktrees/v461-round-robin/aster-vale-advisory",
        "status": "NO_FINAL_ADVISORY",
        "sandbox": "read-only",
        "ephemeral_flag_used": False,
        "completed_within_wait": False,
        "terminated_after_timeout": True,
        "stderr_signal": "missing YAML frontmatter skill-load failures",
    },
]

BROWSER_LEDGER = {
    "status": "PARTIAL_RECOVERY_VERIFIED",
    "verified_url": "https://openai.com/academy/codex-plugins-and-skills/",
    "verified_title": "Plugins and skills | OpenAI",
    "correct_methods": ["tab.url()", "tab.title()", "tab.playwright.locator(...).innerText(...)"],
    "incorrect_prior_method": "tab.playwright.url()",
    "claim_ceiling": "Browser direct iab is no longer absent in this thread, but this is tool-surface evidence only.",
}

SOURCE_ROUTES = [
    {
        "label": "OpenAI Academy - Codex plugins and skills",
        "url": "https://openai.com/academy/codex-plugins-and-skills",
        "use": "Primary OpenAI context for plugin versus skill boundaries and why plugin-cache repair needs careful governance.",
    },
    {
        "label": "OpenAI Help - Codex CLI getting started",
        "url": "https://help.openai.com/en/articles/11096431",
        "use": "Primary OpenAI context for Codex CLI local-agent behavior, sandbox, and approval-mode framing.",
    },
    {
        "label": "OpenAI MCP docs",
        "url": "https://platform.openai.com/docs/mcp/",
        "use": "Primary OpenAI context for connector/MCP prompt-injection and private-source safety boundaries.",
    },
    {
        "label": "NVIDIA CUDA Windows installation guide",
        "url": "https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html",
        "use": "Primary NVIDIA context for Windows accelerator setup and checksum/installation verification discipline.",
    },
]

RAW_BODY_FIELD_RE = re.compile(r"(body_text|original_text|after_text|before_text|raw_body|plugin_body)", re.IGNORECASE)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def build_entries(manifest: dict[str, Any], preview: dict[str, Any]) -> list[dict[str, Any]]:
    manifest_rows = {item["relative_path"]: item for item in manifest.get("skills", [])}
    preview_rows = {item["relative_path"]: item for item in preview.get("preview", {}).get("entries", [])}

    require(len(manifest_rows) == 37, f"expected 37 manifest rows, found {len(manifest_rows)}")
    require(len(preview_rows) == 37, f"expected 37 preview rows, found {len(preview_rows)}")
    require(set(manifest_rows) == set(preview_rows), "manifest and preview path sets differ")

    entries: list[dict[str, Any]] = []
    for index, relative_path in enumerate(sorted(manifest_rows), start=1):
        manifest_row = manifest_rows[relative_path]
        preview_row = preview_rows[relative_path]
        sha256_before = manifest_row.get("sha256_before") or manifest_row.get("content_hash")
        before_hash = preview_row.get("before_hash")
        after_hash = preview_row.get("after_hash")

        entry = {
            "approval_status": "NOT_APPROVED",
            "body_preserved_in_temp_candidate": bool(preview_row.get("body_preserved_in_temp_candidate")),
            "candidate_frontmatter_valid": bool(preview_row.get("candidate_frontmatter_valid")),
            "entry_index": index,
            "entry_id": preview_row.get("entry_id") or manifest_row.get("path_id"),
            "issue_codes": manifest_row.get("issue_codes", []),
            "line_delta": preview_row.get("line_delta"),
            "path_id": manifest_row.get("path_id"),
            "path_safe": path_safe(relative_path) and bool(preview_row.get("path_safe")),
            "post_write_verification_ref": f"{PHASE_X1}-rollback-verification-plan-v1.json",
            "proposed_change_kind": "frontmatter_repair_preview_only",
            "proposed_frontmatter": preview_row.get("proposed_frontmatter", {}),
            "raw_body_text_included": False,
            "relative_path": relative_path,
            "requires_path_specific_approval": True,
            "rollback_plan_ref": f"{PHASE_X1}-rollback-verification-plan-v1.json",
            "sha256_after_preview": after_hash,
            "sha256_before": sha256_before,
            "source_checksum_unchanged": bool(preview_row.get("source_checksum_unchanged")),
            "source_preview_before_hash": before_hash,
            "write_performed": False,
            "write_target": "none_live_packet_only",
        }
        entries.append(entry)
    return entries


def validate_entries(entries: list[dict[str, Any]], preview: dict[str, Any], regression: dict[str, Any]) -> list[dict[str, Any]]:
    raw_body_fields = sorted({name for name in collect_field_names(entries) if RAW_BODY_FIELD_RE.search(name)})
    unexpected_raw_fields = [name for name in raw_body_fields if name != "raw_body_text_included"]
    checks = [
        row("entry_count", "PASS_SHAPE_ONLY" if len(entries) == 37 else "FAIL_BLOCKER", "Approval packet must carry exactly 37 path rows", {"count": len(entries)}),
        row("relative_path_safety", "PASS_SHAPE_ONLY" if all(entry["path_safe"] for entry in entries) else "FAIL_BLOCKER", "All rows must use safe relative paths only"),
        row("hash_presence", "PASS_SHAPE_ONLY" if all(entry["sha256_before"] and entry["sha256_after_preview"] for entry in entries) else "FAIL_BLOCKER", "All rows must carry before and preview-after hashes"),
        row("no_live_writes", "PASS_SHAPE_ONLY" if not any(entry["write_performed"] for entry in entries) else "FAIL_BLOCKER", "Approval packet must not perform live writes"),
        row("approval_not_granted", "PASS_SHAPE_ONLY" if all(entry["approval_status"] in {"NOT_APPROVED", "NOT_REQUESTED"} for entry in entries) else "FAIL_BLOCKER", "Approval packet cannot mark plugin-cache rows approved"),
        row("path_specific_approval_required", "PASS_SHAPE_ONLY" if all(entry["requires_path_specific_approval"] for entry in entries) else "FAIL_BLOCKER", "Every plugin-cache row must require future exact path-specific approval"),
        row("raw_body_absence", "PASS_SHAPE_ONLY" if not unexpected_raw_fields and not any(entry["raw_body_text_included"] for entry in entries) else "FAIL_BLOCKER", "No raw plugin body text or body fields may be included", unexpected_raw_fields),
        row("frontmatter_candidate_validity", "PASS_SHAPE_ONLY" if all(entry["candidate_frontmatter_valid"] for entry in entries) else "FAIL_BLOCKER", "All tempdir frontmatter candidates must parse as candidate frontmatter"),
        row("body_preservation_rehearsal", "PASS_SHAPE_ONLY" if all(entry["body_preserved_in_temp_candidate"] for entry in entries) else "FAIL_BLOCKER", "Tempdir candidates must preserve original body suffixes"),
        row("source_checksum_stability", "PASS_SHAPE_ONLY" if all(entry["source_checksum_unchanged"] for entry in entries) else "FAIL_BLOCKER", "Source files must remain unchanged by preview chain"),
        row("prior_preview_status", preview.get("aggregate_status", "OPEN_GAP"), "v471 tempdir diff preview status is carried forward"),
        row("prior_regression_status", regression.get("aggregate_status", "OPEN_GAP"), "v472 v1 regression status is carried forward"),
    ]
    return checks


def aggregate_status(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] == "OPEN_GAP" for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def write_artifacts(root: Path) -> list[Path]:
    manifest_ref = "v471-thos-v5-x1-plugin-cache-affected-manifest-v1.json"
    preview_ref = "v471-thos-v7-x1-tempdir-diff-preview-v1.json"
    regression_ref = "v472-thos-v1-x1-regression-guard-v1.json"
    manifest = read_json(root / manifest_ref)
    preview = read_json(root / preview_ref)
    regression = read_json(root / regression_ref)

    entries = build_entries(manifest, preview)
    checks = validate_entries(entries, preview, regression)
    status = aggregate_status(checks)
    generated_at = utc_now()
    written: list[Path] = []

    approval_packet = {
        "aggregate_status": status,
        "app_advisories": APP_ADVISORIES,
        "approval_packet_id": f"{PHASE_X1}-plugin-cache-live-repair-approval-request-v1",
        "approval_status": "NOT_APPROVED_PACKET_ONLY",
        "broad_live_write_ceiling_received": True,
        "broad_live_write_ceiling_usd": 100,
        "browser_method_correction": BROWSER_LEDGER,
        "claim_ceiling": [
            "This packet is a path-specific approval request, not approval.",
            "No live plugin-cache write, quarantine, deletion, or repair was performed.",
            "The user-approved $100 ceiling authorizes scoped phase work, not exact plugin-cache mutation.",
            "Future plugin-cache mutation requires a separate exact path-specific approval.",
        ],
        "cli_lanes": CLI_LANES,
        "entry_count_observed": len(entries),
        "entry_count_required": 37,
        "entries": entries,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": checks,
        "source_artifacts": {
            "manifest": manifest_ref,
            "preview": preview_ref,
            "regression_guard": regression_ref,
        },
    }
    path = root / f"{PHASE_X1}-live-repair-approval-packet-v1.json"
    write_json(path, approval_packet)
    written.append(path)
    write_md(
        root / f"{PHASE_X1}-live-repair-approval-packet-v1.md",
        f"""
# v472 THOS v2 x1 Live-Repair Approval Packet

Status: `{status}`.

This artifact packages 37 plugin-cache frontmatter repair candidates as an approval request only. It records relative paths, path IDs, before hashes, preview-after hashes, proposed frontmatter metadata, rollback references, and post-write verification references. It does not include raw plugin body text and it performs no live plugin-cache write.

The approved `$100` THOS/GMUT work ceiling is recorded as broad phase authorization only. It is not treated as exact path-specific approval for plugin-cache mutation.
""",
    )
    written.append(root / f"{PHASE_X1}-live-repair-approval-packet-v1.md")

    risk_rows = [
        row("approval_confusion", "OPEN_GAP", "Approval packet could be mistaken for approval unless future prompts preserve the NOT_APPROVED_PACKET_ONLY state"),
        row("budget_confusion", "OPEN_GAP", "The $100 spend ceiling could be mistaken for plugin-cache mutation consent; this packet forbids that interpretation"),
        row("tempdir_confusion", "OPEN_GAP", "Preview hashes prove candidate shape only, not live repair"),
        row("browser_durability", "OPEN_GAP", "Browser worked in this turn with corrected methods, but future surface availability must still be rechecked"),
        row("cli_skill_loader", "OPEN_GAP", "Arby and Aster still show missing YAML frontmatter skill-load failures and no final advisory"),
        row("gmut_claim_boundary", "PASS_SHAPE_ONLY", "THOS repair governance does not close any GMUT gate"),
    ]
    risk_register = {
        "aggregate_status": aggregate_status(risk_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "risks": risk_rows,
    }
    path = root / f"{PHASE_X1}-path-specific-risk-register-v1.json"
    write_json(path, risk_register)
    written.append(path)
    write_md(
        root / f"{PHASE_X1}-path-specific-risk-register-v1.md",
        """
# v472 THOS v2 x1 Path-Specific Risk Register

The main risks are approval confusion, budget confusion, tempdir-preview confusion, Browser durability, CLI skill-loader failure, and GMUT claim bleed. The packet keeps all plugin-cache rows unapproved and all GMUT gates open.
""",
    )
    written.append(root / f"{PHASE_X1}-path-specific-risk-register-v1.md")

    rollback_steps = [
        "Fetch and drift-check omega before any future approved mutation.",
        "Verify the exact path list equals this packet's 37 relative paths.",
        "For each path, confirm live sha256 equals sha256_before before writing.",
        "Apply only the approved frontmatter-only diff for that exact path.",
        "Re-hash each file and compare to sha256_after_preview.",
        "Parse YAML frontmatter for required name and description fields.",
        "Run no-raw-body and path-safety guards before publishing any receipt.",
        "If any check fails, stop; do not auto-rollback without exact approval unless the future approval explicitly includes rollback execution.",
    ]
    rollback_plan = {
        "aggregate_status": "PASS_SHAPE_ONLY",
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rollback_execution_approved_now": False,
        "steps": rollback_steps,
        "verification_requirements": [
            "exact path-specific approval receipt",
            "before-hash match for every path",
            "after-hash match for every path",
            "frontmatter parse pass for every path",
            "no raw body text in curated receipts",
            "curated exact staging only",
        ],
    }
    path = root / f"{PHASE_X1}-rollback-verification-plan-v1.json"
    write_json(path, rollback_plan)
    written.append(path)
    write_md(
        root / f"{PHASE_X1}-rollback-verification-plan-v1.md",
        """
# v472 THOS v2 x1 Rollback and Verification Plan

Future live repair requires exact path-specific approval, before-hash verification, frontmatter-only mutation, after-hash verification, YAML parse checks, no-raw-body receipts, and curated exact staging. No rollback execution is approved by this packet.
""",
    )
    written.append(root / f"{PHASE_X1}-rollback-verification-plan-v1.md")

    source_ledger = {
        "aggregate_status": "PASS_SHAPE_ONLY",
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "source_routes": SOURCE_ROUTES,
        "use_ceiling": "Source routes support THOS tooling and safety context only; they do not validate GMUT physics or authorize plugin-cache mutation.",
    }
    path = root / f"{PHASE_X1}-source-routing-ledger-v1.json"
    write_json(path, source_ledger)
    written.append(path)
    write_md(
        root / f"{PHASE_X1}-source-routing-ledger-v1.md",
        """
# v472 THOS v2 x1 Source Routing Ledger

Official OpenAI and NVIDIA routes were carried for plugin/skill, CLI, MCP, and Windows accelerator-installation safety context. They support THOS routing only and do not close GMUT gates.
""",
    )
    written.append(root / f"{PHASE_X1}-source-routing-ledger-v1.md")

    x1_status = {
        "aggregate_status": status,
        "app_advisory_pass_completed": True,
        "browser_status": BROWSER_LEDGER["status"],
        "cli_lane_status": "NO_FINAL_ADVISORY_FROM_ARBY_OR_ASTER",
        "generated_at_utc": generated_at,
        "gmUT_gates_open": GMUT_GATES,
        "mutation_performed": False,
        "next_expected_phase": PHASE_X2,
        "phase_slug": PHASE_X1,
        "summary": "Built the path-specific approval packet for 37 plugin-cache repair candidates without live mutation.",
    }
    path = root / f"{PHASE_X1}-run-status-v1.json"
    write_json(path, x1_status)
    written.append(path)
    write_md(
        root / f"{PHASE_X1}-run-status-v1.md",
        f"""
# v472 THOS v2 x1 Run Status

Status: `{status}`. Built approval-packet artifacts only. Browser method correction is recorded. Arby/Aster remain no-final-advisory due CLI skill-loader failures. All GMUT gates remain open.
""",
    )
    written.append(root / f"{PHASE_X1}-run-status-v1.md")

    handoff_rows = [
        row("x2_synthesis", "PASS_SHAPE_ONLY", "Use x2 to freeze claim ceilings and prepare v472 v3 expected-negative fixtures"),
        row("do_not_execute", "PASS_SHAPE_ONLY", "Do not execute plugin-cache live repair from this packet"),
        row("browser_next", "OPEN_GAP", "Future browser tasks should use tab.url()/tab.title() and recheck availability"),
        row("cli_next", "OPEN_GAP", "Future CLI repair should address missing YAML frontmatter loader failures first"),
    ]
    handoff = {
        "aggregate_status": aggregate_status(handoff_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_expected_phase": PHASE_X2,
        "phase_slug": PHASE_X1,
        "rows": handoff_rows,
    }
    path = root / f"{PHASE_X1}-x2-handoff-v1.json"
    write_json(path, handoff)
    written.append(path)
    write_md(
        root / f"{PHASE_X1}-x2-handoff-v1.md",
        """
# v472 THOS v2 x1 to x2 Handoff

x2 should freeze the approval claim ceiling, preserve no-write state, and route v472 v3 toward expected-negative fixtures rather than live plugin-cache mutation.
""",
    )
    written.append(root / f"{PHASE_X1}-x2-handoff-v1.md")

    x2_claim_rows = [
        row("packet_not_approval", "PASS_SHAPE_ONLY", "The approval packet is not approval"),
        row("budget_not_plugin_cache_consent", "PASS_SHAPE_ONLY", "The $100 ceiling is not exact plugin-cache mutation consent"),
        row("no_current_write", "PASS_SHAPE_ONLY", "No live plugin-cache write happened in v472 v2"),
        row("no_gmut_closure", "PASS_SHAPE_ONLY", "No GMUT gate was tested or closed"),
        row("no_journey_validation", "PASS_SHAPE_ONLY", "Journey/Solas context, if later used, remains journey_context_not_canon"),
    ]
    x2_claim = {
        "aggregate_status": aggregate_status(x2_claim_rows),
        "generated_at_utc": generated_at,
        "gmUT_gates_open": GMUT_GATES,
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": x2_claim_rows,
    }
    path = root / f"{PHASE_X2}-approval-claim-ceiling-v1.json"
    write_json(path, x2_claim)
    written.append(path)
    write_md(
        root / f"{PHASE_X2}-approval-claim-ceiling-v1.md",
        """
# v472 THOS v2 x2 Approval Claim Ceiling

x2 freezes the safety boundary: approval packet is not approval, budget is not plugin-cache consent, no current write occurred, no Journey/Solas material validates the repair, and no GMUT gate is closed.
""",
    )
    written.append(root / f"{PHASE_X2}-approval-claim-ceiling-v1.md")

    x2_handoff_rows = [
        row("v472_v3_option_a", "PASS_SHAPE_ONLY", "Build expected-negative fixture suite for invalid approval states"),
        row("v472_v3_option_b", "PASS_SHAPE_ONLY", "Add Browser API surface smoke probe using tab.url and tab.title"),
        row("v472_v3_option_c", "OPEN_GAP", "Diagnose CLI missing-frontmatter loader failures without mutating plugin cache"),
        row("v472_v3_option_d", "PASS_SHAPE_ONLY", "Keep all GMUT gates open unless exact closure artifacts exist"),
    ]
    x2_handoff = {
        "aggregate_status": aggregate_status(x2_handoff_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_expected_phase": "v472-thos-v3-x1",
        "phase_slug": PHASE_X2,
        "rows": x2_handoff_rows,
    }
    path = root / f"{PHASE_X2}-v472-thos-v3-handoff-v1.json"
    write_json(path, x2_handoff)
    written.append(path)
    write_md(
        root / f"{PHASE_X2}-v472-thos-v3-handoff-v1.md",
        """
# v472 THOS v2 x2 to v472 THOS v3 Handoff

Next best move: build expected-negative approval fixtures and a small Browser API smoke probe while keeping plugin-cache live mutation approval-gated.
""",
    )
    written.append(root / f"{PHASE_X2}-v472-thos-v3-handoff-v1.md")

    x2_status = {
        "aggregate_status": aggregate_status(x2_claim_rows + x2_handoff_rows),
        "commit_recommended": True,
        "generated_at_utc": generated_at,
        "gmUT_gates_open": GMUT_GATES,
        "mutation_performed": False,
        "next_expected_phase": "v472-thos-v3-x1",
        "phase_slug": PHASE_X2,
        "summary": "x2 freezes claim ceilings and hands v472 v3 to expected-negative approval fixtures plus Browser/CLI recovery.",
    }
    path = root / f"{PHASE_X2}-run-status-v1.json"
    write_json(path, x2_status)
    written.append(path)
    write_md(
        root / f"{PHASE_X2}-run-status-v1.md",
        """
# v472 THOS v2 x2 Run Status

x2 completes the approval claim ceiling and recommends a curated commit for the v472 v2 packet. Next expected phase is `v472-thos-v3-x1`.
""",
    )
    written.append(root / f"{PHASE_X2}-run-status-v1.md")

    return written


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    artifact_root = repo_root / "docs" / "trinity-live-traces"
    written = write_artifacts(artifact_root)
    print(json.dumps({"status": "PASS_WRITE_ARTIFACTS_ONLY", "written": [path.as_posix() for path in written]}, indent=2))


if __name__ == "__main__":
    main()
