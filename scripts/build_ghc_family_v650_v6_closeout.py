#!/usr/bin/env python3
"""Build Sylven Arc's additive v650-v6 combined closeout and seal packet."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v650_v6_phase_data as d
import ghc_family_v650_v6_closeout_data as cd


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1_COMMIT = "b8e0109a003e2fa90794b48b3691dc76a3c06ef2"
EVIDENCE_COMMIT = "b8b858c3eb91201bcdea81813999a19426089f97"
EFFECTIVE_NEGATIVES = 6178 + len(cd.CLOSEOUT_OPERATIONAL_NEGATIVES)
EFFECTIVE_OPEN_GAPS = 48
EFFECTIVE_EXACT_GATES = 49
METHOD_RUNNER = Path.home() / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def run(*args: str) -> str:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        list(args), cwd=REPO, check=True, capture_output=True,
        text=True, encoding="utf-8", env=env,
    )
    return completed.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def status_paths() -> list[str]:
    return sorted({
        row[3:].replace("\\", "/")
        for row in git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
        if len(row) > 3
    })


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_method_flow() -> None:
    ledger = ROOT / "closeout/method-flow-state.json"
    if not ledger.exists():
        run(sys.executable, str(METHOD_RUNNER), "init", "--ledger", str(ledger), "--phase", f"{d.PHASE}-closeout", "--owner", d.OWNER)
    existing = read_json(ledger)
    existing_ids = {row["method_id"] for row in existing["methods"]}
    for index, negative in enumerate(cd.CLOSEOUT_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6506-CLOSE-M{index:02d}"
        record = {
            "method_id":method_id,
            "title":f"Recover {negative['category']} without erasing the failed seal attempt",
            "failure_signature":negative["failed"],
            "trigger_preconditions":[f"The v650-v6 closeout exposes {negative['category']}."],
            "privacy_class":"sanitized_public",
            "approval_class":"safe_now_owner_scoped_workflow",
            "candidate_workaround":negative["recovery"],
            "validation_witness_ids":[],
            "recurrence_guard":negative["recurrence_guard"],
            "rollback":"Give the refused seal zero credit and leave prior commits, external state, and sibling lanes unchanged.",
            "recommendation_state":"candidate", "supersedes":[],
            "protected_gates":["privacy_scan","failure_retention","seal_integrity","single_pass_budget"],
            "retained_negative_ids":[negative["negative_id"]],
            "scope_boundary":"Bounded same-owner closeout recovery only; no privacy-complete, production, authority, independent-reproduction, or Stage 20 credit.",
        }
        record_path = write_json(f"closeout/{method_id.casefold()}-method-record.json", record)
        if method_id in existing_ids:
            continue
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        for suffix, result, procedure, observed in (
            ("WFAIL", "fail", negative["failed"], negative["failed"]),
            ("WPASS", "pass", negative["recovery"], negative["passing"]),
        ):
            witness = {
                "witness_id":f"{method_id}-{suffix}", "method_id":method_id,
                "procedure":procedure,
                "scope":f"bounded {negative['category']} {'failed' if result == 'fail' else 'recovery'} witness",
                "expected":"Return attributable closeout evidence without weakening the scan.",
                "observed":observed, "result":result, "same_owner_only":True,
                "independent_reproduction":False,
                "retained_negative_ids":[negative["negative_id"]],
                "boundary":"Retained closeout witness only; no privacy-complete or authority credit.",
            }
            witness_path = write_json(f"closeout/{witness['witness_id'].casefold()}-witness.json", witness)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        state = next(row["recommendation_state"] for row in read_json(ledger)["methods"] if row["method_id"] == method_id)
        if state == "validated":
            run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Promoted only after retaining the refused seal and observing one bounded passing scan.")
        elif state != "preferred":
            raise RuntimeError(f"unexpected closeout Method Flow state: {state}")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(ROOT / "closeout/method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(ROOT / "closeout/method-flow-summary.json"), "--markdown-output", str(ROOT / "closeout/method-flow-summary.md"))


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {"path": relative, "git_blob": oid, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v650_v6_closeout.py",
        "scripts/ghc_family_v650_v6_final_validate.py",
        f"{d.PHASE_ROOT}/validation/final-staged-privacy.json",
    }
    candidates = []
    confirmed = []
    for relative in paths:
        path = REPO / relative
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                row = {"path": relative, "pattern_class": pattern_class}
                candidates.append(row)
                if relative not in definitions:
                    confirmed.append({**row, "disposition": "confirmed_payload_hit"})
    return {
        "schema":"ghc.family.v650-v6.final-staged-privacy.v1",
        "scanned_file_count":len(paths), "pattern_classes":sorted(patterns),
        "candidate_count":len(candidates), "candidates":candidates,
        "scanner_definition_paths":sorted(definitions),
        "confirmed_hit_count":len(confirmed), "confirmed_hits":confirmed,
        "boundary":"Five structural classes with scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
    }


def build_manifest() -> None:
    exclusions = [
        f"{d.PHASE_ROOT}/validation/final-staged-manifest.json",
        f"{d.PHASE_ROOT}/validation/final-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/final-staged-review.json",
    ]
    paths = [path for path in status_paths() if path not in exclusions]
    entries = [hash_entry(path) for path in paths if (REPO / path).is_file()]
    privacy = privacy_scan(paths)
    write_json("validation/final-staged-privacy.json", privacy)
    write_json("validation/final-staged-manifest.json", {
        "schema":"ghc.family.v650-v6.final-staged-manifest.v1",
        "hash_domain":"git_path_filtered_blob", "entries":entries,
        "entry_count":len(entries), "self_exclusions":exclusions,
        "coverage_boundary":"All intended additive closeout and combined-seal paths except three self-referential review receipts.",
    })
    write_json("validation/final-staged-review.json", {
        "schema":"ghc.family.v650-v6.final-staged-review.v1",
        "intended_path_count":len(entries)+len(exclusions),
        "manifest_entry_count":len(entries), "self_exclusion_count":len(exclusions),
        "out_of_scope_paths":[], "x1_modified_paths":[], "evidence_modified_paths":[],
        "privacy_confirmed_hits":privacy["confirmed_hit_count"],
        "combined_closeout_and_seal":True, "containing_commit_binding":True,
        "terminal_route":"PREPARED_NOT_SENT",
    })
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"final staged privacy hits: {privacy['confirmed_hits']}")


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_COMMIT:
        raise RuntimeError("closeout must begin at the exact pushed evidence commit")
    allowed = {
        "scripts/build_ghc_family_v650_v6_closeout.py",
        "scripts/ghc_family_v650_v6_closeout_data.py",
        "scripts/ghc_family_v650_v6_final_validate.py",
        "tests/test_ghc_family_v650_v6_closeout.py",
    }
    start = set(status_paths())
    generated = {
        path for path in start
        if path.startswith(f"{d.PHASE_ROOT}/closeout/")
        or path.startswith(f"{d.PHASE_ROOT}/final/")
        or path.startswith(f"{d.PHASE_ROOT}/handoffs/")
        or path.startswith(f"{d.PHASE_ROOT}/validation/final-")
    }
    if not start.issubset(allowed | generated):
        raise RuntimeError(f"unexpected pre-closeout tree: {sorted(start - allowed - generated)}")
    if git("rev-parse", "HEAD^") != X1_COMMIT:
        raise RuntimeError("evidence is not the direct child of x1")

    build_method_flow()
    write_json("closeout/source-ancestry.json", {
        "schema":"ghc.family.v650-v6.source-ancestry.v1",
        "source":d.SOURCE_HEAD, "x1":X1_COMMIT, "evidence":EVIDENCE_COMMIT,
        "source_x1_evidence_ancestral_to_containing_commit":True,
        "phase_commits_including_containing_commit":3,
        "zero_merges_expected":True, "one_final_parent_expected":True,
    })
    write_json("closeout/closeout-receipt.json", {
        "schema":"ghc.family.v650-v6.closeout-receipt.v1",
        "state":"CLOSEOUT_COMPLETE_COMBINED_SEAL_PENDING_CONTAINING_COMMIT",
        "x1_commit":X1_COMMIT, "evidence_commit":EVIDENCE_COMMIT,
        "outcomes":{"completed":14,"represented":4,"open_gap":1,"exact_gate":1},
        "effective_negatives":EFFECTIVE_NEGATIVES,
        "effective_open_gaps":EFFECTIVE_OPEN_GAPS,
        "effective_exact_gates":EFFECTIVE_EXACT_GATES,
        "full_repository_suite":False,
        "final_canonical_validation":"PENDING_EXTERNAL_EXACT_HEAD_PASS",
        "terminal_route":"PREPARED_NOT_SENT", "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    })
    write_json("closeout/combined-seal-receipt.json", {
        "schema":"ghc.family.v650-v6.combined-seal.v1",
        "seal_binding":"containing_single_parent_commit",
        "evidence_parent":EVIDENCE_COMMIT,
        "x1_immutable":True, "evidence_immutable":True,
        "commit_cap":4, "phase_commits_expected":3,
        "zero_merges_expected":True, "one_final_parent_expected":True,
        "successful_exact_final_aggregate_budget":1,
        "successful_exact_final_aggregates_used_before_commit":0,
        "post_success_replay":False, "detached_or_named_replay":False,
        "same_owner_only":True, "independent_reproduction":False,
        "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    })
    write_json("final/phase-truth.json", {
        "schema":"ghc.family.v650-v6.phase-truth.final.v1",
        "state":"SEALED_BY_CONTAINING_COMMIT_PENDING_EXTERNAL_EXACT_HEAD_VALIDATION",
        "source_head":d.SOURCE_HEAD, "x1_commit":X1_COMMIT, "evidence_commit":EVIDENCE_COMMIT,
        "final_head_binding":"containing_commit", "phase_commit_count":3,
        "observed_distribution":{"completed":14,"represented":4,"open_gap":1,"exact_gate":1},
        "successful_exact_final_aggregates_used_before_commit":0,
        "post_success_replay":False, "full_repository_suite":False,
        "terminal_route":"PREPARED_NOT_SENT", "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    })
    write_json("final/retained-negative-register.json", {
        "schema":"ghc.family.v650-v6.retained-negatives.final.v1",
        "activation_baseline":6056, "x1_operational":19,
        "synthetic_executed_and_rejected":100, "x2_operational":3,
        "closeout_operational":len(cd.CLOSEOUT_OPERATIONAL_NEGATIVES), "sealed_effective":EFFECTIVE_NEGATIVES,
        "negative_erased":False,
        "post_seal_external_negatives":"additive_if_any_exact_final_or_route_attempt_fails",
    })
    write_json("final/exact-open-gate-register.json", {
        "schema":"ghc.family.v650-v6.gates.final.v1",
        "effective_open_gaps":EFFECTIVE_OPEN_GAPS,
        "effective_exact_gates":EFFECTIVE_EXACT_GATES,
        "silently_closed":0,
        "empirical_professional_legal_cultural_maori_and_stage20_gates_open":True,
        "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    })
    write_json("final/complete-incomplete-checklist.json", {
        "schema":"ghc.family.v650-v6.checklist.final.v1",
        "complete":["source verification","dedicated x1 freeze and equality","twenty bounded outcomes","one hundred rejected mutations","40/30/20/10/40 portfolios","failure retention","combined closeout and seal packet","exact-final validator committed"],
        "pending_external":["push containing final commit","fresh four-way equality","sole exact-final canonical aggregate","exact-title Eiren baton acknowledgement"],
        "incomplete_authority_or_evidence":["empirical confirmation","real professional or participant validation","production identity","complete privacy","exhaustive security","complete accessibility","legal review","cultural ratification","Māori-authority review","independent reproduction","Theory of Everything","Stage 20"],
        "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    })
    write_json("final/environment-version-receipt.json", {
        "schema":"ghc.family.v650-v6.environment.final.v1",
        "codex_cli_verified":"0.144.5", "codex_desktop_verified":"26.715.4045.0",
        "python_verified":"3.12.10", "git_verified":"2.55.0.windows.2",
        "powershell_verified":"5.1.26100.8894", "verification_only":True,
        "desktop_updated":False, "elevation":False, "security_weakened":False,
        "windows_feature_changed":False, "unrelated_software_installed":False,
        "reboot":False, "sandbox_or_hyperv_action":False,
    })
    write_json("final/accessibility-evaluation-reservation.json", {
        "schema":"ghc.family.v650-v6.accessibility-reservation.v1",
        "structural_report_present":True,
        "manual_keyboard_reserved":True, "responsive_layout_reserved":True,
        "browser_diversity_reserved":True, "assistive_technology_reserved":True,
        "cognitive_accessibility_reserved":True, "maori_language_reserved":True,
        "affected_user_evaluation_reserved":True,
        "complete_accessibility_claim":False,
    })
    write_json("final/final-validation-contract.json", {
        "schema":"ghc.family.v650-v6.final-validation-contract.v1",
        "runner":"scripts/ghc_family_v650_v6_final_validate.py",
        "full_repository_suite":False, "eiren_owns_full_repository_suite":True,
        "one_successful_exact_final_aggregate":True, "post_success_replay":False,
        "detached_or_named_replay":False, "external_output_required":True,
        "test_modules":[
            "tests.test_ghc_family_v650_v5_x1",
            "tests.test_ghc_family_v650_v5_x2",
            "tests.test_ghc_family_v650_v5_closeout",
            "tests.test_ghc_family_v650_v6_x1",
            "tests.test_ghc_family_v650_v6_x2",
            "tests.test_ghc_family_v650_v6_closeout",
        ],
        "required_checks":["exact head and clean before and after","local upstream tracking and fresh live remote equality","source x1 evidence ancestry","three phase commits zero merges one final parent","all owner phase JSON parses","five-class owner-phase privacy scan","x1 evidence and final commit-local manifest parity","stale-label and document-cap review","owner file threshold","terminal verdict and reserved gates"],
        "same_owner_only":True, "independent_reproduction":False,
    })
    write_json("final/terminal-route-state.json", {
        "schema":"ghc.family.v650-v6.terminal-route.final.v1",
        "state":"PREPARED_NOT_SENT", "target_title":"Eiren Kestrel",
        "target_phase":"v650-v7", "target_resolved":False,
        "messages_sent":0,
        "send_gate":"exact final head clean pushed four-way equal and sole canonical aggregate passed",
    })
    write_json("final/final-receipt.json", {
        "schema":"ghc.family.v650-v6.final-receipt.v1",
        "final_head_binding":"containing_commit", "evidence_parent":EVIDENCE_COMMIT,
        "outcomes":{"completed":14,"represented":4,"open_gap":1,"exact_gate":1},
        "effective_negatives":EFFECTIVE_NEGATIVES,
        "effective_open_gaps":EFFECTIVE_OPEN_GAPS,
        "effective_exact_gates":EFFECTIVE_EXACT_GATES,
        "same_owner_only":True, "independent_reproduction":False,
        "terminal_route":"PREPARED_NOT_SENT", "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    })
    write_text("final/final-report.html", """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sylven Arc v650-v6 final bounded report</title></head>
