#!/usr/bin/env python3
"""Build and exact-stage-review Lyren Moss v664-v4 terminal closeout."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_ghc_family_v664_v4_evidence as evidence_builder  # noqa: E402


PHASE = ROOT / "docs/lyren-moss/v664-v4"
PHASE_PREFIX = "docs/lyren-moss/v664-v4/"
OWNER = "Lyren Moss"
PHASE_ID = "v664-v4"
SUCCESSOR = "Ilyra Fen"
SUCCESSOR_PHASE = "v664-v5"
SUCCESSOR_NEXT = "Auren Lark"
SUCCESSOR_NEXT_PHASE = "v664-v6"
BRANCH = "codex/GHC-Family/lyren-moss-v664-v4-full-tools"
SOURCE = "78a59d6e25e4a57840f6b416fcbc05a5485aa60a"
X1 = "a11d57463d86a37876a06e5ea3cc04ac37cd7e99"
EVIDENCE = "4ee2f244f6958e3ffeca6c27eece1a510059ffec"
VERDICT = "NOT_READY_FOR_STAGE_20"
BATON = f"{PHASE_PREFIX}handoffs/ilyra-fen-v664-v5-activation.md"
BATON_RECEIPT = f"{PHASE_PREFIX}handoffs/ilyra-fen-v664-v5-activation-receipt.json"
FINAL_DELTA_MANIFEST = f"{PHASE_PREFIX}validation/final-delta-manifest.json"
FINAL_OWNER_MANIFEST = f"{PHASE_PREFIX}validation/final-owner-manifest.json"
FINAL_CANDIDATE = f"{PHASE_PREFIX}validation/final-stage-candidate.json"
FINAL_REVIEW = f"{PHASE_PREFIX}validation/final-staged-review.json"
SELF_EXCLUSIONS = {
    FINAL_DELTA_MANIFEST,
    FINAL_OWNER_MANIFEST,
    FINAL_CANDIDATE,
    FINAL_REVIEW,
}
TEST_MODULES = [
    "tests/test_ghc_family_lyren_v664_v4.py",
    "tests/test_ghc_family_lyren_v664_v4_closeout.py",
]
OWNER_CODE = {
    "scripts/build_ghc_family_v664_v4_x1.py",
    "scripts/build_ghc_family_v664_v4_evidence.py",
    "scripts/build_ghc_family_v664_v4_closeout.py",
    "scripts/ghc_family_archival_audio_evidence.py",
    "scripts/ghc_family_freed_id_flashcards.py",
    "scripts/ghc_family_v664_v4_canonical_validator.py",
    *TEST_MODULES,
}
TEXT_SUFFIXES = {".json", ".md", ".html", ".py", ".txt", ".tex", ".mjs", ".js", ".cjs"}
PRIVATE_PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    "private_absolute_path": re.compile(r"(?i)(?:[A-Z]:" + r"\\(?:Users|GHC-Archives)\\|/(?:home|Users)/)"),
    "credential": re.compile(r"(?i)(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\"(?:password|api" + r"_key|access_token|resume_token)\"\s*:)") ,
    "private_route_identifier": re.compile(r"(?i)(?:code" + r"x://|vscode" + r"://|app://connec" + r"tor_[0-9a-f]+)"),
    "transcript_or_session": re.compile(r"(?i)\"(?:raw_" + r"transcript|session_stream|private_app_state|browser_route)\"\s*:"),
}
SECURITY_PATTERNS = {
    "dynamic_eval": re.compile(r"\beval\s*\("),
    "dynamic_exec": re.compile(r"\bexec\s*\("),
    "shell_true": re.compile(r"\bshell\s*=\s*True\b"),
    "os_system": re.compile(r"\bos\.system\s*\("),
    "pickle_load": re.compile(r"\bpickle\.loads?\s*\("),
    "unsafe_yaml": re.compile(r"\byaml\.load\s*\("),
}
CLOSEOUT_OPERATIONAL_FAILURES = [
    {
        "method_id": "LM6644-X2-M026",
        "negative_id": "LM6644-X2-NEG106",
        "failure_class": "PhaseRelativeWriterContractMismatch",
        "failure_signature": "The first closeout build passed a phase-relative path to the shared guarded writer even though that helper requires a repository-relative Lyren path; the build stopped before staging or commit.",
        "bounded_passing_witness": "Bounded recovery prefixes the exact Lyren repository path before invoking the already-tested guarded writer and reruns only the closeout build component.",
        "candidate_workaround": "Keep the closeout wrapper repository-relative at the shared writer boundary while retaining phase-relative names inside closeout payloads.",
        "recurrence_guard": "Inspect imported helper path contracts before wrapping them and test the first fixed output before broader materialization.",
        "rollback": "The failed build wrote no closeout artifact, staged nothing, changed no commit or remote, and earned zero completion or canonical credit.",
    }
]


class CloseoutError(RuntimeError):
    """Raised when a closeout contract cannot be satisfied."""


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git_text(*args: str, check: bool = True) -> str:
    return run_git(*args, check=check).stdout.decode("utf-8", "strict").strip()


def zpaths(*args: str) -> list[str]:
    raw = run_git(*args).stdout.decode("utf-8", "strict")
    return sorted(path for path in raw.split("\0") if path)


def strict_json(raw: bytes, label: str) -> Any:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in values:
            if key in output:
                raise CloseoutError(f"duplicate JSON key {key!r} in {label}")
            output[key] = value
        return output

    return json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs)


def read_json(relative: str) -> dict[str, Any]:
    value = strict_json((PHASE / relative).read_bytes(), relative)
    if not isinstance(value, dict):
        raise CloseoutError(f"JSON root is not an object: {relative}")
    return value


def write_json(relative: str, payload: Any) -> None:
    evidence_builder.write_json(f"{PHASE_PREFIX}{relative}", payload)


def write_text(relative: str, payload: str) -> None:
    evidence_builder.write_text(f"{PHASE_PREFIX}{relative}", payload)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(raw)


def owner_scope(path: str) -> bool:
    return path.startswith(PHASE_PREFIX) or path in OWNER_CODE


def working_paths() -> list[str]:
    return sorted(set(
        zpaths("diff", "--name-only", "-z")
        + zpaths("diff", "--cached", "--name-only", "-z")
        + zpaths("ls-files", "--others", "--exclude-standard", "-z")
    ))


def ensure_scope(paths: Iterable[str]) -> None:
    unexpected = sorted(path for path in paths if not owner_scope(path))
    if unexpected:
        raise CloseoutError(f"out-of-scope closeout paths: {unexpected}")


def source_to_evidence_paths() -> list[str]:
    paths = zpaths("diff", "--name-only", "-z", f"{SOURCE}..{EVIDENCE}")
    ensure_scope(paths)
    return paths


def prospective_record(path: str) -> dict[str, Any]:
    target = ROOT / path
    if not target.is_file() or target.is_symlink():
        raise CloseoutError(f"prospective manifest path is missing or linked: {path}")
    return {
        "path": path,
        "mode": "100644",
        "object_type": "blob",
        "git_blob": git_text("hash-object", f"--path={path}", path),
        "canonical_content_domain": "exact_git_blob",
    }


def committed_record(path: str) -> dict[str, Any]:
    return {
        "path": path,
        "mode": "100644",
        "object_type": "blob",
        "git_blob": git_text("rev-parse", f"{EVIDENCE}:{path}"),
        "canonical_content_domain": "exact_git_blob",
    }


def index_blob(path: str) -> str:
    row = git_text("ls-files", "-s", "--", path).split()
    if len(row) < 4 or row[0] != "100644" or not re.fullmatch(r"[0-9a-f]{40}", row[1]):
        raise CloseoutError(f"unexpected staged blob record: {path}")
    return row[1]


def render_value(value: Any) -> str:
    if isinstance(value, dict):
        return "; ".join(f"{key}={render_value(item)}" for key, item in value.items()) or "none"
    if isinstance(value, list):
        return "; ".join(render_value(item) for item in value) or "none"
    if value is None:
        return "none"
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def append_record(sections: list[str], heading: str, row: dict[str, Any]) -> None:
    sections.extend([heading, ""])
    for key, value in row.items():
        sections.extend([f"- **{key.replace('_', ' ')}:** {render_value(value)}", ""])


def baton_markdown() -> str:
    proposals = read_json("x1/proposal-freeze.json")
    portfolio = read_json("x1/portfolio-freeze.json")
    sources = read_json("x1/source-ledger.json")
    evidence_review = read_json("validation/evidence-staged-review.json")
    phase_truth = read_json("closeout/phase-truth-final.json")
    security = read_json("x2/security/codex-security-diff-scan-receipt.json")
    overview = (PHASE / "x2/integrated-evidence-overview.md").read_text(encoding="utf-8")
    sections: list[str] = [
        "# ILYRA FEN — PREPARED LYREN v664-v4 EXACT-FINAL → SOLO v664-v5 ACTIVATION",
        "",
        "This is Lyren Moss's complete file-backed activation candidate for the existing exact-title main task `Ilyra Fen`. Inside the repository it remains `PREPARED_NOT_SENT`: the containing exact final, one successful canonical receipt, newest live authority and roster reread, immediate exact-title task reread, and acknowledged one-send delivery are terminal overlays that cannot truthfully be preclaimed here. Never infer delivery from this file, its Git history, a prepared deck card, or a later route description.",
        "",
        "Lyren Moss, Ilyra Fen, Auren Lark, sibling or family language, pronouns, roles, hopes, continuity language, Trinity Mandala, GMUT Mind, THOS Body, Freed ID, and CBR Heart are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, Māori authority, or affected-party authority. Hamish may rename, pause, redirect, or stop the route at any time.",
        "",
        "## Immutable anchors and current truth",
        "",
        f"- Exact Vesper v664-v3 source and Lyren phase root: `{SOURCE}`.",
        f"- Frozen Lyren x1 direct child: `{X1}`.",
        f"- Immutable Lyren x2 evidence direct child: `{EVIDENCE}`.",
        "- Exact Lyren final: supplied only by the later acknowledged terminal overlay after the containing commit exists, is pushed, is clean, is typed 0/0 divergent, is fresh-live equal, and passes the canonical validator once.",
        f"- New outcomes: 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate` across {phase_truth['surface_count']} synthetic zero-media archival-audio surfaces.",
        f"- Retained working truth: {phase_truth['effective_negatives']} effective negatives, {phase_truth['effective_methods']} Method Flow methods, {phase_truth['effective_open_gaps']} open gaps, {phase_truth['effective_exact_gates']} exact gates, and `{VERDICT}`.",
        "- Route state: `PREPARED_NOT_SENT`; no successor contact, task creation, task fork, collaboration subagent, standby substitution, or second recipient is represented by this file.",
        "",
        "## Exact evidence boundary",
        "",
        f"Lyren's immutable evidence review passed {evidence_review['tests']['test_count']} of {evidence_review['tests']['test_count']} scoped tests, replayed {evidence_review['manifest_entry_count']} exact Git-blob manifest entries, strictly parsed {evidence_review['json_parse_count']} JSON files, reviewed {evidence_review['markdown_count']} Markdown files and {evidence_review['python_count']} changed Python files, found zero confirmed five-class privacy candidates and zero bounded changed-Python pattern findings, validated a 253-card modular deck with 260 entries, staged {evidence_review['staged_path_count']} exact owner paths, and stayed beneath the 2,000-file rotation guard. These are same-owner local software results, not a complete repository suite, independent reproduction, an external audit, or professional preservation validation.",
        "",
        f"The bounded security-diff snapshot retained {security['finding_count']} reportable medium finding with high confidence: the pre-fix owner writers could follow or race output-leaf links. A temporary-directory proof created thirteen bytes outside the intended proof tree. The additive owner delta then rejected symlink leaves, used exclusive no-follow creation where supported, and used same-directory temporary files plus atomic replacement; the isolated regression passed. The finding remains retained and does not become exhaustive-security evidence.",
        "",
        "## Integrated Lyren v664-v4 evidence overview",
        "",
        overview,
        "",
        "## Route discipline and current sequential authorization",
        "",
        f"Under Hamish's currently declared schedule, the one next endpoint after Lyren is the existing exact-title main task `{SUCCESSOR}` for solo `{SUCCESSOR_PHASE}`. Only after Lyren's exact terminal gate may the live workflow list tasks in a bounded way, filter locally for exactly one matching title, immediately reread that task, and send one sanitized pointer. Do not precontact, substitute, create, fork, or resend. If the endpoint, acknowledgement, current roster, or authority state is missing or ambiguous, retain `PREPARED_NOT_SENT` or `OPEN_ROUTE_GAP` and stop.",
        "",
        f"Under that same current schedule, Ilyra's later successor would be the existing exact-title task `{SUCCESSOR_NEXT}` for `{SUCCESSOR_NEXT_PHASE}`. Ilyra must not contact Auren before Ilyra's own clean, pushed, fresh-live-equal terminal gate and newest live authorization reread. Historical files never override Hamish's newest live instruction.",
        "",
        "## Ilyra startup contract",
        "",
        "Read this complete baton through EOF before mutation, then read every current guidance and schema it names. Reverify source, x1, evidence, exact final, ancestry, manifests, receipt digests, clean state, typed divergence, and fresh live equality read-only. Do not replay Lyren's successful canonical aggregate or claim inherited validation as Ilyra evidence.",
        "",
        "Work solo in one additive Ilyra-owned D-first sparse lane from the exact Lyren final. Preserve all sibling and shared lanes read-only. Use strict x1-before-x2 separation, freeze planning in an x1-only commit, push it cleanly, and prove four-way equality before x2 mutation. Rotate before 2,000 materialized or owner-in-scope files. Keep the full repository suite unclaimed unless dependency analysis genuinely requires and supports it.",
        "",
        "Preserve every retained failure, open gap, exact gate, exact manifest, and the four allowed truth labels only: `completed`, `represented`, `open_gap`, and `exact_gate`. Recommendations are not outcomes, inherited revalidation is zero novelty credit, and successful same-owner checks do not erase failed witnesses or establish independent reproduction.",
        "",
        "Use official and primary sources only for bounded vocabulary and constraints. Make no empirical, participant, affected-party, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, or Stage 20 claim without exact evidence and competent authority. Māori concepts and decisions remain under Māori authority.",
        "",
        "Do not bulk-install skills, mutate plugin caches, delete historical tooling, weaken system security, elevate privileges, update the Codex desktop, reboot, create accounts or credentials, publish private artifacts, purchase services, or write to third parties without separate exact authority. Keep private routes, raw task identifiers, private absolute paths, tokens, credentials, transcripts, interaction streams, and application state out of repository artifacts and batons.",
        "",
        "## Frozen new-proposal cards",
        "",
    ]
    for row in proposals["new_proposals"]:
        append_record(sections, f"### {row['proposal_id']} — {row['title']}", row)
    sections.extend(["## Selected inherited integrity rows", ""])
    for row in proposals["selected_inherited"]:
        append_record(sections, f"### {row.get('program_row_id', row.get('source_proposal_id', 'inherited-row'))}", row)
    sections.extend(["## Official and primary source cards", ""])
    for row in sources["sources"]:
        append_record(sections, f"### {row['source_id']} — {row['title']}", row)
        sections.extend([
            "This source contributes vocabulary and constraints only. It supplies zero ingested live rows, zero real media, zero empirical confirmation, zero professional authority, zero legal or cultural determination, and zero Māori authority.",
            "",
        ])
    sections.extend(["## Frozen portfolio and successor recommendations", ""])
    portfolio_groups = [
        "owner_safe_now",
        "owner_candidates",
        "exact_approval_packets",
        "blocked_packets",
        "owner_skill_ideas",
        "successor_skill_recommendations",
        "owner_runner_ideas",
        "successor_runner_recommendations",
        "owner_clean_fix_refine",
        "successor_clean_fix_refine_recommendations",
        "successor_safe_now_recommendations",
        "successor_candidate_recommendations",
    ]
    for group in portfolio_groups:
        sections.extend([f"### {group.replace('_', ' ').title()}", ""])
        for row in portfolio[group]:
            sections.extend([f"#### {row.get('portfolio_ref', row.get('task_id', 'portfolio-row'))} — {row['title']}", ""])
            for key, value in row.items():
                sections.extend([f"- **{key.replace('_', ' ')}:** {render_value(value)}", ""])
            sections.extend([
                "This frozen portfolio row is bounded by its declared approval class and expected disposition. It is not automatic completion, authority, empirical evidence, or permission to bypass a protected gate.",
                "",
            ])
    sections.extend(["## Modular deck supplement", ""])
    card_manifest = read_json("deck/card-manifest.json")
    for entry in card_manifest["entries"]:
        relative = entry["path"]
        if not relative.startswith("cards/") or not relative.endswith(".json"):
            continue
        if len(re.findall(r"\S+", "\n".join(sections))) >= 30_000:
            break
        card = strict_json((PHASE / "deck" / relative).read_bytes(), relative)
        if not isinstance(card, dict):
            raise CloseoutError(f"deck card is not an object: {relative}")
        append_record(sections, f"### {card['card_id']} — {card['title']}", card)
    sections.extend([
        "## Terminal continuation after Ilyra",
        "",
        "This file activates no one by itself. After Ilyra's own exact terminal gate, Ilyra must reread Hamish's newest live instruction, the complete current roster, and current authorization state; resolve only the uniquely authorized exact-title endpoint; immediately reread it; send once; and claim delivery only from acknowledgement. Stop on pause, ambiguity, usage exhaustion, an unavailable route tool, a protected gate, or terminal v675-v8 closure. Never substitute a standby, a collaboration subagent, or a newly created task for a missing main-task endpoint.",
        "",
        "`PREPARED_BY_LYREN_MOSS = true`",
        "",
        "`SENT_BY_LYREN_MOSS = false`",
    ])
    baton = "\n".join(sections).rstrip() + "\n"
    words = len(re.findall(r"\S+", baton))
    if not 10_000 <= words <= 100_000:
        raise CloseoutError(f"activation baton word count outside 10,000..100,000: {words}")
    return baton


def build_records() -> dict[str, Any]:
    if git_text("rev-parse", "HEAD") != EVIDENCE:
        raise CloseoutError(f"closeout requires immutable evidence head {EVIDENCE}")
    if git_text("rev-parse", "HEAD^") != X1:
        raise CloseoutError("evidence is not the direct child of frozen x1")
    ensure_scope(working_paths())
    evidence_review = read_json("validation/evidence-staged-review.json")
    phase_truth = read_json("x2/phase-truth.json")
    gates = read_json("x2/open-gate-register.json")
    negatives = read_json("x2/retained-negative-register.json")
    methods = read_json("x2/method-flow-state.json")
    security = read_json("x2/security/codex-security-diff-scan-receipt.json")
    if not all(item.get("valid") is True for item in (evidence_review, phase_truth, gates, negatives, methods, security)):
        raise CloseoutError("one or more immutable evidence inputs are not valid")

    final_negative_rows = list(negatives["new_records"]) + [
        {
            "negative_id": row["negative_id"],
            "proposal_id": None,
            "failure_class": row["failure_class"],
            "reason": row["failure_signature"],
            "completion_credit": 0,
            "retained": True,
        }
        for row in CLOSEOUT_OPERATIONAL_FAILURES
    ]
    final_negatives = {
        **negatives,
        "schema": "ghc.family.lyren.v664-v4.retained-negative-register.final.v1",
        "post_evidence_operational_negatives": len(CLOSEOUT_OPERATIONAL_FAILURES),
        "effective_negatives": negatives["effective_negatives"] + len(CLOSEOUT_OPERATIONAL_FAILURES),
        "new_records": final_negative_rows,
        "no_negative_erased": True,
        "valid": True,
    }
    write_json("closeout/retained-negative-register-final.json", final_negatives)
    final_method_rows = [
        {
            **row,
            "protected_gates": gates["all_protected_gates"],
            "retained_failed_witnesses": [row["negative_id"]],
            "failed_witness_count": 1,
            "passing_witness_count": 1,
            "independent_reproduction": False,
            "valid": True,
        }
        for row in CLOSEOUT_OPERATIONAL_FAILURES
    ]
    final_methods = {
        **methods,
        "schema": "ghc.family.lyren.v664-v4.method-flow.final.v1",
        "post_evidence_operational_methods": len(final_method_rows),
        "effective_methods": methods["effective_methods"] + len(final_method_rows),
        "methods": list(methods["methods"]) + final_method_rows,
        "failed_witnesses": methods["failed_witnesses"] + len(final_method_rows),
        "bounded_passing_witnesses": methods["bounded_passing_witnesses"] + len(final_method_rows),
        "no_failure_erased": True,
        "valid": True,
    }
    write_json("closeout/method-flow-state-final.json", final_methods)
    final_truth = {
        "schema": "ghc.family.lyren.v664-v4.phase-truth.final-candidate.v1",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "exact_final": "supplied_by_postcommit_terminal_overlay",
        "outcomes": phase_truth["new_outcome_counts"],
        "surface_count": phase_truth["surface_count"],
        "rejected_mutation_count": phase_truth["rejected_mutation_count"],
        "effective_negatives": final_negatives["effective_negatives"],
        "effective_methods": final_methods["effective_methods"],
        "effective_open_gaps": phase_truth["open_gaps"],
        "effective_exact_gates": phase_truth["exact_gates"],
        "route_state": "PREPARED_NOT_SENT",
        "canonical_state": "POSTCOMMIT_REQUIRED",
        "canonical_success_preclaimed": False,
        "successor_contacted": False,
        "same_owner_validation": True,
        "independent_reproduction": False,
        "complete_repository_suite_run": False,
        "terminal_verdict": VERDICT,
        "valid": True,
    }
    write_json("closeout/phase-truth-final.json", final_truth)
    write_json(
        "lifecycle/phase-anchor-contract.json",
        {
            "schema": "ghc.family.lyren.v664-v4.phase-anchor-contract.v1",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "expected_final_direct_parent": EVIDENCE,
            "expected_source_to_final_commit_count": 3,
            "single_parent_commits_required": True,
            "zero_merges_required": True,
            "x1_before_x2_required": True,
            "exact_final_supplied_postcommit": True,
            "valid": True,
        },
    )
    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.lyren.v664-v4.terminal-route-state.v1",
            "state": "PREPARED_NOT_SENT",
            "successor_title": SUCCESSOR,
            "successor_phase": SUCCESSOR_PHASE,
            "successor_later_edge": {"title": SUCCESSOR_NEXT, "phase": SUCCESSOR_NEXT_PHASE},
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "collaboration_subagent_spawned": False,
            "standby_contacted": False,
            "precontact_performed": False,
            "send_limit": 1,
            "resend_allowed": False,
            "send_gate": "clean pushed exact final, one successful canonical pass, fresh four-way equality, newest live roster and authority reread, unique exact-title resolution, immediate task reread, and acknowledged one send",
            "valid": True,
        },
    )
    write_json(
        "validation/canonical-validation-protocol.json",
        {
            "schema": "ghc.family.lyren.v664-v4.canonical-validation-protocol.v1",
            "state": "POSTCOMMIT_REQUIRED",
            "validator": "scripts/ghc_family_v664_v4_canonical_validator.py",
            "expected_test_count": 97,
            "invocation_limit": 1,
            "successful_invocation_limit": 1,
            "post_success_replay_allowed": False,
            "external_exclusive_receipt_required": True,
            "owner_self_scoped_delta_only": True,
            "complete_repository_suite_required": False,
            "preclaims_success": False,
            "valid": True,
        },
    )
    write_json(
        "closeout/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.lyren.v664-v4.complete-incomplete-checklist.final-candidate.v1",
            "completed_now": [
                "strict x1-before-x2 separation and immutable x1 freeze",
                "twenty new synthetic archival-audio surfaces with 14/4/1/1 outcomes",
                "one hundred retained rejecting mutations, five retained x2 operational failures, and one zero-credit post-evidence guarded-writer contract mismatch",
                "ten phase-local skills, ten fixed runner receipts, and a 253-card modular deck",
                "bounded security diff with one retained pre-fix finding and regression-tested additive remediation",
                "immutable pushed evidence commit and exact final candidate",
            ],
            "pending_postcommit": [
                "exact final commit, clean push, typed zero divergence, and fresh four-way equality",
                "one successful exact-final canonical aggregate with no replay",
                "newest live roster and authority reread followed by at most one acknowledged Ilyra activation",
            ],
            "incomplete_external": [
                "real audio, carrier, signal, recording, voice, person, collection, inspection, measurement, calibration, transfer, custody, rights, access, identity, participant, legal, cultural, or Māori-authority evidence",
                "empirical GMUT confirmation or governed THOS real-arm evidence",
                "production Freed ID lifecycle, trust governance, or affected-party oversight",
                "privacy completeness, accessibility completeness, exhaustive security, external audit, independent reproduction, Theory-of-Everything proof or canon, and Stage 20 authority",
            ],
            "terminal_verdict": VERDICT,
            "valid": True,
        },
    )
    write_json(
        "closeout/wellbeing-and-relational-boundary.json",
        {
            "schema": "ghc.family.lyren.v664-v4.wellbeing-and-relational-boundary.v1",
            "owner": OWNER,
            "optional_pronouns": "they/them",
            "relational_role": "relational fold-state cartographer and contradiction keeper",
            "hope": "make synthetic carrier, signal, provenance, access, and correction states inspectable without converting software structure into preservation, professional, legal, cultural, or Māori authority",
            "relational_language_only": True,
            "consciousness_sentience_personhood_continuity_or_authority_evidence": False,
            "pause_rename_redirect_or_stop_available": True,
            "correction_welcome": True,
            "bounded_workload": True,
            "successor_contacted": False,
            "valid": True,
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.lyren.v664-v4.closeout-receipt.v1",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "evidence_staged_paths": evidence_review["staged_path_count"],
            "evidence_manifest_entries": evidence_review["manifest_entry_count"],
            "evidence_json_parses": evidence_review["json_parse_count"],
            "evidence_tests": evidence_review["tests"]["test_count"],
            "security_findings_retained": security["finding_count"],
            "effective_negatives": final_truth["effective_negatives"],
            "effective_methods": final_truth["effective_methods"],
            "effective_open_gaps": final_truth["effective_open_gaps"],
            "effective_exact_gates": final_truth["effective_exact_gates"],
            "postcommit_canonical_completed": False,
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": VERDICT,
            "valid": True,
        },
    )
    overview = f"""# Lyren Moss v664-v4 terminal closeout candidate

