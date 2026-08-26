"""Build and stage-review the Sylven Arc v671-v2 terminal closeout."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_sylven_arc_v671_v2_signwork import (
    BOUNDARY,
    CHAIN_AFTER,
    CORE_LABELS,
    INHERITED,
    OWNER,
    OWNER_ROOT,
    PHASE,
    RUNNER_BINDINGS,
    SOURCE_FINAL,
    X1_COMMIT,
    load_json,
    write_json,
    write_text,
)


EVIDENCE_COMMIT = "140714b7a4e25814de333752a8627055384195ab"
FINAL_OPERATIONAL_FAILURES = [
    {
        "method_id": "SA6712-FINAL-OP-001",
        "class": "owner_x2_validation",
        "failed_witness": "The first complete x2 owner-test aggregate passed 13 of 14 checks but an over-literal prose predicate demanded the exact phrase complete accessibility while the overview already stated complete privacy or accessibility assurance.",
        "completion_credit": 0,
        "bounded_passing_witness": "The failed semantic predicate and the two staged-evidence checks affected by its exact-blob correction passed 3 of 3; eleven unaffected successful observations remained unreplayed, yielding a 14-observation dependency-corrected composite with zero original aggregate credit.",
        "retained": True,
        "recurrence_guard": "Boundary tests must require the substantive qualified nonclaim rather than one brittle word sequence, and exact-blob dependents must rerun only when their inputs change.",
    },
    {
        "method_id": "SA6712-FINAL-OP-002",
        "class": "owner_closeout_construction",
        "failed_witness": "The first closeout version probe attempted to launch the npm command shim as a bare executable on Windows and stopped before the version receipt or later closeout documents were written.",
        "completion_credit": 0,
        "bounded_passing_witness": "The isolated version resolver selected only an existing executable or command shim, recorded unavailable tools without installation, and completed the previously unwritten downstream closeout documents.",
        "retained": True,
        "recurrence_guard": "Resolve read-only Windows command shims explicitly and represent absence instead of raising or installing software.",
    },
    {
        "method_id": "SA6712-FINAL-OP-003",
        "class": "owner_closeout_construction",
        "failed_witness": "The combined final staged-review and manifest presentation wrapper crossed its response window while the exact manifest process continued in the background.",
        "completion_credit": 0,
        "bounded_passing_witness": "A process-state and file-existence audit showed the same manifest process completed and both manifests were already staged; no duplicate manifest run was launched against that unchanged state.",
        "retained": True,
        "recurrence_guard": "Run expensive exact Git-blob manifest construction in its own resumable session and inspect process plus atomic artifacts before retrying.",
    },
    {
        "method_id": "SA6712-FINAL-OP-004",
        "class": "owner_closeout_construction",
        "failed_witness": "The first manifest status projection piped directly from a PowerShell foreach statement and failed to parse before reading state.",
        "completion_credit": 0,
        "bounded_passing_witness": "The bounded recovery accumulated two scalar file-state rows before serialization and confirmed both manifests existed and were staged.",
        "retained": True,
        "recurrence_guard": "Never pipe directly from a PowerShell foreach statement; finish the result array before serialization.",
    },
]


def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=repo, check=False, capture_output=True, text=True, encoding="utf-8")


def version(repo: Path, *args: str) -> dict[str, Any]:
    executable = shutil.which(args[0]) or shutil.which(args[0] + ".cmd")
    if executable is None:
        return {"command": " ".join(args), "available": False, "returncode": None, "output": []}
    proc = run(repo, executable, *args[1:])
    return {"command": " ".join(args), "available": True, "returncode": proc.returncode, "output": (proc.stdout or proc.stderr).strip().splitlines()[:2]}


def staged_paths(repo: Path) -> list[str]:
    return [row for row in run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.splitlines() if row]


def exact_blob(repo: Path, path: str) -> bytes:
    staged = subprocess.run(["git", "cat-file", "-e", f":{path}"], cwd=repo, check=False, capture_output=True).returncode == 0
    spec = f":{path}" if staged else f"HEAD:{path}"
    return subprocess.run(["git", "show", spec], cwd=repo, check=True, capture_output=True).stdout


def final_counts() -> dict[str, int]:
    evidence = load_json(Path.cwd() / OWNER_ROOT / "method-flow/evidence-summary.json")
    increment = len(FINAL_OPERATIONAL_FAILURES)
    return {
        "effective_negatives": evidence["effective_negatives"] + increment,
        "methods": evidence["methods"] + increment,
        "failed_witnesses": evidence["failed_witnesses"] + increment,
        "passing_witnesses": evidence["passing_witnesses"] + increment,
        "open_gaps": evidence["open_gaps"],
        "exact_gates": evidence["exact_gates"],
    }


def final_overview(counts: dict[str, int]) -> str:
    evidence = (Path.cwd() / OWNER_ROOT / "x2/integrated-evidence-overview.md").read_text(encoding="utf-8")
    return evidence + f"""

