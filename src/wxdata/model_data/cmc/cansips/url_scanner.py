"""
This file hosts the URL Scanner for the CanSIPS

(C) Eric J. Drewitz 2025-2026
"""
import requests
import sys
import time
import wxdata.model_data.cmc.utils._exceptions as _exceptions

from wxdata.model_data.cmc.utils.filenames import get_filenames
from wxdata.model_data.cmc.utils.cmc_keys import cansips_variable_keys
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

CURRENT_MONTH_DIRECTORY = f"https://dd.weather.gc.ca/{now.strftime('%Y%m%d')}/WXO-DD/model_cansips/100km/forecast/{now.strftime('%Y')}/{now.strftime('%m')}/"
PREVIOUS_MONTH_DIRECTORY = f"https://dd.weather.gc.ca/{last_month.strftime('%Y%m%d')}/WXO-DD/model_cansips/100km/forecast/{last_month.strftime('%Y')}/{last_month.strftime('%m')}/"

def _invalid_category(category):
    
    """
    Returns an error message for an invalid category.
    """
    
    print(f"Error: '{category}' is not a valid category.\nPlease try again")
    sys.exit(1)
    
def _invalid_level_type(level_type):
    
    """
    Returns an error message for an invalid level type.
    """
    
    print(f"Error: '{level_type}' is not a valid level type.\nPlease try again")
    sys.exit(1)

def _get_category(category):
    
    """
    This function maps the category (if one exists) to this portion on the filename for our HTTP request.
    
    Required Arguments: 
    
    1) category (String) - The category of the data.
    
    ***Category List***
    
    'probability above normal'
    'probability below normal'
    'probability near normal'
    'probability > 10th percentile'
    'probability > 20th percentile'
    'probability > 30th percentile'
    'probability > 40th percentile'
    'probability > 50th percentile'
    'probability > 60th percentile'
    'probability > 70th percentile'
    'probability > 80th percentile'
    'probability > 90th percentile'
    
    Optional Arguments: None
    
    Returns
    -------
    
    The category of the data (if one exists) on the filename for our HTTP request.    
    """
    
    categories = {
        
        'probability above normal':'ProbAboveNormal',
        'probability below normal':'ProbBelowNormal',
        'probability near normal':'ProbNearNormal',
        'probability > 10th percentile':'ProbGT10Pct',
        'probability > 20th percentile':'ProbGT20Pct',
        'probability > 30th percentile':'ProbGT30Pct',
        'probability > 40th percentile':'ProbGT40Pct',
        'probability > 50th percentile':'ProbGT50Pct',
        'probability > 60th percentile':'ProbGT60Pct',
        'probability > 70th percentile':'ProbGT70Pct',
        'probability > 80th percentile':'ProbGT80Pct',
        'probability > 90th percentile':'ProbGT90Pct'
        
    }
    
    try:
        return categories[category]
    except Exception as e:
        _invalid_category(category)
        
def _get_level_type(level_type):
    
    """
    This function returns the level type of the parameter for our HTTP request
    
    Required Arguments:
    
    1) level_type (String) - The level type.
    
    ***Level Types***
    
        'height above ground'
        'pressure'
        'surface'
        'geoid'
        'mean sea level'
    
    
    Optional Arguments: None
    
    Returns
    -------
    
    The level type on the filename for our HTTP request.
    """
    
    level_types = {
        
        'height above ground':'AGL',
        'pressure':'ISBL',
        'surface':'Sfc',
        'geoid':'Geoid',
        'mean sea level':'MSL'
    }
    
    try:
        return level_types[level_type]
    except Exception as e:
        _invalid_level_type(level_type)
        
        
