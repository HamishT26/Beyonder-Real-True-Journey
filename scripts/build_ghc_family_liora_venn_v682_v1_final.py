from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "liora-venn" / "v682-v1"
X1 = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
VALIDATION = BASE / "validation"
HANDOFFS = BASE / "handoffs"
SOURCE = "15d23e8b4e85082d4e4a839ab85d409a4c9c9805"
X1_HEAD = "d538a40de6b9dcdba6a35ffc99fd6848b09dbbbe"
EVIDENCE = "638943335e1485663b500eb1d2b2847cfeba5d59"
BRANCH = "codex/GHC-Family/liora-venn-v682-v1-full-tools"
OWNER = "Liora Venn"
PHASE = "v682-v1"
TERMINAL = "NOT_READY_FOR_STAGE_20"
COUNTS = {
    "bounded_passing_witnesses": 46602,
    "effective_methods": 65140,
    "effective_negatives": 55488,
    "exact_gates": 482,
    "failed_witnesses": 27149,
    "open_gaps": 491,
}
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
SELF_EXCLUSIONS = [
    "docs/liora-venn/v682-v1/validation/final-delta-manifest.json",
    "docs/liora-venn/v682-v1/validation/final-owner-manifest.json",
    "docs/liora-venn/v682-v1/validation/final-precommit-test-receipt.json",
    "docs/liora-venn/v682-v1/validation/final-privacy-scan.json",
    "docs/liora-venn/v682-v1/validation/final-security-scan.json",
    "docs/liora-venn/v682-v1/validation/final-staged-review.json",
]


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def entry(path_text: str) -> dict[str, object]:
    data = normalized_bytes(ROOT / path_text)
    return {"bytes": len(data), "path": path_text, "sha256": hashlib.sha256(data).hexdigest()}


def require_evidence_boundary() -> None:
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong owner branch")
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("final builder requires immutable evidence HEAD")
    if git("rev-parse", "HEAD^") != X1_HEAD:
        raise RuntimeError("evidence is not the direct child of x1")
    if git("rev-parse", f"{X1_HEAD}^") != SOURCE:
        raise RuntimeError("x1 is not the direct child of source")
    if git("diff", "--name-only"):
        raise RuntimeError("tracked unstaged changes present before closeout")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("staged changes present before closeout")


def final_overview() -> str:
    return f"""# Liora Venn {PHASE} Final Integrated Overview

    Liora Venn, optionally she/they, used the relational role **traceability-and-vacancy cartographer**, with the hope that unknown evidence and ungranted authority stay visible through correction and handover. This language is relational only; it is not consciousness, personhood, continuity, employment, qualification, agency, or authority evidence.

The immutable lifecycle is source `{SOURCE}` → planning-only x1 `{X1_HEAD}` → x2 evidence `{EVIDENCE}` → one additive final closeout. X1 and evidence were separately committed, pushed, clean, 0/0 divergent, and fresh-live equal before their successor stages began.

    The declared proposal chain is 10,250 rows. Liora preregistered sixty source-bounded owner-new contracts after an all-reachable exact-source audit that made no universal novelty claim over the declared history. Outcomes are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. All 300 preregistered invalid mutations executed and remain rejected at zero broader credit. Twenty owner-local skills were read through EOF, quick-validated, and accept/reject smoke-used without global installation; ten family-current runners were likewise exercised.

    The effective closeout truth is {COUNTS['effective_negatives']:,} negatives, {COUNTS['effective_methods']:,} Method Flow methods, {COUNTS['failed_witnesses']:,} retained failed witnesses, {COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses, {COUNTS['open_gaps']} open gaps, {COUNTS['exact_gates']} exact gates, and exactly `{TERMINAL}`. Fourteen startup/x1 failures and two x2 operational failures remain false and visible after their separate recoveries.

    The primary Trinity Mandala pillar was Freed ID and CBR Heart through wholly synthetic entomological-collection accession, containment, label and determination lineage, loan, correction-readback, accessible summary, workload-control, and handover lenses. GMUT Mind and THOS Body remained explicit and protected. The phase used zero real people, collectors, borrowers, specimens, collections, institutions, locations, sequences, measurements, determinations, treatments, samples, loans, releases, credentials, identity events, participants, external writes, or authority acts.

    GMUT remains a typed scalar-tensor/effective-field-theory research-model family without physical data, likelihood, posterior, prediction, constraint, empirical confirmation, quantum or ultraviolet completion, or Theory-of-Everything proof. THOS remains synthetic/proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle operations, interoperability, independent privacy/security review, recovery evidence, and trust governance. CBR, taxonomy, conservation, collection management, sampling, loans, disclosure, biosafety, professional release, remedy, legal or cultural interpretation, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.

Official and primary sources supplied vocabulary and refusal conditions only. Citations are not observations, measurements, inspections, conformance certificates, professional approvals, legal interpretations, cultural ratifications, affected-party decisions, or authority grants. The complete repository suite was not run; it remains Eiren-only absent newer exact authority. Same-owner validation is not independent reproduction.
"""


