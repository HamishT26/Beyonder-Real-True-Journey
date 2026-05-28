# v461A-v490A Ninety-Minute Heartbeat Run Status

Generated UTC: `2026-05-28T13:00:12Z`

Generated NZ: `2026-05-29T01:00:12+12:00`

Status: `heartbeat_replacement_packet_authored`

Shared head at authoring: `58dc715f8af9925a22e97b6e1b7d60401044d3eb`

Remote drift at authoring: `0 0`

v464A opened: `false`

## Changes

- Corrected obsolete shared omega head from the `bf527c7...` series to `58dc715f8af9925a22e97b6e1b7d60401044d3eb`.
- Changed automation cadence from every 3 hours to every 90 minutes.
- Changed run model from one v1/v2 pair per heartbeat to one phase-version half per heartbeat.
- Set sequence to `v461A v1`, `v461A v2`, `v462A v1`, `v462A v2`, continuing through `v490A v2`.
- Preserved Kimi hold, postponed Parfit-main reconnect, App-vs-CLI boundaries, forward-only publication checks, and no-v491+ stop rule.
- Recorded NZ calendar correction: Friday midnight after Thursday May 28 is Friday May 29, 2026.

Next action: paste the v2 ninety-minute packet into the paused automation and unpause when ready.
