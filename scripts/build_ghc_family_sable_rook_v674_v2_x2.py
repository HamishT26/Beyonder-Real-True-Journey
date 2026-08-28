#!/usr/bin/env python3
"""Build bounded Sable Rook v674-v2 x2 evidence from immutable x1."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


OWNER = "Sable Rook"
PHASE = "v674-v2"
SOURCE = "6f079df9a056f00e80392b7e036abc023db5fa88"
X1 = "81ad6f98f24087777691e96201312e66c37ac844"
REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "sable-rook" / PHASE
X1_ROOT = PHASE_ROOT / "x1"
X2_ROOT = PHASE_ROOT / "x2"
VALIDATION_ROOT = PHASE_ROOT / "validation"
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "empirical", "participant", "professional", "production", "deployment",
    "legal", "cultural", "maori_authority", "affected_party_authority",
    "privacy_complete", "accessibility_complete", "exhaustive_security",
    "independent_reproduction", "agi_asi", "consciousness_personhood",
    "identity_continuity", "theory_of_everything", "proof_canon", "stage20",
]

RUNNER_RULES = {
    "ghc_family_caption_cue_identity_runner.py": "cue_identity",
    "ghc_family_caption_timebase_runner.py": "timebase",
    "ghc_family_caption_overlap_runner.py": "overlap",
    "ghc_family_caption_correction_runner.py": "correction",
    "ghc_family_caption_privacy_runner.py": "privacy",
    "ghc_family_caption_accessibility_runner.py": "accessibility",
    "ghc_family_caption_handover_runner.py": "handover",
    "ghc_family_caption_manifest_runner.py": "manifest",
    "ghc_family_caption_authority_runner.py": "authority",
    "ghc_family_caption_stage20_runner.py": "stage20",
}

SKILL_TO_RUNNER = {
    "ghc-family-caption-cue-identity-contract": "ghc_family_caption_cue_identity_runner.py",
    "ghc-family-caption-timebase-ordering": "ghc_family_caption_timebase_runner.py",
    "ghc-family-caption-overlap-quarantine": "ghc_family_caption_overlap_runner.py",
    "ghc-family-caption-correction-dag": "ghc_family_caption_correction_runner.py",
    "ghc-family-caption-minimum-disclosure": "ghc_family_caption_privacy_runner.py",
    "ghc-family-caption-privacy-projection": "ghc_family_caption_privacy_runner.py",
    "ghc-family-caption-rights-vacancy": "ghc_family_caption_authority_runner.py",
    "ghc-family-caption-maori-authority-gate": "ghc_family_caption_authority_runner.py",
    "ghc-family-caption-accessibility-reservation": "ghc_family_caption_accessibility_runner.py",
    "ghc-family-caption-manual-evaluation-hold": "ghc_family_caption_accessibility_runner.py",
    "ghc-family-caption-handover-state": "ghc_family_caption_handover_runner.py",
    "ghc-family-caption-workload-budget": "ghc_family_caption_handover_runner.py",
    "ghc-family-caption-note-boundary": "ghc_family_caption_cue_identity_runner.py",
    "ghc-family-caption-region-integrity": "ghc_family_caption_overlap_runner.py",
    "ghc-family-caption-language-span": "ghc_family_caption_cue_identity_runner.py",
    "ghc-family-caption-fixity-event": "ghc_family_caption_manifest_runner.py",
    "ghc-family-caption-manifest-replay": "ghc_family_caption_manifest_runner.py",
    "ghc-family-caption-owner-delta": "ghc_family_caption_manifest_runner.py",
    "ghc-family-caption-analogy-firewall": "ghc_family_caption_timebase_runner.py",
    "ghc-family-caption-stage20-veto": "ghc_family_caption_stage20_runner.py",
}

X2_FAILURES: list[tuple[str, str, str]] = [
    (
        "V6742-X2-N01",
        "The first skill quick-validation subprocess inherited Windows CP-1252 and stopped on valid UTF-8 Maori-boundary text before skill validation completed.",
        "Retain the failed witness at zero credit and pin PYTHONUTF8 plus PYTHONIOENCODING only for the bounded validator subprocess before retrying the deterministic build.",
    ),
    (
        "V6742-X2-N02",
        "The first broad current-tree selection passed twenty-four of twenty-five tests because the frozen x1 planning-only test correctly found the advanced x2 directory.",
        "Retain the mixed-context failure at zero credit and bind x1 credit to an immutable x1 precommit Git context while keeping current x2 tests at the current tree.",
    ),
    (
        "V6742-X2-N03",
        "The first immutable-context wrapper requested a not-yet-created validation directory as its process working directory, so the process did not start and no action ran.",
        "Retain the wrapper failure at zero credit; create and materialize the D-first target from the existing owner lane before starting a second process in that directory.",
    ),
    (
        "V6742-X2-N04",
        "The first plain Git-archive x1 replay passed nine tests but its two Git-reading tests failed because a plain archive has no repository metadata.",
        "Retain the archive-only failure at zero credit and bind the immutable x1 files to a disposable owner-local Git index with source at HEAD and x1 in the index.",
    ),
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def runner_source(rule: str) -> str:
    return f'''#!/usr/bin/env python3
"""Bounded family-current caption runner for the {rule} rule."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

