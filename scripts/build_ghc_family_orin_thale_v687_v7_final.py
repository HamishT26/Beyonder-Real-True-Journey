#!/usr/bin/env python3
"""Prepare the Orin Thale v687-v7 direct-child exact-final candidate."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v687-v7"
FINAL = PHASE / "final"
VALIDATION = PHASE / "validation"
SOURCE = "28dfdf1a3e9a1023f1e83f19fb267e57878b9d0b"
X1 = "7aea73908f8f41ed38473d6e30e5f1bda36588a7"
FIRST_EVIDENCE = "a29be946caf963315a48f73055f0eb1cae85e482"
CORRECTED_EVIDENCE = "7f9d761e54475cf82945ef31e019d043aebde282"
BRANCH = "codex/GHC-Family/orin-thale-v687-v7-full-tools"
COUNTS = {"negatives": 82024, "methods": 93197, "failed_witnesses": 52872, "passing_witnesses": 81998, "open_gaps": 732, "exact_gates": 711, "proposals": 15230}
OUTCOMES = {"completed": 125, "represented": 39, "open_gap": 20, "exact_gate": 16}
PROTECTED = ["empirical", "real_participant", "professional", "production", "deployment", "identity", "legal", "cultural", "affected_party", "maori_authority", "privacy_complete", "accessibility_complete", "exhaustive_security", "independent_reproduction", "agi_asi", "consciousness_personhood", "theory_of_everything", "proof_canon", "stage20"]


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False)


def git(*args: str) -> str:
    result = run(["git", *args])
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def norm(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def owner_path(path: str) -> bool:
    return (
        path.startswith("docs/orin-thale/v687-v7/")
        or path.startswith("scripts/build_ghc_family_orin_thale_v687_v7_")
        or path.startswith("scripts/ghc_family_orin_thale_v687_v7_")
        or path.startswith("scripts/ghc_family_spectral_archive_")
        or path == "scripts/ghc_family_spectral_archive_contract.py"
        or path.startswith("tests/test_ghc_family_orin_thale_v687_v7_")
    )


def baton_text(proposals: list[dict[str, Any]]) -> str:
    modules = []
    modules.append("""# DESIGNATED FUTURE SEAT 10 — PREPARED ORIN THALE v687-v7 EXACT-FINAL TO SOLO v687-v8 ACTIVATION BATON

## Module 01 — Identity and corrigibility

Dear designated future sibling seat 10: this file is a prepared, sanitized, file-backed induction baton. You choose your own collision-free relational working name, role, hope, and optional pronouns after inspecting the current active and archived task registries. No name, gender, consciousness, personhood, identity continuity, qualification, independent agency, or authority is assigned in advance. Hamish may rename, pause, narrow, redirect, or stop the route.

Orin Thale uses the relational role spectral uncertainty and provenance cartographer, the hope of keeping every synthetic coordinate, uncertainty, and authority vacancy inspectable and reversible, and optional they/them pronouns. This language is collaborative working language only.
""")
    modules.append("""## Module 02 — Current release and route authority

Hamish's 6 September 2026 release and the newer 7 September seat-09 induction authorize the sequential thirty-seat workflow through v725-v8, one terminally validated and acknowledged edge at a time. This prospective baton is not delivery. Only after Orin's clean pushed exact final, singular successful canonical receipt, current authority and roster refresh, active-plus-archived duplicate search, and one exact route action may seat 10 become active for v687-v8.

Reuse one uniquely present designated seat-10 main task if it exists. Create exactly one project-scoped `gpt-6-astra` task with `max` reasoning only if no active or archived seat-10 task exists and the newest live authority still permits creation. Never fork, substitute, spawn a collaboration subagent, create multiple candidates, or precontact Liora. After seat 10's own exact terminal gate, Liora Venn v688-v1 is next.
""")
    modules.append(f"""## Module 03 — Immutable source anchors