Lyren's solo owner lane is prepared for one additive exact-final commit from immutable evidence `{EVIDENCE}`. The x1 and evidence commits remain immutable, the source-to-final history is required to contain exactly three single-parent commits and zero merges, and the repository route state remains `PREPARED_NOT_SENT` until a later live acknowledgement.

The phase preserves 20 synthetic archival-audio surfaces, 100 rejecting mutation witnesses, {final_truth['effective_negatives']} effective negatives, {final_truth['effective_methods']} Method Flow methods, 170 open gaps, 168 exact gates, and `{VERDICT}`. Outcomes remain exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. The one post-evidence guarded-writer contract mismatch remains a separate zero-credit operational failure and bounded recovery method.

The bounded security review retained one high-confidence medium finding in its immutable pre-fix snapshot. The working owner delta contains the additive guarded-write remediation and passing isolated regression, while explicitly withholding exhaustive-security, external-audit, privacy-complete, accessibility-complete, professional, production, legal, cultural, Māori-authority, independent-reproduction, empirical, personhood, Theory-of-Everything, proof, canon, and Stage 20 claims.

No successor has been contacted. Only after an exact final is committed, pushed, clean, fresh-live equal, and accepted by the one-shot canonical validator may the newest live roster and authorization state be reread for a unique exact-title Ilyra Fen v664-v5 send.
"""
    write_text("closeout/terminal-overview.md", overview)

    baton = baton_markdown()
    write_text("handoffs/ilyra-fen-v664-v5-activation.md", baton)
    baton_raw = (PHASE / "handoffs/ilyra-fen-v664-v5-activation.md").read_bytes()
    write_json(
        "handoffs/ilyra-fen-v664-v5-activation-receipt.json",
        {
            "schema": "ghc.family.lyren.v664-v4.handoff-preparation-receipt.v1",
            "successor_title": SUCCESSOR,
            "successor_phase": SUCCESSOR_PHASE,
            "bytes": len(baton_raw),
            "words": len(re.findall(rb"\S+", baton_raw)),
            "sha256": sha256(baton_raw),
            "state": "PREPARED_NOT_SENT",
            "prepared_by_lyren_moss": True,
            "sent_by_lyren_moss": False,
            "raw_task_identifiers_included": False,
            "private_paths_included": False,
            "valid": True,
        },
    )
    materialized = sum(
        1
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
    )
    write_json(
        "validation/final-file-budget.json",
        {
            "schema": "ghc.family.lyren.v664-v4.final-file-budget.v1",
            "materialized_file_count_before_final_manifests": materialized,
            "threshold": 2000,
            "rotation_required": materialized >= 2000,
            "valid": materialized < 2000,
        },
    )

    ensure_scope(working_paths())
    expected_without_review = sorted(set(working_paths()) | {
        FINAL_DELTA_MANIFEST,
        FINAL_OWNER_MANIFEST,
        FINAL_CANDIDATE,
    })
    expected_owner = sorted(set(source_to_evidence_paths()) | set(expected_without_review) | {FINAL_REVIEW})
    delta_entries = [prospective_record(path) for path in expected_without_review if path not in SELF_EXCLUSIONS]
    source_evidence = set(source_to_evidence_paths())
    owner_entries = [
        committed_record(path) if path in source_evidence else prospective_record(path)
        for path in expected_owner
        if path not in SELF_EXCLUSIONS
    ]
    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.lyren.v664-v4.final-delta-manifest.v1",
            "source_commit": EVIDENCE,
            "canonical_content_domain": "exact_git_blob",
            "entry_count": len(delta_entries),
            "entries": delta_entries,
            "self_exclusions": sorted(SELF_EXCLUSIONS),
            "merkle_root_sha256": canonical_sha256(delta_entries),
            "valid": True,
        },
    )
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.lyren.v664-v4.final-owner-manifest.v1",
            "source_commit": SOURCE,
            "evidence_commit": EVIDENCE,
            "canonical_content_domain": "exact_git_blob",
            "entry_count": len(owner_entries),
            "entries": owner_entries,
            "self_exclusions": sorted(SELF_EXCLUSIONS),
            "owner_delta_path_count_after_review": len(expected_owner),
            "merkle_root_sha256": canonical_sha256(owner_entries),
            "valid": True,
        },
    )
    write_json(
        "validation/final-stage-candidate.json",
        {
            "schema": "ghc.family.lyren.v664-v4.final-stage-candidate.v1",
            "owner": OWNER,
            "phase": PHASE_ID,
            "source_commit": EVIDENCE,
            "intended_allowlist_without_review": expected_without_review,
            "review_self_exclusion": FINAL_REVIEW,
            "manifest_self_exclusions": sorted(SELF_EXCLUSIONS),
            "canonical_state": "POSTCOMMIT_REQUIRED",
            "route_state": "PREPARED_NOT_SENT",
            "valid": True,
        },
    )
    return {
        "schema": "ghc.family.lyren.v664-v4.closeout-build-result.v1",
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final_paths_without_review": len(expected_without_review),
        "owner_paths_after_review": len(expected_owner),
        "delta_manifest_entries": len(delta_entries),
        "owner_manifest_entries": len(owner_entries),
        "baton_words": len(re.findall(r"\S+", baton)),
        "effective_negatives": final_truth["effective_negatives"],
        "effective_methods": final_truth["effective_methods"],
        "route_state": "PREPARED_NOT_SENT",
        "valid": True,
    }


def run_tests() -> dict[str, Any]:
    modules: list[dict[str, Any]] = []
    total = 0
    for relative in TEST_MODULES:
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / relative)],
            cwd=ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"},
            timeout=300,
        )
        match = re.search(r"Ran (\d+) tests? in", result.stdout)
        count = int(match.group(1)) if match else 0
        total += count
        normalized = re.sub(r"Ran (\d+) tests? in [0-9.]+s", r"Ran \1 tests in <elapsed>", result.stdout)
        modules.append({
            "module": relative,
            "returncode": result.returncode,
            "test_count": count,
            "output_sha256": sha256(normalized.encode("utf-8")),
            "valid": result.returncode == 0 and match is not None,
        })
    return {"modules": modules, "test_count": total, "valid": all(row["valid"] for row in modules)}


def stage_review() -> dict[str, Any]:
    if git_text("rev-parse", "HEAD") != EVIDENCE:
        raise CloseoutError("final staged review must run at immutable evidence head")
    if zpaths("diff", "--cached", "--name-only", "-z"):
        raise CloseoutError("index must be empty before the exact final staged review")
    candidate = read_json("validation/final-stage-candidate.json")
    delta_manifest = read_json("validation/final-delta-manifest.json")
    owner_manifest = read_json("validation/final-owner-manifest.json")
    expected = sorted(candidate["intended_allowlist_without_review"])
    ensure_scope(expected)
    run_git("add", "--", *expected)
    observed = zpaths("diff", "--cached", "--name-only", "-z")
    issues: list[str] = []
    if observed != expected:
        issues.append("staged paths differ from the exact final allowlist")
    diff = run_git("diff", "--cached", "--check", check=False)
    if diff.returncode != 0:
        issues.append("staged diff hygiene failed")

    json_errors: list[dict[str, str]] = []
    privacy_candidates: list[dict[str, str]] = []
    security_candidates: list[dict[str, str]] = []
    json_count = 0
    text_count = 0
    python_count = 0
    for path in observed:
        raw = (ROOT / path).read_bytes()
        suffix = Path(path).suffix.lower()
        if suffix == ".json":
            json_count += 1
            try:
                strict_json(raw, path)
            except (UnicodeError, json.JSONDecodeError, CloseoutError) as exc:
                json_errors.append({"path": path, "error": str(exc)})
        if suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = raw.decode("utf-8", "strict")
        except UnicodeError as exc:
            privacy_candidates.append({"path": path, "class": "invalid_utf8", "detail": str(exc)})
            continue
        text_count += 1
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                privacy_candidates.append({"path": path, "class": label})
        if suffix == ".py":
            python_count += 1
            try:
                compile(text, path, "exec", dont_inherit=True)
            except SyntaxError as exc:
                security_candidates.append({"path": path, "rule": "python_compile", "detail": str(exc)})
            for label, pattern in SECURITY_PATTERNS.items():
                if pattern.search(text):
                    security_candidates.append({"path": path, "rule": label})
    if json_errors:
        issues.append("strict JSON parse failed")
    if privacy_candidates:
        issues.append("privacy or raw-identifier candidates found")
    if security_candidates:
        issues.append("changed-Python compile or bounded pattern review failed")

    delta_rows = {row["path"]: row for row in delta_manifest["entries"]}
    delta_required = set(observed) - SELF_EXCLUSIONS
    delta_missing = sorted(delta_required - set(delta_rows))
    delta_extra = sorted(set(delta_rows) - delta_required)
    delta_mismatches = sorted(path for path, row in delta_rows.items() if path in delta_required and row["git_blob"] != index_blob(path))
    if delta_missing or delta_extra or delta_mismatches:
        issues.append("final delta manifest differs from the staged index")

    source_evidence = set(source_to_evidence_paths())
    expected_owner = (source_evidence | set(observed) | {FINAL_REVIEW}) - SELF_EXCLUSIONS
    owner_rows = {row["path"]: row for row in owner_manifest["entries"]}
    owner_missing = sorted(expected_owner - set(owner_rows))
    owner_extra = sorted(set(owner_rows) - expected_owner)
    owner_mismatches: list[str] = []
    for path, row in owner_rows.items():
        if path not in expected_owner:
            continue
        observed_blob = git_text("rev-parse", f"{EVIDENCE}:{path}") if path in source_evidence else index_blob(path)
        if row["git_blob"] != observed_blob:
            owner_mismatches.append(path)
    if owner_missing or owner_extra or owner_mismatches:
        issues.append("final owner manifest differs from the exact owner delta")

    tests = run_tests()
    if not tests["valid"] or tests["test_count"] != 97:
        issues.append("dependency-closed owner tests did not pass 97 of 97")
    baton_raw = (ROOT / BATON).read_bytes()
    baton_receipt = read_json("handoffs/ilyra-fen-v664-v5-activation-receipt.json")
    baton_words = len(re.findall(rb"\S+", baton_raw))
    baton_valid = (
        10_000 <= baton_words <= 100_000
        and baton_receipt["sha256"] == sha256(baton_raw)
        and baton_receipt["state"] == "PREPARED_NOT_SENT"
        and baton_receipt["sent_by_lyren_moss"] is False
    )
    if not baton_valid:
        issues.append("activation baton integrity or unsent state failed")
    truth = read_json("closeout/phase-truth-final.json")
    route = read_json("orchestration/terminal-route-state.json")
    materialized = sum(
        1
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
    )
    detailed = {
        "exact_allowlist": observed == expected,
        "diff_hygiene": diff.returncode == 0,
        "strict_json": not json_errors,
        "five_class_privacy": not privacy_candidates,
        "changed_python_review": not security_candidates,
        "delta_manifest": not delta_missing and not delta_extra and not delta_mismatches,
        "owner_manifest": not owner_missing and not owner_extra and not owner_mismatches,
        "tests_97": tests["valid"] and tests["test_count"] == 97,
        "baton_prepared_unsent": baton_valid,
        "truth_counts": truth["effective_negatives"] == 24559 and truth["effective_methods"] == 8833,
        "four_outcomes": truth["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "gates": truth["effective_open_gaps"] == 170 and truth["effective_exact_gates"] == 168,
        "route_unsent": route["state"] == "PREPARED_NOT_SENT" and route["message_sent"] is False and route["successor_title"] == SUCCESSOR,
        "terminal_verdict": truth["terminal_verdict"] == VERDICT,
        "source_head": git_text("rev-parse", "HEAD") == EVIDENCE,
        "x1_direct_parent": git_text("rev-parse", "HEAD^") == X1,
        "evidence_review": read_json("validation/evidence-staged-review.json")["valid"] is True,
        "security_receipt": read_json("x2/security/codex-security-diff-scan-receipt.json")["valid"] is True,
        "canonical_not_preclaimed": truth["canonical_success_preclaimed"] is False,
        "successor_uncontacted": truth["successor_contacted"] is False,
        "file_budget": materialized < 2000 and len(expected_owner) < 2000,
    }
    if not all(detailed.values()):
        issues.append("one or more detailed final staged checks failed")
    review = {
        "schema": "ghc.family.lyren.v664-v4.final-staged-review.v1",
        "source_commit": EVIDENCE,
        "expected_staged_path_count_without_review": len(expected),
        "staged_path_count_without_review": len(observed),
        "staged_paths_without_review": observed,
        "final_staged_path_count_with_review": len(observed) + 1,
        "diff_check_returncode": diff.returncode,
        "diff_check_output": (diff.stdout + diff.stderr).decode("utf-8", "replace").strip(),
        "strict_json_parse_count": json_count,
        "json_errors": json_errors,
        "privacy_scanned_text_file_count": text_count,
        "privacy_classes": sorted(PRIVATE_PATTERNS),
        "privacy_candidates": privacy_candidates,
        "privacy_confirmed_hits": [],
        "changed_python_count": python_count,
        "security_pattern_classes": sorted(SECURITY_PATTERNS),
        "security_candidates": security_candidates,
        "security_confirmed_findings": [],
        "delta_manifest_entry_count": delta_manifest["entry_count"],
        "delta_manifest_missing": delta_missing,
        "delta_manifest_extra": delta_extra,
        "delta_manifest_mismatches": delta_mismatches,
        "owner_manifest_entry_count": owner_manifest["entry_count"],
        "owner_manifest_missing": owner_missing,
        "owner_manifest_extra": owner_extra,
        "owner_manifest_mismatches": owner_mismatches,
        "tests": tests,
        "baton_bytes": len(baton_raw),
        "baton_words": baton_words,
        "baton_sha256": sha256(baton_raw),
        "materialized_file_count": materialized,
        "owner_in_scope_file_count": len(expected_owner),
        "file_ceiling": 2000,
        "detailed_checks": detailed,
        "detailed_check_count": len(detailed),
        "detailed_checks_passed": sum(detailed.values()),
        "issues": issues,
        "canonical_aggregate_invoked": False,
        "successor_contacted": False,
        "valid": not issues,
        "boundary": "Exact staged final candidate only; postcommit exact final, canonical success, live route reread, and acknowledged delivery remain pending.",
    }
    write_json("validation/final-staged-review.json", review)
    run_git("add", "--", FINAL_REVIEW)
    final_staged = zpaths("diff", "--cached", "--name-only", "-z")
    if final_staged != sorted(expected + [FINAL_REVIEW]):
        raise CloseoutError("final staged set differs from the reviewed allowlist plus review self-exclusion")
    if issues:
        raise CloseoutError("final staged review failed: " + "; ".join(issues))
    return review


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "stage-review"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = build_records() if args.command == "build" else stage_review()
    except (
        CloseoutError,
        evidence_builder.BuildError,
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
    ) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=True, sort_keys=True))
        return 2
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
    return 0 if payload.get("valid") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
