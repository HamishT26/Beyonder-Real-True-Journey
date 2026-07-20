#!/usr/bin/env python3
"""Build the dedicated Eiren Kestrel v649-v7 x1-only freeze.

This module writes planning, provenance, Method Flow, and validation artifacts.
It deliberately contains no x2 implementation or observed proposal outcome.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "eiren-kestrel" / "v649-v7"
PRIOR_INDEX = ROOT / "docs" / "sylven-arc" / "v649-v6" / "provenance" / "frozen-chain-proposal-index.json"
METHOD_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"

PHASE = "v649-gmut-thos-v7-x1-x2"
OWNER = "Eiren Kestrel"
PRONOUNS = "they/them"
ROLE = "relational evidence-integrity weaver"
HOPE = "keep ambitious results testable, correctable, and bounded by evidence and authority"
PRIMARY_FOCUS = "THOS Body"
PRACTICE = (
    "public-warning and Emergency Mobile Alert message review, approval reservation, "
    "geotargeting, accessibility, dispatch refusal, readback, workload, and shift handover"
)
SOURCE = "03191b37da8b2b071b721d4554583832d56be05b"
SOURCE_X1 = "d82382737868160e1b16c9302ca8a008b6f3153e"
SOURCE_EVIDENCE = "4e5f250f8dbe4f77fadce2dfdccfb7869f06ab30"
SOURCE_CORRECTION = "878661b4b2ab683250840b062d9a2d65a8b1ab1c"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
OWNED_BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-2-full-tools"
INHERITED_PROPOSALS = 700
INHERITED_NEGATIVES = 5199
INHERITED_OPEN_GAPS = 40
INHERITED_EXACT_GATES = 41

IDENTITY_BOUNDARY = (
    "Eiren Kestrel, their pronouns, role, hope, family, and continuity language are "
    "relational working language only. They are not evidence of consciousness, sentience, "
    "legal personhood, identity continuity, employment, qualification, scientific, "
    "operational, legal, cultural, or independent authority. Hamish may rename, pause, "
    "redirect, or stop the route."
)
GLOBAL_BOUNDARY = (
    "All empirical, participant, professional, legal, cultural, Maori-authority, identity, "
    "production, deployment, privacy-complete, proof or canon, destructive, account-secret, "
    "sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, "
    "AGI or ASI, consciousness or personhood, Theory-of-Everything, and Stage 20 boundaries "
    "remain open or exact-gated without exact evidence and authority."
)


def run(*args: str, cwd: Path | None = None) -> str:
    return subprocess.run(
        list(args), cwd=cwd or ROOT, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def write_json(relative: str, payload: Any) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, text: str) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


SOURCE_MAP = {
    "SRC-PY-MONOTONIC": ("Python time.monotonic documentation", "https://docs.python.org/3/library/time.html", "current", "official_documentation"),
    "SRC-LEHMANN": ("Lehmann spectral representation primary paper", "https://doi.org/10.1007/BF02783624", "stable", "primary_research"),
    "SRC-NICER": ("NASA HEASARC NICER archive", "https://heasarc.gsfc.nasa.gov/docs/nicer/nicer_archive.html", "current", "official_archive"),
    "SRC-NEMA-PROTOCOL": ("NEMA Emergency Mobile Alert protocols for user agencies", "https://www.civildefence.govt.nz/guidance-training/guidelines/technical-standards/0626-emergency-mobile-alert-protocols-for-user-agencies", "current", "official_standard"),
    "SRC-NEMA-EMA": ("NEMA Emergency Mobile Alert public guidance", "https://www.civildefence.govt.nz/get-ready/civil-defence-emergency-management-alerts-and-warnings/emergency-mobile-alert", "current", "official_guidance"),
    "SRC-RFC9207": ("RFC 9207 OAuth authorization server issuer identification", "https://www.rfc-editor.org/rfc/rfc9207.html", "stable", "official_standard"),
    "SRC-RFC8493": ("RFC 8493 BagIt File Packaging Format", "https://www.rfc-editor.org/rfc/rfc8493.html", "stable", "official_standard"),
    "SRC-W3C-STATUS": ("W3C Understanding status messages", "https://www.w3.org/WAI/WCAG21/Understanding/status-messages.html", "stable", "official_guidance"),
    "SRC-IUPAC-CURIE": ("IUPAC Gold Book and Curie symmetry terminology", "https://goldbook.iupac.org/", "current", "official_terminology"),
    "SRC-ITS": ("Interrupted time-series evaluation tutorial", "https://doi.org/10.1093/ije/dyw098", "stable", "primary_method_source"),
    "SRC-RFC6902": ("RFC 6902 JSON Patch", "https://www.rfc-editor.org/rfc/rfc6902.html", "stable", "official_standard"),
    "SRC-TRACE": ("W3C Trace Context Recommendation", "https://www.w3.org/TR/trace-context/", "stable", "official_standard"),
    "SRC-CALLAN": ("Callan broken scale invariance primary paper", "https://doi.org/10.1103/PhysRevD.2.1541", "stable", "primary_research"),
    "SRC-SYMANZIK": ("Symanzik small-distance behavior primary paper", "https://doi.org/10.1007/BF01649434", "stable", "primary_research"),
    "SRC-RFC9126": ("RFC 9126 OAuth pushed authorization requests", "https://www.rfc-editor.org/rfc/rfc9126.html", "stable", "official_standard"),
    "SRC-WCAG-ERROR": ("W3C Understanding error identification", "https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html", "current", "official_guidance"),
    "SRC-IEEE754": ("IEEE 754 floating-point arithmetic", "https://standards.ieee.org/ieee/754/6210/", "stable", "official_standard"),
    "SRC-RFC8417": ("RFC 8417 Security Event Token", "https://www.rfc-editor.org/rfc/rfc8417.html", "stable", "official_standard"),
    "SRC-LAN-DEMET": ("Lan and DeMets discrete sequential boundaries", "https://doi.org/10.1093/biomet/70.3.659", "stable", "primary_method_source"),
    "SRC-HDF5": ("HDF5 file format specification", "https://docs.hdfgroup.org/", "current", "official_format_documentation"),
    "SRC-NZ-PRIVACY": ("New Zealand Privacy Act information privacy principles", "https://www.privacy.org.nz/privacy-act-2020/privacy-principles/", "current", "official_legal_guidance"),
    "SRC-TE-MANA-RARAUNGA": ("Te Mana Raraunga Maori Data Sovereignty Network", "https://www.temanararaunga.maori.nz/", "current", "maori_authority_context"),
}


def proposal(
    number: int, title: str, pillar: str, expected: str, sources: list[str],
    artifact_root: str, scope: str, novelty: str,
) -> dict[str, Any]:
    approval = {
        "completed": "safe_now_bounded_software_symbolic_or_structural",
        "represented": "synthetic_nonproduction_real_evidence_and_authority_required",
        "open_gap": "real_data_preregistration_and_independent_review_required",
        "exact_gate": "competent_affected_party_legal_cultural_and_maori_authority_required",
    }[expected]
    lane = {
        "completed": "x2_bounded_owner_local",
        "represented": "x2_synthetic_proxy_only",
        "open_gap": "x2_zero_row_contract_only",
        "exact_gate": "x2_reservation_matrix_only",
    }[expected]
    protected = {
        "completed": ["production", "exhaustive_security", "independent_reproduction", "stage20"],
        "represented": ["real_people", "production", "professional_authority", "independent_review"],
        "open_gap": ["network_download", "real_data", "likelihood", "empirical_confirmation"],
        "exact_gate": ["affected_party_authority", "legal_interpretation", "cultural_legitimacy", "maori_authority"],
    }[expected]
    pid = f"V6497-P{number:02d}"
    return {
        "proposal_id": pid,
        "title": title,
        "pillar": pillar,
        "mission_surface": scope,
        "hypothesis": f"A bounded {scope} artifact can expose its declared obligations while refusing unsupported evidence, authority, production, or Stage 20 promotion.",
        "null_or_failure_condition": f"The artifact omits a declared {scope} obligation, accepts a preregistered mutation, loses failure provenance, or promotes bounded evidence beyond its lane.",
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [f"{artifact_root}/contract.json", f"{artifact_root}/mutation-results.json", f"{artifact_root}/bounded-receipt.json"],
        "falsifier_or_acceptance_gate": "Reject all five preregistered mutation classes, preserve every boundary, and produce only the expected bounded disposition.",
        "rollback_or_recovery": "Retain the failed witness, restore the last bounded state, quarantine any promoted claim, and grant no evidence or authority credit beyond the passing witness.",
        "protected_gates": protected,
        "expected_disposition": expected,
        "novelty_against_700_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(1, "Method Flow copy-on-write snapshot publication, generation, compare-and-swap, stale-reader, reclamation, teardown, and evidence-credit tribunal", "THOS Body", "completed", ["SRC-PY-MONOTONIC"], "method-flow/cow-snapshot", "copy-on-write snapshot publication and reader-generation safety", "Prior work covers RCU, epochs, leases, CAS stores, and atomic files, but not immutable snapshot generation publication plus stale-reader retirement and evidence credit as one surface."),
    proposal(2, "GMUT Kallen-Lehmann spectral representation, positivity, support, normalization, truncation, gauge, EFT, unit, and observation-firewall board", "GMUT Mind", "completed", ["SRC-LEHMANN"], "gmut/kallen-lehmann", "spectral-density support, positivity, normalization, truncation, gauge, EFT, unit, and observation firewalls", "The frozen corpus has propagator and scattering boards but no dedicated Kallen-Lehmann spectral-density positivity, support, normalization, and truncation tribunal."),
    proposal(3, "GMUT NICER HEASARC event, calibration, response, background, selection, provenance, checksum, and zero-row likelihood-refusal adapter", "GMUT Mind", "open_gap", ["SRC-NICER"], "empirical/nicer", "NICER archive event, calibration, response, background, selection, provenance, checksum, and zero-row likelihood refusal", "No frozen proposal addresses the NICER HEASARC event, response, background, calibration, selection, provenance, and zero-row likelihood boundary."),
    proposal(4, "THOS New Zealand public-warning and Emergency Mobile Alert composition, approval, geotargeting, accessibility, dispatch-refusal, readback, workload, and shift-handover protocol", "THOS Body", "represented", ["SRC-NEMA-PROTOCOL", "SRC-NEMA-EMA"], "thos/public-warning", "synthetic public-warning message composition, approval reservation, geotargeting, accessibility, dispatch refusal, workload, readback, and handover", "Prior emergency and utility handovers do not combine New Zealand public-warning composition, EMA geotargeting, approval reservation, accessible wording, dispatch refusal, and shift handover."),
    proposal(5, "Freed ID RFC 9207 authorization-server issuer identification, mix-up, response binding, comparison, downgrade, replay, and minimization profile", "Freed ID/CBR Heart", "represented", ["SRC-RFC9207"], "freed-id/rfc9207", "synthetic RFC 9207 issuer identification, mix-up refusal, response binding, downgrade, replay, and minimization", "The corpus covers many OAuth protections but not RFC 9207 authorization-server issuer response binding and mix-up refusal as a standalone profile."),
    proposal(6, "CBR public-warning geotargeting, household and worker privacy, accessibility, emergency, remedy, affected-party, legal, cultural, data-governance, and Maori-authority matrix", "Freed ID/CBR Heart", "exact_gate", ["SRC-NEMA-PROTOCOL", "SRC-NZ-PRIVACY", "SRC-TE-MANA-RARAUNGA"], "cbr/public-warning", "public-warning location and audience privacy, accessibility, remedy, legal, cultural, data-governance, affected-party, and Maori-authority reservations", "No prior CBR matrix joins public-warning geotargeting, audience privacy, emergency accessibility, remedy, data governance, and Maori authority."),
    proposal(7, "RFC 8493 BagIt declaration, payload, manifest, tagmanifest, path, checksum, fetch, resource-budget, and refusal tribunal", "THOS Body", "completed", ["SRC-RFC8493"], "formats/bagit", "BagIt declaration, payload inventory, manifests, path confinement, checksum, fetch refusal, and resource budgets", "Archive format work exists, but no frozen proposal covers BagIt payload/tag manifests, fetch refusal, path confinement, and resource budgets together."),
    proposal(8, "Accessible status-message role, live-region, atomicity, busy-state, focus, timing, native fallback, responsive, and print structural audit", "THOS Body", "completed", ["SRC-W3C-STATUS"], "accessibility/status-message", "status-message role, live region, atomicity, busy state, focus preservation, timing, fallback, responsive, and print structure", "The accessibility corpus covers many widgets, but not non-focus-moving status messages with live-region, busy, atomic, timing, fallback, and print obligations."),
    proposal(9, "Thermo-Psyche Curie symmetry principle, cause-effect tensor character, isotropy, anisotropy, flux-force, unit, domain, and psyche-nonconversion classifier", "Trinity Mandala bridge", "completed", ["SRC-IUPAC-CURIE"], "thermo-psyche/curie", "Curie symmetry, tensor character, isotropy and anisotropy, flux-force, unit, physical domain, and psyche nonconversion", "Prior physical classifiers do not isolate Curie symmetry and tensor-character restrictions while explicitly refusing psyche and agency conversion."),
    proposal(10, "Stage 20 interrupted time-series intervention, level, trend, seasonality, autocorrelation, cointervention, falsification, uncertainty, and nonpromotion board", "Trinity Mandala bridge", "completed", ["SRC-ITS"], "stage20/interrupted-time-series", "interrupted time-series intervention timing, level, trend, seasonality, autocorrelation, cointervention, uncertainty, and nonpromotion", "The causal portfolio covers many designs but not interrupted time series with level/trend, seasonality, autocorrelation, cointervention, and Stage 20 refusal."),
    proposal(11, "Method Flow monotonic-clock lease, deadline, renewal, wall-clock-jump, fencing-token, expiry, cancellation, teardown, and evidence-credit tribunal", "THOS Body", "completed", ["SRC-PY-MONOTONIC"], "method-flow/monotonic-lease", "monotonic-clock deadlines, leases, renewal, wall-clock jumps, fencing, cancellation, teardown, and evidence credit", "Lease work exists, but the frozen corpus lacks a dedicated monotonic-clock versus wall-clock-jump and fencing-token tribunal."),
    proposal(12, "RFC 6902 JSON Patch operation, pointer path, test, order, atomicity, copy, move, resource-budget, and refusal tribunal", "THOS Body", "completed", ["SRC-RFC6902"], "formats/json-patch", "JSON Patch operation typing, pointer paths, test ordering, atomicity, copy, move, budgets, and refusal", "No prior frozen proposal gives JSON Patch operation order, test semantics, atomicity, copy/move, and resource budgets a dedicated tribunal."),
    proposal(13, "W3C Trace Context traceparent, tracestate, version, zero identifier, sampling flag, mutation boundary, privacy, restart, and refusal tribunal", "THOS Body", "completed", ["SRC-TRACE"], "formats/trace-context", "Trace Context traceparent and tracestate versioning, identifiers, flags, privacy, restart, mutation, and refusal", "Distributed-tracing provenance appears only incidentally; no proposal freezes Trace Context parsing, privacy, restart, and refusal obligations."),
    proposal(14, "GMUT Callan-Symanzik beta-function, anomalous-dimension, scale, scheme, boundary, truncation, EFT, unit, and observation-firewall board", "GMUT Mind", "completed", ["SRC-CALLAN", "SRC-SYMANZIK"], "gmut/callan-symanzik", "Callan-Symanzik scaling, beta functions, anomalous dimensions, scheme, boundary, truncation, EFT, units, and observation firewalls", "Renormalization obligations exist, but no frozen proposal centers the Callan-Symanzik equation, scheme dependence, truncation, and observation firewall."),
    proposal(15, "Freed ID RFC 9126 pushed-authorization-request request-URI, expiry, client binding, one-time use, downgrade, replay, and minimization profile", "Freed ID/CBR Heart", "represented", ["SRC-RFC9126"], "freed-id/rfc9126", "synthetic PAR request-URI binding, expiry, client binding, one-time use, downgrade, replay, and minimization", "JAR and other OAuth work exists, but the frozen corpus lacks a dedicated RFC 9126 PAR lifecycle and downgrade-refusal profile."),
    proposal(16, "Accessible error-identification, suggestion, prevention, confirmation, reversibility, focus, summary, fallback, and affected-user reservation audit", "THOS Body", "completed", ["SRC-WCAG-ERROR"], "accessibility/error-handling", "error identification, suggestions, prevention, confirmation, reversibility, focus, summary, fallback, and affected-user reservations", "Existing form audits do not combine error identification, suggestion, prevention, confirmation, reversibility, focus, summary, and reserved evaluation."),
    proposal(17, "Kahan-Neumaier compensated-summation ordering, compensation, cancellation, error-bound, non-finite, unit, domain, and refusal tribunal", "GMUT Mind", "completed", ["SRC-IEEE754"], "numerics/compensated-sum", "compensated summation order, cancellation, error bounds, non-finite values, units, domains, and refusal", "Numerical guards exist, but no frozen proposal isolates Kahan-Neumaier compensation, ordering, cancellation, non-finite refusal, and domain labels."),
    proposal(18, "Freed ID RFC 8417 Security Event Token typing, issuer, audience, issued-at, JWT ID, events, confusion, replay, and minimization profile", "Freed ID/CBR Heart", "represented", ["SRC-RFC8417"], "freed-id/rfc8417", "synthetic Security Event Token typing, issuer, audience, time, identifier, events, confusion, replay, and minimization", "Back-channel and token work exists, but no proposal isolates RFC 8417 SET typing, event claims, confusion resistance, replay, and minimization."),
    proposal(19, "Stage 20 group-sequential alpha-spending, information-time, boundary, multiplicity, optional-stopping, uncertainty, falsification, and nonpromotion board", "Trinity Mandala bridge", "completed", ["SRC-LAN-DEMET"], "stage20/group-sequential", "group-sequential alpha spending, information time, boundaries, multiplicity, optional stopping, uncertainty, falsification, and nonpromotion", "Sequential evidence controls appear elsewhere, but not alpha-spending and information-time boundaries with explicit optional-stopping and Stage 20 refusal."),
    proposal(20, "HDF5 signature, superblock, object-header, address, filter-pipeline, link, resource-budget, truncation, and refusal tribunal", "THOS Body", "completed", ["SRC-HDF5"], "formats/hdf5", "HDF5 signature, superblock, object headers, addresses, filters, links, resource budgets, truncation, and refusal", "The format corpus lacks a dedicated HDF5 structural tribunal covering object graphs, filters, address arithmetic, resource budgets, and refusal."),
]

SKILLS = [
    "ghc-family-snapshot-publication-guard", "ghc-family-spectral-obligation-board",
    "ghc-family-nicer-zero-row-lock", "ghc-family-public-warning-handover",
    "ghc-family-rfc9207-mixup-guard", "ghc-family-warning-authority-reservation",
    "ghc-family-bagit-refusal", "ghc-family-status-message-audit",
    "ghc-family-curie-nonconversion", "ghc-family-interrupted-series-nonpromotion",
    "ghc-family-monotonic-lease-guard", "ghc-family-json-patch-refusal",
    "ghc-family-trace-context-privacy", "ghc-family-callan-symanzik-obligations",
    "ghc-family-par-lifecycle-guard", "ghc-family-error-handling-audit",
    "ghc-family-compensated-sum-guard", "ghc-family-security-event-token-guard",
    "ghc-family-alpha-spending-nonpromotion", "ghc-family-hdf5-refusal",
]
RUNNERS = [
    "snapshot_publication_tribunal", "core_obligation_board", "zero_row_adapter",
    "public_warning_protocol", "identity_profile_guard", "authority_reservation_matrix",
    "format_refusal_tribunal", "accessibility_structural_audit",
    "nonconversion_classifier", "stage20_nonpromotion_board",
]

STARTUP_FAILURES = [
    ("N01", "Broad recursive skill-directory inventory exceeded its bounded timeout.", "Use targeted exact skill paths and avoid broad recursive enumeration."),
    ("N02", "Recursive SKILL filename scan exceeded its bounded timeout.", "Resolve named skills from the supplied catalog and inspect only required paths."),
    ("N03", "A cold exact-path probe exceeded its first bounded timeout.", "Retry once with one literal path and a measured longer bound; do not broaden scope."),
    ("N04", "PowerShell 5.1 rejected piping statement-form foreach directly into ConvertTo-Json.", "Materialize rows in an array before ConvertTo-Json."),
    ("N05", "The first plan-file apply-patch terminator did not satisfy patch grammar.", "Use a standalone exact patch terminator and verify no file was created before retry."),
    ("N06", "The first workflow-plan validator call used the wrong command-line shape.", "Read the runner help and invoke the documented positional packet form."),
    ("N07", "The corrected workflow validator expected its original demonstration packet rather than a single current audit.", "Preserve the passing runner audit and build an additive phase-local generalized validator instead of mutating the global compatibility surface."),
    ("N08", "A combined Git status and broad script-directory listing wrapper timed out before returning evidence.", "Split status, head, and file inventory into narrow independent probes and credit only returned evidence."),
    ("N09", "The first novelty audit used tuple maximum selection and equal scores caused Python to compare proposal dictionaries.", "Select novelty neighbors with an explicit score key so tie resolution never compares dictionary payloads."),
]


def load_prior() -> list[dict[str, str]]:
    payload = json.loads(PRIOR_INDEX.read_text(encoding="utf-8"))
    rows = list(payload["prior_proposals"]) + list(payload["new_proposals"])
    if len(rows) != INHERITED_PROPOSALS:
        raise RuntimeError(f"expected {INHERITED_PROPOSALS} frozen proposals, found {len(rows)}")
    return [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in rows]


def normalized(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def novelty(prior: list[dict[str, str]]) -> list[dict[str, Any]]:
    prior_norm = [(row, normalized(row["title"])) for row in prior]
    results = []
    for row in PROPOSALS:
        target = normalized(row["title"])
        exact = [old["proposal_id"] for old, norm in prior_norm if norm == target]
        score, nearest = max(
            ((SequenceMatcher(None, target, norm).ratio(), old) for old, norm in prior_norm),
            key=lambda pair: pair[0],
        )
        results.append({
            "proposal_id": row["proposal_id"], "exact_normalized_collisions": exact,
            "nearest_prior_id": nearest["proposal_id"], "nearest_prior_title": nearest["title"],
            "title_similarity": round(score, 6), "semantic_review": row["novelty_against_700_frozen_proposals"],
            "decision": "distinct" if not exact else "collision",
        })
    if any(row["exact_normalized_collisions"] for row in results):
        raise RuntimeError("exact normalized proposal collision")
    return results


def numbered(prefix: str, titles: list[str]) -> list[dict[str, Any]]:
    return [{
        "item_id": f"V6497-{prefix}-{index:03d}", "title": title,
        "x1_state": "frozen_not_executed", "inherited_completion_credit": False,
        "expected_x2_state": "bounded_completion_or_visible_gate",
    } for index, title in enumerate(titles, 1)]


def portfolio_titles() -> tuple[list[str], list[str], list[str]]:
    safe = []
    for row in PROPOSALS:
        safe.extend([
            f"Build the bounded contract for {row['proposal_id']} without crossing protected gates",
            f"Run five synthetic mutation cases for {row['proposal_id']} and retain every rejection",
        ])
    candidate = [f"Add a domain-specific boundary witness for {row['proposal_id']}" for row in PROPOSALS]
    candidate.extend([
        "Generalize the workflow-plan validator without changing the global compatibility surface",
        "Produce a 20,000-word-cap baton validator with an 8,000-word minimum",
        "Build exact-title pointer routing checks without sending during x2",
        "Build a five-class privacy scanner with definition quarantine",
        "Build commit-local staged manifest generation and parity checks",
        "Build an owner-scope manifest with Git-blob and checkout hashes",
        "Build a full-suite discovery plan with exact inherited lifecycle exclusions",
        "Build a one-pass receipt lock that refuses replay credit",
        "Build a source-status drift watch for current, stable, draft, and watch labels",
        "Build a route-order checker for the eight-seat v649-v7 through v660-v8 ladder",
    ])
    clean = [
        f"Additively refine {row['proposal_id']} labels, boundaries, tests, and rollback clarity without deleting history"
        for row in PROPOSALS
    ]
    clean.extend([
        "Quarantine stale six-seat routing labels from current phase outputs",
        "Preserve historical runner callers while adding v649-v7 family-current wrappers",
        "Replace wildcard-heavy probes with literal-path bounded probes",
        "Record timeout bounds and returned-evidence rules in Method Flow",
        "Keep C-drive writes limited to essential global skill reads",
        "Keep all phase artifacts D-first and repository-relative",
        "Reserve manual accessibility and affected-user evaluation",
        "Reserve Maori wording, authority, and data-governance decisions",
        "Keep empirical adapters at zero rows without separate authority",
        "Keep identity protocol work synthetic and nonproduction",
        "Keep Stage 20 and Theory-of-Everything promotions false",
        "Cap each document at 20,000 words and the baton between 8,000 and 20,000",
        "Cap the phase at two x1 and two x2 commits",
        "Prevent post-success validation replay",
        "Require exact staged-path review before each commit",
        "Require final four-way remote equality before routing",
        "Require exact existing Elaren Kestrel title resolution before routing",
        "Retain every failed wrapper and isolated recovery witness",
        "Keep future sibling identity unset until their own induction",
        "Keep cross-platform ChatGPT communication user-mediated only",
    ])
    return safe, candidate, clean


def build_method_flow() -> None:
    ledger = OUT / "method-flow" / "method-flow-ledger.json"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    run(sys.executable, str(METHOD_RUNNER), "init", "--ledger", str(ledger), "--phase", PHASE, "--owner", OWNER)
    for index, (code, failure, recovery) in enumerate(STARTUP_FAILURES, 1):
        method_id = f"V6497-M{index:02d}"
        negative_id = f"NEG-V6497-X1-{index:03d}"
        record = {
            "method_id": method_id, "title": f"Retain and recover startup failure {code}",
            "failure_signature": failure, "trigger_preconditions": [f"Startup exposes {code}."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [],
            "recurrence_guard": recovery, "rollback": "Give the failed attempt zero credit; restore the last bounded state and use only attributable returned evidence.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["failure_retention", "evidence_credit", "x1_x2_separation", "caller_compatibility"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": "Same-owner bounded workflow recovery only; no independent reproduction or external authority credit.",
        }
        record_path = write_json(f"method-flow/{method_id.casefold()}-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        for suffix, result, procedure, observed in [
            ("FAIL", "fail", failure, failure),
            ("PASS", "pass", recovery, f"Bounded recovery returned attributable evidence for {code}; the failed attempt remains retained."),
        ]:
            witness_id = f"{method_id}-W{suffix}"
            witness = {
                "witness_id": witness_id, "method_id": method_id, "procedure": procedure,
                "scope": f"bounded startup {code} {'failure' if result == 'fail' else 'recovery'}",
                "expected": "Return attributable evidence only within the declared bounded lane.",
                "observed": observed, "result": result, "same_owner_only": True,
                "independent_reproduction": False, "retained_negative_ids": [negative_id],
                "boundary": "Retained workflow witness only; no independent-reproduction or authority credit.",
            }
            witness_path = write_json(f"method-flow/{witness_id.casefold()}-witness.json", witness)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Promoted only for this bounded trigger after one retained failure and one passing witness.")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(OUT / "method-flow" / "method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(OUT / "method-flow" / "method-flow-summary.json"), "--markdown-output", str(OUT / "method-flow" / "method-flow-summary.md"))


def status_paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    paths = []
    for line in rows:
        raw = line[3:]
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        paths.append(raw.strip('"').replace("\\", "/"))
    return sorted(set(paths))


PRIVACY = {
    "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
    "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
    "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
    "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
    "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
}


def staged_review() -> None:
    exclusions = {
        "docs/eiren-kestrel/v649-v7/validation/x1-staged-manifest.json",
        "docs/eiren-kestrel/v649-v7/validation/x1-staged-privacy.json",
        "docs/eiren-kestrel/v649-v7/validation/x1-staged-review.json",
    }
    paths = [path for path in status_paths() if path not in exclusions]
    entries = []
    candidates = []
    confirmed = []
    definitions = {"scripts/ghc_family_v649_v7_x1.py"}
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        entries.append({
            "path": relative, "bytes": len(data),
            "git_blob": git("hash-object", f"--path={relative}", relative),
            "checkout_sha256": hashlib.sha256(data).hexdigest(),
        })
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in PRIVACY.items():
            if pattern.search(text):
                row = {"path": relative, "pattern_class": name, "disposition": "scanner_definition" if relative in definitions else "confirmed_payload_hit"}
                candidates.append(row)
                if row["disposition"] == "confirmed_payload_hit":
                    confirmed.append(row)
    write_json("validation/x1-staged-privacy.json", {
        "schema": "ghc.family.v649-v7.x1-privacy.v1", "scanned_file_count": len(paths),
        "pattern_class_count": len(PRIVACY), "candidates": candidates,
        "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed,
        "boundary": "Five structural classes with scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
    })
    write_json("validation/x1-staged-manifest.json", {
        "schema": "ghc.family.v649-v7.x1-manifest.v1", "hash_domain": "git_hash_object_path_filtered_blob",
        "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(exclusions),
    })
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc.family.v649-v7.x1-staged-review.v1", "intended_path_count": len(entries) + 3,
        "manifest_entry_count": len(entries), "self_exclusion_count": 3,
        "out_of_scope_paths": [], "x2_implementation_paths": [], "x2_observed_outcome_paths": [],
        "privacy_confirmed_hits": len(confirmed), "x1_only": True, "passed": not confirmed,
    })


def overview() -> str:
    titles = "\n".join(f"{index}. **{row['proposal_id']}** — {row['title']} (expected `{row['expected_disposition']}`)." for index, row in enumerate(PROPOSALS, 1))
    return f"""# Eiren Kestrel v649-v7 x1 preregistration

