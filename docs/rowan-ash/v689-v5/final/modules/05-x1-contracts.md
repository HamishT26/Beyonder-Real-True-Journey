# Module 05 - Exact simplicial and graph contracts

The x1 tranche contains one hundred frozen main requests, one hundred separately frozen candidate probes and one hundred inherited source-record refinements. Every main request matched its complete expected envelope and left the input unchanged. The candidate predicates confirmed the expected refusal; their inadmissible subjects retain zero success credit. The cleanup rows reconstruct full source records from keyed projections and claim no host cleanup or inherited execution.

The operation notes below explain the profile and its independent oracle. Each case listing gives the actual explicit payload, observed value and admitted outcome. These listings are a readable index to the exact JSON receipts, not a replacement for their hashes. Closely related parameter cases remain related examples within one operation family; they are not described as independent inventions.

The separate invariant module supplies additional checks beyond the frozen case table. It tests orientation changes, missing assumptions, rank or kernel properties, malformed inputs and exact boundary behavior as appropriate to this tranche. The module passed eighteen tests at its own execution boundary. A later summary-reader correction in x1 did not rerun those tests.

## Simplex Faces

Generate every nonempty face in dimension then lexicographic order. The empty face belongs to an augmented convention that this profile does not implement. Face counts alone do not identify a topological space. Compare a four-vertex simplex against the independently known counts 4, 6, 4, 1.

The ten recorded cases use the following explicit inputs. The full expected and observed envelopes, input hashes, refusal subjects and scalar types are retained in the corresponding results and planning files. The entries below do not imply empirical measurement or a broader authority decision.

**RA6895-N001** - Explicit input: `{"simplex":[0,1,2]}`. Observed value: `[[0],[1],[2],[0,1],[0,2],[1,2],[0,1,2]]`. Outcome: `completed`. Independent expected-value basis: Independent bitmask enumeration of every nonempty subset. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N002** - Explicit input: `{"simplex":[1,2,3,4]}`. Observed value: `[[1],[2],[3],[4],[1,2],[1,3],[1,4],[2,3],[2,4],[3,4],[1,2,3],[1,2,4],[1,3,4],[2,3,4],[1,2,3,4]]`. Outcome: `completed`. Independent expected-value basis: Independent bitmask enumeration of every nonempty subset. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N003** - Explicit input: `{"simplex":[2,3,4]}`. Observed value: `[[2],[3],[4],[2,3],[2,4],[3,4],[2,3,4]]`. Outcome: `completed`. Independent expected-value basis: Independent bitmask enumeration of every nonempty subset. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N004** - Explicit input: `{"simplex":[3,4,5,6]}`. Observed value: `[[3],[4],[5],[6],[3,4],[3,5],[3,6],[4,5],[4,6],[5,6],[3,4,5],[3,4,6],[3,5,6],[4,5,6],[3,4,5,6]]`. Outcome: `completed`. Independent expected-value basis: Independent bitmask enumeration of every nonempty subset. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N005** - Explicit input: `{"simplex":[4,5,6]}`. Observed value: `[[4],[5],[6],[4,5],[4,6],[5,6],[4,5,6]]`. Outcome: `completed`. Independent expected-value basis: Independent bitmask enumeration of every nonempty subset. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N006** - Explicit input: `{"simplex":[5,6,7,8]}`. Observed value: `[[5],[6],[7],[8],[5,6],[5,7],[5,8],[6,7],[6,8],[7,8],[5,6,7],[5,6,8],[5,7,8],[6,7,8],[5,6,7,8]]`. Outcome: `completed`. Independent expected-value basis: Independent bitmask enumeration of every nonempty subset. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N007** - Explicit input: `{"simplex":[6,7,8]}`. Observed value: `[[6],[7],[8],[6,7],[6,8],[7,8],[6,7,8]]`. Outcome: `completed`. Independent expected-value basis: Independent bitmask enumeration of every nonempty subset. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N008** - Explicit input: `{"simplex":[7,8,9,10]}`. Observed value: `[[7],[8],[9],[10],[7,8],[7,9],[7,10],[8,9],[8,10],[9,10],[7,8,9],[7,8,10],[7,9,10],[8,9,10],[7,8,9,10]]`. Outcome: `completed`. Independent expected-value basis: Independent bitmask enumeration of every nonempty subset. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N009** - Explicit input: `{"simplex":[8,9,10]}`. Observed value: `[[8],[9],[10],[8,9],[8,10],[9,10],[8,9,10]]`. Outcome: `completed`. Independent expected-value basis: Independent bitmask enumeration of every nonempty subset. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N010** - Explicit input: `{"simplex":[9,10,11,12]}`. Observed value: `[[9],[10],[11],[12],[9,10],[9,11],[9,12],[10,11],[10,12],[11,12],[9,10,11],[9,10,12],[9,11,12],[10,11,12],[9,10,11,12]]`. Outcome: `completed`. Independent expected-value basis: Independent bitmask enumeration of every nonempty subset. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

