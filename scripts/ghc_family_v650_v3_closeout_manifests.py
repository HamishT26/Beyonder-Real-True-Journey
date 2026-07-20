"""Build exact closeout staged and owner manifests with explicit self-exclusions."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PHASE = "docs/sable-rook/v650-v3"
OUTPUTS = [
    f"{PHASE}/validation/final-owner-manifest.json",
    f"{PHASE}/validation/final-staged-manifest.json",
    f"{PHASE}/validation/final-staged-privacy.json",
    f"{PHASE}/validation/final-staged-review.json",
]
PATTERNS = {
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(r"(?:[A-Z]:\\Users\\|/home/[^/\s]+/|/Users/[^/\s]+/)", re.I),
    "private_uri": re.compile(r"(?:codex|vscode|file)://", re.I),
    "credential_assignment": re.compile(r"(?i)(?:api[_-]?key|password|secret)\s*[:=]\s*['\"][^'\"]+"),
    "delegation_markup": re.compile(r"<codex_delegation>|<source_thread_id>|<thread_id>", re.I),
}


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=REPO, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def index_oids() -> dict[str, str]:
    rows: dict[str, str] = {}
    for raw in run("git", "ls-files", "-s", "-z").stdout.split(b"\0"):
        if not raw:
            continue
        metadata, encoded_path = raw.split(b"\t", 1)
        rows[encoded_path.decode()] = metadata.split()[1].decode()
    return rows


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        check=True,
        input=("\n".join(unique) + "\n").encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output = proc.stdout
    offset = 0
    blobs: dict[str, bytes] = {}
    for expected in unique:
        newline = output.index(b"\n", offset)
        header = output[offset:newline].decode().split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header for {expected}: {' '.join(header)}")
        size = int(header[2])
        start = newline + 1
        end = start + size
        blobs[expected] = output[start:end]
        offset = end + 1
    return blobs


def entry(path: str, oids: dict[str, str], blobs: dict[str, bytes]) -> dict:
    try:
        oid = oids[path]
        data = blobs[oid]
    except KeyError as exc:
        raise RuntimeError(f"missing index blob {path}") from exc
    return {"path": path, "git_blob": oid, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main() -> int:
    staged = sorted(p.decode() for p in run("git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").stdout.split(b"\0") if p)
    staged_content = [p for p in staged if p not in OUTPUTS]
    tracked = sorted(p.decode() for p in run("git", "ls-files", "-z", "--", PHASE).stdout.split(b"\0") if p)
    owner_paths = sorted(set(tracked) | {p for p in staged_content if p.startswith(PHASE + "/")})
    owner_content = [p for p in owner_paths if p not in OUTPUTS]
    oids = index_oids()
    requested_oids = [oids[p] for p in dict.fromkeys(staged_content + owner_content)]
    blobs = batch_blobs(requested_oids)
    staged_entries = [entry(p, oids, blobs) for p in staged_content]
    owner_entries = [entry(p, oids, blobs) for p in owner_content]
    candidates = []
    confirmed = []
    for row in owner_entries:
        data = blobs[row["git_blob"]]
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                disposition = "scanner_definition" if "closeout_manifests.py" in row["path"] else "confirmed_payload"
                item = {"path": row["path"], "class": class_name, "line": text.count("\n", 0, match.start()) + 1, "disposition": disposition}
                candidates.append(item)
                if disposition == "confirmed_payload":
                    confirmed.append(item)
    hygiene = run("git", "diff", "--cached", "--check", check=False)
    x1 = json.loads((REPO / f"{PHASE}/validation/x1-staged-manifest.json").read_text(encoding="utf-8"))
    x1_paths = {r["path"] for r in x1["entries"]} | set(x1["self_exclusions"])
    x1_changes = sorted(set(staged) & x1_paths)
    manifest_common = {"hash_domain": "git_index_blob", "self_exclusions": OUTPUTS}
    payloads = {
        OUTPUTS[0]: {"schema": "ghc.family.v650-v3.final-owner-manifest.v1", **manifest_common, "entry_count": len(owner_entries), "entries": owner_entries},
        OUTPUTS[1]: {"schema": "ghc.family.v650-v3.final-staged-manifest.v1", **manifest_common, "entry_count": len(staged_entries), "entries": staged_entries},
        OUTPUTS[2]: {"schema": "ghc.family.v650-v3.final-staged-privacy.v1", "pattern_classes": list(PATTERNS), "owner_scanned_count": len(owner_entries), "candidate_count": len(candidates), "confirmed_hit_count": len(confirmed), "candidates": candidates, "confirmed_hits": confirmed, "complete_privacy_claim": False},
        OUTPUTS[3]: {"schema": "ghc.family.v650-v3.final-staged-review.v1", "intended_path_count": len(staged_entries) + len(OUTPUTS), "manifest_entry_count": len(staged_entries), "owner_entry_count": len(owner_entries), "self_exclusion_count": len(OUTPUTS), "x1_frozen_changes": x1_changes, "privacy_confirmed_hits": len(confirmed), "diff_hygiene_issue_count": len(hygiene.stdout.decode(errors="replace").splitlines()), "passed": not x1_changes and not confirmed and hygiene.returncode == 0},
    }
    for relative, value in payloads.items():
        target = REPO / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"staged_entries": len(staged_entries), "owner_entries": len(owner_entries), "self_exclusions": len(OUTPUTS), "confirmed_hits": len(confirmed), "x1_changes": len(x1_changes), "passed": payloads[OUTPUTS[3]]["passed"]}, sort_keys=True))
    return 0 if payloads[OUTPUTS[3]]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
