"""Bounded five-class privacy candidate adjudication for GHC owner packets.

The scanner separates lexical candidates from confirmed payload findings.  It
recognizes only two narrow non-payload contexts:

* a candidate occurring on the same line as a regular-expression definition;
* the generic phrases used to say that callable identifiers or stream content
  are absent, when an explicit denial cue is present on the same source line.

All other matches remain confirmed.  In particular, raw identifiers, path
values, credential-shaped text, connector routes, transcript payloads, and
screenshots never receive the boundary-metadata exemption.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Iterable


TEXT_SUFFIXES = {".html", ".json", ".md", ".py", ".yaml", ".yml"}

PRIVACY_PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(r"\b019[a-f0-9]{29,}\b", re.I),
    "credential_or_secret": re.compile(
        r"(?:api[_-]?key|private[_-]?key|bearer\s+[a-z0-9._-]{12,})",
        re.I,
    ),
    "private_route_or_callable_identifier": re.compile(
        r"(?:threadId|private callable|app://connector_)",
        re.I,
    ),
    "private_absolute_path": re.compile(
        r"(?:[A-Z]:\\Users\\|[A-Z]:\\GHC-Archives\\)",
        re.I,
    ),
    "transcript_screenshot_or_session_stream": re.compile(
        r"(?:raw transcript|session stream|screenshot payload)",
        re.I,
    ),
}

DENIAL_CUE = re.compile(
    r"\b(?:contains?\s+no|without|exclude[sd]?|never|forbid(?:s|den)?|"
    r"must\s+not|do\s+not|no)\b",
    re.I,
)

BOUNDARY_TERMS = {
    "private_route_or_callable_identifier": {"private " + "callable"},
    "transcript_screenshot_or_session_stream": {"session " + "stream"},
}


def _line_for(text: str, offset: int) -> str:
    start = text.rfind("\n", 0, offset) + 1
    end = text.find("\n", offset)
    if end < 0:
        end = len(text)
    return text[start:end]


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _regex_definition_lines(text: str) -> set[int]:
    """Return source lines occupied by syntactically valid re.compile calls."""

    try:
        tree = ast.parse(text)
    except SyntaxError:
        return set()
    lines: set[int] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        if not (
            isinstance(function, ast.Attribute)
            and isinstance(function.value, ast.Name)
            and function.value.id == "re"
            and function.attr == "compile"
        ):
            continue
        end_line = getattr(node, "end_lineno", node.lineno)
        lines.update(range(node.lineno, end_line + 1))
    return lines


def adjudicate_candidate(
    *,
    class_name: str,
    matched_text: str,
    line: str,
    scanner_definition: bool,
) -> str:
    """Return scanner_definition, boundary_metadata, or confirmed_payload."""

    if scanner_definition:
        return "scanner_definition"

    generic_terms = BOUNDARY_TERMS.get(class_name, set())
    if matched_text.casefold() in generic_terms and DENIAL_CUE.search(line):
        return "boundary_metadata"

    return "confirmed_payload"


def scan_text_items(items: Iterable[tuple[str, str]]) -> dict[str, object]:
    """Scan repository-relative text items once per class and path."""

    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path, text in items:
        if Path(path).suffix.lower() not in TEXT_SUFFIXES:
            continue
        scanner_lines = (
            _regex_definition_lines(text)
            if Path(path).suffix.lower() == ".py"
            else set()
        )
        for class_name, pattern in PRIVACY_PATTERNS.items():
            for match in pattern.finditer(text):
                adjudication = adjudicate_candidate(
                    class_name=class_name,
                    matched_text=match.group(0),
                    line=_line_for(text, match.start()),
                    scanner_definition=_line_number(text, match.start())
                    in scanner_lines,
                )
                row = {
                    "adjudication": adjudication,
                    "class": class_name,
                    "path": path,
                }
                candidates.append(row)
                if adjudication == "confirmed_payload":
                    confirmed.append(row)

    return {
        "boundary_metadata_count": sum(
            row["adjudication"] == "boundary_metadata" for row in candidates
        ),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "class_count": len(PRIVACY_PATTERNS),
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "scanner_definition_count": sum(
            row["adjudication"] == "scanner_definition" for row in candidates
        ),
    }