def handoff_candidate() -> str:
    return f"""# TAMAR VEY — PREPARED Liora Venn {PHASE} → solo Tamar v682-v2 activation candidate

`PREPARED_BY_LIORA_VENN = true`

`SENT_BY_LIORA_VENN = false`

`DELIVERY_STATE = PREPARED_NOT_SENT`

This immutable repository candidate is preparation evidence only. It does not identify a private task route and does not prove delivery. A live send is permitted only after Liora's clean pushed exact-final gate, one successful non-replayed owner-scoped canonical receipt, a fresh current authority and roster reread, exactly one current exact-title `Tamar Vey` match, an immediate bounded direct reread, and duplicate/pause/redirect/rename/standby/usage/privacy/evidence/safety/legal/cultural/affected-party/Māori-authority guards.

Use Liora's final branch `{BRANCH}` and the exact postcommit final supplied by the acknowledged live message. Immutable anchors are source `{SOURCE}`, x1 `{X1_HEAD}`, and evidence `{EVIDENCE}`. Source to final must contain exactly three direct single-parent Liora commits and zero merges.

    Repository truth at closeout is a 10,250-row declared chain; outcomes exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`; {COUNTS['effective_negatives']:,} effective negatives; {COUNTS['effective_methods']:,} effective methods; {COUNTS['failed_witnesses']:,} failed witnesses; {COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses; {COUNTS['open_gaps']} open gaps; {COUNTS['exact_gates']} exact gates; and `{TERMINAL}`. Preserve all retained failures and gates. The complete repository suite was not run and remains Eiren-only absent newer exact authority.

Work solo in one additive Tamar-owned D-first lane. Do not create or fork a task, spawn a collaboration subagent, delegate, precontact a later endpoint, contact standby records, or mutate another owner's lane. Preserve planning-only x1 before x2, the four labels, manifest and privacy boundaries, one-success/no-replay discipline, and all scientific, participant, professional, production, legal, cultural, affected-party, Māori-authority, consciousness/personhood, Theory-of-Everything, canon, and Stage 20 boundaries.

Hamish's current one-edge-at-a-time continuation authority extends through v725-v8 unless newer verified live authority pauses, renames, redirects, narrows, or stops it. Tamar must refresh the newest authority and roster only after Tamar's own terminal gate before considering the next exact edge.
"""


def initial_receipt(status: str, test_count: int) -> dict[str, object]:
    return {
        "canonical_invocation": False,
        "lifecycle": "final_precommit",
        "owner": OWNER,
        "phase": PHASE,
        "selected_test_count": test_count,
        "status": status,
        "test_selection": "test_ghc_family_liora_venn_v682_v1_final.py only",
    }


