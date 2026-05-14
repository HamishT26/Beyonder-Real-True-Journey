# v241-v260 Live Write Action Pack

Purpose: turn queued council prompts into real CLI responses while remote-control QR remains postponed.

Required surfaces:
- Codex CLI for Arby and Aster Vale, run with `--sandbox read-only` and plugins disabled.
- Kimi CLI for Kimi, run as a one-step bounded print response because no read-only Kimi flag is exposed in current help.
- Local multiplex TUI: `docs/trinity-live-traces/v241-v260-multiplex-council-multiplex-tui.ps1`.
- Stop file: create `docs/trinity-live-traces/v241-v260-multiplex-council.stop` to halt the runner before the next turn.

Safety boundaries:
- No commits.
- No provider mutations.
- No remote-control QR tokens stored.
- No dashboard dependency.
- Each response is counted only when its response file exists.

Run modes:
- Full run: `python scripts/trinity_v241_v260_exchange_runner.py --start-turn 2 --end-turn 50 --lanes arby,kimi,aster_vale`.
- Small batch: `python scripts/trinity_v241_v260_exchange_runner.py --start-turn 2 --end-turn 5 --lanes arby,kimi,aster_vale`.
