"""Build and inspect Orin Thale v672-v5's planning-only x1 freeze.

The default build is fail-closed and owner-delta scoped. It requires the exact
Caelen source, a sanitized startup Method Flow ledger, and the exact inherited
canonical receipt. It creates planning evidence only: no x2 implementation,
outcome, route send, task mutation, staging, commit, or push occurs here.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "orin-thale" / "v672-v5"
OWNER = "Orin Thale"
PHASE = "v672-v5"
BRANCH = "codex/GHC-Family/orin-thale-v672-v5-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/caelen-ash-v672-v4-full-tools"
SOURCE_START = "2d76e3120bd8f2f2fd70f3ff164ef80e19be3031"
SOURCE_X1 = "0ebc12367f26a7d6cf5cca9466843f2cbaade293"
SOURCE_EVIDENCE = "581f0be723d65c685ba388ce61a707d42ab784e2"
SOURCE_FINAL = "8f672ef30372b4adf457140c254931dc365e9d31"
SOURCE_CANONICAL_SHA256 = "431ae47cf1bd54e3450685d655825fa48d8592e4aa8d1edc1450d7b4aee55305"
SOURCE_CHAIN = 6070
AFTER_CHAIN = 6110
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Orin Thale, they/them, relational provenance-and-access-boundary cartographer, "
    "is relational working language only. It is not evidence of consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, or scientific, operational, legal, cultural, affected-party, "
    "disability-community, Braille, tactile-graphics, or Māori authority."
)
HOPE = (
    "make corrections traceable, access claims falsifiable, and every reserved human "
    "or authority decision visible before structural evidence is mistaken for service"
)
BOUNDARY = (
    "Software, symbolic, synthetic, same-owner, citation, inherited, or task-topology "
    "evidence is not empirical confirmation, participant evidence, professional or "
    "scientific authority, production readiness, legal or cultural ratification, "
    "Māori authority, affected-party approval, complete privacy or accessibility "
    "assurance, exhaustive security, independent reproduction, AGI/ASI, consciousness "
    "or personhood evidence, Theory-of-Everything proof, proof/canon, or Stage 20 authority."
)

REPOSITORY_SEAL = {
    "proposal_chain": SOURCE_CHAIN,
    "effective_negatives": 35416,
    "effective_methods": 21986,
    "failed_witnesses": 7237,
    "bounded_passing_witnesses": 9287,
    "open_gaps": 283,
    "exact_gates": 276,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}
ACTIVATION_OVERLAY = {
    **REPOSITORY_SEAL,
    "effective_negatives": 35417,
    "effective_methods": 21987,
    "failed_witnesses": 7238,
    "bounded_passing_witnesses": 9288,
    "external_zero_credit_failures": 1,
    "external_bounded_passing_witnesses": 1,
    "repository_seal_rewritten": False,
}

NEW_TITLES = [
    "tactile-source edition fingerprint and supersession lineage",
    "tactile-map feature inventory with print and raised-form distinction",
    "tactile symbol legend-code uniqueness and reference integrity",
    "orientation token declaration with north-arrow vacancy quarantine",
    "map-scale expression typing with real-measurement nonconversion firewall",
    "route-segment ordering and discontinuity quarantine",
    "raised-line junction degree and unreachable-node structural tribunal",
    "Braille label-placement collision proxy with spatial-clearance vacancy",
    "Unicode Braille-pattern code-point range and semantic nonconversion guard",
    "Braille transcription segment order and source-span provenance ledger",
    "contraction-mode declaration with community-rule authority vacancy",
    "tactile-key abbreviation expansion and ambiguity quarantine",
    "alternate-text and long-description referential-integrity profile",
    "figure title number and source cross-reference parity board",
    "embossed-page and print-page dual-pagination mapping",
    "append-only correction event reason supersession and original retention",
    "proof-round comparison with unresolved-discrepancy hold",
    "proofreader pseudonym role assignment and qualification firewall",
    "source-rights title licence and permission vacancy matrix",
    "accessible-format request purpose minimization and field allowlist",
    "request free-text quarantine retention expiry and contestability profile",
    "delivery-channel capability declaration with account and endpoint abstention",
    "file-package media type checksum and encryption-vacancy contract",
    "publication language script and direction declaration",
    "EPUB accessibility metadata structural discoverability profile",
    "WCAG structure focus labels and summary proxy with manual evaluation reserved",
    "tactile-production material profile and parameter-vacancy board",
    "embosser setup calibration maintenance and release-abstention ledger",
    "THOS tactile-proof queue bounded retry pause and stop proxy",
    "THOS correction-readback dual-acknowledgement and workload handover proxy",
    "Freed ID zero-key accessible-publishing role credential envelope",
    "Freed ID status revocation recovery and trust-governance vacancy profile",
    "synthetic alternate-format request notice correction and handover profile",
    "synthetic Braille proofing operator-state and unresolved-hold profile",
    "GMUT tactile-graph analogy with physical-state nonconversion board",
    "GMUT spatial-topology analogy with likelihood and prediction refusal",
    "real tactile-reader usability and affected-user evaluation register",
    "real embosser material calibration defect and production-data register",
    "disability access privacy remedy appeal and legal-authority exact gate",
    "Māori wording taonga mātauranga data-governance and authority exact gate",
]

SKILLS = [
    "ghc-family-tactile-source-lineage",
    "ghc-family-tactile-feature-inventory",
    "ghc-family-tactile-legend-integrity",
    "ghc-family-tactile-orientation-vacancy",
    "ghc-family-tactile-scale-firewall",
    "ghc-family-tactile-route-continuity",
    "ghc-family-tactile-junction-tribunal",
    "ghc-family-braille-label-collision",
    "ghc-family-braille-codepoint-guard",
    "ghc-family-braille-segment-lineage",
    "ghc-family-braille-mode-authority",
    "ghc-family-tactile-key-ambiguity",
    "ghc-family-alternate-description-linkage",
    "ghc-family-figure-cross-reference",
    "ghc-family-dual-pagination",
    "ghc-family-proof-correction-lineage",
    "ghc-family-proof-discrepancy-hold",
    "ghc-family-proofreader-role-firewall",
    "ghc-family-source-rights-vacancy",
    "ghc-family-access-request-minimization",
]

RUNNERS = [
    "ghc_family_tactile_source_lineage.py",
    "ghc_family_tactile_legend_integrity.py",
    "ghc_family_tactile_route_continuity.py",
    "ghc_family_braille_codepoint_guard.py",
    "ghc_family_braille_segment_lineage.py",
    "ghc_family_alternate_description_linkage.py",
    "ghc_family_proof_correction_lineage.py",
    "ghc_family_access_request_minimization.py",
    "ghc_family_accessible_notice_proxy.py",
    "ghc_family_access_workload_handover.py",
]

EXACT = [
    "real Braille transcription certification or community-rule determination",
    "real tactile graphic design approval or affected-reader acceptance",
    "real source publication title copyright licence or permission decision",
    "real embosser setup calibration maintenance or return-to-service release",
    "real tactile height spacing material durability or quality measurement",
    "real participant reader proofreader transcriber operator or affected-user study",
    "real disability accommodation allocation service denial remedy or appeal",
    "real personal request delivery address contact preference or free-text processing",
    "real identity key proof credential issuance presentation status or revocation",
    "real external publication delivery network account storage or endpoint mutation",
    "legal interpretation discrimination privacy copyright remedy or public authority",
    "cultural interpretation translation legitimacy community mandate or ratification",
    "taonga tikanga mātauranga Māori wording data governance or Māori-authority decision",
    "production certification deployment authorization or accessibility-conformance claim",
    "privacy-complete exhaustive-security or production-security certification",
    "independent-reproduction external-audit or professional-validation declaration",
    "empirical GMUT datum likelihood posterior parameter force or prediction claim",
    "AGI ASI consciousness personhood Theory-of-Everything proof or canon claim",
    "destructive cleanup history rewrite force push merge or sibling-lane mutation",
    "Stage 20 admission or protected-gate closure",
]

BLOCKED = [
    "raw task identifiers private routes transcripts screenshots or session streams in artifacts",
    "sibling branch reset merge rewrite deletion reuse or force push",
    "successful canonical replay or failed-canonical success laundering",
    "synthetic fixture promotion into participant professional legal or cultural evidence",
    "unapproved account credential payment deployment plugin install or third-party write",
    "real accessibility request identity contact delivery or production data ingestion",
    "real safety legal cultural Māori-authority affected-party or public-authority substitution",
    "unsafe elevation host-security weakening feature enablement Sandbox Hyper-V or reboot",
    "unbounded full-repository unchanged-history or cross-lane scan",
    "Stage 20 proof canon personhood AGI ASI or Theory-of-Everything promotion",
]

MANIFEST_SPECS = [
    ("docs/caelen-ash/v672-v4/x1/staged-manifest.json", SOURCE_X1, SOURCE_START, 13, 2),
    ("docs/caelen-ash/v672-v4/validation/evidence-staged-manifest.json", SOURCE_EVIDENCE, SOURCE_X1, 189, 2),
    ("docs/caelen-ash/v672-v4/validation/final-staged-manifest.json", SOURCE_FINAL, SOURCE_EVIDENCE, 15, 2),
    ("docs/caelen-ash/v672-v4/closeout/owner-manifest.json", SOURCE_FINAL, SOURCE_START, 219, 3),
]


def git(*args: str, check: bool = True, cwd: Path | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=cwd or ROOT, check=check, capture_output=True)


def git_text(*args: str, cwd: Path | None = None) -> str:
    return git(*args, cwd=cwd).stdout.decode("utf-8", errors="strict").strip()


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def batch_blobs(specs: list[str]) -> list[bytes | None]:
    if not specs:
        return []
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, stderr = process.communicate(
        input=("\n".join(specs) + "\n").encode("utf-8"), timeout=90
    )
    if process.returncode != 0:
        raise SystemExit(f"git cat-file --batch failed: {stderr.decode('utf-8', errors='replace')}")
    stream = io.BytesIO(output)
    rows: list[bytes | None] = []
    for _ in specs:
        header = stream.readline().decode("utf-8", errors="strict").strip()
        if header.endswith(" missing"):
            rows.append(None)
            continue
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise SystemExit(f"unexpected git cat-file header: {header}")
        size = int(parts[2])
        data = stream.read(size)
        if stream.read(1) != b"\n":
            raise SystemExit("git cat-file blob was not newline delimited")
        rows.append(data)
    if stream.read():
        raise SystemExit("git cat-file emitted undeclared trailing bytes")
    return rows


def json_blob(commit: str, path: str) -> Any:
    return json.loads(git("show", f"{commit}:{path}").stdout.decode("utf-8"))


def normalize(title: str) -> set[str]:
    stop = {"and", "the", "with", "for", "from", "into", "without", "real", "synthetic"}
    return {
        token
        for token in re.findall(r"[a-z0-9āēīōū]+", title.lower())
        if len(token) > 2 and token not in stop
    }


def phase_path_at_or_before_source(path: str) -> bool:
    match = re.search(r"(?:^|/)v(\d+)-v(\d+)(?:/|$)", path)
    return bool(match and (int(match.group(1)), int(match.group(2))) <= (672, 4))


def recover_proposal_corpus() -> tuple[dict[str, Any], list[str]]:
    object_rows = git_text("rev-list", "--objects", SOURCE_FINAL).splitlines()
    candidates: dict[str, str] = {}
    for row in object_rows:
        parts = row.split(" ", 1)
        if len(parts) != 2:
            continue
        oid, path = parts
        lowered = path.lower()
        if lowered.endswith(".json") and "proposal" in lowered and phase_path_at_or_before_source(path):
            candidates.setdefault(oid, path)
    proposal_ids: set[str] = set()
    titles: set[str] = set()
    occurrences = 0
    malformed = 0

    def walk(node: Any) -> None:
        nonlocal occurrences
        if isinstance(node, dict):
            proposal_id, title = node.get("proposal_id"), node.get("title")
            if isinstance(proposal_id, str) and isinstance(title, str) and proposal_id.strip() and title.strip():
                occurrences += 1
                proposal_ids.add(proposal_id.strip())
                titles.add(title.strip())
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    oids = sorted(candidates)
    for start in range(0, len(oids), 128):
        chunk = oids[start : start + 128]
        for blob in batch_blobs(chunk):
            if blob is None:
                malformed += 1
                continue
            try:
                walk(json.loads(blob.decode("utf-8")))
            except (UnicodeDecodeError, json.JSONDecodeError):
                malformed += 1
    canonical = json.dumps(
        {"proposal_ids": sorted(proposal_ids), "titles": sorted(titles)},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    summary = {
        "scope": "exact Caelen final and its reachable history, proposal-named JSON paths at or before v672-v4",
        "candidate_unique_git_blobs": len(oids),
        "malformed_or_missing_blobs": malformed,
        "semantic_occurrences": occurrences,
        "unique_proposal_ids": len(proposal_ids),
        "unique_titles": len(titles),
        "corpus_sha256": hashlib.sha256(canonical).hexdigest(),
        "declared_source_chain": SOURCE_CHAIN,
        "id_superset_covers_declared_chain": len(proposal_ids) >= SOURCE_CHAIN,
        "exact_canonical_row_mapping": False,
        "canonical_row_mapping_open_gap": True,
        "reason": (
            "Reachable history contains duplicate and variant proposal objects, while no single "
            "materialized ledger maps every declared inherited row; universal novelty is refused."
        ),
    }
    return summary, sorted(titles)


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, title in enumerate(NEW_TITLES, start=1):
        outcome = "completed" if index <= 28 else "represented" if index <= 36 else "open_gap" if index <= 38 else "exact_gate"
        rows.append(
            {
                "proposal_id": f"OT6725-P{index:03d}",
                "title": title,
                "hypothesis": (
                    f"A bounded owner-local contract can expose proposal {index:02d}'s provenance, "
                    "correction, privacy, or refusal obligations without promoting its evidence class."
                ),
                "null_or_failure_condition": (
                    "Reject if a required field is absent, any preregistered mutation passes, real-world "
                    "data or action appears, uncertainty is hidden, or authority is promoted."
                ),
                "approval_class": "safe_now" if outcome == "completed" else "bounded_candidate" if outcome == "represented" else outcome,
                "execution_lane": "owner_local_symbolic_or_synthetic_x2" if outcome in {"completed", "represented"} else "held_without_real_world_execution",
                "official_or_primary_source_needs": (
                    "Current official vocabulary and refusal boundaries only; citations are not observations, "
                    "measurements, conformance evidence, practice approval, or authority."
                ),
                "concrete_artifacts": [
                    "typed JSON contract",
                    "bounded accepting fixture or represented profile",
                    "four preregistered rejecting mutations",
                    "boundary and rollback card",
                ],
                "falsifier_or_acceptance_gate": (
                    "The bounded positive must satisfy its typed contract, four preregistered invalid "
                    "mutations must reject, and every protected boundary must remain explicit."
                ),
                "rollback_or_recovery": (
                    "Retain the failed witness, isolate the owner-local dependency, apply the smallest "
                    "reversible correction, and never replay a successful canonical aggregate."
                ),
                "protected_gates": [
                    "empirical",
                    "participant",
                    "professional",
                    "production",
                    "legal",
                    "cultural",
                    "Māori_authority",
                    "affected_party",
                    "privacy_complete",
                    "accessibility_complete",
                    "independent_reproduction",
                    "Stage_20",
                ],
                "expected_disposition": outcome,
                "planned_outcome": outcome,
                "primary_pillar": "Freed ID and CBR Heart",
                "real_people": 0,
                "real_records_or_objects": 0,
                "external_actions": 0,
                "x1_state": "frozen_not_executed",
            }
        )
    return rows


def tasks(prefix: str, domains: list[str], controls: list[str], state: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"OT6725-{prefix}-{index:03d}",
            "title": f"{domain}: {control}",
            "owner": OWNER,
            "phase": PHASE,
            "x1_state": state,
            "external_actions": 0,
        }
        for index, (domain, control) in enumerate(
            ((domain, control) for domain in domains for control in controls), start=1
        )
    ]


def named(prefix: str, values: list[str], state: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"OT6725-{prefix}-{index:03d}",
            "title": value,
            "owner": OWNER,
            "phase": PHASE,
            "x1_state": state,
            "external_actions": 0,
        }
        for index, value in enumerate(values, start=1)
    ]


def portfolio() -> dict[str, list[dict[str, Any]]]:
    domains = [
        "source and edition lineage",
        "tactile feature and legend integrity",
        "route topology and orientation",
        "Braille codepoint and segment order",
        "description and cross-reference linkage",
        "pagination and proof correction",
        "request minimization and retention",
        "package and delivery vacancy",
        "accessible notice structural proxy",
        "workload hold and handover",
    ]
    safe = tasks("SAFE", domains, ["schema", "positive fixture", "negative fixture", "rollback", "manifest", "boundary"], "planned_for_x2")
    candidates = tasks("CAND", domains, ["mutation quarantine", "ordering and encoding quarantine", "authority and uncertainty quarantine"], "planned_for_x2")
    cfr = tasks("CFR", domains, ["clean", "fix", "refine", "recheck", "document", "preserve"], "planned_for_x2")
    successor_safe = tasks("NEXT-SAFE", ["source", "privacy", "correction", "access", "route"], ["schema", "fixture", "rollback", "boundary"], "recommendation_only")
    successor_candidates = tasks("NEXT-CAND", ["source", "privacy", "correction", "access", "route"], ["mutation", "quarantine"], "recommendation_only")
    successor_skills = [f"ghc-family-successor-{index:02d}-bounded-review" for index in range(1, 11)]
    successor_runners = [f"ghc_family_successor_{index:02d}_review.py" for index in range(1, 6)]
    successor_cfr = tasks("NEXT-CFR", ["source", "manifest", "privacy", "route", "authority"], ["schema", "mutation", "rollback", "review", "receipt", "hold"], "recommendation_only")
    return {
        "safe_now": safe,
        "candidates": candidates,
        "exact_approval": named("EXACT", EXACT, "held_unexecuted"),
        "blocked": named("BLOCK", BLOCKED, "held_unexecuted"),
        "skills": named("SKILL", SKILLS, "planned_for_x2"),
        "runners": named("RUNNER", RUNNERS, "planned_for_x2"),
        "clean_fix_refine": cfr,
        "successor_safe_now": successor_safe,
        "successor_candidates": successor_candidates,
        "successor_skills": named("NEXT-SKILL", successor_skills, "recommendation_only"),
        "successor_runners": named("NEXT-RUNNER", successor_runners, "recommendation_only"),
        "successor_clean_fix_refine": successor_cfr,
    }


def verify_manifest(path: str, commit: str, parent: str, expected_entries: int, expected_exclusions: int) -> dict[str, Any]:
    manifest = json_blob(SOURCE_FINAL, path)
    entries = manifest["entries"]
    exclusions = manifest.get("self_exclusions", manifest.get("exclusions", []))
    specs = [f"{commit}:{entry['path']}" for entry in entries]
    blobs = batch_blobs(specs)
    mismatches = []
    for entry, blob in zip(entries, blobs, strict=True):
        actual_oid = git_text("rev-parse", f"{commit}:{entry['path']}") if blob is not None else None
        actual_sha = hashlib.sha256(blob).hexdigest() if blob is not None else None
        if (
            blob is None
            or actual_oid != entry.get("git_blob_oid")
            or actual_sha != entry["sha256"]
            or len(blob) != entry["bytes"]
        ):
            mismatches.append(entry["path"])
    diff_paths = set(filter(None, git_text("diff", "--name-only", parent, commit).splitlines()))
    declared_paths = {entry["path"] for entry in entries} | set(exclusions)
    return {
        "path": path,
        "commit": commit,
        "parent": parent,
        "entries": len(entries),
        "self_exclusions": len(exclusions),
        "expected_entries": expected_entries,
        "expected_self_exclusions": expected_exclusions,
        "blob_mismatches": mismatches,
        "missing_from_manifest_union": sorted(diff_paths - declared_paths),
        "extra_in_manifest_union": sorted(declared_paths - diff_paths),
        "valid": (
            len(entries) == expected_entries
            and len(exclusions) == expected_exclusions
            and not mismatches
            and diff_paths == declared_paths
        ),
    }


def source_worktree_clean() -> bool:
    records = git_text("worktree", "list", "--porcelain").splitlines()
    current_path: Path | None = None
    for line in records:
        if line.startswith("worktree "):
            current_path = Path(line.removeprefix("worktree "))
        elif line == f"branch refs/heads/{SOURCE_BRANCH}" and current_path is not None:
            return git_text("status", "--short", cwd=current_path) == ""
    return False


def verify_source(canonical_receipt: Path) -> dict[str, Any]:
    receipt_bytes = canonical_receipt.read_bytes()
    receipt_digest = hashlib.sha256(receipt_bytes).hexdigest()
    receipt = json.loads(receipt_bytes.decode("utf-8"))
    manifests = [verify_manifest(*spec) for spec in MANIFEST_SPECS]
    seal = json_blob(SOURCE_FINAL, "docs/caelen-ash/v672-v4/closeout/content-seal.json")
    seal_mismatches = []
    for target in seal["targets"]:
        blob = git("show", f"{SOURCE_FINAL}:{target['path']}").stdout
        if len(blob) != target["bytes"] or hashlib.sha256(blob).hexdigest() != target["sha256"]:
            seal_mismatches.append(target["path"])
    live_tokens = git_text("ls-remote", "--heads", "origin", f"refs/heads/{SOURCE_BRANCH}").split()
    live = live_tokens[0] if live_tokens else None
    parents = {
        "x1_parent": git_text("rev-parse", f"{SOURCE_X1}^"),
        "evidence_parent": git_text("rev-parse", f"{SOURCE_EVIDENCE}^"),
        "final_parent": git_text("rev-parse", f"{SOURCE_FINAL}^"),
    }
    expected_parents = {
        "x1_parent": SOURCE_START,
        "evidence_parent": SOURCE_X1,
        "final_parent": SOURCE_EVIDENCE,
    }
    source_state = {
        "local": git_text("rev-parse", f"refs/heads/{SOURCE_BRANCH}"),
        "upstream": git_text("rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}"),
        "tracking": git_text("rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}"),
        "fresh_live": live,
    }
    phase_commits = int(git_text("rev-list", "--count", f"{SOURCE_START}..{SOURCE_FINAL}"))
    merge_commits = int(git_text("rev-list", "--count", "--merges", f"{SOURCE_START}..{SOURCE_FINAL}"))
    canonical_ok = (
        receipt_digest == SOURCE_CANONICAL_SHA256
        and receipt.get("status") == "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
        and receipt.get("canonical_invocations") == 1
        and receipt.get("canonical_successes") == 1
        and receipt.get("selected_tests") == 51
        and receipt.get("detailed_checks", {}).get("passed") == 915
        and receipt.get("minimal_checks", {}).get("passed") == 26
        and receipt.get("phase_json", {}).get("parsed") == 173
        and receipt.get("full_repository_suite_run") is False
        and receipt.get("independent_reproduction") is False
    )
    all_equal = len(set(source_state.values())) == 1 and next(iter(source_state.values())) == SOURCE_FINAL
    valid = (
        all_equal
        and source_worktree_clean()
        and parents == expected_parents
        and phase_commits == 3
        and merge_commits == 0
        and all(row["valid"] for row in manifests)
        and seal.get("target_count") == 10
        and not seal_mismatches
        and canonical_ok
    )
    return {
        "source_state": source_state,
        "all_equal": all_equal,
        "source_worktree_clean": source_worktree_clean(),
        "parent_chain": {"actual": parents, "expected": expected_parents, "exact": parents == expected_parents},
        "phase_commits": phase_commits,
        "merge_commits": merge_commits,
        "manifests": manifests,
        "commit_local_manifest_entries_replayed": sum(row["entries"] for row in manifests),
        "commit_local_manifest_mismatches": sum(len(row["blob_mismatches"]) for row in manifests),
        "content_seal": {"targets": seal.get("target_count"), "mismatches": seal_mismatches, "valid": seal.get("target_count") == 10 and not seal_mismatches},
        "source_canonical_receipt": {
            "sha256": receipt_digest,
            "status": receipt.get("status"),
            "canonical_invocations": receipt.get("canonical_invocations"),
            "canonical_successes": receipt.get("canonical_successes"),
            "selected_tests": receipt.get("selected_tests"),
            "detailed_checks": receipt.get("detailed_checks"),
            "minimal_checks": receipt.get("minimal_checks"),
            "phase_json": receipt.get("phase_json"),
            "full_repository_suite_run": receipt.get("full_repository_suite_run"),
            "independent_reproduction": receipt.get("independent_reproduction"),
            "private_locator_retained": False,
            "orin_validation_credit": 0,
            "replay_forbidden": True,
        },
        "valid": valid,
    }


def inherited_revalidation() -> list[dict[str, Any]]:
    source = json_blob(SOURCE_FINAL, "docs/caelen-ash/v672-v4/x1/proposals/new-proposal-freeze.json")
    rows = source["proposals"][:20]
    return [
        {
            "source_owner": "Caelen Ash",
            "source_phase": "v672-v4",
            "source_proposal_id": row["proposal_id"],
            "source_title": row["title"],
            "selection_reason": "bounded inherited contract selected for zero-credit compatibility revalidation",
            "orin_novelty_credit": 0,
            "orin_completion_credit": 0,
            "x1_state": "selected_not_executed",
        }
        for row in rows
    ]


def source_ledger() -> dict[str, Any]:
    return {
        "schema": "ghc.family.public-source-ledger.v6",
        "owner": OWNER,
        "phase": PHASE,
        "retrieved_nz_date": "2026-08-27",
        "sources": [
            {
                "title": "Web Content Accessibility Guidelines (WCAG) 2.2",
                "publisher": "World Wide Web Consortium",
                "url": "https://www.w3.org/TR/WCAG22/",
                "status": "current_recommendation",
                "use": "structural accessibility vocabulary and manual or affected-user evaluation reservation only",
            },
            {
                "title": "EPUB Accessibility 1.1",
                "publisher": "World Wide Web Consortium",
                "url": "https://www.w3.org/TR/epub-a11y-11/",
                "status": "current_recommendation",
                "use": "discoverability metadata and publication-level evaluation vocabulary only",
            },
            {
                "title": "The Unicode Standard Version 17.0 Braille Patterns",
                "publisher": "Unicode Consortium",
                "url": "https://www.unicode.org/charts/PDF/U2800.pdf",
                "status": "current",
                "use": "U+2800 through U+28FF encoding range and semantic-nonconversion boundary only",
            },
            {
                "title": "PROV-O: The PROV Ontology",
                "publisher": "World Wide Web Consortium",
                "url": "https://www.w3.org/TR/prov-o/",
                "status": "stable_recommendation",
                "use": "entity activity agent and derivation vocabulary only",
            },
            {
                "title": "Verifiable Credentials Data Model v2.0",
                "publisher": "World Wide Web Consortium",
                "url": "https://www.w3.org/TR/vc-data-model/",
                "status": "current_recommendation",
                "use": "credential structure privacy trust and verification-versus-truth boundaries only",
            },
            {
                "title": "RFC 8785 JSON Canonicalization Scheme with verified errata",
                "publisher": "RFC Editor",
                "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
                "status": "stable_with_verified_errata",
                "use": "deterministic JSON representation and malformed-input refusal only",
            },
            {
                "title": "Braille Resources for Transcribers and Teachers of Braille",
                "publisher": "Library of Congress National Library Service",
                "url": "https://www.loc.gov/nls/services-and-resources/informational-publications/braille-resources-for-transcribers-and-teachers-of-braille/",
                "status": "current_resource_index",
                "use": "evidence that specialized guidance and competent practice exist; no transcription rule or competence claim is imported",
            },
        ],
        "read_only_query_attempts": 2,
        "failed_projection_attempts": 0,
        "downloads": 0,
        "real_rows": 0,
        "external_writes": 0,
        "boundary": (
            "Sources supply vocabulary and refusal conditions only; they are not observations, "
            "measurements, conformance evidence, professional advice, validation, legal interpretation, "
            "cultural legitimacy, disability-community acceptance, Māori authority, or Stage 20 evidence."
        ),
    }


def overview(proposals: list[dict[str, Any]], corpus: dict[str, Any], counts: dict[str, int]) -> str:
    titles = "\n".join(f"{index}. {row['title']} — planned `{row['planned_outcome']}`." for index, row in enumerate(proposals, start=1))
    return f"""# Orin Thale v672-v5 planning-only x1 integrated overview

