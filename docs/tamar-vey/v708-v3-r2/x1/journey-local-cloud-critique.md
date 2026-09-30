# Journey Local/Cloud Nexus critique

The Journey v41-v44 texts preserve a valuable architectural intuition: keep a
durable local vault and use isolated cloud compute for bounded workloads. They
also anticipate provider-spend controls, manifest reconciliation, a claims truth
board, and explicit local/cloud boundaries.

This remaster adopts those ideas only after correction:

1. The local bank is canonical custody, not a “sacred memory” or identity proof.
2. Cloud compute is execution capacity, not a mind or consciousness.
3. A sandbox reduces some risks but does not guarantee safety, correctness,
   privacy, or authority.
4. Mirroring a phone does not by itself move all rendering or computation to the
   phone; measurements would be required.
5. Kubernetes, Vercel, Neon, Cloudflare, OCI, and other providers are optional
   implementation candidates, not mandatory components or free-cost facts.
6. A passing CI suite cannot by itself gate all API traffic or prove that a
   system “never hallucinates.”
7. The current managed Codex cloud environment is the smallest useful cloud
   substrate. New clusters, tunnels, public deployments, databases, and provider
   accounts remain outside this remaster.

The resulting design is a capsule exchange, not a monolithic operating system:
local export, cloud execution, cloud receipt, local quarantine, and explicit
promotion. Every boundary is content-addressed and every missing authority stays
visible.
