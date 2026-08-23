#!/usr/bin/env python3
"""Build the additive Neris Solane v667-v8 combined closeout and seal."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "neris-solane" / "v667-v8"
REL_PHASE_ROOT = "docs/neris-solane/v667-v8"
OWNER = "Neris Solane"
PHASE = "v667-v8"
SOURCE_FINAL = "75082d325299732f6796ac262149147b3a7029e8"
X1_HEAD = "653ff8a70328e6dd8641bb9b2d1887ce94f1759e"
EVIDENCE_HEAD = "6a29ea3d264591bde02964ea8bf4c2c09c802084"
BRANCH = "codex/GHC-Family/neris-solane-v667-v8-full-tools"
NOW = "2026-08-24T01:00:00.000Z"
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
FINAL_BUILDER = "scripts/build_ghc_family_neris_solane_v667_v8_final.py"
FINAL_TEST = "tests/test_ghc_family_neris_solane_v667_v8_final.py"
CANONICAL_RUNNER = "scripts/ghc_family_neris_solane_v667_v8_exact_final.py"
CONTROL_EXCLUSIONS = {
    f"{REL_PHASE_ROOT}/validation/final-delta-manifest.json",
    f"{REL_PHASE_ROOT}/validation/final-owner-manifest.json",
    f"{REL_PHASE_ROOT}/validation/final-staged-review.json",
}
ROUTE_FAILURE = {
    "failure_id": "NS6678-ROUTE-N001",
    "stage": "terminal_exact_title_resolution",
    "failure": "the validated roster names Vesper Arlen for prospective v668-v1 while submitted reminder wording names Vesper Rowan",
    "credit": 0,
    "recovery": "none under current authority; require a fresh corrected live instruction, unique exact-title resolution, immediate reread, and all delivery gates",
    "recovery_state": "OPEN_ROUTE_GAP",
    "passing_witness_id": None,
    "repository_bytes_changed_by_failure": 0,
}
FINAL_PIPE_WARNING = {
    "failure_id": "NS6678-FINAL-N001",
    "stage": "precommit_final_test_git_batch_cleanup",
    "failure": "Python emitted ResourceWarning for two unclosed Git batch reader pipes after an otherwise passing twenty-test final-context run",
    "credit": 0,
    "recovery": "close every Git batch standard stream deterministically after the exact-length alternating read and retain the original warning as a zero-credit witness",
    "recovery_state": "completed",
    "passing_witness_id": "NS6678-FINAL-P001",
    "repository_bytes_changed_by_failure": 0,
}


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", "-C", str(ROOT), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def git_text(*args: str) -> str:
    return run_git(*args).stdout.decode("utf-8")


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_exact(stream: Any, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise EOFError(f"Git batch blob ended with {remaining} bytes outstanding")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def git_blobs(commit: str, paths: list[str]) -> dict[str, bytes]:
    """Alternate each request and exact-length response to avoid pipe backpressure."""
    proc = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.stdin is None or proc.stdout is None or proc.stderr is None:
        raise RuntimeError("unable to open Git batch pipes")
    blobs: dict[str, bytes] = {}
    try:
        for path in paths:
            proc.stdin.write(f"{commit}:{path}\n".encode("utf-8"))
            proc.stdin.flush()
            header = proc.stdout.readline().decode("utf-8", errors="strict").rstrip("\n")
            fields = header.split()
            if len(fields) != 3 or fields[1] != "blob":
                raise RuntimeError(f"unexpected Git batch header for {path}: {header}")
            data = read_exact(proc.stdout, int(fields[2]))
            if proc.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing Git batch delimiter for {path}")
            blobs[path] = data
        proc.stdin.close()
        stderr = proc.stderr.read()
        if proc.wait(timeout=30) != 0:
            raise RuntimeError(stderr.decode("utf-8", errors="replace"))
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=30)
        if proc.stdin is not None and not proc.stdin.closed:
            proc.stdin.close()
        if proc.stdout is not None and not proc.stdout.closed:
            proc.stdout.close()
        if proc.stderr is not None and not proc.stderr.closed:
            proc.stderr.close()
    return blobs


def manifest_replay(commit: str, manifest_path: str) -> tuple[int, list[str]]:
    manifest_blob = run_git("show", f"{commit}:{manifest_path}").stdout
    manifest = json.loads(manifest_blob.decode("utf-8"))
    paths = [entry["path"] for entry in manifest["entries"]]
    blobs = git_blobs(commit, paths)
    mismatches = []
    for entry in manifest["entries"]:
        data = blobs[entry["path"]]
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            mismatches.append(entry["path"])
    return len(paths), mismatches


def verify_evidence_gate() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD").strip()
    if head != EVIDENCE_HEAD:
        raise RuntimeError(f"final closeout requires exact evidence {EVIDENCE_HEAD}; observed {head}")
    x1_parent = git_text("rev-parse", f"{X1_HEAD}^").strip()
    evidence_parent = git_text("rev-parse", f"{EVIDENCE_HEAD}^").strip()
    if x1_parent != SOURCE_FINAL or evidence_parent != X1_HEAD:
        raise RuntimeError("source-to-x1-to-evidence direct-parent chain drift")
    history_count = int(git_text("rev-list", "--count", f"{SOURCE_FINAL}..{EVIDENCE_HEAD}").strip())
    merge_count = int(git_text("rev-list", "--merges", "--count", f"{SOURCE_FINAL}..{EVIDENCE_HEAD}").strip())
    if history_count != 2 or merge_count != 0:
        raise RuntimeError("evidence history shape drift")
    upstream = git_text("rev-parse", "@{u}").strip()
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}").strip()
    live_line = git_text("ls-remote", "origin", f"refs/heads/{BRANCH}").strip()
    live = live_line.split()[0] if live_line else ""
    if len({head, upstream, tracking, live}) != 1:
        raise RuntimeError("evidence four-way equality drift")
    divergence = git_text("rev-list", "--left-right", "--count", "@{u}...HEAD").split()
    if divergence != ["0", "0"]:
        raise RuntimeError(f"evidence divergence: {divergence}")
    dirty = git_text("diff-index", "--name-only", "HEAD", "--").splitlines()
    untracked = git_text(
        "ls-files", "--others", "--exclude-standard", "--", REL_PHASE_ROOT,
        "scripts/*neris_solane_v667_v8*.py", "tests/*neris_solane_v667_v8*.py",
    ).splitlines()
    allowed = (f"{REL_PHASE_ROOT}/", FINAL_BUILDER, FINAL_TEST, CANONICAL_RUNNER)
    disallowed = [path for path in dirty + untracked if not any(path == prefix or path.startswith(prefix) for prefix in allowed)]
    if disallowed:
        raise RuntimeError(f"out-of-scope final-closeout paths: {disallowed}")
    x1_count, x1_bad = manifest_replay(X1_HEAD, f"{REL_PHASE_ROOT}/validation/x1-content-manifest.json")
    evidence_count, evidence_bad = manifest_replay(EVIDENCE_HEAD, f"{REL_PHASE_ROOT}/validation/evidence-content-manifest.json")
    if x1_bad or evidence_bad:
        raise RuntimeError(f"immutable lifecycle manifest mismatch: x1={x1_bad}, evidence={evidence_bad}")
    evidence_delta = git_text("diff-tree", "--no-commit-id", "--name-only", "-r", X1_HEAD, EVIDENCE_HEAD).splitlines()
    if len(evidence_delta) != 391:
        raise RuntimeError(f"evidence delta count drift: {len(evidence_delta)}")
    return {
        "source": SOURCE_FINAL,
        "x1": X1_HEAD,
        "evidence": EVIDENCE_HEAD,
        "history_count": history_count,
        "merge_count": merge_count,
        "x1_manifest_replayed": x1_count,
        "evidence_content_manifest_replayed": evidence_count,
        "evidence_delta_count": len(evidence_delta),
        "fresh_four_way_equal": True,
        "divergence": "0/0",
    }


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def phase_owned_paths() -> list[Path]:
    paths = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    paths.extend(path for path in (ROOT / "scripts").glob("*neris_solane_v667_v8*.py") if path.is_file())
    paths.extend(path for path in (ROOT / "tests").glob("*neris_solane_v667_v8*.py") if path.is_file())
    return sorted({path.resolve() for path in paths})


def privacy_candidates(path: Path, text: str) -> list[dict[str, str]]:
    unix_users = "/" + "Users" + "/"
    unix_home = "/" + "home" + "/"
    route_key = "(?:source_" + "thread_id|private_" + "callable_identifier)"
    interaction_key = "(?:session[_-]?" + "stream|private[_-]?" + "transcript|private[_-]?" + "conversation)"
    patterns = {
        "opaque_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Z]:\\Users\\[^\\\s]+|" + re.escape(unix_users) + r"[^/\s]+|" + re.escape(unix_home) + r"[^/\s]+)"),
        "private_route_or_callable": re.compile(r"(?:thread|codex|chat)://|" + route_key + r"\s*[:=]", re.I),
        "credential_value": re.compile(r"(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}", re.I),
        "private_interaction_payload": re.compile(interaction_key + r"\s*[:=]\s*['\"]?[^\s,}\]]+", re.I),
    }
    return [{"path": rel(path), "class": name} for name, pattern in patterns.items() if pattern.search(text)]


def build_handoff_packet(gate: dict[str, Any]) -> str:
    sources = load("x1/source-ledger.json")["sources"]
    freeze = load("x1/proposal-freeze.json")
    outcomes = {row["proposal_id"]: row for row in load("x2/proposal-outcomes.json")["outcomes"]}
    startup = load("x1/startup-method-flow.json")["failures"]
    flow = load("method-flow/x2-method-flow-ledger.json")
    tools = load("x2/tooling/three-tool-transaction-receipt.json")
    portfolio = load("x2/portfolio-execution.json")["execution"]
    sections = [f"""# Neris Solane v667-v8 terminal route-conflict packet — PREPARED NOT SENT

