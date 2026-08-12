"""教学注释版：tests/test_module_registry.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from pathlib import Path
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.services.module_registry import ModuleRegistry

# [教学注释 L4] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def test_load_storage_module():
    # [教学注释 L5] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    registry = ModuleRegistry(Path("modules"))
    # [教学注释 L6] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    module = registry.get("storage-wizard", "1.0.0")
    # [教学注释 L7] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    assert module.name == "Storage Wizard TRD Parser"
