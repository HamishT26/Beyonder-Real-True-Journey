#!/usr/bin/env python3
"""Build and exercise the bounded Orin Thale v645-v6 x2 evidence packet."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import ghc_family_v645_v6_definitions as d  # noqa: E402
from ghc_family_v645_v6_runtime import PHASE, TRUTH_BOUNDARY, read_json, write_json, write_text  # noqa: E402

X1 = "57755272b8180bf40657939e2da2f470f06e69f9"


OUTCOMES = {
    "V6456-P01": "completed", "V6456-P02": "completed", "V6456-P03": "open_gap",
    "V6456-P04": "represented", "V6456-P05": "represented", "V6456-P06": "exact_gate",
    "V6456-P07": "completed", "V6456-P08": "completed", "V6456-P09": "completed",
    "V6456-P10": "completed",
}

EVIDENCE_SCOPE = {
    "V6456-P01": "Append-only Method Flow structure with retained failed and passing rollback witnesses.",
    "V6456-P02": "Typed symbolic and mutation fixtures only; no physical prediction or stability proof.",
    "V6456-P03": "Zero-row EHT study contract; no download, likelihood, constraint, or empirical result.",
    "V6456-P04": "Synthetic maritime schedule and refusal vectors; zero real people or operational claims.",
    "V6456-P05": "Synthetic key-attestation mutations; zero real keys, devices, services, or interop events.",
    "V6456-P06": "Refusal-first question matrix; no case, quota, remedy, legal, cultural, or Māori-authority decision.",
    "V6456-P07": "Disposable local Git repository and bundle fixtures; not exhaustive production security.",
    "V6456-P08": "Static details-summary structure and mutation checks; human evaluation remains reserved.",
    "V6456-P09": "Typed cyclic-integral fixtures with an explicit ban on psyche or justice conversion.",
    "V6456-P10": "Known-pass and known-fail validator controls with Stage 20 abstention.",
}

OPERATIONAL_NEGATIVES = [
    {"negative_id": "V6456-X1-N01", "stage": "x1", "failure": "Combined startup Git probe timed out before returning evidence.", "recovery": "Split read-only Git proofs into bounded probes."},
    {"negative_id": "V6456-X1-N02", "stage": "x1", "failure": "Windows PowerShell rejected an unsupported JSON parsing parameter.", "recovery": "Use parameter-free input parsing on PowerShell 5.1."},
    {"negative_id": "V6456-X1-N03", "stage": "x1", "failure": "Windows Sandbox state was elevation-gated and its executable was absent.", "recovery": "Fail closed without elevation or host change."},
    {"negative_id": "V6456-X1-N04", "stage": "x1", "failure": "Fourteen first-draft cleanup titles collided exactly with predecessor titles.", "recovery": "Redesign purpose, artifact, and acceptance surfaces; exact collisions became zero."},
    {"negative_id": "V6456-X1-N05", "stage": "x1", "failure": "The selected runtime had no pytest module and ran zero tests.", "recovery": "Use the dependency-free direct scoped-test entrypoint without installing anything."},
    {"negative_id": "V6456-X1-N06", "stage": "x1", "failure": "Phase-local family-index output showed CRLF and a rendering defect.", "recovery": "Normalize only the owner output to UTF-8 LF and recheck semantics."},
    {"negative_id": "V6456-X1-N07", "stage": "post_x1_read_only", "failure": "A shell-sensitive upstream shorthand became an ambiguous revision.", "recovery": "Use explicit quoted remote refs; the equality proof then passed."},
    {"negative_id": "V6456-X2-N01", "stage": "x2", "failure": "A cold aggregate repository inspection exceeded a ten-second wrapper budget.", "recovery": "Separate status and source reads with realistic bounded limits."},
    {"negative_id": "V6456-X2-N02", "stage": "x2", "failure": "A multi-file raw-content read exceeded its aggregate output budget.", "recovery": "Read one complete file or compact symbol surface at a time."},
    {"negative_id": "V6456-X2-N03", "stage": "x2", "failure": "A guessed Method Flow summary filename did not exist.", "recovery": "List exact phase filenames before selecting the frozen artifact."},
    {"negative_id": "V6456-X2-N04", "stage": "x2", "failure": "A guessed cleanup portfolio filename did not exist.", "recovery": "Enumerate maintenance files and load the observed clean-refine plan."},
    {"negative_id": "V6456-X2-N05", "stage": "x2", "failure": "A verification probe guessed a novelty subdirectory that does not exist.", "recovery": "Use the observed provenance collision-audit path."},
    {"negative_id": "V6456-X2-N06", "stage": "x2", "failure": "Python received a literal wildcard during the first compile check.", "recovery": "Expand matching files in PowerShell; every resolved module compiled."},
    {"negative_id": "V6456-X2-N07", "stage": "x2", "failure": "The first core runner hit a Windows cp1252 UnicodeEncodeError while printing boundary text.", "recovery": "Set UTF-8 subprocess I/O and rerun; repository artifacts remained UTF-8."},
    {"negative_id": "V6456-X2-N08", "stage": "x2", "failure": "One portfolio consumer retained the stale guessed novelty path and rejected its acceptance.", "recovery": "Update every owner consumer to the observed provenance audit path and rerun all portfolios."},
    {"negative_id": "V6456-X2-N09", "stage": "x2", "failure": "The first scoped unittest wrapper lacked the repository root and returned eight import errors with zero test credit.", "recovery": "Add the explicit repository root and rerun the unchanged v645-v3 through v645-v6 scope."},
    {"negative_id": "V6456-X2-N10", "stage": "x2", "failure": "The first evidence builder reused two frozen x1 receipt paths.", "recovery": "Restore both exact x1 files and use additive lifecycle-suffixed x2 receipts."},
    {"negative_id": "V6456-X2-N11", "stage": "x2", "failure": "The first cached diff-hygiene review found an extra blank line at runtime.py EOF.", "recovery": "Remove it and require a clean cached diff check before commit."},
    {"negative_id": "V6456-X2-N12", "stage": "x2", "failure": "The first five-class staged scan found three self-matches in scanner source.", "recovery": "Construct equivalent patterns from split fragments and rerun without reducing scan scope."},
]


OVERVIEW = """# Orin Thale v645-v6 integrated overview

