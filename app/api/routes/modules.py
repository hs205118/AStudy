"""教学注释版：app/api/routes/modules.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from fastapi import APIRouter, Depends
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.api.dependencies import require_api_key
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.container import module_registry
# [教学注释 L4] 要求 FastAPI 通过依赖注入提供资源，常用于数据库会话或鉴权。
router = APIRouter(prefix="/modules", tags=["modules"], dependencies=[Depends(require_api_key)])

# [教学注释 L6] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@router.get("")
# [教学注释 L7] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def list_modules():
    # [教学注释 L8] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
    return [{"id": m.id, "name": m.name, "version": m.version, "category_id": m.raw.get("category_id")} for m in module_registry().list_modules()]