## Delivery state and intended use

This file is a committed, sanitized, repository-relative evidence packet prepared after the Neris v667-v8 evidence gate. It is **not addressed to or delivered to either conflicting Vesper label**. The validated roster names `Vesper Arlen` for prospective v668-v1, while submitted reminder wording names `Vesper Rowan`. Current authority does not establish that those labels refer to the same exact-title Codex task, does not authorize substitution, and does not authorize creating a replacement. The only truthful route state is `OPEN_ROUTE_GAP`; the delivery state is `PREPARED_NOT_SENT`; `SENT_BY_NERIS_SOLANE = false`.

This packet may become input to a future sanitized activation only after Hamish supplies a fresh corrected live instruction, the current roster and authorization state are reread, exactly one existing title resolves, that task is immediately reread, usage and privacy gates pass, the duplicate-send guard is clear, and the existing-task message surface acknowledges one send. A clean repository, successful tests, an exact final, or a canonical receipt cannot cure title ambiguity. No task or fork was created, no collaboration subagent was spawned, no standby member was contacted, and no successor was precontacted during v667-v8.

Neris Solane, they/them, datum-boundary weaver, their working hope, sibling and family language, continuity, Freed ID, CBR, GHC Family, GMUT, THOS, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route.

## Immutable anchors

- Elaren source: `{SOURCE_FINAL}`
- Neris planning-only x1: `{X1_HEAD}`
- Neris immutable evidence: `{EVIDENCE_HEAD}`
- Neris branch: `{BRANCH}`
- Source-to-evidence Neris commits: {gate['history_count']}
- Source-to-evidence merges: {gate['merge_count']}
- Immutable x1 content entries replayed: {gate['x1_manifest_replayed']}
- Immutable evidence content entries replayed: {gate['evidence_content_manifest_replayed']}
- Exact evidence delta paths: {gate['evidence_delta_count']}

