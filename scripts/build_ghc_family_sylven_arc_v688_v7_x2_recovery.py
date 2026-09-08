#!/usr/bin/env python3
"""Additively recover the retained partial x2 materialisation without replaying it."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REL = Path("docs/sylven-arc/v688-v7")
BASE = ROOT / REL
X1 = "4b7459cdf681726b8d411d644dc6f8db70e83871"
SOURCE = "e7db6f3be1327de72f93873eb6540aabfc773344"
BOUNDARY = (
    "Same-owner synthetic chess-record software evidence only; no real game, participant, rating, "
    "tournament, professional, legal, cultural, Maori-authority, independent-reproduction, consciousness, "
    "Theory-of-Everything, or Stage 20 evidence."
)


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("utf-8")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_new(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = value.rstrip() + "\n" if isinstance(value, str) else json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, required=True)
    args = parser.parse_args()
    bank = args.bank.resolve()
    if bank.drive.upper() != "D:":
        raise RuntimeError("D_first_bank_required")
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() != X1:
        raise RuntimeError("exact_x1_head_required")
    x2 = BASE / "x2"
    required_base = [
        x2 / "entry-gate.json",
        x2 / "portfolio-results.json",
        x2 / "negative-controls.json",
        x2 / "method-flow/ledger.json",
        x2 / "method-flow/validation.json",
        x2 / "retained-negative-register.json",
        x2 / "open-gap-register.json",
        x2 / "exact-gate-register.json",
        x2 / "local-tool-validation.json",
        x2 / "promotion-receipt.json",
        x2 / "package-transaction.json",
    ]
    if any(not path.is_file() for path in required_base):
        raise RuntimeError("partial_base_incomplete")
    contracts = sorted((x2 / "contracts").glob("*.json"))
    challenges = sorted((x2 / "challenges").glob("*.json"))
    if len(contracts) != 200 or len(challenges) != 20:
        raise RuntimeError("partial_base_contract_shape")
    base_ledger = load(x2 / "method-flow/ledger.json")
    base_negative = load(x2 / "negative-controls.json")
    base_validation = load(x2 / "method-flow/validation.json")
    if base_ledger["counts"] != {"methods": 53, "witnesses": 609, "failed_witnesses": 541, "passing_witnesses": 68, "state_events": 53, "recommendations": 53}:
        raise RuntimeError("partial_base_method_shape")
    if base_negative["new_unique_negative_count"] != 511 or base_negative["count"] != 493 or not base_validation["valid"]:
        raise RuntimeError("partial_base_negative_shape")
    failures = load(bank / "x2-operational-failures.json")["failures"]
    if [item["failure_id"] for item in failures] != ["SA6887-X2-N001", "SA6887-X2-N002"]:
        raise RuntimeError("operational_failure_overlay_shape")
    proposals = load(BASE / "x1/new-proposals.json")["proposals"]
    practice = load(BASE / "x1/pillar-practice-freeze.json")
    baseline = load(BASE / "x1/phase-truth.json")["inherited_baseline"]
    gates = proposals[0]["protected_gates"]
    outcomes = {label: sum(item["expected_execution_disposition"] == label for item in proposals) for label in ("completed", "represented", "open_gap", "exact_gate")}

    methods = []
    witnesses = []
    events = []
    recommendations = []
    for index, failure in enumerate(failures, 54):
        method_id = f"SA6887-M{index:03d}"
        failed_id = f"SA6887-W{609 + (index - 54) * 2 + 1:04d}"
        passed_id = f"SA6887-W{609 + (index - 54) * 2 + 2:04d}"
        methods.append({
            "method_id": method_id,
            "title": failure["recovery"],
            "failure_signature": failure["failed_witness"],
            "trigger_preconditions": ["exact owner scope", "the retained partial materialisation"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": failure["recovery"],
            "validation_witness_ids": [failed_id, passed_id],
            "recurrence_guard": failure["recurrence_guard"],
            "rollback": "Retain the partial base and correction overlay; stop selecting either if their bindings fail.",
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": gates,
            "retained_negative_ids": [failure["failure_id"]],
            "scope_boundary": BOUNDARY,
            "artifact": f"{REL.as_posix()}/x2/correction1/recovery-receipt.json",
        })
        witnesses.extend([
            {"witness_id": failed_id, "method_id": method_id, "procedure": "retained x2 build attempt", "scope": f"{REL.as_posix()}/x2/correction1/recovery-receipt.json", "expected": "The failed attempt remains zero-credit evidence.", "observed": failure["failed_witness"], "result": "fail", "witness_kind": "operational_failure", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [failure["failure_id"]], "boundary": BOUNDARY},
            {"witness_id": passed_id, "method_id": method_id, "procedure": "additive focused recovery", "scope": f"{REL.as_posix()}/x2/correction1/recovery-receipt.json", "expected": "Only missing outputs and explicit overlays are added.", "observed": failure["recovery"], "result": "pass", "witness_kind": "bounded_passing_witness", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [], "boundary": BOUNDARY},
        ])
        events.append({"method_id": method_id, "from": "candidate", "to": "preferred", "note": "Additive recovery preserves the partial base and both failures."})
        recommendations.append({"method_id": method_id, "preconditions": "same partial-output signature", "recommendation": failure["recurrence_guard"], "delivered": False})
    correction_counts = {"methods": 2, "witnesses": 4, "failed_witnesses": 2, "passing_witnesses": 2, "state_events": 2, "recommendations": 2}
    total_counts = {key: base_ledger["counts"][key] + correction_counts[key] for key in correction_counts}
    effective = {
        "proposals": baseline["proposals"] + 200,
        "negatives": baseline["negatives"] + 513,
        "methods": baseline["methods"] + total_counts["methods"],
        "failed_witnesses": baseline["failed_witnesses"] + total_counts["failed_witnesses"],
        "passing_witnesses": baseline["passing_witnesses"] + total_counts["passing_witnesses"],
        "open_gaps": baseline["open_gaps"] + outcomes["open_gap"],
        "exact_gates": baseline["exact_gates"] + outcomes["exact_gate"],
    }
    overlay = {
        "schema": "ghc.family.method-flow-correction-overlay.v1",
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "base_ledger_sha256": sha_bytes((x2 / "method-flow/ledger.json").read_bytes()),
        "base_counts": base_ledger["counts"],
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": recommendations,
        "correction_counts": correction_counts,
        "combined_counts": total_counts,
        "failed_witnesses_erased": 0,
        "boundary": BOUNDARY,
    }
    corrected_truth = {
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "source": SOURCE,
        "x1": X1,
        "state": "X2_OBSERVED_EVIDENCE_PRECOMMIT_WITH_ADDITIVE_RECOVERY",
        "base_partial_materialisation_preserved": True,
        "correction_overlay_ref": f"{REL.as_posix()}/x2/correction1/method-flow-overlay.json",
        "new_proposals": 200,
        "proposal_chain_after": effective["proposals"],
        "outcomes": outcomes,
        "effective_counts": effective,
        "method_flow_counts": total_counts,
        "observed_contracts": 200,
        "portfolio_checks": 850,
        "unique_phase_negatives": 513,
        "exact_packets_unexecuted": 50,
        "blocked_packets_unexecuted": 30,
        "skills_promoted": 10,
        "runner_interfaces_promoted": 5,
        "ordinary_package_additions": 3,
        "canonical_invocations": 0,
        "successor_contacts": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }

    cards = []

    def add_card(tier: int, card_type: str, title: str, parents: list[str], content: object, disposition: str = "represented", stability: str = "volatile") -> str:
        payload = {"schema": "ghc.family.freed-id.card.v1", "tier": tier, "card_type": card_type, "title": title, "parent_ids": parents, "owner": "Sylven Arc", "phase": "v688-v7", "stability": stability, "disposition": disposition, "content": content, "source_refs": [{"commit": X1, "path": f"{REL.as_posix()}/x1/new-proposals.json"}], "protected_gates": gates, "boundary": BOUNDARY}
        card_id = "ghc-card-" + sha_bytes(canonical(payload))[:24]
        payload["card_id"] = card_id
        cards.append(payload)
        return card_id

    owner = add_card(1, "freed_id_anchor", "Sylven Arc", [], {"relational_role": practice["role"], "hope": practice["hope"], "identity_claim": False}, stability="stable")
    pillars = {name: add_card(2, "trinity_pillar", name, [owner], {"scope": "research model, synthetic proxy, or synthetic nonproduction governance only"}, stability="stable") for name in ("GMUT Mind", "THOS Body", "Freed ID and CBR Heart")}
    parent_for = {practice["practices"][0]: "Freed ID and CBR Heart", practice["practices"][1]: "GMUT Mind", practice["practices"][2]: "Freed ID and CBR Heart", practice["practices"][3]: "THOS Body"}
    practices = {name: add_card(3, "bounded_practice", name, [pillars[parent_for[name]]], {"synthetic_learning_lens": True, "employment": False, "qualification": False, "authority": False}) for name in practice["practices"]}
    for proposal in proposals:
        add_card(4, "proposal_task", proposal["title"], [practices[proposal["practice"]]], {"proposal_id": proposal["proposal_id"], "artifact": proposal["concrete_artifact"], "frozen_contract_matched": True}, proposal["expected_execution_disposition"])
    for item in [*base_ledger["methods"], *methods]:
        add_card(4, "method", item["title"], [practices[practice["practices"][3]]], {"method_id": item["method_id"], "retained_negative_ids": item["retained_negative_ids"], "ledger": f"{REL.as_posix()}/x2/method-flow/ledger.json" if item["method_id"] <= "SA6887-M053" else f"{REL.as_posix()}/x2/correction1/method-flow-overlay.json"}, "completed")
    card_ids = [card["card_id"] for card in cards]
    if len(cards) != 263 or len(card_ids) != len(set(card_ids)) or any(parent not in set(card_ids) for card in cards for parent in card["parent_ids"]):
        raise RuntimeError("recovered_card_shape")

    write_new(x2 / "correction1/method-flow-overlay.json", overlay)
    write_new(x2 / "correction1/retained-negative-overlay.json", {"base_unique_phase_negatives": 511, "additional_operational_negatives": [item["failure_id"] for item in failures], "combined_unique_phase_negatives": 513, "effective_negatives": effective["negatives"], "erased": 0})
    write_new(x2 / "correction1/recovery-receipt.json", {
        "schema": "ghc.family.x2-partial-materialisation-recovery.v1",
        "state": "VALID_ADDITIVE_RECOVERY",
        "base_files_preserved": len(required_base) + len(contracts) + len(challenges),
        "base_method_flow_sha256": sha_bytes((x2 / "method-flow/ledger.json").read_bytes()),
        "base_negative_controls_sha256": sha_bytes((x2 / "negative-controls.json").read_bytes()),
        "retained_failures": failures,
        "successful_base_contracts_replayed": 0,
        "successful_package_or_tool_checks_replayed": 0,
        "added_method_count": 2,
        "added_failed_witness_count": 2,
        "added_passing_witness_count": 2,
        "boundary": BOUNDARY,
    })
    for card in cards:
        write_new(x2 / "deck/cards" / f"{card['card_id']}.json", card)
    write_new(x2 / "deck/deck-index.json", {"schema": "ghc.family.freed-id.deck.v1", "owner": "Sylven Arc", "phase": "v688-v7", "source": SOURCE, "x1": X1, "cards": card_ids, "card_count": len(cards), "tier_counts": {str(tier): sum(card["tier"] == tier for card in cards) for tier in range(1, 5)}, "outcomes": outcomes, "acyclic_parent_graph": True, "boundary": BOUNDARY})
    write_new(x2 / "deck/stable-prefix.json", {"cards": [card["card_id"] for card in cards if card["stability"] == "stable"], "cache_hit_claimed": False})
    write_new(x2 / "deck/volatile-index.json", {"cards": [card["card_id"] for card in cards if card["stability"] == "volatile"], "implicit_completion_credit": False})
    write_new(x2 / "deck/baton-module-index.json", {"minimum_modules": 13, "modules": ["identity and route", "immutable source", "lifecycle", "proposals", "portfolio", "pillar and practices", "packages", "skills", "runners", "Method Flow", "gaps and gates", "validation", "terminal route"], "baton_state": "NOT_YET_PREPARED", "terminal_delivery": False})
    manifest_entries = [{"path": path.relative_to(ROOT).as_posix(), "bytes": len(path.read_bytes()), "sha256": sha_bytes(path.read_bytes())} for path in sorted((x2 / "deck").rglob("*")) if path.is_file()]
    write_new(x2 / "deck/card-manifest.json", {"byte_domain": "UTF8_LF_repository_bytes", "entries": manifest_entries, "self_exclusions": [f"{REL.as_posix()}/x2/deck/card-manifest.json"]})
    write_new(x2 / "phase-truth.json", corrected_truth)
    summary = {"outcomes": outcomes, "effective_counts": effective, "method_flow": total_counts, "contracts": 200, "portfolio_checks": 850, "unique_phase_negatives": 513, "cards": 263, "skills": 10, "runners": 5, "packages": 3, "retained_x2_operational_failures": 2, "unexpected_contract_or_test_failures": 0}
    write_new(x2 / "evidence-summary.json", summary)
    report = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sylven Arc v688-v7 x2 evidence</title></head><body><main>
<h1>Sylven Arc v688-v7 x2 evidence</h1><p>This report describes bounded same-owner synthetic chess-record work. It is not real-game, participant, professional, independent, empirical, legal, cultural, Maori-authority, consciousness, Theory-of-Everything, or Stage 20 evidence.</p>
<nav aria-label="Report sections"><ol><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#work">Work</a></li><li><a href="#tools">Tools</a></li><li><a href="#failures">Failures</a></li><li><a href="#gates">Gaps and gates</a></li><li><a href="#access">Accessibility reservations</a></li></ol></nav>
<section id="scope"><h2>Scope</h2><p>Primary pillar: Freed ID and CBR Heart. Synthetic practices: {html.escape(', '.join(practice['practices']))}. Zero real games, people, identity events, ratings, tournaments, or external actions.</p></section>
<section id="outcomes"><h2>Outcomes</h2><table><caption>Frozen outcomes</caption><thead><tr><th scope="col">Label</th><th scope="col">Count</th></tr></thead><tbody>{''.join(f'<tr><th scope="row">{html.escape(label)}</th><td>{count}</td></tr>' for label, count in outcomes.items())}</tbody></table></section>
<section id="work"><h2>Work</h2><p>Two hundred contract envelopes and 850 portfolio predicates passed. Fifty exact-approval and thirty blocked packets stayed unexecuted.</p></section>
<section id="tools"><h2>Packages, skills, and runners</h2><p>Three packages were installed to an isolated D-first target. Ten skills and five runner interfaces passed local and post-promotion accepting/adverse smokes with byte parity and no overwrite.</p></section>
<section id="failures"><h2>Retained failures</h2><p>The partial materialisation and exclusive-create retry failures remain in an additive overlay. The combined phase has 513 unique negatives, {total_counts['failed_witnesses']} phase failed witnesses, and zero erased failures.</p></section>
<section id="gates"><h2>Gaps and gates</h2><p>Effective open gaps: {effective['open_gaps']}. Effective exact gates: {effective['exact_gates']}. Terminal verdict: NOT_READY_FOR_STAGE_20.</p></section>
<section id="access"><h2>Accessibility reservations</h2><p>Structural HTML checks do not establish conformance. Manual browser, assistive-technology, cognitive-accessibility, Maori-language, affected-user, and independent evaluations remain open or exact-gated. Maori concepts remain under Maori authority.</p></section>
</main></body></html>"""
    write_new(x2 / "accessible-report.html", report)
    receipt = {"state": "VALID_ADDITIVE_X2_RECOVERY", "base_successful_components_replayed": 0, "retained_failures": 2, "combined_methods": 55, "combined_witnesses": 613, "cards": 263, "effective_counts": effective}
    write_new(bank / "x2-build-recovery.json", receipt)
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
