---
name: openspec-new-change
description: Start a new OpenSpec change using the experimental artifact workflow. Use when the user wants to create a new feature, fix, or modification with a structured step-by-step approach.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.2.0"
---

使用实验性 artifact 驱动流程创建新 change（只做“起步”，不自动写完全部文档）。

**输入**：change 名称（kebab-case）或需求描述。

**步骤**

1. **确认需求与名称**

   若输入不清晰，先用 **AskUserQuestion** 询问并推导 change 名。

2. **确定 schema**

   默认使用项目默认 schema（通常 `spec-driven`）。

   仅在以下场景指定 `--schema`：
   - 用户明确给了 schema 名称
   - 用户要求查看可选 workflow（先跑 `openspec schemas --json`）

3. **创建 change 目录**

   ```bash
   openspec new change "<name>"
   ```

4. **展示 artifact 状态**

   ```bash
   openspec status --change "<name>"
   ```

5. **展示首个 artifact 指令**

   找到第一个 `ready` artifact 后执行：
   ```bash
   openspec instructions <first-artifact-id> --change "<name>"
   ```

6. **停止并等待用户**

**输出要点**
- change 名称和路径
- 当前 workflow/schema 与 artifact 顺序
- 当前完成度（通常 0/N）
- 首个 artifact 的模板/说明
- 提示用户下一步是否继续创建 artifact

**Guardrails**
- 不要提前创建 artifacts
- 只负责“创建 + 展示第一步”
- 同名 change 已存在时，建议继续该 change
