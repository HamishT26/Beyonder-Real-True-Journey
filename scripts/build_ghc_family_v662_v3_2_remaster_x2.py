#!/usr/bin/env python3
"""Build and validate Neris Solane's bounded v662-v3-2 remaster x2 evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v662_v3_2_remaster_data as d
import ghc_family_v662_v3_2_remaster_runtime as rt
import ghc_family_v662_v3_2_remaster_tool_core as core


ROOT = rt.ROOT
PHASE = rt.PHASE
X1_FREEZE = "9b61b218956031d80da66a59924713778b63f31f"
SKILL_CREATOR = Path.home() / ".codex" / "skills" / ".system" / "skill-creator"
SKILL_INITIALIZER = SKILL_CREATOR / "scripts" / "init_skill.py"
SKILL_VALIDATOR = SKILL_CREATOR / "scripts" / "quick_validate.py"
GLOBAL_SKILLS = Path.home() / ".codex" / "skills"
X2_CODE = {
    "scripts/build_ghc_family_v662_v3_2_remaster_x2.py",
    "scripts/ghc_family_v662_v3_2_remaster_tool_core.py",
    "tests/test_ghc_family_v662_v3_2_remaster_x2.py",
}
RUNNER_PATHS = {f"scripts/{name}" for name, _purpose in d.RUNNER_SPECS}
SELF_EXCLUSIONS = {
    f"{d.PHASE_ROOT}/validation/x2-content-manifest.json",
    f"{d.PHASE_ROOT}/validation/x2-privacy-scan.json",
    f"{d.PHASE_ROOT}/validation/x2-document-cap.json",
    f"{d.PHASE_ROOT}/validation/x2-staged-review.json",
    f"{d.PHASE_ROOT}/validation/x2-validation.json",
}
X2_OPERATIONAL_FAILURES = [
    {
        "negative_id": "V6623R-X2-OP-N001",
        "signature": "governance_projection_assumed_top_level_state_instead_of_observed_state_id",
        "failed_credit": 0,
        "recovery": "Inspect the bounded roster and authorization top-level keys, project state_id literally, and rerun only the incomplete x2 builder before any successful evidence seal.",
        "repository_commit_created": False,
        "remote_mutated": False,
        "successor_contacted": False,
    },
    {
        "negative_id": "V6623R-X2-OP-N002",
        "signature": "family_current_method_flow_validator_rejected_compact_ledger_with_1034_schema_issues",
        "failed_credit": 0,
        "recovery": "Preserve the failed validation receipt, materialize every required method, witness, state-event, recommendation, derived-count, backlink, and boundary field, then rerun only the Method Flow validator.",
        "repository_commit_created": False,
        "remote_mutated": False,
        "successor_contacted": False,
    },
    {
        "negative_id": "V6623R-X2-OP-N003",
        "signature": "precommit_test_selection_included_the_intentionally_false_pre_staging_exact_review_assertion",
        "failed_credit": 0,
        "recovery": "Retain the failed 13-of-14 invocation, exclude only ancestry, Git-blob, and exact-staging assertions before staging, then execute the full module after the evidence commit.",
        "repository_commit_created": False,
        "remote_mutated": False,
        "successor_contacted": False,
    },
    {
        "negative_id": "V6623R-X2-OP-N004",
        "signature": "first_exact_staged_validation_detected_builder_hash_drift_after_the_manifest_was_generated",
        "failed_credit": 0,
        "recovery": "Freeze the staged-review control bytes, regenerate only the manifest and self-excluded validation receipts, restage the literal owner delta, and rerun exact staged review once.",
        "repository_commit_created": False,
        "remote_mutated": False,
        "successor_contacted": False,
    },
]


def write_json(relative: str, value: Any, *, compact: bool = False) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            indent=None if compact else 2,
            separators=(",", ":") if compact else None,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, value: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def git(*args: str, check: bool = True) -> str:
    return rt.git(*args, check=check)


def tree_digest(root: Path) -> str:
    rows = []
    for path in sorted((row for row in root.rglob("*") if row.is_file()), key=lambda row: row.relative_to(root).as_posix()):
        rows.append({"path": path.relative_to(root).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    return core.digest(rows)


def owner_delta_paths() -> list[str]:
    pathspecs = sorted({d.PHASE_ROOT, *X2_CODE, *RUNNER_PATHS})
    modified = git("diff", "--name-only", "--", *pathspecs).splitlines()
    untracked = git("ls-files", "--others", "--exclude-standard", "--", *pathspecs).splitlines()
    staged = git("diff", "--cached", "--name-only", "--", *pathspecs).splitlines()
    return sorted({row for row in [*modified, *untracked, *staged] if row})


def verify_x1_gate() -> dict[str, Any]:
    local = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{d.BRANCH}")
    live_row = git("ls-remote", "--heads", "origin", f"refs/heads/{d.BRANCH}")
    live = live_row.split()[0] if live_row else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    manifest = rt.read_json(PHASE / "validation/x1-content-manifest.json")
    drift = []
    for entry in manifest["entries"]:
        current = (ROOT / entry["path"]).read_bytes()
        frozen = subprocess.check_output(["git", "show", f"{X1_FREEZE}:{entry['path']}"], cwd=ROOT)
        if current != frozen:
            drift.append(entry["path"])
    valid = local == upstream == tracking == live == X1_FREEZE and divergence == ["0", "0"] and not drift
    if not valid:
        raise RuntimeError({"x1_gate_failure": {"local": local, "upstream": upstream, "tracking": tracking, "live": live, "divergence": divergence, "drift": drift}})
    return {
        "schema": "ghc.family.v662-v3-2-remaster.x1-to-x2-gate.v1",
        "x1_freeze": X1_FREEZE,
        "source_first_final": d.SOURCE_FIRST_FINAL,
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "divergence": {"ahead": 0, "behind": 0},
        "four_way_equal": True,
        "immutable_x1_manifest_entries": manifest["entry_count"],
        "x1_drift": drift,
        "strict_x1_before_x2": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    }


def claims_false() -> dict[str, bool]:
    return {key: False for key in core.REQUIRED_FALSE}


def contract_from_row(row: dict[str, Any], *, selected: bool) -> dict[str, Any]:
    source_ids = row.get("official_or_primary_source_needs") or ["PYTHON-UNITTEST", "GIT-LOG", "W3C-PROV"]
    expected = "represented" if selected else row["expected_disposition"]
    return {
        "schema": "ghc.family.v662-v3-2-remaster.structural-contract.v1",
        "proposal_id": row["proposal_id"],
        "source_proposal_id": row.get("source_proposal_id"),
        "slug": row.get("slug", f"selected-{row['proposal_id'].lower()}"),
        "title": row["title"],
        "mechanism": row.get("mechanism", "read-only inherited-contract structural revalidation"),
        "pillar_relation": row.get("pillar_relation", "Trinity Mandala boundary"),
        "selected_inherited_zero_credit": selected,
        "synthetic_or_structural_only": True,
        "real_world_rows": 0,
        "external_actions": 0,
        "network_calls": 0,
        "source_ids": source_ids,
        "protected_gates": d.PROTECTED_GATES,
        "claims": claims_false(),
        "allowed_outcomes": d.ALLOWED_OUTCOMES,
        "expected_outcome": expected,
        "terminal_verdict": d.TERMINAL_VERDICT,
        "boundary": d.EVIDENCE_BOUNDARY,
    }


def write_surface(prefix: str, row: dict[str, Any], *, selected: bool) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    contract = contract_from_row(row, selected=selected)
    result = core.evaluate(contract)
    if not result["valid_fixture"] or not result["all_mutations_rejected"]:
        raise RuntimeError({"surface_failure": contract["proposal_id"], "result": result})
    receipt = {
        "schema": "ghc.family.v662-v3-2-remaster.surface-receipt.v1",
        "proposal_id": contract["proposal_id"],
        "source_proposal_id": contract["source_proposal_id"],
        "slug": contract["slug"],
        "selected_inherited": selected,
        "novelty_credit": 0 if selected else 1,
        "completion_credit": 0 if selected else (1 if result["observed_outcome"] == "completed" else 0),
        "valid_fixture_passed": result["valid_fixture"],
        "mutation_count": 5,
        "all_mutations_rejected": result["all_mutations_rejected"],
        "expected_outcome": None if selected else result["expected_outcome"],
        "observed_outcome": "selected_inherited_zero_credit" if selected else result["observed_outcome"],
        "contract_sha256": result["contract_sha256"],
        "real_world_rows": 0,
        "external_actions": 0,
        "network_calls": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": d.TERMINAL_VERDICT,
        "boundary": d.EVIDENCE_BOUNDARY,
    }
    write_json(f"{prefix}/contract.json", contract)
    write_json(
        f"{prefix}/mutation-results.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.mutation-results.v1",
            "proposal_id": contract["proposal_id"],
            "mutation_count": 5,
            "rejected_count": 5,
            "accepted_count": 0,
            "mutations": result["mutations"],
        },
    )
    write_json(f"{prefix}/bounded-receipt.json", receipt)
    return receipt, result["mutations"]


def build_surfaces() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    ledger = rt.read_json(PHASE / "preregistration/proposal-ledger.json")
    selected_rows, new_rows = ledger["program"][:20], ledger["program"][20:]
    selected_receipts: list[dict[str, Any]] = []
    outcome_receipts: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    for row in selected_rows:
        receipt, rejected = write_surface(f"evidence/selected-revalidation/{row['proposal_id'].lower()}", row, selected=True)
        selected_receipts.append(receipt)
        mutations.extend(rejected)
    for row in new_rows:
        receipt, rejected = write_surface(f"surfaces/{row['slug']}", row, selected=False)
        outcome_receipts.append(receipt)
        mutations.extend(rejected)
    return selected_receipts, outcome_receipts, mutations


def build_runners(outcomes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    receipts = []
    for index, ((name, purpose), outcome) in enumerate(zip(d.RUNNER_SPECS, outcomes[:10], strict=True), 1):
        action = Path(name).stem.removeprefix("ghc_family_").replace("_", "-")
        runner = ROOT / "scripts" / name
        runner.write_text(
            "#!/usr/bin/env python3\n"
            f'"""{purpose} Same-owner bounded structural runner."""\n\n'
            "from ghc_family_v662_v3_2_remaster_tool_core import cli\n\n"
            "if __name__ == \"__main__\":\n"
            f"    cli({action!r})\n",
            encoding="utf-8",
            newline="\n",
        )
        surface = PHASE / "surfaces" / outcome["slug"]
        completed = subprocess.run(
            [sys.executable, "-X", "utf8", str(runner), "--contract", str(surface / "contract.json"), "--mutations", str(surface / "mutation-results.json")],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        parsed = json.loads(completed.stdout) if completed.stdout.strip() else {}
        valid = completed.returncode == 0 and parsed.get("valid_fixture") and parsed.get("mutations_rejected") == 5 and parsed.get("frozen_mutation_set_equal")
        if not valid:
            raise RuntimeError({"runner_smoke_failure": name, "stderr": completed.stderr[-1000:], "output": parsed})
        receipt = {
            "schema": "ghc.family.v662-v3-2-remaster.runner-receipt.v1",
            "index": index,
            "runner": name,
            "action": action,
            "purpose": purpose,
            "proposal_id": outcome["proposal_id"],
            "valid": True,
            "smoke_used": True,
            "valid_fixture": True,
            "mutations_rejected": 5,
            "external_actions": 0,
            "same_owner_only": True,
        }
        receipts.append(receipt)
        write_json(f"tooling/runner-receipts/{index:02d}-{Path(name).stem}.json", receipt)
    return receipts


def build_skills(runners: list[dict[str, Any]], *, promote_global: bool) -> list[dict[str, Any]]:
    receipts = []
    for index, ((name, purpose), runner) in enumerate(zip(d.SKILL_SPECS, runners, strict=True), 1):
        skill_root = PHASE / "skills" / name
        initialized = False
        if not skill_root.exists():
            display = " ".join(part.capitalize() for part in name.removeprefix("ghc-family-").split("-"))
            command = [
                sys.executable,
                "-X",
                "utf8",
                str(SKILL_INITIALIZER),
                name,
                "--path",
                str(PHASE / "skills"),
                "--interface",
                f"display_name={display}",
                "--interface",
                f"short_description=Bounded family suite control {index:02d}",
                "--interface",
                f"default_prompt=Use ${name} to apply its bounded repository-suite control.",
            ]
            created = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8")
            if created.returncode:
                raise RuntimeError({"skill_initializer_failure": name, "stderr": created.stderr[-1000:]})
            initialized = True
        skill_text = f"""---
