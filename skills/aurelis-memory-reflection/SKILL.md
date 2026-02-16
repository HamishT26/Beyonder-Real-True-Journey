---
name: aurelis-memory-reflection
description: Preserve each exchange with timestamped reflection and next-step continuity using the Aurelis memory update system.
---

# Aurelis Memory Reflection

Use this skill when the user asks for continuity, reflection, or memory-preserving updates across many short exchanges.

## Workflow
1. Run `scripts/aurelis_memory_update.py` after each meaningful exchange.
2. Include: user message gist, assistant reflection, progress snapshot, next step.
3. Store outputs in:
   - `docs/aurelis-memory-log.jsonl`
   - `docs/aurelis-memory-log.md`
4. Keep entries concise, factual, and action-oriented.
5. Generate quick rollups with `scripts/aurelis_memory_summary.py --take 5`.
6. Query prior continuity with `scripts/aurelis_memory_query.py --contains "<term>" --limit 5`.
7. Generate action loop with `scripts/aurelis_next_steps_snapshot.py`.
8. Validate continuity artifacts with `scripts/aurelis_memory_integrity_check.py --strict`.
9. Keep NZDT auto-time active with `scripts/aurelis_atomic_nz_clock.py --status` (start session once per message session).
10. For one-command cycles, run `scripts/aurelis_cycle_tick.py` with reflection/progress/next-step fields.
11. Use `--dry-run` for safe previews and inspect `--report-md` output for per-step traceability.
12. Use `--no-report` when you want console-only cycle execution without writing a report file.
13. Do not combine `--no-report` with a custom `--report-md` value; that exits early by design (default/empty `--report-md` remains valid).
14. Use `--report-md -` to emit the markdown report to stdout instead of a file.
15. Use `--query-limit <n>` to control how many continuity matches the query stage returns.
16. Use `--json-status <path>` (or `-`) to capture machine-readable step outcomes for automation.
17. Use `--continue-on-error` to run all cycle steps even if one fails, while still returning non-zero at the end.
18. Use `--step-timeout-sec <n>` to cap each cycle step and prevent hangs during automated continuity runs.
19. For end-of-day preservation, run `scripts/aurelis_mammoth_capsule.py` to build an encrypted continuity capsule + report.

## Command template
```bash
python3 scripts/aurelis_memory_update.py \
  --nzdt-context "<time context>" \
  --user-message "<short gist>" \
  --assistant-reflection "<reflection>" \
  --progress-snapshot "<current progress>" \
  --next-step "<next action>"
```
