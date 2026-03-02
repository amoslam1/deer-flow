## Purpose
定义 DeerFlow 在线程级 agent 操作中的 sandbox 生命周期与执行行为基线，确保文件与命令执行可控、可隔离且具备可回收能力。

## Requirements

### Requirement: Thread-Scoped Sandbox Lifecycle
系统 SHALL 为工具执行获取并复用线程级 sandbox 上下文，并在 provider 关闭时释放资源。

#### Scenario: Acquire sandbox for thread
- **WHEN** 线程执行请求开始
- **THEN** sandbox provider 获取或复用绑定到该线程上下文的 sandbox
- **AND** 执行中间件可获得 sandbox 标识符

#### Scenario: Shutdown provider
- **WHEN** 触发 sandbox provider shutdown
- **THEN** 释放活动 sandbox 资源
- **AND** 重置 provider 单例缓存

### Requirement: Sandbox File and Command Operations
系统 SHALL 通过已配置 sandbox tools 支持受控的文件读写与命令执行。

#### Scenario: Execute allowed sandbox tool
- **WHEN** agent 调用 `ls`、`read_file`、`write_file`、`str_replace`、`bash` 等已配置工具
- **THEN** 操作在 sandbox 边界内执行
- **AND** 结果返回给 agent 工作流

#### Scenario: Upload file becomes sandbox-accessible
- **WHEN** 用户向线程上传文件
- **THEN** 文件保存到线程 uploads 范围
- **AND** 返回可供后续工具访问的虚拟 sandbox 路径元数据
