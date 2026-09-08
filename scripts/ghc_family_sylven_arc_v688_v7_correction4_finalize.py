#!/usr/bin/env python3
"""Prepare and verify exact manifests for Sylven Arc v688-v7 correction 4."""
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
C3 = "b105ef20548eb149b0f88fe9908c5b1ff5d81dca"
DELTA = ROOT / BASE / "correction4/validation/correction-delta-manifest.json"
OWNER = ROOT / BASE / "correction4/validation/corrected-owner-manifest.json"
REVIEW = ROOT / BASE / "correction4/validation/correction-staged-review.json"
SELF = {f"{BASE}/correction4/validation/correction-delta-manifest.json", f"{BASE}/correction4/validation/corrected-owner-manifest.json", f"{BASE}/correction4/validation/correction-staged-review.json"}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def packet(paths: list[str], content: dict[str, bytes], schema: str, scope: str) -> dict:
    return {"schema": schema, "owner": "Sylven Arc", "phase": "v688-v7", "scope": scope, "byte_domain": "exact Git index blobs before correction4 commit", "source": SOURCE, "correction3": C3, "entries": [{"path": path, "bytes": len(content[path]), "sha256": hashlib.sha256(content[path]).hexdigest()} for path in paths], "entry_count": len(paths), "self_exclusions": sorted(SELF)}


def prepare() -> None:
    if any(path.exists() for path in (DELTA, OWNER, REVIEW)) or git("rev-parse", "HEAD") != C3:
        raise RuntimeError("correction4_entry_gate")
    status = [line for line in git("diff", "--cached", "--name-status").splitlines() if line]
    if not status or any(not line.startswith(("A\t", "M\t")) for line in status):
        raise RuntimeError("correction4_status_shape")
    modified = [line.split("\t")[-1] for line in status if line.startswith("M\t")]
    if modified != ["scripts/ghc_family_sylven_arc_v688_v7_canonical.py"]:
        raise RuntimeError("correction4_modified_scope")
    immutable = [f"{BASE}/x1", f"{BASE}/x2", f"{BASE}/final", f"{BASE}/seal", f"{BASE}/validation", f"{BASE}/correction1", f"{BASE}/correction2", f"{BASE}/correction3", f"{BASE}/handoffs/future-seat-14-v688-v8-activation-baton.md", f"{BASE}/handoffs/future-seat-14-v688-v8-correction1-supplement.md", f"{BASE}/handoffs/future-seat-14-v688-v8-correction2-supplement.md", f"{BASE}/handoffs/future-seat-14-v688-v8-correction3-supplement.md"]
    if git("diff", "--name-only", C3, "--", *immutable):
        raise RuntimeError("immutable_correction3_artifact_changed")
    delta_paths = [line for line in git("diff", "--cached", "--name-only", C3).splitlines() if line]
    allowed = lambda path: path.startswith(f"{BASE}/correction4/") or path == f"{BASE}/handoffs/future-seat-14-v688-v8-correction4-supplement.md" or path in {"scripts/build_ghc_family_sylven_arc_v688_v7_correction4.py", "scripts/ghc_family_sylven_arc_v688_v7_canonical.py", "scripts/ghc_family_sylven_arc_v688_v7_correction4_finalize.py", "tests/test_ghc_family_sylven_arc_v688_v7_correction4.py"}
    if any(not allowed(path) for path in delta_paths):
        raise RuntimeError("correction4_allowlist:" + next(path for path in delta_paths if not allowed(path)))
    owner_paths = [line for line in git("diff", "--cached", "--name-only", SOURCE).splitlines() if line]
    if len(owner_paths) >= 2000:
        raise RuntimeError("owner_file_ceiling")
    content = shared.blobs(owner_paths)
    checks = shared.inspect(owner_paths, content)
    seal = json.loads((ROOT / BASE / "correction4/content-seal.json").read_text(encoding="utf-8"))
    for item in seal["targets"]:
        data = (ROOT / item["path"]).read_bytes()
        if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise RuntimeError("content_seal:" + item["path"])
    shared.write_new(DELTA, packet(delta_paths, {path: content[path] for path in delta_paths}, "ghc.family.correction4-delta-manifest.v1", "exact correction4 delta from correction3"))
    shared.write_new(OWNER, packet(owner_paths, content, "ghc.family.correction4-owner-manifest.v1", "complete cardinality-corrected Sylven owner delta from source"))
    shared.write_new(REVIEW, {"schema": "ghc.family.correction4-staged-review.v1", "state": "VALID_EXACT_CORRECTION4_STAGED_PRECOMMIT", "owner": "Sylven Arc", "phase": "v688-v7", "source": SOURCE, "correction3": C3, "checks": checks, "correction_delta_count": len(delta_paths), "owner_file_count": len(owner_paths), "modified_existing_paths": modified, "staged_deletions": 0, "immutable_correction3_artifact_mutations": 0, "content_seal_targets": len(seal["targets"]), "targeted_test_observation": {"module": "tests.test_ghc_family_sylven_arc_v688_v7_correction4", "tests": 5, "passed": 5, "failed": 0, "replay_count": 0}, "prior_failed_canonical_receipts": ["526b15d930704f592486754db0547a594f0590329728cb7084de89a797eb2014", "0383cb436f6167a1d80d552dd961f67e97613f207273947868eb11cc99655c10"], "current_exact_head_canonical_invocations": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    print(json.dumps({"state": "VALID_EXACT_CORRECTION4_STAGED_PRECOMMIT", "correction_delta": len(delta_paths), "owner_files": len(owner_paths), **checks}, sort_keys=True))


def verify() -> None:
    delta = json.loads(DELTA.read_text(encoding="utf-8")); owner = json.loads(OWNER.read_text(encoding="utf-8")); review = json.loads(REVIEW.read_text(encoding="utf-8"))
    delta_paths = [line for line in git("diff", "--cached", "--name-only", C3).splitlines() if line]
    owner_paths = [line for line in git("diff", "--cached", "--name-only", SOURCE).splitlines() if line]
    if set(delta_paths) != {item["path"] for item in delta["entries"]} | SELF or set(owner_paths) != {item["path"] for item in owner["entries"]} | SELF:
        raise RuntimeError("manifest_path_set")
    content = shared.blobs(owner_paths); checks = shared.inspect(owner_paths, content)
    for manifest in (delta, owner):
        for item in manifest["entries"]:
            data = content[item["path"]]
            if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
                raise RuntimeError("manifest_blob:" + item["path"])
    if review["state"] != "VALID_EXACT_CORRECTION4_STAGED_PRECOMMIT":
        raise RuntimeError("review_state")
    print(json.dumps({"state": "VERIFIED_EXACT_CORRECTION4_STAGE", "correction_delta": len(delta_paths), "owner_files": len(owner_paths), "manifest_entries": len(delta["entries"]) + len(owner["entries"]), "self_exclusions": 3, **checks}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("mode", choices=("prepare", "verify")); args = parser.parse_args()
    prepare() if args.mode == "prepare" else verify()


if __name__ == "__main__":
    main()
