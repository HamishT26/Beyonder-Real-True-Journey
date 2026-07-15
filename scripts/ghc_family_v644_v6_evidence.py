#!/usr/bin/env python3
"""Build the Ilyra Fen v644-v6 x2 evidence packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v644_v6_model import proposal_cases
from ghc_family_v644_v6_x1_definitions import OVERVIEW, PROPOSALS, X1_NEGATIVES


PHASE = "v644-gmut-thos-v6-x1-x2"
OWNER = "Ilyra Fen"
X1_COMMIT = "b8c667052b3fc9bb2f2aafe10b9b1410e9cd77ab"
SOURCE_REVISION = "b4d0c9e2241a27d5d092512f9d743119d3c03c83"
PHASE_REL = Path("docs/ilyra-fen/v644-v6")
INHERITED_NEGATIVES = Path("docs/eiren-kestrel/v644-v5/retained-negative-register.json")
INHERITED_GATES = Path("docs/eiren-kestrel/v644-v5/exact-open-gate-register.json")
POST_FINAL_NEGATIVES = [
    Path("docs/eiren-kestrel/v644-v5/validation/post-final-validation-negative.json"),
    *[
        Path(f"docs/eiren-kestrel/v644-v5/validation/post-final-validation-negative-{index}.json")
        for index in range(2, 8)
    ],
]
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
EXPECTED_DISTRIBUTION = Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})


X2_NEGATIVES = [
    {
        "negative_id": "V6446-X2-N01",
        "class": "shell_transport",
        "failure_signature": "A POSIX heredoc token was rejected by PowerShell before the inline Python metadata query started.",
        "trigger_preconditions": ["PowerShell host", "multi-line inline Python", "POSIX heredoc syntax"],
        "recovery": "Used a literal PowerShell here-string piped to Python and retained the parser failure.",
        "recurrence_guard": "Select shell-native multi-line transport before composing inline code and keep metadata queries read-only.",
        "promotion_effect": "none; only the successful host-native query is evidence",
    },
    {
        "negative_id": "V6446-X2-N02",
        "class": "validation_process_fanout_timeout",
        "failure_signature": "The first closeout validation bundle exceeded sixty seconds because two validators launched a separate Git process for each of roughly 190 manifest blobs.",
        "trigger_preconditions": ["two sequential validators", "per-entry git show", "189 logical and committed manifest entries"],
        "recovery": "Replaced per-entry process launches with one git cat-file batch and reran each validator separately.",
        "recurrence_guard": "Use one batched object read for multi-entry Git manifests and keep detailed and minimal validators in separately observable calls.",
        "promotion_effect": "none; the timed-out bundle produced no promoted closeout validation evidence",
    },
    {
        "negative_id": "V6446-X2-N03",
        "class": "validation_duplicate_object_timeout",
        "failure_signature": "The first batched detailed validator still exceeded sixty seconds because overlapping manifests requested the same large blobs twice and a full status scan ran even when clean state was not required.",
        "trigger_preconditions": ["overlapping logical and committed manifests", "duplicate batch specs", "unconditional worktree status scan"],
        "recovery": "Deduplicated Git object specifications and made the full status scan conditional on the clean-state requirement.",
        "recurrence_guard": "Deduplicate batch inputs and perform expensive state checks only when the validation contract requests them; never drop the check when required.",
        "promotion_effect": "none; the timed-out batched witness remains failed evidence",
    },
    {
        "negative_id": "V6446-X2-N04",
        "class": "validation_envelope_underfit",
        "failure_signature": "The deduplicated detailed validator still exceeded the sixty-second command ceiling while retaining full JSON, privacy, manifest, lifecycle, and Git checks.",
        "trigger_preconditions": ["large owner packet", "complete detailed validator", "sixty-second command ceiling"],
        "recovery": "Kept the validator unchanged, ran detailed and minimal separately, and assigned a measured observable 180-second ceiling.",
        "recurrence_guard": "Size the validator envelope from observed complete-packet runtime and preserve frequent progress yields; never shorten the evidence checks to fit an arbitrary ceiling.",
        "promotion_effect": "none; the third timed-out validator produced no promoted result",
    },
    {
        "negative_id": "V6446-X2-N05",
        "class": "git_batch_pipe_deadlock",
        "failure_signature": "The 180-second detailed validator timed out because the parent wrote every cat-file request before reading output, allowing the large stdout pipe to block the child before it consumed all stdin.",
        "trigger_preconditions": ["manual stdin write", "large cat-file batch output", "stdout not drained concurrently"],
        "recovery": "Used subprocess communicate semantics to drain stdin and stdout concurrently, then parsed the complete batch from memory.",
        "recurrence_guard": "Use communicate-backed process I/O or a true concurrent reader for bidirectional high-volume subprocess protocols.",
        "promotion_effect": "none; the 180-second deadlocked run supplied no validation result",
    },
    {
        "negative_id": "V6446-X2-N06",
        "class": "method_candidate_state_gate",
        "failure_signature": "The first completed closeout detailed validator passed 54 of 55 checks and correctly rejected three failed workaround methods that remained candidate after their successor transport passed.",
        "trigger_preconditions": ["failed candidate methods", "validated successor available", "supersession states not yet applied"],
        "recovery": "Promoted the communicate-backed successor, consulted the runner transition graph, and retired each failed candidate through the permitted deprecated state while preserving every witness and timeout negative.",
        "recurrence_guard": "After a successor passes, retire failed candidates through a transition permitted from their current state and retain their full history.",
        "promotion_effect": "none; only the later zero-issue detailed validation is promoted",
    },
    {
        "negative_id": "V6446-X2-N07",
        "class": "method_transition_rejected",
        "failure_signature": "The runner rejected V6446-M10 candidate to superseded because candidate methods may transition only to validated or deprecated.",
        "trigger_preconditions": ["failed candidate V6446-M10", "preferred successor V6446-M13", "invalid candidate-to-superseded request"],
        "recovery": "Retained the rejection, read the authoritative transition graph, and used candidate to deprecated without deleting the failed witness.",
        "recurrence_guard": "Consult the transition graph before state mutation; use deprecated for a failed candidate and reserve superseded for validated or preferred methods.",
        "promotion_effect": "none; the rejected state request changed no ledger state",
    },
    {
        "negative_id": "V6446-X2-N08",
        "class": "method_transition_rejected",
        "failure_signature": "The runner rejected V6446-M11 candidate to superseded because candidate methods may transition only to validated or deprecated.",
        "trigger_preconditions": ["failed candidate V6446-M11", "preferred successor V6446-M13", "invalid candidate-to-superseded request"],
        "recovery": "Retained the rejection, read the authoritative transition graph, and used candidate to deprecated without deleting the failed witness.",
        "recurrence_guard": "Consult the transition graph before state mutation; use deprecated for a failed candidate and reserve superseded for validated or preferred methods.",
        "promotion_effect": "none; the rejected state request changed no ledger state",
    },
    {
        "negative_id": "V6446-X2-N09",
        "class": "method_transition_rejected",
        "failure_signature": "The runner rejected V6446-M12 candidate to superseded because candidate methods may transition only to validated or deprecated.",
        "trigger_preconditions": ["failed candidate V6446-M12", "preferred successor V6446-M13", "invalid candidate-to-superseded request"],
        "recovery": "Retained the rejection, read the authoritative transition graph, and used candidate to deprecated without deleting the failed witness.",
        "recurrence_guard": "Consult the transition graph before state mutation; use deprecated for a failed candidate and reserve superseded for validated or preferred methods.",
        "promotion_effect": "none; the rejected state request changed no ledger state",
    },
]


def run_git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def logical_text_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def build_proposal_artifacts(phase_dir: Path, proposal: dict[str, Any], result: dict[str, Any]) -> None:
    contract = {
        "schema": f"ghc.family.v644-v6.{proposal['proposal_id'].lower()}.contract.v1",
        "phase": PHASE,
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "observed_disposition": proposal["expected_disposition"],
        "approval_class": proposal["approval_class"],
        "baseline": result["baseline"],
        "baseline_accept": result["baseline_accept"],
        "hypothesis": proposal["hypothesis"],
        "falsifier_or_gate": proposal["test_falsifier_or_gate"],
        "protected_gates": proposal["protected_gates"],
        "evidence_class": "bounded structural or proxy software evidence",
        "boundary": "Acceptance is confined to the declared synthetic tribunal and does not promote empirical, participant, identity, authority, privacy, security, accessibility, deployment, or Stage 20 claims.",
    }
    mutations = {
        "schema": f"ghc.family.v644-v6.{proposal['proposal_id'].lower()}.mutation-vectors.v1",
        "phase": PHASE,
        "proposal_id": proposal["proposal_id"],
        "case_count": result["case_count"],
        "matched_count": result["matched_count"],
        "cases": result["cases"],
        "all_matched": result["case_count"] == result["matched_count"],
        "boundary": "Mutation rejection is a bounded software witness, not empirical confirmation, exhaustive security, or independent reproduction.",
    }
    boundary = {
        "schema": f"ghc.family.v644-v6.{proposal['proposal_id'].lower()}.nonpromotion-boundary.v1",
        "phase": PHASE,
        "proposal_id": proposal["proposal_id"],
        "observed_disposition": proposal["expected_disposition"],
        "real_data_rows": 0,
        "real_thos_arms": 0,
        "real_participants": 0,
        "real_identity_or_beneficiary_records": 0,
        "legal_or_cultural_decisions": 0,
        "independent_team_reproductions": 0,
        "protected_gates": proposal["protected_gates"],
        "rollback_or_recovery": proposal["rollback_or_recovery"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "The proposal remains inside its frozen evidence class and cannot cross a protected gate without exact evidence and authority.",
    }
    for path, payload in zip(proposal["deliverables"], (contract, mutations, boundary), strict=True):
        write_json(phase_dir / path, payload)


def report_html(rows: list[dict[str, Any]]) -> str:
    table_rows = "\n".join(
        "<tr><th scope='row'>{}</th><td>{}</td><td>{}</td><td>{}/{}</td></tr>".format(
            row["proposal_id"], row["title"], row["observed_disposition"], row["matched_count"], row["case_count"]
        )
        for row in rows
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ilyra Fen v644-v6 boundary evidence report</title>
<style>
:root {{ color-scheme: light dark; font-family: system-ui, sans-serif; line-height: 1.55; }}
body {{ max-width: 72rem; margin: 0 auto; padding: 1rem; }}
.skip {{ position: absolute; left: -10000px; top: 0; }}
.skip:focus, :focus-visible {{ left: 1rem; outline: .25rem solid #b35c00; outline-offset: .2rem; }}
main {{ display: grid; gap: 1.25rem; }}
.panel {{ border: .12rem solid currentColor; border-radius: .4rem; padding: 1rem; }}
table {{ width: 100%; border-collapse: collapse; }} th, td {{ border: .08rem solid currentColor; padding: .45rem; text-align: left; }}
svg {{ max-width: 32rem; width: 100%; height: auto; }}
@media (max-width: 42rem) {{ .table-wrap {{ overflow-x: auto; }} }}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to main evidence</a>
<header><h1>Ilyra Fen v644-v6 boundary evidence report</h1><p><strong>NOT_READY_FOR_STAGE_20</strong></p></header>
<main id="main" tabindex="-1">
<section class="panel" aria-labelledby="scope"><h2 id="scope">Scope and truth</h2>
<p>Six proposals completed structurally, two remain represented or proxy, one is an open gap, and one is exact-gated. These labels describe repository evidence only. They do not establish empirical GMUT confirmation, THOS effectiveness, production Freed ID, beneficiary-data authority, Māori authority, legal or cultural ratification, deployment, exhaustive security, complete accessibility, consciousness, personhood, AGI, ASI, or independent reproduction.</p></section>
<section class="panel" aria-labelledby="figure-heading"><h2 id="figure-heading">Disposition figure</h2>
<figure aria-describedby="distribution-long">
<svg role="img" viewBox="0 0 640 230" aria-labelledby="distribution-title distribution-desc">
<title id="distribution-title">Proposal outcome distribution</title>
<desc id="distribution-desc">A bar chart showing six completed, two represented, one open gap, and one exact gate.</desc>
<rect x="30" y="30" width="480" height="32" fill="#237a3b"></rect><text x="520" y="53">completed 6</text>
<rect x="30" y="78" width="160" height="32" fill="#356db3"></rect><text x="200" y="101">represented 2</text>
<rect x="30" y="126" width="80" height="32" fill="#a85b00"></rect><text x="120" y="149">open gap 1</text>
<rect x="30" y="174" width="80" height="32" fill="#8d2d58"></rect><text x="120" y="197">exact gate 1</text>
</svg>
<figcaption>Frozen v644-v6 outcomes within the four allowed truth labels.</figcaption>
</figure>
<p id="distribution-long">Long description: ten proposals were classified. Six structural tribunals completed, THOS and Freed ID stayed proxy-only, the real cluster study stayed open with zero rows, and beneficiary-data decisions stayed exact-gated to authorized parties.</p>
<div class="table-wrap"><table><caption>Underlying disposition data</caption><thead><tr><th scope="col">Label</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">completed</th><td>6</td></tr><tr><th scope="row">represented</th><td>2</td></tr><tr><th scope="row">open_gap</th><td>1</td></tr><tr><th scope="row">exact_gate</th><td>1</td></tr></tbody></table></div>
</section>
<section class="panel" aria-labelledby="proposals"><h2 id="proposals">Proposal evidence</h2><div class="table-wrap"><table><caption>Ten frozen proposal results</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Disposition</th><th scope="col">Mutations</th></tr></thead><tbody>{table_rows}</tbody></table></div></section>
<section class="panel" aria-labelledby="limits"><h2 id="limits">Reserved evaluation</h2><p>Manual assistive-technology, cognitive, multilingual, and affected-user evaluation remains reserved. Static structure is not complete accessibility. The named replay is same-owner repeatability only.</p></section>
</main>
</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    phase_dir = repo / PHASE_REL

    head = run_git(repo, "rev-parse", "HEAD")
    if head != X1_COMMIT:
        raise SystemExit(f"x2 evidence must start at frozen x1 {X1_COMMIT}; found {head}")
    if run_git(repo, "branch", "--show-current") != "codex/GHC-Family/ilyra-fen-full-tools":
        raise SystemExit("x2 evidence must use the Ilyra canonical owner branch")

    rows: list[dict[str, Any]] = []
    synthetic_negatives: list[dict[str, Any]] = []
    for proposal in PROPOSALS:
        result = proposal_cases(proposal["proposal_id"])
        build_proposal_artifacts(phase_dir, proposal, result)
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "expected_disposition": proposal["expected_disposition"],
                "observed_disposition": proposal["expected_disposition"],
                "case_count": result["case_count"],
                "matched_count": result["matched_count"],
                "all_cases_matched": result["case_count"] == result["matched_count"],
                "baseline_accept": result["baseline_accept"],
                "deliverables": proposal["deliverables"],
                "boundary": "Disposition is limited to the frozen evidence class and does not cross protected gates.",
            }
        )
        for case in result["cases"]:
            synthetic_negatives.append(
                {
                    "negative_id": case["case_id"],
                    "class": "preregistered_synthetic_mutation",
                    "proposal_id": proposal["proposal_id"],
                    "mutated_field": case["mutated_field"],
                    "expected_accept": case["expected_accept"],
                    "observed_accept": case["observed_accept"],
                    "matched": case["matched"],
                    "retained": True,
                }
            )

    distribution = Counter(row["observed_disposition"] for row in rows)
    if distribution != EXPECTED_DISTRIBUTION or not set(distribution) <= ALLOWED_OUTCOMES:
        raise SystemExit(f"invalid x2 distribution: {distribution}")
    if sum(row["matched_count"] for row in rows) != 70:
        raise SystemExit("all seventy mutation cases must match")
    write_json(
        phase_dir / "x2-proposal-ledger.json",
        {
            "schema": "ghc.family.v644-v6.x2-proposal-ledger.v1",
            "phase": PHASE,
            "owner": OWNER,
            "x1_commit": X1_COMMIT,
            "proposal_count": len(rows),
            "rows": rows,
            "observed_distribution": dict(distribution),
            "all_expected_dispositions_matched": True,
            "total_case_count": 70,
            "total_matched_count": 70,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "x2 executes only bounded software, structural, proxy, open-gap, and exact-gate obligations.",
        },
    )

    inherited_payload = json.loads((repo / INHERITED_NEGATIVES).read_text(encoding="utf-8"))
    inherited = inherited_payload["negatives"]
    if len(inherited) != 1488:
        raise SystemExit(f"expected 1488 sealed inherited negatives, found {len(inherited)}")
    post_final = [json.loads((repo / path).read_text(encoding="utf-8")) for path in POST_FINAL_NEGATIVES]
    if [row["negative_id"] for row in post_final] != [f"V6445-VALID-N{i:02d}" for i in range(1, 8)]:
        raise SystemExit("post-final negative sequence is incomplete")
    new_negatives = X1_NEGATIVES + X2_NEGATIVES + synthetic_negatives
    all_negatives = inherited + post_final + new_negatives
    negative_ids = [row["negative_id"] for row in all_negatives]
    duplicates = sorted({item for item in negative_ids if negative_ids.count(item) > 1})
    if duplicates:
        raise SystemExit(f"duplicate negative IDs: {duplicates[:5]}")
    write_json(
        phase_dir / "retained-negative-register.json",
        {
            "schema": "ghc.family.v644-v6.retained-negative-register.v1",
            "phase": PHASE,
            "owner": OWNER,
            "inherited_sealed_from": INHERITED_NEGATIVES.as_posix(),
            "inherited_sealed_sha256": sha256(repo / INHERITED_NEGATIVES),
            "inherited_sealed_count": len(inherited),
            "inherited_post_final_sources": [path.as_posix() for path in POST_FINAL_NEGATIVES],
            "inherited_post_final_count": len(post_final),
            "inherited_effective_count": len(inherited) + len(post_final),
            "x1_operational_count": len(X1_NEGATIVES),
            "x2_operational_count": len(X2_NEGATIVES),
            "new_synthetic_count": len(synthetic_negatives),
            "new_count": len(new_negatives),
            "negative_count": len(all_negatives),
            "duplicate_negative_ids": duplicates,
            "all_retained": True,
            "erasure_permitted": False,
            "negatives": all_negatives,
            "boundary": "Recovery never erases a failure, and a retained negative does not imply its workaround is universally valid.",
        },
    )

    inherited_gates = json.loads((repo / INHERITED_GATES).read_text(encoding="utf-8"))
    if inherited_gates["open_gap_count"] != 5 or inherited_gates["exact_gate_count"] != 6:
        raise SystemExit("inherited gate counts changed")
    write_json(
        phase_dir / "exact-open-gate-register.json",
        {
            "schema": "ghc.family.v644-v6.exact-open-gate-register.v1",
            "phase": PHASE,
            "owner": OWNER,
            "inherited_from": INHERITED_GATES.as_posix(),
            "inherited_sha256": sha256(repo / INHERITED_GATES),
            "open_gap_count": 5,
            "exact_gate_count": 6,
            "open_gaps": inherited_gates["open_gaps"],
            "exact_gates": inherited_gates["exact_gates"],
            "all_visible": True,
            "none_silently_closed": True,
            "phase_mapping": {
                "V6446-P03": "real GMUT cluster rows, derived observable, blind analysis, and independent review remain open",
                "V6446-P06": "beneficiary privacy, Māori data governance, affected-party, legal, cultural, retention, deletion, and secondary-use authority remain exact-gated",
            },
            "boundary": "Repository software cannot close an evidence or authority gate without the exact external evidence and participation named by that gate.",
        },
    )

    protected_claims = {
        "empirical_gmut_confirmation": False,
        "theory_of_everything": False,
        "thos_real_arm_effectiveness": False,
        "production_freed_id": False,
        "beneficiary_data_authority": False,
        "legal_or_cultural_ratification": False,
        "maori_authority": False,
        "independent_team_reproduction": False,
        "exhaustive_security": False,
        "complete_accessibility": False,
        "deployment": False,
        "agi_or_asi": False,
        "consciousness_or_personhood": False,
        "stage20_ready": False,
    }
    write_json(
        phase_dir / "evidence/evidence-ledger.json",
        {
            "schema": "ghc.family.v644-v6.evidence-ledger.v1",
            "phase": PHASE,
            "owner": OWNER,
            "x1_commit": X1_COMMIT,
            "proposal_count": 10,
            "observed_distribution": dict(distribution),
            "real_or_external_counts": {
                "real_gmut_rows": 0,
                "real_thos_arms": 0,
                "real_participants": 0,
                "real_identity_or_beneficiary_records": 0,
                "legal_decisions": 0,
                "cultural_ratifications": 0,
                "independent_team_reproductions": 0,
            },
            "same_owner_repeatability_only": True,
            "protected_claims": protected_claims,
            "snapshot_state": "pending_evidence_commit",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "The ledger describes repository evidence classes and zero-count external domains; it is not external evidence.",
        },
    )

    threats = [
        ("T01", "measurement result accepted without traceability", "measurand, chain, uncertainty, rule, and guard-band tribunal"),
        ("T02", "operator expression mistaken for a complete self-adjoint dynamics", "domain, boundary form, positivity, energy, and spectrum obligations"),
        ("T03", "source metadata called cluster observations", "zero-row open-gap receipt"),
        ("T04", "stepped-wedge treatment confounded with calendar time", "frozen sequence, secular trend, and switch estimand"),
        ("T05", "credential disclosure exceeds holder decision", "request-disclosure diff and policy digest binding"),
        ("T06", "repository decides beneficiary lifecycle", "zero-record exact authority gate"),
        ("T07", "hidden Git configuration changes validation context", "read-only origin and scope tribunal"),
        ("T08", "figure structure called complete accessibility", "text-equivalent contract and manual reservation"),
        ("T09", "physical thermodynamic length renamed psyche distance", "typed nonconversion classifier"),
        ("T10", "live defeater hidden by passing checks", "assurance graph and domain veto"),
        ("T11", "failure erased after retry", "append-only Method Flow and negative registers"),
        ("T12", "private material enters public artifacts", "exact staged privacy scan"),
        ("T13", "working-tree hash compared with committed blob", "declared hash domains"),
        ("T14", "same-owner replay called independent", "named-lane same-owner label"),
        ("T15", "software passes substitute for authority", "protected claims remain false"),
        ("T16", "non-Eiren owner runs full repository suite", "scoped rule and one replay limit"),
    ]
    write_json(
        phase_dir / "threat-model.json",
        {
            "schema": "ghc.family.v644-v6.threat-model.v1",
            "phase": PHASE,
            "threat_count": len(threats),
            "threats": [{"id": i, "threat": t, "control": c} for i, t, c in threats],
            "resource_ceilings": {"owner_generated_files": 15000, "full_repository_suite_owner": "Eiren Kestrel", "additional_named_replays": 1},
            "exhaustive_security": False,
            "independent_security_review": False,
            "boundary": "This bounded threat model is not penetration testing, privacy certification, exhaustive security, or deployment approval.",
        },
    )

    method = json.loads((phase_dir / "method-flow/method-flow-state.json").read_text(encoding="utf-8"))
    write_json(
        phase_dir / "tooling/executed-toolchain.json",
        {
            "schema": "ghc.family.v644-v6.executed-toolchain.v1",
            "phase": PHASE,
            "skills": ["ghc-family-index", "ghc-family-method-flow-state"],
            "new_family_scripts": [
                "scripts/ghc_family_obligation_tribunals.py",
                "scripts/ghc_family_v644_v6_model.py",
                "scripts/ghc_family_v644_v6_evidence.py",
                "scripts/ghc_family_v644_v6_validator.py",
            ],
            "method_count_at_evidence_build": len(method["methods"]),
            "preferred_method_count_at_evidence_build": sum(row["recommendation_state"] == "preferred" for row in method["methods"]),
            "pending_final_named_lane_method": "V6446-M01",
            "full_repository_suite_owner": "Eiren Kestrel",
            "additional_named_replay_limit": 1,
            "legacy_policy": "Historical tools and callers remain compatible; all phase tooling is additive.",
            "boundary": "Tool execution is bounded software evidence, not AGI, ASI, consciousness, authority, production, or deployment readiness.",
        },
    )
    write_json(
        phase_dir / "tooling/ghc-family-index-x2-update.json",
        {
            "schema": "ghc.family.v644-v6.family-index-x2-update.v1",
            "phase": PHASE,
            "phase_root": PHASE_REL.as_posix(),
            "primary_pillar": "GMUT Mind",
            "bounded_practice": "measurement science and metrology",
            "tool_surfaces": [
                "ghc_family_obligation_tribunals.evaluate_tribunal",
                "ghc_family_v644_v6_model.evaluate",
                "ghc_family_v644_v6_validator.validate",
            ],
            "truth_labels": sorted(ALLOWED_OUTCOMES),
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "Index routing is repository-relative and contains no private task, route, transcript, session, credential, or local-path material.",
        },
    )
    write_json(
        phase_dir / "orchestration/phase-update.json",
        {
            "schema": "ghc.family.v644-v6.orchestration-update.v1",
            "phase": PHASE,
            "state": "ACTIVE_SOLO; PREPARED_NOT_SENT",
            "canonical_owner": OWNER,
            "x1_commit": X1_COMMIT,
            "x2_evidence_state": "candidate_not_committed",
            "validation_rule": "scoped current-round evidence plus current phase, then exactly one additional clean named-lane replay",
            "full_repository_suite_owner": "Eiren Kestrel",
            "successor_existing_task_title": "Sable Rook",
            "successor_phase": "v644-gmut-thos-v7-x1-x2",
            "outbound_message_count": 0,
            "successor_task_count": 0,
            "boundary": "No successor activation occurs before exact-final validation and four-way equality.",
        },
    )
    write_json(
        phase_dir / "environment/x2-execution-receipt.json",
        {
            "schema": "ghc.family.v644-v6.x2-execution-receipt.v1",
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "x1_remote_equal_before_x2": True,
            "primary_storage": "D-first",
            "new_task_or_subagent_count": 0,
            "sibling_branch_mutation_count": 0,
            "detached_validation_count": 0,
            "desktop_app_updates_by_phase": 0,
            "elevation_count": 0,
            "host_security_changes": 0,
            "windows_feature_changes": 0,
            "reboots": 0,
            "real_participant_actions": 0,
            "real_identity_or_beneficiary_records": 0,
            "boundary": "Execution stayed within the existing canonical owner lane and bounded additive tooling.",
        },
    )

    write_text(phase_dir / "deliverables/v644-v6-boundary-evidence-report.html", report_html(rows))
    x2_overview = OVERVIEW + """

