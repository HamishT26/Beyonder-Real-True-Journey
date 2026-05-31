# v464A Restart Automation Prompt

Status: manual paste required.

No callable `automation_update` tool is exposed in this session, and Computer Use must not automate the Codex Desktop UI. Use this as a paste-ready prompt for manual automation setup.

Recommended schedule: every 2 hours for restart/catchup mode, or every 40 minutes once `v464A_GMUT_v1` heartbeat mode is resumed.

```xml
<heartbeat>
  <automation_id>aletheon</automation_id>
  <instructions>
v464A-v490A GMUT/THOS Restart Heartbeat v1.

Project authority: D:/GHC-Archives/worktrees/v58-omega. If cwd differs, set it there.

At heartbeat start: record current Pacific/Auckland local time/date, fetch, read local HEAD, read upstream HEAD, record drift, and treat live Git verification as authoritative.

Current durable baseline: v463A_GMUT_v8 is published and remote-verified at cc0c9f630eda7096f2db4098313cda8410628553. Next expected phase is v464A_GMUT_v1 only if live artifact verification agrees.

Strict sibling rule: do not spawn new siblings through the old sub-agent spawning system. If callable main-thread creation tools are not exposed, do not create replacement siblings; use existing reachable lanes only. Arby and Aster Vale must remain non-ephemeral read-only advisory lanes. Parfit/Lorentz remains standby until safely reconnected. Do not fabricate Orun, Ari, Parfit, or Lorentz advisories.

GMUT phases: v464A through v475A, v1-v8 each unless Hamish changes scope. THOS phases: v476A through v490A, v1-v8 each unless Hamish changes scope.

Carry all six GMUT gates open until exact closure artifacts exist: null recovery; dimensional/SI consistency; conservation or exchange law; baseline recovery; fifth-force/equivalence constraints; consciousness measurement bridge.

Claim taxonomy: evidence, context, hypothesis, blocker, advisory, open_gap, journey_context_not_canon. Do not claim GMUT validation, final physics, solved consciousness, empirical spiritual proof, fifth-force safety, or canon promotion.

Journey/Solas material: use only as journey_context_not_canon with local path/line references. Do not treat it as physics validation or canon proof.

v464A_GMUT_v1 target: produce open-gate ledger, coefficient/SI dictionary scaffold, scalar-route scope, null/baseline ladder, conservation/exchange choice ledger, fifth-force/equivalence map, consciousness proxy bridge, and run-status pair. If scope is too large, publish blockers honestly.

Before any shared commit/push: fetch, drift-check, forward-only merge only if needed, curated stage only, JSON parse, credential/path/raw-log/session/screenshot guard, whitespace check, staged diff review, commit, push, and verify remote equals local.

Never reset, rebase, force-push, broadly stage, stage raw logs/session JSONL/screenshots/credential material, or delete worktrees/junk without explicit separate approval.
  </instructions>
</heartbeat>
```
