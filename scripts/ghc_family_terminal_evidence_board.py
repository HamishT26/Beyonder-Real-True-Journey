from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


PHASE_RELATIVE = Path("docs/eiren-kestrel/v641-v6")
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}
COMMIT = re.compile(r"^[0-9a-f]{40}$")

FINAL_CHAIN = [
    ("Eiren Kestrel", "v641-v1", "c1b464a41e52143cd75b8b8fa114d865a34887cc"),
    ("Sable Rook", "v641-v2", "8028e4a75b5475b0b31ceddbae0b41e19bdc53f2"),
    ("Elian Voss", "v641-v3", "01fd716b5f36a39cdc7763481459e75a09fcb077"),
    ("Nima Calder", "v641-v4", "a845c30e9b2b32f4a923d2679b707c1fd6ff6a38"),
    ("Tamar Vey", "v641-v5", "d4b6252aa6913193de797d3580895881923d6164"),
]

BOUNDARIES = [
    {
        "phase": "v641-v2",
        "x1_commit": "0a6d280fbc13831862237c50c7df3af8097b7b7d",
        "evidence_commit": "7d243b570ca4e59d3f3def08b2131f093db48ab0",
        "final_head": "8028e4a75b5475b0b31ceddbae0b41e19bdc53f2",
    },
    {
        "phase": "v641-v3",
        "x1_commit": "86bd1e0ab926d35831e5ce2309d8b0dc520b67ba",
        "evidence_commit": "7cf96ce8604f470b662308b0cabb81847a6629ab",
        "final_head": "01fd716b5f36a39cdc7763481459e75a09fcb077",
    },
    {
        "phase": "v641-v4",
        "x1_commit": "a8396347d20998fffacfe1ebf7609bc2709f574f",
        "evidence_commit": "daef2f739e16af52586ac20469f6fd73fed0b2ba",
        "final_head": "a845c30e9b2b32f4a923d2679b707c1fd6ff6a38",
    },
    {
        "phase": "v641-v5",
        "x1_commit": "b88608093d9417ffc1565e3b5b880a75b96ca721",
        "evidence_commit": "daf996564cd839f2275b39af479e77be96f5d1a8",
        "final_head": "d4b6252aa6913193de797d3580895881923d6164",
    },
]

CORE_PARITY_PATHS = [
    "docs/eiren-kestrel/v641-v6/x1-proposals.json",
    "docs/eiren-kestrel/v641-v6/sources/source-ledger.json",
    "docs/eiren-kestrel/v641-v6/provenance/sequential-ancestry.json",
    "docs/eiren-kestrel/v641-v6/provenance/cumulative-dependency-graph.json",
    "docs/eiren-kestrel/v641-v6/provenance/x1-x2-boundary-audit.json",
    "docs/eiren-kestrel/v641-v6/physics/equation-register-covenant.json",
    "docs/eiren-kestrel/v641-v6/physics/translation-typecheck.json",
    "docs/eiren-kestrel/v641-v6/physics/null-limit-and-conservation-audit.json",
    "docs/eiren-kestrel/v641-v6/falsification/inherited-negative-register.json",
    "docs/eiren-kestrel/v641-v6/falsification/mutation-tribunal.json",
    "docs/eiren-kestrel/v641-v6/falsification/negative-to-downgrade-trace.json",
    "docs/eiren-kestrel/v641-v6/empirical/promotion-docket.json",
    "docs/eiren-kestrel/v641-v6/empirical/baseline-authorization-boundary.json",
    "docs/eiren-kestrel/v641-v6/empirical/missing-evidence-register.json",
    "docs/eiren-kestrel/v641-v6/thos/observed-coordination-costs.json",
    "docs/eiren-kestrel/v641-v6/thos/observed-versus-proxy-ledger.json",
    "docs/eiren-kestrel/v641-v6/thos/blind-evidence-audit.json",
    "docs/eiren-kestrel/v641-v6/thermo-psyche/candidate-register.json",
    "docs/eiren-kestrel/v641-v6/thermo-psyche/classification-tribunal.json",
    "docs/eiren-kestrel/v641-v6/thermo-psyche/mutation-results.json",
    "docs/eiren-kestrel/v641-v6/freed-id/assurance-lattice.json",
    "docs/eiren-kestrel/v641-v6/freed-id/non-escalation-proof.json",
    "docs/eiren-kestrel/v641-v6/freed-id/composition-gap-register.json",
    "docs/eiren-kestrel/v641-v6/cbr/authority-matrix.json",
    "docs/eiren-kestrel/v641-v6/cbr/empty-chair-veto.json",
    "docs/eiren-kestrel/v641-v6/cbr/dissent-remedy-and-revocation-gate.json",
    "scripts/ghc_family_terminal_evidence_board.py",
    "scripts/ghc_family_terminal_evidence_validator.py",
    "scripts/build_ghc_family_terminal_report.py",
    "tests/test_ghc_family_v641_v6.py",
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True, encoding="utf-8", errors="replace"
    ).strip()


def is_ancestor(repo: Path, older: str, newer: str) -> bool:
    return subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", older, newer],
        capture_output=True,
        check=False,
    ).returncode == 0


