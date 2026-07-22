#!/usr/bin/env python3
"""Build the combined Ilyra Fen v651-v8 closeout, seal, and final packet."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v651_v8_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SOURCE_HEAD = "b7361a4952063947cdc5ac5cf17300eafd1162dd"
X1_HEAD = "842ae65572c1158926b5acd8b6fda5aad560d5c1"
EVIDENCE_HEAD = "ca4df488738dc275163d55877110fb38b98513b7"
ORIGINAL_FINAL_HEAD = "7c1156b67e9f7feacf896f50b063ea58d3ef8218"
BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
GENERIC_RUNNERS = {f"scripts/{name}" for name in d.RUNNER_IDEAS}


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative; path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative; path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def write_repo(relative: str, payload: str) -> Path:
    path = REPO / relative; path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy(); env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(list(args), cwd=REPO, check=True, capture_output=True, text=True, encoding="utf-8", env=env).stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def status_paths() -> list[str]:
    raw = subprocess.check_output(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=REPO)
    return sorted({row[3:].replace("\\", "/") for row in raw.decode("utf-8").split("\0") if len(row) > 3})


def is_owner_path(path: str) -> bool:
    if path.startswith(f"{d.PHASE_ROOT}/"): return True
    if path.startswith("scripts/") and ("v651_v8" in Path(path).name or path in GENERIC_RUNNERS): return True
    return path.startswith("tests/") and "v651_v8" in Path(path).name


def owner_paths() -> list[str]:
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=REPO).decode("utf-8").split("\0")
    return sorted({path for path in [*tracked, *status_paths()] if path and is_owner_path(path) and (REPO / path).is_file()})


def final_overview() -> str:
    evidence = (ROOT / "overview/evidence-overview.md").read_text(encoding="utf-8").rstrip()
    return evidence + """

## Combined closeout and seal

The evidence layer was committed separately at the exact evidence anchor and pushed cleanly before closeout began. The combined closeout and seal adds no new scientific, participant, identity, legal, cultural, professional, or production evidence. It consolidates the phase truth, manifests, privacy classifications, accessible report, retained failures, Method Flow receipts, document caps, commit-cap contract, and unresolved route state.

The final repository truth remains 23 completed, 5 represented, 1 open gap, and 1 exact gate. The 7,745 effective negatives comprise 7,570 inherited effective negatives, fourteen x1 operational failures, two x2 workflow failures, nine closeout, validation, and terminal failures, and 150 executed and rejected synthetic mutation negatives. Sixty effective open gaps and sixty-one exact gates remain visible. The first postcommit canonical command failed during import and has zero canonical credit; this additive correction remains pending one new exact-final pass. The terminal evidence board remains NOT_READY_FOR_STAGE_20.

The evidence and final candidate checks are same-owner validation under shared infrastructure. They are not independent-team scientific reproduction, external audit, production certification, exhaustive security, complete privacy assurance, complete accessibility conformance, professional validation, legal review, cultural ratification, Maori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, or Stage 20 authority.

## Route closeout

