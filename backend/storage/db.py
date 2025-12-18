import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "tradergpt.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id TEXT PRIMARY KEY,
        symbol TEXT,
        horizon TEXT,
        bias TEXT,
        confidence INTEGER,
        risk_reward TEXT,
        summary TEXT,
        trade_json TEXT,
        created_at TEXT,
        outcome TEXT
    )
    """)

    conn.commit()
    conn.close()
