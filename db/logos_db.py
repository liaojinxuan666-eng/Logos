# db/logos_db.py
import sqlite3
import json
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "logos_skills.db")

def init_db():
    """初始化技能库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intent_signature TEXT UNIQUE,
            ir_json TEXT,
            code TEXT,
            test_cases TEXT,
            success_count INTEGER DEFAULT 0,
            fail_count INTEGER DEFAULT 0,
            last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def generate_signature(ir_json):
    """根据 IR JSON 生成唯一指纹"""
    if isinstance(ir_json, str):
        ir_str = ir_json
    else:
        ir_str = json.dumps(ir_json, sort_keys=True)
    return hashlib.md5(ir_str.encode()).hexdigest()

def save_skill(ir_json, code, test_cases):
    """存入技能"""
    sig = generate_signature(ir_json)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO skills (intent_signature, ir_json, code, test_cases, success_count)
            VALUES (?, ?, ?, ?, 1)
            ON CONFLICT(intent_signature) 
            DO UPDATE SET 
                success_count = success_count + 1,
                last_used = CURRENT_TIMESTAMP
        ''', (sig, json.dumps(ir_json), code, json.dumps(test_cases)))
        conn.commit()
        return True
    except Exception as e:
        print(f"存入技能失败: {e}")
        return False
    finally:
        conn.close()

def get_skill(ir_json):
    """检索技能"""
    sig = generate_signature(ir_json)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT code, test_cases, success_count FROM skills WHERE intent_signature = ?', (sig,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "hit": True,
            "code": row[0],
            "test_cases": json.loads(row[1]),
            "success_count": row[2]
        }
    return {"hit": False}

def record_failure(ir_json):
    """记录失败经验"""
    sig = generate_signature(ir_json)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE skills SET fail_count = fail_count + 1 WHERE intent_signature = ?', (sig,))
    conn.commit()
    conn.close()