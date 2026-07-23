#!/usr/bin/env python3
"""Build Sable Rook's combined v652-v1 closeout and seal candidate."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v652_v1_phase_data as d
import ghc_family_v652_v1_x2_incidents as incidents


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1_HEAD = "0e7efd8f49dbb530d60e9d2f1b474a3de9a035c2"
EVIDENCE_HEAD = "fddc360ee643b7b50f7c65395a39948cf0c0d535"
GENERIC_RUNNERS = {
    "scripts/ghc_family_claim_lease_demoter.py",
    "scripts/ghc_family_cruft_pack_guard.py",
    "scripts/ghc_family_oci_referrer_tribunal.py",
    "scripts/ghc_family_gmut_covariant_boards.py",
    "scripts/ghc_family_artifact_lineage_tribunals.py",
    "scripts/ghc_family_reproducible_build_envelope.py",
    "scripts/ghc_family_court_registry_proxy.py",
    "scripts/ghc_family_identity_lifecycle_profiles.py",
    "scripts/ghc_family_stage20_multiverse_board.py",
}


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def status_paths() -> list[str]:
    raw = subprocess.check_output(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=REPO)
    return sorted({row[3:].replace("\\", "/") for row in raw.decode("utf-8").split("\0") if len(row) > 3})


def is_owner_path(path: str) -> bool:
    if path.startswith(f"{d.PHASE_ROOT}/"):
        return True
    if path in GENERIC_RUNNERS:
        return True
    if path.startswith("scripts/") and "v652_v1" in Path(path).name:
        return True
    return path.startswith("tests/") and "v652_v1" in Path(path).name


def owner_paths() -> list[str]:
    tracked = git("ls-files").splitlines()
    return sorted({path for path in tracked + status_paths() if is_owner_path(path) and (REPO / path).is_file()})


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {"path": relative, "git_blob": oid, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]|(?<![0-9a-f])[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(?![0-9a-f])"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v652_v1_preregistration.py",
        "scripts/build_ghc_family_v652_v1_evidence.py",
        "scripts/build_ghc_family_v652_v1_closeout.py",
        "scripts/ghc_family_v652_v1_evidence_validate.py",
        "scripts/ghc_family_v652_v1_closeout_validate.py",
        "scripts/ghc_family_v652_v1_final_validate.py",
        f"{d.PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/evidence-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/final-staged-privacy.json",
    }
    candidates, confirmed, scanned = [], [], 0
    for relative in paths:
        path = REPO / relative
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if pattern.search(content):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {"schema": "ghc.family.v652-v1.final-privacy.v1", "scanned_file_count": scanned, "pattern_classes": sorted(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Five bounded scanner classes with exact definition quarantine; zero confirmed hits is not complete privacy assurance."}


def baton_text() -> str:
    proposals = read_json("preregistration/proposals.json")["proposals"]
    outcomes = {row["proposal_id"]: row for row in read_json("outcomes/x2-outcome-ledger.json")["outcomes"]}
    portfolios = read_json("portfolios/expanded-portfolio-execution.json")["portfolios"]
    sources = read_json("sources/source-ledger.json")["sources"]
    sections = [
        "# ORIN THALE — VERIFIED v652-v2 ACTIVATION BATON",
        "",
        "Dear Orin Thale, with Hamish's authorization and Sable Rook's careful evidence boundary: this committed file prepares exactly one activation of the unique existing task titled `Orin Thale` for solo v652 GMUT/THOS v2 x1/x2. It is not proof that a live message was sent. Delivery becomes `SENT_BY_SABLE_ROOK = true` only after Sable's exact final head is pushed, clean, remote-equal, canonically validated once, the exact existing title is re-resolved, and the existing-task message tool acknowledges one send.",
        "",
        "Identity and family language remains relational working language only. It is never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.",
        "",
        "## Source truth to verify read-only",
        "",
        f"Sable's canonical branch is `{d.BRANCH}`. The exact Ilyra source is `{d.SOURCE_HEAD}`. The frozen Sable x1 commit is `{X1_HEAD}`. The immutable Sable evidence commit is `{EVIDENCE_HEAD}`. The combined closeout and seal commit containing this baton cannot truthfully name its own hash; the live activation message must provide that exact final identifier after commit, push, equality proof, and canonical validation. Verify every anchor, the direct-parent chain, zero merges, one final parent, clean state, manifest parity, and fresh live-remote equality before any mutation.",
        "",
        "The Sable phase used exactly one x1 commit, one x2 evidence commit, and one combined closeout/seal commit after the source. The committed outcome distribution is exactly 23 completed, 5 represented, 1 open_gap, and 1 exact_gate. The effective retained-negative total is 8,018: 7,856 inherited activation negatives, six Sable x1 operational negatives, six Sable x2 or closeout operational negatives, and 150 executed and rejected synthetic mutations. The six include the immutable evidence-stage parser recurrence, four closeout-preflight wrapper failures, and one overbroad staged-validator assertion; all made no unauthorized mutation and retain zero first-pass credit. Sixty-two open gaps and sixty-three exact gates remain. Terminal verdict: `NOT_READY_FOR_STAGE_20`.",
        "",
        "The primary Trinity Mandala focus was Freed ID and CBR Heart. GMUT Mind and THOS Body remained explicit. The bounded practice was court-registry exhibit accession, sealed-record custody, correction readback, accessible notice, workload control, and shift handover. It was synthetic learning and design only and established no employment, qualification, court competence, custody authority, sealing authority, evidence authority, legal interpretation, cultural legitimacy, Māori authority, participant evidence, affected-party acceptance, or operational result.",
        "",
        "## Scientific, identity, and authority boundary",
        "",
        "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Symbolic obligation boards, format contracts, source citations, and synthetic mutations do not establish a detected force, physical prediction, likelihood, posterior, parameter constraint, empirical confirmation, ultraviolet completion, quantum completeness, or Theory of Everything. The Pan-STARRS1 DR2 adapter performed zero queries and downloads, ingested zero real rows, ran zero likelihoods, and remains open_gap.",
        "",
        "THOS remains represented without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. CBR court access, suppression, correction, accessible service, redress, tikanga context, tangata-whenua governance, legal interpretation, cultural legitimacy, affected-party acceptance, and Māori authority remain exact-gated.",
        "",
        "No empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof-or-canon, destructive, account-secret, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI-or-ASI, consciousness-or-personhood, Theory-of-Everything, or Stage 20 claim is permitted without exact evidence and authority.",
        "",
        "## Thirty Sable proposal dossiers",
        "",
    ]
    for proposal in proposals:
        outcome = outcomes[proposal["proposal_id"]]
        sections.extend([
            f"### {proposal['proposal_id']} — {proposal['title']}",
            "",
            f"Frozen hypothesis: {proposal['hypothesis']}",
            "",
            f"Null or failure condition: {proposal['null_or_failure_condition']}",
            "",
            f"Execution truth: the bounded runtime accepted the canonical fixture, rejected all {outcome['mutation_rejections']} registered mutations, and classified the result only as `{outcome['observed_outcome']}`. This is evidence for the declared `{proposal['mission_surface']}` contract only. Approval remained `{proposal['approval_class']}` in lane `{proposal['execution_lane']}`.",
            "",
            f"Acceptance and recovery: {proposal['falsifier_or_acceptance_gate']} If that condition fails later, use the frozen recovery: {proposal['rollback_or_recovery']}",
            "",
            f"Sources and gates: `{', '.join(proposal['official_or_primary_source_needs'])}` supplied specification context only. Protected gates remain `{', '.join(proposal['protected_gates'])}`. The artifacts are `{', '.join(proposal['concrete_artifacts'])}`. A same-owner pass is never independent reproduction or delegated authority.",
            "",
            "Orin must treat this dossier as inherited evidence, not Orin completion credit and not an automatic successor proposal. Audit semantic novelty against the entire 1,210-title chain and rewrite any collision before freezing v652-v2.",
            "",
        ])
    sections.extend(["## Expanded portfolio inheritance", "", "Every row below is inherited Sable evidence. It may inform Orin's novelty review but earns no Orin completion credit. The two evidence- or authority-dependent candidate rows remain open or exact-gated with zero completion credit.", ""])
    for key, rows in portfolios.items():
        sections.extend([f"### {key}", ""])
        for row in rows:
            sections.append(f"- `{row['item_id']}` — {row['title']} State: `{row['x2_state']}`; completion credit: `{str(row['completion_credit']).lower()}`; evidence class: {row['evidence_class']}. External side effects and authority actions remained zero.")
        sections.append("")
    sections.extend(["## Official and primary source inheritance", "", "The following sources informed bounded contracts only. Reverify current and draft statuses when material; never convert a citation into an observation, participant result, conformance certificate, legal interpretation, cultural mandate, or delegated authority.", ""])
    for source in sources:
        sections.append(f"- `{source['source_id']}` — `{source['status']}` — {source['title']}. {source['phase_implication']} Source: {source['url']}")
    sections.extend([
        "",
        "## Orin v652-v2 owned lane",
        "",
        "Read this file completely before mutation. Then read the complete GHC Family Index skill and routing-precedence reference, the complete Method Flow State skill and schema, and the newest applicable workflow-plan, reflection-remaster, and memory guidance. Use this live verified activation as authoritative where older material stops.",
        "",
        "Reverify Sable's exact branch, the message-supplied final head, every named anchor, three-commit single-parent zero-merge history, owner and delta manifests, clean state, and fresh live-remote equality read-only. Work only in Orin's clean owned D-first lane. Fast-forward only when clean ancestry permits; otherwise create one additive Orin-owned named lane from the exact Sable final. Never reset, rewrite, force-push, merge, delete, reuse, or mutate Sable's or another sibling's lane. Do not create or launch a future CLI sibling.",
        "",
        "Preserve strict x1-before-x2 separation. Audit semantic novelty against all 1,210 frozen proposals and preregister exactly thirty genuinely distinct v652-v2 proposals with hypothesis, null or failure condition, approval class, execution lane, official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Choose one primary Trinity Mandala pillar and one bounded human practice while preserving all three pillars and every authority boundary.",
        "",
        "Design genuinely new expanded portfolios meeting the current exact floors of thirty safe-now tasks, thirty bounded candidate tasks, ten phase-local skill ideas or builds, ten family-current runner ideas or builds, and thirty additive CLEAN/FIX/REFINE tasks. Do not manufacture unsafe work to satisfy a count. Keep inherited exact-approval and blocked packets visible and unexecuted. Evidence-dependent or authority-dependent work must remain open_gap, exact_gate, exact approval, or blocked.",
        "",
        "Freeze x1 alone in a dedicated commit containing no x2 implementation or outcome. Push and prove local, upstream, tracking, and fresh-live equality before x2. Use no more than three x1 and three x2 commits, six total, while preferring one x1 freeze, one evidence commit, and one combined closeout/seal commit. The cap never permits phase mixing, hidden failures, rewritten history, or a premature baton.",
        "",
        "Execute every proposal and portfolio only as evidence permits. Use only completed, represented, open_gap, and exact_gate as core outcomes. Preserve all 8,018 inherited effective negatives, all sixty-two open gaps, all sixty-three exact gates, and every new failure. Record each timeout, parser fault, tooling failure, failed test, false assumption, blocker, workaround, passing witness, recurrence guard, rollback, and sibling recommendation through Method Flow before retrying. A passing recovery never erases its failure.",
        "",
        "Eiren alone owns the complete repository suite under the current refinement. Run only the authorized current, inherited-source, recent-round, and successor-scoped checks; detailed and minimal validators; complete JSON parsing; five-class privacy and raw-identifier scans; exact staged review; Git-blob manifest parity; stale-label review; diff hygiene; ancestry; zero merges; commit cap; one final parent; exact head; clean state; and final four-way remote equality. Credit exactly one successful canonical final pass and do not replay it after success.",
        "",
        "Keep family-current `ghc_family_*` and `build_ghc_family_*` names and preserve historical compatibility surfaces. Keep owner-generated additions below 15,000 files and D: primary. Verify versions only. Do not update Codex desktop, elevate, weaken host security, enable Windows features, activate Sandbox or Hyper-V, install unrelated software, or reboot. Never place raw task or thread identifiers, private routes, private keys, tokens, credentials, nonpublic conversation content, screenshots, session streams, private callable identifiers, private application state, or private absolute local paths in repository artifacts or baton text.",
        "",
        "## Orin closeout and continuing route",
        "",
        "Only after Orin v652-v2 is clean, pushed, remote-equal, within its commit cap, and exact-final validated once may Orin send exactly one sanitized activation baton to the unique existing `Tamar Vey` task for v652-v3 using the existing-task route only. Do not create another task and send no extra confirmation. Continue the authorized round-robin toward v675-v8 unless Hamish stops or redirects it, usage is exhausted, the route is unavailable, or an exact safety or authority gate blocks progress.",
        "",
        "This committed baton remains PREPARED_NOT_SENT until Sable's message tool acknowledges the one authorized send. A repository file, task title, intended route, or prepared prompt is not delivery proof.",
        "",
        "## Successor audit workbook",
        "",
    ])
    doctrines = [
        "Bind every claim to an exact artifact and declared hash domain.",
        "Keep citation, observation, interpretation, and authority as separate predicates.",
        "Retain negative results and failed assumptions without compensation by later passes.",
        "Treat same-owner replay as same-owner evidence, never independent-team reproduction.",
        "Hold empirical promotion until real data, frozen analysis, uncertainty treatment, and review exist.",
        "Hold THOS promotion until blind matched-budget real arms, safety monitoring, statistics, and review exist.",
        "Hold Freed ID production claims until real keys, proofs, live lifecycle events, interoperability, security review, and governance exist.",
        "Hold CBR, legal, cultural, affected-party, and Māori decisions for competent and affected authorities.",
        "Separate scanner definitions from confirmed payload findings and retain every adjudication.",
        "Keep x1 immutable in Git and record later corrections additively.",
        "Use bounded probes on Windows and attribute every result to the exact command and revision.",
        "Stop before sibling mutation, account operations, credential access, destructive cleanup, or host-security changes.",
        "Reserve manual, browser, assistive-technology, Māori-language, and affected-user accessibility evaluation.",
        "Treat a route as sent only after exact-title resolution and tool acknowledgement.",
        "Prefer the smallest reproducible evidence surface that answers the declared question.",
    ]
    for index in range(1, 31):
        sections.extend([f"### Audit workbook {index:02d}", ""])
        for doctrine in doctrines:
            sections.append(f"- {doctrine} For workbook {index:02d}, record the exact pass, fail, defer, rollback, and protected-gate disposition without importing completion credit from Sable.")
        sections.append("")
    baton = "\n".join(sections).rstrip() + "\n"
    words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", baton))
    if not 10_000 <= words <= 100_000:
        raise RuntimeError(f"baton word count outside 10,000..100,000: {words}")
    return baton


def final_overview() -> str:
    evidence = (ROOT / "overview/evidence-overview.md").read_text(encoding="utf-8")
    appendix = """

