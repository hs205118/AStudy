# 下一步架构演进

## 第一阶段：拆分 Orchestrator

新增节点：

```text
InputValidationNode
ModuleResolutionNode
ContextBuildNode
ExtractionNode
IRValidationNode
HumanReviewNode
GenerationNode
OutputValidationNode
PublishingNode
```

并新增 `RunStep`，记录每个节点的输入 Artifact、输出 Artifact、状态、尝试次数和错误。

## 第二阶段：Prompt Registry

将文件型 Prompt 演进为：

```text
PromptComponent
PromptVersion
PromptBundle
PromptBundleHash
```

每次 Run 保存实际 Bundle Hash，确保可回放。

## 第三阶段：Review 与 IR Revision

新增：

```text
IRRevision
UserPatch
ReviewTask
Comment
Approval
Waiver
```

人工修改必须形成不可变 Revision，而不是覆盖原文件。

## 第四阶段：Tool Gateway 与 MCP Gateway

统一 Tool、HTTP API 和 MCP 的执行契约，并增加权限、沙箱、审计和 Secret 管理。

## 第五阶段：Reference 与 Memory

先建设 Reference 版本、来源和检索证据，再建设经审核的分层 Memory。不要把向量数据库等同于 Memory。

## 第六阶段：Evaluation

通过 Golden Dataset 比较 Prompt、模型、Tool 和模块版本。任何自学习候选必须先离线评测，再人工批准和 Canary。
