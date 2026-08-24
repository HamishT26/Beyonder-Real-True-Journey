"""Build the additive canonical-dependency correction overlay for Neris r3."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "neris-solane" / "v667-v8-r3"
FAILED_FINAL = "68979e155cf1dc27a3fc967657f613cc3b1172c2"
EVIDENCE_HEAD = "08dd119b863c7103607b8399b3a201b5cb511af9"
X1_HEAD = "705f4cda336639d2a700d2d830a975cd281c7e4b"
FAILURE_RECEIPT = Path(f"{chr(68)}:{os.sep}") / "GHC-Archives" / "receipts" / "neris-solane-v667-v8-r3" / "canonical-exact-final-receipt.json"
FAILURE_RECEIPT_SHA256 = "74c29c0a4b38128a591ae1e9f4867d457d35ae8ed84d3b2505a40aa0370b9a14"
CORRECTED_OWNER_MANIFEST = PHASE / "validation" / "corrected-owner-manifest.json"
CORRECTION_DELTA_MANIFEST = PHASE / "validation" / "correction-delta-manifest.json"
FILE_CEILING = 2000


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(payload))
    return path


def write_text(relative: str, text: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def git(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(ROOT), *arguments], text=True, encoding="utf-8", errors="replace", capture_output=True, check=check)


def owner_files() -> list[Path]:
    return sorted([path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts], key=lambda path: path.relative_to(ROOT).as_posix())


def entries(paths: list[Path]) -> list[dict[str, Any]]:
    return [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size} for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix())]


def privacy_candidates(paths: list[Path]) -> list[dict[str, str]]:
    patterns = {
        "windows_absolute_path": re.compile(r"(?<![A-Za-z])[A-Z]:[\\/]+", re.I),
        "raw_thread_or_session_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "credential_assignment": re.compile(r"(?:api[_-]?key|pass" + r"word|sec" + r"ret|bearer)\s*[:=]\s*[^\s\"<]{8,}", re.I),
        "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        "private_route_or_resume_value": re.compile(r"(?:resume|session|thread)[_-]?(?:id|token)\s*[:=]\s*[^\s\"<]{8,}", re.I),
    }
    hits = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                hits.append({"class": class_name, "path": path.relative_to(ROOT).as_posix(), "match_sha256": hashlib.sha256(match.group(0).encode()).hexdigest()})
    return hits


def manifest_replay(path: Path) -> int:
    payload = json.loads(path.read_text(encoding="utf-8"))
    for row in payload["entries"]:
        target = ROOT / row["path"]
        if not target.is_file() or target.stat().st_size != row["bytes"] or sha256(target) != row["sha256"]:
            raise AssertionError(f"manifest mismatch: {row['path']}")
    return len(payload["entries"])


def build() -> dict[str, Any]:
    if git("rev-parse", "HEAD").stdout.strip() != FAILED_FINAL:
        raise RuntimeError("correction must begin at the exact failed canonical final")
    if git("rev-parse", "HEAD^").stdout.strip() != EVIDENCE_HEAD:
        raise RuntimeError("failed final parent drift")
    if not FAILURE_RECEIPT.is_file() or sha256(FAILURE_RECEIPT) != FAILURE_RECEIPT_SHA256:
        raise RuntimeError("canonical failure receipt anchor drift")
    failure = json.loads(FAILURE_RECEIPT.read_text(encoding="utf-8"))
    if failure["state"] != "INVALID_ZERO_CANONICAL_SUCCESS_CREDIT" or failure["canonical_success_count"] != 0:
        raise RuntimeError("canonical failure truth drift")

    write_json(
        "correction/canonical-failure-anchor.json",
        {
            "state": failure["state"],
            "failed_head": FAILED_FINAL,
            "failure_receipt_sha256": FAILURE_RECEIPT_SHA256,
            "error": failure["error"],
            "canonical_invocation_count": 1,
            "canonical_success_count": 0,
            "canonical_replay_authorized": False,
            "canonical_replayed": False,
            "credit": 0,
        },
    )
    write_json(
        "correction/method-flow-external-overlay.json",
        {
            "repository_sealed_x2": {"effective_negatives": 28733, "methods": 15319, "open_gaps": 203, "exact_gates": 201, "failed_witnesses": 1034, "passing_witnesses": 1875},
            "external_canonical_failure_addition": {"effective_negatives": 1, "methods": 1, "failed_witnesses": 1, "passing_witnesses": 0},
            "corrected_activation_overlay": {"effective_negatives": 28734, "methods": 15320, "open_gaps": 203, "exact_gates": 201, "failed_witnesses": 1035, "passing_witnesses": 1875},
            "repository_seal_rewritten": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text(
        "correction/canonical-dependency-recovery.md",
        """# Canonical dependency recovery

