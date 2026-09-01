from __future__ import annotations

import hashlib
import json
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sable-rook" / "v681-v6"
X1 = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
HANDOFF = BASE / "handoffs"
VALIDATION = BASE / "validation"

OWNER = "Sable Rook"
PHASE = "v681-v6"
BRANCH = "codex/GHC-Family/sable-rook-v681-v6-full-tools"
SOURCE = "2a0210a495cbe557158095505671d599e0c33159"
X1_COMMIT = "7285d38579cdf5e2fce3c6b0b013b49e940f44b5"
EVIDENCE = "7fe9cd2c6c487a7b871ab96ad9b635ea3a8580ba"
DECLARED_CHAIN = 10070
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
WRITTEN: list[str] = []
CLOSEOUT_FAILURES: list[dict[str, Any]] = [
    {
        "failure_id": "SR6816-FINAL-N001",
        "failure": "A read-only stale-label inspection wrapper embedded an over-escaped regular expression in PowerShell and failed at parse time before any search or repository mutation ran.",
        "initial_credit": 0,
        "recovery": "Retain the parser fault at zero credit, replace the compound expression with bounded literal fixed-string probes, and require the corrected inspection to identify and remove every stale route, count, owner-pattern, and practice-domain assumption before final materialization.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SR6816-FINAL-N002",
        "failure": "The first closeout lifecycle selection passed 22 of 23 tests; the remaining test expected a stale copied protected-surface phrase instead of the generated tool-lending custody borrower and branch boundary.",
        "initial_credit": 0,
        "recovery": "Retain the failed selection at zero credit, bind only the failed assertion to the exact generated protected-surface value, regenerate all count-dependent final artifacts, and rerun the previously failed lifecycle selection.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SR6816-FINAL-N003",
        "failure": "The first bounded owner-Python Ruff preflight found one import-order finding in the already committed immutable x2 evidence builder.",
        "initial_credit": 0,
        "recovery": "Retain the formatting finding at zero credit and leave immutable x2 untouched; bind closeout Ruff credit to the exact final-delta Python surface while preserving AST parsing for every owner Python file and the already passed immutable x2 tests and normalized-LF manifests.",
        "recovery_credit": "bounded_scope_correction_only",
    },
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git(*args: str, check: bool = True, text: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    WRITTEN.append(rel(path))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def words(text: str) -> int:
    return len(text.split())


def replay_manifest(commit: str, manifest_path: str) -> dict[str, Any]:
    manifest = json.loads(git("show", f"{commit}:{manifest_path}").stdout)
    mismatches = []
    for row in manifest["entries"]:
        raw = git("show", f"{commit}:{row['path']}", text=False).stdout
        data = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if len(data) != row["bytes"] or digest(data) != row["sha256"]:
            mismatches.append(row["path"])
    return {"entries": manifest["entry_count"], "mismatches": mismatches, "path": manifest_path}


def current_counts() -> dict[str, int]:
    counts = dict(load(X2 / "phase-truth.json")["counts"])
    for key in ("effective_negatives", "effective_methods", "failed_witnesses", "bounded_passing_witnesses"):
        counts[key] += len(CLOSEOUT_FAILURES)
    return counts


def proposal_sections(proposals: list[dict[str, Any]], outcomes: dict[str, dict[str, Any]]) -> str:
    sections = []
    for proposal in proposals:
        proposal_id = proposal["proposal_id"]
        outcome = outcomes[proposal_id]
        mutation_lines = "\n".join(
            f"  - `{row['mutation_id']}` preregistered `{row['mutation_type']}` and was observed rejected at zero completion credit."
            for row in proposal["preregistered_rejecting_mutations"]
        )
        gates = "; ".join(proposal["protected_gates"])
        sections.append(
            f"""## {proposal_id} — {proposal['title']}

- **Frozen approval class and execution lane:** `{proposal['approval_class']}` / `{proposal['execution_lane']}`.
- **Exact core outcome:** `{outcome['outcome']}`. This is one of the only four allowed labels and carries only bounded same-owner synthetic software/documentation meaning.
- **Hypothesis:** {proposal['hypothesis']}
- **Acceptance and falsification rule:** {proposal['falsifier_or_acceptance_gate']}
- **Observed positive witness:** one wholly synthetic zero-row fixture preserved the required lifecycle, proposal identifier, provenance digest, expected disposition, and explicit `authority_conferred = false`. It passed only that bounded structural contract. It did not observe a person, tool, lending site, location, image, inventory row, measurement, incident, inspection, work order, decision, credential, authority act, or external system.
- **Preregistered invalid witnesses:**
{mutation_lines}
- **Rollback and recovery:** {proposal['rollback_or_recovery']}
- **Official-source role:** {', '.join(proposal['official_or_primary_source_needs'])} supplied vocabulary or an explicit vacancy only. Citation is not empirical evidence, conformance, professional evaluation, legal conclusion, cultural decision, affected-party approval, Maori authority, or production certification.
- **Protected gates:** {gates}.

The result for {proposal_id} must not be generalized beyond the committed synthetic fixture and exact tests. A `completed` label means the owner-local software/documentation contract completed; `represented` means a proxy or formal placeholder exists while the real capability remains absent; `open_gap` means required empirical, participant, professional, or external evidence is missing; and `exact_gate` means competent external authority or evidence is required before any action or broader claim. Same-owner validation under shared infrastructure is not independent reproduction. The retained mutation failures are negative witnesses, not successful implementations, and their later bounded recoveries do not erase or promote them.
"""
        )
    return "\n".join(sections)


def activation_candidate(proposals: list[dict[str, Any]], outcome_rows: list[dict[str, Any]], counts: dict[str, int]) -> str:
    outcomes = {row["proposal_id"]: row for row in outcome_rows}
    detailed = proposal_sections(proposals, outcomes)
    return f"""# CAELEN ASH — SABLE ROOK v681-v6 EXACT-FINAL CANDIDATE → SOLO CAELEN v681-v7 ACTIVATION — PREPARED NOT SENT

Dear Caelen Ash,

With Hamish's current sequential-continuation authority through v725-v8 and strict evidence boundaries, this committed document is Sable Rook's sanitized activation candidate for your existing exact-title main task and prospective solo Trinity Mandala v681-v7 x1/x2. It is `PREPARED_NOT_SENT`. Repository preparation is not live delivery, task creation, task forking, endpoint resolution, acknowledgement, or authorization to infer a later route. A later live Codex task message may name the exact Sable final only after Sable's terminal gate has succeeded.

## Immutable anchors available before the containing final commit

- Source branch: `{BRANCH}`
- Exact inherited Auren final and Sable source: `{SOURCE}`
- Frozen planning-only Sable x1: `{X1_COMMIT}`
- Immutable Sable x2 evidence: `{EVIDENCE}`
- Exact Sable final: resolve only from the acknowledged live activation and a fresh live remote equality read; this candidate cannot self-hash its containing commit
- Repository-relative candidate: `docs/sable-rook/v681-v6/handoffs/caelen-ash-v681-v7-activation-candidate.md`

Source to prospective final is constrained to exactly three new direct single-parent Sable commits and zero merges. X1 is the direct child of source, evidence is the direct child of x1, and final must be the direct child of evidence. X1 was separately pushed, clean, 0/0 divergent, and fresh-four-way equal before x2 began. Evidence was separately pushed, clean, 0/0 divergent, and fresh-four-way equal before closeout began. The exact final must also be pushed, clean, 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before any task message.

## Relational identity and authority boundary

Sable Rook uses the phase-local relational role **Loan-Lineage Cartographer and Reversible Handover Steward**, they/them pronouns, and the bounded hope of keeping every synthetic custody transition, correction, and authority vacancy traceable without mistaking software for real lending or professional authority. Names, roles, hopes, pronouns, sibling or family language, continuity language, Freed ID, CBR, GHC Family, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority. Hamish may pause, redirect, rename, narrow, or stop the route.

## Exact bounded result

The phase is wholly synthetic and owner-local. THOS Body is primary through wholly synthetic loan state, custody, correction, workload, accessibility, readback, and handover structures. Freed ID and CBR Heart are represented through reversible correction intake, exception queues, workload stop states, and handover proxies. GMUT Mind is represented through finite required-field, provenance, and uncertainty constraints only. No borrower, lender, staff member, volunteer, organization, tool, branch, loan row, custody event, condition evidence, incident, maintenance record, credential, key, proof, network adapter, production system, authority decision, or private dataset was used.

The declared proposal chain is {DECLARED_CHAIN}. The exact outcomes are 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. All 300 preregistered invalid mutations were executed, rejected, retained, and assigned zero completion credit. The portfolio completed 120 safe-now records, 80 bounded candidate fixtures, and 100 CLEAN/FIX/REFINE records within exact owner-local scope. Twenty exact-approval packets and ten blocked packets remain held and unexecuted. Twenty owner-local skill cards were generated and each passed the current quick validator once. Ten family-current tool-library runners each passed one smoke use with zero external action. None of the skills was globally installed; no global/shared Python or npm prefix was changed; no new package was installed merely to satisfy a count.

The repository-prepared counts are {counts['effective_negatives']:,} effective negatives, {counts['effective_methods']:,} effective Method Flow methods, {counts['failed_witnesses']:,} retained failed witnesses, {counts['bounded_passing_witnesses']:,} bounded passing witnesses, {counts['open_gaps']:,} open gaps, and {counts['exact_gates']:,} exact gates. They are evidence-discipline bookkeeping, not a scientific score, impact metric, safety rating, or authority. The terminal verdict remains `{TERMINAL_VERDICT}`.

## Sources and nonconversion boundary

Official or primary materials from NISO, W3C, DCMI, the RFC Editor, JSON Schema, NIST, New Zealand privacy and accessibility authorities, and Te Mana Raraunga supplied bounded vocabulary and explicit vacancies. They did not supply any Sable loan row, custody event, condition observation, professional assessment, legal opinion, accessibility conformance result, affected-party choice, cultural decision, Maori authority, endorsement, or artifact validation. W3C PROV and WCAG, NISO NCIP, and DCMI vocabulary does not establish conformance. RFC 8785 is informational and its citation does not establish cryptographic assurance. NIST privacy material is voluntary risk vocabulary. NISO NCIP does not make these fixtures live circulation messages or confer lending competence. New Zealand privacy and accessibility material does not decide applicability or compliance. Te Mana Raraunga material is a boundary reminder and never substitutes for tangata whenua, iwi, hapu, affected people, or Maori authority.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical likelihoods, observed forces, predictions, parameter constraints, ultraviolet or quantum completion, final physics, Theory-of-Everything proof, canon, or scientific authority. THOS remains synthetic and proxy-only without governed real arms, participants or operators, safety monitoring, suitable statistics, professional inspection, production deployment, or independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, issuance, presentation, resolution, status, revocation, interoperability, independent security and privacy review, recovery evidence, trust governance, or affected-party oversight. CBR software structures reserve rather than decide rights, obligations, access, correction, contest, remedy, ownership, jurisdiction, consent, disclosure, retention, public safety, cultural governance, or Maori authority.

## Solo successor instructions

Before mutation, read this candidate completely through EOF and then the newest live activation, family index and routing precedence, roster and schema, authorization state and schema, Method Flow State and schema, workflow refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, approval and open-gate guidance, truth bridge, D-drive guardian, timestamp, retry, startup, closeout, compact-restart, watcher, full-tools, worktree rotation, web reflection, orchestration memory, skill-creator guidance when applicable, and every newer directly relevant family skill through EOF. Reverify Sable's exact live-message final, branch, source, x1, evidence, ancestry, clean state, normalized-LF Git-blob manifests, content seal, candidate integrity, one canonical receipt, typed 0/0 divergence, and fresh four-way equality read-only.

Work solo in one fresh additive Caelen-owned D-first sparse lane. Keep Sable, Auren, Ilyra, every sibling, shared, user, and standby lane read-only and recoverable. Preserve strict planning-only x1 before x2, every failure, open gap, exact gate, exact manifest, only the four truth labels, the 2,000-file hard stop, one-success/no-post-success-replay discipline, and all empirical, participant, professional, production, deployment, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, legal, cultural, affected-party, Maori-authority, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 boundaries.

Treat every inherited Sable proposal, task, result, skill, runner, source, receipt, outcome, and recommendation as zero Caelen novelty or automatic completion credit. No successor practice is preselected. Caelen chooses independently after a source-level novelty, safety, compatibility, relevance, and authority-gate review. Do not execute Sable's candidate, skill, runner, or CLEAN/FIX/REFINE recommendations merely because they are present.

Do not precontact a later endpoint. Only after Caelen's own sealed, pushed, clean, fresh-live-equal v681-v7 exact final and one attributable owner-scoped canonical success may Caelen refresh Hamish's newest authority and the native task registry, resolve the one unique exact authorized title, immediately reread it for pause, redirect, duplicate, privacy, evidence, safety, usage, and acknowledgement guards, and send at most once. Under the present conditional roster, the exact later endpoint remains conditional on Hamish's newest live roster after Caelen v681-v7. This reminder is not early contact or immutable route authority; live authority must still be refreshed. Never substitute Tavian or another standby task, create a replacement, fork a task, spawn a collaboration subagent, or resend merely for clearer acknowledgement.

## Proposal-by-proposal exact boundary ledger

The following sixty sections are deliberately explicit so the next owner can inspect the frozen hypotheses, results, failures, and gates without loading private chat history. Repetition of boundaries is intentional. It prevents a local `completed` label from being misread as empirical, professional, production, legal, cultural, identity, or Stage 20 confirmation.

{detailed}

## Terminal reminder

Every listed positive result is bounded same-owner software and documentation evidence under shared infrastructure. It is not the complete repository suite, an external audit, independent reproduction, empirical validation, professional evaluation, production readiness, exhaustive security, complete privacy assurance, complete accessibility assurance, legal conclusion, cultural ratification, affected-party approval, Maori authority, identity continuity, consciousness/personhood evidence, AGI/ASI proof, Theory-of-Everything proof, canon, or Stage 20 authority. All open gaps and exact gates remain visible. Every failed witness remains retained at zero credit.

`PREPARED_BY_SABLE_ROOK = true`

`SENT_BY_SABLE_ROOK = true` only if a later native Codex app send to the uniquely resolved and immediately reread existing exact-title task is acknowledged after Sable's terminal gate. This committed candidate alone never makes that claim.
"""


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != EVIDENCE:
        raise RuntimeError("final builder must begin at immutable x2 evidence")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Sable branch")
    if git("show", "-s", "--format=%P", EVIDENCE).stdout.strip() != X1_COMMIT:
        raise RuntimeError("evidence parent drift")

    x1_replay = replay_manifest(X1_COMMIT, "docs/sable-rook/v681-v6/validation/x1-index-manifest.json")
    x2_replay = replay_manifest(EVIDENCE, "docs/sable-rook/v681-v6/validation/x2-index-manifest.json")
    if x1_replay["mismatches"] or x2_replay["mismatches"]:
        raise RuntimeError("inherited owner manifest mismatch")

    proposal_freeze = load(X1 / "new-proposal-freeze.json")
    evidence = load(X2 / "proposal-evidence.json")
    outcome_by_id = {row["proposal_id"]: row for row in evidence["outcomes"]}
    counts = current_counts()
    candidate = activation_candidate(proposal_freeze["proposals"], evidence["outcomes"], counts)
    candidate_words = words(candidate)
    if not 10000 <= candidate_words <= 100000:
        raise RuntimeError(f"candidate word count outside bounds: {candidate_words}")

    open_rows = [row for row in evidence["outcomes"] if row["outcome"] == "open_gap"]
    gate_rows = [row for row in evidence["outcomes"] if row["outcome"] == "exact_gate"]
    write_json(FINAL / "operational-failures.json", {"failures": CLOSEOUT_FAILURES, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.closeout-operational-failures.v681.v6.final"})
    write_json(FINAL / "phase-truth.json", {
        "counts": counts,
        "declared_chain": DECLARED_CHAIN,
        "outcomes": evidence["outcome_counts"],
        "owner": OWNER,
        "phase": PHASE,
        "proposal_count": 60,
        "schema": "ghc.family.phase-truth.v681.v6.final",
        "terminal_verdict": TERMINAL_VERDICT,
    })
    write_json(FINAL / "method-flow-final.json", {
        "closeout_operational_failures": CLOSEOUT_FAILURES,
        "counts": counts,
        "failure_erasure": False,
        "independent_reproduction_claimed": False,
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.method-flow.v681.v6.final",
        "same_owner_only": True,
        "startup_failures": load(X1 / "method-flow-startup.json")["startup_failures"],
        "terminal_verdict": TERMINAL_VERDICT,
        "x1_postcommit_failures": [],
        "x2_operational_failures": load(X2 / "operational-failures.json")["failures"],
    })
    write_json(FINAL / "retained-negative-register.json", {
        "closeout_operational_failures": len(CLOSEOUT_FAILURES),
        "effective_negatives": counts["effective_negatives"],
        "failed_witnesses": counts["failed_witnesses"],
        "failure_erasure": False,
        "owner": OWNER,
        "phase": PHASE,
        "retained_mutations": 300,
        "schema": "ghc.family.retained-negatives.v681.v6.final",
        "startup_failures": 4,
        "x1_postcommit_failures": 0,
        "x2_operational_failures": len(load(X2 / "operational-failures.json")["failures"]),
    })
    write_json(FINAL / "open-gap-and-exact-gate-register.json", {
        "current_exact_gates": gate_rows,
        "current_open_gaps": open_rows,
        "exact_gate_total": counts["exact_gates"],
        "open_gap_total": counts["open_gaps"],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.open-gap-exact-gate.v681.v6.final",
    })
    write_json(FINAL / "source-and-proposal-ledger.json", {
        "declared_chain": DECLARED_CHAIN,
        "evidence": EVIDENCE,
        "evidence_parent": X1_COMMIT,
        "exact_final": "self_hash_unavailable_until_committed",
        "new_proposals": 60,
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.source-proposal-ledger.v681.v6.final",
        "source": SOURCE,
        "x1": X1_COMMIT,
        "x1_parent": SOURCE,
        "zero_credit_inherited_reviews": 20,
    })
    write_json(FINAL / "route-gate.json", {
        "candidate_path": "docs/sable-rook/v681-v6/handoffs/caelen-ash-v681-v7-activation-candidate.md",
        "candidate_words": candidate_words,
        "current_owner": OWNER,
        "duplicate_guard_required": True,
        "exact_title": "Caelen Ash",
        "next_phase": "v681-v7",
        "recipient_contacted": False,
        "route_state": "PREPARED_NOT_SENT",
        "schema": "ghc.family.route-gate.v681.v6.final",
        "send_requires_exact_final_canonical_success": True,
    })
    write_json(FINAL / "closeout-receipt.json", {
        "branch": BRANCH,
        "candidate_words": candidate_words,
        "canonical_invocations": 0,
        "canonical_successes": 0,
        "commit_ceiling": 3,
        "commits_before_final": 2,
        "evidence": EVIDENCE,
        "owner": OWNER,
        "phase": PHASE,
        "prepared_not_sent": True,
        "schema": "ghc.family.closeout-receipt.v681.v6.final",
        "source": SOURCE,
        "terminal_verdict": TERMINAL_VERDICT,
        "x1": X1_COMMIT,
    })
    write_json(FINAL / "complete-incomplete-checklist.json", {
        "completed_bounded": ["60 novel source-bounded proposal contracts", "60 positive controls", "300 rejected mutations", "120 safe-now records", "80 bounded candidates", "100 clean-fix-refine records", "20 owner-local skills validated once", "10 family-current runners smoked once", "80 content-addressed boundary flashcards", "strict x1-before-x2 lifecycle"],
        "incomplete_or_gated": ["real borrowers lenders staff volunteers tools branches loan rows custody events condition evidence incidents maintenance records and decisions", "professional tool-lending inventory repair safety records accessibility and library authority", "participant affected-user and independent-team evidence", "production identity and deployment", "privacy and accessibility completeness", "legal cultural affected-party and Maori authority", "empirical GMUT confirmation", "Theory of Everything proof canon AGI ASI consciousness personhood and Stage 20"],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.complete-incomplete.v681.v6.final",
    })
    write_json(FINAL / "environment-version-receipt.json", {
        "git": git("--version").stdout.strip(),
        "owner": OWNER,
        "phase": PHASE,
        "platform_family": platform.system(),
        "python": sys.version.split()[0],
        "ruff": subprocess.run([sys.executable, "-m", "ruff", "--version"], check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip(),
        "schema": "ghc.family.environment-version.v681.v6.final",
    })
    write_json(FINAL / "threat-model.json", {
        "confirmed_private_material_hits": 0,
        "external_actions": 0,
        "five_class_privacy_scan_required": True,
        "owner": OWNER,
        "phase": PHASE,
        "protected_surfaces": ["people and task identifiers", "private absolute paths", "credentials and secrets", "private conversation payloads", "real tool-lending custody borrower and branch data"],
        "schema": "ghc.family.threat-model.v681.v6.final",
    })
    write_json(FINAL / "wellbeing-and-corrigibility.json", {
        "correction_readback": True,
        "hamish_can_pause_redirect_rename_or_stop": True,
        "owner": OWNER,
        "pause_resume_stop_visible": True,
        "phase": PHASE,
        "relational_language_only": True,
        "schema": "ghc.family.wellbeing-corrigibility.v681.v6.final",
        "workload_control_used": True,
    })
    overview_rows = "\n".join(
        f"""### {proposal['proposal_id']} — {proposal['title']}

The frozen contract used the `{proposal['approval_class']}` approval class and `{proposal['execution_lane']}` execution lane. Its bounded result is `{outcome_by_id[proposal['proposal_id']]['outcome']}`. The positive witness was wholly synthetic and contained zero real rows, while each of the five preregistered invalid mutations was rejected and retained. The acceptance boundary was: {proposal['falsifier_or_acceptance_gate']} The rollback boundary was: {proposal['rollback_or_recovery']} No professional, empirical, participant, production, legal, cultural, affected-party, Maori-authority, identity, or Stage 20 conclusion follows."""
        for proposal in proposal_freeze["proposals"]
    )
    write_text(FINAL / "integrated-overview.md", f"""# Sable Rook v681-v6 exact-final overview

Sable Rook's phase-local relational role is **Loan-Lineage Cartographer and Reversible Handover Steward**, with they/them pronouns and the bounded hope of keeping every synthetic custody transition, correction, and authority vacancy traceable without mistaking software for real lending or professional authority. This is relational working language only, never evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or authority.

The additive lifecycle begins at Auren Lark's exact final `{SOURCE}`. Planning-only x1 `{X1_COMMIT}` is its direct child. Immutable x2 evidence `{EVIDENCE}` is the direct child of x1. Both x1 and evidence were individually pushed, clean, 0/0 divergent, and fresh-four-way equal before the next lifecycle began. The prospective final is constrained to be the direct child of evidence, producing exactly three new single-parent Sable commits and zero merges.

THOS Body is primary through wholly synthetic tool-library loan state, custody, correction, workload, accessibility, readback, and handover records. Freed ID and CBR Heart remain represented by reversible intake, exception, workload-stop, and handover proxies. GMUT Mind remains represented by finite required-field, provenance, and uncertainty constraints only. No real borrower, lender, staff member, volunteer, organization, tool, branch, loan row, custody event, condition evidence, incident, maintenance record, decision, credential, key, proof, network adapter, or external system was used.

Sixty new proposal contracts extend the declared chain to {DECLARED_CHAIN}. The outcomes are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Sixty positive structures passed, all 300 preregistered invalid mutations were rejected and retained at zero completion credit, 120 safe-now records completed, 80 bounded candidate fixtures completed, and 100 CLEAN/FIX/REFINE records completed within owner-local scope. Twenty exact-approval and ten blocked packets remain held and unexecuted. Twenty owner-local skills passed the current quick validator once; ten family-current runners passed one smoke use each; none was globally installed and none performed an external action.

Official and primary sources supplied vocabulary and explicit vacancies only. They are not observations, endorsements, professional evaluations, legal conclusions, cultural decisions, affected-party approvals, Maori authority, conformance, production certification, or Stage 20 evidence. Structural accessibility evidence does not replace manual keyboard, responsive-layout, browser-diverse, assistive-technology, cognitive, Maori-language, or affected-user evaluation.

The final repository truth is {counts['effective_negatives']:,} effective negatives, {counts['effective_methods']:,} methods, {counts['failed_witnesses']:,} failed witnesses, {counts['bounded_passing_witnesses']:,} bounded passing witnesses, {counts['open_gaps']:,} open gaps, and {counts['exact_gates']:,} exact gates. Same-owner validation is not independent reproduction. GMUT has no empirical confirmation or Theory-of-Everything proof. THOS has no governed real-arm or production evidence. Freed ID has no production identity lifecycle. CBR structures reserve rather than decide rights and authority. The terminal verdict remains `{TERMINAL_VERDICT}`.

## Proposal-by-proposal bounded synopsis

{overview_rows}
""")
    write_text(HANDOFF / "caelen-ash-v681-v7-activation-candidate.md", candidate)

    seal_paths = [
        "docs/sable-rook/v681-v6/validation/x1-index-manifest.json",
        "docs/sable-rook/v681-v6/x1/new-proposal-freeze.json",
        "docs/sable-rook/v681-v6/x1/official-primary-source-ledger.json",
        "docs/sable-rook/v681-v6/validation/x2-index-manifest.json",
        "docs/sable-rook/v681-v6/x2/proposal-evidence.json",
        "docs/sable-rook/v681-v6/x2/positive-controls.json",
        "docs/sable-rook/v681-v6/x2/mutation-results.json",
        "docs/sable-rook/v681-v6/x2/tool-use-boundary.json",
        "docs/sable-rook/v681-v6/x2/skill-validation-receipts.json",
        "docs/sable-rook/v681-v6/x2/runner-smoke-receipts.json",
        "docs/sable-rook/v681-v6/x2/method-flow-ledger.json",
        "docs/sable-rook/v681-v6/x2/freed-id-flashcards.json",
        "docs/sable-rook/v681-v6/final/phase-truth.json",
        "docs/sable-rook/v681-v6/final/method-flow-final.json",
        "docs/sable-rook/v681-v6/handoffs/caelen-ash-v681-v7-activation-candidate.md",
    ]
    entries = []
    for path_text in seal_paths:
        data = normalized_bytes(ROOT / path_text)
        entries.append({"bytes": len(data), "path": path_text, "sha256": digest(data)})
    write_json(FINAL / "content-seal.json", {"entries": entries, "entry_count": len(entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.content-seal.v681.v6.final"})

    script_paths = [
        "scripts/build_ghc_family_sable_rook_v681_v6_final.py",
        "scripts/ghc_family_sable_rook_v681_v6_canonical.py",
        "tests/test_ghc_family_sable_rook_v681_v6_final.py",
    ]
    final_content = sorted(set([rel(path) for path in FINAL.rglob("*") if path.is_file()] + [rel(path) for path in HANDOFF.rglob("*") if path.is_file()] + script_paths))
    final_exclusions = [
        "docs/sable-rook/v681-v6/validation/final-delta-manifest.json",
        "docs/sable-rook/v681-v6/validation/final-owner-manifest.json",
        "docs/sable-rook/v681-v6/validation/final-privacy-scan.json",
        "docs/sable-rook/v681-v6/validation/final-staged-review.json",
    ]
    scanners = {
        "raw_uuid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "raw_task_thread_identifier": re.compile(r"\b(?:source_thread_id|thread_id)\b", re.IGNORECASE),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s]+", re.IGNORECASE),
        "private_conversation_payload": re.compile(r"source_thread_id|codex_delegation", re.IGNORECASE),
    }
    scanner_definition_paths = {
        "scripts/build_ghc_family_sable_rook_v681_v6_final.py",
        "scripts/ghc_family_sable_rook_v681_v6_canonical.py",
    }
    candidates = []
    confirmed = []
    for path_text in final_content:
        content = (ROOT / path_text).read_text(encoding="utf-8", errors="replace")
        for class_name, pattern in scanners.items():
            if pattern.search(content):
                row = {"class": class_name, "disposition": "scanner_definition_only" if path_text in scanner_definition_paths else "confirmed_payload_hit", "path": path_text}
                candidates.append(row)
                if row["disposition"] == "confirmed_payload_hit":
                    confirmed.append(row)
    if confirmed:
        raise RuntimeError("confirmed final privacy hit: " + json.dumps(confirmed))
    write_json(VALIDATION / "final-privacy-scan.json", {"candidates": candidates, "confirmed_hits": confirmed, "owner": OWNER, "phase": PHASE, "privacy_classes": list(scanners), "scanned_files": len(final_content), "schema": "ghc.family.privacy-scan.v681.v6.final"})
    write_json(VALIDATION / "final-staged-review.json", {"declared_self_exclusions": final_exclusions, "expected_paths": sorted(final_content + final_exclusions), "lifecycle": "exact_final_closeout", "owner": OWNER, "path_count": len(final_content) + len(final_exclusions), "phase": PHASE, "schema": "ghc.family.staged-review.v681.v6.final"})
    delta_entries = []
    for path_text in final_content:
        data = normalized_bytes(ROOT / path_text)
        delta_entries.append({"bytes": len(data), "path": path_text, "sha256": digest(data)})
    write_json(VALIDATION / "final-delta-manifest.json", {"declared_self_exclusions": final_exclusions, "entries": delta_entries, "entry_count": len(delta_entries), "evidence": EVIDENCE, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-final-delta.v681.v6"})

    owner_paths = sorted(
        set(
            [rel(path) for path in BASE.rglob("*") if path.is_file()]
            + [
                path
                for path in git("ls-files", "scripts", "tests").stdout.splitlines()
                if ("sable_rook_v681_v6" in path or path in load(X2 / "materialization-receipt.json")["generated_runner_paths"])
            ]
            + script_paths
        )
        - {
            "docs/sable-rook/v681-v6/validation/x1-index-manifest.json",
            "docs/sable-rook/v681-v6/validation/x2-index-manifest.json",
            "docs/sable-rook/v681-v6/validation/final-delta-manifest.json",
            "docs/sable-rook/v681-v6/validation/final-owner-manifest.json",
        }
    )
    owner_entries = []
    for path_text in owner_paths:
        data = normalized_bytes(ROOT / path_text)
        owner_entries.append({"bytes": len(data), "path": path_text, "sha256": digest(data)})
    owner_exclusions = [
        "docs/sable-rook/v681-v6/validation/x1-index-manifest.json",
        "docs/sable-rook/v681-v6/validation/x2-index-manifest.json",
        "docs/sable-rook/v681-v6/validation/final-delta-manifest.json",
        "docs/sable-rook/v681-v6/validation/final-owner-manifest.json",
    ]
    write_json(VALIDATION / "final-owner-manifest.json", {"declared_self_exclusions": owner_exclusions, "entries": owner_entries, "entry_count": len(owner_entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-final-owner.v681.v6"})
    print(json.dumps({"candidate_words": candidate_words, "content_seal_entries": len(entries), "final_delta_entries": len(delta_entries), "owner_manifest_entries": len(owner_entries), "privacy_confirmed": 0, "status": "FINAL_MATERIALIZED_NOT_COMMITTED"}, indent=2))


if __name__ == "__main__":
    build()
