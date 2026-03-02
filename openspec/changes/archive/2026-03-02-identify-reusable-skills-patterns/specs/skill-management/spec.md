## ADDED Requirements

### Requirement: Codex Skill Namespace Governance
项目 SHALL 定义清晰的命名空间边界，区分 Codex Skills 与 runtime skills，避免位置与归属歧义。

#### Scenario: Classify skill ownership
- **WHEN** 提出一个新的可复用工作流技能
- **THEN** 维护者可明确判断该技能属于 `.codex/skills` 或 `skills/public|custom`
- **AND** 放置规则被文档化并纳入技能管理规范

### Requirement: Skill Metadata Quality Gate
技能管理流程 SHALL 包含验证规则，确保每个技能保持机器可读 frontmatter 与必填元数据键。

#### Scenario: Validate skill metadata before adoption
- **WHEN** 创建或更新技能
- **THEN** 对 frontmatter 的可解析性与必填字段进行校验
- **AND** 不合格的技能定义在修复前不得进入 rollout