The one exact-final canonical invocation ran once and failed once. It earned zero
canonical aggregate-success credit and must never be replayed. The isolated
finding was the scanner's own rule string, not an executable subprocess shell
argument and not a call to the Python dynamic-evaluation builtins.

The additive recovery leaves the failed-final tree and manifests unchanged. A
new AST-based dependency check distinguishes string literals from executable
call structure, and a separate bounded component composite validates the new
corrected head. That composite is same-owner evidence under shared
infrastructure; it is not the canonical aggregate, independent reproduction,
external audit, exhaustive security, or Stage 20 authority.
""",
    )
    write_text(
        "handoffs/vesper-arlen-v668-v1-correction-overlay.md",
        f"""# Vesper Arlen v668-v1 correction overlay

Read the 24,519-word primary baton at
`docs/neris-solane/v667-v8-r3/handoffs/vesper-arlen-v668-v1-activation-prepared.md`
completely through EOF, then read this overlay.

The primary baton is unchanged commit-time evidence. Its canonical state was
subsequently resolved by exactly one invocation at `{FAILED_FINAL}`, which
failed on a bounded security-scanner self-match and earned zero canonical
success credit. Receipt SHA-256: `{FAILURE_RECEIPT_SHA256}`.

The exact corrected final is the commit containing this overlay and will be
supplied by the one acknowledged live activation. Verify it freshly across
local, upstream, tracking, and live remote. The terminal evidence class is
`VALID_DEPENDENCY_CORRECTED_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT` only
if the separate recovery receipt says so. Do not describe it as a successful
canonical aggregate or independent reproduction.

All proposal outcomes and repository-sealed counts remain unchanged. The live
external overlay adds one retained canonical failure: 28,734 effective
negatives, 15,320 methods, 203 open gaps, 201 exact gates, 1,035 failed
witnesses, and 1,875 bounded passing witnesses. The verdict remains
`NOT_READY_FOR_STAGE_20`.

