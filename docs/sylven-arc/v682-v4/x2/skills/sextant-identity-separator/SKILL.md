---
name: sextant-identity-separator
description: Separate a synthetic sextant record from component, custody, observation, and authority claims. Use when normalizing owner-local instrument intake fixtures.
---

# Sextant Identity Separator

Use only synthetic surrogate identifiers. Record the instrument record, component records, custody vacancy, and observation vacancy as distinct fields. Reject real serial numbers, owner claims, measurements, professional assessment, and authority promotion. Accept only `synthetic=true`, `real_row_count=0`, `observation_status=absent`, and `authority_status=reserved`.
