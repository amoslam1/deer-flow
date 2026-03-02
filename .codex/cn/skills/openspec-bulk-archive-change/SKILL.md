---
name: openspec-bulk-archive-change
description: Archive multiple completed changes at once. Use when archiving several parallel changes.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.2.0"
---

批量归档多个 change（支持并行变更一次性收口）。

该技能会对多 change 的 spec 冲突做“基于代码事实”的智能判定，再执行批量归档。

**输入**：可为空（会引导选择）。

**步骤**

1. **获取活动 change**

   执行 `openspec list --json`。若无活动 change，直接结束。

2. **让用户选择归档范围**

   使用 **AskUserQuestion**（多选）展示：
   - 每个 change 名称与 schema
   - `All changes` 选项

   禁止自动选择。

3. **批量收集状态**

   对每个已选 change 收集：
   - Artifact 状态：`openspec status --change "<name>" --json`
   - Task 完成度：读取 `tasks.md` 统计 `[ ]/[x]`
   - Delta specs：`openspec/changes/<name>/specs/` 下能力列表与 requirement 名称

4. **识别 spec 冲突**

   构建映射：`capability -> changes[]`。
   当同一 capability 被 2 个及以上 change 修改时视为冲突。

5. **冲突解析（基于代码）**

   对每个冲突 capability：
   - 读取各 change 的 delta spec
   - 在代码库中搜索实现证据
   - 判定同步顺序：
     - 仅一个已实现：只同步该 change
     - 多个都已实现：按创建时间先旧后新
     - 都未实现：跳过同步并警告

6. **展示批量状态总表**

   展示每个 change：
   - artifacts 是否完成
   - tasks 完成数
   - specs 情况
   - 是否冲突
   - 预期处理状态

7. **统一确认**

   用一次确认询问用户：
   - 归档全部
   - 仅归档 ready 的
   - 取消

8. **按顺序执行**

   对确认归档的 change：
   - 先按冲突结论同步 specs（需要时）
   - 再归档目录：
     ```bash
     mkdir -p openspec/changes/archive
     mv openspec/changes/<name> openspec/changes/archive/YYYY-MM-DD-<name>
     ```
   - 记录每项结果（成功/失败/跳过）

9. **输出最终汇总**

   包含：
   - 成功归档列表与路径
   - 跳过列表与原因
   - 失败列表与错误
   - spec 同步数量与冲突处理摘要

**成功输出示例**

```markdown
## Bulk Archive Complete

Archived N changes:
- <change-1> -> archive/YYYY-MM-DD-<change-1>/
- <change-2> -> archive/YYYY-MM-DD-<change-2>/

Spec sync summary:
- N delta specs synced to main specs
- No conflicts (or: M conflicts resolved)
```

**部分成功输出示例**

```markdown
## Bulk Archive Complete (partial)

Archived N changes:
- <change-1> -> archive/YYYY-MM-DD-<change-1>/

Skipped M changes:
- <change-2> (user chose not to archive incomplete)

Failed K changes:
- <change-3>: Archive directory already exists
```

**Guardrails**
- 任意数量都支持（1+ 可用，2+ 常见）
- 必须用户选择，不自动挑选
- 冲突先识别再处理
- 多个都已实现时按时间顺序同步
- 未实现才可跳过同步，并明确告警
- 统一确认后执行，过程可追踪
- 单项失败不影响其他项继续
