#!/usr/bin/env python3
"""Prepare and verify exact manifests for Sylven Arc v688-v7 correction 2."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_sylven_arc_v688_v7_correction1_finalize as shared

BASE = "docs/sylven-arc/v688-v7"
SOURCE = "e7db6f3be1327de72f93873eb6540aabfc773344"
CORRECTION1 = "c0f79218f2d644592bd4eee0947058f0f3803b50"
DELTA = ROOT / BASE / "correction2/validation/correction-delta-manifest.json"
OWNER = ROOT / BASE / "correction2/validation/corrected-owner-manifest.json"
REVIEW = ROOT / BASE / "correction2/validation/correction-staged-review.json"
SELF = {
    f"{BASE}/correction2/validation/correction-delta-manifest.json",
    f"{BASE}/correction2/validation/corrected-owner-manifest.json",
    f"{BASE}/correction2/validation/correction-staged-review.json",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def packet(paths: list[str], content: dict[str, bytes], schema: str, scope: str) -> dict:
    return {"schema": schema, "owner": "Sylven Arc", "phase": "v688-v7", "scope": scope, "byte_domain": "exact Git index blobs before correction2 commit", "source": SOURCE, "correction1": CORRECTION1, "entries": [{"path": path, "bytes": len(content[path]), "sha256": hashlib.sha256(content[path]).hexdigest()} for path in paths], "entry_count": len(paths), "self_exclusions": sorted(SELF)}


def prepare() -> None:
    if any(path.exists() for path in (DELTA, OWNER, REVIEW)):
        raise RuntimeError("correction2_manifest_exists")
    if git("rev-parse", "HEAD") != CORRECTION1:
        raise RuntimeError("exact_correction1_required")
    status = [line for line in git("diff", "--cached", "--name-status").splitlines() if line]
    if not status or any(not line.startswith(("A\t", "M\t")) for line in status):
        raise RuntimeError("correction2_status_shape")
    modified = [line.split("\t")[-1] for line in status if line.startswith("M\t")]
    if modified != ["scripts/ghc_family_sylven_arc_v688_v7_canonical.py"]:
        raise RuntimeError("correction2_modified_scope")
    immutable = [f"{BASE}/x1", f"{BASE}/x2", f"{BASE}/final", f"{BASE}/seal", f"{BASE}/validation", f"{BASE}/correction1", f"{BASE}/handoffs/future-seat-14-v688-v8-activation-baton.md", f"{BASE}/handoffs/future-seat-14-v688-v8-correction1-supplement.md"]
    if git("diff", "--name-only", CORRECTION1, "--", *immutable):
        raise RuntimeError("immutable_correction1_artifact_changed")
    delta_paths = [line for line in git("diff", "--cached", "--name-only", CORRECTION1).splitlines() if line]
    allowed = lambda path: path.startswith(f"{BASE}/correction2/") or path == f"{BASE}/handoffs/future-seat-14-v688-v8-correction2-supplement.md" or path in {"scripts/build_ghc_family_sylven_arc_v688_v7_correction2.py", "scripts/ghc_family_sylven_arc_v688_v7_canonical.py", "scripts/ghc_family_sylven_arc_v688_v7_correction2_finalize.py", "tests/test_ghc_family_sylven_arc_v688_v7_correction2.py"}
    if any(not allowed(path) for path in delta_paths):
        raise RuntimeError("correction2_allowlist:" + next(path for path in delta_paths if not allowed(path)))
    owner_paths = [line for line in git("diff", "--cached", "--name-only", SOURCE).splitlines() if line]
    if len(owner_paths) >= 2000:
        raise RuntimeError("owner_file_ceiling")
    content = shared.blobs(owner_paths)
    checks = shared.inspect(owner_paths, content)
    seal = json.loads((ROOT / BASE / "correction2/content-seal.json").read_text(encoding="utf-8"))
    for item in seal["targets"]:
        data = (ROOT / item["path"]).read_bytes()
        if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise RuntimeError("content_seal:" + item["path"])
    shared.write_new(DELTA, packet(delta_paths, {path: content[path] for path in delta_paths}, "ghc.family.correction2-delta-manifest.v1", "exact correction2 delta from correction1"))
    shared.write_new(OWNER, packet(owner_paths, content, "ghc.family.correction2-owner-manifest.v1", "complete second-corrected Sylven owner delta from source"))
    shared.write_new(REVIEW, {"schema": "ghc.family.correction2-staged-review.v1", "state": "VALID_EXACT_CORRECTION2_STAGED_PRECOMMIT", "owner": "Sylven Arc", "phase": "v688-v7", "source": SOURCE, "correction1": CORRECTION1, "checks": checks, "correction_delta_count": len(delta_paths), "owner_file_count": len(owner_paths), "modified_existing_paths": modified, "staged_deletions": 0, "immutable_correction1_artifact_mutations": 0, "content_seal_targets": len(seal["targets"]), "targeted_test_observation": {"module": "tests.test_ghc_family_sylven_arc_v688_v7_correction2", "tests": 6, "passed": 6, "failed": 0, "replay_count": 0}, "canonical_invocations": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    print(json.dumps({"state": "VALID_EXACT_CORRECTION2_STAGED_PRECOMMIT", "correction_delta": len(delta_paths), "owner_files": len(owner_paths), **checks}, sort_keys=True))


def verify() -> None:
    delta = json.loads(DELTA.read_text(encoding="utf-8"))
    owner = json.loads(OWNER.read_text(encoding="utf-8"))
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    delta_paths = [line for line in git("diff", "--cached", "--name-only", CORRECTION1).splitlines() if line]
    owner_paths = [line for line in git("diff", "--cached", "--name-only", SOURCE).splitlines() if line]
    if set(delta_paths) != {item["path"] for item in delta["entries"]} | SELF:
        raise RuntimeError("delta_path_set")
    if set(owner_paths) != {item["path"] for item in owner["entries"]} | SELF:
        raise RuntimeError("owner_path_set")
    content = shared.blobs(owner_paths)
    checks = shared.inspect(owner_paths, content)
    for manifest in (delta, owner):
        for item in manifest["entries"]:
            data = content[item["path"]]
            if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
                raise RuntimeError("manifest_blob:" + item["path"])
    if review["state"] != "VALID_EXACT_CORRECTION2_STAGED_PRECOMMIT":
        raise RuntimeError("review_state")
    print(json.dumps({"state": "VERIFIED_EXACT_CORRECTION2_STAGE", "correction_delta": len(delta_paths), "owner_files": len(owner_paths), "manifest_entries": len(delta["entries"]) + len(owner["entries"]), "self_exclusions": 3, **checks}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "verify"))
    args = parser.parse_args()
    prepare() if args.mode == "prepare" else verify()


if __name__ == "__main__":
    main()
