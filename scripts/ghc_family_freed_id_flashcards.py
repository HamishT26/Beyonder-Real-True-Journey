#!/usr/bin/env python3
"""Build and validate bounded GHC Freed ID flashcard decks.

The runner is owner-delta scoped. It never enumerates sibling worktrees, deletes
history, sends a task message, or converts relational labels into identity,
personhood, qualification, or authority evidence.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import html
import json
import os
import re
import sys
from collections import Counter, defaultdict, deque
from collections.abc import Iterable
from pathlib import Path, PurePosixPath
from typing import Any

SCHEMA = "ghc.family.freed-id-flashcards.v1"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
ALLOWED_TYPES = {"freed_id_anchor", "trinity_pillar", "bounded_practice", "task"}
TIER_FOR_TYPE = {
    "freed_id_anchor": 1,
    "trinity_pillar": 2,
    "bounded_practice": 3,
    "task": 4,
}
REQUIRED_SECTIONS = [
    "identity-and-corrigibility",
    "route-and-authority",
    "source-anchors",
    "x1-proposals",
    "trinity-pillars",
    "bounded-practice",
    "task-cards",
    "method-flow-and-negatives",
    "open-gaps-and-exact-gates",
    "validation-and-manifests",
    "wellbeing-and-workload",
    "successor-recommendations",
    "compact-baton-index",
]
PORTFOLIO_GROUPS = [
    "owner_safe_now",
    "successor_safe_now_recommendations",
    "owner_candidates",
    "successor_candidate_recommendations",
    "exact_approval_packets",
    "blocked_packets",
    "owner_skill_ideas",
    "successor_skill_recommendations",
    "owner_runner_ideas",
    "successor_runner_recommendations",
    "owner_clean_fix_refine",
    "successor_clean_fix_refine_recommendations",
]


class FlashcardError(ValueError):
    pass


def duplicate_guard(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise FlashcardError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=duplicate_guard)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FlashcardError(f"unable to parse {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise FlashcardError(f"top-level JSON must be an object: {path.name}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def digest_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not normalized:
        raise FlashcardError("unable to derive a card slug")
    return normalized[:96]


def safe_relative(value: str) -> str:
    value = value.replace("\\", "/").strip()
    pure = PurePosixPath(value)
    if not value or pure.is_absolute() or ".." in pure.parts or re.match(r"^[A-Za-z]:", value):
        raise FlashcardError(f"unsafe relative path: {value}")
    return pure.as_posix()


def ensure_under(root: Path, candidate: Path) -> Path:
    resolved_root = root.resolve()
    resolved = candidate.resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise FlashcardError("output must remain inside the declared repository") from exc
    current = resolved_root
    for part in resolved.relative_to(resolved_root).parts[:-1]:
        current = current / part
        if current.exists() and current.is_symlink():
            raise FlashcardError("symlinked output parent is not allowed")
    return resolved


def write_equal_or_new(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise FlashcardError(f"refusing symlinked output leaf: {path.name}")
    if path.exists():
        if not path.is_file() or path.read_bytes() != raw:
            raise FlashcardError(f"refusing to overwrite divergent output: {path.name}")
        return
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags, 0o600)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except (FileExistsError, OSError) as exc:
        raise FlashcardError(f"exclusive output collision: {path.name}") from exc


def private_candidates(text: str) -> list[str]:
    patterns = {
        "private_absolute_path": re.compile(r"(?i)(?:[A-Z]:" + r"\\(?:Users|GHC-Archives)\\|/(?:home|Users)/)"),
        "raw_uuid_or_identifier": re.compile(
            r"(?i)(?:\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b|\"(?:"
            + "task"
            + r"|thread|session|agent)_id\"\s*:)"
        ),
        "credential_or_private_key": re.compile(
            r"(?i)(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\"(?:password|api"
            + r"_key|access_token|resume_token)\"\s*:\s*\")"
        ),
        "private_route": re.compile(r"(?i)(?:codex" + r"://|vscode" + r"://|app" + r"://connector_[0-9a-f]+)"),
        "raw_transcript_or_app_state": re.compile(
            r"(?i)\"(?:raw_" + r"transcript|session_stream|private_app_state|browser_route)\"\s*:"
        ),
    }
    return sorted(label for label, pattern in patterns.items() if pattern.search(text))


def card(
    card_id: str,
    tier: int,
    card_type: str,
    title: str,
    parents: list[str],
    phase: str,
    owner: str,
    stability: str,
    content: dict[str, Any],
    *,
    outcome: str = "represented",
    source_refs: Iterable[str] = (),
    protected_gates: Iterable[str] = (),
) -> dict[str, Any]:
    return {
        "schema": f"{SCHEMA}.card",
        "card_id": card_id,
        "tier": tier,
        "card_type": card_type,
        "title": title,
        "parent_ids": parents,
        "owner": owner,
        "phase": phase,
        "stability": stability,
        "outcome": outcome,
        "content": content,
        "source_refs": sorted(set(source_refs)),
        "protected_gates": sorted(set(protected_gates)),
        "relational_boundary": "Working-language record only; not consciousness, personhood, identity continuity, qualification, or authority evidence.",
    }


def portfolio_outcome(group: str, row: dict[str, Any]) -> str:
    outcome = row.get("expected_execution_disposition")
    if outcome not in ALLOWED_OUTCOMES:
        raise FlashcardError(f"portfolio group {group} has an invalid frozen disposition")
    return outcome


def build_model(phase_root: Path, x1_head: str) -> dict[str, Any]:
    global REQUIRED_SECTIONS
    charter = strict_json(phase_root / "x1" / "phase-charter.json")
    proposals = strict_json(phase_root / "x1" / "proposal-freeze.json")
    portfolio = strict_json(phase_root / "x1" / "portfolio-freeze.json")
    architecture = strict_json(phase_root / "x1" / "flashcard-architecture-freeze.json")
    source = strict_json(phase_root / "x1" / "source-verification.json")
    if not re.fullmatch(r"[0-9a-f]{40}", x1_head):
        raise FlashcardError("x1 head must be one exact lowercase Git object id")
    frozen_sections = architecture.get("required_deck_sections")
    base_sections = list(REQUIRED_SECTIONS)
    if (
        not isinstance(frozen_sections, list)
        or len(frozen_sections) < 10
        or len(frozen_sections) != len(set(frozen_sections))
        or any(not isinstance(value, str) or not value for value in frozen_sections)
        or [value for value in frozen_sections if value in base_sections] != base_sections
    ):
        raise FlashcardError("x1 deck sections must preserve the family-current base order and contain at least ten unique labels")
    REQUIRED_SECTIONS = list(frozen_sections)
    phase = charter.get("display_phase") or charter["canonical_phase_id"]
    owner = charter["owner"]
    if architecture.get("owner") != owner or architecture.get("phase") != phase:
        raise FlashcardError("flashcard architecture owner or phase differs from the charter")
    current_route = architecture.get("current_route")
    successor_route = architecture.get("successor_route")
    if not isinstance(current_route, dict) or current_route.get("owner") != owner or current_route.get("phase") != phase:
        raise FlashcardError("current route differs from the frozen owner and phase")
    if not isinstance(successor_route, dict) or successor_route.get("contacted") is not False:
        raise FlashcardError("successor route must remain frozen and uncontacted")
    successor_label = successor_route.get("owner") or successor_route.get("title")
    if not isinstance(successor_label, str) or not successor_label.strip() or not isinstance(successor_route.get("phase"), str):
        raise FlashcardError("successor route needs an owner or title label and one phase")
    owner_slug = slug(owner)
    gates = proposals["new_proposals"][0]["protected_gates"]
    owner_id = f"ghc-card-owner-{owner_slug}"
    freed_id_pillar = "ghc-card-pillar-freed-id-cbr-heart"
    cards: list[dict[str, Any]] = [
        card(
            owner_id,
            1,
            "freed_id_anchor",
            f"{owner} relational anchor",
            [],
            phase,
            owner,
            "stable",
            {
                "role": charter["relational_role"],
                "hope": charter["hope"],
                "optional_pronouns": charter["optional_pronouns"],
                "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
                "identity_boundary": charter["identity_boundary"],
            },
            source_refs=[source["source_exact_final"], x1_head],
            protected_gates=gates,
        )
    ]
    pillar_specs = [
        ("gmut-mind", "GMUT Mind", "Typed scalar-tensor and EFT research-model family; no empirical, force, prediction, constraint, proof, canon, or Theory-of-Everything claim."),
        ("thos-body", "THOS Body", "Synthetic protocol only; no governed participants, blind matched-budget real arms, operational effectiveness, deployment, AGI, ASI, consciousness, or personhood evidence."),
        ("freed-id-cbr-heart", "Freed ID and CBR Heart", "Synthetic nonproduction identity and rights design; real keys, proofs, lifecycle, privacy, security, trust governance, affected-party, legal, cultural, and Maori authority remain gated."),
    ]
    for key, title, boundary in pillar_specs:
        cards.append(
            card(
                f"ghc-card-pillar-{key}",
                2,
                "trinity_pillar",
                title,
                [owner_id],
                phase,
                owner,
                "stable",
                {
                    "boundary": boundary,
                    "primary": (
                        (key == "gmut-mind" and "gmut" in charter["primary_pillar"].lower())
                        or (key == "thos-body" and "thos" in charter["primary_pillar"].lower())
                        or (key == "freed-id-cbr-heart" and "freed id" in charter["primary_pillar"].lower())
                    ),
                },
                protected_gates=gates,
            )
        )
    practice_id = f"ghc-card-practice-{slug(charter['bounded_practice'])}"
    practice_parent = (
        "ghc-card-pillar-thos-body"
        if "thos" in charter["primary_pillar"].lower()
        else freed_id_pillar
    )
    cards.append(
        card(
            practice_id,
            3,
            "bounded_practice",
            charter["bounded_practice"],
            [practice_parent],
            phase,
            owner,
            "volatile",
            {
                "scope": charter["bounded_practice"],
                "boundary": charter["practice_boundary"],
                "real_records_used": 0,
                "professional_decisions_made": 0,
            },
            protected_gates=gates,
        )
    )

    proposal_card_ids: list[str] = []
    new_proposal_card_ids: list[str] = []
    for inherited in proposals["selected_inherited"]:
        card_id = f"ghc-card-{slug(inherited['program_row_id'])}"
        proposal_card_ids.append(card_id)
        cards.append(
            card(
                card_id,
                4,
                "task",
                inherited["source_title"],
                [practice_id],
                phase,
                owner,
                "volatile",
                {
                    "program_class": "selected_inherited_revalidation",
                    "source_proposal_id": inherited["source_proposal_id"],
                    "hypothesis": inherited["hypothesis"],
                    "null_or_failure_condition": inherited["null_or_failure_condition"],
                    "approval_class": inherited["approval_class"],
                    "execution_lane": inherited["execution_lane"],
                    "concrete_artifacts": inherited["concrete_artifacts"],
                    "falsifier_or_acceptance_gate": inherited["falsifier_or_acceptance_gate"],
                    "rollback_or_recovery": inherited["rollback_or_recovery"],
                    "novelty_credit": False,
                    "automatic_completion_credit": False,
                },
                outcome=inherited["expected_disposition"],
                source_refs=[inherited["source_proposal_id"]],
                protected_gates=inherited["protected_gates"],
            )
        )
    for new in proposals["new_proposals"]:
        card_id = f"ghc-card-{slug(new['proposal_id'])}"
        proposal_card_ids.append(card_id)
        new_proposal_card_ids.append(card_id)
        cards.append(
            card(
                card_id,
                4,
                "task",
                new["title"],
                [practice_id],
                phase,
                owner,
                "volatile",
                {
                    "program_class": "genuinely_new_core_proposal",
                    "proposal_id": new["proposal_id"],
                    "hypothesis": new["hypothesis"],
                    "null_or_failure_condition": new["null_or_failure_condition"],
                    "approval_class": new["approval_class"],
                    "execution_lane": new["execution_lane"],
                    "official_or_primary_source_needs": new["current_official_or_primary_source_needs"],
                    "concrete_artifacts": new["concrete_artifacts"],
                    "falsifier_or_acceptance_gate": new["falsifier_or_acceptance_gate"],
                    "rollback_or_recovery": new["rollback_or_recovery"],
                    "novelty_credit": True,
                },
                outcome=new["expected_disposition"],
                source_refs=[new["proposal_id"]],
                protected_gates=new["protected_gates"],
            )
        )

    portfolio_ids: dict[str, list[str]] = defaultdict(list)
    for group in PORTFOLIO_GROUPS:
        rows = portfolio.get(group)
        if not isinstance(rows, list):
            raise FlashcardError(f"missing portfolio group: {group}")
        for index, row in enumerate(rows, 1):
            card_id = f"ghc-card-{slug(row['portfolio_ref'])}"
            portfolio_ids[group].append(card_id)
            cards.append(
                card(
                    card_id,
                    4,
                    "task",
                    row["title"],
                    [practice_id],
                    phase,
                    owner,
                    "volatile",
                    {
                        "program_class": group,
                        "portfolio_ref": row["portfolio_ref"],
                        "approval_class": row["approval_class"],
                        "execution_lane": row["execution_lane"],
                        "expected_execution_disposition": row["expected_execution_disposition"],
                        "credit_boundary": row["credit_boundary"],
                        "observed_evidence_boundary": "Evidence is limited to the generated card, runner behavior, fixtures, or explicit representation recorded in this remaster.",
                    },
                    outcome=portfolio_outcome(group, row),
                    source_refs=[row["portfolio_ref"]],
                    protected_gates=gates,
                )
            )

    section_anchor_ids: dict[str, str] = {}
    for section in REQUIRED_SECTIONS:
        card_id = f"ghc-card-section-{slug(section)}"
        section_anchor_ids[section] = card_id
        cards.append(
            card(
                card_id,
                4,
                "task",
                f"Deck section anchor: {section}",
                [practice_id],
                phase,
                owner,
                "volatile",
                {
                    "program_class": "navigation_anchor",
                    "section": section,
                    "completion_credit": 0,
                    "purpose": "Provide deterministic modular loading without replacing underlying evidence.",
                },
                outcome="represented",
                protected_gates=gates,
            )
        )

    sections: list[dict[str, Any]] = []
    exact_and_blocked = portfolio_ids["exact_approval_packets"] + portfolio_ids["blocked_packets"]
    successor = [
        card_id
        for group in PORTFOLIO_GROUPS
        if group.startswith("successor_")
        for card_id in portfolio_ids[group]
    ]
    owner_tasks = [
        card_id
        for group in PORTFOLIO_GROUPS
        if group.startswith("owner_")
        for card_id in portfolio_ids[group]
    ]
    section_cards = {
        "identity-and-corrigibility": [owner_id],
        "route-and-authority": [section_anchor_ids["route-and-authority"], *exact_and_blocked],
        "source-anchors": [section_anchor_ids["source-anchors"], owner_id],
        "x1-proposals": proposal_card_ids,
        "trinity-pillars": [f"ghc-card-pillar-{key}" for key, _, _ in pillar_specs],
        "bounded-practice": [practice_id],
        "task-cards": owner_tasks,
        "method-flow-and-negatives": [section_anchor_ids["method-flow-and-negatives"], *portfolio_ids["owner_runner_ideas"][:1]],
        "open-gaps-and-exact-gates": [section_anchor_ids["open-gaps-and-exact-gates"], *exact_and_blocked],
        "validation-and-manifests": [section_anchor_ids["validation-and-manifests"], *portfolio_ids["owner_safe_now"][-7:]],
        "wellbeing-and-workload": [section_anchor_ids["wellbeing-and-workload"], *portfolio_ids["owner_candidates"][9:11]],
        "successor-recommendations": [section_anchor_ids["successor-recommendations"], *successor],
        "compact-baton-index": [section_anchor_ids["compact-baton-index"]],
    }
    for section in REQUIRED_SECTIONS:
        section_cards.setdefault(section, [section_anchor_ids[section]])
    for section in REQUIRED_SECTIONS:
        sections.append({"section": section, "card_ids": list(dict.fromkeys(section_cards[section]))})

    stable = [owner_id, *[f"ghc-card-pillar-{key}" for key, _, _ in pillar_specs]]
    all_ids = [row["card_id"] for row in cards]
    expected_tier4 = (
        len(proposals["selected_inherited"])
        + len(proposals["new_proposals"])
        + sum(len(portfolio[group]) for group in PORTFOLIO_GROUPS)
        + len(REQUIRED_SECTIONS)
    )
    model = {
        "cards": cards,
        "new_proposal_card_ids": new_proposal_card_ids,
        "index": {
            "schema": f"{SCHEMA}.deck-index",
            "owner": owner,
            "phase": phase,
            "display_phase": charter["display_phase"],
            "source_exact_final": source["source_exact_final"],
            "x1_head": x1_head,
            "card_order": sorted(all_ids, key=lambda value: (next(row["tier"] for row in cards if row["card_id"] == value), value)),
            "tier_counts": dict(sorted(Counter(row["tier"] for row in cards).items())),
            "expected_tier_counts": {"1": 1, "2": 3, "3": 1, "4": expected_tier4},
            "card_count": len(cards),
            "new_core_outcomes": dict(sorted(Counter(row["outcome"] for row in cards if row["card_id"] in new_proposal_card_ids).items())),
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "bounded_practice": charter["bounded_practice"],
            "primary_pillar": charter["primary_pillar"],
            "current_route": current_route,
            "successor_route": successor_route,
            "phase_root": f"docs/{owner_slug}/{phase}",
        },
        "stable_prefix": {
            "schema": f"{SCHEMA}.stable-prefix",
            "ordering_basis": "static relational and scientific boundaries before volatile phase work",
            "card_ids": stable,
            "exact_prefix_required_for_cache_reuse": True,
            "cache_effect_measured": False,
        },
        "volatile_index": {
            "schema": f"{SCHEMA}.volatile-index",
            "card_ids": [value for value in all_ids if value not in stable],
            "lazy_loading_required": True,
            "presence_grants_completion": False,
        },
        "baton_index": {
            "schema": f"{SCHEMA}.baton-index",
            "section_count": len(sections),
            "sections": sections,
            "detailed_baton_mode": "modular_cards",
            "live_message_mode": "compact_pointer",
        },
    }
    return model


def validate_model(model: dict[str, Any]) -> dict[str, Any]:
    cards = model.get("cards")
    issues: list[str] = []
    if not isinstance(cards, list):
        raise FlashcardError("model cards must be a list")
    by_id: dict[str, dict[str, Any]] = {}
    for row in cards:
        if not isinstance(row, dict):
            issues.append("non-object card")
            continue
        card_id = row.get("card_id")
        if not isinstance(card_id, str) or not re.fullmatch(r"ghc-card-[a-z0-9-]+", card_id):
            issues.append("invalid card id")
            continue
        if card_id in by_id:
            issues.append(f"duplicate card id: {card_id}")
        by_id[card_id] = row
        card_type = row.get("card_type")
        tier = row.get("tier")
        if card_type not in ALLOWED_TYPES or TIER_FOR_TYPE.get(card_type) != tier:
            issues.append(f"type or tier mismatch: {card_id}")
        if row.get("outcome") not in ALLOWED_OUTCOMES:
            issues.append(f"invalid outcome: {card_id}")
        if private_candidates(json.dumps(row, ensure_ascii=False)):
            issues.append(f"private material candidate: {card_id}")
    for card_id, row in by_id.items():
        parents = row.get("parent_ids")
        if not isinstance(parents, list):
            issues.append(f"invalid parent list: {card_id}")
            continue
        if row["tier"] == 1 and parents:
            issues.append(f"tier one card has parent: {card_id}")
        if row["tier"] > 1 and len(parents) != 1:
            issues.append(f"non-root card must have one parent: {card_id}")
        for parent in parents:
            if parent not in by_id:
                issues.append(f"missing parent: {card_id}")
            elif by_id[parent]["tier"] != row["tier"] - 1:
                issues.append(f"parent tier mismatch: {card_id}")

    indegree = {card_id: 0 for card_id in by_id}
    children: dict[str, list[str]] = defaultdict(list)
    for card_id, row in by_id.items():
        for parent in row.get("parent_ids", []):
            if parent in by_id:
                indegree[card_id] += 1
                children[parent].append(card_id)
    queue = deque(sorted(card_id for card_id, degree in indegree.items() if degree == 0))
    order: list[str] = []
    while queue:
        current = queue.popleft()
        order.append(current)
        for child in sorted(children[current]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(order) != len(by_id):
        issues.append("card dependency cycle")

    index = model.get("index", {})
    declared = index.get("card_order", [])
    if set(declared) != set(by_id) or len(declared) != len(by_id):
        issues.append("deck index card set mismatch")
    stable = model.get("stable_prefix", {}).get("card_ids", [])
    volatile = model.get("volatile_index", {}).get("card_ids", [])
    if set(stable) & set(volatile) or set(stable) | set(volatile) != set(by_id):
        issues.append("stable and volatile partition mismatch")
    sections = model.get("baton_index", {}).get("sections", [])
    section_names = [row.get("section") for row in sections if isinstance(row, dict)]
    if (
        len(section_names) < 10
        or len(section_names) != len(set(section_names))
        or [value for value in section_names if value in REQUIRED_SECTIONS] != REQUIRED_SECTIONS
    ):
        issues.append("baton section order mismatch")
    for section in sections:
        values = section.get("card_ids", [])
        if not values or any(value not in by_id for value in values):
            issues.append(f"invalid baton section: {section.get('section')}")
    tier_counts = Counter(row.get("tier") for row in cards)
    expected_tier_counts = Counter(
        {int(key): value for key, value in model.get("index", {}).get("expected_tier_counts", {}).items()}
    )
    if tier_counts != expected_tier_counts or expected_tier_counts[4] < 1:
        issues.append(f"unexpected tier counts: {dict(tier_counts)}")
    core = Counter(by_id[value]["outcome"] for value in model.get("new_proposal_card_ids", []) if value in by_id)
    if core != Counter(completed=14, represented=4, open_gap=1, exact_gate=1):
        issues.append(f"new core outcome mismatch: {dict(core)}")
    return {
        "schema": f"{SCHEMA}.model-validation",
        "valid": not issues,
        "issue_count": len(issues),
        "issues": issues,
        "card_count": len(cards),
        "tier_counts": {str(key): value for key, value in sorted(tier_counts.items())},
        "topological_order_count": len(order),
        "section_count": len(sections),
        "new_core_outcomes": dict(sorted(core.items())),
        "boundary": "Structural and synthetic card validation only; not cache-effect, identity, professional, production, empirical, independent, or Stage 20 evidence.",
    }


def card_relative_path(row: dict[str, Any]) -> str:
    return f"cards/tier{row['tier']}/{row['card_id']}.json"


def compact_message(model: dict[str, Any]) -> str:
    index = model["index"]
    successor = index["successor_route"]
    successor_label = successor.get("owner") or successor.get("title")
    if not isinstance(successor_label, str) or not successor_label.strip():
        raise FlashcardError("successor route label is missing")
    return f"""# PREPARED MODULAR POINTER — NOT AN ACTIVATION