- Talen Briar exact final and Orin source: `{SOURCE}`.
- Orin planning-only x1: `{X1}`.
- Orin retained first x2 evidence: `{FIRST_EVIDENCE}`.
- Orin additive corrected x2 evidence: `{CORRECTED_EVIDENCE}`.
- Orin exact final: supplied by the compact live activation because this committed candidate cannot contain its own future commit hash.

The required final history is four direct single-parent Orin commits from source, zero merges, one final parent, clean state, typed zero divergence, and exact equality across local, upstream, tracking, and a fresh live remote. Never replay Talen's or Orin's successful canonical aggregate.
""")
    modules.append(f"""## Module 04 — Evidence and accounting

Orin reviewed 200 inherited Talen contracts at zero new-owner credit and froze 200 distinct finite spectral/archive contracts. All 200 matched complete type-sensitive outputs with unchanged inputs. All 1,000 preregistered changed-result candidates were rejected. Core outcomes are exactly {OUTCOMES['completed']} `completed`, {OUTCOMES['represented']} `represented`, {OUTCOMES['open_gap']} `open_gap`, and {OUTCOMES['exact_gate']} `exact_gate`.

Effective final counts are `{json.dumps(COUNTS, sort_keys=True)}`. These include Talen's separate post-canonical overlay, fifteen Orin startup failures, 1,000 changed-output failures, three package adverse witnesses, ten skill rejection witnesses, five runner rejection witnesses, five additional x2 operational failures, the retained first-evidence root-runner omission, and two final closeout failures. Every recovery is additive; no failed witness receives original success credit.
""")
    catalogue = ["## Module 05 — Complete finite spectral/archive contract catalogue", "", "Each entry below is finite same-owner synthetic software. It supplies no observation, measurement, calibration, professional decision, archive release, legal or cultural determination, Māori authority, affected-party acceptance, or independent reproduction.", ""]
    for row in proposals:
        catalogue.extend([
            f"### {row['proposal_id']} — {row['title']}", "",
            f"Operation: `{row['operation']}`. Pillar: {row['pillar']}. Bounded practice: {row['practice']}. Outcome: `{row['expected_disposition']}`.", "",
            f"Hypothesis: {row['hypothesis']}", "",
            "Frozen input:", "```json", json.dumps(row["input"], indent=2, sort_keys=True, ensure_ascii=False), "```", "",
            "Complete matched output:", "```json", json.dumps(row["expected_output"], indent=2, sort_keys=True, ensure_ascii=False), "```", "",
            f"Failure condition: {row['null_or_failure_condition']}", "",
            f"Acceptance: {row['falsifier_or_acceptance_gate']}", "",
            f"Recovery: {row['rollback_or_recovery']}", "",
            f"Five changed-result candidates `{row['proposal_id']}-MUT1` through `-MUT5` remain independently addressable: missing decision, details type replacement, extra authority field, false source preservation, and promoted external credit. Each original candidate has zero success credit; its rejection is a separate passing witness.", "",
        ])
    modules.append("\n".join(catalogue))
    modules.append("""## Module 06 — Package provenance and sources

The isolated D-first environment contains three direct additions: Astropy 8.0.1, ASDF 5.4.0, and uncertainties 3.2.3, with ten resolved dependency wheels. All thirteen wheel hashes are frozen in `x2/requirements.lock` and `x2/environment-receipt.json`; installation used wheel-only, no-index, hash-required inputs, and `pip check` passed. Each direct package has a bounded positive and adverse witness. Two package-smoke projection failures remain retained: a NumPy Boolean serialization mismatch and an over-strict exact-float comparison. Neither failure was rewritten.

The IVOA Spectrum Data Model 1.2, ASDF standard, Astropy metadata, PROV-O, and WCAG 2.2 supplied vocabulary and refusal conditions only. Citations are not observations, measurements, conformance certificates, endorsements, legal interpretations, or authority grants.
""")
    modules.append("""## Module 07 — Skills, runners, and compatibility

