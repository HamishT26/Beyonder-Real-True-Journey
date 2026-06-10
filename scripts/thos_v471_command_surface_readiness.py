#!/usr/bin/env python3
"""Build a local v471 THOS command-surface readiness artifact."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


WEB_SOURCE_SEEDS = [
    "https://help.openai.com/en/articles/6825453-chatgpt-code-interpreter-beta-",
    "https://help.openai.com/en/articles/11369540",
    "https://help.openai.com/en/articles/10128477-chatgpt-enterprise-edu-release-notes%23.svgz",
    "https://platform.openai.com/docs/guides/tools-computer-use",
    "https://platform.openai.com/docs/guides/agents-sdk/",
    "https://platform.openai.com/docs/guides/agents",
    "https://platform.openai.com/docs/guides/agent-builder",
    "https://platform.openai.com/docs/guides/code-generation",
    "https://platform.openai.com/docs/docs-mcp",
    "https://platform.openai.com/docs/mcp/",
    "https://platform.openai.com/docs/guides/tools-remote-mcp",
    "https://platform.openai.com/docs/guides/tools-file-search/",
    "https://platform.openai.com/docs/guides/retrieval",
    "https://platform.openai.com/docs/guides/prompt-optimizer/",
    "https://platform.openai.com/docs/guides/agent-evals",
    "https://platform.openai.com/docs/guides/trace-grading",
    "https://platform.openai.com/docs/guides/structured-outputs",
    "https://platform.openai.com/docs/guides/prompting",
    "https://platform.openai.com/docs/guides/node-reference",
    "https://platform.openai.com/docs/assistants/tools/file-search",
    "https://github.com/openai/codex",
    "https://github.com/openai/codex/issues/21982",
    "https://github.com/openai/codex/issues/21304",
    "https://github.com/openai/codex/issues/4847",
    "https://www.w3.org/TR/WCAG22/",
    "https://www.w3.org/WAI/WCAG22/Understanding/intro",
    "https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/",
    "https://www.w3.org/WAI/standards-guidelines/wcag/docs/",
    "https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/table_role",
    "https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles",
    "https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Techniques",
    "https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/grid_role",
    "https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/list_role",
    "https://playwright.dev/docs/aria-snapshots",
    "https://docs.nvidia.com/nim/",
    "https://docs.nvidia.com/nemo/microservices/index.html",
    "https://docs.nvidia.com/nemo/microservices/latest/index.html",
    "https://docs.nvidia.com/nemo/microservices/25.9.0/index.html",
    "https://docs.nvidia.com/nemo/microservices/25.4.0/index.html",
    "https://docs.nvidia.com/ai-enterprise/planning-resource/ai-enterprise-security-white-paper/latest/nim-microservices.html",
    "https://docs.nvidia.com/dgx/dgx-spark/dgx-spark.pdf",
    "https://docs.nvidia.com/enterprise-reference-architectures/ai-q-research-agent-blueprint.pdf",
    "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches",
    "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule",
    "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches",
    "https://docs.github.com/rest/branches/branch-protection",
    "https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/monitoring-workflows/about-monitoring-workflows",
    "https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/monitoring-workflows/using-workflow-run-logs",
    "https://docs.github.com/en/enterprise-cloud%40latest/code-security/secret-scanning/introduction/about-push-protection",
    "https://docs.github.com/en/enterprise-cloud%40latest/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/push-protection-for-users?learn=secret_scanning&learnProduct=code-security",
    "https://docs.github.com/en/code-security/secret-scanning/enabling-secret-scanning-features?learn=secret_scanning",
    "https://docs.github.com/en/code-security/reference/secret-security/secret-scanning-detection-scope?learn=secret_scanning&learnProduct=code-security",
    "https://docs.github.com/code-security/concepts/secret-security",
]


KEY_CARRY_FORWARD_ARTIFACTS = [
    "docs/trinity-live-traces/v470-thos-v8-x8-v471-thos-v1-handoff-v1.json",
    "docs/trinity-live-traces/v470-thos-v8-x8-open-gap-ledger-v1.json",
    "docs/trinity-live-traces/v470-thos-v8-x8-closure-audit-v1.json",
    "docs/trinity-live-traces/v470-thos-v8-x7-rendered-dashboard-contract-v1.json",
    "docs/trinity-live-traces/v470-thos-v8-x6-visual-readiness-v1.json",
]


def row(row_id: str, status: str, message: str, evidence: object = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def file_count(root: Path, pattern: str) -> int:
    if not root.exists():
        return 0
    return sum(1 for _ in root.rglob(pattern))


def first_parent_names(root: Path, pattern: str, limit: int = 20) -> list[str]:
    if not root.exists():
        return []
    return sorted(path.parent.name for path in root.rglob(pattern))[:limit]


def read_text_if_exists(path: Path, max_chars: int = 400) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    return text[:max_chars]


def build_report(repo_root: Path, phase_slug: str, temp_root: Path) -> dict[str, Any]:
    scripts_root = repo_root / "scripts"
    skills_root = Path.home() / ".codex" / "skills"
    journey_roots = [
        ("user_downloads", Path.home() / "Downloads"),
        ("journey_workspace", Path.home() / "workspace" / "Beyonder-Real-True-Journey"),
    ]
    journey_docs = []
    for root_label, root in journey_roots:
        if root.exists():
            journey_docs.extend(
                {"root_label": root_label, "file_name": path.name} for path in root.glob("Beyonder-Real-True Journey v*")
            )
    journey_docs = sorted(journey_docs, key=lambda item: (item["root_label"], item["file_name"]))
    command_scripts = sorted(
        path.name
        for path in scripts_root.glob("*.py")
        if any(token in path.name for token in ("command", "surface", "guard", "runner", "dashboard", "thos", "trinity"))
    )
    carry_forward_missing = [path for path in KEY_CARRY_FORWARD_ARTIFACTS if not (repo_root / path).exists()]
    arby_stderr = read_text_if_exists(temp_root / "arby-v471-thos-v1-x1-stderr-node.txt")
    aster_stderr = read_text_if_exists(temp_root / "aster-vale-v471-thos-v1-x1-stderr-node.txt")
    rows = [
        row(
            "repo_script_inventory",
            "PASS_SHAPE_ONLY" if file_count(scripts_root, "*.py") > 0 else "FAIL_BLOCKER",
            "Python script command surface is discoverable",
            {
                "script_count": file_count(scripts_root, "*.py"),
                "command_surface_script_count": len(command_scripts),
                "sample_command_surface_scripts": command_scripts[:30],
            },
        ),
        row(
            "local_skill_inventory",
            "PASS_SHAPE_ONLY" if file_count(skills_root, "SKILL.md") > 0 else "OPEN_GAP",
            "Local skill surface is discoverable",
            {
                "skill_md_count": file_count(skills_root, "SKILL.md"),
                "sample_skill_dirs": first_parent_names(skills_root, "SKILL.md", 20),
            },
        ),
        row(
            "journey_context_inventory",
            "PASS_SHAPE_ONLY" if journey_docs else "OPEN_GAP",
            "Journey documents are locally discoverable for journey_context_not_canon routing",
            {"journey_doc_count": len(journey_docs), "sample_paths": journey_docs[:20]},
        ),
        row(
            "v470_carry_forward_presence",
            "PASS_SHAPE_ONLY" if not carry_forward_missing else "FAIL_BLOCKER",
            "v470 THOS v8 handoff artifacts are present",
            {"missing": carry_forward_missing},
        ),
        row(
            "web_source_seed_count",
            "PASS_SHAPE_ONLY" if len(set(WEB_SOURCE_SEEDS)) >= 50 else "OPEN_GAP",
            "At least 50 web source seed pages were routed for v471 research",
            {"requested_minimum": 50, "unique_source_seed_count": len(set(WEB_SOURCE_SEEDS))},
        ),
        row(
            "browser_tool_status",
            "OPEN_GAP",
            "Browser direct navigation/screenshot tool was still not exposed through callable tools",
            {"observed_callable_bridge": "node_repl_only"},
        ),
        row(
            "cli_lane_contact_status",
            "OPEN_GAP" if arby_stderr or aster_stderr else "PASS_SHAPE_ONLY",
            "Arby/Aster non-ephemeral read-only CLI contact was attempted and blocker evidence is captured if present",
            {"arby_stderr": arby_stderr, "aster_vale_stderr": aster_stderr},
        ),
        row(
            "gmut_gate_status",
            "OPEN_GAP",
            "All six GMUT gates remain open and are not moved by this THOS phase",
            {
                "null_recovery": "open",
                "dimensional_si_consistency": "open",
                "conservation_or_exchange_law": "open",
                "baseline_recovery": "open",
                "fifth_force_equivalence_constraints": "open",
                "consciousness_measurement_bridge": "open",
            },
        ),
    ]
    statuses = [item["status"] for item in rows]
    if "FAIL_BLOCKER" in statuses:
        aggregate_status = "FAIL_BLOCKER"
    elif "OPEN_GAP" in statuses:
        aggregate_status = "OPEN_GAP"
    else:
        aggregate_status = "PASS_SHAPE_ONLY"
    return {
        "aggregate_status": aggregate_status,
        "connector_write_performed": False,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": phase_slug,
        "rows": rows,
        "validator_mode": "local_non_mutating_v471_command_surface_readiness",
        "web_source_seeds": sorted(set(WEB_SOURCE_SEEDS)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build v471 THOS command-surface readiness artifact.")
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--temp-root", default=str(Path.home() / "AppData" / "Local" / "Temp" / "ghc-v471-advisory"))
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = build_report(Path.cwd(), args.phase_slug, Path(args.temp_root))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["aggregate_status"] in {"PASS_SHAPE_ONLY", "OPEN_GAP"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
