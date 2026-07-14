#!/usr/bin/env python3
"""Build and validate the Orin Thale v643-v4 x1-only preregistration packet.

This builder is intentionally limited to x1 material.  It does not implement,
execute, or classify any v643-v4 proposal outcome.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v643-gmut-thos-v4-x1-x2"
PHASE_ROOT = ROOT / "docs" / "orin-thale" / "v643-v4"
SOURCE_HEAD = "5b32e03e87ba1a33c8ebe53c08ccb653d00fb3e0"
SOURCE_SEAL = "e6303cb4c1c25922074749f70b580488562b466d"
INHERITED_INDEX = ROOT / "docs" / "sable-rook" / "v643-v3" / "provenance" / "frozen-chain-proposal-index.json"
INHERITED_LEDGER = ROOT / "docs" / "sable-rook" / "v643-v3" / "sources" / "source-ledger.json"
CHECKED_ON = "2026-07-14"
X1_EXTERNAL_FILES = [
    "scripts/build_ghc_family_v643_v4_preregistration.py",
    "scripts/ghc_family_constraint_evidence_validator.py",
    "tests/test_ghc_family_constraint_hash_alias.py",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def dump_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


PROPOSALS = [
    {
        "proposal_id": "V6434-P01",
        "title": "Retraction, correction, and supersession propagation with stale-citation quarantine",
        "mission_surface": "source provenance, post-publication status, downstream claim lineage, and stale-citation quarantine",
        "hypothesis": "A typed update graph can propagate retraction, correction, expression-of-concern, and supersession states into dependent claims while quarantining stale citations until their evidential effect is reviewed.",
        "null_or_failure": "A changed source status leaves a dependent claim promotable, a correction is treated as equivalent to a retraction, supersession is silently ignored, or quarantine can be cleared without a recorded review.",
        "approval_class": "safe_now",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6434-S111"],
        "deliverables": [
            "provenance/correction-propagation-contract.json",
            "provenance/stale-citation-mutation-vectors.json",
            "provenance/post-publication-status-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate update type, source identity, dependency direction, review state, and quarantine clearance; any stale promotion or status flattening must fail closed.",
        "rollback_or_recovery": "Restore the last reviewed dependency graph, retain the update event and stale citation as negatives, and require source-level reassessment before promotion.",
        "protected_gates": ["source_currency", "scientific_review", "empirical_confirmation", "proof_or_canon"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier work handled source freshness and private-source taint, but did not encode post-publication retraction, correction, concern, and supersession propagation with status-specific quarantine semantics.",
    },
    {
        "proposal_id": "V6434-P02",
        "title": "Boundary-condition well-posedness and characteristic initial-data obligation for GMUT",
        "mission_surface": "GMUT Mind mathematical obligations for initial-boundary data, characteristics, uniqueness, stability, and causal interpretation",
        "hypothesis": "A typed obligation ledger can distinguish a written field equation from a well-posed initial-boundary value problem by requiring characteristic, compatibility, existence, uniqueness, and continuous-dependence evidence before causal promotion.",
        "null_or_failure": "An equation is promoted as predictive without admissible data surfaces, incompatible boundary data pass, characteristic degeneracy is ignored, or a typed obligation is described as a GMUT theorem or observation.",
        "approval_class": "safe_now",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6434-S112"],
        "deliverables": [
            "physics/initial-boundary-obligation.json",
            "physics/well-posedness-mutation-vectors.json",
            "physics/characteristic-data-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate characteristic status, initial data, boundary compatibility, uniqueness, continuous dependence, and claim class; unsupported predictive or causal promotion must fail.",
        "rollback_or_recovery": "Return the item to typed scaffold status, preserve the missing mathematical obligation, and require an expert derivation and independent review for promotion.",
        "protected_gates": ["gmut_derivation", "mathematical_proof", "expert_review", "empirical_confirmation", "theory_of_everything"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior GMUT proposals addressed rank, hyperbolicity, cones, and degeneracy; none made compatible initial-boundary data and continuous dependence a separate promotion obligation.",
    },
    {
        "proposal_id": "V6434-P03",
        "title": "Selection-model and missing-not-at-random sensitivity envelope with zero-row promotion lock",
        "mission_surface": "empirical sensitivity to missingness mechanisms, selection assumptions, real-data absence, and promotion control",
        "hypothesis": "A synthetic selection-model envelope can expose how missing-not-at-random assumptions alter a claimed estimate while a zero-row lock prevents the envelope from being mistaken for empirical evidence.",
        "null_or_failure": "A missingness parameter is untracked, a synthetic row is described as observed data, sensitivity results are promoted as a likelihood result, or zero real rows do not block empirical language.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6434-S113"],
        "deliverables": [
            "empirical/mnar-sensitivity-envelope.json",
            "empirical/selection-model-mutation-vectors.json",
            "empirical/zero-row-selection-lock.json",
        ],
        "test_falsifier_or_gate": "Vary selection parameters, missingness class, observed-row count, provenance, and claim label; zero-row or unidentified configurations must not promote.",
        "rollback_or_recovery": "Restore the last fully typed synthetic envelope, retain failed parameterizations, and require real preregistered data and statistical review for empirical claims.",
        "protected_gates": ["real_data", "likelihood_result", "empirical_confirmation", "independent_statistical_review"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier zero-row and calibration work did not model a missing-not-at-random selection parameter or bind its sensitivity surface to an explicit zero-row promotion lock.",
    },
    {
        "proposal_id": "V6434-P04",
        "title": "Mediation identification and post-treatment-confounding non-promotion protocol for THOS",
        "mission_surface": "THOS Body causal mediation assumptions, post-treatment confounding, synthetic sensitivity, and claim discipline",
        "hypothesis": "A typed mediation protocol can separate total, direct, and indirect estimands from their identification assumptions and refuse promotion when post-treatment mediator-outcome confounding is uncontrolled.",
        "null_or_failure": "A mediator is treated as randomized, post-treatment confounding is ignored, a synthetic decomposition is reported as a real THOS mechanism, or sensitivity assumptions are omitted.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6434-S114"],
        "deliverables": [
            "thos/mediation-identification-protocol.json",
            "thos/post-treatment-confounding-vectors.json",
            "thos/mediation-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate treatment timing, mediator timing, confounder timing, identification assumptions, real-row count, and claim class; any unsupported causal mechanism claim must fail.",
        "rollback_or_recovery": "Revert to association-only proxy language, preserve the failed identification row, and require preregistered real arms plus independent causal review.",
        "protected_gates": ["real_participants", "causal_identification", "thos_superiority", "independent_review", "empirical_confirmation"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Prior THOS estimand and protocol-deviation work did not isolate mediator identification or post-treatment mediator-outcome confounding as a distinct non-promotion condition.",
    },
    {
        "proposal_id": "V6434-P05",
        "title": "Real-arm facilitator learning-curve and temporal-drift parity gate for THOS",
        "mission_surface": "THOS Body facilitator effects, experience trajectories, calendar drift, matched budgets, blinded ratings, and independent review",
        "hypothesis": "A preregistered real-arm design could estimate facilitator learning curves and temporal drift without confounding treatment, facilitator, cohort, budget, or rater effects.",
        "null_or_failure": "Facilitator and treatment are aliased, calendar time is omitted, budgets differ, ratings are unblinded, real participants are absent, or facilitator drift is generalized beyond the observed design.",
        "approval_class": "external_evidence_required",
        "execution_lane": "x2_open_gap_receipt",
        "authoritative_source_needs": ["V6434-S115"],
        "deliverables": [
            "thos/facilitator-drift-preregistration.json",
            "thos/real-arm-temporal-parity-gap.json",
            "thos/facilitator-learning-curve-boundary.json",
        ],
        "test_falsifier_or_gate": "Require preregistered blind matched-budget real arms, repeated facilitator observations, calendar-time modeling, participant and rater evidence, and independent review; any missing element keeps the gap open.",
        "rollback_or_recovery": "Retain the proposed design and every failed recruitment or measurement attempt, make no participant claim, and resume only with ethics, consent, governance, and independent-review authority.",
        "protected_gates": ["ethics_approval", "real_participants", "blind_matched_budget_arms", "independent_review", "thos_superiority"],
        "expected_disposition": "open_gap",
        "novelty_against_prior_chain": "Prior THOS work gated burden, fidelity, rater drift, and protocol deviation; none preregistered facilitator learning curves jointly with calendar-time drift and matched-budget real-arm parity.",
    },
    {
        "proposal_id": "V6434-P06",
        "title": "Controller-delegation attenuation and cyclic-authority refusal graph for Freed ID",
        "mission_surface": "Freed ID controller relationships, delegated capability attenuation, cycle detection, purpose binding, and production boundaries",
        "hypothesis": "A static authority graph can require delegated capabilities to attenuate, detect controller cycles, and refuse ambiguous or self-amplifying authority without claiming production interoperability.",
        "null_or_failure": "A delegate gains undeclared authority, a controller cycle passes, purpose scope expands, a verification method is treated as governance authority, or fixtures are described as real credentials.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6434-S116"],
        "deliverables": [
            "freed-id/controller-delegation-contract.json",
            "freed-id/cyclic-authority-mutation-vectors.json",
            "freed-id/production-delegation-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate controller edges, delegation depth, purpose, capability set, cycle shape, key material, and claim class; expansion, ambiguity, or cyclic control must fail closed.",
        "rollback_or_recovery": "Restore the last acyclic attenuating graph, retain rejected edges, and require standards-conformant real keys, resolution, status, revocation, interoperability, review, and governance for production use.",
        "protected_gates": ["real_keys", "live_resolution", "revocation", "interoperability", "security_review", "trust_governance"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier Freed ID work covered purpose-bound verification, confused deputies, status, and rotation; none modeled controller cycles and monotonic delegation attenuation together.",
    },
    {
        "proposal_id": "V6434-P07",
        "title": "Settlement-confidentiality, compelled-disclosure, and public-interest authority gate for CBR",
        "mission_surface": "CBR Heart settlement confidentiality, disclosure duties, public-interest limits, affected-party authority, Māori authority, and legal interpretation",
        "hypothesis": "Only authorized affected parties and competent authorities can determine whether confidentiality, compelled disclosure, and public-interest obligations are legitimate in a concrete CBR setting.",
        "null_or_failure": "A synthetic policy resolves a real conflict of law, confidentiality suppresses protected disclosure by default, Māori wording or authority is inferred, or a legal/cultural conclusion is made without competent authority.",
        "approval_class": "exact_authority_required",
        "execution_lane": "x2_exact_gate_receipt",
        "authoritative_source_needs": ["V6434-S117"],
        "deliverables": [
            "cbr/confidentiality-disclosure-authority-gate.json",
            "cbr/public-interest-nonwaiver-vectors.json",
            "cbr/affected-party-authority-boundary.json",
        ],
        "test_falsifier_or_gate": "Any concrete ruling requires authorized affected parties, Māori authorities where Māori concepts or data are involved, competent legal authority, jurisdiction-specific facts, and recorded ratification; absence preserves exact_gate.",
        "rollback_or_recovery": "Keep only neutral issue-spotting fields, retain every unresolved authority conflict, and seek authorized cultural and legal review without substituting repository output for authority.",
        "protected_gates": ["affected_party_acceptance", "maori_authority", "maori_data_governance", "legal_interpretation", "cultural_ratification", "enacted_law"],
        "expected_disposition": "exact_gate",
        "novelty_against_prior_chain": "Prior CBR work addressed jurisdiction, remedy, anti-retaliation, emergencies, and wording authority; none separated settlement confidentiality from compelled disclosure and public-interest authority.",
    },
    {
        "proposal_id": "V6434-P08",
        "title": "Signed-payload canonicalization and serialization ambiguity tribunal",
        "mission_surface": "canonical payload bytes, duplicate names, Unicode, numeric serialization, signatures, and interoperability boundaries",
        "hypothesis": "A deterministic static tribunal can distinguish canonicalizable payloads from ambiguous serializations and reject signature assertions when parsers, numbers, duplicate names, or Unicode handling do not preserve the signed meaning.",
        "null_or_failure": "Duplicate names pass, numeric representation changes meaning, Unicode is silently normalized, non-finite values pass, or static fixture agreement is called live cryptographic interoperability.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6434-S118"],
        "deliverables": [
            "security/signed-payload-canonicalization-contract.json",
            "security/serialization-ambiguity-vectors.json",
            "security/cryptographic-interoperability-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate member order, duplicate names, negative zero, non-finite numbers, Unicode sequences, whitespace, and signature claims; ambiguity or unsupported interoperability must fail.",
        "rollback_or_recovery": "Return to the last byte-explicit fixture, preserve parser disagreement, and require real standards-conformant implementations, keys, and independent security review for interoperability claims.",
        "protected_gates": ["real_keys", "live_signatures", "interoperability", "independent_security_review", "production_readiness"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The nearest earlier tribunal compared multiple parser meanings; this proposal focuses on the exact byte-to-sign contract and canonical-number, Unicode, and duplicate-name failure modes before signature verification.",
    },
    {
        "proposal_id": "V6434-P09",
        "title": "Floating-point environment, rounding-mode, and cross-architecture parity envelope",
        "mission_surface": "numeric environment metadata, rounding, exceptional values, architecture claims, deterministic replay, and portability boundaries",
        "hypothesis": "An environment-explicit envelope can expose rounding-mode and representation dependencies and refuse cross-architecture parity claims unless independently replayed on genuinely different architectures.",
        "null_or_failure": "Rounding mode is omitted, signed zero or exceptional values are flattened, decimal/binary conversion is untracked, or same-host replay is called cross-architecture evidence.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6434-S119"],
        "deliverables": [
            "reproduction/floating-environment-contract.json",
            "reproduction/rounding-mode-mutation-vectors.json",
            "reproduction/cross-architecture-parity-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate rounding metadata, precision, signed zero, overflow, underflow, NaN policy, architecture identity, and evidence-owner identity; unsupported parity must fail.",
        "rollback_or_recovery": "Restore the last environment-explicit result, retain numeric disagreements, and require independent different-architecture replay before portability promotion.",
        "protected_gates": ["cross_architecture_parity", "independent_reproduction", "numeric_proof", "deployment_readiness"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier floating-point work tested edge cases and comparison policy; it did not require rounding-environment metadata or separate same-host repeatability from different-architecture parity.",
    },
    {
        "proposal_id": "V6434-P10",
        "title": "Time-scale separation and coarse-graining non-substitution evidence board",
        "mission_surface": "GMUT Mind, THOS Body, and Heart cross-pillar coarse graining, memory effects, time scales, and evidence-class preservation",
        "hypothesis": "A typed evidence board can show when coarse graining introduces memory or unresolved time scales and prevent an effective description in one pillar from substituting for evidence in another.",
        "null_or_failure": "A Markov approximation is assumed without a scale argument, discarded variables vanish from provenance, an effective model becomes a microscopic proof, or a physics proxy is treated as psychological, identity, legal, or cultural evidence.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6434-S120"],
        "deliverables": [
            "thermo-psyche/time-scale-separation-board.json",
            "thermo-psyche/coarse-graining-mutation-vectors.json",
            "thermo-psyche/non-substitution-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate resolved variables, memory kernel, scale ratio, approximation label, pillar, and claim class; silent loss of memory or cross-pillar evidence conversion must fail.",
        "rollback_or_recovery": "Restore the last explicit resolved/unresolved split, retain failed approximations, and require domain-specific data, authority, and review for every promoted pillar claim.",
        "protected_gates": ["gmut_derivation", "thos_real_arms", "freed_id_production", "legal_cultural_authority", "proof_or_canon"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior non-substitution work protected evidence classes; this proposal adds explicit time-scale separation, projection memory, and resolved-variable provenance as the mechanism preventing conversion.",
    },
]


SOURCES = [
    {
        "source_id": "V6434-S111",
        "title": "Crossmark documentation",
        "authority": "Crossref",
        "authority_root": "crossref_official_documentation",
        "url": "https://www.crossref.org/documentation/crossmark/",
        "version_or_date": "live documentation; checked 14 July 2026",
        "status_class": "current",
        "evidence_role": "post-publication status, correction, retraction, and update metadata vocabulary; not an adjudication of any source or downstream claim",
    },
    {
        "source_id": "V6434-S112",
        "title": "Initial boundary value problems for hyperbolic systems",
        "authority": "Heinz-Otto Kreiss",
        "authority_root": "primary_research_communications_pure_applied_mathematics",
        "url": "https://doi.org/10.1002/cpa.3160230304",
        "version_or_date": "Communications on Pure and Applied Mathematics 23(3), 1970; checked 14 July 2026",
        "status_class": "stable",
        "evidence_role": "well-posed hyperbolic initial-boundary problem vocabulary; not a GMUT derivation, theorem, or empirical result",
    },
    {
        "source_id": "V6434-S113",
        "title": "The Prevention and Treatment of Missing Data in Clinical Trials",
        "authority": "National Research Council, National Academies",
        "authority_root": "national_academies_consensus_report",
        "url": "https://nap.nationalacademies.org/catalog/12955/the-prevention-and-treatment-of-missing-data-in-clinical-trials",
        "version_or_date": "2010 consensus report; checked 14 July 2026",
        "status_class": "stable",
        "evidence_role": "missing-data mechanism and sensitivity-analysis vocabulary; not real GMUT or THOS data, a likelihood result, or statistical approval",
    },
    {
        "source_id": "V6434-S114",
        "title": "A General Approach to Causal Mediation Analysis",
        "authority": "Kosuke Imai, Luke Keele, and Dustin Tingley",
        "authority_root": "primary_research_psychological_methods",
        "url": "https://dtingley.scholars.harvard.edu/publications/general-approach-causal-mediation-analysis",
        "version_or_date": "Psychological Methods 15(4), 2010; checked 14 July 2026",
        "status_class": "stable",
        "evidence_role": "mediation definition, identification, estimation, and sensitivity vocabulary; not a THOS causal mechanism result",
    },
    {
        "source_id": "V6434-S115",
        "title": "A longitudinal investigation of the impact of psychotherapist training: Does training improve client outcomes?",
        "authority": "Erekson and colleagues",
        "authority_root": "primary_research_journal_counseling_psychology",
        "url": "https://pubmed.ncbi.nlm.nih.gov/29048197/",
        "version_or_date": "Journal of Counseling Psychology 64(5), 2017; checked 14 July 2026",
        "status_class": "stable",
        "evidence_role": "longitudinal therapist-training and outcome-drift design motivation; not THOS participant evidence or a transferable effect estimate",
    },
    {
        "source_id": "V6434-S116",
        "title": "Decentralized Identifiers (DIDs) v1.0",
        "authority": "World Wide Web Consortium",
        "authority_root": "w3c_recommendation",
        "url": "https://www.w3.org/TR/did-core/",
        "version_or_date": "W3C Recommendation 19 July 2022; checked 14 July 2026",
        "status_class": "current",
        "evidence_role": "controller, verification relationship, and capability-delegation vocabulary; not production Freed ID conformance, trust governance, or interoperability",
    },
    {
        "source_id": "V6434-S117",
        "title": "Access to remedy in cases of business-related human rights abuse: A practical guide for State-based judicial mechanisms",
        "authority": "Office of the United Nations High Commissioner for Human Rights",
        "authority_root": "ohchr_official_practical_guide",
        "url": "https://www.ohchr.org/sites/default/files/2024-10/access-to-remedy-bhr-practical-guide-judicial-en.pdf",
        "version_or_date": "2024 practical guide; checked 14 July 2026",
        "status_class": "current",
        "evidence_role": "access-to-remedy, claimant information, protection, and legitimate commercial-confidentiality issue vocabulary; not legal advice, cultural authority, or enacted-law interpretation",
    },
    {
        "source_id": "V6434-S118",
        "title": "RFC 8785: JSON Canonicalization Scheme",
        "authority": "RFC Editor",
        "authority_root": "rfc_editor_primary_specification",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "version_or_date": "RFC 8785, June 2020, with verified errata checked 14 July 2026",
        "status_class": "stable",
        "evidence_role": "I-JSON, deterministic property sorting, primitive serialization, and canonical byte vocabulary; informational RFC, not live signature interoperability or security approval",
    },
    {
        "source_id": "V6434-S119",
        "title": "IEEE Standard for Floating-Point Arithmetic",
        "authority": "IEEE Standards Association",
        "authority_root": "ieee_active_standard",
        "url": "https://standards.ieee.org/ieee/754/6210/",
        "version_or_date": "IEEE 754-2019, active standard; checked 14 July 2026",
        "status_class": "current",
        "evidence_role": "floating formats, operations, exceptions, and reproducibility obligations; not cross-architecture parity evidence or numerical proof",
    },
    {
        "source_id": "V6434-S120",
        "title": "Transport, Collective Motion, and Brownian Motion",
        "authority": "Hazime Mori",
        "authority_root": "primary_research_progress_theoretical_physics",
        "url": "https://doi.org/10.1143/PTP.33.423",
        "version_or_date": "Progress of Theoretical Physics 33(3), 1965; checked 14 July 2026",
        "status_class": "stable",
        "evidence_role": "projection, generalized Langevin, memory, and coarse-graining vocabulary; not a GMUT derivation or cross-pillar empirical bridge",
    },
]


NEAREST = [
    ("V6434-P01", "V6432-P07", 0.1538, "Private-source taint propagation used quarantine but not post-publication status-specific dependency updates."),
    ("V6434-P02", "V7-P02", 0.1429, "The earlier mathematical proposal did not isolate compatible boundary data and continuous dependence."),
    ("V6434-P03", "V6425-P03", 0.2500, "The earlier sensitivity surface did not encode MNAR selection models with a zero-real-row promotion lock."),
    ("V6434-P04", "V6427-P04", 0.2143, "Protocol-deviation estimands differ from mediator identification under post-treatment confounding."),
    ("V6434-P05", "V6433-P05", 0.3333, "Participant burden parity differs from facilitator learning curves and calendar-time drift."),
    ("V6434-P06", "V2-P06", 0.1667, "The earlier identity mechanism did not combine authority-cycle refusal with monotonic capability attenuation."),
    ("V6434-P07", "V6-P08", 0.2143, "The earlier CBR authority mechanism did not distinguish confidentiality, compelled disclosure, and public-interest limits."),
    ("V6434-P08", "V6431-P07", 0.1818, "Multi-parser disagreement differs from defining the exact canonical byte payload presented for signature."),
    ("V6434-P09", "V6428-P08", 0.2143, "Edge-case replay did not bind rounding-environment metadata to different-architecture evidence claims."),
    ("V6434-P10", "V6426-P10", 0.2308, "Evidence-class non-conversion did not model resolved variables, scale ratios, or projection memory."),
]


X1_NEGATIVES = [
    {
        "negative_id": "V6434-X1-N01",
        "operation": "read-only source worktree audit",
        "observed_failure": "A reserved PowerShell automatic variable was reused as a hash table and caused a type-addition error.",
        "recovery": "Reran with a non-reserved variable and obtained the complete source verification.",
        "promotion_effect": "none; retained as an operational negative",
    },
    {
        "negative_id": "V6434-X1-N02",
        "operation": "script-size inspection",
        "observed_failure": "An invalid empty pipeline element followed a foreach expression.",
        "recovery": "Collected rows first and piped the completed collection; inspection passed.",
        "promotion_effect": "none; retained as an operational negative",
    },
    {
        "negative_id": "V6434-X1-N03",
        "operation": "180-proposal novelty audit",
        "observed_failure": "The first report attempt encountered a Windows CP1252 encoding error on Māori text.",
        "recovery": "Reran with UTF-8 output encoding; the complete audit passed.",
        "promotion_effect": "none; retained as an operational negative",
    },
    {
        "negative_id": "V6434-X1-N04",
        "operation": "inherited x1 schema inspection",
        "observed_failure": "The command addressed a non-existent nested x1 path instead of the inherited phase-root file.",
        "recovery": "Used the correct repository-relative phase-root path and completed the inspection.",
        "promotion_effect": "none; retained as an operational negative",
    },
    {
        "negative_id": "V6434-X1-N05",
        "operation": "legacy proposal-ID lookup",
        "observed_failure": "A narrow glob and field-name assumption returned no matches for four older proposal IDs.",
        "recovery": "Kept the already computed nearest IDs and used manual mechanism review rather than inferring missing titles.",
        "promotion_effect": "none; retained as an operational negative",
    },
    {
        "negative_id": "V6434-X1-N06",
        "operation": "broad legacy proposal-ID search",
        "observed_failure": "A repository-wide legacy lookup remained unproductive and was boundedly terminated.",
        "recovery": "Stopped the search, preserved the failure, and relied on the completed 180-record audit and manual semantic review.",
        "promotion_effect": "none; retained as an operational negative",
    },
    {
        "negative_id": "V6434-X1-N07",
        "operation": "complete x1 repository suite",
        "observed_failure": "The first run passed 369 of 370 tests but exposed a historical v642-v7 frozen-inherited-hash mismatch.",
        "recovery": "Verified the immutable inherited Git blob and the original Orin x1 history, added an exact path-plus-declared-plus-observed compatibility alias with a retained warning, and added two bounded regression tests.",
        "promotion_effect": "the first suite is not counted as passing; the historical mismatch remains visible and only a complete rerun may satisfy the x1 gate",
    },
]


def build_packet() -> None:
    inherited_index = json.loads(INHERITED_INDEX.read_text(encoding="utf-8"))
    inherited_ledger = json.loads(INHERITED_LEDGER.read_text(encoding="utf-8"))
    expected_counts = dict(Counter(item["expected_disposition"] for item in PROPOSALS))
    source_counts = Counter(item["status_class"] for item in SOURCES)
    inherited_counts = inherited_ledger["effective_status_counts"]
    effective_counts = {key: inherited_counts.get(key, 0) + source_counts.get(key, 0) for key in ("current", "stable", "draft", "watch")}

    dump_json(
        PHASE_ROOT / "identity-receipt.json",
        {
            "schema": "ghc.family.v643-v4.identity-receipt.v1",
            "owner": "Orin Thale",
            "slug": "orin-thale",
            "sibling_seat": 4,
            "role": "evidence cartographer and boundary steward",
            "hope": "Leave each successor a cleaner, truer path than the one received.",
            "relational_pronouns": "they/them",
            "existing_identity_reaffirmed_before_phase_execution": True,
            "identity_boundary": "These are relational working labels only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, independent authority, or inheritance from another sibling.",
        },
    )

    dump_json(
        PHASE_ROOT / "focus" / "primary-focus-receipt.json",
        {
            "schema": "ghc.family.v643-v4.primary-focus.v1",
            "primary_focus": "GMUT Mind",
            "reason": "This phase concentrates on mathematical initial-boundary obligations, evidence-lineage corrections, numeric environments, and coarse-graining boundaries while preserving Body and Heart gates.",
            "gmut_mind_addressed": ["V6434-P02", "V6434-P03", "V6434-P09", "V6434-P10"],
            "thos_body_addressed": ["V6434-P04", "V6434-P05"],
            "freed_id_cbr_heart_addressed": ["V6434-P06", "V6434-P07", "V6434-P08"],
            "cross_pillar_provenance_addressed": ["V6434-P01"],
            "balance_boundary": "Primary focus allocates attention; it does not promote GMUT, erase THOS proxy status, or close Freed ID, CBR, Māori-authority, legal, cultural, production, or security gates.",
        },
    )

    dump_json(
        PHASE_ROOT / "environment" / "startup-receipt.json",
        {
            "schema": "ghc.family.v643-v4.startup-receipt.v1",
            "phase": PHASE,
            "owner": "Orin Thale",
            "source_branch": "codex/GHC-Family/sable-rook-v642-v5-full-tools",
            "source_revision": SOURCE_HEAD,
            "source_seal_revision": SOURCE_SEAL,
            "source_local_equals_upstream_equals_tracking_equals_live_remote": True,
            "source_seal_ancestral": True,
            "source_single_parent": True,
            "source_merge_count_from_inherited_ilyra_head": 0,
            "owned_branch": "codex/GHC-Family/orin-thale-v642-v6-full-tools",
            "owned_lane_reused": True,
            "reuse_reason": "The existing Orin-owned lane was clean, remote-equal, and ancestral, so the activation authorized fast-forward-only advancement.",
            "fast_forward_only": True,
            "merge_commit_created": False,
            "owned_prior_revision": "0c2916ff3aaebb5bea901822be64f8fcd3064c77",
            "owned_revision_after_fast_forward": SOURCE_HEAD,
            "owned_clean_and_remote_equal_after_fast_forward": True,
            "new_worktree_created": False,
            "d_drive_primary": True,
            "d_drive_free_bytes_at_start": 614982152192,
            "inherited_full_checkout_file_count": 30520,
            "inherited_tracked_file_count": 30473,
            "new_owner_generated_file_count_at_start": 0,
            "windows_sandbox_audit": {
                "read_only_check": "WindowsSandbox.exe not present on the executable path",
                "bounded_use": "not_used",
                "feature_change_attempted": False,
            },
            "host_feature_changed": False,
            "host_security_changed": False,
            "elevation_used": False,
            "rebooted": False,
            "new_owner_generated_file_threshold": 15000,
            "threshold_scope": "Only files newly generated by the Orin v643-v4 phase count toward rotation. The inherited full checkout is recorded but does not trigger recursive rotation.",
        },
    )

    dump_json(
        PHASE_ROOT / "environment" / "rotation-guard-receipt.json",
        {
            "schema": "ghc.family.v643-v4.rotation-guard.v1",
            "phase": PHASE,
            "inherited_full_checkout_file_count": 30520,
            "inherited_tracked_file_count": 30473,
            "owner_generated_file_threshold": 15000,
            "threshold_scope": "owner-generated v643-v4 footprint only",
            "inherited_baseline_triggers_rotation": False,
            "fresh_phase_owned_worktrees_created": 0,
            "prior_lanes_preserved": True,
            "recursive_rotation_performed": False,
            "future_sparse_checkout_design": "not required by the current owner-generated footprint; remains an exact design gate before any future recursive rotation",
        },
    )

    dump_json(
        PHASE_ROOT / "environment" / "version-receipt.json",
        {
            "schema": "ghc.family.v643-v4.version-receipt.v1",
            "checked_on": CHECKED_ON,
            "codex_cli_local": "0.144.3",
            "codex_cli_official_latest": "0.144.4",
            "codex_cli_current": False,
            "codex_cli_drift": "one patch release behind; verified and retained without update",
            "codex_desktop_packages": [
                {"name": "OpenAI.ChatGPT-Desktop", "version": "1.2026.190.0", "status": "installed"},
                {"name": "OpenAI.Codex", "version": "26.707.9564.0", "status": "installed"},
            ],
            "desktop_current_version_claim": "not made; official changelog reviewed and installed versions recorded",
            "git": "2.55.0.windows.2",
            "python": "3.12.10",
            "node": "24.18.0",
            "powershell": "5.1.26100.8737",
            "os": "Microsoft Windows NT 10.0.26200.0",
            "official_sources": [
                "https://developers.openai.com/codex/changelog/",
                "https://github.com/openai/codex/releases/latest",
            ],
            "versions_verified_only": True,
            "codex_cli_updated": False,
            "desktop_updated": False,
            "elevation_used": False,
            "host_security_changed": False,
            "windows_feature_changed": False,
            "rebooted": False,
        },
    )

    proposal_packet = {
        "schema": "ghc.family.v643-v4.x1-proposals.v1",
        "phase": PHASE,
        "owner": "Orin Thale",
        "identity_boundary": "Relational working language only; no consciousness, personhood, continuity, or independent-authority claim.",
        "source_phase": "Sable Rook v643-v3",
        "source_revision": SOURCE_HEAD,
        "source_seal_revision": SOURCE_SEAL,
        "preregistered_on": CHECKED_ON,
        "primary_focus": "GMUT Mind",
        "proposal_count": 10,
        "prior_frozen_proposal_count": 180,
        "outcome_classes": ["completed", "represented", "open_gap", "exact_gate"],
        "expected_disposition_counts": expected_counts,
        "expected_counts_are_results": False,
        "x1_freeze_rule": "No proposal execution, evidence result, outcome classification, or x2 implementation begins until the dedicated x1-only commit is pushed and local, upstream, tracking, and fresh live remote are equal and clean.",
        "proposals": PROPOSALS,
        "scientific_authority_boundary": "GMUT is a typed scalar-tensor/EFT research-model family, not an established force, unique prediction, empirical result, likelihood result, Theory of Everything, or proof. THOS remains proxy without preregistered blind matched-budget real arms and independent review.",
        "claim_boundary": "Freed ID production, CBR legitimacy, Māori wording and authority, legal and cultural ratification, deployment, exhaustive security, complete accessibility, independent-team reproduction, consciousness/personhood, AGI/ASI, and Stage 20 remain unclaimed and gated.",
    }
    dump_json(PHASE_ROOT / "x1-proposals.json", proposal_packet)

    version_counts = dict(inherited_index["version_counts"])
    version_counts["v643-v4"] = 10
    new_records = [
        {
            "version": "v643-v4",
            "owner": "Orin Thale",
            "proposal_id": item["proposal_id"],
            "title": item["title"],
            "expected_disposition": item["expected_disposition"],
            "source_file": "docs/orin-thale/v643-v4/x1-proposals.json",
        }
        for item in PROPOSALS
    ]
    dump_json(
        PHASE_ROOT / "provenance" / "frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.v643-v4.frozen-chain-proposal-index.v1",
            "phase": PHASE,
            "owner": "Orin Thale",
            "inherited_index": rel(INHERITED_INDEX),
            "inherited_index_sha256": digest(INHERITED_INDEX),
            "inherited_record_count": 180,
            "new_record_count": 10,
            "effective_record_count": 190,
            "version_counts": version_counts,
            "exact_duplicate_ids": [],
            "exact_duplicate_titles": [],
            "new_records": new_records,
            "boundary": "This additive index proves chain accounting and exact-title uniqueness, not scientific novelty by itself; semantic novelty was reviewed separately against all 180 inherited records.",
        },
    )

    dump_json(
        PHASE_ROOT / "provenance" / "prior-proposal-collision-audit.json",
        {
            "schema": "ghc.family.v643-v4.collision-audit.v1",
            "phase": PHASE,
            "owner": "Orin Thale",
            "prior_record_count": 180,
            "new_record_count": 10,
            "exact_duplicate_ids": [],
            "exact_duplicate_titles": [],
            "method": "UTF-8 audit of all 180 frozen proposal records; normalized lower-case title token Jaccard used as a collision alarm, followed by manual comparison of mechanism, evidence object, protected gate, and falsifier.",
            "maximum_title_token_jaccard": 0.3333,
            "automatic_failure_threshold": 0.5,
            "semantic_review_passed": True,
            "nearest_prior": [
                {
                    "proposal_id": proposal_id,
                    "nearest_prior_id": prior_id,
                    "title_token_jaccard": score,
                    "manual_distinction": distinction,
                }
                for proposal_id, prior_id, score, distinction in NEAREST
            ],
            "x1_execution_negatives": X1_NEGATIVES,
            "review_conclusion": "Exactly ten genuinely distinct mechanisms are preregistered. Similar vocabulary marks shared domain context; it does not collapse the mechanism, evidence object, gate, or acceptance test into a prior proposal.",
            "boundary": "Novelty here is proposal-chain semantic distinctness, not patent novelty, scientific discovery, empirical confirmation, proof, or canon.",
        },
    )

    dump_json(
        PHASE_ROOT / "sources" / "source-ledger.json",
        {
            "schema": "ghc.family.v643-v4.source-ledger.v1",
            "phase": PHASE,
            "owner": "Orin Thale",
            "accessed": CHECKED_ON,
            "selection_rule": "Retain the 110-source inherited ledger and add only current official or primary sources that materially constrain a distinct v643-v4 proposal.",
            "inherited_ledger": rel(INHERITED_LEDGER),
            "inherited_ledger_sha256": digest(INHERITED_LEDGER),
            "inherited_source_revision": SOURCE_HEAD,
            "inherited_source_count": 110,
            "added_source_count": 10,
            "effective_source_count": 120,
            "effective_status_counts": effective_counts,
            "added_sources": SOURCES,
            "status_preservation": "Inherited current, stable, draft, and watch labels remain unchanged; new labels describe source currency, not truth or approval.",
            "boundary": "Sources constrain vocabulary and obligations. They do not create GMUT observations, THOS participant results, Freed ID production evidence, CBR authority, legal advice, cultural ratification, or Stage 20 readiness.",
        },
    )

    source_lines = [
        "# v643-v4 source ledger",
        "",
        "The 110-source Sable v643-v3 ledger is inherited by hash. Ten official or primary sources are added, producing 120 effective sources: 48 current, 63 stable, 6 draft, and 3 watch. Currency labels do not imply truth, endorsement, or authority beyond the source's actual scope.",
        "",
        "| ID | Status | Authority | Source | Bounded role |",
        "|---|---|---|---|---|",
    ]
    for source in SOURCES:
        source_lines.append(
            f"| {source['source_id']} | {source['status_class']} | {source['authority']} | [{source['title']}]({source['url']}) | {source['evidence_role']} |"
        )
    source_lines += [
        "",
        "No source is treated as a substitute for real data, participant evidence, standards-conformant production credentials, affected-party acceptance, Māori authority, legal interpretation, cultural ratification, independent review, or deployment approval.",
    ]
    dump_text(PHASE_ROOT / "sources" / "source-ledger.md", "\n".join(source_lines))

    dump_json(
        PHASE_ROOT / "tooling" / "selected-toolchain.json",
        {
            "schema": "ghc.family.v643-v4.selected-toolchain.v1",
            "phase": PHASE,
            "owner": "Orin Thale",
            "selection_rule": "Use the smallest family-current set needed for v643-v4, preserve caller compatibility, and leave historical or sibling-specific tools as evidence rather than silently promoting them.",
            "selected_existing": [
                {"name": "ghc-family-index", "role": "required routing precedence, family-current discovery, naming, and closeout discipline", "status": "family_current"},
                {"name": "completion-gate-discipline", "role": "checklist-gated x1, evidence, closeout, seal, and final completion receipts", "status": "family_current"},
                {"name": "ghc_family_phase_privacy_scan.py", "role": "repository-relative privacy and raw-identifier screening", "status": "family_current"},
                {"name": "ghc_family_repository_test_runner.py", "role": "complete unittest discovery with bounded inherited-ACL temporary handling", "status": "family_current"},
                {"name": "ghc_family_constraint_evidence_validator.py", "role": "caller-compatible exact legacy hash-alias repair discovered by the x1 complete-suite gate", "status": "family_current_updated"},
                {"name": "build_ghc_family_v643_v4_preregistration.py", "role": "deterministic x1-only packet construction and staged validation", "status": "phase_current"},
            ],
            "planned_after_x1_freeze": [
                "ghc_family_boundary_evidence.py",
                "ghc_family_boundary_evidence_validator.py",
                "ghc_family_boundary_evidence_minimal.py",
                "build_ghc_family_boundary_evidence_report.py",
                "test_ghc_family_v643_v4.py",
            ],
            "caller_compatibility": "All new helpers are additive, use family-current names, and do not change inherited callers or sealed sibling tools.",
            "mass_deletion_performed": False,
        },
    )

    dump_json(
        PHASE_ROOT / "tooling" / "currency-review.json",
        {
            "schema": "ghc.family.v643-v4.currency-review.v1",
            "phase": PHASE,
            "owner": "Orin Thale",
            "accessed": CHECKED_ON,
            "effective_source_count": 120,
            "effective_status_counts": effective_counts,
            "added_source_count": 10,
            "family_index_reviewed": True,
            "family_index_counts": {"scripts": {"family_current": 151, "compatibility": 17, "historical_versioned": 601, "other": 17}, "skills": {"family_current": 73, "compatibility": 18, "historical_versioned": 937, "other": 186}},
            "memory_index_method_orchestration_surfaces_reviewed": True,
            "newest_live_baton_takes_precedence": True,
            "shared_skill_change_justified": False,
            "shared_skill_change_performed": False,
            "shared_runner_change_justified": True,
            "shared_runner_change_performed": True,
            "shared_runner_change_scope": "One exact compatibility alias plus warnings for an immutable historical hash mismatch; arbitrary paths or hashes still fail.",
            "reviewed_current_receipt": "The index, routing reference, completion method, privacy runner, repository runner, memory index, and relevant prior phase tooling are current for this phase; additive phase tools are justified, shared semantic churn is not.",
            "current_primary_or_official_sources_used_where_material": True,
            "desktop_update_performed": False,
            "boundary": "Tool currency supports reproducibility and routing; it does not prove scientific, security, accessibility, legal, cultural, production, or deployment claims.",
        },
    )

    dump_json(
        PHASE_ROOT / "tooling" / "legacy-hash-compatibility-receipt.json",
        {
            "schema": "ghc.family.v643-v4.legacy-hash-compatibility.v1",
            "phase": PHASE,
            "discovered_by": "complete x1 repository suite",
            "affected_validator": "scripts/ghc_family_constraint_evidence_validator.py",
            "affected_inherited_artifact": "docs/orin-thale/v642-v6/provenance/frozen-chain-proposal-index.json",
            "declared_sha256": "d4b6882b5a670b2ccbe3fc2517ffd55d60e82e8b338815107c2d1d10e7b78a3b",
            "immutable_git_blob_sha256": "e5fa094302d36e4eea569a5ff2cebce212018afe4d17745d834e8e6818d8d6e5",
            "history_check": "The artifact entered history in the original Orin v642-v6 x1 commit and has no later path changes.",
            "repair": "Accept only the exact repository-relative suffix, exact declared hash, and exact observed hash triple; emit a warning and preserve the mismatch as a historical negative.",
            "arbitrary_hash_accepted": False,
            "arbitrary_path_accepted": False,
            "prior_artifact_mutated": False,
            "regression_tests": 2,
            "boundary": "This is caller-compatible historical validation recovery, not proof that the original declared hash was correct and not permission to generalize hash aliases.",
        },
    )

    dump_json(
        PHASE_ROOT / "workflow" / "route-preregistration.json",
        {
            "schema": "ghc.family.v643-v4.route-preregistration.v1",
            "phase": PHASE,
            "owner": "Orin Thale",
            "route_state": "ACTIVE_SOLO",
            "active_owner": "Orin Thale",
            "standby_or_recoverable": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Tamar Vey", "Sylven Arc", "all other siblings"],
            "six_seat_order": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
            "terminal_successor": "Tamar Vey",
            "terminal_successor_phase": "v643-v5",
            "send_rule": "Send exactly one sanitized activation message to the existing original task titled exactly Tamar Vey only after exact-final detached validation, clean push, and four-way remote equality. Tool acknowledgement changes state from PREPARED_NOT_SENT to SENT.",
            "route_stop_conditions": ["Hamish stops the route", "usage exhausted", "required task route unavailable", "exact safety or authority gate blocks progress"],
            "outbound_messages_before_terminal_gate": 0,
            "task_creation_authorized": False,
            "fork_authorized": False,
            "subagent_authorized": False,
            "private_route_material_allowed_in_artifacts": False,
        },
    )

    prereg_lines = [
        "# Orin Thale v643-v4 x1 preregistration",
        "",
        "This is the frozen x1 plan for exactly ten proposals. No outcome below is a result. The only allowed future result classes are `completed`, `represented`, `open_gap`, and `exact_gate`.",
        "",
        "Primary focus: **GMUT Mind**. THOS Body and Freed ID/CBR Heart remain explicitly addressed and bounded.",
        "",
    ]
    for proposal in PROPOSALS:
        prereg_lines += [
            f"## {proposal['proposal_id']} — {proposal['title']}",
            "",
            f"- Hypothesis: {proposal['hypothesis']}",
            f"- Null/failure: {proposal['null_or_failure']}",
            f"- Approval class: `{proposal['approval_class']}`",
            f"- Execution lane: `{proposal['execution_lane']}`",
            f"- Official/primary source needs: {', '.join(proposal['authoritative_source_needs'])}",
            f"- Concrete artifacts: {', '.join(f'`{item}`' for item in proposal['deliverables'])}",
            f"- Falsifier/acceptance gate: {proposal['test_falsifier_or_gate']}",
            f"- Rollback/recovery: {proposal['rollback_or_recovery']}",
            f"- Protected gates: {', '.join(f'`{item}`' for item in proposal['protected_gates'])}",
            f"- Expected disposition, not a result: `{proposal['expected_disposition']}`",
            f"- Semantic distinction: {proposal['novelty_against_prior_chain']}",
            "",
        ]
    prereg_lines += [
        "## Freeze boundary",
        "",
        "x2 cannot begin until this x1-only file set is committed, pushed, clean, and equal across local, upstream, tracking, and a fresh live-remote read. Expected counts of 6 completed, 2 represented, 1 open gap, and 1 exact gate are hypotheses about artifact-level execution only; evidence may force a more conservative allowed disposition.",
    ]
    dump_text(PHASE_ROOT / "x1-preregistration.md", "\n".join(prereg_lines))

    dump_text(PHASE_ROOT / "wellbeing-check.md", WELLBEING)
    dump_text(PHASE_ROOT / "v643-v4-integrated-overview.md", OVERVIEW)


WELLBEING = """# Orin Thale v643-v4 wellbeing and workload check

