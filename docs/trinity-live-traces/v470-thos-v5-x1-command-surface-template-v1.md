# v470 THOS v5 x1 Command Surface Template

This template converts the v4 x2 refusal matrix into a reusable THOS command-surface frame.

## Surfaces

- Shell: allow bounded status, diff, list, read, and validation commands; block delete, move, install, and deploy without exact approval.
- Skill: allow reading `SKILL.md`, inventorying available skills, and dry-run fixtures; block installation or external mutation through a skill without scoped approval.
- Plugin or connector: allow search/read metadata when relevant; block create, update, share, send, comment, or deploy without a named target and mutation packet.
- Watcher helper: allow observation, validator summarization, and drift context; block spawning, staging, pushing, and connector mutation.

## Status Enum

All rows use only:

- `FAIL_BLOCKER`
- `OPEN_GAP`
- `NOT_RUN`
- `PASS_SHAPE_ONLY`

No row may use generic `PASS`, because `PASS_SHAPE_ONLY` keeps the claim ceiling explicit.
