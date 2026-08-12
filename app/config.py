"""教学注释版：app/config.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from functools import lru_cache
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from pathlib import Path
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
from pydantic_settings import BaseSettings, SettingsConfigDict

# [教学注释 L5] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class Settings(BaseSettings):
    # [教学注释 L6] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    model_config = SettingsConfigDict(env_file=".env", env_prefix="TRD_", extra="ignore")
    # [教学注释 L7] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    app_name: str = "TRD Agent Platform"
    # [教学注释 L8] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    environment: str = "development"
    # [教学注释 L9] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    database_url: str = "sqlite:///./data/trd_agent.db"
    # [教学注释 L10] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    artifact_root: Path = Path("./data/artifacts")
    # [教学注释 L11] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    module_root: Path = Path("./modules")
    # [教学注释 L12] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    max_repair_attempts: int = 2
    # [教学注释 L13] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    require_api_key: bool = False
    # [教学注释 L14] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    api_key: str = "replace-me"

# [教学注释 L16] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@lru_cache
# [教学注释 L17] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def get_settings() -> Settings:
    # [教学注释 L18] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
    return Settings()
