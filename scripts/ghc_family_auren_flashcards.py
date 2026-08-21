#!/usr/bin/env python3
"""Auren-local compatibility entry points for the generic family deck runner.

The immutable Auren x1 charter uses ``canonical_phase_id`` and intentionally
omits the older redundant ``display_phase`` mirror. This adapter supplies that
display-only value in memory while leaving x1 bytes and the shared runner
unchanged.
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

import ghc_family_freed_id_flashcards as _base


FlashcardError = _base.FlashcardError
private_candidates = _base.private_candidates
write_equal_or_new = _base.write_equal_or_new
validate_model = _base.validate_model
compact_message = _base.compact_message
accessible_report = _base.accessible_report
load_deck = _base.load_deck
manifest_status = _base.manifest_status
privacy_status = _base.privacy_status
validate_deck = _base.validate_deck
mutation_receipt = _base.mutation_receipt


@contextmanager
def _display_phase_compatibility() -> Iterator[None]:
    original = _base.strict_json

    def compatible(path: Path) -> dict[str, Any]:
        value = original(path)
        if path.name == "phase-charter.json" and "display_phase" not in value:
            value = {**value, "display_phase": value["canonical_phase_id"]}
        return value

    _base.strict_json = compatible
    try:
        yield
    finally:
        _base.strict_json = original


def build_model(phase_root: Path, x1_head: str) -> dict[str, Any]:
    with _display_phase_compatibility():
        return _base.build_model(phase_root, x1_head)


def build_outputs(repo: Path, phase_root_rel: str, output_rel: str, x1_head: str) -> dict[str, Any]:
    with _display_phase_compatibility():
        return _base.build_outputs(repo, phase_root_rel, output_rel, x1_head)