Dear {successor_label},

This owner-local deck prepares a compact pointer for `{successor['phase']}` but is not sent and carries no delivery claim. Only after {index['owner']}'s clean, pushed, fresh-live-equal terminal gate and a fresh roster and authorization reread may one exact-title activation be attempted. Read the committed modular baton index at `{index['phase_root']}/deck/baton-index.json`, then load the stable prefix and only the task-local volatile cards it names. The inherited exact source is `{index['source_exact_final']}` and {index['owner']}'s frozen x1 is `{index['x1_head']}`.

Relational names, roles, hopes, and family language are working language only, never consciousness, personhood, identity continuity, qualification, employment, independent agency, or authority evidence. GMUT remains a typed research-model family; THOS remains synthetic; Freed ID remains nonproduction; legal, cultural, affected-party, and Maori authority remain gated. The verdict remains `NOT_READY_FOR_STAGE_20`.

If the later route gate opens, work only in {successor_label}'s owned lane, preserve every failure and gate, and do not contact a later task before {successor_label}'s own terminal closeout. Tavian Sol remains on standby and is not a substitute endpoint. Send once only after fresh exact-title resolution and immediate reread; claim delivery only from acknowledgement, and never create or substitute a missing task.

PREPARED_NOT_SENT = true
SENT = false
"""


def accessible_report(model: dict[str, Any]) -> str:
    index = model["index"]
    counts = Counter(row["tier"] for row in model["cards"])
    section_rows = "\n".join(
        f"<tr><th scope=\"row\">{html.escape(row['section'])}</th><td>{len(row['card_ids'])}</td></tr>"
        for row in model["baton_index"]["sections"]
    )
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>GHC Freed ID flashcard deck</title></head>
<body>
<a href="#main">Skip to main content</a>
<header><h1>GHC Freed ID flashcard deck</h1><p>{html.escape(index['owner'])} {html.escape(index['phase'])}</p><p>{html.escape(index['bounded_practice'])}</p></header>
<nav aria-label="Deck sections"><a href="#hierarchy">Hierarchy</a> <a href="#sections">Sections</a> <a href="#boundaries">Boundaries</a></nav>
<main id="main">
<section id="hierarchy"><h2>Four-tier hierarchy</h2><ol><li>Freed ID anchor: {counts[1]}</li><li>Trinity pillars: {counts[2]}</li><li>Bounded practice: {counts[3]}</li><li>Task cards: {counts[4]}</li></ol></section>
<section id="sections"><h2>Modular baton sections</h2><table><caption>Card references per section</caption><thead><tr><th scope="col">Section</th><th scope="col">References</th></tr></thead><tbody>{section_rows}</tbody></table></section>
<section id="boundaries"><h2>Evidence and authority boundaries</h2><p>Card structure is same-owner software evidence only. Manual browser, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved. No card proves identity, personhood, professional competence, empirical GMUT, production readiness, legal or cultural authority, Maori authority, exhaustive security, independent reproduction, or Stage 20 readiness.</p></section>
</main>
<footer><p>Status is also expressed in text; colour is not required. Verdict: NOT_READY_FOR_STAGE_20.</p></footer>
</body></html>
"""


