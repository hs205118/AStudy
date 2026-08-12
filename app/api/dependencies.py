"""教学注释版：app/api/dependencies.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from fastapi import Header, HTTPException
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.config import get_settings

# [教学注释 L4] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    # [教学注释 L5] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    settings = get_settings()
    # [教学注释 L6] 根据当前状态或输入条件选择执行分支。
    if settings.require_api_key and x_api_key != settings.api_key:
        # [教学注释 L7] 主动终止当前路径并向上层报告受控错误，避免静默产生错误结果。
        raise HTTPException(status_code=401, detail="Invalid API key")
