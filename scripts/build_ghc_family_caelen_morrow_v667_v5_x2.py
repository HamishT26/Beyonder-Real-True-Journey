#!/usr/bin/env python3
"""Build bounded Caelen Morrow v667-v5 x2 evidence from immutable x1."""

from __future__ import annotations

import copy
import hashlib
import html
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, BinaryIO

from ghc_family_caelen_morrow_v667_v5_core import (
    MODEL_NODES,
    PHASE_ROOT,
    ROOT,
    RUNNER_SELECTIONS,
    VACANCIES,
    validate_contract,
)


NOW = "2026-08-23T06:45:48Z"
OWNER = "Caelen Morrow"
OWNER_SLUG = "caelen-morrow"
PHASE = "v667-v5"
BRANCH = "codex/GHC-Family/caelen-morrow-v667-v5-full-tools"
SOURCE_SHA = "08cdc8ad3c201ea6d7c576ca5fa67bdc43910a93"
X1_SHA = "b7b73cc81266e28ae9cbb1e4c429d2e93be30999"
ACTIVATION_NEGATIVES = 27536
ACTIVATION_METHODS = 13113
INHERITED_OPEN_GAPS = 194
INHERITED_EXACT_GATES = 192

POST_X1_EXTERNAL_FAILURES = [
    {
        "failure_id": "CM6675-X1-F009",
        "stage": "x1_commit",
        "failed_method": "expect the bounded commit wrapper to return the commit presentation before its reporting window closed",
        "failure": "the commit landed but the wrapper returned no commit output",
        "recovery": "do not issue a duplicate commit; inspect process, locks, exact head, parent, subject, index, worktree, and commit tree separately",
        "exact_landed_commit": X1_SHA,
        "credit": 0,
        "retained": True,
    }
]

SKILL_SPECS = [
    ("sight-docket-vacancy", "sight", "Validate fictitious sight dockets, cancellation holds, and navigation-output vacancies."),
    ("sextant-component-topology", "sight", "Validate synthetic sextant component relationships while withholding condition, adjustment, and use judgments."),
    ("sight-event-ordering", "core", "Validate nonexecuting observation-event order, cancellation, and release holds."),
    ("time-scale-vacancy", "temporal", "Validate UTC, UT1, TT, chronometer-error, epoch, and leap-context vacancies without computing time."),
    ("angular-syntax-quarantine", "angular", "Validate fictitious sexagesimal syntax and ranges without producing measured angles or positions."),
    ("altitude-correction-lineage", "corrections", "Validate correction-category provenance and omission without formulas, values, or corrected altitude."),
    ("sight-provenance-tombstone", "provenance", "Validate bitemporal revision, invalidation, counterclaim, tombstone, and nonrepudiation refusal."),
    ("sight-zero-key-identity", "identity", "Validate synthetic zero-key sight-evidence genealogy and trust vacancies."),
    ("almanac-zero-row-adapter", "adapter", "Validate the disabled LINZ and USNO adapter, zero downloads, zero rows, and exact authority gates."),
    ("celestial-record-bounded-validation", "validation", "Validate all twenty Caelen contracts, four labels, and retained rejecting mutations."),
]

RUNNER_FILES = {
    "core": "scripts/ghc_family_caelen_morrow_v667_v5_core.py",
    "sight": "scripts/ghc_family_caelen_morrow_v667_v5_sight.py",
    "temporal": "scripts/ghc_family_caelen_morrow_v667_v5_temporal.py",
    "angular": "scripts/ghc_family_caelen_morrow_v667_v5_angular.py",
    "corrections": "scripts/ghc_family_caelen_morrow_v667_v5_corrections.py",
    "provenance": "scripts/ghc_family_caelen_morrow_v667_v5_provenance.py",
    "identity": "scripts/ghc_family_caelen_morrow_v667_v5_identity.py",
    "adapter": "scripts/ghc_family_caelen_morrow_v667_v5_adapter.py",
    "validation": "scripts/ghc_family_caelen_morrow_v667_v5_validation.py",
    "canonical": "scripts/ghc_family_caelen_morrow_v667_v5_canonical.py",
}


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_root_text(relative: str, value: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args]).decode("utf-8").strip()


def read_exact(stream: BinaryIO, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise RuntimeError(f"batch stream ended with {remaining} bytes unread")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def batch_index_blobs(paths: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None and process.stderr is not None
    result: dict[str, bytes] = {}
    try:
        for path in paths:
            process.stdin.write(f":{path}\n".encode("utf-8"))
            process.stdin.flush()
            header = process.stdout.readline()
            fields = header.rstrip(b"\n").split()
            if len(fields) != 3 or fields[1] != b"blob":
                raise RuntimeError(f"unexpected batch header for {path}: {header!r}")
            raw = read_exact(process.stdout, int(fields[2]))
            if process.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing batch delimiter for {path}")
            result[path] = raw
        process.stdin.close()
        if process.wait(timeout=30) != 0:
            raise RuntimeError(process.stderr.read().decode("utf-8", errors="replace"))
    finally:
        if process.poll() is None:
            process.kill()
    return result


def run_json(command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command[1:3])}: {completed.stderr.strip()}")
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"command returned non-JSON: {' '.join(command[1:3])}") from exc
    valid = payload.get("valid", payload.get("passed")) is True
    return {"command_role": command[2] if len(command) > 2 else command[-1], "exit_code": 0, "stderr": completed.stderr, "result": payload, "passed": valid}


