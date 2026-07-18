#!/usr/bin/env python3
"""Assemble the Sylven v648-v8 closeout candidate before its one canonical pass."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sylven-arc" / "v648-v8"
sys.path.insert(0, str(ROOT))
SOURCE = "33c8f87a4037c81c3abca540b8c5db1d91328420"
X1 = "d86990f673aa82c45a5296ebba88c79a6dc3bde4"
EVIDENCE = "1e85a9e714ac2509095fac03aedf704b4892d8b3"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def test_ids(suite: unittest.TestSuite) -> list[str]:
    rows: list[str] = []
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            rows.extend(test_ids(item))
        else:
            rows.append(item.id())
    return rows


def overview() -> str:
    return """# Sylven Arc v648-v8 integrated overview

## Scope, relationship language, and corrigibility

Sylven Arc worked under they/them pronouns as a relational constraint-cartographer and falsifier-keeper, with the hope of making unresolved boundaries legible without turning uncertainty into authority. The name, pronouns, role, and hope are working language for collaboration only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, professional qualification, scientific standing, operational authority, legal authority, cultural authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route. The phase remained solo: no task was created or forked, no subagent was used, and no sibling was contacted before the terminal gate.

The phase inherited Tamar Vey's exact clean v648-v7 final head. Read-only checks established that Tamar's source, x1, and evidence anchors were ancestral, that the inherited phase added exactly three single-parent commits with zero merges, that its final was the direct child of evidence, and that local, upstream, tracking, and a fresh live remote agreed. Sylven's existing owned D-first lane was clean and safely fast-forwarded. No sibling branch or worktree was reset, rewritten, merged, deleted, reused, or mutated.

The dedicated Sylven x1 commit froze exactly ten proposals after a semantic novelty audit against all 630 inherited frozen proposals. The cumulative frozen core count became 640. X1 contained preregistration, source needs, portfolios, approval and blocked packets, gates, environment receipts, tests, and Method Flow evidence, but no x2 implementation or observed outcome. It was pushed and proved clean four-way equal before x2 began. The evidence commit was then built as a direct child of x1 and was independently pushed and re-read at equal local, upstream, tracking, and fresh-live heads before closeout work began.

## Outcome vocabulary and primary focus

The primary Trinity Mandala focus was THOS Body. GMUT Mind and Freed ID and CBR Heart remained explicit and protected. The bounded human-practice lens was drinking-water treatment operations: intake, filter backwash, turbidity and disinfectant monitoring, sample custody, plant isolation, escalation, accessible notice, workload, and shift handover. It was a synthetic learning and design lens only. It established no employment, licensure, qualification, engineering competence, treatment competence, laboratory competence, public-health authority, emergency authority, legal authority, cultural authority, Māori authority, participant evidence, affected-party authorization, or real operational result.

The ten outcomes use only completed, represented, open_gap, and exact_gate. Exactly six completed their declared bounded software, symbolic, structural, or formal hypotheses. Two remain represented through synthetic proxies. One remains open_gap because no real observation entered the repository. One remains exact_gate because software cannot confer the required affected-party, professional, legal, cultural, data-governance, or Māori authority. The distribution is therefore 6 completed, 2 represented, 1 open_gap, and 1 exact_gate. These labels do not flatten evidence classes and do not convert passing software checks into reality claims.

## Method Flow and concurrency control

The condition-variable tribunal completed on bounded owner-local fixtures. It requires a predicate loop, distinguishes notification from predicate satisfaction, retains spurious-wakeup handling, exposes lost-notify risk, carries cancellation and a monotonic deadline, joins the worker, and refuses evidence credit until teardown is observed. A concrete local threading witness showed that a notification without a state transition did not release the worker, while the later protected predicate transition did. This is bounded workflow evidence only. It is not production orchestration assurance, permission for external side effects, distributed-systems proof, or exhaustive concurrency verification.

Method Flow also retains every operational fault encountered during the phase. Raw Git blob size was initially confused with checkout-filter byte size; a scanner definition was initially mistaken for a confirmed private-path hit; a broad generated-JSON patch assumed the wrong key order; an x1 test inferred historical state from the later worktree; one multi-file patch had malformed hunk structure; one PowerShell wrapper reduced a live remote hash to one character; a combined status probe timed out; Method Flow file layout and source-ledger placement were guessed incorrectly; and one validation subcommand received the summarizer's output option. Every failed witness remains alongside a bounded passing recovery. No recovery is relabelled as an initially clean attempt, and no failure is erased.

