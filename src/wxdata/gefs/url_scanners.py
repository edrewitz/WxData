"""
This file hosts the GEFS URL Scanner Functions.

These functions return the URL and filename for the latest available data on the dataservers.

(C) Eric J. Drewitz 2025-2026
"""

import requests
import sys
import numpy as np
import time

from wxdata.gefs.exception_messages import(    
    gefs0p50,
    gefs0p25
)

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

NCEP_NOMADS_PREFIX = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/"
AMAZON_AWS_PREFIX = f"https://noaa-gefs-pds.s3.amazonaws.com/"
GOOGLE_CLOUD_PREFIX = f"https://storage.googleapis.com/gfs-ensemble-forecast-system/"

def gefs_0p50_url_scanner(cat, 
                          final_forecast_hour, 
                          proxies, 
                          members,
                          source):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) cat (string) - The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 

    3) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                            
    4) members (List) The individual ensemble members. There are 30 members in this ensemble.  
    
    5) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, download URL and server response code.     
    """
    # Makes the category all lower case for consistency
    cat = cat.lower()
    
    source = source.lower()
    if source == 'noaa':
        PREFIX = NCEP_NOMADS_PREFIX
    elif source == 'aws':
        PREFIX = AMAZON_AWS_PREFIX
    else:
        PREFIX = GOOGLE_CLOUD_PREFIX
            
    m = []
    for member in members:
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"      
        
        m.append(aa) 
    
    # Gets the file abbreviation based on category
    # Ensemble Mean
    if cat == 'mean':
        aa = f"avg"
    # Ensemble Members
    elif cat == 'members':
        member = members[-1]
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"
    # Control Run
    elif cat == 'control':
        aa = f"c00"
    # Ensemble Spread
    elif cat == 'spread':
        aa = f"spr"
    # User enters an invalid category
    # When a category is invalid - Defaults to Ensemble Mean
    else:
        gefs0p50.gefs0p50_cat_error('gefs0p50')
        aa = f"avg"
        
    # This section handles the final forecast hour for the filename
    if final_forecast_hour > 384:
        gefs0p50.forecast_hour_error()
        final_forecast_hour = 384
    else:
        final_forecast_hour = final_forecast_hour
        
    if final_forecast_hour >= 100:
        final_forecast_hour = f"{final_forecast_hour}"
    elif final_forecast_hour >= 10 and final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = f"00{final_forecast_hour}"
           
    # These are the different download URLs for the various runtimes in the past 24 hours
    
    # URLs to scan for the latest file
    today_18z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/18/atmos/pgrb2ap5/")
    today_12z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/12/atmos/pgrb2ap5/")
    today_06z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/06/atmos/pgrb2ap5/")
    today_00z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/00/atmos/pgrb2ap5/")
    
    yesterday_18z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/18/atmos/pgrb2ap5/")
    yesterday_12z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/12/atmos/pgrb2ap5/")
    yesterday_06z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/06/atmos/pgrb2ap5/")
    yesterday_00z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/00/atmos/pgrb2ap5/")
        
    # The filenames for the different run times
    f_18z = f"ge{aa}.t18z.pgrb2a.0p50.f{final_forecast_hour}"
    f_12z = f"ge{aa}.t12z.pgrb2a.0p50.f{final_forecast_hour}"
    f_06z = f"ge{aa}.t06z.pgrb2a.0p50.f{final_forecast_hour}"
    f_00z = f"ge{aa}.t00z.pgrb2a.0p50.f{final_forecast_hour}"
    
    # Tests the connection for each link. 
    # The first link with a response of 200 will be the download link
    
    # This is if the user has proxy servers disabled
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                stream=True)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                stream=True)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                stream=True)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                stream=True)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                stream=True)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                stream=True)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                stream=True)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                stream=True)
            y_00.close()
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                        stream=True)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                        stream=True)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                        stream=True)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                        stream=True)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                        stream=True)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                        stream=True)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                        stream=True)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                        stream=True)
                    y_00.close()   
                    break
                except Exception as e:
                    i = i     
    
    # This is if the user has a VPN/Proxy Server connection enabled
    else:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                stream=True, 
                                proxies=proxies)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                stream=True, 
                                proxies=proxies)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                stream=True, 
                                proxies=proxies)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                stream=True, 
                                proxies=proxies)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                stream=True, 
                                proxies=proxies)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                stream=True, 
                                proxies=proxies)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                stream=True, 
                                proxies=proxies)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                stream=True, 
                                proxies=proxies)
            y_00.close()
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_00.close()   
                    break
                except Exception as e:
                    i = i  
        
    # Creates a list of URLs and URL responses to loop through when checking
    
    urls = [
        today_18z_scan,
        today_12z_scan,
        today_06z_scan,
        today_00z_scan,
        yesterday_18z_scan,
        yesterday_12z_scan,
        yesterday_06z_scan,
        yesterday_00z_scan
    ]
    
    responses = [
        t_18,
        t_12,
        t_06,
        t_00,
        y_18,
        y_12,
        y_06,
        y_00
    ]
    
    filenames = [
        f_18z,
        f_12z,
        f_06z,
        f_00z,
        f_18z,
        f_12z,
        f_06z,
        f_00z
    ]
    
    # Testing the status code and then returning the first link with a status code of 200
    for response, url, filename in zip(responses, urls, filenames):
        if response.status_code == 200:
            url = url
            run = int(f"{url[-18]}{url[-17]}")
            filename = filename
            break        
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
    
    return url, filename, run


def gefs_0p50_secondary_parameters_url_scanner(cat, 
                                                final_forecast_hour, 
                                                proxies, 
                                                members,
                                                source):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) cat (string) - The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) control
    4) spread
    
    
    2) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The GEFS0P50 SECONDARY PARAMETERS
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 

    3) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                            
    4) members (List) The individual ensemble members. There are 30 members in this ensemble.  
    
    5) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, download URL and server response code.        
    """
    cat = cat.lower()
    
    source = source.lower()
    if source == 'noaa':
        PREFIX = NCEP_NOMADS_PREFIX
    elif source == 'aws':
        PREFIX = AMAZON_AWS_PREFIX
    else:
        PREFIX = GOOGLE_CLOUD_PREFIX
    
    m = []
    for member in members:
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"      
        
        m.append(aa) 
    
    # Gets the file abbreviation based on category
    # Ensemble Mean
    if cat == 'members' or cat == 'mean' or cat == 'spread':
        member = members[-1]
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"
    # Control Run
    elif cat == 'control':
        aa = f"c00"
    # User enters an invalid category
    # When a category is invalid - Defaults to Control Run
    else:
        gefs0p50.gefs0p50_cat_error('gefs0p50 secondary parameters')
        aa = f"c00"
        
    # This section handles the final forecast hour for the filename
    if final_forecast_hour > 384:
        gefs0p50.forecast_hour_error()
        final_forecast_hour = 384
    else:
        final_forecast_hour = final_forecast_hour
        
    if final_forecast_hour >= 100:
        final_forecast_hour = f"{final_forecast_hour}"
    elif final_forecast_hour >= 10 and final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = f"00{final_forecast_hour}"
           
    # These are the different download URLs for the various runtimes in the past 24 hours
    
    # URLs to scan for the latest file
    
    today_18z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/18/atmos/pgrb2bp5/")
    today_12z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/12/atmos/pgrb2bp5/")
    today_06z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/06/atmos/pgrb2bp5/")
    today_00z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/00/atmos/pgrb2bp5/")
    
    yesterday_18z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/18/atmos/pgrb2bp5/")
    yesterday_12z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/12/atmos/pgrb2bp5/")
    yesterday_06z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/06/atmos/pgrb2bp5/")
    yesterday_00z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/00/atmos/pgrb2bp5/")
        
    # The filenames for the different run times
    f_18z = f"ge{aa}.t18z.pgrb2b.0p50.f{final_forecast_hour}"
    f_12z = f"ge{aa}.t12z.pgrb2b.0p50.f{final_forecast_hour}"
    f_06z = f"ge{aa}.t06z.pgrb2b.0p50.f{final_forecast_hour}"
    f_00z = f"ge{aa}.t00z.pgrb2b.0p50.f{final_forecast_hour}"
    
    # Tests the connection for each link. 
    # The first link with a response of 200 will be the download link
    
    # This is if the user has proxy servers disabled
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                stream=True)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                stream=True)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                stream=True)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                stream=True)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                stream=True)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                stream=True)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                stream=True)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                stream=True)
            y_00.close()
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                        stream=True)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                        stream=True)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                        stream=True)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                        stream=True)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                        stream=True)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                        stream=True)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                        stream=True)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                        stream=True)
                    y_00.close()   
                    break
                except Exception as e:
                    i = i     
    
    # This is if the user has a VPN/Proxy Server connection enabled
    else:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                stream=True, 
                                proxies=proxies)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                stream=True, 
                                proxies=proxies)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                stream=True, 
                                proxies=proxies)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                stream=True, 
                                proxies=proxies)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                stream=True, 
                                proxies=proxies)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                stream=True, 
                                proxies=proxies)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                stream=True, 
                                proxies=proxies)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                stream=True, 
                                proxies=proxies)
            y_00.close()
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_00.close()   
                    break
                except Exception as e:
                    i = i         
        
    # Creates a list of URLs and URL responses to loop through when checking
    
    urls = [
        today_18z_scan,
        today_12z_scan,
        today_06z_scan,
        today_00z_scan,
        yesterday_18z_scan,
        yesterday_12z_scan,
        yesterday_06z_scan,
        yesterday_00z_scan
    ]
    
    responses = [
        t_18,
        t_12,
        t_06,
        t_00,
        y_18,
        y_12,
        y_06,
        y_00
    ]
    
    filenames = [
        f_18z,
        f_12z,
        f_06z,
        f_00z,
        f_18z,
        f_12z,
        f_06z,
        f_00z
    ]
    
    # Testing the status code and then returning the first link with a status code of 200
    for response, url, filename in zip(responses, urls, filenames):
        if response.status_code == 200:
            url = url
            filename = filename
            run = int(f"{url[-18]}{url[-17]}")
            break      
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
    

    
    return url, filename, run
            

