# DeerFlow PyCharm 启动指南

本文说明如何在 PyCharm 中从源码启动 DeerFlow。

## 适用范围

- 项目根目录：`deer-flow/`
- 目标模式：本地开发
- 提供两种启动方式：
  - 单命令启动（最快）：`make dev`
  - 组合配置启动（便于调试）：LangGraph + Gateway + Frontend

## 1. 前置准备

在项目根目录执行：

```bash
make check
```

预期依赖：

- Node.js 22+
- pnpm
- uv
- nginx

安装依赖：

```bash
make install
```

## 2. 基础配置

首次启动先初始化配置文件：

```bash
cp config.example.yaml config.yaml
cp .env.example .env
```

然后编辑：

- `.env`：API Key（LLM 等）
- `config.yaml`：模型与 sandbox 配置

## 3. 方案 A：一个 Run Configuration（`make dev`）

适合希望与命令行快速启动行为一致的场景。

### PyCharm 配置

- Type：`Shell Script`
- Name：`deerflow-dev-all`
- Script text：`make dev`
- Working directory：项目根目录（`deer-flow/`）

### 启动后服务

- LangGraph：`localhost:2024`
- Gateway API：`localhost:8001`
- Frontend：`localhost:3000`
- Nginx：`localhost:2026`（统一入口）

访问：

- 应用：`http://localhost:2026`

停止：

- 在 Run 窗口按 `Ctrl+C`，或执行 `make stop`

## 4. 方案 B：Compound 组合启动（推荐调试）

适合在 PyCharm 中分别调试后端与前端。

### 4.1 LangGraph 配置

- Type：`Shell Script`
- Name：`deerflow-langgraph`
- Script text：`cd backend && uv run langgraph dev --no-browser --allow-blocking --no-reload`
- Working directory：项目根目录

### 4.2 Gateway 配置

- Type：`Shell Script`
- Name：`deerflow-gateway`
- Script text：`cd backend && uv run uvicorn src.gateway.app:app --host 0.0.0.0 --port 8001`
- Working directory：项目根目录

### 4.3 Frontend 配置

- Type：`npm`
- Name：`deerflow-frontend`
- Package.json：`frontend/package.json`
- Command：`run`
- Script：`dev`

### 4.4 前端直连后端配置（重要）

如果该方案不启动 nginx，请在 `frontend/.env` 中设置：

```bash
NEXT_PUBLIC_BACKEND_BASE_URL=http://localhost:8001
NEXT_PUBLIC_LANGGRAPH_BASE_URL=http://localhost:2024
```

访问：

- 前端：`http://localhost:3000`

### 4.5 创建 Compound

创建一个 `Compound` 配置，包含：

1. `deerflow-langgraph`
2. `deerflow-gateway`
3. `deerflow-frontend`

启动该 Compound 即可一次拉起全部服务。

## 5. 可选：在 PyCharm 启动 Nginx

如果在方案 B 中仍希望使用统一入口 `:2026`，新增一个 Shell 配置：

- Type：`Shell Script`
- Name：`deerflow-nginx`
- Script text：`mkdir -p logs && nginx -g 'daemon off;' -c $(pwd)/docker/nginx/nginx.local.conf -p $(pwd)`
- Working directory：项目根目录

然后把它加入 Compound。

## 6. 常见问题

### 端口被占用

先执行：

```bash
make stop
```

再重启。

### 前端能打开，但 API 调用失败

检查以下之一：

- 方案 A：确认 nginx 正常运行，并访问 `http://localhost:2026`
- 方案 B：确认 `frontend/.env` 里两个 `NEXT_PUBLIC_*_BASE_URL` 都已设置

### 后端启动成功，但模型调用失败

通常是 `.env` 缺少 API Key，或 `config.yaml` 模型配置不匹配。

### 方案冲突：`make dev` 与 Docker 同时运行

两者都可能占用 `2026` 端口，不要混跑。请选择一种模式运行。

## 7. 常用命令速查

```bash
# 一键启动
make dev

# 停止全部服务
make stop

# 检查环境
make check

# 安装依赖
make install
```
