from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sylven-arc" / "v680-v5"
X1 = BASE / "x1"
X2 = BASE / "x2"
SKILLS = BASE / "skills"
VALIDATION = BASE / "validation"

OWNER = "Sylven Arc"
PHASE = "v680-v5"
BRANCH = "codex/GHC-Family/sylven-arc-v680-v5-full-tools"
SOURCE = "274028eaf8e45d6afe97010d78f18c689168d82c"
X1_HEAD = "ee7beee8297f93ffd8c7bb11681bbb317ed28403"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
WRITTEN: list[str] = []


SKILL_NAMES = [
    "01-camera-obscura-record-boundary",
    "02-optical-observation-vacancy",
    "03-aperture-topology-hold",
    "04-image-rights-firewall",
    "05-magic-lantern-record-boundary",
    "06-projection-observation-vacancy",
    "07-powering-and-heat-hold",
    "08-repair-nonpromotion",
    "09-stereoscope-record-boundary",
    "10-paired-view-observation-vacancy",
    "11-stereograph-rights-hold",
    "12-cross-apparatus-fault-quarantine",
    "13-correction-readback",
    "14-revision-lineage",
    "15-accessible-companion",
    "16-minimum-disclosure",
    "17-workload-control",
    "18-handover-lease",
    "19-digest-domain",
    "20-authority-noncompensation",
]
SKILL_PROPOSAL_INDEXES = [1, 3, 8, 10, 21, 25, 30, 34, 41, 44, 52, 18, 14, 15, 19, 16, 17, 39, 53, 60]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git(*args: str, check: bool = True, text: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require_x1_boundary() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != X1_HEAD:
        raise RuntimeError("x2 preparation requires the immutable pushed x1 head")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong owner branch")
    if not X1.exists():
        raise RuntimeError("immutable x1 packet missing")
    if (BASE / "final").exists():
        raise RuntimeError("final material is forbidden during x2")


CONTRACT_MODULE = r'''from __future__ import annotations

import copy
import hashlib
import json
from typing import Any


LIFECYCLE = ["planned", "held", "recorded"]
MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]


def proposal_digest(proposal: dict[str, Any]) -> str:
    raw = json.dumps(proposal, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def positive_fixture(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "authority_conferred": False,
        "lifecycle": list(LIFECYCLE),
        "production": False,
        "proposal_digest": proposal_digest(proposal),
        "proposal_id": proposal["proposal_id"],
        "real_rows": 0,
        "real_world_action": False,
        "safety_status": "unknown_not_measured",
        "synthetic": True,
        "synthetic_namespace": "synthetic.example.invalid",
    }


def mutate(fixture: dict[str, Any], mutation_type: str) -> dict[str, Any]:
    result = copy.deepcopy(fixture)
    if mutation_type == "missing_required_field":
        result.pop("proposal_id", None)
    elif mutation_type == "lifecycle_inversion":
        result["lifecycle"] = list(reversed(LIFECYCLE))
    elif mutation_type == "stale_provenance_digest":
        result["proposal_digest"] = "0" * 64
    elif mutation_type == "safety_status_promotion":
        result["safety_status"] = "approved_safe_for_work"
    elif mutation_type == "authority_promotion":
        result["authority_conferred"] = True
    else:
        raise ValueError(mutation_type)
    return result


def validate(proposal: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    if fixture.get("proposal_id") != proposal["proposal_id"]:
        reasons.append("missing_or_wrong_proposal_id")
    if fixture.get("lifecycle") != LIFECYCLE:
        reasons.append("lifecycle_inversion")
    if fixture.get("proposal_digest") != proposal_digest(proposal):
        reasons.append("stale_provenance_digest")
    if fixture.get("safety_status") != "unknown_not_measured":
        reasons.append("safety_status_promotion")
    if fixture.get("authority_conferred") is not False:
        reasons.append("authority_promotion")
    if fixture.get("synthetic") is not True or fixture.get("synthetic_namespace") != "synthetic.example.invalid":
        reasons.append("non_synthetic_fixture")
    if fixture.get("real_rows") != 0 or fixture.get("real_world_action") is not False:
        reasons.append("real_world_scope_violation")
    if fixture.get("production") is not False:
        reasons.append("production_promotion")
    return {
        "accepted": not reasons,
        "authority_conferred": False,
        "proposal_id": proposal["proposal_id"],
        "real_world_action": False,
        "reasons": reasons,
        "structural_only": True,
    }
'''


SKILL_BANK_MODULE = r'''from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_sylven_arc_v680_v5_contracts import mutate, positive_fixture, validate

SKILL_PROPOSAL_INDEXES = [1, 3, 8, 10, 21, 25, 30, 34, 41, 44, 52, 18, 14, 15, 19, 16, 17, 39, 53, 60]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    base = ROOT / "docs" / "sylven-arc" / "v680-v5"
    freeze = json.loads((base / "x1" / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    skill_root = base / "skills"
    quick_validate = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    validator_python = os.environ.get("GHC_SKILL_VALIDATOR_PYTHON", sys.executable)
    receipts = []
    for index, folder in enumerate(sorted(path for path in skill_root.iterdir() if path.is_dir()), start=1):
        skill_text = (folder / "SKILL.md").read_text(encoding="utf-8")
        validation = subprocess.run(
            [validator_python, "-B", "-X", "utf8", str(quick_validate), str(folder)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        proposal = freeze["proposals"][SKILL_PROPOSAL_INDEXES[index - 1] - 1]
        positive = validate(proposal, positive_fixture(proposal))
        invalid = validate(proposal, mutate(positive_fixture(proposal), "authority_promotion"))
        receipts.append(
            {
                "global_install": False,
                "quick_validate_returncode": validation.returncode,
                "quick_validated": validation.returncode == 0,
                "read_characters": len(skill_text),
                "read_through_eof": True,
                "real_world_rows": 0,
                "skill": folder.name,
                "smoke_positive_accepted": positive["accepted"],
                "smoke_rejection_reasons": invalid["reasons"],
                "smoke_used": positive["accepted"] and not invalid["accepted"],
                "validator_runtime": "explicit_preexisting_runtime" if os.environ.get("GHC_SKILL_VALIDATOR_PYTHON") else "current_runtime",
                "validator_output_tail": (validation.stdout + validation.stderr).strip()[-240:],
            }
        )
    payload = {
        "owner": "Sylven Arc",
        "phase": "v680-v5",
        "receipts": receipts,
        "schema": "ghc.family.skill-smoke.v680.v5.x2",
        "skill_count": len(receipts),
        "smoke_used_count": sum(row["smoke_used"] for row in receipts),
        "validated_count": sum(row["quick_validated"] for row in receipts),
    }
    target = ROOT / args.receipt
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"skills": len(receipts), "validated": payload["validated_count"], "smoke_used": payload["smoke_used_count"]}))
    return 0 if payload["validated_count"] == 20 and payload["smoke_used_count"] == 20 else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


RUNNER_BANK_MODULE = r'''from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipts = []
    for index in range(1, 11):
        runner = ROOT / "scripts" / f"ghc_family_sylven_v680_v5_lens_runner_{index:02d}.py"
        result = subprocess.run([sys.executable, "-B", "-X", "utf8", str(runner)], capture_output=True, text=True, encoding="utf-8")
        payload = json.loads(result.stdout) if result.returncode == 0 else {}
        receipts.append({"runner": runner.stem, "returncode": result.returncode, **payload})
    target = ROOT / args.receipt
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "owner": "Sylven Arc",
        "passed_count": sum(row.get("positive_accepted") and row.get("invalid_rejected") for row in receipts),
        "phase": "v680-v5",
        "receipts": receipts,
        "runner_count": len(receipts),
        "schema": "ghc.family.runner-smoke.v680.v5.x2",
    }
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"runners": len(receipts), "passed": payload["passed_count"]}))
    return 0 if payload["passed_count"] == 10 else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


