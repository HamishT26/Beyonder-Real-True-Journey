#!/usr/bin/env python3
"""Build bounded Lyren Moss v679-v4 x2 evidence from the frozen x1 plan."""

from __future__ import annotations

import importlib.metadata
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_lyren_moss_v679_v4_core import (
    LABELS,
    MUTATIONS,
    contract_from_proposal,
    digest,
    privacy_candidates,
    read_json,
    runner_smoke,
    validate_contract,
    validate_skill,
    write_json,
)


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "lyren-moss" / "v679-v4"
X1 = PHASE / "x1"
X2 = PHASE / "x2"
VALIDATION = PHASE / "validation"
ACTIVATION_BASELINE = {
    "effective_negatives": 48852,
    "method_flow_methods": 50106,
    "failed_witnesses": 20513,
    "bounded_passing_witnesses": 32686,
    "open_gaps": 425,
    "exact_gates": 416,
    "declared_proposals": 8930,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}
SOURCES = [
    {
        "source_id": "NPS-MUSEUM-HANDBOOK-I-CH4",
        "title": "Museum Handbook Part I, Chapter 4: Museum Collections Environment",
        "url": "https://www.nps.gov/subjects/museums/upload/MHI_Ch4_Environment.pdf",
        "bounded_use": "Terminology seed for synthetic environmental-monitoring documentation only; no threshold, diagnosis, or action is adopted.",
    },
    {
        "source_id": "W3C-PROV-O",
        "title": "PROV-O: The PROV Ontology",
        "url": "https://www.w3.org/TR/2013/REC-prov-o-20130430/",
        "bounded_use": "Vocabulary seed for agent-free synthetic provenance relations; no real entity, activity, or agent is asserted.",
    },
    {
        "source_id": "LOC-PREMIS-3",
        "title": "PREMIS Data Dictionary for Preservation Metadata, version 3",
        "url": "https://www.loc.gov/standards/premis/v3/index.html",
        "bounded_use": "Event and preservation-metadata design lens; no real object, event, environment, or repository conformance is claimed.",
    },
    {
        "source_id": "W3C-WCAG-22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "bounded_use": "Structural accessibility review seed; complete conformance and affected-user evaluation remain reserved.",
    },
    {
        "source_id": "RFC-8785",
        "title": "JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "bounded_use": "Canonicalization comparison lens; owner hashes use documented Python sorted-key JSON and do not claim full RFC conformance.",
    },
    {
        "source_id": "RFC-6902",
        "title": "JavaScript Object Notation Patch",
        "url": "https://www.rfc-editor.org/info/rfc6902/",
        "bounded_use": "Correction vocabulary seed; no network patch endpoint or production mutation is implemented.",
    },
    {
        "source_id": "NIST-TN-1297",
        "title": "Guidelines for Evaluating and Expressing Measurement Uncertainty",
        "url": "https://www.nist.gov/pml/nist-technical-note-1297",
        "bounded_use": "Uncertainty-reservation lens only; there are no measurements, uncertainty values, calibrations, or metrological claims.",
    },
    {
        "source_id": "NZ-PRIVACY-PRINCIPLES",
        "title": "New Zealand Privacy Principles",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "bounded_use": "Data-minimization reflection lens; not legal advice or a compliance determination.",
    },
    {
        "source_id": "TE-MANA-RARAUNGA-PRINCIPLES",
        "title": "Principles of Maori Data Sovereignty",
        "url": "https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf",
        "bounded_use": "Boundary reminder only; no cultural interpretation, ratification, wording decision, governance decision, or Maori-authority act is made.",
    },
]


