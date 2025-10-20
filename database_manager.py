import time
import sqlite3

from logger import log


def was_file_downloaded(file_dir, sqlite_db="downloads_db.db", table_name="downloads"):
    try:
        if not sqlite_db:
            log("error", "Invalid or missing downloads database file.")
            return False
        
        conn = sqlite3.connect(sqlite_db)
        cursor = conn.cursor()
        
        query = f"SELECT 1 FROM {table_name} WHERE file_path = ?"
        cursor.execute(query, (file_dir,))
        
        result = cursor.fetchone()
        
        conn.close()
        
        return result is not None
    
    except sqlite3.Error as e:
        log("error", f"SQLite error: {e}")
        return False
    except Exception as he:
        log("error", f"was_file_downloaded function error: {he}")
        return False
    except KeyboardInterrupt:
        log("warning", "KeyboardInterrupt: Exited from function [was_file_downloaded]")
        time.sleep(10)
        return False

