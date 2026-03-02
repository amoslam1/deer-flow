---
name: openspec-sync-specs
description: Sync delta specs from a change to main specs. Use when the user wants to update main specs with changes from a delta spec, without archiving the change.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.2.0"
---

将 change 下的 delta specs 同步到主 `openspec/specs`。

这是**代理驱动**的智能合并：会读取 delta 与主 spec，再按意图合并，而不是机械覆盖。

**输入**：可选 change 名称。未提供且有歧义时必须让用户选择。

**步骤**

1. **选择 change**

   运行 `openspec list --json`，通过 **AskUserQuestion** 让用户选有 delta specs 的 change。

2. **定位 delta specs**

   `openspec/changes/<name>/specs/*/spec.md`，识别以下块：
   - `## ADDED Requirements`
   - `## MODIFIED Requirements`
   - `## REMOVED Requirements`
   - `## RENAMED Requirements`

   若无 delta specs，直接结束。

3. **逐 capability 合并到主 spec**

   对每个 `openspec/changes/<name>/specs/<capability>/spec.md`：
   - 读取 delta spec
   - 读取主 spec `openspec/specs/<capability>/spec.md`（可能不存在）
   - 按规则应用：

   **ADDED**：
   - 主 spec 无该 requirement：新增
   - 主 spec 已有该 requirement：按 MODIFIED 处理为更新

   **MODIFIED**：
   - 定位主 requirement
   - 只改 delta 涉及的部分，保留未提及内容

   **REMOVED**：
   - 删除对应 requirement 块

   **RENAMED**：
   - 按 `FROM -> TO` 重命名 requirement

   若主 spec 不存在：
   - 新建 `openspec/specs/<capability>/spec.md`
   - 补 `Purpose` + `Requirements` 基础结构

4. **输出同步摘要**

   说明每个 capability 的新增/修改/删除/重命名结果。

**关键原则：智能合并，不做盲目覆盖**

- 增加 scenario 时无需重贴整段 requirement
- delta 表达的是“变更意图”，不是完整替换文件
- 允许做局部且可解释的语义合并

**Guardrails**
- 同步前必须同时读取 delta 与主 spec
- 未提及内容默认保留
- 不明确时先问
- 过程可复跑，结果尽量保持幂等
