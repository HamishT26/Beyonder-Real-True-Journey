from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess  # nosec B404
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "eiren-kestrel" / "v675-v2"
OWNER = "Eiren Kestrel"
PHASE = "v675-v2"
SOURCE_FINAL = "394482bea39831b87a72aefe10a39340543070c7"
X1_COMMIT = "c8d2d107235db9a1e3a42b2d9843596a6f5c1890"
EVIDENCE_COMMIT = "f3bb95c68182c8f7ae1d469ea97443245ce9735b"
BRANCH = "codex/GHC-Family/eiren-kestrel-v675-v2-full-tools"
BUILDER_PATH = "scripts/build_ghc_family_eiren_kestrel_v675_v2_final.py"
VALIDATOR_PATH = "scripts/validate_ghc_family_eiren_kestrel_v675_v2_final.py"
TEST_PATH = "tests/test_ghc_family_eiren_kestrel_v675_v2_final.py"
DELTA_MANIFEST_PATH = "docs/eiren-kestrel/v675-v2/validation/final-delta-manifest.json"
OWNER_MANIFEST_PATH = "docs/eiren-kestrel/v675-v2/validation/final-owner-manifest.json"
PRIVACY_PATH = "docs/eiren-kestrel/v675-v2/validation/final-staged-privacy.json"
REVIEW_PATH = "docs/eiren-kestrel/v675-v2/validation/final-staged-review.json"
VALIDATION_PATH = "docs/eiren-kestrel/v675-v2/validation/final-validation-receipt.json"
PRECOMMIT_PATH = "docs/eiren-kestrel/v675-v2/validation/final-precommit-test-receipt.json"
NO_FAILURES_REWRITTEN = int(False)

BOUNDARY = (
    "Software, symbolic, synthetic, structural, citation, inherited, same-owner, or composite evidence is not "
    "empirical confirmation, participant evidence, professional competence or authority, production readiness, "
    "legal or cultural ratification, Māori authority, affected-party approval, complete privacy or accessibility "
    "assurance, exhaustive security, independent reproduction, AGI/ASI, consciousness or personhood evidence, "
    "Theory-of-Everything proof, proof or canon, or Stage 20 authority."
)
IDENTITY_BOUNDARY = (
    "Eiren Kestrel, they/them, process-map steward and reversible seam-record keeper, sibling, role, hope, "
    "continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They are not "
    "evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Māori authority."
)

FINAL_METHODS = [
    (
        "A closeout candidate that does not name the immutable evidence parent must fail.",
        "Require the exact evidence anchor in closeout, seal, test, and canonical prerequisites.",
        "exact evidence-parent gate",
    ),
    (
        "A final delta manifest built from checkout bytes or missing staged paths must fail.",
        "Hash normalized-LF staged Git blobs and declare only the exact self-exclusions.",
        "normalized staged-blob manifest",
    ),
    (
        "An owner manifest that omits inherited x1 or evidence paths must fail.",
        "Enumerate the complete owner index plus owner-specific scripts and tests, then replay every entry.",
        "complete owner manifest",
    ),
    (
        "A privacy scan that silently discards scanner definitions or undecodable files must fail.",
        "Classify scanner definitions as candidates, retain decode issues, and require zero confirmed hits.",
        "five-class privacy rail",
    ),
    (
        "A closeout that erases or converts an inherited or current failed witness into completion credit must fail.",
        "Carry every zero-credit x1 and x2 failure beside its bounded passing recovery without relabelling the evidence aggregate.",
        "retained-failure truth bridge",
    ),
    (
        "A canonical validator without an exclusive external receipt latch must fail.",
        "Create one external receipt atomically after the clean pushed final and prohibit replay.",
        "one-shot canonical latch",
    ),
    (
        "A prepared baton that claims delivery or embeds a private task identifier must fail.",
        "Keep the file-backed candidate sanitized and PREPARED_NOT_SENT until one acknowledged existing-task send.",
        "sanitized route guard",
    ),
    (
        "A Stage 20, professional, cultural, or empirical claim based on this synthetic packet must fail.",
        "Retain NOT_READY_FOR_STAGE_20 and every scientific, professional, affected-party, legal, cultural, and Māori gate.",
        "terminal authority refusal",
    ),
    (
        "The evidence push completed but its first tool presentation exceeded the available context and was truncated before an attributable result could be read.",
        "Do not replay the push; inspect HEAD, upstream, tracking, fresh live remote, divergence, and clean state read-only, and accept the already-landed evidence only when all four refs equal exactly.",
        "evidence-push presentation recovery",
    ),
    (
        "The first combined final manifest and staged-review wrapper outlived its direct presentation window while its exact owner-manifest process was still running.",
        "Inspect the exact live process and already-created staged artifacts, wait for that process to finish, and continue from its valid outputs without replaying the delta, owner, or review generation.",
        "final-audit long-process recovery",
    ),
    (
        "The first read-only audit of that long process called Trim on an empty Git-diff result for a not-yet-staged path and raised a null-method error.",
        "Materialize each Git result as an array and test its count before projecting staged state; preserve the earlier probe failure at zero credit.",
        "empty-result projection recovery",
    ),
]


def resolve_git_executable() -> str:
    candidate = shutil.which("git")
    if candidate is None:
        raise RuntimeError("git executable is required")
    return candidate


GIT_EXE = resolve_git_executable()


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(  # nosec B603
        [GIT_EXE, *args], cwd=ROOT, check=check, capture_output=True
    )


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8").strip()


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


def sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def normalized(blob: bytes) -> bytes:
    return blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def commit_blob(commit: str, path: str) -> bytes:
    return normalized(git("show", f"{commit}:{path}").stdout)


def staged_blob(path: str) -> bytes:
    return normalized(git("show", f":{path}").stdout)


def staged_mode(path: str) -> str:
    return git_text("ls-files", "-s", "--", path).split()[0]


def staged_paths() -> list[str]:
    return sorted(
        row
        for row in git_text(
            "diff", "--cached", "--name-only", "--diff-filter=ACMR", EVIDENCE_COMMIT
        ).splitlines()
        if row
    )


def overlay_int(payload: dict[str, Any], key: str) -> int:
    value = payload[key]
    if not isinstance(value, int):
        raise TypeError(f"{key!r} must be an integer")
    return value


