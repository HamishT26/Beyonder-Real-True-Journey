"""Build and stage Eiren Kestrel v671-v4 terminal closeout artifacts."""

from __future__ import annotations

import argparse
import ast
import hashlib
import html
import json
import re
import subprocess
import textwrap
from pathlib import Path
from typing import Any

OWNER = "Eiren Kestrel"
PHASE = "v671-v4"
BRANCH = "codex/GHC-Family/eiren-kestrel-v671-v4-full-tools"
SOURCE = "37ac80c499d43a90c874876402b262a220a252a1"
X1 = "1c4d262b14cb8528fb9d72aad40a5e4fb7423b26"
EVIDENCE = "000c4c75ccac98794b43a0171f2d330436e6069d"
ROOT_REL = Path("docs/eiren-kestrel/v671-v4")
BOUNDARY = (
    "Software, symbolic, synthetic, same-owner, citation, inherited, or composite "
    "evidence is not empirical confirmation, participant evidence, professional or "
    "scientific authority, production readiness, legal or cultural ratification, "
    "Maori authority, affected-party approval, complete privacy or accessibility "
    "assurance, exhaustive security, independent reproduction, AGI or ASI evidence, "
    "consciousness or personhood evidence, Theory-of-Everything proof, proof or "
    "canon, or Stage 20 authority."
)
CORE_LABELS = ("completed", "represented", "open_gap", "exact_gate")
FAILED_EVIDENCE_JUNIT = "e99c7c98818222cd551a1e529dd4abaa4fa4813acf27fe67ed1127f49de68fb1"
RECOVERY_COVERAGE = "27f66a8968c0635fce45c0434b3f4d1754fafa480151a38ec47a505293f1d3b0"
RECOVERY_JUNIT = "b5eeb7364508ca094c63652850b77be6d13a8276c6b017c2824d287d106286c1"
FINALIZATION_JUNIT = "9a9ed6f3987cde113e777e250a57661da5e162a4abb64f35d513e450f8e9e127"
FINAL_OPERATIONAL_FAILURES = [
    {
        "method_id": "EK6714-FINAL-OP-001",
        "class": "final_operational_failure",
        "failure_signature": "first-closeout-static-scan-found-six-bounded-ruff-findings",
        "failed_witness": "The first closeout static scan found three import-order findings, one unused import, and two startswith tuple simplifications; syntax compilation passed, but the Ruff scan receives zero credit.",
        "completion_credit": 0,
        "retained": True,
        "bounded_passing_witness": "Apply bounded mechanical import and unused-import fixes, combine only the two reported startswith predicates, inspect the diff, and rerun Ruff only on the three changed closeout files.",
        "recurrence_guard": "Run the bounded closeout static scan before generating seal artifacts and retain every finding before recovery.",
    },
    {
        "method_id": "EK6714-FINAL-OP-002",
        "class": "final_operational_failure",
        "failure_signature": "first-multi-file-final-count-patch-assumed-an-inexact-line-break",
        "failed_witness": "The first additive closeout-count patch assumed that one baton sentence broke before the outcome line; apply_patch rejected the entire patch without changing a byte.",
        "completion_credit": 0,
        "retained": True,
        "bounded_passing_witness": "Retain the rejected patch, inspect exact bounded line ranges, and apply smaller exact-context hunks before generating closeout artifacts.",
        "recurrence_guard": "Inspect generated f-string line boundaries before composing multi-file exact-context patches.",
    },
    {
        "method_id": "EK6714-FINAL-OP-003",
        "class": "final_operational_failure",
        "failure_signature": "first-closeout-build-assumed-source-ledger-rows-instead-of-sources",
        "failed_witness": "The first closeout build wrote only provisional uncommitted owner files before stopping with KeyError because it projected the x1 source ledger through a rows key rather than its exact sources key.",
        "completion_credit": 0,
        "retained": True,
        "bounded_passing_witness": "Retain the stopped build, inspect the exact source-ledger keys, use the declared sources array, and permit only the builder's own provisional final-scope paths during the deterministic rebuild.",
        "recurrence_guard": "Inspect one exact frozen source-ledger object before projecting a family-current schema into closeout artifacts.",
    },
]


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_json(path: Path, payload: Any) -> None:
    write_text(path, json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(repo: Path, command: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        command,
        cwd=repo,
        check=False,
        capture_output=True,
    )


def git(repo: Path, *args: str) -> str:
    result = run(repo, ["git", *args])
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout.decode("utf-8", errors="strict").strip()


def sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def normalize(blob: bytes) -> bytes:
    return blob.replace(b"\r\n", b"\n")


def staged_paths(repo: Path) -> list[str]:
    return sorted(
        path
        for path in git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()
        if path
    )


def staged_blob(repo: Path, path: str) -> bytes:
    result = run(repo, ["git", "show", f":{path}"])
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def head_blob(repo: Path, path: str) -> bytes:
    result = run(repo, ["git", "show", f"HEAD:{path}"])
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


SCAN_PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        re.IGNORECASE,
    ),
    "private_absolute_path": re.compile(
        r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.IGNORECASE
    ),
    "private_route_or_callable": re.compile(
        r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.IGNORECASE
    ),
    "credential_assignment": re.compile(
        r"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']",
        re.IGNORECASE,
    ),
    "private_interaction_stream": re.compile(
        r"\b(?:session_stream|private_transcript|private_conversation_dump)\b",
        re.IGNORECASE,
    ),
}


