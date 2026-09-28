from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

OWNER = "Sable Rook"
PHASE = "v707-v5"
SOURCE_OWNER = "Auren Lark"
SOURCE_PHASE = "v707-v4"
SOURCE_HEAD = "aa2c563b247d978798ab9363d43b5050aca09ee8"
SOURCE_PLANNING = "d686188bbbdcb77b7609c246da59117a834f1b08"
SOURCE_X1 = "ab1df555f71c0ee8a646c2e5052d6c0fedd2fede"
SOURCE_X2 = "71d6f11b610084f6dd25386f43f1663eba23ecf2"
BRANCH = "codex/GHC-Family/sable-rook-v707-v5-full-tools"
ROOT = Path(__file__).resolve().parents[4]
PREFIX = Path("docs/sable-rook/v707-v5")
PHASE_ROOT = ROOT / PREFIX
SOURCE_ROOT = ROOT / "docs/auren-lark/v707-v4"

BOUNDARY = (
    "Finite synthetic same-owner chordal-graph software and documentation evidence only. "
    "No independent reproduction, empirical GMUT confirmation, production THOS or Freed ID, "
    "participant result, professional judgment, deployment authority, legal or cultural conclusion, "
    "affected-party or Maori authority, complete privacy, accessibility or security assurance, "
    "AGI or ASI, consciousness or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 readiness."
)

PROTECTED_GATES = [
    "empirical_evidence",
    "participant_or_operator_evidence",
    "professional_validation",
    "production_or_deployment",
    "legal_or_cultural_authority",
    "affected_party_acceptance",
    "maori_authority",
    "complete_privacy_accessibility_security",
    "independent_reproduction",
    "agi_asi_consciousness_personhood",
    "theory_of_everything_or_canon",
    "stage_20",
]

OPERATIONS = [
    ("record-shape", "Validate finite simple-undirected graph record shape", "x1", "completed"),
    ("graph-normalization", "Normalize and deduplicate undirected edge records", "x1", "completed"),
    ("adjacency-symmetry", "Check exact adjacency symmetry and loop refusal", "x1", "completed"),
    ("connected-components", "Compute deterministic connected components", "x1", "completed"),
    ("induced-subgraph", "Project an exact deterministic induced subgraph", "x1", "completed"),
    ("simplicial-vertices", "Enumerate vertices with clique neighborhoods", "x1", "completed"),
    ("maximum-cardinality-search", "Compute a deterministic maximum-cardinality ordering", "x1", "completed"),
    ("perfect-elimination-order", "Construct or refuse a perfect elimination ordering", "x1", "completed"),
    ("chordality-decision", "Decide finite chordality from exact elimination obligations", "x1", "completed"),
    ("chordless-cycle-witness", "Return a bounded induced-cycle obstruction when present", "x1", "completed"),
    ("maximal-cliques", "Enumerate exact maximal cliques", "x2", "completed"),
    ("clique-tree-candidate", "Build a deterministic maximum-intersection clique forest", "x2", "completed"),
    ("running-intersection-check", "Check the clique running-intersection obligation", "x2", "completed"),
    ("minimal-separator-profile", "Record clique-tree intersection separators", "x2", "completed"),
    ("fill-edge-triangulation", "Compute a deterministic bounded chordal completion", "x2", "completed"),
    ("edge-deletion-comparison", "Compare chordality after deterministic edge deletion", "x2", "completed"),
    ("relabel-covariance", "Check graph invariants under deterministic relabeling", "x2", "completed"),
    ("three-coordinate-model", "Represent vertex edge and maximal-clique counts", "x2", "represented"),
    ("external-graph-corpus-gap", "Reserve transfer from finite fixtures to external graph corpora", "x2", "open_gap"),
    ("deployment-authority-hold", "Hold operational use behind competent authority", "x2", "exact_gate"),
]

FIXTURES = [
    {"id": "CG01-PATH4", "nodes": ["a", "b", "c", "d"], "edges": [["a", "b"], ["b", "c"], ["c", "d"]]},
    {"id": "CG02-STAR5", "nodes": ["a", "b", "c", "d", "e"], "edges": [["a", "b"], ["a", "c"], ["a", "d"], ["a", "e"]]},
    {"id": "CG03-TRIANGLE", "nodes": ["a", "b", "c"], "edges": [["a", "b"], ["b", "c"], ["a", "c"]]},
    {"id": "CG04-CLIQUE4", "nodes": ["a", "b", "c", "d"], "edges": [["a", "b"], ["a", "c"], ["a", "d"], ["b", "c"], ["b", "d"], ["c", "d"]]},
    {"id": "CG05-CYCLE4", "nodes": ["a", "b", "c", "d"], "edges": [["a", "b"], ["b", "c"], ["c", "d"], ["a", "d"]]},
    {"id": "CG06-CYCLE5", "nodes": ["a", "b", "c", "d", "e"], "edges": [["a", "b"], ["b", "c"], ["c", "d"], ["d", "e"], ["a", "e"]]},
    {"id": "CG07-DIAMOND", "nodes": ["a", "b", "c", "d"], "edges": [["a", "b"], ["a", "c"], ["a", "d"], ["b", "c"], ["b", "d"]]},
    {"id": "CG08-BOWTIE", "nodes": ["a", "b", "c", "d", "e"], "edges": [["a", "b"], ["b", "c"], ["a", "c"], ["c", "d"], ["d", "e"], ["c", "e"]]},
    {"id": "CG09-K23", "nodes": ["a", "b", "c", "d", "e"], "edges": [["a", "c"], ["a", "d"], ["a", "e"], ["b", "c"], ["b", "d"], ["b", "e"]]},
    {"id": "CG10-THREE-SUN", "nodes": ["c1", "c2", "c3", "s1", "s2", "s3"], "edges": [["c1", "c2"], ["c2", "c3"], ["c1", "c3"], ["s1", "c1"], ["s1", "c2"], ["s2", "c2"], ["s2", "c3"], ["s3", "c3"], ["s3", "c1"]]},
    {"id": "CG11-WHEEL4", "nodes": ["h", "a", "b", "c", "d"], "edges": [["a", "b"], ["b", "c"], ["c", "d"], ["a", "d"], ["h", "a"], ["h", "b"], ["h", "c"], ["h", "d"]]},
    {"id": "CG12-DISCONNECTED", "nodes": ["a", "b", "c", "d", "e"], "edges": [["a", "b"], ["b", "c"], ["a", "c"], ["d", "e"]]},
    {"id": "CG13-FAN5", "nodes": ["a", "b", "c", "d", "e"], "edges": [["a", "b"], ["b", "c"], ["c", "d"], ["d", "e"], ["a", "e"], ["a", "c"], ["a", "d"]]},
    {"id": "CG14-EMPTY4", "nodes": ["a", "b", "c", "d"], "edges": []},
    {"id": "CG15-EDGE", "nodes": ["a", "b"], "edges": [["a", "b"]]},
]

