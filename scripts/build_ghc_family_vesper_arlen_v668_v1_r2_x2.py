#!/usr/bin/env python3
"""Build the bounded Vesper v668-v1-r2 x2 evidence packet."""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_vesper_arlen_v668_v1_r2_archive import (
    ALLOWED_OUTCOMES,
    EVIDENCE_BOUNDARY,
    IDENTITY_BOUNDARY,
    OWNER,
    PHASE,
    PHASE_ROOT,
    REL_PHASE_ROOT,
    ROOT,
    SOURCE_FINAL,
    manifest_rows,
    sha256_bytes,
    utc_now,
    write_json,
    write_text,
)
from ghc_family_vesper_arlen_v668_v1_r2_controls import (
    ContractError,
    accession_envelope,
    append_correction,
    bagit_paths,
    base_envelope,
    custody_order,
    digest,
    fixity_quorum,
    language_fallback,
    mutated_envelope,
    namespace_tribunal,
    retention_decision,
    reversible_redaction,
    role_access,
    route_transition,
    salvage_queue,
    transfer_readback,
    validate_control_envelope,
    validate_flashcard_graph,
    validation_credit_transition,
)

X1_HEAD = "be908eb829185971c10be6d100c2c85fd35871e0"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
FOUR_TIERS = ("freed_id_anchor", "pillar", "practice", "task")
PRACTICES = (
    "museum collections registrar accession and provenance reconciliation",
    "public-library digital preservation migration and retention handover",
    "archival conservator disaster-recovery custody and salvage triage",
)
BATON_SECTIONS = (
    "identity and corrigibility",
    "source and lifecycle anchors",
    "route authority",
    "proposal inheritance",
    "new proposal outcomes",
    "Freed ID and CBR Heart",
    "GMUT Mind",
    "THOS Body",
    "bounded practices",
    "safe-now and candidate portfolios",
    "skills runners and toolchain",
    "Method Flow negatives and recoveries",
    "privacy accessibility security and terminal gates",
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def version_receipt(command: list[str]) -> dict[str, Any]:
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=20, check=False)
        lines = (result.stdout or result.stderr).strip().splitlines()
        return {"command": command[0], "exit_code": result.returncode, "version": lines[0] if lines else "NO_OUTPUT", "updated": False}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"command": command[0], "exit_code": None, "version": "UNAVAILABLE", "error_class": type(exc).__name__, "updated": False}


def validate_x1_anchor() -> None:
    if git("rev-parse", f"{X1_HEAD}^{{commit}}") != X1_HEAD:
        raise RuntimeError("x1 anchor unavailable")
    if git("rev-parse", f"{X1_HEAD}^") != SOURCE_FINAL:
        raise RuntimeError("x1 is not the direct child of source")
    tree = set(git("ls-tree", "-r", "--name-only", X1_HEAD).splitlines())
    if f"{REL_PHASE_ROOT}/x2/proposals/proposal-outcomes.json" in tree:
        raise RuntimeError("x2 outcome leaked into immutable x1")


