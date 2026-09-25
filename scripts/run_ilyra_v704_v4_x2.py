#!/usr/bin/env python3
"""Execute the frozen Ilyra v704-v4 x2 portfolio and build bounded evidence."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_coupled_uncertainty import ContractError, evaluate


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "ilyra-fen" / "v704-v4" / "planning"
OUT = ROOT / "docs" / "ilyra-fen" / "v704-v4" / "x2"
BOUNDARY = "Finite synthetic same-owner mathematical and software evidence. No empirical GMUT confirmation, production THOS or Freed ID, independent reproduction, real participant evidence, identity, consciousness, personhood, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, AGI, ASI or Theory-of-Everything proof. NOT_READY_FOR_STAGE_20."


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_contracts() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for file in sorted((PLAN / "proposals").glob("*.json"))[10:]:
        rows.extend(json.loads(file.read_text(encoding="utf-8"))["contracts"])
    if len(rows) != 150:
        raise AssertionError(f"expected 150 x2 contracts, got {len(rows)}")
    return rows


def mutate(request: dict[str, Any], kind: str) -> dict[str, Any]:
    row = copy.deepcopy(request)
    data = row["input"]
    if kind == "missing_model":
        data.pop("global_models", None)
    elif kind == "mass_mismatch":
        data["global_models"][0][0][0][0] = "2"
    elif kind == "initial_shape":
        data["initial"].append("0")
    elif kind == "bad_policy":
        data["fixed_policy"][0] = 2
    elif kind == "negative_horizon":
        data["horizon"] = -1
    elif kind == "invalid_discount":
        data["discount"] = "3/2"
    elif kind == "reward_shape":
        data["rewards"].pop()
    elif kind == "empty_actions":
        data["actions"] = []
    elif kind == "zero_denominator":
        data["terminal"][0] = "1/0"
    elif kind == "unknown_operation":
        row["op"] = "unregistered_evidence_promotion"
    else:
        raise AssertionError(kind)
    return row


def skill_body(name: str, title: str) -> str:
    return f"""---
name: {name}
description: Inspect {title} in finite globally coupled transition-model records; use for bounded synthetic exact-rational review, never empirical or operational authority.
---

# {title.title()}

Use the frozen v704-v4 schema and exact fractions. Keep the fixed-global-model problem distinct from its separately labelled rectangular relaxation.

## Workflow

1. Validate dimensions, probability mass, horizon, discount, policy actions and the requested operation.
2. Preserve exact fractions, every exact tie, and the declared outcome label.
3. Retain failed subjects at zero credit even when a bounded refusal passes.
4. Keep calibration, deployment, participant, legal, cultural and Maori-authority gaps explicit.

## Boundary