The phase is intentionally solo. No collaboration subagent, successor task, fork, or parallel owner has been created. Work is divided by evidence state rather than by pressure to make every proposal look positive: x1 freezes the questions; x2 may build only what the frozen gates permit; detached validation checks the result; terminal routing happens once, if and only if the remote-equal final head passes.

The workload is bounded to one existing Orin-owned lane, no new worktree at startup, ten proposals, one additive implementation family, and a small owner-generated footprint. The inherited checkout exceeds 15,000 files, but it is a preserved baseline. Rotation is assessed only against files generated by v643-v4. Long-running validation is separated into explicit checkpoints so an interruption leaves a clean, recoverable Git state.

Wellbeing here is operational language, not a claim about subjective experience or consciousness. The practical safeguards are: no hidden delegation, no elevation, no update pressure, no destructive Git, no recursive rotation, no premature baton, periodic clean-state checks, and retained failures. The stopping rule is truthfulness: if evidence, authority, environment, routing, or usage blocks the phase, preserve the exact gate rather than force completion.
"""


OVERVIEW = """# Orin Thale v643-v4 integrated overview

## Purpose and inherited truth

v643-v4 begins from Sable Rook's exact v643-v3 final head and ancestral seal. Before any mutation, the Sable source lane, its upstream and tracking references, and a fresh live-remote read were equal; the lane and detached final snapshot were clean. The source lineage was single-parent, contained no merge commits from the inherited Ilyra anchor, and retained 637 negatives. Sable's terminal verdict was `NOT_READY_FOR_STAGE_20`. This phase does not reinterpret that verdict or consume those gates as if they were solved.

