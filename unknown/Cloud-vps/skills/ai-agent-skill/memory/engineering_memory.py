import sqlite3, json, hashlib
from datetime import datetime
from typing import List, Dict

class EngineeringMemory:
    def __init__(self, db_path="/root/AI-Agent-Skill/memory/engineering_memory.db"):
        self.db_path = db_path
        self.init_db()
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS experiences (id TEXT PRIMARY KEY, title TEXT, category TEXT, problem TEXT, solution TEXT, environment TEXT, tags TEXT, importance REAL DEFAULT 1.0, created_at TEXT, usage_count INTEGER DEFAULT 0)")
        c.execute("CREATE TABLE IF NOT EXISTS decisions (id TEXT PRIMARY KEY, context TEXT, decision TEXT, rationale TEXT, outcome TEXT, timestamp TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS failures (id TEXT PRIMARY KEY, error_type TEXT, error_message TEXT, root_cause TEXT, fix TEXT, timestamp TEXT)")
        conn.commit(); conn.close()
    def add_experience(self, title, problem, solution, environment, tags, importance=1.0):
        eid = hashlib.sha256(f"{title}{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        conn = sqlite3.connect(self.db_path); c = conn.cursor()
        c.execute("INSERT INTO experiences (id, title, category, problem, solution, environment, tags, importance, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (eid, title, "engineering", problem, solution, environment, json.dumps(tags), importance, datetime.now().isoformat()))
        conn.commit(); conn.close()
        return eid
