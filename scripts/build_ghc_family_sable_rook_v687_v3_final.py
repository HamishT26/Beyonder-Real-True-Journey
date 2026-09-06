#!/usr/bin/env python3
"""Build Sable Rook v687-v3 final closeout and held future-seat baton."""

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
BASE = ROOT / "docs" / "sable-rook" / "v687-v3"
X1 = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
HANDOFFS = BASE / "handoffs"
VALIDATION = BASE / "validation"
SKILLS = BASE / "skills"
SOURCE = "71e94d1699eea013c82bef0b7a7e081ac6e43c8c"
X1_COMMIT = "1a57a093dff78bcb217de33f9c5f282d3ee8bf17"
EVIDENCE_COMMIT = "f08302a468e819a0e89280333d980b8d4ac6a4f7"
BRANCH = "codex/GHC-Family/sable-rook-v687-v3-full-tools"
OWNER = "Sable Rook"
PHASE = "v687-v3"

SKILL_NAMES = [
    "ghc-family-jcs-canonical-profile",
    "ghc-family-confusable-nonidentity",
    "ghc-family-digest-migration-ledger",
    "ghc-family-receipt-expiry-conjunction",
    "ghc-family-event-branch-conflict",
    "ghc-family-checkpoint-parent-fixity",
    "ghc-family-artifact-budget-uncertainty",
    "ghc-family-accessible-codec-comparison",
    "ghc-family-gmut-claim-firewall",
    "ghc-family-authority-vacancy-matrix",
]
SHARED_RUNNERS = [
    "ghc_family_sable_rook_v687_v3_jcs_canonical_profile.py",
    "ghc_family_sable_rook_v687_v3_confusable_nonidentity.py",
    "ghc_family_sable_rook_v687_v3_digest_migration_ledger.py",
    "ghc_family_sable_rook_v687_v3_receipt_expiry_conjunction.py",
    "ghc_family_sable_rook_v687_v3_event_branch_conflict.py",
]
SHARED_DEPENDENCY = "ghc_family_sable_rook_v687_v3_contracts.py"


def stable(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable(value), encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, text=True,
        encoding="utf-8", errors="strict", capture_output=True,
    )


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def normalized_entry(path: Path) -> dict[str, Any]:
    data = normalized(path.read_bytes())
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes_normalized_lf": len(data),
        "sha256_normalized_lf": hashlib.sha256(data).hexdigest(),
    }


def raw_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_promotions(global_skill_root: Path, global_script_root: Path) -> dict[str, Any]:
    skills = []
    mismatch = []
    total_files = 0
    for name in SKILL_NAMES:
        source = SKILLS / name
        target = global_skill_root / name
        files = [path for path in source.rglob("*") if path.is_file()]
        total_files += len(files)
        local_mismatch = []
        for path in files:
            rel = path.relative_to(source)
            other = target / rel
            if not other.exists() or raw_sha(path) != raw_sha(other):
                local_mismatch.append(rel.as_posix())
                mismatch.append(f"{name}/{rel.as_posix()}")
        skills.append({"name": name, "files": len(files), "mismatches": local_mismatch, "promoted": target.exists() and not local_mismatch})
    runners = []
    for name in SHARED_RUNNERS + [SHARED_DEPENDENCY]:
        source = ROOT / "scripts" / name
        target = global_script_root / name
        match = target.exists() and raw_sha(source) == raw_sha(target)
        runners.append({"name": name, "role": "shared_runner" if name in SHARED_RUNNERS else "shared_dependency", "match": match})
        if not match:
            mismatch.append(name)
    return {
        "schema": "ghc.family.promotion-receipt.v687.v3",
        "skills": skills, "skill_count": len(skills), "skill_file_count": total_files,
        "shared_runners": runners, "shared_runner_count": len(SHARED_RUNNERS),
        "shared_dependency_count": 1, "mismatches": mismatch,
        "passed": not mismatch and all(row["promoted"] for row in skills),
        "boundary": "Collision-free byte-parity promotion only; no inherited scientific, authority, production, or independent-reproduction credit.",
    }