## Simplex Orientation

Retain the supplied vertex order until its parity is calculated. Sorting vertices without retaining the sign erases orientation. The runtime uses permutation-cycle parity; compare it against inversion parity or an adjacent-swap witness. An orientation is algebraic, not a handedness measurement from an apparatus.

The ten recorded cases use the following explicit inputs. The full expected and observed envelopes, input hashes, refusal subjects and scalar types are retained in the corresponding results and planning files. The entries below do not imply empirical measurement or a broader authority decision.

**RA6895-N011** - Explicit input: `{"simplex":[0,1,2,3]}`. Observed value: `{"sign":1,"sorted":[0,1,2,3]}`. Outcome: `completed`. Independent expected-value basis: Permutation inversion parity; runtime uses permutation cycle parity. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N012** - Explicit input: `{"simplex":[0,1,3,2]}`. Observed value: `{"sign":-1,"sorted":[0,1,2,3]}`. Outcome: `completed`. Independent expected-value basis: Permutation inversion parity; runtime uses permutation cycle parity. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N013** - Explicit input: `{"simplex":[0,2,1,3]}`. Observed value: `{"sign":-1,"sorted":[0,1,2,3]}`. Outcome: `completed`. Independent expected-value basis: Permutation inversion parity; runtime uses permutation cycle parity. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N014** - Explicit input: `{"simplex":[0,2,3,1]}`. Observed value: `{"sign":1,"sorted":[0,1,2,3]}`. Outcome: `completed`. Independent expected-value basis: Permutation inversion parity; runtime uses permutation cycle parity. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N015** - Explicit input: `{"simplex":[0,3,1,2]}`. Observed value: `{"sign":1,"sorted":[0,1,2,3]}`. Outcome: `completed`. Independent expected-value basis: Permutation inversion parity; runtime uses permutation cycle parity. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N016** - Explicit input: `{"simplex":[0,3,2,1]}`. Observed value: `{"sign":-1,"sorted":[0,1,2,3]}`. Outcome: `completed`. Independent expected-value basis: Permutation inversion parity; runtime uses permutation cycle parity. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N017** - Explicit input: `{"simplex":[1,0,2,3]}`. Observed value: `{"sign":-1,"sorted":[0,1,2,3]}`. Outcome: `completed`. Independent expected-value basis: Permutation inversion parity; runtime uses permutation cycle parity. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N018** - Explicit input: `{"simplex":[1,0,3,2]}`. Observed value: `{"sign":1,"sorted":[0,1,2,3]}`. Outcome: `completed`. Independent expected-value basis: Permutation inversion parity; runtime uses permutation cycle parity. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N019** - Explicit input: `{"simplex":[1,2,0,3]}`. Observed value: `{"sign":1,"sorted":[0,1,2,3]}`. Outcome: `completed`. Independent expected-value basis: Permutation inversion parity; runtime uses permutation cycle parity. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N020** - Explicit input: `{"simplex":[1,2,3,0]}`. Observed value: `{"sign":-1,"sorted":[0,1,2,3]}`. Outcome: `completed`. Independent expected-value basis: Permutation inversion parity; runtime uses permutation cycle parity. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

## Triangle Boundary

Use the alternating oriented boundary and canonical edge bases. A descending edge must contribute its orientation sign when normalized. Reversing the triangle must negate the full chain, not merely reorder output rows. The result is a formal chain without physical flux units.

The ten recorded cases use the following explicit inputs. The full expected and observed envelopes, input hashes, refusal subjects and scalar types are retained in the corresponding results and planning files. The entries below do not imply empirical measurement or a broader authority decision.

