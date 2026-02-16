# Aurelis Memory Integrity Report

Checks passed: **6/6**

Mode: **strict**

## Check results
- jsonl_exists_and_nonempty: **PASS** (rows=4)
- markdown_entry_count_matches_jsonl: **PASS** (md_entries=4, jsonl_rows=4)
- summary_entry_count_expected: **PASS** (summary=4, expected=4)
- next_steps_references_latest_timestamp: **PASS** (latest_ts=2026-02-16T03:50:41.682630+00:00)
- strict_required_fields_present: **PASS** (missing_or_empty_fields=0)
- strict_timestamp_monotonic_non_decreasing: **PASS** (ordering_violations=0)
