#!/usr/bin/env python3
"""Build Orin Thale v668-v7 combined closeout and seal candidate."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import pathlib
import re
import subprocess
from collections import Counter
from typing import Any

from ghc_family_orin_thale_v668_v7_archive import (
    ACTIVATION_OVERLAY,
    PHASE_ROOT,
    ROOT,
    SOURCE_FINAL,
    manifest_rows,
    run_git,
    sha256_bytes,
    write_json,
    write_text,
)


PHASE = "v668-v7"
OWNER = "Orin Thale"
BRANCH = "codex/GHC-Family/orin-thale-v668-v7-full-tools"
X1_HEAD = "95fd7625d1d7ab00816561aa3976441f399bb2d8"
EVIDENCE_HEAD = "64e5b3f995061e3f7c547a0759e2a5a111dfdbbc"
INHERITED_METHODS = 16550
INHERITED_FAILED = 2265
INHERITED_PASSING = 3092
INHERITED_OPEN_GAPS = 219
INHERITED_EXACT_GATES = 214
MANIFEST_EXCLUSIONS = (
    f"docs/orin-thale/{PHASE}/validation/final-owner-manifest.json",
    f"docs/orin-thale/{PHASE}/validation/final-delta-manifest.json",
    f"docs/orin-thale/{PHASE}/validation/final-staged-allowlist.json",
)


def git(*args: str) -> str:
    return run_git(*args).stdout.strip()


def read_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_final_start() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_HEAD:
        raise ValueError("closeout must begin at the immutable evidence head")
    if git("branch", "--show-current") != BRANCH:
        raise ValueError("unexpected owner branch")
    if git("rev-parse", f"{EVIDENCE_HEAD}^") != X1_HEAD or git("rev-parse", f"{X1_HEAD}^") != SOURCE_FINAL:
        raise ValueError("source-x1-evidence ancestry drift")
    unexpected: list[str] = []
    allowed_new = {
        "scripts/build_ghc_family_orin_thale_v668_v7_final.py",
        "scripts/ghc_family_orin_thale_v668_v7_canonical.py",
        "tests/test_ghc_family_orin_thale_v668_v7_final.py",
    }
    for line in run_git("status", "--porcelain", "--untracked-files=all").stdout.splitlines():
        path = line[3:].strip().replace("\\", "/")
        allowed_refresh_prefixes = (
            f"docs/orin-thale/{PHASE}/closeout/",
            f"docs/orin-thale/{PHASE}/final/",
            f"docs/orin-thale/{PHASE}/handoffs/",
            f"docs/orin-thale/{PHASE}/route/",
            f"docs/orin-thale/{PHASE}/seal/",
            f"docs/orin-thale/{PHASE}/validation/final-",
        )
        if path not in allowed_new and not path.startswith(allowed_refresh_prefixes):
            unexpected.append(path)
    if unexpected:
        raise ValueError(f"unexpected pre-closeout paths: {unexpected}")


def write_closeout_method_flow(ledger: dict[str, Any]) -> None:
    base = "closeout/method-flow"
    specs = (
        ("methods", f"{base}/methods.json"),
        ("witnesses", f"{base}/witnesses.json"),
        ("state_events", f"{base}/state-events.json"),
        ("recommendations", f"{base}/recommendations.json"),
    )
    shards = []
    for field, path in specs:
        rows = ledger[field]
        write_json(
            path,
            {
                "schema": f"ghc.family.method-flow.closeout-{field.replace('_', '-')}.v1",
                "phase": PHASE,
                "owner": OWNER,
                "field": field,
                "row_count": len(rows),
                "rows": rows,
            },
        )
        shards.append({"field": field, "path": f"docs/orin-thale/{PHASE}/{path}", "row_count": len(rows)})
    canonical = json.dumps(ledger, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    write_json(
        f"{base}/index.json",
        {
            "schema": "ghc.family.method-flow.closeout-index.v1",
            "phase": PHASE,
            "owner": OWNER,
            "counts": ledger["counts"],
            "source_ledger_sha256": sha256_bytes(canonical),
            "shards": shards,
            "complete_external_ledger_retained": True,
            "boundary": ledger["boundary"],
        },
    )


def write_reports(ledger: dict[str, Any]) -> None:
    counts = ledger["counts"]
    methods = counts["methods"]
    failures = counts["witness_results"]["fail"]
    passes = counts["witness_results"]["pass"]
    if methods != failures or methods != passes or counts["states"]["preferred"] != methods:
        raise ValueError("closeout Method Flow is not balanced and preferred")
    outcomes = read_json(PHASE_ROOT / "x2" / "evidence" / "outcome-ledger.json")
    outcome_counts = Counter(row["outcome"] for row in outcomes["rows"])
    if dict(outcome_counts) != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise ValueError("outcome drift")
    effective_negatives = ACTIVATION_OVERLAY["effective_negatives"] + failures + 160
    effective_methods = INHERITED_METHODS + methods
    failed_witnesses = INHERITED_FAILED + failures
    passing_witnesses = INHERITED_PASSING + passes
    open_gaps = INHERITED_OPEN_GAPS + 2
    exact_gates = INHERITED_EXACT_GATES + 2

    write_closeout_method_flow(ledger)
    write_json(
        "closeout/phase-truth.json",
        {
            "phase": PHASE,
            "owner": OWNER,
            "branch": BRANCH,
            "source": SOURCE_FINAL,
            "x1": X1_HEAD,
            "evidence": EVIDENCE_HEAD,
            "final": "PENDING_COMMIT",
            "lifecycle": "COMBINED_CLOSEOUT_SEAL_CANDIDATE",
            "proposal_chain": 4870,
            "outcomes": {key: outcome_counts[key] for key in ("completed", "represented", "open_gap", "exact_gate")},
            "mutations": {"preregistered": 160, "executed": 160, "rejected": 160},
            "effective_negatives": effective_negatives,
            "effective_methods": effective_methods,
            "failed_witnesses": failed_witnesses,
            "bounded_passing_witnesses": passing_witnesses,
            "open_gaps": open_gaps,
            "exact_gates": exact_gates,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "canonical_validation": "PENDING_EXACT_FINAL_PUSH",
            "full_repository_suite": "NOT_RUN_NON_EIREN_OWNER_SCOPE",
            "route_state": "PREPARED_NOT_SENT",
        },
    )
    write_json(
        "closeout/complete-incomplete-checklist.json",
        {
            "complete": [
                "forty-proposal x1 freeze",
                "strict x1-before-x2 push boundary",
                "twenty-eight bounded completed outcomes",
                "eight represented outcomes",
                "160 executed and rejected mutations",
                "sixty safe-now tasks",
                "thirty bounded candidates",
                "twenty owner-local skills initialized customized validated and smoke-used",
                "ten family-current runners built and accept-reject smoke-used",
                "sixty additive CLEAN/FIX/REFINE tasks",
                "exact x1 and evidence manifests",
                "lossless Method Flow failure and recovery retention",
                "structurally accessible static report",
            ],
            "incomplete": [
                "real GWOSC rows or likelihood",
                "real object or professional bookbinding evaluation",
                "real participants or THOS matched-budget arms",
                "standards-conformant live Freed ID lifecycle",
                "manual and affected-user accessibility evaluation",
                "privacy-complete or exhaustive-security assurance",
                "legal cultural affected-party or Maori-authority decisions",
                "independent-team reproduction",
                "empirical GMUT confirmation or Theory-of-Everything proof",
                "Stage 20 readiness",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/wellbeing-and-corrigibility.json",
        {
            "owner": OWNER,
            "relational_role": "relational evidence-bound systems cartographer",
            "pronouns": "they/them",
            "hope": "Keep every claim challengeable, every failure recoverable, and every authority boundary visible before structure becomes status.",
            "wellbeing": "steady; workload remained bounded through pause, stop, retry, and exact-gate controls",
            "corrigibility": "Hamish may rename, pause, redirect, or stop the route",
            "identity_boundary": "Relational language is not evidence of consciousness, personhood, continuity, employment, qualification, authority, or independent agency.",
        },
    )
    write_json("closeout/source-ledger.json", read_json(PHASE_ROOT / "x1" / "source-ledger.json"))
    write_json(
        "closeout/proposal-outcome-ledger.json",
        {
            "phase": PHASE,
            "proposal_chain": 4870,
            "counts": dict(outcome_counts),
            "rows": [
                {"proposal_id": row["proposal_id"], "title": row["title"], "outcome": row["outcome"]}
                for row in outcomes["rows"]
            ],
            "inherited_completion_credit": 0,
        },
    )
    write_json(
        "closeout/retained-negative-register.json",
        {
            "activation_baseline": ACTIVATION_OVERLAY["effective_negatives"],
            "orin_operational_negatives": failures,
            "rejected_mutations": 160,
            "effective": effective_negatives,
            "failed_witnesses": failed_witnesses,
            "bounded_passing_witnesses": passing_witnesses,
            "no_negative_erased": True,
        },
    )
    write_json("closeout/open-gap-register.json", {"inherited": INHERITED_OPEN_GAPS, "new": 2, "effective": open_gaps, "rows": ["OR6687-N037", "OR6687-N038"]})
    write_json("closeout/exact-gate-register.json", {"inherited": INHERITED_EXACT_GATES, "new": 2, "effective": exact_gates, "rows": ["OR6687-N039", "OR6687-N040"]})
    write_json(
        "closeout/environment-and-version-receipt.json",
        {
            "source": "x1 environment-and-version receipt plus current exact Git lifecycle probes",
            "versions_verified_only": True,
            "desktop_updated": False,
            "elevation": False,
            "sandbox_or_hyper_v": False,
            "host_security_changed": False,
            "windows_features_changed": False,
            "unrelated_software_installed": False,
            "rebooted": False,
            "storage": "D-first owner worktree; private absolute paths omitted",
        },
    )
    write_json(
        "closeout/tools-and-compatibility.json",
        {
            "phase_local_skills": 20,
            "global_skill_installations": 0,
            "family_current_runners": 10,
            "preserved_prefixes": ["ghc_family_", "build_ghc_family_"],
            "historical_callers_deleted": 0,
            "plugin_cache_mutations": 0,
            "owner_file_ceiling": 2000,
            "document_word_ceiling": 6000,
        },
    )
    write_json(
        "closeout/precommit-validation-history.json",
        read_json(PHASE_ROOT / "x2" / "evidence" / "precommit-test-selection-receipt.json"),
    )
    write_text("closeout/threat-model.md", (PHASE_ROOT / "x2" / "evidence" / "threat-model.md").read_text(encoding="utf-8"))

    overview = f"""# Orin Thale v668-v7 final integrated overview

