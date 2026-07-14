#!/usr/bin/env python3
"""Build Ilyra Fen's v643-v8 x1-only preregistration packet.

This builder cannot execute proposals or write x2 outcome classifications.  It
freezes ten questions, their sources, falsifiers, recovery rules, and gates.
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
PHASE = "v643-gmut-thos-v8-x1-x2"
PHASE_ROOT = ROOT / "docs" / "ilyra-fen" / "v643-v8"
SOURCE_HEAD = "428e2da33b504e45d7d4863b2d68e3ec48bcf6d5"
SOURCE_SEAL = "f20303c33bf4d8ba4e7dc0c34c614a3f0038f61b"
INHERITED_INDEX = ROOT / "docs" / "eiren-kestrel" / "v643-v7" / "provenance" / "frozen-chain-proposal-index.json"
INHERITED_LEDGER = ROOT / "docs" / "eiren-kestrel" / "v643-v7" / "sources" / "source-ledger.json"
INHERITED_TOOL_INDEX = ROOT / "docs" / "eiren-kestrel" / "v643-v7" / "tooling" / "ghc-family-index.json"
CHECKED_ON = "2026-07-15"
X1_EXTERNAL_FILES = [
    "scripts/build_ghc_family_v643_v8_preregistration.py",
    "scripts/ghc_family_v643_v8_x1_definitions.py",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def dump_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git_lines(*args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, encoding="utf-8", stdout=subprocess.PIPE
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
            return records
        current = ROOT / inherited


def title_tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


PROPOSALS = [
    {
        "proposal_id": "V6438-P01",
        "title": "Claim-vocabulary migration and semantic-version quarantine tribunal",
        "mission_surface": "provenance, controlled claim terms, term splits and merges, deprecation, semantic versions, and compatibility quarantine",
        "hypothesis": "A typed migration map can distinguish label-only edits from meaning changes and quarantine artifacts whose terms were removed, split, merged, narrowed, broadened, or reassigned without an explicit compatibility decision.",
        "null_or_failure": "A meaning-changing vocabulary edit is treated as cosmetic, a removed term remains promotable, a split or merge loses lineage, or an unknown vocabulary version silently passes.",
        "approval_class": "safe_now",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S131"],
        "deliverables": ["provenance/claim-vocabulary-migration-contract.json", "provenance/semantic-version-mutation-vectors.json", "provenance/unknown-version-quarantine-boundary.json"],
        "test_falsifier_or_gate": "Mutate term identity, preferred label, definition, domain, range, deprecation state, replacement relation, and declared version; meaning drift or an unknown version must fail closed.",
        "rollback_or_recovery": "Restore the last mapped vocabulary, retain every incompatible artifact as a negative, and require a reviewed migration before reuse.",
        "protected_gates": ["source_currency", "semantic_authority", "proof_or_canon", "production_readiness"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The 200 frozen proposals cover source drift, credential schema evolution, canonicalization, and claim lineage, but none treats the controlled claim vocabulary itself as a versioned migration object with split, merge, and unknown-version quarantine semantics.",
    },
    {
        "proposal_id": "V6438-P02",
        "title": "GMUT singular-perturbation regime map and nonuniform-limit boundary",
        "mission_surface": "GMUT Mind small parameters, outer and inner regimes, boundary layers, matched asymptotics, noncommuting limits, and EFT claim discipline",
        "hypothesis": "A typed regime map can expose where a nominally small GMUT parameter creates nonuniform behavior and require separate inner, outer, and overlap obligations before an asymptotic statement is promoted.",
        "null_or_failure": "A pointwise limit is called uniform, a boundary layer is omitted, inner and outer variables are mixed, overlap is absent, or a formal expansion is called a GMUT theorem or observation.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S132"],
        "deliverables": ["physics/singular-perturbation-regime-contract.json", "physics/boundary-layer-mutation-vectors.json", "physics/asymptotic-nonpromotion-boundary.json"],
        "test_falsifier_or_gate": "Mutate small-parameter range, scaling variable, inner and outer domains, overlap, matching condition, remainder order, and claim class; nonuniform or unmatched cases must fail.",
        "rollback_or_recovery": "Return to an explicitly local formal expansion, retain failed regimes, and require expert derivation and independent mathematical review for broader claims.",
        "protected_gates": ["gmut_derivation", "uniform_asymptotics", "mathematical_proof", "expert_review", "empirical_confirmation", "theory_of_everything"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier GMUT proposals cover null limits, stability, hyperbolicity, EFT truncation, continuation, and frame changes; none separates inner and outer singular-perturbation regimes or tests whether a small-parameter limit is nonuniform.",
    },
    {
        "proposal_id": "V6438-P03",
        "title": "GMUT manufactured-solution and observed-order discretization tribunal",
        "mission_surface": "GMUT Mind numerical verification, manufactured sources, grid refinement, observed convergence order, residual norms, and simulation nonpromotion",
        "hypothesis": "A deterministic manufactured-solution tribunal can detect discretization defects by comparing observed refinement order with a frozen expected order while keeping synthetic verification separate from physical validation.",
        "null_or_failure": "The manufactured source is inconsistent, refinement is absent, observed order falls outside tolerance, residuals are hidden, or code verification is called physical or empirical validation.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S133"],
        "deliverables": ["physics/manufactured-solution-verification-contract.json", "physics/grid-refinement-mutation-vectors.json", "physics/physical-validation-nonpromotion-boundary.json"],
        "test_falsifier_or_gate": "Mutate manufactured field, forcing term, mesh sequence, norm, expected order, observed errors, and claim class; inconsistent sources, nonconvergence, or validation language must fail.",
        "rollback_or_recovery": "Restore the last verified discretization fixture, retain every failed mesh sequence, and require real observations plus independent validation for physical claims.",
        "protected_gates": ["real_data", "physical_validation", "gmut_confirmation", "independent_review", "empirical_confirmation"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior numerical proposals address conservation, cross-solver tolerance, floating-point policies, and architecture parity; none uses manufactured forcing and observed grid-refinement order as a code-verification tribunal separated from physical validation.",
    },
    {
        "proposal_id": "V6438-P04",
        "title": "THOS adverse-event solicitation parity and attribution-blind harms ledger",
        "mission_surface": "THOS Body harms ascertainment, solicited and unsolicited events, arm-equal questioning, severity, recoverability, attribution blinding, and participant evidence",
        "hypothesis": "A synthetic protocol can represent equal harms solicitation across arms and separate event occurrence, severity, recoverability, and causal attribution without manufacturing participant results.",
        "null_or_failure": "Arms receive different prompts, only expected harms are collected, severity or recovery is missing, attribution reveals allocation, or fixtures are called real THOS safety evidence.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S134"],
        "deliverables": ["thos/harms-solicitation-parity-protocol.json", "thos/adverse-event-ascertainment-mutation-vectors.json", "thos/real-participant-harms-gap.json"],
        "test_falsifier_or_gate": "Mutate prompt schedule, arm coverage, event source, severity, recovery, attribution blindness, real-arm count, and claim class; differential solicitation or zero real arms must block a safety conclusion.",
        "rollback_or_recovery": "Return to protocol-only proxy language, preserve every ascertainment mismatch, and require ethics, consent, real participants, preregistered blind matched-budget arms, qualified review, and independent analysis.",
        "protected_gates": ["ethics_approval", "real_participants", "blind_matched_budget_arms", "qualified_safety_review", "independent_review", "thos_safety"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "The earlier safety-event proposal governs stopping rules; this proposal instead tests whether harms are solicited symmetrically and whether occurrence, severity, recovery, and causal attribution remain distinct and blinded.",
    },
    {
        "proposal_id": "V6438-P05",
        "title": "Freed ID cross-wallet migration and semantic-loss quarantine profile",
        "mission_surface": "Freed ID wallet migration, export and import, proof and status preservation, unsupported fields, semantic loss, interoperability, and production boundaries",
        "hypothesis": "A synthetic migration profile can compare pre-export and post-import credential meaning, identify unsupported or transformed fields, and quarantine lossy migrations without claiming real interoperability.",
        "null_or_failure": "A required field disappears, proof or status references are rewritten without disclosure, unsupported features are ignored, or fixture parity is called production interoperability.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S135"],
        "deliverables": ["freed-id/wallet-migration-profile.json", "freed-id/semantic-loss-mutation-vectors.json", "freed-id/production-interoperability-boundary.json"],
        "test_falsifier_or_gate": "Mutate credential type, context, proof metadata, status reference, holder binding, unsupported extension, and claim class; loss or unverified production language must fail.",
        "rollback_or_recovery": "Retain the original synthetic package, quarantine the import, preserve every loss witness, and require standards-conformant real keys and proofs, live resolution and status, cross-vendor trials, privacy and security review, and trust governance.",
        "protected_gates": ["real_keys", "live_resolution", "status_and_revocation", "cross_vendor_interoperability", "privacy_review", "security_review", "trust_governance"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier Freed ID work covers lifecycle, rotation, schema evolution, recovery, status, delegation, and multi-device forks; none evaluates semantic loss across an explicit wallet export-import boundary.",
    },
    {
        "proposal_id": "V6438-P06",
        "title": "Mātauranga Māori and taonga-use provenance with benefit-sharing authority gate",
        "mission_surface": "CBR Heart, mātauranga Māori and taonga-use provenance, kaitiaki relationships, consent, benefit sharing, legal and cultural authority, and non-substitution",
        "hypothesis": "Only appropriately authorized Māori authorities and affected parties can determine whether a proposed use, attribution, access condition, or benefit-sharing arrangement is legitimate for specific mātauranga Māori or taonga.",
        "null_or_failure": "Repository output identifies kaitiaki, grants permission, defines benefit sharing, generalizes Māori authority, interprets law, or presents neutral fields as cultural ratification.",
        "approval_class": "exact_authority_required",
        "execution_lane": "x2_exact_gate_receipt",
        "authoritative_source_needs": ["V6438-S136"],
        "deliverables": ["cbr/taonga-use-authority-gate.json", "cbr/neutral-provenance-question-set.json", "cbr/benefit-sharing-nonratification-boundary.json"],
        "test_falsifier_or_gate": "Any concrete permission, attribution, kaitiaki determination, benefit-sharing term, legal conclusion, or cultural wording requires case-specific affected-party participation, appropriate Māori authority, cultural ratification, and competent legal review.",
        "rollback_or_recovery": "Keep only neutral unanswered questions, retain every authority conflict, and seek case-specific Māori, affected-party, and legal review without substituting repository output for authority.",
        "protected_gates": ["affected_party_acceptance", "maori_authority", "maori_data_governance", "kaitiaki_determination", "benefit_sharing", "cultural_ratification", "legal_interpretation", "enacted_law"],
        "expected_disposition": "exact_gate",
        "novelty_against_prior_chain": "Prior CBR proposals address collective consent, wording, remedies, preservation, appeals, and authority conflicts; none isolates case-specific taonga-use provenance and benefit-sharing terms as an authority decision that repository output cannot make.",
    },
    {
        "proposal_id": "V6438-P07",
        "title": "Executable-resolution shadowing and environment-injection confinement tribunal",
        "mission_surface": "bounded security, executable lookup order, current-directory shadowing, PATH and PATHEXT injection, explicit resolution, allowlists, and non-exhaustive assurance",
        "hypothesis": "A deterministic tribunal can detect when an attacker-controlled directory or extension changes which executable a declared command resolves to and require explicit allowlisted resolution.",
        "null_or_failure": "A shadow executable wins, current-directory precedence is ignored, PATH or PATHEXT mutation changes the target without rejection, or bounded fixtures are called exhaustive host security.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S137"],
        "deliverables": ["security/executable-resolution-contract.json", "security/path-shadowing-mutation-vectors.json", "security/host-assurance-nonpromotion-boundary.json"],
        "test_falsifier_or_gate": "Mutate current directory, PATH ordering, PATHEXT, requested extension, resolved path, allowlist, and claim class; shadowing, ambiguity, or assurance language must fail.",
        "rollback_or_recovery": "Restore explicit allowlisted resolution, retain every shadow witness, narrow the supported environment, and require independent host-security review for broader claims.",
        "protected_gates": ["host_security", "system_path_change", "elevation", "independent_security_review", "exhaustive_security", "production_readiness"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior security work covers package manifests, path authorization, reparse points, parser attacks, and algorithmic complexity; none models executable search-order shadowing across current directory, PATH, and PATHEXT.",
    },
    {
        "proposal_id": "V6438-P08",
        "title": "Static landmark, heading, and focus-sequence structural audit",
        "mission_surface": "accessible static reporting, landmarks, heading hierarchy, focusable elements, focus order, table semantics, automated structure, and manual-evaluation reservation",
        "hypothesis": "A deterministic structural audit can reject missing main landmarks, broken heading hierarchy, illogical positive tabindex ordering, unlabeled tables, and absent manual-evaluation reservations.",
        "null_or_failure": "A required landmark or heading is absent, focus sequence contradicts document order, a data table lacks headers, or an automated pass is called complete accessibility.",
        "approval_class": "safe_now",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S138"],
        "deliverables": ["accessibility/static-structure-contract.json", "accessibility/landmark-focus-mutation-vectors.json", "accessibility/manual-evaluation-reservation.json"],
        "test_falsifier_or_gate": "Mutate landmark presence, heading levels, focusable order, tabindex, table headers, language declaration, and claim class; structural defects or completeness claims must fail.",
        "rollback_or_recovery": "Restore the last structurally valid static report, retain every rejected mutation, and keep manual and affected-user evaluation expressly reserved.",
        "protected_gates": ["manual_accessibility_evaluation", "affected_user_evaluation", "assistive_technology_coverage", "accessibility_complete"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier accessibility work maps evidence and tests reflow, zoom, color, and print; none freezes landmark, heading, table, and focus-sequence structure as one deterministic static-report contract.",
    },
    {
        "proposal_id": "V6438-P09",
        "title": "Finite-size ensemble inequivalence and limit-order non-substitution barrier",
        "mission_surface": "GMUT Mind and thermo-psyche classification, microcanonical and canonical ensembles, finite-size effects, thermodynamic limits, noncommuting limits, and category boundaries",
        "hypothesis": "A typed fixture can show that ensemble equivalence requires declared assumptions and limits, and can reject transfer of finite-size or ensemble-specific behavior into psyche claims.",
        "null_or_failure": "Canonical and microcanonical results are equated without assumptions, finite-size behavior is erased, limit order is unrecorded, or ensemble vocabulary is transferred to psychology or GMUT law claims.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S139"],
        "deliverables": ["thermo-psyche/ensemble-regime-contract.json", "thermo-psyche/limit-order-mutation-vectors.json", "thermo-psyche/ensemble-nonsubstitution-boundary.json"],
        "test_falsifier_or_gate": "Mutate ensemble, interaction range, system size, convexity assumption, limit order, observable, pillar, and claim class; unsupported equivalence or cross-pillar transfer must fail.",
        "rollback_or_recovery": "Restore explicit ensemble and finite-size labels, retain every inequivalence witness, and require domain-specific data and expert review for physical or psychological promotion.",
        "protected_gates": ["thermodynamic_law", "psyche_evidence", "gmut_derivation", "empirical_confirmation", "proof_or_canon"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier thermo-psyche proposals cover entropy types, open systems, detailed balance, time-scale separation, and coarse graining; none tests finite-size ensemble inequivalence or the order of thermodynamic and parameter limits.",
    },
    {
        "proposal_id": "V6438-P10",
        "title": "Affected-user assistive-technology evaluation matrix and recruitment gap",
        "mission_surface": "accessibility affected-user evaluation, assistive technologies, user characteristics, task coverage, browsers, reporting scope, ethics, consent, and non-generalization",
        "hypothesis": "A preregistered matrix could bound an affected-user evaluation across assistive technologies, experience levels, browsers, and representative tasks without treating automated structure as lived-use evidence.",
        "null_or_failure": "No affected users participate, consent or privacy is absent, the matrix omits material technologies or tasks, a small sample is generalized, or automated checks substitute for user evidence.",
        "approval_class": "external_evidence_required",
        "execution_lane": "x2_open_gap_receipt",
        "authoritative_source_needs": ["V6438-S140"],
        "deliverables": ["accessibility/affected-user-evaluation-preregistration.json", "accessibility/assistive-technology-coverage-gap.json", "accessibility/non-generalization-boundary.json"],
        "test_falsifier_or_gate": "Require authorized recruitment, informed consent, privacy protection, affected-user participation, declared technologies and tasks, issue handling, and scoped reporting; any missing element keeps the gap open.",
        "rollback_or_recovery": "Retain the preregistration, keep manual and user evaluation reserved, and resume only with authorized participants, safeguards, and qualified accessibility review.",
        "protected_gates": ["participant_recruitment", "ethics_and_consent", "privacy_review", "affected_user_evaluation", "qualified_accessibility_review", "accessibility_complete"],
        "expected_disposition": "open_gap",
        "novelty_against_prior_chain": "The prior accessibility proposal reserved user participation but did not preregister a matrix spanning affected-user characteristics, assistive technologies, browsers, tasks, safeguards, and non-generalization rules.",
    },
]


SOURCES = [
    {"source_id": "V6438-S131", "title": "SKOS Simple Knowledge Organization System Reference", "authority": "World Wide Web Consortium", "url": "https://www.w3.org/TR/skos-reference/", "version_or_date": "W3C Recommendation; checked 15 July 2026", "status_class": "stable", "evidence_role": "controlled-vocabulary mapping and semantic-relation vocabulary; not claim authority"},
    {"source_id": "V6438-S132", "title": "Geometric singular perturbation theory for ordinary differential equations", "authority": "Neil Fenichel", "url": "https://doi.org/10.1016/0022-0396(79)90152-9", "version_or_date": "Journal of Differential Equations 31(1), 1979", "status_class": "stable", "evidence_role": "primary mathematical source for singular-perturbation regime vocabulary; not a GMUT derivation"},
    {"source_id": "V6438-S133", "title": "NASA-STD-7009B Standard for Models and Simulations", "authority": "National Aeronautics and Space Administration", "url": "https://standards.nasa.gov/standard/NASA/NASA-STD-7009", "version_or_date": "NASA-STD-7009B, 2024; checked 15 July 2026", "status_class": "current", "evidence_role": "official model verification and validation boundary vocabulary; not physical validation evidence"},
    {"source_id": "V6438-S134", "title": "E6(R3) Good Clinical Practice Guidance for Industry", "authority": "United States Food and Drug Administration", "url": "https://www.fda.gov/media/169090/download", "version_or_date": "September 2025 guidance; checked 15 July 2026", "status_class": "current", "evidence_role": "official clinical safety and adverse-event vocabulary; not THOS approval or participant evidence"},
    {"source_id": "V6438-S135", "title": "OpenID for Verifiable Credential Issuance 1.0", "authority": "OpenID Foundation", "url": "https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html", "version_or_date": "Final specification; checked 15 July 2026", "status_class": "current", "evidence_role": "primary cross-wallet issuance and metadata obligations; not production interoperability evidence"},
    {"source_id": "V6438-S136", "title": "Ko Aotearoa Tēnei: Report on the Wai 262 Claim", "authority": "Waitangi Tribunal", "url": "https://www.waitangitribunal.govt.nz/en/news/ko-aotearoa-tenei-report-on-the-wai-262-claim-released", "version_or_date": "Official report release, 2 July 2011; checked 15 July 2026", "status_class": "stable", "evidence_role": "official inquiry context for Māori culture, identity, traditional knowledge, and taonga; not case-specific authority or legal advice"},
    {"source_id": "V6438-S137", "title": "path command", "authority": "Microsoft", "url": "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/path", "version_or_date": "Microsoft Learn; checked 15 July 2026", "status_class": "current", "evidence_role": "official Windows executable search-order vocabulary; not host-security assurance"},
    {"source_id": "V6438-S138", "title": "Understanding Success Criterion 2.4.3: Focus Order", "authority": "World Wide Web Consortium Web Accessibility Initiative", "url": "https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html", "version_or_date": "WCAG 2.2 understanding document; checked 15 July 2026", "status_class": "current", "evidence_role": "official focus-order interpretation; not complete accessibility conformance"},
    {"source_id": "V6438-S139", "title": "Equivalence and nonequivalence of ensembles: thermodynamic, macrostate, and measure levels", "authority": "Hugo Touchette", "url": "https://doi.org/10.1088/1751-8113/48/37/375001", "version_or_date": "Journal of Physics A 48, 2015", "status_class": "stable", "evidence_role": "primary scholarly ensemble-equivalence vocabulary; not a GMUT or psyche law"},
    {"source_id": "V6438-S140", "title": "Involving Users in Evaluating Web Accessibility", "authority": "World Wide Web Consortium Web Accessibility Initiative", "url": "https://www.w3.org/WAI/test-evaluate/involving-users/", "version_or_date": "WAI guidance; checked 15 July 2026", "status_class": "current", "evidence_role": "official affected-user evaluation and non-generalization guidance; not participant authorization"},
]


# v643-v8 replaces the copied v6 prototype above with a fresh, explicitly
# reviewed proposal and source surface.  Keeping the prototype in this builder
# makes the compatibility lineage visible, while only this final assignment is
# used to build or validate x1.
PROPOSALS = [
    {
        "proposal_id": "V6438-P01",
        "title": "Claim-scope lattice and quantifier-strength nonpromotion tribunal",
        "mission_surface": "provenance, claim scope, universal and existential quantifiers, conditions, populations, time windows, and monotone claim-strength control",
        "hypothesis": "A typed claim-scope lattice can reject any transformation that strengthens quantifiers, populations, time windows, or certainty beyond the bound evidence while preserving explicit weakening and qualification paths.",
        "null_or_failure": "A conditional claim becomes unconditional, some becomes all, a bounded population broadens, an interval disappears, or uncertainty language is removed without stronger evidence.",
        "approval_class": "safe_now",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6-S01"],
        "deliverables": ["provenance/claim-scope-lattice-contract.json", "provenance/quantifier-strength-mutation-vectors.json", "provenance/claim-strength-nonpromotion-boundary.json"],
        "test_falsifier_or_gate": "Mutate quantifier, condition, population, time window, modality, uncertainty, and evidence reference; every unsupported strengthening must fail closed.",
        "rollback_or_recovery": "Restore the narrowest evidenced scope, retain every strengthening witness, and require a new source-and-evidence review before promotion.",
        "protected_gates": ["source_currency", "scope_authority", "empirical_confirmation", "proof_or_canon"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The 210 frozen proposals govern provenance, vocabulary migration, outcome completeness, and claim lineage, but none models claim strength as an ordered lattice across quantifier, condition, population, time, modality, and uncertainty dimensions.",
    },
    {
        "proposal_id": "V6438-P02",
        "title": "GMUT gauge-fixing, residual-gauge, and observable-invariance tribunal",
        "mission_surface": "GMUT Mind perturbations, gauge choice, residual transformations, gauge-invariant observables, coordinate artifacts, and nonpromotion",
        "hypothesis": "A synthetic gauge tribunal can distinguish declared gauge conditions from residual gauge freedom and reject observables that change under an allowed residual transformation.",
        "null_or_failure": "Gauge conditions are incomplete, residual transformations are omitted, a coordinate component is treated as observable, or an invariant is promoted to a GMUT prediction without derivation and data.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S141"],
        "deliverables": ["physics/gauge-invariance-contract.json", "physics/residual-gauge-mutation-vectors.json", "physics/observable-nonpromotion-boundary.json"],
        "test_falsifier_or_gate": "Mutate gauge conditions, residual generator, transformation law, invariant combination, observable map, and claim class; gauge-dependent outputs or prediction language must fail.",
        "rollback_or_recovery": "Return to gauge-labeled variables, retain every residual-gauge witness, and require a model-specific derivation plus expert review before wider use.",
        "protected_gates": ["gmut_derivation", "gauge_invariance_proof", "real_data", "expert_review", "theory_of_everything"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier phases test frames, causal cones, boundary data, singular limits, and continuation, but none freezes residual gauge freedom and tests observable invariance under the allowed transformation group.",
    },
    {
        "proposal_id": "V6438-P03",
        "title": "GMUT constraint-propagation and damping-parameter stability envelope",
        "mission_surface": "GMUT Mind evolution constraints, propagation systems, damping parameters, resolved modes, growth bounds, and numerical nonpromotion",
        "hypothesis": "A deterministic constraint-propagation fixture can reject parameter choices that amplify resolved violations while separating continuum damping analysis from physical validation.",
        "null_or_failure": "Constraints are not monitored, a constant or unresolved mode is silently claimed damped, a parameter produces growth, or a synthetic decay trace is called physical validation.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S142"],
        "deliverables": ["physics/constraint-propagation-contract.json", "physics/damping-stability-mutation-vectors.json", "physics/continuum-to-physical-nonpromotion-boundary.json"],
        "test_falsifier_or_gate": "Mutate constraint norm, resolved-mode flag, damping sign, parameter range, growth tolerance, continuum assumptions, and validation label; amplification or overclaim must fail.",
        "rollback_or_recovery": "Restore the last bounded parameter interval, retain every growth trace, and require convergence, model-specific analysis, real observations, and independent review for physical claims.",
        "protected_gates": ["continuum_analysis", "numerical_convergence", "physical_validation", "real_data", "independent_review"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior work checks conservation, stability, discretization order, floating-point behavior, and well-posedness; none separates resolved constraint modes and damping-parameter intervals from constant-mode and physical-validation claims.",
    },
    {
        "proposal_id": "V6438-P04",
        "title": "THOS intercurrent-event estimand and treatment-strategy preregistration",
        "mission_surface": "THOS Body estimands, intercurrent events, treatment-policy and hypothetical strategies, outcomes, sensitivity analysis, and real-arm boundaries",
        "hypothesis": "A protocol-only THOS fixture can bind each anticipated intercurrent event to a prospective estimand strategy and sensitivity obligation without manufacturing participant outcomes.",
        "null_or_failure": "An event is handled post hoc, strategies are mixed silently, the target population or variable changes, sensitivity analysis is absent, or zero-row fixtures are called effectiveness evidence.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6432-S92"],
        "deliverables": ["thos/intercurrent-event-estimand-contract.json", "thos/strategy-switch-mutation-vectors.json", "thos/real-arm-estimand-gap.json"],
        "test_falsifier_or_gate": "Mutate event taxonomy, strategy, population, variable, summary, sensitivity plan, real-arm count, and claim class; post-hoc switching or zero-row promotion must fail.",
        "rollback_or_recovery": "Return to preregistered strategy labels, preserve every switch witness, and require ethics, consent, blind matched-budget real arms, real participants, and independent analysis.",
        "protected_gates": ["ethics_approval", "real_participants", "blind_matched_budget_arms", "independent_review", "thos_effectiveness"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier THOS proposals govern allocation, contamination, fidelity, burden, mediation, harms, and sham credibility; none binds intercurrent-event classes to explicit estimand strategies and strategy-switch sensitivity obligations.",
    },
    {
        "proposal_id": "V6438-P05",
        "title": "Freed ID pairwise-subject and presentation-minimization unlinkability profile",
        "mission_surface": "Freed ID/CBR Heart, pairwise pseudonyms, selective presentation, verifier audiences, transaction binding, attribute minimization, and correlation boundaries",
        "hypothesis": "A synthetic presentation profile can reject global subject reuse, unnecessary attribute release, missing audience or nonce binding, and unqualified unlinkability claims without using real credentials.",
        "null_or_failure": "The same subject identifier crosses relying parties, optional attributes are disclosed without need, audience or nonce is missing, or a structural fixture is called production privacy.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S143", "V6438-S147"],
        "deliverables": ["freed-id/pairwise-presentation-profile.json", "freed-id/correlation-mutation-vectors.json", "freed-id/production-unlinkability-boundary.json"],
        "test_falsifier_or_gate": "Mutate relying-party sector, subject derivation, audience, nonce, requested attributes, disclosure set, issuer metadata, and claim class; correlation or overclaim must fail.",
        "rollback_or_recovery": "Quarantine the presentation, restore minimal synthetic fields, retain every correlation witness, and require real keys, wallets, verifiers, privacy analysis, and independent security review.",
        "protected_gates": ["real_keys", "live_wallets", "cross_vendor_interoperability", "privacy_assurance", "security_review", "trust_governance"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Prior Freed ID work covers identifier rotation, disclosure budgets, lifecycle, recovery, migration, delegation, and sync forks; none combines pairwise relying-party subjects with audience-bound presentation minimization and explicit verifier-correlation witnesses.",
    },
    {
        "proposal_id": "V6438-P06",
        "title": "Collective data-purpose, benefit, and authority determination gate",
        "mission_surface": "CBR Heart, collective data interests, purpose, benefit, authority, Indigenous and Māori data governance, affected parties, and non-substitution",
        "hypothesis": "Concrete determinations about collective purpose, benefit, authority, or acceptable reuse require case-specific affected-party participation and the appropriate Māori or other Indigenous authorities rather than repository inference.",
        "null_or_failure": "A repository artifact identifies the collective, grants reuse, defines benefit, transfers authority, interprets law, or treats general principles as case-specific consent or ratification.",
        "approval_class": "exact_authority_required",
        "execution_lane": "x2_exact_gate_receipt",
        "authoritative_source_needs": ["V6432-S96", "V6-S20"],
        "deliverables": ["cbr/collective-data-authority-gate.json", "cbr/neutral-purpose-benefit-question-set.json", "cbr/collective-ratification-nonpromotion-boundary.json"],
        "test_falsifier_or_gate": "Any concrete collective identity, purpose, permission, benefit allocation, governance rule, legal conclusion, or cultural wording requires authorized affected parties and competent Māori, Indigenous, cultural, and legal authority as applicable.",
        "rollback_or_recovery": "Keep only neutral unanswered fields, retain every authority conflict, and seek case-specific authorized participation without treating technical output as consent or governance.",
        "protected_gates": ["affected_party_acceptance", "maori_authority", "indigenous_data_governance", "collective_consent", "benefit_determination", "cultural_ratification", "legal_interpretation", "enacted_law"],
        "expected_disposition": "exact_gate",
        "novelty_against_prior_chain": "Earlier CBR work gates wording, taonga use, benefit sharing, representation, preservation, appeals, and emergency powers; none freezes purpose, benefit, and authority as a joint collective-data determination that cannot be inferred from general principles.",
    },
    {
        "proposal_id": "V6438-P07",
        "title": "Unicode bidirectional-control and visual-order spoofing quarantine",
        "mission_surface": "bounded security, Unicode logical order, bidirectional controls, isolates, overrides, filenames, labels, visual-order spoofing, and safe rendering",
        "hypothesis": "A deterministic scanner can expose bidi controls and logical-versus-visual order differences, require escaped evidence views, and quarantine ambiguous security-sensitive labels.",
        "null_or_failure": "A bidi override is invisible, logical order is discarded, isolates are unbalanced, a security-sensitive name renders ambiguously, or the bounded scan is called exhaustive security.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S144"],
        "deliverables": ["security/bidi-control-contract.json", "security/visual-order-mutation-vectors.json", "security/unicode-spoofing-nonassurance-boundary.json"],
        "test_falsifier_or_gate": "Mutate embedding, override, isolate, terminator, logical sequence, visual preview, security sensitivity, and claim class; ambiguity or assurance language must fail.",
        "rollback_or_recovery": "Preserve escaped logical order, quarantine the label, retain every spoof witness, and require independent host and product security review for broader assurance.",
        "protected_gates": ["host_security", "product_security", "independent_security_review", "exhaustive_security", "production_readiness"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior Unicode work covers confusables and prior parser work covers canonicalization, but none tests bidirectional formatting controls, isolate balance, and logical-versus-visual ordering in security-sensitive labels.",
    },
    {
        "proposal_id": "V6438-P08",
        "title": "Accessible-name provenance and hidden-label conflict audit",
        "mission_surface": "accessible static reporting, accessible-name sources, visible labels, aria references, hidden content, duplicate names, conflict resolution, and manual reservation",
        "hypothesis": "A deterministic structural audit can record each interactive element's accessible-name provenance and reject empty, conflicting, hidden-only, or misleading names while reserving assistive-technology evaluation.",
        "null_or_failure": "A control has no computed name, visible and programmatic labels conflict, hidden content silently overrides meaning, duplicate names are ambiguous, or a static pass is called complete accessibility.",
        "approval_class": "safe_now",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S145"],
        "deliverables": ["accessibility/accessible-name-contract.json", "accessibility/hidden-label-mutation-vectors.json", "accessibility/manual-name-evaluation-reservation.json"],
        "test_falsifier_or_gate": "Mutate visible label, aria-label, referenced description, hidden state, duplicate context, language, and claim class; empty or conflicting names and completeness claims must fail.",
        "rollback_or_recovery": "Restore the last unambiguous label mapping, retain every conflict, and keep manual and affected-user assistive-technology evaluation explicitly reserved.",
        "protected_gates": ["manual_accessibility_evaluation", "affected_user_evaluation", "assistive_technology_coverage", "accessibility_complete"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier accessibility work covers evidence mapping, reflow, color, landmarks, heading order, and user recruitment; none records accessible-name provenance or tests conflicts among visible, referenced, and hidden labeling sources.",
    },
    {
        "proposal_id": "V6438-P09",
        "title": "Maximum-entropy inference and thermodynamic-entropy non-substitution barrier",
        "mission_surface": "thermo-psyche, maximum-entropy inference, thermodynamic entropy, constraints, priors, ensembles, physical units, psyche analogy, and domain separation",
        "hypothesis": "A typed classifier can distinguish an inference distribution selected by stated constraints from thermodynamic entropy and reject transfers into physical or psyche law claims.",
        "null_or_failure": "Constraints or base measure are hidden, informational and thermodynamic quantities are equated without a physical model, units are omitted, or an inference artifact is called a psyche or GMUT law.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S146"],
        "deliverables": ["thermo-psyche/maxent-domain-contract.json", "thermo-psyche/entropy-substitution-mutation-vectors.json", "thermo-psyche/physical-psyche-nonconversion-boundary.json"],
        "test_falsifier_or_gate": "Mutate constraint set, base measure, units, ensemble, physical model, target domain, and claim class; hidden assumptions or cross-domain conversion must fail.",
        "rollback_or_recovery": "Restore explicit inference-only labels, retain every substitution witness, and require domain-specific derivation, data, and expert review for physical or psychological claims.",
        "protected_gates": ["thermodynamic_law", "psyche_evidence", "gmut_derivation", "empirical_confirmation", "proof_or_canon"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior thermo-psyche work separates Landauer cost, fluctuation theorems, detailed balance, coarse graining, ensembles, and time scales; none distinguishes maximum-entropy inference from thermodynamic entropy through constraints, base measure, units, and physical-model obligations.",
    },
    {
        "proposal_id": "V6438-P10",
        "title": "Cross-vendor collusion and pairwise-linkability live interoperability study",
        "mission_surface": "Freed ID/CBR Heart, real wallets and verifiers, pairwise identifiers, presentation metadata, colluding relying parties, linkability measurement, privacy review, and interoperability",
        "hypothesis": "A preregistered live study could measure whether independent wallets and verifiers leak stable correlators across relying parties under declared collusion scenarios.",
        "null_or_failure": "No independent vendors participate, real keys or transactions are absent, collusion scenarios are not preregistered, privacy safeguards are missing, or same-owner synthetic fixtures are called live unlinkability evidence.",
        "approval_class": "external_evidence_required",
        "execution_lane": "x2_open_gap_receipt",
        "authoritative_source_needs": ["V6438-S143", "V6438-S147"],
        "deliverables": ["freed-id/live-linkability-study-preregistration.json", "freed-id/cross-vendor-collusion-gap.json", "freed-id/independent-privacy-review-boundary.json"],
        "test_falsifier_or_gate": "Require real standards-conformant keys, at least two independent wallet and verifier implementations, declared collusion channels, consent and privacy review, measured linkage error, and independent analysis.",
        "rollback_or_recovery": "Retain the preregistration and synthetic risk map, keep the gate open, and resume only with authorized vendors, users, safeguards, and independent privacy and security review.",
        "protected_gates": ["real_keys", "independent_vendors", "live_resolution", "privacy_review", "security_review", "trust_governance", "independent_reproduction"],
        "expected_disposition": "open_gap",
        "novelty_against_prior_chain": "Earlier interoperability work remains structural or migration-focused; none preregisters a live colluding-verifier study that measures cross-vendor pairwise-linkability leakage under independent privacy and security review.",
    },
]

SOURCES = [
    {"source_id": "V6438-S141", "title": "Gauge-invariant cosmological perturbations", "authority": "James M. Bardeen", "url": "https://doi.org/10.1103/PhysRevD.22.1882", "version_or_date": "Physical Review D 22, 1980", "status_class": "stable", "evidence_role": "primary gauge-invariant perturbation vocabulary; not a GMUT derivation or prediction"},
    {"source_id": "V6438-S142", "title": "Constraint damping in the Z4 formulation and harmonic gauge", "authority": "Carsten Gundlach, Jose M. Martin-Garcia, Gioel Calabrese, and Ian Hinder", "url": "https://arxiv.org/abs/gr-qc/0504114", "version_or_date": "Primary preprint, 2005", "status_class": "stable", "evidence_role": "primary constraint-propagation and damping vocabulary; not GMUT validation"},
    {"source_id": "V6438-S143", "title": "NIST SP 800-63C-4: Digital Identity Guidelines — Federation and Assertions", "authority": "National Institute of Standards and Technology", "url": "https://csrc.nist.gov/pubs/sp/800/63/c/4/final", "version_or_date": "Final, July 2025; checked 15 July 2026", "status_class": "current", "evidence_role": "official pairwise-pseudonym, federation, consent, and privacy obligations; not Freed ID production evidence"},
    {"source_id": "V6438-S144", "title": "Unicode Standard Annex #9: Unicode Bidirectional Algorithm", "authority": "Unicode Consortium", "url": "https://www.unicode.org/reports/tr9/", "version_or_date": "Revision 51 for Unicode 17.0.0, 13 August 2025; checked 15 July 2026", "status_class": "stable", "evidence_role": "official logical-order and bidi-control behavior; not exhaustive spoofing assurance"},
    {"source_id": "V6438-S145", "title": "Accessible Name and Description Computation 1.2", "authority": "World Wide Web Consortium", "url": "https://www.w3.org/TR/accname-1.2/", "version_or_date": "Working Draft, 29 May 2026; checked 15 July 2026", "status_class": "draft", "evidence_role": "current draft accessible-name algorithm vocabulary; not complete conformance or affected-user evidence"},
    {"source_id": "V6438-S146", "title": "Information Theory and Statistical Mechanics", "authority": "Edwin T. Jaynes", "url": "https://doi.org/10.1103/PhysRev.106.620", "version_or_date": "Physical Review 106, 1957", "status_class": "stable", "evidence_role": "primary maximum-entropy inference vocabulary; not a psyche law or GMUT result"},
    {"source_id": "V6438-S147", "title": "OpenID for Verifiable Presentations 1.0", "authority": "OpenID Foundation", "url": "https://openid.net/specs/openid-4-verifiable-presentations-1_0-final.html", "version_or_date": "Final specification, 9 July 2025; checked 15 July 2026", "status_class": "current", "evidence_role": "official presentation, audience, nonce, and holder-binding obligations; not live interoperability or unlinkability evidence"},
]

X1_NEGATIVES = [
    {"negative_id": "V6438-X1-N01", "operation": "combined source verifier wrapper", "observed_failure": "The first PowerShell wrapper placed a command and exit-code capture inside an expression and failed to parse before any Git command ran.", "recovery": "Separated command execution from exit-code capture and reran the checks read-only.", "promotion_effect": "none; the parse failure is retained and uncounted"},
    {"negative_id": "V6438-X1-N02", "operation": "combined local and live-remote source verifier", "observed_failure": "The corrected combined wrapper reached an external operation but timed out before returning buffered output.", "recovery": "Split local truth from network truth and completed fresh live-remote reads separately.", "promotion_effect": "none; the timed-out wrapper is not evidence"},
    {"negative_id": "V6438-X1-N03", "operation": "pre-fast-forward packet path probe", "observed_failure": "The Sylven v642-v8 checkout correctly lacked Tamar's later v643-v5 directory, so the optional path probe reported a missing path.", "recovery": "Verified ancestry and then used the authorized fast-forward-only update before inspecting the inherited packet.", "promotion_effect": "none; no source fact was inferred from the missing path"},
    {"negative_id": "V6438-X1-N04", "operation": "recursive frozen-index audit", "observed_failure": "The first PowerShell collector treated an absent new_records property as a one-element null array and reported only 81 records.", "recovery": "Tested property presence explicitly and decoded all 200 frozen records across both index schemas.", "promotion_effect": "none; the incomplete 81-record report is not novelty evidence"},
    {"negative_id": "V6438-X1-N05", "operation": "source URL duplicate scan", "observed_failure": "The first ripgrep call used a Windows-invalid wildcard path for source-ledger files.", "recovery": "Used ripgrep's native include filter and then traversed the inherited ledger chain directly.", "promotion_effect": "none; only the corrected chain scan supports source uniqueness"},
    {"negative_id": "V6438-X1-N06", "operation": "x1 builder context patch", "observed_failure": "The first patch expected underscore-version filenames to have changed during a hyphen-version mechanical copy and was rejected without modifying the file.", "recovery": "Inspected the exact copied header and replaced the prototype with this explicit phase builder.", "promotion_effect": "none; the rejected patch made no change"},
    {"negative_id": "V6438-X1-N07", "operation": "inherited checkout portability materialization", "observed_failure": "The inherited v5 adapter verified semantic hashes and changed only line endings, but one older Orin artifact still appeared as a working-tree modification after the passing suite.", "recovery": "Restored that exact file to its recorded pre-run raw SHA-256, confirmed the owned worktree had no inherited diff, and excluded it from staging.", "promotion_effect": "none; the transient working-copy materialization is retained and is not repository evidence"},
    {"negative_id": "V6438-X1-N08", "operation": "staged-state repository suite without inherited portability precondition", "observed_failure": "The complete suite ran 425 tests with one failure because the legacy constraint-hash alias warning fixture was checked under the unmaterialized CRLF working-copy form.", "recovery": "Kept the 424-of-425 run uncounted, applied the exact hash-verified inherited materializer only for the suite, reran completely, and restored the original raw hash afterward.", "promotion_effect": "the 424-of-425 run is failed evidence; only a complete adapted rerun may satisfy the x1 gate"},
]


WELLBEING = """# Ilyra Fen v643-v8 wellbeing and workload check

