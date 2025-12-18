import json
import uuid
from datetime import datetime
from backend.storage.db import get_conn

def save_analysis(data: dict) -> str:
    analysis_id = str(uuid.uuid4())
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO analyses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        analysis_id,
        data["symbol"],
        data["horizon"],
        data["bias"],
        data["confidence_score"],
        data["risk_reward_ratio"],
        data["summary"],
        json.dumps(data["trade_idea"]),
        datetime.utcnow().isoformat(),
        None
    ))

    conn.commit()
    conn.close()
    return analysis_id


def get_last_analysis(symbol: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM analyses
    WHERE symbol = ?
    ORDER BY created_at DESC
    LIMIT 1
    """, (symbol,))

    row = cur.fetchone()
    conn.close()
    return row
