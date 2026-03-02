## Why

`.codex/skills` 下 OpenSpec 相关 SKILL 文档主要为英文，团队中文协作时理解成本高、执行口径不一致，容易在 propose/apply/archive 流程中出现误解。

## What Changes

- 将 `.codex/skills` 中 OpenSpec 相关 `SKILL.md` 正文翻译为中文。
- 保留 frontmatter 结构和关键字段，确保工具解析不受影响。
- 统一术语翻译口径（change/spec/tasks/apply/archive 等）。
- 增加最小校验步骤，确认翻译后文档仍可被 YAML/frontmatter 解析。

## Capabilities

### New Capabilities
- `codex-skill-localization`: 为 Codex OpenSpec 技能文档提供中文化规范与一致化流程。

### Modified Capabilities
- None.

## Impact

- `.codex/skills/openspec-*/SKILL.md`：文档正文更新为中文。
- `openspec/changes/translate-codex-skills-to-chinese/*`：新增 proposal/specs/design/tasks。
- 无运行时代码、API、模型或沙箱逻辑改动。

## Non-goals

- 不修改 DeerFlow 运行时功能（backend/frontend/sandbox）。
- 不修改 OpenSpec CLI 或 schema 实现。
- 不引入自动翻译工具链或新增构建流程。

## Dependencies

- `openspec` CLI（用于流程与校验）。
- 现有 `.codex/skills` 文档结构保持稳定。
