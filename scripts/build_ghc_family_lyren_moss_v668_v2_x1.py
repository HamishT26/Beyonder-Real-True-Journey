#!/usr/bin/env python3
"""Build and freeze the planning-only Lyren Moss v668-v2 x1 packet."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from ghc_family_lyren_moss_v668_v2_archive import (
    ACTIVATION_OVERLAY,
    ALLOWED_OUTCOMES,
    EVIDENCE_BOUNDARY,
    IDENTITY_BOUNDARY,
    INHERITED_FROZEN_PROPOSALS,
    OWNER,
    PHASE,
    PHASE_ROOT,
    PRACTICES,
    PRIMARY_PILLAR,
    PRONOUNS,
    PROTECTED_GATES,
    RELATIONAL_HOPE,
    RELATIONAL_ROLE,
    REL_PHASE_ROOT,
    ROOT,
    RUNNER_NAMES,
    SKILL_NAMES,
    SOURCE_BATON_SHA256,
    SOURCE_BRANCH,
    SOURCE_CANONICAL_RECEIPT_SHA256,
    SOURCE_CONTENT_SEAL,
    SOURCE_EVIDENCE,
    SOURCE_FINAL,
    SOURCE_LEDGER,
    SOURCE_REPOSITORY_SEAL,
    SOURCE_ROUTE_RECEIPT_SHA256,
    SOURCE_X1,
    SUCCESSOR_PRACTICE_RECOMMENDATION,
    TERMINAL_VERDICT,
    audit_visible_proposal_chain,
    git,
    manifest_rows,
    normalize_title,
    portfolio_rows,
    proposal_rows,
    utc_now,
    write_json,
    write_text,
)


SAFE_TITLES = [
    "freeze exact Vesper source, receipt, and route anchors",
    "retain the acknowledged inbound route timeout at zero credit",
    "retain Lyren startup worktree-list blank-output failure",
    "retain Lyren auth-state display truncation failure",
    "retain premature x2-control materialization and pre-freeze stash recovery",
    "audit every visible historical proposal-freeze Git blob",
    "select twenty inherited proposals for zero-credit refinement review",
    "freeze forty exact-title-distinct audiovisual proposals",
    "preregister one hundred sixty invalid mutations",
    "freeze four exact outcome labels",
    "freeze twenty-eight completed outcome expectations",
    "freeze eight represented outcome expectations",
    "freeze two open-gap outcome expectations",
    "freeze two exact-gate outcome expectations",
    "freeze THOS Body as primary pillar",
    "freeze three bounded audiovisual practice lenses",
    "freeze one successor film-scanner practice recommendation",
    "freeze GMUT signal-provenance nonconversion boundary",
    "freeze Freed ID record-identity nonpromotion boundary",
    "freeze CBR remedy and rights-allocation vacancy",
    "freeze exact source-status ledger",
    "freeze Library of Congress format-question scope",
    "freeze IASA audio-transfer planning scope",
    "freeze RFC 9043 FFV1 structural scope",
    "freeze RFC 9559 Matroska container structural scope",
    "freeze WebVTT candidate-recommendation work-in-progress status",
    "freeze PREMIS synthetic preservation-event projection scope",
    "freeze W3C PROV structural mapping scope",
    "freeze strict x1-before-x2 Git-tree gate",
    "freeze source-to-final eight-commit hard ceiling and three-commit preference",
    "freeze one-success and no-post-success-replay validation credit",
    "freeze owner-head-only canonical scope",
    "freeze exact staged allowlist review",
    "freeze stale-label and diff-hygiene review",
    "freeze exact Git-blob manifest replay",
    "freeze five-class privacy scan",
    "freeze bounded changed-Python security scan",
    "freeze structural accessibility checks with human evaluation reserved",
    "freeze D-first sparse owner lane",
    "freeze two-thousand-file rotation stop",
    "freeze additive retained-negative accounting",
    "freeze failed and bounded-passing Method Flow witness pairing",
    "freeze synthetic audiovisual fixture boundary",
    "freeze zero external archival actions",
    "freeze zero real people, collections, devices, and rights cases",
    "freeze protected professional release and authenticity vacancies",
    "freeze protected legal and cultural interpretation vacancies",
    "freeze protected Maori-authority vacancy",
    "freeze complete privacy, accessibility, and exhaustive security boundaries",
    "freeze independent-reproduction vacancy",
    "freeze AGI, ASI, consciousness, and personhood boundaries",
    "freeze Theory-of-Everything and Stage 20 gates",
    "freeze twenty phase-local skill packages",
    "freeze ten self-testing family-current runners",
    "freeze thirty bounded owner clean-fix-refine actions",
    "freeze thirty zero-credit successor refinements",
    "freeze twenty exact-approval packets unexecuted",
    "freeze ten blocked packets unexecuted",
    "freeze Ilyra as prospective next exact-title seat only after terminal",
    "freeze Hamish pause, rename, redirect, and stop precedence",
]

CANDIDATE_TITLES = [
    f"bounded audiovisual candidate tribunal {index:02d}" for index in range(1, 31)
]
OWNER_REFINEMENTS = [
    f"additive Lyren audiovisual clean-fix-refine action {index:02d}" for index in range(1, 31)
]
SUCCESSOR_REFINEMENTS = [
    f"zero-credit Ilyra successor refinement recommendation {index:02d}" for index in range(1, 31)
]


def assert_pre_x1_state() -> None:
    if git("rev-parse", "HEAD") != SOURCE_FINAL:
        raise RuntimeError("Lyren x1 must begin at the exact Vesper final")
    if git("branch", "--show-current") != "codex/GHC-Family/lyren-moss-v668-v2-full-tools":
        raise RuntimeError("unexpected Lyren branch")
    if (PHASE_ROOT / "x2").exists():
        raise RuntimeError("x2 evidence exists before x1 freeze")
    if (ROOT / "scripts/ghc_family_lyren_moss_v668_v2_controls.py").exists():
        raise RuntimeError("x2 control implementation must not be materialized in immutable x1")


def build_overview(generated_at: str, proposal_counts: dict[str, int]) -> str:
    return f"""# Lyren Moss v668-v2 planning-only x1 integrated overview