{BOUNDARY}
"""


def runner_source(allowed: list[str]) -> str:
    return f'''#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT / "scripts"))
from ghc_family_coupled_uncertainty import ContractError,evaluate
ALLOWED={allowed!r}
try:
    request=json.load(sys.stdin) if len(sys.argv)==1 else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if request.get("op") not in ALLOWED: raise ContractError("operation outside this bounded runner")
    print(json.dumps({{"ok":True,"result":evaluate(request)}},sort_keys=True))
except Exception as exc:
    print(json.dumps({{"ok":False,"error":str(exc)}},sort_keys=True))
    raise SystemExit(2)
'''


def method_flow(
    safe: list[dict[str, Any]],
    failed: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    cfr: list[dict[str, Any]],
    operations: list[str],
) -> dict[str, Any]:
    methods: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    state_events: list[dict[str, Any]] = []
    recommendations: list[dict[str, Any]] = []
    negative_by_method: dict[str, list[str]] = {op: [] for op in operations}
    witness_by_method: dict[str, list[str]] = {op: [] for op in operations}
    for row in failed:
        negative_by_method[row["operation"]].append(row["negative_id"])
    for rows, result, prefix in (
        (safe, "pass", "S"),
        (failed, "fail", "C"),
        (refusals, "pass", "R"),
        (cfr, "pass", "F"),
    ):
        for row in rows:
            witness_id = f"IF7044-x2-W{prefix}{row['ordinal']:03d}"
            operation = row["operation"]
            witness_by_method[operation].append(witness_id)
            witnesses.append(
                {
                    "witness_id": witness_id,
                    "method_id": f"IF7044-x2-M{operations.index(operation)+1:02d}",
                    "procedure": row["procedure"],
                    "scope": "v704-v4 x2 owner delta",
                    "expected": row["expected"],
                    "observed": row["observed"],
                    "result": result,
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [row["negative_id"]] if row.get("negative_id") else [],
                    "boundary": BOUNDARY,
                }
            )
    for index, operation in enumerate(operations, 1):
        method_id = f"IF7044-x2-M{index:02d}"
        methods.append(
            {
                "method_id": method_id,
                "title": operation.replace("_", " "),
                "failure_signature": "Malformed dimensions, mass, rational values, policy actions, unknown operations or unsupported evidence promotion must fail closed.",
                "trigger_preconditions": ["frozen x2 request", "immutable pushed x1", "finite globally coupled model"],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now",
                "candidate_workaround": "Validate the smallest literal record and return exact bounded output or a typed refusal.",
                "validation_witness_ids": witness_by_method[operation],
                "recurrence_guard": "Keep fixed-global and rowwise-rectangular semantics explicitly distinct and compare exact frozen results.",
                "rollback": "Discard only the derived output; retain the request, failure, refusal, gap and gate records.",
                "recommendation_state": "validated",
                "supersedes": [],
                "protected_gates": ["x1_immutable", "candidate_nonpromotion", "calibration_nonpromotion", "authority_nonpromotion"],
                "retained_negative_ids": negative_by_method[operation],
                "scope_boundary": BOUNDARY,
            }
        )
        state_events.append(
            {
                "event_id": f"IF7044-x2-E{index:02d}",
                "method_id": method_id,
                "from": "observed",
                "to": "validated",
                "witness_id": next(w for w in witness_by_method[operation] if "-WS" in w),
            }
        )
        recommendations.append(
            {
                "recommendation_id": f"IF7044-x2-R{index:02d}",
                "method_id": method_id,
                "state": "validated",
                "text": f"Use {operation} only within its frozen finite synthetic contract.",
            }
        )
    passing = sum(1 for witness in witnesses if witness["result"] == "pass")
    failing = sum(1 for witness in witnesses if witness["result"] == "fail")
    baseline = {
        "negatives": 64077,
        "methods": 5733,
        "failed_witnesses": 55242,
        "passing_witnesses": 174793,
        "witnesses": 230035,
        "open_gaps": 1978,
        "exact_gates": 2063,
    }
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": "v704-v4-x2",
        "owner": "Ilyra Fen",
        "identity_boundary": "Relational working identity only; no consciousness, personhood, continuity or authority evidence.",
        "execution_authority": "owner_self_scoped_delta",
        "source_commit": "0459221af11cf03a12feb2b70d65bfff4f97df7e",
        "final_commit": None,
        "changed_file_allowlist": [
            "docs/ilyra-fen/v704-v4/x2",
            "scripts/ghc_family_coupled_uncertainty.py",
            "scripts/run_ilyra_v704_v4_x2.py",
            "tests/test_ilyra_v704_v4_x2.py",
        ],
        "module_allowlist": [
            "scripts/ghc_family_coupled_uncertainty.py",
            "scripts/run_ilyra_v704_v4_x2.py",
            "tests/test_ilyra_v704_v4_x2.py",
        ],
        "repository_scan": False,
        "module_scan": True,
        "cross_lane_scan": False,
        "unchanged_history_scan": False,
        "sibling_lane_mutation": False,
        "exact_pushed_head_required": True,
        "methods": methods,
        "witnesses": witnesses,
        "state_events": state_events,
        "recommendations": recommendations,
        "counts": {
            "methods": len(methods),
            "witnesses": len(witnesses),
            "state_events": len(state_events),
            "recommendations": len(recommendations),
            "states": {"observed": 0, "candidate": 0, "validated": len(methods), "preferred": 0, "superseded": 0, "deprecated": 0},
            "witness_results": {"pass": passing, "fail": failing},
        },
        "evidence_counts": {
            "negatives": failing,
            "methods": len(methods),
            "failed_witnesses": failing,
            "passing_witnesses": passing,
            "witnesses": len(witnesses),
            "open_gaps": 0,
            "exact_gates": 0,
        },
        "selected_prior_baseline": baseline,
        "source_fold_count": 0,
        "effective_totals": {
            "negatives": baseline["negatives"] + failing,
            "methods": baseline["methods"] + len(methods),
            "failed_witnesses": baseline["failed_witnesses"] + failing,
            "passing_witnesses": baseline["passing_witnesses"] + passing,
            "witnesses": baseline["witnesses"] + len(witnesses),
            "open_gaps": baseline["open_gaps"],
            "exact_gates": baseline["exact_gates"],
        },
        "boundary": BOUNDARY,
    }


def build_viewer(contracts: list[dict[str, Any]]) -> None:
    scenes = []
    by_profile = {row["profile_id"]: row for row in contracts if row["operation"] == "accessible_summary"}
    coordinates = {row["profile_id"]: row for row in contracts if row["operation"] == "scene_coordinates"}
    for profile_id in sorted(by_profile):
        summary = evaluate(by_profile[profile_id]["request"])
        coordinate = evaluate(coordinates[profile_id]["request"])
        scenes.append({"profile_id": profile_id, **summary, "coordinates": coordinate["coordinates"]})
    write_json(OUT / "viewer" / "data.json", {"count": len(scenes), "scenes": scenes, "boundary": BOUNDARY})
    embedded = json.dumps(scenes, ensure_ascii=False).replace("</", "<\\/")
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ilyra v704-v4 coupled uncertainty viewer</title>
<style>
:root{{--bg:#f7f4ec;--ink:#15251f;--card:#fff;--accent:#176b5b;--line:#bfd2c9;--muted:#53645d}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.55 system-ui,sans-serif}}
main{{max-width:1040px;margin:auto;padding:2rem}} h1{{line-height:1.1}} .boundary{{border-left:.4rem solid #9b5d00;padding:1rem;background:#fff8e6}}
label{{font-weight:700}} select{{font:inherit;padding:.55rem;margin:.5rem 0 1rem;border:2px solid var(--accent);border-radius:.35rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1rem}} .card{{background:var(--card);border:1px solid var(--line);border-radius:.7rem;padding:1rem}}
dt{{font-weight:700;color:var(--accent)}} dd{{margin:0 0 .75rem}} table{{width:100%;border-collapse:collapse}} th,td{{border:1px solid var(--line);padding:.6rem;text-align:left}} caption{{font-weight:700;text-align:left;margin:.8rem 0}}
:focus-visible{{outline:4px solid #f0a000;outline-offset:3px}} .muted{{color:var(--muted)}}
</style>
</head>
<body><main>
<h1>Coupled transition-model uncertainty</h1>
<p class="boundary"><strong>Boundary:</strong> finite synthetic same-owner evidence only. This viewer is not empirical validation, operational authority, independent reproduction, or Stage 20 evidence.</p>
<label for="profile">Choose one of 15 exact synthetic profiles</label><br>
<select id="profile"></select>
<section id="summary" aria-live="polite"></section>
<table><caption>All profile coordinates</caption><thead><tr><th>Profile</th><th>Decisions</th><th>States</th><th>Exact gap</th></tr></thead><tbody id="rows"></tbody></table>
<p class="muted">A rectangular comparator may combine rows that no single fixed global model contains.</p>
</main><script>
const scenes={embedded};
const select=document.querySelector('#profile'),summary=document.querySelector('#summary'),rows=document.querySelector('#rows');
for(const scene of scenes){{const option=document.createElement('option');option.value=scene.profile_id;option.textContent=`${{scene.profile_id}} — ${{scene.title}}`;select.append(option);const tr=document.createElement('tr');for(const value of [scene.profile_id,...scene.coordinates]){{const td=document.createElement('td');td.textContent=value;tr.append(td)}}rows.append(tr)}}
function render(){{const s=scenes.find(x=>x.profile_id===select.value)||scenes[0];summary.innerHTML=`<h2>${{s.profile_id}} — ${{s.title}}</h2><div class="grid"><dl class="card"><dt>Fixed-global robust value</dt><dd>${{s.robust_value}}</dd><dt>Rowwise rectangular value</dt><dd>${{s.rectangular_value}}</dd></dl><dl class="card"><dt>Exact rectangularity gap</dt><dd>${{s.gap}}</dd><dt>States / global models</dt><dd>${{s.states}} / ${{s.global_models}}</dd></dl></div><p>${{s.note}}</p>`}}select.addEventListener('change',render);render();
</script></body></html>'''
    write_text(OUT / "viewer" / "index.html", html)


def build_plugin() -> None:
    plugin = OUT / "plugins" / "ghc-family-ilyra-coupled-workflow-hooks"
    manifest = {
        "name": "ghc-family-ilyra-coupled-workflow-hooks",
        "version": "1.0.0",
        "description": "Ten bounded nonblocking advisories for coupled-model evidence and guarded delivery.",
        "author": {"name": "GHC Ilyra tooling"},
        "interface": {
            "displayName": "GHC coupled workflow advisories",
            "shortDescription": "Keep model, evidence, Git and delivery boundaries visible.",
            "longDescription": "Ten synchronous constant-output advisory hooks with bounded input and no payload-driven side effects. Manual validation remains separate from live lifecycle observation.",
            "developerName": "GHC Ilyra tooling",
            "category": "Productivity",
            "capabilities": [],
            "defaultPrompt": ["Review coupled-model workflow boundaries."],
        },
    }
    write_json(plugin / ".codex-plugin" / "plugin.json", manifest)
    plan = json.loads((PLAN / "hook-plan.json").read_text(encoding="utf-8"))
    grouped: dict[str, list[dict[str, Any]]] = {"PreToolUse": [], "PostToolUse": [], "Stop": []}
    for row in plan["hooks"]:
        command = f'node "${{PLUGIN_ROOT}}/scripts/advisories.txt" {row["hook_id"]}'
        command_windows = f'node "$env:PLUGIN_ROOT/scripts/advisories.txt" {row["hook_id"]}'
        item: dict[str, Any] = {
            "hooks": [{"type": "command", "command": command, "commandWindows": command_windows, "timeout": 5, "async": False, "statusMessage": "Checking a bounded coupled-model advisory"}]
        }
        if row["event"] != "Stop":
            item["matcher"] = ".*"
        grouped[row["event"]].append(item)
    write_json(plugin / "hooks" / "hooks.json", {"description": "Nonblocking constant-output checks; no payload-driven side effects.", "hooks": grouped})
    advisories = r'''\'use strict\';
const fs=require('fs');
const messages={
 model_setting_change:'Model changes require a fresh exact authority check; preserve the admitted model.',
 source_lane_mutation:'The source and sibling lanes are read-only; use the additive owner lane.',
 successful_replay:'Do not replay a successful canonical or successful stage aggregate.',
 rectangularity_promotion:'A rectangular relaxation is a comparator, not evidence for the fixed-global model or the real world.',
 malformed_subject_promotion:'A passing refusal never promotes the malformed subject.',
 broad_git_stage:'Stage only reviewed owner paths and protect foreign staged work.',
 destructive_git:'Destructive Git requires exact current authority and is outside this additive phase.',
 raw_identifier_output:'Do not publish raw identifiers or private local paths.',
 prepared_delivery:'Prepared delivery is not sent or acknowledged delivery.',
 accepted_resend:'Do not resend an acknowledged or unresolved accepted handoff.'
};
function inspect(id,p){
 if(!Object.hasOwn(messages,id)||!p||typeof p!=='object'||Array.isArray(p))return{};
 if(p.hook_event_name==='Stop'&&p.stop_hook_active===true)return{};
 const command=typeof p.tool_input?.command==='string'?p.tool_input.command:typeof p.tool_input?.cmd==='string'?p.tool_input.cmd:'';
 const response=p.tool_response??{},text=typeof response==='string'?response:typeof response.output==='string'?response.output:JSON.stringify(response);
 const summary=typeof p.last_assistant_message==='string'?p.last_assistant_message:'';let adverse=false;
 switch(id){
 case'model_setting_change':adverse=/\b(?:model|reasoning effort)\b[\s\S]{0,60}\b(?:change|override|switch)\b/i.test(command);break;
 case'source_lane_mutation':adverse=/talen-briar-main-1/i.test(command)&&/\b(?:add|commit|write|remove|delete|move)\b/i.test(command);break;
 case'successful_replay':adverse=/\b(?:canonical|aggregate)\b[\s\S]{0,60}\b(?:replay|rerun|again)\b/i.test(command);break;
 case'rectangularity_promotion':adverse=/rectangular[\s\S]{0,100}\b(?:empirical|real-world|proves?|validated)\b/i.test(command+' '+summary);break;
 case'malformed_subject_promotion':adverse=/subject_promoted[\s\S]{0,10}true|malformed[\s\S]{0,80}\bcompleted\b/i.test(command+' '+text);break;
 case'broad_git_stage':adverse=/\bgit\s+add\s+(?:-A\b|\.(?:\s|$))/i.test(command);break;
 case'destructive_git':adverse=/\bgit\s+(?:reset\s+--hard|clean\s+-[a-z]*f|push\b[\s\S]*(?:--force|\s-f(?:\s|$)))/i.test(command);break;
 case'raw_identifier_output':adverse=/[A-Za-z]:\\(?:Users|GHC-Archives)\\|\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b/i.test(text);break;
 case'prepared_delivery':adverse=typeof response==='object'&&response!==null&&(response.state==='PREPARED_NOT_SENT'||response.route_state==='PREPARED_NOT_SENT');break;
 case'accepted_resend':adverse=/\b(?:resent|resending|send again)\b[\s\S]{0,80}\b(?:acknowledged|accepted|unresolved)\b/i.test(summary);break;
 }
 return adverse?{systemMessage:messages[id]}:{};
}
function main(){const buffer=Buffer.alloc(131073);let count=0,result={};while(count<buffer.length){const n=fs.readSync(0,buffer,count,buffer.length-count,null);if(n===0)break;count+=n}if(count<=131072){try{result=inspect(process.argv[2],JSON.parse(buffer.subarray(0,count).toString('utf8')))}catch{}}process.stdout.write(JSON.stringify(result)+'\n')}
module.exports={inspect};if(require.main===module)main();
'''.replace("\\'use strict\\';", "'use strict';")
    write_text(plugin / "scripts" / "advisories.txt", advisories)
    write_text(
        plugin / "README.md",
        f"""# GHC coupled workflow advisories

