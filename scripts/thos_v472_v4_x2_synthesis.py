#!/usr/bin/env python3
"""Build v472 THOS v4 x2 post-repair synthesis artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v472-thos-v4-x2"
NEXT_PHASE = "v472-thos-v5-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"

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
        "submission_id": "019e8891-5233-7061-b01f-e82a1a184735",
        "status": "ADVISORY_RETURNED",
        "summary": "Bound repair claims to observed loader categories; publish receipts only; v5 should add regression guards without GMUT overclaim.",
    },
    {
        "lane": "Kierkegaard",
        "submission_id": "019e8891-8d4d-7653-bede-1f8bccd13bb6",
        "status": "ADVISORY_RETURNED",
        "summary": "Loader repair is not broader platform health; retry success is not final advisory quality; THOS reliability does not close GMUT gates.",
    },
    {
        "lane": "Aristotle",
        "submission_id": "019e8891-d625-7b63-8acf-5ae24e9efa47",
        "status": "ADVISORY_RETURNED",
        "summary": "Publish repair summary, retry summary, Browser correction ledger, and v5 expected-negative fixture plan.",
    },
]

CLI_PROBES = [
    {
        "completed_within_wait": False,
        "ephemeral_flag_used": False,
        "lane": "Arby",
        "last_message_bytes": 0,
        "loader_error_counts": {
            "invalid_name": 0,
            "missing_frontmatter": 0,
            "stale_plugin_temp_access_denied": 0,
        },
        "runtime_warnings": [
            "stale curated plugins temp directory warning with os error 2",
            "PowerShell shell snapshot unsupported warning",
        ],
        "sandbox": "read-only",
        "terminated_after_timeout": True,
    },
    {
        "completed_within_wait": False,
        "ephemeral_flag_used": False,
        "lane": "Aster Vale",
        "last_message_bytes": 0,
        "loader_error_counts": {
            "invalid_name": 0,
            "missing_frontmatter": 0,
            "stale_plugin_temp_access_denied": 1,
        },
        "runtime_warnings": [
            "stale curated plugins temp directory warning with os error 5 access denied",
            "PowerShell shell snapshot unsupported warning",
        ],
        "sandbox": "read-only",
        "terminated_after_timeout": True,
    },
]

BROWSER_SMOKE = {
    "api_methods": ["tab.url()", "tab.title()", "tab.playwright.locator('body').innerText(...)"],
    "body_start_observed": "OpenAI Academy plugins and skills page body text observed",
    "claim_ceiling": "Browser smoke proves corrected method shape for this page only; it is not broad Browser durability.",
    "incorrect_prior_method": "tab.playwright.url()",
    "ok": True,
    "title": "Plugins and skills | OpenAI",
    "url": "https://openai.com/academy/codex-plugins-and-skills/",
}

EXPECTED_NEGATIVES = [
    "missing frontmatter delimiter",
    "leading UTF-8 BOM before raw frontmatter delimiter",
    "frontmatter without name",
    "frontmatter without description",
    "overlong plugin-prefixed skill name",
    "malformed YAML delimiter placement",
    "absolute or path-escaping repair target",
    "raw body text leaked into curated receipt",
    "unbounded CLI retry",
    "wrong Browser method tab.playwright.url",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(name: str) -> dict[str, Any]:
    return json.loads((ARTIFACT_ROOT / name).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def aggregate(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] == "OPEN_GAP" for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    v3_receipt = read_json("v472-thos-v3-x2-refreshed-live-repair-receipt-v1.json")
    v4_receipt = read_json("v472-thos-v4-x1-user-skill-bom-repair-receipt-v1.json")
    v4_retry = read_json("v472-thos-v4-x1-arby-aster-post-user-skill-retry-v1.json")

    plugin_verified = sum(
        item["status"] == "CURRENT_VALID_REPAIRED_NAME"
        for item in v3_receipt["plugin_cache_target_verification"]
    )
    user_skill_writes = v4_receipt["writes_performed"]
    retry_missing = sum(item["loader_error_counts"]["missing_frontmatter"] for item in v4_retry["retries"])
    retry_invalid = sum(item["loader_error_counts"]["invalid_name"] for item in v4_retry["retries"])
    x2_missing = sum(item["loader_error_counts"]["missing_frontmatter"] for item in CLI_PROBES)
    x2_invalid = sum(item["loader_error_counts"]["invalid_name"] for item in CLI_PROBES)
    x2_stale_temp = sum(item["loader_error_counts"]["stale_plugin_temp_access_denied"] for item in CLI_PROBES)

    written: list[Path] = []

    repair_rows = [
        row("plugin_cache_names", "PASS_SHAPE_ONLY" if plugin_verified == 8 else "FAIL_BLOCKER", "Eight plugin-cache invalid-name targets are verified current-valid", {"verified": plugin_verified}),
        row("user_skill_bom", "PASS_SHAPE_ONLY" if user_skill_writes == 6 else "FAIL_BLOCKER", "Six approved user-skill BOM removals were performed", {"writes": user_skill_writes}),
        row("post_repair_retry", "PASS_SHAPE_ONLY" if retry_missing == 0 and retry_invalid == 0 else "FAIL_BLOCKER", "Post-repair retry has zero missing-frontmatter and invalid-name errors", {"missing": retry_missing, "invalid": retry_invalid}),
        row("x2_cli_probe", "PASS_SHAPE_ONLY" if x2_missing == 0 and x2_invalid == 0 else "FAIL_BLOCKER", "v4 x2 CLI probes preserve zero loader-class errors", {"missing": x2_missing, "invalid": x2_invalid}),
        row("stale_temp_hygiene", "OPEN_GAP" if x2_stale_temp else "PASS_SHAPE_ONLY", "Aster still shows a stale temp plugin-clone access warning; no cleanup was performed", {"signals": x2_stale_temp}),
    ]
    repair_summary = {
        "aggregate_status": aggregate(repair_rows),
        "app_advisories": APP_ADVISORIES,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "mutation_performed": False,
        "phase_slug": PHASE,
        "rows": repair_rows,
        "source_receipts": [
            "v472-thos-v3-x2-refreshed-live-repair-receipt-v1.json",
            "v472-thos-v4-x1-user-skill-bom-repair-receipt-v1.json",
            "v472-thos-v4-x1-arby-aster-post-user-skill-retry-v1.json",
        ],
    }
    path = ARTIFACT_ROOT / f"{PHASE}-loader-repair-summary-v1.json"
    write_json(path, repair_summary)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-loader-repair-summary-v1.md",
        """
