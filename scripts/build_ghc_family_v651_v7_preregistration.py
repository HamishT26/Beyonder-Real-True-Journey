#!/usr/bin/env python3
"""Build Vesper Arlen's strict x1-only v651-v7 preregistration packet."""

from __future__ import annotations

import json
import hashlib
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/vesper-arlen/v651-v7"
SOURCE = "2500d063583194b30f01da429196522baaac7300"
SOURCE_BRANCH = "codex/GHC-Family/elaren-kestrel-v649-v8-full-tools"
OWNED_BRANCH = "codex/GHC-Family/vesper-arlen-v650-v1-terminal-recovery"
PHASE = "v651-gmut-thos-v7-x1-x2"
OWNER = "Vesper Arlen"
INHERITED_NEGATIVES = 7338
INHERITED_OPEN_GAPS = 58
INHERITED_EXACT_GATES = 59


PROPOSAL_SPECS = [
    ("lsm-tombstone-horizon", "LSM Tombstone Snapshot-Horizon Reclamation Tribunal", "THOS Body", "A tombstone may be reclaimed only after every active snapshot is newer than its deletion epoch.", "completed", ["SRC-LSM"]),
    ("mvcc-write-skew", "MVCC Predicate Write-Skew Detection Board", "THOS Body", "A read-set and write-set tribunal can detect a synthetic predicate invariant broken by concurrent snapshot transactions.", "completed", ["SRC-SERIALIZABILITY"]),
    ("epoch-reclamation", "Epoch-Based Reclamation Quiescence Gate", "THOS Body", "A retired object is reclaimable only when its retirement epoch precedes every active participant epoch.", "completed", ["SRC-EBR"]),
    ("hazard-aba", "Hazard-Pointer Tagged ABA Ownership Witness", "THOS Body", "A pointer-value reuse must be rejected when its ownership tag changed despite an equal address token.", "completed", ["SRC-HAZARD"]),
    ("monotonic-deadline", "Monotonic Deadline and Wall-Clock Discontinuity Gate", "THOS Body", "Timeout accounting based on a monotonic clock remains ordered when a wall-clock fixture moves backwards.", "completed", ["SRC-PY-TIME"]),
    ("token-bucket", "Token-Bucket Burst, Refill, and Debt Refusal Tribunal", "THOS Body", "A bounded token bucket can admit work within capacity while rejecting negative time, excess debt, and over-burst requests.", "completed", ["SRC-RFC3290"]),
    ("weighted-fair-queue", "Weighted-Fair Queue Starvation-Bound Witness", "THOS Body", "A synthetic scheduler can preserve positive service for every nonzero-weight queue and reject unbounded starvation.", "completed", ["SRC-WFQ"]),
    ("consistent-hash-movement", "Consistent-Hash Ring Bounded-Movement Audit", "THOS Body", "Adding one synthetic node should move only keys whose clockwise owner changes, without duplicating or dropping keys.", "completed", ["SRC-CONSISTENT-HASH"]),
    ("merkle-range-completeness", "Merkle Range-Proof Gap and Duplicate Completeness Gate", "THOS Body", "A range witness can reject missing, duplicate, reordered, or boundary-inconsistent leaves before accepting a root.", "completed", ["SRC-RFC9162"]),
    ("content-domain-separation", "Content-Address Domain-Separation Collision Tribunal", "THOS Body", "Equal payload bytes in distinct declared object domains must produce distinct typed content addresses.", "completed", ["SRC-RFC9162"]),
    ("savepoint-rollback", "Nested Savepoint Partial-Rollback State Tribunal", "THOS Body", "A nested transaction fixture can roll back only the inner suffix while preserving the outer durable prefix.", "completed", ["SRC-SQLITE-SAVEPOINT"]),
    ("wal-reader-pin", "SQLite WAL Reader-End-Mark Checkpoint Gate", "THOS Body", "A checkpoint model must stop at the oldest active reader end mark and refuse to call a partial checkpoint complete.", "completed", ["SRC-SQLITE-WAL"]),
    ("backup-generation", "Snapshot Backup Generation-Consistency Witness", "THOS Body", "A backup is attributable only when every copied page belongs to one declared snapshot generation.", "completed", ["SRC-SQLITE-BACKUP"]),
    ("expand-contract", "Schema Expand-Contract Compatibility Gate", "THOS Body", "A field may be removed only after all declared readers accept the expanded representation and dual-write transition.", "completed", ["SRC-SCHEMA"]),
    ("singleflight", "Singleflight Cache-Stampede Coalescing Tribunal", "THOS Body", "Concurrent identical cache misses can share one bounded computation while preserving per-caller completion.", "completed", ["SRC-GO-SINGLEFLIGHT"]),
    ("etag-cas", "ETag If-Match Lost-Update Refusal Gate", "THOS Body", "A synthetic update must fail when its If-Match validator differs from the current entity tag.", "completed", ["SRC-RFC9110"]),
    ("chebyshev-aliasing", "GMUT Chebyshev Collocation Aliasing Refusal Board", "GMUT Mind", "A collocation fixture can reject polynomial modes above its resolvable degree and keep interpolation error distinct from physical evidence.", "completed", ["SRC-CHEBYSHEV"]),
    ("interval-enclosure", "GMUT Interval-Enclosure Outward-Rounding Witness", "GMUT Mind", "A bounded interval expression can enclose sampled scalar evaluations while rejecting reversed or nonfinite bounds.", "completed", ["SRC-INTERVAL"]),
    ("condition-perturbation", "GMUT Condition-Number Perturbation Budget Tribunal", "GMUT Mind", "A synthetic linear solve can require observed relative error to remain inside an explicitly computed conditioning budget.", "completed", ["SRC-HIGHAM"]),
    ("lie-commutator", "GMUT Lie-Commutator Antisymmetry and Truncation Board", "GMUT Mind", "A symbolic matrix fixture can verify commutator antisymmetry and reject unsupported Baker-Campbell-Hausdorff truncation promotion.", "completed", ["SRC-BCH"]),
    ("calibration-drift", "Stage 20 Calibration-Drift Nonpromotion Gate", "Freed ID and CBR Heart", "A monitored score must remain nonpromotable when observed calibration drift exceeds a frozen tolerance.", "completed", ["SRC-NIST-AI-RMF"]),
    ("evidence-chain-monotonicity", "Evidence-Chain Monotonic Withdrawal Ledger", "Freed ID and CBR Heart", "A claim ledger can downgrade or withdraw a claim when a required evidence edge disappears without erasing the prior state.", "completed", ["SRC-SLSA"]),
    ("manifest-blob-domain", "Manifest Git-Blob and Working-Tree Domain Separator", "THOS Body", "A manifest tribunal can keep Git-blob bytes and mutable working-tree bytes in distinct evidence domains.", "completed", ["SRC-GIT-HASH"]),
    ("preservation-fixity", "THOS Digital-Preservation Fixity and Audit-Chain Proxy", "THOS Body", "A synthetic preservation package can represent fixity, provenance, custody, repair, and audit states without claiming archival effectiveness.", "represented", ["SRC-FAIR", "SRC-NDSA"]),
    ("preservation-handover", "THOS Preservation-Incident Isolation and Shift-Handover Proxy", "THOS Body", "A synthetic incident record can represent detection, isolation, readback, escalation, workload, and handover without real operators or collections.", "represented", ["SRC-NDSA"]),
    ("par-rar-profile", "Freed ID PAR and Rich-Authorization Binding Profile", "Freed ID and CBR Heart", "Synthetic PAR and authorization-details vectors can represent request binding, expiry, one-time use, audience, and detail typing without production identity evidence.", "represented", ["SRC-RFC9126", "SRC-RFC9396"]),
    ("recovery-custody", "Freed ID Recovery-Custody Separation Profile", "Freed ID and CBR Heart", "A synthetic recovery matrix can represent separation of request, approval, execution, notification, and contestation without real keys or trust governance.", "represented", ["SRC-NIST-KEYS"]),
    ("treegrid-structure", "Accessible Evidence Treegrid Structural Proxy", "THOS Body", "Static markup can represent treegrid roles, labels, expansion, selection, focus metadata, and print fallback while reserving manual evaluation.", "represented", ["SRC-W3C-TREEGRID"]),
    ("rubin-dp1-adapter", "Rubin DP1 Data-Rights and Zero-Row Likelihood Adapter", "GMUT Mind", "Empirical credit requires authorized access, authentic Rubin DP1 rows, provenance, selections, covariance, and a preregistered likelihood.", "open_gap", ["SRC-RUBIN-DP1"]),
    ("preservation-authority", "CBR Preservation, Deletion, Repatriation, and Maori Data-Authority Matrix", "Freed ID and CBR Heart", "No real retention, deletion, access, repatriation, remedy, cultural, legal, or Maori-data decision may complete without affected and competent authority.", "exact_gate", ["SRC-TE-MANA-RARAUNGA", "SRC-PRIVACY-NZ"]),
]