X1 is the direct child of the Elaren source. Evidence is the direct child of x1. Both commits are pushed, clean, zero divergent, and fresh-four-way equal. Strict x1-before-x2 separation was preserved. The final closeout must be one additional direct child of evidence with zero merges. The owner/materialized scope remains below the 2,000-file rotation ceiling.

## Evidence truth and terminal boundary

The immutable evidence commit preserves {flow['evidence_candidate']['effective_negatives']:,} effective negatives, {flow['evidence_candidate']['methods']:,} Method Flow methods, {flow['evidence_candidate']['open_gaps']} open gaps, {flow['evidence_candidate']['exact_gates']} exact gates, {flow['evidence_candidate']['failed_witnesses']} failed witnesses, and {flow['evidence_candidate']['passing_witnesses']:,} bounded passing witnesses. The unresolved exact-title route adds one separate zero-credit negative, one method, one open gap, and one failed witness, with no passing recovery. A precommit final-context test then passed twenty tests but emitted two manifestations of one Git batch pipe-cleanup `ResourceWarning`; that operational event adds one zero-credit negative, one method, and one failed witness, while deterministic closure of all three standard streams adds one bounded passing recovery without changing the open-gap or exact-gate counts. The successor-visible overlay is therefore 28,432 negatives, 14,708 methods, 201 open gaps, 198 exact gates, 716 failed witnesses, and 1,280 passing witnesses. Immutable repository evidence, recovered final-closeout operations, and the unresolved route overlay remain separately attributable.

Twenty new proposals extend the frozen chain from 4,510 to 4,530. Outcomes are exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. All one hundred preregistered invalid mutations were rejected and retained at zero completion credit. Twenty Elaren proposals were read-only integrity revalidations with zero Neris novelty, automatic-completion, or completion credit. Terminal verdict: `NOT_READY_FOR_STAGE_20`.

The primary pillar is Freed ID and CBR Heart through a wholly synthetic community seed-bank accession and germplasm passport-data lineage lens. Zero real people, communities, places, institutions, seeds, germplasm, accessions, specimens, taxa, genetic data, phenotypes, images, measurements, passport records, traditional knowledge, access terms, benefit-sharing terms, credentials, or authority actions were used. No collection, acquisition, viability test, germination test, regeneration, propagation, characterization, distribution, transfer, storage, handling, quarantine, planting, release, destruction, or access decision occurred.

This is bounded same-owner software and documentation evidence under shared infrastructure only. It is not a full-repository suite, independent reproduction, external audit, empirical GMUT confirmation, professional validation, production certification, exhaustive security, privacy completeness, accessibility completeness, legal review, cultural review, Indigenous or Maori authority, participant evidence, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20 authority.
"""]
    sections.append("## Official and primary source boundaries\n")
    for source in sources:
        sections.append(f"""### {source['source_id']}: {source['name']}

