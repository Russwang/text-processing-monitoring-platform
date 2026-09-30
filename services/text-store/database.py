"""SQLite storage shared by both read and write endpoints."""
import os
import sqlite3
from pathlib import Path

DB_PATH = os.environ.get('TEXT_DB_PATH', str(Path(__file__).parent / 'database' / 'text.db'))

def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS text_store (id TEXT PRIMARY KEY, text TEXT NOT NULL)')

def pull(text_id):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute('SELECT text FROM text_store WHERE id = ?', (text_id,)).fetchone()