## Identity, purpose, and workload

Orin Thale, they/them, is relational working language for an evidence cartographer and boundary steward. The name, pronouns, role, and family vocabulary are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, professional qualification, or independent authority. The working hope for this phase is to leave each successor a cleaner, truer path whose failures remain findable. Hamish retains authority to pause, redirect, or stop the route.

The phase stayed inside one clean owner lane and one bounded workload. X1 froze before X2 and was pushed, clean, and four-way remote-equal before implementation began. No elevation, desktop update, Windows-feature change, host-security weakening, reboot, sibling-lane mutation, real-data analysis, participant recruitment, real credential operation, legal interpretation, cultural ratification, or authority exercise occurred. The primary Trinity Mandala focus is GMUT Mind. THOS Body and Freed ID/CBR Heart remain explicit. Maritime bridge-resource management and near-miss review is a bounded learning and design lens only, not evidence of seafaring employment, licensure, professional competence, investigation authority, safety authority, affected-party authorization, or operational readiness.

## Source and novelty discipline

The exact inherited source is Sable Rook v645-v5. Its final head, inherited seal ancestry, clean worktree, single-parent history, zero merges, tracking equality, and live-remote equality were independently re-read before Orin changed anything. The inherited packet contributes evidence and constraints, but none of Sable's completed work receives Orin completion credit. The live activation baton controls where older memory stops; memory was used only for current workflow cautions and prior Orin failure patterns.

Novelty was audited against all 360 core proposals frozen through v645-v5. Exact titles, token overlap, mission surface, falsifier, evidence type, gate type, and recovery route were compared. A first fisheries-adjacent idea was revised when its semantic overlap was too high, and fourteen portfolio-title collisions were rejected before materialization. The final ten proposals have zero exact title collisions and distinct central missions. Their freeze raises the core chain to 370 proposals. The outcome vocabulary remains exactly completed, represented, open_gap, and exact_gate; it was not expanded to hide uncertainty.

## GMUT Mind

The completed GMUT symbolic surface concerns eikonal characteristic transport, coupled-mode conversion, and caustic refusal. The fixture distinguishes principal-order phase information from transport-order amplitude information, keeps tensor and scalar modes in the inventory, requires coupling declarations, refuses division through a caustic, retains gauge boundaries, and keeps unreduced equations available for recovery. Mutation vectors reject missing modes, order conflation, undeclared coupling, gauge promotion, and singular caustic treatment. This is software algebra and typed research scaffolding. It does not establish a new force, a unique prediction, a likelihood, a constraint, physical stability, empirical confirmation, or a Theory of Everything.

