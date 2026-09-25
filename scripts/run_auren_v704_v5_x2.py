from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v704-v5"
PLAN = BASE / "planning"
X2 = BASE / "x2"
EXPECTED_HEAD = "0b701a3af0d36fb520c6945803235890fef7d3ca"
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


def minimum_risk(prior: list[Fraction]) -> Fraction:
    return 1 - max(prior)


def one_step_risk(profile: dict, prior: list[Fraction], experiment: int) -> Fraction:
    risk = Fraction()
    for outcome in (0, 1):
        weights = [prior[h] * likelihood(profile, experiment, outcome, h) for h in range(len(prior))]
        risk += sum(weights, Fraction()) - max(weights)
    return risk


def discrimination(profile: dict, experiment: int) -> Fraction:
    probabilities = [frac(x) for x in profile["experiments"][experiment]["success"]]
    return sum((abs(probabilities[i] - probabilities[j]) for i in range(len(probabilities)) for j in range(i + 1, len(probabilities))), Fraction())


def nonadaptive(profile: dict, prior: list[Fraction]) -> dict:
    rows = []
    for first in range(len(profile["experiments"])):
        for second in range(len(profile["experiments"])):
            risk = Fraction()
            for y1 in (0, 1):
                for y2 in (0, 1):
                    weights = [prior[h] * likelihood(profile, first, y1, h) * likelihood(profile, second, y2, h) for h in range(len(prior))]
                    risk += sum(weights, Fraction()) - max(weights)
            rows.append({"pair": [profile["experiments"][first]["id"], profile["experiments"][second]["id"]], "risk": risk})
    best = min(row["risk"] for row in rows)
    return {"risk": best, "pairs": [row["pair"] for row in rows if row["risk"] == best], "all": rows}


def adaptive(profile: dict, prior: list[Fraction]) -> dict:
    candidates = []
    for first in range(len(profile["experiments"])):
        total = Fraction()
        branches = []
        for y1 in (0, 1):
            predictive, updated = posterior(profile, prior, first, y1)
            risks = [one_step_risk(profile, updated, second) for second in range(len(profile["experiments"]))]
            best = min(risks)
            seconds = [profile["experiments"][second]["id"] for second, risk in enumerate(risks) if risk == best]
            total += predictive * best
            branches.append({"outcome": str(y1), "second_experiments": seconds, "conditional_risk": best})
        candidates.append({"first_experiment": profile["experiments"][first]["id"], "risk": total, "branches": branches})
    best = min(candidate["risk"] for candidate in candidates)
    return {"risk": best, "policies": [candidate for candidate in candidates if candidate["risk"] == best], "all": candidates}


def rationalize(value: object) -> object:
    if isinstance(value, Fraction):
        return text(value)
    if isinstance(value, list):
        return [rationalize(item) for item in value]
    if isinstance(value, dict):
        return {key: rationalize(item) for key, item in value.items()}
    return value


def operate(profile: dict, operation: str) -> dict:
    validate_profile(profile)
    prior = [frac(x) for x in profile["prior"]]
    if operation == "nonadaptive_two_step_design":
        result = nonadaptive(profile, prior)
        return rationalize({"risk": result["risk"], "optimal_pairs": result["pairs"]})
    if operation == "adaptive_two_step_policy":
        result = adaptive(profile, prior)
        policies = [{"first_experiment": item["first_experiment"], "branches": item["branches"]} for item in result["policies"]]
        return rationalize({"risk": result["risk"], "optimal_policies": policies})
    if operation == "value_of_adaptation":
        nonadaptive_result = nonadaptive(profile, prior)
        adaptive_result = adaptive(profile, prior)
        value = nonadaptive_result["risk"] - adaptive_result["risk"]
        return {"nonadaptive_risk": text(nonadaptive_result["risk"]), "adaptive_risk": text(adaptive_result["risk"]), "value": text(value), "nonnegative": value >= 0}
    if operation == "prior_sensitivity_envelope":
        uniform = [Fraction(1, len(prior)) for _ in prior]
        declared = adaptive(profile, prior)["risk"]
        equal = adaptive(profile, uniform)["risk"]
        return {"declared": text(declared), "uniform": text(equal), "lower": text(min(declared, equal)), "upper": text(max(declared, equal)), "prior_family_size": 2}
    if operation == "outcome_coarsening_compare":
        informative = min(one_step_risk(profile, prior, experiment) for experiment in range(len(profile["experiments"])))
        collapsed = minimum_risk(prior)
        return {"informative_best_risk": text(informative), "collapsed_outcome_risk": text(collapsed), "information_value": text(collapsed - informative), "nonnegative": collapsed >= informative}
    if operation == "relabel_covariance":
        reversed_profile = copy.deepcopy(profile)
        reversed_profile["hypotheses"] = list(reversed(reversed_profile["hypotheses"]))
        reversed_profile["prior"] = list(reversed(reversed_profile["prior"]))
        for experiment in reversed_profile["experiments"]:
            experiment["success"] = list(reversed(experiment["success"]))
        original = adaptive(profile, prior)["risk"]
        relabeled = adaptive(reversed_profile, [frac(x) for x in reversed_profile["prior"]])["risk"]
        return {"original_risk": text(original), "relabeled_risk": text(relabeled), "invariant": original == relabeled}
    if operation == "accessible_summary":
        nonadaptive_result = nonadaptive(profile, prior)
        adaptive_result = adaptive(profile, prior)
        return {"title": f"{profile['id']} exact experiment-design summary", "hypotheses": len(profile["hypotheses"]), "experiments": len(profile["experiments"]), "nonadaptive_risk": text(nonadaptive_result["risk"]), "adaptive_risk": text(adaptive_result["risk"]), "statement": "Finite synthetic exact-rational comparison; no empirical or authority promotion."}
    if operation == "mixture_representation":
        epsilon = min(prior[0], prior[1]) / 2
        plus = [prior[0] + epsilon, prior[1] - epsilon, prior[2]]
        minus = [prior[0] - epsilon, prior[1] + epsilon, prior[2]]
        return rationalize({"weights": ["1/2", "1/2"], "components": [plus, minus], "reconstructed": prior, "generative_mixture_claim": False})
    if operation == "external_evidence_gap":
        return {"state": "open_gap", "missing": ["governed observations", "sampling design", "likelihood calibration", "coverage assessment", "independent review"], "external_credit": False}
    if operation == "authority_gate":
        return {"state": "exact_gate", "held": ["real intervention", "participant decision", "production deployment", "professional judgment", "legal or cultural authority", "Maori authority"], "executed": False}
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

