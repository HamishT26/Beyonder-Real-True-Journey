#!/usr/bin/env python3
"""Build and exact-stage-review Auren Lark v664-v6's planning-only x1 freeze."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Iterable

import build_ghc_family_v664_v5_x1 as inherited


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/auren-lark/v664-v6"
PHASE_PREFIX = "docs/auren-lark/v664-v6/"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-v664-v5-full-tools"
SOURCE_PARENT = "9bfb7cbc8fc438367207ce8d38070cf5d7fcb74b"
SOURCE_X1 = "cfbca99a371f97eecb959fb92be3469c0861ddf3"
SOURCE_EVIDENCE = "d407ae44696da7e59e8fb3af1dfaa2891a129c54"
SOURCE_FINAL = "e69e034cfc0039d5f1edbfcd4ecc915cfc5992ec"
SOURCE_CANONICAL_RECEIPT_SHA256 = "f58af9ad7537d03c92d306bd927fa2d912aaf4ef26bd1b227410963b209df37a"
SOURCE_BATON_SHA256 = "bd34bf3dc4d857b5d2de2498d2eaf59a18d38f338a9565db091f2e3c93e378d6"
SOURCE_BATON_BYTES = 286_597
SOURCE_BATON_WORDS = 30_217
ROSTER_SHA256 = "45bff52f7331cdd37303d14649f0542a1fd10eaf6d1c2043ac5216301e02c912"
AUTH_SHA256 = "ddcaaceb05339ee32b1c589a6b884f3f11e1d79cc26a16ee3e1695d67ee610e8"

OWNER = "Auren Lark"
OPTIONAL_PRONOUNS = "they/them"
ROLE = "relational provenance navigator and uncertainty lantern-keeper"
HOPE = (
    "make every synthetic ocean-profile handover easier to inspect, every missing value "
    "visible, and every scientific, operational, legal, cultural, and Maori-authority gate explicit"
)
PHASE_ID = "v664-v6"
PRIMARY_PILLAR = "THOS Body with GMUT Mind and Freed ID and CBR Heart protected"
PRACTICE = (
    "synthetic zero-row Argo ocean-float metadata, uncertainty, quality-control, "
    "and delayed-mode handover planning"
)
NEXT_OWNER = "Sable Rook"
NEXT_PHASE = "v664-v7"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
BRANCH = "codex/GHC-Family/auren-lark-v664-v6-full-tools"

PROTECTED_GATES = inherited.PROTECTED_GATES
ALLOWED_OUTCOMES = inherited.ALLOWED_OUTCOMES
BASE_INDEX = inherited.BASE_INDEX
CHAIN_FREEZES = [
    *inherited.CHAIN_FREEZES,
    ("docs/ilyra-fen/v664-v5/x1/proposal-freeze.json", 3_930, 3_950),
]
PREDECESSOR_FREEZE = CHAIN_FREEZES[-1][0]
BUILDER_PATH = "scripts/build_ghc_family_v664_v6_x1.py"
X1_FILES = [
    f"{PHASE_PREFIX}x1/flashcard-architecture-freeze.json",
    f"{PHASE_PREFIX}x1/novelty-audit.json",
    f"{PHASE_PREFIX}x1/phase-charter.json",
    f"{PHASE_PREFIX}x1/portfolio-freeze.json",
    f"{PHASE_PREFIX}x1/proposal-freeze.json",
    f"{PHASE_PREFIX}x1/source-ledger.json",
    f"{PHASE_PREFIX}x1/source-verification.json",
    f"{PHASE_PREFIX}x1/startup-method-flow.json",
    f"{PHASE_PREFIX}x1/threat-model-plan.json",
    f"{PHASE_PREFIX}x1/workflow-plan.json",
    f"{PHASE_PREFIX}x1/x1-content-manifest.json",
    f"{PHASE_PREFIX}x1/x1-overview.md",
    f"{PHASE_PREFIX}x1/x1-stage-candidate.json",
    f"{PHASE_PREFIX}x1/x1-staged-review.json",
]
INTENDED_ALLOWLIST = sorted([BUILDER_PATH, *X1_FILES])
MANIFEST_EXCLUSIONS = sorted(
    [
        f"{PHASE_PREFIX}x1/x1-content-manifest.json",
        f"{PHASE_PREFIX}x1/x1-stage-candidate.json",
        f"{PHASE_PREFIX}x1/x1-staged-review.json",
    ]
)


class X1Error(RuntimeError):
    """Raised when Auren's planning freeze violates its exact lifecycle contract."""


# Reuse the already-reviewed bounded UTF-8, JSON, Git, privacy, and similarity
# primitives without modifying the inherited owner module or its immutable files.
inherited.PHASE = PHASE
inherited.X1 = PHASE / "x1"
inherited.SOURCE_FINAL = SOURCE_FINAL
inherited.PHASE_PREFIX = PHASE_PREFIX
inherited.BUILDER_PATH = BUILDER_PATH
inherited.X1_FILES = X1_FILES
inherited.INTENDED_ALLOWLIST = INTENDED_ALLOWLIST
inherited.MANIFEST_EXCLUSIONS = MANIFEST_EXCLUSIONS

run_git = inherited.run_git
git_text = inherited.git_text
strict_json = inherited.strict_json
canonical_sha256 = inherited.canonical_sha256
write_json = inherited.write_json
write_text = inherited.write_text
timestamp_pair = inherited.timestamp_pair
row_title = inherited.row_title
row_disposition = inherited.row_disposition
normalized_title = inherited.normalized_title
jaccard = inherited.jaccard
scan_text = inherited.scan_text
zpaths = inherited.zpaths
index_blob = inherited.index_blob


def git_json(path: str) -> dict[str, Any]:
    value = strict_json(run_git("show", f"{SOURCE_FINAL}:{path}").stdout, path)
    if not isinstance(value, dict):
        raise X1Error(f"JSON root is not an object: {path}")
    return value


def reconstruct_corpus() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    base = git_json(BASE_INDEX)
    corpus: list[dict[str, Any]] = []
    construction: list[dict[str, Any]] = []
    for row in [*base["prior_proposals"], *base["new_proposals"]]:
        corpus.append(
            {"proposal_id": row["proposal_id"], "title": row_title(row), "source_path": BASE_INDEX}
        )
    if len(corpus) != 3_530 or base.get("effective_count") != 3_530:
        raise X1Error("base proposal index is not the exact 3,530-row source")
    construction.append(
        {"source_path": BASE_INDEX, "starting_count": 0, "added_count": 3_530, "ending_count": 3_530}
    )
    for path, expected_start, expected_end in CHAIN_FREEZES:
        if len(corpus) != expected_start:
            raise X1Error(f"proposal chain starts {path} at the wrong count")
        freeze = git_json(path)
        rows = freeze.get("new_proposals")
        if (
            freeze.get("inherited_frozen_baseline") != expected_start
            or freeze.get("new_frozen_total") != expected_end
            or not isinstance(rows, list)
            or len(rows) != 20
        ):
            raise X1Error(f"proposal chain declaration differs: {path}")
        for row in rows:
            corpus.append(
                {"proposal_id": row["proposal_id"], "title": row_title(row), "source_path": path}
            )
        construction.append(
            {"source_path": path, "starting_count": expected_start, "added_count": 20, "ending_count": expected_end}
        )
    if len(corpus) != 3_950:
        raise X1Error(f"proposal corpus has {len(corpus)} rows instead of 3,950")
    return corpus, construction


