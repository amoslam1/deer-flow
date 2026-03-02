---
name: openspec-archive-change
description: Archive a completed change in the experimental workflow. Use when the user wants to finalize and archive a change after implementation is complete.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.2.0"
---

在实验工作流中归档已完成的 change。

**输入**：可选 `change` 名称。未提供且有歧义时，必须让用户选择。

**步骤**

1. **选择 change**

   执行 `openspec list --json` 获取活动 change，使用 **AskUserQuestion** 让用户选择。

   要求：
   - 仅展示活动 change（未归档）
   - 尽量展示 schema 信息
   - 不允许猜测或自动选择

2. **检查 artifact 完成状态**

   ```bash
   openspec status --change "<name>" --json
   ```

   解析：
   - `schemaName`
   - `artifacts` 的完成状态

   若存在未完成 artifact：
   - 明确警告
   - 询问是否继续归档

3. **检查任务完成状态**

   读取任务文件（通常 `tasks.md`），统计：
   - `- [ ]` 未完成
   - `- [x]` 已完成

   若存在未完成任务：
   - 明确警告并询问是否继续

4. **评估 delta spec 同步状态**

   检查 `openspec/changes/<name>/specs/`：
   - 无 delta specs：跳过同步提示
   - 有 delta specs：对比主 specs，先给出汇总，再让用户选择

   典型选项：
   - 有差异：`Sync now (recommended)` / `Archive without syncing`
   - 已同步：`Archive now` / `Sync anyway` / `Cancel`

   若用户选同步：调用 `openspec-sync-specs` 流程后继续归档。

5. **执行归档**

   ```bash
   mkdir -p openspec/changes/archive
   mv openspec/changes/<name> openspec/changes/archive/YYYY-MM-DD-<name>
   ```

   归档前先检查目标是否存在：
   - 已存在则报错并提示处理
   - 不存在则继续

6. **输出归档结果**

   展示：
   - change 名称
   - schema
   - 归档路径
   - specs 是否同步
   - 是否带警告继续归档

**成功输出示例**

```markdown
## Archive Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Archived to:** openspec/changes/archive/YYYY-MM-DD-<name>/
**Specs:** ✓ Synced to main specs (or "No delta specs" or "Sync skipped")

All artifacts complete. All tasks complete.
```

**Guardrails**
- 未指定 change 时必须选择，不自动猜
- 以 `openspec status --json` 为准评估完成度
- 发现未完成项只警告并确认，不强制阻断
- 移动目录时保留 `.openspec.yaml`
- 若涉及 spec 同步，先完成同步评估再归档