def cansips_url_scanner(level_type,
                        proxies,
                        variable,
                        level,
                        category,
                        period):
    
    
    """
    This function scans for the latest available CanSIPS data from https://dd.weather.gc.ca/
    
    Required Arguments:
    
    1) level_type (String) - The type of level surface for the variable.
    
    ***Level Types***
    
        'height above ground'
        'pressure'
        'surface'
        'geoid'
        'mean sea level'
        
    2) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    3) variable (String) - Variable the user is requesting.
    
    ***Variable List***
    
        'temperature'
        'geopotential height'
        'precipitation'
        'precipitation rate'
        'pressure'
        'sea surface height'
        'sea surface temperature'
        'u-wind component'
        'v-wind component'
       
    
    4) level (Integer) - The pressure level in hPa or height above ground in meters.
    
    5) category (String or None) - The type of probabilistic category. If not requesting a probabilistic forecast set this to None.
    
    ***Category List***
    
    'probability above normal'
    'probability below normal'
    'probability near normal'
    'probability > 10th percentile'
    'probability > 20th percentile'
    'probability > 30th percentile'
    'probability > 40th percentile'
    'probability > 50th percentile'
    'probability > 60th percentile'
    'probability > 70th percentile'
    'probability > 80th percentile'
    'probability > 90th percentile'
    
    6) period (String) - The forecast increment (monthly or seasonal [3-month])
    
    Returns
    -------
    
    The user can recieve either 1 of 2 things:
    
    1) A list of full download URLs for the client.
    
    2) An error message for an invalid request with instructions on how to correct the user-error. 
    
    """
    period = period.lower()
    level_type = level_type.lower()
    variable = variable.lower()
    level_abbrev = _get_level_type(level_type)
    variable = cansips_variable_keys(variable)
    
    current_files = []
    previous_files = []
    if category != None:
        category = _get_category(category)
        if level_type == 'height above ground':
            if period == 'seasonal':
                for i in range(0, 10, 1):
                    if i < 8:
                        cname = f"{now.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_{level_abbrev}-{level}m_LatLon1.0_P0{i}M-P0{i+2}M.grib2"
                        pname = f"{last_month.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_{level_abbrev}-{level}m_LatLon1.0_P0{i}M-P0{i+2}M.grib2"
                    else:
                        cname = f"{now.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_{level_abbrev}-{level}m_LatLon1.0_P0{i}M-P{i+2}M.grib2"
                        pname = f"{last_month.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_{level_abbrev}-{level}m_LatLon1.0_P0{i}M-P{i+2}M.grib2"
                    
                    current_files.append(cname)
                    previous_files.append(pname)
            else:
                for i in range(0, 12, 1):
                    if i < 10:
                        cname = f"{now.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_{level_abbrev}-{level}m_LatLon1.0_P0{i}M.grib2"
                        pname = f"{last_month.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_{level_abbrev}-{level}m_LatLon1.0_P0{i}M.grib2"
                    else:
                        cname = f"{now.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_{level_abbrev}-{level}m_LatLon1.0_P{i}M.grib2"
                        pname = f"{last_month.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_{level_abbrev}-{level}m_LatLon1.0_P{i}M.grib2"
                    
                    current_files.append(cname)
                    previous_files.append(pname)
        else:
            if period == 'seasonal':
                for i in range(0, 10, 1):
                    if i < 8:
                        cname = f"{now.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_Sfc_LatLon1.0_P0{i}M-P0{i+2}M.grib2"
                        pname = f"{last_month.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_Sfc_LatLon1.0_P0{i}M-P0{i+2}M.grib2"
                    else:
                        cname = f"{now.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_Sfc_LatLon1.0_P0{i}M-P{i+2}M.grib2"
                        pname = f"{last_month.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_Sfc_LatLon1.0_P0{i}M-P{i+2}M.grib2"
                    
                    current_files.append(cname)
                    previous_files.append(pname)
            else:
                for i in range(0, 12, 1):
                    if i < 10:
                        cname = f"{now.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_Sfc_LatLon1.0_P0{i}M.grib2"
                        pname = f"{last_month.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_Sfc_LatLon1.0_P0{i}M.grib2"
                    else:
                        cname = f"{now.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_Sfc_LatLon1.0_P{i}M.grib2"
                        pname = f"{last_month.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{category}_Sfc_LatLon1.0_P{i}M.grib2"
                    
                    current_files.append(cname)
                    previous_files.append(pname)
    else:
        if level_type == 'pressure':
            if period == 'seasonal':
                _exceptions.invalid_cansips_request()
            else:
                for i in range(0, 12, 1):
                    if i < 10:
                        cname = f"{now.strftime('%Y%m')}_MSC_CanSIPS_{variable}_{level_abbrev}-0{level}_LatLon1.0_P0{i}M.grib2"
                        pname = f"{last_month.strftime('%Y%m')}_MSC_CanSIPS_{variable}_{level_abbrev}-0{level}_LatLon1.0_P0{i}M.grib2"
                    else:
                        cname = f"{now.strftime('%Y%m')}_MSC_CanSIPS_{variable}_{level_abbrev}-0{level}_LatLon1.0_P{i}M.grib2"
                        pname = f"{last_month.strftime('%Y%m')}_MSC_CanSIPS_{variable}_{level_abbrev}-0{level}_LatLon1.0_P{i}M.grib2"
                    
                    current_files.append(cname)
                    previous_files.append(pname)  
                    
        elif level_type == 'geoid':
            if period == 'seasonal':
                _exceptions.invalid_cansips_request()
            else:
                for i in range(0, 12, 1):
                    if i < 10:
                        cname = f"{now.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{level_abbrev}_LatLon1.0_P0{i}M.grib2"
                        pname = f"{last_month.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{level_abbrev}_LatLon1.0_P0{i}M.grib2"
                    else:
                        cname = f"{now.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{level_abbrev}_LatLon1.0_P{i}M.grib2"
                        pname = f"{last_month.strftime('%Y%m')}_MSC_CanSIPS_{variable}-{level_abbrev}_LatLon1.0_P{i}M.grib2"
                    
                    current_files.append(cname)
                    previous_files.append(pname)  
        
        else:
            if period == 'seasonal':
                _exceptions.invalid_cansips_request()
            else:
                for i in range(0, 12, 1):
                    if i < 10:
                        cname = f"{now.strftime('%Y%m')}_MSC_CanSIPS_{variable}_{level_abbrev}_LatLon1.0_P0{i}M.grib2"
                        pname = f"{last_month.strftime('%Y%m')}_MSC_CanSIPS_{variable}_{level_abbrev}_LatLon1.0_P0{i}M.grib2"
                    else:
                        cname = f"{now.strftime('%Y%m')}_MSC_CanSIPS_{variable}_{level_abbrev}_LatLon1.0_P{i}M.grib2"
                        pname = f"{last_month.strftime('%Y%m')}_MSC_CanSIPS_{variable}_{level_abbrev}_LatLon1.0_P{i}M.grib2"
                    
                    current_files.append(cname)
                    previous_files.append(pname)       
        
                
    
    if proxies == None:
        try:
            r0 = requests.get(f"{CURRENT_MONTH_DIRECTORY}{current_files[-1]}",
                                stream=True)
            
            r0.close()
            
            r1 = requests.get(f"{PREVIOUS_MONTH_DIRECTORY}{previous_files[-1]}",
                                stream=True)
            
            r1.close()
        except Exception as e:
            for i in range(0, 10, 1):
                try:
                    time.sleep(60)
                    r0 = requests.get(f"{CURRENT_MONTH_DIRECTORY}{current_files[-1]}",
                                        stream=True)
                    
                    r0.close()
                    
                    r1 = requests.get(f"{PREVIOUS_MONTH_DIRECTORY}{previous_files[-1]}",
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
            r0 = requests.get(f"{CURRENT_MONTH_DIRECTORY}{current_files[-1]}",
                                stream=True,
                                proxies=proxies)
            
            r0.close()
            
            r1 = requests.get(f"{PREVIOUS_MONTH_DIRECTORY}{previous_files[-1]}",
                                stream=True,
                                proxies=proxies)
            
            r1.close()
        except Exception as e:
            for i in range(0, 10, 1):
                try:
                    time.sleep(60)
                    r0 = requests.get(f"{CURRENT_MONTH_DIRECTORY}{current_files[-1]}",
                                        stream=True,
                                        proxies=proxies)
                    
                    r0.close()
                    
                    r1 = requests.get(f"{PREVIOUS_MONTH_DIRECTORY}{previous_files[-1]}",
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
                    
              
    responses = [r0, r1]
    urls = [CURRENT_MONTH_DIRECTORY, 
            PREVIOUS_MONTH_DIRECTORY]
    
    file_lists = [current_files,
                  previous_files]
    
    for r, u, f in zip(responses, urls, file_lists):
        if r.status_code == 200:
            url = u
            files = f
            break
        else:
            pass
        
        
    download_urls = []
    try:
        for f in files:
            download_url = f"{url}{f}"
            download_urls.append(download_url)
    except Exception as e:
        _exceptions.invalid_cansips_request()
        
    return download_urls, files
        
        
            
    
                        

        
        
    
    
    
    
    