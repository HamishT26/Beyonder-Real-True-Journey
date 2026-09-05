"""Build an exact additive owner allowlist and normalized-LF manifest before staging."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = Path("docs/neris-solane/v686-v1")


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True, encoding="utf-8").rstrip("\n")


def write(path: Path, value) -> None:
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")


def content(path: Path) -> bytes:
    data = (ROOT / path).read_bytes()
    return data if path.suffix.lower() == ".pdf" else data.replace(b"\r\n", b"\n")


def status_paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "-uall").splitlines()
    result = []
    for row in rows:
        code = row[:2]
        path = row[3:]
        if code not in ("??", " A", "A ", " M", "M "):
            raise ValueError("Non-additive or unsupported status row: " + row)
        result.append(path.replace("\\", "/"))
    return sorted(result)


def allowed(path: str, stage: str) -> bool:
    if path.startswith("docs/neris-solane/v686-v1/"):
        if stage == "evidence":
            return any(path.startswith(prefix) for prefix in [
                "docs/neris-solane/v686-v1/x2/",
                "docs/neris-solane/v686-v1/skills/",
                "docs/neris-solane/v686-v1/tooling/",
                "docs/neris-solane/v686-v1/validation/evidence-",
            ])
        return any(path.startswith(prefix) for prefix in [
            "docs/neris-solane/v686-v1/final/",
            "docs/neris-solane/v686-v1/validation/final-",
        ])
    if stage == "evidence":
        return (
            path.startswith("scripts/build_ghc_family_neris_solane_v686_v1_")
            or path.startswith("scripts/ghc_family_neris_solane_v686_v1_")
            or path.startswith("scripts/ghc_family_report_")
            or path == "tests/test_ghc_family_neris_solane_v686_v1_x2.py"
        )
    return path in {
        "scripts/ghc_family_neris_solane_v686_v1_canonical.py",
        "scripts/ghc_family_neris_solane_v686_v1_overview_pdf.py",
        "scripts/build_ghc_family_neris_solane_v686_v1_final.py",
        "tests/test_ghc_family_neris_solane_v686_v1_final.py",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True, choices=["evidence", "final"])
    parser.add_argument("--base", required=True)
    args = parser.parse_args()
    if git("rev-parse", "HEAD") != args.base:
        raise ValueError("Manifest base must equal current HEAD")
    validation = PHASE_ROOT / "validation"
    generated = [
        validation / f"{args.stage}-allowlist.json",
        validation / f"{args.stage}-manifest.json",
        validation / f"{args.stage}-preflight.json",
        validation / f"{args.stage}-staged-review.json",
    ]
    existing = status_paths()
    if any(str(path).replace("\\", "/") in existing for path in generated):
        raise FileExistsError("Refusing to overwrite an existing manifest stage")
    paths = sorted(set(existing + [path.as_posix() for path in generated]))
    rejected = [path for path in paths if not allowed(path, args.stage)]
    if rejected:
        raise ValueError("Paths outside owner stage allowlist: " + repr(rejected[:10]))
    if len(paths) != len(set(paths)):
        raise ValueError("Duplicate owner paths")
    materialized = sum(1 for path in ROOT.rglob("*") if path.is_file())
    if materialized >= 2000 or len(paths) >= 2000:
        raise ValueError("The 2,000-file rotation ceiling was reached")
    write(generated[0], {"stage": args.stage, "base": args.base, "paths": paths, "zero_deletions_required": True})
    write(
        generated[2],
        {
            "stage": args.stage,
            "base": args.base,
            "owner": "Neris Solane",
            "phase": "v686-v1",
            "expected_path_count": len(paths),
            "materialized_file_count": materialized,
            "materialized_file_ceiling": 2000,
            "repository_scan": False,
            "unchanged_history_scan": False,
            "cross_lane_scan": False,
            "sibling_lane_mutation": False,
            "status": "READY_FOR_EXACT_STAGING",
        },
    )
    write(
        generated[3],
        {
            "stage": args.stage,
            "base": args.base,
            "observed_uncommitted_owner_paths": existing,
            "expected_staged_paths": paths,
            "missing_before_stage": [],
            "extra_before_stage": [],
            "state": "OWNER_DELTA_READY_FOR_EXACT_STAGING",
            "claim_boundary": "Actual Git staging equality is a separate terminal command witness.",
        },
    )
    entries = []
    manifest_path = generated[1].as_posix()
    for path_text in paths:
        if path_text == manifest_path:
            continue
        path = Path(path_text)
        payload = content(path)
        entries.append({"path": path_text, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
    write(
        generated[1],
        {
            "schema": "ghc.family.neris.git-blob-manifest.v1",
            "stage": args.stage,
            "base": args.base,
            "hash_domain": "normalized-LF Git blob bytes for text and raw bytes for PDF",
            "entries": entries,
            "self_exclusions": [manifest_path],
        },
    )
    print(json.dumps({"stage": args.stage, "paths": len(paths), "manifest_entries": len(entries), "materialized_files": materialized}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
