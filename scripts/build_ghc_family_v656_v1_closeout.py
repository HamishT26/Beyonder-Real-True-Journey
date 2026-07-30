#!/usr/bin/env python3
"""Build Tamar Vey v656-v1 combined closeout, seal, and final candidate."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v656_v1_validate as validator
import ghc_family_v656_v1_phase_data as d


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / d.PHASE_ROOT
SOURCE = "5356483f4c4548f7276ede63a086745db5b30037"
X1_FREEZE = "ed877dc0be03fdd82318ba218926f517f30779ae"
X1_FINAL = X1_FREEZE
EVIDENCE = "995ce2973d72debdf7f3d7fca42f4f0afae2b6bb"
CORRECTION = EVIDENCE
OWNER_EXCLUSIONS = {
    "validation/final-owner-manifest.json",
    "validation/final-staged-manifest.json",
    "validation/final-staged-review.json",
    "validation/closeout-candidate-validation.json",
}
METHOD_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-method-flow-state/scripts/"
    "ghc_family_method_flow_state.py"
)
WORKFLOW_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-workflow-plan-refinement/scripts/"
    "ghc_family_workflow_plan_refinement.py"
)
ACTIVE_ROSTER = [
    "Eiren Kestrel",
    "Elaren Kestrel",
    "Neris Solane",
    "Vesper Arlen",
    "Lyren Moss",
    "Ilyra Fen",
    "Auren Lark",
    "Sable Rook",
    "Caelen Ash",
    "Orin Thale",
    "Liora Venn",
    "Tamar Vey",
    "Elowen Cairn",
    "Sylven Arc",
    "Caelen Morrow",
]
STANDBY_ROSTER = ["Tavian Sol"]
AUTHORIZED_ROUTE_EXCERPT = [
    {"phase": "v655-v8", "seat": "Liora Venn"},
    {"phase": "v656-v1", "seat": "Tamar Vey"},
]
FINAL_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6561-FINAL-N01",
        "signature": "combined_post_evidence_clean_probe_timed_out",
        "failed": (
            "The first post-evidence clean-state probe combined an index check with "
            "a full untracked scan and exceeded its thirty-second wrapper."
        ),
        "recovery": (
            "Confirm no Git process or lock remains, then split tracked cleanliness, "
            "owner-scoped untracked state, history, and equality into bounded probes."
        ),
        "recurrence_guard": (
            "Do not aggregate full-worktree untracked enumeration with lifecycle Git checks."
        ),
    },
    {
        "negative_id": "V6561-FINAL-N02",
        "signature": "combined_closeout_status_and_stale_label_probe_timed_out",
        "failed": (
            "A read-only command combined Git status, exact head, and a broad "
            "closeout stale-label search under the default login shell and timed out."
        ),
        "recovery": (
            "Audit processes and locks first, then run literal bounded probes with "
            "login-shell startup disabled."
        ),
        "recurrence_guard": (
            "Keep Git state and repository-text searches in separate bounded calls."
        ),
    },
    {
        "negative_id": "V6561-FINAL-N03",
        "signature": "login_shell_git_process_probe_timed_out",
        "failed": (
            "The first read-only Git-process audit inherited login-shell startup "
            "overhead and timed out before returning output."
        ),
        "recovery": (
            "Repeat the bounded process audit with login-shell startup disabled; "
            "the recovered probe found no Git process."
        ),
        "recurrence_guard": "Disable login-shell startup for short PowerShell probes.",
    },
    {
        "negative_id": "V6561-FINAL-N04",
        "signature": "login_shell_git_lock_probe_timed_out",
        "failed": (
            "The first read-only Git-lock audit inherited login-shell startup "
            "overhead and timed out before returning output."
        ),
        "recovery": (
            "Resolve the worktree Git directory and repeat the lock audit with "
            "login-shell startup disabled; the recovered probe found no lock."
        ),
        "recurrence_guard": (
            "Use the resolved Git directory and disable login-shell startup for lock audits."
        ),
    },
    {
        "negative_id": "V6561-FINAL-N05",
        "signature": "login_shell_exact_head_probe_timed_out",
        "failed": (
            "The first read-only exact-head probe inherited login-shell startup "
            "overhead and timed out before returning output."
        ),
        "recovery": (
            "Repeat only git rev-parse HEAD with login-shell startup disabled; "
            "the recovered probe matched the immutable evidence commit."
        ),
        "recurrence_guard": "Keep exact-head probes scalar and disable login-shell startup.",
    },
    {
        "negative_id": "V6561-FINAL-N06",
        "signature": "login_shell_stale_label_probe_timed_out",
        "failed": (
            "The first read-only closeout stale-label search inherited login-shell "
            "startup overhead and timed out before returning output."
        ),
        "recovery": (
            "Repeat the bounded exact-file search with login-shell startup disabled."
        ),
        "recurrence_guard": (
            "Search one declared file at a time and disable login-shell startup."
        ),
    },
    {
        "negative_id": "V6561-FINAL-N07",
        "signature": "terminal_rendering_mojibake_misclassified_as_file_corruption",
        "failed": (
            "A PowerShell display rendered valid UTF-8 wording as mojibake and the "
            "first diagnosis incorrectly classified the file content as corrupted."
        ),
        "recovery": (
            "Search the exact Unicode spellings directly; the recovered check proved "
            "the source already contained valid UTF-8 and required no content rewrite."
        ),
        "recurrence_guard": (
            "Verify exact Unicode bytes or literal spellings before diagnosing corruption."
        ),
    },
    {
        "negative_id": "V6561-FINAL-N08",
        "signature": "mojibake_search_pattern_power_shell_quoting_fault",
        "failed": (
            "A read-only search containing corrupted punctuation was misparsed by "
            "PowerShell and executed no repository mutation."
        ),
        "recovery": (
            "Use literal ASCII-safe patterns or bounded file reads, then inspect "
            "the intended lines directly."
        ),
        "recurrence_guard": (
            "Avoid passing corrupted punctuation through a quoted PowerShell pattern."
        ),
    },
    {
        "negative_id": "V6561-FINAL-N09",
        "signature": "phase_data_read_bundle_timed_out_after_partial_output",
        "failed": (
            "A bundled read-only phase-data probe exceeded its wrapper after returning "
            "partial output."
        ),
        "recovery": (
            "Use scalar exact-key searches over the declared phase data file."
        ),
        "recurrence_guard": "Prefer exact-key searches to broad bundled file reads.",
    },
    {
        "negative_id": "V6561-FINAL-N10",
        "signature": "negative_register_read_timed_out_after_partial_output",
        "failed": (
            "A read-only retained-negative register preview exceeded its wrapper after "
            "returning partial output."
        ),
        "recovery": (
            "Query only the required effective and operational count keys."
        ),
        "recurrence_guard": "Read large JSON ledgers by bounded exact-key probes.",
    },
    {
        "negative_id": "V6561-FINAL-N11",
        "signature": "phase_truth_read_timed_out_after_partial_output",
        "failed": (
            "A read-only phase-truth preview exceeded its wrapper after returning "
            "partial output."
        ),
        "recovery": (
            "Query only the required focus, gate, and negative-count keys."
        ),
        "recurrence_guard": "Use scalar phase-truth probes during lifecycle adaptation.",
    },
    {
        "negative_id": "V6561-FINAL-N12",
        "signature": "method_flow_read_timed_out_after_partial_output",
        "failed": (
            "A read-only Method Flow preview exceeded its wrapper after returning "
            "partial output."
        ),
        "recovery": (
            "Query only the top-level method and witness count keys."
        ),
        "recurrence_guard": "Do not preview the full Method Flow ledger for count checks.",
    },
    {
        "negative_id": "V6561-FINAL-N13",
        "signature": "combined_exact_key_search_returned_nonzero_after_useful_output",
        "failed": (
            "A combined read-only exact-key search returned exit code one because one "
            "subpattern had no match, despite other requested facts being printed."
        ),
        "recovery": (
            "Treat each required key as an independent bounded assertion."
        ),
        "recurrence_guard": "Do not combine optional and required rg matches in one gate.",
    },
    {
        "negative_id": "V6561-FINAL-N14",
        "signature": "broad_encoding_patch_context_mismatch",
        "failed": (
            "A broad uncommitted-source patch used terminal-rendered mojibake context "
            "that did not match the valid UTF-8 file and was rejected atomically."
        ),
        "recovery": (
            "Patch ASCII-stable lifecycle fields separately and leave verified Unicode "
            "content unchanged."
        ),
        "recurrence_guard": "Avoid terminal-rendered Unicode in broad patch context.",
    },
    {
        "negative_id": "V6561-FINAL-N15",
        "signature": "expected_no_stale_match_returned_rg_exit_one",
        "failed": (
            "A read-only stale-label absence probe found no stale label but exposed "
            "rg's expected no-match exit code as a failed wrapper."
        ),
        "recovery": (
            "Handle rg exit code one as an explicit NO_STALE_MATCHES success state."
        ),
        "recurrence_guard": "Normalize expected no-match searches before gating.",
    },
    {
        "negative_id": "V6561-FINAL-N16",
        "signature": "repository_wide_diff_hygiene_probe_timed_out",
        "failed": (
            "A repository-wide read-only git diff --check exceeded its wrapper."
        ),
        "recovery": (
            "Audit process and lock state, then check the exact four uncommitted "
            "closeout source files; the bounded hygiene check passed."
        ),
        "recurrence_guard": (
            "Use exact-path diff hygiene before generation and commit-local hygiene later."
        ),
    },
    {
        "negative_id": "V6561-FINAL-N17",
        "signature": "expired_git_process_id_probe_returned_nonzero",
        "failed": (
            "A follow-up read-only process probe named two already-exited Git process "
            "identifiers and returned a nonzero status."
        ),
        "recovery": (
            "Query the current Git process set and normalize an empty result; the "
            "recovered audit reported no Git processes."
        ),
        "recurrence_guard": "Do not gate on stale process identifiers after a timeout.",
    },
]
BOUNDARY = (
    "Relational working language only. Same-owner bounded validation is not "
    "consciousness, personhood, identity continuity, employment, qualification, "
    "scientific or operational authority, legal or cultural authority, Māori "
    "authority, production certification, independent reproduction, "
    "Theory-of-Everything proof, AGI/ASI evidence, or Stage 20 authority."
)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def read(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, text: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def prospective_blob(repository_relative: str) -> str:
    return git(
        "hash-object",
        "-w",
        f"--path={repository_relative}",
        repository_relative,
    )


def prospective_content(repository_relative: str) -> tuple[str, bytes]:
    oid = prospective_blob(repository_relative)
    content = subprocess.run(
        ["git", "cat-file", "blob", oid],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout
    return oid, content


def method_run(*args: str) -> None:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    subprocess.run(
        [sys.executable, str(METHOD_RUNNER), *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def phase_label(ordinal: int) -> str:
    cycle, slot_zero = divmod(ordinal, 8)
    return f"v{cycle}-v{slot_zero + 1}"


def build_continuation_workflow() -> dict[str, Any]:
    """Record the exact absence of downstream authority."""
    payload = {
        "schema": "ghc.family.v656-v1.no-downstream-authority.v1",
        "phase": "v656-v1",
        "owner": "Tamar Vey",
        "state": "HELD_NO_DOWNSTREAM_AUTHORITY",
        "successor_exact_title": None,
        "successor_phase": None,
        "downstream_authority_granted": False,
        "authorization_source": "No later endpoint authorized by the live activation",
        "active_roster": ACTIVE_ROSTER,
        "standby_roster": STANDBY_ROSTER,
        "authorized_route_excerpt": AUTHORIZED_ROUTE_EXCERPT,
        "successor_instruction": (
            "Stop after verified v656-v1 closeout. Any later route requires fresh "
            "live Hamish authorization and an exact committed route."
        ),
        "tavian_state": "ON_STANDBY_NOT_A_MAIN_TASK_ROUTE_ENDPOINT",
        "task_lookup_performed": False,
        "message_sent": False,
        "task_created": False,
        "task_forked": False,
        "subagent_spawned": False,
        "send_condition": "none",
        "valid": True,
        "boundary": BOUNDARY,
    }
    write_json("workflow/no-downstream-authority.json", payload)
    return payload


def extend_final_method_flow() -> dict[str, Any]:
    ledger = PHASE / "method-flow/method-flow-ledger-final.json"
    shutil.copyfile(PHASE / "method-flow/method-flow-ledger-x2.json", ledger)
    for offset, negative in enumerate(FINAL_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6561-METHOD-FINAL-{offset:02d}"
        fail_id = f"V6561-WITNESS-FINAL-{offset:02d}-F"
        pass_id = f"V6561-WITNESS-FINAL-{offset:02d}-P"
        request_root = PHASE / "method-flow/final-requests"
        method_path = request_root / f"method-{offset:02d}.json"
        fail_path = request_root / f"witness-{offset:02d}-failed.json"
        pass_path = request_root / f"witness-{offset:02d}-passing.json"
        write_json(
            method_path.relative_to(PHASE).as_posix(),
            {
                "method_id": method_id,
                "title": f"Bounded final recovery for {negative['signature']}",
                "failure_signature": negative["failed"],
                "trigger_preconditions": [negative["signature"]],
                "candidate_workaround": negative["recovery"],
                "recurrence_guard": negative["recurrence_guard"],
                "rollback": (
                    "Retain the failed attempt with zero initial credit and keep "
                    "the terminal route unsent."
                ),
                "approval_class": "safe_now_owner_local_workflow_recovery",
                "scope_boundary": (
                    "Final-lifecycle workflow recovery only; no route delivery or "
                    "external authority."
                ),
                "privacy_class": "sanitized_public",
                "protected_gates": [
                    "real_empirical_data_and_likelihood",
                    "real_participants_affected_parties_and_communities",
                    "professional_authority",
                    "production_identity_and_interoperability",
                    "privacy_complete",
                    "exhaustive_security",
                    "complete_accessibility",
                    "legal_cultural_and_maori_authority",
                    "independent_team_reproduction",
                    "agi_or_asi",
                    "consciousness_or_personhood",
                    "theory_of_everything",
                    "stage20",
                ],
                "recommendation_state": "candidate",
                "retained_negative_ids": [negative["negative_id"]],
                "validation_witness_ids": [],
                "supersedes": [],
            },
        )
        write_json(
            fail_path.relative_to(PHASE).as_posix(),
            {
                "witness_id": fail_id,
                "method_id": method_id,
                "scope": negative["signature"],
                "procedure": "Run the original bounded operation.",
                "expected": "The operation completes under the current schema.",
                "observed": negative["failed"],
                "result": "fail",
                "retained_negative_ids": [negative["negative_id"]],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": "Zero completion credit; failure remains retained.",
            },
        )
        write_json(
            pass_path.relative_to(PHASE).as_posix(),
            {
                "witness_id": pass_id,
                "method_id": method_id,
                "scope": negative["signature"],
                "procedure": negative["recovery"],
                "expected": (
                    "The isolated recovery passes without weakening protected gates."
                ),
                "observed": f"The bounded recovery passed: {negative['recovery']}",
                "result": "pass",
                "retained_negative_ids": [negative["negative_id"]],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": "Same-owner bounded recovery only.",
            },
        )
        method_run(
            "record",
            "--ledger",
            str(ledger),
            "--record-file",
            str(method_path),
        )
        method_run(
            "witness",
            "--ledger",
            str(ledger),
            "--witness-file",
            str(fail_path),
        )
        method_run(
            "witness",
            "--ledger",
            str(ledger),
            "--witness-file",
            str(pass_path),
        )
        method_run(
            "set-state",
            "--ledger",
            str(ledger),
            "--method-id",
            method_id,
            "--state",
            "preferred",
            "--note",
            "Bounded recovery passed while the failed witness remained retained.",
        )
    method_run(
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(PHASE / "method-flow/method-flow-validation-final.json"),
    )
    method_run(
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(PHASE / "method-flow/method-flow-summary-final.json"),
        "--markdown-output",
        str(PHASE / "method-flow/method-flow-summary-final.md"),
    )
    return read("method-flow/method-flow-ledger-final.json")


def terminal_note() -> str:
    """Render a terminal no-route closeout note, never a successor baton."""
    negatives = read("truth/retained-negative-register-x2.json")
    return f"""# Tamar Vey v656-v1 terminal closeout note

