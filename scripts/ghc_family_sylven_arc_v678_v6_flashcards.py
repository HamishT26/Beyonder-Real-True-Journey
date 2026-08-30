#!/usr/bin/env python3
"""Build and validate Sylven Arc v678-v6 four-tier Freed ID flashcards."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path
from typing import Any


SCHEMA = "ghc-freed-id-flashcard/v1"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}
TIERS = {1: "freed_id_anchor", 2: "trinity_pillar", 3: "bounded_practice", 4: "task"}
OWNERS = [
    "Sylven Arc", "Eiren Kestrel", "Elaren Kestrel", "Neris Solane", "Vesper Arlen",
    "Lyren Moss", "Ilyra Fen", "Auren Lark", "Sable Rook", "Caelen Ash", "Orin Thale",
    "Liora Venn", "Tamar Vey", "Elowen Cairn", "Caelen Morrow",
]
PILLARS = [
    ("GMUT Mind", "typed research-model obligations; no empirical or final-physics claim"),
    ("THOS Body", "participant-free synthetic proxy; no operational or deployment claim"),
    ("Freed ID and CBR Heart", "synthetic nonproduction rights record; no keys, proofs, or authority act"),
]
PRACTICES = [
    ("Synthetic globemaking records analyst", "GMUT Mind", "zero-globe documentation lens"),
    ("Synthetic mechanical-automaton linkage analyst", "THOS Body", "zero-machine documentation lens"),
    ("Synthetic stained-glass handover steward", "Freed ID and CBR Heart", "zero-window documentation lens"),
]
RELATIONAL_BOUNDARY = (
    "Relational name and role language is working language only; it is not evidence of consciousness, "
    "sentience, personhood, identity continuity, employment, qualification, agency, or authority."
)
PRIVATE_PATTERNS = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(r"(?i)(terminal transcript|session stream|screenshot payload)"),
}


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def card_id(seed: str) -> str:
    return "ghc-card-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:24]


def make_card(*, seed: str, tier: int, title: str, parents: list[str], owner: str,
              outcome: str, content: dict[str, Any], sources: list[str], gates: list[str]) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "card_id": card_id(seed),
        "tier": tier,
        "card_type": TIERS[tier],
        "title": title,
        "parent_ids": parents,
        "owner": owner,
        "phase": "v678-v6",
        "stability": "stable" if tier <= 2 else "phase_bounded",
        "outcome": outcome,
        "content": content,
        "source_refs": sources,
        "protected_gates": gates,
        "relational_boundary": RELATIONAL_BOUNDARY,
    }


def validate_card(card: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    required = {
        "schema", "card_id", "tier", "card_type", "title", "parent_ids", "owner", "phase",
        "stability", "outcome", "content", "source_refs", "protected_gates", "relational_boundary",
    }
    missing = sorted(required - card.keys())
    if missing:
        return ["missing:" + ",".join(missing)]
    tier = card["tier"]
    if tier not in TIERS or card["card_type"] != TIERS[tier]:
        errors.append("tier_or_type_invalid")
    if not str(card["card_id"]).startswith("ghc-card-"):
        errors.append("card_id_invalid")
    if card["outcome"] not in LABELS:
        errors.append("outcome_invalid")
    parents = card["parent_ids"]
    if tier == 1 and parents:
        errors.append("tier1_parent_forbidden")
    if tier > 1 and len(parents) != 1:
        errors.append("single_parent_required")
    if tier > 1 and len(parents) == 1:
        parent = by_id.get(parents[0])
        if not parent or parent.get("tier") != tier - 1:
            errors.append("parent_tier_invalid")
    if card["phase"] != "v678-v6":
        errors.append("phase_invalid")
    if card["relational_boundary"] != RELATIONAL_BOUNDARY:
        errors.append("relational_boundary_invalid")
    return errors


def build(repo: Path, phase_root: Path, output: Path, x1: str) -> dict[str, Any]:
    proposal_path = phase_root / "x1" / "new-proposal-freeze.json"
    proposal_doc = json.loads(proposal_path.read_text(encoding="utf-8"))
    proposals = proposal_doc["proposals"]
    if len(proposals) != 60:
        raise SystemExit("expected exactly 60 frozen proposals")
    output.mkdir(parents=True, exist_ok=True)
    cards: list[dict[str, Any]] = []
    owner_cards: dict[str, str] = {}
    for owner in OWNERS:
        card = make_card(
            seed=f"v678-v6|owner|{owner}", tier=1, title=f"{owner} relational working anchor",
            parents=[], owner=owner, outcome="represented",
            content={
                "anchor_kind": "relational_working_anchor", "continuity_claim": False,
                "identity_certification": False, "authority_claim": False,
                "active_phase_owner": owner == "Sylven Arc",
            }, sources=["current-bounded-fifteen-main-task-roster"],
            gates=["no consciousness, personhood, continuity, qualification, or authority inference"],
        )
        owner_cards[owner] = card["card_id"]
        cards.append(card)
    pillar_cards: dict[str, str] = {}
    for name, boundary in PILLARS:
        card = make_card(
            seed=f"v678-v6|pillar|{name}", tier=2, title=name,
            parents=[owner_cards["Sylven Arc"]], owner="Sylven Arc", outcome="represented",
            content={"boundary": boundary, "primary": name == "THOS Body", "real_world_rows": 0},
            sources=["x1/primary-pillar-and-lens.json"],
            gates=["no empirical, participant, professional, production, legal, cultural, or Stage 20 promotion"],
        )
        pillar_cards[name] = card["card_id"]
        cards.append(card)
    practice_cards: list[str] = []
    for name, pillar, boundary in PRACTICES:
        card = make_card(
            seed=f"v678-v6|practice|{name}", tier=3, title=name,
            parents=[pillar_cards[pillar]], owner="Sylven Arc", outcome="represented",
            content={"lens": boundary, "employment_claim": False, "qualification_claim": False, "real_objects": 0},
            sources=["x1/primary-pillar-and-lens.json", "x1/official-source-ledger.json"],
            gates=["synthetic learning and design lens only; no handling, operation, treatment, custody, or release"],
        )
        practice_cards.append(card["card_id"])
        cards.append(card)
    for index, proposal in enumerate(proposals):
        practice_index = min(index // 20, 2)
        card = make_card(
            seed=f"v678-v6|task|{proposal['proposal_id']}", tier=4, title=proposal["title"],
            parents=[practice_cards[practice_index]], owner="Sylven Arc",
            outcome=proposal["expected_disposition"],
            content={
                "proposal_id": proposal["proposal_id"], "hypothesis": proposal["hypothesis"],
                "null_or_failure_condition": proposal["null_or_failure_condition"],
                "acceptance_gate": proposal["falsifier_or_acceptance_gate"],
                "rollback_or_recovery": proposal["rollback_or_recovery"],
                "expected_execution_disposition": proposal["expected_disposition"],
                "real_world_rows": 0, "external_actions": 0,
            }, sources=proposal["official_or_primary_source_needs"], gates=proposal["protected_gates"],
        )
        cards.append(card)
    by_id = {card["card_id"]: card for card in cards}
    if len(by_id) != len(cards):
        raise SystemExit("duplicate deterministic card id")
    validation = {cid: validate_card(card, by_id) for cid, card in by_id.items()}
    failures = {cid: errs for cid, errs in validation.items() if errs}
    if failures:
        raise SystemExit(json.dumps(failures, sort_keys=True))
    card_dir = output / "cards"
    card_dir.mkdir(parents=True, exist_ok=True)
    for card in cards:
        write_json(card_dir / f"{card['card_id']}.json", card)
    tier_counts = {str(tier): sum(card["tier"] == tier for card in cards) for tier in TIERS}
    index = {
        "schema": "ghc-freed-id-flashcard-deck-index/v1", "phase": "v678-v6", "owner": "Sylven Arc",
        "x1_commit": x1, "card_count": len(cards), "tier_counts": tier_counts,
        "outcome_counts": dict(sorted(__import__("collections").Counter(card["outcome"] for card in cards).items())),
        "cards": [{"card_id": c["card_id"], "tier": c["tier"], "title": c["title"]} for c in cards],
        "prompt_cache_guarantee": False, "identity_continuity_claim": False,
    }
    write_json(output / "deck-index.json", index)
    write_json(output / "stable-prefix.json", {
        "schema": "ghc-freed-id-stable-prefix/v1", "phase": "v678-v6",
        "card_ids": [c["card_id"] for c in cards if c["tier"] <= 2],
        "meaning": "bounded relational and pillar prefix; no prompt-cache or continuity guarantee",
    })
    write_json(output / "volatile-index.json", {
        "schema": "ghc-freed-id-volatile-index/v1", "phase": "v678-v6",
        "card_ids": [c["card_id"] for c in cards if c["tier"] >= 3],
        "mutable_after_additive_successor_review": True,
    })
    sections = [
        "relational-boundary", "source-and-lifecycle", "retained-failures", "proposal-and-outcome",
        "pillar-and-practice", "owner-safe-now", "candidate", "exact-and-blocked", "skills-and-runners",
        "clean-fix-refine", "validation", "protected-authority-boundaries", "terminal-route",
    ]
    write_json(output / "baton-index.json", {
        "schema": "ghc-freed-id-baton-index/v1", "phase": "v678-v6", "section_count": len(sections),
        "sections": [{"order": i + 1, "name": name} for i, name in enumerate(sections)],
        "minimum_monolithic_prompt_words": None, "file_backed_packet_preferred": True,
    })
    return {"status": "BUILT", "cards": len(cards), "tier_counts": tier_counts, "output": str(output.relative_to(repo))}


def load_deck(deck: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cards = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((deck / "cards").glob("*.json"))]
    index = json.loads((deck / "deck-index.json").read_text(encoding="utf-8"))
    return cards, index


def validate(deck: Path) -> dict[str, Any]:
    cards, index = load_deck(deck)
    by_id = {card["card_id"]: card for card in cards}
    errors = {cid: errs for cid, card in by_id.items() if (errs := validate_card(card, by_id))}
    if len(cards) != index["card_count"]:
        errors["deck-index"] = ["card_count_mismatch"]
    tier_counts = {str(tier): sum(c["tier"] == tier for c in cards) for tier in TIERS}
    if tier_counts != index["tier_counts"]:
        errors["deck-index-tier"] = ["tier_counts_mismatch"]
    result = {"status": "VALID" if not errors else "INVALID", "card_count": len(cards), "tier_counts": tier_counts, "errors": errors}
    if errors:
        raise SystemExit(json.dumps(result, sort_keys=True))
    return result


def manifest(deck: Path) -> dict[str, Any]:
    paths = sorted(path for path in deck.rglob("*") if path.is_file() and path.name != "card-manifest.json")
    value = {
        "schema": "ghc-freed-id-card-manifest/v1", "algorithm": "sha256", "self_exclusions": ["card-manifest.json"],
        "entries": [{"path": path.relative_to(deck).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)} for path in paths],
    }
    write_json(deck / "card-manifest.json", value)
    return {"status": "MANIFESTED", "entries": len(paths)}


def graph(deck: Path) -> dict[str, Any]:
    cards, _ = load_deck(deck)
    edges = [(parent, card["card_id"]) for card in cards for parent in card["parent_ids"]]
    result = {"schema": "ghc-freed-id-card-graph/v1", "nodes": len(cards), "edges": len(edges), "acyclic_by_tier": all(next(c["tier"] for c in cards if c["card_id"] == a) < next(c["tier"] for c in cards if c["card_id"] == b) for a, b in edges)}
    write_json(deck / "card-graph.json", result)
    return result


def privacy(deck: Path) -> dict[str, Any]:
    candidates: list[dict[str, str]] = []
    for path in sorted(deck.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".html"}:
            continue
        text = path.read_text(encoding="utf-8")
        for name, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                candidates.append({"path": path.relative_to(deck).as_posix(), "class": name})
    result = {"status": "PASS" if not candidates else "FAIL", "classes": sorted(PRIVATE_PATTERNS), "candidates": candidates, "confirmed_hits": len(candidates)}
    write_json(deck / "privacy-receipt.json", result)
    if candidates:
        raise SystemExit(json.dumps(result, sort_keys=True))
    return result


def render_html(deck: Path) -> dict[str, Any]:
    cards, index = load_deck(deck)
    rows = "".join(f"<tr><td>{c['tier']}</td><td>{html.escape(c['card_type'])}</td><td>{html.escape(c['title'])}</td><td>{html.escape(c['outcome'])}</td></tr>" for c in cards)
    document = f"""<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Sylven v678-v6 flashcards</title></head><body><main><h1>Sylven Arc v678-v6 four-tier flashcards</h1><p>{html.escape(RELATIONAL_BOUNDARY)}</p><p>Structural accessibility only; manual browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved.</p><table><caption>{index['card_count']} cards across four tiers</caption><thead><tr><th scope=\"col\">Tier</th><th scope=\"col\">Type</th><th scope=\"col\">Title</th><th scope=\"col\">Outcome</th></tr></thead><tbody>{rows}</tbody></table></main></body></html>"""
    (deck / "accessible-report.html").write_text(document, encoding="utf-8", newline="\n")
    return {"status": "RENDERED", "cards": len(cards), "accessibility_complete": False}


