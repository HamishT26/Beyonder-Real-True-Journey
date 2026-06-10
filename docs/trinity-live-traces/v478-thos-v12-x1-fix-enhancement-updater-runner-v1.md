# v478-thos-v12-x1 Fix Enhancement Updater Runner

- generated_nz: `2026-06-04T16:23:48+12:00`
- overall_status: `PASS_WITH_LIVE_SKILL_APPROVAL_REQUIRED`
- policy: repo-runner design only; no live skill mutation; no persistent process started.
- claim boundary: fix and enhancement planning only; all GMUT gates remain open.

## Issues
- `ISSUE-BACKGROUND-PARTIAL` / `open`: background runner can fuse app success with CLI open gap but cannot force final markers. Repair class `background_completion_policy`.
- `ISSUE-MULTIPLEX-CLI-OPEN` / `open`: multiplex board can display app readiness while CLI lanes remain open. Repair class `operator_visibility`.

## Enhancements
- `ENH-01` background_notifier_completion_contract: Use one runner to coordinate app completion and CLI final-marker status while keeping temp output unpublished. Scope `repo_script_only`.
- `ENH-02` local_multiplex_status_board: Show all five sibling lanes in one status surface without creating new threads. Scope `repo_script_only`.
- `ENH-03` fix_enhancement_plan_sandbox: Turn recurring open gaps into bounded repair plans and approval packets. Scope `repo_script_only`.
- `ENH-04` multi_agent_orchestration_skill_draft: Prepare a draft evolved orchestration skill before any live skill mutation. Scope `draft_artifact_only`.
- `ENH-05` future_background_detach_gate: Add a detached watcher mode only after a separate exact approval covers persistent processes. Scope `approval_required`.