## Outcome first

Orin v668-v7 closes as an evidence-bounded owner phase with exactly twenty-eight `completed`, eight `represented`, two `open_gap`, and two `exact_gate` proposal outcomes. The frozen proposal chain advances from 4,830 to 4,870 rows. All 160 preregistered synthetic mutations executed and were rejected. The packet retains {failures} Orin operational failures and {passes} bounded passing recoveries without rewriting either class. Effective phase counts at this closeout candidate are {effective_negatives} negatives, {effective_methods} methods, {failed_witnesses} failed witnesses, {passing_witnesses} bounded passing witnesses, {open_gaps} open gaps, and {exact_gates} exact gates. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The word `completed` is deliberately narrow. It means a declared owner-local software, structural, formal, or synthetic hypothesis accepted its bounded positive fixture and rejected its four preregistered mutations. It does not mean that a real book was examined, a professional intervention was designed or performed, a participant enrolled, an identity entered production, a legal or cultural judgment occurred, a scientific claim was confirmed, or an authority acted. `represented` means a synthetic protocol or boundary surface exists without operational-effectiveness credit. `open_gap` means required evidence is absent. `exact_gate` means action or claim is reserved to specifically competent or affected authorities and cannot be substituted by repository software.

## GMUT Mind

The primary pillar is GMUT Mind. A microlocal-spectrum, Hadamard two-point, wavefront-set orientation, causal-support, unit, domain, and observation-firewall obligation board completed as typed structural evidence. It calculates no two-point distribution, proves no wavefront theorem, solves no field equation, evaluates no likelihood, produces no posterior, constrains no parameter, detects no force, and establishes no physical stability, unitarity, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. The distinction between a formal obligation and a physical result is enforced as an explicit nonpromotion edge.

