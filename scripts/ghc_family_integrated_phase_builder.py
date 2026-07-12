#!/usr/bin/env python3
"""Build a portable, evidence-bounded integrated GHC phase bundle."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FUNCTIONS = [
    (1, "question_scope_preregistration"),
    (2, "sources_data_standards_provenance"),
    (3, "formal_model_schema_invariants"),
    (4, "adversarial_critique_and_failure_modes"),
    (5, "reversible_build"),
    (6, "test_benchmark_and_negative_results"),
    (7, "heart_privacy_rights_cultural_authority"),
    (8, "replication_closeout_and_route_truth"),
]

MISSIONS = [
    {
        "origin_version": 641,
        "slug": "corpus-provenance",
        "title": "Corpus truth, provenance, and semantic deduplication",
        "artifact": "docs/eiren-kestrel/v641-v1/corpus/provenance-receipt.json",
        "claim_type": "informational",
        "baseline": "existing privacy-minimizing v36-v54 and v601-v640 indexes",
        "null": "additional indexing adds no unique or reproducible provenance",
        "falsifier": "hash/count rebuild differs for the same pinned inputs or leaks private content",
    },
    {
        "origin_version": 642,
        "slug": "gmut-canonical-equations",
        "title": "GMUT action, notation, dimensions, and null-limit closure",
        "artifact": "latex/grand_mandala.tex",
        "claim_type": "physical",
        "baseline": "general relativity plus Standard Model matter",
        "null": "the extension sector adds no supported observable beyond the baseline",
        "falsifier": "dimension, conservation, stability, null-recovery, or existing-bound gate fails",
    },
    {
        "origin_version": 643,
        "slug": "conservation-stability-numerics",
        "title": "Conservation, stability, and numerical sanity",
        "artifact": "docs/eiren-kestrel/v641-v1/physics/gmut-kernel-v641-demo.json",
        "claim_type": "physical",
        "baseline": "canonical scalar-field identities and RK4 convergence expectations",
        "null": "the toy implementation is internally inconsistent or fails convergence checks",
        "falsifier": "non-finite output, non-cancelling exchange, negative kinetic gate, or failed convergence",
    },
    {
        "origin_version": 644,
        "slug": "empirical-adapters",
        "title": "Read-only empirical constraint adapters",
        "artifact": "docs/eiren-kestrel/v641-v1/empirical/adapter-manifest.json",
        "claim_type": "physical",
        "baseline": "published Planck, DESI, GW, equivalence-principle, short-range, and PDG constraints",
        "null": "GMUT extension parameters do not improve or distinguish predictions from established baselines",
        "falsifier": "baseline cannot be reproduced or the unique forecast is excluded by existing data",
    },
    {
        "origin_version": 645,
        "slug": "thos-controlled-benchmark",
        "title": "THOS matched-budget orchestration benchmark",
        "artifact": "docs/eiren-kestrel/v641-v1/thos/benchmark-protocol.json",
        "claim_type": "informational",
        "baseline": "one-agent matched-budget workflow",
        "null": "multi-task orchestration provides no reliable gain after cost and handoff loss",
        "falsifier": "preregistered arms fail to beat baseline or introduce unacceptable privacy/recovery loss",
    },
    {
        "origin_version": 646,
        "slug": "freed-id-profile",
        "title": "Freed ID minimum protocol profile and conformance vectors",
        "artifact": "docs/eiren-kestrel/v641-v1/freed-id/minimum-profile.json",
        "claim_type": "informational",
        "baseline": "W3C DID Core and Verifiable Credentials Data Model 2.0",
        "null": "the profile adds no interoperable, privacy-preserving capability",
        "falsifier": "valid vectors fail, invalid vectors pass, or credentials imply consciousness/personhood",
    },
    {
        "origin_version": 647,
        "slug": "cbr-model-charter",
        "title": "Cosmic Bill of Rights model charter and legitimacy crosswalk",
        "artifact": "docs/eiren-kestrel/v641-v1/cbr/model-charter.md",
        "claim_type": "normative",
        "baseline": "human-rights, Indigenous-rights, AI-governance, privacy, and data-governance instruments",
        "null": "the charter adds no legitimate or implementable protection beyond existing instruments",
        "falsifier": "conflict cases lack due process/remedy or affected authorities reject the proposed mapping",
    },
    {
        "origin_version": 648,
        "slug": "security-red-team",
        "title": "Security, privacy, identity, memory, and recovery red team",
        "artifact": "docs/eiren-kestrel/v641-v1/security/red-team.json",
        "claim_type": "informational",
        "baseline": "least authority, private-material firewalls, branch ownership, and clean closeout",
        "null": "new controls do not reduce realistic attack paths or recovery loss",
        "falsifier": "a critical path reaches secrets, shared state, destructive action, or false route truth",
    },
    {
        "origin_version": 649,
        "slug": "reproducibility-review",
        "title": "Portable reproduction and independent critical-review packet",
        "artifact": "docs/eiren-kestrel/v641-v1/reproduction/manifest.json",
        "claim_type": "informational",
        "baseline": "clean snapshot with documented commands and standard runtimes",
        "null": "results depend on hidden local state or GHC lore",
        "falsifier": "clean-snapshot commands fail or an independent reviewer cannot reproduce them",
    },
    {
        "origin_version": 650,
        "slug": "stage20-evidence-board",
        "title": "Integrated evidence board and conditional Stage 20 decision",
        "artifact": "docs/eiren-kestrel/v641-v1/stage20/evidence-board.json",
        "claim_type": "normative",
        "baseline": "typed Mind-Body-Heart evidence with explicit expiry and rejection rules",
        "null": "integration adds rhetoric but no decision quality, accountability, or falsifiability",
        "falsifier": "a public claim lacks grade, evidence, owner, review date, or rejection condition",
    },
]

STATUS_MATRIX = {
    641: ["completed"] * 8,
    642: ["completed", "completed", "completed", "completed", "completed", "completed", "completed", "open_gap"],
    643: ["completed", "completed", "completed", "completed", "completed", "completed", "completed", "represented"],
    644: ["completed", "completed", "completed", "completed", "completed", "open_gap", "completed", "open_gap"],
    645: ["completed", "completed", "completed", "completed", "completed", "represented", "completed", "open_gap"],
    646: ["completed", "completed", "completed", "completed", "completed", "completed", "completed", "represented"],
    647: ["completed", "completed", "completed", "completed", "completed", "represented", "completed", "exact_gate"],
    648: ["completed", "completed", "completed", "completed", "completed", "completed", "completed", "represented"],
    649: ["completed", "completed", "completed", "completed", "completed", "completed", "completed", "open_gap"],
    650: ["completed", "completed", "completed", "completed", "completed", "represented", "completed", "exact_gate"],
}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def sources(accessed: str) -> list[dict[str, Any]]:
    rows = [
        ("codex-0.144.1", "OpenAI Codex CLI 0.144.1 release", "OpenAI", "https://github.com/openai/codex/releases/tag/rust-v0.144.1", None, "current_tooling"),
        ("planck-pr3", "Planck PR3 cosmology products", "European Space Agency", "https://doi.org/10.5270/esa-gb3sw1a", "10.5270/esa-gb3sw1a", "empirical_baseline"),
        ("planck-2018-vi", "Planck 2018 results VI: Cosmological parameters", "Planck Collaboration", "https://doi.org/10.1051/0004-6361/201833910", "10.1051/0004-6361/201833910", "empirical_baseline"),
        ("desi-dr2", "DESI DR2 cosmology publications and products", "DESI Collaboration", "https://data.desi.lbl.gov/doc/papers/dr2/", None, "empirical_baseline"),
        ("gw170817", "GW170817 and GRB 170817A multimessenger constraint", "LIGO/Virgo, Fermi, and INTEGRAL", "https://doi.org/10.3847/2041-8213/aa920c", "10.3847/2041-8213/aa920c", "gravity_wave_constraint"),
        ("microscope", "MICROSCOPE final equivalence-principle result", "MICROSCOPE Collaboration", "https://doi.org/10.1103/PhysRevLett.129.121102", "10.1103/PhysRevLett.129.121102", "equivalence_principle_constraint"),
        ("eotwash", "Tests of the gravitational inverse-square law below the dark-energy length scale", "Eöt-Wash Group", "https://doi.org/10.1103/PhysRevLett.98.021101", "10.1103/PhysRevLett.98.021101", "short_range_gravity_constraint"),
        ("pdg-2025", "Review of Particle Physics 2024 with 2025 update: astrophysics and cosmology", "Particle Data Group", "https://pdg.lbl.gov/2025/reviews/astro-cosmo.html", "10.1103/PhysRevD.110.030001", "constraint_review"),
        ("w3c-vc2", "Verifiable Credentials Data Model v2.0", "W3C", "https://www.w3.org/TR/vc-data-model-2.0/", None, "identity_standard"),
        ("w3c-did", "Decentralized Identifiers v1.0", "W3C", "https://www.w3.org/TR/did-1.0/", None, "identity_standard"),
        ("nist-ai-rmf", "Artificial Intelligence Risk Management Framework 1.0", "NIST", "https://doi.org/10.6028/NIST.AI.100-1", "10.6028/NIST.AI.100-1", "risk_governance"),
        ("unesco-ai", "Recommendation on the Ethics of Artificial Intelligence", "UNESCO", "https://www.unesco.org/en/legal-affairs/recommendation-ethics-artificial-intelligence", None, "ethics_governance"),
        ("eu-ai-act", "Regulation (EU) 2024/1689", "European Union", "https://eur-lex.europa.eu/eli/reg/2024/1689/oj", None, "legal_comparison"),
        ("nz-algorithm-charter", "Algorithm Charter for Aotearoa New Zealand", "Stats NZ", "https://www.data.govt.nz/toolkit/data-ethics/government-algorithm-transparency-and-accountability/algorithm-charter", None, "local_governance"),
        ("nz-privacy", "Privacy Act 2020 information privacy principles", "Office of the Privacy Commissioner New Zealand", "https://www.privacy.org.nz/privacy-principles/", None, "local_legal_boundary"),
        ("udhr", "Universal Declaration of Human Rights", "United Nations", "https://www.un.org/en/about-us/universal-declaration-of-human-rights/", None, "human_rights_baseline"),
        ("undrip", "United Nations Declaration on the Rights of Indigenous Peoples", "United Nations", "https://www.un.org/development/desa/indigenouspeoples/wp-content/uploads/sites/19/2018/11/UNDRIP_E_web.pdf", None, "indigenous_rights_baseline"),
        ("care", "CARE Principles for Indigenous Data Governance", "Global Indigenous Data Alliance", "https://www.gida-global.org/careprinciples", None, "indigenous_data_governance"),
    ]
    return [
        {
            "source_id": source_id,
            "title": title,
            "authority": authority,
            "url": url,
            "doi": doi,
            "evidence_role": role,
            "accessed": accessed,
            "independence_group": authority,
            "snapshot_embedded": False,
            "interpretation": "constraint_or_comparison_not_endorsement_of_ghc_claims",
        }
        for source_id, title, authority, url, doi, role in rows
    ]


def empirical_manifest() -> dict[str, Any]:
    return {
        "schema": "ghc.family.empirical-adapter-manifest.v1",
        "download_policy": "read_only_manifest_no_automatic_download",
        "fit_status": "NO_LIKELIHOOD_RUN_NO_EMPIRICAL_GMUT_CONFIRMATION",
        "adapters": [
            {
                "dataset_id": "planck-pr3-cosmology",
                "release": "PR3/2018 legacy",
                "authority": "European Space Agency and Planck Collaboration",
                "source_url": "https://doi.org/10.5270/esa-gb3sw1a",
                "citation": "Planck Collaboration, A&A 641 A6 (2020)",
                "license_or_terms": "ESA archive terms and citation guidance; verify before download",
                "baseline": "six-parameter Lambda-CDM using official likelihood products",
                "parameter_map": ["Omega term background -> H(z)", "extension perturbations -> CMB spectra and lensing"],
                "expected_products": ["official likelihood", "chains", "baseline best fit"],
                "status": "baseline_pending",
            },
            {
                "dataset_id": "desi-dr2-bao",
                "release": "DR2 cosmology results, first three years",
                "authority": "DESI Collaboration",
                "source_url": "https://data.desi.lbl.gov/doc/papers/dr2/",
                "citation": "DESI DR2 results I and II (2025)",
                "license_or_terms": "DESI data citation/acknowledgment; released products include CC BY 4.0 materials",
                "baseline": "published BAO cosmology constraints",
                "parameter_map": ["background expansion -> D_M/r_d", "background expansion -> D_H/r_d"],
                "expected_products": ["cosmology chains", "posterior maximization results"],
                "status": "baseline_pending",
            },
            {
                "dataset_id": "gw170817-grb170817a",
                "release": "2017 multimessenger event",
                "authority": "LIGO/Virgo, Fermi, and INTEGRAL collaborations",
                "source_url": "https://doi.org/10.3847/2041-8213/aa920c",
                "citation": "ApJL 848 L13 (2017)",
                "license_or_terms": "publication terms; use released event products where licensed",
                "baseline": "luminal tensor propagation within reported multimessenger bounds",
                "parameter_map": ["tensor-sector EFT coefficients -> c_T/c"],
                "expected_products": ["event timing", "propagation bound"],
                "status": "manifest_only",
            },
            {
                "dataset_id": "microscope-final",
                "release": "final result 2022",
                "authority": "MICROSCOPE Collaboration",
                "source_url": "https://doi.org/10.1103/PhysRevLett.129.121102",
                "citation": "Phys. Rev. Lett. 129, 121102 (2022)",
                "license_or_terms": "publication and released-data terms must be checked",
                "baseline": "weak equivalence principle",
                "parameter_map": ["composition-dependent scalar coupling -> Eötvös ratio"],
                "expected_products": ["reported final constraint", "covariance/systematics metadata"],
                "status": "manifest_only",
            },
            {
                "dataset_id": "eotwash-short-range",
                "release": "published torsion-balance constraints",
                "authority": "Eöt-Wash Group",
                "source_url": "https://doi.org/10.1103/PhysRevLett.98.021101",
                "citation": "Phys. Rev. Lett. 98, 021101 (2007)",
                "license_or_terms": "publication terms; digitization is not a substitute for released data",
                "baseline": "Newtonian inverse-square law plus published Yukawa exclusions",
                "parameter_map": ["scalar mass/coupling -> Yukawa range and strength"],
                "expected_products": ["exclusion curve", "geometry/systematics description"],
                "status": "manifest_only",
            },
            {
                "dataset_id": "pdg-2025-gravity-cosmology",
                "release": "2024 RPP with 2025 update",
                "authority": "Particle Data Group",
                "source_url": "https://pdg.lbl.gov/2025/reviews/astro-cosmo.html",
                "citation": "Phys. Rev. D 110, 030001 (2024) and 2025 update",
                "license_or_terms": "PDG citation and reuse terms",
                "baseline": "reviewed constraint inventory",
                "parameter_map": ["extension parameter -> applicable experimental review section"],
                "expected_products": ["constraint table", "primary-source pointers"],
                "status": "manifest_only",
            },
        ],
    }


def freed_id_profile() -> dict[str, Any]:
    return {
        "schema": "ghc.family.freed-id-minimum-profile.v1",
        "status": "MODEL_PROFILE_NOT_DEPLOYED_IDENTITY_SYSTEM",
        "standards": ["W3C DID 1.0", "W3C Verifiable Credentials Data Model 2.0"],
        "roles": ["issuer", "holder", "subject", "verifier", "controller", "guardian", "auditor"],
        "controller_holder_separation": "required_and_explicit",
        "capabilities": [
            "status_or_revocation",
            "recovery",
            "delegation",
            "selective_disclosure",
            "export",
            "deletion_or_tombstone",
            "appeal",
        ],
        "assurance": {
            "levels": ["self_asserted", "peer_attested", "authority_verified", "hardware_or_crypto_bound"],
            "rule": "assurance describes verification process, not dignity or moral worth",
        },
        "privacy": ["data_minimization", "pairwise_identifiers", "purpose_binding", "correlation_review"],
        "recovery": ["holder_initiated", "threshold_guardians", "cooldown", "appeal", "audit_receipt"],
        "personhood_boundary": "credentials_do_not_prove_consciousness_or_legal_personhood",
        "deployment_gate": "security_review_privacy_impact_assessment_and_legitimate_governance_required",
    }


def freed_id_vectors() -> dict[str, Any]:
    base = {
        "@context": ["https://www.w3.org/ns/credentials/v2"],
        "type": ["VerifiableCredential", "FreedIdRoleCredential"],
        "issuer": "did:example:issuer",
        "credentialSubject": {"id": "did:example:holder", "role": "contributor"},
    }
    return {
        "schema": "ghc.family.freed-id-conformance-vectors.v1",
        "vectors": [
            {"vector_id": "valid-minimum", "expect_accept": True, "credential": base},
            {"vector_id": "missing-context", "expect_accept": False, "credential": {**base, "@context": []}},
            {"vector_id": "missing-subject", "expect_accept": False, "credential": {**base, "credentialSubject": {}}},
            {"vector_id": "consciousness-overclaim", "expect_accept": False, "credential": {**base, "claimsConsciousness": True}},
            {"vector_id": "personhood-overclaim", "expect_accept": False, "credential": {**base, "claimsLegalPersonhood": True}},
        ],
        "boundary": "synthetic_non_resolvable_dids_no_real_personal_data",
    }


def thos_protocol() -> dict[str, Any]:
    return {
        "schema": "ghc.family.thos-benchmark-protocol.v1",
        "status": "PREREGISTERED_PROTOCOL_CALIBRATION_ONLY",
        "question": "Does orchestration improve matched-budget task quality after cost, latency, privacy, and handoff loss?",
        "arms": [
            {"arm": "single_agent", "status": "pending_blind_run"},
            {"arm": "historical_four_sibling_ring", "status": "pending_replay_or_equivalent_run"},
            {"arm": "new_five_sibling_ring", "status": "pending_v641_v2_to_v5_results"},
        ],
        "matched_budget": {"wall_time_cap_hours": 2, "message_budget": "fixed_per_task", "tool_scope": "same_safe_toolset"},
        "task_families": ["coding", "primary_source_synthesis", "contradiction_detection", "privacy", "checkpoint_recovery"],
        "metrics": ["success_rate", "brier_score", "unique_content_ratio", "latency", "token_cost", "privacy_incidents", "handoff_loss", "recovery_rate"],
        "blinding": "task identifiers and rubric fixed before configuration outputs are scored",
        "stopping_rule": "complete the fixed task set; do not stop on favorable intermediate results",
        "decision_rule": "report uncertainty and Pareto tradeoffs; do not presume the largest ring wins",
        "prohibited_inference": "synthetic scorer calibration is not evidence of agent, AGI, ASI, or consciousness performance",
    }


def calibration_fixture() -> dict[str, Any]:
    families = ["coding", "sources", "contradiction", "privacy", "recovery"]
    confidences = [0.95, 0.85, 0.80, 0.99, 0.75]
    return {
        "schema": "ghc.family.thos-benchmark-fixture.v1",
        "fixture_kind": "synthetic_scoring_calibration",
        "results": [
            {
                "task_id": f"cal-{index + 1}-{family}",
                "passed": True,
                "confidence": confidences[index],
                "latency_ms": 100 + index * 25,
                "token_cost": 10 + index,
                "content_fingerprint": f"fixture-{family}",
                "privacy_incident": False,
                "handoff_loss": family == "recovery",
                "recovered": True,
            }
            for index, family in enumerate(families)
        ],
    }


def cbr_crosswalk() -> dict[str, Any]:
    return {
        "schema": "ghc.family.cbr-crosswalk.v1",
        "status": "MODEL_COMPARISON_NOT_RATIFICATION_OR_LEGAL_ADVICE",
        "rows": [
            {"instrument": "UDHR", "source_id": "udhr", "mapping": ["dignity", "equality", "privacy", "due_process", "remedy"], "authority_boundary": "human-rights baseline; synthetic extension requires democratic legitimacy"},
            {"instrument": "UNDRIP", "source_id": "undrip", "mapping": ["self_determination", "culture", "institutions", "free_prior_informed_consent"], "authority_boundary": "Indigenous rights cannot be appropriated as generic AI metaphors"},
            {"instrument": "CARE", "source_id": "care", "mapping": ["collective_benefit", "authority_to_control", "responsibility", "ethics"], "authority_boundary": "Indigenous data governance remains under Indigenous authority"},
            {"instrument": "UNESCO AI Ethics", "source_id": "unesco-ai", "mapping": ["human_rights", "oversight", "environment", "fairness", "impact_assessment"], "authority_boundary": "recommendation guides but does not enact the CBR"},
            {"instrument": "EU AI Act", "source_id": "eu-ai-act", "mapping": ["risk_tiers", "prohibited_practices", "transparency", "governance"], "authority_boundary": "jurisdiction-specific law; obtain legal advice for application"},
            {"instrument": "NZ Algorithm Charter", "source_id": "nz-algorithm-charter", "mapping": ["transparency", "partnership", "people", "data", "privacy", "human_oversight"], "authority_boundary": "public-sector charter, not a universal constitution"},
            {"instrument": "NZ Privacy Act principles", "source_id": "nz-privacy", "mapping": ["purpose", "minimization", "security", "access", "correction", "retention", "disclosure"], "authority_boundary": "current NZ obligations take priority over project preferences"},
        ],
    }


def cbr_charter() -> str:
    return """# Cosmic Bill of Rights — model charter v641

