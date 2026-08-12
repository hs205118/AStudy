# AStudy 教学注释版：从这里开始

## 1. 先建立两个事实

第一，当前仓库是一个**可运行的 Agent 平台骨架**，不是完成态产品。它已经实现 Run、IR、Artifact、模块配置、校验和 Tool/MCP 接口，但真实模型、Reference、分层 Memory、MCP Gateway 和企业级安全治理仍需继续建设。

第二，代码中的“用户输入”不等于“用户 Memory”。当前 `RunRecord.input_text` 和 `RunRecord.parameters` 只是单次 Run 的输入。仓库目前没有正式的 User Memory 持久化服务。

## 2. 正确阅读顺序

```text
README.md
→ pyproject.toml
→ app/main.py
→ app/config.py
→ app/container.py
→ app/api/routes/runs.py
→ app/domain/schemas.py
→ app/infrastructure/database.py
→ app/services/run_service.py
→ app/core/state_machine.py
→ app/services/module_registry.py
→ modules/storage-wizard/module.yaml
→ modules/storage-wizard/prompts/system.md
→ app/services/model_provider.py
→ app/services/orchestrator.py
→ app/services/artifact_service.py
→ app/validators/
→ app/tools/
→ app/tools/mcp.py
→ tests/
```

## 3. 阅读一个文件的固定问题

1. 这个文件属于接口、业务、领域、能力还是基础设施层？
2. 谁调用它？
3. 它调用谁？
4. 输入和输出分别是什么？
5. 哪些错误在这里处理，哪些向上抛出？
6. 这里依赖的是接口还是具体实现？
7. 如果替换数据库、模型或 Tool，需要修改这里吗？
8. 对应的测试在哪里？

## 4. 第一次跟踪练习

启动服务后，在 Swagger 创建 Run，然后依次在 IDE 中设置断点：

```text
app/api/routes/runs.py:create_run
app/services/run_service.py:create
app/infrastructure/database.py:RunRecord
```

再调用 Execute，设置断点：

```text
app/api/routes/runs.py:execute
app/services/orchestrator.py:execute_until_review
app/services/module_registry.py:get
app/services/model_provider.py:structured_extract
app/services/artifact_service.py:create_json
```

最后调用 Generate，跟踪：

```text
app/services/orchestrator.py:generate_and_validate
app/validators/schema_validator.py:validate
app/validators/business_rules.py:validate
```

## 5. 注释阅读方法

代码中的 `[教学注释 Lx]` 指原始文件中的逻辑行号。它解释“这一句为什么存在”。不要只逐字阅读，要在每个函数结束后用一句话总结：

```text
这个函数接收什么，保证什么，返回什么，失败时怎样表现。
```