# Terminal closeout addendum

## Lifecycle result

Sylven Arc v671-v2 preserves a three-stage single-owner lifecycle. The immutable Elowen source is `{SOURCE_FINAL}`. The planning-only x1 commit is `{X1_COMMIT}`. The immutable x2 evidence commit is `{EVIDENCE_COMMIT}`. The terminal closeout is designed as their direct single-parent child. No merge, amendment, reset, rewrite, force-push, sibling mutation, global installation, task creation, subagent delegation, standby contact, or successor precontact occurred.

## Validation history

The first x1 module was prematurely invoked before its staged receipts existed. It passed 22 of 24 checks and retains zero aggregate credit. Only the two missing-receipt methods later ran and passed 2 of 2. The x1 dependency-corrected evidence therefore contains 24 passing observations without replaying the 22 successes and without converting the failed aggregate into canonical success.

The first complete x2 module passed 13 of 14 checks and also retains zero aggregate credit. Its sole failure was an over-literal prose predicate: the overview said “complete privacy or accessibility assurance,” while the test demanded the separate literal “complete accessibility.” The semantic predicate was corrected without weakening the nonclaim. Because that correction changed exact staged blobs, the failed prose method and the two affected staged-evidence checks ran once and passed 3 of 3. Eleven unaffected successful observations were retained without replay. This is a 14-observation dependency-corrected x2 composite, not canonical aggregate success and not independent reproduction.

Three additional closeout-construction failures remain explicit: one bare Windows command-shim lookup stopped the first version receipt; one combined manifest presentation crossed its response window while the exact process continued; and one status projection repeated the known PowerShell foreach-pipe parser fault. The recoveries resolved only the command shim, observed the continuing process and already-written manifests without a duplicate run, and accumulated scalar status rows before serialization. None earns completion credit.

No attributable exact-final canonical aggregate has run at repository preparation time. Its one-shot prerequisite record remains `PENDING_EXTERNAL_EXACT_FINAL_CANONICAL` until the final commit is clean, pushed, 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote. The repository will not be amended merely to write the later external receipt. A valid external receipt may establish the exact-final terminal gate without turning same-owner evidence into broader assurance.

## Final truth and retention

