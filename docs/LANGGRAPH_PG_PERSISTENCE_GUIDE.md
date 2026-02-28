# LangGraph PostgreSQL 持久化方案（DeerFlow）

本文说明如何在 DeerFlow 本地/开发环境中，把 LangGraph 的线程运行状态持久化到 PostgreSQL，并给出当前版本对应的表结构与数据关系。

## 1. 目标与范围

- 目标：解决 `langgraph dev` 重启后线程状态丢失、`thread not found` 等问题。
- 范围：仅覆盖 **LangGraph Checkpointer 持久化**。
- 不在范围：用户文件、技能文件、memory.json 等业务文件（这些仍在本地文件系统）。

## 2. 当前项目数据存储总览

### 2.1 启用 PG Checkpointer 后

- LangGraph 线程/运行状态：**PostgreSQL**（通过 checkpointer）
- 线程工作目录（workspace/uploads/outputs）：`backend/.deer-flow/threads/{thread_id}/user-data/...`
- 全局记忆：`backend/.deer-flow/memory.json`
- Sandbox 映射状态：`backend/.deer-flow/threads/{thread_id}/sandbox.json`

### 2.2 关键结论

- PG 方案只替换“图状态持久化层”，不会替换 DeerFlow 现有文件落盘路径。

## 3. 版本基线（本文表结构对应版本）

- `langgraph-checkpoint-postgres==3.0.4`
- `langgraph==1.0.6`
- `psycopg==3.3.3`

> 表结构来源：`langgraph.checkpoint.postgres.base.MIGRATIONS`（该版本源码）。

## 4. 接入步骤（完整）

### 4.1 启动 PostgreSQL（示例）

```bash
docker run -d --name deerflow-pg \
  -e POSTGRES_USER=deer \
  -e POSTGRES_PASSWORD=deer \
  -e POSTGRES_DB=deerflow \
  -p 5432:5432 \
  postgres:16
```

### 4.2 安装依赖（backend 目录）

```bash
cd backend
uv add langgraph-checkpoint-postgres
```

如果本机缺少 `libpq` 导致 `psycopg` 导入失败，再执行：

```bash
uv add "psycopg[binary]"
```

### 4.3 配置连接串（`backend/.env`）

```env
LANGGRAPH_POSTGRES_URL=postgresql://deer:deer@localhost:5432/deerflow?sslmode=disable
```

### 4.4 新建 `backend/checkpointer.py`

```python
import os
from contextlib import contextmanager

from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = os.environ["LANGGRAPH_POSTGRES_URL"]


def setup_checkpointer() -> None:
    """首次初始化数据库表结构/迁移。"""
    with PostgresSaver.from_conn_string(DB_URI) as saver:
        saver.setup()


@contextmanager
def checkpointer():
    """供 langgraph.json 引用的 checkpointer 工厂。"""
    with PostgresSaver.from_conn_string(DB_URI) as saver:
        yield saver
```

### 4.5 初始化表结构（首次一次即可）

```bash
cd backend
uv run python -c "from checkpointer import setup_checkpointer; setup_checkpointer()"
```

### 4.6 修改 `backend/langgraph.json`

在根级增加 `checkpointer` 字段：

```json
{
  "$schema": "https://langgra.ph/schema.json",
  "dependencies": ["."],
  "env": ".env",
  "graphs": {
    "lead_agent": "src.agents:make_lead_agent"
  },
  "checkpointer": "checkpointer:checkpointer"
}
```

### 4.7 启动

```bash
cd backend
uv run langgraph dev --no-browser --allow-blocking --no-reload
```

## 5. PostgreSQL 表结构（3.0.4）

`setup()` 会自动创建并迁移以下对象。

### 5.1 `checkpoint_migrations`

```sql
CREATE TABLE IF NOT EXISTS checkpoint_migrations (
  v INTEGER PRIMARY KEY
);
```

用途：记录已执行迁移版本。

### 5.2 `checkpoints`

