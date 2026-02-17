# GMUT Claim Register v0 (Evidence-Bounded)

Purpose: track GMUT claims in a falsifiable format and keep each claim tied to concrete evidence and next tests.

Statuses:
- `conceptual` = phrased but not yet numerically test-ready.
- `simulatable` = implementable in local sandbox/simulation.
- `externally_testable` = can be checked against external/public datasets or experiments.

---

## Claim matrix

| claim_id | claim_statement | source | observable | comparator_model | status | evidence_now | next_falsification_test |
|---|---|---|---|---|---|---|---|
| GMUT-001 | A weakly coupled scalar consciousness field can be added to EH+SM without immediately contradicting low-energy behavior. | `gmut_lagrangian.md` | Effective coupling bounds (`lambda_psi`, `beta_psi`) | LambdaCDM + GR + SM effective-field limits | conceptual | Lagrangian term and weak-coupling intent are documented. | Derive explicit parameter bounds and reject parameter regions violating fifth-force/lab constraints. |
| GMUT-002 | The psi field can induce frequency-dependent modifications in gravitational-wave spectra. | `gmut_predictions.md`; `trinity_simulation_engine.py` | Spectrum deviation ratio vs frequency | GR stochastic background templates | simulatable | Local simulator computes modified/baseline energy density ratios. | Produce parameter sweep curves and specify exclusion criteria relative to PTA/LISA sensitivity envelopes. |
| GMUT-003 | GMUT effects may appear as low-frequency anomalies detectable by PTAs. | `gmut_predictions.md` | PTA residual spectral slope/shape | Standard PTA background fits | conceptual | Prediction direction is stated, but no fit function is defined. | Define exact anomaly functional form and run goodness-of-fit against public PTA posterior samples. |
| GMUT-004 | Psi dynamics could contribute to dark-energy behavior through slow-roll-like evolution. | `gmut_predictions.md`; `gmut_lagrangian.md` | Equation-of-state evolution `w(z)` | LambdaCDM (`w = -1`) and CPL models | conceptual | Cosmology linkage is described qualitatively. | Derive `w(z)` from a specific `V(psi)` and test against survey constraints. |
| GMUT-005 | Psi-mediated couplings must remain below current fifth-force bounds. | `gmut_predictions.md`; `gmut_lagrangian.md` | Effective force-strength limits | Existing torsion-balance/LLR constraints | externally_testable | Constraint class is identified explicitly. | Map model couplings to force range/strength and compare numerically with published limits. |
| GMUT-006 | Psi interactions might shift coherence/decoherence signatures in precision quantum systems. | `gmut_predictions.md` | Decoherence-rate residuals | Standard open-quantum-system noise models | conceptual | Candidate experimental channels are listed. | Define signal model and compute detectability thresholds on representative setups. |
| GMUT-007 | A compact simulation sandbox is useful for iterating parameter-level GMUT hypotheses before external validation. | `trinity_simulation_engine.py`; `run_simulation.py` | Reproducible simulated ratios across gamma sweep | N/A (engineering claim) | simulatable | Command-line runs currently succeed and produce stable outputs. | Add seeded regression test and expected output bands per gamma profile. |

---

## Parameter and rejection criteria v1 (working bounds)

Important: these are **engineering guardrails for iterative validation**, not externally confirmed physics constraints.

| claim_id | parameter | working_bound | rejection_condition | evidence_tag |
|---|---|---|---|---|
| GMUT-001 | `lambda_psi`, `beta_psi` effective couplings | Start with exploratory magnitude cap `<= 1e-6` until external fit stage | Reject trial set if couplings exceed cap without new empirical justification note | open_gap |
| GMUT-002 | Simulation coupling `gamma` | Baseline sweep range `0.0 <= gamma <= 0.2` for stable sandbox comparison | Reject sweep if ratio calculations are non-monotonic due to numerical instability or parser failure | confirmed_evidence |
| GMUT-002 | Ratio span (`max_ratio - min_ratio`) in baseline sweep | Keep span within expected sandbox band (`<= 0.25`) unless explicitly testing stress mode | Reject run as benchmark-grade if span exceeds threshold without stress-mode flag | inference |
| GMUT-003 | PTA anomaly fit residual | Require explicit model function and residual threshold declaration before status promotion | Reject promotion to `externally_testable` until residual metric + dataset link are present | open_gap |
| GMUT-004 | Dark-energy `w(z)` derivation readiness | Require explicit potential form `V(psi)` + derived `w(z)` expression | Reject cosmology claim promotion until derivation and target-survey comparator are attached | open_gap |
| GMUT-007 | Reproducibility consistency | Require fixed-seed/same-input rerun tolerance note | Reject benchmark label when repeated runs diverge without documented stochastic allowance | inference |

---

## External comparator datasets v1 (public reference anchors)

These references are comparator anchors for externally-testable progression, not endorsements of GMUT validity.

