# DeerFlow 本地 Debug 启动命令

本文整理本地调试 DeerFlow 的命令集（不依赖 Docker），并按日期归档日志。

默认前提：以下命令都在项目根目录执行（`deer-flow/`）。

## 推荐：后端单进程调试脚本（`backend/debug.py`）

`backend/debug.py` 适合直接打断点调试 agent 逻辑（输入问题 -> 观察工具调用/返回），不需要先启动 LangGraph/Gateway/Frontend。

```bash
mkdir -p logs/archive
cd backend
uv run python debug.py 2>&1 | python3 ../scripts/tee_daily_log.py backend-debug --log-root ../logs
```

说明：

- 该脚本是交互式调试（终端输入问题，`quit`/`exit` 退出）。
- 固定 thread：`debug-thread-001`，便于复现。
- 如 `uv` 不在 PATH，可改用 `~/.local/bin/uv run python debug.py`。
- 如需改模型/plan mode，可直接编辑 `backend/debug.py` 中的 `config`。

## 全链路联调（前端 + 网关 + LangGraph）

如需验证 2026 入口、上传接口、前端页面联动，使用下面多终端命令。

## 日志格式说明

- 项目当前不是单一日志格式：
  - LangGraph：结构化键值风格（包含 `thread_id`、`run_id` 等上下文）
  - Gateway：Python logging 文本格式
  - Nginx：access/error 日志格式
- 因此不同服务日志长相不一致，属于预期行为。

## 日志归档规则

- 每天日志写入：`logs/archive/YYYY-MM-DD/*.log`
- 同时维护最新软链：`logs/backend-debug.log`、`logs/langgraph.log`、`logs/gateway.log`、`logs/frontend.log`、`logs/nginx.log`
- 支持跨天自动切换到新日期日志文件（无需手动改文件名）

## 终端 1：LangGraph

```bash
mkdir -p logs/archive
cd backend
LOG_LEVEL=DEBUG NO_COLOR=1 uv run langgraph dev --server-log-level debug --no-browser --allow-blocking --no-reload 2>&1 | python3 ../scripts/tee_daily_log.py langgraph --log-root ../logs
```

## 终端 2：Gateway

```bash
mkdir -p logs/archive
cd backend
uv run uvicorn src.gateway.app:app --host 0.0.0.0 --port 8001 --reload --log-level debug 2>&1 | python3 ../scripts/tee_daily_log.py gateway --log-root ../logs
```

## 终端 3：Frontend（可选）

```bash
mkdir -p logs/archive
cd frontend
pnpm run dev 2>&1 | python3 ../scripts/tee_daily_log.py frontend --log-root ../logs
```

## 终端 4（可选）：统一入口 2026（本地 Nginx）

```bash
mkdir -p logs/archive
nginx -g 'daemon off;' -c docker/nginx/nginx.local.conf -p "$(pwd)" 2>&1 | python3 scripts/tee_daily_log.py nginx --log-root logs
```

## 快速校验

```bash
curl -I http://localhost:2024/docs
curl -I http://localhost:8001/docs
curl -I http://localhost:2026
```

## 查看日志

```bash
tail -f logs/backend-debug.log
tail -f logs/langgraph.log
tail -f logs/gateway.log
tail -f logs/frontend.log
tail -f logs/nginx.log
```

## 按日期查看归档日志

```bash
ls -lah logs/archive
ls -lah logs/archive/$(date +%F)
tail -f logs/archive/$(date +%F)/backend-debug.log
tail -f logs/archive/$(date +%F)/langgraph.log
```

## 常见问题排查

### 1）终端 4（Nginx）日志不在 `logs/archive`

- 必须使用本文档里的终端 4 命令（包含 `python3 scripts/tee_daily_log.py nginx --log-root logs`）。
- 不要使用旧命令（仅 `nginx ...`），旧命令不会归档。
- 验证：

```bash
ls -lah logs/archive/$(date +%F)/nginx.log
readlink logs/nginx.log
```

### 2）文件存在但没有内容

- 若没有请求流量，`nginx.log` 可能为空，这是正常现象。
- 执行一次请求后再看：

```bash
curl -I http://localhost:2026
tail -f logs/archive/$(date +%F)/nginx.log
```
