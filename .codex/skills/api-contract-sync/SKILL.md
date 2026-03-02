---
name: api-contract-sync
description: Synchronize backend gateway API contracts with frontend core API and hooks usage.
license: MIT
compatibility: Requires access to backend/src/gateway and frontend/src/core.
metadata:
  author: deerflow
  version: "1.0"
---

同步后端 Gateway 契约与前端调用契约。

## 使用场景
- 后端路由、字段、响应结构发生变更。
- 前端出现 404/字段缺失/解析错误。

## 输入
- 变更的后端 router 列表。
- 关联前端 core 模块列表。

## 执行步骤
1. 提取后端变更：路径、方法、字段、错误码。
2. 对比前端 `core/*/api.ts` 与 `types.ts`。
3. 标记 breaking/non-breaking 差异。
4. 更新前端 API 与 hooks 逻辑。
5. 输出回归清单（关键接口、关键页面）。

## 输出
- 契约差异报告。
- 前端同步补丁。
- 回归测试建议。

## Guardrails
- 不假设字段兼容；以代码和文档为准。
- 每个 breaking change 必须给迁移说明。
- 保持改动范围只覆盖相关模块。
