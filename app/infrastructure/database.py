"""教学注释版：app/infrastructure/database.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from datetime import datetime, timezone
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from pathlib import Path
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
from sqlalchemy import JSON, DateTime, Integer, String, Text, create_engine
# [教学注释 L4] 导入本行后续代码依赖的类型、框架或标准库能力。
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
# [教学注释 L5] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.config import get_settings

# [教学注释 L7] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class Base(DeclarativeBase):
    # [教学注释 L8] 该位置只定义接口或占位行为，具体能力由其他实现提供。
    pass

# [教学注释 L10] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def utcnow() -> datetime:
    # [教学注释 L11] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
    return datetime.now(timezone.utc)

# [教学注释 L13] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class RunRecord(Base):
    # [教学注释 L14] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    __tablename__ = "runs"
    # [教学注释 L15] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    # [教学注释 L16] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    module_id: Mapped[str] = mapped_column(String(200), index=True)
    # [教学注释 L17] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    module_version: Mapped[str] = mapped_column(String(50))
    # [教学注释 L18] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    status: Mapped[str] = mapped_column(String(50), index=True)
    # [教学注释 L19] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    parameters: Mapped[dict] = mapped_column(JSON, default=dict)
    # [教学注释 L20] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    input_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    # [教学注释 L21] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    current_step: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # [教学注释 L22] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    # [教学注释 L23] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    # [教学注释 L24] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

# [教学注释 L26] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class ArtifactRecord(Base):
    # [教学注释 L27] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    __tablename__ = "artifacts"
    # [教学注释 L28] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    # [教学注释 L29] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    run_id: Mapped[str] = mapped_column(String(36), index=True)
    # [教学注释 L30] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    kind: Mapped[str] = mapped_column(String(50), index=True)
    # [教学注释 L31] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    name: Mapped[str] = mapped_column(String(255))
    # [教学注释 L32] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    media_type: Mapped[str] = mapped_column(String(100))
    # [教学注释 L33] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    uri: Mapped[str] = mapped_column(Text)
    # [教学注释 L34] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    sha256: Mapped[str] = mapped_column(String(64))
    # [教学注释 L35] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    revision: Mapped[int] = mapped_column(Integer, default=1)
    # [教学注释 L36] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    # [教学注释 L37] 声明 ORM 字段及其数据库类型、索引、默认值或空值规则。
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

# [教学注释 L39] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
_settings = get_settings()
# [教学注释 L40] 根据当前状态或输入条件选择执行分支。
if _settings.database_url.startswith("sqlite"):
    # [教学注释 L41] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    Path("data").mkdir(exist_ok=True)
# [教学注释 L42] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
engine = create_engine(_settings.database_url, connect_args={"check_same_thread": False} if _settings.database_url.startswith("sqlite") else {})
# [教学注释 L43] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

# [教学注释 L45] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def init_db() -> None:
    # [教学注释 L46] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    Base.metadata.create_all(engine)

# [教学注释 L48] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def get_db():
    # [教学注释 L49] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    db = SessionLocal()
    # [教学注释 L50] 开始可能失败的操作，并在后续分支中把异常转换为可诊断结果。
    try:
        # [教学注释 L51] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        yield db
    # [教学注释 L52] 无论成功还是失败都执行清理，避免连接、文件或进程泄漏。
    finally:
        # [教学注释 L53] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        db.close()