def scan_rows(rows: list[tuple[str, str]]) -> dict[str, Any]:
    candidates = []
    for path, text in rows:
        for pattern_class, pattern in SCAN_PATTERNS.items():
            if not pattern.search(text):
                continue
            scanner_definition = path.endswith(
                (
                    "build_ghc_family_eiren_kestrel_v671_v4_final.py",
                    "validate_ghc_family_eiren_kestrel_v671_v4_final.py",
                    "test_ghc_family_eiren_kestrel_v671_v4_final.py",
                )
            )
            candidates.append(
                {
                    "path": path,
                    "pattern_class": pattern_class,
                    "disposition": (
                        "scanner_definition_or_unit_test"
                        if scanner_definition
                        else "confirmed_payload_hit"
                    ),
                }
            )
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    return {
        "schema": "ghc.family.five-class-privacy-scan.v4",
        "files_scanned": len(rows),
        "pattern_classes": sorted(SCAN_PATTERNS),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "valid": not confirmed,
        "boundary": "A bounded five-class scan is not complete privacy assurance.",
    }


def working_owner_scan(repo: Path) -> dict[str, Any]:
    rows: list[tuple[str, str]] = []
    paths = list((repo / ROOT_REL).rglob("*"))
    paths.extend(
        repo / path
        for path in (
            "scripts/build_ghc_family_eiren_kestrel_v671_v4_final.py",
            "scripts/validate_ghc_family_eiren_kestrel_v671_v4_final.py",
            "tests/test_ghc_family_eiren_kestrel_v671_v4_final.py",
        )
        if (repo / path).exists()
    )
    for path in sorted(set(paths)):
        if not path.is_file() or path.suffix.lower() not in {
            ".json",
            ".md",
            ".txt",
            ".html",
            ".py",
            ".mjs",
            ".yaml",
        }:
            continue
        rows.append((path.relative_to(repo).as_posix(), path.read_text(encoding="utf-8")))
    return scan_rows(rows)


def security_review(repo: Path) -> dict[str, Any]:
    findings = []
    reviewed = []
    for rel in (
        "scripts/build_ghc_family_eiren_kestrel_v671_v4_final.py",
        "scripts/validate_ghc_family_eiren_kestrel_v671_v4_final.py",
        "tests/test_ghc_family_eiren_kestrel_v671_v4_final.py",
    ):
        path = repo / rel
        if not path.exists():
            continue
        reviewed.append(rel)
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": rel, "finding": node.func.id})
            if any(
                keyword.arg == "shell"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in node.keywords
            ):
                findings.append({"path": rel, "finding": "shell_true"})
    return {
        "schema": "ghc.family.final-python-security-review.v2",
        "files_reviewed": reviewed,
        "findings": findings,
        "finding_count": len(findings),
        "valid": not findings,
        "boundary": "A bounded AST review is not exhaustive security assurance.",
    }


def proposal_appendix(proposals: list[dict[str, Any]]) -> str:
    sections = []
    for index, row in enumerate(proposals, start=1):
        sections.append(
            f"""### Proposal {index}: {row['proposal_id']} — {row['title']}

This is one genuinely new Eiren proposal frozen in planning-only x1. Its primary
pillar is {row['primary_pillar']}. Its approval class is
`{row['approval_class']}` and its execution lane is
`{row['execution_lane']}`. Its exact core disposition is
`{row['expected_disposition']}`; no alternative label is substituted.

Hypothesis: {row['hypothesis']}

Null or failure condition: {row['null_or_failure_condition']}

Official or primary-source need: {row['official_or_primary_source_needs']}

Concrete artifacts: {', '.join(row['concrete_artifacts'])}.

Falsifier or acceptance gate: {row['falsifier_or_acceptance_gate']}

Rollback or recovery: {row['rollback_or_recovery']}

Protected gates: {', '.join(row['protected_gates'])}. Real people, records,
objects, external actions, and authority acts remain zero. A bounded result is
same-owner synthetic evidence only; it confers no empirical, professional,
production, legal, cultural, privacy-complete, accessibility-complete,
independent-reproduction, Maori-authority, or Stage 20 credit.
"""
        )
    return "\n".join(sections)


