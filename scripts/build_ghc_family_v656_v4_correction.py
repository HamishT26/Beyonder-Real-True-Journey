#!/usr/bin/env python3
"""Additive-history correction for v656-v4 Method Flow document caps."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v656_v4_phase_data as d
from ghc_family_v656_v4_phase_catalogue import RUNNER_IDEAS, SKILL_IDEAS


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SOURCE = d.SOURCE_FINAL
X1 = "1c84cf2616df4efbb13c2df89397941251e2def5"
EVIDENCE = "6f6c32a470b25ee46d16c2f8207018c701c81e02"
CLOSEOUT = "f5a8bcfc1480b4d600806b75a3c921bf3a132bb5"
FINAL_NEGATIVE = {
    "negative_id": "V6564-NEG-FINAL-003",
    "signature": "method-flow-document-word-cap-preflight-failure",
    "observed": (
        "The pre-canonical document-cap audit found the x1, x2, and final "
        "Method Flow ledgers contained 150819, 195070, and 195773 whitespace "
        "tokens because repeated retained prose was embedded inline."
    ),
    "recovery": (
        "Preserve every method, witness, state event, recommendation, and prose "
        "value through deterministic lossless text references, serialize the "
        "three ledgers compactly, and validate each final document at or below "
        "100000 whitespace-delimited words."
    ),
    "recurrence_guard": (
        "Run a physical document word-cap preflight before the first pushed "
        "closeout candidate and normalize repeated ledger prose losslessly."
    ),
    "credit": 0,
    "retained": True,
}
FINAL_EFFECTIVE_NEGATIVES = 14357
FINAL_METHODS = 643


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_compact_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        + "\n",
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


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    result = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return result.stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_map(commit: str) -> dict[str, str]:
    raw = subprocess.run(
        ["git", "ls-tree", "-r", "-z", commit],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout
    result = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        _mode, kind, oid = meta.decode("ascii").split()
        if kind == "blob":
            result[path.decode("utf-8")] = oid
    return result


def batch_blobs(oids: list[str]) -> list[bytes]:
    completed = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input=("".join(f"{oid}\n" for oid in oids)).encode("ascii"),
        check=True,
        capture_output=True,
    )
    stream = io.BytesIO(completed.stdout)
    result = []
    for expected in oids:
        header = stream.readline().decode("ascii").strip().split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header: {header}")
        size = int(header[2])
        result.append(stream.read(size))
        if stream.read(1) != b"\n":
            raise RuntimeError("missing cat-file separator")
    return result


def owner_paths() -> list[str]:
    paths = {
        path.relative_to(REPO).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
    }
    paths.update(
        {
            "scripts/build_ghc_family_v656_v4_x1.py",
            "scripts/ghc_family_v656_v4_phase_catalogue.py",
            "scripts/ghc_family_v656_v4_phase_data.py",
            "scripts/build_ghc_family_v656_v4_evidence.py",
            "scripts/ghc_family_v656_v4_core.py",
            "scripts/ghc_family_v656_v4_validate.py",
            "scripts/ghc_family_v656_v4_x2_data.py",
            "scripts/build_ghc_family_v656_v4_closeout.py",
            "scripts/ghc_family_v656_v4_final_validate.py",
            "scripts/build_ghc_family_v656_v4_correction.py",
            "tests/test_ghc_family_v656_v4_x1.py",
            "tests/test_ghc_family_v656_v4_core.py",
            "tests/test_ghc_family_v656_v4_validation.py",
            "tests/test_ghc_family_v656_v4_closeout.py",
            "tests/test_ghc_family_v656_v4_correction.py",
        }
    )
    paths.update(f"scripts/{name}" for name in RUNNER_IDEAS)
    return sorted(paths)


def correction_paths() -> list[str]:
    paths = owner_paths()
    prior = tree_map(CLOSEOUT)
    prior_paths = [path for path in paths if path in prior]
    prior_data = dict(
        zip(prior_paths, batch_blobs([prior[path] for path in prior_paths]))
    )
    changed = []
    for relative in paths:
        data = (REPO / relative).read_bytes()
        if relative not in prior_data or prior_data[relative] != data:
            changed.append(relative)
    return sorted(changed)


def expand_text_references(ledger: dict[str, Any]) -> dict[str, Any]:
    dictionary = ledger.pop("text_dictionary", {})
    encoding = ledger.pop("text_reference_encoding", None)
    if not dictionary:
        return ledger
    prefix = encoding["prefix"] if encoding else "@MF-TEXT:"

    def expand(value: Any) -> Any:
        if isinstance(value, str) and value.startswith(prefix):
            key = value[len(prefix) :]
            return dictionary[key]
        if isinstance(value, list):
            return [expand(item) for item in value]
        if isinstance(value, dict):
            return {key: expand(item) for key, item in value.items()}
        return value

    return expand(ledger)


def normalize_text_references(ledger: dict[str, Any]) -> dict[str, Any]:
    strings: list[str] = []

    def collect(value: Any) -> None:
        if isinstance(value, str):
            strings.append(value)
        elif isinstance(value, list):
            for item in value:
                collect(item)
        elif isinstance(value, dict):
            for item in value.values():
                collect(item)

    collect(ledger)
    counts = Counter(strings)
    selected = sorted(
        value
        for value, count in counts.items()
        if count >= 2
        and len(re.findall(r"\b[\w'-]+\b", value, flags=re.UNICODE)) >= 4
    )
    codes = {value: f"MF{index:04d}" for index, value in enumerate(selected, 1)}
    prefix = "@MF-TEXT:"

    def replace(value: Any) -> Any:
        if isinstance(value, str) and value in codes:
            return prefix + codes[value]
        if isinstance(value, list):
            return [replace(item) for item in value]
        if isinstance(value, dict):
            return {key: replace(item) for key, item in value.items()}
        return value

    normalized = replace(ledger)
    normalized["text_reference_encoding"] = {
        "schema": "ghc.family.method-flow.text-reference.v1",
        "prefix": prefix,
        "lossless": True,
        "selection": "repeated_at_least_twice_and_at_least_four_words",
        "expansion": "replace each exact token with the matching text_dictionary value",
        "dictionary_entries": len(codes),
    }
    normalized["text_dictionary"] = {
        codes[value]: value for value in selected
    }
    return normalized


def append_cap_failure(flow: dict[str, Any]) -> dict[str, Any]:
    method_id = "V6564-FINAL-METHOD-03"
    if any(item["method_id"] == method_id for item in flow["methods"]):
        return flow
    failed_id = "V6564-FINAL-WITNESS-03-F"
    passing_id = "V6564-FINAL-WITNESS-03-P"
    flow["methods"].append(
        {
            "method_id": method_id,
            "title": "Bounded recovery for Method Flow document word-cap failure",
            "trigger_preconditions": [FINAL_NEGATIVE["signature"]],
            "failure_signature": FINAL_NEGATIVE["observed"],
            "candidate_workaround": FINAL_NEGATIVE["recovery"],
            "recurrence_guard": FINAL_NEGATIVE["recurrence_guard"],
            "approval_class": "safe_now_owner_local_lossless_normalization",
            "privacy_class": "sanitized_public",
            "scope_boundary": (
                "Same-owner lossless document normalization only; no evidence, "
                "failure, authority, or lifecycle state is removed."
            ),
            "rollback": (
                "Stop, retain the oversized-document failure at zero credit, "
                "and leave immutable commits, siblings, and external state unchanged."
            ),
            "protected_gates": d.PROTECTED_GATES,
            "retained_negative_ids": [FINAL_NEGATIVE["negative_id"]],
            "validation_witness_ids": [failed_id, passing_id],
            "recommendation_state": "preferred",
            "supersedes": [],
        }
    )
    flow["witnesses"].extend(
        [
            {
                "witness_id": failed_id,
                "method_id": method_id,
                "result": "fail",
                "scope": FINAL_NEGATIVE["signature"],
                "procedure": "Count physical whitespace-delimited words before canonical validation.",
                "expected": "Every owner document is at or below 100000 words.",
                "observed": FINAL_NEGATIVE["observed"],
                "retained_negative_ids": [FINAL_NEGATIVE["negative_id"]],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": "Zero closeout credit; oversized documents retained in prior commits.",
            },
            {
                "witness_id": passing_id,
                "method_id": method_id,
                "result": "pass",
                "scope": FINAL_NEGATIVE["signature"],
                "procedure": FINAL_NEGATIVE["recovery"],
                "expected": "Every final-tree document is at or below 100000 words.",
                "observed": "Lossless references preserve every string and all three physical ledgers pass the cap.",
                "retained_negative_ids": [FINAL_NEGATIVE["negative_id"]],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": "Same-owner physical representation recovery only.",
            },
        ]
    )
    start = len(flow["state_events"])
    flow["state_events"].extend(
        [
            {
                "event_index": start + 1,
                "method_id": method_id,
                "before": None,
                "after": "candidate",
                "reason": "Document-cap failure retained at zero credit.",
                "witness_id": failed_id,
            },
            {
                "event_index": start + 2,
                "method_id": method_id,
                "before": "candidate",
                "after": "validated",
                "reason": "Lossless normalization and cap audit passed.",
                "witness_id": passing_id,
            },
            {
                "event_index": start + 3,
                "method_id": method_id,
                "before": "validated",
                "after": "preferred",
                "reason": "Pre-closeout cap preflight retained as recurrence guard.",
                "witness_id": passing_id,
            },
        ]
    )
    flow["recommendations"].append(
        {
            "recommendation_id": "V6564-FINAL-REC-03",
            "method_id": method_id,
            "recommendation": FINAL_NEGATIVE["recurrence_guard"],
            "state": "preferred",
            "scope": "family_current_method_flow_serialization_recommendation",
            "completion_credit": False,
        }
    )
    flow["current_phase_final_method_ids"] = list(
        flow.get("current_phase_final_method_ids", [])
    ) + [method_id]
    results = Counter(item["result"] for item in flow["witnesses"])
    states = Counter(
        item.get("after", item.get("to", "unknown"))
        for item in flow["state_events"]
    )
    flow["counts"] = {
        "methods": len(flow["methods"]),
        "witnesses": len(flow["witnesses"]),
        "witness_results": dict(sorted(results.items())),
        "state_events": len(flow["state_events"]),
        "states": dict(sorted(states.items())),
        "recommendations": len(flow["recommendations"]),
    }
    flow["lifecycle"] = "corrected_closeout_content_seal_candidate"
    return flow


def update_baton() -> int:
    path = ROOT / "handoffs/eiren-kestrel-v656-v5-activation.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        f"- Immutable Caelen evidence: `{EVIDENCE}`",
        (
            f"- Immutable Caelen evidence: `{EVIDENCE}`\n"
            f"- Immutable Caelen combined closeout candidate: `{CLOSEOUT}`"
        ),
    )
    old_history = (
        "Source-to-final must contain exactly three new single-parent Caelen commits: "
        "one dedicated x1 freeze, one x2 evidence commit, and one combined "
        "closeout/content-seal commit. It must contain zero merges and final must "
        "have one parent; final must be the direct child of evidence, and source, "
        "x1, and evidence must be ancestral."
    )
    new_history = (
        "Source-to-final must contain exactly four new single-parent Caelen commits: "
        "one dedicated x1 freeze, one x2 evidence commit, one combined closeout "
        "candidate, and one lossless document-cap correction/content-seal commit. "
        "It must contain zero merges and every phase commit must have one parent; "
        "the closeout candidate must be the direct child of evidence, corrected "
        "final must be the direct child of the closeout candidate, and source, x1, "
        "evidence, and closeout candidate must be ancestral."
    )
    if old_history not in text:
        raise RuntimeError("baton history paragraph not found")
    text = text.replace(old_history, new_history)
    text = text.replace("14,356", "14,357")
    text = text.replace("642 methods", "643 methods")
    text = text.replace("642 retained failed", "643 retained failed")
    text = text.replace("642 bounded passing", "643 bounded passing")
    marker = (
        "The bounded recoveries never erase the initial failures. Eiren must "
        "inherit the recurrence guards as recommendations rather than pretend "
        "the failed attempts did not happen."
    )
    replacement = (
        "The physical document-cap preflight also remains retained because three "
        "Method Flow ledgers exceeded 100,000 words through repeated inline prose. "
        "The corrected final preserves every value through deterministic lossless "
        "text references and keeps the oversized original blobs in immutable prior "
        "commits. " + marker
    )
    if marker not in text:
        raise RuntimeError("baton failure marker not found")
    text = text.replace(marker, replacement)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    words = len(text.split())
    if not 10000 <= words <= 100000:
        raise RuntimeError(f"corrected baton word count out of bounds: {words}")
    return words


def privacy_scan() -> None:
    scan_path = f"{d.PHASE_ROOT}/validation/final-privacy-scan.json"
    patterns = {
        "raw_uuid": re.compile(
            r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
        ),
        "private_absolute_path": re.compile(
            r"(?i)(?:[a-z]:\\\\users\\\\[^\\\\\s]+|[a-z]:\\\\ghc-archives)"
        ),
        "credential_or_token": re.compile(
            r"(?i)(?:api[_-]?key|access[_-]?token|authorization:\s*bearer|sk-[a-z0-9]{12,})\s*[:=]"
        ),
        "raw_task_identifier": re.compile(
            r"(?i)(?:source_thread_id|thread_id|task_id|conversation_id)\s*[:=]"
        ),
        "private_callable_detail": re.compile(
            r"(?i)(?:send_message_to_thread|private_target|callable_route_id)\s*[:=(]"
        ),
    }
    hits = {label: [] for label in patterns}
    paths = owner_paths()
    for relative in paths:
        if relative == scan_path:
            continue
        path = REPO / relative
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits[label].append(relative)
    confirmed = sum(len(items) for items in hits.values())
    write_json(
        "validation/final-privacy-scan.json",
        {
            "schema": "ghc.family.v656-v4.privacy-scan.corrected-final.v1",
            "classes": list(patterns),
            "scanned_file_count": len(paths),
            "hits": hits,
            "confirmed_hit_count": confirmed,
            "valid": confirmed == 0,
            "boundary": (
                "Five-class complete owner-file scan; still not exhaustive "
                "security or privacy-complete assurance."
            ),
        },
    )
    if confirmed:
        raise RuntimeError(f"corrected final privacy hits: {hits}")


def correction_manifests() -> None:
    correction_manifest = (
        f"{d.PHASE_ROOT}/validation/correction-staged-manifest.json"
    )
    owner_manifest = f"{d.PHASE_ROOT}/validation/final-owner-manifest.json"
    delta = [
        path
        for path in correction_paths()
        if path not in {correction_manifest, owner_manifest}
    ]
    statuses = {
        path: ("modified" if path in tree_map(CLOSEOUT) else "added")
        for path in delta
    }
    entries = [
        {
            "path": relative,
            "status": statuses[relative],
            "bytes": (REPO / relative).stat().st_size,
            "sha256": sha256(REPO / relative),
        }
        for relative in delta
    ]
    write_json(
        "validation/correction-staged-manifest.json",
        {
            "schema": "ghc.family.v656-v4.correction-staged-manifest.v1",
            "closeout_candidate": CLOSEOUT,
            "entries": entries,
            "entry_count": len(entries),
            "declared_exclusions": [
                {
                    "path": correction_manifest,
                    "reason": "self_hash_impossible_inside_same_blob",
                },
                {
                    "path": owner_manifest,
                    "reason": "generated_after_correction_manifest_for_complete_owner_tree",
                },
            ],
            "expected_commit_path_count": len(entries) + 2,
            "zero_deletions": True,
            "history_additive": True,
            "content_modifications": [
                "lossless Method Flow text-reference normalization",
                "truth and validation correction for retained cap failure",
            ],
            "exact_set_required": True,
        },
    )
    owner_entries = []
    for relative in owner_paths():
        if relative == owner_manifest:
            continue
        path = REPO / relative
        owner_entries.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.v656-v4.final-owner-manifest.corrected.v1",
            "source": SOURCE,
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "declared_exclusions": [
                {"path": owner_manifest, "reason": "self_hash_impossible_inside_same_blob"}
            ],
            "expected_owner_path_count": len(owner_entries) + 1,
            "owner_file_cap": 2000,
            "exact_set_required": True,
        },
    )


def build() -> None:
    if run("git", "rev-parse", "HEAD") != CLOSEOUT:
        raise RuntimeError("correction builder must start at exact closeout candidate")
    if run("git", "rev-parse", "HEAD^") != EVIDENCE:
        raise RuntimeError("closeout candidate is not direct child of evidence")
    if run("git", "rev-list", "--count", "--merges", f"{SOURCE}..{CLOSEOUT}") != "0":
        raise RuntimeError("history contains a merge before correction")

    final_flow = expand_text_references(
        read_json("method-flow/method-flow-ledger-final.json")
    )
    final_flow = append_cap_failure(final_flow)
    x1_flow = normalize_text_references(
        expand_text_references(read_json("method-flow/method-flow-ledger.json"))
    )
    x2_flow = normalize_text_references(
        expand_text_references(read_json("method-flow/method-flow-ledger-x2.json"))
    )
    final_flow = normalize_text_references(final_flow)
    write_compact_json("method-flow/method-flow-ledger.json", x1_flow)
    write_compact_json("method-flow/method-flow-ledger-x2.json", x2_flow)
    write_compact_json("method-flow/method-flow-ledger-final.json", final_flow)
    ledger_words = {
        name: len((ROOT / "method-flow" / name).read_text(encoding="utf-8").split())
        for name in (
            "method-flow-ledger.json",
            "method-flow-ledger-x2.json",
            "method-flow-ledger-final.json",
        )
    }
    if any(value > 100000 for value in ledger_words.values()):
        raise RuntimeError(f"normalized ledger still exceeds cap: {ledger_words}")
    if final_flow["counts"]["methods"] != FINAL_METHODS:
        raise RuntimeError("corrected Method Flow count mismatch")

    write_json(
        "method-flow/method-flow-summary-final.json",
        {
            "schema": "ghc.family.v656-v4.method-flow-summary.corrected-final.v1",
            "counts": final_flow["counts"],
            "methods": FINAL_METHODS,
            "retained_failed_witnesses": FINAL_METHODS,
            "bounded_passing_witnesses": FINAL_METHODS,
            "new_final_operational_failures": 3,
            "lossless_text_reference_normalization": True,
            "physical_ledger_word_counts": ledger_words,
            "no_failure_erased": True,
        },
    )
    write_text(
        "method-flow/method-flow-summary-final.md",
        f"""# Caelen Morrow v656-v4 corrected final Method Flow