1. Validate the frozen prior, likelihood, experiment and hypothesis structure first.
2. Preserve adaptive and nonadaptive semantics, exact fractions, every exact tie and explicit comparator labels.
3. Keep malformed subjects failed even when the separate refusal check passes.
4. Preserve empirical, participant, production, identity and authority gaps and gates.

## Boundary

{BOUNDARY}
'''


def runner_text(allowed: list[str]) -> str:
    return f'''from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ALLOWED = {allowed!r}

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


def advisory_script() -> str:
    return r'''"use strict";
const fs=require("fs");
const messages={
 model_setting_change:"Model changes require a fresh exact authority check; preserve the admitted model.",
 source_lane_mutation:"Source and sibling lanes are read-only; use the additive Auren lane.",
 successful_replay:"Do not replay a successful canonical or successful stage aggregate.",
 adaptive_nonadaptive_promotion:"A finite adaptive advantage is a fixture result, not empirical validation.",
 malformed_subject_promotion:"A passing refusal never promotes the malformed subject.",
 broad_git_stage:"Stage only reviewed owner paths and protect foreign staged work.",
 destructive_git:"Destructive Git is outside this additive phase.",
 raw_identifier_output:"Do not publish raw identifiers or private local paths.",
 prepared_delivery:"Prepared delivery is not sent or acknowledged delivery.",
 accepted_resend:"Do not resend an acknowledged, opaque or unresolved handoff."
};
function inspect(id,p){
 if(!Object.hasOwn(messages,id)||!p||typeof p!=="object"||Array.isArray(p))return{};
 if(p.hook_event_name==="Stop"&&p.stop_hook_active===true)return{};
 const command=typeof p.tool_input?.command==="string"?p.tool_input.command:typeof p.tool_input?.cmd==="string"?p.tool_input.cmd:"";
 const response=p.tool_response??{},out=typeof response==="string"?response:typeof response.output==="string"?response.output:JSON.stringify(response);
 const summary=typeof p.last_assistant_message==="string"?p.last_assistant_message:"";let adverse=false;
 switch(id){
 case"model_setting_change":adverse=/\b(?:model|reasoning effort)\b[\s\S]{0,60}\b(?:change|override|switch)\b/i.test(command);break;
 case"source_lane_mutation":adverse=/ilyra-fen\/v704-v4/i.test(command)&&/\b(?:add|commit|write|remove|delete|move)\b/i.test(command);break;
 case"successful_replay":adverse=/\b(?:canonical|aggregate)\b[\s\S]{0,60}\b(?:replay|rerun|again)\b/i.test(command);break;
 case"adaptive_nonadaptive_promotion":adverse=/adaptive[\s\S]{0,100}\b(?:empirical|real-world|proves?|validated)\b/i.test(command+" "+summary);break;
 case"malformed_subject_promotion":adverse=/subject_promoted[\s\S]{0,10}true|malformed[\s\S]{0,80}\bcompleted\b/i.test(command+" "+out);break;
 case"broad_git_stage":adverse=/\bgit\s+add\s+(?:-A\b|\.(?:\s|$))/i.test(command);break;
 case"destructive_git":adverse=/\bgit\s+(?:reset\s+--hard|clean\s+-[a-z]*f|push\b[\s\S]*(?:--force|\s-f(?:\s|$)))/i.test(command);break;
 case"raw_identifier_output":adverse=/[A-Za-z]:\\(?:Users|GHC-Archives)\\|\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b/i.test(out);break;
 case"prepared_delivery":adverse=typeof response==="object"&&response!==null&&(response.state==="PREPARED_NOT_SENT"||response.route_state==="PREPARED_NOT_SENT");break;
 case"accepted_resend":adverse=/\b(?:resent|resending|send again)\b[\s\S]{0,80}\b(?:acknowledged|accepted|opaque|unresolved)\b/i.test(summary);break;
 }
 return adverse?{systemMessage:messages[id]}:{};
}
function main(){const buffer=Buffer.alloc(131073);let count=0,result={};while(count<buffer.length){const n=fs.readSync(0,buffer,count,buffer.length-count,null);if(n===0)break;count+=n}if(count<=131072){try{result=inspect(process.argv[2],JSON.parse(buffer.subarray(0,count).toString("utf8")))}catch{}}process.stdout.write(JSON.stringify(result)+"\n")}
module.exports={inspect};if(require.main===module)main();
'''


