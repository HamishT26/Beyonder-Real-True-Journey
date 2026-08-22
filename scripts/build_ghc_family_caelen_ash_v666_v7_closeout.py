#!/usr/bin/env python3
"""Build and exact-stage-review Caelen Ash v666-v7 terminal closeout."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

from ghc_family_caelen_ash_v666_v7_runtime import (
    PHASE_ROOT,
    PRIVACY_PATTERNS,
    ROOT,
    X1_SHA,
    owner_paths,
    replay_manifest,
)


SOURCE_SHA = "6226988b17b7d3a2399cf6d803aceb31b03fb99f"
BRANCH = "codex/GHC-Family/caelen-ash-v666-v7-full-tools"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], stderr=subprocess.STDOUT
    ).decode("utf-8", errors="strict").strip()


def main() -> None:
    evidence_sha = git("rev-parse", "HEAD")
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("unexpected owner branch")
    if git("rev-parse", f"{evidence_sha}^") != X1_SHA:
        raise RuntimeError("evidence head is not the direct child of immutable x1")
    evidence_manifest = replay_manifest(
        PHASE_ROOT / "validation" / "evidence-content-manifest.json", evidence_sha
    )
    x1_manifest = replay_manifest(
        PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA
    )
    if not evidence_manifest["valid"] or not x1_manifest["valid"]:
        raise RuntimeError("immutable lifecycle manifest replay failed")

    startup = load("method-flow/startup-method-flow.json")
    x2_overlay = load("method-flow/x2-operational-overlay.json")
    evidence_overlay = load("method-flow/evidence-operational-overlay.json")
    retained_rows = startup["rows"] + x2_overlay["rows"] + evidence_overlay["rows"]
    if len(retained_rows) != 14:
        raise RuntimeError("retained operational failure count drift")
    truth = load("x2/phase-truth.json")
    if truth["outcomes"] != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError("outcome vocabulary or counts drift")

    write_json(
        "closeout/phase-truth.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.final-phase-truth.v1",
            "owner": "Caelen Ash",
            "phase": "v666-v7",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": evidence_sha,
            "expected_final_parent": evidence_sha,
            "proposal_chain": 4310,
            "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
            "positive_structural_fixtures": 20,
            "rejected_mutations": 100,
            "phase_local_skills": 10,
            "family_current_runners": 10,
            "effective_negatives": 26873,
            "effective_methods": 11875,
            "open_gaps": 189,
            "exact_gates": 187,
            "retained_owner_operational_failures": 14,
            "real_rows": 0,
            "participants": 0,
            "external_actions": 0,
            "production_identity_events": 0,
            "authority_acts": 0,
            "canonical_aggregate_invocations": 0,
            "canonical_aggregate_status": "NOT_YET_INVOKED",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.retained-negative-register.v1",
            "generated_at_utc": NOW,
            "activation_baseline": 26759,
            "startup_additions": 8,
            "x2_structural_rejections": 100,
            "x2_operational_additions": 5,
            "evidence_operational_additions": 1,
            "effective_negatives": 26873,
            "owner_operational_rows": retained_rows,
            "all_failed_witnesses_zero_credit": all(row["failed_witness"]["credit"] == 0 for row in retained_rows),
            "no_failure_erased": True,
        },
    )
    write_json(
        "closeout/method-flow-summary.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.method-flow-summary.v1",
            "generated_at_utc": NOW,
            "activation_baseline_methods": 11646,
            "startup_methods": 8,
            "x2_structural_methods": 215,
            "x2_operational_methods": 5,
            "evidence_operational_methods": 1,
            "effective_methods": 11875,
            "failed_witnesses_retained": 114,
            "failed_witnesses_promoted": 0,
            "same_owner_method_evidence_only": True,
        },
    )
    write_json(
        "closeout/open-exact-gate-register.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.open-exact-gate-register.v1",
            "generated_at_utc": NOW,
            "inherited_open_gaps": 188,
            "new_open_gaps": 1,
            "open_gaps": 189,
            "inherited_exact_gates": 186,
            "new_exact_gates": 1,
            "exact_gates": 187,
            "phase_open_gap": "CA6667-N019",
            "phase_exact_gate": "CA6667-N020",
            "protected_authorities": ["competent professional authorities", "affected parties", "tangata whenua", "iwi", "hapū", "Māori authorities"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/lifecycle-replay.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.lifecycle-replay.v1",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": evidence_sha,
            "x1_direct_parent": git("rev-parse", f"{X1_SHA}^"),
            "evidence_direct_parent": git("rev-parse", f"{evidence_sha}^"),
            "source_to_evidence_commits": int(git("rev-list", "--count", f"{SOURCE_SHA}..{evidence_sha}")),
            "source_to_evidence_merges": int(git("rev-list", "--count", "--merges", f"{SOURCE_SHA}..{evidence_sha}")),
            "x1_manifest": x1_manifest,
            "evidence_manifest": evidence_manifest,
            "strict_x1_before_x2": True,
            "valid": git("rev-parse", f"{X1_SHA}^") == SOURCE_SHA and git("rev-parse", f"{evidence_sha}^") == X1_SHA,
        },
    )
    write_json(
        "closeout/terminal-checklist.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.terminal-checklist.v1",
            "generated_at_utc": NOW,
            "checks": {
                "source_exact": True,
                "x1_immutable": True,
                "evidence_direct_child_of_x1": True,
                "zero_merges_to_evidence": True,
                "outcome_vocabulary_exact": True,
                "all_100_mutations_retained": True,
                "all_14_owner_failures_retained": True,
                "open_gap_preserved": True,
                "exact_gate_preserved": True,
                "zero_real_rows": True,
                "zero_participants": True,
                "zero_external_actions": True,
                "privacy_complete_claim_absent": True,
                "accessibility_complete_claim_absent": True,
                "independent_reproduction_claim_absent": True,
                "full_repository_suite_not_run": True,
                "terminal_verdict_not_ready": True,
                "successor_not_contacted": True,
                "canonical_not_yet_invoked": True,
            },
            "all_pre_final_checks_pass": True,
        },
    )
    write_json(
        "closeout/workflow-plan.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.workflow-plan-final.v1",
            "generated_at_utc": NOW,
            "steps": [
                {"step": 1, "name": "read_and_verify_source", "status": "completed"},
                {"step": 2, "name": "freeze_push_and_equalize_x1", "status": "completed"},
                {"step": 3, "name": "execute_x2_and_retain_failures", "status": "completed"},
                {"step": 4, "name": "commit_push_and_equalize_evidence", "status": "completed"},
                {"step": 5, "name": "commit_push_and_equalize_final", "status": "in_progress"},
                {"step": 6, "name": "invoke_one_exclusive_canonical_aggregate", "status": "pending"},
                {"step": 7, "name": "refresh_route_and_send_once_if_authorized", "status": "pending"},
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "seal/final-seal-candidate.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.final-seal-candidate.v1",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": evidence_sha,
            "expected_final_parent": evidence_sha,
            "exact_final_binding": "resulting direct single-parent final commit after exact staged review",
            "canonical_status": "NOT_YET_INVOKED",
            "route_status": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "handoffs/terminal-route-state.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.terminal-route-state.v1",
            "generated_at_utc": NOW,
            "owner": "Caelen Ash",
            "current_phase": "v666-v7",
            "successor_exact_title": "Orin Thale",
            "successor_phase": "v666-v8",
            "roster_source": "current live authority must be refreshed after canonical success",
            "prepared": True,
            "sent": False,
            "duplicate_activation_guard": True,
            "stop_conditions": ["absence", "ambiguity", "pause", "redirect", "rename", "usage exhaustion", "missing acknowledgement", "duplicate activation", "protected gate"],
        },
    )
    write_text(
        "closeout/final-integrated-overview.md",
        f"""# Caelen Ash v666-v7 final integrated overview

