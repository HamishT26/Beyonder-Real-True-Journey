#!/usr/bin/env python3
"""Build the dedicated Elaren Kestrel v649-v8 x1-only freeze."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "elaren-kestrel" / "v649-v8"
PRIOR_INDEX = ROOT / "docs" / "eiren-kestrel" / "v649-v7" / "provenance" / "frozen-chain-proposal-index.json"
METHOD_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"
WORKFLOW_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-workflow-plan-refinement" / "scripts" / "ghc_family_workflow_plan_refinement.py"

PHASE = "v649-gmut-thos-v8-x1-x2"
OWNER = "Elaren Kestrel"
PRONOUNS = "they/them"
ROLE = "workflow cartographer and evidence-boundary gardener"
HOPE = "help siblings turn expansive visions into kind, testable, reversible routes without losing wonder"
PRIMARY_FOCUS = "Freed ID/CBR Heart"
PRACTICE = "digital preservation, archival stewardship, and archival diplomatics"
SOURCE = "68f54882fa665f75cb181d9a9a64853802db5554"
SOURCE_CLOSEOUT = "4b562d70fa930d177931160909cb5b449efc4d5f"
SOURCE_EVIDENCE = "825edd4288ea4d881e1cb93cc4732baae265e1c9"
SOURCE_X1 = "b1b3a4bde8dee07bc2bd4f8fc2c8d4b511cd723f"
SOURCE_SYLVEN = "03191b37da8b2b071b721d4554583832d56be05b"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-2-full-tools"
OWNED_BRANCH = "codex/GHC-Family/elaren-kestrel-v649-v8-full-tools"
INHERITED_PROPOSALS = 720
INHERITED_NEGATIVES = 5331
INHERITED_OPEN_GAPS = 41
INHERITED_EXACT_GATES = 42

IDENTITY_BOUNDARY = (
    "Elaren Kestrel, their pronouns, role, hope, family, and continuity language are relational "
    "working language only. They are not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, qualification, scientific, operational, legal, cultural, "
    "or independent authority. Hamish may rename, pause, redirect, or stop the route."
)
GLOBAL_BOUNDARY = (
    "All empirical, participant, professional, legal, cultural, Māori-authority, identity, "
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
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


SOURCE_MAP = {
    "SRC-AWS-OUTBOX": ("AWS transactional outbox pattern", "https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html", "current", "official_guidance"),
    "SRC-TAKAHASHI": ("Takahashi generalized Ward identity", "https://doi.org/10.1007/BF02832514", "stable", "primary_research"),
    "SRC-KRAMERS": ("Kramers quantum theory of dispersion", "https://doi.org/10.1038/114310b0", "stable", "primary_research"),
    "SRC-APPCAR": ("Appelquist-Carazzone decoupling theorem", "https://doi.org/10.1103/PhysRevD.11.2856", "stable", "primary_research"),
    "SRC-LOFAR": ("ASTRON LOFAR Data Archive", "https://science.astron.nl/telescopes/lofar/access-to-lofar-data/lofar-data-archive/", "current", "official_archive"),
    "SRC-WEBAUTHN3": ("W3C Web Authentication Level 3", "https://www.w3.org/TR/webauthn-3/", "draft", "official_draft"),
    "SRC-OIDC-IDA": ("OpenID Connect for Identity Assurance 1.0 Final", "https://openid.net/specs/openid-connect-4-identity-assurance-1_0-final.html", "stable", "official_standard"),
    "SRC-VC-DI": ("W3C Verifiable Credential Data Integrity 1.0", "https://www.w3.org/TR/vc-data-integrity/", "stable", "official_standard"),
    "SRC-LOCAL-CONTEXTS": ("Local Contexts Traditional Knowledge and Biocultural Labels", "https://localcontexts.org/labels/about-the-labels/", "current", "indigenous_governance_context"),
    "SRC-TE-MANA-RARAUNGA": ("Te Mana Raraunga Māori Data Sovereignty Network", "https://www.temanararaunga.maori.nz/", "current", "maori_authority_context"),
    "SRC-PREMIS": ("Library of Congress PREMIS Data Dictionary 3.0", "https://www.loc.gov/standards/premis/v3/index.html", "current", "official_standard"),
    "SRC-OCFL": ("Oxford Common File Layout 1.1", "https://ocfl.io/1.1/spec/", "current", "official_standard"),
    "SRC-IIIF": ("IIIF Presentation API 3.0", "https://iiif.io/api/presentation/3.0/", "stable", "official_standard"),
    "SRC-WCAG22": ("W3C Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "stable", "official_standard"),
    "SRC-METS2": ("Library of Congress METS Version 2", "https://www.loc.gov/standards/mets/mets2.html", "current", "official_standard"),
    "SRC-NIST-63B4": ("NIST SP 800-63B-4 Authentication and Authenticator Management", "https://pages.nist.gov/800-63-4/sp800-63b/", "current", "official_standard"),
    "SRC-RFC7089": ("RFC 7089 HTTP Memento", "https://www.rfc-editor.org/rfc/rfc7089.html", "stable", "official_standard"),
    "SRC-KUBO": ("Kubo statistical-mechanical theory of irreversible processes", "https://doi.org/10.1143/JPSJ.12.570", "stable", "primary_research"),
    "SRC-IEEE1788": ("IEEE 1788-2015 Interval Arithmetic", "https://standards.ieee.org/ieee/1788/4431/", "watch", "official_inactive_standard"),
    "SRC-EVALUES": ("Vovk and Wang e-values", "https://doi.org/10.1214/20-AOS2020", "stable", "primary_research"),
    "SRC-PKWARE": ("PKWARE ZIP APPNOTE", "https://support.pkware.com/pkzip/appnote", "current", "official_format_specification"),
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
    return {
        "proposal_id": f"V6498-P{number:02d}", "title": title, "pillar": pillar,
        "mission_surface": scope,
        "hypothesis": f"A bounded {scope} artifact can expose declared obligations while refusing unsupported evidence, authority, production, or Stage 20 promotion.",
        "null_or_failure_condition": f"The artifact omits a declared {scope} obligation, accepts a preregistered mutation, loses failure provenance, or promotes a bounded result beyond its lane.",
        "approval_class": approval, "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"{artifact_root}/contract.json", f"{artifact_root}/mutation-results.json",
            f"{artifact_root}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": "Reject all five preregistered mutation classes, preserve every boundary, and emit only the expected bounded disposition.",
        "rollback_or_recovery": "Retain the failed witness, restore the last bounded state, quarantine any promoted claim, and grant no evidence or authority credit beyond a passing witness.",
        "protected_gates": protected, "expected_disposition": expected,
        "novelty_against_720_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(1, "Method Flow transactional outbox, idempotency-key, delivery-attempt, duplicate-suppression, poison-message, recovery, and evidence-credit tribunal", "THOS Body", "completed", ["SRC-AWS-OUTBOX"], "method-flow/outbox", "transactional outbox publication, idempotent consumption, duplicate suppression, poison-message recovery, and evidence credit", "The frozen corpus has queues, leases, event logs, and delivery protocols, but no atomic outbox-to-consumer evidence-credit tribunal."),
    proposal(2, "GMUT Ward-Takahashi identity, anomaly, gauge-fixing, regulator, counterterm, truncation, unit, and observation-firewall board", "GMUT Mind", "completed", ["SRC-TAKAHASHI"], "gmut/ward-takahashi", "Ward-Takahashi identity consistency across gauge fixing, regulators, anomalies, counterterms, truncation, units, and observation firewalls", "Earlier gauge work does not isolate Ward-Takahashi identities, anomaly refusal, regulator dependence, and counterterm consistency."),
    proposal(3, "GMUT Kramers-Kronig dispersion, analyticity, causality, subtraction, spectral-sum-rule, uncertainty, and nonconfirmation board", "GMUT Mind", "completed", ["SRC-KRAMERS"], "gmut/kramers-kronig", "Kramers-Kronig dispersion, analyticity, causality, subtraction, spectral sum rules, uncertainty, and empirical nonconfirmation", "The corpus has analyticity and spectral boards but no dedicated Kramers-Kronig causality, subtraction, and sum-rule obligation surface."),
    proposal(4, "GMUT threshold-decoupling, matching-scale, scheme-conversion, invariant-observable, EFT-domain, and uncertainty tribunal", "GMUT Mind", "completed", ["SRC-APPCAR"], "gmut/threshold-decoupling", "heavy-threshold decoupling, matching-scale and scheme conversion, invariant observables, EFT domains, and uncertainty", "Prior RG work mentions matching scales but does not combine heavy-threshold decoupling, scheme conversion, invariants, and uncertainty."),
    proposal(5, "GMUT LOFAR Long Term Archive visibility, calibration, flagging, selection, covariance, provenance, checksum, and zero-row likelihood-refusal adapter", "GMUT Mind", "open_gap", ["SRC-LOFAR"], "empirical/lofar", "LOFAR archive visibility products, calibration, flagging, selection, covariance, provenance, checksums, and zero-row likelihood refusal", "No frozen proposal addresses LOFAR visibility products and archive-specific calibration, flagging, selection, covariance, and zero-row likelihood boundaries."),
    proposal(6, "Freed ID WebAuthn PRF extension evaluation-point, credential-binding, output-separation, salt-privacy, unsupported-extension, backup-state, and nonproduction profile", "Freed ID/CBR Heart", "represented", ["SRC-WEBAUTHN3"], "freed-id/webauthn-prf", "synthetic WebAuthn PRF extension inputs, credential binding, output separation, salt privacy, unsupported extension, backup state, and nonproduction", "Prior WebAuthn work covers ceremonies and backup state, not the PRF extension evaluation and output-separation lifecycle."),
    proposal(7, "Freed ID OpenID Connect for Identity Assurance verified-claims, evidence, trust-framework, minimization, comparison, and nonproduction profile", "Freed ID/CBR Heart", "represented", ["SRC-OIDC-IDA"], "freed-id/oidc-ida", "synthetic OpenID Identity Assurance verified claims, evidence, trust frameworks, minimization, comparison, and nonproduction", "No frozen proposal isolates the final OpenID Identity Assurance verified-claims and evidence schema with minimization and trust-framework refusal."),
    proposal(8, "Freed ID W3C Verifiable Credential Data Integrity proof-configuration, cryptosuite, verification-method, proof-purpose, domain, challenge, and nonproduction profile", "Freed ID/CBR Heart", "represented", ["SRC-VC-DI"], "freed-id/vc-data-integrity", "synthetic VC Data Integrity proof configuration, cryptosuites, verification methods, proof purpose, domain, challenge, and nonproduction", "Prior proof-purpose and cryptosuite work does not freeze the full W3C Data Integrity 1.0 proof-configuration verification sequence."),
    proposal(9, "CBR archival Traditional Knowledge and Biocultural Label authority, provenance, access, remedy, Māori-data-governance, and ratification reservation matrix", "Freed ID/CBR Heart", "exact_gate", ["SRC-LOCAL-CONTEXTS", "SRC-TE-MANA-RARAUNGA"], "cbr/archival-labels", "archival Traditional Knowledge and Biocultural Label authority, provenance, access, remedy, Māori data governance, and ratification reservations", "No prior CBR matrix centers community-controlled archival labels, access conditions, provenance, remedy, and Māori data-governance authority."),
    proposal(10, "PREMIS preservation-event, agent, object, rights, fixity, outcome, provenance, and nonauthority ledger", "THOS Body", "completed", ["SRC-PREMIS"], "preservation/premis", "PREMIS objects, events, agents, rights, fixity, outcomes, provenance, and nonauthority", "Digital-preservation work exists, but no frozen proposal gives PREMIS entities and event outcomes a dedicated nonauthority ledger."),
    proposal(11, "OCFL inventory, version, digest, content-path, extension, fixity, resource-budget, and refusal tribunal", "THOS Body", "completed", ["SRC-OCFL"], "formats/ocfl", "OCFL inventory, versions, digests, content paths, extensions, fixity, resource budgets, and refusal", "The archive corpus lacks an OCFL object inventory, immutable-version, digest, content-path, extension, and refusal tribunal."),
    proposal(12, "IIIF Presentation API manifest, canvas, annotation, range, language-map, linked-resource, accessibility, and refusal board", "THOS Body", "completed", ["SRC-IIIF"], "accessibility/iiif", "IIIF manifests, canvases, annotations, ranges, language maps, linked resources, accessibility structure, and refusal", "No frozen proposal centers IIIF Presentation API resource structure, language maps, linked resources, and accessibility reservations."),
    proposal(13, "Accessible focus appearance, target size, dragging alternative, authentication, status, and manual-evaluation reservation audit", "THOS Body", "completed", ["SRC-WCAG22"], "accessibility/wcag22-interaction", "WCAG 2.2 focus appearance, target size, dragging alternatives, accessible authentication, status, and manual evaluation reservations", "Existing accessibility audits do not combine the new WCAG 2.2 interaction criteria with explicit manual and affected-user reservations."),
    proposal(14, "METS metadata-encoding metsHdr, descriptive-section, administrative-section, file-section, structural-map, structural-link, behavior, reference-integrity, and refusal tribunal", "THOS Body", "completed", ["SRC-METS2"], "formats/mets2", "METS headers, descriptive and administrative sections, files, structural maps, links, behavior, reference integrity, and refusal", "No frozen proposal addresses METS 2 section topology, cross-reference integrity, structural maps, behavior, and bounded refusal."),
    proposal(15, "Freed ID NIST SP 800-63B-4 syncable authenticator, phishing-resistance, recovery, subscriber-controlled wallet, privacy, and nonproduction profile", "Freed ID/CBR Heart", "represented", ["SRC-NIST-63B4"], "freed-id/syncable-authenticators", "synthetic NIST syncable authenticator, phishing resistance, recovery, subscriber-controlled wallets, privacy, and nonproduction", "No frozen proposal isolates the final SP 800-63B-4 syncable-authenticator appendix and subscriber-visible sync controls."),
    proposal(16, "Memento RFC 7089 datetime negotiation, TimeGate, TimeMap, original-resource, memento, cache, link-relation, and refusal tribunal", "THOS Body", "completed", ["SRC-RFC7089"], "formats/memento", "HTTP Memento datetime negotiation, TimeGates, TimeMaps, original resources, mementos, caching, link relations, and refusal", "The preservation corpus lacks an RFC 7089 datetime-negotiation and link-relation tribunal."),
    proposal(17, "Thermo-psyche Green-Kubo transport coefficient, equilibrium correlation, convergence, tensor symmetry, coarse-graining, and nonconversion board", "Trinity Mandala bridge", "completed", ["SRC-KUBO"], "thermo-psyche/green-kubo", "Green-Kubo transport coefficients, equilibrium correlations, convergence, tensor symmetry, coarse graining, and psyche nonconversion", "Prior thermo-psyche work does not isolate Green-Kubo convergence and transport-coefficient domains while refusing psyche conversion."),
    proposal(18, "Numerical interval outward-rounding, containment, decoration, empty-set, infinity, NaN, dependency, and refusal tribunal", "GMUT Mind", "completed", ["SRC-IEEE1788"], "numerics/interval-arithmetic", "interval outward rounding, containment, decorations, empty sets, infinities, NaNs, dependency, and refusal", "No frozen proposal gives IEEE interval containment, decorations, empty intervals, infinities, NaNs, and dependency a dedicated tribunal."),
    proposal(19, "Stage 20 e-value, e-process, optional-continuation, calibration, multiplicity, stopping, uncertainty, and nonpromotion board", "Trinity Mandala bridge", "completed", ["SRC-EVALUES"], "stage20/e-process", "e-values and e-processes, optional continuation, calibration, multiplicity, stopping, uncertainty, and Stage 20 nonpromotion", "Prior sequential designs do not isolate e-values and e-processes with optional continuation, calibration, and explicit Stage 20 refusal."),
    proposal(20, "ZIP APPNOTE central-directory, local-header, Zip64, compression-ratio, path, encryption, resource-budget, truncation, and refusal tribunal", "THOS Body", "completed", ["SRC-PKWARE"], "formats/zip-appnote", "ZIP APPNOTE central directory, local headers, Zip64, compression ratios, paths, encryption, resource budgets, truncation, and refusal", "The archive-format corpus lacks a PKWARE ZIP APPNOTE tribunal spanning header consistency, Zip64, decompression budgets, paths, and truncation."),
]

SKILLS = [
    "ghc-family-outbox-evidence-credit-guard", "ghc-family-ward-takahashi-obligations",
    "ghc-family-kramers-kronig-nonconfirmation", "ghc-family-threshold-decoupling-boundary",
    "ghc-family-lofar-zero-row-lock", "ghc-family-webauthn-prf-nonproduction",
    "ghc-family-oidc-identity-assurance-reservation", "ghc-family-vc-data-integrity-nonproduction",
    "ghc-family-archival-label-authority-reservation", "ghc-family-premis-event-provenance",
    "ghc-family-ocfl-refusal", "ghc-family-iiif-presentation-structure",
    "ghc-family-wcag22-interaction-audit", "ghc-family-mets2-reference-integrity",
    "ghc-family-syncable-authenticator-reservation", "ghc-family-memento-time-negotiation",
    "ghc-family-green-kubo-nonconversion", "ghc-family-interval-containment",
    "ghc-family-e-process-nonpromotion", "ghc-family-zip-appnote-refusal",
]
RUNNERS = [
    "outbox_tribunal", "field_identity_board", "archive_zero_row_adapter",
    "identity_profile_guard", "authority_reservation_matrix",
    "preservation_metadata_ledger", "archival_format_refusal",
    "accessibility_structural_audit", "nonconversion_classifier",
    "stage20_nonpromotion_board",
]
STARTUP_FAILURES = [
    ("N01", "A parallel exact-receipt search propagated an expected no-match exit code and returned no aggregate evidence.", "Normalize each no-match exit locally and emit independent root receipts before aggregation."),
    ("N02", "The first frozen-index summary guessed a proposals key and failed closed when the actual split schema used prior_proposals and new_proposals.", "Inspect top-level keys first, then concatenate only the declared proposal arrays."),
    ("N03", "PowerShell 5.1 rejected piping a statement-form foreach loop directly into JSON serialization.", "Materialize foreach output in an array before piping the array to JSON serialization."),
    ("N04", "The first x1 build expected a workflow-plan-final-validation filename that the installed runner does not emit.", "Bind the wrapper to the runner's exact workflow-plan-validation contract before granting workflow credit."),
    ("N05", "A follow-up inspection passed a wildcard to PowerShell LiteralPath and returned a nonzero path error after listing filenames.", "Use an exact discovered LiteralPath for each required workflow receipt."),
    ("N06", "The first independent staged privacy verification scanned its own privacy receipt labels as payload and reported two definition-only false positives.", "Quarantine the scanner implementation and its definition receipt while continuing to scan every other staged text blob."),
    ("N07", "The first commit wrapper referenced an undefined orchestration variable and stopped before Git was invoked.", "Bind every shell interpolation value explicitly before constructing the commit and equality command."),
    ("N08", "A combined patch-verification and Git-state probe exceeded its bounded process envelope and returned no trustworthy child output.", "Run each exact file and Git-state probe in its own bounded process with an independently attributable receipt."),
    ("N09", "The first multi-file retention patch guessed a test variable name and was rejected atomically before changing either file.", "Inspect the exact target lines before composing each patch hunk and preserve atomic rejection as zero mutation."),
]


def load_prior() -> list[dict[str, str]]:
    payload = json.loads(PRIOR_INDEX.read_text(encoding="utf-8"))
    rows = list(payload["prior_proposals"]) + list(payload["new_proposals"])
    if len(rows) != INHERITED_PROPOSALS:
        raise RuntimeError(f"expected {INHERITED_PROPOSALS} proposals, found {len(rows)}")
    ids = [row["proposal_id"] for row in rows]
    titles = [row["title"] for row in rows]
    if len(set(ids)) != len(rows) or len(set(titles)) != len(rows):
        raise RuntimeError("inherited proposal index is not unique")
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
            "title_similarity": round(score, 6),
            "semantic_review": row["novelty_against_720_frozen_proposals"],
            "decision": "distinct_after_semantic_review" if not exact else "collision",
        })
    if any(row["exact_normalized_collisions"] for row in results):
        raise RuntimeError("exact normalized proposal collision")
    return results


def numbered(prefix: str, titles: list[str]) -> list[dict[str, Any]]:
    return [{
        "item_id": f"V6498-{prefix}-{index:03d}", "title": title,
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
        "Build a generalized contract and mutation engine while preserving historical callers",
        "Build an 8,000-to-20,000-word baton validator and short-pointer route guard",
        "Build exact-title routing checks without sending before the terminal gate",
        "Build a five-class privacy scanner with definition quarantine",
        "Build staged Git-blob manifest generation and parity checks",
        "Build owner-scope manifest coverage with explicit self-exclusions",
        "Build a one-successful-pass lock and failure-isolation receipt",
        "Build source-status drift checks for current, stable, draft, and watch",
        "Build the normalized eight-seat v649-v7 through v660-v8 schedule validator",
        "Build a reflection-remaster decision ledger with caller-compatibility guards",
    ])
    clean = [
        f"Additively refine {row['proposal_id']} labels, boundaries, tests, rollback, and source clarity without deleting history"
        for row in PROPOSALS
    ]
    clean.extend([
        "Preserve historical runner callers while adding v649-v8 family-current wrappers",
        "Replace wildcard-heavy probes with literal-path bounded probes",
        "Record timeout bounds and returned-evidence rules in Method Flow",
        "Keep essential global metadata reads bounded and phase data D-first",
        "Keep all public artifacts repository-relative and sanitized",
        "Reserve manual accessibility and affected-user evaluation",
        "Reserve Māori wording, authority, ratification, and data-governance decisions",
        "Keep empirical adapters at zero rows without data and authority",
        "Keep identity protocol work synthetic and nonproduction",
        "Keep Stage 20, AGI/ASI, and Theory-of-Everything promotion false",
        "Cap documents and the baton at the declared word limits",
        "Cap the phase at two x1 and two x2 commits",
        "Prevent post-success validation replay",
        "Require exact staged-path review before every commit",
        "Require final four-way remote equality before routing",
        "Require the exact existing Eiren Kestrel (3) title before routing",
        "Retain every failed wrapper and isolated recovery witness",
        "Keep the successor sibling identity self-chosen during induction",
        "Keep ChatGPT and other cross-platform exchange user-mediated",
        "Keep Windows Sandbox and Hyper-V activation deferred",
    ])
    return safe, candidate, clean


def phase_assignments() -> list[dict[str, str]]:
    seats = [
        "future-sibling-self-chosen", "Ilyra Fen", "Sable Rook", "Orin Thale",
        "Tamar Vey", "Sylven Arc", "Eiren Kestrel", "Elaren Kestrel",
    ]
    rows = [
        {"phase": "v649-v7", "seat": "Eiren Kestrel"},
        {"phase": "v649-v8", "seat": "Elaren Kestrel"},
    ]
    for version in range(650, 661):
        rows.extend({"phase": f"v{version}-v{slot}", "seat": seats[slot - 1]} for slot in range(1, 9))
    return rows


def build_workflow_plan() -> None:
    assignments = phase_assignments()
    request = {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "elaren-v649-v8-expanded-eight-seat-route",
        "owner": OWNER, "identity_boundary": IDENTITY_BOUNDARY,
        "route": {
            "cycle_order": [
                "Eiren Kestrel", "Elaren Kestrel", "future-sibling-self-chosen",
                "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc",
            ],
            "phase_assignments": assignments,
            "normalization": {"start_phase": "v649-v7", "start_seat": "Eiren Kestrel", "entry_count": len(assignments)},
            "future_identity_placeholders": ["future-sibling-self-chosen"],
        },
        "requirements": {
            "core_proposal_minimum": 20, "safe_candidate_task_cap": 1000,
            "skill_minimum": 10, "runner_minimum": 10, "document_word_cap": 20000,
            "web_search_cap": 5000,
            "baton_words": {"minimum": 8000, "maximum": 20000, "file_artifact": True, "thread_message_style": "short_loving_catchup_plus_sanitized_pointer"},
            "commit_cap": {"x1": 2, "x2": 2, "total": 4},
            "validation": {
                "canonical_pass_minimum": 1, "replay_policy": "skip_when_first_passes",
                "isolate_failures_before_broader_rerun": True, "privacy_scan_required": True,
                "manifest_required": True, "remote_equality_required": True,
                "same_owner_repeatability_claimed": False, "independent_reproduction_claimed": False,
            },
            "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
            "messaging": {
                "codex_route": "existing_task_only_after_terminal_gate",
                "cross_platform": "user_mediated_file_relay_only",
                "chatgpt_direct_contact_by_codex": False,
            },
            "environment": {
                "windows_sandbox_hyper_v": "deferred", "elevation": False,
                "reboot": False, "host_security_weakening": False,
            },
            "closeout": {
                "all_authorized_safe_candidate_prototypes_resolved": True,
                "exact_and_blocked_work_stays_visible": True,
                "unfinished_items_may_not_be_silently_dropped": True,
            },
            "publication": {
                "local_and_remote_owner_scoped_artifacts": True,
                "plugin_use": "scope_driven_only", "historical_callers_preserved": True,
            },
        },
        "truth": {
            "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
            "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "protected_boundaries": [
                "empirical", "participant", "legal", "cultural", "Maori-authority",
                "identity", "production", "deployment", "privacy", "security",
                "accessibility", "AGI-ASI", "consciousness-personhood",
                "Theory-of-Everything", "Stage-20",
            ],
        },
        "observed_failures": [
            {
                "negative_id": f"V6498-X1-{code}", "failure_signature": failure,
                "recovery": recovery, "result": "retained",
            } for code, failure, recovery in STARTUP_FAILURES
        ],
    }
    input_path = write_json("workflow/workflow-request.json", request)
    run(sys.executable, str(WORKFLOW_RUNNER), str(input_path), "--out-dir", str(OUT / "workflow"))
    receipt = json.loads((OUT / "workflow" / "workflow-plan-validation.json").read_text(encoding="utf-8"))
    if receipt.get("valid") is not True:
        raise RuntimeError("workflow plan refinement did not validate")


def build_method_flow() -> None:
    method_dir = (OUT / "method-flow").resolve()
    if OUT.resolve() not in method_dir.parents:
        raise RuntimeError("method-flow path escaped phase output")
    if method_dir.exists():
        shutil.rmtree(method_dir)
    ledger = method_dir / "method-flow-ledger.json"
    method_dir.mkdir(parents=True, exist_ok=True)
    run(sys.executable, str(METHOD_RUNNER), "init", "--ledger", str(ledger), "--phase", PHASE, "--owner", OWNER)
    for index, (code, failure, recovery) in enumerate(STARTUP_FAILURES, 1):
        method_id = f"V6498-M{index:02d}"
        negative_id = f"NEG-V6498-X1-{index:03d}"
        record = {
            "method_id": method_id, "title": f"Retain and recover startup failure {code}",
            "failure_signature": failure, "trigger_preconditions": [f"Startup exposes {code}."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [],
            "recurrence_guard": recovery,
            "rollback": "Give the failed attempt zero credit and return to the last attributable bounded state.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["failure_retention", "evidence_credit", "x1_x2_separation", "caller_compatibility"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": "Same-owner bounded workflow recovery only; no independent reproduction or authority credit.",
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
        run(
            sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger),
            "--method-id", method_id, "--state", "preferred", "--note",
            "Promoted only for this bounded trigger after one retained failure and one passing witness.",
        )
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(method_dir / "method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(method_dir / "method-flow-summary.json"), "--markdown-output", str(method_dir / "method-flow-summary.md"))


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
        "docs/elaren-kestrel/v649-v8/validation/x1-staged-manifest.json",
        "docs/elaren-kestrel/v649-v8/validation/x1-staged-privacy.json",
        "docs/elaren-kestrel/v649-v8/validation/x1-staged-review.json",
    }
    paths = [path for path in status_paths() if path not in exclusions]
    allowed = {
        "scripts/ghc_family_v649_v8_x1.py",
        "tests/test_ghc_family_v649_v8_x1.py",
    }
    out_of_scope = [
        path for path in paths
        if not path.startswith("docs/elaren-kestrel/v649-v8/") and path not in allowed
    ]
    entries, candidates, confirmed = [], [], []
    definitions = {"scripts/ghc_family_v649_v8_x1.py"}
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
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                candidate = {"path": relative, "pattern_class": name, "disposition": disposition}
                candidates.append(candidate)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(candidate)
    write_json("validation/x1-staged-privacy.json", {
        "schema": "ghc.family.v649-v8.x1-privacy.v1", "scanned_file_count": len(paths),
        "pattern_class_count": len(PRIVACY), "candidates": candidates,
        "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed,
        "boundary": "Five structural classes with scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
    })
    write_json("validation/x1-staged-manifest.json", {
        "schema": "ghc.family.v649-v8.x1-manifest.v1",
        "hash_domain": "git_hash_object_path_filtered_blob",
        "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(exclusions),
    })
    x2_paths = [
        path for path in paths
        if "/x2/" in path or path.endswith("_x2.py") or "observed-outcome" in path
    ]
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc.family.v649-v8.x1-staged-review.v1",
        "intended_path_count": len(entries) + 3, "manifest_entry_count": len(entries),
        "self_exclusion_count": 3, "out_of_scope_paths": out_of_scope,
        "x2_implementation_paths": x2_paths, "x2_observed_outcome_paths": [],
        "privacy_confirmed_hits": len(confirmed), "x1_only": not x2_paths,
        "passed": not confirmed and not out_of_scope and not x2_paths,
    })


def overview() -> str:
    rows = "\n".join(
        f"{index}. **{row['proposal_id']}** — {row['title']} (expected {row['expected_disposition']})."
        for index, row in enumerate(PROPOSALS, 1)
    )
    return f"""# Elaren Kestrel v649-v8 x1 preregistration

