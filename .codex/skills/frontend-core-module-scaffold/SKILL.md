---
name: frontend-core-module-scaffold
description: Scaffold frontend core module files (api/hooks/types/index) with consistent React Query patterns.
license: MIT
compatibility: Requires Next.js/TypeScript project context.
metadata:
  author: deerflow
  version: "1.0"
---

按前端 `core` 目录模式快速生成可维护模块。

## 使用场景
- 新增一个前端数据域模块。
- 需要对齐 `api.ts` / `hooks.ts` / `types.ts` / `index.ts` 结构。

## 输入
- 模块名。
- API 路径与数据类型。
- 查询与变更行为。

## 执行步骤
1. 创建模块目录与 `types.ts`。
2. 编写 `api.ts`（`fetch` + `response.ok` 错误处理）。
3. 编写 `hooks.ts`（`useQuery/useMutation` + `invalidateQueries`）。
4. 编写 `index.ts` 聚合导出。
5. 对齐 `queryKey` 命名与依赖注入模式。
6. 给出组件层使用示例。

## 输出
- 完整 core 模块脚手架。
- 可复用 query key 与 hooks。
- 最小手工验证说明。

## Guardrails
- 避免 `any`，优先显式类型。
- 不破坏现有模块出口。
- API 错误信息必须可读。
