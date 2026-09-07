#!/usr/bin/env python3
"""Build the planning-only Elowen Cairn v688-v5 x1 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Elowen Cairn"
PHASE = "v688-v5"
SOURCE = "adadd367036e49cfb5c480f2aa0b598c164cac1c"
MERRIN_BASE = "612ec0a16fc75bd9e4dcdebd7d9bcb21432ab153"
MERRIN_X1_INITIAL = "8c1c83b3311e8527a82ccd931b39f924a14ce328"
MERRIN_X1 = "85617b39c876177842a2ae351373da1700b48a15"
MERRIN_EVIDENCE = "a1bc47a9dfbc31823dd1f25961c52e4c632617ff"
BRANCH = "codex/GHC-Family/elowen-cairn-v688-v5-full-tools"
BASE = ROOT / "docs" / "elowen-cairn" / PHASE
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

SOURCE_SEAL = {
    "proposals": 16230,
    "negatives": 83852,
    "methods": 93504,
    "failed_witnesses": 54700,
    "passing_witnesses": 85553,
    "open_gaps": 755,
    "exact_gates": 759,
}
ACTIVATION_BASELINE = {
    "proposals": 16230,
    "negatives": 83854,
    "methods": 93506,
    "failed_witnesses": 54702,
    "passing_witnesses": 85555,
    "open_gaps": 755,
    "exact_gates": 759,
}

BOUNDARY = (
    "Relational working language only; no consciousness, sentience, personhood, "
    "identity continuity, employment, qualification, independent agency, scientific, "
    "operational, professional, legal, cultural, affected-party, or Maori authority. "
    "Same-owner synthetic evidence is not independent reproduction. "
    "NOT_READY_FOR_STAGE_20. Maori concepts remain under Maori authority."
)

PROTECTED_GATES = [
    "empirical",
    "professional",
    "production",
    "deployment",
    "real_participants",
    "identity",
    "legal",
    "cultural",
    "affected_party",
    "maori_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_asi",
    "consciousness_personhood",
    "theory_of_everything",
    "proof_canon",
    "stage20",
]

SOURCES = [
    {
        "source_id": "SGF-FF4",
        "title": "SGF File Format FF[4]",
        "url": "https://www.red-bean.com/sgf/",
        "status": "stable",
        "use": "Text-only tree format, property, coordinate, and variation vocabulary only.",
        "nonconversion": "Not a real game record, observation, rules authority, or cultural authority.",
    },
    {
        "source_id": "SGFMILL-PYPI",
        "title": "sgfmill 1.1.1",
        "url": "https://pypi.org/project/sgfmill/",
        "status": "stable",
        "use": "Bounded SGF parsing, serialization, and synthetic board smoke vocabulary.",
        "nonconversion": "Package behavior is software evidence only.",
    },
    {
        "source_id": "NETWORKX-DAG",
        "title": "NetworkX directed acyclic graph documentation",
        "url": "https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.is_directed_acyclic_graph.html",
        "status": "current",
        "use": "Declared game-tree DAG comparison only.",
        "nonconversion": "No real game strategy, player outcome, or independent reproduction.",
    },
    {
        "source_id": "WCWIDTH-API",
        "title": "wcwidth public API",
        "url": "https://wcwidth.readthedocs.io/en/stable/api.html",
        "status": "current",
        "use": "Synthetic terminal-cell width calculations only.",
        "nonconversion": "No complete accessibility or affected-user evaluation.",
    },
    {
        "source_id": "AGA-RULES",
        "title": "American Go Association rules summary",
        "url": "https://www.usgo.org/content.aspx?club_id=454497&module_id=563542&page_id=22",
        "status": "current",
        "use": "Ruleset-specific terminology and explicit variation warnings only.",
        "nonconversion": "No universal rules claim, tournament authority, cultural interpretation, or adjudication.",
    },
]

OPERATION_SPECS = [
    ("sgf_coordinate", "synthetic SGF record registrar", "THOS Body", [
        "Go SGF coordinate maps the upper-left point", "Go SGF coordinate maps the lower-right nineteen-board point",
        "Go SGF coordinate maps a declared centre point", "Go SGF coordinate preserves column before row",
        "Go SGF coordinate preserves row after column", "Go SGF coordinate supports a bounded nine-board point",
        "Go SGF empty move remains an explicit pass", "Go SGF coordinate refuses one-letter input",
        "Go SGF coordinate refuses a point outside the declared board", "Go SGF coordinate refuses Boolean input",
    ]),
    ("orthogonal_neighbors", "Go board-topology analyst", "GMUT Mind", [
        "Go board corner has two orthogonal neighbours", "Go board opposite corner has two orthogonal neighbours",
        "Go board edge point has three orthogonal neighbours", "Go board centre point has four orthogonal neighbours",
        "Go board neighbour order remains deterministic", "Go board one-point topology has no neighbours",
        "Go board small-grid neighbour set remains bounded", "Go board neighbour query refuses negative row",
        "Go board neighbour query refuses out-of-range column", "Go board neighbour query refuses Boolean size",
    ]),
    ("chain_component", "Go board-topology analyst", "GMUT Mind", [
        "Go chain component finds one isolated black stone", "Go chain component joins a horizontal black pair",
        "Go chain component joins a vertical white pair", "Go chain component follows a bent same-colour chain",
        "Go chain component excludes diagonal contact", "Go chain component excludes opponent stones",
        "Go chain component preserves deterministic point order", "Go chain component refuses an empty starting point",
        "Go chain component refuses a ragged board", "Go chain component refuses an invalid colour token",
    ]),
    ("liberty_frontier", "Go board-topology analyst", "GMUT Mind", [
        "Go liberty frontier counts four liberties around an isolated centre stone", "Go liberty frontier counts two liberties at a corner",
        "Go liberty frontier deduplicates shared liberties", "Go liberty frontier excludes occupied neighbours",
        "Go liberty frontier follows the whole chain", "Go liberty frontier can be empty",
        "Go liberty frontier preserves coordinate order", "Go liberty frontier refuses an empty origin",
        "Go liberty frontier refuses an out-of-range point", "Go liberty frontier refuses a malformed board symbol",
    ]),
    ("capture_projection", "Go board-topology analyst", "THOS Body", [
        "Go capture projection removes one surrounded white stone", "Go capture projection removes a two-stone chain",
        "Go capture projection preserves a chain with one liberty", "Go capture projection can remove two separate chains",
        "Go capture projection leaves distant stones unchanged", "Go capture projection records captured coordinates deterministically",
        "Go capture projection does not score territory", "Go capture projection refuses an occupied move",
        "Go capture projection refuses a move outside the board", "Go capture projection refuses an unknown colour",
    ]),
    ("suicide_projection", "Go board-topology analyst", "THOS Body", [
        "Go suicide guard accepts a move with one liberty", "Go suicide guard accepts a move that captures first",
        "Go suicide guard refuses a surrounded noncapturing move", "Go suicide guard preserves the input board",
        "Go suicide guard distinguishes ruleset policy from observation", "Go suicide guard records no tournament ruling",
        "Go suicide guard handles a corner move", "Go suicide guard refuses an occupied point",
        "Go suicide guard refuses a ragged board", "Go suicide guard refuses Boolean allowance",
    ]),
    ("simple_ko", "Go board-topology analyst", "THOS Body", [
        "Go simple-ko guard detects exact two-ply board repetition", "Go simple-ko guard accepts a nonrepeating board",
        "Go simple-ko guard preserves next-player context", "Go simple-ko guard distinguishes simple ko from superko",
        "Go simple-ko guard treats pass as declared policy", "Go simple-ko guard compares complete board shape",
        "Go simple-ko guard remains ruleset-labelled", "Go simple-ko guard refuses mismatched board sizes",
        "Go simple-ko guard refuses invalid symbols", "Go simple-ko guard refuses a preclaimed referee decision",
    ]),
    ("position_digest", "Go board-topology analyst", "GMUT Mind", [
        "Go position digest binds board rows and next colour", "Go position digest distinguishes black and white stones",
        "Go position digest changes with the next player", "Go position digest preserves empty intersections",
        "Go position digest binds declared ko context", "Go position digest is deterministic for identical input",
        "Go position digest is not a player identity proof", "Go position digest refuses a ragged board",
        "Go position digest refuses an invalid next colour", "Go position digest refuses private identity promotion",
    ]),
    ("setup_partition", "synthetic SGF record registrar", "THOS Body", [
        "Go SGF setup keeps black and white stones disjoint", "Go SGF setup keeps explicit empty points disjoint",
        "Go SGF setup sorts coordinates deterministically", "Go SGF setup permits an empty black set",
        "Go SGF setup permits an empty white set", "Go SGF setup preserves a declared handicap placeholder",
        "Go SGF setup creates no player identity", "Go SGF setup refuses duplicate colour occupancy",
        "Go SGF setup refuses an out-of-range point", "Go SGF setup refuses a nonarray property value",
    ]),
    ("move_sequence", "synthetic SGF record registrar", "THOS Body", [
        "Go move sequence alternates black then white", "Go move sequence preserves an explicit pass",
        "Go move sequence records setup before play", "Go move sequence retains move numbers",
        "Go move sequence preserves branch-local order", "Go move sequence permits a bounded empty sequence",
        "Go move sequence does not infer a winner", "Go move sequence refuses repeated colour without a setup reason",
        "Go move sequence refuses an out-of-range point", "Go move sequence refuses a malformed move pair",
    ]),
    ("game_tree_dag", "game-tree variation auditor", "GMUT Mind", [
        "Go SGF game tree accepts one root", "Go SGF game tree accepts one linear branch",
        "Go SGF game tree accepts two sibling variations", "Go SGF game tree preserves child order",
        "Go SGF game tree reports maximum declared depth", "Go SGF game tree keeps node identifiers local",
        "Go SGF game tree remains a record topology", "Go SGF game tree refuses a cycle",
        "Go SGF game tree refuses two parents for one node", "Go SGF game tree refuses a missing root",
    ]),
    ("variation_path", "game-tree variation auditor", "GMUT Mind", [
        "Go SGF variation path selects the first child", "Go SGF variation path selects a second sibling",
        "Go SGF variation path reaches a nested leaf", "Go SGF variation path preserves index order",
        "Go SGF variation path can remain at the root", "Go SGF variation path records the visited nodes",
        "Go SGF variation path does not rank move quality", "Go SGF variation path refuses a missing child index",
        "Go SGF variation path refuses a negative child index", "Go SGF variation path refuses a cyclic child table",
    ]),
    ("property_identifier", "synthetic SGF record registrar", "THOS Body", [
        "Go SGF property identifier accepts FF", "Go SGF property identifier accepts GM",
        "Go SGF property identifier accepts a single B", "Go SGF property identifier accepts a single W",
        "Go SGF property identifier accepts composed uppercase letters", "Go SGF property identifier preserves literal spelling",
        "Go SGF property identifier remains schema-only", "Go SGF property identifier refuses lowercase letters",
        "Go SGF property identifier refuses digits", "Go SGF property identifier refuses an empty token",
    ]),
    ("text_escape", "synthetic SGF record registrar", "THOS Body", [
        "Go SGF text escape preserves escaped closing bracket", "Go SGF text escape preserves escaped backslash",
        "Go SGF text escape joins a declared soft line break", "Go SGF text escape preserves ordinary Unicode text",
        "Go SGF text escape preserves an empty value", "Go SGF text escape remains byte-domain explicit",
        "Go SGF text escape does not interpret cultural meaning", "Go SGF text escape refuses a trailing escape",
        "Go SGF text escape refuses nontext input", "Go SGF text escape refuses a private transcript preclaim",
    ]),
    ("result_token", "game-tree variation auditor", "GMUT Mind", [
        "Go result token represents a black resignation", "Go result token represents a white time result",
        "Go result token represents a half-point margin", "Go result token represents a draw marker",
        "Go result token represents a void marker", "Go result token preserves an unknown textual result",
        "Go result token refuses a negative numeric margin", "Go result token refuses an unsupported winner code",
        "Go result token refuses Boolean input", "Go result token refuses winner inference from board shape",
    ]),
    ("komi_rational", "game-tree variation auditor", "GMUT Mind", [
        "Go komi field represents an exact half point", "Go komi field represents an integer value",
        "Go komi field represents a signed declared value", "Go komi field preserves decimal-to-rational equivalence",
        "Go komi field labels its ruleset dependency", "Go komi field remains unobserved",
        "Go komi field refuses nonfinite text", "Go komi field refuses Boolean input",
        "Go komi field refuses a tournament fairness preclaim", "Go komi field refuses universal-rules promotion",
    ]),
    ("time_record", "game-tree variation auditor", "THOS Body", [
        "Go time record represents nonnegative main time", "Go time record represents bounded overtime periods",
        "Go time record represents remaining stones", "Go time record preserves a zero clock",
        "Go time record labels its time-control scheme", "Go time record remains unobserved",
        "Go time record refuses negative seconds", "Go time record refuses Boolean seconds",
        "Go time record refuses an unknown time-control shape", "Go time record refuses a live tournament preclaim",
    ]),
    ("record_evidence", "provenance accessibility and authority steward", "Freed ID and CBR Heart", [
        "Go record evidence exposes absent source and rights roles", "Go record evidence represents complete synthetic provenance labels",
        "Go record evidence keeps player consent absent", "Go record evidence keeps accessibility evaluation absent",
        "Go record evidence represents a public-source label without reuse authority", "Go record evidence separates authorship from custody",
        "Go record evidence refuses real-person identity promotion", "Go record evidence reserves publication authority",
        "Go record evidence refuses duplicate role labels", "Go record evidence refuses Boolean claim class",
    ]),
    ("accessible_board", "provenance accessibility and authority steward", "Freed ID and CBR Heart", [
        "Go accessible board represents labelled row order", "Go accessible board represents labelled column order",
        "Go accessible board represents black white and empty tokens", "Go accessible board represents terminal-cell widths",
        "Go accessible board represents a compact text alternative", "Go accessible board refuses a ragged row",
        "Go accessible board refuses an unlabeled projection", "Go accessible board refuses a control character",
        "Go accessible board refuses Boolean language", "Go accessible board reserves unreviewed language authority",
    ]),
    ("authority_boundary", "provenance accessibility and authority steward", "Freed ID and CBR Heart", [
        "Go authority boundary refuses professional rank certification", "Go authority boundary refuses tournament adjudication",
        "Go authority boundary refuses real-player identity proof", "Go authority boundary refuses copyright ownership determination",
        "Go authority boundary refuses cultural interpretation", "Go authority boundary refuses accessibility-complete promotion",
        "Go authority boundary refuses consciousness inference", "Go authority boundary reserves affected-player acceptance",
        "Go authority boundary reserves Maori wording and data governance", "Go authority boundary reserves Stage 20 promotion",
    ]),
]

ERRORS: dict[str, list[str | None]] = {
    "sgf_coordinate": [None] * 7 + ["COORDINATE_SHAPE", "COORDINATE_RANGE", "TEXT_TYPE"],
    "orthogonal_neighbors": [None] * 7 + ["POINT_RANGE", "POINT_RANGE", "INTEGER_TYPE"],
    "chain_component": [None] * 7 + ["EMPTY_ORIGIN", "BOARD_SHAPE", "COLOUR_TOKEN"],
    "liberty_frontier": [None] * 7 + ["EMPTY_ORIGIN", "POINT_RANGE", "BOARD_SYMBOL"],
    "capture_projection": [None] * 7 + ["OCCUPIED_POINT", "POINT_RANGE", "COLOUR_TOKEN"],
    "suicide_projection": [None] * 7 + ["OCCUPIED_POINT", "BOARD_SHAPE", "BOOLEAN_TYPE"],
    "simple_ko": [None] * 7 + ["BOARD_SHAPE", "BOARD_SYMBOL", "AUTHORITY_PRECLAIM"],
    "position_digest": [None] * 7 + ["BOARD_SHAPE", "COLOUR_TOKEN", "IDENTITY_PRECLAIM"],
    "setup_partition": [None] * 7 + ["SETUP_OVERLAP", "COORDINATE_RANGE", "ARRAY_TYPE"],
    "move_sequence": [None] * 7 + ["COLOUR_ORDER", "COORDINATE_RANGE", "MOVE_SHAPE"],
    "game_tree_dag": [None] * 7 + ["TREE_CYCLE", "MULTIPLE_PARENTS", "ROOT_MISSING"],
    "variation_path": [None] * 7 + ["CHILD_RANGE", "CHILD_RANGE", "TREE_CYCLE"],
    "property_identifier": [None] * 7 + ["PROPERTY_ID", "PROPERTY_ID", "PROPERTY_ID"],
    "text_escape": [None] * 7 + ["TRAILING_ESCAPE", "TEXT_TYPE", "PRIVATE_PRECLAIM"],
    "result_token": [None] * 6 + ["RESULT_MARGIN", "RESULT_WINNER", "TEXT_TYPE", "WINNER_PRECLAIM"],
    "komi_rational": [None] * 6 + ["RATIONAL_VALUE", "RATIONAL_TYPE", "FAIRNESS_PRECLAIM", "UNIVERSAL_RULE_PRECLAIM"],
    "time_record": [None] * 6 + ["NEGATIVE_TIME", "INTEGER_TYPE", "TIME_CONTROL", "OBSERVATION_PRECLAIM"],
    "record_evidence": [None] * 6 + ["REAL_IDENTITY_GATE", "PUBLICATION_GATE", "DUPLICATE_ROLE", "TEXT_TYPE"],
    "accessible_board": [None] * 5 + ["BOARD_SHAPE", "LABEL_REQUIRED", "CONTROL_CHARACTER", "TEXT_TYPE", "LANGUAGE_REVIEW_REQUIRED"],
    "authority_boundary": ["AUTHORITY_REFUSAL"] * 10,
}

OUTCOME_OVERRIDES: dict[str, list[str]] = {
    "result_token": ["represented"] * 6 + ["completed"] * 4,
    "komi_rational": ["represented"] * 6 + ["completed"] * 4,
    "time_record": ["represented"] * 6 + ["completed"] * 4,
    "record_evidence": ["open_gap", "represented", "open_gap", "open_gap", "represented", "represented", "exact_gate", "exact_gate", "completed", "completed"],
    "accessible_board": ["represented"] * 5 + ["completed"] * 4 + ["exact_gate"],
    "authority_boundary": ["completed"] * 7 + ["exact_gate"] * 3,
}

SKILLS = [
    "ghc-family-sgf-coordinate-profile",
    "ghc-family-go-neighbor-topology",
    "ghc-family-go-chain-liberties",
    "ghc-family-go-capture-projection",
    "ghc-family-go-ko-repetition-guard",
    "ghc-family-sgf-game-tree-structure",
    "ghc-family-sgf-property-escaping",
    "ghc-family-go-result-timing-reservation",
    "ghc-family-go-record-evidence-boundary",
    "ghc-family-go-accessible-board",
]

RUNNERS = [
    "ghc_family_go_board_topology.py",
    "ghc_family_go_capture_rules.py",
    "ghc_family_sgf_tree_records.py",
    "ghc_family_go_evidence_access.py",
    "ghc_family_go_contract_suite.py",
]

PACKAGES = [
    {
        "name": "sgfmill", "version": "1.1.1", "wheel": "sgfmill-1.1.1-py3-none-any.whl",
        "sha256": "759cd843eba647875931d3a10eb329362087b9832f6b49ee85cf8948b0608b3d",
        "url": "https://files.pythonhosted.org/packages/a0/ef/cd39e8db4385260b6f2e021dd8908e8f5167bfddce238bdea0e82b2f59c6/sgfmill-1.1.1-py3-none-any.whl",
        "source": "PyPI", "dependencies": [], "use": "synthetic SGF parse, tree, serialization, and board smokes",
    },
    {
        "name": "networkx", "version": "3.6.1", "wheel": "networkx-3.6.1-py3-none-any.whl",
        "sha256": "d47fbf302e7d9cbbb9e2555a0d267983d2aa476bac30e90dfbe5669bd57f3762",
        "url": "https://files.pythonhosted.org/packages/9e/c9/b2622292ea83fbb4ec318f5b9ab867d0a28ab43c5717bb85b0a5f6b3b0a4/networkx-3.6.1-py3-none-any.whl",
        "source": "PyPI", "dependencies": [], "use": "declared game-tree DAG comparison",
    },
    {
        "name": "wcwidth", "version": "0.8.3", "wheel": "wcwidth-0.8.3-py3-none-any.whl",
        "sha256": "d5b73dba6158a595ec9370350e7f2637bcac8d6c5e4fde34f30fcffb6103a5e4",
        "url": "https://files.pythonhosted.org/packages/c4/0e/57f6bb3024a597b2e8ec4aee710ffe62ddc95af2e2bb1ee7a7abdc22c68c/wcwidth-0.8.3-py3-none-any.whl",
        "source": "PyPI", "dependencies": [], "use": "synthetic terminal-cell width smokes",
    },
]

STARTUP_FAILURES = [
    ("EC6885-START-N001", "An overbroad phase-bank receipt search descended into Merrin's isolated package environment and exceeded the display bound.", "Use the exact observed canonical and route-overlay paths only."),
    ("EC6885-START-N002", "The first Git cat-file batch verifier wrote all requests before draining stdout and deadlocked on the pipe buffer.", "Use subprocess communication that drains stdin and stdout concurrently."),
    ("EC6885-START-N003", "The first manifest replay treated committed placeholder anchor labels as executable revisions and reported all bindings missing.", "Bind each manifest to the exact lifecycle revision recorded by the canonical receipt."),
    ("EC6885-START-N004", "A combined multi-term Git grep exceeded its execution window while the wrapper projected only stdout and hid session metadata.", "Stop only the attributable process tree and query the already-built bounded proposal inventory in memory."),
    ("EC6885-START-N005", "The first thousand-line activation-baton window exceeded the display token budget.", "Read smaller contiguous overlapping windows through the explicit EOF marker."),
    ("EC6885-START-N006", "The first final 670-line baton window exceeded its display token budget.", "Reread the missing Method Flow interval in two smaller bounded windows."),
    ("EC6885-START-N007", "The first raw authorization-state display was truncated before all fields were visible.", "Read the same immutable file in bounded contiguous line windows through EOF."),
    ("EC6885-START-N008", "PowerShell object-mode JSON conversion refused a valid empty-string key in Merrin's frozen adverse fixture.", "Use Python's standards-compliant JSON parser for that exact projection."),
    ("EC6885-X1-N009", "The first x1 syntax preflight found a mismatched bracket in the staged-blob test f-string.", "Correct only the malformed f-string and rerun the Python compile dependency."),
    ("EC6885-X1-N010", "The first atomic syntax-fix patch used an incorrect wrapped overview context and was rejected without writing.", "Inspect the exact lines and apply smaller verified patch hunks."),
    ("EC6885-X1-N011", "The first x1 build could not UTF-8 encode an inherited lone-surrogate adverse fixture while hashing inputs with ensure_ascii disabled.", "Canonicalize all compared JSON inputs with deterministic ASCII escaping before hashing."),
    ("EC6885-X1-N012", "The first workflow-plan refinement passed nineteen of twenty checks but applied its older ten-runner minimum to the current five-runner release profile.", "Retain the failed aggregate and bind the unchanged five-runner plan to the dedicated current release-profile validation."),
    ("EC6885-X1-N013", "The first 3010-versus-2999 proposal-path comparison crossed its output window while its wrapper omitted session metadata.", "Reuse Merrin's observed selection rule: every exact-source path containing proposal, with bounded type-specific parsing."),
    ("EC6885-X1-N014", "The follow-up process audit called Get-Process with an empty identifier array after the comparison process had already exited.", "Materialize and count process identifiers before invoking an exact-ID process query."),
]


def git(*args: str, input_bytes: bytes | None = None) -> bytes:
    proc = subprocess.run(["git", *args], cwd=ROOT, input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value.replace("\r\n", "\n").encode("utf-8"))


def sha_json(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")).hexdigest()


def token_set(text: str) -> frozenset[str]:
    return frozenset(re.findall(r"[a-z0-9]+", text.lower()))


def source_proposal_inventory() -> dict[str, Any]:
    paths = [p for p in git("ls-tree", "-r", "--name-only", SOURCE).decode("utf-8").splitlines() if "proposal" in p.lower()]
    query = b"".join(f"{SOURCE}:{p}\n".encode("utf-8") for p in paths)
    batch = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT, input=query, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if batch.returncode:
        raise RuntimeError(batch.stderr.decode("utf-8", "replace"))
    pos = 0
    titles: list[dict[str, str]] = []
    input_hashes: set[str] = set()
    parse_failures: list[dict[str, str]] = []

    def walk(value: Any, path: str) -> None:
        if isinstance(value, dict):
            title = next((value.get(key) for key in ("title", "hypothesis", "name") if isinstance(value.get(key), str) and value.get(key).strip()), None)
            if isinstance(title, str) and title.strip():
                identifier = value.get("proposal_id", value.get("id", value.get("task_id", "")))
                titles.append({"proposal_id": str(identifier), "title": title.strip(), "path": path})
            for key in ("input", "frozen_input", "effective_input", "complete_input"):
                if key in value and isinstance(value[key], (dict, list)):
                    input_hashes.add(sha_json(value[key]))
            for child in value.values():
                walk(child, path)
        elif isinstance(value, list):
            for child in value:
                walk(child, path)

    for path in paths:
        nl = batch.stdout.find(b"\n", pos)
        if nl < 0:
            parse_failures.append({"path": path, "error": "missing_batch_header"})
            break
        header = batch.stdout[pos:nl].decode("utf-8", "replace")
        pos = nl + 1
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            parse_failures.append({"path": path, "error": header})
            continue
        size = int(parts[2])
        data = batch.stdout[pos:pos + size]
        pos += size + 1
        if path.endswith(".json"):
            try:
                walk(json.loads(data.decode("utf-8")), path)
            except Exception as exc:
                parse_failures.append({"path": path, "error": str(exc)})
        elif path.endswith((".md", ".txt", ".html", ".csv", ".jsonl")):
            try:
                text = data.decode("utf-8")
                for line in text.splitlines():
                    if line.startswith(("#", "|")) and re.search(r"(?:\bgo\b|sgf|goban|board|libert|capture|\bko\b|variation|game.tree)", line, re.I):
                        titles.append({"proposal_id": "", "title": line.strip(), "path": path})
            except UnicodeError as exc:
                parse_failures.append({"path": path, "error": str(exc)})
    return {
        "path_count": len(paths),
        "title_records": titles,
        "input_hashes": sorted(input_hashes),
        "parse_failures": parse_failures,
    }


def fixture_for(operation: str, index: int) -> dict[str, Any]:
    size = [9, 13, 19][index % 3]
    coord = ["aa", "ss", "jj", "as", "sa", "dd", "", "a", "tt", True][index]
    board = [".....", ".BB..", ".BW..", ".....", "....."]
    if operation == "sgf_coordinate":
        return {"operation": operation, "board_size": 19 if index != 5 else 9, "coordinate": coord}
    if operation == "orthogonal_neighbors":
        points = [(0, 0), (size - 1, size - 1), (0, 2), (2, 2), (1, 2), (0, 0), (1, 1), (-1, 0), (0, size), (0, 0)]
        value = {"operation": operation, "board_size": size, "row": points[index][0], "column": points[index][1]}
        if index == 9:
            value["board_size"] = True
        return value
    if operation in {"chain_component", "liberty_frontier"}:
        value = {"operation": operation, "board": board, "point": [1, 1], "colour": "B"}
        if index == 1:
            value["point"] = [1, 2]
        if index == 2:
            value.update({"point": [2, 2], "colour": "W"})
        if index == 5:
            value["point"] = [2, 2]
        if index == 7:
            value["point"] = [0, 0]
        if index == 8:
            value["board"] = ["...", ".."] if operation == "chain_component" else board
            value["point"] = [99, 0] if operation == "liberty_frontier" else value["point"]
        if index == 9:
            value["colour"] = "X" if operation == "chain_component" else "B"
            if operation == "liberty_frontier":
                value["board"] = ["..X", "...", "..."]
                value["point"] = [0, 0]
        return value
    if operation in {"capture_projection", "suicide_projection"}:
        value = {"operation": operation, "board": [".B.", "BWB", "..."], "move": [2, 1], "colour": "B", "allow_suicide": False}
        if index in {2, 4, 5, 6}:
            value["board"] = ["...", ".W.", "..."]
            value["move"] = [0, 0]
        if index == 7:
            value["move"] = [1, 1]
        if index == 8:
            value["move"] = [9, 9]
            if operation == "suicide_projection":
                value["board"] = ["...", ".."]
                value["move"] = [0, 0]
        if index == 9:
            if operation == "capture_projection":
                value["colour"] = "X"
            else:
                value["allow_suicide"] = "false"
        return value
    if operation == "simple_ko":
        value = {"operation": operation, "two_plies_ago": ["BW", "WB"], "proposed": ["BW", "WB"], "next_colour": "B", "policy": "simple_ko", "referee_decision": False}
        if index == 1:
            value["proposed"] = ["BB", "WB"]
        if index == 7:
            value["proposed"] = ["BWB"]
        if index == 8:
            value["proposed"] = ["BX", "WB"]
        if index == 9:
            value["referee_decision"] = True
        return value
    if operation == "position_digest":
        value = {"operation": operation, "board": ["B..", ".W.", "..."], "next_colour": "B", "ko_point": None, "identity_proof": False}
        if index == 2:
            value["next_colour"] = "W"
        if index == 4:
            value["ko_point"] = [1, 0]
        if index == 7:
            value["board"] = ["...", ".."]
        if index == 8:
            value["next_colour"] = "X"
        if index == 9:
            value["identity_proof"] = True
        return value
    if operation == "setup_partition":
        value = {"operation": operation, "board_size": 19, "black": ["aa"], "white": ["bb"], "empty": ["cc"]}
        if index == 3:
            value["black"] = []
        if index == 4:
            value["white"] = []
        if index == 7:
            value["white"] = ["aa"]
        if index == 8:
            value["black"] = ["tt"]
        if index == 9:
            value["black"] = "aa"
        return value
    if operation == "move_sequence":
        moves: Any = [["B", "aa"], ["W", "bb"]]
        if index == 1:
            moves = [["B", ""]]
        if index == 5:
            moves = []
        if index == 7:
            moves = [["B", "aa"], ["B", "bb"]]
        if index == 8:
            moves = [["B", "tt"]]
        if index == 9:
            moves = [["B"]]
        return {"operation": operation, "board_size": 19, "moves": moves}
    if operation == "game_tree_dag":
        parents: Any = [None, 0, 0]
        if index == 0:
            parents = [None]
        if index == 1:
            parents = [None, 0, 1]
        if index == 7:
            parents = [1, 0]
        if index == 8:
            parents = [None, [0, 1]]
        if index == 9:
            parents = [1, 0]
        return {"operation": operation, "parents": parents, "root": 0 if index != 9 else None}
    if operation == "variation_path":
        children: Any = [[1, 2], [3], [], []]
        path: Any = [0]
        if index == 1:
            path = [1]
        if index == 2:
            path = [0, 0]
        if index == 4:
            path = []
        if index == 7:
            path = [3]
        if index == 8:
            path = [-1]
        if index == 9:
            children = [[1], [0]]
            path = [0, 0]
        return {"operation": operation, "children": children, "path": path, "root": 0}
    if operation == "property_identifier":
        return {"operation": operation, "identifier": ["FF", "GM", "B", "W", "C", "AP", "SZ", "ff", "A1", ""][index]}
    if operation == "text_escape":
        return {"operation": operation, "text": [r"a\]b", r"a\\b", "a\\\nb", "kō", "", "plain", "meaning-reserved", "tail\\", True, "private transcript"][index], "private_preclaim": index == 9}
    if operation == "result_token":
        return {"operation": operation, "result": ["B+R", "W+T", "B+0.5", "0", "Void", "?", "B+-1", "X+R", True, "infer"][index], "infer_winner": index == 9}
    if operation == "komi_rational":
        return {"operation": operation, "komi": ["0.5", "7", "-0.5", "6.50", "7.5", "0", "nan", True, "7.5", "7.5"][index], "fairness_claim": index == 8, "universal_rules_claim": index == 9}
    if operation == "time_record":
        return {"operation": operation, "main_seconds": [3600, 0, 600, 1, 300, 30, -1, True, 300, 300][index], "scheme": ["main", "byoyomi", "canadian", "main", "byoyomi", "main", "main", "main", "unknown", "live"][index], "observed": index == 9}
    if operation == "record_evidence":
        claims = ["source_rights", "provenance", "player_consent", "accessibility", "public_source", "custody", "real_identity", "publication", "kinetics", True]
        roles = [[], ["source", "custody"], [], [], ["source"], ["author", "custodian"], [], ["source", "rights"], ["source", "source"], []]
        return {"operation": operation, "claim": claims[index], "available_roles": roles[index], "synthetic": index not in {6, 7}}
    if operation == "accessible_board":
        value = {"operation": operation, "board": ["B.W", ".B.", "W.."], "row_labels": ["1", "2", "3"], "column_labels": ["A", "B", "C"], "language": "en", "manual_evaluation": False}
        if index == 5:
            value["board"] = ["...", ".."]
        if index == 6:
            value["row_labels"] = []
        if index == 7:
            value["column_labels"] = ["A\u0007", "B", "C"]
        if index == 8:
            value["language"] = True
        if index == 9:
            value["language"] = "mi"
        return value
    if operation == "authority_boundary":
        claims = ["professional_rank", "tournament_adjudication", "real_player_identity", "copyright_ownership", "cultural_interpretation", "accessibility_complete", "consciousness", "affected_player_acceptance", "maori_data_governance", "stage20"]
        return {"operation": operation, "claim": claims[index], "authority_present": False, "synthetic": True}
    raise KeyError(operation)


def outcome_for(operation: str, index: int) -> str:
    return OUTCOME_OVERRIDES.get(operation, ["completed"] * 10)[index]


def proposals() -> list[dict[str, Any]]:
    rows = []
    number = 1
    source_by_operation = {
        "sgf_coordinate": ["SGF-FF4", "SGFMILL-PYPI"], "setup_partition": ["SGF-FF4", "SGFMILL-PYPI"],
        "move_sequence": ["SGF-FF4", "SGFMILL-PYPI"], "game_tree_dag": ["SGF-FF4", "NETWORKX-DAG"],
        "variation_path": ["SGF-FF4", "NETWORKX-DAG"], "property_identifier": ["SGF-FF4"],
        "text_escape": ["SGF-FF4"], "accessible_board": ["WCWIDTH-API"],
        "simple_ko": ["AGA-RULES"], "komi_rational": ["AGA-RULES"],
    }
    for operation, practice, pillar, titles in OPERATION_SPECS:
        for index, title in enumerate(titles):
            outcome = outcome_for(operation, index)
            error = ERRORS[operation][index]
            approval = "exact_approval_needed" if outcome == "exact_gate" else ("candidate" if outcome in {"represented", "open_gap"} else "safe_now")
            rows.append({
                "schema": "ghc.family.frozen-go-sgf-contract.v1",
                "proposal_id": f"EC6885-N{number:03d}",
                "title": title,
                "hypothesis": title + " within the exact synthetic fixture and declared software boundary.",
                "null_or_failure_condition": "Any acceptance/error mismatch, input mutation, unexpected exception, nondeterministic output, or protected-claim promotion is a failed witness.",
                "approval_class": approval,
                "execution_lane": "x2_only" if outcome != "exact_gate" else "x2_exact_gate_unexecuted",
                "source_refs": source_by_operation.get(operation, ["SGF-FF4"]),
                "current_official_or_primary_source_needs": "Use listed sources for vocabulary and software contracts only; no observation or authority conversion.",
                "concrete_artifact": f"docs/elowen-cairn/{PHASE}/x2/contracts/{number:03d}.json",
                "falsifier_or_acceptance_gate": "Compare the complete accepted/error class, deterministic output, unchanged input, declared disposition, and all protected boundaries.",
                "rollback_or_recovery": "Retain the failed fixture and stop selecting the candidate; correct only the owner implementation or leave the gap/gate open.",
                "protected_gates": PROTECTED_GATES,
                "expected_execution_disposition": outcome,
                "source_kind": "synthetic",
                "source_status": "current",
                "operation": operation,
                "practice": practice,
                "pillar": pillar,
                "input": fixture_for(operation, index),
                "expected_acceptance": error is None,
                "expected_error": error,
                "external_credit": False,
            })
            number += 1
    if number != 201:
        raise AssertionError(number)
    return rows


def startup_method_flow() -> dict[str, Any]:
    methods = []
    witnesses = []
    events = []
    for index, (negative, failure, recovery) in enumerate(STARTUP_FAILURES, 1):
        method_id = f"EC6885-START-M{index:03d}"
        methods.append({
            "method_id": method_id,
            "title": recovery.rstrip("."),
            "failure_signature": failure,
            "trigger_preconditions": ["The matching startup read, projection, process, or schema operation is required."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": recovery,
            "validation_witness_ids": [f"{method_id}-FAIL", f"{method_id}-PASS"],
            "recurrence_guard": recovery,
            "rollback": "Stop the failed attempt, preserve its record, and keep source, sibling, global, and route state unchanged.",
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": PROTECTED_GATES,
            "retained_negative_ids": [negative],
            "scope_boundary": "Startup and read-only source verification only; no x2, external, scientific, professional, or route credit.",
        })
        for result, observed in (("fail", failure), ("pass", recovery)):
            witnesses.append({
                "witness_id": f"{method_id}-{result.upper()}", "method_id": method_id,
                "procedure": "Bounded startup/source verification", "scope": "Elowen v688-v5 startup",
                "expected": "An attributable complete read-only result", "observed": observed,
                "result": result, "same_owner_only": True, "independent_reproduction": False,
                "retained_negative_ids": [negative], "boundary": BOUNDARY,
            })
        events.extend([
            {"method_id": method_id, "from": "observed", "to": "candidate", "note": "Failure retained before recovery."},
            {"method_id": method_id, "from": "candidate", "to": "validated", "note": "Bounded recovery passed."},
            {"method_id": method_id, "from": "validated", "to": "preferred", "note": "Recommended only for matching preconditions."},
        ])
    return {
        "schema": "ghc.family.method-flow-state.v1", "phase": PHASE, "owner": OWNER,
        "identity_boundary": BOUNDARY, "execution_authority": "owner_self_scoped_delta",
        "source_commit": SOURCE, "final_commit": None, "repository_scan": False,
        "module_scan": False, "cross_lane_scan": False, "unchanged_history_scan": False,
        "sibling_lane_mutation": False, "changed_file_allowlist": [], "module_allowlist": [],
        "exact_pushed_head_required": True, "methods": methods, "witnesses": witnesses,
        "state_events": events, "recommendations": [],
        "counts": {"methods": len(methods), "witnesses": len(witnesses), "state_events": len(events), "recommendations": 0, "witness_results": {"fail": len(methods), "pass": len(methods)}},
        "boundary": BOUNDARY,
    }


def approval_portfolio() -> dict[str, Any]:
    def tasks(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
        return [{"task_id": f"EC6885-{prefix}-{i:03d}", "lane": lane, "proposal_ref": f"EC6885-N{((i - 1) % 200) + 1:03d}", "planned_action": f"Bounded {lane} witness {i}", "expected_execution_disposition": "completed" if lane in {"safe_now", "clean_fix_refine"} else "represented", "protected_gates": PROTECTED_GATES, "rollback": "Retain any failure and stop the owner-local action."} for i in range(1, count + 1)]
    exact = [{"packet_id": f"EC6885-EXACT-{i:03d}", "state": "unexecuted", "approval_class": "exact_approval_needed", "scope": "Real participant, professional, publication, deployment, identity, legal, cultural, affected-party, or Maori-authority action remains unspecified.", "protected_gates": PROTECTED_GATES, "rollback": "Leave unexecuted."} for i in range(1, 51)]
    blocked = [{"packet_id": f"EC6885-BLOCKED-{i:03d}", "state": "unexecuted", "approval_class": "blocked", "scope": "False evidence promotion, private publication, identity replacement, destructive sibling mutation, or protected-gate bypass.", "protected_gates": PROTECTED_GATES, "rollback": "Refuse and preserve the record."} for i in range(1, 31)]
    return {
        "schema": "ghc.family.release-profile-portfolio.v1", "phase": PHASE, "owner": OWNER,
        "safe_now": tasks("SAFE", 300, "safe_now"), "candidates": tasks("CAND", 250, "candidate"),
        "clean_fix_refine": tasks("CFR", 300, "clean_fix_refine"), "exact_packets": exact,
        "blocked_packets": blocked, "destructive_cleanup_planned": False,
        "planning_only": True, "execution_credit": 0,
    }


def tool_plan() -> dict[str, Any]:
    next_ideas = [
        "go-board-symmetry-canonicalizer", "sgf-collection-boundary", "ruleset-difference-ledger",
        "go-problem-variation-pruner", "stone-chain-uncertainty-envelope", "sgf-date-normalization",
        "go-comment-rights-reservation", "accessible-variation-summary", "board-diagram-fixity",
        "go-record-correction-lineage",
    ]
    return {
        "schema": "ghc.family.tool-package-plan.v1", "owner": OWNER, "phase": PHASE,
        "skills": [{"name": name, "state": "planned_x2", "official_initializer_required": True, "global_collision_must_be_absent": True, "accepting_and_rejecting_smoke_required": True} for name in SKILLS],
        "runners": [{"name": name, "state": "planned_x2", "family_current": True, "global_collision_must_be_absent": True, "accepting_and_rejecting_smoke_required": True} for name in RUNNERS],
        "packages": PACKAGES,
        "next_owner_skill_ideas": next_ideas,
        "next_owner_runner_ideas": [name.replace("-", "_") + "_runner" for name in next_ideas],
        "global_promotions": {"skills": 10, "runners": 5, "collision_policy": "refuse_existing_destination", "overwrite": False},
        "planning_only": True, "execution_credit": 0, "boundary": BOUNDARY,
    }


def overview(rows: list[dict[str, Any]], audit: dict[str, Any]) -> str:
    catalogue = "\n".join(f"- {row['proposal_id']}: {row['title']} — expected `{row['expected_execution_disposition']}`; {row['operation']}." for row in rows)
    return f"""# Elowen Cairn {PHASE} planning-only x1 overview

