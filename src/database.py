import sqlite3
from sqlite3 import Connection
from typing import List, Tuple, Optional
import threading
import datetime

DB_LOCK = threading.Lock()

class EmailDatabase:
    def __init__(self, db_path: str = "emails.db"):
        self.db_path = db_path
        self.conn = self._connect()
        self._create_table()

    def _connect(self) -> Connection:
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _create_table(self):
        with DB_LOCK:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    domain TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            self.conn.commit()

    def add_email(self, email: str, domain: str):
        with DB_LOCK:
            cursor = self.conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO emails (email, domain, created_at) VALUES (?, ?, ?)",
                    (email, domain, datetime.datetime.utcnow().isoformat())
                )
                self.conn.commit()
            except sqlite3.IntegrityError:
                pass  # Email déjà présent

    def delete_email(self, email_id: int):
        with DB_LOCK:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM emails WHERE id=?", (email_id,))
            self.conn.commit()

    def list_emails(self, search: Optional[str] = None) -> List[Tuple[int, str, str, str]]:
        with DB_LOCK:
            cursor = self.conn.cursor()
            if search:
                like_search = f"%{search}%"
                cursor.execute(
                    "SELECT id, email, domain, created_at FROM emails WHERE email LIKE ? ORDER BY created_at DESC",
                    (like_search,)
                )
            else:
                cursor.execute(
                    "SELECT id, email, domain, created_at FROM emails ORDER BY created_at DESC"
                )
            return cursor.fetchall()
