# Aurelis Memory Integrity Report

Checks passed: **6/6**

Mode: **strict**

## Check results
- jsonl_exists_and_nonempty: **PASS** (rows=1)
- markdown_entry_count_matches_jsonl: **PASS** (md_entries=1, jsonl_rows=1)
- summary_entry_count_expected: **PASS** (summary=1, expected=1)
- next_steps_references_latest_timestamp: **PASS** (latest_ts=2026-02-16T01:08:39.584644+00:00)
- strict_required_fields_present: **PASS** (missing_or_empty_fields=0)
- strict_timestamp_monotonic_non_decreasing: **PASS** (rows<2)
