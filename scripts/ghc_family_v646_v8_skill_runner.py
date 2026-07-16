#!/usr/bin/env python3
"""Build, validate, and smoke-use the 20 frozen v646-v8 phase-local skills."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import ghc_family_v646_v8_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v646-v8"
SKILL_ROOT = PHASE / "prototypes/skills"

RUNNER_BY_SKILL = {
    "ghc-family-merkle-split-view-tribunal": "ghc_family_merkle_split_view.py",
    "ghc-family-vilkovisky-dewitt-obligations": "ghc_family_vilkovisky_dewitt_obligations.py",
    "ghc-family-gwosc-o4a-zero-row": "ghc_family_gwosc_o4a_zero_row.py",
    "ghc-family-aviation-techlog-handover": "ghc_family_aviation_techlog_handover.py",
    "ghc-family-scitt-statement-profile": "ghc_family_scitt_statement_profile.py",
    "ghc-family-aviation-authority-reservation": "ghc_family_v646_v8_runtime.py",
    "ghc-family-sqlite-backup-confinement": "ghc_family_sqlite_backup_confinement.py",
    "ghc-family-carousel-motion-audit": "ghc_family_carousel_motion_audit.py",
    "ghc-family-maxwell-reciprocity-domain": "ghc_family_maxwell_reciprocity_domain.py",
    "ghc-family-harking-lineage-guard": "ghc_family_harking_lineage_guard.py",
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def skill_markdown(name: str, purpose: str) -> str:
    runner = RUNNER_BY_SKILL.get(name)
    execution = (
        f"Invoke `scripts/{runner}` only on declared owner-local fixtures and inspect its JSON result."
        if runner
        else "Inspect the exact phase ledger or Git evidence named by the request; do not infer missing evidence."
    )
    return f"""---
name: {name}
description: Use when a v646-v8 family packet must {purpose[0].lower() + purpose[1:]}; preserves evidence and authority gates.
---

# {name}

## Trigger and scope

Use this phase-local skill when the requested surface is: **{purpose}**. It applies only to the Ilyra Fen v646-v8 owner-local structural, symbolic, synthetic, or read-only Git evidence lane. It is not installed globally.

## Procedure

1. Confirm the input and requested effect remain owner-scoped and within the frozen x1 approval class.
2. {execution}
3. Treat every rejected fixture, timeout, parser fault, tooling failure, and false assumption as a retained negative.
4. Accept only an exact bounded witness; leave absent evidence as `open_gap` and absent authority as `exact_gate`.
5. Emit only `completed`, `represented`, `open_gap`, or `exact_gate` for a core proposal.

## Acceptance and recovery

Acceptance requires a deterministic witness, zero protected-gate crossings, and an explicit boundary statement. On failure, stop, preserve the failed witness through Method Flow, apply only a trigger-matched recovery, and rerun the unchanged check. Recovery never erases the original failure.

## Protected boundary

Stop before real people, aircraft, observations, keys, signatures, production services, legal or cultural decisions, Māori authority, deployment, destructive changes, independent-reproduction claims, or Stage 20 promotion. {d.TRUTH_BOUNDARY}
"""


def yaml_text(name: str, purpose: str) -> str:
    display = name.removeprefix("ghc-family-").replace("-", " ").title()
    short = purpose if len(purpose) <= 100 else purpose[:97].rstrip() + "..."
    return f'''interface:
  display_name: "GHC Family {display}"
  short_description: "{short}"
  default_prompt: "Use ${name} to apply its bounded v646-v8 procedure and preserve every protected gate."
'''


def internal_smoke(path: Path, name: str) -> list[str]:
    issues: list[str] = []
    skill = (path / "SKILL.md").read_text(encoding="utf-8")
    yaml = (path / "agents/openai.yaml").read_text(encoding="utf-8")
    match = re.match(r"^---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n", skill)
    if not match or match.group(1) != name:
        issues.append("frontmatter name or shape invalid")
    for heading in ("## Trigger and scope", "## Procedure", "## Acceptance and recovery", "## Protected boundary"):
        if heading not in skill:
            issues.append(f"missing {heading}")
    if f"${name}" not in yaml:
        issues.append("default prompt does not name the skill")
    runner = RUNNER_BY_SKILL.get(name)
    if runner and not (ROOT / "scripts" / runner).is_file():
        issues.append(f"runner missing: {runner}")
    return issues


def main() -> int:
    validator_root = os.environ.get("CODEX_SKILL_CREATOR_ROOT")
    validator = Path(validator_root) / "scripts/quick_validate.py" if validator_root else None
    rows = []
    for name, purpose in d.SKILL_SPECS:
        path = SKILL_ROOT / name
        write(path / "SKILL.md", skill_markdown(name, purpose))
        write(path / "agents/openai.yaml", yaml_text(name, purpose))
        smoke_issues = internal_smoke(path, name)
        official_returncode = None
        official_output = "validator root not supplied"
        if validator and validator.is_file():
            result = subprocess.run(
                [sys.executable, str(validator), str(path)],
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
                timeout=30,
                check=False,
            )
            official_returncode = result.returncode
            official_output = (result.stdout + result.stderr).strip()
        issues = list(smoke_issues)
        if official_returncode != 0:
            issues.append("skill-creator quick validation did not pass")
        rows.append(
            {
                "name": name,
                "description": purpose,
                "path": f"prototypes/skills/{name}/SKILL.md",
                "phase_local": True,
                "global_skill_install": False,
                "built": True,
                "skill_creator_quick_validate_returncode": official_returncode,
                "skill_creator_output": official_output,
                "smoke_used": not smoke_issues,
                "validated": not issues,
                "issues": issues,
                "authority_granted": False,
                "forward_test_by_subagent": "not_run_because_subagents_are_explicitly_prohibited",
            }
        )
    payload = {
        "schema": "ghc.family.v646-v8.skill-build-use.v1",
        "phase": d.PHASE,
        "skill_count": len(rows),
        "built_count": sum(row["built"] for row in rows),
        "validated_count": sum(row["validated"] for row in rows),
        "smoke_used_count": sum(row["smoke_used"] for row in rows),
        "global_skill_changes": 0,
        "skills": rows,
        "result": "pass" if len(rows) == 20 and all(row["validated"] and row["smoke_used"] for row in rows) else "fail",
        "boundary": d.TRUTH_BOUNDARY,
    }
    write(PHASE / "prototypes/skill-build-use-receipt.json", json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    print(json.dumps({"skills": len(rows), "validated": payload["validated_count"], "smoke_used": payload["smoke_used_count"], "result": payload["result"]}, ensure_ascii=False))
    return 0 if payload["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