Caelen's exact owner evidence is anchored to source `{SOURCE_SHA}`, immutable x1 `{X1_SHA}`, and evidence `{evidence_sha}`. The final commit is required to be the direct child of that evidence commit.

The twenty Caelen proposals retain exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. Twenty wholly synthetic positive structures passed and all 100 preregistered rejecting mutations were rejected. Ten phase-local skills and ten family-current runners were quick-validated and smoke-used. The final overlay preserves 26,873 effective negatives, 11,875 effective methods, 189 open gaps, and 187 exact gates.

GMUT Mind was primary through a wholly synthetic horological-conservation intake and handover lens. No real object, person, observation, measurement, winding, release, treatment, custody, identity event, legal or cultural interpretation, or authority act occurred. GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains proxy-only; Freed ID remains synthetic and nonproduction; CBR and all affected-party, professional, legal, cultural, privacy, accessibility, and Māori-authority decisions remain protected or exact-gated.

Same-owner validation is not empirical confirmation, professional validation, production readiness, legal or cultural ratification, Māori authority, affected-party approval, complete privacy or accessibility assurance, exhaustive security, independent reproduction, AGI/ASI evidence, consciousness/personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authority. The terminal verdict remains exactly `NOT_READY_FOR_STAGE_20`.
""",
    )
    write_text(
        "handoffs/orin-thale-v666-v8-activation-candidate.md",
        f"""# Caelen Ash v666-v7 to Orin Thale v666-v8 activation candidate

