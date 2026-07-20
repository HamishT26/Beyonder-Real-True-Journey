#!/usr/bin/env python3
"""Shared bounded runner support for the ten v650-v6 family-current callers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import ghc_family_v650_v6_runtime as runtime


def execute_group(name: str, proposal_ids: Iterable[str], output: Path) -> dict:
    ids = list(proposal_ids)
    rows = [runtime.execute_proposal(proposal_id) for proposal_id in ids]
    payload = {
        "schema": "ghc.family.v650-v6.runner-witness.v1",
        "runner": name,
        "proposal_ids": ids,
        "valid_fixture_count": sum(row["canonical_result"]["accepted"] for row in rows),
        "rejected_mutation_count": sum(
            not mutation["accepted"] for row in rows for mutation in row["mutations"]
        ),
        "passed": all(row["passed"] for row in rows),
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": "Bounded synthetic, symbolic, structural, or zero-row witness only; no production, empirical, professional, authority, independent-reproduction, or Stage 20 credit.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return payload


def wrapper_main(name: str, proposal_ids: Iterable[str]) -> int:
    parser = argparse.ArgumentParser(description=f"Run bounded {name} fixtures.")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = execute_group(name, proposal_ids, args.output)
    return 0 if payload["passed"] else 1