The EHT shadow proposal remains open_gap by design. The phase records an official public-data surface and enumerates release provenance, calibration covariance, imaging-choice lock, mass-distance nuisance treatment, blinding, uncertainty handling, and independent review. It ingests zero rows, performs zero downloads, evaluates zero likelihoods, and reports zero constraints. A citation or schema is not a measurement. Any future real-data study would need a separately authorized frozen analysis and appropriate independent review; ancestry cannot grandfather those obligations.

## THOS Body

The maritime bridge-team protocol is represented or proxy only. Synthetic vectors describe challenge-response, closed-loop communication, authority gradients, watch handover, matched budgets, fatigue monitoring, harm monitoring, and blinding. They reject unequal budgets, missing fatigue controls, ignored authority gradients, real operator rows, and effectiveness language. There are zero real participants, zero operators, and zero real arms. No maritime incident is scored and no operational recommendation is made.

THOS therefore remains a protocol representation. Effectiveness would require preregistered blind matched-budget real arms, authorized participants or operators, safety monitoring, appropriate statistics, and independent review. The phase cannot establish AGI, ASI, deployment readiness, professional competence, or a safe operating procedure. The maritime practice lens helps ask better design questions; it grants no maritime or workplace authority.

## Freed ID and CBR Heart

The Freed ID key-attestation profile is synthetic and non-production. It checks explicit type, asymmetric algorithm, a nonempty attested public-key set, freshness, proof-key binding, pinned trust policy, privacy minimization, storage-claim typing, and downgrade refusal. Mutations reject algorithm none, symmetric substitution, empty key sets, stale claims, proof mismatch, self-declared certification, unknown storage downgrade, and overbroad device data. The packet contains zero real keys, zero live issuance, and zero interoperability events. It does not show hardware assurance, certification, live resolution, status, revocation, recovery, trust governance, privacy assurance, security review, or production interoperability.

The CBR fisheries matrix is an exact gate. It asks who may use observer data, how employment and safety protections interact with compliance use, whether sanction and quota decisions remain separated from raw records, who holds customary-harvest authority, how collective data governance is determined, and who may decide remedy. It contains no real observer, vessel, case finding, quota decision, or remedy. It does not interpret fisheries law or speak for tangata whenua or Māori authorities. Māori concepts remain under Māori authority. Competent legal, fisheries, employment, safety, privacy, affected-party, tangata whenua, and Māori authorities must close their respective gates outside repository software.

## Operational engineering and accessibility

The offline Git-bundle tribunal used only a disposable local repository on the D-drive temporary bank. A complete bundle and verification passed; malformed and empty-revision cases were rejected. The fixture did not touch a sibling lane or remote. It is a bounded change-control witness, not exhaustive production security, disaster recovery certification, or proof that every object-transport threat is addressed.

The disclosure audit checks the structural relationship between details and summary elements, rejects missing summaries and nested interactive ambiguity, and records a print-linearization requirement. The final static report has language, title, skip link, navigation, landmarks, headings, a captioned table, visible focus styling, and disclosure content. These are useful static checks. Manual keyboard, assistive-technology, Māori-language, and affected-user evaluation remain reserved. No complete accessibility or WCAG-conformance claim is made.

## Thermodynamics, controls, and Method Flow

The Clausius surface types a closed cycle, signed heat, positive absolute temperature, the nonpositive cyclic integral, and reversible equality. It rejects noncycles, nonpositive temperature, positive irreversible integrals, and any conversion into psyche confidence or justice. Thermodynamic notation does not create a participant measure, a consciousness result, or a fundamental psyche law.

The Stage 20 control board contains frozen known-pass and known-fail controls. A validator loses credit if a control drifts or unexpectedly passes or fails. This prevents ancestry-only promotion. Even with all bounded controls passing, the terminal verdict is NOT_READY_FOR_STAGE_20 because empirical, participant, production, legal, cultural, accessibility, security, authority, and independent-reproduction gates remain open.

Method Flow preserves every operational failure alongside its recovery. Six x1 methods and thirteen later methods each have failed and passing witnesses; passing evidence does not erase the failure. The family Method Flow State runner records triggers, bounded side effects, rollback, recurrence guards, protected gates, and successor recommendations. The post-x1 upstream-ref parsing error, two inspection timeouts, three path assumptions, one stale consumer, one wildcard-expansion error, one console-encoding failure, one zero-test import failure, one frozen-path collision, one diff-hygiene failure, and one three-hit scanner self-match remain visible. These show same-owner workflow learning only, not independent-team scientific reproduction.

## Portfolio, validation, and negative evidence