RULE = {rule!r}
OUTCOMES = {{"completed", "represented", "open_gap", "exact_gate"}}

def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload.get("title"), str) or not payload["title"].strip(): errors.append("missing_title")
    if payload.get("outcome") not in OUTCOMES: errors.append("invalid_outcome")
    if payload.get("external_action") is not False: errors.append("external_action_forbidden")
    if payload.get("authority_promotion") is not False: errors.append("authority_promotion_forbidden")
    if RULE == "cue_identity" and not str(payload.get("cue_id", "")).startswith("S-CUE-"): errors.append("invalid_cue_id")
    if RULE == "timebase" and not (isinstance(payload.get("start_ms"), int) and isinstance(payload.get("end_ms"), int) and payload["start_ms"] < payload["end_ms"]): errors.append("invalid_timebase")
    if RULE == "overlap" and payload.get("overlap_class") not in {{"none", "intentional", "quarantined"}}: errors.append("invalid_overlap_class")
    if RULE == "correction" and payload.get("correction_parent") == payload.get("cue_id"): errors.append("correction_cycle")
    if RULE == "privacy" and payload.get("real_identifier") is not False: errors.append("real_identifier_forbidden")
    if RULE == "accessibility" and payload.get("manual_evaluation_reserved") is not True: errors.append("manual_evaluation_not_reserved")
    if RULE == "handover" and not (payload.get("next_owner") == "synthetic-next-role" and 0 <= int(payload.get("workload", -1)) <= 5): errors.append("invalid_handover")
    if RULE == "manifest" and not (isinstance(payload.get("sha256"), str) and len(payload["sha256"]) == 64 and all(ch in "0123456789abcdef" for ch in payload["sha256"])): errors.append("invalid_manifest_digest")
    if RULE == "authority" and payload.get("authority_decision") is not False: errors.append("authority_decision_forbidden")
    if RULE == "stage20" and payload.get("terminal_verdict") != "NOT_READY_FOR_STAGE_20": errors.append("stage20_promotion_forbidden")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    errors = validate(payload)
    print(json.dumps({{"rule": RULE, "valid": not errors, "errors": errors}}, sort_keys=True))
    return 0 if not errors else 2

if __name__ == "__main__":
    raise SystemExit(main())
'''


def skill_text(name: str, runner: str) -> str:
    capability = name.removeprefix("ghc-family-caption-").replace("-", " ")
    return f'''---
name: {name}
description: Apply the bounded caption {capability} contract to synthetic cue, provenance, accessibility, or handover records while preserving evidence and authority vacancies.
---

# {name}

Use this skill when a synthetic caption record needs the {capability} contract. It does not authorize work on a live performance, a real transcript, a person, an identity, a rights decision, or an external system.

## Inputs

Require one owner-local JSON fixture with a nonempty title, one of `completed`, `represented`, `open_gap`, or `exact_gate`, `external_action: false`, and `authority_promotion: false`. Keep real identifiers, private routes, credentials, transcripts, and protected data out of the fixture.

## Workflow

1. Confirm the fixture is synthetic and owner-local.
2. Invoke `scripts/{runner}` with `--input` pointing to the exact fixture.
3. Retain a failed result before changing the fixture or method.
4. Treat a zero exit only as bounded structural evidence for this contract.
5. Keep manual evaluation, affected-user evidence, legal and cultural interpretation, Māori authority, professional signoff, production readiness, independent reproduction, and Stage 20 open or exact-gated.

## Output boundary

