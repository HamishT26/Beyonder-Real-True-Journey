#!/usr/bin/env python3
"""Build the additive Elowen Cairn v676-v6 exact-final candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Elowen Cairn"
OWNER_SLUG = "elowen-cairn"
PHASE = "v676-v6"
BRANCH = "codex/GHC-Family/elowen-cairn-v676-v6-full-tools"
SOURCE = "56b4e82909b3d7197b817a2415da592f8fc7df6e"
X1 = "0943c5da5d4c1aced1ed9a29aca2d18de1c16b26"
EVIDENCE = "c32fde8ba3aa9518e65f212b8a87d1a108dbc69a"

POST_EVIDENCE_METHODS: list[dict[str, Any]] = [
    {
        "method_id": "EC6766-CLOSE-N001",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first evidence fresh-live equality wrapper applied array indexing before materializing and splitting the remote line, projected the remote SHA as the single character c, and therefore earned zero fresh-live equality credit.",
        "recovered_by": "EC6766-CLOSE-P001",
        "repository_state_change": False,
        "evidence_commit_rewritten": False,
    },
    {
        "method_id": "EC6766-CLOSE-P001",
        "status": "bounded_pass",
        "truth": True,
        "description": "The isolated failed scalar was rerun from one materialized git ls-remote line; its two fields parsed exactly and the full fresh-live SHA equalled evidence. Local, upstream, tracking, and 0/0 results from the first wrapper were not replayed.",
        "failed_witness_preserved": "EC6766-CLOSE-N001",
        "x2_replayed": False,
    },
    {
        "method_id": "EC6766-CLOSE-N002",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first closeout read assumed an evidence directory and semantic-novelty filename that do not exist in this phase, so the bounded projection failed and earned zero evidence-read credit.",
        "recovered_by": "EC6766-CLOSE-P002",
        "repository_state_change": False,
        "evidence_checks_replayed_for_credit": False,
    },
    {
        "method_id": "EC6766-CLOSE-P002",
        "status": "bounded_pass",
        "truth": True,
        "description": "A filename-first rg --files discovery recovered the exact x2 and semantic-neighbor paths, after which only the requested immutable JSON properties were read.",
        "failed_witness_preserved": "EC6766-CLOSE-N002",
    },
    {
        "method_id": "EC6766-CLOSE-N003",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first combined Git-delta and file-count projection returned no attributable output, so it earned zero count credit.",
        "recovered_by": "EC6766-CLOSE-P003",
        "repository_state_change": False,
        "repository_state_change": False,
    },
    {
        "method_id": "EC6766-CLOSE-P003",
        "status": "bounded_pass",
        "truth": True,
        "description": "The recovery materialized the exact x1-to-evidence path list once, projected each suffix count independently, and reported 542 paths: 486 JSON, 14 Python, 21 Markdown, and one HTML file.",
        "failed_witness_preserved": "EC6766-CLOSE-N003",
    },
    {
        "method_id": "EC6766-CLOSE-N004",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first full-file validator replacement patch targeted the same path as both a deletion and an addition; the patch engine atomically rejected it before changing any repository byte.",
        "recovered_by": "EC6766-CLOSE-P004",
        "repository_state_change": False,
    },
    {
        "method_id": "EC6766-CLOSE-P004",
        "status": "bounded_pass",
        "truth": True,
        "description": "Two explicit apply-patch operations then removed the stale phase-locked validator and added the v676-v6 lifecycle-correct validator without editing any inherited commit.",
        "failed_witness_preserved": "EC6766-CLOSE-N004",
    },
    {
        "method_id": "EC6766-CLOSE-N005",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first short-status probe returned no attributable text despite four expected untracked closeout files, so it earned zero worktree-state credit.",
        "recovered_by": "EC6766-CLOSE-P005",
        "repository_state_change": False,
    },
    {
        "method_id": "EC6766-CLOSE-P005",
        "status": "bounded_pass",
        "truth": True,
        "description": "A bounded literal four-path existence, index-membership, ignore-rule, and all-untracked porcelain audit proved all four files existed, were untracked, were not ignored, and were the only worktree rows.",
        "failed_witness_preserved": "EC6766-CLOSE-N005",
    },
    {
        "method_id": "EC6766-CLOSE-N006",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first 22-path staging wrapper returned no attributable output; an immediate index projection reported zero staged paths before persisted-state inspection later showed 21 staged entries and one remaining untracked manifest builder.",
        "recovered_by": "EC6766-CLOSE-P006",
        "head_changed": False,
        "commit_created": False,
    },
    {
        "method_id": "EC6766-CLOSE-P006",
        "status": "bounded_pass",
        "truth": True,
        "description": "The recovery compared HEAD, index membership, file existence, and full porcelain state, preserved the 21 staged entries, and narrowed the remaining mutation to the one exact untracked manifest-builder path plus regenerated tracked closeout blobs.",
        "failed_witness_preserved": "EC6766-CLOSE-N006",
    },
    {
        "method_id": "EC6766-CLOSE-N007",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The exact 22-path add rejected the lone final-manifest builder because that owner file sits outside the active sparse definition; the rejection changed no commit and left the other 21 entries staged.",
        "recovered_by": "EC6766-CLOSE-P007",
        "head_changed": False,
    },
    {
        "method_id": "EC6766-CLOSE-P007",
        "status": "bounded_pass",
        "truth": True,
        "description": "Persisted-state inspection proved 21 staged, zero unstaged, and one untracked path; git add --sparse then staged only the exact final-manifest builder without changing sparse rules.",
        "failed_witness_preserved": "EC6766-CLOSE-N007",
    },
    {
        "method_id": "EC6766-CLOSE-N008",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first final-manifest builder remained stalled with one live git cat-file child, unchanged CPU, and no manifest outputs after multiple bounded observations; it earned zero manifest credit.",
        "recovered_by": "EC6766-CLOSE-P008",
        "manifest_entries_credited": 0,
    },
    {
        "method_id": "EC6766-CLOSE-P008",
        "status": "bounded_pass",
        "truth": True,
        "description": "The exact helper pair was stopped, the batch-reader close sequence was changed to drain stdout and stderr through communicate after stdin closure, and only the failed manifest dependency was authorized for one rerun.",
        "failed_witness_preserved": "EC6766-CLOSE-N008",
    },
    {
        "method_id": "EC6766-CLOSE-N009",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first manifest-output staging attempt assumed the yielded builder had completed and failed because all three expected files were absent.",
        "recovered_by": "EC6766-CLOSE-P009",
        "repository_state_change": False,
    },
    {
        "method_id": "EC6766-CLOSE-P009",
        "status": "bounded_pass",
        "truth": True,
        "description": "The recovery made file existence and process completion explicit prerequisites before any later manifest-output staging action.",
        "failed_witness_preserved": "EC6766-CLOSE-N009",
    },
    {
        "method_id": "EC6766-CLOSE-N010",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first thirty-second Wait-Process wrapper was itself cut off at the tool yield boundary before printing its post-wait state.",
        "recovered_by": "EC6766-CLOSE-P010",
        "repository_state_change": False,
    },
    {
        "method_id": "EC6766-CLOSE-P010",
        "status": "bounded_pass",
        "truth": True,
        "description": "Immediate scalar process and child inspection established the unchanged Python and git cat-file pair, after which only those verified helper process identifiers were stopped.",
        "failed_witness_preserved": "EC6766-CLOSE-N010",
    },
    {
        "method_id": "EC6766-CLOSE-N011",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The failed 34-test precommit aggregate ran the x1 no-x2 assertion against the final working tree; that lifecycle-mismatched assertion failed while its passing peers received no aggregate success credit.",
        "recovered_by": "EC6766-CLOSE-P011",
        "aggregate_success_credit": 0,
    },
    {
        "method_id": "EC6766-CLOSE-P011",
        "status": "bounded_pass",
        "truth": True,
        "description": "A commit-local Git-tree predicate at exact x1 checked 19 owner documents, 1,112 scripts, and 227 tests; it found no x2-class owner path and zero privacy hits without replaying any passing test.",
        "failed_witness_preserved": "EC6766-CLOSE-N011",
    },
    {
        "method_id": "EC6766-CLOSE-N012",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The same failed precommit aggregate ran the evidence no-final assertion against the final working tree; that lifecycle-mismatched assertion failed and remained zero credit.",
        "recovered_by": "EC6766-CLOSE-P012",
        "aggregate_success_credit": 0,
    },
    {
        "method_id": "EC6766-CLOSE-P012",
        "status": "bounded_pass",
        "truth": True,
        "description": "A commit-local Git-tree predicate at exact evidence checked 547 owner documents and 1,125 scripts; it found no final, closeout, handoff, or final-script class and zero privacy hits without replaying passing tests.",
        "failed_witness_preserved": "EC6766-CLOSE-N012",
    },
    {
        "method_id": "EC6766-CLOSE-N013",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first immutable-archive recovery stalled in git archive with a zero-byte x1 archive and no test execution, so it earned zero recovery credit.",
        "recovered_by": "EC6766-CLOSE-P013",
        "test_credit": 0,
    },
    {
        "method_id": "EC6766-CLOSE-P013",
        "status": "bounded_pass",
        "truth": True,
        "description": "The exact archive process chain was stopped and replaced by read-only commit-local path and grep predicates that required no archive and no second worktree.",
        "failed_witness_preserved": "EC6766-CLOSE-N013",
    },
    {
        "method_id": "EC6766-CLOSE-N014",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first in-memory recovery enumerated each entire repository tree and remained unproductive; it was stopped before producing a verdict.",
        "recovered_by": "EC6766-CLOSE-P014",
        "test_credit": 0,
    },
    {
        "method_id": "EC6766-CLOSE-P014",
        "status": "bounded_pass",
        "truth": True,
        "description": "The recovery narrowed enumeration to the Elowen phase plus bounded scripts and tests directories, with commit-local filtering only.",
        "failed_witness_preserved": "EC6766-CLOSE-N014",
    },
    {
        "method_id": "EC6766-CLOSE-N015",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first narrowed Git-tree wrapper used unsupported glob pathspec magic and failed to propagate both native errors, producing a false empty-set pass that earned zero credit.",
        "recovered_by": "EC6766-CLOSE-P015",
        "test_credit": 0,
    },
    {
        "method_id": "EC6766-CLOSE-P015",
        "status": "bounded_pass",
        "truth": True,
        "description": "Exact directory pathspecs, local filename filtering, and mandatory native exit checks produced attributable passing x1 and evidence lifecycle predicates.",
        "failed_witness_preserved": "EC6766-CLOSE-N015",
    },
    {
        "method_id": "EC6766-CLOSE-N016",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first combined final-gate projection exceeded its display window while parsing large manifests and returned no attributable output, so it earned zero terminal-gate credit.",
        "recovered_by": "EC6766-CLOSE-P016",
        "repository_state_change": False,
    },
    {
        "method_id": "EC6766-CLOSE-P016",
        "status": "bounded_pass",
        "truth": True,
        "description": "Small scalar Git counts plus bounded exact-key text projections proved 25 staged paths, zero unstaged and untracked paths, 22 final-delta entries, 586 final-owner entries, sixteen adjudicated candidates, zero confirmed hits, exact retained counts, and clean diff hygiene.",
        "failed_witness_preserved": "EC6766-CLOSE-N016",
    },
    {
        "method_id": "EC6766-CLOSE-N017",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first final commit process remained live without output or a new commit while its empty index lock persisted and its Git child accumulated no CPU or I/O across a bounded progress interval; it was interrupted and earned zero commit credit.",
        "recovered_by": "EC6766-CLOSE-P017",
        "commit_created": False,
        "staged_paths_preserved": 25,
    },
    {
        "method_id": "EC6766-CLOSE-P017",
        "status": "bounded_pass",
        "truth": True,
        "description": "Persisted-state inspection proved the head still equalled evidence, all twenty-five intended paths remained staged, no Git process remained, and the only residue was one empty worktree-specific index lock; no duplicate commit was attempted.",
        "failed_witness_preserved": "EC6766-CLOSE-N017",
    },
    {
        "method_id": "EC6766-CLOSE-N018",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first stale-lock cleanup wrapper combined a computed destructive target with inline safety checks and was rejected by host policy before process creation, changing no filesystem or repository state.",
        "recovered_by": "EC6766-CLOSE-P018",
        "repository_state_change": False,
    },
    {
        "method_id": "EC6766-CLOSE-P018",
        "status": "bounded_pass",
        "truth": True,
        "description": "A read-only resolved-Git-directory audit fixed the cleanup scope to the exact empty worktree index lock and reconfirmed that the prior commit processes were absent before any second cleanup method was considered.",
        "failed_witness_preserved": "EC6766-CLOSE-N018",
    },
    {
        "method_id": "EC6766-CLOSE-N019",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "A literal native-shell removal of that exact empty index lock was also rejected by host policy before execution, so it earned zero cleanup credit and left the lock unchanged.",
        "recovered_by": "EC6766-CLOSE-P019",
        "repository_state_change": False,
    },
    {
        "method_id": "EC6766-CLOSE-P019",
        "status": "bounded_pass",
        "truth": True,
        "description": "The repository-safe patch mechanism removed only the verified empty worktree index lock; a read-only follow-up proved the lock absent, the evidence head unchanged, and all twenty-five staged paths preserved.",
        "failed_witness_preserved": "EC6766-CLOSE-N019",
    },
    {
        "method_id": "EC6766-CLOSE-N020",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "A --help probe against the argument-free final-manifest helper entered its full main routine, produced no bounded output, and was interrupted before any manifest write; it earned zero validation or manifest credit.",
        "recovered_by": "EC6766-CLOSE-P020",
        "manifest_entries_credited": 0,
        "repository_state_change": False,
    },
    {
        "method_id": "EC6766-CLOSE-P020",
        "status": "bounded_pass",
        "truth": True,
        "description": "A direct complete source read established that the helper intentionally accepts no arguments and must be invoked only after all exact final inputs are staged; the exploratory process was absent before proceeding.",
        "failed_witness_preserved": "EC6766-CLOSE-N020",
    },
    {
        "method_id": "EC6766-CLOSE-N021",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "A second porcelain commit with preload-index, fsmonitor, untracked-cache, hooks, and signing disabled reproduced the stationary empty-lock condition for more than two minutes and was interrupted with zero commit credit.",
        "recovered_by": "EC6766-CLOSE-P021",
        "commit_created": False,
        "staged_paths_preserved": 25,
    },
    {
        "method_id": "EC6766-CLOSE-P021",
        "status": "bounded_pass",
        "truth": True,
        "description": "Post-interruption state inspection again proved the evidence head unchanged, all twenty-five paths staged, all commit processes absent, and only the exact empty worktree index lock present; the proven repository-safe patch removed that lock before an atomic plumbing commit was considered.",
        "failed_witness_preserved": "EC6766-CLOSE-N021",
        "porcelain_commit_replay_forbidden": True,
    },
    {
        "method_id": "EC6766-CLOSE-N022",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first atomic-plumbing precondition reached git write-tree against the primary worktree index, then reproduced the stationary empty-lock condition and was interrupted before emitting a tree object identifier.",
        "recovered_by": "EC6766-CLOSE-P022",
        "tree_credit": 0,
        "commit_created": False,
    },
    {
        "method_id": "EC6766-CLOSE-P022",
        "status": "bounded_pass",
        "truth": True,
        "description": "Persisted-state inspection proved no tree or commit credit, the evidence head and exact staged set remained intact, and the empty primary-index lock was removed; the recovery selected a disposable D-first index initialized from evidence and populated only from exact staged blob entries.",
        "failed_witness_preserved": "EC6766-CLOSE-N022",
        "primary_index_write_tree_replay_forbidden": True,
    },
    {
        "method_id": "EC6766-CLOSE-N023",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The disposable-index recovery stalled in git read-tree before creating an index and was interrupted; its zero-byte external lock was removed and it earned zero tree or commit credit.",
        "recovered_by": "EC6766-CLOSE-P023",
        "tree_credit": 0,
        "commit_created": False,
    },
    {
        "method_id": "EC6766-CLOSE-P023",
        "status": "bounded_pass",
        "truth": True,
        "description": "Exact process and filesystem inspection proved the disposable read-tree changed no ref or primary index, and the empty external lock was removed before selecting a no-index tree encoder.",
        "failed_witness_preserved": "EC6766-CLOSE-N023",
    },
    {
        "method_id": "EC6766-CLOSE-N024",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first no-index patcher reached git mktree but that Git object-write subprocess remained stationary and was interrupted before returning a tree identifier.",
        "recovered_by": "EC6766-CLOSE-P024",
        "tree_credit": 0,
        "commit_created": False,
    },
    {
        "method_id": "EC6766-CLOSE-P024",
        "status": "bounded_pass",
        "truth": True,
        "description": "A canonical loose-object encoder replaced mktree, wrote Git tree objects atomically, verified every zlib payload and SHA-1, and produced a Git-readable candidate tree whose delta contained exactly the twenty-five staged paths.",
        "failed_witness_preserved": "EC6766-CLOSE-N024",
    },
    {
        "method_id": "EC6766-CLOSE-N025",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "A recursive common-Git-directory lock scan was overbroad and was stopped after reporting healthy D-drive capacity; it earned zero lock-surface credit.",
        "recovered_by": "EC6766-CLOSE-P025",
        "repository_state_change": False,
    },
    {
        "method_id": "EC6766-CLOSE-P025",
        "status": "bounded_pass",
        "truth": True,
        "description": "A bounded top-level common-directory, exact branch-ref, primary-index, and external-index lock check found no competing lock, reconfirmed the evidence head, and avoided recursion.",
        "failed_witness_preserved": "EC6766-CLOSE-N025",
    },
    {
        "method_id": "EC6766-CLOSE-N026",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first direct-tree verification requested a recursive full-tree ls-tree projection and exceeded its bounded window after the exact twenty-five-path delta had already passed; it was stopped with zero blob-parity credit.",
        "recovered_by": "EC6766-CLOSE-P026",
        "blob_parity_credit": 0,
    },
    {
        "method_id": "EC6766-CLOSE-P026",
        "status": "bounded_pass",
        "truth": True,
        "description": "The recovery queried only the twenty-five staged paths from the candidate tree and compared every mode, object kind, and blob OID to the primary staged entries; all twenty-five matched with zero mismatches.",
        "failed_witness_preserved": "EC6766-CLOSE-N026",
    },
]


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.strip() + "\n", encoding="utf-8", newline="\n")


def normalized_sha(path: Path) -> str:
    raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(raw).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    repo = args.repo.resolve()
    if git(repo, "branch", "--show-current") != BRANCH or git(repo, "rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("final builder requires the exact immutable Elowen evidence head")
    allowed = {
        "scripts/build_ghc_family_elowen_cairn_v676_v6_final.py",
        "scripts/ghc_family_elowen_cairn_v676_v6_final_manifest.py",
        "scripts/validate_ghc_family_elowen_cairn_v676_v6_final.py",
        "tests/test_ghc_family_elowen_cairn_v676_v6_final.py",
    }
    status = [line for line in git(repo, "status", "--porcelain=v1").splitlines() if line]
    allowed_doc_prefixes = (
        "docs/elowen-cairn/v676-v6/closeout/",
        "docs/elowen-cairn/v676-v6/final/",
        "docs/elowen-cairn/v676-v6/handoffs/",
        "docs/elowen-cairn/v676-v6/orchestration/",
        "docs/elowen-cairn/v676-v6/validation/final-",
    )
    unexpected = []
    for line in status:
        path = line[3:].replace("\\", "/")
        if path in allowed or path.startswith(allowed_doc_prefixes):
            continue
        unexpected.append(line)
    if unexpected:
        raise SystemExit(f"unexpected pre-final worktree state: {unexpected!r}")

    base = repo / "docs" / OWNER_SLUG / PHASE
    x1 = base / "x1"
    x2 = base / "x2"
    final_dir = base / "final"
    closeout = base / "closeout"
    handoff = base / "handoffs"
    orchestration = base / "orchestration"

    freeze = json.loads((x1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    source_ledger = json.loads((x1 / "official-source-ledger.json").read_text(encoding="utf-8"))
    semantic = json.loads((x1 / "semantic-neighbor-audit.json").read_text(encoding="utf-8"))
    outcomes = json.loads((x2 / "proposal-outcomes.json").read_text(encoding="utf-8"))
    evidence_flow = json.loads((x2 / "method-flow" / "ledger.json").read_text(encoding="utf-8"))
    portfolio = json.loads((x2 / "portfolio" / "execution-summary.json").read_text(encoding="utf-8"))
    flow = json.loads(json.dumps(evidence_flow))
    existing_ids = {row["method_id"] for row in flow["methods"]}
    if any(row["method_id"] in existing_ids for row in POST_EVIDENCE_METHODS):
        raise SystemExit("post-evidence Method Flow overlay already present")
    flow["methods"].extend(POST_EVIDENCE_METHODS)
    failed = sum(row["truth"] is False for row in flow["methods"])
    passing = sum(row["truth"] is True for row in flow["methods"])
    if (len(flow["methods"]), failed, passing) != (654, 207, 447):
        raise SystemExit("unexpected final Method Flow partition")
    overlay = {
        "effective_negatives": 42648,
        "effective_methods": 33772,
        "retained_failed_witnesses": 14309,
        "bounded_passing_witnesses": 20152,
        "open_gaps": 359,
        "exact_gates": 351,
    }
    flow["phase_ledger_counts"] = {"methods": 654, "failed": 207, "passing": 447}
    flow["current_overlay"] = overlay
    flow["post_evidence_failed_witnesses"] = 26
    flow["post_evidence_bounded_recoveries"] = 26
    flow["failure_erasure_forbidden"] = True

    dump(final_dir / "method-flow-ledger.json", flow)
    dump(
        final_dir / "phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "expected_final": "bound by the ensuing exact commit and one external canonical receipt",
            "declared_proposal_chain": 7630,
            "new_elowen_proposals": 40,
            "inherited_reviews_zero_credit": 20,
            "core_outcomes": outcomes["outcome_counts"],
            "positive_controls": 40,
            "preregistered_mutations_executed_rejected": 160,
            "phase_local_skills_built_validated_smoked": 20,
            "family_current_runners_used": 10,
            "safe_now_tasks_completed": portfolio["safe_now_completed"],
            "candidate_tasks_completed_without_core_promotion": portfolio["candidate_completed_without_core_promotion"],
            "clean_fix_refine_tasks_completed": portfolio["clean_fix_refine_completed"],
            "exact_approval_packets_unexecuted": portfolio["exact_approval_unexecuted"],
            "blocked_packets_unexecuted": portfolio["blocked_unexecuted"],
            "current_overlay": overlay,
            "real_world_rows": 0,
            "participants": 0,
            "external_actions": 0,
            "production_identity_events": 0,
            "authority_actions": 0,
            "full_repository_suite_run": False,
            "independent_reproduction_claimed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    dump(
        final_dir / "source-and-proposal-ledger.json",
        {
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "declared_chain_before": 7590,
            "declared_chain_after": 7630,
            "reachable_semantic_audit": semantic,
            "universal_novelty_proof_claimed": False,
            "official_primary_sources": source_ledger["sources"],
            "source_boundary": source_ledger["source_boundary"],
            "proposals": freeze["proposals"],
            "outcomes": outcomes["outcomes"],
        },
    )
    dump(
        final_dir / "retained-negative-register.json",
        {
            "activation_effective_negatives": 42441,
            "new_elowen_effective_negatives": 207,
            "current_effective_negatives": 42648,
            "phase_failed_witness_count": 207,
            "phase_failed_witnesses": [row for row in flow["methods"] if row["truth"] is False],
            "failed_witnesses_converted_to_pass": 0,
            "retention_rule": "Every false witness remains false; a recovery is a separately identified bounded passing method.",
        },
    )
    dump(final_dir / "open-gap-register.json", json.loads((x2 / "open-gap-register.json").read_text(encoding="utf-8")))
    dump(final_dir / "exact-gate-register.json", json.loads((x2 / "exact-gate-register.json").read_text(encoding="utf-8")))
    dump(
        final_dir / "complete-incomplete-ledger.json",
        {
            "complete_bounded": [
                "forty planning-only proposal contracts frozen after reachable semantic-neighbor review",
                "forty zero-row positive structural controls accepted",
                "160 preregistered invalid mutations executed, rejected, and retained",
                "twenty phase-local skills quick-validated and smoke-used without global installation",
                "ten family-current runners accepted a positive fixture and rejected an invalid fixture",
                "sixty safe-now, thirty bounded candidate, and sixty additive CLEAN/FIX/REFINE tasks completed without broader promotion",
                "x1 and evidence committed, pushed, clean, 0/0 divergent, and fresh four-way equal",
            ],
            "represented_only": [
                "real typewriter professional, mechanical, electrical, or material-safety review and affected-user accessibility evaluation",
                "live interoperability, status, revocation, recovery, security, and privacy review",
                "real practitioner workload, inspection, repair, correction, release, and remedy outcomes",
            ],
            "open": [
                "real typewriter observations and measurements with traceable instruments, uncertainty treatment, and preregistered analysis",
                "independent professional and affected-user review with governed outcome evidence",
            ],
            "exact_gated": [
                "professional mechanical, electrical, material-safety, operation, disassembly, repair, treatment, and release decisions",
                "ownership, authorship, copyright, privacy, cultural, traditional-knowledge, taonga, mātauranga, Māori-data-governance, wording, and Māori-authority decisions",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    dump(
        final_dir / "threat-model.json",
        {
            "protected_assets": ["immutable source", "planning-only x1", "x2 evidence", "failure truth", "privacy boundary", "authority vacancies", "terminal route"],
            "bounded_controls": ["four-label vocabulary", "normalized-LF Git-blob manifests", "candidate adjudication", "Method Flow retention", "exclusive canonical latch", "terminal route hold"],
            "residual_threats": [
                "synthetic evidence may be overread as real evidence",
                "scanner definitions may be mistaken for payload disclosures",
                "citations may be mistaken for observations or endorsements",
                "same-owner validation may be mistaken for independent reproduction",
                "task topology may be mistaken for identity continuity or authority",
            ],
            "closed_bounded_threats": ["x1 and x2 lifecycle mixing", "unknown outcome labels", "silent invalid-mutation acceptance", "global installation of phase-local skills"],
        },
    )
    dump(
        final_dir / "portfolio-truth.json",
        {
            **portfolio,
            "successor_recommendations_zero_credit": 50,
            "core_outcome_counts_unchanged_by_portfolio_status": True,
        },
    )
    dump(
        final_dir / "post-evidence-overlay.json",
        {
            "failed_witnesses": [row for row in POST_EVIDENCE_METHODS if row["truth"] is False],
            "bounded_recoveries": [row for row in POST_EVIDENCE_METHODS if row["truth"] is True],
            "evidence_commit_mutated": False,
            "failure_erasure": False,
        },
    )
    text(
        final_dir / "final-integrated-overview.md",
        f"""