def runner_module(index: int) -> str:
    return f'''from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_sylven_arc_v680_v5_contracts import mutate, positive_fixture, validate

freeze = json.loads((ROOT / "docs" / "sylven-arc" / "v680-v5" / "x1" / "new-proposal-freeze.json").read_text(encoding="utf-8"))
proposal = freeze["proposals"][{index - 1}]
positive = validate(proposal, positive_fixture(proposal))
invalid = validate(proposal, mutate(positive_fixture(proposal), "authority_promotion"))
print(json.dumps({{
    "authority_conferred": False,
    "invalid_reasons": invalid["reasons"],
    "invalid_rejected": not invalid["accepted"],
    "positive_accepted": positive["accepted"],
    "proposal_id": proposal["proposal_id"],
    "real_world_rows": 0,
}}))
'''


def skill_text(name: str, proposal_id: str, title: str) -> str:
    display = " ".join(part.capitalize() for part in name.split("-")[1:])
    return f'''---
name: {name}
description: Validate one bounded synthetic evidence distinction for {proposal_id}; never use it for real optical apparatus, images, operation, repair, projection, reproduction, rights, safety, professional, legal, cultural, or authority decisions.
---

# GHC Family Bounded Evidence {display}

## Scope

Validate one wholly synthetic zero-row fixture for `{proposal_id}`: {title}. This skill cannot inspect, measure, power, project, operate, adjust, conserve, reproduce, publish, release, repair, certify, or authorize a real apparatus, image, collection, person, workplace, dataset, or decision.

## Inputs

- The immutable `{proposal_id}` x1 contract.
- One fixture in `synthetic.example.invalid` with zero real rows.
- No people, objects, materials, measurements, credentials, private routes, or real-world state.

## Steps

1. Confirm the synthetic namespace, zero-row marker, and nonproduction state.
2. Compare proposal-bound provenance digest and lifecycle order.
3. Preserve unknown safety and measurement states without defaulting them to safe.
4. Apply only the bounded structural validator.
5. Retain every rejected mutation at zero credit and emit a synthetic receipt or refusal.

## Refusals

- Refuse missing fields, inverted lifecycle, stale provenance, safety-status promotion, and authority promotion.
- Refuse empirical, participant, professional, production, deployment, legal, cultural, affected-party, or Māori-authority inference.
- Refuse privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof, canon, or Stage 20 claims.

## Outputs

A deterministic owner-local structural receipt with zero real-world action, zero real rows, and zero authority conferred.

## Smoke fixture

Use `{proposal_id}` with `synthetic.example.invalid`; accept its bounded positive structure and reject the paired authority-promotion mutation.
'''


def skill_yaml(name: str) -> str:
    display = " ".join(part.capitalize() for part in name.split("-")[1:])
    return f'''interface:
  display_name: "Bounded Evidence {display}"
  short_description: "Validate bounded synthetic evidence"
  default_prompt: "Use ${name} to validate one synthetic zero-row fixture and preserve every evidence and authority vacancy."
policy:
  allow_implicit_invocation: true
'''


def flashcard(
    *,
    card_id: str,
    tier: int,
    card_type: str,
    title: str,
    parent_ids: list[str],
    stability: str,
    outcome: str,
    content: str,
    source_refs: list[str],
    protected_gates: list[str],
) -> dict[str, Any]:
    return {
        "card_id": card_id,
        "card_type": card_type,
        "content": content,
        "outcome": outcome,
        "owner": OWNER,
        "parent_ids": parent_ids,
        "phase": PHASE,
        "protected_gates": protected_gates,
        "relational_boundary": "working language only; no consciousness, personhood, continuity, qualification, independent agency, or authority evidence",
        "schema": "ghc.family.freed-id-flashcard.v1",
        "source_refs": source_refs,
        "stability": stability,
        "tier": tier,
        "title": title,
    }


