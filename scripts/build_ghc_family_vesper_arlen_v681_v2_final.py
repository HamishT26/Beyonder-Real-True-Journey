from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "vesper-arlen" / "v681-v2"
X1 = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
HANDOFFS = BASE / "handoffs"
VALIDATION = BASE / "validation"
OWNER = "Vesper Arlen"
PHASE = "v681-v2"
BRANCH = "codex/GHC-Family/vesper-arlen-v681-v2-full-tools"
SOURCE = "14b34a2b7f1b1c74e3b4102b18cc5c3b5fc854d2"
X1_COMMIT = "5a5ef294b84ece97da4f2b1238d1852ce80a5b51"
EVIDENCE_COMMIT = "fd0e470dbcfd5576982819b626c18dbd99b3c2a9"
DECLARED_CHAIN = 9830
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
WRITTEN: list[str] = []


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
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def overview(proposals: list[dict[str, Any]]) -> str:
    grouped = {
        "completed": [row for row in proposals if row["expected_disposition"] == "completed"],
        "represented": [row for row in proposals if row["expected_disposition"] == "represented"],
        "open_gap": [row for row in proposals if row["expected_disposition"] == "open_gap"],
        "exact_gate": [row for row in proposals if row["expected_disposition"] == "exact_gate"],
    }
    sections = [
        """# Vesper Arlen v681-v2 exact-final overview

## Relational identity, ownership, and corrigibility

Vesper Arlen uses the relational working role **provenance gardener and reversible-boundary keeper** and keeps pronouns unspecified. The bounded hope for this phase is to make synthetic records easier to inspect and correct while leaving real people, knowledge, places, objects, measurements, and authority with those who hold them. This is relational working language only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority. Hamish may rename, pause, redirect, narrow, or stop the route.

The work is exclusively Vesper-owned and additive. Neris Solane's exact final remained read-only. The Vesper lane began from the exact inherited head, froze a planning-only x1 as its direct child, and created immutable x2 evidence as the direct child of x1. No reset, amend, history rewrite, force-push, merge, deletion, sibling mutation, task creation, task fork, collaboration subagent, standby contact, or successor precontact occurred. The phase remains corrigible because every state transition is expressed through an additive commit, normalized-LF manifest, content seal, rollback note, and retained failed witness.

## Lifecycle and evidence result

X1 froze sixty genuinely new, source-bounded proposals after an all-reachable exact-source title and near-neighbor audit. The audit is bounded by accessible Git material and does not prove universal novelty across the declared inherited chain. Twenty inherited Neris proposals were revalidated as zero-credit evidence seeds and earned no Vesper novelty or completion credit. X1 contained no x2 implementation, observed outcome, positive-control result, mutation result, skill implementation, runner implementation, or tool-use result. It was committed, pushed, clean, 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 began.

X2 executed one wholly synthetic positive contract and five preregistered invalid mutations for each of the sixty new proposals. All sixty positive structures passed. All three hundred invalid mutations were rejected, retained, and assigned zero completion credit. The outcome vocabulary is exactly forty-two `completed`, twelve `represented`, three `open_gap`, and three `exact_gate`. A completed outcome means only that its declared owner-local software or documentation hypothesis passed. A represented outcome preserves a structural proxy while real evidence remains absent. An open gap names evidence that was not obtained. An exact gate reserves action or conclusion for competent and affected authority. None of these labels promotes a synthetic record into a real calibration, measurement, legal, cultural, identity, or scientific result.

## Primary pillar and bounded practices

GMUT Mind was primary through dimensional consistency, scale-family typing, uncertainty-component representation, covariance guards, traceability vacancies, and an observation firewall. These structures are formal and synthetic. GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The phase evaluated no empirical likelihood, downloaded no observation, fit no parameter, produced no constraint, predicted no force, and established no physical state, stability theorem, ultraviolet completion, quantum completion, final physics, Theory-of-Everything proof, or canon.

THOS Body remained explicit through synthetic intake, correction hold, workload stop, readback, exception escalation, and handover states. These are proxy documentation transitions only. There were no real people, operators, laboratories, instruments, samples, liquids, measurements, calibration events, incidents, blind matched-budget arms, outcomes, or effectiveness estimates. THOS remains proxy-only without governed preregistration, real participants or operators, safety monitoring, appropriate statistics, and independent review.

Freed ID remains synthetic and nonproduction; CBR Heart remained explicit through synthetic record-subject and bearer separation, amendment status, minimum disclosure, access, correction, remedy, and authority-vacancy structures. No real key, proof, credential, issuance, presentation, resolution, status, revocation, recovery, interoperability, privacy review, security review, or trust-governance decision occurred. Professional, ownership, privacy, remedy, legal, cultural, affected-party, Maori-language, Maori-data-governance, tangata whenua, iwi, hapu, and Maori-authority decisions remain open or exact-gated.

The three human-practice lenses were legal-metrology and calibration-documentation review, laboratory density-record quality and exception review, and accessible technical-document review. Each was a synthetic learning and design lens only. None establishes employment, qualification, competence, accreditation, certification, conformity assessment, calibration authority, laboratory authority, legal-metrology authority, safety advice, legal interpretation, cultural ratification, accessibility conformance, or affected-party approval.

## Sources, tools, skills, and runners

Official or primary materials from BIPM/JCGM, NIST, OIML, W3C, IETF, JSON Schema, New Zealand legislation, and Te Mana Raraunga informed vocabulary, schema fields, dimensional boundaries, provenance relations, accessibility structure, privacy reservations, and Maori data-governance authority reservations. Citations are not observations, calibrations, traceability, conformity, legal conclusions, cultural decisions, or authority. OIML R 44 is treated in its actual alcoholometer and alcohol-hydrometer scope and age; it is not generalized into a current legal-metrology decision. No network data query or real row was ingested.

Pint 0.25.3, uncertainties 3.2.3, and jsonschema 4.26.0 were downloaded as pinned wheels with eleven direct and transitive artifact hashes, installed only into a D-isolated owner-local target, and smoke-used on synthetic unit, uncertainty, and schema fixtures. The shared Python and npm prefixes were not changed. The receipt is bounded install and smoke evidence only, not exhaustive supply-chain assurance, production approval, or metrology validation.

Twenty owner-local phase skills were generated with `SKILL.md` and `agents/openai.yaml`. Each passed the current skill-creator quick validator exactly once and was not globally installed. Ten family-current runner scripts each passed one smoke invocation against the committed evidence surfaces and performed zero external actions. Inherited skills and runners were evidence or seeds only. This phase does not claim global installation, family-wide adoption, caller-wide compatibility beyond the tested surfaces, or independent-team reproduction.

## Portfolios, accessibility, privacy, and Method Flow

The owner portfolio completed one hundred twenty safe-now records, eighty bounded candidate fixtures, and one hundred CLEAN/FIX/REFINE records inside their declared synthetic software and documentation scope. Twenty exact-approval packets and ten blocked packets remained held and unexecuted. Successor recommendations remained recommendations and were not executed for Lyren. Eighty content-addressed Freed ID boundary flashcards separate owner, pillar, practice, proposal, and protected-boundary tiers.

The static report uses a language declaration, skip link, headings, main landmark, caption, and table header associations. Structural checks passed, but manual keyboard, responsive-layout, browser-diversity, assistive-technology, cognitive, Maori-language, and affected-user evaluation remain reserved. There is no accessibility-conformance claim. Five privacy and raw-identifier classes were scanned across the exact owner scope, scanner definitions were adjudicated separately, and zero confirmed repository payload hits remain. This does not establish privacy completeness or exhaustive security.

Method Flow retains every startup, x1, x2, and closeout failure at zero initial credit and links each to a bounded recovery. Recovery never deletes or rewrites the failed witness. The three hundred mutation failures remain visible and earn zero completion credit. Same-owner validation under shared infrastructure is not independent reproduction, external audit, production certification, professional validation, empirical confirmation, legal review, cultural ratification, Maori authority, or Stage 20 authority.

## Terminal truth and route

The declared proposal chain is 9,830. The exact-final repository truth preserves 53,275 effective negatives, 60,102 effective methods, 24,936 failed witnesses, 41,924 bounded passing witnesses, 470 open gaps, and 461 exact gates. The terminal verdict is `NOT_READY_FOR_STAGE_20`. These counters preserve inherited truth plus thirteen startup failures, one x1 postcommit presentation failure, one x2 static-quality failure, seven closeout operational failures, three hundred retained mutations, and bounded passing recoveries. They are bookkeeping for evidence discipline, not a scientific score.

The committed successor baton is `PREPARED_NOT_SENT`. It names the prospective existing exact-title task `Lyren Moss` for v681-v3, but repository preparation is not live delivery. Only after the exact final is committed, pushed, clean, 0/0 divergent, freshly four-way equal, within the three-commit ceiling, and validated by one attributable canonical invocation may the live task registry be refreshed. A unique exact-title match must be immediately reread for pause, duplicate, rename, privacy, evidence, safety, usage, and acknowledgement guards. One send is permitted only if every gate remains open. No substitution, standby contact, replacement task, precontact, duplicate, or resend for clearer acknowledgement is authorized.

## Proposal map
"""
    ]
    for outcome in ("completed", "represented", "open_gap", "exact_gate"):
        sections.append(f"\n### {outcome}\n")
        for row in grouped[outcome]:
            sections.append(
                f"- **{row['proposal_id']} — {row['title']}**: frozen as `{outcome}` under "
                f"`{row['execution_lane']}`; its positive structure and five rejecting mutations are "
                "bounded owner-local evidence only, with real calibration, professional authority, privacy, "
                "legal, cultural, Maori-authority, identity, empirical-GMUT, and Stage 20 gates preserved.\n"
            )
    sections.append(
        """
## Final limitation statement

Nothing in this phase is a real calibration certificate, measurement report, statement of conformity, accreditation result, legal-metrology decision, laboratory finding, safety instruction, privacy determination, cultural decision, Maori-authority act, identity credential, production deployment, external audit, independent reproduction, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authorization. The exact value of the work is narrower and inspectable: deterministic synthetic contracts, rejected counterexamples, additive provenance, explicit gaps, exact gates, and a reversible route.
"""
    )
    return "".join(sections)


