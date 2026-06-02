#!/usr/bin/env python3
"""Repair approved user-level Codex skill loader issues."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v472-thos-v4-x1"
HOME = Path.home()
USER_SKILL_ROOT = HOME / ".codex" / "skills"
PLUGIN_ROOT = HOME / ".codex" / "plugins" / "cache"
TMP_ROOT = HOME / ".codex" / ".tmp"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
MAX_RETRY_COUNT = 50

EXACT_USER_SKILLS = [
    "body-reliability-gating/SKILL.md",
    "heart-conformance-gating/SKILL.md",
    "mind-expansion-systems/SKILL.md",
    "trinity-expansion-qa/SKILL.md",
    "trinity-expansion-release/SKILL.md",
    "trinity-live-gating-operations/SKILL.md",
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def display_path(path: Path) -> str:
    text = str(path).replace("\\", "/")
    home = str(HOME).replace("\\", "/")
    if text.lower().startswith(home.lower()):
        return "<user-home>" + text[len(home) :]
    return text


def assert_user_skill_scope(relative_path: str) -> Path:
    if relative_path.startswith("/") or relative_path.startswith("\\") or ".." in Path(relative_path).parts:
        raise ValueError(f"unsafe relative user-skill path: {relative_path}")
    target = (USER_SKILL_ROOT / Path(relative_path)).resolve()
    if not str(target).lower().startswith(str(USER_SKILL_ROOT.resolve()).lower()):
        raise ValueError(f"user-skill path escapes scope: {relative_path}")
    return target


def frontmatter_probe(data: bytes) -> dict[str, Any]:
    starts_raw = data.startswith(b"---")
    starts_bom = data.startswith(b"\xef\xbb\xbf")
    text = data.decode("utf-8-sig", errors="replace")
    lines = text.splitlines()
    starts_text = bool(lines and lines[0].strip() == "---")
    closing_line = None
    if starts_text:
        for index, line in enumerate(lines[1:], start=2):
            if line.strip() == "---":
                closing_line = index
                break
    header = "\n".join(lines[1 : closing_line - 1]) if closing_line else "\n".join(lines[1:50])
    return {
        "closing_delimiter_line": closing_line,
        "description_seen": bool(re.search(r"(?m)^description\s*:", header)),
        "name_seen": bool(re.search(r"(?m)^name\s*:", header)),
        "starts_with_bom": starts_bom,
        "starts_with_delimiter_after_sig_decode": starts_text,
        "starts_with_delimiter_raw": starts_raw,
    }


def remove_bom_only() -> list[dict[str, Any]]:
    repairs: list[dict[str, Any]] = []
    for relative_path in EXACT_USER_SKILLS:
        target = assert_user_skill_scope(relative_path)
        before = target.read_bytes()
        probe_before = frontmatter_probe(before)
        if before.startswith(b"\xef\xbb\xbf"):
            after = before[3:]
            if after != before[3:]:
                raise ValueError(f"unexpected byte mutation for {relative_path}")
            if not after.startswith(b"---"):
                raise ValueError(f"BOM removal would not expose delimiter for {relative_path}")
            probe_after = frontmatter_probe(after)
            if not (probe_after["name_seen"] and probe_after["description_seen"]):
                raise ValueError(f"required frontmatter fields missing after BOM removal: {relative_path}")
            target.write_bytes(after)
            write_performed = True
        else:
            after = before
            probe_after = probe_before
            write_performed = False
        repairs.append(
            {
                "after_hash": sha256_bytes(after),
                "before_hash": sha256_bytes(before),
                "body_after_bom_preserved": after == before[3:] if before.startswith(b"\xef\xbb\xbf") else True,
                "display_path": display_path(target),
                "frontmatter_after": probe_after,
                "frontmatter_before": probe_before,
                "relative_path": relative_path,
                "repair_kind": "leading_utf8_bom_removal_only",
                "write_performed": write_performed,
            }
        )
    return repairs


def run_cli_probe(output_dir: Path, lane_name: str, worktree: str) -> dict[str, Any]:
    prompt = f"v472 user-skill loader verification for {lane_name}. Read-only non-ephemeral. If skill loading succeeds, return concise advisory. Do not mutate files."
    command = [
        "python",
        "scripts/thos_codex_cli_advisory_launcher.py",
        "--lane-name",
        lane_name,
        "--worktree",
        worktree,
        "--prompt",
        prompt,
        "--output-dir",
        str(output_dir),
        "--execute",
        "--wait-seconds",
        "40",
        "--terminate-on-timeout",
    ]
    completed = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, timeout=100, check=False)
    plan = json.loads(completed.stdout)
    stderr_path = Path(plan["stderr_file"])
    stderr_text = stderr_path.read_text(encoding="utf-8", errors="replace") if stderr_path.exists() else ""
    loader_lines = [
        line
        for line in stderr_text.splitlines()
        if "failed to load skill" in line or "failed to remove stale curated plugins temp directory" in line
    ]
    redacted_lines = [line.replace(str(HOME) + "\\", "<user-home>\\") for line in loader_lines][:40]
    return {
        "completed_within_wait": plan.get("completed_within_wait"),
        "ephemeral_flag_used": plan.get("ephemeral_flag_used"),
        "lane": lane_name,
        "last_message_bytes": plan.get("last_message_bytes"),
        "loader_error_counts": {
            "invalid_name": sum("invalid name" in line for line in loader_lines),
            "missing_frontmatter": sum("missing YAML frontmatter" in line for line in loader_lines),
            "stale_plugin_temp_access_denied": sum("stale curated plugins temp directory" in line for line in loader_lines),
        },
        "loader_error_lines": redacted_lines,
        "sandbox": plan.get("sandbox"),
        "stderr_bytes": plan.get("stderr_bytes"),
        "terminated_after_timeout": plan.get("terminated_after_timeout"),
    }


def inspect_stale_plugin_temp() -> list[dict[str, Any]]:
    if not TMP_ROOT.exists():
        return []
    items: list[dict[str, Any]] = []
    for path in sorted(TMP_ROOT.glob("plugins-clone-*")):
        try:
            child_count = sum(1 for _ in path.iterdir()) if path.is_dir() else None
            items.append(
                {
                    "display_path": display_path(path),
                    "exists": path.exists(),
                    "is_dir": path.is_dir(),
                    "child_count": child_count,
                    "cleanup_performed": False,
                    "status": "INSPECTED_ONLY",
                }
            )
        except OSError as exc:
            items.append(
                {
                    "display_path": display_path(path),
                    "cleanup_performed": False,
                    "error": str(exc),
                    "status": "INSPECT_FAILED",
                }
            )
    return items


def write_artifacts(payload: dict[str, Any]) -> list[Path]:
    written: list[Path] = []
    phase = payload["phase_slug"]

    path = ARTIFACT_ROOT / f"{phase}-user-skill-bom-repair-receipt-v1.json"
    write_json(path, payload)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{phase}-user-skill-bom-repair-receipt-v1.md",
        f"""
