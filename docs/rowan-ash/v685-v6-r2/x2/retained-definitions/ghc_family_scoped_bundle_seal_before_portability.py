"""Raw Git-blob owner-delta seal with an exclusive, non-replayed receipt."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime, timezone

def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])

def safe_relative(path):
    return (isinstance(path, str) and bool(path) and not path.startswith(("/", "\\", ":"))
            and "\\" not in path and ":" not in path
            and all(ord(c) >= 32 and ord(c) != 127 for c in path)
            and all(p not in {"", ".", ".."} for p in path.split("/")))

def manifest(repo, source, final, allowed_prefix, allowed_files):
    for ref in (source, final):
        if not re.fullmatch(r"[0-9a-f]{40}", ref):
            raise ValueError("Use an exact full commit")
    git(repo, "merge-base", "--is-ancestor", source, final)
    names = git(repo, "diff", "--name-only", "-z", source, final).decode("utf-8").split("\0")
    rows = []
    for name in filter(None, names):
        if not safe_relative(name) or not (name.startswith(allowed_prefix) or name in allowed_files):
            raise ValueError("Owner scope violation: " + name)
        blob = git(repo, "show", f"{final}:{name}")
        rows.append({"path": name, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    if not rows:
        raise ValueError("Empty owner delta")
    return rows

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--final", required=True)
    ap.add_argument("--policy", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--canonical", action="store_true")
    a = ap.parse_args()
    policy = json.loads(a.policy.read_text(encoding="utf-8"))
    rows = manifest(a.repo, a.source, a.final, policy["allowed_prefix"], set(policy["allowed_files"]))
    state = {}
    if a.canonical:
        marker = a.output.with_suffix(a.output.suffix + ".invocation.json")
        if a.output.exists() or marker.exists():
            raise FileExistsError("Receipt or invocation exists; no replay")
        if git(a.repo, "status", "--porcelain").strip():
            raise ValueError("Working tree must be clean")
        branch = git(a.repo, "symbolic-ref", "--short", "HEAD").decode().strip()
        local = git(a.repo, "rev-parse", "HEAD").decode().strip()
        upstream = git(a.repo, "rev-parse", "@{u}").decode().strip()
        tracking = git(a.repo, "rev-parse", f"refs/remotes/origin/{branch}").decode().strip()
        live = git(a.repo, "ls-remote", "origin", f"refs/heads/{branch}").decode().split()[0]
        if not local == upstream == tracking == live == a.final:
            raise ValueError("Fresh local/upstream/tracking/live equality failed")
        state = dict(local=local, upstream=upstream, tracking=tracking, live=live, clean=True)
        if policy.get("current_hold") is not True:
            raise ValueError("This remaster requires the current terminal hold")
        for check in policy["required_receipts"]:
            content = git(a.repo, "show", f'{a.final}:{check["path"]}')
            obj = json.loads(content)
            if obj.get(check["key"]) != check["expected"]:
                raise ValueError("Required receipt failed: " + check["path"])
        a.output.parent.mkdir(parents=True, exist_ok=True)
        with marker.open("x", encoding="utf-8", newline="\n") as f:
            json.dump({"phase": "v685-v6-r2", "final": a.final, "invocations": 1,
                       "timestamp_utc": datetime.now(timezone.utc).isoformat()}, f, indent=2)
    result = {"schema": "ghc.family.scoped-bundle-seal.v1", "status": "PASS",
              "source": a.source, "final": a.final, "hash_domain": "raw Git blob bytes",
              "owner_file_count": len(rows), "files": rows, "head_state": state,
              "canonical": a.canonical, "success_count": 1 if a.canonical else 0,
              "replays": 0, "delivery": "PREPARED_NOT_SENT", "send_calls": 0}
    with a.output.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    print(json.dumps({k: v for k, v in result.items() if k != "files"}))

if __name__ == "__main__":
    main()