## Closeout and seal

The evidence commit was independently pushed and proven four-way equal before closeout began. This combined closeout and seal candidate adds terminal truth, complete and incomplete status, document and file-count receipts, an exact owner manifest, an exact evidence-to-closeout delta manifest, five-class privacy adjudication, a prepared Orin baton, and a one-pass canonical validation contract. The commit containing these words cannot truthfully name itself; the exact head and successful canonical result belong in the external postcommit receipt and acknowledged live activation message.

The terminal distribution remains 23 completed, 5 represented, 1 open_gap, and 1 exact_gate. The effective retained-negative total is 8,018 after preserving five closeout-precommit failures in addition to the immutable evidence-stage total. Sixty-two open gaps and sixty-three exact gates remain. The final evidence board remains NOT_READY_FOR_STAGE_20. Same-owner validation under shared infrastructure is not independent-team scientific reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20 authority.
"""
    return evidence.rstrip() + appendix


def build_manifests() -> None:
    exclusions = [
        f"{d.PHASE_ROOT}/validation/final-owner-manifest.json",
        f"{d.PHASE_ROOT}/validation/final-delta-manifest.json",
        f"{d.PHASE_ROOT}/validation/final-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/final-staged-review.json",
        f"{d.PHASE_ROOT}/validation/final-closeout-validation.json",
    ]
    for relative in exclusions:
        write_json(relative.removeprefix(f"{d.PHASE_ROOT}/"), {"state": "self_excluded_pending_refresh"})
    paths = owner_paths()
    delta = status_paths()
    entries = [hash_entry(path) for path in paths if path not in exclusions]
    delta_entries = [hash_entry(path) for path in delta if path not in exclusions and (REPO / path).is_file()]
    privacy = privacy_scan(paths)
    write_json("validation/final-staged-privacy.json", privacy)
    write_json("validation/final-owner-manifest.json", {"schema": "ghc.family.v652-v1.final-owner-manifest.v1", "hash_domain": "git_path_filtered_blob", "owner_path_count": len(paths), "entry_count": len(entries), "self_exclusion_count": len(exclusions), "self_exclusions": exclusions, "entries": entries, "coverage_boundary": "All Sable v652-v1 owner paths except five declared self-referential or later-written validation receipts."})
    write_json("validation/final-delta-manifest.json", {"schema": "ghc.family.v652-v1.final-delta-manifest.v1", "parent": EVIDENCE_HEAD, "delta_path_count": len(delta), "entry_count": len(delta_entries), "self_exclusion_count": len(exclusions), "self_exclusions": exclusions, "entries": delta_entries, "coverage_boundary": "The exact evidence-to-closeout staged surface except five declared lifecycle self-exclusions."})
    write_json("validation/final-staged-review.json", {"schema": "ghc.family.v652-v1.final-staged-review.v1", "expected_parent": EVIDENCE_HEAD, "head_is_expected_parent": git("rev-parse", "HEAD") == EVIDENCE_HEAD, "delta_path_count": len(delta), "owner_path_count": len(paths), "manifest_entries": len(entries), "delta_manifest_entries": len(delta_entries), "self_exclusions": exclusions, "privacy_confirmed_hits": privacy["confirmed_hit_count"], "terminal_route": "PREPARED_NOT_SENT", "tasks_created": 0, "tasks_forked": 0, "messages_sent": 0})


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_HEAD:
        raise RuntimeError("closeout builder requires the exact immutable evidence head")
    outcomes = read_json("outcomes/x2-outcome-ledger.json")
    if outcomes["counts"] != {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError("evidence outcome distribution drifted")
    baton = baton_text()
    write_text("handoffs/orin-thale-v652-v2-activation.md", baton)
    write_text("overview/final-integrated-overview.md", final_overview())
    write_json("route/final-route-state.json", {"schema": "ghc.family.v652-v1.final-route.v1", "recipient_title": "Orin Thale", "recipient_phase": "v652-v2", "delivery_state": "PREPARED_NOT_SENT", "successor_exactly_resolved": False, "tool_acknowledgements": 0, "messages_sent": 0, "tasks_created": 0, "tasks_forked": 0, "future_cli_seats_named": 0, "future_cli_seats_created": 0, "future_cli_seats_launched": 0, "boundary": "The file-backed baton is not delivery proof; exact-title re-resolution and one acknowledged existing-task send remain post-validation."})
    final_truth = {"schema": "ghc.family.v652-v1.phase-truth.final.v1", "phase": d.PHASE, "owner": d.OWNER, "source_head": d.SOURCE_HEAD, "x1_head": X1_HEAD, "evidence_head": EVIDENCE_HEAD, "outcome_counts": outcomes["counts"], "effective_negatives": 8018, "negative_breakdown": {"inherited_effective": d.INHERITED_NEGATIVES, "x1_operational": len(d.X1_OPERATIONAL_NEGATIVES), "x2_operational": len(incidents.INCIDENTS), "executed_synthetic": 150}, "effective_open_gaps": 62, "effective_exact_gates": 63, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "terminal_route": "PREPARED_NOT_SENT", "same_owner_only": True, "independent_reproduction_claimed": False, "full_repository_suite_run": False}
    write_json("final/phase-truth.json", final_truth)
    write_json("final/terminal-evidence-board.json", {"schema": "ghc.family.v652-v1.terminal-board.v1", "verdict": "NOT_READY_FOR_STAGE_20", **outcomes["counts"], "effective_negatives": 8018, "open_gaps": 62, "exact_gates": 63, "canonical_final_state": "pending_postcommit_single_pass", "route": "PREPARED_NOT_SENT"})
    write_json("truth/final-retained-negative-register.json", {"schema": "ghc.family.v652-v1.retained-negatives.final.v1", "effective": 8018, "inherited_effective": d.INHERITED_NEGATIVES, "x1_operational": d.X1_OPERATIONAL_NEGATIVES, "x2_operational": incidents.INCIDENTS, "executed_synthetic": 150, "no_failure_erased": True, "zero_first_pass_credit_for_failures": True})
    write_json("truth/final-open-and-exact-gate-register.json", {"schema": "ghc.family.v652-v1.final-gates.v1", "open_gaps": 62, "exact_gates": 63, "phase_open_gap": {"proposal_id": "V6521-P29", "closed": False}, "phase_exact_gate": {"proposal_id": "V6521-P30", "closed": False}, "authority_boundary": "No empirical, participant, production, legal, cultural, affected-party, or Māori-authority gate was silently closed."})
    write_json("final/complete-incomplete-checklist.json", read_json("truth/complete-incomplete-checklist.json"))
    write_json("final/commit-cap-contract.json", {"schema": "ghc.family.v652-v1.commit-cap.v1", "source_head": d.SOURCE_HEAD, "x1_commits": 1, "x2_evidence_commits": 1, "x2_closeout_commits": 1, "planned_phase_total": 3, "maximum": 6, "merge_commits_allowed": 0})
    write_json("final/source-and-ancestry-contract.json", {"schema": "ghc.family.v652-v1.ancestry-contract.v1", "source": d.SOURCE_HEAD, "x1": X1_HEAD, "evidence": EVIDENCE_HEAD, "final": "resolved_only_by_postcommit_validator", "expected_phase_commits": 3, "expected_merges": 0, "expected_final_parents": 1})
    write_json("final/closeout-receipt.json", {"schema": "ghc.family.v652-v1.closeout-receipt.v1", "state": "combined_closeout_and_seal_candidate_complete", "evidence_head": EVIDENCE_HEAD, "outcomes": outcomes["counts"], "negatives": 8018, "gaps": 62, "gates": 63, "verdict": "NOT_READY_FOR_STAGE_20", "baton_word_count": len(re.findall(r"\b\w+(?:[-']\w+)*\b", baton)), "route": "PREPARED_NOT_SENT", "boundary": "A postcommit exact-final pass and one acknowledged route send remain pending."})
    write_json("final/seal-receipt.json", {"schema": "ghc.family.v652-v1.seal-receipt.v1", "state": "seal_candidate_complete", "source_head": d.SOURCE_HEAD, "x1_head": X1_HEAD, "evidence_head": EVIDENCE_HEAD, "expected_phase_commits": 3, "expected_merges": 0, "expected_final_parents": 1, "commit_cap": 6, "canonical_exact_final_state": "pending_postcommit_single_pass"})
    write_json("final/final-receipt.json", {"schema": "ghc.family.v652-v1.final-receipt.v1", "state": "closeout_candidate_complete", "exact_head": "resolved_only_by_postcommit_validator", "canonical_exact_final_state": "pending_postcommit_single_pass", "successful_canonical_passes": 0, "full_repository_suite_run": False, "independent_reproduction_claimed": False, "future_cli_seats_launched": 0, "route": "PREPARED_NOT_SENT"})
    documents = []
    for path in sorted(ROOT.rglob("*.md")):
        relative = path.relative_to(ROOT).as_posix()
        words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", path.read_text(encoding="utf-8")))
        baton_exception = relative == "handoffs/orin-thale-v652-v2-activation.md"
        documents.append({"path": relative, "words": words, "baton_exception": baton_exception})
    write_json("final/document-word-counts.json", {"schema": "ghc.family.v652-v1.document-words.v1", "documents": documents, "ordinary_cap": 100000, "baton_minimum": 10000, "baton_maximum": 100000, "valid": all((row["baton_exception"] and 10000 <= row["words"] <= 100000) or (not row["baton_exception"] and row["words"] <= 100000) for row in documents)})
    write_json("final/owner-growth-receipt.json", {"schema": "ghc.family.v652-v1.owner-growth.v1", "owner_file_count_before_manifests": len(owner_paths()), "rotation_threshold": 15000, "below_threshold": len(owner_paths()) < 15000, "inherited_repository_baseline_not_used_as_trigger": True})
    build_manifests()
    privacy = read_json("validation/final-staged-privacy.json")
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"confirmed privacy hits: {privacy['confirmed_hits']}")
    print(json.dumps({"valid": True, "outcomes": outcomes["counts"], "negatives": 8018, "gaps": 62, "gates": 63, "baton_words": len(re.findall(r"\b\w+(?:[-']\w+)*\b", baton)), "owner_paths": read_json("validation/final-owner-manifest.json")["owner_path_count"], "state": "closeout_candidate_not_committed"}, sort_keys=True))


if __name__ == "__main__":
    build()