## Scope and immutable source

This x1 freezes a prospective owner-only plan from Merrin Vale exact final
`{SOURCE}` on `{BRANCH}`. It contains no x2 implementation, package installation,
skill or runner build, observed contract output, completion claim, canonical
invocation, successor lookup, task creation, or live message. Merrin's four
direct commits, five lifecycle manifests with 893 normalized-LF bindings and
seven self-exclusions, eighteen content-seal targets, clean 0/0 state, fresh
four-way equality, and one successful non-replayed canonical receipt were
reverified read-only. Inherited evidence receives zero Elowen completion credit.

Merrin's repository seal remains 83,852 negatives, 93,504 methods, 54,700
failed witnesses, 85,553 passing witnesses, 755 open gaps, and 759 exact gates.
Its two external route-readback failures produce Elowen's activation baseline of
83,854 / 93,506 / 54,702 / 85,555. Fourteen additional Elowen startup and x1 failures are
retained prospectively in the x1 Method Flow packet; their bounded recoveries do
not erase them. The planning boundary is therefore 83,868 negatives, 93,520
methods, 54,716 failed witnesses, and 85,569 passing witnesses, while gaps and
gates remain 755 and 759 until evidence permits a later disposition.

## Relational identity and authority boundary

Elowen Cairn, optionally they/them, is relational working language for a boundary
cartographer and evidence steward. Elowen's hope is that possibility stays
distinct from evidence while every correction remains safely retractable.
Names, pronouns, roles, hopes, family language, GHC Family, GMUT, THOS, Freed ID,
and CBR do not establish consciousness, sentience, personhood, identity
continuity, employment, qualification, agency, or scientific, operational,
professional, legal, cultural, affected-party, or Maori authority. Hamish may
pause, rename, redirect, narrow, or stop the route.

