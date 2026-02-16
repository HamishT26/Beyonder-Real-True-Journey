"""
freed_id_audit_log.py
---------------------

Append-only audit ledger helper for Freed ID governance controls.

This module stores newline-delimited JSON events and links them using a simple
hash chain:
  entry_hash = sha256(prev_hash + canonical_entry_json)

The chain gives tamper-evidence suitable for local governance verification.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Tuple

ZERO_HASH = "0" * 64


def _canonical_json(payload: Dict[str, object]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _hash(prev_hash: str, payload: Dict[str, object]) -> str:
    raw = f"{prev_hash}{_canonical_json(payload)}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


@dataclass
class AuditAppendResult:
    index: int
    prev_hash: str
    entry_hash: str


class FreedIDAuditLedger:
    """Append-only JSONL ledger with hash-chain integrity checks."""

    def __init__(self, ledger_path: str | Path) -> None:
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)

    def iter_entries(self) -> Iterable[Dict[str, object]]:
        if not self.ledger_path.exists():
            return []
        entries = []
        with self.ledger_path.open("r", encoding="utf-8") as handle:
            for raw in handle:
                line = raw.strip()
                if not line:
                    continue
                entries.append(json.loads(line))
        return entries

    def append(self, action: str, did: str, details: Dict[str, object] | None = None) -> AuditAppendResult:
        entries = list(self.iter_entries())
        prev_hash = ZERO_HASH if not entries else str(entries[-1].get("entry_hash", ZERO_HASH))
        idx = len(entries)

        payload: Dict[str, object] = {
            "index": idx,
            "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "action": action,
            "did": did,
            "details": details or {},
        }
        entry_hash = _hash(prev_hash, payload)
        payload["prev_hash"] = prev_hash
        payload["entry_hash"] = entry_hash

        with self.ledger_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, sort_keys=True) + "\n")

        return AuditAppendResult(index=idx, prev_hash=prev_hash, entry_hash=entry_hash)

    def verify_integrity(self) -> Tuple[bool, str]:
        entries = list(self.iter_entries())
        prev_hash = ZERO_HASH
        for idx, entry in enumerate(entries):
            try:
                expected_prev = str(entry["prev_hash"])
                provided_hash = str(entry["entry_hash"])
                payload = {
                    "index": entry["index"],
                    "timestamp_utc": entry["timestamp_utc"],
                    "action": entry["action"],
                    "did": entry["did"],
                    "details": entry.get("details", {}),
                }
            except KeyError as exc:
                return False, f"missing_required_field_at_index={idx}:{exc}"

            if expected_prev != prev_hash:
                return False, f"prev_hash_mismatch_at_index={idx}"

            computed = _hash(prev_hash, payload)
            if provided_hash != computed:
                return False, f"entry_hash_mismatch_at_index={idx}"

            prev_hash = provided_hash
        return True, f"entries_verified={len(entries)}"
