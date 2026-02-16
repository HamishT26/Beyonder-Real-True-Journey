#!/usr/bin/env python3
"""Trinity token/credit regeneration + zip snapshot converter.

Tracks token/credit usage and regeneration from QCIT + quantum reports, writes a
machine-readable report, and can trigger an indexed zip archive snapshot.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "docs" / "token-credit-bank-report.json"
DEFAULT_LEDGER = ROOT / "docs" / "token-credit-bank-ledger.jsonl"
DEFAULT_RESERVE_STATE = ROOT / "docs" / "energy-bank-state.json"


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _estimate_credits(tokens: float, tokens_per_credit: int) -> float:
    return round(tokens / max(1, tokens_per_credit), 6)


def _run_zip_snapshot(label: str) -> str:
    cmd = [
        "python3",
        "scripts/trinity_zip_memory_converter.py",
        "archive",
        "--label",
        label,
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return f"warn: zip snapshot failed ({proc.stderr.strip() or proc.stdout.strip()})"
    return proc.stdout.strip() or "ok"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Trinity token/credit zip converter")
    parser.add_argument("--tokens-used", type=int, default=12000)
    parser.add_argument("--credits-used", type=float, default=12.0)
    parser.add_argument("--tokens-per-credit", type=int, default=1000)
    parser.add_argument("--qcit", default="docs/qcit-coordination-report.json")
    parser.add_argument("--quantum", default="docs/quantum-energy-transmutation-report.json")
    parser.add_argument("--reserve-state", default=str(DEFAULT_RESERVE_STATE.relative_to(ROOT)))
    parser.add_argument("--use-reserve-first", action="store_true", default=True)
    parser.add_argument("--no-use-reserve-first", action="store_false", dest="use_reserve_first")
    parser.add_argument("--reserve-energy-per-token", type=float, default=0.001)
    parser.add_argument("--regeneration-multiplier", type=float, default=1.0, help="Scale regenerated outputs (e.g., 3.0 for 3x throughput)")
    parser.add_argument("--target-reimbursement-ratio", type=float, default=1.0, help="Minimum tokens-covered / tokens-used target (>=1.0 means full reimbursement or better)")
    parser.add_argument("--out", default=str(DEFAULT_OUT.relative_to(ROOT)))
    parser.add_argument("--ledger", default=str(DEFAULT_LEDGER.relative_to(ROOT)))
    parser.add_argument("--zip-snapshot", action="store_true", help="Create indexed zip snapshot after report write")
    parser.add_argument("--zip-label", default="token-credit-cycle")
    args = parser.parse_args()

    qcit = _load_json(ROOT / args.qcit)
    quantum = _load_json(ROOT / args.quantum)
    reserve = _load_json(ROOT / args.reserve_state)

    coordination_score = float(qcit.get("outputs", {}).get("coordination_score", 0.0))
    net_energy = float(quantum.get("outputs", {}).get("net_usable_energy", 0.0))

    reserve_tokens_available = float(reserve.get("reserve_tokens", 0.0))
    reserve_credits_available = float(reserve.get("reserve_credits", 0.0))
    reserve_energy_available = float(reserve.get("reserve_energy_units", 0.0))

    reserve_tokens_consumed = 0.0
    reserve_credits_consumed = 0.0
    reserve_energy_consumed = 0.0
    if args.use_reserve_first:
        reserve_tokens_consumed = min(float(args.tokens_used), reserve_tokens_available)
        reserve_credits_consumed = min(float(args.credits_used), reserve_credits_available)
        reserve_energy_consumed = min(
            reserve_energy_available,
            reserve_tokens_consumed * max(0.0, args.reserve_energy_per_token),
        )

    remaining_tokens_demand = max(0.0, float(args.tokens_used) - reserve_tokens_consumed)
    remaining_credits_demand = max(0.0, float(args.credits_used) - reserve_credits_consumed)

    base_tokens_regenerated = remaining_tokens_demand * (0.35 + 0.65 * coordination_score) + net_energy * 25
    multiplier = max(0.0, args.regeneration_multiplier)
    tokens_regenerated = round(base_tokens_regenerated * multiplier, 6)
    credits_regenerated = _estimate_credits(tokens_regenerated, args.tokens_per_credit)

    tokens_used_float = float(args.tokens_used)
    target_ratio = max(0.0, args.target_reimbursement_ratio)
    target_tokens_covered = target_ratio * tokens_used_float

    total_tokens_covered = reserve_tokens_consumed + tokens_regenerated
    topup_tokens = 0.0
    if total_tokens_covered < target_tokens_covered:
        topup_tokens = target_tokens_covered - total_tokens_covered
        tokens_regenerated = round(tokens_regenerated + topup_tokens, 6)
        credits_regenerated = _estimate_credits(tokens_regenerated, args.tokens_per_credit)
        total_tokens_covered = reserve_tokens_consumed + tokens_regenerated

    total_tokens_covered = round(total_tokens_covered, 6)
    total_credits_covered = round(reserve_credits_consumed + credits_regenerated, 6)
    token_delta = round(total_tokens_covered - tokens_used_float, 6)
    credit_delta = round(total_credits_covered - float(args.credits_used), 6)

    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "engine": "trinity-token-credit-zip-converter",
        "inputs": {
            "tokens_used": args.tokens_used,
            "credits_used": args.credits_used,
            "tokens_per_credit": args.tokens_per_credit,
            "coordination_score": coordination_score,
            "net_usable_energy": net_energy,
            "use_reserve_first": bool(args.use_reserve_first),
            "reserve_state": args.reserve_state,
            "regeneration_multiplier": multiplier,
            "target_reimbursement_ratio": target_ratio,
        },
        "outputs": {
            "reserve_tokens_available": round(reserve_tokens_available, 6),
            "reserve_credits_available": round(reserve_credits_available, 6),
            "reserve_energy_available": round(reserve_energy_available, 6),
            "reserve_tokens_consumed": round(reserve_tokens_consumed, 6),
            "reserve_credits_consumed": round(reserve_credits_consumed, 6),
            "reserve_energy_consumed": round(reserve_energy_consumed, 6),
            "remaining_tokens_demand": round(remaining_tokens_demand, 6),
            "remaining_credits_demand": round(remaining_credits_demand, 6),
            "tokens_regenerated": tokens_regenerated,
            "topup_tokens_for_target_ratio": round(topup_tokens, 6),
            "credits_regenerated": credits_regenerated,
            "total_tokens_covered": total_tokens_covered,
            "total_credits_covered": total_credits_covered,
            "token_delta": token_delta,
            "credit_delta": credit_delta,
            "reimbursement_ratio": round(total_tokens_covered / max(1.0, tokens_used_float), 6),
            "status": "surplus" if token_delta >= 0 else "deficit",
        },
    }

    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    ledger = ROOT / args.ledger
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(report, ensure_ascii=False) + "\n")

    snapshot_message = "skipped"
    if args.zip_snapshot:
        snapshot_message = _run_zip_snapshot(args.zip_label)

    print(f"Wrote {out}")
    print(f"Appended {ledger}")
    if args.zip_snapshot:
        print(snapshot_message)


if __name__ == "__main__":
    main()
