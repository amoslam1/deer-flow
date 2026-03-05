# Component Design（API 与通用模块 I/O）

## 1. API 作用与输入输出

1. `GET /api/models`
- 模块 hash：`940295218756d42f`（`api:GET /api/models`）
- 作用：返回可用模型列表
- 输入：无
- 输出：模型数组（名称、展示名、能力标记）
- 主要依赖：`gateway -> models`
- 依赖路径（hash）：`940295218756d42f->98ceb006215e09fe->97ed0223ace4b7a8`

2. `GET/PUT /api/mcp/config`
- 模块 hash：`270e242441b1a834`（GET），`73d861c3d5bddf33`（PUT）
- 作用：读取/更新 MCP 服务配置
- 输入：`PUT` 时为 MCP 配置对象
- 输出：当前配置快照或更新后的配置
- 主要依赖：`gateway -> mcp -> config`
- 依赖路径（hash）：
  - `270e242441b1a834->98ceb006215e09fe->3adecdefb9444aed->2b5b425e006ef4fe`
  - `73d861c3d5bddf33->98ceb006215e09fe->3adecdefb9444aed->2b5b425e006ef4fe`

3. `GET/PUT /api/skills`、`POST /api/skills/install`
- 模块 hash：`555cec3f1c4599c7`（GET），`f22ca4b6499f7386`（PUT），`3a9e46986bbaf5c1`（POST）
- 作用：查询技能状态、启停技能、安装 skill 包
- 输入：技能名、启用状态、安装包
- 输出：技能列表/详情、更新结果、安装结果
- 主要依赖：`gateway -> skills -> skills/public|skills/custom`
- 依赖路径（hash）：
  - `555cec3f1c4599c7->98ceb006215e09fe->5894741b612dae26`
  - `f22ca4b6499f7386->98ceb006215e09fe->5894741b612dae26`
  - `3a9e46986bbaf5c1->98ceb006215e09fe->5894741b612dae26`

4. `GET /api/memory`、`POST /api/memory/reload`、`GET /api/memory/status`
- 模块 hash：`281862bedb91c209`（GET memory），`c7f595cf59e59a50`（POST reload），`c5daf628327d8abe`（GET status）
- 作用：读取记忆、触发重载、查看状态
- 输入：重载触发参数（可为空）
- 输出：记忆数据与配置状态
- 主要依赖：`gateway -> memory -> agents/memory`
- 依赖路径（hash）：
  - `281862bedb91c209->98ceb006215e09fe->7ebfd43cccc67cf5`
  - `c7f595cf59e59a50->98ceb006215e09fe->7ebfd43cccc67cf5`
  - `c5daf628327d8abe->98ceb006215e09fe->7ebfd43cccc67cf5`

5. `POST /api/threads/{id}/uploads`、`GET /list`、`DELETE /{filename}`
- 模块 hash：`fec2e606e0dc2fdb`（POST），`8b64f8027f996b3b`（GET list），`004b67bb26c09ad5`（DELETE）
- 作用：上传/列举/删除线程文件
- 输入：线程 ID、文件内容、目标文件名
- 输出：文件元数据、列表、删除结果
- 主要依赖：`gateway -> uploads -> sandbox/thread data`
- 依赖路径（hash）：
  - `fec2e606e0dc2fdb->98ceb006215e09fe->2fd7b9dce5128c2d`
  - `8b64f8027f996b3b->98ceb006215e09fe->2fd7b9dce5128c2d`
  - `004b67bb26c09ad5->98ceb006215e09fe->2fd7b9dce5128c2d`

6. `GET /api/threads/{id}/artifacts/{path}`
- 模块 hash：`81e9973d19c54346`
- 作用：读取或下载生成产物
- 输入：线程 ID、产物路径、可选 `download=true`
- 输出：文件流或错误信息
- 主要依赖：`gateway -> artifacts -> thread outputs`
- 依赖路径（hash）：`81e9973d19c54346->98ceb006215e09fe->2fd7b9dce5128c2d`

## 2. 通用模块作用与输入输出