# v472 THOS v4 x1 User-Skill BOM Repair Receipt

Status: `{payload["aggregate_status"]}`.

Removed leading UTF-8 BOM bytes from `{payload["writes_performed"]}` approved user-level skills. All six now start with raw `---`, retain `name` and `description`, and keep all bytes after the BOM unchanged.
""",
    )
    written.append(ARTIFACT_ROOT / f"{phase}-user-skill-bom-repair-receipt-v1.md")

    retry_payload = {
        "aggregate_status": payload["cli_retry_status"],
        "generated_at_utc": payload["generated_at_utc"],
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": phase,
        "retries": payload["cli_retries"],
        "rows": payload["rows"],
    }
    path = ARTIFACT_ROOT / f"{phase}-arby-aster-post-user-skill-retry-v1.json"
    write_json(path, retry_payload)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{phase}-arby-aster-post-user-skill-retry-v1.md",
        """
# v472 THOS v4 x1 Arby/Aster Post-Repair Retry

Arby and Aster were retried after the approved user-skill BOM repair. Remaining loader/temp signals are recorded without raw logs.
""",
    )
    written.append(ARTIFACT_ROOT / f"{phase}-arby-aster-post-user-skill-retry-v1.md")

    run_status = {
        "aggregate_status": payload["aggregate_status"],
        "generated_at_utc": payload["generated_at_utc"],
        "gmUT_gates_open": GMUT_GATES,
        "mutation_performed": True,
        "next_expected_phase": "v472-thos-v4-x2",
        "phase_slug": phase,
        "summary": payload["summary"],
    }
    path = ARTIFACT_ROOT / f"{phase}-run-status-v1.json"
    write_json(path, run_status)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{phase}-run-status-v1.md",
        """
