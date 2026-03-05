## Why

缺少统一模块标识，跨模块定位慢。新增 16 位 hash 与父子依赖链，支持按 hash 还原上下文。

## What Changes

- 输出技术/架构模块清单：hash + 依赖。
- 输出服务/调度/通用模块清单：`Ahash->Bhash->Chash`。

## Capabilities

### New Capabilities
- `project-architecture-hash-index`: 架构 hash 索引。
- `service-module-hash-chain`: 服务 hash 链路。

### Modified Capabilities
- None.

## Non-goals

- 不改业务逻辑与 API 行为。

## Dependencies

- 依赖现有目录/入口稳定与 OpenSpec 目录可写。

## 可复用 Skills

- `openspec-propose`：复用。
- `openspec-new-change`：初始化已用，不复用。

## Impact

仅新增文档规范，不改运行时。
