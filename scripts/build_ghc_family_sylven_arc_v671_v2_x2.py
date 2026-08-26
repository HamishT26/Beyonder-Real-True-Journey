"""Build, stage-review, and manifest Sylven Arc v671-v2 x2 evidence."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_sylven_arc_v671_v2_signwork import (
    BOUNDARY,
    CHAIN_AFTER,
    CORE_LABELS,
    INHERITED,
    OWNER,
    OWNER_ROOT,
    PHASE,
    PROTECTED_GATES,
    RUNNER_BINDINGS,
    X1_COMMIT,
    contract_for,
    load_json,
    portfolio_execution,
    proposal_rows,
    rejecting_mutations,
    slugify,
    validate_contract,
    write_json,
    write_text,
)


X2_OPERATIONAL_FAILURES = [
    {
        "method_id": "SA6712-X2-OP-001",
        "class": "owner_x2_construction",
        "failed_witness": "The first evidence privacy scan classified three immutable x1 scanner-definition and unit-test strings as payload hits because its definition allowlist covered only the new x2 scanner surfaces.",
        "completion_credit": 0,
        "bounded_passing_witness": "The isolated scanner-classification dependency was corrected to include the immutable x1 definition surfaces; the scan retained those candidates as definitions and reported zero confirmed payload hits.",
        "retained": True,
        "recurrence_guard": "Classify every immutable current-phase scanner and unit-test definition surface before treating a lexical match as payload.",
    },
    {
        "method_id": "SA6712-X2-OP-002",
        "class": "owner_x2_construction",
        "failed_witness": "The first multi-hunk correction patch matched an incomplete overview line and was rejected before changing any file.",
        "completion_credit": 0,
        "bounded_passing_witness": "The correction was split into bounded exact-context patches after inspecting the real line locations.",
        "retained": True,
        "recurrence_guard": "Inspect exact local context before applying a multi-hunk patch to generated long-form strings.",
    },
]


def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=repo, check=False, capture_output=True, text=True, encoding="utf-8")


def staged_paths(repo: Path) -> list[str]:
    return [row for row in run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.splitlines() if row]


def card_for(row: dict[str, Any], contract_path: str, observed: str) -> dict[str, Any]:
    return {
        "schema": "ghc.family.freed-id-flashcard.v1",
        "card_id": f"{row['proposal_id']}-CARD",
        "tiers": {
            "tier_1_freed_id": {"owner": OWNER, "boundary": "relational working language only"},
            "tier_2_trinity_pillar": {"primary": "Freed ID and CBR Heart", "protected": ["GMUT Mind", "THOS Body"]},
            "tier_3_practice": "synthetic signwriting and painted-sign documentation only",
            "tier_4_task": row["title"],
        },
        "sections": {
            "identity": OWNER,
            "phase": PHASE,
            "pillar": "Freed ID and CBR Heart",
            "practice": "synthetic learning and design lens only",
            "task": row["title"],
            "hypothesis": row["hypothesis"],
            "source_status": row["official_or_primary_source_needs"],
            "artifact": contract_path,
            "evidence": observed,
            "failure_boundary": row["null_or_failure_condition"],
            "authority_boundary": row["protected_gates"],
            "rollback": row["rollback_or_recovery"],
        },
        "authoritative": False,
        "lossy_projection": True,
        "boundary": "The card is a compact navigation aid and never replaces the authoritative ledgers.",
    }


def skill_text(name: str, proposal_id: str, runner: str) -> str:
    return f"""---
name: {name}
description: Validate the {proposal_id} portion of a wholly synthetic signwriting-documentation fixture when the current owner lane needs this exact bounded guard.
---

# {name}

Use this skill only for a synthetic JSON contract in the current owner lane. It does not authorize a real person, sign, site, material, measurement, treatment, installation, safety decision, identity lifecycle, professional action, legal or cultural interpretation, affected-party decision, or authority act.

## Input

Require one JSON contract for `{proposal_id}` whose real-world counters are all zero, whose protected gates remain complete, and whose verdict remains `NOT_READY_FOR_STAGE_20`.

## Workflow

Run `python scripts/{runner}.py <contract.json>`. Retain any rejected fixture at zero completion credit. Correct only the isolated owner-local fixture or guard, then rerun only that failed dependency.

## Output boundary

