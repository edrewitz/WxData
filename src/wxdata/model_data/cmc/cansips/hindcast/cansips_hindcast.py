"""
This file hosts the functions for the CanSIPS Hindcast Data Client

(C) Eric J. Drewitz 2025-2026
"""
import os as _os
import wxdata.client.client as _client
import warnings as _warnings
_warnings.filterwarnings('ignore')
import wxdata.post_processors.cmc_post_processing as _cmc_post_processing

from wxdata.model_data.cmc.cansips.hindcast.file_sorter import sort_files as _sort_files
from wxdata.model_data.cmc.utils.file_scanner import scan_local_machine as _scan_local_machine
from wxdata.model_data.cmc.cansips.hindcast.url_scanner import cansips_hindcast_url_scanner as _cansips_hindcast_url_scanner
from wxdata.calc.unit_conversion import convert_temperature_units as _convert_temperature_units
from wxdata.utils.recycle_bin import(
    clear_recycle_bin_windows as _clear_recycle_bin_windows,
    clear_trash_bin_mac as _clear_trash_bin_mac,
    clear_trash_bin_linux as _clear_trash_bin_linux
)

def cansips_hindcast(western_bound=-180,
                     eastern_bound=180,
                     northern_bound=90,
                     southern_bound=-90,
                     level_type='pressure',
                     level=500,
                     variable='geopotential height',
                     proxies=None,
                     clear_recycle_bin=False,
                     convert_temperature=True,
                     convert_to='celsius',
                     process_data=True,
                     path=f"CanSIPS/Hindcast",
                     chunk_size=8192,
                     notifications='off',
                     clear_data=False):
    
    """
    
    """
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    print(f"Scanning https://dd.weather.gc.ca/ for the latest requested data.")
    print("Please Wait...")
    
    urls, files = _cansips_hindcast_url_scanner(level_type,
                                 variable,
                                 level,
                                 proxies)
    
    print(f"Server Scan Complete!")

    download = _scan_local_machine(urls,
                                    f"{path}/2020")
    
    if download == True or clear_data == True:
        print("Downloading Data")
        try:
            for file in _os.listdir(path):
                _os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
        for url, file in zip(urls, files):
            _client.get_gridded_data(url,
                                     f"{path}/Temp",
                                     file,
                                    proxies=proxies,
                                    chunk_size=chunk_size,
                                    notifications=notifications)
        _sort_files(f"{path}",
                    urls)

        print("CanSIPS Download Complete!")
    else:
        print("CanSIPS Data Is Up To Date\nSkipping Download...")
        
    if process_data == True:
        
        ds = _cmc_post_processing.cansips_hindcast_post_processing(path,
                                                                    variable,
                                                                    western_bound,
                                                                    eastern_bound,
                                                                    northern_bound,
                                                                    southern_bound)
        
        if convert_temperature == True:
            ds = _convert_temperature_units(ds, 
                                        convert_to)
         
        print("CanSIPS Hindcast Data Processing Complete!")   
        return ds
    else:
        pass
        
        
        