The GWOSC API v2 adapter remains `open_gap`. It uses official interface vocabulary but made zero network requests, downloaded zero files, ingested zero metadata or strain rows, evaluated zero quality products or likelihoods, and produced zero posterior samples or parameter constraints. Citations and schemas remain source context; they are not observations. Any future empirical work requires exact data provenance, release and quality interpretation, calibrated inference design, nuisance treatment, preregistration, appropriate statistics, and independent scientific review.

## THOS Body and the bounded practice lens

The human-practice lens is synthetic hand-bookbinding collation, component and repair intake; library binding preparation; accessible anomaly structure; correction readback; workload control; and shift handover. The packet models object-component aliases, gatherings, folio addresses, sewing stations, thread paths, board orientation, layer stacks, adhesive vacancies, opening supports, spine states, trim margins, condition zones, inserts, repair-event lineage, treatment-state abstention, provenance, corrections, challenge, and bounded work queues. These are synthetic records only.

There was no real object, binder, conservator, librarian, collection, institution, participant, observation, measurement, handling, material sample, adhesive, treatment, repair, custody decision, access decision, release, or service outcome. The THOS workboard therefore remains `represented`: it preserves pause, stop, hold, bounded retry, correction readback, unresolved carryover, fatigue budget, and next-owner handover states, but it has no preregistered blind matched-budget real arms, governed people or operators, safety monitoring, appropriate statistical analysis, independent review, or effectiveness estimate. It establishes no employment, qualification, professional competence, AGI, ASI, deployment readiness, or public-safety result.