def gefs_0p25_url_scanner(cat, 
                        final_forecast_hour, 
                        proxies, 
                        members,
                        source):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) cat (string) - The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The GEFS0P25
    goes out to 240 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    240 by the nereast increment of 3 hours. 

    3) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                            
    4) members (List) The individual ensemble members. There are 30 members in this ensemble.  
    
    5) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, download URL and server response code.    
    """
    cat = cat.lower()
    
    source = source.lower()
    if source == 'noaa':
        PREFIX = NCEP_NOMADS_PREFIX
    elif source == 'aws':
        PREFIX = AMAZON_AWS_PREFIX
    else:
        PREFIX = GOOGLE_CLOUD_PREFIX
    
    m = []
    for member in members:
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"      
        
        m.append(aa) 
    
    # Gets the file abbreviation based on category
    # Ensemble Mean
    if cat == 'mean':
        aa = f"avg"
    # Ensemble Members
    elif cat == 'members':
        member = members[-1]
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"
    # Control Run
    elif cat == 'control':
        aa = f"c00"
    # Ensemble Spread
    elif cat == 'spread':
        aa = f"spr"
    # User enters an invalid category
    # When a category is invalid - Defaults to Ensemble Mean
    else:
        gefs0p25.gefs0p25_cat_error()
        aa = f"avg"
        
    # This section handles the final forecast hour for the filename
    if final_forecast_hour > 240:
        gefs0p25.forecast_hour_error()
        final_forecast_hour = 240
    else:
        final_forecast_hour = final_forecast_hour
        
    if final_forecast_hour >= 100:
        final_forecast_hour = f"{final_forecast_hour}"
    elif final_forecast_hour >= 10 and final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = f"00{final_forecast_hour}"
           
    # These are the different download URLs for the various runtimes in the past 24 hours
    
    # URLs to scan for the latest file
    today_18z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/18/atmos/pgrb2sp25/")
    today_12z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/12/atmos/pgrb2sp25/")
    today_06z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/06/atmos/pgrb2sp25/")
    today_00z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/00/atmos/pgrb2sp25/")
    
    yesterday_18z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/18/atmos/pgrb2sp25/")
    yesterday_12z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/12/atmos/pgrb2sp25/")
    yesterday_06z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/06/atmos/pgrb2sp25/")
    yesterday_00z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/00/atmos/pgrb2sp25/")
    
    # The filenames for the different run times
    f_18z = f"ge{aa}.t18z.pgrb2s.0p25.f{final_forecast_hour}"
    f_12z = f"ge{aa}.t12z.pgrb2s.0p25.f{final_forecast_hour}"
    f_06z = f"ge{aa}.t06z.pgrb2s.0p25.f{final_forecast_hour}"
    f_00z = f"ge{aa}.t00z.pgrb2s.0p25.f{final_forecast_hour}"
    
    # Tests the connection for each link. 
    # The first link with a response of 200 will be the download link
    
    # This is if the user has proxy servers disabled
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                stream=True)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                stream=True)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                stream=True)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                stream=True)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                stream=True)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                stream=True)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                stream=True)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                stream=True)
            y_00.close()
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                        stream=True)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                        stream=True)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                        stream=True)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                        stream=True)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                        stream=True)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                        stream=True)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                        stream=True)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                        stream=True)
                    y_00.close()   
                    break
                except Exception as e:
                    i = i     
    
    # This is if the user has a VPN/Proxy Server connection enabled
    else:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                stream=True, 
                                proxies=proxies)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                stream=True, 
                                proxies=proxies)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                stream=True, 
                                proxies=proxies)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                stream=True, 
                                proxies=proxies)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                stream=True, 
                                proxies=proxies)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                stream=True, 
                                proxies=proxies)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                stream=True, 
                                proxies=proxies)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                stream=True, 
                                proxies=proxies)
            y_00.close()
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_00.close()   
                    break
                except Exception as e:
                    i = i  
        
    # Creates a list of URLs and URL responses to loop through when checking
    
    urls = [
        today_18z_scan,
        today_12z_scan,
        today_06z_scan,
        today_00z_scan,
        yesterday_18z_scan,
        yesterday_12z_scan,
        yesterday_06z_scan,
        yesterday_00z_scan
    ]
    
    responses = [
        t_18,
        t_12,
        t_06,
        t_00,
        y_18,
        y_12,
        y_06,
        y_00
    ]
    
    filenames = [
        f_18z,
        f_12z,
        f_06z,
        f_00z,
        f_18z,
        f_12z,
        f_06z,
        f_00z
    ]
    
    # Testing the status code and then returning the first link with a status code of 200

    for response, url, filename in zip(responses, urls, filenames):
        if response.status_code == 200:
            url = url
            filename = filename
            run = int(f"{url[-19]}{url[-18]}")
            break      
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
    

    return url, filename, run