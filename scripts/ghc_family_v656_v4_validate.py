#!/usr/bin/env python3
"""Detailed and minimal validators for Caelen Morrow v656-v4 evidence."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Callable

import ghc_family_v656_v4_phase_data as d
from ghc_family_v656_v4_core import MUTATION_CLASSES, ZERO_REAL_COUNTS, validate_contract


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT


def read_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def _check(check_id: str, description: str, predicate: Callable[[], bool]) -> dict:
    try:
        passed = bool(predicate())
        detail = "passed" if passed else "predicate returned false"
    except Exception as exc:  # retained by caller if this ever occurs
        passed = False
        detail = f"{type(exc).__name__}: {exc}"
    return {
        "check_id": check_id,
        "description": description,
        "passed": passed,
        "detail": detail,
    }


def detailed_checks() -> list[dict]:
    proposals = read_json("x2/proposal-ledger.json")["proposals"]
    rows: list[dict] = []
    for index, proposal in enumerate(proposals, 1):
        slug = proposal["slug"]
        rows.append(
            _check(
                f"D{index:03d}",
                f"{proposal['proposal_id']} valid contract",
                lambda slug=slug: validate_contract(
                    read_json(f"surfaces/{slug}/contract.json")
                )
                == [],
            )
        )
    for index, proposal in enumerate(proposals, 31):
        slug = proposal["slug"]
        rows.append(
            _check(
                f"D{index:03d}",
                f"{proposal['proposal_id']} rejects all mutations",
                lambda slug=slug: (
                    read_json(f"surfaces/{slug}/mutation-results.json")[
                        "mutations_rejected"
                    ]
                    == 5
                    and {
                        item["mutation_class"]
                        for item in read_json(
                            f"surfaces/{slug}/mutation-results.json"
                        )["mutation_rows"]
                    }
                    == set(MUTATION_CLASSES)
                ),
            )
        )
    runner_receipts = sorted((ROOT / "runners").glob("*-receipt.json"))
    for offset, path in enumerate(runner_receipts, 61):
        relative = path.relative_to(ROOT).as_posix()
        rows.append(
            _check(
                f"D{offset:03d}",
                f"{relative} is a passing family-compatible runner receipt",
                lambda relative=relative: read_json(relative)["valid"] is True,
            )
        )
    skill_receipts = sorted((ROOT / "skills").glob("*/smoke-receipt.json"))
    for offset, path in enumerate(skill_receipts, 71):
        relative = path.relative_to(ROOT).as_posix()
        rows.append(
            _check(
                f"D{offset:03d}",
                f"{relative} is a passing phase-local skill receipt",
                lambda relative=relative: read_json(relative)["valid"] is True,
            )
        )
    rows.extend(
        [
            _check(
                "D081",
                "outcome ledger is exactly 23/5/1/1",
                lambda: Counter(p["observed_outcome"] for p in proposals)
                == Counter(
                    {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
                ),
            ),
            _check(
                "D082",
                "Method Flow retains every mutation failure and bounded recovery",
                lambda: (
                    read_json("method-flow/method-flow-ledger-x2.json")["counts"][
                        "methods"
                    ]
                    >= 640
                    and read_json("method-flow/method-flow-ledger-x2.json")["counts"][
                        "witness_results"
                    ]["fail"]
                    == read_json("method-flow/method-flow-ledger-x2.json")["counts"][
                        "witness_results"
                    ]["pass"]
                ),
            ),
        ]
    )
    if len(rows) != 82:
        raise RuntimeError(f"expected 82 detailed checks, built {len(rows)}")
    return rows


def minimal_checks() -> list[dict]:
    proposals = read_json("x2/proposal-ledger.json")["proposals"]
    checks = [
        ("M001", "proposal count", lambda: len(proposals) == 30),
        (
            "M002",
            "outcome vocabulary",
            lambda: set(p["observed_outcome"] for p in proposals)
            <= set(d.OUTCOME_CLASSES),
        ),
        (
            "M003",
            "outcome distribution",
            lambda: Counter(p["observed_outcome"] for p in proposals)
            == Counter({"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}),
        ),
        (
            "M004",
            "all zero-real-count contracts",
            lambda: all(
                read_json(f"surfaces/{p['slug']}/contract.json")["zero_real_counts"]
                == ZERO_REAL_COUNTS
                for p in proposals
            ),
        ),
        (
            "M005",
            "all valid fixtures pass",
            lambda: all(
                read_json(f"surfaces/{p['slug']}/bounded-receipt.json")["valid"]
                for p in proposals
            ),
        ),
        (
            "M006",
            "all 150 mutations rejected",
            lambda: sum(
                read_json(f"surfaces/{p['slug']}/mutation-results.json")[
                    "mutations_rejected"
                ]
                for p in proposals
            )
            == 150,
        ),
        (
            "M007",
            "effective negatives retained",
            lambda: read_json("truth/retained-negative-register-x2.json")[
                "effective_count"
            ]
            >= 14354,
        ),
        (
            "M008",
            "open gaps additive",
            lambda: read_json("truth/open-gap-register-x2.json")["effective_count"]
            == 100,
        ),
        (
            "M009",
            "exact gates additive",
            lambda: read_json("truth/exact-gate-register-x2.json")["effective_count"]
            == 99,
        ),
        (
            "M010",
            "ten phase-local skills",
            lambda: len(list((ROOT / "skills").glob("*/SKILL.md"))) == 10,
        ),
        (
            "M011",
            "ten family-compatible runners",
            lambda: len(list((ROOT / "runners").glob("*-receipt.json"))) == 10,
        ),
        (
            "M012",
            "privacy scan clean",
            lambda: read_json("validation/evidence-privacy-scan.json")[
                "confirmed_hit_count"
            ]
            == 0,
        ),
        (
            "M013",
            "terminal route remains unsent",
            lambda: read_json("truth/phase-truth-evidence.json")[
                "terminal_route_contacted"
            ]
            is False,
        ),
        (
            "M014",
            "source and x1 anchors immutable",
            lambda: read_json("truth/phase-truth-evidence.json")["x1_freeze"]
            == "1c84cf2616df4efbb13c2df89397941251e2def5",
        ),
        (
            "M015",
            "Stage 20 remains blocked",
            lambda: read_json("truth/phase-truth-evidence.json")["verdict"]
            == "NOT_READY_FOR_STAGE_20",
        ),
    ]
    return [_check(*item) for item in checks]


def validate() -> dict:
    detailed = detailed_checks()
    minimal = minimal_checks()
    return {
        "schema": "ghc.family.v656-v4.validation.v1",
        "phase": d.PHASE,
        "detailed": {
            "count": len(detailed),
            "passed": sum(item["passed"] for item in detailed),
            "checks": detailed,
        },
        "minimal": {
            "count": len(minimal),
            "passed": sum(item["passed"] for item in minimal),
            "checks": minimal,
        },
        "valid": all(item["passed"] for item in detailed + minimal),
    }


if __name__ == "__main__":
    print(json.dumps(validate(), ensure_ascii=False, sort_keys=True))
