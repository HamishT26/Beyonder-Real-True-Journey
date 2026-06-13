# Live Skill Evolution Approval Packet

- phase_slug: `v491-gmut-thos-v27-v1-x2`
- version_label: `v491-x2-cli-final-marker-blocker`
- status: `approval_required_before_live_skill_mutation`
- approved repo work already performed: `draft artifacts and runner scripts only`

## Proposed Live Scope
- Update the existing multi-agent orchestration operations skill frontmatter and body from the draft artifact.
- Preserve the original skill backup locally if live mutation is later approved.
- Verify YAML frontmatter after any approved live mutation.
- Do not edit unrelated skills, plugin cache files, account settings, or app state.

## Current Issues
- `ISSUE-NONE-DETECTED`: no open issue found in curated receipts for this phase.

## Enhancements
- `ENH-01` background_notifier_completion_contract: Use one runner to coordinate app completion and CLI final-marker status while keeping temp output unpublished.
- `ENH-02` local_multiplex_status_board: Show all five sibling lanes in one status surface without creating new threads.
- `ENH-03` fix_enhancement_plan_sandbox: Turn recurring open gaps into bounded repair plans and approval packets.
- `ENH-04` multi_agent_orchestration_skill_draft: Prepare a draft evolved orchestration skill before any live skill mutation.
- `ENH-05` future_background_detach_gate: Add a detached watcher mode only after a separate exact approval covers persistent processes.

## Mandatory Pause Conditions
- Any live path outside the named skill is needed.
- Any body-preserving rule cannot be satisfied.
- Any auth-material or nonpublic payload appears.
- Any external account, plugin cache, or app state mutation is required.