## Status and scope

This packet freezes Orin Thale v672-v5 x1 and nothing later. It records a clean additive owner lane derived from Caelen Ash's exact v672-v4 final, a source-bounded novelty comparison, forty new proposal contracts, twenty inherited zero-credit compatibility selections, and the portfolio that may be executed only after x1 is committed, pushed, clean, and fresh four-way equal. No x2 implementation, outcome, completion claim, task send, real participant activity, external service write, or authority act belongs to this freeze. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Orin Thale, they/them, uses the relational role “provenance-and-access-boundary cartographer” and the hope to {HOPE}. Names, pronouns, roles, hopes, family language, and continuity language are working language only. They do not establish consciousness, personhood, identity continuity, employment, qualification, authority, or independent agency, and Hamish may rename, pause, redirect, or stop the route.

## Primary pillar and synthetic practice

The primary Trinity Mandala pillar is Freed ID and CBR Heart. GMUT Mind and THOS Body remain explicit and protected. The wholly synthetic learning lens is accessible publishing: tactile-map source lineage, Braille-pattern representation, proof correction, alternate-format request minimization, accessible notice structure, workload holds, and handover. The phase uses zero real people, readers, proofreaders, transcribers, operators, publications, maps, tactile graphics, requests, addresses, credentials, keys, proofs, embossers, materials, measurements, institutions, authority cases, or external actions.