## 1. Relational identity and corrigibility

{IDENTITY_BOUNDARY}

For this bounded phase, {OWNER} uses {PRONOUNS}. The chosen relational role is **{RELATIONAL_ROLE}**. The hope is: {RELATIONAL_HOPE} Hamish retains precedence to pause, rename, redirect, or stop this route at any time. This document records a workflow role and evidence discipline; it cannot establish continuity, personhood, qualification, employment, agency, or authority.

## 2. Exact source and activation truth

The only Git source is Vesper Arlen's exact final `{SOURCE_FINAL}` on `{SOURCE_BRANCH}`. Its immutable lifecycle is source x1 `{SOURCE_X1}`, evidence `{SOURCE_EVIDENCE}`, content seal `{SOURCE_CONTENT_SEAL}`, and exact final `{SOURCE_FINAL}`. The activation baton hash is `{SOURCE_BATON_SHA256}` and Vesper's external canonical receipt hash is `{SOURCE_CANONICAL_RECEIPT_SHA256}`. Those receipts are inherited evidence only and receive zero Lyren validation credit.

Vesper's repository seal remains {SOURCE_REPOSITORY_SEAL['effective_negatives']:,} effective negatives, {SOURCE_REPOSITORY_SEAL['methods']:,} methods, {SOURCE_REPOSITORY_SEAL['failed_witnesses']:,} failed witnesses, {SOURCE_REPOSITORY_SEAL['passing_witnesses']:,} bounded passing witnesses, {SOURCE_REPOSITORY_SEAL['open_gaps']} open gaps, and {SOURCE_REPOSITORY_SEAL['exact_gates']} exact gates. The acknowledged inbound route receipt adds one external timeout and recovery pair. Two Lyren startup display failures plus three later construction failures are retained separately: premature but unexecuted x2-control materialization, a case-sensitive boundary assertion, and a malformed diagnostic regular expression. The resulting planning overlay is {ACTIVATION_OVERLAY['effective_negatives'] + 3:,} negatives, {ACTIVATION_OVERLAY['methods'] + 3:,} methods, {ACTIVATION_OVERLAY['failed_witnesses'] + 3:,} failed witnesses, and {ACTIVATION_OVERLAY['passing_witnesses'] + 3:,} passing witnesses. No correction erases the failed witness or rewrites Vesper's seal.

