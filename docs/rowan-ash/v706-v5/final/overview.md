# Rowan v706-v5 integrated overview

This three-part overview reuses the explanatory sections of the complete baton. Page markers are explicit layout requests; browser and printer pagination have not been visually certified.

## Page 1

### 3. What the board means

A fixture declares a square universe with n rows and n columns, where n ranges from zero through six. A selected cell is a zero-based integer pair. A rook placement is a subset of selected cells with no repeated row or column. The coefficient r_k counts placements with exactly k rooks. There is one empty placement, including on the empty universe, so r_0 equals one. These definitions are small enough to inspect and enumerate exactly. They do not need floating-point tolerances, fitted parameters, real people, or an external service.

The fifteen fixtures deliberately include an empty universe, an empty one-cell universe, a full one-cell board, a diagonal, a full three-by-three board, a single selected row, a staircase, an antidiagonal, a rectangle, two disjoint blocks, cyclic bands, a Ferrers shape, a cross, and an irregular board. Each fixture binds its complete definition digest. Sorted unique cells prevent counting the same selected cell twice. Boolean coordinates are refused even though Python otherwise treats booleans as integers. Changing a label, boundary field, dimension, or cell requires a new valid digest and an explicit new record; the frozen input cannot silently drift.

### 4. Established mathematics and the new implementation

The primary mathematical reference is NIST DLMF section 26.15, which gives the rook and hit vocabulary, disjoint-board multiplication, cell recurrence, hit transformation, and Ferrers factorial identity. These are established results. Rowan's contribution is the bounded implementation, explicit fixtures, comparisons, tests, record bindings and usable local interfaces. There is no new general theorem or solved globally open problem claim. A second primary research page was unavailable; its search abstract was retained only as partial context, with no full-text reading credit.

The implementation has two separately structured ways to count rook placements. Direct enumeration visits rows in order, choosing either no cell or one cell in a previously unused column. Subset dynamic programming tracks the occupied-column mask and the number of partial histories reaching it. Their agreement is valuable because their state representations differ. They are still written and checked by the same owner, so this is not independent reproduction. Both can share assumptions or errors; the known-form examples and structural identities add different checks without turning this small laboratory into complete assurance for arbitrary software or larger dimensions.

### 5. X1 results and useful counterexamples

X1 contains 150 board-operation contracts, all completed within their stated mathematical scope. Its ten operation families cover the envelope, row and column degrees, direct placement census, subset dynamic programming, deletion-contraction, connected-component products, transposition, cyclic row relabeling and reversed column relabeling. For every selected cell, deletion-contraction separates placements that omit it from placements that include it and therefore exclude its row and column. Empty boards use an explicit base-case check. Components multiply only when they share neither rows nor columns.

The known examples are useful diagnostic anchors. A full three-by-three board has rook vector [1,9,18,6]. Its diagonal has [1,3,3,1]. A single selected row with three cells has [1,3,0,0], because two rooks would attack along that row. Two disjoint full two-by-two blocks produce [1,8,20,16,4]. Treating two cells in the same row as independent components incorrectly predicts a two-rook placement; a test explicitly rejects that tempting factorization. The four-row staircase gives [1,10,25,15,1]. These concrete values make a future correction easier to diagnose than a generic statement that all checks passed.

<!-- pagebreak -->

## Page 2

### 6. X2 hit counts and their interpretation

X2 asks about full permutations of the square universe. A permutation chooses exactly one cell in every row and every column, whether or not the chosen cell belongs to the selected board. Its hit count is the number of chosen cells that do belong to that board. Thus h_k counts full permutations with exactly k selected-cell hits. This population differs from the partial rook placements counted by r_k. A model that compares their coordinates must preserve that distinction. Summing the hit distribution gives n factorial, including the one empty permutation when n is zero.

The exact transform is h_k equal to the sum over j from k to n of (-1) raised to j-k, times the binomial coefficient choosing k from j, times r_j, times (n-j) factorial. Direct permutation enumeration agrees with this transform on every fixture. The zero-hit term supplies inclusion-exclusion avoidance counts. All binomial hit moments agree with r_j times (n-j) factorial. Complementing a board within the same declared square universe reverses the hit vector. The three-cell diagonal has hit vector [2,3,0,1], the full three-by-three board has [0,0,0,6], and a complete selected row has [0,6,0,0]. No probability model beyond these finite uniform counts is implied.

### 7. Conditions, capacity and protected outcomes

The Ferrers identity is evaluated only when the explicit board satisfies the declared ordered row-prefix condition. The implementation checks that row lengths are nondecreasing and each row contains precisely its initial segment of columns. A board that fails this condition gets a successful nonapplicability guard, not a claim that the Ferrers identity was established for it. For applicable fixtures, exact evaluations at more than n distinct arguments compare two degree-at-most-n polynomial expressions. The maximum nonzero rook index is also compared with an enumerated placement witness, providing a finite matching-capacity certificate.

