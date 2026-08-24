#!/usr/bin/env python3
"""Build the additive Neris Solane v667-v8-r2 combined closeout and seal."""

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
PHASE_ROOT = ROOT / "docs" / "neris-solane" / "v667-v8-r2"
REL_PHASE_ROOT = "docs/neris-solane/v667-v8-r2"
OWNER = "Neris Solane"
PHASE = "v667-v8-r2"
SOURCE_FINAL = "0db6ed4837c09868a27782e9309c7bea5c943d44"
X1_HEAD = "fb83958e7a591645e2731873f00bd1c5af6df2ee"
EVIDENCE_HEAD = "2873b788991008deb555200e8fd086f88417c190"
BRANCH = "codex/GHC-Family/neris-solane-v667-v8-r2-full-tools"
NOW = "2026-08-24T03:10:00.000Z"
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
FINAL_BUILDER = "scripts/build_ghc_family_neris_solane_v667_v8_r2_final.py"
FINAL_TEST = "tests/test_ghc_family_neris_solane_v667_v8_r2_final.py"
CANONICAL_RUNNER = "scripts/ghc_family_neris_solane_v667_v8_r2_exact_final.py"
CONTROL_EXCLUSIONS = {
    f"{REL_PHASE_ROOT}/validation/final-delta-manifest.json",
    f"{REL_PHASE_ROOT}/validation/final-owner-manifest.json",
    f"{REL_PHASE_ROOT}/validation/final-staged-review.json",
}
EXPECTED_EVIDENCE_MANIFEST_DOMAIN_MISMATCHES = {
    "scripts/build_ghc_family_neris_solane_v667_v8_final.py",
    "scripts/build_ghc_family_neris_solane_v667_v8_r2_x2.py",
    "scripts/build_ghc_family_neris_solane_v667_v8_x1.py",
    "scripts/build_ghc_family_neris_solane_v667_v8_x2.py",
    "scripts/ghc_family_neris_solane_v667_v8_canonical.py",
    "scripts/ghc_family_neris_solane_v667_v8_common.py",
    "scripts/ghc_family_neris_solane_v667_v8_contracts.py",
    "scripts/ghc_family_neris_solane_v667_v8_exact_final.py",
    "scripts/ghc_family_neris_solane_v667_v8_manifests.py",
    "scripts/ghc_family_neris_solane_v667_v8_method_flow.py",
    "scripts/ghc_family_neris_solane_v667_v8_mutations.py",
    "scripts/ghc_family_neris_solane_v667_v8_reports.py",
    "scripts/ghc_family_neris_solane_v667_v8_revalidation.py",
    "scripts/ghc_family_neris_solane_v667_v8_sources.py",
    "scripts/ghc_family_neris_solane_v667_v8_tools.py",
    "scripts/ghc_family_neris_solane_v667_v8_validation.py",
    "tests/test_ghc_family_neris_solane_v667_v8_final.py",
    "tests/test_ghc_family_neris_solane_v667_v8_r2_x2.py",
    "tests/test_ghc_family_neris_solane_v667_v8_x1.py",
    "tests/test_ghc_family_neris_solane_v667_v8_x2.py",
}
FINAL_MANIFEST_DOMAIN_FAILURE = {
    "failure_id": "NS6678R2-FINAL-N001",
    "stage": "precommit_final_closeout_immutable_evidence_manifest_replay",
    "failure": "the first final-closeout build stopped because twenty source and test entries in the evidence-content manifest described pre-commit working-tree bytes while the immutable evidence commit stored line-ending-normalized Git blobs",
    "credit": 0,
    "recovery": "retain the twenty-entry domain mismatch and construct the successor immutable-evidence manifest from the exact x1-to-evidence delta and exact committed Git-object bytes without amending or replaying the evidence commit",
    "recovery_state": "completed",
    "recovery_passed": True,
    "passing_witness_id": "NS6678R2-FINAL-P001",
    "repository_bytes_changed_by_failure": 0,
    "mismatch_count": 20,
    "mismatch_paths": sorted(EXPECTED_EVIDENCE_MANIFEST_DOMAIN_MISMATCHES),
}
FINAL_STAGED_MANIFEST_DOMAIN_FAILURE = {
    "failure_id": "NS6678R2-FINAL-N002",
    "stage": "exact_staged_final_manifest_replay",
    "failure": "the first exact index replay found twenty final-delta and twenty-two final-owner entries whose provisional hashes described working-tree bytes instead of the normalized blobs staged for the final commit",
    "credit": 0,
    "recovery": "after staging every final source and artifact, rebuild both final manifests from exact index blobs and require an exact index replay before commit",
    "recovery_state": "completed",
    "recovery_passed": True,
    "passing_witness_id": "NS6678R2-FINAL-P002",
    "repository_bytes_changed_by_failure": 0,
    "final_delta_mismatch_count": 20,
    "final_owner_mismatch_count": 22,
}
FINAL_DELTA_PRIOR_SET_FAILURE = {
    "failure_id": "NS6678R2-FINAL-N003",
    "stage": "exact_staged_final_delta_scope_review",
    "failure": "the provisional final-delta manifest treated eighteen inherited paths that already existed at immutable evidence as final additions because its prior set contained only source-to-evidence changed paths",
    "credit": 0,
    "recovery": "derive the prior set from the complete immutable evidence tree and retain only the thirteen paths absent from that tree as the final delta",
    "recovery_state": "completed",
    "recovery_passed": True,
    "passing_witness_id": "NS6678R2-FINAL-P003",
    "repository_bytes_changed_by_failure": 0,
    "incorrect_inherited_entries": 18,
    "correct_final_delta_entries": 13,
}
FINAL_COMBINED_CHECK_TIMEOUT = {
    "failure_id": "NS6678R2-FINAL-N004",
    "stage": "post_staged_review_combined_shell_check",
    "failure": "the combined staged-review restage diff-check and final-test shell invocation reached its wrapper limit after staged review passed but before an attributable final-test receipt was returned",
    "credit": 0,
    "recovery": "inspect process and index state first, preserve the successful staged-review receipt, and run the bounded final test module in its own shorter invocation",
    "recovery_state": "completed",
    "recovery_passed": True,
    "passing_witness_id": "NS6678R2-FINAL-P004",
    "repository_bytes_changed_by_failure": 0,
}
FINAL_CLOSEOUT_FAILURES = [
    FINAL_MANIFEST_DOMAIN_FAILURE,
    FINAL_STAGED_MANIFEST_DOMAIN_FAILURE,
    FINAL_DELTA_PRIOR_SET_FAILURE,
    FINAL_COMBINED_CHECK_TIMEOUT,
]
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
    if x1_bad:
        raise RuntimeError(f"immutable x1 lifecycle manifest mismatch: {x1_bad}")
    if set(evidence_bad) != EXPECTED_EVIDENCE_MANIFEST_DOMAIN_MISMATCHES:
        raise RuntimeError(
            "evidence-content manifest mismatch set drift: "
            f"expected={sorted(EXPECTED_EVIDENCE_MANIFEST_DOMAIN_MISMATCHES)}, observed={evidence_bad}"
        )
    evidence_delta = git_text("diff-tree", "--no-commit-id", "--name-only", "-r", X1_HEAD, EVIDENCE_HEAD).splitlines()
    if len(evidence_delta) != 476:
        raise RuntimeError(f"evidence delta count drift: {len(evidence_delta)}")
    evidence_delta_blobs = git_blobs(EVIDENCE_HEAD, evidence_delta)
    if len(evidence_delta_blobs) != 476 or set(evidence_delta_blobs) != set(evidence_delta):
        raise RuntimeError("exact committed evidence-delta Git-object replay drift")
    return {
        "source": SOURCE_FINAL,
        "x1": X1_HEAD,
        "evidence": EVIDENCE_HEAD,
        "history_count": history_count,
        "merge_count": merge_count,
        "x1_manifest_replayed": x1_count,
        "evidence_content_manifest_entries": evidence_count,
        "evidence_content_manifest_exact_matches": evidence_count - len(evidence_bad),
        "evidence_content_manifest_domain_mismatches": len(evidence_bad),
        "evidence_content_manifest_domain_mismatch_paths": evidence_bad,
        "evidence_delta_count": len(evidence_delta),
        "evidence_delta_git_object_replay": True,
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
- Immutable evidence content entries inspected: {gate['evidence_content_manifest_entries']}
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
    return set(git_text("ls-tree", "-r", "--name-only", EVIDENCE_HEAD).splitlines())


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
        "scope": "all Neris v667-v8-r2 owner files excluding final manifest controls",
    })