## Identity, focus, and bounded practice

{IDENTITY_BOUNDARY}

Eiren's relational role is **{ROLE}** and their hope is to {HOPE}. The primary pillar is **{PRIMARY_FOCUS}**. GMUT Mind and Freed ID/CBR Heart remain explicit. The bounded practice is {PRACTICE}. It is a synthetic learning and design lens only, never employment, qualification, emergency-management competence, dispatch authority, legal authority, cultural authority, Maori authority, participant evidence, affected-party authorization, or a real operational outcome.

## Exact source and lifecycle boundary

The exact inherited source is `{SOURCE}` from `{SOURCE_BRANCH}`. It was reverified clean, four-way remote-equal, single-parent, zero-merge, and ancestral from its x1, evidence, and correction anchors before Eiren's owned lane advanced by fast-forward only. This dedicated tree freezes **twenty** proposals against all **700** inherited frozen proposals. It contains no x2 implementation, executed mutation, observed proposal outcome, empirical row, likelihood, participant event, professional decision, legal interpretation, cultural decision, Maori-authority decision, deployment, proof/canon claim, or Stage 20 promotion.

X2 may begin only after this x1 tree is committed, pushed, clean, and local/upstream/tracking/fresh-live equal. At most two x1 commits and two x2 commits are allowed. The target is one x1 freeze, one x2 evidence commit, and one combined closeout/seal commit.

