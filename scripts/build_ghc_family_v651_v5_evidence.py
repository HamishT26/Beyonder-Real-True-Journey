#!/usr/bin/env python3
"""Build Eiren Kestrel v651-v5 bounded x2 evidence ledgers."""

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
import ghc_family_v651_v5_phase_data as d  # noqa: E402

ROOT = REPO / d.PHASE_ROOT
X1_COMMIT = "c2c51a9e4f1786a45d77390b1d2e75e170dde170"
X1_MANIFEST = f"{d.PHASE_ROOT}/validation/x1-staged-manifest.json"
X1_OPS = 19
X2_OPS = [
    {"negative_id": "V6515-X2-N01", "summary": "A malformed JavaScript inspection wrapper used PowerShell array syntax and failed before reading or changing files.", "recovery": "Use valid JavaScript orchestration that emits a PowerShell command string, and retain the failed wrapper with zero credit."},
    {"negative_id": "V6515-X2-N02", "summary": "A broad x2 patch failed exact-context verification on an encoding-sensitive inherited sentence and applied no changes.", "recovery": "Use short stable patch anchors and retain the failed patch with zero credit."},
    {"negative_id": "V6515-X2-N03", "summary": "The first evidence build wrote correct JSON gate registers but its terminal summary printed inherited 54 and 55 gate totals.", "recovery": "Bind summary counts to the inherited constants plus the one current open gap and exact gate, then rebuild without changing evidence class."},
    {"negative_id": "V6515-X2-N04", "summary": "A combined artifact and Git inspection wrapper exceeded its bounded timeout before returning any usable state.", "recovery": "Split direct artifact reads from a separately bounded Git audit, avoid an all-in-one broad status wrapper, and retain the timed-out attempt with zero credit."},
    {"negative_id": "V6515-X2-N05", "summary": "The first isolated x2 rerun passed thirteen of fifteen tests but two assertions still expected the pre-timeout negative totals.", "recovery": "Update only the two stale retained-negative expectations after binding them to the additive failure ledger, then rerun the isolated x2 module."},
    {"negative_id": "V6515-X2-N06", "summary": "The second isolated x2 rerun passed fourteen of fifteen tests but a nearby effective-count assertion still held the older total.", "recovery": "Inspect the complete retained-negative assertion block, update all linked exact totals together, and rerun the isolated module without broadening any evidence claim."},
]
EXPECTED = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}


def write_json(relative: str, payload: dict) -> Path:
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
    process = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input="".join(oid + "\n" for oid in unique).encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    stream = io.BytesIO(process.stdout)
    result = {}
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
    return {
        "schema": "ghc.family.v651-v5.x1-immutability.v1",
        "x1_commit": X1_COMMIT,
        "entry_count": len(manifest["entries"]),
        "self_exclusion_count": len(manifest["self_exclusions"]),
        "issues": issues,
        "immutable_git_object_parity": not issues,
        "lifecycle_companions_advanced": [
            "method-flow/method-flow-ledger.json",
            "method-flow/method-flow-summary.json",
            "method-flow/method-flow-summary.md",
            "method-flow/method-flow-validation.json",
        ],
        "boundary": "Immutable x1 objects remain exact; append-only x2 lifecycle companions do not rewrite the x1 commit.",
        "valid": not issues,
    }


def overview(effective_negatives: int, methods: dict) -> str:
    return f"""# Eiren Kestrel v651-v5 bounded evidence overview

## Outcome first

All twenty frozen proposals executed only within their declared lanes. The distribution is exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. All one hundred preregistered mutations executed and were rejected or quarantined. The packet preserves {effective_negatives:,} effective negatives, now carries fifty-five open gaps and fifty-six exact gates, and remains `NOT_READY_FOR_STAGE_20`.

The completed label applies only to bounded owner-local software, symbolic, formal, numerical, structural, or synthetic hypotheses. It does not establish empirical confirmation, professional competence, production readiness, privacy completeness, exhaustive security, complete accessibility, independent reproduction, legal or cultural legitimacy, Māori authority, consciousness, personhood, a Theory of Everything, or Stage 20 readiness.

## Trinity Mandala and bounded practice

GMUT Mind is primary. The greenhouse climate and fertigation handover surfaces remain synthetic representations with zero real workers, sites, crops, equipment, chemicals, water batches, alarms, incidents, blind matched-budget arms, or operational-effectiveness estimates. The structural format, concurrency, accessibility, numerical, and data-structure surfaces complete only their declared bounded guard hypotheses.

GMUT Mind remains a typed scalar-tensor and EFT research-model family. The York-Lichnerowicz and Regge-Wheeler-Zerilli boards are typed obligation and mutation guards only. They establish no physical state, solution, force, prediction, likelihood, constraint, stability theorem, empirical confirmation, ultraviolet completion, or Theory of Everything. The Roman WFI prelaunch adapter remains an open gap with zero queries, downloads, rows, likelihood evaluations, posterior samples, or constraints.

Freed ID and CBR Heart remain synthetic and nonproduction. The ECDSA-SD and RFC 8693 token-exchange profiles use zero real keys, proofs, credentials, clients, tokens, accounts, services, network calls, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. The greenhouse authority matrix remains exact-gated and makes no safety, environmental, privacy, remedy, legal, cultural, data-governance, affected-party, or Māori-authority decision.

The bounded human-practice lens was commercial-greenhouse climate control, fertigation exception review, chemical and biosecurity refusal, accessible notice, workload control, correction readback, and shift handover. It was synthetic learning and design only. It establishes no employment, qualification, horticulture competence, chemical or biosecurity competence, environmental authority, operational authority, participant evidence, legal interpretation, cultural legitimacy, Māori authority, affected-party acceptance, or operational outcome.

## Portfolios, skills, runners, and Method Flow

Forty new safe-now items, thirty bounded candidate prototypes, twenty phase-local skills, ten family-current runners, and forty additive CLEAN/FIX/REFINE items passed their declared owner-local gates. The thirty candidates were built, tested, and invoked. All skills were initialized with the official skill-creator workflow, customized, validated under an explicit UTF-8 envelope, and smoke-used. They were not globally installed, and no subagent forward test ran because this phase expressly forbids delegation.

The ten runners preserve family-current `ghc_family_*` naming. Eight proposal-group runners emitted twenty bounded surface receipts, one portfolio runner emitted exact 40/30/20/10/40 evidence, and the aggregate runner confirmed twenty surfaces and one hundred mutations. These are useful bounded engineering tools, never production certification or independent audit.

Method Flow contains {methods['methods']} preferred methods, {methods['witness_results']['fail']} retained failed witnesses, and {methods['witness_results']['pass']} bounded passing witnesses. The {len(X2_OPS)} x2 operational failures are enumerated in the retained-negative register. Every first attempt retains zero credit; recovery does not erase it.

## Validation and route boundary

The dedicated x1 commit `{X1_COMMIT}` replays exactly across 109 manifest entries plus three self-exclusions. Eiren alone owns the complete repository suite. The current phase uses bounded current, inherited-source, recent, and successor-scoped checks with one credited exact-final canonical pass and no replay after success.

Public artifacts exclude private identifiers, routes, transcripts, credentials, keys, tokens, private application state, session streams, screenshots, and private absolute paths. Five-class scanning is bounded hygiene, not privacy completeness. The successor route remains held until a clean pushed exact final passes every terminal gate. Only tool acknowledgement of one exact-title message to `Ilyra Fen` for v651-v6 may change the route truth to sent.
"""


