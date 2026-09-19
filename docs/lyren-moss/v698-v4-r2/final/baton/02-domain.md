# Finite directed source-claim provenance graph domain

The phase defines thirty wholly synthetic profiles. A directed hyperedge has nonempty tail and head sets. Reachability uses an explicit all-tail firing convention; weak components forget direction within the finite incidence clique; a cut candidate is a vertex whose removal increases weak-component count. These are declared local semantics, not universal definitions. The operations are:

- sl_profile (x1; completed): Return exact source-node and claim-link counts plus declared provenance roots.
- sl_vertices (x1; completed): Return the canonical lexical source-alias list without inventing documents.
- sl_hyperedges (x1; completed): Return canonical directed source-to-claim links with sorted tails and heads.
- sl_incidence (x1; completed): Return exact incoming and outgoing claim-link identifiers for each source alias.
- sl_unique (x1; completed): Confirm source-alias, link-identifier and canonical-link uniqueness.
- sl_sources (x1; completed): Return source aliases with no incoming claim link.
- sl_sinks (x1; completed): Return source aliases with no outgoing claim link.
- sl_reachable (x1; completed): Apply declared all-source support reachability from the provenance roots.
- sl_layers (x1; completed): Return the earliest support layer for every reachable source alias.
- sl_transpose (x1; completed): Reverse every finite synthetic source-claim link for comparison only.
- sl_union (x2; completed): Return the canonical union of two claim-link signature collections.
- sl_intersection (x2; completed): Return the canonical claim-link signature intersection.
- sl_difference (x2; completed): Return claim-link signatures present only in the first source graph.
- sl_boundary (x2; completed): Return source-only, claim-only and mixed-incidence aliases.
- sl_projection (x2; completed): Project each provenance link to finite source-to-claim arc pairs.
- sl_components (x2; completed): Return weak components of the finite source-claim incidence projection.
- sl_cut_candidates (x2; completed): Return source aliases whose omission changes weak-component count.
- sl_scene (x2; represented): Represent one bounded accessible source-lattice layout without evidentiary promotion.
- sl_evidence_gap (x2; open_gap): Retain missing empirical, affected-party and independent evidence as an open gap.
- sl_authority_gate (x2; exact_gate): Retain legal, cultural, affected-party and Maori record authority as exact gates.

No graph encodes a real person, place, device, system, measurement, identity or authority act. A possible partition is not a probability, and reachability is not physical causation.
