# GHC hybrid workflow

Hamish selected this architecture on 5 October 2026: **PowerShell is the local foundation; cloud Linux handles heavier Linux work; WSL is an optional compatibility layer.** This is an execution and coordination design, not a replacement Windows or Linux kernel.

## Choosing an executor

| Work | Preferred route | What must be checked |
| --- | --- | --- |
| Windows administration, local paths, shortcuts, signed app launch | Local PowerShell | Current process token, target path and the particular operation |
| Git, Node, Python, small portable checks and artifact hashing | Native Windows tools for local work; cloud for larger batches | Actual executable/version and identical input semantics |
| Larger numerical or verification batches | Existing measured cloud Linux worker | Current worker quota, bounded workload, selected source hash and result receipt |
| Linux package, service, filesystem or kernel behavior | Cloud Linux; WSL only when a working local Linux instance is specifically needed | Actual Linux environment and supported permissions |
| Linux containers or GPU work | A cloud environment already configured for that workload | Container/GPU access is observed, not inferred from a cloud label |
| Personal authentication | Provider-supported private storage on the relevant host | Correct account, refresh ownership, scope and recovery behavior |
| Cross-host transfer | Selected source/results with explicit byte/hash expectations | Keep credentials and raw private histories outside the transfer |

PowerShell can replace a dependency on WSL for many **workflows**: native Node/Python execution, Git operations, JSON processing, hashing, local administration and launching supported cloud tools. It cannot reproduce Linux kernel interfaces, systemd, Linux permissions or a Linux container merely by translating shell syntax. Test platform-specific behavior in its real executor.

The Windows hub therefore offers cloud Linux tasks as its primary Linux menu route. Its optional local Ubuntu entry is clearly separate. A copy installed inside a cloud worker can use that worker's actual Bash and portable PowerShell. The official Codex Cloud picker and task-list API are experimental routes; their task population may differ from managed app chats. A successful empty listing does not discover every cloud workspace or provide SSH access. Persistent remote-terminal integration is a later option under Q60.

## Local authority and cloud computation

The local bank holds reviewed source expectations, approvals, selected result receipts, rollback records and the operator's private storage. The cloud receives the bounded workload and only the data it needs. Results return with source bindings before local review or publication.

Human authorization, requested Full access, the configured sandbox, the measured Windows/Linux token and a successfully performed action are separate observations. The Windows Administrator hub requests normal UAC and its child processes inherit that token. Cloud permissions belong to the cloud executor and connected service. The menu cannot convert local Administrator membership into a cloud owner role or grant every Google account scope.

Normal desktop/CLI login, API credentials, Google OAuth scopes and cloud-runtime credentials also remain separate. Their use should be visible and supported. The hub captures no password, device-login code, OAuth cache or raw authentication output in its event records. It keeps the working sign-in while private-store migration is prepared and verified. Restoring a configuration file does not reverse server-side token rotation.

## WSL findings and recommendations

The current laptop has approximately 4 GB installed RAM. Recent Windows observations showed roughly half a gigabyte free; these are timestamped samples, not permanent available capacity. The actual WSL configuration at this stage was already **1 GB RAM, one CPU and 2 GB swap on D:**.

Two authorized startup attempts were performed. The first gave WSL a 120-second outer allowance and failed with `Wsl/Service/ERROR_TIMEOUT` after about 96 seconds. After a confirmed shutdown, the second kept the same memory/CPU/swap values and disabled optional GUI and nested-virtualization features for a console-only trial. It failed with the same service error after about 106 seconds. Neither reached the Linux readiness marker. The trial configuration was rolled back and shutdown confirmed. No distribution data or package cache was deleted.

The result does not identify RAM as the cause. The service returned its own error before the outer deadline; increasing the outer timer again would not, by itself, diagnose that failure. Package cleanup also cannot be assumed to repair a failure before a shell starts.

Recommendations for a later, separately started repair investigation:

1. Keep cloud Linux primary and local WSL stopped when not needed.
2. Capture supported WSL startup diagnostics and distinguish service, VM, distribution-init and shell failures.
3. Check system resource headroom before a controlled 1.5 GB trial; do not increase the cap merely because more sounds faster. A cap is not a reservation, and swap is not physical RAM.
4. Use console-only settings when Linux GUI support is unnecessary, but retain a rollback and check that the settings actually took effect.
5. If a working shell is obtained, inspect concrete startup services and cache sizes before changing them. Keep unique data and the verified distribution backup.
6. Compare one change at a time. The two existing attempts are historical observations, not a license for a restart loop.

Microsoft documents the distinction between [VM-wide and distribution-specific configuration](https://learn.microsoft.com/en-us/windows/wsl/wsl-config), including the need for a stopped subsystem before changes apply. Its [troubleshooting guide](https://learn.microsoft.com/en-us/windows/wsl/troubleshooting) is the starting point for targeted startup evidence.

## Resource and process policy

The menu performs no automatic WSL start, periodic probe, model invocation or background-service launch. Small local checks run serially. Larger test batches belong in a measured cloud worker. OS-visible memory is not proof of an executor's cgroup quota or allocatable capacity; obtain current worker limits before a large job.

Requested timeouts are timer deadlines, not real-time scheduling guarantees during host stalls. The hub records elapsed time and distinguishes an immediate child closing from unconfirmed cleanup or arbitrary descendants. An unknown result is reconciled before another action; it is never automatically treated as a failure requiring replay.

Keep the existing app launcher and the new hub shortcut separate, as chosen in Q59. The Windows global context configuration remains unchanged; Q63 removes forced context/compaction values from the portable hub's invocation arguments. Fast is requested through the observed adapter tier, with actual service behavior separately verified.

## Research boundary

This launcher stage precedes run (3) x2. The saved x1 review remains unfinished. The hub is a tool for that future work; installing it does not complete the fifty-project portfolio, recover missing original CLI histories or establish a scientific theory. Read `RESEARCH-BASELINE.md` for the bounded research register and Sentinel preparation.