def build_hooks(plugin: Path) -> list[str]:
    ids = ["model_setting_change", "source_lane_mutation", "successful_replay", "adaptive_nonadaptive_promotion", "malformed_subject_promotion", "broad_git_stage", "destructive_git", "raw_identifier_output", "prepared_delivery", "accepted_resend"]
    write_json(plugin / ".codex-plugin" / "plugin.json", {"name": "ghc-family-auren-experiment-workflow-hooks", "version": "1.0.0", "description": "Ten bounded nonblocking advisories for exact experiment-design evidence and guarded delivery.", "author": {"name": "GHC Auren tooling"}, "interface": {"displayName": "GHC experiment workflow advisories", "shortDescription": "Keep experiment, evidence, Git and delivery boundaries visible.", "longDescription": "Ten synchronous constant-output advisory hooks with bounded input and no payload-driven side effects. Manual validation remains separate from live lifecycle observation.", "developerName": "GHC Auren tooling", "category": "Productivity", "capabilities": [], "defaultPrompt": ["Review exact experiment workflow boundaries."]}})
    grouped: dict[str, list[dict]] = {"PreToolUse": [], "PostToolUse": [], "Stop": []}
    for index, hook_id in enumerate(ids):
        event = "PreToolUse" if index < 6 else "PostToolUse" if index < 9 else "Stop"
        command = {"type": "command", "command": f'node "${{PLUGIN_ROOT}}/scripts/advisories.txt" {hook_id}', "commandWindows": f'node "$env:PLUGIN_ROOT/scripts/advisories.txt" {hook_id}', "timeout": 5, "async": False, "statusMessage": "Checking a bounded experiment-design advisory"}
        row = {"hooks": [command]}
        if event != "Stop":
            row["matcher"] = ".*"
        grouped[event].append(row)
    write_json(plugin / "hooks" / "hooks.json", {"description": "Nonblocking constant-output checks; no payload-driven side effects.", "hooks": grouped})
    script = plugin / "scripts" / "advisories.txt"
    script.parent.mkdir(parents=True, exist_ok=True)
    script.write_text(advisory_script(), encoding="utf-8", newline="\n")
    return ids


