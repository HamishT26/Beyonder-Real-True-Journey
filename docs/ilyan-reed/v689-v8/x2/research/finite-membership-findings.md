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
