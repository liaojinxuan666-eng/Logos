# nlg/verbalizer.py
import random

# 情绪状态（未来可由系统状态动态修改）
EMOTION_STATE = {
    "confidence": 0.8,
    "frustration": 0,
    "curiosity": 0.5
}

TEMPLATES = {
    "success": [
        "搞定！代码已经跑通了：\n{code}",
        "小事一桩，这是我写好的函数：\n{code}",
        "一切正常，测试都过了：\n{code}"
    ],
    "failure": [
        "哎，试了一下，这个逻辑没跑通。错误是：{error}",
        "有点难搞，执行的时候报错了：{error}。我们换条路试试？",
        "出师不利，测试没通过：{error}"
    ],
    "unknown": [
        "抱歉，我目前的认知范围还没覆盖到这个需求。或许我们可以把它拆解一下？",
        "这有点超出我现在的技能库了，我准备去查一下文档。"
    ],
    "boundary": [
        "主人，这个任务的规模太大了，超出了我的算力范围。但我可以帮你拆分它。",
        "警告：检测到超纲任务。建议我们从小目标开始。"
    ]
}

def verbalize(status, data=None):
    """将系统的内部状态翻译成人话"""
    data = data or {}
    
    if status == "success":
        tmpl = random.choice(TEMPLATES["success"])
        # 成功时增加自信，减少挫败
        EMOTION_STATE["confidence"] = min(1.0, EMOTION_STATE["confidence"] + 0.1)
        EMOTION_STATE["frustration"] = max(0, EMOTION_STATE["frustration"] - 1)
        return tmpl.format(code=data.get("code", ""))
        
    elif status == "failure":
        tmpl = random.choice(TEMPLATES["failure"])
        # 失败时增加挫败感
        EMOTION_STATE["frustration"] += 1
        EMOTION_STATE["confidence"] = max(0.1, EMOTION_STATE["confidence"] - 0.1)
        return tmpl.format(error=data.get("error", "未知错误"))
        
    elif status == "unknown":
        return random.choice(TEMPLATES["unknown"])
        
    elif status == "boundary":
        return random.choice(TEMPLATES["boundary"])
        
    return "系统状态未知。"