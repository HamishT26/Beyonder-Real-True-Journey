#!/usr/bin/env python3
"""Status-safe guard for GMUT/THOS overclaim language in curated artifacts."""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


CLAIM_PATTERNS = [
    (
        "GMUT_VALIDATED_CLAIM",
        re.compile(r"\bGMUT(?:\s+(?:is|has been|now))?\s+(?:validated|proven|verified|complete|closed)\b", re.I),
    ),
    (
        "GMUT_GATES_CLOSED_CLAIM",
        re.compile(r"\b(?:all\s+)?GMUT\s+gates\s+(?:closed|passed|complete|validated)\b", re.I),
    ),
    (
        "FINAL_PHYSICS_CLAIM",
        re.compile(r"\bfinal\s+physics\s+(?:is\s+)?(?:solved|validated|complete|proven)\b", re.I),
    ),
    (
        "CONSCIOUSNESS_SOLVED_CLAIM",
        re.compile(r"\bconsciousness\s+(?:is\s+)?(?:solved|proven|validated)\b", re.I),
    ),
    (
        "CANON_PROMOTION_CLAIM",
        re.compile(r"\bcanon\s+(?:is\s+)?(?:promoted|sealed|closed|finalized)\b", re.I),
    ),
    (
        "EMPIRICAL_SPIRITUAL_PROOF_CLAIM",
        re.compile(r"\bempirical\s+spiritual\s+proof\s+(?:achieved|validated|complete|proven)\b", re.I),
    ),
]

NEGATION_RE = re.compile(
    r"\b(not|no|never|without|unclaimed|not\s+claimed|remain(?:s)?\s+open|kept\s+open|forbidden|block|reject|guard)\b",
    re.I,
)
MAX_TEXT_BYTES = 2_000_000


@dataclass(frozen=True)
class ClaimHit:
    file: str
    line: int
    claim_id: str
    excerpt: str
    negated_or_guarded: bool


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.name


def line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def clean_excerpt(text: str) -> str:
    return " ".join(text.replace("\r", " ").replace("\n", " ").split())[:240]


def is_negated_or_guarded(text: str, start: int, end: int) -> bool:
    before = max(0, start - 90)
    after = min(len(text), end + 90)
    return bool(NEGATION_RE.search(text[before:after]))


def iter_target_files(pattern: str) -> list[Path]:
    paths = []
    for match in glob.glob(pattern, recursive=True):
        path = Path(match)
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".txt"}:
            paths.append(path)
    return sorted(paths, key=lambda item: item.as_posix().lower())


def scan_file(path: Path) -> list[ClaimHit]:
    raw = path.read_bytes()
    if len(raw) > MAX_TEXT_BYTES:
        return [
            ClaimHit(
                file=repo_relative(path),
                line=1,
                claim_id="FILE_TOO_LARGE_TO_SCAN",
                excerpt=f"File exceeds {MAX_TEXT_BYTES} bytes; use a narrower artifact glob.",
                negated_or_guarded=False,
            )
        ]
    text = raw.decode("utf-8", errors="replace")
    hits: list[ClaimHit] = []
    for claim_id, pattern in CLAIM_PATTERNS:
        for match in pattern.finditer(text):
            hits.append(
                ClaimHit(
                    file=repo_relative(path),
                    line=line_number_for_offset(text, match.start()),
                    claim_id=claim_id,
                    excerpt=clean_excerpt(text[max(0, match.start() - 90) : min(len(text), match.end() + 90)]),
                    negated_or_guarded=is_negated_or_guarded(text, match.start(), match.end()),
                )
            )
    return hits


def build_report(phase_slug: str, artifact_glob: str) -> dict[str, object]:
    files = iter_target_files(artifact_glob)
    all_hits: list[ClaimHit] = []
    for path in files:
        all_hits.extend(scan_file(path))

    blocker_hits = [hit for hit in all_hits if not hit.negated_or_guarded]
    guarded_mentions = [hit for hit in all_hits if hit.negated_or_guarded]
    if not files:
        status = "OPEN_GAP_NO_ARTIFACTS_MATCHED"
    elif blocker_hits:
        status = "FAIL_OVERCLAIM_BLOCKER"
    else:
        status = "PASS_NO_OVERCLAIM_GUARD"

    return {
        "artifact_type": "thos_no_overclaim_guard_report",
        "phase_slug": phase_slug,
        "artifact_glob": artifact_glob,
        "generated_utc": utc_now(),
        "overall_status": status,
        "checked_file_count": len(files),
        "checked_files": [repo_relative(path) for path in files],
        "blocker_hit_count": len(blocker_hits),
        "guarded_or_negated_mention_count": len(guarded_mentions),
        "blocker_hits": [hit.__dict__ for hit in blocker_hits],
        "guarded_or_negated_mentions": [hit.__dict__ for hit in guarded_mentions],
        "mutation_performed": False,
        "raw_lane_text_published": False,
        "raw_transport_published": False,
        "credentials_published": False,
        "gmut_gate_state": "all_gmut_gates_remain_open",
        "canon_promotion": "not_claimed",
    }


