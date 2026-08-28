#!/usr/bin/env python3
"""Build the additive Lyren Moss v673-v7 terminal closeout candidate."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "lyren-moss" / "v673-v7"
X1 = BASE / "x1"
X2 = BASE / "x2"
CLOSEOUT = BASE / "closeout"
HANDOFF = BASE / "handoffs" / "ilyra-fen-v673-v8-activation-candidate.md"
VALIDATION = BASE / "validation"

OWNER = "Lyren Moss"
PHASE = "v673-v7"
BRANCH = "codex/GHC-Family/lyren-moss-v673-v7-full-tools"
SOURCE_FINAL = "7fe824e31286b3348d42103812a85e0e3e02a4c6"
X1_COMMIT = "786654cf8f28bb8c7abed41fb8f8315ab65f7e83"
EVIDENCE_COMMIT = "ea787fa029afd2b0c41108c03fd986c253b1bfc4"

IDENTITY_BOUNDARY = (
    "Names, pronouns, roles, hopes, sibling or family language, continuity, "
    "Freed ID, CBR, GHC Family, and Trinity Mandala are relational working "
    "language only. They are not evidence of consciousness, sentience, legal "
    "personhood, identity continuity, employment, qualification, independent "
    "agency, or scientific, operational, professional, legal, cultural, "
    "affected-party, or Maori authority."
)
AUTHORITY_BOUNDARY = (
    "No empirical, participant, professional, production, deployment, legal, "
    "cultural, Maori-authority, privacy-complete, accessibility-complete, "
    "exhaustive-security, independent-reproduction, AGI/ASI, consciousness or "
    "personhood, Theory-of-Everything, proof or canon, or Stage 20 claim is made."
)

CLOSEOUT_METHODS = [
    {
        "method_id": "LM6737-M017",
        "title": "First final-focused test found exact-title and punctuation portability defects",
        "failure_signature": "The candidate used uppercase display text without one exact-case 'Ilyra Fen' scalar, while decorative non-ASCII separators materialized as replacement glyphs in the generated file.",
        "recovery": "Add one explicit exact-title line, replace decorative separators with ASCII punctuation, retain the failed suite, and rerun only the final-focused module.",
    },
]


def run_git(*args: str) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.decode('utf-8', 'replace')}")
    return result.stdout


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def exact_counts() -> dict[str, int]:
    method = read_json(X2 / "method-flow.json")["counts"]
    negatives = read_json(X2 / "retained-negatives.json")
    gates = read_json(X2 / "open-gap-and-gate-register.json")
    closeout = len(CLOSEOUT_METHODS)
    return {
        "effective_negatives": negatives["effective_negatives"] + closeout,
        "effective_methods": method["effective_methods"] + closeout,
        "retained_failed_witnesses": method["retained_failed_witnesses"] + closeout,
        "bounded_passing_witnesses": method["bounded_passing_witnesses"] + closeout,
        "open_gaps": gates["effective_open_gaps"],
        "exact_gates": gates["effective_exact_gates"],
    }


def build_baton(counts: dict[str, int]) -> str:
    return f"""# ILYRA FEN - LYREN MOSS v673-v7 EXACT-FINAL CANDIDATE -> SOLO v673-v8 ACTIVATION - PREPARED NOT SENT

Dear Ilyra,

This committed document is a sanitized activation candidate only. At commit time it is `PREPARED_NOT_SENT`; `sent_by_lyren_moss` is false. It cannot prove a later Codex task acknowledgement, and it does not authorize any historical delivery claim. Only after Lyren's exact final is committed, pushed, clean, zero-divergent, fresh-live equal, and owner-scoped canonical-validated once may Lyren freshly reread Hamish's newest live authority, the current roster/auth state, the exact-title target, duplicate/pause/privacy/evidence/safety gates, and attempt one existing-task send. Never resend merely for clearer acknowledgement.

{IDENTITY_BOUNDARY}

{AUTHORITY_BOUNDARY}

## Authoritative lifecycle anchors