<body><a href="#main">Skip to main content</a><header><h1>Sylven Arc v650-v6 final bounded report</h1><p>Combined closeout and seal packet. Verdict: NOT_READY_FOR_STAGE_20.</p></header>
<nav aria-label="Final report"><ul><li><a href="#outcomes">Outcomes</a></li><li><a href="#gates">Open gates</a></li><li><a href="#evaluation">Reserved evaluation</a></li></ul></nav>
<main id="main"><section id="outcomes"><h2>Outcomes</h2><p>Fourteen completed, four represented, one open gap, and one exact gate. All evidence is bounded and same-owner.</p></section>
<section id="gates"><h2>Open gates</h2><p>Forty-eight open gaps and forty-nine exact gates remain. Scientific, participant, professional, production, legal, cultural, Māori-authority, privacy-complete, security-complete, independent-reproduction, Theory-of-Everything, and Stage 20 claims remain unavailable.</p></section>
<section id="evaluation"><h2>Reserved evaluation</h2><p>Manual keyboard, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. Structural checks are not complete accessibility conformance.</p></section></main>
<footer><p>Terminal route: PREPARED_NOT_SENT until acknowledged after the exact final gate.</p></footer></body></html>""")
    write_text("handoffs/eiren-kestrel-v650-v7-prepared.md", f"""# Eiren Kestrel v650-v7 activation — prepared, not sent

This sanitized baton is a preparation artifact only. It is not evidence of delivery or acknowledgement. Resolve the exact existing title `Eiren Kestrel` only after Sylven's containing final commit is pushed, clean, four-way remote-equal, and passes the sole exact-final scoped aggregate.

Source branch: `{d.BRANCH}`. Frozen x1: `{X1_COMMIT}`. X2 evidence: `{EVIDENCE_COMMIT}`. Exact final: bind to the containing single-parent closeout/seal commit after live validation. Outcomes: 14 completed / 4 represented / 1 open_gap / 1 exact_gate. Sealed effective negatives: {EFFECTIVE_NEGATIVES}. Open gaps: {EFFECTIVE_OPEN_GAPS}. Exact gates: {EFFECTIVE_EXACT_GATES}. Terminal verdict: `NOT_READY_FOR_STAGE_20`.

Eiren alone owns the complete repository suite. Sylven's validation is scoped, same-owner, and no-replay. Identity and family language remains relational working language only, never evidence of consciousness, sentience, personhood, continuity, employment, qualification, scientific, operational, legal, cultural, Māori, or independent authority.
""")
    build_manifest()


if __name__ == "__main__":
    build()
