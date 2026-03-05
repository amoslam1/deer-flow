# Project Design（项目架构及技术要点）

## 1. 架构分层与主链路

- 统一入口：`nginx`（`http://localhost:2026`）
- 前端服务：`frontend`（Next.js）
- 后端服务：`gateway`（FastAPI）、`langgraph`（Agent Runtime）
- 可选服务：`provisioner`（K8s Sandbox 管理）

核心依赖方向固定为父级 -> 子级：

- `nginx -> frontend`
- `nginx -> gateway`
- `nginx -> langgraph`
- `langgraph -> gateway`（模型/配置能力联动）
- `gateway -> backend/src/gateway|models|mcp|skills`
- `langgraph -> backend/src/agents|tools|subagents|sandbox|community`

## 2. Hash 规则（用于依赖追踪）

- `module_hash = sha256(canonical_id)[:16]`
- `location_hash = sha256(file_path:start_line:end_line:symbol:commit)[:16]`（可选）
- `canonical_id` 前缀：`module|service|entrypoint|scheduler|common|api`
- 依赖链输出：
  - 名称链：`A->B->C`
  - Hash 链：`Ahash->Bhash->Chash`

## 3. 技术要点

- Backend：Python 3.12 + LangGraph + FastAPI + Pydantic
- Frontend：Next.js 16 + React 19 + TypeScript
- Runtime：Nginx 反向代理，Local/AIO Sandbox，可选 Docker provisioner
- 目标能力：输入 hash 或代码位置后，能回溯上下文并支持方案评估

## 4. 索引产物定义（依赖关系落盘）

- `artifacts/hash-index.json`
  - 记录模块/服务基础信息：`hash, canonical_id, type, path, parents, children`
  - 作用：给定 hash 快速定位“当前节点 + 直接上下游”
- `artifacts/hash-chains.json`
  - 记录多跳链路：`Ahash->Bhash->Chash`
  - 作用：给定节点定位“跨层级影响路径”

## 5. 依赖路径（Hash 形式）

### 5.1 核心节点 Hash

- `d23ae50788845411` = `entrypoint:docker/docker-compose-dev.yaml`
- `b6817b8b43c0dced` = `service:nginx`
- `6ef339c43c3b32be` = `service:frontend`
- `98ceb006215e09fe` = `service:gateway`
- `d38bc66c683d3b7a` = `service:langgraph`
- `b3f1ef2553afe509` = `service:provisioner`
- `3596b7d831c7eac0` = `entrypoint:backend/src/gateway/app.py`
- `590e4e520343c8c7` = `entrypoint:backend/langgraph.json`
- `d533dfcdadc90669` = `entrypoint:frontend/src/core/api/api-client.ts`

### 5.2 服务级依赖路径（Ahash->Bhash）

- `d23ae50788845411->b6817b8b43c0dced`（compose -> nginx）
- `d23ae50788845411->6ef339c43c3b32be`（compose -> frontend）
- `d23ae50788845411->98ceb006215e09fe`（compose -> gateway）
- `d23ae50788845411->d38bc66c683d3b7a`（compose -> langgraph）
- `d23ae50788845411->b3f1ef2553afe509`（compose -> provisioner）
- `b6817b8b43c0dced->6ef339c43c3b32be`（nginx -> frontend）
- `b6817b8b43c0dced->98ceb006215e09fe`（nginx -> gateway）
- `b6817b8b43c0dced->d38bc66c683d3b7a`（nginx -> langgraph）
- `590e4e520343c8c7->d38bc66c683d3b7a`（langgraph entry -> langgraph service）
- `3596b7d831c7eac0->98ceb006215e09fe`（gateway entry -> gateway service）
- `d533dfcdadc90669->6ef339c43c3b32be`（frontend api client entry -> frontend service）

### 5.3 模块级依赖路径（Ahash->Bhash）

- `98ceb006215e09fe->72404a558745fd52`（gateway -> module:backend/src/gateway）
- `98ceb006215e09fe->97ed0223ace4b7a8`（gateway -> module:backend/src/models）
- `98ceb006215e09fe->3adecdefb9444aed`（gateway -> module:backend/src/mcp）
- `98ceb006215e09fe->5894741b612dae26`（gateway -> module:backend/src/skills）
- `98ceb006215e09fe->20cdcb391dd00901`（gateway -> common:config-loader）
- `20cdcb391dd00901->2b5b425e006ef4fe`（config-loader -> module:backend/src/config）
- `d38bc66c683d3b7a->7ebfd43cccc67cf5`（langgraph -> module:backend/src/agents）
- `d38bc66c683d3b7a->79b4876d58940a6c`（langgraph -> module:backend/src/tools）
- `d38bc66c683d3b7a->6ffb0e9886eebe40`（langgraph -> module:backend/src/subagents）
- `d38bc66c683d3b7a->2fd7b9dce5128c2d`（langgraph -> module:backend/src/sandbox）
- `d38bc66c683d3b7a->257086f77783d424`（langgraph -> module:backend/src/community）
- `d38bc66c683d3b7a->cd0f77195c2cf57f`（langgraph -> common:tool-registry）
- `cd0f77195c2cf57f->79b4876d58940a6c`（tool-registry -> module:backend/src/tools）
- `d38bc66c683d3b7a->d7049720d2531d96`（langgraph -> scheduler:subagent-executor）
- `d7049720d2531d96->6ffb0e9886eebe40`（subagent-executor -> module:backend/src/subagents）
- `d38bc66c683d3b7a->1a7ef8e766f185a2`（langgraph -> scheduler:memory-update-queue）
- `1a7ef8e766f185a2->7ebfd43cccc67cf5`（memory-update-queue -> module:backend/src/agents）
- `6ef339c43c3b32be->d15ae8d4a14922ba`（frontend -> module:frontend/src/app）
- `6ef339c43c3b32be->34a717ac70d5ebc1`（frontend -> module:frontend/src/core）
- `6ef339c43c3b32be->cd78a768fe713c6f`（frontend -> module:frontend/src/components）

## 6. 代码路径评估流程（jfz-code-path-plan-review）

输入形式：

- `file`（如 `backend/src/gateway/app.py`）
- `file:start-end`（如 `backend/src/gateway/app.py:1-120`）
- `module_hash` / `location_hash`

标准流程：

1. 目标解析：路径或 hash 解析为目标节点 hash。  
2. 上下文定位：在 `hash-index.json` 查询节点元数据与直接依赖。  
3. 链路展开：在 `hash-chains.json` 查询上下游 `Ahash->Bhash`。  
4. 规则对照：结合 `component.md` 的 API/通用模块 I/O 约束做一致性检查。  
5. 结论输出：给出可行性等级、风险点、建议步骤和回滚建议。  

可行性等级定义：

- `high`：链路短、改动边界清晰、I/O 约束明确。  
- `medium`：链路可控但存在不确定依赖或验证缺口。  
- `low`：链路长且关键节点多，或计划与 I/O 约束冲突。  

## 7. 维护与更新规则

- 每次新增/修改服务、模块、API 路由后，必须重生成：
  - `artifacts/hash-index.json`
  - `artifacts/hash-chains.json`
- 文档更新顺序：
  1. 先更新 `project.md` 依赖路径。  
  2. 再更新 `component.md` 的模块 I/O 与 hash 路径。  
- 若 hash 规则变更，必须在变更期并行保留旧 hash 到新 hash 映射一版。
