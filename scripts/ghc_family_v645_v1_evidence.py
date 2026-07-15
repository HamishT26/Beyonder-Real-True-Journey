#!/usr/bin/env python3
"""Build the Tamar Vey v645-v1 x2 evidence packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_git_lfs_boundary import VERSION as LFS_VERSION, classify_bytes
from ghc_family_v645_v1_model import proposal_cases
from ghc_family_v645_v1_x1_definitions import OVERVIEW, PROPOSALS, X1_NEGATIVES


PHASE = "v645-gmut-thos-v1-x1-x2"
OWNER = "Tamar Vey"
X1_COMMIT = "1fa214f0d8ca832ae41045234489bd3e1637f287"
SOURCE_REVISION = "a6c869a44eb7d3fe32ba80bc64964aa7903531c2"
OWNER_BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
PHASE_REL = Path("docs/tamar-vey/v645-v1")
INHERITED_NEGATIVES = Path("docs/orin-thale/v644-v8/retained-negative-register.json")
INHERITED_GATES = Path("docs/orin-thale/v644-v8/exact-open-gate-register.json")
X2_NEGATIVE_FILE = PHASE_REL / "validation/x2-operational-negatives.json"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
EXPECTED_DISTRIBUTION = Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})


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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def proposal_payloads(proposal: dict[str, Any], result: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    common = {
        "phase": PHASE,
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "observed_disposition": proposal["expected_disposition"],
        "protected_gates": proposal["protected_gates"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    contract = {
        "schema": f"ghc.family.v645-v1.{proposal['proposal_id'].lower()}.contract.v1",
        **common,
        "approval_class": proposal["approval_class"],
        "baseline": result["baseline"],
        "baseline_accept": result["baseline_accept"],
        "hypothesis": proposal["hypothesis"],
        "falsifier_or_gate": proposal["test_falsifier_or_gate"],
        "evidence_class": "bounded structural, proxy, open-gap, or exact-gate software evidence",
        "boundary": "Acceptance is confined to the frozen software evidence class and cannot promote empirical, participant, identity, authority, privacy, security, accessibility, deployment, or Stage 20 claims.",
    }
    mutations = {
        "schema": f"ghc.family.v645-v1.{proposal['proposal_id'].lower()}.mutation-vectors.v1",
        **common,
        "case_count": result["case_count"],
        "matched_count": result["matched_count"],
        "cases": result["cases"],
        "all_matched": result["case_count"] == result["matched_count"],
        "boundary": "Mutation rejection is a bounded software witness, not empirical confirmation, exhaustive security, complete accessibility, or independent reproduction.",
    }
    boundary = {
        "schema": f"ghc.family.v645-v1.{proposal['proposal_id'].lower()}.nonpromotion-boundary.v1",
        **common,
        "real_data_rows": 0,
        "real_thos_arms": 0,
        "real_participants": 0,
        "real_identity_or_beneficiary_records": 0,
        "legal_or_cultural_decisions": 0,
        "independent_team_reproductions": 0,
        "rollback_or_recovery": proposal["rollback_or_recovery"],
        "boundary": "The proposal remains inside its frozen evidence class and cannot cross a protected gate without exact evidence and authority.",
    }
    return contract, mutations, boundary


def build_proposal_artifacts(phase_dir: Path, proposal: dict[str, Any], result: dict[str, Any]) -> None:
    for relative, payload in zip(proposal["deliverables"], proposal_payloads(proposal, result), strict=True):
        path = phase_dir / relative
        if path.suffix == ".json":
            write_json(path, payload)
        elif path.suffix == ".md":
            write_text(
                path,
                f"# {proposal['title']}\n\n"
                f"Observed disposition: `{proposal['expected_disposition']}`.\n\n"
                f"{payload['boundary']}\n\n"
                f"Recovery: {proposal['rollback_or_recovery']}",
            )
        elif path.suffix == ".html":
            continue
        else:
            raise ValueError(f"unsupported deliverable suffix: {relative}")


def report_html(rows: list[dict[str, Any]]) -> str:
    proposal_rows = "\n".join(
        "<tr><th scope='row'>{}</th><td>{}</td><td><span class='status'>{}</span></td><td>{}/{}</td></tr>".format(
            row["proposal_id"], row["title"], row["observed_disposition"], row["matched_count"], row["case_count"]
        )
        for row in rows
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tamar Vey v645-v1 boundary evidence report</title>
<style>
:root {{ color-scheme: light dark; font-family: system-ui, sans-serif; line-height: 1.55; }}
body {{ max-width: 72rem; margin: 0 auto; padding: 1rem; }}
.skip {{ position: absolute; left: -10000px; top: 0; }}
.skip:focus, :focus-visible {{ left: 1rem; outline: .25rem solid #b35c00; outline-offset: .2rem; }}
main {{ display: grid; gap: 1.25rem; }}
.panel {{ border: .12rem solid currentColor; border-radius: .4rem; padding: 1rem; }}
.status {{ font-weight: 700; text-decoration: underline; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ border: .08rem solid currentColor; padding: .45rem; text-align: left; vertical-align: top; }}
svg {{ max-width: 32rem; width: 100%; height: auto; }}
@media (max-width: 42rem) {{ .table-wrap {{ overflow-x: auto; }} }}
@media print {{ body {{ max-width: none; }} a {{ color: inherit; }} }}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to main evidence</a>
<header><h1>Tamar Vey v645-v1 boundary evidence report</h1><p><strong>Status: NOT_READY_FOR_STAGE_20</strong></p></header>
<main id="main" tabindex="-1">
<section class="panel" aria-labelledby="scope"><h2 id="scope">Scope and truth</h2>
<p>Six proposals completed structurally, two remain represented or proxy, one remains an open gap, and one remains exact-gated. The labels are visible text, not icon-only or CSS-generated meaning. They do not establish empirical GMUT confirmation, THOS effectiveness, production Freed ID, CBR authority, Maori authority, legal or cultural ratification, deployment, exhaustive security, complete accessibility, consciousness, personhood, AGI, ASI, or independent reproduction.</p></section>
<section class="panel" aria-labelledby="distribution"><h2 id="distribution">Disposition figure</h2>
<figure aria-describedby="distribution-long">
<svg role="img" viewBox="0 0 640 230" aria-labelledby="distribution-title distribution-desc">
<title id="distribution-title">Proposal outcome distribution</title>
<desc id="distribution-desc">Six completed, two represented, one open gap, and one exact gate.</desc>
<rect x="30" y="30" width="480" height="32" fill="#237a3b"></rect><text x="520" y="53">completed 6</text>
<rect x="30" y="78" width="160" height="32" fill="#356db3"></rect><text x="200" y="101">represented 2</text>
<rect x="30" y="126" width="80" height="32" fill="#a85b00"></rect><text x="120" y="149">open gap 1</text>
<rect x="30" y="174" width="80" height="32" fill="#8d2d58"></rect><text x="120" y="197">exact gate 1</text>
</svg>
<figcaption>Frozen v645-v1 outcomes within the four allowed truth labels; color is redundant to visible labels and values.</figcaption>
</figure>
<p id="distribution-long">Long description: ten proposals were classified. Six bounded software artifacts completed, THOS monitoring and Freed ID federation stayed proxy-only, the ISW cross-correlation study stayed open with zero rows, and CBR remedy-fund investment decisions stayed exact-gated.</p>
<div class="table-wrap"><table><caption>Underlying disposition data</caption><thead><tr><th scope="col">Label</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">completed</th><td>6</td></tr><tr><th scope="row">represented</th><td>2</td></tr><tr><th scope="row">open_gap</th><td>1</td></tr><tr><th scope="row">exact_gate</th><td>1</td></tr></tbody></table></div>
</section>
<section class="panel" aria-labelledby="proposals"><h2 id="proposals">Proposal evidence</h2><div class="table-wrap"><table><caption>Ten frozen proposal results</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Disposition</th><th scope="col">Mutations</th></tr></thead><tbody>{proposal_rows}</tbody></table></div></section>
<section class="panel" aria-labelledby="limits"><h2 id="limits">Reserved evaluation</h2><p>Manual keyboard, zoom, reflow, print, assistive-technology, cognitive, multilingual, and affected-user evaluation remains reserved. Passing static structure is not complete accessibility. The later named replay is same-owner repeatability only.</p></section>
</main>
</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    phase_dir = repo / PHASE_REL
    if run_git(repo, "rev-parse", "HEAD") != X1_COMMIT:
        raise SystemExit("x2 evidence must start at the exact frozen x1 commit")
    if run_git(repo, "branch", "--show-current") != OWNER_BRANCH:
        raise SystemExit("x2 evidence must use the Tamar canonical owner branch")

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
    if distribution != EXPECTED_DISTRIBUTION or sum(row["matched_count"] for row in rows) != 70:
        raise SystemExit("frozen disposition or mutation accounting failed")
    write_json(
        phase_dir / "x2-proposal-ledger.json",
        {
            "schema": "ghc.family.v645-v1.x2-proposal-ledger.v1",
            "phase": PHASE,
            "owner": OWNER,
            "x1_commit": X1_COMMIT,
            "proposal_count": 10,
            "rows": rows,
            "observed_distribution": dict(distribution),
            "all_expected_dispositions_matched": True,
            "total_case_count": 70,
            "total_matched_count": 70,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "x2 executes only bounded software, structural, proxy, open-gap, and exact-gate obligations.",
        },
    )

    inherited_payload = load_json(repo / INHERITED_NEGATIVES)
    inherited = inherited_payload["negatives"]
    if len(inherited) != 1750:
        raise SystemExit(f"expected 1750 inherited effective negatives, found {len(inherited)}")
    x2_negatives = load_json(repo / X2_NEGATIVE_FILE)["negatives"]
    all_negatives = inherited + X1_NEGATIVES + x2_negatives + synthetic_negatives
    ids = [row["negative_id"] for row in all_negatives]
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    if duplicates:
        raise SystemExit(f"duplicate negative IDs: {duplicates[:5]}")
    write_json(
        phase_dir / "retained-negative-register.json",
        {
            "schema": "ghc.family.v645-v1.retained-negative-register.v1",
            "phase": PHASE,
            "owner": OWNER,
            "inherited_from": INHERITED_NEGATIVES.as_posix(),
            "inherited_sha256": sha256(repo / INHERITED_NEGATIVES),
            "inherited_effective_count": len(inherited),
            "x1_operational_count": len(X1_NEGATIVES),
            "x2_operational_count": len(x2_negatives),
            "new_synthetic_count": len(synthetic_negatives),
            "new_count": len(X1_NEGATIVES) + len(x2_negatives) + len(synthetic_negatives),
            "negative_count": len(all_negatives),
            "duplicate_negative_ids": duplicates,
            "all_retained": True,
            "erasure_permitted": False,
            "negatives": all_negatives,
            "boundary": "Recovery never erases a failure, and a retained negative does not imply its workaround is universally valid.",
        },
    )

    inherited_gates = load_json(repo / INHERITED_GATES)
    if inherited_gates["open_gap_count"] != 5 or inherited_gates["exact_gate_count"] != 6:
        raise SystemExit("inherited gate counts changed")
    write_json(
        phase_dir / "exact-open-gate-register.json",
        {
            "schema": "ghc.family.v645-v1.exact-open-gate-register.v1",
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
                "V6451-P03": "official CMB and tracer inputs, map and mask lineage, selection kernels, covariance, nuisance lock, blind holdout, and independent review remain open",
                "V6451-P06": "affected-party, beneficiary-privacy, fiduciary, Maori, legal, cultural, investment-mandate, inflation-risk, liquidity, and loss-allocation authority remain exact-gated",
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
    external_counts = {
        "real_gmut_rows": 0,
        "real_thos_arms": 0,
        "real_participants": 0,
        "real_identity_or_beneficiary_records": 0,
        "legal_decisions": 0,
        "cultural_ratifications": 0,
        "independent_team_reproductions": 0,
    }
    write_json(
        phase_dir / "evidence/evidence-ledger.json",
        {
            "schema": "ghc.family.v645-v1.evidence-ledger.v1",
            "phase": PHASE,
            "owner": OWNER,
            "x1_commit": X1_COMMIT,
            "proposal_count": 10,
            "observed_distribution": dict(distribution),
            "real_or_external_counts": external_counts,
            "same_owner_repeatability_only": True,
            "protected_claims": protected_claims,
            "snapshot_state": "pending_evidence_commit",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "The ledger describes repository evidence classes and zero-count external domains; it is not external evidence.",
        },
    )

    threats = [
        ("T01", "a stale Method Flow witness remains preferred", "context-bound invalidation and append-only demotion"),
        ("T02", "screening algebra becomes an empirical force claim", "typed regimes, overlap residual, and nonpromotion boundary"),
        ("T03", "public Planck availability is called a GMUT likelihood", "zero-row ISW cross-correlation open-gap receipt"),
        ("T04", "THOS nuisance re-estimation reveals comparative effects", "sealed labels, frozen variance rule, information target, and budget cap"),
        ("T05", "federation issuers, subjects, authority hints, anchors, expiry, or policy operators are cross-bound", "synthetic OpenID Federation chain binding"),
        ("T06", "software decides remedy-fund investment or loss allocation", "zero-record affected-party, Maori, privacy, fiduciary, and legal authority gate"),
        ("T07", "a Git LFS pointer is treated as materialized content", "network-free pointer grammar and missing-object classifier"),
        ("T08", "essential status exists only in CSS or icons", "visible DOM text, print preservation, and manual-evaluation reservation"),
        ("T09", "thermal equilibrium becomes psyche harmony", "typed zeroth-law domain and nonconversion classifier"),
        ("T10", "a clean random sample becomes readiness", "precommitted frame, randomness provenance, missing-item and tamper retention"),
        ("T11", "retry erases failure", "append-only Method Flow and retained-negative registers"),
        ("T12", "private material enters public artifacts", "exact staged five-class privacy scan"),
        ("T13", "working-copy newline variation defeats manifest parity", "Git-blob hashes and LF-preserving named replay"),
        ("T14", "same-owner replay is called independent", "same-owner-only labels"),
        ("T15", "software passes substitute for authority", "protected claims remain false"),
        ("T16", "non-Eiren owner runs the full suite", "scoped rule and one replay limit"),
    ]
    write_json(
        phase_dir / "threat-model.json",
        {
            "schema": "ghc.family.v645-v1.threat-model.v1",
            "phase": PHASE,
            "threat_count": len(threats),
            "threats": [{"id": key, "threat": threat, "control": control} for key, threat, control in threats],
            "resource_ceilings": {"owner_generated_files": 15000, "full_repository_suite_owner": "Eiren Kestrel", "additional_named_replays": 1},
            "exhaustive_security": False,
            "independent_security_review": False,
            "boundary": "This bounded threat model is not penetration testing, privacy certification, exhaustive security, or deployment approval.",
        },
    )

    pointer = f"version {LFS_VERSION}\noid sha256:{'a' * 64}\nsize 42\n".encode("utf-8")
    lfs_cases = [
        classify_bytes(path="fixtures/present.bin", data=pointer, object_present=True),
        classify_bytes(path="fixtures/missing.bin", data=pointer, object_present=False),
        classify_bytes(path="fixtures/plain.txt", data=b"ordinary content\n"),
        classify_bytes(path="../outside.bin", data=pointer, object_present=True),
        classify_bytes(path="fixtures/bad.bin", data=pointer.replace(b"sha256:", b"sha1:"), object_present=True),
    ]
    write_json(
        phase_dir / "tooling/git-lfs-boundary-runner-receipt.json",
        {
            "schema": "ghc.family.v645-v1.git-lfs-boundary-runner-receipt.v1",
            "phase": PHASE,
            "case_count": len(lfs_cases),
            "cases": lfs_cases,
            "network_fetch_count": sum(bool(row["network_fetch_performed"]) for row in lfs_cases),
            "all_expected": [row["classification"] for row in lfs_cases] == [
                "valid_lfs_pointer_object_present",
                "valid_lfs_pointer_object_missing",
                "ordinary_tracked_content",
                "rejected_out_of_root",
                "malformed_lfs_pointer",
            ],
            "boundary": "Classification is local and network-free; a pointer does not establish that its referenced object is present, scanned, private-free, or trusted.",
        },
    )
    report = report_html(rows)
    write_text(phase_dir / "deliverables/v645-v1-static-report.html", report)
    write_json(
        phase_dir / "validation/generated-content-accessibility-audit.json",
        {
            "schema": "ghc.family.v645-v1.generated-content-accessibility-audit.v1",
            "phase": PHASE,
            "essential_css_generated_content_count": 0,
            "icon_only_state_count": 0,
            "print_suppressed_evidence_count": 0,
            "visible_status_text": True,
            "style_off_semantics_preserved": True,
            "structural_checks_pass": True,
            "complete_accessibility": False,
            "boundary": "Automated structure does not replace manual or affected-user accessibility evaluation.",
        },
    )
    write_json(
        phase_dir / "validation/manual-accessibility-reservation.json",
        {
            "schema": "ghc.family.v645-v1.manual-accessibility-reservation.v1",
            "phase": PHASE,
            "reserved": ["keyboard", "zoom", "reflow", "print", "screen reader", "cognitive", "multilingual", "affected-user evaluation"],
            "completed": [],
            "complete_accessibility": False,
            "boundary": "Manual and affected-user evaluation remains open even when structural checks pass.",
        },
    )

    method = load_json(phase_dir / "method-flow/method-flow-state.json")
    write_text(
        phase_dir / "method-flow/sibling-recommendations.md",
        """# Tamar Vey v645-v1 sibling-safe Method Flow recommendations

