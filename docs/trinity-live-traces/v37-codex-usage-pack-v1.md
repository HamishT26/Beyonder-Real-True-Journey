# V37 Codex Usage Pack

- Large-codebase understanding: lead with `Codex local`; use `Codex cloud environments` for bounded parallel repo jobs when GitHub-backed isolation helps.
- PR and review workflows: use `Codex cloud environments` for reproducible GitHub-backed review lanes, with `Codex local` as the decision and integration surface.
- Scored improvement loops: use `Codex cloud environments` for isolated reruns and `Codex local` for synthesis and follow-through.
- API upgrade work: use `Codex local` as the primary repo-wide implementation surface, with `Kai` available for bounded CLI refresh loops.
- Visual or UI implementation: use `Codex local` for the main implementation lane and keep `Vertex` out of UI ownership except for bounded cloud proof tasks.
- Data and reporting tasks: use `Codex local` for repo-backed reporting and `Kai` for bounded headless command execution where JSON output helps.
