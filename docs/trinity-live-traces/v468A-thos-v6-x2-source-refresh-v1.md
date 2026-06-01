# v468A THOS v6 x2 Source Refresh

Twenty targeted searches were completed for JSON Schema draft 2020-12, Python validator availability, cross-runtime validator caveats, GitHub security/provenance paths, Python guard primitives, MCP schema routing, and Google Drive upload boundaries.

Decision: use the already-installed `jsonschema.Draft202012Validator` as an optional local validator, vendor no new dependency, mutate no cloud state, and keep the THOS schema as operational scaffolding only.

Boundary: these sources support THOS artifact validation and publication hygiene. They do not validate GMUT, close physics gates, prove consciousness, approve cleanup, or approve cloud writes.