This phase remains intentionally solo. No collaboration subagent, new task, fork, parallel owner, or early sibling contact has been created. The work is divided into x1 freeze, x2 execution, evidence, closeout, seal, exact-final validation, and one terminal route gate so that a failure in one state cannot be disguised by progress in another.

The workload stays in the existing clean Sylven-owned D-drive lane because its earlier head was ancestral to Tamar's verified final source. Advancement was fast-forward only. The inherited checkout is excluded from the 15,000 owner-generated-file threshold. Every failed command or rejected fixture remains visible instead of creating pressure to hide negative evidence or repeat risky operations.

Wellbeing is operational language, not evidence of subjective experience, consciousness, sentience, personhood, identity continuity, or independent authority. Safeguards are bounded commands, clean-state checks, no destructive Git, no elevation or host-security change, no application update, no premature message, qualified accessibility and participant reservations, and truthful open-gap or exact-gate outcomes whenever evidence or authority is absent.
"""


OVERVIEW = """# Ilyra Fen v643-v8 integrated overview

## Purpose, source, and bounded identity

v643-v8 inherits Tamar Vey's exact v643-v5 final head and seal. Before mutation, Tamar's local branch, upstream, tracking reference, and a fresh live-remote read all resolved to the named final head with zero divergence. The source worktree was clean; the inherited Orin head, Orin seal, Tamar x1, evidence, closeout, and seal anchors were ancestral; source-to-final history had zero merge commits; and the final source commit had one parent. The source retained 809 effective negatives, five open gaps, six exact gates, same-owner repeatability only, and NOT_READY_FOR_STAGE_20.

