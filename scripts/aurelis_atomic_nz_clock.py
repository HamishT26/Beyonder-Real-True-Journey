#!/usr/bin/env python3
"""Aurelis Atomic NZ Clock System.

Maintains a session-aware NZDT clock record for continuity cycles.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "docs" / "aurelis-nz-clock-state.json"
SESSIONS_PATH = ROOT / "docs" / "aurelis-nz-clock-sessions.jsonl"

NZ = ZoneInfo("Pacific/Auckland")
FMT = "%Y-%m-%d %H:%M"


@dataclass
class ClockState:
    session_name: str
    session_start_nzdt: str
    session_start_utc: str
    last_updated_utc: str


def now_nz() -> datetime:
    return datetime.now(timezone.utc).astimezone(NZ)


def load_state() -> ClockState | None:
    if not STATE_PATH.exists():
        return None
    data = json.loads(STATE_PATH.read_text())
    return ClockState(**data)


def save_state(state: ClockState) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(asdict(state), indent=2))


def append_session_event(event: dict) -> None:
    SESSIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SESSIONS_PATH.open("a") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def elapsed_minutes(start_utc_iso: str) -> int:
    start = datetime.fromisoformat(start_utc_iso)
    now = datetime.now(timezone.utc)
    return int((now - start).total_seconds() // 60)


def cmd_start(session_name: str, start_nzdt: str) -> None:
    dt_nz = datetime.strptime(start_nzdt, FMT).replace(tzinfo=NZ)
    state = ClockState(
        session_name=session_name,
        session_start_nzdt=dt_nz.isoformat(),
        session_start_utc=dt_nz.astimezone(timezone.utc).isoformat(),
        last_updated_utc=datetime.now(timezone.utc).isoformat(),
    )
    save_state(state)
    append_session_event({
        "event": "session_start",
        "session_name": session_name,
        "start_nzdt": state.session_start_nzdt,
        "start_utc": state.session_start_utc,
        "recorded_utc": state.last_updated_utc,
    })
    print(f"Started session '{session_name}' at {state.session_start_nzdt}")


def cmd_status() -> None:
    state = load_state()
    if not state:
        print("No active clock session. Start one with --start-session and --start-nzdt.")
        return
    nz_now = now_nz().isoformat()
    mins = elapsed_minutes(state.session_start_utc)
    print(f"session_name={state.session_name}")
    print(f"session_start_nzdt={state.session_start_nzdt}")
    print(f"now_nzdt={nz_now}")
    print(f"elapsed_minutes={mins}")


def cmd_stamp() -> None:
    state = load_state()
    if not state:
        print(now_nz().strftime("%I:%M%p NZDT %a %d %b %Y"))
        return
    mins = elapsed_minutes(state.session_start_utc)
    print(f"{now_nz().strftime('%I:%M%p NZDT %a %d %b %Y')} | session={state.session_name} | +{mins}m")


def main() -> None:
    p = argparse.ArgumentParser(description="Aurelis Atomic NZ Clock")
    p.add_argument("--start-session", help="Session name to start/update")
    p.add_argument("--start-nzdt", help="Session start in 'YYYY-MM-DD HH:MM' NZDT")
    p.add_argument("--status", action="store_true", help="Print current session status")
    p.add_argument("--stamp", action="store_true", help="Print compact NZDT stamp")
    args = p.parse_args()

    if args.start_session or args.start_nzdt:
        if not (args.start_session and args.start_nzdt):
            raise SystemExit("--start-session and --start-nzdt must be supplied together")
        cmd_start(args.start_session, args.start_nzdt)
        return

    if args.status:
        cmd_status()
        return

    if args.stamp:
        cmd_stamp()
        return

    p.print_help()


if __name__ == "__main__":
    main()