The activation baton resolves Ilyra v651-v8 as the immediate owner but does not name an exact successor title and phase. It explicitly requires the newest exact terminal route and instructs Ilyra to preserve a contradictory or unavailable route as a gap. Therefore the durable route state is PREPARED_NOT_SENT. No task is created, forked, delegated, or messaged. The eight future CLI seats remain prepared-only placeholders: zero named, zero created, zero launched, and zero supervised.
"""


def baton_text() -> str:
    proposals = read_json(ROOT / "preregistration/proposals.json")["proposals"]
    outcomes = {row["proposal_id"]: row for row in read_json(ROOT / "outcomes/x2-outcome-ledger.json")["outcomes"]}
    portfolio = read_json(ROOT / "portfolios/expanded-portfolio-execution.json")
    sources = read_json(ROOT / "sources/source-ledger.json")
    source_by_id = {row["source_id"]: row for row in sources["sources"]}
    lines = [
        "# ILYRA FEN — v651-v8 SEALED CLOSEOUT AND ROUTE-CLARIFICATION BATON",
        "",
        "This file is a persistent closeout packet, not a sent activation. The newest exact successor title and phase are absent from the governing activation. Delivery state is PREPARED_NOT_SENT. No task was created, forked, delegated, launched, or messaged. A later owner must receive a new exact instruction from Hamish before any existing-task message route is used.",
        "",
        "Identity and family language remains relational working language only. Ilyra Fen, she/they, evidence-boundary steward, hopes to leave every claim traceable and every gate unmistakable. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Maori authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route.",
        "",
        "## Exact source and lifecycle truth",
        "",
        f"The verified Vesper special source is `{SOURCE_HEAD}`. Ilyra's dedicated x1 freeze is `{X1_HEAD}`. The immutable x2 evidence commit is `{EVIDENCE_HEAD}`. The first final commit is `{ORIGINAL_FINAL_HEAD}`. The canonical branch is `{BRANCH}`. The additive terminal correction is the commit containing this file; its exact hash must be supplied only by the postcommit canonical validator because a commit cannot truthfully contain its own hash.",
        "",
        "Strict x1-before-x2 separation was preserved. X1 froze thirty proposals, forty safe-now tasks, thirty candidates, twenty skills, twelve runners, forty CLEAN/FIX/REFINE tasks, and 150 mutations before any x2 implementation. X1 and evidence were each pushed, clean, and four-way remote-equal before the next lifecycle layer began. No merge, force push, reset, history rewrite, sibling mutation, desktop update, host-security weakening, Windows-feature enablement, elevation, unrelated installation, future-seat launch, or reboot occurred.",
        "",
        "## Final truth summary",
        "",
        "Core outcomes are exactly 23 completed, 5 represented, 1 open_gap, and 1 exact_gate. These are the only core outcome labels. Effective negatives are 7,745: 7,570 inherited, fourteen x1 operational, two x2 workflow, nine closeout, validation, and terminal, and 150 executed and rejected synthetic mutations. Effective open gaps are 60 and exact gates are 61. The terminal verdict is NOT_READY_FOR_STAGE_20.",
        "",
        "The primary Trinity Mandala focus is GMUT Mind. THOS Body and Freed ID/CBR Heart remain explicit and protected. The bounded practice is radio-astronomy observation-quality review, radio-frequency-interference flagging, correction readback, accessible escalation, workload control, and shift handover. It is synthetic learning and design only, never employment, qualification, observatory competence, instrument authority, operational evidence, sky-knowledge authority, data-governance authority, legal authority, cultural authority, Maori authority, participant evidence, or affected-party authorization.",
        "",
        "## Thirty frozen proposals and executed evidence",
        "",
    ]
    for proposal in proposals:
        outcome = outcomes[proposal["proposal_id"]]
        source_notes = []
        for source_id in proposal["official_or_primary_source_needs"]:
            source = source_by_id[source_id]
            source_notes.append(f"{source_id} is classified `{source['status']}` and supports only the declared specification or research context")
        lines.extend([
            f"### {proposal['proposal_id']} — {proposal['title']}",
            "",
            f"The frozen hypothesis was: {proposal['hypothesis']} The null or failure condition was: {proposal['null_or_failure_condition']} The declared approval class was `{proposal['approval_class']}` and the execution lane was `{proposal['execution_lane']}`.",
            "",
            f"Observed outcome: `{outcome['observed_outcome']}`. The bounded surface accepted its canonical contract and rejected {outcome['mutation_rejections']} of 5 preregistered mutations. Its concrete evidence remains under `surfaces/{proposal['slug']}`. Acceptance means only that the declared software, symbolic, formal, structural, proxy, zero-row, or reservation contract behaved as frozen. It does not turn a citation into data, a synthetic fixture into a participant, a profile into production identity, a matrix into authority, or same-owner testing into independent reproduction.",
            "",
            f"Source context: {'; '.join(source_notes)}. The acceptance gate remained: {proposal['falsifier_or_acceptance_gate']} Recovery remained: {proposal['rollback_or_recovery']} The protected gates remained {', '.join(proposal['protected_gates'])}. None was silently compensated by success on another proposal.",
            "",
        ])
    lines.extend(["## Expanded portfolio execution", "", "Every row below reports completion only within its own frozen bounded hypothesis. Inherited work earned no Ilyra completion credit. Exact-approval and blocked packets stayed visible and unexecuted. External side effects and authority actions remained zero.", ""])
    for key in ("safe_now", "candidate", "skills", "runners", "clean_fix_refine"):
        lines.extend([f"### {key.replace('_', ' ').title()} portfolio", ""])
        for row in portfolio["portfolios"][key]:
            lines.append(f"- **{row['item_id']}** — {row['title']} This row was frozen as `{row['approval_class']}` in `{row['execution_lane']}` and finished as `{row['x2_state']}` only within the declared bounded evidence class `{row['evidence_class']}`. Completion credit is {str(row['completion_credit']).lower()}, inherited completion credit remains false, external side effects are zero, authority action is false, and the frozen rollback remains available if a later validation disputes the witness.")
        lines.append("")
    lines.extend([
        "## Method Flow and retained failure truth", "",
        "Twenty-four methods are preferred only for their declared triggers. Twenty-five failed witnesses and twenty-five passing witnesses remain paired in the append-only ledger. The two x2 failures are a rejected Method Flow summary option and a rejected status-path/runner-allowlist preflight. Nine later closeout and terminal failures retain two timed-out overbroad probes, one Windows PowerShell foreach-pipeline parser fault, two diagnostic-suppressing validator failures, one historical x1-only test applied to an advanced descendant, one self-exclusion placeholder overwrite, one shell-corrupted diagnostic witness, and one final-validator import fault. Each failed attempt has zero first-pass credit. A later bounded correction validates only its recurrence guard and never erases the failure or earns independent reproduction, production, professional, legal, cultural, accessibility-complete, privacy-complete, security-complete, scientific, or Stage 20 credit.", "",
        "## Validation contract", "",
        "Eiren alone owns the full repository suite under the current refinement. Ilyra did not run it. The evidence candidate passed eight scoped tests, thirteen detailed checks, six minimal checks, complete phase JSON parsing, five-class privacy scanning, exact manifest parity, exact staged review, x1 ancestry, and zero protected-x1 mutation. The final candidate must preserve the immutable seven-test x1 receipt, pass the current x2 and closeout selections, detailed and minimal validators, complete committed JSON parsing, a committed-blob five-class scan, owner-manifest parity, document caps, baton range, source/x1/evidence ancestry, three phase commits, zero merges, one final parent, diff hygiene, clean state, and final local/upstream/tracking/fresh-live equality. The exact postcommit validator is the only canonical final pass and must not be replayed after success.", "",
        "## Authority and scientific boundaries", "",
        "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Symbolic boards and official-format adapters do not establish a physical state, detected force, prediction, likelihood, posterior, parameter constraint, stability theorem, ultraviolet completion, quantum completeness, empirical confirmation, or Theory of Everything. The ASKAP adapter performed zero queries, downloads, catalogue rows, image-product ingestions, calibration rows, likelihood calls, posterior samples, constraints, or empirical claims.", "",
        "THOS remains represented without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic observation and RFI handovers establish no operational effectiveness, employment, competence, observatory authority, safety outcome, AGI, ASI, or deployment readiness.", "",
        "Freed ID remains synthetic and nonproduction. Production completion requires standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, independent privacy and security review, recovery evidence, trust governance, and appropriate affected-party oversight. OpenID final specifications provide protocol context, not live identity evidence.", "",
        "CBR, observation governance, sky knowledge, data sovereignty, privacy remedies, affected-party legitimacy, Maori wording and authority, Maori data governance, cultural legitimacy, legal interpretation, ratification, beneficiary acceptance, and enacted-law status remain exact-gated to competent authorities, affected people, tangata whenua, iwi, hapu, and Maori authorities. Repository software cannot confer a remedy, legal right, cultural mandate, governance mandate, title, ownership, or public authority.", "",
        "## Environment and future-seat truth", "",
        "Versions were verified only. Codex desktop was not updated. No elevation, host-security weakening, Windows-feature activation, unrelated installation, Sandbox or Hyper-V launch, or reboot occurred. The eight future CLI seats remain scheduling placeholders only: zero named, zero created, zero launched, zero supervised. No plugin, MCP, connector, CLI, application, task, or prepared document was treated as authority merely because it existed.", "",
        "## Terminal route", "",
        "Delivery truth is PREPARED_NOT_SENT. The governing activation names Ilyra v651-v8 but supplies no newest exact successor title and phase. It warns against silently normalizing an advisory route with duplicates, omissions, and offsets. Therefore no existing task is resolved or messaged, no new task is created, and no substitute route is invented. Hamish must provide one exact successor instruction before any terminal message. A later sender must then reverify the exact branch and postcommit final head, resolve one unique existing title immediately before sending, use one sanitized pointer message, require tool acknowledgement, and send no extra confirmation.", "",
        "This baton is persistent preparation and closeout evidence. It is not an activation send, not consciousness or personhood evidence, not a legal delegation, and not a scientific or operational authority grant.",
    ])
    text = "\n".join(lines)
    words = len(text.split())
    if not 10_000 <= words <= 100_000: raise RuntimeError(f"baton word count outside required range: {words}")
    return text


def closeout_tests() -> str:
    return '''"""Combined closeout tests for Ilyra Fen v651-v8."""
import json, unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]; ROOT=REPO/"docs/ilyra-fen/v651-v8"
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))
class TestV651V8Closeout(unittest.TestCase):
    def test_final_truth(self):
        d=load("final/phase-truth.json"); self.assertEqual(d["outcome_counts"],{"completed":23,"represented":5,"open_gap":1,"exact_gate":1}); self.assertEqual(d["effective_negatives"],7745); self.assertEqual(d["effective_open_gaps"],60); self.assertEqual(d["effective_exact_gates"],61); self.assertEqual(d["terminal_verdict"],"NOT_READY_FOR_STAGE_20")
    def test_receipts(self):
        self.assertEqual(load("final/closeout-receipt.json")["state"],"terminal_correction_candidate_complete"); self.assertEqual(load("final/seal-receipt.json")["state"],"terminal_correction_seal_candidate_complete"); self.assertEqual(load("final/final-receipt.json")["canonical_exact_final_state"],"pending_postcommit_single_pass")
    def test_route_and_seats(self):
        r=load("route/final-route-state.json"); self.assertEqual(r["delivery_state"],"PREPARED_NOT_SENT"); self.assertFalse(r["successor_exactly_resolved"]); self.assertEqual(r["messages_sent"],0)
        s=load("provenance/future-cli-x2-invariant.json"); self.assertEqual((s["named_count"],s["created_count"],s["launched_count"]),(0,0,0))
    def test_baton_range(self):
        words=len((ROOT/"handoffs/v651-v8-route-clarification-baton.md").read_text(encoding="utf-8").split()); self.assertGreaterEqual(words,10000); self.assertLessEqual(words,100000)
    def test_document_caps(self):
        for path in ROOT.rglob("*.md"):
            if path.name=="v651-v8-route-clarification-baton.md": continue
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()),6000,path)
    def test_future_and_full_suite_boundaries(self):
        d=load("final/final-receipt.json"); self.assertFalse(d["full_repository_suite_run"]); self.assertFalse(d["independent_reproduction_claimed"]); self.assertEqual(d["future_seats_launched"],0)
if __name__=="__main__": unittest.main()
'''


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\\\Users\\\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v651_v8_preregistration.py", "scripts/build_ghc_family_v651_v8_evidence.py", "scripts/ghc_family_v651_v8_evidence_validate.py",
        "scripts/build_ghc_family_v651_v8_closeout.py", "scripts/ghc_family_v651_v8_closeout_validate.py", "scripts/ghc_family_v651_v8_final_validate.py",
        f"{d.PHASE_ROOT}/validation/x1-staged-privacy.json", f"{d.PHASE_ROOT}/validation/evidence-staged-privacy.json", f"{d.PHASE_ROOT}/validation/final-privacy.json",
    }
    candidates, confirmed, scanned = [], [], 0
    for relative in paths:
        path = REPO / relative
        try: content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError): continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if pattern.search(content):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}; candidates.append(row)
                if disposition == "confirmed_payload_hit": confirmed.append(row)
    return {"schema": "ghc.family.v651-v8.final-privacy.v1", "scanned_file_count": scanned, "pattern_classes": sorted(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Five structural classes over the owner surface with exact definition quarantine; zero confirmed hits is not complete privacy assurance."}


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {"path": relative, "git_blob": oid, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}


def build_manifest() -> None:
    exclusions = [f"{d.PHASE_ROOT}/validation/final-owner-manifest.json", f"{d.PHASE_ROOT}/validation/final-privacy.json", f"{d.PHASE_ROOT}/validation/final-staged-review.json", f"{d.PHASE_ROOT}/validation/final-candidate-validation.json", f"{d.PHASE_ROOT}/final/final-receipt.json"]
    for relative in exclusions:
        if relative == f"{d.PHASE_ROOT}/final/final-receipt.json":
            continue
        if relative.startswith(f"{d.PHASE_ROOT}/"):
            write_json(relative[len(d.PHASE_ROOT)+1:], {"state": "self_excluded_pending_refresh"})
    paths = owner_paths()
    entries = [hash_entry(path) for path in paths if path not in exclusions]
    privacy = privacy_scan(paths)
    write_json("validation/final-privacy.json", privacy)
    write_json("validation/final-owner-manifest.json", {"schema": "ghc.family.v651-v8.final-owner-manifest.v1", "hash_domain": "git_path_filtered_blob", "owner_path_count": len(paths), "entry_count": len(entries), "self_exclusion_count": len(exclusions), "self_exclusions": exclusions, "entries": entries, "coverage_boundary": "All Ilyra v651-v8 owner paths, including family-current runners created by this phase, except five declared self-referential or later-written receipts."})
    delta = [path for path in status_paths() if is_owner_path(path)]
    write_json("validation/final-staged-review.json", {"schema": "ghc.family.v651-v8.final-staged-review.v2", "delta_path_count": len(delta), "delta_paths": delta, "owner_path_count": len(paths), "manifest_entry_count": len(entries), "self_exclusion_count": len(exclusions), "privacy_confirmed_hits": privacy["confirmed_hit_count"], "x1_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", X1_HEAD, "HEAD"], cwd=REPO).returncode == 0, "evidence_head": EVIDENCE_HEAD, "original_final_head": ORIGINAL_FINAL_HEAD, "correction_exact_parent_candidate": git("rev-parse", "HEAD") == ORIGINAL_FINAL_HEAD, "terminal_route": "PREPARED_NOT_SENT"})


def build() -> None:
    if git("rev-parse", "HEAD") != ORIGINAL_FINAL_HEAD: raise RuntimeError("terminal correction must begin at the exact first final head")
    allowed = {
        "scripts/build_ghc_family_v651_v8_closeout.py",
        "scripts/ghc_family_v651_v8_closeout_validate.py",
        "scripts/ghc_family_v651_v8_final_validate.py",
        "tests/test_ghc_family_v651_v8_closeout.py",
        f"{d.PHASE_ROOT}/method-flow/closeout-incidents.json",
        f"{d.PHASE_ROOT}/method-flow/method-flow-ledger.json",
        f"{d.PHASE_ROOT}/method-flow/method-flow-summary.json",
        f"{d.PHASE_ROOT}/method-flow/method-flow-summary.md",
        f"{d.PHASE_ROOT}/method-flow/method-flow-validation-recheck.json",
    }
    for relative in (
        "deliverables/final-integrated-overview.md",
        "deliverables/final-static-report.html",
        "final/closeout-receipt.json",
        "final/commit-cap-contract.json",
        "final/complete-incomplete-checklist.json",
        "final/document-word-counts.json",
        "final/final-receipt.json",
        "final/phase-truth.json",
        "final/seal-receipt.json",
        "final/terminal-evidence-board.json",
        "handoffs/v651-v8-route-clarification-baton.md",
        "route/final-route-state.json",
        "truth/final-retained-negative-register.json",
        "validation/final-candidate-validation.json",
        "validation/final-owner-manifest.json",
        "validation/final-privacy.json",
        "validation/final-source-and-ancestry-contract.json",
        "validation/final-staged-review.json",
    ):
        allowed.add(f"{d.PHASE_ROOT}/{relative}")
    for number in range(17, 25):
        for suffix in ("method", "fail", "pass"):
            allowed.add(f"{d.PHASE_ROOT}/method-flow/records/v6518-m{number}-{suffix}.json")
    allowed.add(f"{d.PHASE_ROOT}/method-flow/records/v6518-m20-fail2.json")
    allowed.add(f"{d.PHASE_ROOT}/method-flow/records/v6518-m20-pass2.json")
    unexpected = [path for path in status_paths() if path not in allowed]
    if unexpected: raise RuntimeError(f"unexpected pre-closeout paths: {unexpected}")

    write_text("deliverables/final-integrated-overview.md", final_overview())
    static = (ROOT / "reports/accessible-static-report.html").read_text(encoding="utf-8")
    write_text("deliverables/final-static-report.html", static.replace("bounded evidence</title>", "sealed bounded evidence</title>").replace("bounded evidence</h1>", "sealed bounded evidence</h1>"))
    baton = baton_text(); write_text("handoffs/v651-v8-route-clarification-baton.md", baton)
    write_json("route/final-route-state.json", {"schema": "ghc.family.v651-v8.final-route.v1", "delivery_state": "PREPARED_NOT_SENT", "successor_exactly_resolved": False, "reason": "The newest governing activation supplies no exact successor title and phase and forbids silent normalization of the advisory route.", "messages_sent": 0, "tasks_created": 0, "tasks_forked": 0, "future_seats_named": 0, "future_seats_created": 0, "future_seats_launched": 0, "required_next_authority": "Hamish exact successor instruction"})
    final_truth = {"schema": "ghc.family.v651-v8.phase-truth.final.v2", "phase": d.PHASE, "owner": d.OWNER, "source_head": SOURCE_HEAD, "x1_head": X1_HEAD, "evidence_head": EVIDENCE_HEAD, "original_final_head": ORIGINAL_FINAL_HEAD, "outcome_counts": {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}, "effective_negatives": 7745, "negative_breakdown": {"inherited_effective": 7570, "x1_operational": 14, "x2_operational": 2, "closeout_and_terminal_operational": 9, "executed_synthetic": 150}, "effective_open_gaps": 60, "effective_exact_gates": 61, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "terminal_route": "PREPARED_NOT_SENT", "same_owner_only": True, "independent_reproduction_claimed": False, "full_repository_suite_run": False}
    write_json("final/phase-truth.json", final_truth)
    write_json("final/complete-incomplete-checklist.json", read_json(ROOT / "truth/complete-incomplete-checklist.json"))
    write_json("final/terminal-evidence-board.json", {"schema": "ghc.family.v651-v8.terminal-board.v2", "verdict": "NOT_READY_FOR_STAGE_20", "completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1, "effective_negatives": 7745, "open_gaps": 60, "exact_gates": 61, "canonical_final_state": "pending_new_postcommit_single_pass_after_zero_credit_import_failure", "route": "PREPARED_NOT_SENT"})
    write_json("final/closeout-receipt.json", {"schema": "ghc.family.v651-v8.closeout-receipt.v2", "state": "terminal_correction_candidate_complete", "evidence_head": EVIDENCE_HEAD, "original_final_head": ORIGINAL_FINAL_HEAD, "outcomes": final_truth["outcome_counts"], "negatives": 7745, "gaps": 60, "gates": 61, "verdict": "NOT_READY_FOR_STAGE_20", "documents_complete": True, "baton_word_count": len(baton.split()), "route": "PREPARED_NOT_SENT", "boundary": "Additive terminal correction candidate; the prior import failure has zero credit and a new exact committed-head pass remains pending."})
    write_json("truth/final-retained-negative-register.json", {"schema": "ghc.family.v651-v8.retained-negatives.final.v2", "effective": 7745, "inherited_effective": 7570, "x1_operational": 14, "x2_operational": 2, "closeout_and_terminal_operational": 9, "executed_synthetic": 150, "closeout_incident_ids": [f"V6518-CLOSE-N{number:02d}" for number in range(1, 10)], "no_failure_erased": True, "zero_first_pass_credit_for_failures": True, "boundary": "A bounded recovery never converts an earlier failure into a pass or independent evidence."})
    write_json("final/seal-receipt.json", {"schema": "ghc.family.v651-v8.seal-receipt.v2", "state": "terminal_correction_seal_candidate_complete", "source_head": SOURCE_HEAD, "x1_head": X1_HEAD, "evidence_head": EVIDENCE_HEAD, "original_final_head": ORIGINAL_FINAL_HEAD, "expected_phase_commits": 4, "expected_merges": 0, "expected_final_parents": 1, "commit_cap": 6, "canonical_exact_final_state": "pending_postcommit_single_pass"})
    write_json("final/final-receipt.json", {"schema": "ghc.family.v651-v8.final-receipt.v2", "state": "terminal_correction_candidate_complete", "exact_head": "resolved_only_by_postcommit_validator", "canonical_exact_final_state": "pending_postcommit_single_pass", "failed_canonical_attempts_retained": 1, "successful_canonical_passes": 0, "full_repository_suite_run": False, "independent_reproduction_claimed": False, "future_seats_launched": 0, "route": "PREPARED_NOT_SENT", "same_owner_only": True})
    write_json("final/commit-cap-contract.json", {"schema": "ghc.family.v651-v8.commit-cap.v2", "source_head": SOURCE_HEAD, "x1_commits": 1, "x2_evidence_commits": 1, "x2_closeout_and_correction_commits": 2, "planned_phase_total": 4, "maximum": 6, "merge_commits_allowed": 0})
    word_counts = []
    for path in ROOT.rglob("*.md"):
        relative = path.relative_to(ROOT).as_posix(); words = len(path.read_text(encoding="utf-8").split())
        word_counts.append({"path": relative, "words": words, "baton_exception": relative == "handoffs/v651-v8-route-clarification-baton.md"})
    write_json("final/document-word-counts.json", {"schema": "ghc.family.v651-v8.document-words.v1", "documents": word_counts, "non_baton_cap": 6000, "baton_minimum": 10000, "baton_maximum": 100000, "valid": all((row["baton_exception"] and 10000 <= row["words"] <= 100000) or (not row["baton_exception"] and row["words"] <= 6000) for row in word_counts)})
    write_json("validation/final-source-and-ancestry-contract.json", {"schema": "ghc.family.v651-v8.ancestry-contract.v2", "source": SOURCE_HEAD, "x1": X1_HEAD, "evidence": EVIDENCE_HEAD, "original_final": ORIGINAL_FINAL_HEAD, "final": "postcommit_exact_head", "expected_phase_commits": 4, "expected_merges": 0, "expected_final_parents": 1})
    write_repo("tests/test_ghc_family_v651_v8_closeout.py", closeout_tests())
    build_manifest()
    privacy = read_json(ROOT / "validation/final-privacy.json")
    if privacy["confirmed_hit_count"]: raise RuntimeError(f"final privacy hits: {privacy['confirmed_hits']}")
    print(json.dumps({"phase": d.PHASE, "state": "terminal_correction_built_not_committed", "baton_words": len(baton.split()), "owner_paths": read_json(ROOT / "validation/final-owner-manifest.json")["owner_path_count"], "manifest_entries": read_json(ROOT / "validation/final-owner-manifest.json")["entry_count"], "privacy_hits": 0, "route": "PREPARED_NOT_SENT"}, sort_keys=True))


if __name__ == "__main__":
    build()
