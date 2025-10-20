import time
import requests

from logger import log

def conn_status(site="https://www.google.com/"):
    try:
        if requests.get(site, timeout=2).status_code != 200:
            log("warning", "This might be an internet lost connection issue or DNS resolution issue. Attempting to reconnect... ")

    except:
        log("warning", "This might be an internet lost connection issue. Attempting to reconnect... ")
    
    try:
        seconds = 0
        while True:
            if seconds == 0:
                log("critical", "WAIT UPTO 300 SECONDS")

            if seconds == 300:
                log("info", "EXITING 300 SECONDS WAITING PERIOD")
                break
                
            try:
                if requests.get(site, timeout=2).status_code == 200:
                    log("info", "Internet connection re-established! Back to rockin'!")
                    for count_down in range(10, 0, -1):
                        time.sleep(1)

                    break
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                seconds += 1
    except KeyboardInterrupt:
        log("critical", "KeyboardInterrupt. Press Ctrl+C again within the shutdown timer [10s] to exit.")
        
        for count_down in range(10, 0, -1):
            time.sleep(1)
        
    return True
