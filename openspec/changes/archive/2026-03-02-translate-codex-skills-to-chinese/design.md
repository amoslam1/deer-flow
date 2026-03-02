## Context

本变更是文档本地化任务，覆盖 `.codex/skills` 下 OpenSpec 工作流技能。目标是让中文团队在 proposal/apply/archive 等阶段按同一语义执行，避免“字面翻译正确但流程含义偏差”。

## Goals / Non-Goals

**Goals:**
- OpenSpec 相关 SKILL 文档正文统一翻译为中文。
- frontmatter 与元数据保持稳定，确保可解析与可检索。
- 对术语给出统一口径，减少多文件描述不一致。

**Non-Goals:**
- 不改 DeerFlow 产品功能与运行时代码。
- 不改 OpenSpec schema 或 CLI 行为。
- 不做自动化翻译流水线建设。

## Decisions

- 决策 1：frontmatter 保持英文键与结构不变，仅翻译正文。
  - 备选方案：frontmatter 也翻译。
  - 放弃原因：可能影响工具兼容和元数据解析。

- 决策 2：命令示例保持原命令，说明文字中文化。
  - 备选方案：命令与说明全部中文化表达。
  - 放弃原因：命令本身不可本地化，易引入误导。

- 决策 3：采用“逐文件翻译 + 统一术语审校 + frontmatter 校验”的顺序。
  - 备选方案：一次性批量改完再回头检查。
  - 放弃原因：回溯成本高，定位问题困难。

## Risks / Trade-offs

- [风险] 翻译后语义偏离原流程约束 → Mitigation: 对关键 guardrails/steps 逐段对照原文审校。
- [风险] frontmatter 意外破坏导致工具失效 → Mitigation: 增加 YAML/frontmatter 解析校验步骤。
- [风险] 术语在 11 个文件中不一致 → Mitigation: 先定义术语映射，再逐文件统一替换。

## Migration Plan

1. 在变更分支内更新目标 `SKILL.md` 正文。
2. 执行 frontmatter 解析检查与 `openspec validate`。
3. 验证通过后进入 apply 阶段实施并勾选任务。
4. 如需回滚，按文件粒度恢复文档改动。

## Open Questions

- `description` 字段是否需要同步改中文，或保持英文用于触发稳定性？
- 是否需要保留中英文对照版本（当前默认只保留中文正文）？
