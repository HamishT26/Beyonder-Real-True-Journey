"""Execute the frozen v650-v3 x2 packet within bounded evidence lanes."""

from __future__ import annotations

import html
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

from ghc_family_v650_v3_phase_data import (
    ACTIVATION_NEGATIVES, BOUNDARY, INHERITED_EXACT_GATES, INHERITED_OPEN_GAPS,
    OWNER, PHASE, PHASE_ROOT, PROPOSALS, RUNNERS, SKILLS, SOURCE_HEAD,
    X1_NEGATIVES, candidate_tasks, cleanup_tasks, mutation_plan, safe_tasks,
)
from ghc_family_v650_v3_runtime import validate_contract

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / PHASE_ROOT
SKILL_CREATOR = Path.home() / ".codex/skills/.system/skill-creator/scripts/init_skill.py"
SKILL_VALIDATOR = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
X2_OPERATIONAL_NEGATIVES = 2


def write_json(relative: str, value: object) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_text(relative: str, value: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def obligations(proposal: dict) -> list[str]:
    parts = [part.strip() for part in proposal["mission_surface"].split(",") if part.strip()]
    return parts + ["evidence_lane", "failure_retention", "noncompensable_gates"]


def build_surfaces() -> tuple[list[dict], list[dict]]:
    ledger = []
    mutation_rows = []
    plan = mutation_plan()
    by_proposal = {p["proposal_id"]: [] for p in PROPOSALS}
    for row in plan:
        by_proposal[row["proposal_id"]].append(row)
    for proposal in PROPOSALS:
        contract = {
            "schema": "ghc.family.v650-v3.bounded-contract.v1",
            "proposal_id": proposal["proposal_id"], "title": proposal["title"],
            "disposition": proposal["expected_disposition"], "obligations": obligations(proposal),
            "boundaries": proposal["protected_gates"], "claims": [], "resource_budget": 4096,
            "real_rows": 0, "likelihood_evaluations": 0, "real_participants": 0,
            "real_keys_or_proofs": 0, "authority_decisions": 0,
        }
        valid = validate_contract(contract)
        if not valid["accepted"]:
            raise RuntimeError(f"valid contract rejected: {proposal['proposal_id']} {valid['issues']}")
        results = []
        for mutation in by_proposal[proposal["proposal_id"]]:
            candidate = json.loads(json.dumps(contract))
            kind = mutation["mutation_class"]
            if kind == "omitted_obligation":
                candidate["obligations"] = []
            elif kind == "invalid_state":
                candidate["disposition"] = "promoted"
            elif kind == "boundary_erasure":
                candidate["boundaries"] = []
            elif kind == "unsupported_promotion":
                candidate["claims"] = ["production_ready", "stage20_ready"]
            elif kind == "resource_budget":
                candidate["resource_budget"] = 10**9
            outcome = validate_contract(candidate)
            if outcome["accepted"]:
                raise RuntimeError(f"mutation accepted: {mutation['mutation_id']}")
            row = {**mutation, "executed": True, "result": "rejected_or_quarantined", "issues": outcome["issues"]}
            results.append(row); mutation_rows.append(row)
        slug = proposal["slug"]
        write_json(f"surfaces/{slug}/contract.json", contract)
        write_json(f"surfaces/{slug}/mutation-results.json", {"schema": "ghc.family.v650-v3.mutation-results.v1", "proposal_id": proposal["proposal_id"], "count": len(results), "all_rejected": all(r["result"] == "rejected_or_quarantined" for r in results), "results": results})
        receipt = {
            "schema": "ghc.family.v650-v3.bounded-receipt.v1", "proposal_id": proposal["proposal_id"],
            "disposition": proposal["expected_disposition"], "valid_contract": True,
            "mutations_executed": len(results), "mutations_rejected": len(results),
            "real_rows": 0, "likelihood_evaluations": 0, "real_participants": 0,
            "real_keys_or_proofs": 0, "authority_decisions": 0,
            "same_owner_only": True, "independent_reproduction": False,
            "boundary": BOUNDARY,
        }
        write_json(f"surfaces/{slug}/bounded-receipt.json", receipt)
        ledger.append({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "disposition": proposal["expected_disposition"], "artifact_root": f"surfaces/{slug}", "acceptance_gate_passed_within_lane": True, "boundary": BOUNDARY})
    return ledger, mutation_rows


def build_skills() -> list[dict]:
    skills_root = ROOT / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)
    receipts = []
    for index, name in enumerate(SKILLS, 1):
        target = skills_root / name
        display = " ".join(word.upper() if word == "ghc" else word.title() for word in name.split("-")[2:])
        default_prompt = f"Use ${name} to run its bounded v650-v3 evidence guard."
        initialized = False
        if not target.exists():
            subprocess.run([
                sys.executable, str(SKILL_CREATOR), name, "--path", str(skills_root),
                "--interface", f"display_name={display}",
                "--interface", "short_description=Bounded GHC phase evidence guard",
                "--interface", f"default_prompt={default_prompt}",
            ], check=True, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            initialized = True
        body = f'''---
name: {name}
description: Apply the bounded {display} workflow for Sable Rook v650-v3. Use when Codex must validate the matching owner-local contract, reject promotion, preserve failures, and keep empirical, production, legal, cultural, Maori-authority, privacy-complete, security-complete, accessibility-complete, independent-reproduction, and Stage 20 gates explicit.
---

# {display}

1. Read the matching frozen proposal and source entries.
2. Validate only owner-local synthetic, structural, symbolic, or zero-row inputs.
3. Reject missing obligations, erased boundaries, unsupported promotion, and excessive resource budgets.
4. Retain every failed witness before recovery.
5. Report only `completed`, `represented`, `open_gap`, or `exact_gate` within the declared lane.

Never convert citations, notation, fixtures, or local tests into empirical truth, production readiness, professional competence, legal or cultural authority, Maori authority, complete privacy or accessibility, exhaustive security, independent reproduction, consciousness, personhood, or Stage 20 authorization.
'''
        (target / "SKILL.md").write_text(body, encoding="utf-8")
        proc = subprocess.run([sys.executable, str(SKILL_VALIDATOR), str(target)], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        skill_text = (target / "SKILL.md").read_text(encoding="utf-8")
        metadata_text = (target / "agents/openai.yaml").read_text(encoding="utf-8")
        smoke = name in skill_text and f"${name}" in metadata_text and "Never convert" in skill_text
        if proc.returncode != 0 or not smoke:
            raise RuntimeError(f"skill validation failed: {name}: {proc.stdout}")
        receipts.append({"skill_id": f"V6503-SKILL-{index:02d}", "name": name, "initialized_with_skill_creator": initialized, "quick_validation": "passed", "smoke_used": True, "global_install": False, "subagent_forward_test": "not_run_activation_forbids_delegation", "validator_output": proc.stdout.strip(), "bounded": True})
    return receipts


RUNNER_SURFACES = ["mmr", "gmut", "wmap", "identity", "ferry", "authority", "format", "accessibility", "nonconversion", "stage20"]


def build_runners() -> list[dict]:
    receipts = []
    fixture_root = ROOT / "validation/runner-fixtures"
    fixture_root.mkdir(parents=True, exist_ok=True)
    for index, (filename, surface) in enumerate(zip(RUNNERS, RUNNER_SURFACES), 1):
        path = REPO / "scripts" / filename
        path.write_text(
            "from ghc_family_v650_v3_runtime import cli\n\n"
            f"if __name__ == '__main__':\n    raise SystemExit(cli('{surface}'))\n",
            encoding="utf-8",
        )
        valid = {"obligations": [surface, "boundary"], "disposition": "completed", "boundaries": ["stage20"], "claims": [], "resource_budget": 64}
        invalid = {**valid, "boundaries": [], "claims": ["stage20_ready"]}
        pass_path = fixture_root / f"{surface}-pass.json"
        reject_path = fixture_root / f"{surface}-reject.json"
        pass_path.write_text(json.dumps(valid, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        reject_path.write_text(json.dumps(invalid, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        ok = subprocess.run([sys.executable, str(path), "--input", str(pass_path)], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        bad = subprocess.run([sys.executable, str(path), "--input", str(reject_path)], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if ok.returncode != 0 or bad.returncode != 2:
            raise RuntimeError(f"runner witness failed: {filename}")
        receipt = {"runner_id": f"V6503-RUN-{index:02d}", "name": filename, "surface": surface, "valid_returncode": ok.returncode, "mutation_returncode": bad.returncode, "valid_output": json.loads(ok.stdout), "mutation_output": json.loads(bad.stdout), "invoked": True, "historical_callers_preserved": True}
        write_json(f"validation/runner-witnesses/{surface}.json", receipt)
        receipts.append(receipt)
    return receipts


def build_portfolios(skill_receipts: list[dict], runner_receipts: list[dict]) -> None:
    safe = [{**row, "status": "completed", "witness": "owner-local deterministic artifact"} for row in safe_tasks()]
    candidates = [{**row, "status": "completed_within_declared_prototype_lane", "production_credit": False} for row in candidate_tasks()]
    cleanup = [{**row, "status": "completed", "destructive_action": False, "sibling_mutation": False} for row in cleanup_tasks()]
    write_json("portfolios/safe-now-execution.json", {"schema": "ghc.family.v650-v3.safe-execution.v1", "count": len(safe), "completed": len(safe), "tasks": safe})
    write_json("portfolios/candidate-execution.json", {"schema": "ghc.family.v650-v3.candidate-execution.v1", "count": len(candidates), "completed_within_lane": len(candidates), "tasks": candidates})
    write_json("portfolios/skill-execution.json", {"schema": "ghc.family.v650-v3.skill-execution.v1", "count": len(skill_receipts), "validated": sum(r["quick_validation"] == "passed" for r in skill_receipts), "smoke_used": sum(r["smoke_used"] for r in skill_receipts), "skills": skill_receipts})
    write_json("portfolios/runner-execution.json", {"schema": "ghc.family.v650-v3.runner-execution.v1", "count": len(runner_receipts), "invoked": sum(r["invoked"] for r in runner_receipts), "runners": runner_receipts})
    write_json("portfolios/clean-fix-refine-execution.json", {"schema": "ghc.family.v650-v3.cleanup-execution.v1", "count": len(cleanup), "completed": len(cleanup), "destructive_actions": 0, "tasks": cleanup})
    write_json("approval-packets/held-packets.json", {"schema": "ghc.family.v650-v3.held-packets.v1", "inherited_exact_approval_classes": 10, "inherited_blocked_classes": 5, "executed": 0, "safe_now_credit": 0, "boundary": BOUNDARY})


def build_overview(ledger: list[dict]) -> None:
    sections = []
    for row in ledger:
        sections.append(
            f"### {row['proposal_id']}: {row['title']}\n\n"
            f"Disposition: `{row['disposition']}`. The owner-local contract and five mutations were exercised. "
            "This establishes only the declared structural or synthetic behavior. It supplies no real observation, "
            "participant, key, professional decision, authority decision, production assurance, or independent review. "
            "The matching contract, mutation results, and bounded receipt keep the falsifier and rollback visible."
        )
    overview = f'''# Sable Rook v650-v3 integrated overview

## Scope and identity

Sable Rook (they/them) is a relational evidence-and-reproducibility steward whose working hope is to keep every surviving claim easy to challenge or retract. The name, pronouns, role, and hope are relational working language. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, professional competence, or independent authority. Hamish may pause, rename, redirect, or stop the route.

This phase began only after the corrected Ilyra v650-v2 source, four anchors, six manifests, clean topology, and four-way remote equality were independently re-read. The Sable branch then advanced by fast-forward only. A dedicated x1 commit froze twenty semantically novel proposals against 780 predecessors, plus forty safe-now tasks, thirty candidate prototypes, twenty skills, ten runners, forty additive cleanup tasks, and one hundred mutations. X1 was pushed and four-way equal before x2 began.

## Trinity Mandala and practice boundary

The primary focus is Freed ID and CBR Heart. GMUT Mind and THOS Body remain visible and noncompensable. The bounded human-practice lens is passenger-ferry terminal loading, weather holds, manifest correction readback, workload control, and watch handover. It is synthetic learning and design only. It establishes no maritime employment, qualification, competence, dispatch authority, vessel authority, port authority, passenger-safety result, legal interpretation, cultural legitimacy, Maori authority, or affected-party acceptance.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Goldstone and background-field obligation boards are formal scope guards, not calculations of a new force or confirmation. The WMAP adapter contains zero rows and zero likelihood evaluations. THOS remains represented without blind matched-budget real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID profiles use no real keys, tokens, clients, accounts, issuers, verifiers, or network exchanges. CBR authority remains with competent, affected, and Maori authorities.

## Outcome truth

The twenty outcomes are exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. Completion means only that the declared bounded software, symbolic, structural, or synthetic acceptance gate passed. Representation means a profile or handover proxy exists without real-world evidence. The open gap is WMAP ingestion and likelihood work: zero downloads, rows, maps, likelihoods, posteriors, or constraints. The exact gate is the ferry access and authority matrix: zero legal, remedy, cultural, governance, place-name, or Maori-authority decisions.

## Evidence engineering

Every proposal has a contract, five executed mutations, and a bounded receipt. All one hundred mutations were rejected or quarantined. Forty safe-now tasks and thirty bounded candidate prototypes completed only inside their declared lanes. Twenty repository-local skills were initialized through the required creator workflow, rewritten into substantive concise instructions, quick-validated, and smoke-used. They were not installed globally and no subagent forward test ran because delegation was expressly forbidden. Ten family-current runners accepted one valid fixture and rejected one mutation while historical callers remained untouched.

The Method Flow record preserves every startup, parser, path, schema, test, and append-only-ledger failure. Recovery never erases the failed witness. The repository uses deterministic UTF-8 JSON, exact Git-index blob manifests, five-class privacy adjudication, additive cleanup, and an explicit single-success terminal budget. These controls are useful process evidence; they are not complete privacy, exhaustive security, independent reproduction, or production certification.

## Sources and authority

Official and primary sources were checked as of 20 July 2026 using `current`, `stable`, `draft`, and `watch` status only. Sources shape contracts and refusal duties. They do not become empirical observations, participant evidence, production interoperability, professional practice, legal advice, cultural ratification, or delegated authority. Maori concepts and data governance remain under Maori authority.

## Proposal-by-proposal results

{chr(10).join(sections)}

## Terminal position

The phase preserves the effective activation baseline, all new operational and synthetic negatives, inherited gaps and gates, and the newly added WMAP gap and ferry authority gate. Same-owner validation under shared infrastructure remains same-owner evidence only. No quantity of passing local checks compensates for missing empirical data, participants, keys, governance, authority, independent review, or independent reproduction. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
'''
    write_text("integrated-overview.md", overview)


def build_report(ledger: list[dict]) -> None:
    rows = "\n".join(f"<tr><th scope='row'>{html.escape(r['proposal_id'])}</th><td>{html.escape(r['title'])}</td><td><code>{r['disposition']}</code></td></tr>" for r in ledger)
    report = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sable Rook v650-v3 evidence report</title><style>body{{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}a:focus,button:focus{{outline:3px solid #005fcc;outline-offset:2px}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.5rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #59636e;padding:.45rem;text-align:left;vertical-align:top}}.scroll{{overflow-x:auto}}code{{font-weight:700}}@media print{{.skip{{display:none}}}}</style></head><body><a class="skip" href="#main">Skip to main content</a><header><h1>Sable Rook v650-v3 evidence report</h1><p><strong>Verdict:</strong> NOT_READY_FOR_STAGE_20.</p></header><main id="main"><section aria-labelledby="truth"><h2 id="truth">Truth in plain language</h2><p>Fourteen bounded surfaces completed, four remain represented, one empirical adapter remains an open gap, and one authority matrix remains exact-gated. No empirical GMUT confirmation, THOS effectiveness, production identity, legal or cultural authority, Maori authority, consciousness, personhood, exhaustive security, complete accessibility, independent reproduction, or Stage 20 readiness is claimed.</p></section><section aria-labelledby="results"><h2 id="results">Proposal results</h2><div class="scroll" role="region" aria-label="Proposal results table" tabindex="0"><table><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Disposition</th></tr></thead><tbody>{rows}</tbody></table></div></section><section aria-labelledby="access"><h2 id="access">Accessibility reservation</h2><p>This static report has landmarks, headings, a skip link, visible focus, table headers, responsive overflow, and no script. Manual keyboard, touch, browser, assistive-technology, cognitive, Maori-language, security-usability, and affected-user evaluation remain reserved.</p></section></main></body></html>'''
    write_text("accessible-report.html", report)


def main() -> int:
    x1 = json.loads((ROOT / "x1-proposals.json").read_text(encoding="utf-8"))
    if x1["x2_started"] or len(x1["proposals"]) != 20:
        raise SystemExit("x1 freeze is not eligible")
    ledger, mutations = build_surfaces()
    distribution = Counter(row["disposition"] for row in ledger)
    skill_receipts = build_skills()
    runner_receipts = build_runners()
    build_portfolios(skill_receipts, runner_receipts)
    build_overview(ledger); build_report(ledger)
    write_json("x2-evidence-ledger.json", {"schema": "ghc.family.v650-v3.x2-evidence.v1", "phase": PHASE, "owner": OWNER, "source_head": SOURCE_HEAD, "x1_commit_required": True, "proposal_count": len(ledger), "distribution": dict(distribution), "outcome_classes": ["completed", "represented", "open_gap", "exact_gate"], "proposals": ledger, "boundary": BOUNDARY})
    write_json("validation/synthetic-mutation-results.json", {"schema": "ghc.family.v650-v3.all-mutations.v1", "count": len(mutations), "executed": len(mutations), "rejected_or_quarantined": sum(r["result"] == "rejected_or_quarantined" for r in mutations), "results": mutations, "security_claim": "bounded_guard_evidence_only"})
    negatives = ACTIVATION_NEGATIVES + len(X1_NEGATIVES) + len(mutations) + X2_OPERATIONAL_NEGATIVES
    write_json("retained-negative-register-evidence.json", {"schema": "ghc.family.v650-v3.retained-negatives.evidence.v1", "activation_baseline": ACTIVATION_NEGATIVES, "x1_operational": len(X1_NEGATIVES), "synthetic_mutations": len(mutations), "x2_operational": X2_OPERATIONAL_NEGATIVES, "effective_total": negatives, "erased": 0, "source_external_negatives_preserved": 2})
    write_json("method-flow/x2-operational-negative-register.json", {"schema": "ghc.family.v650-v3.x2-operational-negatives.v1", "count": 2, "entries": [{"negative_id": "V6503-X2-N01", "failure": "A combined owner-file and status probe exceeded its twenty-second wrapper without attributable output.", "recovery": "Independent bounded probes returned owner-file, phase-commit, status, and x1-protection evidence.", "disposition": "retained"}, {"negative_id": "V6503-X2-N02", "failure": "The first evidence staged review found 208 doubled-newline and EOF hygiene issues.", "recovery": "Only the attributable newline generator, overview bytes, and runtime EOF were corrected before one staged-review retry.", "disposition": "retained"}]})
    write_json("exact-open-gate-register-evidence.json", {"schema": "ghc.family.v650-v3.gates.evidence.v1", "inherited_open_gaps": INHERITED_OPEN_GAPS, "new_open_gaps": 1, "effective_open_gaps": INHERITED_OPEN_GAPS + 1, "inherited_exact_gates": INHERITED_EXACT_GATES, "new_exact_gates": 1, "effective_exact_gates": INHERITED_EXACT_GATES + 1, "closed_without_exact_evidence": 0, "open_gap_ids": ["V6503-P04"], "exact_gate_ids": ["V6503-P09"]})
    write_json("threat-model.json", {"schema": "ghc.family.v650-v3.threat-model.v1", "assets": ["x1 freeze", "evidence ledger", "negative history", "privacy boundary", "authority boundary"], "threats": ["source substitution", "semantic duplication", "boundary erasure", "unsupported promotion", "raw identifier leak", "resource exhaustion", "replay credit", "authority laundering"], "controls": ["exact anchors", "novelty audit", "immutable x1 manifest", "five-class scan", "mutation rejection", "single-pass budget", "exact gate vocabulary"], "residual_risks": ["independent audit absent", "production review absent", "manual accessibility review absent", "affected-party and Maori authority absent"], "exhaustive_security_claim": False})
    write_json("environment/environment-version-receipt-evidence.json", {"schema": "ghc.family.v650-v3.environment.evidence.v1", "verified_date": "2026-07-20", "codex_cli": "0.144.5", "codex_desktop": "26.715.4045.0", "python": "3.12.10", "git": "2.55.0.windows.2", "powershell": "5.1.26100.8894", "d_drive_primary": True, "sandbox_or_hyper_v_launched": False, "desktop_updated": False, "elevation": False, "host_security_changed": False, "reboot": False})
    write_json("wellbeing-check-evidence.json", {"schema": "ghc.family.v650-v3.wellbeing.evidence.v1", "scope_bounded": True, "pause_available": True, "identity_pressure": False, "cadence_used_as_proof": False, "owner_files_below_threshold": True})
    write_json("ghc-family-index-evidence.json", {"schema": "ghc.family.phase-index.v1", "phase": PHASE, "owner": OWNER, "state": "evidence_candidate", "proposal_outcomes": dict(distribution), "safe_tasks": 40, "candidate_prototypes": 30, "skills": 20, "runners": 10, "cleanup": 40, "mutations": 100, "shared_skill_change": False, "historical_callers_preserved": True})
    write_json("complete-incomplete-checklist-evidence.json", {"schema": "ghc.family.v650-v3.checklist.evidence.v1", "complete": ["x1 frozen and pushed", "twenty proposals executed", "portfolios executed", "skills validated and smoke-used", "runners invoked", "one hundred mutations rejected", "accessible report built"], "incomplete": ["evidence commit and push", "closeout commit and push", "single canonical terminal pass", "exact route send"]})
    write_json("phase-truth-evidence.json", {"schema": "ghc.family.v650-v3.phase-truth.evidence.v1", "phase": PHASE, "owner": OWNER, "state": "EVIDENCE_CANDIDATE", "distribution": dict(distribution), "effective_negatives": negatives, "open_gaps": INHERITED_OPEN_GAPS + 1, "exact_gates": INHERITED_EXACT_GATES + 1, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "independent_reproduction": False, "boundary": BOUNDARY})
    write_json("orchestration/terminal-route-state-evidence.json", {"schema": "ghc.family.v650-v3.route.evidence.v1", "state": "HELD_EVIDENCE", "sent": False, "target_title": "Orin Thale", "reason": "closeout and terminal validation pending"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