| claim_id | comparator_dataset | public_reference_url | intended_use_in_validation |
|---|---|---|---|
| GMUT-002 | LIGO/Virgo/KAGRA Open Data (GWOSC) | https://www.gw-openscience.org | Compare frequency-domain residual behavior against baseline GR templates. |
| GMUT-003 | NANOGrav 15-year data set | https://nanograv.org/science/data/15-year-data-set | Evaluate PTA low-frequency anomaly fit form and residual thresholds. |
| GMUT-003 | EPTA DR2 | https://www.epta.eu.org/epta-dr2 | Cross-check PTA anomaly consistency across collaborations. |
| GMUT-004 | Planck Legacy Archive | https://pla.esac.esa.int | Constrain cosmology parameters when deriving candidate `w(z)` behavior. |
| GMUT-004 | DESI public data portal | https://data.desi.lbl.gov/public | Compare large-scale structure predictions vs baseline cosmology fits. |
| GMUT-005 | Eot-Wash equivalence principle and inverse-square tests | https://www.npl.washington.edu/eotwash | Benchmark scalar fifth-force coupling constraints. |
| GMUT-005 | MICROSCOPE mission resources | https://microscope.cnes.fr/en | Additional equivalence-principle constraint anchor for coupling rejection regions. |
| GMUT-006 | Neutrino Open Data (IceCube) | https://icecube.wisc.edu/science/data/ | Candidate channel for coherence/decoherence signal bounds exploration. |

Promotion rule for externally-testable claims:
1. attach at least one comparator dataset anchor,
2. define explicit fit/error metric,
3. define rejection threshold before claiming readiness uplift.

---

## GMUT-005 external-anchor numeric exclusion note v2

Published via:
- `scripts/gmut_external_anchor_exclusion_note.py`
- canonical inputs: `docs/mind-track-external-anchor-canonical-inputs-v1.json`
- canonical ingestion checklist: `docs/mind-track-external-anchor-ingestion-notes-v0.md`
- latest artifact: `docs/mind-track-gmut-anchor-exclusion-latest.{json,md}`

Current result snapshot (latest):
- `overall_status`: `WARN`,
- external-bound rows now carry required confidence + uncertainty fields,
- canonical rows now include extraction trace IDs + uncertainty propagation metadata,
- rows are treated as canonical-ingested inputs, but current GMUT working bound
  still overhangs anchors by large factors.

Interpretation:
- `confirmed_evidence`: note generation is reproducible and machine-readable each cycle.
- `inference`: numeric overhang suggests parameter tightening is required before any readiness uplift.
- `open_gap`: attach source-side extraction trace artifacts (not just IDs) and propagate uncertainty through parameter-mapping math with reviewable equations.

### Source-extraction linkage (Caelis 17 Feb 2026)

Source-side extraction artifacts for the three canonical GMUT-005 anchors (MICROSCOPE, EOTWASH, LLR) are in `docs/mind-track-source-extraction-artifacts-v0.md`. Each anchor row has a source-side artifact and an explicit uncertainty equation. This partially addresses the `open_gap` above (trace artifacts attached); remaining step: propagate uncertainty through parameter-mapping math with reviewable equations before readiness uplift.

### Uncertainty propagation in parameter-mapping (stub v0)

To close the GMUT-005 evidence gap, anchor effective bounds (from the source-extraction doc) must be mapped into GMUT parameter space (e.g. effective coupling or force-range) with explicit uncertainty propagation.

**Parameter-mapping intent:** Define a mapping from each anchor’s *effective_upper_bound* (and its uncertainty) into one or more GMUT parameters (e.g. `lambda_psi`, `beta_psi`, or a single effective fifth-force strength). The mapping is model-dependent (weak-field approximation, scalar–matter coupling, etc.) and must be documented per anchor.

**Uncertainty propagation equation (stub):** For a derived GMUT parameter `g` that is a function of anchor bounds `b_1, b_2, ...` (each with standard uncertainty `σ(b_i)` from the source-extraction artifacts), assume independent uncertainties and use:

```
σ²(g) = Σ_i (∂g/∂b_i)² σ²(b_i)
```

For a single-anchor bound used as a direct cap (e.g. `g = f(b)` with `f` monotonic), the derived uncertainty on `g` is `σ(g) ≈ |∂g/∂b| σ(b)`. Anchor-side `effective_upper_bound` and `external_uncertainty_abs` are defined in `docs/mind-track-source-extraction-artifacts-v0.md`; assign `σ(b)` from those fields (or from a stated convention) before applying this stub.

**Next implementation step:** Implement the concrete mapping functions and partial derivatives (or Monte Carlo sampling over anchor uncertainties) in the mind-track comparator or exclusion-note pipeline so that GMUT-005 exclusion statements carry a reviewable uncertainty on the derived parameter.

**One anchor-specific mapping example (MICROSCOPE):** For anchor `MICROSCOPE_EP_eta_primary`, let `b = effective_upper_bound` (1.2e-14) and `σ(b) = external_uncertainty_abs` (2e-15) from `docs/mind-track-source-extraction-artifacts-v0.md`. Suppose a linear cap in GMUT parameter space: `g = k * b`, where `g` is an effective coupling bound and `k` a model-dependent constant (e.g. from weak-field scalar–matter mapping). Then `σ(g) = |k| σ(b)`. With the stated values, `σ(g) = |k| × 2e-15`. Implementing this in the exclusion pipeline would attach a numeric uncertainty to the derived GMUT bound for this anchor; the same pattern extends to EOTWASH and LLR with their respective `b` and `σ(b)`.

---

## Evidence classification rule

For every claim update, assign one tag:
- `confirmed_evidence` (directly demonstrated by artifacts/data),
- `inference` (logical extension of evidence),
- `open_gap` (required evidence missing).

Do not upgrade a claim status without adding a citation, run output, or external dataset reference.