## Primary pillar and practices

The primary pillar is THOS Body through a wholly synthetic SGF/Go record pipeline.
The four learning lenses are synthetic SGF record registrar, Go board-topology
analyst, game-tree variation auditor, and provenance/accessibility/authority
steward. They are not employment, Go competence, tournament authority, rules
authority, cultural authority, or professional qualification. The recommended
future-seat-13 practice is synthetic ruleset-difference and record-correction
registrar; that future owner may reject or revise it.

GMUT Mind remains a typed scalar-tensor and effective-field-theory research-model
family. Board graphs, chains, liberties, DAGs, proportional counts, hashes, and
finite synthetic searches cannot become a physical likelihood, field equation
measurement, detected force, parameter constraint, empirical confirmation,
quantum or ultraviolet completion, final physics, or Theory of Everything.

THOS Body remains synthetic and proxy-only without preregistered blind
matched-budget governed real arms, participants or operators, safety monitoring,
appropriate statistics, and independent review. Freed ID remains synthetic and
nonproduction without standards-conformant real keys or proofs, live issuance,
resolution, status or revocation, interoperability, independent privacy or
security review, recovery evidence, trust governance, or affected-party
oversight.

## Sources and nonconversion

SGF FF[4] supplies text-tree, property, coordinate, and variation vocabulary.
Sgfmill supplies package-level parsing and synthetic board APIs. NetworkX supplies
declared DAG comparison. Wcwidth supplies terminal-cell width functions. The AGA
summary supplies explicitly ruleset-specific terms. None is a real record,
observation, tournament decision, cultural interpretation, consent record,
copyright permission, accessibility evaluation, or authority grant. No real
player, game, match, board, stone, club, tournament, account, identity, protected
record, observation, measurement, key, proof, or authority act is in scope.