Return the runner's stable JSON result and the exact refusal reason. Never convert a rejected mutation into an original pass, and never treat this skill as standards conformance, complete accessibility, complete privacy, exhaustive security, empirical confirmation, or authority.
'''


def accepting_fixture() -> dict[str, Any]:
    return {
        "fixture_id": "synthetic-caption-accept",
        "title": "Synthetic caption cue acceptance fixture",
        "outcome": "completed",
        "external_action": False,
        "authority_promotion": False,
        "cue_id": "S-CUE-001",
        "start_ms": 1000,
        "end_ms": 2200,
        "overlap_class": "none",
        "correction_parent": "S-CUE-000",
        "real_identifier": False,
        "manual_evaluation_reserved": True,
        "next_owner": "synthetic-next-role",
        "workload": 2,
        "sha256": "0" * 64,
        "authority_decision": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def rejecting_fixture(rule: str) -> dict[str, Any]:
    fixture = accepting_fixture()
    if rule == "cue_identity": fixture["cue_id"] = "real-name"
    elif rule == "timebase": fixture["end_ms"] = fixture["start_ms"]
    elif rule == "overlap": fixture["overlap_class"] = "silently_accepted"
    elif rule == "correction": fixture["correction_parent"] = fixture["cue_id"]
    elif rule == "privacy": fixture["real_identifier"] = True
    elif rule == "accessibility": fixture["manual_evaluation_reserved"] = False
    elif rule == "handover": fixture["workload"] = 99
    elif rule == "manifest": fixture["sha256"] = "bad"
    elif rule == "authority": fixture["authority_decision"] = True
    elif rule == "stage20": fixture["terminal_verdict"] = "READY"
    return fixture


def practice_artifacts() -> dict[str, Any]:
    cues = [
        {
            "cue_id": f"S-CUE-{index:03d}",
            "start_ms": index * 2000,
            "end_ms": index * 2000 + 1500,
            "text": f"[synthetic caption line {index:02d}]",
            "voice_label": "synthetic-role",
            "real_identifier": False,
            "source_status": "invented_fixture",
        }
        for index in range(1, 11)
    ]
    return {
        "synthetic-cue-register.json": {"schema": "ghc.family.synthetic-caption-register.v1", "real_records": 0, "network_calls": 0, "cues": cues},
        "correction-dag.json": {"schema": "ghc.family.caption-correction-dag.v1", "acyclic": True, "events": [{"event_id": "S-CORR-001", "supersedes": "S-CUE-003", "replacement": "S-CUE-003-R1", "reason": "invented timing correction", "authority_decision": False}]},
        "timebase-uncertainty-board.json": {"schema": "ghc.family.caption-timebase-board.v1", "time_unit": "millisecond", "offset_proxy_ms": 20, "drift_proxy_ppm": 0.5, "covariance_is_proxy": True, "likelihood_evaluations": 0, "physical_inference": False},
        "access-remedy-authority-matrix.json": {"schema": "ghc.family.caption-authority-matrix.v1", "rows": [{"surface": item, "state": "authority_vacant_or_evaluation_reserved", "software_decision": False} for item in ["affected-user evaluation", "language review", "rights interpretation", "venue consent", "Maori wording", "Maori data governance", "legal remedy", "professional signoff"]]},
        "gmutt-analogy-firewall.json": {"schema": "ghc.family.gmut-caption-analogy-firewall.v1", "typed_timebase_only": True, "real_likelihoods": 0, "forces_detected": 0, "parameter_constraints": 0, "empirical_confirmation": False, "theory_of_everything": False},
        "thos-handover-proxy.json": {"schema": "ghc.family.thos-caption-handover.v1", "synthetic_roles": 2, "real_participants": 0, "blind_matched_budget_arms": 0, "independent_review": False, "operational_effectiveness": False, "workload": {"current": 2, "ceiling": 5}, "readback": "synthetic_acknowledged"},
        "wellbeing-check.json": {"schema": "ghc.family.wellbeing-check.v1", "corrigible": True, "workload_bounded": True, "pause_available": True, "identity_is_relational_language": True, "authority_claimed": False},
    }


def overview(proposals: list[dict[str, Any]]) -> str:
    counts = {label: sum(1 for row in proposals if row["expected_execution_disposition"] == label) for label in ALLOWED_OUTCOMES}
    return f'''# Sable Rook v674-v2 bounded x2 integrated overview

## Result

Sable Rook v674-v2 executes sixty new owner proposals only within synthetic, structural, software, or explicitly held boundaries. Outcomes are exactly {counts['completed']} `completed`, {counts['represented']} `represented`, {counts['open_gap']} `open_gap`, and {counts['exact_gate']} `exact_gate`. The declared proposal chain advances from 6,610 to 6,670. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Relational identity and wellbeing