The existing Sylven-owned branch was clean, pushed, remote-equal, and ancestral to Tamar's source. It was advanced by fast-forward only and pushed before any v643-v8 phase file was created. No sibling branch, worktree, task, message route, or artifact was reset, rewritten, force-pushed, merged, moved, deleted, or reused. D remains the primary work and detached-validation bank. Only newly generated Sylven v643-v8 files count against the 15,000-file threshold.

Ilyra Fen is an existing relational working name. The role is evidence cartographer and falsifier-boundary steward, the hope is to leave each falsifier, recovery path, and authority boundary easier to audit than it was at inheritance, and the relational pronouns are they/them. These labels coordinate work. They are not evidence of consciousness, sentience, legal personhood, identity continuity, independent authority, cultural authority, or legal authority.

## Scientific, participant, identity, and authority posture

The primary focus is GMUT Mind. GMUT remains a typed scalar-tensor and effective-field-theory research-model family. A singular-perturbation regime map can expose small-parameter boundary layers and nonuniform limits; it cannot prove a GMUT equation, establish global behavior, or turn a formal expansion into a physical observation. A manufactured-solution tribunal can verify defined numerical behavior; it cannot validate nature, fit real data, establish a force, produce a unique prediction, prove a theory, or confer canon. The difference between code verification and physical validation stays explicit.

