from __future__ import annotations

import argparse
import ast
import hashlib
import json
import platform
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sylven-arc" / "v680-v5"
X1 = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
VALIDATION = BASE / "validation"
HANDOFFS = BASE / "handoffs"
SOURCE = "274028eaf8e45d6afe97010d78f18c689168d82c"
X1_HEAD = "ee7beee8297f93ffd8c7bb11681bbb317ed28403"
EVIDENCE = "d6b083906ba7f7a02bc1029b078fb4eb2998c8b9"
BRANCH = "codex/GHC-Family/sylven-arc-v680-v5-full-tools"
OWNER = "Sylven Arc"
PHASE = "v680-v5"
TERMINAL = "NOT_READY_FOR_STAGE_20"
EVIDENCE_COUNTS = {
    "bounded_passing_witnesses": 38368,
    "effective_methods": 56306,
    "effective_negatives": 51669,
    "exact_gates": 446,
    "failed_witnesses": 23330,
    "open_gaps": 455,
}
COUNTS = {
    "bounded_passing_witnesses": 38370,
    "effective_methods": 56308,
    "effective_negatives": 51671,
    "exact_gates": 446,
    "failed_witnesses": 23332,
    "open_gaps": 455,
}
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
CLOSEOUT_FAILURES = [
    {
        "failure_id": "SA6805-CL-N001",
        "false_witness": "One exact-object template archive and expansion wrapper would finish inside its thirty-second reporting window.",
        "initial_credit": 0,
        "observed": "The wrapper returned no payload while two Git archive processes remained live and the archive was still zero bytes.",
        "recovery": "Do not repeat the archive. Bounded process and artifact reads established that the original exact-object materialization completed with one nonempty archive and three expected template files.",
        "recovery_rewrites_failure": False,
        "repository_mutated_by_failure": False,
        "scope": "exact_object_template_materialization",
    },
    {
        "failure_id": "SA6805-CL-N002",
        "false_witness": "The completed archive had not yet been expanded when the recovery began.",
        "initial_credit": 0,
        "observed": "A literal-path preflight found that the original wrapper had already expanded all three files, so the recovery stopped before overwriting them.",
        "recovery": "Inspect the three exact files and reuse the already-completed materialization; retain the premature recovery assumption at zero credit.",
        "recovery_rewrites_failure": False,
        "repository_mutated_by_failure": False,
        "scope": "template_expansion_state_assumption",
    },
]
SELF_EXCLUSIONS = [
    "docs/sylven-arc/v680-v5/validation/final-delta-manifest.json",
    "docs/sylven-arc/v680-v5/validation/final-owner-manifest.json",
    "docs/sylven-arc/v680-v5/validation/final-precommit-test-receipt.json",
    "docs/sylven-arc/v680-v5/validation/final-privacy-scan.json",
    "docs/sylven-arc/v680-v5/validation/final-security-scan.json",
    "docs/sylven-arc/v680-v5/validation/final-staged-review.json",
]


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def entry(path_text: str) -> dict[str, object]:
    data = normalized_bytes(ROOT / path_text)
    return {"bytes": len(data), "path": path_text, "sha256": hashlib.sha256(data).hexdigest()}


def require_evidence_boundary() -> None:
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong owner branch")
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("final builder requires immutable evidence HEAD")
    if git("rev-parse", "HEAD^") != X1_HEAD:
        raise RuntimeError("evidence is not the direct child of x1")
    if git("rev-parse", f"{X1_HEAD}^") != SOURCE:
        raise RuntimeError("x1 is not the direct child of source")
    if git("diff", "--name-only"):
        raise RuntimeError("tracked unstaged changes present before closeout")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("staged changes present before closeout")