def build_outputs(repo: Path, phase_root_rel: str, output_rel: str, x1_head: str) -> dict[str, Any]:
    phase_root_rel = safe_relative(phase_root_rel)
    output_rel = safe_relative(output_rel)
    phase_root = ensure_under(repo, repo / phase_root_rel)
    output = ensure_under(repo, repo / output_rel)
    model = build_model(phase_root, x1_head)
    expected_output = f"{model['index']['phase_root']}/deck"
    if output_rel != expected_output:
        raise FlashcardError(f"output directory must be the current owner deck: {expected_output}")
    validation = validate_model(model)
    if not validation["valid"]:
        raise FlashcardError("model validation failed: " + "; ".join(validation["issues"]))
    records: list[dict[str, Any]] = []
    for row in sorted(model["cards"], key=lambda item: (item["tier"], item["card_id"])):
        rel = card_relative_path(row)
        raw = pretty_bytes(row)
        write_equal_or_new(output / rel, raw)
        records.append({"path": rel, "bytes": len(raw), "sha256": digest_bytes(raw)})
    artifacts: dict[str, Any] = {
        "deck-index.json": model["index"],
        "stable-prefix.json": model["stable_prefix"],
        "volatile-index.json": model["volatile_index"],
        "baton-index.json": model["baton_index"],
        "model-validation.json": validation,
    }
    for rel, payload in artifacts.items():
        raw = pretty_bytes(payload)
        write_equal_or_new(output / rel, raw)
        records.append({"path": rel, "bytes": len(raw), "sha256": digest_bytes(raw)})
    compact = compact_message(model)
    compact_raw = compact.encode("utf-8")
    if len(compact.split()) > 600 or private_candidates(compact):
        raise FlashcardError("compact message boundary failed")
    write_equal_or_new(output / "compact-activation.md", compact_raw)
    records.append({"path": "compact-activation.md", "bytes": len(compact_raw), "sha256": digest_bytes(compact_raw)})
    report = accessible_report(model)
    report_raw = report.encode("utf-8")
    write_equal_or_new(output / "accessible-report.html", report_raw)
    records.append({"path": "accessible-report.html", "bytes": len(report_raw), "sha256": digest_bytes(report_raw)})
    records = sorted(records, key=lambda row: row["path"])
    manifest = {
        "schema": f"{SCHEMA}.content-manifest",
        "owner": model["index"]["owner"],
        "phase": model["index"]["phase"],
        "source_exact_final": model["index"]["source_exact_final"],
        "x1_head": x1_head,
        "entry_count": len(records),
        "entries": records,
        "canonical_commitment_sha256": digest_bytes(canonical_bytes(records)),
        "self_excluded_paths": ["card-manifest.json"],
        "valid": True,
    }
    write_equal_or_new(output / "card-manifest.json", pretty_bytes(manifest))
    return {
        "schema": f"{SCHEMA}.build-receipt",
        "valid": True,
        "output": output_rel,
        "card_count": len(model["cards"]),
        "manifest_entries": len(records),
        "section_count": len(model["baton_index"]["sections"]),
        "compact_message_words": len(compact.split()),
        "new_core_outcomes": model["index"]["new_core_outcomes"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def load_deck(repo: Path, deck_rel: str) -> tuple[Path, dict[str, Any]]:
    deck_rel = safe_relative(deck_rel)
    deck = ensure_under(repo, repo / deck_rel)
    index = strict_json(deck / "deck-index.json")
    stable = strict_json(deck / "stable-prefix.json")
    volatile = strict_json(deck / "volatile-index.json")
    baton = strict_json(deck / "baton-index.json")
    cards = [strict_json(path) for path in sorted((deck / "cards").rglob("*.json"))]
    new_ids = [row["card_id"] for row in cards if row.get("content", {}).get("program_class") == "genuinely_new_core_proposal"]
    return deck, {"cards": cards, "new_proposal_card_ids": new_ids, "index": index, "stable_prefix": stable, "volatile_index": volatile, "baton_index": baton}


def manifest_status(deck: Path) -> dict[str, Any]:
    manifest = strict_json(deck / "card-manifest.json")
    issues: list[str] = []
    expected = {row["path"]: row for row in manifest.get("entries", [])}
    observed: dict[str, dict[str, Any]] = {}
    for path in sorted(value for value in deck.rglob("*") if value.is_file() and value.name != "card-manifest.json"):
        rel = path.relative_to(deck).as_posix()
        raw = path.read_bytes()
        observed[rel] = {"path": rel, "bytes": len(raw), "sha256": digest_bytes(raw)}
    for rel in sorted(set(expected) | set(observed)):
        if rel not in expected:
            issues.append(f"unexpected file: {rel}")
        elif rel not in observed:
            issues.append(f"missing file: {rel}")
        elif expected[rel] != observed[rel]:
            issues.append(f"manifest mismatch: {rel}")
    if manifest.get("canonical_commitment_sha256") != digest_bytes(canonical_bytes(sorted(observed.values(), key=lambda row: row["path"]))):
        issues.append("manifest commitment mismatch")
    return {
        "schema": f"{SCHEMA}.manifest-status",
        "valid": not issues,
        "issue_count": len(issues),
        "issues": issues,
        "expected_entries": len(expected),
        "observed_entries": len(observed),
    }


def privacy_status(deck: Path) -> dict[str, Any]:
    records = []
    for path in sorted(value for value in deck.rglob("*") if value.is_file()):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            continue
        classes = private_candidates(text)
        if classes:
            records.append({"path": path.relative_to(deck).as_posix(), "classes": classes})
    return {
        "schema": f"{SCHEMA}.privacy-status",
        "classes": 5,
        "candidate_count": len(records),
        "candidates": records,
        "valid": not records,
        "boundary": "Five-class bounded deck scan only; not complete privacy assurance.",
    }


def validate_deck(repo: Path, deck_rel: str) -> dict[str, Any]:
    deck, model = load_deck(repo, deck_rel)
    model_result = validate_model(model)
    manifest_result = manifest_status(deck)
    privacy_result = privacy_status(deck)
    compact = (deck / "compact-activation.md").read_text(encoding="utf-8")
    report = (deck / "accessible-report.html").read_text(encoding="utf-8")
    structure = {
        "doctype": report.lower().startswith("<!doctype html>"),
        "lang": '<html lang="en">' in report,
        "main": '<main id="main">' in report,
        "nav": "<nav" in report,
        "table": "<table>" in report,
        "caption": "<caption>" in report,
    }
    compact_valid = len(compact.split()) <= 600 and not private_candidates(compact)
    valid = model_result["valid"] and manifest_result["valid"] and privacy_result["valid"] and all(structure.values()) and compact_valid
    return {
        "schema": f"{SCHEMA}.deck-validation",
        "valid": valid,
        "model": model_result,
        "manifest": manifest_result,
        "privacy": privacy_result,
        "accessible_structure": structure,
        "compact_message_words": len(compact.split()),
        "compact_message_valid": compact_valid,
        "manual_evaluation_reserved": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def mutation_receipt(repo: Path, deck_rel: str) -> dict[str, Any]:
    _, model = load_deck(repo, deck_rel)
    base_cards = model["cards"]
    cases = []
    mutation_prefix = slug(f"{model['index']['owner']}-{model['index']['phase']}").upper()
    for number, card_id in enumerate(model["new_proposal_card_ids"], 1):
        missing = copy.deepcopy(model)
        missing["cards"] = [row for row in base_cards if row["card_id"] != card_id]
        result = validate_model(missing)
        cases.append({"mutation_id": f"{mutation_prefix}-MUT-{number:03d}-MISSING", "target_card": card_id, "mutation": "remove indexed proposal card", "rejected": not result["valid"], "issues": result["issues"]})
        invalid = copy.deepcopy(model)
        next(row for row in invalid["cards"] if row["card_id"] == card_id)["outcome"] = "promoted"
        result = validate_model(invalid)
        cases.append({"mutation_id": f"{mutation_prefix}-MUT-{number:03d}-OUTCOME", "target_card": card_id, "mutation": "replace outcome with an unapproved label", "rejected": not result["valid"], "issues": result["issues"]})
        orphan = copy.deepcopy(model)
        next(row for row in orphan["cards"] if row["card_id"] == card_id)["parent_ids"] = ["ghc-card-missing-parent"]
        result = validate_model(orphan)
        cases.append({"mutation_id": f"{mutation_prefix}-MUT-{number:03d}-ORPHAN", "target_card": card_id, "mutation": "replace practice parent with missing card", "rejected": not result["valid"], "issues": result["issues"]})
    positive = validate_model(model)
    return {
        "schema": f"{SCHEMA}.mutation-receipt",
        "mutation_count": len(cases),
        "rejected_count": sum(bool(row["rejected"]) for row in cases),
        "cases": cases,
        "positive_proposal_fixture_count": len(model["new_proposal_card_ids"]),
        "positive_deck_valid": positive["valid"],
        "failure_credit": 0,
        "valid": len(cases) == 60 and all(row["rejected"] for row in cases) and positive["valid"],
        "boundary": "Synthetic rejecting mutations only; not exhaustive security, production, cache-effect, identity, empirical, professional, or authority evidence.",
    }


def install_receipt(source: Path, installed: Path) -> dict[str, Any]:
    def records(root: Path) -> list[dict[str, Any]]:
        return [
            {"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size, "sha256": digest_file(path)}
            for path in sorted(value for value in root.rglob("*") if value.is_file())
        ]
    source_records = records(source)
    installed_records = records(installed)
    return {
        "schema": f"{SCHEMA}.install-receipt",
        "source_files": source_records,
        "installed_files": installed_records,
        "byte_for_byte_equal": source_records == installed_records,
        "source_file_count": len(source_records),
        "installed_file_count": len(installed_records),
        "paths_sanitized": True,
        "valid": source_records == installed_records and bool(source_records),
        "boundary": "Local package parity only; not global production readiness or external authority.",
    }


def emit(payload: dict[str, Any], output: Path | None = None) -> None:
    raw = pretty_bytes(payload)
    if output is None:
        sys.stdout.buffer.write(raw)
    else:
        write_equal_or_new(output, raw)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build")
    build.add_argument("--repo", type=Path, required=True)
    build.add_argument("--phase-root", required=True)
    build.add_argument("--output-dir", required=True)
    build.add_argument("--x1", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("--repo", type=Path, required=True)
    validate.add_argument("--deck-dir", required=True)
    for name in ("manifest", "graph", "privacy", "render-html", "diff"):
        sub = commands.add_parser(name)
        sub.add_argument("--repo", type=Path, required=True)
        sub.add_argument("--deck-dir", required=True)
    compact = commands.add_parser("compact-message")
    compact.add_argument("--repo", type=Path, required=True)
    compact.add_argument("--deck-dir", required=True)
    mutations = commands.add_parser("mutations")
    mutations.add_argument("--repo", type=Path, required=True)
    mutations.add_argument("--deck-dir", required=True)
    mutations.add_argument("--output", type=Path)
    smoke = commands.add_parser("smoke")
    smoke.add_argument("--repo", type=Path, required=True)
    smoke.add_argument("--phase-root", required=True)
    smoke.add_argument("--x1", required=True)
    install = commands.add_parser("install-receipt")
    install.add_argument("--source", type=Path, required=True)
    install.add_argument("--installed", type=Path, required=True)
    install.add_argument("--output", type=Path)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "build":
            emit(build_outputs(args.repo.resolve(), args.phase_root, args.output_dir, args.x1))
        elif args.command == "validate":
            emit(validate_deck(args.repo.resolve(), args.deck_dir))
        elif args.command == "manifest":
            deck, _ = load_deck(args.repo.resolve(), args.deck_dir)
            emit(manifest_status(deck))
        elif args.command == "graph":
            _, model = load_deck(args.repo.resolve(), args.deck_dir)
            result = validate_model(model)
            emit({"schema": f"{SCHEMA}.graph", "valid": result["valid"], "card_count": result["card_count"], "topological_order_count": result["topological_order_count"], "issues": result["issues"]})
        elif args.command == "privacy":
            deck, _ = load_deck(args.repo.resolve(), args.deck_dir)
            emit(privacy_status(deck))
        elif args.command == "render-html":
            deck, model = load_deck(args.repo.resolve(), args.deck_dir)
            expected = accessible_report(model).encode("utf-8")
            observed = (deck / "accessible-report.html").read_bytes()
            emit({"schema": f"{SCHEMA}.render-html", "valid": expected == observed, "bytes": len(observed), "sha256": digest_bytes(observed), "manual_evaluation_reserved": True})
        elif args.command == "diff":
            deck, _ = load_deck(args.repo.resolve(), args.deck_dir)
            emit(manifest_status(deck))
        elif args.command == "compact-message":
            _, model = load_deck(args.repo.resolve(), args.deck_dir)
            text = compact_message(model)
            emit({"schema": f"{SCHEMA}.compact-message", "valid": len(text.split()) <= 600 and not private_candidates(text), "words": len(text.split()), "sha256": digest_bytes(text.encode("utf-8")), "message": text})
        elif args.command == "mutations":
            emit(mutation_receipt(args.repo.resolve(), args.deck_dir), args.output)
        elif args.command == "smoke":
            phase = ensure_under(args.repo.resolve(), args.repo.resolve() / safe_relative(args.phase_root))
            model = build_model(phase, args.x1)
            result = validate_model(model)
            emit({"schema": f"{SCHEMA}.smoke", "valid": result["valid"], "card_count": result["card_count"], "section_count": result["section_count"], "new_core_outcomes": result["new_core_outcomes"]})
        elif args.command == "install-receipt":
            emit(install_receipt(args.source.resolve(), args.installed.resolve()), args.output)
        else:
            raise FlashcardError("unknown command")
    except (FlashcardError, OSError) as exc:
        sys.stderr.write(f"GHC_FREED_ID_FLASHCARD_ERROR: {exc}\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