def main() -> None:
    if subprocess.run(["git", "merge-base", "--is-ancestor", X1_COMMIT, "HEAD"], cwd=REPO).returncode:
        raise RuntimeError("x1 is not ancestral")
    receipts = [load(f"surfaces/{proposal['slug']}/bounded-receipt.json") for proposal in d.PROPOSALS]
    counts = Counter(row["observed_disposition"] for row in receipts)
    if dict(counts) != EXPECTED:
        raise RuntimeError(counts)
    mutation_rows = [
        row
        for proposal in d.PROPOSALS
        for row in load(f"surfaces/{proposal['slug']}/mutation-results.json")["results"]
    ]
    if len(mutation_rows) != 100 or not all(row["passed"] for row in mutation_rows):
        raise RuntimeError("mutation execution mismatch")
    runner_paths = sorted((ROOT / "tooling/runner-witnesses").glob("ghc_family_v651_v5_*.json"))
    skill_paths = sorted((ROOT / "tooling/skill-witnesses").glob("*.json"))
    if len(runner_paths) != 10 or not all(json.loads(path.read_text(encoding="utf-8"))["valid"] for path in runner_paths):
        raise RuntimeError("runner witnesses")
    if len(skill_paths) != 20 or not all(json.loads(path.read_text(encoding="utf-8"))["valid"] for path in skill_paths):
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
        outcome_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "pillar": proposal["pillar"],
                "observed_disposition": receipt["observed_disposition"],
                "accepting_fixture_passed": True,
                "mutation_rejected_count": 5,
                "source_ids": proposal["official_or_primary_source_needs"],
                "real_rows": 0,
                "real_participants_or_operators": 0,
                "real_identity_or_network_events": 0,
                "authority_decisions": 0,
                "protected_gates": proposal["protected_gates"],
                "credit_boundary": receipt["boundary"],
            }
        )

    write_json("outcomes/evidence-ledger.json", {"schema": "ghc.family.v651-v5.evidence-ledger.v1", "phase": d.PHASE, "outcome_counts": EXPECTED, "proposals": outcome_rows, "valid": True})
    write_json("validation/mutation-execution-summary.json", {"schema": "ghc.family.v651-v5.mutation-execution.v1", "preregistered": 100, "executed": 100, "rejected_or_quarantined": 100, "accepted": 0, "credit_boundary": "Synthetic rejection is bounded guard evidence only.", "valid": True})
    write_json("tooling/runner-inventory.json", {"schema": "ghc.family.v651-v5.runner-inventory.v1", "planned": d.RUNNERS, "count": 10, "passed": 10, "witness_paths": [path.relative_to(ROOT).as_posix() for path in runner_paths], "family_current_naming": True, "valid": True})
    write_json("tooling/skill-validation-summary.json", {"schema": "ghc.family.v651-v5.skill-validation.v1", "initialized": 20, "customized": 20, "official_quick_validated": 20, "smoke_used": 20, "witness_paths": [path.relative_to(ROOT).as_posix() for path in skill_paths], "global_installation": False, "subagent_forward_test": False, "valid": True})
    write_json("truth/x2-retained-negative-register.json", {"schema": "ghc.family.v651-v5.x2-retained-negatives.v1", "inherited_sealed_and_external": d.INHERITED_NEGATIVES, "x1_operational": X1_OPS, "x2_operational": len(X2_OPS), "preregistered_synthetic_rejections": 100, "effective_count": effective_negatives, "erasures": 0, "x2_operational_negatives": X2_OPS, "all_failures_zero_credit_until_recovered": True})
    write_json("truth/x2-open-gap-register.json", {"schema": "ghc.family.v651-v5.open-gaps.v1", "inherited": d.INHERITED_OPEN_GAPS, "new": 1, "current_effective_count": d.INHERITED_OPEN_GAPS + 1, "new_gate": {"proposal_id": "V6515-P05", "queries": 0, "downloads": 0, "rows": 0, "likelihoods": 0, "posterior_samples": 0, "constraints": 0, "state": "open_gap"}, "silently_closed": 0})
    write_json("truth/x2-exact-gate-register.json", {"schema": "ghc.family.v651-v5.exact-gates.v1", "inherited": d.INHERITED_EXACT_GATES, "new": 1, "current_effective_count": d.INHERITED_EXACT_GATES + 1, "new_gate": {"proposal_id": "V6515-P10", "safety_or_environmental_decisions": 0, "privacy_or_remedy_decisions": 0, "legal_decisions": 0, "cultural_decisions": 0, "data_governance_decisions": 0, "maori_authority_decisions": 0, "state": "exact_gate"}, "silently_closed": 0})
    write_json("truth/complete-incomplete-checklist.json", {"schema": "ghc.family.v651-v5.complete-incomplete.v1", "complete": ["twenty frozen proposals executed within declared lanes", "one hundred preregistered mutations rejected", "forty safe-now items", "thirty built tested invoked bounded prototypes", "twenty initialized validated smoke-used phase-local skills", "ten family-current runners", "forty additive CLEAN/FIX/REFINE items", "immutable x1 Git-object parity"], "incomplete": ["Roman WFI real-data ingestion and likelihood", "real greenhouse workers sites crops chemicals incidents and blind matched-budget arms", "production identity keys proofs accounts services lifecycle and interoperability", "legal cultural affected-party data-governance and Māori-authority decisions", "manual assistive-technology linguistic and affected-user accessibility evaluation", "independent-team scientific reproduction", "complete repository suite at exact final", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("truth/evidence-phase-truth.json", {"schema": "ghc.family.v651-v5.evidence-phase-truth.v1", "phase": d.PHASE, "owner": d.OWNER, "source_head": d.SOURCE_HEAD, "x1_commit": X1_COMMIT, "frozen_proposals": d.PRIOR_FROZEN + len(d.PROPOSALS), "outcomes": EXPECTED, "effective_negatives": effective_negatives, "open_gaps": d.INHERITED_OPEN_GAPS + 1, "exact_gates": d.INHERITED_EXACT_GATES + 1, "method_flow": {"methods": method_counts["methods"], "failed_witnesses": method_counts["witness_results"]["fail"], "passing_witnesses": method_counts["witness_results"]["pass"]}, "full_repository_suite_run": False, "canonical_final_pass_run": False, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True})
    write_json("sources/source-use-receipt.json", {"schema": "ghc.family.v651-v5.source-use.v1", "source_count": len(d.SOURCES), "real_rows": 0, "queries": 0, "downloads": 0, "participants": 0, "real_identity_events": 0, "authority_decisions": 0, "citations_are_observations": False, "valid": True})
    write_json("wellbeing/x2-wellbeing-check.json", {"schema": "ghc.family.v651-v5.wellbeing.v1", "state": "green_with_bounded_recoveries", "single_owner": True, "delegation": False, "failure_permitted": True, "gaps_permitted": True, "stop_conditions": ["privacy or authority drift", "sibling-lane risk", "host-security change", "unrecoverable exact-head mismatch", "Hamish stops or redirects"], "boundary": "Affection, family language, schedule pressure, and portfolio floors never override evidence, safety, privacy, or authority."})
    write_json("threat-model/x2-threat-model.json", {"schema": "ghc.family.v651-v5.threat-model.v1", "assets": ["x1 immutability", "retained negatives", "outcome vocabulary", "privacy boundary", "authority reservations", "single-parent history"], "threats": ["mutation accepted", "citation promoted to observation", "proxy promoted to participant evidence", "production identity claim", "privacy-complete claim", "Māori-authority substitution", "full-suite inference", "same-owner evidence called independent"], "controls": ["exact contracts", "five mutations per proposal", "zero external-event counters", "gate registers", "Method Flow", "Git-blob manifests", "one successful canonical final pass and no replay"], "residual": ["manual accessibility", "independent review", "real data", "real participants", "production governance", "competent affected and Māori authority"], "exhaustive_security": False})
    write_json("orchestration/evidence-state.json", {"schema": "ghc.family.v651-v5.orchestration.v1", "x1_commit": X1_COMMIT, "x1_remote_equal_before_x2": True, "x2_started_after_x1": True, "tasks_created": 0, "tasks_forked": 0, "collaboration_subagents": 0, "siblings_contacted": 0, "cross_platform_substitute": False, "route_state": "held_until_exact_final", "successor": "Ilyra Fen", "successor_phase": "v651-v6", "valid": True})
    write_json("reproduction/canonical-evidence-receipt.json", {"schema": "ghc.family.v651-v5.reproduction.v1", "same_owner": True, "shared_infrastructure": True, "named_or_detached_replay": False, "independent_team": False, "credit": "bounded_same_owner_evidence_only", "full_repository_suite": False, "valid": True})
    write_text("overview/x2-evidence-overview.md", overview(effective_negatives, method_counts))

    table = "".join(f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{row['observed_disposition']}</td><td>5/5 rejected</td></tr>" for row in outcome_rows)
    report = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Eiren Kestrel v651-v5 evidence</title><style>body{{font:1rem/1.55 system-ui;max-width:78rem;margin:auto;padding:1rem}}a:focus{{outline:3px solid currentColor}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid;padding:.45rem;text-align:left;vertical-align:top}}caption{{font-weight:700;text-align:left}}.status{{border-left:.4rem solid;padding-left:1rem}}@media print{{a[href]::after{{content:' (' attr(href) ')'}}}}</style></head><body><a href='#main'>Skip to evidence</a><header><h1>Eiren Kestrel v651-v5 bounded evidence report</h1><p>Relational working language only; no consciousness, personhood, continuity, employment, qualification, or authority claim.</p></header><main id='main'><section class='status'><h2>Terminal verdict: NOT_READY_FOR_STAGE_20</h2><p>14 completed, 4 represented, 1 open gap, 1 exact gate. Completion is bounded to each declared software, formal, structural, numerical, or synthetic hypothesis.</p></section><section><h2>Proposal evidence</h2><div role='region' aria-label='Scrollable proposal evidence' tabindex='0'><table><caption>Twenty frozen proposals and mutation results</caption><thead><tr><th scope='col'>ID</th><th scope='col'>Proposal</th><th scope='col'>Disposition</th><th scope='col'>Mutations</th></tr></thead><tbody>{table}</tbody></table></div></section><section><h2>Reserved gates</h2><p>Roman WFI work remains query-free at zero rows. Greenhouse safety, environmental harm, privacy, remedy, legal, cultural, data-governance, affected-party, and Māori-authority work remains exact-gated at zero decisions.</p></section><section><h2>Accessibility and privacy limits</h2><p>This report has structural alternatives only. Manual, browser, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remains reserved. Five-class scanning is not privacy-complete assurance.</p></section><section><h2>Method and workload</h2><p>{method_counts['methods']} preferred methods retain {method_counts['witness_results']['fail']} failed and {method_counts['witness_results']['pass']} passing witnesses. Same-owner evidence is not independent reproduction. Eiren alone owns the full repository suite.</p></section></main><footer><p>No deployment, production, proof or canon, AGI or ASI, consciousness or personhood, Theory of Everything, or Stage 20 authority.</p></footer></body></html>"""
    write_text("reports/evidence-static-report.html", report)

    phase_files = [path for path in ROOT.rglob("*") if path.is_file()]
    word_issues = []
    for path in phase_files:
        if path.suffix.casefold() in {".md", ".html"}:
            words = len(re.findall(r"\b[\w'-]+\b", path.read_text(encoding="utf-8")))
            if words > 6000:
                word_issues.append({"path": path.relative_to(REPO).as_posix(), "words": words})
    write_json("environment/x2-footprint-receipt.json", {"schema": "ghc.family.v651-v5.footprint.v1", "owner_phase_files": len(phase_files) + 1, "rotation_threshold": 15000, "rotation_triggered": False, "document_word_cap": 6000, "word_cap_issues": word_issues, "inherited_checkout_not_rotation_trigger": True, "valid": len(phase_files) + 1 < 15000 and not word_issues})
    print(json.dumps({"outcomes": EXPECTED, "mutations": 100, "skills": 20, "runners": 10, "effective_negatives": effective_negatives, "open_gaps": d.INHERITED_OPEN_GAPS + 1, "exact_gates": d.INHERITED_EXACT_GATES + 1, "methods": method_counts["methods"], "valid": True}))


if __name__ == "__main__":
    main()