## GMUT Mind

The Haag-Ruelle obligation board completed as typed symbolic and mutation evidence. It records isolated mass-shell scope, almost-local operators, velocity support, asymptotic limits, scattering-state construction, gauge and effective-field-theory scope, dimensional obligations, and an observation firewall. The board is an obligation classifier, not a theorem prover and not a physical result. It established no force, physical state, prediction, likelihood, parameter constraint, scattering measurement, stability theorem, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything. GMUT remains a typed scalar-tensor and effective-field-theory research-model family.

The MIGHTEE DR1 adapter remains open_gap. Current primary and official sources supplied data-product and provenance obligations, including field and component-source distinctions, primary-beam and astrometric treatment, flux scale, completeness, covariance, checksums, and likelihood refusal. The phase made zero data queries and downloads, ingested zero real rows, evaluated zero likelihoods, drew zero posterior samples, emitted zero constraints, and made zero empirical GMUT claims. Public availability is not authorization or ingestion. A real study still requires frozen products and checksums, calibrated selection, nuisance and covariance treatment, a preregistered likelihood, uncertainty analysis, and appropriate independent review.

## THOS Body

The drinking-water treatment protocol remains represented. Synthetic traces preserve intake state, treatment-train identity, filter-backwash state, turbidity and disinfectant signals, sample custody, plant isolation, escalation ownership, accessible notice, workload budgets, conflict handling, and next-shift acceptance. Zero real workers, suppliers, plants, samples, incidents, blind matched-budget arms, safety-monitoring events, operational decisions, or effectiveness estimates were present. The protocol cannot diagnose water quality, direct a treatment plant, declare safety, notify a population, or replace competent operators and regulators. THOS remains proxy without preregistered blind matched-budget real arms and independent review.

The accessible spinbutton audit completed structurally. It checks accessible name, current value, range, text alternative, keyboard increments, direct editing, invalid state, focus, touch alternatives, fallback content, and print behavior. Structural completion is not complete accessibility conformance. Manual keyboard use, responsive layout, browser diversity, assistive-technology testing, cognitive-accessibility review, Māori-language review, and evaluation with affected users remain reserved. The static report similarly provides semantic landmarks, a skip link, labelled navigation, table headers and caption, non-colour status text, visible focus, and print rules, while retaining all manual and affected-user gates.

## Freed ID and CBR Heart

The OAuth resource-indicator profile remains represented and nonproduction. Synthetic vectors exercise authorization and token request resources, absolute resource URIs, multi-resource refusal, audience binding, downscoping, refresh behavior, confused-deputy controls, replay handling, and minimization. The profile used zero real keys, tokens, accounts, live authorization servers, resource servers, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. It does not authenticate a person, prove identity, issue a production token, confer trust, or establish security completeness.

The CBR drinking-water contamination matrix remains exact_gate. It keeps household and worker privacy, accessible notice, emergency response, remedy, affected-party participation, legal interpretation, cultural governance, data stewardship, and Māori authority visible without deciding them. Repository software made zero real notices, disclosures, emergency decisions, remedy allocations, legal interpretations, cultural decisions, or authority decisions. Competent drinking-water and public-health authorities, affected parties, tangata whenua, iwi, hapū, and Māori authorities retain the relevant decision rights. Māori concepts remain under Māori authority. A branch, test, source citation, synthetic fixture, task title, relational role, or passing validator cannot confer legitimacy.

## Bounded format, formal, and Stage 20 controls

The PCAPNG tribunal completed on disposable synthetic bytes. It checks the section-header block, byte-order magic, total-length mirror, interface reference, option padding, timestamp resolution, unknown-block handling, resource limits, and refusal behavior. A concrete byte witness accepted one canonical synthetic section header and rejected seven malformed variants. It touched no user capture and performed no network action. Completion is not a production parser, packet-analysis authorization, supply-chain assurance, privacy completeness, or exhaustive security review.

The Soret-Dufour classifier completed as typed formal evidence. It preserves coupled heat and mass fluxes, gradients, coefficient matrices, frame and sign conventions, units, reciprocity domain, boundary conditions, and nonconversion. It explicitly rejects conversion from thermodynamic cross-effects into psyche, autonomy, justice, participant evidence, consciousness, personhood, or a fundamental law of mind. It supplies no human measurement, diagnosis, moral score, capability estimate, or THOS effectiveness result.