Delivery is still `PREPARED_NOT_SENT`. Vesper remains the only prospective
recipient, Tavian remains on standby, no substitute endpoint is authorized,
and Vesper's prospective post-gate next exact-title task remains Lyren Moss for
v668-v2 subject to a fresh live roster and authority reread.
""",
    )
    write_json(
        "route/vesper-arlen-v668-v1-correction-route.json",
        {
            "delivery_state": "PREPARED_NOT_SENT",
            "recipient_exact_title": "Vesper Arlen",
            "recipient_phase": "v668-v1",
            "failed_final": FAILED_FINAL,
            "exact_corrected_final_resolution": "commit containing the correction overlay; exact SHA supplied by acknowledged live message",
            "canonical_state": "INVALID_ZERO_CANONICAL_SUCCESS_CREDIT",
            "required_recovery_state": "VALID_DEPENDENCY_CORRECTED_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT",
            "canonical_replay_allowed": False,
            "successor_contacted": False,
            "tavian_state": "ON_STANDBY",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "correction/correction-build-receipt.json",
        {
            "state": "CORRECTION_CONTENT_BUILT_NOT_COMMITTED",
            "built_at": now(),
            "failed_final": FAILED_FINAL,
            "expected_corrected_parent": FAILED_FINAL,
            "canonical_failure_receipt_sha256": FAILURE_RECEIPT_SHA256,
            "canonical_success_credit": 0,
            "canonical_replay": False,
            "delivery_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    current = owner_files()
    delta_prefixes = ("docs/neris-solane/v667-v8-r3/correction/",)
    delta_exact = {
        "docs/neris-solane/v667-v8-r3/handoffs/vesper-arlen-v668-v1-correction-overlay.md",
        "docs/neris-solane/v667-v8-r3/route/vesper-arlen-v668-v1-correction-route.json",
        "scripts/build_ghc_family_neris_solane_v667_v8_r3_correction.py",
        "scripts/ghc_family_neris_solane_v667_v8_r3_canonical_dependency_recovery.py",
        "tests/test_ghc_family_neris_solane_v667_v8_r3_correction.py",
    }
    delta_paths = [path for path in current if path.relative_to(ROOT).as_posix().startswith(delta_prefixes) or path.relative_to(ROOT).as_posix() in delta_exact]
    write_json(
        "validation/correction-delta-manifest.json",
        {
            "scope": "additive correction files after failed canonical final",
            "failed_final": FAILED_FINAL,
            "entries": entries(delta_paths),
            "excluded_self_generated_metadata": [CORRECTION_DELTA_MANIFEST.relative_to(ROOT).as_posix(), CORRECTED_OWNER_MANIFEST.relative_to(ROOT).as_posix()],
        },
    )
    current = owner_files()
    write_json(
        "validation/corrected-owner-manifest.json",
        {
            "scope": "all owner files at corrected-final build",
            "entries": entries([path for path in current if path != CORRECTED_OWNER_MANIFEST]),
            "self_excluded": CORRECTED_OWNER_MANIFEST.relative_to(ROOT).as_posix(),
        },
    )
    return validate_tree()


def validate_tree() -> dict[str, Any]:
    anchor = json.loads((PHASE / "correction" / "canonical-failure-anchor.json").read_text(encoding="utf-8"))
    overlay = json.loads((PHASE / "correction" / "method-flow-external-overlay.json").read_text(encoding="utf-8"))
    route = json.loads((PHASE / "route" / "vesper-arlen-v668-v1-correction-route.json").read_text(encoding="utf-8"))
    if anchor["failure_receipt_sha256"] != FAILURE_RECEIPT_SHA256 or anchor["canonical_success_count"] != 0 or anchor["canonical_replayed"]:
        raise AssertionError("canonical failure anchor drift")
    if overlay["corrected_activation_overlay"] != {"effective_negatives": 28734, "methods": 15320, "open_gaps": 203, "exact_gates": 201, "failed_witnesses": 1035, "passing_witnesses": 1875}:
        raise AssertionError("external overlay drift")
    if route["delivery_state"] != "PREPARED_NOT_SENT" or route["successor_contacted"] or route["canonical_replay_allowed"]:
        raise AssertionError("correction route drift")
    delta_count = manifest_replay(CORRECTION_DELTA_MANIFEST)
    owner_count = manifest_replay(CORRECTED_OWNER_MANIFEST)
    current = owner_files()
    manifest_paths = {row["path"] for row in json.loads(CORRECTED_OWNER_MANIFEST.read_text(encoding="utf-8"))["entries"]}
    self_path = CORRECTED_OWNER_MANIFEST.relative_to(ROOT).as_posix()
    current_paths = {path.relative_to(ROOT).as_posix() for path in current}
    if manifest_paths != current_paths - {self_path}:
        raise AssertionError("corrected owner manifest completeness drift")
    privacy = privacy_candidates(current)
    if privacy:
        raise AssertionError(f"privacy candidates: {privacy[:3]}")
    head = git("rev-parse", "HEAD").stdout.strip()
    if head != FAILED_FINAL and git("rev-parse", "HEAD^").stdout.strip() != FAILED_FINAL:
        raise AssertionError("correction lifecycle head drift")
    json_count = 0
    for path in current:
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
            json_count += 1
    if len(current) >= FILE_CEILING:
        raise AssertionError("2,000-file guard reached")
    return {
        "state": "CORRECTION_CONTENT_PASS",
        "head_lifecycle": "failed_final_precommit" if head == FAILED_FINAL else "corrected_final_postcommit",
        "canonical_success_credit": 0,
        "canonical_replayed": False,
        "delta_manifest_entries": delta_count,
        "owner_manifest_entries": owner_count,
        "owner_files": len(current),
        "json_parses": json_count,
        "privacy_candidates": 0,
        "delivery_state": route["delivery_state"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    payload = validate_tree() if args.validate else build()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
