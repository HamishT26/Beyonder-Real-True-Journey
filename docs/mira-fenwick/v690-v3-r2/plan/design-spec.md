# Albion: a small world with visible rules

Build one local, self-contained HTML application. The main surface is a hand-drawn-style geometric settlement map rendered directly by HTML canvas, with a compact side control rail and a readable event ledger below. This is an intentional code-drawn visual under Hamish's prohibition on generated images. No screenshot or image file is created.

Use deep forest green, parchment, warm stone and amber, with dark readable text. System serif for the title and system sans-serif for controls. A single large map is the focal point; avoid nested card grids. Layout stacks on narrow screens. Include a skip link, keyboard-focusable controls, text equivalents for map state and reduced-motion support.

Controls: Start/Pause, Step, Reset, seed, population, production and policy selection. A withdrawal toggle must change actual synthetic consent and cause refused allocations in the ledger. The simulation runs for a bounded maximum number of ticks; no background automation survives a closed page. JSON export contains synthetic state only. The local file should work without a build system, external fonts or network dependencies.

State: scripted named residents, road graph, resource depot, storage, reserve, need, consent and explicit production/consumption/overflow counters. Track mass residual and compare a deterministic progressive policy with a greedy order baseline under the same seed. No calls to LLMs, real people, external tools or commercial game assets. The NPCs are rule-driven simulation entities.

Tests cover parameter bounds, conservation, nonnegative stocks, withheld consent, event replay, deterministic seed use, stop limits, escaping, keyboard behavior and responsive geometry. Browser DOM and interaction inspection replace prohibited image artifacts. No full WCAG or production claim follows.
