---
name: ghc-family-imaging-quantity-vacancy
description: Check typed imaging quantities, units, uncertainty slots, and measurement vacancy without inferring a reading or quality result.
---

# GHC Family Imaging Quantity Vacancy

Use this skill when a synthetic imaging contract names sampling, density, tone response, uniformity, target coordinates, units, or uncertainty.

Require each quantity to declare a type, unit or dimensionless status, source vocabulary, uncertainty slot, and `observed_value: null`. Reject mixed units, invented readings, absent uncertainty status, target applicability promotion, scoring, or conformance language.

Report structural acceptance separately from every vacancy. This skill does not measure a target, calibrate an instrument, estimate uncertainty, certify FADGI performance, or establish empirical evidence.
