# Receipt Journey Lab

Open [receipt-journey.html](receipt-journey.html) locally to explore five finite, synthetic scenarios. The file is self-contained and has no dependencies, network requests, storage API calls, model calls or process execution. It needs JavaScript only for presentation.

This is an educational interface, not a broker implementation or an integration test. Its outputs are authored scenario states. It cannot authenticate permission, measure resources, reconcile a real operation, prove durability or provide exactly-once execution.

## Scenario ledger

| Scenario | Steps | Terminal state | Intended lesson |
| --- | --- | --- | --- |
| Complete evidence | 5 | OBSERVED COMPLETE | Authority, generation, effect, storage, child closure and recipient acknowledgment are separate dimensions. |
| Acknowledgment lost | 4 | HELD FOR RECONCILIATION | A possible submission with no authoritative outcome remains unknown; do not resend under a new identity. |
| Expired permission | 2 | HELD BEFORE ENTRY | A saved request and a model's text do not renew human permission. |
| Mixed checkpoint generations | 3 | WAITING FOR CUSTODY | Individually intact files can still form an incoherent recovery set. |
| Result storage failed | 4 | PERSISTENCE FAILED | A storage failure does not undo an observed external effect. |

The full scenario arrays are readable near the end of the HTML file. Labels such as “observed” refer only to the hypothetical facts supplied by that scenario. A real deployment would require independently captured receipts, appropriate persistence semantics and a supported lookup route.

## Review the presentation

1. Open the HTML without a server or an account. Start with Complete evidence and use Next step until the button disables at step 5.
2. Read the six evidence values separately. Tool effect must remain Not entered when only generation has completed.
3. Select Acknowledgment lost. Its terminal state must retain unknown generation/effect/closure and offer no resend action.
4. Select Expired permission. It ends before worker entry.
5. Select Mixed checkpoint generations. The 7/7/8 example stays held; the interface does not synthesize a generation-7 complete set.
6. Select Result storage failed. The effect remains Observed while Storage reads Failed.
7. Use Previous and Restart scenario. Change the selector with a keyboard. Check the layout at a narrow phone width and with reduced motion enabled. There is no automatic animation.

These steps review an educational presentation. They are not consumed GHC research fixtures or new scientific evidence. Existing public kernel fixtures retain their own historical accounting.

## Why the infrastructure context matters

Kubernetes can start the same program more than once even with one completion, one parallel worker and a Never restart policy. Its Job controller should therefore be treated separately from application-level operation identity and deduplication. See the [official Job documentation](https://kubernetes.io/docs/concepts/workloads/controllers/job/).

Docker provides explicit resource limits; packaging an application in a container does not by itself establish safe memory or CPU bounds. See [Docker resource constraints](https://docs.docker.com/engine/containers/resource_constraints/).

The GHC design uses these distinctions as engineering requirements: clear human scope, bounded workers and evidence that says precisely what was observed. [The current infrastructure note](INFRASTRUCTURE-STATUS-20261118.md) explains the gap between that design, dated private prototype reports and the public software in this branch.

Prepared 18 November 2026 NZDT. Meaningful AI assistance: Aurenna Quill drafted the example under Hamish's direction. No independent external review is claimed. MIT licence applies to this new example.