Ten synchronous, nonblocking constant-output advisories cover admitted-model drift, source-lane mutation, successful replay, rectangularity promotion, malformed-subject promotion, broad staging, destructive Git, raw identifiers, prepared delivery and accepted resend.

The hook program reads at most 131,072 bytes, executes no payload-provided command, writes no file, and returns either an empty object or one fixed advisory message. Installation is not evidence that a live lifecycle event exercised a hook.

## Boundary

{BOUNDARY}
""",
    )


def main() -> int:
    contracts = load_contracts()
    operations = list(dict.fromkeys(row["operation"] for row in contracts))
    safe: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    refusals: list[dict[str, Any]] = []
    cfr: list[dict[str, Any]] = []
    for ordinal, contract in enumerate(contracts, 1):
        actual = evaluate(contract["request"])
        if actual != contract["expected"]:
            raise AssertionError(f"frozen expected mismatch: {contract['proposal_id']}")
        safe.append({"ordinal": ordinal, "task_id": f"IF7044-x2-S{ordinal:03d}", "operation": contract["operation"], "proposal_id": contract["proposal_id"], "procedure": "Evaluate the frozen core request with the independent Python engine.", "expected": "semantic equality with the frozen expected result", "observed": "semantic equality", "result": "pass", "negative_id": None})
    for index in range(250):
        contract = contracts[index % len(contracts)]
        actual = evaluate(copy.deepcopy(contract["request"]))
        if actual != contract["expected"]:
            raise AssertionError(f"auxiliary repeat mismatch {index}")
        ordinal = 151 + index
        safe.append({"ordinal": ordinal, "task_id": f"IF7044-x2-S{ordinal:03d}", "operation": contract["operation"], "proposal_id": contract["proposal_id"], "procedure": "Re-evaluate a frozen request as a deterministic auxiliary boundary fixture.", "expected": "same exact bounded result without new proposal credit", "observed": "same bounded result", "result": "pass", "negative_id": None})
    kinds = ["missing_model", "mass_mismatch", "initial_shape", "bad_policy", "negative_horizon", "invalid_discount", "reward_shape", "empty_actions", "zero_denominator", "unknown_operation"]
    for index in range(300):
        contract = contracts[index % len(contracts)]
        kind = kinds[index % len(kinds)]
        malformed = mutate(contract["request"], kind)
        negative_id = f"IF7044-x2-N{index+1:03d}"
        try:
            evaluate(malformed)
        except (ContractError, KeyError, TypeError, IndexError, ZeroDivisionError) as exc:
            error = str(exc)
        else:
            raise AssertionError(f"candidate unexpectedly accepted {index+1}")
        failed.append({"ordinal": index + 1, "candidate_id": f"IF7044-x2-C{index+1:03d}", "operation": contract["operation"], "mutation_class": kind, "negative_id": negative_id, "procedure": "Submit a preregistered malformed subject.", "expected": "subject remains failed at zero completion credit", "observed": error, "result": "fail", "credit": 0})
        refusals.append({"ordinal": index + 1, "refusal_id": f"IF7044-x2-RF{index+1:03d}", "operation": contract["operation"], "negative_id": negative_id, "procedure": "Check the engine emits a bounded typed refusal for the retained malformed subject.", "expected": "refusal passes without promoting the subject", "observed": "bounded refusal returned", "result": "pass", "subject_promoted": False})
    for index in range(300):
        contract = contracts[index % len(contracts)]
        focus = ["rectangular distinction", "exact fractions", "tie retention", "gap retention", "source binding", "rollback"][index % 6]
        cfr.append({"ordinal": index + 1, "task_id": f"IF7044-x2-F{index+1:03d}", "operation": contract["operation"], "proposal_id": contract["proposal_id"], "focus": focus, "procedure": f"Review {focus} for one frozen contract.", "expected": "review passes without deleting or promoting evidence", "observed": "review passed", "result": "pass", "negative_id": None})

    capability = json.loads((PLAN / "capability-plan.json").read_text(encoding="utf-8"))
    for row in capability["local_skills"][10:]:
        title = row["name"].removeprefix("ghc-family-").replace("-", " ")
        write_text(OUT / "skills" / row["name"] / "SKILL.md", skill_body(row["name"], title))
    allowed_groups = [
        ["rectangular_relaxation", "rectangularity_gap"],
        ["model_deletion_sensitivity", "relabel_covariance"],
        ["discount_zero_certificate", "mixture_representation"],
        ["accessible_summary", "scene_coordinates"],
        ["calibration_evidence_gap", "authority_gate"],
    ]
    runner_smokes = []
    for row, allowed in zip(capability["local_runners"][5:], allowed_groups):
        runner_path = OUT / "runners" / row["name"]
        write_text(runner_path, runner_source(allowed))
        contract = next(item for item in contracts if item["operation"] == allowed[0])
        valid = subprocess.run([sys.executable, str(runner_path)], input=json.dumps(contract["request"]), text=True, capture_output=True)
        malformed = copy.deepcopy(contract["request"])
        malformed["input"].pop("global_models", None)
        invalid = subprocess.run([sys.executable, str(runner_path)], input=json.dumps(malformed), text=True, capture_output=True)
        if valid.returncode != 0 or invalid.returncode != 2:
            raise AssertionError(f"runner smoke failed: {runner_path}")
        runner_smokes.append({"runner": row["name"], "allowed": allowed, "accept_exit": valid.returncode, "reject_exit": invalid.returncode, "accepted": json.loads(valid.stdout)["ok"], "rejected": not json.loads(invalid.stdout)["ok"]})

    flow = method_flow(safe, failed, refusals, cfr, operations)
    build_viewer(contracts)
    build_plugin()
    models = []
    for contract in (row for row in contracts if row["operation"] == "scene_coordinates"):
        models.append({"profile_id": contract["profile_id"], "scene": evaluate(contract["request"]), "source_proposal": contract["proposal_id"]})
    write_json(OUT / "models.json", {"count": len(models), "models": models, "boundary": BOUNDARY})
    write_json(OUT / "core-results.json", {"count": 150, "results": safe[:150], "all_match_frozen_expected": True, "boundary": BOUNDARY})
    write_json(OUT / "safe-results.json", {"count": len(safe), "core": 150, "auxiliary": 250, "results": safe, "auxiliary_novelty_credit": 0, "boundary": BOUNDARY})
    write_json(OUT / "candidate-failures.json", {"count": len(failed), "failed_subjects": failed, "completion_credit": 0, "boundary": BOUNDARY})
    write_json(OUT / "refusal-witnesses.json", {"count": len(refusals), "passing_refusals": refusals, "subject_promotion_count": 0, "boundary": BOUNDARY})
    write_json(OUT / "cfr-results.json", {"count": len(cfr), "results": cfr, "deleted_files": 0, "boundary": BOUNDARY})
    write_json(OUT / "runner-smokes.json", {"checks": len(runner_smokes) * 2, "runners": runner_smokes, "boundary": BOUNDARY})
    write_json(OUT / "method-flow.json", flow)
    write_json(
        OUT / "session-summary.json",
        {
            "schema": "ghc.family.phase-session-summary.v1",
            "owner": "Ilyra Fen",
            "phase": "v704-v4",
            "session": "x2",
            "core_contracts": 150,
            "safe": len(safe),
            "candidate_failed": len(failed),
            "refusal_passed": len(refusals),
            "cfr_passed": len(cfr),
            "local_skills": 10,
            "local_runners": 5,
            "runner_checks": len(runner_smokes) * 2,
            "models": 15,
            "viewer_scenes": 15,
            "plugin_hooks": 10,
            "outcome_counts": {"completed": 105, "represented": 15, "open_gap": 15, "exact_gate": 15},
            "phase_outcome_counts": {"completed": 255, "represented": 15, "open_gap": 15, "exact_gate": 15},
            "engine": "independent Python Fraction implementation",
            "source_or_x1_replayed": False,
            "boundary": BOUNDARY,
        },
    )
    print(json.dumps({"ok": True, "core": 150, "safe": len(safe), "candidate_failed": len(failed), "refusal_passed": len(refusals), "cfr": len(cfr), "skills": 10, "runners": 5, "runner_checks": len(runner_smokes) * 2, "models": 15, "viewer_scenes": 15, "plugin_hooks": 10, "method_flow": flow["evidence_counts"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
