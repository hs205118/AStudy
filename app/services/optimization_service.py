"""教学注释版：app/services/optimization_service.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from typing import Any

# [教学注释 L3] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class OptimizationService:
    # [教学注释 L4] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def propose(self, *, run_id: str, user_patch: list[dict[str, Any]] | None = None, findings: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        # [教学注释 L5] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        signals = []
        # [教学注释 L6] 根据当前状态或输入条件选择执行分支。
        if user_patch: signals.append({"type": "user_patch", "count": len(user_patch)})
        # [教学注释 L7] 根据当前状态或输入条件选择执行分支。
        if findings: signals.append({"type": "validation_findings", "count": len(findings)})
        # [教学注释 L8] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return {"run_id": run_id, "status": "candidate", "signals": signals, "recommendations": ["Evaluate recurring field changes against the golden dataset before changing prompts or memory."] if signals else []}
