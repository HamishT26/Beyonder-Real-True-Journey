#!/usr/bin/env python3
"""Build the additive terminal-validation correction for Ilyra v650-v2."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "ilyra-fen" / "v650-v2"
SOURCE = "f47cd5145647965935f80d67751f0e09d9740540"
X1 = "d70cbab27e64e12d634e0d9b94b73f50aa507ad1"
EVIDENCE = "2c54ccf284f3a9faf7c3cd5809b83af46faa7594"
CLOSEOUT = "ed23f25accb780b542315f4f97e5ba96c98e069f"
BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
METHOD_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"
PRIVACY = {
    "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
    "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
    "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
    "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
    "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
}

if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_v650_v2_validate as validator  # noqa: E402


def run(*args: str, check: bool = True, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=ROOT, check=check, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=timeout,
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def write_json(relative: str, payload: Any) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def load(relative: str) -> dict[str, Any]:
    return json.loads((OUT / relative).read_text(encoding="utf-8"))


def status_paths() -> list[str]:
    raw = run("git", "status", "--porcelain=v1", "-z", "--untracked-files=all").stdout
    paths: list[str] = []
    for record in (row for row in raw.split("\0") if row):
        value = record[3:]
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        paths.append(value.strip('"').replace("\\", "/"))
    return sorted(set(paths))


def build_method_flow(targeted_privacy: dict[str, Any]) -> dict[str, Any]:
    ledger = OUT / "method-flow" / "method-flow-terminal-ledger.json"
    if not ledger.exists():
        write_json("method-flow/method-flow-terminal-ledger.json", load("method-flow/method-flow-ledger-x2.json"))
    method_id = "V6502-M12"
    negative_id = "NEG-V6502-VALID-001"
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if method_id not in {row["method_id"] for row in current["methods"]}:
        record = {
            "method_id": method_id,
            "title": "Classify every committed privacy receipt as a scanner-definition surface",
            "failure_signature": "The first exact-final aggregate classified two scanner-definition strings in the final staged privacy receipt as confirmed payload hits.",
            "trigger_preconditions": ["An exact-final privacy scan includes a committed scanner receipt that describes its own definition candidates."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_validation_correction",
            "candidate_workaround": "Add the exact committed scanner-receipt filename to the definition allowlist, preserve the failed aggregate, and exercise only the classifier before rebuilding terminal manifests.",
            "validation_witness_ids": [],
            "recurrence_guard": "Enumerate every committed scanner-definition receipt explicitly and leave all unmatched files fail-closed as payload candidates.",
            "rollback": "Give the failed aggregate zero successful-pass credit, keep the route held, and revert only the classifier correction if its bounded witness fails.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["privacy", "failure_retention", "single_success_budget", "terminal_route"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": "Classifier correction only; no privacy-complete, security-complete, independent-reproduction, or authority credit.",
        }
        record_path = write_json("method-flow/v6502-m12-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        witnesses = [
            {
                "witness_id": "V6502-M12-WFAIL",
                "method_id": method_id,
                "procedure": "Run the first exact-final canonical aggregate with the incomplete scanner-receipt allowlist.",
                "scope": "exact-final aggregate failure",
                "expected": "Every scanner-definition receipt is classified separately from payload hits.",
                "observed": "Two definition strings in one committed scanner receipt were misclassified as payload hits; the aggregate failed and used zero successful-pass credit.",
                "result": "fail",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [negative_id],
                "boundary": "Retained failed aggregate; no pass, privacy, security, or terminal-send credit.",
            },
            {
                "witness_id": "V6502-M12-WPASS",
                "method_id": method_id,
                "procedure": "Add only the omitted scanner-receipt filename and run the bounded privacy classifier without rerunning the canonical aggregate.",
                "scope": "targeted classifier recovery",
                "expected": "The same owner packet yields zero confirmed payload hits while scanner-definition candidates remain visible.",
                "observed": f"The targeted classifier scanned {targeted_privacy['file_count']} owner files, retained {targeted_privacy['candidate_count']} definition candidates, and confirmed zero payload hits.",
                "result": "pass",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [negative_id],
                "boundary": "Targeted classifier witness only; the corrected exact-final aggregate remains pending.",
            },
        ]
        for witness in witnesses:
            witness_path = write_json(f"method-flow/{witness['witness_id'].casefold()}-witness.json", witness)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        run(
            sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger),
            "--method-id", method_id, "--state", "preferred", "--note",
            "Preferred only for an exact scanner-receipt omission after one retained aggregate failure and one bounded classifier witness.",
        )
    validation = OUT / "method-flow" / "method-flow-validation-terminal.json"
    summary_json = OUT / "method-flow" / "method-flow-summary-terminal.json"
    summary_md = OUT / "method-flow" / "method-flow-summary-terminal.md"
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(validation))
    run(
        sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger),
        "--json-output", str(summary_json), "--markdown-output", str(summary_md),
    )
    return json.loads(summary_json.read_text(encoding="utf-8"))


def build_staged_privacy() -> dict[str, Any]:
    exclusions = {
        "docs/ilyra-fen/v650-v2/validation/terminal-correction-staged-privacy.json",
        "docs/ilyra-fen/v650-v2/validation/terminal-correction-owner-manifest.json",
        "docs/ilyra-fen/v650-v2/validation/terminal-correction-staged-manifest.json",
        "docs/ilyra-fen/v650-v2/validation/terminal-correction-staged-review.json",
    }
    paths = [path for path in status_paths() if path not in exclusions]
    definitions = {
        "scripts/ghc_family_v650_v2_validate.py",
        "scripts/build_ghc_family_v650_v2_terminal_correction.py",
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in PRIVACY.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": name, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    payload = {
        "schema": "ghc.family.v650-v2.terminal-correction-privacy.v1",
        "scanned_file_count": len(paths),
        "pattern_class_count": len(PRIVACY),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "self_exclusions": sorted(exclusions),
    }
    write_json("validation/terminal-correction-staged-privacy.json", payload)
    return payload


def build_owner_manifest() -> dict[str, Any]:
    exclusions = {
        "docs/ilyra-fen/v650-v2/validation/terminal-correction-owner-manifest.json",
        "docs/ilyra-fen/v650-v2/validation/terminal-correction-staged-manifest.json",
        "docs/ilyra-fen/v650-v2/validation/terminal-correction-staged-review.json",
    }
    entries: list[dict[str, Any]] = []
    for path in sorted(item for item in OUT.rglob("*") if item.is_file()):
        relative = path.relative_to(ROOT).as_posix()
        if relative in exclusions:
            continue
        data = path.read_bytes()
        entries.append({"path": relative, "bytes": len(data), "git_blob": git("hash-object", f"--path={relative}", relative), "checkout_sha256": hashlib.sha256(data).hexdigest()})
    payload = {"schema": "ghc.family.v650-v2.terminal-correction-owner-manifest.v1", "hash_domain": "git_hash_object_path_filtered_blob", "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(exclusions)}
    write_json("validation/terminal-correction-owner-manifest.json", payload)
    return payload


def build_staged_manifest() -> dict[str, Any]:
    exclusions = {
        "docs/ilyra-fen/v650-v2/validation/terminal-correction-staged-manifest.json",
        "docs/ilyra-fen/v650-v2/validation/terminal-correction-staged-review.json",
    }
    paths = [path for path in status_paths() if path not in exclusions]
    entries: list[dict[str, Any]] = []
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        entries.append({"path": relative, "bytes": len(data), "git_blob": git("hash-object", f"--path={relative}", relative), "checkout_sha256": hashlib.sha256(data).hexdigest()})
    payload = {"schema": "ghc.family.v650-v2.terminal-correction-staged-manifest.v1", "hash_domain": "git_hash_object_path_filtered_blob", "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(exclusions)}
    write_json("validation/terminal-correction-staged-manifest.json", payload)
    return payload


def build_staged_review(manifest: dict[str, Any], privacy: dict[str, Any]) -> dict[str, Any]:
    paths = [row["path"] for row in manifest["entries"]]
    allowed = [
        path for path in paths
        if path.startswith("docs/ilyra-fen/v650-v2/")
        or path in {"scripts/ghc_family_v650_v2_validate.py", "scripts/build_ghc_family_v650_v2_terminal_correction.py", "tests/test_ghc_family_v650_v2_correction.py"}
    ]
    out_of_scope = sorted(set(paths) - set(allowed))
    evidence_paths = set(git("ls-tree", "-r", "--name-only", EVIDENCE).splitlines())
    evidence_changes = sorted(set(paths) & evidence_paths)
    closeout_paths = set(git("ls-tree", "-r", "--name-only", CLOSEOUT).splitlines())
    closeout_changes = sorted(set(paths) & closeout_paths)
    expected_closeout_changes = ["scripts/ghc_family_v650_v2_validate.py"]
    payload = {
        "schema": "ghc.family.v650-v2.terminal-correction-staged-review.v1",
        "intended_path_count": len(paths) + len(manifest["self_exclusions"]),
        "manifest_entry_count": len(paths),
        "self_exclusion_count": len(manifest["self_exclusions"]),
        "out_of_scope_paths": out_of_scope,
        "evidence_frozen_changes": evidence_changes,
        "closeout_changes": closeout_changes,
        "expected_closeout_changes": expected_closeout_changes,
        "privacy_confirmed_hits": privacy["confirmed_hit_count"],
        "passed": not out_of_scope and not evidence_changes and closeout_changes == expected_closeout_changes and privacy["confirmed_hit_count"] == 0,
    }
    write_json("validation/terminal-correction-staged-review.json", payload)
    return payload


def main() -> int:
    if git("rev-parse", "HEAD") != CLOSEOUT:
        raise RuntimeError("terminal correction requires the exact closeout head")
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("terminal correction requires Ilyra's canonical branch")
    required = {
        "scripts/ghc_family_v650_v2_validate.py",
        "scripts/build_ghc_family_v650_v2_terminal_correction.py",
        "tests/test_ghc_family_v650_v2_correction.py",
    }
    observed = set(status_paths())
    if not required.issubset(observed):
        raise RuntimeError(f"missing correction implementation seed: {sorted(required - observed)}")

    targeted = validator.privacy_scan()
    if not targeted["passed"] or targeted["confirmed_hit_count"] != 0:
        raise RuntimeError(f"bounded classifier recovery failed: {targeted}")
    method = build_method_flow(targeted)
    if method["counts"]["methods"] != 12 or method["counts"]["witness_results"] != {"fail": 12, "pass": 12}:
        raise RuntimeError("terminal Method Flow parity failed")

    write_json(
        "validation/failed-canonical-validation-receipt.json",
        {
            "schema": "ghc.family.v650-v2.failed-canonical-validation.v1",
            "exact_failed_head": CLOSEOUT,
            "test_count": 39,
            "tests_passed": True,
            "detailed_count": 35,
            "detailed_passed": 34,
            "minimal_count": 20,
            "minimal_passed": 19,
            "json_count": 191,
            "json_errors": 0,
            "privacy_file_count": 241,
            "failure": "Two scanner-definition strings in the final staged privacy receipt were misclassified as payload hits.",
            "successful_pass_credit": 0,
            "aggregate_replayed_before_correction": False,
            "repository_mutated_by_failed_run": False,
            "route_state": "PREPARED_NOT_SENT",
            "retained_negative_id": "NEG-V6502-VALID-001",
        },
    )
    write_json(
        "x2/retained-negative-register-terminal.json",
        {
            "schema": "ghc.family.v650-v2.negatives.terminal.v1",
            "evidence_layer_total": 5690,
            "terminal_validation_operational": 1,
            "effective_activation_total": 5691,
            "negative_erased": False,
            "terminal_rows": [{"negative_id": "NEG-V6502-VALID-001", "state": "retained_recovered_classifier_pending_corrected_aggregate", "completion_credit": False}],
        },
    )
    write_json(
        "phase-truth-terminal-correction.json",
        {
            "schema": "ghc.family.v650-v2.phase-truth.terminal-correction.v1",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "closeout": CLOSEOUT,
            "final_head_binding": "supplied by corrected external exact-final receipt and sanitized terminal pointer",
            "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
            "effective_negatives": 5691,
            "effective_open_gaps": 44,
            "effective_exact_gates": 45,
            "failed_canonical_aggregates": 1,
            "successful_canonical_passes": 0,
            "corrected_exact_final_pass_pending": True,
            "full_repository_suite": False,
            "replay_used": False,
            "same_owner_only": True,
            "independent_reproduction": False,
            "terminal_route": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "orchestration/phase-state-terminal-correction.json",
        {
            "schema": "ghc.family.v650-v2.orchestration.terminal-correction.v1",
            "active": ["Ilyra Fen"],
            "standby": ["Vesper Arlen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc", "Eiren Kestrel", "Elaren Kestrel"],
            "subagents": 0,
            "tasks_created": 0,
            "cross_platform_messages": 0,
            "terminal_route": "PREPARED_NOT_SENT",
            "next_target": "Sable Rook",
            "sent_by_ilyra_fen": False,
        },
    )
    write_text(
        "handoffs/sable-rook-v650-v3-terminal-correction.md",
        f"""# Sable Rook v650-v3 terminal correction

