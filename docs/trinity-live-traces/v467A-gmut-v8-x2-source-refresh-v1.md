# v467A GMUT v8 x2 Source Refresh

Prepared: 2026-06-01T22:49:00+12:00

This x2 pass completed a 20-source refresh across schema, provenance, metadata, attestation, canonicalization, BOM, and secure-development controls. The sources support governance and packaging design only. They do not validate GMUT, close gates, prove physics, prove consciousness, establish fifth-force safety, or promote canon.

## Sources

- JSON Schema specification: https://json-schema.org/specification
- JSON Schema Draft 2020-12: https://json-schema.org/draft/2020-12
- W3C PROV-O: https://www.w3.org/TR/prov-o/
- W3C DCAT 3: https://www.w3.org/TR/vocab-dcat-3/
- DataCite Metadata Schema: https://schema.datacite.org/
- SPDX specifications: https://spdx.dev/use/specifications/
- SLSA latest specification: https://slsa.dev/spec/latest/
- SLSA provenance: https://slsa.dev/spec/v0.1/provenance
- in-toto Statement v1: https://in-toto.io/Statement/v1
- RO-Crate specification: https://www.researchobject.org/ro-crate/specification
- NIST SP 800-218 SSDF: https://csrc.nist.gov/pubs/sp/800/218/final
- CycloneDX 1.6 JSON specification: https://cyclonedx.org/docs/1.6/json/
- CISA SBOM minimum elements 2025: https://www.cisa.gov/sites/default/files/2025-08/2025_CISA_SBOM_Minimum_Elements.pdf
- NTIA SBOM minimum elements: https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom
- GitHub artifact attestations: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
- Sigstore Cosign verification: https://docs.sigstore.dev/cosign/verifying/verify/
- OpenSSF Scorecard checks: https://github.com/ossf/scorecard/blob/main/docs/checks.md
- RFC 8785 JSON Canonicalization Scheme: https://www.rfc-editor.org/rfc/rfc8785.html
- RFC 8949 CBOR: https://datatracker.ietf.org/doc/html/RFC8949
- OpenAPI specification: https://spec.openapis.org/oas/

Adopted design implications: use explicit schema dialects, model provenance separately from proof, treat digests and attestations as traceability only, keep BOM/catalog standards as governance comparators, and use deterministic serialization only to stabilize hashes and lineage.