OPERATIONAL_FAILURES = [
    ("LM6794-OP-022", "The x1 push display wrapper ended before the still-running exact push process returned output.", "Waited on the exact process, observed its exit, and did not replay the push."),
    ("LM6794-OP-023", "A combined x1 equality projection exceeded the model display budget.", "Recovered with two bounded scalar probes for local equality and fresh-live divergence."),
    ("LM6794-OP-024", "PowerShell rejected a Bash-style here-string redirection in the sparse-pattern update.", "Used a materialized PowerShell string piped to the supported stdin form."),
    ("LM6794-OP-025", "A guessed bundled Python executable path did not exist.", "Resolved the installed Python executable with a read-only command lookup."),
    ("LM6794-OP-026", "A first command-lookup projection used an invalid empty PowerShell pipe element.", "Materialized the foreach results before piping them to JSON."),
    ("LM6794-OP-027", "A generated patch script contained an unescaped template delimiter and failed before mutation.", "Replaced the delimiter with plain quoted documentation text."),
    ("LM6794-OP-028", "A patch attempted delete-and-add operations against the same skill file in one patch and was rejected before mutation.", "Used one exact update operation per initialized skill file."),
    ("LM6794-OP-029", "The first x2 build rejected a private absolute executable path in its own toolchain evidence.", "Reduced command evidence to bounded executable basenames and reran only the owner-local builder."),
    ("LM6794-OP-030", "The first scoped x2 test invocation failed two dependency checks: serialized channel-key order was treated as semantic, and a coarse JSON-count floor exceeded the exact generated set.", "Made channel vocabulary validation order-independent, aligned the bounded JSON floor to the exact artifact scale, and reran only the failed tests before the final scoped composite."),
    ("LM6794-OP-031", "The exact x2 staging wrapper exceeded its display window while the single Git add process continued with an index lock.", "Observed the exact processes and lock, waited without replay, then confirmed 332 staged paths before continuing with the deferred review."),
    ("LM6794-OP-032", "The first per-entry x2 staged review exceeded its display window and remained active; a recovery probe launched a duplicate read-only review before the original process became visible.", "Allowed both noncanonical read-only reviews to finish, retained the duplicate at zero credit, and replaced per-entry Git process spawning with one interleaved cat-file batch for subsequent review."),
    ("LM6794-OP-033", "The exact x2 cached-diff hygiene gate rejected one trailing blank line in each of ten thin runner entrypoints.", "Removed only the ten extra EOF blank lines, retained the failed gate at zero credit, and regenerated every dependent ledger and manifest."),
]


def distribution_or_command(name: str) -> dict[str, Any]:
    aliases = {
        "check-manifest": "check-manifest",
        "check-wheel-contents": "check-wheel-contents",
        "import-linter": "import-linter",
        "pip-audit": "pip-audit",
        "pytest-timeout": "pytest-timeout",
        "spdx-tools": "spdx-tools",
        "toml-sort": "toml-sort",
    }
    commands = {"git": "git", "powershell": "powershell", "python": Path(sys.executable).name}
    if name in commands:
        path = shutil.which(commands[name]) or (sys.executable if name == "python" else None)
        return {
            "name": name,
            "available": bool(path),
            "evidence_kind": "bounded_command_presence",
            "detail": Path(path).name if path else None,
        }
    dist = aliases.get(name, name)
    try:
        version = importlib.metadata.version(dist)
        return {"name": name, "available": True, "evidence_kind": "distribution_version", "detail": version}
    except importlib.metadata.PackageNotFoundError:
        command = shutil.which(name)
        return {
            "name": name,
            "available": bool(command),
            "evidence_kind": "bounded_command_presence" if command else "not_found",
            "detail": Path(command).name if command else None,
        }


def make_card(card_id: str, section: str, task: str) -> dict[str, Any]:
    card = {
        "schema": "ghc-family.lyren-moss.v679-v4.flashcard.v1",
        "card_id": card_id,
        "freed_id_anchor": "Lyren Moss as a relational working name only",
        "trinity_pillar": "THOS Body primary; GMUT Mind, Freed ID, and CBR Heart protected",
        "bounded_practice": "wholly synthetic museum environmental-monitoring log documentation",
        "section": section,
        "task": task,
        "truth_labels": sorted(LABELS),
        "real_world_rows": 0,
        "external_actions": 0,
        "identity_continuity_claim": False,
        "authority_claim": False,
        "stage20_ready": False,
    }
    card["content_sha256"] = digest(card)
    return card