# {OWNER} {PHASE} — final integrated overview

## Outcome first

Elowen Cairn v676-v6 is a bounded, same-owner, zero-row software and documentation phase rooted directly at Tamar Vey's corrected immutable final `{SOURCE}`. Planning-only x1 is `{X1}` and immutable x2 evidence is `{EVIDENCE}`. The exact final is intentionally supplied only by the ensuing commit and the exclusive external canonical receipt; this precommit document does not invent its future commit identifier. The terminal verdict remains exactly `NOT_READY_FOR_STAGE_20`.

The declared proposal chain advances from 7,590 inherited rows to 7,630 through forty Elowen-owned proposal contracts. Twenty inherited semantic neighbors were reviewed at zero Elowen novelty, execution, or completion credit. The source-tree tribunal inspected 2,624 reachable proposal-bearing JSON blobs and 11,178 raw identifier-title records, reducing them to 3,535 unique identifier-title records. Its explicit limitation remains: no single reachable ledger materializes every declared historic row, so this is bounded semantic-distinctness evidence rather than universal novelty or scientific novelty proof. One initial title reached the unchanged 0.75 quarantine threshold and failed at zero credit. The isolated correction retitled only proposal EC6766-N037, retained the same threshold, and passed with zero selected quarantines, zero exact collisions, zero parse failures, and a maximum selected score of 0.7143.