1. `common:config-loader`（`backend/src/config`）
- 模块 hash：`20cdcb391dd00901`（logical），`2b5b425e006ef4fe`（module）
- 作用：统一加载 `config.yaml/.env/extensions_config`
- 输入：配置路径、环境变量
- 输出：运行时配置对象（模型、工具、沙箱、技能等）
- 依赖关系：`gateway/langgraph -> config-loader`
- 依赖路径（hash）：`98ceb006215e09fe->20cdcb391dd00901->2b5b425e006ef4fe`，`d38bc66c683d3b7a->20cdcb391dd00901->2b5b425e006ef4fe`

2. `common:tool-registry`（`backend/src/tools`）
- 模块 hash：`cd0f77195c2cf57f`（logical），`79b4876d58940a6c`（module）
- 作用：装配内置工具、社区工具、MCP 工具并按组暴露
- 输入：tool groups、模型能力、开关配置
- 输出：可执行工具集合
- 依赖关系：`langgraph -> tool-registry -> builtins/community/mcp`
- 依赖路径（hash）：`d38bc66c683d3b7a->cd0f77195c2cf57f->79b4876d58940a6c`

3. `scheduler:subagent-executor`（`backend/src/subagents/executor.py`）
- 模块 hash：`d7049720d2531d96`（logical），`6ffb0e9886eebe40`（module）
- 作用：调度子代理并发执行与状态轮询
- 输入：task 请求、子代理类型、超时参数
- 输出：子任务状态事件与最终结果
- 依赖关系：`langgraph -> subagent-executor -> subagents`
- 依赖路径（hash）：`d38bc66c683d3b7a->d7049720d2531d96->6ffb0e9886eebe40`

4. `scheduler:memory-update-queue`（`backend/src/agents/memory/queue.py`）
- 模块 hash：`1a7ef8e766f185a2`（logical），`7ebfd43cccc67cf5`（module）
- 作用：对会话记忆更新做防抖、合并与异步落盘
- 输入：对话片段、线程标识、配置阈值
- 输出：结构化 memory 更新结果
- 依赖关系：`langgraph -> memory-update-queue -> agents/memory`
- 依赖路径（hash）：`d38bc66c683d3b7a->1a7ef8e766f185a2->7ebfd43cccc67cf5`

## 3. 面向 Skills 的统一 I/O 契约

1. `jfz-code-path-plan-review`
- 输入：`module_hash | location_hash | file:start-end` + `next_plan`（下一步计划）
- 输出：代码与链路上下文摘要 + 可行性评估（high/medium/low）+ 问题清单 + 推荐下一步（含回滚）

## 4. `jfz-code-path-plan-review` 数据结构

请求结构（示例）：

```json
{
  "target": "backend/src/gateway/app.py:1-120",
  "next_plan": "新增参数校验并补充测试",
  "constraints": {
    "risk_tolerance": "medium",
    "time_budget": "2h"
  }
}
```

响应结构（示例）：

```json
{
  "target": {
    "hash": "3596b7d831c7eac0",
    "canonical_id": "entrypoint:backend/src/gateway/app.py",
    "type": "entrypoint",
    "path": "backend/src/gateway/app.py"
  },
  "context_summary": "命中网关入口，直接影响 gateway 服务链路。",
  "dependency_paths": [
    "3596b7d831c7eac0->98ceb006215e09fe",
    "3596b7d831c7eac0->98ceb006215e09fe->72404a558745fd52"
  ],
  "feasibility": "medium",
  "issues": [
    "需确认改动是否影响 mcp/skills 路由行为。"
  ],
  "next_steps": [
    "先补参数校验单测，再改入口逻辑。"
  ],
  "rollback": "按受影响 hash 路径逐步回退。"
}
```

## 5. 可行性评估规则

- `high`：只涉及单服务内聚模块，依赖路径短（通常 <= 3 节点），测试可覆盖。  
- `medium`：跨 1-2 个关键模块，存在待确认接口/配置耦合。  
- `low`：涉及跨服务链路、关键共用模块或存在明显 I/O 约束冲突。  

## 6. 错误码与失败语义

- `TARGET_UNRESOLVED`：输入 target 无法解析为有效 hash。  
- `CHAIN_NOT_FOUND`：能命中节点但未找到依赖链（需提示索引过期）。  
- `PLAN_MISSING`：未提供 `next_plan`，仅能输出上下文，不能给完整可行性结论。  
- `INDEX_STALE`：文档和索引版本不一致，建议先重建 artifacts。  