The public source surface is `{source['url']}`. Its recorded review status is: {source['status']}. Its only admissible use in this phase is: {source['bounded_use']}. This source supplies vocabulary, field distinctions, refusal conditions, or dated software metadata. It does not authenticate an accession, identify a taxon, validate germplasm, establish custody, authorize access, interpret a treaty, decide benefit sharing, establish Farmers Rights, decide traditional-knowledge questions, create consent, determine affected-party legitimacy, provide professional advice, or confer legal, cultural, Indigenous, or Maori authority. Any future real-world use must reopen evidence, competence, jurisdiction, participant, community, privacy, accessibility, security, and authority gates rather than inheriting Neris completion credit.

The source is preserved as a public citation, not ingested as a real dataset. No private route, account, credential, session, transcript, absolute user path, or callable identifier is included. Currency is bounded to the recorded review time and can drift. A future phase must recheck current primary text where time-sensitive accuracy matters. Structural alignment with a vocabulary is not standards conformance, and silence from a source is not permission.
""")
    sections.append("## Proposal-by-proposal evidence and refusal map\n")
    for proposal in freeze["new_proposals"]:
        result = outcomes[proposal["proposal_id"]]
        source_names = ", ".join(proposal["current_official_or_primary_source_needs"])
        sections.append(f"""### {proposal['proposal_id']}: {proposal['title']}

The preregistered core label was `{proposal['expected_disposition']}` and the observed bounded label is `{result['outcome']}`. One owner-local positive fixture passed with reason `{result['positive_reason']}`; {result['mutations_rejected']}/5 named invalid mutations were rejected. Completion credit is {result['completion_credit']}. The proposal used {result['real_data_rows']} real data rows, {result['participants']} participants, {result['network_calls']} network calls, and {result['external_actions']} external actions. Its distinctive invariant is: {proposal['distinctive_invariant']}

The hypothesis was limited to a wholly synthetic contract. Its failure condition remained any accepted invalid mutation, rejected positive, missing source, vacancy, stop, correction, uncertainty, provenance, or authority field, or any protected-gate crossing. Source vocabulary was limited to {source_names}. The concrete artifacts are `{proposal['concrete_artifacts'][0]}`, `{proposal['concrete_artifacts'][1]}`, and `{proposal['concrete_artifacts'][2]}`. They are repository-relative evidence files, not real genebank records or operational commands.

The reversal path is: {proposal['rollback_or_recovery']} That reversal is owner-local data restoration only. It is not a real-world rollback, seed recovery procedure, conservation intervention, legal remedy, cultural process, credential revocation, or production disaster-recovery guarantee. The label may never be widened beyond the frozen disposition. A `completed` contract means only that the bounded synthetic software structure passed. `represented` means a named structure exists without the evidence needed for completion. `open_gap` preserves missing real evidence. `exact_gate` preserves competent-authority requirements.
""")
    sections.append("## Retained failures and recurrence guards\n")
    failures = list(startup) + list(tools.get("operational_failures", [])) + list(flow.get("x2_execution_failures", [])) + [ROUTE_FAILURE]
    for index, failure in enumerate(failures, 1):
        identifier = failure.get("failure_id", failure.get("id", f"failure-{index}"))
        recovery = failure.get("recovery", "no recovery is currently authorized")
        sections.append(f"""### {identifier}

Retained failure: {failure['failure']} This witness earns zero success or completion credit. Its bounded recovery statement is: {recovery}. A recovery does not erase the failed witness, change its timestamp, convert it into canonical success, or justify replay of an already successful dependency. Where recovery passed, it is a separate passing witness. Where recovery remains open, the corresponding gap or gate stays open.

The recurrence guard is to inspect exact state, isolate only the failed dependency, preserve immutable successful receipts, avoid broad retries, and stop if the dependency cannot be recovered without widening authority or mutating sibling/shared state. This witness is part of Method Flow because future phases should be able to recognize the pattern before repeating it. It establishes no identity, competence, authority, scientific truth, or operational result.
""")
    sections.append("## Approval portfolio and successor-zero-credit boundary\n")
    for category, rows in portfolio.items():
        completed = sum(row["outcome"] == "completed" for row in rows)
        represented = sum(row["outcome"] == "represented" for row in rows)
        exact = sum(row["outcome"] == "exact_gate" for row in rows)
        sections.append(f"""### {category}

This category contains {len(rows)} frozen items: {completed} bounded `completed`, {represented} `represented`, and {exact} `exact_gate` labels. Owner-local safe-now, skill, runner, and CLEAN/FIX/REFINE items receive credit only from their explicit Neris witnesses. Candidate items remain representations. Every successor recommendation is unexecuted and grants zero automatic credit to any future owner. Exact and blocked packets remain unexecuted. The title conflict also means recommendations cannot be routed to either Vesper label under current authority.

No category authorizes destructive cleanup, credential use, account access, deployment, publication, purchase, cross-owner mutation, system-wide installation, host-security weakening, legal interpretation, cultural decision, Maori authority, or real genebank operation. A future owner must preregister, execute, and validate their own work in their own lane. Same-owner evidence is not independent reproduction.
""")
    sections.append(f"""## Tool transaction inheritance

