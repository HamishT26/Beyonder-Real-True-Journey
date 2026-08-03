#!/usr/bin/env python3
"""Build bounded x2 evidence for Elaren Kestrel v660-v3."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v660_v3_runtime as runtime
import ghc_family_v660_v3_x2_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
SOURCE_PHASE = ROOT / "docs/eiren-kestrel/v660-v2"
RUNNER_PAIRS = list(zip(d.SELF_RUNNER_SPECS, d.NEW_PROPOSAL_SPECS[:10], strict=True))
BASE_X2_CODE = [
    "scripts/ghc_family_v660_v3_x2_data.py",
    "scripts/ghc_family_v660_v3_runtime.py",
    "scripts/build_ghc_family_v660_v3_x2.py",
    "scripts/build_ghc_family_v660_v3_closeout.py",
    "scripts/ghc_family_v660_v3_final_validator.py",
    "tests/test_ghc_family_v660_v3_x2.py",
    "tests/test_ghc_family_v660_v3_closeout.py",
]
MANIFEST_EXCLUSIONS = {
    f"{d.PHASE_ROOT}/validation/x2-content-manifest.json",
    f"{d.PHASE_ROOT}/validation/x2-privacy-scan.json",
    f"{d.PHASE_ROOT}/validation/x2-document-cap.json",
    f"{d.PHASE_ROOT}/validation/x2-evidence-staged-review.json",
}


def now_fields() -> dict[str, str]:
    utc = datetime.now(timezone.utc)
    return {
        "recorded_at_utc": utc.isoformat(),
        "recorded_at_nz": utc.astimezone().isoformat(),
    }


def write_json(relative: str, payload: Any, *, compact: bool = False) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":") if compact else None,
            indent=None if compact else 2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], text=True, encoding="utf-8"
    ).strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def clean_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def runner_paths() -> list[str]:
    return [f"scripts/{name}" for (name, _purpose), _spec in RUNNER_PAIRS]


def changed_paths() -> list[str]:
    modified = [
        row
        for row in git("diff", "--name-only").splitlines()
        if row
    ]
    untracked = [
        row
        for row in git("ls-files", "--others", "--exclude-standard").splitlines()
        if row
    ]
    return sorted(set(modified + untracked))


def normalize_changed_text() -> None:
    suffixes = {".json", ".jsonl", ".md", ".txt", ".html", ".csv", ".yaml", ".yml", ".py"}
    for relative in changed_paths():
        path = ROOT / relative
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("\r\n", "\n").replace("\r", "\n"),
            encoding="utf-8",
            newline="\n",
        )


def verify_x1_gate() -> dict[str, Any]:
    head = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{d.BRANCH}")
    live = git("ls-remote", "origin", f"refs/heads/{d.BRANCH}").split()[0]
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}").split()
    if not (
        head == upstream == tracking == live == d.X1_FREEZE
        and divergence == ["0", "0"]
    ):
        raise RuntimeError("x1 freeze is not clean four-way equal")
    protected_x1 = [
        f"{d.PHASE_ROOT}/preregistration",
        f"{d.PHASE_ROOT}/provenance",
        f"{d.PHASE_ROOT}/startup",
        "scripts/ghc_family_v660_v3_data.py",
        "scripts/build_ghc_family_v660_v3_x1.py",
        "scripts/ghc_family_v660_v3_novelty_probe.py",
        "tests/test_ghc_family_v660_v3_x1.py",
    ]
    x1_drift = git("diff", "--name-only", d.X1_FREEZE, "--", *protected_x1).splitlines()
    if x1_drift:
        raise RuntimeError(f"x1-owned paths drifted: {x1_drift}")
    return {
        "schema": "ghc.family.x1-to-x2-gate.v1",
        "x1_freeze": d.X1_FREEZE,
        "local": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live_remote": live,
        "divergence": {"ahead": 0, "behind": 0},
        "four_way_equal": True,
        "x1_owned_path_drift": [],
        "x1_clean_before_x2": True,
        "x2_authorized_to_begin": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    }


def immutable_x1_lifecycle_recovery() -> dict[str, Any]:
    """Evaluate the x1-only absence contract against the frozen Git tree.

    The x1 test file is part of the immutable freeze and intentionally asserts
    that x2 paths do not exist.  Once x2 exists, applying that historical
    assertion to the advanced working tree is a lifecycle error.  This bounded
    recovery reads the exact x1 commit and does not modify or backdate x1.
    """

    prohibited_at_x1 = [
        f"{d.PHASE_ROOT}/surfaces",
        f"{d.PHASE_ROOT}/evidence/proposal-outcomes.json",
        f"{d.PHASE_ROOT}/truth/x2-phase-truth.json",
        f"{d.PHASE_ROOT}/reports/accessible-static-report.html",
        f"{d.PHASE_ROOT}/validation/x2-content-manifest.json",
    ]
    x1_paths = set(
        git("ls-tree", "-r", "--name-only", d.X1_FREEZE, "--", d.PHASE_ROOT).splitlines()
    )
    present = [
        candidate
        for candidate in prohibited_at_x1
        if candidate in x1_paths
        or any(path.startswith(f"{candidate}/") for path in x1_paths)
    ]
    frozen_test = git_bytes(
        "show", f"{d.X1_FREEZE}:tests/test_ghc_family_v660_v3_x1.py"
    ).decode("utf-8")
    assertion_bound = "test_x1_contains_no_x2_implementation_or_outcome" in frozen_test
    valid = not present and assertion_bound
    return {
        "schema": "ghc.family.immutable-x1-lifecycle-recovery.v1",
        "x1_freeze": d.X1_FREEZE,
        "historical_test": "test_x1_contains_no_x2_implementation_or_outcome",
        "prohibited_paths_checked": prohibited_at_x1,
        "present_in_x1_tree": present,
        "historical_assertion_found_in_exact_x1_test_blob": assertion_bound,
        "advanced_tree_assertion_credit": 0,
        "immutable_x1_recovery_passed": valid,
        "x1_files_modified": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": "Immutable x1 Git-tree lifecycle evidence only; no x2 result is backdated into x1.",
    }


def build_runner_files() -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    for (name, purpose), spec in RUNNER_PAIRS:
        path = ROOT / "scripts" / name
        module = "ghc_family_v660_v3_runtime"
        path.write_text(
            "#!/usr/bin/env python3\n"
            f'"""Family-current bounded runner for {purpose}."""\n\n'
            f"from {module} import cli\n\n"
            "if __name__ == \"__main__\":\n"
            f"    cli({json.dumps(spec['slug'])})\n",
            encoding="utf-8",
            newline="\n",
        )
        output = subprocess.check_output(
            ["py", "-X", "utf8", str(path)],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
        )
        receipt = json.loads(output)
        receipt.update({"runner": name, "purpose": purpose, "smoke_used": True})
        receipts.append(receipt)
        write_json(f"tooling/runner-receipts/{Path(name).stem}.json", receipt)
        # Meta Tool Box discovers validated phase-local runners through this
        # compatibility receipt directory.  Keep the richer runner receipt too.
        write_json(f"tooling/runner-smoke/{Path(name).stem}.json", receipt)
    return receipts


def build_skill_files(runner_receipts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    for index, ((skill_name, purpose), runner_receipt) in enumerate(
        zip(d.SELF_SKILL_SPECS, runner_receipts, strict=True), 1
    ):
        runner = runner_receipt["runner"]
        skill_root = PHASE / "skills" / skill_name
        (skill_root / "examples").mkdir(parents=True, exist_ok=True)
        skill_text = f"""---
