import sqlite3
import os
import logging

# Ensure basic logging is configured
logging.basicConfig(level=logging.ERROR)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'travel.db')

def get_db_connection():
    """
    Returns a new connection to the SQLite database.
    Configures row_factory to sqlite3.Row so that rows can be accessed via column names.
    """
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        # Enable foreign keys for cascaded deletes
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise
