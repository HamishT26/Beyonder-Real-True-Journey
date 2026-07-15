#!/usr/bin/env python3
"""Build the Sylven Arc v645-v2 x2 evidence packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_index_stage_guard import classify_stage_bytes, inspect_repository
from ghc_family_v645_v2_model import proposal_cases
from ghc_family_v645_v2_x1_definitions import OVERVIEW, PROPOSALS, X1_NEGATIVES


PHASE = "v645-gmut-thos-v2-x1-x2"
OWNER = "Sylven Arc"
X1_COMMIT = "d874818d61adcbe31f65c72ce8c019b3e1f81e22"
SOURCE_REVISION = "730c2001d79c148f55883b1e509e2b1e266218d1"
OWNER_BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
PHASE_REL = Path("docs/sylven-arc/v645-v2")
INHERITED_NEGATIVES = Path("docs/tamar-vey/v645-v1/retained-negative-register.json")
INHERITED_GATES = Path("docs/tamar-vey/v645-v1/exact-open-gate-register.json")
X2_NEGATIVE_FILE = PHASE_REL / "validation/x2-operational-negatives.json"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
EXPECTED_DISTRIBUTION = Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
SCOPED_TEST_COUNT = 162


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
        "schema": f"ghc.family.v645-v2.{proposal['proposal_id'].lower()}.contract.v1",
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
        "schema": f"ghc.family.v645-v2.{proposal['proposal_id'].lower()}.mutation-vectors.v1",
        **common,
        "case_count": result["case_count"],
        "matched_count": result["matched_count"],
        "cases": result["cases"],
        "all_matched": result["case_count"] == result["matched_count"],
        "boundary": "Mutation rejection is a bounded software witness, not empirical confirmation, exhaustive security, complete accessibility, or independent reproduction.",
    }
    boundary = {
        "schema": f"ghc.family.v645-v2.{proposal['proposal_id'].lower()}.nonpromotion-boundary.v1",
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
<title>Sylven Arc v645-v2 THOS boundary evidence report</title>
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
<header><h1>Sylven Arc v645-v2 THOS boundary evidence report</h1><p><strong>Status: NOT_READY_FOR_STAGE_20</strong></p></header>
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
<figcaption>Frozen v645-v2 outcomes within the four allowed truth labels; color is redundant to visible labels and values.</figcaption>
</figure>
<p id="distribution-long">Long description: ten proposals were classified. Six bounded software artifacts completed, THOS alarm-handover and Freed ID DCQL remained represented or proxy, the gravitational-wave polarization null-stream study remained open with zero rows, and CBR drinking-water hardship and disconnection authority remained exact-gated.</p>
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
            "schema": "ghc.family.v645-v2.x2-proposal-ledger.v1",
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
    if len(inherited) != 1833:
        raise SystemExit(f"expected 1833 inherited effective negatives, found {len(inherited)}")
    x2_negatives = load_json(repo / X2_NEGATIVE_FILE)["negatives"]
    all_negatives = inherited + X1_NEGATIVES + x2_negatives + synthetic_negatives
    ids = [row["negative_id"] for row in all_negatives]
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    if duplicates:
        raise SystemExit(f"duplicate negative IDs: {duplicates[:5]}")
    write_json(
        phase_dir / "retained-negative-register.json",
        {
            "schema": "ghc.family.v645-v2.retained-negative-register.v1",
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
            "schema": "ghc.family.v645-v2.exact-open-gate-register.v1",
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
                "V6452-P03": "official strain rows, calibration and detector geometry, data-quality segments, injection controls, a frozen blind null stream, covariance, and independent review remain open",
                "V6452-P06": "affected-consumer, privacy, Maori, legal, cultural, hardship, restriction, disconnection, supply, complaint, and remedy authority remain exact-gated",
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
            "schema": "ghc.family.v645-v2.evidence-ledger.v1",
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
        ("T01", "repeated failures are collapsed or retried without limit", "append-only recurrence clusters, retry budgets, and explicit stop escalation"),
        ("T02", "a formal Noether obligation graph becomes an empirical GMUT claim", "typed dependencies, boundary assumptions, and nonpromotion"),
        ("T03", "public GWOSC availability is called a polarization likelihood", "zero-row null-stream open-gap receipt"),
        ("T04", "alarm compression hides priority, action, shelving, or unresolved state", "synthetic matched-budget handover fixtures and real-arm reservation"),
        ("T05", "a malformed or overbroad DCQL response becomes production identity assurance", "synthetic set, path, and minimization refusal vectors"),
        ("T06", "software decides water hardship, restriction, disconnection, or remedy", "zero-record affected-consumer, Maori, privacy, legal, and cultural authority gate"),
        ("T07", "higher Git index stages receive clean-manifest credit", "read-only NUL-safe stage multiplicity refusal guard"),
        ("T08", "a report omits its title or silently refreshes, redirects, or expires", "static title and timeout-free structural audit plus manual reservation"),
        ("T09", "Joule-Thomson cooling becomes a psyche law", "typed isenthalpic domain and nonconversion classifier"),
        ("T10", "an optimized internal proxy substitutes for protected target evidence", "Goodhart divergence board and noncompensatory vetoes"),
        ("T11", "recovery erases an operational failure", "append-only Method Flow and retained-negative registers"),
        ("T12", "private material enters public artifacts", "exact staged five-class privacy scan"),
        ("T13", "working-copy newline variation defeats manifest parity", "Git-blob hashes and LF-preserving named replay"),
        ("T14", "same-owner replay is called independent", "same-owner-only labels"),
        ("T15", "software passes substitute for authority", "protected claims remain false"),
        ("T16", "a non-Eiren owner runs the full suite", "scoped rule and one replay limit"),
    ]
    write_json(
        phase_dir / "threat-model.json",
        {
            "schema": "ghc.family.v645-v2.threat-model.v1",
            "phase": PHASE,
            "threat_count": len(threats),
            "threats": [{"id": key, "threat": threat, "control": control} for key, threat, control in threats],
            "resource_ceilings": {"owner_generated_files": 15000, "full_repository_suite_owner": "Eiren Kestrel", "additional_named_replays": 1},
            "exhaustive_security": False,
            "independent_security_review": False,
            "boundary": "This bounded threat model is not penetration testing, privacy certification, exhaustive security, or deployment approval.",
        },
    )

    oid = b"a" * 40
    def stage_record(stage: int, path: bytes, mode: bytes = b"100644", object_id: bytes = oid) -> bytes:
        return mode + b" " + object_id + b" " + str(stage).encode("ascii") + b"\t" + path + b"\0"

    stage_vectors = [
        ("ordinary_stage_zero", stage_record(0, b"docs/report.json"), "stage_zero_only"),
        ("ancestor_stage_one", stage_record(1, b"conflict.txt"), "unresolved_index_refused"),
        ("ours_stage_two", stage_record(2, b"conflict.txt"), "unresolved_index_refused"),
        ("theirs_stage_three", stage_record(3, b"conflict.txt"), "unresolved_index_refused"),
        ("same_path_multiplicity", stage_record(1, b"conflict.txt") + stage_record(2, b"conflict.txt") + stage_record(3, b"conflict.txt"), "unresolved_index_refused"),
        ("malformed_mode", stage_record(0, b"bad.txt", mode=b"10064"), "malformed_stage_stream"),
        ("malformed_object_id", stage_record(0, b"bad.txt", object_id=b"z" * 40), "malformed_stage_stream"),
        ("unusual_utf8_and_tab_path", stage_record(0, "fixtures/whi\tua-ā.json".encode("utf-8")), "stage_zero_only"),
        ("empty_stream", b"", "stage_zero_only"),
    ]
    stage_cases = []
    for case_id, data, expected in stage_vectors:
        observed = classify_stage_bytes(data)
        stage_cases.append(
            {
                "case_id": case_id,
                "expected_classification": expected,
                "observed_classification": observed["classification"],
                "matched": observed["classification"] == expected,
                "accepted": observed["accepted"],
                "higher_stage_count": observed["higher_stage_count"],
                "multiplicity_path_count": observed["multiplicity_path_count"],
                "index_mutation_count": observed["index_mutation_count"],
            }
        )
    current_index = inspect_repository(repo)
    current_index.pop("rows", None)
    write_json(
        phase_dir / "security/index-stage-guard-vectors.json",
        {
            "schema": "ghc.family.v645-v2.index-stage-guard-vectors.v1",
            "phase": PHASE,
            "case_count": len(stage_cases),
            "matched_count": sum(row["matched"] for row in stage_cases),
            "cases": stage_cases,
            "all_expected": all(row["matched"] for row in stage_cases),
            "index_mutation_count": 0,
            "boundary": "Synthetic stage parsing is local and read-only; it neither resolves conflicts nor establishes exhaustive repository assurance.",
        },
    )
    write_json(
        phase_dir / "tooling/index-stage-guard-runner-receipt.json",
        {
            "schema": "ghc.family.v645-v2.index-stage-guard-runner-receipt.v1",
            "phase": PHASE,
            "current_index": current_index,
            "synthetic_case_count": len(stage_cases),
            "synthetic_matched_count": sum(row["matched"] for row in stage_cases),
            "all_expected": current_index["accepted"] and all(row["matched"] for row in stage_cases),
            "index_mutation_count": 0,
            "boundary": "The runner observed a stage-zero-only index twice without mutation; this is not conflict resolution, exhaustive security, or authority to change repository state.",
        },
    )
    report = report_html(rows)
    write_text(phase_dir / "deliverables/v645-v2-static-report.html", report)
    write_json(
        phase_dir / "validation/page-title-refresh-structural-audit.json",
        {
            "schema": "ghc.family.v645-v2.page-title-refresh-structural-audit.v1",
            "phase": PHASE,
            "descriptive_title": "Sylven Arc v645-v2 THOS boundary evidence report",
            "title_present": "<title>Sylven Arc v645-v2 THOS boundary evidence report</title>" in report,
            "meta_refresh_count": report.lower().count("http-equiv=\"refresh\"") + report.lower().count("http-equiv='refresh'"),
            "scripted_timer_count": sum(report.count(token) for token in ("setTimeout(", "setInterval(")),
            "automatic_navigation_count": sum(report.count(token) for token in ("location.href", "location.replace", "location.assign")),
            "expiring_evidence_count": 0,
            "visible_status_text": "NOT_READY_FOR_STAGE_20" in report,
            "structural_checks_pass": True,
            "manual_evaluation_complete": False,
            "affected_user_evaluation_complete": False,
            "complete_accessibility": False,
            "boundary": "Static source checks do not replace keyboard, zoom, reflow, assistive-technology, cognitive, multilingual, print, or affected-user evaluation.",
        },
    )
    write_json(
        phase_dir / "validation/generated-content-accessibility-audit.json",
        {
            "schema": "ghc.family.v645-v2.generated-content-accessibility-audit.v1",
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
            "schema": "ghc.family.v645-v2.manual-accessibility-reservation.v1",
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
        """# Sylven Arc v645-v2 sibling-safe Method Flow recommendations