The corrected final preserves {FINAL_METHODS} methods, {FINAL_METHODS} retained
failed witnesses, and {FINAL_METHODS} bounded passing witnesses. Three final
failures remain explicit: a literal-path privacy candidate, a batch-reader
timeout, and the Method Flow document-cap failure.

Repeated prose is stored through deterministic lossless text references. Every
method, witness, state event, recommendation, and prose value remains
reconstructable. Physical word counts are {ledger_words}. No failure, gap, or
exact gate is erased.
""",
    )
    negatives = read_json("truth/retained-negative-register-final.json")
    current = list(negatives.get("final_operational_negatives", []))
    if not any(item["negative_id"] == FINAL_NEGATIVE["negative_id"] for item in current):
        current.append(FINAL_NEGATIVE)
    negatives.update(
        {
            "schema": "ghc.family.v656-v4.retained-negatives.corrected-final.v1",
            "final_operational_count": len(current),
            "final_operational_negatives": current,
            "effective_count": FINAL_EFFECTIVE_NEGATIVES,
            "all_retained": True,
        }
    )
    write_json("truth/retained-negative-register-final.json", negatives)
    truth = read_json("truth/phase-truth-final.json")
    truth.update(
        {
            "schema": "ghc.family.v656-v4.phase-truth.corrected-final.v1",
            "closeout_candidate": CLOSEOUT,
            "final": "resolve_from_containing_commit",
            "phase_commit_count": 4,
            "effective_negatives": FINAL_EFFECTIVE_NEGATIVES,
            "method_flow": final_flow["counts"],
            "terminal_route_contacted": False,
            "terminal_route_state": "PREPARED_NOT_SENT",
            "verdict": "NOT_READY_FOR_STAGE_20",
        }
    )
    write_json("truth/phase-truth-final.json", truth)
    checklist = read_json("truth/final-complete-incomplete-checklist.json")
    checklist["complete"].append(
        "lossless Method Flow document-cap correction with prior oversized blobs retained"
    )
    checklist["pending_until_external_terminal_gate"] = [
        item
        for item in checklist["pending_until_external_terminal_gate"]
        if item != "commit and push exact final"
    ]
    checklist["pending_until_external_terminal_gate"].insert(
        0, "commit and push corrected exact final"
    )
    write_json("truth/final-complete-incomplete-checklist.json", checklist)

    baton_words = update_baton()
    successor = read_json("orchestration/successor-baton-preparation.json")
    successor.update(
        {
            "word_count": baton_words,
            "closeout_candidate": CLOSEOUT,
            "corrected_final": "resolve_from_containing_commit",
            "state": "PREPARED_NOT_SENT",
            "send_count": 0,
        }
    )
    write_json("orchestration/successor-baton-preparation.json", successor)
    route = read_json("orchestration/terminal-route-state.json")
    route.update(
        {
            "closeout_candidate": CLOSEOUT,
            "corrected_phase_commit_count": 4,
            "state": "PREPARED_NOT_SENT",
            "contact_count": 0,
        }
    )
    write_json("orchestration/terminal-route-state.json", route)
    record = read_json("lifecycle/final-record.json")
    record.update(
        {
            "schema": "ghc.family.v656-v4.final-record.corrected.v1",
            "closeout_candidate": CLOSEOUT,
            "final": "resolve_from_containing_commit",
            "expected_phase_commits": 4,
            "closeout_direct_child_of_evidence": True,
            "corrected_final_direct_child_of_closeout": True,
            "content_seal_in_same_final_commit": False,
            "content_seal_in_correction_commit": True,
        }
    )
    write_json("lifecycle/final-record.json", record)
    write_json(
        "lifecycle/correction-record.json",
        {
            "schema": "ghc.family.v656-v4.correction-record.v1",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "closeout_candidate": CLOSEOUT,
            "corrected_final": "resolve_from_containing_commit",
            "reason": FINAL_NEGATIVE,
            "history_rewritten": False,
            "force_push": False,
            "deletions": 0,
            "lossless": True,
            "commit_cap": {"used": 4, "ceiling": 8},
        },
    )
    closeout = read_json("closeout/closeout-receipt.json")
    closeout.update(
        {
            "schema": "ghc.family.v656-v4.closeout-receipt.corrected.v1",
            "effective_negatives": FINAL_EFFECTIVE_NEGATIVES,
            "methods": FINAL_METHODS,
            "failed_witnesses": FINAL_METHODS,
            "passing_witnesses": FINAL_METHODS,
            "closeout_candidate": CLOSEOUT,
            "corrected_final": "resolve_from_containing_commit",
            "state": "CORRECTED_CANDIDATE_REQUIRES_EXACT_FINAL_GATE",
        }
    )
    write_json("closeout/closeout-receipt.json", closeout)
    seal = read_json("seal/seal-receipt.json")
    seal.update(
        {
            "schema": "ghc.family.v656-v4.seal-receipt.corrected.v1",
            "content_seal": "lossless_document_cap_correction_commit",
            "closeout_candidate": CLOSEOUT,
            "terminal_message_sent": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
    )
    write_json("seal/seal-receipt.json", seal)
    validation_protocol = read_json("validation/final-validation-protocol.json")
    validation_protocol.update(
        {
            "schema": "ghc.family.v656-v4.final-validation-protocol.corrected.v1",
            "phase_commits": 4,
            "closeout_candidate": CLOSEOUT,
            "selected_test_modules": [
                "tests.test_ghc_family_v656_v4_x1 minus two lifecycle-local working-head assertions",
                "tests.test_ghc_family_v656_v4_core",
                "tests.test_ghc_family_v656_v4_validation",
                "tests.test_ghc_family_v656_v4_closeout",
                "tests.test_ghc_family_v656_v4_correction",
            ],
            "x1_exclusion_replacement": [
                "exact commit-local x1 manifest replay at immutable x1",
                "exact immutable x1 tree absence inspection",
            ],
            "manifest_replays": [
                "x1",
                "evidence",
                "closeout delta",
                "correction delta",
                "corrected owner",
            ],
            "word_count_rule": "physical whitespace-delimited words per final-tree document",
        }
    )
    write_json("validation/final-validation-protocol.json", validation_protocol)
    wellbeing = read_json("wellbeing/wellbeing-check-final.json")
    wellbeing.update(
        {
            "commits_planned": 4,
            "baton_word_count": baton_words,
            "document_caps_pass_after_lossless_normalization": True,
        }
    )
    write_json("wellbeing/wellbeing-check-final.json", wellbeing)
    index = read_json("tooling/ghc-family-index-final-addendum.json")
    index.update(
        {
            "schema": "ghc.family.v656-v4.index-addendum.corrected-final.v1",
            "correction_builder": "scripts/build_ghc_family_v656_v4_correction.py",
            "method_flow_representation": "lossless_text_reference_normalized",
            "superseded_closeout_candidate": CLOSEOUT,
            "route_state": "PREPARED_NOT_SENT",
        }
    )
    write_json("tooling/ghc-family-index-final-addendum.json", index)
    write_text(
        "tooling/ghc-family-index-final-addendum.md",
        """# GHC Family Index — Caelen Morrow v656-v4 corrected final addendum

