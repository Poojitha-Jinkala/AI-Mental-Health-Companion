import sqlite3
from datetime import datetime

def create_connection():
    return sqlite3.connect("mental_health.db")

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            sentiment REAL,
            emotion TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_data(user_input, sentiment, emotion):
    conn = create_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO chat_history (user_input, sentiment, emotion, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_input, sentiment, emotion, datetime.now()))
    conn.commit()
    conn.close()

def get_emotion_data():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT emotion, COUNT(*) FROM chat_history GROUP BY emotion")
    data = c.fetchall()
    conn.close()
    return data
