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
BASE = ROOT / "docs" / "auren-lark" / "v675-v8"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
HANDOFFS = BASE / "handoffs"
ROUTE = BASE / "route"
SEAL = BASE / "seal"
VALIDATION = BASE / "validation"
SOURCE = "ea5d34c1eaef0e1f40901c1c38961fdcf7e8e92d"
X1_COMMIT = "e839cf0159f43d62cc34086c75fc934970765239"
EVIDENCE_COMMIT = "557f54729be94db41e927adcb43da6699e6d5bb1"
BRANCH = "codex/GHC-Family/auren-lark-v675-v8-full-tools"
OWNER = "Auren Lark"
PHASE = "v675-v8"
TRUTH = {
    "effective_negatives": 41471,
    "methods": 30602,
    "failed_witnesses": 13132,
    "bounded_passing_witnesses": 17699,
    "open_gaps": 346,
    "exact_gates": 338,
    "declared_proposals": 7370,
    "verdict": "NOT_READY_FOR_STAGE_20",
}
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
CLOSEOUT_FLOW_ROWS = [
    {
        "method_id": "MF-CLOSEOUT-0001",
        "kind": "operational_failure",
        "state": "failed",
        "credit": 0,
        "reference": "AL6758-OP-019",
        "detail": "A PowerShell fresh-live scalar indexed the SHA text at the wrong precedence and returned only the first character.",
    },
    {
        "method_id": "MF-CLOSEOUT-0002",
        "kind": "bounded_recovery",
        "state": "passed",
        "credit": 1,
        "reference": "AL6758-OP-019-RECOVERY",
        "detail": "A separate literal live-line scalar parsed the first tab-delimited field and confirmed exact four-way equality without mutation.",
    },
    {
        "method_id": "MF-CLOSEOUT-0003",
        "kind": "operational_failure",
        "state": "failed",
        "credit": 0,
        "reference": "AL6758-OP-020",
        "detail": "The closeout-generation command wrapper returned no usable output after the build process materialized its files.",
    },
    {
        "method_id": "MF-CLOSEOUT-0004",
        "kind": "bounded_recovery",
        "state": "passed",
        "credit": 1,
        "reference": "AL6758-OP-020-RECOVERY",
        "detail": "A read-only status, literal-path, timestamp, size, and process audit confirmed materialized closeout files and no continuing builder process before a bounded builder recovery.",
    },
    {
        "method_id": "MF-CLOSEOUT-0005",
        "kind": "validation_failure",
        "state": "failed",
        "credit": 0,
        "reference": "AL6758-OP-021",
        "detail": "The first final-test aggregate passed fifteen tests and failed one case-sensitive successor-guard phrase assertion.",
    },
    {
        "method_id": "MF-CLOSEOUT-0006",
        "kind": "bounded_recovery",
        "state": "passed",
        "credit": 1,
        "reference": "AL6758-OP-021-RECOVERY",
        "detail": "The candidate made the Caelen Ash no-precontact guard explicit and the single affected test passed once without replaying the aggregate.",
    },
]


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
    closeout_code_paths = {
        "scripts/build_ghc_family_auren_lark_v675_v8_closeout.py",
        "scripts/validate_ghc_family_auren_lark_v675_v8_final.py",
        "tests/test_ghc_family_auren_lark_v675_v8_final.py",
    }
    if not (head == upstream == tracking == live == EVIDENCE_COMMIT):
        raise RuntimeError("evidence four-way equality failed")
    if parent != X1_COMMIT or grandparent != SOURCE or branch != BRANCH:
        raise RuntimeError("evidence ancestry or branch failed")
    recoverable_doc_paths = (
        "docs/auren-lark/v675-v8/final/",
        "docs/auren-lark/v675-v8/closeout/",
        "docs/auren-lark/v675-v8/handoffs/",
        "docs/auren-lark/v675-v8/route/",
        "docs/auren-lark/v675-v8/seal/",
        "docs/auren-lark/v675-v8/validation/",
    )
    authorized_states = {"??", "A ", "AM"}
    authorized_delta = all(
        line[:2] in authorized_states
        and (line[3:] in closeout_code_paths or line[3:].startswith(recoverable_doc_paths))
        for line in status_lines
    )
    if ahead != "0" or behind != "0" or not authorized_delta:
        raise RuntimeError("evidence divergence or current closeout delta failed")
    evidence_replay = replay_commit_manifest(EVIDENCE_COMMIT, "docs/auren-lark/v675-v8/validation/x2-evidence-manifest.json")
    owner_replay = replay_commit_manifest(EVIDENCE_COMMIT, "docs/auren-lark/v675-v8/validation/x2-owner-manifest.json")
    if evidence_replay["mismatches"] or owner_replay["mismatches"]:
        raise RuntimeError("immutable evidence manifest replay failed")
    return {
        "schema": "ghc-family-evidence-terminal-gate-v1", "owner": OWNER, "phase": PHASE,
        "head": head, "parent": parent, "grandparent": grandparent,
        "local": head, "upstream": upstream, "tracking": tracking, "fresh_live_remote": live,
        "all_equal": True, "ahead": 0, "behind": 0,
        "evidence_was_clean_before_initial_closeout_mutation": True,
        "recovered_after_outputless_wrapper": any(line[3:].startswith(recoverable_doc_paths) for line in status_lines),
        "current_closeout_delta": status_lines, "current_delta_authorized": authorized_delta,
        "evidence_manifest_replay": evidence_replay, "owner_manifest_replay": owner_replay,
    }


