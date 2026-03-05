---
name: local-debug-orchestrator
description: Orchestrate DeerFlow local multi-service debug startup, health checks, and log collection.
license: MIT
compatibility: Requires uv, pnpm, nginx and project scripts.
metadata:
  author: deerflow
  version: "1.0"
---

统一编排 DeerFlow 本地联调（LangGraph/Gateway/Frontend/Nginx）。

## 使用场景
- 需要完整端到端联调。
- 需要结构化日志归档和问题排查。

## 输入
- 可选：日志级别（默认 DEBUG）。
- 可选：是否启用 Nginx 统一入口。

## 执行步骤
1. 清理残留进程与端口占用（langgraph、uvicorn、next、nginx）。
2. 按顺序启动：LangGraph -> Gateway -> Frontend -> Nginx。
3. 通过 `scripts/tee_daily_log.py` 将日志归档到 `logs/archive/YYYY-MM-DD/`。
4. 执行健康检查（2024/8001/2026）。
5. 输出服务状态、日志路径、停止命令。

## 输出
- 各服务启动结果。
- 统一访问入口与 API 入口。
- 日志文件与排障建议。

## Guardrails
- 任一核心服务启动失败时立即停止并输出最后日志。
- 不隐藏失败；必须给出可复现命令。
- 不跳过健康检查。
