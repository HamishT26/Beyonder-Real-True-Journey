# Four-tier deck schema

Every card is UTF-8 JSON with a deterministic `ghc-card-*` identifier. The deck
manifest stores path, byte count, and SHA-256; cards do not self-hash.

Required common fields:

- `schema`, `card_id`, `tier`, `card_type`, `title`, `parent_ids`;
- `owner`, `phase`, `stability`, and one of the four evidence outcomes;
- `content`, `source_refs`, `protected_gates`, and the relational boundary.

Parent rules:

- tier 1 has no parent;
- every tier 2 card has the tier 1 owner anchor as its single parent;
- each tier 3 practice has one tier 2 pillar parent;
- each tier 4 task has one tier 3 practice parent;
- missing targets, tier skips, multiple parents, and cycles are invalid.

Deck artifacts:

- `deck-index.json` binds order, counts, source, x1, and core outcomes;
- `stable-prefix.json` lists durable boundary cards in exact order;
- `volatile-index.json` lists task-local cards and denies implicit completion;
- `baton-index.json` lists the thirteen modular sections;
- `card-manifest.json` binds every other deck file and self-excludes only itself;
- `compact-activation.md` is a short successor pointer;
- `accessible-report.html` is structurally reviewed while manual evaluation stays reserved.

Only `completed`, `represented`, `open_gap`, and `exact_gate` are core evidence
outcomes. Portfolio expectations use `expected_execution_disposition`; they are
not observed outcomes until bounded evidence supports them.
