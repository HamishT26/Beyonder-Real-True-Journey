# v496 GMUT/THOS v32 v7 x2 Skill Overlay Approval Candidate

- Status: `PENDING_USER_APPROVAL`
- Current run real skill creation performed: `false`
- Current run real skill disable performed: `false`
- Enabled/Disabled labels are planning overlay only: `true`

## Objective

Authorize exact future creation or update of wait-run skills and explicit Enabled/Disabled labels without broad user-skill or plugin-cache mutation.

## Candidate Enabled Skill Slugs

1. `wait-alpha-task-operations`
2. `no-babysit-cadence-guard`
3. `x2-build-session-gate`
4. `skill-inventory-auditor`
5. `command-risk-summarizer`
6. `source-ledger-weaver`
7. `no-overclaim-guard`
8. `connector-boundary-watch`
9. `stale-flow-retry-ladder`
10. `trinity-mandala-mapper`

## Candidate Disabled Policy Labels

1. `broad-user-skill-mutation`
2. `plugin-cache-mutation`
3. `raw-lane-publication`
4. `external-account-mutation`
5. `raw-session-stream-publication`

## Future Approval Terms

1. Name every exact skill slug to create or edit.
2. Preserve a local backup before editing any existing user skill.
3. Verify YAML frontmatter includes `name` and `description`.
4. Do not edit plugin-cache skills.
5. Do not edit unrelated skills.
6. Do not disable existing functional skills unless their exact path and replacement are named.
7. Run skill syntax checks and no-overclaim guards before publication.
8. Publish only curated receipts, never raw skill-cache dumps or private app state.

Claim boundary: this is an approval candidate only. It does not create, install, disable, or mutate real skills.
