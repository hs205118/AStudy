"""教学注释版：app/services/patch_service.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from copy import deepcopy
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from typing import Any

# [教学注释 L4] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def apply_json_patch(document: dict[str, Any], operations: list[dict[str, Any]]) -> dict[str, Any]:
    # [教学注释 L5] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    """Small RFC 6902 subset: add, replace, remove. Array append uses '-' token."""
    # [教学注释 L6] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    result = deepcopy(document)
    # [教学注释 L7] 遍历集合中的每个元素，逐项执行相同规则。
    for op in operations:
        # [教学注释 L8] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        operation, path = op["op"], op["path"]
        # [教学注释 L9] 根据当前状态或输入条件选择执行分支。
        if not path.startswith("/"):
            # [教学注释 L10] 主动终止当前路径并向上层报告受控错误，避免静默产生错误结果。
            raise ValueError("Patch path must start with /")
        # [教学注释 L11] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        tokens = [t.replace("~1", "/").replace("~0", "~") for t in path[1:].split("/") if t != ""]
        # [教学注释 L12] 根据当前状态或输入条件选择执行分支。
        if not tokens:
            # [教学注释 L13] 主动终止当前路径并向上层报告受控错误，避免静默产生错误结果。
            raise ValueError("Root replacement is not supported")
        # [教学注释 L14] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        parent: Any = result
        # [教学注释 L15] 遍历集合中的每个元素，逐项执行相同规则。
        for token in tokens[:-1]:
            # [教学注释 L16] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            parent = parent[int(token)] if isinstance(parent, list) else parent[token]
        # [教学注释 L17] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        key = tokens[-1]
        # [教学注释 L18] 根据当前状态或输入条件选择执行分支。
        if operation in {"add", "replace"}:
            # [教学注释 L19] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            value = op.get("value")
            # [教学注释 L20] 根据当前状态或输入条件选择执行分支。
            if isinstance(parent, list):
                # [教学注释 L21] 根据当前状态或输入条件选择执行分支。
                if key == "-": parent.append(value)
                # [教学注释 L22] 当前一条条件未满足时，继续检查另一种受支持情况。
                elif operation == "add": parent.insert(int(key), value)
                # [教学注释 L23] 处理前述条件均未满足时的默认分支。
                else: parent[int(key)] = value
            # [教学注释 L24] 处理前述条件均未满足时的默认分支。
            else: parent[key] = value
        # [教学注释 L25] 当前一条条件未满足时，继续检查另一种受支持情况。
        elif operation == "remove":
            # [教学注释 L26] 根据当前状态或输入条件选择执行分支。
            if isinstance(parent, list): parent.pop(int(key))
            # [教学注释 L27] 处理前述条件均未满足时的默认分支。
            else: parent.pop(key)
        # [教学注释 L28] 处理前述条件均未满足时的默认分支。
        else:
            # [教学注释 L29] 主动终止当前路径并向上层报告受控错误，避免静默产生错误结果。
            raise ValueError(f"Unsupported patch operation: {operation}")
    # [教学注释 L30] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
    return result
