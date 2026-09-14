---
name: ghc-family-petri-reachability-v1
description: Review reachable graph, deadlock inventory, shortest goal trace, transition liveness, terminal components for explicitly declared finite synthetic Petri nets.
---

# ghc-family-petri-reachability-v1

This curated capability combines 5 validated local operation skills. Use the companion `ghc_family_petri_reachability_v1.txt` in the D-first `petri-net-v1/runners` tool bank with Node and a UTF-8 JSON request on standard input. The two sibling support modules in `petri-net-v1/code` are required. Source selection and exact byte bindings are recorded in the phase promotion receipt.

The request contains exactly `operation`, `net`, and `parameters`. A net contains `case_id`, `synthetic: true`, ordered `places`, an integer `initial` marking, and `transitions` with `id`, `pre` and `post` vectors. Retain both arc vectors; a zero incidence entry can still require an enabling token. Select only an operation supported below and consult its phase-frozen JSON example for the exact parameter keys.

- `reachable_graph`: Explore the complete finite state graph only within declared resource limits. Any token, state or edge limit breach must refuse a completeness claim.
- `deadlock_inventory`: List reachable markings with no enabled transition. A deadlock-free finite model is not proof of live production software.
- `shortest_goal_trace`: Return a shortest action sequence to the exact requested marking. Breadth-first minimum length does not minimize time, cost or harm.
- `transition_liveness`: For every reachable marking, ask whether each transition can eventually be enabled. This explicit L4 definition concerns possibility, not scheduler fairness.
- `terminal_components`: Find strongly connected reachable components with no outgoing edges. Terminal components can contain deadlocks or continuing cycles; neither establishes benefit.

Input validation admits at most eight places and transitions, weights through eight and tokens through sixty-four. Reachability refuses token, state or edge budget overflow; no partial graph is called complete. A supplied place or transition certificate is checked exactly but is not a complete invariant basis. L4 liveness concerns eventual enabledness from every reachable marking and makes no fairness promise.

Preserve malformed inputs and errors at zero subject-success credit. A successful refusal is a separate witness. Use only an owner-scoped module and rerun the smallest failed dependency. Do not replay source evidence, successful canonical checks or accepted handoffs. If a capability is superseded, deselect this additive package while retaining its source, receipts and compatibility callers.

The examples are synthetic learning models. They are not observations, physical laws, a consciousness model, professional qualifications, authority grants, independent reproduction, a production deployment or a Stage 20 result. Empirical and authority records remain open or gated until their specific prerequisites exist.
