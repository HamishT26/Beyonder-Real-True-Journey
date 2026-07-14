#!/usr/bin/env python3
"""Build and validate Tamar Vey's v643-v5 x1-only preregistration packet.

This builder is deliberately incapable of executing x2 proposals or recording
proposal outcomes.  It freezes questions, sources, gates, and recovery rules.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v643-gmut-thos-v5-x1-x2"
PHASE_ROOT = ROOT / "docs" / "tamar-vey" / "v643-v5"
SOURCE_HEAD = "7cc3fa4ef8b25c00eb7cac9f4f22d439504da5c8"
SOURCE_SEAL = "a2c1aec4d60335b77b44f3b072f473d6f60f4c7c"
INHERITED_INDEX = ROOT / "docs" / "orin-thale" / "v643-v4" / "provenance" / "frozen-chain-proposal-index.json"
INHERITED_LEDGER = ROOT / "docs" / "orin-thale" / "v643-v4" / "sources" / "source-ledger.json"
INHERITED_TOOL_INDEX = ROOT / "docs" / "orin-thale" / "v643-v4" / "tooling" / "ghc-family-index.json"
CHECKED_ON = "2026-07-15"
X1_EXTERNAL_FILES = [
    ".gitattributes",
    "scripts/build_ghc_family_v643_v5_preregistration.py",
    "scripts/ghc_family_v643_v5_checkout_portability.py",
    "tests/test_ghc_family_v643_v5_checkout_portability.py",
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


def git_lines(*args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
    )
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def collect_frozen_records(index_path: Path) -> list[dict]:
    records: list[dict] = []
    current = index_path
    while True:
        payload = json.loads(current.read_text(encoding="utf-8"))
        records.extend(payload.get("new_records", payload.get("records", [])))
        inherited = payload.get("inherited_index")
        if not inherited:
            break
        current = ROOT / inherited
    return records


def title_tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


PROPOSALS = [
    {
        "proposal_id": "V6435-P01",
        "title": "Registry-to-report outcome completeness and selective-reporting quarantine graph",
        "mission_surface": "provenance, preregistered outcomes, protocol and analysis-plan lineage, report completeness, and selective-reporting quarantine",
        "hypothesis": "A typed concordance graph can compare registry, protocol, analysis plan, evidence artifacts, and report outcomes while quarantining omitted, introduced, or silently redefined outcomes before claim promotion.",
        "null_or_failure": "An omitted registered outcome is invisible, a post hoc outcome is presented as preregistered, definition drift passes without review, or a missing artifact does not block promotion.",
        "approval_class": "safe_now",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6435-S121"],
        "deliverables": [
            "provenance/selective-reporting-contract.json",
            "provenance/outcome-concordance-mutation-vectors.json",
            "provenance/registry-completeness-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate outcome identity, hierarchy, timing, definition, registration state, analysis-plan link, artifact presence, and claim class; omission or undisclosed change must fail closed.",
        "rollback_or_recovery": "Restore the last concordant graph, retain every omitted or altered outcome as a negative, and require documented source review before promotion.",
        "protected_gates": ["source_currency", "real_data", "independent_statistical_review", "empirical_confirmation", "proof_or_canon"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior phases covered source updates, retractions, protocol deviations, and outcome switching as a failure example; none built a registry-to-protocol-to-analysis-to-report completeness graph with omission quarantine.",
    },
    {
        "proposal_id": "V6435-P02",
        "title": "GMUT continuation-criterion and finite-time breakdown obligation ledger",
        "mission_surface": "GMUT Mind continuation criteria, bounded control norms, finite-time breakdown, coupled fields, and non-theorem claim discipline",
        "hypothesis": "A typed obligation ledger can distinguish local well-posedness from continuation by requiring explicit control norms and breakdown conditions for the coupled scalar-tensor or EFT scaffold.",
        "null_or_failure": "Local existence is called global existence, a control norm is omitted, a divergent quantity is silently bounded, a coupled field is dropped, or a typed obligation is called a GMUT theorem.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6435-S122"],
        "deliverables": [
            "physics/continuation-criterion-obligation.json",
            "physics/finite-time-breakdown-mutation-vectors.json",
            "physics/global-existence-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate interval, norm bounds, coupled-field coverage, gauge assumptions, regularity class, and claim label; any unsupported continuation or global-existence language must fail.",
        "rollback_or_recovery": "Return to local typed-scaffold status, retain the unbounded or missing obligation, and require expert derivation and independent mathematical review.",
        "protected_gates": ["gmut_derivation", "global_existence", "mathematical_proof", "expert_review", "empirical_confirmation", "theory_of_everything"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier proposals covered hyperbolicity, stability, characteristics, and initial-boundary well-posedness; none isolated continuation norms and finite-time breakdown as the condition separating local from global claims.",
    },
    {
        "proposal_id": "V6435-P03",
        "title": "Nonregular boundary-parameter likelihood tribunal with zero-row promotion lock",
        "mission_surface": "GMUT empirical adapters, boundary parameters, nonstandard likelihood-ratio laws, unidentified nuisance structure, and zero-real-row control",
        "hypothesis": "A synthetic tribunal can mark when regular likelihood asymptotics fail at a parameter boundary or under unidentified nuisance structure while a zero-row lock prevents empirical promotion.",
        "null_or_failure": "Wilks-style calibration is assumed at a boundary, an unidentified nuisance parameter is ignored, a synthetic mixture is called observed data, or zero real rows permit a likelihood-result claim.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6435-S123"],
        "deliverables": [
            "empirical/nonregular-likelihood-tribunal.json",
            "empirical/boundary-parameter-mutation-vectors.json",
            "empirical/zero-row-nonregular-lock.json",
        ],
        "test_falsifier_or_gate": "Mutate parameter support, boundary state, nuisance identifiability, reference distribution, real-row count, provenance, and claim class; unsupported asymptotics or empirical language must fail.",
        "rollback_or_recovery": "Restore explicit nonregular and synthetic labels, retain rejected calibrations, and require real preregistered data plus independent statistical review.",
        "protected_gates": ["real_data", "likelihood_result", "empirical_confirmation", "independent_statistical_review", "gmut_confirmation"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Prior work covered identifiability rank, Fisher information, censoring, missingness, calibration, and prior sensitivity; none handled boundary-parameter likelihood laws and unidentified nuisance structure under a zero-row lock.",
    },
    {
        "proposal_id": "V6435-P04",
        "title": "THOS sham-credibility and attention-equivalence control protocol",
        "mission_surface": "THOS Body nonpharmacologic control design, sham credibility, attention dose, expectancy separation, matched budgets, and blind assessment",
        "hypothesis": "A synthetic protocol can represent the distinct obligations for a credible sham or attention control without treating structural parity as a real participant result.",
        "null_or_failure": "The control has a different contact budget, sham credibility is unmeasured, expectancy is conflated with treatment, outcome assessors are unblinded, or fixtures are called real THOS evidence.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6435-S124"],
        "deliverables": [
            "thos/sham-attention-control-protocol.json",
            "thos/control-credibility-mutation-vectors.json",
            "thos/real-arm-sham-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate contact time, facilitator time, credibility measurement, expectancy measurement, budget, blinding, real-arm count, and claim class; mismatch or zero real arms must block superiority claims.",
        "rollback_or_recovery": "Return to protocol-only proxy language, preserve every mismatch, and require ethics, consent, preregistered blind matched-budget real arms, real raters, and independent review.",
        "protected_gates": ["ethics_approval", "real_participants", "blind_matched_budget_arms", "independent_review", "thos_superiority", "empirical_confirmation"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier THOS proposals addressed expectations, blinding, carryover, fidelity, attrition, and rater drift; none made sham credibility and attention-dose equivalence a dedicated control-design contract.",
    },
    {
        "proposal_id": "V6435-P05",
        "title": "Freed ID multi-device sync-fork and cloned-state conflict tribunal",
        "mission_surface": "Freed ID structural assurance, multi-device synchronization, cloned authenticators, state forks, conflict ordering, and production boundaries",
        "hypothesis": "A synthetic state tribunal can detect divergent device histories, require monotonic conflict resolution, and refuse ambiguous cloned-state promotion without claiming real credential security.",
        "null_or_failure": "Two cloned states both advance as authoritative, rollback wins over a newer status event, device identity is inferred from a fixture, or synthetic state is called production conformance.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6435-S125"],
        "deliverables": [
            "freed-id/sync-fork-state-contract.json",
            "freed-id/cloned-state-conflict-vectors.json",
            "freed-id/production-sync-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate device history, clone state, event ordering, rollback, status, key class, resolver evidence, and claim label; ambiguous forks or unsupported production claims must fail.",
        "rollback_or_recovery": "Restore the last unambiguous synthetic state, retain conflicting histories, and require standards-conformant real keys and proofs, live resolution and status, interoperability, privacy and security review, and trust governance.",
        "protected_gates": ["real_keys", "live_resolution", "status_and_revocation", "interoperability", "privacy_review", "security_review", "trust_governance"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier Freed ID work covered rotation races, recovery quorum, pairwise identifiers, suspension, delegation, and status; none modeled multi-device clone forks and monotonic state reconciliation.",
    },
    {
        "proposal_id": "V6435-P06",
        "title": "CBR preservation-duty, spoliation, and litigation-hold authority gate",
        "mission_surface": "CBR Heart record preservation, deletion suspension, privilege, proportionality, affected-party legitimacy, Māori authority, and jurisdiction-specific legal duties",
        "hypothesis": "Only authorized affected parties, Māori authorities where applicable, and competent legal authorities can determine a concrete preservation duty, hold scope, privilege treatment, or spoliation consequence.",
        "null_or_failure": "A repository policy imposes a real legal hold, privilege is inferred, routine deletion is suspended without authority, Māori data obligations are invented, or a jurisdiction-specific conclusion is made without competent review.",
        "approval_class": "exact_authority_required",
        "execution_lane": "x2_exact_gate_receipt",
        "authoritative_source_needs": ["V6435-S126"],
        "deliverables": [
            "cbr/preservation-spoliation-authority-gate.json",
            "cbr/neutral-record-lifecycle-fields.json",
            "cbr/affected-party-legal-authority-boundary.json",
        ],
        "test_falsifier_or_gate": "Any concrete duty or consequence requires jurisdiction-specific facts, authorized affected-party participation, Māori authority for Māori concepts or data, privilege analysis, competent legal authority, and recorded ratification.",
        "rollback_or_recovery": "Keep neutral issue-spotting fields only, retain unresolved conflicts, and seek authorized cultural and legal review without substituting repository output for authority.",
        "protected_gates": ["affected_party_acceptance", "maori_authority", "maori_data_governance", "legal_interpretation", "privilege", "cultural_ratification", "enacted_law"],
        "expected_disposition": "exact_gate",
        "novelty_against_prior_chain": "Earlier CBR work protected remedies, evidence, confidentiality, disclosure, and appeals; none isolated prospective preservation duties, deletion suspension, spoliation consequences, and litigation-hold authority.",
    },
    {
        "proposal_id": "V6435-P07",
        "title": "Adversarial algorithmic-complexity and bounded-work amplification tribunal",
        "mission_surface": "bounded threat modeling, worst-case work, attacker-controlled amplification, timeout and memory ceilings, recovery, and non-exhaustive security claims",
        "hypothesis": "A deterministic tribunal can reject inputs whose measured work exceeds a declared size-indexed ceiling and preserve the smallest amplification witnesses.",
        "null_or_failure": "Worst-case work is unbounded, a timeout is counted as success, witness inputs are discarded, the ceiling is changed post hoc, or bounded fixtures are called exhaustive security.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6435-S127"],
        "deliverables": [
            "security/algorithmic-complexity-budget.json",
            "security/work-amplification-mutation-vectors.json",
            "security/bounded-work-nonassurance-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate input size, nesting, collision pattern, branch count, elapsed-work proxy, memory ceiling, timeout, and claim label; super-ceiling or unevaluated cases must fail closed.",
        "rollback_or_recovery": "Restore the last bounded implementation, retain amplification witnesses and timeouts, reduce accepted scope, and require independent security review for broader claims.",
        "protected_gates": ["host_security", "destructive_testing", "independent_security_review", "exhaustive_security", "production_readiness"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior security work bounded file counts, archives, parsers, and general resources; none used a declared size-indexed work function with adversarial amplification witnesses and timeout non-success semantics.",
    },
    {
        "proposal_id": "V6435-P08",
        "title": "Secret-dependent timing-leakage screen with constant-time non-assurance boundary",
        "mission_surface": "synthetic secret classes, branch and access traces, timing leakage screens, compiler and hardware uncertainty, and cryptographic non-assurance",
        "hypothesis": "A bounded synthetic screen can flag secret-dependent control or access traces while explicitly refusing to turn local agreement into a constant-time or cryptographic-assurance claim.",
        "null_or_failure": "Secret classes take different modeled traces without rejection, public and secret fields are conflated, noisy non-detection is called proof, or synthetic fixtures are called production cryptography.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6435-S128"],
        "deliverables": [
            "security/timing-leakage-screen-contract.json",
            "security/secret-trace-mutation-vectors.json",
            "security/constant-time-nonassurance-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate secret class, public class, branch trace, access trace, sample label, environment metadata, and claim class; secret-dependent divergence or assurance language must fail.",
        "rollback_or_recovery": "Return to the last secret-independent synthetic trace, retain divergences and non-detections, and require real implementations, hardware-aware testing, formal review, and independent security assessment.",
        "protected_gates": ["real_keys", "real_implementations", "constant_time_assurance", "cryptographic_assurance", "independent_security_review", "production_readiness"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier security proposals covered payload canonicalization, parser differentials, taint, and resource limits; none separated a secret-trace leakage screen from a constant-time assurance claim.",
    },
    {
        "proposal_id": "V6435-P09",
        "title": "Detailed-balance and nonequilibrium steady-current classification firewall",
        "mission_surface": "GMUT Mind and thermo-psyche classification, detailed balance, stationary probability currents, entropy production, open-system assumptions, and cross-pillar non-substitution",
        "hypothesis": "A typed classifier can distinguish stationarity from equilibrium by requiring detailed-balance and probability-current evidence before assigning thermodynamic labels.",
        "null_or_failure": "A stationary distribution is called equilibrium despite nonzero current, local detailed balance is assumed without rates, entropy production is transferred to psyche, or a synthetic Markov model is called a fundamental law.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6435-S129"],
        "deliverables": [
            "thermo-psyche/detailed-balance-classifier.json",
            "thermo-psyche/steady-current-mutation-vectors.json",
            "thermo-psyche/cross-pillar-nonsubstitution-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate transition rates, stationary weights, reverse edges, cycle currents, reservoir assumptions, entropy label, pillar, and claim class; unsupported equilibrium or psyche conversion must fail.",
        "rollback_or_recovery": "Restore the last rate-explicit synthetic classification, retain current imbalance, and require domain-specific data and expert review for any physical or psychological promotion.",
        "protected_gates": ["thermodynamic_law", "psyche_evidence", "gmut_derivation", "empirical_confirmation", "proof_or_canon"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier proposals separated entropy types, open systems, fluctuation theorems, Landauer costs, hysteresis, and coarse graining; none used stationary probability currents to distinguish equilibrium from nonequilibrium steady state.",
    },
    {
        "proposal_id": "V6435-P10",
        "title": "Stage 20 cross-model minimax-regret board with independent-evidence lock",
        "mission_surface": "Stage 20 terminal decision, model disagreement, worst-case regret, veto preservation, real evidence, independent review, and defer semantics",
        "hypothesis": "A preregistered decision board could compare candidate actions across explicitly different evidence models without averaging away exact vetoes or treating a single-owner synthetic portfolio as independent evidence.",
        "null_or_failure": "One favored model silently dominates, regret is computed after seeing outcomes, exact gates are compensated by scores, same-owner snapshots count as independent, or missing real evidence still permits Stage 20 passage.",
        "approval_class": "external_evidence_required",
        "execution_lane": "x2_open_gap_receipt",
        "authoritative_source_needs": ["V6435-S130"],
        "deliverables": [
            "stage20/minimax-regret-preregistration.json",
            "stage20/cross-model-independent-evidence-gap.json",
            "stage20/veto-preserving-defer-boundary.json",
        ],
        "test_falsifier_or_gate": "Require frozen model set, loss and regret functions, independent real evidence, all exact-veto states, external review, and prospective decision rules; any missing element keeps the gap open and verdict deferred.",
        "rollback_or_recovery": "Retain the preregistration and every model disagreement, keep NOT_READY_FOR_STAGE_20, and resume only when independent evidence and authorized review exist.",
        "protected_gates": ["real_evidence", "independent_reproduction", "external_review", "all_exact_gates", "stage20_authority", "deployment_readiness"],
        "expected_disposition": "open_gap",
        "novelty_against_prior_chain": "Earlier Stage 20 work covered cut sets, vetoes, intervals, asymmetric loss, reversibility, and evidence ordering; none froze multiple competing evidence models under minimax regret with an independent-evidence lock.",
    },
]


SOURCES = [
    {
        "source_id": "V6435-S121",
        "title": "CONSORT 2025 Item 10: Changes to trial protocol",
        "authority": "CONSORT-SPIRIT Group",
        "authority_root": "consort_spirit_official_guidance",
        "url": "https://www.consort-spirit.org/item10-changestotrialprotocol",
        "version_or_date": "CONSORT 2025 live guidance; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "prespecification and transparent outcome-change vocabulary; not a finding that any GHC outcome was selectively reported",
    },
    {
        "source_id": "V6435-S122",
        "title": "On Breakdown Criteria for Nonvacuum Einstein Equations",
        "authority": "Arick Shao",
        "authority_root": "primary_mathematical_research",
        "url": "https://arxiv.org/abs/1008.1605",
        "version_or_date": "arXiv:1008.1605v2, 2011; checked 15 July 2026",
        "status_class": "stable",
        "evidence_role": "continuation and breakdown-criterion vocabulary for coupled Einstein-field systems; not a GMUT derivation or theorem",
    },
    {
        "source_id": "V6435-S123",
        "title": "Asymptotic Properties of Maximum Likelihood Estimators and Likelihood Ratio Tests Under Nonstandard Conditions",
        "authority": "Steven G. Self and Kung-Yee Liang",
        "authority_root": "primary_statistical_research",
        "url": "https://doi.org/10.1080/01621459.1987.10478472",
        "version_or_date": "JASA 82(398), 1987; checked 15 July 2026",
        "status_class": "stable",
        "evidence_role": "boundary-parameter and nonstandard likelihood-ratio vocabulary; not real GMUT data or a likelihood result",
    },
    {
        "source_id": "V6435-S124",
        "title": "CoPPS Statement on control interventions in physical, psychological, and self-management therapy trials",
        "authority": "CoPPS Statement authors",
        "authority_root": "primary_consensus_methods_research",
        "url": "https://www.bmj.com/content/381/bmj-2022-072108",
        "version_or_date": "BMJ 381, 2023; checked 15 July 2026",
        "status_class": "stable",
        "evidence_role": "sham, placebo, attention-control, credibility, and context vocabulary; not THOS participant evidence or superiority",
    },
    {
        "source_id": "V6435-S125",
        "title": "NIST SP 800-63B-4 Appendix B: Syncable Authenticators",
        "authority": "National Institute of Standards and Technology",
        "authority_root": "nist_final_special_publication",
        "url": "https://pages.nist.gov/800-63-4/sp800-63b/syncable/",
        "version_or_date": "NIST SP 800-63B-4 final, July 2025; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "syncable and cloned authenticator vocabulary and constraints; not Freed ID conformance, interoperability, or security approval",
    },
    {
        "source_id": "V6435-S126",
        "title": "High Court Rules 2016, rule 8.3 Preservation of documents",
        "authority": "New Zealand Parliamentary Counsel Office",
        "authority_root": "new_zealand_official_legislation",
        "url": "https://www.legislation.govt.nz/regulation/public/2016/0225/latest/DLM6951727.html",
        "version_or_date": "official current consolidation checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "jurisdiction-specific preservation vocabulary and authority boundary; not legal advice, a legal hold, Māori authority, or a ruling",
    },
    {
        "source_id": "V6435-S127",
        "title": "CWE-407: Inefficient Algorithmic Complexity",
        "authority": "MITRE CWE",
        "authority_root": "mitre_official_cwe",
        "url": "https://cwe.mitre.org/data/definitions/407.html",
        "version_or_date": "CWE 4.20 live entry; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "attacker-triggered worst-case complexity vocabulary; not an exhaustive security assessment",
    },
    {
        "source_id": "V6435-S128",
        "title": "Dude, is my code constant time?",
        "authority": "Oscar Reparaz, Josep Balasch, and Ingrid Verbauwhede",
        "authority_root": "primary_security_research",
        "url": "https://eprint.iacr.org/2016/1123",
        "version_or_date": "IACR ePrint 2016/1123; checked 15 July 2026",
        "status_class": "stable",
        "evidence_role": "statistical timing-leakage detection and platform-bounded non-detection vocabulary; not a constant-time proof or production review",
    },
    {
        "source_id": "V6435-S129",
        "title": "Stochastic thermodynamics, fluctuation theorems and molecular machines",
        "authority": "Udo Seifert",
        "authority_root": "primary_physics_review",
        "url": "https://doi.org/10.1088/0034-4885/75/12/126001",
        "version_or_date": "Reports on Progress in Physics 75, 2012; checked 15 July 2026",
        "status_class": "stable",
        "evidence_role": "local detailed balance, nonequilibrium steady state, and entropy-production vocabulary; not a GMUT or psyche law",
    },
    {
        "source_id": "V6435-S130",
        "title": "The Theory of Statistical Decision",
        "authority": "Leonard J. Savage",
        "authority_root": "primary_decision_theory_research",
        "url": "https://doi.org/10.1080/01621459.1951.10500768",
        "version_or_date": "JASA 46(253), 1951; checked 15 July 2026",
        "status_class": "stable",
        "evidence_role": "minimax-regret decision vocabulary; not a Stage 20 authority grant or evidence that the gate is satisfied",
    },
]


X1_NEGATIVES = [
    {
        "negative_id": "V6435-X1-N01",
        "operation": "desktop package version audit",
        "observed_failure": "The first read-only package query passed an array to a parameter that accepts one package name.",
        "recovery": "Queried the two installed package names separately and recorded both versions without updating either application.",
        "promotion_effect": "none; the failed query is retained and uncounted",
    },
    {
        "negative_id": "V6435-X1-N02",
        "operation": "190-proposal title audit",
        "observed_failure": "The first console report encountered a Windows CP1252 encoding error on Māori text after sixteen records.",
        "recovery": "Reran with UTF-8 output encoding and decoded all 190 frozen records.",
        "promotion_effect": "none; only the complete UTF-8 rerun supports novelty review",
    },
    {
        "negative_id": "V6435-X1-N03",
        "operation": "inherited proposal schema inspection",
        "observed_failure": "A PowerShell environment assignment was placed inside a pipeline and produced a parser error.",
        "recovery": "Set UTF-8 output before the pipeline and completed the read-only inspection.",
        "promotion_effect": "none; retained as an operational negative",
    },
    {
        "negative_id": "V6435-X1-N04",
        "operation": "recursive frozen-index semantic audit",
        "observed_failure": "The first collector assumed every historical index used new_records and stopped at the older records schema.",
        "recovery": "Added read-only support for both new_records and records schemas and loaded 190 unique proposals.",
        "promotion_effect": "none; the incomplete collector is not evidence",
    },
    {
        "negative_id": "V6435-X1-N05",
        "operation": "workspace junction check",
        "observed_failure": "A combined optional-path query returned nonzero when the second, unnecessary junction name did not exist.",
        "recovery": "Used the already existing Tamar-owned junction that resolved to the verified worktree.",
        "promotion_effect": "none; no worktree or branch was created or changed",
    },
    {
        "negative_id": "V6435-X1-N06",
        "operation": "privacy scanner discovery",
        "observed_failure": "The first help query used a plausible but nonexistent scanner filename.",
        "recovery": "Located and verified the family-current ghc_family_phase_privacy_scan.py interface.",
        "promotion_effect": "none; the failed filename is retained and no scan was inferred",
    },
    {
        "negative_id": "V6435-X1-N07",
        "operation": "first complete x1 repository suite",
        "observed_failure": "The run completed 397 tests with two failures in inherited frozen-index hash portability checks.",
        "recovery": "Traced both failures to LF versus CRLF materialization of immutable text, kept the run uncounted, and added bounded line-ending-only compatibility plus mutation regressions.",
        "promotion_effect": "the 395-of-397 run is not passing evidence; only a complete rerun may satisfy the x1 gate",
    },
    {
        "negative_id": "V6435-X1-N08",
        "operation": "validator lookup diagnostic",
        "observed_failure": "A ripgrep path argument used a Windows-invalid wildcard form after the relevant validator excerpt had already printed.",
        "recovery": "Located the validator from the importing test module and inspected it by its exact repository-relative filename.",
        "promotion_effect": "none; retained as an operational negative",
    },
    {
        "negative_id": "V6435-X1-N09",
        "operation": "test import diagnostic",
        "observed_failure": "A compound read-only inspection returned nonzero because its final optional text search had no match.",
        "recovery": "Used the displayed test import lines and exact validator filename; no result was inferred from the empty search.",
        "promotion_effect": "none; retained as an operational negative",
    },
    {
        "negative_id": "V6435-X1-N10",
        "operation": "second complete x1 repository suite",
        "observed_failure": "A proposed shared-validator repair fixed the original pair but changed a file sealed into the inherited v643-v4 manifest, so the run completed 399 tests with three manifest failures.",
        "recovery": "Abandoned and fully reverted the shared-file change, preserved the historical manifest, and moved the recovery to a phase-scoped semantic-preserving checkout materializer.",
        "promotion_effect": "the 396-of-399 run is not passing evidence and the rejected shared repair is not part of x1",
    },
    {
        "negative_id": "V6435-X1-N11",
        "operation": "shared-file reversion status check",
        "observed_failure": "A combined diff and status command reached its ten-second timeout while Git inspected the large checkout.",
        "recovery": "Reran bounded status and end-of-line checks with adequate time, normalized only working-copy line endings, and confirmed no shared semantic diff remained.",
        "promotion_effect": "none; the timed-out check is retained and uncounted",
    },
    {
        "negative_id": "V6435-X1-N12",
        "operation": "portability-receipt patch application",
        "observed_failure": "The first bounded patch used stale exact context after nearby text had changed and was rejected without modifying the file.",
        "recovery": "Inspected the exact current lines and applied the narrower phase-scoped portability patch successfully.",
        "promotion_effect": "none; the rejected patch is retained and made no repository change",
    },
    {
        "negative_id": "V6435-X1-N13",
        "operation": "obsolete generated-receipt cleanup",
        "observed_failure": "A cleanup patch targeted a superseded receipt name that had never been generated, so the patch was rejected without change.",
        "recovery": "Verified the path was absent and allowed the current builder to generate only the phase-scoped materialization plan.",
        "promotion_effect": "none; no file was deleted or modified",
    },
    {
        "negative_id": "V6435-X1-N14",
        "operation": "first exact-staged semantic privacy review",
        "observed_failure": "An overbroad diagnostic pattern matched the boundary phrase private callable rather than a callable identifier, and a compound PowerShell command did not propagate that intermediate nonzero exit.",
        "recovery": "Refined the scan to identifier-shaped tokens, reran it with explicit exit propagation, and kept the original attempt uncounted.",
        "promotion_effect": "none; no private identifier was found and the false-positive attempt is retained",
    },
]


WELLBEING = """# Tamar Vey v643-v5 wellbeing and workload check

