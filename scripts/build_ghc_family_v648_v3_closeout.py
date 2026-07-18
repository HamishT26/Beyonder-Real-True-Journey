#!/usr/bin/env python3
"""Build the Eiren Kestrel v648-v3 no-replay closeout candidate."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "build_ghc_family_v648_v1_closeout.py"
SOURCE = "227a764b2bfad7a601bf45dcbacc1e37ffa5bb62"
X1 = "bd21b594451226294528f4f72f138bdada6cb3af"
EVIDENCE = "240aacba289cbc58280693395733da7b6450faa4"


def replace_once(source: str, old: str, new: str) -> str:
    if source.count(old) != 1:
        raise RuntimeError(f"expected one closeout-template match, found {source.count(old)}: {old[:80]!r}")
    return source.replace(old, new, 1)


def transformed_source() -> str:
    source = TEMPLATE.read_text(encoding="utf-8")
    lifecycle = '''LIFECYCLE_NEGATIVES = [
    {
        "negative_id": "V6483-LC-N01",
        "failure": "A combined status, log, and directory probe exceeded its bounded timeout without usable output.",
        "recovery": "Retain the timeout, award no clean-state credit, and split the read into an untracked-free status probe plus exact revision queries.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6483-LC-N02",
        "failure": "A read-only ripgrep expression for closeout anchors had an unclosed group and searched no files.",
        "recovery": "Retain the parser failure and use separate literal expressions for the bounded source inspection.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6483-LC-N03",
        "failure": "The first closeout adapter looked for the older Method Flow state filename and stopped before writing closeout artifacts.",
        "recovery": "Retain the adaptation miss and bind the closeout reader to Eiren's committed method-flow ledger.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6483-LC-N04",
        "failure": "The first canonical-suite launcher attempt stopped before loading or executing tests because its explicit top-level directory made the tests start directory non-importable.",
        "recovery": "Retain the pre-execution launcher failure, use unittest's native tests-directory discovery root, and distinguish launcher attempts from actual suite executions.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6483-LC-N05",
        "failure": "A read-only ripgrep test scan passed a Windows wildcard path directly to the tool and searched no files.",
        "recovery": "Retain the path error and use ripgrep's tool-native filename glob over the literal tests root.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6483-LC-N06",
        "failure": "A combined historical-head query repeated the same shell wildcard mistake for the final validator source scan.",
        "recovery": "Retain the second path error and issue literal-root ripgrep queries with explicit filename filters.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6483-LC-N07",
        "failure": "The first actual monolithic full-suite execution ran 1,417 tests and returned seven failures plus nine errors.",
        "recovery": "Retain the failed execution, bind historical exact-head assertions to their own sealed revisions, isolate test modules to prevent cross-module state, and permit one recovery execution without replay credit.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6483-LC-N08",
        "failure": "A targeted 48-test diagnostic reproduced the seven historical descendant-head failures.",
        "recovery": "Retain the diagnostic failure and validate each historical commit cap against its own final seal while retaining current-phase head checks separately.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6483-LC-N09",
        "failure": "The first targeted recovery run cleared the five sealed-commit failures but raised two NameError results because the historical test adapter omitted its subprocess import.",
        "recovery": "Retain the two-error run, add the exact standard-library import, and rerun only the bounded 48-test recovery subset.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6483-LC-N10",
        "failure": "The isolated recovery execution passed every loaded unittest case but initially classified three dependency-free direct-runner files with zero unittest cases as process errors.",
        "recovery": "Retain the classification miss, verify the exact three files define no unittest cases, and reconcile the completed receipt without executing the suite again.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6483-LC-N11",
        "failure": "The first exact staged closeout review rejected one extra blank line at the end of the new closeout test.",
        "recovery": "Retain the failed staged gate, remove only the terminal blank line, regenerate closeout counts, and repeat the exact staged-blob review.",
        "result": "retained_then_recovered",
    },
]
FINAL_EFFECTIVE_NEGATIVES'''
    source, count = re.subn(
        r"LIFECYCLE_NEGATIVES = \[.*?\]\nFINAL_EFFECTIVE_NEGATIVES",
        lifecycle,
        source,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise RuntimeError("could not replace lifecycle-negative register")

    replacements = [
        ('SOURCE = "4ada48d3142a6d33e4c723184edbb84e59e22aa4"', f'SOURCE = "{SOURCE}"'),
        ('X1 = "3e2904ec02c893d91c16e9a48fbb2485fc5d824f"', f'X1 = "{X1}"'),
        ('EVIDENCE = "b09681afe5a4cac101bab367ef761e4ac1a7b57e"', f'EVIDENCE = "{EVIDENCE}"'),
        ("EVIDENCE_NEGATIVES = 3926", "EVIDENCE_NEGATIVES = 4115"),
        ("OPEN_GAPS = 26", "OPEN_GAPS = 28"),
        ("EXACT_GATES = 27", "EXACT_GATES = 29"),
        ("METHODS = 11", "METHODS = 13"),
        ("FAILED_WITNESSES = 15", "FAILED_WITNESSES = 14"),
        ("PASSING_WITNESSES = 15", "PASSING_WITNESSES = 14"),
        ('validation["test_result"]["tests"] != 68', 'validation["test_result"]["tests"] != 76'),
        ('load("method-flow/method-flow-state.json")', 'load("method-flow/method-flow-ledger.json")'),
        ("Tamar Vey", "Eiren Kestrel"),
        ("Tamar's", "Eiren's"),
        ("tamar-vey", "eiren-kestrel"),
        ("v648-v1", "v648-v3"),
        ("v648_v1", "v648_v3"),
        ("V6481", "V6483"),
        ('"target_existing_task_title": "Sylven Arc"', '"target_existing_task_title": "Ilyra Fen"'),
        ('"target_phase": "v648-gmut-thos-v2-x1-x2"', '"target_phase": "v648-gmut-thos-v4-x1-x2"'),
        ("single verified Sylven Arc baton", "single verified Ilyra Fen baton"),
        ('"cleanup_completed": 30', '"cleanup_completed": 60'),
        ("thirty additive cleanup tasks", "sixty additive cleanup tasks"),
        ("real DES Y3 analysis or GMUT likelihood", "real DESI DR2 Lyman-alpha analysis or GMUT likelihood"),
    ]
    for old, new in replacements:
        source = source.replace(old, new)

    source, count = re.subn(
        r"BOUNDARY = \(.*?\n\)\n\n\ndef load",
        '''BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains represented; "
    "Freed ID remains synthetic and nonproduction; CBR, identity-incident notification, privacy, "
    "remedy, legal, affected-party, cultural, tangata whenua, iwi, hapu, and Maori authority remain "
    "with competent and affected authorities. No empirical confirmation, Theory of Everything, AGI "
    "or ASI, consciousness, personhood, production deployment, privacy-complete, exhaustive-security, "
    "independent-reproduction, accessibility-complete, professional, legal, proof or canon, or Stage "
    "20 claim is made."
)


def load''',
        source,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise RuntimeError("could not replace closeout boundary")

    method_guard = '''    if methods["counts"]["witness_results"] != {"fail": FAILED_WITNESSES, "pass": PASSING_WITNESSES}:
        raise RuntimeError("Method Flow failed and passing witnesses are incomplete")
'''
    suite_guard = method_guard + '''
    suite_path = PHASE / "validation/full-repository-suite.json"
    full_suite = load("validation/full-repository-suite.json") if suite_path.exists() else None
    full_suite_ok = bool(
        full_suite
        and full_suite.get("canonical") is True
        and full_suite.get("owner") == "Eiren Kestrel"
        and full_suite.get("successful") is True
        and full_suite.get("replay_executed") is False
        and full_suite.get("independent_reproduction") is False
    )
    full_suite_tests = full_suite.get("tests_run", 0) if full_suite else 0
'''
    source = replace_once(source, method_guard, suite_guard)

    source = replace_once(
        source,
        '        "full_repository_suite_run": False,\n        "full_repository_suite_owner": "Eiren Kestrel",',
        '        "full_repository_suite_run": full_suite_ok,\n'
        '        "full_repository_suite_owner": "Eiren Kestrel",\n'
        '        "full_repository_suite_tests": full_suite_tests,\n'
        '        "full_repository_suite_receipt": "validation/full-repository-suite.json" if full_suite_ok else None,\n'
        '        "replay_executed": False,\n'
        '        "repeatability_credit": 0,',
    )
    source = replace_once(
        source,
        '            "named_replay_required": True,',
        '            "named_replay_required": False,\n'
        '            "replay_prohibited_by_latest_user_instruction": True,\n'
        '            "full_repository_suite_required": True,\n'
        '            "full_repository_suite_complete": full_suite_ok,',
    )
    source = replace_once(
        source,
        '        "named_replay_passed": False,',
        '        "named_replay_required": False,\n'
        '        "replay_executed": False,\n'
        '        "repeatability_credit": 0,\n'
        '        "full_repository_suite_passed": full_suite_ok,',
    )
    source = replace_once(
        source,
        '''            "named_replay_requirements": [
                "one local-only named branch and worktree at exact final head",
                "not detached, pushed, canonical, assigned upstream, or present as a live remote ref",
                "same bounded validation exactly once",
                "clean before and after",
            ],
            "full_repository_suite": "not run; Eiren-only under the current refinement",''',
        '''            "named_replay_requirements": [],
            "replay_policy": "PROHIBITED_BY_LATEST_USER_INSTRUCTION; zero repeatability credit",
            "full_repository_suite": {
                "required": True,
                "owner": "Eiren Kestrel",
                "canonical": True,
                "complete": full_suite_ok,
                "tests_run": full_suite_tests,
                "receipt": "validation/full-repository-suite.json" if full_suite_ok else None,
            },''',
    )
    source = replace_once(source, '            "state": "PENDING_POST_COMMIT",', '            "state": "PROHIBITED_BY_LATEST_USER_INSTRUCTION",')
    source = replace_once(source, '            "named_lane_count": 1,', '            "named_lane_count": 0,\n            "repeatability_credit": 0,')
    source = source.replace('                "one named replay",', '                "successful Eiren-owned canonical full repository suite",')
    source = source.replace('                "one local-only named replay",', '                "successful Eiren-owned canonical full repository suite",')
    source = replace_once(
        source,
        '                "four-way remote equality",',
        '                "four-way remote equality",\n                "unique exact existing Ilyra Fen task resolution",',
    )
    source = replace_once(
        source,
        '            "named_replay_pending": True,',
        '            "named_replay_pending": False,\n'
        '            "replay_prohibited": True,\n'
        '            "repeatability_credit": 0,\n'
        '            "full_repository_suite_complete": full_suite_ok,',
    )
    source = replace_once(
        source,
        '            "named_replay_state": "not_started",',
        '            "named_replay_state": "prohibited_by_latest_user_instruction",\n'
        '            "replay_executed": False,\n'
        '            "repeatability_credit": 0,\n'
        '            "full_repository_suite_state": "passed" if full_suite_ok else "pending",',
    )
    source = replace_once(
        source,
        '                "current and authorized scoped tests",',
        '                "current and authorized scoped tests",\n'
        '                "one successful Eiren-owned canonical full repository suite",',
    )
    source = replace_once(
        source,
        '                "evidence validation and retained Method Flow failures",',
        '                "evidence validation and retained Method Flow failures",\n'
        '                *(["one successful Eiren-owned canonical full repository suite"] if full_suite_ok else []),',
    )
    source = replace_once(
        source,
        '            "pending_postcommit": [',
        '            "pending_postcommit": [\n'
        '                *([] if full_suite_ok else ["one Eiren-owned canonical full repository suite"]),',
    )
    return source


def main() -> int:
    namespace = {
        "__name__": "ghc_family_v648_v3_closeout_template",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(transformed_source(), str(Path(__file__).resolve()), "exec"), namespace)
    namespace["build"]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