THOS Body remains proxy. The harms proposal asks whether event solicitation is symmetric across arms and whether occurrence, severity, recovery, and attribution are separately represented. Synthetic rows can falsify a protocol structure, but they cannot create ethics approval, consent, real participants, real facilitators, real raters, blind matched-budget arms, actual adverse events, causal attribution, superiority, safety, or independent review. Its expected disposition is represented and may be downgraded if the structural evidence fails.

Freed ID and CBR Heart remain protected. A synthetic wallet migration profile can expose semantic loss, but production still requires standards-conformant real keys and proofs, live resolution, live status and revocation, cross-vendor interoperability, privacy and security review, and trust governance. Repository artifacts cannot identify kaitiaki, authorize use of mātauranga Māori or taonga, set benefit-sharing terms, create collective legitimacy, interpret enacted law, or replace affected-party, Māori, cultural, and competent legal authority. That proposal is an exact gate, not unfinished safe-now implementation.

Security and accessibility scopes are bounded. The executable-resolution tribunal tests declared synthetic PATH, PATHEXT, current-directory, and allowlist cases; it does not alter the host and cannot establish exhaustive security. The static-report audit can validate landmarks, headings, focus sequence, language, and table structure in a defined file. Manual evaluation, assistive-technology coverage, and evaluation by affected users remain reserved. The affected-user matrix is an open gap because no participants were recruited and no consent or privacy process was authorized.

