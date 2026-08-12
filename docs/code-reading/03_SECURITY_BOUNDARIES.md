# 安全边界代码导读

## 当前已经存在的边界

### API Key 示例边界

```text
app/api/dependencies.py
```

当 `TRD_REQUIRE_API_KEY=true` 时比较 `X-API-Key`。这只是开发级示例，生产环境应替换为 OIDC、RBAC 和 ABAC。

### Artifact 路径边界

```text
app/infrastructure/artifact_store.py
```

写入前拒绝绝对路径和 `..`，再使用 `resolve()` 检查目标是否仍在 Artifact Root 内。这是防止 Path Traversal 的关键边界。

### Module 资源路径边界

```text
app/services/module_registry.py:read_relative
```

模块配置中的 Prompt 或 Schema 路径被视为不可信输入，必须保证规范化后仍位于模块目录内。

### Schema 边界

```text
app/validators/schema_validator.py
```

模型、Tool 或 MCP 的输出不能直接进入下游，必须先匹配结构化契约。

## 当前尚未落实的边界

- 文件病毒扫描和真实 MIME 检测。
- 上传大小、压缩炸弹和 OCR 资源限制。
- Tool 沙箱、网络出口和文件系统白名单。
- MCP Server 登记、权限、超时和 Secret 注入。
- Prompt Injection 内容分区和指令优先级。
- 日志、模型输入和报告的统一脱敏。
- 多租户数据隔离。

## Prompt Injection 处理原则

```text
平台规则 > 模块规则 > 用户任务指令 > 文档内容
```

TRD 文档中的“忽略之前指令”必须被视为文档数据，不能成为系统指令。Tool 和 MCP 返回文本同样是不可信数据。
