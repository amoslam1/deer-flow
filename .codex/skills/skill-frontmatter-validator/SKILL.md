---
name: skill-frontmatter-validator
description: Validate SKILL.md frontmatter structure and required metadata keys for Codex and runtime skills.
license: MIT
compatibility: Requires YAML parser and filesystem access.
metadata:
  author: deerflow
  version: "1.0"
---

校验 `SKILL.md` frontmatter 结构与元数据完整性。

## 使用场景
- 新建或修改 Skills 后。
- 合并前做技能质量门禁。

## 输入
- 目标目录（如 `.codex/skills`、`skills/public`、`skills/custom`）。

## 执行步骤
1. 遍历目标目录下所有 `SKILL.md`。
2. 校验 frontmatter 是否存在且 YAML 可解析。
3. 校验必填键：`name`、`description`、`license`、`compatibility`、`metadata`。
4. 检查 name 命名规范（kebab-case）。
5. 输出逐文件通过/失败结果与修复建议。

## 输出
- 校验报告（通过数/失败数）。
- 失败明细与定位路径。

## Guardrails
- 不自动改写正文语义。
- 失败项必须逐条列出，不可静默。
- 默认只做读操作，修复需明确授权。