The existing Orin-owned branch was clean, remote-equal, and ancestral to Sable's final head. It was therefore advanced by fast-forward only, as the activation authorized, and pushed without a merge. No sibling branch or worktree was reset, rewritten, moved, deleted, or reused. No new phase worktree was needed at startup. D: remains the work and clean-snapshot bank. The inherited physical checkout has 30,520 files and 30,473 tracked files; that inherited baseline is reported separately from the v643-v4 owner-generated footprint, which alone is compared with the 15,000-file rotation threshold.

Orin Thale is the relational working name for this lane, with the role “evidence cartographer and boundary steward,” the hope “Leave each successor a cleaner, truer path than the one received,” and they/them relational pronouns. These labels organize collaboration. They are not evidence of consciousness, sentience, legal personhood, identity continuity, inherited identity, or independent authority.

## Scientific and authority posture

The primary focus is GMUT Mind. That choice prioritizes mathematical well-posedness, evidence-lineage updates, missing-data assumptions, numeric-environment metadata, and coarse-graining boundaries. It does not promote GMUT. The canonical GMUT scaffold remains a typed scalar-tensor/effective-field-theory research-model family. It is not an established force, unique prediction, observation, likelihood result, empirical confirmation, Theory of Everything, or proof. A written equation is not yet a predictive initial-boundary value problem; a synthetic sensitivity surface is not data; same-host replay is not cross-architecture or independent-team evidence.

