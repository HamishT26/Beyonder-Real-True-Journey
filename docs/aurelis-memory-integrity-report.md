# Aurelis Memory Integrity Report

Checks passed: **6/6**

Mode: **strict**

## Check results
- jsonl_exists_and_nonempty: **PASS** (rows=2)
- markdown_entry_count_matches_jsonl: **PASS** (md_entries=2, jsonl_rows=2)
- summary_entry_count_expected: **PASS** (summary=2, expected=2)
- next_steps_references_latest_timestamp: **PASS** (latest_ts=2026-02-16T01:57:52.673248+00:00)
- strict_required_fields_present: **PASS** (missing_or_empty_fields=0)
- strict_timestamp_monotonic_non_decreasing: **PASS** (ordering_violations=0)