- Branch: `{BRANCH}`
- Immutable Vesper v673-v6 final and Lyren source: `{SOURCE_FINAL}`
- Frozen planning-only Lyren x1: `{X1_COMMIT}`
- Immutable Lyren x2 evidence: `{EVIDENCE_COMMIT}`
- Exact Lyren final: resolve from this branch only at the acknowledged live delivery gate; do not infer it from this pre-delivery candidate.
- Committed activation candidate: `docs/lyren-moss/v673-v7/handoffs/ilyra-fen-v673-v8-activation-candidate.md`
- External canonical receipt: resolve from Lyren's one exclusive terminal receipt only after success; it is not committed here.
- Prospective exact-title task: `Ilyra Fen`.

Source to the eventual exact final is designed as exactly three new direct single-parent Lyren commits and zero merges: planning-only x1, immutable x2 evidence, and additive final closeout. X1 is the direct child of Vesper final, evidence is the direct child of x1, and final must be the direct child of evidence. The exact final and remote equality assertions remain pending in this committed candidate until live terminal verification.

## Bounded evidence

Forty genuinely new Lyren proposals extend the declared chain from 6,470 to 6,510 in the bounded accessible comparison. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Twenty inherited Vesper contracts were revalidated at zero current novelty and zero automatic completion credit. Thirty-six invented positive controls passed. All 160 preregistered invalid mutations executed, were rejected, remain retained, and earn zero completion credit.

Sixty safe-now tasks and thirty bounded candidate analyses were executed within their declared dispositions. Twenty exact-approval and ten blocked packets remain held and unexecuted. Twenty repo-local portable skill cards, ten declarative runner cards, and sixty additive CLEAN/FIX/REFINE reviews were built, tested, and used only as bounded documentation evidence. Ten successor skill, ten successor runner, thirty successor refinement, and exactly one successor-practice recommendation remain recommendations at zero Ilyra completion credit.

The synthetic practice was historical punched-paper telegraph documentation and provenance assurance. The three learning lenses were communications-history collections registrar, paper-tape conservation documentation analyst, and software evidence librarian. The one successor practice recommendation is synthetic historical loom pattern-chain documentation and provenance assurance. No real telegram, message content, person, station, device, collection, measurement, credential, key, right, legal or cultural decision, Maori-authority act, deployment, adapter action, or external record was used.

Three tools were dependency-justified, resolved from official PyPI metadata, downloaded with five dependencies, hash-verified across all eight wheels, installed in one D-isolated phase environment, smoke-tested, and used: rfc8785 0.1.4, jsonschema 4.26.0, and networkx 3.6.1. Shared Python and npm prefixes were not mutated. This is local tool evidence, not supply-chain certification, exhaustive security, an external audit, or independent reproduction.

## Preserved truth

- effective negatives: {counts['effective_negatives']}
- Method Flow methods: {counts['effective_methods']}
- retained failed witnesses: {counts['retained_failed_witnesses']}
- bounded passing witnesses: {counts['bounded_passing_witnesses']}
- open gaps: {counts['open_gaps']}
- exact gates: {counts['exact_gates']}
- terminal verdict: `NOT_READY_FOR_STAGE_20`

Every operational failure and bounded recovery remains explicit. Recovery erased no failure. Same-owner local software and documentation checks under shared infrastructure are not independent reproduction, a complete repository suite, an external audit, production certification, exhaustive security, or complete privacy/accessibility assurance.

GMUT remains a typed scalar-tensor/EFT research-model family without empirical confirmation, final physics, Theory-of-Everything proof, or canon. THOS remains proxy-only without governed preregistered blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys/proofs, live lifecycle, interoperability, security review, recovery evidence, trust governance, and affected-party oversight. CBR work remains a synthetic rights-and-remedy representation without legal, cultural, affected-party, or Maori authority.

## Ilyra's solo v673-v8 lane

