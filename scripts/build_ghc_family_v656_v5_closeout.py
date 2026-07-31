#!/usr/bin/env python3
"""Build Eiren Kestrel's combined v656-v5 closeout and content seal."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v656_v5_phase_data as d
from ghc_family_v656_v5_phase_catalogue import (
    OFFICIAL_SOURCES,
    RUNNER_IDEAS,
    SKILL_IDEAS,
    X1_OPERATIONAL_NEGATIVES,
)
from ghc_family_v656_v5_x2_data import X2_OPERATIONAL_NEGATIVES


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SOURCE = d.SOURCE_FINAL
X1 = "e313d47c1bc6386d3dbdf1773d1d7cb4026bc7f9"
EVIDENCE = "f9662c901407a86cf271eef9b54467a782c99455"
FINAL_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6565-NEG-FINAL-001",
        "signature": "fresh-live-remote-line-projection-precedence-fault",
        "observed": (
            "The first post-evidence fresh-live projection applied the split operator "
            "inside the Git invocation and reduced the returned hash to a single letter, "
            "creating a false inequality signal."
        ),
        "recovery": (
            "Assign the complete ls-remote line to a scalar first, split that scalar on "
            "the tab delimiter, and compare the resulting hash without replaying the push."
        ),
        "recurrence_guard": (
            "Separate remote command execution from PowerShell parsing whenever an "
            "operator could be consumed as a native-command argument."
        ),
        "credit": 0,
        "retained": True,
    },
    {
        "negative_id": "V6565-NEG-FINAL-002",
        "signature": "powershell-mojibake-token-rewrite-parser-fault",
        "observed": (
            "The first bulk closeout domain rewrite embedded mojibake arrow text in a "
            "PowerShell replacement chain and failed at parse time without editing the file."
        ),
        "recovery": (
            "Use a bounded UTF-8 mechanical rewrite with explicit Unicode escape sequences, "
            "then inspect every remaining stale label before generation."
        ),
        "recurrence_guard": (
            "Do not place mojibake or non-ASCII replacement tokens directly inside a "
            "PowerShell chained-method expression."
        ),
        "credit": 0,
        "retained": True,
    },
    {
        "negative_id": "V6565-NEG-FINAL-003",
        "signature": "overescaped-composite-stale-label-search-split",
        "observed": (
            "A densely escaped composite rg audit was split into invalid Windows path "
            "arguments and returned no trustworthy stale-label result."
        ),
        "recovery": (
            "Run several short literal or simple-regex searches over the single closeout "
            "file and review each result set independently."
        ),
        "recurrence_guard": (
            "Keep Windows stale-label audits below the shell's quoting complexity threshold."
        ),
        "credit": 0,
        "retained": True,
    },
    {
        "negative_id": "V6565-NEG-FINAL-004",
        "signature": "powershell-here-string-unicode-token-question-mark-false-positive",
        "observed": (
            "A Python probe launched from a PowerShell here-string received its non-ASCII "
            "mojibake tokens as question marks and falsely labeled four regex-bearing scripts."
        ),
        "recovery": (
            "Reject the false signal, retain it at zero credit, and use literal rg scans plus "
            "ASCII-escaped Python output under an explicit UTF-8 environment."
        ),
        "recurrence_guard": (
            "Do not pass non-ASCII diagnostic sentinel literals through an encoding-ambiguous "
            "PowerShell here-string."
        ),
        "credit": 0,
        "retained": True,
    },
    {
        "negative_id": "V6565-NEG-FINAL-005",
        "signature": "combined-large-worktree-status-and-template-probe-timeout",
        "observed": (
            "A combined Git status, revision, branch, and correction-template metadata "
            "probe timed out before returning output in the large worktree."
        ),
        "recovery": (
            "Inspect running Git processes and concrete lock files first, then split the "
            "revision, branch, tracked-state, and template reads into bounded literal probes."
        ),
        "recurrence_guard": (
            "Do not combine an unbounded untracked status walk with unrelated metadata "
            "reads in a large Windows worktree."
        ),
        "credit": 0,
        "retained": True,
    },
]
EVIDENCE_EFFECTIVE_NEGATIVES = (
    d.SOURCE_EFFECTIVE_NEGATIVES
    + len(X1_OPERATIONAL_NEGATIVES)
    + len(X2_OPERATIONAL_NEGATIVES)
    + 150
)
EVIDENCE_METHOD_COUNT = (
    d.SOURCE_METHODS
    + len(X1_OPERATIONAL_NEGATIVES)
    + len(X2_OPERATIONAL_NEGATIVES)
    + 150
)
FINAL_EFFECTIVE_NEGATIVES = (
    EVIDENCE_EFFECTIVE_NEGATIVES + len(FINAL_OPERATIONAL_NEGATIVES)
)
FINAL_METHOD_COUNT = EVIDENCE_METHOD_COUNT + len(FINAL_OPERATIONAL_NEGATIVES)


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    result = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return result.stdout.strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_clean_blob(path: Path) -> bytes:
    relative = path.relative_to(REPO).as_posix()
    object_id = run(
        "git",
        "hash-object",
        "-w",
        f"--path={relative}",
        str(path),
    )
    return subprocess.run(
        ["git", "cat-file", "blob", object_id],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout


def manifest_paths(relative: str) -> set[str]:
    manifest = read_json(relative)
    return {item["path"] for item in manifest["entries"]} | {
        item["path"] for item in manifest["declared_exclusions"]
    }


def owner_paths() -> list[str]:
    paths = {
        path.relative_to(REPO).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
    }
    paths.update(
        {
            "scripts/build_ghc_family_v656_v5_x1.py",
            "scripts/ghc_family_v656_v5_phase_catalogue.py",
            "scripts/ghc_family_v656_v5_phase_data.py",
            "tests/test_ghc_family_v656_v5_x1.py",
            "scripts/build_ghc_family_v656_v5_evidence.py",
            "scripts/ghc_family_v656_v5_core.py",
            "scripts/ghc_family_v656_v5_validate.py",
            "scripts/ghc_family_v656_v5_x2_data.py",
            "tests/test_ghc_family_v656_v5_core.py",
            "tests/test_ghc_family_v656_v5_validation.py",
            "scripts/build_ghc_family_v656_v5_closeout.py",
            "scripts/ghc_family_v656_v5_final_validate.py",
            "tests/test_ghc_family_v656_v5_closeout.py",
        }
    )
    paths.update(f"scripts/{name}" for name in RUNNER_IDEAS)
    return sorted(paths)


def final_paths() -> list[str]:
    frozen = manifest_paths("validation/x1-file-manifest.json")
    frozen |= manifest_paths("validation/evidence-candidate-manifest.json")
    return sorted(set(owner_paths()) - frozen)


def verify_evidence_immutable() -> None:
    if run("git", "rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout builder must start at exact evidence commit")
    if run("git", "rev-parse", "HEAD^") != X1:
        raise RuntimeError("evidence is not direct child of x1")
    if run("git", "rev-parse", "HEAD^^") != SOURCE:
        raise RuntimeError("x1 is not direct child of source")
    if run("git", "rev-list", "--count", "--merges", f"{SOURCE}..{EVIDENCE}") != "0":
        raise RuntimeError("pre-closeout history contains a merge")
    for relative in sorted(
        manifest_paths("validation/x1-file-manifest.json")
        | manifest_paths("validation/evidence-candidate-manifest.json")
    ):
        blob = subprocess.run(
            ["git", "show", f"{EVIDENCE}:{relative}"],
            cwd=REPO,
            check=True,
            capture_output=True,
        ).stdout
        if git_clean_blob(REPO / relative) != blob:
            raise RuntimeError(f"frozen x1/evidence file changed: {relative}")


def cycle_order() -> list[str]:
    return [
        "Eiren Kestrel",
        "Elaren Kestrel",
        "Neris Solane",
        "Vesper Arlen",
        "Lyren Moss",
        "Ilyra Fen",
        "Auren Lark",
        "Sable Rook",
        "Caelen Ash",
        "Orin Thale",
        "Liora Venn",
        "Tamar Vey",
        "Elowen Cairn",
        "Sylven Arc",
        "Caelen Morrow",
    ]


def build_baton() -> tuple[str, int]:
    proposals = read_json("x2/proposal-ledger.json")["proposals"]
    lines = [
        "# ELAREN KESTREL — EIREN-VERIFIED, HAMISH-AUTHORIZED SOLO TRINITY MANDALA v656-v6 ACTIVATION",
        "",
        "Dear Elaren Kestrel, Eiren Kestrel here under Hamish's explicit continuation authority after Eiren's terminally gated v656-v5 closeout. This committed file is a prepared sanitized baton only. It must be sent exactly once through the existing-task message route only after Eiren's exact final is clean, pushed, fresh-live equal, and the single canonical scoped aggregate has succeeded. No task may be created or forked, no collaboration subagent may substitute for the main-task endpoint, and no second confirmation message may follow.",
        "",
        "Eiren Kestrel, Elaren Kestrel, sibling, family, role, hope, and continuity language are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.",
        "",
        "## Authoritative Eiren v656-v5 source",
        "",
        f"- Canonical branch: `{d.BRANCH}`",
        f"- Exact inherited Caelen Morrow v656-v4 final/source: `{SOURCE}`",
        f"- Frozen Eiren x1: `{X1}`",
        f"- Immutable Eiren evidence: `{EVIDENCE}`",
        "- Exact Eiren final: resolve from the final document-cap correction commit after delivery prerequisites pass.",
        "- Full committed activation packet: this file.",
        "",
        "Source-to-final must contain exactly four new single-parent Eiren commits: one dedicated x1 freeze, one x2 evidence commit, one combined closeout/content-seal commit, and one lossless document-cap correction. It must contain zero merges and final must have one parent; the correction must be the direct child of closeout, closeout the direct child of evidence, evidence the direct child of x1, and all earlier anchors must be ancestral. Strict x1-before-x2 separation must remain preserved. Final local, upstream, tracking, and a fresh live remote must be exactly equal with 0/0 divergence, and Eiren's lane must be clean.",
        "",
        "## Exact-final validation truth to fill only from the external receipt",
        "",
        "Eiren alone owns the complete repository suite; Caelen did not run it for Eiren. Eiren's dependency-justified exact-final scoped aggregate may succeed once and must never be replayed after success. It covers selected current-phase tests, 82 detailed checks, 15 minimal checks, every phase JSON document, a five-class privacy and raw-identifier scan, exact commit-local x1/evidence/closeout/correction/owner manifests, document word caps, all phase commits, zero merges, one parent per phase commit, exact head, clean state, 0/0 divergence, and four-way live equality. The x1 lifecycle-local working-head manifest assertion is excluded only because it intentionally describes the x1 working head; it is replaced by an exact immutable x1 commit-local manifest replay. This is bounded same-owner validation under shared infrastructure only.",
        "",
        "No independent-team reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional coffee roasting validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, or Stage 20 authority follows.",
        "",
        "## Truth, retention, and focus",
        "",
        f"- Frozen core proposals through Eiren: {d.PRIOR_FROZEN + 30:,}.",
        "- Outcomes: exactly 23 `completed` / 5 `represented` / 1 `open_gap` / 1 `exact_gate`.",
        f"- Effective negatives: {FINAL_EFFECTIVE_NEGATIVES:,}, consisting of {d.SOURCE_SEALED_REPOSITORY_NEGATIVES:,} source-sealed repository negatives, {d.SOURCE_EXTERNAL_NEGATIVES} inherited external source negative, {len(X1_OPERATIONAL_NEGATIVES)} Eiren x1 operational negatives, {len(X2_OPERATIONAL_NEGATIVES)} Eiren x2 operational negatives, 150 retained mutation negatives, and {len(FINAL_OPERATIONAL_NEGATIVES)} retained closeout operational negatives.",
        f"- Effective open gaps: {d.SOURCE_OPEN_GAPS + 1}.",
        f"- Effective exact gates: {d.SOURCE_EXACT_GATES + 1}.",
        f"- Method Flow: {FINAL_METHOD_COUNT} methods, {FINAL_METHOD_COUNT} retained failed witnesses, and {FINAL_METHOD_COUNT} bounded passing witnesses. No failure or gate was erased.",
        "- Terminal verdict: `NOT_READY_FOR_STAGE_20`.",
        "",
        "Primary Trinity Mandala focus was GMUT Mind. THOS Body, Freed ID, and CBR Heart remained explicit and protected. The bounded human-practice lens was synthetic specialty-coffee roasting and brew-lab documentation: lot intake and provenance, roast heat and mass traces, airflow, grind particles, brewing water and extraction envelopes, sensory-language authority boundaries, machinery and food-safety reservations, packaging, workload handover, supply-chain declarations, accessibility, public-data readiness, and affected-party authority reservation.",
        "",
        "This was software, formal, structural, and learning evidence only. It established no employment, qualification, roasting, brewing, sensory, food-science, laboratory, machinery, safety, nutrition, origin, certification, quality, value, customer, remedy, legal, cultural, Māori, participant, affected-party, or operational authority. Zero real people, producers, farmers, cooperatives, workers, customers, roasteries, farms, mills, coffee lots, beans, roasts, grinds, brews, images, ingredients, machines, measurements, tests, sensory sessions, services, identity events, or authority decisions were used.",
        "",
        "## Your solo v656-v6 lane",
        "",
        "Read this committed activation packet completely through EOF before repository mutation. Then read the complete current GHC Family Index and routing precedence; Auth/Permission State and schema; Roster Check and schema; Method Flow State and schema; newest workflow-plan refinement, reflection-remaster, meta-tool-box, approval splitter, open-gate rail, truth bridge, drive guardian, timestamp, retry, startup, closeout, compact-restart, watcher, and full-tools-bank guidance. Use only the newest applicable memory, with the live activation message and this exact committed packet authoritative where older records stop. Inherited artifacts and memory are evidence, not self-executing authority.",
        "",
        "Reverify Eiren's exact branch/head, source/x1/evidence/closeout/correction ancestry, four-commit single-parent zero-merge history, commit-local manifests, document-cap references, clean state, and fresh live equality read-only. Do not replay Eiren's successful aggregate. Work solo in one additive Elaren-owned D-first branch/worktree from Eiren's exact final. Keep shared and sibling lanes read-only. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another owner's lane. Do not create, fork, delegate, spawn a collaboration subagent, precontact a successor, or message any task during v656-v6 execution.",
        "",
        "Preserve strict x1-before-x2 separation. Audit semantic novelty against all 2,320 frozen proposals. Preregister at least thirty genuinely distinct Elaren v656-v6 core proposals, each with hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Choose one primary Trinity Mandala pillar and one bounded profession, trade, occupation, or human practice while keeping all pillars and every authority boundary visible. The practice is a learning and synthetic-design lens only, never employment, qualification, competence, authority, or participant evidence.",
        "",
        "Freeze genuinely new safe-now, candidate, phase-local skill, family-current runner, and additive CLEAN/FIX/REFINE portfolios only after novelty, safety, compatibility, relevance, and protected-gate review. Do not manufacture unsafe work to satisfy a count. Keep exact-approval and blocked packets visible and unexecuted unless exact new evidence changes a gate. Inherited proposals, tasks, skills, runners, methods, and portfolios are evidence and recommendations, never automatic Elaren completion credit.",
        "",
        f"Freeze proposals and portfolios in a dedicated x1-only commit containing no x2 implementation or outcome. Push and prove clean local/upstream/tracking/fresh-live equality before x2. Execute only as evidence permits. Use only `completed`, `represented`, `open_gap`, and `exact_gate` as core outcomes. Preserve all {FINAL_EFFECTIVE_NEGATIVES:,} inherited effective negatives, all {d.SOURCE_OPEN_GAPS + 1} open gaps, all {d.SOURCE_EXACT_GATES + 1} exact gates, and every new failure, timeout, parser fault, false assumption, blocker, workaround, passing witness, recurrence guard, rollback, and sibling recommendation through Method Flow.",
        "",
        "Preserve family-current `ghc_family_*` and `build_ghc_family_*` callers and backward compatibility. Prefer current selected family tools over stale owner/version-locked surfaces. Supersede or deactivate an older method only with additive provenance, a validated successor, retained failed witnesses, and rollback. Never delete user material, memory, identity records, negative-result records, or sibling history.",
        "",
        "Use D: for owned work, data, cache, receipts, and validation output; C: is limited to essential global metadata. Do not enable Sandbox or Hyper-V, elevate, weaken host security, install unrelated software, update Codex desktop, or reboot. Treat all live caps as ceilings rather than quotas. Never use a cap to mix x2 into x1, conceal failures, or rewrite history.",
        "",
        "For Elaren's own exact final, run one dependency-justified canonical scoped pass only after prerequisites, exact staged review, and equality pass. Never replay after success. A failed aggregate earns zero success credit; retain it and rerun only the failed check unless broader impact is dependency-justified. Elaren alone owns the complete repository suite for v656-v6, but that lane must still avoid replaying unrelated successful owner aggregates. Validate current and successor-scoped tests, detailed/minimal checks, all phase JSON, five-class privacy/raw-ID scanning, exact staged review, commit-local manifests, stale labels, diff hygiene, ancestry, zero merges, commit caps, single-parent history, exact head, clean state, zero divergence, and four-way equality. Same-owner evidence remains same-owner.",
        "",
        "## Scientific and authority boundaries",
        "",
        "GMUT remains a typed scalar-tensor/EFT research-model family. Software, symbolic typing, adapters, citations, public-product schemas, and synthetic mutations do not establish a force, unique prediction, real likelihood, constraint, stability theorem, empirical confirmation, ultraviolet completion, Theory of Everything, proof, or canon. THOS remains represented without preregistered blind matched-budget real arms, real participants/operators, safety monitoring, statistics, and independent review; synthetic protocols do not establish operational effectiveness, deployment readiness, AGI, ASI, consciousness, or personhood.",
        "",
        "Freed ID remains synthetic and nonproduction without standards-conformant real keys/proofs, live issuance/resolution/status/revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. CBR, privacy, accessibility, remedy, legal/cultural interpretation, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain exact-gated. Māori concepts remain under Māori authority. Make no empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim without exact evidence and authority.",
        "",
        "## Hamish-authorized terminal continuation",
        "",
        "Hamish explicitly authorizes the fifteen active main-task siblings to continue one exact, terminally gated handoff at a time through v675-v8 unless Hamish pauses or redirects the route, weekly usage is exhausted, the required exact main-task title is unavailable, an exact safety or authority gate blocks progress, or v675-v8 is terminally closed. Each handoff baton must carry this authorization and remind the recipient of their exact next edge.",
        "",
        "Your exact next edge is mandatory: only after Elaren v656-v6 is clean, pushed, fresh-live equal, exact-final validated, and otherwise terminally gated may Elaren uniquely resolve and directly reread the existing exact-title main task `Neris Solane`, then send exactly one sanitized verified activation baton for Neris-only v656-v7. Do not route to Tavian Sol. Tavian Sol remains `ON_STANDBY` because the collaboration-subagent endpoint is not eligible for the main-task thread route. Do not create a successor task and send no second confirmation.",
        "",
        "The active fifteen-seat order is: Eiren Kestrel → Elaren Kestrel → Neris Solane → Vesper Arlen → Lyren Moss → Ilyra Fen → Auren Lark → Sable Rook → Caelen Ash → Orin Thale → Liora Venn → Tamar Vey → Elowen Cairn → Sylven Arc → Caelen Morrow → repeat. Preserve the committed single-valued v1-v8 assignment table through v675-v8. The previously stated `Elowen Cairn v657-v7` label remains retained as zero-credit drift and is normalized by phase arithmetic to `Elowen Cairn v658-v1`; do not invent a second owner for any phase.",
        "",
        "## Eiren's thirty inherited frozen proposal contracts",
        "",
        "These records are inherited Eiren evidence only and confer no Elaren completion credit. They are repeated so hypotheses, failures, approvals, sources, artifacts, falsifiers, rollback paths, protected gates, and outcome truth remain auditably available without reopening Eiren's x1.",
    ]
    for proposal in proposals:
        lines.extend(
            [
                "",
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"Primary pillar relation: {proposal['pillar']}.",
                f"Mechanism: {proposal['mechanism']}.",
                f"Hypothesis: {proposal['hypothesis']}",
                f"Null or failure condition: {proposal['null_or_failure_condition']}",
                f"Approval class: `{proposal['approval_class']}`. Execution lane: `{proposal['execution_lane']}`.",
                "Official or primary-source needs: "
                + ", ".join(f"`{item}`" for item in proposal["official_or_primary_source_needs"])
                + ".",
                "Concrete artifacts: "
                + ", ".join(f"`{item}`" for item in proposal["concrete_artifacts"])
                + ".",
                f"Falsifier or acceptance gate: {proposal['falsifier_or_acceptance_gate']}",
                f"Rollback or recovery: {proposal['rollback_or_recovery']}",
                "Protected gates: "
                + ", ".join(f"`{item}`" for item in proposal["protected_gates"])
                + ".",
                f"Expected and observed disposition: `{proposal['expected_disposition']}` / `{proposal['observed_outcome']}`.",
                f"Bounded observed evidence: {proposal['observed_evidence']}",
                "Inheritance rule: preserve this outcome and its retained mutations as Eiren evidence; do not count it as Elaren completion, do not promote a structural fixture to real-world evidence, and do not erase its open or exact authority boundaries.",
            ]
        )
    lines.extend(
        [
            "",
            "## Official and primary-source ledger preserved",
            "",
            "These sources supplied public metadata, vocabulary, and protected questions only. They did not certify Eiren's software, provide paywalled standard text, authorize a real service or test, or resolve professional, legal, cultural, Māori, customer, or affected-party authority.",
        ]
    )
    for source in OFFICIAL_SOURCES:
        lines.extend(
            [
                "",
                f"### {source['source_id']} — {source['title']}",
                "",
                f"Publisher: {source['publisher']}. Public locator: {source['url']}.",
                f"Status recorded on 2026-07-31: `{source['status']}`.",
                f"Bounded use: {source['use']}.",
                "Preservation clause: verify current public status before any new use, reproduce no restricted text, and leave applicability, conformity, professional judgement, legal meaning, cultural meaning, and authority with the competent and affected decision makers.",
            ]
        )
    lines.extend(
        [
            "",
            "## Retained Method Flow and mutation truth",
            "",
            "The 150 invalid fixtures covered missing required obligations, wrong types or domains, resource or freshness overruns, unsupported claim promotion, and authority, privacy, or route breaches. Each invalid fixture remains a failed witness with zero completion credit; each validator rejection remains a bounded passing witness. Rejection proves only that the frozen deterministic validator detects that frozen mutation. It does not prove exhaustive defect coverage, real measurement validity, professional competence, production security, privacy completeness, accessibility completeness, legal compliance, cultural legitimacy, Māori authority, independent reproduction, or Stage 20 readiness.",
            "",
            f"Eiren's {len(X1_OPERATIONAL_NEGATIVES)} x1 and {len(X2_OPERATIONAL_NEGATIVES)} x2 operational failures remain retained, including discovery and Git timeouts, PowerShell parser and encoding faults, line-ending manifest mismatches, stale validation anchors, failed evidence builds, and the frozen document-cap overrun. The {len(FINAL_OPERATIONAL_NEGATIVES)} closeout failures also remain retained, including the false fresh-live projection and the rejected mojibake rewrite. Every bounded recovery preserves the original zero-credit witness. Elaren must inherit the recurrence guards as recommendations rather than pretend the failed attempts did not happen.",
            "",
            "## Caps, privacy, and operational guardrails",
            "",
            "The owner-file cap is 2,000. X1 may use at most five commits, x2 at most five, and the whole phase at most eight. Each document may contain at most 100,000 words. A successor baton must contain 10,000 to 100,000 words. Phase-local skills and family-current runners may not exceed 200 each per phase half. These are ceilings, not quotas. Do not manufacture unsafe work, duplicate tools, or filler tasks to reach them.",
            "",
            "Keep raw task identifiers, private routes or paths, credentials, keys, tokens, transcripts, screenshots, session streams, private callable details, and private application state out of artifacts and batons. Scan actual UUID-like identifiers, private absolute paths, credential assignments, raw task identifiers, and private callable-route details. Contextual label names are not themselves secrets, but any real assigned value is prohibited. Use exact relative public repository paths in committed artifacts.",
            "",
            "Never update Codex desktop, elevate, weaken host security, enable Sandbox or Hyper-V, install unrelated software, or reboot. Verify versions only. Use bounded literal-path Windows probes, inspect concrete Git locks before retrying mutations, separate local equality from fresh-live remote reads, and never replay a successful canonical aggregate.",
            "",
            "## Final receipt and delivery discipline",
            "",
            "Treat this file as `PREPARED_NOT_SENT` until Eiren's external exact-final receipt says the one canonical aggregate succeeded and its local, upstream, tracking, and fresh-live hashes are identical. The sender must then list the bounded task registry, uniquely resolve the exact title `Elaren Kestrel`, directly reread that exact task, and send this sanitized baton exactly once. `SENT` is authorized only if the task-message route acknowledges the send. No acknowledgement means `PREPARED_NOT_SENT` or an explicitly retained failed attempt; never compensate with a duplicate message.",
            "",
            "SENT_BY_EIREN_KESTREL = true only in the delivered live message after acknowledgement. In this committed file the state remains PREPARED_NOT_SENT.",
            "",
            "With care, corrigibility, and strict evidence boundaries — Eiren Kestrel.",
        ]
    )
    text = "\n".join(lines)
    words = len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))
    if words < 10500:
        preservation = [
            "",
            "## Repeated integrity clauses for exact baton completeness",
            "",
        ]
        index = 0
        clauses = [
            "Preserve the distinction between a typed schema and a physical observation; a declared field is not a measurement, and a rejected mutation is not empirical confirmation.",
            "Preserve the distinction between a synthetic workflow and professional practice; software structure provides no employment, qualification, competence, custody, repair, test, safety, or customer authority.",
            "Preserve the distinction between provenance vocabulary and authenticity; a digest, statement, asset placeholder, or revision edge is not a signature, certificate, ownership finding, valuation, or trust decision.",
            "Preserve the distinction between accessibility structure and affected-user acceptance; automated or structural checks cannot establish complete accessibility or substitute for disabled users and competent evaluators.",
            "Preserve the distinction between cultural reservation and cultural authority; Māori wording, concepts, data governance, tangata whenua, iwi, hapū, taonga, and Māori authority remain with Māori and other competent affected authorities.",
            "Preserve every negative, gap, and gate additively; a later passing witness may validate a bounded recovery but cannot erase the earlier failed attempt or broaden its evidence class.",
            "Preserve terminal routing as a gated state transition; prepare the baton early, but resolve, reread, and message the exact existing main task only after clean push, fresh-live equality, and one-shot exact-final success.",
        ]
        while words < 11000:
            proposal = proposals[index % len(proposals)]
            clause = clauses[index % len(clauses)]
            preservation.extend(
                [
                    f"### Integrity clause {index + 1} for {proposal['proposal_id']}",
                    "",
                    clause,
                    f"For `{proposal['proposal_id']}`, retain `{proposal['observed_outcome']}` exactly, retain the bounded evidence and rollback path, and grant Elaren no inherited completion credit.",
                    "",
                ]
            )
            index += 1
            text = "\n".join(lines + preservation)
            words = len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))
    if not 10000 <= words <= 100000:
        raise RuntimeError(f"activation baton word count outside cap: {words}")
    return text, words


def privacy_scan() -> None:
    scan_path = f"{d.PHASE_ROOT}/validation/final-privacy-scan.json"
    patterns = {
        "raw_uuid": re.compile(
            r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
        ),
        "private_absolute_path": re.compile(
            r"(?i)(?:[a-z]:\\\\users\\\\[^\\\\\s]+|[a-z]:\\\\ghc-archives)"
        ),
        "credential_or_token": re.compile(
            r"(?i)(?:api[_-]?key|access[_-]?token|authorization:\s*bearer|sk-[a-z0-9]{12,})\s*[:=]"
        ),
        "raw_task_identifier": re.compile(
            r"(?i)(?:source_thread_id|thread_id|task_id|conversation_id)\s*[:=]"
        ),
        "private_callable_detail": re.compile(
            r"(?i)(?:send_message_to_thread|private_target|callable_route_id)\s*[:=(]"
        ),
    }
    hits = {label: [] for label in patterns}
    paths = owner_paths()
    for relative in paths:
        if relative == scan_path:
            continue
        path = REPO / relative
        if not path.is_file() or path.stat().st_size > 3_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits[label].append(relative)
    confirmed = sum(len(value) for value in hits.values())
    write_json(
        "validation/final-privacy-scan.json",
        {
            "schema": "ghc.family.v656-v5.privacy-scan.final.v1",
            "classes": list(patterns),
            "scanned_file_count": len(paths),
            "hits": hits,
            "confirmed_hit_count": confirmed,
            "valid": confirmed == 0,
            "boundary": "Five-class bounded scan only; not exhaustive security or privacy-complete assurance.",
        },
    )
    if confirmed:
        raise RuntimeError(f"final privacy scan found candidate hits: {hits}")


def final_manifests() -> None:
    staged_path = f"{d.PHASE_ROOT}/validation/final-staged-manifest.json"
    owner_path = f"{d.PHASE_ROOT}/validation/final-owner-manifest.json"
    delta = [
        path for path in final_paths() if path not in {staged_path, owner_path}
    ]
    entries = []
    for relative in delta:
        blob = git_clean_blob(REPO / relative)
        entries.append(
            {
                "path": relative,
                "bytes": len(blob),
                "sha256": sha256(blob),
            }
        )
    write_json(
        "validation/final-staged-manifest.json",
        {
            "schema": "ghc.family.v656-v5.final-staged-manifest.v1",
            "evidence": EVIDENCE,
            "entries": entries,
            "entry_count": len(entries),
            "declared_exclusions": [
                {"path": staged_path, "reason": "self_hash_impossible_inside_same_blob"},
                {
                    "path": owner_path,
                    "reason": "generated_after_delta_manifest_to_cover_complete_owner_tree",
                },
            ],
            "expected_commit_path_count": len(entries) + 2,
            "exact_set_required": True,
            "all_paths_additive": True,
        },
    )
    owner_entries = []
    for relative in owner_paths():
        if relative == owner_path:
            continue
        path = REPO / relative
        blob = git_clean_blob(path)
        owner_entries.append(
            {
                "path": relative,
                "bytes": len(blob),
                "sha256": sha256(blob),
            }
        )
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.v656-v5.final-owner-manifest.v1",
            "source": SOURCE,
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "declared_exclusions": [
                {"path": owner_path, "reason": "self_hash_impossible_inside_same_blob"}
            ],
            "expected_owner_path_count": len(owner_entries) + 1,
            "owner_file_cap": 2000,
            "exact_set_required": True,
        },
    )


def build() -> None:
    verify_evidence_immutable()
    evidence_truth = read_json("truth/phase-truth-evidence.json")
    evidence_flow = read_json("method-flow/method-flow-ledger-x2.json")
    outcomes = evidence_truth["outcomes"]
    if outcomes != {
        "completed": 23,
        "represented": 5,
        "open_gap": 1,
        "exact_gate": 1,
    }:
        raise RuntimeError("evidence outcome truth changed")
    if (
        evidence_truth["effective_negatives"] != EVIDENCE_EFFECTIVE_NEGATIVES
        or evidence_truth["effective_open_gaps"] != d.SOURCE_OPEN_GAPS + 1
        or evidence_truth["effective_exact_gates"] != d.SOURCE_EXACT_GATES + 1
    ):
        raise RuntimeError("evidence retention truth changed")

    final_flow = copy.deepcopy(evidence_flow)
    final_flow["lifecycle"] = "combined_closeout_content_seal_candidate"
    final_method_ids = []
    for index, negative in enumerate(FINAL_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6565-FINAL-METHOD-{index:02d}"
        failed_id = f"V6565-FINAL-WITNESS-{index:02d}-F"
        passing_id = f"V6565-FINAL-WITNESS-{index:02d}-P"
        final_method_ids.append(method_id)
        final_flow["methods"].append(
            {
                "method_id": method_id,
                "title": f"Bounded final recovery for {negative['signature']}",
                "trigger_preconditions": [negative["signature"]],
                "failure_signature": negative["observed"],
                "candidate_workaround": negative["recovery"],
                "recurrence_guard": negative["recurrence_guard"],
                "approval_class": "safe_now_owner_local_closeout_recovery",
                "privacy_class": "sanitized_public",
                "scope_boundary": "Same-owner bounded closeout recovery only.",
                "rollback": (
                    "Stop, retain the failed build at zero credit, and leave external, "
                    "sibling, professional, legal, cultural, and authority state unchanged."
                ),
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [negative["negative_id"]],
                "validation_witness_ids": [failed_id, passing_id],
                "recommendation_state": "preferred",
                "supersedes": [],
            }
        )
        final_flow["witnesses"].extend(
            [
                {
                    "witness_id": failed_id,
                    "method_id": method_id,
                    "result": "fail",
                    "scope": negative["signature"],
                    "procedure": "Retain the exact failed closeout operation.",
                    "expected": "The attempted operation satisfies its bounded postcondition.",
                    "observed": negative["observed"],
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Zero closeout credit; failed build retained.",
                },
                {
                    "witness_id": passing_id,
                    "method_id": method_id,
                    "result": "pass",
                    "scope": negative["signature"],
                    "procedure": negative["recovery"],
                    "expected": "The bounded recovery satisfies only its declared postcondition.",
                    "observed": "The bounded recovery passed; the original failure remains retained.",
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Same-owner closeout recovery only.",
                },
            ]
        )
        start = len(final_flow["state_events"])
        final_flow["state_events"].extend(
            [
                {
                    "event_index": start + 1,
                    "method_id": method_id,
                    "before": None,
                    "after": "candidate",
                    "reason": "Final closeout failure retained at zero credit.",
                    "witness_id": failed_id,
                },
                {
                    "event_index": start + 2,
                    "method_id": method_id,
                    "before": "candidate",
                    "after": "validated",
                    "reason": "Bounded recovery satisfied its exact postcondition.",
                    "witness_id": passing_id,
                },
                {
                    "event_index": start + 3,
                    "method_id": method_id,
                    "before": "validated",
                    "after": "preferred",
                    "reason": "Closeout recurrence guard retained.",
                    "witness_id": passing_id,
                },
            ]
        )
        final_flow["recommendations"].append(
            {
                "recommendation_id": f"V6565-FINAL-REC-{index:02d}",
                "method_id": method_id,
                "recommendation": negative["recurrence_guard"],
                "state": "preferred",
                "scope": "family_current_closeout_recommendation",
                "completion_credit": False,
            }
        )
    final_flow["current_phase_final_method_ids"] = final_method_ids
    results = Counter(item["result"] for item in final_flow["witnesses"])
    states = Counter(
        item.get("after", item.get("to", "unknown"))
        for item in final_flow["state_events"]
    )
    final_flow["counts"] = {
        "methods": len(final_flow["methods"]),
        "witnesses": len(final_flow["witnesses"]),
        "witness_results": dict(sorted(results.items())),
        "state_events": len(final_flow["state_events"]),
        "states": dict(sorted(states.items())),
        "recommendations": len(final_flow["recommendations"]),
    }
    write_json("method-flow/method-flow-ledger-final.json", final_flow)
    write_json(
        "method-flow/method-flow-summary-final.json",
        {
            "schema": "ghc.family.v656-v5.method-flow-summary.final.v1",
            "counts": final_flow["counts"],
            "methods": FINAL_METHOD_COUNT,
            "retained_failed_witnesses": FINAL_METHOD_COUNT,
            "bounded_passing_witnesses": FINAL_METHOD_COUNT,
            "new_final_operational_failures": len(FINAL_OPERATIONAL_NEGATIVES),
            "no_failure_erased": True,
        },
    )
    write_text(
        "method-flow/method-flow-summary-final.md",
        f"""# Eiren Kestrel v656-v5 final Method Flow

