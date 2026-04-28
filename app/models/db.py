import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'travel.db')

def get_db_connection():
    """Returns a new connection to the SQLite database."""
    # Ensure the instance directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows that act like dicts
    
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