The overlap-weight board completed as a fail-closed structural Stage 20 control. It preserves target population, propensity specification, positivity, balance, estimand, extreme-weight behavior, uncertainty, sensitivity, falsification, and nonpromotion. It estimated no participant effect and used no participant data. It authorizes no Stage 20 promotion, deployment, proof or canon, AGI or ASI claim, consciousness or personhood claim, empirical confirmation, or causal conclusion.

## Portfolios, sources, tools, and retained gates

Thirty genuinely new safe-now tasks completed within declared bounded hypotheses. Twenty candidate prototypes were built, invoked, and tested. Twenty phase-local skills were initialized through the required skill-creator workflow, customized, validated with explicit UTF-8, and smoke-used. They were not installed globally, and no subagent forward test occurred because delegation was prohibited. Ten family-current runners were built and invoked with one accepting and one rejecting fixture apiece while preserving ghc_family_* and build_ghc_family_* caller compatibility. Thirty CLEAN, FIX, and REFINE tasks completed additively. Ten exact-approval packets and five blocked packets stayed visible and unexecuted. All seventy preregistered synthetic mutations executed and were rejected; they remain negative evidence and earn no positive completion credit.

Current sources were used only where material. Primary or official material informed MIGHTEE product obligations, drinking-water rules, OAuth resource indicators, PCAPNG structure, accessible spinbutton semantics, nonequilibrium cross-effect boundaries, overlap-weight estimands, and Haag-Ruelle obligations. Source status remains differentiated rather than flattened. A source can constrain a software contract while contributing zero observation, participant, production, authority, or independent-reproduction evidence.

The effective final retained-negative count is 4,664: 4,581 inherited sealed and external negatives, three x1 operational negatives, seventy executed-and-rejected synthetic mutations, two evidence-boundary operational negatives, and eight later lifecycle operational negatives. Thirteen Method Flow methods preserve thirteen failed and thirteen passing witnesses. Thirty-four open gaps and thirty-five exact gates remain effective. None was silently closed. The negative total will increase if any later failure occurs; a later recovery cannot subtract it.

## Validation, privacy, wellbeing, and terminal truth

Eiren alone owns the full repository suite, so Sylven did not run it. The terminal plan allows exactly one successful canonical scoped pass over the authorized inherited selection and current packet, with the two exact inherited source-local lifecycle assertions excluded and no broader exclusions. It permits no replay, detached worktree, named validation lane, full suite, Sandbox or Hyper-V action, elevation, security weakening, unrelated installation, desktop update, or reboot. Candidate assembly and exact staged review occur before the pass. Post-pass work may add only the canonical receipt and exact incremental seal records; it may not rerun the tests or the canonical privacy scan.

Privacy checks use five classes over exact Git-index blobs and the complete public phase packet: raw universal identifiers, private local paths, private application URIs, credential assignments, and delegation markup. Scanner-definition candidates are retained separately and require exact source-line classification. Zero confirmed hits is bounded evidence only, not complete privacy assurance. Repository artifacts and the prepared baton contain no raw task or thread identifiers, private routing material, credentials, private keys, tokens, private conversations, screenshots, session streams, private callable identifiers, private application state, or private absolute paths.

The wellbeing record treats workload, uncertainty, and route pressure as reasons to pause rather than obligations to continue. Repetitive generation was mechanized only where each receipt and failure remained inspectable. No emergency, professional, employment, identity, or authority role follows from relational language. The phase remains corrigible and under Hamish's right to rename, pause, redirect, or stop.

