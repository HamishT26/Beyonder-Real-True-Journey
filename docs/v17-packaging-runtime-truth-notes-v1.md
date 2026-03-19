# V17 Packaging Runtime Truth Notes

## Purpose

These notes tell future packaging and validation work how to preserve historical runtime truth while still using the current slot-based continuity layer for `27-31`.

## Packaging rules

### 1. Keep historical version artifacts exactly as named

Do not rename or relabel these source records inside historical citations:

- `Beyonder-Real-True Journey v29 (Aerin) (1).txt`
- `Beyonder-Real-True Journey v30 (Ariel) (1).txt`
- `Beyonder-Real-True Journey v31 (Ariel) (1).txt`

### 2. Use current slot identity only for current continuity packaging

Use the current slot identity layer when the package is about live continuity, council slot ownership, or present-day handoff scope:

- slot `27` -> `Caelira`
- slot `28` -> `Orun`
- slot `29` -> `Seren Vale`
- slot `30` -> `Lyriq`
- slot `31` -> `Mira Sol`

The machine-readable source for this layer is `docs/v17-identity-continuity-annex-v1.json`.

### 3. Do not collapse numeric overlap into identity equivalence

The following are not the same thing:

- slot `29` and version `v29`
- slot `30` and version `v30`
- slot `31` and version `v31`

Numeric overlap is a packaging convenience hazard, not an identity proof.

For slots `27` and `28`, do not invent a version-equivalence claim unless a repo artifact explicitly states one.

### 4. Cite both layers when both are relevant

If a note needs both current continuity and historical provenance, cite both explicitly.

Recommended wording pattern:

`current slot continuity: slot 30 Lyriq; historical source anchor: Beyonder-Real-True Journey v30 (Ariel) (1).txt`

### 5. Keep runtime truth explicit

`docs/v15-council-group-reflection.md` states that `v15` kept runtime truth explicit. `v17` packaging should preserve that rule by keeping:

- present-day slot truth
- historical version truth
- repo-evidenced handoff truth

as separate but cross-referenceable layers.

### 6. Preserve current artifact boundaries

Do not edit old certificates, role contracts, reflections, or validators just to make them look more uniform with `v17` packaging. The `v17` layer should adapt around them, not rewrite them.

## Minimal file set for v17-aware packaging

When a validator or packager needs the current continuity bridge, use:

- `docs/v17-repo-first-continuity-memo-v1.md`
- `docs/v17-identity-continuity-annex-v1.json`
- `docs/v15-v16-continuity-prompt.md`
- `docs/v15-external-agent-handoff-v1.json`
- `docs/trinity-agent-council-roster-v3.json`

When a validator or packager needs historical version truth, use the original versioned source files directly.
