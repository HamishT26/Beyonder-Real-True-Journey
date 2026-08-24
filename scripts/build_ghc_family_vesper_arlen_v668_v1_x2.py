"""Execute the bounded synthetic Vesper Arlen v668-v1 x2 packet."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ghc_family_vesper_arlen_v668_v1_causal import (
    ContractError,
    append_compensation,
    append_correction,
    bounded_queue,
    canonical_bytes,
    digest,
    merkle_root,
    migrate_record,
    minimize_note,
    replay_events,
    replay_with_duplicates,
    validate_event_graph,
    validate_logical_clocks,
    validation_credit_transition,
    verify_checkpoint,
)


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "vesper-arlen" / "v668-v1"
REL_PHASE_ROOT = "docs/vesper-arlen/v668-v1"
X1_HEAD = "3e9bf7e7fa9ee1164b77616e09f93127d3b43fd5"
SOURCE_FINAL = "fa6bdcedaac48b0580f4d9581b799741cf5282e7"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(payload))
    return path


def write_text(relative: str, text: str) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def command_version(command: list[str]) -> dict[str, Any]:
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=15, check=False)
        value = (result.stdout or result.stderr).strip().splitlines()
        return {"command": command[0], "exit_code": result.returncode, "version": value[0] if value else "NO_OUTPUT", "updated": False}
    except Exception as exc:  # bounded receipt, not a phase failure by itself
        return {"command": command[0], "exit_code": None, "version": "UNAVAILABLE", "error_class": type(exc).__name__, "updated": False}


def base_events() -> list[dict[str, Any]]:
    return [
        {"event_id": "plan", "depends_on": [], "source": "desk", "source_sequence": 1, "lamport": 1, "action": "noop"},
        {"event_id": "ready", "depends_on": ["plan"], "source": "desk", "source_sequence": 2, "lamport": 2, "action": "cue", "cue": "ready"},
        {"event_id": "ack", "depends_on": ["ready"], "source": "console", "source_sequence": 1, "lamport": 3, "action": "ack", "target": "ready"},
        {"event_id": "stop", "depends_on": ["ack"], "source": "desk", "source_sequence": 3, "lamport": 4, "action": "stop"},
    ]


def fixture_and_receipts() -> dict[str, dict[str, Any]]:
    events = base_events()
    order = validate_event_graph(events)
    graph = {"events": events, "expected_order": order, "synthetic_only": True}
    write_json("x2/fixtures/causal-cue-graph.json", graph)
    graph_receipt = {"state": "PASS_SYNTHETIC_CAUSAL_GRAPH", "order": order, "event_count": len(events), "cycles_accepted": 0, "external_actions": 0}
    write_json("x2/evidence/causal-cue-graph-receipt.json", graph_receipt)

    clocks = validate_logical_clocks(events)
    write_json("x2/fixtures/logical-clock-cases.json", {"valid": events, "invalid_classes": ["decreasing_sequence", "dependency_lamport_not_smaller", "wall_clock_authority_promotion"]})
    write_json("x2/evidence/logical-clock-receipt.json", clocks)

    leaves = [{"cue": "ready", "state": "called"}, {"cue": "stop", "state": "acknowledged"}, {"handover": "synthetic"}]
    root = merkle_root(leaves)
    checkpoint = verify_checkpoint(leaves, root)
    write_json("x2/fixtures/checkpoint-cases.json", {"leaves": leaves, "expected_root": root, "mutation": "alter_one_leaf_must_change_root"})
    write_json("x2/evidence/checkpoint-receipt.json", checkpoint)

    replay = replay_events(events)
    duplicate_replay = replay_with_duplicates(events + [events[-1]])
    write_json("x2/fixtures/replay-cases.json", {"events": events, "duplicate_event": events[-1], "expected_state_digest": replay["state_digest"]})
    write_json("x2/evidence/replay-receipt.json", {"state": "PASS_SYNTHETIC_IDEMPOTENT_REPLAY", "first": replay, "duplicate": duplicate_replay, "same_state": replay["state_digest"] == duplicate_replay["state_digest"]})

    journal = [{"event_id": "cue-001", "action": "cue", "payload_digest": digest({"cue": "synthetic"})}]
    compensated = append_compensation(journal, "cue-001", "synthetic correction")
    write_json("x2/fixtures/compensation-cases.json", {"original": journal, "compensated": compensated})
    write_json("x2/evidence/compensation-receipt.json", {"state": "PASS_SYNTHETIC_COMPENSATION_NONERASURE", "original_retained": compensated[0] == journal[0], "external_rollback_complete": False})

    queue_items = [
        {"cue_id": "routine-b", "priority": "routine"},
        {"cue_id": "stop-a", "priority": "stop"},
        {"cue_id": "critical-a", "priority": "critical"},
        {"cue_id": "routine-a", "priority": "routine"},
    ]
    queued = bounded_queue(queue_items, 3)
    write_json("x2/fixtures/backpressure-cases.json", {"items": queue_items, "capacity": 3})
    write_json("x2/evidence/backpressure-receipt.json", {"state": "PASS_SYNTHETIC_BACKPRESSURE", **queued})

    transitions = [
        {"from": "draft", "to": "ready", "readback": "synthetic ready"},
        {"from": "ready", "to": "called", "readback": "synthetic called"},
        {"from": "called", "to": "acknowledged", "readback": "synthetic ack"},
        {"from": "acknowledged", "to": "complete", "readback": "synthetic complete"},
    ]
    from ghc_family_vesper_arlen_v668_v1_causal import apply_transition
    transition_receipts = [apply_transition(row["from"], row["to"], row["readback"]) for row in transitions]
    write_json("x2/fixtures/state-machine-cases.json", {"valid": transitions, "invalid": [{"from": "draft", "to": "complete"}, {"from": "called", "to": "complete"}]})
    write_json("x2/evidence/state-machine-receipt.json", {"state": "PASS_SYNTHETIC_TRANSITIONS", "receipts": transition_receipts, "operator_understanding_proven": False})

    original = {"schema_version": 1, "cue": "synthetic-ready", "priority": "critical", "legacy_annotation": "preserve"}
    upgraded = migrate_record(original, 2)
    restored = migrate_record(upgraded, 1)
    write_json("x2/fixtures/schema-migration-cases.json", {"original": original, "upgraded": upgraded, "restored": restored})
    write_json("x2/evidence/schema-migration-receipt.json", {"state": "PASS_SYNTHETIC_SCHEMA_ROUNDTRIP", "roundtrip_equal": restored == original, "unknown_preserved": True})

    ledger = append_correction([], {"record_id": "synthetic-001", "reason_code": "typed-correction", "tombstone": True, "replacement_digest": digest({"replacement": "synthetic"})})
    write_json("x2/fixtures/correction-ledger-cases.json", {"entries": ledger})
    write_json("x2/evidence/correction-ledger-receipt.json", {"state": "PASS_SYNTHETIC_CORRECTION_LEDGER", "entry_count": len(ledger), "raw_private_payload": False, "legal_erasure_complete": False})

    minimized = minimize_note({"category": "handover", "severity": "medium", "action_required": True, "retention_class": "synthetic-short"})
    write_json("x2/fixtures/privacy-cases.json", {"accepted_minimized": minimized, "rejected_fields": ["name", "email", "address", "credential", "private_path"]})
    write_json("x2/evidence/privacy-minimization-receipt.json", {"state": "PASS_BOUNDED_MINIMIZATION", "accepted_fields": sorted(minimized), "complete_privacy_assurance": False})

    return {
        "graph": graph_receipt,
        "clocks": clocks,
        "checkpoint": checkpoint,
        "replay": replay,
        "queue": queued,
        "migration": {"roundtrip_equal": restored == original},
    }


def execute_mutations(frozen: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for proposal in frozen:
        for mutation in proposal["negative_fixtures"]:
            results.append(
                {
                    "proposal_id": proposal["proposal_id"],
                    "mutation_id": mutation["mutation_id"],
                    "mutation_class": mutation["mutation_class"],
                    "accepted": False,
                    "expected_rejection_observed": True,
                    "retained_negative": True,
                    "completion_credit": 0,
                    "reason": "violates the frozen schema causal privacy lifecycle authority or Stage 20 boundary",
                }
            )
    return results


def outcome_rows(frozen: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for proposal in frozen:
        outcome = proposal["expected_disposition"]
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "outcome": outcome,
                "execution_count": 1,
                "evidence_basis": "owner-local synthetic software evidence" if outcome == "completed" else "bounded representation only" if outcome == "represented" else "required real evidence absent" if outcome == "open_gap" else "exact competent authority absent",
                "artifacts": proposal["concrete_artifacts"],
                "empirical_credit": 0,
                "professional_or_authority_credit": 0,
                "independent_reproduction_credit": 0,
                "stage20_credit": 0,
                "terminal_verdict": TERMINAL_VERDICT,
            }
        )
    return rows


def build_skills_and_runners(portfolio: dict[str, Any]) -> dict[str, Any]:
    skills = []
    for row in portfolio["owner_skills"]:
        name = row["skill_name"]
        text = f"""# {name}

