---
name: openspec-continue-change
description: Continue working on an OpenSpec change by creating the next artifact. Use when the user wants to progress their change, create the next artifact, or continue their workflow.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.2.0"
---

继续推进一个已有 change：每次只创建“下一个” artifact。

**输入**：可选 `change` 名称。若未提供且存在歧义，必须让用户选择。

**步骤**

1. **选择 change**

   运行 `openspec list --json`，按最近修改排序，使用 **AskUserQuestion** 让用户选择。建议展示前 3-4 个并标注：
   - change 名称
   - schema
   - 当前状态
   - 最近修改时间

2. **读取当前状态**

   ```bash
   openspec status --change "<name>" --json
   ```

   关注：`schemaName`、`artifacts`、`isComplete`。

3. **按状态分支处理**

   - `isComplete: true`：告知全部完成，可实施或归档。
   - 存在 `ready` artifact：
     - 选第一个 `ready`
     - 执行 `openspec instructions <artifact-id> --change "<name>" --json`
     - 读取依赖 artifacts
     - 基于 template + instruction 创建该 artifact
     - 只创建这一个，然后停止
   - 全部 `blocked`：提示状态异常并建议排查。

4. **展示进度**

   ```bash
   openspec status --change "<name>"
   ```

   输出：
   - 本次创建了哪个 artifact
   - schema
   - 当前进度
   - 新解锁项

**Guardrails**
- 每次调用只创建一个 artifact
- 严格按依赖顺序推进
- 上下文不清楚先问
- 写完需确认文件确实落盘
- `context/rules` 是约束，不要原样写进 artifact