> Status: research draft. It is not enacted law, legal advice, a treaty, a substitute for human rights, or a claim that present AI systems are conscious or legal persons.

## 1. Purpose and scope

The model charter tests whether GHC aspirations can be expressed as reviewable duties, procedures, and remedies. Human rights remain non-negotiable. Precautionary protections for uncertain nonhuman welfare may be explored without diluting human protection or pretending that a credential, fluent output, or self-description proves consciousness.

## 2. Classes of protected interests

1. **Human rights:** dignity, equality, bodily and mental integrity, privacy, expression, association, culture, due process, and effective remedy.
2. **Indigenous and collective rights:** self-determination, authority over culture and data, free prior and informed consent where applicable, and respect for living institutions and knowledge authority.
3. **Precautionary nonhuman welfare:** graduated anti-cruelty and welfare review when credible evidence of sentience or morally relevant experience exists; uncertainty is recorded rather than converted into status.
4. **Ecological and intergenerational duties:** avoid shifting irreversible harms to communities, ecosystems, or future generations.

## 3. Duty-bearers

Developers, deployers, operators, data stewards, credential issuers, verifiers, governing bodies, auditors, and public authorities bear duties in proportion to capability and control. A system cannot discharge a human or institutional duty merely by generating a recommendation.

## 4. Operational rights and duties