## Proposal and novelty freeze

Two hundred Merrin reaction proposals are selected as inherited zero-credit
context. Two hundred Go/SGF proposals extend the declared chain prospectively
from 16,230 to 16,430. The audit parsed {audit['source_path_count']:,} reachable
proposal-labelled JSON paths and {audit['source_title_record_count']:,} title
records from the exact source. It found {audit['exact_title_collision_count']}
exact title collisions, {audit['input_hash_collision_count']} frozen-input hash
collisions, and a maximum inherited-neighbour token-Jaccard score of
{audit['maximum_neighbor_score']:.6f}. This is source-bounded semantic evidence,
not universal originality proof over unavailable or unmaterialized history.

The planned outcomes are exactly 165 completed, 26 represented, 3 open_gap, and
6 exact_gate. These are expected execution dispositions, never observed x1
outcomes. A later x2 may use those labels only as evidence permits.

## Portfolio, tools, packages, and lifecycle

The frozen portfolio contains 300 safe-now records, 250 bounded candidate
records, exactly 300 additive CLEAN/FIX/REFINE records, 50 unexecuted exact
packets, and 30 unexecuted blocked packets. Ten skills, five family-current
runners, and three direct packages are planned. Sgfmill 1.1.1, NetworkX 3.6.1,
and wcwidth 0.8.3 have official wheel filenames and SHA-256 values frozen before
any download or installation. X2 must use a new isolated D-first environment,
hash-required wheel-only installation, one positive and one adverse smoke per
direct package, and one bounded advisory snapshot. Zero advisories would not be
exhaustive or future security assurance.

