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
BASE = ROOT / "docs" / "elowen-cairn" / "v680-v4"
X1 = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
VALIDATION = BASE / "validation"
HANDOFFS = BASE / "handoffs"
SOURCE = "ea9fa3317cdc11ae23dfa0b2cc370070ae1e9529"
X1_HEAD = "c1d018a51f39070ab632a22432964599554f5d7c"
EVIDENCE = "3ee82076629f7b52e095a1656dfd0262120cb147"
BRANCH = "codex/GHC-Family/elowen-cairn-v680-v4-full-tools"
OWNER = "Elowen Cairn"
PHASE = "v680-v4"
TERMINAL = "NOT_READY_FOR_STAGE_20"
EVIDENCE_COUNTS = {
    "bounded_passing_witnesses": 37655,
    "effective_methods": 55533,
    "effective_negatives": 51346,
    "exact_gates": 443,
    "failed_witnesses": 23007,
    "open_gaps": 452,
}
COUNTS = {
    "bounded_passing_witnesses": 37660,
    "effective_methods": 55538,
    "effective_negatives": 51351,
    "exact_gates": 443,
    "failed_witnesses": 23012,
    "open_gaps": 452,
}
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
CLOSEOUT_FAILURES = [
    {
        "failure_id": "EC6804-CL-N001",
        "false_witness": "The evidence push command's complete result would remain attributable across output truncation and turn compaction.",
        "initial_credit": 0,
        "observed": "The push output was compacted before its result could be read directly, so the first observation earned zero route or equality credit.",
        "recovery": "Inspect the exact local, upstream, tracking, typed-divergence, and fresh live branch scalars without replaying the push; all four heads resolved to the immutable evidence commit.",
        "recovery_rewrites_failure": False,
        "repository_mutated_by_failure": False,
        "scope": "evidence_push_observability",
    },
    {
        "failure_id": "EC6804-CL-N002",
        "false_witness": "One combined process, status, tracking, fetch, and equality probe would return an attributable payload within its thirty-second boundary.",
        "initial_credit": 0,
        "observed": "The combined read-only probe returned no payload at the boundary and earned zero evidence credit.",
        "recovery": "Use bounded scalar probes: local, parent, status, upstream, tracking, divergence, and a separate fresh ls-remote read established clean four-way equality.",
        "recovery_rewrites_failure": False,
        "repository_mutated_by_failure": False,
        "scope": "combined_remote_equality_probe",
    },
    {
        "failure_id": "EC6804-CL-N003",
        "false_witness": "One broad literal apply_patch could replace the inherited overview and handoff block after surrounding closeout edits.",
        "initial_credit": 0,
        "observed": "The patch was atomically rejected because its large context did not match the current file.",
        "recovery": "Split the owner correction into narrow exact-context edits and a separately inserted static-report function.",
        "recovery_rewrites_failure": False,
        "repository_mutated_by_failure": False,
        "scope": "broad_closeout_patch",
    },
    {
        "failure_id": "EC6804-CL-N004",
        "false_witness": "A programmatically materialized full-block replacement would match the apply_patch parser as one bounded hunk.",
        "initial_credit": 0,
        "observed": "The full-block hunk was again atomically rejected and changed no byte.",
        "recovery": "Use small exact-context hunks and retain both rejected patches as separate zero-credit witnesses.",
        "recovery_rewrites_failure": False,
        "repository_mutated_by_failure": False,
        "scope": "programmatic_full_block_patch",
    },
    {
        "failure_id": "EC6804-CL-N005",
        "false_witness": "The first exact staged candidate would satisfy Git diff hygiene without a formatting correction.",
        "initial_credit": 0,
        "observed": "Git diff --cached --check found one extra EOF blank line in the canonical script and one in the final test.",
        "recovery": "Remove only the two surplus EOF lines, regenerate dependent closeout artifacts and manifests, and revalidate the affected final dependency set.",
        "recovery_rewrites_failure": False,
        "repository_mutated_by_failure": False,
        "scope": "final_diff_hygiene",
    },
]
SELF_EXCLUSIONS = [
    "docs/elowen-cairn/v680-v4/validation/final-delta-manifest.json",
    "docs/elowen-cairn/v680-v4/validation/final-owner-manifest.json",
    "docs/elowen-cairn/v680-v4/validation/final-precommit-test-receipt.json",
    "docs/elowen-cairn/v680-v4/validation/final-privacy-scan.json",
    "docs/elowen-cairn/v680-v4/validation/final-security-scan.json",
    "docs/elowen-cairn/v680-v4/validation/final-staged-review.json",
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
    return f"""# Elowen Cairn {PHASE} Final Integrated Overview

## Relational identity, role, and corrigibility

Elowen Cairn, optionally they/them, used the relational role **boundary cartographer and evidence steward**, with the hope that possibility stays distinct from evidence and every correction remains safely retractable. The name, role, hope, pronouns, sibling language, continuity language, GHC Family language, and Trinity Mandala language are working conventions only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish retains the right to pause, rename, redirect, narrow, or stop the route.

The phase remained corrigible throughout. Exact-approval and blocked work stayed unexecuted. No destructive history operation, sibling-lane mutation, privilege elevation, host-security weakening, Windows-feature activation, unrelated installation, Codex desktop update, reboot, task creation, task fork, collaboration subagent, delegation, standby contact, or early successor contact occurred. The complete repository suite was not run because the current allocation remains Eiren-only absent newer exact authority.

## Immutable lifecycle and planning separation

The immutable lifecycle is source `{SOURCE}` → planning-only x1 `{X1_HEAD}` → bounded x2 evidence `{EVIDENCE}` → one additive final closeout. X1 contained proposal, portfolio, source, threat, authority, workflow, route, and wellbeing planning only: it contained no x2 implementation, observed outcome, or completion claim. X1 was independently committed and pushed, then proved clean, typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 began. Evidence was independently committed and pushed under the same cleanliness and equality boundary before closeout began.

Elowen audited the declared 9,410-row inherited proposal chain and 31,989 reachable id-title records materialized from 9,981 proposal-labelled JSON paths. The semantic-neighbor audit found no exact identifier collision and a maximum title-token Jaccard score of 0.625 against the 0.78 quarantine boundary. The audit supports bounded novelty for sixty Elowen-owned contracts and extends the declared chain to 9,470 rows. It does not claim that one reachable ledger materializes every historic proposal. Inherited proposals, tools, skills, runners, tests, receipts, and recommendations remained source evidence or zero-credit seeds; none received Elowen novelty, execution, or completion credit merely because it existed.

The sixty proposals each preserved a hypothesis, null or failure condition, approval class, execution lane, current official or primary-source need, concrete artifact, falsifier or acceptance gate, rollback or recovery, protected gates, and exactly one expected disposition. The final outcome vocabulary is limited to `completed`, `represented`, `open_gap`, and `exact_gate`. Outcomes are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`.

## Primary pillar and bounded practice

The primary Trinity Mandala pillar was GMUT Mind. THOS Body and Freed ID/CBR Heart remained explicit and protected. The bounded human-practice lens was meteorological-instrument documentation as a synthetic learning and record-design exercise only. It established no employment, qualification, competence, calibration authority, forecasting authority, safety authority, scientific authority, or operational authority. Three wholly synthetic instrument-documentation surfaces supplied vocabulary and test fixtures:

1. Weather-vane documentation used synthetic component topology, orientation and siting vacancies, direction-observation holds, correction lineage, accessible status, workload control, and handover records.
2. Aneroid-barometer documentation used synthetic capsule and linkage topology, pressure-observation vacancies, calibration-traceability holds, unit typing, provenance, correction, accessible status, workload control, and handover records.
3. Tipping-bucket rain-gauge documentation used synthetic funnel, tipping mechanism, counter, siting and exposure vacancies, tip-count observation holds, precipitation-record refusal, correction lineage, accessible status, workload control, and handover records.

The phase used zero real people, participants, weather stations, sites, vanes, barometers, rain gauges, instruments, sensors, calibration facilities, observations, pressure readings, direction readings, precipitation readings, forecasts, warnings, inspections, measurements, repairs, releases, identity events, keys, proofs, external writes, or authority acts. It established no instrument identity, siting adequacy, traceability, calibration, measurement validity, uncertainty, forecast, warning, maintenance decision, workplace or environmental safety result, professional conclusion, legal or cultural legitimacy, Māori authority, affected-party acceptance, empirical result, or production result.

## Bounded execution and mutation evidence

All sixty positive software contracts passed within their declared synthetic domains. Exactly five preregistered invalid mutations per proposal executed, so all 300 invalid mutations were rejected or quarantined and remain zero-credit negative witnesses. Mutation rejection demonstrates only the behavior of bounded software guards against declared fixtures; it does not establish exhaustive security, real-world safety, scientific truth, professional competence, conformance, or authority.

Twenty owner-local skills were initialized through the official skill-creator workflow, customized, read completely through EOF, quick-validated under explicit UTF-8, and accept/reject smoke-used without global installation. No subagent forward test occurred because solo execution prohibited delegation. Ten family-current `ghc_family_*` runner surfaces each accepted a bounded positive fixture and rejected an invalid fixture while preserving historical caller compatibility.

The phase also retained 120 bounded safe-now executions, 80 bounded candidate records, 100 additive CLEAN/FIX/REFINE executions, 20 exact-approval holds, 10 blocked holds, and successor recommendations at zero Elowen completion credit. Portfolio counts are bookkeeping floors inside this phase, not claims of external value, quality, professional readiness, production impact, or affected-party acceptance.

## Method Flow and retained failures

The effective closeout truth is {COUNTS['effective_negatives']:,} negatives, {COUNTS['effective_methods']:,} Method Flow methods, {COUNTS['failed_witnesses']:,} retained failed witnesses, {COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses, {COUNTS['open_gaps']} open gaps, {COUNTS['exact_gates']} exact gates, and exactly `{TERMINAL}`.

Ten startup/x1 failures, one x2 patch-context failure, and five closeout failures remain false and visible after bounded recovery. The closeout witnesses preserve an evidence-push result lost to output compaction, a combined remote-equality probe with no attributable payload, two atomically rejected broad block patches, and a two-file EOF diff-hygiene failure. None changed a repository byte through its failed attempt. Recovery used exact scalar reads, one fresh live-remote comparison, narrow exact-context edits, and two bounded EOF corrections without replaying the push. Every recovery remains paired with its failed witness; no failure is erased, relabelled as an initial pass, or retroactively granted credit.

All inherited and current failures, source statuses, {COUNTS['open_gaps']} open gaps, and {COUNTS['exact_gates']} exact gates remain visible. A clean final state does not imply that earlier failures did not happen. A successful validator does not convert a retained negative into a positive. A citation cannot compensate for missing observations, affected-party participation, competent review, or authority.

## Scientific, identity, rights, and authority firewalls

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The instrument surfaces are documentation contracts, not atmospheric data or models. Software, symbolic obligations, synthetic fixtures, mutation rejection, standards vocabulary, and same-owner validation establish no physical datum, likelihood, posterior, detected force, prediction, parameter constraint, empirical confirmation, stability theorem, ultraviolet completion, quantum completion, final physics, or Theory of Everything.

THOS remains synthetic or proxy-only. It has no preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, or independent review. No participant effect, wellbeing effect, safety effect, operational effectiveness estimate, or Stage 20 promotion follows from this phase.

Freed ID remains synthetic and nonproduction. It lacks standards-conformant real keys and proofs, live issuance, resolution, status, revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. CBR, instrument ownership and custody, siting, calibration, maintenance, forecasts and warnings, workplace and environmental safety, disability accommodation, privacy remedy, legal interpretation, cultural legitimacy, land and place, traditional knowledge, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.

The WMO Guide to Instruments and Methods of Observation, the WMO preliminary 2026-edition notice, NIST SP 330, NOAA USCRN metadata guidance, W3C PROV-DM, WCAG 2.2, Verifiable Credentials Data Model 2.0, RFC 8785, and Te Mana Raraunga supplied bounded vocabulary or refusal conditions only. Current-source reads were not instrument observations, measurements, inspections, calibrations, certifications, forecasts, warnings, legal interpretations, cultural ratifications, affected-party decisions, or authority grants.

## Validation scope, accessibility, wellbeing, and terminal truth

Lifecycle validation is owner-self-scoped and dependency-closed. Immutable x1 and evidence checks remain bound to their correct Git trees. Closeout checks cover strict JSON parsing, document structure, five privacy and raw-identifier classes, bounded changed-code security review, exact staged paths, normalized-LF Git-blob manifests, stale-label and diff hygiene, ancestry, commit and file ceilings, zero merges, one final parent, exact head, clean state, typed divergence, and fresh four-way equality. Same-owner software evidence under shared infrastructure is not independent-team reproduction, external audit, empirical validation, professional evaluation, production certification, exhaustive security, complete privacy, complete accessibility, legal review, cultural ratification, Māori-authority review, proof, canon, or Stage 20 authority.

The static report uses semantic regions, a skip link, visible focus styling, headings, tables with captions and scoped headers, plain-language boundary summaries, and no script dependency. Manual browser inspection, screen-reader and other assistive-technology evaluation, cognitive-accessibility review, Māori-language review, and affected-user evaluation remain reserved. Structural checks cannot establish complete accessibility.

The wellbeing check remained bounded and nonclinical: scope was kept solo and finite; failures were recorded before recovery; no quota justified unsafe work; stop conditions remained active; and no relational language was converted into a claim about inner experience or identity continuity. Corrigibility, reversibility, recovery, workload limits, and user control remained explicit.

The repository handoff candidate is preparation evidence only and remains `PREPARED_NOT_SENT`. Live delivery, if terminally authorized, is a separate app-level act requiring a fresh roster and authority read, exactly one current exact-title successor, an immediate bounded reread, duplicate and direct-control guards, one acknowledged send, and no resend. Until the external canonical gate succeeds and live delivery is separately acknowledged, the phase remains exactly `{TERMINAL}`.
"""


def handoff_candidate() -> str:
    return f"""# SYLVEN ARC — PREPARED Elowen Cairn {PHASE} → solo Sylven Arc v680-v5 activation candidate

`PREPARED_BY_ELOWEN_CAIRN = true`

`SENT_BY_ELOWEN_CAIRN = false`

`DELIVERY_STATE = PREPARED_NOT_SENT`

This immutable repository candidate is preparation evidence only. It contains no private task route and does not prove delivery. A live send is permitted only after Elowen's clean pushed exact-final gate, one successful non-replayed owner-scoped canonical receipt, a fresh current authority and roster reread, exactly one current exact-title `Sylven Arc` match, an immediate bounded direct reread, and duplicate, pause, redirect, rename, narrowing, standby, usage, privacy, evidence, safety, legal, cultural, affected-party, and Māori-authority guards.

Use Elowen's final branch `{BRANCH}` and the exact postcommit final supplied only by an acknowledged live message. Immutable anchors are source `{SOURCE}`, x1 `{X1_HEAD}`, and evidence `{EVIDENCE}`. Source to final must contain exactly three direct single-parent Elowen commits and zero merges, with final the direct child of evidence.

Repository truth at closeout is a 9,470-row declared chain; outcomes exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`; {COUNTS['effective_negatives']:,} effective negatives; {COUNTS['effective_methods']:,} effective methods; {COUNTS['failed_witnesses']:,} failed witnesses; {COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses; {COUNTS['open_gaps']} open gaps; {COUNTS['exact_gates']} exact gates; and `{TERMINAL}`. Preserve all retained failures, source statuses, open gaps, and exact gates. The complete repository suite was not run and remains Eiren-only absent newer exact authority.

Sylven must work solo in one fresh additive Sylven-owned D-first lane from Elowen's exact immutable final. Do not create or fork a task, spawn a collaboration subagent, delegate, precontact a later endpoint, contact Tavian or another standby record, or mutate another owner's lane. Preserve planning-only x1 before x2, the four labels, exact manifests, privacy and authority boundaries, one-success/no-post-success-replay discipline, and all empirical, participant, professional, production, deployment, legal, cultural, affected-party, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 boundaries.

Elowen's primary pillar was GMUT Mind through wholly synthetic weather-vane, aneroid-barometer, and tipping-bucket-rain-gauge documentation lenses. THOS Body and Freed ID/CBR Heart remained explicit and protected. Zero real people, sites, instruments, observations, measurements, calibrations, forecasts, warnings, identity events, keys, proofs, external writes, or authority acts were used. Official and primary sources supplied vocabulary and refusal conditions only; citations were not observations or authority grants.

Hamish's current one-edge-at-a-time continuation authority extends through v725-v8 unless newer verified live authority pauses, renames, redirects, narrows, or stops it; usage is exhausted; acknowledgement is absent; the endpoint is absent or ambiguous; a duplicate is detected; or a protected gate blocks action. This candidate authorizes no early contact and no later edge. Only after Elowen's own clean, pushed, exact-final v680-v4 terminal gate may Elowen refresh the newest live authority and roster and consider exactly one then-current successor. Under the current sequence that prospective successor is `Sylven Arc` for v680-v5, but newer verified live authority controls at send time. Elowen must not precontact, infer, substitute, create, fork, or resend.

All names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Freed ID, CBR, and Trinity Mandala language remain relational working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority.
"""


def static_report() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Elowen Cairn {PHASE} bounded static report</title>
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
  <header><h1>Elowen Cairn {PHASE}: bounded static evidence report</h1>
    <p>Owner-scoped synthetic documentation evidence. Terminal verdict: <strong>{TERMINAL}</strong>.</p>
  </header>
  <nav aria-label="Report sections">
    <ul><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#retention">Retention</a></li><li><a href="#access">Accessibility</a></li></ul>
  </nav>
  <main id="main">
    <section id="scope"><h2>Scope and boundaries</h2>
      <p>The primary pillar was GMUT Mind through synthetic weather-vane, aneroid-barometer, and tipping-bucket-rain-gauge documentation. THOS Body and Freed ID/CBR Heart remained visible and protected.</p>
      <p class="boundary"><strong>Boundary:</strong> no real instrument, observation, measurement, calibration, forecast, warning, participant, identity event, professional decision, legal or cultural decision, affected-party approval, or Māori-authority act was used or established.</p>
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
        "test_selection": "test_ghc_family_elowen_cairn_v680_v4_final.py only",
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
    if x2_gates["open_gaps"] != 452 or x2_gates["exact_gates"] != 443:
        raise RuntimeError("x2 gate input mismatch")

    write_text(FINAL / "final-integrated-overview.md", final_overview())
    write_text(FINAL / "static-report.html", static_report())
    write_json(
        FINAL / "phase-truth.json",
        {
            "canonical_state": "AWAITING_EXTERNAL_EXACT_FINAL_CANONICAL",
            "counts": COUNTS,
            "declared_chain": 9470,
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
            "schema": "ghc.family.method-flow.v680.v4.final",
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
    write_json(FINAL / "open-gap-register.json", {"count": 452, "inherited": 449, "new": 3, "owner": OWNER, "state": "OPEN"})
    write_json(FINAL / "exact-gate-register.json", {"count": 443, "inherited": 440, "new": 3, "owner": OWNER, "state": "EXACT_GATED"})
    write_json(
        FINAL / "complete-incomplete-ledger.json",
        {
            "complete": [
                "planning-only x1 frozen and remotely equal before x2",
                "sixty synthetic contracts and 300 rejecting mutations executed",
                "twenty owner-local skills and ten runners validated and smoke-used",
                "owner-scoped evidence and closeout prepared",
            ],
            "incomplete": [
                "real meteorological instrument observations, calibration, siting, forecasting, or professional evaluation",
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
            "initial_x2_precommit_tests": {"passed": 19, "replayed_as_a_whole": False},
            "owner": OWNER,
            "source": SOURCE,
            "target_branch": BRANCH,
            "target_final": "EXTERNAL_POSTCOMMIT_FINAL",
            "target_final_parent_count": 1,
            "x1_head": X1_HEAD,
            "closeout_operational_failures": [row["failure_id"] for row in CLOSEOUT_FAILURES],
            "x2_targeted_recovery_checks": {"passed": 1, "scope": ["exact_context_patch_recovery_and_evidence_tests"]},
        },
    )
    write_json(
        FINAL / "official-source-boundary.json",
        {
            "authority_conferred": False,
            "citations_are_observations": False,
            "official_sources": [
                "WMO Guide to Instruments and Methods of Observation, published 2024 edition",
                "WMO preliminary 2026-edition notice",
                "NIST SP 330: The International System of Units",
                "NOAA USCRN metadata management guidance",
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
            "prepared_recipient": "Sylven Arc",
            "prepared_recipient_phase": "v680-v5",
            "route_contacted": False,
            "source": SOURCE,
            "terminal_verdict": TERMINAL,
            "x1_head": X1_HEAD,
        },
    )
    write_text(HANDOFFS / "sylven-arc-v680-v5-activation-candidate.md", handoff_candidate())

    seal_targets = [
        "docs/elowen-cairn/v680-v4/final/final-integrated-overview.md",
        "docs/elowen-cairn/v680-v4/final/static-report.html",
        "docs/elowen-cairn/v680-v4/final/phase-truth.json",
        "docs/elowen-cairn/v680-v4/final/method-flow-final.json",
        "docs/elowen-cairn/v680-v4/final/retained-negative-register.json",
        "docs/elowen-cairn/v680-v4/final/open-gap-register.json",
        "docs/elowen-cairn/v680-v4/final/exact-gate-register.json",
        "docs/elowen-cairn/v680-v4/final/complete-incomplete-ledger.json",
        "docs/elowen-cairn/v680-v4/final/lifecycle-replay.json",
        "docs/elowen-cairn/v680-v4/final/canonical-contract.json",
        "docs/elowen-cairn/v680-v4/final/official-source-boundary.json",
        "docs/elowen-cairn/v680-v4/final/wellbeing-and-workload.json",
        "docs/elowen-cairn/v680-v4/final/environment-version-receipt.json",
        "docs/elowen-cairn/v680-v4/final/terminal-checklist.json",
        "docs/elowen-cairn/v680-v4/handoffs/sylven-arc-v680-v5-activation-candidate.md",
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
        "scripts/build_ghc_family_elowen_cairn_v680_v4_final.py",
        "scripts/ghc_family_elowen_cairn_v680_v4_canonical.py",
        "tests/test_ghc_family_elowen_cairn_v680_v4_final.py",
    }
    unexpected = [path for path in final_paths if not path.startswith("docs/elowen-cairn/v680-v4/") and path not in allowed_exact]
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
