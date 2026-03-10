#!/usr/bin/env python3
"""Wrapper for postgres_local_runtime_surface_audit. """

from __future__ import annotations

from trinity_expansion_system_runner import run_named_system


if __name__ == '__main__':
    raise SystemExit(run_named_system("postgres_local_runtime_surface_audit"))