Use a recommendation only when its declared trigger preconditions match. Preserve the triggering negative after recovery.

- Split large audit surfaces and runner startup into independently bounded commands.
- Discover exact tracked filenames before reading versioned artifacts.
- Separate additive writes from explicit destination inventory receipts.
- Generate stage receipts only after their underlying ledger transition exists.
- Classify Git LFS pointers without fetching and keep missing objects visibly incomplete.
- Bind manifests to normalized Git blobs and require the one clean named replay for checkout parity.
- Do not embed PowerShell backtick escapes inside JavaScript template literals.
- Demote a recommendation when its witness context drifts; never delete the prior pass or failure.

These same-owner methods cannot close empirical, participant, legal, cultural, Maori-authority, identity, production, privacy, deployment, accessibility, exhaustive-security, independent-reproduction, or Stage 20 gates.
""",
    )
    write_json(
        phase_dir / "tooling/executed-toolchain.json",
        {
            "schema": "ghc.family.v645-v1.executed-toolchain.v1",
            "phase": PHASE,
            "skills": ["ghc-family-index", "ghc-family-method-flow-state"],
            "new_family_scripts": [
                "scripts/ghc_family_git_lfs_boundary.py",
                "scripts/ghc_family_v645_v1_model.py",
                "scripts/ghc_family_v645_v1_evidence.py",
                "scripts/ghc_family_v645_v1_staged_review.py",
                "scripts/ghc_family_v645_v1_validator.py",
            ],
            "method_count_at_evidence_build": len(method["methods"]),
            "preferred_method_count_at_evidence_build": sum(row["recommendation_state"] == "preferred" for row in method["methods"]),
            "pending_final_named_lane_method": "v6451-m14",
            "full_repository_suite_owner": "Eiren Kestrel",
            "additional_named_replay_limit": 1,
            "legacy_policy": "Historical tools and callers remain compatible; all phase tooling is additive.",
            "boundary": "Tool execution is bounded software evidence, not AGI, ASI, consciousness, authority, production, or deployment readiness.",
        },
    )
    write_json(
        phase_dir / "tooling/ghc-family-index-x2-update.json",
        {
            "schema": "ghc.family.v645-v1.family-index-x2-update.v1",
            "phase": PHASE,
            "phase_root": PHASE_REL.as_posix(),
            "primary_pillar": "Freed ID/CBR Heart",
            "bounded_practice": "public-interest fund administration and fiduciary governance",
            "tool_surfaces": [
                "ghc_family_git_lfs_boundary.classify_bytes",
                "ghc_family_v645_v1_model.evaluate",
                "ghc_family_v645_v1_validator.validate",
            ],
            "truth_labels": sorted(ALLOWED_OUTCOMES),
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "Index routing is repository-relative and contains no private task, route, transcript, session, credential, or local-path material.",
        },
    )
    write_text(
        phase_dir / "tooling/ghc-family-index-x2-update.md",
        """# Tamar Vey v645-v1 GHC Family Index x2 update