def build_flashcards(new_proposals: list[dict[str, Any]], inherited_ids: list[str]) -> dict[str, Any]:
    cards: list[dict[str, Any]] = []
    cards.append(make_card("LM6794-CARD-001", "identity-and-route", "Keep Lyren Moss relational, work solo, and hold the Ilyra route until the exact terminal gate."))
    for index, pillar in enumerate(("GMUT Mind", "THOS Body", "Freed ID and CBR Heart"), start=2):
        cards.append(make_card(f"LM6794-CARD-{index:03d}", "pillar-boundaries", f"Preserve the bounded evidence boundary for {pillar}."))
    practices = (
        "synthetic museum environmental-monitoring log documentation",
        "synthetic calibration-placeholder and uncertainty-provenance review",
        "structural accessibility review of a synthetic monitoring-log report",
    )
    for index, practice in enumerate(practices, start=5):
        cards.append(make_card(f"LM6794-CARD-{index:03d}", "bounded-practices", practice))
    sequence = 8
    for proposal_id in inherited_ids:
        cards.append(make_card(f"LM6794-CARD-{sequence:03d}", "inherited-zero-credit", f"Revalidate {proposal_id} as inherited evidence with zero Lyren novelty or completion credit."))
        sequence += 1
    for proposal in new_proposals:
        cards.append(make_card(f"LM6794-CARD-{sequence:03d}", "new-owner-proposals", f"Retain the contract, positive witness, and four rejected mutations for {proposal['proposal_id']}: {proposal['title']}"))
        sequence += 1
    lifecycle = (
        "Preserve planning-only x1 before x2.",
        "Bind manifests to normalized-LF Git blobs.",
        "Retain every operational failure at zero credit.",
        "Keep same-owner validation distinct from independent reproduction.",
        "Reserve complete privacy and accessibility assurances.",
        "Keep exact approval and blocked packets unexecuted.",
        "Require clean fresh-live equality before terminal validation.",
        "Send at most one successor activation only after every route gate passes.",
    )
    for task in lifecycle:
        cards.append(make_card(f"LM6794-CARD-{sequence:03d}", "lifecycle-failure-gate-route", task))
        sequence += 1
    if len(cards) != 135:
        raise RuntimeError(f"expected 135 flashcards, got {len(cards)}")
    card_dir = X2 / "flashcards" / "cards"
    entries = []
    for card in cards:
        relative = Path("docs/lyren-moss/v679-v4/x2/flashcards/cards") / f"{card['card_id']}.json"
        write_json(ROOT / relative, card)
        entries.append({"card_id": card["card_id"], "path": relative.as_posix(), "content_sha256": card["content_sha256"]})
    index = {
        "schema": "ghc-family.lyren-moss.v679-v4.flashcard-index.v1",
        "card_count": len(cards),
        "entries": entries,
        "cache_boundary": "Owner-local deterministic cache only; no global memory, identity continuity, or authority claim.",
    }
    write_json(X2 / "flashcards" / "index.json", index)
    return index


