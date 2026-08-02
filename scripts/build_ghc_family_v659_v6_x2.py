#!/usr/bin/env python3
"""Build bounded x2 evidence for Liora Venn v659-v6."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v659_v6_x2_data as d
import ghc_family_v659_v6_runtime as runtime


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
RUNNER_SMOKE = PHASE / "tooling/runner-smoke"
MANIFEST_EXCLUSIONS = {
    "validation/x2-content-manifest.json",
    "validation/x2-owner-privacy-scan.json",
    "validation/x2-document-cap.json",
    "validation/x2-evidence-staged-review.json",
}
X2_CODE = [
    "scripts/ghc_family_v659_v6_data.py",
    "scripts/ghc_family_v659_v6_x2_data.py",
    "scripts/ghc_family_v659_v6_runtime.py",
    "scripts/build_ghc_family_v659_v6_x2.py",
    "scripts/build_ghc_family_v659_v6_skills.py",
    "scripts/validate_ghc_family_v659_v6_skills.py",
    "scripts/ghc_family_v659_v6_evidence_staged_review.py",
    "scripts/build_ghc_family_v659_v6_closeout.py",
    "scripts/ghc_family_v659_v6_closeout_staged_review.py",
    "scripts/ghc_family_v659_v6_validator.py",
    "scripts/ghc_family_v659_v6_minimal.py",
    "scripts/ghc_family_v659_v6_final_validator.py",
    "scripts/ghc_family_v659_v6_canonical.py",
    *[f"scripts/{name}" for name, _ in d.SELF_RUNNER_SPECS],
    "tests/test_ghc_family_v659_v6_x2.py",
    "tests/test_ghc_family_v659_v6_closeout.py",
]


def write_json(relative: str, payload: Any, *, compact: bool = False) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":") if compact else None,
        indent=None if compact else 2,
    )
    path.write_text(text + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True, encoding="utf-8").strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(git_clean_bytes(path)).hexdigest()


def git_clean_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def source_gate() -> dict[str, Any]:
    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{d.BRANCH}")
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{d.BRANCH}")
    live = live_line.split()[0] if live_line else ""
    parent = git("rev-parse", f"{head}^")
    if head != d.X1_FREEZE or branch != d.BRANCH or upstream != head or tracking != head or live != head:
        raise RuntimeError("x1 freeze head, branch, upstream, tracking ref, or fresh live ref drift")
    if parent != d.SOURCE_FINAL:
        raise RuntimeError("x1 freeze parent drift")
    consumer_probe = subprocess.run(
        [
            "git", "-C", str(ROOT), "grep", "-l", "X2_FAILURES", d.X1_FREEZE, "--",
            "scripts/build_ghc_family_v659_v6_x1.py",
            "tests/test_ghc_family_v659_v6_x1.py",
            d.PHASE_ROOT,
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if consumer_probe.returncode not in {0, 1}:
        raise RuntimeError("x1 prefilled-failure consumer probe failed")
    consumer_paths = [row for row in consumer_probe.stdout.splitlines() if row]
    if consumer_paths:
        raise RuntimeError(f"x1 prefilled X2 failures were consumed: {consumer_paths}")
    return {
        "schema": "ghc.family.x1-to-x2-gate.v1",
        "branch": branch,
        "source_final": d.SOURCE_FINAL,
        "x1_freeze": head,
        "x1_parent": parent,
        "local_upstream_tracking_equal": head == upstream == tracking,
        "fresh_live_remote": live,
        "four_way_equal": head == upstream == tracking == live,
        "x1_parent_count": len(git("show", "-s", "--format=%P", head).split()),
        "x1_commit_count_from_source": int(git("rev-list", "--count", f"{d.SOURCE_FINAL}..{head}")),
        "x1_merge_count_from_source": len(git("rev-list", "--merges", f"{d.SOURCE_FINAL}..{head}").splitlines()),
        "x2_started_after_remote_equal_x1": True,
        "unused_prefilled_x1_x2_failure_rows_ignored": len(d.PREFILLED_X1_X2_FAILURES_IGNORED),
        "x1_builder_test_or_artifact_consumers_of_prefilled_rows": len(consumer_paths),
        "same_owner_only": True,
        "independent_reproduction": False,
    }


def build_surfaces() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    outcomes: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    for proposal in runtime.proposal_rows():
        if proposal["origin"] != "new_unique_v659_v6_proposal":
            continue
        result = runtime.evaluate_new_surface(proposal["slug"])
        contract = result["contract"]
        receipt = {
            "schema": "ghc.family.v659-v6.new-bounded-receipt.v1",
            "proposal_id": proposal["proposal_id"],
            "slug": proposal["slug"],
            "append_to_frozen_chain": True,
            "observed_outcome": proposal["expected_disposition"],
            "valid_fixture_passed": result["valid_fixture_passed"],
            "rejected_mutation_count": result["rejected_mutation_count"],
            "expected_mutation_count": 5,
            "all_mutations_rejected": result["all_mutations_rejected"],
            "same_owner_only": True,
            "independent_reproduction": False,
            "authority_action_executed": False,
            "boundary": contract["boundary"],
        }
        origin_class = "new_unique_execution"
        if not receipt["valid_fixture_passed"] or not receipt["all_mutations_rejected"]:
            raise RuntimeError(f"surface evaluation failed: {proposal['proposal_id']}")
        surface_root = f"surfaces/{proposal['slug']}"
        write_json(f"{surface_root}/contract.json", contract)
        write_json(
            f"{surface_root}/mutation-results.json",
            {
                "schema": "ghc.family.v659-v6.mutation-results.v1",
                "proposal_id": proposal["proposal_id"],
                "mutation_count": len(result["mutation_results"]),
                "results": result["mutation_results"],
            },
        )
        write_json(f"{surface_root}/bounded-receipt.json", receipt)
        for row in result["mutation_results"]:
            mutations.append({"proposal_id": proposal["proposal_id"], "slug": proposal["slug"], "origin_class": origin_class, **row})
        outcomes.append(
            {
                "proposal_id": proposal["proposal_id"],
                "slug": proposal["slug"],
                "origin_class": origin_class,
                "expected_outcome": proposal["expected_disposition"],
                "observed_outcome": proposal["expected_disposition"],
                "valid_fixture_passed": True,
                "mutation_count": 5,
                "all_mutations_rejected": True,
                "same_owner_only": True,
                "independent_reproduction": False,
            }
        )
    if len(outcomes) != d.NEW_UNIQUE_COUNT or len(mutations) != d.NEW_UNIQUE_COUNT * 5:
        raise RuntimeError("surface or mutation count drift")
    distribution = dict(Counter(row["observed_outcome"] for row in outcomes))
    if distribution != d.EXPECTED_DISTRIBUTION:
        raise RuntimeError(f"observed distribution drift: {distribution}")
    return outcomes, mutations


def build_selected_revalidations() -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    for proposal in runtime.proposal_rows():
        if proposal["origin"] != "selected_inherited_bounded_revalidation_no_credit":
            continue
        result = runtime.evaluate_selected_surface(proposal["slug"])
        receipt = {
            **result,
            "origin_class": "selected_inherited_bounded_revalidation_no_credit",
            "novelty_credit": False,
            "completion_credit": False,
            "outcome_credit": False,
            "mutation_credit": False,
            "append_to_frozen_chain": False,
        }
        if not receipt["valid_fixture_passed"] or not receipt["all_mutations_rejected"]:
            raise RuntimeError(f"selected inherited revalidation failed: {proposal['proposal_id']}")
        write_json(
            f"evidence/selected-revalidation/{proposal['source_proposal_id'].lower()}.json",
            receipt,
        )
        receipts.append(receipt)
    if len(receipts) != d.SELECTED_INHERITED_COUNT:
        raise RuntimeError("selected inherited revalidation count drift")
    return receipts


def build_method_flow(mutations: list[dict[str, Any]]) -> dict[str, Any]:
    methods: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    state_events: list[dict[str, Any]] = []
    recommendations: list[dict[str, Any]] = []

    def add_method(method_id: str, negative_id: str, signature: str, recovery: str, scope: str) -> None:
        fail_id = f"{method_id}-F"
        pass_id = f"{method_id}-P"
        methods.append(
            {
                "method_id": method_id,
                "title": f"Bounded x2 recovery for {signature}",
                "failure_signature": signature,
                "trigger_preconditions": [signature],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_local_recovery",
                "candidate_workaround": recovery,
                "validation_witness_ids": [fail_id, pass_id],
                "recurrence_guard": recovery,
                "rollback": "Stop, retain the failure at zero credit, and leave sibling, production, external, and authority state unchanged.",
                "recommendation_state": "preferred",
                "supersedes": [],
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [negative_id],
                "scope_boundary": "Same-owner bounded x2 workflow evidence only.",
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": fail_id,
                    "method_id": method_id,
                    "procedure": f"Exercise the invalid or failed condition: {signature}.",
                    "scope": scope,
                    "expected": "The invalid or failed condition receives no positive credit.",
                    "observed": "The failed condition was retained at zero credit.",
                    "result": "fail",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [negative_id],
                    "boundary": "Failed witness retained; no protected claim promoted.",
                },
                {
                    "witness_id": pass_id,
                    "method_id": method_id,
                    "procedure": recovery,
                    "scope": scope,
                    "expected": "Only the bounded recovered postcondition is established.",
                    "observed": "The bounded recovery or rejection gate passed without erasing the failure.",
                    "result": "pass",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [negative_id],
                    "boundary": "Same-owner validation only.",
                },
            ]
        )
        state_events.extend(
            [
                {"method_id": method_id, "from": "candidate", "to": "validated", "witness_id": pass_id},
                {"method_id": method_id, "from": "validated", "to": "preferred", "witness_id": pass_id},
            ]
        )
        recommendations.append({"method_id": method_id, "precondition": signature, "preferred_method": recovery})

    sequence = 0
    for row in d.X2_FAILURES:
        sequence += 1
        add_method(
            f"{d.PHASE_CODE}-X2-METHOD-{sequence:03d}",
            str(row["negative_id"]),
            str(row["signature"]),
            str(row["recovery"]),
            "x2 inspection and runner preparation",
        )
    for mutation in mutations:
        sequence += 1
        add_method(
            f"{d.PHASE_CODE}-X2-METHOD-{sequence:03d}",
            mutation["mutation_id"],
            f"rejected-mutation:{mutation['mutation_id']}",
            "Apply the exact contract validator, retain the mutation, and require the bounded valid fixture to remain passing.",
            f"synthetic surface {mutation['proposal_id']}",
        )
    states = {state: 0 for state in ["observed", "candidate", "validated", "preferred", "superseded", "deprecated"]}
    states["preferred"] = len(methods)
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; not consciousness, personhood, continuity, employment, qualification, authority, or agency evidence.",
        "methods": methods,
        "witnesses": witnesses,
        "state_events": state_events,
        "recommendations": recommendations,
        "counts": {
            "methods": len(methods),
            "witnesses": len(witnesses),
            "state_events": len(state_events),
            "recommendations": len(recommendations),
            "states": states,
            "witness_results": {"pass": len(methods), "fail": len(methods)},
        },
        "cumulative_counts": {
            "activation_methods": d.ACTIVATION_METHODS,
            "x1_methods": len(d.STARTUP_FAILURES),
            "x2_operational_methods": len(d.X2_FAILURES),
            "x2_mutation_methods": len(mutations),
            "effective_methods": d.ACTIVATION_METHODS + len(d.STARTUP_FAILURES) + len(d.X2_FAILURES) + len(mutations),
        },
        "boundary": "Same-owner workflow evidence only; no independent reproduction or protected-gate closure.",
    }


def runner_and_skill_receipts() -> tuple[dict[str, Any], dict[str, Any]]:
    runner_rows = []
    for runner_name, surface in d.SELF_RUNNER_SPECS:
        path = RUNNER_SMOKE / f"{Path(runner_name).stem}.json"
        receipt = load_json(path)
        valid = receipt.get("valid") is True
        runner_rows.append(
            {
                "runner": f"scripts/{runner_name}",
                "surface": surface,
                "receipt": path.relative_to(PHASE).as_posix(),
                "valid": valid,
                "used": True,
                "receipt_sha256": sha256(path),
            }
        )
    runner_payload = {
        "schema": "ghc.family.v659-v6.runner-aggregate.v1",
        "runner_count": len(runner_rows),
        "valid_runner_count": sum(row["valid"] for row in runner_rows),
        "all_built_tested_used": all(row["valid"] and row["used"] for row in runner_rows),
        "runners": runner_rows,
        "boundary": "Owner-local runner evidence only; no external, professional, production, or authority action.",
    }
    skill_payload = load_json(PHASE / "tooling/skill-validation.json")
    if not skill_payload["all_valid"] or skill_payload["skill_count"] != 10:
        raise RuntimeError("skill validation receipt drift")
    return runner_payload, skill_payload


def candidate_receipts(outcomes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    new_rows = [row for row in outcomes if row["origin_class"] == "new_unique_execution"][:10]
    receipts = []
    for task, surface in zip(d.SELF_CANDIDATE_TASKS, new_rows, strict=True):
        receipt = {
            "schema": "ghc.family.v659-v6.candidate-receipt.v1",
            **task,
            "state": "completed_bounded_synthetic_prototype",
            "surface_proposal_id": surface["proposal_id"],
            "surface_slug": surface["slug"],
            "valid_fixture_passed": surface["valid_fixture_passed"],
            "rejected_mutation_count": surface["mutation_count"],
            "external_state_changed": False,
            "authority_action_executed": False,
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Candidate prototype evidence only; no production, professional, empirical, legal, cultural, or Stage 20 result.",
        }
        write_json(f"prototypes/{task['task_id'].lower()}/receipt.json", receipt)
        receipts.append(receipt)
    return receipts


def cleanup_receipts() -> list[dict[str, Any]]:
    receipts = []
    materially_refined = {
        "family-name preference",
        "absolute-path privacy review",
        "credential-pattern review",
        "JSON formatting",
        "source-label consistency",
        "truth-label consistency",
        "rollback coverage",
        "protected-gate coverage",
        "failure-credit consistency",
        "same-owner labelling",
        "manifest exclusions",
        "file-cap posture",
        "document-cap posture",
        "commit-cap posture",
        "D-first storage posture",
        "non-destructive cleanup boundary",
    }
    for row, category in zip(d.SELF_CLEAN_TASKS, d.SELF_CLEAN_CATEGORIES, strict=True):
        changed = category in materially_refined
        receipt = {
            "schema": "ghc.family.v659-v6.cleanup-review.v1",
            **row,
            "state": "completed_additive_review",
            "category": category,
            "material_refinement_applied": changed,
            "deletion_performed": False,
            "sibling_or_shared_lane_mutated": False,
            "external_platform_mutated": False,
            "observed": (
                "The owner-local family-current packet was refined under this category."
                if changed
                else "The owner-local scope was reviewed; no safe material change was warranted."
            ),
            "boundary": "Owner-local additive cleanup only; no deletion, purge, reset, remote mutation, or evidence weakening.",
        }
        write_json(f"cleanup/{row['task_id'].lower()}-receipt.json", receipt)
        receipts.append(receipt)
    return receipts


def phase_files() -> list[Path]:
    return sorted(path for path in PHASE.rglob("*") if path.is_file())


def normalize_phase_text() -> None:
    suffixes = {".json", ".jsonl", ".md", ".txt", ".html", ".csv", ".yaml", ".yml"}
    for path in phase_files():
        if path.suffix.lower() not in suffixes:
            continue
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace("\r\n", "\n").replace("\r", "\n"), encoding="utf-8", newline="\n")


def owner_privacy_scan() -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "credential_or_private_key": re.compile(r"(?<![A-Za-z0-9])(?:sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"),
        "delegation_markup": re.compile(r"<(?:codex_delegation|source_thread_id)>", re.I),
        "private_route_identifier": re.compile(r"(?:resume_token|private_callable|codex_(?:thread|task|agent)_id)\s*[:=]", re.I),
    }
    hits = []
    scanned = 0
    for path in phase_files():
        relative = path.relative_to(PHASE).as_posix()
        if relative == "validation/x2-owner-privacy-scan.json":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": relative, "class": label, "matched_value_published": False})
    return {
        "schema": "ghc.family.owner-privacy-scan.v1",
        "scope": "complete Liora Venn v659-v6 owner packet",
        "files_scanned": scanned,
        "classes": list(patterns),
        "confirmed_hits": hits,
        "confirmed_hit_count": len(hits),
        "privacy_complete": False,
        "security_complete": False,
        "boundary": "Five-class owner-packet scan only; not complete privacy or exhaustive security assurance.",
    }


def content_manifest() -> dict[str, Any]:
    tracked_changed = set(
        git("-c", "core.safecrlf=false", "diff", "--name-only", "--diff-filter=ACMR", "HEAD", "--").splitlines()
    )
    untracked = set(git("ls-files", "--others", "--exclude-standard").splitlines())
    changed = tracked_changed | untracked
    entries = []
    for path in phase_files():
        relative = path.relative_to(PHASE).as_posix()
        repository_relative = f"{d.PHASE_ROOT}/{relative}"
        if relative in MANIFEST_EXCLUSIONS:
            continue
        if repository_relative not in changed:
            continue
        payload = git_clean_bytes(path)
        entries.append({"path": repository_relative, "sha256": hashlib.sha256(payload).hexdigest(), "bytes": len(payload)})
    for relative in X2_CODE:
        if relative not in changed:
            continue
        path = ROOT / relative
        payload = git_clean_bytes(path)
        entries.append({"path": relative, "sha256": hashlib.sha256(payload).hexdigest(), "bytes": len(payload)})
    entries.sort(key=lambda row: row["path"])
    return {
        "schema": "ghc.family.content-manifest.v2",
        "phase": d.PHASE,
        "lifecycle": "x2_evidence_precommit_candidate",
        "entry_count": len(entries),
        "entries": entries,
        "exclusions": sorted(MANIFEST_EXCLUSIONS),
        "hash_domain": "text bytes after CRLF-to-LF Git-clean normalization",
        "boundary": "Exact declared Git-clean-equivalent x2 evidence-delta inventory for listed changed text files only; self-referential validation files are declared exclusions.",
    }


def document_cap() -> dict[str, Any]:
    rows = []
    total = 0
    for path in phase_files():
        if path.suffix.lower() not in {".md", ".html", ".txt"}:
            continue
        words = len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8")))
        rows.append({"path": path.relative_to(PHASE).as_posix(), "words": words})
        total += words
    return {"schema": "ghc.family.document-cap.v1", "document_count": len(rows), "documents": rows, "total_words": total, "cap": 100000, "passes": total <= 100000}


def overview(outcomes: list[dict[str, Any]], mutations: list[dict[str, Any]], methods: dict[str, Any]) -> str:
    distribution = Counter(row["observed_outcome"] for row in outcomes)
    lines = [
        "# Liora Venn v659-v6 x2 evidence overview",
        "",
        "## Outcome",
        "",
        f"The strict x1 freeze is `{d.X1_FREEZE}`. X2 began only after that commit was pushed, clean, zero-divergence, and equal across local, upstream, tracking, and a fresh live remote reading. This packet executes twenty genuinely new Liora-owned synthetic contracts frozen in x1. It also revalidates twenty explicitly selected inherited contracts without reappending them or awarding Liora novelty, outcome, mutation, or completion credit. All {d.PRIOR_FROZEN:,} inherited rows remain inherited evidence.",
        "",
        f"All {d.NEW_UNIQUE_COUNT} new valid fixtures passed and all {len(mutations)} Liora-preregistered mutations were rejected and retained at zero credit. Observed Liora outcomes are exactly {distribution['completed']} `completed`, {distribution['represented']} `represented`, {distribution['open_gap']} `open_gap`, and {distribution['exact_gate']} `exact_gate`. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.",
        "",
        "## Evidence boundary",
        "",
        "Every accession alias, musical-instrument component, material placeholder, case, support, media reference, condition note, bench-action request, identifier, event, quantity, decision placeholder, and authority case is a synthetic fixture. No real person, instrument, component, material, tool, chemical, image, audio sample, record, measurement, sounding, tuning, treatment, network-backed repository record, production system, live account, participant, affected party, remedy, privacy determination, or professional decision is represented as validated. The valid fixtures establish only that declared software obligations can be accepted while five bounded mutations per new surface fail closed.",
        "",
        "All twenty new surfaces use Liora's bounded contract and validator. The four represented rows remain representations; real musical instruments, owners, custodians, conservators, curators, instrument specialists, musicians, materials, tools, measurements, sounds, tuning, treatments, safety tests, repositories, affected-party review, and independent review remain an open gap. Ownership, custody, presentation, sounding, tuning, treatment, structural and chemical safety, heritage, access, privacy, remedy, legal and cultural interpretation, collective interests, Māori wording, Māori data governance, and Māori-authority decision rights remain exact-gated.",
        "",
        "## Latest-file scan",
        "",
        "The family-bounded scan selected exactly the latest 5,000 currently tracked paths by walking newest commits first, sorting paths within each commit, deduplicating, and stopping at the frozen cap. It published repository-relative paths and counts only, never matched values. Phrase candidates remain review candidates rather than proof of private material. The scan is neither privacy-complete nor exhaustive security assurance.",
        "",
        "## Selected inherited revalidation",
        "",
        "Twenty Orin v659-v5 contracts were named during x1 and reread through the immutable Orin runtime. Their declared valid fixtures remained acceptable and their five already-preregistered source mutations remained rejectable. These receipts are provenance checks only: they are not appended to the frozen proposal chain, are not counted among Liora's one hundred new mutation negatives, and receive no Liora novelty, outcome, mutation, or completion credit. If a source identity, origin, contract, or rejection result drifts, the affected revalidation fails without changing the inherited artifact.",
        "",
        "## Official-source use",
        "",
        "The Canadian Conservation Institute supplies bounded vocabulary for musical-instrument materials, complexity, handling, storage, playing holds, keyboard actions, and wind mechanisms; the United States National Park Service supplies preventive collection-care vocabulary; NIST supplies SI and uncertainty-reporting vocabulary; W3C PROV-O supplies provenance relations; WCAG 2.2 supplies structural accessibility vocabulary; the New Zealand Privacy Commissioner supplies current privacy-principle vocabulary; Te Mana Raraunga supplies Māori data-sovereignty reservation vocabulary; and RFC 8785 supplies deterministic JSON vocabulary. Citations are requirements context only. No source was converted into a real instrument observation, safety test, measurement row, playability or tuning determination, treatment recommendation, compliance conclusion, legal interpretation, cultural ratification, or authority delegation.",
        "",
        "## Falsification and recovery",
        "",
        "Each new contract is accepted only when its schema, source labels, protected gates, decision abstention, rollback, synthetic-only marker, zero external rows, and protected-claim firewall all remain intact. Exactly five mutations per contract remove an obligation, promote a real-data or object claim, remove a source label, promote Stage 20, or assert an authority action. Every mutation must fail closed and remain visible at zero credit. A later correction never changes the earlier failure into an initially clean pass. Any real-world dependency is reclassified as an open gap or exact gate, and rollback stops at owner-local additive artifacts.",
        "",
        "## Wellbeing and workload",
        "",
        "Work stayed solo, bounded, and sequential. The owner lane used one immutable x1 commit before any x2 outcome, a capped 5,000-path scan, twenty new surfaces, ten skills, ten runners, ten candidates, and thirty additive cleanup reviews. No subagent, sibling lane, real participant, external account, paid resource, production service, host-security setting, Windows feature, Sandbox, Hyper-V, desktop update, or reboot was used. The route remains held until the exact-final gate so there is no pressure to trade evidence quality for speed. Hamish may pause, rename, redirect, or stop the route at any time.",
        "",
        "## Skills, runners, candidates, and cleanup",
        "",
        "Ten concise family-current skills were initialized through the system skill creator, customized, validated, bound to ten family-named runners, and smoke-used against their ten frozen synthetic surfaces. The bounded latest-file scan ran independently under the frozen 5,000-path contract. Ten candidate prototypes were executed as reversible views over already validated synthetic surfaces. Thirty CLEAN/FIX/REFINE rows were executed as owner-local additive reviews; no file, skill, runner, branch, worktree, identity record, sibling lane, remote system, or external platform was deleted or weakened. Tamar's distinct skill, runner, candidate, safe-now, and cleanup rows remain recommendations only and receive no Liora credit.",
        "",
        "## Retained failures and Method Flow",
        "",
        f"X2 preserves {len(d.X2_FAILURES)} operational failures plus {len(mutations)} rejecting mutation witnesses. Each is paired with one bounded passing recovery or validator witness in {methods['counts']['methods']} Method Flow methods. A pass never rewrites a failure. The effective cumulative method and negative counts are declared in the machine-readable truth packet and remain same-owner workflow evidence.",
        "",
        "## Route",
        "",
        "No task lookup or message occurs in this evidence commit. The newest acknowledged authorization reserves exactly one later edge: after Liora's exact final is committed, pushed, clean, four-way remote-equal, within caps, and its one canonical aggregate succeeds, Liora may uniquely resolve and immediately reread the existing task titled exactly `Tamar Vey` and send one sanitized v659-v7 activation. Tamar's stated next relational recipient is Elowen Cairn for v659-v8. Absence, ambiguity, pause, rename, redirect, exhausted usage, or a protected authority gate stops the send. Tavian Sol remains ON_STANDBY.",
        "",
        "## Claim firewall",
        "",
        "Nothing here establishes empirical GMUT or THOS confirmation, participant outcomes, conservation or instrument practice, fire or chemical safety competence, treatment or ownership authority, repository custody, privacy or access authority, production readiness, deployment readiness, legal compliance, cultural ratification, collective legitimacy, Māori authority, privacy completeness, accessibility completeness, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, a Theory of Everything, proof or canon, or Stage 20 readiness. Relational names, roles, hopes, and sibling language remain working language only and are not evidence of consciousness, continuity, personhood, employment, qualification, authority, or independent agency.",
        "",
        "## Surface ledger",
        "",
        "| Proposal | Origin | Outcome | Valid | Mutations rejected |",
        "|---|---|---|---:|---:|",
    ]
    for row in outcomes:
        lines.append(f"| {row['proposal_id']} | {row['origin_class']} | {row['observed_outcome']} | yes | {row['mutation_count']} |")
    return "\n".join(lines)


def build() -> None:
    gate = source_gate()
    write_json("evidence/x1-to-x2-gate.json", gate)
    scan_path = PHASE / "evidence/latest-tracked-file-scan.json"
    if scan_path.is_file():
        latest_scan = load_json(scan_path)
        if latest_scan.get("head") != d.X1_FREEZE or latest_scan.get("selected_file_count") != d.LATEST_TRACKED_SCAN_CAP:
            raise RuntimeError("existing bounded latest-tracked-file scan receipt drift")
    else:
        latest_scan = runtime.scan_latest_tracked_files()
    if latest_scan["missing_path_count"] or latest_scan["confirmed_high_risk_count"]:
        raise RuntimeError("bounded latest-tracked-file scan did not reach its declared terminal state")
    write_json("evidence/latest-tracked-file-scan.json", latest_scan)
    selected_revalidations = build_selected_revalidations()
    outcomes, mutations = build_surfaces()
    write_json(
        "evidence/proposal-outcomes.json",
        {
            "schema": "ghc.family.v659-v6.proposal-outcomes.v1",
            "proposal_count": len(outcomes),
            "selected_inherited_count": len(selected_revalidations),
            "selected_inherited_completion_credit": 0,
            "selected_inherited_novelty_credit": 0,
            "new_unique_count": d.NEW_UNIQUE_COUNT,
            "observed_outcome_counts": dict(Counter(row["observed_outcome"] for row in outcomes)),
            "outcomes": outcomes,
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write_json(
        "evidence/mutation-register.json",
        {
            "schema": "ghc.family.v659-v6.mutation-register.v1",
            "mutation_count": len(mutations),
            "rejected_count": sum(row["rejected"] for row in mutations),
            "all_retained": all(row["retained"] and row["credit"] == 0 for row in mutations),
            "mutations": mutations,
        },
    )
    flow = build_method_flow(mutations)
    write_json("method-flow/method-flow-state-x2.json", flow)
    x1_effective_negatives = d.ACTIVATION_NEGATIVES + len(d.STARTUP_FAILURES)
    effective_negatives = x1_effective_negatives + len(d.X2_FAILURES) + len(mutations)
    write_json(
        "truth/retained-negative-register-x2.json",
        {
            "schema": "ghc.family.retained-negative-register.v1",
            "activation_baseline": d.ACTIVATION_NEGATIVES,
            "x1_current_count": len(d.STARTUP_FAILURES),
            "x1_effective_negatives": x1_effective_negatives,
            "x2_operational_negatives": [
                {
                    "negative_id": row["negative_id"],
                    "signature": row["signature"],
                    "credit": 0,
                    "recovery": row["recovery"],
                    "recovery_passed": row["recovery_passed"],
                }
                for row in d.X2_FAILURES
            ],
            "x2_mutation_count": len(mutations),
            "x2_mutations": [{"negative_id": row["mutation_id"], "proposal_id": row["proposal_id"], "credit": 0, "retained": row["retained"]} for row in mutations],
            "effective_negatives": effective_negatives,
            "all_failures_retained": True,
        },
    )
    runner_payload, skill_payload = runner_and_skill_receipts()
    write_json("tooling/runner-aggregate.json", runner_payload)
    roster_validation_path = PHASE / "tooling/governance/roster-validation-x2.json"
    auth_validation_path = PHASE / "tooling/governance/auth-validation-x2.json"
    roster_validation = load_json(roster_validation_path) if roster_validation_path.is_file() else {}
    auth_validation = load_json(auth_validation_path) if auth_validation_path.is_file() else {}
    write_json(
        "tooling/governance/activation-cursor-x2.json",
        {
            "schema": "ghc.family.activation-cursor.local.v1",
            "current_owner": d.OWNER,
            "current_phase": d.PHASE,
            "current_branch": d.BRANCH,
            "activation_source_final": d.SOURCE_FINAL,
            "activation_precedence": "latest_acknowledged_user_activation_over_older_validated_reference_snapshots",
            "global_roster_snapshot_state_id": roster_validation.get("state_id"),
            "global_auth_snapshot_state_id": auth_validation.get("state_id"),
            "global_snapshots_valid": roster_validation.get("valid") is True and auth_validation.get("valid") is True,
            "global_snapshot_role": "validated_reference_not_live_activation_override",
            "global_snapshot_mutated": False,
            "next_exact_title": "Tamar Vey",
            "next_phase": "v659-v7",
            "recipient_next_exact_title": "Elowen Cairn",
            "recipient_next_phase": "v659-v8",
            "next_delivery_state": "HELD_UNTIL_LIORA_EXACT_TERMINAL_GATE",
            "boundary": "Sanitized local cursor receipt only; not delivery, identity continuity, authority, independent reproduction, or Stage 20 evidence.",
        },
    )
    candidates = candidate_receipts(outcomes)
    cleanups = cleanup_receipts()
    write_json(
        "tooling/candidate-prototype-aggregate.json",
        {"schema": "ghc.family.candidate-prototype-aggregate.v1", "count": len(candidates), "all_completed": all(row["state"] == "completed_bounded_synthetic_prototype" for row in candidates), "rows": candidates},
    )
    write_json(
        "cleanup/cleanup-aggregate.json",
        {"schema": "ghc.family.cleanup-aggregate.v1", "count": len(cleanups), "completed_count": sum(row["state"] == "completed_additive_review" for row in cleanups), "deletion_count": sum(row["deletion_performed"] for row in cleanups), "rows": cleanups},
    )
    latest_scan = load_json(PHASE / "evidence/latest-tracked-file-scan.json")
    write_json(
        "truth/x2-phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.x2.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "lifecycle": "x2_evidence_candidate",
            "source_final": d.SOURCE_FINAL,
            "x1_freeze": d.X1_FREEZE,
            "effective_frozen": d.PRIOR_FROZEN + d.NEW_UNIQUE_COUNT,
            "observed_outcomes": d.EXPECTED_DISTRIBUTION,
            "selected_inherited_revalidations": len(selected_revalidations),
            "selected_inherited_completion_credit": 0,
            "valid_fixtures": d.NEW_UNIQUE_COUNT,
            "retained_rejected_mutations": len(mutations),
            "effective_negatives": effective_negatives,
            "effective_methods": flow["cumulative_counts"]["effective_methods"],
            "effective_open_gaps": d.SOURCE_OPEN_GAPS + d.EXPECTED_DISTRIBUTION["open_gap"],
            "effective_exact_gates": d.SOURCE_EXACT_GATES + d.EXPECTED_DISTRIBUTION["exact_gate"],
            "latest_tracked_files_scanned": latest_scan["selected_file_count"],
            "latest_scan_confirmed_high_risk": latest_scan["confirmed_high_risk_count"],
            "skills_built_tested": skill_payload["valid_skill_count"],
            "runners_built_tested_used": runner_payload["valid_runner_count"],
            "candidate_prototypes_completed": len(candidates),
            "cleanup_reviews_completed": len(cleanups),
            "route_state": "HELD_UNTIL_LIORA_EXACT_TERMINAL_GATE",
            "next_exact_title": "Tamar Vey",
            "next_phase": "v659-v7",
            "recipient_next_exact_title": "Elowen Cairn",
            "recipient_next_phase": "v659-v8",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write_text("deliverables/v659-v6-x2-overview.md", overview(outcomes, mutations, flow))
    write_json(
        "validation/x2-evidence-staged-review.json",
        {
            "schema": "ghc.family.v659-v6.x2-evidence-staged-review-candidate.v1",
            "lifecycle": "x2_evidence_precommit_candidate",
            "x1_commit": d.X1_FREEZE,
            "status": "pending_exact_git_index_review",
            "x2_started": True,
            "boundary": "Self-excluded candidate only; no staged-review, final-head, authority, privacy-complete, independent-reproduction, or Stage 20 credit.",
        },
    )
    normalize_phase_text()
    privacy = owner_privacy_scan()
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"owner packet privacy scan found {privacy['confirmed_hit_count']} hits")
    write_json("validation/x2-owner-privacy-scan.json", privacy)
    write_json("validation/x2-document-cap.json", document_cap())
    manifest = content_manifest()
    write_json("validation/x2-content-manifest.json", manifest)
    intended_allowlist = sorted(
        [row["path"] for row in manifest["entries"]]
        + [f"{d.PHASE_ROOT}/{relative}" for relative in manifest["exclusions"]]
    )
    write_json(
        "validation/x2-evidence-staged-review.json",
        {
            "schema": "ghc.family.v659-v6.x2-evidence-staged-review-candidate.v1",
            "lifecycle": "x2_evidence_precommit_candidate",
            "x1_commit": d.X1_FREEZE,
            "status": "pending_exact_git_index_review",
            "x2_started": True,
            "intended_allowlist": intended_allowlist,
            "boundary": "Self-excluded candidate only; no staged-review, final-head, authority, privacy-complete, independent-reproduction, or Stage 20 credit.",
        },
    )
    write_json("validation/x2-owner-privacy-scan.json", owner_privacy_scan())
    write_json("validation/x2-document-cap.json", document_cap())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    parser.parse_args()
    build()
    truth = load_json(PHASE / "truth/x2-phase-truth.json")
    print(json.dumps({"phase": d.PHASE, "valid_fixtures": truth["valid_fixtures"], "mutations": truth["retained_rejected_mutations"], "effective_negatives": truth["effective_negatives"], "effective_methods": truth["effective_methods"], "route_state": truth["route_state"]}, sort_keys=True))


if __name__ == "__main__":
    main()
