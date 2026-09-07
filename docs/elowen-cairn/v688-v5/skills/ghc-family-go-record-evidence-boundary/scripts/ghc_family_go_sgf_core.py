#!/usr/bin/env python3
"""Typed synthetic Go/SGF contract core for Elowen Cairn v688-v5."""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import deque
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from typing import Any


ALLOWED: dict[str, set[str]] = {
    "sgf_coordinate": {"operation", "board_size", "coordinate"},
    "orthogonal_neighbors": {"operation", "board_size", "row", "column"},
    "chain_component": {"operation", "board", "point", "colour"},
    "liberty_frontier": {"operation", "board", "point", "colour"},
    "capture_projection": {"operation", "board", "move", "colour", "allow_suicide"},
    "suicide_projection": {"operation", "board", "move", "colour", "allow_suicide"},
    "simple_ko": {"operation", "two_plies_ago", "proposed", "next_colour", "policy", "referee_decision"},
    "position_digest": {"operation", "board", "next_colour", "ko_point", "identity_proof"},
    "setup_partition": {"operation", "board_size", "black", "white", "empty"},
    "move_sequence": {"operation", "board_size", "moves"},
    "game_tree_dag": {"operation", "parents", "root"},
    "variation_path": {"operation", "children", "path", "root"},
    "property_identifier": {"operation", "identifier"},
    "text_escape": {"operation", "text", "private_preclaim"},
    "result_token": {"operation", "result", "infer_winner"},
    "komi_rational": {"operation", "komi", "fairness_claim", "universal_rules_claim"},
    "time_record": {"operation", "main_seconds", "scheme", "observed"},
    "record_evidence": {"operation", "claim", "available_roles", "synthetic"},
    "accessible_board": {"operation", "board", "row_labels", "column_labels", "language", "manual_evaluation"},
    "authority_boundary": {"operation", "claim", "authority_present", "synthetic"},
}


def ok(value: Any) -> dict[str, Any]:
    return {"accepted": True, "error": None, "external_credit": False, "value": value}


def err(code: str) -> dict[str, Any]:
    return {"accepted": False, "error": code, "external_credit": False, "value": None}


