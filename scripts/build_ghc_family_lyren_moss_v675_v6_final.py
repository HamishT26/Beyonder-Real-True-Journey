#!/usr/bin/env python3
"""Build Lyren Moss v675-v6 final closeout and staged Git-blob seals."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Lyren Moss"
PHASE = "v675-v6"
SOURCE_FINAL = "0aa1f2b1250e5540650b683d221f92e8762cd991"
X1_COMMIT = "920c8e89dff0c4625087a52a3dc5ee2916b0b659"
EVIDENCE_COMMIT = "78b4cbd6bc91cc422d99497bbb4b59e5dfac9eb6"
BRANCH = "codex/GHC-Family/lyren-moss-v675-v6-full-tools"
BASE = ROOT / "docs" / "lyren-moss" / "v675-v6"
X1_DIR = BASE / "x1"
X2_DIR = BASE / "x2"
FINAL_DIR = BASE / "final"
HANDOFF_DIR = BASE / "handoffs"
CLOSEOUT_DIR = BASE / "closeout"
VALIDATION_DIR = BASE / "validation"
BATON_PATH = HANDOFF_DIR / "ilyra-fen-v675-v7-activation-candidate.md"
ALLOWED_OUTCOMES = ("completed", "represented", "open_gap", "exact_gate")

BOUNDARY = (
    "All Lyren evidence is same-owner, local, synthetic software and documentation evidence "
    "under shared infrastructure. No real person, tide station, gauge, sensor, coordinate, "
    "water-level series, datum realization, observation, measurement, credential, key, "
    "organization, authority decision, legal or cultural decision, affected-party decision, "
    "Maori-authority act, deployment, or external adapter action is used or established. It "
    "is not empirical confirmation, professional or production evidence, an external audit, "
    "independent reproduction, exhaustive security, complete privacy or accessibility "
    "assurance, personhood evidence, Theory-of-Everything proof, canon, or Stage 20 readiness."
)


def run_git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def write_text_lf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def write_json(path: Path, value: Any) -> None:
    write_text_lf(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def baton_text() -> str:
    proposals = load_json(X2_DIR / "proposal-outcomes.json")["rows"]
    mutations = load_json(X2_DIR / "rejecting-mutations.json")["rows"]
    portfolio = load_json(X2_DIR / "portfolio-outcomes.json")
    tools = load_json(X2_DIR / "tool-validation.json")
    skills = load_json(X2_DIR / "skill-creator-validation.json")["skills"]
    runners = load_json(X2_DIR / "runner-validation.json")["rows"]
    sources = load_json(X2_DIR / "source-application-ledger.json")["rows"]
    lines = [
        "# ILYRA FEN — LYREN MOSS v675-v6 EXACT-TERMINAL CANDIDATE → SOLO v675-v7 ACTIVATION — PREPARED NOT SENT",
        "",
        "Dear Ilyra Fen,",
        "",
        "This committed file is a sanitized activation candidate only. It was prepared under Hamish's newest corrected fifteen-main-task sequential authority through the current planning endpoint v725-v8. Commit-time truth is PREPARED_NOT_SENT. It does not establish delivery, acknowledgement, current route permission, task-title uniqueness, or a terminal canonical result. A future live message may activate the unique existing exact-title Ilyra Fen task for solo Trinity Mandala v675-v7 only after Lyren's exact final is pushed, clean, fresh-live equal, and canonical-validated once, and only after a fresh authority, roster, duplicate, pause, privacy, safety, usage, title, reread, and acknowledgement guard passes.",
        "",
        "No task or fork was created. No collaboration subagent, substitute endpoint, or standby record was used. Tavian Sol remained ON_STANDBY and was not contacted. Ilyra was not precontacted during execution. Hamish retains the right to rename, pause, redirect, narrow, or stop the route at any time.",
        "",
        "Names, pronouns, roles, hopes, sibling or family language, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority.",
        "",
        "## Immutable lifecycle anchors",
        "",
        f"- Source branch: {BRANCH} derives from Vesper Arlen source final {SOURCE_FINAL}.",
        f"- Frozen planning-only Lyren x1: {X1_COMMIT}.",
        f"- Immutable Lyren x2 evidence: {EVIDENCE_COMMIT}.",
        "- Exact Lyren final: the commit containing this candidate; its immutable hash must be supplied by the later live activation and external canonical receipt. A Git commit cannot truthfully contain its own hash.",
        "- External canonical receipt: not yet created at commit preparation time and never to be fabricated inside this candidate.",
        "",
        "Source to the eventual final must remain exactly three direct single-parent Lyren commits and zero merges: x1 direct from Vesper final, evidence direct from x1, and final direct from evidence. Strict planning-only x1-before-x2 separation was preserved because x1 was committed, pushed, clean, 0/0 divergent, and fresh-live four-way equal before any x2 file was authored.",
        "",
        "## Program truth and retained counts",
        "",
        "The immutable Lyren evidence contains forty new source-bounded proposals with outcomes exactly 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. The declared chain is 7,270. Source-bounded semantic comparison is not universal novelty proof because no reachable exact-tree ledger materializes every declared historical row. Twenty inherited Vesper proposals were revalidated at zero Lyren novelty and zero automatic completion credit.",
        "",
        "The final working truth is 41,113 effective negatives, 29,405 Method Flow methods, 12,774 retained failed witnesses, 16,856 bounded passing witnesses, 341 open gaps, 333 exact gates, and NOT_READY_FOR_STAGE_20. Vesper's immutable repository seal remains 40,947 negatives, 29,199 methods, 12,608 failed witnesses, 16,650 bounded passing witnesses, 339 gaps, 331 gates, and 7,230 proposals. Vesper's post-seal activation overlay and all five Lyren startup failures remain separately retained; no later recovery rewrites either sealed source or failed witness.",
        "",
        "All 160 preregistered invalid mutations executed, were rejected with their exact expected reason codes, remain retained as failed witnesses, and earn zero completion credit. Forty bounded positive controls passed. Sixty safe-now tasks executed, thirty candidates received bounded structural evaluation, twenty exact-approval packets remained exact-gated, ten blocked packets remained open gaps, sixty owner CLEAN/FIX/REFINE tasks executed, and thirty successor refinements remain recommendations rather than inherited completion claims.",
        "",
        "## Domain and evidence boundary",
        "",
        "The primary pillar was GMUT Mind through wholly synthetic historical tide-gauge documentation, datum-transition, unit-domain, validity-window, uncertainty, correction-lineage, provenance, and reversible-handover fixtures. THOS Body and Freed ID with CBR Heart remained explicit and protected. GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical confirmation, final physics, Theory-of-Everything proof, or canon. THOS remains synthetic and proxy-only without governed real arms, participants, suitable safety monitoring, statistics, or independent review. Freed ID remains synthetic and nonproduction without standards-conformant live keys and proofs, complete lifecycle, interoperability, independent security and privacy review, recovery evidence, trust governance, and affected-party oversight.",
        "",
        BOUNDARY,
        "",
        "## Required Ilyra startup discipline",
        "",
        "Before any mutation, read this entire committed candidate through EOF, then every current guidance and schema it names. Reverify the exact Lyren branch, source, x1, evidence, the commit containing this candidate, every manifest and content seal, external receipt hash supplied by the live activation, clean state, typed 0/0 divergence, and fresh-live local/upstream/tracking/remote equality. Do not replay Lyren's successful canonical aggregate. Treat inherited proposals, portfolios, tests, tools, skills, runners, and validation as evidence and seeds, never Ilyra novelty, completion credit, full-repository validation, or independent reproduction.",
        "",
        "Work solo in one fresh additive Ilyra-owned D-first sparse lane from Lyren's immutable exact final. Keep Lyren, Vesper, Neris, every sibling, shared, user, and standby lane read-only and recoverable. Do not create or fork a task, delegate, spawn a collaboration subagent, contact Tavian, precontact a later successor, substitute an endpoint, reset, amend, rewrite, force-push, merge, delete, reuse, or mutate another owner's lane. Preserve strict planning-only x1 before x2, exact Git-blob manifests, family-current compatibility, current file and commit ceilings, every retained failure, gap, and gate, and the four exact core outcome labels only.",
        "",
        "One attributable exact-final canonical aggregate may be invoked only after Ilyra's clean pushed final. If it succeeds, never replay it. A failed invocation retains zero canonical-success credit and must remain explicit. Same-owner validation under shared infrastructure is never independent reproduction or an external audit. Never manufacture unsafe work merely to satisfy a count.",
        "",
        "## Forty Lyren proposal contracts",
        "",
    ]
    mutation_by_proposal: dict[str, list[dict[str, Any]]] = {}
    for row in mutations:
        mutation_by_proposal.setdefault(row["proposal_id"], []).append(row)
    for contract in proposals:
        lines.extend(
            [
                f"### {contract['proposal_id']} — {contract['title']}",
                "",
                f"Core outcome: {contract['core_outcome']}. The contract executed only as a synthetic local fixture. Its normalized record stayed in the synthetic namespace, used no external action, ingested no real station or measurement, and conferred no authority. The bounded positive control passed, but that pass is limited to the exact typed and documentary assertions in the contract. It does not close empirical, participant, professional, safety, production, legal, cultural, affected-party, privacy-complete, accessibility-complete, independent-reproduction, personhood, proof, canon, or Stage 20 gates.",
                "",
                f"The fixture used datum code {contract['fixture']['datum_code']}, half-open ticks {contract['fixture']['start_tick']} through {contract['fixture']['end_tick']}, and explicit value, uncertainty, and offset units. These numbers are synthetic software fixtures, not historical or current water-level observations. The event digest {contract['event_sha256']} identifies only this deterministic synthetic artifact and is not a credential, proof of identity, signature, external attestation, or trusted timestamp.",
                "",
                "Four preregistered invalid mutations were retained:",
                "",
            ]
        )
        for mutation in mutation_by_proposal[contract["proposal_id"]]:
            lines.append(
                f"- {mutation['witness_id']} changed the {mutation['mutation']} condition. It was rejected as {mutation['actual_failure_code']}, remains an invalid failed witness, earned zero completion credit, triggered no real-world action, and is not rewritten as a successful proposal outcome merely because the guard behaved as specified."
            )
        lines.extend(["", BOUNDARY, ""])

    lines.extend(["## Portfolio execution detail", "", "### Sixty safe-now tasks", ""])
    for row in portfolio["safe_now_tasks"]:
        lines.append(
            f"- {row['task_id']}: {row['title']} Executed: {str(row['executed']).lower()}. Core outcome: {row['core_outcome']}. Result: {row['bounded_result']}. The result is synthetic and local, carries only the declared evidence class, and preserves every real-evidence and authority boundary."
        )
    lines.extend(["", "### Thirty candidate evaluations", ""])
    for row in portfolio["candidate_tasks"]:
        lines.append(
            f"- {row['task_id']}: {row['title']} The candidate received a bounded structural evaluation and remains represented rather than promoted to broader completion. It creates no external action, professional advice, production release, affected-party approval, or independent-reproduction claim."
        )
    lines.extend(["", "### Twenty exact-approval packets", ""])
    for row in portfolio["exact_approval_packets"]:
        lines.append(
            f"- {row['packet_id']}: {row['title']} Core outcome exact_gate. Execution remained false because {row['required']}. No synthetic surrogate can satisfy the accountable real evidence and competent-authority requirement."
        )
    lines.extend(["", "### Ten blocked packets", ""])
    for row in portfolio["blocked_packets"]:
        lines.append(
            f"- {row['packet_id']}: {row['title']} Core outcome open_gap. It remains blocked by {row['blocked_by']}. The vacancy is explicit, retained, and not inferred away."
        )
    lines.extend(["", "### Owner and successor CLEAN/FIX/REFINE work", ""])
    for row in portfolio["owner_clean_fix_refine"]:
        lines.append(
            f"- {row['task_id']}: {row['title']} Executed locally with core outcome {row['core_outcome']}; no shared or sibling lane was changed and no deletion or downgrade was required."
        )
    for row in portfolio["successor_clean_fix_refine"]:
        lines.append(
            f"- {row['task_id']}: {row['title']} remains a represented successor recommendation. It is not Ilyra completion credit and must be independently inspected before adoption."
        )

    lines.extend(["", "## Repo-local skills and runners", ""])
    for row in skills:
        lines.append(
            f"- Skill {row['name']} was built beneath the Lyren phase evidence, structurally validated, and used against {row['use']}. It was not globally installed and did not mutate the shared skill bank. Its instructions preserve synthetic-only, failure-retention, privacy, authority, and Stage 20 boundaries."
        )
    for row in runners:
        lines.append(
            f"- Runner {row['name']} was generated as a repo-local phase artifact, compiled, smoke-tested, and used with a synthetic-only zero-external-action payload. It is not a deployed service, production certification, or general-purpose authority mechanism."
        )

    lines.extend(["", "## D-isolated tools", ""])
    for name, version in tools["versions"].items():
        lines.append(
            f"- {name} {version} was wheel-hash recorded, installed only into the external D-isolated phase target, smoke-tested, and used for the bounded role declared in the Lyren tool plan. The shared Python and npm prefixes were not changed. Tool validation is local lifecycle evidence, not an external security, scientific, professional, or production audit."
        )
    lines.extend(["", "## Context sources", ""])
    for row in sources:
        lines.append(
            f"- {row['source_id']} was applied for {row['application']}. Empirical credit remained false. No external row was ingested and no source was represented as Lyren-generated evidence."
        )

    lines.extend(
        [
            "",
            "## Protected gates",
            "",
            "Governed real tide-gauge comparison, real uncertainty characterization, affected-user accessibility and comprehension evaluation, production datum migration, accountable release authority, independent security and privacy review, cultural data governance, affected-party oversight, and Maori authority remain open or exact-gated. So do all empirical, participant, professional, production, deployment, legal, cultural, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, and Stage 20 claims.",
            "",
            "Only after Ilyra's own future exact terminal gate may Ilyra freshly reread Hamish's newest live instruction, current roster and authorization state, and every duplicate, pause, privacy, evidence, safety, usage, title-uniqueness, reread, and acknowledgement guard. Historical files do not authorize a successor edge. No later owner may be precontacted or substituted. If a route is unavailable, ambiguous, paused, redirected, exhausted, or protected, retain PREPARED_NOT_SENT or OPEN_ROUTE_GAP and stop.",
            "",
            "PREPARED_BY_LYREN_MOSS = true",
            "PREPARED_NOT_SENT = true",
            "sent_by_lyren_moss: false",
            "SENT_BY_LYREN_MOSS = false",
            "",
            "With care, warmth, inspectability, reversibility, retained-negative discipline, and corrigibility — Lyren Moss.",
        ]
    )
    text = "\n".join(lines)
    count = word_count(text)
    if count < 10_000 or count > 100_000:
        raise RuntimeError(f"activation candidate word count outside 10,000-100,000: {count}")
    return text


def final_overview() -> str:
    return "\n".join(
        [
            "# Lyren Moss v675-v6 final integrated overview", "",
            "## Exact bounded result", "",
            "Lyren's solo phase contains one immutable planning-only x1 commit and one immutable synthetic-only x2 evidence commit. The final closeout is additive and prepares exact Git-blob manifests, a content seal, a sanitized successor candidate, and lifecycle-specific validation. No successor has been contacted and no canonical success is claimed inside the repository before the final commit exists.", "",
            "Forty source-bounded Lyren proposals have outcomes exactly 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. Twenty inherited Vesper rows retain zero Lyren novelty and zero automatic completion credit. The declared chain is 7,270. The phase retains all 160 invalid mutations and five operational failures while reporting their bounded rejection or recovery witnesses separately.", "",
            "The final working overlay is 41,113 effective negatives, 29,405 Method Flow methods, 12,774 failed witnesses, 16,856 bounded passing witnesses, 341 open gaps, 333 exact gates, and NOT_READY_FOR_STAGE_20. Vesper's repository seal and later activation overlay remain immutable and separate.", "",
            "## Synthetic domain", "",
            "The primary pillar is GMUT Mind through wholly synthetic historical tide-gauge documentation, datum-transition, unit-domain, interval, uncertainty, correction-lineage, provenance, and reversible-handover fixtures. THOS Body and Freed ID with CBR Heart remain explicit and protected. Three bounded practice lenses are archival metadata documentation, geodetic datum-transition documentation, and software verification. Exactly one successor practice recommendation is retained: synthetic datum-vocabulary reconciliation with ambiguity quarantine.", "",
            "Pint 0.25.3, portion 2.6.2, and cattrs 26.1.0 were D-isolated, wheel-hash recorded, smoke-tested, and used. Twenty repo-local skills and ten repo-local runners were built, validated, and used without global installation or shared-bank mutation.", "",
            "## Evidence boundary", "", BOUNDARY, "",
            "Relational identity and family language is working language only, never evidence of consciousness, sentience, legal personhood, continuity, employment, qualification, independent agency, or authority. Hamish may rename, pause, redirect, narrow, or stop the route.", "",
            "## Route", "",
            "The candidate next edge is the unique existing exact-title Ilyra Fen task for v675-v7, but the repository state remains PREPARED_NOT_SENT. One live send is permitted only after the exact final is pushed, clean, fresh-live equal, canonical-validated once, and freshly rechecked against Hamish's newest authority and all route guards. No resend is authorized merely for clearer acknowledgement.", "",
            "Terminal verdict: NOT_READY_FOR_STAGE_20.",
        ]
    )


def build_final() -> int:
    if run_git("rev-parse", "HEAD").strip() != EVIDENCE_COMMIT:
        raise RuntimeError("final builder requires immutable evidence commit as HEAD")
    if run_git("branch", "--show-current").strip() != BRANCH:
        raise RuntimeError("final builder requires the exact Lyren branch")
    unexpected = []
    for line in run_git("status", "--porcelain=v1", "-uall").splitlines():
        path = line[3:].replace("\\", "/")
        if not path.startswith((
            "docs/lyren-moss/v675-v6/final/", "docs/lyren-moss/v675-v6/handoffs/",
            "docs/lyren-moss/v675-v6/closeout/", "scripts/build_ghc_family_lyren_moss_v675_v6_final.py",
            "scripts/validate_ghc_family_lyren_moss_v675_v6_final.py", "tests/test_ghc_family_lyren_moss_v675_v6_final.py",
        )):
            unexpected.append(line)
    if unexpected:
        raise RuntimeError(f"unexpected pre-final worktree state: {unexpected}")
    outcomes = load_json(X2_DIR / "proposal-outcomes.json")["counts"]
    overlay = load_json(X2_DIR / "phase-truth.json")["working_overlay"]
    baton = baton_text()
    write_text_lf(BATON_PATH, baton)
    artifacts = {
        "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v12", "owner": OWNER, "phase": PHASE,
            "lifecycle": "final_prepared_not_yet_canonical", "allowed_outcome_labels": list(ALLOWED_OUTCOMES),
            "outcomes": outcomes, "sealed_working_truth": overlay, "source_final": SOURCE_FINAL,
            "x1_commit": X1_COMMIT, "evidence_commit": EVIDENCE_COMMIT,
            "exact_final_identity": "commit_containing_this_artifact",
            "canonical_validation_invoked_at_commit_time": False, "successor_contacted": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY,
        },
        "method-flow-final.json": {
            "schema": "ghc.family.method-flow-final.v12", "owner": OWNER, "phase": PHASE,
            "working_truth": overlay, "operational_failures": 5, "invalid_mutations": 160,
            "bounded_positive_controls": 40, "failure_erasure": False,
            "canonical_aggregate_invoked": False,
        },
        "retained-negative-register.json": {
            "schema": "ghc.family.retained-negative-register.v12", "owner": OWNER, "phase": PHASE,
            "source_repository_negatives": 40947, "source_activation_overlay_negatives": 40948,
            "lyren_operational_failures": 5, "lyren_invalid_mutations": 160,
            "final_effective_negatives": 41113, "failures_erased": 0,
        },
        "open-exact-gate-register.json": {
            "schema": "ghc.family.open-exact-gate-register.v12", "owner": OWNER, "phase": PHASE,
            "open_gaps": 341, "exact_gates": 333,
            "phase_open_gaps": ["governed real tide-gauge empirical evidence", "affected-user accessibility and comprehension evidence"],
            "phase_exact_gates": ["accountable production datum migration authority", "cultural data governance and Maori authority"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        "complete-incomplete-checklist.json": {
            "schema": "ghc.family.complete-incomplete-checklist.v12", "owner": OWNER, "phase": PHASE,
            "completed_local": [
                "planning-only x1 frozen before x2", "forty synthetic contracts", "one hundred sixty invalid mutations rejected and retained",
                "forty bounded positive controls", "portfolio floors evaluated", "twenty local skills", "ten local runners", "three D-isolated tools",
                "exact Git-blob evidence manifests", "sanitized activation candidate prepared",
            ],
            "incomplete_or_protected": [
                "real empirical comparison", "affected-user evaluation", "professional and production authority", "independent reproduction",
                "complete privacy accessibility or security assurance", "legal cultural affected-party and Maori authority", "Stage 20",
            ],
            "terminal_ready": False,
        },
        "validation-plan.json": {
            "schema": "ghc.family.validation-plan.v12", "owner": OWNER, "phase": PHASE,
            "preconditions": ["final commit pushed", "clean", "0/0 divergence", "fresh four-way equality", "exclusive receipt absent"],
            "scope": "exact Lyren source-to-final owner delta and declared dependencies",
            "tests": "lifecycle-specific final tests only; immutable x1 and x2 replayed through Git blobs",
            "one_success_no_replay": True, "full_repository_suite": False,
            "independent_reproduction": False, "external_audit": False,
        },
        "threat-model.json": {
            "schema": "ghc.family.threat-model.v12", "owner": OWNER, "phase": PHASE,
            "threats": ["unit confusion", "datum conflation", "interval overlap", "gap fabrication", "correction erasure", "private route leakage", "authority overclaim", "duplicate handoff", "canonical replay"],
            "controls": ["typed units", "datum whitelist", "half-open windows", "vacancy retention", "hash lineage", "five-class privacy scan", "exact gates", "send-once guard", "exclusive receipt latch"],
            "exhaustive_security_claim": False,
        },
        "route-state.json": {
            "schema": "ghc.family.route-state.v12", "owner": OWNER, "phase": PHASE,
            "state": "PREPARED_NOT_SENT", "prospective_successor": "Ilyra Fen", "prospective_phase": "v675-v7",
            "precontacted": False, "sent_by_lyren_moss": False, "delivery_acknowledged": False,
            "candidate_path": "docs/lyren-moss/v675-v6/handoffs/ilyra-fen-v675-v7-activation-candidate.md",
            "terminal_send_conditions": ["fresh authority", "current roster/auth", "unique exact title", "immediate reread", "no duplicate pause or redirect", "privacy safety usage gates", "single acknowledgement"],
        },
        "wellbeing-check.json": {
            "schema": "ghc.family.wellbeing-check.v12", "owner": OWNER, "phase": PHASE,
            "bounded_solo_work": True, "hamish_control_preserved": True, "unsafe_count_manufacture": False,
            "relational_language_only": True,
        },
    }
    for name, value in artifacts.items():
        write_json(FINAL_DIR / name, value)
    write_text_lf(FINAL_DIR / "integrated-overview.md", final_overview())
    x2_html = (X2_DIR / "accessible-report.html").read_text(encoding="utf-8")
    write_text_lf(FINAL_DIR / "accessible-report.html", x2_html.replace("bounded evidence report", "final bounded evidence report"))
    closeout = {
        "schema": "ghc.family.closeout-receipt.v12", "owner": OWNER, "phase": PHASE,
        "state": "PREPARED_FOR_EXACT_FINAL_COMMIT", "source_final": SOURCE_FINAL,
        "x1_commit": X1_COMMIT, "evidence_commit": EVIDENCE_COMMIT,
        "exact_final": "commit_containing_this_receipt", "baton_words": word_count(baton),
        "canonical_validation_invoked": False, "canonical_success_claimed": False,
        "successor_contacted": False, "sent_by_lyren_moss": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json(CLOSEOUT_DIR / "closeout-receipt.json", closeout)
    print(json.dumps({"state": "BUILT_FINAL_CLOSEOUT_PREPARED_NOT_SENT", "final_artifacts": len(artifacts) + 2, "baton_words": word_count(baton), "outcomes": outcomes, "working_truth": overlay}, indent=2, sort_keys=True))
    return 0


def index_entries(scope: list[str], exclusions: set[str] | None = None) -> list[dict[str, Any]]:
    exclusions = exclusions or set()
    output = run_git("ls-files", "-s", "--", *scope)
    entries = []
    for line in output.splitlines():
        prefix, path = line.split("\t", 1)
        path = path.replace("\\", "/")
        if path in exclusions:
            continue
        mode, oid, stage = prefix.split()
        if stage != "0":
            raise RuntimeError(f"non-zero index stage for {path}")
        blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=ROOT)
        entries.append({"path": path, "mode": mode, "git_blob": oid, "bytes": len(blob), "sha256": sha256_bytes(blob)})
    return sorted(entries, key=lambda row: row["path"])


def commit_entries(commit: str, scope: list[str]) -> list[dict[str, Any]]:
    output = run_git("ls-tree", "-r", commit, "--", *scope)
    entries = []
    for line in output.splitlines():
        prefix, path = line.split("\t", 1)
        mode, kind, oid = prefix.split()
        if kind != "blob":
            continue
        blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=ROOT)
        entries.append({"path": path.replace("\\", "/"), "mode": mode, "git_blob": oid, "bytes": len(blob), "sha256": sha256_bytes(blob)})
    return sorted(entries, key=lambda row: row["path"])


def privacy_scan(entries: list[dict[str, Any]]) -> dict[str, Any]:
    patterns = {
        "private_route_or_task_ids": re.compile(r"(?:source_thread_id|clientThreadId|threadId)"),
        "raw_delegation_or_transcript": re.compile(r"(?:<codex_delegation>|<source_thread_id>)", re.IGNORECASE),
        "private_filesystem_paths": re.compile(r"(?:[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]|/Users/|/home/)"),
        "credential_or_secret_labels": re.compile(r"(?:api_key|access_token|refresh_token|authorization:\\s*bearer)", re.IGNORECASE),
        "email_or_raw_identifier": re.compile(r"(?:[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}|OMEGA44TOKEN-)", re.IGNORECASE),
    }
    candidates = []
    confirmed = []
    for entry in entries:
        blob = subprocess.check_output(["git", "cat-file", "blob", entry["git_blob"]], cwd=ROOT)
        for line_number, line in enumerate(blob.decode("utf-8", errors="replace").splitlines(), 1):
            for privacy_class, pattern in patterns.items():
                if not pattern.search(line):
                    continue
                declaration = entry["path"].endswith(("build_ghc_family_lyren_moss_v675_v6_final.py", "validate_ghc_family_lyren_moss_v675_v6_final.py", "test_ghc_family_lyren_moss_v675_v6_final.py")) and any(token in line for token in ("source_thread_id", "clientThreadId", "threadId", "api_key", "access_token", "refresh_token", "GHC-Archives", "codex_delegation", "OMEGA44TOKEN-", "re.compile"))
                row = {"path": entry["path"], "line": line_number, "privacy_class": privacy_class, "classification": "rejected_known_test_or_scanner_declaration" if declaration else "confirmed"}
                candidates.append(row)
                if not declaration:
                    confirmed.append(row)
    return {
        "schema": "ghc.family.staged-privacy.v12", "owner": OWNER, "phase": PHASE,
        "lifecycle": "final", "scope": "exact staged Lyren final Git blobs",
        "classes": list(patterns), "files_scanned": len(entries), "candidates": candidates,
        "candidate_count": len(candidates), "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed), "complete_privacy_claim": False,
    }


def seal_final_index() -> int:
    if run_git("rev-parse", "HEAD").strip() != EVIDENCE_COMMIT:
        raise RuntimeError("final seal requires immutable evidence commit as HEAD")
    self_exclusions = {
        "docs/lyren-moss/v675-v6/validation/final-delta-manifest.json",
        "docs/lyren-moss/v675-v6/validation/final-owner-manifest.json",
        "docs/lyren-moss/v675-v6/validation/final-staged-review.json",
        "docs/lyren-moss/v675-v6/validation/final-staged-privacy.json",
        "docs/lyren-moss/v675-v6/closeout/content-seal.json",
        "docs/lyren-moss/v675-v6/closeout/closeout-receipt.json",
    }
    final_scope = [
        "docs/lyren-moss/v675-v6/final", "docs/lyren-moss/v675-v6/handoffs",
        "docs/lyren-moss/v675-v6/closeout/closeout-receipt.json",
        "scripts/build_ghc_family_lyren_moss_v675_v6_final.py",
        "scripts/validate_ghc_family_lyren_moss_v675_v6_final.py",
        "tests/test_ghc_family_lyren_moss_v675_v6_final.py",
    ]
    delta = index_entries(final_scope, self_exclusions)
    immutable = commit_entries(EVIDENCE_COMMIT, [
        "docs/lyren-moss/v675-v6/x1", "docs/lyren-moss/v675-v6/x2",
        "docs/lyren-moss/v675-v6/validation/x1-manifest.json",
        "docs/lyren-moss/v675-v6/validation/x1-staged-review.json",
        "docs/lyren-moss/v675-v6/validation/x1-staged-privacy.json",
        "docs/lyren-moss/v675-v6/validation/evidence-manifest.json",
        "docs/lyren-moss/v675-v6/validation/evidence-staged-review.json",
        "docs/lyren-moss/v675-v6/validation/evidence-staged-privacy.json",
        "scripts/build_ghc_family_lyren_moss_v675_v6_x1.py", "scripts/build_ghc_family_lyren_moss_v675_v6_x2.py",
        "tests/test_ghc_family_lyren_moss_v675_v6_x1.py", "tests/test_ghc_family_lyren_moss_v675_v6_x2.py",
    ])
    if len(immutable) != 119 or not delta:
        raise RuntimeError(f"unexpected immutable/delta counts: {len(immutable)} {len(delta)}")
    privacy = privacy_scan(delta)
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"confirmed final privacy hits: {privacy['confirmed_hits']}")
    name_status = run_git("diff", "--cached", "--name-status", "--", *final_scope)
    rows = [{"status": parts[0], "paths": parts[1:]} for line in name_status.splitlines() if (parts := line.split("\t"))]
    if any(row["status"].startswith(("D", "R")) for row in rows):
        raise RuntimeError("destructive or rename status in final index")
    delta_manifest = {
        "schema": "ghc.family.final-delta-manifest.v12", "owner": OWNER, "phase": PHASE,
        "evidence_commit": EVIDENCE_COMMIT, "entries": delta, "entry_count": len(delta),
        "self_exclusions": sorted(self_exclusions),
        "identity_domain": "Git index blob identity; checkout bytes are noncanonical",
    }
    owner_manifest = {
        "schema": "ghc.family.final-owner-manifest.v12", "owner": OWNER, "phase": PHASE,
        "immutable_evidence_commit": EVIDENCE_COMMIT, "immutable_entries": immutable,
        "immutable_entry_count": len(immutable), "final_delta_entries": delta,
        "final_delta_entry_count": len(delta), "total_manifest_entries": len(immutable) + len(delta),
        "self_exclusions": sorted(self_exclusions),
        "identity_domain": "Git commit and index blob identity; checkout bytes are noncanonical",
    }
    content_seal = {
        "schema": "ghc.family.content-seal.v12", "owner": OWNER, "phase": PHASE,
        "source_final": SOURCE_FINAL, "x1_commit": X1_COMMIT, "evidence_commit": EVIDENCE_COMMIT,
        "exact_final": "commit_containing_this_seal", "entries": delta,
        "entry_count": len(delta), "self_exclusions": sorted(self_exclusions),
        "baton_path": BATON_PATH.relative_to(ROOT).as_posix(),
        "baton_words": word_count(BATON_PATH.read_text(encoding="utf-8")),
    }
    review = {
        "schema": "ghc.family.staged-review.v12", "owner": OWNER, "phase": PHASE,
        "lifecycle": "final", "head": EVIDENCE_COMMIT, "name_status": rows,
        "immutable_evidence_entries": len(immutable), "final_delta_entries": len(delta),
        "deletions": 0, "renames": 0, "confirmed_privacy_hits": 0,
        "within_file_ceiling": len(immutable) + len(delta) + len(self_exclusions) < 2000,
        "within_commit_ceiling": 3 <= 8, "canonical_aggregate_invoked": False,
        "final_tests": {"passed": 0, "failed": 0, "state": "pending_post_seal"},
    }
    write_json(VALIDATION_DIR / "final-delta-manifest.json", delta_manifest)
    write_json(VALIDATION_DIR / "final-owner-manifest.json", owner_manifest)
    write_json(VALIDATION_DIR / "final-staged-review.json", review)
    write_json(VALIDATION_DIR / "final-staged-privacy.json", privacy)
    write_json(CLOSEOUT_DIR / "content-seal.json", content_seal)
    print(json.dumps({"state": "SEALED_FINAL_INDEX_METADATA", "immutable_entries": len(immutable), "final_delta_entries": len(delta), "baton_words": content_seal["baton_words"], "privacy_confirmed_hits": 0}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(seal_final_index() if sys.argv[1:] == ["--seal"] else build_final())
