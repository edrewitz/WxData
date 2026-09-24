"""
This file hosts the functions for the GEPS Data Client

(C) Eric J. Drewitz 2025-2026
"""
import os as _os
import wxdata.client.client as _client
import warnings as _warnings
_warnings.filterwarnings('ignore')
import wxdata.post_processors.cmc_post_processing as _cmc_post_processing

from wxdata.utils.transforms import grib_to_netcdf as _grib_to_netcdf
from wxdata.model_data.cmc.utils.file_scanner import scan_local_machine as _scan_local_machine
from wxdata.model_data.cmc.geps.url_scanner import geps_url_scanner as _geps_url_scanner
from wxdata.calc.unit_conversion import convert_temperature_units as _convert_temperature_units
from wxdata.utils.recycle_bin import(
    clear_recycle_bin_windows as _clear_recycle_bin_windows,
    clear_trash_bin_mac as _clear_trash_bin_mac,
    clear_trash_bin_linux as _clear_trash_bin_linux
)


def _geps_client(final_forecast_hour=384, 
             step=1,
             path=f"GEPS",
             proxies=None, 
             chunk_size=8192,
             notifications='off',
             level_type='pressure',
             clear_data=False,
             variable='geopotential height',
             level=500):
    
    """
    This function is our client that scans and downloads the latest data from https://dd.weather.gc.ca/.
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEPS
        goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
        384 by the nereast increment of 1 hour. 
        
    2) step (Integer) - Default=1. Increment in forecast hours (Default=1hrly).
    
    3) path (String) - Default='GEPS'. The parent directory for the GRIB2 files on the local machine.
    
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    5) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    6) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    7) level_type (String) - Default='pressure'. The type of level for the variable.
    
        ***Level Types***
        
        'pressure'
        'height above ground'
        'depth below surface'
        'surface'
        'mean sea level'
        'nominal top'
        'entire atmosphere'
        
    8) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
        
    9) variable (String) - Default='geopotential height'. The variable the user wishes to download.
    
    10) level (Integer) - Default=500. For parameters that have multiple levels, here is where you select the level to 
        download. Default is 500mb. Units for height above ground are (m) and depth below surface (cm). 
    
    
    ***Variables & Proper level_type & level***
    
    Any area where valid_levels = None -> Users do not need to edit the optional argument `level`
        
    'temperature': 
        valid level type(s) = 'pressure', 'height above ground'.
        valid levels:
            level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                   
            level_type='height above ground' (m): 2, 40, 80, 120
        
    'cape':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)
        
    'cin':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)  
            
    'downward longwave radiation flux':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'downward shortwave radiation flux':
        valid level type(s): 'surface', 'nominal top'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
                                                OR 
                           (level_type='nominal top' -> 'nominal top' is the only level)              
                           
    'geopotential height':
        valid level type(s) = 'pressure'.
        valid levels:
            level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10. 
                                                  
    'ice pellets accumulation':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)   
        
    'total convective precipitation':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)   

    'freezing rain accumulation':  
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)  
        
    'rain accumulation':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)  
    
    'snow accumulation':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)  
        
    'latent heat net flux':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)  
        
    'outgoing longwave radiation':
        valid level type(s): 'nominal top'
        valid levels: None (level_type='nominal top' -> 'nominal top' is the only level) 
        
    'sea ice thickness':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'pressure':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'mean sea level pressure':
        valid level type(s): 'mean sea level'
        valid levels: None (level_type='mean sea level' -> 'mean sea level' is the only level) 
        
    'precipitable water':
        valid level type(s): 'entire atmosphere'
        valid levels: None (level_type='entire atmosphere' -> 'entire atmosphere' is the only level) 
        
    'relative humidity':
        valid level type(s) = 'pressure', 'height above ground'.
        valid levels:
            level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                   
            level_type='height above ground' (m): 2
            
    'surface runoff':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'sensible heat net flux':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'snow depth':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'specific humidity':
        valid level type(s) = 'height above ground'.
        valid levels:
            level_type='height above ground' (m): 2, 40, 80, 120.
    
    'soil moisture':
        valid level type(s) = 'depth below surface'.
        valid levels:
            level_type='height above ground' (cm): 10.
            
    'total cloud cover':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'maximum temperature':
        valid level type(s) = 'height above ground'.
        valid levels:
            level_type='height above ground' (m): 2.
            
    'minimum temperature':
        valid level type(s) = 'height above ground'.
        valid levels:
            level_type='height above ground' (m): 2.
            
    'soil temperature':
        valid level type(s) = 'depth below surface'.
        valid levels:
            level_type='height above ground' (cm): 10.
            
    'u-wind component':
        valid level type(s) = 'pressure', 'height above ground'.
        valid levels:
            level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                   
            level_type='height above ground' (m): 10.
            
    'v-wind component':
        valid level type(s) = 'pressure', 'height above ground'.
        valid levels:
            level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                   
            level_type='height above ground' (m): 10.
            
    'upward longwave radiation flux':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'upward shortwave radiation flux':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'vertical velocity':
        valid level type(s) = 'pressure'.
        valid levels:
            level_type='pressure' (hPa): 850.
            
    'wind speed':
        valid level type(s) = 'height above ground'.
        valid levels:
            level_type='height above ground' (m): 2, 40, 80, 120.                       
            
    Returns
    -------
    
    1) Scans and downloads the latest GEPS data for `parameter` of `level_type` at `level` or `layer`
    
    2) When clear_data=False (Default) -> The GEPS URL & file scanners are active and will prevent downloading data
        from the server until newer data arrives. This helps prevent you from getting temporarily blocked from requesting
        data as a result of server rate limits. 
        
    3) Builds and/or clears out the directory and downloads the new files into the directory at {path}
    
    4) The full directory path defined by the user where the GEPS files are stored. 
    
    """
        
    if level_type == 'pressure' or level_type == 'height above ground' or level_type == 'depth below surface':
        
        full_path = f"{path}/{variable.upper()}/{level}"
        
        if level_type == 'pressure':
            suffix = 'mb'
        elif level_type == 'height above ground':
            suffix = 'm'
        else:
            suffix = ' cm'
        
        print(f"Scanning https://dd.weather.gc.ca/ GEPS {variable.upper()} {level}{suffix}")
        print("Please Wait...")
        urls, files = _geps_url_scanner(final_forecast_hour,
                            proxies,
                            level_type,
                            variable,
                            step,
                            level=level)

        print(f"Server Scan Complete!")
        download = _scan_local_machine(urls,
                                    f"{path}/{variable.upper()}/{level}")

        if download == True or clear_data == True:
            print("Downloading Data")

            try:
                for file in _os.listdir(f"{path}/{variable.upper()}/{level}"):
                    _os.remove(f"{path}/{variable.upper()}/{level}/{file}")
            except Exception as e:
                pass
            
            for url, file in zip(urls, files):
                _client.get_gridded_data(url,
                                        f"{path}/{variable.upper()}/{level}",
                                        file,
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications)
            print(f"GEPS {variable.upper()} {level}{suffix} Download Complete!\n")   
        else:
            print(f"GEPS {variable.upper()} {level}{suffix} data on local machine is up to date with latest data on the server.\nSkipping Download.\n")
            
    else:
        
        full_path = f"{path}/{variable.upper()}/{level_type.upper()}"
        
        print(f"Scanning https://dd.weather.gc.ca/ GEPS {variable.upper()} {level_type}")
        print("Please Wait...")
        urls, files = _geps_url_scanner(final_forecast_hour,
                            proxies,
                            level_type,
                            variable,
                            step)

        print(f"Server Scan Complete!")
        
        download = _scan_local_machine(urls,
                                    f"{path}/{variable.upper()}/{level_type.upper()}")

        if download == True or clear_data == True:
            print("Downloading Data")

            try:
                for file in _os.listdir(f"{path}/{variable.upper()}/{level_type.upper()}"):
                    _os.remove(f"{path}/{variable.upper()}/{level_type.upper()}/{file}")
            except Exception as e:
                pass
            
            for url, file in zip(urls, files):
                _client.get_gridded_data(url,
                                        f"{path}/{variable.upper()}/{level_type.upper()}",
                                        file,
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications)
            print(f"GEPS {variable.upper()} {level_type} Download Complete!\n")   
        else:
            print(f"GEPS {variable.upper()} {level_type} data on local machine is up to date with latest data on the server.\nSkipping Download.\n")
            
    
    return full_path
                    

        