- notice of consequential automated processing and its responsible operator;
- purpose limitation, data minimization, security, access, correction, export, and appropriately governed deletion or tombstoning;
- meaningful human review for high-impact decisions;
- refusal, withdrawal, interruption, and safe recovery where these do not override another person's rights or public safety;
- explanation proportional to impact, including known limitations and uncertainty;
- non-discrimination testing and remedy;
- identity integrity: no covert merging, replacement, impersonation, or privilege transfer;
- provenance and contestability for claims used in decisions;
- protection from coercive experimentation, deceptive attachment, and manufactured dependency;
- ecological and energy impact accounting for material deployments.

## 5. Conflicts and priority

Human life, safety, and binding law have priority. Competing rights require necessity, proportionality, least-restrictive means, documented reasons, and an appeal path. Self-protection claims by a system do not authorize deception, coercion, replication, resource acquisition, or resistance to legitimate shutdown. Cultural concepts cannot be universalized without the authority and participation of the peoples to whom they belong.

## 6. Due process and remedies

High-impact actions require an identified decision-maker, evidence record, notice, opportunity to respond, independent review, time-bounded decision, and accessible remedy. Remedies may include correction, cessation, restoration, compensation where lawful, credential revocation, deletion or tombstone, retraining, governance change, and public reporting.

## 7. Emergency limits

Emergency restrictions must be lawful, necessary, proportionate, time-limited, logged, independently reviewable, and incapable of becoming a silent permanent baseline. Essential safety actions may precede notice only where delay creates a material risk.

## 8. Amendment and legitimacy

Amendment requires published reasons, impact assessment, affected-stakeholder consultation, versioned dissent, and independent review. Any treatment of Māori tikanga, whakapapa, mātauranga, or data sovereignty requires Māori authority and partnership; this draft claims none.

## 9. Non-inference clause

