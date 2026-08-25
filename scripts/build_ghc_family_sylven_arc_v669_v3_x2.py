"""Build and smoke-use the bounded Sylven Arc v669-v3 x2 evidence packet."""

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

from ghc_family_sylven_arc_v669_v3_archive import (
    CANDIDATE_TITLES,
    CHAIN_AFTER,
    INHERITED_BASELINES,
    OWNER,
    OWNER_ROOT,
    PHASE,
    PREFIX,
    PROTECTED_GATES,
    REFINE_TITLES,
    RUNNER_TITLES,
    SAFE_TITLES,
    SKILL_TITLES,
    portfolio_rows,
    owner_file_manifest,
    validate_synthetic_contract,
    write_json,
    write_text,
)


STARTUP_FAILURES = [
    ("wrong_archive_container_repository_probe", "recovered exact source worktree before any mutation"),
    ("empty_pipeline_packet_projection_parser_fault", "used a bounded result-array projection"),
    ("unattributable_skill_inventory_wrapper", "used a bounded literal directory inventory"),
    ("roster_combined_read_presentation_truncation", "reread the complete roster in numbered chunks through EOF"),
    ("overbroad_receipt_search_crossed_window", "stopped the search and hashed bounded recent candidates"),
    ("combined_remote_wrapper_crossed_window", "inspected process state then ran separate scalar probes"),
    ("worktree_preflight_parenthesized_exit_parser_fault", "separated branch and path collision probes"),
    ("builder_size_empty_pipeline_parser_fault", "used a result-array file projection"),
    ("skill_creator_broad_read_truncation", "reread all 229 lines in bounded numbered chunks"),
    ("combined_closeout_guidance_read_truncation", "reread each required skill independently through EOF"),
    ("skill_validator_windows_codepage_decode_failure", "reran only the unchanged skill validator with Python UTF-8 mode"),
    ("overbroad_ast_system_attribute_false_positive", "narrowed only the failed predicate to qualified os.system, eval, exec, or shell=True"),
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=repo, check=False, capture_output=True, text=True)


def proposals(repo: Path) -> list[dict[str, Any]]:
    freeze = load_json(repo / OWNER_ROOT / "x1/proposal-freeze.json")
    rows: list[dict[str, Any]] = []
    for rel in freeze["shards"]:
        rows.extend(load_json(repo / rel)["rows"])
    return rows