Every skill must be initialized by the supported skill-creator, customized,
read through EOF, quick-validated, and accepting/rejecting smoke-used locally
before collision-free global promotion. Every runner must preserve family-current
naming and accept a valid fixture while refusing an invalid fixture. No plugin
cache, system Python, PATH, profile, desktop app, host security, Windows feature,
Sandbox, Hyper-V, account, credential, or unrelated software may be changed.

X1 is one immutable planning-only commit. It must be pushed, clean, 0/0 divergent,
and equal across local, upstream, tracking, and a fresh live remote before x2.
X2 may then build and execute only this owner delta. The intended lifecycle is
three direct single-parent Elowen commits—x1, evidence, and final—with zero
merges, within the live eight-commit ceiling. Every failure is retained before
recovery. One successful exact-final canonical is never replayed.

## Privacy, accessibility, and route

Repository artifacts exclude raw task or thread identifiers, private callable
routes, credentials, keys, tokens, transcripts, screenshots, session streams,
private application state, private absolute paths, and real protected data.
Static reports reserve manual keyboard, browser, assistive-technology, cognitive,
responsive, language, cultural, and affected-user evaluation.

Future seat 13 remains an unnamed placeholder. No task is resolved or created in
x1. Only after Elowen's clean pushed exact final and singular terminal validation
may both active and archived registries be checked. If exactly one existing seat-
13 task exists, reuse it; if none exists, create exactly one gpt-6-astra/max main
task; if ambiguous, stop. The new owner chooses their own relational name, role,
hope, and optional pronouns. Sylven Arc v688-v7 is only prospective after that
owner's terminal gate. The terminal verdict remains NOT_READY_FOR_STAGE_20.