SOURCE_LEDGER = [
    {"id": "SRC-01", "title": "NetworkX chordal algorithms", "url": "https://networkx.org/documentation/stable/reference/algorithms/chordal.html", "status": "current", "use": "Algorithm vocabulary and refusal boundaries only; no imported result or conformance claim."},
    {"id": "SRC-02", "title": "NetworkX complete_to_chordal_graph", "url": "https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.chordal.complete_to_chordal_graph.html", "status": "current", "use": "Triangulation vocabulary only; Sable uses a separate finite implementation."},
    {"id": "SRC-03", "title": "W3C PROV-DM", "url": "https://www.w3.org/TR/prov-dm/", "status": "stable", "use": "Provenance and derivation vocabulary only."},
    {"id": "SRC-04", "title": "Python json documentation", "url": "https://docs.python.org/3/library/json.html", "status": "current", "use": "Deterministic JSON serialization vocabulary only."},
    {"id": "SRC-05", "title": "RFC 8259", "url": "https://www.rfc-editor.org/rfc/rfc8259", "status": "stable", "use": "JSON interoperability context only."},
]

def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_value(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))

def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"))

def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((value.rstrip("\r\n") + "\n").encode("utf-8"))

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def git(*args: str, check: bool = True) -> str:
    run = subprocess.run(["git", "-C", str(ROOT), *args], text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and run.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {run.stderr.strip()}")
    return run.stdout.strip()

def git_blob_oid(path: Path) -> str:
    return git("hash-object", f"--path={rel(path)}", str(path))

def manifest_entries(paths: list[Path]) -> list[dict[str, Any]]:
    return [{"path": rel(p), "git_blob": git_blob_oid(p), "bytes": p.stat().st_size, "sha256": sha256_bytes(p.read_bytes())} for p in sorted(paths, key=lambda p: rel(p))]

def owner_files() -> list[Path]:
    if not PHASE_ROOT.exists():
        return []
    return [p for p in PHASE_ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts]

def token_set(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))

def jaccard(a: str, b: str) -> float:
    aa, bb = token_set(a), token_set(b)
    return len(aa & bb) / len(aa | bb) if aa or bb else 1.0

def words(text: str) -> int:
    return len(re.findall(r"\S+", text))

def assert_d_first() -> None:
    if os.name == "nt" and not str(ROOT).lower().startswith("d:\\"):
        raise RuntimeError("owner lane is not D-first")

def stage_paths(stage: str) -> list[Path]:
    stage_dir = PHASE_ROOT / stage
    tools = PHASE_ROOT / "tools"
    stage_tools = {
        "planning": {"phase.txt", "common.py", "build_planning.py", "validate_planning.py", "validate_staged.py"},
        "x1": {"x1_algorithms.py", "build_x1.py", "validate_x1.py"},
        "x2": {"x2_algorithms.py", "build_x2.py", "validate_x2.py"},
        "final": {"build_final.py", "validate_final.py", "canonical.py"},
    }[stage]
    paths = [p for p in stage_dir.rglob("*") if p.is_file() and p.name != "manifest.json"]
    paths += [tools / name for name in stage_tools if (tools / name).exists()]
    return sorted(set(paths), key=lambda p: rel(p))

def build_manifest(stage: str) -> dict[str, Any]:
    entries = manifest_entries(stage_paths(stage))
    return {
        "schema": "ghc.family.git-blob-manifest.v1",
        "owner": OWNER,
        "phase": PHASE,
        "stage": stage,
        "count": len(entries),
        "entries": entries,
        "self_exclusions": [f"{PREFIX.as_posix()}/{stage}/manifest.json"],
        "boundary": "Exact prospective Git-blob byte parity only; not semantic correctness, independent reproduction, or authority.",
    }

def ensure_no_private_text(paths: list[Path]) -> list[dict[str, str]]:
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "windows_absolute_path": re.compile(r"\b[A-Za-z]:\\"),
        "credential_assignment": re.compile(r"(?i)\b(?:password|secret|api[_-]?key|token)\s*[:=]\s*[^\s,}\]]{8,}"),
        "authorization_header": re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._-]{20,}"),
        "private_route_field": re.compile(r"(?i)\b(?:thread_id|source_thread_id|session_stream|private_callable_id)\b"),
    }
    hits: list[dict[str, str]] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": rel(path), "class": name})
    return hits
