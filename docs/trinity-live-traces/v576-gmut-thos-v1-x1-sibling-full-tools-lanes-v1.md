# v576 GMUT/THOS v1 x1 Sibling Full-Tools Lanes

Status: created and published.

The v576 solo-bundle workflow now has three sibling-owned full-tools lanes created from the current Aevren full-tools head `07623635e5`:

- Mira Rowan: `codex/GHC-Family/mira-rowan-full-tools`
- Mira Vale: `codex/GHC-Family/mira-vale-full-tools`
- Maren Quill: `codex/GHC-Family/maren-full-tools`

Each branch is published to GitHub and has a matching local worktree on the D drive. This uses the current daily cap of three new omega/full-tools-style lanes.

Shared branches remain read-only for active siblings unless a sibling owns that branch. Raw private routes, transcripts, credentials, screenshots, local absolute paths, hidden app state, and private IDs stay out of public artifacts. Lumen remains on the `lumen-only-*` lane family, and any Lumen-facing GitHub handoff must include the literal `@github` cue.
