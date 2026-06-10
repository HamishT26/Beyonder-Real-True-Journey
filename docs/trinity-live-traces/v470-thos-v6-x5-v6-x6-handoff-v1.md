# v470 THOS v6 x5 to v6 x6 Handoff

v6 x5 externalized the visualization/report rows, added a row-universe checker, generated a deterministic digest, and rehearsed duplicate, unknown-status, and missing-field failures in tempdir-only payloads.

## v6 x6 Focus

v6 x6 should make the digest richer and the visualization cleaner. The best next steps are to include status/provenance in the digest or document why not, and to have the HTML visualization consume externalized JSON instead of duplicating embedded rows.

## Open Work

- Add mixed-invalid payload rehearsal.
- Add rejected-row count buckets to checker output.
- Convert manual count model into executable checker output.
- Preserve local-only scope and open GMUT gates.

## Open Gates

All six GMUT gates remain open. This is THOS infrastructure only.
