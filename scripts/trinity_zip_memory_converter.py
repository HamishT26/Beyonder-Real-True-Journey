#!/usr/bin/env python3
"""Trinity Hybrid OS Zipfile Converter.

Creates compact zip snapshots for memory/data artifacts and can extract them
back into full form for reflection and recovery workflows.
Supports optional encryption-at-rest and retention pruning.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import secrets
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ARCHIVE_DIR = ROOT / "docs" / "memory-archives"
DEFAULT_INDEX = DEFAULT_ARCHIVE_DIR / "index.jsonl"

DEFAULT_SOURCES = [
    "docs/aurelis-memory-log.jsonl",
    "docs/aurelis-memory-log.md",
    "docs/aurelis-memory-latest-summary.md",
    "docs/aurelis-next-steps.md",
    "docs/aurelis-memory-integrity-report.md",
    "docs/system-suite-status.json",
    "docs/system-suite-run-report.md",
    "docs/trinity-vector-profile.json",
    "docs/qcit-coordination-report.json",
    "docs/quantum-energy-transmutation-report.json",
    "docs/aurelis-mammoth-capsule.json",
    "docs/aurelis-mammoth-capsule-report.md",
    "docs/token-credit-bank-report.json",
    "docs/token-credit-bank-ledger.jsonl",
    "docs/energy-bank-report.json",
    "docs/energy-bank-state.json",
    "docs/gyroscopic-hybrid-zip-report.json",
    "docs/trinity-background-os-status.json",
    "docs/cache-waste-regenerator-report.json",
]


def _resolve_repo_relative(path_str: str) -> Path:
    p = (ROOT / path_str).resolve()
    p.relative_to(ROOT)
    return p


def _read_index(index_path: Path) -> list[dict[str, Any]]:
    if not index_path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _write_index(index_path: Path, rows: list[dict[str, Any]]) -> None:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _derive_key(passphrase: str, salt: bytes, rounds: int = 210_000) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, rounds, dklen=32)


def _stream_xor(data: bytes, key: bytes, nonce: bytes) -> bytes:
    out = bytearray(len(data))
    counter = 0
    offset = 0
    while offset < len(data):
        block = hmac.new(key, nonce + counter.to_bytes(8, "big"), hashlib.sha256).digest()
        chunk = data[offset : offset + len(block)]
        out[offset : offset + len(chunk)] = bytes(a ^ b for a, b in zip(chunk, block))
        counter += 1
        offset += len(chunk)
    return bytes(out)


def _encrypt_bytes(data: bytes, passphrase: str, context: str) -> dict[str, str]:
    rounds = 210_000
    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(16)
    key = _derive_key(passphrase, salt, rounds=rounds)
    cipher = _stream_xor(data, key, nonce)
    sig = hmac.new(key, nonce + cipher, hashlib.sha256).hexdigest()
    return {
        "algorithm": "PBKDF2-HMAC-SHA256 + HMAC-CTR-XOR + HMAC-SHA256",
        "kdf_rounds": rounds,
        "context_hint": context,
        "salt_b64": base64.b64encode(salt).decode("ascii"),
        "nonce_b64": base64.b64encode(nonce).decode("ascii"),
        "cipher_b64": base64.b64encode(cipher).decode("ascii"),
        "hmac_sha256": sig,
    }


def _decrypt_bytes(blob: dict[str, str], passphrase: str) -> bytes:
    salt = base64.b64decode(blob["salt_b64"])
    cipher = base64.b64decode(blob["cipher_b64"])
    rounds = int(blob.get("kdf_rounds", 120_000))
    key = _derive_key(passphrase, salt, rounds=rounds)

    nonce_b64 = blob.get("nonce_b64")
    if nonce_b64:
        nonce = base64.b64decode(nonce_b64)
        calc = hmac.new(key, nonce + cipher, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(calc, str(blob.get("hmac_sha256", ""))):
            raise SystemExit("archive decryption failed: HMAC mismatch (wrong passphrase or tampered archive)")
        return _stream_xor(cipher, key, nonce)

    # Backward compatibility with legacy deterministic format.
    calc = hmac.new(key, cipher, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calc, str(blob.get("hmac_sha256", ""))):
        raise SystemExit("archive decryption failed: HMAC mismatch (wrong passphrase or tampered archive)")
    legacy_stream = hashlib.sha256(key + b"trinity-zip-memory-stream").digest()
    return bytes(b ^ legacy_stream[i % len(legacy_stream)] for i, b in enumerate(cipher))


def _build_plain_zip(out_path: Path, label: str, sources: list[str]) -> tuple[list[str], dict[str, Any]]:
    packed: list[str] = []
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "label": label,
        "files": [],
    }
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for source in sources:
            src = _resolve_repo_relative(source)
            if not src.exists() or not src.is_file():
                continue
            rel = src.relative_to(ROOT).as_posix()
            zf.write(src, arcname=rel)
            packed.append(rel)
            manifest["files"].append(rel)
        zf.writestr("manifest.json", json.dumps(manifest, indent=2) + "\n")
    return packed, manifest


def archive(
    label: str,
    sources: list[str],
    archive_dir: Path,
    index_path: Path,
    encrypt_passphrase: str = "",
) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_label = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in label).strip("-") or "snapshot"
    plain_ext = ".ezip" if encrypt_passphrase else ".zip"
    out_path = archive_dir / f"{timestamp}-{safe_label}{plain_ext}"

    archive_dir.mkdir(parents=True, exist_ok=True)

    with TemporaryDirectory() as td:
        temp_zip = Path(td) / "bundle.zip"
        packed, manifest = _build_plain_zip(temp_zip, label, sources)

        if encrypt_passphrase:
            encrypted = _encrypt_bytes(temp_zip.read_bytes(), encrypt_passphrase, context=f"{timestamp}|{label}")
            wrapped = {
                "generated_utc": datetime.now(timezone.utc).isoformat(),
                "label": label,
                "encrypted": encrypted,
            }
            out_path.write_text(json.dumps(wrapped, indent=2) + "\n", encoding="utf-8")
            encrypted_at_rest = True
        else:
            out_path.write_bytes(temp_zip.read_bytes())
            encrypted_at_rest = False

    index_rows = _read_index(index_path)
    index_rows.append(
        {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "label": label,
            "archive": out_path.relative_to(ROOT).as_posix(),
            "file_count": len(packed),
            "files": packed,
            "encrypted_at_rest": encrypted_at_rest,
            "archive_format": "json-ezip" if encrypted_at_rest else "zip",
            "manifest_generated_utc": manifest["generated_utc"],
        }
    )
    _write_index(index_path, index_rows)
    return out_path


def extract(archive_path: str, dest: str, decrypt_passphrase: str = "") -> Path:
    archive = _resolve_repo_relative(archive_path)
    dest_path = _resolve_repo_relative(dest)
    dest_path.mkdir(parents=True, exist_ok=True)

    suffix = archive.suffix.lower()
    if suffix == ".zip":
        with zipfile.ZipFile(archive, "r") as zf:
            zf.extractall(dest_path)
        return dest_path

    if suffix == ".ezip":
        if not decrypt_passphrase:
            raise SystemExit("encrypted archive requires --decrypt-passphrase")
        wrapped = json.loads(archive.read_text(encoding="utf-8"))
        blob = wrapped.get("encrypted")
        if not isinstance(blob, dict):
            raise SystemExit("invalid encrypted archive format")
        raw_zip = _decrypt_bytes(blob, decrypt_passphrase)
        with TemporaryDirectory() as td:
            temp_zip = Path(td) / "bundle.zip"
            temp_zip.write_bytes(raw_zip)
            with zipfile.ZipFile(temp_zip, "r") as zf:
                zf.extractall(dest_path)
        return dest_path

    raise SystemExit(f"unsupported archive extension: {archive.suffix}")


def list_archives(index_path: Path, limit: int, label_contains: str) -> list[dict[str, Any]]:
    rows = _read_index(index_path)
    if label_contains:
        needle = label_contains.lower()
        rows = [r for r in rows if needle in str(r.get("label", "")).lower()]
    if limit > 0:
        rows = rows[-limit:]
    return rows


def recall(
    index_path: Path,
    label_contains: str,
    latest: bool,
    dest: str,
    decrypt_passphrase: str,
) -> tuple[dict[str, Any], Path]:
    rows = _read_index(index_path)
    if label_contains:
        needle = label_contains.lower()
        rows = [r for r in rows if needle in str(r.get("label", "")).lower()]
    if not rows:
        raise SystemExit("no matching archives found in index")

    selected = rows[-1] if latest else rows[0]
    archive_path = selected.get("archive")
    if not archive_path:
        raise SystemExit("selected index row missing archive path")

    out = extract(archive_path, dest, decrypt_passphrase=decrypt_passphrase)
    return selected, out


def prune(index_path: Path, keep_last: int, label_contains: str, delete_files: bool) -> dict[str, int]:
    if keep_last < 0:
        raise SystemExit("--keep-last must be >= 0")

    rows = _read_index(index_path)
    if not rows:
        return {"kept": 0, "removed": 0, "deleted_files": 0}

    scoped = rows
    if label_contains:
        needle = label_contains.lower()
        scoped = [r for r in rows if needle in str(r.get("label", "")).lower()]

    keep_set = set(id(r) for r in (scoped[-keep_last:] if keep_last > 0 else []))
    kept_rows: list[dict[str, Any]] = []
    removed_rows: list[dict[str, Any]] = []

    for row in rows:
        if row in scoped and id(row) not in keep_set:
            removed_rows.append(row)
        else:
            kept_rows.append(row)

    deleted_files = 0
    if delete_files:
        for row in removed_rows:
            archive_rel = row.get("archive")
            if isinstance(archive_rel, str):
                try:
                    archive_path = _resolve_repo_relative(archive_rel)
                except Exception:
                    continue
                if archive_path.exists() and archive_path.is_file():
                    archive_path.unlink()
                    deleted_files += 1

    _write_index(index_path, kept_rows)
    return {"kept": len(kept_rows), "removed": len(removed_rows), "deleted_files": deleted_files}


def main() -> None:
    parser = argparse.ArgumentParser(description="Trinity Hybrid OS zip memory converter")
    sub = parser.add_subparsers(dest="command", required=True)

    p_archive = sub.add_parser("archive", help="Create compressed snapshot archive")
    p_archive.add_argument("--label", default="memory-cycle")
    p_archive.add_argument("--source", action="append", default=[], help="Repo-relative source file (repeatable)")
    p_archive.add_argument("--archive-dir", default=str(DEFAULT_ARCHIVE_DIR.relative_to(ROOT)))
    p_archive.add_argument("--index", default=str(DEFAULT_INDEX.relative_to(ROOT)))
    p_archive.add_argument("--encrypt-passphrase", default="", help="Optional passphrase for encryption-at-rest")

    p_extract = sub.add_parser("extract", help="Extract an archive back to files")
    p_extract.add_argument("--archive", required=True, help="Repo-relative archive path")
    p_extract.add_argument("--dest", default="docs/memory-archives/extracted")
    p_extract.add_argument("--decrypt-passphrase", default="", help="Passphrase for encrypted archives")

    p_list = sub.add_parser("list", help="List indexed archives")
    p_list.add_argument("--index", default=str(DEFAULT_INDEX.relative_to(ROOT)))
    p_list.add_argument("--limit", type=int, default=10)
    p_list.add_argument("--label-contains", default="")

    p_recall = sub.add_parser("recall", help="Select from index and extract by label/latest")
    p_recall.add_argument("--index", default=str(DEFAULT_INDEX.relative_to(ROOT)))
    p_recall.add_argument("--label-contains", default="")
    p_recall.add_argument("--latest", action="store_true", help="Recall latest matching archive (default first match)")
    p_recall.add_argument("--dest", default="docs/memory-archives/recalled")
    p_recall.add_argument("--decrypt-passphrase", default="", help="Passphrase for encrypted archives")

    p_prune = sub.add_parser("prune", help="Prune old archive index entries")
    p_prune.add_argument("--index", default=str(DEFAULT_INDEX.relative_to(ROOT)))
    p_prune.add_argument("--keep-last", type=int, default=200)
    p_prune.add_argument("--label-contains", default="")
    p_prune.add_argument("--delete-files", action="store_true", help="Also delete archived files removed by prune")

    args = parser.parse_args()

    if args.command == "archive":
        sources = args.source or DEFAULT_SOURCES
        out_path = archive(
            label=args.label,
            sources=sources,
            archive_dir=_resolve_repo_relative(args.archive_dir),
            index_path=_resolve_repo_relative(args.index),
            encrypt_passphrase=args.encrypt_passphrase,
        )
        print(f"Wrote {out_path}")
        return

    if args.command == "extract":
        out = extract(args.archive, args.dest, decrypt_passphrase=args.decrypt_passphrase)
        print(f"Extracted to {out}")
        return

    if args.command == "list":
        rows = list_archives(
            index_path=_resolve_repo_relative(args.index),
            limit=args.limit,
            label_contains=args.label_contains,
        )
        for row in rows:
            print(json.dumps(row, ensure_ascii=False))
        return

    if args.command == "recall":
        row, out = recall(
            index_path=_resolve_repo_relative(args.index),
            label_contains=args.label_contains,
            latest=args.latest,
            dest=args.dest,
            decrypt_passphrase=args.decrypt_passphrase,
        )
        print(f"Recalled {row.get('archive')} -> {out}")
        return

    if args.command == "prune":
        result = prune(
            index_path=_resolve_repo_relative(args.index),
            keep_last=args.keep_last,
            label_contains=args.label_contains,
            delete_files=args.delete_files,
        )
        print(json.dumps(result))


if __name__ == "__main__":
    main()
