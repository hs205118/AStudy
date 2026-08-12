# TRD Agent Platform

面向 TRD 解析、中间文件编辑、目标文件生成、工具校验和受控自学习的 Python 工程框架。

## 已实现的框架能力

- FastAPI REST API 与 OpenAPI 文档
- Category / Module / ModuleVersion 注册管理
- Prompt、Schema、Tool、Validator 的模块化配置
- Run 状态机与端到端编排
- Artifact、IR Revision、Validation Report 的本地持久化
- 可插拔 ModelProvider、Tool、MCP Client 和 Validator 接口
- Storage Wizard 示例模块
- 自动修复循环上限与人工审核节点
- Optimization Proposal 自学习候选，不直接修改生产配置
- SQLite 元数据数据库、文件型 Artifact Store
- 单元测试、Dockerfile、docker-compose 和 Makefile

## 目录

```text
app/                 平台代码
modules/             业务模块配置、Prompt、Schema、规则
tests/               单元与 API 测试
scripts/             初始化和示例执行脚本
data/                运行时目录，首次启动自动创建
docs/                架构与扩展说明
```

## 快速启动

要求 Python 3.11+。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
python scripts/init_db.py
uvicorn app.main:app --reload
```

访问：

- API 文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/health

## 运行示例

```bash
python scripts/demo_run.py
```

或：

```bash
curl -X POST http://127.0.0.1:8000/api/v1/runs \
  -H 'Content-Type: application/json' \
  -d '{"module_id":"storage-wizard","module_version":"1.0.0","parameters":{"product":"demo"},"input_text":"Storage controller requires RAID 1 and 4 NVMe drives."}'
```

然后执行：

```bash
curl -X POST http://127.0.0.1:8000/api/v1/runs/<RUN_ID>/execute
```

默认使用 `FakeModelProvider`，无需外部模型密钥，方便验证完整流程。接入真实模型时，实现 `ModelProvider` 并在 `app/container.py` 中替换注册即可。

## 设计约束

1. Artifact 大内容保存在对象存储抽象中，数据库只保存元数据和引用。
2. 发布版本不可变。修改模块时创建新版本。
3. IR 必须先通过 Schema 校验，再进入人工审核和生成阶段。
4. Blocker/Error 未解决时不得发布最终文件。
5. 自学习只产生候选建议，必须经过评测和审批。
6. Tool 和 MCP 输出均视为不可信输入，必须执行 Schema 和策略检查。

## 测试

```bash
pytest
```

## 生产化前需要替换

- SQLite → PostgreSQL
- LocalArtifactStore → S3 / Azure Blob / MinIO
- InProcess workflow → Temporal / Durable Functions / Celery 等持久化编排
- FakeModelProvider → 企业模型网关
- NoopMCPClient → 受治理的 MCP Gateway
- API Key 示例鉴权 → OIDC、RBAC、ABAC
- 单进程锁 → 分布式锁和幂等键

## Windows 一键自检（AVF）

```powershell
.\self-test.ps1
```

自动创建隔离环境、安装依赖、启动服务、执行环境/API/工作流自检，并生成：

- `.avf/reports/<run-id>/human-report/index.html`
- `.avf/reports/<run-id>/AStudy_AVF_<run-id>_<status>.zip`

完整测试：

```powershell
.\self-test.ps1 -Suite full
```
