---
name: artifact-upload-flow
description: Validate and optimize the end-to-end upload and artifact access workflow across gateway and frontend.
license: MIT
compatibility: Requires gateway upload/artifact APIs and frontend artifact loaders.
metadata:
  author: deerflow
  version: "1.0"
---

上传与产物访问链路专项检查技能。

## 使用场景
- 修改上传接口或 artifact 读取逻辑后。
- 出现上传成功但预览/下载失败的问题。

## 输入
- 目标 thread_id。
- 文件类型样例（文本、二进制、可转换文档）。

## 执行步骤
1. 校验上传接口：`POST /api/threads/{thread_id}/uploads`。
2. 校验列表与删除接口。
3. 校验 artifact URL 解析与返回类型（text/html/binary）。
4. 校验前端 `core/artifacts` loader 与 URL 拼接逻辑。
5. 输出端到端验证结果与改进建议。

## 输出
- 上传链路健康报告。
- 失败请求与定位路径。
- 回归脚本建议。

## Guardrails
- 禁止越权路径访问测试。
- 二进制文件验证必须包含 MIME 检查。
- 不改变业务数据，仅做读/测。
