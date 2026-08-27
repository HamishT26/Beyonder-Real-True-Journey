"""Build the Elowen Cairn v672-v8 closeout and exact-final candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_ghc_family_elowen_cairn_v672_v8_x1 import batch_blobs


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "elowen-cairn" / "v672-v8"
OWNER = "Elowen Cairn"
PHASE = "v672-v8"
BRANCH = "codex/GHC-Family/elowen-cairn-v672-v8-full-tools"
SOURCE_FINAL = "23110f2bb3a8b111626e2af56b6343bbc15a9496"
X1_COMMIT = "2a147ca77378e73fa6d8ff4f95a1f21154da66a8"
EVIDENCE_COMMIT = "cfc32a909fe9693238166020e22b1eaf8b646a8d"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
EVIDENCE_COUNTS = {
    "effective_negatives": 36157,
    "effective_methods": 22485,
    "failed_witnesses": 7818,
    "bounded_passing_witnesses": 10048,
}
COUNTS = {
    "effective_negatives": 36160,
    "effective_methods": 22488,
    "failed_witnesses": 7821,
    "bounded_passing_witnesses": 10051,
    "open_gaps": 291,
    "exact_gates": 284,
}
EXPECTED_FINAL_TESTS = 25
BOUNDARY = (
    "Bounded owner-local software or wholly synthetic evidence only; never empirical "
    "confirmation, participant evidence, professional authority, production readiness, legal "
    "or cultural ratification, Māori authority, affected-party acceptance, complete privacy or "
    "accessibility assurance, exhaustive security, independent reproduction, AGI or ASI, "
    "consciousness or personhood evidence, Theory-of-Everything proof, proof or canon, or "
    "Stage 20 authority."
)
IDENTITY_BOUNDARY = (
    "Elowen Cairn, they/them, relational boundary cartographer and evidence steward, is relational "
    "language only; not consciousness, sentience, legal personhood, identity continuity, "
    "employment, qualification, independent agency, or scientific, operational, professional, "
    "legal, cultural, affected-party, or Māori authority evidence."
)
RUNNER_PATHS = [
    "scripts/ghc_family_music_box_identity.py",
    "scripts/ghc_family_cylinder_pin_track.py",
    "scripts/ghc_family_comb_tooth_relation.py",
    "scripts/ghc_family_spring_motor_abstention.py",
    "scripts/ghc_family_tune_attribution_vacancy.py",
    "scripts/ghc_family_disc_projection_abstention.py",
    "scripts/ghc_family_music_box_condition_separation.py",
    "scripts/ghc_family_music_box_provenance_correction.py",
    "scripts/ghc_family_music_box_privacy_access.py",
    "scripts/ghc_family_music_box_workload_handover.py",
]
FINAL_CODE_PATHS = [
    "scripts/build_ghc_family_elowen_cairn_v672_v8_final.py",
    "scripts/validate_ghc_family_elowen_cairn_v672_v8_final.py",
    "tests/test_ghc_family_elowen_cairn_v672_v8_final.py",
]
FINAL_VALIDATION_PATHS = [
    "docs/elowen-cairn/v672-v8/validation/final-delta-manifest.json",
    "docs/elowen-cairn/v672-v8/validation/final-owner-manifest.json",
    "docs/elowen-cairn/v672-v8/validation/final-method-flow-validation.json",
    "docs/elowen-cairn/v672-v8/validation/final-staged-privacy.json",
    "docs/elowen-cairn/v672-v8/validation/final-staged-review.json",
    "docs/elowen-cairn/v672-v8/validation/final-validation-receipt.json",
    "docs/elowen-cairn/v672-v8/validation/final-precommit-test-receipt.json",
]

FINAL_FAILURES = [
    {
        "negative_id": "EC6728-CLOSE-N001",
        "title": "recover bounded final-scaffold inspection",
        "failed": (
            "The first combined final-builder projection joined a long source slice with a broad regular-"
            "expression report and exceeded the model-visible output context before the review completed."
        ),
        "passed": (
            "Bounded line windows and separate narrow regular-expression summaries recovered every required "
            "final-builder section without truncation, mutation, or a second broad projection."
        ),
        "recurrence_guard": "Never combine a long source slice and a broad match report in one projection.",
        "rollback": "No rollback was required because the failed projection was read-only.",
    },
    {
        "negative_id": "EC6728-CLOSE-N002",
        "title": "recover exact stale-label patch context",
        "failed": (
            "The first wide stale-label patch used a final context fragment whose live line wrapping did "
            "not match, so apply_patch rejected the entire patch atomically before changing any byte."
        ),
        "passed": (
            "Smaller exact-context patches updated the stale-label definitions, dispositions, and compile "
            "selection independently, preserving the rejected patch as a zero-credit witness."
        ),
        "recurrence_guard": "Split multi-region patches when live wrapping has not been verified exactly.",
        "rollback": "No rollback was required because the rejected patch was atomic and changed no byte.",
    },
    {
        "negative_id": "EC6728-CLOSE-N003",
        "title": "bound exact evidence-manifest tree resolution",
        "failed": (
            "The first closeout build inherited a full-repository git ls-tree traversal, remained blocked "
            "before writing any closeout artifact, and was terminated together with its exact child process."
        ),
        "passed": (
            "The recovery resolves only paths declared by the immutable evidence manifest in bounded chunks, "
            "then replays their exact Git blobs without enumerating the full repository tree."
        ),
        "recurrence_guard": "Resolve commit objects from declared manifest paths instead of full-tree enumeration.",
        "rollback": "No repository rollback was required because the stalled build wrote no closeout artifact.",
    },
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def load(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def commit_objects_for_paths(
    commit: str, paths: list[str], *, chunk_size: int = 48
) -> dict[str, tuple[str, str]]:
    objects: dict[str, tuple[str, str]] = {}
    for offset in range(0, len(paths), chunk_size):
        rows = git_text("ls-tree", commit, "--", *paths[offset : offset + chunk_size]).splitlines()
        for row in rows:
            left, path = row.split("\t", 1)
            mode, _kind, object_id = left.split()
            objects[path] = (mode, object_id)
    return objects


def replay_committed_manifest(commit: str, relative: str) -> dict[str, Any]:
    manifest = json.loads(
        git("show", f"{commit}:docs/elowen-cairn/v672-v8/validation/{relative}").stdout.decode(
            "utf-8"
        )
    )
    paths = [row["path"] for row in manifest["entries"]]
    objects = commit_objects_for_paths(commit, paths)
    missing = [row["path"] for row in manifest["entries"] if row["path"] not in objects]
    blobs = (
        batch_blobs([objects[row["path"]][1] for row in manifest["entries"]])
        if not missing
        else []
    )
    mismatches = []
    if not missing:
        for row, blob in zip(manifest["entries"], blobs, strict=True):
            if (
                blob is None
                or len(blob) != row["bytes"]
                or sha(blob) != row["sha256"]
                or objects[row["path"]][0] != row["mode"]
            ):
                mismatches.append(row["path"])
    return {
        "entry_count": manifest["entry_count"],
        "self_exclusions": manifest["self_exclusions"],
        "missing": missing,
        "mismatches": mismatches,
        "manifest": manifest,
    }


def verify_evidence_gate() -> dict[str, Any]:
    branch = git_text("branch", "--show-current")
    head = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{branch}")
    live_tokens = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").split()
    live = live_tokens[0] if live_tokens else None
    divergence = [
        int(value)
        for value in git_text(
            "rev-list", "--left-right", "--count", "HEAD...@{upstream}"
        ).split()
    ]
    evidence_parent = git_text("rev-parse", f"{EVIDENCE_COMMIT}^")
    x1_parent = git_text("rev-parse", f"{X1_COMMIT}^")
    replay = replay_committed_manifest(EVIDENCE_COMMIT, "evidence-manifest.json")
    changed = set(
        git_text(
            "diff-tree", "--no-commit-id", "--name-only", "-r", EVIDENCE_COMMIT
        ).splitlines()
    )
    expected = {row["path"] for row in replay["manifest"]["entries"]} | set(
        replay["self_exclusions"]
    )
    allowed_exact = set(FINAL_CODE_PATHS + FINAL_VALIDATION_PATHS)
    status_rows = git_text("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    unexpected = []
    for row in status_rows:
        code, path = row[:2], row[3:]
        allowed_doc = path.startswith(
            (
                "docs/elowen-cairn/v672-v8/closeout/",
                "docs/elowen-cairn/v672-v8/final/",
                "docs/elowen-cairn/v672-v8/seal/",
                "docs/elowen-cairn/v672-v8/handoffs/",
                "docs/elowen-cairn/v672-v8/orchestration/",
            )
        )
        if code not in {"??", "A ", "AM", " M"} or not (
            path in allowed_exact or allowed_doc
        ):
            unexpected.append(row)
    gate = {
        "branch": branch,
        "head": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "four_way_equal": head == upstream == tracking == live == EVIDENCE_COMMIT,
        "divergence": {"ahead": divergence[0], "behind": divergence[1]},
        "evidence_parent": evidence_parent,
        "evidence_direct_child_of_x1": evidence_parent == X1_COMMIT,
        "x1_parent": x1_parent,
        "x1_direct_child_of_source": x1_parent == SOURCE_FINAL,
        "evidence_manifest_entries": replay["entry_count"],
        "evidence_manifest_missing": replay["missing"],
        "evidence_manifest_mismatches": replay["mismatches"],
        "evidence_manifest_commit_coverage": changed == expected,
        "unexpected_prebuild_status": unexpected,
    }
    if (
        branch != BRANCH
        or not gate["four_way_equal"]
        or divergence != [0, 0]
        or not gate["evidence_direct_child_of_x1"]
        or not gate["x1_direct_child_of_source"]
        or replay["missing"]
        or replay["mismatches"]
        or changed != expected
        or unexpected
    ):
        raise SystemExit(json.dumps(gate, ensure_ascii=False, sort_keys=True))
    return gate


def extend_final_flow(flow: dict[str, Any]) -> dict[str, Any]:
    ledger = deepcopy(flow)
    for index, row in enumerate(FINAL_FAILURES, start=1):
        method_id = f"EC6728-FINAL-M{index:03d}"
        fail_id = f"{method_id}-F"
        pass_id = f"{method_id}-P"
        negative_id = row["negative_id"]
        ledger["methods"].append(
            {
                "method_id": method_id,
                "title": row["title"],
                "failure_signature": row["failed"],
                "trigger_preconditions": ["the declared closeout failure signature is observed"],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now",
                "candidate_workaround": row["passed"],
                "validation_witness_ids": [fail_id, pass_id],
                "recurrence_guard": row["recurrence_guard"],
                "rollback": row["rollback"],
                "recommendation_state": "preferred",
                "supersedes": [],
                "protected_gates": [
                    "exact_evidence",
                    "no_failure_laundering",
                    "no_canonical_replay",
                    "no_successor_precontact",
                ],
                "retained_negative_ids": [negative_id],
                "scope_boundary": BOUNDARY,
            }
        )
        ledger["witnesses"].extend(
            [
                {
                    "witness_id": fail_id,
                    "method_id": method_id,
                    "procedure": row["failed"],
                    "scope": "owner-local read-only closeout workflow",
                    "expected": "an attributable exact bounded result",
                    "observed": row["failed"],
                    "result": "fail",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [negative_id],
                    "boundary": BOUNDARY,
                },
                {
                    "witness_id": pass_id,
                    "method_id": method_id,
                    "procedure": row["passed"],
                    "scope": "owner-local bounded closeout recovery",
                    "expected": "the isolated predicate passes without rewriting its failure",
                    "observed": row["passed"],
                    "result": "pass",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [negative_id],
                    "boundary": BOUNDARY,
                },
            ]
        )
        for before, after, reason in (
            (None, "candidate", "closeout failure recorded"),
            ("candidate", "validated", "bounded recovery passed"),
            ("validated", "preferred", "recurrence guard retained"),
        ):
            ledger["state_events"].append(
                {
                    "event_index": len(ledger["state_events"]) + 1,
                    "method_id": method_id,
                    "before": before,
                    "after": after,
                    "reason": reason,
                    "witness_id": fail_id if before is None else pass_id,
                }
            )
        ledger["recommendations"].append(
            {
                "method_id": method_id,
                "state": "preferred",
                "recommendation": row["recurrence_guard"],
            }
        )
    state_counts = Counter(row["recommendation_state"] for row in ledger["methods"])
    result_counts = Counter(row["result"] for row in ledger["witnesses"])
    ledger["counts"] = {
        "methods": len(ledger["methods"]),
        "witnesses": len(ledger["witnesses"]),
        "state_events": len(ledger["state_events"]),
        "recommendations": len(ledger["recommendations"]),
        "states": {
            state: state_counts.get(state, 0)
            for state in ("candidate", "deprecated", "observed", "preferred", "superseded", "validated")
        },
        "witness_results": {result: result_counts.get(result, 0) for result in ("fail", "pass")},
    }
    ledger["effective_overlay"] = {
        "effective_negatives": COUNTS["effective_negatives"],
        "effective_methods": COUNTS["effective_methods"],
        "failed_witnesses": COUNTS["failed_witnesses"],
        "bounded_passing_witnesses": COUNTS["bounded_passing_witnesses"],
        "repository_seal_rewritten": False,
    }
    ledger["lifecycle"] = "exact_final_candidate"
    ledger["sealed_counts"] = COUNTS
    ledger["terminal_verdict"] = "NOT_READY_FOR_STAGE_20"
    return ledger


def final_overview() -> str:
    planning = (OWNER_ROOT / "x1" / "integrated-overview.md").read_text(encoding="utf-8")
    evidence = (OWNER_ROOT / "x2" / "evidence-overview.md").read_text(encoding="utf-8")
    planning = planning.split("\n", 1)[1] if planning.startswith("# ") else planning
    evidence = evidence.split("\n", 1)[1] if evidence.startswith("# ") else evidence
    return f"""# Elowen Cairn v672-v8 final integrated overview

