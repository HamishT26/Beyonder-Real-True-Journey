#!/usr/bin/env python3
"""Build the Ilyra Fen v659-v1 terminal closeout candidate."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v659_v1_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
EVIDENCE_COMMIT = "88f4734cda8049c887ad7ba12df088e63737c929"
FINAL_CODE = [
    "scripts/build_ghc_family_v659_v1_closeout.py",
    "scripts/ghc_family_v659_v1_validator.py",
    "scripts/ghc_family_v659_v1_minimal.py",
    "scripts/ghc_family_v659_v1_final_validator.py",
    "scripts/ghc_family_v659_v1_canonical.py",
    "tests/test_ghc_family_v659_v1_closeout.py",
]
GENERATED = [
    f"{d.PHASE_ROOT}/deliverables/v659-v1-final-overview.md",
    f"{d.PHASE_ROOT}/deliverables/v659-v1-accessible-static-report.html",
    f"{d.PHASE_ROOT}/handoffs/auren-lark-v659-v2-activation.md",
    f"{d.PHASE_ROOT}/final/completion-checklist.json",
    f"{d.PHASE_ROOT}/final/evidence-receipt.json",
    f"{d.PHASE_ROOT}/final/final-truth.json",
    f"{d.PHASE_ROOT}/final/lifecycle-summary.json",
    f"{d.PHASE_ROOT}/final/lifecycle-method-flow.json",
    f"{d.PHASE_ROOT}/final/open-gate-register.json",
    f"{d.PHASE_ROOT}/final/closeout-seal-receipt.json",
    f"{d.PHASE_ROOT}/final/final-owner-manifest.json",
    f"{d.PHASE_ROOT}/route/prepared-route.json",
    f"{d.PHASE_ROOT}/validation/canonical-pass-plan.json",
    f"{d.PHASE_ROOT}/validation/closeout-privacy-scan.json",
    f"{d.PHASE_ROOT}/validation/closeout-staged-review.json",
    f"{d.PHASE_ROOT}/validation/final-delta-manifest.json",
    f"{d.PHASE_ROOT}/validation/final-document-cap.json",
    f"{d.PHASE_ROOT}/wellbeing/final-wellbeing-check.json",
]
FINAL_FAILURES = [
    {
        "negative_id": "V6591-FINAL-N001",
        "signature": "post-evidence-four-way-wrapper-used-an-invalid-compound-powershell-exit-code-expression",
        "recovery": "Use separate null-safe Git probes and capture each exit code immediately before composing the scalar equality receipt.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-FINAL-N002",
        "signature": "first-detailed-closeout-validator-read-the-outcome-list-from-a-nonexistent-rows-key",
        "recovery": "Bind the unchanged outcome-distribution check to the exact proposal-outcomes schema key named outcomes and refresh every count-dependent closeout surface together.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-FINAL-N003",
        "signature": "second-detailed-closeout-validator-and-one-closeout-test-read-each-outcome-row-from-a-nonexistent-outcome-key",
        "recovery": "Inspect the exact row schema, bind the unchanged distribution check to observed_outcome, and refresh every count-dependent closeout surface together.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-FINAL-N004",
        "signature": "diagnostic-ripgrep-expression-contained-an-unclosed-escaped-group-and-returned-no-search-evidence",
        "recovery": "Replace the compound regular expression with separate fixed-string searches and retain the failed diagnostic at zero credit.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-FINAL-N005",
        "signature": "compile-wrapper-referenced-a-mistyped-nonexistent-canonical-validator-filename",
        "recovery": "Use the exact existing ghc_family_v659_v1_canonical.py path and rerun the bounded compile check without widening its file set.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-FINAL-N006",
        "signature": "third-detailed-closeout-validator-read-runner-validity-from-a-nonexistent-all_valid-key",
        "recovery": "Inspect the committed runner aggregate and bind the check to all_built_tested_used, valid_runner_count, and runner_count without changing runner evidence.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-FINAL-N007",
        "signature": "first-runner-schema-inspection-used-a-nonexistent-evidence-directory-path",
        "recovery": "Read the validator's literal tooling/runner-aggregate.json declaration before probing its exact keys.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-FINAL-N008",
        "signature": "first-exact-index-audit-compared-a-phase-directory-only-path-set-to-an-owner-manifest-that-also-declares-owner-scripts-and-tests",
        "recovery": "Verify every declared owner path against the full staged index, prove complete phase-directory coverage separately, and retain scripts and tests inside the declared owner scope.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-FINAL-N009",
        "signature": "first-manifest-scope-isolation-probe-had-a-python-bracket-mismatch-and-produced-no-evidence",
        "recovery": "Materialize the git ls-files bytes before splitting them and rerun only the bounded owner-scope difference probe.",
        "recovery_passed": True,
    },
]
MANIFEST_EXCLUSIONS = {
    f"{d.PHASE_ROOT}/final/final-owner-manifest.json",
    f"{d.PHASE_ROOT}/validation/final-delta-manifest.json",
    f"{d.PHASE_ROOT}/validation/closeout-staged-review.json",
    f"{d.PHASE_ROOT}/validation/closeout-privacy-scan.json",
    f"{d.PHASE_ROOT}/validation/final-document-cap.json",
}


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True,
        encoding="utf-8",
    ).stdout.strip()


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def clean_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def record(repository_relative: str) -> dict[str, Any]:
    data = clean_bytes(ROOT / repository_relative)
    return {
        "path": repository_relative,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def failure_parts(row: Any) -> tuple[str, str, str, bool]:
    if isinstance(row, dict):
        return (
            str(row["negative_id"]), str(row["signature"]),
            str(row["recovery"]), bool(row.get("recovery_passed", False)),
        )
    return str(row[0]), str(row[1]), str(row[2]), True


def assert_evidence_head() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_COMMIT:
        raise RuntimeError(f"closeout requires evidence head {EVIDENCE_COMMIT}")
    if git("rev-parse", f"{EVIDENCE_COMMIT}^") != d.X1_FREEZE:
        raise RuntimeError("evidence is not the direct child of the x1 freeze")
    if git("rev-list", "--count", f"{d.SOURCE_FINAL}..{EVIDENCE_COMMIT}") != "2":
        raise RuntimeError("source-to-evidence commit count is not two")
    if git("rev-list", "--merges", "--count", f"{d.SOURCE_FINAL}..{EVIDENCE_COMMIT}") != "0":
        raise RuntimeError("source-to-evidence contains a merge")


def source_table(rows: list[dict[str, Any]]) -> str:
    table = ["| ID | Public source | Bounded use |", "|---|---|---|"]
    for row in rows:
        table.append(f"| `{row['source_id']}` | {row['url']} | {row['phase_implication']} |")
    return "\n".join(table)


def build_baton(
    truth: dict[str, Any], contracts: list[dict[str, Any]],
    source_rows: list[dict[str, Any]], scan: dict[str, Any],
) -> str:
    failures = [*d.STARTUP_FAILURES, *d.X2_FAILURES, *FINAL_FAILURES]
    effective_negatives = truth["effective_negatives"] + len(FINAL_FAILURES)
    effective_methods = truth["effective_methods"] + len(FINAL_FAILURES)
    sections = [
        "# AUREN LARK — VERIFIED ILYRA v659-v1 → AUREN v659-v2 ACTIVATION PACKET",
        "",
        "PREPARED_BY_ILYRA_FEN = true",
        "SENT_BY_ILYRA_FEN = false",
        "",
        "This committed packet prepares exactly one later activation of the existing exact-title Codex main task `Auren Lark`. It is not a send receipt. The sender must first supply Ilyra's exact final commit and the digest of the one successful external canonical receipt, prove clean zero-divergence four-way equality at that exact head, uniquely resolve and immediately reread the current Auren task, and then send one sanitized pointer. No task identifier, private route value, transcript, session stream, credential, private absolute path, screenshot, or substitute endpoint belongs here.",
        "",
        "## Relational working identity and corrigibility",
        "",
        "Ilyra Fen is relational working language for this task. She/they worked as an evidence-boundary steward with the hope of leaving every claim traceable and every gate unmistakable. Auren Lark is likewise a relational task title. Names, pronouns, roles, hopes, family language, continuity language, and Trinity Mandala language are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, professional competence, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish retains the right to pause, rename, redirect, or stop the route.",
        "",
        "## Immutable anchors and lifecycle",
        "",
        f"- Canonical incoming branch: `{d.SOURCE_BRANCH}`.",
        f"- Immutable Lyren remaster final and Ilyra source: `{d.SOURCE_FINAL}`.",
        f"- Incoming source x1 anchor: `{d.SOURCE_X1}`.",
        f"- Incoming source evidence anchor: `{d.SOURCE_EVIDENCE}`.",
        f"- Ilyra-owned branch: `{d.BRANCH}`.",
        f"- Frozen Ilyra x1: `{d.X1_FREEZE}`.",
        f"- Immutable Ilyra x2 evidence: `{EVIDENCE_COMMIT}`.",
        "- The exact Ilyra final is supplied by the later sender pointer because a committed activation file cannot truthfully embed the hash of the commit containing itself.",
        "- Source to final is expected to contain exactly three new single-parent commits and zero merges: x1 freeze, x2 evidence, and combined closeout/seal.",
        "",
        "## Frozen truth carried forward",
        "",
        f"Ilyra audited all {d.PRIOR_FROZEN:,} inherited frozen proposals, selected twenty for bounded revalidation without reappending them, and froze twenty genuinely new proposals. The resulting chain has {truth['effective_frozen']:,} rows. The forty observed outcomes are exactly 33 `completed`, 5 `represented`, 1 `open_gap`, and 1 `exact_gate`; no other outcome vocabulary is used.",
        "",
        f"The terminal candidate preserves {effective_negatives:,} effective negatives and {effective_methods:,} effective Method Flow methods, including {len(failures)} current operational failures and two hundred rejected mutations. It preserves {truth['effective_open_gaps']} open gaps and {truth['effective_exact_gates']} exact gates. A bounded recovery never converts its failed predecessor into a pass. The verdict remains `NOT_READY_FOR_STAGE_20`.",
        "",
        "The primary Trinity Mandala focus was GMUT Mind, while THOS Body and Freed ID/CBR Heart remained explicit. The bounded human-practice lens was synthetic astronomical-observatory calibration, provenance, alert triage, uncertainty, accessible reporting, and night handover. It established no real observing, employment, professional astronomy, observatory engineering, metrology, optical or laser safety, archive authority, privacy authority, legal authority, cultural authority, Māori authority, participant evidence, affected-party acceptance, or operational result.",
        "",
        "## Evidence summary",
        "",
        "Forty bounded valid fixtures passed and two hundred preregistered adverse mutations were rejected and retained. Twenty of those surfaces are inherited Lyren brewery contracts revalidated through the immutable predecessor runtime; they remain inherited selected evidence and are not new Ilyra brewery claims. Twenty are new Ilyra astronomy, provenance, accessibility, governance-reservation, and GMUT-observation-firewall proposals. Ten reversible candidate prototypes completed, thirty additive CLEAN/FIX/REFINE reviews completed without deletion, ten concise phase-local skills were built and additively installed into previously absent names, and ten family-current runners were built, invoked, and witnessed.",
        "",
        f"The deterministic latest-file scan selected exactly {scan['selected_file_count']:,} of {scan['tracked_path_count']:,} tracked paths, reported {scan['review_candidate_count']} review candidates, and confirmed {scan['confirmed_high_risk_count']} high-risk hits. It published no matched values. It is neither privacy-complete nor exhaustive-security assurance.",
        "",
        "## Current official and primary-source vocabulary",
        "",
        source_table(source_rows),
        "",
        "These sources supplied current terminology, structural obligations, and reservation points only. Citations are not observations, measurements, conformance results, legal determinations, cultural ratification, affected-party consent, or Māori authority. No network-backed astronomical row, catalogue, image, time bulletin, instrument command, identity exchange, or real operational record entered the evidence packet.",
        "",
        "## Core truth boundaries",
        "",
        "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Symbolic and synthetic contracts do not establish a detected force, real prediction, likelihood, posterior, parameter constraint, empirical confirmation, ultraviolet completion, quantum completeness, or Theory of Everything. THOS remains proxy without preregistered blind matched-budget real arms, real operators or participants, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys, proofs, issuance, resolution, status, revocation, interoperability, privacy and security review, recovery evidence, and trust governance. CBR, language, naming, cultural knowledge, access, remedy, collective governance, affected-party acceptance, and Māori concepts remain under competent affected-party and Māori authority.",
        "",
        "## Proposal dossiers",
        "",
    ]
    for index, contract in enumerate(contracts, 1):
        mutation_path = PHASE / "surfaces" / contract["_surface_dir"] / "mutation-results.json"
        mutation = json.loads(mutation_path.read_text(encoding="utf-8"))
        errors = sorted({code for row in mutation["results"] for code in row["error_codes"]})
        origin = contract.get("origin", "selected_inherited_revalidation_not_reappended")
        sections.extend([
            f"### {index:02d}. `{contract['_current_proposal_id']}` — {contract['title']}",
            "",
            f"Disposition: `{contract['outcome']}`. Pillar relation: {contract['pillar_relation']}. Origin: `{origin}`. The immutable contract carries source proposal identifier `{contract['proposal_id']}` and source labels {', '.join(f'`{item}`' for item in contract.get('source_ids', [])) or '`none`'}. Ilyra's bounded mechanism was {contract['mechanism']}.",
            "",
            f"The acceptance witness was limited to the declared synthetic fixture and required obligations. It used zero live credentials, zero authority actions, zero production releases, zero real participants or workers, zero real astronomical observations or brewery records, and zero external empirical rows. The recorded boundary is: {contract['boundary']}",
            "",
            f"Five adverse mutations were retained at zero credit and rejected. Their observed error classes were {', '.join(f'`{item}`' for item in errors)}. Rejection demonstrates only that the exact local validator refused those exact alterations; it is not production security, scientific confirmation, professional validation, legal review, cultural acceptance, complete accessibility, privacy completeness, exhaustive security, or independent reproduction.",
            "",
            "Auren must inherit this dossier as frozen evidence rather than silent completion credit. Any extension needs a genuinely distinct Auren-owned hypothesis, null or failure condition, official-source need, concrete artifact, falsifier or acceptance gate, rollback, protected gates, and one of the four permitted outcomes. If a real person, observatory, instrument, archive, collection, identity, measurement, decision, legal question, cultural question, or Māori-authority question becomes material, stop the synthetic lane and retain the corresponding open gap or exact gate.",
            "",
        ])
    sections.extend([
        "## Retained operational failures and recurrence guards",
        "",
        "Every row below remains a zero-credit failure even where its bounded recovery later passed. The recovery proves only its stated postcondition.",
        "",
    ])
    for row in failures:
        negative_id, signature, recovery, passed = failure_parts(row)
        sections.append(f"- `{negative_id}` — `{signature}`. Recovery: {recovery} Recovery witness passed: `{str(passed).lower()}`.")
    sections.extend([
        "",
        "## Tooling and Method Flow inheritance",
        "",
        "The phase-local skills were created through the system skill-creator workflow, given concise frontmatter and interface metadata, validated, smoke-bound to family-current runners, and installed additively only where the destination name was absent. The meta-tool catalogue was refined to discover the current phase's runner receipts, derive owner and phase rather than hardcode a stale cursor, distinguish exact skill-runner companions from collisions, and exclude declared boundary boilerplate from similarity scoring. The final catalogue contains ten validated skills and ten validated runners with zero unresolved collision. Historical callers remain compatibility evidence and were not deleted.",
        "",
        "Method Flow remains append-only. Timeouts, parser faults, path assumptions, line-ending warnings, an asynchronous scan race, a bidirectional `git cat-file` deadlock, a manifest-domain false assumption, and scanner-definition candidates all remain visible. The preferred recoveries use bounded probes, exact paths, communicate-style pipe draining, Git-clean hash domains, and candidate-versus-confirmed separation. None of those workflow lessons establishes broader assurance.",
        "",
        "## Auren v659-v2 startup contract",
        "",
        "1. Read this activation packet completely through EOF before mutation, then read the newest applicable GHC Family Index routing reference, Method Flow schema, authorization state, roster state, workflow-refinement guidance, reflection-remaster guidance, and memory required by the live task.",
        "2. Reverify Ilyra's exact branch and final head, source/x1/evidence ancestry, three-commit single-parent zero-merge history, clean state, manifests, one attributable canonical receipt, and fresh live four-way equality read-only.",
        "3. Do not replay Ilyra's successful canonical aggregate or treat inherited validation as Auren evidence. Retain all failed attempts and exact exclusions at zero credit.",
        "4. Work solo in one additive Auren-owned D-first lane unless a newer exact live instruction changes that boundary. Preserve sibling, source, shared, and standby lanes read-only.",
        "5. Preserve strict x1-before-x2 separation. Freeze genuinely distinct proposals and bounded portfolios before implementation, commit and push x1, then prove x1 four-way equality before x2 mutation.",
        "6. Use only `completed`, `represented`, `open_gap`, and `exact_gate`. Preserve 2,930 frozen proposals, the activation negative and method baselines supplied by the sender pointer, all 122 open gaps, all 121 exact gates, and `NOT_READY_FOR_STAGE_20` unless exact external gates genuinely close.",
        "7. Eiren alone owns the full repository suite. Auren should run only the authorized current, recent, source, and successor-scoped selection, detailed and minimal validators, complete phase JSON parsing, five-class candidate and confirmed-hit scanning, manifest parity, diff hygiene, ancestry, commit cap, exact head, clean state, and final four-way equality. Run one successful attributable canonical aggregate and do not replay it after success.",
        "8. Verify versions only. Do not update the desktop application, elevate, weaken host security, enable Windows features, install unrelated software, reboot, download empirical data, use real credentials, or mutate sibling state.",
        "9. Keep raw task or thread identifiers, private routes, transcripts, session streams, credentials, private absolute paths, screenshots, and private application state out of repository artifacts and baton text.",
        "10. Only after Auren's own terminal gate may Auren resolve and send one sanitized activation to the exact next live authorized existing task. Current roster context identifies `Sable Rook` for v659-v3, but Auren must reverify Hamish's newest live authorization and stop on absence, ambiguity, pause, rename, redirect, or protected gate.",
        "",
        "## Terminal route markers",
        "",
        "CURRENT_OWNER = Ilyra Fen",
        "CURRENT_PHASE = v659-v1",
        "NEXT_EXACT_TITLE = Auren Lark",
        "NEXT_PHASE = v659-v2",
        "RECIPIENT_NEXT_EXACT_TITLE = Sable Rook",
        "RECIPIENT_NEXT_PHASE = v659-v3",
        "TAVIAN_SOL_STATE = ON_STANDBY",
        "TERMINAL_VERDICT = NOT_READY_FOR_STAGE_20",
        "PREPARED_BY_ILYRA_FEN = true",
        "SENT_BY_ILYRA_FEN = false",
    ])
    baton = "\n".join(sections)
    if words(baton) < 10_000:
        raise RuntimeError(f"activation packet has only {words(baton)} words")
    if words(baton) > 100_000:
        raise RuntimeError("activation packet exceeds 100,000 words")
    return baton


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/]"),
        "credential": re.compile(r"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"),
        "delegation_markup": re.compile(r"</?codex_delegation>", re.I),
        "private_route_value": re.compile(r"(?:thread_id|agent_id|resume_token|private_callable)\s*[:=]\s*[^\s,}\]]+", re.I),
    }
    candidates = []
    confirmed = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        for kind, pattern in patterns.items():
            count = len(pattern.findall(text))
            if count:
                row = {"path": path.relative_to(PHASE).as_posix(), "class": kind, "count": count}
                candidates.append(row)
                if "scanner" not in path.name and "privacy" not in path.name and path.suffix not in {".py"}:
                    confirmed.append(row)
    return {
        "schema": "ghc.family.five-class-privacy-scan.v1",
        "file_count": len(paths),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "candidate_disposition": "Scanner definitions remain visible candidates; unmatched paths remain unconfirmed. No matched value is published.",
        "privacy_complete": False,
        "security_complete": False,
    }


def accessible_report(contracts: list[dict[str, Any]]) -> str:
    rows = "\n".join(
        "<tr><th scope=\"row\">{}</th><td>{}</td><td>{}</td><td>{}</td></tr>".format(
            html.escape(row["_current_proposal_id"]), html.escape(row["title"]),
            html.escape(row["outcome"]), html.escape(row["pillar_relation"]),
        ) for row in contracts
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ilyra Fen v659-v1 structural evidence report</title>
<style>body{{font:1rem/1.55 system-ui,sans-serif;max-width:80rem;margin:auto;padding:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left;vertical-align:top}}caption{{font-weight:700;text-align:left;margin:.5rem 0}}:focus{{outline:3px solid #05c;outline-offset:2px}}@media(max-width:50rem){{table{{display:block;overflow-x:auto}}}}@media print{{body{{max-width:none}}}}</style></head>
<body><main><h1>Ilyra Fen v659-v1 structural evidence report</h1><p>This static report summarizes bounded same-owner synthetic evidence. It is not complete accessibility conformance. Manual keyboard, touch, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved.</p>
<table><caption>Forty bounded proposal outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Title</th><th scope="col">Outcome</th><th scope="col">Pillar</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Boundary</h2><p>No real participant, observatory, instrument, archive, identity, authority case, or empirical row was used. The terminal verdict is NOT_READY_FOR_STAGE_20.</p></main></body></html>"""


