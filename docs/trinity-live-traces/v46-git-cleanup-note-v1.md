# V46 Git Cleanup Note

- Generated UTC: `2026-04-21T03:23:15+00:00`
- Active head: `0bcdd7ed3a9bd1cece90fe042be619544ff5f519`
- Cleanup posture: `forward_only_allowlist_only`.
- Stage only curated V46 outputs. Leave suite-generated tracked churn unstaged unless it appears in this allowlist.
- Delete only untracked generated junk after D-drive backup through `trinity_v46_cleanup_classifier.py --apply`.