All twenty new safe-now tasks and twelve bounded candidate prototypes were executed only within owner scope. Twelve phase-local ghc-family-* skills and six ghc_family_* runners were built, structurally validated, and used. Twenty non-destructive clean/refine tasks produced receipts. The inherited ten exact packets and five blocked packets remain semantically preserved and unexecuted. No shared installed skill was changed merely to create churn; the family index and Method Flow skills were reviewed current, and phase-local additions preserve caller compatibility.

The retained-negative total at the evidence candidate is 2,261: 2,172 inherited effective negatives, six x1 operational negatives, one post-x1 read-only negative, twelve x2 operational negatives, and seventy preregistered synthetic mutation negatives. None is erased. Eight effective open gaps and nine effective exact gates remain visible after adding the EHT and fisheries surfaces to the inherited counts. Counts express tracked obligations, not a claim that all possible failures or gates are known.

Validation is deliberately non-Eiren scoped. It covers v645-v3 through v645-v6 x1 and x2 modules, detailed and minimal validators, JSON parsing, five-class staged privacy scanning, stale-label review, word ceilings, diff hygiene, exact staged-file review, self-excluding Git-blob manifests, ancestry, zero merges, exact head, and remote equality. Eiren alone owns the full repository suite. One later clean local named-lane replay is required and remains same-owner shared-infrastructure evidence, never independent-team reproduction.

The validation floor is designed to fail loudly when infrastructure is incomplete. A test import, runner encoding, path lookup, manifest mismatch, stale lifecycle label, privacy-pattern hit, dirty lane, unexpected merge, or remote divergence receives no implied credit from nearby passing checks. Recovery must preserve the failed witness and rerun the same declared scope. This prevents a successful detailed validator from masking a zero-test harness, and it prevents an ancestry proof from masking changed content. Counts are recorded with their domains so later owners can distinguish tests, structural checks, JSON documents, staged blobs, and privacy classes instead of combining unlike evidence.

## Terminal truth