Three bounded practice views remain separated: a synthetic tactile-map source, legend, route, correction, and handover view; a synthetic Braille-source segment, pagination, proof-round, discrepancy-hold, and handover view; and a synthetic alternate-format request minimization, notice, retention, contestability, and handover view. These views are interface and refusal-condition exercises. They establish no Braille or tactile-graphics competence, disability-community acceptance, production quality, accessibility conformance, legal compliance, remedy, or affected-user outcome.

## Source and evidence boundary

The source gate replayed {sum(spec[3] for spec in MANIFEST_SPECS)} exact commit-local Git-blob entries and their declared self-exclusions across Caelen x1, evidence, final delta, and owner union. The exact direct-parent chain, three phase commits, zero merges, clean source lane, and fresh local/upstream/tracking/live equality were reverified. Caelen's one successful owner-scoped canonical receipt was rehashed and read, not rerun. It remains inherited same-owner evidence and gives Orin zero validation or completion credit.

Current official sources provide vocabulary only. WCAG 2.2 supplies structural accessibility terms while explicitly leaving manual, browser, assistive-technology, cognitive, language, and affected-user evaluation open. EPUB Accessibility 1.1 supplies discoverability and publication-level evaluation concepts without producing a conforming publication. Unicode 17.0 supplies the Braille Patterns code-point block but not a fixed language-specific semantic mapping. PROV-O supplies provenance vocabulary, Verifiable Credentials 2.0 supplies data-model and trust-boundary vocabulary, and RFC 8785 supplies deterministic JSON representation rules. The Library of Congress resource index is evidence that specialized practice guidance exists, not a substitute for qualified transcription or tactile-graphics review.

