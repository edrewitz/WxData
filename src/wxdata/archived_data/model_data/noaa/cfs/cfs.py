"""
This file hosts the client that retrieves the requested NOAA Climate Forecast System (CFS) Data from the Amazon Web Services Archive.

(C) Eric J. Drewitz 2025-2026
"""
import os as _os
import wxdata.client.client as _client
import wxdata.post_processors.cfs_post_processing as _cfs_post_processing
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.calc.unit_conversion import convert_temperature_units as _convert_temperature_units
from wxdata.utils.warnings import eccodes_warning as _eccodes_warning
from wxdata.archived_data.model_data.noaa.cfs.url_scanner import(
    cfs_flux_url_scanner as _cfs_flux_url_scanner
)

_eccodes_warning()

def get_archived_cfs_flux(
             date,
             run,
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90,
             final_forecast_hour=720,
             proxies=None,
             path=f"CFS Flux/Archive",
             process_data=True,
             clear_recycle_bin=False,
             notifications='off',
             convert_temperature=True,
             chunk_size=8192,
             convert_to='celsius',
             level_type='height above ground',
             variables=['temperature',
                        'maximum temperature',
                        'minimum temperature'],
             levels=[2]
             ):
    
    """
    This function is the URL Scanner for the NOAA Climate System Flux Products (CFS Flux) Data Archive.
    
    The function scans to ensure the data the user requests is available and provides error messages if data is not available.
    
    Required Arguments:
    
    1) date (String or datetime) - The date of the model run.
    
    2) run (Integer) - The model runtime in UTC (0, 6, 12, 18).
    
    3) final_forecast_hour (Integer) - The last forecast timestep the user wishes to download.
        The CFS outputs 6 hourly data for the span of several months. Note that if the user wishes to download
        6 hourly data for several months, processing times may be long. Must be a multiple of 6. 
        
    4) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    """
    
    urls, files, idx_urls = _cfs_flux_url_scanner(date,
                                 run,
                                 final_forecast_hour,
                                 proxies)
    if run > 10:
        path = f"{path}/{date}/{run}z"
    else:
            path = f"{path}/{date}/0{run}z"
            
    try:
        for file in _os.listdir(path):
            _os.remove(f"{path}/{file}")
    except Exception as e:
        pass
    
    for u, f, i in zip(urls, files, idx_urls):
        _client.byte_range_request(u,
                      i,
                      variables,
                      levels,
                      level_type,
                      path,
                      f,
                      proxies=proxies,
                      chunk_size=chunk_size,
                      notifications=notifications,
                      clear_recycle_bin=clear_recycle_bin)
        
    if process_data == True:
        print(f"CFS Flux Data Processing...")
        
        ds = _cfs_post_processing.archived_cfs_post_processing(path,
                                                                western_bound,
                                                                eastern_bound,
                                                                northern_bound,
                                                                southern_bound,
                                                                variables)
        
        if convert_temperature == True:
                ds = _convert_temperature_units(ds, 
                                            convert_to)
                
        else:
            pass
        
        print(f"CFS Flux Data Processing Complete.")
        return ds
    
    else:
        pass 
        
        
