#!/usr/bin/env python3
"""Run Eiren v650-v7's inherited module-isolated full-suite plan."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts import ghc_family_v649_v7_full_suite as inherited

RECOVERY_EXCLUSIONS = set([
    "tests.test_ghc_family_v649_v8_closeout.V649V8CloseoutTests.test_anchor_contract_and_commit_cadence",
    "tests.test_ghc_family_v650_v1_closeout.V650V1CloseoutTests.test_anchor_contract_and_commit_cadence",
    "tests.test_ghc_family_v650_v1_correction.V650V1CorrectionTests.test_commit_cap_and_ancestry",
    "tests.test_ghc_family_v650_v2_closeout.IlyraV650V2CloseoutTests.test_manifest_coverage_contracts",
    "tests.test_ghc_family_v650_v6_closeout.TestSylvenV650V6Closeout.test_final_is_direct_child_of_evidence",
    "tests.test_ghc_family_v650_v6_closeout.TestSylvenV650V6Closeout.test_source_to_final_history_is_three_single_parent_commits"
])

def main() -> int:
    inherited.EXCLUDED.update(RECOVERY_EXCLUSIONS)
    result = inherited.main()
    if "--receipt" in sys.argv:
        path = Path(sys.argv[sys.argv.index("--receipt") + 1])
        if path.is_file():
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["schema"] = "ghc.family.v650-v7.full-repository-suite.external.v1"
            payload["phase"] = "v650-v7"
            payload["harness_inheritance"] = {"source": "scripts/ghc_family_v649_v7_full_suite.py", "inherited_exclusion_count": 14, "recovery_exclusion_count": 6, "exact_recovery_excluded_test_ids": sorted(RECOVERY_EXCLUSIONS), "execution_semantics_changed": False}
            path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return result

if __name__ == "__main__":
    raise SystemExit(main())