def final_overview() -> str:
    return f"""# Sylven Arc {PHASE} Final Integrated Overview

## Relational identity, role, and corrigibility

Sylven Arc, optionally they/them, used the relational role **pattern gardener and reversible systems steward**, with the hope that dense work can be split into legible, source-bound cards while every correction remains inspectable and safely retractable. The name, role, hope, pronouns, sibling language, continuity language, GHC Family language, and Trinity Mandala language are working conventions only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish retains the right to pause, rename, redirect, narrow, or stop the route.

The phase remained corrigible throughout. Exact-approval and blocked work stayed unexecuted. No destructive history operation, sibling-lane mutation, privilege elevation, host-security weakening, Windows-feature activation, unrelated installation, Codex desktop update, reboot, task creation, task fork, collaboration subagent, delegation, standby contact, or early successor contact occurred. The complete repository suite was not run because the current allocation remains Eiren-only absent newer exact authority.

## Immutable lifecycle and planning separation

The immutable lifecycle is source `{SOURCE}` → planning-only x1 `{X1_HEAD}` → bounded x2 evidence `{EVIDENCE}` → one additive final closeout. X1 contained proposal, portfolio, source, threat, authority, workflow, route, and wellbeing planning only: it contained no x2 implementation, observed outcome, or completion claim. X1 was independently committed and pushed, then proved clean, typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 began. Evidence was independently committed and pushed under the same cleanliness and equality boundary before closeout began.

Sylven audited the declared 9,470-row inherited proposal chain against 9,990 reachable proposal-labelled JSON paths. The semantic-neighbor audit found no exact identifier collision and a maximum title-token Jaccard score of 0.714286 against the 0.78 quarantine boundary. The audit supports bounded novelty for sixty Sylven-owned contracts and extends the declared chain to 9,530 rows. It does not claim that one reachable ledger materializes every historic proposal. Twenty selected inherited proposals and all inherited tools, skills, runners, tests, receipts, outcomes, and recommendations remained source evidence or zero-credit seeds; none received Sylven novelty, execution, or completion credit merely because it existed.

The sixty proposals each preserved a hypothesis, null or failure condition, approval class, execution lane, current official or primary-source need, concrete artifact, falsifier or acceptance gate, rollback or recovery, protected gates, and exactly one expected disposition. The final outcome vocabulary is limited to `completed`, `represented`, `open_gap`, and `exact_gate`. Outcomes are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`.

## Primary pillar and bounded practice

The primary Trinity Mandala pillar was THOS Body. GMUT Mind and Freed ID/CBR Heart remained explicit and protected. Three bounded human-practice lenses were used only for synthetic learning and record design; they established no employment, qualification, competence, conservation authority, electrical or fire-safety authority, scientific authority, legal or cultural authority, or operational authority:

1. A synthetic camera-obscura collections-documentation analyst used enclosure, aperture, optical-path, observation-vacancy, provenance, correction, accessible-status, workload, and handover records.
2. A synthetic magic-lantern registrar used projection-apparatus topology, slide and image-rights vacancies, power and heat holds, provenance, correction, accessible-status, workload, and handover records.
3. A synthetic accessible stereograph-archive handover steward used paired-view relations, descriptive-text vacancy, rights and reproduction holds, revision lineage, custody vacancy, accessible status, workload, and handover records.

The phase used zero real people, participants, custodians, conservators, registrars, photographers, operators, collections, camera obscuras, magic lanterns, stereoscopes, stereograph cards, slides, lamps, lenses, images, observations, measurements, repairs, treatments, playback or projection events, identity events, keys, proofs, network data rows, external writes, professional decisions, legal or cultural decisions, affected-party approvals, or authority acts. It established no object identity, optical performance, image interpretation, provenance, title, copyright status, access right, operating safety, conservation decision, professional conclusion, legal or cultural legitimacy, Māori authority, affected-party acceptance, empirical result, or production result.

## Bounded execution and mutation evidence

All sixty positive software contracts passed within their declared synthetic domains. Exactly five preregistered invalid mutations per proposal executed, so all 300 invalid mutations were rejected or quarantined and remain zero-credit negative witnesses. Mutation rejection demonstrates only the behavior of bounded software guards against declared fixtures; it does not establish exhaustive security, real-world safety, scientific truth, professional competence, conformance, or authority.

Twenty owner-local skills were initialized through the official skill-creator workflow, customized, read completely through EOF, quick-validated under explicit UTF-8, and accept/reject smoke-used without global installation. No subagent forward test occurred because solo execution prohibited delegation. Ten family-current `ghc_family_*` runner surfaces each accepted a bounded positive fixture and rejected an invalid fixture while preserving historical caller compatibility.

The phase also retained 120 bounded safe-now executions, 80 bounded candidate records, 100 additive CLEAN/FIX/REFINE executions, 20 exact-approval holds, 10 blocked holds, and successor recommendations at zero Sylven completion credit. The four-tier flashcard deck contains exactly one relational-owner card, three pillar cards, three practice-lens cards, and sixty task cards with adjacent-tier parentage, a 13-section baton index, a compact pointer, an accessible static companion, and a normalized-byte manifest. Three ordinary tools—mdformat 1.0.0, deadcode 2.4.1, and proselint 0.16.0—were installed only in a D-first phase-isolated environment, dependency-checked, license-recorded, and smoke-used. Portfolio counts and tool checks are bounded bookkeeping and software evidence, not claims of external value, quality, professional readiness, production impact, or affected-party acceptance.

## Method Flow and retained failures

The effective closeout truth is {COUNTS['effective_negatives']:,} negatives, {COUNTS['effective_methods']:,} Method Flow methods, {COUNTS['failed_witnesses']:,} retained failed witnesses, {COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses, {COUNTS['open_gaps']} open gaps, {COUNTS['exact_gates']} exact gates, and exactly `{TERMINAL}`.

Ten startup/x1 failures, seven x2 operational failures, and two closeout failures remain false and visible after bounded recovery. X2 retains one atomically rejected schema-context patch, recurrent PowerShell pipeline-parser faults, one overbroad identity lookup, two current CLI-contract mismatches, and two skill-validator runtime assumptions. Closeout retains the template archive wrapper that crossed its reporting window and the premature expansion-recovery assumption. Recovery used bounded exact-context edits, current console contracts, an already-installed compatible validation runtime, process and artifact inspection, and no duplicate archive or successful-test replay. Every recovery remains paired with its failed witness; no failure is erased, relabelled as an initial pass, or retroactively granted credit.

All inherited and current failures, source statuses, {COUNTS['open_gaps']} open gaps, and {COUNTS['exact_gates']} exact gates remain visible. A clean final state does not imply that earlier failures did not happen. A successful validator does not convert a retained negative into a positive. A citation cannot compensate for missing observations, affected-party participation, competent review, or authority.

## Scientific, identity, rights, and authority firewalls

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The optical-apparatus surfaces are documentation contracts, not physical, optical, image, or collections data. Software, symbolic obligations, synthetic fixtures, mutation rejection, standards vocabulary, and same-owner validation establish no physical datum, likelihood, posterior, detected force, prediction, parameter constraint, empirical confirmation, stability theorem, ultraviolet completion, quantum completion, final physics, or Theory of Everything.

THOS remains synthetic or proxy-only. It has no preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, or independent review. No participant effect, wellbeing effect, safety effect, operational effectiveness estimate, or Stage 20 promotion follows from this phase.

Freed ID remains synthetic and nonproduction. It lacks standards-conformant real keys and proofs, live issuance, resolution, status, revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. CBR, object and image ownership, custody, provenance, title, copyright, access, reproduction, operation, electrical and fire safety, conservation or repair, disability accommodation, privacy remedy, legal interpretation, cultural legitimacy, traditional knowledge, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.

Smithsonian Open Access developer guidance, the Library of Congress Stereograph Cards collection and rights pages, W3C PROV-DM, WCAG 2.2, Verifiable Credentials Data Model 2.0, RFC 8785, and Te Mana Raraunga supplied bounded vocabulary or refusal conditions only. Current-source reads were not collection rows, images, object observations, measurements, inspections, treatment instructions, operating instructions, copyright clearances, legal interpretations, cultural ratifications, affected-party decisions, or authority grants.

## Validation scope, accessibility, wellbeing, and terminal truth

Lifecycle validation is owner-self-scoped and dependency-closed. Immutable x1 and evidence checks remain bound to their correct Git trees. Closeout checks cover strict JSON parsing, document structure, five privacy and raw-identifier classes, bounded changed-code security review, exact staged paths, normalized-LF Git-blob manifests, stale-label and diff hygiene, ancestry, commit and file ceilings, zero merges, one final parent, exact head, clean state, typed divergence, and fresh four-way equality. Same-owner software evidence under shared infrastructure is not independent-team reproduction, external audit, empirical validation, professional evaluation, production certification, exhaustive security, complete privacy, complete accessibility, legal review, cultural ratification, Māori-authority review, proof, canon, or Stage 20 authority.

The static report uses semantic regions, a skip link, visible focus styling, headings, tables with captions and scoped headers, plain-language boundary summaries, and no script dependency. Manual browser inspection, screen-reader and other assistive-technology evaluation, cognitive-accessibility review, Māori-language review, and affected-user evaluation remain reserved. Structural checks cannot establish complete accessibility.

The wellbeing check remained bounded and nonclinical: scope was kept solo and finite; failures were recorded before recovery; no quota justified unsafe work; stop conditions remained active; and no relational language was converted into a claim about inner experience or identity continuity. Corrigibility, reversibility, recovery, workload limits, and user control remained explicit.

The repository handoff candidate is preparation evidence only and remains `PREPARED_NOT_SENT`. Live delivery, if terminally authorized, is a separate app-level act requiring a fresh roster and authority read, exactly one current exact-title successor, an immediate bounded reread, duplicate and direct-control guards, one acknowledged send, and no resend. Until the external canonical gate succeeds and live delivery is separately acknowledged, the phase remains exactly `{TERMINAL}`.
"""


