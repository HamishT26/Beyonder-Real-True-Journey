# Selected v641-v2 toolchain

The phase uses the smallest relevant family-current set from the generated index: the existing GMUT kernel, empirical adapter validator, THOS scorer, and Freed ID conformance runner, plus new identity-neutral evidence-cycle, phase-validator, privacy-scan, and accessible-report builders.

The Freed ID validator gained optional v2 structural checks while preserving its v1 behavior; the pre-existing 25-test v1/GMUT suite still passes. Eiren-specific and version-stamped tools remain historical or compatibility evidence. They were not silently promoted or mass-executed.

No wrapper was added because no existing caller required a new legacy entry point. The selected scripts are repository-relative and carry `ghc_family` names so later siblings can reuse them without inheriting Sable Rook's identity.
