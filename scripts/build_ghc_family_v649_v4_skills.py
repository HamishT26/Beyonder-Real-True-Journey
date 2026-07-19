#!/usr/bin/env python3
"""Customize already initialized v649-v4 phase-local skill packages."""

from __future__ import annotations

import json
from pathlib import Path

from ghc_family_v649_v4_portfolio import RUNNER_RECEIPTS

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v649-v4"


def main() -> None:
    plan = json.loads((PHASE / "prototypes/x1-skill-runner-plan.json").read_text(encoding="utf-8"))
    if len(plan["skills"]) != 20:
        raise RuntimeError("expected exactly twenty frozen skill plans")
    for row in plan["skills"]:
        name = row["name"]
        root = PHASE / "skills" / name
        if not (root / "SKILL.md").is_file():
            raise RuntimeError(f"skill-creator initialization missing for {name}")
        runner = RUNNER_RECEIPTS[name]
        title = " ".join(part.capitalize() for part in name.removeprefix("ghc-family-v649-v4-").split("-"))
        body = f"""---
name: {name}
description: Use for the Orin v649-v4 bounded {title.casefold()} workflow when the frozen proposal or portfolio explicitly selects this phase-local package.
---

# {title}

Use this package only inside the owner-scoped v649-v4 evidence lane. Read the frozen proposal, its source needs, null condition, acceptance gate, rollback, and protected gates before invoking any runner. Run `{runner}` against disposable synthetic, symbolic, structural, proxy, or refusal fixtures, then inspect the repository-relative receipt and retain every rejected mutation or operational failure.

The package may support a bounded passing witness only when the declared fields are present and the corresponding acceptance condition is met. It must not convert citations into observations, software structure into empirical truth, proxy traces into participant or operational effectiveness, synthetic identity vectors into production readiness, or a reservation matrix into legal, cultural, Māori, privacy, biological-material, benefit-sharing, or affected-party authority.

Keep the original failure visible, preserve x1 immutability and caller compatibility, and stop if the task would require credentials, accounts, real keys, real participants, empirical downloads, elevation, host-security changes, sibling mutation, destructive cleanup, Sandbox, Hyper-V, deployment, or external authority. Same-owner evidence remains same-owner evidence, never independent reproduction. Return the bounded receipt path, observed outcome class, retained negatives, and every still-open gate.
"""
        (root / "SKILL.md").write_text(body, encoding="utf-8", newline="\n")
        agents = root / "agents"
        agents.mkdir(parents=True, exist_ok=True)
        metadata = f"""interface:
  display_name: "v649-v4 {title}"
  short_description: "Bounded Orin v649-v4 {title.casefold()} evidence"
  default_prompt: "Use ${name} to run the frozen bounded workflow, retain failures, and preserve every protected gate."
"""
        (agents / "openai.yaml").write_text(metadata, encoding="utf-8", newline="\n")
    print(json.dumps({"initialized_elsewhere": 20, "customized": 20, "global_installed": False}, sort_keys=True))


if __name__ == "__main__":
    main()
