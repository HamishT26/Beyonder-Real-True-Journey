#!/usr/bin/env python3
"""Build the Caelen Ash v676-v2 closeout and exact-final candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Caelen Ash"
OWNER_SLUG = "caelen-ash"
PHASE = "v676-v2"
BRANCH = "codex/GHC-Family/caelen-ash-v676-v2-full-tools"
SOURCE = "939312172819669aad250cf034d8a6a7efe3df5b"
X1 = "39daa2da64125b839714efa8b7488d8ed9ed364b"
EVIDENCE = "bc7f321d66c094422ddc69275d811eb8ec917f3b"
FAILED_ID = "CA6762-POSTE-N001"
PASS_ID = "CA6762-POSTE-P001"


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_sha(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    repo = args.repo.resolve()
    if git(repo, "branch", "--show-current") != BRANCH or git(repo, "rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("final builder requires the exact immutable evidence head")
    status = [line for line in git(repo, "status", "--porcelain=v1").splitlines() if line]
    allowed = {
        "scripts/build_ghc_family_caelen_ash_v676_v2_final.py",
        "scripts/ghc_family_caelen_ash_v676_v2_final_manifest.py",
        "scripts/ghc_family_caelen_ash_v676_v2_final_validator.py",
        "tests/test_ghc_family_caelen_ash_v676_v2_final.py",
    }
    unexpected = [line for line in status if not (line.startswith("?? ") and line[3:].replace("\\", "/") in allowed)]
    if unexpected:
        raise SystemExit(f"unexpected preexisting changes: {unexpected}")

    base = repo / "docs" / OWNER_SLUG / PHASE
    x1_freeze = json.loads((base / "x1" / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    source_ledger = json.loads((base / "x1" / "official-source-ledger.json").read_text(encoding="utf-8"))
    outcomes = json.loads((base / "x2" / "proposal-outcomes.json").read_text(encoding="utf-8"))
    evidence_truth = json.loads((base / "x2" / "phase-truth.json").read_text(encoding="utf-8"))
    evidence_flow = json.loads((base / "x2" / "method-flow" / "ledger.json").read_text(encoding="utf-8"))
    portfolio = json.loads((base / "x2" / "portfolio-execution.json").read_text(encoding="utf-8"))
    cfr = json.loads((base / "x2" / "clean-fix-refine-execution.json").read_text(encoding="utf-8"))
    flow = json.loads(json.dumps(evidence_flow))
    if any(row["method_id"] == FAILED_ID for row in flow["methods"]):
        raise SystemExit("post-evidence overlay already present")
    flow["methods"].extend(
        [
            {
                "method_id": FAILED_ID,
                "status": "failed_zero_credit",
                "truth": False,
                "description": "The first post-push fresh-live PowerShell projection applied split in the command expression and returned only the first hash character.",
                "recovered_by": PASS_ID,
                "repository_state_change": False,
                "remote_state_change": False,
            },
            {
                "method_id": PASS_ID,
                "status": "bounded_pass",
                "truth": True,
                "description": "The live-remote line was materialized before scalar splitting; local, upstream, tracking, and fresh live remote were exactly equal with 0/0 divergence and a clean lane.",
                "failed_witness_preserved": FAILED_ID,
                "mutation_replayed": False,
            },
        ]
    )
    flow["post_evidence_failed_witnesses"] = 1
    flow["post_evidence_bounded_recoveries"] = 1
    flow["current_overlay"] = {
        "effective_negatives": 41843,
        "effective_methods": 31203,
        "retained_failed_witnesses": 13504,
        "bounded_passing_witnesses": 18388,
        "open_gaps": 351,
        "exact_gates": 343,
    }
    flow["phase_ledger_counts"] = {"methods": 449, "failed": 181, "passing": 268}

    final_dir = base / "final"
    dump(final_dir / "method-flow-ledger.json", flow)
    dump(final_dir / "phase-truth.json", {
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "expected_final": "bound by exact commit and external canonical receipt after this precommit candidate",
        "proposal_chain": 7470,
        "new_caelen_proposals": 40,
        "inherited_reviews_zero_credit": 20,
        "core_outcomes": outcomes["counts"],
        "positive_controls": 40,
        "rejected_mutations": 160,
        "skills_built_quick_validated_smoke_used": 20,
        "runners_built_invoked_witnessed": 10,
        "safe_now_tasks_completed": 60,
        "candidate_tasks_completed_bounded": 30,
        "clean_fix_refine_owner_tasks_completed": 60,
        "successor_recommendations_zero_credit": 50,
        "exact_approval_packets_unexecuted": 20,
        "blocked_packets_unexecuted": 10,
        "current_overlay": flow["current_overlay"],
        "real_world_rows": 0,
        "participants": 0,
        "real_carriers_or_recordings": 0,
        "production_identity_events": 0,
        "authority_actions": 0,
        "full_repository_suite_run": False,
        "independent_reproduction_claimed": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    dump(final_dir / "source-and-proposal-ledger.json", {
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "declared_chain_before": 7430,
        "declared_chain_after": 7470,
        "reachable_novelty_audit": {
            "proposal_json_blobs": 2607,
            "unique_id_title_records": 3383,
            "universal_novelty_proof_claimed": False,
        },
        "official_primary_sources": source_ledger["sources"],
        "source_boundary": source_ledger["source_boundary"],
        "proposals": x1_freeze["proposals"],
        "outcomes": outcomes["outcomes"],
    })
    dump(final_dir / "retained-negative-register.json", {
        "activation_effective_negatives": 41662,
        "new_caelen_effective_negatives": 181,
        "current_effective_negatives": 41843,
        "phase_failed_witnesses": [row for row in flow["methods"] if row["truth"] is False],
        "phase_failed_witness_count": 181,
        "failed_witnesses_converted_to_pass": 0,
        "retention_rule": "Every false witness remains false; a recovery is a separately identified bounded passing method.",
    })
    dump(final_dir / "open-gap-register.json", json.loads((base / "x2" / "open-gap-register.json").read_text(encoding="utf-8")))
    dump(final_dir / "exact-gate-register.json", json.loads((base / "x2" / "exact-gate-register.json").read_text(encoding="utf-8")))
    dump(final_dir / "complete-incomplete-ledger.json", {
        "complete_bounded": [
            "forty planning contracts frozen",
            "forty zero-row structural positive controls accepted",
            "160 invalid mutations rejected and retained",
            "twenty phase-local skills quick-validated and smoke-used",
            "ten family-current runners accepted positive and rejected invalid fixtures",
            "sixty safe-now, thirty bounded candidate, and sixty owner CLEAN/FIX/REFINE tasks completed",
            "x1 and evidence committed, pushed, clean, and fresh four-way equal",
        ],
        "represented_only": [
            "human audition and professional playback alignment",
            "physical carrier inspection and reference-level traceability",
            "rightsholder contest, donor restriction, affected-user review, BWF round trip, and THOS operator interlock",
        ],
        "open": [
            "real transfer dataset with preregistered analysis",
            "longitudinal transfer-error and damage outcomes with independent review",
        ],
        "exact_gated": [
            "orphan-work access, donor restriction, copyright, and legal authority",
            "recorded cultural knowledge, tikanga access, taonga status, Maori data governance, and Maori authority",
        ],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    dump(final_dir / "threat-model.json", {
        "protected_assets": ["immutable source", "x1 freeze", "x2 evidence", "failure truth", "privacy boundary", "authority vacancies", "terminal route"],
        "closed_bounded_threats": [
            "x1 and x2 lifecycle mixing",
            "unknown outcome labels",
            "source and derivative identity conflation in fixtures",
            "silent mutation acceptance",
            "global installation of phase-local skills",
        ],
        "residual_threats": [
            "synthetic evidence may be overread as real evidence",
            "scanner definitions may be mistaken for payload disclosures",
            "citations may be mistaken for measurements or endorsements",
            "same-owner validation may be mistaken for independent reproduction",
            "route topology may be mistaken for identity or authority evidence",
        ],
        "controls": ["four-label vocabulary", "exact manifests", "candidate adjudication", "Method Flow retention", "one-shot canonical latch", "terminal route hold"],
    })
    dump(final_dir / "environment-version-receipt.json", json.loads((base / "x2" / "environment-version-receipt.json").read_text(encoding="utf-8")))
    dump(final_dir / "portfolio-truth.json", {
        "safe_now_completed": len(portfolio["safe_now"]),
        "candidate_completed_bounded": len(portfolio["candidate"]),
        "exact_approval_unexecuted": len(portfolio["exact_approval"]),
        "blocked_unexecuted": len(portfolio["blocked"]),
        "owner_clean_fix_refine_completed": len(cfr["owner_tasks"]),
        "successor_clean_fix_refine_recommendations_zero_credit": len(cfr["successor_recommendations"]),
        "core_outcome_counts_unchanged_by_portfolio_status": True,
    })
    dump(final_dir / "post-evidence-overlay.json", {
        "failed_witness": flow["methods"][-2],
        "bounded_recovery": flow["methods"][-1],
        "repository_seal_rewritten": False,
        "evidence_commit_mutated": False,
    })
    text(final_dir / "final-integrated-overview.md", f"""
