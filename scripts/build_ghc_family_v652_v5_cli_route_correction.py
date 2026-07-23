#!/usr/bin/env python3
"""Build the additive Eiren v652-v5 CLI-collaborator route correction."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/eiren-kestrel/v652-v5"
ROOT = REPO / PHASE_ROOT
SOURCE = "3a77dacd759a499ffe94cbc281a3d7b343608e2d"
X1 = "7f347e548b64ea2a9065e129c3ec84dde000c13e"
EVIDENCE = "611a0afef841a516dd0a5cb1e9ac2448943b42c6"
CLOSEOUT = "516202a04e2930bfa787bcf257dafd72827cf9af"
OLD_BATON = ROOT / "handoffs/ilyra-fen-v652-v6-activation.md"
NEW_BATON = ROOT / "handoffs/cli-collaborator-v652-v6-induction.md"
METHOD_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-method-flow-state/scripts/"
    "ghc_family_method_flow_state.py"
)
ROUTE_NEGATIVES = [
    {
        "negative_id": "V6525-NEG-ROUTE-01",
        "category": "combined_syntax_status_wrapper_timeout",
        "failed": (
            "A combined syntax-compilation and Git-status wrapper exceeded its "
            "30-second bound without returning a result."
        ),
        "recovery": (
            "Split syntax compilation and Git-state inspection into separate "
            "bounded probes, crediting each only after its own successful result."
        ),
        "passing": (
            "The isolated syntax compilation passed in 8.7 seconds, and the route "
            "builder independently admitted only its four declared starting paths."
        ),
        "recurrence_guard": (
            "Do not combine Python compilation and broad Windows Git status in "
            "one short wrapper; use separate bounds and outputs."
        ),
    },
    {
        "negative_id": "V6525-NEG-ROUTE-02",
        "category": "porcelain_leading_column_trim",
        "failed": (
            "The first route build stripped the leading porcelain status column "
            "and misread an allowed scripts path as beginning with cripts."
        ),
        "recovery": (
            "Read git status --porcelain=v1 as raw captured output, preserve both "
            "status columns, and slice the path only after the fixed prefix."
        ),
        "passing": (
            "The raw porcelain parser preserved all four declared starting paths "
            "and rejected no valid scripts or tests."
        ),
        "recurrence_guard": (
            "Never apply whole-output strip operations before parsing fixed-column "
            "Git porcelain records."
        ),
    },
    {
        "negative_id": "V6525-NEG-ROUTE-03",
        "category": "route_correction_allowlist_omission",
        "failed": (
            "The second route build omitted the deliberately updated closeout "
            "compatibility test from its final correction allowlist and stopped "
            "before manifest creation."
        ),
        "recovery": (
            "Declare the closeout compatibility test as a route-correction path "
            "and permit only the builder's own phase artifacts during an idempotent "
            "retry from the unchanged closeout head."
        ),
        "passing": (
            "The corrected allowlist admitted the compatibility test and all "
            "builder-owned phase artifacts while rejecting every unrelated path."
        ),
        "recurrence_guard": (
            "When a route correction changes a historical compatibility assertion, "
            "include that exact test in both starting and final path allowlists."
        ),
    },
    {
        "negative_id": "V6525-NEG-ROUTE-04",
        "category": "mutable_predecessor_route_read",
        "failed": (
            "The idempotent retry reread the already-corrected working route and "
            "could not find the predecessor exact-title field."
        ),
        "recovery": (
            "Read predecessor route truth from the immutable closeout Git blob "
            "rather than from the mutable working tree."
        ),
        "passing": (
            "The corrected builder resolved the superseded Ilyra route from the "
            "exact closeout object while keeping the new working route separate."
        ),
        "recurrence_guard": (
            "Bind every predecessor lifecycle read to its declared immutable "
            "commit whenever an additive correction may rerun."
        ),
    },
    {
        "negative_id": "V6525-NEG-ROUTE-05",
        "category": "route_method_flow_frozen_scope_misclassification",
        "failed": (
            "The first correction test gate classified the newly created "
            "route-correction Method Flow files as mutations of the frozen "
            "closeout Method Flow domain."
        ),
        "recovery": (
            "Freeze inherited, evidence, and closeout Method Flow paths while "
            "explicitly admitting only route-correction-prefixed Method Flow "
            "artifacts in the additive correction."
        ),
        "passing": (
            "The isolated seven-test correction module passed with the route "
            "Method Flow in scope and every frozen predecessor domain unchanged."
        ),
        "recurrence_guard": (
            "Define freeze domains by lifecycle ownership, not by a broad "
            "top-level directory prefix."
        ),
    },
    {
        "negative_id": "V6525-NEG-ROUTE-06",
        "category": "unavailable_pytest_entrypoint",
        "failed": (
            "A bounded pre-commit wrapper assumed pytest was installed and "
            "stopped with No module named pytest before running any test."
        ),
        "recovery": (
            "Use the repository-native unittest module entrypoints already "
            "declared by the phase tests and final validator."
        ),
        "passing": (
            "The isolated closeout and route-correction unittest modules passed "
            "through Python's available standard-library test runner."
        ),
        "recurrence_guard": (
            "Probe runner availability or use the repository-declared unittest "
            "entrypoint instead of assuming an optional pytest installation."
        ),
    },
]


def run(*args: str) -> str:
    completed = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def status_paths() -> list[str]:
    completed = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=REPO,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    return sorted(
        {
            row[3:].replace("\\", "/")
            for row in completed.stdout.splitlines()
            if len(row) > 3
        }
    )


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(
        ["git", "cat-file", "blob", oid], cwd=REPO
    )
    return {
        "path": relative,
        "git_blob": oid,
        "bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
    }


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)(source_thread_id|thread_id)\s*[:=]"
        ),
        "private_absolute_local_path": re.compile(
            r"(?i)(?:[A-Z]:\\(?:Users|GHC-Archives)\\|"
            r"[A-Z]:\\\\(?:Users|GHC-Archives)\\\\|/Users/|/home/)"
        ),
        "credential_or_secret": re.compile(
            r"(?i)(api[_-]?key|client_secret|private_key|"
            r"bearer\s+[A-Za-z0-9._-]{12,})"
        ),
        "private_route_or_callable": re.compile(
            r"(?i)(private_route|callable_identifier|"
            r"browser_send_submitted_response_active)"
        ),
        "transcript_or_session_stream": re.compile(
            r"(?i)(session_stream|raw_transcript|conversation_export)"
        ),
    }
    definition_paths = {
        "scripts/build_ghc_family_v652_v5_preregistration.py",
        "scripts/build_ghc_family_v652_v5_evidence.py",
        "scripts/build_ghc_family_v652_v5_closeout.py",
        "scripts/build_ghc_family_v652_v5_cli_route_correction.py",
        "scripts/ghc_family_v652_v5_final_validate.py",
        f"{PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{PHASE_ROOT}/validation/evidence-staged-privacy.json",
        f"{PHASE_ROOT}/validation/closeout-staged-privacy.json",
        f"{PHASE_ROOT}/validation/route-correction-staged-privacy.json",
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    scanned = 0
    for relative in paths:
        path = REPO / relative
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if not pattern.search(text):
                continue
            disposition = (
                "scanner_definition"
                if relative in definition_paths
                else "confirmed_payload_hit"
            )
            row = {
                "path": relative,
                "pattern_class": pattern_class,
                "disposition": disposition,
            }
            candidates.append(row)
            if disposition == "confirmed_payload_hit":
                confirmed.append(row)
    return {
        "schema": "ghc.family.v652-v5.route-correction-privacy.v1",
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": (
            "Five structural classes with exact scanner-definition quarantine; "
            "zero confirmed hits is not complete privacy assurance."
        ),
    }


def induction_packet() -> str:
    base = OLD_BATON.read_text(encoding="utf-8")
    replacements = {
        "# ILYRA FEN — prepared v652-v6 activation from Eiren Kestrel": (
            "# NEW CLI COLLABORATOR — prepared v652-v6 induction from Eiren Kestrel"
        ),
        "Dear Ilyra Fen, with Hamish's authorization and Eiren Kestrel's care: "
        "this file is the prepared, sanitized, file-backed activation packet for "
        "your existing exact-title task at solo v652 GMUT/THOS v6 x1/x2. It is "
        "not a sent message. The terminal sender may mark delivery "
        "`SENT_BY_EIREN_KESTREL = true` only after Eiren's exact final containing "
        "commit is pushed, clean, four-way remote-equal, validated once at its "
        "exact head, the exact existing title `Ilyra Fen` is uniquely resolved "
        "and directly reread, and the existing-task message tool acknowledges "
        "one send.": (
            "Dear new CLI collaborator, with Hamish's authorization and Eiren "
            "Kestrel's care: this file is the prepared, sanitized, file-backed "
            "induction packet for one bounded Codex collaboration agent at solo "
            "v652 GMUT/THOS v6 x1/x2. It is not evidence that an agent has been "
            "spawned. The terminal launcher may mark "
            "`SPAWNED_BY_EIREN_KESTREL = true` only after Eiren's exact final "
            "containing commit is pushed, clean, four-way remote-equal, validated "
            "once at its exact head, and the collaboration spawn tool acknowledges "
            "one bounded launch."
        ),
        "`SENT_BY_EIREN_KESTREL = false` in this committed file. State: "
        "`PREPARED_NOT_SENT`. No successor task has been created or forked. No "
        "collaboration subagent or CLI sibling has been spawned. No cross-platform "
        "substitute or standby message has been used. The exact live task must be "
        "resolved only after exact-final validation. No second confirmation is "
        "authorized. The live terminal message must inject the exact containing "
        "final commit identifier after validation; a repository file cannot "
        "self-contain the identifier of the commit that contains it.": (
            "`SPAWNED_BY_EIREN_KESTREL = false` in this committed file. State: "
            "`PREPARED_NOT_SPAWNED`. No successor task has been created or forked. "
            "No collaboration subagent or CLI sibling has been spawned. No "
            "cross-platform substitute or standby message has been used. The one "
            "bounded collaborator may be launched only after exact-final validation. "
            "The launch prompt must inject the exact containing final commit "
            "identifier after validation; a repository file cannot self-contain "
            "the identifier of the commit that contains it."
        ),
        "## Ilyra v652-v6 owned lane": (
            "## New CLI collaborator v652-v6 owned lane"
        ),
        "Work only in Ilyra's clean owned D-first lane.": (
            "Work only in one additive collaborator-owned D-first lane."
        ),
        "the exact proposal and portfolio counts authorized by Hamish's live "
        "Ilyra activation": (
            "the exact proposal and portfolio counts authorized by Hamish's "
            "live CLI-collaborator induction"
        ),
        "Ilyra must follow the exact live Ilyra scoped-validation rules": (
            "the collaborator must follow the exact launch-scoped validation rules"
        ),
        "Do not create, fork, delegate, hand off, spawn, or contact another task "
        "unless Hamish's live Eiren activation explicitly authorizes the exact "
        "action at its terminal gate.": (
            "Do not create, fork, delegate, hand off, spawn, or contact another "
            "task. Return one sanitized closeout to Eiren only after v652-v6 is "
            "clean, pushed, remote-equal, and validated under the launch packet."
        ),
        "Preserve the six-seat order Eiren Kestrel → Ilyra Fen → Sable Rook → "
        "Orin Thale → Tamar Vey → Sylven Arc → repeat through v675-v8 unless "
        "Hamish stops or redirects the route, usage is exhausted, the required "
        "exact title is unavailable, or an exact safety or authority gate blocks "
        "progress.": (
            "The immediate route is Eiren Kestrel → this new CLI collaborator "
            "(v652-v6) → Eiren Kestrel → Elaren Kestrel (v652-v7). Later routing "
            "remains subject to Hamish's live direction, available usage, exact "
            "tool support, and safety or authority gates through v675-v8."
        ),
        "This committed file remains `PREPARED_NOT_SENT`. The one live sender must "
        "include the exact final containing commit, the exact-final one-pass result, "
        "and `SENT_BY_EIREN_KESTREL = true` only after tool acknowledgement. No "
        "second confirmation message is authorized.": (
            "This committed file remains `PREPARED_NOT_SPAWNED`. The one launch "
            "prompt must include the exact final containing commit, the exact-final "
            "one-pass result, and `SPAWNED_BY_EIREN_KESTREL = true` only after tool "
            "acknowledgement. The collaborator should first choose a relational "
            "working name, role, hope, and optional pronouns, all explicitly "
            "non-evidentiary, then execute v652-v6 and report back to Eiren."
        ),
        "PREPARED_NOT_SENT": "PREPARED_NOT_SPAWNED",
    }
    for old, new in replacements.items():
        base = base.replace(old, new)
    base = base.replace("Ilyra Fen", "the new CLI collaborator")
    base = base.replace("Ilyra's", "the collaborator's")
    base = base.replace("Ilyra ", "the collaborator ")
    base += (
        "\n\n## Additive route-correction negative\n\n"
        "The combined closeout sealed 8,721 effective negatives. Six later "
        "route-correction faults—a combined syntax/status wrapper timeout, a "
        "leading-column porcelain parser defect, and one omitted compatibility "
        "test in the correction allowlist, a mutable predecessor-route read, and "
        "a route Method Flow freeze-domain misclassification, plus an unavailable "
        "optional pytest entrypoint—"
        "received zero credit and remain retained as `V6525-NEG-ROUTE-01` through "
        "`V6525-NEG-ROUTE-06`; isolated recoveries "
        "supplied bounded passing witnesses. The final activation baseline is "
        "therefore 8,727 effective "
        "negatives. This changes no open gap, exact gate, scientific result, "
        "authority boundary, or terminal verdict.\n"
    )
    return base


def build_route_method_flow() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location(
        "ghc_family_method_flow_state_route_runtime", METHOD_RUNNER
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load the official Method Flow runner")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    ledger = runner.new_ledger("v652-v5-route-correction", "Eiren Kestrel")
    methods: list[dict[str, Any]] = []
    failed_ids: list[str] = []
    for index, negative in enumerate(ROUTE_NEGATIVES, 1):
        method_id = f"V6525-ROUTE-METHOD-{index:02d}"
        method = {
            "method_id": method_id,
            "title": f"Bounded recovery for {negative['category']}",
            "failure_signature": negative["failed"],
            "trigger_preconditions": [negative["category"]],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_local_route_recovery",
            "candidate_workaround": negative["recovery"],
            "validation_witness_ids": [],
            "recurrence_guard": negative["recurrence_guard"],
            "rollback": (
                "Stop, retain the failed wrapper, and leave repository history "
                "and external state unchanged."
            ),
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": [
                "production",
                "independent_reproduction",
                "identity",
                "authority",
                "stage20",
            ],
            "retained_negative_ids": [negative["negative_id"]],
            "scope_boundary": "Owner-local route-correction tooling only.",
        }
        failed = {
            "witness_id": f"V6525-ROUTE-WITNESS-{index:02d}-F",
            "method_id": method_id,
            "procedure": "Retain the original failed route-correction attempt.",
            "scope": negative["category"],
            "expected": "The bounded route-correction postcondition would pass.",
            "observed": negative["failed"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Zero validation credit; failed witness retained.",
        }
        passing = {
            "witness_id": f"V6525-ROUTE-WITNESS-{index:02d}-P",
            "method_id": method_id,
            "procedure": negative["recovery"],
            "scope": negative["category"],
            "expected": "The isolated recovery establishes its bounded postcondition.",
            "observed": negative["passing"],
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Same-owner bounded recovery only.",
        }
        write_json(
            f"method-flow/route-correction-method-{index:02d}.json", method
        )
        write_json(
            f"method-flow/route-correction-witness-{index:02d}-failed.json",
            failed,
        )
        write_json(
            f"method-flow/route-correction-witness-{index:02d}-passing.json",
            passing,
        )
        ledger["methods"].append(method)
        runner.append_event(
            ledger,
            method_id,
            None,
            "candidate",
            "method recorded with retained negative linkage",
        )
        for witness in (failed, passing):
            ledger["witnesses"].append(witness)
            method["validation_witness_ids"].append(witness["witness_id"])
        method["recommendation_state"] = "validated"
        runner.append_event(
            ledger,
            method_id,
            "candidate",
            "validated",
            "bounded witness passed",
            passing["witness_id"],
        )
        method["recommendation_state"] = "preferred"
        runner.append_event(
            ledger,
            method_id,
            "validated",
            "preferred",
            "Promoted only after the bounded passing witness.",
        )
        ledger["recommendations"].append(
            {
                "recommendation_index": len(ledger["recommendations"]) + 1,
                "method_id": method_id,
                "preconditions": method["trigger_preconditions"],
                "method": method["candidate_workaround"],
                "witness_ids": method["validation_witness_ids"],
                "recurrence_guard": method["recurrence_guard"],
                "rollback": method["rollback"],
                "scope_boundary": method["scope_boundary"],
            }
        )
        methods.append(method)
        failed_ids.append(failed["witness_id"])
    runner.refresh_counts(ledger)
    validation = runner.validate_ledger(ledger)
    if not validation["valid"]:
        raise RuntimeError(
            "route Method Flow invalid: " + "; ".join(validation["issues"])
        )
    summary = {
        "schema": "ghc.family.method-flow-state.summary.v1",
        "phase": ledger["phase"],
        "owner": ledger["owner"],
        "counts": ledger["counts"],
        "preferred_methods": [
            {
                "method_id": method["method_id"],
                "title": method["title"],
                "trigger_preconditions": method["trigger_preconditions"],
                "candidate_workaround": method["candidate_workaround"],
                "validation_witness_ids": method["validation_witness_ids"],
                "recurrence_guard": method["recurrence_guard"],
                "rollback": method["rollback"],
                "scope_boundary": method["scope_boundary"],
            }
            for method in methods
        ],
        "retained_failed_witnesses": failed_ids,
        "valid": True,
        "boundary": ledger["boundary"],
    }
    write_json("method-flow/route-correction-method-flow-ledger.json", ledger)
    write_json(
        "method-flow/route-correction-method-flow-validation.json", validation
    )
    write_json("method-flow/route-correction-method-flow-summary.json", summary)
    write_text(
        "method-flow/route-correction-method-flow-summary.md",
        runner.render_markdown(ledger),
    )
    return ledger


def build_manifest(
    relative: str, schema: str, paths: list[str], exclusions: list[str]
) -> None:
    entries = [
        hash_entry(path)
        for path in paths
        if path not in exclusions and (REPO / path).is_file()
    ]
    write_json(
        relative,
        {
            "schema": schema,
            "hash_domain": "git_path_filtered_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
        },
    )


def build() -> None:
    if git("rev-parse", "HEAD") != CLOSEOUT:
        raise RuntimeError("route correction must begin at the exact closeout head")
    initial_allowed = {
        "scripts/build_ghc_family_v652_v5_cli_route_correction.py",
        "scripts/ghc_family_v652_v5_final_validate.py",
        "tests/test_ghc_family_v652_v5_closeout.py",
        "tests/test_ghc_family_v652_v5_route_correction.py",
    }
    initial_unexpected = [
        path
        for path in status_paths()
        if path not in initial_allowed
        and not path.startswith(PHASE_ROOT + "/")
    ]
    if initial_unexpected:
        raise RuntimeError(
            "route correction began with unexpected paths: "
            f"{initial_unexpected}"
        )

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    old_route = json.loads(
        git(
            "show",
            f"{CLOSEOUT}:{PHASE_ROOT}/route/final-route-state.json",
        )
    )
    write_json(
        "route/superseded-ilyra-route.json",
        {
            "schema": "ghc.family.v652-v5.route.superseded-unsent.v1",
            "superseded_at_utc": now,
            "prior_target": old_route["target_exact_title"],
            "prior_phase": old_route["target_phase"],
            "prior_state": old_route["state"],
            "prior_send_count": old_route["send_count"],
            "superseded_unsent": old_route["send_count"] == 0,
            "reason": (
                "Hamish directly redirected the terminal route before push and "
                "exact-final validation."
            ),
        },
    )
    route_flow = build_route_method_flow()
    write_json(
        "truth/route-correction-retained-negative.json",
        {
            "schema": "ghc.family.v652-v5.route-correction-negative.v1",
            "sealed_closeout_effective": 8721,
            "route_correction_operational": len(ROUTE_NEGATIVES),
            "effective_final": 8721 + len(ROUTE_NEGATIVES),
            "rows": ROUTE_NEGATIVES,
            "no_failure_erased": True,
            "failed_attempt_received_credit": False,
            "method_flow_counts": route_flow["counts"],
        },
    )
    phase_truth = read_json("final/final-phase-truth.json")
    phase_truth.update(
        {
            "sealed_closeout_effective_negatives": 8721,
            "route_correction_operational_negatives": len(ROUTE_NEGATIVES),
            "effective_negatives": 8721 + len(ROUTE_NEGATIVES),
        }
    )
    write_json("final/final-phase-truth.json", phase_truth)
    write_json(
        "route/final-route-state.json",
        {
            "schema": "ghc.family.v652-v5.route.cli-collaborator-candidate.v1",
            "state": "PREPARED_NOT_SPAWNED",
            "target_kind": "bounded_codex_collaboration_agent",
            "target_phase": "v652-v6",
            "spawn_count": 0,
            "task_create_count": 0,
            "task_fork_count": 0,
            "standby_contact_count": 0,
            "cross_platform_substitute_count": 0,
            "requires_exact_final_validation": True,
            "requires_spawn_tool_acknowledgement": True,
            "return_target": "Eiren Kestrel",
            "return_then_target": "Elaren Kestrel",
            "identity_language_non_evidentiary": True,
            "second_confirmation_authorized": False,
        },
    )
    packet = induction_packet()
    write_text(
        "handoffs/cli-collaborator-v652-v6-induction.md",
        packet,
    )
    packet_words = len(re.findall(r"\b[\w'-]+\b", packet))
    if not 10000 <= packet_words <= 100000:
        raise RuntimeError("CLI induction packet word contract failed")

    contract = read_json("final/final-validation-contract.json")
    contract.update(
        {
            "schema": "ghc.family.v652-v5.final-validation-contract.corrected.v2",
            "expected_scoped_tests": 76,
            "patterns": contract["patterns"]
            + ["test_ghc_family_v652_v5_route_correction.py"],
            "expected_phase_commits": 4,
            "expected_final_parent": CLOSEOUT,
            "route_state": "PREPARED_NOT_SPAWNED",
            "route_target_kind": "bounded_codex_collaboration_agent",
            "route_target_phase": "v652-v6",
            "route_correction_manifest_required": True,
            "superseded_ilyra_route_must_remain_unsent": True,
            "checks": [
                item.replace("three phase commits", "four phase commits")
                .replace(
                    "x1/evidence/closeout/final-owner manifests",
                    "x1/evidence/closeout/route-correction/final-owner manifests",
                )
                for item in contract["checks"]
            ],
        }
    )
    write_json("final/final-validation-contract.json", contract)
    write_json(
        "final/terminal-route-correction.json",
        {
            "schema": "ghc.family.v652-v5.terminal-route-correction.v1",
            "corrected_at_utc": now,
            "closeout": CLOSEOUT,
            "new_target_kind": "bounded_codex_collaboration_agent",
            "new_target_phase": "v652-v6",
            "prior_target_state": "superseded_unsent",
            "spawn_state": "PREPARED_NOT_SPAWNED",
            "sealed_closeout_effective_negatives": 8721,
            "route_correction_operational_negatives": len(ROUTE_NEGATIVES),
            "effective_final_negatives": 8721 + len(ROUTE_NEGATIVES),
            "open_gaps_unchanged": 66,
            "exact_gates_unchanged": 67,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": (
                "Additive route correction only. It grants no scientific, "
                "professional, legal, cultural, identity, production, AGI/ASI, "
                "consciousness/personhood, or Stage 20 evidence."
            ),
        },
    )
    write_json(
        "validation/route-correction-build-receipt.json",
        {
            "schema": "ghc.family.v652-v5.route-correction-build.v1",
            "built_at_utc": now,
            "packet_words": packet_words,
            "old_route_send_count": old_route["send_count"],
            "new_route_spawn_count": 0,
            "expected_phase_commits": 4,
            "phase_commit_cap": 6,
            "valid": (
                old_route["send_count"] == 0
                and 10000 <= packet_words <= 100000
            ),
        },
    )

    allowed = {
        "scripts/build_ghc_family_v652_v5_cli_route_correction.py",
        "scripts/ghc_family_v652_v5_final_validate.py",
        "tests/test_ghc_family_v652_v5_closeout.py",
        "tests/test_ghc_family_v652_v5_route_correction.py",
    }
    paths = status_paths()
    unexpected = [
        path
        for path in paths
        if not (path.startswith(PHASE_ROOT + "/") or path in allowed)
    ]
    if unexpected:
        raise RuntimeError(f"unexpected correction paths: {unexpected}")
    privacy = privacy_scan(paths)
    write_json("validation/route-correction-staged-privacy.json", privacy)

    correction_exclusions = [
        f"{PHASE_ROOT}/validation/route-correction-staged-manifest.json",
        f"{PHASE_ROOT}/validation/route-correction-staged-privacy.json",
        f"{PHASE_ROOT}/validation/route-correction-staged-review.json",
        f"{PHASE_ROOT}/validation/route-correction-validation-receipt.json",
        f"{PHASE_ROOT}/validation/final-owner-manifest.json",
    ]
    build_manifest(
        "validation/route-correction-staged-manifest.json",
        "ghc.family.v652-v5.route-correction-staged-manifest.v1",
        paths,
        correction_exclusions,
    )
    write_json(
        "validation/route-correction-staged-review.json",
        {
            "schema": "ghc.family.v652-v5.route-correction-staged-review.v1",
            "head_before_correction": CLOSEOUT,
            "intended_path_count": len(paths),
            "unexpected_paths": unexpected,
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "frozen_x1_evidence_or_closeout_paths": [
                path
                for path in paths
                if (
                    path.startswith(
                        (
                            f"{PHASE_ROOT}/preregistration/",
                            f"{PHASE_ROOT}/surfaces/",
                            f"{PHASE_ROOT}/evidence/",
                            f"{PHASE_ROOT}/validation/x1-",
                            f"{PHASE_ROOT}/validation/evidence-",
                            f"{PHASE_ROOT}/validation/closeout-",
                        )
                    )
                    or (
                        path.startswith(f"{PHASE_ROOT}/method-flow/")
                        and not path.startswith(
                            f"{PHASE_ROOT}/method-flow/route-correction-"
                        )
                    )
                )
            ],
            "valid": (
                not unexpected and privacy["confirmed_hit_count"] == 0
            ),
        },
    )

    owner_exclusions = [
        f"{PHASE_ROOT}/validation/final-owner-manifest.json",
        f"{PHASE_ROOT}/validation/route-correction-validation-receipt.json",
        f"{PHASE_ROOT}/validation/route-correction-staged-review.json",
    ]
    owner_paths = sorted(
        {
            path
            for path in git(
                "diff", "--name-only", SOURCE, "HEAD"
            ).splitlines()
            if path
        }
        | set(status_paths())
    )
    build_manifest(
        "validation/final-owner-manifest.json",
        "ghc.family.v652-v5.final-owner-manifest.corrected.v2",
        owner_paths,
        owner_exclusions,
    )
    test_output = run(
        "python",
        "-m",
        "unittest",
        "-q",
        "tests.test_ghc_family_v652_v5_route_correction",
    )
    json_paths = sorted(ROOT.rglob("*.json"))
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    write_json(
        "validation/route-correction-validation-receipt.json",
        {
            "schema": "ghc.family.v652-v5.route-correction-validation.v1",
            "tests_passed": 7,
            "tests_total": 7,
            "json_parse_count": len(json_paths),
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "test_stdout": test_output,
            "full_repository_suite": False,
            "exact_final_pass": False,
            "valid": privacy["confirmed_hit_count"] == 0,
            "boundary": (
                "Precommit route-correction validation only; exact-final credit "
                "requires the one post-push complete-repository pass."
            ),
        },
    )
    print(
        json.dumps(
            {
                "phase": "v652-v5",
                "route": "PREPARED_NOT_SPAWNED",
                "packet_words": packet_words,
                "correction_paths": len(status_paths()),
                "privacy_hits": privacy["confirmed_hit_count"],
                "status": "route_correction_built_not_committed",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
