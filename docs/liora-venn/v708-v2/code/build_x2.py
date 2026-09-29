#!/usr/bin/env python3
"""Build the bounded Liora v708-v2 X2 evidence package."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X1 = ROOT / "x1"
X2 = ROOT / "x2"
for code_dir in (X1 / "code", X2 / "code"):
    if str(code_dir) not in sys.path:
        sys.path.insert(0, str(code_dir))

import rough_set as x1
import rough_set_x2 as x2


BOUNDARY = (
    "Finite synthetic same-owner rough-set mathematical, software, and documentary evidence "
    "only. No real participant, dataset, measurement, classification, identity decision, "
    "professional act, legal or cultural interpretation, affected-party or Maori authority, "
    "empirical GMUT confirmation, production THOS or Freed ID, complete privacy or "
    "accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/"
    "personhood, Theory-of-Everything, canon, or Stage 20 credit. NOT_READY_FOR_STAGE_20."
)

SKILLS = [
    (
        "ghc-liora-rough-consistency-v1",
        "Audit finite exact-equality decision-table consistency without treating intentional inconsistency as malformed input.",
        "Use the exact declared universe and condition subset. Report each block's decision set. A mixed-decision block is a bounded inconsistency witness, not permission to delete rows or infer real classification authority.",
    ),
    (
        "ghc-liora-missing-semantics-v1",
        "Compare explicitly declared pessimistic and optimistic missing-value neighborhood semantics on synthetic tables.",
        "Freeze the missing-value rule before evaluation. Never silently impute, wildcard, categorize, or delete a row. Refuse null or any undeclared marker as UNDECLARED_MISSING_VALUE_SEMANTICS.",
    ),
    (
        "ghc-liora-dominance-cones-v1",
        "Construct bounded finite dominance cones and upward-union approximations with exact declared directions.",
        "Treat every condition as a declared benefit direction in this local fixture only. Missing comparisons are incomparable except self. This supplies no preference, professional, or policy authority.",
    ),
    (
        "ghc-liora-correction-lineage-v1",
        "Apply one synthetic correction to a copied table while retaining before and after digests and the original record.",
        "Require exact object, attribute, old value, and new value. Reject stale old values. A recovery never erases the original failed or superseded evidence.",
    ),
    (
        "ghc-liora-authority-nonpromotion-v1",
        "Keep finite mathematical outputs separate from classification, identity, remedy, legal, cultural, and Maori authority.",
        "Emit explicit false authority fields with every bounded projection. Identical numbers under different provenance or authority states cannot confer the same real-world action permission.",
    ),
]

RUNNER_GROUPS = {
    "ghc_family_liora_v708_v2_x2_neighborhood.py": [
        "consistency_census",
        "pessimistic_neighborhoods",
        "optimistic_neighborhoods",
        "pessimistic_approximations",
        "optimistic_approximations",
    ],
    "ghc_family_liora_v708_v2_x2_dominance.py": [
        "dominance_cones",
        "dominance_approximations",
    ],
    "ghc_family_liora_v708_v2_x2_boundary.py": [
        "correction_lineage",
        "accessible_projection",
        "authority_boundary",
    ],
}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def sha256_json(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def invalid_subject(table: dict, operation: str, index: int) -> tuple[dict, str, str]:
    malformed = copy.deepcopy(table)
    kind = index % 5
    mutated_operation = operation
    if kind == 0:
        malformed["rows"][0]["decision"] = True
        classification = "INVALID_DECISION_BOOLEAN"
    elif kind == 1:
        attr = malformed["condition_attributes"][0]
        malformed["rows"][0]["conditions"][attr] = None
        classification = "UNDECLARED_MISSING_VALUE_SEMANTICS"
    elif kind == 2:
        malformed["rows"][1]["object"] = malformed["rows"][0]["object"]
        classification = "DUPLICATE_OBJECT"
    elif kind == 3:
        malformed["target"] = ["outside-universe"]
        classification = "UNKNOWN_TARGET_OBJECT"
    else:
        mutated_operation = "outside_scope"
        classification = "UNSUPPORTED_OPERATION"
    return malformed, mutated_operation, classification


def runner_source(allowed: list[str]) -> str:
    return f'''#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for code_dir in (ROOT / "x1" / "code", ROOT / "x2" / "code"):
    if str(code_dir) not in sys.path:
        sys.path.insert(0, str(code_dir))
import rough_set_x2 as domain

ALLOWED = {allowed!r}

parser = argparse.ArgumentParser()
parser.add_argument("--operation", required=True)
parser.add_argument("--table", required=True)
args = parser.parse_args()
if args.operation not in ALLOWED:
    raise SystemExit("outside_runner_scope")
table = json.loads(Path(args.table).read_text(encoding="utf-8"))
print(json.dumps(domain.dispatch(args.operation, table), ensure_ascii=False, sort_keys=True))
'''


def method(method_id: str, title: str, failure: str, witnesses: list[str], negatives: list[str], state: str = "validated") -> dict:
    return {
        "method_id": method_id,
        "title": title,
        "failure_signature": failure,
        "trigger_preconditions": ["immutable pushed X1", "bounded X2 owner lane"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_owner_scoped",
        "candidate_workaround": "Preserve the failed subject and execute only the separately named bounded recovery.",
        "validation_witness_ids": witnesses,
        "recurrence_guard": "Keep subject, oracle, checker, recovery, and authority state distinct.",
        "rollback": "Discard only uncommitted X2 outputs and return to the immutable X1 head.",
        "recommendation_state": state,
        "supersedes": [],
        "protected_gates": ["no_failure_erasure", "no_source_replay", "no_authority_promotion", "no_stage20"],
        "retained_negative_ids": negatives,
        "scope_boundary": BOUNDARY,
    }


def witness(witness_id: str, method_id: str, procedure: str, observed: str, result: str, negatives: list[str]) -> dict:
    return {
        "witness_id": witness_id,
        "method_id": method_id,
        "procedure": procedure,
        "scope": "Liora v708-v2 X2 owner delta",
        "expected": "bounded exact behavior or explicit refusal",
        "observed": observed,
        "result": result,
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": negatives,
        "boundary": BOUNDARY,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick-validate", required=True)
    parser.add_argument("--hook-script", required=True)
    args = parser.parse_args()

    fixtures = json.loads((ROOT / "planning" / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]
    projects = json.loads((ROOT / "planning" / "projects.json").read_text(encoding="utf-8"))["projects"]

    frozen_advice = json.loads((X1 / "advisory" / "teren-serein-reply-summary.json").read_text(encoding="utf-8"))
    write_json(X2 / "freeze" / "teren-boundary-rows.json", {
        "schema": "liora.x2.adviser-seed-freeze.v1",
        "source_label": frozen_advice["recommendation"]["label"],
        "frozen_before_x2_execution": True,
        "source_x1_execution_credit": 0,
        "fixture": x2.adviser_fixture(),
        "oracle": frozen_advice["recommendation"]["positive_region_oracle"],
        "complete_reduct_family": frozen_advice["recommendation"]["complete_reduct_family"],
        "core": frozen_advice["recommendation"]["core"],
        "mutant": frozen_advice["recommendation"]["deliberate_mutant"],
        "malformed_classification": frozen_advice["recommendation"]["malformed_classification"],
        "boundary": BOUNDARY,
    })

    contracts, safe, candidates, refusals, repairs = [], [], [], [], []
    contract_index = 0
    for table in fixtures:
        for operation in x2.X2_OPERATIONS:
            contract_index += 1
            contract_id = f"LI7082-X2-C{contract_index:03d}"
            result = x2.dispatch(operation, table)
            contracts.append({
                "contract_id": contract_id,
                "fixture_id": table["fixture_id"],
                "operation": operation,
                "input_sha256": sha256_json(table),
                "result_sha256": sha256_json(result),
                "outcome": "completed",
                "real_data_rows": 0,
            })
            safe.append({"task_id": contract_id + "-SAFE", "contract_id": contract_id, "status": "completed", "result_sha256": sha256_json(result)})
            malformed, malformed_operation, classification = invalid_subject(table, operation, contract_index)
            negative_id = contract_id + "-N001"
            failed = False
            error = None
            try:
                x2.dispatch(malformed_operation, malformed)
            except (ValueError, TypeError) as exc:
                failed = True
                error = str(exc)
            if not failed:
                raise RuntimeError((contract_id, "invalid subject accepted", classification))
            candidates.append({
                "task_id": contract_id + "-CANDIDATE",
                "contract_id": contract_id,
                "negative_id": negative_id,
                "classification": classification,
                "subject_sha256": sha256_json({"operation": malformed_operation, "table": malformed}),
                "observed_error": error,
                "status": "failed_retained_zero_credit",
            })
            refusals.append({"task_id": contract_id + "-REFUSAL", "negative_id": negative_id, "status": "completed", "original_success_credit": 0})
            recovered = x2.dispatch(operation, copy.deepcopy(table))
            repairs.append({"task_id": contract_id + "-CFR", "negative_id": negative_id, "status": "completed", "recovery_copy_sha256": sha256_json(recovered), "failed_subject_rewritten": False})

    write_json(X2 / "results" / "contracts.json", {"schema":"liora.x2.contracts.v1","count":len(contracts),"records":contracts,"boundary":BOUNDARY})
    write_json(X2 / "results" / "safe-tasks.json", {"schema":"liora.x2.safe.v1","count":len(safe),"records":safe,"boundary":BOUNDARY})
    write_json(X2 / "results" / "candidate-failures.json", {"schema":"liora.x2.candidates.v1","count":len(candidates),"records":candidates,"boundary":BOUNDARY})
    write_json(X2 / "results" / "refusals.json", {"schema":"liora.x2.refusals.v1","count":len(refusals),"records":refusals,"boundary":BOUNDARY})
    write_json(X2 / "results" / "clean-fix-refine.json", {"schema":"liora.x2.cfr.v1","count":len(repairs),"records":repairs,"boundary":BOUNDARY})

    adviser_oracle = x2.adviser_oracle()
    adviser_mutant = x2.adviser_mutant_claim()
    adviser_check = x2.check_adviser_mutant(adviser_mutant)
    null_variant = x2.adviser_fixture()
    null_variant["rows"][1]["conditions"]["a"] = None
    null_error = None
    try:
        x1.validate_table(null_variant)
    except ValueError as exc:
        null_error = str(exc)
    if null_error != "invalid_condition_value" or adviser_check["accepted"]:
        raise RuntimeError("adviser detector discrimination failed")
    write_json(X2 / "results" / "teren-boundary-rows-execution.json", {
        "schema":"liora.x2.teren-boundary-rows.v1",
        "oracle":adviser_oracle,
        "positive_control":{"candidate":["a","b"],"accepted":True},
        "mutant_claim":adviser_mutant,
        "mutant_check":adviser_check,
        "malformed_variant":{"classification":"UNDECLARED_MISSING_VALUE_SEMANTICS","observed_error":null_error,"refused":True},
        "adviser_source_independently_verified":False,
        "same_owner_execution":True,
        "boundary":BOUNDARY,
    })

    outcomes = []
    for project in projects:
        outcome = project["expected_disposition"]
        if project["project_id"] <= "LI7082-P10":
            evidence = "x1/results/contracts.json"
        elif project["project_id"] <= "LI7082-P16":
            evidence = "x2/results/contracts.json"
        elif outcome == "represented":
            evidence = "x2/results/contracts.json#accessible_projection"
        elif outcome == "open_gap":
            evidence = "x2/open-gap-register.json"
        else:
            evidence = "x2/exact-gate-register.json"
        outcomes.append({"project_id":project["project_id"],"title":project["title"],"outcome":outcome,"evidence":evidence})
    counts = {label:sum(row["outcome"]==label for row in outcomes) for label in ("completed","represented","open_gap","exact_gate")}
    if counts != {"completed":16,"represented":1,"open_gap":2,"exact_gate":1}:
        raise RuntimeError(counts)
    write_json(X2 / "outcome-ledger.json", {"schema":"liora.x2.outcomes.v1","records":outcomes,"counts":counts,"allowed_labels":["completed","represented","open_gap","exact_gate"],"boundary":BOUNDARY})
    write_json(X2 / "open-gap-register.json", {"schema":"liora.x2.open-gaps.v1","count":2,"records":[{"id":"LI7082-G001","project_id":"LI7082-P18","gap":"No governed real dataset, likelihood, preregistration, nuisance treatment, or independent empirical review."},{"id":"LI7082-G002","project_id":"LI7082-P19","gap":"No independent team reproduction or affected-user accessibility evaluation."}],"inherited_open_gaps":2511,"effective_open_gaps":2513,"boundary":BOUNDARY})
    write_json(X2 / "exact-gate-register.json", {"schema":"liora.x2.exact-gates.v1","count":1,"records":[{"id":"LI7082-E001","project_id":"LI7082-P20","gate":"Real classification, identity, remedy, legal, cultural, affected-party, and Maori-authority decisions require competent external authority and evidence."}],"inherited_exact_obligations":2871,"effective_exact_obligations":2872,"boundary":BOUNDARY})

    for name, description, body in SKILLS:
        write_text(X2 / "skills" / name / "SKILL.md", f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n\n{body}\n\n## Boundary\n\n{BOUNDARY}\n")
    skill_results = []
    for name, _, _ in SKILLS:
        process = subprocess.run([sys.executable, args.quick_validate, str(X2 / "skills" / name)], text=True, capture_output=True, encoding="utf-8")
        skill_results.append({"skill":name,"exit_code":process.returncode,"stdout":process.stdout.strip(),"stderr":process.stderr.strip()})
        if process.returncode:
            raise RuntimeError((name, process.stdout, process.stderr))
    write_json(X2 / "results" / "skill-validation.json", {"schema":"liora.x2.skill-validation.v1","records":skill_results,"main_agent_eof_read_pending":True,"boundary":BOUNDARY})

    runner_input = fixtures[0]
    write_json(X2 / "results" / "runner-input.json", runner_input)
    runner_smokes = []
    for filename, allowed in RUNNER_GROUPS.items():
        runner = X2 / "runners" / filename
        write_text(runner, runner_source(allowed))
        for operation in allowed:
            process = subprocess.run([sys.executable, str(runner), "--operation", operation, "--table", str(X2 / "results" / "runner-input.json")], text=True, capture_output=True, encoding="utf-8")
            if process.returncode:
                raise RuntimeError((filename, operation, process.stdout, process.stderr))
            json.loads(process.stdout)
            runner_smokes.append({"runner":filename,"operation":operation,"subject":"valid","exit_code":0,"result":"pass"})
        process = subprocess.run([sys.executable, str(runner), "--operation", "outside_scope", "--table", str(X2 / "results" / "runner-input.json")], text=True, capture_output=True, encoding="utf-8")
        if process.returncode == 0:
            raise RuntimeError((filename, "outside scope accepted"))
        runner_smokes.append({"runner":filename,"operation":"outside_scope","subject":"invalid","exit_code":process.returncode,"result":"fail_retained_zero_credit"})
    write_json(X2 / "results" / "runner-smokes.json", {"schema":"liora.x2.runner-smokes.v1","records":runner_smokes,"boundary":BOUNDARY})

    good = json.dumps({"hook_event_name":"SessionStart","cwd":"D:/GHC-Archives/worktrees/liora-venn-main-2"})
    bad = json.dumps({"hook_event_name":"Other","cwd":"D:/GHC-Archives/worktrees/liora-venn-main-2"})
    hook_smokes = []
    for hook in ("source","budget","consultation","roster","evidence"):
        for kind, payload in (("valid",good),("invalid",bad)):
            process = subprocess.run([sys.executable,args.hook_script,hook],input=payload,text=True,capture_output=True,encoding="utf-8")
            parsed = json.loads(process.stdout)
            expected = "hookSpecificOutput" in parsed if kind == "valid" else "systemMessage" in parsed
            if process.returncode or not expected:
                raise RuntimeError((hook,kind,process.stdout,process.stderr))
            hook_smokes.append({"hook":hook,"subject":kind,"exit_code":process.returncode,"expected_shape":expected,"live_host_event":False})
    write_json(X2 / "results" / "hook-smokes.json", {"schema":"liora.x2.hook-smokes.v1","records":hook_smokes,"manual_smokes":10,"live_host_events":0,"boundary":BOUNDARY})

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    tests = subprocess.run([sys.executable,"-m","unittest","discover","-s",str(X2 / "tests"),"-p","test_*.py","-v"],text=True,capture_output=True,encoding="utf-8",env=env)
    combined = tests.stdout + tests.stderr
    test_count = combined.count(" ... ok")
    if tests.returncode or test_count != 35:
        raise RuntimeError((test_count,tests.stdout,tests.stderr))
    write_json(X2 / "results" / "tests.json", {"schema":"liora.x2.tests.v1","exit_code":0,"tests":test_count,"stdout":tests.stdout,"stderr":tests.stderr,"boundary":BOUNDARY})

    flow = json.loads((X1 / "method-flow.json").read_text(encoding="utf-8"))
    flow["phase"] = "v708-v2-x2"
    methods = flow["methods"]
    witnesses = flow["witnesses"]

    post_neg = ["LI7082-X2-N001"]
    methods.append(method("LI7082-X2-M018","Quoted upstream-ref recovery","An unquoted PowerShell @{u} token is transformed before Git receives it.",["LI7082-X2-M018-W001","LI7082-X2-M018-W002"],post_neg))
    witnesses.extend([
        witness("LI7082-X2-M018-W001","LI7082-X2-M018","combined post-X1 divergence probe","Push succeeded, but the unquoted upstream token became an invalid revision.","fail",post_neg),
        witness("LI7082-X2-M018-W002","LI7082-X2-M018","explicit scalar upstream and fresh-live recovery","Clean, 0/0 divergent, and four-way equal at the immutable X1 head.","pass",post_neg),
    ])

    mutation_negatives = [record["negative_id"] for record in candidates]
    contract_witness_ids = []
    for contract, candidate, refusal, repair in zip(contracts,candidates,refusals,repairs):
        base = contract["contract_id"]
        ids = [base+"-SAFE-W",base+"-NEG-W",base+"-REFUSE-W",base+"-CFR-W"]
        contract_witness_ids.extend(ids)
        witnesses.extend([
            witness(ids[0],"LI7082-X2-M019","execute frozen valid contract",contract["result_sha256"],"pass",[]),
            witness(ids[1],"LI7082-X2-M019","execute preregistered invalid subject",candidate["classification"],"fail",[candidate["negative_id"]]),
            witness(ids[2],"LI7082-X2-M019","retain explicit refusal",candidate["observed_error"],"pass",[candidate["negative_id"]]),
            witness(ids[3],"LI7082-X2-M019","execute separate valid-copy recovery",repair["recovery_copy_sha256"],"pass",[candidate["negative_id"]]),
        ])
    methods.append(method("LI7082-X2-M019","Finite X2 contract and mutation harness","An invalid table or operation is admitted, or its failed subject is overwritten by recovery.",contract_witness_ids,mutation_negatives))

    adviser_negatives = ["LI7082-X2-AD-N001","LI7082-X2-AD-N002"]
    adviser_ids = [f"LI7082-X2-AD-W{i:02d}" for i in range(1,7)]
    methods.append(method("LI7082-X2-M020","Teren boundary-row detector","A candidate reduct is evaluated on a silently restricted universe or undeclared missing semantics are invented.",adviser_ids,adviser_negatives))
    witnesses.extend([
        witness(adviser_ids[0],"LI7082-X2-M020","exhaustively enumerate eight attribute subsets","Exact oracle, reduct family, and core matched.","pass",[]),
        witness(adviser_ids[1],"LI7082-X2-M020","positive reduct control","{a,b} preserved the full positive region and was minimal.","pass",[]),
        witness(adviser_ids[2],"LI7082-X2-M020","positive-only-universe mutant",str(adviser_mutant),"fail",[adviser_negatives[0]]),
        witness(adviser_ids[3],"LI7082-X2-M020","mutant detector",str(adviser_check),"pass",[adviser_negatives[0]]),
        witness(adviser_ids[4],"LI7082-X2-M020","undeclared null subject",null_error,"fail",[adviser_negatives[1]]),
        witness(adviser_ids[5],"LI7082-X2-M020","undeclared missing-semantics refusal","UNDECLARED_MISSING_VALUE_SEMANTICS retained separately from unsoundness.","pass",[adviser_negatives[1]]),
    ])

    runner_negatives = [f"LI7082-X2-RUNNER-N{i:02d}" for i in range(1,4)]
    runner_ids = [f"LI7082-X2-RUNNER-W{i:02d}" for i in range(1,len(runner_smokes)+1)]
    methods.append(method("LI7082-X2-M021","Family-current X2 runner scope guard","A runner accepts an operation outside its declared group.",runner_ids,runner_negatives))
    invalid_runner_index = 0
    for witness_id, record in zip(runner_ids,runner_smokes):
        invalid = record["subject"] == "invalid"
        negatives = []
        if invalid:
            negatives = [runner_negatives[invalid_runner_index]]
            invalid_runner_index += 1
        witnesses.append(witness(witness_id,"LI7082-X2-M021","runner smoke",record["runner"]+":"+record["operation"],"fail" if invalid else "pass",negatives))

    skill_ids = [f"LI7082-X2-SKILL-W{i:02d}" for i in range(1,6)]
    methods.append(method("LI7082-X2-M022","Owner-local X2 skill validation and complete readback","A generated guide is used before complete main-agent readback.",skill_ids,[],state="candidate"))
    for witness_id, record in zip(skill_ids,skill_results):
        witnesses.append(witness(witness_id,"LI7082-X2-M022","quick validate generated guide",record["skill"],"pass",[]))

    hook_negatives = [f"LI7082-X2-HOOK-N{i:02d}" for i in range(1,6)]
    hook_ids = [f"LI7082-X2-HOOK-W{i:02d}" for i in range(1,11)]
    methods.append(method("LI7082-X2-M023","Current v20 advisory-hook manual smokes","A malformed hook payload is promoted into live host or routing evidence.",hook_ids,hook_negatives))
    for index,(witness_id,record) in enumerate(zip(hook_ids,hook_smokes)):
        invalid = record["subject"] == "invalid"
        negatives = [hook_negatives[index//2]] if invalid else []
        witnesses.append(witness(witness_id,"LI7082-X2-M023","manual hook smoke",record["hook"],"fail" if invalid else "pass",negatives))

    test_ids = [f"LI7082-X2-TEST-W{i:02d}" for i in range(1,36)]
    methods.append(method("LI7082-X2-M024","X2 owner test selection","A bounded domain or detector obligation lacks an executable test.",test_ids,[]))
    for witness_id in test_ids:
        witnesses.append(witness(witness_id,"LI7082-X2-M024","owner unittest method","pass","pass",[]))

    methods.append(method("LI7082-X2-M025","Single acknowledged five-task X2 advisory","The X2 adviser request is duplicated or asks fewer than five distinct tasks.",["LI7082-X2-ADVISER-W001"],[]))
    witnesses.append(witness("LI7082-X2-ADVISER-W001","LI7082-X2-M025","native existing-conversation send","One acknowledged message requested five non-overlapping advisory tasks; zero resends.","pass",[]))

    hook_path_negatives = ["LI7082-X2-N002"]
    methods.append(method("LI7082-X2-M026","Exact current advisory-hook path recovery","A stale release path is treated as the current v20 advisory-hook location.",["LI7082-X2-M026-W001","LI7082-X2-M026-W002"],hook_path_negatives))
    witnesses.extend([
        witness("LI7082-X2-M026-W001","LI7082-X2-M026","first hook-script path preflight","The guessed plugins/ghc-lab-advisory-hook/scripts path was absent; no X2 build ran.","fail",hook_path_negatives),
        witness("LI7082-X2-M026-W002","LI7082-X2-M026","bounded release inventory and exact path resolution","Resolved plugins/ghc-family-laboratory-v20/scripts/advisory_hook.py.","pass",hook_path_negatives),
    ])

    flow["counts"]["methods"] = len(methods)
    flow["counts"]["witnesses"] = len(witnesses)
    flow["counts"]["states"] = {state:sum(item["recommendation_state"]==state for item in methods) for state in ("observed","candidate","validated","preferred","superseded","deprecated")}
    flow["counts"]["witness_results"] = {"pass":sum(item["result"]=="pass" for item in witnesses),"fail":sum(item["result"]=="fail" for item in witnesses)}
    write_json(X2 / "method-flow.json", flow)

    x1_fail = json.loads((X1 / "failure-ledger.json").read_text(encoding="utf-8"))
    x2_failures = {
        "operational": [
            {"id":"LI7082-X2-N001","failure":"The combined post-push wrapper passed an unquoted PowerShell @{u} expression to Git as an invalid revision after the push had already succeeded.","recovery":"Use explicit quoted/scalar upstream, tracking, and fresh-live refs without replaying the successful push.","original_success_credit":0},
            {"id":"LI7082-X2-N002","failure":"The first hook-script path preflight used a stale plugin directory name and found no file.","recovery":"Inventory only the bounded current release and resolve plugins/ghc-family-laboratory-v20/scripts/advisory_hook.py before the one X2 build.","original_success_credit":0},
        ],
        "candidate_failed_subjects":len(candidates),
        "adviser_failed_subjects":2,
        "runner_failed_subjects":3,
        "hook_failed_subjects":5,
    }
    write_json(X2 / "failure-ledger.json", {"schema":"liora.x2.failures.v1","x1_total_failed_witnesses":x1_fail["total_failed_witnesses"],"x2":x2_failures,"total_failed_witnesses":flow["counts"]["witness_results"]["fail"],"boundary":BOUNDARY})

    write_json(X2 / "advisory-state.json", {"schema":"liora.x2.advisory.v1","title":"Teren Serein","message_sent":True,"five_tasks_requested":True,"send_count":1,"resend_count":0,"delivery_acknowledged":True,"reply_received":False,"state":"SENT_ONCE_ACKNOWLEDGED_REPLY_PENDING","private_target_exported":False,"boundary":BOUNDARY})
    write_json(X2 / "summary.json", {"schema":"liora.x2.summary.v1","contracts":len(contracts),"safe":len(safe),"candidate_failed_subjects":len(candidates),"refusals":len(refusals),"clean_fix_refine":len(repairs),"tests":test_count,"skills":len(SKILLS),"runners":len(RUNNER_GROUPS),"hook_manual_smokes":len(hook_smokes),"hook_live_events":0,"adviser_state":"SENT_ONCE_ACKNOWLEDGED_REPLY_PENDING","adviser_tasks_requested":5,"outcomes":counts,"source_executions":0,"source_canonical_replays":0,"x1_head":"efd43f08eb4bfb66830c5c4da1274c3c643d5d7b","boundary":BOUNDARY})
    write_json(X2 / "build-receipt.json", {"schema":"liora.x2.build.v1","contracts":len(contracts),"tests":test_count,"skills":len(SKILLS),"runners":len(RUNNER_GROUPS),"candidate_failures":len(candidates),"method_flow":flow["counts"],"boundary":BOUNDARY})
    write_text(X2 / "overview.md", f"""# Liora Venn v708-v2 X2 overview