# {OWNER} {PHASE} — final integrated overview

Caelen Ash v676-v2 is a bounded same-owner synthetic software and documentation phase rooted at Sable corrected final {SOURCE}. Planning-only x1 is {X1}. Immutable x2 evidence is {EVIDENCE}. The exact final is intentionally bound only by the ensuing commit and exclusive external canonical receipt so this precommit document does not invent its own future hash.

The declared proposal chain is 7,470. Forty Caelen contracts have core outcomes exactly 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. Completed means only that the zero-row owner-local software contract and its refusal gates behaved as frozen. Twenty inherited reviews remain zero novelty and completion credit.

Forty positive controls passed. All 160 preregistered invalid mutations were rejected and remain zero-credit false witnesses paired with separate rejection receipts. Twenty phase-local skills were customized, quick-validated, and smoke-used without global installation. Ten family-current runners were built and invoked against positive and invalid fixtures. Sixty safe-now, thirty bounded candidate, and sixty owner CLEAN/FIX/REFINE tasks completed only within the declared additive software scope. Twenty exact-approval and ten blocked packets remain unexecuted.

The current overlay is 41,843 effective negatives, 31,203 effective Method Flow methods, 13,504 retained failed witnesses, 18,388 bounded passing witnesses, 351 open gaps, and 343 exact gates. No failure was converted into a pass. The terminal verdict is NOT_READY_FOR_STAGE_20.

