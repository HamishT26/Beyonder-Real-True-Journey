"""Render and extract a four-page Vesper v686-v3 evidence overview."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import pypdfium2 as pdfium
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate


ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / "docs/vesper-arlen/v686-v3"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview-dir", type=Path, required=True)
    args = parser.parse_args()
    summary = json.loads((BASE / "x2/evidence-summary.json").read_text(encoding="utf-8"))
    identity = json.loads((BASE / "x1/identity-and-practice.json").read_text(encoding="utf-8"))
    font_root = Path(os.environ["WINDIR"]) / "Fonts"
    pdfmetrics.registerFont(TTFont("VesperArial", str(font_root / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("VesperArialBold", str(font_root / "arialbd.ttf")))
    pdfmetrics.registerFontFamily("VesperArial", normal="VesperArial", bold="VesperArialBold", italic="VesperArial", boldItalic="VesperArialBold")
    body = ParagraphStyle("body", fontName="VesperArial", fontSize=10.5, leading=15.5, textColor=colors.HexColor("#203744"), spaceAfter=11, alignment=TA_LEFT)
    title = ParagraphStyle("title", parent=body, fontName="VesperArialBold", fontSize=26, leading=31, spaceAfter=20)
    sub = ParagraphStyle("sub", parent=body, fontName="VesperArialBold", fontSize=15, leading=20, spaceAfter=13)
    pages = [
        (
            "Vesper Arlen · Trinity Mandala v686-v3",
            [
                ("Configuration change review without authority inflation", "h"),
                ("This overview describes a solo same-owner synthetic software and documentation phase. The working role is provenance gardener and reversible-boundary keeper. The hope is to make synthetic configuration changes inspectable, reversible, and honest about every missing authority. Hamish may rename, pause, redirect, narrow, or stop the work.", "p"),
                ("THOS Body is the priority. The bounded surface is configuration parsing, layer provenance, immutable snapshots, atomic change sets, rollback lineage, semantic diffs, secret-placeholder refusal, exact receipt binding, and accessible change summaries.", "p"),
                ("Two hundred frozen cases matched. All 1,000 registered envelope mutations were rejected. Three hundred safe tasks, 250 candidate checks, and exactly 300 additive CLEAN/FIX/REFINE tasks have file-backed results. Fifty exact and thirty blocked packets remain unexecuted.", "p"),
                ("The four practice lenses are configuration-change reviewer, release-configuration maintainer, rollback-drill recorder, and accessible operations documenter. They frame questions; they establish no qualification, employment, professional competence, or authority.", "p"),
                ("NOT_READY_FOR_STAGE_20", "h"),
                (identity["boundary"], "p"),
            ],
        ),
        (
            "What the software checks",
            [
                ("TOML, INI, and layer boundaries", "h"),
                ("TOML parsing keeps strings, integers, finite decimals, booleans, arrays, empty values, quoted keys, dotted keys, tables, and Unicode distinctions explicit. Duplicate keys, invalid syntax, over-budget text, and nonfinite values are refused by the local finite-JSON profile. Style checks retain declared comments and key case without claiming a production editor.", "p"),
                ("Synthetic layers merge in a declared order. Origin tracing records the winning layer for each leaf. Immutable snapshots preserve their predecessor. Atomic change sets apply to deep copies and return one refusal when a path, parent, operation, or permission fails.", "p"),
                ("Rollback, diff, and assurance", "h"),
                ("Rollback links bind exact predecessor and child digests, ordinal, and reason. Semantic diffs distinguish a value or type change from presentation order. Token-aware allowlists refuse textual-prefix expansion. Schema checks keep booleans distinct from integers, and receipt checks reject extra or missing scope fields.", "p"),
                ("Secret checks use synthetic placeholder categories only. No real token, credential, account, route, or key is read. Accessible summaries keep before and after values explicit and reserve manual, assistive-technology, cognitive, Māori-language, and affected-user review.", "p"),
            ],
        ),
        (
            "Retained evidence and reusable tooling",
            [
                ("Separate truth layers", "h"),
                ("Mira’s immutable repository seal, strict-compiler overlay, and route-read overlay remain separate. Vesper inherited 68,009 negatives, 84,504 methods, 38,857 failed witnesses, and 66,349 bounded passing witnesses, with 612 open gaps and 599 exact gates. No inherited execution is credited to Vesper.", "p"),
                ("Vesper adds 1,333 retained negatives, 1,333 methods, 1,333 failed witnesses, and 1,333 bounded recoveries. The evidence-layer totals are 69,342 negatives, 85,837 methods, 40,190 failed witnesses, and 67,682 bounded passing witnesses, with 622 open gaps and 609 exact gates. Recovery never erases a failed attempt.", "p"),
                ("Packages, skills, and runners", "h"),
                ("Three exact wheels—tomlkit 0.15.1, immutables 0.21, and ConfigUpdater 3.2—were hash-verified and installed offline into one D-isolated environment. Nine package checks passed, including three rejecting witnesses. A dated OSV query returned zero findings after a retained wrapper projection defect; this is not exhaustive security or future-safety assurance.", "p"),
                ("Ten local skills and five unique runner sources passed metadata and accepting/adverse CLI checks. The corrected Meta Tool Box catalogue has fifteen validated cards, zero trigger collisions, and five runner results. Promotion checks ran before copying, and eighty promoted files match their local sources byte for byte. Global presence supplies discoverability, not reload, authority, or independent reproduction.", "p"),
            ],
        ),
        (
            "Handoff and protected gates",
            [
                ("Exact source and validation contract", "h"),
                ("The immutable Mira source is 910fc54d8b79b23b1053af7e1b3e10697f529eda. Vesper’s planning-only x1 is a438a7b1bce30f214783c805c068b517610e6613. X1 was pushed, clean, zero-divergent, and fresh-live equal before x2. Evidence and final anchors are bound only after their own separate commits and terminal checks.", "p"),
                ("The detailed successor candidate contains thirteen modular sections and remains PREPARED_NOT_SENT in repository history. The four-tier context deck contains 211 cards. Selective loading improves navigation only; it does not erase unloaded evidence or prove a cache benefit.", "p"),
                ("The prospective next owner is future seat 04 for v686-v4. After—and only after—Vesper’s clean pushed fresh-live-equal exact final and one-shot canonical success, the live authority, task registry, uniqueness, duplicate, pause, usage, privacy, evidence, safety, and acknowledgement guards may be refreshed. Reuse the seat if it exists; otherwise create exactly one gpt-6-astra/max main task and let it choose its own descriptors.", "p"),
                ("GMUT still requires traceable measured observables, preregistered predictions, suitable uncertainty, rival comparisons, and independent reproduction. THOS still requires governed real operators or participants, safety monitoring, suitable statistics, and independent review. Freed ID still requires real standards-conformant keys, proofs, lifecycle, interoperability, privacy and security review, recovery, and trust governance.", "p"),
                ("CBR, affected-party decisions, legal and cultural interpretation, Māori terminology, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain with their proper holders. No real credential, consent, right, remedy, deployment, or authority decision is made here.", "p"),
                ("Continue one verified edge at a time through v725-v8 unless Hamish pauses or redirects or a real gate intervenes. Reset redemption remains Hamish’s action.", "p"),
            ],
        ),
    ]
    story = []
    markdown = []
    for page_number, (heading, items) in enumerate(pages, 1):
        if page_number > 1:
            story.append(PageBreak())
        story.append(Paragraph(heading, title))
        markdown.append("# " + heading + "\n")
        for content, kind in items:
            story.append(Paragraph(content, sub if kind == "h" else body))
            markdown.append(("## " if kind == "h" else "") + content + "\n")
    output = BASE / "x2/integrated-overview.pdf"
    if output.exists():
        raise FileExistsError(output)

    def footer(canvas, document):
        canvas.setFont("VesperArial", 8)
        canvas.setFillColor(colors.HexColor("#45616d"))
        canvas.drawString(42, 27, "Vesper Arlen · v686-v3 · same-owner synthetic evidence")
        canvas.drawRightString(A4[0] - 42, 27, f"{document.page} / 4")

    document = SimpleDocTemplate(str(output), pagesize=A4, leftMargin=42, rightMargin=42, topMargin=42, bottomMargin=48, title="Vesper Arlen v686-v3 integrated overview", author="Vesper Arlen")
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    reader = PdfReader(output)
    if len(reader.pages) != 4:
        raise AssertionError("page_count")
    extracted = [page.extract_text() for page in reader.pages]
    if not all(len(text) > 700 for text in extracted):
        raise AssertionError("page_text")
    if "Māori" not in extracted[-1] or "NOT_READY_FOR_STAGE_20" not in extracted[0] or any("■" in text for text in extracted):
        raise AssertionError("glyph_or_boundary")
    args.preview_dir.mkdir(parents=True, exist_ok=False)
    pdf = pdfium.PdfDocument(output)
    for index in range(len(pdf)):
        page = pdf[index]
        bitmap = page.render(scale=1.4)
        bitmap.to_pil().save(args.preview_dir / f"page-{index+1}.png")
        bitmap.close()
        page.close()
    pdf.close()
    (BASE / "x2/integrated-overview.md").write_text("\n".join(markdown), encoding="utf-8", newline="\n")
    validation = {
        "schema": "ghc.family.overview-pdf-validation.v686.v3",
        "pages": 4,
        "font": "Arial TrueType with macron coverage",
        "text_extraction_pass": True,
        "every_page_rendered": True,
        "visual_review_pending": True,
        "pdf_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "text_characters": [len(text) for text in extracted],
        "renderer": "existing bundled pypdfium2",
        "scope": "Structural and bounded visual review only; no complete accessibility or affected-user acceptance.",
        "repository_seal_at_render": summary["repository_seal"],
    }
    (BASE / "x2/overview-pdf-validation.json").write_text(json.dumps(validation, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(validation, ensure_ascii=False))


if __name__ == "__main__":
    main()