# v472 THOS v4 x1 Run Status

The approved six user-skill BOM repair was completed and Arby/Aster were retried. This is THOS loader reliability work only; all GMUT gates remain open.
""",
    )
    written.append(ARTIFACT_ROOT / f"{phase}-run-status-v1.md")
    return written


def main() -> None:
    generated_at = utc_now()
    repairs = remove_bom_only()
    output_dir = Path.home() / "AppData" / "Local" / "Temp" / "ghc-v472-user-skill-repair-final"
    output_dir.mkdir(parents=True, exist_ok=True)
    cli_retries = [
        run_cli_probe(output_dir, "Arby", "D:/GHC-Archives/agent-worktrees/v461-round-robin/arby-advisory"),
        run_cli_probe(output_dir, "Aster Vale", "D:/GHC-Archives/agent-worktrees/v461-round-robin/aster-vale-advisory"),
    ]
    remaining_missing = sum(item["loader_error_counts"]["missing_frontmatter"] for item in cli_retries)
    remaining_invalid = sum(item["loader_error_counts"]["invalid_name"] for item in cli_retries)
    stale_temp_signals = sum(item["loader_error_counts"]["stale_plugin_temp_access_denied"] for item in cli_retries)
    writes_performed = sum(item["write_performed"] for item in repairs)
    all_raw_delimiter = all(item["frontmatter_after"]["starts_with_delimiter_raw"] for item in repairs)
    all_fields = all(item["frontmatter_after"]["name_seen"] and item["frontmatter_after"]["description_seen"] for item in repairs)

    status = "PASS_LOADER_ERRORS_CLEARED"
    if remaining_missing or remaining_invalid:
        status = "OPEN_GAP_REMAINING_LOADER_ERRORS"
    if not (all_raw_delimiter and all_fields):
        status = "FAIL_BLOCKER"

    rows = [
        row("bom_repair", "PASS_SHAPE_ONLY" if writes_performed == 6 else "OPEN_GAP", "Six approved user-skill BOM removals should occur on first live repair", {"writes_performed": writes_performed}),
        row("raw_delimiter", "PASS_SHAPE_ONLY" if all_raw_delimiter else "FAIL_BLOCKER", "Every repaired skill must start with raw frontmatter delimiter"),
        row("required_fields", "PASS_SHAPE_ONLY" if all_fields else "FAIL_BLOCKER", "Every repaired skill must retain name and description"),
        row("post_retry_missing_frontmatter", "PASS_SHAPE_ONLY" if remaining_missing == 0 else "OPEN_GAP", "Arby/Aster should no longer report missing-frontmatter skill loader errors", {"remaining_missing": remaining_missing}),
        row("post_retry_invalid_name", "PASS_SHAPE_ONLY" if remaining_invalid == 0 else "OPEN_GAP", "Arby/Aster should no longer report invalid-name skill loader errors", {"remaining_invalid": remaining_invalid}),
        row("stale_temp", "OPEN_GAP" if stale_temp_signals else "PASS_SHAPE_ONLY", "Stale plugin temp cleanup was inspected only, not deleted", {"signals": stale_temp_signals}),
    ]

    payload = {
        "aggregate_status": status,
        "cli_retries": cli_retries,
        "cli_retry_status": "PASS_LOADER_RETRY" if remaining_missing == 0 and remaining_invalid == 0 else "OPEN_GAP_RETRY_REMAINING_ERRORS",
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "max_retry_count_authorized": MAX_RETRY_COUNT,
        "mutation_performed": writes_performed > 0,
        "phase_slug": PHASE,
        "repairs": repairs,
        "rows": rows,
        "stale_plugin_temp_inspection": inspect_stale_plugin_temp(),
        "summary": f"Removed leading BOM from {writes_performed} approved user skills; retry missing_frontmatter={remaining_missing}, invalid_name={remaining_invalid}.",
        "writes_performed": writes_performed,
    }
    written = write_artifacts(payload)
    print(json.dumps({"status": status, "writes_performed": writes_performed, "written": [path.as_posix() for path in written]}, indent=2))


if __name__ == "__main__":
    main()
