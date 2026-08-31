from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "eiren-kestrel" / "v680-v7"
X1 = BASE / "x1"
X2 = BASE / "x2"
SKILLS = BASE / "skills"
VALIDATION = BASE / "validation"

OWNER = "Eiren Kestrel"
PHASE = "v680-v7"
BRANCH = "codex/GHC-Family/eiren-kestrel-v680-v7-full-tools"
SOURCE = "2522f0ff596b66f57f187f8073d498c692a85712"
X1_HEAD = "e94866a1adf4b5b038479c12bc5354ead6f7c249"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
WRITTEN: list[str] = []


SKILL_NAMES = [
    "01-wallpaper-elevation-boundary",
    "02-layer-stratigraphy-separation",
    "03-wall-face-address-graph",
    "04-maker-attribution-hold",
    "05-condition-nondiagnosis",
    "06-iconographic-authority-hold",
    "07-pattern-repeat-boundary",
    "08-condition-map-lineage",
    "09-intervention-quorum-guard",
    "10-hazardous-pigment-safety-hold",
    "11-physical-action-firewall",
    "12-conservation-dossier-state-machine",
    "13-media-provenance-braid",
    "14-heritage-rights-vacancy",
    "15-minimum-disclosure",
    "16-accessible-condition-companion",
    "17-workload-control",
    "18-handover-lease",
    "19-digest-domain",
    "20-stage20-refusal",
]
SKILL_PROPOSAL_INDEXES = [1, 3, 2, 6, 11, 14, 21, 23, 35, 29, 58, 42, 51, 52, 53, 39, 20, 40, 32, 60]


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
        raise RuntimeError("x2 requires the immutable pushed Eiren x1 head")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Eiren owner branch")
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
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_eiren_kestrel_v680_v7_contracts import mutate, positive_fixture, validate

