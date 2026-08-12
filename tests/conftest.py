"""教学注释版：tests/conftest.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
import os
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from pathlib import Path
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
import pytest

# [教学注释 L5] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@pytest.fixture
# [教学注释 L6] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def isolated(tmp_path, monkeypatch):
    # [教学注释 L7] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    monkeypatch.setenv("TRD_DATABASE_URL", f"sqlite:///{tmp_path}/test.db")
    # [教学注释 L8] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    monkeypatch.setenv("TRD_ARTIFACT_ROOT", str(tmp_path / "artifacts"))
    # [教学注释 L9] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
    return tmp_path
