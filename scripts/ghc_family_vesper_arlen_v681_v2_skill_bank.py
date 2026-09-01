from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "vesper-arlen" / "v681-v2"
SKILLS = BASE / "x2" / "skills"
RECEIPT = BASE / "x2" / "skill-validation-receipts.json"

SLUGS = [
    "hydrometer-physical-record-boundary",
    "scale-family-discriminator",
    "reference-temperature-vacancy",
    "meniscus-convention-guard",
    "correction-sign-classifier",
    "uncertainty-component-ledger",
    "coverage-confidence-firewall",
    "covariance-psd-guard",
    "density-unit-refusal",
    "certificate-revision-lineage",
    "traceability-nonclaim",
    "environmental-field-vacancy",
    "sample-identity-minimizer",
    "status-hold-board",
    "extrapolation-refusal",
    "certificate-collision-recovery",
    "accessible-table-structure",
    "canonical-receipt-domain",
    "provenance-role-separation",
    "stage20-terminal-refusal",
]


def skill_name(slug: str) -> str:
    return f"vesper-{slug}"


def skill_markdown(slug: str) -> str:
    name = skill_name(slug)
    human = slug.replace("-", " ")
    return f"""---
name: {name}
description: Use when reviewing wholly synthetic hydrometer records for {human}; preserve every professional, empirical, identity, legal, cultural, Maori-authority, and Stage 20 gate.
---

# {human.title()}

Use this owner-local phase skill only on wholly synthetic, zero-row hydrometer calibration-certificate and density-record fixtures.

1. Confirm the fixture is marked synthetic and contains zero real rows, people, instruments, samples, laboratories, measurements, certificates, credentials, or authority acts.
2. Apply the named record distinction and its explicit falsifier.
3. Reject missing fields, lifecycle inversion, stale provenance, evidence promotion, and authority promotion.
4. Retain every failed witness at zero credit and preserve a reversible recovery path.
5. Report only `completed`, `represented`, `open_gap`, or `exact_gate` for core outcomes.

This skill is bounded software and documentation guidance. It is not calibration advice, laboratory competence, conformity assessment, accreditation, legal interpretation, cultural ratification, Maori authority, empirical GMUT evidence, independent reproduction, identity assurance, production certification, or Stage 20 authority.
"""


def openai_yaml(slug: str) -> str:
    name = skill_name(slug)
    display = slug.replace("-", " ").title()
    short = f"Synthetic {slug.replace('-', ' ')} guard"
    if len(short) > 64:
        short = short[:61].rstrip() + "..."
    return f"""interface:
  display_name: "{display}"
  short_description: "{short}"
  default_prompt: "Use ${name} to review a wholly synthetic hydrometer record while preserving every authority gate."
policy:
  allow_implicit_invocation: false
"""


def materialize() -> list[str]:
    paths: list[str] = []
    for slug in SLUGS:
        directory = SKILLS / skill_name(slug)
        agents = directory / "agents"
        agents.mkdir(parents=True, exist_ok=True)
        skill_path = directory / "SKILL.md"
        yaml_path = agents / "openai.yaml"
        skill_path.write_text(skill_markdown(slug), encoding="utf-8", newline="\n")
        yaml_path.write_text(openai_yaml(slug), encoding="utf-8", newline="\n")
        paths.extend([skill_path.relative_to(ROOT).as_posix(), yaml_path.relative_to(ROOT).as_posix()])
    return paths


def validate(validator: Path) -> None:
    if RECEIPT.exists():
        raise RuntimeError("skill validation receipt already exists; successful validation must not be replayed")
    rows = []
    for slug in SLUGS:
        directory = SKILLS / skill_name(slug)
        completed = subprocess.run(
            [sys.executable, "-X", "utf8", str(validator), str(directory)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        row = {
            "returncode": completed.returncode,
            "skill": skill_name(slug),
            "skill_sha256": hashlib.sha256((directory / "SKILL.md").read_bytes().replace(b"\r\n", b"\n")).hexdigest(),
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
                "owner": "Vesper Arlen",
                "passed": len(rows),
                "phase": "v681-v2",
                "receipts": rows,
                "schema": "ghc.family.skill-validation.v681.v2.x2",
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
        print(json.dumps({"paths": len(materialize()), "skills": len(SLUGS)}))
    else:
        if args.validator is None:
            raise RuntimeError("--validator is required")
        validate(args.validator)
        print(json.dumps({"passed": len(SLUGS), "receipt": RECEIPT.relative_to(ROOT).as_posix()}))


if __name__ == "__main__":
    main()
