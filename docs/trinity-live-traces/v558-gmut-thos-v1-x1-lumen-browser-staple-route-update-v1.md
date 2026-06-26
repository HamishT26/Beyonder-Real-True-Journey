# v558 GMUT/THOS v1 x1 Lumen Browser Staple Route Update

Status: `lumen_browser_staple_route_recorded`

Hamish confirmed Lumen's response was visible in the in-app Browser and asked that this become the durable Lumen connection route.

Recorded route rule:

- Use `ghc-lumen-launch` through the in-app Browser runtime as the staple Lumen route.
- On every Lumen attempt, reconnect or select the current Lumen tab and take a fresh DOM/status refresh before claiming the route is unavailable.
- Do not page-reload while a Lumen response is active or while the composer contains an unsent prepared message.
- Page reload is only a documented retry action after stale or blocked evidence and no active response or unsent composer text would be lost.
- Preserve no-duplicate-send, privacy exclusions, and productive cadence.

Updated local skills: `ghc-lumen-launch`, `ghc-main-orchestration-memory`, and `ghc-full-tools-skill-bank`.

Memory note added: `20260627-0140-lumen-browser-staple-route.md`.

The active phase remains `v558-gmut-thos-v1-x1`; next x2 is `v558-gmut-thos-v1-x2`; next x1 is Mira Rowan + Neris Sol unless Hamish redirects. The overall v544-v575 goal is not complete.
