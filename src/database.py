import sqlite3
import os
import pandas as pd
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'history.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS submissions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  student TEXT, 
                  problem_id TEXT, 
                  timestamp TEXT, 
                  code TEXT,
                  score REAL, 
                  mode TEXT, 
                  error_cat TEXT,
                  ml_prediction TEXT)''')
    conn.commit()
    conn.close()

def save_submission(student, problem_id, code, score, mode, error_cat, ml_prediction):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO submissions (student, problem_id, timestamp, code, score, mode, error_cat, ml_prediction) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (student, problem_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), code, score, mode, error_cat, ml_prediction))
    conn.commit()
    conn.close()

def get_history():
    if not os.path.exists(DB_PATH): return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT student, problem_id, timestamp, score, mode, error_cat, ml_prediction FROM submissions ORDER BY timestamp DESC", conn)
    conn.close()
    return df
