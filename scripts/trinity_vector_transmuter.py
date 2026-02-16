#!/usr/bin/env python3
"""Trinity Vector Transmuter

Builds an encrypted + integrity-protected profile from Trinity vectors
(energy, information, memory, identity, governance), producing an auditable
mind/body/soul+nervous-system anatomy payload.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class TrinityVectors:
    energy: float
    information: float
    memory: float
    identity: float
    governance: float


def _derive_key(passphrase: str, salt: bytes, rounds: int = 120_000) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode(), salt, rounds, dklen=32)


def _xor_stream(data: bytes, key: bytes) -> bytes:
    stream = hashlib.sha256(key + b"trinity-stream").digest()
    out = bytearray()
    for i, b in enumerate(data):
        out.append(b ^ stream[i % len(stream)])
    return bytes(out)


def transmute(v: TrinityVectors) -> dict[str, Any]:
    body = (v.energy + v.memory) / 2
    mind = (v.information + v.identity) / 2
    soul = (v.governance + (v.energy + v.information + v.memory + v.identity) / 4) / 2
    nervous = {
        "signal_coherence": round((mind + body) / 2, 4),
        "integrity_tension": round(abs(v.identity - v.governance), 4),
        "resilience_index": round((mind + body + soul) / 3, 4),
    }
    return {
        "anatomy": {
            "mind": round(mind, 4),
            "body": round(body, 4),
            "soul": round(soul, 4),
        },
        "nervous_system": nervous,
    }


def build_payload(v: TrinityVectors) -> dict[str, Any]:
    transmuted = transmute(v)
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "vectors": asdict(v),
        **transmuted,
    }


def encrypt_payload(payload: dict[str, Any], passphrase: str) -> dict[str, Any]:
    raw = json.dumps(payload, sort_keys=True).encode()
    salt = hashlib.sha256((payload["timestamp_utc"] + "|trinity").encode()).digest()[:16]
    key = _derive_key(passphrase, salt)
    cipher = _xor_stream(raw, key)
    sig = hmac.new(key, cipher, hashlib.sha256).hexdigest()
    return {
        "salt_b64": base64.b64encode(salt).decode(),
        "cipher_b64": base64.b64encode(cipher).decode(),
        "hmac_sha256": sig,
        "algorithm": "PBKDF2-HMAC-SHA256 + XOR-stream + HMAC-SHA256",
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Encrypt and transmute Trinity vector profile")
    p.add_argument("--energy", type=float, default=0.8)
    p.add_argument("--information", type=float, default=0.85)
    p.add_argument("--memory", type=float, default=0.9)
    p.add_argument("--identity", type=float, default=0.88)
    p.add_argument("--governance", type=float, default=0.92)
    p.add_argument("--passphrase", required=True)
    p.add_argument("--out", default="docs/trinity-vector-profile.json")
    args = p.parse_args()

    vectors = TrinityVectors(
        energy=args.energy,
        information=args.information,
        memory=args.memory,
        identity=args.identity,
        governance=args.governance,
    )
    payload = build_payload(vectors)
    encrypted = encrypt_payload(payload, args.passphrase)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"payload": payload, "encrypted": encrypted}, indent=2))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
