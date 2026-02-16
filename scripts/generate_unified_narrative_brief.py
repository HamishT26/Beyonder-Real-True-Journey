#!/usr/bin/env python3
"""Generate a unified narrative brief from current repo signals."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = ROOT / "docs" / "state-of-journey-changelog.md"
MEMORY_SUMMARY = ROOT / "docs" / "aurelis-memory-latest-summary.md"
OUT = ROOT / "docs" / "grand-unified-narrative-brief.md"


def _tail_bullets(path: Path, take: int) -> list[str]:
    if not path.exists():
        return []
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip().startswith("- ")]
    return lines[-take:] if take > 0 else lines


def _memory_state(path: Path) -> list[str]:
    if not path.exists():
        return ["- Memory summary file not found yet."]
    picked: list[str] = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        if ln.startswith("- Latest timestamp") or ln.startswith("- NZDT context") or ln.startswith("- Progress snapshot") or ln.startswith("- Next step"):
            picked.append(ln)
    return picked or ["- Memory summary not populated yet."]


def build_brief(changelog_take: int) -> str:
    bullets = _tail_bullets(CHANGELOG, changelog_take)
    memory = _memory_state(MEMORY_SUMMARY)
    now = datetime.now(timezone.utc).isoformat()

    lines = [
        "# Grand Unified Narrative Brief",
        "",
        f"Generated (UTC): {now}",
        "",
        "## 1) Current state summary",
        "- Trinity Hybrid OS now includes strict guardrails across cache, token/credit, and energy-bank projections.",
        "- Local skill operations are now first-class via the Trinity local skill installer system.",
        "- Background continuity operations are bounded with lock safety, fail-fast, and runtime-budget controls.",
        "",
        "## 2) Arc of progression",
        "Recent verified progression highlights:",
    ]
    if bullets:
        lines.extend(bullets)
    else:
        lines.append("- No changelog highlights available yet.")

    lines.extend(
        [
            "",
            "## 3) Strengths and gaps",
            "### Strengths",
            "- Reserve-first and projection validation paths are now explicit and machine-checkable.",
            "- Projection accounting now includes per-session coverage/shortfall plus aggregate summary reconciliation.",
            "- Local skill installation/verification can run without external network dependencies.",
            "",
            "### Gaps",
            "- Curated remote skill listing/install remains blocked in this environment due proxy/network limits.",
            "- Working tree still contains pre-existing modified memory-archive zip artifacts requiring separate LFS hygiene handling.",
            "",
            "## 4) Immediate roadmap",
            "- Run local skill installer (`--force --verify`) before each major integration pass.",
            "- Run quick suite + validators, then perform one background cycle with fail-fast enabled.",
            "- Continue memory updates and regenerate this brief at each milestone for continuity.",
            "",
            "## Memory continuity snapshot",
        ]
    )
    lines.extend(memory)
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate unified narrative brief")
    parser.add_argument("--changelog-take", type=int, default=12)
    parser.add_argument("--out", default=str(OUT.relative_to(ROOT)))
    args = parser.parse_args()

    out = (ROOT / args.out).resolve()
    out.relative_to(ROOT)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_brief(max(1, args.changelog_take)), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
