"""教学注释版：tests/test_artifact_store.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
import pytest
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.infrastructure.artifact_store import LocalArtifactStore

# [教学注释 L4] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def test_put_get(tmp_path):
    # [教学注释 L5] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    store = LocalArtifactStore(tmp_path)
    # [教学注释 L6] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    uri, digest = store.put("run/a.txt", b"hello")
    # [教学注释 L7] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    assert store.get(uri) == b"hello"
    # [教学注释 L8] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    assert len(digest) == 64

# [教学注释 L10] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def test_reject_path_traversal(tmp_path):
    # [教学注释 L11] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    store = LocalArtifactStore(tmp_path)
    # [教学注释 L12] 通过上下文管理器确保资源在离开代码块时被正确释放。
    with pytest.raises(ValueError): store.put("../escape", b"x")
