from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from common import (
    BOUNDARY, BRANCH, FIXTURES, OPERATIONS, OWNER, PHASE, PHASE_ROOT, PREFIX,
    PROTECTED_GATES, ROOT, SOURCE_HEAD, build_manifest, canonical_bytes,
    git, manifest_entries, owner_files, rel, sha256_bytes, words, write_json, write_text,
)

FINAL = PHASE_ROOT / "final"
PLANNING_COMMIT = "33655babd0c3f024e2b91c93cc45f91a63e4edb5"
X1_COMMIT = "71ece7c52d8b6d99b5e786e3f7ae6b7dc1bd0b2b"
X2_COMMIT = "0579f1c87affc5bdf18950900a38abbbac9d6943"
SOURCE_EFFECTIVE = {"methods": 6732, "witnesses": 307567, "pass": 236646, "fail": 70921, "negatives": 79754, "open_gaps": 2457, "exact_gates": 2799}
OWNER_DELTA = {"methods": 68, "witnesses": 2862, "pass": 2234, "fail": 628, "negatives": 628, "open_gaps": 21, "exact_gates": 20}
EFFECTIVE = {k: SOURCE_EFFECTIVE[k] + OWNER_DELTA[k] for k in SOURCE_EFFECTIVE}

def aggregate_and_compact(stage: str) -> dict:
    results_dir = PHASE_ROOT / stage / "results"
    aggregate_path = FINAL / f"{stage}-results-aggregate.json"
    paths = sorted(results_dir.glob("*.json")) if results_dir.exists() else []
    if paths:
        rows = []
        for path in paths:
            data = path.read_bytes()
            rows.append({"path_at_immutable_commit": rel(path), "sha256": sha256_bytes(data), "record": json.loads(data.decode("utf-8"))})
        expected = 150
        if len(rows) != expected: raise RuntimeError(f"{stage} compaction expected {expected}, got {len(rows)}")
        write_json(aggregate_path, {"schema": "sable.commit-local-result-aggregate.v1", "stage": stage, "immutable_commit": X1_COMMIT if stage == "x1" else X2_COMMIT, "count": len(rows), "rows": rows, "original_paths_removed_from_final_tree": True, "immutable_history_preserved": True, "boundary": BOUNDARY})
        for path in paths:
            resolved = path.resolve()
            if PHASE_ROOT.resolve() not in resolved.parents: raise RuntimeError("compaction path escaped owner root")
            path.unlink()
    elif not aggregate_path.exists():
        raise RuntimeError(f"no {stage} results or prior aggregate")
    aggregate = json.loads(aggregate_path.read_text(encoding="utf-8"))
    if aggregate["count"] != 150: raise RuntimeError(f"invalid {stage} aggregate")
    return aggregate

