## ADDED Requirements

### Requirement: OpenSpec Skill Documents SHALL Be Available in Chinese
The repository SHALL provide Chinese body content for all OpenSpec-related `SKILL.md` files under `.codex/skills`.

#### Scenario: Translate all target OpenSpec skills
- **WHEN** maintainers complete this change
- **THEN** each OpenSpec-related `.codex/skills/*/SKILL.md` contains Chinese workflow instructions
- **AND** users can follow the same propose/apply/verify/archive flow semantics in Chinese

### Requirement: Skill Frontmatter MUST Remain Machine-Readable
Localization MUST preserve valid YAML frontmatter and required metadata keys for each translated skill file.

#### Scenario: Validate translated frontmatter
- **WHEN** translated skill files are checked after editing
- **THEN** frontmatter remains parseable as YAML
- **AND** required keys such as `name`, `description`, `license`, `compatibility`, and `metadata` remain present
