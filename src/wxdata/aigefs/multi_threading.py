"""
This file hosts the multi-threading functionality for downloading ensemble members.

(C) Eric J. Drewitz 2025-2026
"""
import os

from concurrent.futures import ThreadPoolExecutor
from wxdata.client.client import byte_range_request
from time import sleep

MAX_WORKERS = 2

def download_ensemble_members_presure(url,
                      variables,
                      levels,
                      path,
                      run,
                      final_forecast_hour,
                      proxies=None,
                      chunk_size=1024,
                      notifications='off',
                      clear_recycle_bin=False):
    
    """
    This function wraps byte_range_requests() to be used in a multi-threading process
    
    Required Arguments:
    
    1) url (String) - The URL of the GRIB file that will be downloaded.
        
    2) variables (String List) - The list of variables to be downloaded.
    
    3) levels (Float or Integer List) - The list of pressure or height levels. 
    
    4) level_type (String) - The type of level.
    
        Level Types
        -----------
        
        'hybrid'
        'entire atmosphere'
        'surface':'surface',
        'boundary layer'
        'pressure'
        'mean sea level'
        'height above ground'
        'height below ground'
        'height above sea level'
        'entire atmosphere single layer'
        'low cloud layer'
        'middle cloud layer'
        'high cloud layer'
        'cloud ceiling'
        'tropopause'
        'max wind'
        'isothermal'
        'highest tropospheric freezing level'
        'sigma layer'
        'sigma level'
        'potential vorticity surface'
        'reserved'
    
    5) path (String) - The directory where the file is saved to. 
    
    6) filename (String) - The name the user wishes to save the file as. 
    
    7) run (Integer) - The model run time extracted from the URL scanner.
    
    8) final_forecast_hour (Integer) - The last forecast hour the user wants to download.
    
    Optional Arguments:
    
    1) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    2) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    3) notifications (String) - Default='on'. Notification when a file is downloaded and saved to {path}
    
    4) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin 
    will be deleted with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    Returns
    -------
    
    Downloads a partial GRIB file consisting of the variable the user specifies.    
    
    """
    
    if run < 10:
        run = f"0{run}"
    else:
        run = f"{run}"   
             
    stop = final_forecast_hour + 6
    for i in range(0, stop, 6):
        if i < 10:
            byte_range_request(f"{url}/aigefs.t{run}z.pres.f00{i}.grib2",
                                        f"{url}/aigefs.t{run}z.pres.f00{i}.grib2.idx",
                                        variables,
                                        levels,
                                        'pressure',
                                        path,
                                        f"aigefs.t{run}z.pres.f00{i}.grib2",
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin)
        elif i >= 10 and i < 100:
            byte_range_request(f"{url}/aigefs.t{run}z.pres.f0{i}.grib2",
                                        f"{url}/aigefs.t{run}z.pres.f0{i}.grib2.idx",
                                        variables,
                                        levels,
                                        'pressure',
                                        path,
                                        f"aigefs.t{run}z.pres.f0{i}.grib2",
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin)
        else:
            byte_range_request(f"{url}/aigefs.t{run}z.pres.f{i}.grib2",
                                        f"{url}/aigefs.t{run}z.pres.f{i}.grib2.idx",
                                        variables,
                                        levels,
                                        'pressure',
                                        path,
                                        f"aigefs.t{run}z.pres.f{i}.grib2",
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin)   



def download_ensemble_members(urls,
                      variables,
                      levels,
                      paths,
                      run,
                      final_forecast_hour,
                      proxies=None,
                      chunk_size=1024):
    
    """
    This function uses multi-threading for downloading ensemble members to improve performance.
    
    Required Arguments:
    
    1) url (String) - The URL of the GRIB file that will be downloaded.
        
    2) variables (String List) - The list of variables to be downloaded.
    
    3) levels (Float or Integer List) - The list of pressure or height levels. 
    
    4) level_type (String) - The type of level.
    
        Level Types
        -----------
        
        'hybrid'
        'entire atmosphere'
        'surface':'surface',
        'boundary layer'
        'pressure'
        'mean sea level'
        'height above ground'
        'height below ground'
        'height above sea level'
        'entire atmosphere single layer'
        'low cloud layer'
        'middle cloud layer'
        'high cloud layer'
        'cloud ceiling'
        'tropopause'
        'max wind'
        'isothermal'
        'highest tropospheric freezing level'
        'sigma layer'
        'sigma level'
        'potential vorticity surface'
        'reserved'
    
    5) path (String) - The directory where the file is saved to. 
    
    6) filename (String) - The name the user wishes to save the file as. 
    
    7) run (Integer) - The model run time extracted from the URL scanner.
    
    8) final_forecast_hour (Integer) - The last forecast hour the user wants to download.
    
    Optional Arguments:
    
    1) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    2) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    3) notifications (String) - Default='on'. Notification when a file is downloaded and saved to {path}
    
    4) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin 
    will be deleted with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    Returns
    -------
    
    Downloads a partial GRIB file consisting of the variable the user specifies.  
    """
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for path, url in zip(paths, urls):
            # Submit the job immediately
            executor.submit(download_ensemble_members_presure, 
                                           url,
                                            variables,
                                            levels,
                                            path,
                                            run,
                                            final_forecast_hour,
                                            proxies=proxies,
                                            chunk_size=chunk_size)            
            # Pause the main loop for 1 second before submitting the next job
            sleep(1) 
            