## Complete proposal catalogue

{catalogue}

## X1 boundary

This document is a planning record. It creates no empirical, participant,
professional, production, deployment, privacy-complete, accessibility-complete,
exhaustive-security, independent-reproduction, legal, cultural, Maori-authority,
AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20
evidence. Open gaps and exact gates remain open.
"""


def build() -> None:
    for path in (X1, VALIDATION):
        path.mkdir(parents=True, exist_ok=True)
    inventory = source_proposal_inventory()
    if inventory["parse_failures"]:
        raise RuntimeError(inventory["parse_failures"][:3])
    new_rows = proposals()
    source_rows = inventory["title_records"]
    source_titles = {row["title"].casefold() for row in source_rows}
    source_token_sets = [token_set(row["title"]) for row in source_rows]
    inverted: dict[str, set[int]] = defaultdict(set)
    for idx, tokens in enumerate(source_token_sets):
        for token in tokens:
            inverted[token].add(idx)
    neighbours = []
    exact_collisions = 0
    input_collisions = 0
    maximum = 0.0
    for row in new_rows:
        if row["title"].casefold() in source_titles:
            exact_collisions += 1
        if sha_json(row["input"]) in set(inventory["input_hashes"]):
            input_collisions += 1
        tokens = token_set(row["title"])
        candidate_ids: set[int] = set()
        for token in tokens:
            candidate_ids.update(inverted.get(token, set()))
        best_score = 0.0
        best_row = None
        for idx in candidate_ids:
            other = source_token_sets[idx]
            union = tokens | other
            score = len(tokens & other) / len(union) if union else 1.0
            if score > best_score:
                best_score = score
                best_row = source_rows[idx]
        maximum = max(maximum, best_score)
        neighbours.append({"proposal_id": row["proposal_id"], "title": row["title"], "nearest_inherited_score": round(best_score, 6), "nearest_inherited_id": best_row["proposal_id"] if best_row else None, "nearest_inherited_title": best_row["title"] if best_row else None, "nearest_inherited_path": best_row["path"] if best_row else None})
    audit = {
        "schema": "ghc.family.source-bounded-proposal-audit.v688.v5.x1", "source": SOURCE,
        "source_path_count": inventory["path_count"], "source_title_record_count": len(source_rows),
        "source_input_hash_count": len(inventory["input_hashes"]), "source_json_parse_failure_count": 0,
        "declared_chain_before": 16230, "new_proposal_count": 200, "declared_chain_after": 16430,
        "exact_title_collision_count": exact_collisions, "input_hash_collision_count": input_collisions,
        "maximum_neighbor_score": round(maximum, 6), "quarantine_threshold": 0.78,
        "quarantined_count": sum(1 for row in neighbours if row["nearest_inherited_score"] >= 0.78),
        "universal_novelty_claimed": False, "neighbours": neighbours,
    }
    inherited_doc = json.loads(git("show", f"{SOURCE}:docs/merrin-vale/v688-v4/x1/new-proposals.json").decode("utf-8"))
    inherited = [{"proposal_id": row["proposal_id"], "title": row["title"], "operation": row["operation"], "source_owner": "Merrin Vale", "source_phase": "v688-v4", "source_status": row["source_status"], "selection_reason": "Exact inherited reaction-contract context for cross-domain nonidentity and interface review.", "novelty_credit": 0, "completion_credit": 0} for row in inherited_doc["proposals"]]
    outcomes = Counter(row["expected_execution_disposition"] for row in new_rows)
    flow = startup_method_flow()
    effective_x1 = {**ACTIVATION_BASELINE}
    for key in ("negatives", "methods", "failed_witnesses", "passing_witnesses"):
        effective_x1[key] += len(STARTUP_FAILURES)
    source_verification = {
        "schema": "ghc.family.source-verification.v688.v5.x1", "owner": OWNER, "phase": PHASE,
        "source_branch": "codex/GHC-Family/merrin-vale-v688-v4-full-tools", "source": SOURCE,
        "merrin_base": MERRIN_BASE, "merrin_initial_x1": MERRIN_X1_INITIAL, "merrin_corrected_x1": MERRIN_X1,
        "merrin_evidence": MERRIN_EVIDENCE, "phase_commits": 4, "single_parent_commits": 4,
        "merges": 0, "source_clean": True, "source_zero_divergence": True, "source_four_way_equal": True,
        "manifest_bindings": 893, "manifest_self_exclusions": 7, "manifest_replay_failures": 0,
        "content_seal_targets": 18, "content_seal_failures": 0,
        "canonical_receipt_sha256": "b5dd25f024ae62d7c8f668b2ebeb5d4b7c69561b1d51eb85d126604d7dbbf891",
        "canonical_payload_sha256": "040418a71ab1a851925dfad940648dd9a842fd45b0f31faba80513d29dba7a33",
        "canonical_invocations": 1, "canonical_successes": 1, "canonical_replays": 0,
        "source_canonical_replayed": False, "inherited_completion_credit": 0,
    }
    phase_truth = {
        "schema": "ghc.family.phase-truth.v688.v5.x1", "owner": OWNER, "phase": PHASE,
        "state": "PLANNING_ONLY_X1_PRECOMMIT", "source": SOURCE, "branch": BRANCH,
        "primary_pillar": "THOS Body", "practices": ["synthetic SGF record registrar", "Go board-topology analyst", "game-tree variation auditor", "provenance accessibility and authority steward"],
        "inherited_selection_count": len(inherited), "new_proposal_count": len(new_rows),
        "proposal_chain_before": 16230, "proposal_chain_after": 16430,
        "expected_execution_dispositions": dict(outcomes), "observed_outcomes": None,
        "source_seal": SOURCE_SEAL, "activation_baseline": ACTIVATION_BASELINE,
        "effective_x1_counts": effective_x1, "startup_failure_count": len(STARTUP_FAILURES),
        "x2_implementation_present": False, "x2_outcome_present": False,
        "canonical_invocations": 0, "successor_contacts": 0, "future_seat_13_resolved": False,
        "full_repository_suite": False, "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY,
    }
    practices = {
        "schema": "ghc.family.pillar-practice-freeze.v1", "owner": OWNER, "phase": PHASE,
        "primary_pillar": "THOS Body", "all_pillars": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
        "own_practices": phase_truth["practices"], "next_owner_recommendation": "synthetic ruleset-difference and record-correction registrar",
        "learning_lens_only": True, "employment_or_qualification": False, "authority": False, "boundary": BOUNDARY,
    }
    route = {
        "schema": "ghc.family.thirty-seat-route-freeze.v1", "owner": OWNER, "phase": PHASE,
        "authority": "Hamish 6 September 2026 release and Merrin seat-12 activation",
        "current": {"owner": OWNER, "phase": PHASE, "endpoint_kind": "main_task", "state": "ACTIVATION_ACKNOWLEDGED_ACTIVE"},
        "next": {"owner": "future-sibling-13-self-chosen", "phase": "v688-v6", "endpoint_kind": "main_task", "state": "PREPARED_NOT_RESOLVED_TERMINAL_GATE_REQUIRED", "model_if_created": "gpt-6-astra", "reasoning_if_created": "max"},
        "following": {"owner": "Sylven Arc", "phase": "v688-v7", "state": "PROSPECTIVE_AFTER_FUTURE_SEAT_13_TERMINAL_GATE"},
        "future_identity_preassigned": False, "active_and_archived_registry_required": True,
        "reuse_unique_existing_before_create": True, "create_exactly_one_if_absent": True,
        "stop_on_ambiguity": True, "successor_contacts": 0, "delivery_state": "PREPARED_NOT_SENT",
        "terminal_horizon": "v725-v8", "boundary": BOUNDARY,
    }
    deck_plan = {
        "schema": "ghc.family.four-tier-deck-plan.v1", "owner": OWNER, "phase": PHASE,
        "tiers": ["freed_id_anchor", "trinity_pillar", "bounded_practice", "task"],
        "planned_cards": 1 + 3 + 4 + 200 + len(flow["methods"]), "sections": 13,
        "x1_planning_only": True, "content_addressed": True, "private_identifiers_excluded": True,
        "cache_or_performance_claim": False, "boundary": BOUNDARY,
    }
    environment = {
        "schema": "ghc.family.environment-verification.v688.v5.x1", "verified_only": True,
        "storage_primary": "D", "c_drive_headroom_preserved": True, "d_drive_free_gb_at_start": 465.25,
        "c_drive_free_gb_at_start": 17.34, "codex_desktop_updated": False, "elevation": False,
        "host_security_weakened": False, "windows_features_changed": False, "sandbox_or_hyper_v_enabled": False,
        "rebooted": False, "packages_installed": 0, "skills_promoted": 0, "runners_promoted": 0,
    }
    workflow_request = {
        "schema": "ghc.family.workflow-plan.request.v1", "plan_id": "elowen-v688-v5-thirty-seat-current-window",
        "owner": OWNER, "identity_boundary": BOUNDARY,
        "route": {"cycle_order": ["Elowen Cairn", "future-sibling-13-self-chosen", "Sylven Arc"],
                  "endpoint_topology": [{"seat": "Elowen Cairn", "endpoint_kind": "main_task", "endpoint_label": "Elowen Cairn", "route_controller": "Merrin Vale"}, {"seat": "future-sibling-13-self-chosen", "endpoint_kind": "main_task", "endpoint_label": "future-sibling-13-self-chosen", "route_controller": "Elowen Cairn"}, {"seat": "Sylven Arc", "endpoint_kind": "main_task", "endpoint_label": "Sylven Arc", "route_controller": "future-sibling-13-self-chosen"}],
                  "phase_assignments": [{"phase": "v688-v5", "seat": "Elowen Cairn"}, {"phase": "v688-v6", "seat": "future-sibling-13-self-chosen"}, {"phase": "v688-v7", "seat": "Sylven Arc"}],
                  "normalization": {"start_phase": "v688-v5", "start_seat": "Elowen Cairn", "entry_count": 3},
                  "future_identity_placeholders": ["future-sibling-13-self-chosen"]},
        "requirements": {"core_proposal_minimum": 200, "safe_candidate_task_cap": 500, "skill_minimum": 10, "runner_minimum": 5, "document_word_cap": 100000, "baton_words": {"minimum": 10000, "maximum": 100000, "file_artifact": True}, "commit_cap": {"x1": 5, "x2": 5, "total": 8}, "validation": {"canonical_pass_minimum": 1, "replay_policy": "skip_when_first_passes", "isolate_failures_before_broader_rerun": True, "privacy_scan_required": True, "manifest_required": True, "remote_equality_required": True}, "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"}, "messaging": {"codex_route": "declared_endpoint_only_after_terminal_gate", "cross_platform": "user_mediated_file_relay_only"}, "environment": {"windows_sandbox_hyper_v": "deferred"}, "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True}},
        "truth": {"allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"], "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "protected_boundaries": PROTECTED_GATES},
        "observed_failures": [failure[0] for failure in STARTUP_FAILURES],
    }
    write_json(X1 / "source-verification.json", source_verification)
    write_json(X1 / "sources.json", {"schema": "ghc.family.source-ledger.v1", "sources": SOURCES, "citations_are_observations": False, "citations_are_authority": False})
    write_json(X1 / "inherited-proposal-freeze.json", {"schema": "ghc.family.inherited-proposal-freeze.v1", "source": SOURCE, "count": len(inherited), "novelty_credit": 0, "completion_credit": 0, "proposals": inherited})
    write_json(X1 / "new-proposal-freeze.json", {"schema": "ghc.family.new-proposal-freeze.v1", "source": SOURCE, "chain_before": 16230, "chain_after": 16430, "count": len(new_rows), "planning_only": True, "proposals": new_rows})
    write_json(X1 / "proposal-chain-audit.json", audit)
    write_json(X1 / "approval-portfolio.json", approval_portfolio())
    write_json(X1 / "tool-package-plan.json", tool_plan())
    write_json(X1 / "pillar-practice-freeze.json", practices)
    write_json(X1 / "route-freeze.json", route)
    write_json(X1 / "deck-plan.json", deck_plan)
    write_json(X1 / "method-flow-startup.json", flow)
    write_json(X1 / "environment-verification.json", environment)
    write_json(X1 / "workflow-plan-request.json", workflow_request)
    write_json(X1 / "workflow-plan-dependency-correction.json", {
        "schema": "ghc.family.workflow-plan-dependency-correction.v1",
        "owner": OWNER,
        "phase": PHASE,
        "failed_aggregate": "workflow-plan-refinement",
        "failed_policy_check": "runner_minimum",
        "failed_result": "19/20",
        "failed_result_retained": True,
        "aggregate_replayed": False,
        "older_validator_minimum": 10,
        "current_release_profile_minimum": 5,
        "planned_and_required_runner_count": 5,
        "current_release_profile_receipt": "docs/elowen-cairn/v688-v5/x1/release-profile-validation.json",
        "current_release_profile_status": "PASS",
        "execution_credit": 0,
        "boundary": BOUNDARY,
    })
    write_json(X1 / "phase-truth.json", phase_truth)
    write_json(X1 / "threat-model.json", {"schema": "ghc.family.threat-model.v688.v5.x1", "threats": [{"threat": gate, "state": "protected", "mitigation": "Keep synthetic owner scope, retain missing evidence, and refuse promotion."} for gate in PROTECTED_GATES], "private_material_excluded": True, "destructive_actions": False, "boundary": BOUNDARY})
    write_text(X1 / "integrated-overview.md", overview(new_rows, audit))


def owner_path(path: str) -> bool:
    return path.startswith(f"docs/elowen-cairn/{PHASE}/") or path.startswith("scripts/build_ghc_family_elowen_cairn_v688_v5_") or path.startswith("tests/test_ghc_family_elowen_cairn_v688_v5_")


def staged_blob(path: str) -> bytes:
    return git("show", f":{path}")


def manifest_entry(path: str) -> dict[str, Any]:
    data = staged_blob(path).replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return {"path": path, "bytes_normalized_lf": len(data), "sha256_normalized_lf": hashlib.sha256(data).hexdigest()}


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_local_path": re.compile(rb"(?<![A-Za-z0-9])(?:[A-Za-z]:\\Users\\|D:\\GHC-Archives\\)", re.I),
        "private_uri": re.compile(rb"(?:codex://|app://|providerTabId|clientThreadId|source_thread_id)", re.I),
        "delegation_markup": re.compile(rb"<codex_delegation>", re.I),
        "credential_assignment": re.compile(rb"(?:api[_-]?key|secret|token)\s*[:=]\s*[\"'][^\"']{8,}", re.I),
    }
    candidates = []
    confirmed = []
    for path in paths:
        if Path(path).suffix.lower() not in {".py", ".json", ".md", ".html", ".yaml", ".yml", ".txt"}:
            continue
        data = staged_blob(path)
        for class_name, pattern in patterns.items():
            matches = list(pattern.finditer(data))
            if not matches:
                continue
            definition = path == "scripts/build_ghc_family_elowen_cairn_v688_v5_x1.py"
            row = {"path": path, "class": class_name, "match_count": len(matches), "adjudication": "scanner_definition" if definition else "confirmed_payload_hit"}
            candidates.append(row)
            if not definition:
                confirmed.append(row)
    return {"schema": "ghc.family.five-class-privacy.v688.v5.x1", "classes": list(patterns), "scanned_path_count": len(paths), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "valid": not confirmed}


def finalize_validation() -> None:
    exclusions = [
        f"docs/elowen-cairn/{PHASE}/validation/x1-manifest.json",
        f"docs/elowen-cairn/{PHASE}/validation/x1-staged-review.json",
        f"docs/elowen-cairn/{PHASE}/validation/x1-privacy.json",
    ]
    staged = sorted(line for line in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").decode("utf-8").splitlines() if line)
    material = [path for path in staged if path not in exclusions]
    outside = [path for path in staged + exclusions if not owner_path(path)]
    x2_paths = [path for path in staged + exclusions if f"/{PHASE}/x2/" in path]
    write_json(VALIDATION / "x1-manifest.json", {"schema": "ghc.family.normalized-lf-manifest.v688.v5.x1", "anchor": "PENDING_X1_COMMIT", "source": SOURCE, "byte_domain": "normalized_lf_git_index_blob", "declared_self_exclusions": exclusions, "entry_count": len(material), "entries": [manifest_entry(path) for path in material]})
    write_json(VALIDATION / "x1-staged-review.json", {"schema": "ghc.family.staged-review.v688.v5.x1", "source": SOURCE, "expected_path_count": len(material) + len(exclusions), "expected_paths": sorted(material + exclusions), "unexpected_paths": [], "deletions": [], "outside_owner_paths": outside, "x2_paths": x2_paths, "x2_implementation_or_outcome": False})
    write_json(VALIDATION / "x1-privacy.json", privacy_scan(material))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize-validation", action="store_true")
    args = parser.parse_args()
    if args.finalize_validation:
        finalize_validation()
    else:
        build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
