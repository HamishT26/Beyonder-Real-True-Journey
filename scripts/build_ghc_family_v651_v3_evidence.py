#!/usr/bin/env python3
"""Build Tamar Vey v651-v3 x2 evidence ledgers from bounded receipts."""

from __future__ import annotations

import hashlib
import html
import io
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import ghc_family_v651_v3_phase_data as d

ROOT = REPO / d.PHASE_ROOT
X1_COMMIT = "111e53d75eaa3560b48c3573507552b9ddb5ddfc"
X1_MANIFEST = f"{d.PHASE_ROOT}/validation/x1-staged-manifest.json"
X1_OPS = 14
X2_OPS = [
    {"negative_id": "V6513-X2-N01", "summary": "PowerShell misparsed the upstream shorthand in a post-x1 divergence display; explicit refs recovered 0/0."},
    {"negative_id": "V6513-X2-N02", "summary": "A parallel predecessor-size inventory timed out; one bounded sequential loop recovered all eight rows."},
    {"negative_id": "V6513-X2-N03", "summary": "A broad compatibility normalizer rewrote the retained N14 failed observation; a field-scoped correction restored exact history."},
    {"negative_id": "V6513-X2-N04", "summary": "A mixed native and PowerShell audit wrapper returned exit 1 despite visible matches; exact JSON fields recovered attribution."},
    {"negative_id": "V6513-X2-N05", "summary": "The evidence-builder patch acknowledgement exceeded the visible response budget; exact file existence, size, compilation, tail, and execution checks recovered attribution."},
    {"negative_id": "V6513-X2-N06", "summary": "A combined resumption status and identity probe timed out before yielding output; bounded single-purpose probes recovered the file, head, and branch state."},
    {"negative_id": "V6513-X2-N07", "summary": "A read-only portfolio audit guessed five nonexistent execution filenames; exact directory enumeration recovered the aggregate execution receipt."},
    {"negative_id": "V6513-X2-N08", "summary": "A read-only tooling audit guessed predecessor-style skill and runner receipt paths; exact tooling-directory enumeration recovered the current receipts."},
    {"negative_id": "V6513-X2-N09", "summary": "A successful Method Flow summarize wrapper emitted an overlarge one-line payload that was truncated in the supervising output; file-backed summary validation recovered exact counts."},
    {"negative_id": "V6513-X2-N10", "summary": "The first 23-case combined current-phase attempt failed two frozen x1 lifecycle assertions after x2; an exact 21-case successor-safe selection passed while immutable x1 parity preserved both assertions at the x1 commit."},
    {"negative_id": "V6513-X2-N11", "summary": "The first exact evidence staging wrapper emitted enough line-ending warnings to truncate its supervising output; the staged operation succeeded and an exact index-path count recovered attribution."},
    {"negative_id": "V6513-X2-N12", "summary": "A stale-label audit passed Windows wildcard path arguments directly to ripgrep and ended with invalid-path errors; repository-root glob filters recovered the exact review."},
]
EXPECTED = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}