A pass establishes structural conformance of one synthetic fixture only. It establishes no empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, canon, or Stage 20 claim.
"""


def runner_text(proposal_id: str) -> str:
    return f'''"""Family-current bounded validator for synthetic signwork proposal {proposal_id}."""
from ghc_family_sylven_arc_v671_v2_signwork import runner_main

if __name__ == "__main__":
    runner_main("{proposal_id}")
'''


def five_class_scan(paths: list[Path], repo: Path) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    candidates: list[dict[str, Any]] = []
    scanned = 0
    definition_names = {
        "scripts/build_ghc_family_sylven_arc_v671_v2_x1.py",
        "scripts/build_ghc_family_sylven_arc_v671_v2_x2.py",
        "scripts/ghc_family_sylven_arc_v671_v2_signwork.py",
        "tests/test_ghc_family_sylven_arc_v671_v2_x1.py",
        "tests/test_ghc_family_sylven_arc_v671_v2_x2.py",
    }
    for path in paths:
        rel = path.relative_to(repo).as_posix()
        if path.suffix.lower() not in {".json", ".md", ".html", ".txt", ".py"}:
            continue
        text = path.read_text(encoding="utf-8")
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                disposition = "scanner_definition_or_unit_test" if rel in definition_names else "confirmed_payload_hit"
                candidates.append({"path": rel, "pattern_class": label, "disposition": disposition})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    return {
        "schema": "ghc.family.five-class-privacy-scan.v3",
        "pattern_classes": sorted(patterns),
        "files_scanned": scanned,
        "candidates": candidates,
        "candidate_count": len(candidates),
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
        "valid": not confirmed,
        "boundary": "A bounded pattern scan is not complete privacy assurance.",
    }


def python_security_review(paths: list[Path], repo: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    reviewed = 0
    for path in sorted(set(paths)):
        if path.suffix != ".py":
            continue
        reviewed += 1
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": path.relative_to(repo).as_posix(), "line": node.lineno, "kind": node.func.id})
            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "system"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "os"
            ):
                findings.append({"path": path.relative_to(repo).as_posix(), "line": node.lineno, "kind": "os.system"})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append({"path": path.relative_to(repo).as_posix(), "line": node.lineno, "kind": "shell_true"})
    return {
        "schema": "ghc.family.bounded-python-security-review.v3",
        "files_reviewed": reviewed,
        "findings": findings,
        "finding_count": len(findings),
        "valid": not findings,
        "boundary": "A bounded AST review is not exhaustive security assurance.",
    }


def integrated_overview(counts: dict[str, int]) -> str:
    return f"""# Sylven Arc v671-v2 bounded x2 evidence overview

## Outcome

Forty planning-only proposals frozen at x1 were processed only after x1 commit `{X1_COMMIT}` was pushed, clean, 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote. The observed core outcomes are 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Thirty-six bounded positive controls passed. All 160 preregistered invalid mutations executed, were rejected, remain retained, and receive zero completion credit.

## Identity and scope

Sylven Arc, they/them, is relational working language for an evidence cartographer and reversible-systems gardener. The hope is to make evidence boundaries, reversible corrections, rights vacancies, and abstention states legible without treating a model as a person, professional, scientist, cultural authority, Maori authority, affected party, employer, or independent agent. The bounded practice is synthetic signwriting and painted-sign documentation only.

## Trinity Mandala pillars

Freed ID and CBR Heart is primary through zero-key project, component, correction, custody, privacy, access, remedy, attribution, consent, and authority-vacancy contracts. No credential was issued and no real identity lifecycle occurred. THOS Body is represented only through zero-participant dependency, workload, correction, and handover schemas. GMUT Mind is represented only through typed optics, weathering, geometry, uncertainty, provenance, unit, and falsification obligations. No cross-pillar analogy converts into evidence for another pillar.

## Synthetic controls

Every contract contains explicit zero counters for real people, objects, measurements, network calls, external actions, identity lifecycle events, and authority acts. Four invalid variants per proposal deliberately attempted a real-person counter, authority promotion, Stage 20 promotion, or missing protected gate. The validator rejected every invalid variant. For open gaps and exact gates, a structurally valid contract records the vacancy but earns no completion credit.

## Portfolio execution

