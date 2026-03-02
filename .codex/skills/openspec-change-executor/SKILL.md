---
name: openspec-change-executor
description: Execute a full OpenSpec lifecycle from proposal artifacts to apply, verification, and archive.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: deerflow
  version: "1.0"
---

执行 OpenSpec 全生命周期（create -> apply -> verify -> archive）。

## 使用场景
- 需要标准化推进一个 change。
- 团队希望减少遗漏 artifacts 或任务勾选失真。

## 输入
- change 名称（kebab-case）或需求描述。
- 可选：是否快速生成全部 artifacts。

## 执行步骤
1. 选择或创建 change：`openspec new change <id>`。
2. 生成/补齐 artifacts：proposal、specs、design、tasks。
3. 严格校验：`openspec validate --type change <id> --strict`。
4. 实施阶段按 tasks 顺序执行，完成后再勾选。
5. 完成后执行 verify，确认无关键缺陷。
6. 归档：`openspec archive <id>`。

## 输出
- change 进度报告。
- 已完成任务与验证结果。
- 归档路径与同步信息。

## Guardrails
- proposal 阶段禁止业务代码改动。
- tasks 未完成不得伪造勾选。
- 归档前必须明确同步策略（若有 delta specs）。
