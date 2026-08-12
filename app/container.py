"""教学注释版：app/container.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from functools import lru_cache
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.config import get_settings
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.infrastructure.artifact_store import LocalArtifactStore
# [教学注释 L4] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.services.model_provider import FakeModelProvider
# [教学注释 L5] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.services.module_registry import ModuleRegistry
# [教学注释 L6] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.tools.base import ToolRegistry
# [教学注释 L7] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.tools.builtin import TextStatsTool

# [教学注释 L9] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@lru_cache
# [教学注释 L10] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def artifact_store(): return LocalArtifactStore(get_settings().artifact_root)
# [教学注释 L11] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@lru_cache
# [教学注释 L12] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def module_registry(): return ModuleRegistry(get_settings().module_root)
# [教学注释 L13] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@lru_cache
# [教学注释 L14] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def model_provider(): return FakeModelProvider()
# [教学注释 L15] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@lru_cache
# [教学注释 L16] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def tool_registry():
    # [教学注释 L17] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    registry = ToolRegistry(); registry.register(TextStatsTool()); return registry
