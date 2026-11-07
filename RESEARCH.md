# Complexity and holographic claims in the GHC programme

Status: source-grounded research additions for phase 12. These distinctions guide small experiments and software design; they do not validate GMUT.

## P versus NP and finite search

The Clay Mathematics Institute still lists P versus NP as unsolved. Its distinction is between efficiently checking a proposed solution and efficiently finding a solution for every instance in a problem class. A successful finite enumeration is compatible with either eventual answer to that general question. [Clay, P vs NP](https://www.claymath.org/millennium/p-vs-np/), accessed 31 October 2026.

Our Unique Games demonstration exhausts no more than 4,096 assignments. For a two-colour triangle with a swap constraint on every edge, it finds an optimum of two satisfied edges out of three. The first lexicographic optimum is [0,0,1]. This is a reproducible finite witness: the third parity constraint prevents satisfying all three edges. It is useful for testing constraint orientation, witness ordering and score accounting. It says nothing about the complexity of arbitrary large instances.

The engineering consequence is specific. A scheduler may use a finite solver within an explicit size limit, but must retain a separate strategy for larger inputs. A fast result on a small roster is not evidence that resource allocation, workflow optimization or general reasoning has become computationally easy. Keeping the instance size and search count beside the result prevents a useful demonstration from acquiring an unsupported universal interpretation.

## Unique Games and the current OpenAI manuscript claim

The current OpenAI mathematics catalogue reports a manuscript titled The Unique Games Theorem, dated 23 September 2026. Its formalization scope describes a polynomial-time reduction from binary 3SAT to a restricted family of nonempty unweighted simple bipartite unique games, with a fixed alphabet depending on fixed completeness and soundness parameters. That is a substantially different claim from running an exhaustive solver. [OpenAI, family 102 formalization scope](https://github.com/openai/math/blob/main/lean/docs/102.md).

The repository itself describes its outputs as raw research data at different verification stages. On the inspected revision it lists 721 manuscripts in 373 families, with approximately 42 percent of top-line results formalized. The history includes an October 29 comparator namespace repair. These are repository statements and version records; they are not our independent proof-build results or a finding of peer-reviewed acceptance. [Repository README](https://github.com/openai/math/blob/main/README.md), [revision history](https://github.com/openai/math/blob/main/history.md), accessed 31 October 2026.

For GHC, a prospective formalization review must identify the exact commit, toolchain, theorem statement, assumptions, imports and checker output. It must distinguish fixed parameters from input-dependent quantities. A reduction establishing approximation hardness also does not establish P versus NP merely because its title contains the word theorem. Our next useful activity is a selected statement audit or a bounded build with a stated resource budget, not an inference from catalogue counts. No Lean build was performed for this addition.

## Holographic duality

Maldacena's original paper, first submitted on 27 November 1997 and revised on 22 January 1998, describes particular conformal theories and an anti-de Sitter gravitational/string-theory correspondence. Its journal reference is Advances in Theoretical and Mathematical Physics 2, 231–252 (1998). The abstract expressly presents the broader duality as a conjecture. The source was read at abstract and bibliographic level here, not as a complete technical derivation. [Maldacena, The Large N Limit](https://arxiv.org/abs/hep-th/9711200).

A useful GMUT comparison would name both sides of a proposed correspondence, their state spaces, boundary conditions, limits and observable map. A correspondence between two mathematical descriptions cannot be inferred merely because both use information, entropy, matrices or networks. For an engineering memory system, compression and replication have directly measurable properties; invoking holography does not remove storage costs, synchronization requirements or loss.

The practical next question is therefore about an explicit map. If two finite representations are claimed equivalent, which observables are preserved and which information is discarded? A model can test that question with known inputs and exact reconstruction checks. Such a test remains about the chosen representations. It would not demonstrate a duality between an arbitrary AI architecture and physical spacetime.

## Holonomic brain theory

Pribram and Carlton's Holonomic brain theory in imaging and object perception is indexed as an Acta Psychologica article from December 1986, DOI10.1016/0001-6918(86)90062-4. The inspected PubMed record has no abstract, so this lookup establishes bibliographic provenance rather than a detailed evaluation of its argument. [PubMed record](https://pubmed.ncbi.nlm.nih.gov/3591432/).

The author's page for the 1991 book Brain and Perception describes computational models of perception, a holographic hypothesis, and both distributed and localized processes. This is an author's account of a theoretical programme, not independent evidence for consciousness or a universal physical field. [Pribram, Brain and Perception](https://www.karlpribram.com/brain-and-perception-holonomy-and-structure-in-figural-processing/).

The engineering analogy worth testing is distributed representation. A controlled comparison could encode identical synthetic records with an ordinary index and a transform-based representation, then measure retrieval accuracy, corruption tolerance, update cost and exact provenance retention. If both systems make the same predictions for all measured outputs, the experiment cannot choose between broader ontological interpretations. A claimed neural or physical mechanism requires its own observations and a discriminating alternative.

## Relation to the scalar GMUT comparison

The existing GHC comparison action specifies a conventional minimally coupled scalar in four dimensions, not a newly validated field equation. For constant positive alpha, the redefinition chi=sqrt(alpha)*phi absorbs alpha into the scalar normalization when no separate interaction or source fixes that normalization. Consequently, a numerical fit for alpha would be uninterpretable without additional physical definitions.

This limitation is constructive. Before a real-data fit, specify the observable, detector response, source normalization, calibration, nuisance parameters, covariance and baseline. A synthetic example may explore a declared convention, but its result cannot be reported as empirical evidence for GMUT. The new complexity and holographic additions leave this requirement intact.

## What changed

The programme now has a small exact constraint example and clearer source-status rules for four requested topics. The actionable work is finite solver validation, explicit map comparison, source-bound formal-statement review and preregistered representation benchmarks. The requested large physical and mathematical claims remain separate questions with stronger evidence requirements.