# v472 THOS v4 x2 Loader Repair Summary

The v472 repair chain cleared the inspected plugin-cache invalid-name and user-skill BOM/frontmatter loader errors. Remaining scope is runtime hygiene, not GMUT validation.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-loader-repair-summary-v1.md")

    retry_rows = [
        row("arby_loader", "PASS_SHAPE_ONLY", "Arby v4 x2 probe has zero missing-frontmatter and invalid-name loader errors", CLI_PROBES[0]["loader_error_counts"]),
        row("aster_loader", "PASS_SHAPE_ONLY", "Aster v4 x2 probe has zero missing-frontmatter and invalid-name loader errors", CLI_PROBES[1]["loader_error_counts"]),
        row("final_message_quality", "OPEN_GAP", "Arby/Aster still timed out without final advisory messages in the bounded wait"),
        row("stale_temp", "OPEN_GAP", "Aster still emitted a stale temp plugin-clone access warning; deletion was not performed"),
    ]
    retry_summary = {
        "aggregate_status": aggregate(retry_rows),
        "cli_probes": CLI_PROBES,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE,
        "rows": retry_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-arby-aster-retry-receipt-summary-v1.json"
    write_json(path, retry_summary)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-arby-aster-retry-receipt-summary-v1.md",
        """
# v472 THOS v4 x2 Arby/Aster Retry Summary

Read-only non-ephemeral probes now pass the previous skill-loader class, but final advisory return and stale-temp runtime hygiene remain open.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-arby-aster-retry-receipt-summary-v1.md")

    browser_rows = [
        row("browser_smoke", "PASS_SHAPE_ONLY", "Browser smoke reached the OpenAI Academy plugins/skills page", BROWSER_SMOKE),
        row("method_correction", "PASS_SHAPE_ONLY", "Use tab.url()/tab.title(); do not use tab.playwright.url()"),
        row("durability_claim", "OPEN_GAP", "This is a bounded smoke result, not broad Browser durability"),
    ]
    browser_ledger = {
        "aggregate_status": aggregate(browser_rows),
        "browser_smoke": BROWSER_SMOKE,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE,
        "rows": browser_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-browser-method-correction-ledger-v1.json"
    write_json(path, browser_ledger)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-browser-method-correction-ledger-v1.md",
        """
# v472 THOS v4 x2 Browser Method Ledger

Browser smoke passed with `tab.url()` and `tab.title()`. The old `tab.playwright.url()` method remains an expected-negative case.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-browser-method-correction-ledger-v1.md")

    v5_rows = [
        row("expected_negative_fixtures", "PASS_SHAPE_ONLY", "v5 should materialize expected-negative skill-loader and Browser-method fixtures", EXPECTED_NEGATIVES),
        row("skill_loader_guard", "PASS_SHAPE_ONLY", "v5 should scan for missing frontmatter, BOM-before-frontmatter, invalid names, malformed delimiters, and raw-body leakage"),
        row("runtime_hygiene", "OPEN_GAP", "v5 may inspect stale temp plugin-clone warnings, but cleanup requires exact scoped evidence"),
        row("claim_ceiling", "PASS_SHAPE_ONLY", "v5 must continue THOS reliability only; all GMUT gates remain open"),
    ]
    handoff = {
        "aggregate_status": aggregate(v5_rows),
        "expected_negative_fixtures": EXPECTED_NEGATIVES,
        "generated_at_utc": generated_at,
        "gmUT_gates_open": GMUT_GATES,
        "mutation_performed": False,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": v5_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-v472-thos-v5-handoff-v1.json"
    write_json(path, handoff)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-v472-thos-v5-handoff-v1.md",
        """
# v472 THOS v4 x2 to v5 Handoff

Next: build a skill-loader regression guard with expected-negative fixtures, keep Browser smoke bounded, and preserve no-GMUT-closure claims.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-v472-thos-v5-handoff-v1.md")

    status_payload = {
        "aggregate_status": "OPEN_GAP_RUNTIME_HYGIENE",
        "generated_at_utc": generated_at,
        "gmUT_gates_open": GMUT_GATES,
        "mutation_performed": False,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "summary": "v4 x2 confirms loader-class repair success and carries forward final-advisory timeout plus stale-temp runtime hygiene gaps.",
    }
    path = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(path, status_payload)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md",
        """
# v472 THOS v4 x2 Run Status

Loader-class errors are clear in the inspected Arby/Aster probes. Remaining gaps are bounded final-message timeout and stale-temp runtime hygiene.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md")

    return written


def main() -> None:
    written = write_artifacts()
    print(json.dumps({"status": "PASS_WRITE_ARTIFACTS_ONLY", "written": [path.as_posix() for path in written]}, indent=2))


if __name__ == "__main__":
    main()