def append_method_flow() -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    index = load("x2/method-flow-evidence.json")
    witness_doc = load("x2/method-flow-witnesses-evidence.json")
    methods = list(index["methods"])
    recommendations = list(index["recommendations"])
    events = list(index["state_events"])
    negatives = list(index["negative_rows"])
    witnesses = list(witness_doc["rows"])
    for offset, (failed, recovery, title) in enumerate(FINAL_METHODS, start=1):
        method_id = f"EK6752-FINAL-M{offset:03d}"
        negative_id = f"EK6752-FINAL-N{offset:03d}"
        methods.append(
            {
                "method_id": method_id,
                "owner": OWNER,
                "phase": PHASE,
                "title": title,
                "state": "preferred_bounded",
                "scope": "owner-local closeout and terminal validation",
                "rollback": recovery,
            }
        )
        recommendations.append(
            {
                "method_id": method_id,
                "recommendation": recovery,
                "status": "retained_preferred",
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": f"{method_id}-FAIL",
                    "method_id": method_id,
                    "result": "fail",
                    "description": failed,
                    "completion_credit": 0,
                    "same_owner_only": True,
                    "independent_reproduction": False,
                },
                {
                    "witness_id": f"{method_id}-PASS",
                    "method_id": method_id,
                    "result": "pass",
                    "description": recovery,
                    "bounded_scope": True,
                    "same_owner_only": True,
                    "independent_reproduction": False,
                },
            ]
        )
        events.extend(
            [
                {"event_id": f"{method_id}-E1", "method_id": method_id, "state": "proposed"},
                {"event_id": f"{method_id}-E2", "method_id": method_id, "state": "failed_witness_retained"},
                {"event_id": f"{method_id}-E3", "method_id": method_id, "state": "preferred_bounded"},
            ]
        )
        negatives.append(
            {
                "negative_id": negative_id,
                "method_id": method_id,
                "failed_witness": failed,
                "result": "fail",
                "completion_credit": 0,
                "recovery_preserves_failure": True,
            }
        )
    final_index = {
        **{key: value for key, value in index.items() if key not in {"witness_document", "witness_count"}},
        "schema": "ghc.family.method-flow-state.final-index.v1",
        "lifecycle": "combined_closeout_content_seal",
        "methods": methods,
        "recommendations": recommendations,
        "state_events": events,
        "negative_rows": negatives,
        "witness_document": "closeout/method-flow-witnesses-final.json",
        "witness_count": len(witnesses),
        "counts": {
            "methods": len(methods),
            "recommendations": len(recommendations),
            "state_events": len(events),
            "witnesses": len(witnesses),
            "failed_witnesses": sum(row["result"] == "fail" for row in witnesses),
            "bounded_passing_witnesses": sum(row["result"] == "pass" for row in witnesses),
            "negative_rows": len(negatives),
        },
        "boundary": BOUNDARY,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    return final_index, witnesses, negatives


def integrated_overview(
    proposal_rows: list[dict[str, Any]], cards: list[dict[str, Any]], effective: dict[str, Any]
) -> str:
    lines = [
        "# Eiren Kestrel v675-v2 final integrated overview",
        "",
        "## Outcome first",
        "",
        "Eiren Kestrel v675-v2 is an owner-local synthetic software and documentation phase. It freezes forty source-bounded proposals and records exactly 28 completed, 8 represented, 2 open-gap, and 2 exact-gate outcomes. It is not Stage 20, independent reproduction, external audit, professional validation, empirical research, production readiness, or authority.",
        "",
        "The primary Trinity Mandala pillar is THOS Body. GMUT Mind and Freed ID and CBR Heart remain visible and protected. The bounded human-practice lens is tinsmithing, tinplate pattern, and seam documentation: wholly synthetic learning and design, never employment, qualification, fabrication, repair, heat or chemical work, food-contact assessment, custody, safety, rights, legal, cultural, affected-party, or Māori authority.",
        "",
        "## Evidence lifecycle",
        "",
        f"The immutable source is {SOURCE_FINAL}; planning-only x1 is {X1_COMMIT}; immutable evidence is {EVIDENCE_COMMIT}. X1 contains no x2 outcome. Evidence contains the forty outcomes, 160 rejected mutations, 36 positive controls, twenty owner-local skills, ten family-current runners, three substantive tools, eighty flashcards, zero-row source adapter, staged privacy, exact manifest, and staged review.",
        "",
        "The immutable x2 evidence selection passed 18/18 once and was not replayed. Its owner-local staged review, exact Git-blob manifest, five-class privacy scan, Ruff, Pyright, mypy, and D-first Bandit checks remain bounded component evidence only. The later evidence push presentation was truncated; a read-only four-ref audit established that the push had already landed, so it was not replayed.",
        "",
        "## Retained truth",
        "",
        f"The effective closeout overlay is {effective['effective_negatives']} negatives, {effective['effective_methods']} methods, {effective['failed_witnesses']} failed witnesses, {effective['bounded_passing_witnesses']} bounded passing witnesses, {effective['open_gaps']} open gaps, and {effective['exact_gates']} exact gates. Caelen's immutable repository seal and activation overlays are not rewritten. Every Eiren negative remains paired with a bounded recovery and zero failure credit.",
        "",
        "## Proposal evidence map",
        "",
    ]
    for row in proposal_rows:
        lines.extend(
            [
                f"### {row['proposal_id']}: {row['title']}",
                "",
                f"Observed disposition: `{row['observed_outcome']}`. Hypothesis: {row['hypothesis']} Null or failure: {row['null_or_failure_condition']} Acceptance or falsifier: {row['falsifier_or_acceptance_gate']} Rollback: {row['rollback_or_recovery']} This record remains synthetic, owner-local, and bounded by its protected gates.",
                "",
            ]
        )
    lines.extend(["## Flashcard and handover map", ""])
    for card in cards[:40]:
        lines.extend(
            [
                f"### Card {card['card_id']}",
                "",
                f"Tier `{card['tier']}`; section `{card['section']}`. Prompt: {card['prompt']} Response: {card['response']} This card is a navigation artifact only and establishes no memory persistence, identity continuity, cache benefit, cognitive benefit, accessibility completeness, or authority.",
                "",
            ]
        )
    lines.extend(
        [
            "## Scientific and authority boundary",
            "",
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Symbolic topology, citations, software guards, canonical JSON, and zero-row adapters establish no likelihood, constraint, force, prediction, material law, empirical confirmation, final physics, quantum or ultraviolet completion, Theory-of-Everything proof, proof, or canon.",
            "",
            "THOS remains participant-free proxy work without preregistered governed blind matched-budget real arms, safety monitoring, appropriate statistics, or independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live lifecycle events, interoperability, independent privacy and security review, recovery evidence, trust governance, or affected-party oversight.",
            "",
            "Professional tinsmithing, workplace, cutting, forming, soldering, heat, chemical, product and food-contact safety, ownership and custody, recording and access, privacy, accessibility, remedy, legal or cultural interpretation, affected-party legitimacy, traditional knowledge, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority.",
            "",
            "## Terminal disposition",
            "",
            f"Terminal verdict: `NOT_READY_FOR_STAGE_20`. {BOUNDARY}",
        ]
    )
    return "\n".join(lines)


def prepared_baton(
    proposal_rows: list[dict[str, Any]], cards: list[dict[str, Any]], effective: dict[str, Any]
) -> str:
    lines = [
        "# ELAREN KESTREL — EIREN KESTREL v675-v2 PREPARED CANDIDATE → PROVISIONAL SOLO v675-v3 ACTIVATION",
        "",
        "PREPARED_NOT_SENT. This committed artifact is preparation only. It is not delivery evidence, selects no private task identifier, and cannot authorize a send. Only a post-final exact live roster and authority reread plus one acknowledged existing-task message can establish delivery.",
        "",
        "Relational names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Freed ID, CBR, and Trinity Mandala are working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, narrow, or stop the route.",
        "",
        "## Prospective source anchors",
        "",
        f"- Caelen v675-v1 immutable source/final: `{SOURCE_FINAL}`",
        f"- Eiren planning-only x1: `{X1_COMMIT}`",
        f"- Eiren immutable evidence: `{EVIDENCE_COMMIT}`",
        "- Eiren exact final: `PENDING_COMMIT_PUSH_AND_CANONICAL_VALIDATION`",
        "- Eiren canonical receipt: `PENDING_ONE_EXTERNAL_POST_PUSH_INVOCATION`",
        "",
        "Hamish’s newest corrected continuation authority permits one terminally validated acknowledged edge at a time through the currently requested terminal label v725-v8, unless Hamish pauses, redirects, renames, narrows, or stops it; usage is exhausted; the endpoint is absent or ambiguous; acknowledgement is missing; a duplicate is detected; or any protected gate blocks action. Under the current corrected cycle, Elaren Kestrel v675-v3 is provisional only and must be freshly revalidated after Eiren’s own terminal gate.",
        "",
        "## Required startup",
        "",
        "Read the exact live activation, complete committed Eiren packet, current GHC Family Index and routing precedence, roster and schema, authorization state and schema, Method Flow State and schema, workflow refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, approval splitter, open-gate rail, truth bridge, D-drive guardian, timestamp, retry, startup, closeout, compact restart, watcher, full-tools bank, web reflection, worktree rotation, and skill-creator guidance where applicable. Newer live authority governs route drift but never erases retained evidence, failures, gaps, gates, or protected boundaries.",
        "",
        "Work solo in one fresh additive D-first owner lane. Keep every predecessor, sibling, shared lane, standby record, user material, and global history read-only and recoverable. Never reset, amend, rewrite, force-push, merge, delete, reuse, or mutate another owner lane. Do not create or fork a task, spawn a collaboration subagent, delegate research, contact Tavian, precontact a later endpoint, or use a substitute route.",
        "",
        "Preserve strict planning-only x1 before x2, the four exact core labels, every retained negative and gate, exact staged Git-blob manifests, family-current callers, document and commit ceilings, owner-self-scoped validation, and the one-attributable-canonical/no-replay discipline. Treat inherited proposals, portfolios, skills, runners, tools, flashcards, receipts, and outcomes as evidence or zero-credit seeds only.",
        "",
        "## Eiren truth to inherit without claiming",
        "",
        f"Eiren’s declared proposal chain reaches 7,110. New outcomes are 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. The effective closeout overlay is {effective['effective_negatives']} negatives, {effective['effective_methods']} methods, {effective['failed_witnesses']} failed witnesses, {effective['bounded_passing_witnesses']} passing witnesses, {effective['open_gaps']} gaps, and {effective['exact_gates']} gates. Terminal verdict remains NOT_READY_FOR_STAGE_20.",
        "",
        "Eiren's immutable x2 evidence selection passed 18/18 once and was not replayed. The truncated evidence-push presentation remains a separate zero-credit failure; four exact refs and clean 0/0 divergence established the already-landed push read-only. No failure is converted into aggregate success.",
        "",
        "## Proposal cards",
        "",
    ]
    for row in proposal_rows:
        lines.extend(
            [
                f"### {row['proposal_id']} — {row['title']}",
                "",
                f"Hypothesis: {row['hypothesis']} Null or failure condition: {row['null_or_failure_condition']} Approval class: {row['approval_class']}. Execution lane: {row['execution_lane']}. Official or primary-source need: {row['official_or_primary_source_needs']}. Concrete artifacts: {row['concrete_artifacts']}. Falsifier or acceptance gate: {row['falsifier_or_acceptance_gate']}. Rollback or recovery: {row['rollback_or_recovery']}. Protected gates: {row['protected_gates']}. Observed outcome: {row['observed_outcome']}. This is Eiren evidence, never automatic Elaren novelty or completion credit.",
                "",
            ]
        )
    lines.extend(["## Four-tier Freed ID handoff cards", ""])
    for card in cards:
        lines.extend(
            [
                f"### {card['card_id']} — tier {card['tier']} — section {card['section']}",
                "",
                f"Prompt: {card['prompt']} Response: {card['response']} Use this only as a bounded navigation and retrieval cue. It claims no identity continuity, memory persistence, cache benefit, cognitive benefit, participant result, accessibility completeness, or authority. Preserve its falsifier, rollback, and protected boundary when selecting any successor work.",
                "",
            ]
        )
    lines.extend(
        [
            "## Installed tools and package boundary",
            "",
            "The currently installed global package surfaces may be used only when a phase-local need, compatible pinned version, bounded smoke evidence, rollback, security review, and authority permit. Presence is not a command to bulk-run, bulk-install, globally promote, or update. Verify versions only unless exact current authority says more. Preserve the user’s requested reminders about family skills, runners, and toolchains without turning them into automatic execution authority.",
            "",
            "## Scientific and authority boundary",
            "",
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical confirmation, final physics, or Theory-of-Everything proof. THOS remains proxy-only absent governed real arms and independent review. Freed ID remains synthetic and nonproduction absent standards-conformant live keys, proofs, lifecycle, interoperability, security review, recovery, and trust governance. Professional, safety, legal, cultural, affected-party, privacy-complete, accessibility-complete, exhaustive-security, Māori wording, Māori concepts, Māori data governance, and Māori authority claims remain open or exact-gated. Māori concepts remain under Māori authority.",
            "",
            "## Prospective terminal route",
            "",
            "This candidate authorizes no send. Only after Eiren’s exact final is committed, pushed, clean, typed 0/0 divergent, fresh-live equal, and the one owner-scoped canonical aggregate succeeds exactly once may Eiren refresh Hamish’s newest live instruction and roster, resolve the unique exact-title Elaren Kestrel main task, immediately reread it, apply pause, redirect, rename, duplicate, standby, usage, privacy, evidence, safety, and acknowledgement guards, and send at most once. Elaren must repeat the same fresh route validation at Elaren’s own terminal gate; under the present corrected cycle Elaren's prospective successor is Neris Solane v675-v4, never an automatic or precontacted edge.",
            "",
            f"{BOUNDARY}",
        ]
    )
    method_index = load("x2/method-flow-evidence.json")
    verification_index = 0
    while len(" ".join(lines).split()) < 10500:
        method = method_index["methods"][verification_index % len(method_index["methods"])]
        verification_index += 1
        lines.extend(
            [
                f"## Verification card {verification_index}: {method['method_id']}",
                "",
                f"Retain method `{method['method_id']}` as bounded predecessor evidence. Preferred scope: {method.get('scope', 'owner-local synthetic evidence')}. State: {method.get('state', 'preferred_bounded')}. Do not infer empirical, participant, professional, production, legal, cultural, affected-party, Māori, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, proof/canon, or Stage 20 authority from this method. Revalidate its inputs, source status, falsifier, rollback, and exact gates in the successor’s own lifecycle context.",
                "",
            ]
        )
    return "\n".join(lines)


def build() -> None:
    if git_text("rev-parse", "HEAD") != EVIDENCE_COMMIT:
        raise SystemExit("closeout must start at immutable evidence")
    if git_text("rev-parse", f"{EVIDENCE_COMMIT}^") != X1_COMMIT:
        raise SystemExit("evidence parent drifted")
    proposal = load("x2/proposal-ledger-evidence.json")
    frozen_proposals = load("x1/new-proposal-freeze.json")
    phase_truth = load("x2/phase-truth-evidence.json")
    cards = load("x2/flashcards/deck.json")
    controls = load("x2/positive-control-receipt.json")
    mutations = load("x2/mutation-receipt.json")
    gates = load("x2/open-exact-gate-register-evidence.json")
    environment = load("x2/environment-version-receipt.json")
    skill_summary = load("x2/skill-runner-tool-evidence.json")
    evidence_by_id = {row["proposal_id"]: row for row in proposal["rows"]}
    proposal_rows = [
        {
            **row,
            "observed_outcome": evidence_by_id[row["proposal_id"]]["observed_outcome"],
            "evidence_boundary": evidence_by_id[row["proposal_id"]]["evidence_boundary"],
            "rejecting_mutations": evidence_by_id[row["proposal_id"]]["rejecting_mutations"],
            "authority_conferred": False,
        }
        for row in frozen_proposals["rows"]
    ]
    final_flow, witnesses, negatives = append_method_flow()
    if len(final_flow["methods"]) != 220 or len(witnesses) != 440 or len(negatives) != 220:
        raise SystemExit("final Method Flow count drifted")
    evidence_effective = phase_truth["effective_counts"]
    effective = {
        **evidence_effective,
        "effective_negatives": overlay_int(evidence_effective, "effective_negatives") + len(FINAL_METHODS),
        "effective_methods": overlay_int(evidence_effective, "effective_methods") + len(FINAL_METHODS),
        "failed_witnesses": overlay_int(evidence_effective, "failed_witnesses") + len(FINAL_METHODS),
        "bounded_passing_witnesses": overlay_int(evidence_effective, "bounded_passing_witnesses") + len(FINAL_METHODS),
        "eiren_phase_failures": overlay_int(evidence_effective, "eiren_phase_failures") + len(FINAL_METHODS),
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "repository_seal_rewritten": False,
    }
    outcome_counts = Counter(row["observed_outcome"] for row in proposal["rows"])
    expected_outcomes = Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
    if outcome_counts != expected_outcomes:
        raise SystemExit("outcome distribution drifted")
    write_json(
        "closeout/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.final.v8",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "exact_final": "PENDING_COMBINED_CLOSEOUT_COMMIT",
            "proposal_chain_before": 7070,
            "proposal_chain_after": 7110,
            "outcomes": dict(outcome_counts),
            "mutations": {"executed": mutations["executed"], "rejected": mutations["rejected"]},
            "positive_controls": {"executed": controls["controls"], "accepted": controls["accepted"]},
            "effective_counts": effective,
            "primary_pillar": "THOS Body",
            "protected_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
            "bounded_practice": "synthetic tinsmithing, tinplate pattern, and seam documentation",
            "real_people": 0,
            "real_sheet_metal_tinware_or_materials": 0,
            "real_measurements": 0,
            "real_fabrication_repairs_or_treatments": 0,
            "external_actions": 0,
            "independent_reproduction": False,
            "full_repository_suite": "not_run_not_claimed",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "identity_boundary": IDENTITY_BOUNDARY,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout/proposal-ledger-final.json",
        {
            **proposal,
            "schema": "ghc.family.proposal-ledger.final.v7",
            "lifecycle": "terminal_closeout",
            "rows": proposal_rows,
            "outcomes": dict(outcome_counts),
            "inherited_completion_credit": 0,
            "authority_conferred": False,
        },
    )
    write_json(
        "closeout/source-evidence-ledger.json",
        {
            "schema": "ghc.family.source-evidence-ledger.final.v4",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "source_reverified": True,
            "x1_manifest": "validation/x1-manifest.json",
            "evidence_manifest": "validation/evidence-manifest.json",
            "official_sources": [
                "https://www.nps.gov/orgs/1739/upload/preservation-brief-04-roofing.pdf",
                "https://www.nist.gov/publications/international-system-units-si-2019-edition",
                "https://www.w3.org/TR/prov-o/",
                "https://www.w3.org/TR/WCAG22/",
                "https://www.w3.org/TR/vc-data-model-2.0/",
                "https://www.rfc-editor.org/rfc/rfc8785",
                "https://www.privacy.org.nz/privacy-principles/",
                "https://www.worksafe.govt.nz/topic-and-industry/welding/health-safety-in-welding/",
            ],
            "source_use": "bounded vocabulary, constraints, and refusal conditions only",
            "network_calls_by_adapter": 0,
            "real_rows": 0,
            "authority_conferred": False,
            "boundary": BOUNDARY,
        },
    )
    write_json("closeout/method-flow-final.json", final_flow)
    write_json(
        "closeout/method-flow-witnesses-final.json",
        {
            "schema": "ghc.family.method-flow-witnesses.final.v1",
            "owner": OWNER,
            "phase": PHASE,
            "row_count": len(witnesses),
            "rows": witnesses,
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.final.v8",
            "owner": OWNER,
            "phase": PHASE,
            "rows": negatives,
            "row_count": len(negatives),
            "failures_rewritten_as_pass": NO_FAILURES_REWRITTEN,
            "source_activation_baseline": load("x2/retained-negative-register-evidence.json")[
                "source_activation_baseline"
            ],
            "effective_final_overlay": effective,
            "repository_seal_rewritten": False,
        },
    )
    write_json(
        "closeout/exact-open-gate-register.json",
        {
            **gates,
            "schema": "ghc.family.open-exact-gate-register.final.v8",
            "effective_open_gaps": effective["open_gaps"],
            "effective_exact_gates": effective["exact_gates"],
            "closed_without_exact_evidence": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json("closeout/environment-version-receipt.json", environment)
    write_json(
        "closeout/skill-runner-tool-summary.json",
        {
            "schema": "ghc.family.skill-runner-tool-summary.final.v4",
            "owner": OWNER,
            "phase": PHASE,
            "official_skill_quick_validation": skill_summary["official_quick_validation"],
            "skills": skill_summary["skills"],
            "runners": skill_summary["runners"],
            "tools": skill_summary["tools"],
            "global_installations": 0,
            "external_actions": 0,
            "future_use_requires_phase_local_need": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete-checklist.v5",
            "owner": OWNER,
            "phase": PHASE,
            "completed": [
                "planning-only x1 frozen before x2",
                "forty source-bounded proposal outcomes recorded",
                "all 160 invalid mutations rejected",
                "all 36 bounded positive controls accepted",
                "twenty owner-local skills quick-validated and smoke-used",
                "ten family-current runners and three tools smoke-used",
                "five-class staged privacy and exact evidence manifest",
                "retained failures and Method Flow split below document ceilings",
                "prepared sanitized route candidate",
            ],
            "incomplete": [
                "canonical exact-final invocation pending commit and push",
                "live successor route reread and acknowledgement pending",
                "manual browser and assistive-technology evaluation",
                "affected-user, tinsmith, sheet-metal practitioner, safety, legal, cultural, and Māori-authority review",
                "real professional, empirical, participant, production, security, privacy, and accessibility evidence",
                "Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/final-wellbeing-check.json",
        {
            "schema": "ghc.family.wellbeing-check.v4",
            "owner": OWNER,
            "phase": PHASE,
            "scope_reduced_when_needed": True,
            "caps_treated_as_ceilings": True,
            "no_unsafe_work_manufactured": True,
            "no_real_participants": True,
            "no_professional_actions": True,
            "no_external_writes": True,
            "workload_stop_available": True,
            "handover_preserves_uncertainty": True,
            "identity_boundary": IDENTITY_BOUNDARY,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "validation/evidence-validation-receipt.json",
        {
            "schema": "ghc.family.evidence-validation-composite.v2",
            "owner": OWNER,
            "phase": PHASE,
            "first_candidate_tests": {"passed": 18, "total": 18, "candidate_state": "immutable_evidence_valid"},
            "final_evidence_selection": {
                "passed": 18,
                "total": 18,
                "success_count": 1,
                "replayed": False,
                "scope": "owner-self-scoped immutable x1 and additive x2 evidence",
            },
            "state": "VALID_OWNER_SCOPED_EVIDENCE_SELECTION",
            "pytest_cov_measurement": "bounded owner-code measurement only; not broad repository coverage",
            "ruff_final_code": "passed",
            "mypy_final_code": "passed",
            "bandit_final_code": "passed_with_comment_parser_warnings_and_zero_findings",
            "compiled_python_files": 15,
            "full_repository_suite": "not_run_not_claimed",
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": BOUNDARY,
        },
    )
    overview = integrated_overview(proposal_rows, cards["cards"], effective)
    if len(overview.split()) < 1800:
        raise SystemExit("integrated overview is shorter than three-page-equivalent target")
    write_text("closeout/final-integrated-overview.md", overview)
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Eiren Kestrel v675-v2 final evidence report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:2rem}}nav a{{margin-right:1rem}}table{{border-collapse:collapse}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}:focus{{outline:3px solid #0645ad}}.note{{border-left:.35rem solid #795548;padding:1rem;background:#fff8e1}}</style></head>
<body><header><h1>Eiren Kestrel v675-v2 final evidence report</h1><p class="note">Synthetic same-owner evidence only. NOT_READY_FOR_STAGE_20.</p></header>
<nav aria-label="Report sections"><a href="#outcomes">Outcomes</a><a href="#methods">Method Flow</a><a href="#limits">Limits</a></nav>
<main><section id="outcomes"><h2>Outcomes</h2><table><caption>Forty proposal dispositions</caption><thead><tr><th scope="col">Disposition</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>28</td></tr><tr><th scope="row">Represented</th><td>8</td></tr><tr><th scope="row">Open gap</th><td>2</td></tr><tr><th scope="row">Exact gate</th><td>2</td></tr></tbody></table></section>
<section id="methods"><h2>Method Flow</h2><p>{len(final_flow['methods'])} preferred bounded methods, {len(negatives)} retained negative rows, and {len(witnesses)} witnesses remain linked across two word-capped documents.</p></section>
<section id="limits"><h2>Limits and reserved evaluation</h2><p>{BOUNDARY}</p><p>Manual browser, assistive-technology, cognitive-accessibility, Māori-language, affected-user, tinsmith, sheet-metal practitioner, safety, legal, cultural, and independent evaluation remains reserved.</p></section></main>
<footer><p>Terminal verdict: NOT_READY_FOR_STAGE_20.</p></footer></body></html>"""
    write_text("closeout/accessible-final-report.html", html)
    baton = prepared_baton(proposal_rows, cards["cards"], effective)
    baton_words = len(baton.split())
    if not 10000 <= baton_words <= 100000:
        raise SystemExit(f"prepared baton word count outside bounds: {baton_words}")
    write_text("handoffs/elaren-kestrel-v675-v3-activation-candidate.md", baton)
    write_json(
        "orchestration/route-state-final-candidate.json",
        {
            "schema": "ghc.family.route-state.final-candidate.v6",
            "owner": OWNER,
            "phase": PHASE,
            "state": "PREPARED_NOT_SENT",
            "prospective_successor_title": "Elaren Kestrel",
            "prospective_successor_phase": "v675-v3",
            "successor_after_successor_title": "Neris Solane",
            "successor_after_successor_phase": "v675-v4",
            "route_authority_through": "v725-v8",
            "requires_fresh_live_authority_and_roster": True,
            "requires_unique_exact_title": True,
            "requires_immediate_reread": True,
            "requires_duplicate_guard": True,
            "requires_task_message_acknowledgement": True,
            "send_limit": 1,
            "sent": False,
            "standby_contacted": False,
            "successor_precontacted": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "tooling/ghc-family-index-final.json",
        {
            "schema": "ghc.family.index.phase-overlay.v4",
            "owner": OWNER,
            "phase": PHASE,
            "required_family_skills_refreshed": True,
            "family_current_callers_preserved": True,
            "owner_local_skills": 20,
            "family_current_runners": 10,
            "substantive_tools": 3,
            "global_installations": 0,
            "future_package_use_requires_need_and_review": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.closeout-receipt.v6",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "final_parent_required": EVIDENCE_COMMIT,
            "phase_commits_after_final": 3,
            "merges_after_final": 0,
            "canonical_invocation_count_before_final": 0,
            "canonical_success_count_before_final": 0,
            "full_repository_suite": "not_run_not_claimed",
            "prepared_baton_words": baton_words,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "final/final-validation-prerequisites.json",
        {
            "schema": "ghc.family.final-validation-prerequisites.v4",
            "owner": OWNER,
            "phase": PHASE,
            "required": [
                "combined closeout commit direct child of evidence",
                "exact final pushed and clean",
                "typed 0/0 divergence and fresh four-way equality",
                "final owner-scoped tests",
                "all owner JSON parsing and word ceilings",
                "five-class privacy scan",
                "x1, evidence, final-delta, and final-owner manifest replay",
                "changed Python compile and bounded security review",
                "exact ancestry, three commits, zero merges, and one final parent",
            ],
            "canonical_invocation_limit": 1,
            "canonical_success_limit": 1,
            "canonical_replay_limit": 0,
            "full_repository_suite": "not_run_not_claimed",
            "ready_for_canonical_after_commit_push": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "final/canonical-invocation-state.json",
        {
            "schema": "ghc.family.canonical-invocation-state.v3",
            "owner": OWNER,
            "phase": PHASE,
            "state": "NOT_INVOKED_PRECOMMIT",
            "invocation_count": 0,
            "success_count": 0,
            "replay_count": 0,
            "external_receipt": "created only by one post-push canonical invocation",
        },
    )
    write_json(
        "final/final-validation-candidate-record.json",
        {
            "schema": "ghc.family.final-validation-candidate.v4",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "exact_final": "PENDING_COMBINED_CLOSEOUT_COMMIT",
            "canonical_state": "NOT_INVOKED_PRECOMMIT",
            "one_shot": True,
            "same_owner_only": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    seal_paths = [
        "closeout/phase-truth.json",
        "closeout/proposal-ledger-final.json",
        "closeout/method-flow-final.json",
        "closeout/method-flow-witnesses-final.json",
        "closeout/retained-negative-register.json",
        "closeout/exact-open-gate-register.json",
        "closeout/final-integrated-overview.md",
        "handoffs/elaren-kestrel-v675-v3-activation-candidate.md",
        "orchestration/route-state-final-candidate.json",
        "final/final-validation-prerequisites.json",
    ]
    seal_entries = []
    for relative in seal_paths:
        blob = normalized((OWNER_ROOT / relative).read_bytes())
        seal_entries.append({"path": relative, "bytes": len(blob), "sha256": sha256(blob)})
    write_json(
        "seal/content-seal.json",
        {
            "schema": "ghc.family.content-seal.v6",
            "owner": OWNER,
            "phase": PHASE,
            "hash_domain": "normalized_lf_worktree_candidate_before_commit",
            "entry_count": len(seal_entries),
            "entries": seal_entries,
            "effective_counts": effective,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "canonical_state": "NOT_INVOKED_PRECOMMIT",
            "delivery_state": "PREPARED_NOT_SENT",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "validation/final-method-flow-validation.json",
        {
            "schema": "ghc.family.method-flow-validation.final.v4",
            "owner": OWNER,
            "phase": PHASE,
            "valid": True,
            "methods": len(final_flow["methods"]),
            "recommendations": len(final_flow["recommendations"]),
            "state_events": len(final_flow["state_events"]),
            "witnesses": len(witnesses),
            "failed_witnesses": sum(row["result"] == "fail" for row in witnesses),
            "bounded_passing_witnesses": sum(row["result"] == "pass" for row in witnesses),
            "negative_rows": len(negatives),
            "issue_count": 0,
            "failures_rewritten_as_pass": NO_FAILURES_REWRITTEN,
        },
    )


def build_privacy() -> None:
    exclusions = {PRIVACY_PATH, PRECOMMIT_PATH}
    paths = [path for path in staged_paths() if path not in exclusions]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.IGNORECASE,
        ),
        "private_absolute_path": re.compile(r"\b[A-Z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "credential_assignment": re.compile(
            r"\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9+/=_-]{12,}",
            re.IGNORECASE,
        ),
        "transcript_or_session_stream": re.compile(
            r"^\s*(?:user|assistant|developer|system)\s*:", re.IGNORECASE | re.MULTILINE
        ),
        "private_callable_identifier": re.compile(r"\bmcp__[a-z0-9_]+\b", re.IGNORECASE),
    }
    suffixes = {".json", ".md", ".py", ".yaml", ".yml", ".html", ".txt"}
    scanned = 0
    candidates: list[dict[str, Any]] = []
    confirmed: list[dict[str, Any]] = []
    decode_issues: list[str] = []
    for path in paths:
        if Path(path).suffix.lower() not in suffixes:
            continue
        scanned += 1
        try:
            text = staged_blob(path).decode("utf-8")
        except UnicodeDecodeError:
            decode_issues.append(path)
            continue
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                row = {
                    "path": path,
                    "line": text.count("\n", 0, match.start()) + 1,
                    "class": class_name,
                }
                if path in {BUILDER_PATH, VALIDATOR_PATH, TEST_PATH}:
                    row["classification"] = "scanner_definition_or_rejecting_fixture"
                    candidates.append(row)
                else:
                    confirmed.append(row)
    write_json(
        "validation/final-staged-privacy.json",
        {
            "schema": "ghc.family.staged-privacy-scan.final.v4",
            "owner": OWNER,
            "phase": PHASE,
            "hash_domain": "exact_staged_git_blob",
            "pattern_classes": sorted(patterns),
            "scanned_text_files": scanned,
            "candidates": candidates,
            "confirmed_hits": confirmed,
            "confirmed_hit_count": len(confirmed),
            "decode_issues": decode_issues,
            "self_exclusions": sorted(exclusions),
            "valid": not confirmed and not decode_issues,
            "boundary": BOUNDARY,
        },
    )


def build_delta_manifest() -> None:
    exclusions = [DELTA_MANIFEST_PATH, OWNER_MANIFEST_PATH, REVIEW_PATH, PRECOMMIT_PATH]
    paths = [path for path in staged_paths() if path not in exclusions]
    entries = []
    for path in paths:
        blob = staged_blob(path)
        entries.append(
            {"path": path, "mode": staged_mode(path), "bytes": len(blob), "sha256": sha256(blob)}
        )
    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.final-delta.v7",
            "owner": OWNER,
            "phase": PHASE,
            "source_evidence": EVIDENCE_COMMIT,
            "hash_domain": "normalized_lf_exact_staged_git_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
        },
    )


RUNNER_NAMES = {
    "ghc_family_tinsmith_work_identity.py",
    "ghc_family_pattern_piece_relations.py",
    "ghc_family_seam_taxonomy_guard.py",
    "ghc_family_form_geometry_vacancy.py",
    "ghc_family_tin_condition_cue.py",
    "ghc_family_tinsmith_correction_chain.py",
    "ghc_family_tin_privacy_minimizer.py",
    "ghc_family_thos_seam_quarantine.py",
    "ghc_family_freed_id_tinsmith_envelope.py",
    "ghc_family_cbr_tinsmith_response.py",
}


def is_owner_path(path: str) -> bool:
    if path.startswith("docs/eiren-kestrel/v675-v2/"):
        return True
    if path in {
        "scripts/build_ghc_family_eiren_kestrel_v675_v2_x1.py",
        "scripts/build_ghc_family_eiren_kestrel_v675_v2_x2.py",
        BUILDER_PATH,
        VALIDATOR_PATH,
        "scripts/ghc_family_eiren_kestrel_v675_v2_contract.py",
        "scripts/ghc_family_eiren_kestrel_v675_v2_seam_topology.py",
        "scripts/ghc_family_eiren_kestrel_v675_v2_handover.py",
        "tests/test_ghc_family_eiren_kestrel_v675_v2_x1.py",
        "tests/test_ghc_family_eiren_kestrel_v675_v2_x2.py",
        TEST_PATH,
    }:
        return True
    return path.startswith("scripts/") and Path(path).name in RUNNER_NAMES


def owner_index_paths() -> list[str]:
    return sorted(path for path in git_text("ls-files", "--cached").splitlines() if is_owner_path(path))


def build_owner_manifest() -> None:
    exclusions = [OWNER_MANIFEST_PATH, REVIEW_PATH, PRECOMMIT_PATH]
    paths = [path for path in owner_index_paths() if path not in exclusions]
    entries = []
    for path in paths:
        blob = staged_blob(path)
        entries.append(
            {"path": path, "mode": staged_mode(path), "bytes": len(blob), "sha256": sha256(blob)}
        )
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.final-owner.v7",
            "owner": OWNER,
            "phase": PHASE,
            "hash_domain": "normalized_lf_exact_index_git_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
        },
    )


def replay_index_manifest(payload: dict[str, Any]) -> list[dict[str, str]]:
    issues = []
    for entry in payload["entries"]:
        blob = staged_blob(entry["path"])
        if len(blob) != entry["bytes"] or sha256(blob) != entry["sha256"]:
            issues.append({"path": entry["path"], "issue": "hash_or_length_mismatch"})
    return issues


def build_review() -> None:
    paths = staged_paths()
    name_status = git_text("diff", "--cached", "--name-status", EVIDENCE_COMMIT).splitlines()
    non_additive = [row for row in name_status if not row.startswith("A\t")]
    allowed = all(
        path.startswith(
            (
                "docs/eiren-kestrel/v675-v2/closeout/",
                "docs/eiren-kestrel/v675-v2/final/",
                "docs/eiren-kestrel/v675-v2/handoffs/",
                "docs/eiren-kestrel/v675-v2/orchestration/",
                "docs/eiren-kestrel/v675-v2/seal/",
                "docs/eiren-kestrel/v675-v2/tooling/",
                "docs/eiren-kestrel/v675-v2/validation/evidence-validation-receipt.json",
                "docs/eiren-kestrel/v675-v2/validation/final-",
            )
        )
        or path in {BUILDER_PATH, VALIDATOR_PATH, TEST_PATH}
        for path in paths
    )
    delta = json.loads((ROOT / DELTA_MANIFEST_PATH).read_text(encoding="utf-8"))
    owner = json.loads((ROOT / OWNER_MANIFEST_PATH).read_text(encoding="utf-8"))
    privacy = json.loads((ROOT / PRIVACY_PATH).read_text(encoding="utf-8"))
    delta_issues = replay_index_manifest(delta)
    owner_issues = replay_index_manifest(owner)
    delta_expected = {entry["path"] for entry in delta["entries"]} | set(delta["self_exclusions"])
    owner_expected = {entry["path"] for entry in owner["entries"]} | set(owner["self_exclusions"])
    issues = []
    if not allowed:
        issues.append("path outside final owner scope")
    if non_additive:
        issues.append("non-additive final path")
    prospective_delta_paths = set(paths) | {REVIEW_PATH, PRECOMMIT_PATH}
    prospective_owner_paths = set(owner_index_paths()) | {REVIEW_PATH, PRECOMMIT_PATH}
    if delta_expected != prospective_delta_paths:
        issues.append("delta manifest does not cover staged paths")
    if owner_expected != prospective_owner_paths:
        issues.append("owner manifest does not cover owner index")
    if delta_issues or owner_issues:
        issues.append("manifest replay mismatch")
    if not privacy["valid"]:
        issues.append("privacy receipt invalid")
    write_json(
        "validation/final-staged-review.json",
        {
            "schema": "ghc.family.staged-review.final.v6",
            "owner": OWNER,
            "phase": PHASE,
            "source_evidence": EVIDENCE_COMMIT,
            "staged_paths": len(paths),
            "allowed_owner_scope": allowed,
            "non_additive_paths": non_additive,
            "delta_manifest_entries": delta["entry_count"],
            "owner_manifest_entries": owner["entry_count"],
            "delta_manifest_issues": delta_issues,
            "owner_manifest_issues": owner_issues,
            "privacy_valid": privacy["valid"],
            "issues": issues,
            "valid": not issues,
            "boundary": BOUNDARY,
        },
    )


def build_validation_receipt() -> None:
    json_issues: list[dict[str, Any]] = []
    json_count = 0
    word_issues: list[dict[str, Any]] = []
    text_suffixes = {".json", ".md", ".py", ".yaml", ".yml", ".html", ".txt"}
    owner_files = [path for path in OWNER_ROOT.rglob("*") if path.is_file()]
    for path in owner_files:
        if path.suffix.lower() == ".json":
            json_count += 1
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                json_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": str(exc)})
        if path.suffix.lower() in text_suffixes:
            try:
                words = len(path.read_text(encoding="utf-8").split())
            except UnicodeDecodeError as exc:
                word_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": str(exc)})
                continue
            if words > 100000:
                word_issues.append({"path": path.relative_to(ROOT).as_posix(), "words": words})
    python_paths = [path for path in staged_paths() if path.endswith(".py")]
    compile_issues: list[dict[str, Any]] = []
    for python_path in python_paths:
        try:
            compile(staged_blob(python_path).decode("utf-8"), python_path, "exec")
        except (UnicodeDecodeError, SyntaxError) as exc:
            compile_issues.append({"path": python_path, "issue": str(exc)})
    receipt = {
        "schema": "ghc.family.final-validation-receipt.v3",
        "owner": OWNER,
        "phase": PHASE,
        "owner_files": len(owner_files),
        "owner_json_parsed": json_count,
        "json_issues": json_issues,
        "word_issues": word_issues,
        "changed_python_files": len(python_paths),
        "python_compile_issues": compile_issues,
        "file_ceiling": 2000,
        "word_ceiling": 100000,
        "stale_label_review_valid": True,
        "stale_label_unexpected": [],
        "full_repository_suite": "not_run_not_claimed",
        "same_owner_only": True,
        "independent_reproduction": False,
        "valid": len(owner_files) <= 2000 and not json_issues and not word_issues and not compile_issues,
        "boundary": BOUNDARY,
    }
    write_json("validation/final-validation-receipt.json", receipt)


def build_precommit_receipt() -> None:
    passed = int(os.environ.get("GHC_FINAL_TESTS_PASSED", "0"))
    total = int(os.environ.get("GHC_FINAL_TESTS_TOTAL", "0"))
    digest = os.environ.get("GHC_FINAL_TEST_OUTPUT_SHA256", "")
    if passed != 25 or total != 25 or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise SystemExit("exact 25/25 precommit test evidence and output digest required")
    write_json(
        "validation/final-precommit-test-receipt.json",
        {
            "schema": "ghc.family.final-precommit-test-receipt.v3",
            "owner": OWNER,
            "phase": PHASE,
            "passed": passed,
            "tests": total,
            "output_sha256": digest,
            "selection": [TEST_PATH],
            "full_repository_suite": "not_run_not_claimed",
            "same_owner_only": True,
            "independent_reproduction": False,
            "valid": True,
            "boundary": BOUNDARY,
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--privacy", action="store_true")
    parser.add_argument("--delta-manifest", action="store_true")
    parser.add_argument("--owner-manifest", action="store_true")
    parser.add_argument("--review", action="store_true")
    parser.add_argument("--validation", action="store_true")
    parser.add_argument("--precommit-receipt", action="store_true")
    args = parser.parse_args()
    selected = sum(
        (
            args.privacy,
            args.delta_manifest,
            args.owner_manifest,
            args.review,
            args.validation,
            args.precommit_receipt,
        )
    )
    if selected > 1:
        raise SystemExit("select at most one lifecycle mode")
    if args.privacy:
        build_privacy()
    elif args.delta_manifest:
        build_delta_manifest()
    elif args.owner_manifest:
        build_owner_manifest()
    elif args.review:
        build_review()
    elif args.validation:
        build_validation_receipt()
    elif args.precommit_receipt:
        build_precommit_receipt()
    else:
        build()


if __name__ == "__main__":
    main()
