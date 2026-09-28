from __future__ import annotations

import json
import subprocess
import sys

from common import PREFIX, ROOT

def git_bytes(*args: str) -> bytes:
    run = subprocess.run(["git", "-C", str(ROOT), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if run.returncode:
        raise RuntimeError(run.stderr.decode("utf-8", "replace"))
    return run.stdout

def main() -> None:
    stage = sys.argv[1]
    manifest_path = f"{PREFIX.as_posix()}/{stage}/manifest.json"
    names = [line for line in git_bytes("diff", "--cached", "--name-only", "--diff-filter=ACMR").decode().splitlines() if line]
    if not names or any(not n.startswith(PREFIX.as_posix() + "/") for n in names):
        raise SystemExit(json.dumps({"state": "STAGED_SCOPE_INVALID", "names": names}))
    manifest = json.loads(git_bytes("show", f":{manifest_path}").decode("utf-8"))
    mismatches = []
    for entry in manifest["entries"]:
        try:
            oid = git_bytes("rev-parse", f":{entry['path']}").decode().strip()
        except Exception:
            mismatches.append(entry["path"])
            continue
        if oid != entry["git_blob"]:
            mismatches.append(entry["path"])
    json_count = 0
    for name in names:
        data = git_bytes("show", f":{name}")
        if name.endswith(".json"):
            json.loads(data.decode("utf-8")); json_count += 1
        if data.endswith(b"\n\n"):
            raise RuntimeError(f"double terminal newline: {name}")
    expected = {e["path"] for e in manifest["entries"]} | set(manifest["self_exclusions"])
    if set(names) != expected or mismatches:
        raise SystemExit(json.dumps({"state": "STAGED_MANIFEST_INVALID", "missing": sorted(expected-set(names)), "extra": sorted(set(names)-expected), "mismatches": mismatches}))
    print(json.dumps({"state": "VALID_EXACT_STAGED_SURFACE", "stage": stage, "paths": len(names), "manifest_entries": len(manifest["entries"]), "json": json_count}, sort_keys=True))

if __name__ == "__main__":
    main()