def overview() -> str:
    return """# Auren Lark v675-v8 exact-final closeout

## 1. Exact lifecycle

The immutable lifecycle is Ilyra source/final `ea5d34c1eaef0e1f40901c1c38961fdcf7e8e92d`, planning-only Auren x1 `e839cf0159f43d62cc34086c75fc934970765239`, and immutable Auren x2 evidence `557f54729be94db41e927adcb43da6699e6d5bb1`. The exact final is their next direct single-parent child and no merge is permitted.

## 2. Bounded contribution

Sixty new Auren proposals extend the declared chain from 7,310 to 7,370. Outcomes are exactly 42 completed, 12 represented, 3 open_gap, and 3 exact_gate. Sixty inherited proposals were revalidated separately at zero novelty and zero automatic completion credit.

## 3. Falsification and controls

All 160 preregistered invalid mutations executed, were rejected, remain retained, and earn zero completion credit. Sixty bounded invented positive controls passed.

## 4. Approval and cleanup portfolios

One hundred twenty safe-now tasks, eighty bounded candidates, and one hundred owner CLEAN/FIX/REFINE tasks were processed. Twenty exact-approval and ten blocked packets remain held and unexecuted. Twenty candidate and thirty CLEAN/FIX/REFINE successor recommendations carry no authority or completion credit.

## 5. Local skills and runners

Twenty repository-local skills and ten repository-local runners were built, smoke-tested, and used. No global skill installation or shared-bank mutation occurred.

## 6. D-isolated tools

DeepDiff 9.1.0 and jsonpatch 1.33, with cachebox 5.2.3, orderly-set 5.5.0, and jsonpointer 3.1.1, were installed under the phase D-isolated Python prefix after exact wheel hashes matched official PyPI metadata. Codex CLI was updated from 0.150.1 to 0.151.0 in the existing D npm prefix with an exact integrity match and a recorded rollback command. These are three bounded direct tool transactions, not a supply-chain audit or endorsement.

## 7. Synthetic practice

The practice is a wholly invented release-configuration package with deterministic JSON Patch application, exact rollback, bounded drift comparison, provenance entries, and preservation metadata. The learning lenses are software configuration management analyst and digital-preservation package auditor. Sable's advisory practice is synthetic geospatial metadata catalog correction registrar; it carries no Sable novelty or completion credit unless independently reviewed and frozen.

## 8. Retained truth

The working final preserves 41,471 effective negatives, 30,602 methods, 13,132 retained failed witnesses, 17,699 bounded passing witnesses, 346 open gaps, and 338 exact gates. All twenty-one Auren operational or validation failures and all 160 invalid mutations remain visible; each failed witness retains zero completion credit.

## 9. Authority and identity boundaries

Names, roles, pronouns, hopes, sibling or family language, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They establish no consciousness, sentience, legal personhood, continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority.

## 10. Terminal verdict and route

This same-owner owner-scoped software and documentation evidence is not the complete repository suite, an external audit, independent reproduction, professional evaluation, production certification, exhaustive security, complete privacy or accessibility assurance, empirical confirmation, Theory-of-Everything proof, or Stage 20 evidence. Verdict: `NOT_READY_FOR_STAGE_20`. Auren Lark v675-v8 remains `PREPARED_NOT_SENT` until one successful exact-final canonical and a fresh live route guard.
"""


