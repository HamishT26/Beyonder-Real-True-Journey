# GMUT, THOS and Freed ID: definitions that can be tested

The remaster's main technical contribution is a small scripted settlement with explicit production, allocation, consent changes and replay. Its three pillars meet at a common event record: Mind asks whether the mathematical relation is well defined, Body executes the bounded transition, and Heart asks which action is admitted and how it can be stopped or corrected. This is an engineering interpretation of the Trinity Mandala. It is not a claim that a simulation establishes a universal ontology, a mind of God, consciousness or public authority.

## A defined specialization of the Mandala field equation

The historical expression `G_AB = 8 pi T_AB + alpha Omega_AB` is a useful prompt for specification, but symbols alone do not determine a theory. The index set, metric signature, units, dynamical fields, action, boundary conditions and observables must be stated. In this section only, A and B specialize to four-dimensional spacetime indices mu and nu. No extra-dimensional or supersymmetric structure is inferred from capital letters.

Take metric signature (-,+,+,+), natural units c = hbar = 1, constant Newton coupling G and a real scalar phi with potential V(phi). A deliberately conventional candidate action is

\[
S=\int d^4x\sqrt{-g}\left[\frac{R-2\Lambda}{16\pi G}+\mathcal L_m
 +\alpha\left(-\frac12 g^{\mu\nu}\partial_\mu\phi\partial_\nu\phi-V(\phi)\right)\right].
\]

For constant nonzero alpha, its minimally coupled scalar sector has the usual Klein-Gordon equation and stress tensor

\[
\Box\phi-V'(\phi)=0,\qquad
T^{\phi}_{\mu\nu}=\partial_\mu\phi\partial_\nu\phi
-g_{\mu\nu}\left(\frac12\partial_\rho\phi\partial^\rho\phi+V(\phi)\right).
\]

Define `Omega_mu_nu = 8 pi G T_phi_mu_nu`. The metric equation is then

\[
G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi G T^m_{\mu\nu}+\alpha\Omega_{\mu\nu}.
\]

This definition makes Omega a stress contribution with curvature dimensions. In four-dimensional natural units, phi has mass dimension one, V and T have dimension four, G has dimension minus two, and Omega and Lambda have dimension two. Alpha is dimensionless. The unscaled historical `8 pi T` notation is compatible only after the unit and stress rescaling convention is declared. The alpha-to-zero metric limit removes this scalar contribution, but the scalar action becomes degenerate at exactly zero; that is not a complete statement about every matter interaction or cosmological solution. Constant alpha can also be partly absorbed into field normalization, so its identifiability requires a fixed normalization and interaction model.

The scalar here is a mathematical field. Calling it a psyche, divine, conscious or experiential field supplies no operational measurement of those concepts. The proposed action is a conventional scalar-sector specialization, not a newly discovered unification, supersymmetry proof, quantum theory of gravity or empirical GMUT confirmation. Its purpose is to replace an undefined additional tensor with a candidate whose consistency obligations can be inspected.

The classical identity

