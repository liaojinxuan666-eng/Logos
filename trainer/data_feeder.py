# trainer/data_feeder.py
import json
import random

# 同义词模板
INTENT_TEMPLATES = [
    "写个函数加一",
    "帮我生成一个整数加一的函数",
    "创建一个功能是输入x返回x+1的方法",
    "写一个 add one 函数",
    "给我一个整数自增的函数"
]

def generate_training_data(num_samples=1000, output_file="train_data.jsonl"):
    """
    生成用于训练 NLU（微型神经网络）的语料。
    格式：{"prompt": "人类指令", "completion": "IR JSON 字符串"}
    """
    data = []
    for _ in range(num_samples):
        prompt = random.choice(INTENT_TEMPLATES)
        completion = json.dumps({
            "action": "generate_code",
            "target": "python",
            "function_name": "add_one",
            "args": [{"name": "x", "type": "int"}],
            "return_type": "int",
            "logic_description": "return x + 1",
            "test_cases": [{"inputs": [100], "expected": 101}]
        }, ensure_ascii=False)
        
        data.append({"prompt": prompt, "completion": completion})
        
    with open(output_file, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            
    print(f"成功生成 {num_samples} 条训练数据，保存至 {output_file}")

if __name__ == "__main__":
    generate_training_data(10000)