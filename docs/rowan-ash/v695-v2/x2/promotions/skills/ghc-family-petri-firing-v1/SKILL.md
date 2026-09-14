---
name: ghc-family-petri-firing-v1
description: Review enabled transitions, single firing, firing sequence, commutation witness for explicitly declared finite synthetic Petri nets.
---

# ghc-family-petri-firing-v1

This curated capability combines 4 validated local operation skills. Use the companion `ghc_family_petri_firing_v1.txt` in the D-first `petri-net-v1/runners` tool bank with Node and a UTF-8 JSON request on standard input. The two sibling support modules in `petri-net-v1/code` are required. Source selection and exact byte bindings are recorded in the phase promotion receipt.

The request contains exactly `operation`, `net`, and `parameters`. A net contains `case_id`, `synthetic: true`, ordered `places`, an integer `initial` marking, and `transitions` with `id`, `pre` and `post` vectors. Retain both arc vectors; a zero incidence entry can still require an enabling token. Select only an operation supported below and consult its phase-frozen JSON example for the exact parameter keys.

- `enabled_transitions`: Check every input-arc demand against the supplied marking. Individual enabledness is not simultaneous fireability.
- `single_firing`: Consume the input arcs and then produce the output arcs for one enabled transition. A non-enabled transition has no successful successor marking.
- `firing_sequence`: Check each step and retain every intermediate marking. A transition multiset alone does not certify a feasible order.
- `commutation_witness`: Compare both two-step orders at a particular marking. Coenabled transitions can conflict; a missing second step is not a commutation witness.

Input validation admits at most eight places and transitions, weights through eight and tokens through sixty-four. Reachability refuses token, state or edge budget overflow; no partial graph is called complete. A supplied place or transition certificate is checked exactly but is not a complete invariant basis. L4 liveness concerns eventual enabledness from every reachable marking and makes no fairness promise.

Preserve malformed inputs and errors at zero subject-success credit. A successful refusal is a separate witness. Use only an owner-scoped module and rerun the smallest failed dependency. Do not replay source evidence, successful canonical checks or accepted handoffs. If a capability is superseded, deselect this additive package while retaining its source, receipts and compatibility callers.

The examples are synthetic learning models. They are not observations, physical laws, a consciousness model, professional qualifications, authority grants, independent reproduction, a production deployment or a Stage 20 result. Empirical and authority records remain open or gated until their specific prerequisites exist.
