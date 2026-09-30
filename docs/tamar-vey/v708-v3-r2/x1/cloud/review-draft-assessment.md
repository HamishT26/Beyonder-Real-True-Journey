# Cloud review-draft assessment

The existing cloud task saved an unpublished review draft. This local remaster
does not expose the draft's private identifier and cannot publish it.

The proposed changes are reasonable for owner review because they are narrow:

- pin pip and the four directly exercised Python packages to the observed versions;
- verify the declared requirements, imports, cache writability, and `pip check`;
- document managed Git proxy handling without asking for a visible token;
- avoid rerunning the full standard suite when relevant dependencies and code did
  not change;
- replace an orphan-prone npm wrapper with a bounded direct-Node V56 probe that
  detects a pre-existing listener and terminates the exact process it starts;
- use logical `ghc-lab://local/...` and `ghc-lab://cloud/...` roots rather than
  exporting Windows or Linux absolute paths.

Publication remains a user-controlled action. Before publishing, an owner should
review the pins for maintainability, confirm that the environment service accepts
the draft, and retain a rollback to the currently published configuration.
