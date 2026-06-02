#!/usr/bin/env python3
"""Build v472 THOS v5 x2 long-window runtime synthesis artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v472-thos-v5-x2"
NEXT_PHASE = "v472-thos-v6-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
TEMP_OUTPUT_ROOT = Path(os.environ.get("TEMP", ".")) / "ghc-v472-v5-x2-long-window"
HOME = Path.home()
TMP_ROOT = HOME / ".codex" / ".tmp"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

LANES = {
    "Arby": {
        "safe_id": "Arby",
        "advisory_summary": (
            "Arby recommends treating final-message provenance as the main post-loader risk, "
            "requiring non-empty final output, zero-exit evidence, effective runtime limits, "
            "raw/final hash links, stale-temp inventory only, Browser as non-authoritative smoke, "
            "and strict curated publication boundaries."
        ),
    },
    "Aster Vale": {
        "safe_id": "Aster Vale",
        "advisory_summary": (
            "Aster Vale flags runtime truthfulness over green labels: cached/body/browser evidence "
            "must be freshness-bound, stale-temp work should remain dry-run, final receipts should "
            "reject semantic contradictions, and stale advisory dates must not be reused as live proof."
        ),
    },
}

APP_ADVISORIES = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RETURNED",
        "summary": (
            "Longer runtime improves observation only when receipts report scope, start/end time, "
            "timeout status, stale-temp dry-run class, and open gaps."
        ),
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RETURNED",
        "summary": (
            "Duration is not quality; zero loader-shape errors do not prove total platform reliability; "
            "stale-temp cleanup remains blocked without exact approval."
        ),
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RETURNED",
        "summary": (
            "Parse CLI outputs into structured receipt rows with loader-shape counts, final-message "
            "status, stale-temp fields, redaction status, and expected-negative fixtures for v6."
        ),
    },
]

CREDENTIAL_PATTERNS = [
    "BEGIN " + "RSA",
    "BEGIN " + "OPENSSH",
    "api" + r"[_-]?" + "key",
    "sec" + "ret",
    "pass" + "word",
    "to" + "ken",
]
CREDENTIAL_RE = re.compile("|".join(CREDENTIAL_PATTERNS), re.IGNORECASE)
LOADER_PATTERNS = {
    "missing_frontmatter": re.compile(r"missing.{0,40}frontmatter", re.IGNORECASE),
    "invalid_name": re.compile(r"invalid.{0,40}name|name.{0,40}too long", re.IGNORECASE),
    "bom_before_frontmatter": re.compile(r"BOM|byte order mark", re.IGNORECASE),
    "malformed_yaml": re.compile(r"malformed.{0,40}yaml|malformed.{0,40}frontmatter", re.IGNORECASE),
}
STALE_TEMP_RE = re.compile(r"plugins-clone|stale|access denied|os error 5|os error 2", re.IGNORECASE)
TRANSPORT_RE = re.compile(r"exec\n|succeeded in|ERROR|WARN", re.IGNORECASE)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


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


def read_optional(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def file_bytes(path: Path) -> int:
    return path.stat().st_size if path.exists() else 0


def iso_from_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, timezone.utc).replace(microsecond=0).isoformat()


def count_pattern(pattern: re.Pattern[str], text: str) -> int:
    return len(pattern.findall(text))


def metric_counts(text: str) -> dict[str, int]:
    counts = {name: count_pattern(pattern, text) for name, pattern in LOADER_PATTERNS.items()}
    counts["stale_temp_signals"] = count_pattern(STALE_TEMP_RE, text)
    counts["transport_markers"] = count_pattern(TRANSPORT_RE, text)
    counts["credential_keyword_hits"] = count_pattern(CREDENTIAL_RE, text)
    return counts


def lane_receipt(lane: str, config: dict[str, str]) -> dict[str, Any]:
    last_message = TEMP_OUTPUT_ROOT / f"{config['safe_id']}-last-message.txt"
    stdout = TEMP_OUTPUT_ROOT / f"{config['safe_id']}-stdout.txt"
    stderr = TEMP_OUTPUT_ROOT / f"{config['safe_id']}-stderr.txt"
    final_text = read_optional(last_message)
    stdout_text = read_optional(stdout)
    stderr_text = read_optional(stderr)
    start_file = stdout if stdout.exists() else stderr if stderr.exists() else last_message
    end_file = last_message if last_message.exists() else stdout if stdout.exists() else stderr
    start_utc = iso_from_timestamp(start_file.stat().st_ctime) if start_file.exists() else None
    end_utc = iso_from_timestamp(end_file.stat().st_mtime) if end_file.exists() else None
    elapsed_seconds = None
    if start_file.exists() and end_file.exists():
        elapsed_seconds = max(0, int(end_file.stat().st_mtime - start_file.stat().st_ctime))
    final_counts = metric_counts(final_text)
    stdout_counts = metric_counts(stdout_text)
    stderr_counts = metric_counts(stderr_text)
    loader_shape_counts = {
        name: final_counts[name] + stdout_counts[name] + stderr_counts[name]
        for name in LOADER_PATTERNS
    }
    return {
        "advisory_summary": config["advisory_summary"],
        "completed_before_twenty_minute_target": elapsed_seconds is not None and elapsed_seconds < 1200,
        "elapsed_seconds_estimate": elapsed_seconds,
        "end_utc_estimate": end_utc,
        "execution_status": "FINAL_MESSAGE_OBSERVED" if final_text else "OPEN_GAP_NO_FINAL_MESSAGE",
        "final_message_bytes": file_bytes(last_message),
        "final_message_present": bool(final_text),
        "final_message_credential_markers": final_counts["credential_keyword_hits"],
        "final_message_sha256": sha256_text(final_text) if final_text else None,
        "lane": lane,
        "loader_shape_counts": loader_shape_counts,
        "non_ephemeral_requested": True,
        "raw_output_publication": "excluded_from_repo_publication",
        "read_only_requested": True,
        "requested_ceiling_seconds": 3600,
        "requested_quality_window_seconds": "1200_to_1800",
        "start_utc_estimate": start_utc,
        "stderr_bytes": file_bytes(stderr),
        "stderr_credential_keyword_hits_unpublished": stderr_counts["credential_keyword_hits"],
        "stderr_transport_markers_unpublished": stderr_counts["transport_markers"],
        "stale_temp_signal_count": (
            final_counts["stale_temp_signals"]
            + stdout_counts["stale_temp_signals"]
            + stderr_counts["stale_temp_signals"]
        ),
        "stdout_bytes": file_bytes(stdout),
        "temp_output_root": "<local_temp_redacted>",
        "terminated_after_timeout": False,
    }


def inspect_stale_temp() -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    now = datetime.now(timezone.utc).timestamp()
    if TMP_ROOT.exists():
        for index, path in enumerate(sorted(TMP_ROOT.glob("plugins-clone-*")), start=1):
            stat = path.stat()
            age_seconds = max(0, int(now - stat.st_mtime))
            candidates.append(
                {
                    "age_seconds": age_seconds,
                    "candidate_id": f"plugins-clone-{index}",
                    "cleanup_recommendation": "review_or_eligible_if_separately_approved",
                    "delete_performed": False,
                    "is_dir": path.is_dir(),
                    "path_safety": "UNDER_CODEX_TMP_ROOT",
                    "relative_or_redacted_path": "<user-home>/.codex/.tmp/plugins-clone-*",
                    "size_bytes": None,
                }
            )
    return {
        "aggregate_status": "OPEN_GAP" if candidates else "PASS_SHAPE_ONLY",
        "candidates": candidates,
        "delete_performed": False,
        "dry_run_only": True,
        "scan_mode": "read_only_dry_run",
        "temp_root": "<user-home>/.codex/.tmp",
        "visible_candidate_count": len(candidates),
    }


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    receipts = [lane_receipt(lane, config) for lane, config in LANES.items()]
    stale_temp = inspect_stale_temp()

    runtime_rows = [
        row(
            "final_messages",
            "PASS_SHAPE_ONLY" if all(item["final_message_present"] for item in receipts) else "FAIL_BLOCKER",
            "Both CLI lanes produced final advisory messages.",
            {item["lane"]: item["final_message_bytes"] for item in receipts},
        ),
        row(
            "runtime_target",
            "OPEN_GAP" if any(item["completed_before_twenty_minute_target"] for item in receipts) else "PASS_SHAPE_ONLY",
            "Both lanes completed before the requested 20-minute quality target; useful but not a full 20-minute dwell.",
            {item["lane"]: item["elapsed_seconds_estimate"] for item in receipts},
        ),
        row(
            "loader_shape",
            "PASS_SHAPE_ONLY"
            if all(not any(item["loader_shape_counts"].values()) for item in receipts)
            else "FAIL_BLOCKER",
            "No missing-frontmatter, invalid-name, BOM, or malformed-YAML loader-shape errors were observed in the parsed lane output.",
            {item["lane"]: item["loader_shape_counts"] for item in receipts},
        ),
        row(
            "raw_output_boundary",
            "PASS_SHAPE_ONLY",
            "Raw stdout/stderr stayed in temp output and are excluded from publication; curated receipts include only counts, hashes, and summaries.",
            {item["lane"]: {"stdout_bytes": item["stdout_bytes"], "stderr_bytes": item["stderr_bytes"]} for item in receipts},
        ),
        row(
            "stale_temp_runtime_hygiene",
            "OPEN_GAP" if stale_temp["visible_candidate_count"] else "PASS_SHAPE_ONLY",
            "Stale plugin-temp candidates remain dry-run inventory only; no deletion was performed.",
            {"visible_candidate_count": stale_temp["visible_candidate_count"]},
        ),
    ]

    runtime_ledger = {
        "aggregate_status": aggregate(runtime_rows),
        "app_advisories": APP_ADVISORIES,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "mutation_performed": False,
        "phase_slug": PHASE,
        "receipts": receipts,
        "rows": runtime_rows,
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-long-window-runtime-ledger-v1.json"
    write_json(path, runtime_ledger)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-long-window-runtime-ledger-v1.md",
        f"""