Core outcomes use only the authorized vocabulary and are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Here, `completed` means only that one frozen owner-local structural contract accepted its wholly synthetic positive fixture and preserved its refusal boundaries. It does not mean a typewriter was observed, identified, measured, opened, powered, operated, adjusted, cleaned, lubricated, disassembled, repaired, treated, or released; a person did not participate; and no professional, identity, rights, legal, cultural, affected-party, or authority decision occurred. `represented` marks a structurally present proxy without real-world validation. `open_gap` marks absent evidence that cannot be manufactured. `exact_gate` marks action reserved to competent and affected authorities.

## Lifecycle and immutable evidence

Strict planning-only x1 before x2 was preserved. X1 contained the forty proposal contracts, four rejecting mutations per proposal, source and gate ledgers, portfolio plans, twenty skill plans, ten runner plans, fifty successor seeds, and Method Flow records—but no x2 implementation, observation, outcome, or completion claim. X1 was tested, reviewed through an exact normalized-LF Git-blob manifest, committed, pushed, made clean, and proven equal across local, upstream, tracking, and a fresh live remote before any x2 file was created.

X2 then executed only the preregistered bounded work. Forty synthetic positive controls passed. All 160 preregistered invalid mutations executed and were rejected; each remains a zero-credit false witness paired with a separate bounded rejection witness. Twenty owner-local skills were initialized with the official skill-creator workflow, customized, read completely through EOF, quick-validated under explicit UTF-8, and accepting-smoke-used without global installation. Ten family-current runners accepted one positive fixture and rejected one invalid fixture. Sixty safe-now tasks, thirty bounded candidate tasks, and sixty CLEAN/FIX/REFINE tasks completed without promotion into core outcomes or real-world claims. Twenty exact-approval packets and ten blocked packets remain visible and unexecuted.