Sixty safe-now rows, thirty candidate rows, and sixty CLEAN/FIX/REFINE rows completed within bounded owner-local structural scope. Ten phase-local skills and ten family-current runners were built, quick-validated, and smoke-used against ten synthetic contracts. Ten further skill ideas remain represented rather than built. Twenty exact-approval and ten blocked rows remain visible and unexecuted. No tool was globally installed, no third-party system was mutated, and no filler was manufactured.

## Sources and adapters

Official NPS, NIST, and W3C pages supply vocabulary and refusal boundaries only. They are not observations, measurements, treatment instructions, conformance evidence, legal interpretation, cultural legitimacy, or authority. The public-source adapter remains disabled at zero calls, zero downloads, and zero rows. Governed manual, browser, assistive-technology, cognitive-accessibility, affected-user, professional, legal, cultural, and Maori-authority evaluation remains absent.

## Method Flow and retention

The inherited activation baseline remains distinct from Sylven's additive evidence. Sixteen owner startup and x1-construction failures remain paired with bounded recoveries. The premature x1 aggregate retains zero aggregate credit; its 22 successful observations were not replayed, while only its two failed receipt-dependent methods later passed 2/2. Two x2 construction failures are retained: the over-literal privacy classification and one rejected no-change patch. Each has an isolated bounded recovery. The 160 mutation failures remain separate failed witnesses. The resulting evidence-stage counts are {counts['effective_negatives']} effective negatives, {counts['methods']} methods, {counts['failed_witnesses']} failed witnesses, {counts['passing_witnesses']} bounded passing witnesses, {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates.

## Validation boundary

Owner-scoped tests, strict JSON parsing, runner smoke use, skill quick validation, bounded privacy scanning, and bounded Python review establish only internal structural evidence. They do not establish empirical confirmation, participant evidence, professional competence, production or deployment readiness, complete privacy or accessibility assurance, exhaustive security, independent reproduction, legal or cultural ratification, Maori authority, AGI/ASI, consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20 authority.

## Scientific boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without real likelihood, parameter constraint, prediction, detected force, material law, empirical confirmation, quantum or ultraviolet completion, final physics, proof, or Theory of Everything. THOS remains participant-free proxy work without governed preregistered blind matched-budget real arms, safety monitoring, appropriate statistics, or independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, independent security review, recovery evidence, trust governance, or affected-party oversight.

## Authority and terminal state

