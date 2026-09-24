"""
This file hosts the URL Scanner for the Archived NOAA Climate Forecast System (CFS) Data Archive.

Data Source: NOAA (Hosted via Amazon Web Services)

(C) Eric J. Drewitz 2025-2026
"""

import requests
import sys

from datetime import datetime, timedelta

PREFIX = f"https://noaa-cfs-pds.s3.amazonaws.com"

# The earliest CFS data hosted in the NOAA Archive on AWS is 10/31/2018 00z
start = datetime.strptime("2018103100", "%Y%m%d%H")

def cfs_flux_url_scanner(date,
             run,
             final_forecast_hour,
             proxies):
    
    """
    This function is the URL Scanner for the NOAA Climate System Flux Products (CFS Flux) Data Archive.
    
    The function scans to ensure the data the user requests is available and provides error messages if data is not available.
    
    Required Arguments:
    
    1) date (String or datetime) - The date of the model run. Format: "YYYY-mm-dd".
    
    2) run (Integer) - The model runtime in UTC (0, 6, 12, 18).
    
    3) final_forecast_hour (Integer) - The last forecast timestep the user wishes to download.
        The CFS outputs 6 hourly data for the span of several months. Note that if the user wishes to download
        6 hourly data for several months, processing times may be long. Must be a multiple of 6. 
        
    4) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    Returns
    -------
    
    1) A list of full download URLs for GRIB2 files.
    2) A list of file names for GRIB2 files.
    3) A list of full download URLs for GRIB2 Index files.    
    """
    
    if type(date) != type(start):
        date = f"{date[0:4]}{date[5:7]}{date[8:10]}"
        date = datetime.strptime(date, "%Y%m%d")
    else:
        date = date
        
    if type(run) == type(1):
        if run == 0:
            run = '00'
        elif run == 6:
            run = '06'
        elif run == 12:
            run = '12'
        else:
            run = '18'
        
    init = f"{date.strftime('%Y%m%d')}{run}"
    init = datetime.strptime(init, "%Y%m%d%H")
    end = init + timedelta(hours=final_forecast_hour)

    url = f"https://noaa-cfs-pds.s3.amazonaws.com/cfs.{date.strftime('%Y%m%d')}/{run}/6hrly_grib_01/flxf{end.strftime('%Y%m%d%H')}.01.{init.strftime('%Y%m%d%H')}.grb2"
    
    if proxies == None:
        try:
            response = requests.get(f"{url}", 
                                    stream=True)
        except Exception as e:
            print(f"Error: Data not available for {date.strftime('%Y%m%d')} {run}z")
            print("Please double check the date is correct.")
            print(f"Catalog begins at: {start.strftime('%Y%m%d:%H00')}z")
            sys.exit(1)
            
    else:
        try:
            response = requests.get(f"{url}", 
                                    stream=True,
                                    proxies=proxies)
        except Exception as e:
            print(f"Error: Data not available for {date.strftime('%Y%m%d')} {run}z")
            print("Please double check the date is correct.")
            print(f"Catalog begins at: {start.strftime('%Y%m%d:%H00')}z")
            sys.exit(1)  
            
    
    urls = []
    files = []
    idx_urls = []
    for h in range(0, (final_forecast_hour + 6), 6):
        time = init + timedelta(hours=h)
        url = f"https://noaa-cfs-pds.s3.amazonaws.com/cfs.{date.strftime('%Y%m%d')}/{run}/6hrly_grib_01/flxf{time.strftime('%Y%m%d%H')}.01.{init.strftime('%Y%m%d%H')}.grb2"
        idx_url = f"https://noaa-cfs-pds.s3.amazonaws.com/cfs.{date.strftime('%Y%m%d')}/{run}/6hrly_grib_01/flxf{time.strftime('%Y%m%d%H')}.01.{init.strftime('%Y%m%d%H')}.grb2.idx"
        file = f"flxf{time.strftime('%Y%m%d%H')}.01.{init.strftime('%Y%m%d%H')}.grb2"
        urls.append(url)
        files.append(file)
        idx_urls.append(idx_url)
        
    return urls, files, idx_urls
    
    