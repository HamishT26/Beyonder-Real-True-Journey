#!/usr/bin/env python3
"""Network-free Git LFS pointer and materialization boundary classifier."""

from __future__ import annotations

import re
from pathlib import PurePosixPath
from typing import Any


VERSION = "https://git-lfs.github.com/spec/v1"
OID_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")
SIZE_RE = re.compile(r"(?:0|[1-9][0-9]*)\Z")


def _contained(path: str) -> bool:
    item = PurePosixPath(path.replace("\\", "/"))
    return not item.is_absolute() and ".." not in item.parts and bool(item.parts)


def classify_bytes(*, path: str, data: bytes, object_present: bool | None = None) -> dict[str, Any]:
    """Classify bytes without fetching or traversing outside the supplied path."""
    if not _contained(path):
        return {"classification": "rejected_out_of_root", "accepted": False, "network_fetch_performed": False}
    if len(data) > 4096:
        return {"classification": "materialized_or_ordinary_content", "accepted": True, "network_fetch_performed": False}
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return {"classification": "materialized_or_ordinary_content", "accepted": True, "network_fetch_performed": False}
    lines = text.rstrip("\n").split("\n")
    if not lines or lines[0] != f"version {VERSION}":
        if any(line.startswith(("version ", "oid ", "size ")) for line in lines):
            return {"classification": "malformed_lfs_pointer", "accepted": False, "network_fetch_performed": False}
        return {"classification": "ordinary_tracked_content", "accepted": True, "network_fetch_performed": False}
    if len(lines) < 3 or not lines[1].startswith("oid ") or not lines[2].startswith("size "):
        return {"classification": "malformed_lfs_pointer", "accepted": False, "network_fetch_performed": False}
    oid = lines[1][4:]
    size = lines[2][5:]
    extensions_valid = all(line.startswith("ext-") and " " in line for line in lines[3:])
    if not OID_RE.fullmatch(oid) or not SIZE_RE.fullmatch(size) or not extensions_valid:
        return {"classification": "malformed_lfs_pointer", "accepted": False, "network_fetch_performed": False}
    present = bool(object_present)
    return {
        "classification": "valid_lfs_pointer_object_present" if present else "valid_lfs_pointer_object_missing",
        "accepted": present,
        "oid": oid,
        "declared_size": int(size),
        "object_present": present,
        "network_fetch_performed": False,
    }