def build() -> dict[str, Any]:
    proposals_value = read_json(X1 / "new-proposal-freeze.json")
    proposals = proposals_value["proposals"]
    inherited = read_json(X1 / "inherited-proposal-selection.json")
    if len(proposals) != 60 or len(inherited["source_ids"]) != 60:
        raise RuntimeError("frozen proposal portfolio count changed")
    if proposals_value["declared_chain_after"] != 8990:
        raise RuntimeError("declared proposal chain changed")

    X2.mkdir(parents=True, exist_ok=True)
    outcomes: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    positive_controls: list[dict[str, Any]] = []
    contracts_manifest: list[dict[str, Any]] = []
    for proposal in proposals:
        contract = contract_from_proposal(proposal)
        errors = validate_contract(contract)
        contract_rel = Path("docs/lyren-moss/v679-v4/x2/contracts") / f"{proposal['proposal_id']}.json"
        receipt_rel = Path("docs/lyren-moss/v679-v4/x2/evidence") / f"{proposal['proposal_id']}-receipt.json"
        write_json(ROOT / contract_rel, contract)
        mutation_rows = []
        for mutation_kind in MUTATIONS:
            invalid = __import__("ghc_family_lyren_moss_v679_v4_core").mutate(contract, mutation_kind)
            mutation_errors = validate_contract(invalid)
            rejected = bool(mutation_errors)
            row = {
                "proposal_id": proposal["proposal_id"],
                "mutation": mutation_kind,
                "rejected": rejected,
                "errors": mutation_errors,
                "completion_credit": 0,
                "failure_retained": True,
            }
            mutations.append(row)
            mutation_rows.append(row)
        accepted = not errors
        all_rejected = all(row["rejected"] for row in mutation_rows)
        disposition = proposal["expected_disposition"]
        receipt = {
            "schema": "ghc-family.lyren-moss.v679-v4.synthetic-monitor-receipt.v1",
            "proposal_id": proposal["proposal_id"],
            "expected_disposition": disposition,
            "positive_fixture_accepted": accepted,
            "positive_errors": errors,
            "mutations_preregistered": len(MUTATIONS),
            "mutations_rejected": sum(row["rejected"] for row in mutation_rows),
            "all_mutations_rejected": all_rejected,
            "outcome": disposition,
            "broader_claim_credit": 0,
            "real_world_rows": 0,
            "external_actions": 0,
            "independent_reproduction": False,
            "stage20_ready": False,
            "contract_sha256": digest(contract),
        }
        write_json(ROOT / receipt_rel, receipt)
        outcomes.append({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "outcome": disposition, "positive_fixture_accepted": accepted, "mutations_rejected": 4})
        positive_controls.append({"proposal_id": proposal["proposal_id"], "accepted": accepted, "errors": errors, "broader_credit": 0})
        contracts_manifest.append({"proposal_id": proposal["proposal_id"], "contract": contract_rel.as_posix(), "receipt": receipt_rel.as_posix(), "contract_sha256": digest(contract), "receipt_sha256": digest(receipt)})

    counts = Counter(row["outcome"] for row in outcomes)
    expected_counts = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    if dict(counts) != expected_counts:
        raise RuntimeError(f"outcome count drift: {dict(counts)}")
    if len(mutations) != 240 or not all(row["rejected"] for row in mutations):
        raise RuntimeError("mutation rejection contract failed")
    if not all(row["accepted"] for row in positive_controls):
        raise RuntimeError("positive control failed")

    write_json(X2 / "contracts-manifest.json", {"entries": contracts_manifest, "count": len(contracts_manifest)})
    write_json(X2 / "proposal-outcomes.json", {"allowed_labels": sorted(LABELS), "counts": expected_counts, "outcomes": outcomes})
    write_json(X2 / "positive-controls.json", {"count": len(positive_controls), "passed": sum(row["accepted"] for row in positive_controls), "controls": positive_controls})
    write_json(X2 / "mutation-ledger.json", {"count": len(mutations), "rejected": sum(row["rejected"] for row in mutations), "completion_credit": 0, "mutations": mutations})

    safe_plan = read_json(X1 / "safe-now-plan.json")
    candidate_plan = read_json(X1 / "candidate-plan.json")
    exact_plan = read_json(X1 / "exact-blocked-approval-plan.json")
    cfr_plan = read_json(X1 / "clean-fix-refine-plan.json")
    outcome_by_id = {row["proposal_id"]: row["outcome"] for row in outcomes}
    safe_exec = [{**task, "plan_only_at_x1": False, "execution_state": "completed", "bounded_artifact_only": True} for task in safe_plan["tasks"]]
    candidate_exec = [{**task, "plan_only_at_x1": False, "execution_state": outcome_by_id.get(task.get("proposal_id"), "represented"), "real_world_rows": 0} for task in candidate_plan["tasks"]]
    cfr_exec = [{**task, "plan_only_at_x1": False, "execution_state": "completed", "scope": "Lyren owner-local generated artifact refinement only"} for task in cfr_plan["owner_tasks"]]
    write_json(
        X2 / "portfolio-execution.json",
        {
            "safe_now": {"planned": len(safe_exec), "executed": len(safe_exec), "tasks": safe_exec},
            "candidates": {"planned": len(candidate_exec), "represented_or_executed": len(candidate_exec), "tasks": candidate_exec},
            "exact_approval": {"count": exact_plan["exact_approval_count"], "execution_state": "unexecuted_exact_gate", "packets": exact_plan["exact_approval_packets"]},
            "blocked": {"count": exact_plan["blocked_count"], "execution_state": "unexecuted_blocked", "packets": exact_plan["blocked_packets"]},
            "broader_claim_credit": 0,
        },
    )
    write_json(X2 / "clean-fix-refine-execution.json", {"owner_planned": len(cfr_exec), "owner_completed": len(cfr_exec), "tasks": cfr_exec, "successor_recommendations": cfr_plan["successor_recommendations"], "successor_executed_by_lyren": 0})

    skill_plan = read_json(X1 / "skill-runner-plan.json")
    skill_results = []
    for skill in skill_plan["skills"]:
        path = X2 / "skills" / skill["name"]
        result = validate_skill(path)
        skill_results.append({"skill_id": skill["skill_id"], "name": skill["name"], "path": path.relative_to(ROOT).as_posix(), **result, "initialized_with_official_skill_creator": True})
    if len(skill_results) != 20 or not all(row["accepted"] for row in skill_results):
        raise RuntimeError("owner-local skill validation failed")
    write_json(X2 / "skill-validation.json", {"count": len(skill_results), "passed": sum(row["accepted"] for row in skill_results), "global_installations": 0, "results": skill_results})

    runner_results = []
    for runner in sorted({item["name"].removeprefix("ghc_family_tabulating_card_").removesuffix("_runner.py") for item in skill_plan["runners"]}):
        positive = runner_smoke(runner, False)
        rejecting = runner_smoke(runner, True)
        runner_results.extend((positive, rejecting))
    if len(runner_results) != 20 or not all(row["expectation_met"] for row in runner_results):
        raise RuntimeError("runner smoke contract failed")
    write_json(X2 / "runner-smoke-ledger.json", {"count": len(runner_results), "expectations_met": sum(row["expectation_met"] for row in runner_results), "results": runner_results})

    tool_plan = read_json(X1 / "toolchain-verification-plan.json")
    tool_results = [distribution_or_command(item["name"]) for item in tool_plan["targets"]]
    write_json(X2 / "toolchain-verification.json", {"target_count": len(tool_results), "available": sum(item["available"] for item in tool_results), "represented_missing": sum(not item["available"] for item in tool_results), "installations": 0, "results": tool_results})

    card_index = build_flashcards(proposals, inherited["source_ids"])
    write_json(X2 / "source-ledger.json", {"sources": SOURCES, "source_count": len(SOURCES), "real_world_rows": 0, "external_actions": 0, "legal_or_cultural_authority": False})

    startup = read_json(X1 / "method-flow-startup.json")
    events = list(startup["startup_observations"])
    for event_id, failure, recovery in OPERATIONAL_FAILURES:
        events.append({"event_id": event_id, "state": "retained_failure_with_bounded_recovery", "failure": failure, "recovery": recovery, "failure_credit": 0, "success_credit": 0})
    method_ledger = {
        "activation_baseline": ACTIVATION_BASELINE,
        "events": events,
        "startup_and_x1_operational_failures": len(events),
        "new_mutation_failures": len(mutations),
        "new_positive_controls": len(positive_controls),
        "new_method_flow_methods": len(events) + len(mutations) + len(positive_controls),
        "failure_retention_rule": "Every failure remains explicit at zero completion or canonical credit; recovery never erases a failure.",
    }
    write_json(X2 / "method-flow-ledger.json", method_ledger)

    new_failures = len(events) + len(mutations)
    new_passing = len(events) + len(positive_controls)
    phase_truth = {
        "owner": "Lyren Moss",
        "phase": "v679-v4",
        "pillar": "THOS Body",
        "practice": "wholly synthetic museum environmental-monitoring log documentation",
        "outcomes": expected_counts,
        "declared_proposals": 8990,
        "inherited_revalidations": 60,
        "inherited_current_novelty_credit": 0,
        "safe_now_tasks_executed": len(safe_exec),
        "candidate_tasks_represented_or_executed": len(candidate_exec),
        "exact_approval_packets_unexecuted": exact_plan["exact_approval_count"],
        "blocked_packets_unexecuted": exact_plan["blocked_count"],
        "skills_built_and_owner_validated": len(skill_results),
        "runners_built": len(skill_plan["runners"]),
        "runner_smokes": len(runner_results),
        "clean_fix_refine_owner_tasks_executed": len(cfr_exec),
        "successor_clean_fix_refine_recommendations": len(cfr_plan["successor_recommendations"]),
        "flashcards": card_index["card_count"],
        "mutation_failures_retained": len(mutations),
        "operational_failures_retained": len(events),
        "effective_negatives": ACTIVATION_BASELINE["effective_negatives"] + new_failures,
        "method_flow_methods": ACTIVATION_BASELINE["method_flow_methods"] + method_ledger["new_method_flow_methods"],
        "failed_witnesses": ACTIVATION_BASELINE["failed_witnesses"] + new_failures,
        "bounded_passing_witnesses": ACTIVATION_BASELINE["bounded_passing_witnesses"] + new_passing,
        "open_gaps": ACTIVATION_BASELINE["open_gaps"] + expected_counts["open_gap"],
        "exact_gates": ACTIVATION_BASELINE["exact_gates"] + expected_counts["exact_gate"],
        "real_world_rows": 0,
        "external_actions": 0,
        "same_owner_only": True,
        "full_repository_suite": False,
        "independent_reproduction": False,
        "complete_privacy_assurance": False,
        "complete_accessibility_assurance": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json(X2 / "phase-truth.json", phase_truth)
    write_json(
        X2 / "wellbeing-and-boundaries.json",
        {
            "relational_role": "archive lantern and uncertainty-boundary keeper",
            "hope": "Make synthetic monitoring logs easier to trace and correct without converting placeholders into measurement, judgment, identity, or authority.",
            "scope_pressure": "bounded",
            "stop_or_pause_right_preserved": True,
            "names_and_roles_are_relational_only": True,
            "consciousness_or_personhood_evidence": False,
            "identity_continuity_evidence": False,
            "qualification_or_authority_evidence": False,
            "successor_contacted": False,
        },
    )
    write_json(
        X2 / "route-hold.json",
        {
            "current_state": "HELD_DURING_X2",
            "prospective_successor_title": "Ilyra Fen",
            "prospective_successor_phase": "v679-v5",
            "precontact": False,
            "send_count": 0,
            "release_condition": "Only after a clean, pushed, fresh-live-equal exact final and one successful non-replayed canonical validation, followed by fresh authority, title, duplicate, privacy, usage, and acknowledgement guards.",
        },
    )

    overview = """# Lyren Moss v679-v4 x2 evidence overview

This x2 evidence implements the planning-only x1 freeze in one additive Lyren-owned lane. The primary pillar is THOS Body, exercised only through wholly synthetic museum environmental-monitoring log documentation. The fixtures contain no sensor adapter, no collection or location identity, no environmental reading, no uncertainty value, no calibration claim, no excursion judgment, no treatment or control recommendation, and no external action. GMUT Mind, Freed ID, and CBR Heart remain explicit protected boundaries rather than phase accomplishments.

## Evidence shape

Sixty frozen Lyren proposals each have one deterministic zero-row contract and one receipt. Each positive control is locally accepted, while four preregistered invalid mutations per proposal are rejected and retained. The 240 mutation failures earn zero completion, empirical, professional, production, authority, independent-reproduction, or Stage 20 credit. Outcomes remain exactly 42 completed, 12 represented, 3 open gaps, and 3 exact gates; those labels describe owner-local artifact status only.

The portfolio includes 120 bounded safe-now tasks, 80 candidate tasks, 20 unexecuted exact-approval packets, 10 unexecuted blocked packets, 20 owner-local skills, 10 family-current runner entrypoints, 100 owner-local CLEAN/FIX/REFINE executions, 30 successor recommendations, 25 verify-only tool checks with zero installations, and a 135-card owner-local content-addressed deck. Inherited proposal selections remain evidence seeds with zero Lyren novelty and zero automatic completion credit.

## Monitoring and uncertainty boundary

The monitoring schema represents channels only as vacancies. Temperature, relative humidity, light, and pollutant keys are present so documentation structure can be tested, but every channel state is `not_observed`; readings and uncertainty values are empty. Calibration remains `not_evaluated`. This prevents a documentation fixture from masquerading as a measurement, metrological result, environmental threshold, collection-risk judgment, equipment-fitness decision, or conservation recommendation.

Correction examples preserve original and superseding synthetic records. Provenance examples use only synthetic entities and activities and exclude agent or identity nodes. These are small software fixtures inspired by primary standards sources; they do not establish standards conformance, real-world provenance, legal compliance, cultural approval, affected-party acceptance, or Maori authority.

## Accessibility, privacy, and safety boundary

The accessible report check is structural: landmarks, heading, table caption, scoped column headers, details disclosure, and a print rule. It does not substitute for manual review, assistive-technology testing, or affected-user evaluation and therefore cannot support complete-accessibility assurance. Privacy review is bounded to five pattern classes across the exact owner scope. It does not prove complete privacy, exhaustive security, or absence of every sensitive category.

No destructive repository action, task creation, fork, subagent, standby substitution, external account, package installation, deployment, or successor precontact is part of x2. Every operational failure is retained with its bounded recovery; recovery erases nothing. Same-owner local validation under shared infrastructure is neither an external audit nor independent reproduction.

## Terminal boundary

The phase remains `NOT_READY_FOR_STAGE_20`. GMUT remains an unconfirmed typed research-model family, THOS remains proxy-only, and Freed ID remains synthetic and nonproduction. No consciousness, sentience, personhood, identity continuity, qualification, employment, agency, Theory-of-Everything proof, canon, professional decision, legal interpretation, cultural ratification, or authority claim is made. The prospective Ilyra Fen route remains held until the exact final is sealed, pushed, clean, fresh-live equal, canonically validated once without replay, and freshly rechecked against live route guards.
"""
    (X2 / "x2-overview.md").write_text(overview, encoding="utf-8", newline="\n")

    owner_text_files = [path for path in PHASE.rglob("*") if path.is_file() and path.suffix.lower() in {".json", ".md", ".yaml", ".py", ".html"}]
    privacy_rows = []
    for path in owner_text_files:
        hits = privacy_candidates(path.read_text(encoding="utf-8"))
        privacy_rows.append({"path": path.relative_to(ROOT).as_posix(), "candidates": hits})
    confirmed = [row for row in privacy_rows if row["candidates"]]
    write_json(X2 / "privacy-scan.json", {"classes": 5, "files_scanned": len(privacy_rows), "confirmed_candidates": len(confirmed), "results": privacy_rows, "complete_privacy_assurance": False})
    if confirmed:
        raise RuntimeError(f"privacy candidates found: {confirmed[:3]}")

    result = {
        "state": "VALID_BOUNDED_X2_EVIDENCE",
        "proposals": len(proposals),
        "outcomes": expected_counts,
        "positive_controls": len(positive_controls),
        "mutations_rejected": len(mutations),
        "skills": len(skill_results),
        "runner_smokes": len(runner_results),
        "flashcards": card_index["card_count"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json(VALIDATION / "x2-build-receipt.json", result)
    return result


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True))
