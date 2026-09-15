# Ranked defaults, exceptions and the evidence ceiling

This phase implements a small ordinal model of defeasible conclusions. Its inputs are five synthetic records with two through four propositional atoms, all associated worlds, an explicit rank for each world, a finite default set and three formulas. A world is a truth assignment. A smaller rank means preferred under this supplied model; it is neither a measured probability nor a statement of legitimate authority.

The implementation and the planning reference use different representations. The reference enumerates lists of satisfying worlds. The runtime computes finite bit masks. Their full typed outputs agree for the one hundred frozen operation-case contracts. The agreement is same-owner validation. It does not establish independent reproduction, a useful real policy, calibrated uncertainty, or a model of human reasoning.

## Definitions and source scope

For a formula A, let [A] be its satisfying worlds and let mu(A) be the members with least supplied rank. The declared ranked conditional A =>d B holds when every world in mu(A) satisfies B. Empty antecedents are explicitly reported as vacuous in this operation. Classical entailment instead checks every world in [A], so a classical countermodel can coexist with a successful default conclusion.

For defaults, the System Z procedure repeatedly selects rules that some world verifies while violating none of the remaining rules. Those rules form the next layer. A nonempty residual with no selectable rule is reported as inconsistent. For a consistent base, a world has rank zero when it violates no rule, otherwise one plus the highest violated rule layer. The strict Z query reserves an impossible antecedent with a null conclusion rather than silently choosing a vacuity convention. These are bounded implementations of established [System Z definitions](https://ftp.cs.ucla.edu/pub/stat_ser/R131.pdf).

Rational monotony says that a current default conclusion survives adding C when not-C was not already a default conclusion. Ranked-model theory provides the formal comparator. The present implementation checks the exact predicate and records whether its premises apply, using the [Lehmann–Magidor ranked-model account](https://arxiv.org/abs/cs/0202022). The 1992 journal date and the 2002 arXiv upload are separate dates.

## What the fixtures establish

| Fixture | Finite observation | Consequence for this implementation |
| --- | --- | --- |
| ordinary_default | A default conclusion holds although a higher-ranked classical countermodel exists | Keep classical and default entailment as different operations |
| specific_exception | Adding the exceptional class retracts the parent default | Do not impose ordinary monotonicity on a defeasible consequence operation |
| inheritance_block | Two equally preferred subclass worlds disagree on the additional parent property | Preserve the failed inheritance claim and expose the counterexample world |
| conflicting_defaults | Preferred worlds support opposing answers at the same rank | Retain the tie rather than choosing an arbitrary winner |
| inconsistent_defaults | Worlds with a false antecedent satisfy the material implications, but no rule is tolerated | Material satisfiability alone does not justify inventing a Z partition |

Two overbroad claims are retained as failed subjects in `research-witnesses.json`. Their refutation predicates pass, while the original claims retain zero success credit. The first says every materially satisfiable base has a complete Z partition. The second says an exceptional subclass automatically inherits all other parent defaults. The counterexamples are finite and explicit; no new fundamental law is claimed.

The edge suite contains twenty-five x1 and twenty-five x2 tests. One x2 property examines all 81 assignments of ranks 0, 1 and 2 to four worlds and all 4,096 triples of truth sets for each assignment. All 331,776 tested rational-monotony implications hold. This is the internal denominator of one finite property test, not 331,776 independent experiments. A short reason explains the pattern: if a least-ranked A-world satisfies C, the least-ranked A-and-C worlds have the same least rank and remain among the A-minima. The result's application still depends on the stated ranked-model assumptions.

The declared ranks and the ranks computed from defaults are separate records. Inconsistent defaults can coexist with a separately declared flat ordinal model. That separation is deliberate: the runtime may inspect the flat model but may not label it a valid System Z solution to the inconsistent rules. Strictly increasing transformations of supplied ranks preserve their order; they do not estimate a new likelihood or confidence level.

## Mind, Body and Heart

GMUT Mind benefits from the discipline of stating a domain, symbols, assumptions and falsifiers before asserting a conclusion. The historical Mandala field expression does not become a physical law through a default inference engine. No action, spacetime model, dimensioned observable, physical data, calibrated likelihood, stability proof or empirical parameter estimate was produced here. Ordinal world preference cannot be substituted for a stress tensor or an Omega term.

THOS Body receives closed typed records, finite caps, reproducible responses, retained conflicts and portable text-source runners. The runtime uses at most sixteen worlds, twelve defaults, formula depth twelve, and sixty-four nodes per formula. These are engineering bounds for the declared lab. Real operational reliability, governed workloads, operators, safety monitoring, suitable statistics and independent review remain absent.

Freed ID and CBR Heart are the primary study focus. A default can organize an explicitly hypothetical policy discussion, but it cannot determine a person's identity, consent, credential status, entitlement or appeal. The choice of ranks and defaults belongs to a policy and evidence process. Demonstrating that a program follows those choices does not legitimize them. Competent professional, legal, cultural, affected-party and Maori authority must remain separate from the synthetic record.

The four learning practices are formal methods analysis, knowledge representation engineering, decision-log audit and technical documentation editing. They are study lenses, not employment or qualifications. Belief-revision test design and counterexample-guided model review are the two optional recommendations for Lyren.

## What remains open

The eighty completed core outcomes concern exact finite operations. Ten represented outcomes preserve model interpretation and unmeasured adequacy. Five open gaps retain missing empirical comparison prerequisites. Five exact gates retain consequential deployment and rights authority. Fifty exact packet descriptions and thirty blocked descriptions remain review inventories; their protected actions were not executed.

The practical next questions are narrower than a claim of general reasoning competence: how does a declared rule amendment change the minimal countermodels; which default blocks an expected inheritance; which conclusions are stable across an explicitly permitted rank transformation; and what additional evidence would make a proposed policy reviewable? The next sibling can choose those questions or another useful domain under its current authority.

Only source text, JSON, Markdown, TeX source and HTML are newly authored. No image, screenshot, PDF, DOCX, rendered TeX, package installation, paid external action, Unity project, real participant, real credential or deployment occurred. The source literature and ten reviewed overview artifacts provide context and comparison boundaries; their results receive zero new owner execution or novelty credit.

The terminal evidence verdict remains **NOT_READY_FOR_STAGE_20**.
