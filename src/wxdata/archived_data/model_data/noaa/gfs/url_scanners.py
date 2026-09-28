"""
This file hosts the scanners that scan the Amazon Web Services (AWS) and/or Google Cloud archived for historical GFS data.

(C) Eric J. Drewitz 2025-2026
"""

import requests
import sys
import time

from wxdata.model_data.noaa.gfs.exception_messages import forecast_hour_error
from datetime import datetime

start = datetime.strptime("2021-01-01:00", "%Y-%m-%d:%H")

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

def gfs_0p50_url_scanner(date,
                         run,
                         final_forecast_hour, 
                          proxies, 
                          source):
    
    
    """
    This function scans for the user requested archived GFS dataset from either Amazon Web Services (AWS) or Google Cloud.
    If one of the servers are down, the scanner will rotate to the other one. 
    
    Required Arguments:
    
    1) date (String or datetime) - The date of the model run.
    
    2) run (Integer) - The model runtime in UTC (0, 6, 12, 18).
    
    3) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 

    4) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    5) source (String) - Default='aws'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) Amazon AWS - source='aws'
        2) Google Cloud - source='google'
    
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, filename and the download URL.      
    """
    
    if type(date) == type(start):
        date = date
    else:
        date = f"{date[0:4]}{date[5:7]}{date[8:10]}"
        date = datetime.strptime(date, "%Y%m%d")
    
    if run == 18 or run == '18':
        run = '18'
    elif run == 12 or run == '12':
        run = '12'
    elif run == 6 or run == '06':
        run = '06'
    else:
        run = '00'
    
    
    source = source.lower()
    if source == 'aws':
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
           
    
    url = (f"{PREFIX}gfs.{date.strftime('%Y%m%d')}/{run}/atmos/")
    file = f"gfs.t{run}z.pgrb2full.0p50.f{final_forecast_hour}"
    
    try:
        if proxies == None:
            response = requests.get(f"{url}{file}", 
                                stream=True)
        else:
            response = requests.get(f"{url}{file}", 
                                        stream=True,
                                        proxies=proxies)
        
        response.close()
    except Exception as e:
        print(f"Error: Client cannot connect to {source.upper()} server.")
        if source == 'aws':
            print(f"Rotating to Google Cloud Server.")
            try:
                url = gfs_0p50_url_scanner(date,
                            run,
                            final_forecast_hour, 
                            proxies, 
                            'google')
            except Exception as e:
                print(f"Error: Client unable to establish a connection with either server. - System Exit.")
                print(f"Tip: Check to make sure there are no typos in your date or run.")
                print(f"Data begins at: {start.strftime('%Y%m%d')} 00z")
                sys.exit(1)
                
        else:
            print(f"Rotating to AWS Server.")
            try:
                url = gfs_0p50_url_scanner(date,
                            run,
                            final_forecast_hour, 
                            proxies, 
                            'aws')
            except Exception as e:
                print(f"Error: Client unable to establish a connection with either server. - System Exit.")
                print(f"Tip: Check to make sure there are no typos in your date or run.")
                print(f"Data begins at: {start.strftime('%Y%m%d')} 00z")
                sys.exit(1)

    
    return url