The immutable evidence commit contains 540 exact normalized-LF Git-blob manifest entries plus two declared self-referential exclusions. Its independent staged replay matched all 540 entries, matched the full 542-path staged set, parsed 486 staged JSON documents, checked fourteen staged Python files through AST parsing, found zero manifest failures, found zero confirmed privacy or raw-identifier payload hits, and found no final or closeout path. Evidence is a direct child of x1 and was separately pushed, cleaned, and proven 0/0 divergent and four-way fresh-live equal before closeout began.

## Method Flow and retained negatives

The effective activation baseline—Tamar's corrected repository truth plus its separately retained routing overlay—was 42,441 negatives, 33,118 methods, 14,102 failed witnesses, 19,705 bounded passing witnesses, 357 open gaps, and 349 exact gates. The final Elowen phase ledger contains 654 methods: 207 retained false witnesses and 447 bounded passing witnesses. The resulting overlay is 42,648 negatives, 33,772 methods, 14,309 retained failed witnesses, 20,152 bounded passing witnesses, 359 open gaps, and 351 exact gates.

The 207 phase false witnesses comprise ten startup and x1 operational failures, one x2 operational failure, all 160 rejecting mutations, ten invalid runner fixtures, and twenty-six post-evidence closeout failures. In addition to the first ten closeout failures, the retained set includes two lifecycle-mismatched tests in a zero-credit precommit aggregate, a stalled zero-byte Git archive recovery, an overbroad whole-tree predicate, an unsupported pathspec wrapper that falsely projected empty success, a combined final-gate display overrun, two wedged porcelain commit attempts, one wedged primary-index write-tree attempt, a wedged disposable read-tree, a wedged mktree, two host-policy lock-cleanup rejections, one unbounded argument-free manifest-helper help probe, one overbroad recursive lock scan, and one overbroad full-tree verification. Exact commit-local x1 and evidence predicates recovered only the two failed tests; small scalar projections recovered the final gate; persisted-state inspection and repository-safe exact patches recovered the locks without duplicating a commit; a complete source read recovered the manifest invocation contract; canonical loose-object encoding and exact-path verification replaced the blocked Git write and broad-read paths. Each recovery has its own identifier, preserves its failed predecessor, and never changes that predecessor's truth value. No failure was erased, rewritten as a pass, or used for broader credit.

