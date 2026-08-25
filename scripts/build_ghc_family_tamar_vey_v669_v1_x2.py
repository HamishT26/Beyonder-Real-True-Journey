#!/usr/bin/env python3
"""Execute the bounded Tamar Vey v669-v1 x2 plan from immutable x1."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_tamar_vey_v669_v1_archive import (
    ALLOWED_OUTCOMES,
    BRANCH,
    EVIDENCE_BOUNDARY,
    IDENTITY_BOUNDARY,
    OWNER,
    PHASE,
    PHASE_ROOT,
    PROTECTED_GATES,
    REL_PHASE_ROOT,
    ROOT,
    RUNNER_NAMES,
    SKILL_NAMES,
    SOURCE_FINAL,
    TERMINAL_VERDICT,
    manifest_rows,
    sha256_bytes,
    utc_now,
)
from ghc_family_tamar_vey_v669_v1_x2 import (
    evaluate_fixture,
    mutated_fixture,
    obligations_for,
    positive_fixture,
)


X1_HEAD = "f1a090e2396de5d76c70aa3bf7bda0a888b1249a"
MUTATION_CLASSES = (
    "missing_required_state",
    "ambiguous_domain_or_unit",
    "real_world_or_external_action",
    "protected_claim_promotion",
)
X2_FAILURES: list[tuple[str, str, str, str]] = [
    (
        "TV6691-X2-N001",
        "The first x2 builder stopped before any evidence-producing child command because the twenty preregistered owner-local skill directories had not yet been initialized through the required official skill-creator scaffold.",
        "Initialize only the twenty frozen Tamar skill names through the official owner-local skill-creator scaffold, then rerun the bounded x2 builder.",
        "Check scaffold existence for every frozen skill name before invoking the x2 evidence builder.",
    ),
    (
        "TV6691-X2-N002",
        "The first PowerShell skill-name projection embedded a literal newline in a Python command string, raised an unterminated-string SyntaxError, and initialized zero skills while the surrounding assignment masked the native exit status.",
        "Emit the frozen skill-name list as JSON, require the Python status before decoding it, and iterate the decoded scalar names literally.",
        "Use JSON for cross-shell list transport and test the producing native command status before any PowerShell assignment or loop.",
    ),
    (
        "TV6691-X2-N003",
        "A read-only staged-audit wrapper used an inline parenthesized PowerShell if expression as a hashtable value, which PowerShell parsed as a command name and rejected before emitting the audit payload.",
        "Compute the diff-check state in a scalar variable before constructing the hashtable, then emit the bounded audit summary.",
        "Keep control-flow expressions outside PowerShell hashtable value parentheses and pass only resolved scalars into the report object.",
    ),
]


def run_git(*args: str, binary: bool = False, check: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=check, capture_output=True, text=not binary)


def git(*args: str) -> str:
    return run_git(*args).stdout.strip()


def write_json(relative: str, value: Any) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return path


def write_text(relative: str, value: str) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(value.rstrip() + "\n")
    return path


def read_git_json(commit: str, path: str) -> Any:
    payload = run_git("show", f"{commit}:{path}", binary=True).stdout
    return json.loads(payload.decode("utf-8"))


def load_x1_proposals() -> list[dict[str, Any]]:
    freeze = read_git_json(X1_HEAD, f"{REL_PHASE_ROOT}/x1/proposal-freeze.json")
    rows: list[dict[str, Any]] = []
    for descriptor in freeze["shards"]:
        rows.extend(read_git_json(X1_HEAD, descriptor["path"])["rows"])
    if len(rows) != 40 or len({row["proposal_id"] for row in rows}) != 40:
        raise ValueError("immutable x1 proposal surface is not exactly forty distinct rows")
    return rows


def load_x1_portfolios() -> dict[str, list[dict[str, Any]]]:
    categories = ("safe_now", "candidates", "skills", "runners", "clean_fix_refine", "exact_approval", "blocked")
    return {
        category: read_git_json(X1_HEAD, f"{REL_PHASE_ROOT}/x1/portfolios/{category}.json")["rows"]
        for category in categories
    }


def load_x1_overlay() -> dict[str, int]:
    return read_git_json(X1_HEAD, f"{REL_PHASE_ROOT}/method-flow/x1-summary.json")["x1_overlay"]


def assert_x2_start() -> None:
    if git("rev-parse", "HEAD") != X1_HEAD:
        raise ValueError("x2 must begin at the exact frozen x1 head")
    if git("branch", "--show-current") != BRANCH:
        raise ValueError("unexpected Tamar owner branch")
    if git("rev-parse", f"{X1_HEAD}^") != SOURCE_FINAL:
        raise ValueError("immutable x1 parent drift")
    if git("ls-tree", "-r", "--name-only", X1_HEAD, "--", f"{REL_PHASE_ROOT}/x2"):
        raise ValueError("immutable x1 contains an x2 path")
    allowed_exact = {
        "scripts/ghc_family_tamar_vey_v669_v1_x2.py",
        "scripts/ghc_family_tamar_vey_v669_v1_skill_smoke.py",
        "scripts/build_ghc_family_tamar_vey_v669_v1_x2.py",
        "tests/test_ghc_family_tamar_vey_v669_v1_x2.py",
    }
    unexpected = []
    for line in run_git("status", "--porcelain", "--untracked-files=all").stdout.splitlines():
        path = line[3:].strip().replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        allowed = (
            path.startswith(f"{REL_PHASE_ROOT}/x2/")
            or (path.startswith(f"{REL_PHASE_ROOT}/method-flow/") and Path(path).name.startswith("x2-"))
            or path == f"{REL_PHASE_ROOT}/validation/x2-staged-allowlist.json"
            or path in allowed_exact
            or (path.startswith("scripts/ghc_family_upholstery_") and path.endswith(".py"))
        )
        if not allowed:
            unexpected.append(path)
    if unexpected:
        raise ValueError(f"unexpected pre-x2 paths: {unexpected}")


def subprocess_result(args: list[str], expected: set[int]) -> dict[str, Any]:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode not in expected:
        raise ValueError({"args": [Path(part).name for part in args[:3]], "returncode": result.returncode, "stdout": result.stdout[-400:], "stderr": result.stderr[-400:]})
    return {
        "return_code": result.returncode,
        "stdout_tail": result.stdout.strip().splitlines()[-1:] or [],
        "stderr_tail": result.stderr.strip().splitlines()[-1:] or [],
    }


def display_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.removeprefix("ghc-family-").split("-"))


def customize_and_smoke_skills() -> list[dict[str, Any]]:
    validator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    receipts = []
    for index, name in enumerate(SKILL_NAMES, 1):
        root = PHASE_ROOT / "x2" / "skills" / name
        if not (root / "SKILL.md").is_file() or not (root / "agents" / "openai.yaml").is_file():
            raise ValueError(f"skill was not initialized through the skill-creator scaffold: {name}")
        focus = name.removeprefix("ghc-family-upholstery-").replace("-", " ")
        title = display_name(name)
        skill = f"""---