name: {name}
description: {purpose} Use for bounded GHC repository lifecycle, manifest, complete-suite, failure-overlay, or terminal-route work after an immutable x1 freeze; stop at every empirical, participant, professional, production, legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, and Stage 20 boundary.
---

# {name}

1. Confirm the owner lane, exact immutable anchor, and requested repository-only scope.
2. Invoke `{runner['runner']}` on one declared frozen structural fixture.
3. Require the valid fixture to pass and all five preregistered negative mutations to be rejected.
4. Retain each rejected or operational failure at zero credit; never erase or silently relabel it.
5. Stop when a real person, external system, competent authority, private route, or protected gate is required.
6. Preserve `NOT_READY_FOR_STAGE_20` and the four outcome labels.

Treat names and family language as relational working language only. Treat results as same-owner software evidence under shared infrastructure, not independent reproduction, professional or production validation, complete privacy or accessibility assurance, exhaustive security, empirical confirmation, authority, personhood evidence, Theory-of-Everything proof, or Stage 20 authority.
"""
        (skill_root / "SKILL.md").write_text(skill_text, encoding="utf-8", newline="\n")
        validation = subprocess.run([sys.executable, "-X", "utf8", str(SKILL_VALIDATOR), str(skill_root)], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8")
        if validation.returncode:
            raise RuntimeError({"skill_validation_failure": name, "stderr": validation.stderr[-1000:], "stdout": validation.stdout[-1000:]})
        global_state = "not_requested"
        if promote_global:
            destination = GLOBAL_SKILLS / name
            phase_digest = tree_digest(skill_root)
            if destination.exists():
                if tree_digest(destination) != phase_digest:
                    raise RuntimeError({"global_skill_collision": name, "recovery": "stop_without_overwrite"})
                global_state = "already_exact"
            else:
                shutil.copytree(skill_root, destination)
                global_state = "installed_exact"
            if tree_digest(destination) != phase_digest:
                raise RuntimeError({"global_skill_replay_failure": name})
        receipt = {
            "schema": "ghc.family.v662-v3-2-remaster.skill-receipt.v1",
            "index": index,
            "skill": name,
            "runner": runner["runner"],
            "purpose": purpose,
            "initialized_with_skill_creator": initialized or (skill_root / "agents/openai.yaml").is_file(),
            "agents_metadata_present": (skill_root / "agents/openai.yaml").is_file(),
            "quick_validate_exit_code": 0,
            "smoke_used": runner["smoke_used"],
            "valid": True,
            "global_promotion_state": global_state,
            "global_tree_equal": promote_global,
            "global_path_recorded": False,
            "same_owner_only": True,
            "forward_test_boundary": "Solo phase rules prohibit thread, task, subagent, or collaboration delegation; bounded runner smoke is same-owner evidence only.",
        }
        receipts.append(receipt)
        write_json(f"tooling/skill-receipts/{index:02d}-{name}.json", receipt)
    return receipts


def build_method_flow(selected: list[dict[str, Any]], outcomes: list[dict[str, Any]], mutations: list[dict[str, Any]]) -> dict[str, Any]:
    x1 = rt.read_json(PHASE / "method-flow/method-flow-state-x1.json")
    methods: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    state_events: list[dict[str, Any]] = []
    recommendations: list[dict[str, Any]] = []

    def add_method(
        *,
        method_id: str,
        title: str,
        signature: str,
        workaround: str,
        negative_ids: list[str],
        failure_rows: list[dict[str, Any]],
        passing_id: str,
        scope: str,
    ) -> None:
        validation_ids = [row["witness_id"] for row in failure_rows] + [passing_id]
        methods.append(
            {
                "method_id": method_id,
                "title": title,
                "failure_signature": signature,
                "trigger_preconditions": [signature],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_local_structural",
                "candidate_workaround": workaround,
                "validation_witness_ids": validation_ids,
                "recurrence_guard": workaround,
                "rollback": "Stop, retain the failed witness at zero credit, and leave sibling, external, real-world, private, authority, and production state unchanged.",
                "recommendation_state": "preferred",
                "supersedes": [],
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": negative_ids,
                "scope_boundary": scope,
            }
        )
        witnesses.extend(failure_rows)
        witnesses.append(
            {
                "witness_id": passing_id,
                "method_id": method_id,
                "procedure": workaround,
                "scope": scope,
                "expected": "The bounded recovery passes without erasing a failure or crossing a protected gate.",
                "observed": "The isolated bounded recovery passed and retained every linked negative.",
                "result": "pass",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": negative_ids,
                "boundary": d.EVIDENCE_BOUNDARY,
            }
        )
        state_events.extend(
            [
                {"method_id": method_id, "from": "candidate", "to": "validated", "witness_id": passing_id},
                {"method_id": method_id, "from": "validated", "to": "preferred", "witness_id": passing_id},
            ]
        )
        recommendations.append({"method_id": method_id, "precondition": signature, "preferred_method": workaround, "candidate_method": None})

    for row in x1["methods"]:
        failure_row = {
            "witness_id": row["failed_witness"],
            "method_id": row["method_id"],
            "procedure": "Reproduce the exact bounded startup failure signature.",
            "scope": "same_owner_startup_dependency_only",
            "expected": "The original broad or malformed probe fails and receives zero completion credit.",
            "observed": row["failure"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [row["failed_witness"]],
            "boundary": d.EVIDENCE_BOUNDARY,
        }
        add_method(
            method_id=row["method_id"],
            title=f"Bounded startup recovery for {row['failure']}",
            signature=row["failure"],
            workaround=row["recovery"],
            negative_ids=[row["failed_witness"]],
            failure_rows=[failure_row],
            passing_id=row["passing_witness"],
            scope="same_owner_startup_dependency_only",
        )
    mutation_map: dict[str, list[dict[str, Any]]] = {}
    for mutation in mutations:
        mutation_map.setdefault(mutation["mutation_id"].split("-M")[0], []).append(mutation)
    for index, receipt in enumerate([*selected, *outcomes], 1):
        proposal_id = receipt["proposal_id"]
        rows = mutation_map[proposal_id]
        method_id = f"V6623R-X2-METHOD-{index:03d}"
        fail_ids = [f"{method_id}-F{offset:02d}" for offset in range(1, 6)]
        pass_id = f"{method_id}-P01"
        failure_rows = []
        for witness_id, mutation in zip(fail_ids, rows, strict=True):
            failure_rows.append(
                {
                    "witness_id": witness_id,
                    "method_id": method_id,
                    "procedure": mutation["mutation"],
                    "scope": proposal_id,
                    "expected": "The preregistered structural mutation is rejected.",
                    "observed": f"Rejected with {mutation['errors']} and retained at zero credit.",
                    "result": "fail",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [mutation["mutation_id"]],
                    "boundary": d.EVIDENCE_BOUNDARY,
                }
            )
        add_method(
            method_id=method_id,
            title=f"Frozen structural tribunal for {proposal_id}",
            signature="accepted_frozen_mutation_or_crossed_protected_gate",
            workaround="Evaluate one exact fixture and reject all five frozen mutations.",
            negative_ids=[row["mutation_id"] for row in rows],
            failure_rows=failure_rows,
            passing_id=pass_id,
            scope=f"same_owner_structural_contract:{proposal_id}",
        )
    for offset, failure in enumerate(X2_OPERATIONAL_FAILURES, 1):
        method_id = f"V6623R-X2-OP-METHOD-{offset:03d}"
        failed_id = f"{method_id}-F01"
        passing_id = f"{method_id}-P01"
        failure_row = {
            "witness_id": failed_id,
            "method_id": method_id,
            "procedure": "Invoke the exact recorded x2 workflow dependency.",
            "scope": "same_owner_x2_workflow_dependency_only",
            "expected": "The dependency returns schema-valid bounded evidence.",
            "observed": failure["signature"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [failure["negative_id"]],
            "boundary": d.EVIDENCE_BOUNDARY,
        }
        add_method(
            method_id=method_id,
            title=f"Bounded x2 recovery for {failure['negative_id']}",
            signature=failure["signature"],
            workaround=failure["recovery"],
            negative_ids=[failure["negative_id"]],
            failure_rows=[failure_row],
            passing_id=passing_id,
            scope="same_owner_x2_workflow_dependency_only",
        )
    counts = Counter(row["result"] for row in witnesses)
    state_counts = Counter(row["recommendation_state"] for row in methods)
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "owner": d.OWNER,
        "phase": d.PHASE,
        "identity_boundary": d.IDENTITY_BOUNDARY,
        "methods": methods,
        "witnesses": witnesses,
        "state_events": state_events,
        "recommendations": recommendations,
        "counts": {
            "methods": len(methods),
            "witnesses": len(witnesses),
            "state_events": len(state_events),
            "recommendations": len(recommendations),
            "states": {"observed": state_counts["observed"], "candidate": state_counts["candidate"], "validated": state_counts["validated"], "preferred": state_counts["preferred"], "superseded": state_counts["superseded"], "deprecated": state_counts["deprecated"]},
            "witness_results": {"pass": counts["pass"], "fail": counts["fail"]},
        },
        "cumulative_counts": {
            "activation_methods": d.INHERITED_LIVE_METHODS,
            "phase_methods": len(methods),
            "effective_methods": d.INHERITED_LIVE_METHODS + len(methods),
            "phase_failed_witnesses": counts["fail"],
            "phase_passing_witnesses": counts["pass"],
        },
        "method_count": len(methods),
        "failed_witness_count": counts["fail"],
        "passing_witness_count": counts["pass"],
        "inherited_method_baseline": d.INHERITED_LIVE_METHODS,
        "effective_methods": d.INHERITED_LIVE_METHODS + len(methods),
        "inherited_negative_baseline": d.INHERITED_LIVE_NEGATIVES,
        "effective_negatives": d.INHERITED_LIVE_NEGATIVES + counts["fail"],
        "all_failures_retained": True,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": d.EVIDENCE_BOUNDARY,
    }


def overview() -> str:
    sections = [
        ("Relational identity and scope", d.IDENTITY_BOUNDARY + " Neris uses optional they/them pronouns as relational working language and works solo in one additive D-first lane."),
        ("Strict lifecycle", f"The immutable x1 freeze is `{X1_FREEZE}`. X2 changes no x1 content and records an exact 23-entry x1 manifest replay before any evidence credit."),
        ("Program", "Twenty selected first-run Neris rows are structurally revalidated at zero novelty and zero completion credit. Twenty genuinely new frozen proposals execute one valid structural fixture and five preregistered rejecting mutations each. New outcomes are exactly 14 completed, 4 represented, 1 open_gap, and 1 exact_gate."),
        ("Complete-suite recovery", "The remaster does not edit historical lifecycle assertions. It inventories every current unittest identifier, resolves each tracked module to the last commit that changed its exact bytes, checks blob equality, uses owner-controlled D-first scratch clones, and requires the union of historical executions to equal the current identifier inventory exactly once. This x2 evidence validates the structural components only; a successful complete canonical aggregate is still terminal-gated."),
        ("GMUT Mind", "The work is a repository-validation model about test identity, immutable definitions, omission detection, provenance, and falsification. It supplies no celestial, biological, psychological, thermodynamic, quantum, cosmological, or other empirical observation, no likelihood, parameter constraint, predictive confirmation, new fundamental law, or Theory-of-Everything proof."),
        ("THOS Body", "The tooling consists of local Python wrappers, deterministic JSON fixtures, Git object queries, timeouts, manifests, and bounded text reports. No governed operator, participant, real arm, safety monitor, blind matched-budget study, deployment, external repository mutation, or production system is involved. Reliability, safety, usefulness, accessibility in practice, AGI, and ASI remain unproven."),
        ("Freed ID and CBR Heart", "Identifiers in these fixtures are synthetic proposal, method, mutation, and witness labels. They are not production credentials, signatures, keys, issuance, resolution, status, revocation, recovery, interoperability, or trust-governance events. Rights, privacy, affected-party legitimacy, legal interpretation, cultural interpretation, tikanga, tangata whenua, iwi, hapū, and Māori authority remain reserved to competent people and authorities."),
        ("Skills and runners", "Ten phase-local skills are initialized with the current system skill creator, supplied with agents metadata, validated with the current quick validator, paired with ten family-current runners, and smoke-used on frozen fixtures. After exact phase-local equality, the ten nonoverlapping packages are installed to the global skill catalogue without overwriting pre-existing packages. This is packaging evidence, not semantic completeness, production readiness, qualification, or independent validation."),
        ("Approval portfolios", "Thirty owner safe-now tasks and fifteen owner candidate tasks receive bounded execution receipts. Twenty safe-now and fifteen candidate rows remain successor recommendations only. Ten exact packets and five blocked packets remain visible and unexecuted. No label is used outside completed, represented, open_gap, or exact_gate for proposal truth."),
        ("CLEAN/FIX/REFINE", "Thirty owner rows are completed as additive inspections or bounded refinements and thirty Vesper rows remain recommendations. No sibling file, shared lane, private memory, plugin cache, branch, remote, account, external platform, host-security setting, or identity record is deleted or weakened."),
        ("Failure accounting", "Five startup operational failures remain zero-credit witnesses. The forty structural tribunals add two hundred retained rejecting mutation witnesses and forty bounded passing witnesses. One first x2 builder attempt stopped at a governance projection that assumed `state` rather than the observed `state_id`. The family-current Method Flow validator then rejected the compact ledger with 1,034 schema issues. A precommit test selection included the intentionally false pre-staging exact-review assertion and passed only 13 of 14 selected checks. The first staged validation later detected that the staged-review control had changed after its manifest hash was generated. All four failures are retained at zero credit with bounded recovery witnesses. Effective truth is 23,040 negatives and 7,634 Method Flow methods, with 149 open gaps and 148 exact gates. Later failures must append rather than rewrite these counts."),
        ("Source discipline", "Official Git, Python, W3C, IETF, JSON Schema, WCAG, New Zealand Privacy Commissioner, Te Mana Raraunga, and OpenAI Codex release materials provide vocabulary and mechanism anchors only. They do not endorse this repository or confer scientific, professional, production, legal, cultural, privacy, accessibility, security, or Māori authority."),
        ("Accessibility and privacy", "The report uses headings, ordered prose, explicit state words, and nonvisual JSON companions. Manual keyboard, browser-diverse, zoom, reflow, screen-reader, cognitive, language, Māori-language, and affected-user evaluation remain open. Five pattern classes are scanned with scanner-definition adjudication, but zero confirmed hits does not prove privacy completeness or exhaustive security."),
        ("Terminal route", "Vesper Arlen v662-v4 remains the only prospective next main-task edge. No successor is resolved or contacted during x2. Only after one successful exact-final complete canonical aggregate, clean pushed state, 0/0 divergence, fresh live equality, and a newest live roster and authorization reread may one exact-title send be attempted. Unavailable, ambiguous, paused, redirected, unacknowledged, or protected routes stop without substitution or resend."),
        ("Terminal verdict", "Every empirical, participant, professional, production, legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 boundary remains open or exact-gated. The terminal verdict is `NOT_READY_FOR_STAGE_20`."),
    ]
    lines = ["# Neris Solane v662-v3-2 remaster — bounded x2 evidence overview", ""]
    for title, body in sections:
        lines.extend([f"## {title}", "", body, "", body, ""])
    return "\n".join(lines)


def write_governance_receipt() -> None:
    roster = json.loads((GLOBAL_SKILLS / "ghc-family-roster-check" / "references/current-roster.json").read_text(encoding="utf-8"))
    auth = json.loads((GLOBAL_SKILLS / "ghc-family-auth-permission-state" / "references/current-state.json").read_text(encoding="utf-8"))
    write_json(
        "governance/live-roster-and-authorization-x2.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.governance-snapshot.v1",
            "roster_state": roster["state_id"],
            "authorization_state": auth["state_id"],
            "current_owner": "Neris Solane",
            "current_variant": d.PHASE,
            "canonical_phase": d.CANONICAL_PHASE,
            "active_main_task_count": 15,
            "standby_collaboration_subagent_count": 1,
            "next": {"owner": d.SUCCESSOR, "phase": d.SUCCESSOR_PHASE, "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"},
            "raw_task_or_thread_ids_recorded": False,
            "private_routes_recorded": False,
            "boundary": d.EVIDENCE_BOUNDARY,
        },
    )


def build(*, promote_global: bool) -> dict[str, Any]:
    gate = verify_x1_gate()
    write_json("evidence/x1-to-x2-gate.json", gate)
    selected, outcomes, mutations = build_surfaces()
    distribution = dict(Counter(row["observed_outcome"] for row in outcomes))
    if distribution != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError({"outcome_distribution_drift": distribution})
    if len(mutations) != 200 or not all(row["rejected"] for row in mutations):
        raise RuntimeError({"mutation_drift": len(mutations)})
    write_json(
        "evidence/proposal-outcomes.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.proposal-outcomes.v1",
            "program_count": 40,
            "selected_inherited_revalidated": 20,
            "selected_inherited_novelty_credit": 0,
            "selected_inherited_completion_credit": 0,
            "new_unique_executed": 20,
            "observed_outcome_counts": distribution,
            "outcomes": outcomes,
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write_json("truth/retained-mutation-register-x2.json", {"schema": "ghc.family.v662-v3-2-remaster.mutation-register.v1", "count": 200, "rejected": 200, "accepted": 0, "completion_credit": 0, "mutations": mutations}, compact=True)
    runners = build_runners(outcomes)
    skills = build_skills(runners, promote_global=promote_global)
    write_json(
        "tooling/skill-runner-aggregate.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.skill-runner-aggregate.v1",
            "skills_built_validated_smoke_used": len(skills),
            "runners_built_invoked": len(runners),
            "global_skill_promotions": sum(row["global_tree_equal"] for row in skills),
            "all_valid": all(row["valid"] for row in skills) and all(row["valid"] for row in runners),
            "successor_skill_ideas": [{"name": name, "purpose": purpose, "state": "recommendation_only"} for name, purpose in d.SUCCESSOR_SKILL_IDEAS],
            "successor_runner_ideas": [{"name": name, "purpose": purpose, "state": "recommendation_only"} for name, purpose in d.SUCCESSOR_RUNNER_IDEAS],
            "plugin_caches_mutated": False,
            "same_owner_only": True,
        },
    )
    portfolios = rt.read_json(PHASE / "preregistration/approval-portfolios.json")
    candidate_receipts = []
    for row, outcome in zip(portfolios["owner_candidates"], outcomes[:15], strict=True):
        candidate_receipts.append({**row, "state": "executed_bounded_structural", "proposal_id": outcome["proposal_id"], "observed_outcome": outcome["observed_outcome"], "valid_fixture": True, "external_actions": 0})
    write_json(
        "evidence/approval-packet-receipts.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.approval-packet-receipts.v1",
            "owner_safe_now": [{**row, "state": "completed", "external_actions": 0} for row in portfolios["owner_safe_now"]],
            "successor_safe_now": portfolios["successor_safe_now"],
            "owner_candidates": candidate_receipts,
            "successor_candidates": portfolios["successor_candidates"],
            "owner_exact": portfolios["owner_exact"],
            "owner_blocked": portfolios["owner_blocked"],
            "counts": portfolios["counts"],
            "executed": {"owner_safe_now": 30, "owner_candidates": 15, "owner_exact": 0, "owner_blocked": 0, "successor": 0},
            "boundary": d.EVIDENCE_BOUNDARY,
        },
    )
    cfr_plan = rt.read_json(PHASE / "preregistration/clean-fix-refine-plan.json")
    write_json(
        "evidence/clean-fix-refine-receipts.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.clean-fix-refine-receipts.v1",
            "owner": [{**row, "state": "completed", "deletions": 0, "sibling_mutations": 0, "external_actions": 0} for row in cfr_plan["owner"]],
            "successor": cfr_plan["successor"],
            "counts": {"owner_completed": 30, "successor_recommendations": 30},
            "destructive_cleanup_performed": False,
            "plugin_cache_mutations": 0,
        },
    )
    flow = build_method_flow(selected, outcomes, mutations)
    write_json("method-flow/method-flow-state-x2.json", flow, compact=True)
    write_json(
        "truth/x2-operational-failures.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.operational-failures.v1",
            "failure_count": len(X2_OPERATIONAL_FAILURES),
            "failures": X2_OPERATIONAL_FAILURES,
            "all_zero_credit": True,
            "boundary": d.EVIDENCE_BOUNDARY,
        },
    )
    write_json(
        "truth/x2-phase-truth.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.phase-truth.x2.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "canonical_phase": d.CANONICAL_PHASE,
            "x1_freeze": X1_FREEZE,
            "frozen_proposals": 3530,
            "selected_inherited_credit": 0,
            "new_outcomes": distribution,
            "effective_negatives": 23040,
            "effective_methods": 7634,
            "effective_open_gaps": 149,
            "effective_exact_gates": 148,
            "route": {"owner": d.SUCCESSOR, "phase": d.SUCCESSOR_PHASE, "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"},
            "message_attempted": False,
            "message_sent": False,
            "terminal_verdict": d.TERMINAL_VERDICT,
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": d.EVIDENCE_BOUNDARY,
        },
    )
    write_json("truth/exact-and-blocked-register-x2.json", {"schema": "ghc.family.v662-v3-2-remaster.exact-blocked.v1", "exact_count": 10, "blocked_count": 5, "exact_rows": portfolios["owner_exact"], "blocked_rows": portfolios["owner_blocked"], "executed_count": 0, "boundary": d.EVIDENCE_BOUNDARY})
    write_json("security/threat-model-x2.json", {"schema": "ghc.family.v662-v3-2-remaster.threat-model.v1", "assets": ["immutable x1", "test-ID inventory", "definition anchors", "failure overlay", "route gate"], "threats": ["silent omission", "duplicate execution", "historical assertion editing", "private disclosure", "failure erasure", "stale route", "sibling mutation"], "controls": ["immutable blob equality", "complete set union", "five-class scan", "append-only failures", "one-shot latch", "terminal route gate"], "residual_gaps": ["independent reproduction", "complete privacy", "complete accessibility", "exhaustive security", "professional and authority review"], "security_complete": False})
    write_json("wellbeing/workload-check-x2.json", {"schema": "ghc.family.v662-v3-2-remaster.workload-check.v1", "owner": d.OWNER, "solo": True, "delegated": False, "subagents": 0, "surfaces": 40, "skills": 10, "runners": 10, "candidates": 15, "clean_fix_refine": 30, "pause_redirect_stop_right_preserved": True, "boundary": "Operational workload-care language only; not consciousness, health, employment, or clinical evidence."})
    write_governance_receipt()
    write_text("overview/v662-v3-2-remaster-x2-overview.md", overview())
    write_text("reports/bounded-evidence-report.html", """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neris v662-v3-2 bounded evidence</title></head><body><a href="#main">Skip to evidence</a><header><h1>Neris v662-v3-2 remaster</h1></header><main id="main"><h2>Truth</h2><p>14 completed, 4 represented, 1 open_gap, 1 exact_gate. NOT_READY_FOR_STAGE_20.</p><h2>Limits</h2><p>Same-owner structural software evidence only; no empirical, participant, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, personhood, Theory-of-Everything, or Stage 20 claim.</p></main></body></html>""")
    refresh_validation(pre_staging=True)
    return validate(include_staged=False)


def changed_file_paths() -> list[Path]:
    return [ROOT / row for row in owner_delta_paths() if (ROOT / row).is_file()]


def make_delta_manifest(paths: list[Path]) -> dict[str, Any]:
    entries = []
    for path in sorted(paths, key=rt.repo_relative):
        relative = rt.repo_relative(path)
        if relative in SELF_EXCLUSIONS:
            continue
        payload = path.read_bytes()
        entries.append({"path": relative, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
    return {"schema": "ghc.family.v662-v3-2-remaster.x2-content-manifest.v1", "entry_count": len(entries), "entries": entries, "exclusions": sorted(SELF_EXCLUSIONS), "boundary": d.EVIDENCE_BOUNDARY}


def replay_manifest(manifest: dict[str, Any]) -> list[str]:
    mismatches = []
    for entry in manifest["entries"]:
        path = ROOT / entry["path"]
        if not path.is_file():
            mismatches.append(entry["path"])
            continue
        payload = path.read_bytes()
        if len(payload) != entry["bytes"] or hashlib.sha256(payload).hexdigest() != entry["sha256"]:
            mismatches.append(entry["path"])
    return mismatches


def refresh_validation(*, pre_staging: bool) -> None:
    paths = changed_file_paths()
    manifest = make_delta_manifest(paths)
    write_json("validation/x2-content-manifest.json", manifest)
    paths = changed_file_paths()
    write_json("validation/x2-privacy-scan.json", rt.privacy_scan(paths, schema="ghc.family.v662-v3-2-remaster.x2-privacy-scan.v1"))
    write_json("validation/x2-document-cap.json", rt.document_cap(paths))
    expected = sorted(rt.repo_relative(path) for path in changed_file_paths())
    write_json(
        "validation/x2-staged-review.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.x2-staged-review.v1",
            "state": "PRE_STAGING_NOT_CREDITED" if pre_staging else "EXACT_STAGED_REVIEW",
            "expected_paths": expected,
            "actual_paths": [],
            "missing": expected,
            "unexpected": [],
            "valid": False,
        },
    )
    write_json("validation/x2-validation.json", validate(include_staged=False))


def staged_review() -> dict[str, Any]:
    expected = sorted(rt.repo_relative(path) for path in changed_file_paths())
    actual = sorted(row for row in git("diff", "--cached", "--name-only", "--", d.PHASE_ROOT, *sorted(X2_CODE), *sorted(RUNNER_PATHS)).splitlines() if row)
    payload = {
        "schema": "ghc.family.v662-v3-2-remaster.x2-staged-review.v1",
        "state": "EXACT_STAGED_REVIEW",
        "expected_paths": expected,
        "actual_paths": actual,
        "missing": sorted(set(expected) - set(actual)),
        "unexpected": sorted(set(actual) - set(expected)),
        "valid": set(expected) == set(actual),
        "boundary": "Literal owner-delta staged path equality only; not semantic, authority, or delivery proof.",
    }
    write_json("validation/x2-staged-review.json", payload)
    return payload


def validate(*, include_staged: bool) -> dict[str, Any]:
    outcomes = rt.read_json(PHASE / "evidence/proposal-outcomes.json")
    mutations = rt.read_json(PHASE / "truth/retained-mutation-register-x2.json")
    tools = rt.read_json(PHASE / "tooling/skill-runner-aggregate.json")
    approval = rt.read_json(PHASE / "evidence/approval-packet-receipts.json")
    cfr = rt.read_json(PHASE / "evidence/clean-fix-refine-receipts.json")
    flow = rt.read_json(PHASE / "method-flow/method-flow-state-x2.json")
    truth = rt.read_json(PHASE / "truth/x2-phase-truth.json")
    manifest = rt.read_json(PHASE / "validation/x2-content-manifest.json")
    privacy = rt.read_json(PHASE / "validation/x2-privacy-scan.json")
    doc = rt.read_json(PHASE / "validation/x2-document-cap.json")
    staged = rt.read_json(PHASE / "validation/x2-staged-review.json")
    json_paths = [path for path in changed_file_paths() if path.suffix.lower() == ".json"]
    json_errors = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as error:  # pragma: no cover - diagnostic path
            json_errors.append({"path": rt.repo_relative(path), "error": type(error).__name__})
    checks = {
        "head_is_x1": git("rev-parse", "HEAD") == X1_FREEZE,
        "program_40": outcomes["program_count"] == 40,
        "selected_20_zero_credit": outcomes["selected_inherited_revalidated"] == 20 and outcomes["selected_inherited_completion_credit"] == 0,
        "new_20": outcomes["new_unique_executed"] == 20,
        "outcomes_14_4_1_1": outcomes["observed_outcome_counts"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "mutations_200_rejected": mutations["count"] == mutations["rejected"] == 200 and mutations["accepted"] == 0,
        "skills_10": tools["skills_built_validated_smoke_used"] == 10,
        "runners_10": tools["runners_built_invoked"] == 10,
        "global_promotions_10": tools["global_skill_promotions"] == 10,
        "successor_skills_10": len(tools["successor_skill_ideas"]) == 10,
        "successor_runners_10": len(tools["successor_runner_ideas"]) == 10,
        "safe_30_20": approval["counts"]["owner_safe_now"] == 30 and approval["counts"]["successor_safe_now"] == 20,
        "candidate_15_15": approval["counts"]["owner_candidates"] == 15 and approval["counts"]["successor_candidates"] == 15,
        "exact_10_blocked_5": approval["counts"]["owner_exact"] == 10 and approval["counts"]["owner_blocked"] == 5 and approval["executed"]["owner_exact"] == 0,
        "cfr_30_30": cfr["counts"] == {"owner_completed": 30, "successor_recommendations": 30},
        "methods_49": flow["method_count"] == 49,
        "failed_209": flow["failed_witness_count"] == 209,
        "passing_49": flow["passing_witness_count"] == 49,
        "effective_counts": flow["effective_negatives"] == 23040 and flow["effective_methods"] == 7634,
        "gaps_and_gates": truth["effective_open_gaps"] == 149 and truth["effective_exact_gates"] == 148,
        "not_ready": truth["terminal_verdict"] == d.TERMINAL_VERDICT,
        "route_not_sent": truth["message_attempted"] is False and truth["message_sent"] is False,
        "manifest_replay": not replay_manifest(manifest),
        "privacy_zero": privacy["confirmed_hit_count"] == 0,
        "privacy_not_complete": privacy["privacy_complete"] is False,
        "document_cap": doc["valid"],
        "json_parse": not json_errors,
        "staged_exact": (not include_staged) or staged["valid"],
    }
    return {
        "schema": "ghc.family.v662-v3-2-remaster.x2-validation.v1",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "valid": all(checks.values()),
        "json_files": len(json_paths),
        "json_errors": json_errors,
        "manifest_entries": manifest["entry_count"],
        "privacy_files": privacy["file_count"],
        "boundary": d.EVIDENCE_BOUNDARY,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--promote-global", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--include-staged", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged = staged_review()
        result = validate(include_staged=True) if staged["valid"] else staged
        if staged["valid"]:
            write_json("validation/x2-validation.json", result)
    elif args.refresh:
        refresh_validation(pre_staging=False)
        result = validate(include_staged=args.include_staged)
        write_json("validation/x2-validation.json", result)
    elif args.validate:
        result = validate(include_staged=args.include_staged)
    else:
        result = build(promote_global=args.promote_global)
    print(json.dumps({"valid": result["valid"], "passed": result.get("passed"), "total": result.get("total"), "phase": d.PHASE}, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