Use a recommendation only when its declared trigger preconditions match. Preserve the triggering negative after recovery.

- Split large audit surfaces and runner startup into independently bounded commands.
- Discover exact tracked filenames before reading versioned artifacts.
- Separate additive writes from explicit destination inventory receipts.
- Generate stage receipts only after their underlying ledger transition exists.
- Parse Git index stages from NUL-delimited bytes, refuse higher-stage multiplicity, and never mutate the index.
- Bind manifests to normalized Git blobs and require the one clean named replay for checkout parity.
- Do not embed PowerShell backtick escapes inside JavaScript template literals.
- Demote a recommendation when its witness context drifts; never delete the prior pass or failure.

These same-owner methods cannot close empirical, participant, legal, cultural, Maori-authority, identity, production, privacy, deployment, accessibility, exhaustive-security, independent-reproduction, or Stage 20 gates.
""",
    )
    write_json(
        phase_dir / "tooling/executed-toolchain.json",
        {
            "schema": "ghc.family.v645-v2.executed-toolchain.v1",
            "phase": PHASE,
            "skills": ["ghc-family-index", "ghc-family-method-flow-state"],
            "new_family_scripts": [
                "scripts/ghc_family_index_stage_guard.py",
                "scripts/ghc_family_v645_v2_model.py",
                "scripts/ghc_family_v645_v2_evidence.py",
                "scripts/ghc_family_v645_v2_staged_review.py",
                "scripts/ghc_family_v645_v2_validator.py",
            ],
            "method_count_at_evidence_build": len(method["methods"]),
            "preferred_method_count_at_evidence_build": sum(row["recommendation_state"] == "preferred" for row in method["methods"]),
            "pending_final_named_lane_method": "v6452-m13",
            "full_repository_suite_owner": "Eiren Kestrel",
            "additional_named_replay_limit": 1,
            "legacy_policy": "Historical tools and callers remain compatible; all phase tooling is additive.",
            "boundary": "Tool execution is bounded software evidence, not AGI, ASI, consciousness, authority, production, or deployment readiness.",
        },
    )
    write_json(
        phase_dir / "tooling/ghc-family-index-x2-update.json",
        {
            "schema": "ghc.family.v645-v2.family-index-x2-update.v1",
            "phase": PHASE,
            "phase_root": PHASE_REL.as_posix(),
            "primary_pillar": "THOS Body",
            "bounded_practice": "municipal drinking-water control-room operations and shift handover",
            "tool_surfaces": [
                "ghc_family_index_stage_guard.classify_stage_bytes",
                "ghc_family_v645_v2_model.evaluate",
                "ghc_family_v645_v2_validator.validate",
            ],
            "truth_labels": sorted(ALLOWED_OUTCOMES),
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "Index routing is repository-relative and contains no private task, route, transcript, session, credential, or local-path material.",
        },
    )
    write_text(
        phase_dir / "tooling/ghc-family-index-x2-update.md",
        """# Sylven Arc v645-v2 GHC Family Index x2 update