**RA6895-N021** - Explicit input: `{"coefficient":1,"simplex":[0,1,2]}`. Observed value: `[[[0,1],1],[[0,2],-1],[[1,2],1]]`. Outcome: `completed`. Independent expected-value basis: Explicit oriented triangle formula c([b,c]-[a,c]+[a,b]). The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N022** - Explicit input: `{"coefficient":2,"simplex":[1,2,3]}`. Observed value: `[[[1,2],2],[[1,3],-2],[[2,3],2]]`. Outcome: `completed`. Independent expected-value basis: Explicit oriented triangle formula c([b,c]-[a,c]+[a,b]). The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N023** - Explicit input: `{"coefficient":3,"simplex":[2,3,4]}`. Observed value: `[[[2,3],3],[[2,4],-3],[[3,4],3]]`. Outcome: `completed`. Independent expected-value basis: Explicit oriented triangle formula c([b,c]-[a,c]+[a,b]). The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N024** - Explicit input: `{"coefficient":4,"simplex":[3,4,5]}`. Observed value: `[[[3,4],4],[[3,5],-4],[[4,5],4]]`. Outcome: `completed`. Independent expected-value basis: Explicit oriented triangle formula c([b,c]-[a,c]+[a,b]). The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N025** - Explicit input: `{"coefficient":5,"simplex":[4,5,6]}`. Observed value: `[[[4,5],5],[[4,6],-5],[[5,6],5]]`. Outcome: `completed`. Independent expected-value basis: Explicit oriented triangle formula c([b,c]-[a,c]+[a,b]). The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N026** - Explicit input: `{"coefficient":6,"simplex":[5,6,7]}`. Observed value: `[[[5,6],6],[[5,7],-6],[[6,7],6]]`. Outcome: `completed`. Independent expected-value basis: Explicit oriented triangle formula c([b,c]-[a,c]+[a,b]). The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N027** - Explicit input: `{"coefficient":7,"simplex":[6,7,8]}`. Observed value: `[[[6,7],7],[[6,8],-7],[[7,8],7]]`. Outcome: `completed`. Independent expected-value basis: Explicit oriented triangle formula c([b,c]-[a,c]+[a,b]). The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N028** - Explicit input: `{"coefficient":8,"simplex":[7,8,9]}`. Observed value: `[[[7,8],8],[[7,9],-8],[[8,9],8]]`. Outcome: `completed`. Independent expected-value basis: Explicit oriented triangle formula c([b,c]-[a,c]+[a,b]). The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N029** - Explicit input: `{"coefficient":9,"simplex":[8,9,10]}`. Observed value: `[[[8,9],9],[[8,10],-9],[[9,10],9]]`. Outcome: `completed`. Independent expected-value basis: Explicit oriented triangle formula c([b,c]-[a,c]+[a,b]). The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N030** - Explicit input: `{"coefficient":10,"simplex":[9,10,11]}`. Observed value: `[[[9,10],10],[[9,11],-10],[[10,11],10]]`. Outcome: `completed`. Independent expected-value basis: Explicit oriented triangle formula c([b,c]-[a,c]+[a,b]). The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

## Boundary Squared

Compose the same unaugmented boundary map twice and retain exact cancellation. Missing faces or inconsistent orientations invalidate the premise. Test multiple tetrahedron permutations, including negative chain coefficients. Zero residual is an algebraic consistency check and does not establish empirical conservation.

The ten recorded cases use the following explicit inputs. The full expected and observed envelopes, input hashes, refusal subjects and scalar types are retained in the corresponding results and planning files. The entries below do not imply empirical measurement or a broader authority decision.

