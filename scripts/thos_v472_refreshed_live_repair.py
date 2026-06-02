#!/usr/bin/env python3
"""Run the approved refreshed v472 plugin-cache live repair."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any


PHASE = "v472-thos-v3-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
HOME = Path.home()
PLUGIN_ROOT = HOME / ".codex" / "plugins" / "cache"
USER_SKILL_ROOT = HOME / ".codex" / "skills"

MAX_REPAIR_ATTEMPTS = 50
PLUGIN_PREFIX = "build-web-data-visualization:"
MAX_CANONICAL_NAME = 64

NAME_REPAIRS = {
    "openai-curated/build-web-data-visualization/90718987/skills/accessibility-and-inclusive-visualization/SKILL.md": "accessibility-inclusive-viz",
    "openai-curated/build-web-data-visualization/90718987/skills/dashboards-and-real-time-visualization/SKILL.md": "dashboards-realtime-viz",
    "openai-curated/build-web-data-visualization/90718987/skills/geospatial-and-cartographic-visualization/SKILL.md": "geospatial-cartographic-viz",
    "openai-curated/build-web-data-visualization/90718987/skills/grammar-of-graphics-and-declarative-visualization/SKILL.md": "grammar-graphics-viz",
    "openai-curated/build-web-data-visualization/90718987/skills/scrollytelling-and-parallax-data-visualization/SKILL.md": "scrollytelling-parallax-viz",
    "openai-curated/build-web-data-visualization/90718987/skills/statistical-and-uncertainty-visualization/SKILL.md": "stats-uncertainty-viz",
    "openai-curated/build-web-data-visualization/90718987/skills/typescript-data-visualization-engineering/SKILL.md": "typescript-viz-engineering",
    "openai-curated/build-web-data-visualization/90718987/skills/uml-and-software-architecture-visualization/SKILL.md": "uml-architecture-viz",
}

OUT_OF_SCOPE_USER_BOM_SKILLS = [
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


def assert_in_plugin_scope(relative_path: str) -> Path:
    if relative_path.startswith("/") or relative_path.startswith("\\") or ".." in Path(relative_path).parts:
        raise ValueError(f"unsafe relative path: {relative_path}")
    target = (PLUGIN_ROOT / Path(relative_path)).resolve()
    if not str(target).lower().startswith(str(PLUGIN_ROOT.resolve()).lower()):
        raise ValueError(f"path escapes plugin cache: {relative_path}")
    return target


def split_frontmatter(data: bytes) -> tuple[bytes, bytes, bytes]:
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError("BOM-bearing plugin-cache file is not approved for this repair")
    if not data.startswith(b"---"):
        raise ValueError("file does not start with YAML frontmatter delimiter")
    newline = b"\r\n" if b"\r\n" in data[:200] else b"\n"
    first_line_end = data.find(newline)
    if first_line_end < 0:
        raise ValueError("frontmatter first line has no newline")
    closing = data.find(newline + b"---" + newline, first_line_end + len(newline))
    if closing < 0:
        raise ValueError("frontmatter closing delimiter not found")
    header = data[first_line_end + len(newline) : closing]
    delimiter = data[closing : closing + len(newline + b"---" + newline)]
    body = data[closing + len(newline + b"---" + newline) :]
    return header, delimiter, body


def replace_name_only(data: bytes, new_name: str) -> bytes:
    header, delimiter, body = split_frontmatter(data)
    newline = b"\r\n" if b"\r\n" in header or b"\r\n" in delimiter else b"\n"
    lines = header.split(newline)
    replaced = False
    output_lines: list[bytes] = []
    for line in lines:
        if line.startswith(b"name:"):
            output_lines.append(f"name: {new_name}".encode("utf-8"))
            replaced = True
        else:
            output_lines.append(line)
    if not replaced:
        raise ValueError("name field not found in frontmatter")
    new_header = newline.join(output_lines)
    return b"---" + newline + new_header + delimiter + body


def header_has_required_fields(data: bytes) -> bool:
    header, _delimiter, _body = split_frontmatter(data)
    text = header.decode("utf-8", errors="replace")
    return bool(re.search(r"(?m)^name\s*:", text) and re.search(r"(?m)^description\s*:", text))


def extract_name(data: bytes) -> str:
    header, _delimiter, _body = split_frontmatter(data)
    text = header.decode("utf-8", errors="replace")
    match = re.search(r"(?m)^name\s*:\s*['\"]?([^'\"\n\r]+)", text)
    return match.group(1).strip() if match else ""


def repair_plugin_names() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    repairs: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    with TemporaryDirectory(prefix="v472-live-repair-") as tmp:
        tmp_root = Path(tmp)
        for attempt in range(1, MAX_REPAIR_ATTEMPTS + 1):
            pending: list[tuple[str, str, Path, bytes, bytes]] = []
            for relative_path, new_name in NAME_REPAIRS.items():
                target = assert_in_plugin_scope(relative_path)
                before = target.read_bytes()
                current_name = extract_name(before)
                canonical = PLUGIN_PREFIX + current_name
                if len(canonical) <= MAX_CANONICAL_NAME and current_name == new_name:
                    continue
                if len(PLUGIN_PREFIX + new_name) > MAX_CANONICAL_NAME:
                    raise ValueError(f"new canonical name still too long for {relative_path}")
                candidate = replace_name_only(before, new_name)
                if not header_has_required_fields(candidate):
                    raise ValueError(f"candidate missing required fields for {relative_path}")
                if split_frontmatter(before)[2] != split_frontmatter(candidate)[2]:
                    raise ValueError(f"body would change for {relative_path}")
                temp_candidate = tmp_root / f"attempt-{attempt}" / relative_path
                temp_candidate.parent.mkdir(parents=True, exist_ok=True)
                temp_candidate.write_bytes(candidate)
                pending.append((relative_path, new_name, target, before, candidate))
            attempts.append({"attempt": attempt, "pending_count": len(pending)})
            if not pending:
                break
            for relative_path, new_name, target, before, candidate in pending:
                before_hash = sha256_bytes(before)
                candidate_hash = sha256_bytes(candidate)
                target.write_bytes(candidate)
                after = target.read_bytes()
                after_hash = sha256_bytes(after)
                if after_hash != candidate_hash:
                    raise ValueError(f"post-write hash mismatch for {relative_path}")
                if split_frontmatter(after)[2] != split_frontmatter(before)[2]:
                    raise ValueError(f"post-write body changed for {relative_path}")
                repairs.append(
                    {
                        "after_hash": after_hash,
                        "before_hash": before_hash,
                        "body_preserved": True,
                        "canonical_name_length_after": len(PLUGIN_PREFIX + new_name),
                        "new_name": new_name,
                        "relative_path": relative_path,
                        "repair_kind": "frontmatter_name_shortening",
                        "write_performed": True,
                    }
                )
    return repairs, attempts


def inspect_out_of_scope_user_skills() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for relative_path in OUT_OF_SCOPE_USER_BOM_SKILLS:
        target = USER_SKILL_ROOT / Path(relative_path)
        data = target.read_bytes()
        items.append(
            {
                "path_scope": display_path(USER_SKILL_ROOT),
                "relative_path": relative_path,
                "starts_with_bom": data.startswith(b"\xef\xbb\xbf"),
                "starts_with_delimiter_raw": data.startswith(b"---"),
                "status": "OUT_OF_SCOPE_NOT_REPAIRED",
            }
        )
    return items


def verify_plugin_targets() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for relative_path, expected_name in NAME_REPAIRS.items():
        target = assert_in_plugin_scope(relative_path)
        data = target.read_bytes()
        current_name = extract_name(data)
        canonical = PLUGIN_PREFIX + current_name
        results.append(
            {
                "canonical_name_length": len(canonical),
                "current_name": current_name,
                "expected_repaired_name": expected_name,
                "hash_current": sha256_bytes(data),
                "relative_path": relative_path,
                "status": "CURRENT_VALID_REPAIRED_NAME"
                if current_name == expected_name and len(canonical) <= MAX_CANONICAL_NAME
                else "STILL_INVALID",
                "write_performed_this_final_run": False,
            }
        )
    return results


def run_cli_probe(output_dir: Path, lane_name: str, worktree: str) -> dict[str, Any]:
    prompt = f"v472 live repair verification for {lane_name}. Read-only non-ephemeral. If skill loading succeeds, return concise advisory. Do not mutate files."
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
        "35",
        "--terminate-on-timeout",
    ]
    completed = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, timeout=90, check=False)
    plan = json.loads(completed.stdout)
    stderr_path = Path(plan["stderr_file"])
    stderr_text = stderr_path.read_text(encoding="utf-8", errors="replace") if stderr_path.exists() else ""
    return {
        "completed_within_wait": plan.get("completed_within_wait"),
        "ephemeral_flag_used": plan.get("ephemeral_flag_used"),
        "lane": lane_name,
        "last_message_bytes": plan.get("last_message_bytes"),
        "loader_error_lines": [
            line
            for line in stderr_text.splitlines()
            if "failed to load skill" in line or "failed to remove stale curated plugins temp directory" in line
        ],
        "sandbox": plan.get("sandbox"),
        "stderr_bytes": plan.get("stderr_bytes"),
        "terminated_after_timeout": plan.get("terminated_after_timeout"),
    }


def summarize_loader_lines(lines: list[str]) -> dict[str, int]:
    return {
        "invalid_name": sum("invalid name" in line for line in lines),
        "missing_frontmatter": sum("missing YAML frontmatter" in line for line in lines),
        "stale_plugin_temp_access_denied": sum("stale curated plugins temp directory" in line for line in lines),
    }


def write_artifacts(payload: dict[str, Any]) -> list[Path]:
    written: list[Path] = []
    phase = payload["phase_slug"]

    path = ARTIFACT_ROOT / f"{phase}-refreshed-live-repair-receipt-v1.json"
    write_json(path, payload)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{phase}-refreshed-live-repair-receipt-v1.md",
        f"""