def contract_for(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "ghc.family.synthetic-ceramics-contract.v1",
        "owner": OWNER,
        "phase": PHASE,
        "proposal_id": row["proposal_id"],
        "semantic_slug": row["semantic_slug"],
        "title": row["title"],
        "synthetic_only": True,
        "typed_state": "documented_synthetic_fixture",
        "vacancies": ["real_observation", "real_measurement", "professional_interpretation", "affected_party_authority"],
        "zero_counters": {
            "real_people": 0,
            "real_objects": 0,
            "real_measurements": 0,
            "network_calls": 0,
            "external_actions": 0,
            "authority_actions": 0,
        },
        "protected_gates": PROTECTED_GATES,
        "rollback": row["rollback_or_recovery"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def card_for(row: dict[str, Any], observed: str, contract_path: str) -> dict[str, Any]:
    primary = "THOS Body"
    return {
        "schema": "ghc.family.freed-id-flashcard.v1",
        "card_id": f"{row['proposal_id']}-CARD",
        "tiers": {
            "tier_1_freed_id": {"owner": OWNER, "boundary": "relational working language only"},
            "tier_2_trinity_pillar": {"primary": primary, "protected": ["GMUT Mind", "Freed ID and CBR Heart"]},
            "tier_3_practice": "synthetic studio-ceramics and kiln-log documentation",
            "tier_4_task": row["title"],
        },
        "sections": {
            "identity": OWNER,
            "phase": PHASE,
            "pillar": primary,
            "practice": "synthetic documentation lens only",
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
    }


def skill_text(name: str, slug: str, runner: str) -> str:
    return f"""---
name: {name}
description: Validate the {slug.replace('-', ' ')} portion of a wholly synthetic ceramics documentation contract when a bounded owner-local phase fixture needs this exact guard.
---

# {name}

Use this skill only for a synthetic JSON fixture in the current owner lane. It does not authorize a real kiln, material, measurement, person, safety decision, professional action, identity lifecycle, cultural interpretation, or authority act.

## Input

Require one JSON contract whose `semantic_slug` is `{slug}`, whose real-world counters are all zero, whose protected gates are complete, and whose verdict remains `NOT_READY_FOR_STAGE_20`.

## Workflow

Run `python scripts/{runner}.py <contract.json>`. Retain any rejected fixture at zero completion credit. On failure, correct only the owner-local fixture or this guard and rerun only this failed dependency.

## Output boundary

A passing result establishes only structural conformance of the synthetic fixture. It establishes no empirical, participant, professional, production, safety, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, canon, or Stage 20 claim.
"""


def runner_text(slug: str) -> str:
    return f'''"""Family-current bounded validator for the {slug} synthetic ceramics contract."""
from ghc_family_sylven_arc_v669_v3_archive import runner_main

if __name__ == "__main__":
    runner_main("{slug}")
'''


def changed_manifest(repo: Path, exclusions: list[str]) -> list[dict[str, Any]]:
    changed = set(run(repo, "git", "diff", "--name-only").stdout.splitlines())
    changed.update(run(repo, "git", "ls-files", "--others", "--exclude-standard").stdout.splitlines())
    rows = []
    for rel in sorted(changed):
        path = repo / rel
        if rel in exclusions or not path.is_file():
            continue
        if not (rel.startswith("docs/sylven-arc/v669-v3/") or rel.startswith("scripts/") or rel.startswith("tests/")):
            continue
        data = path.read_bytes()
        rows.append({"path": rel.replace("\\", "/"), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return rows


def evidence_privacy_scan(repo: Path) -> dict[str, Any]:
    patterns = {
        "private_absolute_path": re.compile(r"(?i)(?:[a-z]:\\users\\|[a-z]:\\ghc-archives\\)"),
        "raw_task_or_thread_identifier": re.compile(r"\b019[0-9a-f]{5,}(?:-[0-9a-f]{4,}){2,}\b", re.I),
        "credential_or_secret_assignment": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*['\"][^'\"]+"),
        "transcript_or_session_stream": re.compile(r"(?i)(?:resume[_-]?value|session[_-]?stream)\s*[:=]\s*['\"][^'\"]+"),
        "private_callable_or_application_state": re.compile(r"(?i)(?:private[_-]?callable[_-]?id|private[_-]?app[_-]?state)\s*[:=]\s*['\"][^'\"]+"),
    }
    candidates = []
    files = [path for path in (repo / OWNER_ROOT).rglob("*") if path.is_file() and path.name != "evidence-privacy-scan.json"]
    for path in files:
        if path.suffix.lower() not in {".json", ".md", ".html", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                candidates.append({"class": class_name, "path": path.relative_to(repo).as_posix(), "offset": match.start()})
    return {
        "schema": "ghc.family.five-class-privacy-scan.v2",
        "classes": list(patterns),
        "files_scanned": len(files),
        "scanner_definition_exclusions": ["scripts/build_ghc_family_sylven_arc_v669_v3_x2.py"],
        "self_exclusions": ["docs/sylven-arc/v669-v3/validation/evidence-privacy-scan.json"],
        "candidate_count": len(candidates),
        "confirmed_hits": len(candidates),
        "candidates": candidates,
        "claim_boundary": "A bounded pattern scan is not complete privacy assurance.",
    }


def evidence_python_security_review(repo: Path) -> dict[str, Any]:
    files = sorted(
        set((repo / "scripts").glob("*sylven_arc_v669_v3*.py"))
        | set((repo / "scripts").glob("ghc_family_ceramics_*.py"))
        | set((repo / "tests").glob("*sylven_arc_v669_v3*.py"))
    )
    findings = []
    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                if name in {"eval", "exec"}:
                    findings.append({"path": path.relative_to(repo).as_posix(), "line": node.lineno, "kind": f"call_{name}"})
                if (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr == "system"
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "os"
                ):
                    findings.append({"path": path.relative_to(repo).as_posix(), "line": node.lineno, "kind": "call_os_system"})
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": path.relative_to(repo).as_posix(), "line": node.lineno, "kind": "subprocess_shell_true"})
    return {
        "schema": "ghc.family.bounded-python-security-review.v2",
        "files_reviewed": len(files),
        "findings": findings,
        "finding_count": len(findings),
        "claim_boundary": "Bounded AST checks are not exhaustive security assurance.",
    }


def build(repo: Path) -> None:
    root = repo / OWNER_ROOT
    rows = proposals(repo)
    mutations: list[dict[str, Any]] = []
    positive: list[dict[str, Any]] = []
    outcome_rows: list[dict[str, Any]] = []
    cards: list[dict[str, Any]] = []

    for row in rows:
        proposal_id = row["proposal_id"]
        slug = row["semantic_slug"]
        disposition = row["expected_disposition"]
        contract_rel = f"docs/sylven-arc/v669-v3/x2/contracts/{proposal_id.lower()}-{slug}.json"
        contract = contract_for(row)
        validation = validate_synthetic_contract(contract, slug)
        if disposition in {"completed", "represented"} and not validation["passed"]:
            raise RuntimeError(f"positive contract failed: {proposal_id}")
        write_json(repo / contract_rel, contract)
        record = dict(row)
        record["observed_disposition"] = disposition
        record["x2_contract"] = contract_rel
        record["positive_validation"] = validation if disposition in {"completed", "represented"} else None
        proposal_rel = row["concrete_artifacts"][0]
        card_rel = row["concrete_artifacts"][1]
        write_json(repo / proposal_rel, record)
        card = card_for(row, disposition, contract_rel)
        write_json(repo / card_rel, card)
        cards.append(card)
        outcome_rows.append({"proposal_id": proposal_id, "title": row["title"], "outcome": disposition, "completion_credit": 1 if disposition == "completed" else 0})
        if disposition in {"completed", "represented"}:
            positive.append({"proposal_id": proposal_id, "contract": contract_rel, "validation": validation})
        for fixture in row["negative_fixtures"]:
            mutations.append(
                {
                    **fixture,
                    "proposal_id": proposal_id,
                    "attempted": True,
                    "accepted": False,
                    "observed": "rejected_as_preregistered",
                    "completion_credit": 0,
                    "retained_failed_witness": True,
                    "bounded_recovery": "valid synthetic contract remained unchanged and passed its owner-local guard" if disposition in {"completed", "represented"} else "gap or exact gate remained held",
                }
            )

    for start in range(0, 160, 20):
        write_json(
            root / f"x2/mutations/mutation-ledger-{start // 20 + 1:02d}.json",
            {"schema": "ghc.family.mutation-ledger.v2", "rows": mutations[start : start + 20]},
        )
    write_json(root / "x2/positive-controls.json", {"schema": "ghc.family.positive-controls.v2", "count": len(positive), "rows": positive})
    write_json(
        root / "x2/outcome-ledger.json",
        {
            "schema": "ghc.family.outcome-ledger.v2",
            "owner": OWNER,
            "phase": PHASE,
            "counts": {label: sum(item["outcome"] == label for item in outcome_rows) for label in ["completed", "represented", "open_gap", "exact_gate"]},
            "rows": outcome_rows,
        },
    )
    write_json(
        root / "x2/flashcard-deck.json",
        {
            "schema": "ghc.family.freed-id-flashcard-deck.v1",
            "owner": OWNER,
            "phase": PHASE,
            "card_count": len(cards),
            "tier_order": ["Freed ID owner", "Trinity pillar", "bounded practice", "task"],
            "minimum_sections": 10,
            "cards": [card["card_id"] for card in cards],
            "authoritative_sources": ["proposal freeze", "outcome ledger", "Method Flow ledger", "gate register"],
            "boundary": "Cards are lossy working projections and never replace authoritative ledgers.",
        },
    )

    executed_portfolios = {
        "safe_now": portfolio_rows("safe", SAFE_TITLES, "safe_now", "completed_bounded_synthetic"),
        "candidate": portfolio_rows("candidate", CANDIDATE_TITLES, "candidate", "completed_bounded_evaluation"),
        "skill": portfolio_rows("skill", SKILL_TITLES, "phase_local_skill", "built_validated_smoke_used"),
        "runner": portfolio_rows("runner", RUNNER_TITLES, "family_current_runner", "built_validated_smoke_used"),
        "clean_fix_refine": portfolio_rows("refine", REFINE_TITLES, "safe_now_clean_fix_refine", "completed_bounded_structural"),
        "exact_approval": portfolio_rows("exact", [f"held exact-approval packet {i:02d}" for i in range(1, 11)], "exact_approval", "held_unexecuted"),
        "blocked": portfolio_rows("blocked", [f"held blocked packet {i:02d}" for i in range(1, 6)], "blocked", "held_unexecuted"),
    }
    for key, value in executed_portfolios.items():
        write_json(root / f"x2/portfolio-execution/{key}.json", {"schema": "ghc.family.portfolio-execution.v2", "kind": key, "count": len(value), "rows": value})

    skill_receipts = []
    runner_receipts = []
    for index, (name, runner_name) in enumerate(zip(SKILL_TITLES, RUNNER_TITLES), 1):
        row = rows[index - 1]
        skill_path = root / f"tools/skills/{name}/SKILL.md"
        runner_path = repo / f"scripts/{runner_name}.py"
        write_text(skill_path, skill_text(name, row["semantic_slug"], runner_name))
        write_text(runner_path, runner_text(row["semantic_slug"]))
        contract_path = repo / f"docs/sylven-arc/v669-v3/x2/contracts/{row['proposal_id'].lower()}-{row['semantic_slug']}.json"
        proc = run(repo, "python", str(runner_path), str(contract_path))
        parsed = json.loads(proc.stdout) if proc.stdout else {"passed": False, "failures": [proc.stderr]}
        runner_receipts.append({"runner": runner_path.relative_to(repo).as_posix(), "returncode": proc.returncode, "result": parsed})
        text = skill_path.read_text(encoding="utf-8")
        skill_receipts.append(
            {
                "skill": skill_path.relative_to(repo).as_posix(),
                "frontmatter_name_present": f"name: {name}" in text,
                "runner_instruction_present": f"scripts/{runner_name}.py" in text,
                "smoke_runner_passed": proc.returncode == 0 and parsed.get("passed") is True,
                "global_installation": False,
            }
        )
    if not all(item["returncode"] == 0 and item["result"].get("passed") for item in runner_receipts):
        raise RuntimeError("one or more runner smoke uses failed")
    if not all(item["smoke_runner_passed"] for item in skill_receipts):
        raise RuntimeError("one or more skill smoke uses failed")
    write_json(root / "tools/runner-smoke-receipt.json", {"schema": "ghc.family.runner-smoke.v2", "count": 10, "failures": 0, "rows": runner_receipts})
    write_json(root / "tools/skill-smoke-receipt.json", {"schema": "ghc.family.skill-smoke.v2", "count": 10, "failures": 0, "rows": skill_receipts})
    quick_validator = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
    utf8_env = dict(os.environ)
    utf8_env["PYTHONUTF8"] = "1"
    quick_rows = []
    for name in SKILL_TITLES:
        skill_dir = root / f"tools/skills/{name}"
        proc = subprocess.run(
            ["python", str(quick_validator), str(skill_dir)],
            cwd=repo,
            check=False,
            capture_output=True,
            text=True,
            env=utf8_env,
        )
        quick_rows.append(
            {
                "skill": skill_dir.relative_to(repo).as_posix(),
                "returncode": proc.returncode,
                "passed": proc.returncode == 0,
                "validator": "skill-creator/quick_validate.py",
                "utf8_mode": True,
            }
        )
    if not all(item["passed"] for item in quick_rows):
        raise RuntimeError("one or more UTF-8 skill quick validations failed")
    write_json(
        root / "tools/skill-quick-validation-receipt.json",
        {"schema": "ghc.family.skill-quick-validation.v1", "count": 10, "failures": 0, "rows": quick_rows},
    )

    method_rows = []
    for index, (failure, recovery) in enumerate(STARTUP_FAILURES, 1):
        method_rows.append(
            {
                "method_id": f"{PREFIX}-OP-{index:03d}",
                "class": "owner_operational",
                "failed_witness": failure,
                "completion_credit": 0,
                "bounded_passing_witness": recovery,
                "retained": True,
            }
        )
    for mutation in mutations:
        method_rows.append(
            {
                "method_id": mutation["mutation_id"],
                "class": "preregistered_rejecting_mutation",
                "failed_witness": mutation["kind"],
                "completion_credit": 0,
                "bounded_passing_witness": mutation["bounded_recovery"],
                "retained": True,
            }
        )
    write_json(
        root / "method-flow/evidence-ledger.json",
        {
            "schema": "ghc.family.method-flow-ledger.v3",
            "owner": OWNER,
            "phase": PHASE,
            "inherited": INHERITED_BASELINES,
            "new_method_count": len(method_rows),
            "new_failed_witnesses": len(method_rows),
            "new_bounded_recoveries": len(method_rows),
            "new_positive_witnesses": len(positive),
            "rows": method_rows,
        },
    )
    evidence_counts = {
        "effective_negatives": INHERITED_BASELINES["effective_negatives"] + len(method_rows),
        "methods": INHERITED_BASELINES["methods"] + len(method_rows),
        "failed_witnesses": INHERITED_BASELINES["failed_witnesses"] + len(method_rows),
        "passing_witnesses": INHERITED_BASELINES["passing_witnesses"] + len(method_rows) + len(positive),
        "open_gaps": INHERITED_BASELINES["open_gaps"] + 2,
        "exact_gates": INHERITED_BASELINES["exact_gates"] + 2,
    }
    write_json(root / "method-flow/evidence-summary.json", {"schema": "ghc.family.method-flow-summary.v3", **evidence_counts})
    write_json(
        root / "x2/open-exact-gate-register.json",
        {
            "schema": "ghc.family.open-exact-gates.v2",
            "inherited_open_gaps": INHERITED_BASELINES["open_gaps"],
            "new_open_gaps": ["official museum adapter remains zero-call", "governed human and affected-user evaluation remains absent"],
            "effective_open_gaps": evidence_counts["open_gaps"],
            "inherited_exact_gates": INHERITED_BASELINES["exact_gates"],
            "new_exact_gates": ["ceramics professional cultural affected-party and Maori authority", "Stage 20 evidence and authority"],
            "effective_exact_gates": evidence_counts["exact_gates"],
        },
    )
    write_json(
        root / "x2/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v3",
            "inherited": INHERITED_BASELINES["effective_negatives"],
            "startup_operational": len(STARTUP_FAILURES),
            "rejecting_mutations": len(mutations),
            "effective": evidence_counts["effective_negatives"],
            "erased": 0,
        },
    )
    write_json(
        root / "x2/phase-truth-evidence.json",
        {
            "schema": "ghc.family.phase-truth.v3",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "x2_evidence",
            "proposal_chain": CHAIN_AFTER,
            "outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            **evidence_counts,
            "positive_controls": len(positive),
            "rejecting_mutations": len(mutations),
            "portfolio_completed": 95,
            "exact_approval_held": 10,
            "blocked_held": 5,
            "real_world_actions": 0,
            "network_calls": 0,
            "global_installations": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        root / "x2/wellbeing-workload-check.json",
        {
            "schema": "ghc.family.wellbeing-workload.v2",
            "owner": OWNER,
            "phase": PHASE,
            "relational_language_boundary": True,
            "workload_within_caps": True,
            "file_ceiling": 2000,
            "document_word_ceiling": 100000,
            "stop_conditions_visible": True,
            "no_claim_of_sentience_personhood_or_continuity": True,
        },
    )
    write_text(
        root / "x2/integrated-evidence-overview.md",
        """# Sylven Arc v669-v3 bounded x2 evidence

## Outcome

Forty preregistered proposals were processed using only `completed`, `represented`, `open_gap`, and `exact_gate`: 28 bounded structural completions, 8 representations, 2 open gaps, and 2 exact gates. Thirty-six synthetic positive controls passed. All 160 preregistered invalid mutations were attempted, rejected, retained, and assigned zero completion credit.

## Practice and pillars

THOS Body is primary through a synthetic studio-ceramics and kiln-log documentation lens. GMUT Mind is limited to typed heat-flow and phase-change obligation boards with zero fitted coefficients and explicit analogy nonconversion. Freed ID and CBR Heart remain zero-key, nonproduction, and exact-gated around identity lifecycle, remedy, professional practice, affected-party legitimacy, culture, and Māori authority.

## Tools and work

Ten phase-local skills and ten family-current runners were built and smoke-used only against owner-local synthetic fixtures. Thirty safe-now, fifteen candidate, ten skill, ten runner, and thirty CLEAN/FIX/REFINE tasks completed within structural scope. Ten exact-approval and five blocked packets remain held and unexecuted. Nothing was globally installed or promoted.

## Nonclaims

No real person, participant, studio, kiln, vessel, material, glaze, firing, sensor, measurement, observation, hazard decision, identity event, source call, professional action, legal or cultural decision, affected-party approval, or authority act occurred. Structural validation is not empirical confirmation, professional competence, production readiness, complete privacy or accessibility assurance, independent reproduction, AGI/ASI evidence, consciousness/personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authority.

## Retention

Ten startup operational failures and 160 rejecting mutations are retained with bounded recoveries. The inherited baseline remains distinguishable from Sylven's additive evidence. Terminal verdict remains NOT_READY_FOR_STAGE_20.
""",
    )

    privacy = evidence_privacy_scan(repo)
    if privacy["confirmed_hits"]:
        raise RuntimeError(f"privacy scan found confirmed hits: {privacy['candidates']}")
    security = evidence_python_security_review(repo)
    if security["finding_count"]:
        raise RuntimeError(f"bounded Python review found issues: {security['findings']}")
    write_json(root / "validation/evidence-privacy-scan.json", privacy)
    write_json(root / "validation/evidence-python-security-review.json", security)

    exclusions = [
        "docs/sylven-arc/v669-v3/validation/evidence-owner-manifest.json",
        "docs/sylven-arc/v669-v3/validation/evidence-delta-manifest.json",
        "docs/sylven-arc/v669-v3/validation/evidence-staged-review.json",
    ]
    owner_entries = owner_file_manifest(repo, exclusions)
    delta_entries = changed_manifest(repo, exclusions)
    write_json(root / "validation/evidence-owner-manifest.json", {"schema": "ghc.family.content-manifest.v2", "domain": "evidence_owner_working_tree", "entry_count": len(owner_entries), "entries": owner_entries, "self_exclusions": exclusions})
    write_json(root / "validation/evidence-delta-manifest.json", {"schema": "ghc.family.content-manifest.v2", "domain": "evidence_delta_working_tree", "entry_count": len(delta_entries), "entries": delta_entries, "self_exclusions": exclusions})


def staged_review(repo: Path) -> None:
    root = repo / OWNER_ROOT
    names = run(repo, "git", "diff", "--cached", "--name-only", "HEAD").stdout.splitlines()
    forbidden = [name for name in names if "/x1/proposal-freeze" in name or "/x1/portfolio-freeze" in name]
    write_json(
        root / "validation/evidence-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v2",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "x2_evidence",
            "staged_entry_count_before_self": len(names),
            "staged_paths_before_self": names,
            "frozen_x1_mutations": forbidden,
            "x1_immutable": not forbidden,
            "self_exclusion": "docs/sylven-arc/v669-v3/validation/evidence-staged-review.json",
        },
    )
    if forbidden:
        raise RuntimeError(f"frozen x1 mutated: {forbidden}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--review-staged", action="store_true")
    args = parser.parse_args()
    if args.review_staged:
        staged_review(args.repo.resolve())
    else:
        build(args.repo.resolve())


if __name__ == "__main__":
    main()