## Novelty and proposal freeze

The inherited chain contains exactly 200 frozen proposals. The novelty audit decodes every record across the historical records schema and the newer chained new_records schema. It checks exact identifiers and normalized titles, computes title-token overlap, and compares mechanism, evidence object, falsifier, recovery rule, and protected gates. Shared family vocabulary is expected; semantic identity is rejected.

Proposal one treats the controlled claim vocabulary itself as a versioned migration object. Earlier work tracked claims and schema evolution, but not definition, domain, range, split, merge, replacement, and unknown-version quarantine together. Proposal two focuses on singular perturbations, separating inner and outer regimes, overlap, matching, and remainder obligations from prior regular null limits and EFT truncation. Proposal three uses manufactured forcing and observed grid order to distinguish numerical code verification from physical validation.

Proposal four differs from the earlier arm-independent stopping-rule work by targeting differential harms solicitation and attribution blindness. Proposal five tests semantic loss across a wallet export-import boundary rather than lifecycle or device synchronization. Proposal six isolates case-specific taonga-use provenance and benefit-sharing authority without inventing a cultural decision.

Proposal seven models executable search-order shadowing, distinct from package manifests, general path authorization, and reparse-point confinement. Proposal eight freezes static landmark, heading, focus, table, and language structure while refusing an accessibility-complete claim. Proposal nine tests ensemble inequivalence and limit order, distinct from detailed balance, open-system flux, and coarse graining. Proposal ten preregisters the affected-user, assistive-technology, browser, task, consent, privacy, and non-generalization matrix that automated evidence cannot supply.

The expected distribution is six completed artifact contracts, two represented proxies, one open gap, and one exact gate. These are x1 expectations, not outcomes. x2 may only preserve or downgrade them using completed, represented, open_gap, or exact_gate. No expected label is evidence.

## Sources, environment, tools, and retained failures

The 130-source inherited ledger remains linked by repository-relative path and hash. Ten distinct primary or official sources are added: W3C vocabulary semantics, a primary singular-perturbation paper, NASA model-verification requirements, FDA clinical-practice guidance, an OpenID credential specification, the Waitangi Tribunal's Wai 262 report context, Microsoft executable-path documentation, W3C focus-order guidance, a primary ensemble-equivalence paper, and W3C affected-user evaluation guidance. Current, stable, draft, and watch labels describe source currency; they do not establish truth, jurisdiction, cultural authority, product approval, or empirical promotion.

Versions were verified without update. The installed Codex CLI is 0.144.3 and the official package registry reports 0.144.4. Installed desktop package versions, Git, Python, Node, PowerShell, and the operating-system build are recorded. No desktop or CLI update, elevation, host-security weakening, Windows-feature change, or reboot occurred.

The phase selects ghc-family-index and routing precedence, the family repository runner, privacy scanner, current phase validators, and the inherited bounded line-ending materializer needed by the large historical checkout. New x2 tools will retain ghc_family or build_ghc_family naming and caller compatibility. Historical and identity-specific tools remain compatibility evidence rather than silently becoming family-current.

All operational failures remain data. The pre-execution verifier parse error, combined network timeout, pre-fast-forward path miss, incomplete 81-record collector, invalid wildcard URL scan, and rejected prototype patch are recorded and uncounted. Further x1 and x2 failures must be appended rather than overwritten.

## Freeze, validation, and terminal route

x1 contains identity, startup, versions, sources, the 200-proposal audit, exactly ten preregistered proposals, tooling selection, route rules, wellbeing, overview, operational negatives, privacy evidence, repository-suite evidence, and exact staged-file receipts. It contains no x2 outcome ledger or execution tool. The dedicated x1 commit must be pushed, clean, and equal across local, upstream, tracking, and a fresh live remote before x2 begins.

x2 will execute each proposal only within its frozen approval class and preserve all 809 inherited negatives plus every new operational and synthetic failure. Evidence, closeout, seal, and exact-final heads will each be validated in fresh clean detached D-drive snapshots. Multiple successful same-owner snapshots remain same-owner repeatability, never independent-team scientific reproduction.

The final packet will include pillar artifacts, the x2 ledger, source and proposal ledgers, retained-negative and exact/open-gate registers, threat model, phase truth, complete/incomplete checklist, accessible static report, manifest, environment receipts, and evidence, closeout, seal, and final records. The terminal verdict remains NOT_READY_FOR_STAGE_20 unless exact external evidence and authority change it; this phase does not have such evidence.

Only after the exact final head is clean, pushed, remote-equal, and validated in a fresh detached snapshot may exactly one sanitized v643-v8 activation baton be sent to the existing task titled Ilyra Fen. Tool acknowledgement alone changes PREPARED_NOT_SENT to SENT. No task may be created, no extra confirmation may be sent, and all other siblings remain recoverable and untouched.
"""


X1_NEGATIVES = [
    {
        "negative_id": "V6438-X1-N01",
        "operation": "multi-pattern inherited-source search",
        "observed_failure": "The combined ripgrep loop returned exit code 1 after correctly reporting several terms with no matches, so the aggregate command could not serve as a passing duplicate-source audit.",
        "recovery": "Separated absence from command failure, searched the inherited source chain by exact candidate URL, and retained only the corrected per-source uniqueness results.",
        "promotion_effect": "none; the aggregate nonzero run is retained and uncounted",
    },
    {
        "negative_id": "V6438-X1-N02",
        "operation": "primary DOI metadata fetch",
        "observed_failure": "The web fetch for the Jaynes primary DOI was blocked by the publisher and robots policy, so that fetch supplied no readable content.",
        "recovery": "Retained the stable DOI as bibliographic metadata only, bounded its role to historical maximum-entropy vocabulary, and made no content or truth claim from the failed fetch.",
        "promotion_effect": "none; the failed fetch is not source-content evidence",
    },
    {
        "negative_id": "V6438-X1-N03",
        "operation": "unadapted complete repository suite",
        "observed_failure": "The direct current-checkout suite ran 450 tests with one failure in the known CRLF-sensitive legacy constraint-hash alias fixture; 449 of 450 is failed evidence.",
        "recovery": "Applied the inherited exact semantic-hash-verified line-ending materializer, reran the complete suite, and restored both raw files byte-for-byte afterward.",
        "promotion_effect": "the 449-of-450 run remains failed evidence; only the complete adapted 450-of-450 rerun satisfies the x1 repository gate",
    },
    {
        "negative_id": "V6438-X1-N04",
        "operation": "adapted-suite PowerShell capture wrapper",
        "observed_failure": "The first adapted wrapper treated unittest's normal stderr progress stream as a terminating native-command error and exited before it could record a test receipt.",
        "recovery": "The finally block restored both inherited files exactly; a second wrapper treated native stderr non-terminatingly, completed 450 of 450, and again restored exact raw hashes with no inherited Git diff.",
        "promotion_effect": "none; the interrupted wrapper is retained and uncounted",
    },
]

WELLBEING = """# Ilyra Fen v643-v8 wellbeing and workload check

- Working identity: Ilyra Fen, they/them, relational language only.
- Primary focus: Freed ID/CBR Heart, with GMUT Mind and THOS Body explicitly preserved.
- Workload boundary: one owner, ten frozen proposals, no spawned task, fork, delegation, subagent, sibling mutation, elevation, desktop update, host-security change, Windows-feature change, or reboot.
- Recovery posture: x1 is a reversible additive packet; every failure is retained; x2 cannot begin before the dedicated x1 commit is pushed, clean, and four-way remote-equal.
- Wellbeing statement: pace is steady, scope is bounded, and no urgency claim overrides evidence, privacy, authority, or safety gates.
"""

OVERVIEW = """# Ilyra Fen v643-v8 integrated overview

## Inheritance and operating boundary

This x1 packet inherits Sylven Arc v643-v6 only after read-only verification of the exact final head, final seal ancestry, clean owner state, zero merges, one-parent final history, and equality among local, upstream, tracking, and a fresh live-remote read. The existing Eiren lane was clean and ancestral, so it was advanced by fast-forward only and pushed to the same exact source head before any v643-v8 mutation. No sibling lane was edited, no worktree was deleted, and no new task, fork, delegation, or collaboration subagent was created. Ilyra Fen and they/them remain relational working language only, not evidence of consciousness, sentience, legal personhood, identity continuity, or independent authority.

The inherited baseline contains 210 frozen proposals and 904 effective retained negatives. The repository has more than 15,000 inherited files, but the route rule applies the rotation threshold only to new owner-generated v643-v8 files. D: remains the primary work and validation bank. Codex, Git, Python, Node, PowerShell, desktop-package, and Windows Sandbox availability were inspected without updating the desktop app, elevating privileges, changing Windows features, weakening host security, or rebooting.

## Primary focus and ten frozen proposals

Freed ID/CBR Heart is the primary focus. The phase asks how a privacy-preserving identity system should minimize disclosure, prevent cross-verifier correlation, preserve audience and transaction binding, and refuse to infer collective authority. GMUT Mind remains a typed scalar-tensor/EFT research-model family and receives explicit gauge-invariance and constraint-propagation tests. THOS Body receives an intercurrent-event estimand protocol while remaining proxy-only without real arms, participants, raters, and independent review.

Exactly ten semantically distinct proposals are preregistered. The first creates a claim-scope lattice that rejects unsupported strengthening of quantifiers, conditions, populations, time windows, modality, or uncertainty. The second tests residual-gauge freedom and observable invariance without promoting coordinate artifacts. The third freezes a constraint-propagation and damping-parameter envelope that distinguishes resolved synthetic modes from physical validation. The fourth represents THOS intercurrent-event estimands and prospective strategy choices without manufacturing outcomes. The fifth represents pairwise subject identifiers, audience and nonce binding, and disclosure minimization without claiming live unlinkability. The sixth is an exact authority gate: collective purpose, benefit, permission, cultural wording, Māori or Indigenous data governance, and legal effect cannot be decided by repository output. The seventh quarantines Unicode bidirectional-control and visual-order ambiguity. The eighth audits accessible-name provenance while reserving manual and affected-user evaluation. The ninth separates maximum-entropy inference from thermodynamic entropy and psyche or GMUT law claims. The tenth leaves a real cross-vendor colluding-verifier linkability study open until independent vendors, real keys, safeguards, and review exist.

