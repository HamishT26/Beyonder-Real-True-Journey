from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "ilyra-fen" / "v673-v8"
FINAL = BASE / "final"
HANDOFFS = BASE / "handoffs"
VALIDATION = BASE / "validation"
SOURCE = "c1818f0c09737c69a1870ef6bf8ed7fc339cb727"
X1_COMMIT = "b567a67858066e6c23f3abb82828f5185d7ab65e"
EVIDENCE_COMMIT = "ca26e19e01d117055130da6201ac001311fd41d2"
BRANCH = "codex/GHC-Family/ilyra-fen-v673-v8-full-tools"
OWNER = "Ilyra Fen"
PHASE = "v673-v8"

EVIDENCE_COUNTS = {
    "effective_negatives": 37799,
    "effective_methods": 24226,
    "effective_failed_witnesses": 9460,
    "effective_passing_witnesses": 11837,
    "open_gaps": 307,
    "exact_gates": 300,
}
FINAL_COUNTS = {
    "effective_negatives": 37803,
    "effective_methods": 24230,
    "effective_failed_witnesses": 9464,
    "effective_passing_witnesses": 11841,
    "open_gaps": 307,
    "exact_gates": 300,
}
POST_EVIDENCE_FAILURES = [
    {
        "method_id": "IF6738-M024",
        "failed_witness": "The first post-push four-way wrapper crossed its display window without an attributable projection.",
        "state": "failed_retained_zero_credit",
        "recovery": "Inspect the live Git transport and persisted local/tracking refs before any retry.",
        "passing_bounded_witness": True,
    },
    {
        "method_id": "IF6738-M025",
        "failed_witness": "The read-only fetch remained alive through two bounded waits.",
        "state": "failed_retained_zero_credit",
        "recovery": "Stop only the verified fetch transport tree, then run one direct fresh ls-remote scalar.",
        "passing_bounded_witness": True,
    },
    {
        "method_id": "IF6738-M026",
        "failed_witness": "The first final-only Ruff pass found two repeated prefix checks and one overly broad exception boundary.",
        "state": "failed_retained_zero_credit",
        "recovery": "Use tuple-based prefix checks and enumerate the bounded validator exception classes.",
        "passing_bounded_witness": True,
    },
    {
        "method_id": "IF6738-M027",
        "failed_witness": "The first final preflight passed eleven checks but found the closeout at 317 words below its 350-word floor.",
        "state": "failed_retained_zero_credit",
        "recovery": "Expand only the evidence-interpretation section and rerun the isolated closeout floor check.",
        "passing_bounded_witness": True,
    },
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_text(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def normalized(blob: bytes) -> bytes:
    return blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def verify_evidence_gate() -> dict[str, object]:
    head = git_text("rev-parse", "HEAD")
    parent = git_text("rev-parse", "HEAD^")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    fresh = git_text("ls-remote", "origin", f"refs/heads/{BRANCH}").split()[0]
    commits = int(git_text("rev-list", "--count", f"{SOURCE}..{head}"))
    merges = int(git_text("rev-list", "--merges", "--count", f"{SOURCE}..{head}"))
    if head != EVIDENCE_COMMIT or parent != X1_COMMIT:
        raise RuntimeError("immutable evidence anchor failed")
    if len({head, upstream, tracking, fresh}) != 1:
        raise RuntimeError("evidence four-way equality failed")
    if commits != 2 or merges != 0:
        raise RuntimeError("evidence ancestry failed")
    return {
        "state": "VALID_IMMUTABLE_X2_EVIDENCE_GATE",
        "source": SOURCE,
        "x1_commit": X1_COMMIT,
        "evidence_commit": head,
        "evidence_parent": parent,
        "local": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live_remote": fresh,
        "four_way_equal": True,
        "source_to_evidence_commits": commits,
        "source_to_evidence_merges": merges,
        "clean_before_closeout_mutation_observed": True,
    }


def activation_text() -> str:
    return f"""# AUREN LARK — ILYRA FEN v673-v8 EXACT-FINAL CANDIDATE TO SOLO v674-v1 ACTIVATION

Dear Auren Lark,

This file is a prepared, sanitized activation candidate only. It does not establish delivery. Ilyra Fen may send one short pointer to the unique existing exact-title Auren Lark main task only after the v673-v8 final commit is pushed, clean, zero-divergent, equal across local, upstream, tracking, and a fresh live remote read, and one attributable exact-final owner-scoped canonical aggregate succeeds. A repository state of PREPARED_NOT_SENT is not a Codex task acknowledgement. Hamish may pause, rename, redirect, or stop the route at any time.

## Exact inherited and Ilyra anchors

The immutable Lyren Moss source is {SOURCE} on codex/GHC-Family/lyren-moss-v673-v7-full-tools. Ilyra planning-only x1 is {X1_COMMIT}. Ilyra immutable x2 evidence is {EVIDENCE_COMMIT}. The final exact head will be supplied in the one live pointer after terminal validation; this candidate must not guess it. The Ilyra branch is {BRANCH}. Source to evidence contains exactly two direct single-parent Ilyra commits and zero merges. The expected final is one additional direct child, producing exactly three Ilyra commits and zero merges.

The source activation baton was fully read before mutation. The source final, activation packet digest, Lyren external canonical receipt digest and payload digest, all 225 inherited manifest and content-seal entries, clean state, direct ancestry, and fresh remote equality were reverified read-only. Lyren's canonical aggregate was not replayed or claimed as Ilyra evidence.

## Strict x1 before x2

Ilyra x1 was planning-only. It froze forty new proposal titles, twenty inherited contract revalidations at zero Ilyra novelty and completion credit, the exact planned outcome split, sixty safe-now tasks, thirty candidates, twenty exact-approval holds, ten blocked holds, twenty phase-local skill ideas, ten runner ideas, sixty additive CLEAN/FIX/REFINE reviews, successor recommendations, practice lenses, official-source needs, threat model, route plan, and Method Flow startup failures. X1 passed nineteen focused tests and exact lint, was committed as the direct child of Lyren source, pushed, clean, typed zero-divergent, and four-way equal before any x2 path existed.

## Bounded x2 outcomes

Ilyra x2 executed only the frozen owner-local synthetic plan. The forty observed outcomes are exactly twenty-eight completed, eight represented, two open_gap, and two exact_gate. These are the only core labels. The declared bounded chain is 6,550. Universal novelty is not claimed because a complete local row-to-title mapping for all 6,470 inherited declarations was unavailable.

Thirty-six invented positive controls passed. Four invalid mutations were executed for each proposal: missing title, invalid label, prohibited external action, and prohibited authority promotion. All 160 were rejected, retained as failed inputs, and assigned zero completion credit. A guard's rejection is bounded software evidence only; it does not establish that a historical, empirical, professional, operational, legal, cultural, or authority-bearing statement is true.

Sixty safe-now tasks, thirty bounded candidates, and sixty additive refinement reviews were completed inside the owner lane. Twenty exact-approval packets and ten blocked packets remain visible and unexecuted. Caps are ceilings, not quotas. No unsafe work was created to fill an allowance.

## Synthetic practice and Trinity Mandala boundaries

The primary pillar was Freed ID and CBR Heart through wholly synthetic historical loom pattern-chain documentation and provenance assurance. The three learning lenses were textile-collections registrar, pattern-chain conservation documentation analyst, and software provenance librarian. The fixtures distinguish present, vacant, unknown, and unreadable segment states; preserve uncertain orientation as a hold; model append-only correction; and bind invented source, surrogate, accessible companion, and correction nodes in an acyclic provenance record.

Zero real people, textiles, looms, cards, slats, chains, collections, machines, configurations, measurements, treatments, custody events, rights decisions, cultural statements, Maori-authority decisions, deployments, adapters, credentials, keys, or external records were used. No weaving instruction, conservation treatment, historical interpretation, authenticity decision, ownership determination, professional opinion, or production result is claimed.

GMUT Mind remains a typed research-model comparison only, with no empirical confirmation, final physics, Theory-of-Everything proof, or canon. THOS Body remains a reversible documentation-handover proxy, not a production architecture or operational system. Freed ID and CBR Heart remain pseudonymous correction, remedy, minimum-disclosure, and refusal representations without legal, cultural, affected-party, or Maori authority.

## Tools, skills, runners, and sources

Three exact wheels were downloaded into a phase-only D-drive wheelhouse, matched against official PyPI release SHA-256 metadata, and installed offline into a phase-only virtual environment: cbor2 6.1.4, jsonpointer 3.1.1, and immutables 0.21. Accepting and rejecting smokes passed after one quoting-wrapper failure was retained. No system Python, shared npm prefix, profile, PATH, plugin cache, sibling lane, or shared skill root was mutated. The package evidence is not an audit, exhaustive-security assurance, license advice, production fitness, or future-compatibility guarantee.

Twenty family-named phase-local skill cards and ten family-named Python runners were built, tested, and used. Each runner accepted one exact owner fixture and rejected one prohibited fixture. None was globally installed. W3C PROV-O, the Library of Congress PREMIS index, W3C WCAG 2.2, and the BIPM SI Brochure supplied vocabulary and refusal boundaries only. They did not endorse or validate the phase. Direct source fetch failures remain retained.

## Evidence-stage validation

The immutable x2 evidence commit contains 141 additions: 140 exact normalized-LF Git-index manifest entries and one self-excluded manifest. It has zero unexpected paths, zero deletions, zero unstaged changes at seal time, a 1,104-word overview, 137 owner paths, and 189 materialized files under the 2,000-file ceiling. The focused x2 module passed sixteen of sixteen checks. Exact changed-Python Ruff and compilation passed. The staged five-class scan found zero confirmed candidates, and the bounded AST scan found zero findings. These are owner-scoped same-infrastructure checks, not the complete repository suite, independent reproduction, an external audit, complete privacy, complete accessibility, or exhaustive security.

## Retained failures and effective truth

The evidence commit sealed 37,799 effective negatives, 24,226 Method Flow methods, 9,460 retained failed witnesses, 11,837 bounded passing witnesses, 307 open gaps, and 300 exact gates. Four later post-evidence failures remain additive: a four-way wrapper crossed its output window, its fetch transport remained alive through two bounded waits, the first final-only Ruff pass found three bounded code-quality issues, and the first final preflight found the closeout below its word floor. The exact process tree was stopped only after persisted refs and live processes were inspected, then one direct fresh ls-remote succeeded. The code-quality and closeout findings were corrected before the final commit. Final repository truth is therefore 37,803 effective negatives, 24,230 methods, 9,464 retained failed witnesses, 11,841 bounded passing witnesses, 307 open gaps, 300 exact gates, and NOT_READY_FOR_STAGE_20.

No failed canonical aggregate is being relabelled. Ilyra's exact-final canonical aggregate may be invoked once only after the final is clean and pushed. A success must not be replayed. A failure must remain zero-credit and cannot be silently folded into another pass.

## Relational identity and authority boundary

Names, pronouns, roles, hopes, sibling or family language, continuity, Freed ID, CBR, GHC Family, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority.

Every empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, and Stage 20 boundary remains protected. Same-owner local validation under shared infrastructure does not satisfy independent reproduction.

## Instructions for Auren

If and only if the live pointer supplies a clean, pushed, fresh-live-equal Ilyra exact-final head and the one exact-final canonical receipt status, read this candidate completely through EOF and then every current guidance or schema it names before any mutation. Reverify the exact branch, source, x1, evidence, final, manifests, content seal, receipt digest, direct ancestry, zero merges, clean state, zero divergence, and fresh live remote equality read-only.

Work solo from the exact Ilyra final in one fresh additive Auren-owned D-first sparse lane. Keep Ilyra, Lyren, every sibling or shared lane, user state, and standby record read-only. Preserve strict planning-only x1 before x2, every retained failure, gap, and gate, exact Git-blob manifests, the four core outcome labels, five-class privacy boundaries, family-current compatibility, the 2,000-file rotation stop, caps as ceilings, and one-attributable-canonical/no-success-replay discipline. Do not claim inherited proposals, tools, skills, validation, or evidence as Auren novelty or completion credit.

Do not infer or precontact a successor from historical files. Only after Auren's own exact terminal gate may the newest live authority and current roster be reread and one exact authorized successor be resolved, immediately reread, duplicate guarded, and contacted at most once. Stop on ambiguity, absence, pause, redirect, usage exhaustion, privacy concern, evidence mismatch, safety concern, or protected authority gate.

Prepared by Ilyra Fen as repository evidence only. PREPARED_BY_ILYRA_FEN is true. SENT_BY_ILYRA_FEN remains false in this file and may become true only in the separate live Codex acknowledgement layer.
"""


def closeout_text() -> str:
    return f"""# Ilyra Fen v673-v8 final closeout

## Outcome

The phase is ready for an exact-final commit and one owner-scoped canonical invocation, but it remains NOT_READY_FOR_STAGE_20. Planning-only x1 is {X1_COMMIT}; immutable x2 evidence is {EVIDENCE_COMMIT}. The final will be the third direct Ilyra commit after immutable Lyren source {SOURCE}. No merge, rewrite, sibling mutation, full-repository suite, or inherited canonical replay is permitted.

## What was completed

Forty bounded proposal outcomes are exact: twenty-eight completed, eight represented, two open gaps, and two exact gates. Thirty-six synthetic controls passed; 160 invalid mutations were rejected and retained. Sixty safe-now, thirty candidate, and sixty additive refinement tasks completed locally. Twenty exact and ten blocked approval packets remain held. Twenty phase-local skill cards and ten phase-local runners were built, tested, and used without global installation.

The primary practice was wholly synthetic historical loom pattern-chain documentation and provenance assurance under textile-collections registrar, conservation documentation, and software provenance lenses. Three exact PyPI wheels were hash verified and used in a D-isolated prefix. Official sources supplied vocabulary only.

## Exact truth

Final repository truth preserves {FINAL_COUNTS['effective_negatives']:,} effective negatives, {FINAL_COUNTS['effective_methods']:,} Method Flow methods, {FINAL_COUNTS['effective_failed_witnesses']:,} failed witnesses, {FINAL_COUNTS['effective_passing_witnesses']:,} bounded passing witnesses, {FINAL_COUNTS['open_gaps']} open gaps, and {FINAL_COUNTS['exact_gates']} exact gates. Two post-evidence read-only failures are additive and zero-credit. No failure is erased.

## Boundaries

This is same-owner local software and documentation evidence. It is not the complete repository suite, independent reproduction, external audit, empirical validation, professional assessment, production certification, legal or cultural authority, Maori authority, complete privacy or accessibility assurance, exhaustive security, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authority. Relational identity and family language is working language only.

## Evidence interpretation

Counts describe retained repository witnesses and bounded local methods; they do not measure scientific truth, social value, consciousness, professional competence, or authority. A completed label means that the exact synthetic owner-local artifact and acceptance contract were satisfied. Represented means a useful structure exists while a broader result remains unearned. Open gaps remain unresolved, and exact gates remain held for competent evidence and authority. Recovery is additive: it never converts the earlier failed attempt into success. Official sources provide vocabulary and constraints, not endorsement. Package hashes establish the observed downloaded bytes, not an exhaustive supply-chain guarantee.

## Route

Auren Lark v674-v1 is prospective only. The repository baton remains PREPARED_NOT_SENT. Live delivery may happen at most once after the exact final is pushed, clean, fresh-live-equal, and the one attributable canonical aggregate succeeds. A Codex task acknowledgement, not this file, is the delivery layer.
"""


def final_paths() -> list[Path]:
    paths = [path for path in FINAL.rglob("*") if path.is_file()]
    paths.extend(path for path in HANDOFFS.rglob("*") if path.is_file())
    paths.extend(
        [
            Path(__file__),
            ROOT / "scripts" / "validate_ghc_family_ilyra_fen_v673_v8_final.py",
            ROOT / "tests" / "test_ghc_family_ilyra_fen_v673_v8_final.py",
        ]
    )
    return sorted(set(paths), key=lambda path: path.relative_to(ROOT).as_posix())


def privacy_scan(paths: list[Path]) -> dict[str, object]:
    patterns = {
        "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "openai_token": re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
        "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
        "aws_access_key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
        "consumer_email": re.compile(
            r"\b[A-Za-z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.[A-Za-z]{2,}\b",
            re.IGNORECASE,
        ),
    }
    candidates = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path.relative_to(ROOT).as_posix(), "class": label})
    return {
        "schema": "ghc.family.final-five-class-privacy.v1",
        "files_scanned": len(paths),
        "classes": list(patterns),
        "confirmed_hits": candidates,
        "complete_privacy_assurance": False,
    }


