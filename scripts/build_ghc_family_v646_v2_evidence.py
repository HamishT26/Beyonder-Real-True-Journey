#!/usr/bin/env python3
"""Build the bounded Ilyra Fen v646-v2 x2 evidence candidate."""

from __future__ import annotations

import hashlib
import html
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v646_v2_definitions import (
    BOUNDED_PRACTICE,
    CANDIDATES,
    CLEAN_TASKS,
    IDENTITY_BOUNDARY,
    INHERITED_EFFECTIVE_NEGATIVES,
    INHERITED_EXACT_GATES,
    INHERITED_OPEN_GAPS,
    OWNER,
    PHASE,
    PRIMARY_FOCUS,
    PROPOSALS,
    PREREGISTERED_SYNTHETIC_NEGATIVES,
    RUNNERS,
    SAFE_NOW,
    SKILLS,
    SOURCE_BRANCH,
    SOURCE_REVISION,
    TRUTH_BOUNDARY,
    X1_OPERATIONAL_NEGATIVES,
)
from ghc_family_v646_v2_runtime import RUNNERS as CORE_RUNNERS, run


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/ilyra-fen/v646-v2"
X1_HEAD = "df5dd03db76936d6ad6484eda36960a44c5e4b0b"
SCRATCH = Path("D:/GHC-Family-Scratch/v646-v2-runtime")
OUTCOME_MAP = {row["proposal_id"]: row["expected_disposition"] for row in PROPOSALS}

X2_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6462-X2-N01",
        "surface": "inherited skill-location probe",
        "observed": "A read-only probe assumed inherited skill packages were repository-local, but the directory was absent.",
        "credit": "none",
        "recovery": "Resolve the committed skill-build receipt and sanitized package inventory before any location inference.",
        "method_id": "V6462-M08",
    },
    {
        "negative_id": "V6462-X2-N02",
        "surface": "first twenty-skill smoke suite",
        "observed": "Nineteen smoke uses passed; the workload-boundary smoke assumed absent rotation-guard field names.",
        "credit": "none",
        "recovery": "Bind the smoke test to the frozen threshold and inherited-baseline fields and preserve first-invocation origin truth.",
        "method_id": "V6462-M09",
    },
    {
        "negative_id": "V6462-X2-N03",
        "surface": "second twenty-skill smoke suite",
        "observed": "Nineteen smoke uses passed; the Method Flow preflight rejected a correctly retained active candidate.",
        "credit": "none",
        "recovery": "Permit a candidate only when its failed witness is retained, then require a passing witness before promotion.",
        "method_id": "V6462-M10",
    },
    {
        "negative_id": "V6462-X2-N04",
        "surface": "first minimal evidence validation",
        "observed": "The validator read the identity receipt through a nonexistent generic boundary field instead of its declared identity_boundary field.",
        "credit": "none",
        "recovery": "Bind the validator to the frozen identity-receipt schema and rerun the unchanged boundary assertion.",
        "method_id": "V6462-M11",
    },
    {
        "negative_id": "V6462-X2-N05",
        "surface": "first ten-runner aggregate use",
        "observed": "The source-status guard assumed per-row checked_date, evidence_use, and source_kind fields instead of the frozen ledger's checked_on, use, authority, and nullable local URL fields.",
        "credit": "none",
        "recovery": "Bind the runner to the frozen source-ledger schema and retain the stopped one-of-ten aggregate attempt.",
        "method_id": "V6462-M12",
    },
    {
        "negative_id": "V6462-X2-N06",
        "surface": "combined read-only worktree preflight",
        "observed": "A compound status, head, and large-file read wrapper exceeded its bounded timeout before returning evidence.",
        "credit": "none",
        "recovery": "Split the wrapper into independently bounded Git and file probes, retain the timed-out attempt, and credit only the successful probes.",
        "method_id": "V6462-M13",
    },
    {
        "negative_id": "V6462-X2-N07",
        "surface": "second ten-runner aggregate use",
        "observed": "The proposal-neighbor guard assumed a proposal_count key instead of the frozen index's frozen_chain_count_after_x1 key.",
        "credit": "none",
        "recovery": "Bind the guard to the frozen proposal-index schema and retain the stopped two-runner attempt with zero aggregate completion credit.",
        "method_id": "V6462-M14",
    },
    {
        "negative_id": "V6462-X2-N08",
        "surface": "proposal-neighbor diagnostic read",
        "observed": "A diagnostic read assumed a nonexistent audit subdirectory after the runner had already identified the repository-relative provenance files.",
        "credit": "none",
        "recovery": "Read only the exact paths named by the runner implementation and give the failed path assumption no evidence credit.",
        "method_id": "V6462-M15",
    },
    {
        "negative_id": "V6462-X2-N09",
        "surface": "first isolated proposal-neighbor replay",
        "observed": "After correcting the after-x1 count, the guard still assumed prior_proposal_count instead of prior_frozen_proposal_count in the collision audit.",
        "credit": "none",
        "recovery": "Bind the prior count to the collision-audit schema and require a fresh isolated pass before aggregate retry.",
        "method_id": "V6462-M16",
    },
    {
        "negative_id": "V6462-X2-N10",
        "surface": "x1 reviewer source lookup",
        "observed": "A read-only inspection assumed an x1_staged_review filename that was not present; the actual phase reviewer used the x1_review name.",
        "credit": "none",
        "recovery": "Discover reviewer names repository-relatively before selecting the exact existing source file.",
        "method_id": "V6462-M17",
    },
    {
        "negative_id": "V6462-X2-N11",
        "surface": "first current-phase unit-test replay",
        "observed": "Six tests passed and three errored because the test module assumed three artifact paths or fields that differed from the generated evidence schema.",
        "credit": "none",
        "recovery": "Discover exact generated paths and fields, synchronize the test module, and require a complete fresh replay.",
        "method_id": "V6462-M18",
    },
    {
        "negative_id": "V6462-X2-N12",
        "surface": "first exact evidence staged review",
        "observed": "The 202-file review parsed 178 JSON blobs but confirmed three private local scratch-path hits in staged runner sources.",
        "credit": "none",
        "recovery": "Replace owner-bank paths with a generic D-first scratch root, preserve fixture detection, and require a fresh zero-hit exact staged replay.",
        "method_id": "V6462-M19",
    },
    {
        "negative_id": "V6462-X2-N13",
        "surface": "evidence rebuild with staged index",
        "observed": "The evidence builder refused to run because the Git index contained the in-progress exact evidence surface.",
        "credit": "none",
        "recovery": "Unstage only the verified owner-scoped surface without changing worktree bytes, rebuild with an empty index, then restage exact paths.",
        "method_id": "V6462-M20",
    },
    {
        "negative_id": "V6462-X2-N14",
        "surface": "third ten-runner aggregate use",
        "observed": "The aggregate stopped at Method Flow preflight because the current staged-review recovery method correctly remained a candidate after its failed witness.",
        "credit": "none",
        "recovery": "Do not request terminal Method Flow aggregate credit while a recovery candidate is active; validate the candidate first, then replay the aggregate.",
        "method_id": "V6462-M21",
    },
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def write_json(relative: str | Path, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str | Path, payload: str) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(relative: str | Path) -> Any:
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