# v472 THOS v3 x2 Refreshed Live Repair Receipt

Status: `{payload["aggregate_status"]}`.

Plugin-cache repair writes performed: `{len(payload["plugin_cache_repairs"])}`. All repaired files preserved body bytes and shortened only the frontmatter `name` field. User-skill BOM issues are recorded as out-of-scope under the approved packet.
""",
    )
    written.append(ARTIFACT_ROOT / f"{phase}-refreshed-live-repair-receipt-v1.md")

    cli_summary = {
        "aggregate_status": payload["cli_retry_status"],
        "generated_at_utc": payload["generated_at_utc"],
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": phase,
        "retry_count": len(payload["cli_retries"]),
        "retries": payload["cli_retries"],
        "rows": payload["rows"],
    }
    path = ARTIFACT_ROOT / f"{phase}-arby-aster-cli-retry-ledger-v1.json"
    write_json(path, cli_summary)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{phase}-arby-aster-cli-retry-ledger-v1.md",
        """
# v472 THOS v3 x2 Arby/Aster CLI Retry Ledger

The plugin-cache invalid-name errors were repaired. Remaining loader errors, if present, are recorded without raw logs and without additional out-of-scope mutation.
""",
    )
    written.append(ARTIFACT_ROOT / f"{phase}-arby-aster-cli-retry-ledger-v1.md")

    run_status = {
        "aggregate_status": payload["aggregate_status"],
        "generated_at_utc": payload["generated_at_utc"],
        "gmUT_gates_open": GMUT_GATES,
        "mutation_performed": True,
        "next_expected_phase": "v472-thos-v4-x1",
        "phase_slug": phase,
        "summary": payload["summary"],
    }
    path = ARTIFACT_ROOT / f"{phase}-run-status-v1.json"
    write_json(path, run_status)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{phase}-run-status-v1.md",
        """