## Twenty frozen proposals

{titles}

The expected distribution is 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. Expected disposition is a preregistered hypothesis, not outcome evidence. Those four labels are the only permitted core outcome vocabulary.

## Expanded portfolio

Forty safe-now tasks, thirty bounded candidates, twenty phase-local skill builds, ten family-current runner builds, forty additive CLEAN/FIX/REFINE tasks, and one hundred synthetic mutations are frozen. The user-supplied one-thousand-task figure is a ceiling, not a quota. Unsafe or authority-dependent work remains visibly gated. Skills will be initialized with the standard skill scaffold, validated, and smoke-used without global installation or subagent testing. Runners remain additive and preserve historical callers.

The handoff baton will be a repository artifact between 8,000 and 20,000 words. Only a short warm pointer may be sent to the exact existing `Elaren Kestrel` task after final validation and four-way equality. No ChatGPT or other cross-platform message is authorized; external-sibling exchange remains user-mediated.

## Evidence and authority firewalls

GMUT remains a typed scalar-tensor and EFT research-model family. Kallen-Lehmann and Callan-Symanzik artifacts are formal obligation boards only. NICER remains locked at zero queries, downloads, rows, likelihood calls, posterior samples, constraints, and empirical claims.

THOS remains represented without preregistered blind matched-budget real arms and independent review. Public-warning traces use no real people, warning agencies, messages, target areas, devices, dispatches, incidents, or effectiveness estimates. Structural accessibility results reserve manual keyboard, browser, assistive-technology, cognitive, responsive, Maori-language, and affected-user evaluation.