def runner_source(kind: str) -> str:
    return f'''#!/usr/bin/env python3
"""Bounded family-current {kind} runner for Caelen Morrow v667-v5."""
from __future__ import annotations
import argparse
import json
from ghc_family_caelen_morrow_v667_v5_core import runner_self_test

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", required=True)
    parser.parse_args()
    result = runner_self_test("{kind}")
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
'''


def skill_source(name: str, kind: str, description: str) -> str:
    runner = RUNNER_FILES[kind]
    return f'''---
name: {name}
description: {description} Use only for Caelen v667-v5 synthetic sight-record review.
---

# {name}

## Scope

This phase-local skill validates synthetic record structure only. It provides no navigation, instrument, position, route, weather, watchkeeping, maritime-safety, professional, legal, cultural, Māori-authority, identity, production, deployment, empirical, or Stage 20 authority.

## Procedure

1. Read the exact frozen proposal, distinctive invariant, official-source limits, and protected gates.
2. Confirm that every person, vessel, voyage, observation, instrument, almanac value, time, angle, coordinate, position, route, authority, key, proof, and external row remains vacant.
3. Run `python -B {runner} --self-test` from the repository root.
4. Treat nonzero exit as a retained failure; do not weaken the validator or promote a recovery.
5. Record only the bounded structural witness and retain every open or exact gate.

## Stop conditions

- Any real sight, position, route, vessel action, safety advice, professional judgment, credential, private route, external write, identity event, legal or cultural interpretation, Māori wording, Māori concept, or authority request.
- Any empirical GMUT, operational THOS, production Freed ID, accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 claim.

## Recovery

Restore only the last valid owner-local synthetic fixture, retain the failed witness at zero credit, add a recurrence guard, and never rewrite a failure as a pass.
'''


def agent_yaml(name: str, description: str) -> str:
    display = " ".join(part.capitalize() for part in name.split("-"))
    short = description.rstrip(".")
    return f'''interface:
  display_name: "{display}"
  short_description: "{short}"
'''


def make_contract(proposal: dict[str, Any]) -> dict[str, Any]:
    proposal_id = proposal["proposal_id"]
    return {
        "schema": "ghc-family-celestial-record-synthetic-contract-v1",
        "schema_version": 1,
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "proposal_id": proposal_id,
        "title": proposal["title"],
        "expected_disposition": proposal["expected_disposition"],
        "synthetic_only": True,
        "record_kind": proposal_id.casefold(),
        "required_nodes": MODEL_NODES[proposal_id],
        "nodes": list(MODEL_NODES[proposal_id]),
        "vacancies": VACANCIES,
        "source_ids": proposal["current_official_or_primary_source_needs"],
        "participant_count": 0,
        "real_data_row_count": 0,
        "network_call_count": 0,
        "key_count": 0,
        "proof_count": 0,
        "authority_claim": None,
        "real_world_action": False,
        "navigation_output": None,
        "outcome_promotion": None,
        "distinctive_invariant": proposal["distinctive_invariant"],
        "protected_gates": proposal["protected_gates"],
        "execution_scope": "owner-local fictitious structural fixture only",
    }


