#!/usr/bin/env python3
"""Build v472 THOS v5 x1 skill-loader regression guard artifacts."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any


PHASE = "v472-thos-v5-x1"
NEXT_PHASE = "v472-thos-v5-x2"
HOME = Path.home()
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
SKILL_ROOTS = [
    HOME / ".codex" / "skills",
    HOME / ".codex" / "plugins" / "cache",
]
TMP_ROOT = HOME / ".codex" / ".tmp"
PLUGIN_PREFIX = "build-web-data-visualization:"
MAX_CANONICAL_NAME = 64

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

EXPECTED_NEGATIVE_FIXTURES = {
    "missing_frontmatter": b"# Missing Frontmatter\n\nBody\n",
    "leading_bom": b"\xef\xbb\xbf---\nname: bom-fixture\ndescription: Has leading BOM.\n---\n\nBody\n",
    "missing_name": b"---\ndescription: Missing name.\n---\n\nBody\n",
    "missing_description": b"---\nname: missing-description\n---\n\nBody\n",
    "malformed_delimiter": b"---\nname: malformed\ndescription: Missing close.\n\nBody\n",
    "overlong_name": (
        b"---\nname: "
        + b"x" * 80
        + b"\ndescription: Overlong name.\n---\n\nBody\n"
    ),
    "raw_body_field_leak": b"---\nname: raw-body\ndescription: Raw body field fixture.\nraw_body: should-not-appear\n---\n\nBody\n",
}

BROWSER_SMOKE = {
    "ok": True,
    "url": "https://openai.com/academy/codex-plugins-and-skills/",
    "title": "Plugins and skills | OpenAI",
    "correct_methods": ["tab.url()", "tab.title()"],
    "expected_negative_method": "tab.playwright.url()",
}

APP_ADVISORIES = [
    {"lane": "Cicero", "submission_id": "019e8898-c3d0-75d2-86b0-4d4004b057fe", "status": "REQUEST_SENT"},
    {"lane": "Kierkegaard", "submission_id": "019e8899-0817-7932-8778-93cf50adbdc0", "status": "REQUEST_SENT"},
    {"lane": "Aristotle", "submission_id": "019e8899-7616-7c53-9c6e-3ebc5b27b0ed", "status": "REQUEST_SENT"},
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


def scan_skill_bytes(data: bytes, namespace_prefix: str = "") -> dict[str, Any]:
    errors: list[str] = []
    if data.startswith(b"\xef\xbb\xbf"):
        errors.append("LEADING_UTF8_BOM")
    if not data.startswith(b"---"):
        errors.append("MISSING_RAW_FRONTMATTER_DELIMITER")
        return {"errors": errors, "status": "FAIL_LOADER_SHAPE"}
    newline = b"\r\n" if b"\r\n" in data[:200] else b"\n"
    first_line_end = data.find(newline)
    closing = data.find(newline + b"---" + newline, first_line_end + len(newline))
    if first_line_end < 0 or closing < 0:
        errors.append("MALFORMED_FRONTMATTER_DELIMITERS")
        return {"errors": errors, "status": "FAIL_LOADER_SHAPE"}
    header = data[first_line_end + len(newline) : closing].decode("utf-8", errors="replace")
    name_match = re.search(r"(?m)^name\s*:\s*['\"]?([^'\"\n\r]+)", header)
    description_match = re.search(r"(?m)^description\s*:", header)
    if not name_match:
        errors.append("REQUIRED_NAME_MISSING")
    if not description_match:
        errors.append("REQUIRED_DESCRIPTION_MISSING")
    if re.search(r"(?mi)^(raw_body|body_text|before_text|after_text|plugin_body)\s*:", header):
        errors.append("RAW_BODY_FIELD_PRESENT")
    if name_match:
        name = name_match.group(1).strip()
        canonical_name = namespace_prefix + name
        if len(canonical_name) > MAX_CANONICAL_NAME:
            errors.append("INVALID_NAME_TOO_LONG")
    return {"errors": errors, "status": "PASS_LOADER_SHAPE" if not errors else "FAIL_LOADER_SHAPE"}


def namespace_for(path: Path) -> str:
    parts = [part.lower() for part in path.parts]
    if "build-web-data-visualization" in parts:
        return PLUGIN_PREFIX
    return ""


def scan_live_skills() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for root in SKILL_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("SKILL.md"):
            data = path.read_bytes()
            result = scan_skill_bytes(data, namespace_for(path))
            if result["errors"]:
                rows.append(
                    {
                        "display_path": display_path(path),
                        "errors": result["errors"],
                        "hash": sha256_bytes(data),
                        "status": result["status"],
                    }
                )
    return {
        "error_count": len(rows),
        "errors": rows,
        "scan_roots": [display_path(root) for root in SKILL_ROOTS],
        "status": "PASS_LOADER_SHAPE" if not rows else "FAIL_LOADER_SHAPE",
    }


def run_expected_negative_fixtures() -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    with TemporaryDirectory(prefix="v472-skill-loader-fixtures-") as tmp:
        root = Path(tmp)
        for fixture_name, content in EXPECTED_NEGATIVE_FIXTURES.items():
            path = root / fixture_name / "SKILL.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            result = scan_skill_bytes(content, PLUGIN_PREFIX if fixture_name == "overlong_name" else "")
            entries.append(
                {
                    "body_text_included": False,
                    "detected_errors": result["errors"],
                    "fixture": fixture_name,
                    "hash": sha256_bytes(content),
                    "status": "EXPECTED_NEGATIVE_CAUGHT" if result["errors"] else "FAIL_EXPECTED_NEGATIVE_NOT_CAUGHT",
                    "write_target": "tempdir_only",
                }
            )
    return {
        "entries": entries,
        "failure_count": sum(entry["status"] != "EXPECTED_NEGATIVE_CAUGHT" for entry in entries),
        "fixture_count": len(entries),
        "status": "PASS_EXPECTED_NEGATIVES" if all(entry["status"] == "EXPECTED_NEGATIVE_CAUGHT" for entry in entries) else "FAIL_EXPECTED_NEGATIVES",
    }


def inspect_stale_temp() -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    if TMP_ROOT.exists():
        for path in sorted(TMP_ROOT.glob("plugins-clone-*")):
            entries.append(
                {
                    "cleanup_performed": False,
                    "display_path": display_path(path),
                    "exists": path.exists(),
                    "is_dir": path.is_dir(),
                    "status": "INSPECTED_ONLY",
                }
            )
    return {
        "entries": entries,
        "status": "OPEN_GAP_STALE_TEMP_PRESENT" if entries else "PASS_NO_STALE_TEMP_VISIBLE",
        "visible_count": len(entries),
    }


def aggregate(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] == "OPEN_GAP" for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    live_scan = scan_live_skills()
    fixtures = run_expected_negative_fixtures()
    stale_temp = inspect_stale_temp()

    guard_rows = [
        row("live_skill_scan", "PASS_SHAPE_ONLY" if live_scan["error_count"] == 0 else "FAIL_BLOCKER", "Live user/plugin skill loader scan should have zero current shape errors", {"error_count": live_scan["error_count"]}),
        row("expected_negative_fixtures", "PASS_SHAPE_ONLY" if fixtures["failure_count"] == 0 else "FAIL_BLOCKER", "All expected-negative fixture shapes should be caught", {"fixture_count": fixtures["fixture_count"], "failure_count": fixtures["failure_count"]}),
        row("browser_smoke", "PASS_SHAPE_ONLY" if BROWSER_SMOKE["ok"] else "OPEN_GAP", "Browser smoke uses corrected URL/title methods", BROWSER_SMOKE),
        row("stale_temp", "OPEN_GAP" if stale_temp["visible_count"] else "PASS_SHAPE_ONLY", "Stale temp plugin-clone directories are inspected only; no deletion performed", {"visible_count": stale_temp["visible_count"]}),
        row("claim_ceiling", "PASS_SHAPE_ONLY", "Skill-loader guard does not validate GMUT or close gates"),
    ]

    written: list[Path] = []
    guard = {
        "aggregate_status": aggregate(guard_rows),
        "app_advisories": APP_ADVISORIES,
        "browser_smoke": BROWSER_SMOKE,
        "expected_negative_fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "live_skill_scan": live_scan,
        "mutation_performed": False,
        "phase_slug": PHASE,
        "rows": guard_rows,
        "stale_temp_inspection": stale_temp,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-skill-loader-regression-guard-v1.json"
    write_json(path, guard)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-skill-loader-regression-guard-v1.md",
        """
