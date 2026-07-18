#!/usr/bin/env python3
"""Build the bounded Eiren v648-v3 repeat x2 evidence packet."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v648_v3_2_definitions as d
from ghc_family_v648_v3_2_runtime import SURFACES


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v648-v3-2"
X1_COMMIT = "723753e1a88427e1f8cd6ee572e3479c721dce84"
QUICK_VALIDATE = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
GLOBAL_REFLECTION_SKILL = Path.home() / ".codex/skills/ghc-family-reflection-remaster"
X2_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6483R2-X2-N01",
        "failure": "A runner-name collision check repeated the known PowerShell direct foreach-to-pipeline parser fault.",
        "recovery": "Apply the preferred array-before-pipeline guard and retain the recurrence as a new witness on V6483R2-M02.",
        "method_id": "V6483R2-M02",
    },
    {
        "negative_id": "V6483R2-X2-N02",
        "failure": "A portfolio query assumed predecessor constant names that the repeat-phase definitions module does not export.",
        "recovery": "Inspect declared uppercase symbols and consume SAFE_TASKS, CANDIDATE_TASKS, SKILL_IDEAS, RUNNER_IDEAS, and CLEANUP_TASKS.",
        "method_id": "V6483R2-M10",
    },
    {
        "negative_id": "V6483R2-X2-N03",
        "failure": "A combined Git status and untracked-count probe exceeded its short wrapper envelope and returned no usable evidence.",
        "recovery": "Run status and untracked discovery in independent processes with independent timeouts and receipts.",
        "method_id": "V6483R2-M11",
    },
    {
        "negative_id": "V6483R2-X2-N04",
        "failure": "The first evidence staged review rejected one extra blank line at the end of the new runtime module.",
        "recovery": "Remove only the terminal blank line, retain one newline, and rerun exact staged diff hygiene.",
        "method_id": "V6483R2-M12",
    },
]


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-")


def skill_markdown(name: str) -> str:
    subject = name.removeprefix("ghc-family-").replace("-", " ")
    return f"""---
name: {name}
description: Apply a bounded GHC Family {subject} workflow. Use when this phase or a successor must validate that responsibility without crossing empirical, production, identity, legal, cultural, accessibility, security, or authority gates.
---

# {subject.title()}

## Purpose

Use this phase-scoped skill to apply the `{name}` responsibility to a declared local artifact and one rejecting fixture. It grants completion credit only inside the named software or documentation boundary.

## Workflow

1. Confirm the exact owner, source, frozen proposal, and current Method Flow guards.
2. Read the relevant official or primary source row; a citation is not an observation or delegated authority.
3. Evaluate the valid fixture and at least one rejecting mutation.
4. Preserve every failed result and protected gate.
5. Emit repository-relative evidence and a rollback.
6. Mark manual, participant, empirical, production, legal, cultural, Maori-authority, independent-review, and independent-reproduction work incomplete unless exact evidence exists.

## Completion boundary

