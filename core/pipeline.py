# core/pipeline.py
from nlu.parser import parse_natural_language
from nlg.verbalizer import verbalize
from core.executor import execute_code
from db.logos_db import init_db, get_skill, save_skill, record_failure
from core.schema import validate_ir

def run_uce(user_input):
    """UCE 2.0 的核心处理流水线"""
    
    # 0. 初始化数据库
    init_db()
    
    # 1. 耳朵（NLU）：人类语言 -> IR
    ir_json = parse_natural_language(user_input)
    print(f"[系统内部] 解析出的 IR: {ir_json}")
    
    # 2. 验证 IR 合法性
    is_valid, msg = validate_ir(ir_json)
    if not is_valid:
        return verbalize("unknown")
        
    # 3. 大脑（记忆）：查技能库
    skill = get_skill(ir_json)
    if skill["hit"]:
        print(f"[系统内部] 命中技能库！成功次数: {skill['success_count']}")
        code = skill["code"]
        test_cases = skill["test_cases"]
    else:
        print("[系统内部] 技能库未命中，准备合成代码...")
        # 这里未来接入 code_synthesizer.py，目前先硬编码兜底
        code = "def generated_func(x):\n    return x + 1"
        test_cases = ir_json.get("test_cases", [])
    
    # 4. 手脚（执行）：沙箱跑测试
    is_success, exec_msg = execute_code(code, test_cases)
    
    # 5. 嘴巴（NLG）：根据结果说话
    if is_success:
        # 成功，存入技能库（强化记忆）
        save_skill(ir_json, code, test_cases)
        return verbalize("success", {"code": code})
    else:
        # 失败，记录失败经验
        record_failure(ir_json)
        return verbalize("failure", {"error": exec_msg})

if __name__ == "__main__":
    # 手动测试
    user_says = "帮我写个整数加一的函数"
    print(f"用户说: {user_says}")
    response = run_uce(user_says)
    print(f"UCE 回应:\n{response}")