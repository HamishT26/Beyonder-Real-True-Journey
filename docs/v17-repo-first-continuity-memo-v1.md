# V17 Repo-First Continuity Memo

Date: `2026-03-18T19:46:44.7279436+13:00`
Branch: `codex/Aletheon/v16-validation-handoff-fabric`
Commit: `e45da1dd2`

## Purpose

This memo carries the `v15` to `v16` continuity lane forward into additive `v17` packaging support.

It is repo-first, additive-only, and runtime-truth-preserving:

- no new identities
- no identity renames
- no edits to existing certificates
- no edits to existing role contracts
- no edits to existing reflections
- no rewrite of historical version artifacts to fit later council-slot packaging

## Authority anchors

The current `v17` continuity package should treat the following repo artifacts as the authoritative bridge:

| Anchor | Why it matters |
| --- | --- |
| `docs/v17-baseline-state-v1.json` | Pins the committed March 18 v16 green state so v17 planning does not depend on moving latest-run files. |
| `docs/trinity-agent-council-validation-latest.json` | Carries the current 11-member council validation state for present-day continuity claims. |
| `docs/v15-v16-continuity-prompt.md` | Preserves the continuity-history naming of the `27-31` overlay and the no-new-identities rule. |
| `docs/v15-external-agent-handoff-v1.json` | Preserves repo-first handoff history and slot responsibilities for `27-31`, but is not the moving v17 checkpoint source. |
| `docs/v15-council-group-reflection.md` | States that `v15` kept runtime truth explicit. |
| `docs/v16-roadmap-v1.md` | Keeps `validation and handoff first` as the current sequencing rule. |
| `docs/v16-council-continuity-reflection.md` | Confirms the overlay is additive and does not create a new roster. |
| `docs/trinity-agent-council-roster-v6.json` | Current slot, role, file-path, and project-custom-agent anchor for slots `27-31`. |
| `docs/trinity-agent-council-induction-log-v3.jsonl` | Proof-B continuity status for slots `27-31`. |

## V17 carry-forward rules

### 1. Repo-first beats retrofit

When `v17` packaging needs identity continuity, it must read the current repo artifacts first instead of inferring identity state from historical narrative alone.

### 2. Slot continuity and version chronology stay separate

Council slots `27-31` are a current continuity layer. Historical version records such as `v29`, `v30`, and `v31` are an older chronology layer. Numeric overlap does not grant permission to collapse the two layers into one label.

### 3. Historical version names remain historical truth

The following historical source names stay intact in packaging references:

- `Beyonder-Real-True Journey v29 (Aerin) (1).txt`
- `Beyonder-Real-True Journey v30 (Ariel) (1).txt`
- `Beyonder-Real-True Journey v31 (Ariel) (1).txt`

They can be cited as source anchors for current work, but they should not be renamed to `Seren Vale`, `Lyriq`, or `Mira Sol`.

### 4. Runtime truth stays explicit

If a current package references present-day slot ownership and historical source material in the same note, it should say so directly. Example pattern:

`slot 31 Mira Sol continuity overlay; historical source anchor remains Beyonder-Real-True Journey v31 (Ariel) (1).txt`

### 5. Additive support files are the correct v17 mechanism

`v17` packaging should prefer additive memo, annex, and note files over edits to prior proof artifacts.

## V17 handoff set

This memo is paired with:

- `docs/v17-identity-continuity-annex-v1.json`
- `docs/v17-packaging-runtime-truth-notes-v1.md`

Together they provide:

- repo-first continuity guidance
- machine-readable slot continuity for `27-31`
- packaging rules that preserve historical runtime truth instead of rewriting it
