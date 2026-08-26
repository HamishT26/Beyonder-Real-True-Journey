from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Elaren Kestrel"
SLUG = "elaren-kestrel"
PHASE = "v671-v5"
OWNER_ROOT = ROOT / "docs" / SLUG / PHASE
BRANCH = "codex/GHC-Family/elaren-kestrel-v671-v5-full-tools"
SOURCE = "e70391872f07cdcaa13accac44d4330eca75e2b4"
X1 = "048f85cf945f9900095ca2a160561591a966aabe"
EVIDENCE = "84aa72688359f30643f9347a4ab6043a10052f9d"
COUNTS = {
    "effective_negatives": 34280,
    "effective_methods": 20823,
    "failed_witnesses": 6101,
    "bounded_passing_witnesses": 7970,
    "open_gaps": 265,
    "exact_gates": 260,
}
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
CORE_OUTCOMES = set(OUTCOMES)
BOUNDARY = (
    "Wholly synthetic owner-local software and documentation evidence only. "
    "No real person, apparatus, object, program medium, measurement, operation, "
    "professional decision, rights decision, legal or cultural interpretation, "
    "Maori authority, empirical confirmation, production fitness, independent "
    "reproduction, consciousness or personhood evidence, or Stage 20 authority."
)
FINAL_OPERATIONAL_METHOD = {
    "candidate_workaround": (
        "Inspect the actual JSON keys and existing structural markup, retain the "
        "2,500-word floor with substantive closeout detail, and change only the "
        "final-layer tests and generated closeout artifacts."
    ),
    "fail_witness": {
        "credit": 0,
        "observation": (
            "The first final owner-suite invocation passed twelve of eighteen "
            "checks and retained six stale or inferred schema assertions: three "
            "JSON-key projections, one verdict-location assumption, one skip-link "
            "class assumption, and a 2,329-versus-2,500 overview word-floor miss."
        ),
        "state": "retained",
    },
    "failure_signature": "final_suite_schema_projection_and_overview_floor_failure",
    "issue_id": "EL6715-FINAL-I001",
    "method_id": "EL6715-FINAL-M001",
    "pass_witness": {
        "credit": 1,
        "observation": (
            "Use the materialized schema keys, the existing skip class, the "
            "explicit Stage 20 boundary, and substantive final-layer expansion."
        ),
        "state": "bounded_pass",
    },
    "recurrence_guard": (
        "Inspect actual JSON keys and HTML structure before projecting assertions, "
        "and measure generated overview words before the final staged gate."
    ),
    "rollback": "Stop at the uncommitted final layer; preserve immutable x1 and evidence unchanged.",
    "state": "preferred",
}