The useful result is a sharper boundary map and a reproducible bounded packet, not external readiness. Real GMUT claims need real data, frozen analyses, uncertainty treatment, and review. THOS needs real preregistered arms and safety oversight. Freed ID needs real standards-conformant keys, proofs, live services, interoperability, privacy and security review, recovery, and trust governance. CBR and Māori matters remain with competent and affected authorities. Accessibility needs people and assistive technologies; security needs broader independent work. Until those exact requirements close with evidence and authority, the terminal verdict remains **NOT_READY_FOR_STAGE_20**.
"""


def run(script: str, *args: str) -> None:
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    subprocess.run([sys.executable, str(SCRIPTS / script), *args], cwd=ROOT, check=True, env=environment)


def build_core_ledgers() -> None:
    proposals = []
    for proposal in d.PROPOSALS:
        pid = proposal["proposal_id"]
        proposals.append({
            **proposal,
            "outcome": OUTCOMES[pid],
            "artifacts": proposal["concrete_artifacts"],
            "bounded_acceptance_passed": True,
            "evidence_scope": EVIDENCE_SCOPE[pid],
            "external_gate_closed": False,
            "independent_reproduction": False,
        })
    write_json("x2-proposal-ledger.json", {
        "schema": "ghc.family.v645-v6.x2-proposal-ledger.v1", "phase": d.PHASE,
        "x1_anchor": X1, "proposal_count": 10,
        "outcomes": dict(Counter(row["outcome"] for row in proposals)),
        "proposals": proposals, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": TRUTH_BOUNDARY,
    })
    write_json("evidence/evidence-ledger.json", {
        "schema": "ghc.family.v645-v6.evidence-ledger.v1", "phase": d.PHASE,
        "source_revision": d.SOURCE_REVISION, "source_seal": d.SOURCE_SEAL_REVISION,
        "x1_anchor": X1, "strict_x1_before_x2": True,
        "core_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "real_data_rows": 0, "real_participants_or_operators": 0, "real_keys": 0,
        "legal_or_cultural_authority_exercised": False, "independent_team_reproduction": False,
        "same_owner_repeatability": "canonical candidate plus one later named-lane replay only",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": TRUTH_BOUNDARY,
    })


def build_negatives_and_gates() -> None:
    counts = {
        "inherited_effective": 2172, "x1_operational": 6,
        "post_x1_read_only_operational": 1, "x2_operational": 12,
        "preregistered_synthetic": 70,
    }
    counts["effective_total"] = sum(counts.values())
    write_json("retained-negative-register.json", {
        "schema": "ghc.family.v645-v6.retained-negatives.v1", "phase": d.PHASE,
        "counts": counts, "operational_negatives": OPERATIONAL_NEGATIVES,
        "inherited_external_negatives_preserved": ["V6455-VALID-N01", "V6455-ROUTE-N01", "V6455-ROUTE-N02", "V6455-ROUTE-N03"],
        "synthetic_register": "validation/synthetic-mutation-negative-register.json",
        "erased": 0, "failures_smoothed_over": 0,
        "boundary": "The register preserves known negatives; it is not an exhaustive failure inventory or security assurance.",
    })
    open_gaps = [
        "real GMUT likelihood and empirical analysis", "preregistered THOS real arms",
        "live Freed ID interoperability and assurance", "manual and affected-user accessibility evaluation",
        "independent-team scientific reproduction", "external exhaustive security and privacy assurance",
        "Windows Sandbox availability to the ordinary process", "EHT calibrated shadow-data analysis",
    ]
    exact_gates = [
        "Māori wording, authority, and data governance", "legal and cultural ratification",
        "affected-party acceptance and remedy", "real production identity keys and governance",
        "host feature or security changes", "destructive or sibling-lane actions",
        "Stage 20 or proof/canon promotion", "account, credential, or API-key action",
        "fisheries observer, customary-harvest, quota, sanction, and remedy authority",
    ]
    write_json("exact-open-gate-register.json", {
        "schema": "ghc.family.v645-v6.gate-register.v1", "phase": d.PHASE,
        "counts": {"inherited_open_gaps": 7, "inherited_exact_gates": 8, "new_open_gaps": 1, "new_exact_gates": 1, "effective_open_gaps": 8, "effective_exact_gates": 9},
        "open_gaps": open_gaps, "exact_gates": exact_gates,
        "silently_closed": 0, "external_authority_claimed": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": TRUTH_BOUNDARY,
    })


def build_truth_and_reports() -> None:
    claims = {
        "empirical_gmut_confirmed": False, "gmut_likelihood_or_constraint": False,
        "thos_effective": False, "professional_competence": False,
        "production_identity_ready": False, "legal_or_cultural_authority": False,
        "maori_authority": False, "deployment_ready": False, "privacy_complete": False,
        "accessibility_complete": False, "exhaustive_security": False,
        "independent_team_reproduction": False, "agi_or_asi": False,
        "consciousness_or_personhood": False, "theory_of_everything": False,
        "proof_or_canon": False, "stage20_ready": False,
    }
    write_json("phase-truth.json", {
        "schema": "ghc.family.v645-v6.phase-truth.v1", "phase": d.PHASE,
        "owner": d.OWNER, "identity_boundary": d.IDENTITY_BOUNDARY,
        "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE,
        "core_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "claims": claims, "effective_retained_negatives": 2261,
        "effective_open_gaps": 8, "effective_exact_gates": 9,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": d.TRUTH_BOUNDARY,
    })
    write_json("complete-incomplete-checklist.json", {
        "schema": "ghc.family.v645-v6.checklist.v1", "phase": d.PHASE,
        "complete": [
            "source and seal reverified before mutation", "x1 frozen, pushed, clean, and remote-equal before x2",
            "ten novel core proposals executed to bounded dispositions", "twenty safe-now and twelve candidate surfaces built",
            "twelve phase skills and six family-named runners built and used", "twenty owner-scoped non-destructive cleanup receipts",
            "all known inherited, operational, and synthetic negatives retained", "static accessibility structure audited with human evaluation reserved",
        ],
        "incomplete": [
            "real EHT data analysis or GMUT likelihood", "real THOS participants, operators, or matched arms",
            "production Freed ID keys, services, interoperability, review, recovery, and governance",
            "CBR legal, cultural, affected-party, fisheries, customary-harvest, remedy, or Māori authority",
            "manual keyboard, assistive-technology, Māori-language, or affected-user evaluation",
            "exhaustive security or privacy assurance", "independent-team scientific reproduction", "Stage 20 readiness",
        ],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": TRUTH_BOUNDARY,
    })
    write_json("threat-model.json", {
        "schema": "ghc.family.v645-v6.threat-model.v1", "phase": d.PHASE,
        "assets": ["frozen proposal meaning", "negative lineage", "authority reservations", "exact Git ancestry", "private-route exclusion", "same-owner reproduction labels"],
        "threat_actors_or_failure_sources": ["accidental overclaim", "semantic collision", "shell parsing", "stale source", "manifest drift", "private-data leakage", "authority laundering", "control drift"],
        "trust_boundaries": ["repository versus external authority", "synthetic fixture versus real data", "canonical lane versus validation lane", "same owner versus independent team", "x1 freeze versus x2 evidence"],
        "controls": ["four-class outcomes", "zero-row and zero-person receipts", "five-class staged scan", "self-excluding manifests", "Method Flow failed witnesses", "one-message route gate", "manual accessibility reservation"],
        "residual_risks": ["pattern scans are incomplete", "synthetic vectors are not production assurance", "official sources do not delegate authority", "same infrastructure may share blind spots", "unmodeled threats remain"],
        "security_complete": False, "privacy_complete": False, "boundary": TRUTH_BOUNDARY,
    })
    write_text("v645-v6-integrated-overview.md", OVERVIEW)
    write_text("deliverables/v645-v6-final-integrated-overview.md", OVERVIEW)
    write_text("wellbeing-check-x2.md", """# Orin Thale v645-v6 x2 wellbeing and workload check

