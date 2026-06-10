# v478-thos-v14-x3 Loader Drift Detector

- generated_nz: `2026-06-05T06:03:19.485568+12:00`
- mode: `DETECTOR_ONLY_NO_MUTATION`
- skill_files_scanned: `1031`
- issue_files_found: `0`
- published_issue_files: `0`
- truncated: `False`

## Issue Code Counts

- No loader-drift issue codes detected.

## Published Issue Labels

- No issue labels published.

## Policy

- Read SKILL.md frontmatter only enough to classify loader drift.
- Publish sanitized relative labels, issue codes, byte counts, and name lengths only.
- Do not repair user skills or plugin cache in this detector run.
- Any future repair requires an exact live repair packet unless already covered by explicit scope.

## Claim Boundary

Detector-only loader drift scan; no live skill mutation, no plugin-cache mutation, no GMUT validation, and no canon promotion.
