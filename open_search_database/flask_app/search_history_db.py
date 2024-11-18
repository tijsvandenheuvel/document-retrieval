import sqlite3
import json
from flask import g

DATABASE = 'search_history.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            result TEXT NOT NULL,
            result_titles TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    return g.db

def close_db():
    if 'db' in g:
        g.db.close()

def insert_search_history(query, result, result_titles):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO search_history (query, result, result_titles) VALUES (?, ?, ?)',
        (query, json.dumps(result), json.dumps(result_titles))
    )
    conn.commit()

def fetch_search_history(limit=10):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        f'SELECT id, query, result, result_titles, timestamp FROM search_history ORDER BY timestamp DESC LIMIT {limit}'
    )
    return cursor.fetchall()

def fetch_history_entry(history_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT query, result, result_titles FROM search_history WHERE id = ?', (history_id,))
    return cursor.fetchone()

def get_search_history():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Fetch rows from the search_history table
        query = "SELECT id, query, result, result_titles, timestamp FROM search_history;"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Get column names
        columns = [desc[0] for desc in cursor.description]

        # Convert rows to list of dictionaries
        search_history = [dict(zip(columns, row)) for row in rows]

        conn.close()
        return search_history
    except Exception as e:
        print(f"Error retrieving search history: {e}")
        return None
    
    
def clear_database():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
            
        cursor.execute(f"DELETE FROM search_history;")
        conn.commit()
        
        conn.close()
        return True
    except Exception as e:
        print(f"Error clearing database: {e}")
        return False