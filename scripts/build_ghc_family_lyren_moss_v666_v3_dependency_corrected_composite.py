#!/usr/bin/env python3
"""One-shot dependency-corrected composite after the retained failed canonical.

This is deliberately not a canonical retry and can never create canonical
success credit.  It reuses the corrected read-only payload checks only after
the import-path dependency is fixed in a new exact final.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from build_ghc_family_lyren_moss_v666_v3_canonical_completion import canonical_payload


FAILED_CANONICAL_FINAL = "7bb3e0e266242ba04927bcdf8d20dd0e4f875df1"
FAILED_CANONICAL_RECEIPT_SHA256 = "50ff0f90a967a9be82b282695085056e6afca4d96627473636db9831090d928d"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--receipt-dir", required=True)
    args = parser.parse_args()
    receipt_dir = Path(args.receipt_dir).resolve()
    receipt_dir.mkdir(parents=True, exist_ok=True)
    failed_receipt = receipt_dir / f"canonical-completion-{FAILED_CANONICAL_FINAL}.json"
    if not failed_receipt.exists():
        raise SystemExit("retained failed canonical receipt is missing")
    if hashlib.sha256(failed_receipt.read_bytes()).hexdigest() != FAILED_CANONICAL_RECEIPT_SHA256:
        raise SystemExit("retained failed canonical receipt hash mismatch")
    state_path = receipt_dir / f"dependency-corrected-composite-state-{args.expected_final}.json"
    receipt_path = receipt_dir / f"dependency-corrected-composite-{args.expected_final}.json"
    if state_path.exists() or receipt_path.exists():
        raise SystemExit("dependency-corrected composite invocation already recorded; replay refused")
    state = {
        "schema": "ghc.family.lyren-moss.v666-v3.dependency-corrected-composite-state.v1",
        "owner": "Lyren Moss",
        "phase": "v666-v3",
        "expected_final": args.expected_final,
        "invocation_count": 1,
        "success_count": 0,
        "canonical_invocation_count": 1,
        "canonical_success_count": 0,
        "canonical_replay": False,
        "status": "invoked",
        "invoked_at_utc": now(),
    }
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    try:
        payload = canonical_payload(args.expected_final)
        success = payload["tests"]["successful"] and all(payload["detailed_checks"].values()) and all(payload["minimal_checks"].values())
        canonical_bytes = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        receipt = {
            "schema": "ghc.family.lyren-moss.v666-v3.dependency-corrected-composite-receipt.v1",
            "owner": "Lyren Moss",
            "phase": "v666-v3",
            "generated_at_utc": now(),
            "invocation_count": 1,
            "success_count": 1 if success else 0,
            "success": success,
            "canonical_invocation_count": 1,
            "canonical_success_count": 0,
            "canonical_replay": False,
            "canonical_credit": 0,
            "failed_canonical_final": FAILED_CANONICAL_FINAL,
            "failed_canonical_receipt_sha256": FAILED_CANONICAL_RECEIPT_SHA256,
            "dependency_correction": "insert the repository root into sys.path before importing test modules",
            "composite_payload_sha256": hashlib.sha256(canonical_bytes).hexdigest(),
            "payload": payload,
        }
    except Exception as exc:
        receipt = {
            "schema": "ghc.family.lyren-moss.v666-v3.dependency-corrected-composite-receipt.v1",
            "owner": "Lyren Moss",
            "phase": "v666-v3",
            "generated_at_utc": now(),
            "invocation_count": 1,
            "success_count": 0,
            "success": False,
            "canonical_invocation_count": 1,
            "canonical_success_count": 0,
            "canonical_replay": False,
            "canonical_credit": 0,
            "failed_canonical_final": FAILED_CANONICAL_FINAL,
            "failed_canonical_receipt_sha256": FAILED_CANONICAL_RECEIPT_SHA256,
            "exception": {"type": type(exc).__name__, "message": str(exc)},
        }
    receipt_text = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    receipt_path.write_text(receipt_text, encoding="utf-8", newline="\n")
    state.update({
        "success_count": 1 if receipt["success"] else 0,
        "status": "success" if receipt["success"] else "failed",
        "completed_at_utc": now(),
        "receipt_sha256": hashlib.sha256(receipt_text.encode("utf-8")).hexdigest(),
    })
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    payload = receipt.get("payload", {})
    print(json.dumps({
        "success": receipt["success"],
        "canonical_success_count": 0,
        "canonical_replay": False,
        "receipt_sha256": state["receipt_sha256"],
        "composite_payload_sha256": receipt.get("composite_payload_sha256"),
        "selected_tests": payload.get("tests", {}).get("selected_count"),
        "detailed": [payload.get("detailed_passed"), payload.get("detailed_total")],
        "minimal": [payload.get("minimal_passed"), payload.get("minimal_total")],
        "manifest_entries": payload.get("manifest_entry_total"),
        "json_parsed": payload.get("json", {}).get("parsed"),
        "privacy_files": payload.get("privacy", {}).get("files"),
        "security_python_files": payload.get("security", {}).get("python_files"),
    }, sort_keys=True))
    if not receipt["success"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