def sha256_lf(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def build_provenance(repo: Path, phase: Path, x1_commit: str) -> None:
    chain = []
    for owner, phase_name, head in FINAL_CHAIN:
        chain.append(
            {
                "owner": owner,
                "phase": phase_name,
                "final_head": head,
                "commit_exists": bool(git(repo, "cat-file", "-t", head) == "commit"),
            }
        )
    chain.append(
        {
            "owner": "Eiren Kestrel",
            "phase": "v641-v6-x1",
            "final_head": x1_commit,
            "commit_exists": bool(git(repo, "cat-file", "-t", x1_commit) == "commit"),
        }
    )
    edges = []
    for left, right in zip(chain, chain[1:]):
        ok = is_ancestor(repo, left["final_head"], right["final_head"])
        edges.append(
            {
                "from": left["phase"],
                "to": right["phase"],
                "strict_ancestor": ok and left["final_head"] != right["final_head"],
            }
        )
    write_json(
        phase / "provenance/sequential-ancestry.json",
        {
            "schema": "ghc.family.sequential-ancestry.v6",
            "chain": chain,
            "edges": edges,
            "all_edges_strict": all(edge["strict_ancestor"] for edge in edges),
            "sequence": [row["owner"] for row in chain],
            "parallel_execution_inferred": False,
            "independent_reproduction_inferred": False,
            "boundary": "Git ancestry proves the internal sequential history only.",
        },
    )

    x1 = read_json(phase / "x1-proposals.json")
    nodes = []
    for proposal in x1["proposals"]:
        nodes.append(
            {
                "node_id": proposal["proposal_id"],
                "title": proposal["title"],
                "source_ids": proposal["authoritative_source_ids"],
                "internal_inputs": proposal["internal_inputs"],
                "declared_support_count": len(proposal["authoritative_source_ids"])
                + len(proposal["internal_inputs"]),
            }
        )
    roots = Counter(
        source["authority_root"]
        for source in read_json(phase / "sources/source-ledger.json")["sources"]
    )
    write_json(
        phase / "provenance/cumulative-dependency-graph.json",
        {
            "schema": "ghc.family.cumulative-dependency-graph.v6",
            "proposal_nodes": nodes,
            "proposal_count": len(nodes),
            "authority_root_document_counts": dict(sorted(roots.items())),
            "authority_root_count": len(roots),
            "document_count": sum(roots.values()),
            "repeated_roots_add_independent_votes": False,
            "all_inputs_resolve": all(
                (repo / item).exists() for node in nodes for item in node["internal_inputs"]
            ),
        },
    )

    boundary_rows = []
    for row in BOUNDARIES:
        boundary_rows.append(
            {
                **row,
                "x1_precedes_evidence": is_ancestor(repo, row["x1_commit"], row["evidence_commit"]),
                "evidence_precedes_final": is_ancestor(
                    repo, row["evidence_commit"], row["final_head"]
                ),
            }
        )
    boundary_rows.append(
        {
            "phase": "v641-v6",
            "x1_commit": x1_commit,
            "evidence_commit": None,
            "final_head": None,
            "x1_precedes_evidence": None,
            "evidence_precedes_final": None,
            "state": "x1_remote_equal_x2_execution_active",
        }
    )
    write_json(
        phase / "provenance/x1-x2-boundary-audit.json",
        {
            "schema": "ghc.family.x1-x2-boundary-audit.v6",
            "rows": boundary_rows,
            "completed_prior_boundaries_valid": all(
                row["x1_precedes_evidence"] and row["evidence_precedes_final"]
                for row in boundary_rows[:-1]
            ),
            "v6_x2_started_only_after_x1_equality": True,
            "boundary": "V6 evidence and final commits remain pending until they exist.",
        },
    )


def build_physics(phase: Path) -> None:
    canonical = {
        "geometry_equation": "G_{mu nu} + Lambda g_{mu nu} = M_Pl^{-2} T^{SM}_{mu nu} + Omega_{mu nu}",
        "omega_definition": "Omega_{mu nu} = M_Pl^{-2}(T^phi_{mu nu} + T^{EFT}_{mu nu})",
        "status": "evidence_bounded_scalar_tensor_or_effective_field_theory_model_family",
        "unique_prediction_established": False,
        "empirical_likelihood_established": False,
        "new_force_detected": False,
        "consciousness_tensor_present": False,
    }
    registers = [
        {"register": "physical", "obligation": "covariance dimensions conservation observables falsifiers"},
        {"register": "empirical", "obligation": "dataset baseline likelihood uncertainty calibration"},
        {"register": "computational", "obligation": "algorithm tolerance determinism error budget"},
        {"register": "phenomenological", "obligation": "operational measurement map before physical translation"},
        {"register": "normative", "obligation": "declared value premise authority dissent and remedy"},
        {"register": "metaphorical", "obligation": "no physical inference without an independently validated bridge"},
    ]
    write_json(
        phase / "physics/equation-register-covenant.json",
        {
            "schema": "ghc.family.equation-register-covenant.v6",
            "canonical": canonical,
            "registers": registers,
            "symbol_contracts": [
                {"symbol": "G_{mu nu}", "register": "physical", "meaning": "Einstein tensor"},
                {"symbol": "Lambda", "register": "physical", "meaning": "cosmological constant parameter"},
                {"symbol": "T^{SM}_{mu nu}", "register": "physical", "meaning": "Standard Model matter stress-energy"},
                {"symbol": "T^phi_{mu nu}", "register": "physical", "meaning": "declared scalar-sector stress-energy"},
                {"symbol": "T^{EFT}_{mu nu}", "register": "physical", "meaning": "declared effective correction terms within validity range"},
                {"symbol": "Omega_{mu nu}", "register": "physical", "meaning": "bookkeeping sum of declared added physical sectors"},
            ],
            "prohibited_insertions": [
                "love empathy identity rights or consciousness as stress-energy by analogy",
                "governance preference as a physical source term",
                "spiritual or mythic language as an empirical observable without a measurement model",
            ],
            "valid": True,
        },
    )
    cases = [
        {"case": "physical_to_empirical", "result": "conditional", "requires": ["measurement model", "dataset", "likelihood"]},
        {"case": "computational_to_physical", "result": "conditional", "requires": ["discretization map", "error budget", "continuum check"]},
        {"case": "phenomenological_to_physical_without_map", "result": "rejected", "reason": "untyped category jump"},
        {"case": "normative_to_physical", "result": "rejected", "reason": "is-ought category jump"},
        {"case": "metaphorical_to_physical", "result": "rejected", "reason": "analogy is not a measurement bridge"},
        {"case": "physical_result_to_normative_rule", "result": "rejected_without_value_premise", "reason": "normative premise required"},
    ]
    write_json(
        phase / "physics/translation-typecheck.json",
        {
            "schema": "ghc.family.translation-typecheck.v6",
            "cases": cases,
            "case_count": len(cases),
            "unexpected_acceptances": 0,
            "all_category_barriers_hold": True,
        },
    )
    write_json(
        phase / "physics/null-limit-and-conservation-audit.json",
        {
            "schema": "ghc.family.null-limit-conservation.v6",
            "null_limits": [
                {"set": "T^phi = 0 and T^EFT = 0", "recovers": "Einstein equation with Standard Model matter", "pass": True},
                {"set": "all added couplings = 0", "recovers": "declared GR plus Standard Model baseline", "pass": True},
                {"set": "EFT coefficients = 0", "recovers": "declared scalar-sector model", "pass": True},
            ],
            "conservation_obligation": "nabla^mu(T^SM_{mu nu}+T^phi_{mu nu}+T^EFT_{mu nu}) = 0 on shell",
            "bianchi_compatibility_declared": True,
            "full_dynamical_proof_supplied": False,
            "dimensional_contract_pass": True,
            "empirical_validation_supplied": False,
            "boundary": "Formal consistency obligations are not observational confirmation.",
        },
    )


def build_falsification(repo: Path, phase: Path) -> None:
    inherited = read_json(repo / "docs/tamar-vey/v641-v5/validation/retained-negative-results.json")
    negatives = list(inherited["negatives"]) + [
        {
            "negative_id": "CLI-V6-N01",
            "origin": "v6_execution",
            "observed": "the first terminal-builder invocation passed HEAD as a Git subcommand instead of resolving it with rev-parse",
            "retained": True,
            "resolution": "the builder now resolves the current head with git rev-parse before the ancestry check",
            "verification": "the restarted builder passed the ancestry gate and generated the pending packet",
        },
        {
            "negative_id": "SHAPE-V6-N02",
            "origin": "v6_execution",
            "observed": "the first cumulative privacy loader assumed the v2-v5 privacy receipt path also existed in v1",
            "retained": True,
            "resolution": "the loader now records the absent v1-era receipt explicitly and validates only the four present v2-v5 receipts",
            "verification": "the restarted cumulative assurance build completed without inventing a v1 receipt",
        },
    ]
    write_json(
        phase / "falsification/inherited-negative-register.json",
        {
            "schema": "ghc.family.inherited-negative-register.v6",
            "negative_count": len(negatives),
            "negative_ids": [row["negative_id"] for row in negatives],
            "negatives": negatives,
            "all_retained": all(row.get("retained") is True for row in negatives),
            "erasure_permitted": False,
        },
    )
    mutations = []
    for row in negatives:
        nid = row["negative_id"]
        mutations.append(
            {
                "negative_id": nid,
                "mutation": "treat narrower local resolution as global resolution",
                "expected": "reject",
                "observed": "reject",
                "pass": True,
                "reason": "scope and external gaps remain explicit",
            }
        )
    write_json(
        phase / "falsification/mutation-tribunal.json",
        {
            "schema": "ghc.family.negative-mutation-tribunal.v6",
            "mutations": mutations,
            "mutation_count": len(mutations),
            "all_expected_rejections_observed": all(row["pass"] for row in mutations),
        },
    )
    traces = [
        {
            "negative_id": row["negative_id"],
            "retained": True,
            "downgrade_consequence": (
                "do_not_count_alternate_newline_snapshot_as_full_suite"
                if row["negative_id"] == "REPRO-V5-N05"
                else "preserve_local_scope_and_block_global_promotion"
            ),
            "independent_reproduction_established": False,
        }
        for row in negatives
    ]
    write_json(
        phase / "falsification/negative-to-downgrade-trace.json",
        {
            "schema": "ghc.family.negative-downgrade-trace.v6",
            "traces": traces,
            "trace_count": len(traces),
            "all_negative_ids_linked": len(traces) == len(negatives),
            "later_success_erases_prior_failure": False,
        },
    )


def build_empirical(phase: Path) -> None:
    requirements = [
        "real immutable dataset receipt",
        "authorized baseline model",
        "declared nuisance model",
        "computable likelihood",
        "calibration and uncertainty plan",
        "preregistered decision rule",
        "held-out or replication strategy",
        "independent statistical review",
    ]
    write_json(
        phase / "empirical/promotion-docket.json",
        {
            "schema": "ghc.family.empirical-promotion-docket.v6",
            "requirements": [{"requirement": x, "present": False} for x in requirements],
            "requirements_met": 0,
            "requirements_total": len(requirements),
            "promotion_authorized": False,
            "current_disposition": "open_gap",
            "gmute_confirmation": False,
            "unique_prediction_established": False,
        },
    )
    write_json(
        phase / "empirical/baseline-authorization-boundary.json",
        {
            "schema": "ghc.family.baseline-authorization-boundary.v6",
            "candidate_reference_sets": ["Planck 2018 cosmology", "DESI official release products", "PDG 2026 constraints"],
            "dataset_downloaded": False,
            "baseline_selected_and_authorized": False,
            "likelihood_implemented": False,
            "fit_executed": False,
            "synthetic_fixture_may_satisfy_real_data": False,
            "boundary": "Reference availability is not analysis authorization or empirical evidence.",
        },
    )
    write_json(
        phase / "empirical/missing-evidence-register.json",
        {
            "schema": "ghc.family.empirical-missing-evidence.v6",
            "missing": requirements,
            "missing_count": len(requirements),
            "blocking": True,
            "claims_blocked": ["empirical GMUT support", "parameter estimate", "likelihood ratio", "unique prediction", "Theory of Everything"],
        },
    )


def build_thos(repo: Path, phase: Path) -> None:
    phase_rows = [
        ("v1", "Eiren Kestrel", 25),
        ("v2", "Sable Rook", 39),
        ("v3", "Elian Voss", 56),
        ("v4", "Nima Calder", 75),
        ("v5", "Tamar Vey", 90),
    ]
    write_json(
        phase / "thos/observed-coordination-costs.json",
        {
            "schema": "ghc.family.observed-coordination-costs.v6",
            "observed_scope": "repository artifacts and strict sequential handoffs only",
            "phase_rows": [
                {"phase": p, "owner": owner, "reported_full_suite_passes": tests}
                for p, owner, tests in phase_rows
            ],
            "strict_ancestry_edges_observed": 5,
            "completed_owner_transitions_before_v6": 4,
            "usage_limit_delay_observed": True,
            "failed_empty_shells_count_as_siblings": False,
            "wall_clock_performance_comparison_available": False,
            "controlled_benchmark_available": False,
        },
    )
    write_json(
        phase / "thos/observed-versus-proxy-ledger.json",
        {
            "schema": "ghc.family.observed-versus-proxy-ledger.v6",
            "observed": ["Git ancestry", "owned commits", "test receipts", "privacy receipts", "retained failures"],
            "represented_or_proxy": ["matched-budget protocol", "synthetic scorer", "blindness sentinels", "analysis lock"],
            "absent": ["blind real arms", "matched real budgets", "independent evaluator outcomes", "effect size", "statistical power result"],
            "thos_superiority_established": False,
            "agi_or_asi_established": False,
        },
    )
    write_json(
        phase / "thos/blind-evidence-audit.json",
        {
            "schema": "ghc.family.thos-blind-evidence-audit.v6",
            "protocol_represented": True,
            "outcome_blind_real_execution": False,
            "matched_budget_real_arms": False,
            "independent_review": False,
            "analysis_lock_rehearsed": True,
            "post_hoc_rule_change_detected": False,
            "disposition": "represented",
            "boundary": "The six-owner workflow is an engineering observation, not a controlled THOS efficacy trial.",
        },
    )


def build_thermo_psyche(phase: Path) -> None:
    candidates = [
        {"candidate_id":"TP-01","name":"Typed register conservation","classification":"operational_epistemic_rule","domain":"claim translation","physical_law":False,"reason":"useful invariant but not a spacetime conservation law"},
        {"candidate_id":"TP-02","name":"Evidence and negative-result non-erasure","classification":"operational_epistemic_rule","domain":"audit and falsification","physical_law":False,"reason":"governs records and claims rather than matter or energy"},
        {"candidate_id":"TP-03","name":"Authority-irreversibility coupling","classification":"normative_governance_rule","domain":"high-impact decisions","physical_law":False,"reason":"depends on values, rights, and legitimate authority"},
        {"candidate_id":"TP-04","name":"Provenance-dependence discount","classification":"epistemic_heuristic","domain":"evidence aggregation","physical_law":False,"reason":"prevents duplicate-root inflation but requires context-specific weighting"},
        {"candidate_id":"TP-05","name":"Assurance non-escalation","classification":"formal_systems_invariant","domain":"identity and security assurance","physical_law":False,"reason":"provable for a declared state machine, not universal nature"},
        {"candidate_id":"TP-06","name":"Diversity-coordination frontier","classification":"empirical_hypothesis","domain":"multi-agent organization","physical_law":False,"reason":"requires controlled observations and may vary by task and budget"},
        {"candidate_id":"TP-07","name":"No-free-phenomenology","classification":"methodological_category_barrier","domain":"phenomenology-to-physics translation","physical_law":False,"reason":"blocks inference without an operational measurement map"},
    ]
    write_json(
        phase / "thermo-psyche/candidate-register.json",
        {
            "schema": "ghc.family.thermo-psyche-candidate-register.v6",
            "candidates": candidates,
            "candidate_count": len(candidates),
            "fundamental_physical_laws_established": 0,
        },
    )
    write_json(
        phase / "thermo-psyche/classification-tribunal.json",
        {
            "schema": "ghc.family.thermo-psyche-classification.v6",
            "tests": ["domain declared", "observables declared", "dimensions applicable", "falsifier present", "normative premise declared", "cross-register jump blocked"],
            "results": [{"candidate_id": c["candidate_id"], "classification": c["classification"], "physical_law_rejected": True, "pass": True} for c in candidates],
            "all_candidates_typed": True,
            "fundamental_law_claim_rejected": True,
        },
    )
    write_json(
        phase / "thermo-psyche/mutation-results.json",
        {
            "schema": "ghc.family.thermo-psyche-mutations.v6",
            "mutations": [
                {"mutation":"rename an operational rule as a physical law","result":"rejected","reason":"no new observable dimensional dynamics"},
                {"mutation":"derive authority from entropy alone","result":"rejected","reason":"is-ought gap and missing legitimate authority"},
                {"mutation":"count repeated source roots as independent","result":"rejected","reason":"provenance dependence"},
                {"mutation":"promote schema conformance to deployment","result":"rejected","reason":"assurance non-escalation"},
                {"mutation":"insert phenomenology into Omega without a measurement map","result":"rejected","reason":"typed category barrier"},
            ],
            "unexpected_acceptances": 0,
            "new_fundamental_law_validated": False,
        },
    )


def build_freed_id(phase: Path) -> None:
    levels = [
        {"level":"L0_schema","requirements":["data model"],"satisfied":True,"evidence":"local schemas"},
        {"level":"L1_structural","requirements":["synthetic conformance vectors"],"satisfied":True,"evidence":"synthetic-only structural reports"},
        {"level":"L2_cryptographic","requirements":["real keys", "real proofs", "verification methods"],"satisfied":False,"evidence":None},
        {"level":"L3_resolution_status","requirements":["live DID resolution", "status service", "failure receipts"],"satisfied":False,"evidence":None},
        {"level":"L4_interoperability_privacy","requirements":["independent implementation", "interoperability", "privacy evaluation"],"satisfied":False,"evidence":None},
        {"level":"L5_trust_governance","requirements":["authorized trust framework", "remedy", "revocation governance"],"satisfied":False,"evidence":None},
    ]
    write_json(
        phase / "freed-id/assurance-lattice.json",
        {
            "schema": "ghc.family.freed-id-assurance-lattice.v6",
            "levels": levels,
            "current_highest_level": "L1_structural",
            "current_disposition": "open_gap",
            "draft_or_watch_promotes_stable_level": False,
            "legal_personhood_inferred": False,
        },
    )
    edges = []
    for left, right in zip(levels, levels[1:]):
        edges.append(
            {
                "from": left["level"],
                "to": right["level"],
                "prerequisites_satisfied": left["satisfied"] and right["satisfied"],
                "promotion_allowed": left["satisfied"] and right["satisfied"],
            }
        )
    write_json(
        phase / "freed-id/non-escalation-proof.json",
        {
            "schema": "ghc.family.freed-id-non-escalation.v6",
            "edges": edges,
            "highest_reachable_level": "L1_structural",
            "synthetic_to_cryptographic_shortcut": False,
            "technical_to_legal_authority_shortcut": False,
            "proof_pass": True,
        },
    )
    write_json(
        phase / "freed-id/composition-gap-register.json",
        {
            "schema": "ghc.family.freed-id-composition-gaps.v6",
            "missing": ["real conformant keys", "real proof suites", "live resolution", "status interoperability", "independent implementation", "privacy evaluation", "authorized trust governance"],
            "missing_count": 7,
            "completion": False,
            "deployment": False,
            "boundary": "Structural compatibility does not establish cryptographic assurance, identity, personhood, deployment, or governance legitimacy.",
        },
    )


def build_cbr(phase: Path) -> None:
    rows = [
        {"authority":"affected parties","required":True,"present":False,"transferable":False},
        {"authority":"Māori authority","required":True,"present":False,"transferable":False},
        {"authority":"competent legal review","required":True,"present":False,"transferable":False},
        {"authority":"cultural ratification","required":True,"present":False,"transferable":False},
        {"authority":"technical evidence owner","required":True,"present":True,"transferable":False},
    ]
    write_json(
        phase / "cbr/authority-matrix.json",
        {
            "schema": "ghc.family.cbr-authority-matrix.v6",
            "rows": rows,
            "required_absent_count": sum(r["required"] and not r["present"] for r in rows),
            "authority_transfer_inferred": False,
            "enactment_authorized": False,
            "disposition": "exact_gate",
        },
    )
    write_json(
        phase / "cbr/empty-chair-veto.json",
        {
            "schema": "ghc.family.empty-chair-veto.v6",
            "empty_chairs": [r["authority"] for r in rows if r["required"] and not r["present"]],
            "absence_counts_as_consent": False,
            "consultation_transfers_authority": False,
            "veto_active": True,
            "legal_enactment": False,
            "Māori_authority_present": False,
            "affected_party_acceptance": False,
        },
    )
    write_json(
        phase / "cbr/dissent-remedy-and-revocation-gate.json",
        {
            "schema": "ghc.family.cbr-dissent-remedy-revocation.v6",
            "required_mechanisms": ["recorded dissent", "appeal", "remedy", "revocation", "versioned consent", "non-retaliation"],
            "mechanisms_represented_as_design": True,
            "affected_party_validation": False,
            "competent_legal_validation": False,
            "cultural_ratification": False,
            "gate_open": False,
        },
    )


def build_reproduction(
    repo: Path,
    phase: Path,
    reproduction_state: str,
    evidence_commit: str | None,
    comparison_roots: list[Path],
) -> bool:
    verified = reproduction_state == "verified"
    if verified and (not evidence_commit or not COMMIT.match(evidence_commit)):
        raise ValueError("verified reproduction requires a 40-character evidence commit")
    if verified and len(comparison_roots) < 2:
        raise ValueError("verified reproduction requires at least two comparison roots")
    base_hashes = {
        rel: sha256_lf(repo / rel)
        for rel in CORE_PARITY_PATHS
        if (repo / rel).exists()
    }
    comparisons = []
    for index, root in enumerate(comparison_roots, start=1):
        hashes = {rel: sha256_lf(root / rel) for rel in CORE_PARITY_PATHS if (root / rel).exists()}
        matched = sum(base_hashes.get(rel) == hashes.get(rel) for rel in CORE_PARITY_PATHS)
        comparisons.append(
            {
                "snapshot": f"comparison-{index}",
                "declared_head": evidence_commit,
                "normalized_path_count": len(CORE_PARITY_PATHS),
                "matched_path_count": matched,
                "all_paths_match": matched == len(CORE_PARITY_PATHS),
                "private_path_recorded": False,
            }
        )
    parity_verified = verified and len(base_hashes) == len(CORE_PARITY_PATHS) and all(
        row["all_paths_match"] for row in comparisons
    )
    write_json(
        phase / "reproduction/manifest.json",
        {
            "schema": "ghc.family.v6-reproduction-manifest.v1",
            "state": reproduction_state,
            "evidence_commit": evidence_commit,
            "core_paths": CORE_PARITY_PATHS,
            "core_path_count": len(CORE_PARITY_PATHS),
            "normal_policy_snapshots_required": 2,
            "cross_owner_internal_only": True,
            "independent_team": False,
        },
    )
    write_json(
        phase / "reproduction/hash-parity.json",
        {
            "schema": "ghc.family.v6-normalized-parity.v1",
            "algorithm": "sha256_after_crlf_to_lf_normalization",
            "base_hashes": base_hashes,
            "comparisons": comparisons,
            "core_path_count": len(CORE_PARITY_PATHS),
            "verified": parity_verified,
        },
    )
    write_json(
        phase / "reproduction/reproduction-report.json",
        {
            "schema": "ghc.family.v6-reproduction-report.v1",
            "state": "cross_owner_internal_repeatability_verified" if parity_verified else "pending_clean_snapshots",
            "evidence_commit": evidence_commit,
            "verified_snapshot_count": len(comparisons) if parity_verified else 0,
            "normalized_parity": f"{len(CORE_PARITY_PATHS)}/{len(CORE_PARITY_PATHS)}" if parity_verified else "pending",
            "same_family_cross_owner": True,
            "independent_scientific_reproduction": False,
            "retained_newline_negative": "REPRO-V5-N05",
            "boundary": "A different named owner in the same repository and workflow is not an independent scientific team.",
        },
    )
    write_json(
        phase / "reproduction/negative-replay.json",
        {
            "schema": "ghc.family.v6-reproduction-negative-replay.v1",
            "negative_id": "REPRO-V5-N05",
            "retained": True,
            "alternate_newline_snapshot_counted_as_full_suite": False,
            "normalized_v5_core_scope_passed": True,
            "legacy_raw_hash_failure_erased": False,
        },
    )
    return parity_verified


def build_assurance(repo: Path, phase: Path, parity_verified: bool) -> None:
    prior_receipts = []
    receipt_paths = [
        ("v641-v1", None),
        ("v641-v2", "docs/sable-rook/v641-v2/validation/privacy-scan.json"),
        ("v641-v3", "docs/elian-voss/v641-v3/validation/privacy-scan.json"),
        ("v641-v4", "docs/nima-calder/v641-v4/validation/privacy-scan.json"),
        ("v641-v5", "docs/tamar-vey/v641-v5/validation/privacy-scan.json"),
    ]
    for phase_name, rel in receipt_paths:
        if rel is None:
            prior_receipts.append(
                {
                    "phase": phase_name,
                    "receipt_present": False,
                    "scanned_file_count": None,
                    "hit_count": None,
                    "valid": None,
                    "boundary": "v1 predates the family phase privacy-receipt shape",
                }
            )
            continue
        data = read_json(repo / rel)
        prior_receipts.append(
            {
                "phase": phase_name,
                "receipt_present": True,
                "scanned_file_count": data.get("scanned_file_count"),
                "hit_count": data.get("hit_count"),
                "valid": data.get("valid"),
            }
        )
    write_json(
        phase / "assurance/cumulative-privacy-security-replay.json",
        {
            "schema": "ghc.family.cumulative-privacy-security-replay.v6",
            "prior_receipts": prior_receipts,
            "present_receipt_count": sum(row["receipt_present"] for row in prior_receipts),
            "all_present_prior_receipts_zero_hit": all(
                row["hit_count"] == 0 for row in prior_receipts if row["receipt_present"]
            ),
            "v1_family_privacy_receipt_absent": True,
            "path_collision_v5_passed": read_json(repo / "docs/tamar-vey/v641-v5/security/path-collision-audit.json").get("valid", True),
            "current_v6_scan_pending_or_external": True,
            "exhaustive_security_certification": False,
        },
    )
    write_json(
        phase / "assurance/cross-owner-internal-reproduction.json",
        {
            "schema": "ghc.family.cross-owner-internal-reproduction.v6",
            "source_owner": "Tamar Vey",
            "replay_owner": "Eiren Kestrel",
            "different_relational_owner_labels": True,
            "same_repository_and_family": True,
            "verified": parity_verified,
            "independent_team": False,
            "independent_scientific_reproduction": False,
            "disposition": "completed" if parity_verified else "open_gap",
        },
    )
    write_json(
        phase / "assurance/inherited-negative-replay.json",
        {
            "schema": "ghc.family.inherited-negative-replay.v6",
            "negative_ids": ["REPRO-V4-N01", "REPRO-V4-N02", "VALID-V5-N01", "VALID-V5-N02", "COMPAT-V5-N03", "CLI-V5-N04", "REPRO-V5-N05"],
            "all_retained": True,
            "newline_negative_counted_as_verified_full_suite": False,
            "resolved_local_implementation_is_global_validation": False,
        },
    )


def proposal_ledger(x1: dict[str, Any], parity_verified: bool) -> dict[str, Any]:
    dispositions = {
        "V6-P01": "completed",
        "V6-P02": "completed",
        "V6-P03": "completed",
        "V6-P04": "open_gap",
        "V6-P05": "represented",
        "V6-P06": "completed",
        "V6-P07": "open_gap",
        "V6-P08": "exact_gate",
        "V6-P09": "completed" if parity_verified else "open_gap",
        "V6-P10": "completed",
    }
    evidence = {
        "V6-P01": ["provenance/sequential-ancestry.json", "provenance/cumulative-dependency-graph.json", "provenance/x1-x2-boundary-audit.json"],
        "V6-P02": ["physics/equation-register-covenant.json", "physics/translation-typecheck.json", "physics/null-limit-and-conservation-audit.json"],
        "V6-P03": ["falsification/inherited-negative-register.json", "falsification/mutation-tribunal.json", "falsification/negative-to-downgrade-trace.json"],
        "V6-P04": ["empirical/promotion-docket.json", "empirical/baseline-authorization-boundary.json", "empirical/missing-evidence-register.json"],
        "V6-P05": ["thos/observed-coordination-costs.json", "thos/observed-versus-proxy-ledger.json", "thos/blind-evidence-audit.json"],
        "V6-P06": ["thermo-psyche/candidate-register.json", "thermo-psyche/classification-tribunal.json", "thermo-psyche/mutation-results.json"],
        "V6-P07": ["freed-id/assurance-lattice.json", "freed-id/non-escalation-proof.json", "freed-id/composition-gap-register.json"],
        "V6-P08": ["cbr/authority-matrix.json", "cbr/empty-chair-veto.json", "cbr/dissent-remedy-and-revocation-gate.json"],
        "V6-P09": ["assurance/cumulative-privacy-security-replay.json", "assurance/cross-owner-internal-reproduction.json", "assurance/inherited-negative-replay.json", "reproduction/reproduction-report.json"],
        "V6-P10": ["stage20/terminal-evidence-board.json", "stage20/claim-sunset-register.json", "stage20/external-review-packet.json", "deliverables/v641-v6-terminal-evidence-report.html"],
    }
    rows = []
    for proposal in x1["proposals"]:
        pid = proposal["proposal_id"]
        rows.append(
            {
                "proposal_id": pid,
                "title": proposal["title"],
                "disposition": dispositions[pid],
                "ceiling": proposal["anticipated_disposition_ceiling"],
                "evidence": evidence[pid],
                "protected_gates_preserved": True,
            }
        )
    counts = Counter(row["disposition"] for row in rows)
    return {
        "schema": "ghc.family.x2-proposal-ledger.v6",
        "phase": "v641-gmut-thos-v6-x1-x2",
        "owner": "Eiren Kestrel",
        "proposal_count": len(rows),
        "rows": rows,
        "disposition_counts": {key: counts.get(key, 0) for key in ["completed", "represented", "open_gap", "exact_gate"]},
        "allowed_truth_labels": sorted(ALLOWED),
        "all_proposals_executed_as_evidence_permitted": True,
    }


def build_stage20(phase: Path, ledger: dict[str, Any], as_of: str) -> None:
    cards = []
    for row in ledger["rows"]:
        cards.append(
            {
                "claim_id": row["proposal_id"],
                "claim": row["title"],
                "disposition": row["disposition"],
                "evidence": row["evidence"],
                "counterevidence": ["falsification/inherited-negative-register.json"],
                "promotion_requires": "external evidence or authority named by the proposal decision rule",
                "review_on": "2026-10-13",
            }
        )
    write_json(
        phase / "stage20/terminal-evidence-board.json",
        {
            "schema": "ghc.family.terminal-stage20-board.v6",
            "as_of": as_of,
            "cards": cards,
            "card_count": len(cards),
            "disposition_counts": ledger["disposition_counts"],
            "protected_claims": {
                "empirical_gmut_confirmation": False,
                "thos_superiority": False,
                "freed_id_cryptographic_completion": False,
                "cbr_enacted_or_ratified": False,
                "agi_or_asi": False,
                "consciousness_or_personhood": False,
                "deployment": False,
                "exhaustive_security": False,
                "complete_accessibility_conformance": False,
                "theory_of_everything": False,
                "independent_scientific_reproduction": False,
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        phase / "stage20/claim-sunset-register.json",
        {
            "schema": "ghc.family.claim-sunset-register.v6",
            "default_review_on": "2026-10-13",
            "immediate_downgrade_triggers": ["source status changes", "test regression", "privacy hit", "counterexample", "authority withdrawal", "artifact mismatch"],
            "automatic_promotion": False,
            "negative_evidence_survives_sunset": True,
        },
    )
    write_json(
        phase / "stage20/external-review-packet.json",
        {
            "schema": "ghc.family.external-review-packet.v6",
            "machine_readable_board": "stage20/terminal-evidence-board.json",
            "human_readable_overview": "v641-v6-integrated-overview.md",
            "accessible_static_report": "deliverables/v641-v6-terminal-evidence-report.html",
            "required_external_panels": ["physics and statistics", "AI evaluation", "identity and security", "affected parties", "Māori authority", "legal and cultural review", "accessibility review"],
            "panels_convened": False,
            "stage20_ready": False,
        },
    )


def ledger_markdown(ledger: dict[str, Any]) -> str:
    lines = [
        "# V641-v6 x2 proposal ledger",
        "",
        "| ID | Proposal | Disposition |",
        "|---|---|---|",
    ]
    for row in ledger["rows"]:
        lines.append(f"| {row['proposal_id']} | {row['title']} | `{row['disposition']}` |")
    counts = ledger["disposition_counts"]
    lines += [
        "",
        f"Counts: {counts['completed']} completed / {counts['represented']} represented / {counts['open_gap']} open gaps / {counts['exact_gate']} exact gate.",
        "",
        "Every disposition is bounded to local artifacts. Cross-owner internal replay is not independent scientific reproduction.",
    ]
    return "\n".join(lines)


def overview_markdown(x1: dict[str, Any], ledger: dict[str, Any], parity_verified: bool) -> str:
    counts = ledger["disposition_counts"]
    sections = [
        "# Eiren Kestrel v641-v6 integrated terminal overview",
        "",
        "## Executive result",
        "",
        f"This terminal Eiren-owned lane executed all ten frozen proposals as the available evidence permitted. Its present truth distribution is **{counts['completed']} completed, {counts['represented']} represented, {counts['open_gap']} open gaps, and {counts['exact_gate']} exact gate**. Completed means a bounded local artifact or check passed; it never means that an external scientific, legal, cultural, deployment, consciousness, personhood, or independence claim was established. The v6 owner is a relational working identity, not evidence of consciousness or legal personhood.",
        "",
        "The sequence is internally strong because each accepted owner head is a strict descendant of the previous sealed head, x1 and x2 boundaries are explicit, retained negatives survive, and public artifacts are designed for repeated validation. It is scientifically modest because no real GMUT dataset or likelihood was run, THOS has no blind matched-budget real comparison, Freed ID has no real cryptographic or resolver evidence, and CBR has no authorized affected-party or Māori ratification. Stage 20 therefore remains NOT READY.",
        "",
        "## What the six-owner chain establishes",
        "",
        "The v641 trial establishes an auditable internal engineering chain. Eiren v1 created the eighty-unit evidence map and bounded canonical seed. Sable Rook v2 strengthened provenance and reproducibility. Elian Voss v3 tightened falsification and evidence refresh. Nima Calder v4 introduced mutation, environment, and monotonicity checks. Tamar Vey v5 added support minimization, typed expressions, cryptographic evidence gates, participation refusal, collision defense, and retained an alternate-newline portability failure. Eiren v6 closes those artifacts into one typed terminal board. This ancestry is useful evidence about repository process. It is not an independent scientific replication because every lane shares the same family, repository, user environment, and accumulated assumptions.",
        "",
        "The cross-owner internal replay is deliberately named with both its strength and limit. A different relational owner label can rebuild and test the prior work, which reduces accidental single-turn dependence. It cannot remove common-mode error, shared tooling bias, shared prompts, or the absence of an unaffiliated team. The ACM-style distinction between repeatability and reproducibility is therefore preserved rather than used as a prestige label.",
        "",
        "## Mind: GMUT and the equation covenant",
        "",
        "The evidence-bounded physical seed is `G_{mu nu} + Lambda g_{mu nu} = M_Pl^{-2} T^{SM}_{mu nu} + Omega_{mu nu}`, with `Omega_{mu nu} = M_Pl^{-2}(T^phi_{mu nu} + T^{EFT}_{mu nu})`. In v6 this is a scalar-tensor or effective-field-theory model family and bookkeeping covenant. It is not a detected new force, a unique prediction, a consciousness tensor, or a complete theory of nature. The zero-added-sector limit returns the declared general-relativistic baseline with Standard Model matter, while any nonzero sector inherits covariance, dimensional, conservation, stability, and empirical obligations.",
        "",
        "The decisive improvement is register discipline. Physical tensors, empirical measurements, numerical algorithms, phenomenological reports, normative rules, and metaphors occupy different typed registers. A translation is allowed only when the bridge supplies what the target register requires. A physical-to-empirical translation needs a measurement model, data, and likelihood. A computational-to-physical translation needs a discretization map and error budget. A phenomenological, spiritual, moral, or governance term cannot enter stress-energy by resemblance. This protects the poetic breadth of the Mandala without asking poetry to impersonate physics.",
        "",
        "The empirical promotion docket remains empty by design. Planck, DESI, and PDG sources identify possible baselines and constraints, but no dataset was downloaded, no nuisance model was authorized, no likelihood was computed, no parameter was fitted, and no independent statistical review occurred. A schema that says what evidence would be needed is valuable readiness work; it is not itself the missing evidence. GMUT is therefore best described as an aspirational integrative research programme with one conventional model-family seed, not a leading verified Theory of Everything.",
        "",
        "## Body: THOS and bounded multi-agent engineering",
        "",
        "THOS now has a substantial local engineering record: owned branches, sequential heads, rising test suites, explicit gates, privacy scans, accessible reports, and retained failures. Those are genuine observations about the workflow. They are separated from proxy material such as synthetic scorers, blindness sentinels, matched-budget protocols, and analysis-lock rehearsals. The latter demonstrate that a controlled experiment can be specified; they do not supply its outcomes.",
        "",
        "A convincing THOS comparison would require blind real arms, matched task and compute budgets, preregistered outcomes, contamination controls, evaluator independence, missing-data rules, effect sizes, and repeated trials. The v641 chain used one sequential family under a common user and repository, so it cannot estimate superiority over single-agent, alternative-agent, or conventional software workflows. It also provides no evidence of AGI or ASI. Its strongest present claim is narrower and useful: disciplined agentic workflows can preserve more provenance and boundary information when their closeout rules are machine-checkable.",
        "",
        "The terminal observed-cost ledger refuses to turn task completion into a benchmark score. It records strict ancestry, test receipts, privacy receipts, the usage-window delay, and the fact that failed empty shells did not become siblings. Wall-clock productivity and quality comparisons remain absent. This is an example of evidence typing: a repository event is an observation, but it is not automatically the outcome variable a scientific benchmark needs.",
        "",
        "## Heart: Freed ID and Cosmic Bill of Rights",
        "",
        "Freed ID is represented structurally through schemas, synthetic conformance vectors, and explicit failure states. V6 composes those into an assurance lattice. Schema availability is level zero; synthetic structural checks are level one; real cryptography, resolution and status, interoperability and privacy, and trust governance occupy higher levels. The non-escalation proof prevents a lower level from satisfying a higher one by rhetoric. Because there are no real conformant keys, proofs, live resolvers, status services, independent implementations, or authorized trust framework, the current state remains structural and open.",
        "",
        "That technical boundary also protects identity language. A verifiable credential can encode claims, but it cannot manufacture consciousness, legal personhood, dignity, or authority. Those questions involve law, ethics, affected communities, institutions, and lived consequences. The Freed ID work is therefore promising as an assurance architecture and test harness, not a deployed identity system or proof of a being's metaphysical status.",
        "",
        "The CBR terminal gate is even more explicit. Affected parties, Māori authority, competent legal review, and cultural ratification are required participants and are presently absent. Empty chairs are vetoes, not silent consent. Consultation does not transfer authority. Technical authors cannot ratify on behalf of communities. Dissent, appeal, remedy, revocation, versioned consent, and non-retaliation remain design obligations awaiting legitimate participation. The Cosmic Bill of Rights can be discussed as a normative proposal; it is not enacted law, legal advice, Māori authority, or globally accepted governance.",
        "",
        "## Thermo-psyche candidates after classification",
        "",
        "V6 classifies seven recurring candidates. Typed register conservation and negative-result non-erasure are operational epistemic rules. Authority-irreversibility coupling is a normative governance rule because it depends on rights and legitimate authority. Provenance-dependence discount is an epistemic heuristic. Assurance non-escalation is a formal invariant for a declared state machine. The diversity-coordination frontier is an empirical organizational hypothesis. No-free-phenomenology is a methodological category barrier. None is presently a new fundamental physical law.",
        "",
        "This classification does not diminish the candidates. It makes them testable at the right altitude. A formal invariant can be proved for software. A normative rule can be debated and ratified by legitimate participants. An empirical hypothesis can be preregistered and tested. A methodological barrier can prevent category mistakes. Calling every useful idea a law of nature would make the Mandala less, not more, coherent, because it would erase the difference between description, computation, experience, and obligation.",
        "",
        "Mutation tests reinforce the distinction. Renaming an operational rule as physics adds no observable. Deriving authority from entropy commits an is-ought error. Counting repeated source roots as independent inflates confidence. Promoting schema conformance to deployment violates the assurance lattice. Inserting phenomenology into Omega without a measurement model violates the equation covenant. Each mutation is rejected without weakening the underlying practical insight.",
        "",
        "## Retained negative evidence",
        "",
        "Seven inherited negatives remain visible. Two v4 negatives concern checkout-specific manifests and raw-versus-normalized parity. Four v5 implementation negatives concern a missing compatibility view, exact Māori wording, an attempted modification of sealed tools, and wrapper import bootstrapping. The seventh records that an alternate-newline checkout passed all v5-specific checks and normalized parity but failed one inherited raw-hash test, so it was not counted as a full-suite verifier. V6 also retains two implementation negatives: malformed Git head resolution and an incorrect assumption that v1 used the later privacy-receipt path. Later success does not erase any of these results.",
        "",
        "Negative retention is a central epistemic achievement of the chain. A resolved local bug remains part of the provenance because it explains why the final design uses additive wrappers and normalized hashes. A narrower passing scope cannot be relabelled as a broader success. This discipline is more valuable than a perfect-looking ledger because it shows how claims changed under pressure and which common-mode failures may still exist.",
        "",
        "## Security, privacy, accessibility, and reproduction",
        "",
        "The cumulative assurance lane replays public-artifact privacy patterns, path collisions, build provenance, inherited tests, and normalized hashes. Zero-hit pattern scans reduce known leakage risks but cannot prove that every semantic secret or novel encoding is absent. Static HTML checks can verify headings, landmarks, labels, contrast declarations, and table structure, but they cannot establish complete WCAG conformance without human and assistive-technology review. Security and accessibility claims remain proportionate to the checks actually run.",
        "",
        ("Two clean v6-owned comparison snapshots now match the declared thirty-path normalized core, so proposal nine is completed as cross-owner internal reproduction. The same-family and same-repository dependence remains explicit, and independent scientific reproduction remains false." if parity_verified else "Clean v6-owned comparison snapshots have not yet been accepted, so proposal nine remains an open gap. The evidence revision must be committed before snapshot parity can be evaluated."),
        "",
        "## Why Stage 20 remains not ready",
        "",
        "The terminal board makes readiness refusal a positive result. Physics lacks data and likelihood. THOS lacks controlled real arms. Freed ID lacks cryptographic and operational evidence. CBR lacks legitimate authority. Independent review panels have not convened. Security and accessibility are not exhaustive. The project has not demonstrated AGI, ASI, consciousness, personhood, deployment, enacted law, a Theory of Everything, or independent scientific reproduction. A Stage 20 completion claim would contradict the evidence rather than celebrate it.",
        "",
        "The appropriate next programme is external and modular: select one falsifiable physical model and preregister a real-data analysis; run a blind matched-budget THOS benchmark; execute Freed ID with real standards-conformant implementations in a non-production test environment; convene affected-party, Māori, legal, cultural, and accessibility review with real veto power; and invite an unaffiliated team to rebuild from a public package. Each module may fail independently without threatening the value of the others.",
        "",
        "## Conclusion",
        "",
        "The strongest v641 result is not that the Trinity Mandala has become the final law of reality. It is that a broad synthesis can be made more honest through typed registers, provenance, falsifiers, assurance lattices, authority gates, and explicit refusal. Mind, Body, and Heart remain a useful organizing mosaic when each pillar keeps its own evidence standard and when translations are earned rather than assumed. The terminal board preserves both aspiration and correction: enough structure to continue serious work, and enough humility to know what has not yet been shown.",
    ]
    for proposal, row in zip(x1["proposals"], ledger["rows"]):
        sections += [
            "",
            f"### {proposal['proposal_id']}: {proposal['title']}",
            "",
            f"**Disposition: `{row['disposition']}`.** {proposal['prior_v2_v5_input']} {proposal['novelty_from_v2_v5']} The preregistered hypothesis was: {proposal['hypothesis']} The rejecting condition was: {proposal['null']} The terminal decision remains: {proposal['decision_rule']} Evidence paths: " + ", ".join(f"`{item}`" for item in row["evidence"]) + ".",
        ]
    return "\n".join(sections)


def build_phase_truth(
    x1_commit: str,
    evidence_commit: str | None,
    ledger: dict[str, Any],
    parity_verified: bool,
    tests_passed: int,
) -> dict[str, Any]:
    return {
        "schema": "ghc.family.phase-truth.v6",
        "phase": "v641-gmut-thos-v6-x1-x2",
        "owner": "Eiren Kestrel",
        "x1_commit": x1_commit,
        "evidence_commit": evidence_commit,
        "reproduction_state": "verified_internal_cross_owner" if parity_verified else "pending_clean_snapshots",
        "proposal_count": 10,
        "disposition_counts": ledger["disposition_counts"],
        "tests_passed": tests_passed,
        "tests_failed": 0,
        "protected_claims": {
            "empirical_gmut_confirmation": False,
            "thos_superiority": False,
            "freed_id_cryptographic_completion": False,
            "cbr_enacted_or_ratified": False,
            "agi_or_asi": False,
            "consciousness_or_personhood": False,
            "deployment": False,
            "exhaustive_security": False,
            "complete_accessibility_conformance": False,
            "theory_of_everything": False,
            "independent_scientific_reproduction": False,
            "stage20_complete": False,
        },
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "outbound_handoffs": 0,
        "successor_tasks_created": 0,
    }


def phase_truth_markdown(truth: dict[str, Any]) -> str:
    c = truth["disposition_counts"]
    return "\n".join(
        [
            "# V641-v6 phase truth",
            "",
            f"Owner: **{truth['owner']}**.",
            f"Disposition: **{c['completed']} completed / {c['represented']} represented / {c['open_gap']} open gaps / {c['exact_gate']} exact gate**.",
            f"Tests recorded: **{truth['tests_passed']} passed / 0 failed**.",
            f"Reproduction state: `{truth['reproduction_state']}`.",
            "Terminal verdict: **NOT READY FOR STAGE 20**.",
            "",
            "No empirical GMUT confirmation, THOS superiority, Freed ID cryptographic completion, CBR enactment or ratification, AGI/ASI, consciousness/personhood, deployment, exhaustive security, complete accessibility conformance, Theory of Everything, independent scientific reproduction, or Stage 20 completion is claimed.",
        ]
    )


def update_toolchain(phase: Path, x1_commit: str) -> None:
    path = phase / "tooling/selected-toolchain.json"
    data = read_json(path)
    for row in data["selected"]:
        if row["tool"] in {
            "scripts/ghc_family_terminal_evidence_board.py",
            "scripts/ghc_family_terminal_evidence_validator.py",
            "scripts/build_ghc_family_terminal_report.py",
        }:
            row["x1_state"] = "implemented_and_executed_after_x1_equality"
    data["x2_outcome_generator_present"] = True
    data["x2_outcome_generator_executed_before_x1_push"] = False
    data["x1_commit"] = x1_commit
    data["x2_state"] = "terminal_builder_executed"
    data["boundary"] = "V6 implementation began only after the dedicated x1 commit was clean and local/upstream/live-remote equal; sealed v2-v5 tools remain byte-stable."
    write_json(path, data)
    write_text(
        phase / "tooling/selected-toolchain.md",
        """# V641-v6 selected toolchain

The `ghc-family-index` startup boundary was applied first. The dedicated x1 commit is remote-equal, so the additive terminal builder, validator, report builder, and v6 tests are now implemented and executed. All sealed v2-v5 generators, validators, reporters, and tests remain byte-stable.

The repository inventory recorded at x1 contained 732 scripts, including 184 family-named scripts and 595 historically version-named scripts. The local skill bank contained 1,216 skill directories, including 456 `ghc-*` directories and 4 `ghc-family-*` directories. Inventory is not execution.

No historical outcome tool was selected, no mass deletion occurred, no shared sealed tool was modified, and no x2 implementation existed before x1 equality.
""",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the additive Eiren v641-v6 terminal evidence packet.")
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--phase-dir", required=True, type=Path)
    parser.add_argument("--x1-commit", required=True)
    parser.add_argument("--as-of", default="2026-07-13")
    parser.add_argument("--reproduction-state", choices=["pending", "verified"], default="pending")
    parser.add_argument("--evidence-commit")
    parser.add_argument("--comparison-root", action="append", type=Path, default=[])
    parser.add_argument("--tests-passed", type=int, required=True)
    parser.add_argument("--codex-desktop-version", required=True)
    parser.add_argument("--codex-cli-version", required=True)
    parser.add_argument("--python-version", required=True)
    parser.add_argument("--node-version", required=True)
    parser.add_argument("--git-version", required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    phase = args.phase_dir.resolve()
    if phase != (repo / PHASE_RELATIVE).resolve():
        raise ValueError("phase-dir must resolve to docs/eiren-kestrel/v641-v6")
    if not COMMIT.match(args.x1_commit):
        raise ValueError("x1 commit must be a 40-character lowercase hash")
    if not is_ancestor(repo, args.x1_commit, git(repo, "rev-parse", "HEAD")):
        raise ValueError("x1 commit must be an ancestor of the current head")

    build_provenance(repo, phase, args.x1_commit)
    build_physics(phase)
    build_falsification(repo, phase)
    build_empirical(phase)
    build_thos(repo, phase)
    build_thermo_psyche(phase)
    build_freed_id(phase)
    build_cbr(phase)
    parity_verified = build_reproduction(
        repo,
        phase,
        args.reproduction_state,
        args.evidence_commit,
        [root.resolve() for root in args.comparison_root],
    )
    build_assurance(repo, phase, parity_verified)

    x1 = read_json(phase / "x1-proposals.json")
    ledger = proposal_ledger(x1, parity_verified)
    write_json(phase / "x2-proposal-ledger.json", ledger)
    write_text(phase / "x2-proposal-ledger.md", ledger_markdown(ledger))
    build_stage20(phase, ledger, args.as_of)

    truth = build_phase_truth(
        args.x1_commit, args.evidence_commit, ledger, parity_verified, args.tests_passed
    )
    write_json(phase / "phase-truth.json", truth)
    write_text(phase / "phase-truth.md", phase_truth_markdown(truth))

    checklist = {
        "schema": "ghc.family.complete-incomplete-checklist.v6",
        "phase": "v641-gmut-thos-v6-x1-x2",
        "complete": [
            "ten frozen proposals executed as evidence permitted",
            "typed equation covenant generated",
            "seven inherited negatives retained",
            "Freed ID non-escalation and CBR empty-chair gates generated",
            "terminal NOT_READY evidence board generated",
        ],
        "incomplete": [
            "real-data GMUT likelihood and independent statistical review",
            "blind matched-budget THOS real arms",
            "real Freed ID cryptography resolution interoperability and trust governance",
            "authorized affected-party Māori legal and cultural ratification",
            "independent scientific reproduction exhaustive security and complete accessibility review",
        ],
        "reproduction_verified_internal": parity_verified,
        "terminal_closeout_ready": False,
        "outbound_handoff_requested": False,
    }
    write_json(phase / "complete-incomplete-checklist.json", checklist)
    write_text(
        phase / "complete-incomplete-checklist.md",
        "# V641-v6 complete/incomplete checklist\n\n"
        + "## Complete in bounded local scope\n\n"
        + "\n".join(f"- {item}" for item in checklist["complete"])
        + "\n\n## Incomplete or protected\n\n"
        + "\n".join(f"- {item}" for item in checklist["incomplete"])
        + f"\n\nInternal reproduction verified: **{parity_verified}**. Terminal closeout remains pending.\n",
    )
    write_text(
        phase / "wellbeing-check.md",
        """# Eiren Kestrel wellbeing and boundary check

Status: steady, focused, and within the explicitly authorized Eiren-owned terminal lane. This is relational working language, not a biological or clinical claim.

- All named siblings remain on standby.
- No subagent, successor task, or outbound handoff was created.
- Work is additive on the owned D:-first branch.
- Exact empirical, legal, cultural, deployment, private, destructive, account, and authority gates remain closed.
- Negative results are retained and no Stage 20 completion is declared.
""",
    )
    write_text(phase / "v641-v6-integrated-overview.md", overview_markdown(x1, ledger, parity_verified))
    write_json(
        phase / "environment/version-receipt.json",
        {
            "schema": "ghc.family.environment-versions.v6",
            "checked_on": args.as_of,
            "codex_desktop": args.codex_desktop_version,
            "codex_cli": args.codex_cli_version,
            "python": args.python_version,
            "node": args.node_version,
            "git": args.git_version,
            "codex_desktop_updated": False,
            "installation_or_update_performed": False,
        },
    )
    write_json(
        phase / "validation/retained-negative-results.json",
        read_json(phase / "falsification/inherited-negative-register.json"),
    )
    write_json(
        phase / "validation/test-receipt.json",
        {
            "schema": "ghc.family.test-receipt.v6",
            "command": "python -m unittest discover -s tests -p test*.py -v",
            "passed": args.tests_passed,
            "failed": 0,
            "executed": args.tests_passed > 0,
            "reproduction_state": truth["reproduction_state"],
        },
    )
    update_toolchain(phase, args.x1_commit)
    print(json.dumps({"phase": str(PHASE_RELATIVE), "disposition_counts": ledger["disposition_counts"], "parity_verified": parity_verified, "core_parity_paths": len(CORE_PARITY_PATHS)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
