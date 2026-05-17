"""
This file hosts the GFS URL Scanner Functions.

These functions return the URL and filename for the latest available data on the dataservers.

(C) Eric J. Drewitz 2025-2026
"""

import requests
import sys
import time

from wxdata.gfs.exception_messages import forecast_hour_error
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

NCEP_NOMADS_PREFIX = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/"
AMAZON_AWS_PREFIX = f"https://noaa-gfs-bdp-pds.s3.amazonaws.com/"
GOOGLE_CLOUD_PREFIX = f"https://storage.googleapis.com/global-forecast-system/"

def assign_cat(cat):
    
    """
    This function converts the category into the abbreviation used on the NCEP/NOMADS server.
    
    Required Arguments:
    
    1) cat (string) - The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) atmosphere
    2) ocean
    
    Optional Arguments: None
    
    Returns
    -------    
    
    The abbreviation used on NOMADS (atmos or wave)
    """
    
    cats = {
        'atmosphere':'atmos',
        'ocean':'wave'
    }
    
    return cats[cat]

def gfs_0p50_url_scanner(final_forecast_hour, 
                          proxies, 
                          source):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 

    2) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    3) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
    
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, filename and the download URL.      
    """
    source = source.lower()
    if source == 'noaa':
        PREFIX = NCEP_NOMADS_PREFIX
    elif source == 'aws':
        PREFIX = AMAZON_AWS_PREFIX
    else:
        PREFIX = GOOGLE_CLOUD_PREFIX
        
    # This section handles the final forecast hour for the filename
    if final_forecast_hour > 384:
        forecast_hour_error()
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
    today_18z_scan = (f"{PREFIX}gfs.{now.strftime('%Y%m%d')}/18/atmos/")
    today_12z_scan = (f"{PREFIX}gfs.{now.strftime('%Y%m%d')}/12/atmos/")
    today_06z_scan = (f"{PREFIX}gfs.{now.strftime('%Y%m%d')}/06/atmos/")
    today_00z_scan = (f"{PREFIX}gfs.{now.strftime('%Y%m%d')}/00/atmos/")
    
    yesterday_18z_scan = (f"{PREFIX}gfs.{yd.strftime('%Y%m%d')}/18/atmos/")
    yesterday_12z_scan = (f"{PREFIX}gfs.{yd.strftime('%Y%m%d')}/12/atmos/")
    yesterday_06z_scan = (f"{PREFIX}gfs.{yd.strftime('%Y%m%d')}/06/atmos/")
    yesterday_00z_scan = (f"{PREFIX}gfs.{yd.strftime('%Y%m%d')}/00/atmos/")
    
    # The filenames for the different run times
    f_18z = f"gfs.t18z.pgrb2full.0p50.f{final_forecast_hour}"
    f_12z = f"gfs.t12z.pgrb2full.0p50.f{final_forecast_hour}"
    f_06z = f"gfs.t06z.pgrb2full.0p50.f{final_forecast_hour}"
    f_00z = f"gfs.t00z.pgrb2full.0p50.f{final_forecast_hour}"
    
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
            run = int(f"{url[-9]}{url[-8]}")
            break        
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
    
    return url, filename, run

def gfs_0p25_url_scanner(final_forecast_hour, 
                          proxies, 
                          source):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 

    2) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    3) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
    
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, filename and the download URL.     
    """

    source = source.lower()
    if source == 'noaa':
        PREFIX = NCEP_NOMADS_PREFIX
    elif source == 'aws':
        PREFIX = AMAZON_AWS_PREFIX
    else:
        PREFIX = GOOGLE_CLOUD_PREFIX
    
    # This section handles the final forecast hour for the filename
    if final_forecast_hour > 384:
        forecast_hour_error()
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
    today_18z_scan = (f"{PREFIX}gfs.{now.strftime('%Y%m%d')}/18/atmos/")
    today_12z_scan = (f"{PREFIX}gfs.{now.strftime('%Y%m%d')}/12/atmos/")
    today_06z_scan = (f"{PREFIX}gfs.{now.strftime('%Y%m%d')}/06/atmos/")
    today_00z_scan = (f"{PREFIX}gfs.{now.strftime('%Y%m%d')}/00/atmos/")
    
    yesterday_18z_scan = (f"{PREFIX}gfs.{yd.strftime('%Y%m%d')}/18/atmos/")
    yesterday_12z_scan = (f"{PREFIX}gfs.{yd.strftime('%Y%m%d')}/12/atmos/")
    yesterday_06z_scan = (f"{PREFIX}gfs.{yd.strftime('%Y%m%d')}/06/atmos/")
    yesterday_00z_scan = (f"{PREFIX}gfs.{yd.strftime('%Y%m%d')}/00/atmos/")
    
    # The filenames for the different run times
    f_18z = f"gfs.t18z.pgrb2.0p25.f{final_forecast_hour}"
    f_12z = f"gfs.t12z.pgrb2.0p25.f{final_forecast_hour}"
    f_06z = f"gfs.t06z.pgrb2.0p25.f{final_forecast_hour}"
    f_00z = f"gfs.t00z.pgrb2.0p25.f{final_forecast_hour}"
    
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
            run = int(f"{url[-9]}{url[-8]}")
            break        
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
    

    return url, filename, run


def gfs_0p25_secondary_parameters_url_scanner(final_forecast_hour, 
                                                            proxies, 
                                                            source):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 

    2) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    3) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
    
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, filename and the download URL.    
    """
    
    source = source.lower()
    if source == 'noaa':
        PREFIX = NCEP_NOMADS_PREFIX
    elif source == 'aws':
        PREFIX = AMAZON_AWS_PREFIX
    else:
        PREFIX = GOOGLE_CLOUD_PREFIX
        
    # This section handles the final forecast hour for the filename
    if final_forecast_hour > 384:
        forecast_hour_error()
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
    today_18z_scan = (f"{PREFIX}gfs.{now.strftime('%Y%m%d')}/18/atmos/")
    today_12z_scan = (f"{PREFIX}gfs.{now.strftime('%Y%m%d')}/12/atmos/")
    today_06z_scan = (f"{PREFIX}gfs.{now.strftime('%Y%m%d')}/06/atmos/")
    today_00z_scan = (f"{PREFIX}gfs.{now.strftime('%Y%m%d')}/00/atmos/")
    
    yesterday_18z_scan = (f"{PREFIX}gfs.{yd.strftime('%Y%m%d')}/18/atmos/")
    yesterday_12z_scan = (f"{PREFIX}gfs.{yd.strftime('%Y%m%d')}/12/atmos/")
    yesterday_06z_scan = (f"{PREFIX}gfs.{yd.strftime('%Y%m%d')}/06/atmos/")
    yesterday_00z_scan = (f"{PREFIX}gfs.{yd.strftime('%Y%m%d')}/00/atmos/")
    
    # The filenames for the different run times
    f_18z = f"gfs.t18z.pgrb2b.0p25.f{final_forecast_hour}"
    f_12z = f"gfs.t12z.pgrb2b.0p25.f{final_forecast_hour}"
    f_06z = f"gfs.t06z.pgrb2b.0p25.f{final_forecast_hour}"
    f_00z = f"gfs.t00z.pgrb2b.0p25.f{final_forecast_hour}"
    
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
            run = int(f"{url[-9]}{url[-8]}")
            break        
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
    
    return url, filename, run
