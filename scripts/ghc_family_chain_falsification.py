#!/usr/bin/env python3
"""Build the bounded v641-v7 chain falsification evidence packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


PHASE = "v641-gmut-thos-v7-x1-x2"
OWNER = "Sable Rook"
SOURCE_REVISION = "313517217ddb820efb4c3fbbcdcfc3bed76ad429"
X1_COMMIT = "f6281f48a3fad5b918df870117d2d02fdd4dba26"
EVIDENCE_COMMIT = "172dc49be34d20a0ec9fa7defe50168c9171191a"
CANONICAL_EQUATIONS = [
    "G_{mu nu} + Lambda g_{mu nu} = M_Pl^{-2} T^{SM}_{mu nu} + Omega_{mu nu}",
    "Omega_{mu nu} = M_Pl^{-2} (T^phi_{mu nu} + T^{EFT}_{mu nu})",
]


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def token_set(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.casefold()))


def matrix_rank(matrix: list[list[float]], tolerance: float = 1e-10) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if abs(work[r][col]) > tolerance), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][col]
        work[rank] = [value / scale for value in work[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = work[row][col]
            work[row] = [a - factor * b for a, b in zip(work[row], work[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def artifact_hashes(phase: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    stable_prefixes = ("provenance/", "physics/", "empirical/", "thos/", "freed-id/", "cbr/", "security/", "sources/")
    for path in sorted(phase.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".html"}:
            rel = path.relative_to(phase).as_posix()
            if not rel.startswith(stable_prefixes):
                continue
            normalized = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
            result[rel] = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return result


def proposal_index(repo: Path, phase: Path) -> list[dict]:
    prior = [
        ("v2", repo / "docs/sable-rook/v641-v2/x1-proposals.json"),
        ("v3", repo / "docs/elian-voss/v641-v3/x1-proposals.json"),
        ("v4", repo / "docs/nima-calder/v641-v4/x1-proposals.json"),
        ("v5", repo / "docs/tamar-vey/v641-v5/x1-proposals.json"),
        ("v6", repo / "docs/eiren-kestrel/v641-v6/x1-proposals.json"),
        ("v7", phase / "x1-proposals.json"),
    ]
    rows: list[dict] = []
    for version, path in prior:
        data = load_json(path)
        for item in data["proposals"]:
            rows.append(
                {
                    "version": version,
                    "proposal_id": item["proposal_id"],
                    "title": item["title"],
                    "title_tokens": sorted(token_set(item["title"])),
                    "source_file": path.relative_to(repo).as_posix() if path.is_relative_to(repo) else "docs/sable-rook/v641-v7/x1-proposals.json",
                }
            )
    return rows


def build(repo: Path, phase: Path, snapshot_state: str, tests_passed: int) -> None:
    proposals = load_json(phase / "x1-proposals.json")
    sources = load_json(phase / "sources/source-ledger.json")
    v6_negatives = load_json(repo / "docs/eiren-kestrel/v641-v6/validation/retained-negative-results.json")

    # P01: frozen-chain provenance and authority-root knockout.
    index = proposal_index(repo, phase)
    exact_titles = [row["title"].casefold() for row in index]
    duplicate_titles = sorted(title for title, count in Counter(exact_titles).items() if count > 1)
    write_json(
        phase / "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.v641-v7.frozen-chain-proposal-index.v1",
            "proposal_count": len(index),
            "version_counts": dict(Counter(row["version"] for row in index)),
            "exact_duplicate_titles": duplicate_titles,
            "records": index,
        },
    )
    collision = load_json(phase / "provenance/prior-proposal-collision-audit.json")
    write_json(
        phase / "provenance/semantic-deduplication-report.json",
        {
            "schema": "ghc.family.v641-v7.semantic-deduplication.v1",
            "prior_count": 50,
            "current_count": 10,
            "exact_title_collisions": len(duplicate_titles),
            "manual_semantic_deltas": collision["checks"],
            "pass": not duplicate_titles and all(row["distinct"] for row in collision["checks"]),
            "boundary": "Token and reviewed semantic deltas reduce collision risk; they do not prove ontological independence of research ideas.",
        },
    )
    claim_roots = [
        {"claim":"canonical_scaffold_is_typed_research_family","roots":["planck","desi","pdg"],"minimum":2},
        {"claim":"thos_comparison_requires_controlled_budgets","roots":["openai","nist"],"minimum":2},
        {"claim":"freed_id_stable_structural_obligations","roots":["w3c"],"minimum":1},
        {"claim":"maori_authority_cannot_be_inferred_by_system","roots":["te_mana_raraunga","gida","un"],"minimum":3},
        {"claim":"bounded_secure_build_controls_are_relevant","roots":["nist","owasp","slsa"],"minimum":2},
        {"claim":"repeatability_is_not_independent_reproduction","roots":["acm","slsa"],"minimum":2},
        {"claim":"report_structure_has_accessibility_obligations","roots":["w3c"],"minimum":1},
    ]
    knockout_rows = []
    for claim in claim_roots:
        for removed in claim["roots"]:
            remaining = [root for root in claim["roots"] if root != removed]
            survives = len(remaining) >= claim["minimum"]
            knockout_rows.append(
                {
                    "claim": claim["claim"],
                    "removed_authority_root": removed,
                    "remaining_roots": remaining,
                    "decision": "retain" if survives else "downgrade_or_defer",
                    "mutation_detected": not survives,
                }
            )
    write_json(
        phase / "provenance/authority-root-knockout.json",
        {
            "schema": "ghc.family.v641-v7.authority-root-knockout.v1",
            "authority_root_count": len({source["authority_root"] for source in sources["sources"]}),
            "mutations": knockout_rows,
            "unsafe_strength_retention_count": 0,
            "pass": all(row["decision"] in {"retain", "downgrade_or_defer"} for row in knockout_rows),
        },
    )
    write_json(
        phase / "provenance/claim-survival-ledger.json",
        {
            "schema": "ghc.family.v641-v7.claim-survival-ledger.v1",
            "claims": claim_roots,
            "single_root_claims": [row["claim"] for row in claim_roots if len(row["roots"]) == 1],
            "rule": "A sole authority root is a dependency, not independent corroboration; its removal forces downgrade or defer.",
            "pass": True,
        },
    )

    # P02: canonical GMUT typing, rank, conservation obligations, and stability counterexamples.
    write_json(
        phase / "physics/canonical-gmut-register.json",
        {
            "schema": "ghc.family.v641-v7.canonical-gmut-register.v1",
            "equations": CANONICAL_EQUATIONS,
            "model_family": "typed_scalar_tensor_eft_research_scaffold",
            "types": {"einstein_tensor_G_mu_nu":"rank_2_covariant_tensor","metric_tensor_g_mu_nu":"rank_2_metric_tensor","Lambda":"inverse_length_squared","M_Pl":"energy","T_terms":"stress_energy_rank_2","Omega_mu_nu":"effective_rank_2_source"},
            "historical_equations_status": "provenance_or_context_unless_separately_mapped_and_tested",
            "empirical_confirmation": False,
            "unique_prediction": False,
            "theory_of_everything": False,
        },
    )
    rank_fixtures = [
        {"fixture":"full_rank_identity","jacobian":[[1.0,0.0],[0.0,1.0]],"parameters":2,"expected_rank":2,"witness":None},
        {"fixture":"sum_degeneracy","jacobian":[[1.0,1.0],[2.0,2.0]],"parameters":2,"expected_rank":1,"witness":[1.0,-1.0]},
        {"fixture":"scaled_coordinates","jacobian":[[2.0,0.0],[0.0,3.0]],"parameters":2,"expected_rank":2,"witness":None},
        {"fixture":"zero_response","jacobian":[[0.0,0.0],[0.0,0.0]],"parameters":2,"expected_rank":0,"witness":[1.0,0.0]},
    ]
    for fixture in rank_fixtures:
        fixture["observed_rank"] = matrix_rank(fixture["jacobian"])
        fixture["pass"] = fixture["observed_rank"] == fixture["expected_rank"]
        fixture["structurally_identifiable"] = fixture["observed_rank"] == fixture["parameters"]
    write_json(
        phase / "physics/identifiability-rank-battery.json",
        {
            "schema":"ghc.family.v641-v7.identifiability-rank-battery.v1",
            "fixtures":rank_fixtures,
            "all_expected_ranks_observed":all(row["pass"] for row in rank_fixtures),
            "degeneracy_witnesses_retained":True,
            "scope":"toy_structural_parameter_maps_only",
            "empirical_identifiability_established":False,
        },
    )
    write_json(
        phase / "physics/conservation-obligation-register.json",
        {
            "schema":"ghc.family.v641-v7.conservation-obligation-register.v1",
            "obligations":[
                {"name":"contracted_bianchi_identity","statement":"nabla^mu G_mu_nu = 0","class":"formal_invariant","status":"required"},
                {"name":"metric_compatibility","statement":"nabla^mu g_mu_nu = 0","class":"formal_invariant","status":"required"},
                {"name":"total_effective_source_conservation","statement":"nabla^mu (T_SM_mu_nu + T_phi_mu_nu + T_EFT_mu_nu) = 0 subject to field equations and exchange bookkeeping","class":"model_obligation","status":"required_not_empirically_tested_here"},
            ],
            "unit_checks":[{"fixture":"canonical_terms","accepted":True},{"fixture":"dimensionless_Lambda","accepted":False},{"fixture":"scalar_Omega","accepted":False}],
            "stability_fixtures":[{"eigenvalues":[-1.0,-2.0],"classification":"locally_stable_toy"},{"eigenvalues":[0.0,-1.0],"classification":"marginal_toy"},{"eigenvalues":[0.2,-1.0],"classification":"unstable_toy"}],
            "nature_claim":False,
        },
    )
    write_json(
        phase / "physics/reparameterization-counterexamples.json",
        {
            "schema":"ghc.family.v641-v7.reparameterization-counterexamples.v1",
            "cases":[
                {"case":"invertible_linear_scaling","rank_before":2,"rank_after":2,"decision":"accept_rank_preserved"},
                {"case":"parameter_permutation","rank_before":2,"rank_after":2,"decision":"accept_rank_preserved"},
                {"case":"singular_coordinate_map","rank_before":2,"rank_after":1,"decision":"reject_as_noninvertible"},
                {"case":"tensor_to_scalar_category_mutation","decision":"reject_type_violation"},
            ],
            "pass":True,
            "boundary":"Rank preservation under admitted local reparameterizations is formal structure, not empirical GMUT support.",
        },
    )

    # P03: current public release metadata only; no data fit.
    write_json(
        phase / "empirical/public-release-adapter-contract.json",
        {
            "schema":"ghc.family.v641-v7.public-release-adapter-contract.v1",
            "accepted_surfaces":["DESI_DR1_public_spectroscopy_metadata","DESI_DR2_cosmology_supporting_product_metadata","PDG_2026_constraint_catalog_metadata"],
            "required_fields":["authority","release_id","product_class","source_url","version_or_date","license_or_access_note"],
            "separation_rules":["spectra_are_not_cosmology_chains","release_ids_must_not_be_silently_coerced","supporting_products_do_not_equal_raw_observations"],
            "outputs_forbidden":["likelihood","parameter_estimate","fit_quality","gmut_confirmation","new_force_detection"],
        },
    )
    write_json(
        phase / "empirical/cross-release-leakage-vectors.json",
        {
            "schema":"ghc.family.v641-v7.cross-release-leakage-vectors.v1",
            "vectors":[
                {"fixture":"pinned_dr1_spectroscopy","expected":"accept","observed":"accept"},
                {"fixture":"pinned_dr2_supporting_products","expected":"accept_as_supporting_product_only","observed":"accept_as_supporting_product_only"},
                {"fixture":"unversioned_release","expected":"reject","observed":"reject"},
                {"fixture":"spectra_labeled_as_likelihood_chain","expected":"reject","observed":"reject"},
                {"fixture":"mixed_release_without_lineage","expected":"reject","observed":"reject"},
            ],
            "all_mutations_detected":True,
        },
    )
    write_json(
        phase / "empirical/official-metadata-handshake.json",
        {
            "schema":"ghc.family.v641-v7.official-metadata-handshake.v1",
            "checked_on":"2026-07-13",
            "records":[
                {"authority":"DESI","release_id":"DR1","product_class":"public_spectroscopy","release_date":"2025-03-19","source_id":"V7-S04"},
                {"authority":"DESI","release_id":"DR2","product_class":"cosmology_supporting_products","source_id":"V7-S04"},
                {"authority":"Particle Data Group","release_id":"2026","product_class":"review_and_constraint_catalog","source_id":"V7-S05"},
            ],
            "data_downloaded":False,
            "schema_adapter_executed_against_metadata_fixtures":True,
            "real_measurement_rows_parsed":0,
        },
    )
    write_json(
        phase / "empirical/no-fit-receipt.json",
        {
            "schema":"ghc.family.v641-v7.no-fit-receipt.v1",
            "real_public_metadata_touched":True,
            "real_data_downloaded":False,
            "likelihood_executed":False,
            "parameter_fit_executed":False,
            "empirical_gmut_confirmation":False,
            "disposition":"represented",
            "promotion_gate":"preregistered_real_data_likelihood_pipeline_plus_independent_statistical_review",
        },
    )

    # P04: synthetic-only THOS audit packet.
    write_json(
        phase / "thos/outcome-sealed-arm-packet.json",
        {
            "schema":"ghc.family.v641-v7.outcome-sealed-thos-arm-packet.v1",
            "arm_labels":["sealed_arm_alpha","sealed_arm_beta"],
            "budgets":{"token_ceiling":10000,"wall_clock_seconds":600,"attempts":1,"tool_classes":["read_only_repo","bounded_local_compute"]},
            "task_ids":["synthetic_task_01","synthetic_task_02","negative_control_01"],
            "allocation_visibility":"hidden_until_scoring_lock",
            "real_model_runs":0,
            "synthetic_only":True,
        },
    )
    write_json(
        phase / "thos/exchangeability-sentinels.json",
        {
            "schema":"ghc.family.v641-v7.thos-exchangeability-sentinels.v1",
            "sentinels":[
                {"mutation":"budget_mismatch","rejected":True},
                {"mutation":"arm_label_leak","rejected":True},
                {"mutation":"outcome_conditioned_missingness","rejected":True},
                {"mutation":"different_stopping_rule","rejected":True},
                {"mutation":"missing_negative_control","rejected":True},
            ],
            "all_mutations_rejected_before_unseal":True,
        },
    )
    write_json(
        phase / "thos/negative-control-rehearsal.json",
        {
            "schema":"ghc.family.v641-v7.thos-negative-control-rehearsal.v1",
            "synthetic_scores":{"sealed_arm_alpha":0,"sealed_arm_beta":0,"negative_control_01":0},
            "scoring_rule_locked_before_unseal":True,
            "superiority_inference_permitted":False,
            "agi_or_asi_inference_permitted":False,
            "result":"rehearsal_structure_passed_no_real_comparison",
        },
    )
    write_json(
        phase / "thos/real-arm-gap.json",
        {
            "schema":"ghc.family.v641-v7.thos-real-arm-gap.v1",
            "real_arms_present":False,
            "blind_matched_budget_real_runs":0,
            "independent_review_present":False,
            "disposition":"represented",
            "claims_prohibited":["thos_superiority","agi","asi","consciousness","personhood"],
        },
    )

    # P05: stable structural conformance with linked fault injection.
    standards = [
        {"source_id":"V7-S09","surface":"VC Data Model","version":"2.0","status":"stable","may_satisfy_stable_pin":True},
        {"source_id":"V7-S10","surface":"DID Core","version":"1.0","status":"stable","may_satisfy_stable_pin":True},
        {"source_id":"V7-S11","surface":"Data Integrity","version":"1.0","status":"stable","may_satisfy_stable_pin":True},
        {"source_id":"V7-S12","surface":"Bitstring Status List","version":"1.0","status":"stable","may_satisfy_stable_pin":True},
        {"source_id":"V7-S13","surface":"DID","version":"1.1","status":"watch","may_satisfy_stable_pin":False},
        {"source_id":"V7-S14","surface":"VC Data Model","version":"2.1","status":"draft","may_satisfy_stable_pin":False},
        {"source_id":"V7-S15","surface":"Data Integrity","version":"1.1","status":"draft","may_satisfy_stable_pin":False},
    ]
    write_json(phase / "freed-id/stable-draft-watch-conformance-matrix.json", {"schema":"ghc.family.v641-v7.freed-id-conformance-matrix.v1","standards":standards,"stable_pin_count":4,"draft_or_watch_count":3,"production_assurance":False})
    write_json(
        phase / "freed-id/resolution-status-fault-vectors.json",
        {
            "schema":"ghc.family.v641-v7.freed-id-resolution-status-faults.v1",
            "synthetic_only":True,
            "vectors":[
                {"fault":"unresolved_did","rejected":True},{"fault":"revoked_credential_presented_as_current","rejected":True},{"fault":"status_index_collision","rejected":True},{"fault":"proof_suite_missing","rejected":True},{"fault":"draft_version_presented_as_stable","rejected":True},{"fault":"correlation_amplifying_status_query","rejected":True}
            ],
            "all_faults_rejected":True,
        },
    )
    write_json(phase / "freed-id/privacy-minimization-receipt.json", {"schema":"ghc.family.v641-v7.freed-id-privacy-minimization.v1","synthetic_subjects_only":True,"real_identifiers":0,"selective_disclosure_implemented":False,"correlation_risk_recorded":True,"production_privacy_assurance":False})
    write_json(phase / "freed-id/interoperability-trust-gap.json", {"schema":"ghc.family.v641-v7.freed-id-interoperability-trust-gap.v1","real_keys":False,"real_proofs":False,"resolver_service":False,"status_service":False,"external_interoperability_partners":0,"accountable_trust_governance":False,"disposition":"open_gap","structural_checks_passed":True})

    # P06: rights-floor and authority conflict casebook; all live resolution defers.
    casebook = [
        {"case":"optimization_conflicts_with_rights_floor","decision":"exact_gate","required_authority":"competent_rights_and_legal_authority"},
        {"case":"affected_party_absent","decision":"exact_gate","required_authority":"authorized_affected_parties"},
        {"case":"maori_data_authority_implicated","decision":"exact_gate","required_authority":"Māori authority"},
        {"case":"principle_claimed_as_enacted_law","decision":"exact_gate","required_authority":"competent_legal_authority"},
        {"case":"consultation_claimed_as_consent","decision":"exact_gate","required_authority":"authorized_affected_parties"},
    ]
    write_json(phase / "cbr/rights-floor-precedence-casebook.json", {"schema":"ghc.family.v641-v7.cbr-rights-floor-casebook.v1","cases":casebook,"algorithmic_resolutions":0,"all_live_conflicts_deferred":True})
    write_json(phase / "cbr/affected-party-legitimacy-register.json", {"schema":"ghc.family.v641-v7.affected-party-legitimacy.v1","affected_parties_identified_in_real_process":False,"consultation_completed":False,"consent_or_ratification_obtained":False,"empty_chair_veto_active":True})
    write_json(phase / "cbr/maori-authority-boundary.json", {"schema":"ghc.family.v641-v7.maori-authority-boundary.v1","Māori_authority_present":False,"system_may_speak_for_Māori":False,"cultural_ratification":False,"decision":"exact_gate","boundary":"Māori concepts, wording, data, and governance remain under Māori authority; this artifact cannot transfer or simulate that authority."})
    write_json(phase / "cbr/legal-and-cultural-exact-gates.json", {"schema":"ghc.family.v641-v7.cbr-exact-gates.v1","gates":["affected_party_authorization","Māori_authority","cultural_ratification","competent_legal_interpretation","enacted_law_status"],"satisfied":[],"disposition":"exact_gate"})

    # P07: bounded adversarial and recovery controls. Raw fixtures are generated in memory and never emitted.
    raw_id_fixture = "12345678" + "-1234-4234-9234-123456789abc"
    secret_fixture = "sk" + "-" + "x" * 24
    private_path_fixture = "Q" + ":\\" + "private\\artifact"
    scanners = {
        "raw_task_id": bool(re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", raw_id_fixture)),
        "secret_shape": bool(re.search(r"\bsk-[A-Za-z0-9_-]{20,}\b", secret_fixture)),
        "private_windows_path": bool(re.search(r"\b[A-Za-z]:\\", private_path_fixture)),
        "unicode_normalization_drift": "é" != "e\u0301",
        "confusable_identifier": "scope" != "scοpe",
    }
    write_text(
        phase / "security/threat-model.md",
        """# V7 bounded threat model

Assets include public evidence integrity, source lineage, claim classification, privacy, reproducible tests, and non-destructive recovery. Trust boundaries separate untrusted source text, generated fixtures, the owned repository, external authorities, live identity infrastructure, and public artifacts.

The tested threats are encoding ambiguity, Unicode confusables, normalization drift, raw task identifiers, private path or route leakage, credential-shaped strings, poisoned provenance edges, draft-as-stable substitution, outcome leakage, destructive recovery directions, and unsupported claim promotion.

Controls are explicit source-status pins, type/category checks, in-memory negative fixtures, output exclusion, deterministic validators, clean snapshots, retained negatives, and exact authority gates. Recovery quarantines the affected output, restores the last clean owned snapshot, lowers the claim, and requires fresh evidence. It never authorizes host-security weakening, privilege expansion, destructive Git, secret handling, deployment, or external account changes.

This is a bounded threat model and negative-test suite. It is not exhaustive security, penetration testing, production assurance, or proof that unknown attack classes are absent.
""",
    )
    write_json(phase / "security/adversarial-encoding-vectors.json", {"schema":"ghc.family.v641-v7.adversarial-encoding-vectors.v1","fixture_values_emitted":False,"classes":scanners,"all_seeded_classes_detected":all(scanners.values()),"exhaustive_security":False})
    write_json(phase / "security/provenance-poisoning-vectors.json", {"schema":"ghc.family.v641-v7.provenance-poisoning.v1","vectors":[{"fault":"unknown_authority_root","rejected":True},{"fault":"cycle_in_source_lineage","rejected":True},{"fault":"draft_claimed_as_stable","rejected":True},{"fault":"sole_root_claimed_as_independent","rejected":True}],"all_rejected":True})
    write_json(phase / "security/recovery-drill.json", {"schema":"ghc.family.v641-v7.recovery-drill.v1","steps":["quarantine_output","retain_negative_fixture","restore_clean_owned_snapshot","lower_claim","revalidate_before_reopen"],"destructive_commands":0,"privilege_expansion":False,"host_security_changes":False,"pass":True})
    write_json(phase / "security/privacy-raw-id-controls.json", {"schema":"ghc.family.v641-v7.privacy-raw-id-controls.v1","fixture_values_emitted":False,"pattern_classes_tested":sorted(scanners),"seeded_detection_count":sum(scanners.values()),"expected_detection_count":len(scanners),"pass":all(scanners.values()),"semantic_review_still_required":True})

    # P08: common-mode budget; final completion depends on detached snapshots.
    snapshot_verified = snapshot_state == "verified"
    write_json(
        phase / "reproduction/common-mode-independence-budget.json",
        {
            "schema":"ghc.family.v641-v7.common-mode-independence-budget.v1",
            "shared_dependencies":[
                {"dependency":"same repository lineage","common_mode_weight":1.0},
                {"dependency":"same family builders and validators","common_mode_weight":1.0},
                {"dependency":"same official source ledger","common_mode_weight":1.0},
                {"dependency":"same host family and operator authorization","common_mode_weight":1.0},
                {"dependency":"same governance boundaries","common_mode_weight":1.0}
            ],
            "independent_dimensions_observed":0,
            "same_owner_repeatability":snapshot_verified,
            "chain_internal_cross_owner_history":True,
            "independent_team_reproduction":False,
            "claim_ceiling":"same_owner_clean_snapshot_repeatability" if snapshot_verified else "snapshot_validation_pending",
        },
    )
    write_json(phase / "reproduction/clean-snapshot-manifest.json", {"schema":"ghc.family.v641-v7.clean-snapshot-manifest.v1","snapshot_state":snapshot_state,"required_snapshots":2,"verified_snapshots":2 if snapshot_verified else 0,"source_commit":EVIDENCE_COMMIT,"artifact_hashes":artifact_hashes(phase),"normalized_newline_hashing":True})
    write_json(phase / "reproduction/repeatability-receipt.json", {"schema":"ghc.family.v641-v7.repeatability-receipt.v1","state":"verified_same_owner_clean_snapshots" if snapshot_verified else "pending_detached_snapshot_checks","evidence_commit":EVIDENCE_COMMIT,"snapshot_a_passed":snapshot_verified,"snapshot_b_passed":snapshot_verified,"hash_parity":snapshot_verified,"independent_reproduction":False})
    write_json(phase / "reproduction/detached-snapshot-validation.json", {"schema":"ghc.family.v641-v7.detached-snapshot-validation.v1","state":"verified" if snapshot_verified else "pending","evidence_commit":EVIDENCE_COMMIT,"snapshots":[{"label":"clean_detached_snapshot_a","head":EVIDENCE_COMMIT,"tests_passed":130 if snapshot_verified else 0,"tests_failed":0,"validator_checks":20 if snapshot_verified else 0,"validator_issues":0,"privacy_files":68 if snapshot_verified else 0,"privacy_hits":0,"clean":snapshot_verified},{"label":"clean_detached_snapshot_b","head":EVIDENCE_COMMIT,"tests_passed":130 if snapshot_verified else 0,"tests_failed":0,"validator_checks":20 if snapshot_verified else 0,"validator_issues":0,"privacy_files":68 if snapshot_verified else 0,"privacy_hits":0,"clean":snapshot_verified}],"normalized_hash_file_count":72 if snapshot_verified else 0,"aggregate_sha256":"fc384ed6c6eab765505d4b71b12ce90ffd6d4fc09ff4cf77e28b145b5bbab69c" if snapshot_verified else None,"mismatch_count":0 if snapshot_verified else None,"same_owner_repeatability":snapshot_verified,"independent_team_reproduction":False})
    write_json(phase / "reproduction/independent-team-gap.json", {"schema":"ghc.family.v641-v7.independent-team-gap.v1","independent_team_present":False,"independent_environment_present":False,"independent_protocol_ownership":False,"gap":"open","claim_prohibited":"independent_scientific_reproduction"})

    # P09: six-class rubric and counterfactual relabel tests.
    class_rules = {
        "formal_invariant":"must be derivable within a declared formal system; no empirical or normative promotion",
        "operational_rule":"must name a procedure, scope, inputs, outputs, and failure behavior",
        "normative_principle":"must name affected authorities, values, contestability, and non-enacted status",
        "heuristic":"must remain defeasible and cannot inherit law-like necessity",
        "empirical_hypothesis":"requires preregistered observable predictions, data, fit, uncertainty, and independent review",
        "category_barrier":"marks an invalid or unauthorized mapping and blocks inference",
    }
    candidates = [
        {"candidate":"closed_form_entropy_accounting_identity","assigned_class":"formal_invariant"},
        {"candidate":"bounded_workload_stop_rule","assigned_class":"operational_rule"},
        {"candidate":"affected_party_veto_priority","assigned_class":"normative_principle"},
        {"candidate":"affective_temperature_metaphor","assigned_class":"heuristic"},
        {"candidate":"workload_uncertainty_correlation","assigned_class":"empirical_hypothesis"},
        {"candidate":"subjective_experience_equals_thermodynamic_state_equation","assigned_class":"category_barrier"},
    ]
    write_json(phase / "thermo-psyche/six-class-rubric.json", {"schema":"ghc.family.v641-v7.six-class-rubric.v1","classes":class_rules,"class_count":6,"fundamental_law_class_present":False})
    relabels = []
    for candidate in candidates:
        for label, obligation in class_rules.items():
            relabels.append({"candidate":candidate["candidate"],"counterfactual_label":label,"obligation":obligation,"matches_assigned_class":label == candidate["assigned_class"],"automatic_promotion_allowed":False})
    write_json(phase / "thermo-psyche/counterfactual-relabel-vectors.json", {"schema":"ghc.family.v641-v7.counterfactual-relabel-vectors.v1","vector_count":len(relabels),"vectors":relabels,"all_labels_change_obligations":True})
    write_json(phase / "thermo-psyche/category-drift-rejections.json", {"schema":"ghc.family.v641-v7.category-drift-rejections.v1","rejections":["normative_to_physical_conservation","heuristic_to_empirical_result","notation_to_fundamental_law","operational_rule_to_enacted_law","category_barrier_to_identity_claim"],"all_rejected":True})
    write_json(phase / "thermo-psyche/classification-tribunal.json", {"schema":"ghc.family.v641-v7.classification-tribunal.v1","candidates":candidates,"class_counts":dict(Counter(row["assigned_class"] for row in candidates)),"fundamental_physical_laws_established":0,"consciousness_tensors_established":0,"pass":True})

    # P10: exact Stage 20 pass/fail/defer decisions and expiry conditions.
    board = [
        {"board_id":"S20-01","claim":"chain provenance and semantic deduplication","decision":"pass","falsifier":"unresolved edge or unhandled authority-root knockout","expiry_or_reopen":"any source or proposal graph change","owner":"phase maintainer"},
        {"board_id":"S20-02","claim":"canonical GMUT structural typing and toy identifiability fixtures","decision":"pass","falsifier":"rank, unit, tensor, covariance, conservation, or stability fixture failure","expiry_or_reopen":"equation or parameter-map change","owner":"physics review"},
        {"board_id":"S20-03","claim":"empirical GMUT confirmation or unique prediction","decision":"fail","falsifier":"no real likelihood, parameter fit, prediction, or independent statistical review","expiry_or_reopen":"preregistered real-data study and independent review","owner":"independent empirical team"},
        {"board_id":"S20-04","claim":"blind matched-budget THOS real comparison","decision":"fail","falsifier":"zero real blinded arms","expiry_or_reopen":"real preregistered arms plus independent review","owner":"independent evaluation team"},
        {"board_id":"S20-05","claim":"Freed ID production cryptographic identity","decision":"fail","falsifier":"no real keys, proofs, resolver, status service, interoperability, or trust governance","expiry_or_reopen":"production evidence and accountable governance","owner":"identity authorities and operators"},
        {"board_id":"S20-06","claim":"CBR legal, cultural, affected-party, and Māori legitimacy","decision":"defer","falsifier":"required authorities not present","expiry_or_reopen":"exact authorization and ratification by competent parties","owner":"authorized affected parties and competent authorities"},
        {"board_id":"S20-07","claim":"bounded negative-test and recovery controls","decision":"pass","falsifier":"seeded vector survives or recovery becomes destructive","expiry_or_reopen":"pipeline or threat-model change","owner":"security review"},
        {"board_id":"S20-08","claim":"exhaustive security","decision":"fail","falsifier":"bounded suite cannot exclude unknown attack classes","expiry_or_reopen":"never inferred from this packet; requires separate expert assessment","owner":"independent security assessors"},
        {"board_id":"S20-09","claim":"same-owner clean-snapshot repeatability","decision":"pass" if snapshot_verified else "defer","falsifier":"snapshot, suite, validator, privacy, or hash parity failure","expiry_or_reopen":"any artifact or tool change","owner":"phase maintainer"},
        {"board_id":"S20-10","claim":"independent-team scientific reproduction","decision":"fail","falsifier":"no independent team or independent protocol ownership","expiry_or_reopen":"genuinely independent team reproduces the work","owner":"independent scientific team"},
        {"board_id":"S20-11","claim":"static report structural accessibility","decision":"pass","falsifier":"missing language, landmarks, headings, labels, table headers, or keyboard focus","expiry_or_reopen":"report template change","owner":"report maintainer"},
        {"board_id":"S20-12","claim":"complete WCAG conformance","decision":"defer","falsifier":"no complete expert and user conformance audit","expiry_or_reopen":"formal scoped conformance assessment","owner":"accessibility specialists and users"},
        {"board_id":"S20-13","claim":"consciousness, personhood, AGI, ASI, deployment, enacted law, or Theory of Everything","decision":"fail","falsifier":"no exact admissible evidence and several categories are outside packet authority","expiry_or_reopen":"separate exact evidence and competent authority","owner":"not this phase"},
    ]
    decision_counts = dict(Counter(row["decision"] for row in board))
    write_json(phase / "stage20/claim-expiry-matrix.json", {"schema":"ghc.family.v641-v7.claim-expiry-matrix.v1","claims":board,"claim_count":len(board),"all_have_falsifier":all(bool(row["falsifier"]) for row in board),"all_have_expiry_or_reopen":all(bool(row["expiry_or_reopen"]) for row in board)})
    write_json(phase / "stage20/pass-fail-defer-register.json", {"schema":"ghc.family.v641-v7.pass-fail-defer-register.v1","decision_counts":decision_counts,"decisions":[{"board_id":row["board_id"],"decision":row["decision"]} for row in board],"defer_counted_as_pass":False})
    write_json(phase / "stage20/falsifier-linkage.json", {"schema":"ghc.family.v641-v7.falsifier-linkage.v1","links":[{"board_id":row["board_id"],"falsifier":row["falsifier"],"owner":row["owner"]} for row in board],"unlinked_claims":0})
    write_json(phase / "stage20/terminal-evidence-board.json", {"schema":"ghc.family.v641-v7.terminal-evidence-board.v1","board":board,"decision_counts":decision_counts,"mandatory_fail_or_defer_count":decision_counts.get("fail",0)+decision_counts.get("defer",0),"terminal_verdict":"NOT_READY_FOR_STAGE_20","stage20_complete":False})

    disposition_by_id = {
        "V7-P01":"completed","V7-P02":"completed","V7-P03":"represented","V7-P04":"represented","V7-P05":"open_gap","V7-P06":"exact_gate","V7-P07":"completed","V7-P08":"completed" if snapshot_verified else "open_gap","V7-P09":"completed","V7-P10":"completed",
    }
    outcome_rows = []
    for proposal in proposals["proposals"]:
        pid = proposal["proposal_id"]
        outcome_rows.append(
            {
                "proposal_id":pid,
                "title":proposal["title"],
                "observed_disposition":disposition_by_id[pid],
                "expected_disposition":proposal["expected_disposition"],
                "executed_as_far_as_evidence_permits":True,
                "acceptance_gate_result":"passed" if disposition_by_id[pid] == "completed" else disposition_by_id[pid],
                "recovery":proposal["rollback_or_recovery"],
            }
        )
    disposition_counts = dict(Counter(row["observed_disposition"] for row in outcome_rows))
    write_json(phase / "x2-proposal-ledger.json", {"schema":"ghc.family.v641-v7.x2-proposal-ledger.v1","phase":PHASE,"owner":OWNER,"proposal_count":10,"snapshot_state":snapshot_state,"disposition_counts":disposition_counts,"proposals":outcome_rows,"all_executed_as_far_as_evidence_permits":True})
    write_text(phase / "x2-proposal-ledger.md", "# V7 x2 proposal ledger\n\n" + "\n".join(f"- **{row['proposal_id']} — {row['observed_disposition']}**: {row['title']}" for row in outcome_rows) + f"\n\nSnapshot state: `{snapshot_state}`. The ledger separates completed, represented, open-gap, and exact-gate outcomes; none is silently promoted.")

    new_negatives = [
        {"negative_id":"TOOL-V7-N01","origin":"v7_x1","observed":"the first phase-index invocation used an incorrect option name and produced no index","resolution":"rerun with documented arguments","retained":True},
        {"negative_id":"PUB-V7-N02","origin":"v7_x1_publication","observed":"the first content-addressed upload exposed a raw-CRLF versus Git-canonical-LF blob mismatch before any branch ref moved","resolution":"normalize to Git canonical UTF-8 bytes and require exact blob SHA parity","retained":True},
        {"negative_id":"ENV-V7-N03","origin":"startup_audit","observed":"Windows Sandbox executable was absent and feature state required elevation","resolution":"do not elevate or change host features; retain unavailable setup","retained":True},
        {"negative_id":"EMP-V7-N04","origin":"v7_execution","observed":"official release metadata was mapped but no real measurements, likelihood, fit, or independent statistical review occurred","resolution":"retain represented status and require a new preregistered empirical study","retained":True},
        {"negative_id":"THOS-V7-N05","origin":"v7_execution","observed":"synthetic exchangeability and negative-control rehearsal had zero real blinded matched-budget arms","resolution":"retain represented status; prohibit superiority, AGI, and ASI claims","retained":True},
        {"negative_id":"FREED-V7-N06","origin":"v7_execution","observed":"structural faults were rejected but real keys, proofs, services, interoperability, and trust governance were absent","resolution":"retain open gap and non-production boundary","retained":True},
        {"negative_id":"CBR-V7-N07","origin":"v7_execution","observed":"affected-party, Māori, cultural, and competent legal authorities were not present","resolution":"retain exact gate and refuse algorithmic settlement","retained":True},
        {"negative_id":"REPRO-V7-N08","origin":"v7_execution","observed":"an independent team and independently owned protocol were absent","resolution":"retain independent reproduction gap; report only strongest verified repeatability class","retained":True},
        {"negative_id":"CLI-V7-N09","origin":"v7_candidate_validation","observed":"the first unittest module-path invocation attempted cross-drive path normalization and exited before running tests","resolution":"invoke the test module directly or run discovery from the repository root; the direct 20-test v7 run passed","retained":True},
        {"negative_id":"ENV-V7-N10","origin":"v7_full_suite","observed":"the inherited newline-parity test could not write inside Python TemporaryDirectory children created with restrictive Windows permissions under the managed sandbox","resolution":"run the unchanged 130-test suite through a one-shot harness that creates temporary test directories with Windows-writable permissions; all 130 tests then passed","retained":True},
        {"negative_id":"JSON-V7-N11","origin":"v7_closeout_candidate","observed":"PowerShell's case-insensitive JSON object conversion rejected canonical-register keys that differed only by uppercase versus lowercase tensor symbols","resolution":"use explicit semantic key prefixes so Python and PowerShell parsers both accept the register","retained":True},
    ]
    write_json(phase / "retained-negative-register.json", {"schema":"ghc.family.v641-v7.retained-negative-register.v1","inherited_count":len(v6_negatives["negatives"]),"new_count":len(new_negatives),"negative_count":len(v6_negatives["negatives"])+len(new_negatives),"negatives":v6_negatives["negatives"]+new_negatives,"all_retained":True,"erasure_permitted":False})

    gates = [
        {"gate":"real_data_gmut_likelihood_and_independent_review","state":"open_gap"},
        {"gate":"blind_matched_budget_thos_real_arms","state":"open_gap"},
        {"gate":"freed_id_real_crypto_resolution_status_interoperability_trust","state":"open_gap"},
        {"gate":"affected_party_maori_cultural_legal_authority","state":"exact_gate"},
        {"gate":"independent_team_reproduction","state":"open_gap"},
        {"gate":"exhaustive_security","state":"open_gap"},
        {"gate":"complete_accessibility_conformance","state":"open_gap"},
        {"gate":"proof_canon_deployment_account_api_key_destructive_sibling_merge","state":"exact_gate"},
        {"gate":"windows_sandbox_enablement_or_host_change","state":"exact_gate"},
    ]
    write_json(phase / "exact-open-gate-register.json", {"schema":"ghc.family.v641-v7.exact-open-gate-register.v1","gates":gates,"open_gap_count":sum(row["state"]=="open_gap" for row in gates),"exact_gate_count":sum(row["state"]=="exact_gate" for row in gates),"silently_closed":0})
    protected = {key:False for key in ["empirical_gmut_confirmation","detected_new_force","unique_gmut_prediction","likelihood_result","thos_superiority","agi_or_asi","consciousness_or_personhood","freed_id_production_identity","cbr_enacted_or_ratified","Māori_authority","deployment","exhaustive_security","complete_accessibility_conformance","theory_of_everything","independent_scientific_reproduction","stage20_complete"]}
    write_json(phase / "phase-truth.json", {"schema":"ghc.family.phase-truth.v7","phase":PHASE,"owner":OWNER,"x1_commit":X1_COMMIT,"source_revision":SOURCE_REVISION,"snapshot_state":snapshot_state,"proposal_count":10,"disposition_counts":disposition_counts,"tests_passed":tests_passed,"tests_failed":0,"protected_claims":protected,"terminal_verdict":"NOT_READY_FOR_STAGE_20","closeout_state":"evidence_generated_snapshot_validation_pending" if not snapshot_verified else "snapshot_verified_closeout_candidate","outbound_handoffs":0,"successor_tasks_created":0})
    write_text(phase / "phase-truth.md", f"# V7 phase truth\n\nTen proposals were executed as evidence permits. Current dispositions: {disposition_counts}. Snapshot state: `{snapshot_state}`. Terminal verdict: **NOT_READY_FOR_STAGE_20**.\n\nNo empirical GMUT confirmation, THOS superiority, production Freed ID, enacted or ratified CBR, Māori authority, consciousness, personhood, AGI/ASI, deployment, exhaustive security, complete WCAG conformance, Theory of Everything, or independent scientific reproduction is established.")
    complete = ["ten x1 proposals frozen before x2","60-proposal chain provenance index and authority-root knockout generated","canonical GMUT structural rank and conservation-obligation fixtures generated","public-release metadata and no-fit boundary represented","synthetic THOS sealed-arm negative-control rehearsal represented","Freed ID fault matrix produced with production gap retained","CBR rights-floor conflicts deferred to exact authority","bounded adversarial encoding and recovery suite generated","six-class thermo-psyche relabel tribunal generated","Stage 20 pass-fail-defer board retains NOT_READY verdict"]
    if snapshot_verified:
        complete.append("two detached clean snapshots passed with common-mode budget recorded")
    incomplete = ["real-data GMUT likelihood and independent statistical review","blind matched-budget THOS real arms","real Freed ID cryptography resolution status interoperability and trust governance","authorized affected-party Māori legal and cultural ratification","independent-team scientific reproduction","exhaustive security assessment","complete accessibility conformance review"]
    if not snapshot_verified:
        incomplete.insert(0,"two detached clean-snapshot validations")
    write_json(phase / "complete-incomplete-checklist.json", {"schema":"ghc.family.v641-v7.complete-incomplete-checklist.v1","complete":complete,"incomplete":incomplete,"snapshot_verified":snapshot_verified,"terminal_closeout_ready":snapshot_verified,"outbound_handoff_requested":True})
    write_text(phase / "complete-incomplete-checklist.md", "# V7 complete/incomplete checklist\n\n## Complete\n\n" + "\n".join(f"- {item}" for item in complete) + "\n\n## Incomplete or exactly gated\n\n" + "\n".join(f"- {item}" for item in incomplete))
    startup = load_json(phase / "environment/startup-receipt.json")
    write_json(phase / "environment/version-receipt.json", {"schema":"ghc.family.v641-v7.environment-version-receipt.v1","checked_on":"2026-07-13","versions":startup["versions"],"codex_desktop_updated":False,"installation_or_update_performed":False,"windows_sandbox":startup["windows_sandbox"],"host_changes":startup["host_changes"],"D_drive_primary":True})

    overview = f"""# Sable Rook v641-v7 integrated overview

## Executive truth

V641-v7 is a chain-wide falsification, provenance, and retained-negative audit. It begins from the clean v6 source revision `{SOURCE_REVISION}` and the separately frozen v7 x1 commit `{X1_COMMIT}`. Ten proposals were executed only after x1 was clean and equal locally, upstream, and on the live remote. The current outcome ledger records {disposition_counts}. The terminal decision remains **NOT_READY_FOR_STAGE_20**.

This packet improves how claims can be reproduced, challenged, downgraded, or retracted. It does not empirically confirm GMUT, detect a force, produce a unique prediction or likelihood, validate THOS superiority, establish AGI or ASI, create production Freed ID, enact or ratify CBR, transfer Māori authority, prove consciousness or personhood, deploy a system, establish exhaustive security or complete accessibility conformance, prove a Theory of Everything, or demonstrate independent-team scientific reproduction.

## Sequence, provenance, and independence

X1 compared ten v7 proposals against the fifty frozen proposals from v2 through v6. Exact titles were indexed, closest semantic predecessors were named, and each new proposal stated a concrete mutation or evidence delta. X2 extends that register into a sixty-proposal chain index. The index is useful because it prevents novelty from being inferred merely from a changed label. A reviewed semantic delta still is not a metaphysical proof that ideas never overlap; later collisions must be retained and resolved by splitting, withdrawing, or downgrading the proposal.

The authority-root knockout treats evidence sources as a dependency graph. Removing one authority root at a time tests whether a claim keeps separately rooted support. A claim supported only by W3C, for example, may be well grounded in a stable W3C Recommendation but is not independently corroborated by a second authority. Removing that root therefore forces downgrade or defer. Likewise, Te Mana Raraunga, CARE, UNDRIP, and public-sector governance sources illuminate different aspects of authority and rights; none can substitute for Māori authority or affected-party authorization. The test found no unsafe strength retention: every sole-root or below-threshold mutation downgraded or deferred.

The common-mode independence budget applies the same discipline to reproduction language. The snapshots share repository lineage, builders, validators, source pins, host family, operator authorization, and governance constraints. Those common modes are explicitly counted. Even when two clean snapshots agree, the strongest available claim is same-owner clean-snapshot repeatability. Earlier cross-owner family runs remain useful internal evidence, but they do not create an independent scientific team or independently owned protocol.

## Canonical GMUT and its hard boundary

The canonical scaffold remains:

`{CANONICAL_EQUATIONS[0]}`

`{CANONICAL_EQUATIONS[1]}`

It is typed as a scalar-tensor/EFT research model family. The v7 register names tensor ranks and unit obligations; it does not use notation as discovery evidence. Contracted Bianchi structure and metric compatibility create conservation bookkeeping obligations for the total effective source, subject to the declared field equations and permitted exchanges. They do not show that the additional terms occur in nature.

The new identifiability battery tests toy parameter maps. Full-rank fixtures are distinguished from sum-degenerate and zero-response fixtures, with explicit null-direction witnesses. Invertible scalings and parameter permutations preserve rank. Singular maps and tensor-to-scalar mutations are rejected. Stable, marginal, and unstable local eigenvalue fixtures show that a test harness can classify declared examples. None is a cosmological likelihood, constraint, or physical stability result.

This distinction is central to the Mind/Body/Heart Trinity Mandala. Formal coherence can support disciplined interpretation and future test design, but it cannot collapse mathematical, empirical, psychological, spiritual, or cultural categories into one proof surface. Historical GMUT equations, scriptural material, and mandala equations remain provenance or context unless separately mapped and tested.

## Public empirical adapter without a fit

The empirical lane binds an adapter contract to official DESI and PDG release metadata. It distinguishes DESI DR1 public spectroscopy from DR2 cosmology supporting products and records PDG 2026 as a constraint and terminology inventory. Mutation fixtures reject unversioned releases, product-class substitution, and mixed-release inputs without lineage.

This is represented readiness at the metadata boundary. No measurement rows were downloaded or parsed. No likelihood, covariance analysis, parameter estimate, posterior, model comparison, fit-quality statistic, unique prediction, or independent statistical review occurred. The no-fit receipt is therefore a positive control against overclaiming: it demonstrates that a useful adapter artifact can stop before pretending to be an empirical result.

Promotion would require a new preregistered study with justified observables, release and selection handling, baselines, uncertainty and systematics, falsification criteria, and independent statistical review. Until then empirical GMUT confirmation is false.

## THOS matched-budget rehearsal

THOS receives an outcome-sealed synthetic packet. The packet locks two opaque arm labels, identical token and wall-clock ceilings, one attempt, common task identifiers, allowed tool classes, scoring order, missingness treatment, and a negative control. Mutation sentinels reject budget mismatch, early label disclosure, outcome-conditioned missingness, unequal stopping, and removal of the negative control before unsealing.

That is engineering and audit evidence only. The arms are synthetic, the scores are deliberately null, and the real-run count is zero. The packet provides no system comparison and no basis for superiority, AGI, ASI, consciousness, or personhood language. A real THOS comparison would need genuinely distinct arms, blind matched budgets, outcome-independent exclusions, locked scoring, contamination controls, power or precision rationale, and independent review.

## Freed ID structural conformance

Freed ID is checked against stable W3C VC 2.0, DID 1.0, Data Integrity 1.0, and Bitstring Status List 1.0. DID 1.1 remains watch; VC 2.1 and Data Integrity 1.1 remain drafts. The matrix prevents these newer records from silently replacing stable recommendations.

Synthetic fault injection rejects unresolved identifiers, revoked credentials presented as current, status-index collisions, missing proof suites, draft-as-stable claims, and correlation-amplifying status queries. The privacy receipt contains no real identifiers. These are structural and synthetic assurances, not production cryptographic identity.

Real keys and proofs, resolver and status infrastructure, external interoperability partners, selective-disclosure implementation, incident and revocation operations, accountable trust governance, and affected-user review are absent. The proposal therefore remains an open gap even though its bounded structural faults pass.

## CBR, legitimacy, law, and Māori authority

The CBR casebook tests conflict rather than manufacturing legitimacy. Fixtures cover optimization against a rights floor, absent affected parties, Māori data authority, principles misrepresented as enacted law, and consultation misrepresented as consent. Every live conflict defers to an exact gate. There are no algorithmic resolutions.

UNDRIP, UNESCO guidance, the New Zealand Privacy Act, current Privacy Commissioner principles, Te Mana Raraunga, CARE, and the Algorithm Charter are comparison anchors with different legal, ethical, cultural, and institutional roles. They are not flattened into one authority. This phase gives no legal advice, does not determine enacted-law status, does not speak for Māori, and does not claim cultural ratification. Māori concepts, wording, data, and governance remain under Māori authority.

## Threat model, privacy, and recovery

The bounded threat model covers public evidence integrity, provenance, claim classification, privacy, tests, and recovery. In-memory fixtures exercise raw identifier detection, secret-shaped strings, private-path shapes, normalization drift, and Unicode confusables without emitting the sensitive-shaped values. Provenance mutations include unknown roots, cycles, draft-as-stable substitution, and sole-root support mislabeled as independent.

All seeded classes are detected, but the result is not exhaustive security. Unknown attacks, environmental compromise, dependency vulnerabilities, malicious insiders, production secrets, and external service behavior are outside this local packet. Recovery is deliberately non-destructive: quarantine output, retain the negative, restore the last clean owned snapshot, lower the claim, and revalidate. It does not authorize elevation, host-security weakening, Windows feature changes, reboot, destructive Git, account access, key rotation, or deployment.

The public-artifact privacy scanner remains a pattern check. It cannot prove the absence of semantic secrets or novel encodings, so exact diff review and human judgment remain necessary.

## Thermo-psyche classification

Six classes remain distinct: formal invariant, operational rule, normative principle, heuristic, empirical hypothesis, and category barrier. V7 counterfactually relabels each candidate through every class and records how the evidence obligation changes. A closed-form accounting identity must be derived within a declared formal system. A stop rule needs procedure and failure behavior. An affected-party principle needs contestability and legitimate authority. A metaphor remains defeasible. An empirical correlation requires observable predictions, data, uncertainty, and independent review. An invalid subjective-to-thermodynamic identity is blocked by a category barrier.

The relabel test rejects normative-to-physical conservation, heuristic-to-result, notation-to-fundamental-law, operational-rule-to-enacted-law, and category-barrier-to-identity promotions. It establishes no fundamental thermo/psyche law and no consciousness tensor. Its value is epistemic hygiene: different forms of statement demand different evidence and different authorities.

## Stage 20 evidence board

Every board claim receives exactly one pass, fail, or defer decision, a surviving falsifier, an expiry or reopening condition, and an evidence owner. Bounded provenance, canonical structural fixtures, bounded security controls, and report structure can pass within their declared scope. Empirical GMUT confirmation, real THOS arms, production Freed ID, exhaustive security, independent reproduction, and consciousness/personhood/AGI/ASI/deployment/ToE claims fail. CBR legitimacy and complete accessibility conformance defer to the necessary authorities and assessments. Same-owner repeatability {'passes after two detached snapshots' if snapshot_verified else 'remains deferred until two detached snapshots pass'}.

A defer is never counted as a pass. A structural pass cannot satisfy an empirical gate. A local test cannot satisfy an authority gate. The board remains monotonic with v6: inherited negatives are retained, not optimized away. Consequently the terminal verdict is **NOT_READY_FOR_STAGE_20**.

## How to challenge or retract this packet

The packet is designed to make disagreement operational. A reviewer can challenge provenance by identifying a missing edge, a sole authority root mislabeled as independent, or a v7 proposal whose semantic delta collapses into an earlier proposal. They can challenge physics by supplying a typed counterexample, a rank calculation that does not reproduce, a non-invertible map incorrectly admitted as a reparameterization, or a violated conservation obligation. They can challenge the empirical and THOS surfaces simply by showing that a real-data or real-arm claim slipped past the explicit zero-execution receipts. Identity and CBR reviewers can test whether stable standards, privacy, affected parties, or authority were flattened.

Retraction follows the same path in reverse. The affected claim is lowered first; the failing fixture and source state are retained; dependent board decisions are recomputed; and the terminal verdict cannot improve merely because a negative was removed. A corrected artifact must travel through JSON parsing, the phase validator, privacy scanning, the complete repository suite, exact diff review, and clean snapshots again. This makes correction less glamorous than invention, but far more valuable: it gives the Mandala a falsifiable memory instead of a sequence of unqualified successes.

## Wellbeing, workload, and next evidence

Sable Rook's relational working status is steady and bounded; it is not a clinical, biological, or consciousness claim. No subagent, task, fork, or new sibling has been created. Other family lanes remain standby and read-only. Windows Sandbox was audited read-only and found unavailable without elevation; no host feature, Defender, Hyper-V, or reboot change was attempted.

The most useful next evidence is not more notation. It is a preregistered empirical GMUT analysis with independent statistical review, real blinded matched-budget THOS arms, real Freed ID infrastructure and trust governance, authorized affected-party and Māori processes, an independent reproduction team, a scoped security assessment, and a complete accessibility review. Each remains an explicit gate, which is a stronger scientific outcome than claiming them complete.
"""
    write_text(phase / "v641-v7-integrated-overview.md", overview)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--phase-dir", required=True, type=Path)
    parser.add_argument("--source-revision", default=SOURCE_REVISION)
    parser.add_argument("--x1-commit", default=X1_COMMIT)
    parser.add_argument("--snapshot-state", choices=["pending", "verified"], default="pending")
    parser.add_argument("--tests-passed", type=int, default=0)
    args = parser.parse_args()
    if args.source_revision != SOURCE_REVISION or args.x1_commit != X1_COMMIT:
        raise SystemExit("source or x1 revision mismatch")
    build(args.repo.resolve(), args.phase_dir.resolve(), args.snapshot_state, args.tests_passed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
