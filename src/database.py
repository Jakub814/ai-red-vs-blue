import sqlite3
from pathlib import Path

DB_PATH = Path("db/simulation.db")

def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS simulation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            attack_type TEXT,
            difficulty TEXT,
            message TEXT,
            true_label TEXT,
            predicted_label TEXT,
            confidence REAL,
            explanation TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_result(result: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO simulation_results (
            attack_type,
            difficulty,
            message,
            true_label,
            predicted_label,
            confidence,
            explanation
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        result["attack_type"],
        result["difficulty"],
        result["message"],
        result["true_label"],
        result["predicted_label"],
        result["confidence"],
        result["explanation"]
    ))

    conn.commit()
    conn.close()

def load_results():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, attack_type, difficulty, message,
               true_label, predicted_label, confidence, explanation
        FROM simulation_results
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows