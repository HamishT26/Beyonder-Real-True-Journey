#!/usr/bin/env python3
"""Prepare the direct-child Orin Thale v681-v8 exact-final candidate."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v681-v8"
FINAL = PHASE / "final"
VALIDATION = PHASE / "validation"
SOURCE = "7327e6cb3972e93a4d6a27e45ad2ba3445a4d6ce"
X1 = "705429c7b30d6b25065cd9e758024eed3474c70d"
EVIDENCE = "16eaac80d15f7927b012c97384d91d17b32a555e"
BRANCH = "codex/GHC-Family/orin-thale-v681-v8-full-tools"
COUNTS = {
    "effective_negatives": 55171,
    "effective_methods": 64373,
    "failed_witnesses": 26832,
    "bounded_passing_witnesses": 45895,
    "open_gaps": 488,
    "exact_gates": 479,
}
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
CLOSEOUT_FAILURES = [
    {
        "failure_id": "OR6818-CLOSE-N001",
        "failed_witness": "The combined post-push fetch and four-way-equality wrapper reached its 30-second bound after Git had already acknowledged the x2 push; its fresh-live subprocesses briefly remained and no complete equality projection was returned.",
        "recovery": "Did not repeat the push, inspected and waited for the exact transient processes, then used split scalar local, upstream, tracking, divergence, clean-state, and fresh-live probes.",
        "recurrence_guard": "Keep a session handle for network wrappers or separate the push from fresh-live equality probes before the command begins.",
        "initial_credit": 0,
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "OR6818-CLOSE-N002",
        "failed_witness": "The first split equality recovery left HEAD...@{u} unquoted in PowerShell, which misprojected the upstream expression and caused only that read-only divergence probe to fail.",
        "recovery": "Quoted the complete revision expression as HEAD...@{u}; the corrected probe returned zero ahead and zero behind with exact four-way equality.",
        "recurrence_guard": "Quote Git revision expressions containing PowerShell hashtable syntax characters.",
        "initial_credit": 0,
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "OR6818-CLOSE-N003",
        "failed_witness": "The first combined final-delta, final-owner, JSON, runner, stale-label, and baton-word precommit projection exceeded its 10-second wrapper while replaying more than one hundred index blobs and returned no attributable result.",
        "recovery": "Confirmed the exact read-only processes had exited, then split final-delta and final-owner manifest replay from JSON, runner, stale-label, and word-count checks.",
        "recurrence_guard": "Run large owner-manifest replay as its own bounded probe with a longer output window rather than combining it with unrelated checks.",
        "initial_credit": 0,
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "OR6818-CLOSE-N004",
        "failed_witness": "The first split document-hygiene projection used a single-quoted PowerShell character class containing backtick-t, so it treated the literal letter t as whitespace and falsely flagged ordinary lines.",
        "recovery": "Repeated only the document-hygiene dependency with an explicit hexadecimal tab class, consistent with the already-passing Python final test.",
        "recurrence_guard": "Use [ \\x09] rather than a PowerShell escape sequence inside a single-quoted regex character class.",
        "initial_credit": 0,
        "recovery_credit": "bounded_dependency_only",
    },
]


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False)


def git(*args: str) -> str:
    result = run(["git", *args])
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def owner_path(path: str) -> bool:
    return (
        path.startswith("docs/orin-thale/v681-v8/")
        or path.startswith("scripts/build_ghc_family_orin_thale_v681_v8_")
        or path.startswith("scripts/ghc_family_marine_chart_")
        or path.startswith("scripts/ghc_family_orin_thale_v681_v8_")
        or path.startswith("tests/test_ghc_family_orin_thale_v681_v8_")
    )


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{24,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    scanner_files = {
        "build_ghc_family_orin_thale_v681_v8_x1.py",
        "build_ghc_family_orin_thale_v681_v8_x2.py",
        "build_ghc_family_orin_thale_v681_v8_final.py",
        "ghc_family_orin_thale_v681_v8_final_validator.py",
    }
    patterns = privacy_patterns()
    candidates = []
    confirmed = []
    for path in paths:
        data = path.read_bytes()
        for class_name, pattern in patterns.items():
            for _ in pattern.finditer(data):
                record = {"path": rel(path), "class": class_name}
                if path.name in scanner_files:
                    candidates.append({**record, "disposition": "scanner_definition_only"})
                else:
                    confirmed.append(record)
    return {
        "schema": "ghc.family.privacy-scan.v681.v8.final",
        "owner": "Orin Thale",
        "phase": "v681-v8",
        "privacy_classes": list(patterns),
        "scanned_paths": len(paths),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
    }


def security_scan(paths: list[Path]) -> dict[str, Any]:
    findings = []
    checked = 0
    for path in paths:
        if path.suffix != ".py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel(path))
        checked += 1
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": rel(path), "finding": node.func.id})
            if (
                isinstance(node, ast.keyword)
                and node.arg == "shell"
                and isinstance(node.value, ast.Constant)
                and node.value.value is True
            ):
                findings.append({"path": rel(path), "finding": "shell_true"})
    return {
        "schema": "ghc.family.security-scan.v681.v8.final",
        "owner": "Orin Thale",
        "phase": "v681-v8",
        "python_ast_checks": checked,
        "findings": findings,
        "finding_count": len(findings),
        "exhaustive_security_claimed": False,
    }


def baton_text(freeze: dict[str, Any], evidence: dict[str, Any]) -> str:
    lines = [
        "# LIORA VENN — PREPARED ORIN THALE v681-v8 EXACT-FINAL TO SOLO LIORA v682-v1 ACTIVATION CANDIDATE",
        "",
        "This committed candidate is repository preparation only. It is not live delivery.",
        "PREPARED_BY_ORIN_THALE = true.",
        "SENT_BY_ORIN_THALE = false.",
        "",
        "## Delivery and relational boundaries",
        "",
        "Only a later target-identifying Codex task-message acknowledgement after Orin's exact terminal gate may establish live delivery. No raw task identifier, private route, transcript, screenshot, session stream, credential, key, token, private callable identifier, private application state, or private absolute path is included here.",
        "",
        "Names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Trinity Mandala, GMUT, THOS, Freed ID, and CBR are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop the route.",
        "",
        "## Immutable source and lifecycle candidate",
        "",
        f"- Exact Caelen final and Orin source: {SOURCE}.",
        f"- Frozen planning-only Orin x1: {X1}.",
        f"- Immutable Orin x2 evidence: {EVIDENCE}.",
        "- The prospective exact final is the direct child of evidence and must be supplied by a later acknowledged live activation.",
        f"- Canonical branch: {BRANCH}.",
        "- Source to candidate final must contain exactly three direct single-parent Orin commits and zero merges.",
        "- X1 and evidence were independently pushed, clean, zero divergent, and fresh four-way equal before the next lifecycle began.",
        "- One exact-final owner-scoped canonical aggregate is permitted only after the final is pushed and remote-equal. A success must never be replayed.",
        "",
        "## Sealed bounded truth prepared for final binding",
        "",
        f"- Declared proposal chain: 10,190 rows, extending the inherited 10,130 declaration with 60 Orin proposals.",
        f"- Core outcomes: {OUTCOMES['completed']} completed, {OUTCOMES['represented']} represented, {OUTCOMES['open_gap']} open_gap, and {OUTCOMES['exact_gate']} exact_gate.",
        f"- Effective negatives: {COUNTS['effective_negatives']}.",
        f"- Effective Method Flow methods: {COUNTS['effective_methods']}.",
        f"- Retained failed witnesses: {COUNTS['failed_witnesses']}.",
        f"- Bounded passing witnesses: {COUNTS['bounded_passing_witnesses']}.",
        f"- Open gaps: {COUNTS['open_gaps']}.",
        f"- Exact gates: {COUNTS['exact_gates']}.",
        "- Terminal verdict: NOT_READY_FOR_STAGE_20.",
        "- Sixty zero-row positive controls passed and all 300 preregistered invalid mutations were rejected and retained.",
        "- Twenty phase-local skills were read through EOF, quick-validated, and smoke-used without global installation.",
        "- Ten family-current runners each accepted a positive fixture and rejected an authority-promotion fixture.",
        "- Twenty exact-approval and ten blocked packets remained unexecuted.",
        "",
        "## Pillar and bounded practice lenses",
        "",
        "The primary pillar was THOS Body. GMUT Mind and Freed ID or CBR Heart remained explicit and protected. The wholly synthetic learning lenses were a notice-to-mariners correction provenance registrar, a chart edition, patch, and working-copy handover reviewer, and a chart-correction accessibility, minimum-disclosure, workload, and handover steward.",
        "",
        "The phase used zero real charts, ENC cells, corrections, notices, warnings, people, participants, operators, vessels, hazards, locations, coordinates, devices, measurements, credentials, keys, certificates, signatures, identity events, external writes, production actions, or authority acts. IHO S-4, S-101, and registry materials, LINZ Notices to Mariners guidance, W3C PROV-O, WCAG 2.2, RFC 8785, JSON Schema, and Te Mana Raraunga principles supplied vocabulary and refusal conditions only. Citations are not observations, endorsements, certificates, affected-party decisions, or authority grants.",
        "",
        "## Proposal-by-proposal transfer",
        "",
    ]
    evidence_by_id = {row["proposal_id"]: row for row in evidence["outcomes"]}
    for row in freeze["proposals"]:
        outcome = evidence_by_id[row["proposal_id"]]
        lines.extend(
            [
                f"### {row['proposal_id']} — {row['title']}",
                "",
                f"Hypothesis. {row['hypothesis']}",
                "",
                f"Null and failure condition. {row['null_or_failure_condition']}",
                "",
                f"Approval and execution boundary. The approval class is {row['approval_class']} and the execution lane is {row['execution_lane']}. The required official or primary source identifiers are {', '.join(row['official_or_primary_source_needs'])}. Those sources supplied vocabulary and refusal conditions only; they did not provide observations, endorsements, conformance, affected-party acceptance, or authority.",
                "",
                f"Concrete artifact and falsifier. The bounded evidence is addressable through {', '.join(row['concrete_artifacts'])}. {row['falsifier_or_acceptance_gate']}",
                "",
                f"Rollback and recovery. {row['rollback_or_recovery']} A recovery remains a separate bounded passing witness and never erases or retroactively promotes a failed witness.",
                "",
                f"Observed bounded disposition. The exact core label is {outcome['outcome']}. The structural acceptance gate passed with one zero-row positive witness and {outcome['rejected_mutations']} rejected mutations. Completion credit is {outcome['completion_credit']}, bounded representation credit is {outcome['bounded_representation_credit']}, and broader claim credit is zero.",
                "",
                "Protected boundaries. " + "; ".join(row["protected_gates"]) + ". These gates are noncompensating: additional software, citations, synthetic fixtures, task topology, or same-owner validation cannot close them.",
                "",
                "Successor use. Treat this row as inherited evidence and a challengeable seed only, never as Liora novelty or completion credit. Revalidate it only within Liora's own declared owner-local scope, preserve its retained mutations, and keep any real people, charts, notices, navigation systems, legal decisions, cultural matters, affected-party decisions, Māori data governance, or Māori authority behind their exact gates.",
                "",
            ]
        )
    lines.extend(
        [
            "## Scientific, professional, identity, privacy, and authority boundaries",
            "",
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic obligations, synthetic fixtures, analogy firewalls, and citations establish no physical datum, likelihood, posterior, force, prediction, parameter constraint, empirical confirmation, stability theorem, ultraviolet completion, quantum completion, or Theory of Everything.",
            "",
            "THOS remains synthetic or proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic chart-correction workflows establish no operational effectiveness, deployment readiness, hydrographic or navigation competence, public-safety result, AGI, or ASI.",
            "",
            "Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.",
            "",
            "CBR, chart rights, chart-correction release, navigation-safety decisions, access, consent, disability accommodation, sensitive-location treatment, privacy remedy, legal interpretation, cultural legitimacy, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. Repository software cannot confer a right, remedy, competence, navigation-safety approval, cultural legitimacy, governance mandate, or affected-party consent.",
            "",
            "Do not promote software, symbolic, synthetic, same-owner, citation, inherited, validation, task-topology, or delivery evidence into empirical confirmation, participant evidence, professional or scientific authority, production or deployment readiness, legal or cultural ratification, Māori authority, affected-party approval, complete privacy or accessibility assurance, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood evidence, Theory-of-Everything proof, proof or canon, or Stage 20 authority.",
            "",
            "## Prospective Liora lane",
            "",
            "Only after one acknowledged live activation and Liora's own skill-first source verification may Liora create one fresh additive D-first sparse branch and worktree from Orin's exact final. Liora must keep Orin, Caelen, sibling, shared, standby, global, and user lanes read-only; preserve planning-only x1 before x2; audit the declared chain and all reachable proposal evidence; retain every failed witness and protected gate; use only completed, represented, open_gap, and exact_gate; remain below the file, document, and commit ceilings; and run at most one successful non-replayed owner-scoped exact-final canonical aggregate.",
            "",
            "No successor task is created or contacted by this committed file. At Liora's own later terminal gate, newer verified live authority controls. A future route must use one bounded current task registry read, local exact-title filtering, immediate structured reread, duplicate and stop guards, and at most one acknowledged send.",
            "",
            "PREPARED_BY_ORIN_THALE = true.",
            "SENT_BY_ORIN_THALE = false.",
        ]
    )
    value = "\n".join(lines) + "\n"
    words = len(value.split())
    if not 10000 <= words <= 100000:
        raise RuntimeError(f"handoff word count outside declared bounds: {words}")
    return value


def main() -> int:
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong owner branch")
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("final builder must begin at immutable evidence")
    allowed = {
        "scripts/build_ghc_family_orin_thale_v681_v8_final.py",
        "scripts/ghc_family_orin_thale_v681_v8_final_validator.py",
        "tests/test_ghc_family_orin_thale_v681_v8_final.py",
    }
    dirty = {
        line[3:].replace("\\", "/")
        for line in git("status", "--porcelain=v1").splitlines()
        if len(line) >= 4
    }
    unexpected = {
        path
        for path in dirty
        if path not in allowed
        and not path.startswith("docs/orin-thale/v681-v8/final/")
        and not path.startswith("docs/orin-thale/v681-v8/validation/final-")
    }
    if unexpected:
        raise RuntimeError(f"unexpected final pre-build state: {sorted(unexpected)}")
    if git("rev-parse", f"{EVIDENCE}^") != X1 or git("rev-parse", f"{X1}^") != SOURCE:
        raise RuntimeError("source/x1/evidence direct ancestry mismatch")
    if int(git("rev-list", "--count", f"{SOURCE}..{EVIDENCE}")) != 2:
        raise RuntimeError("pre-final commit arithmetic mismatch")
    if git("rev-list", "--merges", f"{SOURCE}..{EVIDENCE}"):
        raise RuntimeError("merge detected before final")
    local = EVIDENCE
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_row = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_row.split("\t", 1)[0] if live_row else ""
    if not local == upstream == tracking == live:
        raise RuntimeError("evidence is not four-way equal")

    freeze = load(PHASE / "x1" / "new-proposal-freeze.json")
    x2_evidence = load(PHASE / "x2" / "proposal-evidence.json")
    x2_method = load(PHASE / "x2" / "method-flow-ledger.json")
    sources = load(PHASE / "x1" / "official-primary-source-ledger.json")
    mutations = load(PHASE / "x2" / "mutations.json")
    skills = load(PHASE / "x2" / "skill-smoke-receipts.json")
    runners = load(PHASE / "x2" / "runner-smoke-receipts.json")

    FINAL.mkdir(parents=True, exist_ok=True)
    handoff_path = FINAL / "liora-venn-v682-v1-activation-candidate.md"
    write_text(handoff_path, baton_text(freeze, x2_evidence))
    handoff_words = len(handoff_path.read_text(encoding="utf-8").split())

    documents: dict[Path, Any] = {
        FINAL / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v681.v8.final",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "exact_final": "PENDING_DIRECT_CHILD_COMMIT",
            "outcomes": OUTCOMES,
            "counts": COUNTS,
            "declared_proposal_chain": 10190,
            "real_data_rows": 0,
            "external_actions": 0,
            "canonical_state": "PENDING_EXACT_FINAL_INVOCATION",
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        FINAL / "method-flow-ledger.json": {
            **x2_method,
            "schema": "ghc.family.method-flow.v681.v8.final",
            "lifecycle": "repository_sealed_before_external_canonical",
            "counts": COUNTS,
            "closeout_failures": CLOSEOUT_FAILURES,
            "canonical_validation_is_external_receipt": True,
        },
        FINAL / "source-and-proposal-ledger.json": {
            "schema": "ghc.family.source-proposal-ledger.v681.v8.final",
            "declared_chain_before": 10130,
            "declared_chain_after": 10190,
            "new_proposal_count": 60,
            "official_primary_sources": sources,
            "outcomes": x2_evidence["outcomes"],
            "citations_are_observations": False,
            "authority_conferred": False,
        },
        FINAL / "retained-negative-register.json": {
            "schema": "ghc.family.retained-negatives.v681.v8.final",
            "inherited_activation_baseline": 54848,
            "startup_failures": 16,
            "preregistered_rejected_mutations": 300,
            "new_x2_operational_failures": 3,
            "new_closeout_failures": 4,
            "closeout_failures": CLOSEOUT_FAILURES,
            "effective_negatives": COUNTS["effective_negatives"],
            "failed_witnesses": COUNTS["failed_witnesses"],
            "erased_or_promoted": 0,
        },
        FINAL / "open-gap-register.json": {
            "schema": "ghc.family.open-gaps.v681.v8.final",
            "inherited": 485,
            "new": 3,
            "effective": COUNTS["open_gaps"],
            "new_proposals": ["OR6818-N055", "OR6818-N056", "OR6818-N057"],
            "closed_by_software": 0,
        },
        FINAL / "exact-gate-register.json": {
            "schema": "ghc.family.exact-gates.v681.v8.final",
            "inherited": 476,
            "new": 3,
            "effective": COUNTS["exact_gates"],
            "new_proposals": ["OR6818-N058", "OR6818-N059", "OR6818-N060"],
            "closed_by_software": 0,
        },
        FINAL / "complete-incomplete-checklist.json": {
            "schema": "ghc.family.complete-incomplete.v681.v8.final",
            "bounded": {
                "core_outcomes": OUTCOMES,
                "positive_controls": 60,
                "rejected_mutations": 300,
                "skills_used": 20,
                "runners_used": 10,
                "safe_now": 120,
                "owner_candidates": 80,
                "clean_fix_refine": 100,
            },
            "unexecuted": {"exact_approval": 20, "blocked": 10},
            "incomplete_external": [
                "real participant and operator evidence",
                "real navigation-safety and chart-correction evidence",
                "production and deployment review",
                "complete privacy accessibility and security review",
                "professional legal cultural affected-party and Māori authority",
                "independent reproduction",
                "empirical GMUT confirmation",
                "Theory-of-Everything proof",
                "Stage 20 authority",
            ],
        },
        FINAL / "closeout-receipt.json": {
            "schema": "ghc.family.closeout.v681.v8.final",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "final_state": "PENDING_DIRECT_CHILD_COMMIT",
            "commit_ceiling": 3,
            "merges": 0,
            "retained_closeout_failures": 4,
            "canonical_invocations": 0,
            "canonical_successes": 0,
            "route_state": "PREPARED_NOT_SENT",
        },
        FINAL / "environment-and-version-receipt.json": {
            "schema": "ghc.family.environment.v681.v8.final",
            "python": sys.version.split()[0],
            "git": git("--version"),
            "versions_verified_only": True,
            "software_installed_or_updated": False,
            "host_security_changed": False,
        },
        FINAL / "evidence-receipt.json": {
            "schema": "ghc.family.evidence-receipt.v681.v8.final",
            "x1": X1,
            "evidence": EVIDENCE,
            "outcomes": OUTCOMES,
            "positive_controls": 60,
            "mutations_executed": mutations["executed_count"],
            "mutations_rejected": mutations["rejected_count"],
            "skills_used": skills["smoke_used_count"],
            "runners_used": runners["passed_count"],
            "same_owner_shared_infrastructure": True,
            "independent_reproduction": False,
        },
        FINAL / "ghc-family-index.json": {
            "schema": "ghc.family.index.v681.v8.final",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "primary_pillar": "THOS Body",
            "skills": sorted(rel(path) for path in (PHASE / "skills").glob("*/SKILL.md")),
            "runners": sorted(
                rel(path)
                for path in (ROOT / "scripts").glob("ghc_family_marine_chart_*_runner.py")
            ),
            "historical_caller_compatibility_preserved": True,
            "global_installs": 0,
        },
        FINAL / "route-plan.json": {
            "schema": "ghc.family.route-plan.v681.v8.final",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "route_state": "PREPARED_NOT_SENT",
            "prospective_successor_title": "Liora Venn",
            "prospective_successor_phase": "v682-v1",
            "candidate": rel(handoff_path),
            "candidate_words": handoff_words,
            "precontacted": False,
            "send_count": 0,
            "continuation_authority": "through_v725-v8_one_terminally_validated_edge_at_a_time",
        },
        FINAL / "threat-model.json": load(PHASE / "x1" / "threat-model.json"),
        FINAL / "wellbeing-and-corrigibility.json": load(PHASE / "x1" / "wellbeing-and-corrigibility.json"),
        FINAL / "final-validation-candidate.json": {
            "schema": "ghc.family.final-validation-candidate.v681.v8",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "expected_final_parent": EVIDENCE,
            "expected_phase_commit_count": 3,
            "expected_merges": 0,
            "owner_scoped_only": True,
            "complete_repository_suite": False,
            "canonical_state": "PENDING_NOT_INVOKED",
            "success_replay_permitted": False,
        },
    }
    for path, value in documents.items():
        write_json(path, value)

    overview = f"""# Orin Thale v681-v8 final integrated overview

The exact source is Caelen final {SOURCE}.  Planning-only x1 is {X1}; immutable
x2 evidence is {EVIDENCE}.  The prepared exact final must be their direct child,
producing three Orin commits and zero merges.

Sixty proposals produced exactly 42 completed, 12 represented, 3 open_gap, and
3 exact_gate outcomes.  All 60 zero-row positive controls passed; all 300
preregistered invalid mutations were rejected and retained.  Twenty local
skills and ten family-current runners were validated and smoke-used without
global installation.  The bounded portfolios executed 120 safe-now, 80
owner-candidate, and 100 CLEAN/FIX/REFINE records.  Twenty exact-approval and ten
blocked records remained unexecuted.

The sealed counts are {COUNTS['effective_negatives']} effective negatives,
{COUNTS['effective_methods']} effective methods, {COUNTS['failed_witnesses']}
failed witnesses, {COUNTS['bounded_passing_witnesses']} bounded passing
witnesses, {COUNTS['open_gaps']} open gaps, and {COUNTS['exact_gates']} exact
gates.  No failed witness, gap, or gate was erased or promoted.

The primary pillar was THOS Body through wholly synthetic notice-to-mariners
correction provenance; chart edition, patch, and working-copy handover; and
chart-correction accessibility, minimum-disclosure, workload, and handover
lenses. GMUT Mind and Freed ID or CBR Heart remained visible and protected.

