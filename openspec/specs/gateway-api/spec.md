## Purpose
定义 DeerFlow 网关 API 在模型元数据、配置管理与线程级文件访问方面的基线契约，确保前后端与代理流程在统一接口语义下稳定协作。

## Requirements

### Requirement: Gateway Endpoint Coverage
网关 SHALL 提供模型元数据、MCP 配置、记忆访问、技能管理、artifact 访问与文件上传相关 HTTP API。

#### Scenario: Query model list
- **WHEN** 客户端调用 `GET /api/models`
- **THEN** 网关返回已配置模型元数据
- **AND** 响应不包含 API key 等敏感字段

#### Scenario: Query skills list
- **WHEN** 客户端调用 `GET /api/skills`
- **THEN** 网关返回 public 与 custom skills 及其 enabled 状态

### Requirement: Artifact Access Resolution
网关 SHALL 将线程级虚拟路径解析为安全的 artifact 响应，并拒绝无效路径访问。

#### Scenario: Access valid artifact
- **WHEN** 客户端请求线程下存在的 artifact 路径
- **THEN** 网关返回内容并附带合适的 MIME type

#### Scenario: Path traversal attempt
- **WHEN** 客户端提交超出允许线程 artifact 范围的路径
- **THEN** 网关以访问错误拒绝请求
