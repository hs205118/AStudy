"""教学注释版：app/services/model_provider.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from typing import Any, Protocol
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
import re

# [教学注释 L4] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class ModelProvider(Protocol):
    # [教学注释 L5] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def structured_extract(self, *, system_prompt: str, user_content: str, schema: dict[str, Any]) -> dict[str, Any]: ...
    # [教学注释 L6] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def semantic_validate(self, *, source: str, candidate: dict[str, Any]) -> list[dict[str, Any]]: ...

# [教学注释 L8] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class FakeModelProvider:
    # [教学注释 L9] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    """可离线运行的开发 Provider。生产环境应替换为企业 Model Gateway。"""
    # [教学注释 L10] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def structured_extract(self, *, system_prompt: str, user_content: str, schema: dict[str, Any]) -> dict[str, Any]:
        # [教学注释 L11] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        raid = re.findall(r"RAID\s*([0-9]+)", user_content, re.I)
        # [教学注释 L12] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        drives = re.findall(r"(\d+)\s*(?:NVMe|drives?|disks?)", user_content, re.I)
        # [教学注释 L13] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return {
            # [教学注释 L14] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            "ir_version": "1.0",
            # [教学注释 L15] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            "requirements": [{
                # [教学注释 L16] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
                "id": "REQ-001",
                # [教学注释 L17] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
                "text": user_content.strip() or "No textual requirement supplied",
                # [教学注释 L18] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
                "type": "storage",
                # [教学注释 L19] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
                "status": "extracted",
                # [教学注释 L20] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
                "source": {"artifact_id": "inline", "location": "input_text"},
                # [教学注释 L21] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
                "confidence": 0.85
            # [教学注释 L22] 结束上一行开始的复合表达式或参数列表。
            }],
            # [教学注释 L23] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            "entities": {
                # [教学注释 L24] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
                "raid_levels": sorted(set(raid)),
                # [教学注释 L25] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
                "drive_count": int(drives[0]) if drives else None
            # [教学注释 L26] 结束上一行开始的复合表达式或参数列表。
            },
            # [教学注释 L27] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            "conflicts": [],
            # [教学注释 L28] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            "missing_items": [] if user_content.strip() else ["input_text"]
        # [教学注释 L29] 结束上一行开始的复合表达式或参数列表。
        }

    # [教学注释 L31] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def semantic_validate(self, *, source: str, candidate: dict[str, Any]) -> list[dict[str, Any]]:
        # [教学注释 L32] 根据当前状态或输入条件选择执行分支。
        if not candidate.get("requirements"):
            # [教学注释 L33] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
            return [{"rule_id": "ai.requirement.coverage", "severity": "error", "message": "No requirements generated"}]
        # [教学注释 L34] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return []