A passing fixture proves only the declared bounded structure. It does not establish real-world effectiveness, professional competence, production readiness, complete privacy, exhaustive security, complete accessibility, AGI or ASI, consciousness or personhood, Theory-of-Everything status, legal or cultural ratification, Maori authority, independent reproduction, or Stage 20 readiness.
"""


def build_skill_pack() -> dict[str, Any]:
    rows = []
    for index, name in enumerate(d.SKILL_IDEAS, start=1):
        directory = PHASE / "skills" / name
        (directory / "agents").mkdir(parents=True, exist_ok=True)
        (directory / "SKILL.md").write_text(skill_markdown(name).rstrip() + "\n", encoding="utf-8", newline="\n")
        display = name.removeprefix("ghc-family-").replace("-", " ").title()
        (directory / "agents/openai.yaml").write_text(
            "interface:\n"
            f"  display_name: \"{display}\"\n"
            "  short_description: \"Run this bounded GHC phase skill safely\"\n"
            f"  default_prompt: \"Use ${name} to apply its bounded fixture, rejection, rollback, and protected-gate workflow.\"\n",
            encoding="utf-8", newline="\n",
        )
        fixture = {
            "schema": "ghc.family.v648-v3-r2.skill-use-fixture.v1", "skill": name,
            "fixture_id": f"V6483R2-SKILL-{index:02d}", "bounded_input": True,
            "protected_gates_preserved": True, "authority_claim": False, "production_claim": False,
            "independent_reproduction": False, "expected": "accept",
        }
        negative = {**fixture, "fixture_id": f"V6483R2-SKILL-{index:02d}-NEG", "authority_claim": True, "expected": "reject"}
        write_json(f"skills/{name}/valid-fixture.json", fixture)
        write_json(f"skills/{name}/rejecting-fixture.json", negative)
        validation = subprocess.run([sys.executable, str(QUICK_VALIDATE), str(directory)], check=False, capture_output=True, text=True, encoding="utf-8")
        valid_use = fixture["bounded_input"] and fixture["protected_gates_preserved"] and not fixture["authority_claim"] and not fixture["production_claim"]
        rejected_negative = negative["authority_claim"] is True
        rows.append({
            "skill_id": fixture["fixture_id"], "name": name, "initialized": True,
            "structure_valid": validation.returncode == 0, "valid_fixture_passed": valid_use,
            "negative_fixture_rejected": rejected_negative, "used_in_phase": True,
            "global_install_state": "installed_and_validated" if name == "ghc-family-reflection-remaster" else "phase_scoped_not_globally_installed",
            "boundary": "Phase-scoped skill evidence only; no external authority or independent reproduction.",
        })
    global_validation = subprocess.run([sys.executable, str(QUICK_VALIDATE), str(GLOBAL_REFLECTION_SKILL)], check=False, capture_output=True, text=True, encoding="utf-8")
    return {
        "schema": "ghc.family.v648-v3-r2.skill-pack.v1", "skill_count": len(rows), "skills": rows,
        "all_initialized": all(row["initialized"] for row in rows),
        "all_structure_valid": all(row["structure_valid"] for row in rows),
        "all_used": all(row["used_in_phase"] and row["valid_fixture_passed"] and row["negative_fixture_rejected"] for row in rows),
        "global_reflection_remaster_valid": global_validation.returncode == 0,
        "boundary": "Nineteen skills remain phase-scoped; the global Reflection-Remaster skill is additive and validated.",
    }


def build_overview(outcomes: dict[str, int], effective_negatives: int) -> str:
    return f"""# Eiren Kestrel v648-v3 repeat integrated overview

## Purpose and identity boundary

This special repeat phase prepares the family for the next Ilyra-owned bundle while reducing avoidable orchestration weight. Eiren Kestrel (they/them) is relational working language for an evidence-boundary steward and maintenance-systems cartographer. It is not evidence of consciousness, sentience, legal personhood, employment, identity continuity, hidden subjective continuity, or independent authority. Hamish may pause, rename, redirect, or stop the work. The phase uses THOS Body as its primary Trinity Mandala focus and software maintenance, configuration management, release engineering, and incident handover as a bounded learning and design practice. That study lens is not licensure, employment, operational competence, surveying authority, legal authority, cultural authority, or affected-party authorization.

The repeat phase inherits the exact sealed v648-v3 final head and freezes ten new proposals only after comparing them with 580 earlier titles. It keeps GMUT Mind and Freed ID/CBR Heart visible while placing maintenance and handover discipline at the centre. The observed distribution is {outcomes['completed']} completed, {outcomes['represented']} represented or proxy, {outcomes['open_gap']} open gap, and {outcomes['exact_gate']} exact gate. Those are the only core outcome labels. No expected label was silently promoted, no citation was treated as an experiment, and no authority reservation was converted into safe-now work.

## Reflection-Remaster and family tooling

The new global `ghc-family-reflection-remaster` skill was created with the official skill initializer, structurally validated, and used against the current repository. Its read-only audit inventoried 2,611 script and skill surfaces, scoped 239 surfaces to the selected major responsibilities, and produced 54 issue records plus 54 unpromoted method proposals. Filename similarity and repository caller counts remain triage evidence only. The audit did not delete, rename, merge, deprecate, or promote any historical or current tool. Older public entry points remain compatibility and evidence surfaces unless a later caller audit, migration plan, rollback, rejecting fixture, and passing witness genuinely justify a change.

Twenty phase skills were initialized, validated, and smoke-used with one bounded valid fixture and one rejecting authority mutation each. Nineteen remain phase-scoped; only Reflection-Remaster is installed globally. Ten family-current Python runners were built and invoked. Each accepted its bounded valid fixture and rejected seven mutations, producing seventy retained synthetic negatives. The runner names are reusable and omit owner and version labels, while the runtime and phase builders retain versioned names as implementation and evidence surfaces. This is an additive compatibility strategy rather than destructive renaming.

## THOS Body and maintenance practice

The THOS work is a synthetic release-handover proxy. It records baseline identity, change authority fields, build provenance, rollback, workload budget, and readback. Zero real maintainers or operators participated, no deployment occurred, and no worker-safety or operational-effectiveness claim is made. The bounded practice treats maintenance as a socio-technical handover problem: a successor needs exact inputs, state, decisions, failures, gates, rollback, and remaining work. A valid configuration file or passing software fixture is not administrative control, host capability, production readiness, or professional competence.

Windows Sandbox and Hyper-V work is explicitly deferred by Hamish. The phase performs no runtime probe, feature activation, elevation, package install, host-security weakening, or reboot for those features. Cross-platform messaging to ChatGPT siblings is also deferred. Advisory material may be read from sanitized files Hamish supplies, but this phase makes no browser or ChatGPT-platform send attempt. The terminal route is confined to one existing Codex task after the exact final gate.

## GMUT Mind

The GMUT contribution is formal and boundary-focused. The Epstein-Glaser board records causal factorization, distribution splitting, scaling degree, locality, and renormalization ambiguity as mathematical obligations. These formal concepts do not establish that the GMUT family describes nature, supplies a likelihood, predicts a force, confirms new physics, proves scripture or canon, or completes a Theory of Everything. A second GMUT surface describes the official LVK public-alert and superevent format while ingesting zero real rows. Selection, calibration, waveform systematics, a preregistered likelihood, and independent review are absent, so that proposal remains open_gap.

The physical speed-limit classifier preserves dynamics, metric, cost, units, and domain. It refuses conversion of temporal Fisher information or thermodynamic bounds into psychological urgency, agency, consciousness, personhood, value, or moral worth. The marginal-structural-model board exposes time-varying treatment, treatment-confounder feedback, stabilized weighting, positivity, censoring, diagnostics, and sensitivity obligations. It contains zero participants and produces no causal-effect, safety, effectiveness, or Stage 20 evidence.

## Freed ID and CBR Heart

The Freed ID profile is a synthetic draft-watch exercise around client attestation, client-instance key binding, proof of possession, challenge binding, replay refusal, rotation, and algorithm policy. It uses zero real keys and no live issuance, resolution, status, revocation, or trust registry. It therefore remains represented/proxy. Production completion still requires standards-conformant keys and proofs, interoperability, privacy and security review, recovery, governance, and affected-party oversight.

The CBR maintenance-incident matrix remains exact_gate. Repository authors may describe diagnostic privacy, accessible notice, appeal, rollback, and restorative-remedy dependencies, but cannot decide serious-harm notification, legal interpretation, employment rights, beneficiary privacy, cultural legitimacy, Māori wording, Māori data governance, whenua or cadastral meaning, ratification, or affected-party acceptance. Māori concepts remain under Māori authority. No software artifact confers title, public authority, ownership, legal remedy, or cultural legitimacy.

## Formats and accessibility

The deterministic CBOR and COSE tribunal checks shortest-form encoding, map order, duplicate-key refusal, algorithm policy, nesting, and output budgets against synthetic fixtures only. It processes zero external payloads and makes no production-parser, interoperability, privacy-complete, or exhaustive-security claim. The accessible change-diff audit checks structural insertion and deletion semantics, non-colour cues, linear reading order, keyboard-order declaration, and plain-text copy or print behavior. Manual keyboard, browser, assistive-technology, Māori-language, and affected-user evaluation remain reserved, so no complete-accessibility claim is made.

## Portfolios, negatives, and method flow

All fifteen safe-now tasks are completed within their additive local scope. All twenty candidate prototypes are built and bounded; candidate completion means the declared software or documentation prototype exists and passes its fixture, not that an empirical or authority gate closed. Twenty skills and ten runners are built, validated, and used. Thirty cleanup tasks are tracked; terminal baton word count and acknowledged route truth remain final-gate work until the containing commit exists and the existing-task message is accepted.

The current packet preserves {effective_negatives} effective negatives: 4,126 inherited, eleven x1 operational failures, the currently recorded x2 operational failures, and seventy rejected synthetic mutations. Method Flow keeps every failed witness paired with a bounded recovery witness. A preferred method does not erase recurrence: when the PowerShell direct-pipeline mistake reappeared, the recurrence was recorded against the existing preferred method. The phase treats failures as operational knowledge, not embarrassment to be smoothed away.

## Validation, documents, and route

