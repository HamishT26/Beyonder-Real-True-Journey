"""Build exact final staged and owner manifests for Orin v650-v4."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PHASE = "docs/orin-thale/v650-v4"
OUTPUTS = [
    f"{PHASE}/validation/final-owner-manifest.json",
    f"{PHASE}/validation/final-staged-manifest.json",
    f"{PHASE}/validation/final-staged-privacy.json",
    f"{PHASE}/validation/final-staged-review.json",
]
FROZEN_X1_PREFIXES = (
    f"{PHASE}/x1-preregistration.md",
    f"{PHASE}/x1-proposals.json",
    f"{PHASE}/provenance/proposal-collision-audit.json",
    f"{PHASE}/sources/",
    f"{PHASE}/portfolios/safe-now-plan.json",
    f"{PHASE}/portfolios/candidate-plan.json",
    f"{PHASE}/portfolios/skill-plan.json",
    f"{PHASE}/portfolios/runner-plan.json",
    f"{PHASE}/portfolios/clean-fix-refine-plan.json",
    f"{PHASE}/validation/x1-synthetic-mutation-plan.json",
)
SCANNER_DEFINITION_FILES = {
    "scripts/ghc_family_v650_v4_staged_review.py",
    "scripts/ghc_family_v650_v4_closeout_manifests.py",
    "scripts/ghc_family_v650_v4_final_validate.py",
}
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
        if raw:
            meta, path = raw.split(b"\t", 1)
            rows[path.decode()] = meta.split()[1].decode()
    return rows


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    proc = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=REPO, check=True,
        input=("\n".join(unique) + "\n").encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    output = proc.stdout
    offset = 0
    blobs: dict[str, bytes] = {}
    for expected in unique:
        newline = output.index(b"\n", offset)
        header = output[offset:newline].decode().split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header for {expected}")
        size = int(header[2])
        start = newline + 1
        end = start + size
        blobs[expected] = output[start:end]
        offset = end + 1
    return blobs


def entry(path: str, oids: dict[str, str], blobs: dict[str, bytes]) -> dict:
    oid = oids[path]
    data = blobs[oid]
    return {"path": path, "git_blob": oid, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main() -> int:
    staged = sorted(p.decode() for p in run("git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").stdout.split(b"\0") if p)
    staged_content = [p for p in staged if p not in OUTPUTS]
    tracked = sorted(p.decode() for p in run("git", "ls-files", "-z", "--", PHASE).stdout.split(b"\0") if p)
    owner_paths = sorted(set(tracked) | {p for p in staged_content if p.startswith(PHASE + "/")})
    owner_content = [p for p in owner_paths if p not in OUTPUTS]
    oids = index_oids()
    missing = [p for p in staged_content + owner_content if p not in oids]
    if missing:
        raise RuntimeError(f"missing index paths: {missing[:3]}")
    blobs = batch_blobs([oids[p] for p in dict.fromkeys(staged_content + owner_content)])
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
                disposition = "scanner_definition" if row["path"] in SCANNER_DEFINITION_FILES else "confirmed_payload"
                item = {"path": row["path"], "class": class_name, "line": text.count("\n", 0, match.start()) + 1, "disposition": disposition}
                candidates.append(item)
                if disposition == "confirmed_payload":
                    confirmed.append(item)
    hygiene = run("git", "diff", "--cached", "--check", check=False)
    frozen_changes = sorted(path for path in staged if any(path == prefix or path.startswith(prefix) for prefix in FROZEN_X1_PREFIXES))
    common = {"hash_domain": "git_index_blob", "self_exclusions": OUTPUTS}
    payloads = {
        OUTPUTS[0]: {"schema": "ghc.family.v650-v4.final-owner-manifest.v1", **common, "entry_count": len(owner_entries), "entries": owner_entries},
        OUTPUTS[1]: {"schema": "ghc.family.v650-v4.final-staged-manifest.v1", **common, "entry_count": len(staged_entries), "entries": staged_entries},
        OUTPUTS[2]: {"schema": "ghc.family.v650-v4.final-staged-privacy.v1", "pattern_classes": list(PATTERNS), "owner_scanned_count": len(owner_entries), "candidate_count": len(candidates), "confirmed_hit_count": len(confirmed), "candidates": candidates, "confirmed_hits": confirmed, "complete_privacy_claim": False},
        OUTPUTS[3]: {"schema": "ghc.family.v650-v4.final-staged-review.v1", "intended_path_count": len(staged_entries) + len(OUTPUTS), "manifest_entry_count": len(staged_entries), "owner_entry_count": len(owner_entries), "self_exclusion_count": len(OUTPUTS), "frozen_x1_changes": frozen_changes, "privacy_confirmed_hits": len(confirmed), "diff_hygiene_issue_count": len(hygiene.stdout.decode(errors="replace").splitlines()), "passed": not frozen_changes and not confirmed and hygiene.returncode == 0},
    }
    for relative, value in payloads.items():
        target = REPO / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"staged_entries": len(staged_entries), "owner_entries": len(owner_entries), "self_exclusions": len(OUTPUTS), "confirmed_hits": len(confirmed), "frozen_x1_changes": len(frozen_changes), "passed": payloads[OUTPUTS[3]]["passed"]}, sort_keys=True))
    return 0 if payloads[OUTPUTS[3]]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