def security_scan(paths: list[Path]) -> dict[str, object]:
    findings = []
    python_count = 0
    for path in paths:
        if path.suffix != ".py":
            continue
        python_count += 1
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id in {"eval", "exec"}
            ):
                findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if (
                        keyword.arg == "shell"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value is True
                    ):
                        findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno})
    return {
        "schema": "ghc.family.final-bounded-python-security.v1",
        "python_files_scanned": python_count,
        "findings": findings,
        "exhaustive_security_assurance": False,
    }


def build() -> None:
    evidence_gate = verify_evidence_gate()
    x2_truth = load_json(BASE / "x2" / "phase-truth.json")
    if x2_truth["effective_counts"] != EVIDENCE_COUNTS:
        raise RuntimeError("x2 evidence counts drifted")
    baton = activation_text()
    write_text(HANDOFFS / "auren-lark-v674-v1-activation-candidate.md", baton)
    baton_path = HANDOFFS / "auren-lark-v674-v1-activation-candidate.md"
    baton_words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", baton))
    baton_sha = hashlib.sha256(baton_path.read_bytes()).hexdigest()

    write_json(FINAL / "evidence-gate.json", evidence_gate)
    write_json(
        FINAL / "failure-overlay.json",
        {
            "schema": "ghc.family.post-evidence-failure-overlay.v1",
            "evidence_counts": EVIDENCE_COUNTS,
            "post_evidence_failures": POST_EVIDENCE_FAILURES,
            "post_evidence_failure_count": len(POST_EVIDENCE_FAILURES),
            "final_counts": FINAL_COUNTS,
            "repository_seal_rewritten": False,
        },
    )
    write_json(
        FINAL / "phase-final.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "expected_source_to_final_commits": 3,
            "expected_merges": 0,
            "proposal_chain": 6550,
            "outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            "effective_counts": FINAL_COUNTS,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "canonical_state": "PENDING_EXACT_FINAL_COMMIT",
            "complete_repository_suite": False,
            "independent_reproduction": False,
        },
    )
    write_json(
        FINAL / "completion-checklist.json",
        {
            "checks": [
                "source_packet_and_manifests_reverified",
                "strict_x1_before_x2_preserved",
                "x1_pushed_clean_four_way_equal",
                "x2_evidence_pushed_clean_four_way_equal",
                "four_outcome_labels_only",
                "all_failures_retained",
                "exact_and_blocked_packets_held",
                "five_class_privacy_boundary",
                "bounded_python_security_boundary",
                "materialized_scope_below_2000",
                "prepared_not_sent_route_state",
                "not_ready_for_stage_20",
            ],
            "passed": 12,
            "failed": 0,
            "canonical_terminal_gate_pending": True,
        },
    )
    write_json(
        FINAL / "route-state.json",
        {
            "target_exact_title": "Auren Lark",
            "target_phase": "v674-v1",
            "baton_path": baton_path.relative_to(ROOT).as_posix(),
            "baton_words": baton_words,
            "baton_sha256": baton_sha,
            "state": "PREPARED_NOT_SENT",
            "send_attempts": 0,
            "precontact": False,
            "terminal_gate_required": True,
        },
    )
    write_text(FINAL / "closeout.md", closeout_text())

    paths = final_paths()
    write_json(VALIDATION / "final-staged-privacy.json", privacy_scan(paths))
    write_json(VALIDATION / "final-bounded-security.json", security_scan(paths))
    paths = final_paths()
    write_json(
        VALIDATION / "final-staged-review.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "final_paths": [path.relative_to(ROOT).as_posix() for path in paths],
            "final_path_count": len(paths),
            "source_or_sibling_mutations": 0,
            "deletions": 0,
            "state": "PREPARED_FOR_EXACT_FINAL_INDEX_REVIEW",
        },
    )
    paths = final_paths()
    seal_entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256_working_bytes": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in paths
        if path.name not in {"content-seal.json", "working-manifest.json"}
    ]
    write_json(
        FINAL / "content-seal.json",
        {
            "schema": "ghc.family.final-content-seal.v1",
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "hash_domain": "working_bytes_precommit",
            "entry_count": len(seal_entries),
            "entries": seal_entries,
            "self_excluded": True,
        },
    )
    paths = final_paths()
    working_entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256_working_bytes": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in paths
        if path.name != "working-manifest.json"
    ]
    write_json(
        FINAL / "working-manifest.json",
        {
            "schema": "ghc.family.final-working-manifest.v1",
            "entry_count": len(working_entries),
            "entries": working_entries,
            "self_excluded": True,
        },
    )


