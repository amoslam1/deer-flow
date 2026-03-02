## Context（背景）

项目中存在高频重复流程：环境准备、服务启动与联调、网关/前端模块脚手架、OpenSpec 生命周期执行、技能文档质量校验等。当前这些流程分散在 README、CONTRIBUTING、Makefile、docs 和人工经验中，缺乏统一可复用的 Codex Skills 设计。

本设计目标是将重复模式沉淀为可复用的 Codex Skills 蓝图，统一触发条件、输入输出和执行步骤。

## Goals / Non-Goals（目标与非目标）

**Goals（目标）:**
- 产出可执行的 Codex Skills 设计清单（含使用场景和步骤）。
- 每个 Skill 定义明确边界，避免与其他 Skill 职责重叠。
- 优先覆盖高频、高收益、低风险流程。

**Non-Goals（非目标）:**
- 本阶段不直接实现全部 Skills 代码与脚本。
- 不改 DeerFlow 运行时业务逻辑（backend/frontend）。
- 不改变 OpenSpec CLI 或 schema 行为。

## Decisions（关键决策）

### Decision 1（决策 1）: 按“开发链路阶段”分组技能
- 方案：按 Setup、Scaffold、Quality、Release 四层组织技能。
- 原因：便于用户按工作阶段快速选择技能，减少触发歧义。

### Decision 2（决策 2）: 每个 Skill 强制定义“输入-步骤-输出”
- 方案：所有 Skill 统一模板：Use Cases / Inputs / Steps / Outputs / Guardrails。
- 原因：便于复用、评审和后续自动化校验。

### Decision 3（决策 3）: 优先抽象“文档化但重复人工执行”的流程
- 方案：先覆盖已在 docs/Makefile 反复出现的操作。
- 原因：风险低、收益快，且可直接映射现有命令。

## Reusable Codex Skills Design（可复用技能设计）

### 1) `dev-env-bootstrap`
**使用场景**
- 新成员首次进入项目。
- 本地环境异常，需要快速定位缺失依赖。

**执行步骤**
1. 运行 `make check` 检查 Node/pnpm/uv/nginx。
2. 若缺失依赖，按平台给出安装命令。
3. 执行 `make config` 生成本地配置模板。
4. 执行 `make install` 安装前后端依赖。
5. 输出“可启动状态”检查结论和下一步命令。

### 2) `local-debug-orchestrator`
**使用场景**
- 需要本地多服务联调（LangGraph/Gateway/Frontend/Nginx）。
- 需要统一日志归档与问题定位。

**执行步骤**
1. 读取 `docs/LOCAL_DEBUG_COMMANDS.md` 与 `scripts/start_local_debug.sh`。
2. 检查端口占用与旧进程残留。
3. 按顺序启动 LangGraph → Gateway → Frontend → Nginx。
4. 启用 `tee_daily_log.py` 进行按日归档。
5. 输出访问地址、日志路径和停止命令。

### 3) `gateway-router-scaffold`
**使用场景**
- 新增 Gateway API 资源（models/memory/mcp/skills/uploads 类似模式）。
- 需要统一 FastAPI 路由、响应模型和错误处理。

**执行步骤**
1. 识别目标资源、路由前缀和 HTTP 方法。
2. 生成 Pydantic request/response 模型。
3. 生成 `APIRouter(prefix="/api", tags=[...])` 与端点函数。
4. 补充 `summary/description`、异常分支和日志。
5. 将 router 接入 `gateway/app.py` 并给出验证请求示例。

### 4) `frontend-core-module-scaffold`
**使用场景**
- 新增前端数据域模块，需遵循 `core/{api,hooks,types,index}` 约定。
- 需要 React Query 模式统一。

**执行步骤**
1. 定义模块名与 queryKey 规范。
2. 生成 `types.ts` 与 `api.ts`（fetch + 错误处理）。
3. 生成 `hooks.ts`（`useQuery/useMutation` + invalidate）。
4. 生成 `index.ts` 出口并检查导入路径。
5. 给出组件侧调用示例和最小验证步骤。