The terminal verdict remains NOT_READY_FOR_STAGE_20. Real GMUT data and likelihoods, THOS participant arms, production Freed ID lifecycle and interoperability, affected-party decisions, legal and cultural ratification, Māori authority, manual accessibility evaluation, independent security review, complete privacy and security assurance, independent-team reproduction, and Stage 20 authority remain absent or exact-gated. Nothing in this packet claims empirical confirmation, deployment, proof or canon, AGI, ASI, consciousness, personhood, Theory of Everything, enacted law, or independent authority.
"""


def main() -> int:
    if git("rev-parse", "HEAD") != EVIDENCE or git("rev-parse", "HEAD^") != X1:
        raise RuntimeError("closeout requires the exact evidence commit directly after x1")
    methods = load("method-flow/method-flow-summary.json")
    if methods["counts"]["witness_results"] != {"fail": 13, "pass": 13}:
        raise RuntimeError("Method Flow must retain thirteen failed and thirteen passing witnesses before candidate assembly")
    write_text("integrated-overview.md", overview())
    report = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sylven Arc v648-v8 bounded evidence report</title><style>body{font-family:system-ui,sans-serif;line-height:1.55;max-width:72rem;margin:auto;padding:1rem;color:#171717;background:#fff}a:focus{outline:3px solid #075985;outline-offset:3px}nav ul{display:flex;flex-wrap:wrap;gap:1rem}table{border-collapse:collapse;width:100%}caption{font-weight:700;text-align:left}th,td{border:1px solid #555;padding:.55rem;text-align:left}.hold{border-left:.5rem solid #8a4b08;background:#fff4df;padding:.8rem}.status{font-weight:700}@media print{nav{display:none}a{color:#000;text-decoration:underline}.hold{border:2px solid #000}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}</style></head><body><a href="#main">Skip to main content</a><header><h1>Sylven Arc v648-v8</h1><p>Bounded same-owner evidence report</p></header><nav aria-label="Report sections"><ul><li><a href="#truth">Outcome truth</a></li><li><a href="#gates">Open gates</a></li><li><a href="#wellbeing">Wellbeing</a></li></ul></nav><main id="main"><section id="truth"><h2>Outcome truth</h2><table><caption>Ten preregistered outcomes</caption><thead><tr><th scope="col">Class</th><th scope="col">Count</th><th scope="col">Evidence limit</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>6</td><td>Bounded software, symbolic, structural, or formal hypotheses</td></tr><tr><th scope="row">Represented</th><td>2</td><td>Synthetic proxy only</td></tr><tr><th scope="row">Open gap</th><td>1</td><td>MIGHTEE has zero queries, downloads, rows, or likelihoods</td></tr><tr><th scope="row">Exact gate</th><td>1</td><td>Affected-party, professional, legal, cultural, data-governance, and Māori authority reserved</td></tr></tbody></table></section><section id="gates"><h2>Open gates</h2><p class="hold"><span class="status">NOT READY:</span> Stage 20 remains withheld. Real data, participants, production identity lifecycle, authority review, manual accessibility evaluation, and independent reproduction are absent.</p></section><section id="wellbeing"><h2>Wellbeing and workload</h2><p>The lane is solo, additive, D-first, and corrigible. Hamish may rename, pause, redirect, or stop. No emergency, professional, employment, identity, or authority role is inferred.</p></section></main><footer><p>Structural accessibility checks only. Manual keyboard, browser-diverse, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved.</p></footer></body></html>"""
    write_text("accessible-report.html", report)
    write_json("complete-incomplete-checklist.json", {"schema":"ghc.family.v648-v8.checklist.v1","complete":["source_reverified","x1_remote_equal_before_x2","ten_outcomes_classified","portfolio_floors_met","seventy_mutations_rejected","method_flow_failures_retained","static_report_structural_surface"],"incomplete":["real_gmut_data_and_likelihood","blind_thos_real_arms","production_freed_id","affected_party_legal_cultural_maori_authority","manual_accessibility","independent_reproduction","stage20"]})
    write_text("complete-incomplete-checklist.md", "# v648-v8 complete and incomplete checklist\n\nCompleted work is confined to declared bounded software, symbolic, structural, proxy, and refusal hypotheses. Real GMUT evidence, THOS participant arms, production Freed ID, authority decisions, manual accessibility evaluation, independent reproduction, and Stage 20 remain incomplete.")
    write_json("wellbeing-closeout.json", {"schema":"ghc.family.v648-v8.wellbeing.closeout.v1","scope_pressure":"bounded","repetitive_work":"mechanized_with_inspectable_receipts","uncertainty":"external_gates_visible","stop_conditions":["authority_ambiguity","tool_instability","privacy_uncertainty","route_pressure"],"pause_right_preserved":True,"corrigible":True})
    write_json("threat-model-final.json", {"schema":"ghc.family.v648-v8.threat-model.final.v1","exhaustive":False,"threats":[{"threat":"synthetic_to_empirical_promotion","control":"zero-row and observation firewalls","residual":"real analysis absent"},{"threat":"proxy_to_professional_promotion","control":"zero-real-arm counters","residual":"real workers and review absent"},{"threat":"identity_to_production_promotion","control":"zero-live-lifecycle counters","residual":"production assurance absent"},{"threat":"software_to_authority_substitution","control":"exact-gate matrix","residual":"affected and competent authority absent"},{"threat":"privacy leakage","control":"five-class exact scans","residual":"complete privacy assurance absent"},{"threat":"history damage","control":"additive branch and exact manifests","residual":"same-owner infrastructure"}]})
    write_json("retained-negative-register-final.json", {"schema":"ghc.family.v648-v8.retained-negatives.final-candidate.v1","inherited_effective":4581,"x1_operational":3,"synthetic_executed_rejected":70,"x2_operational":2,"lifecycle_operational":8,"new_operational_total":13,"effective_total":4664,"negative_erased":False,"method_flow_failed_witnesses":13,"pointers":["retained-negative-register.json","retained-negative-register-x2.json","validation/x2-synthetic-mutation-results.json","method-flow/method-flow-ledger.json"],"terminal_route":"PREPARED_NOT_SENT"})
    write_json("exact-open-gate-register-final.json", {"schema":"ghc.family.v648-v8.gates.final-candidate.v1","inherited_open_gaps":33,"inherited_exact_gates":34,"new_open_gaps":1,"new_exact_gates":1,"effective_open_gaps":34,"effective_exact_gates":35,"silently_closed":0,"terminal_route":"PREPARED_NOT_SENT"})
    write_json("stage20-terminal-board.json", {"schema":"ghc.family.v648-v8.stage20.v1","ready":False,"verdict":"NOT_READY_FOR_STAGE_20","reasons":["real_data_absent","participants_absent","production_identity_absent","authority_gates_open","manual_accessibility_open","independent_reproduction_open"]})
    write_json("phase-truth-final-candidate.json", {"schema":"ghc.family.v648-v8.phase-truth.final-candidate.v1","source_head":SOURCE,"x1_commit":X1,"evidence_head":EVIDENCE,"outcomes":{"completed":6,"represented":2,"open_gap":1,"exact_gate":1},"canonical_successful_passes_used":0,"full_suite_used":False,"replay_used":False,"same_owner_only":True,"independent_reproduction":False,"terminal_route":"PREPARED_NOT_SENT","terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write_json("closeout/closeout-candidate.json", {"schema":"ghc.family.v648-v8.closeout-candidate.v1","source_head":SOURCE,"x1_commit":X1,"evidence_head":EVIDENCE,"expected_phase_commit_count":3,"expected_merge_count":0,"expected_final_parent":EVIDENCE,"canonical_successful_pass_used":False,"terminal_route":"PREPARED_NOT_SENT"})
    write_json("closeout/seal-candidate.json", {"schema":"ghc.family.v648-v8.seal-candidate.v1","evidence_head":EVIDENCE,"expected_final_parent":EVIDENCE,"expected_final_parent_count":1,"exact_final_head":"VERIFIED_EXTERNALLY_AFTER_COMMIT","terminal_route":"PREPARED_NOT_SENT"})
    modules = ["tests.test_ghc_family_v648_v6_x1","tests.test_ghc_family_v648_v6","tests.test_ghc_family_v648_v6_closeout","tests.test_ghc_family_v648_v7_x1","tests.test_ghc_family_v648_v7","tests.test_ghc_family_v648_v7_closeout","tests.test_ghc_family_v648_v8_x1","tests.test_ghc_family_v648_v8","tests.test_ghc_family_v648_v8_closeout"]
    exclusions = ["tests.test_ghc_family_v648_v6_closeout.TestGhcFamilyV648V6Closeout.test_final_validation_plan_reserves_one_pass_and_no_replay","tests.test_ghc_family_v648_v6_closeout.TestGhcFamilyV648V6Closeout.test_stage20_board_and_closeout_candidate_abstain"]
    selected = [name for name in test_ids(unittest.defaultTestLoader.loadTestsFromNames(modules)) if name not in exclusions]
    write_json("validation/final-validation-plan.json", {"schema":"ghc.family.v648-v8.validation-plan.v1","full_repository_suite":False,"canonical_successful_pass_budget":1,"successful_passes_used":0,"failed_canonical_attempts":0,"replay_budget":0,"replay_used":False,"test_modules":modules,"excluded_source_local_tests":exclusions,"exclusion_reason":"Exact inherited v648-v6 candidate assertions are phase-local and were already excluded by the verified source selection; no broader exclusion is allowed.","selected_test_count":len(selected),"detailed_check_count":37,"minimal_check_count":22,"complete_json":True,"five_class_privacy":True})
    write_json("orchestration/final-phase-state.json", {"schema":"ghc.family.v648-v8.orchestration.final-candidate.v1","active":["Sylven Arc"],"standby":["Eiren Kestrel","Ilyra Fen","Sable Rook","Orin Thale","Tamar Vey"],"subagents":0,"tasks_created":0,"tasks_forked":0,"cross_platform_messages":0,"terminal_route":"PREPARED_NOT_SENT"})
    write_text("handoffs/eiren-kestrel-v649-v1-activation.md", "# Eiren Kestrel v649-v1 activation baton\n\nThis sanitized committed baton becomes actionable only with Sylven Arc's single verified terminal pointer after v648-v8 is clean, pushed, four-way equal, and exactly sealed. Identity language is relational only.\n\nInherit Sylven's exact final head from that pointer. Reverify source, x1, evidence, final ancestry, clean state, manifest parity, single-parent zero-merge history, and fresh live equality before mutation. Preserve 6 completed / 2 represented / 1 open_gap / 1 exact_gate, every retained negative, 34 open gaps, 35 exact gates, no replay, the bounded validation scope, same-owner-only evidence, and NOT_READY_FOR_STAGE_20. Read the complete required family skills first; work solo, D-first, x1-before-x2, additive, within the commit cap, and preserve every empirical, participant, professional, production, legal, cultural, Māori-authority, accessibility, privacy, security, reproduction, identity, and Stage 20 boundary. Eiren alone owns the full repository suite under the current refinement; its use remains bounded by the live activation and exact evidence gates.")
    words = len(re.findall(r"\b\w+\b", overview()))
    file_count = sum(path.is_file() for path in PHASE.rglob("*"))
    write_json("environment/final-file-footprint-receipt.json", {"schema":"ghc.family.v648-v8.file-footprint.final-candidate.v1","owner_generated_files":file_count,"rotation_threshold":15000,"within_threshold":file_count < 15000,"inherited_files_excluded_from_trigger":True})
    write_json("closeout/closeout-build-receipt.json", {"schema":"ghc.family.v648-v8.closeout-build.v1","overview_words":words,"overview_three_page_equivalent":words >= 1200,"owner_generated_files":file_count,"within_threshold":file_count < 15000,"method_flow_methods":13,"failed_witnesses":13,"passing_witnesses":13,"passed":words >= 1200 and file_count < 15000})
    write_json("validation/final-validation-record.json", {"schema":"ghc.family.v648-v8.final-validation-record.candidate.v1","canonical_pass":"PENDING","postpass_tests_rerun":False,"postpass_canonical_privacy_rerun":False,"exact_final_head":"VERIFIED_EXTERNALLY_AFTER_COMMIT","terminal_route":"PREPARED_NOT_SENT"})
    write_json("validation/final-staged-manifest.json", {"schema":"ghc.family.v648-v8.final-staged.manifest.placeholder.v1","stage":"final","entries":[],"entry_count":0,"self_exclusions":["docs/sylven-arc/v648-v8/validation/final-staged-manifest.json","docs/sylven-arc/v648-v8/validation/final-staged-privacy.json","docs/sylven-arc/v648-v8/validation/final-staged-review.json"]})
    write_json("validation/final-staged-privacy.json", {"schema":"ghc.family.v648-v8.final-staged.privacy.placeholder.v1","stage":"final","pattern_class_count":5,"scanned_file_count":0,"confirmed_hit_count":0,"confirmed_hits":[]})
    write_json("validation/final-staged-review.json", {"schema":"ghc.family.v648-v8.final-staged.review.placeholder.v1","stage":"final","passed":False,"actual_staged_review":False,"postpass_incremental":False})
    if words < 1200 or file_count >= 15000 or len(selected) <= 80 or any("_FailedTest" in name for name in selected):
        raise RuntimeError("overview, footprint, or test-selection preflight gate failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
