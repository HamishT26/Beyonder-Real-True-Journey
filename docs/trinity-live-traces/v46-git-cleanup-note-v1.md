# V46 Git Cleanup Note

- Generated UTC: `2026-04-21T03:24:36+00:00`
- Active head: `3b459c3bd8890c76c6bfeb29084fa543f0aa30f5`
- Cleanup posture: `forward_only_allowlist_only`.
- Stage only curated V46 outputs. Leave suite-generated tracked churn unstaged unless it appears in this allowlist.
- Delete only untracked generated junk after D-drive backup through `trinity_v46_cleanup_classifier.py --apply`.