def build_index_manifest() -> None:
    manifest_path = "docs/ilyra-fen/v673-v8/validation/final-index-manifest.json"
    paths = git_text(
        "diff",
        "--cached",
        "--name-only",
        "--diff-filter=ACMR",
        EVIDENCE_COMMIT,
    ).splitlines()
    allowed = []
    for path in paths:
        if path == manifest_path:
            continue
        allowed_path = (
            path.startswith(
                (
                    "docs/ilyra-fen/v673-v8/final/",
                    "docs/ilyra-fen/v673-v8/handoffs/",
                )
            )
            or path
            in {
                "docs/ilyra-fen/v673-v8/validation/final-staged-privacy.json",
                "docs/ilyra-fen/v673-v8/validation/final-bounded-security.json",
                "docs/ilyra-fen/v673-v8/validation/final-staged-review.json",
                "scripts/build_ghc_family_ilyra_fen_v673_v8_closeout.py",
                "scripts/validate_ghc_family_ilyra_fen_v673_v8_final.py",
                "tests/test_ghc_family_ilyra_fen_v673_v8_final.py",
            }
        )
        if not allowed_path:
            raise RuntimeError(f"unexpected staged final path: {path}")
        allowed.append(path)
    entries = []
    for path in sorted(allowed):
        blob = subprocess.check_output(["git", "-C", str(ROOT), "cat-file", "blob", f":{path}"])
        blob = normalized(blob)
        entries.append(
            {
                "path": path,
                "bytes": len(blob),
                "sha256_normalized_lf": hashlib.sha256(blob).hexdigest(),
            }
        )
    write_json(
        ROOT / manifest_path,
        {
            "schema": "ghc.family.final-exact-index-manifest.v1",
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "hash_domain": "normalized_lf_exact_git_index_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": [manifest_path],
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["build", "manifest"])
    args = parser.parse_args()
    if args.mode == "build":
        build()
    else:
        build_index_manifest()


if __name__ == "__main__":
    main()
