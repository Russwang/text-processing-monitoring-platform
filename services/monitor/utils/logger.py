from contextlib import closing
import os
import sqlite3
from pathlib import Path

DB_PATH = os.environ.get('MONITOR_DB_PATH', str(Path(__file__).resolve().parents[1] / 'database' / 'monitoring.db'))

def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DB_PATH)) as conn, conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            status TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")

def log(service_name, status, message):
    with closing(sqlite3.connect(DB_PATH)) as conn, conn:
        conn.execute('INSERT INTO logs (service_name, status, message) VALUES (?, ?, ?)',
                     (service_name, status, message))
