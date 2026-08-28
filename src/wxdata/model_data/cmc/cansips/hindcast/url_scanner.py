"""
This file hosts the URL Scanner for the CanSIPS Hindcasts

(C) Eric J. Drewitz 2025-2026
"""
import requests
import sys
import time
import wxdata.model_data.cmc.utils._exceptions as _exceptions

from wxdata.model_data.cmc.utils.filenames import get_filenames
from wxdata.model_data.cmc.utils.cmc_keys import cansips_hindcast_keys
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
last_month = now - timedelta(days=31)

if now.month < 10:
    month = f"0{now.month}"
else:
    month = f"{now.month}"
    
if last_month.month < 10:
    prev_month = f"0{last_month.month}"
else:
    prev_month = f"{last_month.month}"

current_dirs = []
prev_dirs = []
for i in range(1991, 2021, 1):
    current_dir = f"https://dd.weather.gc.ca/{now.strftime('%Y%m%d')}/WXO-DD/model_cansips/100km/hindcast/{i}/{month}/"
    previous_dir = f"https://dd.weather.gc.ca/{now.strftime('%Y%m%d')}/WXO-DD/model_cansips/100km/hindcast/{i}/{prev_month}/"
    current_dirs.append(current_dir)
    prev_dirs.append(previous_dir)


