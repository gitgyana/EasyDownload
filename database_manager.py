import os 
import time
import sqlite3
from datetime import datetime

from logger import log


def was_file_downloaded(file_dir, sqlite_db="downloads_db.db", table_name="downloads", db_dir=None):
    try:
        if db_dir: 
            os.makedirs(db_dir, exist_ok=True)
            sqlite_db = os.path.join(db_dir, sqlite_db)

        if not sqlite_db:
            log("error", "Invalid or missing downloads database file.")
            return False
        
        file_dir = os.path.normpath(file_dir)
        
        conn = sqlite3.connect(sqlite_db)
        cursor = conn.cursor()
        
        base_dir = os.getcwd() 
        relative_file_dir = os.path.relpath(file_dir, base_dir) 
        
        query = f"SELECT 1 FROM {table_name} WHERE file_path = ?"
        cursor.execute(query, (relative_file_dir,)) 
        
        result = cursor.fetchone()
        
        conn.close()
        
        return result is not None
    
    except sqlite3.Error as e:
        log("error", f"SQLite error: {e}")
        return False
    except Exception as func_err:
        log("error", f"was_file_downloaded function error: {func_err}")
        return False
    except KeyboardInterrupt:
        log("critical", "KeyboardInterrupt: Exited from function [was_file_downloaded]")
        time.sleep(10)
        return False


def insert(columns=None, values=None, sqlite_db="downloads_db.db", table_name="downloads", db_dir=None):
    try:
        if db_dir: 
            os.makedirs(db_dir, exist_ok=True)
            sqlite_db = os.path.join(db_dir, sqlite_db)
        
        if not columns:
            log("error", "Columns must be provided")
            return False

        if not values:
            log("error", "Values for the columns must be provided")
            return False

        column_definitions = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        column_placeholders = ", ".join(["?" for _ in columns])
        column_names = ", ".join(columns.keys())

        if len(values) != len(columns):
            log("error", "The number of values must match the number of columns")
            return False

        conn = sqlite3.connect(sqlite_db)
        cursor = conn.cursor()

        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})")

        cursor.execute(f"INSERT OR IGNORE INTO {table_name} ({column_names}) VALUES ({column_placeholders})", tuple(values))

        conn.commit()
        conn.close()
        
        log("info", f"Successful Insertion [DB: {sqlite_db}] [TABLE: {table_name}]")
        return True
    
    except sqlite3.Error as e:
        log("error", f"SQLite error: {e}")
        return False
    except Exception as func_err:
        log("error", f"insert function error: {func_err}")
        return False
    except KeyboardInterrupt:
        log("critical", "KeyboardInterrupt: Exited from function [insert]")
        time.sleep(10)
        return False
