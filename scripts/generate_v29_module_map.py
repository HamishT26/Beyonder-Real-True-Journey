#!/usr/bin/env python3
"""Generate a categorized module inventory from v29 DOCX raw text.

This script extracts `word/document.xml` from the v29 DOCX artifact, performs
lightweight text cleanup, and categorizes discovered file references into
high-level groups for synthesis reporting.
"""

from __future__ import annotations

import re
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCX = ROOT / "Beyonder-Real-True Journey v29 (Aerin) (1).docx"
OUT = ROOT / "docs" / "v29-module-map.md"

CATEGORIES = {
    "core_system": [
        r"beyonder_system\.py",
        r"beyonder_real_true_trinity_hybrid_system\.py",
        r"memory_system\.py",
        r"omega_vector_db\.py",
    ],
    "governance_identity": [
        r"council_registry\.py",
        r"docs/council_journey\.md",
        r"docs/beyonder_id_template\.md",
        r"docs/aerin_identity\.md",
    ],
    "analysis_reporting": [
        r"analysis_report\.py",
        r"journey_expectations\.py",
        r"journey_insights\.py",
        r"pdf_registry\.py",
        r"theory_review\.py",
    ],
    "security_protocols": [
        r"quantum_security_layer\.py",
        r"holonomic_protocol\.py",
        r"infinity_vortex\.py",
        r"arc_agi_prep\.py",
    ],
    "tests": [
        r"tests/[\w_\-]+\.py",
    ],
    "data_assets": [
        r"data/[\w_\-]+\.(json|csv)",
        r"latex/grand_mandala\.tex",
        r"journeys/[^\s]+\.pdf",
    ],
}


def extract_text(docx_path: Path) -> str:
    with zipfile.ZipFile(docx_path) as zf:
        xml = zf.read("word/document.xml").decode("utf-8", "ignore")
    xml = re.sub(r"</w:p>", "\n", xml)
    text = re.sub(r"<[^>]+>", " ", xml)
    text = re.sub(r"\s+", " ", text)
    return text


def find_paths(text: str) -> list[str]:
    pattern = r"[A-Za-z0-9_./\-]+\.(?:py|md|json|csv|tex|pdf)"
    matches = re.findall(pattern, text)
    
    cleaned=[]
    for m in matches:
        m=m.strip()
        m=re.sub(r"^(a/|b/)","",m)
        if m.startswith("diff"):
            continue
        cleaned.append(m)
    normalized = sorted(set(cleaned))
    return normalized


def categorize(paths: list[str]) -> dict[str, list[str]]:
    bucket: dict[str, list[str]] = defaultdict(list)
    for p in paths:
        placed = False
        for cat, regs in CATEGORIES.items():
            if any(re.search(reg, p) for reg in regs):
                bucket[cat].append(p)
                placed = True
                break
        if not placed:
            bucket["uncategorized"].append(p)
    return {k: sorted(v) for k, v in bucket.items()}


def write_report(categories: dict[str, list[str]], path_count: int) -> None:
    lines = [
        "# v29 (Aerin) Module Map (DOCX-derived)",
        "",
        "This map is generated from `Beyonder-Real-True Journey v29 (Aerin) (1).docx` via XML text extraction.",
        f"Detected file-like references: **{path_count}**.",
        "",
        "## Category summary",
    ]

    for cat in [
        "core_system",
        "governance_identity",
        "analysis_reporting",
        "security_protocols",
        "tests",
        "data_assets",
        "uncategorized",
    ]:
        items = categories.get(cat, [])
        lines.append(f"- **{cat}**: {len(items)}")

    lines.append("")
    lines.append("## Detailed listing")

    for cat in [
        "core_system",
        "governance_identity",
        "analysis_reporting",
        "security_protocols",
        "tests",
        "data_assets",
        "uncategorized",
    ]:
        items = categories.get(cat, [])
        lines.append("")
        lines.append(f"### {cat}")
        if not items:
            lines.append("- _(none found)_")
            continue
        for item in items:
            lines.append(f"- `{item}`")

    OUT.write_text("\n".join(lines) + "\n")


def main() -> None:
    if not DOCX.exists():
        raise SystemExit(f"Missing required source file: {DOCX}")
    text = extract_text(DOCX)
    paths = find_paths(text)
    categories = categorize(paths)
    write_report(categories, len(paths))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