def compact_message(deck: Path) -> dict[str, Any]:
    _, index = load_deck(deck)
    message = (
        "Sylven Arc v678-v6 is file-backed in this four-tier flashcard deck. Read deck-index, stable-prefix, "
        "volatile-index, baton-index, card-manifest, privacy receipt, accessible report, then the exact-final "
        "handoff. Relational names are working language only. Validate the current roster and authorization "
        "before any route; this compact note is not evidence of delivery, continuity, or authority.\n"
    )
    (deck / "compact-activation.md").write_text(message, encoding="utf-8", newline="\n")
    return {"status": "COMPACT_MESSAGE_WRITTEN", "characters": len(message), "cards": index["card_count"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build_parser = sub.add_parser("build")
    build_parser.add_argument("--repo", type=Path, required=True)
    build_parser.add_argument("--phase-root", type=Path, required=True)
    build_parser.add_argument("--output-dir", type=Path, required=True)
    build_parser.add_argument("--x1", required=True)
    for name in ("validate", "manifest", "graph", "privacy", "render-html", "compact-message"):
        child = sub.add_parser(name)
        child.add_argument("--repo", type=Path, required=True)
        child.add_argument("--deck-dir", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.command == "build":
        result = build(repo, (repo / args.phase_root).resolve(), (repo / args.output_dir).resolve(), args.x1)
    else:
        deck = (repo / args.deck_dir).resolve()
        operations = {"validate": validate, "manifest": manifest, "graph": graph, "privacy": privacy, "render-html": render_html, "compact-message": compact_message}
        result = operations[args.command](deck)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