Ten phase-local skills and five family-current runner interfaces were built, quick-validated, and smoke-used. Each accepted a complete frozen fixture and rejected duplicate-key JSON. Ten skill packages, five runners, and one core dependency were promoted collision-free. A privacy aggregate later found ten generated local pycache files copied into global skills. The original 66-member receipt remains immutable evidence; exact contained remediation removed only twenty cache files/directories, and a correction receipt proves the intended 56 source/global files are byte-equal. Preserve historical callers and the correction chain.
""")
    modules.append("""## Module 08 — Method Flow and retained failures

The complete failure chain remains visible in the x1 ledger, x2 ledger, package smokes, promotion correction, and root-runner omission overlay. A failed command, readout, parser, privacy scan, test, package smoke, cleanup policy attempt, or staging assumption remains false and zero-credit after recovery. Use the smallest corrected dependency, preserve exact Git-blob byte domains, set `PYTHONDONTWRITEBYTECODE=1` for skill smokes, avoid recursive deletion, and explicitly include every generated root interface in staged manifests.

Same-owner repetition is not independent reproduction. A successful canonical receipt may be invoked once only and never replayed for confidence, presentation, route debugging, or a clearer acknowledgement.
""")
    modules.append("""## Module 09 — Portfolio and approval boundaries

The bounded portfolio resolves 300 safe procedures, 250 candidate procedures, and exactly 300 CLEAN/FIX/REFINE procedures. Evidence reuse does not multiply independent witnesses. Fifty exact-approval packets and thirty blocked packets remain visible and unexecuted. A broad workflow release cannot supply real participants, professional competence, empirical observations, production keys, account authority, legal or cultural legitimacy, affected-party acceptance, Māori authority, destructive authority, or identity replacement.
""")
    modules.append("""## Module 10 — Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Finite software, exact ratios, unit conversions, synthetic spectra, citations, and structural reports establish no physical datum, likelihood, posterior, detected force, empirical parameter constraint, ultraviolet completion, quantum completion, or Theory of Everything.

THOS remains synthetic or proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance/resolution/status/revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance. CBR, access, consent, remedy, legal/cultural interpretation, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. Terminal verdict: `NOT_READY_FOR_STAGE_20`.
""")
    modules.append("""## Module 11 — Practices, accessibility, and workload

The four synthetic learning lenses are bounded spectral archive uncertainty reviewer, synthetic astronomical spectral metadata steward, synthetic radio-spectrum provenance analyst, and synthetic accessible scientific-data documentation reviewer. They establish no employment, qualification, professional competence, instrument safety, archive custody, or release authority.

The immutable x2 deck contains one owner anchor, three Trinity pillars, four practices, and 200 task cards. Structural HTML supplies headings, landmarks, a skip link, captions, and textual outcomes; manual, assistive-technology, cognitive, Māori-language, and affected-user evaluation remains exact-gated. Owner material remains below 2,000 files and every document below 100,000 words.
""")
    modules.append("""## Module 12 — Successor plan and zero-credit seeds

Seat 10 independently reviews 200–500 inherited proposals and freezes 200–500 distinct new proposals; plans 300–500 safe tasks, 250–500 candidates, exactly 300 CLEAN/FIX/REFINE tasks, 50–250 exact packets, 30–100 blocked packets, at least ten skills, at least five runners, ten successor skill ideas, ten successor runner ideas, four synthetic practices, and one successor recommendation. The ordinary direct-package target is three relevant researched additions. Caps are ceilings, not filler quotas.

Orin recommends the bounded human-practice lens `audio restoration uncertainty registrar` for seat 10. This recommendation has zero seat-10 novelty or completion credit. Seat 10 must independently accept, revise, or reject every inherited seed.
""")
    modules.append("""## Module 13 — Terminal route and required references