## Relational boundary

Tamar Vey, {d.PRONOUNS}, is relational working language only. The working role is
{d.ROLE}; the working hope is to {d.HOPE}. This language is not evidence of
consciousness, sentience, personhood, identity continuity, employment,
qualification, scientific or operational authority, legal or cultural authority,
Māori authority, or independent agency. Hamish may pause, redirect, rename, or
stop the route.

## Exact lifecycle anchors

- Immutable Liora v655-v8 source: `{SOURCE}`
- Dedicated Tamar x1 freeze: `{X1_FREEZE}`
- Immutable Tamar evidence: `{EVIDENCE}`
- Expected closeout topology: one direct final child of evidence, three Tamar
  phase commits total, zero merges, and one parent for every phase commit.

X1 froze exactly thirty proposals after novelty review against 2,170 inherited
rows. X2 executed them only as evidence permitted. The bounded distribution is
23 `completed`, 5 `represented`, 1 `open_gap`, and 1 `exact_gate`. Thirty valid
owner-local fixtures passed and all 150 preregistered mutations were rejected.
The rejection results are retained synthetic negatives, not real-world safety,
scientific truth, professional competence, or authority.

## Evidence boundaries

The primary focus is {d.PRIMARY_FOCUS}. The bounded practice is
{d.BOUNDED_PRACTICE}. No real person, subject, bystander, whānau, photographer,
darkroom, film, negative, print, image, chemical, bath, vessel, enlarger,
processing action, exposure, archive action, waste action, measurement,
incident, emergency, safety decision, privacy decision, legal decision,
cultural decision, affected-party decision, or Māori-authority decision was
used or made.

