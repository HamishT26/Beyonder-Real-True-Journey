#!/usr/bin/env python3
"""Read-only semantic-neighbour screen for Eiren Kestrel v660-v2 titles.

The probe reads a JSON array of proposed titles from standard input, compares
each title with the immutable frozen-chain index and with every other proposed
title, and emits a deterministic JSON receipt.  It never writes repository or
external state.  Token overlap is only a bounded screen; mechanism review is
still required before preregistration.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


def tokens(value: str) -> set[str]:
    return set(TOKEN_PATTERN.findall(value.lower()))


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / len(left | right) if left or right else 1.0


def load_titles() -> list[str]:
    payload = json.load(sys.stdin)
    if not isinstance(payload, list) or not all(isinstance(row, str) for row in payload):
        raise ValueError("standard input must be a JSON array of title strings")
    return payload


def load_prior(path: Path) -> list[dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = [*payload["prior_proposals"], *payload["new_proposals"]]
    if len(rows) != payload["effective_count"]:
        raise ValueError("frozen-chain count drift")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("index", type=Path)
    parser.add_argument("--threshold", type=float, default=0.60)
    parser.add_argument("--expected-count", type=int, default=20)
    args = parser.parse_args()

    titles = load_titles()
    prior = load_prior(args.index)
    if len(titles) != args.expected_count:
        raise ValueError(f"expected {args.expected_count} titles, received {len(titles)}")
    if len(set(titles)) != len(titles):
        raise ValueError("duplicate proposed title")

    prior_tokens = [
        (row["proposal_id"], row["title"], tokens(row["title"])) for row in prior
    ]
    proposed_tokens = [(index + 1, title, tokens(title)) for index, title in enumerate(titles)]
    results: list[dict[str, Any]] = []
    for proposal_number, title, title_token_set in proposed_tokens:
        prior_score, prior_id, prior_title = max(
            (
                jaccard(title_token_set, prior_token_set),
                prior_proposal_id,
                prior_proposal_title,
            )
            for prior_proposal_id, prior_proposal_title, prior_token_set in prior_tokens
        )
        peer_candidates = [
            (jaccard(title_token_set, peer_tokens), peer_number, peer_title)
            for peer_number, peer_title, peer_tokens in proposed_tokens
            if peer_number != proposal_number
        ]
        peer_score, peer_number, peer_title = max(peer_candidates)
        results.append(
            {
                "proposal_number": proposal_number,
                "title": title,
                "inherited_titles_checked": len(prior_tokens),
                "nearest_prior_proposal_id": prior_id,
                "nearest_prior_title": prior_title,
                "max_prior_token_jaccard": round(prior_score, 6),
                "nearest_peer_number": peer_number,
                "nearest_peer_title": peer_title,
                "max_peer_token_jaccard": round(peer_score, 6),
                "passes_bounded_threshold": (
                    prior_score < args.threshold and peer_score < args.threshold
                ),
            }
        )

    receipt = {
        "schema": "ghc.family.proposal-novelty-read-only-probe.v1",
        "prior_title_count": len(prior),
        "proposed_title_count": len(titles),
        "threshold": args.threshold,
        "pass_count": sum(row["passes_bounded_threshold"] for row in results),
        "all_pass": all(row["passes_bounded_threshold"] for row in results),
        "maximum_prior_score": max(row["max_prior_token_jaccard"] for row in results),
        "maximum_peer_score": max(row["max_peer_token_jaccard"] for row in results),
        "results": results,
        "boundary": (
            "Token overlap is a bounded screen plus later mechanism review, not "
            "universal semantic novelty proof."
        ),
    }
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
