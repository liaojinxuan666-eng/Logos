# core/schema.py

# 神经网络（嘴）唯一允许输出的格式
IR_SCHEMA = {
    "action": "generate_code", # 动作类型
    "target": "python",        # 目标语言（后续可扩展 swift）
    "function_name": "string", # 函数名
    "args": [{"name": "string", "type": "string"}], # 参数列表
    "return_type": "string",   # 返回类型
    "logic_description": "string", # 逻辑描述
    "test_cases": [{"inputs": [0], "expected": 1}] # 测试用例
}

# 技能库存入的完整结构
SKILL_SCHEMA = {
    "id": 0,
    "intent_signature": "md5_hash",
    "ir_json": "{}",
    "code": "",
    "test_cases": "[]",
    "success_count": 0,
    "fail_count": 0
}

def validate_ir(ir_json):
    """验证神经网络的输出是否符合规范"""
    required_keys = ["action", "target", "function_name", "args", "logic_description"]
    for key in required_keys:
        if key not in ir_json:
            return False, f"IR 缺失字段: {key}"
    return True, "验证通过"