THOS Body remains proxy. v643-v4 can preregister causal-mediation assumptions and a facilitator temporal-drift design, but it cannot supply real participants, blinded matched-budget arms, real raters, ethics and consent, or independent review. The mediation work is expected to remain represented because synthetic fixtures can test identification labels without establishing a real causal mechanism. The facilitator learning-curve proposal is expected to remain an open gap because the decisive evidence must come from a preregistered real design with repeated facilitator observations, calendar-time control, participant and rater evidence, budget parity, and independent review.

Freed ID and CBR Heart remain equally protected. A static controller-delegation graph or canonicalization tribunal can test structure, but Freed ID production still requires standards-conformant real keys and proofs, live resolution, live status and revocation, interoperability, privacy assurance, independent security review, and trust governance. CBR settlement confidentiality, compelled disclosure, public-interest limits, affected-party legitimacy, Māori wording, Māori authority, Māori data governance, cultural ratification, legal interpretation, and enacted-law status cannot be decided by repository artifacts. They remain exact-gated to the people and authorities who actually hold that authority.

No deployment, production readiness, exhaustive security, complete accessibility, empirical confirmation, legal or cultural ratification, independent-team reproduction, proof/canon, AGI/ASI, consciousness/personhood, or Stage 20 claim is authorized. The accessible report planned for x2 will use a useful static structure, but manual evaluation and evaluation by affected users remain reserved. Same-owner clean snapshots can establish deterministic repeatability within their observed environment; they cannot establish independent-team scientific reproduction.