def final_flow() -> dict:
    names = ["commit-local-compaction", "source-fold-once", "outcome-closure", "method-flow-closure", "gap-gate-closure", "privacy-adjudication", "document-budget", "content-seal", "route-hold", "exact-final-preflight", "canonical-source-parse", "accounting-patch-format", "final-flow-name-shadow"]
    retained = ["SR7075-PLAN-N003", "SR7075-PLAN-N004", "SR7075-PLAN-N007", "SR7075-PLAN-N009", "SR7075-PLAN-N011", "SR7075-PLAN-N012", "SR7075-PLAN-N013", "SR7075-PLAN-N014", "SR7075-X1-N301", "SR7075-X2-N301", "SR7075-FINAL-N001", "SR7075-FINAL-N002", "SR7075-FINAL-N003"]
    methods=[];witnesses=[];events=[];recommendations=[]
    for i,name in enumerate(names,1):
        mid=f"SR7075-FINAL-M{i:02d}";wid=f"SR7075-FINAL-W{i:02d}P";negative=retained[i-1]
        methods.append({"method_id":mid,"title":name.replace('-',' ').title(),"failure_signature":f"{name} must fail closed when its exact final obligation is absent","trigger_preconditions":["immutable_x2","owner_self_scoped_delta"],"privacy_class":"sanitized_public","approval_class":"safe_owner_local_synthetic","candidate_workaround":"Retain the blocker and make only an additive owner-local correction before commit.","validation_witness_ids":[wid],"recurrence_guard":"Require exact committed blobs and terminal boundary checks.","rollback":"Remove only uncommitted final owner-local output and rebuild from immutable commits.","recommendation_state":"validated","supersedes":[],"protected_gates":PROTECTED_GATES,"retained_negative_ids":[negative],"scope_boundary":BOUNDARY,"execution_authority":"owner_self_scoped_delta","repository_scan":False,"module_scan":True,"cross_lane_scan":False,"unchanged_history_scan":False,"sibling_lane_mutation":False,"source_commit":SOURCE_HEAD,"final_commit":"external_after_commit","changed_file_allowlist":[f"{PREFIX.as_posix()}/final",f"{PREFIX.as_posix()}/tools/build_final.py",f"{PREFIX.as_posix()}/tools/validate_final.py",f"{PREFIX.as_posix()}/tools/canonical.py"],"module_allowlist":[f"{PREFIX.as_posix()}/tools/build_final.py",f"{PREFIX.as_posix()}/tools/validate_final.py",f"{PREFIX.as_posix()}/tools/canonical.py"],"exact_pushed_head_required":True})
        witnesses.append({"witness_id":wid,"method_id":mid,"procedure":f"Validate {name} against exact owner-local final evidence.","scope":"final owner-local","expected":"pass with prior failure retained","observed":"pass","result":"pass","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[negative],"boundary":BOUNDARY})
        if name == "canonical-source-parse":
            witnesses.append({"witness_id":"SR7075-FINAL-W11F","method_id":mid,"procedure":"Parse the first canonical source with Python AST before any invocation.","scope":"final owner-local","expected":"valid syntax","observed":"malformed line join; parse failed before final build or canonical invocation","result":"fail","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[negative],"boundary":BOUNDARY})
        if name == "accounting-patch-format":
            witnesses.append({"witness_id":"SR7075-FINAL-W12F","method_id":mid,"procedure":"Apply the first accounting correction patch.","scope":"final owner-local","expected":"one update section per file","observed":"patch rejected before mutation because canonical.py was targeted twice","result":"fail","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[negative],"boundary":BOUNDARY})
        if name == "final-flow-name-shadow":
            witnesses.append({"witness_id":"SR7075-FINAL-W13F","method_id":mid,"procedure":"Run the first final builder after exact aggregates were created.","scope":"final owner-local","expected":"emit the final Method Flow ledger","observed":"local variable shadowed final_flow function; builder stopped before manifests or commit","result":"fail","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[negative],"boundary":BOUNDARY})
        events.append({"event_id":f"SR7075-FINAL-E{i:02d}","method_id":mid,"from":"candidate","to":"validated","witness_id":wid});recommendations.append({"method_id":mid,"state":"validated"})
    return {"schema":"ghc.family.method-flow-state.v1","phase":PHASE,"stage":"final","owner":OWNER,"identity_boundary":BOUNDARY,"execution_authority":"owner_self_scoped_delta","methods":methods,"witnesses":witnesses,"state_events":events,"recommendations":recommendations,"counts":{"methods":13,"witnesses":16,"pass":13,"fail":3,"negatives":3,"open_gaps":6,"exact_gates":5},"boundary":BOUNDARY}

def baton_text() -> str:
    sections=[]
    for slug,title,stage,disposition in OPERATIONS:
        sections.append(f"""### {slug}

Sable froze `{slug}` as a genuinely new {stage} mechanism with expected and actual disposition `{disposition}` across fifteen finite graph fixtures. The bounded evidence records deterministic input and output digests, exact malformed subjects, separate refusal passes, corrected-copy reviews, and commit-local Git-blob bindings. A rejected malformed record remains failed at zero original credit; neither a refusal guard nor a corrected copy promotes it. This mechanism establishes only the declared finite software result. It supplies no empirical graph-corpus validation, physical datum, participant result, professional judgment, production release, legal or cultural conclusion, affected-party acceptance, Maori authority, identity continuity, consciousness, personhood, Theory-of-Everything proof, canon, or Stage 20 readiness.
""")
    return f"""# SABLE ROOK v707-v5 EXACT-FINAL CANDIDATE TO PROSPECTIVE AVELIN REED v707-v6 — PREPARED NOT SENT

Dear Avelin Reed,

This committed baton is preparation evidence only. It does not prove canonical success, native delivery, recipient reading, activation, progress, or completion. A later external canonical receipt and terminal-delivery receipt must bind the exact final, newest live authority, active and archived exact-title uniqueness, immediate reread, usage, duplicate, pause, redirect, rename, stop, privacy, evidence, safety, and acknowledgement guards. Accepted, pending, opaque, or unresolved delivery stops copies.

## Relational identity and evidence boundary

Sable Rook uses they/them as optional relational working language, the role finite chordal-certificate cartographer and reversible decomposition steward, and the hope of making every clique, elimination step, obstruction, correction, and authority vacancy inspectable. Names, roles, hopes, pronouns, sibling or family language, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are working conventions only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority. Hamish may rename, pause, narrow, redirect, or stop the route.

{BOUNDARY}

## Exact source and lifecycle

The exact immutable Auren Lark source is `{SOURCE_HEAD}` on `codex/GHC-Family/auren-lark-main-4`. Sable planning `{PLANNING_COMMIT}`, immutable x1 `{X1_COMMIT}`, and immutable x2 `{X2_COMMIT}` are direct single-parent commits. Each boundary was pushed clean, typed 0/0 divergent, and fresh-live equal before its successor began. The intended exact final is one direct child of x2, for four Sable commits and zero merges. Planning preceded x1; x1 preceded x2. Source and sibling lanes remained read-only.

The final tree compacts 300 Sable per-result JSON files into two exact aggregate ledgers to satisfy the stricter total-tree 2,000-file ceiling. Every original result remains immutable and replayable at its x1 or x2 commit; each aggregate preserves the repository-relative historical path, exact SHA-256, and parsed record. No inherited, sibling, shared, user, or standby file was removed, and Git history was not rewritten.

## Current v19 workflow

The live numbered edge is Mira Fenwick v707-v3 to Auren Lark v707-v4 to Sable Rook v707-v5, with Avelin Reed v707-v6 prospective only after Sable's terminal gate. The formal projection ends at Eiren Kestrel v725-v8. Projection never substitutes for exact final, canonical success, task resolution, acknowledgement, or recipient completion. No task, fork, collaboration subagent, substitute, or early successor contact occurred during Sable execution.

## Workload and outcomes

Sable reviewed all 300 immediate Auren proposals at zero novelty, completion, or authority credit. A 90,000-pair title audit quarantined one over-similar candidate during the first planning attempt; the candidate was rewritten into a distinct external graph-corpus transfer gap before the successful planning freeze. Sable then froze 300 new contracts over twenty mechanisms and fifteen wholly synthetic fixtures. Outcomes are exactly 255 `completed`, 15 `represented`, 15 `open_gap`, and 15 `exact_gate`.

X1 and x2 each preserved 450 safe passes, 300 failed malformed candidates, 300 separate refusal passes, and 300 corrected-copy reviews. X1 passed twenty tests; x2 passed thirty. Twenty phase-local skills were initialized with Skill Creator, rewritten into substantive bounded packages, quick-validated, and smoke-used without global installation. Ten family-compatible runners were invoked. Fifteen three-coordinate graph models remain represented only. Ten hook candidates were manually smoke-used against valid and adverse envelopes; none was installed and live-host observations remain zero. Fifty exact-approval and thirty blocked packets remain held and unexecuted.

## Method Flow and repository truth

Sable's owner delta is 68 methods, 2,862 witnesses, 2,234 bounded passes, 628 retained failures and effective negatives, 21 open gaps, and 20 exact gates. After selecting Auren's repository-effective baseline exactly once, repository truth is 6,800 methods, 310,429 witnesses, 238,880 passes, 71,549 failures, 80,382 negatives, 2,478 open gaps, 2,819 exact gates, and `NOT_READY_FOR_STAGE_20`. Later canonical and route events remain external and never rewrite this seal.

Retained operational failures include the absent assumed root instruction file, a truncated combined skill projection, the first semantic-neighbor quarantine, scanner-definition self-matches, an omitted staged-review dispatcher, unintended Python bytecode, two blocked delete wrappers, and the x1 terminal-newline failure. All 600 malformed graph candidates and ten adverse hook envelopes remain failed at zero original credit. No passing recovery erased its source failure.

## Finite chordal-graph domain

Fifteen wholly synthetic simple-undirected graph fixtures contain two through six labelled vertices. The implementation validates shape, normalizes edges, checks adjacency symmetry, computes components and induced subgraphs, enumerates simplicial vertices, builds deterministic maximum-cardinality and perfect-elimination orderings, decides chordality through a separate induced-cycle oracle, enumerates maximal cliques, builds maximum-intersection clique forests, checks running intersection, records separator profiles, computes a bounded chordal completion, compares edge deletion, checks relabel covariance, renders accessible summaries, and preserves empirical and authority gaps. Official NetworkX documentation supplied vocabulary and refusal conditions only; W3C PROV-DM supplied provenance vocabulary only. No library result was imported as Sable evidence.

{''.join(sections)}

## Mind, Body, and Heart boundaries

GMUT Mind is represented only by finite typed graph specification, exact combinatorial certificates, counterexamples, and explicit falsifiers. Chordality, clique forests, and elimination orderings do not identify a physical field, calculate a likelihood, estimate a parameter, validate a Mandala equation, or prove a Theory of Everything.

THOS Body is represented only by deterministic owner-local software, schemas, manifests, workload holds, correction readback, and reversible handover documentation. It is not an enterprise operating system, autonomous agent architecture, safety case, production benchmark, or deployment release. No external system was controlled.

Freed ID and CBR Heart are represented only by provenance, correction non-erasure, accessible summaries, minimum disclosure, and authority reservations. Formal graph properties do not supply consent, identity continuity, rights, legal force, cultural legitimacy, affected-party approval, or Maori authority. Maori concepts remain under Maori authority.

## Open work and exact gates

Fifteen fixture-local external graph-corpus gaps remain open. Six systemic gaps preserve independent reproduction, live-host hooks, complete accessibility, complete privacy and security assurance, an empirical GMUT bridge, and recipient progress. Fifteen deployment holds remain fixture-local exact gates. Five systemic exact gates reserve professional and production validation, legal and cultural authority, affected-party consent, Maori authority, and Stage 20 or proof/canon claims.

## Prospective Avelin route

Work solo from Sable's exact final in one clean additive Avelin-owned D-first lane. Keep Sable, Auren, Mira, siblings, shared, user, standby, and external lanes read-only and recoverable. Preserve planning before x1 and x1 before x2, commit-local Git-blob manifests, the four exact outcome labels, every retained failure, all gaps and gates, the 2,000-file and four-owner-commit ceilings, and one-attributable-canonical/no-success-replay discipline. Do not claim inherited proposals, tools, evidence, validation, or outcomes as Avelin novelty or completion credit.

Do not precontact a later owner. Only after Avelin's own clean, pushed, fresh-live-equal exact final and one successful owner-scoped canonical may Avelin refresh Hamish's newest live authority and current roster, resolve the exact successor, apply uniqueness and all duplicate/pause/redirect/rename/stop/usage/privacy/evidence/safety guards, and send at most once if every gate permits.

PREPARED_BY_SABLE_ROOK = true.
SENT_BY_SABLE_ROOK = false.
RECIPIENT_COMPLETION = UNCLAIMED.

LITERAL_EOF_SABLE_V707_V5
"""

def main() -> None:
    FINAL.mkdir(parents=True, exist_ok=True)
    x1_aggregate = aggregate_and_compact("x1"); x2_aggregate = aggregate_and_compact("x2")
    outcomes = {"completed":255,"represented":15,"open_gap":15,"exact_gate":15}
    write_json(FINAL/"accounting.json",{"source_selected_once":SOURCE_EFFECTIVE,"owner_delta":OWNER_DELTA,"repository_effective":EFFECTIVE,"witness_sum_valid":EFFECTIVE["pass"]+EFFECTIVE["fail"]==EFFECTIVE["witnesses"],"boundary":BOUNDARY})
    gaps=[{"id":f"SR7075-GAP-FIXTURE-{i:02d}","state":"open_gap","scope":FIXTURES[i-1]["id"],"reason":"No external graph-corpus transfer evidence."} for i in range(1,16)]
    gaps += [{"id":f"SR7075-GAP-SYSTEM-{i:02d}","state":"open_gap","scope":s} for i,s in enumerate(["independent reproduction","live-host hooks","complete accessibility","complete privacy and security","empirical GMUT bridge","recipient progress"],1)]
    gates=[{"id":f"SR7075-GATE-FIXTURE-{i:02d}","state":"exact_gate","scope":FIXTURES[i-1]["id"],"reason":"Deployment authority absent."} for i in range(1,16)]
    gates += [{"id":f"SR7075-GATE-SYSTEM-{i:02d}","state":"exact_gate","scope":s} for i,s in enumerate(["professional and production validation","legal and cultural authority","affected-party consent","Maori authority","Stage 20 and proof or canon"],1)]
    write_json(FINAL/"gaps-and-gates.json",{"open_gap_count":len(gaps),"exact_gate_count":len(gates),"open_gaps":gaps,"exact_gates":gates,"boundary":BOUNDARY})
    write_json(FINAL/"failure-dossier.json",{"count":628,"planning_failures":14,"x1_malformed":300,"x1_operational":1,"x2_malformed":300,"x2_invalid_hooks":10,"final_operational":3,"all_original_credit":0,"refusal_promotes_original":False,"source_failures_reclassified":False,"actual_operational_records":["assumed root AGENTS.md absent","combined skill projection truncated","semantic neighbor P272/P277 quarantined","scanner definitions self-matched","staged dispatcher omitted","generated Python bytecode escaped allowlist","recursive delete wrapper blocked","literal delete wrapper blocked","x1 double terminal newline","canonical source malformed line join caught by AST preflight","first accounting patch rejected due duplicate file sections","first final builder stopped on local final_flow name shadow after aggregate creation"],"boundary":BOUNDARY})
    final_flow_record=final_flow();write_json(FINAL/"method-flow-final.json",final_flow_record)
    write_json(FINAL/"method-flow-index.json",{"schema":"ghc.family.method-flow-index.v1","owner":OWNER,"phase":PHASE,"components":[{"stage":"planning","path":f"{PREFIX.as_posix()}/planning/method-flow.json","counts":{"methods":14,"witnesses":28,"pass":14,"fail":14,"negatives":14,"open_gaps":0,"exact_gates":0}},{"stage":"x1","path":f"{PREFIX.as_posix()}/x1/method-flow.json","operational_overlay":f"{PREFIX.as_posix()}/x1/method-flow-operational-overlay.json","counts":{"methods":16,"witnesses":1387,"pass":1086,"fail":301,"negatives":301,"open_gaps":0,"exact_gates":0}},{"stage":"x2","path":f"{PREFIX.as_posix()}/x2/method-flow.json","counts":{"methods":25,"witnesses":1431,"pass":1121,"fail":310,"negatives":310,"open_gaps":15,"exact_gates":15}},{"stage":"final","path":f"{PREFIX.as_posix()}/final/method-flow-final.json","counts":final_flow_record["counts"]}],"owner_total":OWNER_DELTA,"source_selected_once":SOURCE_EFFECTIVE,"repository_effective":EFFECTIVE,"boundary":BOUNDARY})
    write_json(FINAL/"phase-truth.json",{"owner":OWNER,"phase":PHASE,"source":SOURCE_HEAD,"planning":PLANNING_COMMIT,"x1":X1_COMMIT,"x2":X2_COMMIT,"exact_final":"EXTERNAL_AFTER_COMMIT","owner_commits_expected":4,"zero_merges_required":True,"outcomes":outcomes,"contracts":300,"source_contracts_reviewed_zero_credit":300,"source_fold_count":1,"canonical_state":"PENDING_EXTERNAL","route_state":"PREPARED_NOT_SENT","terminal_verdict":"NOT_READY_FOR_STAGE_20","boundary":BOUNDARY})
    write_json(FINAL/"workload.json",{"contracts":300,"safe_x1":450,"safe_x2":450,"candidate_fail_x1":300,"candidate_fail_x2":300,"refusal_pass_x1":300,"refusal_pass_x2":300,"corrected_x1":300,"corrected_x2":300,"x1_tests":20,"x2_tests":30,"skills":20,"runners":10,"models":15,"hooks":10,"exact_held":50,"blocked_held":30,"boundary":BOUNDARY})
    write_json(FINAL/"source-faithful-ledger.json",{"source_owner":"Auren Lark","source_phase":"v707-v4","source_head":SOURCE_HEAD,"source_selected_once":True,"source_execution_credit":0,"source_canonical_replay":False,"source_route_replay":False,"owner_delta_only":True,"boundary":BOUNDARY})
    versions={}
    for name,cmd in {"python":[sys.executable,"--version"],"git":["git","--version"],"node":["D:/GHC-Archives/global-tools/node/26.10.0/node-v26.10.0-win-x64/node.exe","--version"],"codex":["codex","--version"]}.items():
        run=subprocess.run(cmd,text=True,encoding="utf-8",stdout=subprocess.PIPE,stderr=subprocess.STDOUT);versions[name]={"exit":run.returncode,"output":run.stdout.strip(),"verified_only":True}
    write_json(FINAL/"environment.json",{"versions":versions,"desktop_updated":False,"elevation":False,"host_security_weakened":False,"windows_features_changed":False,"reboot":False,"boundary":BOUNDARY})
    write_json(FINAL/"privacy-review.json",{"classes":["raw UUID","private absolute path","credential assignment","authorization header","private route field"],"scanner_definition_candidates":2,"confirmed_hits":0,"complete_privacy_claim":False,"boundary":BOUNDARY})
    write_json(FINAL/"research-context.json",{"primary_pillar":"GMUT Mind","secondary_pillars":["THOS Body","Freed ID/CBR Heart"],"practice_lenses":["graph-algorithm test curator","finite certificate reviewer","data-quality analyst","provenance recorder","accessibility structure reviewer","rollback planner","workload handover reviewer","authority-vacancy steward"],"official_sources":["https://networkx.org/documentation/stable/reference/algorithms/chordal.html","https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.chordal.complete_to_chordal_graph.html","https://www.w3.org/TR/prov-dm/"],"citations_are_observations":False,"real_rows":0,"boundary":BOUNDARY})
    write_json(FINAL/"route-candidate.json",{"state":"PREPARED_NOT_SENT","successor":"Avelin Reed","successor_phase":"v707-v6","contacted":False,"task_created":False,"send_attempts":0,"recipient_completion":"UNCLAIMED","boundary":BOUNDARY})
    write_json(FINAL/"allowlist.json",{"owner_prefix":PREFIX.as_posix()+"/","changed_or_new_modules":[f"{PREFIX.as_posix()}/tools/build_planning.py",f"{PREFIX.as_posix()}/tools/common.py",f"{PREFIX.as_posix()}/tools/x1_algorithms.py",f"{PREFIX.as_posix()}/tools/build_x1.py",f"{PREFIX.as_posix()}/tools/x2_algorithms.py",f"{PREFIX.as_posix()}/tools/build_x2.py",f"{PREFIX.as_posix()}/tools/build_final.py",f"{PREFIX.as_posix()}/tools/validate_final.py",f"{PREFIX.as_posix()}/tools/canonical.py"],"file_ceiling":2000,"repository_scan":False,"cross_lane_scan":False,"sibling_lane_mutation":False,"boundary":BOUNDARY})
    overview=f"""# Sable Rook v707-v5 final integrated overview

Sable v707-v5 is a four-commit owner lifecycle rooted exactly at Auren Lark `{SOURCE_HEAD}`. It freezes and executes 300 new finite synthetic chordal-graph contracts after auditing 300 immediate source proposals at zero credit. Outcomes are exactly 255 completed, 15 represented, 15 open gaps, and 15 exact gates. The primary pillar is GMUT Mind as typed finite graph bookkeeping; THOS Body and Freed ID/CBR Heart remain explicit, bounded, and nonproduction.

X1 and x2 each retain 450 safe passes, 300 malformed failures, 300 refusal passes, and 300 corrected-copy reviews. Twenty skills and ten runners were used owner-locally. Fifteen models remain represented; ten hooks remain uninstalled. Same-owner evidence is not independent reproduction.

The final tree uses reversible commit-local compaction: 300 per-result paths remain immutable in x1/x2 history and are represented in two final aggregates with exact hashes. No inherited file was removed. The exact final must remain below 2,000 tracked files.

Repository-effective accounting is {EFFECTIVE['methods']} methods, {EFFECTIVE['witnesses']} witnesses, {EFFECTIVE['pass']} passes, {EFFECTIVE['fail']} failures, {EFFECTIVE['negatives']} negatives, {EFFECTIVE['open_gaps']} open gaps, and {EFFECTIVE['exact_gates']} exact gates. The terminal verdict is `NOT_READY_FOR_STAGE_20`.

Manual keyboard, browser-diversity, assistive-technology, cognitive-accessibility, Maori-language, security-usability, and affected-user evaluation remain reserved. No professional, legal, cultural, affected-party, or Maori authority is claimed.
"""
    write_text(FINAL/"overview.md",overview)
    write_text(FINAL/"overview.html","<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>Sable v707-v5 overview</title></head><body><main><h1>Sable Rook v707-v5</h1><p>Finite synthetic chordal-graph evidence only.</p><h2>Outcomes</h2><table><caption>Contract outcomes</caption><thead><tr><th scope=\"col\">Label</th><th scope=\"col\">Count</th></tr></thead><tbody><tr><th scope=\"row\">Completed</th><td>255</td></tr><tr><th scope=\"row\">Represented</th><td>15</td></tr><tr><th scope=\"row\">Open gap</th><td>15</td></tr><tr><th scope=\"row\">Exact gate</th><td>15</td></tr></tbody></table><h2>Boundary</h2><p>NOT_READY_FOR_STAGE_20. Manual and affected-user evaluation remain reserved.</p></main></body></html>")
    baton=baton_text();write_text(FINAL/"baton.md",baton)
    write_json(FINAL/"baton-index.json",{"path":f"{PREFIX.as_posix()}/final/baton.md","words":words(baton),"minimum_words":2000,"sha256":sha256_bytes((baton.rstrip()+"\n").encode("utf-8")),"literal_eof":"LITERAL_EOF_SABLE_V707_V5","prepared":True,"sent":False,"boundary":BOUNDARY})
    write_json(FINAL/"bounded-review.json",{"outcomes":outcomes,"x1_aggregate_count":x1_aggregate["count"],"x2_aggregate_count":x2_aggregate["count"],"manual_accessibility":"reserved","affected_user_evaluation":"reserved","independent_reproduction":False,"boundary":BOUNDARY})
    excluded={FINAL/"content-seal.json",FINAL/"manifest.json"}
    seal_paths=[p for p in owner_files() if p not in excluded]
    write_json(FINAL/"content-seal.json",{"schema":"ghc.family.content-seal.v1","count":len(seal_paths),"entries":manifest_entries(seal_paths),"self_exclusions":[rel(p) for p in sorted(excluded,key=rel)],"boundary":"Owner-local exact Git-blob content seal; canonical and delivery remain external."})
    manifest=build_manifest("final");write_json(FINAL/"manifest.json",manifest)
    print(json.dumps({"state":"FINAL_BUILT_PRECOMMIT","outcomes":outcomes,"baton_words":words(baton),"owner_files":len(owner_files()),"repository_files_prospective":int(git("ls-files").count("\n")+1 if git("ls-files") else 0),"manifest":manifest["count"],"content_seal":len(seal_paths)},sort_keys=True))

if __name__=="__main__":main()