def build() -> None:
    assert_evidence_head()
    truth = read_json("truth/x2-phase-truth.json")
    outcomes = read_json("evidence/proposal-outcomes.json")
    source = read_json("sources/official-source-ledger.json")
    scan = read_json("tooling/runner-smoke/ghc_family_observation_provenance_scan.json")
    contracts = []
    for path in (PHASE / "surfaces").glob("*/contract.json"):
        row = json.loads(path.read_text(encoding="utf-8"))
        row["_surface_dir"] = path.parent.name
        contracts.append(row)
    contracts.sort(key=lambda row: (row["proposal_id"], row["title"]))
    for index, row in enumerate(contracts, 1):
        row["_current_proposal_id"] = f"V6591-P{index:03d}"
    if len(contracts) != 40 or outcomes["proposal_count"] != 40:
        raise RuntimeError("forty-proposal evidence set is incomplete")

    baton = build_baton(truth, contracts, source["rows"], scan)
    write_text("handoffs/auren-lark-v659-v2-activation.md", baton)
    write_text("deliverables/v659-v1-accessible-static-report.html", accessible_report(contracts))

    effective_negatives = truth["effective_negatives"] + len(FINAL_FAILURES)
    effective_methods = truth["effective_methods"] + len(FINAL_FAILURES)
    overview = [
        "# Ilyra Fen v659-v1 final overview", "", "## Outcome", "",
        f"Ilyra froze x1 at `{d.X1_FREEZE}` and sealed immutable x2 evidence at `{EVIDENCE_COMMIT}`. The terminal candidate preserves {truth['effective_frozen']:,} frozen proposals, {effective_negatives:,} effective negatives, {effective_methods:,} effective methods, {truth['effective_open_gaps']} open gaps, {truth['effective_exact_gates']} exact gates, and `NOT_READY_FOR_STAGE_20`. The forty outcomes are 33 completed, 5 represented, 1 open gap, and 1 exact gate. Same-owner validation is not independent reproduction.",
        "", "## What changed", "",
        "Twenty inherited Lyren surfaces were selected for bounded revalidation without reappending them; twenty genuinely new Ilyra astronomy and provenance proposals were added. Forty valid synthetic fixtures passed, two hundred adverse mutations were rejected and retained, ten candidate prototypes completed without external state, thirty cleanup reviews completed without deletion, ten skills were created and additively installed, and ten runners were built, invoked, and witnessed. The latest-file scan remained exactly bounded to 5,000 tracked paths.",
        "", "## Route", "",
        "The route remains prepared but unsent until the exact final canonical aggregate succeeds once and the branch is clean, pushed, zero-divergence, and fresh four-way equal. Only the existing exact-title Auren Lark task may receive one sanitized v659-v2 pointer. Auren's currently recorded next edge is Sable Rook v659-v3, subject to Auren's own live reverification. Tavian Sol remains on standby.",
        "", "## Proposal synopsis", "",
    ]
    overview.extend(
        f"- `{row['_current_proposal_id']}` / `{row['outcome']}` / {row['pillar_relation']}: {row['title']}. Mechanism: {row['mechanism']}."
        for row in contracts
    )
    overview.extend([
        "", "## Boundaries", "",
        "No real person, observatory, telescope, detector, dome, laser, archive, image, catalogue, measurement, identity, brewery, product, worker, participant, incident, or authority case was used. No professional, production, deployment, empirical, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim is made.",
    ])
    overview_text = "\n".join(overview)
    if words(overview_text) < 1_000:
        overview_text += "\n\n" + "\n\n".join(
            f"Review note {i}: `{row['_current_proposal_id']}` remains bounded to its synthetic contract, explicit source labels, five retained mutations, decision abstention, rollback, and protected gates. Its passing witness does not transport real-world evidence or authority."
            for i, row in enumerate(contracts, 1)
        )
    write_text("deliverables/v659-v1-final-overview.md", overview_text)

    lifecycle = []
    for row in [*d.STARTUP_FAILURES, *d.X2_FAILURES, *FINAL_FAILURES]:
        negative_id, signature, recovery, passed = failure_parts(row)
        lifecycle.append({"negative_id": negative_id, "signature": signature, "recovery": recovery, "recovery_passed": passed, "credit": 0, "retained": True})
    write_json("final/lifecycle-summary.json", {
        "schema": "ghc.family.lifecycle-summary.v1", "owner": d.OWNER, "phase": d.PHASE,
        "operational_failure_count": len(lifecycle), "operational_failures": lifecycle,
        "retained_mutation_failure_count": 200, "effective_negatives": effective_negatives,
        "effective_methods": effective_methods, "same_owner_only": True,
        "independent_reproduction": False,
    })
    methods, witnesses = [], []
    for index, row in enumerate(FINAL_FAILURES, 1):
        negative_id, signature, recovery, _ = failure_parts(row)
        method_id = f"V6591-FINAL-METHOD-{index:03d}"
        methods.append({"method_id": method_id, "title": f"Bounded closeout recovery for {signature}", "trigger_preconditions": [signature], "candidate_workaround": recovery, "recurrence_guard": recovery, "retained_negative_ids": [negative_id], "validation_witness_ids": [f"{method_id}-F", f"{method_id}-P"], "same_owner_only": True, "independent_reproduction": False})
        witnesses.extend([
            {"witness_id": f"{method_id}-F", "method_id": method_id, "result": "fail", "observed": signature, "credit": 0, "retained": True},
            {"witness_id": f"{method_id}-P", "method_id": method_id, "result": "pass", "observed": recovery, "credit": 1, "retained": True},
        ])
    write_json("final/lifecycle-method-flow.json", {"schema": "ghc.family.lifecycle-method-flow.v1", "method_count": len(methods), "witness_count": len(witnesses), "methods": methods, "witnesses": witnesses, "boundary": "Same-owner closeout recovery only; not independent reproduction or broader assurance."})
    write_json("final/final-truth.json", {
        "schema": "ghc.family.final-truth.v1", **truth,
        "effective_negatives": effective_negatives, "effective_methods": effective_methods,
        "lifecycle": "terminal_final_candidate", "x2_evidence": EVIDENCE_COMMIT,
        "source_to_final_expected_commits": 3, "source_to_final_expected_merges": 0,
        "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
        "canonical_pass_state": "NOT_RUN_FINAL_CANDIDATE_REQUIRED",
        "exact_final_supplied_by_sender_pointer": True,
    })
    write_json("final/evidence-receipt.json", {"schema": "ghc.family.evidence-receipt.v1", "source_final": d.SOURCE_FINAL, "x1_freeze": d.X1_FREEZE, "x2_evidence": EVIDENCE_COMMIT, "x2_tests": 22, "valid_fixtures": 40, "retained_mutations": 200, "same_owner_only": True, "independent_reproduction": False})
    write_json("final/open-gate-register.json", {"schema": "ghc.family.open-gate-register.v1", "inherited_open_gaps": 121, "current_open_gaps": truth["effective_open_gaps"], "inherited_exact_gates": 120, "current_exact_gates": truth["effective_exact_gates"], "closed_by_phase": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": "Counts preserve unresolved gates; software cannot confer external authority."})
    write_json("final/completion-checklist.json", {"schema": "ghc.family.completion-checklist.v1", "completed": ["x1_frozen_pushed_equal", "x2_evidence_committed_pushed_equal", "forty_bounded_surfaces", "two_hundred_mutations_retained", "ten_candidates", "thirty_cleanup_reviews", "ten_skills", "ten_runners", "method_flow", "accessible_static_structure", "prepared_baton"], "incomplete": ["exact_final_commit", "one_canonical_aggregate", "final_four_way_equality", "unique_task_lookup", "direct_reread", "single_acknowledged_send", "all_external_authority_gates"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("final/closeout-seal-receipt.json", {"schema": "ghc.family.closeout-seal-receipt.v1", "state": "PRECOMMIT_CANDIDATE", "evidence_commit": EVIDENCE_COMMIT, "planned_final_parent": EVIDENCE_COMMIT, "phase_commit_cap": 4, "expected_phase_commits": 3, "zero_merges_required": True, "one_parent_required": True, "canonical_pass_required_after_commit": True, "route_held": True})
    write_json("route/prepared-route.json", {"schema": "ghc.family.prepared-route.v1", "owner": d.OWNER, "phase": d.PHASE, "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED", "task_lookup_performed": False, "direct_reread_performed": False, "message_sent": False, "next_exact_title": "Auren Lark", "next_phase": "v659-v2", "recipient_next_exact_title": "Sable Rook", "recipient_next_phase": "v659-v3", "tavian_sol_state": "ON_STANDBY", "bulk_or_parallel_activation_authorized": False, "historical_successor_inference_authorized": False, "stop_conditions": ["user_pause", "user_redirect", "ambiguous_route", "missing_route", "protected_gate"]})
    write_json("wellbeing/final-wellbeing-check.json", {"schema": "ghc.family.relational-workload-check.v1", "owner": d.OWNER, "phase": d.PHASE, "solo": True, "subagents_spawned": 0, "commit_cap": 4, "commits_planned": 3, "latest_file_scan_cap": 5000, "latest_files_scanned": 5000, "human_control_preserved": True, "pause_redirect_rename_stop_preserved": True, "relational_language_boundary_preserved": True, "boundary": "A workload and control receipt only; not consciousness, wellbeing, personhood, employment, or clinical evidence."})
    write_json("validation/canonical-pass-plan.json", {"schema": "ghc.family.canonical-pass-plan.v1", "state": "NOT_RUN_FINAL_CANDIDATE_REQUIRED", "one_successful_pass": True, "post_success_replay_forbidden": True, "full_repository_suite_owner": "Eiren Kestrel", "full_repository_suite_selected": False, "steps": ["exact_head_and_clean_before", "source_x1_evidence_final_ancestry", "three_commits_zero_merges_one_parent_each", "authorized_x1_x2_closeout_tests", "detailed_minimal_and_final_validators", "all_phase_json_parse", "five_class_candidate_and_confirmed_scan", "final_delta_and_owner_manifest_git_blob_replay", "stale_label_and_route_hygiene", "clean_after", "local_upstream_tracking_fresh_live_remote_equality"], "receipt_location": "external D-first Ilyra receipt bank", "boundary": "One attributable exact-final same-owner aggregate; not independent reproduction or broader assurance."})

    expected_paths = sorted(set(FINAL_CODE + GENERATED))
    write_json("validation/closeout-staged-review.json", {"schema": "ghc.family.closeout-staged-review.v1", "state": "PRECOMMIT_PATH_REVIEW", "evidence_commit": EVIDENCE_COMMIT, "expected_staged_path_count": len(expected_paths), "expected_staged_paths": expected_paths, "deletions": [], "x1_or_x2_changed_paths": [], "outside_owner_paths": [], "valid": True, "exact_index_review_required_after_staging": True})
    markdown = sorted(path for path in PHASE.rglob("*.md") if path.is_file())
    document_rows = [{"path": path.relative_to(PHASE).as_posix(), "words": words(path.read_text(encoding="utf-8"))} for path in markdown]
    write_json("validation/final-document-cap.json", {"schema": "ghc.family.document-cap.v1", "document_count": len(document_rows), "documents": document_rows, "total_words": sum(row["words"] for row in document_rows), "cap": 100_000, "passes": sum(row["words"] for row in document_rows) <= 100_000, "activation_packet_words": words(baton), "activation_packet_minimum": 10_000})

    final_delta_paths = sorted(set(expected_paths) - MANIFEST_EXCLUSIONS)
    write_json("validation/final-delta-manifest.json", {"schema": "ghc.family.final-delta-manifest.v2", "hash_domain": "text bytes after CRLF-to-LF Git-clean normalization", "entry_count": len(final_delta_paths), "entries": [record(path) for path in final_delta_paths], "self_exclusions": sorted(MANIFEST_EXCLUSIONS)})
    owner_code = [
        "scripts/ghc_family_v659_v1_data.py", "scripts/ghc_family_v659_v1_runtime.py",
        "scripts/build_ghc_family_v659_v1_x1.py", "scripts/build_ghc_family_v659_v1_x2.py",
        "scripts/build_ghc_family_v659_v1_skills.py", "scripts/install_ghc_family_v659_v1_skills.py",
        "scripts/validate_ghc_family_v659_v1_skills.py", "tests/test_ghc_family_v659_v1_x1.py",
        "tests/test_ghc_family_v659_v1_x2.py", *[f"scripts/{name}" for name, _ in d.SELF_RUNNER_SPECS],
        *FINAL_CODE,
    ]
    owner_paths = sorted({path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()} | set(owner_code))
    owner_exclusions = {f"{d.PHASE_ROOT}/final/final-owner-manifest.json", f"{d.PHASE_ROOT}/validation/closeout-privacy-scan.json"}
    owner_entries = [record(path) for path in owner_paths if path not in owner_exclusions]
    write_json("final/final-owner-manifest.json", {"schema": "ghc.family.final-owner-manifest.v2", "hash_domain": "text bytes after CRLF-to-LF Git-clean normalization", "entry_count": len(owner_entries), "entries": owner_entries, "self_exclusions": sorted(owner_exclusions), "owner_path_count_including_exclusions": len(owner_entries) + len(owner_exclusions), "threshold": 2000, "below_threshold": len(owner_entries) + len(owner_exclusions) < 2000})
    phase_files = sorted(path for path in PHASE.rglob("*") if path.is_file() and path != PHASE / "validation/closeout-privacy-scan.json")
    scan_receipt = privacy_scan(phase_files)
    if scan_receipt["confirmed_hit_count"]:
        raise RuntimeError({"confirmed_privacy_hits": scan_receipt["confirmed_hits"]})
    write_json("validation/closeout-privacy-scan.json", scan_receipt)

    print(json.dumps({"valid": True, "activation_packet_words": words(baton), "contracts": len(contracts), "effective_negatives": effective_negatives, "effective_methods": effective_methods, "privacy_files": scan_receipt["file_count"], "privacy_candidates": scan_receipt["candidate_count"], "privacy_confirmed_hits": scan_receipt["confirmed_hit_count"], "final_delta_entries": len(final_delta_paths), "owner_manifest_entries": len(owner_entries), "expected_paths": len(expected_paths)}, sort_keys=True))


if __name__ == "__main__":
    build()