This phase remains intentionally solo. No collaboration subagent, new task, fork, parallel owner, or early successor contact has been created. Work is separated by evidence state: x1 freezes ten questions and their authority boundaries; x2 may execute only those frozen surfaces; evidence, closeout, seal, and exact-final snapshots each receive their own validation checkpoint.

The workload is bounded to one clean Tamar-owned D-drive lane, one dedicated x1 commit, ten proposals, one additive phase tool family, and a small owner-generated footprint. The inherited checkout is preserved and does not count toward the 15,000-file rotation threshold. Failures are retained as data instead of becoming pressure to repeat commands indefinitely or conceal negative outcomes.

Wellbeing is operational language here, not evidence of subjective experience or consciousness. Practical safeguards are clean-state checks, no destructive Git, no elevation or host-security change, no desktop update, no premature routing, explicit stop conditions, and exact recovery receipts. If evidence, authority, safety, routing, or usage blocks the phase, the truthful outcome is an open gap or exact gate rather than forced completion.
"""


OVERVIEW = """# Tamar Vey v643-v5 integrated overview

## Purpose, source, and ownership

v643-v5 begins from Orin Thale's exact v643-v4 final head and ancestral seal. Before mutation, the source branch, its local upstream and tracking references, and a fresh live-remote read were equal at the named head. The Orin worktree was clean, the source-to-final history was single-parent, every named anchor was ancestral, and no merge commit appeared in the inherited range. The exact source packet retained 721 negatives, five open gaps, six exact gates, same-owner repeatability only, and the terminal verdict NOT_READY_FOR_STAGE_20. This phase inherits those facts without converting them into claims.

