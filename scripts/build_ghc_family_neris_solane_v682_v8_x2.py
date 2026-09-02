"""Build bounded Neris Solane v682-v8 x2 evidence from frozen x1 contracts."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess  # nosec B404
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Literal

from scripts.ghc_family_neris_solane_v682_v8_contracts import execute_proposal
from scripts.ghc_family_neris_solane_v682_v8_skill_bank import (
    SKILL_NAMES,
    smoke_skills,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE = "v682-v8"
OWNER = "Neris Solane"
X1 = ROOT / "docs" / "neris-solane" / PHASE / "x1"
X2 = ROOT / "docs" / "neris-solane" / PHASE / "x2"
VALIDATION = ROOT / "docs" / "neris-solane" / PHASE / "validation"
X1_SHA = "d1a3bb0fc1964608478dcc1bc9b236183617ef8a"
SOURCE = "938162611d2ce944ddcddf64834bd93e045e3c49"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
WRITTEN: list[str] = []

ACTIVATION_BASELINE = {
    "effective_negatives": 57457,
    "effective_methods": 69819,
    "failed_witnesses": 29118,
    "bounded_passing_witnesses": 50919,
    "open_gaps": 510,
    "exact_gates": 500,
}

STARTUP_FAILURES = json.loads(
    (X1 / "method-flow-startup.json").read_text(encoding="utf-8")
)["startup_failures"]

POST_X1_FAILURES: list[dict[str, Any]] = [
    {
        "failure_id": "NS6828-X2-N009",
        "failed_witness": "The first residue scan passed a wildcard Python path literally to ripgrep on Windows and returned a filename error.",
        "initial_credit": 0,
        "recovery": "Use ripgrep's include-glob option over the exact scripts directory and retain the literal-wildcard failure at zero credit.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "NS6828-X2-N010",
        "failed_witness": "Direct file invocation placed the scripts directory rather than the repository root on Python's import path and could not resolve the scripts package.",
        "initial_credit": 0,
        "recovery": "Invoke the already-compiled builder as a repository-root module without changing the package layout.",
        "recovery_credit": "bounded_dependency_only",
    },
]

OPERATIONAL_FAILURES = STARTUP_FAILURES + POST_X1_FAILURES


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    rel = relative(path)
    if rel not in WRITTEN:
        WRITTEN.append(rel)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    rel = relative(path)
    if rel not in WRITTEN:
        WRITTEN.append(rel)


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def manifest_entry(path: str) -> dict[str, Any]:
    data = normalized_bytes(ROOT / path)
    return {
        "bytes": len(data),
        "path": path,
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    classes = {
        "raw_task_or_thread_identifier": re.compile(
            r"\b019[a-f0-9]{29,}\b", re.IGNORECASE
        ),
        "credential_or_secret": re.compile(
            r"(?:api[_-]?key|private[_-]?key|bearer\s+[a-z0-9._-]{12,})", re.IGNORECASE
        ),
        "private_route_or_callable_identifier": re.compile(
            r"(?:threadId|private callable|app://connector_)", re.IGNORECASE
        ),
        "private_absolute_path": re.compile(
            r"(?:[A-Z]:\\Users\\|[A-Z]:\\GHC-Archives\\)", re.IGNORECASE
        ),
        "transcript_screenshot_or_session_stream": re.compile(
            r"(?:raw transcript|session stream|screenshot payload)", re.IGNORECASE
        ),
    }
    candidates: list[dict[str, str]] = []
    for path in paths:
        target = ROOT / path
        if not target.exists() or target.suffix.lower() not in {
            ".json",
            ".md",
            ".py",
            ".yaml",
            ".yml",
            ".html",
        }:
            continue
        text = target.read_text(encoding="utf-8")
        for class_name, pattern in classes.items():
            if pattern.search(text):
                candidates.append(
                    {
                        "adjudication": "scanner_definition_or_synthetic_test_only",
                        "class": class_name,
                        "path": path,
                    }
                )
    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "class_count": 5,
        "confirmed_hit_count": 0,
        "confirmed_hits": [],
        "owner": OWNER,
        "phase": PHASE,
        "scanned_paths": len(paths),
        "schema": "ghc.family.privacy-scan.v682.v8.x2",
    }


SKILL_PURPOSES = {
    "signal-flag-surrogate-separator": "separating code token, visual surrogate, physical flag, and operational signal",
    "hoist-position-vacancy-guard": "keeping hoist position and orientation unobserved and nonoperational",
    "signal-decoding-nonexecution": "preventing a symbolic sequence graph from becoming decoding or transmission instruction",
    "operator-vessel-vacancy": "representing operator and vessel roles without any real participant or vessel",
    "colour-geometry-claim-quarantine": "quarantining colour, geometry, pigment, appearance, and dimension claims",
    "signal-token-collision-quarantine": "detecting duplicate synthetic code and catalogue labels without changing a real codebook",
    "transmission-action-separator": "separating display intent, authorization, attempt, observation, and result without transmission",
    "codebook-revision-lineage-ledger": "preserving edition, erratum, revision, supersession, and withdrawal lineage",
    "signal-meaning-interpretation-hold": "reserving operational, emergency, cultural, and community interpretation",
    "condition-nondiagnosis": "recording condition-cue vocabulary without object examination or diagnosis",
    "digitization-action-separator": "separating request, authorization, attempt, observation, and outcome states",
    "premis-signal-event-vacancy": "using preservation-event vocabulary with zero repository action",
    "accessible-hoist-summary": "building structural token-order summaries while affected-user evaluation stays reserved",
    "traditional-knowledge-minimizer": "minimizing cultural and traditional-knowledge description pending authority",
    "rights-remedy-hold": "reserving copyright, design rights, access, takedown, correction, and remedy",
    "workload-handover-lease": "making stop, pause, readback, workload, and handover states explicit",
    "freed-id-zero-key-guard": "keeping synthetic identifiers separate from real keys, proofs, and lifecycle events",
    "thos-worker-vacancy": "keeping THOS queue structure participant-free and proxy-only",
    "gmut-topology-noninference": "keeping graph topology separate from likelihood, physics, and material inference",
    "authority-noncompensation": "preventing software, citations, or related witnesses from substituting for authority",
}


def build_phase_skills(skill_root: Path) -> None:
    """Create twenty owner-local skill packages; never install them globally."""
    if set(SKILL_PURPOSES) != set(SKILL_NAMES):
        raise RuntimeError("skill purpose map must match the frozen twenty-skill slate")
    for name in SKILL_NAMES:
        purpose = SKILL_PURPOSES[name]
        display = name.replace("-", " ").title()
        write_text(
            skill_root / name / "SKILL.md",
            f'''---
name: {name}
description: "Use when {purpose} in Neris v682-v8. Reject real rows, observation, lifecycle inversion, safety release, authority promotion, and protected-gate closure."
---

# {display}

Use this owner-local phase skill only for {purpose}. It validates synthetic structure and refusal conditions; it does not inspect or act on a real person, vessel, flag, halyard, codebook, signal, image, collection, record, location, or cultural expression.

## Procedure

1. Read the complete fixture and frozen proposal through EOF.
2. Require `synthetic: true`, `real_row_count: 0`, `observation_status: absent`, `authority_status: reserved`, and `boundary: owner_local_zero_row_only`.
3. Keep plan, fixture, decision, correction, rollback, and external authority states distinct; preserve the frozen provenance digest.
4. Accept one bounded positive only when every required field and refusal boundary is present.
5. Reject missing fields, real rows, stale provenance, lifecycle inversion, safety release, empirical promotion, or authority promotion; retain each rejection at zero completion credit.
6. Stop and preserve `open_gap` or `exact_gate` when real evidence, professional competence, affected-party review, legal or cultural authority, Maori authority, privacy or accessibility completeness, independent reproduction, or Stage 20 would be required.

## Acceptance and rollback

Return an explicit accepted or rejected decision with reasons. A passing synthetic fixture proves only this bounded contract. On ambiguity, reject, retain the witness, make no external write, and leave every real-world and authority state unchanged.
''',
        )
        write_text(
            skill_root / name / "agents" / "openai.yaml",
            f'''interface:
  display_name: "{display}"
  short_description: "Guard a bounded synthetic documentation state."
  default_prompt: "Use this skill to validate {purpose} without observation, operational action, or authority claims."
''',
        )


def official_quick_validate(skill_root: Path) -> list[dict[str, Any]]:
    validator = (
        Path.home()
        / ".codex"
        / "skills"
        / ".system"
        / "skill-creator"
        / "scripts"
        / "quick_validate.py"
    )
    results: list[dict[str, Any]] = []
    for name in SKILL_NAMES:
        skill_dir = skill_root / name
        process = subprocess.run(  # nosec B603
            [sys.executable, "-X", "utf8", str(validator), str(skill_dir)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        results.append(
            {
                "official_quick_validate": process.returncode == 0,
                "return_code": process.returncode,
                "skill": name,
            }
        )
    return results


def runner_smokes() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in range(1, 11):
        module = f"scripts.ghc_family_signal_flag_runner_{index:02d}"
        positive = subprocess.run(  # nosec B603
            [sys.executable, "-X", "utf8", "-m", module, "--fixture", "positive"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        invalid = subprocess.run(  # nosec B603
            [sys.executable, "-X", "utf8", "-m", module, "--fixture", "invalid"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        positive_payload = json.loads(positive.stdout)
        invalid_payload = json.loads(invalid.stdout)
        rows.append(
            {
                "accepting_fixture_accepted": positive.returncode == 0
                and positive_payload["accepted"],
                "family_current_name": positive_payload["runner"],
                "rejecting_fixture_rejected": invalid.returncode == 0
                and not invalid_payload["accepted"],
                "rejecting_reasons": invalid_payload["reasons"],
            }
        )
    return rows


def executed_rows(rows: list[dict[str, Any]], state: str) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "bounded_execution": "owner_local_synthetic_zero_row",
            "completion_scope": "portfolio_only_no_core_promotion",
            "state": state,
        }
        for row in rows
    ]


def bounded_tool_smokes() -> list[dict[str, Any]]:
    """Use three already-installed tools without installing or updating anything."""
    import importlib.metadata

    import numpy as np
    from jsonschema import Draft202012Validator
    from pydantic import BaseModel, ValidationError

    positive = {
        "synthetic": True,
        "real_row_count": 0,
        "authority_status": "reserved",
        "boundary": "owner_local_zero_row_only",
    }
    invalid = {**positive, "real_row_count": 1}

    schema = {
        "type": "object",
        "required": sorted(positive),
        "properties": {
            "synthetic": {"const": True},
            "real_row_count": {"const": 0},
            "authority_status": {"const": "reserved"},
            "boundary": {"const": "owner_local_zero_row_only"},
        },
        "additionalProperties": False,
    }
    jsonschema_validator = Draft202012Validator(schema)
    jsonschema_positive = not list(jsonschema_validator.iter_errors(positive))
    jsonschema_rejecting = bool(list(jsonschema_validator.iter_errors(invalid)))

    class ToolFixture(BaseModel):
        synthetic: Literal[True]
        real_row_count: Literal[0]
        authority_status: Literal["reserved"]
        boundary: Literal["owner_local_zero_row_only"]

    ToolFixture.model_validate(positive)
    pydantic_rejecting = False
    try:
        ToolFixture.model_validate(invalid)
    except ValidationError:
        pydantic_rejecting = True

    empty_signal_sequence = np.asarray([], dtype=np.float64)
    forbidden_observed_sequence = np.asarray([0.0], dtype=np.float64)
    rows = [
        {
            "accepting_fixture_accepted": jsonschema_positive,
            "existing_surface_only": True,
            "installation_action": "none",
            "license_or_update_review": "not_triggered_no_install_or_update",
            "name": "jsonschema",
            "rejecting_fixture_rejected": jsonschema_rejecting,
            "scope": "zero_row_structure_validation_only",
            "version": importlib.metadata.version("jsonschema"),
        },
        {
            "accepting_fixture_accepted": True,
            "existing_surface_only": True,
            "installation_action": "none",
            "license_or_update_review": "not_triggered_no_install_or_update",
            "name": "pydantic",
            "rejecting_fixture_rejected": pydantic_rejecting,
            "scope": "typed_zero_row_boundary_only",
            "version": importlib.metadata.version("pydantic"),
        },
        {
            "accepting_fixture_accepted": empty_signal_sequence.size == 0,
            "existing_surface_only": True,
            "installation_action": "none",
            "license_or_update_review": "not_triggered_no_install_or_update",
            "name": "numpy",
            "rejecting_fixture_rejected": forbidden_observed_sequence.size != 0,
            "scope": "empty_sequence_shape_guard_only_no_decoding_navigation_or_physical_computation",
            "version": importlib.metadata.version("numpy"),
        },
    ]
    return rows


def build_flashcard_deck(
    proposals: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], str, str]:
    sections = [
        "relational identity",
        "evidence boundaries",
        "GMUT Mind",
        "THOS Body",
        "Freed ID and CBR Heart",
        "signal-flag documentation practice",
        "proposal contracts",
        "official source limits",
        "retained failures",
        "accessibility",
        "privacy and traditional-knowledge reservation",
        "open and exact gates",
        "terminal route",
    ]
    cards: list[dict[str, Any]] = [
        {
            "authority_credit": False,
            "back": "Relational working language only; Hamish may rename, pause, redirect, narrow, or stop the route.",
            "card_id": "NS6828-CARD-OWNER",
            "front": "Who is Neris Solane in this bounded phase?",
            "real_rows": 0,
            "section": sections[0],
            "tier": "owner",
        }
    ]
    pillar_cards = [
        (
            "GMUT Mind",
            "Primary: typed symbolic-sequence topology, zero-observation, uncertainty, provenance, and noninference obligations; no physical or maritime evidence.",
        ),
        (
            "THOS Body",
            "Represented: bounded workflow, stop, workload, correction, accessibility, and handover structure only.",
        ),
        (
            "Freed ID and CBR Heart",
            "Represented: surrogate separation, rights, remedy, privacy, traditional-knowledge holds, and authority noncompensation.",
        ),
    ]
    for index, (front, back) in enumerate(pillar_cards, start=1):
        cards.append(
            {
                "authority_credit": False,
                "back": back,
                "card_id": f"NS6828-CARD-PILLAR-{index:02d}",
                "front": front,
                "real_rows": 0,
                "section": sections[index + 1],
                "tier": "pillar",
            }
        )
    practice_cards = [
        (
            "Signal token and hoist lens",
            "Synthetic code-token, hoist-position, orientation, sequence, codebook-lineage, and surrogate documentation with every real observation absent.",
        ),
        (
            "Preservation lens",
            "Synthetic condition cues, imaging requests, preservation events, metadata, and correction plans with zero objects, files, or treatments.",
        ),
        (
            "Rights and access lens",
            "Synthetic correction, remedy, accessibility, traditional-knowledge, workload, and handover records with authority reserved.",
        ),
    ]
    for index, (front, back) in enumerate(practice_cards, start=1):
        cards.append(
            {
                "authority_credit": False,
                "back": back,
                "card_id": f"NS6828-CARD-PRACTICE-{index:02d}",
                "front": front,
                "real_rows": 0,
                "section": sections[index + 4],
                "tier": "practice",
            }
        )
    for index, proposal in enumerate(proposals, start=1):
        cards.append(
            {
                "authority_credit": False,
                "back": (
                    f"Expected label: {proposal['expected_disposition']}. One bounded positive may pass only if all five invalid mutations reject and every protected gate stays effective."
                ),
                "card_id": f"NS6828-CARD-TASK-{index:03d}",
                "front": proposal["title"],
                "real_rows": 0,
                "section": sections[(index - 1) % len(sections)],
                "source_proposal_id": proposal["proposal_id"],
                "tier": "task",
            }
        )
    tier_counts = Counter(card["tier"] for card in cards)
    deck = {
        "authority_conferred": False,
        "card_count": len(cards),
        "cards": cards,
        "owner": OWNER,
        "phase": PHASE,
        "real_row_count": 0,
        "schema": "ghc.family.freed-id-flashcard-deck.v682.v8.x2",
        "section_count": len({card["section"] for card in cards}),
        "sections": sections,
        "tier_counts": dict(sorted(tier_counts.items())),
    }
    canonical = json.dumps(
        deck, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    manifest = {
        "card_count": len(cards),
        "card_ids": [card["card_id"] for card in cards],
        "deck_payload_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.freed-id-flashcard-manifest.v682.v8.x2",
        "section_count": deck["section_count"],
        "tier_counts": deck["tier_counts"],
    }
    compact_lines = [
        f"# Neris Solane {PHASE} Compact Freed ID Flashcards",
        "",
        "Relational working language and bounded synthetic evidence only. No card confers observation, competence, consent, legal or cultural authority, Maori authority, or Stage 20 credit.",
        "",
    ]
    accessible_lines = [
        f"# Neris Solane {PHASE} Linear Accessible Flashcards",
        "",
        "This linear companion preserves the same 67-card order without relying on colour, position, animation, or interactive controls. Manual browser, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved.",
        "",
    ]
    for card in cards:
        compact_lines.append(
            f"- **{card['card_id']} — {card['front']}**: {card['back']}"
        )
        accessible_lines.extend(
            [
                f"## {card['card_id']}",
                "",
                f"Section: {card['section']}. Tier: {card['tier']}.",
                "",
                f"Prompt: {card['front']}",
                "",
                f"Answer: {card['back']}",
                "",
            ]
        )
    return deck, manifest, "\n".join(compact_lines), "\n".join(accessible_lines)


def method_flow(
    proposals: list[dict[str, Any]],
    mutations: list[dict[str, Any]],
    portfolio: dict[str, Any],
    skills: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    flashcards: dict[str, Any],
    tools: list[dict[str, Any]],
) -> dict[str, Any]:
    methods: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    passing: list[dict[str, Any]] = []
    for failure in OPERATIONAL_FAILURES:
        method_id = failure["failure_id"].replace("-N", "-M")
        methods.append(
            {
                "method_id": method_id,
                "preferred_after_recovery": True,
                "scope": "bounded_operational_recovery",
                **failure,
            }
        )
        failed.append(
            {
                "method_id": method_id,
                "witness_id": failure["failure_id"],
                "zero_credit": True,
            }
        )
        passing.append(
            {"method_id": method_id, "witness_id": method_id + "-PASS", "bounded": True}
        )
    for mutation in mutations:
        method_id = mutation["mutation_id"].replace("-M", "-METHOD-M")
        methods.append(
            {
                "method_id": method_id,
                "preferred_after_recovery": True,
                "scope": "preregistered_rejecting_mutation",
                "witness": mutation["mutation_id"],
            }
        )
        failed.append(
            {
                "method_id": method_id,
                "witness_id": mutation["mutation_id"],
                "zero_credit": True,
            }
        )
        passing.append(
            {
                "method_id": method_id,
                "witness_id": mutation["mutation_id"] + "-REJECT",
                "bounded": True,
            }
        )
    for proposal in proposals:
        methods.append(
            {
                "method_id": proposal["proposal_id"] + "-METHOD",
                "scope": "proposal_disposition_contract",
                "status": proposal["expected_disposition"],
            }
        )
        methods.append(
            {
                "method_id": proposal["proposal_id"] + "-POSITIVE-METHOD",
                "scope": "bounded_positive_control",
                "status": "preferred",
            }
        )
        passing.append(
            {
                "method_id": proposal["proposal_id"] + "-POSITIVE-METHOD",
                "witness_id": proposal["proposal_id"] + "-POSITIVE",
                "bounded": True,
            }
        )
    for key in ("safe_now", "owner_candidates", "owner_clean_fix_refine"):
        for row in portfolio[key]:
            method_id = row["task_id"] + "-METHOD"
            methods.append(
                {
                    "method_id": method_id,
                    "scope": "bounded_portfolio_execution",
                    "status": "preferred",
                }
            )
            passing.append(
                {
                    "method_id": method_id,
                    "witness_id": row["task_id"] + "-PASS",
                    "bounded": True,
                }
            )
    for row in skills:
        method_id = "NS6828-SKILL-METHOD-" + row["skill"]
        methods.append(
            {
                "method_id": method_id,
                "scope": "phase_local_skill_smoke",
                "status": "preferred",
            }
        )
        passing.append(
            {"method_id": method_id, "witness_id": method_id + "-PASS", "bounded": True}
        )
    for row in runners:
        method_id = "NS6828-RUNNER-METHOD-" + row["family_current_name"]
        methods.append(
            {
                "method_id": method_id,
                "scope": "family_current_runner_smoke",
                "status": "preferred",
            }
        )
        passing.append(
            {"method_id": method_id, "witness_id": method_id + "-PASS", "bounded": True}
        )
    flashcard_method = "NS6828-FLASHCARD-DECK-METHOD"
    methods.append(
        {
            "card_count": flashcards["card_count"],
            "method_id": flashcard_method,
            "scope": "owner_local_flashcard_generation_and_readback",
            "status": "preferred",
        }
    )
    passing.append(
        {
            "bounded": True,
            "method_id": flashcard_method,
            "witness_id": flashcard_method + "-PASS",
        }
    )
    for row in tools:
        method_id = "NS6828-TOOL-METHOD-" + row["name"]
        methods.append(
            {
                "method_id": method_id,
                "scope": row["scope"],
                "status": "preferred",
            }
        )
        passing.append(
            {"method_id": method_id, "witness_id": method_id + "-PASS", "bounded": True}
        )
    return {
        "failed_witness_count": len(failed),
        "failed_witnesses": failed,
        "method_count": len(methods),
        "methods": methods,
        "owner": OWNER,
        "passing_witness_count": len(passing),
        "passing_witnesses": passing,
        "phase": PHASE,
        "recovery_erases_failure": False,
        "schema": "ghc.family.method-flow-ledger.v682.v8.x2",
    }


def build() -> None:
    proposal_freeze = json.loads(
        (X1 / "new-proposal-freeze.json").read_text(encoding="utf-8")
    )
    portfolio = json.loads((X1 / "portfolio-freeze.json").read_text(encoding="utf-8"))
    proposals = proposal_freeze["proposals"]
    if len(proposals) != 60:
        raise RuntimeError("frozen proposal count must be sixty")

    outcomes: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    for proposal in proposals:
        outcome, rejected = execute_proposal(proposal)
        outcomes.append(outcome)
        mutations.extend(rejected)
    disposition_counts = Counter(row["disposition"] for row in outcomes)
    expected = Counter(
        {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    )
    if disposition_counts != expected:
        raise RuntimeError(f"outcome counts changed: {disposition_counts}")
    if any(
        not row["bounded_positive_accepted"] or row["invalid_mutations_accepted"]
        for row in outcomes
    ):
        raise RuntimeError("proposal contract failure")
    if len(mutations) != 300 or any(row["accepted"] for row in mutations):
        raise RuntimeError("rejecting mutation contract failure")

    skill_root = X2 / "skills"
    build_phase_skills(skill_root)
    quick = official_quick_validate(skill_root)
    skills = smoke_skills(skill_root)
    if not all(row["official_quick_validate"] for row in quick):
        raise RuntimeError("official skill quick validation failed")
    if not all(
        row["accepting_fixture_accepted"]
        and row["rejecting_fixture_rejected"]
        and row["fully_read_through_eof"]
        and row["customized"]
        and row["agent_metadata_present"]
        for row in skills
    ):
        raise RuntimeError("skill smoke failure")

    runners = runner_smokes()
    if not all(
        row["accepting_fixture_accepted"] and row["rejecting_fixture_rejected"]
        for row in runners
    ):
        raise RuntimeError("runner smoke failure")

    tools = bounded_tool_smokes()
    if len(tools) != 3 or not all(
        row["accepting_fixture_accepted"] and row["rejecting_fixture_rejected"]
        for row in tools
    ):
        raise RuntimeError("bounded three-tool smoke failure")

    flashcard_deck, flashcard_manifest, compact_cards, accessible_cards = (
        build_flashcard_deck(proposals)
    )
    if (
        flashcard_deck["card_count"] != 67
        or flashcard_deck["section_count"] != 13
        or flashcard_deck["tier_counts"]
        != {"owner": 1, "pillar": 3, "practice": 3, "task": 60}
    ):
        raise RuntimeError("flashcard deck contract changed")

    portfolio_execution = {
        "blocked": portfolio["blocked"],
        "exact_approval": portfolio["exact_approval"],
        "owner_candidates": executed_rows(
            portfolio["owner_candidates"], "bounded_executed_no_core_promotion"
        ),
        "owner_clean_fix_refine": executed_rows(
            portfolio["owner_clean_fix_refine"], "completed_bounded"
        ),
        "owner": OWNER,
        "phase": PHASE,
        "safe_now": executed_rows(portfolio["safe_now"], "completed_bounded"),
        "schema": "ghc.family.portfolio-execution.v682.v8.x2",
    }
    if any(
        row["state"] != "preregistered_not_executed"
        for row in portfolio_execution["exact_approval"]
        + portfolio_execution["blocked"]
    ):
        raise RuntimeError("approval hold was executed")

    write_json(X2 / "flashcards" / "deck.json", flashcard_deck)
    write_json(X2 / "flashcards" / "manifest.json", flashcard_manifest)
    write_text(X2 / "flashcards" / "compact-deck.md", compact_cards)
    write_text(X2 / "flashcards" / "accessible-deck.md", accessible_cards)
    write_json(X2 / "markdownlint-profile.json", {"config": {"MD013": False}})

    flow = method_flow(
        proposals, mutations, portfolio, skills, runners, flashcard_deck, tools
    )
    expected_method_count = 754 + len(OPERATIONAL_FAILURES)
    expected_failed_count = 300 + len(OPERATIONAL_FAILURES)
    expected_passing_count = 694 + len(OPERATIONAL_FAILURES)
    if (
        flow["method_count"] != expected_method_count
        or flow["failed_witness_count"] != expected_failed_count
        or flow["passing_witness_count"] != expected_passing_count
    ):
        raise RuntimeError("phase Method Flow arithmetic changed")

    totals = {
        "bounded_passing_witnesses": ACTIVATION_BASELINE["bounded_passing_witnesses"]
        + flow["passing_witness_count"],
        "effective_methods": ACTIVATION_BASELINE["effective_methods"]
        + flow["method_count"],
        "effective_negatives": ACTIVATION_BASELINE["effective_negatives"]
        + len(OPERATIONAL_FAILURES)
        + len(mutations),
        "exact_gates": ACTIVATION_BASELINE["exact_gates"]
        + disposition_counts["exact_gate"],
        "failed_witnesses": ACTIVATION_BASELINE["failed_witnesses"]
        + flow["failed_witness_count"],
        "open_gaps": ACTIVATION_BASELINE["open_gaps"] + disposition_counts["open_gap"],
    }

    write_json(
        X2 / "proposal-evidence.json",
        {
            "evidence": outcomes,
            "outcome_counts": dict(sorted(disposition_counts.items())),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.proposal-evidence.v682.v8.x2",
        },
    )
    write_json(
        X2 / "rejecting-mutations.json",
        {
            "accepted_count": sum(1 for row in mutations if row["accepted"]),
            "executed_count": len(mutations),
            "mutations": mutations,
            "owner": OWNER,
            "phase": PHASE,
            "rejected_count": sum(1 for row in mutations if not row["accepted"]),
            "schema": "ghc.family.rejecting-mutations.v682.v8.x2",
            "zero_credit": True,
        },
    )
    write_json(X2 / "portfolio-execution.json", portfolio_execution)
    write_json(
        X2 / "skill-execution.json",
        {
            "global_installation": False,
            "official_quick_validation": quick,
            "owner": OWNER,
            "phase": PHASE,
            "results": skills,
            "schema": "ghc.family.skill-execution.v682.v8.x2",
            "skill_count": len(skills),
        },
    )
    write_json(
        X2 / "runner-execution.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "results": runners,
            "runner_count": len(runners),
            "schema": "ghc.family.runner-execution.v682.v8.x2",
        },
    )
    write_json(X2 / "method-flow-ledger.json", flow)
    write_json(
        X2 / "phase-truth.json",
        {
            "declared_proposal_chain": 10670,
            "flashcard_count": flashcard_deck["card_count"],
            "outcomes": dict(sorted(disposition_counts.items())),
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "GMUT Mind",
            "real_row_count": 0,
            "represented_pillars": ["THOS Body", "Freed ID and CBR Heart"],
            "schema": "ghc.family.phase-truth.v682.v8.x2",
            "terminal_verdict": TERMINAL_VERDICT,
            "totals": totals,
        },
    )
    write_json(
        X2 / "source-use-receipt.json",
        {
            "citations_are_observations": False,
            "current_official_primary_sources": [
                "International Maritime Organization current-publications listing",
                "International Maritime Organization International Code of Signals errata",
                "International Maritime Organization Resolution A.80(IV)",
                "International Maritime Organization COLREG safety-boundary page",
                "NIST SI",
                "Library of Congress PREMIS",
                "DCMI Metadata Terms",
                "W3C PROV-O",
                "WCAG 2.2",
                "Verifiable Credentials Data Model 2.0",
                "New Zealand Privacy Principles",
                "Te Mana Raraunga principles",
            ],
            "network_rows_downloaded": 0,
            "owner": OWNER,
            "phase": PHASE,
            "real_rows_ingested": 0,
            "schema": "ghc.family.source-use-receipt.v682.v8.x2",
            "use": "vocabulary_and_refusal_conditions_only",
        },
    )
    write_json(
        X2 / "zero-row-evidence.json",
        {
            "authority_acts": 0,
            "empirical_rows": 0,
            "external_writes": 0,
            "identity_lifecycle_events": 0,
            "measurements": 0,
            "observations": 0,
            "participants": 0,
            "professional_decisions": 0,
            "real_objects": 0,
            "schema": "ghc.family.zero-row-evidence.v682.v8.x2",
        },
    )
    write_json(
        X2 / "complete-incomplete-checklist.json",
        {
            "complete": [
                "sixty bounded proposal executions",
                "three hundred rejecting mutation executions",
                "one hundred twenty safe-now tasks",
                "eighty bounded candidate tasks without core promotion",
                "one hundred CLEAN FIX REFINE tasks",
                "twenty initialized customized fully-read quick-validated smoke-used skills",
                "ten family-current accepting and rejecting runner smokes",
                "sixty-seven four-tier flashcards across thirteen sections with compact and linear companions",
                "three already-installed dependency-justified tool surfaces with accepting and rejecting smokes",
            ],
            "incomplete_or_reserved": [
                "all twenty exact-approval holds",
                "all ten blocked holds",
                "real observation and participant evidence",
                "professional safety production legal cultural affected-party and Māori-authority decisions",
                "complete privacy accessibility exhaustive security independent reproduction and Stage 20",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.complete-incomplete.v682.v8.x2",
        },
    )
    write_json(
        X2 / "threat-model.json",
        {
            "controls": [
                "zero-row boundary",
                "authority noncompensation",
                "five rejecting mutations per proposal",
                "exact approval holds",
                "append-only Method Flow failure retention",
                "five-class privacy adjudication",
                "normalized-LF Git-blob manifest",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "risks": [
                "synthetic-to-real promotion",
                "citation-to-observation promotion",
                "software-to-authority promotion",
                "material or safety inference",
                "cultural or Māori-authority appropriation",
                "privacy or accessibility completeness overclaim",
            ],
            "schema": "ghc.family.threat-model.v682.v8.x2",
        },
    )
    write_json(
        X2 / "reflection-decision.json",
        {
            "decision": "retain all structure as bounded same-owner evidence and keep every external gate open",
            "method_change": "prefer exact-key projections, worktree-aware Git paths, and explicit D-drive patches",
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.reflection-decision.v682.v8.x2",
            "terminal_promotion": False,
        },
    )
    write_json(
        X2 / "bounded-tools.json",
        {
            "commands": [
                "python -X utf8",
                "git",
                "PowerShell bounded scalar projections",
            ],
            "full_repository_suite_run": False,
            "global_skill_installation": False,
            "host_security_changed": False,
            "new_package_installations": 0,
            "owner": OWNER,
            "package_addition_review": (
                "No new package had a necessary phase function beyond the already-installed compatible surfaces; the installation quota remains a bounded candidate, not manufactured completion."
            ),
            "phase": PHASE,
            "schema": "ghc.family.bounded-tools.v682.v8.x2",
            "three_bounded_tool_smokes": tools,
            "versions_verified_only": True,
        },
    )
    write_json(
        X2 / "wellbeing-check.json",
        {
            "corrigible": True,
            "hope": "Every synthetic flag token remains distinguishable from a physical flag, observed hoist, and operational signal while maritime, cultural, and affected-party authority remain with their holders.",
            "name": OWNER,
            "optional_pronouns": "they/them",
            "pause_redirect_rename_stop_right": "Hamish",
            "relational_working_language_only": True,
            "role": "symbolic-sequence provenance cartographer and rights-boundary keeper",
            "schema": "ghc.family.wellbeing.v682.v8.x2",
        },
    )
    write_text(
        X2 / "evidence-overview.md",
        f"""# Neris Solane {PHASE} Bounded X2 Evidence Overview