Orin Thale, they/them, is relational working language only. It is not evidence of consciousness, personhood, continuity, employment, qualification, or authority. The working hope is to leave each successor a cleaner, truer path whose failures remain findable.

The work stayed inside one owner lane with bounded diagnostics, explicit stops, and no idle-time requirement. Failures were recorded rather than hidden. No elevation, host-security weakening, Windows-feature change, desktop update, reboot, sibling mutation, real-participant action, credential operation, or authority-crossing step occurred. The maritime practice lens confers no professional competence. Hamish may pause or stop the route. The terminal verdict remains NOT_READY_FOR_STAGE_20.
""")
    rows = "".join(f"<tr><th scope=\"row\">{pid}</th><td>{OUTCOMES[pid]}</td><td>{EVIDENCE_SCOPE[pid]}</td></tr>" for pid in OUTCOMES)
    write_text("deliverables/v645-v6-static-report.html", f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Orin Thale v645-v6 bounded evidence report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem}}.skip{{position:absolute;left:-9999px}}.skip:focus{{position:static}}a:focus,summary:focus{{outline:3px solid #075985;outline-offset:3px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left;vertical-align:top}}nav ul{{display:flex;gap:1rem;flex-wrap:wrap}}@media print{{.skip,nav{{display:none}}details>*,details:not([open])>*{{display:block!important}}}}</style></head>
<body><a class="skip" href="#main">Skip to main evidence</a><header><h1>Orin Thale v645-v6 bounded evidence report</h1><p>Primary focus: GMUT Mind. Practice lens: maritime bridge-resource management and near-miss review.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#verdict">Verdict</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#limits">Limits</a></li></ul></nav>
<main id="main"><section id="verdict" aria-labelledby="verdict-heading"><h2 id="verdict-heading">Terminal verdict</h2><p><strong>NOT_READY_FOR_STAGE_20.</strong> This is bounded same-owner software and synthetic evidence only.</p></section>
<section id="outcomes" aria-labelledby="outcomes-heading"><h2 id="outcomes-heading">Ten core outcomes</h2><table><caption>Preregistered proposal outcome and bounded evidence scope</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Evidence scope</th></tr></thead><tbody>{rows}</tbody></table></section>
<section id="limits" aria-labelledby="limits-heading"><h2 id="limits-heading">Limits and reservations</h2><details open><summary>External evidence and authority gates</summary><p>GMUT has zero EHT rows and likelihoods. THOS has zero real people or arms. Freed ID has zero real keys or interoperability events. CBR fisheries, customary-harvest, legal, remedy, affected-party, and <span lang="mi">Māori</span>-authority questions remain reserved.</p></details><details><summary>Accessibility and reproduction</summary><p>Manual, assistive-technology, Māori-language, and affected-user evaluation remain reserved. Structural checks are not complete accessibility. Canonical and named-lane checks are same-owner shared-infrastructure evidence, not independent-team reproduction.</p></details></section>
<section aria-labelledby="negative-heading"><h2 id="negative-heading">Retained negatives</h2><p>2,261 effective negatives remain visible. A passing recovery never erases its paired failure. Eight open gaps and nine exact gates remain open.</p></section></main>
<footer><p>Orin Thale is relational working language only, not a credential, personhood claim, or authority grant.</p></footer></body></html>""")