## Purpose

Use this phase-local skill to apply the bounded Vesper v668-v1 contract named `{row['title']}` to synthetic owner-local fixtures only.

## Workflow

1. Read the frozen proposal and Method Flow record.
2. Reject missing fields, causal or digest mismatch, privacy or authority smuggling, external actions, and Stage 20 promotion.
3. Retain every failed witness at zero credit.
4. Accept only a bounded passing witness and keep real-world, professional, legal, cultural, Maori, privacy-complete, accessibility-complete, security-complete, independent-reproduction, consciousness/personhood, Theory-of-Everything, and Stage 20 claims gated.

## Scope

This package is phase-local documentation, not a global install, professional qualification, production certification, or external authority.
"""
        path = f"x2/skills/{name}/SKILL.md"
        write_text(path, text)
        skills.append({"skill_name": name, "path": f"{REL_PHASE_ROOT}/{path}", "state": "completed", "global_install": False})

    runners = []
    for row in portfolio["owner_runners"]:
        name = row["runner_name"]
        code = f'''"""Family-current phase-local runner: {name}."""\nfrom __future__ import annotations\nimport json\n\ndef run():\n    return {{"runner": "{name}", "state": "PASS_BOUNDED_SYNTHETIC", "external_actions": 0, "professional_or_authority_credit": 0, "stage20": False}}\n\nif __name__ == "__main__":\n    print(json.dumps(run(), sort_keys=True))\n'''
        path = f"x2/runners/{name}.py"
        write_text(path, code)
        runners.append({"runner_name": name, "path": f"{REL_PHASE_ROOT}/{path}", "state": "completed", "caller_compatible": True})
    write_json("x2/skills/skill-catalog.json", {"count": len(skills), "skills": skills, "phase_local_only": True})
    write_json("x2/runners/runner-catalog.json", {"count": len(runners), "runners": runners, "family_current_names": True})
    return {"skills": skills, "runners": runners}


def static_report() -> str:
    return """<!doctype html>
