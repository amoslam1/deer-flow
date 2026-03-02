---
name: openspec-ff-change
description: Fast-forward through OpenSpec artifact creation. Use when the user wants to quickly create all artifacts needed for implementation without stepping through each one individually.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.2.0"
---

快速生成可实施所需的全部 artifacts（一步到位）。

**输入**：change 名称（kebab-case）或功能描述。

**步骤**

1. **明确目标**

   若用户目标不清晰，使用 **AskUserQuestion** 询问要做什么，并推导 kebab-case change 名。

2. **创建 change**

   ```bash
   openspec new change "<name>"
   ```

3. **读取构建顺序**

   ```bash
   openspec status --change "<name>" --json
   ```

   提取：
   - `applyRequires`
   - `artifacts` 状态与依赖

4. **按依赖顺序创建 artifacts**

   对每个 `ready` artifact：
   - `openspec instructions <artifact-id> --change "<name>" --json`
   - 读取依赖文件
   - 按 template 创建文件
   - 应用 `context/rules`（仅作为写作约束）

   每创建一个都刷新状态，直到 `applyRequires` 全部为 `done`。

5. **输出最终状态**

   ```bash
   openspec status --change "<name>"
   ```

**输出要点**
- change 名称与路径
- 已创建 artifacts 清单
- 当前可实施状态（apply-ready）
- 下一步提示：运行 `/opsx:apply`

**Guardrails**
- 必须创建到 apply-ready
- 不跳过依赖
- 上下文不清楚可询问，但默认优先推进
- 文件落盘后再进入下一项
