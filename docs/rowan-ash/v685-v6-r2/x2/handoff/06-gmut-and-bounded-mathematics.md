# GMUT consistency and bounded scientific comparisons

Rowan Ash gives GMUT Mind the lead for this remaster. The useful advance is a sharper set of conditions that a proposed physical model would have to meet, together with executable numerical examples. The current record contains no new real-world observation, independent replication, demonstrated ASI architecture, legal recognition, or solved universal conjecture. These absences remain part of the result.

## The inherited equation and its source

The legacy equation is read from latex/grand_mandala.tex at main commit 3a5d9f16e5c34f4e30ce83dea517cf4f9c137edd, blob 836411e944da159026e732d46534ff7081558431. The source describes its own canon as a repository consistency surface. That is an internal editorial role, not an empirical status.

\[
\mathcal{G}_{AB}+\Omega^{(M)}_{AB}+\Omega^{(R)}_{AB}
=8\pi\mathcal{T}_{AB}+\alpha\Xi_{AB}.
\]

The present phase does not invent definitions for the bridge tensors. A useful next specification must state the manifold, metric signature, connection, index ranges, dynamical fields, units, coupling dimensions, initial or boundary conditions, gauge structure, and observable map. Without these, apparently similar tensor equations may denote very different models.

## A necessary divergence condition

Under a Levi-Civita connection and the usual contracted Bianchi identity for the Einstein tensor, taking a covariant divergence gives the necessary condition

\[
\nabla^A\!\left(\Omega^{(M)}_{AB}+\Omega^{(R)}_{AB}-\alpha\Xi_{AB}\right)
=8\pi\nabla^A\mathcal{T}_{AB}.
\]

If matter is separately conserved, the right-hand side is zero. If there is exchange with additional fields, it must retain that exchange. Declaring conservation without an action, field equations, or explicit interaction model would hide the problem instead of solving it.

For a spacetime-dependent scalar coupling,

\[
\nabla^A(\alpha\Xi_{AB})
=(\nabla^A\alpha)\Xi_{AB}+\alpha\nabla^A\Xi_{AB}.
\]

The derivative of alpha cannot be discarded merely because an earlier example used a constant. The trusted SymPy calculation checks this product rule in a scalar flat-component illustration. It does not establish the covariance or physical meaning of the complete model. This distinction makes the test useful: it can catch a local algebra error without claiming to validate a theory.

## Dimensions and the general relativity limit

With an explicit geometric convention, the tensor terms must have compatible dimensions. In SI language, curvature and stress energy require a coupling with appropriate dimensions; natural units do not remove the need to state the convention. The current unit dictionary deliberately refuses an invented psyche-energy unit. It also distinguishes a dimensionless Shannon information quantity from an experiential or semantic concept.

