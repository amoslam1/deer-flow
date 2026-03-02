---
name: dev-env-bootstrap
description: Bootstrap DeerFlow local development environment with deterministic preflight checks and setup steps.
license: MIT
compatibility: Requires openspec CLI, make, and project root access.
metadata:
  author: deerflow
  version: "1.0"
---

统一初始化 DeerFlow 本地开发环境。

## 使用场景
- 新成员首次拉起项目。
- 本地环境损坏后需要快速恢复。
- CI 前本地做依赖与配置预检查。

## 输入
- 可选：是否使用 Docker 模式。
- 可选：是否只执行检查不安装。

## 执行步骤
1. 确认当前目录是仓库根目录。
2. 执行 `make check`，识别缺失依赖（Node/pnpm/uv/nginx）。
3. 执行 `make config` 生成 `config.yaml/.env/frontend/.env` 模板。
4. 执行 `make install` 安装前后端依赖。
5. 按用户模式输出下一步：
   - 本地模式：`make dev`
   - Docker 模式：`make docker-init && make docker-start`

## 输出
- 依赖检查报告。
- 配置文件初始化状态。
- 可执行的启动命令和入口地址。

## Guardrails
- 不自动覆盖已有配置文件。
- 缺失关键依赖时停止后续安装步骤。
- 不写入明文 API Key 到版本库文件。
