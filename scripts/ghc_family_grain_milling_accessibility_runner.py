"""Render a static, script-free synthetic milling evidence table."""

from __future__ import annotations

import html
from collections.abc import Iterable, Mapping


def render(rows: Iterable[Mapping[str, object]]) -> str:
    material = list(rows)
    body = "\n".join(
        "<tr><th scope=\"row\">{}</th><td>{}</td><td>{}</td></tr>".format(
            html.escape(str(row["proposal_id"])),
            html.escape(str(row["outcome"])),
            html.escape(str(row["boundary"])),
        )
        for row in material
    )
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Lyren v670-v1 synthetic milling evidence</title></head>
<body>
<a href="#main">Skip to evidence</a>
<header><h1>Lyren v670-v1 synthetic milling evidence</h1></header>
<main id="main">
<p>This static table is structural same-owner evidence only. It is not a real milling, food-safety, professional, legal, cultural, accessibility-complete, or Stage 20 result.</p>
<table><caption>Forty synthetic proposal outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Boundary</th></tr></thead><tbody>
{body}
</tbody></table>
</main>
</body>
</html>
"""
