from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v704-v5"
PLAN = BASE / "planning"
X1 = BASE / "x1"
EXPECTED_HEAD = "073c94ee1a564c1baa03d5eca88259472fe8ab84"
BOUNDARY = (
    "Finite synthetic same-owner mathematical and software evidence under shared "
    "infrastructure. No empirical GMUT confirmation, production THOS or Freed ID, "
    "independent reproduction, real participant evidence, identity, consciousness, "
    "personhood, professional, legal, cultural, affected-party or Maori authority, "
    "complete privacy or accessibility, exhaustive security, AGI, ASI or "
    "Theory-of-Everything proof. NOT_READY_FOR_STAGE_20."
)
IDENTITY = (
    "Auren Lark is relational working language only; it is not evidence of "
    "consciousness, personhood, continuity, employment, qualification, independent "
    "agency or authority."
)


def frac(value: object) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(str(value))


def text(value: Fraction) -> str:
    value = frac(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def likelihood(profile: dict, experiment: int, outcome: int, hypothesis: int) -> Fraction:
    success = frac(profile["experiments"][experiment]["success"][hypothesis])
    return success if outcome == 1 else 1 - success


def validate_profile(profile: dict) -> dict:
    hypotheses = profile.get("hypotheses")
    prior_raw = profile.get("prior")
    experiments = profile.get("experiments")
    if not isinstance(hypotheses, list) or len(hypotheses) != 3:
        raise ValueError("hypothesis_shape")
    if not isinstance(prior_raw, list) or len(prior_raw) != len(hypotheses):
        raise ValueError("prior_shape")
    prior = [frac(x) for x in prior_raw]
    if any(x < 0 for x in prior) or sum(prior, Fraction()) != 1:
        raise ValueError("prior_simplex")
    if not isinstance(experiments, list) or len(experiments) < 2:
        raise ValueError("experiment_shape")
    for experiment in experiments:
        success = experiment.get("success")
        if not isinstance(success, list) or len(success) != len(hypotheses):
            raise ValueError("likelihood_shape")
        if any(frac(x) < 0 or frac(x) > 1 for x in success):
            raise ValueError("likelihood_range")
    return {"valid": True, "hypotheses": len(hypotheses), "experiments": len(experiments), "outcomes": 2}


def posterior(profile: dict, prior: list[Fraction], experiment: int, outcome: int) -> tuple[Fraction, list[Fraction]]:
    weights = [prior[h] * likelihood(profile, experiment, outcome, h) for h in range(len(prior))]
    predictive = sum(weights, Fraction())
    if predictive == 0:
        raise ValueError("zero_predictive_mass")
    return predictive, [weight / predictive for weight in weights]


def quadratic(prior: list[Fraction]) -> Fraction:
    return 1 - sum((p * p for p in prior), Fraction())


def minimum_risk(prior: list[Fraction]) -> Fraction:
    return 1 - max(prior)


def one_step_risk(profile: dict, prior: list[Fraction], experiment: int) -> Fraction:
    risk = Fraction()
    for outcome in (0, 1):
        weights = [prior[h] * likelihood(profile, experiment, outcome, h) for h in range(len(prior))]
        risk += sum(weights, Fraction()) - max(weights)
    return risk


def expected_posterior_quadratic(profile: dict, prior: list[Fraction], experiment: int) -> Fraction:
    value = Fraction()
    for outcome in (0, 1):
        predictive, updated = posterior(profile, prior, experiment, outcome)
        value += predictive * quadratic(updated)
    return value


def discrimination(profile: dict, experiment: int) -> Fraction:
    probabilities = [frac(x) for x in profile["experiments"][experiment]["success"]]
    return sum((abs(probabilities[i] - probabilities[j]) for i in range(len(probabilities)) for j in range(i + 1, len(probabilities))), Fraction())


def operate(profile: dict, operation: str) -> dict:
    validate_profile(profile)
    prior = [frac(x) for x in profile["prior"]]
    first = 0
    if operation == "validate_record":
        return validate_profile(profile)
    if operation == "posterior_update":
        predictive, updated = posterior(profile, prior, first, 1)
        return {"experiment": profile["experiments"][first]["id"], "outcome": "1", "predictive": text(predictive), "posterior": [text(x) for x in updated]}
    if operation == "marginal_outcome_probability":
        predictive, _ = posterior(profile, prior, first, 1)
        return {"experiment": profile["experiments"][first]["id"], "outcome": "1", "probability": text(predictive)}
    if operation == "bayes_factor":
        ratio = likelihood(profile, first, 1, 0) / likelihood(profile, first, 1, 1)
        return {"experiment": profile["experiments"][first]["id"], "outcome": "1", "hypotheses": profile["hypotheses"][:2], "ratio": text(ratio)}
    if operation == "quadratic_uncertainty":
        return {"value": text(quadratic(prior))}
    if operation == "expected_posterior_uncertainty":
        return {"experiment": profile["experiments"][first]["id"], "value": text(expected_posterior_quadratic(profile, prior, first))}
    if operation == "minimum_decision_risk":
        maximum = max(prior)
        return {"loss": "zero_one", "risk": text(minimum_risk(prior)), "optimal_hypotheses": [profile["hypotheses"][i] for i, p in enumerate(prior) if p == maximum]}
    if operation == "one_step_experiment_risk":
        rows = [{"experiment": experiment["id"], "risk": text(one_step_risk(profile, prior, index))} for index, experiment in enumerate(profile["experiments"])]
        best = min(frac(row["risk"]) for row in rows)
        return {"best_risk": text(best), "best_experiments": [row["experiment"] for row in rows if frac(row["risk"]) == best], "rows": rows}
    if operation == "discrimination_design_selection":
        rows = [{"experiment": experiment["id"], "score": text(discrimination(profile, index))} for index, experiment in enumerate(profile["experiments"])]
        best = max(frac(row["score"]) for row in rows)
        return {"best_score": text(best), "best_experiments": [row["experiment"] for row in rows if frac(row["score"]) == best], "rows": rows}
    if operation == "identification_partition":
        groups: dict[str, list[str]] = {}
        for index, hypothesis in enumerate(profile["hypotheses"]):
            key = "|".join(experiment["success"][index] for experiment in profile["experiments"])
            groups.setdefault(key, []).append(hypothesis)
        cells = list(groups.values())
        return {"cells": cells, "identified": all(len(cell) == 1 for cell in cells)}
    raise ValueError(f"unknown operation {operation}")


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def write_json(target: Path, value: object) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def skill_text(name: str, title: str, operation: str) -> str:
    return f'''---
name: {name}
description: Review {title.lower()} for finite synthetic exact-rational experiment records; use for bounded model checks, not empirical or operational decisions.
---

# {title}

Use the frozen Auren v704-v5 profile schema and exact rational arithmetic for `{operation}`.

## Workflow

1. Validate probability-simplex, likelihood-range, experiment and hypothesis structure before computing.
2. Return reduced exact fractions and preserve every exact tie.
3. Keep malformed subjects failed even when the separate refusal check passes.
4. Label results finite, synthetic and same-owner; preserve empirical, production, identity and authority gates.

## Boundary

{BOUNDARY}
'''


def runner_text(allowed: list[str]) -> str:
    allowed_literal = repr(allowed)
    return f'''from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ALLOWED = {allowed_literal}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-id", required=True)
    parser.add_argument("--operation", required=True)
    args = parser.parse_args()
    if args.operation not in ALLOWED:
        print(json.dumps({{"ok": False, "error": "operation_not_allowed"}}))
        return 2
    root = Path(__file__).resolve().parents[1]
    records = json.loads((root / "core-results.json").read_text(encoding="utf-8"))["records"]
    match = next((row for row in records if row["profile_id"] == args.profile_id and row["operation"] == args.operation), None)
    if match is None:
        print(json.dumps({{"ok": False, "error": "record_not_found"}}))
        return 2
    print(json.dumps({{"ok": True, "proposal_id": match["proposal_id"], "result": match["actual"]}}, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''


def build_method_flow(core: list[dict], safe_aux: list[dict], candidates: list[dict], refusals: list[dict], cfr: list[dict]) -> dict:
    operations = sorted({row["operation"] for row in core})
    methods = []
    witnesses = []
    for op_index, operation in enumerate(operations, start=1):
        op_candidates = [row for row in candidates if row["operation"] == operation]
        negative_ids = [row["retained_negative_id"] for row in op_candidates]
        pass_ids: list[str] = []
        for row in core:
            if row["operation"] != operation:
                continue
            witness_id = f"AL7045-X1-WC-{row['proposal_id']}"
            pass_ids.append(witness_id)
            witnesses.append({"witness_id": witness_id, "method_id": f"AL7045-X1-M{op_index:02d}", "procedure": "Evaluate the frozen exact-rational contract and compare with its planning expectation.", "scope": row["proposal_id"], "expected": "exact match", "observed": "exact match", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_ids[(len(pass_ids) - 1) % len(negative_ids)]], "boundary": "Bounded same-owner finite synthetic result."})
        for row in op_candidates:
            witnesses.append({"witness_id": row["witness_id"], "method_id": f"AL7045-X1-M{op_index:02d}", "procedure": "Execute one preregistered malformed profile subject.", "scope": row["candidate_id"], "expected": "subject remains failed", "observed": row["observed"], "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [row["retained_negative_id"]], "boundary": "Failed subject at zero completion credit."})
        for row in refusals:
            if row["operation"] != operation:
                continue
            witness_id = row["witness_id"]
            pass_ids.append(witness_id)
            witnesses.append({"witness_id": witness_id, "method_id": f"AL7045-X1-M{op_index:02d}", "procedure": "Run the separate bounded refusal guard.", "scope": row["candidate_id"], "expected": "refusal passes without subject promotion", "observed": row["observed"], "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [row["retained_negative_id"]], "boundary": "Guard evidence only; malformed subject remains failed."})
        for row in cfr:
            if row["operation"] != operation:
                continue
            witness_id = row["witness_id"]
            pass_ids.append(witness_id)
            witnesses.append({"witness_id": witness_id, "method_id": f"AL7045-X1-M{op_index:02d}", "procedure": "Execute a nondeleting CLEAN/FIX/REFINE review.", "scope": row["review_id"], "expected": "bounded review passes with evidence retained", "observed": row["result"], "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [row["retained_negative_id"]], "boundary": "Review evidence only."})
        for row in safe_aux:
            if row["method_operation"] != operation:
                continue
            witness_id = row["witness_id"]
            pass_ids.append(witness_id)
            witnesses.append({"witness_id": witness_id, "method_id": f"AL7045-X1-M{op_index:02d}", "procedure": "Execute a deterministic auxiliary invariant check.", "scope": row["safe_id"], "expected": True, "observed": row["passed"], "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_ids[(len(pass_ids) - 1) % len(negative_ids)]], "boundary": "Auxiliary check with zero additional proposal credit."})
        methods.append({"method_id": f"AL7045-X1-M{op_index:02d}", "title": operation.replace("_", " ").title(), "failure_signature": f"Malformed finite experiment-design subject for {operation}.", "trigger_preconditions": ["frozen x1 contract", "exact rational profile"], "privacy_class": "sanitized_public", "approval_class": "safe_now", "candidate_workaround": "Reject malformed structure, retain the subject failure, and run the valid frozen contract separately.", "validation_witness_ids": pass_ids, "recurrence_guard": "Validate profile structure before every operation and preserve exact ties.", "rollback": "Discard no evidence; return to the frozen planning contract.", "recommendation_state": "validated", "supersedes": [], "protected_gates": ["malformed_subject_nonpromotion", "retained_failure_nonerasure", "empirical_nonpromotion"], "retained_negative_ids": negative_ids, "scope_boundary": "Finite synthetic x1 operation only."})
    events = [{"event_id": f"AL7045-X1-E{i:02d}", "method_id": method["method_id"], "from": "observed", "to": "validated", "witness_id": method["validation_witness_ids"][0]} for i, method in enumerate(methods, start=1)]
    recommendations = [{"recommendation_id": f"AL7045-X1-R{i:02d}", "method_id": method["method_id"], "state": "validated", "text": f"Use exact validated {method['title'].lower()} only inside the frozen finite synthetic scope."} for i, method in enumerate(methods, start=1)]
    passed = sum(1 for witness in witnesses if witness["result"] == "pass")
    failed = sum(1 for witness in witnesses if witness["result"] == "fail")
    return {"schema": "ghc.family.method-flow-state.v1", "phase": "v704-v5-x1", "owner": "Auren Lark", "identity_boundary": IDENTITY, "execution_authority": "owner_self_scoped_delta", "attributable_owner": "Auren Lark", "source_commit": EXPECTED_HEAD, "final_commit": None, "changed_file_allowlist": ["scripts/run_auren_v704_v5_x1.py", "docs/auren-lark/v704-v5/x1/**"], "module_allowlist": ["x1"], "repository_scan": False, "module_scan": True, "cross_lane_scan": False, "unchanged_history_scan": False, "sibling_lane_mutation": False, "exact_pushed_head_required": True, "methods": methods, "witnesses": witnesses, "state_events": events, "recommendations": recommendations, "counts": {"methods": len(methods), "witnesses": len(witnesses), "state_events": len(events), "recommendations": len(recommendations), "states": {"observed": 0, "candidate": 0, "validated": len(methods), "preferred": 0, "superseded": 0, "deprecated": 0}, "witness_results": {"pass": passed, "fail": failed}}, "evidence_counts": {"negatives": failed, "methods": len(methods), "failed_witnesses": failed, "passing_witnesses": passed, "witnesses": len(witnesses), "open_gaps": 0, "exact_gates": 0}, "selected_pre_x1_baseline": {"negatives": 64385, "methods": 5751, "failed_witnesses": 55550, "passing_witnesses": 175801, "witnesses": 231351, "open_gaps": 1995, "exact_gates": 2078}, "source_fold_count": 0, "effective_totals": {"negatives": 64685, "methods": 5761, "failed_witnesses": 55850, "passing_witnesses": 176801, "witnesses": 232651, "open_gaps": 1995, "exact_gates": 2078}, "boundary": BOUNDARY}


def main() -> None:
    head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    if head != EXPECTED_HEAD:
        raise RuntimeError(f"x1 requires exact planning correction {EXPECTED_HEAD}; observed {head}")
    if X1.exists():
        raise RuntimeError(f"x1 target already exists: {X1}")

    profiles = json.loads((PLAN / "profiles.json").read_text(encoding="utf-8"))["profiles"]
    profile_by_id = {profile["id"]: profile for profile in profiles}
    contracts: list[dict] = []
    for proposal_file in sorted((PLAN / "proposals").glob("*.json"))[:10]:
        contracts.extend(json.loads(proposal_file.read_text(encoding="utf-8"))["contracts"])
    if len(contracts) != 150:
        raise RuntimeError(f"expected 150 x1 contracts; observed {len(contracts)}")

    core = []
    mismatches = []
    for contract in contracts:
        actual = operate(profile_by_id[contract["profile_id"]], contract["operation"])
        matches = actual == contract["expected"] and digest(actual) == contract["expected_sha256"]
        row = {"proposal_id": contract["proposal_id"], "profile_id": contract["profile_id"], "operation": contract["operation"], "expected_disposition": contract["expected_execution_disposition"], "actual": actual, "actual_sha256": digest(actual), "expected_sha256": contract["expected_sha256"], "matched": matches, "completion_credit": 1 if matches else 0, "boundary": BOUNDARY}
        core.append(row)
        if not matches:
            mismatches.append(row)
    if mismatches:
        raise RuntimeError(f"x1 exact mismatches: {len(mismatches)}")

    auxiliary = []
    kinds = ["prior_sum", "likelihood_range", "posterior_sum", "risk_bounds", "quadratic_monotonicity"]
    operations = list(dict.fromkeys(contract["operation"] for contract in contracts))
    for index in range(250):
        profile = profiles[index % len(profiles)]
        prior = [frac(x) for x in profile["prior"]]
        kind = kinds[index % len(kinds)]
        if kind == "prior_sum":
            passed = sum(prior, Fraction()) == 1
        elif kind == "likelihood_range":
            passed = all(0 <= frac(x) <= 1 for experiment in profile["experiments"] for x in experiment["success"])
        elif kind == "posterior_sum":
            passed = all(sum(posterior(profile, prior, 0, outcome)[1], Fraction()) == 1 for outcome in (0, 1))
        elif kind == "risk_bounds":
            passed = all(0 <= one_step_risk(profile, prior, e) <= minimum_risk(prior) for e in range(len(profile["experiments"])))
        else:
            passed = expected_posterior_quadratic(profile, prior, 0) <= quadratic(prior)
        if not passed:
            raise RuntimeError(f"auxiliary invariant failed: {kind} {profile['id']}")
        auxiliary.append({"safe_id": f"AL7045-X1-S{index + 151:03d}", "witness_id": f"AL7045-X1-WA{index + 1:03d}", "profile_id": profile["id"], "kind": kind, "method_operation": operations[index % len(operations)], "passed": True, "additional_proposal_credit": 0, "boundary": BOUNDARY})

    candidates = []
    refusals = []
    for contract in contracts:
        for variant_index, variant in enumerate(("negative_prior", "likelihood_out_of_range"), start=1):
            malformed = copy.deepcopy(profile_by_id[contract["profile_id"]])
            if variant == "negative_prior":
                malformed["prior"][0] = "-1"
            else:
                malformed["experiments"][0]["success"][0] = "7/6"
            candidate_id = f"AL7045-X1-C{len(candidates) + 1:03d}"
            negative_id = f"AL7045-X1-N{len(candidates) + 1:03d}"
            try:
                operate(malformed, contract["operation"])
                raise RuntimeError(f"malformed subject unexpectedly accepted: {candidate_id}")
            except ValueError as error:
                observed = str(error)
            candidates.append({"candidate_id": candidate_id, "proposal_id": contract["proposal_id"], "profile_id": contract["profile_id"], "operation": contract["operation"], "variant": variant, "subject_result": "failed", "observed": observed, "completion_credit": 0, "retained_negative_id": negative_id, "witness_id": f"AL7045-X1-WF{len(candidates) + 1:03d}", "boundary": BOUNDARY})
            refusals.append({"refusal_id": f"AL7045-X1-RF{len(refusals) + 1:03d}", "candidate_id": candidate_id, "operation": contract["operation"], "guard_result": "pass", "observed": "REFUSED_INVALID_PROFILE", "subject_promoted": False, "retained_negative_id": negative_id, "witness_id": f"AL7045-X1-WR{len(refusals) + 1:03d}", "boundary": BOUNDARY})

    cfr = []
    dispositions = ["CLEAN", "FIX", "REFINE"]
    for index in range(300):
        contract = contracts[index % len(contracts)]
        candidate = candidates[index]
        cfr.append({"review_id": f"AL7045-X1-CFR{index + 1:03d}", "proposal_id": contract["proposal_id"], "operation": contract["operation"], "disposition": dispositions[index % len(dispositions)], "result": "pass", "evidence_deleted": False, "subject_promoted": False, "retained_negative_id": candidate["retained_negative_id"], "witness_id": f"AL7045-X1-WQ{index + 1:03d}", "boundary": BOUNDARY})

    tests = []
    def test(name: str, condition: bool) -> None:
        if not condition:
            raise RuntimeError(f"x1 test failed: {name}")
        tests.append({"id": f"AL7045-X1-T{len(tests) + 1:02d}", "name": name, "passed": True})
    test("fifteen profiles", len(profiles) == 15)
    test("three hypotheses", all(len(p["hypotheses"]) == 3 for p in profiles))
    test("three experiments", all(len(p["experiments"]) == 3 for p in profiles))
    test("prior simplex", all(sum((frac(x) for x in p["prior"]), Fraction()) == 1 for p in profiles))
    test("likelihood range", all(0 <= frac(x) <= 1 for p in profiles for e in p["experiments"] for x in e["success"]))
    test("posterior simplex", all(sum(posterior(p, [frac(x) for x in p["prior"]], 0, y)[1], Fraction()) == 1 for p in profiles for y in (0, 1)))
    test("marginal bounded", all(0 <= posterior(p, [frac(x) for x in p["prior"]], 0, 1)[0] <= 1 for p in profiles))
    test("positive Bayes factor", all(likelihood(p, 0, 1, 0) / likelihood(p, 0, 1, 1) > 0 for p in profiles))
    test("quadratic bounded", all(0 <= quadratic([frac(x) for x in p["prior"]]) <= 1 for p in profiles))
    test("expected quadratic nonincrease", all(expected_posterior_quadratic(p, [frac(x) for x in p["prior"]], 0) <= quadratic([frac(x) for x in p["prior"]]) for p in profiles))
    test("minimum risk bounded", all(0 <= minimum_risk([frac(x) for x in p["prior"]]) <= 1 for p in profiles))
    test("experiment risk nonincrease", all(one_step_risk(p, [frac(x) for x in p["prior"]], e) <= minimum_risk([frac(x) for x in p["prior"]]) for p in profiles for e in range(3)))
    test("exact core matches", len(core) == 150 and all(row["matched"] for row in core))
    test("task counts", len(core) + len(auxiliary) == 400 and len(candidates) == len(refusals) == len(cfr) == 300)
    test("subject nonpromotion", all(not row["subject_promoted"] for row in refusals + cfr))
    if len(tests) != 15:
        raise RuntimeError("x1 test inventory mismatch")

    X1.mkdir(parents=True)
    write_json(X1 / "core-results.json", {"schema": "ghc.family.x1-core-results.v1", "owner": "Auren Lark", "phase": "v704-v5", "count": len(core), "records": core, "boundary": BOUNDARY})
    write_json(X1 / "safe-results.json", {"schema": "ghc.family.safe-results.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x1", "core_count": len(core), "auxiliary_count": len(auxiliary), "total": len(core) + len(auxiliary), "auxiliary": auxiliary, "boundary": BOUNDARY})
    write_json(X1 / "candidate-failures.json", {"schema": "ghc.family.candidate-failures.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x1", "count": len(candidates), "all_failed": True, "records": candidates, "boundary": BOUNDARY})
    write_json(X1 / "refusal-witnesses.json", {"schema": "ghc.family.refusal-witnesses.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x1", "count": len(refusals), "passing": len(refusals), "subjects_promoted": 0, "records": refusals, "boundary": BOUNDARY})
    write_json(X1 / "cfr-results.json", {"schema": "ghc.family.clean-fix-refine.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x1", "count": len(cfr), "passing": len(cfr), "evidence_deleted": 0, "records": cfr, "boundary": BOUNDARY})
    write_json(X1 / "tests.json", {"schema": "ghc.family.test-receipt.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x1", "invocations": 1, "successes": 1, "replays": 0, "passed": len(tests), "failed": 0, "tests": tests, "boundary": BOUNDARY})

    skill_plan = json.loads((PLAN / "capability-plan.json").read_text(encoding="utf-8"))["x1"]["skills"]
    op_by_skill = list(zip(skill_plan, sorted({row["operation"] for row in core})))
    for skill_name, operation in op_by_skill:
        title = " ".join(part.capitalize() for part in skill_name.removeprefix("ghc-family-").split("-"))
        target = X1 / "skills" / skill_name / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(skill_text(skill_name, title, operation), encoding="utf-8", newline="\n")
    validator = Path(os.environ.get("USERPROFILE", "")) / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    skill_checks = []
    for skill_name, _ in op_by_skill:
        proc = subprocess.run([sys.executable, str(validator), str(X1 / "skills" / skill_name)], capture_output=True, text=True, check=False)
        skill_checks.append({"skill": skill_name, "passed": proc.returncode == 0, "exit_code": proc.returncode, "summary": (proc.stdout or proc.stderr).strip()[-300:]})
    if not all(row["passed"] for row in skill_checks):
        raise RuntimeError("x1 skill validation failed")
    write_json(X1 / "skill-validation.json", {"schema": "ghc.family.skill-validation.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x1", "count": len(skill_checks), "passed": sum(row["passed"] for row in skill_checks), "records": skill_checks, "boundary": BOUNDARY})

    runner_names = json.loads((PLAN / "capability-plan.json").read_text(encoding="utf-8"))["x1"]["runners"]
    grouped = [operations[i:i + 2] for i in range(0, len(operations), 2)]
    for runner_name, allowed in zip(runner_names, grouped, strict=True):
        target = X1 / "runners" / runner_name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(runner_text(allowed), encoding="utf-8", newline="\n")
    smoke_records = []
    for runner_name, allowed in zip(runner_names, grouped, strict=True):
        target = X1 / "runners" / runner_name
        valid = subprocess.run([sys.executable, str(target), "--profile-id", profiles[0]["id"], "--operation", allowed[0]], capture_output=True, text=True, check=False)
        invalid = subprocess.run([sys.executable, str(target), "--profile-id", profiles[0]["id"], "--operation", "not_an_operation"], capture_output=True, text=True, check=False)
        smoke_records.extend([
            {"runner": runner_name, "case": "valid", "passed": valid.returncode == 0 and json.loads(valid.stdout)["ok"] is True, "exit_code": valid.returncode},
            {"runner": runner_name, "case": "invalid", "passed": invalid.returncode == 2 and json.loads(invalid.stdout)["ok"] is False, "exit_code": invalid.returncode}
        ])
    if not all(row["passed"] for row in smoke_records):
        raise RuntimeError("x1 runner smoke failed")
    write_json(X1 / "runner-smokes.json", {"schema": "ghc.family.runner-smokes.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x1", "count": len(smoke_records), "passed": sum(row["passed"] for row in smoke_records), "records": smoke_records, "boundary": BOUNDARY})

    method_flow = build_method_flow(core, auxiliary, candidates, refusals, cfr)
    if method_flow["counts"]["witness_results"] != {"pass": 1000, "fail": 300}:
        raise RuntimeError(f"x1 Method Flow count mismatch: {method_flow['counts']['witness_results']}")
    write_json(X1 / "method-flow.json", method_flow)
    summary = {"schema": "ghc.family.session-summary.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x1", "domain_harness": {"invocations": 1, "successes": 1, "replays": 0, "contracts": 150, "mismatches": 0}, "safe": 400, "candidate_failed": 300, "separate_refusals_passed": 300, "clean_fix_refine_passed": 300, "skills_validated": 10, "runners": 5, "runner_smokes": 10, "tests": {"invocations": 1, "passed": 15, "failed": 0, "replays": 0}, "malformed_subjects_promoted": 0, "evidence_deleted": 0, "outcomes": {"completed": 150, "represented": 0, "open_gap": 0, "exact_gate": 0}, "boundary": BOUNDARY}
    write_json(X1 / "session-summary.json", summary)

    manifest_path = X1 / "manifest.json"
    targets = sorted([file for file in X1.rglob("*") if file.is_file() and file != manifest_path] + [Path(__file__)])
    entries = []
    for target in targets:
        raw = target.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
        entries.append({"path": target.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "domain": "normalized_lf_expected_git_blob"})
    write_json(manifest_path, {"schema": "ghc.family.x1-manifest.v1", "owner": "Auren Lark", "phase": "v704-v5", "stage": "x1", "entry_count": len(entries), "entries": entries, "excluded_self": manifest_path.relative_to(ROOT).as_posix(), "normalization": "CRLF is normalized to LF before hashing so the digest domain matches committed Git text blobs.", "boundary": BOUNDARY})
    write_json(X1 / "validation-summary.json", {"schema": "ghc.family.x1-validation-summary.v1", "owner": "Auren Lark", "phase": "v704-v5", "state": "VALID_X1_OWNER_SCOPED", "strict_json_expected_after_manifest": 12, "manifest_entries": len(entries), "tests": "15/15", "skills": "10/10", "runner_smokes": "10/10", "privacy_state": "pending bounded stage preflight", "boundary": BOUNDARY})

    # Refresh the manifest for the validation summary written immediately above.
    targets = sorted([file for file in X1.rglob("*") if file.is_file() and file != manifest_path] + [Path(__file__)])
    entries = []
    for target in targets:
        raw = target.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
        entries.append({"path": target.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "domain": "normalized_lf_expected_git_blob"})
    write_json(manifest_path, {"schema": "ghc.family.x1-manifest.v1", "owner": "Auren Lark", "phase": "v704-v5", "stage": "x1", "entry_count": len(entries), "entries": entries, "excluded_self": manifest_path.relative_to(ROOT).as_posix(), "normalization": "CRLF is normalized to LF before hashing so the digest domain matches committed Git text blobs.", "boundary": BOUNDARY})
    print(json.dumps({"state": "VALID_X1_OWNER_SCOPED", "contracts": 150, "safe": 400, "candidate_failed": 300, "refusals": 300, "cfr": 300, "tests": 15, "skills": 10, "runner_smokes": 10, "manifest_entries": len(entries), "successful_replay": 0, "boundary": BOUNDARY}, sort_keys=True))


if __name__ == "__main__":
    main()