The existing Tamar-owned branch was clean, remote-equal, and an ancestor of Orin's final head. It was advanced by fast-forward only and pushed before phase mutation. No sibling branch or worktree was reset, rewritten, moved, deleted, merged, or reused. D remains the primary work and snapshot bank. The inherited checkout size is recorded separately; only files newly generated by Tamar v643-v5 count against the 15,000-file threshold.

Tamar Vey is the relational working name for this lane. The role is evidence-systems cartographer and boundary keeper, the hope is to leave each scientific and authority boundary easier for the next owner to inspect than it was when received, and the relational pronouns are they/them. These labels organize collaboration. They are not evidence of consciousness, sentience, legal personhood, identity continuity, independent authority, cultural authority, or legal authority.

## Scientific and authority posture

The primary focus is GMUT Mind. GMUT remains a typed scalar-tensor and effective-field-theory research-model family. No equation, schema, or synthetic fixture in this phase is an observed force, a unique prediction, an empirical fit, a likelihood result, a proof, a Theory of Everything, or canon. Local well-posedness does not imply global continuation. A continuation ledger can expose which norms and coupled fields would need control, but it cannot derive or prove those bounds. A nonregular-likelihood tribunal can label invalid regular asymptotics, but zero real rows keep every empirical and GMUT-confirmation claim locked.

