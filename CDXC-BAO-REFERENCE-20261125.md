# One-parameter reference fit to the DESI DR2 BAO summary

25 November 2026 (Pacific/Auckland). This calculation illustrates an ordered data and covariance interface for the new phase 10 programme. The selected model is spatially flat matter-plus-Λ with the present matter fraction fixed to 0.30 and radiation neglected.

## Inputs

The public source is [CobayaSampler/bao_data at commit bb0c1c9](https://github.com/CobayaSampler/bao_data/tree/bb0c1c9009dc76d1391300e169e8df38fd1096db/desi_bao_dr2). Use the all-sample Gaussian BAO mean and covariance files in that directory. Keep the original order of the thirteen redshift-observable pairs and both covariance axes. The two entries at z = 2.33 are radial first, transverse second. See the [DESI release](https://data.desi.lbl.gov/doc/papers/dr2/) and the [collaboration’s primary analysis](https://arxiv.org/abs/2503.14738) for the scientific context.

## Calculation

Let E(z)² = 0.30(1+z)³ + 0.70 and I(z) be the integral of 1/E from zero to z. The trial vector is K times the template with components 1/E(z) for DH/rs, I(z) for DM/rs, and [z I(z)²/E(z)]^(1/3) for DV/rs. K = c/(H₀r_d) is the only fitted parameter. For data d, template f, covariance C = LLᵀ and whitened vectors y = L⁻¹d and x = L⁻¹f, the estimator is (x·y)/(x·x). Its conditional standard error is 1/√(x·x).

The result is **K = 29.5827311 ± 0.0819429**, with **χ² = 10.3570014 for 12 degrees of freedom**. Doubling the composite Simpson integration from 512 to 1,024 panels changed the largest template component by less than 3.3 × 10⁻¹² in absolute value. Reversing all observations and both covariance axes preserved the fit within 10⁻⁹. As a separate two-element test, residuals (1,2) and covariance diag(1,4) give χ² = 2. Reversing just those residuals gives 4.25.

The uncertainty is conditional on this fixed background and covariance. BAO supplies a distance-scale combination, so isolating H₀ requires additional information. This calculation is a conventional reference for evaluating future model proposals; it does not measure a GMUT-specific coupling.