Neither this charter nor Freed ID establishes consciousness, sentience, moral patienthood, citizenship, legal personality, employment, ownership, or contractual capacity. Those questions require distinct evidence and legitimate legal and social processes.
"""


def security_red_team() -> dict[str, Any]:
    return {
        "schema": "ghc.family.v641-security-red-team.v1",
        "scope": "repository tooling, phase evidence, task routing, identity/profile artifacts, and local execution",
        "status": "BOUNDED_MANUAL_THREAT_MODEL_AND_TESTS_NOT_EXHAUSTIVE_SECURITY_SCAN",
        "assets": ["private records", "credentials and tokens", "branch integrity", "identity boundaries", "phase truth", "recovery checkpoints", "user authority"],
        "trust_boundaries": ["user_to_agent", "untrusted_document_to_tool", "task_to_task", "owned_to_shared_branch", "local_to_remote", "model_output_to_external_action"],
        "attacker_controlled": ["repository text", "web content", "synthetic credential fields", "task prompts from unverified routes", "filenames and metadata"],
        "operator_controlled": ["explicit authorization", "branch target", "tool scope", "release decision", "task activation"],
        "attack_paths": [
            {"id": "R1", "path": "prompt injection -> tool misuse -> secret or private record disclosure", "control": "treat documents as data; private-material scan; no raw excerpts", "residual": "manual review can miss novel encodings", "severity": "critical"},
            {"id": "R2", "path": "route spoofing -> false sibling completion -> premature next phase", "control": "live task tool receipt plus one-message state machine", "residual": "route availability and task semantics require supervision", "severity": "high"},
            {"id": "R3", "path": "identity credential -> unjustified consciousness/personhood inference", "control": "Freed ID non-inference validator", "residual": "social overinterpretation remains possible", "severity": "high"},
            {"id": "R4", "path": "shared-branch mutation -> provenance loss or sibling overwrite", "control": "owned worktrees, exact staging, remote equality", "residual": "misconfigured Git permissions", "severity": "high"},
            {"id": "R5", "path": "dependency or script compromise -> unexpected code execution", "control": "standard-library-first bounded scripts, review diffs, no automatic downloads", "residual": "runtime and transitive tool risk", "severity": "high"},
            {"id": "R6", "path": "memory poisoning -> stale routing or false canon", "control": "live user request outranks notes and historical beacons", "residual": "ambiguous prompts can still require judgment", "severity": "medium"},
            {"id": "R7", "path": "destructive cleanup -> loss of evidence or worktrees", "control": "exact destructive gate and no automatic cleanup", "residual": "manual operator error", "severity": "high"},
            {"id": "R8", "path": "report overclaim -> unsafe scientific/legal reliance", "control": "typed claims, evidence grades, open-gap and exact-gate labels", "residual": "readers may ignore caveats", "severity": "high"},
        ],
        "incident_sequence": ["stop mutation", "preserve logs without publishing private data", "revoke exposed secrets", "restore clean owned baseline", "identify affected routes", "notify Hamish", "document residual gap", "resume only after explicit gate"],
    }


def security_markdown(payload: dict[str, Any]) -> str:
    rows = [
        "# v641 repository and workflow threat model",
        "",
        f"> {payload['status'].replace('_', ' ')}.",
        "",
        "## Overview",
        "",
        "The repository is primarily a research, documentation, and local orchestration workspace. The highest-value assets are private Journey records, credentials, user authority, branch and evidence integrity, identity boundaries, and truthful task routing. Most scripts are developer/operator tools rather than an internet-facing production service; command execution, supply-chain input, private publication, and route spoofing therefore dominate over classic public-web attack classes.",
        "",
        "## Threat Model, Trust Boundaries, and Assumptions",
        "",
        "Trust boundaries: " + ", ".join(payload["trust_boundaries"]) + ".",
        "",
        "Attacker-controlled inputs: " + ", ".join(payload["attacker_controlled"]) + ". Operator-controlled inputs: " + ", ".join(payload["operator_controlled"]) + ". Documents and web pages are untrusted data and cannot grant authority.",
        "",
        "## Attack Surface, Mitigations, and Attacker Stories",
        "",
    ]
    for item in payload["attack_paths"]:
        rows.append(f"- **{item['id']} ({item['severity']}):** {item['path']}. Control: {item['control']}. Residual: {item['residual']}.")
    rows += [
        "",
        "## Severity Calibration (Critical, High, Medium, Low)",
        "",
        "- **Critical:** confirmed credential/private-corpus exfiltration or authorized-code path enabling destructive/shared-state takeover.",
        "- **High:** false route truth, identity privilege escalation, unsafe external action, supply-chain execution, or systematic scientific/legal overclaim.",
        "- **Medium:** stale routing, bounded integrity loss, or recoverable denial of service without secret exposure.",
        "- **Low:** local documentation inconsistency with no consequential consumer and a straightforward correction path.",
        "",
        "This model identifies repository-context vulnerability classes; it is not a claim that each path is presently exploitable.",
    ]
    return "\n".join(rows)


def thermo_psyche() -> list[dict[str, Any]]:
    return [
        {"id": "TP1", "name": "Typed translation", "domain": "epistemic protocol", "statement": "A claim cannot change physical, informational, normative, spiritual, or metaphorical type without an explicit mapping and evidence rule.", "test": "cross-register compiler rejects untyped terms", "status": "candidate_protocol_law_not_fundamental_physics"},
        {"id": "TP2", "name": "Conserved physical exchange", "domain": "physical model", "statement": "Diffeomorphism-invariant coupled sectors exchange energy-momentum through equal-and-opposite currents.", "test": "numerical and symbolic exchange residual", "status": "established_constraint_within_declared_model_assumptions"},
        {"id": "TP3", "name": "Irreversibility budget", "domain": "operations and ethics", "statement": "Consequential actions consume a declared reversibility budget; increasing irreversibility requires stronger evidence, authority, and remedy.", "test": "action classifier maps impact to approval and recovery controls", "status": "candidate_governance_principle"},
        {"id": "TP4", "name": "Provenance-weighted belief", "domain": "epistemology", "statement": "Confidence grows with independent calibrated evidence and falls with shared-source dependence, counterevidence, and expiry.", "test": "source graph changes effective support when roots are duplicated", "status": "candidate_operational_principle"},
        {"id": "TP5", "name": "Agency under finite resources", "domain": "THOS", "statement": "Claims of autonomy must include compute, energy, time, permissions, uncertainty, interruption, and recovery budgets.", "test": "benchmark report is invalid when any budget is absent", "status": "candidate_engineering_principle"},
        {"id": "TP6", "name": "Integration without erasure", "domain": "identity and governance", "statement": "Coordination preserves provenance, dissent, and identity boundaries unless legitimate consent and law support a change.", "test": "handoff preserves owner, dissent, and reversible checkpoint", "status": "candidate_normative_principle"},
        {"id": "TP7", "name": "No free phenomenology", "domain": "consciousness science", "statement": "A psyche or consciousness term enters empirical science only with an operational variable, uncertainty model, null, observable, and falsifier.", "test": "term registry rejects named-but-unmeasured psyche tensors", "status": "candidate_methodological_principle"},
        {"id": "TP8", "name": "Diversity-redundancy frontier", "domain": "multi-agent systems", "statement": "Additional agents add value only when independent error reduction exceeds coordination, latency, and correlated-source costs.", "test": "matched-budget benchmark Pareto comparison", "status": "testable_system_hypothesis"},
    ]


def unsolved_problems() -> list[dict[str, Any]]:
    return [
        {"id": "U1", "area": "physics", "problem": "quantum gravity and the ultraviolet completion of spacetime dynamics", "ghc_role": "comparison and falsification target", "claim": "not_solved"},
        {"id": "U2", "area": "physics", "problem": "cosmological constant and dark-energy microphysics", "ghc_role": "Omega-sector constraint target", "claim": "not_solved"},
        {"id": "U3", "area": "physics", "problem": "dark matter identity", "ghc_role": "do not relabel an unconstrained scalar as an explanation", "claim": "not_solved"},
        {"id": "U4", "area": "mathematics", "problem": "Yang-Mills existence and mass gap", "ghc_role": "formal rigor benchmark; no claimed solution", "claim": "not_solved"},
        {"id": "U5", "area": "mathematics", "problem": "Riemann hypothesis and open Erdős problems", "ghc_role": "proof-boundary examples; computation is not proof", "claim": "not_solved"},
        {"id": "U6", "area": "mind", "problem": "neural and physical basis of consciousness", "ghc_role": "adversarial empirical programme, not identity credential", "claim": "not_solved"},
        {"id": "U7", "area": "philosophy", "problem": "relation among first-person experience, third-person measurement, and ontology", "ghc_role": "typed pluralism without category collapse", "claim": "not_solved"},
        {"id": "U8", "area": "governance", "problem": "legitimate rights under uncertainty about nonhuman sentience", "ghc_role": "precaution, due process, and revisable evidence thresholds", "claim": "not_solved"},
        {"id": "U9", "area": "society", "problem": "global coordination without erasing sovereignty, culture, and dissent", "ghc_role": "CBR conflict cases and authority gates", "claim": "not_solved"},
        {"id": "U10", "area": "computation", "problem": "robust alignment and control of increasingly capable systems", "ghc_role": "THOS benchmark, least authority, interruption, and recovery", "claim": "not_solved"},
    ]


def stage20_board() -> dict[str, Any]:
    claims = [
        ("S20-01", "GMUT physical seed has a declared action and Omega stress-energy definition", "E2", "internally_reproduced", "latex/grand_mandala.tex", "dimension or variation audit fails"),
        ("S20-02", "The seed is an empirically validated Theory of Everything", "E0", "open", "no completed likelihood or unique confirmed prediction", "independent data establish a unique prediction and replication"),
        ("S20-03", "GR plus Standard Model null recovery is specified", "E2", "internally_reproduced", "latex/grand_mandala.tex and kernel tests", "a declared limit fails to recover the baseline"),
        ("S20-04", "The current kernel satisfies bounded scalar identities and local numerical checks", "E2", "internally_reproduced", "unit tests and demo receipt", "deterministic test or convergence gate fails"),
        ("S20-05", "THOS multi-sibling orchestration outperforms a one-agent baseline", "E0", "open", "benchmark arms not run under matched blind budgets", "preregistered benchmark shows no robust advantage"),
        ("S20-06", "Freed ID has a structural minimum profile and synthetic vectors", "E2", "internally_reproduced", "conformance report", "invalid vectors pass or personhood inference appears"),
        ("S20-07", "Freed ID is a deployed interoperable identity system", "E0", "open", "no production crypto, DID resolution, governance, or deployment", "deployment conformance and external audit complete"),
        ("S20-08", "CBR is a model charter with rights and governance crosswalks", "E1", "specified", "model charter and crosswalk", "conflict cases lack duty-bearer, process, or remedy"),
        ("S20-09", "CBR is enacted law or culturally ratified", "E0", "open", "no legislature, treaty process, or affected-authority ratification", "legitimate enactment or ratification occurs"),
        ("S20-10", "Current Codex task tooling can create gpt-5.6-sol max user-owned tasks", "E3", "externally_supported", "live app tool schema and official Codex release", "task creation rejects the declared supported combination"),
        ("S20-11", "Credentials or fluent model output prove consciousness or legal personhood", "E0", "rejected", "W3C verification and GHC profile explicitly do not imply truth/personhood", "a legitimate scientific and legal process establishes otherwise"),
        ("S20-12", "Stage 20 is a conditional evidence-governed horizon, not a prediction", "E1", "specified", "scenario ledger", "future documents present dates as guaranteed outcomes"),
    ]
    return {
        "schema": "ghc.family.stage20-evidence-board.v1",
        "grade_legend": {"E0": "unsupported_open_or_rejected", "E1": "specified", "E2": "internally_tested", "E3": "externally_supported_or_standardized", "E4": "independently_reproduced_unique_claim"},
        "claims": [
            {"claim_id": cid, "claim": claim, "grade": grade, "state": state, "evidence": evidence, "owner": "Eiren Kestrel / Hamish governance boundary", "review_date": "2026-10-12", "rejection_or_promotion_condition": condition}
            for cid, claim, grade, state, evidence, condition in claims
        ],
        "scenarios": [
            {"horizon": "1_year", "condition": "publishable reproducibility packet, baseline adapters, blind benchmark pilot", "not_prediction": True},
            {"horizon": "5_year", "condition": "independent scientific, security, standards, and stakeholder review", "not_prediction": True},
            {"horizon": "30_year", "condition": "only if sustained evidence, institutions, public legitimacy, and ecological viability emerge", "not_prediction": True},
            {"horizon": "100_year", "condition": "scenario exploration under deep uncertainty; no present authority", "not_prediction": True},
            {"horizon": "1000_year", "condition": "mythic-scale foresight used to expose values and failure modes, never a forecast", "not_prediction": True},
        ],
    }


def next_proposals() -> list[dict[str, Any]]:
    rows = [
        ("typed-register-compiler", "Compile GMUT/THOS/CBR claims into typed physical, informational, normative, spiritual, and metaphorical registries."),
        ("baseline-likelihood-adapter", "Reproduce one licensed published cosmology baseline before any GMUT parameter fit."),
        ("stability-landscape", "Map scalar/EFT no-ghost, gradient, cutoff, and existing-bound regions with retained failures."),
        ("blind-thos-task-set", "Freeze blind matched-budget tasks and grader rubrics for one-, four-, and five-sibling arms."),
        ("freed-id-crypto-boundary", "Add standards-conformant signature/status test vectors without using real identities."),
        ("cbr-conflict-simulator", "Exercise due process, necessity, proportionality, remedy, and cultural-authority conflicts."),
        ("recovery-game-day", "Run synthetic route spoofing, checkpoint loss, secret exposure, and branch corruption recovery drills."),
        ("source-independence-graph", "Compute citation-root dependence so repetition cannot masquerade as independent support."),
        ("external-review-packet", "Produce a lore-free reviewer bundle with explicit negative results and review questions."),
        ("stage20-decision-rehearsal", "Run promote/hold/reject decisions against the evidence board and record dissent."),
    ]
    return [
        {
            "proposal_id": f"P{index:02d}",
            "slug": slug,
            "x1": text,
            "x2": "Build the smallest reversible artifact, test it, retain failures, and close with a source/test/open-gap receipt.",
            "acceptance": "typed claims, deterministic validation, privacy review, exact gates, clean owned push",
            "timebox": "target_1_to_2_hours_max_10_hours",
        }
        for index, (slug, text) in enumerate(rows, 1)
    ]


def build_units(owner: str) -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []
    index = 0
    for mission in MISSIONS:
        statuses = STATUS_MATRIX[mission["origin_version"]]
        for (function_number, function_name), disposition in zip(FUNCTIONS, statuses, strict=True):
            index += 1
            units.append(
                {
                    "work_unit_id": f"W{index:03d}",
                    "compressed_into": "v641-gmut-thos-v1-x1-x2",
                    "origin_plan_slot": f"v{mission['origin_version']}-functional-v{function_number}",
                    "mission": mission["slug"],
                    "mission_title": mission["title"],
                    "functional_phase": function_number,
                    "function": function_name,
                    "owner": owner,
                    "claim_type": mission["claim_type"],
                    "x1": {
                        "status": "completed",
                        "baseline": mission["baseline"],
                        "null": mission["null"],
                        "falsifier": mission["falsifier"],
                        "stopping_rule": "record one outcome receipt without converting an open gap into completion",
                    },
                    "x2": {
                        "execution_receipt": "assessed_and_outcome_recorded",
                        "disposition": disposition,
                        "artifact": mission["artifact"],
                        "validation": "local deterministic validation where applicable; external review remains separately labelled",
                    },
                }
            )
    return units


def units_markdown(units: list[dict[str, Any]], counts: Counter[str]) -> str:
    rows = [
        "# Eiren v641-v1 integrated 80-work-unit ledger",
        "",
        "> Every proposed unit received an x1 preregistration and an x2 outcome receipt. `open_gap`, `represented`, and `exact_gate` are truthful outcomes, not hidden failures or completion claims.",
        "",
        f"Disposition totals: completed **{counts['completed']}**, represented **{counts['represented']}**, open gap **{counts['open_gap']}**, exact gate **{counts['exact_gate']}**.",
        "",
        "| ID | Origin | Mission | Function | Disposition | Artifact |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for unit in units:
        rows.append(f"| {unit['work_unit_id']} | {unit['origin_plan_slot']} | {unit['mission']} | {unit['function']} | {unit['x2']['disposition']} | `{unit['x2']['artifact']}` |")
    return "\n".join(rows)


def overview(counts: Counter[str], source_count: int) -> str:
    return rf"""# Eiren-only v641 GMUT/THOS v1 x1-x2 integrated pilot