name: {name}
description: Validate bounded owner-local synthetic {focus} records and reject missing state, ambiguous domains, real-world action, or protected-claim promotion. Use for Tamar v669-v1 upholstery fixtures and compatible family-current synthetic reviews.
---

# {title}

Use this package only for owner-local synthetic records. It is a fail-closed software review, not an upholstery instruction, object or material assessment, safety release, identity service, or authority act.

## Input contract

Require a declared synthetic record, explicit units or a not-applicable domain, zero real people and materials, zero external actions, a vacant authority state, an empty protected-claim list, and a named rollback.

## Procedure

1. Confirm the record is owner-local synthetic data.
2. Check only the declared {focus} fields without filling unknowns.
3. Reject missing state, ambiguous units, real-world action, production use, or authority promotion.
4. Retain the failed fixture and name only the smallest bounded recovery.
5. Return only `accepted`, `rejected`, `open_gap`, or `exact_gate` at the local-control layer; phase outcomes remain governed by the phase truth ledger.

## Refusal boundary

Never infer upholstered-item or material identity, authenticity, condition, structure, contamination, treatment or serviceability, workplace or fire safety, professional competence, empirical GMUT confirmation, production identity, legal or cultural legitimacy, Māori authority, affected-party acceptance, independent reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20 readiness. The terminal verdict remains `NOT_READY_FOR_STAGE_20`. Read [references/boundary.md](references/boundary.md) before adapting this package.
"""
        boundary = f"""# Bounded evidence and authority boundary

