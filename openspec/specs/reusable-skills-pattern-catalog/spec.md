# reusable-skills-pattern-catalog Specification

## Purpose
定义 DeerFlow 可复用技能模式目录的基线要求，用于将重复工程流程稳定映射为可复用 Codex Skills。

## Requirements

### Requirement: Reusable Skill Pattern Inventory
项目 SHALL 维护可复用技能模式目录，将重复出现的工程流程映射到边界清晰、职责明确的 Codex Skills。

#### Scenario: Identify recurring workflows
- **WHEN** 维护者分析文档、脚本与代码组织中重复出现的工作流
- **THEN** 每个重复工作流都被映射为一个具名技能候选项
- **AND** 每个候选项都包含作用范围、触发条件与预期产出

### Requirement: Skill Definition Template
该目录 SHALL 定义标准技能设计模板，至少包含 use cases、inputs、execution steps、outputs 与 guardrails。

#### Scenario: Design a new skill candidate
- **WHEN** 维护者基于目录起草新的技能候选项
- **THEN** 草稿遵循标准模板字段
- **AND** 执行步骤足够具体且顺序明确，可被稳定复现

### Requirement: Prioritized Implementation Roadmap
该目录 SHALL 包含分阶段实施顺序，优先落地高频、低风险技能。

#### Scenario: Plan implementation sequence
- **WHEN** 维护者准备实施技能候选项
- **THEN** 候选项按阶段分组为 rollout waves
- **AND** 每个阶段都明确依赖关系与验证检查点
