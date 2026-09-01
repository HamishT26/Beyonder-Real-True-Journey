from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sable-rook" / "v681-v6"
SKILLS = BASE / "x2" / "skills"
RECEIPT = BASE / "x2" / "skill-validation-receipts.json"

SKILL_NAMES = [
    "ghc-family-tool-catalogue-referent-split",
    "ghc-family-loan-item-key-collision",
    "ghc-family-custody-event-separator",
    "ghc-family-tool-label-verification-vacancy",
    "ghc-family-serial-mark-uncertainty",
    "ghc-family-loan-kit-completeness-hold",
    "ghc-family-condition-safety-firewall",
    "ghc-family-loan-location-minimizer",
    "ghc-family-borrower-alias-minimizer",
    "ghc-family-reservation-priority-hold",
    "ghc-family-training-competence-firewall",
    "ghc-family-maintenance-release-state-rail",
    "ghc-family-custody-transfer-authority-hold",
    "ghc-family-return-readback-disagreement",
    "ghc-family-nonerasing-damage-amendment",
    "ghc-family-tool-kit-topology",
    "ghc-family-accessible-loan-status",
    "ghc-family-loan-exception-handover",
    "ghc-family-loan-canonical-receipt",
    "ghc-family-stage20-terminal-refusal",
]


def human(name: str) -> str:
    return name.removeprefix("ghc-family-").replace("-", " ")


def short_description(name: str) -> str:
    value = f"Review synthetic {human(name)} records"
    if len(value) > 64:
        value = value[:61].rstrip() + "..."
    if len(value) < 25:
        value += " safely"
    return value


def skill_markdown(name: str) -> str:
    topic = human(name)
    return f"""---
name: {name}
description: Use when reviewing wholly synthetic tool-library-loan records for {topic} while preserving privacy, authority, evidence, and Stage 20 boundaries.
---

# {topic.title()}

Use this owner-local phase skill only on wholly synthetic, zero-row tool-library-loan correction, provenance, accessibility, and refusal fixtures.

1. Confirm the fixture is marked synthetic and contains zero real borrowers, lenders, staff, volunteers, organizations, tools, branches, loan rows, custody events, condition evidence, incidents, maintenance records, credentials, or authority acts.
2. Apply the named record distinction and its explicit falsifier.
3. Reject missing fields, lifecycle inversion, stale provenance, evidence promotion, and authority promotion.
4. Retain every failed witness at zero credit and preserve a reversible recovery path.
5. Report only `completed`, `represented`, `open_gap`, or `exact_gate` for core outcomes.

This skill is bounded software and documentation guidance. It is not tool lending, inventory, repair, safety, records, accessibility, library operations, legal, or cultural advice; professional or operational competence; affected-party approval; Maori authority; empirical GMUT evidence; independent reproduction; identity assurance; production certification; or Stage 20 authority.
"""


def openai_yaml(name: str) -> str:
    display = human(name).title()
    return f"""interface:
  display_name: "{display}"
  short_description: "{short_description(name)}"
  default_prompt: "Use ${name} to review a wholly synthetic tool-library-loan record while preserving every authority and evidence gate."
policy:
  allow_implicit_invocation: false
"""


def materialize() -> list[str]:
    paths: list[str] = []
    for name in SKILL_NAMES:
        directory = SKILLS / name
        agents = directory / "agents"
        agents.mkdir(parents=True, exist_ok=True)
        skill_path = directory / "SKILL.md"
        yaml_path = agents / "openai.yaml"
        skill_path.write_text(skill_markdown(name), encoding="utf-8", newline="\n")
        yaml_path.write_text(openai_yaml(name), encoding="utf-8", newline="\n")
        paths.extend([skill_path.relative_to(ROOT).as_posix(), yaml_path.relative_to(ROOT).as_posix()])
    return paths


def validate(validator: Path) -> None:
    if RECEIPT.exists():
        raise RuntimeError("skill validation receipt already exists; successful validation must not be replayed")
    rows = []
    for name in SKILL_NAMES:
        directory = SKILLS / name
        completed = subprocess.run(
            [sys.executable, "-X", "utf8", str(validator), str(directory)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        row = {
            "returncode": completed.returncode,
            "skill": name,
            "skill_sha256": hashlib.sha256(
                (directory / "SKILL.md").read_bytes().replace(b"\r\n", b"\n")
            ).hexdigest(),
            "stdout": completed.stdout.strip(),
            "validator_invocations": 1,
        }
        rows.append(row)
        if completed.returncode != 0:
            raise RuntimeError(json.dumps(row))
    RECEIPT.write_text(
        json.dumps(
            {
                "global_installation": False,
                "owner": "Sable Rook",
                "passed": len(rows),
                "phase": "v681-v6",
                "receipts": rows,
                "schema": "ghc.family.skill-validation.v681.v6.x2",
                "validator_replayed_after_success": False,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("materialize", "validate"))
    parser.add_argument("--validator", type=Path)
    args = parser.parse_args()
    if args.mode == "materialize":
        print(json.dumps({"paths": len(materialize()), "skills": len(SKILL_NAMES)}))
    else:
        if args.validator is None:
            raise RuntimeError("--validator is required")
        validate(args.validator)
        print(json.dumps({"passed": len(SKILL_NAMES), "receipt": RECEIPT.relative_to(ROOT).as_posix()}))


if __name__ == "__main__":
    main()