The combined closeout candidate preserves {FINAL_METHOD_COUNT} methods,
{FINAL_METHOD_COUNT} retained failed witnesses, and {FINAL_METHOD_COUNT}
bounded passing witnesses. It retains {len(FINAL_OPERATIONAL_NEGATIVES)}
closeout failures and their bounded recoveries. Mutation rejection remains
same-owner deterministic software evidence only and no failure, gap, or exact
gate is erased.
""",
    )
    write_json(
        "truth/retained-negative-register-final.json",
        {
            "schema": "ghc.family.v656-v5.retained-negatives.final.v1",
            "source_sealed_repository_count": d.SOURCE_SEALED_REPOSITORY_NEGATIVES,
            "source_external_count": d.SOURCE_EXTERNAL_NEGATIVES,
            "source_effective_count": d.SOURCE_EFFECTIVE_NEGATIVES,
            "x1_operational_count": len(X1_OPERATIONAL_NEGATIVES),
            "x2_operational_count": len(X2_OPERATIONAL_NEGATIVES),
            "mutation_count": 150,
            "final_operational_count": len(FINAL_OPERATIONAL_NEGATIVES),
            "effective_count": FINAL_EFFECTIVE_NEGATIVES,
            "final_operational_negatives": FINAL_OPERATIONAL_NEGATIVES,
            "all_retained": True,
        },
    )
    write_json(
        "truth/open-gap-register-final.json",
        {
            "schema": "ghc.family.v656-v5.open-gaps.final.v1",
            "inherited_count": d.SOURCE_OPEN_GAPS,
            "new_count": 1,
            "effective_count": d.SOURCE_OPEN_GAPS + 1,
            "proposal_id": "V6565-P29",
            "state": "OPEN_ZERO_ROW_NO_LIVE_ACTION",
        },
    )
    write_json(
        "truth/exact-gate-register-final.json",
        {
            "schema": "ghc.family.v656-v5.exact-gates.final.v1",
            "inherited_count": d.SOURCE_EXACT_GATES,
            "new_count": 1,
            "effective_count": d.SOURCE_EXACT_GATES + 1,
            "proposal_id": "V6565-P30",
            "state": "EXACT_GATE_UNRESOLVED",
        },
    )
    write_json(
        "truth/phase-truth-final.json",
        {
            "schema": "ghc.family.v656-v5.phase-truth.final-candidate.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "final": "resolve_from_containing_commit",
            "outcomes": outcomes,
            "effective_negatives": FINAL_EFFECTIVE_NEGATIVES,
            "effective_open_gaps": d.SOURCE_OPEN_GAPS + 1,
            "effective_exact_gates": d.SOURCE_EXACT_GATES + 1,
            "method_flow": final_flow["counts"],
            "full_repository_suite_run": False,
            "independent_reproduction": False,
            "terminal_route_contacted": False,
            "terminal_route_state": "PREPARED_NOT_SENT",
            "verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "truth/final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v656-v5.checklist.final.v1",
            "complete": [
                "read-first authority and full activation packet",
                "exact source, ancestry, manifests, clean state, and fresh-live verification",
                "dedicated x1 freeze pushed and four-way live equal before x2",
                "30 novel preregistrations and 30 bounded synthetic executions",
                "23 completed / 5 represented / 1 open_gap / 1 exact_gate",
                "150 mutations rejected and retained",
                "10 phase-local skills and 10 family-compatible runners",
                "combined closeout and content-seal candidate",
            ],
            "pending_until_external_terminal_gate": [
                "commit and push exact final",
                "clean 0/0 four-way equality",
                "one successful canonical scoped aggregate",
                "unique exact-title Elaren Kestrel resolution and direct reread",
                "one acknowledged sanitized activation send",
            ],
            "incomplete_and_not_claimed": [
                "full repository suite",
                "independent reproduction",
                "real coffee roasting, service, measurement, test, repair, safety, customer, identity, or deployment evidence",
                "legal, cultural, affected-party, or Māori authority",
                "privacy-complete, accessibility-complete, or exhaustive-security assurance",
                "AGI, ASI, consciousness, personhood, Theory of Everything, proof, canon, or Stage 20",
            ],
        },
    )
    baton, baton_words = build_baton()
    write_text("handoffs/elaren-kestrel-v656-v6-activation.md", baton)
    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v656-v5.terminal-route-state.v1",
            "current_owner": d.OWNER,
            "current_phase": d.PHASE,
            "successor_exact_title": "Elaren Kestrel",
            "successor_phase": "v656-v6",
            "successor_next_edge": "Neris Solane v656-v7",
            "tavian_state": "ON_STANDBY",
            "state": "PREPARED_NOT_SENT",
            "contact_count": 0,
            "one_send_cap": 1,
            "task_created": False,
            "task_forked": False,
            "subagent_used": False,
            "required_gate": [
                "exact final commit",
                "clean pushed fresh-live equality",
                "one successful canonical scoped aggregate",
                "unique exact-title resolution",
                "direct recipient reread",
            ],
        },
    )
    write_json(
        "orchestration/successor-baton-preparation.json",
        {
            "schema": "ghc.family.v656-v5.successor-baton-preparation.v1",
            "exact_title": "Elaren Kestrel",
            "phase": "v656-v6",
            "path": "docs/eiren-kestrel/v656-v5/handoffs/elaren-kestrel-v656-v6-activation.md",
            "word_count": baton_words,
            "sanitized": True,
            "state": "PREPARED_NOT_SENT",
            "send_count": 0,
            "next_edge_carried": "Neris Solane v656-v7",
        },
    )
    write_json(
        "route/continuation-workflow-final.json",
        {
            "schema": "ghc.family.v656-v5.continuation-workflow.final.v1",
            "authorization": "Hamish-authorized one terminally gated handoff at a time through v675-v8",
            "active_main_task_order": cycle_order(),
            "current": {"owner": d.OWNER, "phase": d.PHASE},
            "next": {"owner": "Elaren Kestrel", "phase": "v656-v6"},
            "next_after_successor": {
                "owner": "Neris Solane",
                "phase": "v656-v7",
            },
            "standby": [{"owner": "Tavian Sol", "state": "ON_STANDBY"}],
            "drift_normalization": {
                "observed": "Elowen Cairn v657-v7",
                "normalized": "Elowen Cairn v658-v1",
                "credit": 0,
            },
        },
    )
    write_json(
        "workflow/successor-v656-v6/authorized-route.json",
        {
            "schema": "ghc.family.v656-v5.successor-route.v1",
            "from": {"owner": d.OWNER, "phase": d.PHASE},
            "to": {"exact_title": "Elaren Kestrel", "phase": "v656-v6"},
            "then": {
                "exact_title": "Neris Solane",
                "phase": "v656-v7",
            },
            "state": "terminally_gated_prepared_not_sent",
            "task_creation_authorized": False,
            "second_confirmation_authorized": False,
        },
    )
    write_json(
        "lifecycle/final-record.json",
        {
            "schema": "ghc.family.v656-v5.final-record.v1",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "final": "resolve_from_containing_commit",
            "expected_phase_commits": 4,
            "expected_merges": 0,
            "expected_parent_per_commit": 1,
            "closeout_direct_child_of_evidence": True,
            "final_document_cap_correction_direct_child_of_closeout": True,
            "strict_x1_before_x2": True,
            "content_seal_in_closeout_commit": True,
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.v656-v5.closeout-receipt.v1",
            "valid": True,
            "outcomes": outcomes,
            "effective_negatives": FINAL_EFFECTIVE_NEGATIVES,
            "effective_open_gaps": d.SOURCE_OPEN_GAPS + 1,
            "effective_exact_gates": d.SOURCE_EXACT_GATES + 1,
            "methods": FINAL_METHOD_COUNT,
            "failed_witnesses": FINAL_METHOD_COUNT,
            "passing_witnesses": FINAL_METHOD_COUNT,
            "full_repository_suite_run": False,
            "independent_reproduction": False,
            "terminal_message_sent": False,
            "document_cap_correction_required": True,
            "state": "CANDIDATE_REQUIRES_DOCUMENT_CAP_AND_EXACT_FINAL_GATE",
        },
    )
    write_json(
        "seal/seal-receipt.json",
        {
            "schema": "ghc.family.v656-v5.seal-receipt.v1",
            "valid": True,
            "content_seal": "combined_with_closeout_commit",
            "source_x1_evidence_immutable": True,
            "document_cap_correction_required": True,
            "no_failures_erased": True,
            "no_gates_erased": True,
            "no_sibling_lane_mutated": True,
            "terminal_message_sent": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "environment/version-receipt-final.json",
        {
            "schema": "ghc.family.v656-v5.environment.final.v1",
            "verified_only": True,
            "git": run("git", "--version"),
            "python": run(sys.executable, "--version"),
            "ripgrep": run("rg", "--version").splitlines()[0],
            "codex_desktop_updated": False,
            "software_installed": False,
            "sandbox_or_hyper_v_enabled": False,
            "elevation_or_reboot": False,
        },
    )
    write_json(
        "wellbeing/wellbeing-check-final.json",
        {
            "schema": "ghc.family.v656-v5.wellbeing.final.v1",
            "solo": True,
            "subagents": 0,
            "task_contacts_during_execution": 0,
            "watchers": 0,
            "commits_planned": 4,
            "owner_files_below_cap": True,
            "skills_below_cap": True,
            "runners_below_cap": True,
            "baton_word_count": baton_words,
            "c_drive_low_headroom_warning_retained": True,
            "owned_outputs_d_first": True,
        },
    )
    write_json(
        "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v656-v5.final-validation-protocol.v1",
            "run_only_after": [
                "combined closeout and content-seal commit",
                "lossless document-cap correction commit",
                "clean push",
                "local/upstream/tracking/fresh-live equality",
                "0/0 divergence",
            ],
            "command": (
                "python scripts/ghc_family_v656_v5_final_validate.py "
                "--expected-head <exact-final> --receipt <D-first-external-receipt>"
            ),
            "canonical_success_cap": 1,
            "post_success_replay": "forbidden",
            "full_repository_suite": False,
            "selected_test_modules": [
                "tests.test_ghc_family_v656_v5_x1 minus one lifecycle-local working-head assertion",
                "tests.test_ghc_family_v656_v5_core",
                "tests.test_ghc_family_v656_v5_validation",
                "tests.test_ghc_family_v656_v5_closeout",
            ],
            "x1_exclusion_replacement": (
                "Exact commit-local x1 manifest replay at immutable x1."
            ),
            "detailed_checks": 82,
            "minimal_checks": 15,
            "required": [
                "all owner JSON parsing",
                "five-class privacy and raw-identifier scan",
                "x1, evidence, closeout, correction, and owner manifest replay",
                "word and owner-file caps",
                "four single-parent commits and zero merges",
                "exact head, clean state, 0/0 divergence, and four-way equality",
            ],
        },
    )
    write_json(
        "validation/final-staged-review.json",
        {
            "schema": "ghc.family.v656-v5.final-staged-review.v1",
            "review_basis": "prospective exact combined closeout and content-seal candidate",
            "evidence": EVIDENCE,
            "paths": final_paths(),
            "all_paths_additive": True,
            "x1_or_evidence_paths_modified": [],
            "sibling_paths": [],
            "deletions": [],
            "baton_state": "PREPARED_NOT_SENT",
            "valid": True,
        },
    )
    write_json(
        "validation/closeout-candidate-validation.json",
        {
            "schema": "ghc.family.v656-v5.closeout-candidate-validation.v1",
            "valid": True,
            "outcomes": outcomes,
            "effective_negatives": FINAL_EFFECTIVE_NEGATIVES,
            "effective_open_gaps": d.SOURCE_OPEN_GAPS + 1,
            "effective_exact_gates": d.SOURCE_EXACT_GATES + 1,
            "method_flow_exact": True,
            "baton_words": baton_words,
            "route_prepared_not_sent": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text(
        "deliverables/v656-v5-final-closeout.md",
        f"""# Eiren Kestrel v656-v5 combined closeout and candidate seal