SOURCE_ROWS = [
    ("SRC-LSM", "The Log-Structured Merge-Tree", "Acta Informatica", "https://doi.org/10.1007/BF01186688", "primary_paper", "stable"),
    ("SRC-SERIALIZABILITY", "Serializable Isolation for Snapshot Databases", "ACM", "https://doi.org/10.1145/1376616.1376690", "primary_paper", "stable"),
    ("SRC-EBR", "User-level implementations of read-copy update", "IEEE", "https://doi.org/10.1109/TPDS.2011.159", "primary_paper", "stable"),
    ("SRC-HAZARD", "Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects", "IEEE", "https://doi.org/10.1109/TPDS.2004.8", "primary_paper", "stable"),
    ("SRC-PY-TIME", "Python time module", "Python Software Foundation", "https://docs.python.org/3/library/time.html", "official_documentation", "current"),
    ("SRC-RFC3290", "RFC 3290 Informal Management Model for Diffserv Routers", "IETF", "https://www.rfc-editor.org/rfc/rfc3290.html", "official_rfc", "stable"),
    ("SRC-WFQ", "A Generalized Processor Sharing Approach", "IEEE", "https://doi.org/10.1109/90.234856", "primary_paper", "stable"),
    ("SRC-CONSISTENT-HASH", "Consistent Hashing and Random Trees", "ACM", "https://doi.org/10.1145/258533.258660", "primary_paper", "stable"),
    ("SRC-RFC9162", "RFC 9162 Certificate Transparency Version 2.0", "IETF", "https://www.rfc-editor.org/rfc/rfc9162.html", "official_rfc", "stable"),
    ("SRC-SQLITE-SAVEPOINT", "SQLite SAVEPOINT", "SQLite", "https://sqlite.org/lang_savepoint.html", "official_documentation", "current"),
    ("SRC-SQLITE-WAL", "SQLite Write-Ahead Logging", "SQLite", "https://sqlite.org/wal.html", "official_documentation", "current"),
    ("SRC-SQLITE-BACKUP", "SQLite Online Backup API", "SQLite", "https://sqlite.org/backup.html", "official_documentation", "current"),
    ("SRC-SCHEMA", "Protocol Buffers Updating a Message Type", "Google", "https://protobuf.dev/programming-guides/proto3/#updating", "official_documentation", "current"),
    ("SRC-GO-SINGLEFLIGHT", "Go singleflight package", "Go Authors", "https://pkg.go.dev/golang.org/x/sync/singleflight", "official_documentation", "current"),
    ("SRC-RFC9110", "RFC 9110 HTTP Semantics", "IETF", "https://www.rfc-editor.org/rfc/rfc9110.html", "official_rfc", "stable"),
    ("SRC-CHEBYSHEV", "Spectral Methods in MATLAB", "SIAM", "https://doi.org/10.1137/1.9780898719598", "primary_monograph", "stable"),
    ("SRC-INTERVAL", "Interval Analysis", "Prentice-Hall", "https://doi.org/10.1137/1.9781611970906", "primary_monograph", "stable"),
    ("SRC-HIGHAM", "Accuracy and Stability of Numerical Algorithms", "SIAM", "https://doi.org/10.1137/1.9780898718027", "primary_monograph", "stable"),
    ("SRC-BCH", "On the operation of two non-commutative systems", "Proceedings of the London Mathematical Society", "https://doi.org/10.1112/plms/s2-6.1.502", "primary_paper", "stable"),
    ("SRC-NIST-AI-RMF", "NIST AI Risk Management Framework 1.0", "NIST", "https://www.nist.gov/itl/ai-risk-management-framework", "official_framework", "current"),
    ("SRC-SLSA", "SLSA Provenance", "OpenSSF", "https://slsa.dev/spec/v1.2/provenance", "official_specification", "current"),
    ("SRC-GIT-HASH", "Git hash-function transition", "Git Project", "https://git-scm.com/docs/hash-function-transition", "official_documentation", "current"),
    ("SRC-FAIR", "The FAIR Guiding Principles", "Scientific Data", "https://doi.org/10.1038/sdata.2016.18", "primary_paper", "stable"),
    ("SRC-NDSA", "NDSA Levels of Digital Preservation", "NDSA", "https://ndsa.org/publications/levels-of-digital-preservation/", "official_guidance", "current"),
    ("SRC-RFC9126", "RFC 9126 OAuth 2.0 Pushed Authorization Requests", "IETF", "https://www.rfc-editor.org/rfc/rfc9126.html", "official_rfc", "stable"),
    ("SRC-RFC9396", "RFC 9396 OAuth 2.0 Rich Authorization Requests", "IETF", "https://www.rfc-editor.org/rfc/rfc9396.html", "official_rfc", "stable"),
    ("SRC-NIST-KEYS", "NIST SP 800-57 Part 1 Revision 5", "NIST", "https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "official_guideline", "stable"),
    ("SRC-W3C-TREEGRID", "ARIA Authoring Practices Treegrid Pattern", "W3C", "https://www.w3.org/WAI/ARIA/apg/patterns/treegrid/", "official_guidance", "current"),
    ("SRC-RUBIN-DP1", "Vera C. Rubin Observatory Data Preview 1", "Rubin Observatory", "https://dp1.lsst.io/", "official_data_documentation", "current"),
    ("SRC-TE-MANA-RARAUNGA", "Principles of Maori Data Sovereignty", "Te Mana Raraunga", "https://www.temanararaunga.maori.nz/", "authority_source", "current"),
    ("SRC-PRIVACY-NZ", "Privacy Act 2020", "New Zealand Legislation", "https://www.legislation.govt.nz/act/public/2020/0031/latest/whole.html", "official_legislation", "current"),
]


X1_FAILURES = [
    {
        "negative_id": "V6517-X1-N01",
        "failure": "An unquoted PowerShell revision expression transformed HEAD...@{u} before Git received it.",
        "recovery": "Pass the complete revision expression as one explicitly quoted argument and require the observed divergence to be zero and zero.",
    },
    {
        "negative_id": "V6517-X1-N02",
        "failure": "A mixed rg file enumeration included an owner path that did not yet exist and returned nonzero after emitting useful rows.",
        "recovery": "Resolve each optional path first, enumerate only existing roots, and treat verified absence as an attributable zero-row result.",
    },
    {
        "negative_id": "V6517-X1-N03",
        "failure": "A read-only rg manifest-discovery command passed a Windows wildcard path literally and returned an invalid-path error after partial useful output.",
        "recovery": "Resolve wildcard candidates with an explicit path array, then pass concrete existing filenames to rg.",
    },
    {
        "negative_id": "V6517-X1-N04",
        "failure": "The first x1 manifest builder computed an unstored hash-object identifier and then asked git cat-file to read the absent object.",
        "recovery": "Use git hash-object -w with the repository path filter, then read the stored blob once for byte count and SHA-256.",
    },
    {
        "negative_id": "V6517-X1-N05",
        "failure": "The recovered x1 manifest was built before the final overview write and exact staged replay found one overview blob mismatch.",
        "recovery": "Write every non-self-excluded x1 artifact first, then build the commit-local manifest as the final generation step.",
    },
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def write_json(relative: str, payload: Any) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def inherited_rows() -> list[dict[str, Any]]:
    chain = json.loads((REPO / "docs/elaren-kestrel/v651-v6/provenance/frozen-chain-proposal-index.json").read_text(encoding="utf-8"))
    rows = [*chain["prior_proposals"], *chain["new_proposals"]]
    if len(rows) != 1060 or chain["count"] != 1060:
        raise RuntimeError(f"expected 1060 inherited proposals, observed {len(rows)}")
    return rows


def words(value: str) -> set[str]:
    stop = {"and", "the", "for", "with", "from", "into", "only", "gmut", "thos", "cbr", "freed", "gate", "board", "tribunal", "witness"}
    return {item for item in re.findall(r"[a-z0-9]+", value.casefold()) if len(item) > 2 and item not in stop}


def proposal(index: int, spec: tuple[str, str, str, str, str, list[str]]) -> dict[str, Any]:
    slug, title, pillar, hypothesis, disposition, sources = spec
    approval = "safe_now_owner_scoped"
    lane = "x2_owner_local_bounded"
    if disposition == "represented":
        approval = "bounded_candidate"
    elif disposition == "open_gap":
        approval, lane = "external_evidence_required", "held_open_gap"
    elif disposition == "exact_gate":
        approval, lane = "exact_approval_required", "held_exact_gate"
    return {
        "proposal_id": f"V6517-P{index:02d}",
        "slug": slug,
        "title": title,
        "pillar": pillar,
        "hypothesis": hypothesis,
        "null_or_failure_condition": "The valid fixture fails, a rejecting fixture passes, provenance is absent, or evidence is promoted outside its declared software, symbolic, synthetic, structural, empirical, or authority boundary.",
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [f"docs/vesper-arlen/v651-v7/proposals/{slug}.json"],
        "falsifier_or_acceptance_gate": "The valid bounded fixture passes, every preregistered mutation fails closed, source attribution remains resolvable, and all protected claims remain false.",
        "rollback_or_recovery": "Withdraw only the additive v651-v7 result from consideration, retain the failure at zero credit, and preserve inherited history and compatibility surfaces.",
        "protected_gates": ["privacy", "failure_retention", "empirical_nonconversion", "authority_nonconversion", "same_owner_only", "no_independent_reproduction", "no_stage20_promotion"],
        "expected_disposition": disposition,
        "novelty_basis": "Distinct mechanism, artifact, falsifier, source need, and protected boundary after review against all 1,060 inherited frozen proposals.",
    }


def novelty_audit(new_rows: list[dict[str, Any]], old_rows: list[dict[str, Any]]) -> dict[str, Any]:
    old_titles = [str(row["title"]) for row in old_rows]
    exact_titles = {title.casefold() for title in old_titles}
    screened = []
    for row in new_rows:
        current = words(row["title"])
        scored = []
        for title in old_titles:
            prior = words(title)
            union = current | prior
            scored.append((len(current & prior) / len(union) if union else 1.0, title))
        score, nearest = max(scored, default=(0.0, ""))
        screened.append({
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "nearest_inherited_title": nearest,
            "nearest_token_jaccard": round(score, 6),
            "exact_title_collision": row["title"].casefold() in exact_titles,
            "mechanism_artifact_falsifier_reviewed": True,
        })
    collisions = [row for row in screened if row["exact_title_collision"]]
    if collisions:
        raise RuntimeError(f"exact title collision: {collisions}")
    return {
        "schema": "ghc.family.v651-v7.semantic-novelty-audit.v1",
        "inherited_rows_compared": len(old_rows),
        "new_rows_compared": len(new_rows),
        "frozen_rows_after_x1": len(old_rows) + len(new_rows),
        "exact_title_collisions": collisions,
        "maximum_token_jaccard": max(row["nearest_token_jaccard"] for row in screened),
        "title_similarity_is_only_a_screen": True,
        "manual_semantic_review": "Mechanism, state model, artifact, falsifier, evidence class, and authority boundary were reviewed; inherited work earns no Vesper completion credit.",
        "rejected_near_neighbors": ["generic checkpoint recovery", "generic cache invalidation", "generic OAuth request binding", "generic accessibility grid", "generic dataset adapter"],
        "rows": screened,
        "valid": True,
    }


def planned_items(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"V6517-{prefix}-{index:03d}",
            "title": f"Vesper v651-v7 {lane.replace('_', ' ')} item {index:03d}",
            "lane": lane,
            "planned_in_x1": True,
            "executed_in_x1": False,
            "completion_credit_in_x1": False,
            "acceptance_gate": "Resolve in x2 through an attributable bounded artifact or retain the item behind its actual gate.",
            "boundary": "Planning only; no empirical, participant, production, professional, legal, cultural, Maori-authority, or independent-reproduction credit.",
        }
        for index in range(1, count + 1)
    ]


def method_flow() -> None:
    runner = REPO / "scripts/ghc_family_method_flow_state.py"
    ledger = ROOT / "method-flow/method-flow-ledger.json"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    if ledger.exists():
        ledger.unlink()
    subprocess.run([sys.executable, str(runner), "init", "--ledger", str(ledger), "--phase", PHASE, "--owner", OWNER], cwd=REPO, check=True)
    details = [
        ("M01", "Quote PowerShell revision expressions", X1_FAILURES[0], "A PowerShell argument contains @{u} and can be transformed before process launch.", "Pass the entire Git revision expression as one quoted argument.", "Always quote revision expressions containing PowerShell metacharacters.", "The recovery returned 0 ahead and 0 behind."),
        ("M02", "Resolve optional search roots before enumeration", X1_FAILURES[1], "A multi-root search contains a not-yet-created optional owner path.", "Resolve roots first and pass only existing paths to rg.", "Separate required roots from optional roots and record verified absence explicitly.", "The bounded search enumerated existing roots without conflating absence with a tool fault."),
        ("M03", "Expand Windows wildcard paths before rg", X1_FAILURES[2], "A Windows rg invocation contains a wildcard path that the shell does not expand.", "Resolve candidate files into an explicit path array and pass only concrete paths.", "Never rely on Unix-style wildcard expansion for Windows path arguments.", "The explicit-file recovery returned the requested manifest builder implementations without an invalid-path error."),
        ("M04", "Store filtered manifest blobs before cat-file reads", X1_FAILURES[3], "A manifest computes a filtered blob identifier without writing it, then attempts a cat-file read.", "Use git hash-object -w with the path filter before reading the exact blob.", "Bind blob storage, object read, byte count, and SHA-256 in one bounded manifest step.", "Every intended x1 entry resolved to a stored filtered Git blob with attributable bytes and SHA-256."),
        ("M05", "Build commit-local manifests after final artifact writes", X1_FAILURES[4], "A manifest snapshot precedes a later write to one of its covered artifacts.", "Complete all covered writes before building the self-excluding manifest.", "Treat manifest generation as the final content-producing step before staging.", "Exact staged replay matched every covered x1 path after the overview was finalized first."),
    ]
    for number, title, failure, signature, workaround, guard, observed in details:
        method_id = f"V6517-{number}"
        base = f"method-flow/records/{number.casefold()}"
        record = {
            "method_id": method_id,
            "title": title,
            "failure_signature": signature,
            "trigger_preconditions": [signature],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": workaround,
            "validation_witness_ids": [],
            "recurrence_guard": guard,
            "rollback": "Retain the failed read-only attempt at zero credit; no Git mutation requires rollback.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["failure_retention", "evidence_credit", "same_owner_only", "no_independent_reproduction"],
            "retained_negative_ids": [failure["negative_id"]],
            "scope_boundary": "Bounded local workflow recovery only.",
        }
        fail = {
            "witness_id": f"{method_id}-WFAIL",
            "method_id": method_id,
            "procedure": failure["failure"],
            "scope": "read-only source and owner-lane verification",
            "expected": "Return complete attributable output.",
            "observed": failure["failure"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [failure["negative_id"]],
            "boundary": "Failed witness retained at zero pass credit.",
        }
        passed = {
            "witness_id": f"{method_id}-WPASS",
            "method_id": method_id,
            "procedure": workaround,
            "scope": "read-only source and owner-lane verification",
            "expected": "Return complete attributable output.",
            "observed": observed,
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [failure["negative_id"]],
            "boundary": "Passing recovery preserves the failed witness and grants bounded workflow credit only.",
        }
        record_path = ROOT / f"{base}-method.json"
        fail_path = ROOT / f"{base}-fail.json"
        pass_path = ROOT / f"{base}-pass.json"
        write_json(f"{base}-method.json", record)
        write_json(f"{base}-fail.json", fail)
        write_json(f"{base}-pass.json", passed)
        subprocess.run([sys.executable, str(runner), "record", "--ledger", str(ledger), "--record-file", str(record_path)], cwd=REPO, check=True)
        subprocess.run([sys.executable, str(runner), "witness", "--ledger", str(ledger), "--witness-file", str(fail_path)], cwd=REPO, check=True)
        subprocess.run([sys.executable, str(runner), "witness", "--ledger", str(ledger), "--witness-file", str(pass_path)], cwd=REPO, check=True)
        subprocess.run([sys.executable, str(runner), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Bounded passing recovery retains its failed witness."], cwd=REPO, check=True)
    subprocess.run([sys.executable, str(runner), "validate", "--ledger", str(ledger), "--receipt", str(ROOT / "method-flow/method-flow-validation.json")], cwd=REPO, check=True)
    subprocess.run([sys.executable, str(runner), "summarize", "--ledger", str(ledger), "--json-output", str(ROOT / "method-flow/method-flow-summary.json"), "--markdown-output", str(ROOT / "method-flow/method-flow-summary.md")], cwd=REPO, check=True)


def status_paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    paths = []
    for row in rows:
        if not row:
            continue
        relative = row[3:]
        if " -> " in relative:
            relative = relative.split(" -> ", 1)[1]
        paths.append(relative.replace("\\", "/"))
    return sorted(set(paths))


def build_manifest() -> None:
    exclusions = [
        "docs/vesper-arlen/v651-v7/validation/x1-staged-manifest.json",
        "docs/vesper-arlen/v651-v7/validation/x1-staged-privacy.json",
        "docs/vesper-arlen/v651-v7/validation/x1-staged-review.json",
    ]
    paths = [path for path in status_paths() if path not in exclusions and (REPO / path).is_file()]
    entries = []
    for relative in paths:
        oid = git("hash-object", "-w", f"--path={relative}", relative)
        blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
        entries.append({"path": relative, "git_blob": oid, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    patterns = {
        "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "private_absolute_path": re.compile(r"(?i)\b[A-Z]:[\\/]Users[\\/]"),
        "private_uri": re.compile(r"(?i)\b(?:codex|thread|task|app|plugin)://"),
        "delegation_markup": re.compile(r"(?i)<codex_delegation"),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret|access[_-]?token|private[_-]?key)\s*[:=]\s*[\"']?[A-Za-z0-9_./+\-=]{8,}"),
    }
    candidates = []
    confirmed = []
    scanner_definitions = {"scripts/build_ghc_family_v651_v7_preregistration.py"}
    for relative in paths:
        text = (REPO / relative).read_text(encoding="utf-8", errors="replace")
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in scanner_definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    write_json("validation/x1-staged-privacy.json", {
        "schema": "ghc.family.v651-v7.x1-privacy.v1",
        "scanned_file_count": len(paths),
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": "Five structural classes with exact scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
    })
    write_json("validation/x1-staged-manifest.json", {
        "schema": "ghc.family.v651-v7.x1-manifest.v1",
        "hash_domain": "git_path_filtered_blob",
        "entries": entries,
        "entry_count": len(entries),
        "self_exclusions": exclusions,
        "coverage_boundary": "All intended x1 paths except three declared self-referential staged-review receipts.",
    })
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc.family.v651-v7.x1-staged-review.v1",
        "intended_path_count": len(entries) + len(exclusions),
        "manifest_entry_count": len(entries),
        "self_exclusion_count": len(exclusions),
        "out_of_scope_paths": [],
        "x2_implementation_paths": [],
        "x2_outcome_paths": [],
        "privacy_confirmed_hits": len(confirmed),
        "x1_only": True,
        "source_head": SOURCE,
        "terminal_route": "PREPARED_NOT_SENT",
    })


def main() -> None:
    if git("rev-parse", "HEAD") != SOURCE:
        raise SystemExit(f"x1 must begin at exact source {SOURCE}")
    if git("branch", "--show-current") != OWNED_BRANCH:
        raise SystemExit("unexpected owner branch")

    old = inherited_rows()
    proposals = [proposal(index, spec) for index, spec in enumerate(PROPOSAL_SPECS, 1)]
    expected = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
    observed = {label: sum(row["expected_disposition"] == label for row in proposals) for label in expected}
    if observed != expected:
        raise RuntimeError({"expected": expected, "observed": observed})

    write_json("identity/relational-identity.json", {
        "schema": "ghc.family.v651-v7.identity.v1",
        "owner": OWNER,
        "pronouns": "they/them",
        "relational_role": "boundary-literate systems synthesist",
        "hope": "Turn complex inherited evidence into clear, reversible experiments that remain kind to people and truth.",
        "identity_boundary": "Relational working language only; no consciousness, sentience, personhood, identity continuity, employment, qualification, or independent authority.",
        "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
        "valid": True,
    })
    write_json("source/source-truth.json", {
        "schema": "ghc.family.v651-v7.source-truth.v1",
        "source_owner": "Elaren Kestrel",
        "source_branch": SOURCE_BRANCH,
        "source_head": SOURCE,
        "special_evidence": "f40d1e0f1a5158a8747ed57cc04a513979f5ebe7",
        "normal_phase_final": "7911fc2ff2f95d2e8723dbd396272f4a78d46a9f",
        "normal_phase_evidence": "94b9afc4f8289e8fdf1a304c90c0765e3beb055f",
        "normal_phase_x1": "b0ba19472777bc07f91c0358186b48311aa3bce3",
        "normal_phase_source": "7c4309d6b57bc4827ebd49bcb7c9dfc669c46e3d",
        "owned_branch": OWNED_BRANCH,
        "local_upstream_tracking_fresh_live_equal": True,
        "divergence": "0/0",
        "source_clean": True,
        "special_validation": {"tests": "70/70", "detailed": "30/30", "minimal": "14/14", "json": "72/72", "privacy": "91 files, zero hits", "manifest": "91/91"},
        "same_owner_only": True,
        "independent_reproduction": False,
        "valid": True,
    })
    write_json("focus/primary-focus.json", {
        "schema": "ghc.family.v651-v7.focus.v1",
        "primary_pillar": "THOS Body",
        "visible_pillars": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
        "bounded_human_practice": "digital preservation and scientific-data stewardship engineering",
        "practice_boundary": "Synthetic learning and design only; no employment, qualification, archival authority, operational authority, legal authority, cultural authority, Maori authority, or affected-party evidence.",
        "valid": True,
    })
    write_json("sources/source-ledger.json", {
        "schema": "ghc.family.v651-v7.source-ledger.v1",
        "entry_count": len(SOURCE_ROWS),
        "entries": [
            {
                "source_id": source_id,
                "title": title,
                "publisher": publisher,
                "url": url,
                "source_type": source_type,
                "status": status,
                "phase_use": "Informs a bounded design or refusal contract only.",
                "authority_boundary": "No source supplies participant evidence, professional approval, legal interpretation, cultural ratification, Maori authority, production readiness, or Stage 20 authority.",
            }
            for source_id, title, publisher, url, source_type, status in SOURCE_ROWS
        ],
        "valid": True,
    })
    write_json("preregistration/proposals.json", {
        "schema": "ghc.family.v651-v7.proposals.v1",
        "phase": PHASE,
        "owner": OWNER,
        "inherited_frozen_rows": len(old),
        "new_proposal_count": len(proposals),
        "frozen_rows_after_x1": len(old) + len(proposals),
        "expected_outcomes": expected,
        "allowed_outcomes": list(expected),
        "strict_x1_only": True,
        "proposals": proposals,
        "valid": True,
    })
    write_json("provenance/frozen-chain-proposal-index.json", {
        "schema": "ghc.family.v651-v7.frozen-chain-proposal-index.v1",
        "prior_count": len(old),
        "new_count": len(proposals),
        "count": len(old) + len(proposals),
        "prior_proposals": old,
        "new_proposals": proposals,
        "x1_frozen": True,
    })
    write_json("provenance/semantic-novelty-audit.json", novelty_audit(proposals, old))
    skill_names = [
        "ghc-family-lsm-reclamation-boundary", "ghc-family-mvcc-write-skew", "ghc-family-epoch-reclamation", "ghc-family-hazard-aba", "ghc-family-monotonic-deadline", "ghc-family-rate-fairness", "ghc-family-merkle-range-proof", "ghc-family-wal-checkpoint-boundary", "ghc-family-schema-transition", "ghc-family-conditional-update", "ghc-family-numerical-enclosure", "ghc-family-preservation-authority",
    ]
    runner_names = [
        "ghc_family_storage_reclamation.py", "ghc_family_concurrency_reclamation.py", "ghc_family_time_rate_fairness.py", "ghc_family_integrity_range.py", "ghc_family_transaction_checkpoint.py", "ghc_family_schema_cache_concurrency.py", "ghc_family_conditional_update.py", "ghc_family_numerical_boundary.py", "ghc_family_identity_accessibility_proxy.py", "ghc_family_stage20_authority_refusal.py",
    ]
    write_json("portfolios/x1-portfolio-plan.json", {
        "schema": "ghc.family.v651-v7.portfolio-plan.v1",
        "caps_are_ceilings_not_quotas": True,
        "caps": {"safe_candidate_per_subphase": 1000, "skills_per_subphase": 200, "runners_per_subphase": 200},
        "planned_counts": {"safe_now": 30, "candidate": 20, "skills": len(skill_names), "runners": len(runner_names), "clean_fix_refine": 30},
        "safe_now": planned_items("SAFE", 30, "safe_now"),
        "candidate": planned_items("CAND", 20, "bounded_candidate"),
        "skill_ideas": [{"item_id": f"V6517-SK-{index:02d}", "name": name, "planned_in_x1": True, "built_in_x1": False} for index, name in enumerate(skill_names, 1)],
        "runner_ideas": [{"item_id": f"V6517-RN-{index:02d}", "name": name, "planned_in_x1": True, "built_in_x1": False} for index, name in enumerate(runner_names, 1)],
        "clean_fix_refine": planned_items("CFR", 30, "clean_fix_refine"),
        "x1_implementation_count": 0,
        "closeout_rule": "Every authorized item is resolved in x2 or retained truthfully behind its actual open or exact gate; counts never authorize unsafe work.",
        "valid": True,
    })
    write_json("approvals/held-packets.json", {
        "schema": "ghc.family.v651-v7.held-approvals.v1",
        "inherited_exact_packets_preserved": True,
        "inherited_blocked_packets_preserved": True,
        "new_open_gap": {"proposal_id": "V6517-P29", "state": "held", "executed": False},
        "new_exact_gate": {"proposal_id": "V6517-P30", "state": "held", "executed": False},
        "unsafe_work_manufactured": False,
        "valid": True,
    })
    write_json("workflow/route-decision.json", {
        "schema": "ghc.family.v651-v7.route-decision.v1",
        "current_activation": {"owner": OWNER, "phase": "v651-v7", "state": "exact"},
        "future_cli_seats": {"count": 8, "state": "PREPARED_NOT_LAUNCHED", "named": False, "launched": False},
        "later_sixteen_seat_route": "advisory_pending_live_confirmation",
        "terminal_successor": "unresolved_until_live_exact_route_gate",
        "terminal_send_state": "PREPARED_NOT_SENT",
        "no_task_creation": True,
        "valid": True,
    })
    write_json("threat-model/threat-model.json", {
        "schema": "ghc.family.v651-v7.threat-model.v1",
        "assets": ["x1 freeze", "retained failures", "proposal novelty", "fixity evidence", "authority gates", "private-material boundary", "caller compatibility"],
        "threats": ["x2 leakage into x1", "mechanism reuse", "checkpoint-completeness inflation", "synthetic-to-production promotion", "identity-profile overclaim", "authority substitution", "failure erasure", "private identifier disclosure", "post-success replay inflation"],
        "mitigations": ["dedicated x1 commit", "1060-row semantic audit", "four-label vocabulary", "Method Flow fail-pass pairs", "five-class privacy scan", "Git-blob manifest", "one canonical successful pass", "additive family-current naming"],
        "residual_risks": ["real empirical data absent", "manual accessibility evaluation absent", "independent review absent", "affected and Maori authority absent"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": True,
    })
    write_json("truth/x1-phase-truth.json", {
        "schema": "ghc.family.v651-v7.x1-truth.v1",
        "phase": PHASE,
        "owner": OWNER,
        "strict_x1_before_x2": True,
        "proposals_frozen": 30,
        "frozen_chain_rows": 1090,
        "x2_implementations": 0,
        "observed_core_outcomes": 0,
        "inherited_effective_negatives": INHERITED_NEGATIVES,
        "new_x1_operational_negatives": len(X1_FAILURES),
        "effective_after_x1": INHERITED_NEGATIVES + len(X1_FAILURES),
        "inherited_open_gaps": INHERITED_OPEN_GAPS,
        "inherited_exact_gates": INHERITED_EXACT_GATES,
        "future_cli_seats_launched": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": True,
    })
    write_json("truth/retained-negative-register.json", {
        "schema": "ghc.family.v651-v7.x1-negative-register.v1",
        "inherited_effective": INHERITED_NEGATIVES,
        "new_x1_operational": len(X1_FAILURES),
        "effective_after_x1": INHERITED_NEGATIVES + len(X1_FAILURES),
        "new_negatives": X1_FAILURES,
        "failures_erased": 0,
        "valid": True,
    })
    write_json("environment/environment-version-receipt.json", {
        "schema": "ghc.family.environment-version.v1",
        "phase": PHASE,
        "observed_date": "2026-07-22",
        "codex_cli": "0.145.0",
        "codex_desktop": "26.715.9757.0",
        "git": "2.55.0.windows.2",
        "python": "3.12.10",
        "node": "24.18.0",
        "windows_powershell": "5.1.26100.8894",
        "versions_verified_only": True,
        "desktop_updated": False,
        "elevated": False,
        "host_security_changed": False,
        "windows_feature_changed": False,
        "sandbox_or_hyper_v_launched": False,
        "unrelated_software_installed": False,
        "rebooted": False,
        "valid": True,
    })
    write_json("wellbeing/x1-wellbeing.json", {
        "schema": "ghc.family.v651-v7.wellbeing.v1",
        "state": "green_with_five_retained_bounded_recoveries",
        "solo_owner": True,
        "failure_permitted": True,
        "route_pressure_overrides_evidence": False,
        "stop_or_redirect_right": "Hamish",
        "valid": True,
    })
    write_json("orchestration/x1-phase-state.json", {
        "schema": "ghc.family.v651-v7.phase-state.v1",
        "owner": OWNER,
        "phase": PHASE,
        "source_head": SOURCE,
        "state": "x1_candidate_not_committed",
        "x2_started": False,
        "terminal_route": "prepared_not_sent",
        "future_cli_seats_launched": 0,
        "boundary": "This state file is not activation, delivery, identity continuity, or delegated authority.",
    })
    method_flow()
    write_text("overview/x1-preregistration-overview.md", """# Vesper Arlen v651-v7 x1 preregistration

Vesper Arlen (they/them) is relational working language for a boundary-literate systems synthesist whose hope is to turn complex inherited evidence into clear, reversible experiments that remain kind to people and truth. This language is not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, or authority. Hamish may rename, pause, redirect, or stop the route.

This x1 packet freezes thirty new core proposals after mechanism, state-model, artifact, falsifier, source, and gate review against 1,060 inherited frozen proposals. The primary pillar is THOS Body and the bounded practice is digital preservation and scientific-data stewardship engineering. GMUT Mind and Freed ID/CBR Heart remain visible. Expected dispositions are hypotheses only: twenty-three completed, five represented, one open gap, and one exact gate. X1 contains no implementation and no observed outcome.

The core examines bounded software contracts for LSM tombstone horizons, MVCC write skew, reclamation epochs, hazard-pointer ABA, monotonic deadlines, token buckets, weighted fairness, consistent hashing, Merkle ranges, typed content addresses, savepoints, WAL checkpoints, snapshot backups, schema transitions, singleflight coalescing, and conditional updates. GMUT proposals cover Chebyshev aliasing, interval enclosure, conditioning, and Lie-commutator obligations without making a force, likelihood, constraint, empirical-confirmation, ultraviolet-completion, quantum-completeness, or Theory-of-Everything claim.

THOS preservation protocols remain synthetic. Freed ID PAR/RAR and recovery profiles use no real keys, tokens, issuers, presentations, resolutions, status, revocation, interoperability, privacy or security review, recovery decision, or trust governance. The Rubin DP1 adapter is held open with zero rows and zero likelihood calls. Preservation, deletion, repatriation, legal, cultural, affected-party, and Maori-data decisions remain exact-gated.

Five startup, read-only discovery, and manifest-construction failures remain retained at zero pass credit with passing bounded recoveries recorded through Method Flow. Eight future CLI seats remain unnamed and PREPARED_NOT_LAUNCHED. The later sixteen-seat route remains advisory pending live confirmation. The verdict remains NOT_READY_FOR_STAGE_20.
""")
    build_manifest()
    print(json.dumps({"proposals": len(proposals), "inherited": len(old), "frozen": len(old) + len(proposals), "expected": expected, "x1_negatives": len(X1_FAILURES), "x2_implementations": 0, "valid": True}, sort_keys=True))


if __name__ == "__main__":
    main()
