## 1. Hash 文档基线（先做）

- [x] 1.1 编写 `docs/design/project.md` 与 `docs/design/component.md`，固定 canonical_id、`sha256(... )[:16]`、父级->子级依赖方向与链路格式。
- [x] 1.2 在文档中定义两类 hash：`module_hash`（模块级）与 `location_hash`（可选，`file:start:end:symbol:commit`）。
- [x] 1.3 定义统一数据结构（record、parents、children、chains、reverse_index）并提供最小示例。

## 2. Hash 索引与链路产物

- [x] 2.1 扫描技术/架构模块（backend/frontend/skills/entrypoints），生成 `artifacts/hash-index.json`。
- [x] 2.2 扫描服务/后台调度/通用模块，生成 `artifacts/hash-chains.json`（含 `Ahash->Bhash->Chash`）。
- [x] 2.3 生成 reverse index，保证输入 hash 可返回完整上下文与上下游链路。

## 3. Skills 复用与接入（引用 hash 文档）

- [ ] 3.1 扫描 `.codex/skills` 与 `.codex/cn/skills`，形成可复用清单（复用/不复用原因）。
- [x] 3.2 定义并落地单一 skill：`jfz-code-path-plan-review`（输入代码路径/模块 hash + next_plan，输出上下文摘要 + 可行性评估 + 下一步建议），统一读取 hash 文档与索引产物。
- [x] 3.3 为该 skill 增加输入输出契约（位置/哈希入参、可行性等级、问题清单、建议步骤、回滚结构、错误码/空结果约定）。

## 4. 兼容“按 hash 指定实现点”

- [ ] 4.1 建立 `module_hash/location_hash -> 文件/符号/候选行区间` 回溯规则，支持从模块级定位到代码实现点。
- [ ] 4.2 增加 location hash 兼容路径：代码移动时基于 `commit + symbol` 回退解析。
- [ ] 4.3 在回溯后自动汇总局部与链路上下文，并对“当前实现方案”输出合理性评估和替代方案建议。

## 5. 校验与交付

- [ ] 5.1 校验 hash 长度/唯一性/依赖方向一致性，修复冲突与孤立节点。
- [ ] 5.2 执行受影响检查并更新交付文档（OpenSpec 工件 + hash 使用说明），准备 apply/verify。