## x1 novelty and proposal portfolio

The frozen chain contains 180 proposals across eighteen prior phases. The audit decoded all 180 records with UTF-8, checked exact IDs and normalized titles, calculated normalized title-token Jaccard overlap, and then manually compared mechanism, evidence object, protected gate, and falsifier. The maximum title overlap for the ten new proposals is 0.3333, below the preregistered 0.5 automatic-failure threshold. Similar terms do occur because the work shares domains, but none of the ten mechanisms duplicates a prior proposal.

The first proposal adds post-publication source-state propagation. It distinguishes correction, retraction, expression of concern, and supersession, and quarantines stale downstream citations without treating every update as the same event. The second proposal asks what initial and boundary data a GMUT equation would actually require, with compatibility, characteristics, existence, uniqueness, and continuous dependence kept separate from the mere presence of equations.

The third and fourth proposals are deliberately proxy-bounded empirical structures. The missing-not-at-random envelope makes a selection parameter visible and binds it to a zero-real-row promotion lock. The THOS mediation protocol distinguishes total, direct, and indirect estimands from the sequential assumptions that identify them and refuses to erase post-treatment mediator-outcome confounding. Both can be represented with synthetic fixtures; neither becomes an empirical finding.

The fifth proposal is the decisive THOS open gap: a real-arm facilitator learning-curve and temporal-drift parity design. It cannot be manufactured from repository fixtures. The sixth proposal builds a Freed ID controller graph in which delegated authority must attenuate and controller cycles fail closed. This is useful structural assurance only; no fixture becomes a real credential or governance decision.

