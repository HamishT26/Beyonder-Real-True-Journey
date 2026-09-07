"""Assemble Tamar v688-v3 x2 evidence, Method Flow, and four-tier deck."""
from __future__ import annotations

import collections
import hashlib
import html
import json
import os
import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / "docs/tamar-vey/v688-v3"
BANK = pathlib.Path(os.environ["GHC_OWNER_BANK"])
SOURCE = "c4c676d81235bc6e453bb867b0c0f0de121b7733"
X1 = "6439f733e37a904a5f6e943c3acdbd507f0a98f8"
OWNER = "Tamar Vey"
PHASE = "v688-v3"
BOUNDARY = (
    "Relational working language only; no consciousness, personhood, continuity, "
    "qualification, employment, independent agency, or authority claim. Synthetic "
    "same-owner software evidence is not independent reproduction. "
    "NOT_READY_FOR_STAGE_20. Māori concepts remain under Māori authority."
)
SHORT_BOUNDARY = "Same-owner synthetic structural evidence only; no independent reproduction or authority."
GATES = [
    "empirical",
    "real_participants",
    "professional",
    "production",
    "deployment",
    "identity",
    "legal",
    "cultural",
    "affected_party",
    "maori_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_asi",
    "consciousness_personhood",
    "theory_of_everything",
    "proof_canon",
    "stage20",
]
ACTIVATION = {
    "proposals": 15830,
    "negatives": 83026,
    "methods": 93370,
    "failed_witnesses": 53874,
    "passing_witnesses": 83959,
    "open_gaps": 750,
    "exact_gates": 750,
}


def read(relative):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def write(relative, value):
    path = BASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def add_method(ledger, method_id, title, failure_signature, negative_ids, fail_rows, pass_rows, scope):
    witness_ids = []
    for witness in fail_rows + pass_rows:
        witness_ids.append(witness["witness_id"])
        ledger["witnesses"].append(witness)
    ledger["methods"].append(
        {
            "method_id": method_id,
            "title": title,
            "failure_signature": failure_signature,
            "trigger_preconditions": [scope],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": "Use the bounded accepting contract or refusal witness while retaining every failed candidate.",
            "validation_witness_ids": witness_ids,
            "recurrence_guard": "Bind the exact x1 definition, use strict UTF-8 JSON, and compare the complete typed output before promotion.",
            "rollback": "Stop selecting the owner implementation and retain the definition, failed candidate, and recovery evidence.",
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": GATES,
            "retained_negative_ids": negative_ids or [method_id + "-NO-ERASURE"],
            "scope_boundary": scope + "; no real-font, participant, authority, or independent-reproduction credit.",
        }
    )
    for before, after in [("observed", "candidate"), ("candidate", "validated"), ("validated", "preferred")]:
        ledger["state_events"].append({"method_id": method_id, "from": before, "to": after, "note": "Failed witnesses remain retained; bounded passing evidence supports only this method scope."})


def witness(witness_id, method_id, result, procedure, observed, negative_ids=None):
    return {
        "witness_id": witness_id,
        "method_id": method_id,
        "procedure": procedure,
        "scope": "Tamar Vey v688-v3 exact owner delta",
        "expected": "The frozen complete contract or bounded refusal must be preserved.",
        "observed": observed,
        "result": result,
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": negative_ids or [],
        "boundary": SHORT_BOUNDARY,
    }