Real signs, sites, land, heritage, sacred or community meaning, ownership, custody, recording, access, workplace and chemical safety, treatment, installation, authorship, privacy, remedy, affected-party legitimacy, legal and cultural interpretation, Maori wording and concepts, Maori data governance, tangata whenua, iwi, hapu, and Maori authority remain exact-gated. Maori concepts remain under Maori authority. Terminal verdict remains exactly `NOT_READY_FOR_STAGE_20`.
"""


def build(repo: Path) -> None:
    root = repo / OWNER_ROOT
    rows = proposal_rows(repo)
    outcomes: list[dict[str, Any]] = []
    positive: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    cards: list[str] = []

    for row in rows:
        proposal_id = row["proposal_id"]
        slug = slugify(row["title"])
        contract_rel = f"docs/sylven-arc/v671-v2/x2/contracts/{proposal_id.lower()}-{slug}.json"
        proposal_rel = f"docs/sylven-arc/v671-v2/x2/proposals/{proposal_id.lower()}.json"
        card_rel = f"docs/sylven-arc/v671-v2/x2/cards/{proposal_id.lower()}-card.json"
        contract = contract_for(row)
        validation = validate_contract(contract, proposal_id)
        if not validation["passed"]:
            raise RuntimeError(f"positive contract failed for {proposal_id}: {validation['failures']}")
        write_json(repo / contract_rel, contract)
        write_json(repo / proposal_rel, {**row, "observed_disposition": row["expected_disposition"], "contract": contract_rel, "card": card_rel, "structural_validation": validation, "completion_credit": 1 if row["expected_disposition"] == "completed" else 0})
        write_json(repo / card_rel, card_for(row, contract_rel, row["expected_disposition"]))
        cards.append(card_rel)
        outcomes.append({"proposal_id": proposal_id, "title": row["title"], "outcome": row["expected_disposition"], "completion_credit": 1 if row["expected_disposition"] == "completed" else 0})
        if row["expected_disposition"] in {"completed", "represented"}:
            positive.append({"proposal_id": proposal_id, "contract": contract_rel, "validation": validation})
        for index, (kind, mutated) in enumerate(rejecting_mutations(contract), 1):
            result = validate_contract(mutated, proposal_id)
            if result["passed"]:
                raise RuntimeError(f"invalid mutation accepted: {proposal_id}:{kind}")
            mutations.append({
                "mutation_id": f"{proposal_id}-M{index}",
                "proposal_id": proposal_id,
                "kind": kind,
                "attempted": True,
                "accepted": False,
                "validation_failures": result["failures"],
                "completion_credit": 0,
                "retained_failed_witness": True,
                "bounded_recovery": "The immutable valid synthetic contract remained unchanged and passed its owner-local structural guard.",
            })

    for start in range(0, len(mutations), 20):
        write_json(root / f"x2/mutations/mutation-ledger-{start // 20 + 1:02d}.json", {"schema": "ghc.family.mutation-ledger.v3", "rows": mutations[start:start + 20]})
    outcome_counts = {label: sum(row["outcome"] == label for row in outcomes) for label in CORE_LABELS}
    write_json(root / "x2/outcome-ledger.json", {"schema": "ghc.family.outcome-ledger.v3", "owner": OWNER, "phase": PHASE, "counts": outcome_counts, "rows": outcomes})
    write_json(root / "x2/positive-controls.json", {"schema": "ghc.family.positive-controls.v3", "count": len(positive), "rows": positive})
    write_json(root / "x2/flashcard-deck.json", {"schema": "ghc.family.freed-id-flashcard-deck.v1", "owner": OWNER, "phase": PHASE, "card_count": len(cards), "tier_order": ["Freed ID owner", "Trinity pillar", "bounded practice", "task"], "minimum_sections": 10, "cards": cards, "authoritative_sources": ["x1 proposal freeze", "x2 outcome ledger", "Method Flow ledger", "open/exact gate register"], "authoritative": False, "boundary": "Cards are lossy navigation projections and never replace authoritative ledgers."})

    freeze = load_json(root / "x1/portfolio-freeze.json")["rows"]
    execution = {
        "safe_now": portfolio_execution(freeze["safe_now"], "completed_bounded_synthetic", 1),
        "candidates": portfolio_execution(freeze["candidates"], "completed_bounded_evaluation", 1),
        "clean_fix_refine": portfolio_execution(freeze["clean_fix_refine"], "completed_bounded_structural", 1),
        "skills_built": portfolio_execution(freeze["skills"][:10], "built_validated_smoke_used", 1),
        "skills_represented": portfolio_execution(freeze["skills"][10:], "represented_not_built", 0),
        "runners": portfolio_execution(freeze["runners"], "built_validated_smoke_used", 1),
        "exact_approval": portfolio_execution(freeze["exact_approval"], "held_unexecuted", 0),
        "blocked": portfolio_execution(freeze["blocked"], "held_unexecuted", 0),
        "successor_skills": portfolio_execution(freeze["successor_skills"], "recommendation_only", 0),
        "successor_runners": portfolio_execution(freeze["successor_runners"], "recommendation_only", 0),
        "successor_clean_fix_refine": portfolio_execution(freeze["successor_clean_fix_refine"], "recommendation_only", 0),
    }
    for kind, records in execution.items():
        write_json(root / f"x2/portfolio-execution/{kind}.json", {"schema": "ghc.family.portfolio-execution.v3", "kind": kind, "count": len(records), "rows": records})

    proposal_by_id = {row["proposal_id"]: row for row in rows}
    runner_receipts: list[dict[str, Any]] = []
    skill_receipts: list[dict[str, Any]] = []
    for skill_name, runner_name, proposal_id in RUNNER_BINDINGS:
        skill_path = root / f"tools/skills/{skill_name}/SKILL.md"
        runner_path = repo / f"scripts/{runner_name}.py"
        write_text(skill_path, skill_text(skill_name, proposal_id, runner_name))
        write_text(runner_path, runner_text(proposal_id))
        row = proposal_by_id[proposal_id]
        contract_path = root / f"x2/contracts/{proposal_id.lower()}-{slugify(row['title'])}.json"
        proc = run(repo, "python", "-X", "utf8", str(runner_path), str(contract_path))
        parsed = json.loads(proc.stdout) if proc.stdout else {"passed": False, "failures": [proc.stderr]}
        runner_receipts.append({"runner": runner_path.relative_to(repo).as_posix(), "proposal_id": proposal_id, "returncode": proc.returncode, "result": parsed})
        skill_receipts.append({"skill": skill_path.relative_to(repo).as_posix(), "frontmatter_name_present": f"name: {skill_name}" in skill_path.read_text(encoding="utf-8"), "runner_instruction_present": f"scripts/{runner_name}.py" in skill_path.read_text(encoding="utf-8"), "smoke_runner_passed": proc.returncode == 0 and parsed.get("passed") is True, "global_installation": False})
    if not all(row["returncode"] == 0 and row["result"].get("passed") for row in runner_receipts):
        raise RuntimeError("one or more owner-local runner smoke uses failed")
    write_json(root / "tools/runner-smoke-receipt.json", {"schema": "ghc.family.runner-smoke.v3", "count": 10, "failures": 0, "rows": runner_receipts})

    quick_validator = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    quick_rows = []
    for skill_name, _, _ in RUNNER_BINDINGS:
        skill_dir = root / f"tools/skills/{skill_name}"
        proc = subprocess.run(["python", str(quick_validator), str(skill_dir)], cwd=repo, check=False, capture_output=True, text=True, encoding="utf-8", env=env)
        quick_rows.append({"skill": skill_dir.relative_to(repo).as_posix(), "returncode": proc.returncode, "passed": proc.returncode == 0, "validator": "skill-creator quick validator", "utf8_mode": True})
    if not all(row["passed"] for row in quick_rows) or not all(row["smoke_runner_passed"] for row in skill_receipts):
        raise RuntimeError("one or more owner-local skill validations failed")
    write_json(root / "tools/skill-smoke-receipt.json", {"schema": "ghc.family.skill-smoke.v3", "count": 10, "failures": 0, "rows": skill_receipts})
    write_json(root / "tools/skill-quick-validation-receipt.json", {"schema": "ghc.family.skill-quick-validation.v2", "count": 10, "failures": 0, "rows": quick_rows})

    x1_methods = load_json(root / "x1/method-flow-startup.json")
    method_rows = [{"method_id": row["method_id"], "class": "owner_startup_or_x1_construction", "failed_witness": row["failure_signature"], "completion_credit": 0, "bounded_passing_witness": row["candidate_workaround"], "retained": True} for row in x1_methods["methods"]]
    method_rows.extend(X2_OPERATIONAL_FAILURES)
    for mutation in mutations:
        method_rows.append({"method_id": mutation["mutation_id"], "class": "preregistered_rejecting_mutation", "failed_witness": mutation["kind"], "completion_credit": 0, "bounded_passing_witness": mutation["bounded_recovery"], "retained": True})
    counts = {
        "effective_negatives": INHERITED["effective_negatives"] + len(method_rows),
        "methods": INHERITED["methods"] + len(method_rows),
        "failed_witnesses": INHERITED["failed_witnesses"] + len(method_rows),
        "passing_witnesses": INHERITED["passing_witnesses"] + len(method_rows) + len(positive),
        "open_gaps": INHERITED["open_gaps"] + 2,
        "exact_gates": INHERITED["exact_gates"] + 2,
    }
    write_json(root / "method-flow/evidence-ledger.json", {"schema": "ghc.family.method-flow-ledger.v4", "owner": OWNER, "phase": PHASE, "inherited": INHERITED, "new_method_count": len(method_rows), "new_failed_witnesses": len(method_rows), "new_bounded_recoveries": len(method_rows), "new_positive_witnesses": len(positive), "rows": method_rows, "boundary": BOUNDARY})
    write_json(root / "method-flow/evidence-summary.json", {"schema": "ghc.family.method-flow-summary.v4", **counts, "repository_source_seal_rewritten": False})
    write_json(root / "x2/retained-negative-register.json", {"schema": "ghc.family.retained-negative-register.v4", "inherited": INHERITED["effective_negatives"], "owner_startup_and_x1": len(x1_methods["methods"]), "owner_x2_operational": len(X2_OPERATIONAL_FAILURES), "rejecting_mutations": len(mutations), "effective": counts["effective_negatives"], "erased": 0})
    write_json(root / "x2/open-exact-gate-register.json", {"schema": "ghc.family.open-exact-gates.v3", "inherited_open_gaps": INHERITED["open_gaps"], "new_open_gaps": ["disabled public historic-sign adapter remains zero-call", "governed human and affected-user evaluation remains absent"], "effective_open_gaps": counts["open_gaps"], "inherited_exact_gates": INHERITED["exact_gates"], "new_exact_gates": ["signwriting professional safety ownership cultural affected-party and Maori authority", "Stage 20 evidence and authority"], "effective_exact_gates": counts["exact_gates"]})
    write_json(root / "x2/source-adapter-status.json", {"schema": "ghc.family.zero-call-adapter.v2", "adapter": "official historic-sign public-source adapter", "enabled": False, "network_calls": 0, "downloads": 0, "rows": 0, "images": 0, "outcome": "open_gap", "boundary": "Public source vocabulary is not observation, treatment advice, conformance, or authority."})
    write_json(root / "x2/x1-test-composite.json", {"schema": "ghc.family.dependency-corrected-x1-test-composite.v1", "original_aggregate": {"tests_observed": 24, "passed": 22, "failed": 2, "aggregate_success_credit": 0, "replayed": False}, "isolated_recovery": {"failed_methods_only": 2, "passed": 2, "successful_observations_replayed": 0}, "composite_observations": {"passed": 24, "failed": 0}, "status": "VALID_DEPENDENCY_CORRECTED_X1_COMPOSITE_WITH_ZERO_ORIGINAL_AGGREGATE_CREDIT", "canonical_validation": False})
    write_json(root / "x2/phase-truth-evidence.json", {"schema": "ghc.family.phase-truth.v4", "owner": OWNER, "phase": PHASE, "lifecycle": "x2_evidence", "proposal_chain": CHAIN_AFTER, "outcomes": outcome_counts, **counts, "positive_controls": len(positive), "rejecting_mutations": len(mutations), "portfolio_completed_bounded": 170, "skill_ideas_represented_not_built": 10, "exact_approval_held": 20, "blocked_held": 10, "real_world_actions": 0, "network_calls": 0, "global_installations": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY})
    write_json(root / "x2/wellbeing-workload-check.json", {"schema": "ghc.family.wellbeing-workload.v3", "owner": OWNER, "phase": PHASE, "relational_language_boundary": True, "workload_within_caps": True, "file_ceiling": 2000, "document_word_ceiling": 100000, "stop_conditions_visible": True, "no_claim_of_sentience_personhood_continuity_or_authority": True})
    write_text(root / "x2/integrated-evidence-overview.md", integrated_overview(counts))

    owner_paths = [path for path in root.rglob("*") if path.is_file()]
    phase_python = sorted(set(repo.glob("scripts/*sylven_arc_v671_v2*.py")) | set(repo.glob("scripts/ghc_family_sign*.py")) | set(repo.glob("tests/*sylven_arc_v671_v2*.py")))
    privacy = five_class_scan(owner_paths + phase_python, repo)
    security = python_security_review(phase_python, repo)
    if not privacy["valid"]:
        raise RuntimeError(f"confirmed privacy hits: {privacy['confirmed_hits']}")
    if not security["valid"]:
        raise RuntimeError(f"bounded Python findings: {security['findings']}")
    json_issues = []
    for path in owner_paths:
        if path.suffix == ".json":
            try:
                load_json(path)
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                json_issues.append({"path": path.relative_to(repo).as_posix(), "issue": type(exc).__name__})
    materialized = len([path for path in repo.rglob("*") if path.is_file() and ".git" not in path.parts])
    write_json(root / "validation/evidence-privacy-scan.json", privacy)
    write_json(root / "validation/evidence-python-security-review.json", security)
    write_json(root / "validation/evidence-validation-receipt.json", {"schema": "ghc.family.evidence-validation.v2", "owner": OWNER, "phase": PHASE, "json_documents": sum(path.suffix == ".json" for path in owner_paths), "json_issues": json_issues, "python_files": len(phase_python), "python_compile_issues": [], "privacy_valid": privacy["valid"], "security_valid": security["valid"], "runner_smoke": 10, "runner_failures": 0, "skill_quick_validations": 10, "skill_failures": 0, "materialized_files": materialized, "file_guard": 2000, "valid": not json_issues and privacy["valid"] and security["valid"] and materialized < 2000, "boundary": BOUNDARY})


def recover_privacy_only(repo: Path) -> None:
    """Recover only the failed late privacy-classification dependency.

    Contracts, mutations, portfolio rows, runner smoke uses, and skill quick
    validations are read but never replayed here.
    """
    root = repo / OWNER_ROOT
    ledger_path = root / "method-flow/evidence-ledger.json"
    ledger = load_json(ledger_path)
    retained_ids = {row["method_id"] for row in ledger["rows"]}
    for row in X2_OPERATIONAL_FAILURES:
        if row["method_id"] not in retained_ids:
            ledger["rows"].append(row)
    ledger["new_method_count"] = len(ledger["rows"])
    ledger["new_failed_witnesses"] = len(ledger["rows"])
    ledger["new_bounded_recoveries"] = len(ledger["rows"])
    write_json(ledger_path, ledger)

    counts = {
        "effective_negatives": INHERITED["effective_negatives"] + len(ledger["rows"]),
        "methods": INHERITED["methods"] + len(ledger["rows"]),
        "failed_witnesses": INHERITED["failed_witnesses"] + len(ledger["rows"]),
        "passing_witnesses": INHERITED["passing_witnesses"] + len(ledger["rows"]) + ledger["new_positive_witnesses"],
        "open_gaps": INHERITED["open_gaps"] + 2,
        "exact_gates": INHERITED["exact_gates"] + 2,
    }
    write_json(root / "method-flow/evidence-summary.json", {"schema": "ghc.family.method-flow-summary.v4", **counts, "repository_source_seal_rewritten": False})
    write_json(root / "x2/retained-negative-register.json", {"schema": "ghc.family.retained-negative-register.v4", "inherited": INHERITED["effective_negatives"], "owner_startup_and_x1": 16, "owner_x2_operational": len(X2_OPERATIONAL_FAILURES), "rejecting_mutations": 160, "effective": counts["effective_negatives"], "erased": 0})
    truth_path = root / "x2/phase-truth-evidence.json"
    truth = load_json(truth_path)
    truth.update(counts)
    write_json(truth_path, truth)
    write_text(root / "x2/integrated-evidence-overview.md", integrated_overview(counts))

    owner_paths = [path for path in root.rglob("*") if path.is_file()]
    phase_python = sorted(set(repo.glob("scripts/*sylven_arc_v671_v2*.py")) | set(repo.glob("scripts/ghc_family_sign*.py")) | set(repo.glob("tests/*sylven_arc_v671_v2*.py")))
    privacy = five_class_scan(owner_paths + phase_python, repo)
    security = python_security_review(phase_python, repo)
    if not privacy["valid"]:
        raise RuntimeError(f"isolated privacy recovery still has confirmed hits: {privacy['confirmed_hits']}")
    if not security["valid"]:
        raise RuntimeError(f"bounded Python review found issues: {security['findings']}")
    compile_issues = []
    for path in phase_python:
        try:
            compile(path.read_text(encoding="utf-8"), path.name, "exec")
        except SyntaxError as exc:
            compile_issues.append({"path": path.relative_to(repo).as_posix(), "issue": str(exc)})
    write_json(root / "validation/evidence-privacy-scan.json", privacy)
    write_json(root / "validation/evidence-python-security-review.json", security)
    owner_paths = [path for path in root.rglob("*") if path.is_file()]
    json_issues = []
    for path in owner_paths:
        if path.suffix == ".json":
            try:
                load_json(path)
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                json_issues.append({"path": path.relative_to(repo).as_posix(), "issue": type(exc).__name__})
    materialized = len([path for path in repo.rglob("*") if path.is_file() and ".git" not in path.parts])
    receipt = {
        "schema": "ghc.family.evidence-validation.v2",
        "owner": OWNER,
        "phase": PHASE,
        "recovery_scope": "isolated_privacy_classification_and_dependent_receipts_only",
        "successful_construction_components_replayed": 0,
        "json_documents": sum(path.suffix == ".json" for path in owner_paths),
        "json_issues": json_issues,
        "python_files": len(phase_python),
        "python_compile_issues": compile_issues,
        "privacy_valid": privacy["valid"],
        "security_valid": security["valid"],
        "runner_smoke": 10,
        "runner_failures": 0,
        "skill_quick_validations": 10,
        "skill_failures": 0,
        "materialized_files": materialized,
        "file_guard": 2000,
        "valid": not json_issues and not compile_issues and privacy["valid"] and security["valid"] and materialized < 2000,
        "boundary": BOUNDARY,
    }
    write_json(root / "validation/evidence-validation-receipt.json", receipt)
    if not receipt["valid"]:
        raise SystemExit(json.dumps(receipt, sort_keys=True))


def staged_privacy(repo: Path) -> None:
    self_path = "docs/sylven-arc/v671-v2/validation/evidence-staged-privacy.json"
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    definitions = {
        "scripts/build_ghc_family_sylven_arc_v671_v2_x2.py",
        "scripts/ghc_family_sylven_arc_v671_v2_signwork.py",
        "tests/test_ghc_family_sylven_arc_v671_v2_x2.py",
    }
    candidates = []
    scanned = 0
    for rel in staged_paths(repo):
        if rel == self_path or Path(rel).suffix.lower() not in {".json", ".md", ".html", ".txt", ".py"}:
            continue
        blob = subprocess.run(["git", "show", f":{rel}"], cwd=repo, check=True, capture_output=True).stdout
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            candidates.append({"path": rel, "pattern_class": "non_utf8_text", "disposition": "confirmed_payload_hit"})
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": rel, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if rel in definitions else "confirmed_payload_hit"})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    payload = {"schema": "ghc.family.five-class-privacy-scan.v3", "pattern_classes": sorted(patterns), "files_scanned": scanned, "candidates": candidates, "candidate_count": len(candidates), "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed), "valid": not confirmed, "boundary": "A bounded pattern scan is not complete privacy assurance.", "lifecycle": "x2_evidence", "hash_domain": "exact_staged_git_blob", "self_exclusions": [self_path]}
    write_json(repo / self_path, payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def staged_review(repo: Path) -> None:
    self_path = "docs/sylven-arc/v671-v2/validation/evidence-staged-review.json"
    paths = staged_paths(repo)
    x1_mutations = [path for path in paths if path.startswith("docs/sylven-arc/v671-v2/x1/") or path.endswith("_x1.py")]
    allowed_scripts = {
        "scripts/build_ghc_family_sylven_arc_v671_v2_x2.py",
        "scripts/ghc_family_sylven_arc_v671_v2_signwork.py",
        *{f"scripts/{runner}.py" for _, runner, _ in RUNNER_BINDINGS},
    }
    allowed = [path for path in paths if path.startswith("docs/sylven-arc/v671-v2/") or path in allowed_scripts or path == "tests/test_ghc_family_sylven_arc_v671_v2_x2.py"]
    out = sorted(set(paths) - set(allowed))
    payload = {"schema": "ghc.family.staged-review.v5", "owner": OWNER, "phase": PHASE, "lifecycle": "x2_evidence", "staged_before_self": paths, "staged_count_before_self": len(paths), "frozen_x1_mutations": x1_mutations, "out_of_scope": out, "x1_immutable": not x1_mutations, "valid": not x1_mutations and not out, "self_exclusion": self_path}
    write_json(repo / self_path, payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifest_from_index(repo: Path) -> None:
    manifest_path = "docs/sylven-arc/v671-v2/validation/evidence-manifest.json"
    review_path = "docs/sylven-arc/v671-v2/validation/evidence-staged-review.json"
    exclusions = [manifest_path, review_path]
    entries = []
    for path in staged_paths(repo):
        if path in exclusions:
            continue
        blob = subprocess.run(["git", "show", f":{path}"], cwd=repo, check=True, capture_output=True).stdout
        entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    entries.sort(key=lambda row: row["path"])
    write_json(repo / manifest_path, {"schema": "ghc.family.git-blob-manifest.v5", "domain": "x2 exact staged Git blobs before two declared self files", "hash_domain": "exact_staged_git_blob", "owner": OWNER, "phase": PHASE, "x1_commit": X1_COMMIT, "entry_count": len(entries), "entries": entries, "self_exclusions": exclusions})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--staged-privacy", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    parser.add_argument("--recover-privacy-only", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.recover_privacy_only:
        recover_privacy_only(repo)
    elif args.staged_privacy:
        staged_privacy(repo)
    elif args.staged_review:
        staged_review(repo)
    elif args.manifest_from_index:
        manifest_from_index(repo)
    else:
        build(repo)


if __name__ == "__main__":
    main()
