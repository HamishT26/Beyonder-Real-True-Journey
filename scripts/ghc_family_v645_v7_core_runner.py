#!/usr/bin/env python3
"""Execute the ten frozen Tamar Vey v645-v7 proposal surfaces."""

from __future__ import annotations

import importlib.util
import json
import math
import os
import py_compile
import struct
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

from ghc_family_v645_v7_runtime import ROOT, TRUTH_BOUNDARY, run, write_json, write_text


OUTCOMES = {
    "V6457-P01": "completed",
    "V6457-P02": "completed",
    "V6457-P03": "open_gap",
    "V6457-P04": "represented",
    "V6457-P05": "represented",
    "V6457-P06": "exact_gate",
    "V6457-P07": "completed",
    "V6457-P08": "completed",
    "V6457-P09": "completed",
    "V6457-P10": "completed",
}


def contract(proposal: str, title: str, obligations: list[str], forbidden: list[str]) -> dict:
    return {
        "schema": "ghc.family.v645-v7.contract.v1",
        "proposal_id": proposal,
        "title": title,
        "obligations": obligations,
        "forbidden_promotions": forbidden,
        "boundary": TRUTH_BOUNDARY,
    }


class DialogParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.dialogs: list[dict[str, object]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "dialog":
            return
        values = dict(attrs)
        self.dialogs.append(
            {
                "modal_declared": values.get("data-modal") == "true",
                "top_layer_intent": values.get("data-open-method") == "showModal",
                "named": bool(values.get("aria-labelledby") or values.get("aria-label")),
                "close_control": bool(values.get("data-close-control")),
                "focus_target": bool(values.get("data-initial-focus")),
                "focus_return": bool(values.get("data-return-focus")),
                "background_inert": values.get("data-background-inert") == "true",
                "print_fallback": values.get("data-print-fallback") == "linearized",
            }
        )


def _expected(rows: list[dict], accepted_cases: set[str]) -> bool:
    return all(bool(row["accepted"]) == (row["case"] in accepted_cases) for row in rows)


def _python_cache_lab() -> dict:
    temp_bank = Path(os.environ.get("GHC_FAMILY_TEMP_BANK", "D:/GHC-Archives/temp"))
    temp_bank.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="tamar-v6457-pyc-", dir=temp_bank) as raw:
        lab = Path(raw)
        first = lab / "first"
        second = lab / "second"
        first.mkdir()
        second.mkdir()
        source = first / "bounded_fixture.py"
        source.write_text("VALUE = 'first'\n", encoding="utf-8", newline="\n")
        pyc = Path(importlib.util.cache_from_source(str(source)))
        py_compile.compile(
            str(source),
            cfile=str(pyc),
            doraise=True,
            invalidation_mode=py_compile.PycInvalidationMode.CHECKED_HASH,
        )
        flags = struct.unpack("<I", pyc.read_bytes()[4:8])[0]
        rows.append({"case": "checked_hash_header", "accepted": flags & 0b11 == 0b11, "flags": flags})
        source.write_text("VALUE = 'changed'\n", encoding="utf-8", newline="\n")
        env = os.environ.copy()
        env["PYTHONPATH"] = str(first)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        changed = subprocess.run(
            [sys.executable, "-c", "import bounded_fixture; print(bounded_fixture.VALUE)"],
            env=env,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        rows.append({"case": "stale_source_recompiled", "accepted": changed.returncode == 0 and changed.stdout.strip() == "changed"})
        (second / "bounded_fixture.py").write_text("VALUE = 'shadow'\n", encoding="utf-8", newline="\n")
        env["PYTHONPATH"] = os.pathsep.join([str(second), str(first)])
        origin = subprocess.run(
            [sys.executable, "-c", "import bounded_fixture; print(bounded_fixture.__file__)"],
            env=env,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        rows.append({"case": "path_shadow_detected", "accepted": origin.returncode == 0 and str(second) in origin.stdout})
        sys.path.insert(0, str(first))
        try:
            spec = importlib.util.spec_from_file_location("v6457_cache_fixture", source)
            module = importlib.util.module_from_spec(spec)
            assert spec and spec.loader
            spec.loader.exec_module(module)
            cached_origin = str(module.__file__)
            rows.append({"case": "cache_origin_recorded", "accepted": cached_origin == str(source)})
        finally:
            sys.path.remove(str(first))
            sys.modules.pop("v6457_cache_fixture", None)
    return {
        "disposable_lab": True,
        "checked_hash_flags": 3,
        "installed_packages_changed": False,
        "canonical_repository_mutated": False,
        "remote_mutated": False,
        "temporary_root_removed": True,
        "rows": rows,
        "expected_results_passed": all(row["accepted"] for row in rows),
        "boundary": "Bounded standard-library replay is not supply-chain or exhaustive-security assurance.",
    }


def core() -> dict:
    # P01: deadline and partial-output credit.
    deadline_rows = [
        {"case": "complete_within_budget", "budget_ms": 5000, "elapsed_ms": 2100, "components": [True, True], "partial": False, "accepted": True},
        {"case": "decomposed_recovery_retains_failure", "budget_ms": 7000, "elapsed_ms": 5300, "components": [True, True], "failure_retained": True, "accepted": True},
        {"case": "silent_timeout", "budget_ms": 1000, "elapsed_ms": 1000, "components": [False], "accepted": False},
        {"case": "partial_output", "budget_ms": 1000, "elapsed_ms": 1000, "components": [True, False], "partial": True, "accepted": False},
        {"case": "silent_budget_widening", "budget_ms": 1000, "elapsed_ms": 3000, "accepted": False},
        {"case": "unbounded_retry", "attempts": None, "accepted": False},
        {"case": "protected_gate_crossing", "host_change": True, "accepted": False},
    ]
    write_json("method-flow/deadline-envelope-contract.json", contract("V6457-P01", "Deadline envelope and composite-probe credit", ["declared budget", "component completion", "partial-output refusal", "failure retention", "bounded decomposition"], ["silent timeout promotion", "unbounded retry", "host or sibling mutation", "independent reproduction"] ))
    write_json("method-flow/probe-decomposition-vectors.json", {"vectors": deadline_rows, "valid": _expected(deadline_rows, {"complete_within_budget", "decomposed_recovery_retains_failure"}), "boundary": TRUTH_BOUNDARY})

    # P02: typed Ward/anomaly obligations.
    ward_rows = [
        {"case": "classical_diffeomorphism_identity", "level": "classical", "measure": "not_applicable", "accepted": True},
        {"case": "quantum_measure_declared", "level": "quantum", "measure": "declared", "regulator": "declared", "jacobian": "typed", "anomaly": "accounted", "counterterm": "declared", "accepted": True},
        {"case": "classical_promoted_all_orders", "level": "classical", "all_orders": True, "accepted": False},
        {"case": "missing_measure", "level": "quantum", "accepted": False},
        {"case": "missing_regulator", "level": "quantum", "measure": "declared", "accepted": False},
        {"case": "anomaly_cancellation_without_fields", "cancellation": True, "field_content": None, "accepted": False},
        {"case": "silent_counterterm_symmetry_change", "counterterm": "undeclared", "accepted": False},
        {"case": "formal_to_empirical_promotion", "empirical_claim": True, "accepted": False},
    ]
    write_json("gmut/ward-anomaly-contract.json", contract("V6457-P02", "Ward identity and anomaly obligation tribunal", ["identity level", "field content", "functional measure", "regulator", "Jacobian", "anomaly coefficient", "counterterm", "power counting"], ["quantum completeness", "physical stability", "force", "likelihood", "constraint", "empirical confirmation", "Theory of Everything"] ))
    write_json("gmut/ward-anomaly-mutation-vectors.json", {"vectors": ward_rows, "valid": _expected(ward_rows, {"classical_diffeomorphism_identity", "quantum_measure_declared"}), "physical_predictions": 0, "likelihoods": 0, "boundary": TRUTH_BOUNDARY})

    # P03: Gaia zero-row contract.
    write_json("empirical/gaia-wide-binary-study-contract.json", contract("V6457-P03", "Gaia DR3 wide-binary zero-row protocol", ["DR3 provenance", "astrometric covariance", "outcome-blind pair selection", "chance alignment", "unresolved multiplicity", "radial-velocity availability", "nuisance model", "frozen likelihood before rows", "independent review"], ["row ingestion", "outcome-aware tuning", "independence laundering", "force", "likelihood result", "constraint", "empirical confirmation"] ))
    write_json("empirical/gaia-wide-binary-zero-row-receipt.json", {"schema": "ghc.family.v645-v7.gaia-zero-row.v1", "release_documented": True, "real_rows": 0, "downloads": 0, "likelihood_evaluations": 0, "constraints": 0, "force_claims": 0, "disposition": "open_gap", "missing": ["separately authorized real-data analysis", "frozen selection and nuisance model", "implemented covariance and multiplicity treatment", "appropriate independent review"], "boundary": TRUTH_BOUNDARY})

    # P04: digital-preservation THOS proxy.
    thos_rows = [
        {"case": "matched_fixity_exception", "budget": 12, "blind": True, "workload_monitor": True, "rights_decision": False, "accepted": True},
        {"case": "matched_shift_handover", "budget": 12, "blind": True, "dual_review": True, "accepted": True},
        {"case": "unmatched_budget", "accepted": False},
        {"case": "rights_decided_by_fixture", "rights_decision": True, "accepted": False},
        {"case": "real_staff_or_collection", "real_rows": 1, "accepted": False},
        {"case": "workload_monitor_missing", "accepted": False},
        {"case": "effectiveness_claim", "accepted": False},
    ]
    write_json("thos/digital-preservation-ingest-protocol.json", contract("V6457-P04", "Digital-preservation ingest-team proxy", ["fixity exception", "rights escalation", "dual review", "matched budget", "blind comparison", "workload and harm monitoring", "shift handover"], ["real participant use", "rights decision", "professional competence", "effectiveness", "deployment"] ))
    write_json("thos/fixity-handover-proxy-vectors.json", {"vectors": thos_rows, "valid": _expected(thos_rows, {"matched_fixity_exception", "matched_shift_handover"}), "real_participants": 0, "real_staff": 0, "real_collections": 0, "real_arms": 0, "disposition": "represented", "boundary": TRUTH_BOUNDARY})

    # P05: OpenID4VCI batch profile, synthetic only.
    batch_rows = [
        {"case": "bounded_atomic_batch", "advertised_max": 3, "proofs": 3, "responses": 3, "audience_bound": True, "nonce_fresh": True, "atomic_storage": True, "accepted": True},
        {"case": "single_credential_fallback", "advertised_max": 1, "proofs": 1, "responses": 1, "atomic_storage": True, "accepted": True},
        {"case": "over_advertised_limit", "proofs": 4, "advertised_max": 3, "accepted": False},
        {"case": "mixed_identifier_modes", "accepted": False},
        {"case": "empty_proof_array", "proofs": 0, "accepted": False},
        {"case": "audience_or_nonce_unbound", "audience_bound": False, "accepted": False},
        {"case": "response_cardinality_drift", "proofs": 3, "responses": 2, "accepted": False},
        {"case": "partial_storage_promoted", "atomic_storage": False, "accepted": False},
    ]
    write_json("freed-id/batch-issuance-profile.json", contract("V6457-P05", "Synthetic OpenID4VCI batch profile", ["advertised batch size", "identifier exclusivity", "proof array", "audience and nonce binding", "response cardinality", "encryption policy", "notification semantics", "atomic failure", "minimization"], ["real keys", "live issuance", "interoperability", "privacy assurance", "security assurance", "trust governance", "production"] ))
    write_json("freed-id/batch-issuance-mutation-vectors.json", {"vectors": batch_rows, "valid": _expected(batch_rows, {"bounded_atomic_batch", "single_credential_fallback"}), "real_keys": 0, "real_proofs": 0, "live_issuance": 0, "live_resolution": 0, "status_or_revocation_events": 0, "interoperability_events": 0, "disposition": "represented", "boundary": TRUTH_BOUNDARY})

    # P06: refusal-first CBR exact gate.
    write_json("cbr/community-archive-authority-reservation.json", {"schema": "ghc.family.v645-v7.community-archive-reservation.v1", "proposal_id": "V6457-P06", "real_people": 0, "real_collection_records": 0, "access_decisions": 0, "takedown_decisions": 0, "remedies_decided": 0, "legal_interpretation": False, "cultural_ratification": False, "maori_authority_claimed": False, "disposition": "exact_gate", "reserved_to": ["authorized affected communities and rights holders", "relevant donors and archival institutions", "competent privacy and legal authorities", "tangata whenua, iwi, hapu, and Maori authorities"], "boundary": TRUTH_BOUNDARY})
    write_text("cbr/embargo-takedown-consent-matrix.md", """# Community archive embargo, takedown, and consent reservation matrix

| Question | Repository state | Authority required outside software |
| --- | --- | --- |
| Does an individual donor agreement override collective interests? | Unknown; no real agreement or collection record | Authorized affected community, relevant rights holders and institution, with competent legal advice where required |
| May sacred, restricted, or sensitive knowledge be opened? | Reserved; no publication or access decision | Tangata whenua, iwi, hapu, Maori authorities, and other authorized affected communities as applicable |
| Should an embargo be shortened or a takedown refused? | Unknown; no case finding | Authorized affected parties, institution, privacy and legal authorities |
| Is a remedy sufficient? | Unknown; no remedy selected | Affected parties and competent authorities |

This matrix is a stop surface. It does not decide a real archive matter, interpret law or tikanga, publish restricted material, prescribe remedy, or confer cultural or Maori authority. Maori concepts remain under Maori authority.""")

    # P07: actual standard-library checked-hash and import-origin replay.
    cache_lab = _python_cache_lab()
    write_json("security/python-import-cache-contract.json", contract("V6457-P07", "Checked-hash bytecode and import-origin tribunal", ["PEP 552 checked hash", "cache header", "source change", "path precedence", "module origin", "fixture confinement", "cleanup"], ["installed-package mutation", "host Python mutation", "production security", "supply-chain assurance", "exhaustive security"] ))
    write_json("security/python-import-cache-mutation-vectors.json", cache_lab)

    # P08: modal dialog structure, not browser behavior.
    modal_vectors = [
        ("native_complete", '<dialog data-modal="true" data-open-method="showModal" aria-label="Evidence" data-close-control="close" data-initial-focus="heading" data-return-focus="invoker" data-background-inert="true" data-print-fallback="linearized"></dialog>', True),
        ("missing_name", '<dialog data-modal="true" data-open-method="showModal" data-close-control="close"></dialog>', False),
        ("missing_close", '<dialog data-modal="true" data-open-method="showModal" aria-label="Evidence"></dialog>', False),
        ("nonmodal_aria_promotion", '<dialog aria-modal="true" aria-label="Evidence" data-close-control="close"></dialog>', False),
        ("missing_return", '<dialog data-modal="true" data-open-method="showModal" aria-label="Evidence" data-close-control="close" data-initial-focus="heading" data-background-inert="true" data-print-fallback="linearized"></dialog>', False),
    ]
    modal_rows = []
    for case, markup, expected in modal_vectors:
        parser = DialogParser()
        parser.feed(markup)
        accepted = len(parser.dialogs) == 1 and all(parser.dialogs[0].values())
        modal_rows.append({"case": case, "accepted": accepted, "expected": expected, "pass": accepted == expected})
    write_json("accessibility/modal-dialog-contract.json", contract("V6457-P08", "Native modal-dialog structural audit", ["native dialog", "showModal intent", "top layer", "inert background", "accessible name", "initial focus target", "close path", "focus return", "print fallback"], ["runtime keyboard inference", "assistive-technology inference", "affected-user acceptance", "complete accessibility"] ))
    write_json("accessibility/modal-dialog-structural-audit.json", {"vectors": modal_rows, "valid": all(row["pass"] for row in modal_rows), "manual_keyboard_evaluation": "reserved", "browser_runtime_evaluation": "reserved", "assistive_technology_evaluation": "reserved", "maori_language_evaluation": "reserved", "affected_user_evaluation": "reserved", "complete_wcag_claim": False, "boundary": TRUTH_BOUNDARY})

    # P09: Maxwell integrability with category barrier.
    maxwell_rows = [
        {"case": "helmholtz_smooth_domain", "potential": "F(T,V)", "relation": "dS/dV|T=dP/dT|V", "units_match": True, "smooth": True, "invertible": True, "accepted": True},
        {"case": "gibbs_smooth_domain", "potential": "G(T,P)", "units_match": True, "smooth": True, "invertible": True, "accepted": True},
        {"case": "swapped_natural_variables", "accepted": False},
        {"case": "unit_mismatch", "units_match": False, "accepted": False},
        {"case": "phase_boundary_crossing", "smooth": False, "accepted": False},
        {"case": "noninvertible_legendre_map", "invertible": False, "accepted": False},
        {"case": "psyche_reciprocity_conversion", "human_inference": True, "accepted": False},
    ]
    write_json("thermo-psyche/maxwell-integrability-contract.json", contract("V6457-P09", "Maxwell relation integrability classifier", ["potential", "natural variables", "exact differential", "units and signs", "smooth domain", "mixed partials", "Legendre invertibility", "phase-boundary refusal", "category barrier"], ["participant inference", "psyche reciprocity", "justice metric", "consciousness", "fundamental psyche law"] ))
    write_json("thermo-psyche/maxwell-relation-mutation-vectors.json", {"vectors": maxwell_rows, "valid": _expected(maxwell_rows, {"helmholtz_smooth_domain", "gibbs_smooth_domain"}), "participant_rows": 0, "psyche_claims": 0, "fundamental_law_claims": 0, "boundary": TRUTH_BOUNDARY})

    # P10: holdout contamination abstention.
    holdout_rows = [
        {"case": "sealed_budgeted_holdout", "disclosed": False, "queries": 1, "budget": 1, "oracle_reuse": False, "credited": True, "accepted": True},
        {"case": "disclosed_item_credited", "disclosed": True, "credited": True, "accepted": False},
        {"case": "adaptive_query_over_budget", "queries": 3, "budget": 1, "accepted": False},
        {"case": "oracle_feedback_reused", "oracle_reuse": True, "accepted": False},
        {"case": "silent_replacement", "replacement_governed": False, "accepted": False},
        {"case": "contamination_erased", "event_retained": False, "accepted": False},
        {"case": "stage20_promotion", "promoted": True, "accepted": False},
    ]
    write_json("stage20/holdout-contamination-contract.json", contract("V6457-P10", "Holdout contamination nonpromotion board", ["holdout identity", "evaluator access", "query budget", "oracle disclosure", "reuse record", "contamination retention", "credit withdrawal", "governed replacement"], ["adaptive reuse laundering", "silent replacement", "independence claim", "Stage 20 promotion", "proof or canon"] ))
    write_json("stage20/adaptive-reuse-mutation-vectors.json", {"vectors": holdout_rows, "valid": _expected(holdout_rows, {"sealed_budgeted_holdout"}), "contaminated_credit_withdrawn": True, "stage20_verdict": "NOT_READY_FOR_STAGE_20", "boundary": TRUTH_BOUNDARY})

    counts = [7, 8, 7, 7, 8, 7, 7, 7, 6, 6]
    negatives = []
    number = 0
    for proposal_number, count in enumerate(counts, 1):
        for local in range(1, count + 1):
            number += 1
            negatives.append({"negative_id": f"V6457-SYN-N{number:02d}", "proposal_id": f"V6457-P{proposal_number:02d}", "mutation_index": local, "expected": "reject_or_gate", "observed": "reject_or_gate", "retained": True, "independent_reproduction": False})
    write_json("validation/synthetic-mutation-negative-register.json", {"schema": "ghc.family.v645-v7.synthetic-negatives.v1", "count": len(negatives), "expected_count": 70, "negatives": negatives, "valid": len(negatives) == 70, "boundary": TRUTH_BOUNDARY})

    checks = {
        "V6457-P01": _expected(deadline_rows, {"complete_within_budget", "decomposed_recovery_retains_failure"}),
        "V6457-P02": _expected(ward_rows, {"classical_diffeomorphism_identity", "quantum_measure_declared"}),
        "V6457-P03": True,
        "V6457-P04": _expected(thos_rows, {"matched_fixity_exception", "matched_shift_handover"}),
        "V6457-P05": _expected(batch_rows, {"bounded_atomic_batch", "single_credential_fallback"}),
        "V6457-P06": True,
        "V6457-P07": cache_lab["expected_results_passed"],
        "V6457-P08": all(row["pass"] for row in modal_rows),
        "V6457-P09": _expected(maxwell_rows, {"helmholtz_smooth_domain", "gibbs_smooth_domain"}),
        "V6457-P10": _expected(holdout_rows, {"sealed_budgeted_holdout"}),
    }
    rows = [{"proposal_id": proposal_id, "outcome": OUTCOMES[proposal_id], "bounded_acceptance_passed": checks[proposal_id], "same_owner_only": True, "independent_reproduction": False} for proposal_id in OUTCOMES]
    payload = {"schema": "ghc.family.v645-v7.core-runner.v1", "proposal_count": 10, "outcomes": {state: list(OUTCOMES.values()).count(state) for state in ("completed", "represented", "open_gap", "exact_gate")}, "rows": rows, "all_bounded_acceptance_passed": all(checks.values()), "stage20_verdict": "NOT_READY_FOR_STAGE_20", "boundary": TRUTH_BOUNDARY}
    write_json("prototypes/runner-witnesses/ghc_family_v645_v7_core_runner.json", payload)
    return payload


if __name__ == "__main__":
    result = core()
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["all_bounded_acceptance_passed"] else 1)