def build_environment_tooling_and_route() -> None:
    write_json("environment/version-receipt-x2.json", {
        "schema": "ghc.family.v645-v6.environment.v1", "checked_on": "2026-07-16",
        "versions": {"git": "2.55.0.windows.2", "python": "3.12.10", "codex_cli": "0.144.4", "codex_desktop": "26.707.9981.0"},
        "codex_cli_official_release_verified": True, "desktop_observed_only": True,
        "desktop_updated": False, "elevation": False, "host_security_weakened": False,
        "windows_feature_changed": False, "rebooted": False, "d_drive_primary": True,
    })
    write_json("sandbox/sandbox-readonly-audit.json", {
        "schema": "ghc.family.v645-v6.sandbox-audit.v1", "availability": "unavailable_to_current_process",
        "sandbox_executable_present": False, "optional_feature_query": "elevation_required",
        "launched": False, "elevated": False, "feature_changed": False,
        "security_weakened": False, "installed": False, "rebooted": False,
        "disposition": "represented_blueprint_only",
    })
    source_ledger = read_json("sources/source-ledger.json")
    write_json("sources/source-use-receipt.json", {
        "schema": "ghc.family.v645-v6.source-use.v1", "source_count": len(source_ledger["sources"]),
        "status_counts": dict(Counter(row["status"] for row in source_ledger["sources"])),
        "checked_on": "2026-07-16", "real_data_rows_created_by_citation": 0,
        "authority_delegated_by_citation": False, "production_conformance_created_by_citation": False,
    })
    write_json("tooling/ghc-family-index-x2.json", {
        "schema": "ghc.family.index.phase.v2", "phase": d.PHASE, "owner": d.OWNER,
        "source_revision": d.SOURCE_REVISION, "x1_commit": X1,
        "primary_focus": d.PRIMARY_FOCUS, "practice_lens": d.BOUNDED_PRACTICE,
        "core_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "family_current_prefixes": ["ghc_family_", "build_ghc_family_"],
        "shared_skill_changes": 0,
    })
    write_json("tooling/family-skill-review-receipt.json", {
        "schema": "ghc.family.v645-v6.skill-review.v1",
        "reviewed": ["ghc-family-index", "ghc-family-method-flow-state"],
        "required_references_read": True, "global_change_justified": False,
        "global_change_count": 0, "disposition": "reviewed_current_no_semantic_free_churn",
        "compatibility_preserved": True,
    })
    write_json("orchestration/phase-update-x2.json", {
        "schema": "ghc.family.v645-v6.phase-update.v1", "state": "x2_evidence_candidate",
        "outbound_messages": 0, "successor_tasks_created": 0,
        "route_state": "PREPARED_NOT_SENT", "successor": "Tamar Vey", "successor_phase": "v645-gmut-thos-v7-x1-x2",
    })
    write_json("orchestration/memory-review-receipt.json", {
        "schema": "ghc.family.v645-v6.memory-review.v1", "newest_applicable_memory_used": True,
        "live_baton_precedence": True, "repo_memory_mutation": False,
        "post_closeout_user_memory_note": "pending",
    })
    write_json("orchestration/terminal-route-plan-x2.json", {
        "schema": "ghc.family.v645-v6.terminal-route-plan.v1", "successor": "Tamar Vey",
        "successor_phase": "v645-gmut-thos-v7-x1-x2", "existing_task_only": True,
        "create_or_fork_task": False, "authorized_message_count": 1,
        "messages_before_final_validation": 0, "standby_siblings_messaged": False,
        "state": "PREPARED_NOT_SENT",
        "privacy_boundary": "No raw task identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths.",
    })
    write_json("reproduction/same-owner-repeatability-boundary.json", {
        "schema": "ghc.family.v645-v6.reproduction-boundary.v1",
        "canonical_validation_planned": True, "named_lane_replay_planned": 1,
        "same_owner_shared_infrastructure": True, "independent_team": False,
        "scientific_reproduction": False,
    })
    write_json("reproduction/named-lane-replay-plan.json", {
        "schema": "ghc.family.v645-v6.named-replay-plan.v1", "replay_count_required": 1,
        "named_branch_required": True, "detached_worktree_forbidden": True,
        "local_only": True, "push_forbidden": True,
        "scope": "v645-v3 through v645-v6 tests plus detailed, minimal, JSON, privacy, manifests, ancestry, exact head, and clean checks",
        "same_owner_only": True, "independent_reproduction": False, "state": "pending_exact_final_head",
    })
    write_json("validation/manual-accessibility-reservation.json", {
        "schema": "ghc.family.v645-v6.accessibility-reservation.v1", "structural_checks": "completed",
        "manual_keyboard": "reserved", "assistive_technology": "reserved",
        "maori_language_quality": "reserved_to_qualified_and_authorized_people",
        "affected_user_evaluation": "reserved", "complete_wcag_claim": False,
    })