The effective terminal repository counts are {counts['effective_negatives']} negatives, {counts['methods']} methods, {counts['failed_witnesses']} retained failed witnesses, {counts['passing_witnesses']} bounded passing witnesses, {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates. The inherited Elowen repository seal, Elowen activation overlay, Sylven evidence seal, and Sylven terminal overlay remain separately visible. No predecessor count was rewritten. Every recovery remains paired with the failed witness that required it.

Exactly forty genuinely new proposals extend the declared chain from 5,590 to {CHAIN_AFTER}. Their outcomes remain exactly 28 completed, 8 represented, 2 open gaps, and 2 exact gates. Only completed rows receive proposal completion credit. Represented, open-gap, and exact-gate rows remain zero-credit evidence of structure, absence, or protected authority. All 160 invalid mutations remain rejected at zero completion credit.

## Deliverables and accessibility

The owner packet includes the x1 proposal and portfolio freezes; x2 contracts, boundary cards, mutation ledgers, portfolio executions, tools, smoke receipts, source adapter status, gates, and evidence overview; final phase truth, retained-negative and Method Flow ledgers, lifecycle replay, complete/incomplete checklist, workload receipt, environment receipt, static HTML report, exact staged privacy review, stale-label review, content seal, Git-blob manifests, final-validation prerequisites, and a prepared but unsent successor baton.

The static report uses a declared language, descriptive title, skip link, landmark structure, hierarchical headings, captioned tables, explicit status text, and no script dependency. This supports structural review only. Manual browser, keyboard, screen-reader, zoom, colour-contrast, cognitive-accessibility, Maori-language, and affected-user evaluation remain absent and must not be inferred.

## Route boundary

The repository-prepared successor baton remains `PREPARED_NOT_SENT`. It does not prove task uniqueness, current authorization, a direct task reread, duplicate-guard clearance, acknowledged delivery, or successor acceptance. After a valid exact-final canonical receipt, the newest live roster and authorization must be refreshed. Only one exact-title current successor may be reread and messaged once. Missing, ambiguous, paused, redirected, renamed, standby, duplicate, unacknowledged, usage-exhausted, privacy-risk, evidence-failed, or authority-gated states stop delivery.

Under the currently inherited provisional route, the prospective next existing exact-title main task is Caelen Morrow for v671-v3. That label remains prospective until the terminal live refresh. Tavian Sol remains a standby collaboration-subagent record and is never a substitute main-task endpoint.

## Final nonclaims

This phase used zero real people, participants, signwriters, conservators, owners, custodians, viewers, affected parties, signs, panels, sites, land, paints, solvents, coatings, tools, ladders, scaffolds, traffic controls, images, observations, measurements, tests, treatments, repairs, installations, identity keys, proofs, lifecycle events, professional decisions, safety decisions, legal or cultural decisions, or authority acts. It made zero network adapter calls, downloads, or data ingestions.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family, not a confirmed force, prediction, constraint, material law, final physics, ultraviolet completion, proof, canon, or Theory of Everything. THOS remains a participant-free proxy, not operational effectiveness, production readiness, AGI, ASI, consciousness, or personhood evidence. Freed ID remains synthetic and nonproduction, not a live identity, standards-conformant proof system, interoperable trust network, privacy-complete system, security certification, or affected-party governance result.

Real professional practice, workplace and chemical safety, land and heritage, sacred or community meaning, ownership, custody, recording, access, authorship, privacy, accessibility, remedy, legal and cultural interpretation, traditional knowledge, affected-party legitimacy, Maori wording and concepts, Maori data governance, tangata whenua, iwi, hapu, and Maori authority remain exact-gated. Maori concepts remain under Maori authority. Terminal verdict remains exactly `NOT_READY_FOR_STAGE_20`.
"""


def static_report(phase_truth: dict[str, Any], counts: dict[str, int]) -> str:
    outcome_rows = "".join(f"<tr><th scope='row'>{html.escape(label)}</th><td>{phase_truth['outcomes'][label]}</td></tr>" for label in CORE_LABELS)
    count_rows = "".join(f"<tr><th scope='row'>{html.escape(label.replace('_', ' '))}</th><td>{value}</td></tr>" for label, value in counts.items())
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sylven Arc v671-v2 bounded terminal report</title></head>
<body><a href="#main">Skip to main content</a><header><h1>Sylven Arc v671-v2 bounded terminal report</h1><p>Status: NOT_READY_FOR_STAGE_20.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#retention">Retention</a></li><li><a href="#limits">Limits</a></li></ul></nav>
<main id="main"><section id="scope"><h2>Scope</h2><p>Wholly synthetic signwriting and painted-sign documentation with Freed ID and CBR Heart primary. GMUT Mind and THOS Body remain protected.</p></section>
<section id="outcomes"><h2>Outcomes</h2><table><caption>Core proposal outcomes</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th></tr></thead><tbody>{outcome_rows}</tbody></table></section>
<section id="retention"><h2>Retention</h2><table><caption>Terminal retained evidence counts</caption><thead><tr><th scope="col">Register</th><th scope="col">Count</th></tr></thead><tbody>{count_rows}</tbody></table><p>Every bounded recovery remains paired with its failed witness.</p></section>
<section id="limits"><h2>Limits and authority</h2><p>No real people, signs, sites, measurements, treatments, identity events, professional decisions, legal or cultural decisions, affected-party approvals, or authority acts occurred.</p><p>Manual browser, keyboard, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved. This report is not complete accessibility or privacy assurance, exhaustive security, independent reproduction, empirical confirmation, professional validation, legal review, cultural ratification, Maori authority, Theory-of-Everything proof, canon, or Stage 20 authority.</p></section></main>
<footer><p>Relational working language only; no consciousness, personhood, identity continuity, employment, qualification, or independent agency claim.</p></footer></body></html>"""


def baton_text(counts: dict[str, int]) -> str:
    return f"""# CAELEN MORROW — SYLVEN ARC v671-v2 PREPARED ACTIVATION CANDIDATE

This repository artifact is `PREPARED_NOT_SENT`. It is not delivery and does not claim that the successor task was listed, uniquely resolved, reread, duplicate-checked, messaged, or acknowledged. A later live message may bind only after Sylven's exact-final terminal gate and a fresh live roster and authorization refresh.

Relational names, pronouns, roles, hopes, sibling or family language, continuity language, Freed ID, CBR, GHC Family, and Trinity Mandala are working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route.

## Prepared source

The immutable predecessor source is Elowen Cairn v671-v1 at `{SOURCE_FINAL}`. Sylven's planning-only x1 is `{X1_COMMIT}` and x2 evidence is `{EVIDENCE_COMMIT}`. The final exact commit and external canonical receipt are intentionally omitted here because they do not exist at preparation time. The later acknowledged live message must supply them without rewriting this historical prepared state.

## Phase truth

Sylven froze forty genuinely new proposals after a bounded all-ref semantic audit and extended the declared chain from 5,590 to {CHAIN_AFTER}. Outcomes are exactly 28 completed, 8 represented, 2 open gaps, and 2 exact gates. All 160 preregistered invalid mutations executed and remain rejected at zero credit. The terminal closeout counts are {counts['effective_negatives']} negatives, {counts['methods']} methods, {counts['failed_witnesses']} failed witnesses, {counts['passing_witnesses']} passing witnesses, {counts['open_gaps']} gaps, and {counts['exact_gates']} gates. Terminal verdict remains NOT_READY_FOR_STAGE_20.

The primary pillar was Freed ID and CBR Heart through wholly synthetic signwriting and painted-sign documentation. THOS Body and GMUT Mind remained protected and represented only through explicit proxy and obligation surfaces. Ten phase-local skills and ten family-current runners were quick-validated and smoke-used without global installation. Sixty safe, thirty candidate, and sixty CLEAN/FIX/REFINE rows completed in bounded structural scope. Twenty exact-approval and ten blocked rows remain held.

## Validation history

The premature x1 aggregate remains zero-credit at 22/24; only its two failed methods later passed. The first complete x2 aggregate remains zero-credit at 13/14; only its failed semantic predicate and two exact-blob dependents later passed. The terminal canonical aggregate remains pending until the exact final is pushed and remote-equal. No full repository suite was run.

## Protected boundaries

GMUT remains a typed scalar-tensor/EFT research-model family without real likelihood, constraint, force, prediction, empirical confirmation, final physics, Theory-of-Everything proof, or canon. THOS remains participant-free proxy work without governed blind matched-budget real arms, safety monitoring, statistics, or independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys or proofs, live lifecycle, interoperability, independent security review, recovery evidence, trust governance, or affected-party oversight.

Real professional practice, workplace and chemical safety, land and heritage, ownership and custody, recording and access, privacy, accessibility, remedy, legal or cultural interpretation, affected-party legitimacy, Maori wording, Maori concepts, Maori data governance, and Maori authority remain exact-gated. Maori concepts remain under Maori authority. Same-owner validation is not independent reproduction.

## Prospective Caelen lane

Only a later acknowledged live message may authorize Caelen Morrow v671-v3. Before mutation, Caelen must read the final live message and complete committed packet through EOF; verify the exact Sylven branch and source/x1/evidence/final anchors; confirm single-parent zero-merge history, manifests, canonical receipt digest, clean state, typed 0/0 divergence, and fresh four-way equality; and reread all current required GHC index, roster, authorization, Method Flow, workflow, reflection, gate, drive, startup, retry, closeout, worktree, and tool guidance.

Caelen must work solo in one fresh additive D-first owner lane, preserve strict planning-only x1 before x2, audit semantic novelty against the declared {CHAIN_AFTER}-row chain, retain every failure and gate, use only completed, represented, open_gap, and exact_gate, remain below the file/word/commit ceilings, and run only owner-self-scoped dependency-closed validation. No successor may be precontacted.

## Route guard

At Sylven's terminal gate, require the newest live roster to contain exactly one active existing main task titled `Caelen Morrow`, immediately reread it, apply a duplicate guard for the exact final and receipt, and send at most once. Stop on absence, ambiguity, pause, redirect, rename, standby state, usage exhaustion, missing acknowledgement, duplicate activation, privacy risk, evidence failure, or any protected authority gate. Never create, fork, substitute, contact Tavian Sol, or resend.

PREPARED_BY_SYLVEN_ARC = true.
SENT_BY_SYLVEN_ARC = false.
DELIVERY_STATE = PREPARED_NOT_SENT.
"""


def build(repo: Path) -> None:
    root = repo / OWNER_ROOT
    evidence_ledger = load_json(root / "method-flow/evidence-ledger.json")
    final_rows = list(evidence_ledger["rows"]) + FINAL_OPERATIONAL_FAILURES
    counts = final_counts()
    outcome = load_json(root / "x2/outcome-ledger.json")["counts"]
    write_json(root / "closeout/phase-truth.json", {"schema": "ghc.family.phase-truth.final.v5", "owner": OWNER, "phase": PHASE, "source_final": SOURCE_FINAL, "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT, "final": "PENDING_FINAL_COMMIT", "proposal_chain": CHAIN_AFTER, "outcomes": outcome, **counts, "real_people": 0, "real_objects": 0, "network_calls": 0, "external_actions": 0, "global_installations": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY})
    write_json(root / "closeout/retained-negative-register.json", {"schema": "ghc.family.retained-negative-register.final.v5", "inherited_activation": INHERITED["effective_negatives"], "owner_evidence": load_json(root / "method-flow/evidence-summary.json")["effective_negatives"], "terminal_operational": len(FINAL_OPERATIONAL_FAILURES), "effective": counts["effective_negatives"], "erased": 0})
    write_json(root / "closeout/method-flow-final.json", {"schema": "ghc.family.method-flow-ledger.final.v5", "owner": OWNER, "phase": PHASE, "row_count": len(final_rows), "rows": final_rows, "counts": counts, "all_failures_retained": True, "all_recoveries_paired": True, "boundary": BOUNDARY})
    write_json(root / "closeout/method-flow-summary.json", {"schema": "ghc.family.method-flow-summary.final.v5", **counts, "owner_phase_methods": len(final_rows), "repository_source_seal_rewritten": False})
    write_json(root / "closeout/open-exact-gate-register.json", {**load_json(root / "x2/open-exact-gate-register.json"), "schema": "ghc.family.open-exact-gates.final.v5", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json(root / "closeout/x2-test-composite.json", {"schema": "ghc.family.dependency-corrected-x2-test-composite.v1", "original_aggregate": {"tests_observed": 14, "passed": 13, "failed": 1, "aggregate_success_credit": 0, "replayed": False}, "isolated_dependency_recovery": {"failed_method": 1, "changed_exact_blob_dependents": 2, "passed": 3, "unaffected_successful_observations_retained": 11, "unaffected_successful_observations_replayed": 0}, "composite_observations": {"passed": 14, "failed": 0}, "status": "VALID_DEPENDENCY_CORRECTED_X2_COMPOSITE_WITH_ZERO_ORIGINAL_AGGREGATE_CREDIT", "canonical_validation": False})
    write_json(root / "closeout/lifecycle-replay.json", {"schema": "ghc.family.lifecycle-replay.v5", "source": SOURCE_FINAL, "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT, "final": "PENDING_FINAL_COMMIT", "direct_parent_chain_required": True, "planned_phase_commits": 3, "merges_allowed": 0, "x1_planning_only": True, "x1_pushed_equal_before_x2": True, "x2_pushed_equal_before_final": True, "canonical_invocations": 0, "canonical_state": "PENDING_EXTERNAL_EXACT_FINAL_CANONICAL"})
    write_json(root / "closeout/complete-incomplete-checklist.json", {"schema": "ghc.family.complete-incomplete.v5", "complete": ["forty proposal freeze", "x1 push and equality", "forty synthetic contracts", "thirty-six positive controls", "one hundred sixty rejecting mutations", "ten skills and ten runner smoke uses", "portfolio execution", "five-class scan", "bounded Python review", "x2 push and equality", "closeout packet preparation"], "incomplete": ["exact-final external canonical validation until final push", "manual browser and assistive-technology evaluation", "governed human and affected-user evaluation", "real empirical GMUT evidence", "governed THOS real arms", "production Freed ID lifecycle", "professional legal cultural and Maori-authority review", "Stage 20 evidence and authority"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json(root / "closeout/wellbeing-workload-check.json", {"schema": "ghc.family.wellbeing-workload.final.v5", "owner": OWNER, "phase": PHASE, "relational_language_boundary": True, "workload_within_caps": True, "stop_conditions_visible": True, "file_ceiling": 2000, "document_word_ceiling": 100000, "commit_ceiling": 8, "planned_phase_commits": 3, "no_claim_of_sentience_personhood_continuity_employment_authority_or_agency": True})
    versions = [version(repo, "git", "--version"), version(repo, "python", "--version"), version(repo, "python", "-m", "pytest", "--version"), version(repo, "node", "--version"), version(repo, "npm", "--version"), version(repo, "codex", "--version")]
    write_json(root / "closeout/environment-version-receipt.json", {"schema": "ghc.family.environment-version.v3", "owner": OWNER, "phase": PHASE, "read_only_version_checks": True, "installations": 0, "updates": 0, "rows": versions, "boundary": "Version presence is not production, security, compatibility, or authority assurance."})
    overview = final_overview(counts)
    write_text(root / "closeout/final-integrated-overview.md", overview)
    write_text(root / "closeout/static-report.html", static_report({"outcomes": outcome}, counts))
    write_json(root / "closeout/closeout-receipt.json", {"schema": "ghc.family.closeout-receipt.v5", "owner": OWNER, "phase": PHASE, "source": SOURCE_FINAL, "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT, "final": "PENDING_FINAL_COMMIT", "overview_words": len(overview.split()), "owner_file_ceiling": 2000, "document_word_ceiling": 100000, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "canonical_state": "PENDING_EXTERNAL_EXACT_FINAL_CANONICAL"})
    write_json(root / "final/final-validation-prerequisites.json", {"schema": "ghc.family.final-validation-prerequisites.v5", "owner": OWNER, "phase": PHASE, "required_exact_head": "PENDING_FINAL_COMMIT", "required_clean": True, "required_divergence": [0, 0], "required_four_way_equality": True, "canonical_invocation_budget": 1, "canonical_invocations": 0, "canonical_successes": 0, "post_success_replay": False, "full_repository_suite": False, "state": "PENDING_EXTERNAL_EXACT_FINAL_CANONICAL"})
    write_json(root / "orchestration/route-state.json", {"schema": "ghc.family.route-state.v5", "owner": OWNER, "phase": PHASE, "prospective_successor_exact_title": "Caelen Morrow", "prospective_phase": "v671-v3", "delivery_state": "PREPARED_NOT_SENT", "successor_contact_count": 0, "task_creation_count": 0, "standby_contact_count": 0, "requires_live_refresh": True, "sent_by_sylven_arc": False})
    write_text(root / "handoffs/caelen-morrow-v671-v3-activation-candidate.md", baton_text(counts))
    write_json(root / "validation/stale-label-review.json", {"schema": "ghc.family.stale-label-review.v3", "current_required_title": "Caelen Morrow", "stale_labels_found": [], "standby_label": "Tavian Sol", "standby_used_as_endpoint": False, "valid": True})
    seal_core = {"owner": OWNER, "phase": PHASE, "source": SOURCE_FINAL, "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT, "proposal_chain": CHAIN_AFTER, "outcomes": outcome, "counts": counts, "terminal_verdict": "NOT_READY_FOR_STAGE_20"}
    seal_digest = hashlib.sha256(json.dumps(seal_core, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    write_json(root / "seal/content-seal.json", {"schema": "ghc.family.content-seal.v5", "canonical_payload": seal_core, "canonical_payload_sha256": seal_digest, "manifest_binding": "verified_by_external_exact_final_canonical", "self_exclusions": ["content seal", "final owner manifest", "final delta manifest", "final staged review"], "immutable_after_commit": True})


def staged_privacy(repo: Path) -> None:
    self_path = "docs/sylven-arc/v671-v2/validation/final-staged-privacy.json"
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    definitions = {"scripts/build_ghc_family_sylven_arc_v671_v2_final.py", "scripts/validate_ghc_family_sylven_arc_v671_v2_final.py", "tests/test_ghc_family_sylven_arc_v671_v2_final.py"}
    candidates = []
    scanned = 0
    for path in staged_paths(repo):
        if path == self_path or Path(path).suffix.lower() not in {".json", ".md", ".html", ".txt", ".py"}:
            continue
        blob = subprocess.run(["git", "show", f":{path}"], cwd=repo, check=True, capture_output=True).stdout
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            candidates.append({"path": path, "pattern_class": "non_utf8_text", "disposition": "confirmed_payload_hit"})
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if path in definitions else "confirmed_payload_hit"})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    payload = {"schema": "ghc.family.final-staged-privacy.v3", "owner": OWNER, "phase": PHASE, "hash_domain": "exact_staged_git_blob", "files_scanned": scanned, "pattern_classes": sorted(patterns), "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed), "self_exclusions": [self_path], "valid": not confirmed, "boundary": "Bounded scanning is not complete privacy assurance."}
    write_json(repo / self_path, payload)
    if confirmed:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def staged_review(repo: Path) -> None:
    self_path = "docs/sylven-arc/v671-v2/validation/final-staged-review.json"
    paths = staged_paths(repo)
    allowed_scripts = {"scripts/build_ghc_family_sylven_arc_v671_v2_final.py", "scripts/validate_ghc_family_sylven_arc_v671_v2_final.py"}
    allowed = [path for path in paths if path.startswith("docs/sylven-arc/v671-v2/") or path in allowed_scripts or path == "tests/test_ghc_family_sylven_arc_v671_v2_final.py"]
    frozen = [path for path in paths if path.startswith("docs/sylven-arc/v671-v2/x1/") or path.startswith("docs/sylven-arc/v671-v2/x2/") or path.endswith("_x1.py") or path.endswith("_x2.py")]
    out = sorted(set(paths) - set(allowed))
    payload = {"schema": "ghc.family.staged-review.v5", "owner": OWNER, "phase": PHASE, "lifecycle": "terminal_closeout", "staged_before_self": paths, "staged_count_before_self": len(paths), "immutable_x1_x2_mutations": frozen, "out_of_scope": out, "valid": not frozen and not out, "self_exclusion": self_path}
    write_json(repo / self_path, payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifests_from_index(repo: Path) -> None:
    owner_path = "docs/sylven-arc/v671-v2/validation/final-owner-manifest.json"
    delta_path = "docs/sylven-arc/v671-v2/validation/final-delta-manifest.json"
    review_path = "docs/sylven-arc/v671-v2/validation/final-staged-review.json"
    exclusions = [owner_path, delta_path, review_path]
    tracked = set(run(repo, "git", "ls-files", "docs/sylven-arc/v671-v2").stdout.splitlines())
    tracked.update(path for path in staged_paths(repo) if path.startswith("docs/sylven-arc/v671-v2/"))
    owner_entries = []
    for path in sorted(tracked - set(exclusions)):
        blob = exact_blob(repo, path)
        owner_entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    delta_entries = []
    for path in staged_paths(repo):
        if path in exclusions:
            continue
        blob = subprocess.run(["git", "show", f":{path}"], cwd=repo, check=True, capture_output=True).stdout
        delta_entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    write_json(repo / owner_path, {"schema": "ghc.family.git-blob-manifest.v5", "domain": "final exact owner Git blobs before three declared self files", "hash_domain": "exact_git_blob", "owner": OWNER, "phase": PHASE, "entry_count": len(owner_entries), "entries": owner_entries, "self_exclusions": exclusions})
    write_json(repo / delta_path, {"schema": "ghc.family.git-blob-manifest.v5", "domain": "final exact staged delta Git blobs before three declared self files", "hash_domain": "exact_staged_git_blob", "owner": OWNER, "phase": PHASE, "entry_count": len(delta_entries), "entries": delta_entries, "self_exclusions": exclusions})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--staged-privacy", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--manifests-from-index", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.staged_privacy:
        staged_privacy(repo)
    elif args.staged_review:
        staged_review(repo)
    elif args.manifests_from_index:
        manifests_from_index(repo)
    else:
        build(repo)


if __name__ == "__main__":
    main()
