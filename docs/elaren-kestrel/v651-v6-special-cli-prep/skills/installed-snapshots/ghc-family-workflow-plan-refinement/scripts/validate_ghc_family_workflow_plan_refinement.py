#!/usr/bin/env python3
"""Validate the workflow-plan skill and one D-drive preparation packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import py_compile
import re
import sys
from pathlib import Path
from typing import Any


UUID_RE = re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b")
PRIVATE_URI_RE = re.compile(r"(?i)\b(?:thread|task|session|codex)://\S+")
ABSOLUTE_PATH_RE = re.compile(r"(?i)(?:^|[\s\"'])(?:[a-z]:[\\/]|\\\\)[^\s\"']+")
CREDENTIAL_RE = re.compile(
    r"(?i)(?:api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|private[_-]?key)\s*[:=]\s*\S+"
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--packet-dir", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []
    issues: list[str] = []

    def check(name: str, passed: bool, observed: Any, expected: str) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed, "expected": expected})
        if not passed:
            issues.append(name)

    required_skill = {
        "SKILL.md",
        "agents/openai.yaml",
        "references/workflow-plan-schema.md",
        "scripts/ghc_family_workflow_plan_refinement.py",
        "scripts/validate_ghc_family_workflow_plan_refinement.py",
    }
    actual_skill = {
        path.relative_to(args.skill_dir).as_posix()
        for path in args.skill_dir.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    check("required_skill_files", required_skill <= actual_skill, sorted(actual_skill), "all required skill files")
    skill_text = (args.skill_dir / "SKILL.md").read_text(encoding="utf-8")
    yaml_text = (args.skill_dir / "agents/openai.yaml").read_text(encoding="utf-8")
    check("skill_frontmatter", skill_text.startswith("---\nname: ghc-family-workflow-plan-refinement\n"), True, "valid named frontmatter")
    check(
        "skill_default_prompt",
        "$ghc-family-workflow-plan-refinement" in yaml_text,
        "$ghc-family-workflow-plan-refinement" in yaml_text,
        "default prompt names the skill",
    )
    compile_issues: list[str] = []
    for script in sorted((args.skill_dir / "scripts").glob("*.py")):
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError:
            compile_issues.append(script.name)
    check("python_compile", not compile_issues, compile_issues, "zero compile failures")

    json_paths = sorted(path for path in args.packet_dir.rglob("*.json") if path.resolve() != args.receipt.resolve())
    json_issues: list[str] = []
    for path in json_paths:
        try:
            read_json(path)
        except (OSError, json.JSONDecodeError):
            json_issues.append(path.relative_to(args.packet_dir).as_posix())
    check("json_parse", not json_issues, {"parsed": len(json_paths), "issues": json_issues}, "all packet JSON parses")

    raw = read_json(args.packet_dir / "raw-audit/workflow-plan-refinement.json")
    normalized = read_json(args.packet_dir / "normalized-pass/workflow-plan-refinement.json")
    check(
        "raw_route_rejecting_witness",
        raw.get("valid") is False
        and raw.get("counts", {}).get("errors") == 4
        and raw.get("counts", {}).get("policy_checks_passed") == 20,
        raw.get("counts"),
        "invalid with four route errors and 20 passing policy checks",
    )
    check(
        "normalized_route_passing_witness",
        normalized.get("valid") is True
        and normalized.get("counts", {}).get("issues") == 0
        and normalized.get("counts", {}).get("policy_checks_passed") == 20
        and normalized.get("counts", {}).get("privacy_findings") == 0,
        normalized.get("counts"),
        "valid with zero issues, 20 passing policy checks, and zero privacy findings",
    )

    method_validation = read_json(args.packet_dir / "method-flow/method-flow-validation.json")
    method_summary = read_json(args.packet_dir / "method-flow/method-flow-summary.json")
    negatives = read_json(args.packet_dir / "method-flow/records/retained-negative-register.json")
    method_counts = method_summary.get("counts", {})
    check(
        "method_flow_validation",
        method_validation.get("valid") is True
        and method_counts.get("methods") == 7
        and method_counts.get("witness_results") == {"fail": 7, "pass": 7}
        and method_counts.get("states", {}).get("preferred") == 7,
        method_counts,
        "seven preferred methods with seven retained fail and seven pass witnesses",
    )
    check(
        "retained_negatives",
        negatives.get("negative_count") == 9
        and len(negatives.get("negatives", [])) == 9
        and negatives.get("erased_negative_count") == 0,
        {
            "declared": negatives.get("negative_count"),
            "rows": len(negatives.get("negatives", [])),
            "erased": negatives.get("erased_negative_count"),
        },
        "nine retained, zero erased",
    )

    document_rows: list[dict[str, Any]] = []
    for path in sorted(args.packet_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".txt", ".html"}:
            words = len(path.read_text(encoding="utf-8").split())
            document_rows.append({"path": path.relative_to(args.packet_dir).as_posix(), "words": words})
    max_words = max((row["words"] for row in document_rows), default=0)
    check("document_word_cap", max_words <= 100000, {"documents": len(document_rows), "maximum_words": max_words}, "maximum <= 100000")

    privacy_hits: list[dict[str, str]] = []
    pattern_classes = {
        "raw_uuid": UUID_RE,
        "private_uri": PRIVATE_URI_RE,
        "absolute_local_path": ABSOLUTE_PATH_RE,
        "credential_assignment": CREDENTIAL_RE,
    }
    scanned_files = 0
    for path in sorted(args.packet_dir.rglob("*")):
        if not path.is_file() or path.resolve() == args.receipt.resolve():
            continue
        if path.suffix.lower() not in {".json", ".md", ".txt", ".html", ".py", ".yaml", ".yml"}:
            continue
        scanned_files += 1
        text = path.read_text(encoding="utf-8")
        for label, pattern in pattern_classes.items():
            if pattern.search(text):
                privacy_hits.append({"path": path.relative_to(args.packet_dir).as_posix(), "class": label})
    check(
        "privacy_scan",
        not privacy_hits,
        {"files": scanned_files, "pattern_classes": sorted(pattern_classes), "hits": privacy_hits},
        "zero concrete privacy hits",
    )

    manifest: list[dict[str, Any]] = []
    for path in sorted(args.packet_dir.rglob("*")):
        if path.is_file() and path.resolve() != args.receipt.resolve():
            manifest.append(
                {
                    "path": path.relative_to(args.packet_dir).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    check("packet_manifest", len(manifest) >= 20, len(manifest), "at least twenty explicitly hashed packet files")

    passed = sum(1 for row in checks if row["passed"])
    receipt = {
        "schema": "ghc.family.workflow-plan.final-validation.v1",
        "valid": passed == len(checks),
        "check_count": len(checks),
        "checks_passed": passed,
        "checks": checks,
        "issue_count": len(issues),
        "issues": issues,
        "json_parse_count": len(json_paths),
        "privacy_file_count": scanned_files,
        "privacy_pattern_class_count": len(pattern_classes),
        "privacy_hits": privacy_hits,
        "manifest_entry_count": len(manifest),
        "manifest": manifest,
        "same_owner_only": True,
        "independent_reproduction": False,
        "route_state": "STANDBY_PREPARED",
        "baton_sent": False,
        "boundary": (
            "Bounded local skill and preparation-packet validation only. It is not phase activation, delivery, "
            "scientific confirmation, identity continuity, independent reproduction, authority, production "
            "readiness, deployment approval, or Stage 20 readiness."
        ),
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "valid": receipt["valid"],
                "checks": f"{passed}/{len(checks)}",
                "json": len(json_paths),
                "privacy_files": scanned_files,
                "privacy_hits": len(privacy_hits),
                "manifest": len(manifest),
            }
        )
    )
    return 0 if receipt["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
