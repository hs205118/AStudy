"""教学注释版：tests/test_patch_service.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.services.patch_service import apply_json_patch

# [教学注释 L3] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def test_patch_replace_and_add():
    # [教学注释 L4] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    result = apply_json_patch({"a": 1, "items": []}, [{"op": "replace", "path": "/a", "value": 2}, {"op": "add", "path": "/items/-", "value": "x"}])
    # [教学注释 L5] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    assert result == {"a": 2, "items": ["x"]}
