# core/schema.py
# 这是神经网络和符号引擎之间的绝对契约！

IR_SCHEMA = {
    "action": "generate_code", # 当前只做这一个
    "target": "python",        # 目标语言
    "function_name": "string",
    "args": [{"name": "string", "type": "string"}],
    "return_type": "string",
    "logic_description": "string", # 用自然语言描述逻辑裁判
}