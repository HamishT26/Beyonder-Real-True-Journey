# v470 THOS v1 x1 Plugin, MCP, And Skill Boundary Rules

Classification: `evidence`

Plugins, MCP connectors, and skills are capability surfaces. They are not consent, not proof, not publication authority, and not a shortcut around project safety rules.

## Boundary Table

| Surface | Authority ceiling | Safe posture | Approval-required posture |
| --- | --- | --- | --- |
| Skills | Workflow guidance | Read instructions, reuse templates, apply checks | Install, edit, or run mutation-capable helpers |
| Plugins | Tool capability | Read-only inspection and safe local verification | External writes, credentials, account settings |
| MCP connectors | Connector protocol | Read allowed resources and record safe summaries | Database, cloud, config, or secret changes |
| Browser and Computer Use | Interactive UI control | View and inspect visible state | Submit, buy, delete, change settings, edit automation |
| GitHub and Drive cloud surfaces | External service surface | Read when specifically needed and safe | Create, edit, delete, share, merge, or protect |

## Publication Requirements

- Label every source as local evidence, external context, advisory, blocker, or open gap.
- Record mutation-capable surfaces as blocked unless there is separate explicit approval.
- Include `no_gmut_validation_import` in THOS manifests.
- Do not stage raw connector output.
- Do not treat sibling advisory text as independent receipt material.

## Practical Rule

If a tool can change something outside the curated local phase artifact set, THOS treats it as approval-required by default.
