---
name: ghc-family-enclosure-hull-intersection-local
description: Inspect and execute hull intersection on bounded synthetic rational interval inputs.
---

# Hull Intersection

Compute the smallest interval containing both operands and their exact intersection. Empty intersections use null endpoints and an explicit empty flag.

Read the complete request and frozen expected envelope first. From this guide directory invoke `python -X utf8 ../../tools/ghc_family_enclosure_domain.txt` with one JSON request on standard input. The sibling `enclosure-kernel.txt` is required. The runner admits only the domain operation group and emits a complete JSON envelope. Exit 0 means accepted input, including an open-gap or exact-gate representation; exit 2 means refusal. A successful refusal test does not grant subject success.

Inputs use reduced rational strings, with numerator magnitude and denominator at most one million. Intermediate rational components are bounded to 512 bits; iteration is bounded to eight steps. Unknown fields, floating-point endpoints, reversed intervals and unsafe divisors are refused. Check one admitted request and one malformed request, retain both receipts, and compare full outputs and input immutability. If a result differs, stop selecting it and correct only the affected dependency while keeping the failed evidence.

All examples are dimensionless discrete teaching calculations. They do not establish a continuous-solution enclosure, empirical GMUT evidence, independent reproduction, production THOS or Freed ID, consciousness, personhood, identity continuity, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, deployment approval or Stage 20 readiness. Maori concepts remain under Maori authority.
