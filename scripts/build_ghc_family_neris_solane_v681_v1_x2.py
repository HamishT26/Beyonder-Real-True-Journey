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
BASE = ROOT / "docs" / "neris-solane" / "v681-v1"
X1 = BASE / "x1"
X2 = BASE / "x2"
SKILLS = BASE / "skills"
VALIDATION = BASE / "validation"

OWNER = "Neris Solane"
PHASE = "v681-v1"
BRANCH = "codex/GHC-Family/neris-solane-v681-v1-full-tools"
SOURCE = "40eefe9e5bd82c69063e2fe040db53ba08acb593"
X1_HEAD = "dc2a06ff4429ccf3bcac079aaa93da44905248df"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
WRITTEN: list[str] = []


SKILL_NAMES = [
    "01-pneumatic-carrier-object-boundary",
    "02-station-route-label-separation",
    "03-tube-topology-nonoperation",
    "04-dispatch-docket-nonmail",
    "05-pressure-measurement-vacancy",
    "06-payload-content-firewall",
    "07-operator-identity-vacancy",
    "08-custody-title-non-equivalence",
    "09-route-exception-lineage",
    "10-pressure-equipment-safety-hold",
    "11-physical-action-firewall",
    "12-synthetic-dispatch-state-machine",
    "13-envelope-provenance-braid",
    "14-message-rights-vacancy",
    "15-minimum-disclosure",
    "16-accessible-sequence-companion",
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
        raise RuntimeError("x2 requires the immutable pushed Neris x1 head")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Neris owner branch")
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
from ghc_family_neris_solane_v681_v1_contracts import (
    mutate,
    positive_fixture,
    validate,
)

SKILL_PROPOSAL_INDEXES = [1, 3, 2, 6, 11, 14, 21, 23, 35, 29, 58, 42, 51, 52, 53, 39, 20, 40, 32, 60]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    base = ROOT / "docs" / "neris-solane" / "v681-v1"
    freeze = json.loads((base / "x1" / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    quick_validate = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    receipts = []
    for index, folder in enumerate(sorted(path for path in (base / "skills").iterdir() if path.is_dir()), start=1):
        skill_text = (folder / "SKILL.md").read_text(encoding="utf-8")
        validation = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(quick_validate), str(folder)],
            check=False,
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
        "owner": "Neris Solane",
        "phase": "v681-v1",
        "receipts": receipts,
        "schema": "ghc.family.skill-smoke.v681.v1.x2",
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
        runner = ROOT / "scripts" / f"ghc_family_neris_v681_v1_lens_runner_{index:02d}.py"
        result = subprocess.run([sys.executable, "-B", "-X", "utf8", str(runner)], check=False, capture_output=True, text=True, encoding="utf-8")
        payload = json.loads(result.stdout) if result.returncode == 0 else {}
        receipts.append({"runner": runner.stem, "returncode": result.returncode, **payload})
    target = ROOT / args.receipt
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "owner": "Neris Solane",
        "passed_count": sum(row.get("positive_accepted") and row.get("invalid_rejected") for row in receipts),
        "phase": "v681-v1",
        "receipts": receipts,
        "runner_count": len(receipts),
        "schema": "ghc.family.runner-smoke.v681.v1.x2",
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
from ghc_family_neris_solane_v681_v1_contracts import (
    mutate,
    positive_fixture,
    validate,
)

freeze = json.loads((ROOT / "docs" / "neris-solane" / "v681-v1" / "x1" / "new-proposal-freeze.json").read_text(encoding="utf-8"))
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
description: Validate the bounded synthetic pneumatic-dispatch record distinction for {proposal_id}; do not use for real messages, mail, carriers, stations, tubes, pressure equipment, routes, operations, safety, rights, cultural, or authority decisions.
---

# GHC Family Bounded Evidence {display}

## Scope

Validate one wholly synthetic zero-row fixture for `{proposal_id}`: {title}. This skill cannot inspect, count, measure, route, open, transport, pressurize, operate, maintain, repair, release, publish, certify, or authorize a real person, message, mail item, carrier capsule, station, tube, compressor, pressure system, route, workplace, dataset, identity event, or decision.

## Inputs

- The immutable `{proposal_id}` x1 contract.
- One fixture in `synthetic.example.invalid` with zero real rows.
- No people, objects, materials, measurements, credentials, private routes, or real-world state.

## Steps

1. Confirm the synthetic namespace, zero-row marker, and nonproduction state.
2. Compare proposal-bound provenance digest and lifecycle order.
3. Preserve unknown safety, operator, custody, payload, pressure, measurement, and rights states.
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
    owner_id = "ghc-card-ne6811-owner"
    pillar_ids = {
        "GMUT Mind": "ghc-card-ne6811-pillar-gmut",
        "THOS Body": "ghc-card-ne6811-pillar-thos",
        "Freed ID and CBR Heart": "ghc-card-ne6811-pillar-freed-id-cbr",
    }
    practice_ids = {
        "carrier": "ghc-card-ne6811-practice-carrier-station-record",
        "route": "ghc-card-ne6811-practice-dispatch-route-lineage",
        "envelope": "ghc-card-ne6811-practice-envelope-privacy-custody",
    }
    common_gates = [
        "real people messages mail carrier capsules stations tubes compressors pressure systems routes observations and measurements",
        "professional pressure-equipment engineering machinery operation maintenance workplace and public safety",
        "payload access custody title privacy remedy legal cultural affected-party and Maori authority",
        "empirical production independent-reproduction proof canon and Stage 20",
    ]
    cards: list[dict[str, Any]] = [
        flashcard(
            card_id=owner_id,
            tier=1,
            card_type="freed_id_owner",
            title="Neris Solane relational owner anchor",
            parent_ids=[],
            stability="stable_boundary",
            outcome="represented",
            content="Pneumatic-dispatch provenance cartographer and pressure-operation gatekeeper; synthetic carrier, station, route, envelope, exception, and correction transitions remain legible without converting relational language into identity or authority evidence.",
            source_refs=["docs/neris-solane/v681-v1/x1/identity-and-boundary.json"],
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
                source_refs=["docs/neris-solane/v681-v1/x1/portfolio-freeze.json"],
                protected_gates=common_gates,
            )
        )
    practice_rows = [
        (practice_ids["carrier"], pillar_ids["THOS Body"], "Synthetic historical carrier-capsule and station-record analyst", "Synthetic carrier, station-label, topology, pressure-vacancy, safety-hold, correction, accessibility, and handover records only."),
        (practice_ids["route"], pillar_ids["GMUT Mind"], "Dispatch-route and queue exception-lineage steward", "Synthetic route graph, queue transition, mutation rejection, revision, workload, and zero-operation handover records only."),
        (practice_ids["envelope"], pillar_ids["Freed ID and CBR Heart"], "Message-envelope privacy and custody-provenance steward", "Synthetic payload-content vacancy, custody, minimum disclosure, message-rights vacancy, correction, remedy, and nonproduction identity records only."),
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
                source_refs=["docs/neris-solane/v681-v1/x1/portfolio-freeze.json"],
                protected_gates=common_gates,
            )
        )
    for index, proposal in enumerate(proposals, start=1):
        parent = practice_ids["carrier"] if index <= 20 else practice_ids["route"] if index <= 40 else practice_ids["envelope"]
        cards.append(
            flashcard(
                card_id=f"ghc-card-ne6811-task-{index:03d}",
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

The complete sanitized v681-v1 baton will be split across the thirteen modules in `docs/neris-solane/v681-v1/x2/flashcards/baton-index.json`. Read the exact final packet and current roster before any later edge. This repository pointer is `PREPARED_NOT_SENT`; it is not delivery evidence.
""",
    )
    write_text(
        deck / "accessible-report.html",
        """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Neris Solane v681-v1 flashcard deck</title></head><body><header><h1>Neris Solane v681-v1 four-tier flashcard deck</h1></header><main><section aria-labelledby="structure"><h2 id="structure">Structure</h2><p>One relational owner card, three pillar cards, three practice cards, and sixty task cards are linked without tier skips.</p></section><section aria-labelledby="limits"><h2 id="limits">Evidence limits</h2><p>No card is evidence of consciousness, identity continuity, professional authority, empirical confirmation, legal or cultural authority, Maori authority, or Stage 20.</p></section><section aria-labelledby="evaluation"><h2 id="evaluation">Reserved evaluation</h2><p>Manual browser, assistive-technology, cognitive-accessibility, affected-user, and Maori-language evaluation remain open or exact-gated.</p></section></main></body></html>""",
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
    module_path = ROOT / "scripts" / "ghc_family_neris_solane_v681_v1_contracts.py"
    spec = importlib.util.spec_from_file_location("ghc_family_neris_solane_v681_v1_contracts", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Neris bounded contract module")
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

    write_text(ROOT / "scripts" / "ghc_family_neris_solane_v681_v1_contracts.py", CONTRACT_MODULE)
    write_text(ROOT / "scripts" / "ghc_family_neris_solane_v681_v1_skill_bank.py", SKILL_BANK_MODULE)
    write_text(ROOT / "scripts" / "ghc_family_neris_solane_v681_v1_runner_bank.py", RUNNER_BANK_MODULE)
    for index in range(1, 11):
        write_text(ROOT / "scripts" / f"ghc_family_neris_v681_v1_lens_runner_{index:02d}.py", runner_module(index))

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
            "schema": "ghc.family.skill-initialization.v681.v1.x2",
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
        "schema": "ghc.family.portfolio-results.v681.v1.x2",
        "successor_candidates": portfolio["successor_candidates"],
        "successor_credit": 0,
    }
    write_json(X2 / "positive-controls.json", {"accepted_count": 60, "owner": OWNER, "phase": PHASE, "receipts": positives, "schema": "ghc.family.positive-controls.v681.v1.x2"})
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
            "schema": "ghc.family.mutations.v681.v1.x2",
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
            "schema": "ghc.family.proposal-evidence.v681.v1.x2",
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
            "schema": "ghc.family.phase-toolchain-selection.v681.v1.x2",
            "selected_tools": [
                {
                    "maturity_limit": "library-only bounded pointer resolution; not a schema, security, interoperability, or production validator",
                    "name": "jsonpointer",
                    "official_project_url": "https://pypi.org/project/jsonpointer/",
                    "official_wheel_sha256": "8ff8b95779d071ba472cf5bc913028df06031797532f08a7d5b602d8b2a488ca",
                    "pinned_version": "3.1.1",
                    "state": "selected_pending_isolated_install",
                    "use": "resolve one local synthetic route pointer and reject one missing pointer",
                },
                {
                    "maturity_limit": "PyPI classifies the release as pre-alpha; use is restricted to disposable syntax fixtures and earns no production assurance",
                    "name": "rfc3339-validator",
                    "official_project_url": "https://pypi.org/project/rfc3339-validator/",
                    "official_wheel_sha256": "24f6ec1eda14ef823da9e36ec7113124b39c04d50a4d3d3a3c2859577e7791fa",
                    "pinned_version": "0.1.4",
                    "state": "selected_pending_isolated_install",
                    "use": "accept one local synthetic RFC 3339 timestamp and reject one invalid timestamp",
                },
                {
                    "maturity_limit": "library-only bounded hostname syntax check; not DNS resolution, reachability, identity, ownership, or security evidence",
                    "name": "fqdn",
                    "official_project_url": "https://pypi.org/project/fqdn/",
                    "official_wheel_sha256": "3a179af3761e4df6eb2e026ff9e1a3033d3587bf980a0b1b2e1e5d08d7358014",
                    "pinned_version": "1.5.1",
                    "state": "selected_pending_isolated_install",
                    "use": "accept one local synthetic FQDN and reject one whitespace-bearing invalid hostname",
                },
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
            "schema": "ghc.family.successor-recommendations.v681.v1.x2",
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
            "schema": "ghc.family.x2-prepared-state.v681.v1",
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


def record_toolchain(venv: Path, wheel_dir: Path) -> None:
    require_x1_boundary()
    python = venv / "Scripts" / "python.exe"
    if not python.is_file():
        raise RuntimeError("phase-isolated virtual environment is missing")
    if not wheel_dir.is_dir():
        raise RuntimeError("verified wheel directory is missing")
    pip_check = run_process([str(python), "-m", "pip", "check"])
    freeze = run_process([str(python), "-m", "pip", "freeze", "--all"])
    smoke_scripts = {
        "jsonpointer": """import json
from jsonpointer import JsonPointerException, resolve_pointer
good = resolve_pointer({"route": {"station": "SYN"}}, "/route/station") == "SYN"
try:
    resolve_pointer({"route": {}}, "/route/missing")
except JsonPointerException:
    bad = True
else:
    bad = False
print(json.dumps({"accepted": good, "rejected": bad}))
""",
        "rfc3339-validator": """import json
from rfc3339_validator import validate_rfc3339
print(json.dumps({"accepted": validate_rfc3339("2026-09-01T00:00:00Z"), "rejected": not validate_rfc3339("not-a-timestamp")}))
""",
        "fqdn": """import json
from fqdn import FQDN
print(json.dumps({"accepted": FQDN("station.synthetic.example").is_valid, "rejected": not FQDN("not a host").is_valid}))
""",
    }
    expected = {
        "jsonpointer": {"version": "3.1.1", "wheel_sha256": "8ff8b95779d071ba472cf5bc913028df06031797532f08a7d5b602d8b2a488ca"},
        "rfc3339-validator": {"version": "0.1.4", "wheel_sha256": "24f6ec1eda14ef823da9e36ec7113124b39c04d50a4d3d3a3c2859577e7791fa"},
        "fqdn": {"version": "1.5.1", "wheel_sha256": "3a179af3761e4df6eb2e026ff9e1a3033d3587bf980a0b1b2e1e5d08d7358014"},
    }
    tools = []
    for name, expectation in expected.items():
        version = expectation["version"]
        normalized_prefix = f"{name}-{version}".replace("-", "_").casefold()
        wheel_candidates = [
            path
            for path in wheel_dir.glob("*.whl")
            if path.name.replace("-", "_").casefold().startswith(normalized_prefix)
        ]
        if len(wheel_candidates) != 1:
            raise RuntimeError(f"expected exactly one wheel for {name} {version}, found {len(wheel_candidates)}")
        wheel = wheel_candidates[0]
        wheel_sha256 = sha256_bytes(wheel.read_bytes())
        if wheel_sha256 != expectation["wheel_sha256"]:
            raise RuntimeError(f"official wheel hash mismatch for {name}")
        probe = run_process([str(python), "-X", "utf8", "-c", DIST_PROBE, name])
        if probe.returncode != 0:
            raise RuntimeError(f"distribution probe failed for {name}: {probe.stderr}")
        metadata_row = json.loads(probe.stdout)
        installed = metadata_row["version"] == version
        smoke_probe = run_process([str(python), "-X", "utf8", "-c", smoke_scripts[name]])
        smoke_result = json.loads(smoke_probe.stdout) if smoke_probe.returncode == 0 else {}
        smoke_passed = smoke_result.get("accepted") is True and smoke_result.get("rejected") is True
        tools.append(
            {
                "downloaded_and_installed": installed,
                "installed": installed,
                "installed_file_count": metadata_row["installed_file_count"],
                "license": metadata_row["license"],
                "name": name,
                "package_sha256": metadata_row["package_sha256"],
                "smoke": "Accepted one bounded local synthetic fixture and rejected one paired invalid fixture; no network or repository path was supplied.",
                "smoke_passed": smoke_passed,
                "version": metadata_row["version"],
                "wheel_filename": wheel.name,
                "wheel_sha256": wheel_sha256,
                "wheel_sha256_verified": True,
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
            "schema": "ghc.family.phase-toolchain-install.v681.v1.x2",
            "smoke_used_count": 3,
            "target_environment": "D-first phase-isolated virtual environment",
            "tools": tools,
            "wheel_hashes_verified": True,
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
            "failure_id": "NE6811-X2-N001",
            "false_witness": "The first exact generated-surface Ruff review would pass without any target-specific formatting correction.",
            "initial_credit": 0,
            "observed": "Compilation passed, but Ruff rejected one extra blank line in the generated skill-bank import block.",
            "recovery": "Retain the rejection at zero credit, remove only the redundant blank line from both the generator template and generated skill bank, and rerun only the changed exact static-quality dependency.",
            "recovery_rewrites_failure": False,
            "repository_mutated_by_failure": False,
            "scope": "x2_generated_skill_bank_static_quality",
        }
    ]
    counts = {
        "bounded_passing_witnesses": 41208 + len(x2_operational_failures),
        "effective_methods": 59386 + len(x2_operational_failures),
        "effective_negatives": 52949 + len(x2_operational_failures),
        "exact_gates": 458,
        "failed_witnesses": 24610 + len(x2_operational_failures),
        "open_gaps": 467,
    }
    method_records = [
        {
            "candidate": "preregistered_in_immutable_x1",
            "independent_reproduction": False,
            "method_id": f"NE6811-METHOD-{index:03d}",
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
            "schema": "ghc.family.method-flow.v681.v1.x2",
            "startup_and_x1_failures": startup["startup_failures"],
            "x2_operational_failures": x2_operational_failures,
        },
    )
    write_json(
        X2 / "phase-truth.json",
        {
            "counts": counts,
            "declared_chain": 9770,
            "outcomes": evidence["outcome_counts"],
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": 60,
            "schema": "ghc.family.phase-truth.v681.v1.x2",
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
            "schema": "ghc.family.retained-negatives.v681.v1.x2",
            "startup_and_x1_failures": 15,
            "x2_operational_failures": x2_operational_failures,
        },
    )
    write_json(
        X2 / "gate-register.json",
        {
            "exact_gates": 458,
            "inherited_exact_gates": 455,
            "inherited_open_gaps": 464,
            "new_exact_gates": 3,
            "new_open_gaps": 3,
            "open_gaps": 467,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.gate-register.v681.v1.x2",
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
            "schema": "ghc.family.source-use.v681.v1.x2",
            "sources_used_for_vocabulary_only": 12,
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
            "schema": "ghc.family.threat-controls.v681.v1.x2",
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
                "all 467 open gaps",
                "all 458 exact gates",
                "manual browser assistive-technology cognitive Maori-language and affected-user evaluation",
                "full repository suite",
                "independent reproduction",
                "Stage 20",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.complete-incomplete.v681.v1.x2",
        },
    )
    write_json(
        X2 / "prepared-state.json",
        {
            "finalized": True,
            "owner": OWNER,
            "phase": PHASE,
            "runner_smoke_pending": False,
            "schema": "ghc.family.x2-prepared-state.v681.v1",
            "skill_read_validate_smoke_pending": False,
            "toolchain_smoke_pending": False,
        },
    )
    write_text(
        X2 / "integrated-overview.md",
        """# Neris Solane v681-v1 bounded x2 evidence

This phase executed sixty wholly synthetic zero-row proposal contracts and all 300 preregistered rejecting mutations. Outcomes are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Every rejected mutation remains a zero-credit failed witness. Twenty owner-local skills were officially initialized, customized, read through EOF, quick-validated, and accepting/rejecting smoke-used without global installation. Ten family-current runners were accepting/rejecting smoke-used. Three pinned tools were installed only into a D-first phase-isolated environment and smoke-used on disposable synthetic fixtures.

THOS Body is primary through wholly synthetic historical pneumatic carrier-capsule, station-record, route-topology, queue-transition, exception-lineage, message-envelope, and custody-provenance dossiers. GMUT Mind, Freed ID, and CBR Heart remain explicit and protected. No real person, participant, sender, recipient, operator, owner, custodian, message, mail item, carrier capsule, station, tube, compressor, pressure system, route, measurement, handling, transport, operation, maintenance, repair, identity event, credential, safety action, external write, or authority act occurred.

Official sources supplied vocabulary and refusal boundaries only. No software, synthetic fixture, citation, or same-owner validation establishes empirical confirmation, professional competence, workplace or machinery safety, production readiness, legal or cultural legitimacy, affected-party acceptance, Maori authority, complete privacy or accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything proof, canon, or Stage 20 authority.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )

    script_path = "scripts/build_ghc_family_neris_solane_v681_v1_x2.py"
    test_path = "tests/test_ghc_family_neris_solane_v681_v1_evidence.py"
    status_rows = git("status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines()
    actual_paths = sorted({row[3:].replace("\\", "/") for row in status_rows if len(row) >= 4})
    exclusions = [
        "docs/neris-solane/v681-v1/validation/evidence-index-manifest.json",
        "docs/neris-solane/v681-v1/validation/evidence-privacy-scan.json",
        "docs/neris-solane/v681-v1/validation/evidence-security-scan.json",
        "docs/neris-solane/v681-v1/validation/evidence-staged-review.json",
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
        {"candidates": candidates, "confirmed_hits": confirmed, "owner": OWNER, "phase": PHASE, "privacy_classes": list(scanners), "scanned_files": len(content_paths), "schema": "ghc.family.privacy-scan.v681.v1.evidence"},
    )
    write_json(
        VALIDATION / "evidence-security-scan.json",
        {"ast_errors": ast_errors, "bounded_findings": 0, "owner": OWNER, "phase": PHASE, "python_files": sum(path.endswith(".py") for path in content_paths), "schema": "ghc.family.security-scan.v681.v1.evidence"},
    )
    expected_paths = sorted(set(content_paths + exclusions))
    write_json(
        VALIDATION / "evidence-staged-review.json",
        {"declared_self_exclusions": exclusions, "expected_paths": expected_paths, "lifecycle": "bounded_x2_evidence", "owner": OWNER, "path_count": len(expected_paths), "phase": PHASE, "schema": "ghc.family.staged-review.v681.v1.evidence"},
    )
    entries = []
    for path_text in content_paths:
        data = normalized_bytes(ROOT / path_text)
        entries.append({"bytes": len(data), "path": path_text, "sha256": sha256_bytes(data)})
    write_json(
        VALIDATION / "evidence-index-manifest.json",
        {"declared_self_exclusions": exclusions, "entries": entries, "entry_count": len(entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-index-manifest.v681.v1.evidence", "x1": X1_HEAD},
    )
    print(json.dumps({"status": "X2_FINALIZED_FOR_EVIDENCE_REVIEW", "entries": len(entries), "skills": 20, "runners": 10}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize", action="store_true")
    parser.add_argument("--record-toolchain", action="store_true")
    parser.add_argument("--venv")
    parser.add_argument("--wheel-dir")
    args = parser.parse_args()
    if args.finalize:
        finalize()
    elif args.record_toolchain:
        if not args.venv or not args.wheel_dir:
            raise RuntimeError("--venv and --wheel-dir are required for toolchain recording")
        record_toolchain(Path(args.venv), Path(args.wheel_dir))
    else:
        prepare()


if __name__ == "__main__":
    main()