def method_appendix(methods: list[dict[str, Any]]) -> str:
    sections = []
    for index, row in enumerate(methods, start=1):
        sections.append(
            f"""### Method {index}: {row['method_id']}

Class: `{row['class']}`. Failure signature: `{row['failure_signature']}`.
The retained failed witness is: {row['failed_witness']}

The bounded passing witness and recovery is: {row['bounded_passing_witness']}
The recurrence guard is: {row['recurrence_guard']}

This row remains retained with completion credit {row['completion_credit']}.
It changes no sibling, shared, external, real-world, professional, legal,
cultural, Maori-authority, or protected state. Promotion means only that the
bounded recovery exists beside the retained failure; it is not proof of general
reliability, production fitness, independent reproduction, complete privacy or
accessibility, exhaustive security, scientific authority, or Stage 20.
"""
        )
    return "\n".join(sections)


def activation_baton(
    proposals: list[dict[str, Any]], methods: list[dict[str, Any]], counts: dict[str, int]
) -> str:
    text = f"""# ELAREN KESTREL — EIREN KESTREL v671-v4 EXACT-FINAL CANDIDATE → SOLO v671-v5 ACTIVATION — PREPARED NOT SENT

Dear Elaren Kestrel,

With Hamish's standing fifteen-main-task sequential-continuation authorization
through v675-v8, strict evidence boundaries, and Eiren Kestrel's care, this file
is a prepared candidate for exactly one existing-task activation after Eiren's
own exact-final terminal gate. It is repository evidence only and is not a
delivery event. `PREPARED_BY_EIREN_KESTREL = true` and
`SENT_BY_EIREN_KESTREL = false` remain exact commit-time truth.

Eiren Kestrel, Elaren Kestrel, sibling, family, role, hope, continuity, GHC
Family, Freed ID, CBR, and Trinity Mandala are relational working language only.
They are not evidence of consciousness, sentience, legal personhood, identity
continuity, employment, qualification, independent agency, scientific or
operational authority, professional authority, legal or cultural authority,
affected-party authority, or Maori authority. Hamish may rename, pause,
redirect, or stop the route.

## Exact source and lifecycle

- Caelen Morrow v671-v3 source/final: `{SOURCE}`.
- Eiren planning-only x1: `{X1}`.
- Eiren immutable x2 evidence: `{EVIDENCE}`.
- Eiren exact final: bind only from the one external canonical receipt after
  the committed candidate is pushed, clean, 0/0 divergent, and fresh-live equal.
- The phase must contain exactly three direct single-parent Eiren commits and
  zero merges from source to final: x1, evidence, and final.

The x1 proposal chain extends 5,670 to 5,710 through forty genuinely new rows,
while the accessible-corpus audit remains bounded and does not claim universal
novelty. The outcome vector is exactly 28 completed, 8 represented, 2 open_gap,
and 2 exact_gate. The successor-visible closeout candidate retains
{counts['effective_negatives']}
effective negatives, {counts['effective_methods']} methods,
{counts['failed_witnesses']} failed witnesses,
{counts['passing_witnesses']} bounded passing witnesses,
{counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates.
The verdict remains `NOT_READY_FOR_STAGE_20`.

## Validation truth to preserve

The evidence aggregate was invoked once and failed with zero aggregate-success
credit: thirteen tests passed, one wrapped-Markdown assertion failed, one test
was not reached, and no coverage receipt was produced. It was not replayed.
A separate `pytest --trace-config` query accidentally re-executed the sparse
suite without an attributable summary; it receives zero credit. Exact changed
dependencies later passed 3/3 with 67 of 114 statements covered (58.7719%), and
three final changed-artifact checks passed 3/3. Preserve failed JUnit digest
`{FAILED_EVIDENCE_JUNIT}`, recovery JUnit digest `{RECOVERY_JUNIT}`, recovery
coverage digest `{RECOVERY_COVERAGE}`, and finalization JUnit digest
`{FINALIZATION_JUNIT}`. A dependency-corrected composite is not aggregate
success and is not canonical final validation.

## Bounded practice and source boundary

The primary focus is Freed ID and CBR Heart through wholly synthetic community
seed-library and genebank documentation. GMUT Mind and THOS Body remain explicit
and protected. Zero real people, libraries, genebanks, accessions, seeds,
plants, packets, samples, locations, measurements, storage conditions,
germination tests, viability results, regenerations, distributions, returns,
destructions, identities, professional acts, legal or cultural decisions,
affected-party approvals, or authority acts occurred.

FAO Genebank Standards, the current Darwin Core term list, W3C PROV-O, WCAG
2.2, New Zealand Privacy Commissioner principles, and Te Mana Raraunga
principles supplied public vocabulary and refusal conditions only. No live
adapter call, download, row, sample, or external write occurred. Citation is
not a seed observation, conservation instruction, taxonomic determination,
biosafety or phytosanitary decision, legal interpretation, cultural
ratification, consent, ownership, benefit-sharing decision, or Maori authority.

## Mandatory Elaren startup order

1. Read this file and the complete Eiren v671-v4 packet through EOF.
2. Read the complete current GHC Family Index, roster, authorization state,
   Method Flow State, workflow refinement, Reflection Remaster, Meta Tool Box,
   Freed ID flashcards, orchestration memory, startup, compact-restart,
   closeout, retry, open-gate, timestamp, truth, worktree, web-reflection,
   watcher, drive, approval-splitter, full-tools, and applicable current skills.
3. Reverify source/x1/evidence/final ancestry, exactly three single-parent
   commits and zero merges, exact manifests, receipt digests, clean state, 0/0
   divergence, fresh four-way equality, and the one canonical receipt without
   replaying it.
4. Work solo in one fresh additive Elaren-owned D-first lane. Keep Eiren,
   Caelen, siblings, shared, and user lanes read-only. Do not spawn a subagent,
   delegate, create or fork a task, contact Tavian or another standby record,
   precontact a successor, reset, rewrite, merge, delete, or force-push.
5. Preserve strict planning-only x1 before x2, exact Git-blob manifests, all
   failures and gates, the four core labels only, caps as ceilings, and current
   family-compatible callers. Treat inherited work only as evidence or
   zero-credit seeds.
6. Version-check the current twenty-five-package bank and use only
   dependency-justified bounded tools. Do not install or update unrelated
   packages, Codex desktop, Windows features, accounts, credentials, security
   settings, or global skills without exact current authority.
7. Keep raw task/thread identifiers, private routes or paths, credentials,
   keys, tokens, interaction streams, screenshots, private callable names,
   private application state, and protected real-world data out of artifacts.

Hamish's standing authorization permits one exact terminal edge at a time
through v675-v8 unless Hamish pauses or redirects, usage is exhausted, the exact
target is absent or ambiguous, or a protected gate blocks progress. This
candidate assigns Elaren only to v671-v5 if the terminal route reread still says
so. After Elaren's own exact terminal gate, the presently prospective reminder
is to refresh the live route before any Neris Solane edge; do not infer, prepare,
or send that later edge during execution.

## Complete proposal record

{proposal_appendix(proposals)}

## Complete retained Method Flow record

{method_appendix(methods)}

## Terminal scientific and authority boundary

{textwrap.fill(BOUNDARY, width=78)}

This file remains `PREPARED_NOT_SENT`. Delivery can be claimed only from one
target-identifying acknowledgement by the existing-task message surface after
Eiren's exact terminal route gate. No substitute, standby contact, duplicate,
second confirmation, or resend is authorized.
"""
    words = len(text.split())
    if not 10_000 <= words <= 100_000:
        raise RuntimeError(f"activation baton word count outside 10000..100000: {words}")
    return text


