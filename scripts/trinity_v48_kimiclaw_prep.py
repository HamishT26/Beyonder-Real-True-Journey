#!/usr/bin/env python3
"""Publish V48 Kimiclaw slot-41 and swarm 42-53 prep surfaces."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v48_common import ROOT, V48_ARTIFACT_ROOT, git_head, now_iso, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v48-kimiclaw-prep-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v48-kimiclaw-prep-v1.md"
SLOT41_MD = ROOT / "docs" / "v48-kimiclaw-slot-41-receiver-pack-v1.md"
SWARM_JSON = ROOT / "docs" / "trinity-live-traces" / "v48-swarm-42-53-spec-v1.json"
SWARM_MD = ROOT / "docs" / "trinity-live-traces" / "v48-swarm-42-53-spec-v1.md"
ARTIFACT_SWARM_JSON = V48_ARTIFACT_ROOT / "v48-swarm-registry-spec-v1.json"

SWARM_ROLES = [
    "intake-cartographer",
    "source-anchor-auditor",
    "suite-residual-summarizer",
    "plugin-surface-mapper",
    "notion-mission-scribe",
    "vercel-sandbox-scout",
    "neon-schema-steward",
    "circleci-signal-runner",
    "kimiclaw-runtime-witness",
    "memory-boundary-keeper",
    "handoff-packager",
    "risk-and-cost-governor",
]


def _swarm_slots() -> list[dict[str, Any]]:
    slots = []
    for offset, role in enumerate(SWARM_ROLES, start=42):
        slots.append(
            {
                "slot_number": offset,
                "label": f"kimiclaw-{role}",
                "role": role.replace("-", " "),
                "continuity_state": "spec_only_not_spawned",
                "runtime_surface": "future_kimiclaw_or_kimi_runtime",
                "proof_gate": "must be spawned by inducted slot 41 and then pass identity_memory_task_publication gates",
            }
        )
    return slots


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V48 Kimiclaw Prep",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Slot 41 state: `{payload['slot_41_preparation_state']}`",
        f"- Swarm 42-53 state: `{payload['swarm_42_53_state']}`",
        "",
        "## Required Future Gates",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["future_slot_41_gates"])
    return "\n".join(lines).rstrip() + "\n"


def _slot41_pack(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# V48 Kimiclaw Slot 41 Receiver Pack",
            "",
            "Slot 41 is prepared, not inducted.",
            "",
            "## Future Induction Gates",
            "",
            *[f"- {item}" for item in payload["future_slot_41_gates"]],
            "",
            "## Continuity Rule",
            "",
            "No slot 41 certificate, role contract, memory ledger, or official identity claim is valid until the future Kimiclaw runtime passes every gate and the operator explicitly performs the induction.",
            "",
            "## Handoff Prompt",
            "",
            "Read the V48 closeout, this receiver pack, the swarm 42-53 spec, and the plugin-surface matrix. Report only what your runtime can actually prove.",
        ]
    ) + "\n"


def _swarm_markdown(slots: list[dict[str, Any]]) -> str:
    lines = ["# V48 Swarm 42-53 Spec", "", "All listed slots are spec-only and not spawned in V48.", ""]
    lines.extend(f"- Slot `{row['slot_number']}`: `{row['label']}` - `{row['continuity_state']}`" for row in slots)
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish V48 Kimiclaw prep artifacts.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()
    slots = _swarm_slots()
    payload = {
        "generated_utc": now_iso(),
        "phase": "v48_omega",
        "overall_status": "PASS",
        "current_head_sha": git_head(),
        "kimiclaw_research_state": "official_sources_anchored_advisory_claims_bounded",
        "slot_41_preparation_state": "prepared_not_inducted",
        "swarm_42_53_state": "spec_only_not_spawned",
        "slot_41_identity_state": "operator_reserved_future_induction",
        "future_slot_41_gates": [
            "official Kimi or Moonshot account/auth truth",
            "runtime identity and model-name truth",
            "CLI, SDK, or web-agent callability proof",
            "one read-only repo analysis proof",
            "one bounded memory or handoff continuity proof",
            "operator-confirmed induction after gates pass",
        ],
        "blocked_claims": [
            "no slot 41 certificate in V48",
            "no slots 42-53 certificates in V48",
            "no claim that Kimiclaw can use Codex app plugins from CLI or Kimi runtime without proof",
            "no 300-agent swarm spawn in V48",
        ],
        "swarm_slots": slots,
        "source_anchors": [
            {"name": "Moonshot platform overview", "url": "https://platform.moonshot.ai/docs/overview"},
            {"name": "Kimi Claw introduction", "url": "https://www.kimi.com/resources/kimi-claw-introduction"},
        ],
        "published_paths": {
            "slot_41_receiver_pack": SLOT41_MD.relative_to(ROOT).as_posix(),
            "swarm_spec_json": SWARM_JSON.relative_to(ROOT).as_posix(),
            "swarm_spec_md": SWARM_MD.relative_to(ROOT).as_posix(),
            "artifact_swarm_registry": str(ARTIFACT_SWARM_JSON),
        },
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    write_text(SLOT41_MD, _slot41_pack(payload))
    write_json(SWARM_JSON, {"generated_utc": now_iso(), "phase": "v48_omega", "swarm_42_53_state": "spec_only_not_spawned", "slots": slots})
    write_text(SWARM_MD, _swarm_markdown(slots))
    write_json(ARTIFACT_SWARM_JSON, {"generated_utc": now_iso(), "artifact_scope": "d_drive_non_authoritative_spec_copy", "slots": slots})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
