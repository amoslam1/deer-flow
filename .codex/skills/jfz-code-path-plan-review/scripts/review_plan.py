#!/usr/bin/env python3
"""Resolve context by code path/hash and evaluate next-step plan feasibility."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

HEX16_RE = re.compile(r"^[0-9a-f]{16}$")
LINE_RANGE_RE = re.compile(r"^(?P<path>.+?):(?P<start>\d+)-(?P<end>\d+)$")


def detect_repo_root() -> Path:
    candidates = [Path.cwd(), Path(__file__).resolve()]
    for base in candidates:
        for p in [base, *base.parents]:
            if (p / "artifacts" / "hash-index.json").exists():
                return p
    raise FileNotFoundError("Cannot find repo root containing artifacts/hash-index.json")


def sha16(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_target_hash(target: str, records: list[dict], reverse_index: dict) -> tuple[str | None, str]:
    if HEX16_RE.match(target) and target in reverse_index:
        return target, "hash"

    by_cid = {r["canonical_id"]: r for r in records}
    if target in by_cid:
        return by_cid[target]["hash"], "canonical_id"

    m = LINE_RANGE_RE.match(target)
    if m:
        target = m.group("path")

    rel_target = target.lstrip("./")
    by_path = [r for r in records if isinstance(r.get("path"), str) and rel_target.startswith(r["path"])]
    if by_path:
        best = sorted(by_path, key=lambda x: len(x["path"]), reverse=True)[0]
        return best["hash"], "path-prefix"

    return None, "unresolved"


def evaluate_feasibility(next_plan: str, dependency_count: int) -> tuple[str, list[str], list[str], str]:
    issues: list[str] = []
    next_steps: list[str] = []
    rollback = "保留当前分支与变更点，若评估后执行失败则按受影响 hash 链逐步回退。"

    if not next_plan.strip():
        issues.append("未提供 next_plan，无法做完整可行性评估。")
        next_steps.append("补充 next_plan，至少包含改动目标、影响范围和验证方式。")
        return "medium", issues, next_steps, rollback

    plan = next_plan.lower()
    risky_words = ["delete", "remove", "rename", "migrate", "删除", "重命名", "迁移", "替换"]
    safe_words = ["add", "新增", "补充", "文档", "test", "测试", "校验"]

    if any(w in plan for w in risky_words) and dependency_count >= 4:
        feasibility = "low"
        issues.append("计划包含高风险动作且依赖链较长，可能引发跨模块回归。")
    elif any(w in plan for w in safe_words) and dependency_count <= 6:
        feasibility = "high"
    else:
        feasibility = "medium"

    if "skip test" in plan or "不测" in plan or "不测试" in plan:
        issues.append("计划包含跳过测试，存在回归风险。")
        feasibility = "low" if feasibility == "medium" else feasibility

    next_steps.extend(
        [
            "先按 dependency_paths 识别直接上下游模块。",
            "先改最小范围并补充受影响路径测试。",
            "完成后复查是否影响相邻 hash 节点的输入输出契约。",
        ]
    )
    return feasibility, issues, next_steps, rollback


def main() -> None:
    parser = argparse.ArgumentParser(description="Review code path/hash context and plan feasibility.")
    parser.add_argument("--target", required=True, help="hash / canonical_id / file / file:start-end")
    parser.add_argument("--next-plan", default="", help="Proposed next implementation steps")
    parser.add_argument("--max-paths", type=int, default=8, help="Max dependency paths to output")
    args = parser.parse_args()

    root = detect_repo_root()
    idx = load_json(root / "artifacts" / "hash-index.json")
    chs = load_json(root / "artifacts" / "hash-chains.json")

    records = idx.get("records", [])
    reverse = idx.get("reverse_index", {})
    chain_reverse = chs.get("reverse_index", {})

    target_hash, resolved_by = resolve_target_hash(args.target, records, reverse)
    if not target_hash:
        result = {
            "target": {"input": args.target, "resolved_by": resolved_by},
            "feasibility": "low",
            "issues": ["target 无法解析到有效 hash。"],
            "next_steps": ["检查输入路径/行区间是否存在，或改用已知模块 hash。"],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    node = reverse[target_hash]
    chain_info = chain_reverse.get(target_hash, {"upstream_chains": [], "downstream_chains": []})
    paths = chain_info.get("upstream_chains", []) + chain_info.get("downstream_chains", [])
    paths = list(dict.fromkeys(paths))[: args.max_paths]

    feasibility, issues, next_steps, rollback = evaluate_feasibility(args.next_plan, len(paths))
    context_summary = (
        f"命中节点 {node.get('canonical_id')} ({target_hash})，"
        f"parents={len(node.get('parents', []))}，children={len(node.get('children', []))}。"
    )

    result = {
        "target": {
            "input": args.target,
            "resolved_by": resolved_by,
            "hash": target_hash,
            "canonical_id": node.get("canonical_id"),
            "path": node.get("path"),
            "type": node.get("type"),
        },
        "context_summary": context_summary,
        "dependency_paths": paths,
        "feasibility": feasibility,
        "issues": issues,
        "next_steps": next_steps,
        "rollback": rollback,
        "data_sources": {
            "project_doc": str(root / "docs" / "design" / "project.md"),
            "component_doc": str(root / "docs" / "design" / "component.md"),
            "hash_index": str(root / "artifacts" / "hash-index.json"),
            "hash_chains": str(root / "artifacts" / "hash-chains.json"),
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