The closeout candidate remains immutable evidence. A fourth single-parent
correction commit losslessly normalizes repeated Method Flow prose so every
final-tree document remains within the 100,000-word ceiling. The correction
builder and one-shot validator are phase-local. Existing family-current callers
remain unchanged, and the Eiren Kestrel route remains `PREPARED_NOT_SENT`.
""",
    )
    write_text(
        "deliverables/v656-v4-final-closeout.md",
        f"""# Caelen Morrow v656-v4 corrected final closeout

The bounded outcomes remain 23 `completed`, 5 `represented`, 1 `open_gap`, and
1 `exact_gate`. Effective negatives are {FINAL_EFFECTIVE_NEGATIVES:,}; open gaps
are 100; exact gates are 99. Method Flow retains {FINAL_METHODS} methods,
{FINAL_METHODS} failed witnesses, and {FINAL_METHODS} bounded passing witnesses.

The immutable closeout candidate `{CLOSEOUT}` was followed by one single-parent
lossless document-cap correction. No history was rewritten, no commit was
force-pushed, no file was deleted, and every original oversized blob remains in
its immutable prior commit. The corrected final uses deterministic text
references and every physical final-tree document is at or below 100,000 words.

The {baton_words:,}-word sanitized Eiren Kestrel v656-v5 baton remains
`PREPARED_NOT_SENT`. It may be sent exactly once only after the corrected exact
final is clean, pushed, fresh-live equal, and the one canonical scoped aggregate
succeeds. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )
    write_json(
        "validation/correction-build-receipt.json",
        {
            "schema": "ghc.family.v656-v4.correction-build-receipt.v1",
            "valid": True,
            "closeout_candidate": CLOSEOUT,
            "corrected_final": "resolve_from_containing_commit",
            "retained_negative": FINAL_NEGATIVE,
            "lossless_text_references": True,
            "ledger_word_counts": ledger_words,
            "effective_negatives": FINAL_EFFECTIVE_NEGATIVES,
            "methods": FINAL_METHODS,
            "baton_words": baton_words,
            "history_rewritten": False,
            "deletions": 0,
            "terminal_contact": False,
        },
    )
    write_json(
        "validation/correction-staged-review.json",
        {
            "schema": "ghc.family.v656-v4.correction-staged-review.v1",
            "closeout_candidate": CLOSEOUT,
            "paths": correction_paths(),
            "path_count": len(correction_paths()),
            "deletions": [],
            "history_additive": True,
            "content_modifications": [
                "lossless Method Flow representation",
                "truth counts and lifecycle anchors",
                "validator and tests for four-commit corrected lifecycle",
            ],
            "terminal_route_state": "PREPARED_NOT_SENT",
            "valid": True,
        },
    )
    privacy_scan()
    review = read_json("validation/correction-staged-review.json")
    review["paths"] = correction_paths()
    review["path_count"] = len(review["paths"])
    write_json("validation/correction-staged-review.json", review)
    privacy_scan()
    # Verify every physical final-tree document before producing exact manifests.
    over_cap = []
    for relative in owner_paths():
        try:
            text = (REPO / relative).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        words = len(text.split())
        if words > 100000:
            over_cap.append({"path": relative, "words": words})
    if over_cap:
        raise RuntimeError(f"final documents exceed word cap: {over_cap}")
    correction_manifests()
    owner_count = read_json("validation/final-owner-manifest.json")[
        "expected_owner_path_count"
    ]
    if owner_count > 2000:
        raise RuntimeError("owner file cap exceeded")
    print(
        json.dumps(
            {
                "valid": True,
                "phase": d.PHASE,
                "closeout_candidate": CLOSEOUT,
                "ledger_words": ledger_words,
                "effective_negatives": FINAL_EFFECTIVE_NEGATIVES,
                "methods": FINAL_METHODS,
                "baton_words": baton_words,
                "correction_delta_entries": read_json(
                    "validation/correction-staged-manifest.json"
                )["entry_count"],
                "owner_manifest_entries": read_json(
                    "validation/final-owner-manifest.json"
                )["entry_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
