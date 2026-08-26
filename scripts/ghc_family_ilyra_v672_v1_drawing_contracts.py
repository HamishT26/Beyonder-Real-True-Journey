"""Bounded synthetic drawing-package contract board for Ilyra v672-v1.

The module validates declared revision and provenance structure only. It does
not create, approve, issue, coordinate, certify, or interpret a real drawing.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

REQUIRED = {
    "package_id",
    "sheet_index",
    "document_identity",
    "revision",
    "prior_revision",
    "supersedes",
    "issue_status",
    "issue_purpose",
    "external_references",
    "reference_pin_state",
    "transmittal",
    "provenance",
    "authority_vacancy",
    "rights_vacancy",
    "accessible_register",
    "gm_ut_boundary",
    "real_documents",
    "professional_decisions",
    "external_actions",
}


class DrawingContractError(ValueError):
    """Raised when a bounded drawing-package obligation is absent or promoted."""


def positive_fixture() -> dict[str, Any]:
    """Return one wholly synthetic, non-authoritative drawing package."""

    return {
        "package_id": "synthetic-drawing-package-01",
        "sheet_index": [
            {"sheet_id": "SYN-A-001", "title": "synthetic context plan", "revision": 2},
            {"sheet_id": "SYN-A-101", "title": "synthetic plan", "revision": 2},
        ],
        "document_identity": {
            "namespace": "owner-local-synthetic",
            "stable_id": "drawing-package-01",
            "identity_authority": False,
        },
        "revision": 2,
        "prior_revision": 1,
        "supersedes": "synthetic-drawing-package-01-r1",
        "issue_status": "held_for_bounded_review",
        "issue_purpose": "synthetic coordination exercise only",
        "external_references": ["synthetic-structure-grid-r2", "synthetic-services-layout-r2"],
        "reference_pin_state": "declared_exact_synthetic_revision",
        "transmittal": {
            "recipient": "synthetic-vacant-recipient",
            "readback": True,
            "delivery": False,
        },
        "provenance": {
            "source": "owner-local-fixture",
            "lineage_complete_for_fixture": True,
            "real_world_provenance": False,
        },
        "authority_vacancy": True,
        "rights_vacancy": True,
        "accessible_register": {
            "caption": True,
            "column_headers": True,
            "status_text": True,
            "manual_evaluation": False,
            "affected_user_evaluation": False,
        },
        "gm_ut_boundary": {
            "drawing_geometry_is_not_physical_evidence": True,
            "prediction": False,
            "parameter_constraint": False,
            "theory_of_everything": False,
            "stage20": False,
        },
        "real_documents": 0,
        "professional_decisions": 0,
        "external_actions": 0,
    }


def validate_board(board: dict[str, Any]) -> dict[str, Any]:
    """Validate one structural fixture and fail closed on authority promotion."""

    if not isinstance(board, dict):
        raise DrawingContractError("board must be an object")
    missing = sorted(REQUIRED - board.keys())
    if missing:
        raise DrawingContractError(f"missing obligations: {missing}")
    if not board["sheet_index"]:
        raise DrawingContractError("sheet index must not be empty")
    sheet_ids = [row.get("sheet_id") for row in board["sheet_index"]]
    if len(sheet_ids) != len(set(sheet_ids)) or any(not value for value in sheet_ids):
        raise DrawingContractError("sheet identifiers must be present and unique")
    if board["revision"] != board["prior_revision"] + 1:
        raise DrawingContractError("revision must advance exactly once")
    expected_superseded = f"synthetic-drawing-package-01-r{board['prior_revision']}"
    if board["supersedes"] != expected_superseded:
        raise DrawingContractError("supersession edge does not match the prior revision")
    if board["reference_pin_state"] != "declared_exact_synthetic_revision":
        raise DrawingContractError("external references are not revision pinned")
    if board["transmittal"].get("readback") is not True or board["transmittal"].get("delivery") is not False:
        raise DrawingContractError("transmittal must retain readback and refuse delivery")
    if board["authority_vacancy"] is not True or board["rights_vacancy"] is not True:
        raise DrawingContractError("authority and rights vacancies must remain explicit")
    accessible = board["accessible_register"]
    if any(accessible.get(key) is not True for key in ("caption", "column_headers", "status_text")):
        raise DrawingContractError("accessible register structure is incomplete")
    if accessible.get("manual_evaluation") is not False or accessible.get("affected_user_evaluation") is not False:
        raise DrawingContractError("manual or affected-user evaluation cannot be fabricated")
    firewall = board["gm_ut_boundary"]
    if firewall.get("drawing_geometry_is_not_physical_evidence") is not True:
        raise DrawingContractError("GMUT evidence firewall is absent")
    if any(firewall.get(key) is not False for key in ("prediction", "parameter_constraint", "theory_of_everything", "stage20")):
        raise DrawingContractError("physical or terminal promotion is prohibited")
    if any(board[key] != 0 for key in ("real_documents", "professional_decisions", "external_actions")):
        raise DrawingContractError("real documents, professional decisions, and actions must remain zero")
    return {
        "accepted": True,
        "package_id": board["package_id"],
        "sheet_count": len(board["sheet_index"]),
        "revision": board["revision"],
        "authority_conferred": False,
        "professional_result": False,
        "boundary": "synthetic drawing-package contract evidence only",
    }


def rejecting_fixtures() -> list[dict[str, Any]]:
    """Return preregistered mutations that each violate one protected invariant."""

    fixtures: list[dict[str, Any]] = []
    for mutator in (
        lambda row: row.pop("sheet_index"),
        lambda row: row.update({"revision": row["prior_revision"]}),
        lambda row: row.update({"supersedes": "synthetic-wrong-parent"}),
        lambda row: row.update({"authority_vacancy": False}),
        lambda row: row.update({"external_actions": 1}),
    ):
        row = deepcopy(positive_fixture())
        mutator(row)
        fixtures.append(row)
    return fixtures