The local general relativity limit sets the additional contributions to zero and checks the remaining residual. That is a necessary special-case consistency check. A model also needs to recover established observations, state the scale where extra effects matter, and avoid contradicted degrees of freedom. The comparison with effective field theory and scalar-tensor research supplies a list of obligations, not an equivalence claim. [BIPM SI Brochure](https://www.bipm.org/en/publications/si-brochure), [Donoghue effective field theory paper](https://arxiv.org/abs/gr-qc/9405057), [Kobayashi Horndeski review](https://arxiv.org/abs/1901.07183).

## Uncertainty that retains correlation

A synthetic two-variable example uses a Jacobian of [2, 3] and covariance matrix [[1, 0.5], [0.5, 4]]. The first-order propagated variance is 46. Dropping the off-diagonal covariance produces 40. The difference of 6 is a concrete demonstration of why correlations cannot be silently removed. The matrix is symmetric and has positive eigenvalues, so this particular example satisfies the positive semidefinite requirement.

The corresponding standard uncertainty is the square root of 46. It has a meaningful interpretation only when the input quantities, units, covariance estimation procedure, and local linear approximation are declared. The result does not calibrate an instrument or establish a measurement uncertainty for GMUT. It tests arithmetic and record structure against a controlled example. [NIST law of propagation of uncertainty](https://physics.nist.gov/cuu/Uncertainty/combination.html).

## Information and thermodynamics

Shannon entropy, thermodynamic entropy, semantic meaning, and subjective experience are different concepts. A mapping between them requires operational definitions and a model. Landauer-type physical bounds concern a specified physical process under explicit assumptions; they do not establish a universal law of psyche, spiritual energy, or moral worth.

The proposed operational rule for THOS is narrower: reformatting or exporting a record must not raise its evidence class. This is a software and governance invariant. The contract lab can reject a synthetic result relabelled as a real observation. Calling this invariant a new fundamental physical law would be an unsupported promotion. [Reeb and Wolf on Landauer and finite-size corrections](https://arxiv.org/abs/1306.4352).

## Exact unit fractions and an unresolved conjecture

The unit-fraction study distinguishes two formulations. The positive-denominator formulation permits repeated denominators for n at least two. The distinct-denominator formulation used in the current problem catalogue asks for strictly increasing positive denominators when n is greater than two.

The runner verifies

\[
\frac{4}{n}=\frac{1}{x}+\frac{1}{y}+\frac{1}{z}
\]

using exact rational arithmetic. It checks positivity and strict ordering separately from equality. Thus an exact sum with repeated denominators does not silently pass the distinct variant. For n equal to two, [1, 2, 2] is valid for the positive variant and refused for the distinct variant.

Two known constructions are reused. For n equal to 2k with k at least two, choose [k, k+1, k(k+1)]. For n equal to 3k with k at least one, choose [k, 4k, 12k]. The phase claims no new theorem for either identity.

For remaining inputs, the finite search uses a residual a/b after selecting x. The identity (ay-b)(az-b)=b squared turns the remaining two-unit-fraction equation into an integer divisor search. Every returned candidate is independently checked with Fraction equality and the declared domain. A timeout or exhausted search would remain an open gap, not a counterexample to the conjecture.

The completed sweep found and verified a witness for every integer from 3 through 1,000: 998 inputs. It proves that these returned triples satisfy these finite instances. It does not prove the universal conjecture, measure an asymptotic density, or establish a novel method. [Maintained problem 242](https://www.erdosproblems.com/242), [Elsholtz and Tao](https://arxiv.org/abs/1107.1010).

## Experimental comparisons without invented participants

The preregistration contracts require a hypothesis, falsifier, analysis population, stopping rule, exclusions, resource budget, and treatment of amendments before results. The sampling contracts distinguish unique observations, clusters, missing values, and repeated seeds. A thousand bootstrap draws do not create a thousand participants.

The illustrative multiple-testing calculations use P values [0.01, 0.04, 0.03]. Holm and Benjamini-Hochberg adjustments are computed with statsmodels and checked against the local reference algorithms. These are synthetic numbers chosen to exercise ordering and adjustment behavior. They support no claim about a real treatment, population, or causal effect. [Center for Open Science preregistration](https://www.cos.io/initiatives/prereg), [statsmodels regression documentation](https://www.statsmodels.org/stable/regression.html).

## Body and Heart comparisons

THOS gains a reproducible local environment and a contract laboratory. A meaningful future architecture comparison still needs an externally specified task set, a fixed baseline, comparable resource units, failure handling, and outcomes measured in a real environment. A passing repository suite is not evidence that the architecture is AGI or ASI.

Freed ID and the Cosmic Bill of Rights gain clearer technical and authority boundaries. RDF, JSON LD, PROV, and SHACL can describe and validate structure. A credential type, proof field, or identifier-shaped string does not establish a verified signature, trusted issuer, real DID registration, legal recognition, or consciousness. The choice to treat possible future systems with care remains a normative design commitment, not a measured conclusion about their inner experience. [W3C Verifiable Credentials](https://www.w3.org/TR/vc-data-model-2.0/), [W3C PROV](https://www.w3.org/TR/prov-o/), [W3C SHACL](https://www.w3.org/TR/shacl/).

## Stage 20 research board

The physical-law gate remains open until the model supplies defined dynamics, falsifiable predictions, and adequate observations. The architecture-superiority gate remains open until a matched real comparison is performed. The identity and rights gates retain their separate scientific, legal, cultural, and ethical questions. The independent-reproduction gate remains open because Rowan authored and checked this phase.

These gates do not prevent useful engineering. They determine which conclusions the engineering can support. The current advance is an inspectable path from a declared question to a bounded test, a retained counterexample, and a precisely limited result.