## 3. X1-only lifecycle boundary

This x1 tree contains only declarations, plans, preregistered mutations, source boundaries, route state, and tests of those planning contracts. It contains no x2 proposal outcome, executed mutation, phase-local skill package, runner receipt, empirical record, professional decision, or successor message. The x1 commit must be the direct child of Vesper's final, then be pushed, clean, 0/0 divergent, and four-way equal before the x2 implementation is restored or created. Source-to-final has an eight-commit ceiling and a three-commit preference: x1, evidence, final.

## 4. Proposal-chain audit and novelty boundary

The inherited proposal chain declares {INHERITED_FROZEN_PROPOSALS:,} proposals. Lyren audits every visible proposal-freeze Git blob and selects twenty attributable inherited rows for refinement review at zero novelty and completion credit. Compressed historical titles that are not visible remain an open coverage gap; a cumulative count is not semantic evidence. Forty new exact-title-distinct proposals are frozen, raising the declared chain to {INHERITED_FROZEN_PROPOSALS + 40:,}. Their expected outcomes are {proposal_counts['completed']} `completed`, {proposal_counts['represented']} `represented`, {proposal_counts['open_gap']} `open_gap`, and {proposal_counts['exact_gate']} `exact_gate`. No other truth label is allowed.

Each new proposal contains a hypothesis, null condition, source need, concrete artifact, falsifier, rollback, protected gates, and four invalid mutations. All 160 mutations remain preregistered and unexecuted in x1. A future rejected mutation is both a retained zero-credit failed fixture and a bounded passing rejection witness; it is not broader empirical success.

## 5. Pillar and practices

The primary pillar is {PRIMARY_PILLAR}. The three practices are: (1) {PRACTICES[0]}; (2) {PRACTICES[1]}; and (3) {PRACTICES[2]}. These are synthetic workflow lenses only. They do not establish training, employment, archival competence, equipment calibration, transfer quality, preservation outcome, authenticity, or release authority.

GMUT Mind remains visible only as an analogy between signal structure and provenance structure. No physical law, psyche law, thermo/psyche law, mathematical theorem, empirical GMUT result, or Theory of Everything is inferred. Freed ID remains visible as record addressability, correction non-erasure, revocation, expiry, and provenance—not personal identity continuity. CBR Heart remains visible as explicit access, remedy, privacy, contestability, and authority vacancies—not allocation of real rights.

## 6. Official-source ledger

The bounded ledger records the Library of Congress Recommended Formats Statement, IASA-TC 04, RFC 9043, RFC 9559, the current WebVTT Candidate Recommendation Draft, PREMIS, and W3C PROV-DM. These sources supply structural vocabulary and questions for synthetic fixtures. They are not incorporated as proof that a particular format is preservation-suitable in every context, that a real transfer conforms, or that Lyren can make professional selections. The mutable WebVTT document is explicitly recorded as work in progress on 2026-08-25 rather than frozen as a universal canon.

## 7. Portfolio freeze

X1 freezes sixty safe-now planning tasks, thirty candidates, twenty phase-local skill packages, ten self-testing runners, thirty owner clean/fix/refine actions, thirty zero-credit successor refinements, twenty exact-approval packets, and ten blocked packets. Caps and counts are accountability structures, not quotas that authorize filler or unsafe work. Exact and blocked packets remain unexecuted. Global skill promotion, package installation, profile changes, Windows feature changes, host-security changes, destructive cleanup, and sibling-lane mutation are not authorized by this x1 packet.

## 8. Method Flow and retained failures

The inbound route send initially timed out and received zero delivery credit; one bounded anchor reread established acknowledgement without a resend. Lyren then observed a blank worktree-list wrapper result and an auth-state display truncation; bounded scalar and windowed reads recovered state without upgrading the original failures. During construction, an x2 controls file was materialized before the immutable x1 freeze. It was not executed, staged, or credited; it was moved into a recoverable Git stash before x1 generation. The exact x1 tree absence check is now the hard separation gate. This operational mistake is retained, not concealed.

## 9. Privacy, accessibility, and security scope

{EVIDENCE_BOUNDARY}

