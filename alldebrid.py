import time
import datetime

import socket
import requests
import tldextract

from logger import log
from network_status import conn_status
from utilities.utils import size_format
from utilities.metadata import get, update
from credentials import alldebrid_api_key_list, alldebrid_test_link

api_index = int(datetime.datetime.now().strftime('%d')) % 2
alldebrid_api_key = alldebrid_api_key_list[api_index]


def alldebrid(link=alldebrid_test_link, test=False, alldebrid_key=alldebrid_api_key):
    if test:
        log("info", f"Alldebrid Key: [{alldebrid_key[:4] + ((len(alldebrid_key) - 4) * '.')}]: ")

    try:
        domain = tldextract.extract(link).domain
        if domain in get('skip_debrid_list'):
            log("info", f"Present in [skip debrid list] - '{domain}' in {get('skip_debrid_list')}")

            return f"LINK_HOST_LIMIT_REACHED: {domain}", "0 KB", False
            
        try:
            response = requests.get(
                "https://api.alldebrid.com/v4/link/unlock?agent=api&apikey={0}&link={1}"
                .format(alldebrid_key, link)
            )
            time.sleep(2)

            if response.status_code == 200:
                data = response.json()
                log("info", f"Data: {data}")

                try:
                    if data['status'] == "success":
                        if not test:
                            log("info", f"{data['data']['link']} | {size_format(data['data']['filesize'])}")
                            time.sleep(5)
                            
                        return data['data']['link'], size_format(data['data']['filesize']), True
                    elif data['status'] == "error":
                        if data['error']['code'] == "AUTH_BLOCKED":
                            log("error", f"{data['error']['message']}")
                            wait_timer = 1

                            try:
                                log("info", "Waiting timer: 60 seconds")
                                while wait_timer < 61:
                                    time.sleep(1)                                    
                                    wait_timer += 1
                                    
                            except KeyboardInterrupt:
                                if not test:
                                    log("critical", "KeyboardInterrupt")
                                    
                                for count_down in range(10, 0, -1):
                                    time.sleep(1)

                            return alldebrid(link=link, test=test, alldebrid_key=alldebrid_key)
                        elif data['error']['code'] == "LINK_HOST_LIMIT_REACHED":
                            update(skip_debrid_list=domain)
                                
                            return f"{data['error']['code']}: {data}", "0 KB", False
                        elif data['error']['code'] == "LINK_HOST_UNAVAILABLE":
                            update(skip_url_list=link)
                                
                            return f"{data['error']['code']}: {data}", "0 KB", False
                        else:
                            return f"{data['error']['code']}: {data}", "0 KB", False
                            
                    else:
                        return f"{data['error']['code']}: {data}", "0 KB", False
                        
                except Exception as e:
                    return f"Alldebrid DataAccess Error: {data}", "0 KB", False
                    
            else:
                if test:
                    log("info", f"Response Status Code: {response.status_code}")
                
                if not test:
                    log("error", f"Alldebrid StatusCode Error: {response.status_code}")
                    
                return f"Alldebrid StatusCode Error: response.status_code:{response.status_code}", "0 KB", False
                
        except Exception as e:
            if not test:
                log("error", f"Alldebrid Unknown Error: {str(e)}")

            if isinstance(e, (requests.exceptions.ConnectionError, socket.gaierror)) and conn_status():
                return alldebrid(link=link, test=test, alldebrid_key=alldebrid_key)
            
            return f"Alldebrid Unknown Error: {str(e)}", "0 KB", False
            
    except Exception as debrid_err:
        log("error", f"{debrid_err}")
        if not test:
            log("error", f"[ alldebrid function error: {debrid_err} ]")
            
        return f"Function Error: [alldebrid]: [{debrid_err}]", "0 KB", False