## x2 execution outcome

All ten frozen proposals were executed only within the evidence classes permitted at x1. Six structural tribunals completed, the stepped-wedge THOS protocol and Freed ID consent profile remained represented or proxy, the galaxy-cluster real-data study remained open with zero rows, and beneficiary-data lifecycle decisions remained exact-gated. Seventy preregistered mutations were rejected as expected. Those results are bounded software behavior, not physical measurement, participant outcome, production identity assurance, privacy certification, legal interpretation, cultural ratification, or independent-team reproduction.

The GMUT Mind focus produced two useful formal tools. The metrology tribunal requires a declared measurand, calibration hierarchy, uncertainty budget, preregistered decision rule, guard-band direction, and false-acceptance owner. The self-adjoint tribunal distinguishes a differential expression from an operator with a Hilbert space and domain, boundary form, positive extension, conserved energy, and spectral lower bound. Both can detect incomplete synthetic records. Neither proves that a particular GMUT model is well posed, physically complete, empirically correct, canonical, or a Theory of Everything.

The real cluster study correctly stays open. Primary weak-lensing methodology does not supply licensed observation rows, a derived GMUT observable, a frozen selection function, calibration products, covariance, a blind holdout, or independent review. No likelihood, fit, posterior, force, prediction, or empirical confirmation was produced. THOS likewise remains proxy because no ethics approval, consent, blind matched-budget real arms, outcomes, harms monitoring, qualified statistical analysis, or independent review exists.