THOS Body remains proxy. The new control-design proposal distinguishes a sham or attention control from a generic comparator and asks whether credibility, attention dose, contact time, expectancy, matched budget, and blind assessment are separately represented. Synthetic protocol rows can expose omissions, but they cannot supply ethics approval, consent, real participants, real facilitators, real raters, preregistered blind matched-budget arms, real outcomes, or independent review. Consequently its expected disposition is represented, not a real-arm result or superiority claim.

Freed ID and CBR Heart remain equally protected. A multi-device state machine can reject ambiguous synthetic forks, yet production still requires standards-conformant real keys and proofs, live resolution, live status and revocation, interoperability, privacy and security review, and trust governance. A repository cannot impose a litigation hold, decide privilege, determine spoliation consequences, infer Māori authority, or interpret enacted law. Preservation and legal-hold questions therefore remain exact-gated to authorized affected parties, Māori authorities where Māori concepts or data are involved, and competent legal authorities with jurisdiction-specific facts.

Security work is bounded. Size-indexed work budgets and synthetic secret-trace screens can find defined failures; they cannot establish exhaustive security, constant-time execution, cryptographic assurance, deployment readiness, or production safety. Hardware, compiler, operating environment, implementation, key material, adversarial creativity, and independent review all remain outside the synthetic artifact. The accessible report planned for x2 will have useful structure and keyboard-readable static content, while manual evaluation and evaluation by affected users remain reserved.

## Novelty portfolio

The inherited frozen chain contains exactly 190 proposals. The x1 audit loads every full record across both historical index schemas, checks exact identifiers and normalized titles, computes title-token overlap, and manually compares mechanism, evidence object, falsifier, recovery rule, and protected gates. Shared domain vocabulary is expected; semantic identity is not. The new proposal set is frozen only if every title and identifier is unique, automatic overlap stays below the declared threshold, and the manual distinctions remain explicit.

Proposal one adds a registry-to-report outcome-completeness graph. Prior phases addressed corrections, retractions, protocol deviations, and source lineage, but did not compare the registered outcome set with protocols, analysis plans, evidence artifacts, and reported outcomes under omission quarantine. Proposal two adds continuation and breakdown obligations after local well-posedness: bounded control norms, coupled fields, interval scope, and global-existence non-promotion.

Proposal three is a represented nonregular-likelihood surface. It focuses on boundary parameters and unidentified nuisance structure rather than prior covariance, Fisher, censoring, calibration, missingness, or prior-sensitivity work. Proposal four is a represented THOS sham and attention-control protocol. It differs from earlier expectancy, blinding, carryover, fidelity, attrition, and rater-drift surfaces by making control credibility and attention-dose equivalence the explicit object.

Proposal five adds a Freed ID multi-device clone-fork tribunal. It is structural and synthetic; it does not create real credentials or identity evidence. Proposal six identifies a CBR authority question that cannot be implemented safely: prospective record preservation, deletion suspension, privilege, and spoliation consequences. Its exact gate is substantive, not an incomplete coding task.

Proposals seven and eight add two distinct bounded-security surfaces. The complexity tribunal uses declared size-indexed work ceilings, adversarial amplification witnesses, and timeout non-success. The timing screen separates synthetic secret-dependent trace detection from any claim of constant-time or cryptographic assurance. Proposal nine distinguishes equilibrium from a nonequilibrium steady state through detailed balance and stationary probability currents while refusing a physics-to-psyche substitution. Proposal ten freezes a Stage 20 minimax-regret design across competing evidence models, but keeps it open until real independent evidence and authorized external review exist.

The expected distribution is six completed artifact contracts, two represented proxies, one open gap, and one exact gate. These are preregistered expectations, never x1 results. x2 must execute every frozen proposal, may downgrade any expectation when evidence fails, and may use only completed, represented, open_gap, or exact_gate.