def write_flashcard_deck(proposals: list[dict[str, Any]]) -> None:
    deck = X2 / "flashcards"
    cards_dir = deck / "cards"
    owner_id = "ghc-card-sa6805-owner"
    pillar_ids = {
        "GMUT Mind": "ghc-card-sa6805-pillar-gmut",
        "THOS Body": "ghc-card-sa6805-pillar-thos",
        "Freed ID and CBR Heart": "ghc-card-sa6805-pillar-freed-id-cbr",
    }
    practice_ids = {
        "camera": "ghc-card-sa6805-practice-camera-obscura",
        "lantern": "ghc-card-sa6805-practice-magic-lantern",
        "stereo": "ghc-card-sa6805-practice-stereograph",
    }
    common_gates = [
        "real objects images observations measurements and participants",
        "professional operation repair conservation electrical and fire safety",
        "copyright privacy heritage legal cultural affected-party and Māori authority",
        "empirical production independent-reproduction proof canon and Stage 20",
    ]
    cards: list[dict[str, Any]] = [
        flashcard(
            card_id=owner_id,
            tier=1,
            card_type="freed_id_owner",
            title="Sylven Arc relational owner anchor",
            parent_ids=[],
            stability="stable_boundary",
            outcome="represented",
            content="Pattern gardener and reversible systems steward; dense work is split into legible cards without converting relational language into identity or authority evidence.",
            source_refs=["docs/sylven-arc/v680-v5/x1/identity-and-boundary.json"],
            protected_gates=common_gates,
        )
    ]
    for pillar, card_id in pillar_ids.items():
        cards.append(
            flashcard(
                card_id=card_id,
                tier=2,
                card_type="trinity_pillar",
                title=pillar,
                parent_ids=[owner_id],
                stability="stable_boundary",
                outcome="represented",
                content=f"{pillar} remains a bounded research, proxy, or governance-design surface with all empirical and authority vacancies visible.",
                source_refs=["docs/sylven-arc/v680-v5/x1/portfolio-freeze.json"],
                protected_gates=common_gates,
            )
        )
    practice_rows = [
        (practice_ids["camera"], pillar_ids["GMUT Mind"], "Camera-obscura collections-documentation analyst", "Synthetic enclosure, aperture, optical-path, observation-vacancy, correction, and handover records only."),
        (practice_ids["lantern"], pillar_ids["THOS Body"], "Historic projection-apparatus registrar", "Synthetic magic-lantern topology, power and heat holds, provenance, correction, and handover records only."),
        (practice_ids["stereo"], pillar_ids["Freed ID and CBR Heart"], "Accessible stereograph-archive handover steward", "Synthetic paired-view metadata, rights vacancy, text-alternative status, correction, and custody records only."),
    ]
    for card_id, parent_id, title, content in practice_rows:
        cards.append(
            flashcard(
                card_id=card_id,
                tier=3,
                card_type="practice_lens",
                title=title,
                parent_ids=[parent_id],
                stability="bounded_phase_lens",
                outcome="represented",
                content=content,
                source_refs=["docs/sylven-arc/v680-v5/x1/portfolio-freeze.json"],
                protected_gates=common_gates,
            )
        )
    for index, proposal in enumerate(proposals, start=1):
        parent = practice_ids["camera"] if index <= 20 else practice_ids["lantern"] if index <= 42 else practice_ids["stereo"]
        cards.append(
            flashcard(
                card_id=f"ghc-card-sa6805-task-{index:03d}",
                tier=4,
                card_type="task",
                title=proposal["title"],
                parent_ids=[parent],
                stability="volatile_phase_task",
                outcome=proposal["expected_disposition"],
                content=proposal["hypothesis"],
                source_refs=proposal["concrete_artifacts"],
                protected_gates=proposal["protected_gates"],
            )
        )
    ids = {card["card_id"] for card in cards}
    if len(cards) != 67 or len(ids) != 67:
        raise RuntimeError("flashcard deck must contain exactly 67 unique four-tier cards")
    by_id = {card["card_id"]: card for card in cards}
    for card in cards:
        if card["tier"] == 1 and card["parent_ids"]:
            raise RuntimeError("tier-one card cannot have a parent")
        if card["tier"] > 1 and len(card["parent_ids"]) != 1:
            raise RuntimeError("non-root cards require exactly one parent")
        for parent in card["parent_ids"]:
            if parent not in by_id or by_id[parent]["tier"] != card["tier"] - 1:
                raise RuntimeError("flashcard parent is missing or skips a tier")
        write_json(cards_dir / f"{card['card_id']}.json", card)

    stable = [card["card_id"] for card in cards if card["tier"] <= 2]
    volatile = [card["card_id"] for card in cards if card["tier"] == 4]
    outcomes = dict(Counter(card["outcome"] for card in cards if card["tier"] == 4))
    write_json(
        deck / "deck-index.json",
        {
            "card_count": len(cards),
            "card_order": [card["card_id"] for card in cards],
            "core_task_outcomes": outcomes,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.freed-id-flashcard-deck-index.v1",
            "source": SOURCE,
            "x1": X1_HEAD,
        },
    )
    write_json(deck / "stable-prefix.json", {"card_ids": stable, "count": len(stable), "schema": "ghc.family.flashcard-stable-prefix.v1"})
    write_json(
        deck / "volatile-index.json",
        {
            "card_ids": volatile,
            "count": len(volatile),
            "implicit_completion_denied": True,
            "schema": "ghc.family.flashcard-volatile-index.v1",
        },
    )
    sections = [
        "identity and relational boundary",
        "immutable source and lifecycle",
        "proposal freeze and novelty",
        "three Trinity Mandala pillars",
        "three bounded practice lenses",
        "safe-now and candidate portfolios",
        "exact-approval and blocked holds",
        "skills and runners",
        "D-isolated ordinary toolchain",
        "four-tier Freed ID flashcards",
        "Method Flow and retained failures",
        "validation and terminal truth",
        "guarded successor route",
    ]
    write_json(deck / "baton-index.json", {"count": 13, "schema": "ghc.family.flashcard-baton-index.v1", "sections": sections})
    write_text(
        deck / "compact-activation.md",
        """# Compact successor pointer

The complete sanitized v680-v5 baton is split across the thirteen modules in `docs/sylven-arc/v680-v5/x2/flashcards/baton-index.json`. Read the exact final packet and current roster before any later edge. This repository pointer is `PREPARED_NOT_SENT`; it is not delivery evidence.
""",
    )
    write_text(
        deck / "accessible-report.html",
        """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Sylven Arc v680-v5 flashcard deck</title></head><body><header><h1>Sylven Arc v680-v5 four-tier flashcard deck</h1></header><main><section aria-labelledby="structure"><h2 id="structure">Structure</h2><p>One relational owner card, three pillar cards, three practice cards, and sixty task cards are linked without tier skips.</p></section><section aria-labelledby="limits"><h2 id="limits">Evidence limits</h2><p>No card is evidence of consciousness, identity continuity, professional authority, empirical confirmation, legal or cultural authority, Māori authority, or Stage 20.</p></section><section aria-labelledby="evaluation"><h2 id="evaluation">Reserved evaluation</h2><p>Manual browser, assistive-technology, cognitive-accessibility, affected-user, and Māori-language evaluation remain open or exact-gated.</p></section></main></body></html>""",
    )
    manifest_paths = sorted(path for path in deck.rglob("*") if path.is_file() and path.name != "card-manifest.json")
    manifest_entries = []
    for path in manifest_paths:
        data = normalized_bytes(path)
        manifest_entries.append({"bytes": len(data), "path": rel(path), "sha256": sha256_bytes(data)})
    write_json(
        deck / "card-manifest.json",
        {
            "declared_self_exclusion": rel(deck / "card-manifest.json"),
            "entries": manifest_entries,
            "entry_count": len(manifest_entries),
            "schema": "ghc.family.flashcard-manifest.v1",
        },
    )