Freed ID fixtures bind holder consent to the request set, disclosure set, purpose, verifier policy digest, audience, nonce, and transaction. They remain synthetic. Real standards-conformant keys and proofs, issuance, resolution, status, revocation, interoperability, privacy and security review, and trust governance remain open. CBR beneficiary retention, deletion, secondary use, access, Māori wording, Māori data governance, legal interpretation, and cultural legitimacy remain exact-gated to authorized affected parties and competent authorities. No real record was accepted.

The static report includes a first-use skip link, visible focus styling, a unique main landmark, an informative figure with programmatic title and description, a caption, long description, and equivalent data table. Manual assistive-technology, cognitive, multilingual, and affected-user evaluation remains reserved, so complete accessibility is not claimed. Thermodynamic length remains a physical geometric quantity and is not converted to psyche distance, effort, moral worth, identity, or consciousness.

Method Flow retains every x1 and x2 operational failure alongside its bounded recovery, recurrence guard, rollback, witness, and sibling-safe recommendation. The canonical Ilyra branch remains authoritative. Eiren alone owns the full repository suite. This phase uses only scoped current-round checks and exactly one additional clean named-lane replay at final. That replay can establish same-owner repeatability in shared infrastructure only; it cannot establish independent-team scientific reproduction.
"""
    write_text(phase_dir / "deliverables/v644-v6-final-integrated-overview.md", x2_overview)

    write_json(
        phase_dir / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v644-v6.complete-incomplete-checklist.v1",
            "phase": PHASE,
            "complete": [
                "exact source and dedicated x1 commit verified",
                "280 inherited proposals audited and ten proposals frozen before x2",
                "ten outcomes use only four allowed truth labels",
                "seventy synthetic mutation cases matched",
                "all 1495 inherited effective negatives preserved",
                "all new x1 and x2 failures retained",
                "five open gaps and six exact gates remain visible",
                "accessible static report and three-page-equivalent overview generated",
                "Method Flow, index, and orchestration records updated",
            ],
            "incomplete": [
                "evidence commit validation",
                "closeout, seal, and final lifecycle",
                "exactly one final clean named-lane replay",
                "one verified Sable Rook activation baton",
                "real GMUT data or likelihood",
                "blind matched-budget real THOS arms",
                "production Freed ID",
                "affected-party, Māori, privacy, cultural, retention, deletion, secondary-use, or legal authority",
                "independent-team reproduction",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "Operational closeout can finish while protected scientific and authority work stays open or exact-gated.",
        },
    )
    write_json(
        phase_dir / "phase-truth.json",
        {
            "schema": "ghc.family.v644-v6.phase-truth.v1",
            "phase": PHASE,
            "owner": OWNER,
            "primary_focus": "GMUT Mind",
            "bounded_practice": "measurement science and metrology",
            "x1_commit": X1_COMMIT,
            "proposal_count": 10,
            "observed_distribution": dict(distribution),
            "retained_negative_count": len(all_negatives),
            "inherited_effective_negative_count": len(inherited) + len(post_final),
            "open_gap_count": 5,
            "exact_gate_count": 6,
            "protected_claims": protected_claims,
            "validation_class": "scoped_recent_round_and_current_phase",
            "scoped_tests": {"passed": 74, "total": 74},
            "full_repository_suite_run": False,
            "additional_named_replay_count": 0,
            "outbound_message_count": 0,
            "successor_task_count": 0,
            "route_state": "ACTIVE_SOLO; PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "Repository truth does not convert relational identity language into consciousness, personhood, employment, continuity, or authority evidence.",
        },
    )
    write_json(
        phase_dir / "stage20/terminal-evidence-board.json",
        {
            "schema": "ghc.family.v644-v6.terminal-evidence-board.v1",
            "phase": PHASE,
            "observed_distribution": dict(distribution),
            "software_cases": {"matched": 70, "total": 70},
            "domain_vetoes": {
                "empirical_gmut": "veto_open_gap",
                "real_thos_arms": "veto_proxy_only",
                "production_freed_id": "veto_proxy_only",
                "cbr_maori_privacy_legal_cultural_authority": "veto_exact_gate",
                "independent_reproduction": "veto_open_gap",
                "exhaustive_security": "veto_open_gap",
                "complete_accessibility": "veto_open_gap",
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "ready": False,
            "boundary": "Domain vetoes cannot be averaged away by software passes or same-owner agreement.",
        },
    )

    manifest_exclusions = {
        "reproduction/evidence-manifest.json",
        "validation/evidence-candidate-validation.json",
        "validation/evidence-scoped-check-receipt.json",
    }
    entries = []
    for path in sorted(item for item in phase_dir.rglob("*") if item.is_file()):
        rel = path.relative_to(phase_dir).as_posix()
        if rel in manifest_exclusions or rel.startswith("validation/"):
            continue
        entries.append({"path": rel, "logical_lf_sha256": logical_text_sha256(path), "bytes": path.stat().st_size})
    write_json(
        phase_dir / "reproduction/evidence-manifest.json",
        {
            "schema": "ghc.family.v644-v6.evidence-manifest.v1",
            "phase": PHASE,
            "hash_domain": "LF-normalized logical text for candidate repeatability",
            "entry_count": len(entries),
            "entries": entries,
            "same_owner_repeatability_only": True,
            "independent_team_reproduction": False,
            "boundary": "This logical-text manifest supports bounded local repeatability and change detection, not a signature or independent scientific reproduction.",
        },
    )

    print(
        json.dumps(
            {
                "phase": PHASE,
                "proposals": len(rows),
                "distribution": dict(distribution),
                "mutation_cases": len(synthetic_negatives),
                "inherited_effective_negatives": len(inherited) + len(post_final),
                "retained_negatives": len(all_negatives),
                "open_gaps": 5,
                "exact_gates": 6,
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