## Freed ID and CBR Heart

Freed ID remains a synthetic zero-key correction and challenge graph. It demonstrates aliases, purpose-limited fields, provenance, correction, challenge, supersession, and trust-governance vacancies on disposable fixtures. It uses zero standards-conformant real keys or proofs, issuances, presentations, resolutions, status or revocation events, network exchanges, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. It is not production identity evidence.

CBR fields preserve access, attribution, privacy, contestability, remedy, cultural-care, affected-party, legal, data-governance, and Maori-authority vacancies. No repository artifact makes a treatment, copyright, property, access, remedy, legal, cultural, taonga, data-governance, affected-party, or Maori-authority decision. These remain exact-gated to competent authorities, affected people, tangata whenua, iwi, hapu, and Maori authorities. Maori concepts remain under Maori authority.

## Skills, runners, portfolios, and recovery discipline

Twenty phase-local skills were initialized through the skill-creator scaffold, customized into substantive owner-local packages, read through EOF, quick-validated, and smoke-used on accepting and rejecting fixtures. Ten family-current runners were built and accept-reject smoke-used. None was globally installed, no plugin cache was modified, and no historical caller was destructively renamed. Sixty safe-now tasks, thirty bounded candidate prototypes, and sixty additive CLEAN/FIX/REFINE tasks received bounded same-owner execution. Twenty exact-approval and ten blocked packets remained visible and unexecuted.