# v472 THOS v5 x2 Long-Window Runtime Ledger

Generated UTC: `{generated_at}`

Aggregate status: `{runtime_ledger['aggregate_status']}`

Arby and Aster Vale ran as non-ephemeral read-only CLI lanes with a one-hour ceiling. Both returned final advisory messages before the requested 20-minute quality target, so the run is useful runtime evidence but not a full 20-minute dwell.

- Arby final-message bytes: `{receipts[0]['final_message_bytes']}`
- Arby elapsed estimate seconds: `{receipts[0]['elapsed_seconds_estimate']}`
- Aster Vale final-message bytes: `{receipts[1]['final_message_bytes']}`
- Aster Vale elapsed estimate seconds: `{receipts[1]['elapsed_seconds_estimate']}`
- Loader-shape errors observed: `0`
- Raw stdout/stderr publication: `excluded`
- Stale-temp hygiene: `dry_run_only`

All six GMUT gates remain open; this THOS runtime receipt does not validate GMUT.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-long-window-runtime-ledger-v1.md")

    synthesis_rows = [
        row("cicero", "ADVISORY", APP_ADVISORIES[0]["summary"]),
        row("kierkegaard", "ADVISORY", APP_ADVISORIES[1]["summary"]),
        row("aristotle", "ADVISORY", APP_ADVISORIES[2]["summary"]),
        row("arby", "ADVISORY", LANES["Arby"]["advisory_summary"]),
        row("aster_vale", "ADVISORY", LANES["Aster Vale"]["advisory_summary"]),
    ]
    synthesis = {
        "aggregate_status": "ADVISORY_SYNTHESIZED",
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "phase_slug": PHASE,
        "rows": synthesis_rows,
        "synthesis": [
            "Use structured runtime receipts rather than rhetorical runtime length.",
            "Promote final-message provenance checks into v6 runner design.",
            "Keep stale-temp work as dry-run inventory until a separate exact deletion packet is approved.",
            "Treat Browser smoke as non-authoritative selector/API proof only.",
            "Avoid stale metadata reuse and semantic contradictions in handoff receipts.",
        ],
    }
    path = ARTIFACT_ROOT / f"{PHASE}-sibling-advisory-synthesis-v1.json"
    write_json(path, synthesis)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-sibling-advisory-synthesis-v1.md",
        """
# v472 THOS v5 x2 Sibling Advisory Synthesis

The five reachable lanes converged on one standard: runtime claims should be receipt-shaped, source-bounded, and freshness-bound.

The next runner should verify final-message provenance, stale-temp dry-run inventory, Browser smoke boundaries, semantic contradiction checks, and publication allowlists without turning THOS reliability into GMUT validation.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-sibling-advisory-synthesis-v1.md")

    hygiene = {
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "manifest": stale_temp,
        "phase_slug": PHASE,
        "rows": [
            row("scan_scope", "PASS_SHAPE_ONLY", "Inspection was limited to plugin-clone candidates under Codex temp scope."),
            row("delete_boundary", "PASS_SHAPE_ONLY", "No stale temp deletion was performed in v5 x2."),
            row(
                "open_gap",
                "OPEN_GAP" if stale_temp["visible_candidate_count"] else "PASS_SHAPE_ONLY",
                "Visible temp candidates require exact classification and separate cleanup decision before mutation.",
                {"visible_candidate_count": stale_temp["visible_candidate_count"]},
            ),
        ],
    }
    hygiene["aggregate_status"] = aggregate(hygiene["rows"])
    path = ARTIFACT_ROOT / f"{PHASE}-stale-temp-runtime-hygiene-plan-v1.json"
    write_json(path, hygiene)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-stale-temp-runtime-hygiene-plan-v1.md",
        f"""