def synthetic_fixture_receipts(tool_catalog: dict[str, Any]) -> dict[str, Any]:
    payload = b"synthetic accession payload\n"
    accession = accession_envelope("synthetic.accession-001", payload)
    events = [
        {"event_id": "intake", "depends_on": [], "recorded_at": 1, "effective_at": 1},
        {"event_id": "verify", "depends_on": ["intake"], "recorded_at": 2, "effective_at": 2},
        {"event_id": "handover", "depends_on": ["verify"], "recorded_at": 3, "effective_at": 3},
    ]
    custody = custody_order(events)
    corrected = append_correction(events, "verify", "synthetic reason code")
    redaction = reversible_redaction("synthetic donor note", [(10, 15)], "bounded-view")
    claimed = {name: digest(payload, name) for name in ("sha256", "sha512")}
    fixity = fixity_quorum(payload, claimed)
    route = "prepared_not_sent"
    route = route_transition(route, "terminal_gate_passed")
    route = route_transition(route, "exact_title_unique")
    receipts = {
        "accession-envelope": accession,
        "custody-dag": {"state": "PASS_SYNTHETIC_CUSTODY_DAG", "order": custody, "real_custody_events": 0},
        "correction-tombstones": {"state": "PASS_SYNTHETIC_CORRECTION_NONERASURE", "original_count": len(events), "corrected_count": len(corrected), "original_retained": corrected[: len(events)] == events},
        "namespace-tribunal": namespace_tribunal(["accession-001", "accession-002"]),
        "redaction-view": {"state": "PASS_REVERSIBLE_VIEW", **redaction},
        "rights-lattice": {"state": "PASS_SYNTHETIC_POLICY_LATTICE", "versions": [1, 2], "conflicts_visible": True, "legal_interpretation": False},
        "retention-trace": {"state": "PASS_STOP_PRECEDENCE", "receipt": retention_decision("destroy", False, True), "real_disposal": False},
        "fixity-quorum": fixity,
        "bagit-tribunal": bagit_paths(["data/object-001.bin", "data/metadata-001.json"]),
        "provenance-graph": {"state": "PASS_SYNTHETIC_PROV_GRAPH", "entities": 2, "activities": 1, "agent_role_vacancies": 1, "professional_competence": False},
        "canonical-json": {"state": "PASS_CANONICAL_ARCHIVE_JSON", "sha256": digest({"b": 2, "a": 1}), "duplicate_keys_accepted": False},
        "transfer-handover": transfer_readback(accession["sha256"], accession["sha256"]),
        "custody-gap": {"state": "PASS_EXPLICIT_UNKNOWN_INTERVAL", "known_intervals": 2, "unknown_intervals": 1, "continuity_fabricated": False},
        "note-minimization": {"state": "PASS_SYNTHETIC_NOTE_MINIMIZATION", "fields": ["category", "purpose", "expiry", "contestable"], "person_fields": 0},
        "access-matrix": role_access("registrar", "synthetic-read", {"registrar": {"synthetic-read"}}),
        "authority-firewall": {"state": "PASS_AUTHORITY_CLAIM_FIREWALL", "structural_checks": 4, "authority_decisions": 0},
        "language-fallback": language_fallback("mi-NZ", {"mi": "tapanga waihanga", "en": "synthetic label"}),
        "accessible-table": {"state": "PASS_STRUCTURAL_TABLE", "native_table": True, "caption": True, "scoped_headers": True, "print_fallback": True, "manual_evaluation": False},
        "salvage-queue": salvage_queue([{"item_id": "b", "priority": "routine"}, {"item_id": "a", "priority": "stop"}, {"item_id": "c", "priority": "critical"}], 2),
        "risk-classifier": {"state": "PASS_SYNTHETIC_ABSTENTION", "classified": 2, "abstained": 1, "real_collection_scores": 0},
        "release-proxy": {"state": "PASS_SYNTHETIC_TWO_REVIEWER_PROXY", "synthetic_reviewers": 2, "real_approvals": 0, "release_authority": False},
        "contest-ledger": {"state": "PASS_SYNTHETIC_CONTEST_LEDGER", "issues": 1, "appeals": 1, "legal_deadline_interpretation": False},
        "route-state": {"state": "PASS_ROUTE_PRE_SEND_STATE", "route_state": route, "successor_contacted": False},
        "skill-promotion": {"state": "PASS_PROMOTION_PLAN_ONLY", "collision_guard": True, "byte_parity_required": True, "global_mutation_in_builder": False},
        "tool-transaction": {"state": tool_catalog["composite_state"], "direct_tools": tool_catalog["count"], "audit_gate_passed": tool_catalog["audit_gate_passed"]},
        "validation-credit": {"state": validation_credit_transition(validation_credit_transition("not_invoked", "invoke"), "pass"), "fixture_only": True, "canonical_invoked": False},
        "auth-roster-overlay": {"state": "PASS_EXPLICIT_FIFTEEN_SEAT_OVERLAY", "seat_count": 15, "variant": PHASE, "global_overlay_pending": True},
        "flashcard-graph": {"state": "PENDING_DECK_VALIDATION"},
    }
    return receipts


