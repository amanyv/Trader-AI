from backend.storage.db import get_conn

def get_metrics():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT outcome, COUNT(*) FROM analyses
    WHERE outcome IS NOT NULL
    GROUP BY outcome
    """)

    rows = cur.fetchall()
    conn.close()

    total = sum(r[1] for r in rows)
    metrics = {r[0]: r[1] for r in rows}

    return {
        "total_evaluated": total,
        "breakdown": metrics,
        "win_rate": (
            metrics.get("target_hit", 0) / total
            if total > 0 else None
        )
    }
