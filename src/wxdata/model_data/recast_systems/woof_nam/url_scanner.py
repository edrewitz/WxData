"""
This file has the URL scanners to find the latest WOOF-NAM forecast data from Recast Systems

(C) Eric J. Drewitz 2025-2026
"""
import requests
import sys
import time

# Exception handling for Python >= 3.13 and Python < 3.13
try:
    from datetime import datetime, timedelta, UTC
except Exception as e:
    from datetime import datetime, timedelta

# Gets current time in UTC
try:
    now = datetime.now(UTC)
except Exception as e:
    now = datetime.utcnow()

# Gets yesterday's date
yd = now - timedelta(days=1)

PREFIX = f"https://woof-nam.recastsystems.com/woof-nam/12km/"

def woof_nam_url_scanner(final_forecast_hour,
                         proxies):
    
    """
    This function scans the Recast Systems server for the latest available WOOF-NAM data.
    
    Required Arguments: 
    
    1) final_forecast_hour (Integer) - The last forecast hour in the set. Maximum is 84 hours.
    
    2) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    Optional Arguments: None
                               
    **Returns**
    
    The URL, model runtime and filename of the latest data.  
    """
    
    if final_forecast_hour < 10:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        pass
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/141.0 Safari/537.36"
        ),
        "Referer": "https://woof-nam.recastsystems.com/"
    }
    
    today_18z_url = f"{PREFIX}{now.strftime('%Y%m%d')}/18z/"
    today_12z_url = f"{PREFIX}{now.strftime('%Y%m%d')}/12z/"
    today_06z_url = f"{PREFIX}{now.strftime('%Y%m%d')}/06z/"
    today_00z_url = f"{PREFIX}{now.strftime('%Y%m%d')}/00z/"
    
    yesterday_18z_url = f"{PREFIX}{yd.strftime('%Y%m%d')}/18z/"
    yesterday_12z_url = f"{PREFIX}{yd.strftime('%Y%m%d')}/12z/"
    yesterday_06z_url = f"{PREFIX}{yd.strftime('%Y%m%d')}/06z/"
    yesterday_00z_url = f"{PREFIX}{yd.strftime('%Y%m%d')}/00z/"
    
    file_18z = f"woof-nam.t18z.awphys{final_forecast_hour}.tm00.grib2"
    file_12z = f"woof-nam.t12z.awphys{final_forecast_hour}.tm00.grib2"
    file_06z = f"woof-nam.t06z.awphys{final_forecast_hour}.tm00.grib2"
    file_00z = f"woof-nam.t00z.awphys{final_forecast_hour}.tm00.grib2"
    
    if proxies == None:
        try:
            t_18z = requests.get(f"{today_18z_url}{file_18z}",
                                 headers=headers,
                                 stream=True)
            t_18z.close()
            
            t_12z = requests.get(f"{today_12z_url}{file_12z}",
                                 headers=headers,
                                 stream=True)
            t_12z.close()
            
            t_06z = requests.get(f"{today_06z_url}{file_06z}",
                                 headers=headers,
                                 stream=True)
            t_06z.close()
            
            t_00z = requests.get(f"{today_00z_url}{file_00z}",
                                 headers=headers,
                                 stream=True)
            t_00z.close()
            
            y_18z = requests.get(f"{yesterday_18z_url}{file_18z}",
                                 headers=headers,
                                 stream=True)
            y_18z.close()
            
            y_12z = requests.get(f"{yesterday_12z_url}{file_12z}",
                                 headers=headers,
                                 stream=True)
            y_12z.close()
            
            y_06z = requests.get(f"{yesterday_06z_url}{file_06z}",
                                 headers=headers,
                                 stream=True)
            y_06z.close()
            
            y_00z = requests.get(f"{yesterday_00z_url}{file_00z}",
                                 headers=headers,
                                 stream=True)
            y_00z.close()
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(60)
                try:
                    t_18z = requests.get(f"{today_18z_url}{file_18z}",
                                        headers=headers,
                                        stream=True)
                    t_18z.close()
                    
                    t_12z = requests.get(f"{today_12z_url}{file_12z}",
                                        headers=headers,
                                        stream=True)
                    t_12z.close()
                    
                    t_06z = requests.get(f"{today_06z_url}{file_06z}",
                                        headers=headers,
                                        stream=True)
                    t_06z.close()
                    
                    t_00z = requests.get(f"{today_00z_url}{file_00z}",
                                        headers=headers,
                                        stream=True)
                    t_00z.close()
                    
                    y_18z = requests.get(f"{yesterday_18z_url}{file_18z}",
                                        headers=headers,
                                        stream=True)
                    y_18z.close()
                    
                    y_12z = requests.get(f"{yesterday_12z_url}{file_12z}",
                                        headers=headers,
                                        stream=True)
                    y_12z.close()
                    
                    y_06z = requests.get(f"{yesterday_06z_url}{file_06z}",
                                        headers=headers,
                                        stream=True)
                    y_06z.close()
                    
                    y_00z = requests.get(f"{yesterday_00z_url}{file_00z}",
                                        headers=headers,
                                        stream=True)
                    y_00z.close()
                except Exception as e:
                    i = i
                    if i >= 9:
                        print(f"Error: Client unable to establish a connection to the server. - System Exit.")
                        sys.exit(1)
                    else:
                        pass
                    
    else:
        try:
            t_18z = requests.get(f"{today_18z_url}{file_18z}",
                                 headers=headers,
                                 stream=True,
                                 proxies=proxies)
            t_18z.close()
            
            t_12z = requests.get(f"{today_12z_url}{file_12z}",
                                 headers=headers,
                                 stream=True,
                                 proxies=proxies)
            t_12z.close()
            
            t_06z = requests.get(f"{today_06z_url}{file_06z}",
                                 headers=headers,
                                 stream=True,
                                 proxies=proxies)
            t_06z.close()
            
            t_00z = requests.get(f"{today_00z_url}{file_00z}",
                                 headers=headers,
                                 stream=True,
                                 proxies=proxies)
            t_00z.close()
            
            y_18z = requests.get(f"{yesterday_18z_url}{file_18z}",
                                 headers=headers,
                                 stream=True,
                                 proxies=proxies)
            y_18z.close()
            
            y_12z = requests.get(f"{yesterday_12z_url}{file_12z}",
                                 headers=headers,
                                 stream=True,
                                 proxies=proxies)
            y_12z.close()
            
            y_06z = requests.get(f"{yesterday_06z_url}{file_06z}",
                                 headers=headers,
                                 stream=True,
                                 proxies=proxies)
            y_06z.close()
            
            y_00z = requests.get(f"{yesterday_00z_url}{file_00z}",
                                 headers=headers,
                                 stream=True,
                                 proxies=proxies)
            y_00z.close()
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(60)
                try:
                    t_18z = requests.get(f"{today_18z_url}{file_18z}",
                                        headers=headers,
                                        stream=True,
                                        proxies=proxies)
                    t_18z.close()
                    
                    t_12z = requests.get(f"{today_12z_url}{file_12z}",
                                        headers=headers,
                                        stream=True,
                                        proxies=proxies)
                    t_12z.close()
                    
                    t_06z = requests.get(f"{today_06z_url}{file_06z}",
                                        headers=headers,
                                        stream=True,
                                        proxies=proxies)
                    t_06z.close()
                    
                    t_00z = requests.get(f"{today_00z_url}{file_00z}",
                                        headers=headers,
                                        stream=True,
                                        proxies=proxies)
                    t_00z.close()
                    
                    y_18z = requests.get(f"{yesterday_18z_url}{file_18z}",
                                        headers=headers,
                                        stream=True,
                                        proxies=proxies)
                    y_18z.close()
                    
                    y_12z = requests.get(f"{yesterday_12z_url}{file_12z}",
                                        headers=headers,
                                        stream=True,
                                        proxies=proxies)
                    y_12z.close()
                    
                    y_06z = requests.get(f"{yesterday_06z_url}{file_06z}",
                                        headers=headers,
                                        stream=True,
                                        proxies=proxies)
                    y_06z.close()
                    
                    y_00z = requests.get(f"{yesterday_00z_url}{file_00z}",
                                        headers=headers,
                                        stream=True,
                                        proxies=proxies)
                    y_00z.close()
                except Exception as e:
                    i = i
                    if i >= 9:
                        print(f"Error: Client unable to establish a connection to the server. - System Exit.")
                        sys.exit(1)
                    else:
                        pass
                    
    
    responses = [
        t_18z,
        t_12z,
        t_06z,
        t_00z,
        y_18z,
        y_12z,
        y_06z,
        y_00z
    ]
                    
    urls = [
        today_18z_url,
        today_12z_url,
        today_06z_url,
        today_00z_url,
        yesterday_18z_url,
        yesterday_12z_url,
        yesterday_06z_url,
        yesterday_00z_url
    ]
                    
                    
    files = [
        file_18z,
        file_12z,
        file_06z,
        file_00z,
        file_18z,
        file_12z,
        file_06z,
        file_00z
    ]
    
    for r, u, f in zip(responses, urls, files):
        if r.status_code == 200:
            url = u
            run = int(f[10:12])
            filename = f
            break
        else:
            pass
        
    return url, run, filename
                    