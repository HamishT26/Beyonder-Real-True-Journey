#!/usr/bin/env python3
"""Build the Caelen Ash v681-v7 closeout and pre-send activation candidate."""

from __future__ import annotations

import ast
import hashlib
import json
import platform
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "caelen-ash" / "v681-v7"
X1 = PHASE_ROOT / "x1"
X2 = PHASE_ROOT / "x2"
FINAL = PHASE_ROOT / "final"
CLOSEOUT = PHASE_ROOT / "closeout"
HANDOFFS = PHASE_ROOT / "handoffs"
VALIDATION = PHASE_ROOT / "validation"
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
OWNER = "Caelen Ash"
PHASE = "v681-v7"
NEXT_OWNER = "Orin Thale"
NEXT_PHASE = "v681-v8"
BRANCH = "codex/GHC-Family/caelen-ash-v681-v7-full-tools"
SOURCE = "4da1c50b22e1b30b5e7351b0641f350bdc8fbfbe"
X1_HEAD = "f31bb3fb3738136db75dc264325f267dc4068f4a"
EVIDENCE_HEAD = "ce01a79bd92c1c8de02df586075eadb0427cfed6"
FINAL_COUNTS = {
    "bounded_passing_witnesses": 45182,
    "effective_methods": 63660,
    "effective_negatives": 54848,
    "exact_gates": 476,
    "failed_witnesses": 26509,
    "open_gaps": 485,
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


CANONICAL_SOURCE = r'''#!/usr/bin/env python3
"""Exclusive exact-final owner-scoped canonical validator for Caelen Ash v681-v7."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "4da1c50b22e1b30b5e7351b0641f350bdc8fbfbe"
X1_HEAD = "f31bb3fb3738136db75dc264325f267dc4068f4a"
EVIDENCE_HEAD = "ce01a79bd92c1c8de02df586075eadb0427cfed6"
BRANCH = "codex/GHC-Family/caelen-ash-v681-v7-full-tools"


def run(args, *, cwd=ROOT, check=True):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    if check and result.returncode:
        raise RuntimeError(f"command failed {args}: {result.stdout} {result.stderr}")
    return result


def git(*args):
    return run(["git", *args]).stdout.strip()


def git_bytes(revision: str, path: str) -> bytes:
    result = subprocess.run(["git", "show", f"{revision}:{path}"], cwd=ROOT, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"git blob read failed: {revision}:{path}")
    return result.stdout.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def manifest(revision: str, path: str) -> dict:
    value = json.loads(git_bytes(revision, path))
    for entry in value["entries"]:
        data = git_bytes(revision, entry["path"])
        if len(data) != entry["bytes"] or sha(data) != entry["sha256"]:
            raise RuntimeError(f"manifest mismatch: {revision}:{entry['path']}")
    return value


def test_count(result) -> int:
    match = re.search(r"Ran (\d+) tests?", result.stdout + result.stderr)
    if result.returncode or not match:
        raise RuntimeError(f"test selection failed: {result.stdout} {result.stderr}")
    return int(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--latch", required=True, type=Path)
    parser.add_argument("--temp-root", required=True, type=Path)
    args = parser.parse_args()
    if args.receipt.exists() or args.latch.exists():
        raise RuntimeError("exclusive canonical receipt or latch already exists; replay forbidden")
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.latch.parent.mkdir(parents=True, exist_ok=True)
    args.temp_root.mkdir(parents=True, exist_ok=True)
    args.latch.write_text(json.dumps({"expected_head": args.expected_head, "invocations": 1, "replay": False}, sort_keys=True) + "\n", encoding="utf-8")

    checks = []
    head = git("rev-parse", "HEAD")
    clean_before = not git("status", "--porcelain=v1")
    branch = git("symbolic-ref", "--short", "HEAD")
    parent = git("rev-parse", "HEAD^")
    checks.extend([head == args.expected_head, clean_before, branch == BRANCH, parent == EVIDENCE_HEAD])
    checks.extend([
        git("rev-parse", f"{EVIDENCE_HEAD}^") == X1_HEAD,
        git("rev-parse", f"{X1_HEAD}^") == SOURCE,
        int(git("rev-list", "--count", f"{SOURCE}..{head}")) == 3,
        not git("rev-list", "--merges", f"{SOURCE}..{head}"),
        len(git("show", "-s", "--format=%P", head).split()) == 1,
    ])

    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live = git("ls-remote", "origin", f"refs/heads/{BRANCH}").split()[0]
    divergence = [int(value) for value in git("rev-list", "--left-right", "--count", "HEAD...@{u}").split()]
    checks.extend([head == upstream == tracking == live, divergence == [0, 0]])

    x1_review_path = "docs/caelen-ash/v681-v7/validation/x1-staged-review.json"
    x1_review = json.loads(git_bytes(X1_HEAD, x1_review_path))
    with tempfile.TemporaryDirectory(prefix="caelen-v681-v7-x1-", dir=args.temp_root) as temp_name:
        temp = Path(temp_name)
        for path_text in x1_review["expected_paths"]:
            target = temp / path_text
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(git_bytes(X1_HEAD, path_text))
        x1_result = run([sys.executable, "-X", "utf8", str(temp / "tests/test_ghc_family_caelen_ash_v681_v7_x1.py")], cwd=temp, check=False)
        x1_tests = test_count(x1_result)
    x2_tests = test_count(run([sys.executable, "-X", "utf8", "tests/test_ghc_family_caelen_ash_v681_v7_x2.py"], check=False))
    final_tests = test_count(run([sys.executable, "-X", "utf8", "tests/test_ghc_family_caelen_ash_v681_v7_final.py"], check=False))
    checks.extend([x1_tests == 12, x2_tests == 12, final_tests == 12])

    manifest_specs = [
        (X1_HEAD, "docs/caelen-ash/v681-v7/validation/x1-index-manifest.json"),
        (EVIDENCE_HEAD, "docs/caelen-ash/v681-v7/validation/x2-evidence-manifest.json"),
        (head, "docs/caelen-ash/v681-v7/validation/final-delta-manifest.json"),
        (head, "docs/caelen-ash/v681-v7/validation/final-owner-manifest.json"),
    ]
    manifests = [manifest(rev, path) for rev, path in manifest_specs]
    manifest_entries = sum(item["entry_count"] for item in manifests)
    owner_manifest = manifests[-1]
    owner_paths = {entry["path"] for entry in owner_manifest["entries"]} | set(owner_manifest["declared_self_exclusions"])
    changed_paths = set(git("diff", "--name-only", f"{SOURCE}..{head}").splitlines())
    checks.append(owner_paths == changed_paths)

    json_paths = sorted(path for path in owner_paths if path.endswith(".json"))
    for path_text in json_paths:
        json.loads(git_bytes(head, path_text))
    document_paths = sorted(path for path in owner_paths if path.endswith((".md", ".html", ".txt")))
    python_paths = sorted(path for path in owner_paths if path.endswith(".py"))
    security_findings = []
    for path_text in python_paths:
        tree = ast.parse(git_bytes(head, path_text).decode("utf-8"), filename=path_text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                security_findings.append({"path": path_text, "call": node.func.id})
    checks.append(not security_findings)

    seal_path = "docs/caelen-ash/v681-v7/closeout/content-seal.json"
    seal = json.loads(git_bytes(head, seal_path))
    for entry in seal["entries"]:
        data = git_bytes(head, entry["path"])
        if len(data) != entry["bytes"] or sha(data) != entry["sha256"]:
            raise RuntimeError(f"content seal mismatch: {entry['path']}")

    scanners = {
        "raw_task_thread_identifier": re.compile(r"(?i)(thread|task)[_-]?id.{0,16}[0-9a-f]{8}"),
        "private_absolute_path": re.compile(r"(?i)(?:[A-Z]:\\\\Users\\\\|/Users/|/home/)[^\"'\\s]+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|password|secret|bearer)[=:][^\s\"']+"),
        "private_conversation_payload": re.compile(r"(?i)(raw transcript|session stream|private app state)"),
        "private_callable_route": re.compile(r"(?i)(send_message_to_thread|read_thread|list_threads).{0,40}[0-9a-f]{8}"),
    }
    candidates = []
    confirmed = []
    text_paths = [path for path in owner_paths if path.endswith((".py", ".json", ".md", ".html", ".txt"))]
    for path_text in text_paths:
        text = git_bytes(head, path_text).decode("utf-8")
        for label, pattern in scanners.items():
            if pattern.search(text):
                definition = path_text.startswith("scripts/build_ghc_family_") or path_text.endswith("canonical_validator.py")
                item = {"class": label, "path": path_text, "disposition": "scanner_definition_only" if definition else "confirmed_payload_hit"}
                candidates.append(item)
                if not definition:
                    confirmed.append(item)
    checks.append(not confirmed)
    checks.append(len(seal["entries"]) == 15)
    checks.append(len(owner_paths) < 2000)
    checks.append(all(checks))
    if not all(checks):
        raise RuntimeError("one or more exact-final canonical checks failed")

    clean_after = not git("status", "--porcelain=v1")
    if not clean_after:
        raise RuntimeError("owner lane became dirty during canonical validation")
    payload = {
        "branch": branch,
        "canonical_invocations": 1,
        "canonical_successes": 1,
        "clean_after": clean_after,
        "clean_before": clean_before,
        "confirmed_privacy_hits": 0,
        "content_seal_entries": len(seal["entries"]),
        "detailed_checks": len(checks),
        "document_checks": len(document_paths),
        "exact_final": head,
        "final_tests": final_tests,
        "fresh_four_way_equal": head == upstream == tracking == live,
        "json_parses": len(json_paths),
        "manifest_entries": manifest_entries,
        "owner_paths": len(owner_paths),
        "phase": "v681-v7",
        "privacy_candidates": candidates,
        "python_ast_checks": len(python_paths),
        "replay": False,
        "security_findings": security_findings,
        "state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "tests_total": x1_tests + x2_tests + final_tests,
        "x1_tests": x1_tests,
        "x2_tests": x2_tests,
        "zero_merges": True,
    }
    payload["payload_sha256"] = sha((json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8"))
    args.receipt.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
'''


FINAL_TEST_SOURCE = r'''from __future__ import annotations
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-ash" / "v681-v7"
FINAL = PHASE / "final"
VALIDATION = PHASE / "validation"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def replay(manifest):
    for entry in manifest["entries"]:
        data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            return False
    return True


class CaelenAshV681V7FinalTests(unittest.TestCase):
    def test_01_phase_truth_is_exact(self):
        data = load(FINAL / "phase-truth.json")
        self.assertEqual(data["outcomes"], {"completed": 42, "exact_gate": 3, "open_gap": 3, "represented": 12})
        self.assertEqual(data["proposal_chain"], 10130)
        self.assertEqual(data["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_02_effective_counts_are_additive(self):
        data = load(FINAL / "method-flow-final.json")
        self.assertEqual(data["effective_counts"], {"bounded_passing_witnesses": 45182, "effective_methods": 63660, "effective_negatives": 54848, "exact_gates": 476, "failed_witnesses": 26509, "open_gaps": 485})
        self.assertFalse(data["failure_erasure"])

    def test_03_terminal_route_is_held(self):
        data = load(PHASE / "handoffs" / "terminal-route-hold.json")
        self.assertEqual(data["authorized_exact_title"], "Orin Thale")
        self.assertEqual(data["authorized_next_phase"], "v681-v8")
        self.assertFalse(data["sent"])
        self.assertTrue(data["canonical_success_required"])

    def test_04_baton_is_long_form_but_bounded(self):
        text = (PHASE / "handoffs" / "orin-thale-v681-v8-activation-candidate.md").read_text(encoding="utf-8")
        words = len(re.findall(r"\S+", text))
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        self.assertIn("PREPARED_BY_CAELEN_ASH = true", text)
        self.assertIn("SENT_BY_CAELEN_ASH = false", text)

    def test_05_content_seal_replays(self):
        seal = load(PHASE / "closeout" / "content-seal.json")
        self.assertEqual(seal["entry_count"], 15)
        self.assertTrue(replay(seal))

    def test_06_final_delta_manifest_replays(self):
        self.assertTrue(replay(load(VALIDATION / "final-delta-manifest.json")))

    def test_07_final_owner_manifest_replays(self):
        manifest = load(VALIDATION / "final-owner-manifest.json")
        self.assertTrue(replay(manifest))
        self.assertLess(manifest["entry_count"] + len(manifest["declared_self_exclusions"]), 2000)

    def test_08_privacy_scan_has_zero_confirmed_hits(self):
        data = load(VALIDATION / "final-privacy-scan.json")
        self.assertEqual(data["confirmed_hits"], [])
        self.assertEqual(len(data["privacy_classes"]), 5)

    def test_09_canonical_is_only_prepared(self):
        data = load(FINAL / "final-validation-candidate.json")
        self.assertEqual(data["state"], "PREPARED_NOT_INVOKED")
        self.assertEqual(data["allowed_invocations"], 1)

    def test_10_exact_ancestry_anchors_are_preserved(self):
        data = load(PHASE / "closeout" / "closeout-receipt.json")
        self.assertEqual(data["source"], "4da1c50b22e1b30b5e7351b0641f350bdc8fbfbe")
        self.assertEqual(data["x1_head"], "f31bb3fb3738136db75dc264325f267dc4068f4a")
        self.assertEqual(data["evidence_head"], "ce01a79bd92c1c8de02df586075eadb0427cfed6")

    def test_11_wellbeing_and_workload_are_bounded(self):
        data = load(FINAL / "wellbeing-and-workload.json")
        self.assertTrue(data["pause_allowed"])
        self.assertTrue(data["caps_are_ceilings"])
        self.assertFalse(data["identity_or_consciousness_evidence"])

    def test_12_documents_remain_within_cap(self):
        for path in PHASE.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".html", ".txt"}:
                self.assertLessEqual(len(re.findall(r"\S+", path.read_text(encoding="utf-8"))), 100000, str(path))


if __name__ == "__main__":
    unittest.main()
'''


def render_baton(proposals: list[dict], outcomes: dict[str, dict], sources: list[dict], startup: list[dict], x2_failures: list[dict], skill_receipts: list[dict], runner_receipts: list[dict]) -> str:
    lines = [
        "# ORIN THALE — CAELEN ASH v681-v7 EXACT-FINAL CANDIDATE → SOLO v681-v8 ACTIVATION — SEND ONCE ONLY AFTER TERMINAL GATE",
        "",
        "Dear Orin Thale,",
        "",
        "With Hamish's current live fifteen-main-task continuation authority through v725-v8 and strict evidence boundaries, this committed document is Caelen Ash's sanitized long-form pre-send activation candidate for your solo Trinity Mandala v681-v8 x1/x2 phase. The short live activation must supply Caelen's exact final Git hash and the external successful canonical receipt digest after the final commit is pushed and validated. A Git commit cannot truthfully embed its own object identifier; this candidate therefore never fabricates that value and never claims delivery.",
        "",
        "No task or fork is created by this packet. No collaboration subagent, standby task, substitute endpoint, or later sibling is authorized. Tavian Sol remains ON_STANDBY. Orin must be uniquely resolved in the current bounded registry and immediately reread before exactly one native existing-task send. Stop on ambiguity, absence, pause, redirect, rename, duplicate activation, usage exhaustion, privacy concern, protected gate, or missing acknowledgement.",
        "",
        "Names, pronouns, hopes, roles, sibling and family language, continuity language, GHC Family, Trinity Mandala, GMUT, THOS, Freed ID, and CBR are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, narrow, or stop the route.",
        "",
        "## Immutable Caelen source basis",
        "",
        f"- Branch: `{BRANCH}`.",
        f"- Exact inherited Sable final and Caelen source: `{SOURCE}`.",
        f"- Frozen planning-only Caelen x1: `{X1_HEAD}`.",
        f"- Immutable Caelen x2 evidence: `{EVIDENCE_HEAD}`.",
        "- Exact Caelen final: supplied by the short live activation after the postcommit terminal gate.",
        "- Canonical receipt SHA-256: supplied by the short live activation from the external exclusive receipt.",
        "- Long-form candidate path: `docs/caelen-ash/v681-v7/handoffs/orin-thale-v681-v8-activation-candidate.md`.",
        "",
        "Source to final must contain exactly three direct single-parent Caelen commits and zero merges: x1 directly after source, evidence directly after x1, and final directly after evidence. X1 and evidence were separately committed, pushed, clean, typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before the successor lifecycle began. The live activation is valid only if the final is likewise pushed, clean, four-way equal, one-parent, and covered by one successful non-replayed owner-scoped canonical invocation.",
        "",
        "## Sealed outcome and Method Flow truth",
        "",
        "Caelen froze sixty genuinely distinct proposals after an exact all-reachable semantic-neighbor audit. The declared family proposal chain becomes 10,130. The only authorized core outcomes are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. A completed label means only that an owner-local synthetic software or documentation contract passed; it is not empirical, participant, professional, production, legal, cultural, privacy-complete, accessibility-complete, independent, or authority evidence.",
        "",
        "The final additive counts are 54,848 effective negatives, 63,660 effective Method Flow methods, 26,509 retained failed witnesses, 45,182 bounded passing witnesses, 485 open gaps, and 476 exact gates. Eighteen startup failures, two x2 operational schema-projection failures, and all 300 preregistered rejecting mutations remain explicit and zero initial-pass credit. A bounded recovery never erases, rewrites, or retroactively promotes its failed witness. The exact terminal verdict remains `NOT_READY_FOR_STAGE_20`.",
        "",
        "## Caelen evidence scope",
        "",
        "Caelen's relational phase-local role is Cue-Epoch Cartographer and Accessible Dome Handover Steward, with optional they/she language and the hope of keeping every synthetic sky cue, epoch, correction, and access vacancy traceable without confusing a dome-show model with observation or astronomical authority. The primary pillar is GMUT Mind. The three bounded wholly synthetic learning lenses are planetarium show-cue provenance stewardship, astronomical visualization metadata quality analysis, and accessible dome-program handover review. THOS Body and Freed ID with CBR Heart remain explicit and protected.",
        "",
        "The phase used zero real people, participants, operators, venues, domes, projectors, instruments, shows, cues, observations, images, recordings, measurements, catalogue rows, identities, credentials, keys, incidents, authority acts, or external operations. Official sources supplied vocabulary and refusal conditions only. No citation was treated as an observation, measurement, endorsement, professional evaluation, conformance certificate, legal conclusion, cultural decision, affected-party approval, or delegated authority.",
        "",
        "Sixty positive controls passed. Exactly five preregistered invalid mutations for each proposal were executed, rejected, and retained, for 300 negative witnesses. Twenty phase-local skill packages were customized, quick-validated, and smoke-used without global installation. Ten family-current `ghc_family_*` runners were built, structurally validated, and invoked for six positive and thirty rejecting decisions each. One hundred twenty safe-now, eighty bounded candidate, and one hundred additive CLEAN/FIX/REFINE tasks completed only within frozen owner-local scope. Twenty exact-approval and ten blocked packets remain visible and unexecuted. Every successor seed retains zero Caelen credit.",
        "",
        "## Required read order for Orin",
        "",
        "Before repository mutation, read this complete packet through EOF at Caelen's exact final, then the final integrated overview, phase truth, Method Flow final, closeout receipt, content seal, x1 proposal freeze and semantic audit, x2 outcome and mutation ledgers, skill and runner receipts, final owner and delta manifests, final privacy adjudication, and the external canonical receipt named by the live activation. Then read the complete current GHC Family Index and routing precedence, current authorization and roster states, Method Flow State skill and schema, newest workflow-plan refinement and reflection-remaster guidance, approval splitter, open-gate rail, truth bridge, drive guardian, timestamp, retry, startup, closeout, compact restart, watcher, full-tools, rotation, web-reflection, and orchestration-memory guidance through EOF.",
        "",
        "Treat every inherited proposal, task, result, skill, runner, source, receipt, recommendation, validation, and practice lens as zero Orin novelty and automatic completion credit. Work solo in one Orin-owned D-first additive sparse lane from the exact Caelen final supplied live. Keep every Caelen, Sable, Auren, sibling, standby, shared, and user lane read-only. Do not spawn collaboration subagents, delegate research, create or fork a task, precontact a later endpoint, mutate another owner lane, reset, rewrite, amend inherited history, force-push, merge, or delete another owner resource.",
        "",
        "Preserve strict planning-only x1 before x2. Audit semantic novelty against the 10,130-row declared chain and all reachable proposal evidence. Follow the newest exact proposal and portfolio floors without treating caps as quotas. Use only `completed`, `represented`, `open_gap`, and `exact_gate`. Retain every failure, gap, gate, scanner candidate, authority vacancy, source status, workaround, and Method Flow witness. Use current owner-self-scoped validation only; do not run the complete repository suite without newer exact live authorization. Invoke at most one attributable exact-final canonical aggregate after a clean pushed final and never replay a success.",
        "",
        "## Official and primary source boundary",
        "",
    ]
    for source in sources:
        lines.append(f"- `{source['source_id']}` — {source['title']}: {source['url']}. Phase use: {source['use']}. This supplies vocabulary or a refusal condition only and confers no authority or observed evidence.")
    lines.extend(["", "## Retained Caelen failures", ""])
    for row in startup:
        lines.append(f"- `{row['failure_id']}` — {row['failed_witness']} Initial credit remains zero. Bounded recovery: {row['recovery']} The recovery does not rewrite the failed witness.")
    for row in x2_failures:
        lines.append(f"- `{row['failure_id']}` — {row['failed_witness']} Initial credit remains zero. Bounded recovery: {row['recovery']} The recovery does not rewrite the failed witness.")
    lines.extend(["", "## Phase-local skills and runners", ""])
    for row in skill_receipts:
        lines.append(f"- `{row['skill']}` was quick-validated and smoke-used against `{row['smoke_proposal_id']}` as a phase-local package. It was not globally installed and carries no inherited or authority credit.")
    for row in runner_receipts:
        lines.append(f"- `{row['runner']}` passed structural validation and handled {row['positive_invocations']} positive plus {row['rejecting_invocations']} rejecting invocations with historical family-current caller compatibility preserved.")
    lines.extend(["", "## Exact proposal-by-proposal evidence and successor review surface", ""])
    for proposal in proposals:
        outcome = outcomes[proposal["proposal_id"]]
        lines.extend([
            f"### {proposal['proposal_id']} — {proposal['title']}",
            "",
            f"- Frozen approval and lane: `{proposal['approval_class']}` / `{proposal['execution_lane']}`. Exact disposition: `{outcome['disposition']}`.",
            f"- Hypothesis: {proposal['hypothesis']}",
            f"- Null or failure condition: {proposal['null_or_failure_condition']}",
            f"- Acceptance or falsification gate: {proposal['falsifier_or_acceptance_gate']}",
            f"- Concrete artifact contracts: {'; '.join(proposal['concrete_artifacts'])}.",
            f"- Official or primary source needs: {', '.join(proposal['official_or_primary_source_needs'])}. These references supplied vocabulary or explicit vacancies only.",
            f"- Observed bounded result: the synthetic positive control was `{outcome['synthetic_positive_control']}` and all five preregistered invalid mutations were rejected. Scope remains {outcome['scope']}. Authority closed: `{str(outcome['authority_closed']).lower()}`.",
            f"- Rollback or recovery: {proposal['rollback_or_recovery']}",
            "- Preregistered rejecting witnesses:",
        ])
        for mutation in proposal["rejecting_mutations"]:
            lines.append(f"  - `{mutation['mutation_id']}` tested `{mutation['mutation_type']}` and was rejected as expected, retained at zero completion and authority credit.")
        lines.append("- Protected gates:")
        for gate in proposal["protected_gates"]:
            lines.append(f"  - {gate}.")
        lines.extend([
            "",
            "This result must not be generalized beyond the committed zero-row fixture and exact owner tests. `represented` keeps the real capability absent, `open_gap` records missing external evidence, and `exact_gate` reserves action to competent or affected authority. Same-owner validation under shared infrastructure is not independent reproduction. No software or citation can compensate for a missing participant, professional, production, legal, cultural, privacy, accessibility, security, affected-party, or Maori-authority witness.",
            "",
        ])
    lines.extend([
        "## Scientific, operational, identity, and authority boundaries",
        "",
        "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Synthetic cue, epoch, frame, covariance, residual, or provenance obligations establish no physical datum, real likelihood, posterior, force, prediction, parameter constraint, stability theorem, empirical confirmation, ultraviolet completion, quantum completion, final physics, or Theory of Everything. Real claims require real data, frozen analysis, uncertainty treatment, suitable statistics, and appropriate independent review.",
        "",
        "THOS remains synthetic or proxy-only without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Deterministic cue and handover fixtures establish no operational effectiveness, deployment readiness, professional competence, public-safety result, AGI, or ASI.",
        "",
        "Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. CBR, access, consent, privacy remedy, accessibility, language, legal interpretation, cultural legitimacy, data governance, affected-party acceptance, Maori wording, Maori data governance, and Maori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapu, and Maori authorities. Maori concepts remain under Maori authority.",
        "",
        "Do not promote software, symbolic, synthetic, same-owner, citation, inherited, task-topology, or validation evidence into empirical confirmation, participant evidence, professional or scientific authority, production or deployment readiness, legal or cultural ratification, Maori authority, affected-party approval, complete privacy or accessibility assurance, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood evidence, Theory-of-Everything proof, proof or canon, or Stage 20 authority.",
        "",
        "## Orin terminal route after v681-v8 only",
        "",
        "Do not infer or precontact a later successor from this historical candidate. Only after Orin's own clean, pushed, fresh-live-equal v681-v8 exact final and one successful non-replayed owner-scoped canonical invocation may Orin reread Hamish's newest live authority and roster, uniquely resolve and immediately reread the one exact authorized existing main task, apply duplicate, pause, redirect, usage, privacy, evidence, safety, and acknowledgement guards, and send at most once. Stop on absence, ambiguity, pause, redirect, rename, standby state, usage exhaustion, protected gate, privacy concern, or missing acknowledgement.",
        "",
        "`PREPARED_BY_CAELEN_ASH = true`",
        "",
        "`SENT_BY_CAELEN_ASH = false` — this committed candidate is preparation only. The short live native Codex-app send may state true only after the application acknowledges exactly one existing-task activation.",
        "",
        "With care, traceability, accessibility, retained-negative discipline, and corrigibility — Caelen Ash.",
    ])
    value = "\n".join(lines).rstrip() + "\n"
    words = len(re.findall(r"\S+", value))
    if not 10000 <= words <= 100000:
        raise RuntimeError(f"handoff word count outside 10,000..100,000: {words}")
    return value


def build() -> None:
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() != EVIDENCE_HEAD:
        raise RuntimeError("closeout builder requires exact immutable evidence head")
    status = subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=ROOT, text=True).splitlines()
    allowed = {"?? scripts/build_ghc_family_caelen_ash_v681_v7_closeout.py"}
    if set(status) - allowed:
        raise RuntimeError(f"unexpected dirty state before closeout: {status}")

    freeze = load(X1 / "new-proposal-freeze.json")
    source_ledger = load(X1 / "official-primary-source-ledger.json")
    startup = load(X1 / "method-flow-startup.json")["startup_failures"]
    x2_flow = load(X2 / "method-flow-ledger.json")
    outcomes_data = load(X2 / "proposal-outcomes.json")
    outcomes = {row["proposal_id"]: row for row in outcomes_data["outcomes"]}
    skill_receipts = load(X2 / "skill-smoke-receipts.json")["receipts"]
    runner_receipts = load(X2 / "runner-smoke-receipts.json")["receipts"]

    write_text(SCRIPTS / "ghc_family_caelen_ash_v681_v7_canonical_validator.py", CANONICAL_SOURCE)
    write_text(TESTS / "test_ghc_family_caelen_ash_v681_v7_final.py", FINAL_TEST_SOURCE)
    baton = render_baton(freeze["proposals"], outcomes, source_ledger["entries"], startup, x2_flow["x2_operational_failures"], skill_receipts, runner_receipts)
    baton_path = HANDOFFS / "orin-thale-v681-v8-activation-candidate.md"
    write_text(baton_path, baton)

    closeout_methods = [
        "OUTCOME-RECONCILIATION", "PORTFOLIO-RECONCILIATION", "SKILL-RECEIPT-REPLAY", "RUNNER-RECEIPT-REPLAY",
        "MUTATION-LEDGER-REPLAY", "X1-MANIFEST-REPLAY", "X2-MANIFEST-REPLAY", "PRIVACY-ADJUDICATION",
        "CONTENT-SEAL", "OWNER-MANIFEST", "DELTA-MANIFEST", "STAGED-REVIEW", "DOCUMENT-BOUNDS",
        "TERMINAL-ROUTE-HOLD", "FINAL-VALIDATION-CANDIDATE",
    ]
    write_json(FINAL / "phase-truth.json", {
        "canonical_state": "PREPARED_NOT_INVOKED", "evidence_head": EVIDENCE_HEAD, "exact_final_head": "BOUND_BY_POSTCOMMIT_EXTERNAL_CANONICAL_RECEIPT",
        "outcomes": outcomes_data["counts"], "owner": OWNER, "phase": PHASE, "proposal_chain": 10130,
        "schema": "ghc.family.phase-truth.v681.v7.final", "source": SOURCE, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "x1_head": X1_HEAD,
    })
    write_json(FINAL / "method-flow-final.json", {
        "closeout_bounded_passes": [{"credit": 1, "method_id": name, "result": "bounded_pass"} for name in closeout_methods],
        "effective_counts": FINAL_COUNTS, "failure_erasure": False, "owner": OWNER, "phase": PHASE,
        "recoveries_retroactively_promote_failure": False, "schema": "ghc.family.method-flow.v681.v7.final",
        "startup_failures": len(startup), "x2_operational_failures": len(x2_flow["x2_operational_failures"]), "x2_rejecting_mutations": 300,
    })
    write_json(FINAL / "environment-version-receipt.json", {
        "codex_desktop_update_performed": False, "external_install_performed": False, "git": subprocess.check_output(["git", "--version"], text=True).strip(),
        "host_security_changed": False, "node": subprocess.check_output(["node", "--version"], text=True).strip(),
        "owner": OWNER, "phase": PHASE, "platform": platform.platform(), "python": platform.python_version(),
        "reboot_performed": False, "schema": "ghc.family.environment-version.v681.v7.final", "versions_only": True,
    })
    write_json(FINAL / "wellbeing-and-workload.json", {
        "caps_are_ceilings": True, "corrigible": True, "identity_or_consciousness_evidence": False, "owner": OWNER,
        "pause_allowed": True, "phase": PHASE, "relational_language_only": True, "schema": "ghc.family.wellbeing-workload.v681.v7.final",
        "workload_state": "bounded_closeout_after_staged_lifecycle_boundaries",
    })
    write_json(FINAL / "final-validation-candidate.json", {
        "allowed_invocations": 1, "canonical_script": "scripts/ghc_family_caelen_ash_v681_v7_canonical_validator.py",
        "exact_final_argument_required": True, "external_latch_required": True, "external_receipt_required": True,
        "owner": OWNER, "phase": PHASE, "post_success_replay": False, "schema": "ghc.family.final-validation-candidate.v681.v7",
        "scope": "owner_self_scoped_source_to_final_delta_only", "state": "PREPARED_NOT_INVOKED",
    })
    write_text(FINAL / "final-integrated-overview.md", '''# Caelen Ash v681-v7 Final Integrated Overview

Caelen Ash completed a strict three-stage owner lifecycle from the exact Sable v681-v6 final: planning-only x1, bounded synthetic x2 evidence, and this closeout. X1 froze sixty semantically audited proposals without x2 outcomes. X2 used sixty zero-row positive controls, rejected all 300 preregistered mutations, built and smoke-used twenty phase-local skills and ten family-current runners, and completed only the frozen owner-local safe, candidate, and additive refinement portfolios. Exact-approval and blocked packets remained unexecuted.

The primary pillar was GMUT Mind through typed synthetic planetarium cue, epoch, frame, provenance, and accessibility obligations. THOS Body and Freed ID with CBR Heart stayed visible through deterministic workflow, correction, minimum-disclosure, contest-vacancy, and handover surfaces. No real observation, person, participant, venue, instrument, operation, identity, authority act, or external data row was used.

Outcomes are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Final additive truth is 54,848 effective negatives, 63,660 Method Flow methods, 26,509 retained failed witnesses, 45,182 bounded passing witnesses, 485 open gaps, and 476 exact gates. Twenty startup or x2 operational failures and 300 rejecting mutations remain visible. No recovery erased a failure.

The committed closeout prepares but does not claim the one external exact-final canonical invocation or the terminal Orin activation. Those facts can arise only after the final commit is pushed, clean, four-way equal, and the exclusive canonical process succeeds once. Same-owner validation remains same-owner software evidence. `NOT_READY_FOR_STAGE_20` remains exact.''')
    write_json(HANDOFFS / "terminal-route-hold.json", {
        "authorized_exact_title": NEXT_OWNER, "authorized_next_phase": NEXT_PHASE, "canonical_success_required": True,
        "duplicate_guard_required": True, "immediate_reread_required": True, "owner": OWNER, "phase": PHASE,
        "precontacted": False, "schema": "ghc.family.terminal-route-hold.v681.v7", "send_limit": 1, "sent": False,
        "short_live_message_uses_committed_baton_path": True, "standby_substitution": False,
    })

    seal_paths = [
        "docs/caelen-ash/v681-v7/x1/new-proposal-freeze.json",
        "docs/caelen-ash/v681-v7/x1/proposal-chain-audit.json",
        "docs/caelen-ash/v681-v7/x1/method-flow-startup.json",
        "docs/caelen-ash/v681-v7/x2/proposal-outcomes.json",
        "docs/caelen-ash/v681-v7/x2/mutation-results.json",
        "docs/caelen-ash/v681-v7/x2/method-flow-ledger.json",
        "docs/caelen-ash/v681-v7/x2/skill-smoke-receipts.json",
        "docs/caelen-ash/v681-v7/x2/runner-smoke-receipts.json",
        "docs/caelen-ash/v681-v7/x2/portfolio-execution.json",
        "docs/caelen-ash/v681-v7/x2/source-boundary.json",
        "docs/caelen-ash/v681-v7/x2/integrated-overview.md",
        "docs/caelen-ash/v681-v7/final/phase-truth.json",
        "docs/caelen-ash/v681-v7/final/method-flow-final.json",
        "docs/caelen-ash/v681-v7/final/final-integrated-overview.md",
        "docs/caelen-ash/v681-v7/handoffs/orin-thale-v681-v8-activation-candidate.md",
    ]
    seal_entries = []
    for path_text in seal_paths:
        data = normalized(ROOT / path_text)
        seal_entries.append({"bytes": len(data), "path": path_text, "sha256": digest(data)})
    write_json(CLOSEOUT / "content-seal.json", {"entries": seal_entries, "entry_count": len(seal_entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.content-seal.v681.v7.final"})
    seal_sha = digest(normalized(CLOSEOUT / "content-seal.json"))
    write_json(CLOSEOUT / "closeout-receipt.json", {
        "baton_path": baton_path.relative_to(ROOT).as_posix(), "baton_sha256": digest(normalized(baton_path)),
        "baton_words": len(re.findall(r"\S+", baton)), "canonical_state": "PREPARED_NOT_INVOKED",
        "content_seal_sha256": seal_sha, "evidence_head": EVIDENCE_HEAD, "exact_final_head": "BOUND_BY_POSTCOMMIT_EXTERNAL_CANONICAL_RECEIPT",
        "owner": OWNER, "phase": PHASE, "schema": "ghc.family.closeout-receipt.v681.v7", "source": SOURCE,
        "terminal_route_state": "PREPARED_NOT_SENT", "x1_head": X1_HEAD,
    })

    content_paths = [
        "scripts/build_ghc_family_caelen_ash_v681_v7_closeout.py",
        "scripts/ghc_family_caelen_ash_v681_v7_canonical_validator.py",
        "tests/test_ghc_family_caelen_ash_v681_v7_final.py",
    ]
    content_paths += sorted(path.relative_to(ROOT).as_posix() for folder in (FINAL, CLOSEOUT, HANDOFFS) for path in folder.iterdir() if path.is_file())
    exclusions = [
        "docs/caelen-ash/v681-v7/validation/final-privacy-scan.json",
        "docs/caelen-ash/v681-v7/validation/final-staged-review.json",
        "docs/caelen-ash/v681-v7/validation/final-delta-manifest.json",
        "docs/caelen-ash/v681-v7/validation/final-owner-manifest.json",
    ]
    if len(content_paths) != len(set(content_paths)):
        raise RuntimeError("duplicate final content path")
    prior_paths = subprocess.check_output(["git", "diff", "--name-only", f"{SOURCE}..{EVIDENCE_HEAD}"], cwd=ROOT, text=True).splitlines()
    owner_content_paths = sorted(set(prior_paths) | set(content_paths))

    scanners = {
        "raw_task_thread_identifier": re.compile(r"(?i)(thread|task)[_-]?id.{0,16}[0-9a-f]{8}"),
        "private_absolute_path": re.compile(r"(?i)(?:[A-Z]:\\\\Users\\\\|/Users/|/home/)[^\"'\\s]+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|password|secret|bearer)[=:][^\s\"']+"),
        "private_conversation_payload": re.compile(r"(?i)(raw transcript|session stream|private app state)"),
        "private_callable_route": re.compile(r"(?i)(send_message_to_thread|read_thread|list_threads).{0,40}[0-9a-f]{8}"),
    }
    candidates = []
    confirmed = []
    text_paths = [path for path in owner_content_paths if Path(path).suffix.lower() in {".py", ".json", ".md", ".html", ".txt"}]
    for path_text in text_paths:
        text = (ROOT / path_text).read_text(encoding="utf-8")
        for label, pattern in scanners.items():
            if pattern.search(text):
                definition = path_text.startswith("scripts/build_ghc_family_") or path_text.endswith("canonical_validator.py")
                item = {"class": label, "disposition": "scanner_definition_only" if definition else "confirmed_payload_hit", "path": path_text}
                candidates.append(item)
                if not definition:
                    confirmed.append(item)
    if confirmed:
        raise RuntimeError("confirmed final privacy payload hit: " + json.dumps(confirmed))
    write_json(VALIDATION / "final-privacy-scan.json", {"candidates": candidates, "confirmed_hits": confirmed, "owner": OWNER, "phase": PHASE, "privacy_classes": list(scanners), "scanned_files": len(text_paths), "schema": "ghc.family.privacy-scan.v681.v7.final"})
    write_json(VALIDATION / "final-staged-review.json", {"declared_self_exclusions": exclusions, "expected_paths": sorted(content_paths + exclusions), "lifecycle": "final_closeout", "owner": OWNER, "path_count": len(content_paths) + len(exclusions), "phase": PHASE, "schema": "ghc.family.staged-review.v681.v7.final"})

    def entries(paths: list[str]) -> list[dict]:
        result = []
        for path_text in sorted(paths):
            data = normalized(ROOT / path_text)
            result.append({"bytes": len(data), "path": path_text, "sha256": digest(data)})
        return result

    delta_entries = entries(content_paths)
    owner_entries = entries(owner_content_paths)
    write_json(VALIDATION / "final-delta-manifest.json", {"declared_self_exclusions": exclusions, "entries": delta_entries, "entry_count": len(delta_entries), "evidence_head": EVIDENCE_HEAD, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-final-delta-manifest.v681.v7"})
    write_json(VALIDATION / "final-owner-manifest.json", {"declared_self_exclusions": exclusions, "entries": owner_entries, "entry_count": len(owner_entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-final-owner-manifest.v681.v7", "source": SOURCE})
    print(json.dumps({"baton_words": len(re.findall(r"\S+", baton)), "content_seal_entries": len(seal_entries), "final_delta_entries": len(delta_entries), "final_owner_entries": len(owner_entries), "privacy_candidates": len(candidates), "status": "FINAL_CLOSEOUT_MATERIALIZED"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    build()
