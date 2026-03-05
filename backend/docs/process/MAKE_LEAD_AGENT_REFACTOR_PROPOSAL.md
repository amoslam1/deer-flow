# make_lead_agent 改造建议（可执行版）

目标：在不改变核心能力的前提下，提升 `make_lead_agent` 的一致性、可维护性与可测试性。

## P0: 保证并发上限提示与硬限制一致

### 问题
- Prompt 使用 `max_concurrent_subagents` 原始值。
- `SubagentLimitMiddleware` 会将值 clamp 到 `[2,4]`。
- 传入非法值时，模型看到的规则与实际执行不一致。

### 影响
- 模型可能基于错误并发上限规划子任务，导致任务被静默截断。

### 建议
1. 在 `make_lead_agent` 中统一规范化一次 `max_concurrent_subagents`。  
2. 规范化后的值同时用于：
   - `apply_prompt_template(...)`
   - `SubagentLimitMiddleware(max_concurrent=...)`
   - `config["metadata"]`

### 验收标准
- 任何输入下，提示词并发上限与中间件实际上限完全一致。

---

## P0: 减少 `config` 原地修改副作用

### 问题
- 当前会直接修改传入 `config["metadata"]`。

### 影响
- 若上游复用同一个 config dict，可能产生跨调用污染。

### 建议
1. 在函数开头浅拷贝 `config`（至少复制顶层与 `metadata`）。  
2. 后续只修改本地副本并传入 `create_agent`。

### 验收标准
- 多次调用 `make_lead_agent` 时，外部原始 config 不被污染。

---

## P1: 抽离运行时参数解析器

### 问题
- `make_lead_agent` 同时负责参数读取、兜底、日志、装配，职责偏多。

### 建议
1. 增加 `resolve_runtime_options(config) -> RuntimeOptions`（dataclass）。  
2. 在该函数中集中处理：
   - 模型名回退
   - thinking 兼容降级
   - 并发上限规范化
   - metadata 组装

### 收益
- 主函数变为“纯装配”，便于阅读和测试。

---

## P1: 强化中间件顺序的回归测试

### 问题
- 当前测试覆盖了模型解析和 vision 条件，但未覆盖完整中间件顺序。

### 建议
新增测试断言 `_build_middlewares(...)` 的顺序（含可选分支）：
1. `subagent_enabled=false`, `is_plan_mode=false`, 非 vision  
2. `subagent_enabled=true`, `is_plan_mode=true`, vision  

### 验收标准
- 顺序变化会触发测试失败，避免回归。

---

## P2: 标准化日志字段，提升可观测性

### 现状
- 部分中间件使用 `print`，部分使用 `logger`。

### 建议
1. 统一改为结构化 logger。  
2. 建议统一日志字段：`thread_id`, `model_name`, `trace_id`, `is_plan_mode`, `subagent_enabled`。

### 收益
- 线上排障更快，日志检索可聚合。

---

## P2: 澄清中断行为文档化 + 测试化

### 问题
- `ask_clarification` 的真实行为由中间件 `goto END` 完成，容易被误读为普通工具调用。

### 建议
1. 在 API / 架构文档加“中断语义”说明。  
2. 增加端到端测试断言：
   - 命中 `ask_clarification` 后本轮立即结束；
   - 输出中包含对应 ToolMessage。

---

## 建议实施顺序

1. P0-1: 并发上限统一规范化  
2. P0-2: config 副作用隔离  
3. P1-1: 参数解析器重构  
4. P1-2: 中间件顺序测试  
5. P2: 日志统一与澄清中断测试补齐

## 预估成本（粗略）

- P0 两项：0.5-1 天  
- P1 两项：1-1.5 天  
- P2 两项：0.5-1 天  

总计：约 2-3.5 天（含测试）。