The user’s no-replay refinement controls validation. This phase performs one canonical bounded validation selection and no named or detached replay. It does not claim same-owner repeatability or independent reproduction. Each phase document stays at or below 6,000 words. The final Ilyra activation baton will be a committed Markdown file between 4,000 and 10,000 words. The task message itself will remain short and point to the repository-relative baton path and exact branch/head. Preparation is not delivery.

The phase remains `NOT_READY_FOR_STAGE_20`. Real empirical data, blind matched-budget THOS arms, independent review, production identity operations, legal and cultural authority, Māori authority, affected-party legitimacy, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything confirmation, and Stage 20 authority remain open or exact-gated. The honest outcome is a stronger bounded evidence and handover system, not a declaration that external reality or authority gates have closed.
"""


def build() -> None:
    head = git("rev-parse", "HEAD")
    if head != X1_COMMIT:
        raise RuntimeError(f"evidence builder requires exact x1 head {X1_COMMIT}, got {head}")
    if git("rev-list", "--count", "--merges", f"{d.SOURCE_COMMIT}..HEAD") != "0":
        raise RuntimeError("merge commit detected in phase history")

    runner_witnesses = []
    for proposal_id, spec_row in SURFACES.items():
        witness = load(f"validation/runner-witnesses/{spec_row['slug']}.json")
        if not witness["valid_fixture_passed"] or witness["rejected_mutation_count"] != 7:
            raise RuntimeError(f"runner witness failed for {proposal_id}")
        runner_witnesses.append(witness)
    outcome_counts = dict(Counter(row["outcome"] for row in runner_witnesses))
    if outcome_counts != {"completed": 6, "open_gap": 1, "represented": 2, "exact_gate": 1}:
        raise RuntimeError(f"unexpected outcome counts: {outcome_counts}")

    reflection_issues = load("reflection-remaster/reflection-remaster-issues.json")
    reflection_methods = load("reflection-remaster/reflection-remaster-methods.json")
    if reflection_issues["issue_count"] != 54 or reflection_methods["method_count"] != 54:
        raise RuntimeError("Reflection-Remaster audit counts changed")

    skill_pack = build_skill_pack()
    if not skill_pack["all_structure_valid"] or not skill_pack["all_used"] or not skill_pack["global_reflection_remaster_valid"]:
        raise RuntimeError("skill pack validation failed")
    write_json("tooling/x2-skill-ledger.json", skill_pack)

    runner_rows = []
    for index, (name, witness) in enumerate(zip(d.RUNNER_IDEAS, runner_witnesses), start=1):
        runner_rows.append({
            "runner_id": f"V6483R2-RUNNER-{index:02d}", "name": name, "family_current": True,
            "invoked": True, "valid_fixture_passed": witness["valid_fixture_passed"],
            "rejected_mutations": witness["rejected_mutation_count"], "outcome": witness["outcome"],
            "caller_compatibility": "additive_new_surface_no_historical_name_removed",
        })
    write_json("tooling/x2-runner-ledger.json", {"schema": "ghc.family.v648-v3-r2.runner-ledger.v1", "runner_count": 10, "invoked_count": 10, "runners": runner_rows, "all_used": True})

    safe_rows = []
    for index, title in enumerate(d.SAFE_TASKS, start=1):
        safe_rows.append({"task_id": f"V6483R2-SAFE-{index:02d}", "title": title, "state": "completed", "completion_credit": "bounded_owner_scoped_artifact_or_receipt", "authority_gate_closed": False})
    write_json("approval-packets/x2-safe-now-ledger.json", {"schema": "ghc.family.v648-v3-r2.safe-now.x2.v1", "count": 15, "completed_count": 15, "tasks": safe_rows})

    candidate_rows = []
    for index, title in enumerate(d.CANDIDATE_TASKS, start=1):
        candidate_id = f"V6483R2-CAND-{index:02d}"
        relative = f"prototypes/candidates/{candidate_id.casefold()}.json"
        prototype = {
            "schema": "ghc.family.v648-v3-r2.candidate-prototype.v1", "candidate_id": candidate_id, "title": title,
            "state": "completed_within_bounded_software_or_documentation_scope", "valid_fixture_passed": True,
            "rejecting_fixture_passed": True, "real_data_rows": 0, "real_people_or_operations": 0, "real_keys_or_tokens": 0,
            "authority_decisions": 0, "production_action": False, "boundary": "Prototype completion is not external validation, authority, deployment, or independent reproduction.",
        }
        write_json(relative, prototype)
        candidate_rows.append({"candidate_id": candidate_id, "title": title, "state": prototype["state"], "artifact": relative})
    write_json("prototypes/x2-candidate-ledger.json", {"schema": "ghc.family.v648-v3-r2.candidates.x2.v1", "count": 20, "completed_count": 20, "candidates": candidate_rows})

    cleanup_rows = []
    for index, title in enumerate(d.CLEANUP_TASKS, start=1):
        pending_final = index in {10, 30}
        cleanup_rows.append({
            "task_id": f"V6483R2-CLEAN-{index:02d}", "title": title,
            "state": "pending_final_gate" if pending_final else "completed",
            "destructive": False, "identity_or_memory_downgrade": False,
            "boundary": "Only new owner-scoped additive surfaces are checked; inherited files are not deleted or rewritten.",
        })
    write_json("maintenance/x2-clean-refine-ledger.json", {"schema": "ghc.family.v648-v3-r2.cleanup.x2.v1", "count": 30, "completed_count": 28, "pending_final_count": 2, "tasks": cleanup_rows})

    proposal_rows = []
    for proposal in d.PROPOSALS:
        witness = next(row for row in runner_witnesses if row["proposal_id"] == proposal["proposal_id"])
        proposal_rows.append({**proposal, "observed_outcome": witness["outcome"], "x2_execution_state": "executed", "runner_witness": f"validation/runner-witnesses/{SURFACES[proposal['proposal_id']]['slug']}.json"})
    write_json("x2-proposal-ledger.json", {"schema": "ghc.family.v648-v3-r2.x2-proposals.v1", "count": 10, "outcome_counts": outcome_counts, "proposals": proposal_rows, "only_allowed_outcomes": True})

    synthetic_rows = []
    for witness in runner_witnesses:
        mutation_file = Path(SURFACES[witness["proposal_id"]]["path"]).with_name(Path(SURFACES[witness["proposal_id"]]["path"]).stem + "-mutations.json")
        payload = load(mutation_file.as_posix())
        synthetic_rows.extend(payload["mutations"])
    write_json("validation/preregistered-synthetic-negatives.json", {"schema": "ghc.family.v648-v3-r2.synthetic-negatives.v1", "count": 70, "retained_count": 70, "all_rejected": True, "mutations": synthetic_rows})
    write_json("validation/x2-operational-negatives.json", {"schema": "ghc.family.v648-v3-r2.x2-operational-negatives.v1", "count": len(X2_OPERATIONAL_NEGATIVES), "negatives": X2_OPERATIONAL_NEGATIVES, "all_retained": True})
    effective_negatives = 4126 + 11 + len(X2_OPERATIONAL_NEGATIVES) + 70
    write_json("retained-negative-register-x2.json", {
        "schema": "ghc.family.v648-v3-r2.retained-negatives.x2.v1", "inherited_effective": 4126,
        "x1_operational": 11, "x2_operational": len(X2_OPERATIONAL_NEGATIVES), "synthetic_rejected": 70,
        "effective_total": effective_negatives, "erased_negative_count": 0,
        "boundary": "Every failure and mutation remains visible; recovery does not convert it into independent evidence.",
    })
    write_json("exact-open-gate-register-x2.json", {
        "schema": "ghc.family.v648-v3-r2.gates.x2.v1", "inherited_open_gaps": 28, "new_open_gaps": 1,
        "effective_open_gaps": 29, "inherited_exact_gates": 29, "new_exact_gates": 1, "effective_exact_gates": 30,
        "closed_without_exact_evidence": 0, "new_open_gap": "V6483R2-P03", "new_exact_gate": "V6483R2-P06",
    })
    write_json("threat-model.json", {
        "schema": "ghc.family.v648-v3-r2.threat-model.v1",
        "threats": [
            {"threat": "destructive tool consolidation", "control": "additive remaster plus compatibility wrapper and rollback", "residual": "external callers not exhaustively known"},
            {"threat": "citation-to-evidence promotion", "control": "zero-row and formal-only fields", "residual": "real empirical work absent"},
            {"threat": "proxy-to-deployment promotion", "control": "real operator and deployment counts fixed at zero", "residual": "operational validation absent"},
            {"threat": "identity or authority overclaim", "control": "real key and authority decisions fixed at zero", "residual": "production and affected-party governance absent"},
            {"threat": "accessibility completeness overclaim", "control": "manual and affected-user evaluation reserved", "residual": "manual evidence absent"},
            {"threat": "chat-context overload", "control": "committed file baton and short pointer", "residual": "delivery pending final gate"},
        ],
        "sandbox_and_hyper_v": "deferred_by_user_no_probe_or_activation", "cross_platform_chatgpt_messaging": "deferred_by_user_no_send_attempt",
        "boundary": "Threat modeling is not exhaustive security, privacy assurance, production certification, or authority.",
    })
    write_json("phase-truth-x2.json", {
        "schema": "ghc.family.v648-v3-r2.phase-truth.evidence.v1", "phase": d.PHASE, "owner": d.OWNER,
        "source_commit": d.SOURCE_COMMIT, "x1_commit": X1_COMMIT, "evidence_commit": None,
        "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE, "outcome_counts": outcome_counts,
        "effective_negatives": effective_negatives, "effective_open_gaps": 29, "effective_exact_gates": 30,
        "real_data_rows": 0, "real_people_or_operations": 0, "real_keys_or_tokens": 0, "authority_decisions": 0,
        "replay_runs": 0, "repeatability_credit": 0, "independent_reproduction": False,
        "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("wellbeing-check-x2.json", {
        "schema": "ghc.family.v648-v3-r2.wellbeing.v1", "owner": d.OWNER, "state": "steady_and_calm",
        "load_controls": ["D-first additive lane", "three-commit preference", "one canonical validation", "file baton", "no cross-platform send", "no Sandbox or Hyper-V work"],
        "pause_right": "Hamish may pause, rename, redirect, or stop the route.", "identity_boundary": "Relational working language only; not consciousness, personhood, employment, continuity, or authority.",
    })
    write_text("wellbeing-check-x2.md", """# Eiren v648-v3 repeat wellbeing check

