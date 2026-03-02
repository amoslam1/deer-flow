# OpenSpec 命令速查（Codex 版）

只用这 7 条命令就够了（`<change-id>` 用你的名字替换，例如 `add-user-login`）。

## 标准顺序

1. 创建：`$openspec-new-change <change-id>`
2. 一步生成 proposal/specs/design/tasks：`$openspec-propose <change-id>`
3. 继续补齐下一个 artifact：`$openspec-continue-change <change-id>`
4. 执行实现（按 tasks）：`$openspec-apply-change <change-id>`
5. 验证实现与工件一致：`$openspec-verify-change <change-id>`
6. 归档：`$openspec-archive-change <change-id>`
7. 仅同步 specs（不归档）：`$openspec-sync-specs <change-id>`

## 命令说明

1. `$openspec-new-change <change-id>`
创建 change 目录，初始化 OpenSpec 流程。

2. `$openspec-propose <change-id>`
一次性生成可实施工件（proposal/specs/design/tasks）。

3. `$openspec-continue-change <change-id>`
每次只推进一个 artifact，适合分步补文档。

4. `$openspec-apply-change <change-id>`
按 `tasks.md` 执行实现并更新任务勾选。

5. `$openspec-verify-change <change-id>`
检查实现是否覆盖 tasks/specs/design，归档前建议执行。

6. `$openspec-archive-change <change-id>`
归档 change，并把 delta specs 同步到 `openspec/specs`。

7. `$openspec-sync-specs <change-id>`
只同步 specs，不归档 change（change 保持 active）。

## 最短示例

```bash
$openspec-new-change add-user-login
$openspec-propose add-user-login
$openspec-apply-change add-user-login
$openspec-verify-change add-user-login
$openspec-archive-change add-user-login
```

## `openspec/specs` 写入与校验

1. 写入（不归档）：
`$openspec-sync-specs <change-id>`
作用：把 `openspec/changes/<change-id>/specs/*` 同步到 `openspec/specs/*`，但 change 仍保持 active。

2. 写入（并归档）：
`$openspec-archive-change <change-id>`
作用：归档 change 时同步 specs 到 `openspec/specs/*`，适合收尾阶段一次完成。

3. 校验主 specs：
`openspec validate --specs --strict --no-interactive`
作用：严格校验 `openspec/specs` 目录下所有 spec 文件结构与规则是否合规。
