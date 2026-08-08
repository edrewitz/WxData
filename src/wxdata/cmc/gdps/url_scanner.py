"""
This file hosts the URL Scanner for the GDPS

(C) Eric J. Drewitz 2025-2026
"""

import requests
import sys
import time
import wxdata.cmc.gdps._exceptions as _exceptions

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

# Gets local time
local = datetime.now()

# Gets yesterday's date
yd = now - timedelta(days=1)

PREFIX_TODAY_12Z = f"https://dd.weather.gc.ca/{now.strftime('%Y%m%d')}/WXO-DD/model_gdps/15km/12"
PREFIX_TODAY_00Z = f"https://dd.weather.gc.ca/{now.strftime('%Y%m%d')}/WXO-DD/model_gdps/15km/00"
PREFIX_YESTERDAY_12Z = f"https://dd.weather.gc.ca/{yd.strftime('%Y%m%d')}/WXO-DD/model_gdps/15km/12"
PREFIX_YESTERDAY_00Z = f"https://dd.weather.gc.ca/{yd.strftime('%Y%m%d')}/WXO-DD/model_gdps/15km/00"


def gdps_url_scanner(final_forecast_hour,
                                    proxies,
                                    type_of_level,
                                    parameter,
                                    levels,
                                    step):
    
    """
    This function scans for the latest available GDPS data from https://dd.weather.gc.ca/
    
    Required Arguments:
    
    1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GFS0P25
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 6 hours. 
    
    2) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    3) type_of_level (String) - The type of level surface for the variable.
    
        Types of Levels
        ---------------
        
        'pressure'
        'surface'
        'height above ground'
        'pressure layer'
        'depth below surface'
        'mean sea level'
        'potential vorticity surface'
        'entire atmosphere'
        
    4) parameter (String) - Parameter the user is requesting.
    
    5) levels (Integer or Float list) - The level(s) the user wishes to download. 

        if type_of_level='pressure' => levels=[pressure level] (levels=[500] = example for 500mb)
        if type_of_level='height above ground' => levels=[height above ground level] (levels=[10] = example for 10m)
        if type_of_level='pressure layer' => levels=[pressure at lower level, pressure at higher level] (levels=[1000, 500] = example for 1000mb to 500mb)
        if type_of_level='depth below surface' => levels=[height of higher level, height at lower level] (levels=[0, 10] = example for 0cm to 10cm)
        if type_of_level='potential vorticity surface' => levels=[potential vorticity surface] (levels=[1.5] = example for 1.5 PVU)
        
    6) step (Integer) - Increment of forecast hours. 
    
    Optional Arguments: None
    
    Returns
    ------
    
    A list of full URLs for the client to download the GDPS files. 
    """
    type_of_level = type_of_level.lower()
    
    if final_forecast_hour > 240:
        final_forecast_hour = 240
        print("Maximum value for final_forecast_hour is 240.\nDefaulting to 240.")
    else:
        final_forecast_hour = final_forecast_hour
    
    if final_forecast_hour < 10:
        final_forecast_hour = f"00{final_forecast_hour}"
    elif final_forecast_hour >= 10 and final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = final_forecast_hour
    
    url_12z_today = f"{PREFIX_TODAY_12Z}/{final_forecast_hour}/"
    url_00z_today = f"{PREFIX_TODAY_00Z}/{final_forecast_hour}/"
    url_12z_yesterday = f"{PREFIX_YESTERDAY_12Z}/{final_forecast_hour}/"
    url_00z_yesterday = f"{PREFIX_YESTERDAY_00Z}/{final_forecast_hour}/"
    
    if type_of_level == 'pressure':
        
        has_levels = True
        level = levels[0]
        
        if level < 10:
            level = f"000{level}"
        elif level >= 10 and level < 100:
            level = f"00{level}"
        elif level >= 100 and level < 1000:
            level = f"0{level}"
        else:
            level = f"{level}"
            
        file_12z_today = f"{now.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_IsbL-{level}_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_today = f"{now.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_IsbL-{level}_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_12z_yesterday = f"{yd.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_IsbL-{level}_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_yesterday = f"{yd.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_IsbL-{level}_LatLon0.15_PT{final_forecast_hour}H.grib2"
        
    elif type_of_level == 'surface':
        
        has_levels = False
        file_12z_today = f"{now.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_Sfc_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_today = f"{now.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_Sfc_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_12z_yesterday = f"{yd.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_Sfc_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_yesterday = f"{yd.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_Sfc_LatLon0.15_PT{final_forecast_hour}H.grib2"
        
    elif type_of_level == 'height above ground':
        
        has_levels = True
        level = levels[0]
        
        file_12z_today = f"{now.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_AGL-{level}m_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_today = f"{now.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_AGL-{level}m_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_12z_yesterday = f"{yd.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_AGL-{level}m_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_yesterday = f"{yd.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_AGL-{level}m_LatLon0.15_PT{final_forecast_hour}H.grib2" 
        
    elif type_of_level == 'pressure layer':
        
        has_levels = True
        
        level_low = levels[0]
        level_high = levels[1]
        
        if level_low < 10:
            level_low = f"000{level_low}"
        elif level_low >= 10 and level_low < 100:
            level_low = f"00{level_low}"
        elif level_low >= 100 and level_low < 1000:
            level_low = f"0{level_low}"
        else:
            level_low = f"{level_low}"
            
        if level_high < 10:
            level_high = f"000{level_high}"
        elif level_high >= 10 and level_high < 100:
            level_high = f"00{level_high}"
        elif level_high >= 100 and level_high < 1000:
            level_high = f"0{level_high}"
        else:
            level_high = f"{level_high}"
           
        file_12z_today = f"{now.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_IsbL-{level_low}to{level_high}_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_today = f"{now.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_IsbL-{level_low}to{level_high}_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_12z_yesterday = f"{yd.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_IsbL-{level_low}to{level_high}_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_yesterday = f"{yd.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_IsbL-{level_low}to{level_high}_LatLon0.15_PT{final_forecast_hour}H.grib2"
        
    elif type_of_level == 'depth below surface':
        
        has_levels = True
        
        level_low = levels[0]
        level_high = levels[1]
        
        file_12z_today = f"{now.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_DBS-{level_low}to{level_high}cm_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_today = f"{now.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_DBS-{level_low}to{level_high}cm_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_12z_yesterday = f"{yd.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_DBS-{level_low}to{level_high}cm_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_yesterday = f"{yd.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_DBS-{level_low}to{level_high}cm_LatLon0.15_PT{final_forecast_hour}H.grib2"
        
    elif type_of_level == 'mean sea level':
        
        has_levels = False
        
        file_12z_today = f"{now.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_MSL_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_today = f"{now.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_MSL_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_12z_yesterday = f"{yd.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_MSL_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_yesterday = f"{yd.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_MSL_LatLon0.15_PT{final_forecast_hour}H.grib2"
        
    elif type_of_level == 'potential vorticity surface':
        
        has_levels = True
        
        level = levels[0]
        
        file_12z_today = f"{now.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_PVU-{level}_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_today = f"{now.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_PVU-{level}_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_12z_yesterday = f"{yd.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_PVU-{level}_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_yesterday = f"{yd.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_PVU-{level}_LatLon0.15_PT{final_forecast_hour}H.grib2"
        
    else:
        
        has_levels = False
        
        file_12z_today = f"{now.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_NTAtm_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_today = f"{now.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_NTAtm_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_12z_yesterday = f"{yd.strftime('%Y%m%d')}T12Z_MSC_GDPS_{parameter}_NTAtm_LatLon0.15_PT{final_forecast_hour}H.grib2"
        file_00z_yesterday = f"{yd.strftime('%Y%m%d')}T00Z_MSC_GDPS_{parameter}_NTAtm_LatLon0.15_PT{final_forecast_hour}H.grib2"
        
        
    if proxies == None:
        
        try:
            r0 = requests.get(f"{url_12z_today}{file_12z_today}",
                            stream=True)
            
            r0.close()
            
            r1 = requests.get(f"{url_00z_today}{file_00z_today}",
                                    stream=True)
            
            r1.close()
            
            r2 = requests.get(f"{url_12z_yesterday}{file_12z_yesterday}",
                                    stream=True)
            
            r2.close()
            
            r3 = requests.get(f"{url_00z_yesterday}{file_00z_yesterday}",
                                            stream=True)
            
            r3.close()
            
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(60)
                try:
                    r0 = requests.get(f"{url_12z_today}{file_12z_today}",
                                    stream=True)
                    
                    r0.close()
                    
                    r1 = requests.get(f"{url_00z_today}{file_00z_today}",
                                            stream=True)
                    
                    r1.close()
                    
                    r2 = requests.get(f"{url_12z_yesterday}{file_12z_yesterday}",
                                            stream=True)
                    
                    r2.close()
                    
                    r3 = requests.get(f"{url_00z_yesterday}{file_00z_yesterday}",
                                                    stream=True)  
                    
                    r3.close()
                    break
                except Exception as e:
                    i = i
                    if i >= 9:
                        print("Error: Client cannot establish connection to: https://dd.weather.gc.ca/")   
                        print("System Exit")
                        sys.exit(1)     
                    else:
                        pass         
        
    else:
        
        try:
            r0 = requests.get(f"{url_12z_today}{file_12z_today}",
                        stream=True,
                        proxies=proxies)
            
            r0.close()
            
            r1 = requests.get(f"{url_00z_today}{file_00z_today}",
                            stream=True,
                            proxies=proxies)
            
            r1.close()
            
            r2 = requests.get(f"{url_12z_yesterday}{file_12z_yesterday}",
                            stream=True,
                            proxies=proxies)
            
            r2.close()
            
            r3 = requests.get(f"{url_00z_yesterday}{file_00z_yesterday}",
                            stream=True,
                            proxies=proxies)
            
            r3.close()
            
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(60)
                try:
                    r0 = requests.get(f"{url_12z_today}{file_12z_today}",
                                    stream=True,
                                    proxies=proxies)
                    
                    r0.close()
                    
                    r1 = requests.get(f"{url_00z_today}{file_00z_today}",
                                    stream=True,
                                    proxies=proxies)
                    
                    r1.close()
                    
                    r2 = requests.get(f"{url_12z_yesterday}{file_12z_yesterday}",
                                    stream=True,
                                    proxies=proxies)
                    
                    r2.close()
                    
                    r3 = requests.get(f"{url_00z_yesterday}{file_00z_yesterday}",
                                    stream=True,
                                    proxies=proxies)  
                    
                    r3.close()
                    
                    break
                except Exception as e:
                    i = i
                    if i >= 9:
                        print("Error: Client cannot establish connection to: https://dd.weather.gc.ca/")   
                        print("System Exit")
                        sys.exit(1)     
                    else:
                        pass   
    
        
    responses = []
    responses.append(r0)
    responses.append(r1)
    responses.append(r2)
    responses.append(r3)
    
    prefix_list = []
    prefix_list.append(PREFIX_TODAY_12Z)
    prefix_list.append(PREFIX_TODAY_00Z)
    prefix_list.append(PREFIX_YESTERDAY_12Z)
    prefix_list.append(PREFIX_YESTERDAY_00Z)
    
    for r, p in zip(responses, prefix_list):
        if r.status_code == 200:
            prefix = p
            if p == PREFIX_TODAY_12Z:
                run = '12'
                date = f"{now.strftime('%Y%m%d')}"
            elif p == PREFIX_TODAY_00Z:
                run = '00'
                date = f"{now.strftime('%Y%m%d')}"
            elif p == PREFIX_YESTERDAY_12Z:
                run = '12'
                date = f"{yd.strftime('%Y%m%d')}"
            else:
                run = '00'
                date = f"{yd.strftime('%Y%m%d')}"
            break
        else:
            pass
        
    urls = []
    files = []
    
    for i in range(0, int(final_forecast_hour) + step, step):
        if i < 10:
            hour = f"00{i}"
        elif i >= 10 and i < 100:
            hour = f"0{i}"
        else:
            hour = f"{i}"
            
        try:    
            url = f"{prefix}/{hour}/"
        except Exception as e:
            _exceptions.invalid_info(has_levels)
            
            sys.exit(1)
            
        urls.append(url)

        if type_of_level == 'pressure':
            
            level = levels[0]      
            if level < 10:
                level = f"000{level}"
            elif level >= 10 and level < 100:
                level = f"00{level}"
            elif level >= 100 and level < 1000:
                level = f"0{level}"
            else:
                level = f"{level}"
                
            file = f"{date}T{run}Z_MSC_GDPS_{parameter}_IsbL-{level}_LatLon0.15_PT{hour}H.grib2"
            
        elif type_of_level == 'surface':
            
            file = f"{date}T{run}Z_MSC_GDPS_{parameter}_Sfc_LatLon0.15_PT{hour}H.grib2"
            
        elif type_of_level == 'height above ground':
            
                level = levels[0]
                
                f"{date}T{run}Z_MSC_GDPS_{parameter}_AGL-{level}m_LatLon0.15_PT{hour}H.grib2"
                
        elif type_of_level == 'pressure layer':
        
            level_low = levels[0]
            level_high = levels[1]
            
            if level_low < 10:
                level_low = f"000{level_low}"
            elif level_low >= 10 and level_low < 100:
                level_low = f"00{level_low}"
            elif level_low >= 100 and level_low < 1000:
                level_low = f"0{level_low}"
            else:
                level_low = f"{level_low}"
                
            if level_high < 10:
                level_high = f"000{level_high}"
            elif level_high >= 10 and level_high < 100:
                level_high = f"00{level_high}"
            elif level_high >= 100 and level_high < 1000:
                level_high = f"0{level_high}"
            else:
                level_high = f"{level_high}"
            
            file = f"{date}T{run}Z_MSC_GDPS_{parameter}_IsbL-{level_low}to{level_high}_LatLon0.15_PT{hour}H.grib2"
        
        elif type_of_level == 'depth below surface':
            
            level_low = levels[0]
            level_high = levels[1]
            
            file = f"{date}T{run}Z_MSC_GDPS_{parameter}_DBS-{level_low}to{level_high}cm_LatLon0.15_PT{hour}H.grib2"
        
        elif type_of_level == 'mean sea level':
        
            file = f"{date}T{run}Z_MSC_GDPS_{parameter}_MSL_LatLon0.15_PT{hour}H.grib2"
            
        elif type_of_level == 'potential vorticity surface':
                
            level = levels[0]
                
            file = f"{date}T{run}Z_MSC_GDPS_{parameter}_PVU-{level}_LatLon0.15_PT{hour}H.grib2"
            
        else:
            
            file = f"{date}T{run}Z_MSC_GDPS_{parameter}_NTAtm_LatLon0.15_PT{hour}H.grib2"
            
        files.append(file)
    
    
    full_urls = []
    
    for u, f in zip(urls, files):
        
        full_url = f"{u}{f}"
        
        full_urls.append(full_url)
        
    url_responses = []
    
    for f in full_urls:
        if proxies == None:
            response = requests.get(f"{f}",
                                    stream=True)
            
        else:
            response = requests.get(f"{f}",
                                    stream=True,
                                    proxies=proxies)
        response.close()
            
        url_responses.append(response)
        
    filtered_urls = []
    
    for r, u in zip(url_responses, full_urls):
        if r.status_code == 200:
            filtered_urls.append(u)
        else:
            pass
    
    return filtered_urls
        
            
        