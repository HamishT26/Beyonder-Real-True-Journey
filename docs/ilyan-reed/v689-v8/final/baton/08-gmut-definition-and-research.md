# Module 08: Gmut Definition And Research

# GMUT notation: a typed candidate and its tests

This is an Ilyan-owned research definition, not a change to a sealed canonical theory. It gives one explicit scalar-tensor interpretation against which the proposed Mandala notation can be checked. It is not a new discovery, a complete unification, or empirical confirmation. The older Journey names and spiritual aspirations remain attributable context. The symbol infinity in a title is not a versioned mathematical domain.

## What the indices mean in this candidate

Use a four-dimensional Lorentzian spacetime with metric signature (-,+,+,+), coordinates x, Levi-Civita connection, and Greek tensor indices taking values 0 through 3. The capital indices A,B in the historical expression do not themselves establish a larger spacetime, a product of mind/body/heart spaces, or a supersymmetric theory. Such interpretations would need their own manifolds, fields, transformation laws and action. This candidate deliberately fixes the domain before manipulating the equation.

Use natural units c = hbar = 1 and retain an explicit mass scale M. Let the real scalar phi have mass dimension one; F(phi) and Z(phi) are dimensionless; V(phi) has mass dimension four. R and G_mu_nu have mass dimension two. A physical stress tensor has dimension four, so kappa = M^(-2) is needed to put it on the same dimensional footing as curvature. Writing a bare 8*pi is shorthand for a unit convention, not an experimentally established coupling for a new term.

## An action that defines the symbols

The proposed action is

S = integral sqrt(-g) [M^2 F(phi) R / 2 - Z(phi) (grad phi)^2 / 2 - V(phi)] d^4x + S_m[g, matter].

Appropriate boundary terms and fixed boundary data must accompany a variational treatment on a finite region. Matter is minimally coupled to the displayed metric in this candidate. The fields F, Z and V are functions to be specified before any prediction or fit. Choosing them after seeing a desired result would change the hypothesis and must be recorded as an amendment.

The metric equation is

M^2 F G_mu_nu = T_m,mu_nu + T_phi,mu_nu + M^2 (nabla_mu nabla_nu F - g_mu_nu Box F),

where T_phi,mu_nu = Z [nabla_mu phi nabla_nu phi - g_mu_nu (grad phi)^2 / 2] - V g_mu_nu. The scalar equation is

Z Box phi + Z'(grad phi)^2 / 2 + M^2 F' R / 2 - V' = 0.