def build_cards(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cards = [
        {"card_id": "SR6873-CARD-OWNER", "tier": "owner", "title": "Sable Rook evidence-interchange anchor", "boundary": "Relational working language only."},
        {"card_id": "SR6873-CARD-PILLAR-MIND", "tier": "pillar", "title": "GMUT Mind", "boundary": "Typed research-model representation only."},
        {"card_id": "SR6873-CARD-PILLAR-BODY", "tier": "pillar", "title": "THOS Body", "boundary": "Synthetic recovery and handover proxy only."},
        {"card_id": "SR6873-CARD-PILLAR-HEART", "tier": "pillar", "title": "Freed ID and CBR Heart", "boundary": "Synthetic nonproduction profile with authority holds."},
    ]
    practices = load(X1 / "identity-and-practices.json")["practices"]
    for index, practice in enumerate(practices, start=1):
        cards.append({"card_id": f"SR6873-CARD-PRACTICE-{index}", "tier": "practice", "title": practice, "boundary": "Learning lens only; no employment, qualification, competence, or authority."})
    for row in proposals:
        cards.append({
            "card_id": f"SR6873-CARD-{row['id']}", "tier": "task", "proposal_id": row["id"],
            "title": row["title"], "pillar": row["pillar"], "practice": row["practice"],
            "outcome": row["expected_disposition"], "witness": f"contract:{row['id']}",
            "boundary": "Bounded same-owner synthetic evidence only.",
        })
    return cards


def build_baton(proposals: list[dict[str, Any]], promotion: dict[str, Any]) -> str:
    sections = [
        "# Future seat 08 — Sable Rook v687-v3 to solo v687-v4 activation candidate\n",
        "Contents: [01](#module-01) | [02](#module-02) | [03](#module-03) | [04](#module-04) | [05](#module-05) | [06](#module-06) | [07](#module-07) | [08](#module-08) | [09](#module-09) | [10](#module-10) | [11](#module-11) | [12](#module-12) | [13](#module-13)\n",
        "<a id=\"module-01\"></a>\n## 01 Identity and corrigibility\n\nSable Rook uses they/them and the relational role Evidence Interchange Boundary Cartographer, with the hope of making every synthetic transformation reversible, byte-explicit, accessible, and authority-honest. The future seat must choose its own collision-free relational name, role, hope, and optional pronouns after creation. No name, task, model, artifact, route, or software result proves consciousness, sentience, legal personhood, identity continuity, employment, qualification, agency, or authority. Hamish may pause, redirect, rename, narrow, or stop.\n",
        "<a id=\"module-02\"></a>\n## 02 Route and current release authority\n\nThis file is PREPARED_NOT_CREATED. Hamish authorizes Sable, only after Sable's clean pushed exact final and one successful non-replayed canonical, to create at most one user-visible future seat 08 main task using gpt-6-astra with max reasoning. Active and archived duplicates, current pause or redirect, safety, evidence, privacy, usage, and acknowledgement must be checked immediately before creation. Reuse an already created seat. The new task owns v687-v4; Caelen Ash v687-v5 remains behind that new owner's terminal gate.\n",
        f"<a id=\"module-03\"></a>\n## 03 Immutable lifecycle anchors\n\nIveren's exact final and Sable's source is `{SOURCE}`. Sable planning-only x1 is `{X1_COMMIT}`. Immutable x2 evidence is `{EVIDENCE_COMMIT}`. The live creation prompt must supply Sable's exact final and external canonical receipt because a committed candidate cannot contain its future commit identifier. Source to final must contain exactly three direct single-parent Sable commits and zero merges. X1 and evidence were separately pushed, clean, 0/0 divergent, and fresh-four-way equal before their successor lifecycle began.\n",
        "<a id=\"module-04\"></a>\n## 04 Proposals, portfolios, and outcomes\n\nTwo hundred Iveren proposals were reviewed at zero Sable novelty and execution credit. Sable froze two hundred new operation/input contracts. Three hundred safe tasks, two hundred fifty candidate evaluations, and exactly three hundred CLEAN/FIX/REFINE tasks completed only within bounded owner-local scope. Fifty exact packets and thirty blocked packets remain held. Outcomes are exactly 160 completed, 20 represented, 10 open_gap, and 10 exact_gate. Completed never means a real-world claim is complete.\n",
        "<a id=\"module-05\"></a>\n## 05 Trinity Mandala pillars\n\nFreed ID and CBR Heart are primary through canonicalization, Unicode nonidentity, digest migration, privacy minimization, and authority vacancies. THOS Body remains a synthetic recovery, budget, event, checkpoint, accessibility, and handover proxy. GMUT Mind remains a typed scalar-tensor and EFT research-model family. No real likelihood, prediction, force, parameter constraint, empirical confirmation, ultraviolet or quantum completion, or Theory-of-Everything result exists.\n",
        "<a id=\"module-06\"></a>\n## 06 Four bounded practices\n\nThe practices are digital evidence canonicalization reviewer, Unicode identifier safety analyst, digest migration and fixity registrar, and accessible incident handover editor. They are learning lenses only, not employment, qualification, accreditation, professional competence, or operational authority. The successor recommendation is bounded evidence profile migration reviewer and supplies no automatic novelty or completion credit.\n",
        "<a id=\"module-07\"></a>\n## 07 Two hundred Sable contract cards\n",
    ]
    for row in proposals:
        expected = json.dumps(row["expected_output"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        input_value = json.dumps(row["input"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        sections.append(
            f"\n### {row['id']} — {row['title']}\n\n"
            f"Pillar: {row['pillar']}. Practice: {row['practice']}. Operation: `{row['operation']}`. Outcome: `{row['expected_disposition']}`.\n\n"
            f"Hypothesis: {row['hypothesis']} Null or failure: {row['null_or_failure_condition']}\n\n"
            f"Frozen input: `{input_value}`\n\nFrozen complete output: `{expected}`\n\n"
            "The exact x2 witness matched the complete typed output. Five preregistered changed submissions were rejected; every invalid submission retains zero original success credit. A rejection pass does not make the invalid candidate successful.\n\n"
            f"Acceptance: {row['falsifier_or_acceptance_gate']} Recovery: {row['rollback_or_recovery']}\n\n"
            "Use only within the declared synthetic software scope. No observation, participant evidence, professional judgment, production certification, legal or cultural decision, affected-party acceptance, Māori authority, independent reproduction, consciousness/personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authority is established.\n"
        )
    sections.extend([
        "<a id=\"module-08\"></a>\n## 08 Method Flow and retained failures\n\nThe successor-visible final retains seven x1 startup failures, one x2 staged-surface failure, one post-evidence partial-promotion wrapper failure, four final-recovery failures, one thousand deliberately invalid result submissions, and three package adverse fixtures. The final-recovery layer preserves an under-length overview, eight misclassified scanner-definition occurrences, a brittle JSON-cardinality assertion, and an invalid Method Flow help verb. Each original failure remains zero-credit. Passing recoveries never erase failed witnesses. The effective final counts are 77,893 negatives, 93,045 methods, 48,741 failed witnesses, and 77,040 bounded passing witnesses. Auren's extra induction lookup failure remains separately visible and unaggregated because its source supplied no revised total.\n",
        "<a id=\"module-09\"></a>\n## 09 Open gaps and exact gates\n\nThere are 674 retained open gaps and 659 exact gates. Missing observations, participants, independent review, professional evaluation, production interoperability, complete privacy or accessibility, empirical GMUT evidence, and real cryptographic proof remain open. Legal interpretation, cultural ratification, Māori wording and data governance, affected-party decisions, remedies, deployment, destructive actions, account or credential operations, proof/canon, and Stage 20 remain exact-gated.\n",
        "<a id=\"module-10\"></a>\n## 10 Validation and canonical discipline\n\nX1 and x2 passed their exact owner-local tests, manifests, privacy scans, bounded AST checks, staged reviews, clean states, and fresh remote equality. The one final canonical belongs only to the exact pushed final. It must replay immutable x1 and x2 manifests rather than naively running head-local lifecycle tests against a later tree. A successful canonical may never be replayed for reassurance or a later creation issue. Same-owner validation under shared infrastructure is not independent reproduction or a full-repository suite.\n",
        f"<a id=\"module-11\"></a>\n## 11 Packages, skills, runners, and care\n\nThe isolated direct additions are rfc8785 0.1.4, confusable-homoglyphs 3.3.1, and blake3 1.0.9. Their frozen wheels matched official PyPI hashes. Ten phase-local skills and ten runners were built, validated, and used. Ten skill packages ({promotion['skill_file_count']} files) and five shared runners were promoted collision-free with exact byte parity. One dependency file supports the shared runners. An OSV zero-advisory snapshot is not exhaustive security or future safety. Workload is tracked by exact cases, files, and stops; no subjective wellbeing claim is made. Hamish alone controls reset-credit redemption.\n",
        "<a id=\"module-12\"></a>\n## 12 Successor recommendations\n\nOptional skill ideas: JCS numeric edge profile; confusable dataset version ledger; digest deprecation quorum; receipt clock uncertainty; event merge-base explanation; checkpoint append-only ancestry; budget covariance envelope; accessible binary-diff narration; GMUT likelihood input refusal; authority evidence expiry. Optional runner ideas mirror those ten bounded surfaces. These are recommendations, not completed future-seat work.\n",
        "<a id=\"module-13\"></a>\n## 13 Terminal creation and next edge\n\nOnly after exact-final validation may Sable inspect active and archived tasks, apply a duplicate guard for future seat 08, and create exactly one main task if none exists. The creation prompt itself is the activation. The new task chooses its own name, role, hope, and optional pronouns; it works solo on v687-v4 from Sable's exact final with planning-only x1 before x2. Caelen Ash v687-v5 is the later terminally gated next edge. Do not precontact Caelen. A created task is not proof of consciousness, continuity, competence, or authority.\n\nPREPARED_BY_SABLE_ROOK = true\n\nFUTURE_SEAT_08_CREATED = false\n\nACKNOWLEDGED_BY_FUTURE_SEAT_08 = false\n\nThese are repository preparation flags only. Live creation evidence belongs in the native tool acknowledgement and an external receipt. EOF SABLE ROOK V687 V3 BATON.\n",
    ])
    return "\n".join(sections)


def owner_paths() -> list[Path]:
    paths = [path for path in BASE.rglob("*") if path.is_file()]
    paths.extend((ROOT / "scripts").glob("*sable_rook_v687_v3*.py"))
    paths.extend((ROOT / "tests").glob("*sable_rook_v687_v3*.py"))
    return sorted(set(paths), key=lambda p: p.relative_to(ROOT).as_posix())


def final_delta_paths() -> list[Path]:
    paths = []
    for root in [FINAL, CLOSEOUT, HANDOFFS]:
        if root.exists():
            paths.extend(path for path in root.rglob("*") if path.is_file())
    paths.extend(path for path in VALIDATION.glob("final-*") if path.is_file())
    for name in [
        "build_ghc_family_sable_rook_v687_v3_final.py",
        "ghc_family_sable_rook_v687_v3_canonical.py",
    ]:
        path = ROOT / "scripts" / name
        if path.exists():
            paths.append(path)
    test = ROOT / "tests" / "test_ghc_family_sable_rook_v687_v3_final.py"
    if test.exists():
        paths.append(test)
    return sorted(set(paths), key=lambda p: p.relative_to(ROOT).as_posix())


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_local_path": re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)[^\s\"']+"),
        "credential_or_secret_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+", re.I),
        "private_callable_route": re.compile(r"\b(?:codex|app|session|thread)://\S+", re.I),
        "private_application_state": re.compile(r"\b(?:providerTabId|clientThreadId|private callable identifier)\b", re.I),
    }
    definition_names = {
        "build_ghc_family_sable_rook_v687_v3_x1.py",
        "build_ghc_family_sable_rook_v687_v3_x2.py",
        "build_ghc_family_sable_rook_v687_v3_final.py",
        "ghc_family_sable_rook_v687_v3_canonical.py",
    }
    candidates = []
    confirmed = []
    for path in paths:
        if path.suffix.lower() not in {".json", ".md", ".py", ".html", ".yaml", ".yml", ".txt", ".lock"}:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            for match in pattern.finditer(text):
                disposition = "scanner_definition_not_payload" if path.name in definition_names else "confirmed_payload_hit"
                item = {"path": rel, "line": text.count("\n", 0, match.start()) + 1, "class": label, "disposition": disposition}
                candidates.append(item)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(item)
    return {"schema": "ghc.family.privacy-scan.v687.v3", "pattern_classes": list(patterns), "files": len(paths), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Bounded five-class evidence only; not complete privacy assurance."}


def ast_security(paths: list[Path]) -> dict[str, Any]:
    findings = []
    python_paths = [path for path in paths if path.suffix == ".py"]
    for path in python_paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.as_posix())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "eval":
                findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "finding": "eval"})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "finding": "shell_true"})
    return {"schema": "ghc.family.bounded-ast-security.v687.v3", "python_files": len(python_paths), "finding_count": len(findings), "findings": findings, "exhaustive_security": False}