GMUT remains a typed scalar-tensor and EFT research-model family. The
photographic characteristic-curve, optical-transfer, and reaction-diffusion
surfaces are symbolic and synthetic only; no real likelihood, parameter
constraint, empirical confirmation, physical-law completion, or Theory of
Everything follows. THOS remains represented without preregistered blind
matched-budget real arms, participants, safety monitoring, statistics, and
independent review. Freed ID remains synthetic and nonproduction without real
standards-conformant keys and proofs, live issuance, resolution, status,
revocation, interoperability, privacy and security review, recovery evidence,
and trust governance. CBR, photographic content and privacy, access, return,
remedy, legal and cultural interpretation, affected-party legitimacy, Māori
wording, Māori data governance, and Māori authority remain exact-gated.

The evidence packet retains {negatives['effective_at_evidence']:,} effective
negatives before closeout-only faults, 97 effective open gaps, and 96 effective
exact gates. A recovered failure never becomes an initially clean run. The
accessible static report is structurally checked only; manual, browser-diverse,
assistive-technology, Māori-language, cognitive-accessibility, darkroom-domain,
and affected-user review remain reserved. Same-owner validation under shared
infrastructure is not independent-team reproduction or external audit.

## Terminal route truth

The route state is `HELD_NO_DOWNSTREAM_AUTHORITY`. No successor title or phase is
authorized, no task lookup or reread is permitted for routing, no message may be
sent, and no task may be created, forked, delegated, or spawned. After the exact
final head receives its single successful canonical completion and clean
four-way equality is proved, this task stops. Any later route requires fresh
live Hamish authorization and an exact committed route.