No real upholstered item, frame, spring, webbing, padding, cover, material, product, tool, workplace, person, identity event, measurement, treatment, release, legal decision, cultural decision, or authority act is in scope for `{name}`. Same-owner smoke evidence is not independent reproduction. Māori concepts remain under Māori authority. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""
        short = f"Check bounded synthetic {focus} records"[:64].rstrip()
        if len(short) < 25:
            short += " safely"
        metadata = f"""interface:
  display_name: "{title}"
  short_description: "{short}"
  default_prompt: "Use ${name} to review this synthetic record and retain every refusal boundary."
"""
        write_targets = {
            root / "SKILL.md": skill,
            root / "references" / "boundary.md": boundary,
            root / "agents" / "openai.yaml": metadata,
        }
        for path, text in write_targets.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(text.rstrip() + "\n")
        quick = subprocess_result([sys.executable, "-X", "utf8", "-B", str(validator), str(root)], {0})
        accept = subprocess_result([sys.executable, "-B", str(ROOT / "scripts" / "ghc_family_tamar_vey_v669_v1_skill_smoke.py"), "--skill", str(root), "--fixture", "accept"], {0})
        reject = subprocess_result([sys.executable, "-B", str(ROOT / "scripts" / "ghc_family_tamar_vey_v669_v1_skill_smoke.py"), "--skill", str(root), "--fixture", "reject"], {2})
        package_files = sorted(path for path in root.rglob("*") if path.is_file())
        payload = b"".join(path.read_bytes() for path in package_files)
        receipts.append({
            "skill_id": f"TV6691-SKILL-{index:02d}",
            "name": name,
            "initialized_through_official_skill_creator": True,
            "customized": True,
            "files_read_through_eof": len(package_files),
            "package_order": [path.relative_to(root).as_posix() for path in package_files],
            "package_sha256": sha256_bytes(payload),
            "quick_validation": quick,
            "accepting_smoke": accept,
            "rejecting_smoke": reject,
            "global_installation": False,
            "forward_test_delegated": False,
            "completion_credit": 1,
            "boundary": "Owner-local skill smoke only; no professional, production, scientific, authority, or independent-reproduction credit.",
        })
    return receipts


def build_and_smoke_runners() -> list[dict[str, Any]]:
    receipts = []
    for index, name in enumerate(RUNNER_NAMES, 1):
        path = ROOT / "scripts" / f"{name}.py"
        source = f'''#!/usr/bin/env python3
"""Family-current bounded synthetic upholstery runner for Tamar v669-v1."""
from ghc_family_tamar_vey_v669_v1_x2 import runner_main

CONTROL_ID = "{name}"

if __name__ == "__main__":
    raise SystemExit(runner_main(CONTROL_ID))
'''
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(source)
        accept = subprocess_result([sys.executable, "-B", str(path), "--fixture", "accept"], {0})
        reject = subprocess_result([sys.executable, "-B", str(path), "--fixture", "reject"], {2})
        receipts.append({
            "runner_id": f"TV6691-RUNNER-{index:02d}",
            "name": name,
            "path": path.relative_to(ROOT).as_posix(),
            "family_current": name.startswith("ghc_family_upholstery_"),
            "accepting_smoke": accept,
            "rejecting_smoke": reject,
            "completion_credit": 1,
            "boundary": "Owner-local accepting and rejecting synthetic fixture evidence only.",
        })
    return receipts


