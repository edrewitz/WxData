"""
This file hosts the functions for the GDPS Data Client

(C) Eric J. Drewitz 2025-2026
"""
import os as _os
import wxdata.client.client as _client
import warnings as _warnings
_warnings.filterwarnings('ignore')
import wxdata.post_processors.cmc_post_processing as _cmc_post_processing

from wxdata.cmc.gdps.file_scanner import scan_local_machine as _scan_local_machine
from wxdata.cmc.gdps.url_scanner import gdps_url_scanner as _gdps_url_scanner
from wxdata.cmc.utils.cmc_keys import gdps_rdps_variable_keys as _gdps_rdps_variable_keys
from wxdata.calc.unit_conversion import convert_temperature_units as _convert_temperature_units
from wxdata.utils.recycle_bin import(
    clear_recycle_bin_windows as _clear_recycle_bin_windows,
    clear_trash_bin_mac as _clear_trash_bin_mac,
    clear_trash_bin_linux as _clear_trash_bin_linux
)


def _gdps_client(final_forecast_hour=240, 
             step=1,
             path=f"GDPS",
             proxies=None, 
             chunk_size=8192,
             notifications='off',
             level_type='pressure',
             clear_data=False,
            variable='geopotential height',
            level=500,
            layer=[1000, 500]):
    
    """
    
    """
    
    variable_key = _gdps_rdps_variable_keys(variable)
    
    if level_type == 'pressure' or level_type == 'height above ground' or level_type == 'potential vorticity surface':
        
        full_path = f"{path}/{variable.upper()}/{level}"
        
        if level_type == 'pressure':
            suffix = 'mb'
        elif level_type == 'height above ground':
            suffix = 'm'
        else:
            suffix = ' PVU'
        
        print(f"Scanning https://dd.weather.gc.ca/ GDPS {variable.upper()} {level}{suffix}")
        print("Please Wait...")
        urls, files = _gdps_url_scanner(final_forecast_hour,
                            proxies,
                            level_type,
                            variable_key,
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
            print(f"GDPS {variable.upper()} {level}{suffix} Download Complete!\n")   
        else:
            print(f"GDPS {variable.upper()} {level}{suffix} data on local machine is up to date with latest data on the server.\nSkipping Download.\n")
            
    elif level_type == 'pressure layer' or level_type == 'depth below surface':
        
        if level_type == 'pressure layer':
            ext = f"{layer[0]}to{layer[1]}mb"
        else:
            ext = f"{layer[0]}to{layer[1]}cm"
            
        full_path = f"{path}/{variable.upper()}/{ext}"
        
        print(f"Scanning https://dd.weather.gc.ca/ GDPS {variable.upper()} {ext}")
        print("Please Wait...")
        urls, files = _gdps_url_scanner(final_forecast_hour,
                            proxies,
                            level_type,
                            variable_key,
                            step,
                            levels=layer)

        print(f"Server Scan Complete!")
        
        download = _scan_local_machine(urls,
                                    f"{path}/{variable.upper()}/{ext}")

        if download == True or clear_data == True:
            print("Downloading Data")

            try:
                for file in _os.listdir(f"{path}/{variable.upper()}/{ext}"):
                    _os.remove(f"{path}/{variable.upper()}/{ext}/{file}")
            except Exception as e:
                pass
            
            for url, file in zip(urls, files):
                _client.get_gridded_data(url,
                                        f"{path}/{variable.upper()}/{ext}",
                                        file,
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications)
            print(f"GDPS {variable.upper()} {ext} Download Complete!\n")   
        else:
            print(f"GDPS {variable.upper()} {ext} data on local machine is up to date with latest data on the server.\nSkipping Download.\n")
            
    else:
        
        full_path = f"{path}/{variable.upper()}/{level_type.upper()}"
        
        print(f"Scanning https://dd.weather.gc.ca/ GDPS {variable.upper()} {level_type}")
        print("Please Wait...")
        urls, files = _gdps_url_scanner(final_forecast_hour,
                            proxies,
                            level_type,
                            variable_key,
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
            print(f"GDPS {variable.upper()} {level_type} Download Complete!\n")   
        else:
            print(f"GDPS {variable.upper()} {level_type} data on local machine is up to date with latest data on the server.\nSkipping Download.\n")
            
    
    return full_path
                    

        

def gdps(final_forecast_hour=240, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             step=1,
             path=f"GDPS",
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
            layer=[1000, 500]):
    
    """
    
    """
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass

    if level_type == 'pressure' or level_type == 'height above ground' or level_type == 'potential vorticity surface':

        dir = _gdps_client(final_forecast_hour=final_forecast_hour, 
                    step=step,
                    path=path,
                    proxies=proxies, 
                    chunk_size=chunk_size,
                    notifications=notifications,
                    level_type=level_type,
                    clear_data=clear_data,
                    variable=variable,
                    level=level)
            
            
    elif level_type == 'pressure layer' or level_type == 'depth below surface':
        dir = _gdps_client(final_forecast_hour=final_forecast_hour, 
                    step=step,
                    path=path,
                    proxies=proxies, 
                    chunk_size=chunk_size,
                    notifications=notifications,
                    level_type=level_type,
                    clear_data=clear_data,
                    variable=variable,
                    layer=layer)
        
        
    else:
        dir = _gdps_client(final_forecast_hour=final_forecast_hour, 
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
        
        ds = _cmc_post_processing.gdps_rdps_post_processing(dir,
                                                        western_bound,
                                                        eastern_bound,
                                                        northern_bound,
                                                        southern_bound,
                                                        variable=variable)
        
        if convert_temperature == True:
            ds = _convert_temperature_units(ds, 
                                        convert_to)
                        
        else:
            pass
        
        if level_type == 'pressure' or level_type == 'height above ground' or level_type == 'potential vorticity surface':
            print(f"GDPS Data Processing Complete: {variable.upper()} - {level}mb")
        elif level_type == 'pressure layer' or level_type == 'depth below surface':
            if level_type == 'pressure layer':
                print(f"GDPS Data Processing Complete: {variable.upper()} - {layer[0]}to{layer[1]}mb")
            else:
                print(f"GDPS Data Processing Complete: {variable.upper()} - {layer[0]}to{layer[1]}cm")
        else:
            print(f"GDPS Data Processing Complete: {variable.upper()} - surface")
        return ds
    else:
        pass
                
    