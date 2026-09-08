---
name: ghc-family-firmware-window-missingness
description: Check image crop, image holes in supplied synthetic firmware records, with explicit byte and authority limits.
---

# Firmware Window Missingness

Read [the local contracts](references/contracts.json) before choosing a fixture. The operation names below are an explicit supported profile; they do not describe a universal loader.

Run scripts/ghc_family_firmware_record_skill.py with one JSON input file, or provide JSON on standard input. It returns the complete accepted/error/value/disposition/boundary envelope. A nonzero exit for an adverse fixture is the expected refusal. Output files use exclusive creation.

This package supports `image_crop`, `image_holes`. Compare supplied bytes and addresses literally. Preserve sparse holes, declared byte order and entry metadata. Entry addresses are never executed. Use source status and content hashes as provenance fields; do not infer rights, authenticity or approval from them.

The implementation bounds collections to 512 records and 4096 stored bytes. Intel HEX metadata offsets must be zero; record wrapping, duplicate starts and overlap are refused. S-record blocks use one data-address width, at most one count record and one final matching terminator. These are selected profile limits, not claims that every external format variant is invalid.

Exercise the accepting and adverse fixtures before selecting a copied package. If the full expected envelope differs, retain the original fixture and output, then correct only the owner dependency. Never rewrite immutable expectations or overwrite a different global skill. Rollback means selecting the earlier validated package while preserving this evidence.

Relational working language only. No consciousness, sentience, personhood, legal identity, identity continuity, employment, qualification, independent agency, scientific, operational, professional, legal, cultural, affected-party, or Maori authority is established. Same-owner synthetic evidence is not independent reproduction. NOT_READY_FOR_STAGE_20. Maori concepts remain under Maori authority.