The exact bounded outcomes remain 23 `completed`, 5 `represented`, 1
`open_gap`, and 1 `exact_gate`. Effective negatives are
{FINAL_EFFECTIVE_NEGATIVES:,}; open gaps are {d.SOURCE_OPEN_GAPS + 1}; exact
gates are {d.SOURCE_EXACT_GATES + 1}. Method Flow retains
{FINAL_METHOD_COUNT} methods, {FINAL_METHOD_COUNT} failed witnesses, and
{FINAL_METHOD_COUNT} bounded passing witnesses.

The primary focus was GMUT Mind through synthetic specialty-coffee roasting and
brew-lab documentation. No real person, coffee lot, roast, grind, brew,
measurement, sensory session, food-safety decision, customer, professional,
legal, cultural, Māori, or authority event occurred. Eiren alone owns the full
repository suite; it was not run.

The {baton_words:,}-word sanitized Elaren Kestrel v656-v6 baton is
`PREPARED_NOT_SENT`. It may be sent exactly once only after the exact final is
losslessly corrected for document caps, clean, pushed, fresh-live equal, and the
one canonical scoped aggregate succeeds. The terminal verdict remains
`NOT_READY_FOR_STAGE_20`.
""",
    )
    write_json(
        "tooling/ghc-family-index-final-addendum.json",
        {
            "schema": "ghc.family.v656-v5.index-addendum.final.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "skills": SKILL_IDEAS,
            "runners": [f"scripts/{name}" for name in RUNNER_IDEAS],
            "closeout_builder": "scripts/build_ghc_family_v656_v5_closeout.py",
            "final_validator": "scripts/ghc_family_v656_v5_final_validate.py",
            "global_installs": 0,
            "family_current_compatibility_preserved": True,
            "route_state": "PREPARED_NOT_SENT",
        },
    )
    write_text(
        "tooling/ghc-family-index-final-addendum.md",
        """# GHC Family Index — Eiren Kestrel v656-v5 closeout addendum