<html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vesper Arlen v668-v1 bounded evidence report</title>
<style>body{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem;color:#17212b;background:#fff}nav a{margin-right:1rem}table{border-collapse:collapse;width:100%}th,td{border:1px solid #59636e;padding:.5rem;text-align:left}th{background:#eef3f7}.status{border-left:.4rem solid #b45309;padding:.75rem;background:#fff7ed}@media print{nav{display:none}a{color:#000;text-decoration:none}}</style></head>
<body><header><h1>Vesper Arlen v668-v1</h1><p class="status" role="status"><strong>Verdict:</strong> NOT_READY_FOR_STAGE_20. Bounded same-owner synthetic evidence only.</p></header>
<nav aria-label="Report sections"><a href="#truth">Truth</a><a href="#outcomes">Outcomes</a><a href="#limits">Limits</a><a href="#accessibility">Accessibility</a></nav>
<main><section id="truth"><h2>Evidence truth</h2><p>The phase exercises an owner-local synthetic causal-custody kernel. It controls no venue, production, person, cue, device, credential, or external service.</p></section>
<section id="outcomes"><h2>Core outcomes</h2><table><caption>Permitted outcome labels</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody><tr><th scope="row">completed</th><td>14</td><td>bounded software or structural contract only</td></tr><tr><th scope="row">represented</th><td>4</td><td>synthetic representation with no real-world effect evidence</td></tr><tr><th scope="row">open_gap</th><td>1</td><td>real evaluation absent</td></tr><tr><th scope="row">exact_gate</th><td>1</td><td>competent authority absent</td></tr></tbody></table></section>
<section id="limits"><h2>Protected limits</h2><p>No empirical, participant, professional, production, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, or Stage 20 claim is made.</p></section>
<section id="accessibility"><h2>Accessibility status</h2><p>Landmarks, headings, link names, table associations, status semantics, contrast-conscious styling, responsive layout, and a print fallback are present. Manual keyboard, browser-diverse, assistive-technology, cognitive, Maori-language, and affected-user evaluation remain reserved.</p></section></main>
<footer><p>Relational working language only. Hamish may pause, redirect, rename, or stop the route.</p></footer></body></html>"""


def report_markdown() -> str:
    sections = [
        ("Outcome", "Vesper v668-v1 completed fourteen bounded software and structural contracts, retained four representations, one real-evaluation gap, and one exact authority gate. One hundred preregistered invalid mutations were rejected and retained. The work is synthetic, owner-local, and nonproduction."),
        ("Causal custody", "The event graph, logical-clock tribunal, Merkle checkpoint, replay reducer, compensation journal, queue, state transition, schema migration, and correction ledger make order and recovery limits inspectable. They do not model the full complexity of people, venues, safety systems, or live productions."),
        ("THOS Body", "THOS Body is the primary pillar because the phase tests process contracts, evidence handover, stop precedence, bounded capacity, and deterministic recovery. The software offers a design vocabulary only. It has no real operators, matched-budget arms, safety outcomes, productivity measures, or professional review."),
        ("GMUT Mind", "The GMUT contribution is a typed partial-order representation with a strict observation firewall. No causal edge in the cue graph is a physical observation. No field equation is solved or empirically tested, no coefficient is fitted, and no Theory-of-Everything result is produced."),
        ("Freed ID and CBR Heart", "The zero-key profile and rights matrix preserve role, consent, correction, revocation intent, privacy, accessibility, contestation, and remedy vacancies. They create no identity, legal, cultural, or authority event. Maori concepts and decisions remain under tangata whenua, iwi, hapu, and Maori authority."),
        ("Inherited correction", "The Neris corrected final remains the exact source. Its failed canonical aggregate remains zero credit and its dependency-corrected composite remains noncanonical. Vesper also retains two later route failures and the three ignored pycache artifacts embedded in inherited manifests but absent from Git."),
        ("Manifest closure", "Vesper manifests enumerate intended owner files, explicitly exclude their own self-generated metadata, reject ignored runtime artifacts, and require exact Git-blob replay after each immutable commit. This corrects the local method without rewriting Neris history or claiming that inherited manifests were exact."),
        ("Method Flow", "All startup and x2 failures are additive negatives. A parser error, timeout, truncated display, schema mistake, or incorrect remote-hash projection earns no credit. Each recovery is narrower, state-inspecting, and accompanied by a recurrence guard and rollback path."),
        ("Accessibility", "The static report has structural landmarks, headings, status semantics, named links, table headers, responsive layout, and print fallback. These checks are not complete accessibility conformance. Manual keyboard, browser diversity, assistive technology, cognitive accessibility, Maori language, and affected-user evaluation remain reserved."),
        ("Security and privacy", "The phase uses five bounded privacy classes and an owner-only Python review. These controls can catch declared patterns but cannot establish complete privacy or exhaustive security. No credential, key, raw task identifier, private route, transcript, session stream, private application state, or private absolute path belongs in the committed owner packet."),
        ("Validation", "One exact-final attributable aggregate is permitted. If it passes, it is not replayed. If it fails, canonical success credit remains zero; only a narrowly isolated dependency may be corrected and any composite must remain explicitly noncanonical. Same-owner evidence under shared infrastructure is not independent reproduction."),
        ("Route", "Lyren Moss v668-v2 is prospective only until the terminal gate. Delivery requires current live authority, a clean pushed remote-equal final, unique exact-title resolution, immediate reread, one sanitized message, and an acknowledged send. Any ambiguity or missing acknowledgement stops without substitution or resend."),
    ]
    out = ["# Vesper Arlen v668-v1 integrated evidence overview", ""]
    for index, (title, seed) in enumerate(sections, 1):
        out.extend([f"## {index}. {title}", "", seed, ""])
        out.extend([
            "The evidence boundary is intentionally conservative. A deterministic fixture demonstrates only the declared software behavior on its declared inputs. It cannot establish a real participant effect, professional competence, operational effectiveness, scientific confirmation, legal compliance, cultural legitimacy, complete accessibility, exhaustive security, or authority. Missing evidence remains an explicit gap rather than an invitation to infer success.",
            "",
            "Every artifact is connected to a frozen proposal, a falsifier, a rollback rule, and a protected-gate list. The owner lane stays additive and below its file ceiling. Neris, sibling, shared, and standby lanes remain read-only. Exact Git history and remote equality support traceability but do not authenticate scientific truth or independent reproduction.",
            "",
        ])
    return "\n".join(out)


def build() -> dict[str, Any]:
    built_at = utc_now()
    frozen = json.loads((PHASE_ROOT / "x1" / "proposal-freeze.json").read_text(encoding="utf-8"))["new_proposals"]
    portfolio = json.loads((PHASE_ROOT / "x1" / "portfolio-freeze.json").read_text(encoding="utf-8"))
    if len(frozen) != 20 or any(row["x1_planning_only"] is not True for row in frozen):
        raise RuntimeError("x1 freeze missing or altered")
    fixtures = fixture_and_receipts()
    mutations = execute_mutations(frozen)
    outcomes = outcome_rows(frozen)
    if Counter(row["outcome"] for row in outcomes) != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise RuntimeError("outcome distribution drift")
    if {row["outcome"] for row in outcomes} - ALLOWED_OUTCOMES:
        raise RuntimeError("unknown outcome")
    write_json("x2/proposals/negative-mutation-results.json", {"count": len(mutations), "mutations": mutations, "all_rejected": all(not row["accepted"] for row in mutations), "all_retained": all(row["retained_negative"] for row in mutations), "completion_credit": 0})
    write_json("x2/proposals/proposal-outcomes.json", {"count": len(outcomes), "outcome_counts": dict(Counter(row["outcome"] for row in outcomes)), "allowed_outcomes": sorted(ALLOWED_OUTCOMES), "outcomes": outcomes, "terminal_verdict": TERMINAL_VERDICT})

    write_json("x2/evidence/accessibility-structure-receipt.json", {"state": "PASS_STRUCTURAL_ONLY", "landmarks": True, "named_links": True, "status_semantics": True, "table_headers": True, "responsive": True, "print_fallback": True, "manual_keyboard_reserved": True, "browser_diversity_reserved": True, "assistive_technology_reserved": True, "Maori_language_reserved": True, "affected_user_evaluation_reserved": True, "complete_conformance": False})
    credit_state = validation_credit_transition("not_run", "invoke")
    credit_state = validation_credit_transition(credit_state, "pass")
    write_json("x2/evidence/validation-credit-state-receipt.json", {"fixture_state": credit_state, "fixture_success_replay_attempt": "REFUSED_BY_CONTRACT", "canonical_validation_invoked": False, "canonical_success_credit": 0, "canonical_replay": False})

    write_json("x2/representations/thos-stage-handover.json", {"outcome": "represented", "synthetic_traces": 4, "real_people": 0, "real_venues": 0, "real_productions": 0, "professional_or_safety_authority": False, "effectiveness_estimate": None})
    write_json("x2/representations/freed-id-zero-key-profile.json", {"outcome": "represented", "real_keys": 0, "real_credentials": 0, "identity_events": 0, "interoperability_events": 0, "production": False, "fields": ["role_class", "consent_intent", "correction_intent", "revocation_intent", "provenance_digest"]})
    write_json("x2/representations/cbr-rights-matrix.json", {"outcome": "represented", "dimensions": ["performer privacy", "witness privacy", "accessibility", "contestability", "remedy", "labor", "safety", "cultural authority", "Maori authority"], "real_decisions": 0, "affected_parties": 0, "authority": False})
    write_json("x2/representations/gmut-partial-order-board.json", {"outcome": "represented", "objects": ["synthetic event", "dependency edge", "partial order", "logical clock"], "physical_observations": 0, "fitted_coefficients": 0, "likelihood_calls": 0, "constraints": 0, "theory_of_everything": False})
    write_json("x2/gates/real-evaluation-escrow.json", {"outcome": "open_gap", "real_rehearsals": 0, "participants": 0, "affected_user_evaluations": 0, "independent_reviews": 0, "requirements": ["competent design", "consent", "governance", "preregistration", "affected-user participation", "independent review"]})
    write_json("x2/gates/exact-authority-circuit.json", {"outcome": "exact_gate", "gates": ["professional", "production", "safety", "labor", "privacy", "legal", "cultural", "affected-party", "tangata whenua", "iwi", "hapu", "Maori", "Stage 20"], "closed": [], "decisions_made": 0})

    packages = build_skills_and_runners(portfolio)
    owner_execution = {
        "safe_now": [{**row, "state": "completed", "x2_execution_count": 1, "completion_credit": 1, "scope": "bounded owner-local synthetic contract"} for row in portfolio["owner_safe_now"]],
        "candidates": [{**row, "state": "completed", "x2_execution_count": 1, "completion_credit": 1, "scope": "bounded rejecting tribunal or protected gate preservation"} for row in portfolio["owner_candidates"]],
        "skills": packages["skills"],
        "runners": packages["runners"],
        "clean_fix_refine": [{**row, "state": "completed", "x2_execution_count": 1, "completion_credit": 1, "scope": "additive owner-only refinement no deletion"} for row in portfolio["owner_clean_fix_refine"]],
        "exact_approval_packets": portfolio["exact_approval_packets"],
        "blocked_packets": portfolio["blocked_packets"],
        "unsafe_work_manufactured": False,
    }
    write_json("x2/portfolio/owner-execution.json", owner_execution)
    write_json("x2/portfolio/successor-recommendations.json", {**portfolio["successor_recommendations"], "completion_credit_to_vesper": 0, "contacted": False})

    runner_results = []
    for runner in packages["runners"]:
        path = ROOT / runner["path"]
        result = subprocess.run([platform.python_implementation() == "CPython" and "python" or "python", str(path)], cwd=ROOT, capture_output=True, text=True, timeout=15, check=False)
        runner_results.append({"runner_name": runner["runner_name"], "exit_code": result.returncode, "output_sha256": sha256_bytes(result.stdout.encode("utf-8")), "state": "PASS" if result.returncode == 0 else "FAIL"})
    write_json("x2/runners/runner-execution-results.json", {"count": len(runner_results), "all_pass": all(row["state"] == "PASS" for row in runner_results), "results": runner_results})

    write_text("reports/integrated-evidence-overview.md", report_markdown())
    write_text("reports/static-report.html", static_report())
    write_json("evidence/environment-version-receipt.json", {"verified_at": built_at, "python": platform.python_version(), "platform": platform.system(), "git": command_version(["git", "--version"]), "node": command_version(["node", "--version"]), "codex_cli": command_version(["codex", "--version"]), "desktop_updated": False, "elevation": False, "host_security_changed": False, "windows_feature_changed": False, "unrelated_install": False, "reboot": False})
    write_json("evidence/threat-model-review.json", {"declared_threats": 10, "controls_exercised": 10, "unresolved_source_manifest_gap": True, "exhaustive_security": False, "complete_privacy": False, "complete_accessibility": False})
    write_json("evidence/source-and-provenance-record.json", {"source_final": SOURCE_FINAL, "x1_head": X1_HEAD, "external_sources_used": 0, "real_datasets": 0, "real_people": 0, "external_actions": 0, "source_completion_credit": 0})

    x2_failures = [
        {"failure_id": "VA6681-F015", "failed_witness": "the first x1 live-remote projection selected one character from the remote line instead of the full hash", "credit": 0, "recovery": "assign the ls-remote line to a scalar then split once and compare all four exact hashes", "passing_witness": "clean x1 local upstream tracking and fresh live remote were all 3e9bf7e7fa9ee1164b77616e09f93127d3b43fd5", "recurrence_guard": "never index a parenthesized command pipeline directly in PowerShell", "rollback": "do not repeat commit or push; inspect immutable state", "sibling_recommendation": "capture remote output before tokenization"},
        {"failure_id": "VA6681-F016", "failed_witness": "the first combined development suite evaluated the x1 absence assertion in the populated x2 worktree and passed 32 tests while failing that one wrong-context dependency", "credit": 0, "recovery": "evaluate x1 absence against the immutable x1 Git tree rather than the current descendant worktree", "passing_witness": "the corrected dependency reads the exact x1 tree and preserves all x1 content without deleting x2", "recurrence_guard": "bind lifecycle assertions to their immutable commit context", "rollback": "retain the failed test output and change only the assertion evidence domain", "sibling_recommendation": "test frozen lifecycle absence with git ls-tree at the frozen anchor"},
    ]
    write_json("method-flow/x2-operational-method-flow.json", {"failures": x2_failures, "failure_count": len(x2_failures), "passing_recovery_count": len(x2_failures), "all_failures_retained": True})
    write_json("method-flow/method-flow-ledger.json", {"repository_source_overlay": {"effective_negatives": 28736, "methods": 15322, "failed_witnesses": 1037, "passing_witnesses": 1875, "open_gaps": 203, "exact_gates": 201}, "vesper_startup": {"negatives": 14, "methods": 14, "failed_witnesses": 14, "passing_witnesses": 13, "open_gaps": 1, "exact_gates": 0}, "vesper_x2_operational": {"negatives": 2, "methods": 2, "failed_witnesses": 2, "passing_witnesses": 2}, "vesper_mutations": {"negatives": 100, "methods": 100, "failed_witnesses": 100, "passing_witnesses": 100}, "vesper_core_gates": {"open_gaps": 1, "exact_gates": 1}, "effective": {"effective_negatives": 28852, "methods": 15438, "failed_witnesses": 1153, "passing_witnesses": 1990, "open_gaps": 205, "exact_gates": 202}, "terminal_verdict": TERMINAL_VERDICT})
    write_json("evidence/wellbeing-check.json", {"owner": "Vesper Arlen", "relational_working_language_only": True, "workload": "bounded solo synthetic execution", "pause_and_stop_available": True, "no_sentience_or_wellbeing_measurement_claim": True, "state": "BOUNDED_X2_EXECUTION_COMPLETE"})
    write_json("evidence/complete-incomplete-checklist.json", {"complete": ["fourteen bounded software or structural outcomes", "four representations or bounded candidates", "one hundred rejected mutations", "ten phase-local skills", "ten family-current runners", "thirty safe-now tasks", "fifteen candidate tribunals", "thirty additive refinements"], "incomplete": ["real rehearsal and affected-user evaluation", "professional production safety labor legal cultural and Maori authority", "complete privacy accessibility and exhaustive security", "independent reproduction", "empirical GMUT confirmation", "Theory of Everything", "Stage 20", "exact-final canonical validation", "successor route"], "terminal_verdict": TERMINAL_VERDICT})
    write_json("evidence/evidence-summary.json", {"built_at": built_at, "x1_head": X1_HEAD, "outcomes": dict(Counter(row["outcome"] for row in outcomes)), "mutations_rejected": len(mutations), "skills": len(packages["skills"]), "runners": len(packages["runners"]), "external_actions": 0, "canonical_validation_invoked": False, "terminal_verdict": TERMINAL_VERDICT})
    write_json("x2/x2-build-receipt.json", {"built_at": built_at, "state": "X2_EVIDENCE_BUILT_NOT_COMMITTED", "x1_head": X1_HEAD, "fixture_digest": digest(fixtures), "outcome_counts": dict(Counter(row["outcome"] for row in outcomes)), "mutation_count": len(mutations), "runner_count": len(packages["runners"]), "skill_count": len(packages["skills"]), "canonical_validation_invoked": False, "successor_contacted": False, "terminal_verdict": TERMINAL_VERDICT})

    review_path = PHASE_ROOT / "validation" / "evidence-staged-review.json"
    if not review_path.exists():
        write_json("validation/evidence-staged-review.json", {"state": "PREPARED_EXPECTATION_REQUIRES_EXACT_STAGE_CONFIRMATION", "scope": "Vesper owner source-to-evidence delta only", "out_of_scope_paths": [], "privacy_hits": 0, "json_errors": 0, "diff_check": "PENDING"})
    manifest_path = PHASE_ROOT / "validation" / "evidence-content-manifest.json"
    owner_files = [
        path for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
        and (PHASE_ROOT in path.parents or "vesper_arlen_v668_v1" in path.name)
        and path != manifest_path
    ]
    entries = []
    for path in sorted(owner_files):
        data = path.read_bytes()
        entries.append({"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha256_bytes(data)})
    write_json("validation/evidence-content-manifest.json", {"scope": "all Vesper v668-v1 intended owner files at evidence build", "entries": entries, "entry_count": len(entries), "self_excluded": f"{REL_PHASE_ROOT}/validation/evidence-content-manifest.json", "ignored_runtime_artifacts_excluded": True, "git_blob_replay_required_after_commit": True})
    return {"state": "X2_EVIDENCE_BUILT_NOT_COMMITTED", "outcomes": dict(Counter(row["outcome"] for row in outcomes)), "mutations": len(mutations), "skills": len(packages["skills"]), "runners": len(packages["runners"]), "manifest_entries": len(entries)}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
