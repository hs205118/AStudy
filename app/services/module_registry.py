"""教学注释版：app/services/module_registry.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from dataclasses import dataclass
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from pathlib import Path
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
from typing import Any
# [教学注释 L4] 导入本行后续代码依赖的类型、框架或标准库能力。
import yaml

# [教学注释 L6] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@dataclass(frozen=True)
# [教学注释 L7] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class ModuleDefinition:
    # [教学注释 L8] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    id: str
    # [教学注释 L9] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    name: str
    # [教学注释 L10] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    version: str
    # [教学注释 L11] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    raw: dict[str, Any]
    # [教学注释 L12] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    base_path: Path

# [教学注释 L14] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class ModuleRegistry:
    # [教学注释 L15] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def __init__(self, root: Path):
        # [教学注释 L16] 把依赖或运行状态保存到当前对象，供其他方法复用。
        self.root = root

    # [教学注释 L18] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def list_modules(self) -> list[ModuleDefinition]:
        # [教学注释 L19] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        result = []
        # [教学注释 L20] 根据当前状态或输入条件选择执行分支。
        if not self.root.exists():
            # [教学注释 L21] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
            return result
        # [教学注释 L22] 遍历集合中的每个元素，逐项执行相同规则。
        for file in self.root.glob("*/module.yaml"):
            # [教学注释 L23] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            result.append(self._load(file))
        # [教学注释 L24] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return result

    # [教学注释 L26] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def get(self, module_id: str, version: str) -> ModuleDefinition:
        # Prevent path traversal; module IDs are resolved by scanning trusted manifests.
        # [教学注释 L28] 遍历集合中的每个元素，逐项执行相同规则。
        for module in self.list_modules():
            # [教学注释 L29] 根据当前状态或输入条件选择执行分支。
            if module.id == module_id and module.version == version:
                # [教学注释 L30] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
                return module
        # [教学注释 L31] 主动终止当前路径并向上层报告受控错误，避免静默产生错误结果。
        raise KeyError(f"Module not found: {module_id}@{version}")

    # [教学注释 L33] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def _load(self, file: Path) -> ModuleDefinition:
        # [教学注释 L34] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        raw = yaml.safe_load(file.read_text(encoding="utf-8"))
        # [教学注释 L35] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        data = raw["module"]
        # [教学注释 L36] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return ModuleDefinition(data["id"], data["name"], data["version"], data, file.parent)

    # [教学注释 L38] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
    @staticmethod
    # [教学注释 L39] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def read_relative(module: ModuleDefinition, relative: str) -> str:
        # [教学注释 L40] 转换为规范绝对路径，便于检查路径是否越出允许目录。
        target = (module.base_path / relative).resolve()
        # [教学注释 L41] 根据当前状态或输入条件选择执行分支。
        if module.base_path.resolve() not in target.parents:
            # [教学注释 L42] 主动终止当前路径并向上层报告受控错误，避免静默产生错误结果。
            raise ValueError("Unsafe module resource path")
        # [教学注释 L43] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return target.read_text(encoding="utf-8")