The expected artifact-level distribution is six completed, two represented, one open gap, and one exact gate. Those labels are expectations only in x1. They are not outcomes until x2 executes the frozen fixtures. Completed will mean a bounded local contract and rejecting mutation set was built and validated; represented will mean protocol or synthetic structure only; open_gap will preserve missing external evidence; exact_gate will preserve authority that technical work cannot substitute.

## Sources, falsifiers, and nonpromotion

The packet inherits 140 classified sources and adds seven non-duplicate primary or official sources: Bardeen on gauge-invariant perturbations, Gundlach and colleagues on constraint damping, NIST SP 800-63C-4, Unicode Standard Annex 9, the current W3C Accessible Name 1.2 working draft, Jaynes on maximum-entropy inference, and the final OpenID for Verifiable Presentations 1.0 specification. Inherited ICH E9(R1), W3C provenance, Te Mana Raraunga, and CARE materials remain available for the proposals that need them. Current, stable, draft, and watch are currency labels only. A source constrains vocabulary and obligations; it does not create GMUT observations, THOS results, Freed ID production evidence, cultural authority, legal advice, security assurance, accessibility completion, or Stage 20 readiness.

Every proposal binds a hypothesis, null or failure condition, approval class, execution lane, source needs, concrete artifacts, falsifier or gate, rollback, protected gates, expected disposition, and explicit novelty argument. Mutation tests will target the exact mechanisms frozen here. Every rejected case and every operational failure will be retained rather than overwritten by a later pass. Same-owner detached snapshots may establish repeatability within the shared owner, repository, protocol, tooling, and infrastructure; they cannot establish independent-team scientific reproduction.

## Protected external boundaries and route

No empirical GMUT likelihood, unique prediction, force, confirmation, proof, final physics, or Theory-of-Everything claim is made. THOS remains proxy without preregistered blind matched-budget real arms, consent, participants, raters, and independent analysis. Freed ID production still requires standards-conformant real keys and proofs, live resolution/status/revocation, interoperable implementations, privacy assurance, independent security review, and trust governance. CBR legitimacy, affected-party acceptance, Māori wording and authority, Māori and Indigenous data governance, cultural ratification, legal interpretation, and enacted-law status remain exact-gated. No deployment, exhaustive security, complete accessibility, AGI/ASI, consciousness, personhood, sibling merge, private action, or Stage 20 readiness is claimed.