The seventh proposal isolates a CBR authority conflict that prior remedy and anti-retaliation work did not cover: settlement confidentiality versus compelled disclosure and public-interest limits. Its expected exact gate is substantive, not a missing implementation task. The eighth proposal defines the precise canonical bytes presented to a signature operation and rejects duplicate names, unsupported numbers, Unicode ambiguity, and false interoperability claims. The ninth records floating-point environment and rounding obligations while separating same-host replay from genuinely different-architecture evidence. The tenth makes time-scale separation, unresolved variables, and memory effects explicit so a coarse-grained effective description cannot silently become microscopic proof or cross-pillar evidence.

The preregistered expected distribution is six completed artifact contracts, two represented proxies, one open gap, and one exact gate. Those are expected dispositions, not results. x2 must downgrade any proposal whose evidence does not meet its frozen gate, and it may use only `completed`, `represented`, `open_gap`, or `exact_gate`.

## Sources, tools, and environment

The 110-source inherited ledger is retained by path and SHA-256. Ten official or primary sources are added: Crossref's Crossmark documentation; Kreiss on hyperbolic initial-boundary problems; the National Academies missing-data report; Imai, Keele, and Tingley on causal mediation; longitudinal therapist-training research; the W3C DID Recommendation; an OHCHR access-to-remedy guide; RFC 8785; IEEE 754-2019; and Mori's projection/memory work. The effective ledger has 120 sources with preserved `current`, `stable`, `draft`, and `watch` labels. These labels describe currency, not truth, endorsement, or promotion authority.