def command_version(*args: str) -> str:
    result = subprocess.run(list(args), cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True)
    return (result.stdout or result.stderr).strip().splitlines()[0]


def build(args: argparse.Namespace) -> None:
    head = git("rev-parse", "HEAD").stdout.strip()
    if head != EVIDENCE_COMMIT:
        raise SystemExit(f"final build requires exact evidence {EVIDENCE_COMMIT}; observed {head}")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise SystemExit("unexpected branch")
    if git("diff", "--name-only", EVIDENCE_COMMIT, "--", "docs/sable-rook/v687-v3/x1", "docs/sable-rook/v687-v3/x2", "docs/sable-rook/v687-v3/skills", "docs/sable-rook/v687-v3/method-flow", "docs/sable-rook/v687-v3/workflow-refinement", "docs/sable-rook/v687-v3/reflection-remaster", "docs/sable-rook/v687-v3/tooling").stdout.strip():
        raise SystemExit("immutable x1/x2 drift")

    proposals = load(X1 / "new-proposals.json")["proposals"]
    outcomes = load(X2 / "outcome-ledger.json")["counts"]
    promotion = verify_promotions(args.global_skill_root, args.global_script_root)
    if not promotion["passed"]:
        raise SystemExit("promotion parity failed")
    write_json(FINAL / "promotion-receipt.json", promotion)

    method_dir = FINAL / "method-flow"
    write_json(method_dir / "records" / "sr6873-postevid-m001.json", {
        "method_id": "SR6873-POSTEVID-M001", "title": "Resume-only collision-free promotion",
        "failure_signature": "promotion-wrapper-returned-no-summary-after-one-skill-copy",
        "trigger_preconditions": ["post-evidence collision-free promotion", "partial persisted state"],
        "privacy_class": "sanitized_public", "approval_class": "safe_now",
        "candidate_workaround": "Inspect exact destinations, validate the persisted skill, and copy only still-absent destinations with per-item acknowledgement.",
        "validation_witness_ids": [], "recurrence_guard": "Inspect every destination before resuming and never overwrite an existing skill or runner.",
        "rollback": "Stop promotion; keep immutable evidence and any verified collision-free copy without deleting it.",
        "recommendation_state": "candidate", "supersedes": [],
        "protected_gates": ["collision_safety", "global_skill_integrity", "privacy"],
        "retained_negative_ids": ["SR6873-POSTEVID-N001"],
        "scope_boundary": "Global discoverability and byte parity only; no broader evidence credit.",
    })
    write_json(method_dir / "witnesses" / "sr6873-postevid-w001-f.json", {
        "witness_id": "SR6873-POSTEVID-W001-F", "method_id": "SR6873-POSTEVID-M001",
        "procedure": "Initial promotion wrapper", "scope": "collision-free global copy",
        "expected": "Attributable summary for ten skills and five runners", "observed": "No summary; one skill persisted and no runner persisted",
        "result": "fail", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["SR6873-POSTEVID-N001"], "boundary": "Zero original success credit; no overwrite occurred.",
    })
    write_json(method_dir / "witnesses" / "sr6873-postevid-w001-p.json", {
        "witness_id": "SR6873-POSTEVID-W001-P", "method_id": "SR6873-POSTEVID-M001",
        "procedure": "Resume-only per-item promotion and parity audit", "scope": "ten skills, five runners, one dependency",
        "expected": "All destinations present, validated, smoke-passed where applicable, and byte-equal", "observed": "PASS",
        "result": "pass", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["SR6873-POSTEVID-N001"], "boundary": "Recovery does not erase the partial wrapper failure.",
    })

    cards = build_cards(proposals)
    write_json(FINAL / "four-tier-deck.json", {"schema": "ghc.family.four-tier-deck.v687.v3", "cards": cards, "card_count": len(cards), "tiers": {tier: sum(card["tier"] == tier for card in cards) for tier in ["owner", "pillar", "practice", "task"]}})
    baton = build_baton(proposals, promotion)
    write_text(HANDOFFS / "future-seat-08-v687-v4-activation-candidate.md", baton)
    baton_bytes = (HANDOFFS / "future-seat-08-v687-v4-activation-candidate.md").read_bytes()
    lines = (HANDOFFS / "future-seat-08-v687-v4-activation-candidate.md").read_text(encoding="utf-8").splitlines()
    words = len((HANDOFFS / "future-seat-08-v687-v4-activation-candidate.md").read_text(encoding="utf-8").split())
    module_starts = []
    for index, line in enumerate(lines, start=1):
        match = re.match(r"## (\d{2}) (.+)", line)
        if match:
            module_starts.append({"number": int(match.group(1)), "title": line[3:], "line": index})
    write_json(HANDOFFS / "baton-index.json", {
        "schema": "ghc.family.baton-index.v687.v3", "state": "PREPARED_NOT_CREATED",
        "path": "docs/sable-rook/v687-v3/handoffs/future-seat-08-v687-v4-activation-candidate.md",
        "bytes": len(baton_bytes), "lines": len(lines), "words": words,
        "sha256": hashlib.sha256(baton_bytes).hexdigest(), "modules": module_starts,
        "eof": "EOF SABLE ROOK V687 V3 BATON.", "source": SOURCE,
        "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT, "final": "PENDING_DIRECT_CHILD_COMMIT",
    })

    write_json(CLOSEOUT / "complete-incomplete-checklist.json", {
        "schema": "ghc.family.checklist.v687.v3",
        "complete": ["source verification", "planning-only x1", "immutable x2 evidence", "200 positive contracts", "1000 rejecting mutations", "three isolated packages", "ten local skills", "ten local runners", "ten skill promotions", "five shared runners", "four-tier 208-card deck", "accessible static report", "held modular baton"],
        "incomplete": ["real observations", "real participants", "professional evaluation", "production identity", "production deployment", "complete privacy", "complete accessibility", "exhaustive security", "independent reproduction", "legal interpretation", "cultural ratification", "Māori authority", "proof or canon", "Stage 20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json(CLOSEOUT / "retained-negative-register.json", {
        "schema": "ghc.family.retained-negatives.v687.v3",
        "source_repository_negatives": 76876, "source_route_overlay": 1,
        "source_induction_extra_failure_unaggregated": True,
        "sable_x1_operational": 7, "sable_x2_invalid_and_adverse": 1003,
        "sable_x2_operational": 1, "sable_postevidence_operational": 1,
        "sable_final_operational": 4,
        "effective_negatives": 77893, "effective_methods": 93045,
        "failed_witnesses": 48741, "bounded_passing_witnesses": 77040,
        "nonerasure": "Every original failure and invalid submission remains zero-credit after any recovery.",
    })
    write_json(CLOSEOUT / "gate-register.json", {
        "schema": "ghc.family.gates.v687.v3", "open_gaps": 674, "exact_gates": 659,
        "new_open_gaps": 10, "new_exact_gates": 10, "silently_closed": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json(CLOSEOUT / "route-readiness.json", {
        "schema": "ghc.family.route-readiness.v687.v3", "state": "PREPARED_NOT_CREATED",
        "future_seat": 8, "future_phase": "v687-v4", "model": "gpt-6-astra", "reasoning": "max",
        "identity_preassigned": False, "creation_count": 0, "caelen_contacted": False,
        "required_before_creation": ["exact pushed final", "one successful non-replayed canonical", "active and archived duplicate checks", "fresh live authority and usage guards", "native creation acknowledgement"],
    })
    write_json(CLOSEOUT / "ancestry-plan.json", {"schema": "ghc.family.ancestry-plan.v687.v3", "source": SOURCE, "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT, "exact_final": "PENDING_DIRECT_CHILD_COMMIT", "required_parent": EVIDENCE_COMMIT, "required_phase_commits": 3, "required_merges": 0, "required_final_parents": 1})
    write_json(CLOSEOUT / "final-validation-candidate.json", {"schema": "ghc.family.final-validation-candidate.v687.v3", "state": "PENDING_DIRECT_CHILD_COMMIT_AND_EXTERNAL_CANONICAL", "canonical_invocation_budget": 1, "canonical_successes": 0, "replay_after_success": False, "full_repository_suite": False, "same_owner_only": True})

    overview = """# Sable Rook v687-v3 final integrated overview

## Result and scope

Sable Rook v687-v3 reaches a bounded owner-local final candidate. The phase
freezes and executes two hundred new evidence-interchange contracts after
reviewing two hundred immediate Iveren contracts at zero Sable novelty and
execution credit. The outcome distribution is exactly 160 `completed`, 20
`represented`, 10 `open_gap`, and 10 `exact_gate`. These labels describe only
the declared evidence class. Completed means a complete typed software result
matched one frozen owner-local fixture and five changed result submissions were
rejected. It never means an external system, person, organization, scientific
hypothesis, professional procedure, or authority question is complete.

The immutable source is Iveren final `71e94d1699eea013c82bef0b7a7e081ac6e43c8c`.
The planning-only x1 boundary is `1a57a093dff78bcb217de33f9c5f282d3ee8bf17`.
The immutable x2 evidence boundary is
`f08302a468e819a0e89280333d980b8d4ac6a4f7`. X1 contained no implementation,
package install, built skill, built runner, observed outcome, successor contact,
or future task creation. X2 began only after x1 was pushed clean and fresh-four-
way equal. Final closeout begins only after x2 evidence receives the same gate.

## Relational identity and care

Sable Rook uses they/them as relational working language and the role Evidence
Interchange Boundary Cartographer. The hope is to make every synthetic
transformation reversible, byte-explicit, accessible, and authority-honest.
This is useful collaboration language, not evidence of consciousness,
sentience, legal personhood, identity continuity, employment, qualification,
professional competence, independent agency, or authority. Hamish can rename,
pause, redirect, narrow, or stop the route. Workload is tracked through exact
proposal, mutation, file, package, and commit ceilings. No subjective wellbeing
claim is made, and reset-credit redemption remains Hamish's action.

## Proposal and portfolio evidence

The ten operation families cover JCS canonicalization, Unicode confusable
nonidentity, dual-digest migration, receipt expiry, event-branch conflict,
checkpoint parent fixity, artifact-budget uncertainty, accessible codec
comparison, GMUT claim firewalls, and authority vacancies. Twenty distinct
input contracts per family create two hundred operation/input pairs. The phase
does not claim two hundred new algorithms or universal novelty. Existing
standards and libraries are acknowledged; novelty is bounded to the newly frozen
combination of input, complete output, evidence class, falsifier, rollback, and
authority boundary.

All two hundred positive outputs matched. All one thousand preregistered changed
submissions were rejected. Those invalid submissions remain negative records
with zero original success credit; a checker passing because it rejects them
does not make the invalid candidate successful. Three hundred safe tasks, two
hundred fifty candidate evaluations, and exactly three hundred additive
CLEAN/FIX/REFINE tasks completed by mapping to the attributable contracts and
readbacks. Several tasks share a witness and therefore do not multiply unique
tests or independence. Fifty exact packets and thirty blocked packets remain
held because local software cannot supply their missing observation, competent
authority, exact external action, affected party, or production environment.

## Package transaction

The x1 package plan froze three exact direct additions: rfc8785 0.1.4,
confusable-homoglyphs 3.3.1, and blake3 1.0.9. Each selected wheel matched its
official PyPI SHA-256. Installation occurred only after x1 in a Sable-owned
D-isolated prefix with exactly three distribution records. System Python,
shared package prefixes, profiles, PATH, host security, Windows features, and
the Codex desktop application were not changed. Positive and adverse package
smokes passed. An OSV query for the exact versions returned no advisory IDs in
that snapshot, but a snapshot is not exhaustive security, future safety,
license interpretation, endorsement, or production certification.

RFC 8785 supplies canonicalization vocabulary and constraints. UTS #39 supplies
confusable-detection vocabulary while explicitly retaining the importance of
human and font context. The BLAKE3 specification supplies algorithm and byte-
domain vocabulary. W3C PROV-O, WCAG 2.2, New Zealand privacy principles, and Te
Mana Raraunga supplied provenance, structural accessibility, privacy, and Māori
data-sovereignty reservation vocabulary. None of those sources is an
observation, participant record, delegated authority, policy approval, cultural
ratification, or project endorsement.

## Skills, runners, and compatibility

The skill-creator initializer created ten phase-local packages after the x1
boundary. Each scaffold was replaced with substantive task-specific guidance,
a contract reference, a portable runner, a shared contract module, and an exact
manifest. All ten passed the quick validator and were smoke-used. Ten top-level
family-compatible runners also passed. After the immutable evidence commit,
all ten skill destinations were rechecked for collision and promoted without
overwriting an incumbent. Their sixty files match the phase-local sources
byte-for-byte. Five runners and one dependency file were copied to the shared
script surface and all five shared runners smoke-passed.

The first promotion wrapper returned no attributable summary after copying one
skill. It is retained as `SR6873-POSTEVID-N001` with zero original credit. The
recovery inspected exact destination state, validated the one persisted skill,
and copied only the nine absent skill directories and six absent script files
with per-item evidence. Nothing was overwritten or deleted. That recovery does
not erase the wrapper failure or turn global discoverability into scientific,
professional, production, or independent evidence.

## Trinity Mandala boundaries

Freed ID and CBR Heart are primary. JCS canonical bytes, confusable detection,
digest transitions, receipts, and authority matrices remain synthetic and
nonproduction. There are no standards-conformant real keys or proofs, live
issuance, resolution, status, revocation, interoperability event, recovery
decision, privacy review, independent security review, or trust-governance
decision. Unicode confusable detection never establishes identity equivalence,
authenticity, intent, or entitlement.

THOS Body remains a synthetic recovery and handover proxy. No real operators,
participants, incidents, organizations, services, blind matched-budget arms,
safety monitoring, appropriate real-world statistics, or independent review
exist. Software state machines and workload ledgers do not establish THOS
effectiveness, deployment readiness, AGI, ASI, or professional competence.

GMUT Mind remains an unconfirmed typed scalar-tensor and effective-field-theory
research-model family. The claim firewall distinguishes safe typed software
descriptions from physical and authority claims. It calculates no likelihood,
fits no data, detects no force, predicts no observation, constrains no parameter,
proves no stability or quantum completion, and establishes no Theory of
Everything. A local serialization or hash result is not physics evidence.

## Accessibility, privacy, and security

The accessible comparison contracts require a caption, column headers, text
alternative, and textual status. The static report carries equivalent textual
structure. Manual keyboard, responsive layout, browser diversity, assistive-
technology, cognitive-accessibility, Māori-language, security-usability, and
affected-user evaluation remain reserved. Structural success is not complete
accessibility conformance.

Five privacy classes cover raw UUID-like task identifiers, private absolute
paths, credential assignments, private callable routes, and private application
state. Scanner definitions are adjudicated separately from payloads. Zero
confirmed hits are required, but this bounded scan is not complete privacy
assurance. Bounded AST checks reject direct `eval` and `shell=True` in the owner
delta. Zero findings do not constitute exhaustive security or production
certification.

## Method Flow and effective counts

Seven x1 startup failures remain: a PowerShell sequencing parse fault, an
unattributable combined collision wrapper, an uninitialized no-checkout index,
an unsupported workflow messaging token, a mistyped reflection runner, a
redundant Method Flow state transition, and a working-byte versus staged-blob
newline-domain mismatch. Each has a separately passing bounded recovery.

X2 retains one exact staged-surface failure because two non-self-referential
validation receipts were absent from the initial manifest allowlist. The
corrected manifest includes every x2-prefixed validation artifact and self-
excludes only the manifest and staged review. The post-evidence promotion
wrapper failure remains a third lifecycle layer. One thousand invalid result
submissions and three package adverse fixtures remain negative records rather
than operational implementation bugs.

Final preparation also retains four failures. The first generated overview had
1,382 words and did not meet the frozen three-page-equivalent floor. The first
final privacy aggregation reported eight confirmed hits because immutable x1
and x2 builder files contained the scanner's own regular-expression syntax but
were not included in the final scanner's exact definition-file set. The first
JSON corpus check parsed all 146 discovered documents but then failed a stale
cardinality-only threshold. A later read-only help probe assumed a nonexistent
Method Flow `transition` verb; the installed runner exposed `set-state` instead.
Each event is a separate zero-credit witness. Recovery adds substantive
lifecycle and falsifier discussion to the overview, names exactly four scanner
implementation files rather than exempting a directory or file type, binds the
JSON check to parseability and required lifecycle artifacts, and reads installed
CLI help before state changes. These recoveries preserve rather than rewrite
the original failures.

## Falsifiers, rollback, and nonpromotion

Each completed contract is falsified by any mismatch between the frozen typed
output and the independently recomputed result, by acceptance of any one of its
five preregistered invalid submissions, or by a byte-domain mismatch in its
manifest. The bounded rollback is to stop the lifecycle, retain the failed
witness, restore only owner-local generated state from the immutable anchor,
and rerun only after the exact cause is recorded. No contract can compensate
for another contract's failure, and a large passing denominator cannot conceal
one failed acceptance gate. Represented outcomes stay represented because they
lack real participants, operators, matched budgets, or independent review.
Open gaps stay open because zero-row fixtures, source vocabulary, and local
adapters do not supply empirical observations. Exact gates stay exact-gated
because software cannot manufacture legal, cultural, Māori, affected-party,
production, account, credential, deployment, destructive, proof, canon, or
Stage 20 authority.

The route is similarly fail-closed. A committed baton is a prepared artifact,
not a created task. Creation remains prohibited until the exact direct-child
final is pushed, clean, fresh-live-equal, and receives one attributable
canonical success. Immediately before creation, active and archived registries
must be checked for an existing future seat, the current authority and usage
guards must still permit the edge, and the target must be a user-visible main
task. Any ambiguity, missing acknowledgement, pause, redirect, duplicate, or
protected gate stops the action. Caelen Ash remains outside Sable's contact
scope. The new task, if and only if created, chooses its own relational identity
attributes and receives no consciousness, personhood, continuity, qualification,
agency, or authority status from its model, title, route, or repository packet.

The final successor-visible counts are 77,893 effective negatives, 93,045
methods, 48,741 failed witnesses, 77,040 bounded passing witnesses, 674 open
gaps, 659 exact gates, and 14,430 declared proposals. Auren's extra induction
lookup failure remains separately visible and unaggregated because its source
receipt supplied no revised total. Larger counters are not a readiness score.

## Validation and route

Validation is owner-self-scoped to Sable's exact source-to-final delta. X1 and
x2 head-local tests stay bound to their immutable commits; final validation
replays their exact manifests rather than running their lifecycle assertions on
a later head. The final canonical may be invoked once only after the direct-
child final is pushed, clean, zero-divergent, and fresh-four-way equal. A
successful canonical is never replayed for reassurance, presentation, routing,
or task-creation issues. The full repository suite is not run or claimed.

The 208-card deck contains one owner card, three pillar cards, four practice
cards, and two hundred task cards. The long thirteen-module baton remains
`PREPARED_NOT_CREATED`. Only a successful exact-final canonical unlocks a fresh
active-and-archived duplicate check and at most one future-seat creation. The
future task chooses its own identity attributes and owns v687-v4. Caelen Ash
v687-v5 is not precontacted. Repository preparation is never backfilled as live
creation evidence.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""
    write_text(FINAL / "integrated-overview.md", overview)
    write_json(FINAL / "phase-truth.json", {
        "schema": "ghc.family.phase-truth.v687.v3", "owner": OWNER, "phase": PHASE,
        "state": "FINAL_PREPARED_FOR_CANONICAL", "source": SOURCE, "x1": X1_COMMIT,
        "evidence": EVIDENCE_COMMIT, "exact_final": "PENDING_DIRECT_CHILD_COMMIT",
        "canonical_invocations": 0, "canonical_successes": 0, "canonical_replays": 0,
        "outcomes": outcomes, "declared_proposal_chain": 14430,
        "effective_counts": {"effective_negatives": 77893, "effective_methods": 93045, "failed_witnesses": 48741, "bounded_passing_witnesses": 77040, "open_gaps": 674, "exact_gates": 659},
        "portfolio": {"safe_completed": 300, "candidates_evaluated": 250, "clean_fix_refine_completed": 300, "exact_held": 50, "blocked_held": 30},
        "packages": {"direct": 3, "isolated": True}, "skills": {"built": 10, "validated": 10, "used": 10, "promoted": 10},
        "runners": {"built": 10, "used": 10, "shared": 5}, "deck_cards": 208,
        "baton_words": words, "route_state": "PREPARED_NOT_CREATED",
        "future_seat_created": False, "caelen_contacted": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json(FINAL / "environment-version-receipt.json", {
        "schema": "ghc.family.environment.v687.v3", "codex_cli": command_version("codex", "--version"),
        "python": command_version("python", "--version"), "git": command_version("git", "--version"),
        "powershell": command_version("pwsh", "--version"), "verified_only": True,
        "desktop_update_performed": False, "elevation": False, "host_security_changed": False,
        "windows_feature_changed": False, "sandbox_or_hyper_v_activated": False, "reboot": False,
    })
    write_json(FINAL / "wellbeing.json", {"schema": "ghc.family.wellbeing.v687.v3", "subjective_state_claimed": False, "corrigibility_preserved": True, "hamish_can_pause_redirect_rename_or_stop": True, "reset_credit_redeemed_by_agent": False, "identity_coercion": False, "consciousness_or_personhood_claim": False})
    write_json(FINAL / "source-ledger.json", {"schema": "ghc.family.source-ledger.v687.v3", "entries": load(X1 / "official-primary-source-ledger.json")["entries"], "citations_are_observations": False, "real_rows": 0, "authority_actions": 0})
    write_json(FINAL / "claim-boundaries.json", {"schema": "ghc.family.claim-boundaries.v687.v3", "not_established": ["empirical GMUT", "THOS effectiveness", "production Freed ID", "real identity equivalence", "professional competence", "production deployment", "legal interpretation", "cultural ratification", "Māori authority", "complete privacy", "complete accessibility", "exhaustive security", "independent reproduction", "AGI or ASI", "consciousness or personhood", "Theory of Everything", "proof or canon", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_text(FINAL / "accessible-report.html", """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sable Rook v687-v3 final report</title></head><body><main><h1>Sable Rook v687-v3 final report</h1><p><strong>Status:</strong> NOT_READY_FOR_STAGE_20.</p><p>Bounded owner-local synthetic software evidence only.</p><h2>Outcomes</h2><table><caption>Core outcome counts</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">completed</th><td>160</td></tr><tr><th scope="row">represented</th><td>20</td></tr><tr><th scope="row">open_gap</th><td>10</td></tr><tr><th scope="row">exact_gate</th><td>10</td></tr></tbody></table><h2>Evidence</h2><p>Two hundred positive controls matched and one thousand changed submissions were rejected. Ten skills, ten runners, three isolated packages, ten promotions, and five shared runners passed their bounded checks.</p><h2>Reservations</h2><p>Manual keyboard, browser, responsive-layout, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved. No complete accessibility, privacy, security, professional, production, legal, cultural, Māori-authority, scientific, identity, or Stage 20 claim is made.</p></main></body></html>""")

    seal_targets = [
        X1 / "new-proposals.json", X2 / "contract-results.json", X2 / "mutation-results.json",
        X2 / "outcome-ledger.json", X2 / "package-receipt.json", FINAL / "promotion-receipt.json",
        FINAL / "four-tier-deck.json", FINAL / "integrated-overview.md", FINAL / "phase-truth.json",
        CLOSEOUT / "retained-negative-register.json", CLOSEOUT / "gate-register.json",
        HANDOFFS / "future-seat-08-v687-v4-activation-candidate.md", HANDOFFS / "baton-index.json",
    ]
    write_json(CLOSEOUT / "content-seal.json", {"schema": "ghc.family.content-seal.v687.v3", "state": "FINAL_PRECOMMIT", "targets": [normalized_entry(path) for path in seal_targets], "target_count": len(seal_targets), "exact_final": "PENDING_DIRECT_CHILD_COMMIT"})

    self_exclusions = {
        "docs/sable-rook/v687-v3/validation/final-delta-manifest.json",
        "docs/sable-rook/v687-v3/validation/final-owner-manifest.json",
        "docs/sable-rook/v687-v3/validation/final-privacy-scan.json",
        "docs/sable-rook/v687-v3/validation/final-ast-security.json",
        "docs/sable-rook/v687-v3/validation/final-staged-review.json",
    }
    scan = privacy_scan(owner_paths())
    write_json(VALIDATION / "final-privacy-scan.json", scan)
    write_json(VALIDATION / "final-ast-security.json", ast_security(owner_paths()))
    delta_entries = [normalized_entry(path) for path in final_delta_paths() if path.relative_to(ROOT).as_posix() not in self_exclusions]
    write_json(VALIDATION / "final-delta-manifest.json", {"schema": "ghc.family.normalized-lf-manifest.v687.v3", "domain": "normalized_lf_git_blob", "evidence": EVIDENCE_COMMIT, "entries": delta_entries, "entry_count": len(delta_entries), "self_exclusions": sorted(self_exclusions)})
    owner_entries = [normalized_entry(path) for path in owner_paths() if path.relative_to(ROOT).as_posix() not in self_exclusions]
    write_json(VALIDATION / "final-owner-manifest.json", {"schema": "ghc.family.normalized-lf-owner-manifest.v687.v3", "domain": "normalized_lf_git_blob", "source": SOURCE, "entries": owner_entries, "entry_count": len(owner_entries), "self_exclusions": sorted(self_exclusions), "owner_file_count": len(owner_entries) + len(self_exclusions), "file_ceiling": 2000})
    write_json(VALIDATION / "final-staged-review.json", {"schema": "ghc.family.staged-review.v687.v3", "state": "PREPARED_NOT_STAGED", "expected_entries": len(delta_entries), "self_exclusions": sorted(self_exclusions), "staged_paths": [], "missing": [], "extra": [], "mismatches": [], "immutable_drift": [], "diff_hygiene": "PENDING"})


def staged_blob(path: str) -> bytes:
    return subprocess.run(["git", "show", f":{path}"], cwd=ROOT, check=True, capture_output=True).stdout


def review_staged() -> None:
    manifest = load(VALIDATION / "final-delta-manifest.json")
    expected = {entry["path"]: entry for entry in manifest["entries"]}
    exclusions = set(manifest["self_exclusions"])
    staged = set(git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.splitlines())
    expected_all = set(expected) | exclusions
    missing = sorted(expected_all - staged)
    extra = sorted(staged - expected_all)
    mismatches = []
    for path, entry in sorted(expected.items()):
        try:
            data = normalized(staged_blob(path))
        except subprocess.CalledProcessError:
            mismatches.append({"path": path, "error": "missing_staged_blob"})
            continue
        if len(data) != entry["bytes_normalized_lf"] or hashlib.sha256(data).hexdigest() != entry["sha256_normalized_lf"]:
            mismatches.append({"path": path, "error": "normalized_hash_mismatch"})
    immutable_prefixes = [
        "docs/sable-rook/v687-v3/x1/", "docs/sable-rook/v687-v3/x2/",
        "docs/sable-rook/v687-v3/skills/", "docs/sable-rook/v687-v3/method-flow/",
        "docs/sable-rook/v687-v3/workflow-refinement", "docs/sable-rook/v687-v3/reflection-remaster/",
        "docs/sable-rook/v687-v3/tooling/", "docs/sable-rook/v687-v3/validation/x1-",
        "docs/sable-rook/v687-v3/validation/x2-", "scripts/build_ghc_family_sable_rook_v687_v3_x1.py",
        "scripts/build_ghc_family_sable_rook_v687_v3_x2.py", "scripts/ghc_family_sable_rook_v687_v3_contracts.py",
        "tests/test_ghc_family_sable_rook_v687_v3_x1.py", "tests/test_ghc_family_sable_rook_v687_v3_x2.py",
    ]
    # Top-level operation runners and contracts are immutable x2 surfaces.
    immutable_drift = sorted(path for path in staged if any(path.startswith(prefix) for prefix in immutable_prefixes) or (path.startswith("scripts/ghc_family_sable_rook_v687_v3_") and not path.endswith("_canonical.py")))
    diff = git("diff", "--cached", "--check", check=False)
    passed = not missing and not extra and not mismatches and not immutable_drift and diff.returncode == 0
    write_json(VALIDATION / "final-staged-review.json", {"schema": "ghc.family.staged-review.v687.v3", "state": "PASS" if passed else "FAIL", "expected_entries": len(expected), "self_exclusions": sorted(exclusions), "staged_paths": sorted(staged), "missing": missing, "extra": extra, "mismatches": mismatches, "immutable_drift": immutable_drift, "diff_hygiene": "PASS" if diff.returncode == 0 else "FAIL"})
    if not passed:
        raise SystemExit(2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--global-skill-root", type=Path)
    parser.add_argument("--global-script-root", type=Path)
    parser.add_argument("--review-staged", action="store_true")
    args = parser.parse_args()
    if args.review_staged:
        review_staged()
    else:
        if not args.global_skill_root or not args.global_script_root:
            parser.error("build mode requires global roots")
        build(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