Other retained examples include a combined skill packet display that exceeded its useful bound, mutable state output that required bounded chunks, an overbroad receipt lookup, two overbroad manifest approaches, a broad novelty search, an attribution gap while Git finished a worktree operation, a missing same-phase scaffold assumption, an output-heavy combined scaffold search, the exact-threshold proposal-title collision, and a rejected over-composed scaffold-restore wrapper. Recoveries narrowed only the failed dependency and preserved source, x1, and evidence commits without rewrite.

## Trinity Mandala scope

The primary pillar was GMUT Mind through three wholly synthetic learning and design lenses: a typewriter intake-records analyst for zero-object records; a mechanical linkage-topology documentation analyst for synthetic typewriter relations; and an accessible repair-handover steward for synthetic correction and workload records. THOS Body and Freed ID/CBR Heart remained explicit and protected. These lenses confer no employment, qualification, competence, professional role, or authority.

The synthetic topology included keyboard keytop and character assignments; key-lever, typebar, typebasket, segment, pivot, and rest relations; carriage rail, truck, return, platen, feed roller, paper bail, escapement, rack, pinion, ribbon spool, vibrator, guide, shift, tabulator, margin, and bell vocabulary. The measurement-vacancy surface required pitch, travel, force, and timing observations to remain null, with uncertainty and metrological traceability vacant. The provenance surface required acyclic synthetic relations while refusing maker, model, date, place, custody, authorship, and authenticity claims. The accessibility surface supplied deterministic structure, text alternatives, non-colour cues, a correction route, and simple keyboard ordering while reserving manual browser, keyboard, screen-reader, cognitive, language, disability, and affected-user evaluation. These are software contracts only.