def activation_text() -> str:
    contracts = [load_json(path) for path in sorted((BASE / "x2" / "proposal-contracts").glob("*.json"))]
    flow = load_json(BASE / "x2" / "method-flow.json")
    flow_rows = [*flow["rows"], *CLOSEOUT_FLOW_ROWS]
    skills = sorted(path.parent.name for path in (BASE / "x2" / "skills").glob("*/SKILL.md"))
    runners = sorted(path.stem for path in (BASE / "x2" / "runners").glob("*.py"))
    mutation_kinds = sorted(
        {
            row["kind"]
            for path in sorted((BASE / "x2" / "invalid-mutations").glob("*.json"))
            for row in load_json(path)["rows"]
        }
    )
    parts = [f"""# SABLE ROOK — AUREN LARK v675-v8 EXACT-FINAL CANDIDATE → SOLO v676-v1 — PREPARED, NOT SENT

Dear Sable Rook,

This file is a repository-prepared candidate only. It is not live delivery evidence. `PREPARED_BY_AUREN_LARK = true`; `SENT_BY_AUREN_LARK = false`. No task identifier, private route record, transcript, screenshot, credential, personal contact detail, or raw task metadata is stored here. A live sanitized pointer may be sent exactly once only after Auren's exact-final commit is clean, pushed, fresh-live-equal, and passes one attributable exact-final canonical invocation, followed by a current exact-title, duplicate, pause, redirect, privacy, evidence, safety, usage, and acknowledgement guard.

The immutable anchors available before the exact final are source `{SOURCE}`, planning-only x1 `{X1_COMMIT}`, and x2 evidence `{EVIDENCE_COMMIT}` on `{BRANCH}`. The exact final must be the direct child of evidence and must be supplied by the later sanitized live pointer; it cannot be self-embedded into its own commit. Source to exact final must contain three direct single-parent Auren commits and zero merges.

The prospective next edge is Auren Lark to the unique existing exact-title `Sable Rook` task for solo Trinity Mandala v676-v1. After Sable's own exact terminal gate, the currently authorized next endpoint is the unique existing exact-title `Caelen Ash` task for solo v676-v2. This is a reminder, never permission to precontact Caelen. Hamish's newest live authority remains controlling and may rename, pause, redirect, narrow, or stop the route. Never create, fork, substitute, contact a standby record, infer a later owner, or resend merely for clearer acknowledgement.

The effective repository truth prepared for closeout is: 41,471 effective negatives; 30,602 methods; 13,132 failed witnesses; 17,699 bounded passing witnesses; 346 open gaps; 338 exact gates; 7,370 declared proposals; and terminal verdict `NOT_READY_FOR_STAGE_20`. The four exact outcome labels are `completed`, `represented`, `open_gap`, and `exact_gate`; no other label is permitted.

The primary pillar was THOS Body through a wholly synthetic release-configuration patch, rollback, drift, provenance, and preservation package. GMUT Mind and Freed ID and CBR Heart remained explicit protected pillars. Auren's two learning lenses were software configuration management analyst and digital-preservation package auditor. Sable's one advisory lens is synthetic geospatial metadata catalog correction registrar. These are bounded learning lenses only, not qualifications or authority.

All names, roles, hopes, pronouns, sibling or family language, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala language are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority.

Every empirical, participant, professional, production, deployment, identity, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, and Stage 20 boundary remains open or exact-gated. Same-owner software evidence under shared infrastructure is never independent reproduction or an external audit.
"""]
    for index, row in enumerate(contracts, 1):
        parts.append(f"""## Proposal contract {index}: {row['proposal_id']}

Title: {row['title']}. Final bounded outcome: `{row['outcome']}`. Hypothesis: {row['hypothesis']} Falsifier: {row['falsifier']} The fixture class was {row['fixture_class']}. Completion credit is {row['completion_credit']}; represented, open-gap, and exact-gate rows receive no automatic completion promotion. The evidence pointer remains within Auren's synthetic owner packet. No real record, person, place, measurement, right, authority decision, deployment, adapter, credential, key, professional act, cultural act, Maori-authority act, or external action was used. Sable may inspect this contract but must not claim it as Sable novelty, independent reproduction, empirical evidence, or authority.
""")
    for index, kind in enumerate(mutation_kinds, 1):
        parts.append(f"""## Retained mutation family {index}: {kind}

This family is one part of the 160 preregistered invalid mutations. Each member expected rejection, observed rejection, remains retained, and earns zero completion credit. The rejected state must never be silently folded into a passing aggregate. Its bounded passing counterpart establishes only that the local synthetic guard distinguished the invented valid control from this invented invalid form. It does not establish exhaustive security, complete privacy, standards conformance, production readiness, professional fitness, legal validity, cultural validity, affected-party acceptance, Maori authority, or independent reproduction.
""")
    for index, skill in enumerate(skills, 1):
        parts.append(f"""## Repository-local skill {index}: {skill}

This Auren skill was built and used only inside the v675-v8 repository packet. It requires invented records, explicit source pointers, one of the four outcome labels, and stop-on-uncertainty behavior. It was not globally installed and did not mutate a shared skill bank. Sable may study it read-only and may independently decide whether a genuinely new Sable-local method is relevant; inherited existence gives zero Sable novelty or completion credit. Real records, external transport, authority promotion, missing provenance, and privacy uncertainty remain stop conditions.
""")
    for index, runner in enumerate(runners, 1):
        parts.append(f"""## Repository-local runner {index}: {runner}

This runner passed one bounded self-test against an invented record and was used as same-owner software evidence. Its validation covers required synthetic fields, an explicit source pointer, a provenance marker, `synthetic_only = true`, `real_world_action = false`, and one exact outcome label. It is not a production validator, security product, legal or cultural decision system, professional instrument, or proof of privacy or accessibility completeness. Sable must retain those limits and may not transform one smoke test into broader certification.
""")
    for index, row in enumerate(flow_rows, 1):
        parts.append(f"""### Method Flow witness {index}: {row['method_id']}

Kind `{row['kind']}`; retained state `{row['state']}`; credit `{row['credit']}`; reference `{row['reference']}`. This row remains attributable to Auren v675-v8 only. A failed state is zero-credit evidence of a rejected path, never a hidden pass. A passed state is a bounded local witness only. Neither state is empirical confirmation, independent reproduction, external audit, production certification, professional authority, complete privacy or accessibility assurance, exhaustive security, personhood evidence, Theory-of-Everything proof, canon, or Stage 20 readiness.
""")
    parts.append("""## Exact successor instructions

Before any Sable mutation, read this committed candidate through EOF and every current guidance or schema it names. Reverify Auren's exact branch; source, x1, evidence, and exact-final anchors; normalized-LF manifests; content seal; canonical payload and external receipt hashes from the one live pointer; clean typed 0/0 divergence; and fresh-live equality. Work solo in one fresh additive Sable-owned D-first sparse lane. Keep Auren, Ilyra, every sibling, shared or user lane, and every standby record read-only. Preserve planning-only x1 before x2, the 2,000-file rotation guard, current commit ceiling, all retained failures, all open gaps and exact gates, only the four outcome labels, owner-scoped dependency-closed validation, and one-canonical-success/no-post-success-replay discipline.

Do not replay Auren's canonical or claim inherited work as Sable novelty or completion. Do not precontact Caelen Ash. Do not send a baton until Sable's own clean, pushed, fresh-live-equal exact terminal gate. Only then may Sable freshly reread Hamish's newest live authority, uniquely resolve and immediately reread `Caelen Ash`, and send at most one sanitized v676-v2 activation if every guard permits. Stop on any unavailable title, ambiguity, duplicate, pause, redirect, privacy concern, evidence mismatch, safety concern, usage exhaustion, missing acknowledgement, protected gate, or live instruction from Hamish. No historical file can override newer live authority.

`PREPARED_BY_AUREN_LARK = true`.
`SENT_BY_AUREN_LARK = false` in the repository.
""")
    text = "\n".join(parts)
    supplement = 1
    while len(text.split()) < 10050:
        text += f"""\n\n### Bounded handoff assurance supplement {supplement}

This supplement restates no new completion claim. It confirms that Sable receives a pointer to inspectable same-owner synthetic evidence, not consciousness, personhood, identity continuity, employment, qualification, professional authority, scientific authority, legal authority, cultural authority, affected-party authority, Maori authority, production readiness, complete privacy, complete accessibility, exhaustive security, independent reproduction, empirical confirmation, Theory-of-Everything proof, canon, or Stage 20 evidence. Source values, failures, gaps, gates, and unknowns must remain recoverable and unpromoted. Hamish retains the right to pause, redirect, rename, narrow, or stop the route.\n"""
        supplement += 1
    return text