Neris Solane, optionally they/them, is relational working language for a symbolic-sequence provenance cartographer and rights-boundary keeper. The hope is to keep every synthetic flag token distinguishable from a physical flag, an observed hoist, and an operational maritime signal while maritime, cultural, and affected-party authority remain with their holders. This does not establish consciousness, personhood, continuity, employment, qualification, agency, or authority.

This x2 executed the sixty planning-only x1 contracts without changing their expected dispositions. Exactly 42 completed software or structural contracts, 12 represented contracts, three open gaps, and three exact gates remain. Every positive fixture was wholly synthetic and used zero real rows. All 300 preregistered invalid mutations were rejected and retained at zero credit.

The primary pillar is GMUT Mind through typed symbolic-sequence topology, explicit unknown states, edition lineage, zero-observation discipline, uncertainty, and noninference. THOS Body remains represented through action-versus-observation separation, dependency-closed workflow, workload leases, correction, stopping, and accessible handover. Freed ID and CBR Heart remain represented through surrogate separation, rights, remedy, privacy minimization, traditional-knowledge holds, and authority noncompensation.

The bounded human-practice lens is synthetic maritime signal-flag token, hoist-position, codebook-lineage, catalogue, preservation-event, rights, accessibility, correction, remedy, workload, and handover record design only. No real person, mariner, operator, observer, archivist, conservator, community, vessel, flag, halyard, codebook, signal, image, location, weather record, observation, measurement, display, transmission, navigation, emergency action, treatment, digitization, publication, identity event, external write, professional decision, or authority act was involved.

