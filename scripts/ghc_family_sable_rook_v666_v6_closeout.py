#!/usr/bin/env python3
"""Sable Rook v666-v6 closeout bounded runner."""

from __future__ import annotations

import sys

from ghc_family_sable_rook_v666_v6_runtime import emit, runner_payload


if __name__ == "__main__":
    payload = runner_payload("closeout", probe=sys.argv[1:] == ["--probe"])
    emit(payload)
    raise SystemExit(0 if payload.get("valid") else 1)
