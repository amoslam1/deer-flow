# codex-skill-localization Specification

## Purpose
定义 OpenSpec 相关 Codex Skills 的中文化基线，确保中文协作场景下流程语义一致、元数据可机器解析。

## Requirements

### Requirement: OpenSpec Skill Documents SHALL Be Available in Chinese
仓库 SHALL 为 `.codex/skills` 下所有 OpenSpec 相关 `SKILL.md` 提供中文正文内容。

#### Scenario: Translate all target OpenSpec skills
- **WHEN** 维护者完成该变更
- **THEN** 每个 OpenSpec 相关 `.codex/skills/*/SKILL.md` 均包含中文流程说明
- **AND** 用户可用中文遵循 propose/apply/verify/archive 的同等语义流程

### Requirement: Skill Frontmatter MUST Remain Machine-Readable
本地化 MUST 保持每个翻译后技能文件的 YAML frontmatter 与必填元数据键有效。

#### Scenario: Validate translated frontmatter
- **WHEN** 翻译后的技能文件在编辑后被检查
- **THEN** frontmatter 仍可被 YAML 正确解析
- **AND** `name`、`description`、`license`、`compatibility`、`metadata` 等必填键保持存在