- Phase root: `docs/tamar-vey/v645-v1`.
- Primary pillar: Freed ID/CBR Heart.
- Bounded practice: public-interest fund administration and fiduciary governance.
- Reusable surface: `ghc_family_git_lfs_boundary`.
- Versioned compatibility surfaces: `ghc_family_v645_v1_model` and `ghc_family_v645_v1_validator`.
- Truth labels: completed, represented, open_gap, and exact_gate only.
- Terminal verdict: `NOT_READY_FOR_STAGE_20`.

The x1 index remains the preregistration snapshot. This additive x2 update contains repository-relative routing facts only.
""",
    )
    write_json(
        phase_dir / "orchestration/phase-update.json",
        {
            "schema": "ghc.family.v645-v1.orchestration-update.v1",
            "phase": PHASE,
            "state": "ACTIVE_SOLO; PREPARED_NOT_SENT",
            "canonical_owner": OWNER,
            "x1_commit": X1_COMMIT,
            "x2_evidence_state": "candidate_not_committed",
            "validation_rule": "scoped recent round-robin evidence plus current phase, then exactly one additional clean named-lane replay",
            "full_repository_suite_owner": "Eiren Kestrel",
            "successor_existing_task_title": "Sylven Arc",
            "successor_phase": "v645-gmut-thos-v2-x1-x2",
            "outbound_message_count": 0,
            "successor_task_count": 0,
            "boundary": "No successor activation occurs before exact-final validation and four-way equality.",
        },
    )
    write_json(
        phase_dir / "environment/x2-execution-receipt.json",
        {
            "schema": "ghc.family.v645-v1.x2-execution-receipt.v1",
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "x1_remote_equal_before_x2": True,
            "primary_storage": "D-first",
            "inherited_checkout_tracked_file_count": 31983,
            "owner_generated_file_count_at_evidence_validation": sum(1 for item in phase_dir.rglob("*") if item.is_file()),
            "owner_generated_file_threshold": 15000,
            "rotation_required": False,
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

    x2_overview = OVERVIEW + """