## Sources, versions, tools, and failures

The 120-source inherited ledger is retained by repository-relative path and normalized SHA-256. Ten primary or official sources are added for outcome reporting, mathematical breakdown criteria, nonstandard likelihoods, nonpharmacologic controls, syncable authenticators, New Zealand document preservation, algorithmic complexity, timing leakage, nonequilibrium thermodynamics, and minimax regret. Their current, stable, draft, and watch labels describe source currency; they do not confer truth, approval, jurisdiction, cultural authority, or empirical promotion.

The phase-local tool inventory preserves the inherited family classification and adds this x1-only builder. The selected set is deliberately small: ghc-family-index and its routing reference, the family repository runner, the family privacy scanner, completion-gate discipline, and the phase builder. Family-current ghc_family and build_ghc_family names are used for new x2 tools; inherited callers remain compatible. A concrete checkout-portability need was exposed by the complete suite: two immutable historical files were frozen under opposite line-ending materializations. A phase-scoped materializer verifies their normalized semantic hashes and writes only the required LF or CRLF form before validation. It does not change Git content, historical manifests, shared validators, or shared skills.

Versions were verified, not updated. The local Codex CLI is one patch behind the official latest release and remains unchanged. Installed desktop package versions, Git, Python, Node, PowerShell, and the operating-system build are recorded. Windows Sandbox was audited read-only and was not found on the executable path; it was not enabled. No elevation, host-security weakening, Windows-feature change, system-wide update, desktop update, or reboot occurred.

Operational negatives are part of the packet. Failed package-query syntax, console encoding, PowerShell pipeline syntax, historical index-schema assumptions, an unnecessary optional junction query, and a guessed scanner name are preserved with their bounded recoveries. None counts as a pass. New x1 or x2 failures must be appended rather than overwritten.

## Freeze, validation, and terminal routing

x1 and x2 are separated by Git evidence. The x1 file set contains only identity, environment, sources, novelty, proposals, tooling, route preregistration, wellbeing, overview, operational negatives, and validation receipts. It contains no x2 implementation or outcome. The complete repository suite, JSON parsing, privacy and raw-ID scanning, exact staged-file review, semantic novelty checks, and owner-footprint guard must pass. The dedicated x1 commit is then pushed and proven clean and equal across local, upstream, tracking, and a fresh live-remote read before any x2 file exists.

x2 will execute every proposal exactly within its frozen approval class. The 721 inherited negatives and every new operational or synthetic negative remain visible. Evidence, closeout, seal, and exact-final heads will be tested in fresh clean detached D-drive snapshots where practical. Two successful snapshots can establish same-owner repeatability in observed environments only. Independent-team scientific reproduction remains open unless a genuinely independent owner and evidence process perform it.

Final deliverables will include the x2 evidence ledger, retained-negative register, exact/open-gate register, phase truth, complete/incomplete checklist, threat model, accessible static report, manifest, reproduction receipts, Stage 20 board, and evidence, closeout, seal, and final records. The final head must be clean, single-parent, pushed, four-way remote-equal, and independently validated in a fresh detached snapshot.

