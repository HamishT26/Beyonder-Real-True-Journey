#!/usr/bin/env python3
"""Trinity expansion system wrapper: postgres_materialization_surface_audit."""

from trinity_expansion_system_runner import run_named_system


if __name__ == "__main__":
    raise SystemExit(run_named_system("postgres_materialization_surface_audit"))