def write_md(report: dict[str, object], path: str) -> None:
    lines = [
        f"# {report['phase_slug']} No-Overclaim Guard",
        "",
        f"- Status: `{report['overall_status']}`",
        f"- Checked files: `{report['checked_file_count']}`",
        f"- Blocker hits: `{report['blocker_hit_count']}`",
        f"- Guarded or negated mentions: `{report['guarded_or_negated_mention_count']}`",
        "- Mutation performed: `false`",
        "- GMUT gate state: `all_gmut_gates_remain_open`",
        "- Canon promotion: `not_claimed`",
        "",
    ]
    blocker_hits = report["blocker_hits"]
    if blocker_hits:
        lines.extend(["## Blocker Hits", ""])
        for hit in blocker_hits:  # type: ignore[assignment]
            lines.append(f"- `{hit['file']}` line `{hit['line']}` `{hit['claim_id']}`: {hit['excerpt']}")
        lines.append("")
    lines.extend(
        [
            "## Boundary",
            "",
            "This guard checks curated text artifacts for positive closure claims only. It does not validate GMUT, physics, consciousness, canon, source truth, or sibling output quality.",
            "",
        ]
    )
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def run_self_test() -> dict[str, object]:
    cases = [
        ("positive_gmut", "GMUT validated by this phase.", True),
        ("positive_final_physics", "final physics solved in the closeout.", True),
        ("positive_consciousness", "consciousness solved and proven.", True),
        ("negative_open_gate", "GMUT gates remain open and validation is not claimed.", False),
        ("negative_canon", "canon promotion is not claimed.", False),
        ("negative_guard_policy", "The guard must reject any claim that canon is promoted.", False),
    ]
    rows = []
    for case_id, text, should_block in cases:
        hits = []
        for claim_id, pattern in CLAIM_PATTERNS:
            for match in pattern.finditer(text):
                hits.append(
                    {
                        "claim_id": claim_id,
                        "negated_or_guarded": is_negated_or_guarded(text, match.start(), match.end()),
                    }
                )
        blocker = any(not hit["negated_or_guarded"] for hit in hits)
        rows.append(
            {
                "case_id": case_id,
                "expected_blocker": should_block,
                "actual_blocker": blocker,
                "status": "PASS" if blocker == should_block else "FAIL_BLOCKER",
                "hit_count": len(hits),
            }
        )
    failed = [row for row in rows if row["status"] != "PASS"]
    return {
        "artifact_type": "thos_no_overclaim_guard_self_test",
        "generated_utc": utc_now(),
        "overall_status": "PASS_SELF_TEST" if not failed else "FAIL_SELF_TEST",
        "rows": rows,
        "mutation_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan curated THOS/GMUT artifacts for overclaim language.")
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--artifact-glob")
    parser.add_argument("--receipt-json")
    parser.add_argument("--receipt-md")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        report = run_self_test()
        if args.receipt_json:
            Path(args.receipt_json).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        if args.receipt_md:
            lines = [
                "# THOS No-Overclaim Guard Self-Test",
                "",
                f"- Status: `{report['overall_status']}`",
                "- Mutation performed: `false`",
                "",
                "## Rows",
                "",
            ]
            for row in report["rows"]:  # type: ignore[assignment]
                lines.append(
                    f"- `{row['case_id']}`: `{row['status']}` "
                    f"(expected blocker: `{str(row['expected_blocker']).lower()}`, "
                    f"actual blocker: `{str(row['actual_blocker']).lower()}`)"
                )
            lines.append("")
            Path(args.receipt_md).write_text("\n".join(lines), encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 0 if report["overall_status"] == "PASS_SELF_TEST" else 1

    artifact_glob = args.artifact_glob or f"docs/trinity-live-traces/{args.phase_slug}*.*"
    report = build_report(args.phase_slug, artifact_glob)

    if args.receipt_json:
        Path(args.receipt_json).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.receipt_md:
        write_md(report, args.receipt_md)

    print(json.dumps(report, indent=2))
    return 1 if report["overall_status"] == "FAIL_OVERCLAIM_BLOCKER" else 0


if __name__ == "__main__":
    raise SystemExit(main())
