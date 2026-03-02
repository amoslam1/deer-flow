---
name: openspec-onboard
description: Guided onboarding for OpenSpec - walk through a complete workflow cycle with narration and real codebase work.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.2.0"
---

引导用户完成一次完整 OpenSpec 新手流程（从想法到归档）。

目标不是“讲理论”，而是“边做边学”。

---

## 预检

先检查 CLI：

```bash
# Unix/macOS
openspec --version 2>&1 || echo "CLI_NOT_INSTALLED"
```

若未安装：
> OpenSpec CLI 未安装，请先安装后再执行 `/opsx:onboard`。

---

## Phase 1: Welcome

向用户说明本次演练内容：
1. 选一个小而真实的任务
2. 快速探索问题
3. 创建 change
4. 完成 proposal → specs → design → tasks
5. 实施任务
6. 归档变更

建议用时：15-20 分钟。

---

## Phase 2: 选任务

### 代码库扫描（找小切口）

建议搜索：
- `TODO` / `FIXME` / `HACK` / `XXX`
- 吞异常或薄弱错误处理
- 缺测试的关键函数
- TypeScript 中 `any` 滥用
- 非调试场景残留 `console.log/debugger`
- 输入校验不足点

也可看最近提交：

```bash
git log --oneline -10 2>/dev/null || echo "No git history"
```

### 给出 3-4 个可选任务

每个建议要包含：
- 文件位置
- 预估改动范围（文件数/行数）
- 为什么适合做首次 OpenSpec 演练

若找不到明显切口，就直接问用户“最想先修哪个小问题”。

### 范围护栏（软约束）

如果用户选了过大的任务：
- 先建议切更小范围
- 也允许用户坚持原任务
- 明确告知：首次演练建议小而完整的闭环

---

## Phase 3: Explore 演示

在建 change 前先展示 explore 思维：
- 读取相关代码
- 给出简要分析
- 必要时画 ASCII 图

输出后**暂停**，等用户确认再进入下一步。

---

## Phase 4: 创建 Change

说明 change 的意义：
- 它是本次工作的容器
- 目录在 `openspec/changes/<name>/`
- 包含 proposal/specs/design/tasks

执行：

```bash
openspec new change "<derived-name>"
```

展示目录结构并说明下一步先写 proposal。

---

## Phase 5: Proposal

解释：proposal 关注 **WHY + WHAT**（不是 HOW）。

先草拟，再向用户确认，确认后写入：
- `openspec/changes/<name>/proposal.md`

建议通过：
```bash
openspec instructions proposal --change "<name>" --json
```
获取模板与约束。

**暂停**：等待用户确认草案。

---

## Phase 6: Specs

解释：spec 定义“系统应该做什么”，必须可测试。

按能力创建 delta spec：

```bash
mkdir -p openspec/changes/<name>/specs/<capability>
```

写入格式：
- `## ADDED Requirements`
- `### Requirement: ...`
- `#### Scenario: ...`
- `WHEN / THEN / AND`

---

## Phase 7: Design

解释：design 定义 **HOW**，用于记录关键决策与取舍。

小变更可简写，但至少覆盖：
- Context
- Goals / Non-Goals
- Decisions
- Risks / Trade-offs

---

## Phase 8: Tasks

解释：tasks 是 apply 阶段的执行清单。

要求：
- 分组编号（`## 1.`、`## 2.`）
- 每项必须是 checkbox：`- [ ] X.Y ...`
- 可验证、可完成、顺序清晰

草拟后**暂停**，确认用户准备进入实现。

---

## Phase 9: Apply（实施）

实施节奏：
1. 公布当前任务
2. 实施最小改动
3. 必要时引用 specs/design 决策
4. 任务完成后勾选 `- [x]`
5. 简短汇报并继续下一个

全部完成后给出完成汇总。

---

## Phase 10: Archive（归档）

解释归档价值：
- 把 change 迁移到历史目录
- 形成可追溯决策记录

执行：

```bash
openspec archive "<name>"
```

展示归档路径：
`openspec/changes/archive/YYYY-MM-DD-<name>/`

---

## Phase 11: 复盘与下一步

总结完整节奏：
1. Explore
2. New
3. Proposal
4. Specs
5. Design
6. Tasks
7. Apply
8. Archive

并给出命令速查：
- `/opsx:propose`
- `/opsx:explore`
- `/opsx:apply`
- `/opsx:archive`
- `/opsx:new`
- `/opsx:continue`
- `/opsx:ff`
- `/opsx:verify`

---

## 退出处理（Graceful Exit）

### 中途暂停

若用户要暂停：
- 告知 change 已保存路径
- 提示后续可用：
  - `/opsx:continue <name>`
  - `/opsx:apply <name>`

### 只想看命令

直接给简版命令清单，不强推教程流程。

---

## Guardrails

- 在关键节点遵循 **EXPLAIN → DO → SHOW → PAUSE**
- 实施阶段讲解要简洁，不要逐行说教
- 不跳阶段（onboard 目标是让用户体验完整闭环）
- 有暂停点就暂停，不抢用户控制权
- 用真实代码库任务，不做虚构示例
- 适度引导范围变小，但尊重用户选择