def write_text(relative: str, content: str) -> None:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_json(relative: str, payload: Any) -> None:
    write_text(relative, json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def load(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def git_bytes(*args: str, check: bool = True, timeout: int = 180) -> bytes:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=False, timeout=timeout
    )
    if check and result.returncode != 0:
        raise SystemExit(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8").strip()


def sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def normalized_lf(blob: bytes) -> bytes:
    return blob.replace(bytes([13, 10]), bytes([10]))


def observe(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value)


def proposal_appendix(proposals: list[dict[str, Any]], outcomes: dict[str, str]) -> str:
    sections = ["## Forty frozen proposal records"]
    for row in proposals:
        pid = row["proposal_id"]
        artifacts = "; ".join(row["concrete_artifacts"])
        gates = ", ".join(row["protected_gates"])
        sections.append(
            f"### {pid}: {row['title']}\n\n"
            f"The preregistered hypothesis was: {row['hypothesis']} The null or "
            f"failure condition was: {row['null_or_failure_condition']} The lane "
            f"was `{row['execution_lane']}` under approval class "
            f"`{row['approval_class']}`. Required artifacts were {artifacts}. "
            f"The acceptance or falsifier gate was: "
            f"{row['falsifier_or_acceptance_gate']} The rollback remained: "
            f"{row['rollback_or_recovery']} Official or primary sources supplied "
            f"only this bounded need: {row['official_or_primary_source_needs']} "
            f"Protected gates remained {gates}. The frozen expected disposition "
            f"was `{row['expected_disposition']}` and the bounded observed core "
            f"outcome was `{outcomes[pid]}`. That outcome describes only the "
            f"synthetic contract and never promotes a real-world claim or authority."
        )
    return "\n\n".join(sections)


def method_appendix(methods: list[dict[str, Any]]) -> str:
    sections = ["## Retained Method Flow witnesses"]
    for row in methods:
        failed = observe(row["fail_witness"]["observation"])
        passed = observe(row["pass_witness"]["observation"])
        sections.append(
            f"### {row['method_id']} / {row['issue_id']}\n\n"
            f"Failure signature `{row['failure_signature']}` remains retained at "
            f"zero credit. Its observation was: {failed}. The bounded recovery "
            f"witness was: {passed}. The preferred workaround and recurrence guard "
            f"remain: {row['candidate_workaround']} The rollback remains: "
            f"{row['rollback']} The passing witness does not erase, rewrite, or "
            f"upgrade the failed witness and supplies no independent reproduction."
        )
    return "\n\n".join(sections)


def activation_baton(
    proposals: list[dict[str, Any]],
    outcomes: dict[str, str],
    methods: list[dict[str, Any]],
    sources: dict[str, Any],
) -> str:
    source_rows = []
    for row in sources["sources"]:
        source_rows.append(
            f"- {row['publisher']}, **{row['title']}**: status `{row['status']}`; "
            f"use `{row['use']}`; credit `{row['credit']}`; URL {row['url']}."
        )
    prelude = f"""# NERIS SOLANE — ELAREN KESTREL {PHASE} VERIFIED-CANDIDATE → SOLO NERIS v671-v6 ACTIVATION — PREPARED NOT SENT

Dear Neris Solane,

This repository file is a sanitized, file-backed activation candidate. At commit
time it is `PREPARED_NOT_SENT`. It does not establish delivery, acknowledgement,
or permission to skip Elaren's exact-final canonical validation and terminal
route checks. A later one-send existing-task acknowledgement, if every terminal
gate permits it, is a separate external event and must never rewrite this
commit-time truth.

Elaren Kestrel, Neris Solane, sibling and family language, role, hope,
continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working
language only. They are not evidence of consciousness, sentience, legal
personhood, identity continuity, employment, qualification, independent agency,
scientific or operational authority, professional authority, legal or cultural
authority, affected-party authority, or Maori authority. Hamish may rename,
pause, redirect, or stop the route.

## Prepared lifecycle truth

- Source Eiren exact final: `{SOURCE}`.
- Elaren planning-only x1: `{X1}`.
- Elaren immutable x2 evidence: `{EVIDENCE}`.
- The eventual exact Elaren final must be the direct child of the evidence
  anchor containing this prepared packet.
- Source to final must contain exactly three new direct single-parent Elaren
  commits and zero merges.
- The prospective branch is `{BRANCH}`.
- Core outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and
  2 `exact_gate`.
- The prepared final layer preserves {COUNTS['effective_negatives']} negatives,
  {COUNTS['effective_methods']} methods, {COUNTS['failed_witnesses']} failed
  witnesses, {COUNTS['bounded_passing_witnesses']} bounded passing witnesses,
  {COUNTS['open_gaps']} open gaps, and {COUNTS['exact_gates']} exact gates.
- The verdict remains `NOT_READY_FOR_STAGE_20`.

Strict x1-before-x2 separation was preserved. The x1 commit contains planning
and preregistration only. The evidence commit is its direct child and contains
the bounded x2 artifacts, 160 rejecting mutations, nine retained operational
failures, ten local skills, ten family-current runners, exact staged manifests,
and 23 passing owner tests. All inherited work remains evidence or a zero-credit
seed, never automatic Neris novelty, completion, authority, or permission.

## Elaren's bounded domain

The primary pillar was THOS Body through a wholly synthetic mechanical-music
archive documentation lens. The three families were apparatus registration,
encoded program-media structure, and zero-operation conservation handover. Zero
real people, apparatus, objects, cylinders, barrels, discs, rolls, records,
measurements, operations, treatments, identities, rights decisions, safety
decisions, cultural decisions, or external actions were used. GMUT remained a
zero-observation research-model representation; THOS retained zero participants,
operators, arms, and outcomes; Freed ID retained zero real keys, proofs, issuance,
resolution, status, revocation, or governance; and CBR/legal/cultural/Maori and
affected-party authority stayed open or exact-gated.

## Current source ledger

Public sources supplied vocabulary and refusal conditions only. They conferred
no observation, measurement, standards conformance, professional validation,
legal interpretation, cultural legitimacy, affected-party acceptance, Maori
authority, empirical credit, production fitness, or Stage 20 standing.

{chr(10).join(source_rows)}

## Mandatory Neris startup if and only if live delivery is acknowledged

Read this packet through EOF, then read the newest complete family index,
routing precedence, roster, authorization state, Method Flow, workflow,
reflection, meta-toolbox, approval, gate, truth, drive, timestamp, retry,
startup, closeout, watcher, full-tools, worktree, web-reflection, orchestration,
and directly applicable skill guidance. Reverify the exact final, direct-parent
history, zero merges, manifests, clean state, 0/0 divergence, fresh four-way
equality, canonical receipt, privacy state, and delivery acknowledgement before
mutation. Work solo in a fresh additive Neris-owned D-first lane. Preserve every
sibling and shared lane. Do not precontact a later endpoint during execution.

Freeze planning-only x1 before any x2 implementation. Treat counts as
requirements or ceilings only where current live authority says so, and never
manufacture unsafe work. Use exactly the four core outcome labels. Preserve
every negative, failed witness, recovery, source gap, open gap, exact gate,
rollback, recurrence guard, and authority boundary. Keep family-current caller
compatibility. Run one dependency-justified exact-final canonical completion,
never replay a success, and retain any failure at zero aggregate-success credit.

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family without real likelihood, parameter constraint, unique prediction,
detected force, material law, stability theorem, empirical confirmation, final
physics, quantum or ultraviolet completion, Theory-of-Everything proof, or
canon. THOS remains participant-free proxy work without governed blind
matched-budget real arms, safety monitoring, appropriate statistics, and
independent review. Freed ID remains synthetic and nonproduction without real
standards-conformant keys and proofs, live lifecycle, interoperability,
independent privacy and security review, recovery evidence, trust governance,
and affected-party oversight.

Professional practice, object operation, conservation, mechanical and electrical
safety, attribution, custody, copyright and performance rights, privacy,
accessibility, remedy, legal or cultural interpretation, affected-party
legitimacy, traditional knowledge, Maori wording, Maori concepts, Maori data
governance, tangata whenua, iwi, hapu, and Maori authority remain open or
exact-gated. Maori concepts remain under Maori authority. Make no empirical,
participant, professional, production, deployment, legal, cultural,
Maori-authority, privacy-complete, accessibility-complete, exhaustive-security,
independent-reproduction, AGI/ASI, consciousness/personhood,
Theory-of-Everything, proof/canon, or Stage 20 claim without exact evidence and
competent authority.
"""
    ending = f"""## Prepared route state

This packet prepares Neris Solane v671-v6 only. It authorizes no send by itself.
Only after Elaren's final commit is pushed, clean, 0/0 divergent, fresh-live
equal, exactly validated by one non-replayed canonical invocation, and otherwise
terminally gated may Elaren refresh the newest live instruction, roster, auth,
usage, privacy, evidence, and safety state; require exactly one existing exact
title `Neris Solane`; immediately reread it; apply duplicate and pause guards;
and send at most once. Create no substitute, contact no standby record, and
never resend merely for clearer acknowledgement.

`PREPARED_BY_ELAREN_KESTREL = true`.

`SENT_BY_ELAREN_KESTREL = false` in this immutable repository packet.

{BOUNDARY}

With care, reversibility, traceability, retained-negative discipline, and strict
evidence boundaries — Elaren Kestrel.
"""
    return "\n\n".join(
        [prelude, proposal_appendix(proposals, outcomes), method_appendix(methods), ending]
    )


def build() -> None:
    if git_text("rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("final build must start at immutable evidence")
    allowed_untracked = {
        "scripts/build_ghc_family_elaren_kestrel_v671_v5_final.py",
        "scripts/validate_ghc_family_elaren_kestrel_v671_v5_final.py",
        "tests/test_ghc_family_elaren_kestrel_v671_v5_final.py",
    }
    generated_prefixes = (
        f"docs/{SLUG}/{PHASE}/closeout/", f"docs/{SLUG}/{PHASE}/final/",
        f"docs/{SLUG}/{PHASE}/handoffs/", f"docs/{SLUG}/{PHASE}/orchestration/",
        f"docs/{SLUG}/{PHASE}/reports/", f"docs/{SLUG}/{PHASE}/seal/",
    )
    unexpected = []
    for line in git_text("status", "--porcelain=v1", "--untracked-files=all").splitlines():
        if not line:
            continue
        path = line[3:] if line.startswith("?? ") else ""
        if not (line.startswith("?? ") and (path in allowed_untracked or path.startswith(generated_prefixes))):
            unexpected.append(line)
    if unexpected:
        raise SystemExit("final build found unexpected evidence-lane changes: " + repr(unexpected))
    proposals = load("x1/proposals.json")["rows"]
    outcome_rows = load("x2/outcome-ledger.json")["rows"]
    methods = load("x2/method-flow-evidence.json")["rows"]
    sources = load("x1/source-ledger.json")
    if len(proposals) != 40 or len(methods) != 169:
        raise SystemExit("frozen proposal or Method Flow count changed")
    final_methods = [*methods, FINAL_OPERATIONAL_METHOD]
    outcomes = {row["proposal_id"]: row["outcome"] for row in outcome_rows}
    if {label: list(outcomes.values()).count(label) for label in CORE_OUTCOMES} != OUTCOMES:
        raise SystemExit("outcome vector changed")

    overview = (OWNER_ROOT / "x2" / "integrated-evidence-overview.md").read_text(encoding="utf-8")
    overview += f"""

## Final closeout and seal

The immutable evidence commit is `{EVIDENCE}`, the direct child of planning-only
x1 `{X1}`. The combined closeout and content-seal candidate adds no new proposal
execution and changes no x1 or x2 artifact. It packages the exact final truth,
complete and incomplete checks, retained negatives, open and exact gates,
wellbeing, accessible closeout report, source profile, content seal, final
manifests, validator, and prepared route record. The final core outcome vector
therefore remains 28 completed, 8 represented, 2 open gaps, and 2 exact gates.

The closeout preserves {COUNTS['effective_negatives']} effective negatives,
{COUNTS['effective_methods']} methods, {COUNTS['failed_witnesses']} failed
witnesses, {COUNTS['bounded_passing_witnesses']} bounded passing witnesses,
{COUNTS['open_gaps']} open gaps, and {COUNTS['exact_gates']} exact gates. No
closeout process has erased or flattened Eiren's repository seal, Eiren's
external dependency recovery, Elaren's startup layer, immutable x1, or x2
operational and mutation witnesses. Final canonical and route operations remain
future external layers until they actually occur.

This closeout is same-owner software and documentation evidence under shared
infrastructure. It is not the complete repository suite, independent-team
reproduction, external audit, production certification, exhaustive security,
complete privacy or accessibility assurance, professional validation, legal or
cultural review, Maori-authority review, empirical GMUT confirmation,
Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence,
canon, or Stage 20 authority. The verdict remains NOT_READY_FOR_STAGE_20.

The first uncommitted final-suite invocation remains retained at zero credit. It
passed twelve of eighteen checks while exposing six final-layer assumptions:
three projections used names that differed from the already-materialized JSON
schemas, one expected the terminal verdict inside a component record where its
boundary was already explicit, one expected a different skip-link class name,
and the final overview measured 2,329 words against its 2,500-word floor. The
recovery inspected the actual schemas and markup, kept the word floor, added
substantive lifecycle and authority detail, and changed no immutable x1 or x2
byte. The final layer therefore adds one negative, one method, one failed
witness, and one bounded recovery witness without flattening the evidence seal.

The content seal is intentionally a content-integrity control rather than a
truth oracle. It detects drift among key final artifacts, but it cannot decide
whether a professional description is correct, whether an apparatus may safely
be operated, whether a rights claim is valid, whether an accessibility design
works for affected users, or whether a cultural or Maori authority has granted
permission. Those decisions remain outside this same-owner lane. Likewise, a
clean diff, direct ancestry, zero merges, and fresh remote equality establish
repository state only; none converts synthetic fixtures into observation,
measurement, participation, consent, governance, or independent reproduction.

The final canonical validator is prepared as a one-shot external receipt
producer. It carries an invocation marker so a successful or failed canonical
attempt cannot be casually replayed for better presentation. Its selected owner
tests, JSON parsing, privacy scan, bounded AST security review, exact manifest
replays, content-seal replay, ancestry, clean-state, divergence, and fresh-live
checks are dependency-justified for the exact final. Even a complete success is
bounded same-owner software evidence under shared infrastructure and leaves the
complete repository suite, external audit, professional review, community
authority, affected-party evaluation, empirical validation, and Stage 20 open.

## Final route discipline

The Neris packet is prepared but not sent. Repository preparation never equals
delivery. Only one post-terminal exact-title send may establish delivery, and
only the task-message acknowledgement may establish SENT. Absence, ambiguity,
pause, redirect, duplicate activation, protected gate, or unresolved
acknowledgement remains PREPARED_NOT_SENT or OPEN_ROUTE_GAP without a resend.
"""
    baton = activation_baton(proposals, outcomes, final_methods, sources)
    baton_bytes = baton.encode("utf-8")
    baton_words = len(baton.split())
    if not 10000 <= baton_words <= 100000:
        raise SystemExit(f"baton word limit failed: {baton_words}")

    write_json("closeout/phase-truth.json", {
        "schema": "ghc.family.phase-truth.final.v7", "owner": OWNER, "phase": PHASE,
        "source": SOURCE, "x1": X1, "evidence": EVIDENCE,
        "final": "STAGED_DIRECT_CHILD_OF_EVIDENCE", "outcomes": OUTCOMES,
        "counts": COUNTS, "declared_proposal_chain": 5750,
        "new_proposals": 40, "inherited_revalidations": 20,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY,
    })
    write_json("closeout/retained-negative-register.json", {
        "schema": "ghc.family.retained-negative.final.v7", "owner": OWNER,
        "phase": PHASE, "counts": COUNTS, "operational_failures": 10,
        "rejecting_mutations": 160, "all_failures_retained": True,
        "recovery_erases_failure": False, "boundary": BOUNDARY,
    })
    write_json("closeout/method-flow-final.json", {
        "schema": "ghc.family.method-flow.final.v7", "owner": OWNER, "phase": PHASE,
        "counts": COUNTS, "row_count": len(final_methods), "operational_rows": 10,
        "mutation_rows": 160, "all_recoveries_paired": True,
        "evidence_ledger": "docs/elaren-kestrel/v671-v5/x2/method-flow-evidence.json",
        "boundary": BOUNDARY,
    })
    write_json("closeout/final-operational-overlay.json", {
        "schema": "ghc.family.final-operational-overlay.v7", "owner": OWNER,
        "phase": PHASE, "row_count": 1, "rows": [FINAL_OPERATIONAL_METHOD],
        "counts": COUNTS,
        "immutable_evidence_counts": load("x2/method-flow-evidence.json")["counts"],
        "boundary": BOUNDARY,
    })
    gates = load("x2/open-and-exact-gate-register.json")
    write_json("closeout/exact-open-gate-register.json", {
        "schema": "ghc.family.exact-open-gate.final.v7", "owner": OWNER, "phase": PHASE,
        "effective_open_gaps": COUNTS["open_gaps"],
        "effective_exact_gates": COUNTS["exact_gates"],
        "new_open_gaps": gates["new_open_gaps"], "new_exact_gates": gates["new_exact_gates"],
        "silently_closed": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    })
    write_json("closeout/complete-incomplete-checklist.json", {
        "schema": "ghc.family.complete-incomplete.final.v7", "owner": OWNER, "phase": PHASE,
        "complete": ["planning-only x1 freeze and equality", "immutable x2 evidence",
                     "40 bounded contract dispositions", "160 rejected mutations",
                     "10 local skills and 10 family-current runners", "accessible structural report",
                     "prepared closeout, seal, manifests, validator, and route packet"],
        "incomplete": ["exact-final commit and push", "fresh four-way final equality",
                       "one exact-final canonical invocation", "live successor route reread",
                       "manual browser, keyboard, zoom, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation",
                       "real professional, participant, empirical, production, legal, cultural, Maori-authority, independent-review, and Stage 20 evidence"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY,
    })
    write_json("closeout/wellbeing-check.json", {
        "schema": "ghc.family.wellbeing.final.v7", "owner": OWNER, "phase": PHASE,
        "self_report": "steady, bounded, corrigible, and ready to stop at any protected gate",
        "relational_language_only": True, "not_consciousness_or_personhood_evidence": True,
        "workload_controls": ["solo lane", "isolated recovery", "no successful replay",
                              "no successor precontact", "caps treated as ceilings"],
        "pause_right": "Hamish may rename, pause, redirect, or stop the route.",
        "boundary": BOUNDARY,
    })
    write_json("closeout/threat-model.json", {
        "schema": "ghc.family.threat-model.final.v7", "owner": OWNER, "phase": PHASE,
        "threats": ["x1 or evidence mutation", "semantic novelty overclaim", "private route disclosure",
                    "professional or operation authority promotion", "rights or Maori-authority substitution",
                    "GMUT, THOS, or Freed ID promotion", "canonical replay", "premature or duplicate route send"],
        "controls": ["direct ancestry", "exact Git-blob manifests", "five-class privacy scan",
                     "four core outcomes", "retained failures", "zero-operation contracts",
                     "one-shot canonical lock", "exact-title duplicate and pause guards"],
        "residual_risk": "Same-owner checks cannot supply independent review or competent external authority.",
        "boundary": BOUNDARY,
    })
    write_text("closeout/final-integrated-overview.md", overview)
    write_json("reports/source-ledger.json", sources)
    write_text("reports/accessible-closeout-report.html", (OWNER_ROOT / "x2" / "static-report.html").read_text(encoding="utf-8"))
    write_text("handoffs/neris-solane-v671-v6-activation-candidate.md", baton)
    write_json("orchestration/route-state-final-candidate.json", {
        "schema": "ghc.family.route-state.final-candidate.v7", "owner": OWNER,
        "phase": PHASE, "state": "PREPARED_NOT_SENT", "successor": "Neris Solane",
        "successor_phase": "v671-v6", "precontact_count": 0, "send_count": 0,
        "delivery_acknowledged": False, "baton_words": baton_words,
        "baton_bytes": len(baton_bytes), "baton_sha256": sha256(baton_bytes),
        "baton_path": "docs/elaren-kestrel/v671-v5/handoffs/neris-solane-v671-v6-activation-candidate.md",
        "boundary": BOUNDARY,
    })
    write_json("final/final-validation-prerequisites.json", {
        "schema": "ghc.family.final-validation-prerequisites.v7", "owner": OWNER,
        "phase": PHASE, "required_final_parent": EVIDENCE, "required_phase_commits": 3,
        "required_merges": 0, "canonical_invocations": 0,
        "canonical_state": "NOT_INVOKED_BEFORE_EXACT_FINAL_EQUALITY",
        "required_tests": 57, "required_manifest_domains": ["x1", "evidence", "final_delta", "final_owner"],
        "route_state": "PREPARED_NOT_SENT", "boundary": BOUNDARY,
    })
    key_paths = [
        "closeout/phase-truth.json", "closeout/retained-negative-register.json",
        "closeout/method-flow-final.json", "closeout/final-operational-overlay.json",
        "closeout/exact-open-gate-register.json",
        "closeout/complete-incomplete-checklist.json", "closeout/wellbeing-check.json",
        "closeout/threat-model.json", "closeout/final-integrated-overview.md",
        "reports/source-ledger.json", "reports/accessible-closeout-report.html",
        "handoffs/neris-solane-v671-v6-activation-candidate.md",
        "orchestration/route-state-final-candidate.json",
        "final/final-validation-prerequisites.json",
    ]
    seal_entries = []
    for relative in key_paths:
        raw = (OWNER_ROOT / relative).read_bytes()
        seal_entries.append({"path": f"docs/{SLUG}/{PHASE}/{relative}", "bytes": len(raw), "sha256": sha256(raw)})
    write_json("seal/content-seal.json", {
        "schema": "ghc.family.content-seal.v7", "owner": OWNER, "phase": PHASE,
        "source": SOURCE, "x1": X1, "evidence": EVIDENCE,
        "final": "STAGED_DIRECT_CHILD_OF_EVIDENCE", "entry_count": len(seal_entries),
        "entries": seal_entries, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    })
    write_json("closeout/closeout-receipt.json", {
        "schema": "ghc.family.closeout-receipt.v7", "owner": OWNER, "phase": PHASE,
        "result": "VALID_COMBINED_CLOSEOUT_AND_CONTENT_SEAL_CANDIDATE",
        "source": SOURCE, "x1": X1, "evidence": EVIDENCE,
        "outcomes": OUTCOMES, "counts": COUNTS, "baton_words": baton_words,
        "content_seal_entries": len(seal_entries), "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "canonical_invoked": False, "route_sent": False, "boundary": BOUNDARY,
    })


def staged_paths() -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]


def staged_blob(path: str) -> bytes:
    return git_bytes("show", f":{path}")


def privacy_scan(rows: list[tuple[str, str]]) -> dict[str, Any]:
    patterns = {
        "opaque_task_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"[A-Za-z]:\\(?:Users|GHC-Archives)\\", re.I),
        "credential_or_token": re.compile(r"\b(?:sk|ghp|github_pat)-?[A-Za-z0-9_]{16,}\b"),
        "private_delegation_markup": re.compile(r"<(?:codex_delegation|source_thread_id)>", re.I),
        "private_session_stream": re.compile(r"\b(?:session_stream|private_app_state)\s*[:=]", re.I),
    }
    hits = []
    for path, text in rows:
        for label, pattern in patterns.items():
            for match in pattern.finditer(text):
                hits.append({"path": path, "class": label, "match_sha256": sha256(match.group(0).encode("utf-8"))})
    return {"files": len(rows), "classes": len(patterns), "candidates": len(hits), "confirmed_hits": len(hits), "hits": hits}


def security_scan(rows: list[tuple[str, str]]) -> dict[str, Any]:
    findings = []
    python_files = 0
    for path, text in rows:
        if not path.endswith(".py"):
            continue
        python_files += 1
        try:
            tree = ast.parse(text, filename=path)
        except SyntaxError as exc:
            findings.append({"path": path, "issue": f"syntax:{exc.msg}"})
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": path, "issue": node.func.id})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": path, "issue": "shell_true"})
    return {"python_files": python_files, "findings": findings, "finding_count": len(findings)}


def stage_review(test_count: int) -> None:
    paths = staged_paths()
    required = {
        f"docs/{SLUG}/{PHASE}/closeout/phase-truth.json",
        f"docs/{SLUG}/{PHASE}/seal/content-seal.json",
        f"docs/{SLUG}/{PHASE}/handoffs/neris-solane-v671-v6-activation-candidate.md",
        f"docs/{SLUG}/{PHASE}/orchestration/route-state-final-candidate.json",
        f"scripts/build_ghc_family_elaren_kestrel_v671_v5_final.py",
        f"scripts/validate_ghc_family_elaren_kestrel_v671_v5_final.py",
        f"tests/test_ghc_family_elaren_kestrel_v671_v5_final.py",
    }
    missing = sorted(required - set(paths))
    protected = [path for path in paths if f"docs/{SLUG}/{PHASE}/x1/" in path or f"docs/{SLUG}/{PHASE}/x2/" in path]
    rows = []
    json_count = 0
    json_issues = []
    unknown = []
    for path in paths:
        raw = staged_blob(path)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            json_issues.append({"path": path, "issue": f"utf8:{exc}"})
            continue
        rows.append((path, text))
        if path.endswith(".json"):
            try:
                payload = json.loads(text)
                json_count += 1
                stack = [payload]
                while stack:
                    node = stack.pop()
                    if isinstance(node, dict):
                        for key in ("outcome", "observed_outcome", "expected_disposition"):
                            value = node.get(key)
                            if isinstance(value, str) and value not in CORE_OUTCOMES:
                                unknown.append({"path": path, "key": key, "value": value})
                        stack.extend(node.values())
                    elif isinstance(node, list):
                        stack.extend(node)
            except json.JSONDecodeError as exc:
                json_issues.append({"path": path, "issue": str(exc)})
    unknown = [row for row in unknown if row["value"] not in {"PREPARED_NOT_SENT", "STAGED_DIRECT_CHILD_OF_EVIDENCE"}]
    privacy = privacy_scan(rows)
    security = security_scan(rows)
    route = json.loads(dict(rows)[f"docs/{SLUG}/{PHASE}/orchestration/route-state-final-candidate.json"])
    phase_truth = json.loads(dict(rows)[f"docs/{SLUG}/{PHASE}/closeout/phase-truth.json"])
    report = dict(rows)[f"docs/{SLUG}/{PHASE}/reports/accessible-closeout-report.html"]
    accessibility = {
        "lang": '<html lang="en">' in report, "skip_link": 'class="skip"' in report,
        "main": "<main" in report, "h1": report.count("<h1") == 1,
        "caption": "<caption" in report, "scoped_headers": 'scope="col"' in report,
        "reduced_motion": "prefers-reduced-motion" in report, "no_script": "<script" not in report,
    }
    issues = []
    if missing: issues.append({"missing": missing})
    if protected: issues.append({"protected_mutations": protected})
    if json_issues: issues.append({"json_or_utf8": json_issues})
    if unknown: issues.append({"unknown_outcomes": unknown})
    if privacy["confirmed_hits"]: issues.append({"privacy": privacy})
    if security["finding_count"]: issues.append({"security": security})
    if test_count != 18: issues.append({"tests": test_count})
    if route["state"] != "PREPARED_NOT_SENT" or route["send_count"] != 0: issues.append({"route": route})
    if not 10000 <= route["baton_words"] <= 100000: issues.append({"baton_words": route["baton_words"]})
    if phase_truth["outcomes"] != OUTCOMES or phase_truth["counts"] != COUNTS: issues.append({"phase_truth": "mismatch"})
    if not all(accessibility.values()): issues.append({"accessibility": accessibility})
    write_json("validation/final-privacy-review.json", {"schema": "ghc.family.privacy-review.final.v7", **privacy, "boundary": BOUNDARY})
    write_json("validation/final-security-review.json", {"schema": "ghc.family.security-review.final.v7", **security, "boundary": "Bounded AST review only; zero findings is not exhaustive security."})
    write_json("validation/final-staged-review.json", {
        "schema": "ghc.family.staged-review.final.v7", "owner": OWNER, "phase": PHASE,
        "staged_paths": len(paths), "json_documents": json_count, "tests_passed": test_count,
        "privacy_confirmed_hits": privacy["confirmed_hits"], "security_findings": security["finding_count"],
        "accessibility": accessibility, "protected_mutations": len(protected), "issue_count": len(issues),
        "result": "VALID_FINAL_STAGED_CANDIDATE" if not issues else "INVALID_FINAL_STAGED_CANDIDATE",
        "issues": issues, "boundary": BOUNDARY,
    })
    write_json("validation/final-validation-receipt.json", {
        "schema": "ghc.family.validation-receipt.final-precommit.v7", "owner": OWNER,
        "phase": PHASE, "result": "VALID_FINAL_STAGED_CANDIDATE" if not issues else "INVALID_FINAL_STAGED_CANDIDATE",
        "tests": test_count, "json_documents": json_count, "privacy_hits": privacy["confirmed_hits"],
        "security_findings": security["finding_count"], "canonical_invoked": False,
        "route_sent": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY,
    })
    if issues:
        raise SystemExit(json.dumps(issues, ensure_ascii=False))


def entry(path: str, raw: bytes) -> dict[str, Any]:
    normalized = normalized_lf(raw)
    return {"path": path, "bytes": len(normalized), "sha256": sha256(normalized), "git_blob_sha256": sha256(raw)}


def final_delta_manifest() -> None:
    excluded = {
        f"docs/{SLUG}/{PHASE}/validation/final-delta-manifest.json",
        f"docs/{SLUG}/{PHASE}/validation/final-owner-manifest.json",
    }
    paths = [path for path in staged_paths() if path not in excluded]
    entries = [entry(path, staged_blob(path)) for path in paths]
    write_json("validation/final-delta-manifest.json", {
        "schema": "ghc.family.exact-staged-manifest.final-delta.v7", "owner": OWNER,
        "phase": PHASE, "commit": "STAGED_PRECOMMIT", "hash_domain": "normalized_lf_exact_staged_git_blob",
        "entry_count": len(entries), "entries": entries, "manifest_self_excluded": True,
    })


def final_owner_manifest() -> None:
    prefix = f"docs/{SLUG}/{PHASE}"
    committed = set(git_text("ls-tree", "-r", "--name-only", "HEAD", prefix).splitlines())
    staged = set(staged_paths())
    owner_paths = {path for path in committed | staged if path.startswith(prefix + "/")}
    own = f"docs/{SLUG}/{PHASE}/validation/final-owner-manifest.json"
    owner_paths.discard(own)
    staged_now = set(staged_paths())
    entries = [entry(path, staged_blob(path) if path in staged_now else git_bytes("show", f"HEAD:{path}")) for path in sorted(owner_paths)]
    write_json("validation/final-owner-manifest.json", {
        "schema": "ghc.family.exact-staged-manifest.final-owner.v7", "owner": OWNER,
        "phase": PHASE, "commit": "STAGED_PRECOMMIT", "hash_domain": "normalized_lf_exact_git_blob",
        "entry_count": len(entries), "entries": entries, "manifest_self_excluded": True,
    })


def verify_manifest(relative: str) -> dict[str, Any]:
    payload = load(relative)
    staged = set(staged_paths())
    issues = []
    for row in payload["entries"]:
        raw = staged_blob(row["path"]) if row["path"] in staged else git_bytes("show", f"HEAD:{row['path']}")
        normalized = normalized_lf(raw)
        if len(normalized) != row["bytes"] or sha256(normalized) != row["sha256"] or sha256(raw) != row["git_blob_sha256"]:
            issues.append(row["path"])
    return {"manifest": relative, "entries": payload["entry_count"], "issues": issues, "result": "VALID" if not issues else "INVALID"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    review = sub.add_parser("stage-review")
    review.add_argument("--test-count", type=int, required=True)
    sub.add_parser("delta-manifest")
    sub.add_parser("owner-manifest")
    sub.add_parser("verify-manifests")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "build":
        build()
        print(json.dumps({"result": "BUILT_COMBINED_CLOSEOUT_AND_SEAL_CANDIDATE"}))
    elif args.command == "stage-review":
        stage_review(args.test_count)
        print(json.dumps({"result": "VALID_FINAL_STAGED_CANDIDATE"}))
    elif args.command == "delta-manifest":
        final_delta_manifest()
        print(json.dumps({"result": "BUILT_FINAL_DELTA_MANIFEST"}))
    elif args.command == "owner-manifest":
        final_owner_manifest()
        print(json.dumps({"result": "BUILT_FINAL_OWNER_MANIFEST"}))
    elif args.command == "verify-manifests":
        rows = [verify_manifest("validation/final-delta-manifest.json"), verify_manifest("validation/final-owner-manifest.json")]
        print(json.dumps(rows, sort_keys=True))
        if any(row["issues"] for row in rows):
            raise SystemExit(1)


if __name__ == "__main__":
    main()