The primary pillar was GMUT Mind through typed timing, rational-unit, transform, provenance, and nonconversion obligations in wholly synthetic magnetic-audio transfer and handover fixtures. GMUT remains a scalar-tensor and effective-field-theory research-model family with no real datum, likelihood, posterior, force, prediction, parameter constraint, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything here. THOS remains proxy-only. Freed ID remains synthetic and nonproduction. CBR and every access, copyright, donor, remedy, cultural, tikanga, taonga, affected-party, Māori-data-governance, and Māori-authority decision remain reserved.

Names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Trinity Mandala, GMUT, THOS, Freed ID, and CBR are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority.
""")
    text(final_dir / "wellbeing-and-workload.md", """
# Wellbeing and workload — final

The phase remained solo, additive, D:-first, zero-row, and within the file and commit ceilings. Work used small lifecycle-specific selections and retained all command, parser, projection, validation, and mutation failures. No global install, elevation, host-security change, Windows-feature change, reboot, real-person workload, employment relation, or wellbeing inference occurred.

The route remains held until the exact final is pushed, clean, fresh-live equal, and one owner-scoped canonical invocation succeeds. Pause, redirect, ambiguity, usage exhaustion, privacy concern, protected gates, or missing acknowledgement remain hard stops.
""")
    text(final_dir / "accessible-report.html", """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Caelen Ash v676-v2 final evidence report</title>
