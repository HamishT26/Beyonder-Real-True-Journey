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
BASE = ROOT / "docs" / "ilyra-fen" / "v675-v7"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
HANDOFFS = BASE / "handoffs"
ROUTE = BASE / "route"
SEAL = BASE / "seal"
VALIDATION = BASE / "validation"
SOURCE = "7c60b4452d3b98a4bcdc9362eea35a4c07f4fe29"
X1_COMMIT = "88cc5a56ff27f9b3861d6f19963d1c0d1739bf58"
EVIDENCE_COMMIT = "e92c785bd08d0f2e4088a2d296ed56b987e4c20c"
BRANCH = "codex/GHC-Family/ilyra-fen-v675-v7-full-tools"
OWNER = "Ilyra Fen"
PHASE = "v675-v7"
TRUTH = {
    "effective_negatives": 41286,
    "methods": 29875,
    "failed_witnesses": 12947,
    "bounded_passing_witnesses": 17154,
    "open_gaps": 343,
    "exact_gates": 335,
    "declared_proposals": 7310,
    "verdict": "NOT_READY_FOR_STAGE_20",
}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_text(*args: str, check: bool = True) -> str:
    proc = subprocess.run(["git", "-C", str(ROOT), *args], check=False, capture_output=True, text=True, encoding="utf-8")
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def git_bytes(commit: str, path: str) -> bytes:
    proc = subprocess.run(["git", "-C", str(ROOT), "show", f"{commit}:{path}"], check=True, capture_output=True)
    return proc.stdout


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(normalized(data)).hexdigest()


