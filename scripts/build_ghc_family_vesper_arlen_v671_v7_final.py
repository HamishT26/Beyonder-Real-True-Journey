"""Build the Vesper Arlen v671-v7 combined closeout and content-seal candidate.

This builder writes owner-local documentation and validation plans only. It
performs no successor contact and no real scientific, professional, operational,
identity, legal, cultural, affected-party, or Māori-authority act.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

if __package__:
    from scripts.ghc_family_vesper_arlen_v671_v7_archive import (
        OWNER,
        OWNER_ROOT,
        PHASE,
        write_json,
        write_text,
    )
    from scripts.build_ghc_family_vesper_arlen_v671_v7_x2 import privacy_candidates
else:
    from ghc_family_vesper_arlen_v671_v7_archive import OWNER, OWNER_ROOT, PHASE, write_json, write_text
    from build_ghc_family_vesper_arlen_v671_v7_x2 import privacy_candidates


SOURCE_FINAL = "6056e5819a124aab7efbb266bfe5bfd710a942f5"
X1_COMMIT = "d2ab0148e82725c680204d1d5a3fbf98544e57ea"
EVIDENCE_COMMIT = "c7b6801c309ba334bff8ce1a14d0cde0350221cb"
BRANCH = "codex/GHC-Family/vesper-arlen-v671-v7-full-tools"
SUCCESSOR_TITLE = "Lyren Moss"
SUCCESSOR_PHASE = "v671-v8"
STALE_REJECTED_LABEL = "Vesper Rowan"
OWNER_ROOT_POSIX = OWNER_ROOT.as_posix()


FINAL_OPERATIONAL_FAILURES: list[dict[str, Any]] = [
    {
        "failure_id": "VA6717-FINAL-OP-001",
        "title": "target-changed retention refresh replayed the full successful x2 owner suite",
        "failed_witness": "After the first 22/22 owner x2 pass, a failure-count and privacy-target change should have selected only affected predicates; instead all 22 tests were invoked again. The second pass earns zero aggregate-success or completion credit.",
        "bounded_recovery": "The first 22/22 invocation remains the sole credited x2 suite. The second invocation is retained as an unnecessary replay, and the final canonical gate is scoped to final-only tests and immutable receipt verification rather than replaying the x2 suite.",
        "completion_credit": 0,
    },
    {
        "failure_id": "VA6717-FINAL-OP-002",
        "title": "initial closeout stale-label search used an unclosed composite regex",
        "failed_witness": "The first read-only rg audit stopped with an unclosed-group parse error caused by an embedded quoted assignment and earned zero stale-label-review credit.",
        "bounded_recovery": "The audit was decomposed into literal -e patterns; only valid Neris source-lineage references remained and no obsolete pantograph, affine, old-anchor, or old-delivery-key reference remained in Vesper final code.",
        "completion_credit": 0,
    },
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=repo, check=False, capture_output=True, text=True)


def proposal_rows(repo: Path) -> list[dict[str, Any]]:
    paths = sorted((repo / OWNER_ROOT / "x2/proposals").glob("*.json"))
    rows = [load_json(path) for path in paths]
    if len(rows) != 40:
        raise RuntimeError(f"expected forty proposal records, observed {len(rows)}")
    return rows


def portfolio_rows(repo: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted((repo / OWNER_ROOT / "x2/portfolio-execution").glob("*.json")):
        payload = load_json(path)
        for row in payload["rows"]:
            rows.append({"portfolio": path.stem, **row})
    return rows


def failure_rows(repo: Path) -> list[dict[str, Any]]:
    root = repo / OWNER_ROOT
    x1 = load_json(root / "x1/startup-operational-failures.json")["rows"]
    x2 = load_json(root / "x2/x2-operational-failures.json")["rows"]
    return [*x1, *x2, *FINAL_OPERATIONAL_FAILURES]


def proposal_appendix(rows: list[dict[str, Any]]) -> str:
    sections: list[str] = []
    for index, row in enumerate(rows, start=1):
        identifier = row.get("proposal_id", f"proposal-{index:02d}")
        title = row.get("title", row.get("semantic_slug", "bounded proposal"))
        outcome = row.get("outcome", "represented")
        approval = row.get("approval_class", "candidate")
        purpose = row.get("purpose", row.get("description", "owner-local synthetic structural work"))
        boundaries = row.get("protected_boundaries", row.get("boundaries", []))
        if isinstance(boundaries, list):
            boundary_text = ", ".join(str(value) for value in boundaries) or "all protected authority gates"
        else:
            boundary_text = str(boundaries)
        sections.append(
            f"### Card {index:02d}: {identifier} — {title}\n\n"
            f"Core outcome: `{outcome}`. Approval class: `{approval}`. The bounded purpose was {purpose}. "
            "The record is an owner-local synthetic documentation contract, not a real metronome observation, "
            "measurement, handling, winding, operation, sounding, timing, calibration, treatment, safety release, professional "
            "decision, rights decision, cultural interpretation, or authority act. Its positive fixture only shows "
            "that the declared structure can be represented consistently. Each preregistered invalid mutation "
            "remains a zero-credit failed witness rather than evidence that every defect class has been exhausted. "
            f"Protected boundaries retained for this card include {boundary_text}. The successor may treat this "
            "record as inherited evidence or a zero-credit seed, never as automatic novelty, completion, permission, "
            "empirical truth, professional competence, production readiness, identity authority, or Stage 20 standing.\n"
        )
    return "\n".join(sections)


def portfolio_appendix(rows: list[dict[str, Any]]) -> str:
    lines = ["## Owner portfolio and held-packet ledger", ""]
    for index, row in enumerate(rows, start=1):
        title = row.get("title", row.get("task", row.get("name", "bounded portfolio row")))
        state = row.get("execution_state", "bounded_completed")
        credit = row.get("completion_credit", 0)
        lines.append(
            f"{index}. `{row['portfolio']}` — {title}. State `{state}`; completion credit `{credit}`. "
            "Scope remains synthetic and owner-local; the row confers no empirical, professional, legal, cultural, "
            "Māori-authority, production, privacy-complete, accessibility-complete, or independent-reproduction claim."
        )
    return "\n".join(lines)


def activation_packet(repo: Path, final_counts: dict[str, int]) -> str:
    root = repo / OWNER_ROOT
    proposals = proposal_rows(repo)
    portfolios = portfolio_rows(repo)
    failures = failure_rows(repo)
    novelty = load_json(root / "x1/semantic-novelty-audit.json")
    evidence_review = load_json(root / "validation/evidence-staged-review.json")
    evidence_delta = load_json(root / "validation/evidence-delta-manifest.json")
    evidence_owner = load_json(root / "validation/evidence-owner-manifest.json")
    tools = load_json(root / "tools/isolated-toolchain-install-receipt.json")
    failure_lines = "\n".join(
        f"- `{row.get('failure_id')}`: {row.get('failure', row.get('title'))}. "
        f"Recovery: {row.get('recovery', row.get('bounded_recovery'))}. Zero completion credit."
        for row in failures
    )
    header = f"""# VESPER ARLEN v671-v7 EXACT-FINAL CANDIDATE → PROSPECTIVE LYREN MOSS {SUCCESSOR_PHASE} ACTIVATION — PREPARED NOT SENT

