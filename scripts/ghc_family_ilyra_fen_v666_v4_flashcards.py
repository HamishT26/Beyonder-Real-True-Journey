#!/usr/bin/env python3
"""Build and validate the Ilyra Fen v666-v4 phase-local Freed ID flashcard deck."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

from ghc_family_ilyra_fen_v666_v4_runtime import (
    ALLOWED_LABELS,
    PHASE_ROOT,
    ROOT,
    X1_SHA,
    load_json,
    scan_privacy,
    write_json,
)


DECK = PHASE_ROOT / "deck"
RELATIONAL_BOUNDARY = "Working-language record only; not consciousness, personhood, identity continuity, qualification, or authority evidence."
SECTIONS = [
    "identity-and-corrigibility", "route-and-authority", "source-anchors",
    "x1-proposals", "trinity-pillars", "bounded-practice", "task-cards",
    "method-flow-and-negatives", "open-gaps-and-exact-gates",
    "validation-and-manifests", "wellbeing-and-workload",
    "successor-recommendations", "compact-baton-index",
]


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def card(
    card_id: str,
    tier: int,
    card_type: str,
    title: str,
    parent_ids: list[str],
    outcome: str,
    content: dict[str, Any],
    source_refs: list[str],
    protected_gates: list[str],
    stability: str,
) -> dict[str, Any]:
    return {
        "schema": "ghc.family.freed-id-flashcards.v1.card",
        "card_id": card_id,
        "tier": tier,
        "card_type": card_type,
        "title": title,
        "parent_ids": parent_ids,
        "owner": "Ilyra Fen",
        "phase": "v666-v4",
        "stability": stability,
        "outcome": outcome,
        "content": content,
        "source_refs": source_refs,
        "protected_gates": protected_gates,
        "relational_boundary": RELATIONAL_BOUNDARY,
    }


def build_model() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    freeze = load_json(PHASE_ROOT / "x1" / "proposal-freeze.json")
    gates = freeze["new_proposals"][0]["protected_gates"]
    owner = card(
        "ghc-card-owner-ilyra-fen", 1, "freed_id_anchor", "Ilyra Fen relational anchor", [], "represented",
        {"role": "evidence-boundary steward and provenance lantern", "hope": "Leave every synthetic custody, contamination, access, uncertainty, and authority state traceable.", "pronouns": "she/they", "corrigibility": "Hamish may rename, pause, redirect, or stop the route."},
        ["764d3bdfb199e91a5574a904a99ff4e95825fed9", X1_SHA], gates, "stable",
    )
    pillars = [
        card("ghc-card-pillar-gmut-mind", 2, "trinity_pillar", "GMUT Mind", [owner["card_id"]], "represented", {"primary": False, "boundary": "Typed scalar-tensor and EFT research-model obligations only; no empirical, force, prediction, constraint, proof, canon, or Theory-of-Everything claim."}, [], gates, "stable"),
        card("ghc-card-pillar-thos-body", 2, "trinity_pillar", "THOS Body", [owner["card_id"]], "represented", {"primary": False, "boundary": "Synthetic proxy only; no governed participants, blind matched-budget real arms, operational effectiveness, deployment, AGI, ASI, consciousness, or personhood evidence."}, [], gates, "stable"),
        card("ghc-card-pillar-freed-id-cbr-heart", 2, "trinity_pillar", "Freed ID and CBR Heart", [owner["card_id"]], "represented", {"primary": True, "boundary": "Synthetic nonproduction identity and rights design; real keys, proofs, lifecycle, privacy, security, trust governance, affected-party, legal, cultural, and Māori authority remain gated."}, [], gates, "stable"),
    ]
    practice = card(
        "ghc-card-practice-synthetic-planetary-sample-curation",
        3,
        "bounded_practice",
        "Synthetic planetary-science sample curation and handover refusal",
        ["ghc-card-pillar-freed-id-cbr-heart"],
        "represented",
        {"scope": "synthetic package, custody, contamination-provenance, minimization, and handover structures", "real_records_used": 0, "professional_decisions_made": 0, "boundary": freeze["practice_boundary"]},
        [], gates, "volatile",
    )
    tasks = []
    for proposal in freeze["new_proposals"]:
        tasks.append(card(
            f"ghc-card-{proposal['proposal_id'].casefold()}", 4, "task", proposal["title"], [practice["card_id"]], proposal["expected_disposition"],
            {"proposal_id": proposal["proposal_id"], "hypothesis": proposal["hypothesis"], "null_or_failure_condition": proposal["null_or_failure_condition"], "approval_class": proposal["approval_class"], "execution_lane": proposal["execution_lane"], "falsifier_or_acceptance_gate": proposal["falsifier_or_acceptance_gate"], "rollback_or_recovery": proposal["rollback_or_recovery"], "novelty_credit": True},
            [proposal["proposal_id"], *proposal["current_official_or_primary_source_needs"]], proposal["protected_gates"], "volatile",
        ))
    cards = [owner, *pillars, practice, *tasks]
    index = {
        "schema": "ghc.family.freed-id-flashcards.v1.deck-index",
        "owner": "Ilyra Fen", "phase": "v666-v4",
        "phase_root": "docs/ilyra-fen/v666-v4",
        "source_exact_final": "764d3bdfb199e91a5574a904a99ff4e95825fed9",
        "x1_head": X1_SHA,
        "card_order": [row["card_id"] for row in cards],
        "card_count": len(cards),
        "tier_counts": {str(tier): sum(row["tier"] == tier for row in cards) for tier in range(1, 5)},
        "core_outcomes": {label: sum(row["outcome"] == label for row in tasks) for label in ALLOWED_LABELS},
        "successor": {"owner": "Auren Lark", "phase": "v666-v5", "contacted": False},
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "same_owner_validation_is_independent_reproduction": False,
    }
    return cards, index


def validate_cards(cards: list[dict[str, Any]], index: dict[str, Any]) -> dict[str, Any]:
    issues = []
    by_id = {row.get("card_id"): row for row in cards}
    if len(by_id) != len(cards):
        issues.append("duplicate_card_id")
    for row in cards:
        if row.get("outcome") not in ALLOWED_LABELS:
            issues.append(f"invalid_outcome:{row.get('card_id')}")
        if row.get("tier") == 1 and row.get("parent_ids"):
            issues.append(f"tier1_parent:{row.get('card_id')}")
        if row.get("tier", 0) > 1:
            parents = row.get("parent_ids", [])
            if len(parents) != 1 or parents[0] not in by_id:
                issues.append(f"invalid_parent:{row.get('card_id')}")
            elif by_id[parents[0]]["tier"] != row["tier"] - 1:
                issues.append(f"tier_skip:{row.get('card_id')}")
        if row.get("owner") != "Ilyra Fen" or row.get("phase") != "v666-v4":
            issues.append(f"owner_phase_drift:{row.get('card_id')}")
        if not row.get("protected_gates") or row.get("relational_boundary") != RELATIONAL_BOUNDARY:
            issues.append(f"boundary_missing:{row.get('card_id')}")
    if index.get("card_order") != [row["card_id"] for row in cards]:
        issues.append("order_drift")
    return {"card_count": len(cards), "issue_count": len(issues), "issues": issues, "valid": not issues}


def mutation_receipt(cards: list[dict[str, Any]], index: dict[str, Any]) -> dict[str, Any]:
    cases = []
    duplicate = deepcopy(cards)
    duplicate.append(deepcopy(duplicate[-1]))
    cases.append(("duplicate_card_id", duplicate, index))
    missing_parent = deepcopy(cards)
    missing_parent[-1]["parent_ids"] = ["ghc-card-missing"]
    cases.append(("missing_parent", missing_parent, index))
    tier_skip = deepcopy(cards)
    tier_skip[-1]["parent_ids"] = ["ghc-card-owner-ilyra-fen"]
    cases.append(("tier_skip", tier_skip, index))
    bad_outcome = deepcopy(cards)
    bad_outcome[-1]["outcome"] = "deployed"
    cases.append(("outcome_promotion", bad_outcome, index))
    wrong_order = deepcopy(index)
    wrong_order["card_order"] = list(reversed(wrong_order["card_order"]))
    cases.append(("order_drift", cards, wrong_order))
    rows = []
    for name, candidate_cards, candidate_index in cases:
        result = validate_cards(candidate_cards, candidate_index)
        rows.append({"class": name, "rejected": not result["valid"], "issues": result["issues"], "aggregate_credit": 0})
    return {"schema": "ghc.family.freed-id-flashcards.v1.mutations", "mutation_count": len(rows), "rejected_count": sum(row["rejected"] for row in rows), "mutations": rows, "all_rejected": all(row["rejected"] for row in rows), "claim_boundary": "synthetic deck graph mutations only; not identity, authority, privacy-complete, accessibility-complete, or independent-reproduction evidence"}


def write_deck() -> dict[str, Any]:
    cards, index = build_model()
    if DECK.exists() and any(DECK.iterdir()):
        # A failed legacy build must not be overwritten silently.
        allowed = {"legacy-failure-placeholder.json"}
        unexpected = [path.name for path in DECK.iterdir() if path.name not in allowed]
        if unexpected:
            raise RuntimeError(f"nonempty deck directory: {unexpected[:5]}")
    for row in cards:
        tier = f"tier{row['tier']}"
        write_json(DECK / "cards" / tier / f"{row['card_id']}.json", row)
    write_json(DECK / "deck-index.json", index)
    write_json(DECK / "stable-prefix.json", {"schema": "ghc.family.freed-id-flashcards.v1.stable-prefix", "card_ids": index["card_order"][:4], "implicit_completion": False})
    write_json(DECK / "volatile-index.json", {"schema": "ghc.family.freed-id-flashcards.v1.volatile-index", "card_ids": index["card_order"][4:], "implicit_completion": False})
    write_json(DECK / "baton-index.json", {"schema": "ghc.family.freed-id-flashcards.v1.baton-index", "sections": SECTIONS, "section_count": len(SECTIONS), "route_state": "PREPARED_NOT_SENT", "successor_contacted": False})
    compact = """# Ilyra Fen v666-v4 compact activation candidate