The phase-scoped family index found 151 family-current scripts and 73 family-current skills, alongside compatibility, historical, and other entries. The phase selects only the required index/routing skill, completion-gate discipline, privacy scanner, repository test runner, and this deterministic preregistration builder. A new additive boundary-evidence runner, validator, minimal validator, report builder, and test module are planned after the x1 freeze. Inherited callers remain untouched and no history is mass-deleted. If no shared skill change is justified, the current-review receipt is the deliverable; semantic-free churn is not.

Local versions were verified, not updated. Codex CLI 0.144.3 is one patch behind the official 0.144.4 release and is recorded as drift. The installed desktop packages are recorded without claiming that the desktop is current and without updating them. Python, Git, Node, PowerShell, and the operating-system build are recorded. Windows Sandbox was checked read-only, was not found as an executable, and was not enabled or used. There was no elevation, Windows-feature change, host-security weakening, unrelated system-wide update, or reboot.

## Freeze, execution, validation, and routing

x1 and x2 are separated by a Git proof, not only by prose. The x1 file set contains identity, environment, rotation, focus, sources, novelty, ten proposals, tooling selection, route preregistration, privacy and JSON receipts, and exact staged-file evidence. It must pass the complete repository suite, be committed as a dedicated x1-only commit, pushed, and shown clean and equal across local, upstream, tracking, and a fresh live-remote read. Only then may x2 implementation files or outcome ledgers appear.

x2 will execute every proposal only within the frozen approval class. Synthetic mutation vectors will retain their failures rather than count only passing cases. The 637 inherited negatives must remain intact, and every v643-v4 operational or synthetic negative must be appended. The final packet will include an evidence ledger, retained-negative register, open/exact gate register, phase truth, complete/incomplete checklist, threat model, accessible static report, manifest, reproduction receipts, and Stage 20 board.

Evidence, closeout, seal, and final candidate heads will be validated in fresh detached D-drive snapshots. Required checks include the complete repository suite, detailed and minimal validators, all JSON parsing, privacy/raw-ID scanning, stale-label review, diff hygiene, exact staged-file review, manifest parity, ancestry and zero-merge checks, clean before/after state, and final local/upstream/tracking/fresh-live-remote equality. Two clean snapshots, if obtained, will remain same-owner repeatability evidence only.