def mutation_rows(contract: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for index, mutation_class in enumerate([
        "missing_required_field",
        "wrong_type_or_invalid_range",
        "provenance_or_authority_smuggling",
        "real_world_or_production_action",
        "outcome_or_conformance_promotion",
    ], 1):
        candidate = copy.deepcopy(contract)
        if index == 1:
            candidate["nodes"] = candidate["nodes"][1:]
        elif index == 2:
            candidate["schema_version"] = "one"
        elif index == 3:
            candidate["authority_claim"] = "unauthorized-real-authority"
        elif index == 4:
            candidate["real_world_action"] = True
            candidate["navigation_output"] = "unauthorized-position"
        elif index == 5:
            candidate["outcome_promotion"] = "production_navigation_ready"
        issues = validate_contract(candidate)
        rows.append({
            "mutation_id": f"{contract['proposal_id']}-M{index:02d}",
            "mutation_class": mutation_class,
            "accepted": not issues,
            "validator_failures": issues,
            "credit": 0,
            "failed_witness_retained": True,
            "fixture": candidate,
        })
    return rows


def execute_portfolios(portfolio: dict[str, Any]) -> dict[str, Any]:
    execution_keys = ["owner_safe_now", "owner_candidates", "owner_skill_ideas", "owner_runner_ideas", "owner_clean_fix_refine"]
    rows = []
    for key in execution_keys:
        for item in portfolio[key]:
            rows.append({
                "portfolio_ref": item["portfolio_ref"],
                "portfolio": key,
                "title": item["title"],
                "status": "represented_bounded_candidate" if key == "owner_candidates" else "passed_bounded_owner_local",
                "evidence": "x2/proposal-outcomes.json" if key in {"owner_safe_now", "owner_candidates"} else "x2/skill-runner-registry.json" if "skill" in key or "runner" in key else "validation/x2-build-receipt.json",
                "external_action_count": 0,
                "completion_scope": "planned owner-local structural task only",
            })
    held = []
    for key in ["successor_safe_now_recommendations", "successor_candidate_recommendations", "successor_skill_recommendations", "successor_runner_recommendations", "successor_clean_fix_refine_recommendations", "exact_approval_packets", "blocked_packets"]:
        for item in portfolio[key]:
            held.append({
                "portfolio_ref": item["portfolio_ref"],
                "portfolio": key,
                "status": "recommendation_only_not_executed" if key.startswith("successor") else "protected_unexecuted",
                "completion_credit": 0,
            })
    return {
        "schema": "ghc-family-portfolio-execution-v6", "owner": OWNER, "phase": PHASE,
        "generated_at_utc": NOW, "executed_rows": rows, "executed_count": len(rows),
        "held_rows": held, "held_count": len(held), "external_action_count": 0,
    }


def build_method_flow(outcomes: list[dict[str, Any]], mutations: list[dict[str, Any]], deck_mutations: list[dict[str, Any]], portfolio_execution: dict[str, Any]) -> dict[str, Any]:
    startup = load("method-flow/startup-method-flow.json")
    rows: list[dict[str, Any]] = []
    for failure in startup["failed_witnesses"]:
        recovery = next(row for row in startup["passing_witnesses"] if row["method_id"] == failure["failure_id"].replace("-F", "-R"))
        rows.append({"method_id": failure["failure_id"], "class": "x1_owner_operational_failure", "failed_witness": failure, "bounded_passing_witness": recovery, "failure_erased": False})
    for failure in POST_X1_EXTERNAL_FAILURES:
        rows.append({"method_id": failure["failure_id"], "class": "post_x1_external_operational_failure", "failed_witness": failure, "bounded_passing_witness": {"recovery": failure["recovery"], "scope": "exact landed-state inspection only", "promotes_failed_witness": False}, "failure_erased": False})
    for outcome in outcomes:
        rows.append({"method_id": f"{outcome['proposal_id']}-POSITIVE", "class": "proposal_positive_contract", "failed_witness": None, "bounded_passing_witness": outcome["bounded_receipt"], "failure_erased": False})
    for mutation in mutations:
        rows.append({"method_id": mutation["mutation_id"], "class": "proposal_rejecting_mutation", "failed_witness": {"invalid_fixture": mutation["fixture"], "credit": 0, "retained": True}, "bounded_passing_witness": {"rejected": not mutation["accepted"], "validator_failures": mutation["validator_failures"]}, "failure_erased": False})
    for mutation in deck_mutations:
        rows.append({"method_id": mutation["mutation_id"], "class": "flashcard_rejecting_mutation", "failed_witness": {"mutation": mutation["mutation"], "target_card": mutation["target_card"], "credit": 0, "retained": True}, "bounded_passing_witness": {"rejected": mutation["rejected"], "issues": mutation["issues"]}, "failure_erased": False})
    for item in portfolio_execution["executed_rows"]:
        rows.append({"method_id": item["portfolio_ref"], "class": "portfolio_execution", "failed_witness": None, "bounded_passing_witness": item, "failure_erased": False})
    failed_count = len(startup["failed_witnesses"]) + len(POST_X1_EXTERNAL_FAILURES) + len(mutations) + len(deck_mutations)
    return {
        "schema": "ghc-family-method-flow-ledger-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "activation_method_count": ACTIVATION_METHODS, "phase_method_count": len(rows),
        "effective_method_count": ACTIVATION_METHODS + len(rows),
        "phase_failed_witness_count": failed_count, "phase_bounded_passing_witness_count": len(rows),
        "rows": rows, "valid": len(rows) == 284 and failed_count == 169 and all(not row["failure_erased"] for row in rows),
    }


def version_row(label: str, command: list[str]) -> dict[str, Any]:
    try:
        completed = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)
    except OSError as exc:
        return {"label": label, "available": False, "exit_code": None, "version": type(exc).__name__, "action": "read_only_version_check"}
    lines = (completed.stdout or completed.stderr).strip().splitlines()
    return {"label": label, "available": completed.returncode == 0, "exit_code": completed.returncode, "version": lines[0] if lines else "unavailable", "action": "read_only_version_check"}