def geps(final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             step=1,
             path=f"GEPS",
             proxies=None, 
             clear_recycle_bin=False,
             process_data=True,
             convert_temperature=True,
             convert_to='celsius',
             chunk_size=8192,
             notifications='off',
             level_type='pressure',
             clear_data=False,
             variable='geopotential height',
             level=500,
             cat='members',
            to_netcdf=False,
            netcdf_path=f"GEPS/NETCDF",
            netcdf_filename=f"geopotential_height.nc",
            delete_previous_netcdf_file=True,
            return_values=True):
    
    """
    This function retrieves the latest GEPS data from https://dd.weather.gc.ca/ and returns an xarray.array of specified data.
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEPS
        goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
        384 by the nereast increment of 1 hour. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=1. Increment in forecast hours (Default=1hrly).
    
    7) path (String) - Default='GEPS'. The parent directory for the GRIB2 files on the local machine.
    
    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    9) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine.
        
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed and no values
       returned to the user.
       
    11) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    12) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    13) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    14) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    15) level_type (String) - Default='pressure'. The type of level for the variable.
    
        ***Level Types***
        
        'pressure'
        'height above ground'
        'depth below surface'
        'surface'
        'mean sea level'
        'nominal top'
        'entire atmosphere'
        
    16) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
        
    17) variable (String) - Default='geopotential height'. The variable the user wishes to download.
    
    18) level (Integer) - Default=500. For parameters that have multiple levels, here is where you select the level to 
        download. Default is 500mb. Units for height above ground are (m) and depth below surface (cm). 
        
    19) cat (String) - Default='members'. Set cat='members' for all ensemble members OR set cat='control' for control run.
        
    20) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.
    
    21) netcdf_path (String) - Default='GEPS/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.
    
    22) netcdf_filename (String) - Default='geopotential_height.nc'. The name of the netCDF (.nc) file. A good practice is to 
        name this netCDF file using the variable name. 
        
    23) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
        new netCDF file. For users who want to archive all data set this to False. 
        
    24) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned. 
    
    ***Variables & Proper level_type & level***
    
    Any area where valid_levels = None -> Users do not need to edit the optional argument `level`
        
    'temperature': 
        valid level type(s) = 'pressure', 'height above ground'.
        valid levels:
            level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                   
            level_type='height above ground' (m): 2, 40, 80, 120
        
    'cape':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)
        
    'cin':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)  
            
    'downward longwave radiation flux':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'downward shortwave radiation flux':
        valid level type(s): 'surface', 'nominal top'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
                                                OR 
                           (level_type='nominal top' -> 'nominal top' is the only level)              
                           
    'geopotential height':
        valid level type(s) = 'pressure'.
        valid levels:
            level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10. 
                                                  
    'ice pellets accumulation':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)   
        
    'total convective precipitation':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)   

    'freezing rain accumulation':  
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)  
        
    'rain accumulation':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)  
    
    'snow accumulation':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)  
        
    'latent heat net flux':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level)  
        
    'outgoing longwave radiation':
        valid level type(s): 'nominal top'
        valid levels: None (level_type='nominal top' -> 'nominal top' is the only level) 
        
    'sea ice thickness':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'pressure':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'mean sea level pressure':
        valid level type(s): 'mean sea level'
        valid levels: None (level_type='mean sea level' -> 'mean sea level' is the only level) 
        
    'precipitable water':
        valid level type(s): 'entire atmosphere'
        valid levels: None (level_type='entire atmosphere' -> 'entire atmosphere' is the only level) 
        
    'relative humidity':
        valid level type(s) = 'pressure', 'height above ground'.
        valid levels:
            level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                   
            level_type='height above ground' (m): 2
            
    'surface runoff':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'sensible heat net flux':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'snow depth':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'specific humidity':
        valid level type(s) = 'height above ground'.
        valid levels:
            level_type='height above ground' (m): 2, 40, 80, 120.
    
    'soil moisture':
        valid level type(s) = 'depth below surface'.
        valid levels:
            level_type='height above ground' (cm): 10.
            
    'total cloud cover':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'maximum temperature':
        valid level type(s) = 'height above ground'.
        valid levels:
            level_type='height above ground' (m): 2.
            
    'minimum temperature':
        valid level type(s) = 'height above ground'.
        valid levels:
            level_type='height above ground' (m): 2.
            
    'soil temperature':
        valid level type(s) = 'depth below surface'.
        valid levels:
            level_type='height above ground' (cm): 10.
            
    'u-wind component':
        valid level type(s) = 'pressure', 'height above ground'.
        valid levels:
            level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                   
            level_type='height above ground' (m): 10.
            
    'v-wind component':
        valid level type(s) = 'pressure', 'height above ground'.
        valid levels:
            level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                   
            level_type='height above ground' (m): 10.
            
    'upward longwave radiation flux':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'upward shortwave radiation flux':
        valid level type(s): 'surface'
        valid levels: None (level_type='surface' -> 'surface' is the only level) 
        
    'vertical velocity':
        valid level type(s) = 'pressure'.
        valid levels:
            level_type='pressure' (hPa): 850.
            
    'wind speed':
        valid level type(s) = 'height above ground'.
        valid levels:
            level_type='height above ground' (m): 2, 40, 80, 120.   
            
    Returns
    -------
    
    An xarray.array of the latest GEPS forecast data for a user-specified variable, level/layer and level_type.
    
    GEPS files are saved to directory {path}  
    """
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass

    if level_type == 'pressure' or level_type == 'height above ground' or level_type == 'depth below surface':

        dir = _geps_client(final_forecast_hour=final_forecast_hour, 
                    step=step,
                    path=path,
                    proxies=proxies, 
                    chunk_size=chunk_size,
                    notifications=notifications,
                    level_type=level_type,
                    clear_data=clear_data,
                    variable=variable,
                    level=level)
        
        
    else:
        dir = _geps_client(final_forecast_hour=final_forecast_hour, 
                    step=step,
                    path=path,
                    proxies=proxies, 
                    chunk_size=chunk_size,
                    notifications=notifications,
                    level_type=level_type,
                    clear_data=clear_data,
                    variable=variable)
                       
    if process_data == True:
        
        print("Data Processing...")
        
        ds = _cmc_post_processing.geps_post_processing(dir,
                                                        western_bound,
                                                        eastern_bound,
                                                        northern_bound,
                                                        southern_bound,
                                                        variable,
                                                        cat)
        
        if convert_temperature == True:
            ds = _convert_temperature_units(ds, 
                                        convert_to)
                        
        else:
            pass
        
        if level_type == 'pressure' or level_type == 'height above ground' or level_type == 'depth below surface':
            
            if level_type == 'pressure':
                suffix = 'mb'
            elif level_type == 'height above ground':
                suffix = 'm'
            else:
                suffix = 'cm'
            
            print(f"GEPS Data Processing Complete: {variable.upper()} - {level}{suffix}")
        else:
            print(f"GEPS Data Processing Complete: {variable.upper()} - surface")
        if to_netcdf == True:
            
            if delete_previous_netcdf_file == True:
                try:
                    _os.remove(f"{netcdf_path}/{netcdf_filename}")
                except Exception as e:
                    pass
            
            _grib_to_netcdf(ds,
                            netcdf_path,
                            netcdf_filename)
        else:
            pass
        
        if return_values == True:    
            return ds
        else:
            pass
    else:
        pass
                
    