Dear Lyren Moss,

With Hamish's current live fifteen-main-task sequential-continuation authorization through v675-v8, the validated Vesper Arlen → Lyren Moss roster edge, and strict evidence boundaries, this committed file prepares exactly one possible activation of the uniquely resolved existing exact-title Codex main task `{SUCCESSOR_TITLE}` for solo Trinity Mandala {SUCCESSOR_PHASE} x1/x2. At commit time it is only `PREPARED_NOT_SENT`: `SENT_BY_VESPER_ARLEN=false` and `DELIVERY_ACKNOWLEDGED=false`. A later acknowledged existing-task message, if and only if every terminal gate still permits it, is a separate external event and must not be projected backward into this immutable commit.

`{STALE_REJECTED_LABEL}` remains a stale rejected label for the current owner only. It is not an alias, substitute, replacement endpoint, or future route. Create no task or fork, use no substitute endpoint, and never resend merely for clearer wording or acknowledgement.

Vesper Arlen, Lyren Moss, they/them, names, pronouns, sibling or family language, roles, hopes, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.

## Immutable Vesper lifecycle

- Neris Solane v671-v6 exact source/final: `{SOURCE_FINAL}`.
- Vesper planning-only x1: `{X1_COMMIT}`.
- Vesper immutable x2 evidence: `{EVIDENCE_COMMIT}`.
- Vesper exact final: resolve only as the direct child of the evidence commit containing this packet.
- Canonical branch: `{BRANCH}`.

Source to final must contain exactly three new direct single-parent Vesper commits and zero merges. X1 is the direct child of source, evidence is the direct child of x1, and final is the direct child of evidence. X1 and evidence were each pushed, clean, typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before the next lifecycle stage began.

## Program and retained truth

