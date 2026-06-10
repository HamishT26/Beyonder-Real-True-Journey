#!/usr/bin/env python3
"""Publish bounded V39 Mind, Body, and Heart proof bundles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
MIND_JSON = ROOT / "docs" / "trinity-live-traces" / "v39-mind-proof-bundle-v1.json"
MIND_MD = ROOT / "docs" / "trinity-live-traces" / "v39-mind-proof-bundle-v1.md"
BODY_JSON = ROOT / "docs" / "trinity-live-traces" / "v39-body-proof-bundle-v1.json"
BODY_MD = ROOT / "docs" / "trinity-live-traces" / "v39-body-proof-bundle-v1.md"
HEART_JSON = ROOT / "docs" / "trinity-live-traces" / "v39-heart-proof-bundle-v1.json"
HEART_MD = ROOT / "docs" / "trinity-live-traces" / "v39-heart-proof-bundle-v1.md"
COMBINED_JSON = ROOT / "docs" / "trinity-live-traces" / "v39-pillar-bundle-v1.json"
COMBINED_MD = ROOT / "docs" / "trinity-live-traces" / "v39-pillar-bundle-v1.md"


def now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def proof_status(payload: dict[str, Any]) -> str:
    return str(payload.get("overall_status") or "MISSING")


def build_mind() -> dict[str, Any]:
    sources = {
        "mind_comparator": "docs/mind-track-gmut-comparator-latest.json",
        "mind_trace_validation": "docs/mind-track-gmut-trace-validation-latest.json",
        "mind_evidence_refresh": "docs/trinity-live-traces/mind-evidence-refresh-v17-proof-v1.json",
    }
    resolved = {name: read_json(ROOT / rel) for name, rel in sources.items()}
    statuses = {name: proof_status(payload) for name, payload in resolved.items()}
    overall = "PASS" if all(value == "PASS" for value in statuses.values()) else "WARN"
    return {
        "generated_utc": now_iso(),
        "phase": "v39_omega",
        "pillar": "mind",
        "overall_status": overall,
        "summary": "Bounded GMUT evidence bundle anchored to current repo and public-source truth.",
        "source_statuses": statuses,
        "source_paths": sources,
    }


def build_body() -> dict[str, Any]:
    sources = {
        "windows_operator": "docs/trinity-live-traces/v38-windows-operator-proof-v1.json",
        "fleet_anthos": "docs/trinity-live-traces/v38-fleet-anthos-proof-v1.json",
        "os_login": "docs/trinity-live-traces/v38-os-login-proof-v1.json",
        "agent_engine_forensics": "docs/trinity-live-traces/v39-agent-engine-forensics-v1.json",
        "agent_engine_minimal": "docs/trinity-live-traces/v39-agent-engine-minimal-probe-v1.json",
        "kai_consultation": "docs/trinity-live-traces/v39-kai-consultation-bridge-v1.json",
        "vesper_runtime": "docs/trinity-live-traces/v39-vesper-runtime-bridge-v1.json",
    }
    resolved = {name: read_json(ROOT / rel) for name, rel in sources.items()}
    statuses = {name: proof_status(payload) for name, payload in resolved.items()}
    overall = "PASS"
    if statuses.get("agent_engine_minimal") != "PASS":
        overall = "WARN"
    if statuses.get("kai_consultation") != "PASS" or statuses.get("vesper_runtime") != "PASS":
        overall = "WARN"
    return {
        "generated_utc": now_iso(),
        "phase": "v39_omega",
        "pillar": "body",
        "overall_status": overall,
        "summary": "Windows operator, cloud runtime, Anthos/fleet support, Agent Engine recovery, Kai bridge, and Vesper memory bridge.",
        "source_statuses": statuses,
        "source_paths": sources,
    }


def build_heart() -> dict[str, Any]:
    sources = {
        "heart_signal_board": "docs/heart-governance-signal-board-latest.json",
        "heart_standards_alignment": "docs/trinity-live-traces/heart-standards-alignment-v17-proof-v1.json",
        "freedid_compliance_fabric": "docs/trinity-live-traces/freedid-compliance-fabric-v16-proof-v1.json",
    }
    resolved = {name: read_json(ROOT / rel) for name, rel in sources.items()}
    statuses = {name: proof_status(payload) for name, payload in resolved.items()}
    overall = "PASS" if all(value == "PASS" for value in statuses.values()) else "WARN"
    return {
        "generated_utc": now_iso(),
        "phase": "v39_omega",
        "pillar": "heart",
        "overall_status": overall,
        "summary": "Bounded governance/Freed ID/Cosmic Bill proof surface without changing legal-force claims.",
        "source_statuses": statuses,
        "source_paths": sources,
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
    parser = argparse.ArgumentParser(description="Publish bounded V39 pillar bundles.")
    parser.add_argument("--combined-json", default=str(COMBINED_JSON))
    parser.add_argument("--combined-md", default=str(COMBINED_MD))
    args = parser.parse_args()

    mind = build_mind()
    body = build_body()
    heart = build_heart()
    combined = {
        "generated_utc": now_iso(),
        "phase": "v39_omega",
        "overall_status": "PASS" if all(item["overall_status"] == "PASS" for item in (mind, body, heart)) else "WARN",
        "pillar_bundle_state": "published",
        "pillars": {
            "mind": {"overall_status": mind["overall_status"], "path": str(MIND_JSON.relative_to(ROOT)).replace("\\", "/")},
            "body": {"overall_status": body["overall_status"], "path": str(BODY_JSON.relative_to(ROOT)).replace("\\", "/")},
            "heart": {"overall_status": heart["overall_status"], "path": str(HEART_JSON.relative_to(ROOT)).replace("\\", "/")},
        },
    }

    write_json(MIND_JSON, mind)
    write_text(MIND_MD, markdown(mind, "V39 Mind Proof Bundle"))
    write_json(BODY_JSON, body)
    write_text(BODY_MD, markdown(body, "V39 Body Proof Bundle"))
    write_json(HEART_JSON, heart)
    write_text(HEART_MD, markdown(heart, "V39 Heart Proof Bundle"))
    write_json(Path(args.combined_json), combined)
    write_text(Path(args.combined_md), markdown({
        "generated_utc": combined["generated_utc"],
        "overall_status": combined["overall_status"],
        "summary": "Combined V39 Mind, Body, and Heart proof bundle.",
        "source_statuses": {key: value["overall_status"] for key, value in combined["pillars"].items()},
    }, "V39 Pillar Bundle"))
    print(f"pillar_bundle={args.combined_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
