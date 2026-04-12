#!/usr/bin/env python3
"""Publish V40 Mind, Body, and Heart proof bundles with status-aware source resolution."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v40_common import ROOT, now_iso, read_json, repo_rel, resolve_status, write_json, write_text

MIND_JSON = ROOT / "docs" / "trinity-live-traces" / "v40-mind-proof-bundle-v1.json"
MIND_MD = ROOT / "docs" / "trinity-live-traces" / "v40-mind-proof-bundle-v1.md"
BODY_JSON = ROOT / "docs" / "trinity-live-traces" / "v40-body-proof-bundle-v1.json"
BODY_MD = ROOT / "docs" / "trinity-live-traces" / "v40-body-proof-bundle-v1.md"
HEART_JSON = ROOT / "docs" / "trinity-live-traces" / "v40-heart-proof-bundle-v1.json"
HEART_MD = ROOT / "docs" / "trinity-live-traces" / "v40-heart-proof-bundle-v1.md"
COMBINED_JSON = ROOT / "docs" / "trinity-live-traces" / "v40-pillar-bundle-v1.json"
COMBINED_MD = ROOT / "docs" / "trinity-live-traces" / "v40-pillar-bundle-v1.md"


def load_sources(source_map: dict[str, str]) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    resolved = {name: read_json(ROOT / rel) for name, rel in source_map.items()}
    statuses = {name: resolve_status(payload) for name, payload in resolved.items()}
    return resolved, statuses


def build_mind() -> dict[str, Any]:
    sources = {
        "mind_comparator": "docs/mind-track-gmut-comparator-latest.json",
        "mind_trace_validation": "docs/mind-track-gmut-trace-validation-latest.json",
        "mind_evidence_refresh": "docs/trinity-live-traces/mind-evidence-refresh-v17-proof-v1.json",
    }
    _resolved, statuses = load_sources(sources)
    overall = "PASS" if all(value == "PASS" for value in statuses.values()) else "WARN"
    return {
        "generated_utc": now_iso(),
        "phase": "v40_omega",
        "pillar": "mind",
        "overall_status": overall,
        "summary": "Bounded GMUT evidence bundle anchored to authoritative repo comparator, trace validation, and V17 evidence-refresh surfaces.",
        "source_statuses": statuses,
        "source_paths": sources,
        "repair_rule": "Treat status/result/actual_state surfaces as authoritative rather than requiring overall_status only.",
    }


def build_body() -> dict[str, Any]:
    sources = {
        "windows_operator": "docs/trinity-live-traces/v38-windows-operator-proof-v1.json",
        "fleet_anthos": "docs/trinity-live-traces/v38-fleet-anthos-proof-v1.json",
        "os_login": "docs/trinity-live-traces/v38-os-login-proof-v1.json",
        "agent_engine_minimal": "docs/trinity-live-traces/v39-agent-engine-minimal-probe-v1.json",
        "agent_engine_advanced": "docs/trinity-live-traces/v40-agent-engine-advanced-probe-v1.json",
        "runtime_truth_completion": "docs/trinity-live-traces/v40-runtime-truth-completion-v1.json",
        "kai_consultation": "docs/trinity-live-traces/v40-kai-consultation-bridge-v1.json",
        "vesper_runtime": "docs/trinity-live-traces/v40-vesper-runtime-bridge-v1.json",
    }
    _resolved, statuses = load_sources(sources)
    required = (
        statuses.get("agent_engine_minimal") == "PASS"
        and statuses.get("agent_engine_advanced") == "PASS"
        and statuses.get("runtime_truth_completion") == "PASS"
        and statuses.get("kai_consultation") == "PASS"
        and statuses.get("vesper_runtime") == "PASS"
    )
    overall = "PASS" if required else "WARN"
    return {
        "generated_utc": now_iso(),
        "phase": "v40_omega",
        "pillar": "body",
        "overall_status": overall,
        "summary": "Windows operator, fleet/Anthos support, OS Login, bounded Agent Engine live session and memory interaction, runtime-truth completion, Kai bridge, and Vesper memory bridge.",
        "source_statuses": statuses,
        "source_paths": sources,
    }


def build_heart() -> dict[str, Any]:
    sources = {
        "heart_signal_board": "docs/heart-governance-signal-board-latest.json",
        "heart_standards_alignment": "docs/trinity-live-traces/heart-standards-alignment-v17-proof-v1.json",
        "freedid_compliance_fabric": "docs/trinity-live-traces/freedid-compliance-fabric-v16-proof-v1.json",
    }
    _resolved, statuses = load_sources(sources)
    overall = "PASS" if all(value == "PASS" for value in statuses.values()) else "WARN"
    return {
        "generated_utc": now_iso(),
        "phase": "v40_omega",
        "pillar": "heart",
        "overall_status": overall,
        "summary": "Bounded governance, standards-alignment, and Freed ID compliance proof surface without inflating legal-force claims.",
        "source_statuses": statuses,
        "source_paths": sources,
        "repair_rule": "Treat active materialization SKIP surfaces with matching desired_state/actual_state and no blockers as PASS.",
    }


def markdown(payload: dict[str, Any], title: str) -> str:
    lines = [
        f"# {title}",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Summary: {payload['summary']}",
        "",
        "## Source Statuses",
        "",
    ]
    for key, value in payload.get("source_statuses", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish the V40 pillar bundles.")
    parser.add_argument("--combined-json", default=str(COMBINED_JSON))
    parser.add_argument("--combined-md", default=str(COMBINED_MD))
    args = parser.parse_args()

    mind = build_mind()
    body = build_body()
    heart = build_heart()
    combined = {
        "generated_utc": now_iso(),
        "phase": "v40_omega",
        "overall_status": "PASS" if all(row["overall_status"] == "PASS" for row in (mind, body, heart)) else "WARN",
        "pillar_bundle_state": "published",
        "pillars": {
            "mind": {"overall_status": mind["overall_status"], "path": repo_rel(MIND_JSON)},
            "body": {"overall_status": body["overall_status"], "path": repo_rel(BODY_JSON)},
            "heart": {"overall_status": heart["overall_status"], "path": repo_rel(HEART_JSON)},
        },
        "repair_summary": {
            "mind_source_resolution": "status/result-aware",
            "heart_source_resolution": "status/result-aware",
        },
    }

    write_json(MIND_JSON, mind)
    write_text(MIND_MD, markdown(mind, "V40 Mind Proof Bundle"))
    write_json(BODY_JSON, body)
    write_text(BODY_MD, markdown(body, "V40 Body Proof Bundle"))
    write_json(HEART_JSON, heart)
    write_text(HEART_MD, markdown(heart, "V40 Heart Proof Bundle"))
    write_json(Path(args.combined_json), combined)
    write_text(
        Path(args.combined_md),
        markdown(
            {
                "generated_utc": combined["generated_utc"],
                "overall_status": combined["overall_status"],
                "summary": "Combined V40 Mind, Body, and Heart proof bundle.",
                "source_statuses": {key: value["overall_status"] for key, value in combined["pillars"].items()},
            },
            "V40 Pillar Bundle",
        ),
    )
    print(f"pillar_bundle={args.combined_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
