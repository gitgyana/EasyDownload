import time

from logger import log
from alldebrid import alldebrid
from streamtape import streamtape
from utilities.metadata import get


def direct_link(link):
    try:
        if get('retrive_link_choice') == 'streamtape':
            return streamtape(link)
        if get('retrive_link_choice') == "alldebrid":
            return alldebrid(link)
                
        if "streamtape" in link or "tapeadsenjoyer" in link:
            return streamtape(link)
        
        return alldebrid(link)
        
    except Exception as func_err:
        log("error", f"[ get_download_link function error: {func_err} ]")
        return f"Function Error: [get_download_link]: [{func_err}]", "0 KB", False
    except KeyboardInterrupt:
        log("critical", "KeyboardInterrupt: Exited from function [get_download_link]")
        time.sleep(10)
        return "KeyboardInterrupt: Exited from function [get_download_link]", "0 KB", False