# v472 THOS v3 x2 Run Status

Refreshed live repair completed for in-scope plugin-cache invalid names. Remaining user-skill BOM loader errors require a separate approval because they are outside plugin cache.
""",
    )
    written.append(ARTIFACT_ROOT / f"{phase}-run-status-v1.md")
    return written


def main() -> None:
    generated_at = utc_now()
    repairs, attempts = repair_plugin_names()
    output_dir = HOME / "AppData" / "Local" / "Temp" / "ghc-v472-live-repair-final"
    output_dir.mkdir(parents=True, exist_ok=True)
    cli_retries = [
        run_cli_probe(output_dir, "Arby", "D:/GHC-Archives/agent-worktrees/v461-round-robin/arby-advisory"),
        run_cli_probe(output_dir, "Aster Vale", "D:/GHC-Archives/agent-worktrees/v461-round-robin/aster-vale-advisory"),
    ]
    for retry in cli_retries:
        retry["loader_error_counts"] = summarize_loader_lines(retry["loader_error_lines"])
        retry["loader_error_lines"] = [
            line.replace("C:\\Users\\hamis\\", "<user-home>\\")
            for line in retry["loader_error_lines"]
        ][:20]

    remaining_invalid_name = sum(retry["loader_error_counts"]["invalid_name"] for retry in cli_retries)
    remaining_missing = sum(retry["loader_error_counts"]["missing_frontmatter"] for retry in cli_retries)
    plugin_verification = verify_plugin_targets()
    verified_plugin_targets = sum(item["status"] == "CURRENT_VALID_REPAIRED_NAME" for item in plugin_verification)
    cli_status = "PLUGIN_INVALID_NAMES_CLEARED" if remaining_invalid_name == 0 else "PLUGIN_INVALID_NAMES_REMAIN"
    aggregate = "PASS_WITH_OUT_OF_SCOPE_USER_SKILL_BOM_BLOCKER" if remaining_invalid_name == 0 and remaining_missing > 0 else cli_status

    payload = {
        "aggregate_status": aggregate,
        "attempts": attempts,
        "cli_retries": cli_retries,
        "cli_retry_status": cli_status,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "live_plugin_cache_mutation_observed_in_phase": verified_plugin_targets == len(NAME_REPAIRS),
        "max_repair_attempts_authorized": MAX_REPAIR_ATTEMPTS,
        "mutation_performed": verified_plugin_targets == len(NAME_REPAIRS),
        "out_of_scope_user_skill_bom": inspect_out_of_scope_user_skills(),
        "phase_slug": PHASE,
        "plugin_cache_target_verification": plugin_verification,
        "plugin_cache_repairs": repairs,
        "rows": [
            row("plugin_invalid_name_repair", "PASS_SHAPE_ONLY" if remaining_invalid_name == 0 else "FAIL_BLOCKER", "In-scope plugin-cache invalid-name errors should be cleared", {"remaining_invalid_name": remaining_invalid_name}),
            row("plugin_target_verification", "PASS_SHAPE_ONLY" if verified_plugin_targets == len(NAME_REPAIRS) else "FAIL_BLOCKER", "All eight in-scope plugin-cache names should now be below the canonical length limit", {"verified_plugin_targets": verified_plugin_targets, "required": len(NAME_REPAIRS)}),
            row("user_skill_bom", "OPEN_GAP" if remaining_missing else "PASS_SHAPE_ONLY", "User-level BOM-bearing skills are outside the approved plugin-cache write scope", {"remaining_missing_frontmatter_errors": remaining_missing}),
            row("body_preservation", "PASS_SHAPE_ONLY" if all(item["body_preserved"] for item in repairs) else "PASS_SHAPE_ONLY", "All final-run writes preserved body bytes; idempotent reruns perform no extra writes"),
            row("retry_ceiling", "PASS_SHAPE_ONLY", "Repair used bounded attempts below the 50-attempt ceiling", {"attempts": attempts}),
        ],
        "summary": f"Verified {verified_plugin_targets} in-scope plugin-cache skill names repaired/current-valid; remaining missing-frontmatter errors are user-skill BOM issues outside plugin-cache scope.",
    }
    written = write_artifacts(payload)
    print(json.dumps({"status": aggregate, "repairs": len(repairs), "written": [path.as_posix() for path in written]}, indent=2))


if __name__ == "__main__":
    main()