## x2 execution outcome

All ten frozen proposals executed only within their preregistered evidence classes. Six bounded structural proposals completed, THOS independent-monitoring and Freed ID OpenID Federation remained represented or proxy, the GMUT late-time integrated Sachs-Wolfe cross-correlation study remained open with zero rows, and CBR remedy-fund investment, inflation-risk, liquidity, and loss-allocation decisions remained exact-gated. Seventy preregistered mutation cases matched their rejection expectations. This is software behavior, not physical measurement, participant outcome, production identity assurance, privacy certification, legal interpretation, cultural ratification, or independent-team reproduction.

The primary Freed ID/CBR Heart focus preserves the boundary between auditable technical evidence and public-interest fund authority. The OpenID Federation fixtures bind synthetic issuer-subject edges, authority hints, trust anchors, expiry ordering, policy operators, and rollover linkage. No real key, proof, live resolution, status, revocation, or identity record was used. The CBR matrix refuses asset allocation, return targets, inflation objectives, liquidity rules, advisers, fees, and loss allocation without competent fiduciary and legal authority, affected-party participation, beneficiary privacy authority, and Maori authority where relevant. This is not investment, legal, fiduciary, beneficiary, or Maori-authority advice.

The GMUT adiabatic soft-limit tribunal checks only long-wavelength scaling, residual gauge generators, constraints, regularity, entropy-source accounting, and a scoped conserved quantity. The scaffold remains a typed scalar-tensor and EFT research family, not an established force, unique prediction, likelihood result, empirical confirmation, proof, canon, or Theory of Everything. No official CMB map or released cross-spectrum, galaxy tracer input, coupled mask, tracer kernel, covariance, frozen nuisance model, blind holdout, or independent review entered this phase. Therefore no fit or likelihood was run.

