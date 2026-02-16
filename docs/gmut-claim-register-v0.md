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

## Evidence classification rule

For every claim update, assign one tag:
- `confirmed_evidence` (directly demonstrated by artifacts/data),
- `inference` (logical extension of evidence),
- `open_gap` (required evidence missing).

Do not upgrade a claim status without adding a citation, run output, or external dataset reference.