**RA6895-N031** - Explicit input: `{"coefficient":1,"simplex":[0,1,2,3]}`. Observed value: `[]`. Outcome: `completed`. Independent expected-value basis: Every codimension-two face cancels with its opposite signed occurrence. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N032** - Explicit input: `{"coefficient":2,"simplex":[1,2,3,4]}`. Observed value: `[]`. Outcome: `completed`. Independent expected-value basis: Every codimension-two face cancels with its opposite signed occurrence. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N033** - Explicit input: `{"coefficient":3,"simplex":[2,3,4,5]}`. Observed value: `[]`. Outcome: `completed`. Independent expected-value basis: Every codimension-two face cancels with its opposite signed occurrence. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N034** - Explicit input: `{"coefficient":4,"simplex":[3,4,5,6]}`. Observed value: `[]`. Outcome: `completed`. Independent expected-value basis: Every codimension-two face cancels with its opposite signed occurrence. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N035** - Explicit input: `{"coefficient":5,"simplex":[4,5,6,7]}`. Observed value: `[]`. Outcome: `completed`. Independent expected-value basis: Every codimension-two face cancels with its opposite signed occurrence. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N036** - Explicit input: `{"coefficient":6,"simplex":[5,6,7,8]}`. Observed value: `[]`. Outcome: `completed`. Independent expected-value basis: Every codimension-two face cancels with its opposite signed occurrence. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N037** - Explicit input: `{"coefficient":7,"simplex":[6,7,8,9]}`. Observed value: `[]`. Outcome: `completed`. Independent expected-value basis: Every codimension-two face cancels with its opposite signed occurrence. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N038** - Explicit input: `{"coefficient":8,"simplex":[7,8,9,10]}`. Observed value: `[]`. Outcome: `completed`. Independent expected-value basis: Every codimension-two face cancels with its opposite signed occurrence. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N039** - Explicit input: `{"coefficient":9,"simplex":[8,9,10,11]}`. Observed value: `[]`. Outcome: `completed`. Independent expected-value basis: Every codimension-two face cancels with its opposite signed occurrence. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N040** - Explicit input: `{"coefficient":10,"simplex":[9,10,11,12]}`. Observed value: `[]`. Outcome: `completed`. Independent expected-value basis: Every codimension-two face cancels with its opposite signed occurrence. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

## Graph Components

Include all declared vertices, including isolated ones. Edges are undirected for connectivity, although their input order remains useful for later incidence calculations. Reject missing endpoints, loops and parallel undirected pairs under this selected simple-graph profile. Component labels carry no identity or community authority.

The ten recorded cases use the following explicit inputs. The full expected and observed envelopes, input hashes, refusal subjects and scalar types are retained in the corresponding results and planning files. The entries below do not imply empirical measurement or a broader authority decision.

**RA6895-N041** - Explicit input: `{"edges":[[0,1],[1,2]],"vertices":[0,1,2]}`. Observed value: `[[0,1,2]]`. Outcome: `completed`. Independent expected-value basis: A path is connected; a separately declared isolated vertex is a second component. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N042** - Explicit input: `{"edges":[[0,1],[1,2],[2,3]],"vertices":[0,1,2,3,4]}`. Observed value: `[[0,1,2,3],[4]]`. Outcome: `completed`. Independent expected-value basis: A path is connected; a separately declared isolated vertex is a second component. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N043** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4]],"vertices":[0,1,2,3,4]}`. Observed value: `[[0,1,2,3,4]]`. Outcome: `completed`. Independent expected-value basis: A path is connected; a separately declared isolated vertex is a second component. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N044** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4],[4,5]],"vertices":[0,1,2,3,4,5,6]}`. Observed value: `[[0,1,2,3,4,5],[6]]`. Outcome: `completed`. Independent expected-value basis: A path is connected; a separately declared isolated vertex is a second component. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N045** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6]],"vertices":[0,1,2,3,4,5,6]}`. Observed value: `[[0,1,2,3,4,5,6]]`. Outcome: `completed`. Independent expected-value basis: A path is connected; a separately declared isolated vertex is a second component. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N046** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7]],"vertices":[0,1,2,3,4,5,6,7,8]}`. Observed value: `[[0,1,2,3,4,5,6,7],[8]]`. Outcome: `completed`. Independent expected-value basis: A path is connected; a separately declared isolated vertex is a second component. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N047** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8]],"vertices":[0,1,2,3,4,5,6,7,8]}`. Observed value: `[[0,1,2,3,4,5,6,7,8]]`. Outcome: `completed`. Independent expected-value basis: A path is connected; a separately declared isolated vertex is a second component. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N048** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9]],"vertices":[0,1,2,3,4,5,6,7,8,9,10]}`. Observed value: `[[0,1,2,3,4,5,6,7,8,9],[10]]`. Outcome: `completed`. Independent expected-value basis: A path is connected; a separately declared isolated vertex is a second component. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N049** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10]],"vertices":[0,1,2,3,4,5,6,7,8,9,10]}`. Observed value: `[[0,1,2,3,4,5,6,7,8,9,10]]`. Outcome: `completed`. Independent expected-value basis: A path is connected; a separately declared isolated vertex is a second component. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N050** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,11]],"vertices":[0,1,2,3,4,5,6,7,8,9,10,11,12]}`. Observed value: `[[0,1,2,3,4,5,6,7,8,9,10,11],[12]]`. Outcome: `completed`. Independent expected-value basis: A path is connected; a separately declared isolated vertex is a second component. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

