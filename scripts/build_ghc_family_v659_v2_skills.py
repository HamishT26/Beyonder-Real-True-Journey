#!/usr/bin/env python3
"""Customize the ten skill-creator initialized Auren v659-v2 packages."""

from __future__ import annotations

from pathlib import Path

import ghc_family_v659_v2_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE_SKILLS = ROOT / d.PHASE_ROOT / "skills"


def title(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-")[2:])


def main() -> None:
    rows = []
    for (skill_name, purpose), (runner_name, surface) in zip(
        d.SELF_SKILL_SPECS, d.SELF_RUNNER_SPECS, strict=True
    ):
        skill_dir = PHASE_SKILLS / skill_name
        skill_file = skill_dir / "SKILL.md"
        agent_file = skill_dir / "agents/openai.yaml"
        if not skill_file.is_file() or not agent_file.is_file():
            raise FileNotFoundError(f"skill-creator initialization missing for {skill_name}")
        description = (
            f"{purpose} Use when Codex must run the bounded {surface} synthetic guard, "
            "retain rejecting mutations, and preserve empirical, professional, legal, cultural, "
            "Māori-authority, production, identity, and Stage 20 boundaries."
        )
        body = f"""---
name: {skill_name}
description: {description}
---

# {title(skill_name)}

Use this skill only for the `{surface}` bounded synthetic surface.

## Workflow

1. Confirm the input contains synthetic aliases only and requests no real fountain pen, ink, customer record, material measurement, writing trial, treatment, authentication, valuation, chemical-safety, identity, legal, cultural, or authority decision.
2. Run `python -X utf8 scripts/{runner_name} --output <owner-local-json>` from the repository root.
3. Require one valid fixture, exactly five rejected mutations, zero external rows, zero network calls, decision abstention, and rollback preservation.
4. Treat every rejected mutation as a retained zero-credit witness. Do not convert a later pass into an initially clean run.
5. Stop and classify the result as `open_gap` or `exact_gate` if real objects or data, repair or conservation competence, chemical-safety review, affected-party legitimacy, legal interpretation, cultural ratification, Māori authority, or production state is required.

## Output contract

Return the runner's JSON receipt unchanged. Report its `valid_fixture_passed`, `rejected_mutation_count`, `all_mutations_rejected`, and boundary fields. Never publish matched secret values or private route identifiers.

## Boundaries

The runner is same-owner structural evidence under shared infrastructure. It is not fountain-pen repair, conservation, authentication, valuation, material compatibility, chemical-safety or customer decision authority, empirical GMUT confirmation, professional validation, production assurance, complete privacy or accessibility, exhaustive security, independent reproduction, consciousness or personhood evidence, a Theory of Everything, or Stage 20 authority.
"""
        skill_file.write_text(body, encoding="utf-8", newline="\n")
        rows.append(skill_name)
    print(f"customized={len(rows)}")


if __name__ == "__main__":
    main()