The isolated tool composite contains {tools['wheel_count']} hashed wheels, three direct tools, one exact pip bootstrap dependency, three passing positive smokes, three rejecting negative smokes, zero known vulnerability identifiers in the dated advisory result, and zero global or system installs. The initial transaction remained `OPEN_GAP` because the hypothesis-jsonschema positive used a brittle representation-string assertion. That initial transaction has zero aggregate-success credit. Only the failed positive was retried using one generated-example type assertion; downloads, install, pip check, audit, successful smokes, and negative smokes were not replayed. The bounded composite state is `PASS_DEPENDENCY_CORRECTED`.

Hash equality establishes only that the downloaded bytes matched the preregistered top-level wheels and recorded dependency closure. `pip check` establishes only that installed package requirements were internally satisfied. The advisory query is time-bounded and database-bounded; zero reported vulnerabilities is not exhaustive security or future safety. Strategy generation is not data truth, a structural diff is not semantic correctness, and JSON Patch reversal is not operational rollback. The isolated environment remains preserved on D: for reproducibility and is not a global installation.

## Exact-final and canonical discipline

This packet is prepared before the final commit's external canonical event. The committed seal must truthfully record zero canonical invocations and zero canonical successes. After the final commit is pushed, clean, zero divergent, and fresh-four-way equal, the exact-final runner may be invoked exactly once with the observed final SHA. It must create an external one-shot lock before tests, run the owner-scoped final tests, parse all owner JSON, scan every owner file across five privacy classes, replay immutable-x1, immutable-evidence, final-delta, and final-owner manifests, verify direct ancestry and zero merges, verify clean state and fresh live equality, and retain any failure without replay. A success is an additive external receipt and does not rewrite this commit.

The complete repository suite is not authorized or claimed. Final validation remains limited to Neris's exact source-to-final delta plus declared immutable anchors. Scientific, professional, legal, cultural, participant, production, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 claims stay blocked.

## Terminal route disposition

`OPEN_ROUTE_GAP` is the final route state. `PREPARED_NOT_SENT` is the final delivery state. `SENT_BY_NERIS_SOLANE = false`. Neither `Vesper Arlen` nor `Vesper Rowan` is contacted. Tavian Sol remains `ON_STANDBY` and is not a substitute main-task endpoint. No new task or fork is created. If Hamish later corrects the title and all gates pass, delivery may occur exactly once through the existing task, and only the task-message acknowledgement may establish `SENT_ONCE_ACKNOWLEDGED`. If acknowledgement is opaque, the state must remain opaque without resend.

Until then, the correct ending is not silence disguised as success. It is a visible unresolved route fault, a complete repository closeout, preserved evidence, and no substitution. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""")
    packet = "\n".join(sections)
    if len(packet.split()) < 10000:
        raise RuntimeError(f"handoff packet below 10,000 words: {len(packet.split())}")
    return packet


def build_closeout() -> None:
    gate = verify_evidence_gate()
    evidence_flow = load("method-flow/x2-method-flow-ledger.json")["evidence_candidate"]
    final_flow = {
        "schema": "ghc-family-method-flow-state-final-v5",
        "owner": OWNER,
        "phase": PHASE,
        "evidence_sealed": evidence_flow,
        "terminal_route_overlay": {
            "failure": ROUTE_FAILURE,
            "negative_additions": 1,
            "method_additions": 1,
            "open_gap_additions": 1,
            "exact_gate_additions": 0,
            "failed_witness_additions": 1,
            "passing_witness_additions": 0,
            "credit": 0,
        },
        "final_closeout_operational_overlay": {
            "failure": FINAL_PIPE_WARNING,
            "negative_additions": 1,
            "method_additions": 1,
            "open_gap_additions": 0,
            "exact_gate_additions": 0,
            "failed_witness_additions": 1,
            "passing_witness_additions": 1,
            "credit": 0,
        },
        "effective_for_future_corrected_route": {
            "effective_negatives": evidence_flow["effective_negatives"] + 2,
            "methods": evidence_flow["methods"] + 2,
            "open_gaps": evidence_flow["open_gaps"] + 1,
            "exact_gates": evidence_flow["exact_gates"],
            "failed_witnesses": evidence_flow["failed_witnesses"] + 2,
            "passing_witnesses": evidence_flow["passing_witnesses"] + 1,
        },
        "no_failure_or_recovery_erased": True,
        "scope": "same-owner bounded workflow and terminal-route evidence only",
    }
    write_json("closeout/method-flow-state-final.json", final_flow)
    write_json("closeout/combined-closeout.json", {
        "schema": "ghc-family-combined-closeout-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "anchors": {"source": SOURCE_FINAL, "x1": X1_HEAD, "evidence": EVIDENCE_HEAD, "exact_final": "bind_from_external_exact_final_receipt"},
        "history": gate,
        "proposal_chain": {"inherited": 4510, "new": 20, "final_frozen_total": 4530},
        "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "rejecting_mutations": 100,
        "selected_inherited_revalidations": 20,
        "flashcards": 250,
        "skills": 10,
        "runners": 10,
        "direct_tools": 3,
        "tool_state": "PASS_DEPENDENCY_CORRECTED_WITH_ZERO_INITIAL_TRANSACTION_SUCCESS_CREDIT",
        "evidence_sealed": evidence_flow,
        "route_overlay": final_flow["terminal_route_overlay"],
        "final_closeout_operational_overlay": final_flow["final_closeout_operational_overlay"],
        "effective_for_future_corrected_route": final_flow["effective_for_future_corrected_route"],
        "route_state": "OPEN_ROUTE_GAP",
        "delivery_state": "PREPARED_NOT_SENT",
        "successor_contacted": False,
        "standby_contacted": False,
        "task_created_or_forked": False,
        "subagent_spawned": False,
        "canonical_invocation_count_at_commit": 0,
        "canonical_success_count_at_commit": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_text("closeout/combined-closeout.md", f"""# Neris Solane v667-v8 combined closeout