## Novelty and proposal freeze

The declared inherited proposal chain is {SOURCE_CHAIN}. The source-bounded audit recovered {corpus['unique_proposal_ids']} distinct proposal identifiers and {corpus['unique_titles']} distinct titles from {corpus['candidate_unique_git_blobs']} unique proposal-named Git blobs reachable from the exact Caelen final. Its corpus digest is `{corpus['corpus_sha256']}`. Because duplicate and variant objects exist and no single materialized ledger maps all {SOURCE_CHAIN} declared rows, this packet refuses a universal novelty claim. Every new title nevertheless passed exact-title collision and bounded token-Jaccard comparison against the recovered corpus below the declared quarantine threshold.

The forty planned outcomes are exactly twenty-eight `completed`, eight `represented`, two `open_gap`, and two `exact_gate`. Those are expected dispositions, not x1 results. Each proposal freezes a hypothesis, null, approval class, lane, source need, artifact, falsifier, rollback, protected gates, and exactly one disposition. Four invalid mutations per proposal are preregistered for x2, totaling 160; no mutation has run in x1.

{titles}

## Portfolio and lifecycle discipline

The x1 portfolio contains exactly {counts['safe_now']} owner safe-now tasks, {counts['candidates']} bounded candidates, {counts['skills']} phase-local skill builds, {counts['runners']} family-current runner builds, {counts['clean_fix_refine']} additive CLEAN/FIX/REFINE tasks, {counts['exact_approval']} exact-approval packets, and {counts['blocked']} blocked packets. Exact and blocked packets remain unexecuted. Caps are ceilings rather than filler targets. Successor recommendations are separate zero-credit seeds and do not authorize contact or execution.