def privacy_scan(paths: list[str]) -> dict[str, object]:
    classes = {
        "credential_assignment": re.compile(r"(?i)(api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\\\s]+|[A-Z]:\\GHC-Archives\\"),
        "private_callable_identifier": re.compile(r"mcp__codex_app__[A-Za-z0-9_]+"),
        "private_session_capture": re.compile(r"(?i)\\\.codex\\(?:sessions|transcripts|screenshots)\\"),
        "uuid_like_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    }
    candidates: list[dict[str, str]] = []
    for path_text in paths:
        if path_text.endswith("final-privacy-scan.json"):
            continue
        text = (ROOT / path_text).read_text(encoding="utf-8")
        for class_name, pattern in classes.items():
            if pattern.search(text):
                classification = "scanner_definition_or_synthetic_test" if path_text.startswith(("scripts/", "tests/")) else "unresolved"
                candidates.append({"classification": classification, "path": path_text, "privacy_class": class_name})
    confirmed = [row for row in candidates if row["classification"] == "unresolved"]
    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "owner": OWNER,
        "phase": PHASE,
        "privacy_classes": sorted(classes),
        "scanned_file_count": len(paths) - 1,
    }


def security_scan(paths: list[str]) -> dict[str, object]:
    python_paths = [path for path in paths if path.endswith(".py")]
    ast_errors: list[str] = []
    findings: list[dict[str, str]] = []
    for path_text in python_paths:
        text = (ROOT / path_text).read_text(encoding="utf-8")
        try:
            tree = ast.parse(text, filename=path_text)
        except SyntaxError:
            ast_errors.append(path_text)
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"finding": f"dynamic_{node.func.id}_call", "path": path_text})
            if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                findings.append({"finding": "subprocess_shell_true", "path": path_text})
    return {
        "ast_errors": ast_errors,
        "bounded_findings": len(findings),
        "findings": findings,
        "owner": OWNER,
        "phase": PHASE,
        "python_file_count": len(python_paths),
        "scope": "owner_source_to_final_changed_python_only",
    }


