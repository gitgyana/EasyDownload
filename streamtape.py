import re
import time
import datetime

import socket
import requests

from logger import log
from network_status import conn_status
from utilities.utils import size_format
from utilities.metadata import get, update
from credentials import streamtape_api_username_list, streamtape_api_password_list


api_index = int(datetime.datetime.now().strftime('%d')) % 2
streamtape_api_username = streamtape_api_username_list[api_index]
streamtape_api_password = streamtape_api_password_list[api_index]


def get_streamtape_video_id(url):
    try:
        if url[-1:] != '/':
            url += '/'
        
        match = re.search(r'/v/([^/]+)/', url)
        if match:
            log("info", f"{match.group(1)}")
            return match.group(1), True
        else:
            match = re.search(r'/e/([^/]+)/', url)

            if match:
                log("info", f"{match.group(1)}")
                return match.group(1), True
            
            return "Invalid URL format. Could not extract video ID.", False

    except Exception as func_err:
        log("error", f"[ get_streamtape_video_id function error: {func_err} ]")

        return f"Function Error: [get_streamtape_video_id]: [{func_err}]", False
    except KeyboardInterrupt:
        log("critical", "KeyboardInterrupt: Exited from function [get_streamtape_video_id]")
        time.sleep(10)

        return "KeyboardInterrupt: Exited from function [get_streamtape_video_id]", False
        

def streamtape(link):
    if "streamtape" in get('skip_debrid_list'):
        return "Too high server load", "0 KB", False
    
    try:
        data = ''
        task = "streamtape processing"
        try:
            video_id, video_id_status = get_streamtape_video_id(link)
            if video_id_status:
                streamtape_ticket_response = requests.get(
                    "https://api.streamtape.com/file/dlticket?file={0}&login={1}&key={2}"
                    .format(video_id, streamtape_api_username, streamtape_api_password)
                )
                streamtape_ticket_response.raise_for_status()
                data = streamtape_ticket_response.json()
                
                task = "checking ticket status"
                if data['status'] != 200:
                    log("error", f"Streamtape Ticket Error: {data}")
                    
                    if data['status'] == 500:
                        log("warning", f"Too high server load: {data}")
                        update(skip_debrid_list="streamtape")

                        return f"Too high server load: {data}", "0 KB", False
                    
                    return f"Streamtape Ticket Error: {data}", "0 KB", False
                
                task = "getting ticket"
                ticket_id = data["result"]["ticket"]
                
                task = "setting timer from ticket"
                log("info", f"Timer for ticket: {data['result']['wait_time']}")
                for count_down in range(data["result"]["wait_time"], 0, -1):
                    time.sleep(1.2)
                
                time.sleep(1)
                
                download_link_response = requests.get(
                    "https://api.streamtape.com/file/dl?file={0}&ticket={1}"
                    .format(video_id, ticket_id)
                )
                download_link_response.raise_for_status()
                data = download_link_response.json()
                
                task = "checking url status"
                if data["status"] != 200:
                    log("error", f"Streamtape DownloadLink Error: {data}")

                    return f"Streamtape DownloadLink Error: {data}", "0 KB", False
                
                task = "returning url and size"
                log("info", f"{data['result']['url']} | {size_format(data['result']['size'])}")

                return data["result"]["url"], size_format(data["result"]["size"]), True
            else:
                log("error", f"Streamtape VideoID Error: {video_id}")
                return f"Streamtape VideoID Error: {video_id}", "0 KB", False

        except Exception as e:
            log("error", f"Streamtape Task Error: [{task}] | {data} | {str(e)}")
            if isinstance(e, (requests.exceptions.ConnectionError, socket.gaierror)) and conn_status():
                return streamtape(link)

            return f"Streamtape Task Error: [{task}] | {data} | {str(e)}", "0 KB", False

    except Exception as func_err:
        log("error", f"[streamtape function error: {func_err}]")

        return f"Function Error: [streamtape]: [{func_err}]", "0 KB", False
