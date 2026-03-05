---
name: regression-check-runner
description: Run minimal regression checks based on changed files and report actionable failures.
license: MIT
compatibility: Requires git diff and project test/lint commands.
metadata:
  author: deerflow
  version: "1.0"
---

根据变更范围执行“最小充分”回归检查。

## 使用场景
- 提交前快速回归。
- 变更范围跨后端/前端/配置文件。

## 输入
- 变更文件列表（默认读取 git status/diff）。
- 可选：强制执行的检查项。

## 执行步骤
1. 分类改动：backend / frontend / config / docs。
2. 生成最小检查命令集：
   - backend: `uv run pytest`（可按模块缩小）
   - frontend: `pnpm lint`、`pnpm typecheck`
   - config: 启动与配置一致性检查
3. 执行并采集失败输出。
4. 将失败映射到相关文件与可能原因。
5. 输出“可提交/需修复”结论。

## 输出
- 检查命令与结果摘要。
- 失败项定位与修复建议。

## Guardrails
- 不默认执行超长全量测试（除非用户要求）。
- 失败必须保留原始关键信息。
- 不自动忽略失败。