## Graph Cycle Rank

Apply E minus V plus the number of connected components only to the admitted finite undirected graph. Do not substitute the formula for a directed-cycle analysis. A union-find redundant-edge count gives a structurally different small-case oracle. The rank describes the supplied graph alone.

The ten recorded cases use the following explicit inputs. The full expected and observed envelopes, input hashes, refusal subjects and scalar types are retained in the corresponding results and planning files. The entries below do not imply empirical measurement or a broader authority decision.

**RA6895-N051** - Explicit input: `{"edges":[[0,1],[1,2],[2,0]],"vertices":[0,1,2]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Connected n-cycle has n edges and n vertices, so E-V+1=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N052** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,0]],"vertices":[0,1,2,3]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Connected n-cycle has n edges and n vertices, so E-V+1=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N053** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4],[4,0]],"vertices":[0,1,2,3,4]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Connected n-cycle has n edges and n vertices, so E-V+1=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N054** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]],"vertices":[0,1,2,3,4,5]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Connected n-cycle has n edges and n vertices, so E-V+1=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N055** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,0]],"vertices":[0,1,2,3,4,5,6]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Connected n-cycle has n edges and n vertices, so E-V+1=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N056** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,0]],"vertices":[0,1,2,3,4,5,6,7]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Connected n-cycle has n edges and n vertices, so E-V+1=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N057** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,0]],"vertices":[0,1,2,3,4,5,6,7,8]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Connected n-cycle has n edges and n vertices, so E-V+1=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N058** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,0]],"vertices":[0,1,2,3,4,5,6,7,8,9]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Connected n-cycle has n edges and n vertices, so E-V+1=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N059** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,0]],"vertices":[0,1,2,3,4,5,6,7,8,9,10]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Connected n-cycle has n edges and n vertices, so E-V+1=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N060** - Explicit input: `{"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,11],[11,0]],"vertices":[0,1,2,3,4,5,6,7,8,9,10,11]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Connected n-cycle has n edges and n vertices, so E-V+1=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

## Euler Characteristic

Close the explicit facets under nonempty faces before forming the alternating count. The current complex includes dimensions zero through three and has a matrix-size ceiling. Equal Euler characteristics do not prove homeomorphism. Use the disk and tetrahedral surface as distinguishable sanity examples.

The ten recorded cases use the following explicit inputs. The full expected and observed envelopes, input hashes, refusal subjects and scalar types are retained in the corresponding results and planning files. The entries below do not imply empirical measurement or a broader authority decision.

**RA6895-N061** - Explicit input: `{"facets":[[0,1,2],[0,2,3],[0,3,1]]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Fan disk counts (n+1)-2n+n=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N062** - Explicit input: `{"facets":[[0,1,2],[0,2,3],[0,3,4],[0,4,1]]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Fan disk counts (n+1)-2n+n=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N063** - Explicit input: `{"facets":[[0,1,2],[0,2,3],[0,3,4],[0,4,5],[0,5,1]]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Fan disk counts (n+1)-2n+n=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N064** - Explicit input: `{"facets":[[0,1,2],[0,2,3],[0,3,4],[0,4,5],[0,5,6],[0,6,1]]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Fan disk counts (n+1)-2n+n=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N065** - Explicit input: `{"facets":[[0,1,2],[0,2,3],[0,3,4],[0,4,5],[0,5,6],[0,6,7],[0,7,1]]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Fan disk counts (n+1)-2n+n=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N066** - Explicit input: `{"facets":[[0,1,2],[0,2,3],[0,3,4],[0,4,5],[0,5,6],[0,6,7],[0,7,8],[0,8,1]]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Fan disk counts (n+1)-2n+n=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N067** - Explicit input: `{"facets":[[0,1,2],[0,2,3],[0,3,4],[0,4,5],[0,5,6],[0,6,7],[0,7,8],[0,8,9],[0,9,1]]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Fan disk counts (n+1)-2n+n=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N068** - Explicit input: `{"facets":[[0,1,2],[0,2,3],[0,3,4],[0,4,5],[0,5,6],[0,6,7],[0,7,8],[0,8,9],[0,9,10],[0,10,1]]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Fan disk counts (n+1)-2n+n=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N069** - Explicit input: `{"facets":[[0,1,2],[0,2,3],[0,3,4],[0,4,5],[0,5,6],[0,6,7],[0,7,8],[0,8,9],[0,9,10],[0,10,11],[0,11,1]]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Fan disk counts (n+1)-2n+n=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N070** - Explicit input: `{"facets":[[0,1,2],[0,2,3],[0,3,4],[0,4,5],[0,5,6],[0,6,7],[0,7,8],[0,8,9],[0,9,10],[0,10,11],[0,11,12],[0,12,1]]}`. Observed value: `1`. Outcome: `completed`. Independent expected-value basis: Fan disk counts (n+1)-2n+n=1. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

## Betti Numbers

Compute rational boundary ranks and subtract the incoming and outgoing ranks from each chain-group dimension. Keep the coefficient field explicit: this does not recover integral torsion. A filled simplex is contractible, while its boundary surface can retain a nonzero top-dimensional Betti number.

The ten recorded cases use the following explicit inputs. The full expected and observed envelopes, input hashes, refusal subjects and scalar types are retained in the corresponding results and planning files. The entries below do not imply empirical measurement or a broader authority decision.

**RA6895-N071** - Explicit input: `{"facets":[[0,1,2],[0,2,3],[0,3,1]]}`. Observed value: `[1,0,0]`. Outcome: `completed`. Independent expected-value basis: A filled fan disk is contractible; the tetrahedral surface has one two-dimensional void. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N072** - Explicit input: `{"facets":[[1,2,3],[1,2,4],[1,3,4],[2,3,4]]}`. Observed value: `[1,0,1]`. Outcome: `completed`. Independent expected-value basis: A filled fan disk is contractible; the tetrahedral surface has one two-dimensional void. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N073** - Explicit input: `{"facets":[[0,1,2],[0,2,3],[0,3,4],[0,4,5],[0,5,1]]}`. Observed value: `[1,0,0]`. Outcome: `completed`. Independent expected-value basis: A filled fan disk is contractible; the tetrahedral surface has one two-dimensional void. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N074** - Explicit input: `{"facets":[[3,4,5],[3,4,6],[3,5,6],[4,5,6]]}`. Observed value: `[1,0,1]`. Outcome: `completed`. Independent expected-value basis: A filled fan disk is contractible; the tetrahedral surface has one two-dimensional void. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N075** - Explicit input: `{"facets":[[0,1,2],[0,2,3],[0,3,4],[0,4,5],[0,5,6],[0,6,7],[0,7,1]]}`. Observed value: `[1,0,0]`. Outcome: `completed`. Independent expected-value basis: A filled fan disk is contractible; the tetrahedral surface has one two-dimensional void. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N076** - Explicit input: `{"facets":[[5,6,7],[5,6,8],[5,7,8],[6,7,8]]}`. Observed value: `[1,0,1]`. Outcome: `completed`. Independent expected-value basis: A filled fan disk is contractible; the tetrahedral surface has one two-dimensional void. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N077** - Explicit input: `{"facets":[[0,1,2],[0,2,3],[0,3,4],[0,4,5],[0,5,6],[0,6,7],[0,7,8],[0,8,9],[0,9,1]]}`. Observed value: `[1,0,0]`. Outcome: `completed`. Independent expected-value basis: A filled fan disk is contractible; the tetrahedral surface has one two-dimensional void. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N078** - Explicit input: `{"facets":[[7,8,9],[7,8,10],[7,9,10],[8,9,10]]}`. Observed value: `[1,0,1]`. Outcome: `completed`. Independent expected-value basis: A filled fan disk is contractible; the tetrahedral surface has one two-dimensional void. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N079** - Explicit input: `{"facets":[[0,1,2],[0,2,3],[0,3,4],[0,4,5],[0,5,6],[0,6,7],[0,7,8],[0,8,9],[0,9,10],[0,10,11],[0,11,1]]}`. Observed value: `[1,0,0]`. Outcome: `completed`. Independent expected-value basis: A filled fan disk is contractible; the tetrahedral surface has one two-dimensional void. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N080** - Explicit input: `{"facets":[[9,10,11],[9,10,12],[9,11,12],[10,11,12]]}`. Observed value: `[1,0,1]`. Outcome: `completed`. Independent expected-value basis: A filled fan disk is contractible; the tetrahedral surface has one two-dimensional void. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

## Chain Cycle

Accumulate signed endpoint contributions in the declared edge order. An equal-weight loop cancels; removing its closing coefficient leaves two endpoints. A chain being closed does not imply it is a boundary. Formal cancellation is not evidence of a real conservation process.

The ten recorded cases use the following explicit inputs. The full expected and observed envelopes, input hashes, refusal subjects and scalar types are retained in the corresponding results and planning files. The entries below do not imply empirical measurement or a broader authority decision.

**RA6895-N081** - Explicit input: `{"coefficients":[1,1,1],"edges":[[0,1],[1,2],[2,0]],"vertices":[0,1,2]}`. Observed value: `{"boundary":[],"is_cycle":true}`. Outcome: `completed`. Independent expected-value basis: Equal cyclic edge coefficients cancel at every vertex; an opened path leaves only two endpoints. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N082** - Explicit input: `{"coefficients":[2,2,2,0],"edges":[[0,1],[1,2],[2,3],[3,0]],"vertices":[0,1,2,3]}`. Observed value: `{"boundary":[[0,-2],[3,2]],"is_cycle":false}`. Outcome: `completed`. Independent expected-value basis: Equal cyclic edge coefficients cancel at every vertex; an opened path leaves only two endpoints. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N083** - Explicit input: `{"coefficients":[3,3,3,3,3],"edges":[[0,1],[1,2],[2,3],[3,4],[4,0]],"vertices":[0,1,2,3,4]}`. Observed value: `{"boundary":[],"is_cycle":true}`. Outcome: `completed`. Independent expected-value basis: Equal cyclic edge coefficients cancel at every vertex; an opened path leaves only two endpoints. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N084** - Explicit input: `{"coefficients":[4,4,4,4,4,0],"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]],"vertices":[0,1,2,3,4,5]}`. Observed value: `{"boundary":[[0,-4],[5,4]],"is_cycle":false}`. Outcome: `completed`. Independent expected-value basis: Equal cyclic edge coefficients cancel at every vertex; an opened path leaves only two endpoints. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N085** - Explicit input: `{"coefficients":[5,5,5,5,5,5,5],"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,0]],"vertices":[0,1,2,3,4,5,6]}`. Observed value: `{"boundary":[],"is_cycle":true}`. Outcome: `completed`. Independent expected-value basis: Equal cyclic edge coefficients cancel at every vertex; an opened path leaves only two endpoints. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N086** - Explicit input: `{"coefficients":[6,6,6,6,6,6,6,0],"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,0]],"vertices":[0,1,2,3,4,5,6,7]}`. Observed value: `{"boundary":[[0,-6],[7,6]],"is_cycle":false}`. Outcome: `completed`. Independent expected-value basis: Equal cyclic edge coefficients cancel at every vertex; an opened path leaves only two endpoints. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N087** - Explicit input: `{"coefficients":[7,7,7,7,7,7,7,7,7],"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,0]],"vertices":[0,1,2,3,4,5,6,7,8]}`. Observed value: `{"boundary":[],"is_cycle":true}`. Outcome: `completed`. Independent expected-value basis: Equal cyclic edge coefficients cancel at every vertex; an opened path leaves only two endpoints. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N088** - Explicit input: `{"coefficients":[8,8,8,8,8,8,8,8,8,0],"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,0]],"vertices":[0,1,2,3,4,5,6,7,8,9]}`. Observed value: `{"boundary":[[0,-8],[9,8]],"is_cycle":false}`. Outcome: `completed`. Independent expected-value basis: Equal cyclic edge coefficients cancel at every vertex; an opened path leaves only two endpoints. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N089** - Explicit input: `{"coefficients":[9,9,9,9,9,9,9,9,9,9,9],"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,0]],"vertices":[0,1,2,3,4,5,6,7,8,9,10]}`. Observed value: `{"boundary":[],"is_cycle":true}`. Outcome: `completed`. Independent expected-value basis: Equal cyclic edge coefficients cancel at every vertex; an opened path leaves only two endpoints. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N090** - Explicit input: `{"coefficients":[10,10,10,10,10,10,10,10,10,10,10,0],"edges":[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,11],[11,0]],"vertices":[0,1,2,3,4,5,6,7,8,9,10,11]}`. Observed value: `{"boundary":[[0,-10],[11,10]],"is_cycle":false}`. Outcome: `completed`. Independent expected-value basis: Equal cyclic edge coefficients cancel at every vertex; an opened path leaves only two endpoints. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

## Chain Boundary

Test whether the supplied oriented edge-chain vector lies in the image of the face-boundary matrix using exact augmented rank. The zero chain is always in the image, including when the image has rank zero. Do not silently supply a missing triangle face to make a loop bound.

The ten recorded cases use the following explicit inputs. The full expected and observed envelopes, input hashes, refusal subjects and scalar types are retained in the corresponding results and planning files. The entries below do not imply empirical measurement or a broader authority decision.

**RA6895-N091** - Explicit input: `{"chain":[[[0,1],1],[[0,2],-1],[[1,2],1]],"facets":[[0,1,2]]}`. Observed value: `true`. Outcome: `completed`. Independent expected-value basis: The triangular loop bounds exactly when the supplied complex includes its two-simplex. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N092** - Explicit input: `{"chain":[[[0,1],2],[[0,2],-2],[[1,2],2]],"facets":[[0,1],[0,2],[1,2]]}`. Observed value: `false`. Outcome: `completed`. Independent expected-value basis: The triangular loop bounds exactly when the supplied complex includes its two-simplex. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N093** - Explicit input: `{"chain":[[[0,1],3],[[0,2],-3],[[1,2],3]],"facets":[[0,1,2]]}`. Observed value: `true`. Outcome: `completed`. Independent expected-value basis: The triangular loop bounds exactly when the supplied complex includes its two-simplex. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N094** - Explicit input: `{"chain":[[[0,1],4],[[0,2],-4],[[1,2],4]],"facets":[[0,1],[0,2],[1,2]]}`. Observed value: `false`. Outcome: `completed`. Independent expected-value basis: The triangular loop bounds exactly when the supplied complex includes its two-simplex. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N095** - Explicit input: `{"chain":[[[0,1],5],[[0,2],-5],[[1,2],5]],"facets":[[0,1,2]]}`. Observed value: `true`. Outcome: `completed`. Independent expected-value basis: The triangular loop bounds exactly when the supplied complex includes its two-simplex. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N096** - Explicit input: `{"chain":[[[0,1],6],[[0,2],-6],[[1,2],6]],"facets":[[0,1],[0,2],[1,2]]}`. Observed value: `false`. Outcome: `completed`. Independent expected-value basis: The triangular loop bounds exactly when the supplied complex includes its two-simplex. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N097** - Explicit input: `{"chain":[[[0,1],7],[[0,2],-7],[[1,2],7]],"facets":[[0,1,2]]}`. Observed value: `true`. Outcome: `completed`. Independent expected-value basis: The triangular loop bounds exactly when the supplied complex includes its two-simplex. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N098** - Explicit input: `{"chain":[[[0,1],8],[[0,2],-8],[[1,2],8]],"facets":[[0,1],[0,2],[1,2]]}`. Observed value: `false`. Outcome: `completed`. Independent expected-value basis: The triangular loop bounds exactly when the supplied complex includes its two-simplex. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N099** - Explicit input: `{"chain":[[[0,1],9],[[0,2],-9],[[1,2],9]],"facets":[[0,1,2]]}`. Observed value: `true`. Outcome: `completed`. Independent expected-value basis: The triangular loop bounds exactly when the supplied complex includes its two-simplex. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.

**RA6895-N100** - Explicit input: `{"chain":[[[0,1],10],[[0,2],-10],[[1,2],10]],"facets":[[0,1],[0,2],[1,2]]}`. Observed value: `false`. Outcome: `completed`. Independent expected-value basis: The triangular loop bounds exactly when the supplied complex includes its two-simplex. The typed envelope and unchanged-input checks passed; the paired candidate remains an inadmissible subject.
