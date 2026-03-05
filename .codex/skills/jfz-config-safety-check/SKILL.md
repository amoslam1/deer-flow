---
name: config-safety-check
description: Check configuration safety and consistency across config.yaml, .env, and extensions files.
license: MIT
compatibility: Requires access to project config files.
metadata:
  author: deerflow
  version: "1.0"
---

配置安全与一致性检查。

## 使用场景
- 修改 `config.yaml/.env/extensions_config.json` 前后。
- 环境切换（本地、Docker、Provisioner）时。

## 输入
- 目标配置文件范围。
- 可选：严格模式（敏感信息一票否决）。

## 执行步骤
1. 检查敏感字段是否明文（API key/token/password）。
2. 检查关键配置完整性（models、sandbox、skills 路径）。
3. 检查路径存在性和端口冲突风险。
4. 检查 `.env` 与 `config.yaml` 的变量引用一致性。
5. 输出风险等级与修复建议。

## 输出
- 配置风险报告（高/中/低）。
- 修复建议与优先级。

## Guardrails
- 不在日志中输出完整敏感值。
- 不自动改写配置，仅给建议。
- 高风险项必须阻断“直接提交”结论。