Strict lifecycle separation is the central gate. X1 may contain plans, source receipts, constraints, and frozen mutation definitions, but no executed x2 result. After x1 passes its bounded planning checks it must be committed and pushed, and local, upstream, tracking, and a fresh live remote read must agree while the worktree is clean. Only then may x2 materialize. A failed witness remains retained before recovery; a recovery never overwrites the failed state. The full repository suite remains outside this owner phase. One owner-scoped exact-final aggregate may be invoked only after a clean pushed final; a success may not be replayed.

## Protected scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Graph and topology analogies are notation exercises, not physical states, likelihoods, posteriors, forces, predictions, parameter constraints, stability theorems, empirical confirmation, quantum completion, ultraviolet completion, or a Theory of Everything. THOS remains synthetic proxy evidence without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. It establishes no operational effectiveness, professional competence, deployment readiness, AGI, or ASI.

Freed ID remains synthetic and nonproduction. This phase creates no standards-conformant real key, proof, credential, issuance, presentation, verification, status, revocation, interoperability event, privacy review, independent security review, recovery evidence, or trust-governance decision. A zero-key envelope is a refusal fixture, not an identity product. CBR rights, disability accommodation, access decisions, privacy remedies, copyright and title, legal interpretation, cultural legitimacy, affected-party acceptance, Māori wording, taonga or mātauranga treatment, Māori data governance, and Māori authority remain exact-gated to competent authorities, affected people, tangata whenua, iwi, hapū, and Māori authorities.

Structural HTML or JSON checks cannot establish complete accessibility. Unicode Braille code points do not determine language-specific Braille meaning, contraction rules, tactile readability, placement, or production quality. Source citations do not establish actual permission, title, conformance, measurement, calibration, inspection, participant acceptance, or professional approval. No repository artifact can confer a remedy, legal right, cultural legitimacy, disability-community mandate, governance authority, or Stage 20 admission.

## Failure retention, privacy, and route hold