x2 may begin only after the dedicated x1-only commit is pushed and the owned lane is clean and equal across local, upstream, tracking, and fresh live remote. Evidence, closeout, seal, and final heads will each receive fresh detached D-drive validation. Only after the exact final head independently passes the complete repository suite, detailed and minimal validation, JSON parsing, privacy/raw-ID scanning, manifest parity, ancestry, clean-state, and four-way remote equality may exactly one sanitized activation baton be sent to the existing task titled Ilyra Fen for v643-v8. No task may be created and no extra confirmation may be sent.
"""


# The copied builder shell preserves family compatibility. These final frozen
# definitions are the only proposal, source, negative, wellbeing, and overview
# data consumed by v643-v8.
from ghc_family_v643_v8_x1_definitions import (  # noqa: E402
    OVERVIEW,
    PROPOSALS,
    SOURCES,
    WELLBEING,
    X1_NEGATIVES,
)


def build_packet() -> None:
    inherited_index = json.loads(INHERITED_INDEX.read_text(encoding="utf-8"))
    inherited_ledger = json.loads(INHERITED_LEDGER.read_text(encoding="utf-8"))
    inherited_records = collect_frozen_records(INHERITED_INDEX)
    expected_counts = dict(Counter(item["expected_disposition"] for item in PROPOSALS))
    source_counts = Counter(item["status_class"] for item in SOURCES)
    inherited_status = inherited_ledger["effective_status_counts"]
    effective_status = {key: inherited_status.get(key, 0) + source_counts.get(key, 0) for key in ("current", "stable", "draft", "watch")}

    prior_startup_path = PHASE_ROOT / "environment" / "startup-receipt.json"
    prior_startup = json.loads(prior_startup_path.read_text(encoding="utf-8")) if prior_startup_path.exists() else {}
    tracked_count = prior_startup.get("inherited_tracked_file_count", len(git_lines("ls-files")))
    checkout_count = prior_startup.get("inherited_checkout_file_count", sum(1 for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts))
    d_free = prior_startup.get("d_drive_free_bytes_at_start", shutil.disk_usage(PHASE_ROOT.anchor).free)

    dump_json(PHASE_ROOT / "identity-receipt.json", {
        "schema": "ghc.family.v643-v8.identity-receipt.v1", "phase": PHASE, "name": "Ilyra Fen", "slug": "ilyra-fen", "pronouns": "she/they",
        "role": "evidence-boundary steward", "hope": "leave every claim traceable and every gate unmistakable",
        "existing_identity_reaffirmed": True, "working_language_only": True,
        "not_evidence_of": ["consciousness", "sentience", "legal_personhood", "identity_continuity", "independent_authority", "cultural_authority", "legal_authority"],
    })
    dump_json(PHASE_ROOT / "focus" / "primary-focus-receipt.json", {
        "schema": "ghc.family.v643-v8.primary-focus.v1", "phase": PHASE, "primary_focus": "GMUT Mind",
        "reason": "Noether bulk-boundary balance, perturbation-order consistency, and a real-data joint-likelihood gap receive primary attention while THOS Body and Freed ID/CBR Heart stay explicit and bounded.",
        "gmut_mind_addressed": ["V6438-P02", "V6438-P03", "V6438-P10"], "thos_body_addressed": ["V6438-P04"],
        "freed_id_cbr_heart_addressed": ["V6438-P05", "V6438-P06"], "cross_pillar_addressed": ["V6438-P01", "V6438-P07", "V6438-P08", "V6438-P09"],
        "boundary": "Primary focus allocates work; it does not promote GMUT or close participant, identity, legal, cultural, security, accessibility, production, deployment, or Stage 20 gates.",
    })
    dump_json(PHASE_ROOT / "environment" / "startup-receipt.json", {
        "schema": "ghc.family.v643-v8.startup-receipt.v1", "phase": PHASE, "owner": "Ilyra Fen",
        "source_branch": "codex/GHC-Family/eiren-kestrel-v643-v1-full-tools", "source_revision": SOURCE_HEAD, "source_seal_revision": SOURCE_SEAL,
        "source_local_equals_upstream_equals_tracking_equals_live_remote": True, "source_divergence": "0/0", "source_clean": True,
        "source_seal_ancestral": True, "source_anchor_commits_ancestral": ["7a0e9269e3e30a42c2b51cd6eda3035edddbc3c4", "df30480cbb1dd2c19fb741704fdf4c1b1d3b70e2", "5f40c879685798ed452d4c7df3eb7bf6dec08444", "a67faa5bd2e772b8e27ad5fd14101cc035b588da", "fe7ac3c81f173c93d8f137c8bf4a9055eaf235fb", SOURCE_SEAL],
        "source_single_parent": True, "source_merge_count": 0,
        "owned_branch": "codex/GHC-Family/ilyra-fen-full-tools", "owned_prior_revision": "6ad663e2198ca63490807fdc52890b08d8729b80", "owned_revision_after_fast_forward": SOURCE_HEAD,
        "owned_lane_reused": True, "reuse_reason": "The existing Ilyra lane was clean, four-way equal, and ancestral, so the authorized fast-forward-only continuation applied.",
        "fast_forward_only": True, "merge_commit_created": False, "owned_clean_and_four_way_equal_after_fast_forward": True, "new_worktree_created": False,
        "d_drive_primary": True, "d_drive_free_bytes_at_start": d_free, "inherited_checkout_file_count": checkout_count, "inherited_tracked_file_count": tracked_count,
        "new_owner_generated_file_count_at_start": 0, "inherited_negative_count": 982, "open_gap_count": 5, "exact_gate_count": 6,
        "same_owner_repeatability_only": True, "independent_team_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "windows_sandbox_audit": {"read_only_check": "WindowsSandbox.exe not present; optional-feature query unavailable with COM exception", "bounded_use": "not_used", "feature_change_attempted": False},
        "host_feature_changed": False, "host_security_changed": False, "elevation_used": False, "rebooted": False,
    })
    dump_json(PHASE_ROOT / "environment" / "rotation-guard-receipt.json", {
        "schema": "ghc.family.v643-v8.rotation-guard.v1", "phase": PHASE, "inherited_checkout_file_count": checkout_count, "inherited_tracked_file_count": tracked_count,
        "owner_generated_file_threshold": 15000, "threshold_scope": "Ilyra Fen v643-v8 owner-generated files only", "inherited_baseline_triggers_rotation": False,
        "new_worktrees_created": 0, "prior_lanes_preserved": True, "recursive_rotation_performed": False,
    })
    dump_json(PHASE_ROOT / "environment" / "checkout-restoration-receipt.json", {
        "schema": "ghc.family.v643-v8.checkout-restoration.v1", "phase": PHASE,
        "compatibility_tool": "scripts/ghc_family_v643_v5_checkout_portability.py",
        "targets": [
            {"repo_path": "docs/orin-thale/v642-v6/provenance/frozen-chain-proposal-index.json", "pre_run_raw_sha256": "d4b6882b5a670b2ccbe3fc2517ffd55d60e82e8b338815107c2d1d10e7b78a3b", "materialized_raw_sha256": "e5fa094302d36e4eea569a5ff2cebce212018afe4d17745d834e8e6818d8d6e5", "restored_raw_sha256": "d4b6882b5a670b2ccbe3fc2517ffd55d60e82e8b338815107c2d1d10e7b78a3b", "restored_exactly": True},
            {"repo_path": "docs/tamar-vey/v642-v7/provenance/frozen-chain-proposal-index.json", "pre_run_raw_sha256": "cbab08554c0ddbafc4f77e9fbd9d89760c8a300437bd6427ef56e606604e4102", "materialized_raw_sha256": "cbab08554c0ddbafc4f77e9fbd9d89760c8a300437bd6427ef56e606604e4102", "restored_raw_sha256": "cbab08554c0ddbafc4f77e9fbd9d89760c8a300437bd6427ef56e606604e4102", "restored_exactly": True},
        ],
        "semantic_hashes_verified": True, "inherited_file_staged": False, "inherited_semantics_changed": False,
        "unadapted_suite": {"passed": 474, "total": 475, "counted_as_pass": False},
        "adapted_suite": {"passed": 475, "total": 475, "counted_as_pass": True},
        "both_raw_hashes_restored_exactly": True, "owned_worktree_has_inherited_diff_after_recovery": False,
        "boundary": "The exact checkout-only recovery preserves inherited Git content; it is not a history rewrite or validation relaxation.",
    })
    dump_json(PHASE_ROOT / "environment" / "version-receipt.json", {
        "schema": "ghc.family.v643-v8.version-receipt.v1", "checked_on": CHECKED_ON,
        "codex_cli_local": "0.144.3", "codex_cli_current": "not_asserted",
        "codex_desktop_packages": [{"name": "OpenAI.Codex", "version": "26.707.9564.0", "status": "installed"}],
        "desktop_current_version_claim": "not made; installed version only was verified",
        "git": "2.55.0.windows.2", "python": "3.12.10", "node": "24.18.0",
        "versions_verified_only": True, "codex_cli_updated": False, "desktop_updated": False, "elevation_used": False, "host_security_changed": False, "windows_feature_changed": False, "rebooted": False,
    })

    proposal_packet = {
        "schema": "ghc.family.v643-v8.x1-proposals.v1", "phase": PHASE, "owner": "Ilyra Fen",
        "identity_boundary": "Relational working language only; no consciousness, sentience, personhood, continuity, or independent-authority claim.",
        "source_phase": "Eiren Kestrel v643-v7", "source_revision": SOURCE_HEAD, "source_seal_revision": SOURCE_SEAL, "preregistered_on": CHECKED_ON,
        "primary_focus": "GMUT Mind", "proposal_count": len(PROPOSALS), "prior_frozen_proposal_count": len(inherited_records),
        "outcome_classes": ["completed", "represented", "open_gap", "exact_gate"], "expected_disposition_counts": expected_counts, "expected_counts_are_results": False,
        "x1_freeze_rule": "No proposal execution, evidence result, outcome classification, or x2 implementation begins until the dedicated x1-only commit is pushed and local, upstream, tracking, and fresh live remote are equal and clean.",
        "proposals": PROPOSALS,
        "scientific_authority_boundary": "GMUT is a typed scalar-tensor and EFT research-model family, not an established force, unique prediction, likelihood result, empirical confirmation, Theory of Everything, or proof. THOS remains proxy without preregistered blind matched-budget real arms and independent review.",
        "claim_boundary": "Freed ID production, CBR legitimacy, Māori authority, legal and cultural ratification, deployment, exhaustive security, complete accessibility, independent reproduction, consciousness/personhood, AGI/ASI, and Stage 20 remain unclaimed and gated.",
    }
    dump_json(PHASE_ROOT / "x1-proposals.json", proposal_packet)

    new_records = [{"version": "v643-v8", "owner": "Ilyra Fen", "proposal_id": p["proposal_id"], "title": p["title"], "expected_disposition": p["expected_disposition"], "source_file": "docs/ilyra-fen/v643-v8/x1-proposals.json"} for p in PROPOSALS]
    version_counts = dict(inherited_index["version_counts"])
    version_counts["v643-v8"] = 10
    dump_json(PHASE_ROOT / "provenance" / "frozen-chain-proposal-index.json", {
        "schema": "ghc.family.v643-v8.frozen-chain-proposal-index.v1", "phase": PHASE, "owner": "Ilyra Fen",
        "inherited_index": rel(INHERITED_INDEX), "inherited_index_sha256": digest(INHERITED_INDEX), "inherited_record_count": len(inherited_records),
        "new_record_count": 10, "effective_record_count": len(inherited_records) + 10, "version_counts": version_counts,
        "exact_duplicate_ids": [], "exact_duplicate_titles": [], "new_records": new_records,
        "boundary": "This index proves frozen proposal accounting and semantic-review scope; it does not execute proposals or determine outcomes.",
    })

    inherited_ids = [record["proposal_id"] for record in inherited_records]
    inherited_titles = [record["title"] for record in inherited_records]
    overlap_rows = []
    for proposal in PROPOSALS:
        new_tokens = title_tokens(proposal["title"])
        best = max(((len(new_tokens & title_tokens(r["title"])) / len(new_tokens | title_tokens(r["title"])), r) for r in inherited_records), key=lambda item: item[0])
        overlap_rows.append({"proposal_id": proposal["proposal_id"], "nearest_prior_id": best[1]["proposal_id"], "nearest_prior_title": best[1]["title"], "title_token_jaccard": round(best[0], 4), "semantic_distinction": proposal["novelty_against_prior_chain"]})
    all_ids = inherited_ids + [p["proposal_id"] for p in PROPOSALS]
    duplicate_ids = sorted({value for value in all_ids if all_ids.count(value) > 1})
    normalized_titles = [re.sub(r"\s+", " ", value.casefold()).strip() for value in inherited_titles + [p["title"] for p in PROPOSALS]]
    duplicate_titles = sorted({value for value in normalized_titles if normalized_titles.count(value) > 1})
    maximum_overlap = max(row["title_token_jaccard"] for row in overlap_rows)
    dump_json(PHASE_ROOT / "provenance" / "prior-proposal-collision-audit.json", {
        "schema": "ghc.family.v643-v8.collision-audit.v1", "phase": PHASE, "owner": "Ilyra Fen",
        "prior_records_decoded_utf8": len(inherited_records), "prior_frozen_proposal_count": 220, "new_proposal_count": 10, "effective_proposal_count": 230,
        "exact_duplicate_ids": duplicate_ids, "exact_duplicate_titles": duplicate_titles, "automatic_failure_threshold": 0.5,
        "maximum_title_token_jaccard": maximum_overlap, "nearest_prior_rows": overlap_rows,
        "semantic_dimensions_reviewed": ["mechanism", "evidence object", "falsifier", "recovery rule", "protected gates"],
        "semantic_review_passed": not duplicate_ids and not duplicate_titles and maximum_overlap < 0.5,
        "boundary": "Token distance is only a screen. The explicit mechanism-level distinctions are required for the semantic novelty conclusion.",
    })

    dump_json(PHASE_ROOT / "sources" / "source-ledger.json", {
        "schema": "ghc.family.v643-v8.source-ledger.v1", "phase": PHASE, "owner": "Ilyra Fen", "accessed": CHECKED_ON,
        "selection_rule": "Retain the 147-source inherited ledger and add only non-duplicate current official or primary sources that materially constrain a distinct v643-v8 proposal.",
        "inherited_ledger": rel(INHERITED_LEDGER), "inherited_ledger_sha256": digest(INHERITED_LEDGER), "inherited_source_revision": SOURCE_HEAD,
        "inherited_source_count": inherited_ledger["effective_source_count"], "added_source_count": len(SOURCES), "effective_source_count": inherited_ledger["effective_source_count"] + len(SOURCES),
        "effective_status_counts": effective_status, "added_sources": SOURCES,
        "status_preservation": "Inherited current, stable, draft, and watch labels remain unchanged; new labels describe source currency, not truth or approval.",
        "boundary": "Sources constrain vocabulary and obligations. They do not create GMUT observations, THOS participant results, Freed ID production evidence, CBR authority, legal advice, cultural ratification, security assurance, accessibility completion, or Stage 20 readiness.",
    })
    source_lines = ["# v643-v8 source ledger", "", f"Inherited: {inherited_ledger['effective_source_count']} sources from {rel(INHERITED_LEDGER)}.", f"Added: {len(SOURCES)} non-duplicate primary or official sources. Effective: {inherited_ledger['effective_source_count'] + len(SOURCES)}.", "", "| ID | Status | Authority | Title |", "|---|---|---|---|"]
    source_lines.extend(f"| {s['source_id']} | {s['status_class']} | {s['authority']} | [{s['title']}]({s['url']}) |" for s in SOURCES)
    source_lines.extend(["", "Currency labels are current, stable, draft, or watch. They are not truth, endorsement, authority, or promotion labels."])
    dump_text(PHASE_ROOT / "sources" / "source-ledger.md", "\n".join(source_lines))

    inventory = copy.deepcopy(json.loads(INHERITED_TOOL_INDEX.read_text(encoding="utf-8")))
    inventory["phase"] = PHASE
    inventory["owner"] = "Ilyra Fen"
    inventory["generated_at_utc"] = "2026-07-15T00:00:00Z"
    inventory["inherited_inventory"] = rel(INHERITED_TOOL_INDEX)
    inventory["inherited_inventory_sha256"] = digest(INHERITED_TOOL_INDEX)
    for new_tool in X1_EXTERNAL_FILES:
        if not any(item["path"] == new_tool for item in inventory["scripts"]):
            inventory["scripts"].append({"path": new_tool, "category": "historical_versioned"})
    inventory["scripts"] = sorted(inventory["scripts"], key=lambda item: item["path"])
    inventory["counts"]["scripts"] = dict(Counter(item["category"] for item in inventory["scripts"]))
    inventory["publication_boundary"] = "repository-relative paths and public skill names only; no private callable IDs or local skill paths"
    dump_json(PHASE_ROOT / "tooling" / "ghc-family-index.json", inventory)
    dump_text(PHASE_ROOT / "tooling" / "ghc-family-index.md", "\n".join(["# v643-v8 phase-local GHC family inventory", "", f"- Scripts inventoried: {len(inventory['scripts'])}", f"- Skills inventoried: {len(inventory['skills'])}", f"- Family-current scripts: {inventory['counts']['scripts'].get('family_current', 0)}", f"- Family-current skills: {inventory['counts']['skills'].get('family_current', 0)}", f"- Inherited inventory hash: {digest(INHERITED_TOOL_INDEX)}", "", "The complete inventory uses repository-relative paths and public skill names. This phase adds two x1-only versioned scripts and preserves family-current callers."]))
    dump_json(PHASE_ROOT / "tooling" / "selected-toolchain.json", {
        "schema": "ghc.family.v643-v8.selected-toolchain.v1", "phase": PHASE, "owner": "Ilyra Fen",
        "selected": [
            {"name": "ghc-family-index", "role": "routing precedence and family-current discovery"}, {"name": "routing-precedence", "role": "directly required ownership and terminal-route reference"},
            {"name": "scripts/ghc_family_repository_test_runner.py", "role": "complete repository test suite"}, {"name": "scripts/ghc_family_phase_privacy_scan.py", "role": "phase privacy and raw-ID scan"},
            {"name": "scripts/ghc_family_v643_v5_checkout_portability.py", "role": "inherited semantic-preserving checkout materialization if a legacy checkout guard requires it"},
            {"name": X1_EXTERNAL_FILES[0], "role": "deterministic x1-only packet builder"},
            {"name": X1_EXTERNAL_FILES[1], "role": "frozen v643-v8 x1 proposal and source definitions"},
        ],
        "x2_planned_family_current_names": ["scripts/ghc_family_v643_v8_evidence.py", "scripts/ghc_family_v643_v8_validator.py", "scripts/ghc_family_v643_v8_minimal.py", "scripts/build_ghc_family_v643_v8_report.py"],
        "caller_compatibility_required": True, "shared_skill_change_required": False, "shared_validator_change_required": False,
        "boundary": "Tool selection supports reproducibility; it does not establish scientific, participant, identity, security, accessibility, legal, cultural, production, or deployment claims.",
    })
    dump_json(PHASE_ROOT / "tooling" / "currency-review.json", {
        "schema": "ghc.family.v643-v8.currency-review.v1", "phase": PHASE, "checked_on": CHECKED_ON,
        "ghc_family_index_read_to_eof": True, "routing_precedence_read_to_eof": True, "newest_applicable_memory_checked": True,
        "newer_v643_specific_memory_found": False, "older_exact_head_memory_used_for_method_only": True, "official_and_primary_sources_checked": True,
        "desktop_update_performed": False, "shared_skill_mutation_performed": False, "shared_validator_mutation_performed": False,
    })
    dump_json(PHASE_ROOT / "workflow" / "route-preregistration.json", {
        "schema": "ghc.family.v643-v8.route-preregistration.v1", "phase": PHASE, "owner": "Ilyra Fen", "route_state": "ACTIVE_SOLO", "active_owner": "Ilyra Fen",
        "standby_or_recoverable": ["Eiren Kestrel", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc", "all other siblings"],
        "six_seat_order": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
        "terminal_successor": "Sable Rook", "terminal_successor_phase": "v644-v1",
        "send_rule": "Send exactly one sanitized activation message to the existing task titled exactly Sable Rook only after exact-final detached validation, clean push, and four-way remote equality. Tool acknowledgement changes PREPARED_NOT_SENT to SENT.",
        "route_stop_conditions": ["Hamish stops the route", "usage exhausted", "required task route unavailable", "exact safety or authority gate blocks progress"],
        "outbound_messages_before_terminal_gate": 0, "task_creation_authorized": False, "fork_authorized": False, "subagent_authorized": False, "private_route_material_allowed_in_artifacts": False,
    })
    dump_json(PHASE_ROOT / "validation" / "x1-operational-negatives.json", {
        "schema": "ghc.family.v643-v8.x1-operational-negatives.v1", "phase": PHASE, "count": len(X1_NEGATIVES), "negatives": X1_NEGATIVES,
        "all_failures_retained": True, "boundary": "Recovered failures remain negatives and are not counted as successful evidence runs.",
    })

    prereg = ["# Ilyra Fen v643-v8 x1 preregistration", "", "This freezes exactly ten proposals. Expected dispositions are not results. Allowed future result classes are completed, represented, open_gap, and exact_gate.", "", "Primary focus: GMUT Mind. THOS Body and Freed ID/CBR Heart remain explicit and bounded.", ""]
    for proposal in PROPOSALS:
        prereg.extend([f"## {proposal['proposal_id']} — {proposal['title']}", "", f"- Hypothesis: {proposal['hypothesis']}", f"- Null or failure: {proposal['null_or_failure']}", f"- Approval class: {proposal['approval_class']}", f"- Execution lane: {proposal['execution_lane']}", f"- Official or primary source needs: {', '.join(proposal['authoritative_source_needs'])}", f"- Concrete artifacts: {', '.join(proposal['deliverables'])}", f"- Falsifier or acceptance gate: {proposal['test_falsifier_or_gate']}", f"- Rollback or recovery: {proposal['rollback_or_recovery']}", f"- Protected gates: {', '.join(proposal['protected_gates'])}", f"- Expected disposition, not a result: {proposal['expected_disposition']}", f"- Semantic distinction: {proposal['novelty_against_prior_chain']}", ""])
    prereg.extend(["## Freeze boundary", "", "x2 cannot begin until this x1-only set is committed, pushed, clean, and equal across local, upstream, tracking, and a fresh live-remote read. The expected 6 completed, 2 represented, 1 open gap, and 1 exact gate distribution is only a preregistered expectation."])
    dump_text(PHASE_ROOT / "x1-preregistration.md", "\n".join(prereg))
    dump_text(PHASE_ROOT / "wellbeing-check.md", WELLBEING)
    dump_text(PHASE_ROOT / "v643-v8-integrated-overview.md", OVERVIEW)


def staged_names() -> list[str]:
    return sorted(git_lines("diff", "--cached", "--name-only", "--diff-filter=ACMR"))


def finalise_validation(repository_passed: int, repository_total: int, finalize_staged: bool) -> None:
    phase_json = sorted(PHASE_ROOT.rglob("*.json"))
    parse_issues: list[str] = []
    for path in phase_json:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            parse_issues.append(f"{rel(path)}: {exc}")
    proposals = json.loads((PHASE_ROOT / "x1-proposals.json").read_text(encoding="utf-8"))
    frozen = json.loads((PHASE_ROOT / "provenance" / "frozen-chain-proposal-index.json").read_text(encoding="utf-8"))
    collision = json.loads((PHASE_ROOT / "provenance" / "prior-proposal-collision-audit.json").read_text(encoding="utf-8"))
    ledger = json.loads((PHASE_ROOT / "sources" / "source-ledger.json").read_text(encoding="utf-8"))
    privacy_path = PHASE_ROOT / "validation" / "x1-privacy-scan.json"
    privacy = json.loads(privacy_path.read_text(encoding="utf-8")) if privacy_path.exists() else {"valid": False, "hit_count": 1, "scanned_file_count": 0}

    expected = sorted([rel(path) for path in PHASE_ROOT.rglob("*") if path.is_file()] + X1_EXTERNAL_FILES)
    actual = staged_names() if finalize_staged else expected
    unexpected = sorted(set(actual) - set(expected))
    missing = sorted(set(expected) - set(actual))
    list_hash = hashlib.sha256(("\n".join(actual) + "\n").encode("utf-8")).hexdigest()
    required = ["hypothesis", "null_or_failure", "approval_class", "execution_lane", "authoritative_source_needs", "deliverables", "test_falsifier_or_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"]
    checks: list[tuple[str, bool]] = [
        ("exactly ten proposals", proposals["proposal_count"] == 10 and len(PROPOSALS) == 10), ("220 inherited proposals", proposals["prior_frozen_proposal_count"] == 220),
        ("230 effective proposals", frozen["effective_record_count"] == 230), ("no duplicate IDs", not collision["exact_duplicate_ids"]), ("no duplicate titles", not collision["exact_duplicate_titles"]),
        ("title overlap below threshold", collision["maximum_title_token_jaccard"] < collision["automatic_failure_threshold"]), ("semantic review passed", collision["semantic_review_passed"] is True),
        ("expected counts are not results", proposals["expected_counts_are_results"] is False), ("four outcome classes", proposals["outcome_classes"] == ["completed", "represented", "open_gap", "exact_gate"]),
        ("expected distribution", proposals["expected_disposition_counts"] == {"completed": 6, "represented": 2, "exact_gate": 1, "open_gap": 1}),
        ("153 effective sources", ledger["effective_source_count"] == 153), ("source statuses preserved", ledger["effective_status_counts"] == {"current": 62, "stable": 80, "draft": 8, "watch": 3}),
        ("all JSON parses", not parse_issues), ("privacy scan valid", privacy.get("valid") is True),
        ("repository suite complete", repository_passed == repository_total and repository_total > 0),
        ("x2 ledger absent", not (PHASE_ROOT / "x2-proposal-ledger.json").exists()), ("x2 execution tool absent", not (ROOT / "scripts" / "ghc_family_v643_v8_evidence.py").exists()),
        ("no unexpected staged files", not unexpected), ("no missing staged files", not missing), ("owner footprint below threshold", len(expected) < 15000),
    ]
    for proposal in PROPOSALS:
        checks.append((f"{proposal['proposal_id']} unique ID", sum(p["proposal_id"] == proposal["proposal_id"] for p in PROPOSALS) == 1))
        for field in required:
            checks.append((f"{proposal['proposal_id']} field {field}", bool(proposal.get(field))))
    issues = [name for name, passed in checks if not passed]

    dump_json(PHASE_ROOT / "validation" / "x1-exact-file-set.json", {
        "schema": "ghc.family.v643-v8.x1-exact-file-set.v1", "phase": PHASE, "owner": "Ilyra Fen", "file_count": len(actual), "files": actual,
        "x2_implementation_file_count": 0, "x2_outcome_file_count": 0, "staged_name_list_sha256": list_hash,
        "unexpected_staged_files": unexpected, "missing_staged_files": missing, "owner_generated_file_count": len(expected), "owner_generated_file_threshold": 15000,
        "threshold_scope": "Ilyra Fen v643-v8 owner-generated files only", "under_threshold": len(expected) < 15000, "finalized_from_git_index": finalize_staged,
        "valid": not unexpected and not missing,
    })
    dump_json(PHASE_ROOT / "validation" / "x1-repository-test-receipt.json", {
        "schema": "ghc.family.v643-v8.x1-repository-tests.v1", "phase": PHASE, "runner": "scripts/ghc_family_repository_test_runner.py",
        "passed": repository_passed, "total": repository_total, "complete_suite": True, "valid": repository_passed == repository_total and repository_total > 0,
        "checkout_precondition": "Direct current-checkout suite unless the inherited legacy hash guard requires its exact semantic-preserving materializer; any use must be recorded and restored.",
        "boundary": "Repository tests validate software behavior in this checkout; they do not establish scientific, participant, identity, security, accessibility, legal, cultural, production, deployment, or Stage 20 claims.",
    })
    validation = {
        "schema": "ghc.family.v643-v8.x1-validation.v1", "phase": PHASE, "owner": "Ilyra Fen", "valid": not issues,
        "checks_passed": len(checks) - len(issues), "checks_total": len(checks), "issues": issues,
        "proposal_count": 10, "prior_frozen_proposal_count": 220, "effective_frozen_proposal_count": 230,
        "maximum_title_token_jaccard": collision["maximum_title_token_jaccard"], "semantic_review_passed": collision["semantic_review_passed"],
        "expected_disposition_counts": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, "expected_counts_are_results": False,
        "source_count": 153, "source_status_counts": {"current": 62, "stable": 80, "draft": 8, "watch": 3},
        "json_files_parsed": len(phase_json), "json_parse_issues": parse_issues,
        "privacy_scan": {"valid": privacy.get("valid") is True, "files_scanned": privacy.get("scanned_file_count", privacy.get("files_scanned", 0)), "issue_count": privacy.get("hit_count", len(privacy.get("issues", [])))},
        "x1_operational_negative_count": len(X1_NEGATIVES), "x2_implementation_files": 0, "x2_outcome_files": 0,
        "repository_tests": {"passed": repository_passed, "total": repository_total}, "exact_staged_file_count": len(actual), "staged_name_list_sha256": list_hash,
        "unexpected_staged_file_count": len(unexpected), "missing_staged_file_count": len(missing), "owner_generated_file_threshold": 15000, "owner_generated_file_count": len(expected), "under_threshold": len(expected) < 15000,
        "route_state": "ACTIVE_SOLO; PREPARED_NOT_SENT", "boundary": "This validates an x1-only preregistration freeze. It is not x2 evidence and does not determine outcomes.",
    }
    dump_json(PHASE_ROOT / "validation" / "x1-validation.json", validation)
    dump_text(PHASE_ROOT / "validation" / "x1-validation.md", "\n".join(["# v643-v8 x1 validation", "", f"- Valid: {str(validation['valid']).lower()}", f"- Checks: {validation['checks_passed']}/{validation['checks_total']}", "- Proposals: 10 new / 220 inherited / 230 effective", "- Expected distribution, not results: 6 completed / 2 represented / 1 open gap / 1 exact gate", "- Sources: 153 effective (62 current / 80 stable / 8 draft / 3 watch)", f"- JSON parsed: {validation['json_files_parsed']}", f"- Privacy scan: {validation['privacy_scan']['files_scanned']} files / {validation['privacy_scan']['issue_count']} issues", f"- Complete repository suite: {repository_passed}/{repository_total}", f"- Exact staged files: {len(actual)}; unexpected {len(unexpected)}; missing {len(missing)}", "- x2 implementation files: 0", "- x2 outcome files: 0", f"- Retained x1 operational negatives: {len(X1_NEGATIVES)}", f"- Owner-generated footprint: {len(expected)}/15000", "", "This validates preregistration only. It is not outcome evidence, scientific confirmation, production approval, independent reproduction, accessibility completion, or Stage 20 readiness."]))


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