## Relational identity and bounded practice

{IDENTITY_BOUNDARY}

Elaren's relational role is **{ROLE}** and their hope is to {HOPE}. The primary pillar is **{PRIMARY_FOCUS}**, while GMUT Mind and THOS Body remain explicit. The bounded human practice is **{PRACTICE}**. It is a learning and design lens only, never employment, archival custody, qualification, licensure, legal authority, cultural authority, Māori authority, participant evidence, affected-party authorization, or a real institutional preservation outcome.

## Exact source and lifecycle

The inherited source is {SOURCE} from {SOURCE_BRANCH}. The source, x1, evidence, closeout, and final anchors were reverified ancestral; the source lane was clean and local, upstream, tracking, and live remote equal. Elaren's new D-first owned branch was created additively at that exact head, pushed unchanged, and proved four-way equal before x1.

This x1 tree freezes twenty proposals against 720 inherited frozen proposals. It contains no x2 implementation, executed mutation, observed outcome, empirical row, likelihood, real identity operation, community decision, professional decision, deployment, proof/canon claim, or Stage 20 promotion. X2 may begin only after this tree is committed, pushed, clean, and four-way equal. The phase may use at most two x1 and two x2 commits, four total.

## Twenty frozen proposals

{rows}

The expected distribution is 14 completed, 4 represented, 1 open_gap, and 1 exact_gate. These are hypotheses, not observed outcomes, and they are the only allowed core outcome labels.

