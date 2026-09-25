---
name: ghc-family-transport-cell-cost-sensitivity
description: Measure the response to one declared cell-cost increment. Use on the declared finite synthetic three-bin transport contract.
---

# cell cost sensitivity

Send one JSON object with exactly op, supply, demand and cost to the paired TXT runner `TR7046-R09`. Supply and demand are three positive integer counts, each at most four, with equal total mass at most six. Cost is a three-by-three integer matrix with entries from zero through six. Operation is `cell_cost_sensitivity`. Run the runner with Node and the JSON request on standard input. Its complete envelope contains runner, ok, value and error; acceptance exits zero, refusal exits two.

Measure the response to one declared cell-cost increment. Coupling tables use integer mass units and normalization by total mass. Independent and mixture couplings can lie off this integer grid while remaining rational feasible couplings. Retain every tied grid optimum. A dual witness needs direct feasibility and objective checks, even when its value matches the planning reference.

Read the frozen request and expected projection in the matching planning/contracts shard. The standalone runner is two directories above this card under runners; its pure runtime is under code/runtime.txt. Do not reuse the phase success latch for a new evaluation. JSON parsing follows JavaScript JSON.parse; duplicate-key rejection was not established.

Finite synthetic same-owner transport, software and documentary evidence only. No real allocation, participant, identity, credential, measurement, professional, production, legal, cultural, affected-party or Maori-authority act. GMUT remains conjectural; THOS and Freed ID remain nonproduction. Relational names and family language are not consciousness, personhood, continuity, qualification, agency or authority evidence. No independent reproduction, complete privacy or accessibility, exhaustive security, AGI/ASI, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