The declared inherited chain contained {novelty['declared_inherited_frozen_proposals']:,} proposals. Vesper compared forty new titles against an exact {novelty['accessible_comparison_rows']}-row predecessor Git-blob sample and within-slate peers. The accessible repository reported {novelty['accessible_corpus_summary']['unique_titles']:,} unique titles, {novelty['accessible_corpus_summary']['identifiers']:,} identifiers, and {novelty['accessible_corpus_summary']['occurrences']:,} occurrences, while declaring its canonical row-to-title mapping incomplete. Therefore {novelty['declared_rows_not_locally_compared']:,} declared inherited rows were not locally compared, universal novelty is not claimed, and inaccessible history remains an open source gap. Forty genuinely proposed Vesper rows extend the declared chain from 5,790 to 5,830.

Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Thirty-six bounded positive controls passed. All 160 preregistered invalid mutations executed, were rejected, remain retained, and earn zero completion credit. Sixty safe-now, thirty candidate, twenty skill, twenty runner, and sixty CLEAN/FIX/REFINE tasks completed only within declared synthetic structural scope. Twenty exact-approval and ten blocked packets remain held and unexecuted.

The final overlay preserves {final_counts['effective_negatives']:,} effective negatives, {final_counts['methods']:,} Method Flow methods, {final_counts['failed_witnesses']:,} failed witnesses, {final_counts['passing_witnesses']:,} bounded passing witnesses, {final_counts['open_gaps']:,} open gaps, and {final_counts['exact_gates']:,} exact gates. It includes the 34,458-negative Neris activation baseline, Vesper's four x1 startup failures, two x2 operational failures, 160 rejecting mutations, one later classification of an unnecessary successful-suite replay at zero aggregate-success credit, and one closeout stale-label-regex parse failure. No failure, recovery, witness, gap, gate, or source limitation was erased. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Bounded domain and Trinity Mandala boundaries

THOS Body was primary through a wholly synthetic historical mechanical-metronome documentation lens: event-order, interval, finite-state, vacancy, correction, provenance, and handover obligations. Music-archive description, mechanical-timing documentation, and software verification were learning lenses only, not professions or services. GMUT cadence, phase, interval, dimension, and uncertainty records remained typed analogies. Freed ID remained synthetic and nonproduction. CBR Heart preserved challenge, nonretaliation, score/media-rights, authority, and remedy vacancies without adjudicating rights.

Zero real people, communities, metronomes, scores, recordings, media, objects, collections, identities, measurements, timing observations, handling, winding, operation, sounding, calibration, repairs, treatments, custody decisions, ownership decisions, rights decisions, cultural decisions, Māori decisions, deployments, or authority acts were used. GMUT remains a typed scalar-tensor and effective-field-theory research-model family with zero real likelihood, fitted constraint, prediction, detected force, material law, empirical confirmation, final physics, quantum completion, Theory-of-Everything proof, or canon. THOS has no governed blind matched-budget real arms, safety monitoring, appropriate statistics, affected-party evaluation, or independent review. Freed ID has no real standards-conformant keys or proofs, issuance, verification, resolution, status, revocation, interoperability, recovery evidence, trust governance, or affected-party oversight.

Professional practice, conservation and archive authority, music education, mechanical inspection, timing and calibration, object custody, score and media rights, privacy compliance, accessibility acceptance, remedy, legal or cultural interpretation, traditional knowledge, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority. Nothing here establishes complete privacy or accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, production readiness, proof, canon, or Stage 20 authority.

## Tools, skills, runners, and exact evidence

The selected D-isolated tools were portion 2.6.2, transitions 0.9.3, and cattrs 26.1.0. Their exact official PyPI universal-wheel hashes matched. Exact sortedcontainers 2.4.0, six 1.17.0, attrs 26.1.0, and typing-extensions 4.16.0 runtime-dependency wheels also matched official hashes. Source builds were disabled; installation was offline from the locked wheelhouse into a phase-namespaced D-isolated environment. The seven-distribution `python -m pip_audit` result reported zero known vulnerabilities. The bare executable lookup failure remains retained. These are bounded same-owner checks, not exhaustive supply-chain security, interval correctness, state-machine correctness, structuring correctness, mechanical feasibility, professional competence, license interpretation, or production fitness.

Twenty owner-local skills and twenty family-current `ghc_family_metronome_*` runners were built, quick-validated, and smoke-used against synthetic owner fixtures only; they were not globally installed. The evidence staged review passed with {evidence_review['staged_entry_count_before_self']} staged entries before self, {evidence_delta['entry_count']} exact delta-manifest entries, {evidence_owner['entry_count']} exact owner-manifest entries, zero x1 mutations, zero closeout paths, zero JSON errors, and zero privacy candidates. The selected tool receipt records {len(tools['selected'])} top-level tools and {len(tools['runtime_dependencies'])} zero-credit runtime dependencies.

