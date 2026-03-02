## Why（背景）

当前项目在开发与协作中存在大量重复动作（环境准备、服务联调、接口模块增量开发、OpenSpec 流程执行、技能文档维护）。这些动作尚未沉淀为统一可复用 Skills，导致新人上手成本高、交付质量依赖个人经验。

## What Changes（变更内容）

- 基于现有代码与文档，梳理重复出现的开发流程、规范与实现模式。
- 提炼可复用 Skill 候选清单，给出触发条件、输入输出、边界和优先级。
- 明确哪些候选属于 Codex 侧技能（`.codex/skills`），哪些属于 DeerFlow 运行时技能（`skills/public|custom`）。
- 形成可落地的技能化路线图（先做高频高收益，再做专项技能）。

## Capabilities（能力变更）

### New Capabilities（新增能力）
- `reusable-skills-pattern-catalog`: 建立项目重复流程与模式到 Skills 的映射目录，支持按优先级落地。

### Modified Capabilities（变更能力）
- `skill-management`: 在现有技能管理能力基础上补充“可复用技能抽象与治理”流程约束。

## Impact（影响）

- `openspec/changes/identify-reusable-skills-patterns/*`：新增 proposal/specs/design/tasks 工件。
- 影响范围聚焦文档与流程设计，不改运行时代码。
- 后续实施阶段预计触达 `.codex/skills`（Codex 技能）与 `skills/*`（DeerFlow 运行时技能）目录。

## Non-goals（非目标）

- 本阶段不直接实现全部新 Skills。
- 不重构 backend/frontend 业务代码。
- 不变更 OpenSpec CLI 与 schema 引擎行为。

## Dependencies（依赖）

- 现有项目文档（README、CONTRIBUTING、LOCAL_DEBUG_COMMANDS 等）与目录结构准确可读。
- 现有 Skills 元数据格式（SKILL frontmatter）保持兼容。
- OpenSpec 流程可用（用于后续 specs/design/tasks 与实施闭环）。
