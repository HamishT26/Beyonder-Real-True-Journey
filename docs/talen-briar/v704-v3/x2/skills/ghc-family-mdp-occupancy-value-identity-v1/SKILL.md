---
name: ghc-family-mdp-occupancy-value-identity-v1
description: "Compare occupancy-based discounted return with the initial optimal value. Use for declared finite synthetic decision records."
---

# mdp occupancy value identity

Retain the discounted terminal term; omitting it can make the identity fail.

Use the closed `{op,input}` envelope with operation `mdp_occupancy_value_identity`. Input contains states, two transition rows and rewards per state, terminal values, discount, horizon, stationary policy, initial distribution and reward shift. State count is one through four, horizon zero through four, and exact inputs are integer/fraction strings. Probability rows and initial mass sum exactly to one.

From the owner checkout, invoke `node docs/talen-briar/v704-v3/x2/runners/pair-03.txt request.json response.json`. The caller reads one request and exclusively creates one output; an existing output is not overwritten. It accepts only its declared pair of operations. The frozen examples and expected responses are in `docs/talen-briar/v704-v3/planning/proposals/mdp_occupancy_value_identity.json`.

Compare the complete response, including outcome and external-credit fields. Preserve rejected subjects and append any correction with its input/output byte bindings. Caller success and mathematical value do not close an evidence or authority gate.

Finite synthetic same-owner software and mathematical evidence only. No real process, person, observation, measurement, identity, credential, deployment, empirical GMUT confirmation, production THOS or Freed ID, independent reproduction, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, AGI or ASI, consciousness, personhood, continuity, Theory-of-Everything proof, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
