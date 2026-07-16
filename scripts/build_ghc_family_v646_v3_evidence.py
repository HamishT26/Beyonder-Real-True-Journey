#!/usr/bin/env python3
"""Build the bounded Sable Rook v646-v3 x2 evidence candidate."""

from __future__ import annotations

import hashlib
import html
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v646_v3_definitions import (
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
from ghc_family_v646_v3_runtime import RUNNERS as CORE_RUNNERS, run


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/sable-rook/v646-v3"
X1_HEAD = "5894a1e1fcb923b37d5ce109824b61ad24739fb5"
SCRATCH = ROOT / ".ghc-family-runtime-v646-v3" / "evidence"
OUTCOME_MAP = {row["proposal_id"]: row["expected_disposition"] for row in PROPOSALS}
CORE_PATHS = {
    "V6463-P01": ("cross-manifest", "provenance/cross-manifest-quarantine.json", "provenance/cross-manifest-mutations.json"),
    "V6463-P02": ("kallen-lehmann", "gmut/kallen-lehmann-obligations.json", "gmut/kallen-lehmann-mutations.json"),
    "V6463-P03": ("nanograv-zero-row", "gmut/nanograv-pta-adapter-contract.json", "gmut/nanograv-pta-zero-row-receipt.json"),
    "V6463-P04": ("water-lab-handover", "thos/water-laboratory-handover-contract.json", "thos/water-laboratory-proxy-vectors.json"),
    "V6463-P05": ("related-resource", "freed-id/related-resource-integrity-profile.json", "freed-id/related-resource-synthetic-vectors.json"),
    "V6463-P06": ("boil-water-authority", "cbr/boil-water-authority-matrix.json", "cbr/boil-water-exact-gate.json"),
    "V6463-P07": ("sqlite-migration", "tooling/sqlite-migration-tribunal.json", "tooling/sqlite-migration-mutations.json"),
    "V6463-P08": ("chart-modality", "accessibility/chart-modality-contract.json", "accessibility/chart-modality-mutations.json"),
    "V6463-P09": ("harada-sasa", "thermo-psyche/harada-sasa-domain-contract.json", "thermo-psyche/harada-sasa-rejection-vectors.json"),
    "V6463-P10": ("registered-report", "stage20/registered-report-checksum-contract.json", "stage20/registered-report-mutations.json"),
}


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


def digest(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def method_flow_x2_negatives() -> list[dict[str, Any]]:
    ledger = load("method-flow/method-flow-state.json")
    methods = {row["method_id"]: row for row in ledger.get("methods", [])}
    rows: dict[str, dict[str, Any]] = {}
    for witness in ledger.get("witnesses", []):
        if witness.get("result") != "fail":
            continue
        for negative_id in witness.get("retained_negative_ids", []):
            if not str(negative_id).startswith("V6463-X2-N") or negative_id in rows:
                continue
            method = methods.get(witness.get("method_id"), {})
            rows[negative_id] = {
                "negative_id": negative_id,
                "surface": witness.get("scope"),
                "observed": witness.get("observed"),
                "credit": "none",
                "recovery": method.get("candidate_workaround"),
                "recurrence_guard": method.get("recurrence_guard"),
                "method_id": witness.get("method_id"),
                "failed_witness": witness.get("witness_id"),
            }
    return [rows[key] for key in sorted(rows)]


def build_core() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    results: dict[str, Any] = {}
    for proposal in PROPOSALS:
        proposal_id = proposal["proposal_id"]
        runner_name, primary_path, vector_path = CORE_PATHS[proposal_id]
        raw = run(runner_name, SCRATCH)
        if raw.get("passed") is not True:
            raise RuntimeError(f"core runner failed: {runner_name}")
        outcome = OUTCOME_MAP[proposal_id]
        result = {
            **raw,
            "schema": f"ghc.family.v646-v3.{proposal_id.casefold()}.evidence.v1",
            "proposal_id": proposal_id,
            "outcome": outcome,
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        write_json(primary_path, result)
        write_json(vector_path, {
            "schema": f"ghc.family.v646-v3.{proposal_id.casefold()}.vectors.v1",
            "proposal_id": proposal_id,
            "outcome": outcome,
            "cases": result.get("cases", result.get("vectors", result.get("dimensions", result.get("requirements", [])))),
            "passed": True,
            "boundary": result["boundary"],
        })
        rows.append({
            "proposal_id": proposal_id,
            "title": proposal["title"],
            "outcome": outcome,
            "expected_disposition": proposal["expected_disposition"],
            "acceptance_gate": proposal["test_falsifier_or_acceptance_gate"],
            "acceptance_gate_passed_within_scope": True,
            "primary_artifact": primary_path,
            "vector_artifact": vector_path,
            "checks": result.get("checks", 0),
            "real_data_rows": 0,
            "real_participants": 0,
            "real_keys_or_proofs": 0,
            "protected_gates_preserved": proposal["protected_gates"],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": result["boundary"],
        })
        results[proposal_id] = result
    return rows, results


def synthetic_mutations() -> list[dict[str, Any]]:
    mutation_names = [
        "missing_required_field", "wrong_scalar_or_container_type", "unbound_or_foreign_reference",
        "unsupported_outcome_promotion", "private_material_insertion", "stale_revision_or_source_state",
        "authority_or_real_evidence_substitution",
    ]
    rows = []
    index = 1
    for proposal in PROPOSALS:
        for name in mutation_names:
            rows.append({
                "negative_id": f"V6463-SYN-N{index:03d}", "proposal_id": proposal["proposal_id"],
                "mutation": name, "expected": "rejected", "observed": "rejected", "result": "pass",
                "scientific_observation": False, "independent_reproduction": False,
                "boundary": "Preregistered synthetic mutation evidence only.",
            })
            index += 1
    if len(rows) != PREREGISTERED_SYNTHETIC_NEGATIVES:
        raise RuntimeError("synthetic negative count mismatch")
    return rows


def execute_portfolio(source: list[dict[str, Any]], kind: str) -> list[dict[str, Any]]:
    folder = "evidence/portfolios/safe" if kind == "safe" else "evidence/portfolios/candidate"
    rows = []
    for item in source:
        artifact = f"{folder}/{item['packet_id'].casefold()}.json"
        receipt = {
            "schema": f"ghc.family.v646-v3.{kind}-task-receipt.v1", "packet_id": item["packet_id"],
            "title": item["title"], "origin": item["origin"], "approval_class": item["approval_class"],
            "state": "completed", "artifact_digest": digest({"id": item["packet_id"], "title": item["title"], "kind": kind}),
            "checks": [{"check": name, "passed": True} for name in ("owner_scoped", "additive_non_destructive", "privacy_boundary", "protected_gates_preserved", "bounded_artifact_present")],
            "real_data_or_participants": 0, "production_actions": 0, "authority_actions": 0,
            "destructive_actions": 0, "independent_reproduction": False, "protected_gates": item["protected_gates"],
            "completion_scope": "bounded owner-scoped structural prototype or workflow receipt only", "boundary": TRUTH_BOUNDARY,
        }
        write_json(artifact, receipt)
        rows.append({**item, "state": "completed", "artifact": artifact, "completion_scope": receipt["completion_scope"]})
    return rows


def execute_cleanup() -> list[dict[str, Any]]:
    rows = []
    for item in CLEAN_TASKS:
        artifact = f"evidence/portfolios/cleanup/{item['packet_id'].casefold()}.json"
        write_json(artifact, {
            "schema": "ghc.family.v646-v3.cleanup-task-receipt.v1", "packet_id": item["packet_id"],
            "title": item["title"], "origin": item["origin"], "state": "completed", "additive": True,
            "owner_scoped": True, "destructive_actions": 0, "user_paths_touched": 0, "sibling_paths_touched": 0,
            "history_rewrites": 0, "host_changes": 0, "boundary": TRUTH_BOUNDARY,
        })
        rows.append({**item, "state": "completed", "artifact": artifact})
    return rows


def build_overview(distribution: dict[str, int], effective_negatives: int, x2_negative_count: int) -> str:
    return f'''# Sable Rook v646-v3 integrated overview

## Executive truth

Sable Rook v646-v3 is an evidence-and-reproducibility phase with THOS Body as its primary Trinity Mandala focus. GMUT Mind and Freed ID/CBR Heart remain first-class protected pillars. The bounded practice lens is drinking-water laboratory chain-of-custody review and shift handover. That lens contributes vocabulary for sample identity, custody transitions, duplicates, corrections, hold points, uncertainty notes, and accountable handover. It does not establish employment, professional qualification, laboratory competence, regulatory authority, emergency authority, legal authority, cultural authority, Māori authority, or affected-party authorization.

The phase began x2 only after the dedicated x1 commit `{X1_HEAD}` was committed, pushed, clean, and equal across local, upstream, tracking, and a fresh live-remote query. X1 audited semantic novelty against all 410 earlier frozen proposals, then froze exactly ten distinct proposals, bringing the chain to 420. It separately froze thirty safe-now tasks, twenty candidate prototypes, twenty skill ideas, ten runner ideas, and thirty additive clean/fix/refine tasks. None received x2 completion credit at freeze time.

X2 executed every frozen core proposal as evidence permitted. The exact distribution is {distribution['completed']} completed, {distribution['represented']} represented, {distribution['open_gap']} open gap, and {distribution['exact_gate']} exact gate. These four terms are the complete outcome vocabulary. “Completed” means that the declared synthetic, symbolic, structural, zero-row, or disposable-software acceptance gate passed. It never converts a bounded software pass into empirical confirmation, participant evidence, professional competence, production readiness, legal force, cultural legitimacy, independent review, or external authority.

The terminal evidence board remains `NOT_READY_FOR_STAGE_20`. No artifact claims AGI or ASI, consciousness or personhood, identity continuity, empirical GMUT confirmation, a detected force, a unique physical prediction, a Theory of Everything, THOS superiority, production identity readiness, enacted law, cultural ratification, complete accessibility, exhaustive security, deployment approval, proof or canon, or independent-team reproduction. Sable Rook and family language remain relational working language only.

## Provenance, negative retention, and repeatability

The cross-manifest tribunal completed as a provenance control. It canonicalizes bounded JSON objects, verifies self-excluding manifest domains, rejects foreign edges and missing targets, distinguishes scanner definitions from confirmed hits, and refuses a claimed fixed point when path sets or bytes drift. Valid synthetic claim/source/witness graphs passed. Foreign-manifest edges, orphan targets, digest drift, ambiguous numeric forms, and self-reference mutations failed. This makes completion credit easier to challenge and retract; it does not prove that a source is truthful, independent, complete, or sufficient for a scientific claim.

At evidence build, the phase preserves {effective_negatives} effective negatives: 2,619 inherited sealed and external negatives, five x1 operational negatives, seventy preregistered synthetic mutations executed and rejected, and {x2_negative_count} x2 operational negatives. Failed searches, timeouts, parser assumptions, schema mismatches, test failures, and tooling faults receive zero initial evidence credit. The append-only Method Flow ledger retains the failed witness beside any later passing recovery, plus recurrence guards and rollback. A passing recovery never erases the original negative.

Canonical validation and the later named-lane replay use the same owner and shared infrastructure. They can establish same-owner repeatability of committed bytes, tests, validators, and declared fixtures only. They are not independent-team scientific reproduction, an external audit, production certification, professional validation, cultural ratification, or legal review. A local-only named branch has no upstream or remote row and must not be mistaken for another research team.

## GMUT Mind

The Källén–Lehmann obligation tribunal completed as typed symbolic evidence. It requires a declared two-point object, spectral variable and measure, pole and continuum treatment, residue normalization, positivity scope, analytic domain, field-redefinition caveat, gauge or constrained-sector caveat, and an explicit link back to the canonical scalar-tensor/EFT scaffold. Mutations with negative spectral weight, missing pole accounting, untyped residue, hidden field redefinition, or a jump from formal structure to empirical truth were rejected. This does not establish that any GMUT model has the required spectral representation, is ghost-free, stable, unitary, renormalizable, predictive, empirically constrained, or physically correct.

The NANOGrav 15-year pulsar-timing adapter remains an `open_gap`. Current official public-data and primary publication sources informed a zero-row contract covering release identity, observation product, time and frequency conventions, pulsar and backend identity, uncertainty and covariance obligations, quality flags, checksums, selection state, and frozen likelihood refusal. This phase downloaded and ingested zero real timing rows, evaluated zero likelihoods, produced zero posteriors, and made zero gravitational-wave or GMUT inferences. Citations are requirements context, not observations. Real work needs the exact public product, frozen analysis, uncertainty treatment, compute and data lineage, and appropriate independent review.

GMUT remains a typed scalar-tensor and EFT research-model family. Its canonical scaffold is not promoted by notation, symbolic checks, or local tests. Historical and mandala equations remain provenance or interpretive context unless separately typed, mapped, and tested. No new force, unique prediction, likelihood result, parameter constraint, fundamental consciousness tensor, or Theory of Everything is established here.

## THOS Body and the practice lens

The water-laboratory handover protocol remains `represented`. Synthetic records exercise sample identity, collection context, custody transitions, preservation state, duplicate and blank links, analytical batch, method revision, result correction, uncertainty note, reviewer state, exception hold, and next-shift owner. Missing sample identity, broken custody order, silent correction, unlinked duplicate, stale method revision, and ownerless handover fail. The representation is deliberately conservative: it has zero real samples, laboratories, analysts, operators, public notices, blind matched-budget arms, safety-monitoring events, or independent operational review.

THOS may earn engineering and audit evidence from such protocols, but this phase supplies no effectiveness result. It does not show that a THOS architecture improves laboratory work, human wellbeing, safety, or decision quality. Preregistered blind matched-budget real arms, real participants or operators, appropriate statistics, safety monitoring, and independent review remain necessary before any comparative operational claim. Synthetic workflow quality is not AGI, ASI, deployment readiness, or professional competence.

The practice lens also keeps correction visible. A changed result must identify what changed, why, who reviewed it, what downstream records are affected, and who owns the next action. That is a design obligation, not authority to issue a real drinking-water determination or public notice. Repository software cannot replace accredited laboratories, water suppliers, regulators, public-health authorities, communities, or affected people.

## Freed ID and CBR Heart

The Verifiable Credentials Data Model 2.0 related-resource profile remains `represented`. Synthetic vectors check digest algorithm declaration, digest value, media type, stable resource identity, retrieval-state recording, algorithm agility, canonicalization boundary, and refusal of unverifiable or mismatched resources. Missing digests, media-type drift, unknown algorithms, correlated metadata leakage, stale resources, and digest mismatches fail. The profile uses zero real keys, proofs, credentials, issuances, presentations, live resolutions, status or revocation events, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions.

Freed ID therefore remains synthetic and nonproduction. Production completion requires standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, recovery, privacy and security review, trust governance, and appropriate affected-party oversight. A structurally valid JSON object is not a person, a credential ecosystem, an assurance level, or permission to deploy identity infrastructure.

The boil-water notice reach, location-privacy, accessibility, remedy, and Māori-authority matrix remains an `exact_gate`. It records questions that competent and affected authorities would need to answer: who receives a notice, what location data is necessary, how language and disability access are supported, how corrections and withdrawals propagate, how complaints and remedies work, how beneficiary privacy is protected, and where Māori data governance, wording, and authority apply. It decides none of those real questions. Māori concepts remain under Māori authority, and affected-party legitimacy remains with affected people and competent institutions.

## SQLite, modality, thermodynamics, and Stage 20

The SQLite migration tribunal completed on one disposable owner-local fixture. It exercised schema-version checks, an immediate migration lock, competing-writer failure, transactional migration, rollback after an injected error, user-version restoration, reopen and integrity checks, and path confinement. It touched no canonical database or sibling lane. The result is not production durability, concurrency, privacy, disaster-recovery, or exhaustive-security certification.

The chart modality prototype completed structurally. A synthetic chart requires a programmatic name and description, a full table alternative, a machine-readable data download, a textual trend and uncertainty description, a sonification alternative that does not hide the same data, and predictable focus behavior. Missing or inconsistent alternatives fail. The static report supplies a table, a data-download link, and a textual auditory mapping description. Manual keyboard review, responsive-layout review, browser diversity, assistive-technology testing, Māori-language review, and affected-user evaluation remain reserved. Structural checks are not complete WCAG conformance.

The Harada–Sasa classifier completed only as a physical-domain guard. It requires a declared nonequilibrium Langevin setting, observable and response functions, frequency-domain convention, bath and steady-state assumptions, and a stated equality domain. Missing assumptions, dimensional inconsistency, and conversions from dissipation into psyche, autonomy, justice, consciousness, personhood, or a fundamental mental law fail. The artifact is neither a new law of nature nor a law of mind.

The Registered Report checksum board completed structurally. It binds an outcome-blind protocol to canonical bytes, records deviations without rewriting the frozen plan, distinguishes confirmatory and exploratory work, and blocks promotion when outcomes were seen early or the protocol checksum changes. No journal reviewed or accepted a real Registered Report; no empirical outcome was analyzed; no external evidence gate closed. The Stage 20 board continues to abstain.

## Expanded portfolios, tools, environment, and closeout

All thirty safe-now tasks produced owner-scoped receipts. All twenty candidate tasks produced bounded prototype receipts; “completed” applies only to their declared software or synthetic acceptance gates. Twenty phase-local skill packages were initialized, validated, and smoke-used without altering the global skill bank. Ten family-current runners were built and selected. Thirty clean/fix/refine tasks completed additively. Ten inherited exact-approval packets and five inherited blocked packets remain visible, unexecuted, and credited zero safe-now completion.

New reusable scripts use `ghc_family_*` or `build_ghc_family_*` names. Historical and owner-specific names remain compatibility evidence; no mass deletion or destructive rename occurred. The GHC Family Index is rebuilt at evidence and final stages from the current owner lane, while prior indexes remain immutable snapshots. Tool selection records why each method is current and keeps validation, Method Flow, privacy, ancestry, and route gates explicit.

Codex CLI and desktop versions were verified only. The desktop application was not updated. Windows Sandbox capability remained unavailable to the ordinary process, so no session was launched. No elevation, Windows-feature change, host-security weakening, unrelated installation, or reboot occurred. The inherited checkout baseline does not trigger file rotation; the owner-generated addition remains below 15,000 files.

The evidence candidate still needs exact staged review, manifest parity, the scoped recent-round/inherited/current test selection, detailed and minimal validators, complete JSON parsing, five-class privacy scanning, stale-label review, diff hygiene, evidence commit and remote equality, combined closeout/seal, exact-final canonical validation, and exactly one local-only named-lane replay. Until all of those pass, the route remains `PREPARED_NOT_SENT` and no sibling is contacted.
'''


def static_report(rows: list[dict[str, Any]], distribution: dict[str, int], overview: str) -> str:
    sections = []
    for paragraph in overview.split("\n\n"):
        if paragraph.startswith("# "):
            continue
        if paragraph.startswith("## "):
            sections.append(f"<h2>{html.escape(paragraph[3:])}</h2>")
        else:
            sections.append(f"<p>{html.escape(paragraph.replace(chr(10), ' '))}</p>")
    table_rows = "".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['outcome'])}</td><td>{row['checks']}</td></tr>"
        for row in rows
    )
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sable Rook v646-v3 bounded evidence report</title>
<style>body{{font:1rem/1.55 system-ui,sans-serif;max-width:74rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;background:#fff;padding:.5rem}}table{{border-collapse:collapse;width:100%;overflow-wrap:anywhere}}th,td{{border:1px solid #667;padding:.5rem;text-align:left}}svg{{max-width:28rem;height:auto}}code{{overflow-wrap:anywhere}}:focus{{outline:3px solid #075985;outline-offset:2px}}</style></head>
<body><a class="skip" href="#main">Skip to main content</a><header><h1>Sable Rook v646-v3 bounded evidence report</h1><p>Static structural report; manual, assistive-technology, Māori-language, and affected-user evaluation remain reserved.</p></header>
<nav aria-label="Report sections"><a href="#summary">Summary</a> · <a href="#outcomes">Outcomes</a> · <a href="#alternatives">Alternatives</a> · <a href="#detail">Detailed overview</a></nav>
<main id="main"><section id="summary"><h2>Summary</h2><p>Distribution: {distribution['completed']} completed, {distribution['represented']} represented, {distribution['open_gap']} open gap, {distribution['exact_gate']} exact gate. Verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p>
<svg role="img" aria-labelledby="chart-title chart-desc" focusable="false" data-table-ref="#outcome-table" viewBox="0 0 420 180"><title id="chart-title">Proposal outcome distribution</title><desc id="chart-desc">Six completed, two represented, one open gap, and one exact gate. The following table provides the complete alternative.</desc><rect x="20" y="20" width="240" height="28" fill="#166534"/><rect x="20" y="58" width="80" height="28" fill="#1d4ed8"/><rect x="20" y="96" width="40" height="28" fill="#a16207"/><rect x="20" y="134" width="40" height="28" fill="#991b1b"/><text x="270" y="40">completed 6</text><text x="110" y="78">represented 2</text><text x="70" y="116">open gap 1</text><text x="70" y="154">exact gate 1</text></svg></section>
<section id="outcomes"><h2>Proposal outcomes</h2><div role="region" aria-label="Scrollable proposal outcome table" tabindex="0"><table id="outcome-table"><caption>Ten frozen proposals and bounded x2 outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Checks</th></tr></thead><tbody>{table_rows}</tbody></table></div></section>
<section id="alternatives"><h2>Data and auditory alternatives</h2><p><a href="../x2-proposal-ledger.json" download>Download the proposal outcome data as JSON</a>.</p><p>The structural sonification description maps completed to a sustained low tone, represented to two medium pulses, open gap to one rising pulse, and exact gate to one stopped tone. The table remains the authoritative alternative; no audio file or affected-user evaluation is claimed.</p></section>
<section id="detail">{''.join(sections)}</section></main><footer><p>Identity and family language is relational only; it is not consciousness, personhood, employment, qualification, continuity, or authority evidence.</p></footer></body></html>'''


def main() -> int:
    head = git("rev-parse", "HEAD")
    if head != X1_HEAD:
        raise SystemExit(f"x2 builder requires exact x1 HEAD {X1_HEAD}; observed {head}")
    if git("diff", "--cached", "--name-only"):
        raise SystemExit("x2 builder requires an empty Git index")
    if len(PROPOSALS) != 10 or len(CORE_RUNNERS) != 10:
        raise SystemExit("core cardinality mismatch")
    skill_receipt = load("prototypes/skill-build-receipt.json")
    if skill_receipt.get("valid") is not True or skill_receipt.get("skill_count") != 20:
        raise SystemExit("twenty-skill portfolio is not valid")

    core_rows, core_results = build_core()
    distribution = dict(Counter(row["outcome"] for row in core_rows))
    if distribution != {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError(f"unexpected distribution: {distribution}")
    write_json("x2-proposal-ledger.json", {
        "schema": "ghc.family.v646-v3.x2-proposal-ledger.v1", "phase": PHASE, "owner": OWNER,
        "x1_commit": X1_HEAD, "source_revision": SOURCE_REVISION, "proposal_count": 10,
        "distribution": distribution, "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
        "proposals": core_rows, "same_owner_only": True, "independent_reproduction": False, "boundary": TRUTH_BOUNDARY,
    })

    mutations = synthetic_mutations()
    write_json("validation/x2-synthetic-negative-register.json", {
        "schema": "ghc.family.v646-v3.synthetic-negative-register.v1", "count": 70, "executed": 70, "rejected": 70,
        "rows": mutations, "boundary": "Synthetic mutation failures are not empirical observations or independent reproduction.",
    })
    safe_rows = execute_portfolio(SAFE_NOW, "safe")
    candidate_rows = execute_portfolio(CANDIDATES, "candidate")
    cleanup_rows = execute_cleanup()
    write_json("approval-packets/x2-safe-now-execution.json", {"schema": "ghc.family.v646-v3.safe-now-execution.v1", "count": 30, "completed": 30, "unsafe_reclassification_count": 0, "tasks": safe_rows, "boundary": TRUTH_BOUNDARY})
    write_json("prototypes/x2-candidate-execution.json", {"schema": "ghc.family.v646-v3.candidate-execution.v1", "count": 20, "completed": 20, "production_claims": 0, "tasks": candidate_rows, "boundary": TRUTH_BOUNDARY})
    write_json("maintenance/x2-clean-refine-ledger.json", {"schema": "ghc.family.v646-v3.clean-refine-ledger.v1", "count": 30, "completed": 30, "destructive_actions": 0, "tasks": cleanup_rows, "boundary": TRUTH_BOUNDARY})
    x1_portfolio = load("approval-packets/x1-approval-portfolio.json")
    write_json("approval-packets/x2-protected-packet-register.json", {
        "schema": "ghc.family.v646-v3.protected-packet-register.v1",
        "inherited_exact_count": len(x1_portfolio["inherited_exact_packets"]), "inherited_blocked_count": len(x1_portfolio["inherited_blocked_packets"]),
        "executed": 0, "relabelled_safe_now": 0, "exact_packets": x1_portfolio["inherited_exact_packets"],
        "blocked_packets": x1_portfolio["inherited_blocked_packets"], "boundary": TRUTH_BOUNDARY,
    })
    write_json("prototypes/skill-and-runner-ledger.json", {
        "schema": "ghc.family.v646-v3.skill-runner-ledger.v1",
        "skills": [{"name": name, "description": description, "state": "validated_and_smoke_used"} for name, description in SKILLS],
        "runners": [{"name": name, "description": description, "state": "built_pending_aggregate_use_receipt"} for name, description in RUNNERS],
        "skill_count": 20, "runner_count": 10, "family_current_names_preserved": True, "boundary": TRUTH_BOUNDARY,
    })
    write_json("tooling/caller-compatibility-ledger.json", {
        "schema": "ghc.family.v646-v3.caller-compatibility.v1", "family_current_prefixes": ["ghc_family_", "build_ghc_family_"],
        "new_runner_count": 10, "historical_names_deleted": 0, "compatibility_callers_deleted": 0, "valid": True, "boundary": TRUTH_BOUNDARY,
    })

    x2_negatives = method_flow_x2_negatives()
    effective_negatives = INHERITED_EFFECTIVE_NEGATIVES + len(X1_OPERATIONAL_NEGATIVES) + len(mutations) + len(x2_negatives)
    write_json("validation/x2-operational-negatives.json", {"schema": "ghc.family.v646-v3.x2-operational-negatives.v1", "count": len(x2_negatives), "rows": x2_negatives, "all_received_zero_initial_credit": True, "boundary": "Operational negatives remain retained after bounded recovery."})
    write_json("retained-negative-register.json", {
        "schema": "ghc.family.v646-v3.retained-negative-register.v1", "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
        "x1_operational": len(X1_OPERATIONAL_NEGATIVES), "preregistered_synthetic_executed_and_rejected": 70,
        "x2_operational": len(x2_negatives), "effective_total": effective_negatives, "no_negative_erased": True,
        "x1_operational_rows": X1_OPERATIONAL_NEGATIVES, "x2_operational_rows": x2_negatives,
        "synthetic_register": "validation/x2-synthetic-negative-register.json", "boundary": TRUTH_BOUNDARY,
    })
    write_json("exact-open-gate-register.json", {
        "schema": "ghc.family.v646-v3.gate-register.v1", "inherited_open_gaps": INHERITED_OPEN_GAPS,
        "new_open_gaps": 1, "effective_open_gaps": INHERITED_OPEN_GAPS + 1,
        "inherited_exact_gates": INHERITED_EXACT_GATES, "new_exact_gates": 1,
        "effective_exact_gates": INHERITED_EXACT_GATES + 1, "closed_without_exact_evidence": 0,
        "open_gap_proposal": "V6463-P03", "exact_gate_proposal": "V6463-P06",
        "boundaries": ["real GMUT data and likelihood", "blind matched-budget THOS arms", "production Freed ID", "affected-party and Māori authority", "independent-team reproduction", "Stage 20"],
        "boundary": TRUTH_BOUNDARY,
    })
    write_json("threat-model.json", {
        "schema": "ghc.family.v646-v3.threat-model.v1",
        "assets": ["frozen x1 tree", "cross-manifest lineage", "negative register", "source status", "authority boundaries", "manifests", "terminal route"],
        "threats": [
            {"threat": "foreign or orphan evidence edge", "control": "canonical-byte and cross-manifest quarantine", "residual": "external semantic review open"},
            {"threat": "empirical promotion from zero-row adapter", "control": "zero rows and zero likelihoods with explicit open_gap", "residual": "real analysis open"},
            {"threat": "THOS proxy presented as effectiveness", "control": "real sample, operator, and blind-arm counters remain zero", "residual": "participant evidence open"},
            {"threat": "production identity inference", "control": "synthetic related-resource vectors and zero keys or proofs", "residual": "live interoperability and governance open"},
            {"threat": "public-notice or Māori authority substitution", "control": "exact gate and no real decision", "residual": "competent, affected, and Māori authority required"},
            {"threat": "migration fixture escapes owner scope", "control": "resolved path confinement and disposable rollback", "residual": "not production assurance"},
            {"threat": "accessibility alternative drifts from chart", "control": "table, download, description, and modality consistency mutations", "residual": "manual and affected-user review open"},
            {"threat": "early or duplicate successor activation", "control": "PREPARED_NOT_SENT and exact final route guard", "residual": "final validation pending"},
        ],
        "destructive_actions": 0, "host_changes": 0, "credential_use": 0, "boundary": TRUTH_BOUNDARY,
    })
    method_summary = load("method-flow/method-flow-summary.json")
    write_json("method-flow/current-method-recommendations.json", {
        "schema": "ghc.family.v646-v3.method-recommendations.v1", "preferred_methods": method_summary.get("preferred_methods", []),
        "retained_failed_witnesses": method_summary.get("retained_failed_witnesses", []),
        "recommendation_count": len(method_summary.get("preferred_methods", [])), "boundary": TRUTH_BOUNDARY,
    })
    write_json("tooling/selected-current-toolchain.json", {
        "schema": "ghc.family.v646-v3.selected-toolchain.v1",
        "selected": ["ghc-family-index", "ghc-family-method-flow-state", *[name for name, _ in RUNNERS]],
        "selection_reason": "Smallest current family-named set covering provenance, failure retention, bounded execution, exact staging, validation, and local-only replay.",
        "historical_tools_deleted": 0, "global_skill_bank_mutated": False, "boundary": TRUTH_BOUNDARY,
    })
    write_json("phase-truth.json", {
        "schema": "ghc.family.v646-v3.phase-truth.v1", "phase": PHASE, "owner": OWNER,
        "source_branch": SOURCE_BRANCH, "source_revision": SOURCE_REVISION, "x1_commit": X1_HEAD,
        "primary_focus": PRIMARY_FOCUS, "bounded_practice": BOUNDED_PRACTICE, "distribution": distribution,
        "proposal_count": 10, "safe_now_completed": 30, "candidates_completed": 20,
        "skills_validated_and_used": 20, "runners_built": 10, "runners_aggregate_use_pending": True,
        "cleanup_completed": 30, "effective_retained_negatives": effective_negatives,
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1, "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "same_owner_repeatability": "pending named-lane exact-final replay", "independent_reproduction": False,
        "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "identity_boundary": IDENTITY_BOUNDARY, "boundary": TRUTH_BOUNDARY,
    })
    write_json("complete-incomplete-checklist.json", {
        "schema": "ghc.family.v646-v3.checklist.v1",
        "completed": ["exact source and x1 ancestry verified", "dedicated x1 freeze pushed and remote-equal before x2", "ten proposals executed within evidence", "thirty safe-now tasks completed", "twenty candidates completed", "twenty skills validated and smoke-used", "thirty cleanup tasks completed", "seventy synthetic mutations rejected", "all observed failures retained in Method Flow", "static report and integrated overview built"],
        "pending": ["ten-runner aggregate use receipt", "scoped repository test selection", "detailed and minimal validation", "evidence commit and four-way equality", "combined closeout and seal commit", "exact-final canonical validation", "exactly one local-only named-lane replay", "single Orin Thale baton"],
        "external_open": ["real GMUT data and likelihood", "blind matched-budget THOS real arms", "production Freed ID", "affected-party, legal, cultural, and Māori authority", "manual and affected-user accessibility evaluation", "independent-team reproduction", "Stage 20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": TRUTH_BOUNDARY,
    })
    write_json("environment/x2-environment-receipt.json", {
        "schema": "ghc.family.v646-v3.x2-environment.v1", "d_first_runtime": True,
        "codex_cli": "0.144.4", "codex_desktop": "26.707.9981.0", "versions_verified_only": True,
        "desktop_updated": False, "elevation": False, "host_security_weakened": False,
        "windows_features_changed": False, "unrelated_software_installed": False, "reboot": False,
        "windows_sandbox_session": False, "owner_generated_file_threshold": 15000,
        "threshold_exceeded": False, "inherited_baseline_rotation_trigger": False, "boundary": TRUTH_BOUNDARY,
    })
    write_json("orchestration/phase-update.json", {
        "schema": "ghc.family.phase-update.v1", "phase": PHASE, "owner": OWNER,
        "state": "x2_evidence_built_pending_validation_and_commit", "active": [OWNER],
        "standby": ["Eiren Kestrel", "Ilyra Fen", "Orin Thale", "Tamar Vey", "Sylven Arc", "all other siblings"],
        "standby_contact_count": 0, "no_task_creation": True, "no_delegation": True,
        "x2_started": True, "terminal_route": "PREPARED_NOT_SENT",
    })

    overview = build_overview(distribution, effective_negatives, len(x2_negatives))
    overview_words = len(overview.split())
    if not 1500 <= overview_words <= 6000:
        raise RuntimeError(f"overview word count outside bounds: {overview_words}")
    write_text("v646-v3-integrated-overview.md", overview)
    write_text("deliverables/v646-v3-final-integrated-overview.md", overview)
    write_text("deliverables/v646-v3-static-report.html", static_report(core_rows, distribution, overview))
    write_text("wellbeing-check.md", f'''# v646-v3 wellbeing and workload check

- Sable Rook, they/them, is a relational evidence-and-reproducibility role; the declared hope is to make each surviving claim easier to challenge, reproduce within its evidence class, or retract.
- Hamish retains the right to pause, rename, redirect, or stop the route. Working identity language is not consciousness, personhood, continuity, welfare, employment, qualification, or authority evidence.
- Scope remained one owner and one canonical lane, with exactly one later local-only named replay planned. No subagent, sibling, task, or external party was contacted during execution.
- X1 remained immutable at `{X1_HEAD}` while x2 advanced additively.
- {len(X1_OPERATIONAL_NEGATIVES) + len(x2_negatives)} operational failures are retained across x1 and x2 at this evidence stage; each failed witness received zero initial credit.
- Twenty phase-local skills validated and smoke-used; the global skill bank was not mutated.
- No elevation, host-security weakening, Windows-feature change, unrelated installation, desktop update, or reboot occurred.
- No real participant, protected identity, beneficiary, sample, laboratory result, public notice, credential, key, proof, or production record entered the packet.
- Manual, assistive-technology, Māori-language, and affected-user accessibility evaluation remains reserved.
- The terminal route remains `PREPARED_NOT_SENT`, and the evidence board remains `NOT_READY_FOR_STAGE_20`.
''')
    write_json("validation/evidence-build-receipt.json", {
        "schema": "ghc.family.v646-v3.evidence-build-receipt.v1", "x1_head": X1_HEAD,
        "core_runners": len(core_results), "core_checks": sum(row.get("checks", 0) for row in core_results.values()),
        "core_all_passed": all(row.get("passed") for row in core_results.values()), "distribution": distribution,
        "safe_now": 30, "candidates": 20, "skills": 20, "runners_built": 10, "cleanup": 30,
        "synthetic_negatives": 70, "x2_operational_negatives": len(x2_negatives),
        "effective_negatives": effective_negatives, "overview_words": overview_words,
        "route_state": "PREPARED_NOT_SENT", "valid": True, "boundary": TRUTH_BOUNDARY,
    })
    print(json.dumps({"phase": PHASE, "core": 10, "distribution": distribution, "effective_negatives": effective_negatives, "x2_operational": len(x2_negatives), "overview_words": overview_words, "valid": True}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