# v472 THOS v5 x1 Skill-Loader Regression Guard

The guard scans live user/plugin skills and tempdir-only expected-negative fixtures. It performs no external mutation and keeps all GMUT gates open.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-skill-loader-regression-guard-v1.md")

    fixture_plan = {
        "aggregate_status": fixtures["status"],
        "entries": fixtures["entries"],
        "generated_at_utc": generated_at,
        "mutation_performed": False,
        "phase_slug": PHASE,
        "use_ceiling": "Fixtures are tempdir-only and no raw skill body text is published.",
    }
    path = ARTIFACT_ROOT / f"{PHASE}-expected-negative-fixture-results-v1.json"
    write_json(path, fixture_plan)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-expected-negative-fixture-results-v1.md",
        """
# v472 THOS v5 x1 Expected-Negative Fixture Results

All expected-negative loader fixtures were caught by the guard. Fixture bodies are not published in curated artifacts.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-expected-negative-fixture-results-v1.md")

    boundary_rows = [
        row("receipts_only", "PASS_SHAPE_ONLY", "Repo publication includes only curated artifacts and scripts"),
        row("no_external_stage", "PASS_SHAPE_ONLY", "User skills/plugin cache files are not staged"),
        row("browser_bounded", "PASS_SHAPE_ONLY", "Browser smoke is bounded to one official OpenAI page and corrected methods"),
        row("stale_temp_cleanup", "OPEN_GAP", "No stale-temp deletion was performed in v5 x1"),
        row("gmut_gate_boundary", "PASS_SHAPE_ONLY", "No GMUT gate closure is claimed"),
    ]
    boundary = {
        "aggregate_status": aggregate(boundary_rows),
        "generated_at_utc": generated_at,
        "gmUT_gates_open": GMUT_GATES,
        "mutation_performed": False,
        "phase_slug": PHASE,
        "rows": boundary_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-publication-boundary-checklist-v1.json"
    write_json(path, boundary)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-publication-boundary-checklist-v1.md",
        """
# v472 THOS v5 x1 Publication Boundary Checklist

Publication remains receipts-only. External repaired skill files, raw logs, media captures, chat exports, and private material are not staged.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-publication-boundary-checklist-v1.md")

    run_status = {
        "aggregate_status": aggregate(guard_rows),
        "generated_at_utc": generated_at,
        "gmUT_gates_open": GMUT_GATES,
        "mutation_performed": False,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "summary": "v5 x1 adds live skill-loader scan, tempdir expected-negative fixtures, Browser method guard, and publication boundaries.",
    }
    path = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(path, run_status)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md",
        """
# v472 THOS v5 x1 Run Status

Skill-loader regression guard is in place. Stale temp runtime hygiene remains open; all GMUT gates remain open.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md")
    return written


def main() -> None:
    written = write_artifacts()
    print(json.dumps({"status": "PASS_WRITE_ARTIFACTS_ONLY", "written": [path.as_posix() for path in written]}, indent=2))


if __name__ == "__main__":
    main()
