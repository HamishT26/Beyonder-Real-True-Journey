#!/usr/bin/env python3
"""Build Orin Thale v651-v2 x2 evidence artifacts from executed bounded receipts."""

from __future__ import annotations

import hashlib
import html
import io
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import ghc_family_v651_v2_phase_data as d

ROOT = REPO / d.PHASE_ROOT
X1_COMMIT = "06c5545a79e992537b6307eb6a68e6d01204144d"
X1_MANIFEST_PATH = f"{d.PHASE_ROOT}/validation/x1-staged-manifest.json"
X1_OPS = 9
X2_OPS = [
    {"negative_id": "V6512-X2-N01", "summary": "The first official skill validation inherited CP1252 and failed before validating the first UTF-8 package; explicit PYTHONUTF8 recovered all twenty."},
    {"negative_id": "V6512-X2-N02", "summary": "A passing-only Method Flow method was promoted with no retained negative; the invalid summary received zero credit and the schema fault was retained."},
    {"negative_id": "V6512-X2-N03", "summary": "The first combined x1/x2 suite bound historical x1 absence assertions to the live x2 worktree; 25 checks passed and one failed, with zero aggregate credit."},
    {"negative_id": "V6512-X2-N04", "summary": "The first historical-test repair patch assumed the wrong import context and was rejected before changing any file."},
    {"negative_id": "V6512-X2-N05", "summary": "A read-only ripgrep alternation was split by PowerShell into a bogus filename after returning partial matches; literal separate searches recovered without mutation."},
]
SYNTHETIC_NEGATIVES = 100


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load(relative: str) -> object:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str, binary: bool = False) -> bytes | str:
    output = subprocess.check_output(["git", *args], cwd=REPO)
    return output if binary else output.decode("utf-8").strip()


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input="".join(oid + "\n" for oid in unique).encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    stream = io.BytesIO(proc.stdout)
    result = {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode().split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"unexpected blob header: {header}")
        size = int(header[2])
        payload = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("missing batch frame terminator")
        result[expected] = payload
    if stream.read():
        raise RuntimeError("unexpected trailing batch output")
    return result


def x1_parity() -> dict:
    manifest = json.loads(git("show", f"{X1_COMMIT}:{X1_MANIFEST_PATH}"))
    blobs = batch_blobs([entry["git_blob"] for entry in manifest["entries"]])
    issues = []
    for entry in manifest["entries"]:
        tree_oid = git("rev-parse", f"{X1_COMMIT}:{entry['path']}")
        data = blobs[entry["git_blob"]]
        if tree_oid != entry["git_blob"]:
            issues.append("blob:" + entry["path"])
        if len(data) != entry["bytes"]:
            issues.append("bytes:" + entry["path"])
        if hashlib.sha256(data).hexdigest() != entry["sha256"]:
            issues.append("sha256:" + entry["path"])
    return {
        "schema": "ghc.family.v651-v2.x1-immutability.v1",
        "x1_commit": X1_COMMIT,
        "entry_count": len(manifest["entries"]),
        "self_exclusion_count": len(manifest["self_exclusions"]),
        "issues": issues,
        "immutable_git_object_parity": not issues,
        "lifecycle_companions_may_advance_in_x2": [
            f"{d.PHASE_ROOT}/method-flow/method-flow-ledger.json",
            f"{d.PHASE_ROOT}/method-flow/method-flow-summary.json",
            f"{d.PHASE_ROOT}/method-flow/method-flow-summary.md",
            f"{d.PHASE_ROOT}/method-flow/method-flow-validation.json",
        ],
        "boundary": "The immutable x1 Git objects remain exact. Later lifecycle companions do not rewrite the x1 commit and receive no x1 fixed-point credit.",
        "valid": not issues,
    }