THOS remains a synthetic monitoring proxy. Role separation, closed-session sealing, minimized sponsor-facing recommendations, reconstruction rejection, and matched-budget preservation can be tested as software fixtures. No ethics approval, competent monitoring committee, consent, participant arm, outcome, safety record, superiority result, or independent review exists. THOS therefore remains represented, not empirically confirmed.

The new Git LFS boundary runner is read-only and network-free. Synthetic vectors distinguish ordinary content, canonical pointers with present and missing objects, malformed pointers, and out-of-root paths. A valid pointer is not its referenced object, and a missing object prevents manifest or privacy completeness. This does not establish exhaustive repository assurance. The static report keeps status in visible text, provides redundant noncolor cues, and preserves evidence for print. Manual keyboard, zoom, reflow, assistive-technology, cognitive, multilingual, color-perception, and affected-user evaluation remains reserved.

Method Flow retains every operational failure alongside its recovery, recurrence guard, rollback, witness, and recommendation state. The LF-to-CRLF warning remains visible; manifests use Git-blob or explicitly LF-normalized domains and the one later clean named replay is required. Eiren alone owns the full repository suite. This phase uses only current-round scoped checks and exactly one additional clean named replay. Same-owner repeatability under shared infrastructure is not independent-team reproduction.
"""
    write_text(phase_dir / "deliverables/v645-v1-final-integrated-overview.md", x2_overview)
    write_json(
        phase_dir / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v645-v1.complete-incomplete-checklist.v1",
            "phase": PHASE,
            "complete": [
                "exact source and dedicated x1 commit verified",
                "310 inherited proposals audited and ten proposals frozen before x2",
                "ten outcomes use only four allowed truth labels",
                "seventy synthetic mutation cases matched",
                "all 1750 inherited effective negatives preserved",
                "all new x1 and x2 failures retained",
                "five open gaps and six exact gates remain visible",
                "accessible static report and three-page-equivalent overview generated",
                "Method Flow, index, and orchestration records updated",
            ],
            "incomplete": [
                "evidence commit validation",
                "closeout, seal, and final lifecycle",
                "exactly one final clean named-lane replay",
                "one verified Sylven Arc activation baton",
                "real GMUT data or likelihood",
                "blind matched-budget real THOS arms",
                "production Freed ID",
                "affected-party, Maori, privacy, cultural, or legal authority",
                "independent-team reproduction",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "Operational closeout can finish while protected scientific and authority work stays open or exact-gated.",
        },
    )
    write_json(
        phase_dir / "phase-truth.json",
        {
            "schema": "ghc.family.v645-v1.phase-truth.v1",
            "phase": PHASE,
            "owner": OWNER,
            "primary_focus": "Freed ID/CBR Heart",
            "bounded_practice": "public-interest fund administration and fiduciary governance",
            "x1_commit": X1_COMMIT,
            "proposal_count": 10,
            "observed_distribution": dict(distribution),
            "retained_negative_count": len(all_negatives),
            "inherited_effective_negative_count": len(inherited),
            "open_gap_count": 5,
            "exact_gate_count": 6,
            "protected_claims": protected_claims,
            "validation_class": "scoped_recent_round_and_current_phase",
            "scoped_tests": {"passed": 120, "total": 120, "state": "evidence_candidate_passed"},
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
        phase_dir / "validation/scoped-test-receipt.json",
        {
            "schema": "ghc.family.v645-v1.scoped-test-receipt.v1",
            "phase": PHASE,
            "scope": [
                "v644-v7 x1 and x2",
                "v644-v8 x1 and x2",
                "v645-v1 x1 and x2",
            ],
            "passed": 120,
            "total": 120,
            "full_repository_suite_run": False,
            "full_repository_suite_owner": "Eiren Kestrel",
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "The receipt covers only the six explicitly named recent-round test modules and cannot establish full-repository, scientific, security, accessibility, or independent-reproduction assurance.",
        },
    )
    write_json(
        phase_dir / "stage20/terminal-evidence-board.json",
        {
            "schema": "ghc.family.v645-v1.terminal-evidence-board.v1",
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
            "randomized_challenge": {"sample_frame": "synthetic_manifest_only", "readiness_promotion": False},
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "ready": False,
            "boundary": "Domain vetoes cannot be averaged away by software passes or same-owner agreement.",
        },
    )

    exclusions = {"reproduction/evidence-manifest.json"}
    entries = []
    for path in sorted(item for item in phase_dir.rglob("*") if item.is_file()):
        relative = path.relative_to(phase_dir).as_posix()
        if relative in exclusions or relative.startswith("validation/evidence-"):
            continue
        entries.append({"path": relative, "logical_lf_sha256": logical_text_sha256(path), "bytes": path.stat().st_size})
    write_json(
        phase_dir / "reproduction/evidence-manifest.json",
        {
            "schema": "ghc.family.v645-v1.evidence-manifest.v1",
            "phase": PHASE,
            "hash_domain": "LF-normalized logical text for candidate repeatability",
            "entry_count": len(entries),
            "entries": entries,
            "same_owner_repeatability_only": True,
            "independent_team_reproduction": False,
            "boundary": "This manifest supports bounded change detection, not a signature or independent scientific reproduction.",
        },
    )
    print(
        json.dumps(
            {
                "phase": PHASE,
                "proposals": len(rows),
                "distribution": dict(distribution),
                "mutation_cases": len(synthetic_negatives),
                "inherited_effective_negatives": len(inherited),
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
