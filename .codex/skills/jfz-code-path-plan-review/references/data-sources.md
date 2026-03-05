# Data Sources

`jfz-code-path-plan-review` reads these files as the single source of truth:

1. `docs/design/project.md`
2. `docs/design/component.md`
3. `artifacts/hash-index.json`
4. `artifacts/hash-chains.json`

Load order:

1. Resolve target via `hash-index.json`.
2. Expand upstream/downstream via `hash-chains.json`.
3. Explain architecture context with `project.md`.
4. Explain API/module IO context with `component.md`.