## Exact lifecycle

Elowen v672-v8 began from immutable Tamar v672-v7 final `{SOURCE_FINAL}`. Planning-only Elowen x1 is `{X1_COMMIT}` and bounded Elowen x2 evidence is `{EVIDENCE_COMMIT}`. Each is a direct single-parent child of its predecessor. X1 and evidence were separately committed, pushed, clean, typed 0/0 divergent, and equal across local, upstream, tracking, and fresh live remote state before the next lifecycle began. This final candidate adds closeout, seal, manifest, validation, and a prepared-but-unsent route candidate only.

## Outcome and retained truth

The declared proposal chain extends from 6,190 to 6,230 rows. The forty Elowen proposals resolve exactly to 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. All 160 preregistered mutations executed and remain rejected at zero completion credit. Twenty-five x1 operational failures, four x2 operational failures, and three closeout failures remain visible with separate bounded recoveries. The closeout failures preserve an oversized combined final-scaffold projection, an atomically rejected patch-context assumption, and a stalled full-tree Git traversal, each with a bounded recovery. No failed witness was erased, rewritten into a pass, or promoted into canonical success.

Effective closeout truth is {COUNTS['effective_negatives']:,} negatives, {COUNTS['effective_methods']:,} Method Flow methods, {COUNTS['failed_witnesses']:,} retained failed witnesses, {COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses, {COUNTS['open_gaps']} open gaps, and {COUNTS['exact_gates']} exact gates. Tamar's sealed 35,967 negatives, 22,262 methods, 7,628 failed witnesses, and 9,825 bounded passes remain unchanged. Tamar's one post-final projection failure and all Elowen additions are carried only as additive overlays.

## Primary pillar and practice scope

Freed ID/CBR Heart is primary through three wholly synthetic music-box documentation lenses: cylinder component and pin-track topology; disc carrier, perforation, drive, label, and storage topology; and orchestral or auxiliary-component relation and timing vacancy. Accessible status, correction, workload, provenance, rights holds, and handover cross all three lenses. GMUT Mind and THOS Body remain explicit and protected. The phase used no real person, participant, collection, music box, cylinder, disc, comb, spring, tune, recording, observation, measurement, playback, treatment, identity event, network data row, external write, professional decision, legal or cultural decision, affected-party approval, or authority act.

Twenty owner-local skills were initialized through the installed official creator, customized, quick-validated, and smoke-used without global installation. Ten family-compatible runners passed. Three substantive tools paired accepting and rejecting fixtures. Sixty safe-now tasks, thirty bounded candidates, and sixty additive CLEAN/FIX/REFINE tasks completed only inside frozen owner-local hypotheses. Twenty exact-approval and ten blocked packets remained unexecuted. Successor recommendations remain zero-credit seeds.

## Evidence boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. No synthetic topology, citation, zero-row adapter, or software guard is a datum, likelihood, posterior, parameter constraint, detected force, prediction, empirical confirmation, stability theorem, quantum completion, ultraviolet completion, final physics, or Theory of Everything. THOS remains participant-free proxy evidence without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live issuance and resolution, status and revocation, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight.

Real conservator, music-mechanism repairer, curator, collector, musicologist, electrical specialist, custodian, affected-user, accessibility, observation, measurement, playback, examination, treatment-outcome, or independent evaluation evidence remains open. Ownership, access, copyright, recording, performance, cultural or sacred context, operation and treatment permission, remedy, legal or cultural interpretation, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.

## Frozen x1 planning narrative

The following planning narrative is copied from the immutable x1 record to keep proposal intent, novelty limits, workflow boundaries, and the wellbeing checkpoint readable in one final packet. It remains planning evidence only; its future-tense language is not substituted for x2 results.

{planning}

## Immutable x2 evidence narrative

The following evidence narrative is copied from the immutable evidence commit. It records the bounded software and synthetic results, retained failures, tool and portfolio scope, and explicit nonpromotion boundaries. Its passing witnesses are same-owner evidence only.

{evidence}

## Validation and route state

The full repository suite was not run or claimed. Owner-scoped tests, strict JSON parsing, exact staged Git blobs, five privacy classes, bounded changed-code checks, diff hygiene, ancestry, commit ceilings, clean state, typed divergence, and fresh equality are same-owner software evidence only. They are not independent reproduction, external audit, complete privacy or accessibility assurance, exhaustive security, professional certification, legal or cultural ratification, Māori-authority review, empirical GMUT confirmation, proof, canon, or Stage 20 authority.

The Sylven Arc v673-v1 activation artifact is `PREPARED_NOT_SENT`. Preparation is not delivery. No task was created, forked, delegated, substituted, or contacted. Only after the exact final is committed, pushed, clean, fresh-live equal, and one canonical aggregate succeeds without replay may the live registry and newest authority be refreshed for one possible acknowledged send.

## Terminal verdict

{IDENTITY_BOUNDARY}

{BOUNDARY}

`NOT_READY_FOR_STAGE_20`
"""


def prepared_baton() -> str:
    return f"""# SYLVEN ARC — PREPARED ELOWEN v672-v8 EXACT FINAL TO PROSPECTIVE v673-v1 ACTIVATION CANDIDATE

`DELIVERY_STATE = PREPARED_NOT_SENT`

Preparation is not delivery. This repository artifact is a sanitized candidate only. It does not prove a live registry match, current route authority, duplicate-guard result, acknowledgement, or delivery. No task identifier, private route, transcript, session stream, credential, screenshot, callable identifier, application state, or private absolute path is included.

Immutable basis after Elowen's final commit:

- Source Tamar v672-v7 final: `{SOURCE_FINAL}`
- Frozen Elowen x1: `{X1_COMMIT}`
- Immutable Elowen evidence: `{EVIDENCE_COMMIT}`
- Exact Elowen final: resolve from the direct child of evidence only after commit and live equality
- Branch: `{BRANCH}`

Outcome truth is exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`, with 6,190 declared frozen proposal rows, {COUNTS['effective_negatives']:,} effective negatives, {COUNTS['effective_methods']:,} methods, {COUNTS['failed_witnesses']:,} failed witnesses, {COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses, {COUNTS['open_gaps']} open gaps, {COUNTS['exact_gates']} exact gates, and `NOT_READY_FOR_STAGE_20`.

Before any repository mutation, Sylven must read the exact committed Elowen packet and independently reverify the branch, anchors, direct-parent history, manifests, clean state, divergence, fresh equality, newest authorization, and current roster. Work solo in a fresh additive Sylven-owned lane; preserve strict x1-before-x2, every retained failure, the four labels, protected gaps and gates, owner-scoped validation, and the one-successful-canonical/no-replay rule. Treat all Elowen proposals, portfolios, tools, skills, runners, receipts, and outcomes only as inherited evidence or zero-credit seeds.

GMUT, THOS, Freed ID, CBR, professional, legal, cultural, affected-party, Māori data governance, and Māori-authority boundaries remain unchanged. Identity and family language is relational working language only.

Prospective delivery is permitted only after Elowen's exact terminal gate, exactly one current exact-title `Sylven Arc` match, immediate bounded reread, duplicate guard, no pause or redirect, and an acknowledged one-send. Stop on absence, ambiguity, standby state, usage exhaustion, acknowledgement failure, or any protected gate. Never create, fork, substitute, precontact, or resend.
"""


def build() -> None:
    if git_text("rev-parse", "HEAD") != EVIDENCE_COMMIT or git_text("branch", "--show-current") != BRANCH:
        raise SystemExit("final build requires the exact pushed Elowen evidence commit and branch")
    gate = verify_evidence_gate()
    outcome = load("x2/outcome-ledger.json")
    flow = load("x2/method-flow-evidence.json")
    mutations = load("x2/mutation-receipt.json")
    phase = load("x2/phase-truth-evidence.json")
    skills = load("x2/skill-evidence.json")
    runners = load("x2/runner-evidence.json")
    tools = load("x2/tool-evidence.json")
    if outcome["counts"] != OUTCOMES or flow["effective_overlay"] != {
        "effective_negatives": EVIDENCE_COUNTS["effective_negatives"],
        "effective_methods": EVIDENCE_COUNTS["effective_methods"],
        "failed_witnesses": EVIDENCE_COUNTS["failed_witnesses"],
        "bounded_passing_witnesses": EVIDENCE_COUNTS["bounded_passing_witnesses"],
        "repository_seal_rewritten": False,
    }:
        raise SystemExit("evidence outcome or count drift")
    final_flow = extend_final_flow(flow)
    failed_rows = [
        {
            "negative_id": witness["retained_negative_ids"][0],
            "method_id": witness["method_id"],
            "failed_witness": witness["observed"],
            "result": "fail",
            "completion_credit": 0,
            "recovery_preserves_failure": True,
        }
        for witness in final_flow["witnesses"]
        if witness["result"] == "fail"
    ]
    open_rows = [row for row in outcome["rows"] if row["observed_outcome"] == "open_gap"]
    exact_rows = [row for row in outcome["rows"] if row["observed_outcome"] == "exact_gate"]
    write_text("closeout/final-integrated-overview.md", final_overview())
    write_json(
        "closeout/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.final.v5",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "final_commit": "DIRECT_CHILD_OF_EVIDENCE_RESOLVES_AFTER_COMMIT",
            "evidence_gate": gate,
            "proposal_chain": 6230,
            "outcomes": OUTCOMES,
            **COUNTS,
            "real_people": 0,
            "real_objects_measurements_rows": 0,
            "external_writes": 0,
            "full_repository_suite": "not_run_not_claimed",
            "same_owner_independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json("closeout/method-flow-final.json", final_flow)
    write_json(
        "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v5",
            "owner": OWNER,
            "phase": PHASE,
            "tamar_repository_seal": {
                "effective_negatives": 35967,
                "effective_methods": 22262,
                "failed_witnesses": 7628,
                "bounded_passing_witnesses": 9825,
            },
            "tamar_external_activation_overlay": {
                "effective_negatives": 35968,
                "effective_methods": 22263,
                "failed_witnesses": 7629,
                "bounded_passing_witnesses": 9826,
            },
            "elowen_evidence": EVIDENCE_COUNTS,
            "elowen_final": COUNTS,
            "phase_failed_witnesses": len(failed_rows),
            "x1_operational_failures": 25,
            "x2_operational_failures": 4,
            "final_operational_failures": 3,
            "mutation_failures": 160,
            "rows": failed_rows,
            "failures_rewritten_as_pass": 0,
        },
    )
    write_json(
        "closeout/exact-open-gate-register.json",
        {
            "schema": "ghc.family.open-exact-gate-register.v5",
            "owner": OWNER,
            "phase": PHASE,
            "open_gap_total": COUNTS["open_gaps"],
            "exact_gate_total": COUNTS["exact_gates"],
            "new_open_gaps": open_rows,
            "new_exact_gates": exact_rows,
            "inherited_open_gaps": COUNTS["open_gaps"] - len(open_rows),
            "inherited_exact_gates": COUNTS["exact_gates"] - len(exact_rows),
            "maori_concepts_remain_under_maori_authority": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/proposal-ledger-final.json",
        {
            "schema": "ghc.family.proposal-ledger.final.v5",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain_before": 6190,
            "proposal_chain_after": 6230,
            "counts": OUTCOMES,
            "rows": outcome["rows"],
            "mutations": {
                "preregistered": mutations["preregistered"],
                "executed": mutations["executed"],
                "rejected": mutations["rejected"],
            },
        },
    )
    write_json(
        "closeout/skill-runner-tool-summary.json",
        {
            "schema": "ghc.family.skill-runner-tool-summary.v2",
            "owner": OWNER,
            "phase": PHASE,
            "skills": {
                "initialized": skills["initialized_with_official_creator"],
                "quick_validated": skills["quick_validated"],
                "smoke_used": skills["smoke_used"],
                "global_install": skills["global_install"],
            },
            "runners": {
                "built": runners["built_new"],
                "executed": runners["executed"],
                "passed": runners["passed"],
            },
            "tools": {"built": len(tools["tools"]), "external_actions": tools["external_actions"]},
            "inherited_completion_credit": 0,
        },
    )
    write_json(
        "closeout/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete-checklist.v5",
            "owner": OWNER,
            "phase": PHASE,
            "complete": [
                "planning-only x1 freeze",
                "bounded synthetic x2 execution",
                "160 retained rejecting mutations",
                "owner-local skills runners and tools",
                "exact staged and Git-blob manifests",
                "prepared unsent route candidate",
            ],
            "incomplete": [
                "real observation or measurement",
                "professional evaluation or treatment authority",
                "participant or affected-user evidence",
                "production identity lifecycle",
                "legal or cultural ratification",
                "Māori authority or Māori data governance",
                "independent reproduction",
                "full repository suite",
                "Stage 20",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.closeout-receipt.v5",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "final_commit_pending": True,
            "phase_commits_after_final": 3,
            "merges_after_final": 0,
            "final_parent_required": EVIDENCE_COMMIT,
            "canonical_invocation_count_before_final": 0,
            "canonical_success_count_before_final": 0,
            "full_repository_suite": "not_run_not_claimed",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/final-wellbeing-check.json",
        {
            "schema": "ghc.family.wellbeing-check.v2",
            "owner": OWNER,
            "phase": PHASE,
            "workload_scope": "bounded owner-local phase",
            "pause_available": True,
            "rollback_available": True,
            "external_pressure_claimed": False,
            "real_worker_assessment": False,
            "professional_health_claim": False,
            "boundary": BOUNDARY,
        },
    )
    write_json("closeout/environment-version-receipt.json", load("x2/environment-receipt.json"))
    write_json("closeout/source-evidence-ledger.json", load("x2/source-evidence-ledger.json"))
    write_text(
        "closeout/accessible-final-report.html",
        (OWNER_ROOT / "x2" / "accessible-evidence-report.html")
        .read_text(encoding="utf-8")
        .replace("bounded evidence", "final bounded evidence")
        .replace("evidence report", "final evidence report"),
    )
    write_json(
        "final/final-validation-prerequisites.json",
        {
            "schema": "ghc.family.final-validation-prerequisites.v2",
            "owner": OWNER,
            "phase": PHASE,
            "required_parent": EVIDENCE_COMMIT,
            "clean_pushed_final_required": True,
            "fresh_four_way_equality_required": True,
            "canonical_invocation_limit": 1,
            "canonical_success_limit": 1,
            "full_repository_suite": "not_authorized_non_eiren",
            "ready_for_canonical_after_commit_push": True,
        },
    )
    write_json(
        "final/canonical-invocation-state.json",
        {
            "schema": "ghc.family.canonical-invocation-state.v2",
            "owner": OWNER,
            "phase": PHASE,
            "state": "NOT_INVOKED_PRECOMMIT",
            "invocation_count": 0,
            "success_count": 0,
            "replay_count": 0,
            "external_receipt": "created only by the one post-push canonical invocation",
        },
    )
    write_json(
        "final/final-validation-candidate-record.json",
        {
            "schema": "ghc.family.final-validation-candidate.v2",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "final_commit": "DIRECT_CHILD_OF_EVIDENCE_RESOLVES_AFTER_COMMIT",
            "branch": BRANCH,
            "counts": COUNTS,
            "outcomes": OUTCOMES,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "seal/content-seal.json",
        {
            "schema": "ghc.family.content-seal.v5",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "final_commit": "DIRECT_CHILD_OF_EVIDENCE_RESOLVES_AFTER_COMMIT",
            "proposal_chain": 6230,
            "outcomes": OUTCOMES,
            **COUNTS,
            "retained_phase_failures": len(failed_rows),
            "failed_witnesses_erased": 0,
            "full_repository_suite": "not_run_not_claimed",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text("handoffs/sylven-arc-v673-v1-activation-candidate.md", prepared_baton())
    write_json(
        "orchestration/route-state-final-candidate.json",
        {
            "schema": "ghc.family.route-state.v5",
            "owner": OWNER,
            "phase": PHASE,
            "prospective_recipient_exact_title": "Sylven Arc",
            "prospective_phase": "v673-v1",
            "delivery_state": "PREPARED_NOT_SENT",
            "successor_contact_count": 0,
            "task_creation_count": 0,
            "fork_count": 0,
            "substitute_endpoint_count": 0,
            "standby_contact_count": 0,
            "required_live_gate": (
                "exact final committed pushed clean fresh-live equal, one successful non-replayed "
                "canonical, newest authority and roster, unique exact title, immediate reread, "
                "duplicate guard, acknowledged one-send"
            ),
        },
    )
    print(
        json.dumps(
            {
                "owner": OWNER,
                "phase": PHASE,
                "source": SOURCE_FINAL,
                "x1": X1_COMMIT,
                "evidence": EVIDENCE_COMMIT,
                "outcomes": OUTCOMES,
                "counts": COUNTS,
                "retained_phase_failures": len(failed_rows),
                "delivery_state": "PREPARED_NOT_SENT",
                "overview_words": len(final_overview().split()),
            },
            sort_keys=True,
        )
    )


def staged_paths() -> list[str]:
    return [
        row
        for row in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()
        if row
    ]


def index_blob_rows(paths: list[str]) -> list[tuple[str, str, bytes]]:
    if not paths:
        return []
    lines = git_text("ls-files", "--stage", "--", *paths).splitlines()
    objects = {}
    for line in lines:
        left, path = line.split("\t", 1)
        mode, object_id, stage = left.split()
        if stage == "0":
            objects[path] = (mode, object_id)
    missing = [path for path in paths if path not in objects]
    if missing:
        raise SystemExit(f"index object mapping missing: {missing}")
    blobs = batch_blobs([objects[path][1] for path in paths])
    rows = []
    for path, blob in zip(paths, blobs, strict=True):
        if blob is None:
            raise SystemExit(f"index blob missing: {path}")
        rows.append((path, objects[path][0], blob))
    return rows


def final_delta_manifest() -> None:
    exclusions = [
        "docs/elowen-cairn/v672-v8/validation/final-delta-manifest.json",
        "docs/elowen-cairn/v672-v8/validation/final-owner-manifest.json",
        "docs/elowen-cairn/v672-v8/validation/final-staged-review.json",
        "docs/elowen-cairn/v672-v8/validation/final-precommit-test-receipt.json",
    ]
    paths = [path for path in staged_paths() if path not in exclusions]
    entries = [
        {"path": path, "mode": mode, "bytes": len(blob), "sha256": sha(blob)}
        for path, mode, blob in index_blob_rows(paths)
    ]
    entries.sort(key=lambda row: row["path"])
    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v5",
            "domain": "final delta exact staged Git blobs before four lifecycle self files",
            "hash_domain": "normalized_lf_exact_git_blob",
            "owner": OWNER,
            "phase": PHASE,
            "source_evidence": EVIDENCE_COMMIT,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
        },
    )


def owner_index_paths() -> list[str]:
    paths = git_text("ls-files").splitlines()
    selected = []
    for path in paths:
        if path.startswith("docs/elowen-cairn/v672-v8/"):
            selected.append(path)
        elif path in RUNNER_PATHS:
            selected.append(path)
        elif re.fullmatch(
            r"(?:scripts|tests)/(?:build_|validate_|test_)?ghc_family_elowen_(?:cairn_)?v672_v8_.+\.py",
            path,
        ):
            selected.append(path)
    return sorted(set(selected))


def final_owner_manifest() -> None:
    exclusions = [
        "docs/elowen-cairn/v672-v8/validation/final-owner-manifest.json",
        "docs/elowen-cairn/v672-v8/validation/final-staged-review.json",
        "docs/elowen-cairn/v672-v8/validation/final-precommit-test-receipt.json",
    ]
    paths = [path for path in owner_index_paths() if path not in exclusions]
    entries = [
        {"path": path, "mode": mode, "bytes": len(blob), "sha256": sha(blob)}
        for path, mode, blob in index_blob_rows(paths)
    ]
    entries.sort(key=lambda row: row["path"])
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v5",
            "domain": "all Elowen v672-v8 owner files in prospective final index",
            "hash_domain": "normalized_lf_exact_git_blob",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
        },
    )


def staged_review() -> None:
    paths = staged_paths()
    allowed_prefixes = (
        "docs/elowen-cairn/v672-v8/closeout/",
        "docs/elowen-cairn/v672-v8/final/",
        "docs/elowen-cairn/v672-v8/seal/",
        "docs/elowen-cairn/v672-v8/handoffs/",
        "docs/elowen-cairn/v672-v8/orchestration/",
    )
    allowed = set(FINAL_CODE_PATHS + FINAL_VALIDATION_PATHS)
    out = [path for path in paths if path not in allowed and not path.startswith(allowed_prefixes)]
    frozen = [
        path
        for path in paths
        if path.startswith(("docs/elowen-cairn/v672-v8/x1/", "docs/elowen-cairn/v672-v8/x2/"))
        or path in RUNNER_PATHS
        or re.search(r"_v672_v8_(?:x1|x2)\.py$", path)
    ]
    payload = {
        "schema": "ghc.family.staged-review.v5",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "final_closeout",
        "staged_before_self": paths,
        "staged_count_before_self": len(paths),
        "out_of_scope": out,
        "frozen_x1_or_evidence_mutations": frozen,
        "declared_lifecycle_self_exclusions": [
            "docs/elowen-cairn/v672-v8/validation/final-delta-manifest.json",
            "docs/elowen-cairn/v672-v8/validation/final-owner-manifest.json",
            "docs/elowen-cairn/v672-v8/validation/final-staged-review.json",
            "docs/elowen-cairn/v672-v8/validation/final-precommit-test-receipt.json",
        ],
        "valid": not out and not frozen,
    }
    write_json("validation/final-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def staged_privacy() -> None:
    self_path = "docs/elowen-cairn/v672-v8/validation/final-staged-privacy.json"
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I
        ),
        "private_route_or_callable": re.compile(
            r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I
        ),
        "credential_assignment": re.compile(
            r"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']",
            re.I,
        ),
        "transcript_or_session_stream": re.compile(
            r"\b(?:session_stream|private_transcript|private_conversation_dump)\b", re.I
        ),
    }
    scanner_surfaces = set(FINAL_CODE_PATHS)
    paths = [
        path
        for path in staged_paths()
        if path != self_path
        and Path(path).suffix.lower() in {".py", ".json", ".md", ".html", ".txt", ".yaml"}
    ]
    candidates = []
    scanned = 0
    for path, _mode, blob in index_blob_rows(paths):
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            candidates.append(
                {"path": path, "pattern_class": "non_utf8_text", "disposition": "confirmed_payload_hit"}
            )
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append(
                    {
                        "path": path,
                        "pattern_class": label,
                        "disposition": (
                            "scanner_definition_or_unit_test"
                            if path in scanner_surfaces
                            else "confirmed_payload_hit"
                        ),
                    }
                )
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    payload = {
        "schema": "ghc.family.staged-privacy-scan.v2",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "final_closeout",
        "hash_domain": "exact_staged_git_blob",
        "pattern_classes": sorted(patterns),
        "scanned_text_files": scanned,
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
        "self_exclusions": [
            self_path,
            "docs/elowen-cairn/v672-v8/validation/final-precommit-test-receipt.json",
        ],
        "valid": not confirmed,
        "boundary": "Scanner definitions and synthetic test strings are candidates; every other match fails closed.",
    }
    write_json("validation/final-staged-privacy.json", payload)
    if confirmed:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def validation_receipt() -> None:
    json_paths = sorted(OWNER_ROOT.rglob("*.json"))
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            json_issues.append(
                {"path": path.relative_to(ROOT).as_posix(), "issue": type(exc).__name__}
            )
    docs = [
        path
        for path in OWNER_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}
    ]
    stale_patterns = {
        "prior_tamar_heritage": re.compile(
            r"stained[-_ ]glass|lead[-_ ]came|dry[-_ ]stone|ornamental[-_ ]plaster", re.I
        ),
        "prior_calculator_domain": re.compile(
            r"mechanical[-_ ]calculator|stepped[-_ ]drum|pinwheel|accumulator|crank[-_ ]turn",
            re.I,
        ),
        "rejected_typewriter_domain": re.compile(r"\btypewriter\b", re.I),
        "owner_name_typo": re.compile(r"\bElowen Venn\b"),
    }
    semantic_neighbor_paths = {
        "docs/elowen-cairn/v672-v8/x1/method-flow-startup.json",
        "docs/elowen-cairn/v672-v8/x1/semantic-neighbor-audit.json",
        "docs/elowen-cairn/v672-v8/x1/integrated-overview.md",
        "docs/elowen-cairn/v672-v8/closeout/final-integrated-overview.md",
    }
    inherited_source_paths = {
        "docs/elowen-cairn/v672-v8/x1/semantic-neighbor-audit.json",
        "docs/elowen-cairn/v672-v8/x1/integrated-overview.md",
        "docs/elowen-cairn/v672-v8/x1/inherited-proposal-revalidation.json",
        "docs/elowen-cairn/v672-v8/closeout/final-integrated-overview.md",
    }
    stale_candidates = []
    for path in docs:
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for label, pattern in stale_patterns.items():
            matches = pattern.findall(text)
            if matches:
                semantic_neighbor = (
                    label in {"prior_calculator_domain", "rejected_typewriter_domain"}
                    and relative in semantic_neighbor_paths
                )
                inherited_source = (
                    label == "prior_tamar_heritage" and relative in inherited_source_paths
                )
                stale_candidates.append(
                    {
                        "path": relative,
                        "label": label,
                        "occurrences": len(matches),
                        "disposition": (
                            "semantic_neighbor_reference"
                            if semantic_neighbor
                            else "inherited_source_reference"
                            if inherited_source
                            else "unexpected_stale_label"
                        ),
                    }
                )
    unexpected_stale = [
        row for row in stale_candidates if row["disposition"] == "unexpected_stale_label"
    ]
    max_words = max(
        (len(path.read_text(encoding="utf-8").split()) for path in docs), default=0
    )
    python_paths = [
        path
        for path in (ROOT / "scripts").glob("*elowen*v672*v8*.py")
    ] + [path for path in (ROOT / "tests").glob("*elowen*v672*v8*.py")] + [
        ROOT / path for path in RUNNER_PATHS
    ]
    python_paths = sorted(set(python_paths))
    compile_issues = []
    for path in python_paths:
        try:
            compile(path.read_text(encoding="utf-8"), path.name, "exec")
        except SyntaxError as exc:
            compile_issues.append(
                {"path": path.relative_to(ROOT).as_posix(), "issue": str(exc)}
            )
    diff = git("diff", "--cached", "--check", check=False)
    frozen = git_text(
        "diff",
        "--name-only",
        EVIDENCE_COMMIT,
        "--",
        "docs/elowen-cairn/v672-v8/x1",
        "docs/elowen-cairn/v672-v8/x2",
        "scripts/build_ghc_family_elowen_cairn_v672_v8_x1.py",
        "scripts/build_ghc_family_elowen_cairn_v672_v8_x2.py",
        "tests/test_ghc_family_elowen_cairn_v672_v8_x1.py",
        "tests/test_ghc_family_elowen_cairn_v672_v8_x2.py",
        *RUNNER_PATHS,
    )
    materialized = len(
        [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    )
    payload = {
        "schema": "ghc.family.final-validation-receipt.v2",
        "owner": OWNER,
        "phase": PHASE,
        "json_documents": len(json_paths),
        "json_issues": json_issues,
        "documents": len(docs),
        "max_document_words": max_words,
        "document_word_guard": 100000,
        "stale_label_candidates": stale_candidates,
        "stale_label_unexpected": unexpected_stale,
        "stale_label_review_valid": not unexpected_stale,
        "python_compiles": len(python_paths),
        "python_compile_issues": compile_issues,
        "diff_hygiene_exit": diff.returncode,
        "frozen_x1_or_evidence_changes": frozen.splitlines() if frozen else [],
        "materialized_files": materialized,
        "file_guard": 2000,
        "full_repository_suite": "not_run_not_claimed",
        "valid": (
            not json_issues
            and not compile_issues
            and not unexpected_stale
            and diff.returncode == 0
            and not frozen
            and materialized < 2000
            and max_words < 100000
        ),
        "boundary": BOUNDARY,
    }
    write_json("validation/final-validation-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def precommit_test_receipt() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "tests.test_ghc_family_elowen_cairn_v672_v8_final",
            "-v",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )
    combined = result.stdout + result.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests", combined)
    tests = int(match.group(1)) if match else 0
    payload = {
        "schema": "ghc.family.final-precommit-test-receipt.v2",
        "owner": OWNER,
        "phase": PHASE,
        "tests": tests,
        "exit_code": result.returncode,
        "result": "passed" if result.returncode == 0 else "failed",
        "output_sha256": sha(combined.encode("utf-8")),
        "x1_tests_rerun": False,
        "x2_tests_rerun": False,
        "full_repository_suite": "not_run_not_claimed",
        "same_owner_only": True,
        "independent_reproduction": False,
        "valid": result.returncode == 0 and tests == EXPECTED_FINAL_TESTS,
        "boundary": BOUNDARY,
    }
    write_json("validation/final-precommit-test-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--delta-manifest", action="store_true")
    parser.add_argument("--owner-manifest", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--staged-privacy", action="store_true")
    parser.add_argument("--validation-receipt", action="store_true")
    parser.add_argument("--precommit-test-receipt", action="store_true")
    args = parser.parse_args()
    if args.delta_manifest:
        final_delta_manifest()
    elif args.owner_manifest:
        final_owner_manifest()
    elif args.staged_review:
        staged_review()
    elif args.staged_privacy:
        staged_privacy()
    elif args.validation_receipt:
        validation_receipt()
    elif args.precommit_test_receipt:
        precommit_test_receipt()
    else:
        build()


if __name__ == "__main__":
    main()