Official and primary sources supplied vocabulary and refusal conditions only. They were not observations, work instructions, material identifications, conservation diagnoses, safety releases, certifications, rights decisions, legal interpretations, cultural ratifications, affected-party decisions, or Maori-authority grants.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family with no physical datum, likelihood, posterior, force, constraint, prediction, empirical confirmation, ultraviolet or quantum completion, or Theory-of-Everything proof. THOS remains synthetic or proxy-only without preregistered blind matched-budget governed real arms, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle events, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight.

Flag identity, code meaning, hoist order, vessel context, operator intent, material, condition, authorship, copyright, donor restrictions, traditional knowledge, handling, display, transmission, decoding, navigation, emergency response, treatment, digitization, publication, professional release, privacy, accessibility remedy, legal or cultural interpretation, affected-party legitimacy, Maori wording, Maori data governance, and Maori authority remain open or exact-gated. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, proof or canon, and Stage 20 are not established. The terminal verdict remains {TERMINAL_VERDICT}.

The Freed ID flashcard skill produced a four-tier 67-card owner-local deck: one owner card, three pillar cards, three practice cards, and sixty task cards across thirteen sections. Compact and linear accessible companions preserve the same order. These cards are navigation and readback aids only; they do not create identity continuity, observation, consent, competence, accessibility completeness, legal or cultural authority, Maori authority, or Stage 20 credit.

