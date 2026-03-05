## Purpose
定义 DeerFlow 服务、后台调度与通用模块的 hash 链路规范，支持按代码位置或 hash 聚合上下文并评估后续实施方案可行性。

## Requirements

### Requirement: Service and backend job coverage
系统 SHALL 覆盖运行时服务、后台调度服务与相关通用模块，并建立统一索引记录。

#### Scenario: Build service scope
- **WHEN** 执行服务扫描
- **THEN** 输出覆盖 gateway、langgraph、frontend、nginx、可选 provisioner 与后台调度/通用模块的记录

### Requirement: Service module hash assignment
每个服务或通用模块记录 MUST 使用 `sha256(canonical_id)[:16]` 生成确定性 16 位 hash。

#### Scenario: Service hash generation
- **WHEN** 扫描服务或通用模块 canonical ID
- **THEN** 记录中生成且仅生成一个对应 16 位 hash

### Requirement: Dependency chain output
系统 SHALL 以父级到子级顺序输出显式依赖链，格式为 `Ahash->Bhash->Chash`。

#### Scenario: Multi-hop dependency chain
- **WHEN** 存在多跳依赖关系
- **THEN** 输出至少一条三节点以上 hash 链并保持父子方向一致

### Requirement: Reverse index for hash-driven context retrieval
系统 MUST 产出以 hash 为键的 reverse index，以支持快速反查上下游依赖上下文。

#### Scenario: Retrieve service context by hash
- **WHEN** 查询已知 hash
- **THEN** 返回命中记录与其 upstream/downstream 链接信息

### Requirement: Code-location context and plan evaluation output
系统 SHALL 支持输入代码位置或 hash 后自动总结上下文，并输出当前方案合理性评估与可执行建议。

#### Scenario: Evaluate approach from a code location
- **WHEN** 输入文件路径行区间或可解析的 location hash
- **THEN** 输出上下文摘要、评估维度与至少一个推荐实施方案