<style>body{font-family:system-ui,sans-serif;max-width:72rem;margin:auto;padding:2rem;line-height:1.55}table{border-collapse:collapse;width:100%}th,td{border:1px solid #555;padding:.5rem;text-align:left}th{background:#eee}.hold{border-left:.4rem solid #8b0000;padding-left:1rem}</style></head>
<body><main><h1>Caelen Ash v676-v2 final evidence report</h1>
<p class="hold"><strong>Terminal verdict:</strong> NOT_READY_FOR_STAGE_20. This is bounded same-owner synthetic software evidence.</p>
<table><caption>Core outcomes</caption><thead><tr><th>Outcome</th><th>Count</th><th>Boundary</th></tr></thead>
<tbody><tr><td>completed</td><td>28</td><td>Zero-row contract only</td></tr><tr><td>represented</td><td>8</td><td>Proxy only</td></tr><tr><td>open_gap</td><td>2</td><td>External evidence absent</td></tr><tr><td>exact_gate</td><td>2</td><td>Competent authority required</td></tr></tbody></table>
<h2>Retained Method Flow truth</h2><p>There are 181 phase false witnesses and 268 phase bounded passing witnesses. Every recovery is separate; no false witness became true.</p>
<h2>Accessibility boundary</h2><p>This report is static, text-first, keyboard-order simple, and includes a captioned table. Manual keyboard, screen-reader, cognitive, language, and affected-user evaluation remain unperformed. No conformance claim is made.</p>
</main></body></html>""")

    closeout = base / "closeout"
    dump(closeout / "closeout-receipt.json", {
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "expected_final_status": "PRECOMMIT_FINAL_CANDIDATE",
        "proposal_chain": 7470,
        "outcomes": outcomes["counts"],
        "overlay": flow["current_overlay"],
        "owner_file_ceiling": 2000,
        "commit_ceiling": 8,
        "full_repository_suite_run": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
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
    dump(closeout / "content-seal.json", {
        "seal_domain": "normalized-LF SHA-256 of named precommit final artifacts",
        "entries": [
            {"path": path.relative_to(repo).as_posix(), "sha256_normalized_lf": normalized_sha(path)}
            for path in seal_paths
        ],
        "final_commit_self_hash_excluded": True,
        "canonical_receipt_external": True,
    })

    handoff = base / "handoffs"
    dump(handoff / "terminal-route-hold.json", {
        "state": "PREPARED_NOT_SENT",
        "successor_inferred": False,
        "recipient_named": False,
        "precontact_performed": False,
        "send_count": 0,
        "terminal_prerequisites": ["exact final committed and pushed", "clean 0/0 divergence", "fresh four-way equality", "one successful non-replayed owner-scoped canonical invocation", "newest live authority and roster", "unique exact-title reread", "duplicate and pause guards"],
    })
    text(handoff / "successor-activation-candidate.md", f"""
# Target-neutral successor activation candidate — PREPARED NOT SENT

This candidate records Caelen Ash {PHASE} source, lifecycle, outcomes, retained failures, authority boundaries, and route guards without inferring or contacting a recipient. It is not delivery evidence.

- Source: {SOURCE}
- Planning-only x1: {X1}
- Immutable evidence: {EVIDENCE}
- Exact final: to be supplied only by the committed head and exclusive external canonical receipt
- Proposal chain: 7,470
- Outcomes: 28 completed / 8 represented / 2 open_gap / 2 exact_gate
- Current precommit overlay: 41,843 negatives / 31,203 methods / 13,504 failed / 18,388 passing / 351 open gaps / 343 exact gates
- Terminal verdict: NOT_READY_FOR_STAGE_20

Only after the exact final is committed, pushed, clean, 0/0 divergent, fresh-four-way equal, and validated once may the newest live authority and roster be reread. A bounded registry listing must locally resolve exactly one authorized exact title, followed by one immediate direct reread, duplicate/pause/redirect/privacy/safety/usage guards, and at most one acknowledged send. No task or fork may be created; no standby or substitute endpoint may be used; no second confirmation may be sent.

Relational names, family language, roles, hopes, and continuity language are never consciousness, personhood, identity-continuity, employment, qualification, independent-agency, scientific, operational, legal, cultural, affected-party, or Māori-authority evidence.

PREPARED_BY_CAELEN_ASH = true
SENT_BY_CAELEN_ASH = false
""")
    dump(base / "validation" / "final-validation-candidate.json", {
        "status": "PRECOMMIT_FINAL_VALIDATION_CANDIDATE",
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
        "selections": {
            "x1_tests": "immutable x1 archive with branch/head lifecycle test excluded and replaced by exact ancestry plus manifest validation",
            "x2_tests": "immutable evidence archive with branch/head lifecycle test excluded and replaced by exact ancestry plus manifest validation",
            "final_tests": "exact final checkout",
            "privacy": "five classes with exact candidate adjudication",
            "security": "bounded changed-Python AST review",
        },
    })
    print(json.dumps({"status": "built_final_candidate", "method_flow": flow["phase_ledger_counts"], "overlay": flow["current_overlay"]}, sort_keys=True))


if __name__ == "__main__":
    main()