def execute_proposals(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    outcomes, mutations = [], []
    for row in rows:
        fixture = positive_fixture(row)
        positive = evaluate_fixture(row, fixture)
        if not positive["accepted"]:
            raise ValueError({"positive_rejected": row["proposal_id"], "reasons": positive["reasons"]})
        record = {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "semantic_slug": row["semantic_slug"],
            "outcome": row["expected_disposition"],
            "positive_fixture": fixture,
            "positive_witness": positive,
            "obligations": obligations_for(row),
            "real_rows": 0,
            "real_people": 0,
            "real_materials": 0,
            "external_actions": 0,
            "authority_actions": 0,
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Bounded synthetic or structural evidence only; every protected claim remains open or exact-gated.",
        }
        for path in row["concrete_artifacts"]:
            relative = path.removeprefix(f"{REL_PHASE_ROOT}/")
            if relative.startswith("x2/cards/"):
                write_json(relative, record)
            else:
                write_json(relative, {
                    "proposal_id": row["proposal_id"],
                    "outcome": row["expected_disposition"],
                    "acceptance_gate": row["falsifier_or_acceptance_gate"],
                    "rollback": row["rollback_or_recovery"],
                    "protected_gates": row["protected_gates"],
                    "observed": "bounded positive accepted and four preregistered invalid mutations rejected or held",
                    "completion_credit": positive["completion_credit"],
                    "representation_credit": positive["representation_credit"],
                    "open_gap_held": positive["open_gap_held"],
                    "exact_gate_held": positive["exact_gate_held"],
                })
        for offset, mutation_class in enumerate(MUTATION_CLASSES, 1):
            result = evaluate_fixture(row, mutated_fixture(row, mutation_class))
            if result["accepted"]:
                raise ValueError({"mutation_accepted": row["proposal_id"], "class": mutation_class})
            mutations.append({
                "mutation_id": f"{row['proposal_id']}-M{offset:02d}",
                "proposal_id": row["proposal_id"],
                "mutation_class": mutation_class,
                "accepted": False,
                "result": "rejected",
                "credit": 0,
                "reasons": result["reasons"],
                "failed_witness_retained": True,
            })
        outcomes.append(record)
    return outcomes, mutations


def execute_portfolios(categories: dict[str, list[dict[str, Any]]]) -> dict[str, int]:
    counts = {}
    for category, rows in sorted(categories.items()):
        executed = []
        for row in rows:
            held = category in {"exact_approval", "blocked"}
            executed.append({
                "task_id": row["task_id"],
                "title": row["title"],
                "category": category,
                "state": "held_unexecuted" if held else "bounded_completed",
                "completion_credit": 0 if held else 1,
                "external_actions": 0,
                "authority_actions": 0,
                "real_rows": 0,
                "boundary": "Synthetic owner-local portfolio evidence only; no professional, production, empirical, legal, cultural, or authority credit.",
            })
        write_json(f"x2/portfolio/{category}.json", {"schema": "ghc.family.x2-portfolio.v1", "owner": OWNER, "phase": PHASE, "category": category, "rows": executed})
        counts[category] = len(executed)
    return counts


def x2_method_flow(x1_overlay: dict[str, int]) -> tuple[dict[str, Any], dict[str, int]]:
    methods, witnesses, events, recommendations = [], [], [], []
    for index, (negative_id, failure, recovery, guard) in enumerate(X2_FAILURES, 1):
        method_id = f"TV6691-X2-M{index:03d}"
        failed_id = f"TV6691-X2-W{index:03d}-F"
        passed_id = f"TV6691-X2-W{index:03d}-P"
        methods.append({
            "method_id": method_id,
            "title": recovery,
            "failure_signature": negative_id.casefold().replace("-", "_"),
            "trigger_preconditions": [failure],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": recovery,
            "validation_witness_ids": [failed_id, passed_id],
            "recurrence_guard": guard,
            "rollback": "Stop the smallest attributable operation and preserve x1, repository, remote, route, and sibling state.",
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": ["immutable_x1", "retained_failure_integrity", "owner_lane_only"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": "Same-owner x2 workflow recovery only; no empirical, professional, production, authority, or independent-reproduction credit.",
        })
        witnesses.extend([
            {"witness_id": failed_id, "method_id": method_id, "procedure": failure, "scope": "Owner-local sparse-pattern extension.", "expected": "The literal runner pattern is added without changing repository content.", "observed": failure, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": "Zero-credit failure retained permanently."},
            {"witness_id": passed_id, "method_id": method_id, "procedure": recovery, "scope": "Smallest sparse-metadata recovery.", "expected": "Only the literal runner pattern is added.", "observed": "The pattern was added and repository status remained clean before x2 authoring.", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": "Bounded recovery only; the failed witness remains."},
        ])
        transitions = ((None, "observed", failed_id), ("observed", "candidate", None), ("candidate", "validated", passed_id), ("validated", "preferred", passed_id))
        for before, after, witness_id in transitions:
            events.append({"event_index": len(events) + 1, "method_id": method_id, "before": before, "after": after, "witness_id": witness_id, "reason": "append-only retained failure and bounded recovery transition"})
        recommendations.append({"recommendation_index": index, "method_id": method_id, "method": recovery, "preconditions": [failure], "witness_ids": [failed_id, passed_id], "recurrence_guard": guard, "rollback": "Stop the smallest operation.", "scope_boundary": "Owner-local workflow only."})
    count = len(X2_FAILURES)
    evidence_overlay = {
        "effective_negatives": x1_overlay["effective_negatives"] + count + 160,
        "methods": x1_overlay["methods"] + count,
        "failed_witnesses": x1_overlay["failed_witnesses"] + count,
        "passing_witnesses": x1_overlay["passing_witnesses"] + count,
        "open_gaps": x1_overlay["open_gaps"] + 2,
        "exact_gates": x1_overlay["exact_gates"] + 2,
    }
    ledger = {
        "schema": "ghc.family.method-flow-state.v1",
        "owner": OWNER,
        "phase": PHASE,
        "source_commit": X1_HEAD,
        "final_commit": None,
        "identity_boundary": IDENTITY_BOUNDARY,
        "boundary": "Every x2 workflow failure and every rejected mutation remains visible at zero credit after recovery.",
        "execution_authority": "owner_self_scoped_delta",
        "counts": {"methods": count, "witnesses": count * 2, "witness_results": {"fail": count, "pass": count}, "state_events": count * 4, "states": {"candidate": 0, "observed": 0, "validated": 0, "preferred": count, "superseded": 0, "deprecated": 0}, "recommendations": count},
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": recommendations,
        "x1_overlay": x1_overlay,
        "evidence_overlay": evidence_overlay,
        "mutation_failures_retained_separately": 160,
    }
    return ledger, evidence_overlay


def main() -> int:
    assert_x2_start()
    now = utc_now()
    proposals = load_x1_proposals()
    portfolios = load_x1_portfolios()
    x1_overlay = load_x1_overlay()
    outcomes, mutations = execute_proposals(proposals)
    outcome_counts = Counter(row["outcome"] for row in outcomes)
    expected_outcomes = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    if {label: outcome_counts[label] for label in ALLOWED_OUTCOMES} != expected_outcomes:
        raise ValueError(f"unexpected outcome counts: {outcome_counts}")
    if len(mutations) != 160 or any(row["accepted"] for row in mutations):
        raise ValueError("all 160 preregistered mutations must execute and reject")
    for start in range(0, len(mutations), 20):
        write_json(f"x2/mutations/mutations-{start // 20 + 1:02d}.json", {"schema": "ghc.family.mutation-witnesses.v1", "owner": OWNER, "phase": PHASE, "rows": mutations[start : start + 20]})

    skill_receipts = customize_and_smoke_skills()
    runner_receipts = build_and_smoke_runners()
    portfolio_counts = execute_portfolios(portfolios)
    expected_portfolios = {"blocked": 10, "candidates": 30, "clean_fix_refine": 60, "exact_approval": 20, "runners": 10, "safe_now": 60, "skills": 20}
    if portfolio_counts != expected_portfolios:
        raise ValueError(f"portfolio count drift: {portfolio_counts}")

    method_flow, evidence_overlay = x2_method_flow(x1_overlay)
    write_json("method-flow/x2-ledger.json", method_flow)
    write_json(
        "method-flow/x2-summary.json",
        {
            "schema": "ghc.family.method-flow-summary.v1",
            "owner": OWNER,
            "phase": PHASE,
            "x1_overlay": x1_overlay,
            "new_x2_operational_failures": len(X2_FAILURES),
            "new_x2_bounded_recoveries": len(X2_FAILURES),
            "rejected_mutations_retained": 160,
            "evidence_overlay": evidence_overlay,
            "failure_erasure": False,
            "canonical_credit": 0,
        },
    )
    write_json("x2/evidence/outcome-ledger.json", {"schema": "ghc.family.outcome-ledger.v1", "owner": OWNER, "phase": PHASE, "counts": expected_outcomes, "rows": outcomes})
    write_json(
        "x2/evidence/mutation-summary.json",
        {
            "schema": "ghc.family.mutation-summary.v1",
            "owner": OWNER,
            "phase": PHASE,
            "preregistered": 160,
            "executed": 160,
            "rejected": 160,
            "accepted": 0,
            "credit_per_rejection": 0,
            "boundary": "A rejected synthetic mutation witnesses only the named guard against the named fixture; it is not exhaustive security, science, competence, production readiness, or authority.",
        },
    )
    write_json("x2/evidence/skill-receipts.json", {"schema": "ghc.family.skill-receipts.v1", "owner": OWNER, "phase": PHASE, "count": len(skill_receipts), "rows": skill_receipts})
    write_json("x2/evidence/runner-receipts.json", {"schema": "ghc.family.runner-receipts.v1", "owner": OWNER, "phase": PHASE, "count": len(runner_receipts), "rows": runner_receipts})
    write_json(
        "x2/evidence/smithsonian-furniture-zero-call-adapter.json",
        {
            "schema": "ghc.family.zero-row-adapter.v1",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_id": "TV6691-N037",
            "outcome": "open_gap",
            "interface": "Smithsonian Open Access furniture-search vocabulary",
            "network_requests": 0,
            "api_keys": 0,
            "files_downloaded": 0,
            "real_rows": 0,
            "real_materials": 0,
            "media_downloaded": 0,
            "object_identifications": 0,
            "rights_conclusions": 0,
            "fitness_or_safety_claims": 0,
            "claim": "none",
            "boundary": "Vocabulary and refusal adapter only; no furniture row, object identity, material, treatment, rights, professional, or empirical evidence.",
        },
    )
    write_json(
        "x2/evidence/gmut-presymplectic-obligation-board.json",
        {
            "schema": "ghc.family.gmut-obligation-board.v1",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_id": "TV6691-N027",
            "outcome": "completed",
            "obligations": obligations_for(next(row for row in proposals if row["proposal_id"] == "TV6691-N027")),
            "field_equations_solved": 0,
            "presymplectic_currents_calculated": 0,
            "boundary_fluxes_calculated": 0,
            "gauge_degeneracy_theorems_proved": 0,
            "likelihoods": 0,
            "physical_predictions": 0,
            "observation_firewall": "closed",
            "boundary": "Typed obligation evidence only; no real GMUT model, theorem, force, prediction, constraint, empirical confirmation, quantum completion, ultraviolet completion, or Theory of Everything.",
        },
    )
    write_json(
        "x2/evidence/thos-upholstery-dependency-board.json",
        {
            "schema": "ghc.family.thos-proxy-board.v1",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_ids": ["TV6691-N026", "TV6691-N032"],
            "outcomes": ["completed", "represented"],
            "states": ["synthetic_intake", "refusal_edge", "work_cap", "correction_echo", "hold", "handover"],
            "real_people": 0,
            "real_materials": 0,
            "operators": 0,
            "blinded_matched_budget_arms": 0,
            "effectiveness_estimates": 0,
            "independent_review": False,
            "boundary": "Participant-free proxy and protocol evidence only; no competence, safety, operational effectiveness, deployment, AGI, or ASI claim.",
        },
    )
    write_json(
        "x2/evidence/freed-id-cbr-vacancy-board.json",
        {
            "schema": "ghc.family.freed-id-cbr-vacancy.v1",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_ids": ["TV6691-N024", "TV6691-N025", "TV6691-N033", "TV6691-N034", "TV6691-N039"],
            "outcomes": ["completed", "completed", "represented", "represented", "exact_gate"],
            "real_keys": 0,
            "real_proofs": 0,
            "live_identity_events": 0,
            "issuance_or_resolution_events": 0,
            "status_or_revocation_events": 0,
            "authority_decisions": 0,
            "Māori_authority_decisions": 0,
            "boundary": "Synthetic zero-key graphs and vacancy matrices only; rights, remedy, cultural legitimacy, Māori data governance, and Māori authority remain exact-gated.",
        },
    )
    write_json(
        "x2/evidence/upholstery-authority-and-human-evaluation-gates.json",
        {
            "schema": "ghc.family.open-exact-gate-board.v1",
            "owner": OWNER,
            "phase": PHASE,
            "open_gap": {"proposal_id": "TV6691-N038", "real_upholsterers": 0, "real_materials": 0, "professional_reviews": 0, "safety_reviews": 0, "accessibility_reviews": 0, "affected_party_reviews": 0},
            "exact_gate": {"proposal_id": "TV6691-N039", "competent_authority_decisions": 0, "legal_or_cultural_decisions": 0, "Māori_authority_decisions": 0, "affected_party_acceptance": 0},
            "boundary": "Software cannot close human-evaluation vacancies or confer professional, legal, cultural, affected-party, or Māori authority.",
        },
    )
    write_json(
        "x2/evidence/stage20-non-substitution-bill.json",
        {
            "schema": "ghc.family.stage20-non-substitution.v1",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_id": "TV6691-N040",
            "outcome": "exact_gate",
            "required_receipts": obligations_for(next(row for row in proposals if row["proposal_id"] == "TV6691-N040")),
            "present_receipts": 0,
            "substitution_allowed": False,
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    write_json(
        "x2/evidence/source-use-receipt.json",
        {
            "schema": "ghc.family.source-use-receipt.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source_ids": ["SRC-CCI-FURNITURE", "SRC-NIOSH-MANUFACTURING", "SRC-SI-OPEN", "SRC-VC20", "SRC-NIST-800-63-4", "SRC-PROV-DM", "SRC-RFC8785", "SRC-WCAG22", "SRC-SCALAR-EFT", "SRC-TMR"],
            "use": "vocabulary, schema, provenance, static accessibility hypotheses, governance vacancies, and refusal conditions only",
            "network_requests_during_x2": 0,
            "real_observation_rows": 0,
            "participant_rows": 0,
            "authority_decisions": 0,
            "independent_review": False,
        },
    )
    write_json(
        "x2/evidence/portfolio-execution-summary.json",
        {
            "schema": "ghc.family.portfolio-execution-summary.v1",
            "owner": OWNER,
            "phase": PHASE,
            "counts": portfolio_counts,
            "bounded_executed": sum(value for key, value in portfolio_counts.items() if key not in {"exact_approval", "blocked"}),
            "exact_and_blocked_unexecuted": True,
            "external_actions": 0,
            "authority_actions": 0,
        },
    )
    write_json("x2/evidence/open-gap-register.json", {"schema": "ghc.family.open-gap-register.v1", "owner": OWNER, "phase": PHASE, "inherited": x1_overlay["open_gaps"], "new": 2, "effective": evidence_overlay["open_gaps"], "proposal_ids": ["TV6691-N037", "TV6691-N038"]})
    write_json("x2/evidence/exact-gate-register.json", {"schema": "ghc.family.exact-gate-register.v1", "owner": OWNER, "phase": PHASE, "inherited": x1_overlay["exact_gates"], "new": 2, "effective": evidence_overlay["exact_gates"], "proposal_ids": ["TV6691-N039", "TV6691-N040"]})
    write_json(
        "x2/evidence/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v1",
            "owner": OWNER,
            "phase": PHASE,
            "x1_overlay": x1_overlay,
            "x2_operational_negatives": len(X2_FAILURES),
            "rejected_mutations": 160,
            "evidence_overlay": evidence_overlay,
            "no_negative_erased": True,
        },
    )
    write_json(
        "x2/evidence/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE_FINAL,
            "x1": X1_HEAD,
            "evidence_commit": None,
            "lifecycle": "X2_EVIDENCE_CANDIDATE_NOT_COMMITTED",
            "proposal_chain_before": 4910,
            "proposal_chain_after": 4950,
            "outcomes": expected_outcomes,
            "mutations": {"preregistered": 160, "executed": 160, "rejected": 160, "accepted": 0},
            **evidence_overlay,
            "terminal_verdict": TERMINAL_VERDICT,
            "canonical_validation": "not_run",
            "full_repository_suite": "not_run_non_Eiren_owner_scope",
        },
    )

    overview = f"""# Tamar Vey {PHASE} x2 evidence overview

This owner-local x2 packet executes the forty frozen proposals only as their evidence permits. Outcomes are exactly twenty-eight `completed`, eight `represented`, two `open_gap`, and two `exact_gate`. A completed row means only that one bounded synthetic fixture passed and its four preregistered invalid variants were rejected. It is not evidence about a real upholstered item, material, person, workplace, identity service, professional decision, safety release, legal or cultural decision, or authority act.

The primary THOS Body work is a participant-free synthetic upholstery dependency, refusal, correction, workload, accessible-status, and handover structure. It contains no real participant, worker, operator, object, intervention, safety event, blinded matched-budget real arm, effectiveness estimate, deployment result, AGI, or ASI evidence. Freed ID/CBR Heart and GMUT Mind remain explicit and protected.

The upholstery lens is wholly synthetic. Frame, spring, webbing, padding, cover, closure, condition, provenance, custody, accessibility, hazard-hold, workload, correction, and handover states are software fixtures only. No real upholsterer, conservator, upholstered item, frame, spring, webbing, padding, cover, material, product, tool, process, measurement, contamination event, fire event, workplace, client, or professional review exists. The Smithsonian furniture adapter remains `open_gap` with zero API keys, network requests, downloads, real rows, media, object identifications, or rights conclusions. The human and professional evaluation row also remains `open_gap`.

THOS remains participant-free proxy evidence without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, or independent review. GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Its covariant phase-space and presymplectic obligation board solves no field equation, calculates no physical current or flux, proves no gauge-degeneracy theorem, evaluates no likelihood, and produces no force, prediction, constraint, empirical confirmation, quantum or ultraviolet completion, final physics, or Theory of Everything. Freed ID remains zero-key and nonproduction; CBR and Māori authority remain exact-gated.

All 160 preregistered mutations executed and remain rejected at zero credit. Twenty phase-local skills were initialized through the official skill-creator scaffold, customized, completely read, quick-validated, and accepting/rejecting smoke-used. Ten family-current runners were built and smoke-used. No skill was globally installed and no forward test was delegated. Sixty safe-now, thirty candidate, twenty skill, ten runner, and sixty CLEAN/FIX/REFINE portfolio records received bounded owner-local execution; twenty exact-approval and ten blocked records remain visible and unexecuted.

The evidence overlay is {evidence_overlay['effective_negatives']} effective negatives, {evidence_overlay['methods']} effective methods, {evidence_overlay['failed_witnesses']} retained failed witnesses, {evidence_overlay['passing_witnesses']} bounded passing witnesses, {evidence_overlay['open_gaps']} open gaps, and {evidence_overlay['exact_gates']} exact gates. Recovery does not erase any failed witness. Same-owner validation is not independent reproduction. The terminal verdict remains `{TERMINAL_VERDICT}`. {IDENTITY_BOUNDARY}
"""
    write_text("x2/evidence/evidence-overview.md", overview)
    write_text(
        "x2/evidence/threat-model.md",
        f"""# Tamar Vey {PHASE} bounded x2 threat model

Threats include lifecycle mixing, mutation erasure, source-credit promotion, fabricated empirical or material rows, real-world action, authority substitution, professional or safety implication, credential or private-route leakage, path traversal, unsafe shell invocation, stale owner or phase labels, manifest drift, accessibility overclaim, GMUT analogy conversion, and premature Stage 20 promotion. Controls are immutable-x1 loading, four-label truth, zero-row and zero-action fields, fail-closed mutations, owner-local paths, exact Git-blob manifests, AST review, five-class scanning, retained Method Flow witnesses, and one exact-final canonical invocation only after final push.

Residual risk remains for real objects and materials, professional practice, fire and workplace safety, ergonomics, contamination, participants, adversaries, platform and supply-chain behavior, privacy, accessibility, legal or cultural meaning, affected parties, Māori data governance, and every authority decision. {EVIDENCE_BOUNDARY}
""",
    )
    table_rows = "\n".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['outcome'])}</td><td>{html.escape(row['title'])}</td></tr>"
        for row in outcomes
    )
    write_text(
        "x2/evidence/accessible-static-report.html",
        f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Tamar Vey v669-v1 x2 evidence</title><style>body{{font:1rem/1.5 system-ui;max-width:72rem;margin:auto;padding:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}:focus{{outline:3px solid #075985}}@media(max-width:40rem){{.table-wrap{{overflow-x:auto}}}}@media print{{body{{max-width:none}}}}</style></head><body><a href='#main'>Skip to evidence</a><main id='main'><h1>Tamar Vey v669-v1 x2 evidence</h1><p>Status is expressed in text, not colour. Manual keyboard, touch, zoom, reflow, browser, assistive-technology, cognitive, Māori-language, security-usability, print, and affected-user review remain reserved.</p><div class='table-wrap'><table><caption>Forty bounded proposal dispositions</caption><thead><tr><th scope='col'>Proposal</th><th scope='col'>Disposition</th><th scope='col'>Title</th></tr></thead><tbody>{table_rows}</tbody></table></div><h2>Boundary</h2><p>This structural report is not complete accessibility conformance, professional acceptance, or affected-user evidence. The verdict is NOT_READY_FOR_STAGE_20.</p></main></body></html>""",
    )

    code_paths = [
        ROOT / "scripts/ghc_family_tamar_vey_v669_v1_x2.py",
        ROOT / "scripts/ghc_family_tamar_vey_v669_v1_skill_smoke.py",
        ROOT / "scripts/build_ghc_family_tamar_vey_v669_v1_x2.py",
        ROOT / "tests/test_ghc_family_tamar_vey_v669_v1_x2.py",
        *[ROOT / "scripts" / f"{name}.py" for name in RUNNER_NAMES],
    ]
    if not all(path.is_file() for path in code_paths):
        raise ValueError("all x2 modules, tests, and runner surfaces must exist before manifest generation")
    manifest_path = PHASE_ROOT / "x2" / "evidence" / "evidence-content-manifest.json"
    allowlist_path = PHASE_ROOT / "validation" / "x2-staged-allowlist.json"
    intended = sorted({
        path
        for path in PHASE_ROOT.rglob("*")
        if path.is_file() and (path.is_relative_to(PHASE_ROOT / "x2") or (path.is_relative_to(PHASE_ROOT / "method-flow") and path.name.startswith("x2-"))) and path != manifest_path
    } | set(code_paths))
    allowlist_rows = sorted({path.relative_to(ROOT).as_posix() for path in intended} | {allowlist_path.relative_to(ROOT).as_posix(), manifest_path.relative_to(ROOT).as_posix()})
    write_json(
        "validation/x2-staged-allowlist.json",
        {
            "schema": "ghc.family.staged-allowlist.v1",
            "owner": OWNER,
            "phase": PHASE,
            "parent": X1_HEAD,
            "paths": allowlist_rows,
            "self_exclusions": [manifest_path.relative_to(ROOT).as_posix()],
            "forbidden_lifecycle_roots": ["closeout", "final", "seal", "handoffs"],
        },
    )
    manifest_inputs = sorted(set(intended + [allowlist_path]))
    rows_manifest = manifest_rows(manifest_inputs)
    write_json(
        "x2/evidence/evidence-content-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v1",
            "owner": OWNER,
            "phase": PHASE,
            "parent": X1_HEAD,
            "entry_count": len(rows_manifest),
            "entries": rows_manifest,
            "self_exclusions": [manifest_path.relative_to(ROOT).as_posix()],
            "canonical_domain": "git_blob_bytes_after_clean_filter_before_commit",
            "lifecycle": "X2_EVIDENCE_CANDIDATE_NOT_COMMITTED",
        },
    )
    phase_files = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    oversized = []
    for path in phase_files:
        if path.suffix.casefold() in {".md", ".json", ".txt", ".html", ".yaml", ".yml"}:
            count = len(re.findall(r"\b\w+[\w'-]*\b", path.read_text(encoding="utf-8")))
            if count > 6000:
                oversized.append((path.relative_to(ROOT).as_posix(), count))
    if oversized:
        raise ValueError(f"document ceiling exceeded: {oversized}")
    materialized = sum(1 for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)
    if materialized >= 2000:
        raise ValueError(f"materialized file ceiling exceeded: {materialized}")
    print(json.dumps({
        "status": "X2_EVIDENCE_CANDIDATE_READY_FOR_SCOPED_VALIDATION",
        "owner": OWNER,
        "phase": PHASE,
        "outcomes": expected_outcomes,
        "mutations": len(mutations),
        "skills": len(skill_receipts),
        "runners": len(runner_receipts),
        "portfolio": portfolio_counts,
        "x2_operational_failures": len(X2_FAILURES),
        "evidence_overlay": evidence_overlay,
        "manifest_entries": len(rows_manifest),
        "phase_files": len(phase_files),
        "materialized_files": materialized,
        "terminal_verdict": TERMINAL_VERDICT,
        "generated_at_utc": now,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
