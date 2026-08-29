#!/usr/bin/env python3
"""Build the additive Orin Thale v676-v3 exact-final candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Orin Thale"
OWNER_SLUG = "orin-thale"
PHASE = "v676-v3"
BRANCH = "codex/GHC-Family/orin-thale-v676-v3-full-tools"
SOURCE = "8f1e9ebc708b5ddc23bee4e407d946fe3e322bf3"
X1 = "3ba3826fb79f836a46a577af2809a5dd6e445350"
EVIDENCE = "b5f7a4dfc6e0b9790c0569f144fbeb4649d79d93"

POST_EVIDENCE_METHODS = [
    {
        "method_id": "OR6763-POSTE-N001",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first evidence-manifest wrapper crossed its bounded projection window without an attributable result while the original Python process remained active.",
        "recovered_by": "OR6763-POSTE-P001",
        "repository_state_change": False,
        "remote_state_change": False,
    },
    {
        "method_id": "OR6763-POSTE-P001",
        "status": "bounded_pass",
        "truth": True,
        "description": "The exact original process was inspected and allowed to finish without replay; it produced and staged the 519-entry evidence manifest plus two declared self-exclusions.",
        "failed_witness_preserved": "OR6763-POSTE-N001",
        "mutation_replayed": False,
    },
    {
        "method_id": "OR6763-POSTE-N002",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first bounded Wait-Process audit returned no attributable projection while the original manifest process was still active.",
        "recovered_by": "OR6763-POSTE-P002",
        "repository_state_change": False,
        "remote_state_change": False,
    },
    {
        "method_id": "OR6763-POSTE-P002",
        "status": "bounded_pass",
        "truth": True,
        "description": "A separate read-only process and Git-index audit showed CPU progress, retained the same process identity, and confirmed the staged index remained intact.",
        "failed_witness_preserved": "OR6763-POSTE-N002",
        "mutation_replayed": False,
    },
    {
        "method_id": "OR6763-POSTE-N003",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "A later wait-and-status projection used an inline PowerShell conditional where a scalar value was required and failed after the wait.",
        "recovered_by": "OR6763-POSTE-P003",
        "repository_state_change": False,
        "remote_state_change": False,
    },
    {
        "method_id": "OR6763-POSTE-P003",
        "status": "bounded_pass",
        "truth": True,
        "description": "The CPU scalar was materialized before comparison; the same original process remained attributable and then completed without replay.",
        "failed_witness_preserved": "OR6763-POSTE-N003",
        "mutation_replayed": False,
    },
    {
        "method_id": "OR6763-POSTE-N004",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The evidence-commit tool projection truncated the large create-file listing before presenting an attributable compact completion summary.",
        "recovered_by": "OR6763-POSTE-P004",
        "repository_state_change": False,
        "remote_state_change": False,
    },
    {
        "method_id": "OR6763-POSTE-P004",
        "status": "bounded_pass",
        "truth": True,
        "description": "A compact read-only Git audit recovered the exact evidence commit, parent, two-commit lifecycle count, clean state, 0/0 divergence, and fresh four-way equality.",
        "failed_witness_preserved": "OR6763-POSTE-N004",
        "mutation_replayed": False,
    },
    {
        "method_id": "OR6763-POSTE-N005",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first final-manifest preflight classified two inherited staged-review scanner-class labels as payload hits solely because those adjudication records were JSON rather than Python.",
        "recovered_by": "OR6763-POSTE-P005",
        "repository_state_change": False,
        "remote_state_change": False,
        "final_manifest_created": False,
    },
    {
        "method_id": "OR6763-POSTE-P005",
        "status": "bounded_pass",
        "truth": True,
        "description": "The recovery recognized previously adjudicated staged-review records as scanner metadata while preserving all five class scans; zero confirmed payload hits remained.",
        "failed_witness_preserved": "OR6763-POSTE-N005",
        "mutation_replayed": False,
    },
    {
        "method_id": "OR6763-POSTE-N006",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first final precommit test wrapper crossed its projection window after four progress markers; the original process later ended after its output handle was lost, leaving no attributable exit code or test summary.",
        "recovered_by": "OR6763-POSTE-P006",
        "repository_state_change": False,
        "remote_state_change": False,
        "validation_credit": 0,
    },
    {
        "method_id": "OR6763-POSTE-P006",
        "status": "bounded_pass",
        "truth": True,
        "description": "The manifest-parity test transport was changed from per-entry Git process spawning to one index/tree map and one streaming batch reader; the separately identified corrected precommit selection then completed with an attributable result.",
        "failed_witness_preserved": "OR6763-POSTE-N006",
        "original_test_result_inferred": False,
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
        raise SystemExit("final builder requires the exact immutable Orin evidence head")
    allowed = {
        "scripts/build_ghc_family_orin_thale_v676_v3_final.py",
        "scripts/ghc_family_orin_thale_v676_v3_final_manifest.py",
        "scripts/ghc_family_orin_thale_v676_v3_final_validator.py",
        "tests/test_ghc_family_orin_thale_v676_v3_final.py",
    }
    status = [line for line in git(repo, "status", "--porcelain=v1").splitlines() if line]
    allowed_doc_prefixes = (
        "docs/orin-thale/v676-v3/closeout/",
        "docs/orin-thale/v676-v3/final/",
        "docs/orin-thale/v676-v3/handoffs/",
        "docs/orin-thale/v676-v3/orchestration/",
        "docs/orin-thale/v676-v3/validation/final-",
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
    if (len(flow["methods"]), failed, passing) != (620, 190, 430):
        raise SystemExit("unexpected final Method Flow partition")
    overlay = {
        "effective_negatives": 42036,
        "effective_methods": 31828,
        "retained_failed_witnesses": 13697,
        "bounded_passing_witnesses": 18820,
        "open_gaps": 353,
        "exact_gates": 345,
    }
    flow["phase_ledger_counts"] = {"methods": 620, "failed": 190, "passing": 430}
    flow["current_overlay"] = overlay
    flow["post_evidence_failed_witnesses"] = 6
    flow["post_evidence_bounded_recoveries"] = 6
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
            "declared_proposal_chain": 7510,
            "new_orin_proposals": 40,
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
            "declared_chain_before": 7470,
            "declared_chain_after": 7510,
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
            "activation_effective_negatives": 41846,
            "new_orin_effective_negatives": 190,
            "current_effective_negatives": 42036,
            "phase_failed_witness_count": 190,
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
                "real claimant interviews, finder interviews, and affected-user accessibility evaluation",
                "live interoperability, status, revocation, recovery, security, and privacy review",
                "real operator workload, incident, custody, correction, and remedy outcomes",
            ],
            "open": [
                "real lost-property records and claimant-participant evidence with preregistered analysis",
                "longitudinal interoperability, retention, security, and independently reviewed outcome evidence",
            ],
            "exact_gated": [
                "ownership, return, disposal, insurance, police, hazardous-item, and legal decisions",
                "cultural property, taonga, tikanga, Māori data governance, wording, and Māori authority",
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

Orin Thale v676-v3 is a bounded same-owner synthetic software and documentation phase rooted at immutable Caelen final `{SOURCE}`. Planning-only x1 is `{X1}` and immutable x2 evidence is `{EVIDENCE}`. The exact final is intentionally bound by the ensuing commit and exclusive external canonical receipt; this precommit document does not invent its own future hash.

The declared proposal chain is 7,510. Forty new Orin contracts have core outcomes exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. `completed` means only that the frozen zero-row owner-local structural contract and its refusal gates behaved as declared. Twenty inherited reviews remain zero novelty and completion credit. No universal novelty proof is claimed because the bounded reachable audit is not a single complete canonical ledger.

Forty positive controls passed. All 160 preregistered invalid mutations were executed, rejected, and retained as zero-credit false witnesses paired with separate rejection evidence. Twenty phase-local skills were customized, quick-validated, and smoke-used without global installation. Ten family-current runners accepted their positive fixture and rejected their paired invalid fixture. Sixty safe-now, thirty bounded candidate, and sixty CLEAN/FIX/REFINE tasks completed only inside the declared owner-local scope. Twenty exact-approval and ten blocked packets remain unexecuted.

The final overlay is 42,036 effective negatives, 31,828 effective Method Flow methods, 13,697 retained failed witnesses, 18,820 bounded passing witnesses, 353 open gaps, and 345 exact gates. The Orin phase ledger contains 620 methods: 190 false and 430 bounded passing. Six post-evidence operational failures and their six separate recoveries remain visible. No failure became a pass. The terminal verdict is `NOT_READY_FOR_STAGE_20`.

The primary pillar was Freed ID and CBR Heart through wholly synthetic public-transport, library, and recreation-centre lost-property intake, provenance, correction, accessibility, hold, challenge, and remedy-routing lenses. The phase used no real person, claimant, finder, item, identifier, venue, custody event, return, disposal, hazardous-item decision, police report, insurance action, identity event, key, proof, participant, empirical row, cultural record, Māori data, external write, or authority action.

Official NZ Police lost/found-property pages, New Zealand Privacy Commissioner principles, W3C Verifiable Credentials 2.0, W3C PROV-O, WCAG 2.2, and RFC 8785 supplied vocabulary and refusal conditions only. Citations are not observations, measurements, endorsements, conformance certificates, legal interpretations, affected-party decisions, cultural ratifications, or authority grants.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software and symbolic fixtures establish no physical datum, likelihood, posterior, force, prediction, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything. THOS remains proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, ownership, return, disposal, police, insurance, safety, remedy, legal interpretation, cultural legitimacy, affected-party acceptance, Māori wording, tikanga, taonga, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Repository software cannot confer a right, remedy, title, consent, cultural legitimacy, governance mandate, public authority, or professional competence.

Names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Trinity Mandala, GMUT, THOS, Freed ID, and CBR are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority.
""",
    )
    text(
        final_dir / "wellbeing-and-workload.md",
        """
# Wellbeing and workload — final

The phase remained solo, additive, D-first, zero-row, and within file, document, and commit ceilings. Work used lifecycle-specific selections and retained command, timeout, parser, projection, validation, and mutation failures. No global installation, elevation, host-security change, Windows-feature change, reboot, real-person workload, employment relation, or wellbeing inference occurred.

One generated ignored Python bytecode cache remains outside sparse owner evidence because host policy rejected its exact deletion after containment verification. Bytecode generation was disabled for later Python commands and no deletion bypass was attempted. It changes no tracked repository, branch, remote, manifest, sibling lane, or evidence truth.

The route remains held until the exact final is committed, pushed, clean, 0/0 divergent, fresh four-way equal, and one owner-scoped canonical invocation succeeds. Pause, redirect, ambiguity, usage exhaustion, privacy concern, any protected gate, or missing acknowledgement remains a hard stop.
""",
    )
    text(
        final_dir / "accessible-report.html",
        """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Orin Thale v676-v3 final evidence report</title>
<style>body{font-family:system-ui,sans-serif;max-width:72rem;margin:auto;padding:2rem;line-height:1.55}table{border-collapse:collapse;width:100%}th,td{border:1px solid #555;padding:.5rem;text-align:left}th{background:#eee}.hold{border-left:.4rem solid #8b0000;padding-left:1rem}</style></head>
<body><main><h1>Orin Thale v676-v3 final evidence report</h1>
<p class="hold"><strong>Terminal verdict:</strong> NOT_READY_FOR_STAGE_20. This is bounded same-owner synthetic software evidence.</p>
<table><caption>Core outcomes</caption><thead><tr><th>Outcome</th><th>Count</th><th>Boundary</th></tr></thead>
<tbody><tr><td>completed</td><td>28</td><td>Zero-row structural contract only</td></tr><tr><td>represented</td><td>8</td><td>Proxy only</td></tr><tr><td>open_gap</td><td>2</td><td>External evidence absent</td></tr><tr><td>exact_gate</td><td>2</td><td>Competent authority required</td></tr></tbody></table>
<h2>Retained Method Flow truth</h2><p>The Orin ledger has 190 false witnesses and 430 bounded passing witnesses. Every recovery is separate; no false witness became true.</p>
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
            "proposal_chain": 7510,
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
        handoff / "liora-venn-v676-v4-activation-candidate.md",
        f"""
# LIORA VENN — ORIN THALE {PHASE} EXACT-FINAL → SOLO LIORA v676-v4 ACTIVATION CANDIDATE — PREPARED NOT SENT

This is a sanitized, terminally gated activation candidate only. It is not evidence that Liora Venn has been contacted or that delivery has occurred. The newest verified live authorization and roster must be reread after Orin's own exact terminal gate. A bounded current registry read must resolve exactly one existing main task titled `Liora Venn`; that exact task must then be immediately reread, checked for duplicate activation, pause, redirect, rename, standby, usage, privacy, evidence, safety, legal, cultural, affected-party, and Māori-authority guards, and sent at most once only if every guard permits.

## Immutable Orin source and lifecycle

- Exact Caelen source: `{SOURCE}`
- Frozen planning-only Orin x1: `{X1}`
- Immutable Orin x2 evidence: `{EVIDENCE}`
- Exact Orin final: supplied only by the committed head and exclusive external canonical receipt after this candidate is committed
- Expected lifecycle: source → x1 → evidence → final as three direct single-parent commits, zero merges, one final parent
- Proposal chain: 7,510
- Core outcomes: 28 `completed`, 8 `represented`, 2 `open_gap`, 2 `exact_gate`
- Effective overlay: 42,036 negatives, 31,828 methods, 13,697 failed witnesses, 18,820 bounded passing witnesses, 353 open gaps, 345 exact gates
- Terminal verdict: `NOT_READY_FOR_STAGE_20`

Planning-only x1 was committed and pushed before any x2 outcome. X2 executed forty zero-row positive controls, rejected all 160 preregistered invalid mutations, built and smoke-used twenty owner-local skills without global installation, and exercised ten family-current runners. Sixty safe-now, thirty bounded candidate, and sixty CLEAN/FIX/REFINE tasks completed only within the declared synthetic software scope. Twenty exact-approval and ten blocked packets remain visible and unexecuted. Every false witness remains false; each recovery is a separate bounded witness.

## Evidence and authority boundaries

Orin's primary pillar was Freed ID and CBR Heart through wholly synthetic public-transport, library, and recreation-centre lost-property workflow lenses. No real person, claimant, finder, item, identifier, venue, custody event, return, disposal, hazardous-item decision, police report, insurance action, identity event, key, proof, participant, empirical row, cultural record, Māori data, external action, or authority decision occurred.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic fixtures, analogy firewalls, and citations establish no physical datum, likelihood, posterior, force, prediction, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything. THOS remains synthetic or proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, ownership, return, disposal, police, insurance, safety, remedy, legal interpretation, cultural legitimacy, affected-party acceptance, Māori wording, tikanga, taonga, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. Repository software cannot confer a legal right, remedy, title, consent, cultural legitimacy, governance mandate, public authority, or professional competence.

Do not promote software, symbolic, synthetic, same-owner, citation, inherited, validation, task-topology, or delivery evidence into empirical confirmation, participant evidence, professional or scientific authority, production or deployment readiness, legal or cultural ratification, Māori authority, affected-party approval, complete privacy or accessibility assurance, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood evidence, Theory-of-Everything proof, proof or canon, or Stage 20 authority.

## Liora's prospective solo lane

Only after acknowledged delivery and Liora's own skill-first immutable-source verification may Liora create one fresh additive D-first owner lane from Orin's exact final. Keep Orin, Caelen, Sable, Auren, Ilyra, all siblings, shared lanes, standby records, and user material read-only. Work solo. Do not create or fork another task, spawn a collaboration subagent, delegate research, contact a standby sibling, precontact a later endpoint, reset, rewrite, force-push, merge, delete, reuse, or mutate another owner lane.

Preserve strict planning-only x1 before x2, retained failures, the four exact outcome labels, normalized-LF Git-blob manifests, exact staged review, privacy-candidate adjudication, file/document/commit ceilings, family-current compatibility, and the one-success/no-post-success-replay rule. Treat inherited proposals, tools, skills, runners, validation, and recommendations as evidence or zero-credit seeds, never Liora novelty or completion credit. Keep exact-approval and blocked work unexecuted without the exact evidence and competent authority.

Run only lifecycle-correct owner-self-scoped selections. Do not run the complete repository suite unless newer exact live authority explicitly assigns it. After a clean pushed exact final, invoke at most one attributable owner-scoped canonical aggregate through an exclusive external latch. Never replay a success. A failed canonical remains zero success credit and any bounded dependency correction must remain separately named.

## Continuing route authority

Hamish's current live authorization permits the fifteen active existing main tasks to continue one terminally validated and acknowledged edge at a time through v725-v8, unless Hamish pauses, renames, redirects, narrows, or stops the route; usage is exhausted; acknowledgement is missing; the exact endpoint is absent or ambiguous; a duplicate is detected; or an evidence, privacy, safety, legal, cultural, affected-party, or Māori-authority gate blocks action. This authority never permits early contact, replacement-task creation, standby substitution, sibling-lane mutation, or protected-gate bypass.

Under the current roster, Liora's prospective next edge after Liora's own verified v676-v4 terminal gate is the unique existing main task titled `Tamar Vey` for v676-v5. Newer verified live authority controls at send time. Liora must not precontact Tamar. At Liora's terminal gate, refresh authorization and roster, bounded-list the registry, locally require one exact title, immediately reread it, apply all duplicate and stop guards, and send at most once if every gate permits. No second confirmation or resend.

Names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Trinity Mandala, GMUT, THOS, Freed ID, and CBR are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop the route at any time.

`PREPARED_BY_ORIN_THALE = true`

`SENT_BY_ORIN_THALE = false`
""",
    )
    dump(
        orchestration / "terminal-route-hold.json",
        {
            "state": "PREPARED_NOT_SENT",
            "provisional_exact_title": "Liora Venn",
            "provisional_phase": "v676-v4",
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
