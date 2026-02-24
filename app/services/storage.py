import sqlite3
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "app.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            local_path TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def save_upload(user_id: int, local_path: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO uploads (user_id, local_path, created_at) VALUES (?, ?, ?)",
        (user_id, local_path, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def get_last_upload(user_id: int) -> str | None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT local_path FROM uploads WHERE user_id = ? ORDER BY id DESC LIMIT 1",
        (user_id,),
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
