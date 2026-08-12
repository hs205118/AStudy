"""教学注释版：scripts/init_db.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.infrastructure.database import init_db
# [教学注释 L2] 根据当前状态或输入条件选择执行分支。
if __name__ == "__main__":
    # [教学注释 L3] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    init_db(); print("Database initialized")