If this candidate is later delivered through one acknowledged exact-title task send, read it completely through EOF before mutation, then reread every current guidance and schema it names. Reverify the exact Lyren branch, source, x1, evidence, final, direct ancestry, zero merges, exact manifests, content seal, clean state, typed zero divergence, tracking/upstream equality, fresh live remote equality, and the exclusive external canonical receipt. Do not replay Lyren's successful canonical aggregate or claim inherited evidence as Ilyra novelty, completion credit, external audit, or independent reproduction.

Work solo in one fresh additive Ilyra-owned D-first sparse branch/worktree from the exact Lyren final. Keep Lyren, Vesper, every sibling/shared/user lane, and every standby record read-only and recoverable. Preserve strict planning-only x1 before x2, the 2,000-file guard, the current commit ceiling, family-current compatibility, exact Git-blob manifests, five-class privacy boundaries, only the four core outcome labels, every retained failure/gap/gate, and one-attributable-canonical/no-success-replay discipline. Do not manufacture unsafe work to satisfy a count.

Hamish's current live sequential-continuation authority extends through v675-v8 but remains subject to his right to pause, rename, redirect, or stop. Do not infer future authority from this file alone; reread the newest live instruction at your own terminal gate. Under the present cycle, Ilyra v673-v8's prospective next exact-title owner is `Auren Lark` for v674-v1. Do not precontact Auren during execution. At Ilyra's terminal gate, freshly resolve and immediately reread that unique existing task and send at most once only if every live route condition permits. Never create, fork, substitute, contact Tavian, or use a standby endpoint.

## Delivery state

`prepared_by_lyren_moss: true`

`prepared_not_sent: true`

`sent_by_lyren_moss: false`

No committed file may project a later acknowledgement backward into this preparation state.

