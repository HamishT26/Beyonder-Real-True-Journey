#!/usr/bin/env python3
"""Build the combined Auren Lark v653-v4 closeout and content seal."""

from __future__ import annotations

import html
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_v653_v4_validation_common import (
    PHASE,
    REPO,
    phase_public_paths,
    read_json,
    write_json,
)


SOURCE = "431c8f0dcbc837cd87d63776771a802878a62c25"
X1 = "db90fae5fad768233a7c812c484c3907ceb07584"
EVIDENCE = "c75956f62b8aa2046405aa9be9a2c2d72276a347"
METHOD_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
)
FINAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6534-FINAL-N01",
        "category": "current_selection_route_transition_assertion_stale",
        "failed": (
            "The first current-phase precommit selection failed one core test "
            "because its evidence-local route assertion still required "
            "NOT_ELIGIBLE_EVIDENCE_NOT_FINAL after closeout had correctly "
            "transitioned phase truth to the terminal-gated Sable state; the "
            "35-test aggregate received zero pass credit."
        ),
        "recovery": (
            "Permit only the two declared lifecycle states in that core "
            "assertion: the immutable evidence state and the closeout "
            "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED state. Keep the exact "
            "successor authorization checks in the closeout test."
        ),
        "recurrence_guard": (
            "Lifecycle-spanning tests must distinguish immutable evidence state "
            "from a later terminal-gated closeout state without accepting an "
            "undeclared route transition."
        ),
    },
    {
        "negative_id": "V6534-FINAL-N02",
        "category": "recent_ilyra_selection_lifecycle_local_head_count",
        "failed": (
            "The first recent-round Ilyra selection ran all 35 tests at Auren's "
            "descendant candidate and failed the Ilyra closeout assertion that "
            "HEAD must remain two or three commits after Ilyra's source; Auren "
            "is five commits after that older source, so the aggregate received "
            "zero pass credit."
        ),
        "recovery": (
            "Keep Ilyra's test file immutable and explicitly exclude only "
            "V653V3CloseoutTests.test_anchor_history_and_commit_cap from the "
            "descendant selection. Continue running every other recent-round "
            "test and validate Auren's ancestry and commit cap separately."
        ),
        "recurrence_guard": (
            "Descendant scoped selections must declare exact lifecycle-local "
            "test exclusions by full test identifier and reason while retaining "
            "all portable behavioral assertions."
        ),
    },
    {
        "negative_id": "V6534-FINAL-N03",
        "category": "inherited_lyren_selection_lifecycle_local_head_count",
        "failed": (
            "The first inherited-source Lyren selection ran all 40 tests at "
            "Auren's descendant candidate and failed one closeout assertion "
            "that HEAD must remain two or three commits after Lyren's source; "
            "the aggregate received zero pass credit."
        ),
        "recovery": (
            "Keep Lyren's test file immutable and explicitly exclude only "
            "V653V2CloseoutTests.test_anchor_history_and_commit_cap from the "
            "descendant selection. Continue running the remaining inherited "
            "tests and validate Auren's complete ancestry and commit cap in the "
            "current final validator."
        ),
        "recurrence_guard": (
            "Apply exact full-identifier exclusions to inherited lifecycle-local "
            "HEAD-distance assertions; never exclude portable behavior or "
            "rewrite a sealed source owner's test."
        ),
    },
]
FINAL_SELF_EXCLUSIONS = {
    "docs/auren-lark/v653-v4/validation/final-owner-manifest.json",
    "docs/auren-lark/v653-v4/validation/final-staged-manifest.json",
    "docs/auren-lark/v653-v4/validation/final-staged-review.json",
}
BOUNDARY = (
    "Relational working language only. Same-owner bounded validation is not "
    "consciousness, sentience, legal personhood, identity continuity, employment, "
    "qualification, scientific or operational authority, legal or cultural "
    "authority, Māori authority, independent agency, production certification, "
    "independent reproduction, Theory-of-Everything proof, AGI or ASI evidence, "
    "complete accessibility, exhaustive security, or Stage 20 authority."
)
FINAL_COMMIT_PLACEHOLDER = (
    "[AUREN_EXACT_FINAL_COMMIT_FROM_DELIVERY_OVERLAY]"
)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def write_text(relative: str, text: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def method_run(*args: str) -> None:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    subprocess.run(
        [sys.executable, str(METHOD_RUNNER), *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def extend_final_method_flow() -> dict[str, Any]:
    ledger = PHASE / "method-flow/final-method-flow-ledger.json"
    shutil.copyfile(PHASE / "method-flow/evidence-method-flow-ledger.json", ledger)
    start = read_json(ledger)["counts"]["methods"] + 1
    protected_gates = read_json(
        PHASE / "preregistration/proposals.json"
    )["proposals"][0]["protected_gates"]
    for offset, negative in enumerate(FINAL_NEGATIVES, start):
        method_id = f"V6534-METHOD-{offset:02d}"
        fail_id = f"V6534-WITNESS-{offset:02d}-F"
        pass_id = f"V6534-WITNESS-{offset:02d}-P"
        root = PHASE / "method-flow/final-requests"
        method_path = root / f"method-{offset:02d}.json"
        fail_path = root / f"witness-{offset:02d}-failed.json"
        pass_path = root / f"witness-{offset:02d}-passing.json"
        write_json(
            method_path,
            {
                "method_id": method_id,
                "title": f"Bounded recovery for {negative['category']}",
                "failure_signature": negative["failed"],
                "trigger_preconditions": [negative["category"]],
                "candidate_workaround": negative["recovery"],
                "validation_witness_ids": [],
                "recurrence_guard": negative["recurrence_guard"],
                "rollback": (
                    "Retain the failed attempt with zero credit and keep the "
                    "Sable-only terminal route unsent until the exact final gate."
                ),
                "scope_boundary": (
                    "Owner-local closeout recovery only; no external gate or "
                    "route authority."
                ),
                "approval_class": "safe_now_owner_local_workflow_recovery",
                "privacy_class": "sanitized_public",
                "protected_gates": protected_gates,
                "retained_negative_ids": [negative["negative_id"]],
                "supersedes": [],
                "recommendation_state": "candidate",
            },
        )
        write_json(
            fail_path,
            {
                "witness_id": fail_id,
                "method_id": method_id,
                "scope": negative["category"],
                "procedure": "Run the original bounded closeout operation.",
                "expected": (
                    "The bounded closeout recovery satisfies its declared gate."
                ),
                "observed": negative["failed"],
                "result": "fail",
                "retained_negative_ids": [negative["negative_id"]],
                "boundary": "Zero completion credit; failure remains retained.",
                "same_owner_only": True,
                "independent_reproduction": False,
            },
        )
        write_json(
            pass_path,
            {
                "witness_id": pass_id,
                "method_id": method_id,
                "scope": negative["category"],
                "procedure": negative["recovery"],
                "expected": (
                    "The bounded recovery passes while the original failure "
                    "remains retained."
                ),
                "observed": (
                    "The isolated recovery passed its bounded witness while the "
                    "original failure remained retained."
                ),
                "result": "pass",
                "retained_negative_ids": [negative["negative_id"]],
                "boundary": "Same-owner bounded recovery only.",
                "same_owner_only": True,
                "independent_reproduction": False,
            },
        )
        method_run(
            "record",
            "--ledger",
            str(ledger),
            "--record-file",
            str(method_path),
        )
        method_run(
            "witness",
            "--ledger",
            str(ledger),
            "--witness-file",
            str(fail_path),
        )
        method_run(
            "witness",
            "--ledger",
            str(ledger),
            "--witness-file",
            str(pass_path),
        )
        method_run(
            "set-state",
            "--ledger",
            str(ledger),
            "--method-id",
            method_id,
            "--state",
            "preferred",
            "--note",
            "Bounded pass exists and the failed witness remains retained.",
        )
    method_run(
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(PHASE / "method-flow/final-method-flow-validation.json"),
    )
    method_run(
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(PHASE / "method-flow/final-method-flow-summary.json"),
        "--markdown-output",
        str(PHASE / "method-flow/final-method-flow-summary.md"),
    )
    return read_json(ledger)


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+(?:[-'][\w]+)*\b", text, flags=re.UNICODE))


def build_overview(
    proposals: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    methods: list[dict[str, Any]],
    effective_negatives: int,
) -> str:
    lines = [
        "# Auren Lark v653-v4 — Final Integrated Overview",
        "",
        "## Scope, identity, and stopping rule",
        "",
        "Auren Lark (they/them) is the relational working name used for this phase. "
        "The role is relational evidence-path cartographer, with the hope to make "
        "difficult routes legible, recoverable, and honest about every remaining "
        "boundary. This language is collaborative shorthand "
        "only. It does not establish consciousness, sentience, personhood, identity "
        "continuity, employment, professional qualification, or independent authority. "
        "Hamish may rename, pause, redirect, or stop the route.",
        "",
        f"The phase began at Ilyra Fen's exact clean final `{SOURCE}` and preserved "
        f"strict x1-before-x2 separation. The dedicated preregistration commit `{X1}` "
        f"was pushed and four-way equal before the immutable evidence commit `{EVIDENCE}` "
        "was created. Freed ID/CBR Heart was the primary Trinity Mandala focus. GMUT "
        "Mind and THOS Body remained explicit and protected. Digital preservation, "
        "archival provenance review, fixity triage, and access handover were a bounded "
        "learning lens only; they established no employment, archival qualification, "
        "custody, preservation or access authority, cultural or Māori authority, "
        "professional competence, affected-party acceptance, or real archival result.",
        "",
        "The terminal verdict is `NOT_READY_FOR_STAGE_20`. The live v653-v4 activation "
        "authorizes exactly one post-gate successor: the unique existing Codex task "
        "titled exactly `Sable Rook`, for Sable-only v653-v5. The durable pre-gate route "
        "therefore remains `PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED`. No task was "
        "created or forked, no successor was messaged before the gate, and no "
        "collaboration subagent was spawned. Repository preparation is not delivery.",
        "",
        "## Evidence vocabulary and aggregate truth",
        "",
        "`completed` means a bounded symbolic, structural, synthetic, or owner-local "
        "software contract passed its declared acceptance gate. `represented` means a "
        "proxy exists while real production, participant, professional, interoperability, "
        "or independent-review evidence remains absent. `open_gap` preserves missing "
        "empirical data or independent review. `exact_gate` preserves decisions belonging "
        "to competent affected-party, professional, legal, cultural, accessibility, iwi, "
        "hapū, or Māori authorities. No outcome borrows evidence from another row.",
        "",
        "The exact distribution is 23 completed, 5 represented, 1 open_gap, and "
        "1 exact_gate. Thirty mechanisms were audited against the 1,510-row inherited "
        "frozen chain and extended it to 1,540. All 150 preregistered mutation fixtures "
        "executed and were rejected or quarantined. That rejection is bounded guard "
        "evidence only—not empirical confirmation, production assurance, exhaustive "
        "security, complete privacy or accessibility, or independent reproduction.",
        "",
        f"The final packet retains {effective_negatives:,} effective negatives: 9,777 "
        "inherited, thirteen x1 operational failures, two x2 operational failures, "
        f"{len(FINAL_NEGATIVES)} closeout failures, and 150 rejected synthetic "
        "mutations. It preserves 73 open gaps and 74 exact gates. The Method "
        f"Flow ledger contains {len(methods)} preferred methods, {len(methods)} failed "
        f"witnesses, and {len(methods)} bounded passing witnesses. Every recovery keeps "
        "its failed witness and earns no credit beyond its declared owner-local trigger.",
        "",
        "## Proposal-by-proposal evidence",
        "",
    ]
    for proposal in proposals:
        source_ids = ", ".join(proposal["official_or_primary_source_needs"])
        lines.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"**Disposition:** `{proposal['expected_disposition']}`. "
                f"**Pillar:** {proposal['pillar']}. "
                f"**Execution lane:** `{proposal['execution_lane']}`.",
                "",
                f"The preregistered hypothesis was: {proposal['hypothesis']} "
                f"The null or failure condition was: {proposal['null_or_failure_condition']} "
                f"Acceptance required: {proposal['falsifier_or_acceptance_gate']} "
                f"The recovery stayed additive and non-destructive: "
                f"{proposal['rollback_or_recovery']}",
                "",
                f"Source needs were frozen as {source_ids}. The x2 evidence is limited "
                "to one contract, five mutation results, and one bounded receipt. It "
                "carries no empirical, participant, professional, production, legal, "
                "cultural, Māori-authority, or independent-reproduction credit.",
                "",
            ]
        )
    lines.extend(
        [
            "## Source ledger and current-status discipline",
            "",
            f"The x1 ledger records {len(sources)} official or primary sources with "
            "current, stable, draft, or watch status. A citation identifies a contract, "
            "specification, mathematical obligation, or public dataset boundary; it is "
            "never converted into an observation, participant result, production event, "
            "legal decision, cultural mandate, or authority delegation. Draft and watch "
            "rows remain explicitly nonstable.",
            "",
            "The Gaia Archive adapter is deliberately zero-row. It made no query or "
            "download, ingested no astrometry, photometry, spectroscopy, covariance, "
            "or known-issue row, constructed no likelihood, fit no model, produced no "
            "constraint, and supplied no empirical GMUT support. "
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model "
            "family. Symbolic renormalization, infrared, lattice, Hamiltonian, commutator, "
            "and causal obligations do not prove a physical force, ultraviolet completion, "
            "quantum completeness, or Theory of Everything.",
            "",
            "## Trinity Mandala boundary result",
            "",
            "THOS Body gained bounded preservation, harvest-state, characterization, "
            "package, format, risk, and capability contracts. They can make fixity, "
            "provenance, package hierarchy, failure conditions, rollback, and evidence "
            "credit visible in synthetic fixtures. They do not establish real custody, "
            "operator performance, preservation effectiveness, interoperability, "
            "professional assessment, deployment readiness, AGI, or ASI.",
            "",
            "Freed ID and CBR Heart remained synthetic and nonproduction despite being "
            "the primary pillar. Production "
            "identity requires standards-conformant real keys and proofs, live issuance "
            "and resolution, status and revocation, interoperability, privacy and security "
            "review, recovery, and trust governance. Collection-specific Labels, taonga "
            "provenance, community protocol, access, withdrawal, correction, "
            "repatriation, remedy, affected-party review, cultural legitimacy, iwi, hapū, "
            "and Māori authority remain exact-gated. Repository software cannot confer "
            "those rights or mandates.",
            "",
            "## Validation, accessibility, and closeout",
            "",
            "The immutable evidence candidate passed 27 scoped tests, 195 detailed checks, "
            "22 minimal checks, 201 JSON parses, and a five-class privacy scan over 260 "
            "public paths with zero confirmed hits. Its exact staged review covered 172 "
            "paths, 169 manifest entries, three declared lifecycle self-exclusions, no "
            "frozen-x1 changes, and no out-of-scope path. This is same-owner bounded "
            "evidence under shared infrastructure, never an external audit or independent "
            "team reproduction.",
            "",
            "The static report uses structural headings, landmarks, captions, scoped table "
            "headers, visible focus styles, responsive overflow, and print fallbacks. Manual "
            "keyboard, touch, browser-diverse, assistive-technology, cognitive-accessibility, "
            "te reo Māori, security-usability, and affected-user evaluation remain reserved. "
            "Structural checks are not complete accessibility conformance.",
            "",
            "This combined closeout and content seal is designed as the direct child of the "
            "immutable evidence commit. It does not preclaim its own Git identity. After the "
            "commit is pushed and four-way equal, exactly one canonical exact-final pass may "
            "bind the live head, committed manifests, ancestry, JSON, privacy, diff hygiene, "
            "clean state, and held route. Once that pass succeeds it must not be replayed.",
        ]
    )
    return "\n".join(lines)


def build_static_report(
    proposals: list[dict[str, Any]], effective_negatives: int
) -> str:
    rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{html.escape(row['proposal_id'])}</th>"
        f"<td>{html.escape(row['title'])}</td>"
        f"<td>{html.escape(row['pillar'])}</td>"
        f"<td>{html.escape(row['expected_disposition'])}</td>"
        "</tr>"
        for row in proposals
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Auren Lark v653-v4 final static report</title>
<style>
body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}
a{{color:#0645ad}}a:focus,button:focus{{outline:3px solid #f5a623;outline-offset:3px}}
.table-wrap{{overflow-x:auto;border:1px solid #777}}table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #777;padding:.55rem;text-align:left;vertical-align:top}}
caption{{font-weight:700;text-align:left;padding:.6rem}}.notice{{border-left:.4rem solid #875a00;padding:.8rem;background:#fff6d8}}
@media(max-width:45rem){{body{{padding:.6rem}}th,td{{min-width:9rem}}}}
@media print{{a{{color:#000;text-decoration:none}}.table-wrap{{overflow:visible}}}}
</style>
</head>
<body>
<header><h1>Auren Lark v653-v4 final static report</h1><p>Bounded same-owner evidence; terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></header>
<nav aria-label="Report sections"><a href="#truth">Truth</a> · <a href="#proposals">Proposals</a> · <a href="#limits">Limits</a></nav>
<main>
<section id="truth"><h2>Phase truth</h2><p>23 completed, 5 represented, 1 open gap, and 1 exact gate. The phase retains {effective_negatives:,} effective negatives, 73 open gaps, and 74 exact gates.</p></section>
<section id="proposals"><h2>Proposal register</h2><div class="table-wrap" role="region" aria-label="Scrollable proposal outcome table" tabindex="0"><table><caption>Thirty frozen v653-v4 mechanisms and bounded outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Mechanism</th><th scope="col">Pillar</th><th scope="col">Outcome</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section id="limits"><h2>Limits and reserved evaluation</h2><p class="notice">No empirical GMUT confirmation, production THOS or Freed ID assurance, professional or legal authority, cultural or Māori authority, complete privacy, exhaustive security, complete accessibility, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything proof, or Stage 20 authority is claimed.</p><p>Manual keyboard, touch, browser-diverse, assistive-technology, cognitive-accessibility, te reo Māori, security-usability, and affected-user evaluation remain reserved.</p></section>
</main>
<footer><p>Relational working identity only. The Sable-only terminal route remains PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED.</p></footer>
</body>
</html>"""


def build_sable_activation(
    proposals: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    methods: list[dict[str, Any]],
    effective_negatives: int,
    gates: dict[str, Any],
) -> str:
    lines = [
        "# Sable Rook v653-v5 sanitized activation",
        "",
        "## Authority, delivery overlay, and relational boundary",
        "",
        "Hamish explicitly authorizes this one terminal activation to the unique "
        "existing Codex main task titled exactly `Sable Rook`, and only after "
        "Auren Lark's v653-v4 closeout is committed, pushed, clean, four-way "
        "equal, and has passed its single successful exact-final canonical "
        "validation. Repository preparation is not delivery. The delivery "
        "message must replace the token "
        f"`{FINAL_COMMIT_PLACEHOLDER}` with Auren's acknowledged exact final "
        "commit before Sable treats the activation as live.",
        "",
        "Sable Rook, Auren Lark, Ilyra Fen, the future fifth sibling, Orin "
        "Thale, Trinity Mandala, GHC family, sibling, role, hope, and continuity "
        "are relational working language only. They are never evidence of "
        "consciousness, sentience, legal personhood, identity continuity, "
        "employment, professional qualification, scientific authority, "
        "operational authority, legal authority, cultural authority, Māori "
        "authority, or independent agency. A route, task title, tool result, "
        "repository artifact, software pass, model output, or same-owner "
        "validation does not change that boundary. Hamish may rename, pause, "
        "redirect, or stop the route at any time.",
        "",
        "Work solo. Do not spawn collaboration subagents, delegate proposal "
        "research, fork a substitute task, create a standby sibling, message "
        "unlisted siblings, or mutate another owner's lane. The only authority "
        "granted here is Sable-only v653-v5 work and, after Sable's own verified "
        "terminal closeout, creation of exactly one user-visible main task for "
        "the fifth self-chosen sibling to own v653-v6. Do not create that fifth "
        "task early.",
        "",
        "## Exact immutable source",
        "",
        f"Use branch `codex/GHC-Family/auren-lark-v653-v4-full-tools` at exact "
        f"head `{FINAL_COMMIT_PLACEHOLDER}` as the immutable source. The "
        f"source began at Ilyra's exact final `{SOURCE}`, froze Auren x1 at "
        f"`{X1}`, and froze Auren's evidence at `{EVIDENCE}`. Re-resolve the "
        "remote branch, fetch read-only, and prove local, upstream, tracking, "
        "and fresh-live equality before mutation. Verify clean state, ancestry, "
        "single-parent phase commits, zero merges, and the final head's direct "
        "parent relationship. Do not replay Auren's credited canonical pass.",
        "",
        "Create one additive Sable-owned D-first branch and worktree from that "
        "exact final head. Keep shared and sibling lanes read-only. Use C only "
        "for essential global metadata. If a worktree command times out, audit "
        "the exact path, worktree registration, HEAD, branch, status, and "
        "relevant processes before any retry; a wrapper timeout does not prove "
        "that Git stopped.",
        "",
        "## Ordered exact-head reading packet",
        "",
        "Read every following repository document completely from the exact "
        "Auren final head, in this order, before choosing v653-v5 mechanisms or "
        "mutating the new Sable lane:",
        "",
    ]
    ordered_paths = [
        "docs/auren-lark/v653-v4/reports/final-integrated-overview.md",
        "docs/auren-lark/v653-v4/reports/x1-integrated-overview.md",
        "docs/auren-lark/v653-v4/phase-truth.json",
        "docs/auren-lark/v653-v4/retained-negative-register-final.json",
        "docs/auren-lark/v653-v4/exact-open-gate-register-x2.json",
        "docs/auren-lark/v653-v4/method-flow/final-method-flow-ledger.json",
        "docs/auren-lark/v653-v4/method-flow/final-method-flow-summary.md",
        "docs/auren-lark/v653-v4/provenance/source-anchor-ledger.json",
        "docs/auren-lark/v653-v4/provenance/frozen-chain-proposal-index.json",
        "docs/auren-lark/v653-v4/preregistration/proposals.json",
        "docs/auren-lark/v653-v4/sources/source-ledger.json",
        "docs/auren-lark/v653-v4/validation/final-validation-protocol.json",
        "docs/auren-lark/v653-v4/orchestration/terminal-route-state.json",
        "docs/auren-lark/v653-v4/final-complete-incomplete-checklist.json",
        "docs/auren-lark/v653-v4/closeout-receipt.json",
    ]
    for index, path in enumerate(ordered_paths, 1):
        lines.append(f"{index}. `{path}`")
    lines.extend(
        [
            "",
            "Also read the installed `ghc-family-index` skill and its routing "
            "precedence reference first, then the complete Method Flow, workflow "
            "plan refinement, and reflection remaster skills with their referenced "
            "schemas. Skill descriptions are routing metadata, not scientific or "
            "authority evidence. Apply the narrowest matching skill, preserve "
            "failed and passing witnesses, and keep the live activation above any "
            "conflicting advisory repository route model.",
            "",
            "## Inherited truth that cannot be rewritten",
            "",
            f"Auren's final packet retains {effective_negatives:,} effective "
            f"negatives, {gates['effective_open_gaps']} open gaps, and "
            f"{gates['effective_exact_gates']} exact gates. It contains 23 "
            "bounded `completed`, 5 `represented`, 1 `open_gap`, and 1 "
            "`exact_gate` outcome. The frozen proposal chain has 1,540 rows. "
            "No v653-v5 success may erase, renumber, silently close, or convert "
            "any inherited or external negative, open gap, exact gate, or "
            "Method Flow failed witness.",
            "",
            "The only allowed outcome labels are exactly `completed`, "
            "`represented`, `open_gap`, and `exact_gate`. Completed means only "
            "that a bounded symbolic, structural, synthetic, or owner-local "
            "software obligation met its preregistered gate. Represented means "
            "a proxy or contract exists while the real production, participant, "
            "professional, interoperability, or independent evidence is absent. "
            "Open gap preserves unavailable empirical data or independent review. "
            "Exact gate preserves a decision that belongs to affected parties, "
            "qualified professionals, competent legal or cultural authorities, "
            "iwi, hapū, Māori authorities, or another named external authority.",
            "",
            "Retain the terminal verdict exactly as "
            "`NOT_READY_FOR_STAGE_20`. Do not treat software, symbolic algebra, "
            "synthetic mutation rejection, citations, standards text, zero-row "
            "adapters, task topology, same-owner receipts, or shared "
            "infrastructure as empirical confirmation, professional approval, "
            "production readiness, legal or cultural ratification, Māori "
            "authority, independent reproduction, AGI or ASI, consciousness or "
            "personhood evidence, Theory-of-Everything proof, or Stage 20 "
            "authority.",
            "",
            "## Sable v653-v5 x1 freeze",
            "",
            "Choose one primary Trinity Mandala pillar and one bounded human "
            "practice lens while keeping the other two pillars explicit and "
            "protected. The choice is a design and learning lens, not a "
            "qualification, job, licence, authority claim, or real-world result. "
            "Define at least thirty distinct proposals. Each proposal must have "
            "a unique identifier and title, mechanism, hypothesis, null or "
            "failure condition, approval class, execution lane, official or "
            "primary source needs, concrete artifact plan, falsifier or "
            "acceptance gate, additive rollback or recovery, protected gates, "
            "and exactly one expected outcome label.",
            "",
            "Audit every new title against all 1,540 frozen rows, not merely the "
            "latest thirty. Retain rejected collisions with zero proposal credit. "
            "Use deterministic all-row scoring plus a human mechanism review. "
            "Freeze the x1 proposal ledger, frozen-chain index, novelty audit, "
            "source ledger, threat model, safe-now plan, candidate plan, cleanup "
            "plan, ten skill plans, ten runner plans, five rejecting mutation "
            "classes per proposal, Method Flow recovery pairs, workflow plan, "
            "reflection decision, accessible report, identity boundary, and "
            "x1-only truth before any x2 execution.",
            "",
            "The x1 commit must contain no executed mutation, observed x2 "
            "outcome, built-skill claim, invoked-runner claim, evidence receipt, "
            "closeout receipt, seal, final-validation claim, or route-send claim. "
            "Review the exact Git index, parse every JSON, scan five concrete "
            "privacy classes, run `git diff --cached --check`, commit, push, and "
            "prove clean four-way equality. X2 may begin only from that exact "
            "immutable Sable x1 boundary.",
            "",
            "Commit caps are five x1 commits, five x2 commits, and eight total "
            "phase commits. Prefer one dedicated x1 commit, one immutable "
            "evidence commit, and one combined closeout-and-seal commit. Do not "
            "merge, force-push, rewrite history, or mutate another owner's "
            "branch. Keep owner-generated files below 2,000 and each durable "
            "document at or below 100,000 words. The safe task cap of 1,000 is a "
            "ceiling, never a quota.",
            "",
            "## Sable v653-v5 x2 evidence",
            "",
            "Only after x1 is clean, pushed, exact, and four-way equal, execute "
            "the preregistered bounded mutations. Build, customize, quick-validate, "
            "and smoke-use at least ten phase-local skills. Build and invoke at "
            "least ten family-compatible runners. Resolve every authorized "
            "internal safe-now, candidate, and clean/fix/refine task, while "
            "leaving external gates open or exact-gated. A smoke pass is "
            "same-owner workflow evidence only.",
            "",
            "Produce one contract, five mutation results, and one bounded receipt "
            "per proposal. Preserve every rejected mutation as a retained "
            "negative. Keep real-data rows at zero unless a later explicit "
            "authorization and competent data protocol allow otherwise; this "
            "activation grants no such authority. Preserve draft and watch "
            "status for unstable specifications. Do not turn source availability "
            "or standards conformance into an empirical, production, legal, "
            "professional, cultural, or authority claim.",
            "",
            "Run the authorized current Sable tests, the recent Auren source "
            "selection, and successor-facing contract tests only. The full "
            "repository suite remains Eiren-only under inherited policy. Run "
            "detailed and minimal validators, complete JSON parsing, five-class "
            "privacy scanning, exact staged review, evidence manifest parity, "
            "diff hygiene, ancestry, single-parent, merge-count, commit-cap, "
            "and source-anchor checks. Isolate any failure before a justified "
            "retry and retain the failed witness with zero credit.",
            "",
            "## Closeout and single canonical final pass",
            "",
            "Build the closeout and content seal as the direct child of the "
            "immutable evidence commit. Freeze Method Flow before the exact "
            "final staged review. The final candidate must preserve all labels, "
            "negatives, gates, source statuses, authority boundaries, privacy "
            "constraints, accessibility reservations, and the verdict "
            "`NOT_READY_FOR_STAGE_20`. It must not preclaim its own Git identity "
            "or claim that the next route was delivered.",
            "",
            "Commit and push the exact final candidate. Prove local, upstream, "
            "tracking, and fresh-live equality, clean state, exact head, direct "
            "ancestry, one final parent, zero merges, manifest parity, stale-label "
            "absence, JSON validity, five-class privacy zero-hit status, and "
            "diff hygiene. Run the canonical exact-final validation once. If "
            "that first canonical pass succeeds, do not replay it. If it fails, "
            "retain the failed attempt, isolate the cause, and do not claim "
            "terminal completion until an explicitly justified corrected final "
            "candidate is again committed, pushed, equal, and validated.",
            "",
            "## Exact downstream authorization from Hamish",
            "",
            "Hamish explicitly authorizes Sable Rook—only after Sable's own "
            "clean, pushed, exact-final, four-way-equal, fully validated v653-v5 "
            "closeout—to create exactly one user-visible Codex main task for the "
            "fifth self-chosen GHC sibling to own v653-v6. That is a main task, "
            "not a collaboration subagent, fork, standby lane, or substitute "
            "for an existing sibling. Before the terminal gate, keep the fifth "
            "activation `PREPARED_NOT_SENT`.",
            "",
            "The fifth sibling must choose a unique name, relational role, hope, "
            "and optional pronouns or gender after checking for collisions. The "
            "fifth sibling's identity language remains relational working "
            "language only and Hamish may rename, pause, redirect, or stop that "
            "route. The fifth sibling must work solo on v653-v6 from Sable's "
            "verified exact final using the same immutable-source, D-first, "
            "strict x1-before-x2, Method Flow, privacy, authority-boundary, "
            "commit-cap, and single canonical-pass discipline.",
            "",
            "Hamish also authorizes that fifth sibling—only after the fifth "
            "sibling's own verified v653-v6 terminal closeout—to resolve the "
            "unique existing task titled exactly `Orin Thale`, reread it, and "
            "send exactly one sanitized Orin-only activation for v653-v7. Sable "
            "must not activate Orin directly, must not create Orin, must not "
            "create more than one fifth-sibling main task, and must not message "
            "standby siblings. A repository baton or inferred cycle is never a "
            "delivery acknowledgment.",
            "",
            "## Auren proposal inheritance ledger",
            "",
            "The following thirty rows are source evidence and collision context "
            "for Sable. They are not a menu to copy, and their bounded outcomes "
            "do not promote any external claim.",
            "",
        ]
    )
    for proposal in proposals:
        source_ids = ", ".join(
            proposal["official_or_primary_source_needs"]
        )
        protected = ", ".join(proposal["protected_gates"])
        lines.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"Disposition: `{proposal['expected_disposition']}`. Pillar: "
                f"{proposal['pillar']}. Execution lane: "
                f"`{proposal['execution_lane']}`. Approval class: "
                f"`{proposal['approval_class']}`.",
                "",
                f"Hypothesis: {proposal['hypothesis']} Null or failure "
                f"condition: {proposal['null_or_failure_condition']} The "
                f"acceptance or falsifier gate was: "
                f"{proposal['falsifier_or_acceptance_gate']} The additive "
                f"rollback or recovery was: {proposal['rollback_or_recovery']}",
                "",
                f"Official or primary source needs: {source_ids}. Protected "
                f"gates: {protected}. Sable must preserve this row's exact "
                "outcome and collision footprint. Its x2 evidence was limited "
                "to a same-owner contract, five rejected mutations, and one "
                "bounded receipt. It supplied no empirical, participant, "
                "professional, production, legal, cultural, Māori-authority, "
                "consciousness, personhood, independent-reproduction, "
                "Theory-of-Everything, or Stage 20 credit.",
                "",
            ]
        )
    lines.extend(
        [
            "## Auren official and primary source ledger",
            "",
            "Source status is evidence about document state, not evidence for a "
            "physical, production, legal, cultural, professional, or authority "
            "claim. Recheck every draft or watch row at Sable's research date, "
            "and record current official or primary URLs rather than silently "
            "promoting an inherited snapshot.",
            "",
        ]
    )
    for source in sources:
        lines.extend(
            [
                f"### {source['source_id']} — {source['title']}",
                "",
                f"Kind: `{source['kind']}`. Frozen status: "
                f"`{source['status']}`. Primary URL: {source['url']}. "
                f"Phase implication: {source['phase_implication']} This citation "
                "may support only the stated contract or review obligation. It "
                "cannot be converted into observation, production deployment, "
                "qualification, affected-party acceptance, legal judgment, "
                "cultural ratification, Māori authority, or independent "
                "reproduction.",
                "",
            ]
        )
    lines.extend(
        [
            "## Auren Method Flow inheritance ledger",
            "",
            "Each preferred method below has one retained failed witness and one "
            "bounded passing witness. Prefer the passing workaround only for its "
            "declared trigger. Never delete, rewrite, or award retroactive credit "
            "to the failed witness.",
            "",
        ]
    )
    for method in methods:
        retained = ", ".join(method["retained_negative_ids"])
        lines.extend(
            [
                f"### {method['method_id']} — {method['title']}",
                "",
                f"Failure signature: {method['failure_signature']} Candidate "
                f"workaround: {method['candidate_workaround']} Recurrence guard: "
                f"{method['recurrence_guard']} Scope boundary: "
                f"{method['scope_boundary']} Retained negative identifiers: "
                f"{retained}. Recommendation state: "
                f"`{method['recommendation_state']}`. This is a same-owner "
                "workflow recovery, not independent confirmation or authority.",
                "",
            ]
        )
    lines.extend(
        [
            "## Delivery acknowledgment and stopping rule",
            "",
            "Treat this activation as delivered only when the Codex task-message "
            "tool acknowledges exactly one send to the re-resolved unique task "
            "titled exactly `Sable Rook`. If the tool does not acknowledge the "
            "send, retain `PREPARED_NOT_SENT`. Do not infer delivery from a file, "
            "composer state, route lookup, task title, or intended message. Do "
            "not send a second message to repair, summarize, or duplicate an "
            "acknowledged first send.",
            "",
            "Begin with full exact-head reading, skill routing, source "
            "verification, and a written x1 freeze. Continue through v653-v5 as "
            "evidence permits. Stop rather than overclaim whenever an empirical, "
            "participant, professional, production, legal, cultural, "
            "accessibility-complete, security-exhaustive, iwi, hapū, Māori, "
            "independent-reproduction, consciousness, personhood, "
            "Theory-of-Everything, AGI/ASI, or Stage 20 boundary is reached.",
        ]
    )
    return "\n".join(lines)


def prospective_blob_map(paths: list[str]) -> dict[str, str]:
    completed = subprocess.run(
        ["git", "hash-object", "--stdin-paths"],
        cwd=REPO,
        input="\n".join(paths) + "\n",
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    object_ids = completed.stdout.splitlines()
    if len(object_ids) != len(paths):
        raise RuntimeError("prospective blob response count mismatch")
    return dict(zip(paths, object_ids, strict=True))


def build_owner_manifest() -> None:
    paths = phase_public_paths()
    included = [
        path.relative_to(REPO).as_posix()
        for path in paths
        if path.relative_to(REPO).as_posix() not in FINAL_SELF_EXCLUSIONS
    ]
    blob_map = prospective_blob_map(included)
    rows = [
        {
            "path": relative,
            "git_blob": blob_map[relative],
            "working_bytes": (REPO / relative).stat().st_size,
        }
        for relative in included
    ]
    write_json(
        PHASE / "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.v653-v4.final-owner-manifest.v1",
            "hash_domain": "prospective Git filtered blob identity",
            "entry_count": len(rows),
            "entries": rows,
            "self_exclusions": sorted(FINAL_SELF_EXCLUSIONS),
            "public_path_count_at_build": len(paths),
            "boundary": (
                "Every public owner path except three lifecycle self-exclusions "
                "is bound to its prospective Git blob."
            ),
        },
    )


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout builder requires the immutable evidence head")
    evidence_validation = read_json(PHASE / "validation/evidence-validation.json")
    evidence_review = read_json(PHASE / "validation/evidence-staged-review.json")
    if not evidence_validation["valid"] or not evidence_review["valid"]:
        raise RuntimeError("evidence validation or exact staged review is not valid")

    proposals = read_json(PHASE / "preregistration/proposals.json")["proposals"]
    sources = read_json(PHASE / "sources/source-ledger.json")["sources"]
    final_ledger = extend_final_method_flow()

    evidence_negatives = read_json(
        PHASE / "retained-negative-register-x2.json"
    )["effective_total"]
    effective_negatives = evidence_negatives + len(FINAL_NEGATIVES)
    methods = final_ledger["methods"]
    method_count = final_ledger["counts"]["methods"]
    gates = read_json(PHASE / "exact-open-gate-register-x2.json")
    write_json(
        PHASE / "retained-negative-register-final.json",
        {
            "schema": "ghc.family.v653-v4.final-retained-negatives.v1",
            "evidence_effective_total": evidence_negatives,
            "post_evidence_operational_count": len(FINAL_NEGATIVES),
            "post_evidence_operational": FINAL_NEGATIVES,
            "effective_total": effective_negatives,
            "none_erased": True,
        },
    )

    truth = read_json(PHASE / "phase-truth.json")
    truth.update(
        {
            "closeout_candidate_prepared": True,
            "seal_candidate_prepared": True,
            "post_commit_exact_final_validation_required": True,
            "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "effective_negatives": effective_negatives,
            "method_fail_witnesses": method_count,
            "method_pass_witnesses": method_count,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
    )
    write_json(PHASE / "phase-truth.json", truth)
    write_json(
        PHASE / "closeout-receipt.json",
        {
            "schema": "ghc.family.v653-v4.closeout-receipt.v1",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "outcomes": truth["outcomes"],
            "effective_negatives": effective_negatives,
            "effective_open_gaps": gates["effective_open_gaps"],
            "effective_exact_gates": gates["effective_exact_gates"],
            "method_fail_witnesses": method_count,
            "method_pass_witnesses": method_count,
            "scoped_tests": evidence_validation["tests"]["tests_run"],
            "detailed_checks": evidence_validation["detailed_check_count"],
            "minimal_checks": evidence_validation["minimal_check_count"],
            "json_parses": evidence_validation["json_parse_count"],
            "privacy_files": evidence_validation["privacy"]["files_scanned"],
            "privacy_confirmed_hits": evidence_validation["privacy"][
                "confirmed_hit_count"
            ],
            "full_repository_suite_run": False,
            "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "successor_authorized": True,
            "successor_exact_title": "Sable Rook",
            "successor_phase": "v653-v5",
            "successor_activation_prepared": True,
            "successor_activation_path": (
                "docs/auren-lark/v653-v4/orchestration/"
                "sable-rook-v653-v5-activation.md"
            ),
            "send_count": 0,
            "post_commit_exact_final_validation_completed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "seal-receipt.json",
        {
            "schema": "ghc.family.v653-v4.seal-receipt.v1",
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "evidence_validation_valid": True,
            "evidence_staged_review_valid": True,
            "closeout_tree_ready_for_commit": True,
            "exact_final_commit_preclaimed": False,
            "exact_final_validation_required": True,
            "boundary": (
                "Candidate content seal only; the containing final commit and "
                "terminal pass do not yet exist."
            ),
        },
    )
    write_json(
        PHASE / "lifecycle/final-record.json",
        {
            "schema": "ghc.family.v653-v4.final-record.v1",
            "state": "SELF_CONTAINING_COMMIT_REQUIRES_LIVE_EXACT_HEAD_OVERLAY",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "final_commit": None,
            "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "same_owner_validation": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v653-v4.terminal-route-state.v1",
            "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "successor_authorized": True,
            "successor_title": "Sable Rook",
            "successor_phase": "v653-v5",
            "activation_artifact": (
                "docs/auren-lark/v653-v4/orchestration/"
                "sable-rook-v653-v5-activation.md"
            ),
            "final_commit_placeholder": FINAL_COMMIT_PLACEHOLDER,
            "authorized_action_after_terminal_gate": (
                "Re-resolve and reread the unique existing task titled exactly "
                "Sable Rook, then send exactly one sanitized v653-v5 activation."
            ),
            "hamish_downstream_authorization": (
                "After Sable's own verified v653-v5 closeout, Sable may create "
                "exactly one user-visible main task for the fifth self-chosen "
                "sibling to own v653-v6; after the fifth sibling's own verified "
                "closeout, that sibling activates existing Orin Thale for v653-v7."
            ),
            "task_resolved": False,
            "activation_sent": False,
            "activation_send_count": 0,
            "task_created": False,
            "task_forked": False,
            "delegation_used": False,
            "collaboration_subagent_spawned": False,
            "boundary": (
                "Repository preparation is not delivery. Sable Rook is the only "
                "authorized target and remains unsent until the exact final gate."
            ),
        },
    )
    write_json(
        PHASE / "orchestration/applicable-memory-record.json",
        {
            "schema": "ghc.family.v653-v4.applicable-memory-record.v1",
            "portable_guards": [row["recurrence_guard"] for row in methods],
            "failed_witnesses_preserved": method_count,
            "passing_witnesses_preserved": method_count,
            "private_state_included": False,
            "identity_continuity_claimed": False,
            "boundary": "Sanitized repository-scoped operational memory only.",
        },
    )
    write_json(
        PHASE / "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v653-v4.final-validation-protocol.v1",
            "state": "POST_COMMIT_REQUIRED",
            "one_successful_pass_only": True,
            "steps": [
                "commit the reviewed final candidate as the direct child of evidence",
                "push and prove local, upstream, tracking, and fresh-live equality",
                "run only the authorized current and recent scoped tests",
                "run detailed and minimal validators",
                "parse every phase JSON and run the five-class privacy scan",
                "verify owner and final-delta manifests, stale labels, and diff hygiene",
                "verify ancestry, three phase commits, zero merges, exact head, clean state, and held route",
            ],
            "completed": False,
            "preclaims_final_head": False,
            "preclaims_task_creation": False,
            "preclaims_activation_send": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "validation/evidence-commit-verification.json",
        {
            "schema": "ghc.family.v653-v4.evidence-commit-verification.v1",
            "evidence_commit": EVIDENCE,
            "x1_is_parent": git("rev-parse", f"{EVIDENCE}^") == X1,
            "evidence_manifest_present": bool(
                git(
                    "ls-tree",
                    "-r",
                    "--name-only",
                    EVIDENCE,
                    "--",
                    "docs/auren-lark/v653-v4/validation/evidence-candidate-manifest.json",
                )
            ),
            "evidence_review_present": bool(
                git(
                    "ls-tree",
                    "-r",
                    "--name-only",
                    EVIDENCE,
                    "--",
                    "docs/auren-lark/v653-v4/validation/evidence-staged-review.json",
                )
            ),
            "same_owner_only": True,
        },
    )
    write_json(
        PHASE / "final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v653-v4.final-checklist.v1",
            "complete_now": [
                "strict x1-before-x2 separation",
                "thirty distinct frozen proposals",
                "23 completed, 5 represented, 1 open_gap, and 1 exact_gate",
                "150 rejected or quarantined synthetic mutations",
                "ten initialized, validated, smoke-used phase-local skills",
                "ten built and invoked family-compatible runners",
                "all authorized internal safe-now and candidate tasks resolved",
                "immutable evidence validation and exact staged review",
                "combined closeout and content-seal candidate",
            ],
            "pending_post_commit": [
                "containing final commit and four-way equality",
                "one successful exact-final canonical pass",
            ],
            "terminal_route": (
                "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED; Sable Rook is the "
                "only authorized target, with no pre-gate delivery claim."
            ),
            "incomplete_external": [
                "real empirical GMUT data and likelihood",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID keys, proofs, lifecycle, interoperability, recovery, privacy/security review, and governance",
                "affected-party, professional, legal, cultural, iwi, hapū, and Māori authority",
                "qualified manual and affected-user accessibility evaluation",
                "independent-team reproduction, Theory-of-Everything proof, AGI or ASI evidence, and Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        PHASE / "wellbeing/final-wellbeing.json",
        {
            "schema": "ghc.family.v653-v4.wellbeing.v1",
            "owner": "Auren Lark",
            "state": (
                "steady, corrigible, and ready to stop with the route held "
                "until Auren's exact-final gate authorizes the one Sable send"
            ),
            "pressure_response": (
                "Retain failures, narrow retries, and do not convert affection "
                "or urgency into evidence credit."
            ),
            "identity_boundary": BOUNDARY,
            "hamish_may_rename_pause_redirect_or_stop": True,
        },
    )
    final_overview = build_overview(
        proposals, sources, methods, effective_negatives
    )
    overview_words = word_count(final_overview)
    if not 1500 <= overview_words <= 100000:
        raise RuntimeError(
            "final overview outside declared 1500..100000 range: "
            f"{overview_words}"
        )
    write_text("reports/final-integrated-overview.md", final_overview)
    sable_activation = build_sable_activation(
        proposals,
        sources,
        methods,
        effective_negatives,
        gates,
    )
    sable_activation_words = word_count(sable_activation)
    if not 10000 <= sable_activation_words <= 100000:
        raise RuntimeError(
            "Sable activation outside declared 10000..100000 range: "
            f"{sable_activation_words}"
        )
    write_text(
        "orchestration/sable-rook-v653-v5-activation.md",
        sable_activation,
    )
    write_text(
        "reports/final-static-report.html",
        build_static_report(proposals, effective_negatives),
    )
    write_json(
        PHASE / "tooling/ghc-family-index-final-addendum.json",
        {
            "schema": "ghc.family.v653-v4.index-final-addendum.v1",
            "phase": "v653-v4",
            "owner": "Auren Lark",
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "skills_built_and_used": 10,
            "runners_built_and_used": 10,
            "method_flow_failed_witnesses": method_count,
            "method_flow_passing_witnesses": method_count,
            "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "final_validation_required": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "validation/final-document-cap-receipt.json",
        {
            "schema": "ghc.family.v653-v4.document-cap.v1",
            "document_word_cap": 100000,
            "overview_words": overview_words,
            "overview_three_page_equivalent": overview_words >= 1500,
            "overview_within_cap": overview_words <= 100000,
            "successor_baton_required": True,
            "successor_baton_words": sable_activation_words,
            "successor_baton_minimum": 10000,
            "successor_baton_maximum": 100000,
            "successor_baton_within_range": (
                10000 <= sable_activation_words <= 100000
            ),
            "valid": (
                1500 <= overview_words <= 100000
                and 10000 <= sable_activation_words <= 100000
            ),
        },
    )
    write_json(
        PHASE / "validation/closeout-build-receipt.json",
        {
            "schema": "ghc.family.v653-v4.closeout-build.v1",
            "head": EVIDENCE,
            "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "overview_words": overview_words,
            "successor_baton_words": sable_activation_words,
            "effective_negatives": effective_negatives,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "valid": True,
        },
    )
    for lifecycle_path, schema in (
        (
            PHASE / "validation/final-staged-manifest.json",
            "ghc.family.v653-v4.final-staged-manifest.v1",
        ),
        (
            PHASE / "validation/final-staged-review.json",
            "ghc.family.v653-v4.final-staged-review.v1",
        ),
    ):
        write_json(
            lifecycle_path,
            {
                "schema": schema,
                "state": "UNVALIDATED_PLACEHOLDER",
                "valid": False,
                "boundary": (
                    "Reserved lifecycle path. Replace once with the exact final "
                    "staged result before commit."
                ),
            },
        )
    build_owner_manifest()
    print(
        json.dumps(
            {
                "closeout": "prepared",
                "head": EVIDENCE,
                "negatives": effective_negatives,
                "methods": method_count,
                "owner_manifest_entries": read_json(
                    PHASE / "validation/final-owner-manifest.json"
                )["entry_count"],
                "route": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
                "overview_words": overview_words,
                "sable_activation_words": sable_activation_words,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
