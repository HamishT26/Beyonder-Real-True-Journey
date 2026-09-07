"""Bounded positive and adverse smokes for three isolated font packages."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import io
import json
import pathlib

import fontTools
import uharfbuzz as hb
import unicodedata2
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, TTLibError


def synthetic_font_bytes():
    builder = FontBuilder(1000, isTTF=True)
    glyph_order = [".notdef", "A"]
    builder.setupGlyphOrder(glyph_order)
    builder.setupCharacterMap({65: "A"})
    glyphs = {}
    pen = TTGlyphPen(None)
    glyphs[".notdef"] = pen.glyph()
    pen = TTGlyphPen(None)
    pen.moveTo((50, 0))
    pen.lineTo((300, 700))
    pen.lineTo((550, 0))
    pen.closePath()
    glyphs["A"] = pen.glyph()
    builder.setupGlyf(glyphs)
    builder.setupHorizontalMetrics({".notdef": (500, 0), "A": (600, 50)})
    builder.setupHorizontalHeader(ascent=800, descent=-200)
    builder.setupOS2(
        sTypoAscender=800,
        sTypoDescender=-200,
        usWinAscent=800,
        usWinDescent=200,
    )
    builder.setupNameTable(
        {
            "familyName": "Synthetic Tamar",
            "styleName": "Regular",
            "uniqueFontIdentifier": "Synthetic-Tamar-v688-v3",
            "fullName": "Synthetic Tamar Regular",
            "psName": "SyntheticTamar-Regular",
            "version": "Version 1.0",
        }
    )
    builder.setupPost()
    builder.setupMaxp()
    stream = io.BytesIO()
    builder.save(stream)
    return stream.getvalue()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    data = synthetic_font_bytes()
    font = TTFont(io.BytesIO(data), recalcBBoxes=False, recalcTimestamp=False)
    cmap = font.getBestCmap()
    fonttools_positive = {
        "glyph_order": font.getGlyphOrder(),
        "cmap_65": cmap.get(65),
        "advance_A": font["hmtx"].metrics["A"][0],
        "lsb_A": font["hmtx"].metrics["A"][1],
        "units_per_em": font["head"].unitsPerEm,
        "required_tables_present": all(tag in font for tag in ["cmap", "head", "hhea", "hmtx", "maxp", "name", "OS/2", "post"]),
        "synthetic_bytes_sha256": hashlib.sha256(data).hexdigest(),
    }
    try:
        TTFont(io.BytesIO(b"bad"))
        fonttools_adverse = {"refused": False, "error_type": None}
    except TTLibError as exc:
        fonttools_adverse = {"refused": True, "error_type": type(exc).__name__}

    face = hb.Face(data)
    hb_font = hb.Font(face)
    buffer = hb.Buffer()
    buffer.add_str("A")
    buffer.guess_segment_properties()
    hb.shape(hb_font, buffer, {})
    harfbuzz_positive = {
        "glyph_count": face.glyph_count,
        "units_per_em": face.upem,
        "shaped_count": len(buffer.glyph_infos),
        "glyph_ids": [info.codepoint for info in buffer.glyph_infos],
        "clusters": [info.cluster for info in buffer.glyph_infos],
        "x_advances": [position.x_advance for position in buffer.glyph_positions],
    }
    empty_face = hb.Face(b"")
    harfbuzz_adverse = {"refused": empty_face.glyph_count == 0, "error_type": "EMPTY_FACE" if empty_face.glyph_count == 0 else None}

    unicode_positive = {
        "unidata_version": unicodedata2.unidata_version,
        "name_A": unicodedata2.name("A"),
        "category_A": unicodedata2.category("A"),
        "combining_A": unicodedata2.combining("A"),
    }
    try:
        unicodedata2.name(chr(0xD800))
        unicode_adverse = {"refused": False, "error_type": None}
    except ValueError as exc:
        unicode_adverse = {"refused": True, "error_type": type(exc).__name__}

    versions = {
        "fonttools": importlib.metadata.version("fonttools"),
        "uharfbuzz": importlib.metadata.version("uharfbuzz"),
        "unicodedata2": importlib.metadata.version("unicodedata2"),
    }
    distributions = sorted(distribution.metadata["Name"].lower() for distribution in importlib.metadata.distributions())
    expected_versions = {"fonttools": "4.64.0", "uharfbuzz": "0.56.1", "unicodedata2": "17.0.1"}
    positive = {
        "fonttools": fonttools_positive,
        "uharfbuzz": harfbuzz_positive,
        "unicodedata2": unicode_positive,
    }
    adverse = {
        "fonttools": fonttools_adverse,
        "uharfbuzz": harfbuzz_adverse,
        "unicodedata2": unicode_adverse,
    }
    if versions != expected_versions:
        raise RuntimeError(f"Version mismatch: {versions}")
    if distributions != ["fonttools", "uharfbuzz", "unicodedata2"]:
        raise RuntimeError(f"Unexpected distributions: {distributions}")
    if not all(row["refused"] for row in adverse.values()):
        raise RuntimeError(f"Package adverse mismatch: {adverse}")
    if not (
        fonttools_positive["cmap_65"] == "A"
        and fonttools_positive["advance_A"] == 600
        and fonttools_positive["units_per_em"] == 1000
        and fonttools_positive["required_tables_present"]
        and harfbuzz_positive["glyph_count"] == 2
        and harfbuzz_positive["shaped_count"] == 1
        and unicode_positive["unidata_version"] == "17.0.0"
    ):
        raise RuntimeError("Package positive smoke mismatch")
    value = {
        "schema": "ghc.family.font-package-smokes.v1",
        "versions": versions,
        "distribution_count": 3,
        "distributions": distributions,
        "positive": positive,
        "adverse": adverse,
        "real_fonts": 0,
        "real_text_rows": 0,
        "rendering": 0,
        "external_writes": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"packages": 3, "positive": 3, "adverse_refused": 3, "output_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
