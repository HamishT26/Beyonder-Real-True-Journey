#!/usr/bin/env python3
"""Five-class privacy scan for bounded Caelen Ash v672-v4 text files."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

PATTERNS = {
    "raw_uuid_identifier": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"),
    "private_absolute_windows_path": re.compile(r"\b[A-Za-z]:\\(?:Users|GHC-Archives|Windows)\\[^\r\n\"']+"),
    "credential_assignment": re.compile(r"\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*[\"'][^\"']{8,}[\"']", re.I),
    "private_application_route": re.compile(r"\b(?:app|file|vscode)://[^\s\"']+"),
    "session_stream_marker": re.compile(r"\b(?:session[_-]?stream|terminal[_-]?session)\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--paths-json", required=True)
    args = parser.parse_args()
    root = Path(args.root)
    paths = json.loads(Path(args.paths_json).read_text(encoding="utf-8"))
    hits = []
    for relative in paths:
        path = root / relative
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                hits.append({"path": relative, "class": class_name, "offset": match.start()})
    print(json.dumps({"files": len(paths), "classes": len(PATTERNS), "confirmed_hits": hits, "valid": not hits}))
    raise SystemExit(0 if not hits else 1)

if __name__ == "__main__":
    main()
