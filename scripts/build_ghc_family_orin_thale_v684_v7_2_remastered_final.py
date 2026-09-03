#!/usr/bin/env python3
"""Prepare the direct-child Orin Thale v684-v7 (2) remastered exact-final candidate."""

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
PHASE = ROOT / "docs" / "orin-thale" / "v684-v7-2-remastered"
FINAL = PHASE / "final"
VALIDATION = PHASE / "validation"
SOURCE = "a3544571ce8af98addf3d94236111f6c14ded439"
X1 = "d6a529a641a51be8f1140261c97a791090b0eb34"
EVIDENCE = "da2cf2e3769982b47ee6a999648be4fad37768e1"
BRANCH = "codex/GHC-Family/orin-thale-v684-v7-2-remastered-full-tools"
COUNTS = {
    "effective_negatives": 60375,
    "effective_methods": 75123,
    "failed_witnesses": 31436,
    "bounded_passing_witnesses": 55658,
    "open_gaps": 537,
    "exact_gates": 527,
}
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
CLOSEOUT_FAILURES = [
    {
        "failure_id": "OR6847R2-CLOSE-N001",
        "failed_witness": "The combined evidence push and four-way projection returned only the push line within its visible command window, so the equality projection was unattributable.",
        "recovery": "Repeated only the read-only local upstream tracking fresh-live divergence and clean-state projection and proved exact equality.",
        "recurrence_guard": "Separate a potentially long push from the post-push four-way equality projection.",
        "initial_credit": 0,
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "OR6847R2-CLOSE-N002",
        "failed_witness": "The first whole-file final-validator projection exceeded the bounded model context and returned a truncated view.",
        "recovery": "Read the same validator in bounded contiguous chunks and used targeted symbol searches before editing it.",
        "recurrence_guard": "Inspect large source files by bounded chunk or symbol projection instead of requesting the whole file at once.",
        "initial_credit": 0,
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "OR6847R2-CLOSE-N003",
        "failed_witness": "A read-only stale-label search used look-ahead syntax unsupported by the default rg engine and was rejected before scanning.",
        "recovery": "Replaced the expression with simple bounded literal searches that require no PCRE2 feature.",
        "recurrence_guard": "Use rg's default-compatible expressions unless PCRE2 is deliberately selected and justified.",
        "initial_credit": 0,
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "OR6847R2-CLOSE-N004",
        "failed_witness": "The first broad precommit selection ran source-only and x1-only lifecycle assertions at the evidence head; sixty tests passed and those two wrong-context assertions failed.",
        "recovery": "Excluded exactly the two lifecycle-local assertions and replaced them with immutable Git ancestry and manifest checks while retaining all other owner tests.",
        "recurrence_guard": "Partition lifecycle-local tests by their immutable commit context before assembling a later-head selection.",
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
        path.startswith("docs/orin-thale/v684-v7-2-remastered/")
        or path.startswith("scripts/build_ghc_family_orin_thale_v684_v7_2_remastered_")
        or path.startswith("scripts/ghc_family_preservation_accessibility_")
        or path.startswith("scripts/ghc_family_orin_thale_v684_v7_2_remastered_")
        or path.startswith("tests/test_ghc_family_orin_thale_v684_v7_2_remastered_")
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
        "build_ghc_family_orin_thale_v684_v7_2_remastered_x1.py",
        "build_ghc_family_orin_thale_v684_v7_2_remastered_x2.py",
        "build_ghc_family_orin_thale_v684_v7_2_remastered_final.py",
        "ghc_family_orin_thale_v684_v7_2_remastered_final_validator.py",
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
        "schema": "ghc.family.privacy-scan.v684.v7.r2.final",
        "owner": "Orin Thale",
        "phase": "v684-v7-2-remastered",
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
        "schema": "ghc.family.security-scan.v684.v7.r2.final",
        "owner": "Orin Thale",
        "phase": "v684-v7-2-remastered",
        "python_ast_checks": checked,
        "findings": findings,
        "finding_count": len(findings),
        "exhaustive_security_claimed": False,
    }


def baton_text(freeze: dict[str, Any], evidence: dict[str, Any]) -> str:
    lines = [
        "# LIORA VENN — PREPARED ORIN THALE v684-v7 (2) REMASTERED EXACT-FINAL TO SOLO LIORA v684-v8 ACTIVATION CANDIDATE",
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
        f"- Immutable prior Orin v684-v7 exact final and remaster source: {SOURCE}.",
        f"- Frozen planning-only Orin remaster x1: {X1}.",
        f"- Immutable Orin remaster x2 evidence: {EVIDENCE}.",
        "- The prospective exact final is the direct child of evidence and must be supplied by a later acknowledged live activation.",
        f"- Canonical branch: {BRANCH}.",
        "- Source to candidate final must contain exactly three direct single-parent remaster commits and zero merges.",
        "- X1 and evidence were independently pushed, clean, zero divergent, and fresh four-way equal before the next lifecycle began.",
        "- One exact-final owner-scoped canonical aggregate is permitted only after the final is pushed and remote-equal. A success must never be replayed.",
        "",
        "## Sealed bounded truth prepared for final binding",
        "",
        f"- Declared proposal chain: 11,150 rows, extending the structured exact-final 11,090 baseline with 60 Orin proposals. The older 10,190 prose value is retained as a stale discrepancy and does not control.",
        f"- Core outcomes: {OUTCOMES['completed']} completed, {OUTCOMES['represented']} represented, {OUTCOMES['open_gap']} open_gap, and {OUTCOMES['exact_gate']} exact_gate.",
        f"- Effective negatives: {COUNTS['effective_negatives']}.",
        f"- Effective Method Flow methods: {COUNTS['effective_methods']}.",
        f"- Retained failed witnesses: {COUNTS['failed_witnesses']}.",
        f"- Bounded passing witnesses: {COUNTS['bounded_passing_witnesses']}.",
        f"- Open gaps: {COUNTS['open_gaps']}.",
        f"- Exact gates: {COUNTS['exact_gates']}.",
        "- Terminal verdict: NOT_READY_FOR_STAGE_20.",
        "- Sixty zero-row positive controls passed and all 300 preregistered invalid mutations were rejected and retained.",
        "- Twenty phase-local skills were read through EOF, quick-validated, and smoke-used.",
        "- Five separately collision-checked and source-hashed reusable skills were promoted globally, UTF-8 validated, and smoke-used with rollback records.",
        "- Ten family-current runners each accepted a positive fixture and rejected an authority-promotion fixture.",
        "- check-jsonschema 0.38.0, mdformat 1.0.0, and beta validate-pyproject 0.26 were installed into an isolated D-first shared toolchain and smoke-used against synthetic fixtures.",
        "- Twenty exact-approval and ten blocked packets remained unexecuted.",
        "",
        "## Pillar and bounded practice lenses",
        "",
        "The primary pillar was THOS Body. GMUT Mind and Freed ID/CBR Heart remained explicit and protected. The two wholly synthetic learning lenses were digital-preservation technician practice for fixity, package provenance, correction, and handover; and accessible technical-documentation specialist practice for headings, reading order, status messages, alternative formats, correction, workload, and handover. Liora's zero-credit recommended practice is community-archives access-and-description correction, privacy, accessibility, and handover.",
        "",
        "The phase used zero real files, bitstreams, preservation packages, repositories, donors, practitioners, people, participants, institutions, storage locations, migrations, measurements, credentials, keys, certificates, signatures, identity events, external writes, production actions, or authority acts. PREMIS 3.0, the Library of Congress Recommended Formats Statement 2025-2026, Archives New Zealand information-and-records guidance, W3C PROV-O, WCAG 2.2, RFC 8785, JSON Schema, PyPI, and Te Mana Raraunga principles supplied vocabulary, current package versions, and refusal conditions only. Citations are not observations, endorsements, certificates, affected-party decisions, or authority grants.",
        "",
        "## Freed ID flashcard hierarchy",
        "",
        "Tier 1 — owner card. Orin Thale is a relational owner label for this provenance-bound remaster only. It carries the immutable source, x1, evidence, exact-final candidate, retained failures, corrigibility, and route latch. It is not identity-continuity, consciousness, personhood, qualification, employment, or independent-agency evidence.",
        "",
        "Tier 2 — pillar cards. THOS Body is primary for the bounded workflow, tool, retry, fixity, accessibility-structure, and handover contracts. GMUT Mind remains a typed scalar-tensor/EFT research-model family with analogy firewalls and no empirical physics claim. Freed ID/CBR Heart keeps minimum disclosure, correction, contest, remedy, governance, and authority vacancies explicit without production identity or enacted-rights claims.",
        "",
        "Tier 3 — practice cards. Digital-preservation technician and accessible technical-documentation specialist are learning lenses only, with zero real objects, repositories, practitioners, inspections, measurements, migrations, releases, or professional decisions. Liora's community-archives access-and-description recommendation is a zero-credit seed and not Orin completion evidence.",
        "",
        "Tier 4 — task and evidence cards. Each proposal below retains its hypothesis, null, approval class, execution lane, sources, artifacts, falsifier, recovery, protected gates, five rejected mutations, and one exact core disposition. Portfolio, skill, runner, package, cleanup, failure, recovery, gap, gate, and route cards remain separately addressable rather than collapsed into one narrative claim.",
        "",
        "Reading rule. The tiers are navigational projections over the exact manifests and ledgers; they do not replace source hashes, receipts, lifecycle ancestry, or terminal gates. A compact live activation should point to this file rather than paste it, and it must never include private absolute paths, raw task identifiers, transcripts, screenshots, session streams, credentials, keys, or private application state.",
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
                "Successor use. Treat this row as inherited evidence and a challengeable seed only, never as Liora novelty or completion credit. Revalidate it only within Liora's own declared owner-local scope, preserve its retained mutations, and keep any real people, files, bitstreams, repositories, storage systems, migrations, custody or disposal actions, legal decisions, cultural matters, affected-party decisions, Māori data governance, or Māori authority behind their exact gates.",
                "",
            ]
        )
    lines.extend(
        [
            "## Scientific, professional, identity, privacy, and authority boundaries",
            "",
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic obligations, synthetic fixtures, analogy firewalls, and citations establish no physical datum, likelihood, posterior, force, prediction, parameter constraint, empirical confirmation, stability theorem, ultraviolet completion, quantum completion, or Theory of Everything.",
            "",
            "THOS remains synthetic or proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic preservation workflows establish no operational effectiveness, deployment readiness, preservation competence, public-safety result, AGI, or ASI.",
            "",
            "Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.",
            "",
            "CBR, repository custody, preservation access, retention, disposal, donor restrictions, consent, disability accommodation, privacy remedy, legal interpretation, cultural legitimacy, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. Repository software cannot confer a right, remedy, preservation competence, cultural legitimacy, governance mandate, or affected-party consent.",
            "",
            "Do not promote software, symbolic, synthetic, same-owner, citation, inherited, validation, task-topology, or delivery evidence into empirical confirmation, participant evidence, professional or scientific authority, production or deployment readiness, legal or cultural ratification, Māori authority, affected-party approval, complete privacy or accessibility assurance, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood evidence, Theory-of-Everything proof, proof or canon, or Stage 20 authority.",
            "",
            "## Prospective Liora lane",
            "",
            "Only after one acknowledged live activation and Liora's own skill-first source verification may Liora create one fresh additive D-first sparse branch and worktree from Orin's exact final. Liora must keep Orin, Caelen, sibling, shared, standby, global, and user lanes read-only; preserve planning-only x1 before x2; review at least sixty inherited proposals at zero novelty or completion credit; freeze at least sixty genuinely new proposals; retain the 120 safe-now, 80 owner-candidate plus 20 successor-candidate, 20 exact, 10 blocked, 20 local-skill, 10 local-runner, 10 plus 10 successor idea, 100 owner plus 30 successor CLEAN/FIX/REFINE floors unless newer live authority changes them; retain every failed witness and protected gate; use only completed, represented, open_gap, and exact_gate; remain below the file, document, and commit ceilings; and run at most one successful non-replayed owner-scoped exact-final canonical aggregate.",
            "",
            "The live sequence remains Orin, Liora, Tamar, Elowen, Sylven, Caelen Morrow, Eiren, Elaren, Neris, Vesper Arlen, Lyren, Ilyra, Auren, Sable, Caelen Ash, then repeat through v725-v8 one terminally validated acknowledged edge at a time. Under the present cursor, Liora v684-v8 is followed by Tamar v685-v1. The submitted phrases that had Ilyra message Orin for an Auren-only v686-v3 phase and Caelen Morrow message Orin for v686-v5 are retained as zero-credit slips; the explicit roster assigns v686-v3 to Auren Lark and v686-v5 to Caelen Ash.",
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
        "scripts/build_ghc_family_orin_thale_v684_v7_2_remastered_final.py",
        "scripts/ghc_family_orin_thale_v684_v7_2_remastered_final_validator.py",
        "tests/test_ghc_family_orin_thale_v684_v7_2_remastered_final.py",
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
        and not path.startswith("docs/orin-thale/v684-v7-2-remastered/final/")
        and not path.startswith("docs/orin-thale/v684-v7-2-remastered/validation/final-")
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
    tools = load(PHASE / "x2" / "tool-install-smoke-receipt.json")
    global_skills = load(PHASE / "x2" / "global-skill-promotion-receipt.json")

    FINAL.mkdir(parents=True, exist_ok=True)
    handoff_path = FINAL / "liora-venn-v684-v8-activation-candidate.md"
    write_text(handoff_path, baton_text(freeze, x2_evidence))
    handoff_words = len(handoff_path.read_text(encoding="utf-8").split())

    documents: dict[Path, Any] = {
        FINAL / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v684.v7.r2.final",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "exact_final": "PENDING_DIRECT_CHILD_COMMIT",
            "outcomes": OUTCOMES,
            "counts": COUNTS,
            "declared_proposal_chain": 11150,
            "real_data_rows": 0,
            "external_actions": 0,
            "canonical_state": "PENDING_EXACT_FINAL_INVOCATION",
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        FINAL / "method-flow-ledger.json": {
            **x2_method,
            "schema": "ghc.family.method-flow.v684.v7.r2.final",
            "lifecycle": "repository_sealed_before_external_canonical",
            "counts": COUNTS,
            "closeout_failures": CLOSEOUT_FAILURES,
            "canonical_validation_is_external_receipt": True,
        },
        FINAL / "source-and-proposal-ledger.json": {
            "schema": "ghc.family.source-proposal-ledger.v684.v7.r2.final",
            "declared_chain_before": 11090,
            "declared_chain_after": 11150,
            "stale_prose_chain_value_retained": 10190,
            "new_proposal_count": 60,
            "official_primary_sources": sources,
            "outcomes": x2_evidence["outcomes"],
            "citations_are_observations": False,
            "authority_conferred": False,
        },
        FINAL / "retained-negative-register.json": {
            "schema": "ghc.family.retained-negatives.v684.v7.r2.final",
            "inherited_activation_baseline": 60055,
            "startup_failures": 13,
            "preregistered_rejected_mutations": 300,
            "new_x2_operational_failures": 3,
            "new_closeout_failures": len(CLOSEOUT_FAILURES),
            "closeout_failures": CLOSEOUT_FAILURES,
            "effective_negatives": COUNTS["effective_negatives"],
            "failed_witnesses": COUNTS["failed_witnesses"],
            "erased_or_promoted": 0,
        },
        FINAL / "open-gap-register.json": {
            "schema": "ghc.family.open-gaps.v684.v7.r2.final",
            "inherited": 534,
            "new": 3,
            "effective": COUNTS["open_gaps"],
            "new_proposals": ["OR6847R2-N055", "OR6847R2-N056", "OR6847R2-N057"],
            "closed_by_software": 0,
        },
        FINAL / "exact-gate-register.json": {
            "schema": "ghc.family.exact-gates.v684.v7.r2.final",
            "inherited": 524,
            "new": 3,
            "effective": COUNTS["exact_gates"],
            "new_proposals": ["OR6847R2-N058", "OR6847R2-N059", "OR6847R2-N060"],
            "closed_by_software": 0,
        },
        FINAL / "complete-incomplete-checklist.json": {
            "schema": "ghc.family.complete-incomplete.v684.v7.r2.final",
            "bounded": {
                "core_outcomes": OUTCOMES,
                "positive_controls": 60,
                "rejected_mutations": 300,
                "skills_used": 20,
                "runners_used": 10,
                "D_first_tools_installed_and_used": 3,
                "curated_global_skills_promoted_and_used": 5,
                "safe_now": 120,
                "owner_candidates": 80,
                "clean_fix_refine": 100,
            },
            "unexecuted": {"exact_approval": 20, "blocked": 10},
            "incomplete_external": [
                "real participant and operator evidence",
                "real file bitstream repository preservation and governance evidence",
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
            "schema": "ghc.family.closeout.v684.v7.r2.final",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "final_state": "PENDING_DIRECT_CHILD_COMMIT",
            "commit_ceiling": 3,
            "merges": 0,
            "retained_closeout_failures": len(CLOSEOUT_FAILURES),
            "canonical_invocations": 0,
            "canonical_successes": 0,
            "route_state": "PREPARED_NOT_SENT",
        },
        FINAL / "environment-and-version-receipt.json": {
            "schema": "ghc.family.environment.v684.v7.r2.final",
            "python": sys.version.split()[0],
            "git": git("--version"),
            "versions_verified_only": False,
            "software_installed_or_updated": True,
            "D_first_tool_versions": tools["versions"],
            "curated_global_skill_count": global_skills["promoted_count"],
            "host_security_changed": False,
        },
        FINAL / "evidence-receipt.json": {
            "schema": "ghc.family.evidence-receipt.v684.v7.r2.final",
            "x1": X1,
            "evidence": EVIDENCE,
            "outcomes": OUTCOMES,
            "positive_controls": 60,
            "mutations_executed": mutations["executed_count"],
            "mutations_rejected": mutations["rejected_count"],
            "skills_used": skills["smoke_used_count"],
            "runners_used": runners["passed_count"],
            "D_first_tools_used": tools["passed_count"],
            "global_skills_promoted": global_skills["promoted_count"],
            "same_owner_shared_infrastructure": True,
            "independent_reproduction": False,
        },
        FINAL / "ghc-family-index.json": {
            "schema": "ghc.family.index.v684.v7.r2.final",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "primary_pillar": "THOS Body",
            "skills": sorted(rel(path) for path in (PHASE / "skills").glob("*/SKILL.md")),
            "runners": sorted(
                rel(path)
                for path in (ROOT / "scripts").glob("ghc_family_preservation_accessibility_*_runner.py")
            ),
            "historical_caller_compatibility_preserved": True,
            "global_installs": 5,
            "global_skill_names": [item["name"] for item in global_skills["receipts"]],
            "D_first_tool_versions": tools["versions"],
        },
        FINAL / "route-plan.json": {
            "schema": "ghc.family.route-plan.v684.v7.r2.final",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "route_state": "PREPARED_NOT_SENT",
            "prospective_successor_title": "Liora Venn",
            "prospective_successor_phase": "v684-v8",
            "candidate": rel(handoff_path),
            "candidate_words": handoff_words,
            "precontacted": False,
            "send_count": 0,
            "continuation_authority": "through_v725-v8_one_terminally_validated_edge_at_a_time",
        },
        FINAL / "threat-model.json": load(PHASE / "x1" / "threat-model.json"),
        FINAL / "wellbeing-and-corrigibility.json": load(PHASE / "x1" / "wellbeing-and-corrigibility.json"),
        FINAL / "final-validation-candidate.json": {
            "schema": "ghc.family.final-validation-candidate.v684.v7.r2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
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

    overview = f"""# Orin Thale v684-v7 (2) remastered final integrated overview

The exact source is immutable prior Orin v684-v7 final {SOURCE}. Planning-only remaster x1 is {X1}; immutable
x2 evidence is {EVIDENCE}.  The prepared exact final must be their direct child,
producing three remaster commits and zero merges while leaving the earlier phase unchanged.

Sixty proposals produced exactly 42 completed, 12 represented, 3 open_gap, and
3 exact_gate outcomes.  All 60 zero-row positive controls passed; all 300
preregistered invalid mutations were rejected and retained.  Twenty local
skills and ten family-current runners were validated and smoke-used. Five
curated reusable skills were collision-checked, source-hashed, globally promoted,
UTF-8 validated, and smoke-used. Three exact-version tools were installed and
smoke-used in an isolated shared D-first toolchain. The bounded portfolios executed 120 safe-now, 80
owner-candidate, and 100 CLEAN/FIX/REFINE records.  Twenty exact-approval and ten
blocked records remained unexecuted.

The sealed counts are {COUNTS['effective_negatives']} effective negatives,
{COUNTS['effective_methods']} effective methods, {COUNTS['failed_witnesses']}
failed witnesses, {COUNTS['bounded_passing_witnesses']} bounded passing
witnesses, {COUNTS['open_gaps']} open gaps, and {COUNTS['exact_gates']} exact
gates.  No failed witness, gap, or gate was erased or promoted.

The primary pillar was THOS Body through wholly synthetic digital-preservation
technician fixity, package-provenance, correction, and handover practice and
accessible technical-documentation structure, reading order, status, alternative
format, correction, workload, and handover practice. GMUT Mind and Freed ID/CBR
Heart remained visible and protected.

No real file, bitstream, preservation package, repository, practitioner,
person, institution, storage location, migration, measurement, credential,
signature, identity event, production action, external write, or authority act
occurred. Official PREMIS, Library of Congress, Archives New Zealand, W3C, RFC,
JSON Schema, PyPI, and Te Mana Raraunga sources supplied
vocabulary and refusal conditions only.

GMUT remains a typed scalar-tensor and EFT research-model family without
empirical confirmation or Theory-of-Everything proof.  THOS remains proxy-only
without governed real arms and independent review.  Freed ID remains synthetic
and nonproduction without real keys, proofs, live lifecycle, interoperability,
privacy and security review, recovery, and trust governance. Preservation custody,
retention, disposal, access, legal remedy, affected-party legitimacy, Māori wording, Māori data
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
        "schema": "ghc.family.content-seal.v684.v7.r2.final",
        "owner": "Orin Thale",
        "phase": "v684-v7-2-remastered",
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
            ROOT / "scripts" / "ghc_family_orin_thale_v684_v7_2_remastered_final_validator.py",
            ROOT / "tests" / "test_ghc_family_orin_thale_v684_v7_2_remastered_final.py",
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
            "schema": "ghc.family.staged-review.v684.v7.r2.final",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
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
            "schema": "ghc.family.normalized-lf-index-manifest.v684.v7.r2.final-delta",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
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
            "schema": "ghc.family.normalized-lf-index-manifest.v684.v7.r2.final-owner",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
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