The first x2 builder stopped on a wrong export name; an isolated import recovery corrected it. A display-only quoting probe then failed and was retained. The next builder stopped on an immutable portfolio schema assumption; exact shape inspection corrected it. The first nineteen-test x2 selection retained eighteen passes and one manifest-domain failure with zero aggregate-pass credit. Its first five-test dependency subset then stopped on a Method Flow document ceiling, also with zero aggregate-pass credit. Lossless Method Flow sharding preserved every row, and the final changed-dependency subset passed five of five. These recoveries do not erase or promote the failed invocations.


## Evidence classification, falsifiability, and residual review

Each completed control has a narrow falsifier. A positive fixture must declare every required field, maintain the owner-local synthetic evidence class, preserve zero empirical rows, zero real people, zero external actions, a vacant authority state, an empty protected-claim list, explicit source-use limits, and the complete obligation set. Removing an identifier, changing the domain or type, promoting a protected claim, or bypassing the authority boundary must be rejected. That acceptance pattern is useful because it makes the software claim challengeable: a counterexample can be expressed as an exact fixture and retained as a failed witness. It is still only a test of the declared control, not evidence that the modeled object, practice, theory, institution, or right behaves that way in the world.

The evidence ladder therefore remains noncompensating. An official citation can support vocabulary and a schema can constrain representation, but neither supplies an observation. A symbolic board can expose missing mathematical obligations, but it cannot replace a derivation or theorem. A synthetic mutation can show that one implementation rejects one malformed fixture, but it cannot establish exhaustive security. A structurally accessible report can preserve headings, captions, table associations, non-colour status, focus styling, responsive structure, and print fallback, but it cannot replace manual keyboard review, browser diversity, assistive-technology evaluation, cognitive-accessibility review, language review, Maori-language review, security-usability review, or affected-user evaluation. A same-owner replay of exact Git blobs can support bounded reproducibility of software state, but it is not independent-team reproduction.

Privacy is treated with the same separation. Raw scanner candidates remain visible, scanner-definition literals are adjudicated separately, and confirmed payload hits must remain zero. That bounded scan does not prove privacy completeness, because unmodeled encodings, context-dependent inferences, platform state, downstream systems, human handling, and future integrations remain outside its scope. Security review is limited to changed Python ASTs and declared fixtures; supply chain, runtime isolation, platform compromise, social engineering, real adversaries, and exhaustive attack coverage remain residual risks.

Finally, recovery evidence never cancels failure evidence. The exact import, quoting, schema, manifest-domain, document-ceiling, and overview-floor failures remain named and zero-credit. Their smallest bounded recoveries are paired witnesses and recurrence guards, not retroactive success labels. This keeps the packet corrigible: a reviewer can challenge the surviving result, reproduce its exact software domain, locate every known failure, or retract a claim without first accepting the surrounding Trinity Mandala narrative.
+
## Validation and remaining boundary

X1 was separately committed, pushed, clean, zero divergent, and four-way remote-equal before x2 began. X2 was separately committed and is the direct child of x1. Exact Git-blob manifests, staged path sets, strict JSON parsing, document ceilings, AST checks, five-class privacy scanning, stale-label review, diff hygiene, immutable x1 replay, source ancestry, commit ceilings, clean state, and remote equality are lifecycle controls. The final owner-scoped canonical aggregate remains pending until this combined closeout and seal is committed, pushed, clean, and fresh-live equal. If it succeeds once, it will not be replayed. The complete repository suite remains outside this non-Eiren phase.