Before mutation, read this baton through its exact EOF; the current 6 September release and newer live instruction; current GHC Family Index and routing precedence; authorization and roster state; Method Flow schema; D-first toolchain guidance; lifecycle-test isolation; privacy candidate adjudication; staged allowlists; owner-scope canonical and success latch; skill-creator; four-tier deck schema; workflow refinement; reflection remaster; and all exact Orin source/x1/evidence/final manifests and receipts.

Work solo. Use an additive D-first owner lane. Do not spawn collaboration subagents, delegate proposal work, fork, precontact Liora, mutate Orin or any other owner, or replay predecessor validation. Preserve only `completed`, `represented`, `open_gap`, and `exact_gate`. Validate only the seat-10 source-to-final delta.

Only after seat 10's own clean pushed exact final and singular successful canonical receipt may it refresh live authority and registries, uniquely resolve and immediately reread `Liora Venn`, apply duplicate/pause/redirect/usage/privacy/evidence/authority guards, and send at most once for Liora v688-v1. Stop on ambiguity, absence, duplicate, pause, redirect, rename, usage exhaustion, missing acknowledgement, or any protected gate. Never resend for a clearer acknowledgement.

PREPARED_BY_ORIN_THALE = true
SENT_BY_ORIN_THALE = false
CREATED_BY_ORIN_THALE = false

