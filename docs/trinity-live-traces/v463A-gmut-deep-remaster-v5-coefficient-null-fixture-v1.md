# v463A GMUT Deep Remaster v5 Coefficient Dictionary And Null Fixture

Generated: 2026-05-29T14:12:43Z / 2026-05-30T02:12:43+12:00

Status: `coefficient_dictionary_and_null_fixture_scaffold_ready`

## Coefficient Rows

- `alpha_Psi`: scalar candidate coupling or normalization. Unit status unknown pending normalization. Default null value: `0`.
- `m_Psi`: scalar mass/range scale if the potential or fifth-force map uses a massive scalar. Requires mass dimension and range mapping.
- `V(Psi)`: scalar potential. Under the 4D natural-unit scalar fixture it should carry mass dimension 4, but no functional form is selected.
- `lambda_T`: trace or invariant source coupling. Set to `0` for the first scalar-only pass; blocked until source trace/invariant and units are defined.
- `alpha_B`: demoted and set to `0`. Not an active physical term.
- `beta_I`, `gamma_C`, `delta_S`: meta-layer only, not physical stress-energy without projection map.
- `epsilon_H`: meaning-layer only, not empirical consciousness proof without measurement bridge.

## Null-Switch Fixtures

- `all_off_baseline`: `alpha_Psi=0`, `lambda_T=0`, `alpha_B=0`, projection disabled, measurement bridge disabled. Expected behavior: recover baseline GR/LambdaCDM/SM surface.
- `scalar_free_spectator`: `alpha_Psi` symbolic nonzero, `lambda_T=0`, `alpha_B=0`. Expected behavior: test scalar stress-energy readiness without matter source coupling or `B_Psi`.
- `scalar_trace_coupled_future`: `alpha_Psi` symbolic nonzero, `lambda_T` symbolic nonzero only after source definition, `alpha_B=0`. Status: blocked.
- `B_branch_guard`: any `alpha_B != 0` case remains blocked or expected-fail until `B_Psi` is defined.

## Conservation And Constraints

The conservation/exchange model is not selected in v5. Future choices are separate scalar conservation after EOM, or explicit exchange current between scalar and matter.

MICROSCOPE and Eot-Wash are retained as external constraint anchors, but model-to-bound mapping remains blocked.

## Classification

Evidence: this dictionary and fixture set encodes duties already required by v462A gates.

Hypothesis: scalar-only fixtures can isolate derivation readiness from undefined `B_Psi` and Mandala/meta terms.

Blocker: fixtures are defined but not executed; external sources are anchored but model mapping is blocked.

Advisory: do not use fixture existence as gate closure.