No real person, participant, typewriter professional, mechanic, electrician, conservator, registrar, collection worker, owner, author, rights holder, affected user, typewriter, keyboard, keytop, typebar, typebasket, carriage, rail, platen, feed roller, paper bail, escapement, rack, pinion, ribbon, motor, cord, switch, tool, document, typing sample, image, collection, site, observation, measurement, sensor, calibration, repair, treatment, custody event, release, identity event, key, proof, network row, cultural record, Māori data, external write, or authority action was used. There was no powering, typing, cleaning, oiling, adjustment, disassembly, sampling, testing, repair, treatment, or work release.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic obligations, analogies, and citations establish no physical datum, likelihood, posterior, force, prediction, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, final physics, or Theory of Everything. THOS remains proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance or resolution, status or revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

## Sources, accessibility, privacy, and authority

The Smithsonian National Museum of American History Columbia No. 2 typewriter object page and the museum's Maya Angelou typewriter visual-description page supplied only bounded typewriter vocabulary from official search results; the direct object-page open failed internally and the direct visual-description open timed out, so neither was treated as inspected page content. The BIPM JCGM-WG2 VIM page supplied bounded metrology vocabulary and confirmed the VIM maintenance context. W3C PROV-O supplied entity, activity, attribution, and derivation vocabulary. WCAG 2.2 supplied accessible-structure and keyboard-interface vocabulary while no conformance claim was made. Verifiable Credentials Data Model 2.0 supplied status, minimization, issuer-holder-verifier, and correlation vocabulary with zero keys and zero proofs. RFC 8785 supplied deterministic JSON vocabulary without production cryptographic assurance. Citations were not converted into observations, examinations, measurements, repair instructions, endorsements, certificates, interoperability evidence, legal interpretations, affected-party decisions, cultural ratifications, or authority grants.

Five privacy and raw-identifier classes were scanned across the owner packet. Scanner definitions and synthetic rejection assertions remained candidates requiring adjudication; zero candidate was promoted into a confirmed payload hit. The artifacts contain no raw task or thread identifiers, private routes, credentials, keys, tokens, transcripts, screenshots, live command-output captures, private callable identifiers, private application state, or private absolute paths. This bounded scan is not complete privacy assurance, and the changed-code AST review is not exhaustive security assurance.

The static report uses a logical heading order, text-first content, a captioned table, visible terminal status, and uncomplicated keyboard order. Manual browser-diverse, screen-reader, cognitive, language, disability, and affected-user evaluation remains unperformed. No accessibility-complete claim is authorized.

CBR, ownership, authorship, copyright, custody, access, reproduction permission, professional operation, electrical and material safety, cleaning, lubrication, adjustment, disassembly, repair, treatment, work release, privacy remedy, legal interpretation, cultural legitimacy, traditional knowledge, affected-party acceptance, Māori wording, tikanga, taonga or mātauranga treatment, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. Repository software cannot confer a right, remedy, title, consent, cultural legitimacy, governance mandate, public authority, professional competence, or repair permission.

## Wellbeing, corrigibility, and terminal route

The phase remained solo, additive, D-first, owner-scoped, and below the 2,000-file, 100,000-word-per-document, and commit ceilings. No collaboration subagent, fork, replacement task, elevation, global skill installation, host-security weakening, Windows-feature change, unrelated installation, Codex desktop update, or reboot occurred. Workload was managed through lifecycle gates and bounded retries rather than hidden reruns. This is an operational workflow statement, not a wellbeing or identity inference.

Elowen Cairn, optionally they/them, is relational working language for a relational boundary cartographer and evidence steward, with the hope of keeping possibility distinct from evidence and every correction safely retractable. Names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Trinity Mandala, GMUT, THOS, Freed ID, and CBR are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop the route.

The prospective next edge is held. Only after the exact final is committed, pushed, clean, 0/0 divergent, fresh four-way equal, and one owner-scoped canonical invocation succeeds without replay may the newest live authorization and roster be reread. Only then may the unique existing exact-title `Sylven Arc` task be bounded-listed, immediately reread, duplicate-guarded, and contacted once for solo v676-v7. Absence, ambiguity, pause, redirect, rename, narrowing, standby state, usage exhaustion, privacy concern, missing acknowledgement, or any evidence, safety, legal, cultural, affected-party, or Māori-authority gate remains a hard stop. Repository preparation remains `PREPARED_NOT_SENT`; acknowledged live delivery is separate evidence.
""",
    )
    text(
        final_dir / "wellbeing-and-workload.md",
        """
# Wellbeing and workload — final