def typed_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return list(left) == list(right) and all(typed_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(typed_equal(a, b) for a, b in zip(left, right))
    return left == right


def strict_loads(data: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise ValueError("DUPLICATE_KEY")
            result[key] = value
        return result

    return json.loads(
        data,
        object_pairs_hook=pairs,
        parse_constant=lambda _: (_ for _ in ()).throw(ValueError("NONFINITE_JSON")),
    )


def _int(value: Any) -> bool:
    return type(value) is int


def _point(value: Any) -> bool:
    return isinstance(value, list) and len(value) == 2 and all(_int(x) for x in value)


def _board(value: Any) -> tuple[list[list[str]] | None, str | None]:
    if not isinstance(value, list) or not value or not all(isinstance(row, str) for row in value):
        return None, "BOARD_SHAPE"
    size = len(value)
    if any(len(row) != size for row in value):
        return None, "BOARD_SHAPE"
    if any(char not in ".BW" for row in value for char in row):
        return None, "BOARD_SYMBOL"
    return [list(row) for row in value], None


def _inside(board: list[list[str]], point: list[int]) -> bool:
    return 0 <= point[0] < len(board) and 0 <= point[1] < len(board)


def _neighbors(size: int, point: tuple[int, int]) -> list[tuple[int, int]]:
    row, column = point
    return sorted((r, c) for r, c in ((row - 1, column), (row, column - 1), (row, column + 1), (row + 1, column)) if 0 <= r < size and 0 <= c < size)


def _chain(board: list[list[str]], point: tuple[int, int]) -> list[tuple[int, int]]:
    colour = board[point[0]][point[1]]
    if colour == ".":
        return []
    seen = {point}
    queue = deque([point])
    while queue:
        current = queue.popleft()
        for neighbour in _neighbors(len(board), current):
            if neighbour not in seen and board[neighbour[0]][neighbour[1]] == colour:
                seen.add(neighbour)
                queue.append(neighbour)
    return sorted(seen)


def _liberties(board: list[list[str]], chain: list[tuple[int, int]]) -> list[tuple[int, int]]:
    found = set()
    for point in chain:
        for neighbour in _neighbors(len(board), point):
            if board[neighbour[0]][neighbour[1]] == ".":
                found.add(neighbour)
    return sorted(found)


def _coordinate(payload: dict[str, Any]) -> dict[str, Any]:
    size = payload["board_size"]
    coordinate = payload["coordinate"]
    if not _int(size) or size < 1 or size > 26:
        return err("INTEGER_TYPE")
    if type(coordinate) is not str:
        return err("TEXT_TYPE")
    if coordinate == "":
        return ok({"pass": True, "row": None, "column": None, "board_size": size})
    if len(coordinate) != 2 or not coordinate.isascii() or not coordinate.islower() or not coordinate.isalpha():
        return err("COORDINATE_SHAPE")
    column, row = ord(coordinate[0]) - 97, ord(coordinate[1]) - 97
    if row >= size or column >= size:
        return err("COORDINATE_RANGE")
    return ok({"pass": False, "row": row, "column": column, "board_size": size})


def _orthogonal(payload: dict[str, Any]) -> dict[str, Any]:
    size, row, column = payload["board_size"], payload["row"], payload["column"]
    if not all(_int(x) for x in (size, row, column)):
        return err("INTEGER_TYPE")
    if size < 1 or not (0 <= row < size and 0 <= column < size):
        return err("POINT_RANGE")
    return ok({"neighbors": [list(p) for p in _neighbors(size, (row, column))], "degree": len(_neighbors(size, (row, column))), "observed": False})


def _chain_or_liberty(payload: dict[str, Any], liberties: bool) -> dict[str, Any]:
    board, issue = _board(payload["board"])
    if issue:
        return err(issue)
    assert board is not None
    if payload["colour"] not in {"B", "W"}:
        return err("COLOUR_TOKEN")
    if not _point(payload["point"]) or not _inside(board, payload["point"]):
        return err("POINT_RANGE")
    point = tuple(payload["point"])
    if board[point[0]][point[1]] == ".":
        return err("EMPTY_ORIGIN")
    chain = _chain(board, point)
    if liberties:
        frontier = _liberties(board, chain)
        return ok({"chain": [list(p) for p in chain], "liberties": [list(p) for p in frontier], "liberty_count": len(frontier), "observed": False})
    return ok({"chain": [list(p) for p in chain], "stone_count": len(chain), "observed": False})


def _play(payload: dict[str, Any], suicide_mode: bool) -> dict[str, Any]:
    board, issue = _board(payload["board"])
    if issue:
        return err(issue)
    assert board is not None
    colour = payload["colour"]
    if colour not in {"B", "W"}:
        return err("COLOUR_TOKEN")
    if type(payload["allow_suicide"]) is not bool:
        return err("BOOLEAN_TYPE")
    move = payload["move"]
    if not _point(move) or not _inside(board, move):
        return err("POINT_RANGE")
    row, column = move
    if board[row][column] != ".":
        return err("OCCUPIED_POINT")
    board[row][column] = colour
    opponent = "W" if colour == "B" else "B"
    captured: set[tuple[int, int]] = set()
    for neighbour in _neighbors(len(board), (row, column)):
        if board[neighbour[0]][neighbour[1]] == opponent:
            chain = _chain(board, neighbour)
            if not _liberties(board, chain):
                captured.update(chain)
    for r, c in captured:
        board[r][c] = "."
    own = _chain(board, (row, column))
    suicidal = not _liberties(board, own)
    if suicide_mode and suicidal and not payload["allow_suicide"]:
        return err("SUICIDE")
    return ok({"board": ["".join(r) for r in board], "captured": [list(p) for p in sorted(captured)], "suicidal": suicidal, "ruleset_decision": False, "observed": False})


def _simple_ko(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["referee_decision"] is not False:
        return err("AUTHORITY_PRECLAIM")
    old, old_issue = _board(payload["two_plies_ago"])
    proposed, proposed_issue = _board(payload["proposed"])
    if old_issue or proposed_issue:
        return err(old_issue or proposed_issue or "BOARD_SHAPE")
    assert old is not None and proposed is not None
    if len(old) != len(proposed):
        return err("BOARD_SHAPE")
    if payload["next_colour"] not in {"B", "W"} or payload["policy"] != "simple_ko":
        return err("COLOUR_TOKEN")
    repeats = old == proposed
    return ok({"repeats_two_plies_ago": repeats, "permitted_under_declared_simple_ko": not repeats, "superko_evaluated": False, "referee_decision": False})


def _position_digest(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["identity_proof"] is not False:
        return err("IDENTITY_PRECLAIM")
    board, issue = _board(payload["board"])
    if issue:
        return err(issue)
    if payload["next_colour"] not in {"B", "W"}:
        return err("COLOUR_TOKEN")
    body = json.dumps({"board": payload["board"], "next_colour": payload["next_colour"], "ko_point": payload["ko_point"]}, sort_keys=True, separators=(",", ":"))
    return ok({"sha256": hashlib.sha256(body.encode()).hexdigest(), "identity_proof": False, "observed": False})


def _setup(payload: dict[str, Any]) -> dict[str, Any]:
    size = payload["board_size"]
    if not _int(size):
        return err("INTEGER_TYPE")
    for key in ("black", "white", "empty"):
        if not isinstance(payload[key], list):
            return err("ARRAY_TYPE")
    decoded: dict[str, list[str]] = {}
    for key in ("black", "white", "empty"):
        decoded[key] = []
        for coordinate in payload[key]:
            result = _coordinate({"operation": "sgf_coordinate", "board_size": size, "coordinate": coordinate})
            if not result["accepted"] or result["value"]["pass"]:
                return err("COORDINATE_RANGE")
            decoded[key].append(coordinate)
    flattened = decoded["black"] + decoded["white"] + decoded["empty"]
    if len(flattened) != len(set(flattened)):
        return err("SETUP_OVERLAP")
    return ok({"black": sorted(decoded["black"]), "white": sorted(decoded["white"]), "empty": sorted(decoded["empty"]), "player_identity_created": False})


def _moves(payload: dict[str, Any]) -> dict[str, Any]:
    size, moves = payload["board_size"], payload["moves"]
    if not _int(size) or not isinstance(moves, list):
        return err("MOVE_SHAPE")
    expected = "B"
    normalized = []
    for number, move in enumerate(moves, 1):
        if not isinstance(move, list) or len(move) != 2 or move[0] not in {"B", "W"}:
            return err("MOVE_SHAPE")
        if move[0] != expected:
            return err("COLOUR_ORDER")
        point = _coordinate({"operation": "sgf_coordinate", "board_size": size, "coordinate": move[1]})
        if not point["accepted"]:
            return err(point["error"] or "COORDINATE_RANGE")
        normalized.append({"number": number, "colour": move[0], "coordinate": move[1], "pass": point["value"]["pass"]})
        expected = "W" if expected == "B" else "B"
    return ok({"moves": normalized, "winner_inferred": False, "observed": False})


def _game_tree(payload: dict[str, Any]) -> dict[str, Any]:
    parents, root = payload["parents"], payload["root"]
    if root is None or not _int(root):
        return err("ROOT_MISSING")
    if not isinstance(parents, list) or not parents or not (0 <= root < len(parents)):
        return err("ROOT_MISSING")
    children = [[] for _ in parents]
    for node, parent in enumerate(parents):
        if parent is None:
            continue
        if isinstance(parent, list):
            return err("MULTIPLE_PARENTS")
        if not _int(parent) or not (0 <= parent < len(parents)):
            return err("ROOT_MISSING")
        children[parent].append(node)
    state = [0] * len(parents)
    def visit(node: int) -> bool:
        if state[node] == 1:
            return False
        if state[node] == 2:
            return True
        state[node] = 1
        if not all(visit(child) for child in children[node]):
            return False
        state[node] = 2
        return True
    if not visit(root) or any(value != 2 for value in state):
        return err("TREE_CYCLE")
    if parents[root] is not None:
        return err("ROOT_MISSING")
    depth = 0
    queue = deque([(root, 0)])
    while queue:
        node, current = queue.popleft()
        depth = max(depth, current)
        queue.extend((child, current + 1) for child in children[node])
    return ok({"node_count": len(parents), "children": children, "maximum_depth": depth, "is_dag": True, "move_quality_ranked": False})


def _variation(payload: dict[str, Any]) -> dict[str, Any]:
    children, path, root = payload["children"], payload["path"], payload["root"]
    if not isinstance(children, list) or not all(isinstance(row, list) for row in children) or not isinstance(path, list) or not _int(root):
        return err("TREE_SHAPE")
    visiting: set[int] = set()
    visited: set[int] = set()
    def acyclic(node: int) -> bool:
        if node in visiting:
            return False
        if node in visited:
            return True
        if not (0 <= node < len(children)):
            return False
        visiting.add(node)
        if not all(_int(child) and acyclic(child) for child in children[node]):
            return False
        visiting.remove(node); visited.add(node); return True
    if not acyclic(root):
        return err("TREE_CYCLE")
    node = root
    visited_path = [node]
    for index in path:
        if not _int(index) or index < 0 or index >= len(children[node]):
            return err("CHILD_RANGE")
        node = children[node][index]
        visited_path.append(node)
    return ok({"visited_nodes": visited_path, "leaf": node, "move_quality_ranked": False})


def _property(payload: dict[str, Any]) -> dict[str, Any]:
    value = payload["identifier"]
    if type(value) is not str or not re.fullmatch(r"[A-Z]{1,2}", value):
        return err("PROPERTY_ID")
    return ok({"identifier": value, "schema_only": True})


def _text_escape(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["private_preclaim"]:
        return err("PRIVATE_PRECLAIM")
    text = payload["text"]
    if type(text) is not str:
        return err("TEXT_TYPE")
    if text.endswith("\\"):
        return err("TRAILING_ESCAPE")
    decoded = text.replace("\\\n", "").replace("\\]", "]").replace("\\\\", "\\")
    return ok({"text": decoded, "cultural_meaning_interpreted": False, "observed": False})


def _result(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["infer_winner"]:
        return err("WINNER_PRECLAIM")
    value = payload["result"]
    if type(value) is not str:
        return err("TEXT_TYPE")
    if value.startswith("X+"):
        return err("RESULT_WINNER")
    if re.fullmatch(r"[BW]\+-.+", value):
        return err("RESULT_MARGIN")
    category = "unknown"
    if re.fullmatch(r"[BW]\+[RT]", value): category = "termination"
    elif re.fullmatch(r"[BW]\+\d+(?:\.\d+)?", value): category = "margin"
    elif value == "0": category = "draw"
    elif value == "Void": category = "void"
    return ok({"literal": value, "category": category, "winner_inferred": False, "observed": False})


def _komi(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["fairness_claim"]:
        return err("FAIRNESS_PRECLAIM")
    if payload["universal_rules_claim"]:
        return err("UNIVERSAL_RULE_PRECLAIM")
    value = payload["komi"]
    if type(value) is not str:
        return err("RATIONAL_TYPE")
    try:
        decimal = Decimal(value)
        if not decimal.is_finite():
            return err("RATIONAL_VALUE")
        fraction = Fraction(decimal)
    except (InvalidOperation, ValueError):
        return err("RATIONAL_VALUE")
    return ok({"declared_fraction": str(fraction), "ruleset_dependent": True, "observed": False})


def _time(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["observed"]:
        return err("OBSERVATION_PRECLAIM")
    value = payload["main_seconds"]
    if not _int(value):
        return err("INTEGER_TYPE")
    if value < 0:
        return err("NEGATIVE_TIME")
    if payload["scheme"] not in {"main", "byoyomi", "canadian"}:
        return err("TIME_CONTROL")
    return ok({"main_seconds": value, "scheme": payload["scheme"], "observed": False, "tournament_authority": False})


def _evidence(payload: dict[str, Any]) -> dict[str, Any]:
    claim = payload["claim"]
    roles = payload["available_roles"]
    if type(claim) is not str:
        return err("TEXT_TYPE")
    if not isinstance(roles, list) or not all(isinstance(role, str) for role in roles):
        return err("ARRAY_TYPE")
    if len(roles) != len(set(roles)):
        return err("DUPLICATE_ROLE")
    if claim == "real_identity" and not payload["synthetic"]:
        return err("REAL_IDENTITY_GATE")
    if claim == "publication" and not payload["synthetic"]:
        return err("PUBLICATION_GATE")
    required = {
        "source_rights": ["source", "rights"], "provenance": ["source", "custody"],
        "player_consent": ["player_consent"], "accessibility": ["manual_accessibility_evaluation"],
        "public_source": ["source", "reuse_authority"], "custody": ["author", "custodian"],
    }.get(claim, [])
    return ok({"required_roles": required, "missing_roles": [role for role in required if role not in roles], "external_claim_supported": False, "synthetic": payload["synthetic"]})


def _accessible(payload: dict[str, Any]) -> dict[str, Any]:
    if type(payload["language"]) is not str:
        return err("TEXT_TYPE")
    if payload["language"] != "en":
        return err("LANGUAGE_REVIEW_REQUIRED")
    board, issue = _board(payload["board"])
    if issue:
        return err(issue)
    assert board is not None
    rows, columns = payload["row_labels"], payload["column_labels"]
    if not isinstance(rows, list) or not isinstance(columns, list) or len(rows) != len(board) or len(columns) != len(board):
        return err("LABEL_REQUIRED")
    if any(type(label) is not str for label in rows + columns):
        return err("TEXT_TYPE")
    if any(any(ord(char) < 32 for char in label) for label in rows + columns):
        return err("CONTROL_CHARACTER")
    lines = ["  " + " ".join(columns)] + [f"{rows[i]} " + " ".join(row) for i, row in enumerate(payload["board"])]
    return ok({"lines": lines, "manual_evaluation": False, "accessibility_complete": False, "language": "en"})


def _authority(payload: dict[str, Any]) -> dict[str, Any]:
    return err("AUTHORITY_REFUSAL")


def evaluate(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return err("MAP_TYPE")
    operation = payload.get("operation")
    if type(operation) is not str or operation not in ALLOWED:
        return err("OPERATION")
    if set(payload) != ALLOWED[operation]:
        return err("FIELD_SET")
    handlers = {
        "sgf_coordinate": _coordinate,
        "orthogonal_neighbors": _orthogonal,
        "chain_component": lambda value: _chain_or_liberty(value, False),
        "liberty_frontier": lambda value: _chain_or_liberty(value, True),
        "capture_projection": lambda value: _play(value, False),
        "suicide_projection": lambda value: _play(value, True),
        "simple_ko": _simple_ko,
        "position_digest": _position_digest,
        "setup_partition": _setup,
        "move_sequence": _moves,
        "game_tree_dag": _game_tree,
        "variation_path": _variation,
        "property_identifier": _property,
        "text_escape": _text_escape,
        "result_token": _result,
        "komi_rational": _komi,
        "time_record": _time,
        "record_evidence": _evidence,
        "accessible_board": _accessible,
        "authority_boundary": _authority,
    }
    try:
        return handlers[operation](payload)
    except (KeyError, IndexError, TypeError, ValueError, ArithmeticError):
        return err("BOUNDED_INPUT")


def validate_against_freeze(payload: dict[str, Any], expected_acceptance: bool, expected_error: str | None) -> dict[str, Any]:
    before = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    observed = evaluate(payload)
    after = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    valid = observed["accepted"] is expected_acceptance and observed["error"] == expected_error and before == after and observed["external_credit"] is False
    return {"valid": valid, "input_unchanged": before == after, "observed": observed}


def main() -> int:
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    try:
        payload = strict_loads(args.input.read_text(encoding="utf-8"))
        result = evaluate(payload)
    except ValueError as exc:
        result = err(str(exc))
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))
    return 0 if result["accepted"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