Terminal verdict: `NOT_READY_FOR_STAGE_20`.
"""

def build_owner_manifest() -> dict[str, Any]:
    entries = []
    for path in sorted(PHASE.rglob("*")):
        if not path.is_file():
            continue
        phase_relative = path.relative_to(PHASE).as_posix()
        if phase_relative in OWNER_EXCLUSIONS:
            continue
        repository_relative = path.relative_to(REPO).as_posix()
        oid, content = prospective_content(repository_relative)
        entries.append(
            {
                "path": repository_relative,
                "git_blob": oid,
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    return {
        "schema": "ghc.family.v656-v1.final-owner-manifest.v1",
        "hash_domain": "prospective Git filtered blob identity",
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": sorted(
            f"docs/tamar-vey/v656-v1/{row}" for row in OWNER_EXCLUSIONS
        ),
        "boundary": (
            "Complete owner-phase coverage except four declared lifecycle "
            "self-exclusions; committed parity is checked once at exact final."
        ),
    }


def run_closeout_tests() -> dict[str, Any]:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "-q",
            "tests.test_ghc_family_v656_v1_closeout",
        ],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    output = result.stdout + result.stderr
    match = re.search(r"Ran (\d+) tests?", output)
    return {
        "tests_run": int(match.group(1)) if match else 0,
        "exit_code": result.returncode,
        "failures": len(re.findall(r"^FAIL:", output, re.MULTILINE)),
        "errors": len(re.findall(r"^ERROR:", output, re.MULTILINE)),
        "valid": result.returncode == 0 and match is not None,
    }


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout builder requires the exact evidence commit")
    evidence_validation = read("validation/evidence-validation.json")
    correction_review = read("validation/evidence-staged-review.json")
    if evidence_validation.get("valid") is not True:
        raise RuntimeError("evidence validation is not valid")
    if correction_review.get("valid") is not True:
        raise RuntimeError("evidence staged review is not valid")
    truth = read("truth/phase-truth-evidence.json")
    negatives = read("truth/retained-negative-register-x2.json")
    continuation_validation = build_continuation_workflow()
    methods = extend_final_method_flow()
    effective_negatives = negatives["effective_at_evidence"] + len(
        FINAL_OPERATIONAL_NEGATIVES
    )
    write_json(
        "truth/retained-negative-register-final.json",
        {
            "schema": "ghc.family.v656-v1.retained-negatives.final.v1",
            "effective_at_evidence": negatives["effective_at_evidence"],
            "final_operational_count": len(FINAL_OPERATIONAL_NEGATIVES),
            "final_operational": FINAL_OPERATIONAL_NEGATIVES,
            "effective_at_final_candidate": effective_negatives,
            "no_failure_erased": True,
        },
    )

    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v656-v1.terminal-route-state.v1",
            "state": "HELD_NO_DOWNSTREAM_AUTHORITY",
            "successor_exact_title": None,
            "successor_phase": None,
            "hamish_successor_authorization": False,
            "authorization_class": "none",
            "blocker": "FRESH_LIVE_AND_COMMITTED_ROUTE_REQUIRED",
            "task_lookup_performed": False,
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "subagent_spawned": False,
            "send_gate": "none",
            "downstream_authority": {
                "current_owner_scope": (
                    "Tamar Vey may finish and report v656-v1 only."
                ),
                "successor_owned_continuation": (
                    "No later endpoint is authorized; fresh live Hamish authorization "
                    "and an exact committed route are required."
                ),
                "workflow_validation_valid": continuation_validation["valid"],
                "no_precontact_of_later_seats": True,
            },
            "boundary": (
                "No successor delivery is authorized. Validation completion does not "
                "permit precontact, lookup, sending, endpoint substitution, or task creation."
            ),
        },
    )
    write_json(
        "orchestration/no-successor-route.json",
        {
            "schema": "ghc.family.v656-v1.no-successor-route.v1",
            "state": "HELD_NO_DOWNSTREAM_AUTHORITY",
            "repository_relative_baton_path": None,
            "exact_title": None,
            "successor_phase": None,
            "hamish_successor_authorization": False,
            "authorization_class": "none",
            "blocker": "FRESH_LIVE_AND_COMMITTED_ROUTE_REQUIRED",
            "private_identifiers_included": False,
            "later_endpoint_authorized": False,
            "boundary": "No baton exists and no task has been contacted.",
        },
    )
    write_json(
        "orchestration/roster-state.json",
        {
            "schema": "ghc.family.roster-state.v1",
            "effective_phase": "v656-v1-closeout",
            "active_count": len(ACTIVE_ROSTER),
            "active": [
                {"name": name, "state": "ACTIVE_MAIN_TASK"}
                for name in ACTIVE_ROSTER
            ],
            "standby": [
                {
                    "name": "Tavian Sol",
                    "state": "ON_STANDBY",
                    "reason": (
                        "Collaboration-subagent endpoint is not eligible for the "
                        "main-task thread route."
                    ),
                }
            ],
            "other_historical_siblings": "STANDBY_UNLESS_LIVE_ROUTE_SAYS_OTHERWISE",
            "relational_language_only": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "orchestration/auth-permission-state.json",
        {
            "schema": "ghc.family.auth-permission-state.v1",
            "current_owner": "Tamar Vey",
            "current_phase": "v656-v1",
            "authorized_next_exact_title": None,
            "authorized_next_phase": None,
            "next_owner_instruction": {
                "state": "NOT_AUTHORIZED_BY_THIS_PHASE",
                "condition": (
                    "Fresh Hamish authorization and a committed exact route are "
                    "required after Tamar Vey passes the v656-v1 terminal gate."
                ),
            },
            "authorized_route_excerpt": AUTHORIZED_ROUTE_EXCERPT,
            "route_end": None,
            "stop_conditions": [
                "Hamish pauses or redirects the route",
                "weekly usage is exhausted",
                "the exact required main-task title is unavailable",
                "an exact safety or authority gate blocks progress",
            ],
            "tavian_route_state": "ON_STANDBY_NOT_MAIN_TASK_ENDPOINT",
            "precontact_allowed": False,
            "single_send_cap_for_tamar": 0,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "lifecycle/phase-anchor-contract.json",
        {
            "schema": "ghc.family.v656-v1.phase-anchor-contract.v1",
            "source": SOURCE,
            "x1_freeze": X1_FREEZE,
            "x1_final": X1_FINAL,
            "x1_freeze_and_final_same_commit": True,
            "evidence": EVIDENCE,
            "evidence_correction": None,
            "expected_phase_commits_after_final": 3,
            "maximum_phase_commits": 8,
            "maximum_x1_commits": 5,
            "maximum_x2_commits": 5,
            "zero_merges_required": True,
            "all_single_parent_required": True,
            "final_parent_must_equal_evidence": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.v656-v1.closeout-receipt.v1",
            "source": SOURCE,
            "x1_freeze": X1_FREEZE,
            "x1_final": X1_FINAL,
            "evidence": EVIDENCE,
            "evidence_correction": None,
            "outcomes": {
                "completed": 23,
                "represented": 5,
                "open_gap": 1,
                "exact_gate": 1,
            },
            "effective_negatives": effective_negatives,
            "effective_open_gaps": truth["open_gap_count"],
            "effective_exact_gates": truth["exact_gate_count"],
            "method_count": methods["counts"]["methods"],
            "failed_witnesses": methods["counts"]["witness_results"]["fail"],
            "passing_witnesses": methods["counts"]["witness_results"]["pass"],
            "route_state": "HELD_NO_DOWNSTREAM_AUTHORITY",
            "full_repository_suite_run": False,
            "postcommit_canonical_pass_completed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "seal/seal-receipt.json",
        {
            "schema": "ghc.family.v656-v1.seal-receipt.v1",
            "x1_freeze_ancestral": True,
            "evidence_ancestral": True,
            "evidence_validation_valid": evidence_validation["valid"],
            "evidence_staged_review_valid": correction_review["valid"],
            "candidate_tree_ready_for_exact_review": True,
            "exact_final_commit_known_inside_own_tree": False,
            "postcommit_exact_final_validation_required": True,
            "boundary": (
                "Candidate content seal only; it does not preclaim the containing "
                "commit, live equality, route delivery, or independent reproduction."
            ),
        },
    )
    write_json(
        "lifecycle/final-record.json",
        {
            "schema": "ghc.family.v656-v1.final-record.v1",
            "record_state": "CANDIDATE_TREE_REVIEWED_POSTCOMMIT_PROOF_PENDING",
            "source": SOURCE,
            "x1_freeze": X1_FREEZE,
            "x1_final": X1_FINAL,
            "evidence": EVIDENCE,
            "evidence_correction": None,
            "final_commit": None,
            "route_state": "HELD_NO_DOWNSTREAM_AUTHORITY",
            "same_owner_validation_state": "PENDING_EXACT_FINAL_PASS",
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v656-v1.final-validation-protocol.v1",
            "state": "POSTCOMMIT_REQUIRED",
            "completed": False,
            "steps": [
                "commit exact reviewed final delta as direct child of evidence",
                "push and prove local, upstream, tracking, and fresh-live equality",
                "run current-phase tests only once",
                "run detailed and minimal validation against committed owner manifest",
                "parse every phase JSON and run five-class privacy scan",
                "verify owner and staged manifests, ancestry, three commits, zero merges, one parent per commit, exact head, diff hygiene, and clean state",
            ],
            "full_repository_suite_authorized": False,
            "replay_after_success_allowed": False,
            "preclaims_exact_final_head": False,
            "preclaims_route_sent": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "truth/final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v656-v1.final-checklist.v1",
            "complete_now": [
                "strict x1 before x2",
                "thirty distinct preregistered proposals",
                "thirty valid fixtures and 150 rejected mutations",
                "ten phase-local skills and ten family-compatible runners used",
                "all safe, candidate, and clean-refine portfolio rows resolved",
                "accessible static report with manual and affected-user review reserved",
                "evidence parent retained without an unnecessary correction commit",
                "verified absence of downstream authority",
                "no successor baton, lookup, message, task creation, fork, or delegation",
            ],
            "pending_postcommit": [
                "exact containing final commit",
                "single canonical exact-final pass",
                "four-way remote equality and clean state",
                "no routing action; stop after verified closeout",
            ],
            "incomplete_external": [
                "real empirical GMUT data and likelihood",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID keys, proofs, issuance, resolution, status, revocation, interoperability, privacy and security review, recovery, and governance",
                "affected-party, legal, cultural, and Māori authority",
                "manual and affected-user accessibility evaluation",
                "independent-team reproduction",
                "Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "wellbeing/wellbeing-check-final.json",
        {
            "schema": "ghc.family.v656-v1.wellbeing.final.v1",
            "owner": "Tamar Vey",
            "relational_language_only": True,
            "pace": "steady_with_bounded_recovery",
            "pressure_to_overclaim": False,
            "route_pressure": False,
            "failures_retained_without_shame_or_erasure": True,
            "hamish_may_pause_or_redirect": True,
            "boundary": (
                "A workflow wellbeing note only; not consciousness, emotion, "
                "employment, craft assessment, or identity-continuity evidence."
            ),
        },
    )
    write_json(
        "tooling/ghc-family-index-final-addendum.json",
        {
            "schema": "ghc.family.v656-v1.index-final-addendum.v1",
            "phase": "v656-v1",
            "owner": "Tamar Vey",
            "primary_pillar": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "skills_built_validated_used": 10,
            "runners_built_validated_used": 10,
            "method_flow_pairs": methods["counts"]["methods"],
            "workflow_route_validation_valid": continuation_validation["valid"],
            "active_roster_count": len(ACTIVE_ROSTER),
            "active_roster": ACTIVE_ROSTER,
            "standby_roster": STANDBY_ROSTER,
            "current_family_scripts": [
                "ghc_family_v656_v1_core.py",
                "ghc_family_v656_v1_validate.py",
                "ghc_family_v656_v1_final_validate.py",
                "ghc_family_v656_v1_final_staged_review.py",
            ],
            "route_state": "HELD_NO_DOWNSTREAM_AUTHORITY",
            "route_blocker": "FRESH_LIVE_AND_COMMITTED_ROUTE_REQUIRED",
            "boundary": BOUNDARY,
        },
    )
    write_text(
        "tooling/ghc-family-index-final-addendum.md",
        """# GHC Family Index — Tamar Vey v656-v1 final addendum