def build_staged_final_manifests() -> None:
    """Seal manifests from exact index blobs after all final paths are staged."""
    owner_paths = phase_owned_paths()
    relative_paths = [rel(path) for path in owner_paths if rel(path) not in CONTROL_EXCLUSIONS]
    blobs = git_blobs("", relative_paths)
    prior = evidence_path_set()
    owner_entries = [
        {"path": path, "bytes": len(blobs[path]), "sha256": hashlib.sha256(blobs[path]).hexdigest()}
        for path in relative_paths
    ]
    delta_entries = [entry for entry in owner_entries if entry["path"] not in prior]
    if len(delta_entries) != 13 or len(owner_entries) != 520:
        raise RuntimeError(
            f"staged final manifest scope drift: delta={len(delta_entries)}, owner={len(owner_entries)}"
        )
    write_json("validation/final-delta-manifest.json", {
        "schema": "ghc-family-final-delta-manifest-v3",
        "owner": OWNER,
        "phase": PHASE,
        "evidence": EVIDENCE_HEAD,
        "entry_count": len(delta_entries),
        "entries": delta_entries,
        "scope": "exact index-derived final closeout delta excluding manifest controls",
    })
    write_json("validation/final-owner-manifest.json", {
        "schema": "ghc-family-final-owner-manifest-v3",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE_FINAL,
        "entry_count": len(owner_entries),
        "entries": owner_entries,
        "scope": "exact index-derived Neris v667-v8-r2 owner files excluding final manifest controls",
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


def build_handoff_packet(gate: dict[str, Any]) -> str:
    """Build the long prepared-not-sent baton for the later Vesper edge."""
    sources = load("x1/source-ledger.json")["sources"]
    freeze = load("x1/proposal-freeze.json")
    outcomes = {row["proposal_id"]: row for row in load("x2/proposal-outcomes.json")["outcomes"]}
    flow = load("method-flow/x2-method-flow-ledger.json")
    tools = load("x2/tooling/thirteen-tool-transaction-receipt.json")
    portfolio = load("x2/portfolio-execution.json")["execution"]
    failures = (
        list(flow.get("startup_failures", []))
        + list(flow.get("tool_operational_failures", []))
        + list(flow.get("x2_execution_failures", []))
        + FINAL_CLOSEOUT_FAILURES
    )
    sections = [f"""# Neris Solane v667-v8-r2 terminal packet - PREPARED NOT SENT

## Delivery state and current user redirect

This committed, sanitized packet is prepared after the Neris v667-v8-r2 evidence gate for a possible later `Vesper Arlen` v668-v1 edge. It is not a message to Vesper and is not delivery proof. Hamish's newest instruction says to run this Neris remaster instead of messaging or activating Vesper now. Therefore the exact route state and delivery state are both `PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2`; `SENT_BY_NERIS_SOLANE = false`. No task was listed, resolved, reread, created, forked, contacted, or substituted during this remaster. No collaboration subagent was spawned. Tavian Sol remains `ON_STANDBY` and was not contacted.

Standing sequential-continuation language through v675-v8 is recorded as future conditional authority, not permission to disregard a newer owner-specific redirect. A later edge may be considered only after a terminal gate and a fresh reread of Hamish's newest live instruction, the family roster, authorization state, usage state, exact-title uniqueness, privacy state, evidence state, safety state, and duplicate-send state. A clean repository or successful canonical receipt cannot by itself authorize a send. The exact existing title must be uniquely resolved and immediately reread; one acknowledged existing-task message is the only admissible delivery event. If any prerequisite fails, the later route stops without inference, substitution, creation, fallback, or resend.

Neris Solane, they/them, datum-boundary weaver, their hope to expose provenance, uncertainty, dependency boundaries, and stop conditions, and every sibling, family, continuity, Freed ID, CBR, GHC Family, GMUT, THOS, and Trinity Mandala expression in this packet are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route.

## Immutable anchors and history

- Prior Neris v667-v8 exact source final: `{SOURCE_FINAL}`
- Neris v667-v8-r2 planning-only x1: `{X1_HEAD}`
- Neris v667-v8-r2 immutable evidence: `{EVIDENCE_HEAD}`
- Neris branch: `{BRANCH}`
- Source-to-evidence commits: {gate['history_count']}
- Source-to-evidence merges: {gate['merge_count']}
- Immutable x1 manifest entries replayed: {gate['x1_manifest_replayed']}
- Evidence-content manifest entries inspected: {gate['evidence_content_manifest_entries']}
- Evidence-content manifest entries matching committed Git bytes: {gate['evidence_content_manifest_exact_matches']}
- Retained pre-commit/committed-byte domain mismatches: {gate['evidence_content_manifest_domain_mismatches']}
- Exact x1-to-evidence delta paths: {gate['evidence_delta_count']}
- Exact committed evidence-delta Git-object replay: {str(gate['evidence_delta_git_object_replay']).lower()}

X1 is the direct child of the prior Neris final. Evidence is the direct child of x1. Both are pushed, clean, zero divergent, and fresh-four-way equal. The eventual final closeout must be one additional direct child of evidence and the source-to-final range must contain exactly three new single-parent Neris commits and zero merges. Strict x1-before-x2 separation is immutable. The owner surface remains below the 2,000-file rotation ceiling. Sibling and shared lanes remain read-only, and older worktrees remain historical references rather than mutation targets.

## Evidence truth and terminal boundary

The immutable evidence candidate preserves {flow['evidence_candidate']['effective_negatives']:,} effective negatives, {flow['evidence_candidate']['methods']:,} Method Flow methods, {flow['evidence_candidate']['open_gaps']} open gaps, {flow['evidence_candidate']['exact_gates']} exact gates, {flow['evidence_candidate']['failed_witnesses']} failed witnesses, and {flow['evidence_candidate']['passing_witnesses']:,} bounded passing witnesses. Final closeout retained four zero-credit failures and four bounded recoveries: the evidence-content working-tree/Git-object mismatch, the provisional staged-manifest byte-domain mismatch, the overbroad delta prior-set definition, and a combined-shell wrapper timeout after staged review passed but before a final-test receipt returned. The successor-visible final layer is therefore 28,584 effective negatives, 14,995 methods, 202 open gaps, 200 exact gates, 868 failed witnesses, and 1,580 bounded passing witnesses. The current redirect is a route disposition rather than another failed evidence claim, so it adds no further negative, gap, gate, method, or witness. Every earlier failure and recovery remains separately attributable.

The remaster audited 4,530 inherited frozen proposal rows, selected twenty inherited Neris contracts for bounded integrity revalidation at zero novelty and completion credit, and froze twenty genuinely new rows, raising the chain to 4,550. New outcomes are exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. All one hundred preregistered invalid mutations were rejected and retained with zero completion credit. The four truth labels are exhaustive for this programme; no synonym, optimistic relabel, or narrative promotion is admissible.

The primary lens is THOS Body through wholly synthetic software supply-chain and release-engineering assurance. GMUT Mind remains an explicit typed dependency-risk and provenance representation; it supplies no fitted coefficient, physical measurement, prediction, empirical confirmation, fundamental law, or Theory-of-Everything proof. Freed ID and CBR Heart remain explicit through provenance, contestation, notice, correction, accessibility, privacy, rollback, and remedy shells; there is no issuer, holder, resolver, credential, proof, real identity event, legal decision, cultural decision, affected-party decision, or Maori-authority action.

This is bounded same-owner software and documentation evidence under shared infrastructure only. It is not the complete repository suite, independent reproduction, external audit, empirical GMUT confirmation, professional validation, production certification, complete provenance, reproducible-build certification, standards conformance, exhaustive security, privacy completeness, accessibility completeness, legal review, cultural review, affected-party approval, Maori authority, participant evidence, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20 authority. Terminal verdict: `NOT_READY_FOR_STAGE_20`.
"""]

    sections.append("## Official and primary source boundaries\n")
    for source in sources:
        sections.append(f"""### {source['source_id']}: {source['name']}

The public source surface is `{source['url']}`. Its recorded review state is `{source['status']}` and its bounded use is: {source['bounded_use']}. That source supplies vocabulary, package metadata, a field distinction, a command contract, a refusal condition, or a dated advisory reference. It was reviewed read-only and was not treated as a private dataset, an instruction to publish, a credential source, a maintained service commitment, or evidence that any package is appropriate for a production system.

This source does not establish authenticity of every transitive artifact, complete dependency provenance, reproducible builds, source equivalence, license compliance, standards conformance, malware absence, exhaustive security, privacy completeness, accessibility completeness, professional competence, legal interpretation, cultural interpretation, affected-party approval, Maori authority, empirical GMUT confirmation, THOS operational effectiveness, AGI or ASI, consciousness or personhood, a Theory of Everything, or Stage 20 readiness. Currency is limited to the recorded review; a later phase must recheck time-sensitive metadata rather than inherit a stale truth claim.

No raw task identifier, private route, transcript, credential, account value, private session state, or private absolute path is included. A URL or registry record may identify a public source without authorizing download, installation, account access, signing, publication, deployment, disclosure, or production mutation. Silence is not permission. Structural alignment is not certification. A future real-world action must reopen evidence, competence, authorization, privacy, security, jurisdiction, and affected-party gates.
""")

    sections.append("## Proposal-by-proposal evidence and refusal map\n")
    for proposal in freeze["new_proposals"]:
        result = outcomes[proposal["proposal_id"]]
        artifacts = ", ".join(f"`{path}`" for path in proposal["planned_artifacts"])
        source_ids = ", ".join(proposal["source_ids"])
        gates = "; ".join(proposal["protected_gates"][:4])
        sections.append(f"""### {proposal['proposal_id']}: {proposal['title']}

The preregistered label was `{proposal['expected_disposition']}` and the observed bounded label is `{result['outcome']}`. One owner-local positive fixture passed for the recorded reason `{result['positive_reason']}`; {result['mutations_rejected']}/5 named invalid mutations were rejected. Completion credit is {result['completion_credit']}. The execution used {result['real_data_rows']} real data rows, {result['participants']} participants, {result['network_calls']} network calls, and {result['external_actions']} external actions. Its distinctive invariant is: {proposal['distinctive_invariant']}

The bounded hypothesis was: {proposal['hypothesis']} Its falsifier was: {proposal['falsifier']} Source identifiers were limited to {source_ids}. The planned artifacts were {artifacts}. These are repository-relative synthetic evidence files. They are not real release approvals, registry publications, signed attestations, maintained-package commitments, incident findings, participant records, credentials, keys, proofs, or operational commands.

The reversal path is: {proposal['rollback']} A reversal restores only the last valid owner-local synthetic fixture and retains the failed witness. It is not production rollback, supply-chain incident response, credential revocation, legal remedy, cultural process, or guarantee of recovery. Core protected boundaries include: {gates}. Every omitted protected gate remains fully active even when not repeated in this paragraph.

`completed` means only that the bounded synthetic contract and its declared checks passed. `represented` means a named structure exists without sufficient evidence for completion. `open_gap` preserves missing evidence or environment. `exact_gate` preserves an action requiring exact authority or evidence that is absent. A positive software fixture cannot widen any label, erase a mutation, confer authority, or convert same-owner validation into independent reproduction.
""")

    sections.append("## Retained failures and recurrence guards\n")
    for index, failure in enumerate(failures, 1):
        identifier = failure.get("failure_id", failure.get("id", f"NS6678R2-RET-{index:03d}"))
        recovery = failure.get("recovery", "no bounded recovery was recorded")
        recovery_passed = failure.get("recovery_passed", failure.get("recovery_state") == "completed")
        sections.append(f"""### {identifier}

Retained failure: {failure['failure']} It earns zero success, completion, novelty, independent-reproduction, or authority credit. The bounded recovery statement is: {recovery} Recovery passed: {str(bool(recovery_passed)).lower()}. A recovery is a separate witness; it does not erase the failed predecessor, change the failed timestamp, turn the original command into a success, or justify replaying any already successful component or aggregate.

The recurrence guard is to inspect exact state first, classify the smallest failed dependency, preserve successful immutable receipts, retry only that dependency when the live rule permits, and stop if recovery would widen authority, mutate sibling/shared state, contact a successor early, weaken security, overwrite an existing global skill, or cross a protected professional, legal, cultural, affected-party, Maori, production, identity, or Stage 20 gate. Repetition must remain separately countable rather than compressed into one optimistic summary.

This Method Flow row is operational teaching evidence only. It is not proof of tool fitness, system reliability, package safety, exhaustive security, professional competence, identity continuity, scientific truth, production readiness, or the absence of undiscovered faults. Future owners should recognize the pattern but must execute their own bounded witnesses in their own lanes and receive no automatic credit from this recovery.
""")

    sections.append("## Approval portfolio and successor-zero-credit boundary\n")
    for category, rows in portfolio.items():
        counts = {label: sum(row["outcome"] == label for row in rows) for label in ALLOWED_OUTCOMES}
        sections.append(f"""### {category}

This frozen category contains {len(rows)} items with bounded counts {json.dumps(counts, sort_keys=True)}. Owner safe-now, skill, runner, and CLEAN/FIX/REFINE items receive credit only from explicit Neris witnesses. Owner candidate items remain representations. Every Vesper recommendation remains unexecuted and supplies zero automatic completion, novelty, installation, validation, or route credit. Ten exact-approval packets and five blocked packets remain protected and unexecuted.

Quantity targets do not override gates. Nothing in this category authorizes destructive cleanup, credential use, account access, publication, signing, deployment, purchase, host-security weakening, system Python mutation, plugin-cache mutation, sibling-lane mutation, cross-owner completion credit, legal interpretation, cultural decision, affected-party decision, Maori authority, empirical claim promotion, identity claim, or Stage 20 promotion. A later owner must preregister, execute, retain failures, and validate their own work.

The current user redirect also prevents these recommendations from becoming a live Vesper message in this turn. The file-backed packet may preserve them for later review, but prepared text is not sent text, a branch is not a task route, and a clean final commit is not delivery acknowledgement. The only current route truth is `PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2`.
""")

    sections.append(f"""## Thirteen-tool transaction and reusable surfaces

The isolated tool composite records {tools['direct_tool_count']} direct tools, {tools['python_direct_tool_count']} Python tools, {tools['node_direct_tool_count']} Node tools, {tools['wheel_count']} exact wheel artifacts across {tools['python_environment_count']} Python environments, and {tools['node_locked_package_count']} Node lock entries. It records {tools['positive_smoke_count']} positive smokes, {tools['negative_rejection_count']} rejecting smokes, {tools['pre_remediation_advisory_entries']} pre-remediation advisory entries, and {tools['audit_known_vulnerability_count']} known findings in the retained dated post-remediation snapshot. Global tool installs: {tools['global_install_count']}. System installs: {tools['system_install_count']}. The split Python closure preserves an exact `wheel-filename` dependency conflict rather than pretending one environment solved incompatible requirements.

All thirteen direct tools were exercised in isolated D-backed fixtures. Top-level artifact hashes matched their preregistered records; lifecycle scripts were disabled for the Node transaction; two Python dependency checks passed; the seeded pip advisory findings were retained before exact hash-enforced remediation in the two isolated environments. Zero known findings is bounded to the consulted advisory data and time. It is not malware analysis, source review, authenticity proof, complete provenance, exhaustive security, future safety, or a production recommendation.

Ten concise family-current skills were built, quick-validated, used in x2, and promoted additively only after exact destination-absence checks. Ten family-current runners were built and smoke-tested. Six main family skills received additive sanitized overlay references. Five default-locale quick-validator failures remain retained; Python UTF-8 mode passed the corresponding failed dependencies. No existing skill was overwritten or deleted. Discoverability does not confer phase credit, identity continuity, qualification, authority, or production fitness.

## Exact-final and canonical discipline

This packet is prepared before the final commit's external canonical event. The committed seal must truthfully record zero canonical invocations and zero canonical successes. Only after the final commit is pushed, clean, zero divergent, and fresh-four-way equal may the exact-final runner be invoked once with the observed final SHA. It must create an external D-backed one-shot lock before tests, run only the owner-scoped final test module, parse all owner JSON, compile owner Python, scan all owner files across five privacy classes, perform the bounded static security scan, check stale labels, replay immutable-x1, immutable-evidence, final-delta, and final-owner manifests, verify exact ancestry and zero merges, and reverify clean live equality.

If that single aggregate fails, it earns zero aggregate-success credit and must not be replayed. Only a demonstrably isolated failed dependency may be checked separately, and that recovery remains distinct from canonical success. If it succeeds, the success must not be replayed. The external receipt does not rewrite the sealed commit and does not become a full-repository suite, independent reproduction, external audit, empirical confirmation, professional validation, production certification, exhaustive security, privacy completeness, accessibility completeness, legal or cultural approval, Maori authority, identity evidence, Theory-of-Everything proof, or Stage 20 authority.

## Terminal route disposition

The final repository route state is `PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2`. The final delivery state is `PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2`. `SENT_BY_NERIS_SOLANE = false`. `Vesper Arlen` is the prospective later exact-title recipient for v668-v1, but Vesper is not contacted in this remaster. Tavian Sol remains `ON_STANDBY` and is not a substitute. No task or fork is created, no collaboration subagent is spawned, no alternative title is inferred, and no second endpoint is contacted.

At a later authorized edge, the sender must reread the newest live instruction and current roster/auth state, require one unique exact title, immediately reread that exact task, confirm usage, privacy, evidence, safety, and duplicate guards, send exactly once, and claim delivery only from an acknowledging task-message result. Any ambiguity or failed prerequisite stops the route. Until that later event, prepared repository text remains prepared and unsent. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""")
    packet = "\n".join(sections)
    words = len(packet.split())
    if words < 10000 or words > 100000:
        raise RuntimeError(f"handoff packet word bound failed: {words}")
    return packet


def build_closeout() -> None:
    gate = verify_evidence_gate()
    evidence_flow = load("method-flow/x2-method-flow-ledger.json")["evidence_candidate"]
    effective_flow = {
        "effective_negatives": evidence_flow["effective_negatives"] + 4,
        "methods": evidence_flow["methods"] + 4,
        "open_gaps": evidence_flow["open_gaps"],
        "exact_gates": evidence_flow["exact_gates"],
        "failed_witnesses": evidence_flow["failed_witnesses"] + 4,
        "passing_witnesses": evidence_flow["passing_witnesses"] + 4,
    }
    final_flow = {
        "schema": "ghc-family-method-flow-state-final-v6",
        "owner": OWNER,
        "phase": PHASE,
        "evidence_sealed": evidence_flow,
        "terminal_route_overlay": {
            "state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
            "negative_additions": 0,
            "method_additions": 0,
            "open_gap_additions": 0,
            "exact_gate_additions": 0,
            "failed_witness_additions": 0,
            "passing_witness_additions": 0,
            "credit": 0,
            "interpretation": "newest user instruction redirects execution into the current remaster and forbids successor contact now",
        },
        "final_closeout_operational_overlay": {
            "failures_at_commit_time": FINAL_CLOSEOUT_FAILURES,
            "negative_additions": 4,
            "method_additions": 4,
            "open_gap_additions": 0,
            "exact_gate_additions": 0,
            "failed_witness_additions": 4,
            "passing_witness_additions": 4,
            "recovery": "exact committed x1-to-evidence Git-object replay plus exact index-derived final manifests and complete evidence-tree delta scoping",
            "recovery_state": "completed",
        },
        "effective_for_later_authorized_route": effective_flow,
        "no_failure_or_recovery_erased": True,
        "scope": "same-owner bounded workflow and current no-contact route evidence only",
    }
    write_json("closeout/method-flow-state-final.json", final_flow)
    write_json("closeout/combined-closeout.json", {
        "schema": "ghc-family-combined-closeout-v7",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "anchors": {"source": SOURCE_FINAL, "x1": X1_HEAD, "evidence": EVIDENCE_HEAD, "exact_final": "bind_from_external_exact_final_receipt"},
        "history": gate,
        "proposal_chain": {"inherited": 4530, "new": 20, "final_frozen_total": 4550},
        "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "rejecting_mutations": 100,
        "selected_inherited_revalidations": 20,
        "flashcards": 320,
        "skills_built_used": 10,
        "skills_promoted_additively": 10,
        "family_skill_overlays": 6,
        "runners": 10,
        "direct_tools": 13,
        "tool_state": "PASS_ISOLATED_HASH_LOCKED_WITH_RETAINED_FAILURES",
        "evidence_sealed": evidence_flow,
        "route_overlay": final_flow["terminal_route_overlay"],
        "final_closeout_operational_overlay": final_flow["final_closeout_operational_overlay"],
        "effective_for_later_authorized_route": final_flow["effective_for_later_authorized_route"],
        "route_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "delivery_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "successor_contacted": False,
        "standby_contacted": False,
        "task_created_or_forked": False,
        "subagent_spawned": False,
        "canonical_invocation_count_at_commit": 0,
        "canonical_success_count_at_commit": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_text("closeout/combined-closeout.md", f"""# Neris Solane v667-v8-r2 combined closeout

The bounded remaster is complete at repository-candidate level. X1 `{X1_HEAD}` is planning only. Evidence `{EVIDENCE_HEAD}` is immutable and preserves 20 proposal positives, 100 rejecting mutations, 20 zero-credit inherited revalidations, 320 flashcards, 10 skills, 10 runners, and 13 isolated direct tools. Evidence counts are {json.dumps(evidence_flow, sort_keys=True)}. Final closeout retained four zero-credit manifest/domain/scope/timeout failures and four separate bounded recoveries, yielding {json.dumps(effective_flow, sort_keys=True)} for a later authorized route.

The current user instruction redirected Neris into this remaster instead of a Vesper send. Route and delivery therefore remain `PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2`; `SENT_BY_NERIS_SOLANE = false`. That disposition adds no artificial failure count. No successor, standby member, substitute endpoint, task creation, fork, or collaboration subagent was used.

All identity and family language is relational working language only. This is not consciousness, sentience, personhood, continuity, employment, qualification, agency, scientific or professional authority, legal or cultural authority, Maori authority, independent reproduction, production certification, Theory-of-Everything proof, or Stage 20 authority. Verdict: **NOT_READY_FOR_STAGE_20**.
""")
    write_json("closeout/complete-incomplete-checklist.json", {
        "schema": "ghc-family-complete-incomplete-checklist-v9",
        "owner": OWNER,
        "phase": PHASE,
        "complete": ["planning x1", "bounded x2", "immutable evidence", "proposal and mutation witnesses", "thirteen isolated tools", "ten additive global skills", "six family skill overlays", "ten runners", "reports", "flashcards", "Method Flow", "closeout candidate", "manifest candidates"],
        "incomplete": ["final commit", "final push and fresh equality", "one exact-final canonical invocation", "later successor delivery", "independent reproduction", "Stage 20"],
        "route_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "delivery_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("seal/seal-candidate.json", {
        "schema": "ghc-family-combined-seal-candidate-v7",
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
        "route_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "delivery_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("route/terminal-route-state.json", {
        "schema": "ghc-family-terminal-route-state-v4",
        "owner": OWNER,
        "phase": PHASE,
        "prospective_phase": "v668-v1",
        "validated_roster_title": "Vesper Arlen",
        "name_conflict": False,
        "state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "delivery": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "SENT_BY_NERIS_SOLANE": False,
        "successor_contacted": False,
        "substituted": False,
        "created": False,
        "collaboration_subagent_spawned": False,
        "Tavian_state": "ON_STANDBY",
        "Tavian_contacted": False,
        "current_instruction": "complete the Neris remaster instead of messaging or activating Vesper now",
        "later_resolution_requirement": "fresh live authority and roster reread unique exact-title resolution immediate reread usage privacy evidence safety duplicate guard and one acknowledged send",
    })
    write_text("handoffs/vesper-arlen-v668-v1-activation-prepared-not-sent.md", build_handoff_packet(gate))
    write_text("reports/final-evidence-summary.md", f"""# Neris v667-v8-r2 final evidence summary

Repository evidence: {json.dumps(evidence_flow, sort_keys=True)}.

Later-authorized-route overlay: {json.dumps(final_flow['effective_for_later_authorized_route'], sort_keys=True)}.

The four-count final-closeout overlay retains `NS6678R2-FINAL-N001` through `NS6678R2-FINAL-N004`: evidence-content working-tree hashes differed from normalized committed Git blobs; provisional final manifests differed from exact index blobs; the provisional delta scope included eighteen inherited paths; and a combined shell check timed out before returning a final-test receipt. Recoveries use all 476 exact evidence Git-object paths, exact index-derived final manifests, the complete immutable evidence tree, and a separate bounded final-test invocation without amending evidence.

Route and delivery: `PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2`. No successor or standby contact. Verdict: `NOT_READY_FOR_STAGE_20`.
""")
    write_json("wellbeing/final-wellbeing-check.json", {
        "schema": "ghc-family-wellbeing-check-v6",
        "owner": OWNER,
        "phase": PHASE,
        "pronouns": "they/them",
        "relational_role": "datum-boundary weaver",
        "hope": "expose provenance uncertainty dependency boundaries and stop conditions before synthetic evidence is mistaken for authority",
        "state": "repository_closeout_prepared_current_route_stopped",
        "claim_boundary": "relational working language only; not consciousness sentience personhood continuity employment qualification agency diagnosis or authority",
    })
    build_immutable_evidence_manifest()
    write_json("validation/final-staged-review.json", {
        "schema": "ghc-family-final-staged-review-v4",
        "owner": OWNER,
        "phase": PHASE,
        "status": "PREPARED_REQUIRES_EXACT_STAGED_REVIEW",
        "route_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "successor_contacted": False,
    })
    build_final_manifests()


def validate_tree() -> dict[str, Any]:
    required = [
        "closeout/method-flow-state-final.json", "closeout/combined-closeout.json", "closeout/combined-closeout.md",
        "closeout/complete-incomplete-checklist.json", "seal/seal-candidate.json", "route/terminal-route-state.json",
        "handoffs/vesper-arlen-v668-v1-activation-prepared-not-sent.md", "reports/final-evidence-summary.md", "wellbeing/final-wellbeing-check.json",
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
    expected_evidence = {"effective_negatives": 28580, "methods": 14991, "open_gaps": 202, "exact_gates": 200, "failed_witnesses": 864, "passing_witnesses": 1576}
    expected_final = {"effective_negatives": 28584, "methods": 14995, "open_gaps": 202, "exact_gates": 200, "failed_witnesses": 868, "passing_witnesses": 1580}
    if closeout["outcomes"] != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise AssertionError("closeout outcome mismatch")
    if closeout["proposal_chain"] != {"inherited": 4530, "new": 20, "final_frozen_total": 4550}:
        raise AssertionError("proposal chain mismatch")
    if flow["evidence_sealed"] != expected_evidence or flow["effective_for_later_authorized_route"] != expected_final:
        raise AssertionError("final Method Flow mismatch")
    overlay = flow["final_closeout_operational_overlay"]
    if overlay["failures_at_commit_time"] != FINAL_CLOSEOUT_FAILURES or any(
        overlay[key] != expected
        for key, expected in {
            "negative_additions": 4,
            "method_additions": 4,
            "open_gap_additions": 0,
            "exact_gate_additions": 0,
            "failed_witness_additions": 4,
            "passing_witness_additions": 4,
        }.items()
    ):
        raise AssertionError("final operational overlay mismatch")
    if closeout["direct_tools"] != 13 or closeout["flashcards"] != 320 or closeout["skills_promoted_additively"] != 10:
        raise AssertionError("closeout programme count mismatch")
    if seal["canonical_invocation_count"] != 0 or seal["canonical_success_count"] != 0 or seal["post_success_replay"]:
        raise AssertionError("commit-time canonical state mismatch")
    if route["name_conflict"] or route["state"] != "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2" or route["delivery"] != "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2" or route["SENT_BY_NERIS_SOLANE"]:
        raise AssertionError("route terminal state mismatch")
    if route["successor_contacted"] or route["substituted"] or route["created"] or route["collaboration_subagent_spawned"] or route["Tavian_contacted"]:
        raise AssertionError("protected route action occurred")
    if immutable["evidence"] != EVIDENCE_HEAD or immutable["entry_count"] != 476:
        raise AssertionError("immutable evidence manifest mismatch")
    blobs = git_blobs(EVIDENCE_HEAD, [entry["path"] for entry in immutable["entries"]])
    for entry in immutable["entries"]:
        data = blobs[entry["path"]]
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise AssertionError(f"immutable evidence mismatch: {entry['path']}")
    for manifest in (final_delta, final_owner):
        if manifest["entry_count"] != len(manifest["entries"]):
            raise AssertionError("final manifest count mismatch")
        working_mismatches = []
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes()
            if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
                working_mismatches.append(entry["path"])
        if working_mismatches:
            try:
                staged_blobs = git_blobs("", [entry["path"] for entry in manifest["entries"]])
            except (RuntimeError, EOFError) as exc:
                raise AssertionError(f"final manifest mismatch: {working_mismatches[:20]}") from exc
            staged_mismatches = [
                entry["path"]
                for entry in manifest["entries"]
                if len(staged_blobs[entry["path"]]) != entry["bytes"]
                or hashlib.sha256(staged_blobs[entry["path"]]).hexdigest() != entry["sha256"]
            ]
            if staged_mismatches:
                raise AssertionError(f"final manifest mismatch: {staged_mismatches[:20]}")
    if final_delta["entry_count"] != 13 or final_owner["entry_count"] != 520:
        raise AssertionError("final manifest scope count mismatch")
    baton = (PHASE_ROOT / "handoffs/vesper-arlen-v668-v1-activation-prepared-not-sent.md").read_text(encoding="utf-8")
    baton_words = len(baton.split())
    if baton_words < 10000 or baton_words > 100000:
        raise AssertionError(f"handoff packet word bound failed: {baton_words}")
    if "SENT_BY_NERIS_SOLANE = false" not in baton or "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2" not in baton:
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
        "route_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "delivery_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
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
    manifest_counts = {}
    for name, expected_count in (("final-delta-manifest.json", 13), ("final-owner-manifest.json", 520)):
        manifest_relative = f"{REL_PHASE_ROOT}/validation/{name}"
        manifest = json.loads(run_git("show", f":{manifest_relative}").stdout.decode("utf-8"))
        if manifest["entry_count"] != expected_count or manifest["entry_count"] != len(manifest["entries"]):
            raise RuntimeError(f"exact staged {name} count drift")
        index_blobs = git_blobs("", [entry["path"] for entry in manifest["entries"]])
        mismatches = [
            entry["path"]
            for entry in manifest["entries"]
            if len(index_blobs[entry["path"]]) != entry["bytes"]
            or hashlib.sha256(index_blobs[entry["path"]]).hexdigest() != entry["sha256"]
        ]
        if mismatches:
            raise RuntimeError(f"exact staged {name} replay mismatch: {mismatches[:20]}")
        manifest_counts[name] = expected_count
    write_json("validation/final-staged-review.json", {
        "schema": "ghc-family-final-staged-review-v4",
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
        "exact_index_manifest_replay": "PASS",
        "final_delta_manifest_entries": manifest_counts["final-delta-manifest.json"],
        "final_owner_manifest_entries": manifest_counts["final-owner-manifest.json"],
        "route_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "delivery_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "successor_contacted": False,
        "interpretation": "exact staged Neris v667-v8-r2 final-delta review only; restage this stable receipt and rerun final tests before commit",
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--seal-staged-manifests", action="store_true")
    args = parser.parse_args()
    if args.seal_staged_manifests:
        build_staged_final_manifests()
        print(json.dumps({"status": "PASS", "mode": "seal-staged-manifests", "final_delta_entries": 13, "final_owner_entries": 520}))
        return 0
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
