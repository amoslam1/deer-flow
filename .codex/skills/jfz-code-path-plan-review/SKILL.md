---
name: jfz-code-path-plan-review
description: 输入代码路径或 hash，自动汇总上下文与 Ahash->Bhash 依赖链，并评估下一步计划可行性与风险。
license: MIT
compatibility: Requires Python 3.10+ and repository hash artifacts.
metadata:
  author: deerflow
  version: "1.0"
---

# JFZ Code Path Plan Review

## Overview

当用户给出代码路径、行区间或 hash，并希望判断“下一步计划是否可行”时使用本技能。
技能会读取 `artifacts/hash-index.json` 和 `artifacts/hash-chains.json`，输出结构化上下文与可行性评估。

## When To Use

- 用户说“看这个文件/这几行的上下文”。
- 用户说“这个修改计划是否可行，有什么风险”。
- 用户只给 hash，希望回溯影响路径并给下一步建议。

## Inputs

- `target`:
  - `module_hash` / `location_hash`
  - `file:start-end`（如 `backend/src/gateway/app.py:1-120`）
  - `file`（如 `frontend/src/core/api/api-client.ts`）
- `next_plan`: 用户下一步计划（建议提供）
- 可选 `depth`: 依赖链深度（默认 2）

## Workflow

1. 解析 `target` 并解析为目标 hash。
2. 在 `artifacts/hash-index.json` 获取目标节点、parents、children。
3. 在 `artifacts/hash-chains.json` 获取上下游 `Ahash->Bhash` 路径。
4. 结合 `docs/design/project.md` + `docs/design/component.md` 汇总业务与技术上下文。
5. 评估 `next_plan` 可行性并输出问题、建议步骤与回滚建议。

## Command

```bash
python .codex/skills/jfz-code-path-plan-review/scripts/review_plan.py \
  --target "backend/src/gateway/app.py:1-120" \
  --next-plan "新增参数校验并补充对应测试"
```

## Output Contract

- `target`: 命中节点（hash、canonical_id、path）
- `context_summary`: 上下文摘要
- `dependency_paths`: 关键 `Ahash->Bhash` 链路
- `feasibility`: `high|medium|low`
- `issues`: 风险与缺失项
- `next_steps`: 推荐执行步骤
- `rollback`: 回滚建议

## Guardrails

- 若无法解析 target，必须明确说明原因，不得编造路径。
- 输出至少 1 条有效 hash 依赖链；若无链路需显式标注。
- 不自动改代码，除非用户明确要求进入实现。
- 评估结论必须附带依据（命中的依赖路径或上下文证据）。

## References

- `references/data-sources.md`
- `references/output-contract.md`
- `docs/design/project.md`
- `docs/design/component.md`