With care, inspectability, reversibility, retained-negative discipline, and strict evidence boundaries - Lyren Moss.
"""


def build() -> None:
    if run_git("rev-parse", "HEAD").decode("utf-8").strip() != EVIDENCE_COMMIT:
        raise RuntimeError("closeout must start from immutable evidence commit")
    status = run_git("status", "--porcelain=v1").decode("utf-8").splitlines()
    allowed_untracked = {
        "?? docs/lyren-moss/v673-v7/closeout/",
        "?? docs/lyren-moss/v673-v7/handoffs/",
        "?? scripts/build_ghc_family_lyren_moss_v673_v7_closeout.py",
        "?? scripts/validate_ghc_family_lyren_moss_v673_v7_final.py",
        "?? tests/test_ghc_family_lyren_moss_v673_v7_final.py",
    }
    unexpected_status = [line for line in status if line not in allowed_untracked]
    if unexpected_status:
        raise RuntimeError(f"closeout build requires a clean evidence anchor plus declared new code only: {unexpected_status}")
    counts = exact_counts()
    proposal_results = read_json(X2 / "proposal-results.json")
    mutations = read_json(X2 / "mutation-register.json")
    tools = read_json(X2 / "toolchain-receipt.json")

    write_json(
        CLOSEOUT / "method-flow-closeout.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "method_count": len(CLOSEOUT_METHODS),
            "methods": [
                {
                    **row,
                    "state": "preferred",
                    "passing_witness": row["recovery"],
                    "retained_negative_id": f"NEG-{row['method_id']}",
                    "independent_reproduction": False,
                }
                for row in CLOSEOUT_METHODS
            ],
            "boundary": "Each closeout recovery preserves its failed witness and adds no empirical, professional, authority, independent, or Stage 20 credit.",
        },
    )

    write_json(
        CLOSEOUT / "terminal-summary.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "exact_final_state": "PENDING_THIS_ADDITIVE_CLOSEOUT_COMMIT",
            "proposal_chain": 6510,
            "outcome_counts": proposal_results["outcome_counts"],
            "positive_controls": 36,
            "invalid_mutations_executed_rejected_retained": mutations["rejected_count"],
            **counts,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "same_owner_not_independent_reproduction": True,
            "identity_boundary": IDENTITY_BOUNDARY,
            "authority_boundary": AUTHORITY_BOUNDARY,
        },
    )
    write_json(
        CLOSEOUT / "lifecycle.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "branch": BRANCH,
            "source": SOURCE_FINAL,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "final": "SELF_COMMIT_PENDING",
            "required_shape": "source -> x1 -> evidence -> final",
            "new_commit_count_at_final": 3,
            "merge_count_at_final": 0,
            "one_parent_each": True,
            "x1_before_x2": True,
            "history_rewrite": False,
        },
    )
    write_json(
        CLOSEOUT / "route-state.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "prospective_exact_title": "Ilyra Fen",
            "prospective_phase": "v673-v8",
            "prospective_ilyra_next_title": "Auren Lark",
            "prospective_ilyra_next_phase": "v674-v1",
            "precontact_performed": False,
            "send_attempts": 0,
            "sent_by_lyren_moss": False,
            "tavian_state": "ON_STANDBY",
            "task_or_fork_created": False,
            "required_live_gates": [
                "exact final clean and pushed",
                "typed zero divergence and fresh four-way equality",
                "one successful exclusive owner-scoped canonical aggregate",
                "fresh newest Hamish authority and roster/auth reread",
                "unique exact-title resolution and immediate target reread",
                "duplicate, pause, redirect, usage, privacy, evidence, and safety guards",
                "one normal non-error existing-task acknowledgement",
            ],
        },
    )
    write_json(
        CLOSEOUT / "canonical-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "state": "NOT_INVOKED_PRE_FINAL",
            "expected_status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "exclusive_receipt_required": True,
            "one_invocation": True,
            "no_replay_after_success": True,
            "selected_tests": [
                "tests/test_ghc_family_lyren_moss_v673_v7_x2.py",
                "tests/test_ghc_family_lyren_moss_v673_v7_final.py",
            ],
            "x1_validation": "exact immutable x1 Git-blob manifest replay; the precommit x1 test was already sealed",
            "complete_repository_suite": False,
            "external_audit": False,
            "independent_reproduction": False,
        },
    )
    write_json(
        CLOSEOUT / "final-safe-task-state.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "safe_task_59": {"state": "represented_pending_exact_final", "outcome": "represented", "requirement": "fresh exact-final remote equality"},
            "safe_task_60": {"state": "prepared_not_sent", "outcome": "represented", "requirement": "one acknowledged exact-title Ilyra send after terminal gate"},
            "external_actions": 0,
            "completion_credit_for_pending_terminal_events": 0,
        },
    )
    write_json(
        CLOSEOUT / "tool-closeout.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "wheel_count": tools["wheel_count"],
            "installed_versions": {key: tools["installed_versions"][key] for key in ["rfc8785", "jsonschema", "networkx"]},
            "all_wheel_hashes_verified": all(row["verified"] for row in tools["wheels"]),
            "shared_prefix_mutated": tools["shared_python_or_npm_prefix_mutated"],
            "environment_disposition": "retained_on_D_for_exact_final_validation_and_recoverable_audit",
            "boundary": tools["boundary"],
        },
    )
    write_text(CLOSEOUT / "family-index-terminal-overlay.md", f"""# Lyren Moss v673-v7 terminal overlay

- source: `{SOURCE_FINAL}`
- frozen x1: `{X1_COMMIT}`
- immutable evidence: `{EVIDENCE_COMMIT}`
- exact final: the self commit containing this additive overlay; resolve from `{BRANCH}` at the live terminal gate
- outcome: `28 completed / 8 represented / 2 open_gap / 2 exact_gate`
- proposal chain: `6,510`
- effective negatives: `{counts['effective_negatives']}`
- effective methods: `{counts['effective_methods']}`
- open gaps: `{counts['open_gaps']}`
- exact gates: `{counts['exact_gates']}`
- terminal verdict: `NOT_READY_FOR_STAGE_20`
- route: `Ilyra Fen v673-v8`, prepared not sent