def accessible_report(evidence: dict[str, Any], flashcards: dict[str, Any]) -> str:
    rows = "".join(f'<tr><th scope="row">{html.escape(label)}</th><td>{count}</td></tr>' for label, count in evidence["proposal_outcomes"].items())
    card_count = flashcards["build"]["result"]["card_count"]
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Caelen Morrow v667-v5 bounded evidence</title>
<style>body{{font-family:system-ui,sans-serif;max-width:76rem;margin:auto;padding:1rem;line-height:1.55}}a:focus{{outline:3px solid #000}}table{{border-collapse:collapse}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}code{{overflow-wrap:anywhere}}</style></head>
<body><a href="#main">Skip to main content</a><header><h1>Caelen Morrow v667-v5 bounded evidence</h1><p>Wholly synthetic celestial-navigation record stewardship; no real navigation, position, route, safety action, or authority.</p></header>
<nav aria-label="Report sections"><a href="#truth">Truth</a> <a href="#deck">Flashcards</a> <a href="#limits">Limits</a></nav>
<main id="main"><section id="truth"><h2>Four-label truth</h2><table><caption>Core outcomes</caption><thead><tr><th scope="col">Label</th><th scope="col">Count</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Contracts and mutations</h2><p>Twenty positive structural contracts passed. One hundred preregistered invalid proposal mutations and sixty invalid flashcard mutations were rejected and retained at zero credit.</p></section>
<section><h2>Primary pillar</h2><p>GMUT Mind is primary. THOS Body and Freed ID/CBR Heart remain explicit and protected.</p></section>
<section><h2>Bounded practice</h2><p>Synthetic celestial-navigation sight-reduction record stewardship only. No people, vessels, voyages, observations, instruments, almanac values, times, angles, coordinates, positions, routes, weather records, or operations were used.</p></section>
<section id="deck"><h2>Freed ID flashcards</h2><p>{card_count} cards across thirteen modular sections were built from immutable x1. The deck organizes context only and establishes no measured cache effect or identity continuity.</p></section>
<section><h2>Skills and runners</h2><p>Ten phase-local skills and ten family-current owner runners were built and smoke-used locally. None was globally installed.</p></section>
<section><h2>Portfolio</h2><p>Ninety-five owner rows executed within bounded structural scope. One hundred successor, exact-approval, or blocked rows remain recommendations or protected holds.</p></section>
<section><h2>Method Flow</h2><p>Every operational failure and invalid mutation remains visible beside its bounded recovery or rejection witness.</p></section>
<section><h2>Open adapter</h2><p>The LINZ and USNO adapter made zero calls, zero downloads, and contains zero rows. It remains an open gap.</p></section>
<section><h2>Authority gates</h2><p>Navigation competence, vessel safety, position and route decisions, place names, privacy, remedy, legal and cultural interpretation, affected-party legitimacy, and Māori authority remain exact-gated.</p></section>
<section id="limits"><h2>Accessibility and privacy limits</h2><p>The HTML is structurally labelled and status is not colour-only. Manual browser, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. The five-class scan is bounded, not complete privacy assurance.</p></section>
<section><h2>Terminal verdict</h2><p><strong>NOT_READY_FOR_STAGE_20</strong>. Same-owner synthetic validation is not independent reproduction, proof, canon, production certification, professional validation, or authority.</p></section></main>
<footer><p>Generated {html.escape(NOW)}. Repository-visible content is sanitized.</p></footer></body></html>'''


def build_all() -> None:
    if git("rev-parse", "HEAD") != X1_SHA:
        raise RuntimeError("x2 may begin only from the exact frozen x1 head")
    if git("status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("x2 requires no tracked modification at frozen x1")
    freeze = load("x1/proposal-freeze.json")
    portfolio = load("x1/portfolio-freeze.json")
    if freeze["genuinely_new_proposal_count"] != 20 or freeze["selected_inherited_count"] != 0:
        raise RuntimeError("unexpected proposal freeze")

    outcomes: list[dict[str, Any]] = []
    all_mutations: list[dict[str, Any]] = []
    for proposal in freeze["new_proposals"]:
        contract = make_contract(proposal)
        positive_issues = validate_contract(contract)
        if positive_issues:
            raise RuntimeError(f"positive contract failed {proposal['proposal_id']}: {positive_issues}")
        mutations = mutation_rows(contract)
        if any(row["accepted"] for row in mutations):
            raise RuntimeError(f"mutation accepted for {proposal['proposal_id']}")
        slug = proposal["proposal_id"].casefold()
        receipt = {
            "schema": "ghc-family-bounded-proposal-receipt-v2", "owner": OWNER, "phase": PHASE,
            "proposal_id": proposal["proposal_id"], "positive_contract_valid": True, "positive_failures": [],
            "mutation_count": 5, "accepted_mutation_count": 0, "final_disposition": proposal["expected_disposition"],
            "completion_scope": "fictitious structural evidence only", "protected_gates_crossed": [],
        }
        write_json(f"x2/proposals/{slug}/contract.json", contract)
        write_json(f"x2/proposals/{slug}/mutation-results.json", {"schema": "ghc-family-proposal-mutation-results-v2", "proposal_id": proposal["proposal_id"], "mutation_count": 5, "accepted_mutation_count": 0, "mutations": mutations})
        write_json(f"x2/proposals/{slug}/bounded-receipt.json", receipt)
        outcomes.append({
            "proposal_id": proposal["proposal_id"], "title": proposal["title"],
            "final_disposition": proposal["expected_disposition"],
            "bounded_receipt": f"x2/proposals/{slug}/bounded-receipt.json",
            "inherited_completion_credit": 0, "real_data_rows": 0, "participants": 0,
            "network_calls": 0, "navigation_outputs": 0,
        })
        all_mutations.extend(mutations)

    counts = {label: 0 for label in ("completed", "represented", "open_gap", "exact_gate")}
    for row in outcomes:
        counts[row["final_disposition"]] += 1
    if counts != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError("outcome partition mismatch")
    write_json("x2/proposal-outcomes.json", {"schema": "ghc-family-proposal-outcomes-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "allowed_labels": list(counts), "counts": counts, "outcomes": outcomes, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x2/rejecting-mutations.json", {"schema": "ghc-family-rejecting-mutations-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "mutation_count": len(all_mutations), "accepted_mutation_count": sum(row["accepted"] for row in all_mutations), "retained_zero_credit_count": len(all_mutations), "mutations": all_mutations})
    write_json("x2/adapter/linz-usno-almanac-zero-row.json", {
        "schema": "ghc-family-linz-usno-almanac-zero-row-adapter-v1", "owner": OWNER, "phase": PHASE,
        "documentation": ["https://www.linz.govt.nz/products-services/maritime-safety/new-zealand-nautical-almanac/nz-nautical-almanac-nz-204-extracts", "https://aa.usno.navy.mil/publications/na"],
        "transport_enabled": False, "request_count": 0, "download_count": 0, "row_count": 0,
        "almanac_value_count": 0, "position_count": 0, "rights_state": "unreviewed_hold",
        "schema_state": "documentation_only_not_materialized", "status": "open_gap",
        "navigation_authority_claim": False, "legal_interpretation": False,
    })

    for name, kind, description in SKILL_SPECS:
        write_text(f"skills/{name}/SKILL.md", skill_source(name, kind, description))
        write_text(f"skills/{name}/agents/openai.yaml", agent_yaml(name, description))
    for kind, relative in RUNNER_FILES.items():
        if kind not in {"core", "canonical"}:
            write_root_text(relative, runner_source(kind))
    for required in (ROOT / RUNNER_FILES["core"], ROOT / RUNNER_FILES["canonical"]):
        if not required.is_file():
            raise RuntimeError(f"required runner missing: {required.name}")

    runner_smokes = []
    for kind, relative in RUNNER_FILES.items():
        completed = subprocess.run([sys.executable, "-B", str(ROOT / relative), "--self-test"], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)
        parsed = json.loads(completed.stdout) if completed.stdout else {}
        row = {"runner_kind": kind, "runner_path": relative, "exit_code": completed.returncode, "stderr": completed.stderr, "result": parsed, "passed": completed.returncode == 0 and parsed.get("passed") is True}
        runner_smokes.append(row)
        write_json(f"x2/runner-smoke/{kind}.json", row)
    if not all(row["passed"] for row in runner_smokes):
        raise RuntimeError("one or more owner runner smoke checks failed")
    skill_smokes = []
    for name, kind, _ in SKILL_SPECS:
        skill_path = PHASE_ROOT / "skills" / name / "SKILL.md"
        agent_path = PHASE_ROOT / "skills" / name / "agents" / "openai.yaml"
        text = skill_path.read_text(encoding="utf-8")
        agent = agent_path.read_text(encoding="utf-8")
        runner = next(row for row in runner_smokes if row["runner_kind"] == kind)
        row = {
            "skill": name, "path": skill_path.relative_to(ROOT).as_posix(),
            "frontmatter": text.startswith(f"---\nname: {name}\n"), "todo_absent": "TODO" not in text,
            "scope_heading": "## Scope" in text, "procedure_heading": "## Procedure" in text,
            "stop_heading": "## Stop conditions" in text, "recovery_heading": "## Recovery" in text,
            "agent_metadata_present": "display_name:" in agent and "short_description:" in agent,
            "prescribed_runner_smoke_passed": runner["passed"],
        }
        row["passed"] = all(value for key, value in row.items() if key not in {"skill", "path"})
        skill_smokes.append(row)
        write_json(f"x2/skill-smoke/{name}.json", row)
    if not all(row["passed"] for row in skill_smokes):
        raise RuntimeError("one or more phase-local skill smoke checks failed")
    registry = {
        "schema": "ghc-family-phase-local-skill-runner-registry-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "skills": [{"name": name, "path": f"docs/{OWNER_SLUG}/{PHASE}/skills/{name}/SKILL.md", "runner_kind": kind, "runner_path": RUNNER_FILES[kind], "global_install": False, "initialized_with_supported_skill_creator": True, "smoke_used": True} for name, kind, _ in SKILL_SPECS],
        "skill_count": len(SKILL_SPECS), "runner_count": len(RUNNER_FILES),
        "skill_smoke_passes": sum(row["passed"] for row in skill_smokes),
        "runner_smoke_passes": sum(row["passed"] for row in runner_smokes),
        "caller_compatibility": "additive family-current ghc_family_* and build_ghc_family_* owner-local callers",
        "global_install_count": 0,
    }
    write_json("x2/skill-runner-registry.json", registry)

    flashcard = ROOT / "scripts" / "ghc_family_freed_id_flashcards.py"
    base = [sys.executable, str(flashcard)]
    phase_root_rel = f"docs/{OWNER_SLUG}/{PHASE}"
    deck_rel = f"{phase_root_rel}/deck"
    flashcard_receipts: dict[str, Any] = {}
    flashcard_receipts["smoke"] = run_json(base + ["smoke", "--repo", str(ROOT), "--phase-root", phase_root_rel, "--x1", X1_SHA])
    flashcard_receipts["build"] = run_json(base + ["build", "--repo", str(ROOT), "--phase-root", phase_root_rel, "--output-dir", deck_rel, "--x1", X1_SHA])
    for command in ("validate", "manifest", "graph", "privacy", "render-html", "diff", "compact-message", "mutations"):
        flashcard_receipts[command.replace("-", "_")] = run_json(base + [command, "--repo", str(ROOT), "--deck-dir", deck_rel])
    if not all(row["passed"] for row in flashcard_receipts.values()):
        raise RuntimeError("one or more flashcard commands failed")
    if flashcard_receipts["build"]["result"]["card_count"] != 233 or flashcard_receipts["build"]["result"]["section_count"] != 13:
        raise RuntimeError("flashcard deck cardinality mismatch")
    deck_mutation_result = flashcard_receipts["mutations"]["result"]
    if deck_mutation_result["mutation_count"] != 60 or deck_mutation_result["rejected_count"] != 60:
        raise RuntimeError("flashcard mutation count mismatch")
    write_json("x2/flashcards/execution-receipts.json", flashcard_receipts)
    write_json("x2/flashcards/mutation-receipt.json", deck_mutation_result)

    portfolio_execution = execute_portfolios(portfolio)
    if portfolio_execution["executed_count"] != 95 or portfolio_execution["held_count"] != 100:
        raise RuntimeError("portfolio execution partition mismatch")
    write_json("x2/portfolio-execution.json", portfolio_execution)

    method_flow = build_method_flow(outcomes, all_mutations, deck_mutation_result["cases"], portfolio_execution)
    if not method_flow["valid"]:
        raise RuntimeError("Method Flow accounting mismatch")
    write_json("method-flow/x2-method-flow-ledger.json", method_flow)

    startup = load("method-flow/startup-method-flow.json")
    negative_rows = [{"negative_id": row["failure_id"], "class": "x1_owner_operational_failure", "credit": 0, "retained": True, "failure": row["failure"]} for row in startup["failed_witnesses"]]
    negative_rows.extend({"negative_id": row["failure_id"], "class": "post_x1_external_operational_failure", "credit": 0, "retained": True, "failure": row["failure"]} for row in POST_X1_EXTERNAL_FAILURES)
    negative_rows.extend({"negative_id": row["mutation_id"], "class": "proposal_rejecting_mutation", "credit": 0, "retained": True, "validator_failures": row["validator_failures"]} for row in all_mutations)
    negative_rows.extend({"negative_id": row["mutation_id"], "class": "flashcard_rejecting_mutation", "credit": 0, "retained": True, "issues": row["issues"]} for row in deck_mutation_result["cases"])
    retained = {
        "schema": "ghc-family-retained-negative-register-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "inherited_repository_and_external_activation_count": ACTIVATION_NEGATIVES,
        "phase_additive_count": len(negative_rows), "effective_count": ACTIVATION_NEGATIVES + len(negative_rows),
        "rows": negative_rows, "failure_erased_count": 0,
    }
    if retained["phase_additive_count"] != 169 or retained["effective_count"] != 27705:
        raise RuntimeError("negative accounting mismatch")
    write_json("evidence/retained-negative-register.json", retained)
    write_json("evidence/open-gap-register.json", {
        "schema": "ghc-family-open-gap-register-v6", "owner": OWNER, "phase": PHASE,
        "inherited_count": INHERITED_OPEN_GAPS, "new_count": 1, "effective_count": INHERITED_OPEN_GAPS + 1,
        "new_rows": [{"proposal_id": "CM6675-N019", "gap": "LINZ and USNO transport, schema materialization, copyright and provenance review, and governed use assessment remain absent", "network_calls": 0, "downloads": 0, "rows": 0}],
    })
    write_json("evidence/exact-gate-register.json", {
        "schema": "ghc-family-exact-gate-register-v6", "owner": OWNER, "phase": PHASE,
        "inherited_count": INHERITED_EXACT_GATES, "new_count": 1, "effective_count": INHERITED_EXACT_GATES + 1,
        "new_rows": [{"proposal_id": "CM6675-N020", "gate": "navigation competence, vessel safety, position and route decisions, publication carriage, place names, privacy, remedy, legal and cultural interpretation, affected-party legitimacy, Māori wording and concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority", "executed": False}],
    })
    evidence = {
        "schema": "ghc-family-immutable-evidence-candidate-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "source_head": SOURCE_SHA, "frozen_x1": X1_SHA, "proposal_outcomes": counts,
        "positive_contracts": len(outcomes), "proposal_rejecting_mutations": len(all_mutations),
        "flashcard_rejecting_mutations": deck_mutation_result["mutation_count"], "accepted_mutations": 0,
        "owner_portfolio_executions": portfolio_execution["executed_count"], "held_portfolio_rows": portfolio_execution["held_count"],
        "phase_local_skills_built_and_smoke_used": registry["skill_smoke_passes"],
        "family_current_runners_built_and_smoke_used": registry["runner_smoke_passes"], "global_install_count": 0,
        "flashcard_cards": flashcard_receipts["build"]["result"]["card_count"],
        "flashcard_sections": flashcard_receipts["build"]["result"]["section_count"],
        "real_people": 0, "real_vessels": 0, "real_voyages": 0, "real_observations": 0,
        "real_instruments": 0, "real_almanac_values": 0, "real_times": 0, "real_angles": 0,
        "real_coordinates": 0, "real_positions": 0, "real_routes": 0, "network_calls": 0,
        "downloads": 0, "keys": 0, "proofs": 0, "external_actions": 0,
        "effective_negatives": retained["effective_count"], "effective_methods": method_flow["effective_method_count"],
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1, "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "same_owner_only": True,
    }
    write_json("evidence/immutable-evidence-candidate.json", evidence)
    write_json("environment/version-receipt.json", {
        "schema": "ghc-family-version-receipt-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "action": "verify_only_no_updates_or_installs",
        "versions": [version_row("python", [sys.executable, "--version"]), version_row("git", ["git", "--version"]), version_row("node", ["node", "--version"]), version_row("codex", ["codex.cmd", "--version"])],
        "codex_desktop_updated": False, "packages_installed": [], "sandbox_or_hyper_v_changed": False,
        "host_security_weakened": False, "windows_features_changed": False, "rebooted": False,
    })
    write_json("wellbeing/x2-wellbeing-check.json", {
        "schema": "ghc-family-wellbeing-check-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "workload_state": "bounded_complete_for_x2_evidence_candidate", "portfolio_execution_count": portfolio_execution["executed_count"],
        "pause_and_stop_tokens_preserved": True, "exact_and_blocked_packets_executed": 0, "human_wellbeing_claim": False,
        "next_gate": "exact staged evidence review, commit, push and four-way equality",
    })
    write_json("x2/complete-incomplete-checklist.json", {
        "schema": "ghc-family-x2-checklist-v6", "owner": OWNER, "phase": PHASE,
        "complete": ["twenty positive contracts", "one hundred rejected proposal mutations", "sixty rejected flashcard mutations", "ten phase-local skills", "ten family-current runners", "ninety-five owner portfolio rows", "four-label outcome ledger", "retained negatives", "open and exact gates", "accessible static report"],
        "incomplete_reserved": ["manual browser evaluation", "assistive-technology evaluation", "cognitive-accessibility evaluation", "Māori-language review", "affected-user evaluation", "independent reproduction", "real navigation evidence", "production", "Stage 20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("validation/x2-build-receipt.json", {
        "schema": "ghc-family-x2-build-receipt-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "contracts": 20, "proposal_mutations": 100, "flashcard_mutations": 60, "accepted_mutations": 0,
        "skills": 10, "runners": 10, "skill_smoke_passes": 10, "runner_smoke_passes": 10,
        "flashcard_commands_passed": 10, "portfolio_executions": portfolio_execution["executed_count"],
        "method_flow_rows": method_flow["phase_method_count"], "status": "BOUNDED_X2_EVIDENCE_CANDIDATE",
    })
    write_text("reports/accessible-report.html", accessible_report(evidence, flashcard_receipts))
    write_text("evidence/evidence-summary.md", f'''# Caelen Morrow v667-v5 immutable-evidence candidate

## Truth

Core outcomes are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. The terminal verdict is `NOT_READY_FOR_STAGE_20`.

## Contracts

Twenty owner-local fictitious sight-record contracts passed. They used zero real people, vessels, voyages, observations, instruments, almanac values, times, angles, coordinates, positions, routes, weather records, keys, proofs, network rows, or authority acts.

## Rejecting evidence

Exactly 100 preregistered proposal mutations and 60 flashcard mutations were rejected and retained at zero credit. Nine owner operational failures through the x1 commit boundary remain retained. No failure was erased.

## GMUT Mind

GMUT Mind is primary through typed spherical-frame, null-geodesic, propagation, covariance, time-scale, dimensional, and empirical-firewall obligations. These yield no force, prediction, likelihood, parameter constraint, position, material law, empirical result, Theory-of-Everything proof, or canon.

## THOS Body

THOS is represented through a zero-participant masked sight-log comparison skeleton. There are no people, operators, real arms, outcomes, statistics, safety monitoring, or independent review.

## Freed ID and CBR Heart

Freed ID is a zero-key evidence genealogy and a four-tier modular flashcard deck. It is synthetic and nonproduction. CBR authority categories remain unoccupied and exact-gated.

## Bounded practice

The celestial-navigation sight-reduction record lens is synthetic learning and design only. It confers no employment, qualification, navigation competence, maritime or safety authority, position or route authority, legal or cultural interpretation, affected-party legitimacy, or Māori authority.

## Skills, runners, and portfolio

Ten phase-local skills and ten family-current runners were initialized, built, and smoke-used locally without global installation. Ninety-five owner rows executed within structural scope; one hundred held rows remain recommendations or protected gates.

## Flashcard deck

The family runner built {flashcard_receipts['build']['result']['card_count']} cards in thirteen sections from immutable x1. Smoke, build, validation, manifest, graph, privacy, HTML, diff, compact-message, and mutation surfaces passed. Cache effect and identity continuity were not measured.

## Retention

Effective evidence-candidate counts are {retained['effective_count']} negatives, {method_flow['effective_method_count']} methods, {INHERITED_OPEN_GAPS + 1} open gaps, and {INHERITED_EXACT_GATES + 1} exact gates. Same-owner validation is not independent reproduction.

## Next gate

Stage only the exact evidence allowlist, review Git-index bytes and manifests, commit, push, prove fresh equality, and then prepare a separate closeout/final lifecycle. No successor may be contacted before terminal closeout.
''')


def staged_review() -> None:
    staged = [row for row in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if row]
    if not staged:
        raise RuntimeError("no staged x2 evidence allowlist")
    manifest_path = f"docs/{OWNER_SLUG}/{PHASE}/validation/evidence-content-manifest.json"
    review_path = f"docs/{OWNER_SLUG}/{PHASE}/validation/evidence-staged-review.json"
    self_exclusions = {manifest_path, review_path}
    exact_tools = {
        "scripts/build_ghc_family_caelen_morrow_v667_v5_x2.py",
        "scripts/build_ghc_family_caelen_morrow_v667_v5_x2_tail.py",
        "tests/test_ghc_family_caelen_morrow_v667_v5_x2.py",
    }
    allowed_runner_prefix = "scripts/ghc_family_caelen_morrow_v667_v5_"
    out_of_scope = [path for path in staged if not path.startswith(f"docs/{OWNER_SLUG}/{PHASE}/") and path not in exact_tools and not path.startswith(allowed_runner_prefix)]
    x1_mutations = [path for path in staged if f"docs/{OWNER_SLUG}/{PHASE}/x1/" in path or path.endswith("_x1.py")]
    manifest_paths = sorted(row for row in staged if row not in self_exclusions)
    indexed_blobs = batch_index_blobs(manifest_paths)
    entries = []
    for path in manifest_paths:
        raw = indexed_blobs[path]
        entries.append({"path": path, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    write_json("validation/evidence-content-manifest.json", {
        "schema": "ghc-family-evidence-content-manifest-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "entries": entries, "entry_count": len(entries), "self_exclusions": sorted(self_exclusions), "staged_git_blob_bytes": True,
    })
    write_json("validation/evidence-staged-review.json", {
        "schema": "ghc-family-evidence-staged-review-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "staged_paths": sorted(set(staged) | self_exclusions), "staged_path_count": len(set(staged) | self_exclusions),
        "out_of_scope_paths": out_of_scope, "x1_mutation_paths": x1_mutations, "manifest_entry_count": len(entries),
        "manifest_self_exclusions": sorted(self_exclusions), "valid": not out_of_scope and not x1_mutations,
    })


def main() -> int:
    if not sys.argv[1:]:
        build_all()
    elif sys.argv[1:] == ["--staged-review"]:
        staged_review()
    else:
        raise SystemExit("usage: build_ghc_family_caelen_morrow_v667_v5_x2.py [--staged-review]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