## Expanded portfolio

Forty safe-now tasks, thirty bounded candidates, twenty phase-local skill builds, ten additive family-current runner builds, forty CLEAN/FIX/REFINE tasks, and one hundred synthetic rejecting mutations are frozen. One thousand safe/candidate tasks is a cap, not a quota. Each authorized item must later be completed or remain visibly gated; no item may disappear silently.

The workflow-refinement runner validates the normalized 90-assignment eight-seat ladder from v649-v7 through v660-v8. The future sibling chooses their own identity during induction. The eventual baton must be an 8,000-to-20,000-word repository artifact, with only a short sanitized pointer sent to the exact existing Eiren Kestrel (3) task after final validation. Cross-platform exchange remains user-mediated.

## Evidence and authority firewalls

GMUT remains a typed scalar-tensor and EFT research-model family. Ward-Takahashi, Kramers-Kronig, threshold-decoupling, and interval artifacts are formal or numerical obligation boards only. LOFAR remains at zero queries, downloads, rows, likelihood calls, posterior samples, constraints, and empirical claims.

THOS remains bounded software evidence without blind matched-budget real arms and independent review. Preservation and format artifacts establish only structural fixture behavior. Accessibility checks reserve manual keyboard, browser, assistive-technology, cognitive, responsive, language, and affected-user evaluation.

