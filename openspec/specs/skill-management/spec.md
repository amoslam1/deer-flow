## Purpose
定义 DeerFlow 在 public/custom 技能目录上的发现、管理与安全安装基线行为，确保技能治理过程具备一致性、可审计性与可扩展性。

## Requirements

### Requirement: Skill Discovery and State
系统 SHALL 从 `public` 与 `custom` 两类目录发现技能，并在加载时应用持久化的启用/禁用状态。

#### Scenario: Load all skills
- **WHEN** skills API 加载可用技能
- **THEN** 扫描两个分类下的 `SKILL.md`
- **AND** 返回解析后的元数据与分类信息

#### Scenario: Apply persisted enabled state
- **WHEN** 某技能在扩展配置中存在持久化状态
- **THEN** 返回的技能状态与持久化 enabled/disabled 值一致

### Requirement: Safe Skill Installation
系统 SHALL 在安装到 custom skills 目录前校验技能包元数据。

#### Scenario: Install valid skill package
- **WHEN** 用户安装包含必填 frontmatter 的有效 `.skill` 包
- **THEN** 系统解压并将技能安装到 custom skills 下
- **AND** 安装响应包含已安装技能名称

#### Scenario: Reject invalid skill package
- **WHEN** 技能包 frontmatter 包含不支持键或无效 name 格式
- **THEN** 安装被校验错误拒绝
- **AND** custom skills 下不留下部分安装残留

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