def build(status: str, test_count: int) -> None:
    require_evidence_boundary()
    x2_method = json.loads((X2 / "method-flow-ledger.json").read_text(encoding="utf-8"))
    x2_gates = json.loads((X2 / "gate-register.json").read_text(encoding="utf-8"))
    x2_evidence = json.loads((X2 / "proposal-evidence.json").read_text(encoding="utf-8"))
    if x2_method["counts"] != COUNTS or x2_evidence["outcome_counts"] != OUTCOMES:
        raise RuntimeError("x2 truth does not match final input")
    if x2_gates["open_gaps"] != 491 or x2_gates["exact_gates"] != 482:
        raise RuntimeError("x2 gate input mismatch")

    write_text(FINAL / "final-integrated-overview.md", final_overview())
    write_json(
        FINAL / "phase-truth.json",
        {
            "canonical_state": "AWAITING_EXTERNAL_EXACT_FINAL_CANONICAL",
            "counts": COUNTS,
            "declared_chain": 10250,
            "full_repository_suite_run": False,
            "outcomes": OUTCOMES,
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": 60,
            "same_owner_validation_is_independent_reproduction": False,
            "terminal_verdict": TERMINAL,
        },
    )
    final_method = dict(x2_method)
    final_method.update({"lifecycle": "exact_final_closeout", "schema": "ghc.family.method-flow.v682.v1.final"})
    write_json(FINAL / "method-flow-final.json", final_method)
    write_json(
        FINAL / "retained-negative-register.json",
        {
            "counts": COUNTS,
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "retained_mutation_failures": 300,
            "startup_and_x1_failures": x2_method["startup_and_x1_failures"],
            "x2_operational_failures": x2_method["x2_operational_failures"],
        },
    )
    write_json(FINAL / "open-gap-register.json", {"count": 491, "inherited": 488, "new": 3, "owner": OWNER, "state": "OPEN"})
    write_json(FINAL / "exact-gate-register.json", {"count": 482, "inherited": 479, "new": 3, "owner": OWNER, "state": "EXACT_GATED"})
    write_json(
        FINAL / "complete-incomplete-ledger.json",
        {
            "complete": [
                "planning-only x1 frozen and remotely equal before x2",
                "sixty synthetic contracts and 300 rejecting mutations executed",
                "twenty owner-local skills and ten runners validated and smoke-used",
                "owner-scoped evidence and closeout prepared",
            ],
            "incomplete": [
                "real specimen, taxonomic, conservation, collection-management, loan, sampling, or professional release evidence",
                "empirical GMUT confirmation",
                "real participant THOS evaluation",
                "production Freed ID lifecycle and governance",
                "legal cultural affected-party and Māori-authority decisions",
                "independent reproduction and complete repository suite",
                "Stage 20 readiness",
            ],
            "terminal_verdict": TERMINAL,
        },
    )
    write_json(
        FINAL / "lifecycle-replay.json",
        {
            "direct_edges": [[SOURCE, X1_HEAD], [X1_HEAD, EVIDENCE], [EVIDENCE, "EXTERNAL_POSTCOMMIT_FINAL"]],
            "evidence_head": EVIDENCE,
            "expected_phase_commits": 3,
            "expected_merges": 0,
            "final_parent_required": EVIDENCE,
            "immutable_x1_precommit_tests": {"passed": 18, "replayed_at_final": False},
            "initial_x2_precommit_tests": {"passed": 19, "canonical_replayed": False},
            "additive_x2_ledger_revalidation": {"passed": 19, "reason": "two retained operational failures and their count overlay were sealed before evidence commit"},
            "owner": OWNER,
            "source": SOURCE,
            "target_branch": BRANCH,
            "target_final": "EXTERNAL_POSTCOMMIT_FINAL",
            "target_final_parent_count": 1,
            "x1_head": X1_HEAD,
            "x2_canonical_replayed_at_final": False,
        },
    )
    write_json(
        FINAL / "official-source-boundary.json",
        {
            "authority_conferred": False,
            "citations_are_observations": False,
            "official_sources": ["NPS Conserve O Gram 11/8", "NPS Conserve O Grams", "TDWG standards", "Darwin Core terms", "W3C PROV-O", "WCAG 2.2", "RFC 8785", "New Zealand DOC research and collection permits", "Te Mana Raraunga principles"],
            "real_data_rows": 0,
            "real_world_actions": 0,
            "scope": "vocabulary_and_refusal_conditions_only",
        },
    )
    write_json(
        FINAL / "canonical-contract.json",
        {
            "Eiren_only_full_suite": True,
            "canonical_receipt_location": "external_to_repository",
            "exact_final_required": True,
            "full_repository_suite_authorized": False,
            "maximum_attributable_invocations": 1,
            "owner_scoped_only": True,
            "post_success_replay_permitted": False,
            "same_owner_is_independent_reproduction": False,
            "status_before_invocation": "NOT_INVOKED",
        },
    )
    write_json(
        FINAL / "terminal-checklist.json",
        {
            "canonical_external_pending": True,
            "clean_pushed_remote_equal_pending": True,
            "evidence_head": EVIDENCE,
            "full_suite_not_run": True,
            "one_final_parent_required": True,
            "owner": OWNER,
            "route_contacted": False,
            "source": SOURCE,
            "terminal_verdict": TERMINAL,
            "x1_head": X1_HEAD,
        },
    )
    write_text(HANDOFFS / "tamar-vey-v682-v2-activation-candidate.md", handoff_candidate())

    seal_targets = [
        "docs/liora-venn/v682-v1/final/final-integrated-overview.md",
        "docs/liora-venn/v682-v1/final/phase-truth.json",
        "docs/liora-venn/v682-v1/final/method-flow-final.json",
        "docs/liora-venn/v682-v1/final/retained-negative-register.json",
        "docs/liora-venn/v682-v1/final/open-gap-register.json",
        "docs/liora-venn/v682-v1/final/exact-gate-register.json",
        "docs/liora-venn/v682-v1/final/complete-incomplete-ledger.json",
        "docs/liora-venn/v682-v1/final/lifecycle-replay.json",
        "docs/liora-venn/v682-v1/final/canonical-contract.json",
        "docs/liora-venn/v682-v1/handoffs/tamar-vey-v682-v2-activation-candidate.md",
    ]
    write_json(
        CLOSEOUT / "content-seal.json",
        {
            "hash_domain": "normalized_lf_worktree_bytes",
            "owner": OWNER,
            "phase": PHASE,
            "targets": [entry(path) for path in seal_targets],
        },
    )
    write_json(VALIDATION / "final-precommit-test-receipt.json", initial_receipt(status, test_count))
    for placeholder in SELF_EXCLUSIONS:
        if not (ROOT / placeholder).exists():
            write_json(ROOT / placeholder, {"owner": OWNER, "phase": PHASE, "state": "SELF_EXCLUDED_PENDING_REGENERATION"})

    final_paths = sorted(git("ls-files", "--others", "--exclude-standard").splitlines())
    allowed_exact = {
        "scripts/build_ghc_family_liora_venn_v682_v1_final.py",
        "scripts/ghc_family_liora_venn_v682_v1_canonical.py",
        "tests/test_ghc_family_liora_venn_v682_v1_final.py",
    }
    unexpected = [path for path in final_paths if not path.startswith("docs/liora-venn/v682-v1/") and path not in allowed_exact]
    if unexpected:
        raise RuntimeError(f"unexpected untracked paths: {unexpected}")
    if any(path in final_paths for path in git("diff", "--name-only").splitlines()):
        raise RuntimeError("final paths overlap tracked modifications")
    if set(SELF_EXCLUSIONS) - set(final_paths):
        raise RuntimeError("declared final self-exclusion is missing")

    write_json(VALIDATION / "final-privacy-scan.json", privacy_scan(final_paths))
    write_json(VALIDATION / "final-security-scan.json", security_scan(final_paths))
    max_row = max(
        (
            (len((ROOT / path).read_text(encoding="utf-8").split()), path)
            for path in final_paths
            if (ROOT / path).is_file()
        ),
        default=(0, ""),
    )
    write_json(
        VALIDATION / "final-staged-review.json",
        {
            "declared_self_exclusions": SELF_EXCLUSIONS,
            "expected_paths": final_paths,
            "lifecycle": "final_closeout_only",
            "max_document_path": max_row[1],
            "max_document_words": max_row[0],
            "owner": OWNER,
            "path_count": len(final_paths),
            "phase": PHASE,
        },
    )
    final_delta_entries = [entry(path) for path in final_paths if path not in SELF_EXCLUSIONS]
    write_json(
        VALIDATION / "final-delta-manifest.json",
        {
            "declared_self_exclusions": SELF_EXCLUSIONS,
            "entries": final_delta_entries,
            "entry_count": len(final_delta_entries),
            "hash_domain": "normalized_lf_git_blob_after_stage",
            "owner": OWNER,
            "phase": PHASE,
        },
    )
    inherited_paths = git("diff", "--name-only", SOURCE, "HEAD").splitlines()
    owner_paths = sorted(set(inherited_paths + final_paths))
    owner_entries = [entry(path) for path in owner_paths if path not in SELF_EXCLUSIONS]
    write_json(
        VALIDATION / "final-owner-manifest.json",
        {
            "declared_self_exclusions": SELF_EXCLUSIONS,
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "hash_domain": "normalized_lf_git_blob_after_stage",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
        },
    )
    print(json.dumps({"final_paths": len(final_paths), "owner_entries": len(owner_entries), "status": status}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-precommit", action="store_true")
    parser.add_argument("--test-count", type=int, default=0)
    args = parser.parse_args()
    if args.record_precommit:
        if args.test_count <= 0:
            raise SystemExit("--test-count must be positive when recording precommit success")
        build("PASSED", args.test_count)
    else:
        build("PENDING", 0)


if __name__ == "__main__":
    main()