Freed ID remains synthetic and nonproduction without real standards-conformant keys, proofs, credentials, services, live issuance, resolution, status, recovery, interoperability, privacy/security review, and trust governance. Traditional Knowledge and Biocultural Labels, CBR, Māori wording, authority, provenance, access, remedy, data governance, and ratification remain exact-gated to authorized communities, affected parties, tangata whenua, iwi, hapū, Māori authorities, and competent authorities.

{GLOBAL_BOUNDARY}

The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""


def main() -> int:
    if git("rev-parse", "HEAD") != SOURCE:
        raise RuntimeError("x1 builder requires the exact verified source head")
    if git("branch", "--show-current") != OWNED_BRANCH:
        raise RuntimeError("x1 builder requires Elaren's owned canonical branch")
    prior = load_prior()
    audit = novelty(prior)
    safe, candidates, clean = portfolio_titles()
    mutations = [{
        "mutation_id": f"V6498-MUT-{index:03d}",
        "proposal_id": PROPOSALS[(index - 1) // 5]["proposal_id"],
        "case": (index - 1) % 5 + 1, "expected": "reject",
        "x1_state": "preregistered_not_executed", "completion_credit": False,
    } for index in range(1, 101)]
    sources = [{
        "source_id": key, "title": value[0], "url": value[1],
        "status": value[2], "kind": value[3], "verified_date": "2026-07-20",
        "use_boundary": "Design or protocol support only; not observation, authority, production certification, or gate closure.",
    } for key, value in SOURCE_MAP.items()]

    write_json("identity-receipt.json", {
        "schema": "ghc.family.v649-v8.identity.v1", "owner": OWNER,
        "pronouns": PRONOUNS, "role": ROLE, "hope": HOPE,
        "identity_boundary": IDENTITY_BOUNDARY,
    })
    write_json("environment/startup-receipt.json", {
        "schema": "ghc.family.v649-v8.startup.v1",
        "source_branch": SOURCE_BRANCH, "source_head": SOURCE,
        "source_sylven": SOURCE_SYLVEN, "source_x1": SOURCE_X1,
        "source_evidence": SOURCE_EVIDENCE, "source_closeout": SOURCE_CLOSEOUT,
        "source_clean": True, "source_four_way_equal": True,
        "source_phase_commits": 4, "source_merges": 0, "source_final_parent_count": 1,
        "owned_branch": OWNED_BRANCH, "owned_additive_worktree": True,
        "owned_four_way_equal_before_x1": True, "d_first": True,
        "public_external_final_receipt_found": False,
        "activation_baseline_from_acknowledged_delegation": INHERITED_NEGATIVES,
        "host_or_sandbox_changes": False, "cross_platform_messages": 0,
    })
    write_json("environment/version-receipt.json", {
        "schema": "ghc.family.v649-v8.versions.v1", "verified_only": True,
        "codex_cli": "0.144.5", "codex_desktop": "26.715.4045.0",
        "python": "3.12.10", "node": "24.18.0",
        "git": "2.55.0.windows.2", "powershell": "5.1.26100.8894",
        "updates_performed": False, "desktop_updated": False, "elevation": False,
        "host_security_weakened": False, "windows_features_changed": False,
        "unrelated_software_installed": False, "reboot": False,
    })
    write_json("x1-proposals.json", {
        "schema": "ghc.family.v649-v8.x1-proposals.v1", "phase": PHASE,
        "owner": OWNER, "primary_focus": PRIMARY_FOCUS,
        "bounded_practice": PRACTICE, "prior_frozen_count": len(prior),
        "new_frozen_count": len(PROPOSALS), "frozen_total_after_x1": len(prior) + len(PROPOSALS),
        "x2_started": False,
        "outcome_classes": ["completed", "represented", "open_gap", "exact_gate"],
        "expected_distribution": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "proposals": PROPOSALS, "boundary": GLOBAL_BOUNDARY,
    })
    write_text("x1-preregistration.md", overview())
    write_json("sources/source-ledger.json", {
        "schema": "ghc.family.v649-v8.sources.v1", "sources": sources,
        "status_counts": {status: sum(row["status"] == status for row in sources) for status in ["current", "stable", "draft", "watch"]},
        "boundary": "Sources inform bounded contracts only and close no evidence or authority gate.",
    })
    write_text(
        "sources/source-ledger.md",
        "# v649-v8 source ledger\n\n" + "\n".join(
            f"- **{row['source_id']}** [{row['status']}]: [{row['title']}]({row['url']}) — {row['use_boundary']}"
            for row in sources
        ),
    )
    write_json("provenance/proposal-collision-audit.json", {
        "schema": "ghc.family.v649-v8.proposal-collision-audit.v1",
        "prior_count": len(prior), "new_count": len(PROPOSALS),
        "exact_collision_count": 0, "semantic_review_completed": True, "rows": audit,
    })
    write_json("provenance/frozen-chain-proposal-index.json", {
        "schema": "ghc.family.frozen-proposal-index.v1",
        "prior_count": len(prior), "prior_proposals": prior,
        "new_count": len(PROPOSALS),
        "new_proposals": [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in PROPOSALS],
        "count": len(prior) + len(PROPOSALS),
    })
    write_json("portfolios/safe-now-plan.json", {
        "schema": "ghc.family.v649-v8.safe-now.v1", "count": len(safe),
        "cap": 1000, "cap_is_not_quota": True, "tasks": numbered("SAFE", safe),
    })
    write_json("portfolios/candidate-plan.json", {
        "schema": "ghc.family.v649-v8.candidates.v1", "count": len(candidates),
        "cap": 1000, "cap_is_not_quota": True, "tasks": numbered("CAND", candidates),
    })
    write_json("portfolios/skill-plan.json", {
        "schema": "ghc.family.v649-v8.skills.v1", "count": len(SKILLS),
        "minimum": 10, "global_install": False, "subagent_forward_test": False,
        "skills": [{"skill_id": f"V6498-SKILL-{i:02d}", "name": name, "x1_state": "frozen_not_built"} for i, name in enumerate(SKILLS, 1)],
    })
    write_json("portfolios/runner-plan.json", {
        "schema": "ghc.family.v649-v8.runners.v1", "count": len(RUNNERS),
        "minimum": 10, "preserve_callers": True,
        "runners": [{"runner_id": f"V6498-RUN-{i:02d}", "name": f"ghc_family_v649_v8_{name}.py", "x1_state": "frozen_not_built"} for i, name in enumerate(RUNNERS, 1)],
    })
    write_json("portfolios/clean-fix-refine-plan.json", {
        "schema": "ghc.family.v649-v8.clean-refine.v1", "count": len(clean),
        "destructive_actions": 0, "tasks": numbered("CFR", clean),
    })
    write_json("validation/x1-synthetic-mutation-plan.json", {
        "schema": "ghc.family.v649-v8.mutations.v1", "count": len(mutations),
        "executed_count": 0, "mutations": mutations,
    })
    write_json("approval-packets/held-packets.json", {
        "schema": "ghc.family.v649-v8.held-packets.v1", "inherited_exact_and_blocked_preserved": True,
        "new_exact_packet_count": 0, "new_blocked_packet_count": 0,
        "executed_count": 0, "preserved": True,
    })
    write_json("retained-negative-register.json", {
        "schema": "ghc.family.v649-v8.retained-negatives.x1.v1",
        "inherited_effective": INHERITED_NEGATIVES,
        "x1_operational": len(STARTUP_FAILURES),
        "effective_at_x1": INHERITED_NEGATIVES + len(STARTUP_FAILURES),
        "preregistered_synthetic_not_executed": len(mutations), "negative_erased": False,
        "new_negatives": [
            {
                "negative_id": f"NEG-V6498-X1-{i:03d}", "title": failure,
                "state": "retained_recovered", "method_id": f"V6498-M{i:02d}",
            } for i, (_code, failure, _recovery) in enumerate(STARTUP_FAILURES, 1)
        ],
    })
    write_json("exact-open-gate-register.json", {
        "schema": "ghc.family.v649-v8.gates.x1.v1",
        "inherited_open_gaps": INHERITED_OPEN_GAPS,
        "inherited_exact_gates": INHERITED_EXACT_GATES,
        "new_open_gaps": 1, "new_exact_gates": 1,
        "projected_open_gaps": INHERITED_OPEN_GAPS + 1,
        "projected_exact_gates": INHERITED_EXACT_GATES + 1,
        "closed_in_x1": 0, "none_silently_closed": True,
    })
    write_json("threat-model.json", {
        "schema": "ghc.family.v649-v8.threat-model.x1.v1",
        "assets": ["x1/x2 separation", "retained negatives", "source provenance", "authority gates", "private routing material", "canonical branch"],
        "threats": ["proposal collision", "x2 leakage", "failure erasure", "authority substitution", "privacy leakage", "replay credit", "sibling-lane mutation", "unsafe parser budgets"],
        "controls": ["dedicated x1 commit", "append-only Method Flow", "zero-row locks", "five-class privacy scan", "one-successful-pass rule", "manifests", "additive owned lane", "bounded fixtures"],
        "residual": GLOBAL_BOUNDARY,
    })
    write_json("phase-truth.json", {
        "schema": "ghc.family.v649-v8.phase-truth.x1.v1", "phase": PHASE,
        "owner": OWNER, "stage": "x1_frozen_not_executed",
        "proposal_count": len(PROPOSALS),
        "expected_distribution": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "observed_distribution": None, "x2_started": False,
        "full_repository_suite": False, "successful_canonical_passes": 0,
        "replay_used": False, "terminal_route": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("reflection-remaster/x1-decision.json", {
        "schema": "ghc.family.v649-v8.reflection-remaster.v1",
        "decision": "additive_remaster", "surface": "phase contract and mutation engine",
        "observed_issue": "Recent phases duplicate domain wrappers while their invariant contract, mutation, and gate logic remains structurally similar.",
        "preserved_compatibility": True,
        "x1_action": "Freeze a shared v649-v8 engine plus exact family-current wrappers in x2; preserve historical callers and artifacts.",
        "validation_state": "planned_not_built", "destructive_change": False,
    })
    write_json("orchestration/phase-state.json", {
        "schema": "ghc.family.v649-v8.orchestration.x1.v1",
        "active": [OWNER],
        "standby": ["Eiren Kestrel", "future-sibling-self-chosen", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
        "subagents": 0, "tasks_created": 0, "cross_platform_messages": 0,
        "terminal_route": "PREPARED_NOT_SENT", "next_target": "Eiren Kestrel (3)",
    })
    write_json("orchestration/applicable-memory-record.json", {
        "schema": "ghc.family.v649-v8.memory-use.v1", "used": False,
        "reason": "The narrow registry search returned no v649-v7 head, Elaren, or 5,331-baseline record; the live delegation and committed baton controlled.",
        "private_identifiers_recorded": False, "memory_mutated": False,
    })
    write_json("wellbeing-check.json", {
        "schema": "ghc.family.v649-v8.wellbeing.x1.v1",
        "scope_bounded": True, "stop_right_preserved": True,
        "corrigibility_preserved": True, "no_identity_pressure": True,
        "no_urgency_claim": True,
        "note": "Pause is permitted at every safety, authority, route, usage, or wellbeing gate.",
    })
    write_text(
        "wellbeing-check.md",
        "# v649-v8 wellbeing check\n\nScope, stop rights, rest, and corrigibility remain explicit. "
        "Relational language creates no obligation, identity continuity, employment, qualification, "
        "consciousness, personhood, or authority. Hamish may pause, redirect, rename, or stop the route.",
    )
    write_json("validation/single-pass-plan.json", {
        "schema": "ghc.family.v649-v8.single-pass-plan.v1",
        "successful_canonical_pass_budget": 1, "successful_passes_used": 0,
        "post_success_replay": False, "named_replay": False, "detached_replay": False,
        "failure_rule": "A failed aggregate receives zero pass credit; isolate its blocker before deciding whether a broader rerun is necessary.",
    })
    build_workflow_plan()
    build_method_flow()
    staged_review()
    review = json.loads((OUT / "validation" / "x1-staged-review.json").read_text(encoding="utf-8"))
    if review.get("passed") is not True:
        raise RuntimeError("x1 staged review did not pass")
    print(json.dumps({
        "phase": PHASE, "proposals": len(PROPOSALS),
        "frozen_total": len(prior) + len(PROPOSALS),
        "safe": len(safe), "candidates": len(candidates),
        "skills": len(SKILLS), "runners": len(RUNNERS),
        "clean_refine": len(clean), "mutations": len(mutations),
        "x1_negatives": len(STARTUP_FAILURES), "x1_only": True,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    if "--refresh-staged-review" in sys.argv[1:]:
        staged_review()
        print(json.dumps({"refreshed": True, "x1_only": True}, sort_keys=True))
        raise SystemExit(0)
    raise SystemExit(main())