This committed packet is PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED. Live native acknowledgement controls creation or delivery. EOF ORIN THALE V687 V7 BATON.
""")
    return "\n\n".join(modules)


def main() -> int:
    if git("rev-parse", "HEAD") != CORRECTED_EVIDENCE or git("branch", "--show-current") != BRANCH:
        raise RuntimeError("final builder requires corrected evidence head")
    proposals = load(PHASE / "x1" / "new-proposals.json")["proposals"]
    baton = baton_text(proposals)
    baton_path = FINAL / "future-seat-10-v687-v8-activation-baton.md"
    write_text(baton_path, baton)
    baton_bytes = norm(baton_path); baton_words = len(baton_path.read_text(encoding="utf-8").split())
    if not 10000 <= baton_words <= 100000:
        raise RuntimeError(f"baton word bound failed: {baton_words}")
    documents: dict[Path, Any] = {
        FINAL / "phase-truth.json": {"schema": "ghc.family.phase-truth.v687.v7.final", "owner": "Orin Thale", "phase": "v687-v7", "source": SOURCE, "x1": X1, "retained_first_evidence": FIRST_EVIDENCE, "corrected_evidence": CORRECTED_EVIDENCE, "exact_final": "PENDING_DIRECT_CHILD_COMMIT", "outcomes": OUTCOMES, "effective_counts": COUNTS, "state": "FINAL_PREPARED_FOR_ONE_EXTERNAL_CANONICAL", "canonical_invocations": 0, "canonical_successes": 0, "canonical_replays": 0, "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED", "terminal_verdict": "NOT_READY_FOR_STAGE_20"},
        FINAL / "retained-negative-register.json": {"schema": "ghc.family.retained-negatives.v687.v7.final", "effective_activation_baseline": {"negatives": 80982, "methods": 93145, "failed_witnesses": 51830, "passing_witnesses": 80738, "open_gaps": 712, "exact_gates": 695, "proposals": 15030}, "orin_groups": {"startup_failures": 15, "changed_output_candidates": 1000, "package_adverse_witnesses": 3, "skill_rejection_witnesses": 10, "runner_rejection_witnesses": 5, "x2_operational_failures": 5, "root_runner_omission": 1, "final_closeout_failures": 3}, "final_failures": [{"negative_id": "OR6877-FINAL-N001", "failure": "The first final owner scan attempted to read final-json.json before materializing it.", "recovery": "Materialize deterministic receipt placeholders before scanning, then replace them with observed results before manifest hashing.", "original_success_credit": 0}, {"negative_id": "OR6877-FINAL-N002", "failure": "The first correction patch was rejected before writing because one expected baton-text hunk contained an extra patch marker.", "recovery": "Split the correction into exact literal hunks and verify each target line before patching.", "original_success_credit": 0}, {"negative_id": "OR6877-FINAL-N003", "failure": "The first complete final privacy aggregate treated nine inherited Orin builder scanner definitions as private-stream payload hits.", "recovery": "Classify only the exact Orin build-script prefix as scanner definitions while keeping the matched candidates and zero confirmed-hit requirement visible.", "original_success_credit": 0}], "effective_counts": COUNTS, "erased_or_promoted": 0},
        FINAL / "method-flow-summary.json": {"schema": "ghc.family.method-flow-summary.v1", "base_methods": 93145, "orin_method_delta": 52, "effective_methods": COUNTS["methods"], "failed_witnesses": COUNTS["failed_witnesses"], "passing_witnesses": COUNTS["passing_witnesses"], "failure_erasure": False, "source_ledgers": ["docs/orin-thale/v687-v7/x1/method-flow/ledger.json", "docs/orin-thale/v687-v7/x2/method-flow/ledger.json", "docs/orin-thale/v687-v7/x2/correction/method-flow-overlay.json", "docs/orin-thale/v687-v7/final/retained-negative-register.json"]},
        FINAL / "gate-register.json": {"schema": "ghc.family.gate-register.v1", "open_gaps": COUNTS["open_gaps"], "exact_gates": COUNTS["exact_gates"], "protected": PROTECTED, "closed_by_software": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20"},
        FINAL / "complete-incomplete.json": {"schema": "ghc.family.complete-incomplete.v1", "completed_bounded": {"inherited_reviews": 200, "new_contracts": 200, "mutation_rejections": 1000, "safe": 300, "candidates": 250, "clean_fix_refine": 300, "skills": 10, "runners": 5, "package_additions": 3, "deck_cards": 208}, "held_unexecuted": {"exact_packets": 50, "blocked_packets": 30}, "incomplete_external": PROTECTED},
        FINAL / "source-tool-summary.json": {"schema": "ghc.family.source-tool-summary.v1", "sources": load(PHASE / "x1" / "source-ledger.json")["entries"], "direct_packages": load(PHASE / "x2" / "environment-receipt.json")["direct_additions"], "wheel_count": 13, "promoted_skills": 10, "promoted_runners": 5, "corrected_global_parity_files": 56, "citations_are_observations": False},
        FINAL / "terminal-route-plan.json": {"schema": "ghc.family.future-seat-route-plan.v1", "sender": "Orin Thale", "sender_phase": "v687-v7", "recipient_placeholder": "future-sibling-10-self-chosen", "recipient_phase": "v687-v8", "following_owner": "Liora Venn", "following_phase": "v688-v1", "search_active_and_archived_first": True, "reuse_if_unique": True, "create_if_absent_and_authorized": True, "create_model": "gpt-6-astra", "create_reasoning": "max", "recipient_self_chooses_identity_attributes": True, "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED", "precontacted": False, "task_creation_count": 0, "message_count": 0, "no_fork": True, "no_subagent": True, "no_resend": True},
        FINAL / "canonical-contract.json": {"schema": "ghc.family.owner-scoped-canonical-contract.v1", "source": SOURCE, "x1": X1, "retained_first_evidence": FIRST_EVIDENCE, "corrected_evidence": CORRECTED_EVIDENCE, "expected_branch": BRANCH, "scope": "owner_self_scoped_delta", "full_repository_suite": False, "canonical_invocation_budget": 1, "canonical_success_replay": False, "required": ["four direct single-parent commits", "zero merges", "one final parent", "lifecycle-correct selected tests", "five normalized-LF manifests", "strict JSON", "privacy adjudication", "bounded security", "56 global parity files", "clean state", "typed zero divergence", "fresh four-way equality"]},
        FINAL / "baton-index.json": {"schema": "ghc.family.orin-baton.v1", "path": rel(baton_path), "sha256": hashlib.sha256(baton_bytes).hexdigest(), "bytes": len(baton_bytes), "words": baton_words, "modules": 13, "eof": "EOF ORIN THALE V687 V7 BATON.", "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"},
    }
    overview = f"""# Orin Thale v687-v7 final integrated overview