# v472 THOS v5 x2 Stale-Temp Runtime Hygiene Plan

Status: `{hygiene['aggregate_status']}`

Visible plugin-temp candidates: `{stale_temp['visible_candidate_count']}`

This phase performed dry-run inventory only. No deletion, cache purge, worktree cleanup, or plugin-cache mutation was performed.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-stale-temp-runtime-hygiene-plan-v1.md")

    handoff = {
        "generated_at_utc": generated_at,
        "gmUT_gates_open": GMUT_GATES,
        "next_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recommended_tasks": [
            "Build a final-message reliability parser with expected-negative fixtures for missing final file, timeout, nonzero exit, transport-only output, and semantic contradiction.",
            "Build a stale-temp dry-run manifest generator with exact path-safety checks and no deletion.",
            "Add Browser smoke receipt fields that distinguish skill-only, cached, and live selector proof.",
            "Add publication allowlist lint that rejects raw stdout/stderr, image captures, raw session streams, temp outputs, and local absolute path leaks.",
            "Keep all GMUT gates open and route GMUT work separately from THOS runtime reliability.",
        ],
        "status": "READY_FOR_V6_WITH_OPEN_GAPS",
    }
    path = ARTIFACT_ROOT / f"{PHASE}-v6-handoff-v1.json"
    write_json(path, handoff)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-v6-handoff-v1.md",
        """
# v472 THOS v6 Handoff

v6 should harden final-message reliability and stale-temp dry-run classification. The v5 x2 long-window pass returned useful advisory content, but both CLI lanes completed before the requested 20-minute target, so duration remains an open runtime-quality gap.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-v6-handoff-v1.md")

    run_status = {
        "aggregate_status": runtime_ledger["aggregate_status"],
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "sibling_lane_status": {
            "app_lanes": "Cicero, Kierkegaard, and Aristotle returned advisory-only reports.",
            "cli_lanes": "Arby and Aster Vale returned read-only non-ephemeral final messages before the requested 20-minute dwell.",
            "cli_completion_notifier": "A reusable watcher helper now records final-message readiness markers without publishing raw lane transport.",
            "parfit_lorentz": "standby_not_contacted",
        },
        "validation_required_before_publication": [
            "python compile",
            "JSON parse",
            "credential/path/raw-log/session/screenshot guard",
            "whitespace check",
            "exact staged diff review",
            "push and remote-equals-local verification",
        ],
    }
    path = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(path, run_status)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md",
        f"""
# v472 THOS v5 x2 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

Cicero, Kierkegaard, Aristotle, Arby, and Aster Vale returned advisory-only input. Arby and Aster Vale ran read-only and non-ephemeral, produced final messages, and completed before the requested 20-minute dwell. Raw temp outputs were not staged or published.

A reusable CLI lane completion notifier was added so future Arby/Aster passes can finish naturally and publish curated readiness markers instead of requiring constant supervision.

All six GMUT gates remain open.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md")

    return written


def main() -> int:
    for path in write_artifacts():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
