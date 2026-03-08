#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path


def _safe_console_text(text: str) -> str:
    encoding = sys.stdout.encoding or "utf-8"
    return text.encode(encoding, errors="replace").decode(encoding, errors="replace")


def _read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _read_docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml").decode("utf-8", errors="ignore")
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<[^>]+>", " ", xml)
    return re.sub(r"[ \t]+", " ", xml)


def _read_pdf_text(path: Path) -> str:
    txt_path = path.with_suffix(".txt")
    if txt_path.exists():
        return _read_text_file(txt_path)
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"no paired .txt and pypdf unavailable for {path.name}: {exc}") from exc
    reader = PdfReader(str(path))
    chunks: list[str] = []
    for page in reader.pages:
        chunks.append(page.extract_text() or "")
    return "\n".join(chunks)


def _read_zip_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        return "\n".join(sorted(archive.namelist()))


def _read_source_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md", ".json", ".py"}:
        return _read_text_file(path)
    if suffix == ".docx":
        return _read_docx_text(path)
    if suffix == ".pdf":
        return _read_pdf_text(path)
    if suffix == ".zip":
        return _read_zip_text(path)
    return _read_text_file(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan Journey artifacts for anchor patterns without Unix-only tooling.")
    parser.add_argument("paths", nargs="+", help="One or more source files to scan.")
    parser.add_argument("--regex", required=True, help="Case-insensitive regex used to find anchor lines.")
    parser.add_argument("--max-matches", type=int, default=20, help="Maximum matches to print per file.")
    parser.add_argument("--allow-empty", action="store_true", help="Exit successfully even if no matches are found.")
    parser.add_argument("--skip-missing", action="store_true", help="Skip missing files instead of failing.")
    args = parser.parse_args()

    pattern = re.compile(args.regex, re.IGNORECASE)
    any_match = False
    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            if args.skip_missing:
                print(_safe_console_text(f"SKIPPED {path.name}: file not found"))
                continue
            print(f"ERROR {path}: file not found", file=sys.stderr)
            return 1
        try:
            text = _read_source_text(path)
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR {path}: {exc}", file=sys.stderr)
            return 1

        matches = 0
        for lineno, line in enumerate(text.splitlines(), start=1):
            if not pattern.search(line):
                continue
            any_match = True
            matches += 1
            print(_safe_console_text(f"{path.name}:{lineno}: {line.strip()}"))
            if matches >= args.max_matches:
                break

    if any_match or args.allow_empty:
        return 0
    print("No matches found.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