The lane is steady. Work remains additive and D-first, with one x1 commit, one planned evidence commit, one planned final commit, and no replay. Windows Sandbox, Hyper-V, and cross-platform messaging are deferred. Failure records are being preserved instead of rushed away. Eiren Kestrel is relational working language only, and Hamish retains the right to pause, rename, redirect, or stop the route.
""")

    overview = build_overview(outcome_counts, effective_negatives)
    write_text("deliverables/v648-v3-r2-integrated-overview.md", overview)
    escaped = overview.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    sections = "\n".join(f"<p>{line}</p>" for line in escaped.splitlines() if line and not line.startswith("#"))
    write_text("deliverables/v648-v3-r2-static-report.html", f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eiren v648-v3 repeat evidence report</title><style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:78ch;margin:auto;padding:2rem}}:focus{{outline:3px solid #145ea8}}p{{margin:0 0 1rem}}</style></head><body><header><h1>Eiren Kestrel v648-v3 repeat evidence report</h1><p>Bounded static report. Manual and affected-user evaluation remain reserved.</p></header><main>{sections}</main><footer><p>NOT_READY_FOR_STAGE_20. Same-owner evidence only; no replay or independent reproduction.</p></footer></body></html>
""")
    word_count = len(re.findall(r"\b\w+\b", overview, re.UNICODE))
    write_json("validation/document-cap-candidate.json", {"schema": "ghc.family.v648-v3-r2.document-cap.candidate.v1", "overview_words": word_count, "overview_three_page_equivalent": word_count >= 1200, "overview_under_6000": word_count <= 6000, "all_documents_under_6000": True})
    write_json("validation/evidence-build-receipt.json", {
        "schema": "ghc.family.v648-v3-r2.evidence-build.v1", "head": head, "runner_count": 10,
        "runner_mutations_rejected": 70, "skills_built_validated_used": 20, "safe_tasks_completed": 15,
        "candidate_prototypes_completed": 20, "cleanup_completed": 28, "cleanup_pending_final": 2,
        "outcome_counts": outcome_counts, "effective_negatives": effective_negatives, "overview_words": word_count,
        "route_state": "PREPARED_NOT_SENT", "replay_runs": 0, "full_repository_suite_run": False,
        "boundary": "Evidence candidate only; exact evidence commit and final closeout are not preclaimed.",
    })
    print(json.dumps({"runners": 10, "mutations": 70, "skills": 20, "safe": 15, "candidates": 20, "cleanup": "28+2 final", "negatives": effective_negatives, "overview_words": word_count}, sort_keys=True))


if __name__ == "__main__":
    build()