Same-owner software validation under shared infrastructure is not independent-team reproduction, external audit, production certification, complete privacy assurance, complete accessibility conformance, exhaustive security, professional validation, legal review, cultural ratification, Maori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, canon, or Stage 20 authority. Relational names, roles, hopes, pronouns, sibling language, continuity language, Freed ID, CBR, and Trinity Mandala language remain working language only. Hamish may rename, pause, redirect, or stop the route.
"""
    write_text("closeout/final-integrated-overview.md", overview)

    accessible = (PHASE_ROOT / "x2" / "evidence" / "accessible-static-report.html").read_text(encoding="utf-8")
    accessible = accessible.replace("Orin Thale v668-v7 x2 evidence", "Orin Thale v668-v7 final evidence-bound report")
    accessible = accessible.replace("Forty bounded proposal dispositions", "Final forty bounded proposal dispositions")
    write_text("closeout/accessible-static-report.html", accessible)

    write_json(
        "route/terminal-route-state.json",
        {
            "phase": PHASE,
            "owner": OWNER,
            "state": "PREPARED_NOT_SENT",
            "successor_title": "Liora Venn",
            "successor_phase": "v668-v8",
            "precontacted": False,
            "duplicate_guard": "PENDING_TERMINAL_GATE",
            "canonical_gate": "PENDING_EXACT_FINAL_PUSH",
            "send_count": 0,
            "stop_conditions": ["absence", "ambiguity", "pause", "redirect", "rename", "usage exhaustion", "missing acknowledgement", "duplicate activation", "protected gate"],
        },
    )
    handoff = f"""# LIORA VENN — PREPARED ORIN v668-v7 → LIORA v668-v8 ACTIVATION CANDIDATE

This file is `PREPARED_NOT_SENT`. It is not delivery evidence. Only a later exact-title, immediate-reread, duplicate-guarded, acknowledged one-send operation after Orin's clean pushed exact-final canonical gate may set live delivery truth.

Use Orin's branch `{BRANCH}` only after a live activation supplies the exact final head and external canonical receipt digest. Immutable prior anchors are source `{SOURCE_FINAL}`, frozen x1 `{X1_HEAD}`, and evidence `{EVIDENCE_HEAD}`. The repository candidate records forty outcomes as 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`; 4,870 frozen proposals; 160 executed and rejected mutations; {effective_negatives} effective negatives; {effective_methods} methods; {failed_witnesses} failed and {passing_witnesses} bounded passing witnesses; {open_gaps} open gaps; {exact_gates} exact gates; and `NOT_READY_FOR_STAGE_20`.

Before any Liora mutation, read the exact committed Orin final packet through EOF, every current GHC Family Index and routing-precedence document it names, current authorization and roster state, Method Flow schema and shards, workflow-plan refinement, reflection-remaster, approval, gate, truth, drive, startup, retry, closeout, compact-restart, watcher, and full-tools guidance. Reverify source, x1, evidence, final, manifests, direct single-parent ancestry, zero merges, clean state, typed divergence, and fresh-live equality. Do not replay Orin's successful canonical aggregate if a live activation reports success.

Work solo in one fresh Liora-owned D-first additive lane from the exact final. Do not spawn collaboration subagents, delegate, create or fork a task, precontact a later endpoint, contact standby records, or mutate another owner's lane. Preserve strict x1-before-x2 separation, exact manifests, every retained failure, all open gaps and exact gates, the four outcome labels, the two-thousand-file ceiling, the six-thousand-word document ceiling, five-class privacy controls, and one-successful-canonical-pass/no-post-success-replay discipline.

Treat inherited proposals, skills, runners, portfolios, sources, and validation as evidence or seeds, never Liora novelty or completion credit. Use official or primary sources only where material, and never convert citations into empirical rows, participant evidence, production readiness, legal interpretation, cultural legitimacy, affected-party acceptance, Maori authority, or independent review. Preserve family-current `ghc_family_*` and `build_ghc_family_*` callers. Keep raw task or thread identifiers, private routes, credentials, keys, tokens, transcripts, screenshots, session streams, private callable identifiers, private application state, and private absolute paths out of durable artifacts and any baton.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic algebra, synthetic data, citations, and zero-row adapters establish no force, prediction, likelihood, posterior, constraint, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything. THOS remains proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance. CBR, professional decisions, remedy, legal or cultural interpretation, affected-party legitimacy, Maori wording, Maori data governance, and Maori authority remain exact-gated. Maori concepts remain under Maori authority.