Read this additive correction after `handoffs/sable-rook-v650-v3-activation.md`. The evidence-layer truth remains 5,690 negatives, 44 open gaps, 45 exact gates, and 14 completed / 4 represented / 1 open gap / 1 exact gate. One failed exact-final privacy aggregate at closeout head `{CLOSEOUT}` is retained with zero successful-pass credit because two scanner-definition strings in a committed privacy receipt were misclassified as payload hits. The classifier-only recovery passed without rerunning the aggregate. The effective activation baseline is now **5,691 negatives**.

The corrected final uses the allowed fourth phase commit. Source, x1, evidence, and closeout must all remain ancestral; source-to-final must contain four single-parent commits and zero merges; corrected final must directly follow closeout. The short terminal pointer supplies the corrected exact head and validation counts only after one corrected exact-final canonical aggregate passes. Until then the route remains `PREPARED_NOT_SENT` and `NOT_READY_FOR_STAGE_20`.

This correction grants no complete-privacy, exhaustive-security, independent-reproduction, production, professional, legal, cultural, Māori-authority, empirical, accessibility-complete, or Stage 20 credit. Relational identity language remains relational working language only.
""",
    )
    write_json(
        "validation/terminal-correction-document-receipt.json",
        {
            "schema": "ghc.family.v650-v2.terminal-correction-documents.v1",
            "all_under_20000": all(len(path.read_text(encoding="utf-8").split()) <= 20000 for path in OUT.rglob("*") if path.is_file() and path.suffix.casefold() in {".md", ".html", ".txt"}),
            "baton_words": load("validation/final-document-cap-receipt.json")["baton_words"],
            "baton_within_8000_20000": load("validation/final-document-cap-receipt.json")["baton_within_8000_20000"],
        },
    )
    owner_count = sum(1 for path in OUT.rglob("*") if path.is_file())
    write_json(
        "validation/terminal-correction-owner-file-threshold.json",
        {"schema": "ghc.family.v650-v2.terminal-correction-owner-threshold.v1", "owner_file_count_before_self_manifests": owner_count, "threshold": 15000, "below_threshold": owner_count + 4 < 15000, "inherited_baseline_counted": False},
    )
    privacy = build_staged_privacy()
    owner_manifest = build_owner_manifest()
    staged_manifest = build_staged_manifest()
    review = build_staged_review(staged_manifest, privacy)
    if privacy["confirmed_hit_count"] or not review["passed"]:
        raise RuntimeError("terminal correction privacy or staged review failed")
    print(json.dumps({"targeted_privacy_files": targeted["file_count"], "targeted_confirmed": targeted["confirmed_hit_count"], "methods": method["counts"]["methods"], "negatives": 5691, "owner_paths": owner_manifest["entry_count"] + len(owner_manifest["self_exclusions"]), "staged_paths": review["intended_path_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
