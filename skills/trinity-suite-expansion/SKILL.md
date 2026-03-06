---
name: trinity-suite-expansion
description: Integrate new deterministic systems into `scripts/run_all_trinity_systems.py` and `scripts/trinity_mandala_scoreboard.py` without making the standard suite depend on live network access. Use when Codex needs to extend suite stages, flags, status outputs, or scoreboard artifact wiring for new Trinity subsystems.
---

# Trinity Suite Expansion

Use this skill when the suite or scoreboard needs new systems.

## Rules

1. Keep standard and deep runs offline-safe by default.
2. Put live refresh steps behind an explicit include flag.
3. Run cached validators and boards before the mandala scoreboard.
4. Let stale caches surface as `WARN`, but keep missing or malformed artifacts as `FAIL`.