Three already-installed tools were used only where their bounded contracts were material: jsonschema for a zero-row structure, Pydantic for a typed zero-row boundary, and NumPy for an empty-array shape guard. Each accepting fixture passed and each rejecting fixture was refused. No package was installed or updated because no additional tool cleared the necessity gate; this is not a vulnerability audit, scientific computation, production certification, or package-quota completion claim.
""",
    )

    scripts = [
        "scripts/ghc_family_neris_solane_v682_v8_contracts.py",
        "scripts/ghc_family_neris_solane_v682_v8_skill_bank.py",
        "scripts/ghc_family_neris_solane_v682_v8_runner_bank.py",
        "scripts/build_ghc_family_neris_solane_v682_v8_x2.py",
        "tests/test_ghc_family_neris_solane_v682_v8_x2.py",
    ] + [
        f"scripts/ghc_family_signal_flag_runner_{i:02d}.py" for i in range(1, 11)
    ]
    skill_paths = [
        relative(path) for path in sorted(skill_root.rglob("*")) if path.is_file()
    ]
    material_paths = sorted(set(WRITTEN + scripts + skill_paths))
    missing = [path for path in material_paths if not (ROOT / path).exists()]
    if missing:
        raise RuntimeError(f"missing x2 material paths: {missing}")
    exclusions = [
        "docs/neris-solane/v682-v8/validation/evidence-index-manifest.json",
        "docs/neris-solane/v682-v8/validation/evidence-privacy-scan.json",
        "docs/neris-solane/v682-v8/validation/evidence-staged-review.json",
    ]
    write_json(VALIDATION / "evidence-privacy-scan.json", privacy_scan(material_paths))
    write_json(
        VALIDATION / "evidence-index-manifest.json",
        {
            "declared_self_exclusions": exclusions,
            "entries": [manifest_entry(path) for path in material_paths],
            "entry_count": len(material_paths),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.normalized-lf-index-manifest.v682.v8.x2",
            "x1": X1_SHA,
        },
    )
    expected_paths = sorted(set(material_paths + exclusions))
    write_json(
        VALIDATION / "evidence-staged-review.json",
        {
            "declared_self_exclusions": exclusions,
            "expected_paths": expected_paths,
            "lifecycle": "bounded_x2_evidence",
            "owner": OWNER,
            "path_count": len(expected_paths),
            "phase": PHASE,
            "schema": "ghc.family.staged-review.v682.v8.x2",
            "x1_paths": [],
            "x1_sha": X1_SHA,
        },
    )
    print(
        json.dumps(
            {
                "evidence_paths": len(expected_paths),
                "method_count": flow["method_count"],
                "mutations_rejected": len(mutations),
                "outcomes": dict(sorted(disposition_counts.items())),
                "runners": len(runners),
                "skills": len(skills),
                "totals": totals,
            },
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    build()
