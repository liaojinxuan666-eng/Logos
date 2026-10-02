FORBIDDEN_KEYWORDS = ["os", "sys", "subprocess", "eval", "exec", "open", "socket"]

def check_code_safety(code_str):
    for word in FORBIDDEN_KEYWORDS:
        if word in code_str:
            return False, f"安全拦截：检测到危险关键字 '{word}'"
    return True, "安全"