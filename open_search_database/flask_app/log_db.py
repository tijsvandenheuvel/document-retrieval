import sqlite3
from flask import g
import json

DATABASE = 'log.db'

def initialize_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitor_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            file_path TEXT,
            timestamp TEXT
        )
    """)
    
    # Create search_history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            result TEXT,
            result_titles TEXT,
            timestamp TEXT
        )
    """)
    
    conn.commit()
    conn.close()

initialize_database()

def get_db():
    """Get a connection to the SQLite database."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row  # Return rows as dictionaries
    return g.db

def close_db():
    if 'db' in g:
        g.db.close()
        
        
def insert_search_history(query, result, result_titles):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO search_history (query, result, result_titles, timestamp) VALUES (?, ?, ?, datetime('now'))",
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
    
    
def clear_search_history():
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
    
def log_event_to_db(event_type, file_path):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO monitor_logs (event_type, file_path, timestamp) VALUES (?, ?, datetime('now'))", (event_type, file_path))
    conn.commit()