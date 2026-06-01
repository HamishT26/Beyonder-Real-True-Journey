# v470 THOS v2 x1 Handoff To v2 x2

Classification: `advisory`

Next expected phase: `v470_THOS_v2_x2`

## Handoff Tasks

1. Validate required fields for every v2 x1 template.
2. Validate enum values for mutation, cleanup, authority, retention, and status fields.
3. Create pass-shape and fail-blocker fixture rows for each template.
4. Run blocked-action lint for deletion, staging, commit, push, reset, clean, connector writes, and generic runtime pass wording.
5. Run consent versus capability matrix tests.
6. Run retention privacy tests for source backlinks, minimal summaries, and non-publishable raw materials.
7. Run dirty-worktree triage fixture tests across clean, dirty known safe, dirty conflict risk, and dirty unknown.
8. Run advisory receipt authority lint.
9. Run no GMUT validation import lint over all v2 artifacts.
10. Publish only curated v2 x2 artifacts after live drift check.

Blocked until explicit approval: cleanup execution, deletion, connector writes, cloud or Drive mutation, automation edits, credential changes, broad staging, and history rewrite.
