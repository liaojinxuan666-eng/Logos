# nlu/parser.py
import json

def parse_natural_language(user_input):
    """
    模拟微型神经网络的翻译过程：人类语言 -> IR JSON。
    未来这里会替换为 TinyBERT / T5-Small 的推理代码。
    """
    # 占位逻辑：先支持固定的加一需求
    if "加一" in user_input or "add one" in user_input:
        return {
            "action": "generate_code",
            "target": "python",
            "function_name": "add_one",
            "args": [{"name": "x", "type": "int"}],
            "return_type": "int",
            "logic_description": "return x + 1",
            "test_cases": [
                {"inputs": [100], "expected": 101},
                {"inputs": [1], "expected": 2}
            ]
        }
    else:
        return {
            "action": "unknown",
            "target": "none",
            "function_name": "none",
            "args": [],
            "return_type": "none",
            "logic_description": "无法识别意图",
            "test_cases": []
        }