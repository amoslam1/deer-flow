# DeerFlow 运维：LangGraph 执行观测指南

本文用于排查和观测 LangGraph 的执行细节，重点包括：调用了哪些工具、每一步决策如何推进、常见报错如何处理。

## 1）启动前检查

- 一次只用一种运行模式：
  - 本地：`make dev`
  - Docker：`make docker-start`
- 不要本地和 Docker 混跑（都会占用 `2026` 端口）。
- 先确认接口可达：

```bash
curl -s -o /dev/null -w "2026:%{http_code}\n" http://127.0.0.1:2026/api/langgraph/docs
curl -s -o /dev/null -w "2024:%{http_code}\n" http://127.0.0.1:2024/docs
```

## 2）获取 `thread_id` 和 `run_id`

`thread_id` 就是前端聊天 URL 里的 UUID，例如：

`http://localhost:2026/workspace/chats/f9294de0-7e3d-4fff-b2c3-eb5fb78343cf`

再通过接口拿该线程的运行记录，取最新 `run_id`：

```bash
BASE=http://127.0.0.1:2026/api/langgraph
THREAD_ID=f9294de0-7e3d-4fff-b2c3-eb5fb78343cf

curl -s "$BASE/threads/$THREAD_ID/runs"
RUN_ID=$(curl -s "$BASE/threads/$THREAD_ID/runs" | python3 -c 'import sys,json;print(json.load(sys.stdin)[0]["run_id"])')
echo "$RUN_ID"
```

## 3）查看完整执行流（推荐）

使用 `stream_mode=updates` 拉取 run 的节点级事件：

```bash
curl -sN -H 'Last-Event-ID: -1' \
"$BASE/threads/$THREAD_ID/runs/$RUN_ID/stream?stream_mode=updates"
```

可观测的信息：

- 中间件执行：`ThreadDataMiddleware.before_agent`、`SandboxMiddleware.before_agent` 等
- 模型决策：`model` 节点（含 `tool_calls`）
- 工具执行结果：`tools` 节点（tool message）

说明：`Last-Event-ID: -1` 会回放该 run 的可恢复历史事件，适合复盘已完成任务。

## 4）提取简版时间线（思考 + 调用工具 + 工具结果）

```bash
curl -sN -H 'Last-Event-ID: -1' \
"$BASE/threads/85fe00b6-6291-4ab0-8b65-70076bd91eea/runs/85fe00b6-6291-4ab0-8b65-70076bd91eea/stream?stream_mode=updates" \
| sed -n 's/^data: //p' \
| python3 -c 'import sys,json
for line in sys.stdin:
 line=line.strip()
 if not line or line=="[DONE]":
  continue
 try:
  obj=json.loads(line)
 except Exception:
  continue
 if not isinstance(obj,dict) or not obj:
  continue
 node=next(iter(obj))
 payload=obj[node]
 if node=="model":
  msgs=(payload or {}).get("messages",[])
  if msgs and isinstance(msgs[-1],dict):
   m=msgs[-1]
   rc=(m.get("additional_kwargs") or {}).get("reasoning_content")
   if rc:
    print("[MODEL_THINK]", str(rc).replace("\\n"," ")[:160])
   for t in (m.get("tool_calls") or []):
    print("[TOOL_CALL]", t.get("name"), "args=", t.get("args"))
 elif node=="tools":
  msgs=(payload or {}).get("messages",[])
  if msgs and isinstance(msgs[-1],dict):
   m=msgs[-1]
   name=m.get("name") or m.get("tool_name") or "tool"
   print("[TOOL_RESULT]", name, "->", str(m.get("content")).replace("\\n"," ")[:160])'
```

## 5）常见问题

### A）`{"detail":"Invalid run ID: must be a UUID"}`

原因：

- 把 `<run_id>` 占位符原样传入了 URL
- `run_id` 有拼写错误或不完整

处理：

- 先调用 `GET /threads/{thread_id}/runs`，复制真实 `run_id` 再请求

### B）`{"detail":"Thread with ID ... not found"}`

原因：

- 线程被 LangGraph 的 TTL 清理器删除了（开发模式常见）

处理：

```bash
LANGGRAPH_THREAD_TTL=1440 make dev
```

或直接启动 LangGraph 时设置：

```bash
cd backend
LANGGRAPH_THREAD_TTL=1440 uv run langgraph dev --no-browser --allow-blocking --no-reload
```

### C）前端 UI 看不到完整思考链

当前默认行为：

- 历史步骤折叠在 `more steps` 下
- `thinking` 区域默认折叠
- 前端提交时使用 `["values","messages-tuple","custom"]`，未订阅 `updates`

相关代码位置：

- `frontend/src/components/workspace/messages/message-group.tsx`
- `frontend/src/core/threads/hooks.ts`
- `frontend/src/core/messages/utils.ts`

因此，运维排障建议以本文的 run stream 命令为准。
