"""教学注释版：app/main.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from contextlib import asynccontextmanager
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from fastapi import FastAPI
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.api.routes.modules import router as modules_router
# [教学注释 L4] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.api.routes.runs import router as runs_router
# [教学注释 L5] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.config import get_settings
# [教学注释 L6] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.infrastructure.database import init_db

# [教学注释 L8] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@asynccontextmanager
# [教学注释 L9] 定义异步函数，使框架可在等待 I/O 时释放执行权。
async def lifespan(app: FastAPI):
    # [教学注释 L10] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    init_db()
    # [教学注释 L11] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    yield

# [教学注释 L13] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
app = FastAPI(title=get_settings().app_name, version="0.1.0", lifespan=lifespan)
# [教学注释 L14] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
app.include_router(modules_router, prefix="/api/v1")
# [教学注释 L15] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
app.include_router(runs_router, prefix="/api/v1")

# [教学注释 L17] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@app.get("/health", tags=["system"])
# [教学注释 L18] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def health(): return {"status": "ok", "environment": get_settings().environment}