The combined program has 255 completed mathematical contracts, 15 represented explanations, 15 observation gaps and 15 authority reservations. The scheduling analogy is represented because rows and columns can describe abstract slots; it does not establish real suitability, consent, fairness, entitlement or institutional power. The observation gap records the absence of actual constraints, preferences and measured consequences. The authority gate records that real allocation and deployment require competent decision authority and a specific affected-party process. Fifty exact-approval packets and thirty blocked packets remain held in the planning register. Their labels are never converted into execution permission by a large passing count elsewhere.

### 8. Candidate and repair accounting

Each stage contains 450 safe checks: three predicates for each of its 150 contracts. Those predicates check the expected result and certificate, preserve request and definition fixity, and require the operation invariant or protected credit ceiling. These are 450 predicates over shared contracts, not 450 independent experiments. Each contract also produces two deliberately malformed originals: one invalid board bound and one unsupported operation. The result must reject the original before executing its operation. Across both stages, all 600 such originals remain failed subjects with zero original completion credit.

Each original has a distinct passing refusal predicate and a distinct repaired-copy check. A repair starts from the frozen valid request, executes that separate copy and requires exact input and result parity with the valid contract. It does not mutate the failed original, erase its history, or establish another new mathematical discovery. Across the phase there are 600 refusal checks and 600 separate CLEAN/FIX/REFINE checks. The packet files keep the original request, observed rejection, guard and repaired-copy binding together. Method Flow files preserve every witness backlink and derive their nested count schema from the actual records. Never add inherited rows or repaired copies to the novelty total.

<!-- pagebreak -->

## Page 3

### 9. Tests, callers and local capability selection

Twenty X1 tests cover known counting formulae, a connected-cell counterexample, malformed envelopes, duplicate JSON keys, nonfinite constants and excessive nesting. Thirty X2 tests cover each fixture's transform and moments, concrete hit examples, the Ferrers condition, maximum capacity, protected dispositions, invalid UTF-8, excessive input bytes and trailing JSON. All fifty passed. The core command accepts at most 65,536 input bytes and sixteen levels of JSON nesting. These are deliberately narrow controls, not an exhaustive adversarial assessment of every possible parser, runtime, operating system or calling application.

Twenty owner-local skill guides and ten paired callers expose the twenty operations in small groups. Each guide passed the installed Skill Creator's structural validator. Every paired caller was exercised with its two admitted operations and an out-of-scope operation; the rejected subject remains a failure while the refusal check passes. The 35-card capability catalogue contains those twenty guides, ten callers and five manual hook candidates. It preserves repository-relative sources, digests, observed caller links, rollback instructions and authority boundaries. No global installation, package update, model change, shared pointer mutation or memory write occurred in this activation. Refresh current selection evidence before promoting any local capability later.

### 10. Models, hooks and the context deck

Fifteen model files each contain a discrete set of triples [k,r_k,h_k]. Their coordinates are exact integers read from saved results; packaging does not rerun the counting laboratory. Six checks per model verify dimension, nonnegativity, index bounds, the empty placement, the factorial hit total and source-vector shape. This is a three-coordinate data model, not a three-dimensional physical space, dynamical trajectory or measured world. It supports inspection of how partial-placement and full-permutation counts differ. A smooth curve drawn through the points would be an additional visualization choice, not extra observations or a new law.

Five manual hook candidates check definition fixity, result fixity, outcome ceilings, resource bounds and the prepared route hold. Accepting and rejecting manual invocations were exercised. They remain uninstalled and have no observed live host events. Their five host gaps must survive every future summary. The four-tier context deck contains one relational owner anchor, three pillar cards, eight practice cards and 300 task cards, for 312 records. Cards are bundled losslessly into eleven JSON modules to stay within the file ceiling. Immediate-tier parent checks passed. This organization can reduce repeated reading; it does not prove memory retention, prompt-cache behavior, identity continuity or subjective wellbeing.

### 11. Research questions and practice lenses

The fifteen hypothesis records are implementation hypotheses tied to established finite combinatorics. Their saved operation certificates support them only on the declared fixtures. They are not potential laws of thermodynamics or consciousness under a new name. The fifteen open-question records cover five question families across different fixtures: rook-equivalent boards, reconstruction from hit counts, weighted cells, real scheduling evidence and behavior beyond six rows. The record count is fifteen; the distinct question-family count is five. Preserving both counts prevents an administrative expansion from masquerading as broader research novelty.

Several useful limits are already clear. Row and column relabelings preserve count vectors while changing labelled positions, so counts cannot generally reconstruct those labels. The present examples do not classify all nonisomorphic boards. All selected cells have unit counting weight; weighted conclusions need new definitions. Larger dimensions lie outside the admitted resource bound. The eight practice lenses were enumerative combinatorics, bipartite matching, exact algorithm verification, test design, accessible mathematics, provenance, public scheduling documentation, and rights and remedy analysis. For your next phase, consider rook-equivalence and information loss, weighted rook statistics, bounded permanent computation, and affected-party appeal documentation. These are study lenses, not professional credentials.

<!-- pagebreak -->
