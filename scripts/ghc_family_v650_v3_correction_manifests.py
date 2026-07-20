"""Build exact terminal-correction manifests for v650-v3."""

from __future__ import annotations

import json

from ghc_family_v650_v3_closeout_manifests import PATTERNS, REPO, batch_blobs, entry, index_oids, run

PHASE = "docs/sable-rook/v650-v3"
OUTPUTS = [
    f"{PHASE}/validation/correction-owner-manifest.json",
    f"{PHASE}/validation/correction-staged-manifest.json",
    f"{PHASE}/validation/correction-staged-privacy.json",
    f"{PHASE}/validation/correction-staged-review.json",
]


def main() -> int:
    staged = sorted(
        path.decode()
        for path in run("git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").stdout.split(b"\0")
        if path
    )
    staged_content = [path for path in staged if path not in OUTPUTS]
    tracked = sorted(path.decode() for path in run("git", "ls-files", "-z", "--", PHASE).stdout.split(b"\0") if path)
    owner_paths = sorted(set(tracked) | {path for path in staged_content if path.startswith(PHASE + "/")})
    owner_content = [path for path in owner_paths if path not in OUTPUTS]
    oids = index_oids()
    requested_oids = [oids[path] for path in dict.fromkeys(staged_content + owner_content)]
    blobs = batch_blobs(requested_oids)
    staged_entries = [entry(path, oids, blobs) for path in staged_content]
    owner_entries = [entry(path, oids, blobs) for path in owner_content]
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
                item = {
                    "path": row["path"],
                    "class": class_name,
                    "line": text.count("\n", 0, match.start()) + 1,
                    "disposition": "confirmed_payload",
                }
                candidates.append(item)
                confirmed.append(item)
    hygiene = run("git", "diff", "--cached", "--check", check=False)
    x1 = json.loads((REPO / f"{PHASE}/validation/x1-staged-manifest.json").read_text(encoding="utf-8"))
    x1_paths = {row["path"] for row in x1["entries"]} | set(x1["self_exclusions"])
    x1_changes = sorted(set(staged) & x1_paths)
    manifest_common = {"hash_domain": "git_index_blob", "self_exclusions": OUTPUTS}
    payloads = {
        OUTPUTS[0]: {
            "schema": "ghc.family.v650-v3.correction-owner-manifest.v1",
            **manifest_common,
            "entry_count": len(owner_entries),
            "entries": owner_entries,
        },
        OUTPUTS[1]: {
            "schema": "ghc.family.v650-v3.correction-staged-manifest.v1",
            **manifest_common,
            "entry_count": len(staged_entries),
            "entries": staged_entries,
        },
        OUTPUTS[2]: {
            "schema": "ghc.family.v650-v3.correction-staged-privacy.v1",
            "pattern_classes": list(PATTERNS),
            "owner_scanned_count": len(owner_entries),
            "candidate_count": len(candidates),
            "confirmed_hit_count": len(confirmed),
            "candidates": candidates,
            "confirmed_hits": confirmed,
            "complete_privacy_claim": False,
        },
        OUTPUTS[3]: {
            "schema": "ghc.family.v650-v3.correction-staged-review.v1",
            "intended_path_count": len(staged_entries) + len(OUTPUTS),
            "manifest_entry_count": len(staged_entries),
            "owner_entry_count": len(owner_entries),
            "self_exclusion_count": len(OUTPUTS),
            "x1_frozen_changes": x1_changes,
            "privacy_confirmed_hits": len(confirmed),
            "diff_hygiene_issue_count": len(hygiene.stdout.decode(errors="replace").splitlines()),
            "passed": not x1_changes and not confirmed and hygiene.returncode == 0,
        },
    }
    for relative, value in payloads.items():
        target = REPO / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    result = {
        "staged_entries": len(staged_entries),
        "owner_entries": len(owner_entries),
        "self_exclusions": len(OUTPUTS),
        "confirmed_hits": len(confirmed),
        "x1_changes": len(x1_changes),
        "passed": payloads[OUTPUTS[3]]["passed"],
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
