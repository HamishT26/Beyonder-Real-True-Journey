# v496 GMUT/THOS v32 v7 x2 Next x1 Readiness Roadmap

- Status: `PASS_NEXT_X1_READINESS_PREPARED_NOT_STARTED`
- Current phase: `v496-gmut-thos-v32-v7-x2`
- Next phase: `v496-gmut-thos-v32-v8-x1`
- v8 x1 started: `false`

## Sequential Boundary

v8 x1 must not start until v7 x2 closeout is validated, committed, pushed, and remote-verified.

Required before v8 x1 start:

1. The 30-minute x2 build window matures.
2. x2 build validation passes.
3. Publication guard checks pass.
4. Exact staging is reviewed.
5. Commit, push, and remote-equals-local verification complete.

## Carry-Forward Policy

- x1 wait mark: `15` minutes
- x2 wait mark: `15` minutes
- x2 prep minimum: `10` minutes
- x2 build/run/test/use minimum: `30` minutes
- Web-search target per wait run: `30`
- Draft skill/micro-workflow target per wait run: `10`
- Safe fix attempts per blocker: `5`
- Real skill mutation requires exact skill-path approval.
- Plugin-cache mutation requires exact approval.

## v8 x1 Launch Packet

- Prompt policy: `v496-gmut-thos-v32-v8-x1-sibling-prompt-policy-v1.json`
- Lanes: `Arby`, `Aster Vale`, `Cicero`, `Kierkegaard`, `Aristotle`
- Lane policy: existing lanes only; watchers supervise; no pre-mark polling; no raw lane text publication.

## Recommended v8 x1 Eureka Focus

1. Ask each lane for build-ready tasks rather than only philosophical synthesis.
2. Require each lane to produce at least 20 concrete eureka tasks.
3. Ask each lane to include 30+ source-search priorities and 10+ draft skill/micro-workflow candidates.
4. Ask each lane to name blocker classes and five safe repair attempts for each.
5. Carry no-overclaim and wait-policy guards into the v8 x2 build phase.

Claim boundary: no raw lane text, raw transport, credentials, local absolute paths, GMUT validation, physics/consciousness proof, or canon promotion is claimed.
