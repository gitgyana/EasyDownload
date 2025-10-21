import os 
import time 

from logger import log 


def get_valid_windows_path(file_path):
    try:
        if len(file_path.strip()) < 260:
            log("info", "Valid Windows File Directory : True")
                
            return file_path.strip()
        
        log("warning", f"Total characters in file directory exceeds 260 characters [ {file_path} ]")
            
        filename = os.path.basename(file_path).strip()
        dir_name = os.path.dirname(file_path).strip()
        extra_chars = len(file_path) - 256
        new_dir_name = dir_name[:extra_chars * -1].strip()
        new_file_path = os.path.join(new_dir_name, filename)
        
        log("info", f"New file directory [ {new_file_path} ]")
            
        return new_file_path    
    
    except Exception as func_err:
        log("error", f"[ validate_windows_file_dir function error: {func_err} ]")
    except KeyboardInterrupt:
        log("critical", "KeyboardInterrupt: Exited from function [validate_windows_file_dir]")
        time.sleep(10)
    
    return os.getcwd()
        

def build_download_path(base_dir, date=None, category=None, filename=None):
    try:
        download_dir = base_dir.strip()
        
        if date:
            download_dir = os.path.join(download_dir, date.strip())
        if category:
            download_dir = os.path.join(download_dir, category.strip())
        if filename:    
            download_dir = os.path.join(download_dir, filename.strip())
        
        return download_dir
    
    except Exception as func_err:
        log("error", f"[ create_download_dir function error: {func_err} ]")
    except KeyboardInterrupt:
        log("critical", "KeyboardInterrupt: Exited from function [create_download_dir]")
        time.sleep(10)
        
    return os.getcwd()


def normalize_path(file_path):
    file_dir = os.path.normpath(file_path) 
        
    base_dir = os.getcwd() 
    file_dir = os.path.relpath(file_dir, base_dir) 

    return file_dir