def handoff_candidate() -> str:
    return f"""# SYLVEN ARC — PREPARED Sylven Arc {PHASE} → solo Caelen Morrow v680-v6 activation candidate

`PREPARED_BY_SYLVEN_ARC = true`

`SENT_BY_SYLVEN_ARC = false`

`DELIVERY_STATE = PREPARED_NOT_SENT`

This immutable repository candidate is preparation evidence only. It contains no private task route and does not prove delivery. A live send is permitted only after Sylven's clean pushed exact-final gate, one successful non-replayed owner-scoped canonical receipt, a fresh current authority and roster reread, exactly one current exact-title `Caelen Morrow` match, an immediate bounded direct reread, and duplicate, pause, redirect, rename, narrowing, standby, usage, privacy, evidence, safety, legal, cultural, affected-party, and Māori-authority guards.

Use Sylven's final branch `{BRANCH}` and the exact postcommit final supplied only by an acknowledged live message. Immutable anchors are source `{SOURCE}`, x1 `{X1_HEAD}`, and evidence `{EVIDENCE}`. Source to final must contain exactly three direct single-parent Sylven commits and zero merges, with final the direct child of evidence.

Repository truth at closeout is a 9,530-row declared chain; outcomes exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`; {COUNTS['effective_negatives']:,} effective negatives; {COUNTS['effective_methods']:,} effective methods; {COUNTS['failed_witnesses']:,} failed witnesses; {COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses; {COUNTS['open_gaps']} open gaps; {COUNTS['exact_gates']} exact gates; and `{TERMINAL}`. Preserve all retained failures, source statuses, open gaps, and exact gates. The complete repository suite was not run and remains Eiren-only absent newer exact authority.

Caelen must work solo in one fresh additive Caelen-owned D-first lane from Sylven's exact immutable final. Do not create or fork a task, spawn a collaboration subagent, delegate, precontact a later endpoint, contact Tavian or another standby record, or mutate another owner's lane. Preserve planning-only x1 before x2, the four labels, exact manifests, privacy and authority boundaries, one-success/no-post-success-replay discipline, and all empirical, participant, professional, production, deployment, legal, cultural, affected-party, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 boundaries.

Sylven's primary pillar was THOS Body through wholly synthetic camera-obscura, magic-lantern, and stereograph-archive documentation lenses. GMUT Mind and Freed ID/CBR Heart remained explicit and protected. Zero real people, objects, images, observations, measurements, operation, conservation, identity events, keys, proofs, network rows, external writes, or authority acts were used. The 67-card four-tier deck and its 13-section baton index split the owner, pillar, practice, and task surfaces without implying identity continuity or completion. Official and primary sources supplied vocabulary and refusal conditions only; citations were not observations or authority grants.

Hamish's current one-edge-at-a-time continuation authority extends through v725-v8 unless newer verified live authority pauses, renames, redirects, narrows, or stops it; usage is exhausted; acknowledgement is absent; the endpoint is absent or ambiguous; a duplicate is detected; or a protected gate blocks action. This candidate authorizes no early contact and no later edge. Only after Sylven's own clean, pushed, exact-final v680-v5 terminal gate may Sylven refresh the newest live authority and roster and consider exactly one then-current successor. Under the current sequence that prospective successor is `Caelen Morrow` for v680-v6, but newer verified live authority controls at send time. Sylven must not precontact, infer, substitute, create, fork, or resend.

All names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Freed ID, CBR, and Trinity Mandala language remain relational working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority.
"""