### 5) `api-contract-sync`
**使用场景**
- 后端路由变更后，需要同步前端 API 层。
- 防止路径、字段、错误处理不一致。

**执行步骤**
1. 扫描 gateway router 变更（路径/模型/字段）。
2. 对比 `frontend/src/core/*/api.ts` 与 `types.ts`。
3. 生成差异清单（breaking/non-breaking）。
4. 更新前端 API 调用和 hooks 失效策略。
5. 输出契约一致性报告和回归检查项。

### 6) `skill-frontmatter-validator`
**使用场景**
- 新增或修改 `SKILL.md` 后的质量门禁。
- 避免 frontmatter 破坏导致技能不可解析。

**执行步骤**
1. 遍历目标目录中的 `SKILL.md`。
2. 校验 frontmatter YAML 可解析。
3. 检查必填键：`name/description/license/compatibility/metadata`。
4. 检查命名约束（kebab-case、长度、非法字符）。
5. 输出逐文件结果与可自动修复建议。

### 7) `openspec-change-executor`
**使用场景**
- 需求从提出到归档，希望标准化闭环。
- 避免遗漏 proposal/specs/design/tasks 或任务勾选失真。

**执行步骤**
1. 新建或选择 change，确认 schema。
2. 生成并校验 artifacts（proposal/specs/design/tasks）。
3. 按 tasks 顺序实施，完成后再勾选。
4. 执行 `openspec validate --strict`。
5. 执行 archive 并输出归档摘要。

### 8) `regression-check-runner`
**使用场景**
- 合并前需要最小充分回归，避免全量测试成本过高。
- 根据改动类型自动推荐验证命令。

**执行步骤**
1. 基于变更文件分类（backend/frontend/config/docs）。
2. 生成最小验证命令集（pytest/eslint/tsc/启动冒烟）。
3. 执行命令并收集失败摘要。
4. 关联失败到改动文件并给出修复建议。
5. 形成“可提交/需修复”结论。

### 9) `artifact-upload-flow`
**使用场景**
- 涉及上传文件、artifact 预览和下载链路开发。
- 需要统一虚拟路径、网关 URL 和前端访问方式。

**执行步骤**
1. 明确 thread 维度路径规则和 artifact URL 规范。
2. 校验上传、列举、删除接口行为一致性。
3. 校验前端 loader/utils 对应路径拼接。
4. 验证下载参数与 MIME 行为。
5. 输出端到端手工测试脚本。

### 10) `config-safety-check`
**使用场景**
- 修改 `config.yaml/.env/extensions_config.json` 前后。
- 防止敏感信息泄露、路径错误、模型配置失配。

**执行步骤**
1. 检查敏感字段是否使用环境变量替代明文。
2. 校验关键配置项是否完整（models/sandbox/skills）。
3. 校验路径存在性与端口冲突风险。
4. 生成风险分级（高/中/低）及修复建议。
5. 输出配置变更审计摘要。

## Risks / Trade-offs（风险与权衡）

- [风险] Skills 粒度过细导致触发混乱 → 缓解措施：采用分层命名与明确触发词。
- [风险] 多 Skill 覆盖同一流程导致职责重叠 → 缓解措施：建立输入输出边界与优先级路由规则。
- [风险] 技能脚本与仓库演进脱节 → 缓解措施：引入定期验证任务，基于文档/命令漂移自动提醒。

## Migration Plan（迁移计划）

1. 先落地高频 3 个：`dev-env-bootstrap`、`local-debug-orchestrator`、`openspec-change-executor`。
2. 第二阶段补齐 scaffold 与契约同步类技能。
3. 第三阶段补齐质量门禁类技能（validator/check-runner/config-check）。
4. 每阶段结束后增加一轮示例任务演练并回收反馈。

## Open Questions（待确认问题）

- 技能触发优先级是否需要中心路由器（meta-skill）统一分发？
- `skill-frontmatter-validator` 是否同时覆盖 `.codex/skills` 与 `skills/public|custom`？
- `regression-check-runner` 的默认“最小验证集”是否按目录可配置？
