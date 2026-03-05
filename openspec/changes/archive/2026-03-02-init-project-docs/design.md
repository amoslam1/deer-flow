## Context

`init-project-docs` 目标是把 DeerFlow 的技术架构、运行服务、后台调度与通用模块整理成“可索引文档”。当前虽然有 README/CLAUDE，但缺少统一模块 ID，无法用一个短标识（hash）做跨文件跳转和依赖串联。该变更仅做文档与扫描规范，不改运行时代码。

## Goals / Non-Goals

**Goals:**
- 为扫描到的每个模块分配固定 16 位 hash。
- 同时输出“名称链路”和“hash 链路”，方向统一为父级 -> 子级。
- 覆盖三类对象：技术与架构模块、服务与后台服务、通用模块。
- 定义可重复执行的生成流程，后续可增量更新。

**Non-Goals:**
- 不修改 Gateway/LangGraph/Frontend 行为。
- 不引入数据库或图存储。
- 不在本次变更实现前端可视化。

## Decisions

### Decision 1: Hash 规范采用 `sha256(canonical_id)[:16]`
- 方案：对每个模块的 canonical_id（如 `module:backend/src/agents`、`service:gateway`）做 SHA-256，取前 16 位小写十六进制。
- 选择原因：实现简单、跨语言一致、碰撞风险可接受、可直接在 shell/python 生成。
- 备选方案：
  - `uuid4`：随机值不可复现，不满足“同模块恒定 hash”。
  - `md5`：虽短但语义上不建议继续推广。
  - `sha256[:8]`：太短，碰撞风险增大。

### Decision 2: 依赖表达采用双轨输出
- 方案：每个模块都记录 `depends_on`（直接父->子），并额外生成链式摘要 `Ahash->Bhash->Chash`。
- 选择原因：
  - 邻接关系便于程序校验与拓扑分析。
  - 链式摘要便于人工沟通和在对话中快速粘贴引用。
- 备选方案：
  - 仅输出链式文本：可读但不便验证。
  - 仅输出邻接表：机器友好但人工阅读成本高。

### Decision 3: 文档拆分为两份能力规格 + 一份聚合清单
- 方案：
  - `project-architecture-hash-index` 定义技术/架构模块盘点。
  - `service-module-hash-chain` 定义服务/后台/通用模块盘点。
  - 实施时再生成汇总文档（包含模块元数据、hash、父子关系、链路样例）。
- 选择原因：保持职责清晰，便于独立演进。
- 备选方案：
  - 单一超大规格：维护困难，审阅成本高。

### Decision 4: Skills 复用策略（从“查询”升级为“评估与方案”）
- 复用 `openspec-propose`：一次产出 proposal/design/specs/tasks。
- 不复用 `config-safety-check`：目标不是配置一致性。
- 不复用 `gateway-router-scaffold` / `frontend-core-module-scaffold`：本变更不涉及 API/前端代码脚手架。
- 新增技能目标（单一 skill）：
  - `jfz-code-path-plan-review`：输入代码位置或 hash + next_plan，自动汇总局部与链路上下文，并输出方案可行性评估与下一步建议。

## Risks / Trade-offs

- [模块边界歧义] 同一目录是否算单模块可能有分歧 -> 先固定“一级目录为模块，必要时白名单细分”规则。
- [hash 变更风险] canonical_id 命名调整会导致 hash 漂移 -> 在文档中冻结 canonical_id 格式并加变更说明。
- [依赖链过长] 深层链不易维护 -> 存储直接依赖，链路按需计算。
- [文档陈旧] 目录更新后清单过时 -> 在任务中加入最小回归检查与更新步骤。

## Migration Plan

1. 创建模块分类规则与 canonical_id 规则。
2. 扫描仓库并生成模块清单（含 hash、依赖、链路）。
3. 将清单提交到变更目录并校验格式。
4. 通过 OpenSpec verify 后再归档同步到主 specs。

Rollback:
- 若规则不合理，回退到上一版文档，保留扫描脚本输入输出以便重放。
- 若 hash 方案需调整，先并行输出新旧 hash 一版，再在后续变更切换。

## Open Questions

- “模块”是否只覆盖一级目录，还是需递归到二级（如 `backend/src/agents/middlewares`）？
- 后台“调度”是否仅指 subagent/memory 队列，还是包含 Docker provisioner 生命周期？
- 聚合清单最终放在 `openspec/basic_design/` 还是 `openspec/changes/<change>/artifacts/`？
