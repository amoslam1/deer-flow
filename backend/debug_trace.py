#!/usr/bin/env python
"""
Step-by-step LangGraph trace debugger for lead_agent.

This script streams graph execution events so you can see:
- Which node/middleware/tool runs at each step
- The update/result of each step
- Custom stream events (e.g. task_started/task_running/task_completed)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Ensure we can import from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agents import make_lead_agent


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Trace LangGraph step execution for lead_agent.")
    parser.add_argument("--thread-id", default="debug-thread-001", help="Thread id for this debug session.")
    parser.add_argument("--model-name", default="kimi-k2.5", help="Runtime model name.")
    parser.add_argument(
        "--stream-modes",
        default="tasks,updates,custom,values",
        help="Comma-separated stream modes. Example: tasks,updates,custom,values,messages,debug",
    )
    parser.add_argument("--plan-mode", action="store_true", help="Enable plan mode.")
    parser.add_argument("--thinking-enabled", action="store_true", help="Enable thinking mode.")
    parser.add_argument("--subagent-enabled", action="store_true", help="Enable subagent task tool.")
    parser.add_argument("--subgraphs", action="store_true", help="Include subgraph events in stream output.")
    parser.add_argument("--max-chars", type=int, default=1600, help="Max chars to print per event payload.")
    parser.add_argument("--recursion-limit", type=int, default=80, help="Graph recursion limit per turn.")
    parser.add_argument("--once", default="", help="Run a single prompt and exit.")
    parser.add_argument(
        "--thread-log-root",
        default="",
        help="Directory for per-thread trace files. Default: <repo>/logs/thread-traces",
    )
    parser.add_argument(
        "--disable-thread-files",
        action="store_true",
        help="Disable writing per-thread log and graph markdown files.",
    )
    return parser.parse_args()


def _safe_json(value: Any, max_chars: int) -> str:
    text = json.dumps(value, ensure_ascii=False, default=str, indent=2)
    if len(text) <= max_chars:
        return text
    return f"{text[:max_chars]}... <truncated {len(text) - max_chars} chars>"


def _content_preview(content: Any, max_chars: int = 180) -> str:
    if isinstance(content, str):
        return content[:max_chars]
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(str(block.get("text", "")))
                else:
                    parts.append(str(block))
            else:
                parts.append(str(block))
        merged = "\n".join(parts)
        return merged[:max_chars]
    return str(content)[:max_chars]


def _summarize_values(data: dict[str, Any]) -> str:
    messages = data.get("messages", [])
    last_message = messages[-1] if messages else None

    msg_type = getattr(last_message, "type", None) if last_message is not None else None
    msg_content = getattr(last_message, "content", None) if last_message is not None else None

    summary = {
        "message_count": len(messages),
        "last_message_type": msg_type,
        "last_message_preview": _content_preview(msg_content),
        "has_title": "title" in data and bool(data.get("title")),
        "artifacts_count": len(data.get("artifacts", []) or []),
        "has_thread_data": bool(data.get("thread_data")),
        "has_sandbox": bool(data.get("sandbox")),
    }
    return _safe_json(summary, max_chars=1200)


def _print_event(
    index: int,
    mode: str,
    data: Any,
    max_chars: int,
    namespace: tuple | None = None,
    emit=print,
) -> None:
    ns = f"[ns={'/'.join(namespace)}] " if namespace else ""

    if mode == "messages":
        if isinstance(data, tuple) and len(data) == 2:
            token, metadata = data
            token_text = _content_preview(getattr(token, "content", token), max_chars=120)
            node_name = metadata.get("langgraph_node") if isinstance(metadata, dict) else None
            if token_text:
                emit(f"[{index:04d}] {ns}mode=messages node={node_name} token={token_text!r}")
            return
        emit(f"[{index:04d}] {ns}mode=messages data={_safe_json(data, max_chars)}")
        return

    if mode == "values" and isinstance(data, dict):
        emit(f"[{index:04d}] {ns}mode=values summary={_summarize_values(data)}")
        return

    if mode == "tasks" and isinstance(data, dict):
        name = data.get("name")
        task_id = data.get("id")
        if "input" in data:
            emit(f"[{index:04d}] {ns}mode=tasks status=start name={name} id={task_id}")
        elif "result" in data or "error" in data:
            status = "error" if data.get("error") else "done"
            payload = {"result": data.get("result"), "error": data.get("error"), "interrupts": data.get("interrupts")}
            emit(f"[{index:04d}] {ns}mode=tasks status={status} name={name} id={task_id} payload={_safe_json(payload, max_chars)}")
        else:
            emit(f"[{index:04d}] {ns}mode=tasks data={_safe_json(data, max_chars)}")
        return

    emit(f"[{index:04d}] {ns}mode={mode} data={_safe_json(data, max_chars)}")


def _normalize_stream_modes(raw: str) -> list[str]:
    modes = [part.strip() for part in raw.split(",") if part.strip()]
    if not modes:
        return ["tasks", "updates", "custom", "values"]
    return modes


def _sanitize_for_filename(value: str) -> str:
    safe = []
    for ch in value:
        if ch.isalnum() or ch in ("-", "_"):
            safe.append(ch)
        else:
            safe.append("_")
    return "".join(safe)


def _resolve_trace_paths(thread_id: str, user_root: str) -> tuple[Path, Path]:
    project_root = Path(__file__).resolve().parent.parent
    root = Path(user_root).expanduser().resolve() if user_root else (project_root / "logs" / "thread-traces")
    root.mkdir(parents=True, exist_ok=True)

    safe_thread_id = _sanitize_for_filename(thread_id)
    trace_log_path = root / f"langgraph_{safe_thread_id}.log"
    graph_md_path = root / f"langgraph_{safe_thread_id}_graph.md"
    return trace_log_path, graph_md_path


def _write_graph_markdown(
    path: Path,
    *,
    thread_id: str,
    model_name: str,
    stream_modes: list[str],
    run_config: dict[str, Any],
    mermaid_text: str,
) -> None:
    content = (
        "# LangGraph Build Snapshot\n\n"
        f"- generated_at: {datetime.now().isoformat(timespec='seconds')}\n"
        f"- thread_id: `{thread_id}`\n"
        f"- model_name: `{model_name}`\n"
        f"- stream_modes: `{','.join(stream_modes)}`\n\n"
        "## Run Config\n\n"
        "```json\n"
        f"{json.dumps(run_config, ensure_ascii=False, indent=2, default=str)}\n"
        "```\n\n"
        "## Mermaid Graph\n\n"
        "```mermaid\n"
        f"{mermaid_text}\n"
        "```\n"
    )
    path.write_text(content, encoding="utf-8")


async def main() -> None:
    args = _parse_args()
    load_dotenv()

    try:
        from src.mcp import initialize_mcp_tools

        await initialize_mcp_tools()
    except Exception as e:
        print(f"Warning: MCP initialization failed: {e}")

    stream_modes = _normalize_stream_modes(args.stream_modes)
    run_config = {
        "recursion_limit": args.recursion_limit,
        "configurable": {
            "thread_id": args.thread_id,
            "model_name": args.model_name,
            "thinking_enabled": args.thinking_enabled,
            "is_plan_mode": args.plan_mode,
            "subagent_enabled": args.subagent_enabled,
        },
    }

    agent = make_lead_agent(run_config)
    trace_file = None
    graph_file = None
    file_handle = None

    def emit(msg: str) -> None:
        print(msg)
        if file_handle is not None:
            file_handle.write(msg + "\n")
            file_handle.flush()

    if not args.disable_thread_files:
        trace_file, graph_file = _resolve_trace_paths(args.thread_id, args.thread_log_root)
        file_handle = trace_file.open("a", encoding="utf-8")
        emit("")
        emit("=" * 88)
        emit(
            "[TRACE_SESSION] "
            f"started_at={datetime.now().isoformat(timespec='seconds')} "
            f"thread_id={args.thread_id} model_name={args.model_name}"
        )
        emit("=" * 88)

        mermaid = agent.get_graph().draw_mermaid()
        _write_graph_markdown(
            graph_file,
            thread_id=args.thread_id,
            model_name=args.model_name,
            stream_modes=stream_modes,
            run_config=run_config,
            mermaid_text=mermaid,
        )

    emit("=" * 72)
    emit("LangGraph Trace Debugger")
    emit(f"thread_id={args.thread_id}")
    emit(f"model_name={args.model_name}")
    emit(f"stream_modes={stream_modes}")
    if trace_file and graph_file:
        emit(f"thread_trace_log={trace_file}")
        emit(f"thread_graph_md={graph_file}")
    emit("Type 'quit' or 'exit' to stop.")
    emit("=" * 72)

    turn = 0
    try:
        if args.once:
            state = {"messages": [HumanMessage(content=args.once)]}
            emit("\n--- Turn 1 stream begin ---")
            event_index = 0
            try:
                async for chunk in agent.astream(
                    state,
                    config=run_config,
                    context={"thread_id": args.thread_id},
                    stream_mode=stream_modes,
                    subgraphs=args.subgraphs,
                ):
                    event_index += 1
                    if isinstance(chunk, tuple) and len(chunk) == 2:
                        mode, data = chunk
                        _print_event(event_index, str(mode), data, args.max_chars, emit=emit)
                    elif isinstance(chunk, tuple) and len(chunk) == 3:
                        namespace, mode, data = chunk
                        ns_tuple = tuple(namespace) if isinstance(namespace, tuple) else (str(namespace),)
                        _print_event(event_index, str(mode), data, args.max_chars, namespace=ns_tuple, emit=emit)
                    else:
                        _print_event(event_index, "single", chunk, args.max_chars, emit=emit)
                emit(f"--- Turn 1 stream end, events={event_index} ---")
            except Exception as e:
                emit(f"[TraceError] {type(e).__name__}: {e}")
            return

        while True:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"quit", "exit"}:
                emit(
                    "[TRACE_SESSION] "
                    f"ended_at={datetime.now().isoformat(timespec='seconds')} "
                    f"thread_id={args.thread_id}"
                )
                break

            turn += 1
            state = {"messages": [HumanMessage(content=user_input)]}
            emit(f"\n--- Turn {turn} stream begin ---")
            event_index = 0

            try:
                async for chunk in agent.astream(
                    state,
                    config=run_config,
                    context={"thread_id": args.thread_id},
                    stream_mode=stream_modes,
                    subgraphs=args.subgraphs,
                ):
                    event_index += 1

                    # (mode, data)
                    if isinstance(chunk, tuple) and len(chunk) == 2:
                        mode, data = chunk
                        _print_event(event_index, str(mode), data, args.max_chars, emit=emit)
                        continue

                    # (namespace, mode, data) when subgraphs=True and multi-mode stream
                    if isinstance(chunk, tuple) and len(chunk) == 3:
                        namespace, mode, data = chunk
                        ns_tuple = tuple(namespace) if isinstance(namespace, tuple) else (str(namespace),)
                        _print_event(event_index, str(mode), data, args.max_chars, namespace=ns_tuple, emit=emit)
                        continue

                    # single-mode stream fallback
                    _print_event(event_index, "single", chunk, args.max_chars, emit=emit)

                emit(f"--- Turn {turn} stream end, events={event_index} ---")
            except Exception as e:
                emit(f"[TraceError] {type(e).__name__}: {e}")
    finally:
        if file_handle is not None and not file_handle.closed:
            file_handle.close()


if __name__ == "__main__":
    asyncio.run(main())
