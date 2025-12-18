from backend.storage.db import get_conn

def update_outcome(analysis_id: str, outcome: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    UPDATE analyses
    SET outcome = ?
    WHERE id = ?
    """, (outcome, analysis_id))

    conn.commit()
    conn.close()
