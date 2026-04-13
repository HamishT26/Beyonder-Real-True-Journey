# V41 Git Cleanup Note

- Generated UTC: `2026-04-13T16:33:13+00:00`
- Active branch head at note time: `eebb0f5dbe4f7292be6418c55d9b62a03f37bbc6`
- Accidental merge retained as historical context: `2531562ec3`
- Cleanup posture: `forward_only`.
- History repair actions intentionally skipped: `git reset`, `git rebase`, and merge rewrite were not used.
- Publication posture: only the curated V41 allowlist should be staged, committed, pushed, and used for PR updates.
- The large dirty tree is treated as carried-forward latest-state churn plus non-stage noise unless a path is explicitly named in the V41 allowlist.