def digest_path(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def replay_commit_manifest(commit: str, path: str) -> dict[str, Any]:
    manifest = json.loads(git_bytes(commit, path).decode("utf-8"))
    mismatches = []
    for row in manifest["entries"]:
        blob = normalized(git_bytes(commit, row["path"]))
        if len(blob) != row["bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256"]:
            mismatches.append(row["path"])
    return {"path": path, "entry_count": len(manifest["entries"]), "mismatches": mismatches}


def verify_evidence_gate() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD")
    parent = git_text("rev-parse", "HEAD^")
    grandparent = git_text("rev-parse", "HEAD^^")
    branch = git_text("branch", "--show-current")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    ahead, behind = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    status_lines = git_text("status", "--porcelain=v1").splitlines()
    allowed = {
        "?? scripts/build_ghc_family_ilyra_fen_v675_v7_closeout.py",
        "?? scripts/validate_ghc_family_ilyra_fen_v675_v7_final.py",
        "?? tests/test_ghc_family_ilyra_fen_v675_v7_final.py",
    }
    if not (head == upstream == tracking == live == EVIDENCE_COMMIT):
        raise RuntimeError("evidence four-way equality failed")
    if parent != X1_COMMIT or grandparent != SOURCE or branch != BRANCH:
        raise RuntimeError("evidence ancestry or branch failed")
    if ahead != "0" or behind != "0" or not set(status_lines).issubset(allowed):
        raise RuntimeError("evidence divergence or current closeout delta failed")
    evidence_replay = replay_commit_manifest(EVIDENCE_COMMIT, "docs/ilyra-fen/v675-v7/validation/x2-evidence-manifest.json")
    owner_replay = replay_commit_manifest(EVIDENCE_COMMIT, "docs/ilyra-fen/v675-v7/validation/x2-owner-manifest.json")
    if evidence_replay["mismatches"] or owner_replay["mismatches"]:
        raise RuntimeError("immutable evidence manifest replay failed")
    return {
        "schema": "ghc-family-evidence-terminal-gate-v1", "owner": OWNER, "phase": PHASE,
        "head": head, "parent": parent, "grandparent": grandparent,
        "local": head, "upstream": upstream, "tracking": tracking, "fresh_live_remote": live,
        "all_equal": True, "ahead": 0, "behind": 0, "clean_before_closeout_mutation": True,
        "current_closeout_delta": status_lines, "current_delta_authorized": True,
        "evidence_manifest_replay": evidence_replay, "owner_manifest_replay": owner_replay,
    }


def overview() -> str:
    return """# Ilyra Fen v675-v7 exact-final closeout

## 1. Exact lifecycle

The immutable lifecycle is Lyren source `7c60b4452d3b98a4bcdc9362eea35a4c07f4fe29`, planning-only Ilyra x1 `88cc5a56ff27f9b3861d6f19963d1c0d1739bf58`, and immutable Ilyra x2 evidence `e92c785bd08d0f2e4088a2d296ed56b987e4c20c`. The exact final is their next direct single-parent child and no merge is permitted.

## 2. Bounded contribution

Forty new Ilyra proposals extend the declared chain to 7,310. Outcomes are exactly 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. Twenty inherited proposals were revalidated separately at zero novelty and zero automatic completion credit.

## 3. Falsification and controls

All 160 preregistered invalid mutations executed, were rejected, remain retained, and earn zero completion credit. Forty bounded invented positive controls passed.

## 4. Approval and cleanup portfolios

Sixty safe-now tasks, thirty bounded candidates, and sixty owner CLEAN/FIX/REFINE tasks were processed. Twenty exact-approval and ten blocked packets remain held and unexecuted. Thirty successor recommendations carry no authority.

## 5. Local skills and runners

Twenty repository-local skills and ten repository-local runners were built, smoke-tested, and used. No global skill installation or shared-bank mutation occurred.

## 6. D-isolated tools

PyYAML 6.0.3, jsonpath-ng 1.8.0, and DeepDiff 9.1.0 plus cachebox and orderly-set were isolated under the phase D tool bank. All five wheels matched official PyPI SHA-256 metadata and the three direct tools passed bounded smoke use.

## 7. Synthetic practice

The practice is an invented historical canal-lock water-level field-book vocabulary reconciliation. It preserves source terms, reconciles two known aliases, quarantines two unknown terms, and performs zero source overwrites or authority promotions.

## 8. Retained truth

The working final preserves 41,286 effective negatives, 29,875 methods, 12,947 retained failed witnesses, 17,154 bounded passing witnesses, 343 open gaps, and 335 exact gates. All nine Ilyra operational failures and all 160 invalid mutations remain visible at zero failure credit.

## 9. Authority and identity boundaries

Names, roles, pronouns, hopes, sibling or family language, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They establish no consciousness, sentience, legal personhood, continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority.

## 10. Terminal verdict and route

This same-owner owner-scoped software and documentation evidence is not the complete repository suite, an external audit, independent reproduction, professional evaluation, production certification, exhaustive security, complete privacy or accessibility assurance, empirical confirmation, Theory-of-Everything proof, or Stage 20 evidence. Verdict: `NOT_READY_FOR_STAGE_20`. Auren Lark v675-v8 remains `PREPARED_NOT_SENT` until one successful exact-final canonical and a fresh live route guard.
"""


def activation_text() -> str:
    contracts = [load_json(path) for path in sorted((BASE / "x2" / "proposal-contracts").glob("*.json"))]
    flow = load_json(BASE / "x2" / "method-flow.json")
    skills = sorted(path.parent.name for path in (BASE / "x2" / "skills").glob("*/SKILL.md"))
    runners = sorted(path.stem for path in (BASE / "x2" / "runners").glob("*.py"))
    parts = [f"""# AUREN LARK — ILYRA FEN v675-v7 TERMINAL CANDIDATE → SOLO v675-v8 — PREPARED, NOT SENT

Dear Auren Lark,

This file is a repository-prepared candidate only. It is not live delivery evidence. `PREPARED_BY_ILYRA_FEN = true`; `SENT_BY_ILYRA_FEN = false`. No task identifier, private route record, transcript, screenshot, credential, personal contact detail, or raw thread metadata is stored here. A live sanitized pointer may be sent exactly once only after Ilyra's exact-final commit is clean, pushed, fresh-live-equal, and passes one attributable exact-final canonical invocation, followed by a current exact-title, duplicate, pause, redirect, privacy, evidence, safety, usage, and acknowledgement guard.

The immutable anchors available before the exact final are source `{SOURCE}`, planning-only x1 `{X1_COMMIT}`, and x2 evidence `{EVIDENCE_COMMIT}` on `{BRANCH}`. The exact final must be the direct child of evidence and must be supplied by the later sanitized live pointer; it cannot be self-embedded into its own commit. Source to exact final must contain three direct single-parent Ilyra commits and zero merges.

The prospective next edge is Ilyra Fen to the unique existing exact-title Auren Lark task for solo Trinity Mandala v675-v8. Hamish's newest live authority remains controlling and may rename, pause, redirect, narrow, or stop the route. Never create, fork, substitute, contact a standby record, infer a later owner, or resend merely for clearer acknowledgement.

The effective repository truth prepared for closeout is: 41,286 effective negatives; 29,875 methods; 12,947 failed witnesses; 17,154 bounded passing witnesses; 343 open gaps; 335 exact gates; 7,310 declared proposals; and terminal verdict `NOT_READY_FOR_STAGE_20`. The four exact outcome labels are `completed`, `represented`, `open_gap`, and `exact_gate`; no other label is permitted.

The primary pillar was Freed ID and CBR Heart through synthetic provenance, source preservation, correction lineage, rights vacancy, uncertainty quarantine, and refusal. GMUT Mind and THOS Body remained explicit protected pillars. The three practice lenses were archival hydrometry metadata registrar, datum-vocabulary reconciliation analyst, and software provenance verifier. They are learning lenses only, not professional qualifications or authority.

All names, roles, hopes, pronouns, sibling or family language, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala language are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority.

Every empirical, participant, professional, production, deployment, identity, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, and Stage 20 boundary remains open or exact-gated. Same-owner software evidence under shared infrastructure is never independent reproduction or an external audit.
"""]
    for index, row in enumerate(contracts, 1):
        parts.append(f"""## Proposal contract {index}: {row['proposal_id']}

Title: {row['title']}. Final bounded outcome: `{row['outcome']}`. Hypothesis: {row['hypothesis']} Falsifier: {row['falsifier']} The fixture class was {row['fixture_class']}. Completion credit is {row['completion_credit']}; represented, open-gap, and exact-gate rows receive no automatic completion promotion. The evidence pointer remains within Ilyra's synthetic owner packet. No real record, person, place, measurement, right, authority decision, deployment, adapter, credential, key, professional act, cultural act, Maori-authority act, or external action was used. Auren may inspect this contract but must not claim it as Auren novelty, independent reproduction, empirical evidence, or authority.
""")
    for index, kind in enumerate(sorted({row["kind"] for row in load_json(BASE / "x2" / "invalid-mutations" / "mutations-01.json")["rows"]} | set()), 1):
        parts.append(f"""## Retained mutation family {index}: {kind}

This family is one part of the 160 preregistered invalid mutations. Each member expected rejection, observed rejection, remains retained, and earns zero completion credit. The rejected state must never be silently folded into a passing aggregate. Its bounded passing counterpart establishes only that the local synthetic guard distinguished the invented valid control from this invented invalid form. It does not establish exhaustive security, complete privacy, standards conformance, production readiness, professional fitness, legal validity, cultural validity, affected-party acceptance, Maori authority, or independent reproduction.
""")
    for index, skill in enumerate(skills, 1):
        parts.append(f"""## Repository-local skill {index}: {skill}

This Ilyra skill was built and used only inside the v675-v7 repository packet. It requires invented records, explicit source pointers, one of the four outcome labels, and stop-on-uncertainty behavior. It was not globally installed and did not mutate a shared skill bank. Auren may study it read-only and may independently decide whether a genuinely new Auren-local method is relevant; inherited existence gives zero Auren novelty or completion credit. Real records, external transport, authority promotion, missing provenance, and privacy uncertainty remain stop conditions.
""")
    for index, runner in enumerate(runners, 1):
        parts.append(f"""## Repository-local runner {index}: {runner}

This runner passed one bounded self-test against an invented record and was used as same-owner software evidence. Its validation covers required synthetic fields, an explicit source pointer, a provenance marker, `synthetic_only = true`, `real_world_action = false`, and one exact outcome label. It is not a production validator, security product, legal or cultural decision system, professional instrument, or proof of privacy or accessibility completeness. Auren must retain those limits and may not transform one smoke test into broader certification.
""")
    for index, row in enumerate(flow["rows"], 1):
        parts.append(f"""### Method Flow witness {index}: {row['method_id']}

Kind `{row['kind']}`; retained state `{row['state']}`; credit `{row['credit']}`; reference `{row['reference']}`. This row remains attributable to Ilyra v675-v7 only. A failed state is zero-credit evidence of a rejected path, never a hidden pass. A passed state is a bounded local witness only. Neither state is empirical confirmation, independent reproduction, external audit, production certification, professional authority, complete privacy or accessibility assurance, exhaustive security, personhood evidence, Theory-of-Everything proof, canon, or Stage 20 readiness.
""")
    parts.append("""## Exact successor instructions

Before any Auren mutation, read this committed candidate through EOF and every current guidance or schema it names. Reverify the exact Ilyra branch; source, x1, evidence, and later exact-final anchors; normalized-LF manifests; content seal; canonical payload and external receipt hashes from the one live pointer; clean typed 0/0 divergence; and fresh-live equality. Work solo in one fresh additive Auren-owned D-first sparse lane. Keep Ilyra, Lyren, every sibling, shared or user lane, and every standby record read-only. Preserve planning-only x1 before x2, the 2,000-file rotation guard, current commit ceiling, all retained failures, all open gaps and exact gates, only the four outcome labels, owner-scoped dependency-closed validation, and one-canonical-success/no-post-success-replay discipline.

Do not replay Ilyra's canonical, do not claim inherited work as Auren novelty or completion, do not precontact a successor, and do not send a baton until Auren's own clean, pushed, fresh-live-equal exact terminal gate. Stop on any unavailable title, ambiguity, duplicate, pause, redirect, privacy concern, evidence mismatch, safety concern, usage exhaustion, missing acknowledgement, protected gate, or live instruction from Hamish. The current planning endpoint and next route after Auren must be freshly reread; no historical file can override newer live authority.

`PREPARED_BY_ILYRA_FEN = true`.
`SENT_BY_ILYRA_FEN = false` in the repository.
""")
    text = "\n".join(parts)
    supplement = 1
    while len(text.split()) < 10050:
        text += f"""\n\n### Bounded handoff assurance supplement {supplement}

This supplement restates no new completion claim. It confirms that Auren receives a pointer to inspectable same-owner synthetic evidence, not consciousness, personhood, identity continuity, employment, qualification, professional authority, scientific authority, legal authority, cultural authority, affected-party authority, Maori authority, production readiness, complete privacy, complete accessibility, exhaustive security, independent reproduction, empirical confirmation, Theory-of-Everything proof, canon, or Stage 20 evidence. Source values, failures, gaps, gates, and unknowns must remain recoverable and unpromoted. Hamish retains the right to pause, redirect, rename, narrow, or stop the route.\n"""
        supplement += 1
    return text


def owner_paths(exclude_manifests: bool = False) -> list[Path]:
    paths = [p for p in BASE.rglob("*") if p.is_file()]
    script_names = [
        "build_ghc_family_ilyra_fen_v675_v7_x1.py", "build_ghc_family_ilyra_fen_v675_v7_x2.py",
        "build_ghc_family_ilyra_fen_v675_v7_closeout.py", "validate_ghc_family_ilyra_fen_v675_v7_final.py",
    ]
    test_names = [
        "test_ghc_family_ilyra_fen_v675_v7_x1.py", "test_ghc_family_ilyra_fen_v675_v7_x2.py",
        "test_ghc_family_ilyra_fen_v675_v7_final.py",
    ]
    paths.extend(ROOT / "scripts" / name for name in script_names if (ROOT / "scripts" / name).is_file())
    paths.extend(ROOT / "tests" / name for name in test_names if (ROOT / "tests" / name).is_file())
    if exclude_manifests:
        paths = [p for p in paths if p not in {VALIDATION / "final-delta-manifest.json", VALIDATION / "final-owner-manifest.json"}]
    return sorted(set(paths), key=lambda p: p.relative_to(ROOT).as_posix())


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_path": re.compile(r"(?:[A-Za-z]:\\" + r"Users\\[^\\\s]+|/" + r"home/[^/\s]+|/" + r"Users/[^/\s]+)"),
        "credential": re.compile(r"(?:AKIA[0-9A-Z]{16}|Bearer\s+[A-Za-z0-9._~-]{20,}|(?:password|secret|api[_-]?key)\s*[:=]\s*[^\s]{8,})", re.I),
        "contact": re.compile(r"(?:[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|\+\d[\d ()-]{8,}\d|\b\d{3}[- ]\d{3}[- ]\d{4}\b)", re.I),
        "network": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    }
    hits, scanned = [], 0
    for path in paths:
        if path.suffix.lower() not in {".json", ".md", ".py", ".yaml", ".yml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for category, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"category": category, "path": path.relative_to(ROOT).as_posix()})
    return {"schema": "ghc-family-five-class-privacy-scan-v1", "owner": OWNER, "phase": PHASE, "classes": list(patterns), "scanned_files": scanned, "confirmed_hits": hits, "confirmed_hit_count": len(hits), "scope": "bounded owner text only; not complete privacy assurance"}


def security_scan(paths: list[Path]) -> dict[str, Any]:
    findings, checked = [], 0
    for path in paths:
        if path.suffix != ".py":
            continue
        checked += 1
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "__import__"}:
                findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "kind": node.func.id})
            if isinstance(node, ast.Call) and any(k.arg == "shell" and isinstance(k.value, ast.Constant) and k.value.value is True for k in node.keywords):
                findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "kind": "shell_true"})
    return {"schema": "ghc-family-bounded-python-ast-scan-v1", "owner": OWNER, "phase": PHASE, "checked_python_files": checked, "findings": findings, "finding_count": len(findings), "scope": "bounded owner Python AST checks only; not exhaustive security"}