def cansips_hindcast_url_scanner(level_type,
                                 variable,
                                 level,
                                 proxies):
    
    """
    This function scans for the latest available CanSIPS hindcast data from https://dd.weather.gc.ca/
    
    Required Arguments:
    
    1) level_type (String) - The type of level surface for the variable.
    
    ***Level Types***
    
        'height above ground'
        'pressure'
        'surface'
        'geoid'
        'mean sea level'
        
    2) variable (String) - Variable the user is requesting.
    
    ***Variable List***
    
        'temperature'
        'geopotential height'
        'precipitation rate'
        'pressure'
        'sea surface height'
        'sea surface temperature'
        'u-wind component'
        'v-wind component'
        
    3) level (Integer) - The pressure level in hPa or height above ground in meters.
    
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    Optional Arguments: None
    
    Returns
    -------
    
    A list of all the download URLs and the filenames of the files being downloaded.     
    """
    
    variable = cansips_hindcast_keys(variable)
    
    level_type = level_type.lower()
    
    current_files = []
    prev_files = []
    if level_type == 'height above ground':
        for j in range(1991, 2021, 1):
            current = []
            prev = []
            for i in range(0, 12, 1):
                if i < 10:
                    current_file = f"{j}{month}_MSC_CanSIPS-Hindcast_{variable}_AGL-{level}m_LatLon1.0_P0{i}M.grib2"
                    prev_file = f"{j}{prev_month}_MSC_CanSIPS-Hindcast_{variable}_AGL-{level}m_LatLon1.0_P0{i}M.grib2"
                else:
                    current_file = f"{j}{month}_MSC_CanSIPS-Hindcast_{variable}_AGL-{level}m_LatLon1.0_P{i}M.grib2"
                    prev_file = f"{j}{prev_month}_MSC_CanSIPS-Hindcast_{variable}_AGL-{level}m_LatLon1.0_P{i}M.grib2"
                    
                current.append(current_file)
                prev.append(prev_file)
                
            current_files.append(current)
            prev_files.append(prev)
        
    elif level_type == 'pressure':
        
        if level < 1000:
            level = f"0{level}"
        else:
            level = level
        
        for j in range(1991, 2021, 1):
            current = []
            prev = []
            for i in range(0, 12, 1):
                if i < 10:
                    current_file = f"{j}{month}_MSC_CanSIPS-Hindcast_{variable}_ISBL-{level}_LatLon1.0_P0{i}M.grib2"
                    prev_file = f"{j}{prev_month}_MSC_CanSIPS-Hindcast_{variable}_ISBL-{level}_LatLon1.0_P0{i}M.grib2"
                else:
                    current_file = f"{j}{month}_MSC_CanSIPS-Hindcast_{variable}_ISBL-{level}_LatLon1.0_P{i}M.grib2"
                    prev_file = f"{j}{prev_month}_MSC_CanSIPS-Hindcast_{variable}_ISBL-{level}_LatLon1.0_P{i}M.grib2"
                    
                current.append(current_file)
                prev.append(prev_file)
                
            current_files.append(current)
            prev_files.append(prev)
        
    elif level_type == 'surface':
        for j in range(1991, 2021, 1):
            current = []
            prev = []
            for i in range(0, 12, 1):
                if i < 10:
                    current_file = f"{j}{month}_MSC_CanSIPS-Hindcast_{variable}_Sfc_LatLon1.0_P0{i}M.grib2"
                    prev_file = f"{j}{prev_month}_MSC_CanSIPS-Hindcast_{variable}_Sfc_LatLon1.0_P0{i}M.grib2"
                else:
                    current_file = f"{j}{month}_MSC_CanSIPS-Hindcast_{variable}_Sfc_LatLon1.0_P{i}M.grib2"
                    prev_file = f"{j}{prev_month}_MSC_CanSIPS-Hindcast_{variable}_Sfc_LatLon1.0_P{i}M.grib2"   
                    
                current.append(current_file)
                prev.append(prev_file)   
                
            current_files.append(current)
            prev_files.append(prev)          
        
    elif level_type == 'mean sea level':
        for j in range(1991, 2021, 1):
            current = []
            prev = []
            for i in range(0, 12, 1):
                if i < 10:
                    current_file = f"{j}{month}_MSC_CanSIPS-Hindcast_{variable}_MSL_LatLon1.0_P0{i}M.grib2"
                    prev_file = f"{j}{prev_month}_MSC_CanSIPS-Hindcast_{variable}_MSL_LatLon1.0_P0{i}M.grib2"
                else:
                    current_file = f"{j}{month}_MSC_CanSIPS-Hindcast_{variable}_MSL_LatLon1.0_P{i}M.grib2"
                    prev_file = f"{j}{prev_month}_MSC_CanSIPS-Hindcast_{variable}_MSL_LatLon1.0_P{i}M.grib2"    
                    
                current.append(current_file)
                prev.append(prev_file)   
                
            current_files.append(current)
            prev_files.append(prev)              
        
    else:
        for j in range(1991, 2021, 1):
            current = []
            prev = []
            for i in range(0, 12, 1):
                if i < 10:
                    current_file = f"{j}{month}_MSC_CanSIPS-Hindcast_{variable}-Geoid_LatLon1.0_P0{i}M.grib2"
                    prev_file = f"{j}{prev_month}_MSC_CanSIPS-Hindcast_{variable}-Geoid_LatLon1.0_P0{i}M.grib2"
                else:
                    current_file = f"{j}{month}_MSC_CanSIPS-Hindcast_{variable}-Geoid_LatLon1.0_P{i}M.grib2"
                    prev_file = f"{j}{prev_month}_MSC_CanSIPS-Hindcast_{variable}-Geoid_LatLon1.0_P{i}M.grib2"
                    
                current.append(current_file)
                prev.append(prev_file)   
                
            current_files.append(current)
            prev_files.append(prev)        

    if proxies == None:   
        try:
            r0 = requests.get(f"{current_dirs[-1]}{current_files[-1][-1]}",
                            stream=True)
            r0.close()
            
            r1 = requests.get(f"{prev_dirs[-1]}{prev_files[-1][-1]}",
                            stream=True)
            r1.close()
            
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(60)
                try:
                    r0 = requests.get(f"{current_dirs[-1]}{current_files[-1][-1]}",
                                    stream=True)
                    r0.close()
                    
                    r1 = requests.get(f"{prev_dirs[-1]}{prev_files[-1][-1]}",
                                    stream=True)
                    r1.close() 
                    
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
            r0 = requests.get(f"{current_dirs[-1]}{current_files[-1][-1]}",
                            stream=True,
                            proxies=proxies)
            r0.close()
            
            r1 = requests.get(f"{prev_dirs[-1]}{prev_files[-1][-1]}",
                            stream=True,
                            proxies=proxies)
            r1.close()
            
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(60)
                try:
                    r0 = requests.get(f"{current_dirs[-1]}{current_files[-1][-1]}",
                                    stream=True,
                                    proxies=proxies)
                    r0.close()
                    
                    r1 = requests.get(f"{prev_dirs[-1]}{prev_files[-1][-1]}",
                                    stream=True,
                                    proxies=proxies)
                    r1.close() 
                    
                except Exception as e:
                    i = i
                    if i >= 9:
                        print("Error: Client cannot establish connection to: https://dd.weather.gc.ca/")   
                        print("System Exit")
                        sys.exit(1)     
                    else:
                        pass  
                    
    if r0.status_code == 200:
        dirs = current_dirs
        files = current_files
    elif r0.status_code != 200 and r1.status_code == 200:
        dirs = prev_dirs
        files = prev_files
    else:
        _exceptions.invalid_cansips_hindcast_request()
        sys.exit(1)
        
    urls = []
    for d, f in zip(dirs, files):
        for file in f:
            url = f"{d}{file}"
            urls.append(url)
            
    files = get_filenames(urls)
            
    return urls, files
            
        
        
        
                        
    
    
    
    
    
    