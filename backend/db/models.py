from typing import Dict
import sqlite3
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///game.db")
db_instance = None


def get_db():
    global db_instance
    if db_instance is None:
        db_instance = Database()
    return db_instance


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('game.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
CREATE TABLE IF NOT EXISTS global_counts (
            word TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
        """)
        self.conn.commit()

    def increment_global_count(self, word: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO global_counts (word, count)
        VALUES (?, 1)
        ON CONFLICT(word) DO UPDATE SET count = count + 1
        RETURNING count
        """, (word,))
        result = cursor.fetchone()
        self.conn.commit()
        return result[0] if result else 0

    def get_global_count(self, word: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT count FROM global_counts WHERE word = ?
        """, (word,))
        result = cursor.fetchone()
        return result[0] if result else 0


def init_db():
    get_db()