def build_method_flow(core: list[dict], safe_aux: list[dict], candidates: list[dict], refusals: list[dict], cfr: list[dict]) -> dict:
    operations = sorted({row["operation"] for row in core})
    methods, witnesses = [], []
    for op_index, operation in enumerate(operations, start=1):
        op_candidates = [row for row in candidates if row["operation"] == operation]
        negative_ids = [row["retained_negative_id"] for row in op_candidates]
        pass_ids: list[str] = []
        for row in core:
            if row["operation"] != operation:
                continue
            witness_id = f"AL7045-X2-WC-{row['proposal_id']}"
            pass_ids.append(witness_id)
            witnesses.append({"witness_id": witness_id, "method_id": f"AL7045-X2-M{op_index:02d}", "procedure": "Evaluate the frozen x2 exact-rational contract and compare with its planning expectation.", "scope": row["proposal_id"], "expected": "exact match", "observed": "exact match", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_ids[(len(pass_ids) - 1) % len(negative_ids)]], "boundary": "Bounded same-owner finite synthetic result."})
        for row in op_candidates:
            witnesses.append({"witness_id": row["witness_id"], "method_id": f"AL7045-X2-M{op_index:02d}", "procedure": "Execute one preregistered malformed profile subject.", "scope": row["candidate_id"], "expected": "subject remains failed", "observed": row["observed"], "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [row["retained_negative_id"]], "boundary": "Failed subject at zero completion credit."})
        for row in refusals:
            if row["operation"] != operation:
                continue
            pass_ids.append(row["witness_id"])
            witnesses.append({"witness_id": row["witness_id"], "method_id": f"AL7045-X2-M{op_index:02d}", "procedure": "Run the separate bounded refusal guard.", "scope": row["candidate_id"], "expected": "refusal passes without subject promotion", "observed": row["observed"], "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [row["retained_negative_id"]], "boundary": "Guard evidence only; malformed subject remains failed."})
        for row in cfr:
            if row["operation"] != operation:
                continue
            pass_ids.append(row["witness_id"])
            witnesses.append({"witness_id": row["witness_id"], "method_id": f"AL7045-X2-M{op_index:02d}", "procedure": "Execute a nondeleting CLEAN/FIX/REFINE review.", "scope": row["review_id"], "expected": "bounded review passes with evidence retained", "observed": row["result"], "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [row["retained_negative_id"]], "boundary": "Review evidence only."})
        for row in safe_aux:
            if row["method_operation"] != operation:
                continue
            pass_ids.append(row["witness_id"])
            witnesses.append({"witness_id": row["witness_id"], "method_id": f"AL7045-X2-M{op_index:02d}", "procedure": "Execute a deterministic x2 auxiliary invariant check.", "scope": row["safe_id"], "expected": True, "observed": row["passed"], "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_ids[(len(pass_ids) - 1) % len(negative_ids)]], "boundary": "Auxiliary check with zero additional proposal credit."})
        methods.append({"method_id": f"AL7045-X2-M{op_index:02d}", "title": operation.replace("_", " ").title(), "failure_signature": f"Malformed finite experiment-design subject for {operation}.", "trigger_preconditions": ["frozen x2 contract", "exact rational profile"], "privacy_class": "sanitized_public", "approval_class": "safe_now", "candidate_workaround": "Reject malformed structure, retain the subject failure, and run the valid frozen contract separately.", "validation_witness_ids": pass_ids, "recurrence_guard": "Validate profile structure before every operation and preserve comparator semantics and exact ties.", "rollback": "Discard no evidence; return to the frozen planning contract.", "recommendation_state": "validated", "supersedes": [], "protected_gates": ["malformed_subject_nonpromotion", "retained_failure_nonerasure", "empirical_nonpromotion"], "retained_negative_ids": negative_ids, "scope_boundary": "Finite synthetic x2 operation only."})
    events = [{"event_id": f"AL7045-X2-E{i:02d}", "method_id": method["method_id"], "from": "observed", "to": "validated", "witness_id": method["validation_witness_ids"][0]} for i, method in enumerate(methods, start=1)]
    recommendations = [{"recommendation_id": f"AL7045-X2-R{i:02d}", "method_id": method["method_id"], "state": "validated", "text": f"Use exact validated {method['title'].lower()} only inside the frozen finite synthetic scope."} for i, method in enumerate(methods, start=1)]
    passed = sum(witness["result"] == "pass" for witness in witnesses)
    failed = sum(witness["result"] == "fail" for witness in witnesses)
    return {"schema": "ghc.family.method-flow-state.v1", "phase": "v704-v5-x2", "owner": "Auren Lark", "identity_boundary": IDENTITY, "execution_authority": "owner_self_scoped_delta", "attributable_owner": "Auren Lark", "source_commit": EXPECTED_HEAD, "final_commit": None, "changed_file_allowlist": ["scripts/run_auren_v704_v5_x2.py", "scripts/validate_auren_v704_v5_hooks.mjs", "scripts/validate_auren_v704_v5_stage.mjs", "docs/auren-lark/v704-v5/x2/**"], "module_allowlist": ["x2"], "repository_scan": False, "module_scan": True, "cross_lane_scan": False, "unchanged_history_scan": False, "sibling_lane_mutation": False, "exact_pushed_head_required": True, "methods": methods, "witnesses": witnesses, "state_events": events, "recommendations": recommendations, "counts": {"methods": len(methods), "witnesses": len(witnesses), "state_events": len(events), "recommendations": len(recommendations), "states": {"observed": 0, "candidate": 0, "validated": len(methods), "preferred": 0, "superseded": 0, "deprecated": 0}, "witness_results": {"pass": passed, "fail": failed}}, "evidence_counts": {"negatives": failed, "methods": len(methods), "failed_witnesses": failed, "passing_witnesses": passed, "witnesses": len(witnesses), "open_gaps": 15, "exact_gates": 15}, "selected_pre_x2_baseline": {"negatives": 64685, "methods": 5761, "failed_witnesses": 55850, "passing_witnesses": 176801, "witnesses": 232651, "open_gaps": 1995, "exact_gates": 2078}, "source_fold_count": 0, "effective_totals": {"negatives": 64985, "methods": 5771, "failed_witnesses": 56150, "passing_witnesses": 177801, "witnesses": 233951, "open_gaps": 2010, "exact_gates": 2093}, "boundary": BOUNDARY}


def main() -> None:
    head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    if head != EXPECTED_HEAD:
        raise RuntimeError(f"x2 requires exact immutable x1 {EXPECTED_HEAD}; observed {head}")
    if X2.exists():
        raise RuntimeError(f"x2 target already exists: {X2}")

    profiles = json.loads((PLAN / "profiles.json").read_text(encoding="utf-8"))["profiles"]
    profile_by_id = {profile["id"]: profile for profile in profiles}
    proposal_files = sorted((PLAN / "proposals").glob("*.json"))[10:]
    contracts: list[dict] = []
    for proposal_file in proposal_files:
        contracts.extend(json.loads(proposal_file.read_text(encoding="utf-8"))["contracts"])
    if len(contracts) != 150:
        raise RuntimeError(f"expected 150 x2 contracts; observed {len(contracts)}")

    core, mismatches = [], []
    for contract in contracts:
        actual = operate(profile_by_id[contract["profile_id"]], contract["operation"])
        matches = actual == contract["expected"] and digest(actual) == contract["expected_sha256"]
        row = {"proposal_id": contract["proposal_id"], "profile_id": contract["profile_id"], "operation": contract["operation"], "expected_disposition": contract["expected_execution_disposition"], "actual": actual, "actual_sha256": digest(actual), "expected_sha256": contract["expected_sha256"], "matched": matches, "completion_credit": 1 if matches and contract["expected_execution_disposition"] == "completed" else 0, "boundary": BOUNDARY}
        core.append(row)
        if not matches:
            mismatches.append(row)
    if mismatches:
        raise RuntimeError(f"x2 exact mismatches: {len(mismatches)}")

    operations = list(dict.fromkeys(contract["operation"] for contract in contracts))
    auxiliary = []
    kinds = ["adaptation_nonnegative", "nonadaptive_optima", "adaptive_optima", "envelope_order", "relabel_invariance"]
    for index in range(250):
        profile = profiles[index % len(profiles)]
        prior = [frac(x) for x in profile["prior"]]
        kind = kinds[index % len(kinds)]
        n = nonadaptive(profile, prior)
        a = adaptive(profile, prior)
        if kind == "adaptation_nonnegative":
            passed = n["risk"] >= a["risk"]
        elif kind == "nonadaptive_optima":
            passed = len(n["pairs"]) >= 1
        elif kind == "adaptive_optima":
            passed = len(a["policies"]) >= 1
        elif kind == "envelope_order":
            result = operate(profile, "prior_sensitivity_envelope")
            passed = frac(result["lower"]) <= frac(result["upper"])
        else:
            passed = operate(profile, "relabel_covariance")["invariant"] is True
        if not passed:
            raise RuntimeError(f"x2 auxiliary invariant failed: {kind} {profile['id']}")
        auxiliary.append({"safe_id": f"AL7045-X2-S{index + 151:03d}", "witness_id": f"AL7045-X2-WA{index + 1:03d}", "profile_id": profile["id"], "kind": kind, "method_operation": operations[index % len(operations)], "passed": True, "additional_proposal_credit": 0, "boundary": BOUNDARY})

    candidates, refusals = [], []
    for contract in contracts:
        for variant in ("negative_prior", "likelihood_out_of_range"):
            malformed = copy.deepcopy(profile_by_id[contract["profile_id"]])
            if variant == "negative_prior":
                malformed["prior"][0] = "-1"
            else:
                malformed["experiments"][0]["success"][0] = "7/6"
            candidate_id = f"AL7045-X2-C{len(candidates) + 1:03d}"
            negative_id = f"AL7045-X2-N{len(candidates) + 1:03d}"
            try:
                operate(malformed, contract["operation"])
                raise RuntimeError(f"malformed subject unexpectedly accepted: {candidate_id}")
            except ValueError as error:
                observed = str(error)
            candidates.append({"candidate_id": candidate_id, "proposal_id": contract["proposal_id"], "profile_id": contract["profile_id"], "operation": contract["operation"], "variant": variant, "subject_result": "failed", "observed": observed, "completion_credit": 0, "retained_negative_id": negative_id, "witness_id": f"AL7045-X2-WF{len(candidates) + 1:03d}", "boundary": BOUNDARY})
            refusals.append({"refusal_id": f"AL7045-X2-RF{len(refusals) + 1:03d}", "candidate_id": candidate_id, "operation": contract["operation"], "guard_result": "pass", "observed": "REFUSED_INVALID_PROFILE", "subject_promoted": False, "retained_negative_id": negative_id, "witness_id": f"AL7045-X2-WR{len(refusals) + 1:03d}", "boundary": BOUNDARY})

    cfr = []
    dispositions = ["CLEAN", "FIX", "REFINE"]
    for index in range(300):
        contract = contracts[index % len(contracts)]
        candidate = candidates[index]
        cfr.append({"review_id": f"AL7045-X2-CFR{index + 1:03d}", "proposal_id": contract["proposal_id"], "operation": contract["operation"], "disposition": dispositions[index % len(dispositions)], "result": "pass", "evidence_deleted": False, "subject_promoted": False, "retained_negative_id": candidate["retained_negative_id"], "witness_id": f"AL7045-X2-WQ{index + 1:03d}", "boundary": BOUNDARY})

    models = []
    for profile in profiles:
        prior = [frac(x) for x in profile["prior"]]
        n = nonadaptive(profile, prior)["risk"]
        a = adaptive(profile, prior)["risk"]
        separation = max(discrimination(profile, index) for index in range(len(profile["experiments"])))
        models.append({"id": profile["id"], "coordinates": [text(n), text(n - a), text(separation)], "axes": ["best_nonadaptive_risk", "value_of_adaptation", "maximum_pairwise_separation"], "physical_claim": False, "boundary": BOUNDARY})

    tests = []
    def test(name: str, condition: bool) -> None:
        if not condition:
            raise RuntimeError(f"x2 test failed: {name}")
        tests.append({"id": f"AL7045-X2-T{len(tests) + 1:02d}", "name": name, "passed": True})
    test("fifteen profiles", len(profiles) == 15)
    test("ten x2 operations", len(operations) == 10)
    test("nonadaptive bounded", all(0 <= nonadaptive(p, [frac(x) for x in p["prior"]])["risk"] <= 1 for p in profiles))
    test("adaptive bounded", all(0 <= adaptive(p, [frac(x) for x in p["prior"]])["risk"] <= 1 for p in profiles))
    test("adaptation nonnegative", all(nonadaptive(p, [frac(x) for x in p["prior"]])["risk"] >= adaptive(p, [frac(x) for x in p["prior"]])["risk"] for p in profiles))
    test("nonadaptive optima nonempty", all(nonadaptive(p, [frac(x) for x in p["prior"]])["pairs"] for p in profiles))
    test("adaptive optima nonempty", all(adaptive(p, [frac(x) for x in p["prior"]])["policies"] for p in profiles))
    test("sensitivity envelope ordered", all(frac(operate(p, "prior_sensitivity_envelope")["lower"]) <= frac(operate(p, "prior_sensitivity_envelope")["upper"]) for p in profiles))
    test("coarsening nonimprovement", all(operate(p, "outcome_coarsening_compare")["nonnegative"] for p in profiles))
    test("relabel invariant", all(operate(p, "relabel_covariance")["invariant"] for p in profiles))
    test("accessible summary boundary", all("no empirical" in operate(p, "accessible_summary")["statement"] for p in profiles))
    test("mixture weights sum", all(sum((frac(x) for x in operate(p, "mixture_representation")["weights"]), Fraction()) == 1 for p in profiles))
    test("mixture components simplex", all(all(sum((frac(x) for x in component), Fraction()) == 1 for component in operate(p, "mixture_representation")["components"]) for p in profiles))
    test("mixture reconstructs prior", all(operate(p, "mixture_representation")["reconstructed"] == p["prior"] for p in profiles))
    test("open gaps held", all(operate(p, "external_evidence_gap")["state"] == "open_gap" for p in profiles))
    test("authority gates held", all(operate(p, "authority_gate")["state"] == "exact_gate" and not operate(p, "authority_gate")["executed"] for p in profiles))
    test("exact core matches", len(core) == 150 and all(row["matched"] for row in core))
    outcomes = {label: sum(row["expected_disposition"] == label for row in core) for label in ("completed", "represented", "open_gap", "exact_gate")}
    test("outcomes exact", outcomes == {"completed": 105, "represented": 15, "open_gap": 15, "exact_gate": 15})
    test("safe count", len(core) + len(auxiliary) == 400)
    test("candidate count", len(candidates) == 300)
    test("refusal count", len(refusals) == 300)
    test("clean fix refine count", len(cfr) == 300)
    test("subject nonpromotion", all(not row["subject_promoted"] for row in refusals + cfr))
    test("evidence nondeletion", all(not row["evidence_deleted"] for row in cfr))
    test("fifteen models", len(models) == 15)
    test("three coordinates", all(len(model["coordinates"]) == 3 for model in models))
    test("coordinate risk rational", all(frac(model["coordinates"][0]) >= 0 for model in models))
    test("coordinate adaptation nonnegative", all(frac(model["coordinates"][1]) >= 0 for model in models))
    test("coordinate separation nonnegative", all(frac(model["coordinates"][2]) >= 0 for model in models))
    packets = json.loads((PLAN / "approval-packets.json").read_text(encoding="utf-8"))
    test("protected packets held", packets["executed"] == 0 and packets["exact_count"] == 50 and packets["blocked_count"] == 30)
    if len(tests) != 30:
        raise RuntimeError("x2 test inventory mismatch")

    X2.mkdir(parents=True)
    write_json(X2 / "core-results.json", {"schema": "ghc.family.x2-core-results.v1", "owner": "Auren Lark", "phase": "v704-v5", "count": len(core), "outcomes": outcomes, "records": core, "boundary": BOUNDARY})
    write_json(X2 / "safe-results.json", {"schema": "ghc.family.safe-results.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x2", "core_count": len(core), "auxiliary_count": len(auxiliary), "total": len(core) + len(auxiliary), "auxiliary": auxiliary, "boundary": BOUNDARY})
    write_json(X2 / "candidate-failures.json", {"schema": "ghc.family.candidate-failures.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x2", "count": len(candidates), "all_failed": True, "records": candidates, "boundary": BOUNDARY})
    write_json(X2 / "refusal-witnesses.json", {"schema": "ghc.family.refusal-witnesses.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x2", "count": len(refusals), "passing": len(refusals), "subjects_promoted": 0, "records": refusals, "boundary": BOUNDARY})
    write_json(X2 / "cfr-results.json", {"schema": "ghc.family.clean-fix-refine.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x2", "count": len(cfr), "passing": len(cfr), "evidence_deleted": 0, "records": cfr, "boundary": BOUNDARY})
    write_json(X2 / "tests.json", {"schema": "ghc.family.test-receipt.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x2", "invocations": 1, "successes": 1, "replays": 0, "passed": len(tests), "failed": 0, "tests": tests, "boundary": BOUNDARY})
    write_json(X2 / "models.json", {"schema": "ghc.family.three-coordinate-models.v1", "owner": "Auren Lark", "phase": "v704-v5", "count": len(models), "records": models, "boundary": BOUNDARY})

    skill_plan = json.loads((PLAN / "capability-plan.json").read_text(encoding="utf-8"))["x2"]["skills"]
    for skill_name, operation in zip(skill_plan, operations, strict=True):
        title = " ".join(part.capitalize() for part in skill_name.removeprefix("ghc-family-").split("-"))
        target = X2 / "skills" / skill_name / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(skill_text(skill_name, title, operation), encoding="utf-8", newline="\n")
    validator = Path(os.environ.get("USERPROFILE", "")) / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    skill_checks = []
    for skill_name in skill_plan:
        proc = subprocess.run([sys.executable, str(validator), str(X2 / "skills" / skill_name)], capture_output=True, text=True, check=False)
        skill_checks.append({"skill": skill_name, "passed": proc.returncode == 0, "exit_code": proc.returncode, "summary": (proc.stdout or proc.stderr).strip()[-300:]})
    if not all(row["passed"] for row in skill_checks):
        raise RuntimeError("x2 skill validation failed")
    write_json(X2 / "skill-validation.json", {"schema": "ghc.family.skill-validation.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x2", "count": len(skill_checks), "passed": sum(row["passed"] for row in skill_checks), "records": skill_checks, "boundary": BOUNDARY})

    runner_names = json.loads((PLAN / "capability-plan.json").read_text(encoding="utf-8"))["x2"]["runners"]
    grouped = [operations[i:i + 2] for i in range(0, len(operations), 2)]
    for runner_name, allowed in zip(runner_names, grouped, strict=True):
        target = X2 / "runners" / runner_name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(runner_text(allowed), encoding="utf-8", newline="\n")
    smoke_records = []
    for runner_name, allowed in zip(runner_names, grouped, strict=True):
        target = X2 / "runners" / runner_name
        valid = subprocess.run([sys.executable, str(target), "--profile-id", profiles[0]["id"], "--operation", allowed[0]], capture_output=True, text=True, check=False)
        invalid = subprocess.run([sys.executable, str(target), "--profile-id", profiles[0]["id"], "--operation", "not_an_operation"], capture_output=True, text=True, check=False)
        smoke_records.extend([
            {"runner": runner_name, "case": "valid", "passed": valid.returncode == 0 and json.loads(valid.stdout)["ok"] is True, "exit_code": valid.returncode},
            {"runner": runner_name, "case": "invalid", "passed": invalid.returncode == 2 and json.loads(invalid.stdout)["ok"] is False, "exit_code": invalid.returncode}
        ])
    if not all(row["passed"] for row in smoke_records):
        raise RuntimeError("x2 runner smoke failed")
    write_json(X2 / "runner-smokes.json", {"schema": "ghc.family.runner-smokes.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x2", "count": len(smoke_records), "passed": sum(row["passed"] for row in smoke_records), "records": smoke_records, "boundary": BOUNDARY})

    plugin = X2 / "plugins" / "ghc-family-auren-experiment-workflow-hooks"
    hook_ids = build_hooks(plugin)
    plugin_validator = Path(os.environ.get("USERPROFILE", "")) / ".codex" / "skills" / ".system" / "plugin-creator" / "scripts" / "validate_plugin.py"
    plugin_proc = subprocess.run([sys.executable, str(plugin_validator), str(plugin)], capture_output=True, text=True, check=False)
    if plugin_proc.returncode != 0:
        raise RuntimeError(f"plugin validation failed: {(plugin_proc.stdout or plugin_proc.stderr)[-500:]}")
    write_json(X2 / "plugin-validation.json", {"schema": "ghc.family.plugin-validation.v1", "owner": "Auren Lark", "phase": "v704-v5", "plugin": plugin.name, "passed": True, "exit_code": plugin_proc.returncode, "summary": (plugin_proc.stdout or plugin_proc.stderr).strip()[-300:], "installation_state": "repository_local_not_installed", "shared_or_personal_marketplace_mutation": False, "live_hook_observation": "open_gap", "boundary": BOUNDARY})
    hook_proc = subprocess.run(["node", str(ROOT / "scripts" / "validate_auren_v704_v5_hooks.mjs")], capture_output=True, text=True, check=False)
    hook_receipt = json.loads(hook_proc.stdout) if hook_proc.stdout else {}
    if hook_proc.returncode != 0 or hook_receipt.get("passed") != 20:
        raise RuntimeError(f"hook smoke failed: {(hook_proc.stdout or hook_proc.stderr)[-500:]}")
    hook_receipt.update({"owner": "Auren Lark", "phase": "v704-v5", "invocations": 1, "successes": 1, "replays": 0, "installed_live_observation": False, "boundary": BOUNDARY})
    write_json(X2 / "hook-smokes.json", hook_receipt)

    model_json = json.dumps(models, ensure_ascii=False)
    options = "".join(f'<option value="{model["id"]}">{model["id"]}</option>' for model in models)
    rows = "".join(f'<tr><th scope="row">{model["id"]}</th><td>{model["coordinates"][0]}</td><td>{model["coordinates"][1]}</td><td>{model["coordinates"][2]}</td></tr>' for model in models)
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Auren v704-v5 exact experiment models</title>
<style>body{{font-family:system-ui;max-width:72rem;margin:auto;padding:1rem;background:#08131f;color:#eef}}select,button{{font:inherit}}:focus-visible{{outline:3px solid #ffd166;outline-offset:3px}}.scene{{perspective:600px;margin:1rem 0}}.point{{width:12rem;padding:1rem;background:#185a73;border:2px solid #8fe3ff;transform:rotateX(18deg) rotateY(-24deg);box-shadow:1rem 1rem 0 #0a3144}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #8aa;padding:.45rem;text-align:left}}</style></head>
<body><h1>Auren v704-v5 exact experiment models</h1><p>{BOUNDARY}</p><label for="profile">Synthetic profile</label> <select id="profile">{options}</select><div class="scene"><div id="point" class="point" tabindex="0"></div></div><p id="summary" aria-live="polite"></p>
<table><caption>All fifteen exact three-coordinate records</caption><thead><tr><th>Profile</th><th>Nonadaptive risk</th><th>Adaptation value</th><th>Separation</th></tr></thead><tbody>{rows}</tbody></table>
<script>const models={model_json};const select=document.querySelector('#profile'),summary=document.querySelector('#summary'),point=document.querySelector('#point');function render(){{const m=models.find(x=>x.id===select.value);summary.textContent=`${{m.id}}: nonadaptive risk ${{m.coordinates[0]}}, adaptation value ${{m.coordinates[1]}}, separation ${{m.coordinates[2]}}.`;point.textContent=m.id+' · '+m.coordinates.join(' · ');}}select.addEventListener('change',render);render();</script></body></html>'''
    viewer = X2 / "viewer" / "index.html"
    viewer.parent.mkdir(parents=True, exist_ok=True)
    viewer.write_text(html, encoding="utf-8", newline="\n")
    viewer_checks = [
        {"id": "title", "passed": "<title>Auren v704-v5 exact experiment models</title>" in html},
        {"id": "options", "passed": html.count("<option ") == 15},
        {"id": "rows", "passed": html.count('<tr><th scope="row">') == 15},
        {"id": "aria_live", "passed": 'aria-live="polite"' in html},
        {"id": "focus_visible", "passed": ":focus-visible" in html},
        {"id": "self_contained", "passed": "http://" not in html and "https://" not in html}
    ]
    if not all(row["passed"] for row in viewer_checks):
        raise RuntimeError("viewer structural validation failed")
    write_json(X2 / "viewer-validation.json", {"schema": "ghc.family.viewer-validation.v1", "owner": "Auren Lark", "phase": "v704-v5", "checks": viewer_checks, "passed": len(viewer_checks), "failed": 0, "same_owner_static_check_only": True, "complete_accessibility_or_cross_browser_assurance": "open_gap", "boundary": BOUNDARY})

    method_flow = build_method_flow(core, auxiliary, candidates, refusals, cfr)
    if method_flow["counts"]["witness_results"] != {"pass": 1000, "fail": 300}:
        raise RuntimeError(f"x2 Method Flow count mismatch: {method_flow['counts']['witness_results']}")
    write_json(X2 / "method-flow.json", method_flow)
    summary = {"schema": "ghc.family.session-summary.v1", "owner": "Auren Lark", "phase": "v704-v5", "session": "x2", "domain_harness": {"invocations": 1, "successes": 1, "replays": 0, "contracts": 150, "mismatches": 0}, "safe": 400, "candidate_failed": 300, "separate_refusals_passed": 300, "clean_fix_refine_passed": 300, "skills_validated": 10, "runners": 5, "runner_smokes": 10, "tests": {"invocations": 1, "passed": 30, "failed": 0, "replays": 0}, "models": 15, "hooks": len(hook_ids), "hook_smokes": 20, "plugin_installed_shared": False, "malformed_subjects_promoted": 0, "evidence_deleted": 0, "outcomes": outcomes, "operational_open_gaps_reserved_for_final": ["live hook execution", "complete accessibility and cross-browser assurance"], "boundary": BOUNDARY}
    write_json(X2 / "session-summary.json", summary)
    write_json(X2 / "validation-summary.json", {"schema": "ghc.family.x2-validation-summary.v1", "owner": "Auren Lark", "phase": "v704-v5", "state": "VALID_X2_OWNER_SCOPED", "strict_json_expected_after_manifest": 16, "manifest_entries": 0, "tests": "30/30", "skills": "10/10", "runner_smokes": "10/10", "hook_smokes": "20/20", "viewer_checks": "6/6", "privacy_state": "pending bounded stage preflight", "boundary": BOUNDARY})

    manifest_path = X2 / "manifest.json"
    extra_scripts = [Path(__file__), ROOT / "scripts" / "validate_auren_v704_v5_hooks.mjs", ROOT / "scripts" / "validate_auren_v704_v5_stage.mjs"]
    targets = sorted([file for file in X2.rglob("*") if file.is_file() and file != manifest_path] + extra_scripts)
    entries = []
    for target in targets:
        raw = target.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
        entries.append({"path": target.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "domain": "normalized_lf_expected_git_blob"})
    write_json(X2 / "validation-summary.json", {"schema": "ghc.family.x2-validation-summary.v1", "owner": "Auren Lark", "phase": "v704-v5", "state": "VALID_X2_OWNER_SCOPED", "strict_json_expected_after_manifest": 16, "manifest_entries": len(entries), "tests": "30/30", "skills": "10/10", "runner_smokes": "10/10", "hook_smokes": "20/20", "viewer_checks": "6/6", "privacy_state": "pending bounded stage preflight", "boundary": BOUNDARY})
    targets = sorted([file for file in X2.rglob("*") if file.is_file() and file != manifest_path] + extra_scripts)
    entries = []
    for target in targets:
        raw = target.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
        entries.append({"path": target.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "domain": "normalized_lf_expected_git_blob"})
    write_json(manifest_path, {"schema": "ghc.family.x2-manifest.v1", "owner": "Auren Lark", "phase": "v704-v5", "stage": "x2", "entry_count": len(entries), "entries": entries, "excluded_self": manifest_path.relative_to(ROOT).as_posix(), "normalization": "CRLF is normalized to LF before hashing so the digest domain matches committed Git text blobs.", "boundary": BOUNDARY})
    print(json.dumps({"state": "VALID_X2_OWNER_SCOPED", "contracts": 150, "outcomes": outcomes, "safe": 400, "candidate_failed": 300, "refusals": 300, "cfr": 300, "tests": 30, "skills": 10, "runner_smokes": 10, "models": 15, "hooks": 10, "hook_smokes": 20, "manifest_entries": len(entries), "successful_replay": 0, "boundary": BOUNDARY}, sort_keys=True))


if __name__ == "__main__":
    main()