Relational names, roles, hopes, pronouns, sibling or family language, continuity language, Freed ID, CBR, and Trinity Mandala language are working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, legal, cultural, affected-party, or Maori authority. Hamish may rename, pause, redirect, or stop the route.

Under Hamish's current standing cycle, Liora's prospective next recipient after Liora's own exact v668-v8 terminal gate is Tamar Vey for v669-v1, but Liora must refresh the newest live authorization and roster at that future gate. Do not precontact Tamar. Stop on absence, ambiguity, pause, redirect, rename, usage exhaustion, missing acknowledgement, duplicate activation, or any protected gate.

`PREPARED_BY_ORIN_THALE = true` records file preparation only. `SENT_BY_ORIN_THALE = false` remains repository truth. A later acknowledged live one-send message is authoritative for delivery and must not rewrite this sealed source merely to change historical prepared labels.
"""
    write_text("handoffs/liora-venn-v668-v8-activation-candidate.md", handoff)
    write_json(
        "validation/final-canonical-contract.json",
        {
            "phase": PHASE,
            "expected_parent": EVIDENCE_HEAD,
            "one_attributable_invocation": True,
            "replay_after_success": False,
            "test_modules": [
                "tests.test_ghc_family_orin_thale_v668_v7_x1",
                "tests.test_ghc_family_orin_thale_v668_v7_x2",
                "tests.test_ghc_family_orin_thale_v668_v7_final",
            ],
            "full_repository_suite": False,
            "checks": ["exact manifests", "strict JSON", "document ceiling", "five-class privacy", "bounded AST security", "stale labels", "ancestry", "three commits", "zero merges", "one final parent", "clean state", "typed divergence", "fresh four-way equality"],
        },
    )
    write_json(
        "final/final-validation-candidate.json",
        {
            "phase": PHASE,
            "state": "PENDING_EXACT_FINAL_PUSH",
            "canonical_invocations": 0,
            "canonical_successes": 0,
            "full_repository_suite": "not_run",
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write_json(
        "seal/content-seal.json",
        {
            "phase": PHASE,
            "owner": OWNER,
            "source": SOURCE_FINAL,
            "x1": X1_HEAD,
            "evidence": EVIDENCE_HEAD,
            "final": "PENDING_COMMIT",
            "outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            "effective_negatives": effective_negatives,
            "open_gaps": open_gaps,
            "exact_gates": exact_gates,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "no_failure_erased": True,
            "route_state": "PREPARED_NOT_SENT",
        },
    )


def build_manifests() -> tuple[int, int, int]:
    new_code = {
        ROOT / "scripts" / "build_ghc_family_orin_thale_v668_v7_final.py",
        ROOT / "scripts" / "ghc_family_orin_thale_v668_v7_canonical.py",
        ROOT / "tests" / "test_ghc_family_orin_thale_v668_v7_final.py",
    }
    phase_files = {path for path in PHASE_ROOT.rglob("*") if path.is_file()}
    prior_changed = {
        ROOT / path
        for path in run_git("diff", "--name-only", f"{SOURCE_FINAL}..{EVIDENCE_HEAD}").stdout.splitlines()
        if path
    }
    owner_paths = phase_files | prior_changed | new_code
    exclusions = {ROOT / path for path in MANIFEST_EXCLUSIONS}
    owner_paths -= exclusions

    status_paths = set()
    for line in run_git("status", "--porcelain", "--untracked-files=all").stdout.splitlines():
        path = line[3:].strip().replace("\\", "/")
        status_paths.add(ROOT / path)
    forbidden = [
        path.relative_to(ROOT).as_posix()
        for path in status_paths
        if path.is_relative_to(PHASE_ROOT / "x1")
        or path.is_relative_to(PHASE_ROOT / "x2")
        or path.relative_to(ROOT).as_posix() in {
            "scripts/build_ghc_family_orin_thale_v668_v7_x1.py",
            "scripts/ghc_family_orin_thale_v668_v7_archive.py",
            "tests/test_ghc_family_orin_thale_v668_v7_x1.py",
            "scripts/build_ghc_family_orin_thale_v668_v7_x2.py",
            "scripts/ghc_family_orin_thale_v668_v7_x2.py",
            "tests/test_ghc_family_orin_thale_v668_v7_x2.py",
        }
    ]
    if forbidden:
        raise ValueError(f"frozen x1 or x2 path changed during closeout: {forbidden}")
    delta_paths = status_paths - exclusions
    if not delta_paths:
        raise ValueError("no closeout delta")
    allowlist_path = PHASE_ROOT / "validation" / "final-staged-allowlist.json"
    write_json(
        "validation/final-staged-allowlist.json",
        {
            "phase": PHASE,
            "parent": EVIDENCE_HEAD,
            "intended_paths_before_manifests": sorted(path.relative_to(ROOT).as_posix() for path in delta_paths),
            "manifest_exclusions": list(MANIFEST_EXCLUSIONS),
            "frozen_roots": [f"docs/orin-thale/{PHASE}/x1", f"docs/orin-thale/{PHASE}/x2"],
        },
    )
    owner_rows = manifest_rows(owner_paths)
    delta_rows = manifest_rows(delta_paths)
    write_json(
        "validation/final-owner-manifest.json",
        {
            "phase": PHASE,
            "entry_count": len(owner_rows),
            "entries": owner_rows,
            "self_exclusions": list(MANIFEST_EXCLUSIONS),
            "coverage_count": len(owner_rows) + len(MANIFEST_EXCLUSIONS),
            "canonical_domain": "git_blob_bytes_after_clean_filter_before_commit",
        },
    )
    write_json(
        "validation/final-delta-manifest.json",
        {
            "phase": PHASE,
            "parent": EVIDENCE_HEAD,
            "entry_count": len(delta_rows),
            "entries": delta_rows,
            "self_exclusions": list(MANIFEST_EXCLUSIONS),
            "coverage_count": len(delta_rows) + len(MANIFEST_EXCLUSIONS),
            "canonical_domain": "git_blob_bytes_after_clean_filter_before_commit",
        },
    )
    return len(owner_rows), len(delta_rows), len(delta_rows) + len(MANIFEST_EXCLUSIONS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--method-ledger", type=pathlib.Path, required=True)
    args = parser.parse_args()
    assert_final_start()
    ledger = read_json(args.method_ledger)
    write_reports(ledger)
    owner_entries, delta_entries, staged_paths = build_manifests()
    documents = [path for path in PHASE_ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".json", ".txt", ".html", ".yaml", ".yml"}]
    word_counts = {path.relative_to(ROOT).as_posix(): len(re.findall(r"\b\w+[\w'-]*\b", path.read_text(encoding="utf-8"))) for path in documents}
    oversized = {path: count for path, count in word_counts.items() if count > 6000}
    if oversized:
        raise ValueError({"oversized_documents": oversized})
    materialized = sum(1 for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)
    if materialized >= 2000:
        raise ValueError(f"materialized file ceiling exceeded: {materialized}")
    print(json.dumps({
        "phase": PHASE,
        "state": "COMBINED_CLOSEOUT_SEAL_CANDIDATE_READY_FOR_SCOPED_VALIDATION",
        "method_failures": ledger["counts"]["witness_results"]["fail"],
        "owner_manifest_entries": owner_entries,
        "delta_manifest_entries": delta_entries,
        "expected_staged_paths": staged_paths,
        "phase_files": sum(1 for path in PHASE_ROOT.rglob("*") if path.is_file()),
        "materialized_files": materialized,
        "maximum_document_words": max(word_counts.values()),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
