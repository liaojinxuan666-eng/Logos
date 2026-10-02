# core/executor.py
def execute_code(code_str, test_cases):
    # 隔离环境执行
    local_scope = {}
    try:
        exec(code_str, {}, local_scope)
        func = local_scope.get("generated_func")
        for inputs, expected in test_cases:
            assert func(*inputs) == expected, f"测试失败: {inputs}"
        return True, "测试通过"
    except Exception as e:
        return False, str(e)