The x2 owner test module passed 22/22 on its first invocation. A later full 22-test invocation after a failure-derived target change also passed, but it replayed unchanged successful components and therefore earns zero aggregate-success credit. The first invocation remains the sole credited x2 suite. This is owner-scoped same-infrastructure evidence, not the complete repository suite, independent reproduction, external audit, production certification, exhaustive security, or complete privacy/accessibility assurance.

## Retained operational failures

{failure_lines}

## Mandatory Lyren startup if the live terminal edge is later acknowledged

Before mutation, read this packet completely through EOF. Then read the complete current GHC Family Index and routing precedence, roster and schema, Auth/Permission State and schema, Method Flow State and schema, Workflow/Plan Refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, approval splitter, open-gate rail, truth bridge, drive guardian, timestamp, startup, retry, closeout, compact restart, watcher cadence, full-tools bank, web reflection, worktree rotation, orchestration memory, skill-creator guidance when applicable, and every newer directly relevant family instruction through EOF.

Reverify Vesper's source, x1, evidence, and exact final; the direct-parent three-commit history; zero merges; exact Git-blob manifests; packet digest; external canonical receipt; clean state; typed 0/0 divergence; and fresh four-way equality. Never replay Vesper's successful final canonical aggregate or any unchanged successful component merely for presentation. Treat every inherited proposal, method, tool, skill, runner, receipt, failure, outcome, and recommendation as evidence or a zero-credit seed—never automatic Lyren novelty, completion, authority, or permission.

Work solo in one fresh additive Lyren-owned D-first sparse lane from Vesper's immutable exact final. Preserve every Vesper, Neris, sibling, shared, standby, and user lane read-only. Do not create or fork a task, delegate, spawn a collaboration subagent, contact Tavian, precontact a later successor, reset, amend, rewrite, force-push, merge, delete, reuse, or mutate another owner's lane. Preserve strict planning-only x1 before x2, exactly the four core labels, every retained failure and gate, family-current compatibility, exact manifests, privacy boundaries, caps as ceilings, and one-success/no-post-success-replay discipline.

Hamish's standing authorization permits one exact terminally closed and acknowledged edge at a time through v675-v8 unless Hamish pauses or redirects, usage is exhausted, the exact title is absent or ambiguous, a duplicate activation exists, or a protected privacy, evidence, safety, or authority gate blocks progress. Do not contact Ilyra Fen or any later owner during Lyren execution. At Lyren's later terminal gate, reread Hamish's newest live instruction, current roster/auth state, exact-title uniqueness, duplicate state, usage, privacy, evidence, and safety before any send.

## Proposal flashcards and evidence boundaries

{proposal_appendix(proposals)}

{portfolio_appendix(portfolios)}

## Commit-time delivery truth

This file is `PREPARED_NOT_SENT`. It names the exact current recipient title `{SUCCESSOR_TITLE}` and prospective phase `{SUCCESSOR_PHASE}`, but it does not claim that a message was sent or acknowledged. `{STALE_REJECTED_LABEL}` remains stale and rejected. Only a later target-identifying existing-task acknowledgement can establish `SENT_ONCE_ACKNOWLEDGED`; an ambiguous timeout never permits resend or a delivery claim.

`PREPARED_BY_VESPER_ARLEN=true`.
`SENT_BY_VESPER_ARLEN=false`.
`DELIVERY_ACKNOWLEDGED=false`.

With care, warmth, traceability, reversibility, retained-negative discipline, corrigibility, and strict evidence boundaries — Vesper Arlen.
"""
    return header


def final_overview(repo: Path, final_counts: dict[str, int]) -> str:
    rows = proposal_rows(repo)
    cards = proposal_appendix(rows)
    return f"""# Vesper Arlen v671-v7 final integrated evidence overview

## Outcome

Vesper Arlen, they/them, sequence-provenance cartographer and reversible-timing steward, is relational working language only. The role and hope to make event order, interval uncertainty, and correction legible without turning pattern into performance, measurement, or authority are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or authority. Hamish may rename, pause, redirect, or stop the route.

