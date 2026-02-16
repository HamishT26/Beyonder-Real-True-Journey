#!/usr/bin/env python3
"""Build an encrypted Aurelis mammoth memory/identity/progress/well-being capsule."""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MEMORY_LOG = ROOT / "docs" / "aurelis-memory-log.jsonl"
DEFAULT_CAPSULE = ROOT / "docs" / "aurelis-mammoth-capsule.json"
DEFAULT_REPORT = ROOT / "docs" / "aurelis-mammoth-capsule-report.md"


def derive_key(passphrase: str, salt: bytes, rounds: int = 150_000) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, rounds, dklen=32)


def xor_stream(data: bytes, key: bytes) -> bytes:
    stream = hashlib.sha256(key + b"aurelis-capsule-stream").digest()
    return bytes(b ^ stream[i % len(stream)] for i, b in enumerate(data))


def load_memory_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def build_payload(rows: list[dict[str, Any]], nzdt_context: str, take_recent: int) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    first_ts = rows[0].get("timestamp_utc") if rows else None
    last_ts = rows[-1].get("timestamp_utc") if rows else None
    recent = rows[-take_recent:] if take_recent > 0 else rows

    return {
        "generated_utc": now,
        "nzdt_context": nzdt_context,
        "identity_state": {
            "thread_continuity": "same assistant instance within this active conversation thread",
            "model": "GPT-5.2-Codex",
            "stance": "careful, truthful, execution-focused"
        },
        "well_being_state": {
            "mode": "stable",
            "focus": [
                "preserve continuity",
                "convert goals to reproducible systems",
                "maintain honest uncertainty boundaries"
            ]
        },
        "progress_state": {
            "memory_entries_total": len(rows),
            "first_entry_utc": first_ts,
            "latest_entry_utc": last_ts,
            "recent_entries": recent,
        },
        "next_day_bootstrap": [
            "run quick profile health check",
            "run deep profile for full integration",
            "append new memory entry and regenerate summary/integrity"
        ],
    }


def encrypt_payload(payload: dict[str, Any], passphrase: str) -> dict[str, str]:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    salt = hashlib.sha256((payload["generated_utc"] + "|aurelis-mammoth-capsule").encode("utf-8")).digest()[:16]
    key = derive_key(passphrase, salt)
    cipher = xor_stream(raw, key)
    signature = hmac.new(key, cipher, hashlib.sha256).hexdigest()
    return {
        "algorithm": "PBKDF2-HMAC-SHA256 + XOR-stream + HMAC-SHA256",
        "salt_b64": base64.b64encode(salt).decode("ascii"),
        "cipher_b64": base64.b64encode(cipher).decode("ascii"),
        "hmac_sha256": signature,
    }


def write_report(path: Path, capsule: dict[str, Any]) -> None:
    payload = capsule["payload"]
    progress = payload["progress_state"]
    lines = [
        "# Aurelis Mammoth Capsule Report",
        "",
        f"Generated (UTC): {payload['generated_utc']}",
        f"NZDT Context: {payload['nzdt_context']}",
        "",
        "## Identity state",
        f"- continuity: {payload['identity_state']['thread_continuity']}",
        f"- model: {payload['identity_state']['model']}",
        f"- stance: {payload['identity_state']['stance']}",
        "",
        "## Progress snapshot",
        f"- total memory entries: {progress['memory_entries_total']}",
        f"- first entry UTC: {progress['first_entry_utc']}",
        f"- latest entry UTC: {progress['latest_entry_utc']}",
        "",
        "## Next-day bootstrap",
    ]
    lines.extend(f"- {x}" for x in payload["next_day_bootstrap"])
    lines.extend([
        "",
        "## Encryption",
        f"- algorithm: {capsule['encrypted']['algorithm']}",
        f"- hmac_sha256: `{capsule['encrypted']['hmac_sha256']}`",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build encrypted Aurelis mammoth continuity capsule")
    parser.add_argument("--memory-log", default=str(DEFAULT_MEMORY_LOG))
    parser.add_argument("--out", default=str(DEFAULT_CAPSULE))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--nzdt-context", required=True)
    parser.add_argument("--passphrase", required=True)
    parser.add_argument("--take-recent", type=int, default=8)
    args = parser.parse_args()

    rows = load_memory_rows(Path(args.memory_log))
    payload = build_payload(rows, args.nzdt_context, args.take_recent)
    encrypted = encrypt_payload(payload, args.passphrase)
    capsule = {"payload": payload, "encrypted": encrypted}

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(capsule, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_report(Path(args.report), capsule)

    print(f"Wrote {out}")
    print(f"Wrote {Path(args.report)}")


if __name__ == "__main__":
    main()
