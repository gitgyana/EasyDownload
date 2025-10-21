import os
import time
from datetime import datetime

import socket
import requests 
from tqdm import tqdm

from logger import log
from network_status import conn_status
from utilities.metadata import update
from utilities.utils import size_format, format_timeperiod
from database_manager import was_file_downloaded, insert
from path_helper import get_valid_windows_path, normalize_path


def download(url, output_dir=None, attempt=0, max_attempt=10, limit_attempt=True):
    if attempt != 0:
        log("info", f"Reattempt: {attempt}")
        
    if limit_attempt and attempt >= max_attempt:
        log("error", "MAX ATTEMPTS/RETRY REACHED")

        return False, "MAX ATTEMPTS/RETRY REACHED", "0 KB"
    
    try:
        file_path = output_dir
        filename = ""
        
        if not output_dir or output_dir.endswith("Downloads"):
            current_time = datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
            output_dir = os.path.join(os.getcwd(), f"Download_{current_time}")
            
            filename = os.path.basename(url)
            if filename.rfind(".html") != -1:
                filename = filename[:filename.rfind(".html")]
            
            file_path = os.path.join(output_dir, filename)
        else:
            filename = os.path.basename(output_dir)
            
        file_path = get_valid_windows_path(file_path)
        
        timeout_duration = 20
        
        resume_header = {}
        downloaded_bytes = 0
        if os.path.exists(file_path):
            downloaded_bytes = os.path.getsize(file_path)
            resume_header = {'Range': f'bytes={downloaded_bytes}-'}
        
        try:
            response = requests.get(url, headers=resume_header, stream=True, timeout=timeout_duration)
            if response.status_code == 416:
                log("warning", "Resume failed: Full file already downloaded or server doesn't support range.")

                content_size = int(requests.get(
                    url=url, 
                    stream=True, 
                    timeout=timeout_duration
                ).headers.get('content-length', 0))

                if os.path.exists(file_path) and (content_size != os.path.getsize(file_path)):
                    os.remove(file_path)
                    
                return False, "Resume failed: File may already be fully downloaded.", size_format(downloaded_bytes)
                
            total_size = int(response.headers.get('content-length', 0)) + downloaded_bytes
            file_size = size_format(total_size)
            block_size = 8192
        
        except requests.exceptions.Timeout:
            log("error", f"The size request timed out after {timeout_duration} seconds")
            return False, f"The size request timed out", "0 KB"
        except requests.exceptions.RequestException as e:
            log("error", f"An error occurred: {str(e)}")
            return False, f"An error occurred during retriving download size: {e}", "0 KB"
        except Exception as se:
            if isinstance(se, (requests.exceptions.ConnectionError, socket.gaierror)) and conn_status():
                return download(url, output_dir, attempt=attempt+1, limit_attempt=False)
            
            return False, f"Unknown Error while retriving download size: {str(e)}", "0 KB"
        
        columns = {
            "pid": "TEXT",
            "directory": "TEXT",
            "filename": "TEXT UNIQUE",
            "size": "TEXT",
            "links": "TEXT",
            "source": "TEXT",
            "log": "TEXT",
            "status": "TEXT"
        }
        
        update(columns=columns)
        
        if os.path.exists(file_path) and size_format(os.path.getsize(file_path)) == file_size:
            log("info", f"File already exists: [ {file_size} > {filename} ]. Skipping download.")
            
            pid = datetime.now().strftime("%Y%m%d_%H%M%S")
            directory = normalize_path(file_path)
            filename = os.path.basename(directory)
            size = file_size
            links = "UNKNOWN"
            source = "UNKNOWN"
            plog = f"File already exists [{file_size}]"
            status = "True"

            values = (pid, directory, filename, size, links, source, plog, status)

            insert(
                columns=columns, 
                values=values, 
                sqlite_db="downloads_db.db", 
                table_name="downloads", 
                db_dir="ProcessedData"
            )
                
            return False, f"File already exists of {file_size} size. Skipping download.", file_size
        
        if was_file_downloaded(file_path, sqlite_db="downloads_db.db", table_name="downloads", db_dir="ProcessedData"):
            log("info", f"File already exist [ {filename} ]. Skipping download.")
            return False, f"File already exist [ {filename} ]. Skipping download.", file_size
        
        if ("KB" in file_size or " B" in file_size) and int(file_size.split(' ')[0].split('.')[0]) < 100:
            log("error", "DOWNLOAD ERROR: Corrupt File")
            return False, "DOWNLOAD ERROR: Corrupt File", file_size
        
        download_dir = os.path.dirname(file_path)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir, exist_ok=True)
            log("info", f"Directory Created > {download_dir}")
        
        log("info", f"Downloading location: {file_path}")
        download_start_period = time.time()
        try:
            with open(file_path, 'ab') as file, tqdm(
                total=total_size,
                initial=downloaded_bytes,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                miniters=1,
            ) as bar:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        bar.update(len(chunk))
                        file.write(chunk)
        except requests.exceptions.Timeout:
            log("error", "DOWNLOAD ERROR: Download timed out.")
            return False, "DOWNLOAD ERROR: Download timed out.", "0 KB"
        except requests.exceptions.RequestException as e:
            log("error", f"DOWNLOAD ERROR: Request Exception Error: {str(e)}")
            if conn_status():
                return download(url, output_dir, attempt=attempt+1, limit_attempt=False)
                
            return False, f"DOWNLOAD ERROR: Request Exception Error: {str(e)}", "0 KB"
        except Exception as e:
            if isinstance(e, (requests.exceptions.ConnectionError, socket.gaierror)) and conn_status():
                return download(url, output_dir, attempt=attempt+1, limit_attempt=False)
            
            log("error", f"DOWNLOAD ERROR: Unexpected Error While Downloading: {str(e)}")
            return False, f"DOWNLOAD ERROR: Unexpected Error: {str(e)}", "0 KB"
        except KeyboardInterrupt:
            os.remove(file_path)
            log("warning", f"KeyboardInterrupt: DELETED FILE {file_path}")
            return False, "KeyboardInterrupt: DELETED FILE", "0 KB"
        else:
            if ("KB" in file_size or " B" in file_size) and int(file_size.split(' ')[0].split('.')[0]) < 100:
                log("error", "DOWNLOAD ERROR: Corrupt File")
                return False, "DOWNLOAD ERROR: Corrupt File", file_size
            
            update(absolute_total_downloaded_size=total_size)
            update(total_downloaded_size=total_size)
            
            pid = datetime.now().strftime("%Y%m%d_%H%M%S")
            directory = normalize_path(file_path)
            filename = os.path.basename(directory)
            size = file_size
            links = "UNKNOWN"
            source = "UNKNOWN"
            status = "True"
            plog = f"Download Successful"

            values = [pid, directory, filename, size, links, source, plog, status]

            insert(
                columns=columns, 
                values=values, 
                sqlite_db="downloads_db.db", 
                table_name="downloads", 
                db_dir="ProcessedData"
            )
        
        download_duration = time.time() - download_start_period
        log("info", f"Download Successful [{format_timeperiod(download_duration)}]")

        return True, f"Download Successful [{format_timeperiod(download_duration)}]", file_size
    
    except Exception as func_err:
        log("error", f"[ download (no idea) function error: {func_err} ]")
        if "Read timed out" in f"{str(func_err)}":
            return download(url, output_dir, attempt=attempt+1, limit_attempt=False)
            
        return False, f"Function Error: [download_file]: [{func_err}]", "0 KB"
    except KeyboardInterrupt:
        log("critical", "KeyboardInterrupt: Exited from function [download_file]")
        return False, "KeyboardInterrupt - Exited from function [download_file]", "0 KB"