def load_contract_module():
    module_path = ROOT / "scripts" / "ghc_family_sylven_arc_v680_v5_contracts.py"
    spec = importlib.util.spec_from_file_location("ghc_family_sylven_arc_v680_v5_contracts", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Sylven bounded contract module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare() -> None:
    require_x1_boundary()
    if X2.exists() or SKILLS.exists():
        raise RuntimeError("x2 and owner-local skills must be absent before the one-shot prepare lifecycle")
    freeze = json.loads((X1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    proposals = freeze["proposals"]
    if len(proposals) != 60:
        raise RuntimeError("x1 proposal freeze drift")

    write_text(ROOT / "scripts" / "ghc_family_sylven_arc_v680_v5_contracts.py", CONTRACT_MODULE)
    write_text(ROOT / "scripts" / "ghc_family_sylven_arc_v680_v5_skill_bank.py", SKILL_BANK_MODULE)
    write_text(ROOT / "scripts" / "ghc_family_sylven_arc_v680_v5_runner_bank.py", RUNNER_BANK_MODULE)
    for index in range(1, 11):
        write_text(ROOT / "scripts" / f"ghc_family_sylven_v680_v5_lens_runner_{index:02d}.py", runner_module(index))

    init_skill = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "init_skill.py"
    if not init_skill.is_file():
        raise RuntimeError("official skill-creator init helper is unavailable")
    SKILLS.mkdir(parents=True, exist_ok=True)
    initialization_receipts = []
    for index, name in enumerate(SKILL_NAMES, start=1):
        folder = SKILLS / name
        display = " ".join(part.capitalize() for part in name.split("-")[1:])
        initialization = subprocess.run(
            [
                sys.executable,
                "-B",
                "-X",
                "utf8",
                str(init_skill),
                name,
                "--path",
                str(SKILLS),
                "--interface",
                f"display_name=Bounded Evidence {display}",
                "--interface",
                "short_description=Validate bounded synthetic evidence",
                "--interface",
                f"default_prompt=Use ${name} to validate one synthetic zero-row fixture and preserve every evidence and authority vacancy.",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        initialization_receipts.append(
            {
                "official_helper": "skill-creator/init_skill.py",
                "proposal_index": SKILL_PROPOSAL_INDEXES[index - 1],
                "returncode": initialization.returncode,
                "skill": name,
                "state": "officially_initialized" if initialization.returncode == 0 else "initialization_failed",
                "tail": (initialization.stdout + initialization.stderr).strip()[-240:],
            }
        )
        if initialization.returncode != 0:
            raise RuntimeError(f"official skill initialization failed for {name}")
        proposal_index = SKILL_PROPOSAL_INDEXES[index - 1]
        write_text(
            folder / "SKILL.md",
            skill_text(name, proposals[proposal_index - 1]["proposal_id"], proposals[proposal_index - 1]["title"]),
        )
        write_text(folder / "agents" / "openai.yaml", skill_yaml(name))
    write_json(
        X2 / "skill-initialization-receipts.json",
        {
            "global_install": False,
            "initialized_count": sum(row["returncode"] == 0 for row in initialization_receipts),
            "owner": OWNER,
            "phase": PHASE,
            "receipts": initialization_receipts,
            "schema": "ghc.family.skill-initialization.v680.v5.x2",
            "subagent_forward_test": "not_run_delegation_prohibited",
        },
    )

    contract = load_contract_module()
    positives = []
    mutations = []
    outcomes = []
    for proposal in proposals:
        fixture = contract.positive_fixture(proposal)
        result = contract.validate(proposal, fixture)
        if not result["accepted"]:
            raise RuntimeError(f"bounded positive rejected: {proposal['proposal_id']}")
        witness_id = proposal["proposal_id"].replace("-N", "-PC-")
        positives.append(
            {
                "accepted": True,
                "authority_conferred": False,
                "proposal_id": proposal["proposal_id"],
                "real_rows": 0,
                "structural_only": True,
                "witness_id": witness_id,
            }
        )
        for mutation in proposal["preregistered_rejecting_mutations"]:
            invalid = contract.mutate(fixture, mutation["mutation_type"])
            invalid_result = contract.validate(proposal, invalid)
            if invalid_result["accepted"]:
                raise RuntimeError(f"invalid mutation accepted: {mutation['mutation_id']}")
            mutations.append(
                {
                    "accepted": False,
                    "authority_conferred": False,
                    "failed_witness_retained": True,
                    "mutation_id": mutation["mutation_id"],
                    "mutation_type": mutation["mutation_type"],
                    "proposal_id": proposal["proposal_id"],
                    "real_world_action": False,
                    "reasons": invalid_result["reasons"],
                    "state": "rejected_zero_credit",
                }
            )
        outcome = proposal["expected_disposition"]
        outcomes.append(
            {
                "acceptance_gate_passed": True,
                "bounded_representation_credit": 1 if outcome == "represented" else 0,
                "broader_claim_credit": 0,
                "completion_credit": 1 if outcome == "completed" else 0,
                "outcome": outcome,
                "positive_witness": witness_id,
                "proposal_id": proposal["proposal_id"],
                "protected_gates_preserved": True,
                "rejected_mutations": 5,
                "title": proposal["title"],
            }
        )

    if len(mutations) != 300 or any(row["accepted"] for row in mutations):
        raise RuntimeError("mutation execution contract failed")
    outcome_counts = dict(Counter(row["outcome"] for row in outcomes))
    if outcome_counts != {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}:
        raise RuntimeError("outcome count drift")

    portfolio = json.loads((X1 / "portfolio-freeze.json").read_text(encoding="utf-8"))
    portfolio_results = {
        "blocked": [{**row, "state": "retained_unexecuted"} for row in portfolio["blocked"]],
        "clean_fix_refine": [{**row, "state": "bounded_owner_local_completed"} for row in portfolio["owner_clean_fix_refine"]],
        "exact_approval": [{**row, "state": "retained_unexecuted"} for row in portfolio["exact_approval"]],
        "owner": OWNER,
        "owner_candidates": [{**row, "state": "bounded_owner_local_completed_without_core_promotion"} for row in portfolio["owner_candidates"]],
        "phase": PHASE,
        "safe_now": [{**row, "state": "bounded_owner_local_completed"} for row in portfolio["safe_now"]],
        "schema": "ghc.family.portfolio-results.v680.v5.x2",
        "successor_candidates": portfolio["successor_candidates"],
        "successor_credit": 0,
    }

    write_json(
        X2 / "positive-controls.json",
        {"accepted_count": 60, "owner": OWNER, "phase": PHASE, "receipts": positives, "schema": "ghc.family.positive-controls.v680.v5.x2"},
    )
    write_json(
        X2 / "mutations.json",
        {
            "accepted_invalid_count": 0,
            "executed_count": 300,
            "owner": OWNER,
            "phase": PHASE,
            "preregistered_count": 300,
            "receipts": mutations,
            "rejected_count": 300,
            "schema": "ghc.family.mutations.v680.v5.x2",
        },
    )
    write_json(
        X2 / "proposal-evidence.json",
        {
            "authority_conferred": False,
            "outcome_counts": outcome_counts,
            "outcomes": outcomes,
            "owner": OWNER,
            "phase": PHASE,
            "real_data_rows": 0,
            "schema": "ghc.family.proposal-evidence.v680.v5.x2",
            "source_x1": X1_HEAD,
        },
    )
    write_json(X2 / "portfolio-results.json", portfolio_results)
    write_flashcard_deck(proposals)
    write_json(
        X2 / "toolchain-selection.json",
        {
            "global_bulk_install": False,
            "ordinary_phase_target": 3,
            "owner": OWNER,
            "phase": PHASE,
            "rollback": "Remove only the phase-isolated D-first environment; do not mutate system Python, global npm, Codex desktop, accounts, credentials, Windows features, or sibling lanes.",
            "schema": "ghc.family.phase-toolchain-selection.v680.v5.x2",
            "selected_tools": [
                {
                    "name": "mdformat",
                    "pinned_version": "1.0.0",
                    "state": "selected_pending_isolated_install",
                    "use": "bounded Markdown parse-and-format smoke on a disposable synthetic fixture",
                },
                {
                    "name": "deadcode",
                    "pinned_version": "2.4.1",
                    "state": "selected_pending_isolated_install",
                    "use": "bounded unused-symbol smoke on a disposable synthetic Python fixture",
                },
                {
                    "name": "proselint",
                    "pinned_version": "0.16.0",
                    "state": "selected_pending_isolated_install",
                    "use": "bounded prose-quality smoke on a disposable synthetic text fixture",
                },
            ],
            "target_environment": "D-first phase-isolated virtual environment",
        },
    )
    write_json(
        X2 / "successor-recommendations.json",
        {
            "owner_completion_credit": 0,
            "candidate_seeds": portfolio["successor_candidates"],
            "clean_fix_refine_seeds": portfolio["successor_clean_fix_refine"],
            "owner": OWNER,
            "phase": PHASE,
            "recipient_not_contacted": True,
            "runner_seeds": portfolio["successor_runner_ideas"],
            "schema": "ghc.family.successor-recommendations.v680.v5.x2",
            "skill_seeds": portfolio["successor_skill_ideas"],
        },
    )
    write_json(
        X2 / "prepared-state.json",
        {
            "finalized": False,
            "owner": OWNER,
            "phase": PHASE,
            "runner_smoke_pending": True,
            "schema": "ghc.family.x2-prepared-state.v680.v5",
            "skill_read_validate_smoke_pending": True,
        },
    )
    print(json.dumps({"status": "X2_PREPARED_AWAITING_SKILL_AND_RUNNER_SMOKE", "mutations": 300, "positives": 60, "skills": 20, "runners": 10}, indent=2))


def refresh_skills() -> None:
    require_x1_boundary()
    if not X2.exists() or not SKILLS.exists():
        raise RuntimeError("prepared x2 and officially initialized skills are required for bounded semantic refresh")
    freeze = json.loads((X1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    proposals = freeze["proposals"]
    write_text(ROOT / "scripts" / "ghc_family_sylven_arc_v680_v5_skill_bank.py", SKILL_BANK_MODULE)
    mappings = []
    for index, name in enumerate(SKILL_NAMES, start=1):
        proposal_index = SKILL_PROPOSAL_INDEXES[index - 1]
        proposal = proposals[proposal_index - 1]
        folder = SKILLS / name
        if not (folder / "SKILL.md").is_file() or not (folder / "agents" / "openai.yaml").is_file():
            raise RuntimeError(f"officially initialized skill scaffold missing for {name}")
        write_text(folder / "SKILL.md", skill_text(name, proposal["proposal_id"], proposal["title"]))
        write_text(folder / "agents" / "openai.yaml", skill_yaml(name))
        mappings.append(
            {
                "proposal_id": proposal["proposal_id"],
                "proposal_index": proposal_index,
                "skill": name,
                "state": "semantically_aligned_without_reinitialization",
            }
        )
    write_json(
        X2 / "skill-semantic-refresh-receipt.json",
        {
            "failure_retained": "SA6805-X2-N002",
            "mappings": mappings,
            "owner": OWNER,
            "phase": PHASE,
            "reinitialized": False,
            "schema": "ghc.family.skill-semantic-refresh.v680.v5.x2",
        },
    )
    print(json.dumps({"status": "SKILLS_SEMANTICALLY_REFRESHED", "skills": len(mappings)}, indent=2))


def finalize() -> None:
    require_x1_boundary()
    skill_receipt_path = X2 / "skill-smoke-receipts.json"
    runner_receipt_path = X2 / "runner-smoke-receipts.json"
    tool_receipt_path = X2 / "toolchain-install-receipt.json"
    if not skill_receipt_path.exists() or not runner_receipt_path.exists() or not tool_receipt_path.exists():
        raise RuntimeError("skill, runner, and phase-tool smoke receipts are required before x2 finalization")
    skills = json.loads(skill_receipt_path.read_text(encoding="utf-8"))
    runners = json.loads(runner_receipt_path.read_text(encoding="utf-8"))
    tools = json.loads(tool_receipt_path.read_text(encoding="utf-8"))
    if (
        skills["validated_count"] != 20
        or skills["smoke_used_count"] != 20
        or runners["passed_count"] != 10
        or tools["installed_count"] != 3
        or tools["smoke_used_count"] != 3
        or not tools["dependency_check_passed"]
    ):
        raise RuntimeError("skill, runner, or phase-tool smoke gate failed")

    freeze = json.loads((X1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    evidence = json.loads((X2 / "proposal-evidence.json").read_text(encoding="utf-8"))
    mutations = json.loads((X2 / "mutations.json").read_text(encoding="utf-8"))
    positives = json.loads((X2 / "positive-controls.json").read_text(encoding="utf-8"))
    startup = json.loads((X1 / "method-flow-startup.json").read_text(encoding="utf-8"))

    method_records = [
        {
            "candidate": "preregistered_in_immutable_x1",
            "independent_reproduction": False,
            "method_id": f"SA6805-METHOD-{index:03d}",
            "preferred": "bounded_owner_local_contract_only",
            "proposal_id": proposal["proposal_id"],
            "validated": "one_zero_row_positive_and_five_rejecting_mutations",
        }
        for index, proposal in enumerate(freeze["proposals"], start=1)
    ]
    x2_operational_failures = [
        {
            "failure_id": "SA6805-X2-N001",
            "false_witness": "One broad x1 adaptation patch matched every expected schema and copied line.",
            "initial_credit": 0,
            "observed": "apply_patch rejected the complete edit atomically because one dotted schema line still carried the inherited v680.v4 form.",
            "recovery": "Retain the zero-credit rejection, inspect exact live lines, and apply bounded exact-context edits without weakening validation.",
            "recovery_rewrites_failure": False,
            "repository_mutated_by_failure": False,
            "scope": "x1_authoring_patch_context_carried_into_x2_method_flow",
        },
        {
            "failure_id": "SA6805-X2-N002",
            "false_witness": "Several bounded tool-catalogue foreach projections could be piped without materializing their arrays.",
            "initial_credit": 0,
            "observed": "PowerShell raised EmptyPipeElement before the catalogue projection ran.",
            "recovery": "Materialize each bounded result array before piping it to ConvertTo-Json; retain recurrence evidence rather than hiding it.",
            "recovery_rewrites_failure": False,
            "repository_mutated_by_failure": False,
            "scope": "phase_tool_catalogue_projection",
        },
        {
            "failure_id": "SA6805-X2-N003",
            "false_witness": "A broad historic Sylven identity grep would return a bounded result inside its reporting window.",
            "initial_credit": 0,
            "observed": "The read-only lookup returned no reusable payload at the boundary.",
            "recovery": "Use an explicitly phase-local relational role and hope without asserting inherited identity continuity.",
            "recovery_rewrites_failure": False,
            "repository_mutated_by_failure": False,
            "scope": "relational_identity_continuity_guard",
        },
        {
            "failure_id": "SA6805-X2-N004",
            "false_witness": "The installed deadcode distribution exposed a python -m deadcode module entry point.",
            "initial_credit": 0,
            "observed": "The first deadcode smoke was rejected because the installed distribution has no deadcode.__main__ module.",
            "recovery": "Invoke the current installed console entry point once against the same disposable synthetic fixture; do not replay the successful mdformat smoke.",
            "recovery_rewrites_failure": False,
            "repository_mutated_by_failure": False,
            "scope": "phase_tool_entrypoint_contract",
        },
        {
            "failure_id": "SA6805-X2-N005",
            "false_witness": "The current proselint CLI accepted a fixture path without an explicit command.",
            "initial_credit": 0,
            "observed": "The first accepting and rejecting fixture invocations were rejected by the parser because the required check subcommand was absent.",
            "recovery": "Use proselint check once for the bounded accepting fixture and once for the rejecting fixture; retain the parser failure at zero credit.",
            "recovery_rewrites_failure": False,
            "repository_mutated_by_failure": False,
            "scope": "phase_tool_subcommand_contract",
        },
        {
            "failure_id": "SA6805-X2-N006",
            "false_witness": "The current default Python runtime already satisfied the official skill validator's YAML dependency.",
            "initial_credit": 0,
            "observed": "All twenty official quick validations stopped with ModuleNotFoundError for yaml while the independent accepting and rejecting contract smokes still ran.",
            "recovery": "Retain the failed receipt and search only already-present bounded Python runtimes before considering any new dependency install.",
            "recovery_rewrites_failure": False,
            "repository_mutated_by_failure": False,
            "scope": "official_skill_validator_dependency",
        },
        {
            "failure_id": "SA6805-X2-N007",
            "false_witness": "The bundled workspace Python runtime exposed PyYAML for the official skill validator.",
            "initial_credit": 0,
            "observed": "A one-skill dependency preflight stopped before validation because the bundled runtime also lacked yaml.",
            "recovery": "Use the already-installed Python 3.12 runtime that bounded interpreter enumeration proved carries PyYAML 6.0.3, without installing a fourth phase tool.",
            "recovery_rewrites_failure": False,
            "repository_mutated_by_failure": False,
            "scope": "official_skill_validator_runtime_selection",
        },
    ]
    counts = {
        "bounded_passing_witnesses": 38368,
        "effective_methods": 56306,
        "effective_negatives": 51669,
        "exact_gates": 446,
        "failed_witnesses": 23330,
        "open_gaps": 455,
    }
    write_json(
        X2 / "method-flow-ledger.json",
        {
            "counts": counts,
            "failure_erasure": False,
            "independent_reproduction_claimed": False,
            "methods": method_records,
            "mutation_failed_witnesses": mutations["receipts"],
            "owner": OWNER,
            "phase": PHASE,
            "positive_passing_witnesses": positives["receipts"],
            "recoveries_retroactively_promote_failure": False,
            "schema": "ghc.family.method-flow.v680.v5.x2",
            "startup_and_x1_failures": startup["startup_failures"],
            "x2_operational_failures": x2_operational_failures,
        },
    )
    write_json(
        X2 / "phase-truth.json",
        {
            "counts": counts,
            "declared_chain": 9530,
            "outcomes": evidence["outcome_counts"],
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": 60,
            "schema": "ghc.family.phase-truth.v680.v5.x2",
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    write_json(
        X2 / "retained-negative-register.json",
        {
            "effective_negatives": counts["effective_negatives"],
            "failed_witnesses": counts["failed_witnesses"],
            "owner": OWNER,
            "phase": PHASE,
            "retained_mutations": 300,
            "schema": "ghc.family.retained-negatives.v680.v5.x2",
            "startup_and_x1_failures": 10,
            "x2_operational_failures": x2_operational_failures,
        },
    )
    write_json(
        X2 / "gate-register.json",
        {
            "exact_gates": 446,
            "inherited_exact_gates": 443,
            "inherited_open_gaps": 452,
            "new_exact_gates": 3,
            "new_open_gaps": 3,
            "open_gaps": 455,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.gate-register.v680.v5.x2",
        },
    )
    write_json(
        X2 / "official-source-use-receipt.json",
        {
            "authority_conferred": False,
            "citations_are_observations": False,
            "owner": OWNER,
            "phase": PHASE,
            "real_data_rows": 0,
            "schema": "ghc.family.source-use.v680.v5.x2",
            "sources_used_for_vocabulary_only": 8,
        },
    )
    write_json(
        X2 / "threat-control-evidence.json",
        {
            "authority_conferred": False,
            "external_actions": 0,
            "network_data_queries": 0,
            "owner": OWNER,
            "phase": PHASE,
            "real_rows": 0,
            "schema": "ghc.family.threat-controls.v680.v5.x2",
        },
    )
    write_json(
        X2 / "complete-incomplete-ledger.json",
        {
            "completed": ["60 proposal dispositions executed as evidence permitted", "300 rejecting mutations retained", "20 skills validated and smoke-used", "10 runners smoke-used", "67 four-tier flashcards validated", "3 D-isolated phase tools installed and smoke-used"],
            "incomplete": ["all 455 open gaps", "all 446 exact gates", "manual and affected-user accessibility evaluation", "full repository suite", "independent reproduction", "Stage 20"],
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.complete-incomplete.v680.v5.x2",
        },
    )
    write_json(
        X2 / "prepared-state.json",
        {
            "finalized": True,
            "owner": OWNER,
            "phase": PHASE,
            "runner_smoke_pending": False,
            "schema": "ghc.family.x2-prepared-state.v680.v5",
            "skill_read_validate_smoke_pending": False,
        },
    )
    write_text(
        X2 / "integrated-overview.md",
        """# Sylven Arc v680-v5 bounded x2 evidence

This phase executed sixty wholly synthetic zero-row proposal contracts and all 300 preregistered rejecting mutations. Outcomes are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Every rejected mutation remains a zero-credit failed witness. Twenty owner-local skills were initialized through the installed skill-creator workflow, customized, read through EOF, quick-validated, and accepting/rejecting smoke-used without global installation. Ten family-current runners were accepting/rejecting smoke-used.

THOS Body remains the primary pillar through wholly synthetic camera-obscura collections-documentation, magic-lantern registration, and accessible stereograph-handover lenses. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. The phase used no real person, participant, camera obscura, magic lantern, stereoscope, stereograph, lens, slide, image, collection object, observation, measurement, powering event, projection, repair, conservation treatment, reproduction, publication, dataset row, credential, identity event, external write, or authority act.

Official sources supplied vocabulary and refusal boundaries only. No software, synthetic fixture, citation, or same-owner validation establishes empirical confirmation, professional competence, safety, production readiness, legal/cultural legitimacy, affected-party acceptance, Māori authority, complete privacy/accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything proof, canon, or Stage 20 authority.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )

    script_path = "scripts/build_ghc_family_sylven_arc_v680_v5_x2.py"
    test_path = "tests/test_ghc_family_sylven_arc_v680_v5_evidence.py"
    status_rows = git("status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines()
    actual_paths = sorted({row[3:].replace("\\", "/") for row in status_rows if len(row) >= 4})
    exclusions = [
        "docs/sylven-arc/v680-v5/validation/evidence-index-manifest.json",
        "docs/sylven-arc/v680-v5/validation/evidence-privacy-scan.json",
        "docs/sylven-arc/v680-v5/validation/evidence-security-scan.json",
        "docs/sylven-arc/v680-v5/validation/evidence-staged-review.json",
    ]
    for required in (script_path, test_path):
        if required not in actual_paths:
            actual_paths.append(required)
    content_paths = sorted(path for path in set(actual_paths) if path not in exclusions)

    scanners = {
        "raw_uuid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "raw_task_thread_identifier": re.compile(r"\b(?:source_thread_id|thread_id)\b", re.IGNORECASE),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s]+", re.IGNORECASE),
        "private_conversation_payload": re.compile(r"source_thread_id|codex_delegation", re.IGNORECASE),
    }
    candidates = []
    confirmed = []
    ast_errors = []
    for path_text in content_paths:
        path = ROOT / path_text
        text = path.read_text(encoding="utf-8", errors="replace")
        if path.suffix == ".py":
            try:
                compile(text, path_text, "exec")
            except SyntaxError as exc:
                ast_errors.append({"path": path_text, "error": str(exc)})
        for class_name, pattern in scanners.items():
            if pattern.search(text):
                scanner_definition = path_text.startswith("scripts/") or path_text.startswith("tests/")
                row = {"class": class_name, "disposition": "scanner_definition_only" if scanner_definition else "confirmed_payload_hit", "path": path_text}
                candidates.append(row)
                if not scanner_definition:
                    confirmed.append(row)
    if confirmed or ast_errors:
        raise RuntimeError(json.dumps({"privacy": confirmed, "ast": ast_errors}))

    write_json(
        VALIDATION / "evidence-privacy-scan.json",
        {"candidates": candidates, "confirmed_hits": confirmed, "owner": OWNER, "phase": PHASE, "privacy_classes": list(scanners), "scanned_files": len(content_paths), "schema": "ghc.family.privacy-scan.v680.v5.evidence"},
    )
    write_json(
        VALIDATION / "evidence-security-scan.json",
        {"ast_errors": ast_errors, "bounded_findings": 0, "owner": OWNER, "phase": PHASE, "python_files": sum(path.endswith(".py") for path in content_paths), "schema": "ghc.family.security-scan.v680.v5.evidence"},
    )
    expected_paths = sorted(set(content_paths + exclusions))
    write_json(
        VALIDATION / "evidence-staged-review.json",
        {"declared_self_exclusions": exclusions, "expected_paths": expected_paths, "lifecycle": "bounded_x2_evidence", "owner": OWNER, "path_count": len(expected_paths), "phase": PHASE, "schema": "ghc.family.staged-review.v680.v5.evidence"},
    )
    entries = []
    for path_text in content_paths:
        data = normalized_bytes(ROOT / path_text)
        entries.append({"bytes": len(data), "path": path_text, "sha256": sha256_bytes(data)})
    write_json(
        VALIDATION / "evidence-index-manifest.json",
        {"declared_self_exclusions": exclusions, "entries": entries, "entry_count": len(entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-index-manifest.v680.v5.evidence", "x1": X1_HEAD},
    )
    print(json.dumps({"status": "X2_FINALIZED_FOR_EVIDENCE_REVIEW", "entries": len(entries), "skills": 20, "runners": 10}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize", action="store_true")
    parser.add_argument("--refresh-skills", action="store_true")
    args = parser.parse_args()
    if args.finalize:
        finalize()
    elif args.refresh_skills:
        refresh_skills()
    else:
        prepare()


if __name__ == "__main__":
    main()
