# 本地 Tool 与 MCP 接入导读

## 本地 Tool 当前代码

```text
app/tools/base.py
app/tools/builtin.py
app/container.py
```

`Tool` Protocol 定义最小契约，`ToolRegistry` 通过 `tool_id@version` 注册，`TextStatsTool` 是可运行示例，`container.py` 是当前依赖装配位置。

## 新增本地 Tool 的步骤

1. 在 `app/tools/` 实现新类。
2. 声明稳定 `id` 和 `version`。
3. 接收 `arguments` 与 `ToolContext`。
4. 返回 `ToolResult`，不要向调用者泄漏任意异常。
5. 在 `container.py` 注册。
6. 在模块 `module.yaml` 的 allowlist 中声明。
7. 增加输入输出 JSON Schema。
8. 增加 TOOL Case ID 和测试。

示意：

```python
class MyTool:
    id = "my-tool"
    version = "1.0.0"

    def execute(self, arguments, context):
        # 先校验 arguments，再执行受限业务动作。
        return ToolResult(ok=True, data={"result": "..."})
```

## Tool 安全边界

Tool 不应默认拥有：

```text
任意文件读取
任意网络访问
任意子进程执行
生产 Secret
跨租户数据
```

后续应建设 Tool Gateway，统一处理 Schema、权限、超时、重试、沙箱、审计和脱敏。

## MCP 当前代码

```text
app/tools/mcp.py
```

当前只有 `MCPClient` Protocol 和 `NoopMCPClient`。这说明接口边界已经预留，但真实 MCP 连接、发现、认证、调用和审计**尚未实现**。

## MCP 正确接入方式

```text
Orchestrator
→ Tool Gateway
→ MCP Adapter
→ MCP Client Gateway
→ Approved MCP Server
```

MCP Gateway 必须负责：

```text
Server Registry
Tool Discovery Snapshot
用户和模块权限交集
输入 Schema 校验
调用超时和熔断
Secret 按次注入
输出 Schema 和内容扫描
Call Audit
```

不要让 Orchestrator 直接连接任意 MCP URL，也不要允许文档内容动态添加 MCP Server。
