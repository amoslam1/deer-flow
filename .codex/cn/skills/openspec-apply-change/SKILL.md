---
name: openspec-apply-change
description: Implement tasks from an OpenSpec change. Use when the user wants to start implementing, continue implementation, or work through tasks.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.2.0"
---

从 OpenSpec change 实施任务。

**输入**：可选 `change` 名称。若未提供，先结合上下文判断；若不明确，必须提示用户选择可用 change。

**步骤**

1. **选择 change**

   - 指定了名称就直接使用。
   - 未指定时：
     - 先尝试从上下文推断；
     - 仅有一个活动 change 时可自动选中；
     - 若有歧义，执行 `openspec list --json`，并使用 **AskUserQuestion** 让用户选择。

   必须明确告知：`Using change: <name>`，并说明如何切换（如 `/opsx:apply <other>`）。

2. **查看状态并识别 schema**

   ```bash
   openspec status --change "<name>" --json
   ```

   重点解析：
   - `schemaName`（如 `spec-driven`）
   - 哪个 artifact 承载任务（通常是 `tasks`，但以状态结果为准）

3. **获取 apply 指令**

   ```bash
   openspec instructions apply --change "<name>" --json
   ```

   返回内容通常包含：
   - `contextFiles`：实现前必须阅读的文件
   - `progress`：总数、完成数、剩余数
   - 当前任务列表与状态
   - 动态执行提示

   **状态处理**：
   - `state: "blocked"`：提示缺失 artifact，建议先用 `openspec-continue-change`
   - `state: "all_done"`：提示已完成，可归档
   - 其他状态：继续实施

4. **读取上下文文件**

   按 `contextFiles` 逐个读取。常见：
   - `spec-driven`：`proposal`、`specs`、`design`、`tasks`
   - 其他 schema：以 CLI 输出为准

5. **展示当前进度**

   展示以下信息：
   - 使用的 schema
   - 进度：`N/M tasks complete`
   - 剩余任务概览
   - CLI 动态提示

6. **按顺序实施任务（循环）**

   对每个未完成任务：
   - 明确当前正在做的任务
   - 做最小且聚焦的代码改动
   - 完成后把 `tasks.md` 对应项从 `- [ ]` 改为 `- [x]`
   - 继续下一个任务

   **以下情况必须暂停并同步用户**：
   - 任务定义不清楚
   - 实施中暴露设计问题（建议先更新 artifact）
   - 出现阻塞或关键错误
   - 用户中断

7. **收尾状态输出（完成或暂停）**

   输出：
   - 本轮完成了哪些任务
   - 总体进度 `N/M`
   - 若全部完成：建议归档
   - 若暂停：说明原因并等待下一步指令

**实施期输出示例**

```markdown
## Implementing: <change-name> (schema: <schema-name>)

Working on task 3/7: <task description>
[...implementation happening...]
✓ Task complete

Working on task 4/7: <task description>
[...implementation happening...]
✓ Task complete
```

**完成时输出示例**

```markdown
## Implementation Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** 7/7 tasks complete ✓

### Completed This Session
- [x] Task 1
- [x] Task 2
...

All tasks complete! Ready to archive this change.
```

**暂停时输出示例**

```markdown
## Implementation Paused

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** 4/7 tasks complete

### Issue Encountered
<description of the issue>

**Options:**
1. <option 1>
2. <option 2>
3. Other approach

What would you like to do?
```

**Guardrails**
- 持续推进，直到全部完成或被阻塞
- 实施前必须读取 `contextFiles`
- 任务不明确先问，不要猜
- 若实现与设计冲突，先暂停并建议更新 artifacts
- 每次改动保持最小范围
- 每完成一项立即更新 checkbox
- 遇到错误或阻塞立即报告
- 依赖 `contextFiles`，不要假设固定文件名

**流式工作流说明**
- 可在任意阶段调用：任务前、任务中、局部完成后都可
- 允许发现问题后回到 artifacts 修订，不是僵化的单向流程
