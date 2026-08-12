"""教学注释版：app/infrastructure/artifact_store.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
import hashlib
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from pathlib import Path
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
from typing import Protocol

# [教学注释 L5] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class ArtifactStore(Protocol):
    # [教学注释 L6] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def put(self, key: str, content: bytes) -> tuple[str, str]: ...
    # [教学注释 L7] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def get(self, uri: str) -> bytes: ...

# [教学注释 L9] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class LocalArtifactStore:
    # [教学注释 L10] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def __init__(self, root: Path):
        # [教学注释 L11] 把依赖或运行状态保存到当前对象，供其他方法复用。
        self.root = root.resolve()
        # [教学注释 L12] 把依赖或运行状态保存到当前对象，供其他方法复用。
        self.root.mkdir(parents=True, exist_ok=True)

    # [教学注释 L14] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def put(self, key: str, content: bytes) -> tuple[str, str]:
        # [教学注释 L15] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        safe = Path(key)
        # [教学注释 L16] 根据当前状态或输入条件选择执行分支。
        if safe.is_absolute() or ".." in safe.parts:
            # [教学注释 L17] 主动终止当前路径并向上层报告受控错误，避免静默产生错误结果。
            raise ValueError("Unsafe artifact key")
        # [教学注释 L18] 转换为规范绝对路径，便于检查路径是否越出允许目录。
        destination = (self.root / safe).resolve()
        # [教学注释 L19] 根据当前状态或输入条件选择执行分支。
        if self.root not in destination.parents:
            # [教学注释 L20] 主动终止当前路径并向上层报告受控错误，避免静默产生错误结果。
            raise ValueError("Artifact path escapes root")
        # [教学注释 L21] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        destination.parent.mkdir(parents=True, exist_ok=True)
        # [教学注释 L22] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        destination.write_bytes(content)
        # [教学注释 L23] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return str(destination), hashlib.sha256(content).hexdigest()

    # [教学注释 L25] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def get(self, uri: str) -> bytes:
        # [教学注释 L26] 转换为规范绝对路径，便于检查路径是否越出允许目录。
        path = Path(uri).resolve()
        # [教学注释 L27] 根据当前状态或输入条件选择执行分支。
        if self.root != path and self.root not in path.parents:
            # [教学注释 L28] 主动终止当前路径并向上层报告受控错误，避免静默产生错误结果。
            raise ValueError("Artifact path escapes root")
        # [教学注释 L29] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return path.read_bytes()
