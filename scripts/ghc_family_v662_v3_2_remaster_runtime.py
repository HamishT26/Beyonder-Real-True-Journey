#!/usr/bin/env python3
"""Deterministic helpers shared by the v662-v3-2 remaster builders and validators."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable

import ghc_family_v662_v3_2_remaster_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT

PRIVACY_PATTERNS = {
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/]"),
    "credential": re.compile(r"(?:api[_-]?key|access[_-]?token|bearer|password|secret)\s*[:=]\s*[^\s,;]+", re.I),
    "private_route_identifier": re.compile(r"(?:thread[_-]?id|task[_-]?id|agent[_-]?id|resume[_-]?token|private[_-]?callable)\s*[:=]", re.I),
    "transcript_or_session": re.compile(r"(?:raw transcript|session stream|conversation export|rollout payload)", re.I),
}


def git(*args: str, check: bool = True) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if check and completed.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {completed.stderr[-2000:]}")
    return completed.stdout.strip()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def owner_paths() -> list[Path]:
    paths: set[Path] = set()
    if PHASE.exists():
        paths.update(path for path in PHASE.rglob("*") if path.is_file())
    for pattern in (
        "scripts/*v662_v3_2_remaster*.py",
        "tests/*v662_v3_2_remaster*.py",
    ):
        paths.update(path for path in ROOT.glob(pattern) if path.is_file())
    return sorted(paths, key=repo_relative)


def make_manifest(paths: Iterable[Path], *, schema: str, exclusions: Iterable[str]) -> dict[str, Any]:
    excluded = set(exclusions)
    entries = []
    for path in sorted(paths, key=repo_relative):
        rel = repo_relative(path)
        if rel in excluded:
            continue
        payload = path.read_bytes()
        entries.append({"path": rel, "bytes": len(payload), "sha256": sha256_bytes(payload)})
    return {
        "schema": schema,
        "owner": d.OWNER,
        "phase": d.PHASE,
        "entry_count": len(entries),
        "entries": entries,
        "exclusions": sorted(excluded),
        "boundary": d.EVIDENCE_BOUNDARY,
    }


def replay_working_manifest(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    mismatches = []
    for entry in manifest["entries"]:
        path = ROOT / entry["path"]
        if not path.is_file():
            mismatches.append({"path": entry["path"], "reason": "missing"})
            continue
        payload = path.read_bytes()
        if len(payload) != entry["bytes"] or sha256_bytes(payload) != entry["sha256"]:
            mismatches.append({"path": entry["path"], "reason": "bytes_or_hash"})
    return mismatches


def privacy_scan(paths: Iterable[Path], *, schema: str) -> dict[str, Any]:
    candidates = []
    confirmed = []
    for path in sorted(paths, key=repo_relative):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = repo_relative(path)
        for label, pattern in PRIVACY_PATTERNS.items():
            if not pattern.search(text):
                continue
            scanner_definition = (
                "privacy" in path.name.lower()
                or path.name.endswith("runtime.py")
                or "validator" in path.name.lower()
                or "canonical" in path.name.lower()
            )
            item = {
                "path": rel,
                "class": label,
                "adjudication": "scanner_definition" if scanner_definition else "prohibition_boundary_vocabulary",
            }
            candidates.append(item)
            if not scanner_definition and label in {"raw_uuid", "private_absolute_path", "credential", "private_route_identifier"}:
                confirmed.append(item)
    return {
        "schema": schema,
        "owner": d.OWNER,
        "phase": d.PHASE,
        "classes": list(PRIVACY_PATTERNS),
        "file_count": len(list(paths)),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "privacy_complete": False,
        "boundary": "Five-class pattern and adjudication scan only; not complete privacy assurance.",
    }


def document_cap(paths: Iterable[Path], *, cap: int = 100000) -> dict[str, Any]:
    rows = []
    over = []
    for path in sorted(paths, key=repo_relative):
        if path.suffix.lower() not in {".md", ".txt", ".json", ".py", ".yaml", ".yml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        words = len(re.findall(r"\S+", text))
        row = {"path": repo_relative(path), "words": words}
        rows.append(row)
        if words > cap:
            over.append(row)
    return {
        "schema": "ghc.family.v662-v3-2-remaster.document-cap.v1",
        "cap": cap,
        "checked": len(rows),
        "over_cap": over,
        "valid": not over,
        "rows": rows,
    }


def normalized_title(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.lower()))


def jaccard(left: str, right: str) -> float:
    a, b = normalized_title(left), normalized_title(right)
    return len(a & b) / len(a | b) if a or b else 1.0


def make_new_proposal(index: int, spec: tuple[str, str, str, str, list[str], str]) -> dict[str, Any]:
    slug, title, mechanism, pillar, sources, disposition = spec
    proposal_id = f"V6623R-P{index:03d}"
    return {
        "proposal_id": proposal_id,
        "slug": slug,
        "title": title,
        "origin": "new_unique_v662_v3_2_remaster_proposal",
        "append_to_frozen_chain": True,
        "expected_disposition": disposition,
        "approval_class": "safe_now_bounded_synthetic_or_structural",
        "execution_lane": "x2_owner_local_bounded_structural",
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable repository-lifecycle obligations "
            "without promoting software structure into empirical, professional, production, legal, "
            "cultural, Māori-authority, identity, independent-reproduction, or Stage 20 evidence."
        ),
        "null_or_failure_condition": (
            f"The artifact omits or contradicts {mechanism}, accepts a frozen mutation, erases a "
            "failure, silently omits a current test identifier, mutates a sibling lane, or crosses a "
            "protected authority or real-world gate."
        ),
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": (
            "One declared structural fixture must pass and five preregistered mutations must be "
            "rejected; no real-world, authority, independent-reproduction, or Stage 20 credit follows."
        ),
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave people, "
            "production state, sibling lanes, external systems, rights, and authority unchanged."
        ),
        "protected_gates": d.PROTECTED_GATES,
    }
