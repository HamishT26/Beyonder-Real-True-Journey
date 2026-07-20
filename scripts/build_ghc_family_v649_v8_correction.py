#!/usr/bin/env python3
"""Record and seal the isolated recovery from Elaren v649-v8 validation failure."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "elaren-kestrel" / "v649-v8"
PRE_CORRECTION_FINAL = "c9ab047dea8debfdfb7c19119b43704ca5f7346c"
METHOD_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"
SELF_EXCLUSIONS = {
    "docs/elaren-kestrel/v649-v8/validation/final-owner-manifest.json",
    "docs/elaren-kestrel/v649-v8/validation/final-staged-manifest.json",
    "docs/elaren-kestrel/v649-v8/validation/final-staged-privacy.json",
    "docs/elaren-kestrel/v649-v8/validation/final-staged-review.json",
    "docs/elaren-kestrel/v649-v8/validation/correction-staged-manifest.json",
    "docs/elaren-kestrel/v649-v8/validation/correction-staged-privacy.json",
    "docs/elaren-kestrel/v649-v8/validation/correction-staged-review.json",
}
ALLOWED_MODIFIED = {
    "docs/elaren-kestrel/v649-v8/closeout-receipt.json",
    "docs/elaren-kestrel/v649-v8/handoffs/eiren-kestrel-3-v650-v1-activation.md",
    "docs/elaren-kestrel/v649-v8/phase-truth-closeout-candidate.json",
    "docs/elaren-kestrel/v649-v8/tooling/ghc-family-index-final.json",
    "docs/elaren-kestrel/v649-v8/validation/final-document-cap-receipt.json",
    "docs/elaren-kestrel/v649-v8/validation/final-owner-manifest.json",
    "scripts/ghc_family_v649_v8_validate.py",
    "tests/test_ghc_family_v649_v8_closeout.py",
}


def run(*args: str, check: bool = True, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=ROOT, check=check, capture_output=True, timeout=timeout,
        text=True, encoding="utf-8", errors="replace",
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def load(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def status_paths() -> list[str]:
    raw = run("git", "status", "--porcelain=v1", "-z", "--untracked-files=all").stdout
    rows = []
    for record in (item for item in raw.split("\0") if item):
        value = record[3:]
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        rows.append(value.strip('"').replace("\\", "/"))
    return sorted(set(rows))


def method_flow() -> dict[str, Any]:
    ledger = PHASE / "method-flow" / "method-flow-ledger-final.json"
    if not ledger.exists():
        write_json("method-flow/method-flow-ledger-final.json", load("method-flow/method-flow-ledger-x2.json"))
    method_id = "V6498-M14"
    negative_id = "V6498-VALID-N01"
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if method_id not in {row["method_id"] for row in current["methods"]}:
        record = {
            "method_id": method_id,
            "title": "Bind minimal identity assertions to the declared schema key",
            "failure_signature": "The first canonical validator guessed identity-receipt boundary instead of identity_boundary and raised KeyError after scoped tests completed.",
            "trigger_preconditions": ["A validator reads a frozen JSON artifact whose semantic field name has not been inspected."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Inspect exact frozen keys, bind the assertion to identity_boundary, and run only the minimal and privacy blocker surfaces before retrying the canonical pass.",
            "validation_witness_ids": [],
            "recurrence_guard": "Inspect frozen JSON keys before writing validator assertions; reject guessed schema fields before the terminal pass.",
            "rollback": "Give the failed canonical attempt zero pass credit, retain it, and keep the route unsent until the corrected exact head passes.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["validation_truth", "identity_boundary", "completion_credit", "terminal_route"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": "Schema-binding recovery only; no stronger identity, scientific, authority, or independent-reproduction claim.",
        }
        record_path = write_json("method-flow/v6498-m14-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        fail = {
            "witness_id": "V6498-M14-WFAIL", "method_id": method_id,
            "procedure": "Run the exact-head validator with a guessed identity-receipt field name.",
            "scope": "failed canonical validation attempt", "expected": "Resolve the declared relational identity boundary field.",
            "observed": "The validator raised KeyError for boundary after the scoped test selection and before producing a canonical receipt.",
            "result": "fail", "same_owner_only": True, "independent_reproduction": False,
            "retained_negative_ids": [negative_id], "boundary": "Failed validation witness only; zero pass credit and no route effect.",
        }
        fail_path = write_json("method-flow/v6498-m14-wfail-witness.json", fail)
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(fail_path))
        passed = {
            "witness_id": "V6498-M14-WPASS", "method_id": method_id,
            "procedure": "Inspect exact identity keys, bind identity_boundary, then run only minimal checks and the five-class privacy blocker scan.",
            "scope": "isolated validator recovery", "expected": "All minimal checks and the blocker privacy scan pass without running the canonical suite.",
            "observed": "The isolated recovery passed 24 minimal checks and a 262-file zero-hit privacy scan.",
            "result": "pass", "same_owner_only": True, "independent_reproduction": False,
            "retained_negative_ids": [negative_id], "boundary": "Isolated schema recovery only; the final canonical pass remains pending.",
        }
        pass_path = write_json("method-flow/v6498-m14-wpass-witness.json", passed)
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(pass_path))
        run(
            sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger),
            "--method-id", method_id, "--state", "preferred", "--note",
            "Preferred only for exact frozen-schema binding after one failed and one isolated passing witness.",
        )
    later_incidents = [
        {
            "method_id": "V6498-M15", "negative_id": "V6498-VALID-N02",
            "title": "Quarantine every exact scanner implementation in correction reviews",
            "failure": "The first correction review quarantined its own scanner but classified the separately modified canonical validator's three regex definitions as payload hits.",
            "recovery": "Enumerate the correction builder and canonical validator as the exact two scanner-definition files while scanning every other correction blob.",
            "pass_observed": "The exact two-file definition quarantine preserved every other scan and returned zero confirmed payload hits.",
            "protected": ["privacy", "exact_staged_surface", "completion_credit", "terminal_route"],
        },
        {
            "method_id": "V6498-M16", "negative_id": "V6498-VALID-N03",
            "title": "Inspect exact source lines before multi-hunk retention patches",
            "failure": "A broad multi-hunk retention patch expected a baton replacement line that was not present and was rejected atomically.",
            "recovery": "Inspect exact source lines and apply smaller independently verifiable hunks without assuming prior generated text.",
            "pass_observed": "The source-guided smaller hunks applied cleanly while the rejected atomic patch remained retained.",
            "protected": ["patch_integrity", "negative_retention", "completion_credit", "terminal_route"],
        },
    ]
    for incident in later_incidents:
        current = json.loads(ledger.read_text(encoding="utf-8"))
        method_id = incident["method_id"]
        negative_id = incident["negative_id"]
        if method_id in {row["method_id"] for row in current["methods"]}:
            continue
        record = {
            "method_id": method_id, "title": incident["title"],
            "failure_signature": incident["failure"],
            "trigger_preconditions": ["The v649-v8 correction workflow exposes this exact failure signature."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": incident["recovery"], "validation_witness_ids": [],
            "recurrence_guard": incident["recovery"],
            "rollback": "Give the failed attempt zero credit, retain it, and keep the correction commit and route blocked until the exact recovery passes.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": incident["protected"], "retained_negative_ids": [negative_id],
            "scope_boundary": "Bounded correction-workflow recovery only; no scientific, authority, privacy-assurance, or independent-reproduction promotion.",
        }
        record_path = write_json(f"method-flow/{method_id.casefold()}-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        for suffix, result, procedure, observed in [
            ("FAIL", "fail", incident["failure"], incident["failure"]),
            ("PASS", "pass", incident["recovery"], incident["pass_observed"]),
        ]:
            witness_id = f"{method_id}-W{suffix}"
            witness = {
                "witness_id": witness_id, "method_id": method_id, "procedure": procedure,
                "scope": f"bounded correction {'failure' if result == 'fail' else 'recovery'}",
                "expected": "Return attributable correction evidence without broadening claims or hiding the failure.",
                "observed": observed, "result": result, "same_owner_only": True,
                "independent_reproduction": False, "retained_negative_ids": [negative_id],
                "boundary": "Retained correction witness only; no independent-reproduction or authority credit.",
            }
            witness_path = write_json(f"method-flow/{witness_id.casefold()}-witness.json", witness)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        run(
            sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger),
            "--method-id", method_id, "--state", "preferred", "--note",
            "Preferred only for the exact correction trigger after one failed and one passing witness.",
        )
    receipt = PHASE / "method-flow" / "method-flow-validation-final.json"
    summary_json = PHASE / "method-flow" / "method-flow-summary-final.json"
    summary_md = PHASE / "method-flow" / "method-flow-summary-final.md"
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(receipt))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(summary_json), "--markdown-output", str(summary_md))
    return json.loads(summary_json.read_text(encoding="utf-8"))


def owner_paths() -> list[str]:
    paths = {path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()}
    paths.update(path.replace("\\", "/") for path in git("ls-files", "scripts/*v649_v8*.py", "tests/test_ghc_family_v649_v8*.py").splitlines())
    paths.add("scripts/build_ghc_family_v649_v8_correction.py")
    return sorted(path for path in paths if (ROOT / path).is_file())


def build_owner_manifest() -> None:
    entries = []
    for relative in owner_paths():
        if relative in SELF_EXCLUSIONS:
            continue
        path = ROOT / relative
        entries.append({
            "path": relative, "repository_path": relative,
            "git_blob": git("hash-object", f"--path={relative}", relative),
            "working_bytes": path.stat().st_size,
        })
    write_json("validation/final-owner-manifest.json", {
        "schema": "ghc.family.v649-v8.final-owner-manifest.v2", "hash_domain": "git_path_filtered_blob",
        "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(SELF_EXCLUSIONS),
        "declared_exclusion_count": len(SELF_EXCLUSIONS), "owner_path_count": len(entries) + len(SELF_EXCLUSIONS),
        "boundary": "All Elaren v649-v8 public owner paths except seven declared lifecycle self-exclusions; exact committed parity is checked after correction commit.",
    })


PRIVACY = {
    "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
    "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
    "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
    "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
    "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
}


def staged_review() -> dict[str, Any]:
    exclusions = {
        "docs/elaren-kestrel/v649-v8/validation/correction-staged-manifest.json",
        "docs/elaren-kestrel/v649-v8/validation/correction-staged-privacy.json",
        "docs/elaren-kestrel/v649-v8/validation/correction-staged-review.json",
    }
    paths = [path for path in status_paths() if path not in exclusions]
    final_tree = set(git("ls-tree", "-r", "--name-only", PRE_CORRECTION_FINAL).splitlines())
    unexpected_modified = sorted(path for path in paths if path in final_tree and path not in ALLOWED_MODIFIED)
    out_of_scope = sorted(
        path for path in paths
        if not path.startswith("docs/elaren-kestrel/v649-v8/")
        and path not in {"scripts/build_ghc_family_v649_v8_correction.py", "scripts/ghc_family_v649_v8_validate.py", "tests/test_ghc_family_v649_v8_closeout.py"}
    )
    definitions = {
        "scripts/build_ghc_family_v649_v8_correction.py",
        "scripts/ghc_family_v649_v8_validate.py",
        "docs/elaren-kestrel/v649-v8/validation/correction-staged-privacy.json",
    }
    entries = []
    candidates = []
    confirmed = []
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        entries.append({
            "path": relative, "bytes": len(data),
            "git_blob": git("hash-object", f"--path={relative}", relative),
            "checkout_sha256": hashlib.sha256(data).hexdigest(),
        })
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in PRIVACY.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": name, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    write_json("validation/correction-staged-privacy.json", {
        "schema": "ghc.family.v649-v8.correction-privacy.v1", "scanned_file_count": len(paths),
        "pattern_class_count": len(PRIVACY), "candidates": candidates,
        "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed,
    })
    write_json("validation/correction-staged-manifest.json", {
        "schema": "ghc.family.v649-v8.correction-manifest.v1", "hash_domain": "git_path_filtered_blob",
        "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(exclusions),
    })
    payload = {
        "schema": "ghc.family.v649-v8.correction-review.v1", "intended_path_count": len(entries) + len(exclusions),
        "manifest_entry_count": len(entries), "self_exclusion_count": len(exclusions),
        "out_of_scope_paths": out_of_scope, "unexpected_modified_paths": unexpected_modified,
        "privacy_confirmed_hits": len(confirmed), "passed": not out_of_scope and not unexpected_modified and not confirmed,
    }
    write_json("validation/correction-staged-review.json", payload)
    return payload


def main() -> int:
    if git("rev-parse", "HEAD") != PRE_CORRECTION_FINAL:
        raise RuntimeError("correction builder requires the exact pre-correction final head")
    methods = method_flow()
    if methods["counts"]["methods"] != 16 or methods["counts"]["witness_results"] != {"fail": 16, "pass": 16}:
        raise RuntimeError(f"unexpected final Method Flow counts: {methods['counts']}")
    write_json("validation/post-final-validation-negatives.json", {
        "schema": "ghc.family.v649-v8.post-final-negatives.v1", "sealed_evidence_negatives": 5444,
        "post_final_operational_count": 3, "effective_activation_baseline": 5447,
        "negative_erased": False,
        "rows": [{
            "negative_id": "V6498-VALID-N01", "state": "retained_recovered",
            "failure": "The first canonical validator guessed boundary instead of identity_boundary and raised KeyError before producing a receipt.",
            "recovery": "Exact-key inspection plus a 24-check minimal and 262-file privacy isolated witness passed before the correction commit.",
            "canonical_pass_credit": False,
        }, {
            "negative_id": "V6498-VALID-N02", "state": "retained_recovered",
            "failure": "The first correction review omitted the modified canonical validator from its exact scanner-definition quarantine and reported three definition-only hits.",
            "recovery": "The exact two-file scanner quarantine preserved all other scanning and returned zero confirmed payload hits.",
            "canonical_pass_credit": False,
        }, {
            "negative_id": "V6498-VALID-N03", "state": "retained_recovered",
            "failure": "A broad multi-hunk retention patch expected a generated baton line that was not present and was rejected atomically.",
            "recovery": "Exact source inspection and smaller independently verifiable hunks applied cleanly.",
            "canonical_pass_credit": False,
        }],
    })
    write_json("validation/isolated-recovery-witness.json", {
        "schema": "ghc.family.v649-v8.isolated-recovery.v1", "method_id": "V6498-M14",
        "minimal_checks": 24, "minimal_failures": 0, "privacy_files": 262, "privacy_hits": 0,
        "canonical_pass": False, "full_repository_suite": False, "independent_reproduction": False,
        "boundary": "Isolated blocker recovery only; the corrected exact head still requires one successful canonical pass.",
    })
    closeout = load("closeout-receipt.json")
    closeout.update({"effective_negatives": 5447, "method_fail_witnesses": 16, "method_pass_witnesses": 16, "post_final_validation_negatives": 3})
    write_json("closeout-receipt.json", closeout)
    truth = load("phase-truth-closeout-candidate.json")
    truth.update({"effective_negatives": 5447, "post_final_validation_negatives": 3, "correction_commit_required": True})
    write_json("phase-truth-closeout-candidate.json", truth)
    index = load("tooling/ghc-family-index-final.json")
    index.update({"methods": 16, "effective_activation_baseline": 5447, "post_final_validation_negatives": 3})
    write_json("tooling/ghc-family-index-final.json", index)
    baton_path = PHASE / "handoffs" / "eiren-kestrel-3-v650-v1-activation.md"
    baton = baton_path.read_text(encoding="utf-8")
    baton = baton.replace("5,444 effective negatives: 5,331 inherited, 9 x1 operational, 4 x2 operational", "5,445 effective negatives: 5,331 inherited, 9 x1 operational, 5 lifecycle or x2 operational")
    baton = baton.replace("5,445 effective negatives: 5,331 inherited, 9 x1 operational, 5 lifecycle or x2 operational", "5,447 effective negatives: 5,331 inherited, 9 x1 operational, 7 lifecycle or x2 operational")
    baton = baton.replace(
        "- The final validator is authorized for one successful canonical pass at the exact final head.",
        "- `V6498-VALID-N01` retains the first canonical attempt's exact-key failure. It produced no receipt and receives zero pass credit; the isolated correction passed 24 minimal checks and a 262-file zero-hit privacy scan.\n- The final validator is authorized for one successful canonical pass at the corrected exact final head.",
    )
    baton = baton.replace("all 5,444 inherited effective negatives", "all 5,445 inherited effective negatives")
    baton = baton.replace("all 5,445 inherited effective negatives", "all 5,447 inherited effective negatives")
    if "`V6498-VALID-N02`" not in baton:
        baton = baton.replace(
            "- The final validator is authorized for one successful canonical pass at the corrected exact final head.",
            "- `V6498-VALID-N02` retains the first correction privacy review's omitted validator definition quarantine; the exact two-file recovery returned zero confirmed payload hits.\n- `V6498-VALID-N03` retains the atomically rejected broad retention patch; exact source inspection and smaller hunks recovered it.\n- The final validator is authorized for one successful canonical pass at the corrected exact final head.",
        )
    write_text("handoffs/eiren-kestrel-3-v650-v1-activation.md", baton)
    write_json("lifecycle/final-correction-record.json", {
        "schema": "ghc.family.v649-v8.final-correction.v1", "pre_correction_final": PRE_CORRECTION_FINAL,
        "retained_negative_ids": ["V6498-VALID-N01", "V6498-VALID-N02", "V6498-VALID-N03"],
        "method_ids": ["V6498-M14", "V6498-M15", "V6498-M16"],
        "isolated_recovery_passed": True, "canonical_pass_pending": True,
        "expected_phase_commit_count_after_correction": 4, "maximum_phase_commits": 4,
        "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    documents = []
    for path in sorted(PHASE.rglob("*")):
        if path.is_file() and path.suffix.casefold() in {".md", ".html", ".txt"}:
            words = len(path.read_text(encoding="utf-8").split())
            documents.append({"path": path.relative_to(PHASE).as_posix(), "words": words, "under_20000": words <= 20000})
    write_json("validation/final-document-cap-receipt.json", {
        "schema": "ghc.family.v649-v8.final-document-cap.v2", "document_count": len(documents),
        "maximum_words": max(row["words"] for row in documents), "all_under_20000": all(row["under_20000"] for row in documents),
        "baton_words": len(baton.split()), "baton_within_8000_20000": 8000 <= len(baton.split()) <= 20000,
        "documents": documents,
    })
    build_owner_manifest()
    review = staged_review()
    if not review["passed"]:
        raise RuntimeError(f"correction staged review failed: {review}")
    print(json.dumps({
        "correction": "prepared", "effective_activation_baseline": 5447,
        "methods": methods["counts"]["methods"], "witnesses": methods["counts"]["witness_results"],
        "baton_words": len(baton.split()), "staged_paths": review["intended_path_count"],
        "route": "PREPARED_NOT_SENT",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
