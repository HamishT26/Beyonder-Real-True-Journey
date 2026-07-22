#!/usr/bin/env python3
"""Initialize, customize, validate, and smoke-use Vesper v651-v7 tools."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from ghc_family_v651_v7_runtime import GROUPS, PHASE, REPO, run_group


SKILLS = [
    ("ghc-family-lsm-reclamation-boundary", "LSM Reclamation Boundary", "Use when auditing tombstone horizons and snapshot-safe reclamation.", "storage-reclamation"),
    ("ghc-family-mvcc-write-skew", "MVCC Write Skew", "Use when checking snapshot transactions for predicate write skew.", "concurrency-reclamation"),
    ("ghc-family-epoch-reclamation", "Epoch Reclamation", "Use when checking quiescence and retirement epochs.", "concurrency-reclamation"),
    ("ghc-family-hazard-aba", "Hazard ABA", "Use when checking tagged ownership and ABA refusal.", "concurrency-reclamation"),
    ("ghc-family-monotonic-deadline", "Monotonic Deadline", "Use when timeouts must survive wall-clock discontinuities.", "time-rate-fairness"),
    ("ghc-family-rate-fairness", "Rate and Fairness", "Use when reviewing token buckets or weighted service.", "time-rate-fairness"),
    ("ghc-family-merkle-range-proof", "Merkle Range Proof", "Use when reviewing range completeness, ordering, and typed hashing.", "integrity-range"),
    ("ghc-family-wal-checkpoint-boundary", "WAL Checkpoint Boundary", "Use when distinguishing partial checkpoints from complete reset.", "transaction-checkpoint"),
    ("ghc-family-schema-transition", "Schema Transition", "Use when reviewing expand-contract and dual-write compatibility.", "schema-cache-concurrency"),
    ("ghc-family-conditional-update", "Conditional Update", "Use when reviewing ETag preconditions or monotone claim withdrawal.", "conditional-update"),
    ("ghc-family-numerical-enclosure", "Numerical Enclosure", "Use when reviewing aliasing, interval, conditioning, or commutator boundaries.", "numerical-boundary"),
    ("ghc-family-preservation-authority", "Preservation Authority", "Use when preservation actions need explicit evidence and authority separation.", "stage20-authority-refusal"),
]

RUNNERS = {
    "ghc_family_storage_reclamation.py": "storage-reclamation",
    "ghc_family_concurrency_reclamation.py": "concurrency-reclamation",
    "ghc_family_time_rate_fairness.py": "time-rate-fairness",
    "ghc_family_integrity_range.py": "integrity-range",
    "ghc_family_transaction_checkpoint.py": "transaction-checkpoint",
    "ghc_family_schema_cache_concurrency.py": "schema-cache-concurrency",
    "ghc_family_conditional_update.py": "conditional-update",
    "ghc_family_numerical_boundary.py": "numerical-boundary",
    "ghc_family_identity_accessibility_proxy.py": "identity-accessibility-proxy",
    "ghc_family_stage20_authority_refusal.py": "stage20-authority-refusal",
}


def write_json(relative: str, payload: object) -> None:
    target = PHASE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def build_skills() -> list[dict[str, object]]:
    creator = Path.home() / ".codex/skills/.system/skill-creator"
    init = creator / "scripts/init_skill.py"
    generate = creator / "scripts/generate_openai_yaml.py"
    validate = creator / "scripts/quick_validate.py"
    skill_root = PHASE / "skills"
    rows = []
    environment = dict(os.environ)
    environment["PYTHONUTF8"] = "1"
    for name, display, description, group in SKILLS:
        folder = skill_root / name
        short_description = f"Bounded {display} workflow and evidence checks"
        default_prompt = "Use $" + name + f" to run a bounded {display} check."
        if not folder.exists():
            subprocess.run([
                sys.executable, str(init), name, "--path", str(skill_root),
                "--interface", f"display_name={display}",
                "--interface", f"short_description={short_description}",
                "--interface", f"default_prompt={default_prompt}",
            ], cwd=REPO, check=True, env=environment, capture_output=True, text=True, encoding="utf-8")
        runner_name = next(key for key, value in RUNNERS.items() if value == group)
        body = f"""---