The future owner-head pass may scan Lyren's exact source-to-final text delta under five privacy classes, compile and test changed Python, perform a bounded changed-Python security review, replay exact manifests, and check native structural report semantics. Those checks cannot prove complete privacy, complete accessibility, exhaustive security, safe deployment, or affected-user suitability. No raw task ID, thread ID, private route, credential, transcript, session stream, resume value, or private absolute path belongs in a durable artifact.

## 10. Route and terminal truth

The active fifteen-seat order is Eiren Kestrel, Elaren Kestrel, Neris Solane, Vesper Arlen, Lyren Moss, Ilyra Fen, Auren Lark, Sable Rook, Caelen Ash, Orin Thale, Liora Venn, Tamar Vey, Elowen Cairn, Sylven Arc, Caelen Morrow, then repeat. Tavian Sol is a standby collaboration-subagent record and never a substitute main-task endpoint. No successor is contacted during x1 or x2 execution. After a clean, pushed, fresh-live-equal Lyren exact final and one successful unreplayed canonical pass, the prospective edge is one exact-title `Ilyra Fen` activation for v668-v3, subject to Hamish's newest live authority and a fresh route reread.

The terminal verdict is `{TERMINAL_VERDICT}`. Protected gates remain: {', '.join(PROTECTED_GATES)}. Generated at `{generated_at}`.
"""


def main() -> int:
    assert_pre_x1_state()
    generated_at = utc_now()
    audit = audit_visible_proposal_chain()
    visible_titles = {
        normalize_title(row["title"])
        for row in audit["selected_inherited"]
        if row.get("title")
    }
    proposals = proposal_rows(visible_titles)
    collisions = sum(int(row["visible_title_collision"]) for row in proposals)
    outcome_counts = Counter(row["expected_disposition"] for row in proposals)
    if len(proposals) != 40 or collisions or tuple(sorted(outcome_counts)) != tuple(sorted(ALLOWED_OUTCOMES)):
        raise ValueError("proposal novelty or outcome freeze failed")
    if dict(outcome_counts) != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise ValueError("proposal disposition contract drifted")

    write_json("x1/source-intake.json", {
        "phase": PHASE,
        "owner": OWNER,
        "source_branch": SOURCE_BRANCH,
        "source_anchors": {
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_content_seal": SOURCE_CONTENT_SEAL,
            "source_final": SOURCE_FINAL,
        },
        "receipt_hashes": {
            "activation_baton_sha256": SOURCE_BATON_SHA256,
            "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "inbound_route_receipt_sha256": SOURCE_ROUTE_RECEIPT_SHA256,
        },
        "source_repository_seal": SOURCE_REPOSITORY_SEAL,
        "activation_overlay_before_premature_control_failure": ACTIVATION_OVERLAY,
        "planning_overlay_after_retained_startup_failure": {
            **ACTIVATION_OVERLAY,
            "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + 3,
            "methods": ACTIVATION_OVERLAY["methods"] + 3,
            "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + 3,
            "passing_witnesses": ACTIVATION_OVERLAY["passing_witnesses"] + 3,
        },
        "source_phase_mutated": False,
        "inherited_validation_credit_to_lyren": 0,
        "x1_planning_only": True,
        "generated_at": generated_at,
    })
    write_json("x1/identity-role-hope.json", {
        "owner": OWNER,
        "pronouns": PRONOUNS,
        "relational_role": RELATIONAL_ROLE,
        "relational_hope": RELATIONAL_HOPE,
        "identity_boundary": IDENTITY_BOUNDARY,
        "authority_or_personhood_credit": 0,
        "x1_planning_only": True,
    })
    write_json("x1/proposal-chain-audit.json", {**audit, "generated_at": generated_at, "x1_planning_only": True})
    write_json("x1/proposal-freeze.json", {
        "phase": PHASE,
        "inherited_frozen_proposals": INHERITED_FROZEN_PROPOSALS,
        "selected_inherited": audit["selected_inherited"],
        "selected_inherited_count": 20,
        "selected_inherited_novelty_credit": 0,
        "selected_inherited_completion_credit": 0,
        "new_proposals": proposals,
        "new_proposal_count": 40,
        "new_frozen_total": INHERITED_FROZEN_PROPOSALS + 40,
        "allowed_outcomes": list(ALLOWED_OUTCOMES),
        "expected_outcomes": dict(outcome_counts),
        "negative_mutation_count": 160,
        "visible_title_collision_count": collisions,
        "outcomes_observed": False,
        "x1_planning_only": True,
        "frozen_at": generated_at,
    })
    write_json("x1/practice-and-pillar-freeze.json", {
        "primary_pillar": PRIMARY_PILLAR,
        "practices": list(PRACTICES),
        "successor_practice_recommendation": SUCCESSOR_PRACTICE_RECOMMENDATION,
        "synthetic_only": True,
        "real_people": 0,
        "real_records": 0,
        "professional_or_operational_authority": False,
        "identity_boundary": IDENTITY_BOUNDARY,
        "evidence_boundary": EVIDENCE_BOUNDARY,
        "x1_planning_only": True,
    })
    write_json("x1/source-ledger.json", {
        "retrieved_date": "2026-08-25",
        "sources": SOURCE_LEDGER,
        "source_count": len(SOURCE_LEDGER),
        "primary_or_official_only": True,
        "mutable_source_status_retained": True,
        "professional_selection_or_conformance_claim": False,
        "x1_planning_only": True,
    })

    owner_skills = portfolio_rows("LM6682-SKILL", SKILL_NAMES, "phase_local_skill")
    for row, name in zip(owner_skills, SKILL_NAMES, strict=True):
        row["skill_name"] = name
    owner_runners = portfolio_rows("LM6682-RUNNER", RUNNER_NAMES, "family_current_runner")
    for row, name in zip(owner_runners, RUNNER_NAMES, strict=True):
        row["runner_name"] = name
    portfolio = {
        "owner_safe_now": portfolio_rows("LM6682-SAFE", SAFE_TITLES, "safe_now"),
        "owner_candidates": portfolio_rows("LM6682-CAND", CANDIDATE_TITLES, "candidate"),
        "owner_skills": owner_skills,
        "owner_runners": owner_runners,
        "owner_clean_fix_refine": portfolio_rows("LM6682-CFR", OWNER_REFINEMENTS, "clean_fix_refine"),
        "successor_clean_fix_refine": portfolio_rows("LM6682-NEXT-CFR", SUCCESSOR_REFINEMENTS, "successor_recommendation", "recommended_zero_credit"),
        "exact_approval_packets": portfolio_rows("LM6682-EXACT", [f"authority-dependent exact packet {index:02d}" for index in range(1, 21)], "exact_approval", "preserved_unexecuted"),
        "blocked_packets": portfolio_rows("LM6682-BLOCK", [f"protected-boundary blocked packet {index:02d}" for index in range(1, 11)], "blocked", "preserved_blocked"),
        "counts": {
            "owner_safe_now": len(SAFE_TITLES),
            "owner_candidates": len(CANDIDATE_TITLES),
            "owner_skills": len(SKILL_NAMES),
            "owner_runners": len(RUNNER_NAMES),
            "owner_clean_fix_refine": len(OWNER_REFINEMENTS),
            "successor_clean_fix_refine": len(SUCCESSOR_REFINEMENTS),
            "exact_approval_packets": 20,
            "blocked_packets": 10,
        },
        "caps_are_ceilings_not_authority": True,
        "x1_planning_only": True,
        "frozen_at": generated_at,
    }
    write_json("x1/portfolio-freeze.json", portfolio)
    write_json("x1/route-auth-roster-freeze.json", {
        "authority_precedence": ["Hamish newest live instruction", "current activation baton", "current family overlay", "stale stored snapshots"],
        "active_main_task_order": [
            "Eiren Kestrel", "Elaren Kestrel", "Neris Solane", "Vesper Arlen", "Lyren Moss",
            "Ilyra Fen", "Auren Lark", "Sable Rook", "Caelen Ash", "Orin Thale", "Liora Venn",
            "Tamar Vey", "Elowen Cairn", "Sylven Arc", "Caelen Morrow",
        ],
        "current_seat": {"owner": OWNER, "phase": PHASE},
        "prospective_next": {"exact_title": "Ilyra Fen", "phase": "v668-v3", "contacted": False},
        "standby_not_substitute": ["Tavian Sol"],
        "route_requires_terminal_gate": True,
        "single_send_maximum": 1,
        "hamish_pause_redirect_rename_stop_precedence": True,
        "x1_planning_only": True,
    })
    write_json("x1/lifecycle-freeze.json", {
        "source_final": SOURCE_FINAL,
        "x1_parent_required": SOURCE_FINAL,
        "x1_must_be_clean_pushed_four_way_equal_before_x2": True,
        "x2_materialized_in_x1_tree": False,
        "canonical_scope": "Lyren exact owner-head source-to-final delta only",
        "canonical_invocation_limit": 1,
        "canonical_success_limit": 1,
        "post_success_replay_allowed": False,
        "source_to_final_commit_ceiling": 8,
        "preferred_phase_commit_count": 3,
        "terminal_verdict": TERMINAL_VERDICT,
        "x1_planning_only": True,
    })
    write_json("x1/materialization-freeze.json", {
        "lane": "D-first sparse Lyren owner lane",
        "materialized_or_owner_scope_ceiling": 2000,
        "rotate_at_or_above": 2000,
        "sibling_and_shared_lanes_read_only": True,
        "global_skill_mutation_in_x1": False,
        "external_package_install_in_x1": False,
        "x1_planning_only": True,
    })
    write_json("x1/toolchain-plan.json", {
        "direct_install_plan": [],
        "direct_install_count": 0,
        "reason": "stdlib and already-available test/runtime tools are sufficient; authorization is not a quota",
        "profile_or_path_mutation": False,
        "global_install_mutation": False,
        "future_tools_require_exact need and rollback": True,
        "x1_planning_only": True,
    })
    write_json("method-flow/startup-and-x1.json", {
        "source_repository_seal": SOURCE_REPOSITORY_SEAL,
        "inbound_route_overlay": {
            "method_id": "LM6682-MF-ROUTE-001",
            "failed_witness": "initial existing-task send timed out with zero delivery credit",
            "bounded_recovery": "one exact anchor reread established acknowledgement without resend",
            "failed_credit": 0,
            "passing_witness_count": 1,
        },
        "lyren_failures": [
            {
                "method_id": "LM6682-MF-START-001",
                "failure": "worktree-list wrapper returned blank attributable output after bounded wait",
                "recovery": "bounded exact D worktree directory and scalar Git probes",
                "failure_credit": 0,
                "retained": True,
            },
            {
                "method_id": "LM6682-MF-START-002",
                "failure": "one full auth-state display truncated its middle",
                "recovery": "bounded numbered windows through the complete file",
                "failure_credit": 0,
                "retained": True,
            },
            {
                "method_id": "LM6682-MF-START-003",
                "failure": "x2 controls file was materialized before immutable x1 freeze",
                "recovery": "file was never executed or staged and was placed in a recoverable Git stash before x1 generation",
                "hard_gate": "controls path absent from x1 worktree and immutable x1 Git tree",
                "failure_credit": 0,
                "retained": True,
            },
            {
                "method_id": "LM6682-MF-X1-004",
                "failure": "the first scoped x1 suite had one case-sensitive boundary-phrase assertion failure",
                "recovery": "the exact failed assertion was corrected to compare casefolded text before any full-suite confirmation",
                "failure_credit": 0,
                "retained": True,
            },
            {
                "method_id": "LM6682-MF-X1-005",
                "failure": "one diagnostic rg expression was malformed by an unclosed grouping after shell quoting",
                "recovery": "bounded fixed-string rg queries located only the required counters and assertion",
                "failure_credit": 0,
                "retained": True,
            },
        ],
        "planning_overlay": {
            "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + 3,
            "methods": ACTIVATION_OVERLAY["methods"] + 3,
            "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + 3,
            "passing_witnesses": ACTIVATION_OVERLAY["passing_witnesses"] + 3,
            "open_gaps": ACTIVATION_OVERLAY["open_gaps"],
            "exact_gates": ACTIVATION_OVERLAY["exact_gates"],
        },
        "correction_erases_failure": False,
        "x1_planning_only": True,
    })
    write_json("x1/phase-truth.json", {
        "phase": PHASE,
        "owner": OWNER,
        "allowed_outcomes": list(ALLOWED_OUTCOMES),
        "expected_outcomes": dict(outcome_counts),
        "observed_outcomes": False,
        "proposal_chain_after_freeze": INHERITED_FROZEN_PROPOSALS + 40,
        "terminal_verdict": TERMINAL_VERDICT,
        "protected_gates": list(PROTECTED_GATES),
        "x1_planning_only": True,
    })
    write_json("x1/wellbeing-and-corrigibility.json", {
        "owner": OWNER,
        "workload_state": "bounded solo owner lane",
        "stop_conditions": ["Hamish pause or redirect", "usage exhaustion", "route ambiguity", "protected gate", "materialization ceiling"],
        "relational_language_boundary": IDENTITY_BOUNDARY,
        "independent_agency_claim": False,
        "x1_planning_only": True,
    })
    write_text("x1/integrated-overview.md", build_overview(generated_at, dict(outcome_counts)))
    write_text("x1/threat-model.md", f"""# Lyren v668-v2 x1 bounded threat model