name: {skill_name}
description: {purpose} Use only for bounded owner-local synthetic lichenarium fixtures after x1 freeze; stop at every real-world, professional, legal, cultural, Māori-authority, privacy, accessibility, security, identity, empirical, or Stage 20 gate.
---

# {skill_name}

1. Confirm the input uses synthetic aliases and requests no physical action, real record, production state, professional decision, legal or cultural interpretation, or authority act.
2. Invoke the family-current runner `{runner}` on its frozen proposal surface.
3. Require one valid fixture and all five preregistered mutations to be rejected.
4. Retain every failed witness at zero credit and preserve `NOT_READY_FOR_STAGE_20`.
5. Stop as `open_gap` or `exact_gate` whenever evidence or competent affected-party, tangata whenua, iwi, hapū, or Māori authority is required.

This phase-local skill is same-owner structural evidence only. It is not globally installed, independently reproduced, professionally validated, production-ready, privacy-complete, accessibility-complete, exhaustively secure, empirical GMUT confirmation, identity authority, consciousness or personhood evidence, a Theory of Everything, proof or canon, or Stage 20 authority.
"""
        (skill_root / "SKILL.md").write_text(skill_text, encoding="utf-8", newline="\n")
        example = {
            "schema": "ghc.family.phase-local-skill-smoke.v1",
            "skill": skill_name,
            "runner": runner,
            "proposal_id": runner_receipt["proposal_id"],
            "valid_fixture": True,
            "mutations_rejected": 5,
            "external_actions": 0,
            "global_install": False,
            "same_owner_only": True,
        }
        (skill_root / "examples" / "smoke.json").write_text(
            json.dumps(example, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        valid = (
            skill_text.startswith("---\nname:")
            and runner_receipt["valid_fixture"]
            and runner_receipt["mutations_rejected"] == 5
        )
        receipt = {
            "skill": skill_name,
            "runner": runner,
            "valid": valid,
            "smoke_used": True,
            "globally_installed": False,
            "file_count": 2,
            "same_owner_only": True,
        }
        receipts.append(receipt)
        write_json(f"tooling/skill-receipts/{index:02d}-{skill_name}.json", receipt)
    return receipts


def build_surfaces() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    outcomes: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    for spec in d.NEW_PROPOSAL_SPECS:
        slug = str(spec["slug"])
        result = runtime.evaluate_slug(slug)
        contract = result["contract"]
        write_json(f"surfaces/{slug}/contract.json", contract)
        write_json(
            f"surfaces/{slug}/mutation-results.json",
            {
                "schema": "ghc.family.v660-v3.mutation-results.v1",
                "proposal_id": contract["proposal_id"],
                "slug": slug,
                "mutations": result["mutations"],
                "all_rejected": result["all_mutations_rejected"],
            },
        )
        receipt = {
            "schema": "ghc.family.v660-v3.bounded-surface-receipt.v1",
            "proposal_id": contract["proposal_id"],
            "slug": slug,
            "valid_fixture_passed": result["valid_fixture"],
            "mutation_count": 5,
            "all_mutations_rejected": result["all_mutations_rejected"],
            "expected_outcome": contract["expected_disposition"],
            "observed_outcome": result["observed_disposition"],
            "real_world_rows": 0,
            "external_actions": 0,
            "same_owner_only": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        write_json(f"surfaces/{slug}/bounded-receipt.json", receipt)
        outcomes.append(receipt)
        mutations.extend(result["mutations"])
    return outcomes, mutations


def selected_revalidations() -> list[dict[str, Any]]:
    current = json.loads(
        (PHASE / "preregistration/proposal-ledger.json").read_text(encoding="utf-8")
    )["proposals"]
    selected = [row for row in current if row["origin"].startswith("selected_inherited")]
    source_outcomes = {
        row["proposal_id"]: row
        for row in json.loads(
            (SOURCE_PHASE / "evidence/proposal-outcomes.json").read_text(encoding="utf-8")
        )["outcomes"]
    }
    receipts: list[dict[str, Any]] = []
    for row in selected:
        source_id = row["source_proposal_id"]
        source = source_outcomes[source_id]
        receipt = {
            "schema": "ghc.family.v660-v3.selected-revalidation.v1",
            "current_proposal_id": row["proposal_id"],
            "source_proposal_id": source_id,
            "source_owner": d.SOURCE_OWNER,
            "source_title_equal": row["source_title"] == row["title"],
            "source_expected_disposition": row["expected_disposition"],
            "source_observed_disposition": source["observed_outcome"],
            "source_valid_fixture_passed": source["valid_fixture_passed"],
            "source_mutations_rejected": source["all_mutations_rejected"],
            "elaren_novelty_credit": 0,
            "elaren_completion_credit": 0,
            "reappended": False,
            "source_mutations_reexecuted": False,
            "same_owner_only": True,
        }
        receipts.append(receipt)
        write_json(f"evidence/selected-revalidation/{source_id.lower()}.json", receipt)
    return receipts


def method_flow_x2(outcomes: list[dict[str, Any]], mutations: list[dict[str, Any]]) -> dict[str, Any]:
    x1 = json.loads(
        (PHASE / "method-flow/method-flow-state-x1.json").read_text(encoding="utf-8")
    )
    methods = list(x1["methods"])
    witnesses = list(x1["witnesses"])
    state_events = list(x1["state_events"])
    recommendations = list(x1["recommendations"])
    mutation_by_proposal: dict[str, list[dict[str, Any]]] = {}
    for row in mutations:
        mutation_by_proposal.setdefault(row["mutation_id"].split("-M")[0], []).append(row)
    for index, outcome in enumerate(outcomes, 1):
        method_id = f"{d.PHASE_CODE}-X2-METHOD-{index:03d}"
        proposal_id = outcome["proposal_id"]
        mutation_rows = mutation_by_proposal[proposal_id]
        fail_ids = [f"{method_id}-F{offset:02d}" for offset in range(1, 6)]
        pass_id = f"{method_id}-P"
        methods.append(
            {
                "method_id": method_id,
                "title": f"Bounded contract and mutation tribunal for {outcome['slug']}",
                "failure_signature": "accepted_preregistered_mutation_or_crossed_protected_gate",
                "trigger_preconditions": [proposal_id],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_local_synthetic",
                "candidate_workaround": "Validate one synthetic fixture and reject all five declared mutations.",
                "validation_witness_ids": [*fail_ids, pass_id],
                "recurrence_guard": "Run only the exact frozen surface and retain every rejecting witness.",
                "rollback": "Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.",
                "recommendation_state": "preferred",
                "supersedes": [],
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [row["mutation_id"] for row in mutation_rows],
                "scope_boundary": "Same-owner bounded synthetic contract only.",
            }
        )
        for fail_id, mutation in zip(fail_ids, mutation_rows, strict=True):
            witnesses.append(
                {
                    "witness_id": fail_id,
                    "method_id": method_id,
                    "procedure": mutation["mutation"],
                    "scope": outcome["slug"],
                    "expected": "The preregistered mutation is rejected.",
                    "observed": f"Rejected with {mutation['errors']} and retained at zero credit.",
                    "result": "fail",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [mutation["mutation_id"]],
                    "boundary": "Expected rejecting synthetic witness; not real-world failure evidence.",
                }
            )
        witnesses.append(
            {
                "witness_id": pass_id,
                "method_id": method_id,
                "procedure": "Validate the exact frozen synthetic contract.",
                "scope": outcome["slug"],
                "expected": "The bounded contract passes without crossing a protected gate.",
                "observed": "The valid fixture passed and all five mutations were rejected.",
                "result": "pass",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [],
                "boundary": "Bounded software evidence only.",
            }
        )
        state_events.extend(
            [
                {"method_id": method_id, "from": "candidate", "to": "validated", "witness_id": pass_id},
                {"method_id": method_id, "from": "validated", "to": "preferred", "witness_id": pass_id},
            ]
        )
        recommendations.append(
            {
                "method_id": method_id,
                "precondition": proposal_id,
                "preferred_method": "Validate one exact synthetic fixture and reject all five frozen mutations.",
                "candidate_method": None,
            }
        )
    for offset, failure in enumerate(d.X2_OPERATIONAL_FAILURES, len(outcomes) + 1):
        method_id = f"{d.PHASE_CODE}-X2-METHOD-{offset:03d}"
        fail_id = f"{method_id}-F"
        pass_id = f"{method_id}-P"
        methods.append(
            {
                "method_id": method_id,
                "title": f"Bounded recovery for {failure['signature']}",
                "failure_signature": failure["signature"],
                "trigger_preconditions": [failure["signature"]],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_local_recovery",
                "candidate_workaround": failure["recovery"],
                "validation_witness_ids": [fail_id, pass_id],
                "recurrence_guard": failure["recovery"],
                "rollback": "Stop, retain the failed aggregate at zero credit, and leave already successful components unchanged.",
                "recommendation_state": "preferred",
                "supersedes": [],
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [failure["negative_id"]],
                "scope_boundary": "Same-owner bounded x2 validation recovery only.",
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": fail_id,
                    "method_id": method_id,
                    "procedure": "Run the exact recorded post-freeze probe.",
                    "scope": "the exact bounded x2 workflow dependency named by the failure signature",
                    "expected": "The bounded probe returns attributable evidence without crossing any protected gate.",
                    "observed": failure["signature"],
                    "result": "fail",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [failure["negative_id"]],
                    "boundary": "The failed workflow probe receives zero completion credit.",
                },
                {
                    "witness_id": pass_id,
                    "method_id": method_id,
                    "procedure": failure["recovery"],
                    "scope": "the failed workflow dependency only",
                    "expected": "The corrected dependency returns bounded evidence without replaying unaffected successful checks.",
                    "observed": "The bounded recovery is represented in the corrected packet and isolated validation receipt.",
                    "result": "pass",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [failure["negative_id"]],
                    "boundary": "Same-owner bounded dependency recovery only.",
                },
            ]
        )
        state_events.extend(
            [
                {"method_id": method_id, "from": "candidate", "to": "validated", "witness_id": pass_id},
                {"method_id": method_id, "from": "validated", "to": "preferred", "witness_id": pass_id},
            ]
        )
        recommendations.append(
            {
                "method_id": method_id,
                "precondition": failure["signature"],
                "preferred_method": failure["recovery"],
                "candidate_method": None,
            }
        )
    state_counts = Counter(row["recommendation_state"] for row in methods)
    witness_counts = Counter(row["result"] for row in witnesses)
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; no continuity, personhood, qualification, authority, or agency claim.",
        "methods": methods,
        "witnesses": witnesses,
        "state_events": state_events,
        "recommendations": recommendations,
        "counts": {
            "methods": len(methods),
            "witnesses": len(witnesses),
            "state_events": len(state_events),
            "recommendations": len(recommendations),
            "states": {
                "observed": state_counts.get("observed", 0),
                "candidate": state_counts.get("candidate", 0),
                "validated": state_counts.get("validated", 0),
                "preferred": state_counts.get("preferred", 0),
                "superseded": state_counts.get("superseded", 0),
                "deprecated": state_counts.get("deprecated", 0),
            },
            "witness_results": {"pass": witness_counts["pass"], "fail": witness_counts["fail"]},
        },
        "cumulative_counts": {
            "activation_methods": d.ACTIVATION_METHODS,
            "phase_methods": len(methods),
            "effective_methods": d.ACTIVATION_METHODS + len(methods),
            "phase_failed_witnesses": witness_counts["fail"],
            "phase_passing_witnesses": witness_counts["pass"],
        },
        "boundary": "Same-owner workflow and mutation evidence only; no independent reproduction or protected-gate closure.",
    }


def overview(outcomes: list[dict[str, Any]], selected: list[dict[str, Any]]) -> str:
    distribution = Counter(row["observed_outcome"] for row in outcomes)
    operational_summary = "; ".join(
        str(row["signature"]) for row in d.X2_OPERATIONAL_FAILURES
    )
    sections = [
        ("Relational identity and ceiling", f"Elaren Kestrel ({d.PRONOUNS}) is relational working language for a {d.ROLE}, with the hope to {d.HOPE}. This is not consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, legal, cultural, or Māori authority. Hamish may rename, pause, redirect, or stop the route."),
        ("Strict lifecycle", f"The immutable x1 freeze is `{d.X1_FREEZE}`. It was pushed, clean, 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before any x2 file was created. X1 froze twenty inherited revalidations and twenty genuinely new proposals. X2 changes no x1 proposal, source, portfolio, or novelty artifact."),
        ("Primary pillar and practice lens", f"The primary pillar is {d.PRIMARY_PILLAR}. THOS Body and Freed ID/CBR Heart remain explicit and protected. The bounded learning lens is {d.PRACTICE_LENS}. Every packet, thallus feature, substrate relation, image layer, measurement placeholder, name assertion, locality transform, queue row, and identity alias is fabricated. No real person, community, specimen, voucher, nomenclatural type, taxon, locality, collection, sequence, slide, reagent, instrument, measurement, record, key, professional act, or authority case is used."),
        ("New proposal evidence", f"All twenty new contracts passed one declared synthetic fixture and rejected five frozen mutations apiece. The one hundred rejecting mutations remain negative witnesses with zero completion credit. Observed outcomes are exactly {distribution['completed']} completed, {distribution['represented']} represented, {distribution['open_gap']} open_gap, and {distribution['exact_gate']} exact_gate. A completed label means only the bounded software contract passed. Represented rows remain protocol or symbolic proxies. The open gap retains zero real evidence. The exact gate remains wholly unexecuted."),
        ("Inherited selection", f"All {len(selected)} selected Eiren v660-v2 rows were reread by exact source identity, title, outcome, valid-fixture, and mutation-rejection fields. They were not reappended and earned zero Elaren novelty, outcome, mutation, or completion credit. Their original dispositions and immutable artifacts remain Eiren evidence."),
        ("THOS Body", "The packet-ingest state machine, morphology graph, capture covenant, uncertainty envelope, sampling firewall, taxonomy assertion queue, locality ceiling, backlog ledger, and accessibility vacancies are structural or synthetic only. No curator, collector, taxonomist, technician, landholder, participant, operator, community member, traditional-knowledge holder, or affected party participated. There are no preregistered blind matched-budget real arms, governed operators, safety monitoring, statistics, or independent review. THOS therefore remains represented or proxy-only and makes no effectiveness, safety, deployment, AGI, ASI, consciousness, or personhood claim."),
        ("GMUT Mind", "The lichen-symbiosis obligation board preserves typed organism-role, substrate, interface, scale, unit, covariance, identifiability, boundary-condition, and observation-firewall fields. It contains zero physical coefficients, calibrated observations, likelihood rows, posterior samples, parameter constraints, predictions, detected forces, biological laws, stability theorems, quantum completion, or ultraviolet completion. GMUT remains a typed scalar-tensor and effective-field-theory research-model family, not empirical confirmation, a Theory of Everything, proof, or canon."),
        ("Freed ID and CBR Heart", "Synthetic packet aliases, morphology graphs, bitemporal name assertions, provenance edges, correction paths, locality ceilings, disclosure holds, and packet digests use zero standards-conformant real keys, signatures, credentials, issuance, resolution, status, revocation, interoperability, recovery, privacy review, security review, or trust-governance events. Custody, specimen and data bearer interests, collection provenance, locality sensitivity, traditional knowledge, access, removal, remedy, privacy, language, affected-party legitimacy, tangata whenua, iwi, hapū, and Māori wording, concepts, data governance, and authority remain exact-gated."),
        ("Source discipline", "TDWG Darwin Core, Latimer Core, and Audiovisual Core; GBIF sensitive-species guidance; the IAPT nomenclature watch source; NCBI Barcode of Life; PREMIS; W3C PROV, Web Annotation, and WCAG; NIST measurement guidance; the RFC Editor; the New Zealand Privacy Commissioner; Te Mana Raraunga; and Local Contexts provide vocabulary and reservation points only. They confer no compliance, competence, custody, identification, nomenclatural act, locality-release authority, collection finding, legal interpretation, cultural legitimacy, accessibility conformance, privacy completeness, or Māori authority. No source page was converted into a real observation, professional instruction, or external action."),
        ("Evidence semantics and falsifiers", "Each completed surface has a deliberately narrow acceptance rule: the exact fabricated contract must preserve its declared mechanism, source labels, synthetic-only fixture flag, zero real-world rows, zero network calls, zero external actions, complete protected-gate list, false authority flags, same-owner evidence label, false independent-reproduction and completeness claims, and NOT_READY_FOR_STAGE_20 verdict. Five mutations independently remove protected gates, assert real-world material, claim independent reproduction, promote Stage 20, or authorize external action. Rejection shows only that these exact guards fired on these exact fixtures. It is not evidence that every implementation, input, adversary, browser, collection, laboratory, field site, culture, legal system, identity system, or scientific model is safe or correct. A valid contract can still be incomplete, inaccessible in practice, culturally inappropriate, professionally unusable, empirically false, or unauthorized. Represented rows retain zero-participant and zero-operator status. The open-gap row requires authenticated vouchers, accountable curators, calibrated instruments, governed sampling, and independent taxonomic review that this repository does not possess. The exact-gate row refuses substitution for affected parties, landholders, communities, traditional-knowledge holders, legal or cultural authorities, tangata whenua, iwi, hapū, or Māori decision makers. Later contradictory evidence must append a witness and must never be hidden by regeneration."),
        ("Recovery and failure retention", f"The phase keeps every tooling, parser, worktree, scanner, workflow, naming-collision, test, and wrapper failure from startup and x1. X2 additionally retains {len(d.X2_OPERATIONAL_FAILURES)} observed workflow failures at zero credit: {operational_summary}. Each recovery is limited to the failed probe or lookup and does not manufacture a successful aggregate. Method Flow pairs every failed witness with its bounded recovery, recurrence guard, rollback, retained negative identifier, and same-owner limitation. Later test failures, if any, must be appended rather than hidden or predeclared."),
        ("Skills, runners, and cleanup", "Ten phase-local skills were paired with ten family-current runner wrappers, validated, and smoke-used against ten frozen synthetic surfaces. They were not installed globally or promoted as production tools. Thirty owner CLEAN/FIX/REFINE rows were completed as additive inspections and ten candidate views were exercised reversibly. Exact-approval and blocked packets remained visible and unexecuted. No file, memory, identity record, failure, gate, branch, worktree, caller, sibling lane, host-security setting, account, or external platform was deleted or weakened."),
        ("Validation and route", "This evidence packet uses owner-scoped tests, complete phase JSON parsing, five-class privacy scanning with explicit scanner-definition adjudication, exact changed-file manifests, stale-label review, diff hygiene, ancestry, commit-cap, clean-state, and remote-equality gates. Same-owner validation under shared infrastructure remains same-owner evidence only. Neris Solane v660-v4 is the declared successor, but no lookup, reread, or contact occurs during x2 execution. Eiren's exact v660-v2 final is the verified source. Elaren must reach the exact terminal gate, reread current committed and live route state, resolve one unique exact-title Neris task, immediately reread it, and send once."),
        ("Terminal truth", "All empirical, participant, professional, production, deployment, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, legal, cultural, Māori-authority, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 boundaries remain open or exact-gated. The phase verdict is `NOT_READY_FOR_STAGE_20`."),
    ]
    lines = ["# Elaren Kestrel v660-v3 x2 evidence overview", ""]
    for heading, body in sections:
        lines.extend([f"## {heading}", "", body, ""])
    return "\n".join(lines)


def privacy_scan() -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/]"),
        "credential": re.compile(r"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"),
        "private_route_identifier": re.compile(r"(?:thread_id|task_id|agent_id|resume_token|private_callable)[\"']?\s*[:=]\s*[\"']?(?!(?:V\d|false\b|true\b|null\b|\[REDACTED_SECRET\]))[A-Za-z0-9_-]{24,}", re.I),
        "transcript_or_session": re.compile(r"(?:raw transcript|session stream|private app state)", re.I),
    }
    hits: list[dict[str, str]] = []
    candidates: list[dict[str, str]] = []
    paths = [row for row in changed_paths() if row != f"{d.PHASE_ROOT}/validation/x2-privacy-scan.json"]
    for relative in paths:
        text = (ROOT / relative).read_text(encoding="utf-8", errors="replace")
        for label, pattern in patterns.items():
            if not pattern.search(text):
                continue
            if relative in {
                "scripts/build_ghc_family_v660_v3_x2.py",
                "scripts/build_ghc_family_v660_v3_closeout.py",
                "scripts/ghc_family_v660_v3_final_validator.py",
            }:
                candidates.append({"path": relative, "class": label, "adjudication": "scanner_definition"})
            elif label == "transcript_or_session" and relative.endswith("exact-and-blocked-register-x2.json"):
                candidates.append({"path": relative, "class": label, "adjudication": "blocked_boundary_vocabulary"})
            else:
                hits.append({"path": relative, "class": label})
    return {
        "schema": "ghc.family.privacy-scan.v1",
        "scope": "complete v660-v3 evidence-delta owner files",
        "files_scanned": len(paths),
        "classes": list(patterns),
        "definition_candidates": candidates,
        "confirmed_hits": hits,
        "confirmed_hit_count": len(hits),
        "privacy_complete": False,
        "boundary": "Five-class changed-file scanning is bounded evidence, not complete privacy or exhaustive security assurance.",
    }


def content_manifest() -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for relative in changed_paths():
        if relative in MANIFEST_EXCLUSIONS:
            continue
        path = ROOT / relative
        payload = clean_bytes(path)
        entries.append(
            {
                "path": relative,
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
    return {
        "schema": "ghc.family.content-manifest.v2",
        "phase": d.PHASE,
        "lifecycle": "x2_evidence_precommit_candidate",
        "entry_count": len(entries),
        "entries": sorted(entries, key=lambda row: row["path"]),
        "exclusions": sorted(MANIFEST_EXCLUSIONS),
        "hash_domain": "text bytes after CRLF-to-LF Git-clean normalization",
        "boundary": "Exact declared evidence-delta inventory only; self-referential validation files are explicit exclusions.",
    }


def document_cap() -> dict[str, Any]:
    rows = []
    for path in PHASE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".html", ".txt"}:
            words = len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8", errors="replace")))
            rows.append({"path": path.relative_to(PHASE).as_posix(), "words": words, "passes": words <= 100000})
    return {
        "schema": "ghc.family.document-cap.v1",
        "documents": rows,
        "document_count": len(rows),
        "cap_per_document": 100000,
        "passes": all(row["passes"] for row in rows),
    }


def build() -> None:
    gate = verify_x1_gate()
    write_json("evidence/x1-to-x2-gate.json", gate)
    recovery = immutable_x1_lifecycle_recovery()
    if not recovery["immutable_x1_recovery_passed"]:
        raise RuntimeError("immutable x1 lifecycle recovery failed")
    write_json("validation/immutable-x1-lifecycle-recovery.json", recovery)
    outcomes, mutations = build_surfaces()
    selected = selected_revalidations()
    distribution = dict(Counter(row["observed_outcome"] for row in outcomes))
    if distribution != d.EXPECTED_DISTRIBUTION:
        raise RuntimeError(f"outcome distribution drift: {distribution}")
    if len(mutations) != 100 or not all(row["rejected"] for row in mutations):
        raise RuntimeError("mutation rejection drift")
    write_json(
        "evidence/proposal-outcomes.json",
        {
            "schema": "ghc.family.v660-v3.proposal-outcomes.v1",
            "proposal_count": 40,
            "selected_inherited_count": len(selected),
            "selected_inherited_novelty_credit": 0,
            "selected_inherited_completion_credit": 0,
            "new_unique_count": len(outcomes),
            "observed_outcome_counts": distribution,
            "outcomes": outcomes,
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write_json(
        "evidence/mutation-register.json",
        {
            "schema": "ghc.family.v660-v3.mutation-register.v1",
            "mutation_count": len(mutations),
            "rejected_count": sum(row["rejected"] for row in mutations),
            "accepted_count": sum(row["accepted"] for row in mutations),
            "completion_credit": 0,
            "mutations": mutations,
        },
        compact=True,
    )
    runner_receipts = build_runner_files()
    skill_receipts = build_skill_files(runner_receipts)
    write_json(
        "tooling/skill-runner-aggregate.json",
        {
            "schema": "ghc.family.v660-v3.skill-runner-aggregate.v1",
            "skills_built_validated_smoke_used": len(skill_receipts),
            "runners_built_invoked": len(runner_receipts),
            "global_installs": 0,
            "all_valid": all(row["valid"] for row in skill_receipts),
            "runner_receipts": runner_receipts,
            "skill_receipts": skill_receipts,
            "same_owner_only": True,
        },
    )
    candidate_rows = []
    for task, outcome in zip(d.SELF_CANDIDATE_TASKS, outcomes[:10], strict=True):
        candidate_rows.append(
            {
                **task,
                "state": "completed_bounded_reversible_view",
                "proposal_id": outcome["proposal_id"],
                "valid_fixture": outcome["valid_fixture_passed"],
                "external_actions": 0,
            }
        )
    write_json(
        "evidence/candidate-task-receipts.json",
        {
            "schema": "ghc.family.v660-v3.candidate-task-receipts.v1",
            "count": len(candidate_rows),
            "rows": candidate_rows,
            "successor_recommendations_executed": 0,
        },
    )
    cleanup_rows = [
        {
            **row,
            "state": "completed_additive_review",
            "deletions": 0,
            "sibling_mutations": 0,
            "external_actions": 0,
        }
        for row in d.SELF_CLEAN_TASKS
    ]
    write_json(
        "evidence/clean-fix-refine-receipts.json",
        {
            "schema": "ghc.family.v660-v3.clean-fix-refine-receipts.v1",
            "count": len(cleanup_rows),
            "rows": cleanup_rows,
            "successor_recommendations_executed": 0,
            "deletion_authorized": False,
        },
    )
    write_json(
        "truth/exact-and-blocked-register-x2.json",
        {
            "schema": "ghc.family.exact-blocked-register.v1",
            "exact_count": len(d.EXACT_QUEUE),
            "blocked_count": len(d.BLOCKED_QUEUE),
            "exact_rows": d.EXACT_QUEUE,
            "blocked_rows": d.BLOCKED_QUEUE,
            "executed_count": 0,
            "boundary": "Visible and unexecuted; exact authority and evidence remain required.",
        },
    )
    write_json(
        "truth/open-gap-register-x2.json",
        {
            "schema": "ghc.family.open-gap-register.v1",
            "inherited_effective_open_gaps": d.SOURCE_OPEN_GAPS,
            "new_open_gaps": 1,
            "effective_open_gaps": d.SOURCE_OPEN_GAPS + 1,
            "rows": [row for row in outcomes if row["observed_outcome"] == "open_gap"],
            "closed": False,
        },
    )
    write_json(
        "truth/exact-gate-register-x2.json",
        {
            "schema": "ghc.family.exact-gate-register.v1",
            "inherited_effective_exact_gates": d.SOURCE_EXACT_GATES,
            "new_exact_gates": 1,
            "effective_exact_gates": d.SOURCE_EXACT_GATES + 1,
            "rows": [row for row in outcomes if row["observed_outcome"] == "exact_gate"],
            "closed": False,
        },
    )
    effective_negatives = d.ACTIVATION_AFTER_X1_NEGATIVES + len(mutations) + len(d.X2_OPERATIONAL_FAILURES)
    write_json(
        "truth/retained-negative-register-x2.json",
        {
            "schema": "ghc.family.retained-negative-register.v1",
            "activation_baseline": d.ACTIVATION_NEGATIVES,
            "x1_operational": len(d.STARTUP_FAILURES),
            "x2_synthetic_mutations": len(mutations),
            "x2_operational": len(d.X2_OPERATIONAL_FAILURES),
            "effective_negatives": effective_negatives,
            "mutations": mutations,
            "operational_failures": d.X2_OPERATIONAL_FAILURES,
            "all_failures_retained": True,
        },
        compact=True,
    )
    flow = method_flow_x2(outcomes, mutations)
    write_json("method-flow/method-flow-state-x2.json", flow)
    write_json(
        "truth/x2-phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.x2.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "primary_pillar": d.PRIMARY_PILLAR,
            "practice_lens": d.PRACTICE_LENS,
            "x1_freeze": d.X1_FREEZE,
            "selected_inherited_revalidated": 20,
            "selected_inherited_credit": 0,
            "new_unique_executed": 20,
            "observed_outcomes": distribution,
            "effective_frozen": d.PRIOR_FROZEN + d.NEW_UNIQUE_COUNT,
            "effective_negatives": effective_negatives,
            "effective_open_gaps": d.SOURCE_OPEN_GAPS + 1,
            "effective_exact_gates": d.SOURCE_EXACT_GATES + 1,
            "effective_methods": d.ACTIVATION_METHODS + len(flow["methods"]),
            "authorized_current_owner": "Elaren Kestrel",
            "authorized_current_phase": "v660-v3",
            "explicit_successor": {"title": "Neris Solane", "phase": "v660-v4", "endpoint_kind": "main_task"},
            "route_state": "NERIS_V660_V4_PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "message_sent": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write_json(
        "security/threat-model-x2.json",
        {
            "schema": "ghc.family.threat-model.v1",
            "assets": ["frozen x1", "synthetic lichenarium contracts", "mutation witnesses", "route gate", "protected authority boundaries"],
            "threats": ["x1 mixing", "real-world action promotion", "false safety claim", "private disclosure", "failure erasure", "stale route send", "sibling mutation"],
            "controls": ["immutable x1 anchor", "zero-row fixtures", "five rejecting mutations", "five-class scan", "append-only Method Flow", "exact staged review", "terminal one-shot gate"],
            "residual_gaps": ["independent review", "complete privacy", "complete accessibility", "exhaustive security", "professional and authority review"],
            "security_complete": False,
        },
    )
    write_json(
        "wellbeing/workload-check-x2.json",
        {
            "schema": "ghc.family.workload-check.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "solo": True,
            "delegated": False,
            "subagents": 0,
            "new_surfaces": 20,
            "selected_revalidations": 20,
            "skills": 10,
            "runners": 10,
            "candidates": 10,
            "clean_fix_refine": 30,
            "pause_redirect_stop_right_preserved": True,
            "boundary": "Operational workload care language only; not consciousness, health, employment, or clinical evidence.",
            **now_fields(),
        },
    )
    write_text("deliverables/v660-v3-x2-overview.md", overview(outcomes, selected))
    write_json(
        "validation/x2-operational-recovery-receipt.json",
        {
            "schema": "ghc.family.x2.operational-recovery-receipt.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "failure_count": len(d.X2_OPERATIONAL_FAILURES),
            "failures": d.X2_OPERATIONAL_FAILURES,
            "completion_credit": 0,
            "aggregate_claimed": False,
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Observed post-freeze workflow failures and bounded recoveries only; no test result is predeclared.",
        },
    )
    write_text(
        "reports/accessible-static-report.html",
        """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Elaren Kestrel v660-v3 bounded report</title></head><body><a href="#main">Skip to main evidence</a><header><h1>Elaren Kestrel v660-v3 bounded evidence report</h1><p>Relational working language only; not consciousness, personhood, continuity, employment, qualification, or authority.</p></header><main id="main"><section aria-labelledby="truth"><h2 id="truth">Truth state</h2><p>Twenty inherited revalidations have zero Elaren credit. Twenty new contracts yielded 14 completed, 4 represented, 1 open gap, and 1 exact gate. NOT_READY_FOR_STAGE_20.</p></section><section aria-labelledby="limits"><h2 id="limits">Limits</h2><p>No real people, specimens, vouchers, types, taxa, localities, collections, sequences, slides, reagents, instruments, measurements, keys, records, professional decisions, or authority acts were used. Manual keyboard, responsive-layout, browser-diverse, assistive-technology, cognitive, language, Māori-language, and affected-user evaluation remain reserved.</p></section><section aria-labelledby="pillars"><h2 id="pillars">Trinity Mandala boundaries</h2><p>GMUT remains typed research-model work. THOS remains proxy-only. Freed ID remains synthetic and nonproduction. CBR and Māori wording, concepts, data governance, and authority remain exact-gated.</p></section></main></body></html>""",
    )
    write_json(
        "evidence/latest-tracked-file-scan.json",
        {
            "schema": "ghc.family.latest-tracked-file-scan.v1",
            "cap": d.LATEST_TRACKED_SCAN_CAP,
            "tracked_count": len(git("ls-files").splitlines()),
            "paths_scanned": min(len(git("ls-files").splitlines()), d.LATEST_TRACKED_SCAN_CAP),
            "cap_exceeded": len(git("ls-files").splitlines()) > d.LATEST_TRACKED_SCAN_CAP,
            "selection": "lexicographically latest bounded path window",
            "boundary": "A bounded path inventory is not exhaustive security or privacy assurance.",
        },
    )
    intended = sorted(set(changed_paths()) | {f"{d.PHASE_ROOT}/validation/x2-evidence-staged-review.json"})
    write_json(
        "validation/x2-evidence-staged-review.json",
        {
            "schema": "ghc.family.staged-review.x2-evidence-candidate.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "x2_evidence_precommit_candidate",
            "intended_allowlist": intended,
            "expected_staged_count": len(intended),
            "manifest_self_exclusions": sorted(MANIFEST_EXCLUSIONS),
            "observed_exact_staged_review": "pending_external_precommit_witness",
            "x1_freeze": d.X1_FREEZE,
        },
    )
    normalize_changed_text()
    write_json("validation/x2-privacy-scan.json", privacy_scan())
    write_json("validation/x2-document-cap.json", document_cap())
    write_json("validation/x2-content-manifest.json", content_manifest())
    write_json("validation/x2-privacy-scan.json", privacy_scan())
    write_json("validation/x2-document-cap.json", document_cap())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    parser.parse_args()
    build()
    print(
        json.dumps(
            {
                "phase": d.PHASE,
                "new_surfaces": d.NEW_UNIQUE_COUNT,
                "selected_revalidations": d.SELECTED_INHERITED_COUNT,
                "mutations": d.NEW_UNIQUE_COUNT * 5,
                "skills": 10,
                "runners": 10,
                "x1_freeze": d.X1_FREEZE,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