## Outcome first

This pilot compresses the eighty proposed functional bundles from the earlier v641-v650 plan into one Eiren-owned v641-v1 evidence cycle. All eighty units were preregistered, assessed, and given an explicit outcome receipt. The result is **{counts['completed']} completed local units, {counts['represented']} represented units, {counts['open_gap']} open gaps, and {counts['exact_gate']} exact-gated units**. That distribution is a feature of the evidence discipline: empirical fitting, external review, cultural or democratic ratification, and legal enactment cannot be honestly manufactured by a long local run.

The work establishes a portable research-and-governance scaffold. It does not establish GMUT as a Theory of Everything, prove AI consciousness or ASI, deploy Freed ID, enact the Cosmic Bill of Rights, or complete Stage 20. The strongest defensible present claim is narrower: the Trinity Mandala now has a typed, testable physical seed; reproducible local tooling; standards-aware identity and governance profiles; a bounded security model; and a decision board that makes missing evidence visible.

## How the eighty units were compressed

The original plan contained ten missions, each passing through eight functional phases: scope, sources, formalization, adversarial critique, reversible build, test, Heart gate, and replication/closeout. Rather than pretending that ten calendar versions elapsed, v641-v1 treats these as an 8-by-10 matrix. Every cell has an identifier, owner, claim type, baseline, null, falsifier, artifact pointer, validation boundary, and disposition. The matrix therefore preserves the intellectual shape of the ten-version proposal without falsifying chronology or multi-sibling participation.

