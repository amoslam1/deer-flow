# Output Contract

The skill returns a structured review with these fields:

- `target`: resolved target metadata (`hash`, `canonical_id`, `path`, `type`)
- `context_summary`: concise context text
- `dependency_paths`: list of `Ahash->Bhash` paths
- `feasibility`: `high|medium|low`
- `issues`: risk and gap list
- `next_steps`: actionable recommended steps
- `rollback`: rollback guidance

Minimum guarantees:

1. If target is resolvable, return at least one dependency path when available.
2. Feasibility must include evidence from dependency paths or missing-data conditions.
3. Do not suggest direct implementation changes unless user asks for implementation.