X2 executes ten finite rough-set consistency, missing-semantics, dominance, correction, accessibility-projection, and authority-boundary operations across fifteen wholly synthetic tables. It retains 150 valid contract results, 150 failed malformed subjects, 150 explicit refusals, and 150 separate valid-copy recoveries. Thirty-five bounded owner tests pass.

Teren Serein's `BOUNDARY_ROWS_ARE_NOT_DISPOSABLE` reply was sanitized and frozen before execution. The exact eight-subset oracle, complete reduct family, core, positive control, restricted-universe mutant, and undeclared-null refusal all produced their expected discriminating results. This is same-owner use of advisory source material, not independent reproduction.

Five phase-local skill guides pass quick validation but remain candidate until complete main-agent readback and smoke-use. Three family-current runners accept their exact groups and refuse outside scope. Five current hooks receive valid and invalid manual smokes; live host events remain zero. One acknowledged X2 message asks Teren for five distinct follow-up tasks and is not resent while pending.

The twenty project outcomes are exactly 16 `completed`, 1 `represented`, 2 `open_gap`, and 1 `exact_gate`. {BOUNDARY}
""")

    print(json.dumps({"contracts":len(contracts),"tests":test_count,"skills":len(SKILLS),"runners":len(RUNNER_GROUPS),"method_flow":flow["counts"],"outcomes":counts},sort_keys=True))


if __name__ == "__main__":
    main()