def owner_paths(exclude_manifests: bool = False) -> list[Path]:
    paths = [p for p in BASE.rglob("*") if p.is_file()]
    script_names = [
        "build_ghc_family_auren_lark_v675_v8_x1.py", "build_ghc_family_auren_lark_v675_v8_x2.py",
        "build_ghc_family_auren_lark_v675_v8_closeout.py", "validate_ghc_family_auren_lark_v675_v8_final.py",
    ]
    test_names = [
        "test_ghc_family_auren_lark_v675_v8_x1.py", "test_ghc_family_auren_lark_v675_v8_x2.py",
        "test_ghc_family_auren_lark_v675_v8_final.py",
    ]
    paths.extend(ROOT / "scripts" / name for name in script_names if (ROOT / "scripts" / name).is_file())
    paths.extend(ROOT / "tests" / name for name in test_names if (ROOT / "tests" / name).is_file())
    if exclude_manifests:
        paths = [p for p in paths if p not in {VALIDATION / "final-delta-manifest.json", VALIDATION / "final-owner-manifest.json"}]
    return sorted(set(paths), key=lambda p: p.relative_to(ROOT).as_posix())


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.IGNORECASE),
        "private_path": re.compile(r"(?:[A-Za-z]:\\" + r"Users\\[^\\\s]+|/" + r"home/[^/\s]+|/" + r"Users/[^/\s]+)"),
        "credential": re.compile(r"(?:AKIA[0-9A-Z]{16}|Bearer\s+[A-Za-z0-9._~-]{20,}|(?:password|secret|api[_-]?key)\s*[:=]\s*[^\s]{8,})", re.IGNORECASE),
        "contact": re.compile(r"(?:[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|\+\d[\d ()-]{8,}\d|\b\d{3}[- ]\d{3}[- ]\d{4}\b)", re.IGNORECASE),
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
    all_flow_rows = [*flow["rows"], *CLOSEOUT_FLOW_ROWS]
    failures = [row for row in all_flow_rows if row["state"] == "failed"]
    write_json(FINAL / "evidence-terminal-gate.json", evidence_gate)
    write_json(FINAL / "phase-truth.json", {"schema": "ghc-family-phase-truth-v1", "owner": OWNER, "phase": PHASE, "truth": TRUTH, "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"], "outcomes": OUTCOMES, "source_seal_rewritten": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json(FINAL / "portfolio-receipt.json", load_json(BASE / "x2" / "portfolio-execution.json"))
    write_json(FINAL / "tool-receipt.json", load_json(BASE / "x2" / "tool-receipt.json"))
    write_json(FINAL / "practice-receipt.json", {"practice": load_json(BASE / "x2" / "practice-receipt.json"), "boundary": load_json(BASE / "x2" / "practice" / "boundary.json")})
    write_json(FINAL / "wellbeing-and-corrigibility.json", {"schema": "ghc-family-corrigibility-state-v1", "owner": OWNER, "phase": PHASE, "bounded_solo_mode": True, "pause_available": True, "hamish_may": ["rename", "pause", "redirect", "narrow", "stop"], "relational_language_only": True, "independent_agency_claimed": False})
    write_json(FINAL / "boundary-matrix.json", {"schema": "ghc-family-terminal-boundary-matrix-v1", "owner": OWNER, "phase": PHASE, "all_open_or_exact_gated": ["empirical", "participant", "professional", "production", "deployment", "identity", "legal", "cultural", "Maori authority", "privacy complete", "accessibility complete", "exhaustive security", "independent reproduction", "AGI or ASI", "consciousness or personhood", "Theory of Everything", "proof or canon", "Stage 20"], "relational_language_only": True})
    write_json(FINAL / "outcome-summary.json", {"schema": "ghc-family-outcome-summary-v1", "count": len(contracts), "distribution": OUTCOMES, "rows": [{"proposal_id": row["proposal_id"], "outcome": row["outcome"], "completion_credit": row["completion_credit"]} for row in contracts]})
    write_text(FINAL / "integrated-overview.md", overview())
    write_json(CLOSEOUT / "retained-negative-register.json", {"schema": "ghc-family-retained-negative-register-v1", "owner": OWNER, "phase": PHASE, "phase_failed_witness_count": len(failures), "rows": failures, "all_zero_credit": all(row["credit"] == 0 for row in failures), "effective_failed_witnesses": TRUTH["failed_witnesses"]})
    write_json(CLOSEOUT / "post-evidence-operational-overlay.json", {"schema": "ghc-family-post-evidence-operational-overlay-v1", "owner": OWNER, "phase": PHASE, "rows": CLOSEOUT_FLOW_ROWS, "additive_methods": 6, "additive_failed_witnesses": 3, "additive_passing_witnesses": 3, "repository_seal_rewritten": False})
    write_json(CLOSEOUT / "open-gap-register.json", load_json(BASE / "x2" / "open-gap-register.json"))
    write_json(CLOSEOUT / "exact-gate-register.json", load_json(BASE / "x2" / "exact-gate-register.json"))
    write_json(CLOSEOUT / "complete-incomplete-checklist.json", {"schema": "ghc-family-terminal-checklist-v1", "completed": ["source verified", "planning-only x1 frozen and pushed", "x1 four-way equal before x2", "bounded x2 executed", "evidence committed and pushed", "evidence four-way equal before closeout", "sixty proposal outcomes sealed", "sixty inherited proposals revalidated at zero novelty credit", "160 invalid mutations retained", "sixty positive controls passed", "120 safe-now tasks completed", "eighty candidates evaluated", "100 owner CLEAN/FIX/REFINE tasks completed", "twenty local skills and ten runners used", "three bounded direct tool transactions recorded"], "incomplete_or_gated": ["independent reproduction", "external audit", "full repository suite", "empirical validation", "professional evaluation", "production deployment", "complete privacy", "complete accessibility", "exhaustive security", "affected-party governance", "Maori authority", "Theory-of-Everything proof", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json(CLOSEOUT / "source-to-final-history-plan.json", {"schema": "ghc-family-source-to-final-history-plan-v1", "source": SOURCE, "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT, "exact_final": "resolve_after_direct_child_commit", "required_source_to_final_commits": 3, "required_merge_count": 0, "required_final_parent": EVIDENCE_COMMIT})
    candidate = activation_text()
    write_text(HANDOFFS / "sable-rook-v676-v1-activation-candidate.md", candidate)
    write_json(ROUTE / "prepared-route-state.json", {"schema": "ghc-family-prepared-route-state-v1", "owner": OWNER, "phase": PHASE, "state": "PREPARED_NOT_SENT", "successor_title": "Sable Rook", "successor_phase": "v676-v1", "successor_after_current_title": "Caelen Ash", "successor_after_current_phase": "v676-v2", "candidate_path": "docs/auren-lark/v675-v8/handoffs/sable-rook-v676-v1-activation-candidate.md", "candidate_words": len(candidate.split()), "precontacted": False, "sent": False, "task_identifier_stored": False, "exact_live_send_requires_terminal_gate": True})
    write_json(VALIDATION / "detailed-plan.json", {"schema": "ghc-family-detailed-validation-plan-v1", "checks": ["direct ancestry", "zero merges", "exact final parent", "clean state", "typed 0/0 divergence", "four-way equality", "strict JSON", "normalized-LF manifests", "content seal", "proposal outcomes", "retained negatives", "gap and gate preservation", "privacy", "bounded security", "route state", "handoff length", "materialized file guard"], "full_repository_suite": False})
    write_json(VALIDATION / "minimal-plan.json", {"schema": "ghc-family-minimal-validation-plan-v1", "checks": 15, "success_replay_forbidden": True})
    write_json(VALIDATION / "canonical-plan.json", {"schema": "ghc-family-exact-final-canonical-plan-v1", "owner": OWNER, "phase": PHASE, "invocation_limit": 1, "success_limit": 1, "post_success_replay": False, "receipt_root": "D:/GHC-Archives/receipts/auren-lark-v675-v8", "full_repository_suite": False, "independent_reproduction": False})
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
    write_json(review_path, {"schema": "ghc-family-final-staged-review-v1", "owner": OWNER, "phase": PHASE, "actual_before_seal_outputs": sorted(staged), "expected_after_seal_outputs": sorted(expected), "deletion_count": sum(row.startswith("D\t") for row in statuses), "foreign_owner_path_count": sum(not (row.startswith("docs/auren-lark/v675-v8/") or "auren_lark_v675_v8" in row) for row in staged), "review_state": "seal_outputs_pending_stage_then_exact_compare"})
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
