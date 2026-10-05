# -*- coding: utf-8 -*-
"""
طبقة إدارة قاعدة بيانات الروابط SQLite
"""

import os
import random
import sqlite3
import string
from datetime import datetime


class URLDatabase:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), "..", "urls.db")
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_url TEXT NOT NULL,
                    short_code TEXT UNIQUE NOT NULL,
                    clicks INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()

    @staticmethod
    def generate_random_code(length=6):
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    def create_short_url(self, original_url, alias=None):
        if not original_url.startswith("http://") and not original_url.startswith("https://"):
            original_url = "https://" + original_url

        code = alias if alias else self.generate_random_code()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM urls WHERE short_code = ?", (code,))
            if cursor.fetchone():
                raise ValueError(f"الكود '{code}' مستخدم مسبقاً، اختر كوداً آخر")

            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            cursor.execute(
                "INSERT INTO urls (original_url, short_code, clicks, created_at) VALUES (?, ?, ?, ?)",
                (original_url, code, 0, now_str)
            )
            conn.commit()

        return code, original_url

    def get_url(self, code):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, original_url, clicks FROM urls WHERE short_code = ?", (code,))
            row = cursor.fetchone()
            if row:
                u_id, orig, clicks = row
                cursor.execute("UPDATE urls SET clicks = clicks + 1 WHERE id = ?", (u_id,))
                conn.commit()
                return orig
        return None

    def get_all(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, short_code, clicks, created_at, original_url FROM urls ORDER BY id DESC")
            return cursor.fetchall()

    def delete_url(self, url_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM urls WHERE id = ?", (url_id,))
            conn.commit()