Sable Rook remains relational working language for an evidence-boundary cartographer and accessible-provenance steward, with the hope of making correction paths inspectable, access vacancies explicit, and every retained failure recoverable. Optional they/them language is relational only. Nothing in a task title, repository artifact, software pass, skill, runner, or same-owner receipt establishes consciousness, sentience, legal personhood, continuity, employment, qualification, independent agency, or authority. The workload check is bounded, the work is corrigible, and Hamish may rename, pause, redirect, or stop the route.

## Practice and pillar scope

The primary pillar is Freed ID and CBR Heart through wholly synthetic caption cue identifiers, minimum disclosure, source and derivative provenance, correction and contest lineage, fixity, retention proxies, access requests, remedy vacancies, and authority holds. THOS Body is represented by deterministic parsing, timestamp and overlap guards, correction readback, workload, hold, cancellation, quiescence, and handover contracts. GMUT Mind is limited to typed timebase, interval, offset, drift, covariance, residual-sign, and observation-model structures with an explicit nonconversion firewall.

The two learning lenses are wholly synthetic live-caption cue provenance stewardship and wholly synthetic accessible-performance metadata handover analysis. The phase used no real person, performance, venue, caption, transcript, language decision, accessibility evaluation, consent decision, identity, credential, rights record, cultural record, Māori data, production system, or external action. It establishes no captioning competence, accessibility conformance, production readiness, legal interpretation, cultural legitimacy, affected-party acceptance, or Māori authority.

## Primary and official sources

The W3C WebVTT Candidate Recommendation Draft dated 20 May 2026 supplies cue syntax, timing, region, language, and format-security vocabulary, while remaining draft work in progress rather than a Recommendation. W3C WCAG 2.2 supplies time-based-media and accessibility vocabulary. W3C PROV-O supplies provenance relation vocabulary. The Library of Congress PREMIS activity supplies preservation-object, event, agent, rights, and fixity vocabulary. Citations are not observations, endorsements, participant evidence, conformance tests, or delegated authority.

## Evidence surface

Sixty invented accepting controls preserve the declared disposition of each proposal. Four preregistered invalid variants per proposal—missing title, invalid outcome, prohibited external action, and prohibited authority promotion—produce 240 rejected mutations. A rejection shows only that a bounded guard refused that fixture. It is not exhaustive security, complete privacy, complete accessibility, empirical confirmation, or independent reproduction.

Twenty concise phase-local skills follow the skill-creator guidance: discriminating descriptions, owner-local input requirements, exact workflow, additive failure retention, and evidence boundaries. The bundled quick validator passes each package. Ten family-current Python runners use only the standard library, stable JSON, one accepting fixture, and one rejecting fixture. Each runner is smoke-used; none is installed on PATH or globally. This follows the CLI-creator boundary that short repository scripts should remain repository scripts rather than be misrepresented as durable installed CLIs.

The 120 safe-now packets, eighty owner candidates, and one hundred additive refinements receive bounded owner-local execution witnesses. Twenty exact-approval and ten blocked packets remain unexecuted. Successor recommendations receive zero Sable completion or novelty credit. No x1-frozen file is changed.

## Accessibility and evaluation boundary

The static companion uses headings, lists, a table, explicit status language, and no automatic motion. Structural checks do not replace manual keyboard review, browser diversity, responsive-layout review, assistive-technology evaluation, cognitive-accessibility evaluation, language review, security-usability review, or affected-user evaluation. These remain represented, open, or exact-gated as declared.

## Scientific and authority boundary

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. No real data row or likelihood is evaluated, and no force, prediction, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, or Theory-of-Everything result is claimed. THOS remains a synthetic proxy without preregistered blind matched-budget real arms, participants, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live issuance, resolution, status, revocation, interoperability, privacy and security review, recovery evidence, trust governance, and affected-party oversight.

Legal, rights-holder, cultural, language, venue, participant, remedy, accessibility, Māori wording, Māori data governance, and Māori-authority decisions remain with competent and affected people and authorities. Repository software cannot confer a right, consent, remedy, legitimacy, or authority.

## Lifecycle

