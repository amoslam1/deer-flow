## Purpose
定义 DeerFlow 项目级技术与架构模块的 hash 索引基线，确保模块身份可稳定追踪，并能通过依赖链回溯上下文。

## Requirements

### Requirement: Architecture module inventory
系统 SHALL 扫描 backend、frontend、skills 与运行入口，生成每个架构模块的唯一 canonical record。

#### Scenario: Build architecture inventory
- **WHEN** 触发架构扫描
- **THEN** 输出覆盖目标域的模块记录
- **AND** 每条记录包含唯一 canonical ID

### Requirement: Deterministic 16-character hash generation
每个模块记录 MUST 使用 `sha256(canonical_id)` 截断 16 位小写十六进制生成稳定 hash。

#### Scenario: Repeatable hash generation
- **WHEN** 同一 canonical ID 在不同扫描轮次中被重复处理
- **THEN** 生成的 16 位 hash 保持一致

### Requirement: Parent-to-child dependency annotation
每个架构模块记录 SHALL 声明父级到子级的直接依赖，并同时提供名称链路与 hash 链路引用。

#### Scenario: Dependency link emission
- **WHEN** 模块依赖其他子模块
- **THEN** 输出包含 `moduleA->moduleB` 与 `hashA->hashB` 两种形式

### Requirement: Hash lookup context bundle
索引 MUST 支持通过 hash 反查完整上下文，包括 canonical ID、domain、parents、children 与链路片段。

#### Scenario: Resolve module by hash
- **WHEN** 输入有效模块 hash
- **THEN** 返回对应模块上下文与关联依赖链信息
