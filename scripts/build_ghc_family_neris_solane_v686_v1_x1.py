"""Freeze Neris Solane v686-v1 planning without executing an x2 contract."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/neris-solane/v686-v1"
SOURCE = "c6b56f912836a46a0dbb07c13aaf6e731e1b32e2"
SOURCE_X1 = "ae33e7fd357e38c464677c10538a50f069b68353"
SOURCE_EVIDENCE = "01e246b683f64993cb2cca2244776e92c237c850"
OWNER = "Neris Solane"
PHASE = "v686-v1"
BOUNDARY = (
    "Neris Solane, they/them, corrigible evidence-continuity steward, the hope to "
    "make bounded claims easier to test and safer to hand onward, names, roles, "
    "hopes, pronouns, family language, GHC Family, Freed ID, CBR, and Trinity "
    "Mandala are relational working language only. They establish no consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, scientific, operational, professional, legal, cultural, "
    "affected-party, or Māori authority. Hamish may rename, pause, redirect, narrow, "
    "or stop the route."
)
GATES = [
    "real participants and governed evaluation",
    "GMUT empirical observable likelihood and confirmation",
    "THOS real matched-budget blind arms and independent review",
    "Freed ID production keys proofs lifecycle and trust governance",
    "CBR legal cultural affected-party and Māori authority",
    "complete privacy accessibility exhaustive security independent reproduction",
    "AGI ASI consciousness personhood Theory of Everything canon Stage 20",
    "deployment accounts credentials purchase and destructive or sibling mutation",
]
PRACTICES = [
    "evidence protocol designer",
    "reproducibility engineer",
    "statistical quality reviewer",
    "accessible governance editor",
]

SIMPY = "https://simpy.readthedocs.io/en/stable/topical_guides/time_and_scheduling.html"
FSM = "https://github.com/pytransitions/transitions"
CSP = "https://python-constraint.github.io/python-constraint/"
STATS = "https://docs.python.org/3.12/library/statistics.html"
PROV = "https://www.w3.org/TR/prov-o/"
WCAG = "https://www.w3.org/TR/WCAG22/"
VC = "https://www.w3.org/TR/vc-data-model-2.0/"
RFC8949 = "https://www.rfc-editor.org/rfc/rfc8949"

FAMILIES: list[dict] = []


def family(name, runner, operation, mission, cases, source, disposition="completed"):
    assert len(cases) == 10, (name, len(cases))
    FAMILIES.append(
        {
            "name": name,
            "runner": runner,
            "operation": operation,
            "mission": mission,
            "cases": cases,
            "source": source,
            "expected_execution_disposition": disposition,
        }
    )


# Every expected result is a frozen hand-specified oracle. A returned error object is
# an expected refusal for that input, not an exception hidden by an outcome collector.
family(
    "event_calendar",
    "trace",
    "schedule",
    "Audit stable ordering, exclusive horizons, and typed event-calendar inputs.",
    [
        ("three separated ticks resolve earliest first", {"events": [["third", 9, 0], ["first", 1, 0], ["second", 4, 0]]}, ["first", "second", "third"]),
        ("three same-tick priorities resolve numerically", {"events": [["low", 3, 8], ["high", 3, -2], ["mid", 3, 1]]}, ["high", "mid", "low"]),
        ("same-tick same-priority events retain insertion", {"events": [["alpha", 6, 2], ["beta", 6, 2], ["gamma", 6, 2]]}, ["alpha", "beta", "gamma"]),
        ("zero horizon excludes a tick-zero event", {"events": [["zero", 0, 0]], "until": 0}, []),
        ("later horizon retains every earlier event", {"events": [["a", 2, 0], ["b", 5, 0]], "until": 6}, ["a", "b"]),
        ("negative priority wins only within one tick", {"events": [["early", 1, 99], ["late", 2, -99]]}, ["early", "late"]),
        ("fractional tick is refused", {"events": [["fraction", 1.5, 0]]}, {"error": "invalid_tick"}),
        ("boolean tick is not an integer event time", {"events": [["boolean", True, 0]]}, {"error": "invalid_tick"}),
        ("fractional priority is refused", {"events": [["priority", 1, 0.5]]}, {"error": "invalid_priority"}),
        ("nonadjacent duplicate labels remain invalid", {"events": [["dup", 1, 0], ["other", 2, 0], ["dup", 3, 0]]}, {"error": "duplicate_event"}),
    ],
    SIMPY,
)

family(
    "trial_state_trace",
    "trace",
    "transition",
    "Audit longer legal traces and terminal-state refusals without claiming a real trial.",
    [
        ("pause-resume then finish reaches recorded", {"events": ["start", "pause", "resume", "finish"]}, "recorded"),
        ("running cancellation reaches cancelled", {"events": ["start", "cancel"]}, "cancelled"),
        ("a second pause after resume remains paused", {"events": ["start", "pause", "resume", "pause"]}, "paused"),
        ("cancelled work cannot restart", {"events": ["cancel", "start"]}, {"error": "invalid_transition"}),
        ("planned work cannot pause", {"events": ["pause"]}, {"error": "invalid_transition"}),
        ("planned work cannot resume", {"events": ["resume"]}, {"error": "invalid_transition"}),
        ("cancelled work cannot finish", {"events": ["start", "cancel", "finish"]}, {"error": "invalid_transition"}),
        ("running work cannot start twice", {"events": ["start", "start"]}, {"error": "invalid_transition"}),
        ("paused work cannot pause twice", {"events": ["start", "pause", "pause"]}, {"error": "invalid_transition"}),
        ("resumed work cannot resume again", {"events": ["start", "pause", "resume", "resume"]}, {"error": "invalid_transition"}),
    ],
    FSM,
)

family(
    "resource_queue",
    "trace",
    "queue",
    "Audit deterministic queue release and typed durations on invented jobs.",
    [
        ("three overlapping arrivals accumulate waiting", {"jobs": [["a", 0, 3], ["b", 1, 2], ["c", 2, 1]]}, [["a", 0, 3], ["b", 3, 5], ["c", 5, 6]]),
        ("three simultaneous arrivals retain FIFO", {"jobs": [["x", 4, 1], ["y", 4, 1], ["z", 4, 1]]}, [["x", 4, 5], ["y", 5, 6], ["z", 6, 7]]),
        ("zero-duration middle job does not move release", {"jobs": [["a", 0, 2], ["b", 1, 0], ["c", 1, 1]]}, [["a", 0, 2], ["b", 2, 2], ["c", 2, 3]]),
        ("unsorted equal arrivals retain source order", {"jobs": [["later-listed", 2, 1], ["earlier-tick", 0, 1], ["peer", 2, 1]]}, [["earlier-tick", 0, 1], ["later-listed", 2, 3], ["peer", 3, 4]]),
        ("large idle interval remains visible", {"jobs": [["a", 0, 1], ["b", 100, 1]]}, [["a", 0, 1], ["b", 100, 101]]),
        ("negative arrival is refused", {"jobs": [["a", -1, 2]]}, {"error": "invalid_job"}),
        ("boolean duration is refused", {"jobs": [["a", 0, True]]}, {"error": "invalid_job"}),
        ("nonadjacent duplicate jobs are refused", {"jobs": [["a", 0, 1], ["b", 2, 1], ["a", 4, 1]]}, {"error": "duplicate_job"}),
        ("vacant queue yields no fabricated service", {"jobs": []}, []),
        ("four-job backlog preserves every interval", {"jobs": [["a", 0, 1], ["b", 0, 2], ["c", 1, 3], ["d", 5, 1]]}, [["a", 0, 1], ["b", 1, 3], ["c", 3, 6], ["d", 6, 7]]),
    ],
    SIMPY,
)

family(
    "checkpoint_replay",
    "trace",
    "replay",
    "Audit idempotent replay, checkpoint conflicts, signed deltas, and strict types.",
    [
        ("three identical deliveries contribute once", {"events": [["e", 4], ["e", 4], ["e", 4]]}, 4),
        ("preseen delivery plus a new event adds only new", {"initial": 5, "seen": {"a": 5}, "events": [["a", 5], ["b", 2]]}, 7),
        ("preseen payload disagreement rejects replay", {"initial": 5, "seen": {"a": 5}, "events": [["a", 6]]}, {"error": "conflicting_replay"}),
        ("negative checkpoint accumulator remains explicit", {"initial": -3, "events": [["a", 1]]}, -2),
        ("fractional checkpoint accumulator is refused", {"initial": 0.5, "events": []}, {"error": "invalid_delta"}),
        ("string delta is refused", {"events": [["a", "1"]]}, {"error": "invalid_delta"}),
        ("repeated zero event contributes zero once", {"events": [["z", 0], ["z", 0]]}, 0),
        ("empty replay starts from zero", {"events": []}, 0),
        ("signed corrections preserve exact total", {"events": [["a", 9], ["b", -4], ["c", -1]]}, 4),
        ("boolean and integer duplicate payloads conflict", {"events": [["a", True], ["a", 1]]}, {"error": "conflicting_replay"}),
    ],
    PROV,
)

family(
    "matched_resource_budget",
    "budget",
    "budget",
    "Audit exact two-arm accounting independently from any effectiveness claim.",
    [
        ("two ten-unit arms match at the ceiling", {"arms": [[4, 6], [10]], "cap": 10}, {"totals": [10, 10], "matched": True, "within_cap": True}),
        ("unequal low totals stay unmatched", {"arms": [[1, 1], [3]], "cap": 5}, {"totals": [2, 3], "matched": False, "within_cap": True}),
        ("equal eleven-unit arms exceed ten", {"arms": [[5, 6], [7, 4]], "cap": 10}, {"totals": [11, 11], "matched": True, "within_cap": False}),
        ("one vacant arm exposes unequal totals", {"arms": [[], [2]], "cap": 2}, {"totals": [0, 2], "matched": False, "within_cap": True}),
        ("two vacant arms fit a positive cap", {"arms": [[], []], "cap": 3}, {"totals": [0, 0], "matched": True, "within_cap": True}),
        ("boolean cap is refused", {"arms": [[1], [1]], "cap": True}, {"error": "nonnegative_integer_required"}),
        ("negative cap is refused", {"arms": [[0], [0]], "cap": -1}, {"error": "nonnegative_integer_required"}),
        ("fractional cost is refused", {"arms": [[1.5], [1]], "cap": 2}, {"error": "nonnegative_integer_required"}),
        ("three arms cannot masquerade as a pair", {"arms": [[1], [1], [1]], "cap": 1}, {"error": "two_arms_required"}),
        ("zero arms match an exact zero ceiling", {"arms": [[0], [0]], "cap": 0}, {"totals": [0, 0], "matched": True, "within_cap": True}),
    ],
    CSP,
)

family(
    "allocation_balance",
    "budget",
    "allocation",
    "Audit declared A/B counts while explicitly withholding randomness claims.",
    [
        ("eight alternating assignments balance", {"sequence": ["A", "B"] * 4}, {"A": 4, "B": 4, "imbalance": 0}),
        ("five assignments leave one extra A", {"sequence": ["A", "B", "A", "B", "A"]}, {"A": 3, "B": 2, "imbalance": 1}),
        ("four assignments leave two extra B", {"sequence": ["B", "B", "A", "B"]}, {"A": 1, "B": 3, "imbalance": 2}),
        ("two blocks can still balance totals", {"sequence": ["B", "B", "B", "A", "A", "A"]}, {"A": 3, "B": 3, "imbalance": 0}),
        ("single A reports unit imbalance", {"sequence": ["A"]}, {"A": 1, "B": 0, "imbalance": 1}),
        ("single B reports unit imbalance", {"sequence": ["B"]}, {"A": 0, "B": 1, "imbalance": 1}),
        ("empty label is not an arm", {"sequence": [""]}, {"error": "unknown_arm"}),
        ("null assignment is not inferred", {"sequence": [None]}, {"error": "unknown_arm"}),
        ("lowercase labels remain unknown", {"sequence": ["a", "b"]}, {"error": "unknown_arm"}),
        ("vacant allocation reports no assignments", {"sequence": []}, {"A": 0, "B": 0, "imbalance": 0}),
    ],
    CSP,
)

family(
    "masking_separation",
    "budget",
    "separation",
    "Audit explicit role-set overlap without inferring real staffing or blinding.",
    [
        ("one shared member is surfaced from larger sets", {"evaluators": ["e1", "e2"], "key_holders": ["k1", "e1"]}, ["e1"]),
        ("three shared members sort lexically", {"evaluators": ["z", "m", "a"], "key_holders": ["m", "a", "z"]}, ["a", "m", "z"]),
        ("two disjoint groups retain no overlap", {"evaluators": ["e1", "e2"], "key_holders": ["k1", "k2"]}, []),
        ("two vacant groups retain no invented member", {"evaluators": [], "key_holders": []}, []),
        ("duplicate evaluator fails before overlap", {"evaluators": ["e", "e"], "key_holders": ["e"]}, {"error": "duplicate_role_member"}),
        ("duplicate key holder fails before overlap", {"evaluators": ["k"], "key_holders": ["k", "k"]}, {"error": "duplicate_role_member"}),
        ("case-distinct labels remain disjoint", {"evaluators": ["Agent"], "key_holders": ["agent"]}, []),
        ("surrounding whitespace is not an alias", {"evaluators": ["e"], "key_holders": [" e "]}, []),
        ("one vacant side retains an empty relation", {"evaluators": ["e1", "e2"], "key_holders": []}, []),
        ("two overlaps exclude unrelated members", {"evaluators": ["a", "b", "c"], "key_holders": ["c", "x", "a"]}, ["a", "c"]),
    ],
    PROV,
)

family(
    "missingness_denominator",
    "budget",
    "denominator",
    "Audit complete disposition denominators without silent dropping or imputation.",
    [
        ("five mixed rows sum to their planned denominator", {"rows": ["observed", "missing", "excluded", "observed", "missing"]}, {"total": 5, "observed": 2, "missing": 2, "excluded": 1}),
        ("four observed rows retain a denominator of four", {"rows": ["observed"] * 4}, {"total": 4, "observed": 4, "missing": 0, "excluded": 0}),
        ("three missing rows stay missing", {"rows": ["missing"] * 3}, {"total": 3, "observed": 0, "missing": 3, "excluded": 0}),
        ("three excluded rows stay countable", {"rows": ["excluded"] * 3}, {"total": 3, "observed": 0, "missing": 0, "excluded": 3}),
        ("vacant plan has an explicit zero denominator", {"rows": []}, {"total": 0, "observed": 0, "missing": 0, "excluded": 0}),
        ("uppercase disposition is refused", {"rows": ["MISSING"]}, {"error": "unknown_disposition"}),
        ("null disposition is refused again at source", {"rows": [None, "observed"]}, {"error": "unknown_disposition"}),
        ("each disposition repeated twice stays exact", {"rows": ["observed", "missing", "excluded"] * 2}, {"total": 6, "observed": 2, "missing": 2, "excluded": 2}),
        ("one observed row keeps a one-row denominator", {"rows": ["observed"]}, {"total": 1, "observed": 1, "missing": 0, "excluded": 0}),
        ("one excluded row is not erased", {"rows": ["excluded"]}, {"total": 1, "observed": 0, "missing": 0, "excluded": 1}),
    ],
    STATS,
)

family(
    "exact_summary_statistics",
    "analysis",
    "summary",
    "Audit exact finite-fixture summaries while withholding population inference.",
    [
        ("two even values have exact mean three", {"values": [2, 4], "stat": "mean"}, "3"),
        ("unsorted odd values retain middle value", {"values": [9, 1, 5], "stat": "median"}, "5"),
        ("unsorted even values average the middle pair", {"values": [8, 2, 6, 4], "stat": "median"}, "5"),
        ("negative values preserve a negative mean", {"values": [-6, -2, 2], "stat": "mean"}, "-2"),
        ("rational strings retain an exact mean", {"values": ["1/2", "3/2"], "stat": "mean"}, "1"),
        ("two-point sample variance uses one degree", {"values": [1, 5], "stat": "sample_variance"}, "8"),
        ("four-point population variance stays rational", {"values": [0, 2, 4, 6], "stat": "population_variance"}, "5"),
        ("empty median is refused", {"values": [], "stat": "median"}, {"error": "insufficient_data"}),
        ("unknown summary statistic is refused", {"values": [1, 2], "stat": "mode"}, {"error": "unknown_statistic"}),
        ("boolean value is not exact numeric input", {"values": [True, 2], "stat": "mean"}, {"error": "malformed_input"}),
    ],
    STATS,
)

family(
    "paired_result_alignment",
    "analysis",
    "paired",
    "Audit label-aligned exact differences with explicit A-minus-B direction.",
    [
        ("three reordered counterparts align by label", {"a": [["p3", 9], ["p1", 4], ["p2", 6]], "b": [["p2", 1], ["p3", 4], ["p1", 3]]}, [["p3", "5"], ["p1", "1"], ["p2", "5"]]),
        ("fractional strings preserve exact paired difference", {"a": [["p", "3/2"]], "b": [["p", "1/2"]]}, [["p", "1"]]),
        ("negative values preserve directional subtraction", {"a": [["p", -4]], "b": [["p", -1]]}, [["p", "-3"]]),
        ("four pairs retain A input ordering", {"a": [["d", 4], ["c", 3], ["b", 2], ["a", 1]], "b": [["a", 0], ["b", 0], ["c", 0], ["d", 0]]}, [["d", "4"], ["c", "3"], ["b", "2"], ["a", "1"]]),
        ("different pair labels are refused", {"a": [["left", 1]], "b": [["right", 1]]}, {"error": "pair_set_mismatch"}),
        ("duplicate left label remains invalid", {"a": [["p", 1], ["p", 1]], "b": [["p", 1]]}, {"error": "duplicate_pair"}),
        ("duplicate right label remains invalid", {"a": [["p", 1]], "b": [["p", 1], ["p", 1]]}, {"error": "duplicate_pair"}),
        ("two vacant pair sets yield no comparison", {"a": [], "b": []}, []),
        ("equal negative values retain zero difference", {"a": [["p", -2]], "b": [["p", -2]]}, [["p", "0"]]),
        ("boolean paired value is refused as malformed", {"a": [["p", True]], "b": [["p", 1]]}, {"error": "malformed_input"}),
    ],
    STATS,
)

family(
    "histogram_boundaries",
    "analysis",
    "histogram",
    "Audit exact finite histogram boundaries without density or distribution claims.",
    [
        ("six values populate three equal-width bins", {"values": [0, 1, 2, 3, 4, 6], "edges": [0, 2, 4, 6]}, [2, 2, 2]),
        ("two interior boundaries enter following bins", {"values": [2, 4], "edges": [0, 2, 4, 6]}, [0, 1, 1]),
        ("uppermost edge is counted exactly once", {"values": [10], "edges": [0, 5, 10]}, [0, 1]),
        ("value below a negative range is refused", {"values": [-6], "edges": [-5, 0, 5]}, {"error": "outside_edges"}),
        ("value above the final edge is refused", {"values": [6], "edges": [-5, 0, 5]}, {"error": "outside_edges"}),
        ("one declared edge cannot define a bin", {"values": [], "edges": [0]}, {"error": "invalid_edges"}),
        ("duplicate leading edges are refused", {"values": [0], "edges": [0, 0, 1]}, {"error": "invalid_edges"}),
        ("rational strings use exact boundaries", {"values": ["1/2", "3/2"], "edges": ["0", "1", "2"]}, [1, 1]),
        ("negative range values populate exact bins", {"values": [-4, -1, 2], "edges": [-5, 0, 5]}, [2, 1]),
        ("empty values retain three zero bins", {"values": [], "edges": [0, 1, 2, 3]}, [0, 0, 0]),
    ],
    STATS,
)

family(
    "preregistered_stopping",
    "analysis",
    "stop",
    "Audit frozen stop precedence while refusing optional result peeking.",
    [
        ("safety dominates simultaneous overspend", {"safety": True, "spent": 9, "cap": 5, "done": False}, "safety_stop"),
        ("completion below a large cap records", {"safety": False, "spent": 1, "cap": 100, "done": True}, "record"),
        ("completion at its cap remains a budget stop", {"safety": False, "spent": 7, "cap": 7, "done": True}, "budget_stop"),
        ("unfinished zero-spend positive-cap work continues", {"safety": False, "spent": 0, "cap": 1, "done": False}, "continue"),
        ("boolean spend is refused", {"safety": False, "spent": True, "cap": 2, "done": False}, {"error": "invalid_budget"}),
        ("negative cap remains invalid", {"safety": False, "spent": 0, "cap": -2, "done": False}, {"error": "invalid_budget"}),
        ("explicit false peek leaves ordinary state", {"safety": False, "spent": 1, "cap": 2, "done": False, "peek": False}, "continue"),
        ("explicit true peek remains prohibited", {"safety": False, "spent": 1, "cap": 2, "done": True, "peek": True}, {"error": "unregistered_peek"}),
        ("integer safety flag is refused", {"safety": 1, "spent": 0, "cap": 2, "done": False}, {"error": "invalid_flag"}),
        ("integer done flag is refused", {"safety": False, "spent": 0, "cap": 2, "done": 0}, {"error": "invalid_flag"}),
    ],
    STATS,
)

family(
    "derivation_graph",
    "provenance",
    "lineage",
    "Audit deterministic DAG order while retaining cycles and missing nodes as failures.",
    [
        ("four-node chain keeps every predecessor first", {"nodes": ["d", "c", "b", "a"], "edges": [["a", "b"], ["b", "c"], ["c", "d"]]}, ["a", "b", "c", "d"]),
        ("one source may branch to two ordered children", {"nodes": ["root", "right", "left"], "edges": [["root", "right"], ["root", "left"]]}, ["root", "left", "right"]),
        ("two roots converge before a final child", {"nodes": ["z", "a", "join", "tail"], "edges": [["z", "join"], ["a", "join"], ["join", "tail"]]}, ["a", "z", "join", "tail"]),
        ("disconnected source precedes its dependent pair", {"nodes": ["z", "a", "b"], "edges": [["a", "b"]]}, ["a", "b", "z"]),
        ("duplicate identical edge does not duplicate a node", {"nodes": ["a", "b"], "edges": [["a", "b"], ["a", "b"]]}, ["a", "b"]),
        ("self-dependency remains cyclic", {"nodes": ["self"], "edges": [["self", "self"]]}, {"error": "cycle"}),
        ("three-member dependency loop is refused", {"nodes": ["a", "b", "c"], "edges": [["a", "b"], ["b", "c"], ["c", "a"]]}, {"error": "cycle"}),
        ("undeclared source node remains missing", {"nodes": ["b", "c"], "edges": [["a", "b"], ["b", "c"]]}, {"error": "missing_node"}),
        ("repeated node label is refused before sorting", {"nodes": ["a", "b", "a"], "edges": []}, {"error": "duplicate_node"}),
        ("empty derivation graph stays empty", {"nodes": [], "edges": []}, []),
    ],
    PROV,
)

family(
    "byte_domain_fixity",
    "provenance",
    "fixity",
    "Audit explicit text-byte domains without treating a digest as identity or authority.",
    [
        ("matching non-ASCII text has equal UTF-8 bytes", {"left": "mōhiotanga", "right": "mōhiotanga", "domain": "utf8"}, True),
        ("CRLF normalizes across three lines", {"left": "a\r\nb\r\nc", "right": "a\nb\nc", "domain": "normalized_lf_utf8"}, True),
        ("raw CRLF differs across three lines", {"left": "a\r\nb\r\nc", "right": "a\nb\nc", "domain": "utf8"}, False),
        ("tab and spaces remain distinct", {"left": "a\tb", "right": "a b", "domain": "utf8"}, False),
        ("two final newlines differ from one", {"left": "a\n\n", "right": "a\n", "domain": "normalized_lf_utf8"}, False),
        ("matching emoji text compares equally", {"left": "evidence ✨", "right": "evidence ✨", "domain": "utf8"}, True),
        ("canonical-equivalent Unicode remains byte-distinct", {"left": "Å", "right": "A\u030a", "domain": "utf8"}, False),
        ("unstated normalization domain is refused", {"left": "a", "right": "a", "domain": "unicode"}, {"error": "unknown_domain"}),
        ("lone carriage return does not normalize", {"left": "x\ry", "right": "x\ny", "domain": "normalized_lf_utf8"}, False),
        ("two empty UTF-8 domains remain equal", {"left": "", "right": "", "domain": "normalized_lf_utf8"}, True),
    ],
    PROV,
)

family(
    "immutable_correction_merge",
    "provenance",
    "merge",
    "Audit additive record merge while refusing silent replacement and type coercion.",
    [
        ("three disjoint keys combine without erasure", {"left": {"a": 1, "b": 2}, "right": {"c": 3}}, {"a": 1, "b": 2, "c": 3}),
        ("matching list payload is idempotent", {"left": {"a": [1, 2]}, "right": {"a": [1, 2]}}, {"a": [1, 2]}),
        ("list-order change remains a conflict", {"left": {"a": [1, 2]}, "right": {"a": [2, 1]}}, {"error": "conflict"}),
        ("false and zero payloads do not coalesce", {"left": {"a": False}, "right": {"a": 0}}, {"error": "conflict"}),
        ("nested key order does not create conflict", {"left": {"a": {"x": 1, "y": 2}}, "right": {"a": {"y": 2, "x": 1}}}, {"a": {"x": 1, "y": 2}}),
        ("matching null payload remains explicit", {"left": {"a": None}, "right": {"a": None}}, {"a": None}),
        ("null and disjoint value both survive", {"left": {"a": None}, "right": {"b": 2}}, {"a": None, "b": 2}),
        ("nested scalar disagreement is quarantined", {"left": {"a": {"x": 1}}, "right": {"a": {"x": 2}}}, {"error": "conflict"}),
        ("vacant history accepts two incoming fields", {"left": {}, "right": {"x": 1, "y": 2}}, {"x": 1, "y": 2}),
        ("two vacant records stay vacant", {"left": {}, "right": {}}, {}),
    ],
    PROV,
)

family(
    "minimal_public_projection",
    "export",
    "export",
    "Audit explicit top-level projection and required-field refusal.",
    [
        ("two allowed fields exclude one private note", {"record": {"title": "report", "state": "open_gap", "note": "omit"}, "allow": ["title", "state"], "required": ["title"]}, {"title": "report", "state": "open_gap"}),
        ("two required fields are retained", {"record": {"title": "report", "state": "represented"}, "allow": ["state", "title"], "required": ["title", "state"]}, {"state": "represented", "title": "report"}),
        ("one of two required fields missing refuses output", {"record": {"title": "report"}, "allow": ["title", "state"], "required": ["title", "state"]}, {"error": "missing_required"}),
        ("required field outside allowlist refuses output", {"record": {"title": "report"}, "allow": [], "required": ["title"]}, {"error": "required_not_allowed"}),
        ("absent optional field remains absent", {"record": {"title": "report"}, "allow": ["title", "summary"], "required": []}, {"title": "report"}),
        ("false value remains a declared field", {"record": {"empirical": False}, "allow": ["empirical"], "required": ["empirical"]}, {"empirical": False}),
        ("zero value remains a declared field again", {"record": {"failures": 0}, "allow": ["failures"], "required": []}, {"failures": 0}),
        ("nested object remains nested", {"record": {"source": {"kind": "synthetic", "count": 2}}, "allow": ["source"], "required": ["source"]}, {"source": {"kind": "synthetic", "count": 2}}),
        ("three repeated allowlist entries are refused", {"record": {"title": "report"}, "allow": ["title", "title", "title"], "required": []}, {"error": "duplicate_allowlist"}),
        ("required field remains case-sensitive", {"record": {"State": "open_gap"}, "allow": ["state"], "required": ["state"]}, {"error": "missing_required"}),
    ],
    VC,
)

family(
    "accessible_evidence_table",
    "export",
    "table",
    "Audit table structure while reserving human and assistive-technology review.",
    [
        ("three-column two-row table is rectangular", {"headers": ["claim", "state", "source"], "rows": [["a", "open_gap", "synthetic"], ["b", "represented", "synthetic"]]}, True),
        ("header-only three-column table is explicit", {"headers": ["claim", "state", "source"], "rows": []}, True),
        ("single visible cell forms a structural table", {"headers": ["value"], "rows": [["unknown"]]}, True),
        ("two-column table rejects one-cell row", {"headers": ["a", "b"], "rows": [["only"]]}, False),
        ("one-column table rejects two-cell row", {"headers": ["a"], "rows": [["one", "two"]]}, False),
        ("three duplicate headers remain ambiguous", {"headers": ["a", "a", "a"], "rows": [["1", "2", "3"]]}, False),
        ("whitespace-only header remains blank", {"headers": ["   "], "rows": [["value"]]}, False),
        ("whitespace-only cell is not visible evidence", {"headers": ["value"], "rows": [["   "]]}, False),
        ("empty string cell remains structurally invalid", {"headers": ["value"], "rows": [[""]]}, False),
        ("no headers cannot define a data table", {"headers": [], "rows": [["orphan"]]}, False),
    ],
    WCAG,
)

for name, disposition, labels, source in [
    (
        "governed_trial_vacancies",
        "represented",
        [
            "prospective sampling frame",
            "real allocation sequence custodian",
            "operator training verification",
            "live incident escalation path",
            "governed stopping committee",
            "real matched workload evidence",
            "participant information process",
            "data monitoring charter",
            "external statistical analysis plan",
            "post-trial remedy pathway",
        ],
        PROV,
    ),
    (
        "gmut_observation_obligations",
        "open_gap",
        [
            "dimensionally closed measurement operator",
            "instrument response transfer function",
            "predeclared observational likelihood",
            "calibrated uncertainty propagation",
            "independently measured boundary data",
            "out-of-sample rival-model score",
            "laboratory or astronomical observation",
            "parameter degeneracy analysis",
            "ultraviolet completion argument",
            "replicable discriminating physical effect",
        ],
        STATS,
    ),
    (
        "cbr_authority_reservations",
        "exact_gate",
        [
            "affected-community purpose approval",
            "lawful retention-period determination",
            "real credential issuer authorization",
            "production revocation governance",
            "independent privacy impact approval",
            "accessible notice acceptance by affected users",
            "Māori terminology and tikanga review",
            "iwi and hapū data-governance decision",
            "tangata whenua benefit and risk judgment",
            "competent legal remedy order",
        ],
        VC,
    ),
]:
    family(
        name,
        "export",
        "reservation",
        "Keep a named real-world prerequisite unresolved despite a valid local record.",
        [
            (
                label,
                {"obligation": label, "evidence": None, "authority": None, "disposition": disposition},
                disposition,
            )
            for label in labels
        ],
        source,
        disposition,
    )


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def read_git_json(spec: str):
    return json.loads(git("show", spec).decode("utf-8"))


def package_plan(wheelhouse: Path) -> list[dict]:
    direct = {"canonicaljson": "2.0.0", "frozendict": "2.4.7", "cbor2": "6.1.4"}
    rows = []
    for name, version in direct.items():
        candidates = sorted(wheelhouse.glob(f"{name.replace('-', '_')}-{version}-*.whl"))
        if len(candidates) != 1:
            raise ValueError(f"Expected one wheel for {name} {version}, found {len(candidates)}")
        wheel = candidates[0]
        with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/{version}/json", timeout=30) as response:
            metadata = json.load(response)
        remote = [row for row in metadata["urls"] if row["filename"] == wheel.name]
        if len(remote) != 1:
            raise ValueError(f"PyPI did not return one matching file for {wheel.name}")
        actual = hashlib.sha256(wheel.read_bytes()).hexdigest()
        if actual != remote[0]["digests"]["sha256"]:
            raise ValueError(f"Wheel digest mismatch for {wheel.name}")
        with zipfile.ZipFile(wheel) as archive:
            names = archive.namelist()
            traversal = [entry for entry in names if entry.startswith(("/", "\\")) or ".." in Path(entry).parts]
            metadata_names = [entry for entry in names if entry.endswith(".dist-info/METADATA")]
            if traversal or len(metadata_names) != 1:
                raise ValueError(f"Wheel structure refused for {wheel.name}")
            text = archive.read(metadata_names[0]).decode("utf-8", errors="strict")
        requires_dist = [line.split(":", 1)[1].strip() for line in text.splitlines() if line.startswith("Requires-Dist:")]
        rows.append(
            {
                "name": name,
                "version": version,
                "category": "direct",
                "wheel": wheel.name,
                "bytes": wheel.stat().st_size,
                "sha256": actual,
                "official_registry_hash_match": True,
                "registry": f"https://pypi.org/project/{name}/{version}/",
                "requires_python": metadata["info"].get("requires_python"),
                "requires_dist": requires_dist,
                "wheel_traversal_candidates": traversal,
                "installation_state": "PLANNED_AFTER_X1_EQUALITY",
            }
        )
    return rows


def build(wheelhouse: Path) -> dict[str, object]:
    if git("rev-parse", "HEAD").decode().strip() != SOURCE:
        raise ValueError("x1 builder must run at the immutable source")
    inherited_payload = read_git_json(SOURCE + ":docs/ilyan-reed/v685-v8/x1/new-proposals.json")
    inherited_rows = inherited_payload["proposals"]
    if len(inherited_rows) != 200:
        raise ValueError("Expected exactly 200 inherited Ilyan proposals")
    inherited = [
        {
            "source_commit": SOURCE,
            "source_path": "docs/ilyan-reed/v685-v8/x1/new-proposals.json",
            "source_record": row,
            "source_record_sha256": digest(row),
            "novelty_credit": 0,
            "execution_credit": 0,
        }
        for row in inherited_rows
    ]
    proposals = []
    for family_index, spec in enumerate(FAMILIES):
        for title, data, expected in spec["cases"]:
            proposal_id = f"NS6861-N{len(proposals) + 1:03d}"
            proposals.append(
                {
                    "proposal_id": proposal_id,
                    "family": spec["name"],
                    "runner": spec["runner"],
                    "operation": spec["operation"],
                    "title": title,
                    "mission": spec["mission"],
                    "practice": PRACTICES[min(family_index // 5, 3)],
                    "pillar": (
                        "GMUT Mind"
                        if family_index == 18
                        else "Freed ID and CBR Heart"
                        if family_index in (17, 19)
                        else "THOS Body"
                    ),
                    "source_refs": [spec["source"]],
                    "source_status": "current" if spec["source"] in (SIMPY, FSM, CSP, STATS) else "stable",
                    "hypothesis": "The new report-integrity runner yields the preregistered result for this exact synthetic input and rejects a fabricated envelope.",
                    "null_or_failure": "Computed result differs, the report is fabricated, the input mutates, or evidence is promoted beyond this named scope.",
                    "falsifier": "Compare strict canonical JSON and types; reject each of five preregistered envelope mutations.",
                    "rollback": "Quarantine the proposal and retain its input, expected report, failure, and any separately attributable correction.",
                    "expected_execution_disposition": spec["expected_execution_disposition"],
                    "approval_class": "safe_now" if family_index < 17 else "candidate",
                    "lane": "x2_build_task",
                    "input": data,
                    "expected_result": expected,
                    "preregistered_mutations": [
                        "fabricated_report",
                        "stale_definition_digest",
                        "phase_epoch_inversion",
                        "empirical_promotion",
                        "authority_promotion",
                    ],
                    "protected_gates": GATES,
                }
            )
    if len(proposals) != 200:
        raise ValueError("Expected 200 new proposals")

    portfolio: dict[str, object] = {"schema": "ghc.family.neris.portfolio-plan.v1", "planning_only": True, "destructive_cleanup_planned": False}
    for key, count, action in [
        ("safe_now", 300, "evaluate_report"),
        ("candidates", 250, "alternate_serialization_review"),
        ("clean_fix_refine", 300, "additive_projection"),
        ("exact_packets", 50, "preserve_exact_prerequisite"),
        ("blocked_packets", 30, "preserve_missing_evidence"),
    ]:
        rows = []
        for index in range(count):
            proposal = proposals[index % 200]
            row = {
                "task_id": f"NS6861-{key.upper()}-{index + 1:03d}",
                "proposal_id": proposal["proposal_id"],
                "action": action,
                "title": proposal["title"],
                "expected_execution_disposition": (
                    "exact_gate" if key == "exact_packets" else "open_gap" if key == "blocked_packets" else proposal["expected_execution_disposition"]
                ),
                "lane": "x2_build_task",
                "execution_credit": 0,
            }
            if key == "safe_now" and index >= 200:
                row["action"] = "verify_runner_repeatability_and_input_nonmutation"
            if key == "candidates":
                row["action"] = "review_canonical_roundtrip" if index < 200 else "review_missing_definition_refusal"
            if key == "clean_fix_refine":
                category = ["CLEAN", "FIX", "REFINE"][index // 100]
                row.update(
                    category=category,
                    action={
                        "CLEAN": "project_minimal_public_envelope",
                        "FIX": "retain_and_correct_false_report",
                        "REFINE": "derive_accessible_report_explanation",
                    }[category],
                )
            if key == "exact_packets":
                gated = proposals[190 + index % 10]
                context = ["proposed wording", "collection boundary", "contested amendment", "public export", "retention or remedy"][index // 10]
                row.update(
                    proposal_id=gated["proposal_id"],
                    title=f"{gated['title']} for {context}",
                    exact_target_class=context,
                    required_evidence="Competent action-specific authority, exact target, current affected-party review, and rollback.",
                    operation_executed=False,
                )
            if key == "blocked_packets":
                gap = proposals[180 + index % 10]
                context = ["model preparation", "future observation", "independent reproduction"][index // 10]
                row.update(
                    proposal_id=gap["proposal_id"],
                    title=f"{gap['title']} during {context}",
                    missing_evidence_context=context,
                    required_evidence="Real preregistered observation, suitable uncertainty treatment, and independent competent review.",
                    operation_executed=False,
                )
            rows.append(row)
        portfolio[key] = rows

    pair_names = [
        "ghc-family-report-timeline-state",
        "ghc-family-report-queue-replay",
        "ghc-family-report-budget-allocation",
        "ghc-family-report-separation-denominator",
        "ghc-family-report-summary-pairing",
        "ghc-family-report-histogram-stopping",
        "ghc-family-report-lineage-fixity",
        "ghc-family-report-correction-projection",
        "ghc-family-report-accessibility-reservations",
        "ghc-family-report-gmut-cbr-boundaries",
    ]
    skills = []
    for index, name in enumerate(pair_names):
        selected = FAMILIES[index * 2 : index * 2 + 2]
        skills.append(
            {
                "name": name,
                "families": [item["name"] for item in selected],
                "missions": [item["mission"] for item in selected],
                "source_refs": [item["source"] for item in selected],
                "promotion": "candidate_after_x2_validation_and_actual_smoke_use",
                "global_collision_checked_before_x1": True,
            }
        )
    runners = [
        {"name": f"ghc_family_report_{name}.py", "base_dependency": f"ghc_family_protocol_{name}.py", "families": [item["name"] for item in FAMILIES if item["runner"] == name]}
        for name in ["trace", "budget", "analysis", "provenance", "export"]
    ]
    next_owner_skills = [
        {"idea": idea, "boundary": "Prospective future-seat-03 owner work only; no automatic build, novelty, authority, or completion credit."}
        for idea in [
            "typed report-schema differencer",
            "phase-epoch monotonicity guard",
            "oracle provenance capsule",
            "false-summary counterexample index",
            "canonical byte-domain adjudicator",
            "portfolio denominator reconciler",
            "protected-gate language linter",
            "accessible failure-table reviewer",
            "package-attestation boundary reader",
            "one-shot receipt dependency tracer",
        ]
    ]
    next_owner_runners = [
        {"idea": idea, "boundary": "Prospective future-seat-03 owner-local software work only; no early contact or execution credit."}
        for idea in [
            "schema-delta tribunal runner",
            "monotonic epoch witness runner",
            "oracle source parity runner",
            "counterexample retention runner",
            "byte-domain comparison runner",
            "portfolio count reconciliation runner",
            "gate-language scan runner",
            "accessible table structure runner",
            "attestation metadata reader",
            "canonical dependency preflight runner",
        ]
    ]

    tokenise = lambda text: set(re.findall(r"[a-z0-9]+", text.lower()))
    inherited_titles = [(row.get("proposal_id", "unknown"), row.get("title", "")) for row in inherited_rows]
    comparisons = []
    for proposal in proposals:
        new_tokens = tokenise(proposal["title"])
        ranked = []
        for inherited_id, inherited_title in inherited_titles:
            old_tokens = tokenise(inherited_title)
            score = len(new_tokens & old_tokens) / len(new_tokens | old_tokens) if new_tokens | old_tokens else 1.0
            ranked.append((score, inherited_id, inherited_title))
        score, inherited_id, inherited_title = max(ranked)
        comparisons.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_inherited": inherited_id,
                "nearest_title": inherited_title,
                "jaccard": score,
                "exact_collision": proposal["title"].casefold() == inherited_title.casefold(),
                "quarantine": score >= 0.80,
            }
        )

    packages = package_plan(wheelhouse)
    profile = read_git_json(SOURCE + ":docs/ilyan-reed/v685-v8/x1/workflow-profile.json")
    source_repository = {
        "effective_negatives": 65519,
        "effective_methods": 82064,
        "failed_witnesses": 36367,
        "bounded_passing_witnesses": 63909,
        "open_gaps": 592,
        "exact_gates": 579,
    }
    source_activation = {
        "effective_negatives": 65523,
        "effective_methods": 82068,
        "failed_witnesses": 36371,
        "bounded_passing_witnesses": 63913,
        "open_gaps": 592,
        "exact_gates": 579,
    }
    artifacts = {
        "x1/workflow-profile.json": profile,
        "x1/inherited-selection.json": {"schema": "ghc.family.neris.inherited.v1", "rows": inherited},
        "x1/new-proposals.json": {"schema": "ghc.family.neris.proposals.v1", "planning_only": True, "proposals": proposals},
        "x1/portfolio-plan.json": portfolio,
        "x1/skill-runner-plan.json": {
            "schema": "ghc.family.neris.skill-runner-plan.v1",
            "skills": skills,
            "runners": runners,
            "global_promotions": [item["name"] for item in skills],
            "shared_runner_promotions": [item["name"] for item in runners],
            "next_owner_skills": next_owner_skills,
            "next_owner_runners": next_owner_runners,
        },
        "x1/identity-and-practice.json": {
            "owner": OWNER,
            "phase": PHASE,
            "pronouns": "they/them",
            "role": "corrigible evidence-continuity steward",
            "hope": "to make bounded claims easier to test and safer to hand onward",
            "identity_boundary": BOUNDARY,
            "priority_pillar": "Freed ID and CBR Heart",
            "practices": PRACTICES,
            "next_practice_recommendation": "data-quality investigator",
            "protected_gates": GATES,
        },
        "x1/package-plan.json": {
            "schema": "ghc.family.neris.package-plan.v1",
            "direct_additions": 3,
            "packages": packages,
            "install_after_x1_equality": True,
            "wheel_only": True,
            "require_hashes": True,
            "wheel_member_traversal_refused": True,
            "rollback_token": "NS6861-TOOLS-01",
            "rollback": "Retain the isolated environment and receipts and select prior tooling. Do not delete, mutate system Python, PATH, npm prefix, plugin caches, or sibling environments.",
            "planned_smokes": {
                "canonicaljson": ["stable key-order bytes", "non-finite value refusal"],
                "frozendict": ["set returns a new mapping", "item assignment refusal"],
                "cbor2": ["canonical map encoding roundtrip", "trailing bytes rejection by bounded decoder"],
            },
        },
        "x1/activation-source.json": {
            "source": SOURCE,
            "source_branch": "codex/GHC-Family/ilyan-reed-v685-v8-full-tools",
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_terminal_state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "source_canonical_invocation_success_replay": [1, 1, 0],
            "source_canonical_receipt_sha256": "5c87c9781deb96fa133d3bea05618190e6da397c15324a02db6740e71909d45b",
            "source_terminal_state_sha256": "58b0bf06cb2bebac39c8a7bdfd03e20ec271636b61fc7ec93e0e84281a8ca7d1",
            "source_packet_sha256": "1466dbc51dc761cb81e12913c014a23c431423b07054a0333087111b49120bf5",
            "source_manifest_entries_reverified": 1267,
            "source_manifest_failures": 0,
            "source_clean": True,
            "source_four_way_equal": True,
            "source_repository_seal": source_repository,
            "source_post_seal_external_events": 4,
            "activation_baseline": source_activation,
            "earlier_elaren_canonical_failure_retained": True,
            "earlier_elaren_canonical_success_credit": 0,
            "source_complete_repository_suite": False,
            "source_independent_reproduction": False,
        },
        "x1/route-plan.json": {
            "owner": OWNER,
            "phase": PHASE,
            "endpoint_kind": "main_task",
            "seat_role": "incumbent Neris position in the released thirty-seat cycle",
            "next_owner": "future-sibling-03-self-chosen",
            "next_phase": "v686-v2",
            "next_endpoint_kind": "main_task",
            "next_task_model": "gpt-6-astra",
            "next_task_reasoning": "max",
            "reuse_if_exact_seat_already_exists": True,
            "create_once_only_if_absent": True,
            "following_owner": "Vesper Arlen",
            "following_phase": "v686-v3",
            "delivery_state": "PREPARED_NOT_SENT",
            "terminal_gate_required": True,
            "send_count": 0,
            "creation_count_this_task": 0,
            "subagents": 0,
            "horizon": "v725-v8",
            "reset_redemption_authorized": False,
        },
        "x1/phase-truth.json": {
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "state": "PLANNING_ONLY",
            "expected_outcomes": {"completed": 170, "represented": 10, "open_gap": 10, "exact_gate": 10},
            "x2_execution_started": False,
            "declared_proposal_chain_before": 12230,
            "declared_proposal_chain_after_if_executed": 12430,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        "x1/novelty-audit.json": {
            "schema": "ghc.family.neris.source-bounded-novelty-audit.v1",
            "scope": "200 exact Ilyan source rows only; bounded lexical comparison plus family-level mission, input, falsifier, and recovery review",
            "comparisons": 40000,
            "rows": comparisons,
            "universal_novelty_claimed": False,
            "family_review": [
                {
                    "family": item["name"],
                    "new_distinction": item["mission"],
                    "changed_evidence": "A distinct frozen input and a new type-strict report-integrity envelope with repeatability and input-nonmutation witnesses.",
                    "null": "Matching mission, input semantics, falsifier, and recovery would remove Neris novelty credit.",
                    "disposition": "candidate_for_x2",
                }
                for item in FAMILIES
            ],
        },
        "x1/source-ledger.json": {
            "sources": [
                {
                    "url": url,
                    "status": "current" if url in (SIMPY, FSM, CSP, STATS) or "pypi.org" in url else "stable",
                    "checked_on": "2026-09-06",
                    "use": "Narrow software, arithmetic, provenance, serialization, accessibility, or evidence-boundary vocabulary only; no observation, conformance, independent review, or authority grant.",
                }
                for url in [
                    SIMPY,
                    FSM,
                    CSP,
                    STATS,
                    PROV,
                    WCAG,
                    VC,
                    RFC8949,
                    "https://pypi.org/project/canonicaljson/2.0.0/",
                    "https://pypi.org/project/frozendict/2.4.7/",
                    "https://pypi.org/project/cbor2/6.1.4/",
                ]
            ],
            "same_owner_only": True,
        },
        "x1/startup-methods.json": {
            "schema": "ghc.family.neris.startup-methods.v1",
            "failures": [
                {
                    "id": "NS6861-START-001",
                    "signature": "Portable plan-contract runner was incorrectly given a release profile before a populated portfolio plan existed",
                    "success_credit": 0,
                    "recovery": "Use ghc_family_release_profile.py with the generated portfolio plan as its positional input and workflow-profile.json through --profile.",
                    "state": "candidate_until_generated_plan_validation",
                },
                {
                    "id": "NS6861-START-002",
                    "signature": "First release-profile runner attempt omitted its required --profile argument",
                    "success_credit": 0,
                    "recovery": "Inspect --help, preserve this parser failure, and invoke the corrected two-input interface only after x1 materializes both files.",
                    "state": "candidate_until_generated_plan_validation",
                },
                {
                    "id": "NS6861-START-003",
                    "signature": "Sparse worktree creation crossed the output boundary while the original Git checkout held index.lock",
                    "success_credit": 0,
                    "recovery": "Do not recreate or kill it; inspect Git processes and the exact worktree Git directory, wait for the original process, then verify the resulting empty sparse lane.",
                    "state": "validated",
                },
                {
                    "id": "NS6861-START-004",
                    "signature": "Installed roster and authorization snapshots remain structurally valid but stale at v667",
                    "success_credit": 0,
                    "recovery": "Apply the newer 6 September release and exact Ilyan activation while retaining older snapshots as historical schema evidence only.",
                    "state": "validated",
                },
            ],
            "source_external_events_preserved": 4,
            "repository_bytes_changed_by_failures": 0,
        },
    }
    return artifacts


def write_json_exclusive(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")


def write_manifest(artifact_paths: list[str]) -> None:
    validation = BASE / "validation"
    allowlist_path = validation / "x1-allowlist.json"
    preflight_path = validation / "x1-preflight.json"
    manifest_path = validation / "x1-manifest.json"
    final_paths = sorted(
        artifact_paths
        + [
            "docs/neris-solane/v686-v1/validation/x1-allowlist.json",
            "docs/neris-solane/v686-v1/validation/x1-manifest.json",
            "docs/neris-solane/v686-v1/validation/x1-preflight.json",
            "scripts/build_ghc_family_neris_solane_v686_v1_x1.py",
            "tests/test_ghc_family_neris_solane_v686_v1_x1.py",
        ]
    )
    write_json_exclusive(allowlist_path, {"paths": final_paths, "zero_deletions_required": True})
    write_json_exclusive(
        preflight_path,
        {
            "source": SOURCE,
            "branch": "codex/GHC-Family/neris-solane-v686-v1-full-tools",
            "planning_only": True,
            "expected_path_count": len(final_paths),
            "materialized_files_at_empty_lane": 1,
            "materialized_file_ceiling": 2000,
            "sibling_lane_mutation": False,
            "unchanged_history_scan": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    entries = []
    for relative in final_paths:
        if relative.endswith("/x1-manifest.json"):
            continue
        content = (ROOT / relative).read_bytes().replace(b"\r\n", b"\n")
        entries.append({"path": relative, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()})
    write_json_exclusive(
        manifest_path,
        {
            "schema": "ghc.family.neris.git-blob-manifest.v1",
            "source": SOURCE,
            "hash_domain": "normalized-LF Git blob bytes",
            "entries": entries,
            "self_exclusions": ["docs/neris-solane/v686-v1/validation/x1-manifest.json"],
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheelhouse", required=True, type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    artifacts = build(args.wheelhouse)
    summary = {
        "families": len(FAMILIES),
        "planning_proposals": len(artifacts["x1/new-proposals.json"]["proposals"]),
        "inherited_rows": len(artifacts["x1/inherited-selection.json"]["rows"]),
        "novelty_quarantine": sum(row["quarantine"] for row in artifacts["x1/novelty-audit.json"]["rows"]),
        "package_count": len(artifacts["x1/package-plan.json"]["packages"]),
        "write": not args.validate_only,
    }
    if args.validate_only:
        print(json.dumps(summary, sort_keys=True))
        return 0
    relative_paths = []
    for relative, value in artifacts.items():
        destination = BASE / relative
        write_json_exclusive(destination, value)
        relative_paths.append(destination.relative_to(ROOT).as_posix())
    write_manifest(relative_paths)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