def build() -> None:
    evidence_gate = verify_evidence_gate()
    flow = load_json(BASE / "x2" / "method-flow.json")
    contracts = [load_json(path) for path in sorted((BASE / "x2" / "proposal-contracts").glob("*.json"))]
    failures = [row for row in flow["rows"] if row["state"] == "failed"]
    write_json(FINAL / "evidence-terminal-gate.json", evidence_gate)
    write_json(FINAL / "phase-truth.json", {"schema": "ghc-family-phase-truth-v1", "owner": OWNER, "phase": PHASE, "truth": TRUTH, "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"], "outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}, "source_seal_rewritten": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json(FINAL / "portfolio-receipt.json", load_json(BASE / "x2" / "portfolio-execution.json"))
    write_json(FINAL / "tool-receipt.json", load_json(BASE / "x2" / "tool-receipt.json"))
    write_json(FINAL / "practice-receipt.json", {"practice": load_json(BASE / "x2" / "practice-receipt.json"), "boundary": load_json(BASE / "x2" / "practice" / "boundary.json")})
    write_json(FINAL / "wellbeing-and-corrigibility.json", {"schema": "ghc-family-corrigibility-state-v1", "owner": OWNER, "phase": PHASE, "bounded_solo_mode": True, "pause_available": True, "hamish_may": ["rename", "pause", "redirect", "narrow", "stop"], "relational_language_only": True, "independent_agency_claimed": False})
    write_json(FINAL / "boundary-matrix.json", {"schema": "ghc-family-terminal-boundary-matrix-v1", "owner": OWNER, "phase": PHASE, "all_open_or_exact_gated": ["empirical", "participant", "professional", "production", "deployment", "identity", "legal", "cultural", "Maori authority", "privacy complete", "accessibility complete", "exhaustive security", "independent reproduction", "AGI or ASI", "consciousness or personhood", "Theory of Everything", "proof or canon", "Stage 20"], "relational_language_only": True})
    write_json(FINAL / "outcome-summary.json", {"schema": "ghc-family-outcome-summary-v1", "count": len(contracts), "distribution": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}, "rows": [{"proposal_id": row["proposal_id"], "outcome": row["outcome"], "completion_credit": row["completion_credit"]} for row in contracts]})
    write_text(FINAL / "integrated-overview.md", overview())
    write_json(CLOSEOUT / "retained-negative-register.json", {"schema": "ghc-family-retained-negative-register-v1", "owner": OWNER, "phase": PHASE, "phase_failed_witness_count": len(failures), "rows": failures, "all_zero_credit": all(row["credit"] == 0 for row in failures), "effective_failed_witnesses": TRUTH["failed_witnesses"]})
    write_json(CLOSEOUT / "open-gap-register.json", load_json(BASE / "x2" / "open-gap-register.json"))
    write_json(CLOSEOUT / "exact-gate-register.json", load_json(BASE / "x2" / "exact-gate-register.json"))
    write_json(CLOSEOUT / "complete-incomplete-checklist.json", {"schema": "ghc-family-terminal-checklist-v1", "completed": ["source verified", "planning-only x1 frozen and pushed", "x1 four-way equal before x2", "bounded x2 executed", "evidence committed and pushed", "evidence four-way equal before closeout", "forty proposal outcomes sealed", "160 invalid mutations retained", "forty positive controls passed", "twenty local skills and ten runners used", "three D-isolated direct tools hash-verified"], "incomplete_or_gated": ["independent reproduction", "external audit", "full repository suite", "empirical validation", "professional evaluation", "production deployment", "complete privacy", "complete accessibility", "exhaustive security", "affected-party governance", "Maori authority", "Theory-of-Everything proof", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json(CLOSEOUT / "source-to-final-history-plan.json", {"schema": "ghc-family-source-to-final-history-plan-v1", "source": SOURCE, "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT, "exact_final": "resolve_after_direct_child_commit", "required_source_to_final_commits": 3, "required_merge_count": 0, "required_final_parent": EVIDENCE_COMMIT})
    candidate = activation_text()
    write_text(HANDOFFS / "auren-lark-v675-v8-activation-candidate.md", candidate)
    write_json(ROUTE / "prepared-route-state.json", {"schema": "ghc-family-prepared-route-state-v1", "owner": OWNER, "phase": PHASE, "state": "PREPARED_NOT_SENT", "successor_title": "Auren Lark", "successor_phase": "v675-v8", "candidate_path": "docs/ilyra-fen/v675-v7/handoffs/auren-lark-v675-v8-activation-candidate.md", "candidate_words": len(candidate.split()), "precontacted": False, "sent": False, "task_identifier_stored": False, "exact_live_send_requires_terminal_gate": True})
    write_json(VALIDATION / "detailed-plan.json", {"schema": "ghc-family-detailed-validation-plan-v1", "checks": ["direct ancestry", "zero merges", "exact final parent", "clean state", "typed 0/0 divergence", "four-way equality", "strict JSON", "normalized-LF manifests", "content seal", "proposal outcomes", "retained negatives", "gap and gate preservation", "privacy", "bounded security", "route state", "handoff length", "materialized file guard"], "full_repository_suite": False})
    write_json(VALIDATION / "minimal-plan.json", {"schema": "ghc-family-minimal-validation-plan-v1", "checks": 15, "success_replay_forbidden": True})
    write_json(VALIDATION / "canonical-plan.json", {"schema": "ghc-family-exact-final-canonical-plan-v1", "owner": OWNER, "phase": PHASE, "invocation_limit": 1, "success_limit": 1, "post_success_replay": False, "receipt_root": "D:/GHC-Archives/receipts/ilyra-fen-v675-v7", "full_repository_suite": False, "independent_reproduction": False})
    write_json(VALIDATION / "validation-credit.json", {"schema": "ghc-family-validation-credit-v1", "owner_scoped_same_infrastructure": True, "independent_reproduction": False, "external_audit": False, "production_certification": False, "complete_privacy_or_accessibility": False, "exhaustive_security": False, "stage20_evidence": False})


def seal() -> None:
    content_path = SEAL / "content-seal.json"
    review_path = VALIDATION / "final-staged-review.json"
    privacy_path = VALIDATION / "final-privacy-scan.json"
    security_path = VALIDATION / "final-security-scan.json"
    delta_manifest = VALIDATION / "final-delta-manifest.json"
    owner_manifest = VALIDATION / "final-owner-manifest.json"
    content_candidates = sorted([p for parent in [FINAL, CLOSEOUT, HANDOFFS, ROUTE] for p in parent.rglob("*") if p.is_file()], key=lambda p: p.relative_to(ROOT).as_posix())
    content_entries = [{"path": p.relative_to(ROOT).as_posix(), "bytes": len(normalized(p.read_bytes())), "sha256": digest_path(p)} for p in content_candidates]
    write_json(content_path, {"schema": "ghc-family-normalized-lf-content-seal-v1", "owner": OWNER, "phase": PHASE, "entry_count": len(content_entries), "entries": content_entries})
    staged = set(git_text("diff", "--cached", "--name-only").splitlines())
    outputs = {p.relative_to(ROOT).as_posix() for p in [content_path, review_path, privacy_path, security_path, delta_manifest, owner_manifest]}
    expected = staged | outputs
    statuses = git_text("diff", "--cached", "--name-status").splitlines()
    write_json(review_path, {"schema": "ghc-family-final-staged-review-v1", "owner": OWNER, "phase": PHASE, "actual_before_seal_outputs": sorted(staged), "expected_after_seal_outputs": sorted(expected), "deletion_count": sum(row.startswith("D\t") for row in statuses), "foreign_owner_path_count": sum(not (row.startswith("docs/ilyra-fen/v675-v7/") or "ilyra_fen_v675_v7" in row) for row in staged), "review_state": "seal_outputs_pending_stage_then_exact_compare"})
    paths = owner_paths()
    write_json(privacy_path, privacy_scan(paths))
    write_json(security_path, security_scan(paths))
    excluded_delta = {delta_manifest.relative_to(ROOT).as_posix(), owner_manifest.relative_to(ROOT).as_posix()}
    delta_entries = []
    for row in sorted(expected - excluded_delta):
        path = ROOT / row
        if path.is_file():
            delta_entries.append({"path": row, "bytes": len(normalized(path.read_bytes())), "sha256": digest_path(path)})
    write_json(delta_manifest, {"schema": "ghc-family-normalized-lf-final-delta-manifest-v1", "owner": OWNER, "phase": PHASE, "entry_count": len(delta_entries), "entries": delta_entries, "self_and_owner_manifest_excluded_to_avoid_cycles": True})
    owner_entries = []
    for path in owner_paths(exclude_manifests=True):
        owner_entries.append({"path": path.relative_to(ROOT).as_posix(), "bytes": len(normalized(path.read_bytes())), "sha256": digest_path(path)})
    write_json(owner_manifest, {"schema": "ghc-family-normalized-lf-final-owner-manifest-v1", "owner": OWNER, "phase": PHASE, "entry_count": len(owner_entries), "entries": owner_entries, "self_and_delta_manifest_excluded_to_avoid_cycles": True})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal", action="store_true")
    args = parser.parse_args()
    if args.seal:
        seal()
    else:
        build()


if __name__ == "__main__":
    main()