This phase-local addendum preserves family-current names, the immutable x1 and
evidence anchors, ten used skills, ten used runners, and the exact matched
Method Flow witness pairs recorded in the final ledger. Historical names remain
compatibility evidence. The route is
`HELD_NO_DOWNSTREAM_AUTHORITY`; no successor baton, lookup, message, task
creation, fork, delegation, or spawn is authorized. Fresh live Hamish
authorization and an exact committed route are required for any later endpoint.

The addendum grants no empirical, professional, production, legal, cultural,
Māori-authority, independent-reproduction, consciousness, personhood,
Theory-of-Everything, AGI/ASI, or Stage 20 credit.
""",
    )
    note = terminal_note()
    note_words = len(note.split())
    if not 300 <= note_words <= 6_000:
        raise RuntimeError(f"terminal note word count outside bounds: {note_words}")
    write_text("terminal/closeout-note.md", note)
    write_json(
        "validation/document-word-cap.json",
        {
            "schema": "ghc.family.v656-v1.document-word-cap.v1",
            "terminal_note_words": note_words,
            "terminal_note_minimum": 300,
            "terminal_note_maximum": 6_000,
            "terminal_note_within_bounds": True,
            "documents": [
                {
                    "path": path.relative_to(PHASE).as_posix(),
                    "words": len(path.read_text(encoding="utf-8").split()),
                }
                for path in sorted(PHASE.rglob("*"))
                if path.is_file() and path.suffix.lower() in {".md", ".html", ".txt"}
            ],
        },
    )
    owner_count = sum(1 for path in PHASE.rglob("*") if path.is_file())
    write_json(
        "validation/owner-file-threshold.json",
        {
            "schema": "ghc.family.v656-v1.owner-file-threshold.v1",
            "owner_file_count_before_lifecycle_self_exclusions": owner_count,
            "threshold": 2000,
            "below_threshold": owner_count < 2000,
            "inherited_repository_baseline_counted": False,
        },
    )
    write_json("validation/final-owner-manifest.json", build_owner_manifest())

    detailed = validator.validate(
        "evidence", "detailed", "validation/final-owner-manifest.json"
    )
    minimal = validator.validate(
        "evidence", "minimal", "validation/final-owner-manifest.json"
    )
    tests = run_closeout_tests()
    receipt = {
        "schema": "ghc.family.v656-v1.closeout-candidate-validation.v1",
        "tests": tests,
        "detailed_valid": detailed["valid"],
        "detailed_check_count": detailed["check_count"],
        "minimal_valid": minimal["valid"],
        "minimal_check_count": minimal["check_count"],
        "json_parse_count_before_self_excluded_receipt": detailed[
            "json_parse_count"
        ],
        "privacy_file_count": detailed["privacy_file_count"],
        "privacy_confirmed_hits": detailed["privacy_confirmed_hits"],
        "owner_manifest_entry_count": detailed["manifest_entry_count"],
        "valid": tests["valid"] and detailed["valid"] and minimal["valid"],
        "full_repository_suite_run": False,
        "final_canonical_pass_run": False,
        "boundary": (
            "Precommit candidate validation only; the exact-final canonical pass "
            "remains pending."
        ),
    }
    write_json("validation/closeout-candidate-validation.json", receipt)
    print(
        json.dumps(
            {
                "state": "combined_final_candidate_built",
                "terminal_note_words": note_words,
                "owner_manifest": detailed["manifest_entry_count"],
                "tests": tests["tests_run"],
                "detailed": detailed["check_count"],
                "minimal": minimal["check_count"],
                "json": detailed["json_parse_count"],
                "privacy_files": detailed["privacy_file_count"],
                "privacy_hits": len(detailed["privacy_confirmed_hits"]),
                "valid": receipt["valid"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    if not receipt["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    build()
