# Elowen Cairn v676-v6 corrected-head lifecycle-test selection

The correction2-final canonical receipt `1879b71dbc7fb4f5acf9dd7ca841ad927e5a32f1bc199b520dfd06d6f64af544` remains immutable and invalid with zero success credit. It passed all 39 detailed checks but its test subprocess retained two failures because original-final-only tests were executed against a later correction head.

Correction3 does not rewrite those tests or convert their failures into passes. It excludes them from corrected-head current-tree execution and replaces them with explicit Git-tree manifest replay and direct-parent topology checks spanning original final, correction1, correction2, and correction3. The two existing x1/evidence lifecycle exclusions remain unchanged. No proposal, outcome, mutation, gap, gate, authority boundary, or prior receipt changes. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.
