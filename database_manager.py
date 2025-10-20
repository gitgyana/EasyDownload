import os 
import time
import sqlite3

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


def insert_file_path(file_dir, sqlite_db="downloads_db.db", table_name="downloads", db_dir=None):
    try:
        if db_dir: 
            os.makedirs(db_dir, exist_ok=True)
            sqlite_db = os.path.join(db_dir, sqlite_db)
        
        file_dir = os.path.normpath(file_dir) 
        
        base_dir = os.getcwd() 
        file_dir = os.path.relpath(file_dir, base_dir) 

        conn = sqlite3.connect(sqlite_db)
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, file_path TEXT UNIQUE)")
        
        cursor.execute(f"INSERT OR IGNORE INTO {table_name} (file_path) VALUES (?)", (file_dir,))
        
        conn.commit()
        conn.close()
        
        log("info", f"File path inserted: {file_dir}")
        return True
    
    except sqlite3.Error as e:
        log("error", f"SQLite error: {e}")
        return False
    except Exception as func_err:
        log("error", f"insert_file_path function error: {func_err}")
        return False
    except KeyboardInterrupt:
        log("critical", "KeyboardInterrupt: Exited from function [insert_file_path]")
        time.sleep(10)
        return False
