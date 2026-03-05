# make_lead_agent 调用时序图

本文给出 `make_lead_agent` 的关键运行时链路，帮助快速定位「请求参数 -> 组装 -> 模型/工具/中间件执行」全过程。

## 1. 初始化与装配时序

```mermaid
sequenceDiagram
    autonumber
    participant LG as LangGraph Server
    participant MA as make_lead_agent
    participant AC as AppConfig
    participant MF as create_chat_model
    participant GT as get_available_tools
    participant BM as _build_middlewares
    participant PT as apply_prompt_template

    LG->>MA: make_lead_agent(config)
    MA->>AC: get_app_config()
    MA->>MA: _resolve_model_name(requested_model_name)
    MA->>MA: thinking_enabled 兼容降级
    MA->>MA: 注入 config.metadata

    MA->>MF: create_chat_model(name, thinking_enabled)
    MF-->>MA: model instance

    MA->>GT: get_available_tools(model_name, subagent_enabled)
    GT-->>MA: tools[]

    MA->>BM: _build_middlewares(config, model_name)
    BM-->>MA: middlewares[]

    MA->>PT: apply_prompt_template(subagent_enabled, max_concurrent_subagents)
    PT-->>MA: system_prompt

    MA-->>LG: create_agent(...)
```

## 2. 单轮执行生命周期（中间件视角）

```mermaid
flowchart TD
    A[before_agent] --> A1[ThreadDataMiddleware]
    A1 --> A2[UploadsMiddleware]
    A2 --> A3[SandboxMiddleware]

    B[before_model/wrap_model_call] --> B1[DanglingToolCallMiddleware]
    B1 --> B2[SummarizationMiddleware 可选]
    B2 --> B3[TodoListMiddleware 可选]
    B3 --> B4[ViewImageMiddleware 可选]

    C[model call] --> D[after_model]
    D --> D1[SubagentLimitMiddleware 可选]

    E[tool call wrapping] --> E1[ClarificationMiddleware 最后拦截]
    E1 --> E2{ask_clarification?}
    E2 -- Yes --> E3[写入 ToolMessage + goto END]
    E2 -- No --> E4[正常执行工具]

    F[after_agent] --> F1[TitleMiddleware]
    F1 --> F2[MemoryMiddleware]
```

## 3. 请求参数影响矩阵

| configurable 参数 | 影响点 | 直接结果 |
|---|---|---|
| `model_name` / `model` | 模型解析 | 决定最终模型与 vision 判定 |
| `thinking_enabled` | 模型创建 | 不支持 thinking 时自动降级 |
| `is_plan_mode` | 中间件 | 决定是否注入 `TodoListMiddleware` |
| `subagent_enabled` | 工具 + 中间件 + prompt | 决定 `task` 工具、并发限制、子代理提示区 |
| `max_concurrent_subagents` | prompt + 限流中间件 | 提示词使用原值；中间件会 clamp 到 `[2,4]` |

## 4. 常见问题定位

1. `task` 工具不出现：检查 `subagent_enabled` 是否为 `true`。  
2. `view_image` 不出现：检查当前模型 `supports_vision`。  
3. 首轮即失败：检查 `runtime.context.thread_id` 是否传入。  
4. 澄清后流程停止：这是 `ClarificationMiddleware` 的 `goto END` 设计行为。  