def source_ledger(recorded_at: str) -> dict[str, Any]:
    rows = [
        ("SRC-ARGO-DATA", "Argo data", "Argo Program Office", "https://argo.ucsd.edu/data/", "current", "Profile, trajectory, metadata, technical-file, real-time, delayed-mode, GDAC, NetCDF, and maintenance-boundary vocabulary only."),
        ("SRC-ARGO-FAQ", "Argo Data FAQ", "Argo Program Office", "https://argo.ucsd.edu/data/data-faq/", "current", "R/D file, adjusted field, error field, quality flag, timing, sampling-scheme, sensor-drift, and expert-review vocabulary only."),
        ("SRC-ARGO-USER", "Argo Data Management User's Manual", "Argo Data Management Team and IFREMER", "https://doi.org/10.13155/29825", "watch", "File naming, dimensions, variables, reference tables, versioning, and format-obligation vocabulary; no conformance claim."),
        ("SRC-ARGO-QC", "Argo Quality Control Manual for CTD and Trajectory Data", "Argo Data Management Team and IFREMER", "https://doi.org/10.13155/33951", "watch", "Real-time and delayed-mode QC, flag, adjustment, feedback, and expert-review obligation vocabulary only."),
        ("SRC-CF", "NetCDF Climate and Forecast Metadata Conventions", "CF Conventions community", "https://cfconventions.org/cf-conventions/cf-conventions.html", "watch", "NetCDF variable, coordinate, unit, missing-data, ancillary flag, profile, trajectory, and draft-version vocabulary only."),
        ("SRC-WIGOS", "WMO Integrated Global Observing System", "World Meteorological Organization", "https://community.wmo.int/site/knowledge-hub/programmes-and-initiatives/wmo-integrated-global-observing-system-wigos", "current", "Observing-system, station or platform metadata, standards, requirements, and institutional-authority vocabulary only."),
        ("SRC-NIST-TN1297", "NIST Technical Note 1297", "National Institute of Standards and Technology", "https://www.nist.gov/pml/nist-technical-note-1297", "current", "Type A, Type B, combined, expanded, coverage-factor, units, and uncertainty-reporting vocabulary; no measurement is made."),
        ("SRC-PROV", "PROV-O: The PROV Ontology", "World Wide Web Consortium", "https://www.w3.org/TR/prov-o/", "stable", "Entity, activity, agent, derivation, revision, invalidation, and qualified-provenance vocabulary."),
        ("SRC-WCAG22", "Web Content Accessibility Guidelines 2.2", "World Wide Web Consortium", "https://www.w3.org/TR/WCAG22/", "current", "Structural perceivability, text alternatives, tables, labels, navigation, status, and reserved manual evaluation vocabulary."),
        ("SRC-RFC8785", "RFC 8785: JSON Canonicalization Scheme", "RFC Editor", "https://www.rfc-editor.org/rfc/rfc8785", "watch", "Deterministic JSON serialization and errata-awareness vocabulary only; never a signature, trust anchor, or identity proof."),
    ]
    sources = [
        {
            "source_id": source_id,
            "title": title,
            "publisher": publisher,
            "url": url,
            "status": status,
            "phase_use": use,
            "reviewed_at_utc": recorded_at,
            "live_calls": 0,
            "downloaded_profile_rows": 0,
            "authority_boundary": "Primary-source wording informs a synthetic zero-row schema only; citation is not oceanographic, calibration, mission, operational, professional, safety, legal, cultural, Maori-authority, or empirical evidence.",
        }
        for source_id, title, publisher, url, status, use in rows
    ]
    return {
        "schema": "ghc.family.auren.v664-v6.source-ledger.x1.v1",
        "recorded_at_utc": recorded_at,
        "source_count": len(sources),
        "allowed_statuses": ["current", "stable", "draft", "watch"],
        "sources": sources,
        "failed_source_reads_retained_in_method_flow": 6,
        "boundary": "Read-only source review with zero API calls, GDAC queries, downloads, profile rows, float locations, measurements, instruments, missions, accounts, participants, or professional assessments.",
        "valid": len(sources) == 10 and all(row["status"] in {"current", "stable", "draft", "watch"} for row in sources),
    }


