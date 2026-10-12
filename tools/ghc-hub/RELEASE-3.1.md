# Nexus Hub 3.1

This maintenance release lets the existing tunnel launcher use an operator-selected local key file. Set `runtimeApiKeyFile` in the existing private `hub28.json` configuration to an absolute local filename. The launcher passes a file reference to the tunnel client and never reads or prints the secret. Omission retains the previous path; an invalid explicit value is rejected. The file must contain the raw API key expected by the tunnel client, rather than a dotenv assignment.

The same private configuration accepts `guiMinimumFreeMemoryMiB`. Its default remains 512; the current operator-approved setting is 200. `nexus.desktop.status` now reports this guard, measured free memory, and resource admission separately from GUI verification. Capacity cannot enable desktop input. Full desktop control remains unverified and unexposed until a supported interactive backend is available and passes validation.

The 26-tool catalogue, reviewed file roots and exact local command approval remain in place. An OpenAI project key authenticates the tunnel client; it does not grant Windows elevation or access to other users, devices or chats. Model API acceptance, tunnel readiness and effective client tool discovery require separate checks.

Runtime publication and installation are recorded in the phase checkpoint. An updated source or cached plugin by itself is not evidence of a running tunnel or a refreshed conversation catalogue.