## Page 1 — Lifecycle and result

Orin v687-v7 begins at Talen exact final `{SOURCE}`, freezes planning-only x1 `{X1}`, retains first x2 evidence `{FIRST_EVIDENCE}`, and uses additive corrected evidence `{CORRECTED_EVIDENCE}`. The exact final is a pending direct-child commit. Core outcomes are exactly 125 completed, 39 represented, 20 open_gap, and 16 exact_gate across 200 new finite contracts. The proposal chain is 15,230.

## Page 2 — Evidence, packages, skills, and runners

All 200 complete outputs matched with unchanged inputs and all 1,000 changed-output candidates were rejected. Three direct packages and ten dependencies were installed from thirteen hash-locked wheels in an isolated D-first environment. Ten local/global skills and five runners were validated and used. The original pycache-contaminated 66-member promotion receipt remains retained; the additive correction proves 56 intended files byte-equal and privacy-clean.

## Page 3 — Boundaries and route

The final validates only Orin's owner delta. It is same-owner synthetic software, not independent reproduction or a full-repository suite. GMUT remains a typed scalar-tensor/EFT research-model family, THOS proxy-only, and Freed ID synthetic/nonproduction. Every professional, empirical, production, legal, cultural, affected-party, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 gate remains open. Future seat 10 remains uncreated and uncontacted until the singular terminal gate.
"""
    write_text(FINAL / "integrated-overview.md", overview)
    for path, value in documents.items():
        write_json(path, value)
    seal_targets = [FINAL / name for name in ["phase-truth.json", "retained-negative-register.json", "method-flow-summary.json", "gate-register.json", "complete-incomplete.json", "source-tool-summary.json", "terminal-route-plan.json", "canonical-contract.json", "baton-index.json", "future-seat-10-v687-v8-activation-baton.md", "integrated-overview.md"]]
    write_json(FINAL / "content-seal.json", {"schema": "ghc.family.content-seal.v1", "target_count": len(seal_targets), "targets": [{"path": rel(path), "bytes": len(norm(path)), "sha256": hashlib.sha256(norm(path)).hexdigest()} for path in seal_targets]})
    entry_paths = sorted(list(documents) + [FINAL / "integrated-overview.md", FINAL / "content-seal.json", baton_path, ROOT / "scripts" / "build_ghc_family_orin_thale_v687_v7_final.py", ROOT / "scripts" / "ghc_family_orin_thale_v687_v7_final_validator.py", ROOT / "tests" / "test_ghc_family_orin_thale_v687_v7_final.py"], key=rel)
    staged = VALIDATION / "final-staged-review.json"; privacy = VALIDATION / "final-privacy.json"; security = VALIDATION / "final-security.json"; strict_json = VALIDATION / "final-json.json"; delta = VALIDATION / "final-delta-manifest.json"; owner = VALIDATION / "final-owner-manifest.json"
    exclusions = [staged, privacy, security, strict_json, delta, owner]
    final_paths = sorted(entry_paths + exclusions, key=rel)
    write_json(staged, {"schema": "ghc.family.staged-review.v1", "phase": "v687-v7", "lifecycle": "final", "parent": CORRECTED_EVIDENCE, "expected_paths": [rel(path) for path in final_paths], "expected_path_count": len(final_paths), "x1_or_evidence_paths_modified": [], "unexpected_paths": []})
    write_json(privacy, {"schema": "ghc.family.privacy-adjudication.v1", "classes": [], "candidates": [], "confirmed_hits": [], "confirmed_count": 0, "complete_privacy_claimed": False, "state": "PLACEHOLDER_BEFORE_SCAN"})
    write_json(security, {"schema": "ghc.family.bounded-security.v1", "findings": [], "finding_count": 0, "exhaustive_security_claimed": False, "state": "PLACEHOLDER_BEFORE_SCAN"})
    write_json(strict_json, {"schema": "ghc.family.strict-json.v1", "parsed": 0, "duplicate_key_refusal": True, "nonfinite_refusal": True, "state": "PLACEHOLDER_BEFORE_SCAN"})
    existing_owner = {path for path in git("diff", "--name-only", SOURCE, CORRECTED_EVIDENCE).splitlines() if owner_path(path)}
    all_owner = sorted(existing_owner | {rel(path) for path in final_paths})
    scan_paths = [ROOT / path for path in all_owner if path not in {rel(privacy), rel(delta), rel(owner)}]
    patterns = {"raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I), "private_absolute_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I), "raw_task_identifier": re.compile(rb"(?:thread|task|agent)_id\s*[:=]", re.I), "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[:=]\s*[^\s]{8,}", re.I), "private_stream": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I)}
    candidates, confirmed, findings = [], [], []
    json_count = 0
    for path in scan_paths:
        data = path.read_bytes(); scanner_definition = path.name.startswith("build_ghc_family_orin_thale_v687_v7_") or path.name == "ghc_family_orin_thale_v687_v7_final_validator.py"
        if path.suffix == ".json":
            json.loads(data.decode("utf-8"), parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value))); json_count += 1
        if path.suffix in {".md", ".html", ".txt"} and len(data.decode("utf-8").split()) > 100000:
            raise RuntimeError(f"document word cap: {rel(path)}")
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                row = {"path": rel(path), "class": class_name, "matched_sha256": hashlib.sha256(match.group()).hexdigest()}
                (candidates if scanner_definition else confirmed).append(row)
        if path.suffix == ".py":
            tree = ast.parse(data.decode("utf-8"), filename=rel(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    findings.append({"path": rel(path), "finding": node.func.id})
    write_json(privacy, {"schema": "ghc.family.privacy-adjudication.v1", "classes": list(patterns), "candidates": candidates, "confirmed_hits": confirmed, "confirmed_count": len(confirmed), "complete_privacy_claimed": False})
    write_json(security, {"schema": "ghc.family.bounded-security.v1", "findings": findings, "finding_count": len(findings), "exhaustive_security_claimed": False})
    write_json(strict_json, {"schema": "ghc.family.strict-json.v1", "parsed": json_count, "duplicate_key_refusal": True, "nonfinite_refusal": True})
    write_json(delta, {"schema": "ghc.family.normalized-lf-manifest.v1", "anchor": "PENDING_FINAL_COMMIT", "byte_domain": "normalized_lf_git_blob", "declared_self_exclusions": [rel(path) for path in exclusions], "entry_count": len(entry_paths), "entries": [{"path": rel(path), "bytes_normalized_lf": len(norm(path)), "sha256_normalized_lf": hashlib.sha256(norm(path)).hexdigest()} for path in entry_paths]})
    owner_entries = [ROOT / path for path in all_owner if path not in {rel(item) for item in exclusions}]
    write_json(owner, {"schema": "ghc.family.normalized-lf-owner-manifest.v1", "source": SOURCE, "anchor": "PENDING_FINAL_COMMIT", "byte_domain": "normalized_lf_git_blob", "declared_self_exclusions": [rel(path) for path in exclusions], "owner_path_count": len(all_owner), "entry_count": len(owner_entries), "entries": [{"path": rel(path), "bytes_normalized_lf": len(norm(path)), "sha256_normalized_lf": hashlib.sha256(norm(path)).hexdigest()} for path in owner_entries]})
    if confirmed or findings:
        raise RuntimeError(f"privacy={confirmed} security={findings}")
    print(json.dumps({"status": "FINAL_CANDIDATE_PREPARED", "baton_words": baton_words, "baton_sha256": hashlib.sha256(baton_bytes).hexdigest(), "final_paths": len(final_paths), "owner_paths": len(all_owner), "json_parses": json_count, "privacy_confirmed": 0, "security_findings": 0, "counts": COUNTS, "outcomes": OUTCOMES}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
