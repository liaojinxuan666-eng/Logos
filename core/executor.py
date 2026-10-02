# core/executor.py
import sys
import io

def execute_code(code_str, test_cases):
    """
    在受控的命名空间中执行代码，并跑测试用例。
    """
    # 安全扫描
    from core.security import check_code_safety
    is_safe, msg = check_code_safety(code_str)
    if not is_safe:
        return False, msg

    # 限制可用模块的全局环境
    safe_globals = {
        "__builtins__": {
            "range": range,
            "len": len,
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list,
            "dict": dict,
            "sum": sum,
            "min": min,
            "max": max,
            "abs": abs,
        }
    }
    
    local_scope = {}
    try:
        # 执行代码
        exec(code_str, safe_globals, local_scope)
        
        # 找到生成的函数（约定函数名为 generated_func）
        func = local_scope.get("generated_func")
        if not func:
            return False, "未找到名为 generated_func 的函数"
            
        # 跑测试用例
        for case in test_cases:
            inputs = case["inputs"]
            expected = case["expected"]
            actual = func(*inputs)
            if actual != expected:
                return False, f"测试失败: 输入 {inputs}, 期望 {expected}, 实际 {actual}"
                
        return True, "所有测试通过"
        
    except Exception as e:
        return False, f"执行异常: {str(e)}"