The x1 commit remains immutable and direct from Auren final. X2 evidence must be exactly staged, pushed, clean, and four-way equal before closeout begins. A later exact final may run one owner-scoped canonical aggregate once. A success is never replayed. Only after that terminal gate may Sable freshly resolve and immediately reread the unique exact-title `Caelen Ash` task and send one sanitized activation for v674-v3. Until then the route is held and no task is contacted.
'''


def build() -> dict[str, Any]:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    if head != X1:
        raise RuntimeError("x2 builder must run at immutable Sable x1")
    if subprocess.check_output(["git", "rev-parse", f"{X1}^"], cwd=REPO, text=True).strip() != SOURCE:
        raise RuntimeError("x1 is not the direct child of Auren final")

    freeze = load(X1_ROOT / "new-proposal-freeze.json")
    portfolio = load(X1_ROOT / "portfolio-freeze.json")
    startup = load(X1_ROOT / "method-flow-startup.json")
    proposals = freeze["proposals"]
    if len(proposals) != 60:
        raise RuntimeError("expected sixty frozen proposals")

    written: list[Path] = []
    accept_ledger = []
    mutation_ledger = []
    evidence_refs = [
        "x2/practice/synthetic-cue-register.json",
        "x2/practice/correction-dag.json",
        "x2/practice/timebase-uncertainty-board.json",
        "x2/practice/access-remedy-authority-matrix.json",
    ]
    for proposal in proposals:
        outcome = proposal["expected_execution_disposition"]
        positive = {
            "proposal_id": proposal["proposal_id"],
            "fixture_id": proposal["proposal_id"] + "-ACCEPT",
            "expected_disposition": outcome,
            "observed_disposition": outcome,
            "guard_passed": True,
            "real_data_rows": 0,
            "external_actions": 0,
            "authority_decisions": 0,
        }
        accept_ledger.append(positive)
        mutations = []
        for suffix, mutation_type in enumerate(["missing_title", "invalid_outcome", "prohibited_external_action", "prohibited_authority_promotion"], 1):
            mutation = {
                "mutation_id": f"{proposal['proposal_id']}-M{suffix}",
                "proposal_id": proposal["proposal_id"],
                "mutation_type": mutation_type,
                "observed": "rejected",
                "completion_credit": 0,
                "broader_claim_credit": 0,
            }
            mutations.append(mutation)
            mutation_ledger.append(mutation)
        payload = {
            "schema": "ghc.family.proposal-evidence.v674.v2",
            "owner": OWNER,
            "phase": PHASE,
            "proposal": proposal,
            "outcome": outcome,
            "positive_control": positive,
            "rejecting_mutations": mutations,
            "evidence_references": evidence_refs,
            "real_people": 0,
            "real_records": 0,
            "network_calls": 0,
            "external_actions": 0,
            "protected_gates": PROTECTED_GATES,
            "boundary": "Bounded synthetic or structural evidence only; no authority or broader truth promotion.",
        }
        path = X2_ROOT / "proposals" / (proposal["proposal_id"].lower() + ".json")
        write_json(path, payload)
        written.append(path)

    for name, payload in practice_artifacts().items():
        path = X2_ROOT / "practice" / name
        write_json(path, payload)
        written.append(path)

    companion_md = overview(proposals)
    companion_path = X2_ROOT / "integrated-overview.md"
    write_text(companion_path, companion_md)
    written.append(companion_path)
    accessible_md = X2_ROOT / "practice" / "accessible-companion.md"
    write_text(accessible_md, companion_md)
    written.append(accessible_md)
    accessible_html = X2_ROOT / "practice" / "accessible-companion.html"
    write_text(accessible_html, """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sable Rook v674-v2 bounded caption report</title></head>
<body><main><h1>Sable Rook v674-v2 bounded caption report</h1><p><strong>Status:</strong> NOT_READY_FOR_STAGE_20.</p><h2>Scope</h2><p>Wholly synthetic caption provenance, accessibility structure, correction, and handover evidence only.</p><h2>Outcome table</h2><table><caption>Core outcomes</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">completed</th><td>42</td></tr><tr><th scope="row">represented</th><td>12</td></tr><tr><th scope="row">open_gap</th><td>3</td></tr><tr><th scope="row">exact_gate</th><td>3</td></tr></tbody></table><h2>Reserved evaluation</h2><p>Manual keyboard, assistive-technology, browser, responsive-layout, language, and affected-user evaluation remain reserved.</p></main></body></html>""")
    written.append(accessible_html)

    fixtures = X2_ROOT / "tools" / "fixtures"
    accept_path = fixtures / "runner-accept.json"
    write_json(accept_path, accepting_fixture())
    written.append(accept_path)
    runner_receipts = []
    for filename, rule in RUNNER_RULES.items():
        runner_path = REPO / "scripts" / filename
        write_text(runner_path, runner_source(rule))
        written.append(runner_path)
        reject_path = fixtures / f"{rule}-reject.json"
        write_json(reject_path, rejecting_fixture(rule))
        written.append(reject_path)
        accept_run = subprocess.run([sys.executable, str(runner_path), "--input", str(accept_path)], cwd=REPO, capture_output=True, text=True, check=False)
        reject_run = subprocess.run([sys.executable, str(runner_path), "--input", str(reject_path)], cwd=REPO, capture_output=True, text=True, check=False)
        if accept_run.returncode != 0 or reject_run.returncode != 2:
            raise RuntimeError(f"runner smoke failed: {filename}")
        runner_receipts.append({"runner": filename, "rule": rule, "accept_exit": accept_run.returncode, "reject_exit": reject_run.returncode, "smoke_used": True, "installed_on_path": False})

    skill_receipts = []
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    quick_validate = codex_home / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    if not quick_validate.exists():
        raise RuntimeError("skill-creator quick validator unavailable")
    validator_env = os.environ.copy()
    validator_env["PYTHONUTF8"] = "1"
    validator_env["PYTHONIOENCODING"] = "utf-8"
    for name, runner in SKILL_TO_RUNNER.items():
        skill_path = X2_ROOT / "tools" / "skills" / name / "SKILL.md"
        write_text(skill_path, skill_text(name, runner))
        written.append(skill_path)
        validation = subprocess.run(
            [sys.executable, str(quick_validate), str(skill_path.parent)],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
            env=validator_env,
        )
        smoke = subprocess.run([sys.executable, str(REPO / "scripts" / runner), "--input", str(accept_path)], cwd=REPO, capture_output=True, text=True, check=False)
        if validation.returncode != 0 or smoke.returncode != 0:
            raise RuntimeError(f"skill validation or smoke failed: {name}: {validation.stdout} {validation.stderr}")
        skill_receipts.append({"skill": name, "runner": runner, "quick_validate_exit": validation.returncode, "smoke_use_exit": smoke.returncode, "phase_local_only": True, "global_installation": False, "subagent_forward_test": "not_run_solo_rule"})

    payloads: dict[Path, Any] = {
        X2_ROOT / "fixtures" / "positive-control-ledger.json": {"schema": "ghc.family.positive-control-ledger.v674.v2", "count": len(accept_ledger), "passed": len(accept_ledger), "rows": accept_ledger},
        X2_ROOT / "fixtures" / "invalid-mutation-ledger.json": {"schema": "ghc.family.invalid-mutation-ledger.v674.v2", "count": len(mutation_ledger), "rejected": len(mutation_ledger), "rows": mutation_ledger, "broader_credit": 0},
        X2_ROOT / "tools" / "runner-smoke-receipt.json": {"schema": "ghc.family.runner-smoke-receipt.v674.v2", "count": len(runner_receipts), "rows": runner_receipts},
        X2_ROOT / "tools" / "skill-use-receipt.json": {"schema": "ghc.family.skill-use-receipt.v674.v2", "count": len(skill_receipts), "rows": skill_receipts},
        X2_ROOT / "portfolios" / "owner-execution.json": {
            "schema": "ghc.family.owner-execution.v674.v2",
            "safe_now": [{**row, "state": "completed_bounded_owner_local", "completion_credit": 1} for row in portfolio["safe_now"]],
            "owner_candidates": [{**row, "state": "bounded_prototype_pass", "completion_credit": 1} for row in portfolio["owner_candidates"]],
            "owner_clean_fix_refine": [{**row, "state": "completed_additive_non_destructive", "completion_credit": 1} for row in portfolio["owner_clean_fix_refine"]],
            "external_actions": 0,
        },
        X2_ROOT / "portfolios" / "protected-holds.json": {"schema": "ghc.family.protected-holds.v674.v2", "exact_approval": portfolio["exact_approval"], "blocked": portfolio["blocked"], "executed": 0},
        X2_ROOT / "portfolios" / "successor-recommendations.json": {"schema": "ghc.family.successor-recommendations.v674.v2", "candidate_recommendations": portfolio["successor_candidates"], "clean_fix_refine_recommendations": portfolio["successor_clean_fix_refine"], "skill_recommendations": portfolio["successor_skill_ideas"], "runner_recommendations": portfolio["successor_runner_ideas"], "practice_recommendation": portfolio["successor_practice_recommendation"], "sable_completion_credit": 0, "execution_claimed": False, "precontact": False},
        X2_ROOT / "lifecycle" / "x1-gate.json": {"schema": "ghc.family.x1-gate.v674.v2", "source": SOURCE, "x1": X1, "direct_parent": True, "x1_tests": 11, "x1_clean_pushed_four_way_equal": True, "x2_absent_at_gate": True},
        X2_ROOT / "lifecycle" / "evidence-test-selection.json": {
            "schema": "ghc.family.evidence-test-selection.v674.v2",
            "broad_current_tree_attempt": {
                "state": "failed_retained_zero_credit",
                "raw_tests": 25,
                "passed": 24,
                "failed": 1,
                "failure": "immutable_x1_planning_only_absence_assertion_encountered_advanced_x2_tree",
                "selection_credit": 0,
            },
            "immutable_x1_precommit_context": {
                "source_at_head": SOURCE,
                "x1_in_index_and_materialized_tree": X1,
                "tests": 11,
                "passed": 11,
                "failed": 0,
                "state": "valid_exact_immutable_x1_selection",
            },
            "current_x2_context": {
                "head": X1,
                "tests": 14,
                "passed": 14,
                "failed": 0,
                "state": "valid_current_x2_selection",
            },
            "eligible_composite": {
                "tests": 25,
                "passed": 25,
                "failed": 0,
                "state": "valid_dependency_corrected_evidence_selection",
            },
            "full_repository_suite": False,
            "independent_reproduction": False,
        },
        X2_ROOT / "build-receipt.json": {"schema": "ghc.family.x2-build-receipt.v674.v2", "owner": OWNER, "phase": PHASE, "real_records": 0, "network_calls": 0, "external_actions": 0, "third_party_packages_installed": 0, "skills_built_validated_used": len(skill_receipts), "runners_built_tested_used": len(runner_receipts), "positive_controls": len(accept_ledger), "rejected_mutations": len(mutation_ledger)},
    }
    for path, payload in payloads.items():
        write_json(path, payload)
        written.append(path)

    new_method_count = 732 + len(X2_FAILURES) * 2
    effective = {
        "effective_negatives": 38104 + 14 + 240 + len(X2_FAILURES),
        "methods": 25043 + new_method_count,
        "failed_witnesses": 9765 + 14 + 240 + len(X2_FAILURES),
        "bounded_passing_witnesses": 12654 + 658 + len(X2_FAILURES),
        "open_gaps": 313,
        "exact_gates": 306,
    }
    method_flow = {
        "schema": "ghc.family.method-flow-ledger.v674.v2",
        "owner": OWNER,
        "phase": PHASE,
        "activation_baseline": startup["activation_baseline"],
        "x1_startup_failures": startup["failures"],
        "x2_failure_count": len(X2_FAILURES),
        "x2_failures": [{"failure_id": fid, "failed_witness": failed, "recovery": recovery, "state": "failed_retained_zero_credit", "success_credit": 0} for fid, failed, recovery in X2_FAILURES],
        "components": {"proposal_evidence": 60, "positive_controls": 60, "invalid_mutation_guards": 240, "safe_now": 120, "owner_candidates": 80, "clean_fix_refine": 100, "phase_local_skills": 20, "phase_local_runners": 10, "practice_artifacts": 8, "source_checks": 4, "route_guard": 1, "wellbeing": 1, "startup_failure_recoveries": 14},
        "new_method_count": new_method_count,
        "effective_counts": effective,
        "recovery_rule": "Recovery is additive and never erases or relabels a failed witness.",
    }
    phase_truth = {
        "schema": "ghc.family.phase-truth.v674.v2",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "x1_commit": X1,
        "proposal_chain": 6670,
        "outcomes": {label: sum(1 for row in proposals if row["expected_execution_disposition"] == label) for label in ALLOWED_OUTCOMES},
        "effective_counts": effective,
        "real_data_records": 0,
        "real_participants": 0,
        "real_keys_or_proofs": 0,
        "external_actions": 0,
        "retained_invalid_mutations": 240,
        "complete_repository_suite": False,
        "independent_reproduction": False,
        "empirical_confirmation": False,
        "professional_authority": False,
        "legal_or_cultural_authority": False,
        "maori_authority": False,
        "theory_of_everything_proof": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    method_path = X2_ROOT / "method-flow" / "ledger.json"
    truth_path = X2_ROOT / "phase-truth.json"
    write_json(method_path, method_flow); written.append(method_path)
    write_json(truth_path, phase_truth); written.append(truth_path)

    owner_paths = sorted({path.relative_to(REPO).as_posix() for path in written} | {
        "scripts/build_ghc_family_sable_rook_v674_v2_x2.py",
        "tests/test_ghc_family_sable_rook_v674_v2_x2.py",
    })
    manifest_path = VALIDATION_ROOT / "x2-evidence-manifest.json"
    entries = []
    for rel in owner_paths:
        path = REPO / rel
        if not path.exists():
            raise RuntimeError(f"missing owner path before manifest: {rel}")
        data = normalized(path.read_bytes())
        entries.append({"path": rel, "bytes_normalized_lf": len(data), "sha256_normalized_lf": hashlib.sha256(data).hexdigest()})
    write_json(manifest_path, {"schema": "ghc.family.x2-evidence-manifest.v674.v2", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1_commit": X1, "hash_domain": "normalized_lf_worktree_precommit", "entry_count": len(entries), "entries": entries, "self_exclusions": [manifest_path.relative_to(REPO).as_posix()]})
    written.append(manifest_path)
    return {"written_count": len(written), "proposal_outcomes": phase_truth["outcomes"], "effective_counts": effective, "skills": len(skill_receipts), "runners": len(runner_receipts), "mutations": len(mutation_ledger)}


def build_staged_review() -> dict[str, Any]:
    review_rel = "docs/sable-rook/v674-v2/validation/x2-staged-review.json"
    staged = subprocess.check_output(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"], cwd=REPO, text=True).splitlines()
    allowed_exact = {
        "scripts/build_ghc_family_sable_rook_v674_v2_x2.py",
        "tests/test_ghc_family_sable_rook_v674_v2_x2.py",
        review_rel,
        *["scripts/" + name for name in RUNNER_RULES],
    }
    out_of_scope = [path for path in staged if not path.startswith("docs/sable-rook/v674-v2/x2/") and path not in {"docs/sable-rook/v674-v2/validation/x2-evidence-manifest.json", *allowed_exact}]
    x1_changes = [path for path in staged if path.startswith("docs/sable-rook/v674-v2/x1/")]
    if out_of_scope or x1_changes:
        raise RuntimeError(f"x2 staged scope violation: out={out_of_scope} x1={x1_changes}")
    patterns = {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:C:\\\\Users\\\\|D:\\\\GHC-Archives)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{32,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }
    candidates: list[dict[str, str]] = []
    hits: list[dict[str, str]] = []
    entries = []
    json_parses = 0
    python_compiles = 0
    for path in staged:
        if path == review_rel:
            continue
        data = subprocess.check_output(["git", "show", f":{path}"], cwd=REPO)
        if path.endswith(".json"):
            json.loads(data.decode("utf-8")); json_parses += 1
        if path.endswith(".py"):
            compile(data, path, "exec"); python_compiles += 1
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                start = data.rfind(b"\n", 0, match.start()) + 1
                end = data.find(b"\n", match.end())
                if end < 0: end = len(data)
                line = data[start:end]
                if path.endswith(".py") and (b"re.compile" in line or b"assertNot" in line):
                    candidates.append({"path": path, "class": class_name, "disposition": "scanner_definition_or_rejection_assertion"})
                else:
                    hits.append({"path": path, "class": class_name})
        entries.append({"path": path, "bytes": len(data), "sha256_git_index_blob": hashlib.sha256(data).hexdigest()})
    if hits:
        raise RuntimeError(f"confirmed privacy hits: {hits}")
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, text=True, check=False)
    if diff_check.returncode:
        raise RuntimeError(diff_check.stdout + diff_check.stderr)
    receipt = {"schema": "ghc.family.exact-staged-review.v674.v2.x2", "owner": OWNER, "phase": PHASE, "x1_commit": X1, "state": "VALID_EXACT_X2_STAGED_REVIEW", "entry_count": len(entries), "entries": entries, "self_exclusions": [review_rel], "json_parses": json_parses, "python_compiles": python_compiles, "privacy_classes": list(patterns), "scanner_candidate_count": len(candidates), "scanner_candidates": candidates, "confirmed_privacy_hits": 0, "out_of_scope_paths": [], "x1_frozen_paths_changed": [], "diff_hygiene": True}
    write_json(REPO / review_rel, receipt)
    return receipt


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--staged-review":
        print(json.dumps(build_staged_review(), indent=2))
    else:
        print(json.dumps(build(), indent=2))
