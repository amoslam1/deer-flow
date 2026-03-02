---
name: openspec-verify-change
description: Verify implementation matches change artifacts. Use when the user wants to validate that implementation is complete, correct, and coherent before archiving.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.2.0"
---

验证实现是否与 change artifacts（specs/tasks/design）一致。

**输入**：可选 change 名称。若未提供且有歧义，必须让用户选择。

**步骤**

1. **选择 change**

   执行 `openspec list --json`，用 **AskUserQuestion** 让用户选择。

   展示时建议包含：
   - 是否有任务文件
   - schema
   - 是否进行中（任务未完成）

2. **读取状态与 schema**

   ```bash
   openspec status --change "<name>" --json
   ```

3. **读取上下文 artifacts**

   ```bash
   openspec instructions apply --change "<name>" --json
   ```

   根据 `contextFiles` 读取可用 artifact。

4. **初始化验证维度**

   建立三类检查：
   - **Completeness**：任务和需求覆盖是否完整
   - **Correctness**：实现是否符合 requirement/scenario
   - **Coherence**：实现是否与 design、项目模式一致

   问题分级：`CRITICAL` / `WARNING` / `SUGGESTION`。

5. **验证 Completeness**

   - 任务完成度：解析 `tasks.md` 的 `[ ]/[x]`
   - spec 覆盖：遍历 delta requirements，检索代码中实现证据
   - 未完成任务或明显未实现 requirement 标记为 `CRITICAL`

6. **验证 Correctness**

   - requirement 对照实现：检查语义是否偏离
   - scenario 覆盖：检查代码与测试是否覆盖主要场景
   - 发现偏离或缺口标记为 `WARNING`

7. **验证 Coherence**

   - 有 `design.md` 时：检查关键决策是否被遵循
   - 检查新增代码是否遵循项目常用模式
   - 风格或结构改进建议标记为 `SUGGESTION`

8. **生成验证报告**

   报告包含：
   - 总结表（Completeness/Correctness/Coherence）
   - 按优先级分组的问题
   - 每个问题的可执行建议（尽量给文件/行号）
   - 最终结论：可归档 / 需修复后再归档

**Graceful Degradation**
- 仅有 tasks：只做任务完整性检查
- 有 tasks + specs：做完整性 + 正确性
- 有完整 artifacts：做三维检查

**Guardrails**
- 结论以证据为基础，避免泛泛而谈
- 不确定时降低级别（Suggestion 优先）
- 每个问题都要可执行、可定位