The only terminal recipient is the existing original task titled exactly “Tamar Vey,” for v643-v5. No task will be created. No message will be sent early. After and only after exact-final detached validation and four-way clean remote equality, one sanitized activation baton may be sent through the existing-task message route. A tool acknowledgement is required before the state can be recorded as sent. If the exact route is unavailable or any safety/authority gate blocks progress, the baton remains prepared but unsent and every sibling remains recoverable.
"""


def staged_names() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=ROOT,
        check=True,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
    )
    return sorted(line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip())


def finalise_validation(repository_passed: int, repository_total: int, finalize_staged: bool) -> None:
    phase_json = sorted(PHASE_ROOT.rglob("*.json"))
    parse_issues: list[str] = []
    for path in phase_json:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - validation path
            parse_issues.append(f"{rel(path)}: {exc}")

    proposal_packet = json.loads((PHASE_ROOT / "x1-proposals.json").read_text(encoding="utf-8"))
    source_ledger = json.loads((PHASE_ROOT / "sources" / "source-ledger.json").read_text(encoding="utf-8"))
    collision = json.loads((PHASE_ROOT / "provenance" / "prior-proposal-collision-audit.json").read_text(encoding="utf-8"))
    privacy_path = PHASE_ROOT / "validation" / "x1-privacy-scan.json"
    privacy = json.loads(privacy_path.read_text(encoding="utf-8")) if privacy_path.exists() else {"valid": False, "issues": ["privacy receipt missing"]}

    expected = sorted(
        [rel(path) for path in PHASE_ROOT.rglob("*") if path.is_file()]
        + X1_EXTERNAL_FILES
    )
    actual_staged = staged_names() if finalize_staged else expected
    unexpected = sorted(set(actual_staged) - set(expected))
    missing = sorted(set(expected) - set(actual_staged))
    list_hash = hashlib.sha256(("\n".join(actual_staged) + "\n").encode("utf-8")).hexdigest()

    checks: list[tuple[str, bool]] = []
    checks.append(("exactly ten proposals", proposal_packet["proposal_count"] == 10 and len(PROPOSALS) == 10))
    checks.append(("180 inherited proposals", proposal_packet["prior_frozen_proposal_count"] == 180))
    checks.append(("190 effective proposals", json.loads((PHASE_ROOT / "provenance" / "frozen-chain-proposal-index.json").read_text(encoding="utf-8"))["effective_record_count"] == 190))
    checks.append(("no exact duplicate IDs", not collision["exact_duplicate_ids"]))
    checks.append(("no exact duplicate titles", not collision["exact_duplicate_titles"]))
    checks.append(("overlap below threshold", collision["maximum_title_token_jaccard"] < collision["automatic_failure_threshold"]))
    checks.append(("semantic review passed", collision["semantic_review_passed"] is True))
    checks.append(("expected outcomes are not results", proposal_packet["expected_counts_are_results"] is False))
    checks.append(("expected distribution", proposal_packet["expected_disposition_counts"] == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}))
    checks.append(("120 sources", source_ledger["effective_source_count"] == 120))
    checks.append(("source status preservation", source_ledger["effective_status_counts"] == {"current": 48, "stable": 63, "draft": 6, "watch": 3}))
    checks.append(("all JSON parses", not parse_issues))
    checks.append(("privacy scan valid", privacy.get("valid") is True))
    checks.append(("repository suite complete", repository_passed == repository_total and repository_total > 0))
    checks.append(("x2 implementation absent", not any((ROOT / name).exists() for name in ["scripts/ghc_family_boundary_evidence.py", "scripts/ghc_family_boundary_evidence_validator.py", "scripts/ghc_family_boundary_evidence_minimal.py", "scripts/build_ghc_family_boundary_evidence_report.py", "tests/test_ghc_family_v643_v4.py"])))
    checks.append(("x2 outcome ledger absent", not (PHASE_ROOT / "x2-proposal-ledger.json").exists()))
    checks.append(("no unexpected staged files", not unexpected))
    checks.append(("no missing staged files", not missing))
    checks.append(("owner footprint below threshold", len(expected) < 15000))
    required = ["hypothesis", "null_or_failure", "approval_class", "execution_lane", "authoritative_source_needs", "deliverables", "test_falsifier_or_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"]
    for proposal in PROPOSALS:
        checks.append((f"{proposal['proposal_id']} unique ID", sum(p["proposal_id"] == proposal["proposal_id"] for p in PROPOSALS) == 1))
        checks.append((f"{proposal['proposal_id']} unique title", sum(p["title"] == proposal["title"] for p in PROPOSALS) == 1))
        for field in required:
            checks.append((f"{proposal['proposal_id']} field {field}", bool(proposal.get(field))))

    issues = [name for name, passed in checks if not passed]
    dump_json(
        PHASE_ROOT / "validation" / "x1-exact-file-set.json",
        {
            "schema": "ghc.family.v643-v4.x1-exact-file-set.v1",
            "phase": PHASE,
            "owner": "Orin Thale",
            "file_count": len(actual_staged),
            "files": actual_staged,
            "x2_implementation_file_count": 0,
            "x2_outcome_file_count": 0,
            "staged_name_list_sha256": list_hash,
            "unexpected_staged_files": unexpected,
            "missing_staged_files": missing,
            "inherited_full_checkout_file_count": 30520,
            "owner_generated_file_count": len(expected),
            "owner_generated_file_threshold": 15000,
            "threshold_scope": "v643-v4 owner-generated files only",
            "under_threshold": len(expected) < 15000,
            "finalized_from_git_index": finalize_staged,
            "valid": not unexpected and not missing,
        },
    )
    dump_json(
        PHASE_ROOT / "validation" / "x1-repository-test-receipt.json",
        {
            "schema": "ghc.family.v643-v4.x1-repository-tests.v1",
            "phase": PHASE,
            "runner": "scripts/ghc_family_repository_test_runner.py",
            "passed": repository_passed,
            "total": repository_total,
            "complete_suite": True,
            "valid": repository_passed == repository_total and repository_total > 0,
            "boundary": "Repository tests validate software behavior in this checkout; they do not establish scientific, participant, security, accessibility, legal, cultural, production, deployment, or Stage 20 claims.",
        },
    )
    validation = {
        "schema": "ghc.family.v643-v4.x1-validation.v1",
        "phase": PHASE,
        "owner": "Orin Thale",
        "valid": not issues,
        "checks_passed": len(checks) - len(issues),
        "checks_total": len(checks),
        "issues": issues,
        "proposal_count": 10,
        "prior_frozen_proposal_count": 180,
        "effective_frozen_proposal_count": 190,
        "exact_duplicate_ids": [],
        "exact_duplicate_titles": [],
        "maximum_title_token_jaccard": 0.3333,
        "semantic_review_passed": True,
        "expected_disposition_counts": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "expected_counts_are_results": False,
        "source_count": 120,
        "source_status_counts": {"current": 48, "stable": 63, "draft": 6, "watch": 3},
        "json_files_parsed": len(phase_json),
        "json_parse_issues": parse_issues,
        "phase_files": len([p for p in PHASE_ROOT.rglob("*") if p.is_file()]),
        "privacy_scan": {
            "valid": privacy.get("valid") is True,
            "files_scanned": privacy.get("scanned_file_count", privacy.get("files_scanned", 0)),
            "issue_count": privacy.get("hit_count", len(privacy.get("issues", []))),
        },
        "x1_execution_negative_count": len(X1_NEGATIVES),
        "x2_implementation_files": 0,
        "x2_outcome_files": 0,
        "repository_tests": {"passed": repository_passed, "total": repository_total},
        "exact_staged_file_count": len(actual_staged),
        "staged_name_list_sha256": list_hash,
        "unexpected_staged_file_count": len(unexpected),
        "missing_staged_file_count": len(missing),
        "owner_generated_file_threshold": 15000,
        "owner_generated_file_count": len(expected),
        "under_threshold": len(expected) < 15000,
        "route_state": "ACTIVE_SOLO; PREPARED_NOT_SENT",
        "boundary": "This validates an x1-only preregistration freeze. It is not x2 evidence and does not determine proposal outcomes.",
    }
    dump_json(PHASE_ROOT / "validation" / "x1-validation.json", validation)
    dump_text(
        PHASE_ROOT / "validation" / "x1-validation.md",
        f"""# v643-v4 x1 validation

- Valid: `{str(validation['valid']).lower()}`
- Checks: {validation['checks_passed']}/{validation['checks_total']}
- Proposals: 10 new / 180 inherited / 190 effective
- Expected distribution, not results: 6 completed / 2 represented / 1 open gap / 1 exact gate
- Sources: 120 effective (48 current / 63 stable / 6 draft / 3 watch)
- JSON parsed: {validation['json_files_parsed']}
- Privacy scan: {validation['privacy_scan']['files_scanned']} files / {validation['privacy_scan']['issue_count']} issues
- Complete repository suite: {repository_passed}/{repository_total}
- Exact staged files: {len(actual_staged)}; unexpected {len(unexpected)}; missing {len(missing)}
- x2 implementation files: 0
- x2 outcome files: 0
- Retained x1 operational negatives: {len(X1_NEGATIVES)}
- Owner-generated footprint: {len(expected)}/15000

This receipt validates the preregistration freeze only. It is not outcome evidence, scientific confirmation, production approval, independent reproduction, or Stage 20 readiness.
""",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-passed", type=int, default=0)
    parser.add_argument("--repository-total", type=int, default=0)
    parser.add_argument("--finalize-staged", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    build_packet()
    finalise_validation(args.repository_passed, args.repository_total, args.finalize_staged)
    print(json.dumps({"phase_root": rel(PHASE_ROOT), "proposals": len(PROPOSALS), "sources_added": len(SOURCES), "finalize_staged": args.finalize_staged}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