def main() -> None:
    if git("merge-base", "--is-ancestor", X1_COMMIT, "HEAD") != "":
        pass
    proposals = {p["proposal_id"]: p for p in d.PROPOSALS}
    receipts = [load(f"surfaces/{p['slug']}/bounded-receipt.json") for p in d.PROPOSALS]
    counts = Counter(row["observed_disposition"] for row in receipts)
    expected_counts = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
    if dict(counts) != expected_counts:
        raise SystemExit(f"outcome count mismatch: {dict(counts)}")
    mutation_rows = [row for p in d.PROPOSALS for row in load(f"surfaces/{p['slug']}/mutation-results.json")["results"]]
    if len(mutation_rows) != 100 or not all(row["passed"] for row in mutation_rows):
        raise SystemExit("mutation execution mismatch")
    runner_witnesses = sorted((ROOT / "tooling" / "runner-witnesses").glob("ghc_family_v651_v2_*.json"))
    if len(runner_witnesses) != 10 or not all(json.loads(path.read_text(encoding="utf-8"))["valid"] for path in runner_witnesses):
        raise SystemExit("runner witness mismatch")
    skill_witnesses = sorted((ROOT / "tooling" / "skill-witnesses").glob("*.json"))
    if len(skill_witnesses) != 20 or not all(json.loads(path.read_text(encoding="utf-8"))["valid"] for path in skill_witnesses):
        raise SystemExit("skill witness mismatch")
    parity = x1_parity()
    if not parity["valid"]:
        raise SystemExit(parity["issues"])
    write_json(ROOT / "provenance" / "x1-immutability-receipt.json", parity)
    method_counts = load("method-flow/method-flow-summary.json")["counts"]

    outcome_rows = []
    for proposal, receipt in zip(d.PROPOSALS, receipts, strict=True):
        outcome_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "pillar": proposal["pillar"],
                "observed_disposition": receipt["observed_disposition"],
                "accepting_fixture_passed": receipt["accepting_fixture_passed"],
                "mutation_rejected_count": receipt["mutation_rejected_count"],
                "source_ids": proposal["official_or_primary_source_needs"],
                "evidence": [
                    f"surfaces/{proposal['slug']}/contract.json",
                    f"surfaces/{proposal['slug']}/mutation-results.json",
                    f"surfaces/{proposal['slug']}/bounded-receipt.json",
                ],
                "real_rows": 0,
                "real_participants_or_operators": 0,
                "real_keys_or_network_events": 0,
                "authority_decisions": 0,
                "protected_gates": proposal["protected_gates"],
                "credit_boundary": receipt["boundary"],
            }
        )
    write_json(ROOT / "outcomes" / "evidence-ledger.json", {"schema": "ghc.family.v651-v2.evidence-ledger.v1", "phase": d.PHASE, "outcome_counts": expected_counts, "proposals": outcome_rows, "valid": True})
    write_json(ROOT / "validation" / "mutation-execution-summary.json", {"schema": "ghc.family.v651-v2.mutation-execution.v1", "preregistered": 100, "executed": 100, "rejected_or_quarantined": 100, "accepted": 0, "credit_boundary": "Synthetic rejections are bounded guard evidence only.", "valid": True})
    write_json(ROOT / "tooling" / "runner-inventory.json", {"schema": "ghc.family.v651-v2.runner-inventory.v1", "planned": d.RUNNERS, "witness_paths": [str(path.relative_to(ROOT)).replace("\\", "/") for path in runner_witnesses], "count": 10, "passed": 10, "family_current_naming": True, "valid": True})
    write_json(ROOT / "tooling" / "skill-validation-summary.json", {"schema": "ghc.family.v651-v2.skill-validation.v1", "initialized": 20, "customized": 20, "official_quick_validated": 20, "smoke_used": 20, "witness_paths": [str(path.relative_to(ROOT)).replace("\\", "/") for path in skill_witnesses], "global_installation": False, "subagent_forward_test": False, "subagent_forward_test_boundary": "Prohibited by the solo activation.", "valid": True})

    effective_negatives = d.INHERITED_NEGATIVES + X1_OPS + len(X2_OPS) + SYNTHETIC_NEGATIVES
    write_json(ROOT / "truth" / "x2-retained-negative-register.json", {"schema": "ghc.family.v651-v2.x2-retained-negatives.v1", "inherited_sealed_and_external": d.INHERITED_NEGATIVES, "x1_operational": X1_OPS, "x2_operational": len(X2_OPS), "preregistered_synthetic_rejections": SYNTHETIC_NEGATIVES, "effective_count": effective_negatives, "erasures": 0, "x2_operational_negatives": X2_OPS, "all_failures_zero_credit_until_recovered": True})
    write_json(ROOT / "truth" / "x2-open-gap-register.json", {"schema": "ghc.family.v651-v2.open-gaps.v1", "inherited": d.INHERITED_OPEN_GAPS, "new": 1, "current_effective_count": d.INHERITED_OPEN_GAPS + 1, "new_gate": {"proposal_id": "V6512-P05", "rows": 0, "queries": 0, "downloads": 0, "likelihoods": 0, "posterior_samples": 0, "state": "open_gap"}, "silently_closed": 0})
    write_json(ROOT / "truth" / "x2-exact-gate-register.json", {"schema": "ghc.family.v651-v2.exact-gates.v1", "inherited": d.INHERITED_EXACT_GATES, "new": 1, "current_effective_count": d.INHERITED_EXACT_GATES + 1, "new_gate": {"proposal_id": "V6512-P10", "service_decisions": 0, "remedy_decisions": 0, "legal_decisions": 0, "cultural_decisions": 0, "data_governance_decisions": 0, "maori_authority_decisions": 0, "state": "exact_gate"}, "silently_closed": 0})
    write_json(ROOT / "truth" / "complete-incomplete-checklist.json", {"schema": "ghc.family.v651-v2.complete-incomplete.v1", "complete": ["twenty frozen proposals executed within declared evidence lanes", "one hundred preregistered mutations rejected", "forty safe-now tasks", "thirty bounded candidates", "twenty initialized, validated, and smoke-used phase-local skills", "ten family-current runners", "forty additive CLEAN/FIX/REFINE tasks", "immutable x1 Git-object parity"], "incomplete": ["Hubble Source Catalog real-data ingestion and likelihood", "real localization participants and blinded matched-budget arms", "production identity keys, proofs, services, status, revocation, and interoperability", "legal, cultural, affected-party, data-governance, and Māori-authority decisions", "manual, assistive-technology, linguistic, and affected-user accessibility evaluation", "independent-team scientific reproduction", "complete repository suite, owned by Eiren", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json(ROOT / "truth" / "evidence-phase-truth.json", {"schema": "ghc.family.v651-v2.evidence-phase-truth.v1", "phase": d.PHASE, "owner": d.OWNER, "x1_commit": X1_COMMIT, "frozen_proposals": 940, "outcomes": expected_counts, "effective_negatives": effective_negatives, "open_gaps": 52, "exact_gates": 53, "method_flow": {"methods": method_counts["methods"], "failed_witnesses": method_counts["witness_results"]["fail"], "passing_witnesses": method_counts["witness_results"]["pass"]}, "full_repository_suite_run": False, "canonical_final_pass_run": False, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True})

    write_json(ROOT / "sources" / "source-use-receipt.json", {"schema": "ghc.family.v651-v2.source-use.v1", "source_count": len(d.SOURCES), "real_rows": 0, "queries": 0, "downloads": 0, "participants": 0, "real_keys": 0, "network_identity_events": 0, "authority_decisions": 0, "citations_are_observations": False, "valid": True})
    write_json(ROOT / "wellbeing" / "x2-wellbeing-check.json", {"schema": "ghc.family.v651-v2.wellbeing.v1", "state": "green_with_bounded_recoveries", "single_owner": True, "delegation": False, "failure_permitted": True, "gaps_permitted": True, "stop_conditions": ["privacy or authority drift", "sibling-lane risk", "host-security change", "unrecoverable exact-head mismatch", "Hamish stops or redirects"], "boundary": "Affection, family language, schedule pressure, and portfolio floors never override evidence, safety, privacy, or authority."})
    write_json(ROOT / "threat-model" / "x2-threat-model.json", {"schema": "ghc.family.v651-v2.threat-model.v1", "assets": ["x1 immutability", "retained negatives", "outcome vocabulary", "privacy boundary", "authority reservations", "single-parent history"], "threats": ["mutation accepted", "citation promoted to observation", "proxy promoted to participant evidence", "production identity claim", "privacy-complete claim", "Māori-authority substitution", "full-suite inference", "same-owner replay called independent"], "controls": ["exact contracts", "five mutations per proposal", "zero external-event counters", "gate registers", "Method Flow", "Git-blob manifests", "one successful canonical final pass and no replay"], "residual": ["manual accessibility", "independent review", "real data", "real participants", "production governance", "competent and affected authority"], "exhaustive_security": False})
    write_json(ROOT / "orchestration" / "evidence-state.json", {"schema": "ghc.family.v651-v2.orchestration.v1", "x1_commit": X1_COMMIT, "x1_remote_equal_before_x2": True, "x2_started_after_x1": True, "tasks_created": 0, "tasks_forked": 0, "collaboration_subagents": 0, "siblings_contacted": 0, "cross_platform_substitute": False, "route_state": "held_until_exact_final", "valid": True})
    write_json(ROOT / "reproduction" / "canonical-evidence-receipt.json", {"schema": "ghc.family.v651-v2.reproduction.v1", "same_owner": True, "shared_infrastructure": True, "named_or_detached_replay": False, "independent_team": False, "credit": "bounded_same_owner_evidence_only", "full_repository_suite": False, "valid": True})

    overview = f"""# Orin Thale v651-v2 x2 evidence overview

## Outcome first

The bounded v651-v2 execution produced exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate` outcomes. All labels describe only the frozen evidence lane. The phase rejects all one hundred preregistered synthetic mutations, preserves {effective_negatives:,} effective negatives, carries fifty-two open gaps and fifty-three exact gates, and remains `NOT_READY_FOR_STAGE_20`. No full repository suite, replay after success, independent-team reproduction, empirical likelihood, participant study, production identity event, authority decision, deployment, AGI or ASI, consciousness, personhood, legal interpretation, cultural ratification, or Māori-authority act occurred.

## Mind, Body, and Heart

THOS Body is the primary focus. The software-localization and timed-text workflows are representations only: their fixtures cover source and cue identity, placeholder and timing boundaries, correction readback, workload budgets, accessibility fallback, and handover ownership. They contain zero real translators, captioners, users, services, incidents, or matched-budget study arms. GMUT Mind remains a typed scalar-tensor and effective-field-theory research family. The Galileon and Vainshtein boards are formal obligation surfaces, while the Hubble Source Catalog adapter stays zero-row and open. Freed ID and CBR Heart remain synthetic and reserved: CWT and FedCM profiles use no keys, accounts, browsers, tokens, services, or network events, and the localization-authority matrix makes no remedy, legal, cultural, data-governance, or Māori-authority decision.

## Bounded tooling and failure truth

Eight proposal-group runners, one portfolio runner, and one current validator passed their declared owner-local gates. Forty safe-now tasks, thirty bounded candidates, and forty additive CLEAN/FIX/REFINE tasks completed without deletion, sibling mutation, elevation, security weakening, Windows feature change, global installation, or reboot. Twenty skills were initialized through the official skill-creator workflow, customized, officially validated under explicit UTF-8, and smoke-used against their exact proposal receipts. They were not globally installed, and the optional subagent forward test stayed unavailable because delegation is prohibited.

The x2 lifecycle retains {len(X2_OPS)} operational failures, including an initial CP1252 decode fault, an invalid passing-only Method Flow promotion, a historical test bound to the live tree, a rejected unverified-context patch, and a shell-split search alternation. Every first attempt receives zero credit. Their bounded recoveries preserve the original failures, and Method Flow closes this evidence boundary with {method_counts["methods"]} preferred methods, {method_counts["witness_results"]["fail"]} failed witnesses, and {method_counts["witness_results"]["pass"]} passing witnesses. The immutable x1 Git objects remain exact at `{X1_COMMIT}` even though declared Method Flow lifecycle companions advance in x2.

## Accessibility, privacy, and authority

The static report is structurally organized with headings, a skip link, labelled outcome and gate tables, textual status, and no colour-only meaning. That structure is useful evidence, not complete accessibility. Manual keyboard review, browser and responsive diversity, assistive-technology evaluation, cognitive review, localization review, Māori-language review, security-usability review, and affected-user evaluation remain reserved. Privacy checks are structural and cannot establish privacy completeness. Every legal, cultural, remedy, affected-party, terminology-stewardship, data-governance, and Māori wording or authority decision remains with competent people, affected parties, tangata whenua, iwi, hapū, and Māori authorities.

## Workload and closeout boundary

The workload remains one owner in one existing D-first lane under a four-commit cap. The x1 freeze was pushed and four-way remote-equal before x2. Evidence may proceed to its own exact staged review and commit; closeout may begin only after that evidence commit is independently re-read, pushed, clean, and four-way equal. The terminal route remains held until one exact-final canonical pass succeeds. No replay follows success, and only an acknowledged message to the exact existing `Tamar Vey` task can change the route state from prepared to sent.
"""
    write_text(ROOT / "overview" / "x2-evidence-overview.md", overview)

    table_rows = "".join(f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['observed_disposition'])}</td><td>5/5 rejected</td></tr>" for row in outcome_rows)
    report = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Orin Thale v651-v2 evidence</title><style>body{{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem}}a:focus,button:focus{{outline:3px solid currentColor}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid;padding:.45rem;text-align:left;vertical-align:top}}caption{{font-weight:700;text-align:left}}.status{{border-left:.4rem solid;padding-left:1rem}}@media print{{a[href]::after{{content:' (' attr(href) ')'}}}}</style></head><body><a href='#main'>Skip to evidence</a><header><h1>Orin Thale v651-v2 bounded evidence report</h1><p>Relational working language only; no consciousness, personhood, employment, continuity, qualification, or authority claim.</p></header><main id='main'><section class='status' aria-labelledby='verdict'><h2 id='verdict'>Terminal verdict: NOT_READY_FOR_STAGE_20</h2><p>Outcomes: 14 completed, 4 represented, 1 open gap, 1 exact gate. Completed means only the declared bounded software, formal, structural, numerical, or synthetic hypothesis.</p></section><section aria-labelledby='outcomes'><h2 id='outcomes'>Proposal evidence</h2><div role='region' aria-label='Scrollable proposal evidence' tabindex='0'><table><caption>Twenty frozen proposals and mutation results</caption><thead><tr><th scope='col'>ID</th><th scope='col'>Proposal</th><th scope='col'>Disposition</th><th scope='col'>Mutations</th></tr></thead><tbody>{table_rows}</tbody></table></div></section><section aria-labelledby='gates'><h2 id='gates'>Reserved gates</h2><p>Hubble data and likelihood work remains open with zero queries, downloads, rows, likelihoods, posteriors, or constraints. Localization access, remedy, legal, cultural, data-governance, affected-party, and Māori-authority work remains exact-gated with zero decisions.</p></section><section aria-labelledby='access'><h2 id='access'>Accessibility and privacy limits</h2><p>This report has structural alternatives only. Manual keyboard, browser, responsive, assistive-technology, cognitive, localization, Māori-language, security-usability, and affected-user evaluation remains reserved. Five-class scanning is not privacy-complete assurance.</p></section><section aria-labelledby='methods'><h2 id='methods'>Method and workload</h2><p>{method_counts["methods"]} preferred methods retain {method_counts["witness_results"]["fail"]} failed and {method_counts["witness_results"]["pass"]} passing witnesses. Same-owner bounded evidence is not independent-team reproduction. Eiren alone owns the full repository suite.</p></section></main><footer><p>No deployment, production, proof or canon, AGI or ASI, consciousness or personhood, Theory of Everything, or Stage 20 authority.</p></footer></body></html>"""
    write_text(ROOT / "reports" / "evidence-static-report.html", report)

    phase_files = sorted(path for path in ROOT.rglob("*") if path.is_file())
    word_issues = []
    for path in phase_files:
        if path.suffix.lower() in {".md", ".txt"}:
            words = len(path.read_text(encoding="utf-8").split())
            if words > 6000:
                word_issues.append({"path": str(path.relative_to(REPO)).replace("\\", "/"), "words": words})
    write_json(ROOT / "environment" / "x2-footprint-receipt.json", {"schema": "ghc.family.v651-v2.footprint.v1", "owner_phase_files": len(phase_files) + 1, "rotation_threshold": 15000, "rotation_triggered": False, "document_word_cap": 6000, "word_cap_issues": word_issues, "inherited_checkout_not_rotation_trigger": True, "valid": len(phase_files) + 1 < 15000 and not word_issues})
    print(json.dumps({"outcomes": expected_counts, "mutations": 100, "skills": 20, "runners": 10, "effective_negatives": effective_negatives, "open_gaps": 52, "exact_gates": 53, "phase_files": len(phase_files) + 1, "valid": True}))


if __name__ == "__main__":
    main()
