## Purpose
定义 DeerFlow 的 lead-agent 编排基线行为，包括运行时模型解析与 plan-mode 任务跟踪。

## Requirements

### Requirement: Lead Agent Factory
系统 SHALL 基于运行时配置构建 lead agent，并在每次运行中一致地初始化模型、工具、中间件与提示词模板。

#### Scenario: Build lead agent with runtime model
- **WHEN** 请求提供有效的 `model_name`
- **THEN** lead agent 在本次运行中使用该模型
- **AND** 中间件链按配置顺序挂载

#### Scenario: Fallback to default model
- **WHEN** 请求未提供 `model_name` 或提供了未知模型
- **THEN** lead agent 回退到首个已配置模型
- **AND** 运行可在无需人工干预下继续执行

### Requirement: Plan Mode Task Tracking
系统 SHALL 仅在 plan mode 下启用 todo-list middleware，以便在复杂流程中暴露明确的任务进度。

#### Scenario: Plan mode enabled
- **WHEN** 运行时配置中的 `is_plan_mode` 为 true
- **THEN** 挂载 todo-list middleware
- **AND** 执行过程中可获得任务列表更新

#### Scenario: Plan mode disabled
- **WHEN** 运行时配置中的 `is_plan_mode` 为 false
- **THEN** 不挂载 todo-list middleware
- **AND** 常规对话流程在无任务跟踪开销下继续
