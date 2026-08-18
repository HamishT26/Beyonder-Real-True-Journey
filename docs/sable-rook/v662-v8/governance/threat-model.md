# Sable Rook v662-v8 exact-delta threat model

## Assets

Exact Git ancestry, owner attribution, immutable x1, sparse scope, changed-file
manifests, bounded declaration contracts, retained failures, privacy boundaries,
and successor-route truth.

## Threats and controls

- RDFC descriptors declare a supported algorithm, hash and poison-dataset budget but never canonicalize or hash a real dataset.
- SHACL and SPARQL checks validate bounded result shapes without executing a shape, graph, endpoint, or query.
- DCAT metadata keeps access and download locations, media types, checksums, licenses, and rights declarative and never dereferences a URL.
- OpenPGP packet ordering and gRPC trailer checks remain syntax-only and perform no cryptographic or network operation.
- SSE, TTML and OpenTelemetry inputs enforce exact count, byte, timing and identifier budgets before any stream, media or telemetry use.
- XMP lineage identifiers remain synthetic and cannot establish custody, authorship, authenticity, ownership, provenance or legal title.
- Authentication-Results, MTA-STS, security.txt and Problem Details fixtures cannot authenticate mail, deploy policy, authorize disclosure or expose a real service.
- The interlibrary-loan practice lens uses fictional requests and records; privacy, access, remedy, legal, cultural and Maori-authority decisions remain exact-gated.
- Scope remains the exact owner delta and literal test dependencies under the 2,000-file ceiling.
- One canonical success is permitted and never replayed; exact-title reread and acknowledgement are required for delivery.

## Residual risk

This is not exhaustive security, platform completeness, production assurance,
complete privacy or accessibility, independent reproduction, legal review,
cultural ratification, or Maori authority. Residual risks remain exact-gated.