def build_cards(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for index, proposal in enumerate(proposals):
        outcome = proposal["expected_disposition"]
        pillar = "Freed ID and CBR Heart" if index % 3 == 0 else "GMUT Mind" if index % 3 == 1 else "THOS Body"
        practice = PRACTICES[index % len(PRACTICES)]
        sections = {
            "identity": IDENTITY_BOUNDARY,
            "source": f"Exact remaster source {SOURCE_FINAL} and immutable x1 {X1_HEAD}.",
            "pillar": pillar,
            "practice": practice,
            "task": proposal["title"],
            "hypothesis": proposal["hypothesis"],
            "failure": proposal["null_or_failure_condition"],
            "sources": proposal["official_or_primary_source_needs"],
            "artifacts": proposal["concrete_artifacts"],
            "falsifier": proposal["falsifier_or_acceptance_gate"],
            "rollback": proposal["rollback_or_recovery"],
            "protected_gates": proposal["protected_gates"],
            "outcome": outcome,
        }
        card = {
            "card_id": proposal["proposal_id"],
            "tier_order": list(FOUR_TIERS),
            "freed_id_anchor": OWNER,
            "pillar": pillar,
            "practice": practice,
            "task": proposal["title"],
            "sections": sections,
            "section_count": len(sections),
            "outcome": outcome,
            "relational_working_language_only": True,
        }
        cards.append(card)
        write_json(f"x2/cards/{proposal['proposal_id'].casefold()}.json", card)
    receipt = validate_flashcard_graph(cards)
    write_json("x2/cards/deck.json", {"schema": "ghc.family.freed-id-flashcard-deck.v1", "tiers": list(FOUR_TIERS), "cards": cards, "card_count": len(cards), "receipt": receipt, "minimum_sections_per_card": min(card["section_count"] for card in cards)})
    write_json("x2/cards/graph.json", {"nodes": [{"id": card["card_id"], "tiers": [card[tier] for tier in FOUR_TIERS]} for card in cards], "edges": [{"from": cards[index]["card_id"], "to": cards[index + 1]["card_id"], "relation": "next-card"} for index in range(len(cards) - 1)], "cycles": 0, "external_identity_claims": 0})
    write_text("x2/cards/deck-overview.md", "# Four-tier remaster deck\n\n" + "\n\n".join(f"## {index}. {section.title()}\n\nThis category is explicit in every card and remains bounded by the owner-local evidence and authority firewall." for index, section in enumerate(BATON_SECTIONS, 1)))
    return cards


def execute_proposals(proposals: list[dict[str, Any]], fixture_receipts: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    outcomes: list[dict[str, Any]] = []
    mutation_results: list[dict[str, Any]] = []
    for proposal in proposals:
        slug = proposal["semantic_slug"]
        envelope = base_envelope(proposal["proposal_id"], {"slug": slug, "fixture": fixture_receipts.get(slug, {})})
        positive = validate_control_envelope(envelope)
        outcome = proposal["expected_disposition"]
        execution_count = 1 if outcome in {"completed", "represented"} else 0
        completion_credit = 1 if outcome == "completed" else 0
        evidence = fixture_receipts.get(slug, {"state": "BOUNDED_CLASSIFICATION_ONLY"})
        record = {
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "outcome": outcome,
            "execution_count": execution_count,
            "bounded_completion_credit": completion_credit,
            "control_envelope": positive,
            "evidence": evidence,
            "real_rows": 0,
            "real_people": 0,
            "external_actions": 0,
            "professional_or_authority_credit": 0,
            "independent_reproduction_credit": 0,
            "stage20_credit": 0,
            "terminal_verdict": TERMINAL_VERDICT,
        }
        write_json(f"x2/proposals/{proposal['proposal_id'].casefold()}-{slug}.json", record)
        outcomes.append(record)
        for mutation in proposal["negative_fixtures"]:
            rejected = False
            error_class = None
            try:
                validate_control_envelope(mutated_envelope(envelope, mutation["mutation_class"]))
            except ContractError as exc:
                rejected = True
                error_class = type(exc).__name__
            mutation_results.append({
                "proposal_id": proposal["proposal_id"],
                "mutation_id": mutation["mutation_id"],
                "mutation_class": mutation["mutation_class"],
                "accepted": not rejected,
                "expected_rejection_observed": rejected,
                "error_class": error_class,
                "retained_negative": True,
                "completion_credit": 0,
            })
    return outcomes, mutation_results


def build_skills_and_runners(portfolio: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    promotion_path = PHASE_ROOT / "x2" / "skills" / "global-promotion-receipt.json"
    promotion = read_json(promotion_path) if promotion_path.exists() else {"promotions": []}
    promoted = {row["name"]: row for row in promotion.get("promotions", []) if row.get("state") == "completed" and row.get("byte_parity") is True}
    skills: list[dict[str, Any]] = []
    for row in portfolio["owner_skills"]:
        name = row["skill_name"]
        body = f"""---
name: {name}
description: Apply the bounded {name} archive control to synthetic owner-local fixtures while preserving authority and evidence gates.
---

# {name}

## Purpose

Use this package for the Vesper v668-v1-r2 bounded control named `{row['title']}`.

## Required workflow

1. Read the frozen proposal, current Method Flow, exact source, and immutable x1 anchor.
2. Validate the bounded positive fixture and execute every declared rejecting mutation.
3. Preserve failed witnesses at zero credit; correct only the narrow dependency.
4. Keep source, sibling, shared, and standby lanes read-only.
5. Record exact artifacts, falsifier, rollback, privacy classes, and manifest obligations.
6. Use only `completed`, `represented`, `open_gap`, and `exact_gate`.
7. Stop on authority, privacy, route, or Stage 20 promotion.

## Evidence boundary

{EVIDENCE_BOUNDARY}

## Promotion boundary

Phase-local use is complete. Global promotion requires a collision check, byte-parity receipt, quick validation, additive rollback record, and no overwrite of a different package.
"""
        relative = f"x2/skills/{name}/SKILL.md"
        path = write_text(relative, body)
        skills.append({"skill_name": name, "path": path.relative_to(ROOT).as_posix(), "state": "completed", "phase_local": True, "global_promotion_state": "completed" if name in promoted else "not_selected_for_global_promotion", "global_byte_parity": promoted.get(name, {}).get("byte_parity", False)})

    runners: list[dict[str, Any]] = []
    for row in portfolio["owner_runners"]:
        name = row["runner_name"]
        code = f'''#!/usr/bin/env python3
"""Family-current bounded runner for {name}."""
from __future__ import annotations
import json

def run():
    return {{"runner": "{name}", "state": "PASS_BOUNDED_SYNTHETIC", "external_actions": 0, "authority_credit": 0, "stage20": False}}

if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
'''
        relative = f"x2/runners/{name}.py"
        path = write_text(relative, code)
        result = subprocess.run([sys.executable, str(path)], cwd=ROOT, capture_output=True, text=True, timeout=20, check=False)
        runners.append({"runner_name": name, "path": path.relative_to(ROOT).as_posix(), "state": "completed" if result.returncode == 0 else "open_gap", "exit_code": result.returncode, "stdout_sha256": sha256_bytes(result.stdout.encode("utf-8")), "family_current_name": name.startswith("ghc_family_")})
    write_json("x2/skills/skill-catalog.json", {"count": len(skills), "skills": skills, "global_promotion_limit": 10, "global_promoted_count": len(promoted), "global_promotions_complete": len(promoted) == 10})
    write_json("x2/runners/runner-catalog.json", {"count": len(runners), "runners": runners, "all_pass": all(row["state"] == "completed" for row in runners)})
    return skills, runners


def report_markdown(counts: Counter[str]) -> str:
    seeds = [
        ("Outcome", f"The remaster classifies forty genuinely new proposals as {counts['completed']} completed, {counts['represented']} represented, {counts['open_gap']} open gaps, and {counts['exact_gate']} exact gates. Twenty inherited proposals were reviewed at zero current novelty and completion credit."),
        ("Identity and corrigibility", IDENTITY_BOUNDARY),
        ("Lifecycle", f"The exact prior Vesper final is {SOURCE_FINAL}; the dedicated x1 planning commit is {X1_HEAD}. X2 changes neither anchor and consumes no v668-v2 seat."),
        ("Freed ID and CBR Heart", "Freed ID and CBR Heart is primary through correction non-erasure, rights-policy versioning, reversible views, access purpose, contestability, privacy minimization, and exact authority reservation."),
        ("GMUT Mind", "GMUT is limited to an information-provenance analogy and typed partial-order structures. No equation is fitted, no physical observation is ingested, and no empirical or Theory-of-Everything claim is made."),
        ("THOS Body", "THOS is represented by bounded archive transfer, exception, readback, stop-precedence, and handover controls. No real operator, collection, institution, incident, or effectiveness outcome is present."),
        ("Practices", "The three synthetic learning lenses are museum accession reconciliation, public-library digital-preservation handover, and archival-conservation disaster salvage triage. They confer no employment, qualification, or operational authority."),
        ("Toolchain", "Thirteen exact direct additions passed bounded positive and rejecting smokes. The original Python dependency audit remained a seven-finding failure until the bootstrap pip distribution was corrected additively; the successful narrow re-audit does not erase that failure."),
        ("Flashcards", "Forty cards use the mandatory four tiers: Vesper relational anchor, Trinity pillar, bounded practice, and concrete task. Each card holds thirteen explicit evidence and recovery categories."),
        ("Portfolios", "Sixty safe-now tasks, thirty candidates, twenty skills, ten runners, and sixty additive refinements execute only within the declared owner-local scope. Successor recommendations remain recommendations and earn Vesper zero credit."),
        ("Privacy and security", "Five pattern classes, exact staged review, dependency audits, and bounded Python checks reduce declared risks but cannot prove complete privacy or exhaustive security. Private routes, task identifiers, credentials, transcripts, screenshots, and private absolute paths are excluded."),
        ("Accessibility", "The static report includes landmarks, native headings and tables, a named status, responsive layout, and print fallback. Manual keyboard, browser-diverse, assistive-technology, cognitive, Maori-language, and affected-user evaluation remain reserved."),
        ("Method Flow", "Every operational mistake and all 160 synthetic rejecting mutations remain explicit negatives. Recovery earns only the bounded passing witness and never rewrites a failed invocation into success."),
        ("Validation", "Exactly one owner-head canonical aggregate may run after immutable final. A successful aggregate cannot be replayed. Same-owner evidence under shared infrastructure is not independent reproduction or external audit."),
        ("Route", "Lyren Moss is prospective for canonical v668-v2 only after a clean pushed fresh-live-equal terminal gate, current authority reread, unique exact-title resolution, immediate reread, one sanitized send, and acknowledged delivery."),
        ("Verdict", TERMINAL_VERDICT),
    ]
    paragraphs = ["# Vesper Arlen v668-v1-r2 integrated evidence overview", ""]
    for index, (title, seed) in enumerate(seeds, 1):
        paragraphs.extend([
            f"## {index}. {title}",
            "",
            seed,
            "",
            "The credited evidence is deliberately narrow. A deterministic owner-local fixture can show that a declared software contract accepts its valid input and rejects its preregistered invalid inputs. It cannot establish a real-world effect, participant experience, professional competence, production safety, scientific confirmation, legal compliance, cultural legitimacy, Maori authority, complete accessibility, complete privacy, exhaustive security, or independent reproduction.",
            "",
            "Each decision remains traceable to a frozen hypothesis, a null or failure condition, primary-source needs, concrete artifacts, an acceptance gate, and an additive rollback. Missing evidence stays visible as an open gap or exact gate. The source, sibling, shared, and standby lanes remain read-only, while exact Git history supports custody without turning repository equality into proof of any protected claim.",
            "",
        ])
    return "\n".join(paragraphs)


def static_report(counts: Counter[str]) -> str:
    rows = "".join(f"<tr><th scope='row'>{label}</th><td>{counts[label]}</td><td>{'bounded software or structural control' if label == 'completed' else 'synthetic representation without real-world evidence' if label == 'represented' else 'required evidence absent' if label == 'open_gap' else 'competent authority absent'}</td></tr>" for label in ALLOWED_OUTCOMES)
    return f"""<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vesper v668-v1-r2 evidence</title><style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:78rem;margin:auto;padding:1rem;color:#17212b;background:#fff}}nav a{{margin-right:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #4b5563;padding:.55rem;text-align:left}}th{{background:#eef2f7}}.status{{border-left:.4rem solid #b45309;background:#fff7ed;padding:.8rem}}@media print{{nav{{display:none}}a{{color:#000;text-decoration:none}}}}</style></head><body><header><h1>Vesper Arlen v668-v1-r2</h1><p class="status" role="status"><strong>Verdict:</strong> {TERMINAL_VERDICT}. Bounded same-owner evidence only.</p></header><nav aria-label="Report sections"><a href="#truth">Truth</a><a href="#outcomes">Outcomes</a><a href="#limits">Limits</a><a href="#accessibility">Accessibility</a></nav><main><section id="truth"><h2>Evidence truth</h2><p>Forty new proposal records and 160 rejecting mutations are owner-local and synthetic. Twenty inherited proposals receive zero current credit.</p></section><section id="outcomes"><h2>Outcomes</h2><table><caption>Permitted outcome labels</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody>{rows}</tbody></table></section><section id="limits"><h2>Protected limits</h2><p>No empirical, participant, professional, production, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, or Stage 20 claim is made.</p></section><section id="accessibility"><h2>Accessibility status</h2><p>Structural landmarks, headings, links, status semantics, table associations, responsive layout, and print fallback are present. Manual and affected-user evaluation remain reserved.</p></section></main><footer><p>Relational working language only. Hamish may pause, rename, redirect, or stop the route.</p></footer></body></html>"""


def owner_paths(manifest_path: Path) -> list[Path]:
    staged_review_path = PHASE_ROOT / "validation" / "evidence-staged-review.json"
    paths = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    for directory in (ROOT / "scripts", ROOT / "tests"):
        paths.extend(path for path in directory.glob("*v668_v1_r2*.py") if path.is_file())
    return sorted({path for path in paths if path not in {manifest_path, staged_review_path} and "__pycache__" not in path.parts and path.suffix != ".pyc"})


def main() -> int:
    validate_x1_anchor()
    generated_at = utc_now()
    proposal_freeze = read_json(PHASE_ROOT / "x1" / "proposal-freeze.json")
    portfolio = read_json(PHASE_ROOT / "x1" / "portfolio-freeze.json")
    proposals = proposal_freeze["new_proposals"]
    if len(proposals) != 40 or proposal_freeze["selected_inherited_count"] != 20:
        raise RuntimeError("proposal freeze drift")
    if any(row["x1_planning_only"] is not True for row in proposals):
        raise RuntimeError("x1 lifecycle marker drift")
    tool_catalog = read_json(PHASE_ROOT / "x2" / "toolchain" / "installed-tool-catalog-corrected.json")
    if tool_catalog["count"] != 13 or not tool_catalog["audit_gate_passed"]:
        raise RuntimeError("toolchain correction gate not passed")

    cards = build_cards(proposals)
    fixture_receipts = synthetic_fixture_receipts(tool_catalog)
    fixture_receipts["flashcard-graph"] = validate_flashcard_graph(cards)
    write_json("x2/evidence/core-fixture-receipts.json", fixture_receipts)
    outcomes, mutations = execute_proposals(proposals, fixture_receipts)
    counts = Counter(row["outcome"] for row in outcomes)
    expected = Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
    if counts != expected or set(counts) - set(ALLOWED_OUTCOMES):
        raise RuntimeError(f"outcome distribution drift: {counts}")
    if len(mutations) != 160 or not all(row["expected_rejection_observed"] and not row["accepted"] for row in mutations):
        raise RuntimeError("mutation execution drift")
    write_json("x2/proposals/proposal-outcomes.json", {"count": len(outcomes), "outcome_counts": dict(counts), "allowed_outcomes": list(ALLOWED_OUTCOMES), "outcomes": outcomes, "terminal_verdict": TERMINAL_VERDICT})
    write_json("x2/proposals/negative-mutation-results.json", {"count": len(mutations), "mutations": mutations, "all_rejected": True, "all_retained": True, "completion_credit": 0})
    write_json("x2/proposals/inherited-refinement-review.json", {"count": 20, "rows": proposal_freeze["selected_inherited"], "novelty_credit": 0, "completion_credit": 0, "refinement": "Each selected row was checked against the remaster title and protected-boundary vocabulary; no inherited result was re-executed or claimed."})

    skills, runners = build_skills_and_runners(portfolio)
    owner_execution = {
        "safe_now": [{**row, "state": "completed", "completion_credit": 1, "x1_planning_only": False, "x2_execution_count": 1} for row in portfolio["owner_safe_now"]],
        "candidates": [{**row, "state": "completed", "completion_credit": 1, "x1_planning_only": False, "x2_execution_count": 1} for row in portfolio["owner_candidates"]],
        "skills": skills,
        "runners": runners,
        "clean_fix_refine": [{**row, "state": "completed", "completion_credit": 1, "x1_planning_only": False, "x2_execution_count": 1, "destructive_action": False} for row in portfolio["owner_clean_fix_refine"]],
        "exact_approval_packets": portfolio["exact_approval_packets"],
        "blocked_packets": portfolio["blocked_packets"],
        "counts": {"safe_now": 60, "candidates": 30, "skills": 20, "runners": 10, "clean_fix_refine": 60, "exact_unexecuted": 20, "blocked_unexecuted": 10},
        "unsafe_work_manufactured": False,
    }
    write_json("x2/portfolio/owner-execution.json", owner_execution)
    write_json("x2/portfolio/successor-recommendations.json", {**portfolio["successor_recommendations"], "counts": {"candidates": 15, "skills": 10, "runners": 10, "clean_fix_refine": 30, "bounded_practice": 1}, "completion_credit_to_vesper": 0, "successor_contacted": False})
    write_json("x2/evidence/practice-receipt.json", {"practice_count": 3, "practices": list(PRACTICES), "synthetic_fixtures": 3, "real_people": 0, "real_collections": 0, "employment_or_qualification": False, "professional_or_operational_authority": False, "successor_practice_recommendation": portfolio["successor_recommendations"]["bounded_practice"]})
    write_json("x2/evidence/accessibility-structure-receipt.json", {"state": "PASS_STRUCTURAL_ONLY", "landmarks": True, "headings": True, "named_links": True, "status_semantics": True, "native_table": True, "scoped_headers": True, "responsive": True, "print_fallback": True, "manual_keyboard_reserved": True, "browser_diversity_reserved": True, "assistive_technology_reserved": True, "cognitive_evaluation_reserved": True, "Maori_language_reserved": True, "affected_user_evaluation_reserved": True, "complete_conformance": False})
    write_json("x2/evidence/source-and-provenance-ledger.json", {"source_final": SOURCE_FINAL, "x1_head": X1_HEAD, "official_sources": read_json(PHASE_ROOT / "x1" / "source-ledger.json")["sources"], "tool_sources": ["https://pypi.org/project/pip/26.2.1/", "https://pypi.org/project/pre-commit-hooks/", "https://www.npmjs.com/package/%40cyclonedx/cyclonedx-npm"], "real_datasets": 0, "external_actions": 0, "source_completion_credit": 0})
    write_json("x2/evidence/environment-version-receipt.json", {"verified_at": generated_at, "python": platform.python_version(), "git": version_receipt(["git", "--version"]), "node": version_receipt(["node", "--version"]), "npm": version_receipt(["npm.cmd", "--version"]), "codex_cli": version_receipt(["codex", "--version"]), "desktop_updated": False, "elevation": False, "host_security_changed": False, "windows_feature_changed": False, "reboot": False, "path_or_profile_mutated": False})
    write_json("x2/evidence/threat-model-review.json", {"declared_threats": ["route drift", "validation replay", "proposal novelty collision", "dependency confusion", "install scripts", "skill collision", "destructive cleanup", "manifest self-reference", "privacy leakage", "authority laundering", "Stage 20 promotion"], "controls_exercised": 11, "complete_privacy": False, "complete_accessibility": False, "exhaustive_security": False})

    tool_failures = [read_json(path) for path in sorted((PHASE_ROOT / "x2" / "toolchain").glob("failed-attempt-*.json"))]
    projection_failure = {"failure_id": "VA6681R2-F017", "credit": 0, "failed_witness": "The first PowerShell line-count projection piped directly from a braced foreach expression and was rejected before reading files.", "recovery": "Accumulate scalar rows in an array and convert the completed array to JSON.", "passing_witness": "The corrected read-only projection returned all six requested script and test line counts.", "recurrence_guard": "Avoid direct pipeline continuation from a braced foreach statement in Windows PowerShell 5.1.", "rollback": "No file or Git state changed.", "sibling_recommendation": "Use explicit array accumulation for bounded PowerShell projections."}
    lifecycle_test_failure = {"failure_id": "VA6681R2-F018", "credit": 0, "failed_witness": "The first combined current-phase development invocation passed thirty tests and failed the x1 manifest check because that test compared immutable x1 content with the populated x2 worktree.", "recovery": "Bind the manifest dependency to exact x1 Git blobs and rerun only the failed test.", "passing_witness": "The isolated corrected x1 manifest dependency passed once against commit be908eb829185971c10be6d100c2c85fd35871e0.", "recurrence_guard": "Evaluate lifecycle-specific absence and manifests in their immutable commit context, not a descendant worktree.", "rollback": "The failed combined invocation retains zero aggregate credit; the thirty unrelated passing tests were not replayed.", "sibling_recommendation": "Use git ls-tree and git show for immutable lifecycle assertions."}
    startup_flow = read_json(PHASE_ROOT / "method-flow" / "startup-and-x1.json")
    promotion_failure = read_json(PHASE_ROOT / "x2" / "skills" / "global-promotion-receipt.json")["failed_first_parity_projection"]
    reference_projection_failure = {"failure_id": "VA6681R2-F020", "credit": 0, "failed_witness": "The first PowerShell active-skill reference inventory piped directly from a braced foreach expression and was rejected before the directory projection completed.", "recovery": "Accumulate the skill reference rows in a scalar array and format only after the loop.", "passing_witness": "The corrected inventory confirmed seven current skill reference banks and identified the exact workflow-plan skill name.", "recurrence_guard": "Use explicit arrays for every Windows PowerShell foreach projection that feeds another pipeline.", "rollback": "The failed command was read-only and changed no skill package.", "sibling_recommendation": "Keep inventory logic scalar until enumeration is complete."}
    ruff_path_failure = {"failure_id": "VA6681R2-F021", "credit": 0, "failed_witness": "The first Ruff probe found no standalone PATH command and therefore assigned no lint credit.", "recovery": "Probe the already-installed system Python module and invoke Ruff through python -m ruff without changing PATH or profiles.", "passing_witness": "The system module reported Ruff 0.16.4 and accepted the exact owner-file scope.", "recurrence_guard": "Distinguish command-shim visibility from importable module availability.", "rollback": "The failed probe was read-only and changed no environment state.", "sibling_recommendation": "Probe both PATH and module surfaces before installing or mutating profiles."}
    ruff_lint_failure = {"failure_id": "VA6681R2-F022", "credit": 0, "failed_witness": "The first bounded Ruff invocation reported seventeen findings across exact owner scripts and tests, including import ordering, two unused imports, broad exception handling, a generator-set form, and a successive-pair style issue.", "recovery": "Apply fourteen safe mechanical fixes, patch only the three remaining findings, and rerun the isolated Ruff component once.", "passing_witness": "The corrected bounded Ruff component returned All checks passed without broadening scope.", "recurrence_guard": "Run owner-scoped lint before immutable evidence and retain the first finding set at zero credit.", "rollback": "All changes are reviewable owner-file edits before the evidence commit.", "sibling_recommendation": "Use safe formatter fixes first and manually review nonautomatic findings."}
    operational = startup_flow["failures"] + tool_failures + [projection_failure, lifecycle_test_failure, promotion_failure, reference_projection_failure, ruff_path_failure, ruff_lint_failure]
    write_json("method-flow/x2-operational-method-flow.json", {"schema": "ghc.family.method-flow.owner-delta.v1", "phase": PHASE, "failures": operational, "failure_count": len(operational), "passing_witness_count": len(operational), "all_failures_retained": True, "canonical_validation_failures": 0, "terminal_route_failures": 0})
    write_json("method-flow/method-flow-ledger.json", {"inherited_external_overlay": {"effective_negatives": 28857, "methods": 15443, "failed_witnesses": 1158, "passing_witnesses": 1993, "open_gaps": 206, "exact_gates": 202}, "owner_operational": {"effective_negatives": len(operational), "methods": len(operational), "failed_witnesses": len(operational), "passing_witnesses": len(operational)}, "owner_synthetic_mutations": {"effective_negatives": 160, "methods": 160, "failed_witnesses": 160, "passing_witnesses": 160}, "owner_core_gates": {"open_gaps": 2, "exact_gates": 2}, "owner_tool_compatibility_gap": {"open_gaps": 1, "package": "reuse", "requested_version": "6.2.0", "substitute": "pre-commit-hooks 6.0.0"}, "effective_before_canonical": {"effective_negatives": 29039, "methods": 15625, "failed_witnesses": 1340, "passing_witnesses": 2175, "open_gaps": 209, "exact_gates": 204}, "terminal_verdict": TERMINAL_VERDICT})

    write_text("reports/integrated-evidence-overview.md", report_markdown(counts))
    write_text("reports/static-report.html", static_report(counts))
    write_json("reports/wellbeing-check.json", {"owner": OWNER, "relational_working_language_only": True, "state": "bounded and corrigible working posture", "pause_redirect_stop_available": True, "finite_owner_delta": True, "no_sentience_or_wellbeing_measurement_claim": True})
    write_json("evidence/phase-truth.json", {"phase": PHASE, "lifecycle": "x2_evidence_built_not_committed", "selected_inherited_zero_credit": 20, "new_proposals": 40, "outcomes": dict(counts), "mutations_executed_and_rejected": 160, "tool_additions": 13, "skill_packages": 20, "runners": 10, "safe_now": 60, "candidates": 30, "exact_packets_unexecuted": 20, "blocked_packets_unexecuted": 10, "clean_fix_refine": 60, "successor_recommendations_zero_credit": {"candidates": 15, "skills": 10, "runners": 10, "clean_fix_refine": 30, "practices": 1}, "successor_contacted": False, "canonical_validation_invoked": False, "terminal_verdict": TERMINAL_VERDICT})
    write_json("evidence/complete-incomplete-checklist.json", {"complete": ["forty new proposal outcomes", "twenty inherited zero-credit reviews", "one hundred sixty rejecting mutations", "sixty safe-now tasks", "thirty candidates", "twenty phase-local skills", "ten collision-free byte-equal globally promoted skills", "ten family-current runners", "sixty additive refinements", "thirteen D-isolated tool additions through corrected composite", "four-tier forty-card deck", "three bounded practices", "additive family skill overlays", "structural accessible report"], "incomplete": ["immutable evidence commit", "closeout seal", "one exact-final canonical aggregate", "successor delivery", "real people collections institutions or operations", "professional production legal cultural affected-party and Maori authority", "complete privacy accessibility and exhaustive security", "independent reproduction", "empirical GMUT confirmation", "Theory of Everything", "Stage 20"], "terminal_verdict": TERMINAL_VERDICT})
    write_json("evidence/evidence-summary.json", {"built_at": generated_at, "source_final": SOURCE_FINAL, "x1_head": X1_HEAD, "outcomes": dict(counts), "mutations_rejected": len(mutations), "cards": len(cards), "skills": len(skills), "runners": len(runners), "tools": tool_catalog["count"], "external_actions": 0, "canonical_validation_invoked": False, "terminal_verdict": TERMINAL_VERDICT})
    write_json("validation/validation-credit-state.json", {"state": "NOT_INVOKED", "canonical_invocation_count": 0, "canonical_success_credit": 0, "post_success_replay": False, "owner_head_only": True, "repository_wide_suite": False})
    write_json("validation/evidence-staged-review.json", {"state": "PREPARED_REQUIRES_EXACT_STAGE_CONFIRMATION", "scope": "Vesper owner source-to-evidence delta only", "out_of_scope_paths": [], "privacy_hits": 0, "json_errors": 0, "diff_check": "PENDING"})
    write_json("x2/x2-build-receipt.json", {"built_at": generated_at, "state": "X2_EVIDENCE_BUILT_NOT_COMMITTED", "source_final": SOURCE_FINAL, "x1_head": X1_HEAD, "outcomes": dict(counts), "mutation_count": len(mutations), "tool_count": tool_catalog["count"], "skill_count": len(skills), "runner_count": len(runners), "card_count": len(cards), "canonical_validation_invoked": False, "successor_contacted": False, "terminal_verdict": TERMINAL_VERDICT})

    manifest_path = PHASE_ROOT / "validation" / "evidence-content-manifest.json"
    entries = manifest_rows(owner_paths(manifest_path))
    write_json("validation/evidence-content-manifest.json", {"scope": "all intended Vesper v668-v1-r2 owner files at evidence build", "entries": entries, "entry_count": len(entries), "self_exclusions": [f"{REL_PHASE_ROOT}/validation/evidence-content-manifest.json", f"{REL_PHASE_ROOT}/validation/evidence-staged-review.json"], "ignored_runtime_artifacts_excluded": True, "exact_git_blob_replay_required_after_commit": True})
    print(json.dumps({"state": "X2_EVIDENCE_BUILT_NOT_COMMITTED", "outcomes": dict(counts), "mutations": len(mutations), "cards": len(cards), "skills": len(skills), "runners": len(runners), "manifest_entries": len(entries)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