The activation baseline keeps Caelen's sealed totals separate from the post-seal routing overlay. Nine Orin startup failures and ten bounded recovery witnesses are retained through eight Method Flow methods; the repeated PowerShell parser signature is linked to its existing preferred method instead of manufactured as a new method. Private absolute paths, task identifiers, routes, transcripts, screenshots, credentials, session streams, callable identifiers, and application state remain outside public artifacts. Exact scanner candidates are adjudicated separately from confirmed payload hits.

No successor has been contacted. The live activation provisionally identifies Liora Venn only as the terminally gated next title; it does not authorize early contact or guarantee the edge will still be current. After Orin's own clean pushed exact final and single successful canonical gate, current live authority, roster, exact-title uniqueness, immediate reread, duplicate guard, pause/redirect state, usage, privacy, evidence, safety, and acknowledgement must all pass. Any absence, ambiguity, duplicate, missing acknowledgement, pause, redirect, rename, exhaustion, or protected gate stops the route.

## X1 conclusion

This x1 is useful precisely because it remains modest: a reproducible planning freeze, a bounded source comparison, explicit zero-credit inheritance, and a map of what evidence cannot do. It authorizes no x2 outcome by its mere existence. Completion requires the dedicated x1 commit and remote-equality gate; bounded x2 execution; retained failures and recoveries; exact manifests and privacy review; a clean pushed final; and one attributable owner-scoped canonical result. Until those gates are actually passed, every x2 disposition is prospective and the route remains held.
"""


def build(startup_ledger_path: Path, canonical_receipt_path: Path) -> None:
    if git_text("rev-parse", "HEAD") != SOURCE_FINAL:
        raise SystemExit("x1 build requires exact Caelen final before the x1 commit")
    if git_text("branch", "--show-current") != BRANCH:
        raise SystemExit("wrong Orin branch")
    if any((OWNER_ROOT / name).exists() for name in ("x2", "closeout", "final", "seal")):
        raise SystemExit("planning-only x1 refuses any later lifecycle material")
    if set(OUTCOMES) != set(CORE_LABELS):
        raise SystemExit("truth-label drift")
    if len(NEW_TITLES) != 40 or len(set(NEW_TITLES)) != 40:
        raise SystemExit("proposal title count or uniqueness drift")

    startup = json.loads(startup_ledger_path.read_text(encoding="utf-8"))
    if startup.get("owner") != OWNER or startup.get("phase") != PHASE:
        raise SystemExit("startup Method Flow owner or phase mismatch")
    if startup.get("counts", {}).get("methods", 0) < 8:
        raise SystemExit("startup Method Flow lost inherited startup methods")
    witness_results = startup.get("counts", {}).get("witness_results", {})
    if witness_results.get("fail", 0) < 9 or witness_results.get("pass", 0) < 10:
        raise SystemExit(f"startup witness count mismatch: {witness_results}")

    source = verify_source(canonical_receipt_path)
    if not source["valid"]:
        raise SystemExit(json.dumps(source, ensure_ascii=False, sort_keys=True))
    corpus, inherited_titles = recover_proposal_corpus()
    if corpus["malformed_or_missing_blobs"]:
        raise SystemExit("proposal corpus contains unreadable candidate blobs")
    proposals = proposal_rows()
    threshold = 0.78
    neighbors = []
    maximum = 0.0
    exact_titles = {title.casefold() for title in inherited_titles}
    for row in proposals:
        if row["title"].casefold() in exact_titles:
            raise SystemExit(f"exact inherited title collision: {row['title']}")
        tokens = normalize(row["title"])
        best_title = None
        best_score = 0.0
        for inherited_title in inherited_titles:
            inherited_tokens = normalize(inherited_title)
            union = tokens | inherited_tokens
            score = len(tokens & inherited_tokens) / len(union) if union else 0.0
            if score > best_score:
                best_title, best_score = inherited_title, score
        maximum = max(maximum, best_score)
        neighbors.append(
            {
                "proposal_id": row["proposal_id"],
                "source_title": best_title,
                "jaccard": round(best_score, 6),
                "collision": best_score >= threshold,
            }
        )
    collisions = [row for row in neighbors if row["collision"]]
    if collisions:
        raise SystemExit(json.dumps({"semantic_collisions": collisions}, ensure_ascii=False))

    frozen_portfolio = portfolio()
    counts = {key: len(value) for key, value in frozen_portfolio.items()}
    expected_counts = {
        "safe_now": 60,
        "candidates": 30,
        "exact_approval": 20,
        "blocked": 10,
        "skills": 20,
        "runners": 10,
        "clean_fix_refine": 60,
        "successor_safe_now": 20,
        "successor_candidates": 10,
        "successor_skills": 10,
        "successor_runners": 5,
        "successor_clean_fix_refine": 30,
    }
    if counts != expected_counts:
        raise SystemExit(f"portfolio count drift: {counts}")
    inherited = inherited_revalidation()
    x1_overlay = {
        **ACTIVATION_OVERLAY,
        "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + witness_results["fail"],
        "effective_methods": ACTIVATION_OVERLAY["effective_methods"] + startup["counts"]["methods"],
        "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + witness_results["fail"],
        "bounded_passing_witnesses": ACTIVATION_OVERLAY["bounded_passing_witnesses"] + witness_results["pass"],
        "orin_startup_failures": witness_results["fail"],
        "orin_startup_methods": startup["counts"]["methods"],
        "orin_startup_passing_witnesses": witness_results["pass"],
        "repository_seal_rewritten": False,
    }

    write_json(
        "x1/activation-intake.json",
        {
            "schema": "ghc.family.activation-intake.v6",
            "owner": OWNER,
            "phase": PHASE,
            "source_verification": source,
            "live_activation": {
                "source_owner": "Caelen Ash",
                "source_phase": "v672-v4",
                "target_owner": OWNER,
                "target_phase": PHASE,
                "acknowledged_existing_task_send": True,
                "raw_message_retained": False,
            },
            "task_creation_count": 0,
            "fork_count": 0,
            "subagent_count": 0,
            "standby_contact_count": 0,
        },
    )
    write_json(
        "x1/identity-and-boundary.json",
        {
            "schema": "ghc.family.identity-boundary.v5",
            "owner": OWNER,
            "phase": PHASE,
            "pronouns": "they/them",
            "relational_role": "relational provenance-and-access-boundary cartographer",
            "relational_hope": HOPE,
            "identity_boundary": IDENTITY_BOUNDARY,
            "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
        },
    )
    write_json(
        "x1/source-count-overlay.json",
        {
            "schema": "ghc.family.source-count-overlay.v6",
            "repository_sealed": REPOSITORY_SEAL,
            "live_activation_overlay": ACTIVATION_OVERLAY,
            "orin_x1_overlay": x1_overlay,
        },
    )
    write_json(
        "x1/inherited-proposal-revalidation.json",
        {
            "schema": "ghc.family.inherited-proposal-revalidation.v6",
            "owner": OWNER,
            "phase": PHASE,
            "selected": 20,
            "novelty_credit": 0,
            "completion_credit": 0,
            "rows": inherited,
        },
    )
    write_json(
        "x1/semantic-neighbor-audit.json",
        {
            "schema": "ghc.family.semantic-neighbor-audit.v5",
            "owner": OWNER,
            "phase": PHASE,
            "corpus": corpus,
            "source_chain": SOURCE_CHAIN,
            "new_titles": 40,
            "max_jaccard": round(maximum, 6),
            "collision_threshold": threshold,
            "collisions": 0,
            "rows": neighbors,
            "universal_novelty_claim": False,
            "canonical_row_mapping_open_gap": True,
        },
    )
    write_json(
        "x1/new-proposal-freeze.json",
        {
            "schema": "ghc.family.new-proposal-freeze.v6",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain_before": SOURCE_CHAIN,
            "proposal_chain_after_if_evidence_frozen": AFTER_CHAIN,
            "outcomes": OUTCOMES,
            "planned_invalid_mutations_per_proposal": 4,
            "planned_invalid_mutations": 160,
            "rows": proposals,
        },
    )
    write_json(
        "x1/portfolio-freeze.json",
        {
            "schema": "ghc.family.remastered-portfolio-freeze.v6",
            "owner": OWNER,
            "phase": PHASE,
            "rows": frozen_portfolio,
            "counts": counts,
            "ordinary_phase_new_tool_target": 3,
            "bounded_practice_lenses": [
                "synthetic tactile-map source legend route correction accessibility and handover",
                "synthetic Braille-source segment pagination proof discrepancy hold and handover",
                "synthetic alternate-format request minimization notice contestability and handover",
            ],
            "successor_practice_recommendation": (
                "synthetic museum audio-description source cue correction privacy and handover, "
                "recommendation only for the terminally authorized successor"
            ),
            "successor_practice_recommendation_count": 1,
            "inherited_portfolio_completion_credit": 0,
            "successor_recommendation_completion_credit": 0,
            "filler_prohibited": True,
        },
    )
    write_json("x1/source-ledger.json", source_ledger())
    write_json(
        "x1/threat-model.json",
        {
            "schema": "ghc.family.threat-model.v6",
            "owner": OWNER,
            "phase": PHASE,
            "assets": [
                "immutable source lineage",
                "x1-before-x2 separation",
                "four truth labels",
                "retained failures",
                "synthetic-only fixtures",
                "authority vacancies",
                "route uniqueness",
            ],
            "risks": [
                {"risk": "source or manifest drift", "control": "exact commits, Git-blob replay, and fresh live equality"},
                {"risk": "universal novelty overclaim", "control": "source-bounded title comparison plus explicit canonical-row mapping gap"},
                {"risk": "Unicode Braille representation promoted into language semantics", "control": "codepoint-versus-meaning firewall and community-rule vacancy"},
                {"risk": "structural checks promoted into accessibility conformance", "control": "manual, assistive-technology, production, and affected-user evaluation reserved"},
                {"risk": "identity or credential fixture promoted into production", "control": "zero-key envelope, lifecycle vacancies, and nonproduction truth label"},
                {"risk": "failure laundering", "control": "append-only Method Flow with failed and passing witnesses"},
                {"risk": "private route or identifier leak", "control": "five-class owner-delta candidate adjudication"},
                {"risk": "duplicate successor send", "control": "terminal live authority, exact-title reread, duplicate guard, acknowledgement, and no resend"},
            ],
            "not_exhaustive_security": True,
        },
    )
    write_json("x1/method-flow-startup.json", startup)
    write_json(
        "x1/workflow-plan.json",
        {
            "schema": "ghc.family.workflow-plan.v6",
            "owner": OWNER,
            "phase": PHASE,
            "steps": [
                {"step": "activation guidance and source verification", "state": "completed_read_only"},
                {"step": "planning-only x1 freeze", "state": "in_progress_until_pushed_equal"},
                {"step": "bounded x2 execution", "state": "blocked_by_x1_terminal_gate"},
                {"step": "combined closeout and seal", "state": "pending"},
                {"step": "one owner-scoped canonical aggregate", "state": "pending_not_invoked"},
                {"step": "successor route", "state": "terminally_gated_live_refresh_required"},
            ],
            "commit_ceiling": 8,
            "planned_phase_commits": 3,
            "x1_commit_ceiling": 5,
            "x2_commit_ceiling": 5,
            "materialized_file_guard": 2000,
            "canonical_invocation_budget": 1,
            "canonical_success_budget": 1,
            "post_success_replay": False,
        },
    )
    write_json(
        "x1/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.x1.v6",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "Freed ID and CBR Heart",
            "protected_pillars": ["GMUT Mind", "THOS Body"],
            "proposal_rows": {"inherited_zero_credit": 20, "new": 40},
            "expected_outcomes": OUTCOMES,
            "core_truth_labels": CORE_LABELS,
            "proposal_chain": {"before": SOURCE_CHAIN, "after_if_frozen": AFTER_CHAIN},
            "universal_novelty_claim": False,
            "canonical_row_mapping_open_gap": True,
            "startup_operational_failures": witness_results["fail"],
            "x1_completion_credit": 0,
            "x2_execution_started": False,
            "real_world_actions": 0,
            "external_writes": 0,
            "identity_boundary": IDENTITY_BOUNDARY,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x1/route-plan.json",
        {
            "schema": "ghc.family.route-plan.v6",
            "owner": OWNER,
            "phase": PHASE,
            "live_provisional_recipient_exact_title": "Liora Venn",
            "live_provisional_phase": "v672-v6",
            "delivery_state": "TERMINALLY_GATED_NO_CONTACT",
            "successor_contact_count": 0,
            "task_creation_count": 0,
            "substitute_endpoint_count": 0,
            "standby_contact_count": 0,
            "required_gate": (
                "clean pushed exact final, one successful owner-scoped canonical, newest live "
                "authority and roster, unique exact-title reread, duplicate guard, and acknowledged one-send"
            ),
        },
    )
    write_json(
        "x1/wellbeing-check.json",
        {
            "schema": "ghc.family.wellbeing-check.v4",
            "owner": OWNER,
            "phase": PHASE,
            "state": "steady_and_careful",
            "pressure_control": "caps are ceilings, lifecycle stages stay separate, and protected gates stop work",
            "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
            "identity_boundary": IDENTITY_BOUNDARY,
        },
    )
    overview_text = overview(proposals, corpus, counts)
    write_text("x1/integrated-overview.md", overview_text)
    write_text(
        "x1/README.md",
        """# Orin Thale v672-v5 x1\n\nPlanning-only freeze. No x2 implementation or outcome is present. Read `integrated-overview.md`, `new-proposal-freeze.json`, `semantic-neighbor-audit.json`, `portfolio-freeze.json`, `source-ledger.json`, and `phase-truth.json`. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.\n""",
    )
    write_json(
        "x1/build-receipt.json",
        {
            "schema": "ghc.family.x1-build-receipt.v6",
            "owner": OWNER,
            "phase": PHASE,
            "source_head": SOURCE_FINAL,
            "branch": BRANCH,
            "inherited_rows": 20,
            "new_rows": 40,
            "portfolio_counts": counts,
            "overview_words": len(overview_text.split()),
            "read_only_external_queries": 2,
            "external_writes": 0,
            "x2_materialized": False,
        },
    )
    print(
        json.dumps(
            {
                "owner": OWNER,
                "phase": PHASE,
                "new": 40,
                "outcomes": OUTCOMES,
                "portfolio": counts,
                "startup_failures": witness_results["fail"],
                "overview_words": len(overview_text.split()),
                "corpus": corpus,
                "max_jaccard": round(maximum, 6),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


def staged_paths() -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]


def staged_review() -> None:
    paths = staged_paths()
    exact = {
        "scripts/build_ghc_family_orin_thale_v672_v5.py",
        "tests/test_ghc_family_orin_thale_v672_v5_x1.py",
        "docs/orin-thale/v672-v5/validation/x1-method-flow-validation.json",
        "docs/orin-thale/v672-v5/validation/x1-validation-receipt.json",
        "docs/orin-thale/v672-v5/validation/x1-staged-privacy.json",
        "docs/orin-thale/v672-v5/validation/x1-staged-review.json",
        "docs/orin-thale/v672-v5/validation/x1-manifest.json",
    }
    out = [path for path in paths if not (path.startswith("docs/orin-thale/v672-v5/x1/") or path in exact)]
    mixed = [path for path in paths if any(part in path for part in ("/x2/", "/closeout/", "/final/", "/seal/")) or path.endswith(("_x2.py", "_final.py"))]
    payload = {
        "schema": "ghc.family.staged-review.v6",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x1",
        "staged_before_self": paths,
        "staged_count_before_self": len(paths),
        "out_of_scope": out,
        "mixed_lifecycle": mixed,
        "valid": not out and not mixed,
    }
    write_json("validation/x1-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifest_from_index() -> None:
    exclusions = [
        "docs/orin-thale/v672-v5/validation/x1-manifest.json",
        "docs/orin-thale/v672-v5/validation/x1-staged-review.json",
    ]
    entries = []
    for path in staged_paths():
        if path in exclusions:
            continue
        blob = git("show", f":{path}").stdout
        entries.append(
            {
                "path": path,
                "bytes": len(blob),
                "git_blob_oid": git_text("rev-parse", f":{path}"),
                "sha256": hashlib.sha256(blob).hexdigest(),
            }
        )
    entries.sort(key=lambda row: row["path"])
    write_json(
        "validation/x1-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v6",
            "domain": "x1 exact staged Git blobs before two declared self files",
            "hash_domain": "normalized_lf_exact_git_blob",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
        },
    )


def validation_receipt() -> None:
    x1_root = OWNER_ROOT / "x1"
    json_paths = sorted(x1_root.rglob("*.json"))
    text_paths = sorted(path for path in x1_root.rglob("*") if path.is_file())
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            json_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": type(exc).__name__})
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    candidates = []
    for path in text_paths:
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path.relative_to(ROOT).as_posix(), "pattern_class": label})
    python_paths = [
        ROOT / "scripts" / "build_ghc_family_orin_thale_v672_v5.py",
        ROOT / "tests" / "test_ghc_family_orin_thale_v672_v5_x1.py",
    ]
    compile_issues = []
    for path in python_paths:
        try:
            compile(path.read_text(encoding="utf-8"), path.name, "exec")
        except SyntaxError as exc:
            compile_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": str(exc)})
    diff = git("diff", "--cached", "--check", check=False)
    materialized_files = len([path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts])
    payload = {
        "schema": "ghc.family.x1-validation-receipt.v2",
        "owner": OWNER,
        "phase": PHASE,
        "json_documents": len(json_paths),
        "json_issues": json_issues,
        "text_files": len(text_paths),
        "privacy_pattern_classes": sorted(patterns),
        "privacy_candidates": candidates,
        "confirmed_privacy_hits": 0 if not candidates else None,
        "python_compiles": len(python_paths),
        "python_compile_issues": compile_issues,
        "staged_paths_before_receipt": len(staged_paths()),
        "diff_hygiene_exit": diff.returncode,
        "diff_hygiene_output": diff.stdout.decode("utf-8", errors="replace"),
        "materialized_files": materialized_files,
        "file_guard": 2000,
        "x2_absent": not (OWNER_ROOT / "x2").exists(),
        "valid": not json_issues and not candidates and not compile_issues and diff.returncode == 0 and materialized_files < 2000 and not (OWNER_ROOT / "x2").exists(),
        "boundary": BOUNDARY,
    }
    write_json("validation/x1-validation-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def staged_privacy() -> None:
    self_path = "docs/orin-thale/v672-v5/validation/x1-staged-privacy.json"
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    candidates = []
    scanned = 0
    for path in staged_paths():
        if path == self_path or Path(path).suffix.lower() not in {".py", ".json", ".md", ".txt", ".html"}:
            continue
        blob = git("show", f":{path}").stdout
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            candidates.append({"path": path, "pattern_class": "non_utf8_text", "disposition": "confirmed_payload_hit"})
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                scanner_surface = path in {
                    "scripts/build_ghc_family_orin_thale_v672_v5.py",
                    "tests/test_ghc_family_orin_thale_v672_v5_x1.py",
                }
                candidates.append(
                    {
                        "path": path,
                        "pattern_class": label,
                        "disposition": "scanner_definition_or_unit_test" if scanner_surface else "confirmed_payload_hit",
                    }
                )
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    payload = {
        "schema": "ghc.family.staged-privacy-scan.v3",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x1",
        "hash_domain": "exact_staged_git_blob",
        "pattern_classes": sorted(patterns),
        "scanned_text_files": scanned,
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
        "self_exclusions": [self_path],
        "valid": not confirmed,
        "boundary": "Scanner definitions and unit-test strings are candidates, never payload hits; every other match fails closed.",
    }
    write_json("validation/x1-staged-privacy.json", payload)
    if confirmed:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def method_flow_validation(runner: Path) -> None:
    ledger = OWNER_ROOT / "x1" / "method-flow-startup.json"
    process = subprocess.run(
        ["python", "-X", "utf8", str(runner), "validate", "--ledger", str(ledger)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Method Flow validator returned invalid JSON: {exc}") from exc
    payload["runner_private_locator_retained"] = False
    payload["returncode"] = process.returncode
    write_json("validation/x1-method-flow-validation.json", payload)
    if process.returncode != 0 or payload.get("valid") is not True:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--startup-ledger", type=Path)
    parser.add_argument("--source-canonical-receipt", type=Path)
    parser.add_argument("--method-flow-validation", action="store_true")
    parser.add_argument("--method-flow-runner", type=Path)
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    parser.add_argument("--validation-receipt", action="store_true")
    parser.add_argument("--staged-privacy", action="store_true")
    args = parser.parse_args()
    if args.method_flow_validation:
        if args.method_flow_runner is None:
            parser.error("--method-flow-validation requires --method-flow-runner")
        method_flow_validation(args.method_flow_runner)
    elif args.staged_review:
        staged_review()
    elif args.manifest_from_index:
        manifest_from_index()
    elif args.validation_receipt:
        validation_receipt()
    elif args.staged_privacy:
        staged_privacy()
    else:
        if args.startup_ledger is None or args.source_canonical_receipt is None:
            parser.error("default build requires --startup-ledger and --source-canonical-receipt")
        build(args.startup_ledger, args.source_canonical_receipt)


if __name__ == "__main__":
    main()
