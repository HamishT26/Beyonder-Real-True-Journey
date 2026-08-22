#!/usr/bin/env python3
"""Auren Lark v666-v5 closeout bounded runner."""

from __future__ import annotations

import sys

from ghc_family_auren_lark_v666_v5_runtime import emit, runner_payload


if __name__ == "__main__":
    payload = runner_payload("closeout", probe=sys.argv[1:] == ["--probe"])
    emit(payload)
    raise SystemExit(0 if payload.get("valid") else 1)