The bounded v667-v8 programme is complete at repository-candidate level. X1 `{X1_HEAD}` is planning only. Evidence `{EVIDENCE_HEAD}` is immutable and preserves 20 proposal positives, 100 rejecting mutations, 20 zero-credit inherited revalidations, 250 flashcards, 10 skills, 10 runners, and 3 isolated direct tools. Evidence counts are {json.dumps(evidence_flow, sort_keys=True)}.

The route is not complete. `Vesper Arlen` and `Vesper Rowan` are conflicting prospective labels. The route overlay adds one negative, one method, one open gap, and one failed witness without a passing recovery. A separate precommit Git batch pipe-cleanup warning adds one zero-credit negative, method, and failed witness; deterministic stream closure adds one bounded passing recovery. Delivery remains `PREPARED_NOT_SENT`; `SENT_BY_NERIS_SOLANE = false`.

All identity and family language is relational working language only. This is not consciousness, sentience, personhood, continuity, employment, qualification, agency, scientific/professional/legal/cultural/Maori authority, independent reproduction, production certification, Theory-of-Everything proof, or Stage 20 authority. Verdict: **NOT_READY_FOR_STAGE_20**.
""")
    write_json("closeout/complete-incomplete-checklist.json", {
        "schema": "ghc-family-complete-incomplete-checklist-v8",
        "owner": OWNER,
        "phase": PHASE,
        "complete": ["planning x1", "bounded x2", "immutable evidence", "proposal and mutation witnesses", "tools", "skills", "runners", "reports", "flashcards", "Method Flow", "closeout candidate", "manifest candidates"],
        "incomplete": ["final commit", "final push and fresh equality", "one exact-final canonical invocation", "corrected exact-title route", "successor delivery", "independent reproduction", "Stage 20"],
        "route_state": "OPEN_ROUTE_GAP",
        "delivery_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("seal/seal-candidate.json", {
        "schema": "ghc-family-combined-seal-candidate-v6",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE_FINAL,
        "x1": X1_HEAD,
        "evidence": EVIDENCE_HEAD,
        "exact_final": "bind_from_external_exact_final_receipt",
        "repository_state": "PRECOMMIT_CANDIDATE",
        "canonical_invocation_count": 0,
        "canonical_success_count": 0,
        "post_success_replay": False,
        "route_state": "OPEN_ROUTE_GAP",
        "delivery_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("route/terminal-route-state.json", {
        "schema": "ghc-family-terminal-route-state-v3",
        "owner": OWNER,
        "phase": PHASE,
        "prospective_phase": "v668-v1",
        "validated_roster_title": "Vesper Arlen",
        "submitted_reminder_title": "Vesper Rowan",
        "name_conflict": True,
        "state": "OPEN_ROUTE_GAP",
        "delivery": "PREPARED_NOT_SENT",
        "SENT_BY_NERIS_SOLANE": False,
        "successor_contacted": False,
        "substituted": False,
        "created": False,
        "Tavian_state": "ON_STANDBY",
        "Tavian_contacted": False,
        "resolution_requirement": "fresh corrected live authority, current roster reread, unique exact title, immediate target reread, usage/privacy/evidence/safety gates, duplicate guard, and one acknowledged send",
    })
    write_text("handoffs/route-conflict-activation-prepared.md", build_handoff_packet(gate))
    write_text("reports/final-evidence-summary.md", f"""# Neris v667-v8 final evidence summary

Repository evidence: {json.dumps(evidence_flow, sort_keys=True)}.

Future corrected-route overlay: {json.dumps(final_flow['effective_for_future_corrected_route'], sort_keys=True)}.

