# core/test_pipeline.py
from db.logos_db import init_db, save_skill, get_skill
from core.executor import execute_code # 假设你的 executor 里有这个函数

# 1. 初始化
init_db()

# 2. 手动制造一个 IR 和对应的代码
mock_ir = {
    "action": "generate_code",
    "function_name": "add_one",
    "args": [{"name": "x", "type": "int"}],
    "return_type": "int",
    "logic_description": "return x + 1"
}
mock_code = "def generated_func(x):\n    return x + 1"
mock_tests = [([100], 101), ([1], 2)]

# 3. 存入技能库
save_skill(mock_ir, mock_code, mock_tests)
print("技能已存入。")

# 4. 检索技能库
result = get_skill(mock_ir)
if result["hit"]:
    print(f"命中技能！成功次数: {result['success_count']}")
    print(f"代码: \n{result['code']}")
    # 这里可以调用 executor 测试结果
else:
    print("未命中，需要生成新代码。")