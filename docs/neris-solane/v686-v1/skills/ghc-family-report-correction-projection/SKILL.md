---
name: ghc-family-report-correction-projection
description: "Audit synthetic immutable correction merge and minimal public projection reports with frozen typed oracles and retained failures."
---

# Report Correction Projection

Use this skill when one of the two retained families in [the frozen contracts](references/contracts.json) exactly matches a synthetic report review. Select by family and operation, not lexical resemblance. The package validates a reported JSON value against a frozen input, preserves strict JSON types, records the computed result, and verifies that the input did not mutate.

Run the matching `scripts/ghc_family_report_*.py` with `--fixture references/positive.json`. A fixture must contain `operation`, `input`, and `reported`. The adverse fixture intentionally omits a required field and must return `malformed_fixture`. Preserve that rejection rather than broadening the input silently.

The package includes five shared report tribunals and their five inherited protocol dependencies so it remains portable. Ten package copies still represent five unique new report runners. Read the exact source contract before adapting a fixture; never replace a preregistered oracle with observed output.

Primary vocabulary sources:

- [https://www.w3.org/TR/prov-o/](https://www.w3.org/TR/prov-o/)
- [https://www.w3.org/TR/vc-data-model-2.0/](https://www.w3.org/TR/vc-data-model-2.0/)

A local pass is same-owner software evidence only. It does not establish a real participant, operational system, empirical GMUT result, professional qualification, production identity lifecycle, complete privacy or accessibility, exhaustive security, independent reproduction, legal or cultural authority, Māori authority, consciousness, personhood, a Theory of Everything, canon, or Stage 20 readiness.

Rollback selects a retained prior skill or holds the affected family. It does not delete this package, a failed witness, history, or another owner's work. Neris Solane, they/them, corrigible evidence-continuity steward, the hope to make bounded claims easier to test and safer to hand onward, names, roles, hopes, pronouns, family language, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They establish no consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific, operational, professional, legal, cultural, affected-party, or Māori authority. Hamish may rename, pause, redirect, narrow, or stop the route.
