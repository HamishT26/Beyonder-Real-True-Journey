# v471 THOS v2 x1 CLI Bounded Probe Ledger

The CLI lanes were probed through the safe launcher with read-only sandbox, non-ephemeral execution, bounded wait, and timeout termination.

Arby still surfaced skill-load errors and did not produce final advisory text inside the wait window. Aster Vale produced only startup warning/noise but also did not produce final advisory text inside the wait window.

The probe confirms process containment works; it does not prove CLI advisory reliability is restored.