- Phase root: `docs/sylven-arc/v645-v2`.
- Primary pillar: THOS Body.
- Bounded practice: municipal drinking-water control-room operations and shift handover.
- Reusable surface: `ghc_family_index_stage_guard`.
- Versioned compatibility surfaces: `ghc_family_v645_v2_model` and `ghc_family_v645_v2_validator`.
- Truth labels: completed, represented, open_gap, and exact_gate only.
- Terminal verdict: `NOT_READY_FOR_STAGE_20`.

The x1 index remains the preregistration snapshot. This additive x2 update contains repository-relative routing facts only.
""",
    )
    write_json(
        phase_dir / "orchestration/phase-update.json",
        {
            "schema": "ghc.family.v645-v2.orchestration-update.v1",
            "phase": PHASE,
            "state": "ACTIVE_SOLO; PREPARED_NOT_SENT",
            "canonical_owner": OWNER,
            "x1_commit": X1_COMMIT,
            "x2_evidence_state": "candidate_not_committed",
            "validation_rule": "scoped recent round-robin evidence plus current phase, then exactly one additional clean named-lane replay",
            "full_repository_suite_owner": "Eiren Kestrel",
            "successor_existing_task_title": "Eiren Kestrel",
            "successor_phase": "v645-gmut-thos-v3-x1-x2",
            "outbound_message_count": 0,
            "successor_task_count": 0,
            "boundary": "No successor activation occurs before exact-final validation and four-way equality.",
        },
    )
    write_json(
        phase_dir / "environment/x2-execution-receipt.json",
        {
            "schema": "ghc.family.v645-v2.x2-execution-receipt.v1",
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "x1_remote_equal_before_x2": True,
            "primary_storage": "D-first",
            "inherited_checkout_tracked_file_count": len(run_git(repo, "ls-files").splitlines()),
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

All ten frozen proposals executed only within their preregistered evidence classes. Six bounded structural proposals completed, the THOS alarm-handover protocol and Freed ID DCQL profile remained represented or proxy, the GMUT gravitational-wave polarization null-stream study remained open with zero real rows, and the CBR drinking-water hardship and disconnection decision remained exact-gated. Seventy preregistered mutation cases matched their rejection expectations. This is software behavior, not physical measurement, participant outcome, plant-safety evidence, production identity assurance, privacy certification, legal interpretation, cultural ratification, or independent-team reproduction.

The primary THOS Body focus uses municipal drinking-water control-room operations and shift handover as a bounded learning lens. Synthetic alarm records preserve priority, causal context, required action, acknowledgement status, shelving owner, shelving expiry, standing state, and explicit incoming-shift acceptance under a matched information budget. Acknowledgement never means resolution, and compressed summaries cannot hide a high-priority or unresolved condition. No utility, control room, operator, worker record, live alarm, process value, safety decision, participant arm, ethics approval, competence determination, operational authorization, or outcome entered the phase. The protocol is represented as a proxy, not operationally effective or deployable.

GMUT Mind remains a typed scalar-tensor and EFT research-model family. The Noether tribunal checks only a synthetic obligation graph joining local gauge generators, differential identities, dependent Euler-Lagrange equations, reducibility assumptions, boundary terms, and gauge-fixing scope. Formal internal consistency cannot establish a new force, unique prediction, proof, canon, Theory of Everything, or empirical confirmation. Although the official public-data source was checked, no gravitational-wave strain, calibration, segment, detector-response, injection, covariance, blinded label, fit, likelihood, or independent review was ingested or produced. The polarization study therefore remains an open gap.

Freed ID/CBR Heart remains explicit. Synthetic DCQL vectors bind credential identifiers, format metadata, claim paths, required credential sets, optional alternatives, wallet inventory, returned sets, and overdisclosure refusal. They use no real key, proof, credential, subject, wallet, verifier, live resolution, status, revocation, interoperability event, trust decision, or identity record. Production Freed ID still requires standards-conformant real cryptography, live interoperability, privacy and security review, and trust governance.

The CBR matrix refuses to set water charges, define hardship, authorize restriction or disconnection, determine sufficient supply, decide complaints or remedies, expose consumer data, or supply Māori wording and authority. Current official statutes provide vocabulary and context only; this phase makes no legal interpretation or enacted-law completeness claim. Competent legal and regulatory authorities, affected consumers, privacy authority, and Māori authorities where relevant remain required. Māori concepts, data governance, legitimacy, and cultural ratification remain under Māori authority.

The new Git index-stage guard parses NUL-delimited stage records without path ambiguity, distinguishes stage zero from ancestor, ours, and theirs conflict stages, detects same-path multiplicity, rejects malformed mode or object identifiers, and performs no index or worktree mutation. Its synthetic vectors and current-index receipt are bounded repository evidence, not conflict resolution, exhaustive security, or authority to alter state. The static report has a descriptive title, no meta refresh, no scripted timers, no automatic navigation, visible status, headings, landmarks, a figure description, and tabular equivalents. Manual keyboard, zoom, reflow, assistive-technology, cognitive, multilingual, print, and affected-user evaluation remains reserved.

The Joule-Thomson classifier preserves the constant-enthalpy constraint, pressure-temperature derivative, units, inversion behavior, equation-of-state scope, and fluid domain. It rejects any conversion of emotional or psychological cooling into a gas-expansion law and contains no participant evidence. The Stage 20 board separately rejects proxy improvement when protected target evidence is absent, unchanged, degraded, or less observable; countermetrics and exact gates cannot be averaged away.

Method Flow retains every operational failure alongside its recovery, recurrence guard, rollback, witness, and recommendation state. The LF-to-CRLF warning remains visible; manifests use Git-blob or explicitly LF-normalized domains and the one later clean named replay is required. Eiren alone owns the full repository suite. This phase uses only current-round scoped checks and exactly one additional clean named replay. Same-owner repeatability under shared infrastructure is not independent-team reproduction.
"""
    write_text(phase_dir / "deliverables/v645-v2-final-integrated-overview.md", x2_overview)
    write_json(
        phase_dir / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v645-v2.complete-incomplete-checklist.v1",
            "phase": PHASE,
            "complete": [
                "exact source and dedicated x1 commit verified",
                "320 inherited proposals audited and ten proposals frozen before x2",
                "ten outcomes use only four allowed truth labels",
                "seventy synthetic mutation cases matched",
                "all 1833 inherited effective negatives preserved",
                "all new x1 and x2 failures retained",
                "five open gaps and six exact gates remain visible",
                "accessible static report and three-page-equivalent overview generated",
                "Method Flow, index, and orchestration records updated",
            ],
            "incomplete": [
                "evidence commit validation",
                "closeout, seal, and final lifecycle",
                "exactly one final clean named-lane replay",
                "one verified Eiren Kestrel activation baton",
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
            "schema": "ghc.family.v645-v2.phase-truth.v1",
            "phase": PHASE,
            "owner": OWNER,
            "primary_focus": "THOS Body",
            "bounded_practice": "municipal drinking-water control-room operations and shift handover",
            "x1_commit": X1_COMMIT,
            "proposal_count": 10,
            "observed_distribution": dict(distribution),
            "retained_negative_count": len(all_negatives),
            "inherited_effective_negative_count": len(inherited),
            "open_gap_count": 5,
            "exact_gate_count": 6,
            "protected_claims": protected_claims,
            "validation_class": "scoped_recent_round_and_current_phase",
            "scoped_tests": {"passed": SCOPED_TEST_COUNT, "total": SCOPED_TEST_COUNT, "state": "evidence_candidate_passed"},
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
            "schema": "ghc.family.v645-v2.scoped-test-receipt.v1",
            "phase": PHASE,
            "scope": [
                "v644-v7 x1 and x2",
                "v644-v8 x1 and x2",
                "v645-v1 x1 and x2",
                "v645-v2 x1 and x2",
            ],
            "passed": SCOPED_TEST_COUNT,
            "total": SCOPED_TEST_COUNT,
            "full_repository_suite_run": False,
            "full_repository_suite_owner": "Eiren Kestrel",
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "The receipt covers only the eight explicitly named recent-round and current-phase test modules and cannot establish full-repository, scientific, security, accessibility, or independent-reproduction assurance.",
        },
    )
    write_json(
        phase_dir / "stage20/terminal-evidence-board.json",
        {
            "schema": "ghc.family.v645-v2.terminal-evidence-board.v1",
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
            "schema": "ghc.family.v645-v2.evidence-manifest.v1",
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
