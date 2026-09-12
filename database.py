import sqlite3
import os
from datetime import date

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "health_app.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Daily Health Tracker Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_tracker (
            date TEXT PRIMARY KEY,
            water_ml INTEGER DEFAULT 0,
            water_goal_ml INTEGER DEFAULT 2500,
            steps INTEGER DEFAULT 0,
            step_goal INTEGER DEFAULT 8000,
            sleep_hours REAL DEFAULT 0.0,
            mood TEXT DEFAULT 'good',
            notes TEXT DEFAULT ''
        )
    """)
    
    # Medication Schedule Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dosage TEXT,
            time TEXT,
            is_taken INTEGER DEFAULT 0,
            date TEXT NOT NULL
        )
    """)
    
    # Chat History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def get_today_str():
    return date.today().isoformat()

def get_daily_tracker(date_str=None):
    if not date_str:
        date_str = get_today_str()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_tracker WHERE date = ?", (date_str,))
    row = cursor.fetchone()
    
    if not row:
        # Create default entry for today
        cursor.execute(
            "INSERT INTO daily_tracker (date, water_ml, water_goal_ml, steps, step_goal, sleep_hours, mood, notes) VALUES (?, 0, 2500, 0, 8000, 0.0, 'good', '')",
            (date_str,)
        )
        conn.commit()
        cursor.execute("SELECT * FROM daily_tracker WHERE date = ?", (date_str,))
        row = cursor.fetchone()
        
    data = dict(row)
    conn.close()
    return data

def update_daily_tracker(date_str=None, **kwargs):
    if not date_str:
        date_str = get_today_str()
    # ensure row exists
    get_daily_tracker(date_str)
    
    allowed = ["water_ml", "water_goal_ml", "steps", "step_goal", "sleep_hours", "mood", "notes"]
    updates = []
    values = []
    for k, v in kwargs.items():
        if k in allowed:
            updates.append(f"{k} = ?")
            values.append(v)
            
    if not updates:
        return get_daily_tracker(date_str)
        
    values.append(date_str)
    query = f"UPDATE daily_tracker SET {', '.join(updates)} WHERE date = ?"
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, tuple(values))
    conn.commit()
    conn.close()
    return get_daily_tracker(date_str)

def get_medications(date_str=None):
    if not date_str:
        date_str = get_today_str()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medications WHERE date = ? ORDER BY time ASC", (date_str,))
    rows = cursor.fetchall()
    meds = [dict(r) for r in rows]
    conn.close()
    return meds

def add_medication(name, dosage, time_str, date_str=None):
    if not date_str:
        date_str = get_today_str()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO medications (name, dosage, time, is_taken, date) VALUES (?, ?, ?, 0, ?)",
        (name.strip(), dosage.strip(), time_str.strip(), date_str)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"id": new_id, "name": name, "dosage": dosage, "time": time_str, "is_taken": 0, "date": date_str}

def toggle_medication(med_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_taken FROM medications WHERE id = ?", (med_id,))
    row = cursor.fetchone()
    if row:
        new_state = 0 if row["is_taken"] == 1 else 1
        cursor.execute("UPDATE medications SET is_taken = ? WHERE id = ?", (new_state, med_id))
        conn.commit()
        conn.close()
        return {"id": med_id, "is_taken": new_state}
    conn.close()
    return None

def delete_medication(med_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medications WHERE id = ?", (med_id,))
    conn.commit()
    conn.close()
    return True

def save_chat_message(role, message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (role, message) VALUES (?, ?)", (role, message))
    conn.commit()
    conn.close()

def get_recent_chat_history(limit=30):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role, message, timestamp FROM chat_history ORDER BY id ASC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    history = [dict(r) for r in rows]
    conn.close()
    return history

def clear_chat_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history")
    conn.commit()
    conn.close()
    return True