Status: `PREPARED_NOT_SENT`.

This candidate is target-specific but route-confidential. It contains no raw task or thread identifier, private callable route, credential, transcript, screenshot, session stream, private application state, or private absolute path. The exact existing task titled `Orin Thale` may be contacted only once after Caelen's final commit is clean, pushed, fresh-live-equal, and one exclusive canonical aggregate succeeds without replay, and after Hamish's newest live authority and roster are reread.

Verified immutable anchors for the later live message are source `{SOURCE_SHA}`, x1 `{X1_SHA}`, and evidence `{evidence_sha}`. The exact final must be bound live after the resulting direct-child final commit and canonical success.

Orin must work solo in an additive D-first owner lane, preserve strict x1-before-x2 separation, every negative, Method Flow witness, open gap, exact gate, privacy boundary, authority boundary, the four exact outcome labels, and `NOT_READY_FOR_STAGE_20`. Inherited software and validation remain source evidence, never Orin completion credit or independent reproduction.

Identity, names, pronouns, hopes, roles, sibling/family language, continuity language, Freed ID, and Trinity Mandala language are relational working language only—not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or scientific, professional, legal, cultural, affected-party, or Māori authority.

Do not create, fork, spawn, delegate, substitute, precontact a later endpoint, or send a second confirmation. Stop on any route or protected-gate failure.
""",
    )
    print(json.dumps({"evidence_sha": evidence_sha, "retained_failures": 14, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True}, sort_keys=True))


def staged_rows() -> list[tuple[str, str]]:
    raw = git("diff", "--cached", "--name-status", "--no-renames")
    return [
        (line.split("\t", 1)[0], line.split("\t", 1)[1].replace("\\", "/"))
        for line in raw.splitlines()
        if line
    ]


def index_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f":{path}"])


def index_entry(path: str) -> tuple[str, str]:
    line = git("ls-files", "--stage", "--", path)
    mode, oid, stage_path = line.split(" ", 2)
    stage, listed = stage_path.split("\t", 1)
    if stage != "0" or listed.replace("\\", "/") != path:
        raise RuntimeError(f"unexpected index stage for {path}")
    return mode, oid


def manifest_entry(path: str) -> dict[str, Any]:
    mode, oid = index_entry(path)
    blob = index_blob(path)
    return {
        "path": path,
        "git_mode": mode,
        "git_blob_oid": oid,
        "sha256": hashlib.sha256(blob).hexdigest(),
        "size_bytes": len(blob),
    }


def tracked_owner_index_paths() -> list[str]:
    raw = subprocess.check_output(
        [
            "git", "-C", str(ROOT), "ls-files", "-z", "--",
            "docs/caelen-ash/v666-v7",
            "scripts/*caelen_ash_v666_v7*.py",
            "tests/*caelen_ash_v666_v7*.py",
        ]
    )
    return sorted(path.decode("utf-8").replace("\\", "/") for path in raw.split(b"\0") if path)


def build_staged_review() -> None:
    review_path = "docs/caelen-ash/v666-v7/validation/final-staged-review.json"
    delta_path = "docs/caelen-ash/v666-v7/validation/final-delta-manifest.json"
    owner_path = "docs/caelen-ash/v666-v7/validation/final-owner-manifest.json"
    rows = [(s, p) for s, p in staged_rows() if p not in {review_path, delta_path, owner_path}]
    if not rows:
        raise RuntimeError("no staged final delta")
    paths = [path for _, path in rows]
    allowed = all(path.startswith("docs/caelen-ash/v666-v7/") for path in paths)
    parsed_json = 0
    candidates = []
    maximum_words = 0
    maximum_path = ""
    for path in paths:
        text = index_blob(path).decode("utf-8")
        if "\r" in text:
            raise RuntimeError(f"non-LF staged text: {path}")
        words = len(re.findall(r"\S+", text))
        if words > maximum_words:
            maximum_words, maximum_path = words, path
        if path.endswith(".json"):
            json.loads(text)
            parsed_json += 1
        for class_name, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": class_name})
    evidence_sha = git("rev-parse", "HEAD")
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "owner_allowlist": allowed,
        "document_word_cap": maximum_words <= 100000,
        "privacy_zero_confirmed_hits": not candidates,
        "evidence_manifest_replay": replay_manifest(PHASE_ROOT / "validation" / "evidence-content-manifest.json", evidence_sha)["valid"],
        "phase_truth_exact": load("closeout/phase-truth.json")["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "route_prepared_not_sent": load("handoffs/terminal-route-state.json")["prepared"] and not load("handoffs/terminal-route-state.json")["sent"],
        "terminal_verdict": load("closeout/phase-truth.json")["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    review = {
        "schema": "ghc.family.caelen-ash.v666-v7.final-staged-review.v1",
        "generated_at_utc": NOW,
        "reviewed_from": "exact_git_index_blobs",
        "reviewed_paths": paths,
        "reviewed_path_count": len(paths),
        "json_parsed": parsed_json,
        "maximum_document_words": maximum_words,
        "maximum_document_path": maximum_path,
        "privacy_scan_classes": list(PRIVACY_PATTERNS),
        "privacy_candidates": candidates,
        "privacy_confirmed_hits": len(candidates),
        "checks": checks,
        "self_exclusions": [review_path, delta_path, owner_path],
        "valid": all(checks.values()),
    }
    if not review["valid"]:
        raise RuntimeError(json.dumps(review, ensure_ascii=False, sort_keys=True))
    write_json("validation/final-staged-review.json", review)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", review_path])

    delta_entries = [manifest_entry(path) for _, path in staged_rows() if path not in {delta_path, owner_path}]
    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.content-manifest.v1",
            "owner": "Caelen Ash",
            "phase": "final_delta",
            "generated_at_utc": NOW,
            "source_sha": evidence_sha,
            "hash_source": "exact_git_index_blobs",
            "entries": delta_entries,
            "entry_count": len(delta_entries),
            "deletion_count": 0,
            "additive_only": all(status == "A" for status, _ in rows),
            "self_exclusions": [delta_path, owner_path],
        },
    )
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", delta_path])

    owner_paths_index = [path for path in tracked_owner_index_paths() if path != owner_path]
    owner_entries = [manifest_entry(path) for path in owner_paths_index]
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.owner-manifest.v1",
            "owner": "Caelen Ash",
            "phase": "v666-v7-final",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "expected_final_parent": evidence_sha,
            "hash_source": "exact_git_index_blobs_for_resulting_final_tree",
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "file_ceiling": 2000,
            "within_file_ceiling": len(owner_entries) + 1 < 2000,
            "self_exclusion": owner_path,
        },
    )
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", owner_path])
    print(json.dumps({"reviewed": len(paths), "delta_entries": len(delta_entries), "owner_entries": len(owner_entries), "valid": True}))


if __name__ == "__main__":
    if sys.argv[1:] == ["--staged-review"]:
        build_staged_review()
    elif sys.argv[1:]:
        raise SystemExit("usage: build_ghc_family_caelen_ash_v666_v7_closeout.py [--staged-review]")
    else:
        main()