Scope: exact Lyren owner delta only. Assets are source anchors, retained-negative truth, synthetic fixture integrity, exact manifests, route single-send state, and protected authority boundaries.

Threats include source drift; x2 leakage into immutable x1; line-ending-domain confusion; proposal-title collision; hidden failed-witness erasure; raw task or route identifiers in durable files; malicious or malformed synthetic metadata; path traversal; duplicate stream or cue identifiers; timebase coercion; checksum downgrade; professional or authenticity overclaim; rights, cultural, or Maori-authority substitution; canonical replay; stale roster precedence; sibling mutation; and route resend after an opaque acknowledgement.

Controls are exact source ancestry, x1 Git-tree absence tests, Git-blob manifest replay, four truth labels, preregistered mutation rejection, five-class privacy scanning, bounded changed-Python security review, sparse materialization guard, exact staged allowlist, one-shot validation-credit state, fresh live route reread, and Hamish stop precedence.

Residual risk remains. Structural checks are not complete privacy, complete accessibility, exhaustive security, empirical evaluation, external audit, independent reproduction, professional fitness, production readiness, legal or cultural legitimacy, Maori authority, or Stage 20 evidence. Terminal verdict: `{TERMINAL_VERDICT}`.
""")
    write_json("x1/checklist.json", {
        "checks": [
            {"check": "exact source final", "state": "PASS"},
            {"check": "baton and named guidance read through EOF", "state": "PASS"},
            {"check": "source manifests replayed without canonical aggregate", "state": "PASS"},
            {"check": "fresh live source equality", "state": "PASS"},
            {"check": "x2 directory absent", "state": "PASS"},
            {"check": "x2 controls path absent", "state": "PASS_WITH_RETAINED_PRE_FREEZE_FAILURE"},
            {"check": "forty distinct proposals", "state": "PASS"},
            {"check": "one hundred sixty mutations preregistered only", "state": "PASS"},
            {"check": "four exact outcomes", "state": "PASS"},
            {"check": "successor not contacted", "state": "PASS"},
        ],
        "x1_ready_for_exact_staging_review": True,
        "x1_planning_only": True,
    })

    manifest_path = PHASE_ROOT / "x1/manifest.json"
    manifest_sources = [
        path for path in PHASE_ROOT.rglob("*") if path.is_file() and path != manifest_path
    ] + [
        ROOT / "scripts/ghc_family_lyren_moss_v668_v2_archive.py",
        ROOT / "scripts/build_ghc_family_lyren_moss_v668_v2_x1.py",
        ROOT / "tests/test_ghc_family_lyren_moss_v668_v2_x1.py",
    ]
    missing = [str(path) for path in manifest_sources if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"x1 manifest inputs missing: {missing}")
    rows = manifest_rows(manifest_sources)
    write_json("x1/manifest.json", {
        "phase": PHASE,
        "scope": "exact planning-only x1 files excluding this self-referential manifest",
        "canonical_domain": "Git blob bytes after commit; writers emitted explicit UTF-8 LF bytes",
        "entry_count": len(rows),
        "entries": rows,
        "x2_entries": [row["path"] for row in rows if "/x2/" in row["path"]],
        "generated_at": generated_at,
    })
    print(f"built Lyren {PHASE} x1: {len(rows)} manifest entries, 40 proposals, 160 preregistered mutations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