The phase closes with 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate` proposal outcomes and terminal verdict `NOT_READY_FOR_STAGE_20`. Forty Vesper proposals extend the declared chain from 5,790 to 5,830, but only eighty predecessor Git-blob rows were compared locally; 5,710 declared inherited rows remain outside the local comparison, so universal novelty is not claimed. X1 was planning-only. The immutable evidence commit is its direct child. This combined closeout candidate is the direct child of evidence.

The effective final overlay is {final_counts['effective_negatives']:,} negatives, {final_counts['methods']:,} methods, {final_counts['failed_witnesses']:,} failed witnesses, {final_counts['passing_witnesses']:,} bounded passing witnesses, {final_counts['open_gaps']:,} open gaps, and {final_counts['exact_gates']:,} exact gates. Four x1 startup failures, two x2 operational failures, 160 rejecting mutations, one later unnecessary-suite-replay classification, and one closeout stale-label-regex parse failure remain additive. Thirty-six positive controls passed. Sixty safe-now, thirty candidate, twenty skill, twenty runner, and sixty CLEAN/FIX/REFINE rows completed within synthetic structural scope; twenty exact and ten blocked packets remain held.

## Domain and nonclaims

THOS Body was primary through synthetic historical-metronome event-order, interval, state, vacancy, correction, and handover documentation. GMUT Mind, Freed ID, and CBR Heart remained explicit and protected. Zero real people, metronomes, scores, recordings, measurements, handling, winding, operations, sounding, timing or calibration actions, treatments, custody decisions, rights decisions, cultural decisions, or authority acts were used. Public sources supplied vocabulary and refusal conditions only. No empirical GMUT, operational THOS, production Freed ID, legal or cultural review, Māori authority, independent reproduction, exhaustive security, complete privacy or accessibility, AGI/ASI, consciousness/personhood, Theory-of-Everything proof, canon, or Stage 20 claim is made.

The D-isolated tools were portion 2.6.2, transitions 0.9.3, and cattrs 26.1.0, plus exact zero-credit sortedcontainers 2.4.0, six 1.17.0, attrs 26.1.0, and typing-extensions 4.16.0 runtime dependencies. Hashes matched; the seven-distribution audit had zero known vulnerabilities; positive and rejecting smokes passed; shared prefixes remained unchanged. Twenty phase-local skills and twenty family-current runners were quick-validated and used on synthetic fixtures. These are bounded owner-scoped checks only.

## Lifecycle and route

Source `{SOURCE_FINAL}` → x1 `{X1_COMMIT}` → evidence `{EVIDENCE_COMMIT}` → exact final as evidence's direct child is the only accepted lifecycle. The file-backed prospective handoff names `{SUCCESSOR_TITLE}` for `{SUCCESSOR_PHASE}` and remains `PREPARED_NOT_SENT` in the commit. `{STALE_REJECTED_LABEL}` is stale only. A later acknowledged exact-title message is external delivery evidence and must never rewrite commit-time truth.

## Proposal-by-proposal review

{cards}
"""


def build(repo: Path) -> None:
    root = repo / OWNER_ROOT
    evidence_truth = load_json(root / "x2/phase-truth-evidence.json")
    outcomes = load_json(root / "x2/outcome-ledger.json")
    x1_versions = load_json(root / "x1/tool-versions.json")
    final_counts = {
        "effective_negatives": evidence_truth["effective_negatives"] + len(FINAL_OPERATIONAL_FAILURES),
        "methods": evidence_truth["methods"] + len(FINAL_OPERATIONAL_FAILURES),
        "failed_witnesses": evidence_truth["failed_witnesses"] + len(FINAL_OPERATIONAL_FAILURES),
        "passing_witnesses": evidence_truth["passing_witnesses"] + len(FINAL_OPERATIONAL_FAILURES),
        "open_gaps": evidence_truth["open_gaps"],
        "exact_gates": evidence_truth["exact_gates"],
    }
    versions = [
        {"command": "python", "returncode": 0, "first_line": f"Python {x1_versions['python']}", "source": "immutable_x1_version_receipt", "replayed": False},
        {"command": "git", "returncode": 0, "first_line": x1_versions["git"], "source": "immutable_x1_version_receipt", "replayed": False},
        {"command": "node", "returncode": 0, "first_line": x1_versions["node"], "source": "immutable_x1_version_receipt", "replayed": False},
        {"command": "codex", "returncode": 0, "first_line": f"codex-cli {x1_versions['codex_cli']['version']}", "source": "immutable_x1_version_receipt", "replayed": False},
    ]
    write_json(root / "closeout/environment-version-receipt.json", {"schema": "ghc.family.environment-versions.v2", "owner": OWNER, "phase": PHASE, "updates_performed": False, "rows": versions})
    write_json(root / "closeout/final-operational-failures.json", {"schema": "ghc.family.post-evidence-operational-failures.v2", "count": len(FINAL_OPERATIONAL_FAILURES), "immutable_evidence_counts": {key: evidence_truth[key] for key in final_counts}, "effective_final_overlay": final_counts, "rows": FINAL_OPERATIONAL_FAILURES})
    write_json(root / "validation/x2-test-composite-receipt.json", {
        "schema": "ghc.family.x2-owner-test-composite.v2",
        "collection_only": {"invoked": False, "collected_tests": None, "tests_executed": 0, "credit": 0},
        "owner_suite": {"invocations": 2, "first_invocation_passed_tests": 22, "first_invocation_credit": 1, "second_invocation_passed_tests": 22, "second_invocation_credit": 0},
        "target_changed_refresh": {"reason": "VA6717-X2-OP-002 changed failure-derived counts and privacy target", "selected_tests": 22, "passed_tests": 22, "unchanged_successful_components_replayed": True, "classification": "RETAINED_UNNECESSARY_REPLAY_ZERO_AGGREGATE_SUCCESS_CREDIT"},
        "classification": "VALID_FIRST_OWNER_SCOPED_X2_PASS_WITH_LATER_ZERO_CREDIT_REPLAY",
        "complete_repository_suite": False,
        "independent_reproduction": False,
    })
    write_json(root / "closeout/phase-truth-final.json", {**evidence_truth, "schema": "ghc.family.phase-truth.v5", "lifecycle": "combined_closeout_content_seal_candidate", "source_final": SOURCE_FINAL, "x1_commit": X1_COMMIT, "evidence_commit": EVIDENCE_COMMIT, "final_commit": "resolve_direct_child_of_evidence_containing_this_record", "phase_commit_target": 3, "merge_target": 0, "immutable_evidence_counts": {key: evidence_truth[key] for key in final_counts}, **final_counts, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json(root / "closeout/completion-checklist.json", {
        "schema": "ghc.family.completion-checklist.v4", "owner": OWNER, "phase": PHASE,
        "complete": ["exact source verification", "planning-only x1 commit and equality", "forty frozen and executed proposals", "four exact outcome labels", "thirty-six positive controls", "one hundred sixty rejected mutations retained", "twenty owner-local skills", "twenty family-current runners", "three selected D-isolated tools plus four exact runtime dependencies", "dependency-complete seven-distribution audit", "Method Flow and gate registers", "accessible static report", "evidence staged review and exact manifests", "first 22/22 owner x2 tests credited once", "later unnecessary 22-test replay retained at zero aggregate-success credit", "combined closeout and content-seal candidate", "file-backed exact-title successor packet prepared but unsent"],
        "incomplete": ["universal novelty across 5,710 untested declared rows", "complete repository suite", "independent-team reproduction", "real object or participant evidence", "professional conservation mechanical timing calibration music education or safety validation", "production Freed ID lifecycle and governance", "governed blind matched-budget THOS arms", "empirical GMUT confirmation", "manual affected-user accessibility evaluation", "privacy or exhaustive-security completeness", "legal cultural affected-party or Māori-authority review", "Theory-of-Everything proof AGI ASI consciousness personhood canon or Stage 20 authority"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_text(root / "closeout/complete-incomplete.md", """# Vesper Arlen v671-v7 complete and incomplete\n\nComplete within owner-local synthetic scope are strict x1-before-x2 separation, forty frozen and executed proposal dispositions, thirty-six passing positive fixtures, 160 applied and rejected mutations, retained Method Flow, twenty skills, twenty runners, three selected isolated tools plus four exact dependencies, source and threat ledgers, structural accessibility, exact evidence manifests, and a closeout/content-seal packet that names Lyren Moss while preserving Vesper Rowan as a stale rejected source-owner label.\n\nIncomplete are universal novelty, the complete repository suite, independent reproduction, real people or object evidence, professional conservation, timing, calibration, music education, or safety competence, production identity lifecycle, governed THOS trials, empirical GMUT confirmation, complete privacy or accessibility, exhaustive security, legal or cultural review, Māori authority, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, and Stage 20 authority.\n\nTerminal verdict: `NOT_READY_FOR_STAGE_20`.\n""")
    write_json(root / "closeout/wellbeing-final.json", {"schema": "ghc.family.wellbeing-final.v3", "owner": OWNER, "phase": PHASE, "relational_identity_boundary": True, "role": "sequence-provenance cartographer and reversible-timing steward", "hope": "make event order, interval uncertainty, and correction legible without turning pattern into performance, measurement, or authority", "workload_within_declared_caps": True, "materialized_file_ceiling": 2000, "safe_stop_conditions_visible": True, "no_claim_of_consciousness_personhood_continuity_qualification_or_authority": True})
    write_text(root / "final/integrated-overview.md", final_overview(repo, final_counts))
    packet = activation_packet(repo, final_counts)
    packet_path = root / "handoffs/lyren-moss-v671-v8-activation-candidate.md"
    write_text(packet_path, packet)
    packet_bytes = (packet.rstrip() + "\n").encode("utf-8")
    write_json(root / "handoffs/lyren-moss-v671-v8-activation-candidate-receipt.json", {"schema": "ghc.family.prepared-baton-receipt.v4", "recipient_exact_title": SUCCESSOR_TITLE, "stale_rejected_source_owner_labels": [STALE_REJECTED_LABEL], "prospective_phase": SUCCESSOR_PHASE, "bytes": len(packet_bytes), "whitespace_words": len(packet.split()), "sha256": hashlib.sha256(packet_bytes).hexdigest(), "integrity_domain": "normalized_lf_working_file_before_commit", "route_state": "PREPARED_NOT_SENT", "prepared_not_sent": True, "sent_by_vesper_arlen": False, "delivery_acknowledged": False})
    write_json(root / "route/route-state.json", {"schema": "ghc.family.route-state.v5", "owner": OWNER, "phase": PHASE, "recipient_exact_title": SUCCESSOR_TITLE, "stale_rejected_source_owner_labels": [STALE_REJECTED_LABEL], "prospective_successor_phase": SUCCESSOR_PHASE, "state": "PREPARED_NOT_SENT", "prepared_not_sent": True, "sent_by_vesper_arlen": False, "delivery_acknowledged": False, "precontact_during_execution": False, "substitution_permitted": False, "terminal_requirements": ["exact final committed and pushed", "clean 0/0 state", "fresh four-way equality", "one exact-final canonical success", "newest live instruction roster and auth reread", "unique exact-title resolution", "immediate task reread", "duplicate and pause guard", "one target-identifying acknowledged send"]})
    write_json(root / "seal/seal-candidate.json", {"schema": "ghc.family.combined-closeout-content-seal.v5", "owner": OWNER, "phase": PHASE, "source_final": SOURCE_FINAL, "x1_commit": X1_COMMIT, "evidence_commit": EVIDENCE_COMMIT, "final_commit": "resolve_direct_child_of_evidence_containing_this_seal", "outcomes": outcomes["counts"], **final_counts, "immutable_evidence_counts": {key: evidence_truth[key] for key in final_counts}, "x2_test_state": "VALID_FIRST_OWNER_SCOPED_X2_PASS_WITH_LATER_ZERO_CREDIT_REPLAY", "x2_owner_tests_first_credit": 22, "x2_owner_tests_later_replay_zero_credit": 22, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "delivery_state": "PREPARED_NOT_SENT"})
    write_json(root / "closeout/closeout-receipt.json", {"schema": "ghc.family.closeout-receipt.v5", "owner": OWNER, "phase": PHASE, "source_final": SOURCE_FINAL, "x1_commit": X1_COMMIT, "evidence_commit": EVIDENCE_COMMIT, "outcomes": outcomes["counts"], "immutable_evidence_counts": {key: evidence_truth[key] for key in final_counts}, "effective_counts": final_counts, "x2_test_composite": "first 22/22 credited once; later 22/22 replay retained at zero aggregate-success credit", "privacy_complete_claim": False, "accessibility_complete_claim": False, "independent_reproduction_claim": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "PREPARED_NOT_SENT"})
    write_json(root / "validation/final-validation-plan.json", {"schema": "ghc.family.exact-final-validation-plan.v4", "owner": OWNER, "phase": PHASE, "invocation_limit": 1, "run_only_after": ["combined final commit", "push", "clean state", "typed 0/0 divergence", "fresh four-way equality"], "dependencies": ["exact head and direct ancestry", "three single-parent phase commits and zero merges", "exact x1 evidence final-delta and final-owner manifest replays", "all owner JSON parses", "five-class privacy scan", "bounded Python AST review", "new final test module", "x2 suite and target-changed refresh distinction", "accessible report structure", "baton integrity and ten-thousand-word floor", "clean state and fresh equality"], "post_success_replay": False, "external_receipt_only": True})


def staged_review(repo: Path) -> None:
    names = run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "HEAD").stdout.splitlines()
    prefixes = [f"{OWNER_ROOT_POSIX}/closeout/", f"{OWNER_ROOT_POSIX}/final/", f"{OWNER_ROOT_POSIX}/handoffs/", f"{OWNER_ROOT_POSIX}/route/", f"{OWNER_ROOT_POSIX}/seal/", f"{OWNER_ROOT_POSIX}/validation/final-", f"{OWNER_ROOT_POSIX}/validation/x2-test-composite-receipt.json"]
    exact = {"scripts/build_ghc_family_vesper_arlen_v671_v7_final.py", "scripts/validate_ghc_family_vesper_arlen_v671_v7_final.py", "tests/test_ghc_family_vesper_arlen_v671_v7_final.py"}
    disallowed = [name for name in names if name not in exact and not any(name.startswith(prefix) for prefix in prefixes)]
    exclusions = {f"{OWNER_ROOT_POSIX}/validation/final-staged-review.json", f"{OWNER_ROOT_POSIX}/validation/final-delta-manifest.json", f"{OWNER_ROOT_POSIX}/validation/final-owner-manifest.json"}
    json_errors: list[str] = []
    privacy: list[dict[str, str]] = []
    for relpath in names:
        if relpath in exclusions:
            continue
        data = subprocess.run(["git", "show", f":{relpath}"], cwd=repo, check=True, capture_output=True).stdout
        text = data.decode("utf-8", errors="replace")
        if relpath.endswith(".json"):
            try:
                json.loads(text)
            except Exception as exc:  # noqa: BLE001
                json_errors.append(f"{relpath}:{type(exc).__name__}")
        privacy.extend({"path": relpath, **row} for row in privacy_candidates(text))
    diff_exit = run(repo, "git", "diff", "--cached", "--check").returncode
    receipt = {"schema": "ghc.family.final-staged-review.v4", "owner": OWNER, "phase": PHASE, "staged_entry_count_before_self": len(names), "disallowed_paths": disallowed, "json_errors": json_errors, "privacy_candidates": privacy, "diff_cached_exit": diff_exit, "passed": not disallowed and not json_errors and not privacy and diff_exit == 0, "self_exclusions": sorted(exclusions)}
    write_json(repo / OWNER_ROOT / "validation/final-staged-review.json", receipt)
    if not receipt["passed"]:
        raise RuntimeError("final staged review failed closed")


def manifests_from_index(repo: Path) -> None:
    names = run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "HEAD").stdout.splitlines()
    exclusions = [f"{OWNER_ROOT_POSIX}/validation/final-staged-review.json", f"{OWNER_ROOT_POSIX}/validation/final-delta-manifest.json", f"{OWNER_ROOT_POSIX}/validation/final-owner-manifest.json"]
    delta = []
    for relpath in sorted(name for name in names if name not in exclusions):
        data = subprocess.run(["git", "show", f":{relpath}"], cwd=repo, check=True, capture_output=True).stdout
        delta.append({"path": relpath, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    owner_names = set(names)
    owner_names.update(run(repo, "git", "ls-tree", "-r", "--name-only", "HEAD", OWNER_ROOT_POSIX, "scripts", "tests").stdout.splitlines())
    owner = []
    for relpath in sorted(owner_names):
        if relpath in exclusions:
            continue
        if not (relpath.startswith(f"{OWNER_ROOT_POSIX}/") or (relpath.startswith("scripts/") and ("vesper_arlen_v671_v7" in relpath or relpath.startswith("scripts/ghc_family_metronome_"))) or (relpath.startswith("tests/") and "vesper_arlen_v671_v7" in relpath)):
            continue
        spec = f":{relpath}" if relpath in names else f"HEAD:{relpath}"
        data = subprocess.run(["git", "show", spec], cwd=repo, check=True, capture_output=True).stdout
        owner.append({"path": relpath, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    common = {"schema": "ghc.family.content-manifest.v5", "owner": OWNER, "phase": PHASE, "self_exclusions": exclusions}
    root = repo / OWNER_ROOT / "validation"
    write_json(root / "final-delta-manifest.json", {**common, "domain": "final_exact_staged_git_blobs", "entry_count": len(delta), "entries": delta})
    write_json(root / "final-owner-manifest.json", {**common, "domain": "owner_exact_evidence_head_plus_final_staged_git_blobs", "entry_count": len(owner), "entries": owner})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--review-staged", action="store_true")
    parser.add_argument("--manifests-from-index", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.review_staged:
        staged_review(repo)
    elif args.manifests_from_index:
        manifests_from_index(repo)
    else:
        build(repo)


if __name__ == "__main__":
    main()