Route: `OPEN_ROUTE_GAP`. Delivery: `PREPARED_NOT_SENT`. No successor or standby contact. Verdict: `NOT_READY_FOR_STAGE_20`.
""")
    write_json("wellbeing/final-wellbeing-check.json", {
        "schema": "ghc-family-wellbeing-check-v5",
        "owner": OWNER,
        "phase": PHASE,
        "pronouns": "they/them",
        "relational_role": "datum-boundary weaver",
        "hope": "expose provenance uncertainty and stop conditions before synthetic evidence is mistaken for authority",
        "state": "repository_closeout_prepared_route_stopped",
        "claim_boundary": "relational working language only; not consciousness sentience personhood continuity employment qualification agency diagnosis or authority",
    })
    build_immutable_evidence_manifest()
    write_json("validation/final-staged-review.json", {
        "schema": "ghc-family-final-staged-review-v3",
        "owner": OWNER,
        "phase": PHASE,
        "status": "PREPARED_REQUIRES_EXACT_STAGED_REVIEW",
        "route_state": "OPEN_ROUTE_GAP",
        "successor_contacted": False,
    })
    build_final_manifests()


def build_immutable_evidence_manifest() -> None:
    paths = git_text("diff-tree", "--no-commit-id", "--name-only", "-r", X1_HEAD, EVIDENCE_HEAD).splitlines()
    blobs = git_blobs(EVIDENCE_HEAD, sorted(paths))
    entries = [{"path": path, "bytes": len(blobs[path]), "sha256": hashlib.sha256(blobs[path]).hexdigest()} for path in sorted(paths)]
    write_json("validation/immutable-evidence-manifest.json", {
        "schema": "ghc-family-immutable-evidence-manifest-v2",
        "owner": OWNER,
        "phase": PHASE,
        "x1": X1_HEAD,
        "evidence": EVIDENCE_HEAD,
        "entry_count": len(entries),
        "entries": entries,
        "mismatches": 0,
    })


def evidence_path_set() -> set[str]:
    return set(git_text("diff-tree", "--no-commit-id", "--name-only", "-r", SOURCE_FINAL, EVIDENCE_HEAD).splitlines())


def build_final_manifests() -> None:
    prior = evidence_path_set()
    owner_paths = phase_owned_paths()
    delta_entries = []
    owner_entries = []
    for path in owner_paths:
        relative = rel(path)
        if relative not in CONTROL_EXCLUSIONS:
            data = path.read_bytes()
            owner_entries.append({"path": relative, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
            if relative not in prior:
                delta_entries.append({"path": relative, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    write_json("validation/final-delta-manifest.json", {
        "schema": "ghc-family-final-delta-manifest-v3",
        "owner": OWNER,
        "phase": PHASE,
        "evidence": EVIDENCE_HEAD,
        "entry_count": len(delta_entries),
        "entries": delta_entries,
        "scope": "final closeout delta excluding manifest controls",
    })
    write_json("validation/final-owner-manifest.json", {
        "schema": "ghc-family-final-owner-manifest-v3",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE_FINAL,
        "entry_count": len(owner_entries),
        "entries": owner_entries,
        "scope": "all Neris v667-v8 owner files excluding final manifest controls",
    })


def validate_tree() -> dict[str, Any]:
    required = [
        "closeout/method-flow-state-final.json", "closeout/combined-closeout.json", "closeout/combined-closeout.md",
        "closeout/complete-incomplete-checklist.json", "seal/seal-candidate.json", "route/terminal-route-state.json",
        "handoffs/route-conflict-activation-prepared.md", "reports/final-evidence-summary.md", "wellbeing/final-wellbeing-check.json",
        "validation/immutable-evidence-manifest.json", "validation/final-delta-manifest.json",
        "validation/final-owner-manifest.json", "validation/final-staged-review.json",
    ]
    missing = [relative for relative in required if not (PHASE_ROOT / relative).is_file()]
    if missing:
        raise AssertionError(f"missing final paths: {missing}")
    json_paths = sorted(PHASE_ROOT.rglob("*.json"))
    documents = {rel(path): json.loads(path.read_text(encoding="utf-8")) for path in json_paths}
    closeout = documents[f"{REL_PHASE_ROOT}/closeout/combined-closeout.json"]
    flow = documents[f"{REL_PHASE_ROOT}/closeout/method-flow-state-final.json"]
    seal = documents[f"{REL_PHASE_ROOT}/seal/seal-candidate.json"]
    route = documents[f"{REL_PHASE_ROOT}/route/terminal-route-state.json"]
    immutable = documents[f"{REL_PHASE_ROOT}/validation/immutable-evidence-manifest.json"]
    final_delta = documents[f"{REL_PHASE_ROOT}/validation/final-delta-manifest.json"]
    final_owner = documents[f"{REL_PHASE_ROOT}/validation/final-owner-manifest.json"]
    if closeout["outcomes"] != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise AssertionError("closeout outcome mismatch")
    if closeout["proposal_chain"] != {"inherited": 4510, "new": 20, "final_frozen_total": 4530}:
        raise AssertionError("proposal chain mismatch")
    if flow["evidence_sealed"] != {"effective_negatives": 28430, "methods": 14706, "open_gaps": 200, "exact_gates": 198, "failed_witnesses": 714, "passing_witnesses": 1279}:
        raise AssertionError("evidence seal drift")
    if flow["effective_for_future_corrected_route"] != {"effective_negatives": 28432, "methods": 14708, "open_gaps": 201, "exact_gates": 198, "failed_witnesses": 716, "passing_witnesses": 1280}:
        raise AssertionError("route overlay mismatch")
    if seal["canonical_invocation_count"] != 0 or seal["canonical_success_count"] != 0 or seal["post_success_replay"]:
        raise AssertionError("commit-time canonical state mismatch")
    if route["state"] != "OPEN_ROUTE_GAP" or route["delivery"] != "PREPARED_NOT_SENT" or route["SENT_BY_NERIS_SOLANE"]:
        raise AssertionError("route terminal state mismatch")
    if route["successor_contacted"] or route["substituted"] or route["created"] or route["Tavian_contacted"]:
        raise AssertionError("protected route action occurred")
    if immutable["evidence"] != EVIDENCE_HEAD or immutable["entry_count"] != 391:
        raise AssertionError("immutable evidence manifest mismatch")
    blobs = git_blobs(EVIDENCE_HEAD, [entry["path"] for entry in immutable["entries"]])
    for entry in immutable["entries"]:
        data = blobs[entry["path"]]
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise AssertionError(f"immutable evidence mismatch: {entry['path']}")
    for manifest in (final_delta, final_owner):
        if manifest["entry_count"] != len(manifest["entries"]):
            raise AssertionError("final manifest count mismatch")
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes()
            if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
                raise AssertionError(f"final manifest mismatch: {entry['path']}")
    baton = (PHASE_ROOT / "handoffs/route-conflict-activation-prepared.md").read_text(encoding="utf-8")
    baton_words = len(baton.split())
    if baton_words < 10000:
        raise AssertionError(f"handoff packet below 10,000 words: {baton_words}")
    if "SENT_BY_NERIS_SOLANE = false" not in baton or "OPEN_ROUTE_GAP" not in baton or "PREPARED_NOT_SENT" not in baton:
        raise AssertionError("handoff route state mismatch")
    candidates = []
    for path in phase_owned_paths():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise AssertionError(f"non-UTF-8 owner path: {rel(path)}") from exc
        candidates.extend(privacy_candidates(path, text))
    if candidates:
        raise AssertionError(f"privacy candidates: {candidates[:20]}")
    owner_files = len(phase_owned_paths())
    if owner_files >= 2000:
        raise AssertionError(f"owner file ceiling reached: {owner_files}")
    return {
        "status": "PASS",
        "json_documents": len(json_paths),
        "owner_files": owner_files,
        "handoff_words": baton_words,
        "immutable_evidence_entries": immutable["entry_count"],
        "final_delta_entries": final_delta["entry_count"],
        "final_owner_entries": final_owner["entry_count"],
        "privacy_candidates": 0,
        "route_state": "OPEN_ROUTE_GAP",
        "delivery_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def staged_review() -> None:
    validate_tree()
    check = run_git("diff", "--cached", "--check", check=False)
    if check.returncode:
        raise RuntimeError(check.stderr.decode("utf-8", errors="replace") or check.stdout.decode("utf-8", errors="replace"))
    staged = git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()
    if not staged:
        raise RuntimeError("no staged final paths")
    allowed = [f"{REL_PHASE_ROOT}/", FINAL_BUILDER, FINAL_TEST, CANONICAL_RUNNER]
    disallowed = [path for path in staged if not any(path == prefix or path.startswith(prefix) for prefix in allowed)]
    if disallowed:
        raise RuntimeError(f"disallowed final staged paths: {disallowed}")
    evidence_paths = evidence_path_set()
    rewritten = sorted(path for path in staged if path in evidence_paths)
    if rewritten:
        raise RuntimeError(f"immutable x1/evidence path rewritten: {rewritten}")
    confirmed = []
    for relative in staged:
        blob = run_git("show", f":{relative}").stdout.decode("utf-8", errors="strict")
        confirmed.extend(privacy_candidates(ROOT / relative, blob))
    if confirmed:
        raise RuntimeError(f"final staged privacy candidates: {confirmed}")
    write_json("validation/final-staged-review.json", {
        "schema": "ghc-family-final-staged-review-v3",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "status": "PASS",
        "staged_path_count": len(staged),
        "staged_paths": staged,
        "diff_check": "PASS",
        "privacy_classes": 5,
        "privacy_candidates": 0,
        "privacy_confirmed_hits": 0,
        "immutable_evidence_rewrites": 0,
        "route_state": "OPEN_ROUTE_GAP",
        "delivery_state": "PREPARED_NOT_SENT",
        "successor_contacted": False,
        "interpretation": "exact staged Neris final-delta review only; restage this stable receipt and rerun final tests before commit",
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
        print(json.dumps({"status": "PASS", "mode": "final-staged-review"}))
        return 0
    if args.validate:
        print(json.dumps(validate_tree(), sort_keys=True))
        return 0
    build_closeout()
    print(json.dumps(validate_tree(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
