# V41 Git Cleanup Note

- Generated UTC: `2026-04-13T16:36:52+00:00`
- Active branch head at note time: `fec4f858336e4d057306f1e49889ba4112840c2a`
- Accidental merge retained as historical context: `2531562ec3`
- Cleanup posture: `forward_only`.
- History repair actions intentionally skipped: `git reset`, `git rebase`, and merge rewrite were not used.
- Publication posture: only the curated V41 allowlist should be staged, committed, pushed, and used for PR updates.
- The large dirty tree is treated as carried-forward latest-state churn plus non-stage noise unless a path is explicitly named in the V41 allowlist.