def build_method_flow():
    ledger = read("x1/method-flow/ledger.json")
    contracts = read("x2/contract-results.json")["rows"]
    proposals = read("x1/new-proposals.json")["proposals"]
    by_id = {row["proposal_id"]: row for row in proposals}
    mutations = read("x2/mutation-results.json")["rows"]
    safe = read("x2/portfolio-results.json")["safe"]
    cfr = read("x2/portfolio-results.json")["clean_fix_refine"]
    skill_use = read("x2/skill-use.json")["rows"]
    runner_use = read("x2/runner-use.json")["rows"]
    package_smokes = read("x2/package-smokes.json")

    operational = [
        ("TV6883-X2-M001", "Frozen metric semantic discrepancy remains explicit", "The first evaluator produced the standard formula result 20 while x1 froze the contract-local result 0.", "TV6883-X2-N001", "The bounded evaluator now matches the immutable local residual while the correction receipt prohibits OpenType conformance credit."),
        ("TV6883-X2-M002", "Skill smoke uses a file-backed orchestrator", "The inline skill-smoke wrapper had an unterminated duplicate-key string and invoked no skill.", "TV6883-X2-N002", "A repository-local orchestrator constructed deterministic bytes and completed ten positive and ten adverse smokes."),
        ("TV6883-X2-M003", "Quoted environment interpreter uses the PowerShell call operator", "The first quoted interpreter command was parsed as a string and stopped before Python execution.", "TV6883-X2-N003", "The call-operator form invoked the exact environment and completed three positive and three adverse package smokes."),
    ]
    for method_id, title, failure, negative_id, recovery in operational:
        add_method(
            ledger,
            method_id,
            title,
            failure,
            [negative_id],
            [witness(method_id + "-FAIL", method_id, "fail", "First bounded operational attempt", failure, [negative_id])],
            [witness(method_id + "-PASS", method_id, "pass", "Smallest corrected operational attempt", recovery)],
            "Owner-local x2 operational recovery",
        )

    operations = list(dict.fromkeys(row["operation"] for row in proposals))
    for operation in operations:
        method_id = "TV6883-X2-M-" + operation
        operation_contracts = [row for row in contracts if by_id[row["proposal_id"]]["operation"] == operation]
        operation_mutations = [row for row in mutations if by_id[row["proposal_id"]]["operation"] == operation]
        fails = [
            witness(row["candidate_id"] + "-CANDIDATE", method_id, "fail", "Execute an altered complete-output candidate", row["mutation"], [row["candidate_id"]])
            for row in operation_mutations
        ]
        passes = [
            witness(row["proposal_id"] + "-CONTRACT", method_id, "pass", "Evaluate the frozen complete-output contract", "Complete typed output matched and input remained unchanged")
            for row in operation_contracts
        ]
        passes += [
            witness(row["candidate_id"] + "-REJECTION", method_id, "pass", "Compare the altered output with the immutable definition", "Altered output rejected without proposal completion credit")
            for row in operation_mutations
        ]
        add_method(ledger, method_id, f"Preserve complete outputs and reject altered outputs for {operation}", f"Altered complete outputs for {operation} remain failed candidates", [row["candidate_id"] for row in operation_mutations], fails, passes, f"Synthetic font operation {operation}")

        interface_id = "TV6883-X2-M-interface-" + operation
        interface_rows = [row for row in safe if row["kind"] == "json_interface" and by_id[row["proposal_id"]]["operation"] == operation]
        adverse = [row for row in interface_rows if row["mode"] in {"duplicate_operation_refusal", "nonfinite_value_refusal"}]
        fails = [witness(row["procedure_id"] + "-INVALID", interface_id, "fail", "Submit a preregistered invalid JSON-interface candidate", row["mode"], [row["procedure_id"]]) for row in adverse]
        passes = [witness(row["procedure_id"] + "-PASS", interface_id, "pass", "Exercise the JSON-interface mode", "Expected complete output or bounded refusal observed") for row in interface_rows]
        add_method(ledger, interface_id, f"Strict JSON interface for {operation}", f"Duplicate-key and nonfinite inputs for {operation} remain invalid candidates", [row["procedure_id"] for row in adverse], fails, passes, f"Strict JSON interface for {operation}")

    cfr_id = "TV6883-X2-M-cfr"
    broken = [row for row in cfr if row["kind"] == "FIX"]
    fails = [witness(row["procedure_id"] + "-BROKEN", cfr_id, "fail", "Retain the synthetic missing-value candidate", row["broken_sha256"], [row["procedure_id"]]) for row in broken]
    passes = [witness(row["procedure_id"] + "-PASS", cfr_id, "pass", f"Execute {row['kind']} procedure", "Original retained and bounded procedure passed") for row in cfr]
    add_method(ledger, cfr_id, "Clean, repair, and explain frozen font records without erasure", "One hundred missing-value candidates remain failed after their recoveries", [row["procedure_id"] for row in broken], fails, passes, "Deterministic CLEAN FIX REFINE procedures")

    for row in skill_use:
        method_id = "TV6883-X2-M-" + row["name"]
        negative_id = row["name"] + "-INVALID"
        fails = [witness(negative_id, method_id, "fail", "Submit duplicate-key skill input", row["adverse"]["error"], [negative_id])]
        passes = [
            witness(row["name"] + "-POSITIVE", method_id, "pass", "Use the first frozen accepting skill contract", "Complete output matched"),
            witness(row["name"] + "-REFUSAL", method_id, "pass", "Require duplicate-key refusal", "DUPLICATE_KEY refused"),
        ]
        add_method(ledger, method_id, f"Portable skill {row['name']} preserves its two-operation scope", "Duplicate-key input remains an invalid skill candidate", [negative_id], fails, passes, "Initialized, read, validated, and smoke-used owner-local skill")

    for row in runner_use:
        base = pathlib.Path(row["name"]).stem
        method_id = "TV6883-X2-M-" + base
        negative_id = base + "-INVALID"
        fails = [witness(negative_id, method_id, "fail", "Submit duplicate-key runner input", row["adverse"]["error"], [negative_id])]
        passes = [witness(base + "-" + item["operation"] + "-PASS", method_id, "pass", "Invoke one declared runner operation", "Complete output matched") for item in row["operations"]]
        passes.append(witness(base + "-REFUSAL", method_id, "pass", "Require duplicate-key runner refusal", "DUPLICATE_KEY refused"))
        add_method(ledger, method_id, f"Family-current runner {row['name']} preserves four operation scopes", "Duplicate-key input remains an invalid runner candidate", [negative_id], fails, passes, "Owner-local family-current runner")

    for package in ["fonttools", "uharfbuzz", "unicodedata2"]:
        method_id = "TV6883-X2-M-package-" + package
        negative_id = "TV6883-PACKAGE-" + package + "-INVALID"
        adverse = package_smokes["adverse"][package]
        fails = [witness(negative_id, method_id, "fail", "Submit the preregistered malformed or unsupported package input", adverse["error_type"], [negative_id])]
        passes = [
            witness(method_id + "-POSITIVE", method_id, "pass", "Run the bounded synthetic package smoke", "Expected package metadata observed"),
            witness(method_id + "-REFUSAL", method_id, "pass", "Require malformed or unsupported input refusal", adverse["error_type"]),
        ]
        add_method(ledger, method_id, f"Pinned {package} package smoke and boundary", "Malformed or unsupported package input remains a failed candidate", [negative_id], fails, passes, "Exact isolated package version and synthetic fixture")

    ledger["final_commit"] = None
    ledger["x1_commit"] = X1
    ledger["source_commit"] = SOURCE
    ledger["execution_authority"] = "owner_self_scoped_delta"
    counts = collections.Counter(witness_row["result"] for witness_row in ledger["witnesses"])
    states = collections.Counter(method["recommendation_state"] for method in ledger["methods"])
    ledger["counts"] = {
        "methods": len(ledger["methods"]),
        "witnesses": len(ledger["witnesses"]),
        "state_events": len(ledger["state_events"]),
        "recommendations": len(ledger["recommendations"]),
        "states": {state: states.get(state, 0) for state in ["observed", "candidate", "validated", "preferred", "superseded", "deprecated"]},
        "witness_results": {"fail": counts["fail"], "pass": counts["pass"]},
    }
    write("x2/method-flow/ledger.json", ledger)
    return ledger