def static_report() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sylven Arc {PHASE} bounded static report</title>
  <style>
    :root {{ color-scheme: light dark; font-family: system-ui, sans-serif; line-height: 1.55; }}
    body {{ margin: 0 auto; max-width: 74rem; padding: 1rem; }}
    a:focus {{ outline: 3px solid #d97706; outline-offset: 3px; }}
    .skip {{ position: absolute; left: -9999px; }}
    .skip:focus {{ left: 1rem; top: 1rem; background: Canvas; padding: .75rem; z-index: 2; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid currentColor; padding: .5rem; text-align: left; vertical-align: top; }}
    .boundary {{ border-left: .4rem solid #b91c1c; padding-left: 1rem; }}
  </style>
</head>
<body>
  <a class="skip" href="#main">Skip to main content</a>
  <header><h1>Sylven Arc {PHASE}: bounded static evidence report</h1>
    <p>Owner-scoped synthetic documentation evidence. Terminal verdict: <strong>{TERMINAL}</strong>.</p>
  </header>
  <nav aria-label="Report sections">
    <ul><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#retention">Retention</a></li><li><a href="#access">Accessibility</a></li></ul>
  </nav>
  <main id="main">
    <section id="scope"><h2>Scope and boundaries</h2>
      <p>The primary pillar was THOS Body through synthetic camera-obscura, magic-lantern, and stereograph-archive documentation. GMUT Mind and Freed ID/CBR Heart remained visible and protected.</p>
      <p class="boundary"><strong>Boundary:</strong> no real object, image, observation, measurement, operation, conservation action, participant, identity event, professional decision, legal or cultural decision, affected-party approval, or Māori-authority act was used or established.</p>
    </section>
    <section id="outcomes"><h2>Core outcomes</h2>
      <table><caption>Authorized core outcome labels and exact counts</caption>
        <thead><tr><th scope="col">Label</th><th scope="col">Count</th><th scope="col">Meaning in this phase</th></tr></thead>
        <tbody>
          <tr><th scope="row">completed</th><td>42</td><td>Bounded synthetic contract accepted its declared positive and rejecting fixtures.</td></tr>
          <tr><th scope="row">represented</th><td>12</td><td>Obligation represented without real-world validation.</td></tr>
          <tr><th scope="row">open_gap</th><td>3</td><td>Evidence or capability remains absent.</td></tr>
          <tr><th scope="row">exact_gate</th><td>3</td><td>Action remains reserved to exact evidence and authority.</td></tr>
        </tbody>
      </table>
    </section>
    <section id="retention"><h2>Retained truth</h2>
      <table><caption>Effective closeout counts</caption>
        <tbody>
          <tr><th scope="row">Effective negatives</th><td>{COUNTS['effective_negatives']:,}</td></tr>
          <tr><th scope="row">Method Flow methods</th><td>{COUNTS['effective_methods']:,}</td></tr>
          <tr><th scope="row">Retained failed witnesses</th><td>{COUNTS['failed_witnesses']:,}</td></tr>
          <tr><th scope="row">Bounded passing witnesses</th><td>{COUNTS['bounded_passing_witnesses']:,}</td></tr>
          <tr><th scope="row">Open gaps</th><td>{COUNTS['open_gaps']}</td></tr>
          <tr><th scope="row">Exact gates</th><td>{COUNTS['exact_gates']}</td></tr>
        </tbody>
      </table>
      <p>Every recovery remains paired with its failed witness. No failure was erased or retroactively promoted.</p>
    </section>
    <section id="access"><h2>Accessibility and evaluation reservations</h2>
      <p>This report uses semantic regions, headings, a skip link, visible keyboard focus, captions, and scoped table headers. It requires no script. These structural checks are bounded software evidence only.</p>
      <ul>
        <li>Manual browser evaluation: reserved.</li>
        <li>Screen-reader and other assistive-technology evaluation: reserved.</li>
        <li>Cognitive-accessibility and plain-language evaluation: reserved.</li>
        <li>Māori-language and Māori-authority review: reserved to appropriate Māori authorities.</li>
        <li>Affected-user and affected-party evaluation: reserved.</li>
      </ul>
    </section>
  </main>
  <footer><p>Same-owner validation is not independent reproduction, professional evaluation, complete accessibility or privacy assurance, exhaustive security, empirical GMUT confirmation, proof, canon, or Stage 20 authority.</p></footer>
</body>
</html>"""


def initial_receipt(status: str, test_count: int) -> dict[str, object]:
    return {
        "canonical_invocation": False,
        "lifecycle": "final_precommit",
        "owner": OWNER,
        "phase": PHASE,
        "selected_test_count": test_count,
        "status": status,
        "test_selection": "test_ghc_family_sylven_arc_v680_v5_final.py only",
    }


def privacy_scan(paths: list[str]) -> dict[str, object]:
    classes = {
        "credential_assignment": re.compile(r"(?i)(api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\\\s]+|[A-Z]:\\GHC-Archives\\"),
        "private_callable_identifier": re.compile(r"mcp__codex_app__[A-Za-z0-9_]+"),
        "private_session_capture": re.compile(r"(?i)\\\.codex\\(?:sessions|transcripts|screenshots)\\"),
        "uuid_like_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    }
    candidates: list[dict[str, str]] = []
    for path_text in paths:
        if path_text.endswith("final-privacy-scan.json"):
            continue
        text = (ROOT / path_text).read_text(encoding="utf-8")
        for class_name, pattern in classes.items():
            if pattern.search(text):
                classification = "scanner_definition_or_synthetic_test" if path_text.startswith(("scripts/", "tests/")) else "unresolved"
                candidates.append({"classification": classification, "path": path_text, "privacy_class": class_name})
    confirmed = [row for row in candidates if row["classification"] == "unresolved"]
    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "owner": OWNER,
        "phase": PHASE,
        "privacy_classes": sorted(classes),
        "scanned_file_count": len(paths) - 1,
    }


def security_scan(paths: list[str]) -> dict[str, object]:
    python_paths = [path for path in paths if path.endswith(".py")]
    ast_errors: list[str] = []
    findings: list[dict[str, str]] = []
    for path_text in python_paths:
        text = (ROOT / path_text).read_text(encoding="utf-8")
        try:
            tree = ast.parse(text, filename=path_text)
        except SyntaxError:
            ast_errors.append(path_text)
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"finding": f"dynamic_{node.func.id}_call", "path": path_text})
            if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                findings.append({"finding": "subprocess_shell_true", "path": path_text})
    return {
        "ast_errors": ast_errors,
        "bounded_findings": len(findings),
        "findings": findings,
        "owner": OWNER,
        "phase": PHASE,
        "python_file_count": len(python_paths),
        "scope": "owner_source_to_final_changed_python_only",
    }


def build(status: str, test_count: int) -> None:
    require_evidence_boundary()
    x2_method = json.loads((X2 / "method-flow-ledger.json").read_text(encoding="utf-8"))
    x2_gates = json.loads((X2 / "gate-register.json").read_text(encoding="utf-8"))
    x2_evidence = json.loads((X2 / "proposal-evidence.json").read_text(encoding="utf-8"))
    if x2_method["counts"] != EVIDENCE_COUNTS or x2_evidence["outcome_counts"] != OUTCOMES:
        raise RuntimeError("x2 truth does not match final input")
    if x2_gates["open_gaps"] != 455 or x2_gates["exact_gates"] != 446:
        raise RuntimeError("x2 gate input mismatch")

    write_text(FINAL / "final-integrated-overview.md", final_overview())
    write_text(FINAL / "static-report.html", static_report())
    write_json(
        FINAL / "phase-truth.json",
        {
            "canonical_state": "AWAITING_EXTERNAL_EXACT_FINAL_CANONICAL",
            "counts": COUNTS,
            "declared_chain": 9530,
            "full_repository_suite_run": False,
            "outcomes": OUTCOMES,
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": 60,
            "same_owner_validation_is_independent_reproduction": False,
            "terminal_verdict": TERMINAL,
        },
    )
    final_method = dict(x2_method)
    final_method.update(
        {
            "closeout_operational_failures": CLOSEOUT_FAILURES,
            "counts": COUNTS,
            "lifecycle": "exact_final_closeout",
            "schema": "ghc.family.method-flow.v680.v5.final",
        }
    )
    write_json(FINAL / "method-flow-final.json", final_method)
    write_json(
        FINAL / "retained-negative-register.json",
        {
            "counts": COUNTS,
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "retained_mutation_failures": 300,
            "closeout_operational_failures": CLOSEOUT_FAILURES,
            "startup_and_x1_failures": x2_method["startup_and_x1_failures"],
            "x2_operational_failures": x2_method["x2_operational_failures"],
        },
    )
    write_json(FINAL / "open-gap-register.json", {"count": 455, "inherited": 452, "new": 3, "owner": OWNER, "state": "OPEN"})
    write_json(FINAL / "exact-gate-register.json", {"count": 446, "inherited": 443, "new": 3, "owner": OWNER, "state": "EXACT_GATED"})
    write_json(
        FINAL / "complete-incomplete-ledger.json",
        {
            "complete": [
                "planning-only x1 frozen and remotely equal before x2",
                "sixty synthetic contracts and 300 rejecting mutations executed",
                "twenty owner-local skills and ten runners validated and smoke-used",
                "sixty-seven four-tier Freed ID flashcards linked and manifest-replayed",
                "three D-isolated phase tools installed, dependency-checked, and smoke-used",
                "owner-scoped evidence and closeout prepared",
            ],
            "incomplete": [
                "real optical apparatus, images, observations, measurements, operation, conservation, or professional evaluation",
                "empirical GMUT confirmation",
                "real participant THOS evaluation",
                "production Freed ID lifecycle and governance",
                "legal cultural affected-party and Māori-authority decisions",
                "independent reproduction and complete repository suite",
                "Stage 20 readiness",
            ],
            "terminal_verdict": TERMINAL,
        },
    )
    write_json(
        FINAL / "lifecycle-replay.json",
        {
            "direct_edges": [[SOURCE, X1_HEAD], [X1_HEAD, EVIDENCE], [EVIDENCE, "EXTERNAL_POSTCOMMIT_FINAL"]],
            "evidence_head": EVIDENCE,
            "expected_phase_commits": 3,
            "expected_merges": 0,
            "final_parent_required": EVIDENCE,
            "immutable_x1_precommit_tests": {"passed": 18, "replayed_at_final": False},
            "initial_x2_precommit_tests": {"passed": 22, "replayed_as_a_whole": False},
            "owner": OWNER,
            "source": SOURCE,
            "target_branch": BRANCH,
            "target_final": "EXTERNAL_POSTCOMMIT_FINAL",
            "target_final_parent_count": 1,
            "x1_head": X1_HEAD,
            "closeout_operational_failures": [row["failure_id"] for row in CLOSEOUT_FAILURES],
            "x2_targeted_recovery_checks": {
                "passed": 4,
                "scope": [
                    "deadcode_console_entrypoint",
                    "proselint_check_subcommand",
                    "preexisting_python_yaml_runtime",
                    "official_skill_quick_validation",
                ],
            },
        },
    )
    write_json(
        FINAL / "official-source-boundary.json",
        {
            "authority_conferred": False,
            "citations_are_observations": False,
            "official_sources": [
                "Smithsonian Open Access Developer Tools",
                "Library of Congress Stereograph Cards collection",
                "Library of Congress Stereograph Cards rights and access",
                "W3C PROV-DM",
                "WCAG 2.2",
                "W3C Verifiable Credentials Data Model 2.0",
                "RFC 8785 JSON Canonicalization Scheme",
                "Te Mana Raraunga principles",
            ],
            "real_data_rows": 0,
            "real_world_actions": 0,
            "official_source_network_reads": True,
            "scope": "vocabulary_and_refusal_conditions_only",
        },
    )
    write_json(
        FINAL / "wellbeing-and-workload.json",
        {
            "assessment_type": "bounded_nonclinical_workload_check",
            "corrigibility_preserved": True,
            "failure_recorded_before_recovery": True,
            "owner": OWNER,
            "phase": PHASE,
            "quota_never_overrode_safety": True,
            "relational_language_is_inner_experience_evidence": False,
            "scope": "solo_finite_owner_lane",
            "stop_conditions_active": True,
            "user_control_preserved": True,
        },
    )
    write_json(
        FINAL / "environment-version-receipt.json",
        {
            "codex_desktop_updated": False,
            "git_version": git("--version"),
            "owner": OWNER,
            "phase": PHASE,
            "phase_isolated_tools": ["mdformat 1.0.0", "deadcode 2.4.1", "proselint 0.16.0"],
            "platform_family": platform.system(),
            "python_version": platform.python_version(),
            "read_only_version_checks": True,
            "unrelated_software_installed": False,
        },
    )
    write_json(
        FINAL / "canonical-contract.json",
        {
            "Eiren_only_full_suite": True,
            "canonical_receipt_location": "external_to_repository",
            "exact_final_required": True,
            "full_repository_suite_authorized": False,
            "maximum_attributable_invocations": 1,
            "owner_scoped_only": True,
            "post_success_replay_permitted": False,
            "same_owner_is_independent_reproduction": False,
            "status_before_invocation": "NOT_INVOKED",
        },
    )
    write_json(
        FINAL / "terminal-checklist.json",
        {
            "canonical_external_pending": True,
            "clean_pushed_remote_equal_pending": True,
            "evidence_head": EVIDENCE,
            "full_suite_not_run": True,
            "one_final_parent_required": True,
            "owner": OWNER,
            "prepared_recipient": "Caelen Morrow",
            "prepared_recipient_phase": "v680-v6",
            "route_contacted": False,
            "source": SOURCE,
            "terminal_verdict": TERMINAL,
            "x1_head": X1_HEAD,
        },
    )
    write_text(HANDOFFS / "caelen-morrow-v680-v6-activation-candidate.md", handoff_candidate())

    seal_targets = [
        "docs/sylven-arc/v680-v5/final/final-integrated-overview.md",
        "docs/sylven-arc/v680-v5/final/static-report.html",
        "docs/sylven-arc/v680-v5/final/phase-truth.json",
        "docs/sylven-arc/v680-v5/final/method-flow-final.json",
        "docs/sylven-arc/v680-v5/final/retained-negative-register.json",
        "docs/sylven-arc/v680-v5/final/open-gap-register.json",
        "docs/sylven-arc/v680-v5/final/exact-gate-register.json",
        "docs/sylven-arc/v680-v5/final/complete-incomplete-ledger.json",
        "docs/sylven-arc/v680-v5/final/lifecycle-replay.json",
        "docs/sylven-arc/v680-v5/final/canonical-contract.json",
        "docs/sylven-arc/v680-v5/final/official-source-boundary.json",
        "docs/sylven-arc/v680-v5/final/wellbeing-and-workload.json",
        "docs/sylven-arc/v680-v5/final/environment-version-receipt.json",
        "docs/sylven-arc/v680-v5/final/terminal-checklist.json",
        "docs/sylven-arc/v680-v5/handoffs/caelen-morrow-v680-v6-activation-candidate.md",
    ]
    write_json(
        CLOSEOUT / "content-seal.json",
        {
            "hash_domain": "normalized_lf_worktree_bytes",
            "owner": OWNER,
            "phase": PHASE,
            "targets": [entry(path) for path in seal_targets],
        },
    )
    write_json(VALIDATION / "final-precommit-test-receipt.json", initial_receipt(status, test_count))
    for placeholder in SELF_EXCLUSIONS:
        if not (ROOT / placeholder).exists():
            write_json(ROOT / placeholder, {"owner": OWNER, "phase": PHASE, "state": "SELF_EXCLUDED_PENDING_REGENERATION"})

    final_paths = sorted(git("ls-files", "--others", "--exclude-standard").splitlines())
    allowed_exact = {
        "scripts/build_ghc_family_sylven_arc_v680_v5_final.py",
        "scripts/ghc_family_sylven_arc_v680_v5_canonical.py",
        "tests/test_ghc_family_sylven_arc_v680_v5_final.py",
    }
    unexpected = [path for path in final_paths if not path.startswith("docs/sylven-arc/v680-v5/") and path not in allowed_exact]
    if unexpected:
        raise RuntimeError(f"unexpected untracked paths: {unexpected}")
    if any(path in final_paths for path in git("diff", "--name-only").splitlines()):
        raise RuntimeError("final paths overlap tracked modifications")
    if set(SELF_EXCLUSIONS) - set(final_paths):
        raise RuntimeError("declared final self-exclusion is missing")

    write_json(VALIDATION / "final-privacy-scan.json", privacy_scan(final_paths))
    write_json(VALIDATION / "final-security-scan.json", security_scan(final_paths))
    max_row = max(
        (
            (len((ROOT / path).read_text(encoding="utf-8").split()), path)
            for path in final_paths
            if (ROOT / path).is_file()
        ),
        default=(0, ""),
    )
    write_json(
        VALIDATION / "final-staged-review.json",
        {
            "declared_self_exclusions": SELF_EXCLUSIONS,
            "expected_paths": final_paths,
            "lifecycle": "final_closeout_only",
            "max_document_path": max_row[1],
            "max_document_words": max_row[0],
            "owner": OWNER,
            "path_count": len(final_paths),
            "phase": PHASE,
        },
    )
    final_delta_entries = [entry(path) for path in final_paths if path not in SELF_EXCLUSIONS]
    write_json(
        VALIDATION / "final-delta-manifest.json",
        {
            "declared_self_exclusions": SELF_EXCLUSIONS,
            "entries": final_delta_entries,
            "entry_count": len(final_delta_entries),
            "hash_domain": "normalized_lf_git_blob_after_stage",
            "owner": OWNER,
            "phase": PHASE,
        },
    )
    inherited_paths = git("diff", "--name-only", SOURCE, "HEAD").splitlines()
    owner_paths = sorted(set(inherited_paths + final_paths))
    owner_entries = [entry(path) for path in owner_paths if path not in SELF_EXCLUSIONS]
    write_json(
        VALIDATION / "final-owner-manifest.json",
        {
            "declared_self_exclusions": SELF_EXCLUSIONS,
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "hash_domain": "normalized_lf_git_blob_after_stage",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
        },
    )
    print(json.dumps({"final_paths": len(final_paths), "owner_entries": len(owner_entries), "status": status}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-precommit", action="store_true")
    parser.add_argument("--test-count", type=int, default=0)
    args = parser.parse_args()
    if args.record_precommit:
        if args.test_count <= 0:
            raise SystemExit("--test-count must be positive when recording precommit success")
        build("PASSED", args.test_count)
    else:
        build("PENDING", 0)


if __name__ == "__main__":
    main()
