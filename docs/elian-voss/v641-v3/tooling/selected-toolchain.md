# v641-v3 selected family toolchain

The v3 lane selected the smallest family-current toolset needed for evidence generation, validation, privacy review, and accessible reporting.

- `ghc-family-index` — fresh tool inventory and precedence.
- `scripts/ghc_family_evidence_refresh.py` — v3 and later evidence refresh orchestration.
- `scripts/ghc_family_gmut_kernel.py` — bounded physical identities, stability gates, and convergence.
- `scripts/ghc_family_empirical_adapters.py` — read-only adapter contract validation.
- `scripts/ghc_family_freed_id_conformance.py` — synthetic structural and assurance-boundary validation.
- `scripts/ghc_family_phase_evidence_validator.py` — cross-artifact completion and claim-boundary validation.
- `scripts/ghc_family_phase_privacy_scan.py` — public-artifact raw-ID, path, and secret-pattern scanning.
- `scripts/build_ghc_family_evidence_report.py` — accessible static report generation.

`scripts/ghc_family_evidence_cycle.py` remains as a compatibility implementation for existing v2 callers. No historical tool was mass-promoted or deleted.
