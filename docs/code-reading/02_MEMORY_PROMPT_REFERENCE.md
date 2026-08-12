# Memory、Prompt 与 Reference 的代码位置

## Prompt 在哪里

当前 Prompt 位于模块目录：

```text
modules/storage-wizard/prompts/system.md
modules/storage-wizard/prompts/user-template.md
modules/pcie-wizard/prompts/system.md
modules/pcie-wizard/prompts/user-template.md
```

`module.yaml` 保存 Prompt 的相对路径，`ModuleRegistry.read_relative()` 负责安全读取。当前 Orchestrator 主要使用 System Prompt，User Prompt 模板组合尚未完整落地。

## 当前有哪种“记忆”

当前只有以下运行态信息：

```text
RunRecord.input_text       单次任务输入
RunRecord.parameters       单次任务参数
Artifact                   单次任务产物
OptimizationService        生成优化候选的骨架
```

它们都不是完整的长期 Memory。

## User Memory 应放在哪里

建议新增：

```text
app/memory/base.py                 MemoryStore 接口
app/memory/service.py              Memory 读取、过滤、候选写入
app/memory/policies.py             Scope、过期、权限和置信度规则
app/infrastructure/memory_store.py 数据库实现
app/api/routes/memory.py           审核和管理 API
```

数据库对象建议包含：

```text
MemoryItem
- id
- scope: user/product/module/organization
- owner_id
- content
- source_run_id
- confidence
- review_status
- valid_from / expires_at
- created_by / approved_by
```

## 分层 Memory 读取顺序

```text
Organization Memory
→ Module Memory
→ Product Memory
→ User Memory
→ Run Memory
```

实际注入前必须执行：

```text
权限过滤
→ Scope 过滤
→ 有效期过滤
→ 审核状态过滤
→ 相关性排序
→ Token 预算裁剪
```

## 安全规则

用户一次修改不能直接成为全局 Memory。正确流程是：

```text
User Patch
→ Memory Candidate
→ 离线评测
→ 人工审核
→ Approved Memory
→ 指定 Scope 生效
```

## Reference 与 Memory 的区别

Reference 是带版本的规范、文档和样例，是外部事实来源。Memory 是从历史任务中提炼、经过治理的可复用经验。两者必须分别存储和审计。