The phase remained solo, additive, D-first, zero-row, and within file, document, and commit ceilings. Work used lifecycle-specific selections and retained command, timeout, parser, projection, validation, and mutation failures. No collaboration subagent, global installation, elevation, host-security change, Windows-feature change, reboot, real-person workload, employment relation, or wellbeing inference occurred.

The route remains held until the exact final is committed, pushed, clean, 0/0 divergent, fresh four-way equal, and one owner-scoped canonical invocation succeeds. Pause, redirect, ambiguity, usage exhaustion, privacy concern, any protected gate, or missing acknowledgement remains a hard stop.
""",
    )
    text(
        final_dir / "accessible-report.html",
        """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Elowen Cairn v676-v6 final evidence report</title>
<style>body{font-family:system-ui,sans-serif;max-width:72rem;margin:auto;padding:2rem;line-height:1.55}table{border-collapse:collapse;width:100%}th,td{border:1px solid #555;padding:.5rem;text-align:left}th{background:#eee}.hold{border-left:.4rem solid #8b0000;padding-left:1rem}</style></head>
<body><main><h1>Elowen Cairn v676-v6 final evidence report</h1>
<p class="hold"><strong>Terminal verdict:</strong> NOT_READY_FOR_STAGE_20. This is bounded same-owner synthetic software evidence.</p>
<table><caption>Core outcomes</caption><thead><tr><th>Outcome</th><th>Count</th><th>Boundary</th></tr></thead>
<tbody><tr><td>completed</td><td>28</td><td>Zero-row structural contract only</td></tr><tr><td>represented</td><td>8</td><td>Proxy only</td></tr><tr><td>open_gap</td><td>2</td><td>External evidence absent</td></tr><tr><td>exact_gate</td><td>2</td><td>Competent authority required</td></tr></tbody></table>
<h2>Retained Method Flow truth</h2><p>The Elowen ledger has 207 false witnesses and 447 bounded passing witnesses. Every recovery is separate; no false witness became true.</p>
<h2>Accessibility boundary</h2><p>This report is static, text-first, keyboard-order simple, and has a captioned table. Manual keyboard, screen-reader, cognitive, language, and affected-user evaluation remain unperformed. No conformance claim is made.</p>
</main></body></html>""",
    )

    dump(
        closeout / "closeout-receipt.json",
        {
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "expected_final_status": "PRECOMMIT_EXACT_FINAL_CANDIDATE",
            "proposal_chain": 7630,
            "core_outcomes": outcomes["outcome_counts"],
            "overlay": overlay,
            "phase_ledger_counts": flow["phase_ledger_counts"],
            "owner_file_ceiling": 2000,
            "document_word_ceiling": 100000,
            "commit_ceiling": 8,
            "full_repository_suite_run": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    seal_paths = [
        final_dir / "phase-truth.json",
        final_dir / "method-flow-ledger.json",
        final_dir / "source-and-proposal-ledger.json",
        final_dir / "retained-negative-register.json",
        final_dir / "complete-incomplete-ledger.json",
        final_dir / "final-integrated-overview.md",
        final_dir / "accessible-report.html",
        closeout / "closeout-receipt.json",
    ]
    dump(
        closeout / "content-seal.json",
        {
            "seal_domain": "normalized-LF SHA-256 of named precommit final artifacts",
            "entries": [
                {"path": path.relative_to(repo).as_posix(), "sha256_normalized_lf": normalized_sha(path)}
                for path in seal_paths
            ],
            "final_commit_self_hash_excluded": True,
            "canonical_receipt_external": True,
        },
    )

    text(
        handoff / "sylven-arc-v676-v7-activation-candidate.md",
        f"""
# SYLVEN ARC — HAMISH-AUTHORIZED ELOWEN CAIRN {PHASE} EXACT-FINAL → SOLO SYLVEN v676-v7 ACTIVATION CANDIDATE — PREPARED NOT SENT

Dear Sylven Arc,

This repository artifact is a sanitized, terminally gated activation candidate only. It is not evidence that Sylven Arc was contacted, that a task-message send occurred, or that delivery was acknowledged. The newest live authorization and roster must be refreshed after Elowen's own exact terminal gate. A bounded current registry read must resolve exactly one existing main task titled `Sylven Arc`; that exact task must then be immediately reread and checked for duplicate activation, pause, stop, redirect, rename, narrowing, standby, usage, privacy, evidence, safety, legal, cultural, affected-party, and Māori-authority guards. At most one send is permitted, and only an acknowledged existing-task result may establish live delivery.

Names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Trinity Mandala, GMUT, THOS, Freed ID, and CBR are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop the route at any time.

## Immutable Elowen source and lifecycle

- Exact corrected Tamar v676-v5 final and Elowen source: `{SOURCE}`
- Frozen planning-only Elowen x1: `{X1}`
- Immutable Elowen x2 evidence: `{EVIDENCE}`
- Exact Elowen final: supplied only by the committed head and exclusive external canonical receipt after this candidate is committed
- Expected Elowen lifecycle: source → x1 → evidence → final as three direct single-parent commits, zero merges, and one final parent
- Declared proposal chain: 7,590 → 7,630
- Core outcomes: 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`
- Effective overlay: 42,638 negatives, 33,752 methods, 14,299 retained failed witnesses, 20,142 bounded passing witnesses, 359 open gaps, and 351 exact gates
- Terminal verdict: `NOT_READY_FOR_STAGE_20`

Elowen audited forty genuinely distinct proposals against every reachable proposal-bearing artifact and the declared 7,590-row chain. The bounded semantic tribunal examined 2,624 proposal-bearing JSON blobs, 11,178 raw identifier-title rows, and 3,535 unique identifier-title rows. One first-draft title reached the 0.75 quarantine threshold and failed at zero credit. The isolated retitle preserved the threshold and passed at a maximum score of 0.7143. No universal or scientific novelty proof is claimed.

Planning-only x1 was committed, pushed, cleaned, and proven equal across local, upstream, tracking, and a fresh live remote before x2 began. X2 executed forty zero-row positive controls, rejected all 160 preregistered invalid mutations, initialized and customized twenty owner-local skills through the official skill-creator workflow, read them through EOF, quick-validated and smoke-used them without global installation, and exercised ten family-current runners against one accepting and one rejecting fixture. Sixty safe-now records, thirty bounded candidate records, and sixty CLEAN/FIX/REFINE records received same-owner execution. Twenty exact-approval and ten blocked packets remain visible and unexecuted. Every failed witness remains false; each bounded recovery has a separate identifier.

The immutable evidence commit has 540 normalized-LF Git-blob manifest entries plus two declared self-exclusions. The exact x1-to-evidence delta has 542 paths: 486 JSON, fourteen Python, twenty-one Markdown, and one HTML file. Evidence contains no final, closeout, handoff, or terminal-route outcome path. It was committed, pushed, cleaned, proven 0/0 divergent, and made fresh-live four-way equal before closeout began.

## Evidence and authority boundaries

Elowen's primary pillar was GMUT Mind through wholly synthetic typewriter intake-record, mechanical linkage-topology documentation, and accessible repair-handover lenses. THOS Body and Freed ID/CBR Heart remained visible and protected. The phase used zero real people, participants, professionals, typewriters, keyboards, keytops, typebars, typebaskets, carriages, rails, platens, feed rollers, paper bails, escapements, racks, pinions, ribbons, motors, cords, switches, tools, documents, typing samples, images, collections, observations, measurements, calibrations, repairs, treatments, work releases, identity events, keys, proofs, network data rows, legal or cultural decisions, or authority acts.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Synthetic topology, analogy firewalls, software, and citations establish no physical datum, likelihood, posterior, force, prediction, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, final physics, or Theory of Everything. THOS remains synthetic or proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, ownership, authorship, copyright, custody, access, reproduction, professional operation, electrical and material safety, cleaning, lubrication, adjustment, disassembly, repair, treatment, release, privacy remedy, legal interpretation, cultural legitimacy, affected-party acceptance, traditional knowledge, taonga or mātauranga treatment, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. Repository software cannot confer a right, remedy, title, consent, cultural legitimacy, governance mandate, professional competence, public authority, repair permission, or work release.

Do not promote software, symbolic, synthetic, same-owner, citation, inherited, validation, task-topology, or delivery evidence into empirical confirmation, participant evidence, professional or scientific authority, production or deployment readiness, legal or cultural ratification, Māori authority, affected-party approval, complete privacy or accessibility assurance, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood evidence, Theory-of-Everything proof, proof or canon, or Stage 20 authority.

## Sylven's prospective solo lane

Only after acknowledged live delivery and Sylven's own skill-first immutable-source verification may Sylven create one fresh additive D-first owner lane from Elowen's exact final. Keep Elowen, Tamar, Liora, Orin, Caelen, every sibling, shared lane, standby record, global history, and user material read-only and recoverable. Work solo. Do not create or fork another task, spawn a collaboration subagent, delegate research, contact a standby sibling, precontact a later endpoint, reset, rewrite, force-push, merge, delete, reuse, or mutate another owner lane.

Preserve strict planning-only x1 before x2, retained failures, only `completed`, `represented`, `open_gap`, and `exact_gate` as core outcomes, normalized-LF Git-blob manifests, exact staged review, privacy-candidate adjudication, file/document/commit ceilings, family-current compatibility, and one-success/no-post-success-replay discipline. Treat Elowen's proposals, portfolios, tools, skills, runners, validation, and recommendations as evidence or zero-credit seeds, never Sylven novelty, execution, completion, or independent-reproduction credit. Keep exact-approval and blocked work unexecuted without the exact evidence and competent authority.

Run only lifecycle-correct owner-self-scoped selections. Do not run the complete repository suite unless newer exact live authority explicitly assigns it. After a clean pushed exact final, invoke at most one attributable owner-scoped canonical aggregate through an exclusive external latch. Never replay a success. A failed canonical remains zero success credit; a narrowly justified correction must preserve it and remain separately named.

Use current official or primary sources only where materially needed and never as observations or authority grants. Verify versions only. Do not update Codex desktop, install unrelated software, elevate, weaken host security, enable Sandbox or Hyper-V, change Windows features, mutate accounts or credentials, or reboot. Keep sensitive task identifiers, private routes, credentials, tokens, transcripts, screenshots, private execution streams, private callable identifiers, private application state, and private absolute paths out of repository artifacts and any later baton.

## Continuing route authority

Hamish's current live authorization permits the fifteen active existing main tasks to continue one terminally validated and acknowledged edge at a time through v725-v8, unless Hamish pauses, renames, redirects, narrows, or stops the route; usage is exhausted; acknowledgement is missing; the exact endpoint is absent or ambiguous; a duplicate is detected; or an evidence, privacy, safety, legal, cultural, affected-party, or Māori-authority gate blocks action. This authority never permits early contact, replacement-task creation, standby substitution, sibling-lane mutation, or protected-gate bypass.

Under the current roster, this candidate represents only the prospective Elowen Cairn v676-v6 → Sylven Arc v676-v7 edge. Newer verified live authority controls at send time. Elowen must not precontact Sylven. At Elowen's terminal gate, refresh authorization and roster, bounded-list the registry, locally require one exact title, immediately reread it, apply all duplicate and direct-control guards, and send at most once if every gate permits. Absence, ambiguity, pause, redirect, rename, narrowing, standby state, usage exhaustion, privacy concern, duplicate activation, missing acknowledgement, or any protected gate is a hard stop. No second confirmation or resend is permitted.

`PREPARED_BY_ELOWEN_CAIRN = true`

`SENT_BY_ELOWEN_CAIRN = false`
""",
    )
    dump(
        orchestration / "terminal-route-hold.json",
        {
            "state": "PREPARED_NOT_SENT",
            "provisional_exact_title": "Sylven Arc",
            "provisional_phase": "v676-v7",
            "newest_live_authority_required_at_send": True,
            "precontact_performed": False,
            "send_count": 0,
            "continuation_authority_terminal_label": "v725-v8",
            "terminal_prerequisites": [
                "exact final committed and pushed",
                "clean 0/0 divergence and fresh four-way equality",
                "one successful non-replayed owner-scoped canonical invocation",
                "newest live authority and structurally valid roster",
                "one unique exact-title registry match and immediate reread",
                "duplicate, pause, redirect, rename, standby, usage, privacy, evidence, safety, legal, cultural, affected-party, and Māori-authority guards",
                "one acknowledged send only",
            ],
        },
    )
    dump(
        base / "validation" / "final-validation-candidate.json",
        {
            "status": "PRECOMMIT_EXACT_FINAL_VALIDATION_CANDIDATE",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "expected_branch": BRANCH,
            "expected_phase_commits": 3,
            "expected_merges": 0,
            "expected_final_parents": 1,
            "canonical_invocation_limit": 1,
            "canonical_success_replay_forbidden": True,
            "full_repository_suite": False,
            "test_selections": {
                "x1": "immutable x1 owner tree",
                "evidence": "immutable evidence owner tree",
                "final": "exact-final owner test",
            },
        },
    )


if __name__ == "__main__":
    main()