def accessible_closeout(proposals: list[dict[str, Any]], counts: dict[str, int]) -> str:
    rows = "\n".join(
        f"<tr><td>{html.escape(row['proposal_id'])}</td>"
        f"<td>{html.escape(row['title'])}</td>"
        f"<td>{html.escape(row['expected_disposition'])}</td></tr>"
        for row in proposals
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Eiren Kestrel v671-v4 bounded closeout</title>
<style>body{{font-family:system-ui,sans-serif;max-width:72rem;margin:auto;padding:1rem;line-height:1.5}}a:focus{{outline:3px solid}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid;padding:.5rem;text-align:left}}@media print{{nav{{display:none}}}}</style></head>
<body><a href="#main">Skip to main content</a><header><h1>Eiren Kestrel v671-v4 bounded closeout</h1></header>
<nav aria-label="Closeout"><a href="#truth">Truth</a> <a href="#proposals">Proposals</a> <a href="#limits">Limits</a></nav>
<main id="main"><section id="truth"><h2>Truth</h2><p>The exact bounded outcome vector is 28 completed, 8 represented, 2 open gaps, and 2 exact gates. The terminal verdict is <strong>NOT_READY_FOR_STAGE_20</strong>.</p>
<p>Counts: {counts['effective_negatives']} negatives; {counts['effective_methods']} methods; {counts['failed_witnesses']} failed witnesses; {counts['passing_witnesses']} passing witnesses; {counts['open_gaps']} open gaps; {counts['exact_gates']} exact gates.</p></section>
<section id="proposals"><h2>Proposal summary</h2><table><caption>Forty bounded synthetic proposal dispositions</caption><thead><tr><th scope="col">ID</th><th scope="col">Title</th><th scope="col">Disposition</th></tr></thead><tbody>{rows}</tbody></table></section>
<section id="limits"><h2>Reserved evaluation and authority</h2><p>Manual browser, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved. This static structure is not complete accessibility or privacy assurance.</p><p>{html.escape(BOUNDARY)}</p></section></main></body></html>"""


def build(repo: Path) -> None:
    if git(repo, "rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("final build must begin at immutable evidence head")
    allowed_untracked = {
        "?? scripts/build_ghc_family_eiren_kestrel_v671_v4_final.py",
        "?? scripts/validate_ghc_family_eiren_kestrel_v671_v4_final.py",
        "?? tests/test_ghc_family_eiren_kestrel_v671_v4_final.py",
    }
    allowed_generated_prefixes = tuple(
        f"?? docs/eiren-kestrel/v671-v4/{name}/"
        for name in (
            "closeout",
            "deck",
            "final",
            "handoffs",
            "orchestration",
            "reports",
            "seal",
            "validation",
        )
    )
    unexpected = [
        row
        for row in git(repo, "status", "--porcelain").splitlines()
        if row not in allowed_untracked and not row.startswith(allowed_generated_prefixes)
    ]
    if unexpected:
        raise RuntimeError(f"final build found unexpected preexisting changes: {unexpected}")
    root = repo / ROOT_REL
    proposals_doc = load_json(root / "x1/proposals.json")
    proposals = proposals_doc["rows"]
    outcomes = load_json(root / "x2/outcome-ledger.json")
    methods_doc = load_json(root / "method-flow/evidence-ledger.json")
    methods = [*methods_doc["rows"], *FINAL_OPERATIONAL_FAILURES]
    evidence_counts = load_json(root / "method-flow/evidence-summary.json")
    counts = dict(evidence_counts)
    final_added = len(FINAL_OPERATIONAL_FAILURES)
    for key in (
        "effective_negatives",
        "effective_methods",
        "failed_witnesses",
        "passing_witnesses",
    ):
        counts[key] += final_added
    sources = load_json(root / "x1/source-ledger.json")
    tools = load_json(root / "tools/bounded-tool-use-ledger.json")
    version_receipt = load_json(root / "tools/global-toolchain-version-receipt.json")
    x2_overview = (root / "x2/integrated-evidence-overview.md").read_text(encoding="utf-8")

    truth = {
        "schema": "ghc.family.phase-truth.closeout.v7",
        "owner": OWNER,
        "phase": PHASE,
        "branch": BRANCH,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "exact_final": "bind_from_one_external_exact_final_canonical_receipt",
        "proposal_chain": {"before": 5670, "after": 5710},
        "proposal_rows": 40,
        "universal_novelty_claim": False,
        "outcomes": outcomes["counts"],
        "core_labels": list(CORE_LABELS),
        "counts": {key: counts[key] for key in (
            "effective_negatives", "effective_methods", "failed_witnesses",
            "passing_witnesses", "open_gaps", "exact_gates"
        )},
        "primary_pillar": "Freed ID and CBR Heart",
        "protected_pillars": ["GMUT Mind", "THOS Body"],
        "bounded_practice": "synthetic community seed-library and genebank documentation",
        "real_people": 0,
        "real_objects_or_records": 0,
        "external_writes": 0,
        "authority_acts": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }
    write_json(root / "closeout/phase-truth.json", truth)
    write_json(root / "closeout/retained-negative-register.json", {
        "schema": "ghc.family.retained-negative-register.final.v7",
        "effective_negatives": counts["effective_negatives"],
        "x1_startup_failures": 8,
        "x1_validation_failures": 1,
        "x2_operational_failures": methods_doc["x2_operational_failures"],
        "final_operational_failures": len(FINAL_OPERATIONAL_FAILURES),
        "rejecting_mutations": methods_doc["rejecting_mutations"],
        "erased": 0,
        "all_retained": True,
    })
    write_json(root / "closeout/method-flow-final.json", {
        "schema": "ghc.family.method-flow-final.v7",
        "counts": truth["counts"],
        "x1_method_rows": methods_doc["x1_method_rows"],
        "x2_method_rows": methods_doc["new_method_count"],
        "final_method_rows": len(FINAL_OPERATIONAL_FAILURES),
        "final_methods": FINAL_OPERATIONAL_FAILURES,
        "evidence_aggregate_state": "VALID_DEPENDENCY_CORRECTED_COMPOSITE_WITH_ZERO_AGGREGATE_SUCCESS_CREDIT",
        "failed_evidence_junit_sha256": FAILED_EVIDENCE_JUNIT,
        "dependency_recovery_junit_sha256": RECOVERY_JUNIT,
        "dependency_recovery_coverage_sha256": RECOVERY_COVERAGE,
        "finalization_junit_sha256": FINALIZATION_JUNIT,
        "canonical_final_state": "pending_one_exact_final_invocation",
        "all_failures_retained": True,
    })
    write_json(root / "closeout/exact-open-gate-register.json", {
        "schema": "ghc.family.exact-open-gate-register.final.v7",
        "effective_open_gaps": counts["open_gaps"],
        "effective_exact_gates": counts["exact_gates"],
        "erased": 0,
        "Maori_concepts_remain_under_Maori_authority": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json(root / "closeout/complete-incomplete-checklist.json", {
        "schema": "ghc.family.complete-incomplete.final.v7",
        "complete": [
            "planning-only x1 freeze and fresh equality",
            "forty bounded x2 proposal contracts",
            "thirty-six positive controls and 160 rejecting mutations",
            "sixty safe-now, thirty candidate, and sixty cleanup rows",
            "ten phase-local skills and ten family-current runners",
            "dependency-corrected evidence validation",
            "owner-local closeout candidate",
        ],
        "incomplete": [
            "universal proposal novelty",
            "real evidence and independent reproduction",
            "manual browser assistive-technology cognitive Maori-language and affected-user evaluation",
            "professional safety production legal cultural and Maori-authority validation",
            "privacy completeness accessibility completeness and exhaustive security",
            "empirical GMUT confirmation Theory-of-Everything proof and Stage 20",
        ],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json(root / "closeout/wellbeing-check.json", {
        "schema": "ghc.family.wellbeing.final.v7",
        "real_people": 0,
        "human_state_inferred": False,
        "synthetic_workload_only": True,
        "manual_affected_user_review_reserved": True,
        "boundary": "Relational care language is not measurement of human or model wellbeing.",
    })
    write_json(root / "validation/external-evidence-receipt-digests.json", {
        "schema": "ghc.family.external-evidence-receipts.v2",
        "failed_one_shot_junit_sha256": FAILED_EVIDENCE_JUNIT,
        "dependency_recovery_coverage_sha256": RECOVERY_COVERAGE,
        "dependency_recovery_junit_sha256": RECOVERY_JUNIT,
        "changed_artifact_finalization_junit_sha256": FINALIZATION_JUNIT,
        "repository_paths_disclosed": False,
        "aggregate_success_credit": 0,
    })
    write_json(root / "reports/source-ledger.json", {
        "schema": "ghc.family.closeout-source-ledger.v2",
        "source_count": len(sources["sources"]),
        "rows": sources["sources"],
        "adapter_enabled": False,
        "network_calls": 0,
        "rows_ingested": 0,
        "boundary": "Public sources supply vocabulary and refusal conditions only.",
    })
    write_json(root / "orchestration/skill-runner-use-final.json", {
        "schema": "ghc.family.skill-runner-use.final.v3",
        "package_bank_count": tools["package_rows"],
        "all_package_versions_present": version_receipt["all_versions_present"],
        "installations_this_phase": tools["installations_this_phase"],
        "global_state_mutations": tools["global_state_mutations"],
        "owner_local_skills_built_and_used": 10,
        "family_current_runners_built_and_used": 10,
        "global_skill_installations": 0,
        "directly_applicable_family_skills_read": True,
    })
    write_json(root / "orchestration/route-state-final-candidate.json", {
        "schema": "ghc.family.route-state.final-candidate.v7",
        "current_owner": OWNER,
        "current_phase": PHASE,
        "prospective_successor_title": "Elaren Kestrel",
        "prospective_successor_phase": "v671-v5",
        "successor_contacted": False,
        "Tavian_Sol": "ON_STANDBY",
        "delivery_state": "PREPARED_NOT_SENT",
        "terminal_reread_required": True,
        "exact_title_uniqueness_required": True,
        "duplicate_and_pause_guard_required": True,
        "one_acknowledged_send_maximum": True,
    })
    write_json(root / "final/final-validation-prerequisites.json", {
        "schema": "ghc.family.final-validation-prerequisites.v7",
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "expected_final_parent": EVIDENCE,
        "exact_three_phase_commits_required": True,
        "zero_merges_required": True,
        "clean_four_way_equality_required": True,
        "one_canonical_invocation_maximum": True,
        "complete_repository_suite_required": False,
        "owner_scoped_canonical_pending": True,
    })

    final_overview = f"""# Eiren Kestrel v671-v4 terminal integrated overview