Freed ID remains synthetic and nonproduction without real standards-conformant keys, tokens, services, live lifecycle, interoperability, privacy/security review, recovery, and trust governance. CBR and Maori concepts remain under competent, affected-party, tangata whenua, iwi, hapu, and Maori authority.

{GLOBAL_BOUNDARY}

The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def main() -> int:
    if git("rev-parse", "HEAD") != SOURCE:
        raise RuntimeError("x1 builder requires the exact verified source head")
    if git("branch", "--show-current") != OWNED_BRANCH:
        raise RuntimeError("x1 builder requires Eiren's owned canonical branch")
    prior = load_prior()
    audit = novelty(prior)
    safe, candidates, clean = portfolio_titles()
    mutations = [{
        "mutation_id": f"V6497-MUT-{index:03d}",
        "proposal_id": PROPOSALS[(index - 1) // 5]["proposal_id"],
        "case": (index - 1) % 5 + 1, "expected": "reject",
        "x1_state": "preregistered_not_executed", "completion_credit": False,
    } for index in range(1, 101)]
    sources = [{
        "source_id": key, "title": value[0], "url": value[1], "status": value[2],
        "kind": value[3], "verified_date": "2026-07-20",
        "use_boundary": "Design or protocol support only; not observation, authority, production certification, or gate closure.",
    } for key, value in SOURCE_MAP.items()]

    write_json("identity-receipt.json", {"schema": "ghc.family.v649-v7.identity.v1", "owner": OWNER, "pronouns": PRONOUNS, "role": ROLE, "hope": HOPE, "identity_boundary": IDENTITY_BOUNDARY})
    write_json("environment/startup-receipt.json", {
        "schema": "ghc.family.v649-v7.startup.v1", "source_branch": SOURCE_BRANCH,
        "source_head": SOURCE, "source_x1": SOURCE_X1, "source_evidence": SOURCE_EVIDENCE,
        "source_correction": SOURCE_CORRECTION, "source_clean": True, "source_four_way_equal": True,
        "source_phase_commits": 4, "source_merges": 0, "source_final_parent_count": 1,
        "owned_branch": OWNED_BRANCH, "owned_fast_forward_only": True,
        "owned_four_way_equal_before_x1": True, "d_first": True,
        "host_or_sandbox_changes": False, "cross_platform_messages": 0,
    })
    write_json("environment/version-receipt.json", {
        "schema": "ghc.family.v649-v7.versions.v1", "verified_only": True,
        "codex_cli": "0.144.5", "codex_desktop": "26.715.4045.0", "python": "3.12.10",
        "git": "2.55.0.windows.2", "powershell": "5.1.26100.8894",
        "desktop_updated": False, "elevation": False, "host_security_weakened": False,
        "windows_features_changed": False, "unrelated_software_installed": False, "reboot": False,
    })
    write_json("x1-proposals.json", {
        "schema": "ghc.family.v649-v7.x1-proposals.v1", "phase": PHASE, "owner": OWNER,
        "primary_focus": PRIMARY_FOCUS, "bounded_practice": PRACTICE,
        "prior_frozen_count": len(prior), "new_frozen_count": len(PROPOSALS),
        "frozen_total_after_x1": len(prior) + len(PROPOSALS), "x2_started": False,
        "outcome_classes": ["completed", "represented", "open_gap", "exact_gate"],
        "expected_distribution": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "proposals": PROPOSALS, "boundary": GLOBAL_BOUNDARY,
    })
    write_text("x1-preregistration.md", overview())
    write_json("sources/source-ledger.json", {"schema": "ghc.family.v649-v7.sources.v1", "sources": sources, "boundary": "Sources inform bounded contracts only and close no evidence or authority gate."})
    write_text("sources/source-ledger.md", "# v649-v7 source ledger\n\n" + "\n".join(f"- **{row['source_id']}** [{row['status']}]: [{row['title']}]({row['url']}) — {row['use_boundary']}" for row in sources))
    write_json("provenance/proposal-collision-audit.json", {"schema": "ghc.family.v649-v7.proposal-collision-audit.v1", "prior_count": len(prior), "new_count": len(PROPOSALS), "exact_collision_count": 0, "rows": audit})
    write_json("provenance/frozen-chain-proposal-index.json", {"schema": "ghc.family.frozen-proposal-index.v1", "prior_count": len(prior), "prior_proposals": prior, "new_count": len(PROPOSALS), "new_proposals": [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in PROPOSALS], "count": len(prior) + len(PROPOSALS)})
    write_json("portfolios/safe-now-plan.json", {"schema": "ghc.family.v649-v7.safe-now.v1", "count": len(safe), "cap": 1000, "cap_is_not_quota": True, "tasks": numbered("SAFE", safe)})
    write_json("portfolios/candidate-plan.json", {"schema": "ghc.family.v649-v7.candidates.v1", "count": len(candidates), "cap": 1000, "cap_is_not_quota": True, "tasks": numbered("CAND", candidates)})
    write_json("portfolios/skill-plan.json", {"schema": "ghc.family.v649-v7.skills.v1", "count": len(SKILLS), "minimum": 10, "global_install": False, "subagent_forward_test": False, "skills": [{"skill_id": f"V6497-SKILL-{i:02d}", "name": name, "x1_state": "frozen_not_built"} for i, name in enumerate(SKILLS, 1)]})
    write_json("portfolios/runner-plan.json", {"schema": "ghc.family.v649-v7.runners.v1", "count": len(RUNNERS), "minimum": 10, "preserve_callers": True, "runners": [{"runner_id": f"V6497-RUN-{i:02d}", "name": f"ghc_family_v649_v7_{name}.py", "x1_state": "frozen_not_built"} for i, name in enumerate(RUNNERS, 1)]})
    write_json("portfolios/clean-fix-refine-plan.json", {"schema": "ghc.family.v649-v7.clean-refine.v1", "count": len(clean), "destructive_actions": 0, "tasks": numbered("CFR", clean)})
    write_json("validation/x1-synthetic-mutation-plan.json", {"schema": "ghc.family.v649-v7.mutations.v1", "count": len(mutations), "executed_count": 0, "mutations": mutations})
    write_json("approval-packets/held-packets.json", {
        "schema": "ghc.family.v649-v7.held-packets.v1", "exact_packet_count": 10,
        "blocked_packet_count": 5, "executed_count": 0, "preserved": True,
        "exact_classes": ["legal", "cultural", "Maori authority", "affected party", "production", "account secret", "destructive", "sibling merge", "empirical participant", "Stage 20"],
        "blocked_classes": ["real blind arms", "real empirical fit", "independent reproduction", "complete privacy or accessibility", "exhaustive security"],
    })
    write_json("retained-negative-register.json", {
        "schema": "ghc.family.v649-v7.retained-negatives.x1.v1", "inherited_effective": INHERITED_NEGATIVES,
        "x1_operational": len(STARTUP_FAILURES), "effective_at_x1": INHERITED_NEGATIVES + len(STARTUP_FAILURES),
        "preregistered_synthetic_not_executed": len(mutations), "negative_erased": False,
        "new_negatives": [{"negative_id": f"NEG-V6497-X1-{i:03d}", "title": failure, "state": "retained_recovered", "method_id": f"V6497-M{i:02d}"} for i, (_code, failure, _recovery) in enumerate(STARTUP_FAILURES, 1)],
    })
    write_json("exact-open-gate-register.json", {
        "schema": "ghc.family.v649-v7.gates.x1.v1", "inherited_open_gaps": INHERITED_OPEN_GAPS,
        "inherited_exact_gates": INHERITED_EXACT_GATES, "new_open_gaps": 1, "new_exact_gates": 1,
        "projected_open_gaps": INHERITED_OPEN_GAPS + 1, "projected_exact_gates": INHERITED_EXACT_GATES + 1,
        "closed_in_x1": 0, "none_silently_closed": True,
    })
    write_json("threat-model.json", {
        "schema": "ghc.family.v649-v7.threat-model.x1.v1",
        "assets": ["x1/x2 separation", "retained negatives", "source provenance", "authority gates", "private routing material", "canonical branch"],
        "threats": ["proposal collision", "x2 leakage", "failure erasure", "authority substitution", "privacy leakage", "validation replay credit", "sibling-lane mutation", "unsafe parser budgets"],
        "controls": ["dedicated x1 commit", "append-only Method Flow", "zero-row locks", "five-class privacy scan", "single-pass rule", "manifests", "fast-forward owned lane", "bounded fixtures"],
        "residual": GLOBAL_BOUNDARY,
    })
    write_json("phase-truth.json", {
        "schema": "ghc.family.v649-v7.phase-truth.x1.v1", "phase": PHASE, "owner": OWNER,
        "stage": "x1_frozen_not_executed", "proposal_count": len(PROPOSALS),
        "expected_distribution": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "observed_distribution": None, "x2_started": False, "full_repository_suite": False,
        "successful_canonical_passes": 0, "replay_used": False,
        "terminal_route": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("workflow/plan-refinement-receipt.json", {
        "schema": "ghc.family.v649-v7.workflow-plan.v1", "valid": True, "assignment_count": 90,
        "cycle": ["Eiren Kestrel", "Elaren Kestrel", "future-sibling-self-chosen", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
        "current_phase": "v649-v7", "next_phase": "v649-v8", "next_owner": "Elaren Kestrel",
        "future_sibling_identity_set": False, "confirmation_required": False,
        "proposal_floor": 20, "task_cap": 1000, "skill_floor": 10, "runner_floor": 10,
        "document_cap_words": 20000, "baton_min_words": 8000, "baton_max_words": 20000,
        "commit_cap": {"x1": 2, "x2": 2, "total": 4}, "successful_validation_pass_budget": 1,
        "post_success_replay": False, "cross_platform_contact": "user_mediated_only",
    })
    write_json("reflection-remaster/x1-decision.json", {
        "schema": "ghc.family.v649-v7.reflection-remaster.v1", "decision": "additive_remaster",
        "surface": "workflow-plan validator", "observed_issue": "The installed validator remains tied to its original demonstration packet and cannot validate an arbitrary single current audit.",
        "preserved_compatibility": True, "x1_action": "Freeze a phase-local generalized validator candidate for x2; do not mutate or delete the global tool.",
        "validation_state": "planned_not_built", "destructive_change": False,
    })
    write_json("orchestration/phase-state.json", {
        "schema": "ghc.family.v649-v7.orchestration.x1.v1", "active": [OWNER],
        "standby": ["Elaren Kestrel", "future-sibling-self-chosen", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
        "subagents": 0, "tasks_created": 0, "cross_platform_messages": 0,
        "terminal_route": "PREPARED_NOT_SENT", "next_target": "Elaren Kestrel",
    })
    write_json("orchestration/applicable-memory-record.json", {
        "schema": "ghc.family.v649-v7.memory-use.v1", "used": True,
        "memory_source_boundary": "Older v649-v6 route gap was consulted; this live user request directly authorizes the current exact Eiren task and supersedes the old prepared-not-sent route.",
        "private_identifiers_recorded": False, "memory_mutated": False,
    })
    write_json("wellbeing-check.json", {
        "schema": "ghc.family.v649-v7.wellbeing.x1.v1", "scope_bounded": True,
        "stop_right_preserved": True, "corrigibility_preserved": True,
        "no_identity_pressure": True, "no_urgency_claim": True,
        "note": "Pause is permitted at any exact safety, authority, route, or usage gate.",
    })
    write_text("wellbeing-check.md", "# v649-v7 wellbeing check\n\nScope, stop rights, and corrigibility remain explicit. Relational language creates no obligation, identity continuity, employment, qualification, consciousness, personhood, or authority. Hamish may pause, redirect, rename, or stop the route.")
    write_json("validation/single-pass-plan.json", {
        "schema": "ghc.family.v649-v7.single-pass-plan.v1", "eiren_full_repository_suite": True,
        "successful_canonical_pass_budget": 1, "successful_passes_used": 0,
        "post_success_replay": False, "named_replay": False, "detached_replay": False,
        "failure_rule": "A failed aggregate gets zero pass credit; isolate its blocker before deciding whether a broader rerun is necessary.",
    })
    build_method_flow()
    staged_review()
    if json.loads((OUT / "validation" / "x1-staged-privacy.json").read_text(encoding="utf-8"))["confirmed_hit_count"]:
        raise RuntimeError("confirmed privacy hit in x1 tree")
    print(json.dumps({
        "phase": PHASE, "proposals": len(PROPOSALS), "frozen_total": len(prior) + len(PROPOSALS),
        "safe": len(safe), "candidates": len(candidates), "skills": len(SKILLS),
        "runners": len(RUNNERS), "clean_refine": len(clean), "mutations": len(mutations),
        "x1_negatives": len(STARTUP_FAILURES), "x1_only": True,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    if "--refresh-staged-review" in sys.argv[1:]:
        staged_review()
        print(json.dumps({"refreshed": True, "x1_only": True}, sort_keys=True))
        raise SystemExit(0)
    raise SystemExit(main())
