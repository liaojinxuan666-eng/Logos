# core/security.py
import re

# 危险关键字黑名单
FORBIDDEN_KEYWORDS = [
    "os", "sys", "subprocess", "eval", "exec", "open", 
    "socket", "shutil", "glob", "pathlib", "importlib"
]

def check_code_safety(code_str):
    """
    检查代码是否包含危险操作。
    返回 (bool, str): 是否安全，及原因。
    """
    if not code_str:
        return False, "代码为空"
        
    # 转小写进行正则匹配，防止绕过
    code_lower = code_str.lower()
    
    for word in FORBIDDEN_KEYWORDS:
        # 精确匹配单词边界，避免误杀（如 os 不会匹配到 cost）
        if re.search(r'\b' + word + r'\b', code_lower):
            return False, f"安全拦截：检测到危险关键字 '{word}'"
            
    return True, "安全"