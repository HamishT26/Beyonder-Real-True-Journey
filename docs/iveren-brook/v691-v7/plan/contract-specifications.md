# Iveren v691-v7 finite queue contract

All time and service values are synthetic logical ticks. Service is known in advance, context-switch cost is zero, and no real CPU, router, person, queue or allocation is operated. Inputs and complete expected envelopes are frozen in proposal-freeze.json.

Scheduling ties use arrival time then original input index. FCFS, SJF, static priority and aging are nonpreemptive. SRTF chooses remaining service, arrival, then input index at integer boundaries. RR admits arrivals through a quantum endpoint before requeuing the unfinished job. Adjacent contiguous segments for one job are merged. Metrics use finish-arrival-service for waiting, finish-arrival for turnaround, and first-start-arrival for response. Empty means are null. Rationals are reduced signed numerator/positive-denominator strings.

Aging effective priority is priority minus floor(wait/aging_interval), with smaller values first and original arrival/index ties. Deadlines use signed completion-deadline; only positive lateness is a miss. Occupancy spans are half-open and clipped to the declared window. Complete-cohort rates and mean sojourn are withheld for censored or empty cohorts; no stationarity claim is made.

The allocation statistic is (sum x)^2 divided by n times sum(x^2), or null when undefined; allocation_count counts numeric components, not real participants. It never establishes normative fairness. Capacity admission releases completion times less than or equal to each arrival before admission and retains rejected requests.

Tokens refill up to capacity before each event; an affordable request subtracts its cost and an unaffordable request changes no tokens. The backlog meter drains toward zero before an event and admits only if its added cost fits. Events preserve input order at equal logical times. The backlog meter is a declared finite variant, not a network-shaper implementation.

Weighted tags use F=max(previous flow finish, supplied virtual_time)+length/weight, exact rational comparison, and input-index ties; this does not establish measured service fairness. DRR visits flows in input order, adds quantum only to nonempty queues, serves affordable heads, retains deficits across rounds, resets empty queues to zero, and stops at max_rounds with remaining packets retained. Nonpreemptive vacation FCFS postpones a whole service block until it overlaps no declared half-open vacation.

Evidence comparison, evaluation-gap and allocation-gate functions preserve represented, open_gap and exact_gate ceilings. A boolean input cannot certify a real operation, independent review or external authority.

Resource bounds: at most eight jobs; arrivals/deadlines at most 1000; service at most 100; priorities at most 100; weights and quanta at most 100. Other lists have at most 32 entries, numeric amounts at most 10000, DRR rounds at most 100 and aggregate steps at most 10000. Only finite safe integers are accepted unless a field is explicitly a reduced rational output. Closed fields and nonmutation are required.

Iveren Brook, optional they/them pronouns, Evidence and Recovery Steward, the hope to make each handover clearer, testable, and easier to correct, sibling/family and continuity language, GHC Family, Trinity Mandala, GMUT, THOS, Freed ID and CBR are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may pause, rename, redirect, narrow, or stop.