```sql
CREATE TABLE IF NOT EXISTS checkpoints (
  thread_id TEXT NOT NULL,
  checkpoint_ns TEXT NOT NULL DEFAULT '',
  checkpoint_id TEXT NOT NULL,
  parent_checkpoint_id TEXT,
  type TEXT,
  checkpoint JSONB NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}',
  PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
);
```

用途：保存每次 checkpoint 主体（状态快照、元数据）。

### 5.3 `checkpoint_blobs`

```sql
CREATE TABLE IF NOT EXISTS checkpoint_blobs (
  thread_id TEXT NOT NULL,
  checkpoint_ns TEXT NOT NULL DEFAULT '',
  channel TEXT NOT NULL,
  version TEXT NOT NULL,
  type TEXT NOT NULL,
  blob BYTEA,
  PRIMARY KEY (thread_id, checkpoint_ns, channel, version)
);
```

用途：保存 channel 对应的大对象/二进制分片。

### 5.4 `checkpoint_writes`

```sql
CREATE TABLE IF NOT EXISTS checkpoint_writes (
  thread_id TEXT NOT NULL,
  checkpoint_ns TEXT NOT NULL DEFAULT '',
  checkpoint_id TEXT NOT NULL,
  task_id TEXT NOT NULL,
  idx INTEGER NOT NULL,
  channel TEXT NOT NULL,
  type TEXT,
  blob BYTEA NOT NULL,
  PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, idx)
);
```

后续迁移会追加：

```sql
ALTER TABLE checkpoint_writes
ADD COLUMN IF NOT EXISTS task_path TEXT NOT NULL DEFAULT '';
```

用途：保存任务执行过程中的写入记录（pending writes/sends）。

### 5.5 索引

```sql
CREATE INDEX CONCURRENTLY IF NOT EXISTS checkpoints_thread_id_idx ON checkpoints(thread_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS checkpoint_blobs_thread_id_idx ON checkpoint_blobs(thread_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS checkpoint_writes_thread_id_idx ON checkpoint_writes(thread_id);
```

## 6. 数据关系与“存储结构”

逻辑关系（按 thread 聚合）：

- `checkpoints`：一个 `thread_id` 下有多个 `checkpoint_id`（时间序列快照）
- `checkpoint_blobs`：按 `(thread_id, checkpoint_ns, channel, version)` 关联 channel 数据
- `checkpoint_writes`：按 `(thread_id, checkpoint_ns, checkpoint_id, task_id, idx)` 关联任务写入

可理解为：

- 主表：`checkpoints`
- 附件表：`checkpoint_blobs`
- 过程写入表：`checkpoint_writes`

## 7. 验证与排障

### 7.1 验证 SQL

```sql
-- 表是否创建成功
\dt checkpoint*

-- 迁移版本
SELECT * FROM checkpoint_migrations ORDER BY v;

-- 查看某个线程的 checkpoint 数量
SELECT thread_id, count(*)
FROM checkpoints
GROUP BY thread_id
ORDER BY count(*) DESC;
```

### 7.2 常见问题

- `ModuleNotFoundError: langgraph.checkpoint.postgres`
  - 未安装依赖，执行 `uv add langgraph-checkpoint-postgres`

- `ImportError: no pq wrapper available`
  - `psycopg` 缺少可用实现，执行 `uv add "psycopg[binary]"`

- `relation "checkpoints" does not exist`
  - 未执行初始化，运行：
    - `uv run python -c "from checkpointer import setup_checkpointer; setup_checkpointer()"`

- 连接失败（认证/网络）
  - 检查 `LANGGRAPH_POSTGRES_URL`、PG 用户密码、端口映射

## 8. 运维建议（最小可行）

- 使用独立数据库实例，不与业务库混用。
- 对 `checkpoints` 做定期归档/清理（按 thread 或时间）。
- 把 PG 备份纳入日常（`pg_dump` + 保留策略）。
- 线上建议启用连接池与监控（连接数、慢查询、磁盘增长）。
