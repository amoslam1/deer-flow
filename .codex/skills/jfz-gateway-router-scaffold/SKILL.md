---
name: gateway-router-scaffold
description: Scaffold FastAPI gateway routers following DeerFlow response model, docs, and error handling conventions.
license: MIT
compatibility: Requires Python/FastAPI codebase context.
metadata:
  author: deerflow
  version: "1.0"
---

按 DeerFlow 规范生成 Gateway Router 脚手架。

## 使用场景
- 新增 `/api/*` 资源端点。
- 统一响应模型、文档描述和错误处理风格。

## 输入
- 资源名、路由前缀、方法列表。
- 请求/响应字段定义。

## 执行步骤
1. 在 `backend/src/gateway/routers/` 新建模块。
2. 定义 APIRouter、Pydantic request/response models。
3. 生成端点函数与异常分支（HTTPException）。
4. 补充 `summary/description` 与 docstring。
5. 在 `gateway/app.py` 注册 router。
6. 输出最小 curl 验证命令。

## 输出
- 可运行的 router 模块。
- app 注册改动。
- 验证命令与预期响应。

## Guardrails
- 遵循已有 `prefix="/api"` 与 tags 约定。
- 响应模型必须显式定义，避免裸 dict。
- 不引入与目标资源无关的重构。
