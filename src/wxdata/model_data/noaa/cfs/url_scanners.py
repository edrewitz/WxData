"""
This file hosts the CFS URL Scanner Functions.

These functions return the URL and filename for the latest available data on the dataservers.

(C) Eric J. Drewitz 2025-2026
"""

import requests
import sys
import time
import warnings 
warnings.filterwarnings('ignore')
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

NOMADS = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod"
AWS = f"https://noaa-cfs-pds.s3.amazonaws.com"

def cfs_flux_url_scanner(final_forecast_hour,
                                    proxies,
                                    source):
    
    """
    This function is the URL Scanner for the NOAA Climate System Flux Products (CFS Flux) Data Archive.
    
    The function scans to ensure the data the user requests is available and provides error messages if data is not available.
    
    Required Arguments:
    
    1) final_forecast_hour (Integer) - The last forecast timestep the user wishes to download.
        The CFS outputs 6 hourly data for the span of several months. Note that if the user wishes to download
        6 hourly data for several months, processing times may be long. Must be a multiple of 6. 
        
    2) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    3) source (String) - The servers to pull the data from.

        ***Server Choices***
        
        'noaa' = NCEP/NOMADS
        'aws' = Amazon Web Services
                               
    Returns
    -------
    
    1) A list of full download URLs for GRIB2 files.
    2) A list of file names for GRIB2 files.
    3) A list of full download URLs for GRIB2 Index files.    
    """
    
    source = source.lower()
    
    if source == 'noaa':
        PREFIX = NOMADS
    else:
        PREFIX = AWS
    
        
    t_18z_init = f"{now.strftime('%Y%m%d')}18"
    t_12z_init = f"{now.strftime('%Y%m%d')}12"
    t_06z_init = f"{now.strftime('%Y%m%d')}06"
    t_00z_init = f"{now.strftime('%Y%m%d')}00"
    
    y_18z_init = f"{yd.strftime('%Y%m%d')}18"
    y_12z_init = f"{yd.strftime('%Y%m%d')}12"
    y_06z_init = f"{yd.strftime('%Y%m%d')}06"
    y_00z_init = f"{yd.strftime('%Y%m%d')}00"
    
    t_18z_init = datetime.strptime(t_18z_init, "%Y%m%d%H")
    t_12z_init = datetime.strptime(t_12z_init, "%Y%m%d%H")
    t_06z_init = datetime.strptime(t_06z_init, "%Y%m%d%H")
    t_00z_init = datetime.strptime(t_00z_init, "%Y%m%d%H")
    
    y_18z_init = datetime.strptime(y_18z_init, "%Y%m%d%H")
    y_12z_init = datetime.strptime(y_12z_init, "%Y%m%d%H")
    y_06z_init = datetime.strptime(y_06z_init, "%Y%m%d%H")
    y_00z_init = datetime.strptime(y_00z_init, "%Y%m%d%H")
    
    t_18z_end = t_18z_init + timedelta(hours=final_forecast_hour)
    t_12z_end = t_12z_init + timedelta(hours=final_forecast_hour)
    t_06z_end = t_06z_init + timedelta(hours=final_forecast_hour)
    t_00z_end = t_00z_init + timedelta(hours=final_forecast_hour)
    
    y_18z_end = y_18z_init + timedelta(hours=final_forecast_hour)
    y_12z_end = y_12z_init + timedelta(hours=final_forecast_hour)
    y_06z_end = y_06z_init + timedelta(hours=final_forecast_hour)
    y_00z_end = y_00z_init + timedelta(hours=final_forecast_hour)

    t_18z_url = f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/18/6hrly_grib_01/flxf{t_18z_end.strftime('%Y%m%d%H')}.01.{t_18z_init.strftime('%Y%m%d%H')}.grb2"
    t_12z_url = f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/12/6hrly_grib_01/flxf{t_12z_end.strftime('%Y%m%d%H')}.01.{t_12z_init.strftime('%Y%m%d%H')}.grb2"
    t_06z_url = f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/06/6hrly_grib_01/flxf{t_06z_end.strftime('%Y%m%d%H')}.01.{t_06z_init.strftime('%Y%m%d%H')}.grb2"
    t_00z_url = f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/00/6hrly_grib_01/flxf{t_00z_end.strftime('%Y%m%d%H')}.01.{t_00z_init.strftime('%Y%m%d%H')}.grb2"
    
    y_18z_url = f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/18/6hrly_grib_01/flxf{y_18z_end.strftime('%Y%m%d%H')}.01.{y_18z_init.strftime('%Y%m%d%H')}.grb2"
    y_12z_url = f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/12/6hrly_grib_01/flxf{y_12z_end.strftime('%Y%m%d%H')}.01.{y_12z_init.strftime('%Y%m%d%H')}.grb2"
    y_06z_url = f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/06/6hrly_grib_01/flxf{y_06z_end.strftime('%Y%m%d%H')}.01.{y_06z_init.strftime('%Y%m%d%H')}.grb2"
    y_00z_url = f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/00/6hrly_grib_01/flxf{y_00z_end.strftime('%Y%m%d%H')}.01.{y_00z_init.strftime('%Y%m%d%H')}.grb2"
    
    if proxies == None:
        try:
            t_18z = requests.get(f"{t_18z_url}", 
                                                stream=True)
            
            t_18z.close()
            
            t_12z = requests.get(f"{t_12z_url}", 
                                                stream=True)
            
            t_12z.close()
            
            t_06z = requests.get(f"{t_06z_url}", 
                                                stream=True)
            
            t_06z.close()
            
            t_00z = requests.get(f"{t_00z_url}", 
                                                stream=True)
            
            t_00z.close()
            
            y_18z = requests.get(f"{y_18z_url}", 
                                                stream=True)
            
            y_18z.close()
            
            y_12z = requests.get(f"{y_12z_url}", 
                                                stream=True)
            
            y_12z.close()
            
            y_06z = requests.get(f"{y_06z_url}", 
                                                stream=True)
            
            y_06z.close()
            
            y_00z = requests.get(f"{y_00z_url}", 
                                                stream=True)
            
            y_00z.close()
            
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(30)
                try:
                    t_18z = requests.get(f"{t_18z_url}", 
                                                        stream=True)
                    
                    t_18z.close()
                    
                    t_12z = requests.get(f"{t_12z_url}", 
                                                        stream=True)
                    
                    t_12z.close()
                    
                    t_06z = requests.get(f"{t_06z_url}", 
                                                        stream=True)
                    
                    t_06z.close()
                    
                    t_00z = requests.get(f"{t_00z_url}", 
                                                        stream=True)
                    
                    t_00z.close()
                    
                    y_18z = requests.get(f"{y_18z_url}", 
                                                        stream=True)
                    
                    y_18z.close()
                    
                    y_12z = requests.get(f"{y_12z_url}", 
                                                        stream=True)
                    
                    y_12z.close()
                    
                    y_06z = requests.get(f"{y_06z_url}", 
                                                        stream=True)
                    
                    y_06z.close()
                    
                    y_00z = requests.get(f"{y_00z_url}", 
                                                        stream=True)
                    
                    y_00z.close()
                    break
                except Exception as e:
                    i = i
                    if i >= 9:
                        print(f"Error: Client cannot establish a connection to {source.upper()} server.")
                        if source == 'noaa':
                            print(f"Rotating to AWS Server.")
                            try:
                                urls, files, idx_urls = cfs_flux_url_scanner(final_forecast_hour,
                                                                                        proxies,
                                                                                        'aws')
                            except Exception as e:
                                print("Error: Client cannot establish a connection to either server. - System Exit.")
                                sys.exit(1)
                        else:
                            print(f"Rotating to NCEP/NOMADS")
                            try:
                                urls, files, idx_urls = cfs_flux_url_scanner(final_forecast_hour,
                                                                                        proxies,
                                                                                        'noaa')   
                            except Exception as e:
                                print("Error: Client cannot establish a connection to either server. - System Exit.")
                                sys.exit(1)                         
                    

            
    else:
        try:
            t_18z = requests.get(f"{t_18z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            t_18z.close()
            
            t_12z = requests.get(f"{t_12z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            t_12z.close()
            
            t_06z = requests.get(f"{t_06z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            t_06z.close()
            
            t_00z = requests.get(f"{t_00z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            t_00z.close()
            
            y_18z = requests.get(f"{y_18z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            y_18z.close()
            
            y_12z = requests.get(f"{y_12z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            y_12z.close()
            
            y_06z = requests.get(f"{y_06z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            y_06z.close()
            
            y_00z = requests.get(f"{y_00z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            y_00z.close()
            
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(30)
                try:
                    t_18z = requests.get(f"{t_18z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    t_18z.close()
                    
                    t_12z = requests.get(f"{t_12z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    t_12z.close()
                    
                    t_06z = requests.get(f"{t_06z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    t_06z.close()
                    
                    t_00z = requests.get(f"{t_00z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    t_00z.close()
                    
                    y_18z = requests.get(f"{y_18z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    y_18z.close()
                    
                    y_12z = requests.get(f"{y_12z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    y_12z.close()
                    
                    y_06z = requests.get(f"{y_06z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    y_06z.close()
                    
                    y_00z = requests.get(f"{y_00z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    y_00z.close()
                    break
                except Exception as e:
                    i = i
                    if i >= 9:
                        print(f"Error: Client cannot establish a connection to {source.upper()} server.")
                        if source == 'noaa':
                            print(f"Rotating to AWS Server.")
                            try:
                                urls, files, idx_urls = cfs_flux_url_scanner(final_forecast_hour,
                                                                                        proxies,
                                                                                        'aws')
                            except Exception as e:
                                print("Error: Client cannot establish a connection to either server. - System Exit.")
                                sys.exit(1)
                        else:
                            print(f"Rotating to NCEP/NOMADS")
                            try:
                                urls, files, idx_urls = cfs_flux_url_scanner(final_forecast_hour,
                                                                                        proxies,
                                                                                        'noaa')   
                            except Exception as e:
                                print("Error: Client cannot establish a connection to either server. - System Exit.")
                                sys.exit(1)   
    
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
        f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/18/6hrly_grib_01",
        f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/12/6hrly_grib_01",
        f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/06/6hrly_grib_01",
        f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/00/6hrly_grib_01",
        f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/18/6hrly_grib_01",
        f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/12/6hrly_grib_01",
        f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/06/6hrly_grib_01",
        f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/00/6hrly_grib_01"
    ]
    
    init_times = [
        t_18z_init,
        t_12z_init,
        t_06z_init,
        t_00z_init,
        y_18z_init,
        y_12z_init,
        y_06z_init,
        y_00z_init
    ]
    
    for r, u, i in zip(responses, urls, init_times):
        if r.status_code == 200:
            url = u
            init = i
            break
        else:
            pass
        
        
    try:
        urls = []
        files = []
        idx_urls = []
        for h in range(0, (final_forecast_hour + 6), 6):
            time = init + timedelta(hours=h)
            full_url = f"{url}/flxf{time.strftime('%Y%m%d%H')}.01.{init.strftime('%Y%m%d%H')}.grb2"
            idx_url = f"{url}/flxf{time.strftime('%Y%m%d%H')}.01.{init.strftime('%Y%m%d%H')}.grb2.idx"
            file = f"flxf{time.strftime('%Y%m%d%H')}.01.{init.strftime('%Y%m%d%H')}.grb2"
            urls.append(full_url)
            files.append(file)
            idx_urls.append(idx_url)
    except Exception as e:
        print(f"Error: Client Unable To Connect to {source.upper()} Server.")
        if source == 'noaa':
            print(f"Rotating to AWS")
            urls, files, idx_urls = cfs_flux_url_scanner(final_forecast_hour,
                                                                proxies,
                                                                'aws') 
        else:
            print(f"Rotating to NCEP/NOMADS")
            urls, files, idx_urls = cfs_flux_url_scanner(final_forecast_hour,
                                                                proxies,
                                                                'aws')   
        
    return urls, files, idx_urls

def cfs_pressure_url_scanner(final_forecast_hour,
                                    proxies,
                                    source):
    
    """
    This function is the URL Scanner for the NOAA Climate System Flux Products (CFS Pressure) Data Archive.
    
    The function scans to ensure the data the user requests is available and provides error messages if data is not available.
    
    Required Arguments:
    
    1) final_forecast_hour (Integer) - The last forecast timestep the user wishes to download.
        The CFS outputs 6 hourly data for the span of several months. Note that if the user wishes to download
        6 hourly data for several months, processing times may be long. Must be a multiple of 6. 
        
    2) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    3) source (String) - The servers to pull the data from.

        ***Server Choices***
        
        'noaa' = NCEP/NOMADS
        'aws' = Amazon Web Services
                               
    Returns
    -------
    
    1) A list of full download URLs for GRIB2 files.
    2) A list of file names for GRIB2 files.
    3) A list of full download URLs for GRIB2 Index files.     
    """
    
    source = source.lower()
    
    if source == 'noaa':
        PREFIX = NOMADS
    else:
        PREFIX = AWS
    
        
    t_18z_init = f"{now.strftime('%Y%m%d')}18"
    t_12z_init = f"{now.strftime('%Y%m%d')}12"
    t_06z_init = f"{now.strftime('%Y%m%d')}06"
    t_00z_init = f"{now.strftime('%Y%m%d')}00"
    
    y_18z_init = f"{yd.strftime('%Y%m%d')}18"
    y_12z_init = f"{yd.strftime('%Y%m%d')}12"
    y_06z_init = f"{yd.strftime('%Y%m%d')}06"
    y_00z_init = f"{yd.strftime('%Y%m%d')}00"
    
    t_18z_init = datetime.strptime(t_18z_init, "%Y%m%d%H")
    t_12z_init = datetime.strptime(t_12z_init, "%Y%m%d%H")
    t_06z_init = datetime.strptime(t_06z_init, "%Y%m%d%H")
    t_00z_init = datetime.strptime(t_00z_init, "%Y%m%d%H")
    
    y_18z_init = datetime.strptime(y_18z_init, "%Y%m%d%H")
    y_12z_init = datetime.strptime(y_12z_init, "%Y%m%d%H")
    y_06z_init = datetime.strptime(y_06z_init, "%Y%m%d%H")
    y_00z_init = datetime.strptime(y_00z_init, "%Y%m%d%H")
    
    t_18z_end = t_18z_init + timedelta(hours=final_forecast_hour)
    t_12z_end = t_12z_init + timedelta(hours=final_forecast_hour)
    t_06z_end = t_06z_init + timedelta(hours=final_forecast_hour)
    t_00z_end = t_00z_init + timedelta(hours=final_forecast_hour)
    
    y_18z_end = y_18z_init + timedelta(hours=final_forecast_hour)
    y_12z_end = y_12z_init + timedelta(hours=final_forecast_hour)
    y_06z_end = y_06z_init + timedelta(hours=final_forecast_hour)
    y_00z_end = y_00z_init + timedelta(hours=final_forecast_hour)

    t_18z_url = f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/18/6hrly_grib_01/pgbf{t_18z_end.strftime('%Y%m%d%H')}.01.{t_18z_init.strftime('%Y%m%d%H')}.grb2"
    t_12z_url = f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/12/6hrly_grib_01/pgbf{t_12z_end.strftime('%Y%m%d%H')}.01.{t_12z_init.strftime('%Y%m%d%H')}.grb2"
    t_06z_url = f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/06/6hrly_grib_01/pgbf{t_06z_end.strftime('%Y%m%d%H')}.01.{t_06z_init.strftime('%Y%m%d%H')}.grb2"
    t_00z_url = f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/00/6hrly_grib_01/pgbf{t_00z_end.strftime('%Y%m%d%H')}.01.{t_00z_init.strftime('%Y%m%d%H')}.grb2"
    
    y_18z_url = f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/18/6hrly_grib_01/pgbf{y_18z_end.strftime('%Y%m%d%H')}.01.{y_18z_init.strftime('%Y%m%d%H')}.grb2"
    y_12z_url = f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/12/6hrly_grib_01/pgbf{y_12z_end.strftime('%Y%m%d%H')}.01.{y_12z_init.strftime('%Y%m%d%H')}.grb2"
    y_06z_url = f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/06/6hrly_grib_01/pgbf{y_06z_end.strftime('%Y%m%d%H')}.01.{y_06z_init.strftime('%Y%m%d%H')}.grb2"
    y_00z_url = f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/00/6hrly_grib_01/pgbf{y_00z_end.strftime('%Y%m%d%H')}.01.{y_00z_init.strftime('%Y%m%d%H')}.grb2"
    
    if proxies == None:
        try:
            t_18z = requests.get(f"{t_18z_url}", 
                                                stream=True)
            
            t_18z.close()
            
            t_12z = requests.get(f"{t_12z_url}", 
                                                stream=True)
            
            t_12z.close()
            
            t_06z = requests.get(f"{t_06z_url}", 
                                                stream=True)
            
            t_06z.close()
            
            t_00z = requests.get(f"{t_00z_url}", 
                                                stream=True)
            
            t_00z.close()
            
            y_18z = requests.get(f"{y_18z_url}", 
                                                stream=True)
            
            y_18z.close()
            
            y_12z = requests.get(f"{y_12z_url}", 
                                                stream=True)
            
            y_12z.close()
            
            y_06z = requests.get(f"{y_06z_url}", 
                                                stream=True)
            
            y_06z.close()
            
            y_00z = requests.get(f"{y_00z_url}", 
                                                stream=True)
            
            y_00z.close()
            
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(60)
                try:
                    t_18z = requests.get(f"{t_18z_url}", 
                                                        stream=True)
                    
                    t_18z.close()
                    
                    t_12z = requests.get(f"{t_12z_url}", 
                                                        stream=True)
                    
                    t_12z.close()
                    
                    t_06z = requests.get(f"{t_06z_url}", 
                                                        stream=True)
                    
                    t_06z.close()
                    
                    t_00z = requests.get(f"{t_00z_url}", 
                                                        stream=True)
                    
                    t_00z.close()
                    
                    y_18z = requests.get(f"{y_18z_url}", 
                                                        stream=True)
                    
                    y_18z.close()
                    
                    y_12z = requests.get(f"{y_12z_url}", 
                                                        stream=True)
                    
                    y_12z.close()
                    
                    y_06z = requests.get(f"{y_06z_url}", 
                                                        stream=True)
                    
                    y_06z.close()
                    
                    y_00z = requests.get(f"{y_00z_url}", 
                                                        stream=True)
                    
                    y_00z.close()
                    break
                except Exception as e:
                    i = i
                    if i >= 9:
                        print(f"Error: Client cannot establish a connection to {source.upper()} server.")
                        if source == 'noaa':
                            print(f"Rotating to AWS Server.")
                            try:
                                urls, files, idx_urls = cfs_pressure_url_scanner(final_forecast_hour,
                                                                                        proxies,
                                                                                        'aws')
                            except Exception as e:
                                print("Error: Client cannot establish a connection to either server. - System Exit.")
                                sys.exit(1)
                        else:
                            print(f"Rotating to NCEP/NOMADS")
                            try:
                                urls, files, idx_urls = cfs_pressure_url_scanner(final_forecast_hour,
                                                                                        proxies,
                                                                                        'noaa')   
                            except Exception as e:
                                print("Error: Client cannot establish a connection to either server. - System Exit.")
                                sys.exit(1)                         
                    

            
    else:
        try:
            t_18z = requests.get(f"{t_18z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            t_18z.close()
            
            t_12z = requests.get(f"{t_12z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            t_12z.close()
            
            t_06z = requests.get(f"{t_06z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            t_06z.close()
            
            t_00z = requests.get(f"{t_00z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            t_00z.close()
            
            y_18z = requests.get(f"{y_18z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            y_18z.close()
            
            y_12z = requests.get(f"{y_12z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            y_12z.close()
            
            y_06z = requests.get(f"{y_06z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            y_06z.close()
            
            y_00z = requests.get(f"{y_00z_url}", 
                                                stream=True,
                                                proxies=proxies)
            
            y_00z.close()
            
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(60)
                try:
                    t_18z = requests.get(f"{t_18z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    t_18z.close()
                    
                    t_12z = requests.get(f"{t_12z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    t_12z.close()
                    
                    t_06z = requests.get(f"{t_06z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    t_06z.close()
                    
                    t_00z = requests.get(f"{t_00z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    t_00z.close()
                    
                    y_18z = requests.get(f"{y_18z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    y_18z.close()
                    
                    y_12z = requests.get(f"{y_12z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    y_12z.close()
                    
                    y_06z = requests.get(f"{y_06z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    y_06z.close()
                    
                    y_00z = requests.get(f"{y_00z_url}", 
                                                        stream=True,
                                                        proxies=proxies)
                    
                    y_00z.close()
                    break
                except Exception as e:
                    i = i
                    if i >= 9:
                        print(f"Error: Client cannot establish a connection to {source.upper()} server.")
                        if source == 'noaa':
                            print(f"Rotating to AWS Server.")
                            try:
                                urls, files, idx_urls = cfs_pressure_url_scanner(final_forecast_hour,
                                                                                        proxies,
                                                                                        'aws')
                            except Exception as e:
                                print("Error: Client cannot establish a connection to either server. - System Exit.")
                                sys.exit(1)
                        else:
                            print(f"Rotating to NCEP/NOMADS")
                            try:
                                urls, files, idx_urls = cfs_pressure_url_scanner(final_forecast_hour,
                                                                                        proxies,
                                                                                        'noaa')   
                            except Exception as e:
                                print("Error: Client cannot establish a connection to either server. - System Exit.")
                                sys.exit(1)   
    
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
        f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/18/6hrly_grib_01",
        f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/12/6hrly_grib_01",
        f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/06/6hrly_grib_01",
        f"{PREFIX}/cfs.{now.strftime('%Y%m%d')}/00/6hrly_grib_01",
        f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/18/6hrly_grib_01",
        f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/12/6hrly_grib_01",
        f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/06/6hrly_grib_01",
        f"{PREFIX}/cfs.{yd.strftime('%Y%m%d')}/00/6hrly_grib_01"
    ]
    
    init_times = [
        t_18z_init,
        t_12z_init,
        t_06z_init,
        t_00z_init,
        y_18z_init,
        y_12z_init,
        y_06z_init,
        y_00z_init
    ]
    
    for r, u, i in zip(responses, urls, init_times):
        if r.status_code == 200:
            url = u
            init = i
            break
        else:
            pass
        
    

    try:
        urls = []
        files = []
        idx_urls = []
        for h in range(0, (final_forecast_hour + 6), 6):
            time = init + timedelta(hours=h)
            full_url = f"{url}/pgbf{time.strftime('%Y%m%d%H')}.01.{init.strftime('%Y%m%d%H')}.grb2"
            idx_url = f"{url}/pgbf{time.strftime('%Y%m%d%H')}.01.{init.strftime('%Y%m%d%H')}.grb2.idx"
            file = f"pgbf{time.strftime('%Y%m%d%H')}.01.{init.strftime('%Y%m%d%H')}.grb2"
            urls.append(full_url)
            files.append(file)
            idx_urls.append(idx_url)
    except Exception as e:
        print(f"Error: Client Unable To Connect to {source.upper()} Server.")
        if source == 'noaa':
            print(f"Rotating to AWS")
            urls, files, idx_urls = cfs_pressure_url_scanner(final_forecast_hour,
                                                                proxies,
                                                                'aws') 
        else:
            print(f"Rotating to NCEP/NOMADS")
            urls, files, idx_urls = cfs_pressure_url_scanner(final_forecast_hour,
                                                                proxies,
                                                                'aws')   
        
    return urls, files, idx_urls