This is an additive terminal overlay and does not rewrite the immutable planning-only index reference. {IDENTITY_BOUNDARY} {AUTHORITY_BOUNDARY}
""")
    write_text(HANDOFF, build_baton(counts))
    write_json(
        CLOSEOUT / "build-receipt.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "mode": "additive_terminal_closeout_candidate",
            "files_written": sorted(str(path.relative_to(ROOT)).replace("\\", "/") for path in [*CLOSEOUT.rglob("*"), HANDOFF] if path.is_file()),
            "x1_or_x2_mutation": False,
            "successor_contact": False,
            "sent_by_lyren_moss": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def staged_paths() -> list[str]:
    return [line for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMRT").decode("utf-8").splitlines() if line]


def staged_blob(path: str) -> bytes:
    return run_git("show", f":{path}")


def privacy_findings(paths: list[str]) -> list[dict[str, str]]:
    patterns = {
        "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "raw_task_or_thread_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
        "credential_assignment": re.compile(r"(?i)(?:password|secret|token|api[_-]?key)\s*[:=]\s*['\"][^'\"]+['\"]"),
        "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        "international_phone_like_number": re.compile(r"(?<!\w)\+\d[\d ()-]{7,}\d(?!\w)"),
    }
    findings = []
    for path in paths:
        if not path.startswith("docs/lyren-moss/v673-v7/"):
            continue
        text = staged_blob(path).decode("utf-8", "replace")
        for category, pattern in patterns.items():
            if pattern.search(text):
                findings.append({"path": path, "class": category})
    return findings


def security_findings(paths: list[str]) -> list[dict[str, Any]]:
    findings = []
    for path in paths:
        if not path.endswith(".py"):
            continue
        tree = ast.parse(staged_blob(path).decode("utf-8"), filename=path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
            if name in {"eval", "exec", "system"}:
                findings.append({"path": path, "line": node.lineno, "call": name})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append({"path": path, "line": node.lineno, "call": "shell=True"})
    return findings


def finalize_staged() -> None:
    paths = staged_paths()
    allowed = (
        "docs/lyren-moss/v673-v7/closeout/",
        "docs/lyren-moss/v673-v7/handoffs/",
        "scripts/build_ghc_family_lyren_moss_v673_v7_closeout.py",
        "scripts/validate_ghc_family_lyren_moss_v673_v7_final.py",
        "tests/test_ghc_family_lyren_moss_v673_v7_final.py",
    )
    unexpected = [path for path in paths if not path.startswith(allowed)]
    immutable = [path for path in paths if path.startswith(("docs/lyren-moss/v673-v7/x1/", "docs/lyren-moss/v673-v7/x2/"))]
    deleted = run_git("diff", "--cached", "--name-only", "--diff-filter=D").decode("utf-8").splitlines()
    privacy = privacy_findings(paths)
    security = security_findings(paths)
    write_json(
        VALIDATION / "final-staged-review.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "evidence_commit": EVIDENCE_COMMIT,
            "staged_path_count_before_review_receipts": len(paths),
            "staged_paths": paths,
            "unexpected_paths": unexpected,
            "immutable_x1_x2_paths": immutable,
            "deletions": deleted,
            "passed": not unexpected and not immutable and not deleted,
        },
    )
    write_json(
        VALIDATION / "final-staged-privacy.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "classes": list({"private_absolute_path": 0, "raw_task_or_thread_uuid": 0, "credential_assignment": 0, "email_address": 0, "international_phone_like_number": 0}),
            "confirmed_hits": privacy,
            "confirmed_hit_count": len(privacy),
            "passed": not privacy,
            "complete_privacy_assurance": False,
        },
    )
    write_json(
        VALIDATION / "final-staged-security.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "python_files": [path for path in paths if path.endswith(".py")],
            "bounded_ast_findings": security,
            "bounded_ast_finding_count": len(security),
            "passed": not security,
            "exhaustive_security": False,
        },
    )
    if unexpected or immutable or deleted or privacy or security:
        raise RuntimeError("final staged review failed")


def index_blob(path: str) -> bytes:
    return normalized(staged_blob(path))


def owner_paths_from_index() -> list[str]:
    paths = run_git("ls-files").decode("utf-8").splitlines()
    return sorted(
        path for path in paths
        if path.startswith("docs/lyren-moss/v673-v7/")
        or path == "ghc-family-index/references/v673-v7-lyren-moss.md"
        or path.startswith("scripts/build_ghc_family_lyren_moss_v673_v7_")
        or path == "scripts/validate_ghc_family_lyren_moss_v673_v7_final.py"
        or path.startswith("tests/test_ghc_family_lyren_moss_v673_v7_")
    )


def build_manifests() -> None:
    final_delta_path = "docs/lyren-moss/v673-v7/validation/final-delta-manifest.json"
    owner_manifest_path = "docs/lyren-moss/v673-v7/validation/final-owner-manifest.json"
    seal_path = "docs/lyren-moss/v673-v7/validation/final-content-seal.json"
    exclusions = {final_delta_path, owner_manifest_path, seal_path}
    delta = sorted(path for path in staged_paths() if path not in exclusions)
    delta_entries = [
        {"path": path, "bytes": len(index_blob(path)), "sha256_normalized_lf": sha256(index_blob(path))}
        for path in delta
    ]
    owner_paths = [path for path in owner_paths_from_index() if path not in {owner_manifest_path, seal_path}]
    owner_entries = [
        {"path": path, "bytes": len(index_blob(path)), "sha256_normalized_lf": sha256(index_blob(path))}
        for path in owner_paths
    ]
    write_json(
        VALIDATION / "final-delta-manifest.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "evidence_commit": EVIDENCE_COMMIT,
            "hash_domain": "normalized_lf_exact_git_index_blob",
            "entry_count": len(delta_entries),
            "entries": delta_entries,
            "self_exclusions": sorted(exclusions),
        },
    )
    write_json(
        VALIDATION / "final-owner-manifest.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "hash_domain": "normalized_lf_exact_git_index_blob",
            "entry_count": len(owner_entries),
            "entries": owner_entries,
            "self_exclusions": [owner_manifest_path, seal_path],
            "file_ceiling": 2000,
            "within_file_ceiling": len(owner_entries) + 2 < 2000,
        },
    )


def build_content_seal() -> None:
    paths = [
        "docs/lyren-moss/v673-v7/validation/x1-manifest.json",
        "docs/lyren-moss/v673-v7/validation/x2-evidence-manifest.json",
        "docs/lyren-moss/v673-v7/validation/final-delta-manifest.json",
        "docs/lyren-moss/v673-v7/validation/final-owner-manifest.json",
        "docs/lyren-moss/v673-v7/validation/final-staged-review.json",
        "docs/lyren-moss/v673-v7/validation/final-staged-privacy.json",
        "docs/lyren-moss/v673-v7/validation/final-staged-security.json",
        "docs/lyren-moss/v673-v7/x2/proposal-results.json",
        "docs/lyren-moss/v673-v7/x2/mutation-register.json",
        "docs/lyren-moss/v673-v7/x2/toolchain-receipt.json",
        "docs/lyren-moss/v673-v7/x2/retained-negatives.json",
        "docs/lyren-moss/v673-v7/closeout/terminal-summary.json",
        "docs/lyren-moss/v673-v7/closeout/lifecycle.json",
        "docs/lyren-moss/v673-v7/closeout/route-state.json",
        "docs/lyren-moss/v673-v7/handoffs/ilyra-fen-v673-v8-activation-candidate.md",
    ]
    entries = []
    for path in paths:
        data = index_blob(path)
        entries.append({"path": path, "bytes": len(data), "sha256_normalized_lf": sha256(data)})
    write_json(
        VALIDATION / "final-content-seal.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "hash_domain": "normalized_lf_exact_git_index_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": ["docs/lyren-moss/v673-v7/validation/final-content-seal.json"],
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["build", "finalize-staged", "manifests", "content-seal"], nargs="?", default="build")
    args = parser.parse_args()
    if args.mode == "build":
        build()
    elif args.mode == "finalize-staged":
        finalize_staged()
    elif args.mode == "manifests":
        build_manifests()
    else:
        build_content_seal()


if __name__ == "__main__":
    main()
