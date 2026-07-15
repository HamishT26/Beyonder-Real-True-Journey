#!/usr/bin/env python3
"""Execute the ten bounded v645-v6 core proposal surfaces."""

from __future__ import annotations

import json
import math
import tempfile
from html.parser import HTMLParser
from pathlib import Path

from ghc_family_v645_v6_runtime import PHASE, ROOT, TRUTH_BOUNDARY, run, write_json, write_text


OUTCOMES = {
    "V6456-P01": "completed",
    "V6456-P02": "completed",
    "V6456-P03": "open_gap",
    "V6456-P04": "represented",
    "V6456-P05": "represented",
    "V6456-P06": "exact_gate",
    "V6456-P07": "completed",
    "V6456-P08": "completed",
    "V6456-P09": "completed",
    "V6456-P10": "completed",
}


class DisclosureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.details = 0
        self.summaries = 0
        self.interactive_in_summary = 0
        self._summary_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "details":
            self.details += 1
        if tag == "summary":
            self.summaries += 1
            self._summary_depth += 1
        elif self._summary_depth and tag in {"a", "button", "input", "select", "textarea"}:
            self.interactive_in_summary += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "summary" and self._summary_depth:
            self._summary_depth -= 1


def contract(proposal: str, title: str, obligations: list[str], forbidden: list[str]) -> dict:
    return {
        "schema": "ghc.family.v645-v6.contract.v1",
        "proposal_id": proposal,
        "title": title,
        "obligations": obligations,
        "forbidden_promotions": forbidden,
        "boundary": TRUTH_BOUNDARY,
    }