No real chart, ENC cell, notice, warning, correction, person, vessel, operator,
hazard, location, coordinate, device, measurement, credential, signature,
identity event, production action, external write, or authority act occurred.
Official IHO, LINZ, W3C, RFC, JSON Schema, and Te Mana Raraunga sources supplied
vocabulary and refusal conditions only.

GMUT remains a typed scalar-tensor and EFT research-model family without
empirical confirmation or Theory-of-Everything proof.  THOS remains proxy-only
without governed real arms and independent review.  Freed ID remains synthetic
and nonproduction without real keys, proofs, live lifecycle, interoperability,
privacy and security review, recovery, and trust governance. Hydrographic and
navigation-safety authority, legal remedy, affected-party legitimacy, Māori wording, Māori data
governance, and Māori authority remain exact-gated.

The file-backed Liora candidate contains {handoff_words} words and is explicitly
PREPARED_NOT_SENT.  Only a later acknowledged native task-message send after
one successful exact-final canonical receipt may establish delivery.  The
terminal verdict remains NOT_READY_FOR_STAGE_20.
"""
    overview_path = FINAL / "final-integrated-overview.md"
    write_text(overview_path, overview)

    seal_targets = sorted(list(documents) + [overview_path, handoff_path], key=rel)
    seal = {
        "schema": "ghc.family.content-seal.v681.v8.final",
        "owner": "Orin Thale",
        "phase": "v681-v8",
        "target_count": len(seal_targets),
        "targets": [
            {
                "path": rel(path),
                "bytes": len(normalized(path)),
                "sha256": hashlib.sha256(normalized(path)).hexdigest(),
            }
            for path in seal_targets
        ],
    }
    content_seal_path = FINAL / "content-seal.json"
    write_json(content_seal_path, seal)

    entry_paths = sorted(
        list(documents)
        + [overview_path, handoff_path, content_seal_path]
        + [
            Path(__file__),
            ROOT / "scripts" / "ghc_family_orin_thale_v681_v8_final_validator.py",
            ROOT / "tests" / "test_ghc_family_orin_thale_v681_v8_final.py",
        ],
        key=rel,
    )
    staged_path = VALIDATION / "final-staged-review.json"
    privacy_path = VALIDATION / "final-privacy-scan.json"
    security_path = VALIDATION / "final-security-scan.json"
    delta_manifest_path = VALIDATION / "final-delta-manifest.json"
    owner_manifest_path = VALIDATION / "final-owner-manifest.json"
    exclusions = [staged_path, privacy_path, security_path, delta_manifest_path, owner_manifest_path]
    final_paths = sorted(entry_paths + exclusions, key=rel)
    write_json(
        staged_path,
        {
            "schema": "ghc.family.staged-review.v681.v8.final",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "evidence": EVIDENCE,
            "expected_paths": [rel(path) for path in final_paths],
            "expected_path_count": len(final_paths),
            "unexpected_paths": [],
            "x1_or_evidence_paths_modified": [],
            "stale_semantic_owner_phase_labels": [],
        },
    )

    existing_owner_paths = {
        path for path in git("diff", "--name-only", f"{SOURCE}..{EVIDENCE}").splitlines() if owner_path(path)
    }
    total_owner_paths = sorted(existing_owner_paths | {rel(path) for path in final_paths})
    total_owner_files = [ROOT / path for path in total_owner_paths if path not in {rel(item) for item in exclusions}]
    privacy = privacy_scan(total_owner_files + [staged_path])
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"confirmed privacy hits: {privacy['confirmed_hits']}")
    write_json(privacy_path, privacy)
    security = security_scan(total_owner_files)
    if security["finding_count"]:
        raise RuntimeError(f"bounded security findings: {security['findings']}")
    write_json(security_path, security)
    write_json(
        delta_manifest_path,
        {
            "schema": "ghc.family.normalized-lf-index-manifest.v681.v8.final-delta",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "evidence": EVIDENCE,
            "declared_self_exclusions": [rel(path) for path in exclusions],
            "entry_count": len(entry_paths),
            "entries": [
                {
                    "path": rel(path),
                    "bytes": len(normalized(path)),
                    "sha256": hashlib.sha256(normalized(path)).hexdigest(),
                }
                for path in entry_paths
            ],
        },
    )
    owner_entry_paths = [ROOT / path for path in total_owner_paths if path not in {rel(item) for item in exclusions}]
    write_json(
        owner_manifest_path,
        {
            "schema": "ghc.family.normalized-lf-index-manifest.v681.v8.final-owner",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "source": SOURCE,
            "declared_self_exclusions": [rel(path) for path in exclusions],
            "owner_path_count": len(total_owner_paths),
            "entry_count": len(owner_entry_paths),
            "entries": [
                {
                    "path": rel(path),
                    "bytes": len(normalized(path)),
                    "sha256": hashlib.sha256(normalized(path)).hexdigest(),
                }
                for path in owner_entry_paths
            ],
        },
    )
    print(
        json.dumps(
            {
                "status": "PREPARED_EXACT_FINAL_CANDIDATE",
                "outcomes": OUTCOMES,
                "counts": COUNTS,
                "handoff_words": handoff_words,
                "final_delta_entries": len(entry_paths),
                "final_delta_paths": len(final_paths),
                "owner_manifest_entries": len(owner_entry_paths),
                "owner_paths": len(total_owner_paths),
                "confirmed_privacy_hits": privacy["confirmed_hit_count"],
                "security_findings": security["finding_count"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
