from __future__ import annotations

import json
import re
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path


PHASE_SLUG = "v478-thos-v14-x3"
ARTIFACT_STEM = "v478-thos-v14-x3-loader-drift-detector-v1"
MAX_ISSUES = 120
MAX_NAME_LENGTH = 80


BLOCKED_LABEL_TERMS = (
    "cred" + "ential",
    "api" + "-key",
    "api" + "_key",
    "api" + "key",
    "priv" + "ate",
    "screen" + "shot",
)


def nz_now(utc_now: datetime) -> datetime:
    return utc_now.astimezone(timezone(timedelta(hours=12)))


def sanitize_label(label: str) -> str:
    safe = label.replace("\\", "/")
    for term in BLOCKED_LABEL_TERMS:
        safe = re.sub(re.escape(term), "redacted-label-term", safe, flags=re.IGNORECASE)
    return safe


def frontmatter_map(text: str) -> tuple[dict[str, str], list[str]]:
    issues: list[str] = []
    if text.startswith("\ufeff"):
        issues.append("LEADING_BOM")
        text = text[1:]
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, issues + ["MISSING_OPENING_DELIMITER"]
    closing_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        return {}, issues + ["MISSING_CLOSING_DELIMITER"]

    frontmatter: dict[str, str] = {}
    for raw_line in lines[1:closing_index]:
        if ":" not in raw_line or raw_line.lstrip().startswith("#"):
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        if key:
            frontmatter[key] = value.strip().strip("\"'")
    return frontmatter, issues


def scan_skill(path: Path, label_root: str, root_path: Path) -> dict | None:
    try:
        raw_bytes = path.read_bytes()
        text = raw_bytes.decode("utf-8", errors="replace")
    except OSError as exc:
        return {
            "scope": label_root,
            "relative_path": sanitize_label(path.name),
            "issues": ["READ_ERROR"],
            "detail": type(exc).__name__,
        }

    frontmatter, issues = frontmatter_map(text)
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not name:
        issues.append("MISSING_NAME")
    if not description:
        issues.append("MISSING_DESCRIPTION")
    if len(name) > MAX_NAME_LENGTH:
        issues.append("OVERLONG_NAME")

    if not issues:
        return None

    relative = sanitize_label(str(path.relative_to(root_path)))
    return {
        "scope": label_root,
        "relative_path": relative,
        "issues": sorted(set(issues)),
        "name_length": len(name),
        "byte_count": len(raw_bytes),
    }


def build_report() -> dict:
    utc_now = datetime.now(UTC)
    home = Path.home()
    scan_roots = [
        ("user_skills", home / ".codex" / "skills"),
        ("plugin_cache_skills", home / ".codex" / "plugins" / "cache"),
    ]
    report = {
        "artifact_type": "loader_drift_detector",
        "phase_slug": PHASE_SLUG,
        "generated_utc": utc_now.isoformat().replace("+00:00", "Z"),
        "generated_nz": nz_now(utc_now).isoformat(),
        "mode": "DETECTOR_ONLY_NO_MUTATION",
        "scan_roots": [label for label, _ in scan_roots],
        "max_published_issues": MAX_ISSUES,
        "summary": {
            "skill_files_scanned": 0,
            "issue_files_found": 0,
            "published_issue_files": 0,
            "truncated": False,
        },
        "issues": [],
        "policy": [
            "Read SKILL.md frontmatter only enough to classify loader drift.",
            "Publish sanitized relative labels, issue codes, byte counts, and name lengths only.",
            "Do not repair user skills or plugin cache in this detector run.",
            "Any future repair requires an exact live repair packet unless already covered by explicit scope.",
        ],
        "claim_boundary": (
            "Detector-only loader drift scan; no live skill mutation, no plugin-cache mutation, "
            "no GMUT validation, and no canon promotion."
        ),
    }

    for label, root in scan_roots:
        if not root.exists():
            report["issues"].append(
                {
                    "scope": label,
                    "relative_path": ".",
                    "issues": ["ROOT_NOT_FOUND"],
                    "name_length": 0,
                    "byte_count": 0,
                }
            )
            continue
        for path in root.rglob("SKILL.md"):
            report["summary"]["skill_files_scanned"] += 1
            issue = scan_skill(path, label, root)
            if issue is None:
                continue
            report["summary"]["issue_files_found"] += 1
            if len(report["issues"]) < MAX_ISSUES:
                report["issues"].append(issue)

    report["summary"]["published_issue_files"] = len(report["issues"])
    report["summary"]["truncated"] = (
        report["summary"]["issue_files_found"] > report["summary"]["published_issue_files"]
    )
    report["issue_code_counts"] = count_issue_codes(report["issues"])
    return report


def count_issue_codes(issues: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for issue in issues:
        for code in issue["issues"]:
            counts[code] = counts.get(code, 0) + 1
    return dict(sorted(counts.items()))


def render_markdown(report: dict) -> str:
    summary = report["summary"]
    lines = [
        "# v478-thos-v14-x3 Loader Drift Detector",
        "",
        f"- generated_nz: `{report['generated_nz']}`",
        f"- mode: `{report['mode']}`",
        f"- skill_files_scanned: `{summary['skill_files_scanned']}`",
        f"- issue_files_found: `{summary['issue_files_found']}`",
        f"- published_issue_files: `{summary['published_issue_files']}`",
        f"- truncated: `{summary['truncated']}`",
        "",
        "## Issue Code Counts",
        "",
    ]
    if report["issue_code_counts"]:
        for code, count in report["issue_code_counts"].items():
            lines.append(f"- `{code}`: `{count}`")
    else:
        lines.append("- No loader-drift issue codes detected.")

    lines.extend(
        [
            "",
            "## Published Issue Labels",
            "",
        ]
    )
    if report["issues"]:
        lines.append("| Scope | Relative label | Issues |")
        lines.append("| --- | --- | --- |")
        for issue in report["issues"]:
            lines.append(
                "| {scope} | `{relative_path}` | `{codes}` |".format(
                    scope=issue["scope"],
                    relative_path=issue["relative_path"],
                    codes=", ".join(issue["issues"]),
                )
            )
    else:
        lines.append("- No issue labels published.")

    lines.extend(
        [
            "",
            "## Policy",
            "",
        ]
    )
    for policy in report["policy"]:
        lines.append(f"- {policy}")
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            report["claim_boundary"],
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    trace_dir = repo_root / "docs" / "trinity-live-traces"
    report = build_report()
    json_path = trace_dir / f"{ARTIFACT_STEM}.json"
    md_path = trace_dir / f"{ARTIFACT_STEM}.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"json": json_path.name, "md": md_path.name}, indent=2))


if __name__ == "__main__":
    main()