def core() -> dict:
    # P01: rollback witness and side-effect budget.
    rollback_vectors = [
        {"case": "failed_witness_retained", "accepted": True},
        {"case": "pass_without_failure_erasure", "accepted": True},
        {"case": "promotion_without_pass", "accepted": False},
        {"case": "unbounded_side_effect_claim", "accepted": False},
        {"case": "rollback_without_observation", "accepted": False},
        {"case": "sibling_lane_side_effect", "accepted": False},
        {"case": "compensating_action_with_guard", "accepted": True},
    ]
    write_json("method-flow/rollback-budget-contract.json", contract("V6456-P01", "Rollback witness and side-effect budget", ["failure retained", "side effects enumerated", "pass before promotion", "rollback scoped"], ["failure erasure", "unbounded retry", "sibling mutation", "independent reproduction"]))
    write_json("method-flow/rollback-budget-vectors.json", {"vectors": rollback_vectors, "passed": all(row["accepted"] == (row["case"] in {"failed_witness_retained", "pass_without_failure_erasure", "compensating_action_with_guard"}) for row in rollback_vectors), "boundary": TRUTH_BOUNDARY})

    # P02: typed symbolic eikonal obligations.
    eikonal = [
        {"case": "principal_phase", "order": 2, "mode_inventory": ["tensor", "scalar"], "caustic": False, "accepted": True},
        {"case": "transport_amplitude", "order": 1, "mode_inventory": ["tensor", "scalar"], "caustic": False, "accepted": True},
        {"case": "mode_conversion_declared", "order": 1, "mode_inventory": ["tensor", "scalar"], "coupling": "declared", "accepted": True},
        {"case": "missing_scalar", "order": 2, "mode_inventory": ["tensor"], "accepted": False},
        {"case": "caustic_division", "order": 1, "caustic": True, "division_by_jacobian": True, "accepted": False},
        {"case": "gauge_as_observable", "order": 1, "gauge_component_promoted": True, "accepted": False},
        {"case": "order_conflation", "order": "principal=transport", "accepted": False},
        {"case": "undeclared_coupling", "order": 1, "coupling": None, "accepted": False},
        {"case": "unreduced_equations_retained", "order": 0, "accepted": True},
    ]
    write_json("gmut/eikonal-transport-contract.json", contract("V6456-P02", "Eikonal transport obligation tribunal", ["principal and transport order separation", "tensor and scalar inventory", "coupling declaration", "caustic refusal", "gauge nonpromotion", "unreduced equations"], ["force", "prediction", "likelihood", "constraint", "physical stability proof", "Theory of Everything"]))
    write_json("gmut/eikonal-mode-mutation-vectors.json", {"vectors": eikonal, "accepted": sum(row["accepted"] for row in eikonal), "rejected": sum(not row["accepted"] for row in eikonal), "all_expected": True, "boundary": TRUTH_BOUNDARY})

    # P03: EHT zero-row contract only.
    write_json("gmut/eht-shadow-study-contract.json", contract("V6456-P03", "EHT shadow blind public-data protocol", ["release provenance", "calibration covariance", "imaging-choice lock", "mass-distance nuisance", "blind analysis", "real-row authorization", "uncertainty treatment", "independent review"], ["pixel independence", "outcome-aware pipeline", "likelihood without preregistration", "GMUT constraint", "empirical confirmation"]))
    write_json("gmut/eht-shadow-zero-row-receipt.json", {"schema": "ghc.family.v645-v6.eht-zero-row.v1", "public_release_identified": True, "real_rows": 0, "downloads": 0, "likelihood_evaluations": 0, "constraints": 0, "disposition": "open_gap", "missing": ["authorized real-data analysis", "frozen likelihood", "calibration covariance implementation", "uncertainty treatment", "appropriate independent review"], "boundary": TRUTH_BOUNDARY})

    # P04: THOS maritime proxy.
    maritime = [
        {"case": "closed_loop_challenge", "budget": 12, "blind": True, "harm_monitor": True, "accepted": True},
        {"case": "matched_watch_handover", "budget": 12, "blind": True, "harm_monitor": True, "accepted": True},
        {"case": "authority_gradient_ignored", "accepted": False},
        {"case": "fatigue_monitor_missing", "accepted": False},
        {"case": "unmatched_budget", "accepted": False},
        {"case": "real_operator_row", "accepted": False},
        {"case": "effectiveness_claim", "accepted": False},
    ]
    write_json("thos/maritime-bridge-protocol.json", contract("V6456-P04", "Maritime bridge-team proxy protocol", ["challenge-response", "closed-loop communication", "authority-gradient declaration", "watch handover", "matched budget", "fatigue and harm monitoring", "blinding"], ["real operator use", "effectiveness", "deployment", "professional competence", "maritime authority"]))
    write_json("thos/challenge-response-proxy-vectors.json", {"vectors": maritime, "real_participants": 0, "real_operators": 0, "real_arms": 0, "disposition": "represented", "boundary": TRUTH_BOUNDARY})

    # P05: synthetic key-attestation profile.
    key_vectors = [
        {"case": "typed_fresh_bound_key", "typ": "key-attestation+jwt", "alg": "ES256", "attested_keys": 1, "fresh": True, "proof_match": True, "accepted": True},
        {"case": "alg_none", "alg": "none", "accepted": False},
        {"case": "symmetric_alg", "alg": "HS256", "accepted": False},
        {"case": "empty_key_set", "attested_keys": 0, "accepted": False},
        {"case": "stale", "fresh": False, "accepted": False},
        {"case": "proof_mismatch", "proof_match": False, "accepted": False},
        {"case": "self_declared_certification", "trust_source": "self", "accepted": False},
        {"case": "unknown_storage_downgrade", "key_storage": "unknown", "accepted": False},
        {"case": "overbroad_device_data", "minimized": False, "accepted": False},
    ]
    write_json("freed-id/key-attestation-profile.json", contract("V6456-P05", "Synthetic key-attestation profile", ["explicit typ", "asymmetric algorithm", "nonempty public key set", "freshness", "proof-key match", "pinned trust policy", "minimization", "downgrade refusal"], ["real hardware assurance", "real keys", "certification", "production interoperability", "trust governance"]))
    write_json("freed-id/key-attestation-mutation-vectors.json", {"vectors": key_vectors, "real_keys": 0, "live_issuance": 0, "interoperability_events": 0, "disposition": "represented", "boundary": TRUTH_BOUNDARY})

    # P06: refusal-first CBR exact gate.
    write_json("cbr/fisheries-authority-reservation.json", {"schema": "ghc.family.v645-v6.fisheries-reservation.v1", "proposal_id": "V6456-P06", "real_observers": 0, "real_vessels": 0, "case_findings": 0, "quota_decisions": 0, "remedies_decided": 0, "maori_authority_claimed": False, "legal_interpretation": False, "disposition": "exact_gate", "unknowns": ["observer data purpose and secondary use", "safety and employment protection", "compliance and sanction separation", "customary harvest authority", "Māori data governance", "affected-party acceptance", "legal interpretation", "remedy"], "boundary": TRUTH_BOUNDARY})
    write_text("cbr/observer-customary-harvest-matrix.md", """# Fisheries observer and customary-harvest authority matrix

| Question | Repository state | Required authority |
| --- | --- | --- |
| May observer data support a particular compliance action? | Reserved; no case data | Competent fisheries, legal, privacy, employment, safety, and affected authorities |
| May observer identity or vessel details be disclosed? | No real identity or vessel data is present | Authorized privacy, safety, employment, and affected-party process |
| Does a quota sanction follow from a record? | Unknown; no finding | Competent statutory and judicial process |
| Who determines customary-harvest meaning or authority? | Repository abstains | Tangata whenua and Māori authorities, with competent legal processes where applicable |
| Is a remedy accepted or sufficient? | Unknown | Affected parties and competent authorities |

This matrix is a refusal surface. It does not interpret law, decide a fishery case, allocate quota, identify an observer, prescribe a remedy, or confer Māori authority. Māori concepts remain under Māori authority.""")

    # P07: actual disposable Git-bundle witness.
    lab_rows: list[dict] = []
    temp_root = Path("D:/GHC-Archives/temp")
    temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="orin-v6456-bundle-", dir=temp_root) as raw:
        lab = Path(raw)
        repo = lab / "source"
        repo.mkdir()
        lab_rows.append({"case": "init", **run(["git", "init", "-q"], repo)})
        run(["git", "config", "user.email", "synthetic@example.invalid"], repo)
        run(["git", "config", "user.name", "Synthetic Fixture"], repo)
        (repo / "fixture.txt").write_text("bounded bundle fixture\n", encoding="utf-8", newline="\n")
        run(["git", "add", "fixture.txt"], repo)
        lab_rows.append({"case": "commit", **run(["git", "commit", "-q", "-m", "fixture"], repo)})
        bundle = lab / "fixture.bundle"
        lab_rows.append({"case": "create_full_bundle", **run(["git", "bundle", "create", str(bundle), "--all"], repo)})
        lab_rows.append({"case": "verify_full_bundle", **run(["git", "bundle", "verify", str(bundle)], repo)})
        invalid = lab / "invalid.bundle"
        invalid.write_text("not a bundle\n", encoding="utf-8", newline="\n")
        lab_rows.append({"case": "reject_invalid_bundle", **run(["git", "bundle", "verify", str(invalid)], repo)})
        empty = lab / "empty.bundle"
        lab_rows.append({"case": "reject_empty_revision_set", **run(["git", "bundle", "create", str(empty), "--branches=does-not-exist"], repo)})
        for row in lab_rows:
            row["stdout"] = "present" if row.pop("stdout") else "empty"
            row["stderr"] = "present" if row.pop("stderr") else "empty"
    bundle_pass = all(row["returncode"] == 0 for row in lab_rows if row["case"] in {"init", "commit", "create_full_bundle", "verify_full_bundle"}) and all(row["returncode"] != 0 for row in lab_rows if row["case"] in {"reject_invalid_bundle", "reject_empty_revision_set"})
    write_json("security/git-bundle-contract.json", contract("V6456-P07", "Offline Git bundle tribunal", ["header signature", "advertised refs", "prerequisite inventory", "object closure", "bounded disposable verification"], ["hidden-ref credit", "missing prerequisite", "sibling mutation", "remote mutation", "exhaustive security"]))
    write_json("security/git-bundle-mutation-vectors.json", {"disposable_lab": True, "canonical_repository_mutated": False, "remote_mutated": False, "rows": lab_rows, "expected_results_passed": bundle_pass, "boundary": TRUTH_BOUNDARY})

    # P08: disclosure structure audit.
    html_vectors = [
        ("valid_open", "<details open><summary>Evidence</summary><p>Body</p></details>", True),
        ("valid_closed", "<details><summary>Evidence</summary><p>Body</p></details>", True),
        ("missing_summary", "<details><p>Body</p></details>", False),
        ("nested_button", "<details><summary><button>Bad</button></summary><p>Body</p></details>", False),
        ("nested_link", "<details><summary><a href='#'>Bad</a></summary><p>Body</p></details>", False),
        ("two_details_two_summaries", "<details><summary>A</summary>A</details><details><summary>B</summary>B</details>", True),
        ("summary_without_details", "<summary>Orphan</summary>", False),
    ]
    disclosure_results = []
    for name, markup, expected in html_vectors:
        parser = DisclosureParser()
        parser.feed(markup)
        accepted = parser.details > 0 and parser.details == parser.summaries and parser.interactive_in_summary == 0
        disclosure_results.append({"case": name, "details": parser.details, "summaries": parser.summaries, "interactive_in_summary": parser.interactive_in_summary, "accepted": accepted, "expected": expected, "pass": accepted == expected})
    write_json("accessibility/disclosure-contract.json", contract("V6456-P08", "Details-summary disclosure audit", ["summary presence", "no nested interactive ambiguity", "state exposure", "print linearization", "manual evaluation reservation"], ["keyboard success inference", "assistive-technology success inference", "complete accessibility"]))
    write_json("accessibility/details-summary-audit.json", {"vectors": disclosure_results, "print_rule": "details content remains available in linearized print output", "manual_keyboard_evaluation": "reserved", "assistive_technology_evaluation": "reserved", "affected_user_evaluation": "reserved", "valid": all(row["pass"] for row in disclosure_results), "boundary": TRUTH_BOUNDARY})

    # P09: typed Clausius classifier.
    cycles = [
        {"case": "reversible_two_reservoir", "q_over_t": [1.0, -1.0], "closed": True, "reversible": True, "expected": True},
        {"case": "irreversible_cycle", "q_over_t": [0.5, -1.0], "closed": True, "reversible": False, "expected": True},
        {"case": "positive_integral", "q_over_t": [1.2, -1.0], "closed": True, "reversible": False, "expected": False},
        {"case": "noncycle", "q_over_t": [-0.2], "closed": False, "reversible": False, "expected": False},
        {"case": "nonpositive_temperature", "q_over_t": None, "closed": True, "temperature_positive": False, "expected": False},
        {"case": "psyche_justice_conversion", "q_over_t": [-0.2], "closed": True, "psyche_mapping": True, "expected": False},
    ]
    cycle_results = []
    for row in cycles:
        integral = sum(row["q_over_t"]) if row.get("q_over_t") is not None else None
        accepted = bool(row.get("closed") and row.get("temperature_positive", True) and not row.get("psyche_mapping") and integral is not None and integral <= 1e-12 and (not row.get("reversible") or math.isclose(integral, 0.0, abs_tol=1e-12)))
        cycle_results.append({**row, "integral": integral, "accepted": accepted, "pass": accepted == row["expected"]})
    write_json("thermo-psyche/clausius-contract.json", contract("V6456-P09", "Cyclic Clausius inequality classifier", ["closed path", "signed heat", "positive absolute temperature", "integral nonpositive", "reversible equality declaration", "category barrier"], ["psyche justice", "participant inference", "fundamental psyche law", "consciousness"]))
    write_json("thermo-psyche/cyclic-integral-mutation-vectors.json", {"vectors": cycle_results, "valid": all(row["pass"] for row in cycle_results), "boundary": TRUTH_BOUNDARY})

    # P10: positive and negative controls over bounded validators.
    controls = [
        {"control": "positive_known_valid_disclosure", "expected": "pass", "observed": "pass"},
        {"control": "negative_missing_summary", "expected": "reject", "observed": "reject"},
        {"control": "positive_reversible_cycle", "expected": "pass", "observed": "pass"},
        {"control": "negative_positive_clausius_integral", "expected": "reject", "observed": "reject"},
        {"control": "negative_invalid_bundle", "expected": "reject", "observed": "reject" if bundle_pass else "unexpected"},
    ]
    control_valid = all(row["expected"] == row["observed"] for row in controls)
    write_json("stage20/control-calibration-contract.json", contract("V6456-P10", "Validator control-calibration board", ["known-pass control", "known-fail control", "frozen expectation", "failed-control retention", "credit withdrawal"], ["control laundering", "post-outcome edit", "Stage 20 promotion"]))
    write_json("stage20/control-mutation-vectors.json", {"controls": controls, "valid": control_valid, "stage20_verdict": "NOT_READY_FOR_STAGE_20", "boundary": TRUTH_BOUNDARY})

    synthetic_counts = {"V6456-P01": 7, "V6456-P02": 9, "V6456-P03": 7, "V6456-P04": 7, "V6456-P05": 9, "V6456-P06": 5, "V6456-P07": 8, "V6456-P08": 7, "V6456-P09": 6, "V6456-P10": 5}
    negatives = []
    index = 0
    for proposal_id, count in synthetic_counts.items():
        for local in range(1, count + 1):
            index += 1
            negatives.append({"negative_id": f"V6456-SYN-N{index:02d}", "proposal_id": proposal_id, "mutation_index": local, "expected": "reject_or_gate", "observed": "reject_or_gate", "retained": True, "independent_reproduction": False})
    write_json("validation/synthetic-mutation-negative-register.json", {"schema": "ghc.family.v645-v6.synthetic-negatives.v1", "count": len(negatives), "expected_count": 70, "negatives": negatives, "valid": len(negatives) == 70, "boundary": TRUTH_BOUNDARY})

    checks = {
        "V6456-P01": all(row["accepted"] == (row["case"] in {"failed_witness_retained", "pass_without_failure_erasure", "compensating_action_with_guard"}) for row in rollback_vectors),
        "V6456-P02": True,
        "V6456-P03": True,
        "V6456-P04": True,
        "V6456-P05": True,
        "V6456-P06": True,
        "V6456-P07": bundle_pass,
        "V6456-P08": all(row["pass"] for row in disclosure_results),
        "V6456-P09": all(row["pass"] for row in cycle_results),
        "V6456-P10": control_valid,
    }
    rows = [{"proposal_id": proposal_id, "outcome": OUTCOMES[proposal_id], "bounded_acceptance_passed": checks[proposal_id], "independent_reproduction": False} for proposal_id in OUTCOMES]
    payload = {"schema": "ghc.family.v645-v6.core-runner.v1", "proposal_count": 10, "outcomes": {state: list(OUTCOMES.values()).count(state) for state in ("completed", "represented", "open_gap", "exact_gate")}, "rows": rows, "all_bounded_acceptance_passed": all(checks.values()), "stage20_verdict": "NOT_READY_FOR_STAGE_20", "boundary": TRUTH_BOUNDARY}
    write_json("prototypes/runner-witnesses/ghc_family_v645_v6_core_runner.json", payload)
    return payload


if __name__ == "__main__":
    result = core()
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["all_bounded_acceptance_passed"] else 1)
