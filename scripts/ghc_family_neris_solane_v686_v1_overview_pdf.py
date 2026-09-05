"""Render and structurally validate the Neris v686-v1 four-section overview PDF."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/neris-solane/v686-v1"
INPUT = BASE / "final/overview-pages.json"
OUTPUT = BASE / "final/integrated-overview.pdf"
VALIDATION = BASE / "final/overview-pdf-validation.json"


def footer(canvas, document):
    canvas.saveState()
    canvas.setFillColor(black)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(A4[0] / 2, 12 * mm, f"Neris Solane v686 v1   Page {document.page}")
    canvas.restoreState()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replace-failed-render", action="store_true")
    args = parser.parse_args()
    if (OUTPUT.exists() or VALIDATION.exists()) and not args.replace_failed_render:
        raise FileExistsError("Refusing to overwrite an overview artifact")
    previous_failure = None
    if args.replace_failed_render:
        if not OUTPUT.is_file() or not VALIDATION.is_file():
            raise FileNotFoundError("A replacement requires the exact retained first-render pair")
        previous_failure = {
            "pdf_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
            "validation_sha256": hashlib.sha256(VALIDATION.read_bytes()).hexdigest(),
            "visual_failure": "Pages 2 and 4 displayed black-square glyph substitutions for Māori macrons under Helvetica.",
            "success_credit": 0,
            "recovery": "Register Arial TrueType fonts with macron coverage, rebuild, and visually inspect every page again.",
        }
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    pdfmetrics.registerFont(TTFont("NerisArial", r"C:\Windows\Fonts\arial.ttf"))
    pdfmetrics.registerFont(TTFont("NerisArialBold", r"C:\Windows\Fonts\arialbd.ttf"))
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="NerisArialBold",
        fontSize=20,
        leading=24,
        textColor=black,
        alignment=TA_CENTER,
        spaceAfter=12 * mm,
    )
    heading = ParagraphStyle(
        "PageHeading",
        parent=styles["Heading1"],
        fontName="NerisArialBold",
        fontSize=15,
        leading=19,
        textColor=black,
        alignment=TA_LEFT,
        spaceAfter=7 * mm,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="NerisArial",
        fontSize=10.2,
        leading=14.5,
        textColor=black,
        alignment=TA_LEFT,
        spaceAfter=4.5 * mm,
    )
    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=24 * mm,
        rightMargin=24 * mm,
        topMargin=22 * mm,
        bottomMargin=22 * mm,
        title="Neris Solane v686 v1 integrated overview",
        author="Neris Solane relational working context",
        subject="Bounded owner-scoped software and evidence closeout",
    )
    story = []
    for index, page in enumerate(payload["pages"]):
        if index == 0:
            story.append(Paragraph("Neris Solane v686 v1 integrated overview", title))
        story.append(Paragraph(page["title"], heading))
        for paragraph in page["paragraphs"]:
            story.append(Paragraph(paragraph, body))
        if index != len(payload["pages"]) - 1:
            story.append(PageBreak())
    story.append(Spacer(1, 3 * mm))
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    reader = PdfReader(str(OUTPUT))
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    result = {
        "schema": "ghc.family.neris.overview-pdf-validation.v1",
        "path": "docs/neris-solane/v686-v1/final/integrated-overview.pdf",
        "bytes": OUTPUT.stat().st_size,
        "pages": len(reader.pages),
        "planned_sections": len(payload["pages"]),
        "pdf_text_extraction_pass": all(page["title"] in extracted for page in payload["pages"]),
        "terminal_verdict_present": "NOT_READY_FOR_STAGE_20" in extracted,
        "manual_visual_review_required": True,
        "previous_failed_render": previous_failure,
        "font_family": "Arial TrueType with macron coverage",
    }
    with VALIDATION.open("w" if args.replace_failed_render else "x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")
    print(json.dumps(result, sort_keys=True))
    return 0 if result["pages"] >= 3 and result["pdf_text_extraction_pass"] and result["terminal_verdict_present"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