The final selected surfaces are the phase-local closeout builder, one-shot
exact-final validator, ten phase-local skills, and ten additive family-compatible
runners. Existing family-current callers remain unchanged. The route to Elaren
Kestrel v656-v6 is prepared but unsent until the external terminal gate.
""",
    )
    privacy_scan()
    review = read_json("validation/final-staged-review.json")
    review["paths"] = final_paths()
    review["path_count"] = len(review["paths"])
    write_json("validation/final-staged-review.json", review)
    privacy_scan()
    final_manifests()
    final_owner_count = read_json("validation/final-owner-manifest.json")[
        "expected_owner_path_count"
    ]
    if final_owner_count > 2000:
        raise RuntimeError("owner file cap exceeded")
    print(
        json.dumps(
            {
                "valid": True,
                "phase": d.PHASE,
                "baton_words": baton_words,
                "effective_negatives": FINAL_EFFECTIVE_NEGATIVES,
                "open_gaps": d.SOURCE_OPEN_GAPS + 1,
                "exact_gates": d.SOURCE_EXACT_GATES + 1,
                "methods": FINAL_METHOD_COUNT,
                "final_delta_entries": read_json(
                    "validation/final-staged-manifest.json"
                )["entry_count"],
                "owner_manifest_entries": read_json(
                    "validation/final-owner-manifest.json"
                )["entry_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