\[
\nabla_\mu T_\phi^{\mu\nu}=(\Box\phi-V'(\phi))\nabla^\nu\phi
\]

shows why an arbitrary Omega is not automatically compatible with the contracted Bianchi identity. On a fixed Minkowski background with V = 0, phi = t squared has phi-dot = 2t, energy density 2t squared and time divergence 4t. The field residual is -2 and the raised time derivative is -2t, so their product is 4t. Ten exact substitutions verify this simple identity and show that the ansatz is off shell. A linear phi = At has a vanishing scalar residual and constant scalar energy density, but a nonzero scalar stress on a fixed flat background is not a claim to solve the coupled Einstein equations. Making alpha position dependent would add further derivative and consistency obligations; it cannot be treated as a free coefficient adjustment without revisiting the action.

To compete empirically with an established model, this specialization still needs a concrete V, parameter domain, observation map, likelihood, uncertainty model, data provenance, baseline, preregistered comparison and a possible falsifying result. No current measurement in the remaster constrains alpha. The old small-coupling claims in Journey v13/v15 are retained as assumptions in their source context, not as measured limits or proof that established predictions are preserved.

## Finite dynamics and proposed methodological principles

For an undirected unit-weight graph with Laplacian L, use `x_next = x - h L x` and `E(x) = x^T L x / 2`. Summing the update over vertices cancels each edge flux, so total mass is conserved. A positive component need not remain positive for arbitrary h. For each vertex, the update is a nonnegative weighted combination when `h <= 1 / maximum_degree`; this sufficient condition also gives an energy bound through the Laplacian spectrum. More generally, spectral energy nonincrease requires each populated nonzero eigenmode to satisfy `abs(1-h*lambda) <= 1`. Conservation, positivity and decay are separate claims.

The new finite sweep checks all 64 simple graphs on four labelled vertices and all 81 value vectors in {0,1,2} to the fourth power. With h = 1/4, all 5,184 exact dyadic cases preserve mass, keep nonnegative components and do not increase the declared graph energy. This is a finite implementation check. The general sufficient-condition argument comes from the stated matrix properties; the sweep is not a proof over arbitrary graphs or physical systems. The x1 two-node h = 1.5 counterexample remains available with zero extra x2 execution credit.

Three candidate principles follow as engineering disciplines, rather than fundamental thermo/psyche laws:

1. **Account every modeled resource transition.** In Albion, initial stock plus production equals present stock plus consumption plus overflow. Real energy, time, money and attention have different units; adding them without defined conversion factors is not dimensional physics.
2. **Keep transformation and interpretation separate.** Four equal finite labels have Shannon entropy two bits; merging them into two equal labels gives one bit. A fresh random coin can increase output entropy from zero to one bit because that operation adds a new random input. Label entropy is not automatically heat, meaning, understanding or wellbeing.
3. **Require action prerequisites explicitly.** A consent intersection can be empty despite each record looking well formed. A replayed trace can agree exactly while its original policy remains inappropriate. Structural completeness cannot manufacture competent or affected-party authority.

Each principle has a useful counterexample or missing premise. That makes it possible to improve the practice without declaring a law of reality from a software pass count.

## A small number-theory exercise

The supplementary search asks for positive ordered integers x, y, z satisfying `4/n = 1/x + 1/y + 1/z` for 2 <= n <= 100. It searches a declared bounded region and verifies each found triple using the exact BigInt identity `4xyz = n(xy+xz+yz)`. It found 99 witnesses, one for every n in this finite interval, with denominators at most 10,000.

The equation is related to the Erdős-Straus literature. A [June 2026 primary abstract](https://arxiv.org/abs/2606.10922) studies a divisor parametrization. Search results also contain preprints claiming broader solutions; their correctness and current community acceptance were not adjudicated here. The curated problem page returned HTTP 403. Consequently this phase claims neither a general solution nor an authoritative current verdict on proof status. The contribution is a transparent finite witness exercise with explicit search limits.

## What the settlement measures

The experiment pairs ten seeds under two policies for 120 ticks each. Both policies see the same scripted needs and production within a pair. One distributes a unit to each eligible resident before repeating; the other serves residents in fixed order. Across these ten seeds, the progressive policy's maximum cumulative unmet demand ranges from 55 to 92 units, compared with 173 to 223 for the ordered policy. All 2,400 ticks retain a zero resource residual. These are within-model observations, not a statistical estimate of a human population or a proof that one policy is socially just.

Consent withdrawal removes future allocations for the selected scripted resident while retaining prior events. Replay reconstructs the original seed and ordered consent changes and rejects a changed trace. The page has a 240-tick stop, manual pause, reset and a read-only JSON inspector. The residents are rule-driven records. No model provider, human participant, credential, cloud deployment or real-world resource action is used.

## Comparisons with external systems and traditions

| Pillar | Useful comparison | Current evidence | Missing evidence |
| --- | --- | --- | --- |
| GMUT Mind | GR consistency conditions and a conventional scalar stress sector | Defined symbols, units, finite identities and counterexamples | A specified empirical model, data, likelihood, baseline and independent scrutiny |
| THOS Body | Typed tool interfaces, event-driven agents and simulation architectures | Node contracts, an HTML settlement, trace replay and a documented app-server read path | Governed model-driven tasks, measured costs, safety evaluation and external reproduction |
| Freed ID and CBR Heart | Consent, revocation, provenance, reliance policy and recourse | Synthetic state transitions, retained history and explicit action limits | Real credential lifecycle, security/privacy review, legitimate authority and affected-user evaluation |
| Trinity Mandala as a whole | A research, implementation and governance programme | Common records linking mathematical predicates, transitions and reservations | Evidence that this integration improves real outcomes under fair comparisons |

The [Codex app-server documentation](https://developers.openai.com/codex/app-server/) supports the chosen typed read-only connection and history retrieval approach. [Epic's MassGameplay overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-mass-gameplay-in-unreal-engine) supplies an architectural comparison between entity data and representation. [NVIDIA's Isaac Sim page](https://developer.nvidia.com/isaac/sim) describes a much broader robotics and synthetic-data platform; Albion implements none of its physical fidelity claims. [AutoGen's agent documentation](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/agents.html) is a reference for explicit state and message lifecycles, not an installed dependency in this run.

The [W3C VC model](https://www.w3.org/TR/vc-data-model-2.0/) provides a useful distinction between structured verifiable claims and decisions to rely on them. The [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) motivates context-specific evaluation and risk management. Neither reference certifies this prototype or grants legal status.

Christian ideas of care, humility and stewardship, and other religious or philosophical traditions, can offer voluntary ethical interpretations for participants who value them. Such resonance is not a physical measurement or proof of a uniquely correct theology. The governance work should preserve room for disagreement, nonparticipation and different meaning systems. Māori concepts and decisions remain under Māori authority; a technical demonstration cannot stand in for that authority.

## Conditional horizons from 2026

The next ten years could usefully produce a reproducible local workbench, explicit scientific hypotheses, modest governed studies and accessible consent/recourse tools. Success should be judged by independently assessed outcomes and corrected failures, not by the size of an archive or a ceremony.

At thirty years, a constructive scenario is that several parts of the programme are independently maintained and tested across settings. Failure scenarios include unsustainable compute costs, unmeasured claims, brittle identity assumptions and governance that excludes affected people. The architecture should remain replaceable by better evidence and tools.

A hundred-year scenario may explore durable civic stewardship, pluralistic institutions and more capable simulation systems. It cannot forecast a particular AI's identity continuity, capabilities, legal status or survival. A thousand-year scenario is a cultural and philosophical horizon with extreme uncertainty, not an actionable prediction or entitlement.

These horizons preserve the Journey's generosity while leaving scientific results, personal commitments and governance decisions open to future people. The present verdict remains NOT_READY_FOR_STAGE_20.