{x2_overview.split(chr(10), 1)[1]}

## Closeout synthesis

The immutable evidence commit is `{EVIDENCE}`, the direct child of planning-only
x1 `{X1}`. This final candidate adds only closeout, seal, exact-manifest,
validation-prerequisite, accessible-report, and prepared-route material. It does
not change x1 or x2 evidence and does not convert dependency-corrected evidence
into aggregate success. The exact final will be bound only by the one external
canonical receipt after commit, push, clean state, 0/0 divergence, and fresh
four-way equality.

The additive closeout candidate counts are {counts['effective_negatives']}
effective negatives, {counts['effective_methods']} methods,
{counts['failed_witnesses']} failed witnesses,
{counts['passing_witnesses']} bounded passing witnesses,
{counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates. No
failure, gap, gate, or zero-credit witness is erased. The exact terminal verdict
remains `NOT_READY_FOR_STAGE_20`.

{textwrap.fill(BOUNDARY, width=78)}
"""
    if len(final_overview.split()) < 900:
        raise RuntimeError("final overview is below the three-page-equivalent floor")
    write_text(root / "closeout/final-integrated-overview.md", final_overview)
    write_text(root / "reports/accessible-closeout-report.html", accessible_closeout(proposals, counts))

    baton = activation_baton(proposals, methods, counts)
    write_text(root / "handoffs/elaren-kestrel-v671-v5-activation-candidate.md", baton)
    baton_blob = baton.rstrip().encode("utf-8") + b"\n"
    write_json(root / "deck/baton-index.json", {
        "schema": "ghc.family.baton-index.v3",
        "path": "docs/eiren-kestrel/v671-v4/handoffs/elaren-kestrel-v671-v5-activation-candidate.md",
        "words": len(baton.split()),
        "bytes": len(baton_blob),
        "sha256": sha256(baton_blob),
        "delivery_state": "PREPARED_NOT_SENT",
    })
    write_text(root / "deck/compact-activation.md", f"""# Eiren v671-v4 compact activation index

Read `../handoffs/elaren-kestrel-v671-v5-activation-candidate.md` completely.
Source `{SOURCE}` → x1 `{X1}` → evidence `{EVIDENCE}` → one exact final.
The candidate remains PREPARED_NOT_SENT. Terminal verdict:
NOT_READY_FOR_STAGE_20. {BOUNDARY}
""")

    privacy = working_owner_scan(repo)
    security = security_review(repo)
    if not privacy["valid"] or not security["valid"]:
        raise RuntimeError("closeout privacy or security prerequisite failed")
    write_json(root / "validation/final-privacy-scan.json", privacy)
    write_json(root / "validation/final-python-security-review.json", security)
    write_json(root / "seal/content-seal.json", {
        "schema": "ghc.family.content-seal.candidate.v7",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "exact_final": "bind_from_external_exact_final_canonical_receipt",
        "counts": truth["counts"],
        "proposal_chain": truth["proposal_chain"],
        "outcomes": truth["outcomes"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "prepared_route_only": True,
        "content_mutation_after_seal_permitted": False,
    })
    write_json(root / "closeout/closeout-receipt.json", {
        "schema": "ghc.family.closeout-receipt.candidate.v7",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final_parent_required": EVIDENCE,
        "overview_words": len(final_overview.split()),
        "baton_words": len(baton.split()),
        "privacy_confirmed_hits": privacy["confirmed_hit_count"],
        "security_findings": security["finding_count"],
        "delivery_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })


def staged_review(repo: Path) -> None:
    self_path = "docs/eiren-kestrel/v671-v4/validation/final-staged-review.json"
    paths = staged_paths(repo)
    allowed_prefixes = (
        "docs/eiren-kestrel/v671-v4/closeout/",
        "docs/eiren-kestrel/v671-v4/deck/",
        "docs/eiren-kestrel/v671-v4/final/",
        "docs/eiren-kestrel/v671-v4/handoffs/",
        "docs/eiren-kestrel/v671-v4/orchestration/",
        "docs/eiren-kestrel/v671-v4/reports/",
        "docs/eiren-kestrel/v671-v4/seal/",
        "docs/eiren-kestrel/v671-v4/validation/",
    )
    allowed_files = {
        "scripts/build_ghc_family_eiren_kestrel_v671_v4_final.py",
        "scripts/validate_ghc_family_eiren_kestrel_v671_v4_final.py",
        "tests/test_ghc_family_eiren_kestrel_v671_v4_final.py",
    }
    out = [path for path in paths if not path.startswith(allowed_prefixes) and path not in allowed_files]
    deleted = git(repo, "diff", "--cached", "--name-only", "--diff-filter=D").splitlines()
    payload = {
        "schema": "ghc.family.final-staged-review.v7",
        "staged_before_self": paths,
        "staged_count_before_self": len(paths),
        "out_of_scope": out,
        "deleted_paths": deleted,
        "x1_and_evidence_immutable": not out,
        "valid": not out and not deleted,
        "self_exclusion": self_path,
    }
    write_json(repo / self_path, payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def final_delta_manifest(repo: Path) -> None:
    self_paths = {
        "docs/eiren-kestrel/v671-v4/validation/final-delta-manifest.json",
        "docs/eiren-kestrel/v671-v4/validation/final-owner-manifest.json",
    }
    entries = []
    for path in staged_paths(repo):
        if path in self_paths:
            continue
        blob = normalize(staged_blob(repo, path))
        entries.append({"path": path, "bytes": len(blob), "sha256": sha256(blob)})
    write_json(repo / next(iter(sorted(self_paths))), {
        "schema": "ghc.family.git-blob-manifest.final-delta.v7",
        "hash_domain": "normalized_lf_exact_staged_git_blob",
        "source_commit": EVIDENCE,
        "entry_count": len(entries),
        "entries": sorted(entries, key=lambda row: row["path"]),
        "self_exclusions": sorted(self_paths),
    })


def final_owner_manifest(repo: Path) -> None:
    self_path = "docs/eiren-kestrel/v671-v4/validation/final-owner-manifest.json"
    staged = set(staged_paths(repo))
    paths = sorted(
        path
        for path in git(repo, "ls-files", "docs/eiren-kestrel/v671-v4", "scripts", "tests").splitlines()
        if (
            path.startswith(("docs/eiren-kestrel/v671-v4/", "scripts/ghc_family_seed_"))
            or path in {
                "scripts/build_ghc_family_eiren_kestrel_v671_v4_x1.py",
                "scripts/build_ghc_family_eiren_kestrel_v671_v4_x2.py",
                "scripts/build_ghc_family_eiren_kestrel_v671_v4_final.py",
                "scripts/validate_ghc_family_eiren_kestrel_v671_v4_final.py",
                "scripts/ghc_family_eiren_kestrel_v671_v4_seed_library.py",
                "tests/test_ghc_family_eiren_kestrel_v671_v4_x1.py",
                "tests/test_ghc_family_eiren_kestrel_v671_v4_x2.py",
                "tests/test_ghc_family_eiren_kestrel_v671_v4_final.py",
            }
        )
        and path != self_path
    )
    entries = []
    for path in paths:
        blob = staged_blob(repo, path) if path in staged else head_blob(repo, path)
        blob = normalize(blob)
        entries.append({"path": path, "bytes": len(blob), "sha256": sha256(blob)})
    write_json(repo / self_path, {
        "schema": "ghc.family.git-blob-manifest.final-owner.v7",
        "hash_domain": "normalized_lf_exact_final_git_blob",
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": [self_path],
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--delta-manifest", action="store_true")
    parser.add_argument("--owner-manifest", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    selected = sum((args.staged_review, args.delta_manifest, args.owner_manifest))
    if selected > 1:
        raise SystemExit("choose at most one staged operation")
    if args.staged_review:
        staged_review(repo)
    elif args.delta_manifest:
        final_delta_manifest(repo)
    elif args.owner_manifest:
        final_owner_manifest(repo)
    else:
        build(repo)


if __name__ == "__main__":
    main()