def gfs_0p25_url_scanner(date,
                         run,
                         final_forecast_hour, 
                          proxies, 
                          source):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) date (String or datetime) - The date of the model run.
    
    2) run (Integer) - The model runtime in UTC (0, 6, 12, 18).
    
    3) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The GEFS0P25
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 

    4) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    5) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) Amazon AWS - source='aws'
        2) Google Cloud - source='google'
    
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, filename and the download URL.     
    """
    
    if type(date) == type(start):
        date = date
    else:
        date = f"{date[0:4]}{date[5:7]}{date[8:10]}"
        date = datetime.strptime(date, "%Y%m%d")
    
    if run == 18 or run == '18':
        run = '18'
    elif run == 12 or run == '12':
        run = '12'
    elif run == 6 or run == '06':
        run = '06'
    else:
        run = '00'

    source = source.lower()
    if source == 'aws':
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
           
    url = (f"{PREFIX}gfs.{date.strftime('%Y%m%d')}/{run}/atmos/")
    file = f"gfs.t{run}z.pgrb2.0p25.f{final_forecast_hour}"

    try:
        if proxies == None:
            response = requests.get(f"{url}{file}", 
                                stream=True)
        else:
            response = requests.get(f"{url}{file}", 
                                        stream=True,
                                        proxies=proxies)
        
        response.close()
    except Exception as e:
        print(f"Error: Client cannot connect to {source.upper()} server.")
        if source == 'aws':
            print(f"Rotating to Google Cloud Server.")
            try:
                url = gfs_0p25_url_scanner(date,
                            run,
                            final_forecast_hour, 
                            proxies, 
                            'google')
            except Exception as e:
                print(f"Error: Client unable to establish a connection with either server. - System Exit.")
                print(f"Tip: Check to make sure there are no typos in your date or run.")
                print(f"Data begins at: {start.strftime('%Y%m%d')} 00z")
                sys.exit(1)
                
        else:
            print(f"Rotating to AWS Server.")
            try:
                url = gfs_0p25_url_scanner(date,
                            run,
                            final_forecast_hour, 
                            proxies, 
                            'aws')
            except Exception as e:
                print(f"Error: Client unable to establish a connection with either server. - System Exit.")
                print(f"Tip: Check to make sure there are no typos in your date or run.")
                print(f"Data begins at: {start.strftime('%Y%m%d')} 00z")
                sys.exit(1)

    
    return url



def gfs_0p25_secondary_parameters_url_scanner(date,
                                              run,
                                              final_forecast_hour, 
                                                proxies, 
                                                source):

    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) date (String or datetime) - The date of the model run.
    
    2) run (Integer) - The model runtime in UTC (0, 6, 12, 18).
    
    3) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The GEFS0P25 Secondary Parameters
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 

    4) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    5) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) Amazon AWS - source='aws'
        2) Google Cloud - source='google'
    
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, filename and the download URL.    
    """
    
    if type(date) == type(start):
        date = date
    else:
        date = f"{date[0:4]}{date[5:7]}{date[8:10]}"
        date = datetime.strptime(date, "%Y%m%d")
    
    if run == 18 or run == '18':
        run = '18'
    elif run == 12 or run == '12':
        run = '12'
    elif run == 6 or run == '06':
        run = '06'
    else:
        run = '00'
    
    source = source.lower()
    if source == 'aws':
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
           
    url = (f"{PREFIX}gfs.{date.strftime('%Y%m%d')}/{run}/atmos/")
    file = f"gfs.t{run}z.pgrb2b.0p25.f{final_forecast_hour}"

    try:
        if proxies == None:
            response = requests.get(f"{url}{file}", 
                                stream=True)
        else:
            response = requests.get(f"{url}{file}", 
                                        stream=True,
                                        proxies=proxies)
        
        response.close()
    except Exception as e:
        print(f"Error: Client cannot connect to {source.upper()} server.")
        if source == 'aws':
            print(f"Rotating to Google Cloud Server.")
            try:
                url = gfs_0p25_secondary_parameters_url_scanner(date,
                            run,
                            final_forecast_hour, 
                            proxies, 
                            'google')
            except Exception as e:
                print(f"Error: Client unable to establish a connection with either server. - System Exit.")
                print(f"Tip: Check to make sure there are no typos in your date or run.")
                print(f"Data begins at: {start.strftime('%Y%m%d')} 00z")
                sys.exit(1)
                
        else:
            print(f"Rotating to AWS Server.")
            try:
                url = gfs_0p25_secondary_parameters_url_scanner(date,
                            run,
                            final_forecast_hour, 
                            proxies, 
                            'aws')
            except Exception as e:
                print(f"Error: Client unable to establish a connection with either server. - System Exit.")
                print(f"Tip: Check to make sure there are no typos in your date or run.")
                print(f"Data begins at: {start.strftime('%Y%m%d')} 00z")
                sys.exit(1)

    
    return url