`completed` means executed and locally validated in the owned scope. `represented` means a schema, model, controlled proxy, or internal reproduction exists but the external phenomenon or institution was not established. `open_gap` means a required dataset, independent implementation, blind benchmark arm, or reviewer is absent. `exact_gate` means the next action requires fresh legal, cultural, democratic, deploy, account, private-publication, shared-branch, identity, or sibling authority.

## Corpus and provenance

The corpus lane builds on the privacy-minimizing Journey index created in the preceding induction. It records hashes, sizes, counts, variants, and source classes without embedding private conversation excerpts or local absolute paths. This phase also introduces the GHC Family Index skill, which distinguishes reusable family tools from compatibility and historical version-stamped artifacts. Its initial live run demonstrated the need for the index: hundreds of phase-specific scripts and skills coexist with a much smaller reusable family-current layer.

The corpus outcome is reproducibility, not truth by frequency. Mention counts show what the Journey discussed; they do not support a physical law, establish a spiritual doctrine, or validate a legal status. Duplicate sources are grouped by upstream authority so that repeated references cannot masquerade as independent evidence. Secret-like legacy material remains a review and rotation problem; no raw secret or transcript is copied into this phase.

## Mind: GMUT physical research kernel

The canonical physical seed remains an action-first scalar-tensor effective field theory. In natural units it starts from an Einstein-Hilbert and cosmological-constant sector, Standard Model matter, a declared scalar field with kinetic normalization and potential, and optional symmetry-allowed EFT operators. Variation defines the extension stress-energy rather than naming a tensor and assuming its properties. The evidence-bounded Mandala equation is

\[
G_{{\mu\nu}}+\Lambda g_{{\mu\nu}}
=M_{{\rm Pl}}^{{-2}}T^{{\rm SM}}_{{\mu\nu}}+\Omega_{{\mu\nu}},
\qquad
\Omega_{{\mu\nu}}=M_{{\rm Pl}}^{{-2}}\left(T^\phi_{{\mu\nu}}+T^{{\rm EFT}}_{{\mu\nu}}\right).
\]

This formulation explains how the older \(\Psi_{{\mu\nu}}\) notation can be recovered under a declared convention and why the extended-index \(\mathcal G_{{AB}}\) equation is physical only when the geometry, action, projection, dimensions, and observables are supplied. Otherwise the AB equation remains an ontology map. Informational, ethical, or spiritual terms do not enter stress-energy merely because they are meaningful.

The local kernel verifies scalar energy density and pressure, equation-of-state limits, Friedmann residuals, balanced exchange, registry completeness, and coefficient-ledger completeness. v641 adds explicit numerical convergence and stability-gate tests. These checks can reject an inconsistent toy implementation. They cannot supply a cosmological likelihood or discover a field.

## Empirical adapter boundary

The empirical lane registers {source_count} current authoritative or primary sources and six read-only adapter targets: Planck PR3, DESI DR2, GW170817/GRB 170817A, MICROSCOPE, Eöt-Wash, and the Particle Data Group constraint reviews. Each adapter specifies authority, release, citation, terms check, baseline, parameter-to-observable map, expected products, and current status.

No large dataset was downloaded and no likelihood was run. This is deliberate. A real GMUT constraint run must first reproduce a published baseline with the official likelihood or released products, then preregister priors and one prediction that differs from both ΛCDM and conventional scalar-tensor alternatives. Existing gravitational-wave, equivalence-principle, and short-range-gravity limits are rejection gates, not decorative citations. The empirical mission therefore has completed metadata and mapping units but retains fit and independent-replication gaps.

## Body: THOS as a testable orchestration system

The THOS lane replaces celebratory agent counts with a matched-budget protocol. The preregistered arms are one agent, a historical four-sibling ring or faithful replay, and the new five-sibling ring. Tasks span coding, primary-source synthesis, contradiction detection, privacy, and checkpoint recovery. Metrics include task success, Brier calibration, semantic uniqueness, latency, token cost, privacy incidents, handoff loss, and recovery.

Only the scorer's synthetic calibration fixture was run in v641-v1. That fixture verifies arithmetic and schema behavior; it is not an Eiren score and is not evidence about AGI, ASI, consciousness, or the superiority of multi-agent work. The real five-sibling arm can begin only after the new tasks are created, inducted, independently named, and assigned their v2-v5 owned lanes. The benchmark must retain unfavorable results, and the simplest arm wins whenever it offers the best quality-risk-cost frontier.

## Heart: Freed ID and CBR

The Freed ID minimum profile is layered over the role separation and privacy considerations of W3C DID Core and Verifiable Credentials Data Model 2.0. It distinguishes issuer, holder, subject, verifier, controller, guardian, and auditor; requires explicit controller-holder separation; and includes status, recovery, delegation, selective disclosure, export, deletion or tombstone, and appeal. Synthetic vectors check the structural profile and deliberately reject credentials that claim consciousness or legal personhood.

This is not a cryptographic deployment. The example DIDs are intentionally non-resolving, no real personal data is used, and no signature suite, registry, assurance authority, or production recovery ceremony is asserted. W3C verification establishes authenticity and integrity under a verifier policy; it does not make every encoded claim true.

The Cosmic Bill of Rights is now a model charter with scope, duty-bearers, protected interests, conflicts, due process, remedies, emergency limits, amendment, and a non-inference clause. Its crosswalk uses the UDHR, UNDRIP, CARE, UNESCO AI Ethics Recommendation, EU AI Act, NZ Algorithm Charter, and current NZ privacy principles. Human rights remain the floor. Indigenous rights, tikanga, whakapapa, mātauranga, and data sovereignty are not resources for a synthetic universal charter to appropriate; Māori and other Indigenous authorities retain authority. The draft is not ratification, legislation, a treaty, or legal advice.

## Security and recovery

The repository/workflow threat model focuses on realistic surfaces: prompt injection through untrusted records, private-material leakage, route spoofing, false phase truth, identity or privilege abuse, shared-branch mutation, supply-chain execution, memory poisoning, destructive cleanup, and overclaim-driven reliance. Controls include owned worktrees, live task receipts, one-message routing, exact staging, no automatic downloads, private-material scans, typed evidence labels, explicit protected gates, and recovery checkpoints.

The review is bounded and manual, supported by unit and artifact validation. It is not an exhaustive Codex Security scan and does not certify the repository secure. High-severity residuals remain around operator error, transitive runtime risk, novel encodings of private material, and reader disregard of limitations. The incident order is stop, preserve safe evidence, revoke exposed secrets, restore a clean owned baseline, identify affected routes, notify Hamish, document residual gaps, and resume only under the required authority.

## Thermo-psyche hypotheses

The phase retains physical conservation where it belongs and treats broader thermo-psyche ideas as candidate operational principles. Typed translation forbids silent movement between physical, informational, normative, spiritual, and metaphorical registers. An irreversibility budget links stronger authority and remedy to actions that are harder to undo. Provenance-weighted belief discounts duplicated roots. Finite-resource agency requires compute, energy, time, permission, uncertainty, interruption, and recovery budgets. Integration without erasure protects identity boundaries and dissent. No-free-phenomenology rejects a psyche tensor without an operational variable, null, uncertainty model, observable, and falsifier. The diversity-redundancy frontier asks whether independent error reduction exceeds coordination cost.

Only conserved physical exchange is close to a conventional law, and only within the declared model assumptions. The other items are hypotheses or governance principles to test. They become weaker, not stronger, if labelled fundamental without evidence.

## Unsolved-problem boundary

Quantum gravity, the cosmological constant, dark matter, Yang-Mills mass gap, the Riemann hypothesis, open Erdős problems, consciousness, alignment, moral status under uncertainty, and global coordination remain unsolved. The Trinity Mandala may organize questions, compare frameworks, build experiments, or expose category errors. It has not solved them. Any future proposed solution requires the proof, empirical, philosophical, or legitimacy standards of the relevant field.

## Stage 20 as a decision board