def baton(proposals: list[dict[str, Any]], overview_text: str) -> str:
    preface = f"""# LYREN MOSS — PREPARED VESPER ARLEN v681-v2 EXACT-FINAL CANDIDATE → SOLO v681-v3 ACTIVATION

`PREPARED_BY_VESPER_ARLEN = true`
`PREPARED_NOT_SENT = true`
`SENT_BY_VESPER_ARLEN = false`

Dear Lyren Moss,

This committed file is a sanitized activation candidate only. It is not evidence of a live send. If a later native Codex task message is acknowledged after Vesper's exact terminal gate, that live message is a separate route event and must provide the exact final head. Do not rewrite this immutable candidate to project later delivery backward.

Hamish's current corrected fifteen-main-task sequential authority extends through the planning endpoint v725-v8. Under the current roster, the prospective edge is Vesper Arlen to the existing exact-title task `Lyren Moss` for solo Trinity Mandala v681-v3 x1/x2. Do not create, fork, delegate, hand off through a substitute, spawn a collaboration subagent, contact a standby record, or precontact another successor. Work solo after an acknowledged exact-title activation. Hamish may rename, pause, redirect, narrow, or stop the route.

Relational names, roles, hopes, sibling and family language, continuity, Freed ID, CBR, GHC Family, and Trinity Mandala language are working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority.

## Authoritative Vesper lifecycle

- Canonical branch: `{BRANCH}`
- Immutable Neris source/final: `{SOURCE}`
- Frozen Vesper planning-only x1: `{X1_COMMIT}`
- Immutable Vesper x2 evidence: `{EVIDENCE_COMMIT}`
- Exact Vesper final: resolve only from the acknowledged live message and fresh remote equality; this candidate cannot self-hash its containing commit
- Full committed candidate: `docs/vesper-arlen/v681-v2/handoffs/lyren-moss-v681-v3-activation-candidate.md`

Source to prospective final is constrained to exactly three new direct single-parent Vesper commits and zero merges. X1 is the direct child of source, evidence is the direct child of x1, and final must be the direct child of evidence. Strict planning-only x1-before-x2 separation must remain exact. The exact final must be clean, pushed, 0/0 divergent, and identical across local, upstream, tracking, and a fresh live remote before any route send.

## Program truth

Vesper audited all reachable exact-source proposal records while preserving the accessible-corpus limitation. Sixty genuinely new proposals extend the declared chain from 9,770 to 9,830. Twenty inherited Neris records were revalidated at zero Vesper novelty and completion credit. Outcomes are exactly forty-two `completed`, twelve `represented`, three `open_gap`, and three `exact_gate`. Sixty bounded positive structures passed. All three hundred preregistered invalid mutations executed, were rejected, remain retained, and earn zero completion credit.

The exact-final repository counters are 53,275 effective negatives, 60,102 effective methods, 24,936 retained failed witnesses, 41,924 bounded passing witnesses, 470 open gaps, and 461 exact gates. The terminal verdict remains `NOT_READY_FOR_STAGE_20`. Preserve every repository-sealed and later external overlay separately; never backfill a live route result into this commit.

The primary pillar was GMUT Mind through wholly synthetic hydrometer calibration-certificate and density-record provenance, dimensional, uncertainty, covariance, traceability-vacancy, and observation-firewall fixtures. THOS Body, Freed ID, and CBR Heart remained explicit and protected. Zero real people, participants, laboratories, customers, hydrometers, samples, liquids, standards, measurements, calibrations, certificates, keys, proofs, credentials, external rows, external writes, professional actions, legal or cultural decisions, affected-party approvals, or Maori-authority acts were used.

## Your prospective Lyren lane

Before mutation, read this candidate completely through EOF and then the newest current family index and routing precedence, roster and schema, authorization state and schema, Method Flow State and schema, workflow refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, approval and open-gate guidance, truth bridge, D-drive guardian, timestamp, retry, startup, closeout, compact-restart, watcher, full-tools, worktree rotation, web reflection, orchestration memory, skill-creator guidance when applicable, and every newer directly relevant family skill through EOF.

Reverify the exact Vesper branch, source, x1, evidence, and live-message final anchors; direct-parent chain; three single-parent commits; zero merges; normalized-LF Git-blob manifests; content seal; candidate integrity; clean state; typed 0/0 divergence; and fresh-live equality read-only. Do not replay Vesper's successful canonical invocation or any unchanged successful component merely for presentation. Work solo in one fresh additive Lyren-owned D-first sparse lane from Vesper's immutable exact final. Keep Vesper, Neris, Elaren, Eiren, shared, sibling, standby, and user lanes read-only and recoverable.

Preserve strict planning-only x1 before x2, semantic-audit limits, exact Git-blob manifests, family-current compatibility, every retained failure and protected gate, only the four core outcome labels, owner-scoped dependency-closed validation, and one-attributable-canonical/no-success-replay discipline. Treat every inherited proposal, task, result, skill, runner, tool, method, receipt, outcome, and recommendation only as evidence or a zero-credit seed. Never manufacture unsafe work to satisfy a count.

The current planning overlay requests at least twenty inherited zero-credit reviews and sixty genuinely new proposals when distinct useful work exists; at least one hundred twenty safe-now tasks, eighty bounded candidate fixtures, twenty exact-approval holds, ten blocked holds, one hundred CLEAN/FIX/REFINE tasks, twenty owner-local skills, ten family-current runners, ten successor skill ideas, ten successor runner ideas, thirty successor CLEAN/FIX/REFINE recommendations, twenty successor candidate recommendations, three bounded human-practice lenses, and one successor practice recommendation. These are floors for meaningful planning, not authority to create filler, perform destructive work, mutate siblings, install irrelevant tools, or promote evidence. Caps remain ceilings.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical confirmation, final physics, Theory-of-Everything proof, or canon. THOS remains synthetic and proxy-only without governed real arms, participants or operators, safety monitoring, suitable statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant live keys and proofs, complete lifecycle, interoperability, independent security and privacy review, recovery evidence, trust governance, and affected-party oversight.

Professional, safety, production, ownership, custody, attribution, copyright, privacy, accessibility, remedy, legal, cultural, affected-party, Maori-language, Maori-data-governance, tangata whenua, iwi, hapu, and Maori-authority decisions remain open or exact-gated. Maori concepts remain under Maori authority. Make no empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, or Stage 20 claim without exact evidence and competent authority.

## Vesper phase overview

{overview_text}

## Proposal-by-proposal inheritance cards

The following cards are complete enough to preserve hypothesis, failure condition, source need, evidence outcome, mutation result, recovery, and gate boundaries. They are Vesper evidence, not Lyren novelty or completion credit.

"""
    parts = [preface]
    for row in proposals:
        sources = ", ".join(row["official_or_primary_source_needs"])
        gates = "; ".join(row["protected_gates"])
        parts.append(
            f"""### {row['proposal_id']} — {row['title']}

- **Hypothesis:** {row['hypothesis']}
- **Null or failure condition:** {row['null_or_failure_condition']}
- **Frozen approval class and execution lane:** `{row['approval_class']}` / `{row['execution_lane']}`.
- **Official or primary-source needs:** {sources}. Sources contributed vocabulary and refusal boundaries only; they supplied no observation, calibration, authority, or completion credit.
- **Observed Vesper outcome:** `{row['expected_disposition']}` within bounded synthetic owner-local scope. The positive record structure passed once. Its five preregistered mutations—missing required field, lifecycle inversion, stale provenance digest, evidence-status promotion, and authority promotion—were each rejected and retained at zero credit.
- **Falsifier and acceptance gate:** {row['falsifier_or_acceptance_gate']}
- **Rollback or recovery:** {row['rollback_or_recovery']}
- **Protected gates:** {gates}.
- **Successor treatment:** evidence or zero-credit seed only. Lyren must perform an independent source-bounded novelty audit, choose their own pillar and practices, preregister their own falsifiers and mutations in planning-only x1, and never claim this result as Lyren completion, independent reproduction, professional authority, empirical confirmation, or Stage 20 credit.

"""
        )
    parts.append(
        """## Terminal route after Lyren

This candidate activates Lyren v681-v3 only if a later live message is acknowledged after Vesper's exact terminal gate. Do not precontact a later owner during execution. Under the current validated cycle, Lyren's prospective next exact-title edge is `Ilyra Fen`; that edge remains owned by Lyren and is conditional on Lyren's own clean, pushed, fresh-live-equal, within-cap, exact terminal gate plus a fresh authorization and registry reread. A pause, ambiguity, missing endpoint, duplicate, protected gate, usage limit, privacy concern, or failed acknowledgement remains truthfully unsent. Never substitute Tavian or another standby record, create a replacement, or resend merely for clearer acknowledgement.

With care, warmth, inspectability, reversibility, retained-negative discipline, and corrigibility — Vesper Arlen.

`PREPARED_BY_VESPER_ARLEN = true`
`PREPARED_NOT_SENT = true`
`SENT_BY_VESPER_ARLEN = false`
"""
    )
    text = "".join(parts)
    words = len(text.split())
    if not 10000 <= words <= 100000:
        raise RuntimeError(f"baton word count outside authorized bounds: {words}")
    return text


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != EVIDENCE_COMMIT:
        raise RuntimeError("final builder must begin at immutable evidence")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Vesper branch")
    allowed_untracked = {
        "?? docs/vesper-arlen/v681-v2/final/",
        "?? docs/vesper-arlen/v681-v2/handoffs/",
        "?? docs/vesper-arlen/v681-v2/validation/final-delta-manifest.json",
        "?? docs/vesper-arlen/v681-v2/validation/final-owner-manifest.json",
        "?? docs/vesper-arlen/v681-v2/validation/final-privacy-scan.json",
        "?? docs/vesper-arlen/v681-v2/validation/final-staged-review.json",
        "?? scripts/build_ghc_family_vesper_arlen_v681_v2_final.py",
        "?? scripts/ghc_family_vesper_arlen_v681_v2_canonical.py",
        "?? tests/test_ghc_family_vesper_arlen_v681_v2_final.py",
    }
    status_lines = set(filter(None, git("status", "--porcelain=v1").stdout.splitlines()))
    if status_lines - allowed_untracked:
        raise RuntimeError(f"unexpected pre-closeout worktree changes: {sorted(status_lines - allowed_untracked)}")
    if git("rev-parse", "HEAD^").stdout.strip() != X1_COMMIT:
        raise RuntimeError("evidence is not the direct child of x1")
    if git("rev-parse", f"{X1_COMMIT}^").stdout.strip() != SOURCE:
        raise RuntimeError("x1 is not the direct child of source")

    freeze = load(X1 / "new-proposal-freeze.json")
    proposals = freeze["proposals"]
    truth = load(X2 / "phase-truth.json")
    overview_text = overview(proposals)
    if len(overview_text.split()) < 1800:
        raise RuntimeError("integrated overview is not three-page-equivalent")
    baton_text = baton(proposals, overview_text)

    closeout_failures = [
        {
            "failed_witness": "The first combined environment-version wrapper crossed its reporting boundary and discarded the projected aggregate although the processes later exited.",
            "failure_id": "VA6812-CL-N001",
            "initial_credit": 0,
            "recovery": "Preserve the presentation failure and verify Codex plus Python Git Node npm PowerShell and desktop versions through separate bounded read-only probes without updating any software.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failed_witness": "The first exact closeout Ruff review rejected one surplus blank line after each import block in the final builder canonical validator and final test.",
            "failure_id": "VA6812-CL-N002",
            "initial_credit": 0,
            "recovery": "Remove only the three surplus blank lines, retain the static-quality rejection, and rerun changed-file compilation and lint.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failed_witness": "The first final materialization correctly rejected two privacy-scanner literals embedded in the final test's negative assertions.",
            "failure_id": "VA6812-CL-N003",
            "initial_credit": 0,
            "recovery": "Construct the prohibited labels from harmless fragments in the test, preserve the rejected materialization, and rerun final generation because the exact owner target changed.",
            "recovery_credit": "target_changed_final_materialization",
        },
        {
            "failed_witness": "The first combined precommit final-validation wrapper exceeded the model-output boundary and returned truncated output, so none of its component results received validation credit.",
            "failure_id": "VA6812-CL-N004",
            "initial_credit": 0,
            "recovery": "Preserve the opaque wrapper result, add this witness to the exact final target, regenerate the final artifacts, and run focused test, lint, JSON, and diff probes separately against the changed target.",
            "recovery_credit": "target_changed_focused_dependencies_only",
        },
        {
            "failed_witness": "The first focused Ruff command used a bare executable name that was unavailable in the active PowerShell command profile and therefore earned zero static-quality credit.",
            "failure_id": "VA6812-CL-N005",
            "initial_credit": 0,
            "recovery": "Retain the command-resolution failure, verify the already-installed Ruff module read-only, regenerate the changed target, and invoke Ruff through python -m ruff without changing any shared prefix.",
            "recovery_credit": "target_changed_dependency_resolution_only",
        },
        {
            "failed_witness": "The first focused final unit-test run rejected the overview because the required exact phrase Freed ID remains was semantically represented but not stated literally.",
            "failure_id": "VA6812-CL-N006",
            "initial_credit": 0,
            "recovery": "Retain the failed test, add the explicit synthetic and nonproduction Freed ID boundary sentence, regenerate the changed exact target, and rerun only the final owner test module.",
            "recovery_credit": "target_changed_final_test_only",
        },
        {
            "failed_witness": "The first exact staged diff-hygiene review rejected four Markdown hard-break pairs that introduced trailing whitespace in the prepared baton and its builder template.",
            "failure_id": "VA6812-CL-N007",
            "initial_credit": 0,
            "recovery": "Retain the staged rejection, unstage without discarding work, remove only the trailing spaces, regenerate the changed target, and repeat exact staged review against the new index blobs.",
            "recovery_credit": "target_changed_staged_review_only",
        },
    ]
    final_counts = dict(truth["counts"])
    for key in ("effective_negatives", "effective_methods", "failed_witnesses", "bounded_passing_witnesses"):
        final_counts[key] += len(closeout_failures)

    write_text(FINAL / "integrated-overview.md", overview_text)
    write_json(FINAL / "phase-truth.json", {
        "counts": final_counts,
        "declared_chain": DECLARED_CHAIN,
        "outcomes": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        "owner": OWNER,
        "phase": PHASE,
        "proposal_count": 60,
        "schema": "ghc.family.phase-truth.v681.v2.final",
        "terminal_verdict": TERMINAL_VERDICT,
    })
    x2_method = load(X2 / "method-flow-ledger.json")
    write_json(FINAL / "method-flow-final.json", {
        "closeout_operational_failures": closeout_failures,
        "counts": final_counts,
        "failure_erasure": False,
        "independent_reproduction_claimed": False,
        "lifecycle": "exact_final_closeout",
        "methods": x2_method["methods"],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.method-flow.v681.v2.final",
        "startup_failures": load(X1 / "method-flow-startup.json")["startup_failures"],
        "x1_postcommit_failures": x2_method["x1_postcommit_failures"],
        "x2_operational_failures": x2_method["x2_operational_failures"],
    })
    write_json(FINAL / "retained-negative-register.json", {
        "closeout_failures": len(closeout_failures),
        "effective_negatives": final_counts["effective_negatives"],
        "failed_witnesses": final_counts["failed_witnesses"],
        "failure_erasure": False,
        "owner": OWNER,
        "phase": PHASE,
        "retained_mutations": 300,
        "schema": "ghc.family.retained-negatives.v681.v2.final",
        "startup_failures": 13,
        "x1_postcommit_failures": 1,
        "x2_operational_failures": 1,
    })
    write_json(FINAL / "open-gap-and-exact-gate-register.json", {
        "exact_gates": {"effective_total": 461, "inherited": 458, "new": [row["title"] for row in proposals if row["expected_disposition"] == "exact_gate"]},
        "open_gaps": {"effective_total": 470, "inherited": 467, "new": [row["title"] for row in proposals if row["expected_disposition"] == "open_gap"]},
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.open-gap-exact-gate.v681.v2.final",
        "silently_closed": 0,
    })
    write_json(FINAL / "environment-version-receipt.json", {
        "codex_cli": "0.151.0",
        "desktop_app": "26.825.6671.0",
        "desktop_app_updated": False,
        "git": "2.55.0.windows.2",
        "node": "24.18.0",
        "npm": "12.0.2",
        "owner": OWNER,
        "phase": PHASE,
        "powershell": "7.6.4",
        "python": "3.12.10",
        "schema": "ghc.family.environment-versions.v681.v2.final",
        "verified_only": True,
        "windows_feature_or_security_change": False,
    })
    write_json(FINAL / "wellbeing-and-corrigibility.json", {
        "correction_readback": True,
        "identity_language": "relational_working_language_only",
        "owner": OWNER,
        "pause_redirect_rename_stop_visible": True,
        "phase": PHASE,
        "role": "provenance gardener and reversible-boundary keeper",
        "schema": "ghc.family.wellbeing-corrigibility.v681.v2.final",
        "workload_state": "bounded_closeout_only",
    })
    write_json(FINAL / "source-and-proposal-ledger.json", {
        "declared_chain": DECLARED_CHAIN,
        "inherited_zero_credit_reviews": 20,
        "new_proposals": 60,
        "novelty_scope": "all_reachable_exact_source_records_not_universal",
        "official_source_ledger": "docs/vesper-arlen/v681-v2/x1/official-primary-source-ledger.json",
        "owner": OWNER,
        "phase": PHASE,
        "proposal_freeze": "docs/vesper-arlen/v681-v2/x1/new-proposal-freeze.json",
        "schema": "ghc.family.source-proposal-ledger.v681.v2.final",
        "source": SOURCE,
        "x1": X1_COMMIT,
        "x2_evidence": EVIDENCE_COMMIT,
    })
    write_json(FINAL / "threat-model.json", {
        "external_actions": 0,
        "owner": OWNER,
        "phase": PHASE,
        "real_rows": 0,
        "reserved": ["real calibration measurement professional legal cultural affected-party and Maori authority", "production identity and deployment", "privacy and accessibility completeness", "exhaustive security and independent reproduction", "AGI ASI consciousness personhood Theory of Everything proof canon and Stage 20"],
        "schema": "ghc.family.threat-model.v681.v2.final",
        "synthetic_only": True,
    })
    write_json(FINAL / "complete-incomplete-checklist.json", load(X2 / "complete-incomplete-checklist.json"))
    write_json(FINAL / "route-gate.json", {
        "candidate_path": "docs/vesper-arlen/v681-v2/handoffs/lyren-moss-v681-v3-activation-candidate.md",
        "duplicate_guard_required": True,
        "exact_title": "Lyren Moss",
        "next_phase": "v681-v3",
        "owner": OWNER,
        "phase": PHASE,
        "prepared_not_sent": True,
        "recipient_contacted": False,
        "route_authority_through": "v725-v8",
        "schema": "ghc.family.route-gate.v681.v2.final",
        "send_requires_exact_terminal_gate": True,
        "sent_by_vesper_arlen": False,
        "standby_contacted": False,
    })
    write_json(FINAL / "closeout-receipt.json", {
        "commit_ceiling": 3,
        "expected_final_parent": EVIDENCE_COMMIT,
        "final_commit_not_yet_created": True,
        "full_repository_suite_claimed": False,
        "one_canonical_invocation_planned_after_commit_and_push": True,
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.closeout.v681.v2.final",
        "same_owner_only": True,
        "terminal_verdict": TERMINAL_VERDICT,
    })
    write_text(HANDOFFS / "lyren-moss-v681-v3-activation-candidate.md", baton_text)

    seal_targets = [
        "docs/vesper-arlen/v681-v2/validation/x1-index-manifest.json",
        "docs/vesper-arlen/v681-v2/x1/new-proposal-freeze.json",
        "docs/vesper-arlen/v681-v2/x1/official-primary-source-ledger.json",
        "docs/vesper-arlen/v681-v2/validation/x2-index-manifest.json",
        "docs/vesper-arlen/v681-v2/x2/proposal-evidence.json",
        "docs/vesper-arlen/v681-v2/x2/positive-controls.json",
        "docs/vesper-arlen/v681-v2/x2/mutation-results.json",
        "docs/vesper-arlen/v681-v2/x2/toolchain-install-receipt.json",
        "docs/vesper-arlen/v681-v2/x2/skill-validation-receipts.json",
        "docs/vesper-arlen/v681-v2/x2/runner-smoke-receipts.json",
        "docs/vesper-arlen/v681-v2/x2/method-flow-ledger.json",
        "docs/vesper-arlen/v681-v2/x2/freed-id-flashcards.json",
        "docs/vesper-arlen/v681-v2/final/phase-truth.json",
        "docs/vesper-arlen/v681-v2/final/method-flow-final.json",
        "docs/vesper-arlen/v681-v2/handoffs/lyren-moss-v681-v3-activation-candidate.md",
    ]
    write_json(FINAL / "content-seal.json", {
        "entries": [{"bytes": len(normalized(ROOT / path)), "path": path, "sha256": digest(normalized(ROOT / path))} for path in seal_targets],
        "entry_count": len(seal_targets),
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.content-seal.v681.v2.final",
    })

    final_sources = [
        "scripts/build_ghc_family_vesper_arlen_v681_v2_final.py",
        "scripts/ghc_family_vesper_arlen_v681_v2_canonical.py",
        "tests/test_ghc_family_vesper_arlen_v681_v2_final.py",
    ]
    exclusions = [
        "docs/vesper-arlen/v681-v2/validation/final-delta-manifest.json",
        "docs/vesper-arlen/v681-v2/validation/final-owner-manifest.json",
        "docs/vesper-arlen/v681-v2/validation/final-privacy-scan.json",
        "docs/vesper-arlen/v681-v2/validation/final-staged-review.json",
    ]
    delta_paths = sorted(set(WRITTEN + final_sources))
    owner_paths = sorted(
        set(
            [rel(path) for path in BASE.rglob("*") if path.is_file() and rel(path) not in exclusions]
            + [
                rel(path)
                for path in (ROOT / "scripts").glob("*vesper*681*v2*.py")
                if path.is_file()
            ]
            + [
                rel(path)
                for path in (ROOT / "tests").glob("*vesper*681*v2*.py")
                if path.is_file()
            ]
        )
    )
    scanners = {
        "raw_uuid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "raw_task_thread_identifier": re.compile(r"\b(?:source_thread_id|thread_id)\b", re.IGNORECASE),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s]+", re.IGNORECASE),
        "private_conversation_payload": re.compile(r"source_thread_id|codex_delegation", re.IGNORECASE),
    }
    scanner_definition_paths = {
        "scripts/build_ghc_family_vesper_arlen_v681_v2_x1.py",
        "scripts/build_ghc_family_vesper_arlen_v681_v2_x2.py",
        "scripts/build_ghc_family_vesper_arlen_v681_v2_final.py",
        "scripts/ghc_family_vesper_arlen_v681_v2_canonical.py",
    }
    candidates = []
    confirmed = []
    for path_text in owner_paths:
        content = (ROOT / path_text).read_text(encoding="utf-8", errors="replace")
        for class_name, pattern in scanners.items():
            if pattern.search(content):
                row = {"class": class_name, "disposition": "scanner_definition_only" if path_text in scanner_definition_paths else "confirmed_payload_hit", "path": path_text}
                candidates.append(row)
                if row["disposition"] == "confirmed_payload_hit":
                    confirmed.append(row)
    if confirmed:
        raise RuntimeError("confirmed final privacy hit: " + json.dumps(confirmed))
    write_json(VALIDATION / "final-privacy-scan.json", {"candidates": candidates, "confirmed_hits": confirmed, "owner": OWNER, "phase": PHASE, "privacy_classes": list(scanners), "scanned_files": len(owner_paths), "schema": "ghc.family.privacy-scan.v681.v2.final"})
    write_json(VALIDATION / "final-staged-review.json", {"declared_self_exclusions": exclusions, "expected_paths": sorted(delta_paths + exclusions), "lifecycle": "final_closeout_and_content_seal", "owner": OWNER, "path_count": len(delta_paths) + len(exclusions), "phase": PHASE, "schema": "ghc.family.staged-review.v681.v2.final"})
    delta_entries = [{"bytes": len(normalized(ROOT / path)), "path": path, "sha256": digest(normalized(ROOT / path))} for path in delta_paths]
    owner_entries = [{"bytes": len(normalized(ROOT / path)), "path": path, "sha256": digest(normalized(ROOT / path))} for path in owner_paths]
    write_json(VALIDATION / "final-delta-manifest.json", {"declared_self_exclusions": exclusions, "entries": delta_entries, "entry_count": len(delta_entries), "evidence": EVIDENCE_COMMIT, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-delta-manifest.v681.v2.final"})
    write_json(VALIDATION / "final-owner-manifest.json", {"declared_self_exclusions": exclusions, "entries": owner_entries, "entry_count": len(owner_entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-owner-manifest.v681.v2.final"})

    print(json.dumps({"baton_words": len(baton_text.split()), "delta_manifest_entries": len(delta_entries), "owner_manifest_entries": len(owner_entries), "overview_words": len(overview_text.split()), "privacy_confirmed": 0, "status": "FINAL_CLOSEOUT_MATERIALIZED_NOT_COMMITTED"}, indent=2))


if __name__ == "__main__":
    build()