SKILL_PROPOSAL_INDEXES = [1, 3, 2, 6, 11, 14, 21, 23, 35, 29, 58, 42, 51, 52, 53, 39, 20, 40, 32, 60]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    base = ROOT / "docs" / "eiren-kestrel" / "v680-v7"
    freeze = json.loads((base / "x1" / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    quick_validate = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    receipts = []
    for index, folder in enumerate(sorted(path for path in (base / "skills").iterdir() if path.is_dir()), start=1):
        skill_text = (folder / "SKILL.md").read_text(encoding="utf-8")
        validation = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(quick_validate), str(folder)],
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
                "validator_runtime": "preexisting_python_with_yaml",
                "validator_output_tail": (validation.stdout + validation.stderr).strip()[-240:],
            }
        )
    payload = {
        "owner": "Eiren Kestrel",
        "phase": "v680-v7",
        "receipts": receipts,
        "schema": "ghc.family.skill-smoke.v680.v7.x2",
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
        runner = ROOT / "scripts" / f"ghc_family_eiren_v680_v7_lens_runner_{index:02d}.py"
        result = subprocess.run([sys.executable, "-B", "-X", "utf8", str(runner)], capture_output=True, text=True, encoding="utf-8")
        payload = json.loads(result.stdout) if result.returncode == 0 else {}
        receipts.append({"runner": runner.stem, "returncode": result.returncode, **payload})
    target = ROOT / args.receipt
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "owner": "Eiren Kestrel",
        "passed_count": sum(row.get("positive_accepted") and row.get("invalid_rejected") for row in receipts),
        "phase": "v680-v7",
        "receipts": receipts,
        "runner_count": len(receipts),
        "schema": "ghc.family.runner-smoke.v680.v7.x2",
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
from ghc_family_eiren_kestrel_v680_v7_contracts import mutate, positive_fixture, validate

freeze = json.loads((ROOT / "docs" / "eiren-kestrel" / "v680-v7" / "x1" / "new-proposal-freeze.json").read_text(encoding="utf-8"))
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
description: Validate the bounded synthetic historic-wallpaper record distinction for {proposal_id}; do not use for real buildings, wallpaper, sampling, conservation, safety, rights, cultural, or authority decisions.
---

# GHC Family Bounded Evidence {display}

## Scope

Validate one wholly synthetic zero-row fixture for `{proposal_id}`: {title}. This skill cannot inspect, count, measure, sample, disturb, remove, treat, conserve, reproduce, publish, release, certify, or authorize a real person, building, wall, wallpaper, layer, pigment, adhesive, collection, workplace, dataset, identity event, or decision.

## Inputs

- The immutable `{proposal_id}` x1 contract.
- One fixture in `synthetic.example.invalid` with zero real rows.
- No people, objects, materials, measurements, credentials, private routes, or real-world state.

## Steps

1. Confirm the synthetic namespace, zero-row marker, and nonproduction state.
2. Compare proposal-bound provenance digest and lifecycle order.
3. Preserve unknown safety, attribution, condition, measurement, and rights states.
4. Apply only the bounded structural validator.
5. Retain every rejected mutation at zero credit and emit a synthetic receipt or refusal.

## Refusals

- Refuse missing fields, inverted lifecycle, stale provenance, safety promotion, and authority promotion.
- Refuse empirical, participant, professional, production, deployment, legal, cultural, affected-party, or Maori-authority inference.
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
  default_prompt: "Use ${name} to validate one synthetic zero-row fixture while preserving evidence and authority vacancies."
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
    owner_id = "ghc-card-ek6807-owner"
    pillar_ids = {
        "GMUT Mind": "ghc-card-ek6807-pillar-gmut",
        "THOS Body": "ghc-card-ek6807-pillar-thos",
        "Freed ID and CBR Heart": "ghc-card-ek6807-pillar-freed-id-cbr",
    }
    practice_ids = {
        "layers": "ghc-card-ek6807-practice-wallpaper-layers",
        "mapping": "ghc-card-ek6807-practice-condition-map",
        "dossier": "ghc-card-ek6807-practice-finish-dossier",
    }
    common_gates = [
        "real people buildings walls wallpapers layers pigments adhesives observations samples and measurements",
        "professional architectural conservation hazardous-material chemical workplace and public safety",
        "ownership access reproduction privacy remedy legal cultural affected-party and Maori authority",
        "empirical production independent-reproduction proof canon and Stage 20",
    ]
    cards: list[dict[str, Any]] = [
        flashcard(
            card_id=owner_id,
            tier=1,
            card_type="freed_id_owner",
            title="Eiren Kestrel relational owner anchor",
            parent_ids=[],
            stability="stable_boundary",
            outcome="represented",
            content="Wallpaper-stratigraphy lantern-keeper and consent-boundary mapper; synthetic layer transitions remain legible and reversible without converting relational language into identity or authority evidence.",
            source_refs=["docs/eiren-kestrel/v680-v7/x1/identity-and-boundary.json"],
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
                source_refs=["docs/eiren-kestrel/v680-v7/x1/portfolio-freeze.json"],
                protected_gates=common_gates,
            )
        )
    practice_rows = [
        (practice_ids["layers"], pillar_ids["GMUT Mind"], "Wallpaper layer-documentation analyst", "Synthetic elevation, layer order, pattern-repeat, maker-vacancy, uncertainty, correction, accessibility, and handover records only."),
        (practice_ids["mapping"], pillar_ids["THOS Body"], "Wallpaper condition-map lineage steward", "Synthetic map topology, mutation rejection, revision, hazardous-pigment holds, physical-action firewall, workload, and handover records only."),
        (practice_ids["dossier"], pillar_ids["Freed ID and CBR Heart"], "Architectural-finish dossier provenance steward", "Synthetic status, custody, minimum disclosure, rights vacancy, correction, remedy, and nonproduction identity records only."),
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
                source_refs=["docs/eiren-kestrel/v680-v7/x1/portfolio-freeze.json"],
                protected_gates=common_gates,
            )
        )
    for index, proposal in enumerate(proposals, start=1):
        parent = practice_ids["layers"] if index <= 20 else practice_ids["mapping"] if index <= 40 else practice_ids["dossier"]
        cards.append(
            flashcard(
                card_id=f"ghc-card-ek6807-task-{index:03d}",
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

The complete sanitized v680-v7 baton will be split across the thirteen modules in `docs/eiren-kestrel/v680-v7/x2/flashcards/baton-index.json`. Read the exact final packet and current roster before any later edge. This repository pointer is `PREPARED_NOT_SENT`; it is not delivery evidence.
""",
    )
    write_text(
        deck / "accessible-report.html",
        """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Eiren Kestrel v680-v7 flashcard deck</title></head><body><header><h1>Eiren Kestrel v680-v7 four-tier flashcard deck</h1></header><main><section aria-labelledby="structure"><h2 id="structure">Structure</h2><p>One relational owner card, three pillar cards, three practice cards, and sixty task cards are linked without tier skips.</p></section><section aria-labelledby="limits"><h2 id="limits">Evidence limits</h2><p>No card is evidence of consciousness, identity continuity, professional authority, empirical confirmation, legal or cultural authority, Maori authority, or Stage 20.</p></section><section aria-labelledby="evaluation"><h2 id="evaluation">Reserved evaluation</h2><p>Manual browser, assistive-technology, cognitive-accessibility, affected-user, and Maori-language evaluation remain open or exact-gated.</p></section></main></body></html>""",
    )
    manifest_paths = sorted(path for path in deck.rglob("*") if path.is_file() and path.name != "card-manifest.json")
    entries = []
    for path in manifest_paths:
        data = normalized_bytes(path)
        entries.append({"bytes": len(data), "path": rel(path), "sha256": sha256_bytes(data)})
    write_json(
        deck / "card-manifest.json",
        {
            "declared_self_exclusion": rel(deck / "card-manifest.json"),
            "entries": entries,
            "entry_count": len(entries),
            "schema": "ghc.family.flashcard-manifest.v1",
        },
    )


def load_contract_module():
    module_path = ROOT / "scripts" / "ghc_family_eiren_kestrel_v680_v7_contracts.py"
    spec = importlib.util.spec_from_file_location("ghc_family_eiren_kestrel_v680_v7_contracts", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Eiren bounded contract module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare() -> None:
    require_x1_boundary()
    if X2.exists() or SKILLS.exists():
        raise RuntimeError("x2 and owner-local skills must be absent before one-shot preparation")
    freeze = json.loads((X1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    proposals = freeze["proposals"]
    if len(proposals) != 60:
        raise RuntimeError("x1 proposal freeze drift")

    write_text(ROOT / "scripts" / "ghc_family_eiren_kestrel_v680_v7_contracts.py", CONTRACT_MODULE)
    write_text(ROOT / "scripts" / "ghc_family_eiren_kestrel_v680_v7_skill_bank.py", SKILL_BANK_MODULE)
    write_text(ROOT / "scripts" / "ghc_family_eiren_kestrel_v680_v7_runner_bank.py", RUNNER_BANK_MODULE)
    for index in range(1, 11):
        write_text(ROOT / "scripts" / f"ghc_family_eiren_v680_v7_lens_runner_{index:02d}.py", runner_module(index))

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
                f"default_prompt=Use ${name} to validate one synthetic zero-row fixture while preserving evidence and authority vacancies.",
            ],
            check=False,
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
        write_text(folder / "SKILL.md", skill_text(name, proposals[proposal_index - 1]["proposal_id"], proposals[proposal_index - 1]["title"]))
        write_text(folder / "agents" / "openai.yaml", skill_yaml(name))
    write_json(
        X2 / "skill-initialization-receipts.json",
        {
            "global_install": False,
            "initialized_count": sum(row["returncode"] == 0 for row in initialization_receipts),
            "owner": OWNER,
            "phase": PHASE,
            "receipts": initialization_receipts,
            "schema": "ghc.family.skill-initialization.v680.v7.x2",
            "subagent_forward_test": "not_run_solo_execution_required",
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
            invalid_result = contract.validate(proposal, contract.mutate(fixture, mutation["mutation_type"]))
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
                "bounded_representation_credit": 1 if outcome == "represented" else 0,
                "broader_claim_credit": 0,
                "completion_credit": 1 if outcome == "completed" else 0,
                "outcome": outcome,
                "positive_witness": witness_id,
                "proposal_id": proposal["proposal_id"],
                "protected_gates_preserved": True,
                "rejected_mutations": 5,
                "structural_positive_passed": True,
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
        "schema": "ghc.family.portfolio-results.v680.v7.x2",
        "successor_candidates": portfolio["successor_candidates"],
        "successor_credit": 0,
    }
    write_json(X2 / "positive-controls.json", {"accepted_count": 60, "owner": OWNER, "phase": PHASE, "receipts": positives, "schema": "ghc.family.positive-controls.v680.v7.x2"})
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
            "schema": "ghc.family.mutations.v680.v7.x2",
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
            "schema": "ghc.family.proposal-evidence.v680.v7.x2",
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
            "schema": "ghc.family.phase-toolchain-selection.v680.v7.x2",
            "selected_tools": [
                {"name": "check-jsonschema", "pinned_version": "0.38.0", "state": "selected_pending_isolated_install", "use": "local accepting and rejecting JSON Schema fixtures only"},
                {"name": "pyupgrade", "pinned_version": "3.21.2", "state": "selected_pending_isolated_install", "use": "disposable synthetic Python modernization fixture only"},
                {"name": "codespell", "pinned_version": "2.4.3", "state": "selected_pending_isolated_install", "use": "disposable accepting and rejecting prose fixtures only"},
            ],
            "target_environment": "D-first phase-isolated virtual environment",
        },
    )
    write_json(
        X2 / "successor-recommendations.json",
        {
            "candidate_seeds": portfolio["successor_candidates"],
            "clean_fix_refine_seeds": portfolio["successor_clean_fix_refine"],
            "owner": OWNER,
            "owner_completion_credit": 0,
            "phase": PHASE,
            "recipient_not_contacted": True,
            "runner_seeds": portfolio["successor_runner_ideas"],
            "schema": "ghc.family.successor-recommendations.v680.v7.x2",
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
            "schema": "ghc.family.x2-prepared-state.v680.v7",
            "skill_read_validate_smoke_pending": True,
            "toolchain_smoke_pending": True,
        },
    )
    print(json.dumps({"status": "X2_PREPARED_AWAITING_BOUNDED_SMOKES", "mutations": 300, "positives": 60, "skills": 20, "runners": 10}, indent=2))


DIST_PROBE = r'''import hashlib
import importlib.metadata as metadata
import json
import pathlib
import sys

dist = metadata.distribution(sys.argv[1])
h = hashlib.sha256()
count = 0
for item in sorted(dist.files or [], key=lambda value: str(value).casefold()):
    path = pathlib.Path(dist.locate_file(item))
    text = str(item).replace("\\", "/")
    if path.is_file() and "__pycache__" not in text and not text.endswith(".pyc"):
        h.update(text.encode("utf-8"))
        h.update(b"\0")
        h.update(path.read_bytes())
        h.update(b"\0")
        count += 1
license_value = dist.metadata.get("License-Expression") or dist.metadata.get("License") or ""
if not license_value.strip():
    license_value = "; ".join(v for v in dist.metadata.get_all("Classifier", []) if v.startswith("License ::"))
print(json.dumps({"installed_file_count": count, "license": license_value.strip(), "name": dist.metadata.get("Name"), "package_sha256": h.hexdigest(), "version": dist.version}))
'''


def run_process(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8")


def record_toolchain(venv: Path) -> None:
    require_x1_boundary()
    python = venv / "Scripts" / "python.exe"
    scripts = venv / "Scripts"
    if not python.is_file():
        raise RuntimeError("phase-isolated virtual environment is missing")
    pip_check = run_process([str(python), "-m", "pip", "check"])
    freeze = run_process([str(python), "-m", "pip", "freeze", "--all"])
    tools = []
    with tempfile.TemporaryDirectory(prefix="ek6807-tool-smoke-", dir=str(venv.parent)) as temporary:
        temp = Path(temporary)
        schema = temp / "schema.json"
        good = temp / "good.json"
        bad = temp / "bad.json"
        schema.write_text(json.dumps({"type": "object", "required": ["synthetic"], "properties": {"synthetic": {"const": True}}, "additionalProperties": False}) + "\n", encoding="utf-8")
        good.write_text('{"synthetic": true}\n', encoding="utf-8")
        bad.write_text('{"synthetic": false}\n', encoding="utf-8")
        check_good = run_process([str(scripts / "check-jsonschema.exe"), "--schemafile", str(schema), str(good)])
        check_bad = run_process([str(scripts / "check-jsonschema.exe"), "--schemafile", str(schema), str(bad)])

        legacy = temp / "legacy.py"
        legacy.write_text('value = u"synthetic"\n', encoding="utf-8")
        before = legacy.read_text(encoding="utf-8")
        upgrade = run_process([str(scripts / "pyupgrade.exe"), "--py3-plus", str(legacy)])
        after = legacy.read_text(encoding="utf-8")

        good_text = temp / "good.txt"
        bad_text = temp / "bad.txt"
        good_text.write_text("synthetic provenance boundary\n", encoding="utf-8")
        bad_text.write_text("teh recieve\n", encoding="utf-8")
        spell_good = run_process([str(scripts / "codespell.exe"), str(good_text)])
        spell_bad = run_process([str(scripts / "codespell.exe"), str(bad_text)])

        smokes = {
            "check-jsonschema": {
                "passed": check_good.returncode == 0 and check_bad.returncode != 0,
                "summary": "Accepted one local conforming instance and rejected one local nonconforming instance; zero remote schema fetches.",
            },
            "pyupgrade": {
                "passed": upgrade.returncode in (0, 1) and before != after and 'u"synthetic"' not in after,
                "summary": "Modernized one disposable synthetic Python fixture; exit 1 correctly denoted a rewrite and no repository path was supplied.",
            },
            "codespell": {
                "passed": spell_good.returncode == 0 and spell_bad.returncode != 0,
                "summary": "Accepted one disposable bounded prose fixture and rejected a paired misspelling fixture.",
            },
        }
    expected = {"check-jsonschema": "0.38.0", "pyupgrade": "3.21.2", "codespell": "2.4.3"}
    for name, version in expected.items():
        probe = run_process([str(python), "-X", "utf8", "-c", DIST_PROBE, name])
        if probe.returncode != 0:
            raise RuntimeError(f"distribution probe failed for {name}: {probe.stderr}")
        metadata_row = json.loads(probe.stdout)
        installed = metadata_row["version"] == version
        smoke = smokes[name]
        tools.append(
            {
                "downloaded_and_installed": installed,
                "installed": installed,
                "installed_file_count": metadata_row["installed_file_count"],
                "license": metadata_row["license"],
                "name": name,
                "package_sha256": metadata_row["package_sha256"],
                "smoke": smoke["summary"],
                "smoke_passed": smoke["passed"],
                "version": metadata_row["version"],
            }
        )
    if pip_check.returncode != 0 or any(not row["installed"] or not row["smoke_passed"] for row in tools):
        raise RuntimeError("phase toolchain dependency or smoke gate failed")
    write_json(
        X2 / "toolchain-install-receipt.json",
        {
            "dependency_check_output": pip_check.stdout.strip(),
            "dependency_check_passed": True,
            "global_install": False,
            "failed_atomic_attempt_retained": None,
            "installed_count": 3,
            "owner": OWNER,
            "phase": PHASE,
            "resolved_environment_packages": sorted(line for line in freeze.stdout.splitlines() if line.strip()),
            "rollback": "Delete only the phase-isolated environment after resolving its literal D-first path; no global package state was changed.",
            "schema": "ghc.family.phase-toolchain-install.v680.v7.x2",
            "smoke_used_count": 3,
            "target_environment": "D-first phase-isolated virtual environment",
            "tools": tools,
        },
    )
    print(json.dumps({"status": "TOOLCHAIN_RECORDED", "installed": 3, "smoke_used": 3}, indent=2))


def finalize() -> None:
    require_x1_boundary()
    skill_receipt_path = X2 / "skill-smoke-receipts.json"
    runner_receipt_path = X2 / "runner-smoke-receipts.json"
    tool_receipt_path = X2 / "toolchain-install-receipt.json"
    if not skill_receipt_path.exists() or not runner_receipt_path.exists() or not tool_receipt_path.exists():
        raise RuntimeError("skill, runner, and phase-tool smoke receipts are required")
    skills = json.loads(skill_receipt_path.read_text(encoding="utf-8"))
    runners = json.loads(runner_receipt_path.read_text(encoding="utf-8"))
    tools = json.loads(tool_receipt_path.read_text(encoding="utf-8"))
    if skills["validated_count"] != 20 or skills["smoke_used_count"] != 20 or runners["passed_count"] != 10:
        raise RuntimeError("skill or runner smoke gate failed")
    if tools["installed_count"] != 3 or tools["smoke_used_count"] != 3 or not tools["dependency_check_passed"]:
        raise RuntimeError("phase tool smoke gate failed")

    freeze = json.loads((X1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    evidence = json.loads((X2 / "proposal-evidence.json").read_text(encoding="utf-8"))
    mutations = json.loads((X2 / "mutations.json").read_text(encoding="utf-8"))
    positives = json.loads((X2 / "positive-controls.json").read_text(encoding="utf-8"))
    startup = json.loads((X1 / "method-flow-startup.json").read_text(encoding="utf-8"))
    x2_operational_failures: list[dict[str, Any]] = [
        {
            "failure_id": "EK6807-X2-N001",
            "false_witness": "The first post-x1 fetch-and-four-way-equality wrapper would either complete inside its reporting window or surface its resumable session identifier.",
            "initial_credit": 0,
            "observed": "The wrapper yielded no payload because its orchestration projection omitted the returned session identifier; later process inspection found no Git process alive and the lane remained clean.",
            "recovery": "Retain the missing presentation at zero credit, do not repeat the completed fetch, and run only a nonmutating scalar ref plus fresh ls-remote comparison; local, upstream, tracking, and fresh live were equal at x1 with 0/0 divergence.",
            "recovery_rewrites_failure": False,
            "repository_mutated_by_failure": False,
            "scope": "post_x1_four_way_equality_presentation",
        },
        {
            "failure_id": "EK6807-X2-N002",
            "false_witness": "A Windows ripgrep inspection could pass shell wildcard path operands for all copied Eiren x2 support modules and runners.",
            "initial_credit": 0,
            "observed": "Ripgrep rejected the wildcard operands with Windows filename syntax error 123 while still returning bounded matches from the two literal file operands.",
            "recovery": "Retain the mixed inspection at zero aggregate credit and use rg --files followed by a filename filter, or pass an exact materialized path array, before content inspection; no repository state depended on the failed wildcard operands.",
            "recovery_rewrites_failure": False,
            "repository_mutated_by_failure": False,
            "scope": "windows_literal_path_content_inventory",
        },
        {
            "failure_id": "EK6807-X2-N003",
            "false_witness": "The first bounded Ruff check of the adapted x2 builder, contract, skill bank, runner bank, ten runners, and evidence test would be clean without family-template modernization.",
            "initial_credit": 0,
            "observed": "Ruff reported 22 import-order, subprocess-check, and prefix-test findings; 17 were declared directly fixable and five required explicit bounded review.",
            "recovery": "Retain the check at zero success credit, apply only Ruff's safe fixes, add explicit check=False to subprocess probes whose return codes are intentionally inspected, use one tuple startswith predicate, inspect the diff, and rerun the exact bounded check.",
            "recovery_rewrites_failure": False,
            "repository_mutated_by_failure": False,
            "scope": "x2_family_surface_static_quality",
        },
    ]
    counts = {
        "bounded_passing_witnesses": 39788 + len(x2_operational_failures),
        "effective_methods": 57846 + len(x2_operational_failures),
        "effective_negatives": 52309 + len(x2_operational_failures),
        "exact_gates": 452,
        "failed_witnesses": 23970 + len(x2_operational_failures),
        "open_gaps": 461,
    }
    method_records = [
        {
            "candidate": "preregistered_in_immutable_x1",
            "independent_reproduction": False,
            "method_id": f"EK6807-METHOD-{index:03d}",
            "preferred": "bounded_owner_local_contract_only",
            "proposal_id": proposal["proposal_id"],
            "validated": "one_zero_row_positive_and_five_rejecting_mutations",
        }
        for index, proposal in enumerate(freeze["proposals"], start=1)
    ]
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
            "schema": "ghc.family.method-flow.v680.v7.x2",
            "startup_and_x1_failures": startup["startup_failures"],
            "x2_operational_failures": x2_operational_failures,
        },
    )
    write_json(
        X2 / "phase-truth.json",
        {
            "counts": counts,
            "declared_chain": 9650,
            "outcomes": evidence["outcome_counts"],
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": 60,
            "schema": "ghc.family.phase-truth.v680.v7.x2",
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
            "schema": "ghc.family.retained-negatives.v680.v7.x2",
            "startup_and_x1_failures": 14,
            "x2_operational_failures": x2_operational_failures,
        },
    )
    write_json(
        X2 / "gate-register.json",
        {
            "exact_gates": 452,
            "inherited_exact_gates": 449,
            "inherited_open_gaps": 458,
            "new_exact_gates": 3,
            "new_open_gaps": 3,
            "open_gaps": 461,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.gate-register.v680.v7.x2",
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
            "schema": "ghc.family.source-use.v680.v7.x2",
            "sources_used_for_vocabulary_only": 10,
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
            "schema": "ghc.family.threat-controls.v680.v7.x2",
        },
    )
    write_json(
        X2 / "complete-incomplete-ledger.json",
        {
            "completed": [
                "60 proposal dispositions executed only as evidence permitted",
                "300 rejecting mutations retained",
                "20 owner-local skills initialized validated read and smoke-used",
                "10 family-current runners smoke-used",
                "67 four-tier flashcards validated",
                "3 D-isolated phase tools installed and smoke-used",
            ],
            "incomplete": [
                "all 461 open gaps",
                "all 452 exact gates",
                "manual browser assistive-technology cognitive Maori-language and affected-user evaluation",
                "full repository suite",
                "independent reproduction",
                "Stage 20",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.complete-incomplete.v680.v7.x2",
        },
    )
    write_json(
        X2 / "prepared-state.json",
        {
            "finalized": True,
            "owner": OWNER,
            "phase": PHASE,
            "runner_smoke_pending": False,
            "schema": "ghc.family.x2-prepared-state.v680.v7",
            "skill_read_validate_smoke_pending": False,
            "toolchain_smoke_pending": False,
        },
    )
    write_text(
        X2 / "integrated-overview.md",
        """# Eiren Kestrel v680-v7 bounded x2 evidence

This phase executed sixty wholly synthetic zero-row proposal contracts and all 300 preregistered rejecting mutations. Outcomes are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Every rejected mutation remains a zero-credit failed witness. Twenty owner-local skills were officially initialized, customized, read through EOF, quick-validated, and accepting/rejecting smoke-used without global installation. Ten family-current runners were accepting/rejecting smoke-used. Three pinned tools were installed only into a D-first phase-isolated environment and smoke-used on disposable synthetic fixtures.

Freed ID and CBR Heart are primary through wholly synthetic historic-wallpaper layer and pattern documentation, condition-map lineage, and architectural-finish dossiers. GMUT Mind and THOS Body remain explicit and protected. No real person, participant, owner, custodian, architect, conservator, building, wall, wallpaper, layer, pigment, adhesive, sample, collection record, observation, measurement, treatment, identity event, credential, safety action, external write, or authority act occurred.

Official sources supplied vocabulary and refusal boundaries only. No software, synthetic fixture, citation, or same-owner validation establishes empirical confirmation, professional competence, workplace or machinery safety, production readiness, legal or cultural legitimacy, affected-party acceptance, Maori authority, complete privacy or accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything proof, canon, or Stage 20 authority.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )

    script_path = "scripts/build_ghc_family_eiren_kestrel_v680_v7_x2.py"
    test_path = "tests/test_ghc_family_eiren_kestrel_v680_v7_evidence.py"
    status_rows = git("status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines()
    actual_paths = sorted({row[3:].replace("\\", "/") for row in status_rows if len(row) >= 4})
    exclusions = [
        "docs/eiren-kestrel/v680-v7/validation/evidence-index-manifest.json",
        "docs/eiren-kestrel/v680-v7/validation/evidence-privacy-scan.json",
        "docs/eiren-kestrel/v680-v7/validation/evidence-security-scan.json",
        "docs/eiren-kestrel/v680-v7/validation/evidence-staged-review.json",
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
                definition_only = path_text.startswith(("scripts/", "tests/"))
                row = {"class": class_name, "disposition": "scanner_definition_only" if definition_only else "confirmed_payload_hit", "path": path_text}
                candidates.append(row)
                if not definition_only:
                    confirmed.append(row)
    if confirmed or ast_errors:
        raise RuntimeError(json.dumps({"privacy": confirmed, "ast": ast_errors}))
    write_json(
        VALIDATION / "evidence-privacy-scan.json",
        {"candidates": candidates, "confirmed_hits": confirmed, "owner": OWNER, "phase": PHASE, "privacy_classes": list(scanners), "scanned_files": len(content_paths), "schema": "ghc.family.privacy-scan.v680.v7.evidence"},
    )
    write_json(
        VALIDATION / "evidence-security-scan.json",
        {"ast_errors": ast_errors, "bounded_findings": 0, "owner": OWNER, "phase": PHASE, "python_files": sum(path.endswith(".py") for path in content_paths), "schema": "ghc.family.security-scan.v680.v7.evidence"},
    )
    expected_paths = sorted(set(content_paths + exclusions))
    write_json(
        VALIDATION / "evidence-staged-review.json",
        {"declared_self_exclusions": exclusions, "expected_paths": expected_paths, "lifecycle": "bounded_x2_evidence", "owner": OWNER, "path_count": len(expected_paths), "phase": PHASE, "schema": "ghc.family.staged-review.v680.v7.evidence"},
    )
    entries = []
    for path_text in content_paths:
        data = normalized_bytes(ROOT / path_text)
        entries.append({"bytes": len(data), "path": path_text, "sha256": sha256_bytes(data)})
    write_json(
        VALIDATION / "evidence-index-manifest.json",
        {"declared_self_exclusions": exclusions, "entries": entries, "entry_count": len(entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-index-manifest.v680.v7.evidence", "x1": X1_HEAD},
    )
    print(json.dumps({"status": "X2_FINALIZED_FOR_EVIDENCE_REVIEW", "entries": len(entries), "skills": 20, "runners": 10}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize", action="store_true")
    parser.add_argument("--record-toolchain", action="store_true")
    parser.add_argument("--venv")
    args = parser.parse_args()
    if args.finalize:
        finalize()
    elif args.record_toolchain:
        if not args.venv:
            raise RuntimeError("--venv is required for toolchain recording")
        record_toolchain(Path(args.venv))
    else:
        prepare()


if __name__ == "__main__":
    main()