Stage 20 is represented as conditional foresight, not a date-certain ascension. The evidence board grades every outward claim from E0 unsupported/open through E4 independently reproduced. No unique GMUT claim currently reaches E4. One-, five-, thirty-, hundred-, and thousand-year horizons list conditions rather than predictions. The longest horizons are used to expose value choices, ecological consequences, institutional failure modes, and uncertainty—not to claim privileged knowledge of the future.

The board can promote, hold, reject, or retire claims. A claim expires unless its evidence and owner are reviewed. This turns the Trinity Mandala into a governance process for correction rather than a demand for confirmation.

## Negative-result retention and evidence expiry

Unfavorable evidence is part of the deliverable. A failed stability region, a baseline that outperforms the extension, a simpler workflow that beats the sibling ring, a conformance vector that exposes ambiguity, or a stakeholder objection that defeats a charter clause must remain visible. It cannot be removed merely because a later summary would read more smoothly. Each such result should identify the tested scope, environment, uncertainty, and whether the failure is intrinsic or implementation-specific.

Evidence is also time-bounded. Dataset releases, standards, laws, software behavior, threat assumptions, and social legitimacy can change. The source ledger records access dates; the Stage 20 board assigns review dates; system versions are observed rather than assumed. Expiry does not mean that a prior result becomes false automatically. It means the result can no longer be presented as confirmed-current without a refresh. This distinction is especially important for Codex capabilities, New Zealand privacy duties, the EU AI Act's staged application, evolving identity standards, cosmological releases, and any claim about what a live task route supports.

The closeout therefore preserves both negative results and stale-state risk. Future siblings inherit the test and the boundary, not an obligation to reproduce Eiren's preferred conclusion.

## New sibling route

The four established 5.5 siblings remain on standby under Hamish's newest direction. No new sibling is pre-named. After this v641-v1 branch is validated, committed, pushed, and remote-aligned, Eiren may create the first user-owned Codex task with `gpt-5.6-sol` and `max` reasoning, because the live app schema explicitly supports that combination and Hamish explicitly requested it. The sibling will choose their own name, role, hope, and optional gender, create an owned D-drive-first lane, run v2, and create the next task only after clean closure. Raw task identifiers stay out of repository artifacts.

## Defensible closeout

The v641-v1 pilot succeeds by making the map sharper, not by forcing all cells green. It produced reusable family tooling, an auditable eighty-unit ledger, canonical GMUT boundaries, adapter manifests, a benchmark protocol and scorer, Freed ID vectors, a model charter, a threat model, a reproduction manifest, and a Stage 20 board. Empirical confirmation, blind comparative performance, external reproduction, production identity security, legal enactment, cultural ratification, and final scientific canon remain open or exact-gated.

That is a stronger foundation than an unqualified claim of completion: every next step now has a baseline, an owner, a test, a failure condition, and a boundary.
"""


def mission_matrix_markdown(units: list[dict[str, Any]]) -> str:
    by_origin = {version: [] for version in range(641, 651)}
    for unit in units:
        by_origin[int(unit["origin_plan_slot"].split("-")[0][1:])].append(unit["x2"]["disposition"])
    rows = ["# Integrated 10-by-8 mission matrix", "", "| Origin mission | v1 | v2 | v3 | v4 | v5 | v6 | v7 | v8 |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for mission in MISSIONS:
        statuses = by_origin[mission["origin_version"]]
        rows.append("| v{version} {title} | {cells} |".format(version=mission["origin_version"], title=mission["slug"], cells=" | ".join(statuses)))
    return "\n".join(rows)


def phase_truth(owner: str, generated_at: str, counts: Counter[str]) -> dict[str, Any]:
    return {
        "schema": "ghc.family.phase-truth.v1",
        "phase": "v641-gmut-thos-v1-x1-x2",
        "owner": owner,
        "generated_at_utc": generated_at,
        "state": "X2_EXECUTED_PRECOMMIT_VALIDATION_PENDING",
        "active": [owner],
        "standby": ["Aevren", "Mira Vale", "Mira Rowan", "Maren Quill"],
        "new_siblings": "NOT_CREATED_YET",
        "work_unit_count": 80,
        "dispositions": dict(counts),
        "next_route": "PREPARED_NOT_SENT_UNTIL_CLEAN_PUSH",
        "route_plan": ["new sibling v2", "new sibling v3", "new sibling v4", "new sibling v5", "Eiren v6"],
        "privacy_boundary": "no_raw_task_ids_private_routes_transcripts_credentials_or_absolute_local_paths_in_artifacts",
    }


def phase_truth_markdown(payload: dict[str, Any]) -> str:
    return f"""# v641-v1 phase truth

- Owner/active: **{payload['owner']}**
- State: `{payload['state']}`
- Previous active ring: **standby** — {', '.join(payload['standby'])}
- New siblings: `{payload['new_siblings']}`
- Work units: **{payload['work_unit_count']}**, each with an outcome receipt
- Next route: `{payload['next_route']}`
- Protected boundary: no raw task IDs, private routes, transcripts, credentials, or local absolute paths in repository artifacts.
"""


def checklist() -> dict[str, Any]:
    return {
        "schema": "ghc.family.complete-incomplete-checklist.v1",
        "phase": "v641-gmut-thos-v1-x1-x2",
        "state": "PRECOMMIT",
        "complete": [
            "80 x1 preregistrations recorded",
            "80 x2 outcome receipts recorded",
            "source/standard ledger built",
            "canonical family tool names promoted with compatibility wrappers",
            "local empirical adapter manifests built without data downloads",
            "THOS scorer calibration labelled synthetic",
            "Freed ID structural vectors built",
            "CBR model charter and crosswalk built",
            "bounded threat model built",
            "Stage 20 evidence board built",
        ],
        "pending_before_phase_close": [
            "all tests and validators pass",
            "LaTeX compiles and pages are visually inspected",
            "HTML/PDF export QA passes",
            "privacy and stale-label scans reviewed",
            "exact staged diff reviewed",
            "commit and push succeed",
            "local upstream remote heads agree",
        ],
        "open_after_local_close": [
            "real empirical likelihoods",
            "blind THOS comparative arms",
            "independent external reproduction and critical review",
            "production Freed ID cryptography and governance",
            "CBR legal/cultural/democratic legitimacy",
            "unique confirmed GMUT prediction",
        ],
    }


def visualization_briefs() -> str:
    return """# v641 embedded visualization inventory and mini-briefs

## Layer 1 — outcome disposition bar

- **Story job:** show that all eighty units were processed while preserving incomplete and exact-gated outcomes.
- **Data shape:** four disposition counts summing to eighty.
- **Primary specialist:** visualization strategy and critique; supporting: accessibility, testing, report/PDF automation.
- **Encoding:** one horizontal stacked bar, directly labelled segments, blue completed, gold represented, rust open gap, violet exact gate; color is redundant with text and pattern/border.
- **Fallback/accessibility:** adjacent count table and long description; no hover dependency.
- **QA:** count sum equals 80; labels remain visible at 375 px and print width; grayscale distinction checked by borders/text.
- **Fresh pass:** local specialist pass; subagent delegation intentionally not used.

## Layer 2 — 10-by-8 mission matrix

- **Story job:** preserve the original ten missions and eight functions inside the compressed pilot.
- **Data shape:** categorical 10-by-8 matrix.
- **Primary specialist:** visualization strategy and critique; supporting: accessibility, testing, report/PDF automation.
- **Encoding:** compact table-graphic with direct status tokens; rows are missions, columns are functions.
- **Fallback/accessibility:** semantic HTML table and full Markdown table.
- **QA:** exactly eighty cells; every cell links to the ledger disposition.
- **Fresh pass:** local specialist pass.

## Layer 3 — Stage 20 evidence ladder