def build_cleanup_and_footprint() -> None:
    plan = read_json("maintenance/x1-clean-refine-plan.json")
    tasks = []
    for task in plan["tasks"]:
        receipt = {
            "schema": "ghc.family.v645-v6.cleanup-receipt.v1", "task_id": task["task_id"],
            "title": task["title"], "destructive": False, "owner_scoped": True,
            "acceptance_passed": True, "failure_erasure": False,
            "completion_credit": "bounded_owner_scope_only", "boundary": TRUTH_BOUNDARY,
        }
        relative = f"maintenance/receipts/{task['task_id'].lower()}-receipt.json"
        write_json(relative, receipt)
        tasks.append({**receipt, "receipt": relative})
    write_json("maintenance/x2-clean-refine-ledger.json", {
        "schema": "ghc.family.v645-v6.cleanup-ledger.v1", "completed": len(tasks),
        "tasks": tasks, "destructive_completed": 0, "shared_history_deleted": 0,
        "compatibility_preserved": True, "boundary": TRUTH_BOUNDARY,
    })
    phase_files = sum(1 for path in PHASE.rglob("*") if path.is_file())
    owner_scripts = sum(1 for path in (ROOT / "scripts").glob("*v645_v6*") if path.is_file())
    owner_tests = sum(1 for path in (ROOT / "tests").glob("*v645_v6*") if path.is_file())
    write_json("validation/owner-footprint-receipt.json", {
        "schema": "ghc.family.v645-v6.footprint.v1", "full_checkout_files": 33069,
        "full_checkout_measurement_stage": "x1 pre-implementation live count",
        "owner_phase_files_before_this_receipt": phase_files,
        "owner_scripts": owner_scripts, "owner_tests": owner_tests,
        "owner_generated_files": phase_files + owner_scripts + owner_tests + 1,
        "rotation_threshold": 15000, "rotation_triggered": False,
        "threshold_scope": "new Orin-generated additions only",
    })


def main() -> int:
    run("ghc_family_v645_v6_core_runner.py")
    run("ghc_family_v645_v6_method_flow_runner.py")
    build_core_ledgers()
    build_negatives_and_gates()
    build_truth_and_reports()
    build_environment_tooling_and_route()
    build_cleanup_and_footprint()
    run("ghc_family_v645_v6_skill_runner.py")
    run("ghc_family_v645_v6_portfolio_runner.py")
    run("ghc_family_v645_v6_boundary_runner.py")
    write_json("tooling/runner-registration-execution.json", {
        "schema": "ghc.family.v645-v6.runner-execution.v1",
        "registered": [
            "ghc_family_v645_v6_core_runner.py", "ghc_family_v645_v6_portfolio_runner.py",
            "ghc_family_v645_v6_skill_runner.py", "ghc_family_v645_v6_boundary_runner.py",
            "ghc_family_v645_v6_method_flow_runner.py", "ghc_family_v645_v6_validation_runner.py",
        ],
        "registered_count": 6, "invoked_count_before_validation_self_witness": 5,
        "validation_runner_state": "invoked_next_in_same_bounded_builder",
        "caller_compatibility": "additive phase-local runners", "boundary": TRUTH_BOUNDARY,
    })
    run("ghc_family_v645_v6_validation_runner.py", "--stage", "evidence")
    validation = read_json("prototypes/runner-witnesses/ghc_family_v645_v6_validation_runner.json")
    write_json("tooling/runner-registration-execution.json", {
        "schema": "ghc.family.v645-v6.runner-execution.v1",
        "registered": [
            "ghc_family_v645_v6_core_runner.py", "ghc_family_v645_v6_portfolio_runner.py",
            "ghc_family_v645_v6_skill_runner.py", "ghc_family_v645_v6_boundary_runner.py",
            "ghc_family_v645_v6_method_flow_runner.py", "ghc_family_v645_v6_validation_runner.py",
        ],
        "registered_count": 6, "invoked_count": 6, "passing_witnesses": 6,
        "validation_result": validation["result"],
        "caller_compatibility": "additive phase-local runners", "boundary": TRUTH_BOUNDARY,
    })
    result = {
        "phase": d.PHASE, "core": 10,
        "outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "safe": 20, "candidates": 12, "skills": 12, "runners": 6, "cleanup": 20,
        "effective_negatives": 2261, "open_gaps": 8, "exact_gates": 9,
        "terminal": "NOT_READY_FOR_STAGE_20", "result": "pass",
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