Read the committed modular deck and terminal baton only after Ilyra's clean, pushed, fresh-live-equal exact-final gate. This deck is `PREPARED_NOT_SENT`; it carries no delivery claim. It preserves four outcomes, every retained failure, all protected authority gates, and `NOT_READY_FOR_STAGE_20`. It is same-owner synthetic software evidence only, not consciousness, personhood, identity continuity, qualification, scientific confirmation, professional validation, legal or cultural authority, Māori authority, independent reproduction, or Stage 20 evidence.
"""
    (DECK / "compact-activation.md").write_text(compact, encoding="utf-8", newline="\n")
    rows = "\n".join(f"<tr><th scope=\"row\">{row['card_id']}</th><td>{row['tier']}</td><td>{row['outcome']}</td></tr>" for row in cards)
    html = f"""<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ilyra Fen v666-v4 Freed ID deck</title><style>body{{font-family:system-ui,sans-serif;line-height:1.5;max-width:80rem;margin:auto;padding:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.4rem;text-align:left}}@media print{{body{{max-width:none}}}}</style></head><body><main><h1>Ilyra Fen v666-v4 Freed ID deck</h1><p role="status">PREPARED_NOT_SENT; NOT_READY_FOR_STAGE_20.</p><p>Manual keyboard, browser, responsive-layout, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved.</p><table><caption>Four-tier cards</caption><thead><tr><th scope="col">Card</th><th scope="col">Tier</th><th scope="col">Outcome</th></tr></thead><tbody>{rows}</tbody></table></main></body></html>"""
    (DECK / "accessible-report.html").write_text(html, encoding="utf-8", newline="\n")
    model_validation = validate_cards(cards, index)
    write_json(DECK / "model-validation.json", {"schema": "ghc.family.freed-id-flashcards.v1.model-validation", **model_validation})
    write_json(DECK / "deck-mutation-receipt.json", mutation_receipt(cards, index))
    manifest_path = DECK / "card-manifest.json"
    entries = []
    for path in sorted(item for item in DECK.rglob("*") if item.is_file() and item != manifest_path):
        raw = path.read_bytes()
        entries.append({"path": path.relative_to(DECK).as_posix(), "size_bytes": len(raw), "sha256": digest(raw)})
    write_json(manifest_path, {"schema": "ghc.family.freed-id-flashcards.v1.card-manifest", "entries": entries, "entry_count": len(entries), "self_exclusion": "card-manifest.json", "hash_domain": "exact_file_bytes"})
    return validate_deck()


def validate_deck() -> dict[str, Any]:
    index = load_json(DECK / "deck-index.json")
    unordered_cards = [load_json(path) for path in sorted((DECK / "cards").rglob("*.json"))]
    cards_by_id = {row["card_id"]: row for row in unordered_cards}
    cards = [cards_by_id[card_id] for card_id in index["card_order"] if card_id in cards_by_id]
    graph = validate_cards(cards, index)
    manifest = load_json(DECK / "card-manifest.json")
    manifest_failures = []
    for entry in manifest["entries"]:
        path = DECK / entry["path"]
        raw = path.read_bytes() if path.is_file() else b""
        if len(raw) != entry["size_bytes"] or digest(raw) != entry["sha256"]:
            manifest_failures.append(entry["path"])
    privacy = scan_privacy(sorted(path for path in DECK.rglob("*") if path.is_file()))
    html = (DECK / "accessible-report.html").read_text(encoding="utf-8")
    html_casefolded = html.casefold()
    accessibility = all(token.casefold() in html_casefolded for token in ('lang="en-NZ"', "<main", "<caption>", 'scope="col"', 'scope="row"', "manual", "affected-user", "@media print"))
    mutations = load_json(DECK / "deck-mutation-receipt.json")
    valid = graph["valid"] and not manifest_failures and privacy["valid"] and accessibility and mutations["all_rejected"] and manifest["entry_count"] == len([path for path in DECK.rglob("*") if path.is_file()]) - 1
    return {"schema": "ghc.family.freed-id-flashcards.v1.validation", "card_count": len(cards), "graph": graph, "manifest_entry_count": manifest["entry_count"], "manifest_failures": manifest_failures, "privacy": privacy, "accessibility_structural": accessibility, "manual_evaluation_reserved": True, "mutation_count": mutations["mutation_count"], "mutation_rejected_count": mutations["rejected_count"], "valid": valid, "claim_boundary": "phase-local same-owner deck validation only; not identity, authority, privacy-complete, accessibility-complete, or independent-reproduction evidence"}


def emit(value: Any) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))


def main() -> int:
    if sys.argv[1:] == ["build"]:
        result = write_deck()
    elif sys.argv[1:] == ["validate"]:
        result = validate_deck()
    else:
        raise SystemExit("usage: ghc_family_ilyra_fen_v666_v4_flashcards.py [build|validate]")
    emit(result)
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