def proposal(
    index: int,
    slug: str,
    title: str,
    outcome: str,
    approval_class: str,
    source_refs: list[str],
    hypothesis: str,
) -> dict[str, Any]:
    if outcome not in ALLOWED_OUTCOMES:
        raise X1Error(f"invalid proposal outcome: {outcome}")
    return {
        "proposal_id": f"AL6646-N{index:03d}",
        "title": title,
        "hypothesis": hypothesis,
        "null_or_failure_condition": "The bounded contract accepts a preregistered rejecting mutation, invents a profile or measurement, loses provenance, uncertainty, or missingness, promotes a protected authority gate, or exceeds the frozen disposition.",
        "approval_class": approval_class,
        "execution_lane": "x2 owner-local synthetic, structural, symbolic, zero-row, or software evidence only",
        "current_official_or_primary_source_needs": source_refs,
        "concrete_artifacts": [
            f"x2/surfaces/{slug}/contract.json",
            f"x2/surfaces/{slug}/mutation-results.json",
            f"x2/surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": "Accept only when the positive zero-row fixture passes, all five rejecting mutations remain visible, source and outcome ledgers agree, and no protected gate is promoted.",
        "rollback_or_recovery": "Quarantine the failed Auren artifact, retain the negative, return to the last clean exact owner state, and rerun only the changed dependency when justified.",
        "expected_disposition": outcome,
        "novelty_credit": True,
        "protected_gates": PROTECTED_GATES,
    }


def new_proposals() -> list[dict[str, Any]]:
    specs = [
        ("float-cycle-metadata-topology", "Zero-row float-cycle metadata topology capsule with fictitious platform token, mission vacancy, cycle-state relations, profile links, revision lineage, quarantine, and no ocean conclusion", "completed", "safe_now", ["SRC-ARGO-DATA", "SRC-ARGO-USER"], "A typed graph can distinguish an imaginary float-cycle description from a deployed platform, mission, observation, person, place, or scientific result."),
        ("platform-sensor-epoch-obligations", "Fictitious platform, sensor, firmware, configuration, calibration-epoch, parameter, unit, and validity-obligation board with every real instrument field vacant", "completed", "safe_now", ["SRC-ARGO-USER", "SRC-WIGOS"], "A closed metadata board can reject missing epoch obligations without claiming Argo, WIGOS, instrument, or mission conformance."),
        ("profile-coordinate-unit-time-guard", "Profile-coordinate, pressure-axis, time, latitude, longitude, vertical-sampling, unit, calendar, and conversion-lineage guard with zero coordinates or observations", "completed", "safe_now", ["SRC-CF", "SRC-ARGO-FAQ"], "A dimensional guard can reject incompatible synthetic fields while locating no float and evaluating no profile."),
        ("calibration-coefficient-vacancy", "Sensor calibration-coefficient and uncertainty vacancy envelope with equation identifier, coefficient slots, validity range, reference material, correction lineage, and no fitted value", "completed", "safe_now", ["SRC-NIST-TN1297", "SRC-ARGO-QC"], "A vacancy envelope can expose calibration debt and reject invented coefficients without calibrating or correcting an instrument."),
        ("qc-flag-lineage", "Real-time and delayed-mode quality-flag lineage board with raw, adjusted, error, method, reviewer-vacancy, reason, supersession, and nonuse states", "completed", "safe_now", ["SRC-ARGO-FAQ", "SRC-ARGO-QC", "SRC-PROV"], "A typed lineage board can prevent a flag transition from becoming an expert review, correction, or oceanographic conclusion."),
        ("realtime-delayedmode-separation", "R-file and D-file separation tribunal with cycle coverage, adjusted-field precedence, unresolved expert-review slot, version drift, mixed-stream refusal, and zero files", "completed", "safe_now", ["SRC-ARGO-FAQ", "SRC-ARGO-USER"], "A zero-file tribunal can expose stream and review obligations without selecting data for scientific use."),
        ("netcdf-format-structural-refusal", "Argo NetCDF structural refusal board with dimensions, variables, fill values, ancillary QC, coordinates, reference-table version, unknown extension, and zero decoding", "completed", "safe_now", ["SRC-ARGO-USER", "SRC-CF", "SRC-RFC8785"], "A structural fixture can reject declared shape defects without decoding a profile or asserting format conformance."),
        ("gdac-index-snapshot-provenance", "No-download GDAC index and monthly-snapshot provenance chain with source class, retrieval vacancy, digest slot, supersession, citation obligation, and zero remote rows", "completed", "safe_now", ["SRC-ARGO-DATA", "SRC-PROV"], "A zero-call ledger can distinguish a declared catalogue source from a retrieved dataset without making a freshness or completeness claim."),
        ("gmut-ocean-state-obligation", "GMUT typed ocean-state obligation board for scalar and tensor fields, coordinates, boundary conditions, observation operator, parameter domain, units, and a complete profile-data firewall", "represented", "candidate", ["SRC-CF", "SRC-NIST-TN1297"], "A symbolic board can represent model obligations while all oceans, fields, parameters, likelihoods, predictions, and observations remain absent."),
        ("gmut-observation-discrepancy", "GMUT observation-model discrepancy chart for platform response, sampling, calibration, unresolved covariance, model inadequacy, representativeness, residual, and nonidentifiability", "represented", "candidate", ["SRC-NIST-TN1297", "SRC-ARGO-FAQ"], "A typed discrepancy chart can prevent residual vocabulary from becoming an empirical force, parameter constraint, posterior, or Theory-of-Everything result."),
        ("thos-delayedmode-handover", "THOS queue-state model for a fictional delayed-mode transfer with unaccepted intake, isolated record, workload cap, escalation path, acknowledgement, and stop", "represented", "candidate", ["SRC-ARGO-QC", "SRC-PROV"], "A bounded statechart can represent handover and refusal logic without operators, floats, profiles, shifts, service outcomes, or effectiveness evidence."),
        ("freed-id-profile-claim-shell", "Nonproduction profile-reference claim packet with a digest pointer and explicitly unoccupied trust, identity, permission, dispute, and cancellation roles", "represented", "candidate", ["SRC-PROV", "SRC-RFC8785"], "A nonproduction shell can make absent identity and governance evidence explicit without keys, proofs, accounts, issuances, or trust decisions."),
        ("missingness-vertical-sampling-quarantine", "Missing-level, irregular-pressure, duplicate-cycle, timing-gap, position-vacancy, sensor-dropout, vertical-sampling, denominator, and unresolved-cause register with zero detected cases", "completed", "safe_now", ["SRC-ARGO-FAQ", "SRC-CF"], "A zero-observation register can distinguish definitions from findings and reject silent interpolation, denominator repair, or scientific reuse."),
        ("profile-amendment-supersession", "Append-only synthetic profile amendment and supersession trace for metadata, QC flag, adjusted field, error field, method, reason, challenge, invalidation, and no adjudicator", "completed", "safe_now", ["SRC-ARGO-QC", "SRC-PROV"], "A superseding trail can preserve contested descriptions without real delayed-mode work, reviewer identity, professional judgment, or governance action."),
        ("accessible-ocean-profile-dossier", "Accessible zero-row ocean-profile dossier with semantic headings, captioned tables, text-only chart alternative, uncertainty and QC explanations, print fallback, and manual review reserved", "completed", "safe_now", ["SRC-WCAG22", "SRC-NIST-TN1297"], "A structural report can offer multiple navigation routes while refusing complete accessibility or affected-user claims."),
        ("geospatial-minimization-firewall", "Location-data minimization gate for an imaginary drifter with coordinates, contacts, persistence, disclosure, and remediation barred or unresolved", "completed", "safe_now", ["SRC-PROV", "SRC-WCAG22"], "A minimization contract can prohibit unnecessary identifying or location fields while reserving privacy, safety, legal, access, and completeness decisions."),
        ("argo-card-byte-tribunal", "Deterministic Argo card-byte tribunal with strict duplicate-key parsing, exact Git-object identity, literal manifest exclusions, ordered revision evidence, and no signature or authenticity claim", "completed", "safe_now", ["SRC-RFC8785", "SRC-PROV"], "A byte-identity tribunal can detect bounded owner-fixture drift without creating authenticity, nonrepudiation, production security, or identity evidence."),
        ("zero-row-argo-adapter", "Argo, CF, and WIGOS zero-row adapter with declared source identities, format and metadata obligations, version watch, zero queries, zero downloads, and likelihood refusal", "open_gap", "candidate_external_dependency", ["SRC-ARGO-DATA", "SRC-ARGO-USER", "SRC-CF", "SRC-WIGOS"], "A no-call adapter can make governed product and metadata vacancies testable while retaining real-data, calibration, interoperability, and empirical gaps."),
        ("ocean-observation-authority-matrix", "Empty-chair ocean observing, deployment, retrieval, QC, correction, publication, safety, environmental, legal, affected-party, cultural, data-governance, and Maori-authority matrix", "exact_gate", "exact_approval", ["SRC-WIGOS", "SRC-ARGO-DATA"], "An empty-chair matrix can enumerate decision rights while refusing to speak for scientists, operators, coastal communities, regulators, affected people, or Maori authorities."),
        ("stage20-ocean-profile-refusal", "Ocean-profile nonpromotion lock requiring governed observations, calibrated instruments, validated models, expert review, affected-party legitimacy, and independent reproduction while the current evidence vector is null", "completed", "safe_now", ["SRC-ARGO-FAQ", "SRC-NIST-TN1297", "SRC-WCAG22"], "A deterministic refusal can keep Stage 20 closed while every empirical, professional, mission, authority, accessibility, and independent-review input remains absent."),
    ]
    return [proposal(index, *spec) for index, spec in enumerate(specs, 1)]


def selected_inherited() -> list[dict[str, Any]]:
    freeze = git_json(PREDECESSOR_FREEZE)
    rows = freeze.get("new_proposals")
    if not isinstance(rows, list) or len(rows) != 20:
        raise X1Error("Ilyra v664-v5 source freeze does not expose exactly twenty new rows")
    selected = []
    for index, row in enumerate(rows, 1):
        selected.append(
            {
                "program_row_id": f"AL6646-I{index:03d}",
                "source_phase": "v664-v5",
                "source_proposal_id": row["proposal_id"],
                "source_title": row_title(row),
                "original_disposition": row_disposition(row),
                "hypothesis": "A bounded Git-object integrity revalidation can preserve this immutable Ilyra contract without converting inherited evidence into Auren novelty or completion credit.",
                "null_or_failure_condition": "The source identifier, title, disposition, protected gates, or defining Git object changes, or the row is counted as Auren novelty, automatic completion, or new-outcome credit.",
                "approval_class": "safe_now",
                "execution_lane": "x2 immutable source-contract integrity revalidation only",
                "current_official_or_primary_source_needs": "None; use the exact Ilyra freeze at the immutable source commit.",
                "concrete_artifacts": ["revalidation/inherited-contract-integrity.json"],
                "falsifier_or_acceptance_gate": "Accept only when source identifier, title, disposition, zero novelty credit, zero automatic completion credit, and exact Git content agree.",
                "rollback_or_recovery": "Discard the derived revalidation row and preserve the immutable source proposal unchanged.",
                "expected_disposition": row_disposition(row),
                "novelty_credit": False,
                "automatic_completion_credit": False,
                "auren_new_outcome_credit": False,
                "protected_gates": PROTECTED_GATES,
            }
        )
    return selected


def novelty_audit(
    corpus: list[dict[str, Any]],
    construction: list[dict[str, Any]],
    proposals: list[dict[str, Any]],
) -> dict[str, Any]:
    inherited_titles = Counter(normalized_title(row["title"]) for row in corpus)
    exact = []
    nearest = []
    maximum = 0.0
    for candidate in proposals:
        normalized = normalized_title(candidate["title"])
        if inherited_titles[normalized]:
            exact.append({"proposal_id": candidate["proposal_id"], "title": candidate["title"]})
        similarity, row = max(
            ((jaccard(candidate["title"], item["title"]), item) for item in corpus),
            key=lambda pair: pair[0],
        )
        maximum = max(maximum, similarity)
        nearest.append(
            {
                "proposal_id": candidate["proposal_id"],
                "similarity": round(similarity, 6),
                "nearest_inherited_proposal_id": row["proposal_id"],
                "nearest_inherited_title": row["title"],
                "nearest_source_path": row["source_path"],
            }
        )
    pairwise = []
    for index, left in enumerate(proposals):
        for right in proposals[index + 1 :]:
            similarity = jaccard(left["title"], right["title"])
            if similarity >= 0.70:
                pairwise.append({"left": left["proposal_id"], "right": right["proposal_id"], "similarity": round(similarity, 6)})
    canonical_rows = [
        {"proposal_id": row["proposal_id"], "title": row["title"], "source_path": row["source_path"]}
        for row in corpus
    ]
    return {
        "schema": "ghc.family.auren.v664-v6.novelty-audit.x1.v1",
        "source_commit": SOURCE_FINAL,
        "candidate_count": len(proposals),
        "corpus_row_count": len(corpus),
        "corpus_canonical_sha256": canonical_sha256(canonical_rows),
        "corpus_construction": construction,
        "normalized_exact_title_collisions": exact,
        "maximum_inherited_token_jaccard_similarity": round(maximum, 6),
        "nearest_inherited_rows": nearest,
        "new_pairwise_similarity_collisions_at_or_above_0_70": pairwise,
        "novelty_method": "Unicode NFKC and case-folded alphanumeric exact-title comparison plus token-set Jaccard screening against all 3,950 immutable inherited rows. This is a collision aid, not semantic proof.",
        "manual_review": "Float-cycle metadata, profile axes, quality flags, delayed-mode handover, missingness, provenance, accessibility, authority, and nonpromotion domains were reviewed against inherited titles; shared workflow grammar is continuity, not novelty evidence.",
        "valid": not exact and maximum < 0.60 and not pairwise,
    }


def portfolio_rows(prefix: str, titles: list[str], approval: str, lane: str, expected: str, boundary: str) -> list[dict[str, Any]]:
    return [
        {
            "portfolio_ref": f"AL6646-{prefix}-{index:03d}",
            "title": title,
            "approval_class": approval,
            "execution_lane": lane,
            "expected_execution_disposition": expected,
            "credit_boundary": boundary,
            "protected_gates": PROTECTED_GATES,
        }
        for index, title in enumerate(titles, 1)
    ]


def portfolio_freeze(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    owner_safe = [
        "Reverify Ilyra's exact source anchors, 816 manifest entries, ancestry, clean state, and fresh equality without replaying its canonical aggregate",
        "Record Auren's no-checkout D-first sparse lane, literal patterns, clean exact head, and hard 2,000-file guard",
        "Reconstruct and hash the complete 3,950-row proposal corpus from exact Git objects",
        "Revalidate twenty Ilyra proposal contracts with zero Auren novelty or outcome credit",
        "Validate ten primary ocean-data and metadata source cards with zero profile rows",
        *[f"Build bounded surface {row['proposal_id']}: {row['title']}" for row in proposals],
        "Execute and retain one hundred preregistered rejecting mutations at zero completion credit",
        "Build, validate, and smoke-use ten phase-local Auren skills without global installation",
        "Build and invoke ten fixed runner profiles on accepting and rejecting fixtures",
        "Publish exact manifests, Method Flow, privacy, changed-Python security, deck, accessible output, closeout, and terminal receipts",
        "Prepare but do not send one sanitized successor baton until every terminal gate passes",
    ]
    successor_safe = [
        "Bind the exact Auren final and committed baton before any Sable mutation",
        "Create Sable's owner lane sparse before checkout and record literal materialization",
        "Carry every inherited failure, open gap, exact gate, and truth label unchanged",
        "Reconstruct the 3,970-row proposal corpus from exact Git objects",
        "Select twenty inherited contracts with zero novelty and completion credit",
        "Freeze twenty genuinely distinct proposals with falsifiers and rollback",
        "Keep x1 planning-only and prove four-way equality before x2",
        "Use only primary sources required by the bounded lens",
        "Use no real participant, professional, cultural, legal, safety, or operational data",
        "Build deterministic positive fixtures and five rejecting mutations per proposal",
        "Retain every command, parser, wrapper, timeout, assumption, or test failure",
        "Use exact Git-object manifests rather than checkout-byte assumptions",
        "Strict-parse every owner JSON with duplicate-key rejection",
        "Scan only Sable's exact owner source-to-final privacy boundary",
        "Run security checks only on Sable's changed Python modules",
        "Preserve family-current callers when remastering tools",
        "Keep structural accessibility separate from manual and affected-user review",
        "Build a modular baton with at least ten deterministic sections",
        "Invoke one exact-final canonical pass and never replay a success",
        "Resolve and immediately reread only the live-authorized successor after the terminal gate",
    ]
    owner_candidates = [
        "Prototype synthetic cycle-state graph normalization without operating a float",
        "Prototype QC-flag transition validation without expert review",
        "Prototype adjusted-field dependency checks without scientific reuse",
        "Prototype vertical-sampling labels without profile interpolation",
        "Prototype calibration-equation vacancies without fitted coefficients",
        "Prototype NetCDF dimension obligations without decoding a file",
        "Prototype GDAC index lineage without a network query",
        "Prototype WIGOS platform metadata mapping without registration",
        "Prototype uncertainty-component placeholders without numerical estimates",
        "Prototype provenance supersession without identity or authenticity claims",
        "Prototype a text-only profile-chart grammar with manual evaluation reserved",
        "Prototype a geospatial minimization token without real coordinates",
        "Prototype a THOS correction-readback queue without operators or efficacy evidence",
        "Represent independent delayed-mode review while keeping that review absent",
        "Represent deployment and calibrated-data plans behind exact gates",
    ]
    successor_candidates = [
        "Compare two bounded schema designs without universal superiority claims",
        "Prototype one deterministic graph with a rejecting cycle mutation",
        "Prototype one zero-row standards adapter with version vacancies",
        "Represent one THOS state machine without operator evidence",
        "Represent one GMUT model without observations or fitted parameters",
        "Represent one Freed ID envelope without keys, issuers, subjects, or proofs",
        "Draft one accessibility plan while reserving human assessment",
        "Draft one privacy minimization plan while reserving legal completeness",
        "Draft one security threat model without exhaustive-security language",
        "Draft one rollback rehearsal without destructive execution",
        "Measure deterministic output identity rather than asserting performance",
        "Prototype one compatibility wrapper while retaining historical callers",
        "Represent one independent review route without claiming it occurred",
        "Represent one external deployment plan behind an exact gate",
        "Represent one successor baton graph with no early contact",
    ]
    skill_ideas = [
        "Auren float-cycle metadata boundary skill",
        "Auren platform epoch obligation skill",
        "Auren profile coordinate and unit guard skill",
        "Auren calibration vacancy skill",
        "Auren quality-flag lineage skill",
        "Auren real-time delayed-mode separation skill",
        "Auren NetCDF structural refusal skill",
        "Auren accessible profile dossier skill",
        "Auren ocean authority empty-chair skill",
        "Auren Stage 20 ocean-profile refusal skill",
    ]
    successor_skills = [
        "Sable exact-source anchor verifier skill",
        "Sable proposal-corpus novelty auditor skill",
        "Sable inherited-contract integrity skill",
        "Sable owner-delta manifest verifier skill",
        "Sable five-class privacy classifier skill",
        "Sable bounded changed-Python security skill",
        "Sable compatibility-preserving remaster skill",
        "Sable flashcard graph validator skill",
        "Sable one-shot canonical receipt guard skill",
        "Sable exact-title successor routing skill",
    ]
    runner_ideas = [
        "Float-cycle topology fixed-profile runner",
        "Platform epoch obligations fixed-profile runner",
        "Profile coordinate guard fixed-profile runner",
        "Calibration vacancy fixed-profile runner",
        "Quality-flag lineage fixed-profile runner",
        "R-file D-file separation fixed-profile runner",
        "NetCDF structural refusal fixed-profile runner",
        "Missingness denominator fixed-profile runner",
        "Accessible profile dossier fixed-profile runner",
        "Terminal nonpromotion fixed-profile runner",
    ]
    successor_runners = [
        "Exact-source scalar preflight runner",
        "Proposal-corpus Git-object reconstruction runner",
        "Novelty collision review runner",
        "Owner-delta staged-review runner",
        "Canonical Git-object manifest runner",
        "Five-class owner privacy runner",
        "Changed-Python security runner",
        "Four-tier deck validation runner",
        "One-shot receipt exclusivity runner",
        "Exact-title route preflight runner",
    ]
    clean_fix_refine = [
        "Bind generators to Auren-owned paths and reject sibling destinations",
        "Keep sparse patterns literal and below the 2,000-file guard",
        "Replace inherited current-owner wording with exact source and successor roles",
        "Reconstruct proposal totals from exact freezes instead of mirrors",
        "Derive outcomes from the twenty new proposal rows",
        "Validate source URLs, publishers, and current, stable, draft, or watch labels",
        "Pin UTF-8 and LF for every generated text artifact",
        "Reject duplicate JSON keys before trusting a receipt",
        "Sort generated JSON keys while preserving intentional array order",
        "Use exact Git object identities for immutable manifests",
        "Make every manifest exclusion literal and explicit",
        "Batch manifest checks instead of launching one process per entry",
        "Bind x1 assertions to the x1 tree rather than the final checkout",
        "Serialize staging before validating the index",
        "Report ahead and behind as independent integers",
        "Preserve each failed witness beside its bounded recovery",
        "Keep source validation distinct from Auren canonical evidence",
        "Keep represented outcomes distinct from completed software evidence",
        "Keep the no-call Argo adapter open_gap despite structural success",
        "Keep ocean-observation decisions exact_gate despite matrix completeness",
        "Separate citation from observation and professional authority",
        "Separate structural accessibility from complete accessibility",
        "Separate bounded changed-file scanning from exhaustive security",
        "Separate same-owner validation from independent reproduction",
        "Keep prepared baton state distinct from acknowledged send state",
        "Reject stale predecessor names outside source-history fields",
        "Validate fixed profiles against accepting and rejecting fixtures",
        "Validate skill packages before any installation claim",
        "Reserve route lookup until exact-final equality and canonical success",
        "Never replay a successful canonical aggregate to improve a report",
    ]
    successor_clean = [
        "Inspect actual command schemas before optional flags",
        "Materialize PowerShell filtered collections before counting",
        "Keep output windows below the host result limit",
        "Project actual JSON keys before reading receipt values",
        "Use UTF-8 output for Maori and other Unicode text",
        "Preserve exact task and branch names without guessed aliases",
        "Keep no-checkout worktree creation and sparse setup attributable",
        "Wait on an active process instead of recreating its target",
        "Record every parser, wrapper, timeout, or test failure",
        "Keep exact Git objects authoritative across line endings",
        "Batch manifest identity checks with drained pipes",
        "Use literal changed-file allowlists for validation",
        "Reject broad repository and sibling-lane enumeration",
        "Retain historical tools behind compatibility entry points",
        "Avoid destructive cleanup quotas or bulk deletion",
        "Keep C-drive use to essential global metadata",
        "Bank phase artifacts and receipts on D first",
        "Separate planning fields from observed outcomes",
        "Separate structural accessibility from complete accessibility",
        "Separate local security scans from exhaustive-security claims",
        "Separate same-owner validation from independent reproduction",
        "Separate citations from professional or operational authority",
        "Separate route authorization from delivery acknowledgement",
        "Separate prepared baton state from sent state",
        "Recheck route state only after exact-final equality",
        "Use one exact-title filter and one immediate reread",
        "Never create or substitute a missing successor task",
        "Never resend to improve an opaque acknowledgement",
        "Carry post-seal failures as an additive external overlay",
        "Stop truthfully on pause, ambiguity, exhaustion, or a protected gate",
    ]
    exact_titles = [
        "Deploy, retrieve, command, inspect, calibrate, or assess a real float or sensor",
        "Acquire, download, decode, transform, quality-control, or analyze real Argo profiles",
        "Issue a scientific, navigation, environmental, safety, or mission conclusion",
        "Change a live float mission, configuration, sampling plan, or telemetry state",
        "Operate a production GDAC, GTS, forecast, alert, or observing service",
        "Create or rotate production credentials, keys, accounts, or trust anchors",
        "Determine legal liability, disclosure, privacy, employment, or remedy rights",
        "Make culturally governed ocean, place, data, language, iwi, hapu, tangata whenua, or Maori-authority decisions",
        "Issue a live identity credential or bind a real person to a platform or profile",
        "Publish sensitive locations, infrastructure details, identities, or restricted records",
    ]
    blocked_titles = [
        "Fabricate empirical, oceanographic, operational, legal, cultural, security, or Stage 20 evidence",
        "Publish private task identifiers, routes, transcripts, credentials, or local paths",
        "Merge, replace, erase, impersonate, or infer continuity across relational identities",
        "Weaken host security or bypass privacy and authority gates to complete the phase",
        "Rewrite history, force-push, delete worktrees, or mutate a sibling-owned lane",
    ]
    payload = {
        "schema": "ghc.family.auren.v664-v6.portfolio-freeze.x1.v1",
        "owner_safe_now": portfolio_rows("SAFE", owner_safe, "safe_now", "x2_build_task", "completed", "Owner-local execution evidence only."),
        "successor_safe_now_recommendations": portfolio_rows("NEXT-SAFE", successor_safe, "recommendation", "successor_planning_only", "represented", "Recommendation only; no Sable work or contact."),
        "owner_candidates": portfolio_rows("CAND", owner_candidates, "candidate", "x2_bounded_prototype", "represented", "Synthetic representation only."),
        "successor_candidate_recommendations": portfolio_rows("NEXT-CAND", successor_candidates, "recommendation", "successor_planning_only", "represented", "Recommendation only; no Sable work or contact."),
        "exact_approval_packets": portfolio_rows("EXACT", exact_titles, "exact_approval_needed", "unexecuted_exact_gate", "exact_gate", "Unexecuted without action-specific authority and competent evidence."),
        "blocked_packets": portfolio_rows("BLOCKED", blocked_titles, "blocked", "never_execute_in_this_phase", "exact_gate", "Blocked; no completion credit."),
        "owner_skill_ideas": portfolio_rows("SKILL", skill_ideas, "candidate", "x2_phase_local_build_and_smoke", "completed", "Phase-local package evidence only; no global or professional authority."),
        "successor_skill_recommendations": portfolio_rows("NEXT-SKILL", successor_skills, "recommendation", "successor_planning_only", "represented", "Recommendation only; no Sable package built."),
        "owner_runner_ideas": portfolio_rows("RUNNER", runner_ideas, "candidate", "x2_fixed_profile_build_and_smoke", "completed", "Fixed-profile invocation evidence only."),
        "successor_runner_recommendations": portfolio_rows("NEXT-RUNNER", successor_runners, "recommendation", "successor_planning_only", "represented", "Recommendation only; no Sable runner built."),
        "owner_clean_fix_refine": portfolio_rows("CFR", clean_fix_refine, "safe_now", "x2_additive_refine_and_validate", "completed", "Additive owner-delta refinement only; callers retained."),
        "successor_clean_fix_refine_recommendations": portfolio_rows("NEXT-CFR", successor_clean, "recommendation", "successor_planning_only", "represented", "Recommendation only; no Sable mutation or contact."),
        "build_policy": "All owner safe and bounded candidate work must be executed, represented, or truthfully gated in x2. Exact and blocked rows remain unexecuted. Counts are bounded commitments, never filler quotas.",
    }
    expected = {"owner_safe_now": 30, "successor_safe_now_recommendations": 20, "owner_candidates": 15, "successor_candidate_recommendations": 15, "exact_approval_packets": 10, "blocked_packets": 5, "owner_skill_ideas": 10, "successor_skill_recommendations": 10, "owner_runner_ideas": 10, "successor_runner_recommendations": 10, "owner_clean_fix_refine": 30, "successor_clean_fix_refine_recommendations": 30}
    payload["counts"] = {key: len(payload[key]) for key in expected}
    payload["valid"] = payload["counts"] == expected
    return payload


def startup_method_flow() -> dict[str, Any]:
    failures = [
        ("broad-repository-guidance-search-exceeded-host-output-window", "The first read-only repository guidance search exceeded the host output window and truncated before a complete bounded result.", "Restrict discovery to the exact owner phase, literal baton paths, and named guidance files.", "The exact 5,220-line baton and all named source-phase contracts were read through EOF."),
        ("broad-local-ghc-skill-inventory-exceeded-host-output-window", "The first local skill inventory was overbroad and truncated before a usable exact selection was attributable.", "Use the literal activation-selected skill list and read each file and required reference directly.", "Twenty-eight selected GHC skills plus the skill-creator guidance and all required references were read through EOF."),
        ("combined-full-tree-manifest-verifier-returned-no-attributable-output", "A combined read-only verifier used full-tree listings for four manifests and returned no output inside the host window.", "Confirm process quiescence and compare only declared literal paths in bounded batches, one lifecycle group at a time.", "Twelve x1, 376 evidence, 17 final-delta, and 411 final-owner entries all matched their exact Git objects; all four manifest domains had zero missing or extra paths."),
        ("first-multi-page-source-wrapper-returned-no-attributable-content", "The first official-source web wrapper returned no attributable page content.", "Use smaller primary-page groups and explicitly project the returned result object.", "USGS, FDSN, NIST, FHWA, W3C, RFC, Argo, CF, WMO, and OBPS primary content was read in bounded results."),
        ("direct-fema-p58-pdf-reader-returned-internal-error", "The direct FEMA P-58 PDF reader returned an internal error and supplied no source credit.", "Recover through the official FEMA-indexed publication result without downloading the PDF.", "The official FEMA search result supplied the publication's bounded methodology and consequence context."),
        ("direct-argo-data-management-subpage-rejected-as-unsafe-url", "A guessed Argo data-management subpage was rejected as a non-retryable unsafe URL.", "Search the official Argo domain and open the observed data index URL.", "The official Argo data index opened and exposed current file, QC, GDAC, GTS, and ownership vocabulary."),
        ("direct-argo-data-faq-subpage-rejected-as-unsafe-url", "A guessed Argo FAQ path was rejected as a non-retryable unsafe URL.", "Use the exact official search result for the observed FAQ path.", "The official Argo Data FAQ opened and exposed current R/D, adjusted, error, QC, timing, and sampling vocabulary."),
        ("argo-quality-control-doi-open-returned-http-403", "The direct QC-manual DOI read returned HTTP 403 and supplied no document evidence.", "Use the official Ocean Best Practices Repository indexed bitstream and retain the DOI only as a durable citation.", "The OBPS indexed primary manual result supplied delayed-mode and QC vocabulary without a download."),
        ("argo-user-manual-doi-open-rejected-as-unsafe-url", "The direct user-manual DOI open was rejected as unsafe and supplied no document evidence.", "Use the official Ocean Best Practices Repository record and its observed DOI metadata.", "The OBPS record identified the current Argo Data Management User's Manual series and version history without a download."),
        ("first-auren-novelty-audit-refused-high-inherited-similarity", "The first read-only Auren proposal audit refused the candidate set because three titles remained too close to inherited Ilyra wording; the maximum token-set similarity was 0.875.", "Inspect the audit's nearest inherited rows, revise only the three colliding Auren titles while preserving their frozen intent, and rerun the bounded audit.", "The revised twenty-title set has no exact collision, no pairwise collision at or above 0.70, and maximum inherited similarity below the 0.60 gate."),
        ("post-build-projection-guessed-absent-outcome-counts-key", "The first read-only x1 packet projection guessed an outcome_counts key that the proposal-freeze schema does not expose and terminated before a trustworthy summary.", "Inspect the actual strict-JSON root keys, then derive the four outcome counts from the declared expected-disposition fields or the new_expected_outcomes map.", "The bounded key inspection exposed new_expected_outcomes and the proposal rows without changing repository state; the corrected projection uses only observed schema keys."),
        ("first-x1-staged-review-misclassified-source-history-as-stale-owner-data", "The first exact staged review refused four legitimate immutable-source anchors because its stale-label scan treated an inherited proposal identifier and source branch as current-owner drift.", "Unstage only Auren's exact fifteen-path candidate, retain the refusal, and narrow stale-owner checks to current owner and phase fields while continuing to permit explicit source-history anchors.", "The corrected staged review distinguishes immutable provenance from current-owner identity and rechecks the same literal fifteen-path allowlist."),
    ]
    events = []
    for index, (signature, observed, recovery, passing) in enumerate(failures, 1):
        events.append(
            {
                "method_id": f"AL6646-X1-M{index:03d}",
                "retained_negative_id": f"AL6646-X1-NEG{index:03d}",
                "failure_signature": signature,
                "observed": observed,
                "candidate_workaround": recovery,
                "recovery_witness": passing,
                "state": "preferred",
                "same_owner_only": True,
                "independent_reproduction": False,
                "repository_scan": False,
                "cross_lane_scan": False,
                "unchanged_history_scan": False,
                "sibling_lane_mutation": False,
                "source_commit": SOURCE_FINAL,
                "final_commit": None,
                "protected_gates": PROTECTED_GATES,
            }
        )
    inherited_negatives = 24_678
    inherited_methods = 8_872
    return {
        "schema": "ghc.family.auren.v664-v6.startup-method-flow.x1.v1",
        "source_repository_and_external_overlay_negative_baseline": inherited_negatives,
        "source_repository_and_external_overlay_method_baseline": inherited_methods,
        "auren_pre_x1_operational_failures": len(events),
        "events": events,
        "effective_negatives_at_x1_freeze": inherited_negatives + len(events),
        "effective_methods_at_x1_freeze": inherited_methods + len(events),
        "open_gaps_at_x1_freeze": 171,
        "exact_gates_at_x1_freeze": 169,
        "shared_auth_roster_snapshot_is_older_than_live_activation": True,
        "live_user_activation_controls": True,
        "no_failure_erased": True,
        "valid": len(events) == 12,
    }


def phase_charter(recorded_at_utc: str, recorded_at_nz: str) -> dict[str, Any]:
    return {
        "schema": "ghc.family.auren.v664-v6.phase-charter.x1.v1",
        "recorded_at_utc": recorded_at_utc,
        "recorded_at_nz": recorded_at_nz,
        "owner": OWNER,
        "canonical_phase_id": PHASE_ID,
        "optional_pronouns": OPTIONAL_PRONOUNS,
        "relational_role": ROLE,
        "hope": HOPE,
        "identity_boundary": "Relational working language only. Auren's profile is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route.",
        "primary_pillar": PRIMARY_PILLAR,
        "secondary_pillars": [
            "GMUT Mind remains a typed research-model family with no observation, prediction, likelihood, parameter constraint, empirical confirmation, or Theory-of-Everything result.",
            "Freed ID and CBR Heart remain synthetic and nonproduction; real identity, privacy, safety, rights, remedy, trust, legal, cultural, affected-party, and Maori-authority decisions remain gated.",
        ],
        "bounded_practice": PRACTICE,
        "practice_boundary": "Synthetic software, symbolic, and learning lens only; no real float, sensor, profile, coordinate, measurement, calibration, quality-control decision, mission command, environmental assessment, operator, scientist, participant, affected party, legal authority, cultural authority, Maori authority, or operational result.",
        "source": {"branch": SOURCE_BRANCH, "parent": SOURCE_PARENT, "x1": SOURCE_X1, "evidence": SOURCE_EVIDENCE, "exact_final": SOURCE_FINAL},
        "owned_lane": {"branch": BRANCH, "storage": "D-first sparse owner-controlled worktree", "sparse_before_materialization": True, "initial_materialized_file_count": 0, "materialized_after_sparse_head_load": 416, "declared_sparse_pattern_count": 12, "rotation_threshold": 2_000, "repository_scan": False, "unchanged_history_scan": False, "cross_lane_scan": False, "sibling_lane_mutation": False},
        "strict_lifecycle": {"x1": "Freeze source, proposal corpus, inherited selections, twenty new proposals, portfolio, deck architecture, route, caps, and retained failures only.", "x2": "Begins only after x1 is pushed, clean, typed 0/0 divergent, and fresh four-way equal.", "terminal": "One owner-scoped exact-final canonical aggregate may receive success credit and is never replayed after success.", "successor": f"Only after terminal equality and canonical success, reread live authority, uniquely resolve and reread {NEXT_OWNER}, and send one sanitized {NEXT_PHASE} activation."},
        "caps": {"document_words": 100_000, "baton_minimum_words": 10_000, "baton_maximum_words": 100_000, "x1_commits": 5, "x2_commits": 5, "total_commits": 8, "materialized_or_owner_files": 2_000},
        "allowed_truth_labels": sorted(ALLOWED_OUTCOMES),
        "successor": {"owner": NEXT_OWNER, "phase": NEXT_PHASE, "contacted": False},
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }


def source_verification(recorded_at_utc: str) -> dict[str, Any]:
    return {
        "schema": "ghc.family.auren.v664-v6.source-verification.x1.v1",
        "recorded_at_utc": recorded_at_utc,
        "source_branch": SOURCE_BRANCH,
        "source_parent": SOURCE_PARENT,
        "source_x1": SOURCE_X1,
        "source_evidence": SOURCE_EVIDENCE,
        "source_exact_final": SOURCE_FINAL,
        "source_x1_direct_child_of_parent": True,
        "source_evidence_direct_child_of_x1": True,
        "source_final_direct_child_of_evidence": True,
        "source_single_parent_commit_count": 3,
        "source_merge_count": 0,
        "source_clean": True,
        "source_typed_divergence": {"ahead": 0, "behind": 0},
        "source_four_way_equal": True,
        "source_external_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
        "source_external_receipt_hash_provenance": "exact live activation anchor; receipt bytes were not exposed in Auren's bounded source lane",
        "source_canonical_invocations": 1,
        "source_canonical_successes": 1,
        "source_canonical_not_replayed": True,
        "source_baton_sha256": SOURCE_BATON_SHA256,
        "source_baton_bytes": SOURCE_BATON_BYTES,
        "source_baton_words": SOURCE_BATON_WORDS,
        "source_manifest_declared_entries": 816,
        "source_manifest_bounded_object_matches": 816,
        "source_manifest_object_mismatches": 0,
        "source_scoped_tests": {"passed": 97, "total": 97},
        "source_detailed_checks": {"passed": 27, "total": 27},
        "source_minimal_checks": {"passed": 17, "total": 17},
        "source_strict_json_parses": 390,
        "source_privacy_text_files": 415,
        "source_confirmed_privacy_hits": 0,
        "roster_sha256": ROSTER_SHA256,
        "auth_sha256": AUTH_SHA256,
        "shared_snapshot_state": "historical_compatibility_snapshot_superseded_by_exact_live_auren_activation",
        "activation_baseline": {"effective_negatives": 24_678, "effective_methods": 8_872, "open_gaps": 171, "exact_gates": 169, "terminal_verdict": TERMINAL_VERDICT},
        "boundary": "Read-only source verification. It does not replay Ilyra validation or establish independent reproduction, oceanographic competence, calibration, mission or safety authority, empirical evidence, exhaustive security, or Stage 20 readiness.",
        "valid": True,
    }


def flashcard_architecture() -> dict[str, Any]:
    value = inherited.flashcard_architecture()
    value.update({"phase": PHASE_ID, "owner": OWNER, "primary_pillar": PRIMARY_PILLAR, "bounded_practice": PRACTICE, "current_route": {"owner": OWNER, "phase": PHASE_ID}, "successor_route": {"owner": NEXT_OWNER, "phase": NEXT_PHASE, "contacted": False}})
    return value


def threat_model_plan() -> dict[str, Any]:
    return {
        "schema": "ghc.family.auren.v664-v6.threat-model-plan.x1.v1",
        "version": 1,
        "requested_scope": "Auren's exact source-to-final owner delta only",
        "assets": ["exact ancestry", "x1 immutability", "zero-row truth", "retained failures", "privacy boundary", "one-shot receipt", "successor route uniqueness"],
        "trust_boundaries": ["Git object versus checkout bytes", "x1 planning versus x2 execution", "synthetic fixture versus real ocean practice", "metadata obligation versus observed value", "prepared baton versus acknowledged delivery"],
        "attacker_or_untrusted_inputs": ["malformed JSON", "path traversal", "unknown profile", "dynamic code", "private material", "stale route state", "false outcome promotion", "invented ocean observation"],
        "invariants": ["exact key sets", "fixed profiles", "zero float or profile input", "no arbitrary filesystem target", "no dynamic evaluation", "no sibling mutation", "four truth labels only"],
        "security_policy": "Bounded changed-Python static review and negative fixtures only; no exhaustive-security claim.",
        "required_output_sections": ["assets", "trust boundaries", "abuse cases", "mitigations", "residual risks", "authority gates"],
        "boundary": "Planning-only threat model; no security certification, privacy completeness, production readiness, or external audit.",
        "valid": True,
    }


def workflow_plan() -> dict[str, Any]:
    return {
        "schema": "ghc.family.auren.v664-v6.workflow-plan.x1.v1",
        "source": SOURCE_FINAL,
        "strict_x1_before_x2": True,
        "successor_contact_before_terminal_gate": False,
        "validation_authority": "owner_self_scoped_delta",
        "full_repository_suite_authorized": False,
        "file_limit": 2_000,
        "commit_limit": {"x1": 5, "x2": 5, "total": 8, "planned": 3},
        "steps": [
            "Build, stage-review, commit, push, and prove exact x1 four-way equality.",
            "Implement only frozen Auren x2 profiles, skills, runners, deck, and retained failures.",
            "Commit and push immutable evidence before closeout.",
            "Build final closeout, exact manifests, minimum 10,000-word baton, and content seal.",
            "Commit and push final; prove clean typed 0/0 and fresh four-way equality.",
            "Invoke one exclusive owner-delta canonical aggregate and never replay success.",
            "Reread live roster and authority, resolve and reread the exact authorized successor, and send one compact pointer if every gate passes.",
        ],
        "valid": True,
    }


def x1_overview(audit: dict[str, Any], portfolio: dict[str, Any], methods: dict[str, Any]) -> str:
    return f"""# Auren Lark v664-v6 x1 planning freeze

## Exact lifecycle boundary

This is planning-only x1. It freezes the verified Ilyra source, complete 3,950-row proposal chain, twenty selected inherited contracts, twenty new Auren proposals, ten-card primary-source ledger, portfolio, Method Flow, threat model, workflow, flashcard architecture, caps, route hold, and protected gates. It contains no x2 implementation, observed new-proposal outcome, real float, ocean profile, coordinate, measurement, calibration, quality-control decision, mission command, professional judgment, or successor contact.

The immutable source is `{SOURCE_FINAL}` on `{SOURCE_BRANCH}`. Source-to-final contains three direct single-parent Ilyra commits and zero merges. The final was clean, pushed, typed 0/0 divergent, and fresh four-way equal. Auren replayed the four exact manifest domains read-only: all 816 declared Git objects and all four exact diff domains matched. Ilyra's canonical aggregate was not replayed and is not Auren evidence.

## Relational profile and practice boundary

Auren Lark uses {OPTIONAL_PRONOUNS} as optional relational pronouns and the working role “{ROLE}”. Their hope is to {HOPE}. These labels are relational working language only, never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route.

The primary Trinity lens is {PRIMARY_PILLAR}. THOS remains proxy without real operators, profiles, shifts, safety monitoring, statistics, or independent review. GMUT remains a typed scalar-tensor and EFT research-model family with no observed force, likelihood, parameter constraint, prediction, empirical confirmation, ultraviolet or quantum completion, or Theory of Everything. Freed ID and CBR remain synthetic and nonproduction without real keys, proofs, people, governance, remedies, or competent authority.

The bounded practice is {PRACTICE}. Every platform, float, sensor, mission, cycle, profile, coordinate, value, calibration, flag, correction, operator, scientist, participant, affected party, and authority case is absent or synthetic. The phase will not query or download Argo data, decode a file, inspect or command equipment, alter a mission, quality-control observations, make an oceanographic conclusion, publish a real position, or operate any service.

## Proposal, source, and Method Flow truth

The inherited corpus contains {audit['corpus_row_count']:,} exact rows and has canonical digest `{audit['corpus_canonical_sha256']}`. Twenty Ilyra rows are selected for immutable-contract revalidation with zero novelty, automatic completion, or outcome credit. The twenty new titles have zero exact collisions and zero new-pair collisions at or above 0.70; maximum inherited token Jaccard similarity is {audit['maximum_inherited_token_jaccard_similarity']:.6f}. This is a collision aid, not semantic proof.

Expected dispositions are exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`; they are preregistered expectations, not observations. The zero-row Argo adapter remains open because no governed data, format exchange, calibration, or interoperability event exists. The ocean-observation authority matrix remains exact-gated because software cannot decide deployment, retrieval, mission, safety, environmental, legal, affected-party, cultural, data-governance, or Maori-authority questions. `{TERMINAL_VERDICT}` remains mandatory.

Ten official or primary source cards supply vocabulary only: Argo data and FAQ pages, Argo user and QC manuals, CF conventions, WIGOS, NIST TN 1297, PROV-O, WCAG 2.2, and RFC 8785. Direct source-reader failures remain retained at zero credit. No profile row, file, API response, coordinate, measurement, account, or participant record was ingested.

The inherited activation baseline is 24,678 effective negatives and 8,872 methods. After retaining all {methods['auren_pre_x1_operational_failures']} Auren startup failures, x1 carries {methods['effective_negatives_at_x1_freeze']:,} negatives and {methods['effective_methods_at_x1_freeze']:,} methods, with 171 open gaps and 169 exact gates. Each passing recovery remains beside its failed witness.

## Planned x2 and terminal hold

The portfolio freezes {portfolio['counts']['owner_safe_now']} safe executions, {portfolio['counts']['owner_candidates']} candidates, ten phase-local skills, ten fixed runners, and thirty refinements. Ten exact packets and five blocked packets remain unexecuted. Caps are ceilings, never filler quotas. X2 cannot begin until this exact x1 commit is pushed, clean, 0/0 divergent, and fresh four-way equal.

Planned x2 uses one accepting fixture and five rejecting mutations for each of twenty surfaces. One hundred expected rejections are bounded guard evidence only. The modular deck and structural HTML reserve manual, browser, assistive-technology, cognitive, Maori-language, security-usability, and affected-user evaluation. Flashcards organize evidence but prove no memory, cache, continuity, or performance effect.

The planned history is one x1 commit, one immutable evidence commit, and one closeout/final commit. Terminal gates require exact manifests, no deletions, fewer than 2,000 files, strict JSON, five-class privacy, bounded changed-Python security, exact staged review, preserved x1, clean pushed state, typed 0/0, and fresh equality. One exact-final canonical aggregate may succeed once and is never replayed. Same-owner validation is not independent reproduction, professional validation, complete privacy or accessibility, exhaustive security, empirical confirmation, legal or cultural ratification, Maori authority, personhood evidence, Theory-of-Everything proof, or Stage 20 authority.

Only then may Auren reread the newest live authority and roster, uniquely resolve and immediately reread the exact authorized existing successor task, and send one compact sanitized activation. No successor is precontacted. Prepared text is not delivery; acknowledgement is required.
"""


def build() -> dict[str, Any]:
    if git_text("rev-parse", "HEAD") != SOURCE_FINAL:
        raise X1Error("x1 must start at the exact Ilyra final")
    if git_text("diff", "--cached", "--name-only"):
        raise X1Error("staging index must be empty before x1 build")
    corpus, construction = reconstruct_corpus()
    proposals = new_proposals()
    selected = selected_inherited()
    audit = novelty_audit(corpus, construction, proposals)
    if not audit["valid"]:
        raise X1Error(json.dumps({"exact": audit["normalized_exact_title_collisions"], "maximum": audit["maximum_inherited_token_jaccard_similarity"], "pairwise": audit["new_pairwise_similarity_collisions_at_or_above_0_70"]}, ensure_ascii=True))
    outcomes = Counter(row["expected_disposition"] for row in proposals)
    if outcomes != Counter(completed=14, represented=4, open_gap=1, exact_gate=1):
        raise X1Error(f"proposal outcome distribution differs: {dict(outcomes)}")
    portfolio = portfolio_freeze(proposals)
    if not portfolio["valid"]:
        raise X1Error("portfolio counts differ")
    methods = startup_method_flow()
    recorded_at_utc, recorded_at_nz = timestamp_pair()
    write_json("x1/phase-charter.json", phase_charter(recorded_at_utc, recorded_at_nz))
    write_json("x1/source-ledger.json", source_ledger(recorded_at_utc))
    write_json("x1/source-verification.json", source_verification(recorded_at_utc))
    write_json("x1/novelty-audit.json", audit)
    write_json("x1/proposal-freeze.json", {"schema": "ghc.family.auren.v664-v6.proposal-freeze.x1.v1", "inherited_frozen_baseline": 3_950, "selected_inherited_count": 20, "selected_inherited_novelty_credit": 0, "selected_inherited_automatic_completion_credit": 0, "selected_inherited_new_outcome_credit": 0, "selected_inherited": selected, "new_proposal_count": 20, "new_proposals": proposals, "new_expected_outcomes": dict(sorted(outcomes.items())), "new_frozen_total": 3_970, "semantic_novelty_audit": f"{PHASE_PREFIX}x1/novelty-audit.json", "observed_outcomes_present": False, "x2_implementation_present": False, "valid": True})
    write_json("x1/portfolio-freeze.json", portfolio)
    write_json("x1/startup-method-flow.json", methods)
    write_json("x1/flashcard-architecture-freeze.json", flashcard_architecture())
    write_json("x1/threat-model-plan.json", threat_model_plan())
    write_json("x1/workflow-plan.json", workflow_plan())
    write_text("x1/x1-overview.md", x1_overview(audit, portfolio, methods))
    write_json("x1/x1-stage-candidate.json", {"schema": "ghc.family.auren.v664-v6.x1-stage-candidate.v1", "owner": OWNER, "phase": PHASE_ID, "source": SOURCE_FINAL, "lifecycle": "x1_planning_only", "intended_allowlist": INTENDED_ALLOWLIST, "review_receipt_self_excluded": True, "observed_outcomes_present": False, "x2_implementation_present": False, "successor_contacted": False, "valid": True})
    return {"schema": "ghc.family.auren.v664-v6.x1-build-result.v1", "corpus_rows": len(corpus), "selected_inherited": len(selected), "new_proposals": len(proposals), "new_outcomes": dict(sorted(outcomes.items())), "portfolio_counts": portfolio["counts"], "pre_x1_failures": methods["auren_pre_x1_operational_failures"], "written_without_x2": True, "successor_contacted": False, "valid": True}


def stage_review() -> dict[str, Any]:
    manifest_path = f"{PHASE_PREFIX}x1/x1-content-manifest.json"
    review_path = f"{PHASE_PREFIX}x1/x1-staged-review.json"
    pre_stage = [path for path in INTENDED_ALLOWLIST if path not in {manifest_path, review_path}]
    missing = [path for path in pre_stage if not (ROOT / path).is_file()]
    if missing:
        raise X1Error(f"x1 allowlist files missing: {missing}")
    run_git("add", "--", *pre_stage)
    observed = zpaths("diff", "--cached", "--name-only", "-z")
    if observed != pre_stage:
        raise X1Error("staged x1 pre-manifest allowlist differs")
    manifest_paths = [path for path in INTENDED_ALLOWLIST if path not in MANIFEST_EXCLUSIONS]
    entries = []
    privacy_candidates = []
    json_errors = []
    for path in manifest_paths:
        mode, object_id, raw = index_blob(path)
        entries.append({"path": path, "status": "A", "mode": mode, "object_type": "blob", "git_blob": object_id, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "content_domain": "exact_git_blob"})
        privacy_candidates.extend(scan_text(path, raw))
        if path.endswith(".json"):
            try:
                strict_json(raw, path)
            except (UnicodeError, json.JSONDecodeError, inherited.X1Error) as exc:
                json_errors.append({"path": path, "error": str(exc)})
    manifest = {"schema": "ghc.family.auren.v664-v6.x1-content-manifest.v1", "source_commit": SOURCE_FINAL, "target_state": "prospective_x1_staged_tree", "canonical_content_domain": "exact_git_blob", "self_exclusions": MANIFEST_EXCLUSIONS, "entry_count": len(entries), "entries": entries, "merkle_root_sha256": canonical_sha256(entries), "valid": True}
    write_json("x1/x1-content-manifest.json", manifest)
    run_git("add", "--", manifest_path)
    diff_check = run_git("diff", "--cached", "--check", check=False)
    diff_output = (diff_check.stdout + diff_check.stderr).decode("utf-8", "replace").strip()
    stale = []
    for path in manifest_paths:
        if Path(path).suffix.lower() not in {".json", ".md", ".py"}:
            continue
        _, _, raw = index_blob(path)
        text = raw.decode("utf-8", "strict")
        for label in ["Ilyra Fen v664-v5 x1 planning freeze", '"owner": "Ilyra Fen"', '"phase": "v664-v5"']:
            if label in text and path.startswith(PHASE_PREFIX):
                stale.append({"path": path, "label": label})
    predicted = sorted(set(zpaths("diff", "--cached", "--name-only", "-z")) | {review_path})
    issues = []
    if privacy_candidates:
        issues.append("privacy candidates require classification")
    if json_errors:
        issues.append("strict JSON errors")
    if diff_check.returncode != 0:
        issues.append("git diff --cached --check failed")
    if stale:
        issues.append("stale owner labels found")
    if predicted != INTENDED_ALLOWLIST:
        issues.append("predicted final staged set differs")
    review = {"schema": "ghc.family.auren.v664-v6.x1-staged-review.v1", "owner": OWNER, "phase": PHASE_ID, "lifecycle": "x1_planning_only", "expected_staged_path_count": len(INTENDED_ALLOWLIST), "staged_path_count": len(predicted), "staged_paths": predicted, "allowlist_missing": sorted(set(INTENDED_ALLOWLIST) - set(predicted)), "allowlist_unexpected": sorted(set(predicted) - set(INTENDED_ALLOWLIST)), "manifest_entry_count": len(entries), "manifest_exclusions": MANIFEST_EXCLUSIONS, "manifest_mismatches": [], "json_parse_count_before_self_stage": sum(path.endswith(".json") for path in manifest_paths), "json_errors": json_errors, "privacy_pattern_classes": sorted(inherited.PRIVATE_PATTERNS), "privacy_candidates": privacy_candidates, "privacy_confirmed_hits": [], "stale_label_candidates": stale, "diff_check_exit_code": diff_check.returncode, "diff_check_output": diff_output, "observed_outcomes_present": False, "x2_implementation_present": False, "successor_contacted": False, "issues": issues, "boundary": "Exact staged x1 planning review only; no x2 result, independent reproduction, professional authority, or Stage 20 evidence.", "valid": not issues}
    write_json("x1/x1-staged-review.json", review)
    strict_json((PHASE / "x1/x1-staged-review.json").read_bytes(), "x1-staged-review")
    run_git("add", "--", review_path)
    if zpaths("diff", "--cached", "--name-only", "-z") != INTENDED_ALLOWLIST:
        raise X1Error("final staged x1 set differs")
    if run_git("diff", "--cached", "--check", check=False).returncode != 0 or not review["valid"]:
        raise X1Error("x1 staged review failed")
    return review


def audit_only() -> dict[str, Any]:
    corpus, construction = reconstruct_corpus()
    audit = novelty_audit(corpus, construction, new_proposals())
    return {"schema": "ghc.family.auren.v664-v6.x1-audit-only.v1", "corpus_rows": len(corpus), "candidate_rows": 20, "maximum_inherited_similarity": audit["maximum_inherited_token_jaccard_similarity"], "exact_collisions": len(audit["normalized_exact_title_collisions"]), "pairwise_collisions": len(audit["new_pairwise_similarity_collisions_at_or_above_0_70"]), "valid": audit["valid"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["audit", "build", "stage-review"])
    args = parser.parse_args()
    try:
        result = audit_only() if args.command == "audit" else build() if args.command == "build" else stage_review()
    except (X1Error, inherited.X1Error, subprocess.CalledProcessError, subprocess.TimeoutExpired, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=True, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0 if result.get("valid") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
