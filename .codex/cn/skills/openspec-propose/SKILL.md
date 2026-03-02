---
name: openspec-propose
description: Propose a new change with all artifacts generated in one step. Use when the user wants to quickly describe what they want to build and get a complete proposal with design, specs, and tasks ready for implementation.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.2.0"
---

为新 change 一次性生成 proposal 阶段所需 artifacts。

我会创建：
- `proposal.md`（做什么、为什么）
- `design.md`（怎么做）
- `tasks.md`（实施清单）

准备实现时，执行 `/opsx:apply`。

**输入**：change 名称（kebab-case）或需求描述。

**步骤**

1. **澄清需求并确定名称**

   需求不清晰时，使用 **AskUserQuestion** 询问，推导 kebab-case 名称。

2. **创建 change**

   ```bash
   openspec new change "<name>"
   ```

3. **读取 artifact 顺序**

   ```bash
   openspec status --change "<name>" --json
   ```

   关注：`applyRequires` 与 `artifacts`。

4. **按依赖顺序创建 artifacts（直到 apply-ready）**

   对每个 `ready` artifact：
   - `openspec instructions <artifact-id> --change "<name>" --json`
   - 读取已完成依赖
   - 按 template 填充内容
   - 仅将 `context/rules` 作为约束，不要写入正文
   - 创建完成后刷新状态

5. **展示最终状态**

   ```bash
   openspec status --change "<name>"
   ```

**输出要点**
- change 名称与路径
- 已创建 artifacts 列表
- 是否已 apply-ready
- 下一步：`/opsx:apply`

**Guardrails**
- 必须创建到可实施状态
- 必须读取依赖 artifacts
- 上下文不清晰时可追问
- 同名 change 已存在时，询问继续还是新建
- 确认每个 artifact 已写入后再推进