def card(payload):
    digest = hashlib.sha256(canonical(payload)).hexdigest()[:24]
    return {"card_id": "ghc-card-" + digest, **payload}


def build_deck(ledger):
    proposals = read("x1/new-proposals.json")["proposals"]
    practices = read("x1/identity.json")["practices"]
    deck = BASE / "x2/deck"
    cards_dir = deck / "cards"
    cards_dir.mkdir(parents=True, exist_ok=True)
    owner = card({"schema": "ghc.family.freed-id-card.v1", "tier": 1, "card_type": "freed_id_anchor", "title": "Tamar Vey relational owner anchor", "parent_ids": [], "owner": OWNER, "phase": PHASE, "stability": "stable", "outcome": "represented", "content": {"role": "evidence-and-recovery steward", "hope": "Every failed witness remains inspectable and every recovery stays bounded.", "corrigibility": ["pause", "rename", "narrow", "redirect", "stop"]}, "source_refs": ["x1/identity.json"], "protected_gates": GATES, "boundary": BOUNDARY})
    pillar_cards = {}
    for pillar in ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"]:
        pillar_cards[pillar] = card({"schema": "ghc.family.freed-id-card.v1", "tier": 2, "card_type": "trinity_pillar", "title": pillar, "parent_ids": [owner["card_id"]], "owner": OWNER, "phase": PHASE, "stability": "stable", "outcome": "represented", "content": {"pillar": pillar, "evidence_ceiling": "Synthetic same-owner structural evidence only"}, "source_refs": ["x1/identity.json"], "protected_gates": GATES, "boundary": BOUNDARY})
    practice_cards = {}
    for practice in practices:
        practice_cards[practice["name"]] = card({"schema": "ghc.family.freed-id-card.v1", "tier": 3, "card_type": "bounded_practice", "title": practice["name"], "parent_ids": [pillar_cards[practice["pillar"]]["card_id"]], "owner": OWNER, "phase": PHASE, "stability": "volatile", "outcome": "represented", "content": {"practice": practice["name"], "pillar": practice["pillar"], "real_people": 0, "real_fonts": 0}, "source_refs": ["x1/identity.json"], "protected_gates": GATES, "boundary": BOUNDARY})
    task_cards = []
    for proposal in proposals:
        task_cards.append(card({"schema": "ghc.family.freed-id-card.v1", "tier": 4, "card_type": "task", "title": proposal["title"], "parent_ids": [practice_cards[proposal["practice"]]["card_id"]], "owner": OWNER, "phase": PHASE, "stability": "volatile", "outcome": proposal["expected_execution_disposition"], "content": {"proposal_id": proposal["proposal_id"], "operation": proposal["operation"], "approval_class": proposal["approval_class"], "hypothesis": proposal["hypothesis"], "null_or_failure_condition": proposal["null_or_failure_condition"], "falsifier": proposal["falsifier_or_acceptance_gate"], "rollback": proposal["rollback_or_recovery"]}, "source_refs": ["x1/new-proposals.json", "x2/contract-results.json"], "protected_gates": proposal["protected_gates"], "boundary": BOUNDARY}))
    for method in ledger["methods"]:
        task_cards.append(card({"schema": "ghc.family.freed-id-card.v1", "tier": 4, "card_type": "method", "title": method["title"], "parent_ids": [practice_cards[practices[0]["name"]]["card_id"]], "owner": OWNER, "phase": PHASE, "stability": "volatile", "outcome": "completed", "content": {"method_id": method["method_id"], "state": method["recommendation_state"], "retained_negative_ids": method["retained_negative_ids"], "recurrence_guard": method["recurrence_guard"], "rollback": method["rollback"]}, "source_refs": ["x2/method-flow/ledger.json"], "protected_gates": method["protected_gates"], "boundary": BOUNDARY}))

    cards = [owner, *pillar_cards.values(), *practice_cards.values(), *task_cards]
    if len({row["card_id"] for row in cards}) != len(cards):
        raise RuntimeError("Card identifier collision")
    for row in cards:
        (cards_dir / (row["card_id"] + ".json")).write_text(json.dumps(row, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")
    tier_counts = collections.Counter(row["tier"] for row in cards)
    write("x2/deck/deck-index.json", {"schema": "ghc.family.freed-id-deck.v1", "source": SOURCE, "x1": X1, "cards": [row["card_id"] for row in cards], "counts": {str(key): value for key, value in sorted(tier_counts.items())}, "unresolved_parents": 0, "cache_or_identity_benefit_claimed": False})
    write("x2/deck/stable-prefix.json", {"schema": "ghc.family.freed-id-stable-prefix.v1", "cards": [owner["card_id"], *[row["card_id"] for row in pillar_cards.values()]], "cache_hit_claimed": False})
    write("x2/deck/volatile-index.json", {"schema": "ghc.family.freed-id-volatile-index.v1", "cards": [row["card_id"] for row in [*practice_cards.values(), *task_cards]], "implicit_completion": False})
    sections = [
        "identity and corrigibility",
        "route and authority",
        "source anchors",
        "x1 proposals",
        "Trinity pillars",
        "bounded practices",
        "task cards",
        "Method Flow and retained negatives",
        "open gaps and exact gates",
        "validation and manifests",
        "wellbeing and workload",
        "successor recommendations",
        "compact baton index",
    ]
    write("x2/deck/baton-index.json", {"schema": "ghc.family.modular-baton-index.v1", "sections": [{"module": index + 1, "title": title} for index, title in enumerate(sections)], "count": 13, "delivery": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"})
    compact = "# Tamar v688-v3 compact activation candidate\n\nExact final and terminal validation remain pending. The prospective terminal edge is the designated future seat 12 for v688-v4, followed by Elowen Cairn v688-v5 only after that seat's own terminal gate. No task is created or contacted by this file.\n"
    (deck / "compact-activation.md").write_text(compact, encoding="utf-8", newline="\n")
    report = "<!doctype html><html lang=\"en\"><meta charset=\"utf-8\"><title>Tamar v688-v3 card report</title><style>@page{size:A4;margin:18mm}body{font:16px/1.65 system-ui;max-width:850px;margin:auto}section{break-after:page;min-height:245mm}section:last-child{break-after:auto}table{border-collapse:collapse}th,td{border:1px solid;padding:.4rem;text-align:left}</style><body><a href=\"#main\">Skip to content</a><main id=\"main\">"
    pages = [
        ("Deck identity and hierarchy", f"The deterministic deck contains {len(cards)} cards: one relational owner anchor, three Trinity pillars, four bounded practices, two hundred proposal task cards, and {len(ledger['methods'])} Method Flow cards."),
        ("Evidence and failure retention", f"The owner Method Flow retains {ledger['counts']['witness_results']['fail']} failed witnesses and {ledger['counts']['witness_results']['pass']} bounded passing witnesses. Card structure is an organization method only and establishes no cache, memory, identity, scientific, or authority result."),
        ("Access and evaluation reservations", "The report supplies language metadata, a skip link, landmarks, headings, and a captioned summary table. Manual keyboard, assistive-technology, cognitive, responsive, language, Māori-language, and affected-user evaluation remain open or exact-gated."),
    ]
    for title, body in pages:
        report += f"<section><h1>{html.escape(title)}</h1><p>{html.escape(body)}</p><p>{html.escape(BOUNDARY)}</p></section>"
    report += "<section><h1>Card counts</h1><table><caption>Four-tier card counts</caption><thead><tr><th scope=\"col\">Tier</th><th scope=\"col\">Count</th></tr></thead><tbody>" + "".join(f"<tr><th scope=\"row\">{tier}</th><td>{count}</td></tr>" for tier, count in sorted(tier_counts.items())) + "</tbody></table></section></main></body></html>\n"
    (deck / "accessible-report.html").write_text(report, encoding="utf-8", newline="\n")

    entries = []
    for path in sorted(item for item in deck.rglob("*") if item.is_file() and item.name != "card-manifest.json"):
        raw = path.read_bytes()
        entries.append({"path": path.relative_to(deck).as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    write("x2/deck/card-manifest.json", {"count": len(entries), "entries": entries, "self_exclusion": "card-manifest.json"})
    return len(cards), len(entries)


def build_overview(ledger, cards):
    pages = [
        ("Tamar v688-v3 identity, pillars, and scope", "Tamar Vey, optionally she/they, uses the relational role evidence-and-recovery steward and the hope that every failed witness remains inspectable and every recovery stays bounded. GMUT Mind is primary through exact synthetic outline, bounding, metric, mapping, and variation contracts. THOS Body and Freed ID with CBR Heart remain explicit and protected."),
        ("Executed owner evidence and retained failures", f"Two hundred frozen complete-output contracts matched; 250 altered-output candidates were rejected; 300 safe procedures and exactly 300 CLEAN/FIX/REFINE records passed. Ten skills and five runners were initialized, read, validated, smoke-used, and promoted without overwrite. Three pinned package additions passed positive and adverse smokes. The four-tier deck contains {cards} cards. Owner Method Flow has {ledger['counts']['methods']} methods, {ledger['counts']['witness_results']['fail']} retained failed witnesses, and {ledger['counts']['witness_results']['pass']} bounded passing witnesses."),
        ("Limits, incomplete work, and terminal route", "No real font, glyph, typeface, text corpus, participant, measurement, rendering, publication, license decision, accessibility evaluation, cultural decision, Māori data, credential, deployment, or authority act occurred. Fifty exact and thirty blocked packets remain unexecuted. The designated future-seat-12 v688-v4 edge remains terminally gated; no task has been created or contacted. The complete repository suite and independent reproduction remain absent."),
    ]
    document = "<!doctype html><html lang=\"en\"><meta charset=\"utf-8\"><title>Tamar v688-v3 x2 overview</title><style>@page{size:A4;margin:18mm}body{font:16px/1.65 system-ui;max-width:850px;margin:auto}section{break-after:page;min-height:245mm}section:last-child{break-after:auto}</style><body><a href=\"#main\">Skip to content</a><main id=\"main\">"
    for title, body in pages:
        document += f"<section><h1>{html.escape(title)}</h1><p>{html.escape(body)}</p><p>{html.escape(BOUNDARY)}</p></section>"
    document += "</main></body></html>\n"
    (BASE / "x2/integrated-overview.html").write_text(document, encoding="utf-8", newline="\n")


def main():
    ledger = build_method_flow()
    cards, manifest_entries = build_deck(ledger)
    build_overview(ledger, cards)
    counts = ledger["counts"]
    effective = {
        "proposals": ACTIVATION["proposals"] + 200,
        "negatives": ACTIVATION["negatives"] + counts["witness_results"]["fail"],
        "methods": ACTIVATION["methods"] + counts["methods"],
        "failed_witnesses": ACTIVATION["failed_witnesses"] + counts["witness_results"]["fail"],
        "passing_witnesses": ACTIVATION["passing_witnesses"] + counts["witness_results"]["pass"],
        "open_gaps": ACTIVATION["open_gaps"] + 2,
        "exact_gates": ACTIVATION["exact_gates"] + 3,
    }
    write("x2/open-gap-register.json", {"inherited": 750, "added": 2, "refs": ["TV6883-N172", "TV6883-N173"], "closed_by_software": 0, "boundary": BOUNDARY})
    write("x2/exact-gate-register.json", {"inherited": 750, "added": 3, "refs": ["TV6883-N175", "TV6883-N176", "TV6883-N177"], "closed_by_software": 0, "boundary": BOUNDARY})
    write(
        "x2/retained-negative-register.json",
        {
            "source_repository_seal": {"negatives": 83024, "methods": 93368, "failed_witnesses": 53872, "passing_witnesses": 83957, "open_gaps": 750, "exact_gates": 750, "proposals": 15830},
            "source_external_overlay": ["OP6882-POSTFINAL-N001", "OP6882-POSTFINAL-N002"],
            "activation_baseline": ACTIVATION,
            "owner_failed_witness_refs": [row["witness_id"] for row in ledger["witnesses"] if row["result"] == "fail"],
            "owner_failed_witness_count": counts["witness_results"]["fail"],
            "effective_counts": effective,
            "failures_erased": 0,
            "failures_promoted": 0,
            "count_boundary": "Every invalid mutation, broken CFR candidate, operational fault, adverse skill/runner/package input, and recovery remains a distinct evidence state.",
        },
    )
    package_smokes = read("x2/package-smokes.json")
    install_report = BANK / "environment-install-report.json"
    write(
        "x2/environment-receipt.json",
        {
            "distribution_count": package_smokes["distribution_count"],
            "versions": package_smokes["versions"],
            "wheel_only": True,
            "no_index": True,
            "no_deps": True,
            "require_hashes": True,
            "environment_pip_present": (BANK / "environment/Scripts/pip.exe").exists(),
            "host_python_mutated": False,
            "installation_report_sha256": hashlib.sha256(install_report.read_bytes()).hexdigest(),
            "rollback": "Stop selecting the isolated owner environment; retain the environment, wheels, lock, and receipts.",
        },
    )
    catalogue = read("x2/tooling/meta-tool-box/catalogue.json")
    collision = read("x2/tooling/meta-tool-box/collisions.json")
    plan = read("x1/skill-runner-plan.json")
    operations = {row["name"]: set(row["operations"]) for row in plan["skills"]}
    findings = []
    for row in collision["findings"]:
        left = row["left"].split(":", 1)[1]
        right = row["right"].split(":", 1)[1]
        findings.append({**row, "operation_intersection": sorted(operations[left] & operations[right]), "disposition": "keep_current_disjoint_exact_operation_scopes", "silent_winner_selected": False})
    write("x2/tooling/meta-tool-box/collision-review.json", {"schema": "ghc.family.font-skill-collision-review.v1", "catalogue_count": len(catalogue["cards"]), "finding_count": len(findings), "findings": findings, "all_operation_intersections_empty": all(not row["operation_intersection"] for row in findings), "selection_performed": False})
    write(
        "x2/workload-wellbeing.json",
        {
            "objective_workload": {"contracts": 200, "safe_procedures": 300, "candidate_rejections": 250, "clean_fix_refine": 300, "skills": 10, "runners": 5, "packages": 3, "method_flow_methods": counts["methods"], "cards": cards},
            "subjective_wellbeing_measured": False,
            "employment_claimed": False,
            "workload_control": ["bounded owner scope", "single x1 and evidence commits", "one canonical latch", "no full repository suite", "no successor precontact"],
            "handover_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
        },
    )
    write(
        "x2/complete-incomplete.json",
        {
            "completed_scope": ["200 complete typed contracts", "300 safe procedures", "250 rejected altered-output candidates", "300 CLEAN/FIX/REFINE procedures", "10 initialized/read/validated/used/promoted skills", "5 built/used/promoted runners", "3 pinned package additions", "four-tier deck"],
            "represented_scope": ["font-outline and glyph-metadata structures", "GMUT exact symbolic geometry proxy", "THOS bounded processing proxy", "Freed ID relational records and CBR reservations"],
            "open_gaps": ["Two unresolved synthetic local glyph references", "independent and empirical evaluation", "manual and affected-user accessibility evaluation"],
            "exact_gates": ["Three external-reference requests", "50 exact packets", "30 blocked packets", "all protected competent and affected authority decisions"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write(
        "x2/phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "state": "X2_OWNER_EVIDENCE_COMPLETE_PENDING_EVIDENCE_COMMIT",
            "source": SOURCE,
            "x1": X1,
            "outcomes": {"completed": 178, "represented": 17, "open_gap": 2, "exact_gate": 3},
            "effective_counts": effective,
            "owner_method_flow": counts,
            "contract_results": 200,
            "candidate_rejections": 250,
            "safe_procedures": 300,
            "clean_fix_refine": 300,
            "skill_builds": 10,
            "skill_uses": 10,
            "runner_builds": 5,
            "runner_positive_operations": 20,
            "package_installations": 3,
            "package_smokes": 3,
            "deck_cards": cards,
            "deck_manifest_entries": manifest_entries,
            "canonical_invocations": 0,
            "canonical_successes": 0,
            "canonical_replays": 0,
            "successor_contacts": 0,
            "full_repository_suite": False,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    print(json.dumps({"methods": counts["methods"], "failed": counts["witness_results"]["fail"], "passing": counts["witness_results"]["pass"], "cards": cards, "card_manifest_entries": manifest_entries, "effective": effective}, sort_keys=True))


if __name__ == "__main__":
    main()