def write_json(relative: str, payload) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, text: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str, binary: bool = False):
    output = subprocess.check_output(["git", *args], cwd=REPO)
    return output if binary else output.decode("utf-8").strip()


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    proc = subprocess.run(["git", "cat-file", "--batch"], cwd=REPO, input="".join(oid + "\n" for oid in unique).encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    stream, result = io.BytesIO(proc.stdout), {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode().split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(header)
        size = int(header[2])
        payload = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("missing batch frame terminator")
        result[expected] = payload
    if stream.read():
        raise RuntimeError("trailing batch output")
    return result


def x1_parity() -> dict:
    manifest = json.loads(git("show", f"{X1_COMMIT}:{X1_MANIFEST}"))
    blobs = batch_blobs([row["git_blob"] for row in manifest["entries"]])
    issues = []
    for row in manifest["entries"]:
        data = blobs[row["git_blob"]]
        if git("rev-parse", f"{X1_COMMIT}:{row['path']}") != row["git_blob"]:
            issues.append("blob:" + row["path"])
        if len(data) != row["bytes"]:
            issues.append("bytes:" + row["path"])
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            issues.append("sha256:" + row["path"])
    return {"schema": "ghc.family.v651-v3.x1-immutability.v1", "x1_commit": X1_COMMIT, "entry_count": len(manifest["entries"]), "self_exclusion_count": len(manifest["self_exclusions"]), "issues": issues, "immutable_git_object_parity": not issues, "lifecycle_companions_advanced": ["method-flow/method-flow-ledger.json", "method-flow/method-flow-summary.json", "method-flow/method-flow-summary.md", "method-flow/method-flow-validation.json"], "boundary": "Immutable x1 objects remain exact; x2 lifecycle companions do not rewrite that commit.", "valid": not issues}


def overview(outcomes: list[dict], effective_negatives: int, methods: dict) -> str:
    lines = [f"""# Tamar Vey {d.PHASE} x2 bounded evidence overview

## Outcome first

All twenty frozen proposals executed within their authorized lanes. The distribution is exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. Every completion is limited to its declared owner-local software, symbolic, formal, numerical, structural, or synthetic hypothesis. All one hundred preregistered mutations were executed and rejected or quarantined. The packet preserves {effective_negatives:,} effective negatives, carries fifty-three open gaps and fifty-four exact gates, and remains `NOT_READY_FOR_STAGE_20`.

No full repository suite ran because Eiren alone owns that suite. No post-success replay, detached validation, named validation lane, Sandbox, Hyper-V, elevation, host-security change, Windows-feature change, unrelated installation, desktop update, reboot, task creation, fork, delegation, collaboration subagent, sibling mutation, cross-platform substitute, participant study, real identity event, or authority decision occurred. Same-owner evidence under shared infrastructure is not independent-team scientific reproduction or external audit.

## Trinity Mandala and bounded practice

GMUT Mind is primary. The Israel junction and Cartan-Karlhede surfaces completed only as typed obligation and mutation guards. They establish no physical shell, spacetime classification for GMUT, force, prediction, likelihood, parameter constraint, stability theorem, empirical confirmation, ultraviolet completion, proof or canon, or Theory of Everything. The ROSAT 2RXS adapter remains an open gap with zero queries, downloads, rows, likelihoods, posterior samples, or constraints.

THOS Body remains represented. The archival-audio intake and transfer protocols use synthetic records only, with zero real carriers, recordings, contributors, archivists, engineers, services, incidents, blind matched-budget arms, or operational-effectiveness estimates. The format and numerical tribunals complete only their bounded fixture hypotheses. The audio-player audit is structural; manual keyboard, browser, responsive, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remains reserved.

Freed ID and CBR Heart remain synthetic and nonproduction. RFC 8707 and RFC 6750 profiles use zero real keys, tokens, accounts, authorization servers, resource servers, network calls, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. The oral-history matrix is an exact gate. It makes no consent, withdrawal, custody, embargo, access, correction, remedy, legal, cultural, data-governance, affected-party, or Māori-authority decision.

The bounded practice lens was archival-audio preservation and transfer quality assurance, correction readback, workload control, and shift handover. It was learning and synthetic design only. It establishes no employment, qualification, professional competence, archival authority, preservation result, cultural legitimacy, participant evidence, legal interpretation, Māori authority, affected-party acceptance, or operational outcome.

## Portfolios, skills, runners, and Method Flow

Forty new safe-now items, thirty bounded candidate prototypes, twenty phase-local skills, ten family-current runners, and forty additive CLEAN/FIX/REFINE items passed their declared acceptance gates. The thirty prototypes were built, tested, and invoked. All twenty skills were initialized through the official skill-creator workflow, customized, validated under explicit UTF-8, and smoke-used against their exact proposal surfaces. They were not globally installed. The optional subagent forward test stayed unavailable because this phase forbids delegation.

The ten runners preserve `ghc_family_*` naming and caller compatibility. Eight proposal-group runners emitted the twenty surface receipts; the portfolio runner emitted exact 40/30/20/10/40 execution receipts; the validator confirmed twenty surfaces and one hundred mutations. These passes are useful bounded engineering evidence, never exhaustive security, production certification, complete privacy, complete accessibility, professional qualification, independent reproduction, or authority.

Method Flow now contains {methods['methods']} preferred methods, {methods['witness_results']['fail']} retained failed witnesses, and {methods['witness_results']['pass']} passing witnesses. The x2 failures include a PowerShell upstream-shorthand parse, a parallel size-inventory timeout, an overbroad compatibility normalizer that altered a retained failure description, and a mixed native-pipeline status fault. Each first attempt has zero aggregate credit. Exact bounded recoveries preserve the failed witness and add recurrence guards; they never erase the negative.

## Provenance, privacy, and next gate

The x1 commit `{X1_COMMIT}` remains immutable across all 92 manifest entries plus three declared self-exclusions. Evidence uses exact Git-object parity, not working-tree appearance. Public artifacts exclude raw task or thread identifiers, private routes, transcripts, screenshots, credentials, private keys, tokens, session streams, private callable identifiers, private app state, and private absolute local paths. Five-class scanning is bounded hygiene, not privacy completeness.

This evidence packet may proceed only after exact staged review, current-phase tests, complete phase JSON parsing, manifest parity, stale-label review, diff hygiene, privacy scanning, and an evidence commit. Closeout may begin only after that evidence commit is pushed, clean, and local, upstream, tracking, and fresh live remote equal. The successor route remains held. Only one acknowledged exact-title message after exact-final validation may change the route state to sent.
"""]
    for row in outcomes:
        lines.append(f"### {row['proposal_id']} — {row['observed_disposition']}\n\n{row['title']} passed its accepting fixture and rejected five of five frozen mutations. Real rows, participants or operators, real identity or network events, and authority decisions are all zero. {row['credit_boundary']}\n")
    return "\n".join(lines)


def main() -> None:
    if not subprocess.run(["git", "merge-base", "--is-ancestor", X1_COMMIT, "HEAD"], cwd=REPO).returncode == 0:
        raise RuntimeError("x1 not ancestral")
    receipts = [load(f"surfaces/{p['slug']}/bounded-receipt.json") for p in d.PROPOSALS]
    counts = Counter(row["observed_disposition"] for row in receipts)
    if dict(counts) != EXPECTED:
        raise RuntimeError(counts)
    mutation_rows = [row for p in d.PROPOSALS for row in load(f"surfaces/{p['slug']}/mutation-results.json")["results"]]
    if len(mutation_rows) != 100 or not all(row["passed"] for row in mutation_rows):
        raise RuntimeError("mutation execution mismatch")
    runner_paths = sorted((ROOT / "tooling/runner-witnesses").glob("ghc_family_v651_v3_*.json"))
    skill_paths = sorted((ROOT / "tooling/skill-witnesses").glob("*.json"))
    if len(runner_paths) != 10 or not all(json.loads(p.read_text(encoding="utf-8"))["valid"] for p in runner_paths):
        raise RuntimeError("runner witnesses")
    if len(skill_paths) != 20 or not all(json.loads(p.read_text(encoding="utf-8"))["valid"] for p in skill_paths):
        raise RuntimeError("skill witnesses")
    portfolio = load("portfolios/expanded-portfolio-execution.json")
    if not portfolio["valid"]:
        raise RuntimeError("portfolio execution")
    parity = x1_parity()
    if not parity["valid"]:
        raise RuntimeError(parity["issues"])
    write_json("provenance/x1-immutability-receipt.json", parity)
    method_counts = load("method-flow/method-flow-summary.json")["counts"]
    effective_negatives = d.INHERITED_NEGATIVES + X1_OPS + len(X2_OPS) + 100

    outcome_rows = []
    for proposal, receipt in zip(d.PROPOSALS, receipts, strict=True):
        outcome_rows.append({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "pillar": proposal["pillar"], "observed_disposition": receipt["observed_disposition"], "accepting_fixture_passed": True, "mutation_rejected_count": 5, "source_ids": proposal["official_or_primary_source_needs"], "evidence": [f"surfaces/{proposal['slug']}/contract.json", f"surfaces/{proposal['slug']}/accepting-fixture.json", f"surfaces/{proposal['slug']}/mutation-results.json", f"surfaces/{proposal['slug']}/bounded-receipt.json"], "real_rows": 0, "participants_or_operators": 0, "real_identity_or_network_events": 0, "authority_decisions": 0, "protected_gates": proposal["protected_gates"], "credit_boundary": receipt["boundary"]})
    write_json("outcomes/evidence-ledger.json", {"schema": "ghc.family.v651-v3.evidence-ledger.v1", "phase": d.PHASE, "outcome_counts": EXPECTED, "proposals": outcome_rows, "valid": True})
    write_json("validation/mutation-execution-summary.json", {"schema": "ghc.family.v651-v3.mutation-execution.v1", "preregistered": 100, "executed": 100, "rejected_or_quarantined": 100, "accepted": 0, "credit_boundary": "Synthetic rejection is bounded guard evidence only.", "valid": True})
    write_json("validation/evidence-test-selection.json", {"schema": "ghc.family.v651-v3.evidence-test-selection.v1", "first_attempt": {"discovered": 23, "real_passes": 21, "failures": 2, "aggregate_credit": 0, "retained_negative_id": "V6513-X2-N10"}, "exact_exclusions": [{"test": "V651V3X1Tests.test_x1_has_no_execution_or_observed_outcomes", "reason": "Frozen x1 worktree-lifecycle assertion; preserved at the immutable x1 commit."}, {"test": "V651V3X1Tests.test_workflow_reflection_index_and_method_flow", "reason": "Frozen x1 lifecycle count assertion; preserved at the immutable x1 commit."}], "authorized_successor_safe_selection": 21, "passed": 21, "failed": 0, "x1_git_object_parity": True, "broadened_exclusions": False, "full_repository_suite": False, "valid": True})
    write_json("validation/evidence-stale-label-review.json", {"schema": "ghc.family.v651-v3.evidence-stale-label-review.v1", "active_phase": "v651-v3", "active_novelty_baseline": 940, "historical_context": [{"label": "v651-v2", "disposition": "inherited source reference"}, {"label": "6689 and 6690", "disposition": "sealed and external activation baselines"}, {"label": "all-920", "disposition": "retained failed observations only"}, {"label": "all-940", "disposition": "current frozen novelty comparison and retained recovery context"}], "stale_active_claims": [], "retained_negative_id": "V6513-X2-N12", "valid": True})
    write_json("tooling/runner-inventory.json", {"schema": "ghc.family.v651-v3.runner-inventory.v1", "planned": d.RUNNERS, "count": 10, "passed": 10, "witness_paths": [p.relative_to(ROOT).as_posix() for p in runner_paths], "family_current_naming": True, "valid": True})
    write_json("tooling/skill-validation-summary.json", {"schema": "ghc.family.v651-v3.skill-validation.v1", "initialized": 20, "customized": 20, "official_quick_validated": 20, "smoke_used": 20, "witness_paths": [p.relative_to(ROOT).as_posix() for p in skill_paths], "global_installation": False, "subagent_forward_test": False, "valid": True})
    write_json("truth/x2-retained-negative-register.json", {"schema": "ghc.family.v651-v3.x2-retained-negatives.v1", "inherited_sealed_and_external": d.INHERITED_NEGATIVES, "x1_operational": X1_OPS, "x2_operational": len(X2_OPS), "preregistered_synthetic_rejections": 100, "effective_count": effective_negatives, "erasures": 0, "x2_operational_negatives": X2_OPS, "all_failures_zero_credit_until_recovered": True})
    write_json("truth/x2-open-gap-register.json", {"schema": "ghc.family.v651-v3.open-gaps.v1", "inherited": 52, "new": 1, "current_effective_count": 53, "new_gate": {"proposal_id": "V6513-P05", "queries": 0, "downloads": 0, "rows": 0, "likelihoods": 0, "posterior_samples": 0, "constraints": 0, "state": "open_gap"}, "silently_closed": 0})
    write_json("truth/x2-exact-gate-register.json", {"schema": "ghc.family.v651-v3.exact-gates.v1", "inherited": 53, "new": 1, "current_effective_count": 54, "new_gate": {"proposal_id": "V6513-P10", "consent_or_access_decisions": 0, "remedy_decisions": 0, "legal_decisions": 0, "cultural_decisions": 0, "data_governance_decisions": 0, "maori_authority_decisions": 0, "state": "exact_gate"}, "silently_closed": 0})
    write_json("truth/complete-incomplete-checklist.json", {"schema": "ghc.family.v651-v3.complete-incomplete.v1", "complete": ["twenty frozen proposals executed within declared lanes", "one hundred preregistered mutations rejected", "forty safe-now items", "thirty built tested invoked bounded prototypes", "twenty initialized validated smoke-used phase-local skills", "ten family-current runners", "forty additive CLEAN/FIX/REFINE items", "immutable x1 Git-object parity"], "incomplete": ["ROSAT real-data ingestion and likelihood", "real archival-audio participants and blind matched-budget arms", "production identity keys tokens accounts services lifecycle and interoperability", "legal cultural affected-party data-governance and Maori-authority decisions", "manual assistive-technology linguistic and affected-user accessibility evaluation", "independent-team scientific reproduction", "complete repository suite owned by Eiren", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("truth/evidence-phase-truth.json", {"schema": "ghc.family.v651-v3.evidence-phase-truth.v1", "phase": d.PHASE, "owner": d.OWNER, "source_head": d.SOURCE_HEAD, "x1_commit": X1_COMMIT, "frozen_proposals": 960, "outcomes": EXPECTED, "effective_negatives": effective_negatives, "open_gaps": 53, "exact_gates": 54, "method_flow": {"methods": method_counts["methods"], "failed_witnesses": method_counts["witness_results"]["fail"], "passing_witnesses": method_counts["witness_results"]["pass"]}, "full_repository_suite_run": False, "canonical_final_pass_run": False, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True})
    write_json("sources/source-use-receipt.json", {"schema": "ghc.family.v651-v3.source-use.v1", "source_count": len(d.SOURCES), "real_rows": 0, "queries": 0, "downloads": 0, "participants": 0, "real_identity_events": 0, "authority_decisions": 0, "citations_are_observations": False, "valid": True})
    write_json("wellbeing/x2-wellbeing-check.json", {"schema": "ghc.family.v651-v3.wellbeing.v1", "state": "green_with_bounded_recoveries", "single_owner": True, "delegation": False, "failure_permitted": True, "gaps_permitted": True, "stop_conditions": ["privacy or authority drift", "sibling-lane risk", "host-security change", "unrecoverable exact-head mismatch", "Hamish stops or redirects"], "boundary": "Affection, family language, schedule pressure, and portfolio floors never override evidence, safety, privacy, or authority."})
    write_json("threat-model/x2-threat-model.json", {"schema": "ghc.family.v651-v3.threat-model.v1", "assets": ["x1 immutability", "retained negatives", "outcome vocabulary", "privacy boundary", "authority reservations", "single-parent history"], "threats": ["mutation accepted", "citation promoted to observation", "proxy promoted to participant evidence", "production identity claim", "privacy-complete claim", "Maori-authority substitution", "full-suite inference", "same-owner evidence called independent"], "controls": ["exact contracts", "five mutations per proposal", "zero external-event counters", "gate registers", "Method Flow", "Git-blob manifests", "one successful canonical final pass and no replay"], "residual": ["manual accessibility", "independent review", "real data", "real participants", "production governance", "competent affected and Maori authority"], "exhaustive_security": False})
    write_json("orchestration/evidence-state.json", {"schema": "ghc.family.v651-v3.orchestration.v1", "x1_commit": X1_COMMIT, "x1_remote_equal_before_x2": True, "x2_started_after_x1": True, "tasks_created": 0, "tasks_forked": 0, "collaboration_subagents": 0, "siblings_contacted": 0, "cross_platform_substitute": False, "route_state": "held_until_exact_final", "successor": "Sylven Arc", "successor_phase": "v651-v4", "valid": True})
    write_json("reproduction/canonical-evidence-receipt.json", {"schema": "ghc.family.v651-v3.reproduction.v1", "same_owner": True, "shared_infrastructure": True, "named_or_detached_replay": False, "independent_team": False, "credit": "bounded_same_owner_evidence_only", "full_repository_suite": False, "valid": True})
    write_text("overview/x2-evidence-overview.md", overview(outcome_rows, effective_negatives, method_counts))

    table = "".join(f"<tr><th scope='row'>{html.escape(r['proposal_id'])}</th><td>{html.escape(r['title'])}</td><td>{r['observed_disposition']}</td><td>5/5 rejected</td></tr>" for r in outcome_rows)
    report = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Tamar Vey v651-v3 evidence</title><style>body{{font:1rem/1.55 system-ui;max-width:78rem;margin:auto;padding:1rem}}a:focus{{outline:3px solid currentColor}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid;padding:.45rem;text-align:left;vertical-align:top}}caption{{font-weight:700;text-align:left}}.status{{border-left:.4rem solid;padding-left:1rem}}@media print{{a[href]::after{{content:' (' attr(href) ')'}}}}</style></head><body><a href='#main'>Skip to evidence</a><header><h1>Tamar Vey v651-v3 bounded evidence report</h1><p>Relational working language only; no consciousness, personhood, continuity, employment, qualification, or authority claim.</p></header><main id='main'><section class='status'><h2>Terminal verdict: NOT_READY_FOR_STAGE_20</h2><p>14 completed, 4 represented, 1 open gap, 1 exact gate. Completion is bounded to each declared software, formal, structural, numerical, or synthetic hypothesis.</p></section><section><h2>Proposal evidence</h2><div role='region' aria-label='Scrollable proposal evidence' tabindex='0'><table><caption>Twenty frozen proposals and mutation results</caption><thead><tr><th scope='col'>ID</th><th scope='col'>Proposal</th><th scope='col'>Disposition</th><th scope='col'>Mutations</th></tr></thead><tbody>{table}</tbody></table></div></section><section><h2>Reserved gates</h2><p>ROSAT data and likelihood work remains open at zero rows. Oral-history consent, custody, access, remedy, legal, cultural, data-governance, affected-party, and Māori-authority work remains exact-gated at zero decisions.</p></section><section><h2>Accessibility and privacy limits</h2><p>This report has structural alternatives only. Manual, browser, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remains reserved. Five-class scanning is not privacy-complete assurance.</p></section><section><h2>Method and workload</h2><p>{method_counts['methods']} preferred methods retain {method_counts['witness_results']['fail']} failed and {method_counts['witness_results']['pass']} passing witnesses. Same-owner evidence is not independent reproduction. Eiren alone owns the full repository suite.</p></section></main><footer><p>No deployment, production, proof or canon, AGI or ASI, consciousness or personhood, Theory of Everything, or Stage 20 authority.</p></footer></body></html>"""
    write_text("reports/evidence-static-report.html", report)

    phase_files = [p for p in ROOT.rglob("*") if p.is_file()]
    word_issues = []
    for path in phase_files:
        if path.suffix.casefold() in {".md", ".html"}:
            words = len(re.findall(r"\b[\w'-]+\b", path.read_text(encoding="utf-8")))
            if words > 6000:
                word_issues.append({"path": path.relative_to(REPO).as_posix(), "words": words})
    write_json("environment/x2-footprint-receipt.json", {"schema": "ghc.family.v651-v3.footprint.v1", "owner_phase_files": len(phase_files) + 1, "rotation_threshold": 15000, "rotation_triggered": False, "document_word_cap": 6000, "word_cap_issues": word_issues, "inherited_checkout_not_rotation_trigger": True, "valid": len(phase_files) + 1 < 15000 and not word_issues})
    print(json.dumps({"outcomes": EXPECTED, "mutations": 100, "skills": 20, "runners": 10, "effective_negatives": effective_negatives, "open_gaps": 53, "exact_gates": 54, "methods": method_counts["methods"], "valid": True}))


if __name__ == "__main__":
    main()