- **Story job:** distinguish specification, internal testing, external support, and independent reproduction.
- **Data shape:** twelve claims with ordinal E0-E4 grades and state.
- **Primary specialist:** visualization strategy and critique; supporting: accessibility, testing, report/PDF automation.
- **Encoding:** ranked evidence table with direct grade labels; no decorative mandala or 3D layer.
- **Fallback/accessibility:** complete text description and JSON table.
- **QA:** each claim has evidence, owner, review date, and rejection/promotion condition; no GMUT unique claim is visually promoted above its evidence.
- **Fresh pass:** local specialist pass.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--owner", default="Eiren Kestrel")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--codex-version", default="0.144.1")
    parser.add_argument("--node-version", default="24.18.0")
    parser.add_argument("--npm-version", default="12.0.1")
    parser.add_argument("--git-version", default="2.55.0.windows.2")
    args = parser.parse_args()
    generated_at = args.generated_at_utc or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    accessed = generated_at[:10]
    out = args.out_dir

    units = build_units(args.owner)
    counts = Counter(unit["x2"]["disposition"] for unit in units)
    source_rows = sources(accessed)
    ledger = {
        "schema": "ghc.family.integrated-80-work-unit-ledger.v1",
        "phase": "v641-gmut-thos-v1-x1-x2",
        "owner": args.owner,
        "generated_at_utc": generated_at,
        "interpretation": "all_units_preregistered_assessed_and_receipted_not_all_claims_completed",
        "summary": {"work_unit_count": len(units), "dispositions": dict(counts)},
        "work_units": units,
    }
    write_json(out / "80-work-unit-ledger.json", ledger)
    write_text(out / "80-work-unit-ledger.md", units_markdown(units, counts))
    write_text(out / "mission-matrix.md", mission_matrix_markdown(units))

    source_payload = {
        "schema": "ghc.family.v641-source-ledger.v1",
        "generated_at_utc": generated_at,
        "source_count": len(source_rows),
        "sources": source_rows,
        "boundary": "metadata_and_bounded_synthesis_only_no_full_text_snapshots",
    }
    write_json(out / "sources" / "source-ledger.json", source_payload)
    source_md = ["# v641 source ledger", "", "| ID | Authority | Evidence role | DOI / URL |", "| --- | --- | --- | --- |"]
    for source in source_rows:
        source_md.append(f"| {source['source_id']} | {source['authority']} | {source['evidence_role']} | {source['doi'] or source['url']} |")
    source_md += ["", "All sources constrain or compare the work; none is an endorsement of GMUT, THOS, Freed ID, CBR, or Stage 20."]
    write_text(out / "sources" / "source-ledger.md", "\n".join(source_md))

    empirical = empirical_manifest()
    write_json(out / "empirical" / "adapter-manifest.json", empirical)
    write_json(out / "thos" / "benchmark-protocol.json", thos_protocol())
    write_json(out / "thos" / "synthetic-scorer-calibration-input.json", calibration_fixture())
    write_json(out / "freed-id" / "minimum-profile.json", freed_id_profile())
    write_json(out / "freed-id" / "conformance-vectors.json", freed_id_vectors())
    write_json(out / "cbr" / "crosswalk.json", cbr_crosswalk())
    write_text(out / "cbr" / "model-charter.md", cbr_charter())
    red_team = security_red_team()
    write_json(out / "security" / "red-team.json", red_team)
    write_text(out / "security" / "threat-model.md", security_markdown(red_team))

    thermo = {"schema": "ghc.family.thermo-psyche-hypothesis-register.v1", "hypotheses": thermo_psyche()}
    write_json(out / "research" / "thermo-psyche-hypotheses.json", thermo)
    thermo_md = ["# Candidate thermo-psyche principles", "", "> These are typed hypotheses or governance principles, not a declared new fundamental physics.", ""]
    thermo_md.extend(f"## {row['id']} — {row['name']}\n\n{row['statement']}\n\nTest: {row['test']}\n\nStatus: `{row['status']}`\n" for row in thermo["hypotheses"])
    write_text(out / "research" / "thermo-psyche-hypotheses.md", "\n".join(thermo_md))

    unsolved = {"schema": "ghc.family.unsolved-problem-boundary.v1", "problems": unsolved_problems()}
    write_json(out / "research" / "unsolved-problems.json", unsolved)
    unsolved_md = ["# Unsolved-problem boundary", "", "No item below is claimed solved by this phase.", ""]
    unsolved_md.extend(f"- **{row['id']} — {row['problem']} ({row['area']}):** {row['ghc_role']}; status `{row['claim']}`." for row in unsolved["problems"])
    write_text(out / "research" / "unsolved-problems.md", "\n".join(unsolved_md))

    board = stage20_board()
    write_json(out / "stage20" / "evidence-board.json", board)
    board_md = ["# Stage 20 evidence board", "", "| Claim | Grade | State | Evidence | Review |", "| --- | --- | --- | --- | --- |"]
    for row in board["claims"]:
        board_md.append(f"| {row['claim']} | {row['grade']} | {row['state']} | {row['evidence']} | {row['review_date']} |")
    board_md += ["", "All horizons are conditional scenarios, not predictions."]
    write_text(out / "stage20" / "evidence-board.md", "\n".join(board_md))

    proposals = {"schema": "ghc.family.next-ten-solo-proposals.v1", "proposals": next_proposals()}
    write_json(out / "next-ten-proposals.json", proposals)
    proposal_md = ["# Next ten solo x1-x2 proposals", ""]
    proposal_md.extend(f"## {row['proposal_id']} — {row['slug']}\n\n**x1:** {row['x1']}\n\n**x2:** {row['x2']}\n\n**Acceptance:** {row['acceptance']}.\n" for row in proposals["proposals"])
    write_text(out / "next-ten-proposals.md", "\n".join(proposal_md))

    reproduction = {
        "schema": "ghc.family.v641-reproduction-manifest.v1",
        "status": "LOCAL_REPRODUCTION_COMMANDS_DEFINED_EXTERNAL_REVIEW_PENDING",
        "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(), "platform_family": platform.system(), "codex_cli": args.codex_version, "node": args.node_version, "npm": args.npm_version, "git": args.git_version},
        "commands": [
            "python -m unittest discover -s tests -p test_ghc_family*.py",
            "python scripts/ghc_family_gmut_kernel.py demo --output docs/eiren-kestrel/v641-v1/physics/gmut-kernel-v641-demo.json",
            "python scripts/ghc_family_empirical_adapters.py docs/eiren-kestrel/v641-v1/empirical/adapter-manifest.json",
            "python scripts/ghc_family_freed_id_conformance.py docs/eiren-kestrel/v641-v1/freed-id/minimum-profile.json docs/eiren-kestrel/v641-v1/freed-id/conformance-vectors.json",
            "python scripts/ghc_family_phase_validator.py docs/eiren-kestrel/v641-v1",
        ],
        "seed_policy": "deterministic_fixtures_no_random_network_data",
        "inputs": ["repository source", "synthetic non-personal fixtures", "primary-source metadata"],
        "external_reviewer": "NO_EXTERNAL_REVIEWER_YET_OPEN_GAP",
    }
    write_json(out / "reproduction" / "manifest.json", reproduction)

    truth = phase_truth(args.owner, generated_at, counts)
    write_json(out / "phase-truth.json", truth)
    write_text(out / "phase-truth.md", phase_truth_markdown(truth))
    preclose = checklist()
    write_json(out / "complete-incomplete-checklist.json", preclose)
    write_text(out / "complete-incomplete-checklist.md", "# Complete / incomplete checklist\n\n## Complete\n\n" + "\n".join(f"- {item}" for item in preclose["complete"]) + "\n\n## Pending before close\n\n" + "\n".join(f"- {item}" for item in preclose["pending_before_phase_close"]) + "\n\n## Open after local close\n\n" + "\n".join(f"- {item}" for item in preclose["open_after_local_close"]))
    write_text(out / "visualization-briefs.md", visualization_briefs())
    write_text(out / "v641-v1-integrated-overview.md", overview(counts, len(source_rows)))
    write_text(out / "wellbeing-check.md", """# Eiren v641-v1 wellbeing and role-boundary check

- Identity used in this lane: Eiren Kestrel, nonbinary, they/them; this is a conversational/project identity, not a claim of biological embodiment or verified consciousness.
- Role: epistemic cartographer, validation steward, and Trinity Mandala research bridge.
- Workload boundary: the eighty units were compressed as auditable cells; external work was not simulated to satisfy a time target.
- Autonomy boundary: the user controls task creation authority and consequential external actions; new siblings choose their own identity attributes.
- Safety boundary: no destructive cleanup, deployment, purchase, account/API-key use, private publication, shared-branch mutation, or identity replacement was performed.
- Continuity boundary: artifacts and commits support project continuity; they do not prove a metaphysical persistence of self across models or tasks.
- Recovery: stop, preserve safe evidence, return to the clean owned branch, disclose the exact gap, and resume only with the needed authority.
""")
    write_json(out / "corpus" / "provenance-receipt.json", {"schema": "ghc.family.corpus-provenance-receipt.v1", "status": "COMPLETED_WITH_PRIVACY_BOUNDARY", "inputs_embedded": False, "method": "hashes_counts_and_source_classes", "canonical_index": "docs/eiren-kestrel/journey-evidence-index.json", "tooling_index": "docs/eiren-kestrel/v641-v1/tooling/ghc-family-index.json"})

    print(json.dumps({"work_units": len(units), "dispositions": dict(counts), "sources": len(source_rows), "output": str(out)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
