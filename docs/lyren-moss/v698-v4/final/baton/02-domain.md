# Finite directed-hypergraph domain

The phase defines thirty wholly synthetic profiles. A directed hyperedge has nonempty tail and head sets. Reachability uses an explicit all-tail firing convention; weak components forget direction within the finite incidence clique; a cut candidate is a vertex whose removal increases weak-component count. These are declared local semantics, not universal definitions. The operations are:

- hg_profile (x1; completed): Return exact finite vertex and directed-hyperedge counts plus declared roots.
- hg_vertices (x1; completed): Return the canonical lexical vertex list without inventing nodes.
- hg_hyperedges (x1; completed): Return canonical directed hyperedges with sorted tails and heads.
- hg_incidence (x1; completed): Return exact incoming and outgoing hyperedge identifiers for each vertex.
- hg_unique (x1; completed): Confirm vertex, edge-identifier and canonical-edge uniqueness.
- hg_sources (x1; completed): Return vertices with no incoming directed hyperedge.
- hg_sinks (x1; completed): Return vertices with no outgoing directed hyperedge.
- hg_reachable (x1; completed): Apply declared all-tail firing reachability from the synthetic roots.
- hg_layers (x1; completed): Return the earliest all-tail firing layer for every reachable vertex.
- hg_transpose (x1; completed): Swap every finite synthetic hyperedge tail and head.
- hg_union (x2; completed): Return the canonical set union of two edge-signature collections.
- hg_intersection (x2; completed): Return the canonical edge-signature intersection.
- hg_difference (x2; completed): Return edge signatures present only in the first graph.
- hg_boundary (x2; completed): Return tail-only, head-only and mixed-incidence synthetic vertices.
- hg_projection (x2; completed): Project each directed hyperedge to its finite tail-to-head arc pairs.
- hg_components (x2; completed): Return weak components of the finite incidence projection.
- hg_cut_candidates (x2; completed): Return vertices whose removal increases weak-component count.
- hg_scene (x2; represented): Represent one bounded accessible two-dimensional layout without physical meaning.
- hg_evidence_gap (x2; open_gap): Retain missing empirical and independent evidence as an open gap.
- hg_authority_gate (x2; exact_gate): Retain legal, cultural, affected-party and Maori authority as exact gates.

No graph encodes a real person, place, device, system, measurement, identity or authority act. A possible partition is not a probability, and reachability is not physical causation.