name: {name}
description: {description} Preserve failure evidence, same-owner limits, and empirical, production, privacy, accessibility, legal, cultural, Maori-authority, independent-reproduction, and Stage 20 boundaries.
---

# {display}

1. Read the frozen proposal and its source identifiers.
2. Run the family-current group with python scripts/{runner_name}.
3. Require the declared valid fixture and every rejection witness.
4. Retain failures at zero credit and record any recovery through Method Flow.
5. Report only completed, represented, open_gap, or exact_gate.

## Boundaries

Treat the output as bounded software, symbolic, synthetic, or structural evidence. Do not infer empirical confirmation, professional competence, production readiness, exhaustive security, complete privacy or accessibility, legal or cultural authority, Maori authority, independent reproduction, consciousness or personhood, a Theory of Everything, or Stage 20 readiness.
"""
        write_text(folder / "SKILL.md", body)
        subprocess.run([
            sys.executable, str(generate), str(folder),
            "--interface", f"display_name={display}",
            "--interface", f"short_description={short_description}",
            "--interface", f"default_prompt={default_prompt}",
        ], cwd=REPO, check=True, env=environment, capture_output=True, text=True, encoding="utf-8")
        process = subprocess.run([sys.executable, str(validate), str(folder)], cwd=REPO, capture_output=True, text=True, encoding="utf-8", env=environment)
        metadata = (folder / "agents/openai.yaml").read_text(encoding="utf-8")
        token = "$" + name
        rows.append({
            "name": name,
            "group": group,
            "initialized_through_skill_creator": True,
            "quick_validate_exit": process.returncode,
            "todo_count": body.count("TODO"),
            "has_boundaries_heading": "## Boundaries" in body,
            "metadata_mentions_skill": token in metadata,
            "global_install": False,
            "valid": process.returncode == 0 and "TODO" not in body and token in metadata,
        })
    return rows


def build_runners() -> list[dict[str, object]]:
    rows = []
    for name, group in RUNNERS.items():
        target = REPO / "scripts" / name
        body = f'''#!/usr/bin/env python3
"""Family-current thin delegate for the v651-v7 {group} group."""

from __future__ import annotations

import argparse
import json

from ghc_family_v651_v7_runtime import run_group


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    result = run_group("{group}")
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))


if __name__ == "__main__":
    main()
'''
        write_text(target, body)
        output = run_group(group)
        write_json(f"tooling/runner-smoke/{target.stem}.json", output)
        rows.append({"name": name, "path": f"scripts/{name}", "group": group, "surface_count": output["surface_count"], "valid": output["valid"], "thin_delegate": True})
    return rows


def main() -> None:
    skills = build_skills()
    runners = build_runners()
    unique_surfaces = sorted({slug for group in GROUPS.values() for slug in group})
    if len(skills) != 12 or not all(row["valid"] for row in skills):
        raise RuntimeError("phase-local skill validation failed")
    if len(runners) != 10 or not all(row["valid"] for row in runners):
        raise RuntimeError("family-current runner smoke failed")
    write_json("tooling/skill-build-receipt.json", {
        "schema": "ghc.family.v651-v7.skill-build.v1",
        "skill_count": len(skills),
        "initialized": len(skills),
        "quick_validated": sum(bool(row["valid"]) for row in skills),
        "global_installs": 0,
        "skills": skills,
        "valid": True,
    })
    write_json("tooling/runner-build-receipt.json", {
        "schema": "ghc.family.v651-v7.runner-build.v1",
        "runner_count": len(runners),
        "invoked_count": len(runners),
        "unique_surface_coverage": len(unique_surfaces),
        "unified_runtime": "scripts/ghc_family_v651_v7_runtime.py",
        "independent_implementations_claimed": False,
        "runners": runners,
        "valid": True,
    })
    print(json.dumps({"skills": len(skills), "runners": len(runners), "unique_surfaces": len(unique_surfaces), "valid": True}, sort_keys=True))


if __name__ == "__main__":
    main()
