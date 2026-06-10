#!/usr/bin/env python3
"""Build v473 THOS v8 x1 repo-only skill design card artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v473-thos-v8-x1"
NEXT_PHASE = "v473-thos-v8-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"

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


def read_json(name: str) -> dict[str, Any]:
    path = ARTIFACT_ROOT / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


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


def skill_design_card(item: dict[str, Any], index: int) -> dict[str, Any]:
    domain = item.get("domain")
    return {
        "approval_required_for_install": True,
        "blocked_paths": [
            "user_skill_root",
            "plugin_cache_root",
        ],
        "claim_ceiling": "repo-only THOS design; no runtime skill activation or GMUT validation.",
        "domain": domain,
        "frontmatter_requirements": ["name", "description"],
        "implementation_status": "DESIGN_CARD_ONLY",
        "kind": "skill-design-card",
        "route_card_id": f"{PHASE}-skill-design-{index:02d}",
        "safe_publication_scope": "docs/trinity-live-traces and scripts only",
        "source_id": item.get("source_id"),
        "source_name": item.get("source_name"),
        "suggested_skill_name": f"thos-{domain}-operations-v473",
        "task": f"Design, but do not install, a THOS skill for {domain} reliability.",
    }


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    cards_source = read_json("v473-thos-v7-x2-system-command-route-cards-v1.json")
    held = cards_source.get("held_skill_route_cards", [])
    design_cards = [skill_design_card(item, index) for index, item in enumerate(held, start=1)]

    design_rows = [
        row("source_cards", cards_source.get("aggregate_status", "OPEN_GAP"), "Skill design source is v7 x2 held skill cards."),
        row("design_count", "PASS_SHAPE_ONLY" if len(design_cards) == 8 else "FAIL_BLOCKER", "Eight repo-only skill design cards are materialized.", {"count": len(design_cards)}),
        row("install_boundary", "OPEN_GAP", "No user skill or plugin-cache install is approved or performed."),
        row("claim_boundary", "PASS_SHAPE_ONLY", "Skill design cards do not affect GMUT gates."),
    ]
    designs = {
        "aggregate_status": aggregate(design_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "rows": design_rows,
        "skill_design_cards": design_cards,
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-repo-only-skill-design-cards-v1.json"
    write_json(path, designs)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-repo-only-skill-design-cards-v1.md",
        f"""
# v473 THOS v8 x1 Repo-Only Skill Design Cards

Generated UTC: `{generated_at}`

Status: `{designs['aggregate_status']}`

Materialized `8` repo-only skill design cards.

No user skill directory or plugin cache mutation is performed.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-repo-only-skill-design-cards-v1.md")

    approval_rows = [
        row("install_scope", "OPEN_GAP", "Actual skill installation requires a future exact path-specific approval packet."),
        row("repo_scope", "PASS_SHAPE_ONLY", "Repo-only design artifacts remain within approved curated paths."),
        row("body_boundary", "PASS_SHAPE_ONLY", "No SKILL.md body text is generated for live installation."),
        row("frontmatter_note", "PASS_SHAPE_ONLY", "Future install packets must verify frontmatter name and description."),
    ]
    approval = {
        "aggregate_status": aggregate(approval_rows),
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "rows": approval_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-skill-install-approval-boundary-v1.json"
    write_json(path, approval)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-skill-install-approval-boundary-v1.md",
        """
# v473 THOS v8 x1 Skill Install Approval Boundary

Skill designs are repo-only. Any live user-skill or plugin-cache write requires a future exact path-specific approval packet.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-skill-install-approval-boundary-v1.md")

    status_rows = [
        row("designs", designs["aggregate_status"], "Repo-only skill design cards published."),
        row("approval_boundary", approval["aggregate_status"], "Skill install approval boundary published."),
    ]
    run_status = {
        "aggregate_status": aggregate(status_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": status_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(path, run_status)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md",
        f"""
# v473 THOS v8 x1 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v8 x1 materializes repo-only skill design cards and an install-approval boundary.

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
