# 从请求到 Final Artifact 的代码链路

## 创建 Run

```text
POST /api/v1/runs
→ app/api/routes/runs.py
→ ModuleRegistry.get()
→ RunService.create()
→ RunRecord
→ SQLite
```

Router 只处理 HTTP，Service 表达业务动作，ORM Record 负责持久化。这样同一业务动作未来可以被 CLI、后台任务或工作流引擎复用。

## Execute

```text
POST /api/v1/runs/{id}/execute
→ Orchestrator.execute_until_review()
→ 加载模块定义
→ 加载 System Prompt 与 IR Schema
→ ModelProvider.structured_extract()
→ 保存 IR Artifact
→ Schema 校验
→ WAITING_FOR_USER_REVIEW
```

`Orchestrator` 是流程协调者，不应该长期承载所有领域算法。后续应把每个步骤拆成 Node 和 RunStep。

## Generate

```text
POST /api/v1/runs/{id}/generate
→ 读取最新 IR
→ 生成 Candidate
→ Schema Validator
→ Business Validator
→ Semantic Validator
→ Validation Report
→ Final Artifact
```

正确性门禁应优先依赖确定性 Validator。AI 适合检查语义遗漏和矛盾，不应替代类型、范围、枚举、唯一性等确定性规则。