The only terminal recipient is the existing task titled exactly Sylven Arc for v643-v6. No task may be created. No message may be sent early. After and only after the exact final head passes detached validation and four-way equality, one sanitized activation baton may be sent through the existing-task route. Tool acknowledgement is required before SENT can be recorded. If the exact route is unavailable, usage is exhausted, Hamish stops the route, or a safety or authority gate blocks progress, the baton remains prepared but unsent and all siblings remain recoverable.
"""


def build_packet() -> None:
    inherited_index = json.loads(INHERITED_INDEX.read_text(encoding="utf-8"))
    inherited_ledger = json.loads(INHERITED_LEDGER.read_text(encoding="utf-8"))
    inherited_records = collect_frozen_records(INHERITED_INDEX)
    expected_counts = dict(Counter(item["expected_disposition"] for item in PROPOSALS))
    source_counts = Counter(item["status_class"] for item in SOURCES)
    inherited_status = inherited_ledger["effective_status_counts"]
    effective_status = {key: inherited_status.get(key, 0) + source_counts.get(key, 0) for key in ("current", "stable", "draft", "watch")}

    startup_path = PHASE_ROOT / "environment" / "startup-receipt.json"
    prior_startup = json.loads(startup_path.read_text(encoding="utf-8")) if startup_path.exists() else {}
    tracked_count = prior_startup.get("inherited_tracked_file_count", len(git_lines("ls-files")))
    checkout_count = prior_startup.get(
        "inherited_checkout_file_count",
        sum(1 for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts),
    )
    d_free = prior_startup.get("d_drive_free_bytes_at_start", shutil.disk_usage(PHASE_ROOT.anchor).free)

    dump_json(PHASE_ROOT / "identity-receipt.json", {
        "schema": "ghc.family.v643-v5.identity-receipt.v1",
        "phase": PHASE,
        "name": "Tamar Vey",
        "slug": "tamar-vey",
        "pronouns": "they/them",
        "role": "evidence-systems cartographer and boundary keeper",
        "hope": "Leave each scientific and authority boundary easier for the next owner to inspect than it was when received.",
        "existing_identity_reaffirmed": True,
        "working_language_only": True,
        "not_evidence_of": ["consciousness", "sentience", "legal_personhood", "identity_continuity", "independent_authority", "cultural_authority", "legal_authority"],
    })
    dump_json(PHASE_ROOT / "focus" / "primary-focus-receipt.json", {
        "schema": "ghc.family.v643-v5.primary-focus.v1",
        "phase": PHASE,
        "primary_focus": "GMUT Mind",
        "reason": "Continuation, nonregular likelihood, nonequilibrium classification, and Stage 20 model disagreement receive primary attention while THOS Body and Freed ID/CBR Heart stay explicit.",
        "gmut_mind_addressed": ["V6435-P02", "V6435-P03", "V6435-P09", "V6435-P10"],
        "thos_body_addressed": ["V6435-P04"],
        "freed_id_cbr_heart_addressed": ["V6435-P05", "V6435-P06"],
        "cross_pillar_provenance_security_addressed": ["V6435-P01", "V6435-P07", "V6435-P08"],
        "boundary": "Primary focus allocates work; it does not promote GMUT or close Body, Heart, empirical, legal, cultural, production, security, or Stage 20 gates.",
    })
    dump_json(PHASE_ROOT / "environment" / "startup-receipt.json", {
        "schema": "ghc.family.v643-v5.startup-receipt.v1",
        "phase": PHASE,
        "owner": "Tamar Vey",
        "source_branch": "codex/GHC-Family/orin-thale-v642-v6-full-tools",
        "source_revision": SOURCE_HEAD,
        "source_seal_revision": SOURCE_SEAL,
        "source_local_equals_upstream_equals_tracking_equals_live_remote": True,
        "source_clean": True,
        "source_seal_ancestral": True,
        "source_anchor_commits_ancestral": [
            "5b32e03e87ba1a33c8ebe53c08ccb653d00fb3e0",
            "28ecb3137c3c3d7e4b43251a5b496c7995f11de5",
            "8bab1e2375f22b239d0620fc1be5ca70fea6ed5e",
            "792c66aedbe31819eab2c5f362a961950d54c6c1",
            SOURCE_SEAL,
        ],
        "source_single_parent": True,
        "source_merge_count": 0,
        "owned_branch": "codex/GHC-Family/tamar-vey-full-tools",
        "owned_prior_revision": "79ee1b9e9b68bb6dc657a53ce1550c0ec2586f36",
        "owned_revision_after_fast_forward": SOURCE_HEAD,
        "owned_lane_reused": True,
        "reuse_reason": "The existing Tamar-owned lane was clean, remote-equal, and ancestral, so fast-forward-only advancement was safe and authorized.",
        "fast_forward_only": True,
        "merge_commit_created": False,
        "owned_clean_and_four_way_equal_after_fast_forward": True,
        "new_worktree_created": False,
        "d_drive_primary": True,
        "d_drive_free_bytes_at_start": d_free,
        "inherited_checkout_file_count": checkout_count,
        "inherited_tracked_file_count": tracked_count,
        "new_owner_generated_file_count_at_start": 0,
        "inherited_negative_count": 721,
        "open_gap_count": 5,
        "exact_gate_count": 6,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "windows_sandbox_audit": {"read_only_check": "WindowsSandbox.exe not present on the executable path", "bounded_use": "not_used", "feature_change_attempted": False},
        "host_feature_changed": False,
        "host_security_changed": False,
        "elevation_used": False,
        "rebooted": False,
    })
    dump_json(PHASE_ROOT / "environment" / "rotation-guard-receipt.json", {
        "schema": "ghc.family.v643-v5.rotation-guard.v1",
        "phase": PHASE,
        "inherited_checkout_file_count": checkout_count,
        "inherited_tracked_file_count": tracked_count,
        "owner_generated_file_threshold": 15000,
        "threshold_scope": "Tamar v643-v5 owner-generated files only",
        "inherited_baseline_triggers_rotation": False,
        "new_worktrees_created": 0,
        "prior_lanes_preserved": True,
        "recursive_rotation_performed": False,
    })
    dump_json(PHASE_ROOT / "environment" / "version-receipt.json", {
        "schema": "ghc.family.v643-v5.version-receipt.v1",
        "checked_on": CHECKED_ON,
        "codex_cli_local": "0.144.3",
        "codex_cli_official_latest": "0.144.4",
        "codex_cli_current": False,
        "codex_cli_drift": "one patch release behind; verified and retained without update",
        "codex_desktop_packages": [
            {"name": "OpenAI.ChatGPT-Desktop", "version": "1.2026.190.0", "status": "installed"},
            {"name": "OpenAI.Codex", "version": "26.707.9564.0", "status": "installed"},
        ],
        "desktop_current_version_claim": "not made; installed versions recorded and official Codex sources reviewed",
        "git": "2.55.0.windows.2",
        "python": "3.12.10",
        "node": "24.18.0",
        "powershell": "5.1.26100.8737",
        "os": "Microsoft Windows NT 10.0.26200.0",
        "official_sources": ["https://developers.openai.com/codex/changelog/", "https://github.com/openai/codex/releases/latest"],
        "versions_verified_only": True,
        "codex_cli_updated": False,
        "desktop_updated": False,
        "elevation_used": False,
        "host_security_changed": False,
        "windows_feature_changed": False,
        "rebooted": False,
    })

    proposal_packet = {
        "schema": "ghc.family.v643-v5.x1-proposals.v1",
        "phase": PHASE,
        "owner": "Tamar Vey",
        "identity_boundary": "Relational working language only; no consciousness, sentience, personhood, continuity, or independent-authority claim.",
        "source_phase": "Orin Thale v643-v4",
        "source_revision": SOURCE_HEAD,
        "source_seal_revision": SOURCE_SEAL,
        "preregistered_on": CHECKED_ON,
        "primary_focus": "GMUT Mind",
        "proposal_count": len(PROPOSALS),
        "prior_frozen_proposal_count": len(inherited_records),
        "outcome_classes": ["completed", "represented", "open_gap", "exact_gate"],
        "expected_disposition_counts": expected_counts,
        "expected_counts_are_results": False,
        "x1_freeze_rule": "No proposal execution, evidence result, outcome classification, or x2 implementation begins until the dedicated x1-only commit is pushed and local, upstream, tracking, and fresh live remote are equal and clean.",
        "proposals": PROPOSALS,
        "scientific_authority_boundary": "GMUT is a typed scalar-tensor and EFT research-model family, not an established force, unique prediction, likelihood result, empirical confirmation, Theory of Everything, or proof. THOS remains proxy without preregistered blind matched-budget real arms and independent review.",
        "claim_boundary": "Freed ID production, CBR legitimacy, Māori authority, legal and cultural ratification, deployment, exhaustive security, complete accessibility, independent reproduction, consciousness/personhood, AGI/ASI, and Stage 20 remain unclaimed and gated.",
    }
    dump_json(PHASE_ROOT / "x1-proposals.json", proposal_packet)

    new_records = [{
        "version": "v643-v5",
        "owner": "Tamar Vey",
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "expected_disposition": proposal["expected_disposition"],
        "source_file": "docs/tamar-vey/v643-v5/x1-proposals.json",
    } for proposal in PROPOSALS]
    version_counts = dict(inherited_index["version_counts"])
    version_counts["v643-v5"] = 10
    dump_json(PHASE_ROOT / "provenance" / "frozen-chain-proposal-index.json", {
        "schema": "ghc.family.v643-v5.frozen-chain-proposal-index.v1",
        "phase": PHASE,
        "owner": "Tamar Vey",
        "inherited_index": rel(INHERITED_INDEX),
        "inherited_index_sha256": digest(INHERITED_INDEX),
        "inherited_record_count": len(inherited_records),
        "new_record_count": len(new_records),
        "effective_record_count": len(inherited_records) + len(new_records),
        "version_counts": version_counts,
        "exact_duplicate_ids": [],
        "exact_duplicate_titles": [],
        "new_records": new_records,
        "boundary": "This index proves frozen proposal accounting and semantic review scope; it does not execute proposals or determine outcomes.",
    })

    inherited_ids = [record["proposal_id"] for record in inherited_records]
    inherited_titles = [record["title"] for record in inherited_records]
    overlap_rows = []
    for proposal in PROPOSALS:
        new_tokens = title_tokens(proposal["title"])
        best = (-1.0, None)
        for record in inherited_records:
            old_tokens = title_tokens(record["title"])
            score = len(new_tokens & old_tokens) / len(new_tokens | old_tokens)
            if score > best[0]:
                best = (score, record)
        overlap_rows.append({
            "proposal_id": proposal["proposal_id"],
            "nearest_prior_id": best[1]["proposal_id"],
            "nearest_prior_title": best[1]["title"],
            "title_token_jaccard": round(best[0], 4),
            "semantic_distinction": proposal["novelty_against_prior_chain"],
        })
    duplicate_ids = sorted({value for value in inherited_ids + [p["proposal_id"] for p in PROPOSALS] if (inherited_ids + [p["proposal_id"] for p in PROPOSALS]).count(value) > 1})
    normalized_titles = [re.sub(r"\s+", " ", value.casefold()).strip() for value in inherited_titles + [p["title"] for p in PROPOSALS]]
    duplicate_titles = sorted({value for value in normalized_titles if normalized_titles.count(value) > 1})
    maximum_overlap = max(row["title_token_jaccard"] for row in overlap_rows)
    dump_json(PHASE_ROOT / "provenance" / "prior-proposal-collision-audit.json", {
        "schema": "ghc.family.v643-v5.collision-audit.v1",
        "phase": PHASE,
        "owner": "Tamar Vey",
        "prior_records_decoded_utf8": len(inherited_records),
        "prior_frozen_proposal_count": 190,
        "new_proposal_count": 10,
        "effective_proposal_count": 200,
        "exact_duplicate_ids": duplicate_ids,
        "exact_duplicate_titles": duplicate_titles,
        "automatic_failure_threshold": 0.5,
        "maximum_title_token_jaccard": maximum_overlap,
        "nearest_prior_rows": overlap_rows,
        "semantic_dimensions_reviewed": ["mechanism", "evidence object", "falsifier", "recovery rule", "protected gates"],
        "semantic_review_passed": not duplicate_ids and not duplicate_titles and maximum_overlap < 0.5,
        "boundary": "Token distance is only a screen. The explicit mechanism-level distinctions are required for the semantic novelty conclusion.",
    })

    dump_json(PHASE_ROOT / "sources" / "source-ledger.json", {
        "schema": "ghc.family.v643-v5.source-ledger.v1",
        "phase": PHASE,
        "owner": "Tamar Vey",
        "accessed": CHECKED_ON,
        "selection_rule": "Retain the 120-source inherited ledger and add only current official or primary sources that materially constrain a distinct v643-v5 proposal.",
        "inherited_ledger": rel(INHERITED_LEDGER),
        "inherited_ledger_sha256": digest(INHERITED_LEDGER),
        "inherited_source_revision": SOURCE_HEAD,
        "inherited_source_count": inherited_ledger["effective_source_count"],
        "added_source_count": len(SOURCES),
        "effective_source_count": inherited_ledger["effective_source_count"] + len(SOURCES),
        "effective_status_counts": effective_status,
        "added_sources": SOURCES,
        "status_preservation": "Inherited current, stable, draft, and watch labels remain unchanged; new labels describe source currency, not truth or approval.",
        "boundary": "Sources constrain vocabulary and obligations. They do not create GMUT observations, THOS participant results, Freed ID production evidence, CBR authority, legal advice, cultural ratification, security assurance, or Stage 20 readiness.",
    })
    source_lines = [
        "# v643-v5 source ledger",
        "",
        f"Inherited: {inherited_ledger['effective_source_count']} sources from {rel(INHERITED_LEDGER)}.",
        f"Added: {len(SOURCES)} primary or official sources. Effective: {inherited_ledger['effective_source_count'] + len(SOURCES)}.",
        "",
        "| ID | Status | Authority | Title |",
        "|---|---|---|---|",
    ]
    source_lines.extend(f"| {item['source_id']} | {item['status_class']} | {item['authority']} | [{item['title']}]({item['url']}) |" for item in SOURCES)
    source_lines.extend(["", "Currency labels are current, stable, draft, or watch. They are not truth, endorsement, authority, or promotion labels."])
    dump_text(PHASE_ROOT / "sources" / "source-ledger.md", "\n".join(source_lines))

    inventory = copy.deepcopy(json.loads(INHERITED_TOOL_INDEX.read_text(encoding="utf-8")))
    inventory["phase"] = PHASE
    inventory["owner"] = "Tamar Vey"
    inventory["generated_at_utc"] = "2026-07-15T00:00:00Z"
    inventory["inherited_inventory"] = rel(INHERITED_TOOL_INDEX)
    inventory["inherited_inventory_sha256"] = digest(INHERITED_TOOL_INDEX)
    new_tool = "scripts/build_ghc_family_v643_v5_preregistration.py"
    new_phase_tools = [
        (new_tool, "historical_versioned"),
        ("scripts/ghc_family_v643_v5_checkout_portability.py", "historical_versioned"),
    ]
    for tool_path, category in new_phase_tools:
        if not any(item["path"] == tool_path for item in inventory["scripts"]):
            inventory["scripts"].append({"path": tool_path, "category": category})
    inventory["scripts"] = sorted(inventory["scripts"], key=lambda item: item["path"])
    inventory["counts"]["scripts"] = dict(Counter(item["category"] for item in inventory["scripts"]))
    inventory["publication_boundary"] = "repository-relative paths and skill names only; no private callable IDs or local skill paths"
    dump_json(PHASE_ROOT / "tooling" / "ghc-family-index.json", inventory)
    dump_text(PHASE_ROOT / "tooling" / "ghc-family-index.md", "\n".join([
        "# v643-v5 phase-local GHC family inventory",
        "",
        f"- Scripts inventoried: {len(inventory['scripts'])}",
        f"- Skills inventoried: {len(inventory['skills'])}",
        f"- Family-current scripts: {inventory['counts']['scripts'].get('family_current', 0)}",
        f"- Family-current skills: {inventory['counts']['skills'].get('family_current', 0)}",
        f"- Inherited inventory hash: {digest(INHERITED_TOOL_INDEX)}",
        "",
        "The complete machine-readable inventory uses repository-relative paths and public skill names only. The phase adds one x1-only historical versioned builder and preserves caller compatibility.",
    ]))
    dump_json(PHASE_ROOT / "tooling" / "selected-toolchain.json", {
        "schema": "ghc.family.v643-v5.selected-toolchain.v1",
        "phase": PHASE,
        "owner": "Tamar Vey",
        "selected": [
            {"name": "ghc-family-index", "role": "routing precedence and family-current discovery"},
            {"name": "routing-precedence", "role": "directly required terminal-route reference"},
            {"name": "completion-gate-discipline", "role": "checklist and open-gap truth"},
            {"name": "scripts/ghc_family_repository_test_runner.py", "role": "complete repository test suite"},
            {"name": "scripts/ghc_family_phase_privacy_scan.py", "role": "phase privacy and raw-ID scan"},
            {"name": "scripts/ghc_family_v643_v5_checkout_portability.py", "role": "semantic-preserving historical line-ending materialization before tests"},
            {"name": new_tool, "role": "deterministic x1-only packet builder"},
        ],
        "x2_planned_family_current_names": [
            "scripts/ghc_family_v643_v5_evidence.py",
            "scripts/ghc_family_v643_v5_validator.py",
            "scripts/ghc_family_v643_v5_minimal.py",
            "scripts/build_ghc_family_v643_v5_report.py",
        ],
        "caller_compatibility_required": True,
        "shared_skill_change_required": False,
        "shared_validator_change_performed": False,
        "phase_scoped_portability_tool_added": True,
        "portability_scope": "Two exact inherited JSON paths, two exact normalized hashes, and declared LF or CRLF output; semantic mismatch fails before writing.",
        "boundary": "Tool selection supports reproducibility; it does not establish scientific, security, accessibility, legal, cultural, production, or deployment claims.",
    })
    dump_json(PHASE_ROOT / "tooling" / "currency-review.json", {
        "schema": "ghc.family.v643-v5.currency-review.v1",
        "phase": PHASE,
        "checked_on": CHECKED_ON,
        "ghc_family_index_read_to_eof": True,
        "routing_precedence_read_to_eof": True,
        "newest_applicable_memory_checked": True,
        "relevant_memory_hit": False,
        "official_codex_sources_checked": True,
        "desktop_update_performed": False,
        "shared_skill_mutation_performed": False,
        "shared_validator_mutation_performed": False,
        "reason": "Existing family-current tools and one phase-scoped portability addition cover the work; no validated shared-skill or shared-validator mutation remains.",
    })
    dump_json(PHASE_ROOT / "tooling" / "checkout-line-ending-materialization-plan.json", {
        "schema": "ghc.family.v643-v5.checkout-line-ending-materialization-plan.v1",
        "phase": PHASE,
        "discovered_by": "first complete x1 repository suite",
        "failed_suites": [
            {"passed": 395, "total": 397, "counted_as_pass": False},
            {"passed": 396, "total": 399, "counted_as_pass": False},
        ],
        "cause": "Two immutable JSON files were frozen under opposite raw line-ending materializations while their normalized semantics remained stable.",
        "repair": "Before tests, verify exact normalized SHA-256 values and materialize only the declared LF or CRLF bytes in the owned checkout.",
        "shared_validator_changed": False,
        "historical_manifest_changed": False,
        "semantic_mutation_accepted": False,
        "prior_artifact_mutated": False,
        "new_phase_scoped_regression_tests": 3,
        "boundary": "This is an owned-checkout materialization step, not a repository-content rewrite, arbitrary hash alias, or scientific, security, or production assurance claim.",
    })

    dump_json(PHASE_ROOT / "workflow" / "route-preregistration.json", {
        "schema": "ghc.family.v643-v5.route-preregistration.v1",
        "phase": PHASE,
        "owner": "Tamar Vey",
        "route_state": "ACTIVE_SOLO",
        "active_owner": "Tamar Vey",
        "standby_or_recoverable": ["Orin Thale", "Sable Rook", "Ilyra Fen", "Eiren Kestrel", "Sylven Arc", "all other siblings"],
        "six_seat_order": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
        "terminal_successor": "Sylven Arc",
        "terminal_successor_phase": "v643-v6",
        "send_rule": "Send exactly one sanitized activation message to the existing task titled exactly Sylven Arc only after exact-final detached validation, clean push, and four-way remote equality. Tool acknowledgement changes PREPARED_NOT_SENT to SENT.",
        "route_stop_conditions": ["Hamish stops the route", "usage exhausted", "required task route unavailable", "exact safety or authority gate blocks progress"],
        "outbound_messages_before_terminal_gate": 0,
        "task_creation_authorized": False,
        "fork_authorized": False,
        "subagent_authorized": False,
        "private_route_material_allowed_in_artifacts": False,
    })
    dump_json(PHASE_ROOT / "validation" / "x1-operational-negatives.json", {
        "schema": "ghc.family.v643-v5.x1-operational-negatives.v1",
        "phase": PHASE,
        "count": len(X1_NEGATIVES),
        "negatives": X1_NEGATIVES,
        "all_failures_retained": True,
        "boundary": "Recovered failures remain negatives and are not counted as successful evidence runs.",
    })

    prereg = [
        "# Tamar Vey v643-v5 x1 preregistration",
        "",
        "This is the frozen x1 plan for exactly ten proposals. No expected disposition is a result. Allowed future result classes are completed, represented, open_gap, and exact_gate.",
        "",
        "Primary focus: GMUT Mind. THOS Body and Freed ID/CBR Heart remain explicitly addressed and bounded.",
        "",
    ]
    for proposal in PROPOSALS:
        prereg.extend([
            f"## {proposal['proposal_id']} — {proposal['title']}",
            "",
            f"- Hypothesis: {proposal['hypothesis']}",
            f"- Null or failure: {proposal['null_or_failure']}",
            f"- Approval class: {proposal['approval_class']}",
            f"- Execution lane: {proposal['execution_lane']}",
            f"- Official or primary source needs: {', '.join(proposal['authoritative_source_needs'])}",
            f"- Concrete artifacts: {', '.join(proposal['deliverables'])}",
            f"- Falsifier or acceptance gate: {proposal['test_falsifier_or_gate']}",
            f"- Rollback or recovery: {proposal['rollback_or_recovery']}",
            f"- Protected gates: {', '.join(proposal['protected_gates'])}",
            f"- Expected disposition, not a result: {proposal['expected_disposition']}",
            f"- Semantic distinction: {proposal['novelty_against_prior_chain']}",
            "",
        ])
    prereg.extend([
        "## Freeze boundary",
        "",
        "x2 cannot begin until this x1-only set is committed, pushed, clean, and equal across local, upstream, tracking, and a fresh live-remote read. The expected 6 completed, 2 represented, 1 open gap, and 1 exact gate distribution is a preregistered expectation only; evidence may force a more conservative allowed disposition.",
    ])
    dump_text(PHASE_ROOT / "x1-preregistration.md", "\n".join(prereg))
    dump_text(PHASE_ROOT / "wellbeing-check.md", WELLBEING)
    dump_text(PHASE_ROOT / "v643-v5-integrated-overview.md", OVERVIEW)


def staged_names() -> list[str]:
    return sorted(git_lines("diff", "--cached", "--name-only", "--diff-filter=ACMR"))


def finalise_validation(repository_passed: int, repository_total: int, finalize_staged: bool) -> None:
    phase_json = sorted(PHASE_ROOT.rglob("*.json"))
    parse_issues = []
    for path in phase_json:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            parse_issues.append(f"{rel(path)}: {exc}")

    proposals = json.loads((PHASE_ROOT / "x1-proposals.json").read_text(encoding="utf-8"))
    ledger = json.loads((PHASE_ROOT / "sources" / "source-ledger.json").read_text(encoding="utf-8"))
    collision = json.loads((PHASE_ROOT / "provenance" / "prior-proposal-collision-audit.json").read_text(encoding="utf-8"))
    privacy_path = PHASE_ROOT / "validation" / "x1-privacy-scan.json"
    privacy = json.loads(privacy_path.read_text(encoding="utf-8")) if privacy_path.exists() else {"valid": False, "hit_count": 1, "scanned_file_count": 0}

    expected = sorted([rel(path) for path in PHASE_ROOT.rglob("*") if path.is_file()] + X1_EXTERNAL_FILES)
    actual = staged_names() if finalize_staged else expected
    unexpected = sorted(set(actual) - set(expected))
    missing = sorted(set(expected) - set(actual))
    list_hash = hashlib.sha256(("\n".join(actual) + "\n").encode("utf-8")).hexdigest()
    required_fields = ["hypothesis", "null_or_failure", "approval_class", "execution_lane", "authoritative_source_needs", "deliverables", "test_falsifier_or_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"]

    checks: list[tuple[str, bool]] = [
        ("exactly ten proposals", proposals["proposal_count"] == 10 and len(PROPOSALS) == 10),
        ("190 inherited proposals", proposals["prior_frozen_proposal_count"] == 190),
        ("200 effective proposals", json.loads((PHASE_ROOT / "provenance" / "frozen-chain-proposal-index.json").read_text(encoding="utf-8"))["effective_record_count"] == 200),
        ("no exact duplicate IDs", not collision["exact_duplicate_ids"]),
        ("no exact duplicate titles", not collision["exact_duplicate_titles"]),
        ("overlap below threshold", collision["maximum_title_token_jaccard"] < collision["automatic_failure_threshold"]),
        ("semantic review passed", collision["semantic_review_passed"] is True),
        ("expected outcomes are not results", proposals["expected_counts_are_results"] is False),
        ("four exact outcome classes", proposals["outcome_classes"] == ["completed", "represented", "open_gap", "exact_gate"]),
        ("expected distribution", proposals["expected_disposition_counts"] == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}),
        ("130 sources", ledger["effective_source_count"] == 130),
        ("source status preservation", ledger["effective_status_counts"] == {"current": 52, "stable": 69, "draft": 6, "watch": 3}),
        ("all JSON parses", not parse_issues),
        ("privacy scan valid", privacy.get("valid") is True),
        ("repository suite complete", repository_passed == repository_total and repository_total > 0),
        ("x2 outcome ledger absent", not (PHASE_ROOT / "x2-proposal-ledger.json").exists()),
        ("x2 phase tool absent", not (ROOT / "scripts" / "ghc_family_v643_v5_evidence.py").exists()),
        ("no unexpected staged files", not unexpected),
        ("no missing staged files", not missing),
        ("owner footprint below threshold", len(expected) < 15000),
    ]
    for proposal in PROPOSALS:
        checks.append((f"{proposal['proposal_id']} unique ID", sum(item["proposal_id"] == proposal["proposal_id"] for item in PROPOSALS) == 1))
        checks.append((f"{proposal['proposal_id']} unique title", sum(item["title"] == proposal["title"] for item in PROPOSALS) == 1))
        for field in required_fields:
            checks.append((f"{proposal['proposal_id']} field {field}", bool(proposal.get(field))))
    issues = [name for name, passed in checks if not passed]

    dump_json(PHASE_ROOT / "validation" / "x1-exact-file-set.json", {
        "schema": "ghc.family.v643-v5.x1-exact-file-set.v1",
        "phase": PHASE,
        "owner": "Tamar Vey",
        "file_count": len(actual),
        "files": actual,
        "x2_implementation_file_count": 0,
        "x2_outcome_file_count": 0,
        "staged_name_list_sha256": list_hash,
        "unexpected_staged_files": unexpected,
        "missing_staged_files": missing,
        "owner_generated_file_count": len(expected),
        "owner_generated_file_threshold": 15000,
        "threshold_scope": "Tamar v643-v5 owner-generated files only",
        "under_threshold": len(expected) < 15000,
        "finalized_from_git_index": finalize_staged,
        "valid": not unexpected and not missing,
    })
    dump_json(PHASE_ROOT / "validation" / "x1-repository-test-receipt.json", {
        "schema": "ghc.family.v643-v5.x1-repository-tests.v1",
        "phase": PHASE,
        "runner": "scripts/ghc_family_repository_test_runner.py",
        "passed": repository_passed,
        "total": repository_total,
        "complete_suite": True,
        "valid": repository_passed == repository_total and repository_total > 0,
        "boundary": "Repository tests validate software behavior in this checkout; they do not establish scientific, participant, security, accessibility, legal, cultural, production, deployment, or Stage 20 claims.",
    })
    validation = {
        "schema": "ghc.family.v643-v5.x1-validation.v1",
        "phase": PHASE,
        "owner": "Tamar Vey",
        "valid": not issues,
        "checks_passed": len(checks) - len(issues),
        "checks_total": len(checks),
        "issues": issues,
        "proposal_count": 10,
        "prior_frozen_proposal_count": 190,
        "effective_frozen_proposal_count": 200,
        "maximum_title_token_jaccard": collision["maximum_title_token_jaccard"],
        "semantic_review_passed": collision["semantic_review_passed"],
        "expected_disposition_counts": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "expected_counts_are_results": False,
        "source_count": 130,
        "source_status_counts": {"current": 52, "stable": 69, "draft": 6, "watch": 3},
        "json_files_parsed": len(phase_json),
        "json_parse_issues": parse_issues,
        "privacy_scan": {"valid": privacy.get("valid") is True, "files_scanned": privacy.get("scanned_file_count", privacy.get("files_scanned", 0)), "issue_count": privacy.get("hit_count", len(privacy.get("issues", [])))},
        "x1_operational_negative_count": len(X1_NEGATIVES),
        "x2_implementation_files": 0,
        "x2_outcome_files": 0,
        "repository_tests": {"passed": repository_passed, "total": repository_total},
        "exact_staged_file_count": len(actual),
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
    dump_text(PHASE_ROOT / "validation" / "x1-validation.md", "\n".join([
        "# v643-v5 x1 validation",
        "",
        f"- Valid: {str(validation['valid']).lower()}",
        f"- Checks: {validation['checks_passed']}/{validation['checks_total']}",
        "- Proposals: 10 new / 190 inherited / 200 effective",
        "- Expected distribution, not results: 6 completed / 2 represented / 1 open gap / 1 exact gate",
        f"- Sources: 130 effective (52 current / 69 stable / 6 draft / 3 watch)",
        f"- JSON parsed: {validation['json_files_parsed']}",
        f"- Privacy scan: {validation['privacy_scan']['files_scanned']} files / {validation['privacy_scan']['issue_count']} issues",
        f"- Complete repository suite: {repository_passed}/{repository_total}",
        f"- Exact staged files: {len(actual)}; unexpected {len(unexpected)}; missing {len(missing)}",
        "- x2 implementation files: 0",
        "- x2 outcome files: 0",
        f"- Retained x1 operational negatives: {len(X1_NEGATIVES)}",
        f"- Owner-generated footprint: {len(expected)}/15000",
        "",
        "This receipt validates preregistration only. It is not outcome evidence, scientific confirmation, production approval, independent reproduction, or Stage 20 readiness.",
    ]))


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