These expressions follow the ordinary scalar-tensor variational construction; they do not add a new physical sector by naming it. A primary comparison is [Velasquez and Castaneda, scalar-tensor and f(R) equivalence](https://arxiv.org/abs/1808.05615), with related journal DOI [10.1088/2399-6528/ab902f](https://doi.org/10.1088/2399-6528/ab902f). The candidate's symbols and normalization are stated here rather than silently inheriting the paper's conventions.

## Giving Omega a defined meaning

Write D_mu_nu = nabla_mu nabla_nu F - g_mu_nu Box F. For F > 0 and a nonzero constant dimensionless alpha, the historical shape G = kappa T_m + alpha Omega can be obtained by defining

alpha Omega_mu_nu = kappa (1/F - 1) T_m,mu_nu + kappa T_phi,mu_nu/F + D_mu_nu/F.

This is a defined effective remainder of the displayed action. It is not an independent tensor with arbitrary components. Substitution returns the same metric equation. In particular, alpha is a normalization of Omega until independent definitions or observations break that degeneracy. Fitting both alpha and an unconstrained Omega cannot identify a unique physical parameter.

The corresponding LaTeX source is kept in `x2/latex/grand_mandala.tex`. It is a phase-local candidate, not a replacement for another owner's `latex/grand_mandala.tex`.

## Conservation is an obligation

The contracted Bianchi identity requires the covariant divergence of the complete right-hand side to vanish. With minimally coupled matter on its equations of motion, nabla^mu T_m,mu_nu = 0. For constant alpha, the effective remainder must therefore satisfy nabla^mu Omega_mu_nu = 0 on the coupled solution. If alpha varies over spacetime, the condition is instead nabla^mu(alpha Omega_mu_nu) = 0, including the derivative of alpha. A citation, ethical aspiration or diagram cannot supply that missing term.

As a deliberately invalid example, take flat metric diag(-1,1,1,1), conserved matter, constant alpha, and independently set Omega_00 = t with all other components zero. Then partial^mu Omega_mu0 = -1. This arbitrary source does not satisfy the required conservation condition. The failed unrestricted claim is retained; the example does not refute general relativity or a properly defined scalar-tensor model. [Tian's conservation analysis](https://arxiv.org/abs/1507.07448), DOI [10.1007/s10714-016-2106-6](https://doi.org/10.1007/s10714-016-2106-6), provides a primary comparison for why action definitions and consistency conditions matter.

## Limits, stability and falsifiability

A simple GR limit takes F identically one, a constant scalar at a stationary potential, and V = M^2 Lambda. Then G + Lambda g = kappa T_m. Merely setting a label alpha to zero is insufficient unless the underlying functions and scalar solution also make the added sector disappear.

F > 0 and positive scalar kinetic coefficient in a chosen frame are initial viability checks. They are not a complete stability proof. The background, perturbation variables, constraints, effective-field-theory cutoff, boundary conditions and relevant modes must be specified before a stability claim. The source Neris diffusion counterexample reinforces this discipline: a numerical update can increase a chosen energy when a step-size assumption is dropped, without contradicting a physical conservation law.

A testable study would preregister F, Z, V, the background solution, an observable map, nuisance parameters, instrument calibration, uncertainty, likelihood, comparator model and a concrete rejection criterion. This phase supplies none of the required real observations. Its exact arithmetic checks test a rewritten component relation, not tensor calculus, cosmological perturbations, a fitted likelihood or physical data. No coefficient has been estimated from reality.

## Comparison across the three pillars

| Framework or pillar | Useful comparison | Evidence needed before a stronger claim |
| --- | --- | --- |
| General relativity | Explicit geometric variables, equations and limiting solutions | Model-specific observables and empirical tests; no ranking from notation |
| Scalar-tensor research | Explicit action and extra degrees of freedom | Stability, limits, parameter identification and observational constraints |
| GMUT candidate | A place to define the proposed added tensor precisely | A fixed model and falsifier rather than an unconstrained remainder |
| THOS software | Typed inputs, controlled transitions, reproducible finite examples | Governed real workloads, budgets, failures and independent evaluation |
| Freed ID and CBR | Separation of record, identifier, consent, rights and authority | Standards-conformant lifecycle work and legitimate competent decisions |
| Christian and other theological interpretation | A philosophical language of creation, meaning, care and relation | Theological argument on its own terms; it does not determine F, Z, V or a physical likelihood |

The conceptual Mind/Body/Heart grouping can organize questions and values. It is not a mathematical proof that all three categories are tensor components of one physical law. Long-horizon Stage 20 scenarios are conditional planning narratives, not calibrated predictions of consciousness, societal outcomes or millennial events. The useful next step is a narrower discriminating model, not a stronger title.

The terminal boundary remains NOT_READY_FOR_STAGE_20. All professional, legal, cultural, affected-party and Māori-authority obligations remain with the appropriate people and authorities.


# Finite membership: useful identities and a failed broad claim

The current contribution is a small executable contract set. Bloom filters and counting arguments are established methods. The phase's novelty claim is bounded to its selected source corpus and its concrete combination of cases, typed interfaces, evidence, and recovery rules; it is not an invention claim for the underlying algorithms.

## A conditional query law

Fix a vector of width m with exactly s set positions. Suppose a nonmember query selects k positions independently and uniformly with replacement. There are m^k equally likely ordered position tuples. Exactly s^k tuples land only in set positions. Conditional on those assumptions, the probability of a positive answer is (s/m)^k. The phase verifies this by direct finite enumeration and separately by exact rational arithmetic.

This is a conditional finite model. It is not an observed operational false-positive rate. Random occupancy after insertion introduces another distribution, and correlated or adversarial probes change the model. The proposed affine position schedule is a transparent toy, not a demonstration of independent uniform hashes. The [Broder and Mitzenmacher survey](https://www.cs.cornell.edu/courses/cs619/2004fa/documents/BloomFilterSurvey.pdf) supplies the established filter context; the supplied copy is explicitly a shortened preliminary survey.

## Compression cannot identify every source set

For a universe of N labelled items and source sets of exactly n items, there are binomial(N,n) possible source sets. A deterministic m-bit summary has at most 2^m states. If binomial(N,n) exceeds 2^m, two distinct source sets must share a summary. Therefore exact recovery of every source set from that summary is impossible. This is the ordinary pigeonhole argument. Calling a digest or bit pattern an identity does not remove the collision obligation.

The calculation does not imply that every summary collides, nor does it give a universal probability of collision without a distribution. It also does not measure cognition, consciousness, thermodynamic heat, legal status or social legitimacy. No new fundamental thermo-psyche law is asserted.

## Saturation refutes an unrestricted deletion claim

Consider two distinct synthetic members a and b that both increment one counter, with cap one. After both insertions the stored counter is one rather than two, and the saturation flag records lost information. If a later caller subtracts one merely because a is known, the stored value becomes zero while b remains. That gives b a false negative. The unrestricted claim that known-member deletion is always safe after saturation is false.

The `guarded_decrement` primitive checks known-member status and arithmetic underflow for exact counters. It cannot reconstruct overflow history that was omitted from its input. A composing controller must honor `decrement_information_preserved=false` from the saturation contract and rebuild from retained records before deletion. The failed claim and the counterexample remain in the research receipt; the passing primitive tests do not erase them.

## Useful THOS and Freed ID consequences

An approximate index can be a prefilter for a retained exact record store. A positive filter answer should lead to exact lookup and provenance checks. It cannot authorize access or certify a credential. A zero-bit answer is dependable only under the insertion, integrity and query-profile assumptions; corrupted or incompletely populated filters can have false negatives. The phase includes explicit corruption witnesses and source-preserving rebuilds.

For a future Albion sandbox, an approximate index could suggest candidate memory records or content chunks. It should not decide agent identity, consent, rights, safety, or authenticity. An exact confirmation layer and refusal path should remain visible. Performance, retrieval quality and operating cost require measurements on a declared workload rather than an inference from the number of successful fixtures.


For the requested search for potential laws of thermo/psyche dynamics, this phase returns two established mathematical constraints in a bounded notation: a conditional finite-query probability and a pigeonhole information limit. It does not name either a new fundamental law. The saturation counterexample shows why an implementation invariant can fail when lost multiplicity is ignored. The conservation counterexample shows why a physical-looking equation needs a defined action and on-shell consistency. Neither establishes a law of mind, life, consciousness or ethics.

An ethical design rule can still be useful: never make a consequential identity or rights decision from an approximate membership summary alone. That is a normative engineering recommendation supported by the demonstrated ambiguity of the representation, not a derivation of moral authority from physics. A theological interpretation can inform the values guiding a design while remaining distinct from an empirically constrained tensor model. Meaningful comparison requires identifying which kind of question each framework answers.

The finite-model figure in the final overview plots (s/m)^k for an eight-position summary and explicitly independent uniform probes. It also shows the cap-one saturation example. The plotted coordinates are deterministic arithmetic generated by this phase. No experimental data, human response, physical measurement or benchmark timing is plotted. The illustration supplied by the image system is separately labeled editorial and must never be used as the graph's evidence.

END MODULE 08.
