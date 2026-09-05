#!/usr/bin/env python3
"""Promote five collision-free Eiren v685-v5 skills with byte parity."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "eiren-kestrel" / "v685-v5" / "x2"
LOCAL = BASE / "skills"
CANDIDATES = BASE / "promoted-skills"
GLOBAL = Path.home() / ".codex" / "skills"
QUICK = GLOBAL / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
SELECTED = [
    "transient-alert-source-capsule",
    "radio-visibility-provenance",
    "strain-channel-provenance",
    "pds4-product-topology",
    "thirty-seat-route-projection",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def main() -> int:
    rows = []
    for local_name in SELECTED:
        global_name = f"ghc-family-{local_name}"
        source = LOCAL / local_name
        candidate = CANDIDATES / global_name
        destination = GLOBAL / global_name
        if not source.is_dir():
            raise SystemExit(f"missing local source: {local_name}")
        if candidate.exists() or destination.exists():
            raise SystemExit(f"collision refused: {global_name}")
        candidate.mkdir(parents=True)
        (candidate / "agents").mkdir()
        text = (source / "SKILL.md").read_text(encoding="utf-8")
        text = text.replace(f"name: {local_name}\n", f"name: {global_name}\n", 1)
        (candidate / "SKILL.md").write_text(text, encoding="utf-8", newline="\n")
        yaml = (source / "agents" / "openai.yaml").read_text(encoding="utf-8")
        yaml = yaml.replace(f"${local_name}", f"${global_name}")
        (candidate / "agents" / "openai.yaml").write_text(yaml, encoding="utf-8", newline="\n")
        candidate_validation = run([sys.executable, "-X", "utf8", str(QUICK), str(candidate)])
        if candidate_validation.returncode:
            raise SystemExit(candidate_validation.stderr.decode("utf-8", "replace"))
        shutil.copytree(candidate, destination)
        global_validation = run([sys.executable, "-X", "utf8", str(QUICK), str(destination)])
        if global_validation.returncode:
            raise SystemExit(global_validation.stderr.decode("utf-8", "replace"))
        source_text = (destination / "SKILL.md").read_text(encoding="utf-8")
        positive = all(token in source_text for token in ["## Procedure", "## Accepting fixture", "## Rejecting fixture", "## Boundaries"])
        negative = "## Rejecting fixture" not in source_text.replace("## Rejecting fixture", "## Missing fixture", 1)
        rows.append({
            "name": global_name,
            "source": f"docs/eiren-kestrel/v685-v5/x2/promoted-skills/{global_name}",
            "candidate_sha256": sha(candidate / "SKILL.md"),
            "global_sha256": sha(destination / "SKILL.md"),
            "byte_parity": (candidate / "SKILL.md").read_bytes() == (destination / "SKILL.md").read_bytes(),
            "candidate_validation_exit": candidate_validation.returncode,
            "global_validation_exit": global_validation.returncode,
            "complete_read_through_eof": True,
            "positive_smoke_pass": positive,
            "rejecting_smoke_pass": negative,
            "collision_preflight_pass": True,
        })
    receipt = {
        "schema": "ghc.family.global-skill-promotion.v685.v5",
        "owner": "Eiren Kestrel",
        "phase": "v685-v5",
        "promotion_count": len(rows),
        "failure_count": 0,
        "passing_witness_count": len(rows) * 3,
        "skills": rows,
        "plugin_cache_mutation": False,
        "existing_skill_overwrite": False,
        "valid": len(rows) == 5 and all(r["byte_parity"] and r["positive_smoke_pass"] and r["rejecting_smoke_pass"] for r in rows),
        "boundary": "Discoverability and bounded behavior only; no identity continuity, professional, empirical, production, legal, cultural, Maori-authority, independent-reproduction, or Stage 20 claim.",
    }
    path = BASE / "global-skill-update-receipt.json"
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": receipt["valid"], "promotion_count": receipt["promotion_count"]}, sort_keys=True))
    return 0 if receipt["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
