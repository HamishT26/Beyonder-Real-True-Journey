# v461 Parfit Reconnect Attempts

Generated UTC: `2026-05-28T05:30:44.7865767Z`

Status: `candidate_unreachable_historical_handle_reachable`

The screenshot candidate `019e485f-15ed-7830-b422-2bbe530fe893` was retried three times in the current tool surface:

- Attempt 1, direct ID: agent not found.
- Attempt 2, literal `agent//019e485f-15ed-7830-b422-2bbe530fe893`: invalid agent id parse error.
- Attempt 3, direct ID: agent not found.

The historical Parfit/Lorentz handle `019e52d7-c06d-7c31-8a66-2162ff7c658b` remains reachable as advisory context only and returned a reconnect plan.

Going forward:
- Mark the screenshot candidate as `resume_failed_unverified`.
- Keep Parfit/Lorentz as `advisory_reachable_in_current_context_only`.
- If the original visible Parfit tab remains open, ask it for a short v461 reconnect receipt and record that as visible-tab evidence, not callable proof.