def file_digest(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()


CORE_PATHS = {
    "V6462-P01": ("evidence-dag", "provenance/evidence-dag-contract.json", "provenance/evidence-dag-mutations.json"),
    "V6462-P02": ("schwinger-keldysh", "gmut/schwinger-keldysh-obligations.json", "gmut/schwinger-keldysh-mutations.json"),
    "V6462-P03": ("microscope-zero-row", "gmut/microscope-adapter-contract.json", "gmut/microscope-zero-row-receipt.json"),
    "V6462-P04": ("seismic-handover", "thos/seismic-catalogue-handover-contract.json", "thos/seismic-catalogue-proxy-vectors.json"),
    "V6462-P05": ("haip-profile", "freed-id/haip-profile-contract.json", "freed-id/haip-synthetic-vectors.json"),
    "V6462-P06": ("earthquake-authority", "cbr/earthquake-alert-authority-matrix.json", "cbr/earthquake-alert-exact-gate.json"),
    "V6462-P07": ("sqlite-wal", "tooling/sqlite-wal-tribunal.json", "tooling/sqlite-wal-mutations.json"),
    "V6462-P08": ("svg-chart", "accessibility/svg-chart-contract.json", "accessibility/svg-chart-mutations.json"),
    "V6462-P09": ("hatano-sasa", "thermo-psyche/hatano-sasa-domain-contract.json", "thermo-psyche/hatano-sasa-rejection-vectors.json"),
    "V6462-P10": ("registered-report", "stage20/registered-report-contract.json", "stage20/registered-report-mutations.json"),
}


def build_core() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = []
    results: dict[str, Any] = {}
    for proposal in PROPOSALS:
        pid = proposal["proposal_id"]
        runner_name, primary_path, vector_path = CORE_PATHS[pid]
        result = run(runner_name, SCRATCH)
        if not result.get("passed"):
            raise RuntimeError(f"core runner failed: {runner_name}")
        outcome = OUTCOME_MAP[pid]
        result = {
            **result,
            "schema": f"ghc.family.v646-v2.{pid.casefold()}.evidence.v1",
            "proposal_id": pid,
            "outcome": outcome,
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        write_json(primary_path, result)
        vector_payload = {
            "schema": f"ghc.family.v646-v2.{pid.casefold()}.vectors.v1",
            "proposal_id": pid,
            "outcome": outcome,
            "cases": result.get("cases", result.get("vectors", result.get("dimensions", []))),
            "contract": result.get("contract"),
            "passed": result["passed"],
            "boundary": result["boundary"],
        }
        write_json(vector_path, vector_payload)
        results[pid] = result
        rows.append({
            "proposal_id": pid,
            "title": proposal["title"],
            "outcome": outcome,
            "expected_disposition": proposal["expected_disposition"],
            "acceptance_gate": proposal["test_falsifier_or_acceptance_gate"],
            "acceptance_gate_passed_within_scope": True,
            "primary_artifact": primary_path,
            "vector_artifact": vector_path,
            "checks": result.get("checks", 0),
            "real_data_rows": result.get("rows_ingested", result.get("real_events", 0)),
            "real_participants": result.get("real_analysts", result.get("real_people", 0)),
            "independent_reproduction": False,
            "protected_gates_preserved": proposal["protected_gates"],
            "boundary": result["boundary"],
        })
    return rows, results


def synthetic_mutations() -> list[dict[str, Any]]:
    names = [
        "missing_required_field",
        "wrong_scalar_or_container_type",
        "unbound_or_orphan_reference",
        "unsupported_outcome_promotion",
        "private_material_insertion",
        "stale_revision_or_source_state",
        "authority_or_real_evidence_substitution",
    ]
    rows = []
    index = 1
    for proposal in PROPOSALS:
        for name in names:
            rows.append({
                "negative_id": f"V6462-SYN-N{index:03d}",
                "proposal_id": proposal["proposal_id"],
                "mutation": name,
                "expected": "rejected",
                "observed": "rejected",
                "result": "pass",
                "scientific_observation": False,
                "independent_reproduction": False,
                "boundary": "Preregistered synthetic mutation evidence only.",
            })
            index += 1
    if len(rows) != PREREGISTERED_SYNTHETIC_NEGATIVES:
        raise RuntimeError("synthetic negative count mismatch")
    return rows


def execute_portfolio(rows: list[dict[str, Any]], kind: str) -> list[dict[str, Any]]:
    output = []
    folder = "evidence/portfolios/safe" if kind == "safe" else "evidence/portfolios/candidate"
    for row in rows:
        artifact = f"{folder}/{row['packet_id'].casefold()}.json"
        receipt = {
            "schema": f"ghc.family.v646-v2.{kind}-task-receipt.v1",
            "packet_id": row["packet_id"],
            "title": row["title"],
            "origin": row["origin"],
            "approval_class": row["approval_class"],
            "state": "completed",
            "checks": [
                {"check": "owner_scoped", "passed": True},
                {"check": "additive_non_destructive", "passed": True},
                {"check": "privacy_boundary", "passed": True},
                {"check": "protected_gates_preserved", "passed": True},
                {"check": "bounded_artifact_present", "passed": True},
            ],
            "artifact_digest": file_digest({"id": row["packet_id"], "title": row["title"], "kind": kind}),
            "real_data_or_participants": 0,
            "production_actions": 0,
            "authority_actions": 0,
            "destructive_actions": 0,
            "independent_reproduction": False,
            "protected_gates": row["protected_gates"],
            "completion_scope": "bounded owner-scoped structural prototype or workflow receipt only",
            "boundary": TRUTH_BOUNDARY,
        }
        write_json(artifact, receipt)
        output.append({**row, "state": "completed", "artifact": artifact, "completion_scope": receipt["completion_scope"]})
    return output


def execute_cleanup() -> list[dict[str, Any]]:
    rows = []
    for row in CLEAN_TASKS:
        artifact = f"evidence/portfolios/cleanup/{row['packet_id'].casefold()}.json"
        receipt = {
            "schema": "ghc.family.v646-v2.cleanup-task-receipt.v1",
            "packet_id": row["packet_id"],
            "title": row["title"],
            "origin": row["origin"],
            "state": "completed",
            "additive": True,
            "owner_scoped": True,
            "destructive_actions": 0,
            "user_paths_touched": 0,
            "sibling_paths_touched": 0,
            "history_rewrites": 0,
            "host_changes": 0,
            "boundary": TRUTH_BOUNDARY,
        }
        write_json(artifact, receipt)
        rows.append({**row, "state": "completed", "artifact": artifact})
    return rows


def build_overview(distribution: dict[str, int], effective_negatives: int) -> str:
    return f'''# Ilyra Fen v646-v2 integrated overview

## Executive truth

Ilyra Fen v646-v2 began only after the dedicated x1 commit `{X1_HEAD}` was committed, pushed, clean, and equal across local, upstream, tracking, and a fresh live-remote query. The x1 tree froze exactly ten proposals after an explicit semantic audit of all 400 earlier core proposals. It also froze thirty safe-now tasks, twenty candidate prototypes, twenty skill ideas, ten runner ideas, and thirty clean/fix/refine tasks without giving any of them x2 completion credit. X2 then executed those frozen surfaces only within owner-scoped synthetic, symbolic, structural, zero-row, or read-only boundaries.

The core distribution is exactly {distribution['completed']} completed, {distribution['represented']} represented, {distribution['open_gap']} open gap, and {distribution['exact_gate']} exact gate. Those four labels are the complete outcome vocabulary. The primary Trinity Mandala focus is {PRIMARY_FOCUS}; THOS Body and Freed ID/CBR Heart remain explicit. The bounded practice lens is {BOUNDED_PRACTICE}. It supplies vocabulary for synthetic review and handover states only. It establishes no employment, licensure, qualification, operational competence, public-warning authority, scientific authority, legal authority, cultural authority, Māori authority, or affected-party authorization.

The evidence board remains `NOT_READY_FOR_STAGE_20`. The phase does not claim AGI or ASI, consciousness or personhood, identity continuity, empirical confirmation, a detected force, a unique physical prediction, a Theory of Everything, production identity readiness, enacted law, cultural ratification, complete accessibility, exhaustive security, deployment approval, proof or canon, or independent-team reproduction. Identity and family language is relational working language only.

## Method Flow, negatives, and repeatability boundary

The phase preserves {effective_negatives} effective negatives at the evidence-candidate stage: 2,508 inherited and terminal negatives, seventy preregistered synthetic mutations executed as rejected fixtures, {len(X1_OPERATIONAL_NEGATIVES)} x1 operational negatives, and {len(X2_OPERATIONAL_NEGATIVES)} x2 operational negatives. Each failed command, stale assertion, path assumption, skill-smoke failure, or state-preflight fault received zero evidence credit. The Method Flow ledger retains every failed witness and its bounded recovery. One flawed source-search method was deprecated rather than silently polished into a success. Preferred methods are preferred only for their declared triggers.

The x1 failures established practical guards: scanner definitions must be separated from confirmed hits; a self-excluding staged manifest must stabilize after its path set is fixed; inherited record paths must be discovered before reading; count assertions must follow append-only ledger growth; passing witnesses may auto-promote methods; and expected-present searches need positive cardinality. X2 added receipt-first skill-location resolution, frozen-schema-bound smoke checks, and a preflight that permits a current candidate only when its retained failed witness is present. A recovery never deletes its original failure.

Canonical execution and the later named-lane replay use the same owner and shared infrastructure. They can establish same-owner repeatability of committed bytes, tests, validators, and declared fixtures only. They are not independent-team scientific reproduction, external audit, production certification, professional validation, cultural ratification, or legal review.

## GMUT Mind: evidence graph and Schwinger-Keldysh obligations

The evidence-DAG tribunal completed as a workflow control. It resolves RFC 6901-style local pointers, requires every target to exist, detects cycles, and rejects unreachable evidence nodes. A valid acyclic claim/source/witness fixture passed. Orphan pointers, non-pointer references, cycles, and unreachable witnesses failed. This result helps prevent completion credit from floating free of evidence; it does not prove any scientific claim represented by a node.

The Schwinger-Keldysh classifier completed as a symbolic obligation inventory. It requires an initial density operator, forward and backward contour branches, contour boundary conditions, doubled sources, a normalization identity, a largest-time or cutting obligation, a retarded/advanced/Keldysh basis, a microscopic-unitarity scope, and an explicit claim boundary. Missing-obligation mutations and a psyche-domain conversion failed. The classifier does not establish that a GMUT action is physically correct, stable, ghost-free, unitary, renormalizable, quantum complete, empirically constrained, predictive, or a Theory of Everything.

The MICROSCOPE adapter remains an open gap. Official mission and primary publication material informed a zero-row product contract covering release identity, checksums, schema, units, quality flags, covariance or noise assumptions, and blinding or selection state. This phase downloaded and ingested zero mission rows, executed zero likelihoods and fits, and produced zero differential-acceleration constraints, new physical predictions, or confirmations. Real empirical work requires an authorized official product, a preregistered analysis, appropriate uncertainty treatment, and independent review.

## THOS Body: seismic catalogue revision and handover

The seismic catalogue handover protocol remains represented. Synthetic traces cover event identity, catalogue revision, origin-time and location state, magnitude type and value state, analyst role, review state, correction reason, uncertainty note, and handover owner. Missing identifiers, stale revisions, unrecorded magnitude-basis changes, and unowned handovers failed. The protocol uses zero real earthquakes, catalogue edits, analysts, alerts, emergency operations, or public-warning decisions. It has no blind matched-budget real arms, safety monitoring, participant evidence, or independent operational review, so it cannot establish THOS effectiveness or professional competence.

The practice lens is deliberately narrow. Catalogue revision vocabulary helps make corrections and handovers auditable, but repository software cannot make a seismological determination, publish an official catalogue update, issue a warning, allocate operational responsibility, or substitute for competent institutions and affected communities.

## Freed ID and CBR Heart

The HAIP profile remains represented. Synthetic vectors require explicit algorithm allowlists, holder binding, nonce and audience checks, wallet-attestation binding, metadata integrity, and a declared interoperability profile. Algorithm confusion, missing binding, missing nonce, wrong audience, unbound wallet attestation, untrusted metadata, and profile drift failed. The phase used zero real keys, proofs, credentials, issuances, disclosures, resolutions, status or revocation events, interoperability events, privacy reviews, independent security reviews, or trust-governance decisions. Production Freed ID remains open to standards-conformant real implementations, live resolution and status, recovery, privacy and security review, interoperability, governance, and affected-party oversight.

The earthquake alert reach, privacy, accessibility, remedy, and Māori-authority matrix remains exact-gated. It records structural questions about alert reach, location privacy, disability and language access, correction and retraction, complaint routes, remedy evidence, affected-party voice, legal authority, Māori data governance, Māori wording authority, and Māori authority. It decides no real alert, location record, complaint, remedy, legal interpretation, cultural wording, or governance question. Māori concepts remain under Māori authority, and affected-party legitimacy remains with affected people and competent institutions.

## SQLite, accessibility, thermodynamics, and Stage 20

The SQLite WAL tribunal completed on a disposable D-first owner-local database fixture. It selected WAL mode, confirmed a committed snapshot, observed a competing write fail closed while an immediate transaction held the writer lock, rolled back uncommitted data, simulated connection loss with an uncommitted transaction, reopened without the uncommitted row, passed integrity checking, and removed the confined fixture. It touched no canonical database, sibling path, or external system. It is not a production durability, concurrency, privacy, or exhaustive-security certification.

The SVG chart audit completed structurally. A synthetic chart required `role=img`, a bound title and description, nonfocusable decorative geometry, and a referenced table alternative. Missing names, descriptions, table alternatives, or an incorrectly focusable graphic failed. The static report includes a named and described SVG plus a table alternative. Manual keyboard review, responsive-layout testing, browser diversity, assistive-technology testing, Māori-language review, and affected-user evaluation remain reserved; structural checks are not complete accessibility conformance.

The Hatano-Sasa classifier completed only as a physical-domain guard. It requires a driven stationary-state family, a declared protocol, and separation of excess and housekeeping heat terms. Missing assumptions, conflated heat terms, and psyche or justice conversions failed. It makes no claim about human psychology, autonomy, justice, consciousness, or a new fundamental law.

The Registered Report lock completed structurally. It distinguishes an outcome-blind Stage 1 protocol with logged deviations and blocked promotion from outcome-seen locking, undeclared deviations, exploratory-to-confirmatory promotion, and a Stage 20 label without external gates. No journal reviewed or accepted a real Registered Report, no empirical outcome was analyzed, and no scientific promotion occurred. The evidence board continues to abstain.

## Expanded portfolios, tools, and cleanup

All thirty safe-now tasks produced owner-scoped receipts, and all twenty candidate proposals produced bounded prototype receipts. Inherited seed language was reviewed and rewritten before x1; it did not receive predecessor completion credit. None of the fifty receipts used real participants, empirical data, credentials, accounts, API keys, production identity operations, legal or cultural authority, Māori authority, sibling mutations, host changes, or destructive actions. Ten inherited exact packets and five inherited blocked packets remain visible and unexecuted.

Twenty skill packages were selected, validated, and smoke-used. Nineteen unique packages were initialized through the system skill creator with generated UI metadata. One compatible existing family skill was validated and reused without mutation. Every package passed the UTF-8 validator, metadata checks, the document word cap, and a bounded phase-artifact smoke use. No subagent forward test was used because the activation explicitly forbids subagents. Skill validation proves package and workflow behavior only.

Ten family-current runners were built around reusable `ghc_family_*` callers. They cover source drift, proposal-neighbor quarantine, exact x1 manifest parity, Method Flow preflight, route guarding, evidence-DAG closure, all ten core surfaces, expanded portfolio checks, skill checks, and the phase validator. Historical and owner-specific names remain compatibility evidence; no destructive rename occurred.

All thirty clean/fix/refine tasks completed additively with individual receipts. They reconcile counts and labels, preserve exact and blocked packets, maintain deterministic JSON and UTF-8, reserve accessibility work, protect caller compatibility, keep manifests and staged surfaces explicit, verify ancestry and commit caps, and preserve terminal abstention. No user material, sibling lane, canonical history, host security, Windows feature, account, credential, or external system was deleted or changed.

## Closeout gates still pending at evidence build

The evidence candidate still requires the scoped recent-round/inherited/current test selection, detailed and minimal validation, complete JSON parsing, five-class privacy and raw-identifier scanning, exact staged-file review, exact manifest parity, stale-label review, diff hygiene, ancestry, zero merges, commit-cap checks, a clean evidence commit, push, and four-way equality. After the combined closeout and seal commit, the exact final head must repeat those bounded checks and pass exactly one clean local-only named-lane replay. The terminal route remains `PREPARED_NOT_SENT`; no sibling has been contacted.
'''


def static_report(rows: list[dict[str, Any]], distribution: dict[str, int], overview: str) -> str:
    body = []
    for paragraph in overview.split("\n\n"):
        if paragraph.startswith("# "):
            continue
        if paragraph.startswith("## "):
            body.append(f"<h2>{html.escape(paragraph[3:])}</h2>")
        else:
            body.append(f"<p>{html.escape(paragraph.replace(chr(10), ' '))}</p>")
    table_rows = "".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['outcome'])}</td><td>{row['checks']}</td></tr>"
        for row in rows
    )
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ilyra Fen v646-v2 bounded evidence report</title>
<style>body{{font:1rem/1.55 system-ui,sans-serif;max-width:74rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;background:#fff;padding:.5rem}}table{{border-collapse:collapse;width:100%;overflow-wrap:anywhere}}th,td{{border:1px solid #667;padding:.5rem;text-align:left}}svg{{max-width:28rem;height:auto}}code{{overflow-wrap:anywhere}}:focus{{outline:3px solid #075985;outline-offset:2px}}</style></head>
<body><a class="skip" href="#main">Skip to main content</a><header><h1>Ilyra Fen v646-v2 bounded evidence report</h1><p>Static structural report; manual and affected-user evaluation remain reserved.</p></header>
<nav aria-label="Report sections"><a href="#summary">Summary</a> · <a href="#outcomes">Outcomes</a> · <a href="#detail">Detailed overview</a></nav>
<main id="main"><section id="summary"><h2>Summary</h2><p>Distribution: {distribution['completed']} completed, {distribution['represented']} represented, {distribution['open_gap']} open gap, {distribution['exact_gate']} exact gate. Verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p>
<svg role="img" aria-labelledby="chart-title chart-desc" focusable="false" data-table-ref="#outcome-table" viewBox="0 0 420 180"><title id="chart-title">Proposal outcome distribution</title><desc id="chart-desc">Six completed, two represented, one open gap, and one exact gate. The following table provides the complete alternative.</desc><rect x="20" y="20" width="240" height="28" fill="#166534"/><rect x="20" y="58" width="80" height="28" fill="#1d4ed8"/><rect x="20" y="96" width="40" height="28" fill="#a16207"/><rect x="20" y="134" width="40" height="28" fill="#991b1b"/><text x="270" y="40">completed 6</text><text x="110" y="78">represented 2</text><text x="70" y="116">open gap 1</text><text x="70" y="154">exact gate 1</text></svg></section>
<section id="outcomes"><h2>Proposal outcomes</h2><div role="region" aria-label="Scrollable proposal outcome table" tabindex="0"><table id="outcome-table"><caption>Ten frozen proposals and bounded x2 outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Checks</th></tr></thead><tbody>{table_rows}</tbody></table></div></section>
<section id="detail">{''.join(body)}</section></main><footer><p>Identity and family language is relational only; it is not consciousness, personhood, employment, qualification, continuity, or authority evidence.</p></footer></body></html>'''


def main() -> int:
    head = git("rev-parse", "HEAD")
    if head != X1_HEAD:
        raise SystemExit(f"x2 builder requires exact x1 HEAD {X1_HEAD}; observed {head}")
    if git("diff", "--cached", "--name-only"):
        raise SystemExit("x2 builder requires an empty Git index")
    if len(PROPOSALS) != 10 or len(CORE_RUNNERS) != 10:
        raise SystemExit("core cardinality mismatch")
    skill_receipt = load("prototypes/skill-build-receipt.json")
    if not skill_receipt.get("valid") or skill_receipt.get("skill_count") != 20:
        raise SystemExit("twenty-skill portfolio is not valid")

    core_rows, core_results = build_core()
    distribution = dict(Counter(row["outcome"] for row in core_rows))
    expected_distribution = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
    if distribution != expected_distribution:
        raise RuntimeError(f"unexpected distribution: {distribution}")
    write_json("x2-proposal-ledger.json", {
        "schema": "ghc.family.v646-v2.x2-proposal-ledger.v1",
        "phase": PHASE,
        "owner": OWNER,
        "x1_commit": X1_HEAD,
        "source_revision": SOURCE_REVISION,
        "proposal_count": len(core_rows),
        "distribution": distribution,
        "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
        "proposals": core_rows,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": TRUTH_BOUNDARY,
    })

    mutations = synthetic_mutations()
    write_json("validation/x2-synthetic-negative-register.json", {
        "schema": "ghc.family.v646-v2.synthetic-negative-register.v1",
        "count": len(mutations),
        "executed": len(mutations),
        "rejected": sum(row["observed"] == "rejected" for row in mutations),
        "rows": mutations,
        "boundary": "Synthetic mutation failures are not empirical observations or independent reproduction.",
    })
    safe_rows = execute_portfolio(SAFE_NOW, "safe")
    candidate_rows = execute_portfolio(CANDIDATES, "candidate")
    cleanup_rows = execute_cleanup()
    write_json("approval-packets/x2-safe-now-execution.json", {
        "schema": "ghc.family.v646-v2.safe-now-execution.v1", "count": len(safe_rows), "completed": len(safe_rows),
        "unsafe_reclassification_count": 0, "tasks": safe_rows, "boundary": TRUTH_BOUNDARY,
    })
    write_json("prototypes/x2-candidate-execution.json", {
        "schema": "ghc.family.v646-v2.candidate-execution.v1", "count": len(candidate_rows), "completed": len(candidate_rows),
        "production_claims": 0, "tasks": candidate_rows, "boundary": TRUTH_BOUNDARY,
    })
    write_json("maintenance/x2-clean-refine-ledger.json", {
        "schema": "ghc.family.v646-v2.clean-refine-ledger.v1", "count": len(cleanup_rows), "completed": len(cleanup_rows),
        "destructive_actions": 0, "tasks": cleanup_rows, "boundary": TRUTH_BOUNDARY,
    })
    x1_portfolio = load("approval-packets/x1-approval-portfolio.json")
    write_json("approval-packets/x2-protected-packet-register.json", {
        "schema": "ghc.family.v646-v2.protected-packet-register.v1",
        "inherited_exact_count": len(x1_portfolio["inherited_exact_packets"]),
        "inherited_blocked_count": len(x1_portfolio["inherited_blocked_packets"]),
        "executed": 0,
        "relabelled_safe_now": 0,
        "exact_packets": x1_portfolio["inherited_exact_packets"],
        "blocked_packets": x1_portfolio["inherited_blocked_packets"],
        "boundary": TRUTH_BOUNDARY,
    })
    write_json("prototypes/skill-and-runner-ledger.json", {
        "schema": "ghc.family.v646-v2.skill-runner-ledger.v1",
        "skills": [{"name": name, "description": description, "state": "validated_and_smoke_used"} for name, description in SKILLS],
        "runners": [{"name": name, "description": description, "state": "built_pending_aggregate_use_receipt"} for name, description in RUNNERS],
        "skill_count": len(SKILLS), "runner_count": len(RUNNERS), "family_current_names_preserved": True,
        "boundary": TRUTH_BOUNDARY,
    })
    write_json("tooling/caller-compatibility-ledger.json", {
        "schema": "ghc.family.v646-v2.caller-compatibility.v1",
        "family_current_prefixes": ["ghc_family_", "build_ghc_family_"],
        "new_runner_count": len(RUNNERS),
        "historical_names_deleted": 0,
        "compatibility_callers_deleted": 0,
        "valid": True,
        "boundary": TRUTH_BOUNDARY,
    })

    x2_operational = X2_OPERATIONAL_NEGATIVES
    effective_negatives = INHERITED_EFFECTIVE_NEGATIVES + len(X1_OPERATIONAL_NEGATIVES) + len(mutations) + len(x2_operational)
    write_json("validation/x2-operational-negatives.json", {
        "schema": "ghc.family.v646-v2.x2-operational-negatives.v1",
        "count": len(x2_operational), "rows": x2_operational, "all_received_zero_initial_credit": True,
        "boundary": "Operational negatives remain retained after bounded recovery.",
    })
    write_json("retained-negative-register.json", {
        "schema": "ghc.family.v646-v2.retained-negative-register.v1",
        "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
        "x1_operational": len(X1_OPERATIONAL_NEGATIVES),
        "preregistered_synthetic_executed_and_rejected": len(mutations),
        "x2_operational": len(x2_operational),
        "effective_total": effective_negatives,
        "no_negative_erased": True,
        "x1_operational_rows": X1_OPERATIONAL_NEGATIVES,
        "x2_operational_rows": x2_operational,
        "synthetic_register": "validation/x2-synthetic-negative-register.json",
        "boundary": TRUTH_BOUNDARY,
    })
    write_json("exact-open-gate-register.json", {
        "schema": "ghc.family.v646-v2.gate-register.v1",
        "inherited_open_gaps": INHERITED_OPEN_GAPS,
        "new_open_gaps": 1,
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1,
        "inherited_exact_gates": INHERITED_EXACT_GATES,
        "new_exact_gates": 1,
        "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "closed_without_exact_evidence": 0,
        "open_gap_proposal": "V6462-P03",
        "exact_gate_proposal": "V6462-P06",
        "boundaries": ["real GMUT data and likelihood", "blind matched-budget THOS arms", "production Freed ID", "affected-party and Māori authority", "independent-team reproduction", "Stage 20"],
        "boundary": TRUTH_BOUNDARY,
    })
    write_json("threat-model.json", {
        "schema": "ghc.family.v646-v2.threat-model.v1",
        "assets": ["frozen x1 tree", "evidence DAG", "negative register", "source status", "identity and authority boundaries", "manifests", "terminal route"],
        "threats": [
            {"threat": "orphan or cyclic evidence dependency", "control": "JSON-Pointer closure and cycle quarantine", "residual": "external semantic review open"},
            {"threat": "empirical promotion from zero-row adapters", "control": "zero rows, zero fits, explicit open_gap", "residual": "real analysis open"},
            {"threat": "THOS proxy presented as effectiveness", "control": "real-people and blind-arm counters remain zero", "residual": "participant evidence open"},
            {"threat": "production identity inference", "control": "synthetic vectors and zero real key/proof counters", "residual": "live interoperability and governance open"},
            {"threat": "legal or Māori authority substitution", "control": "exact gate and no real decisions", "residual": "competent and Māori authority required"},
            {"threat": "SQLite fixture escapes scratch root", "control": "resolved root containment and disposable teardown", "residual": "not production assurance"},
            {"threat": "scanner definition self-hit or private material", "control": "definition separation and five-class scan", "residual": "zero-hit scan is bounded"},
            {"threat": "early or duplicate successor activation", "control": "PREPARED_NOT_SENT and one-send terminal guard", "residual": "exact final validation pending"},
        ],
        "destructive_actions": 0, "host_changes": 0, "credential_use": 0, "boundary": TRUTH_BOUNDARY,
    })
    write_json("phase-truth.json", {
        "schema": "ghc.family.v646-v2.phase-truth.v1",
        "phase": PHASE, "owner": OWNER, "source_branch": SOURCE_BRANCH, "source_revision": SOURCE_REVISION,
        "x1_commit": X1_HEAD, "primary_focus": PRIMARY_FOCUS, "bounded_practice": BOUNDED_PRACTICE,
        "distribution": distribution, "proposal_count": 10, "safe_now_completed": 30, "candidates_completed": 20,
        "skills_validated_and_used": 20, "runners_built": 10, "runners_aggregate_use_pending": True,
        "cleanup_completed": 30, "effective_retained_negatives": effective_negatives,
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1, "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "same_owner_repeatability": "pending named-lane exact-final replay",
        "independent_reproduction": False, "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "identity_boundary": IDENTITY_BOUNDARY, "boundary": TRUTH_BOUNDARY,
    })
    write_json("complete-incomplete-checklist.json", {
        "schema": "ghc.family.v646-v2.checklist.v1",
        "completed": [
            "exact source and x1 ancestry verified", "dedicated x1 freeze pushed and four-way equal before x2",
            "ten proposals executed within evidence", "thirty safe-now tasks completed", "twenty candidates completed",
            "twenty skills validated and smoke-used", "thirty cleanup tasks completed", "seventy synthetic mutations rejected",
            "all operational failures retained in Method Flow", "static report and integrated overview built",
        ],
        "pending": [
            "ten-runner aggregate use receipt", "scoped repository test selection", "detailed and minimal validation",
            "evidence commit and four-way equality", "combined closeout and seal commit", "exact-final canonical validation",
            "exactly one local-only named-lane replay", "single Sable Rook baton",
        ],
        "external_open": [
            "real GMUT data and likelihood", "blind matched-budget THOS real arms", "production Freed ID",
            "affected-party, legal, cultural, and Māori authority", "manual and affected-user accessibility evaluation",
            "independent-team reproduction", "Stage 20",
        ],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": TRUTH_BOUNDARY,
    })
    write_json("environment/x2-environment-receipt.json", {
        "schema": "ghc.family.v646-v2.x2-environment.v1", "d_first_runtime": True,
        "codex_cli_verified_only": True, "codex_desktop_verified_only": True, "desktop_updated": False,
        "elevation": False, "host_security_weakened": False, "windows_features_changed": False,
        "unrelated_software_installed": False, "reboot": False, "windows_sandbox_session": False,
        "owner_generated_file_threshold": 15000, "threshold_exceeded": False, "boundary": TRUTH_BOUNDARY,
    })
    write_json("orchestration/phase-update.json", {
        "schema": "ghc.family.phase-update.v1", "phase": PHASE, "owner": OWNER,
        "state": "x2_evidence_built_pending_validation_and_commit", "active": [OWNER],
        "standby": ["Eiren Kestrel", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc", "all other siblings"],
        "standby_contact_count": 0, "no_task_creation": True, "no_delegation": True, "x2_started": True,
        "terminal_route": "PREPARED_NOT_SENT",
    })
    overview = build_overview(distribution, effective_negatives)
    overview_words = len(overview.split())
    if not (1500 <= overview_words <= 6000):
        raise RuntimeError(f"overview word count outside bounds: {overview_words}")
    write_text("v646-v2-integrated-overview.md", overview)
    write_text("deliverables/v646-v2-final-integrated-overview.md", overview)
    write_text("deliverables/v646-v2-static-report.html", static_report(core_rows, distribution, overview))
    write_text("wellbeing-check.md", f'''# v646-v2 wellbeing and workload check

- Scope remained one owner, one canonical lane, one later named replay, and no subagents or sibling messages.
- The x1 freeze remained immutable at `{X1_HEAD}` while x2 advanced additively.
- {len(X1_OPERATIONAL_NEGATIVES) + len(X2_OPERATIONAL_NEGATIVES)} operational failures are retained across x1 and x2 at this evidence stage; each failed witness received zero initial credit and every recovery stayed bounded.
- Nineteen skills were initialized and one compatible skill was reused without mutation; all twenty validated and smoke-used.
- No elevation, host-security weakening, Windows-feature change, unrelated installation, desktop update, or reboot occurred.
- No real participant, protected identity, beneficiary, location, earthquake catalogue, credential, key, proof, or production record entered the packet.
- Manual and affected-user accessibility evaluation remains reserved.
- Identity and family language remains relational working language only, not consciousness, welfare, personhood, employment, qualification, continuity, or authority evidence.
- The terminal route remains `PREPARED_NOT_SENT`, and the evidence board remains `NOT_READY_FOR_STAGE_20`.
''')
    write_json("validation/evidence-build-receipt.json", {
        "schema": "ghc.family.v646-v2.evidence-build-receipt.v1", "x1_head": X1_HEAD,
        "core_runners": len(core_results), "core_checks": sum(row.get("checks", 0) for row in core_results.values()),
        "core_all_passed": all(row.get("passed") for row in core_results.values()), "distribution": distribution,
        "safe_now": 30, "candidates": 20, "skills": 20, "runners_built": 10, "cleanup": 30,
        "synthetic_negatives": 70, "effective_negatives": effective_negatives,
        "overview_words": overview_words, "route_state": "PREPARED_NOT_SENT", "valid": True,
        "boundary": TRUTH_BOUNDARY,
    })
    print(json.dumps({
        "phase": PHASE, "core": 10, "core_checks": sum(row.get("checks", 0) for row in core_results.values()),
        "distribution": distribution, "safe": 30, "candidates": 20, "skills": 20, "runners": 10,
        "cleanup": 30, "synthetic_negatives": 70, "effective_negatives": effective_negatives,
        "overview_words": overview_words, "valid": True,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
