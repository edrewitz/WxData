"""
This file hosts the client that downloads WOOF-NAM data from Recast Systems.

(C) Eric J. Drewitz 2025-2026
"""
import sys as _sys
import wxdata.client.client as _client
import os as _os
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.post_processors.woof_nam_post_processing import woof_nam_post_processing as _woof_nam_post_processing
from wxdata.model_data.recast_systems.woof_nam.url_scanner import woof_nam_url_scanner as _woof_nam_url_scanner
from wxdata.utils.transforms import grib_to_netcdf as _grib_to_netcdf
from wxdata.utils.warnings import(
    eccodes_warning as _eccodes_warning,
    version_warning as _version_warning
)
from wxdata.calc.unit_conversion import convert_temperature_units as _convert_temperature_units
from wxdata.model_data.recast_systems.woof_nam.file_scanner import local_file_scanner as _local_file_scanner
from wxdata.utils.recycle_bin import(
    clear_recycle_bin_windows as _clear_recycle_bin_windows,
    clear_trash_bin_mac as _clear_trash_bin_mac,
    clear_trash_bin_linux as _clear_trash_bin_linux
)

_eccodes_warning()


def woof_nam(final_forecast_hour=84,
             path=f"WOOF-NAM",
             proxies=None,
             clear_data=False,
             clear_recycle_bin=False,
             convert_temperature=True,
             convert_to='celsius',
             process_data=True,
             chunk_size=8192,
             notifications='off',
             level_type='pressure',
             variables=['geopotential height',
                        'absolute vorticity',
                        'temperature',
                        'relative humidity',
                        'vertical velocity (pressure)',
                        'vertical velocity (height)',
                        'u-component of wind',
                        'v-component of wind',
                        'turbulent kinetic energy'],
             levels=[1000,
                     925,
                     850,
                     700,
                     500,
                     300,
                     250,
                     100,
                     50],
             to_netcdf=False,
             netcdf_path=f"WOOF-NAM/NETCDF",
            netcdf_filename=f"woof_nam.nc",
            delete_previous_netcdf_file=True,
            return_values=True):
    
    """
    
    
    """
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    level_type = level_type.lower()
    
    has_levs = ['pressure',
                  'height above ground',
                  'height below ground',
                  'pressure above ground',
                  'sigma layer',
                  'hybrid',
                  'depth below land layer']
    
    if level_type in has_levs:
        levels = levels
    else:
        levels = None
        
    url, run, filename = _woof_nam_url_scanner(final_forecast_hour,
                                     proxies)
    
    download = _local_file_scanner(path,
                                   run,
                                   filename)
    
    if download == True or clear_data == True:
        if run == 0:
            run = '00'
        elif run == 6:
            run = '06'
        elif run == 12:
            run = '12'
        else:
            run = '18'
        
        try:
            for file in _os.listdir(f"{path}"):
                _os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
        print(f"Downloading The Latest WOOF-NAM Data...")
        
        for i in range(0, (final_forecast_hour + 1), 1):
            if i < 10:
                _client.byte_range_request(f"{url}woof-nam.t{run}z.awphys0{i}.tm00.grib2",
                                           f"{url}woof-nam.t{run}z.awphys0{i}.tm00.grib2.idx",
                                           variables,
                                           levels,
                                           level_type,
                                           path,
                                           f"woof-nam.t{run}z.awphys0{i}.tm00.grib2",
                                           proxies=proxies,
                                           chunk_size=chunk_size,
                                           notifications=notifications,
                                           clear_recycle_bin=False,
                                           source='recast-systems',
                                           model='woof-nam')
            else:
                _client.byte_range_request(f"{url}woof-nam.t{run}z.awphys{i}.tm00.grib2",
                                           f"{url}woof-nam.t{run}z.awphys{i}.tm00.grib2.idx",
                                           variables,
                                           levels,
                                           level_type,
                                           path,
                                           f"woof-nam.t{run}z.awphys{i}.tm00.grib2",
                                           proxies=proxies,
                                           chunk_size=chunk_size,
                                           notifications=notifications,
                                           clear_recycle_bin=False,
                                           source='recast-systems',
                                           model='woof-nam')
                
        print(f"WOOF-NAM Download Complete")
    else:
        print(f"WOOF-NAM Data up to date.\nSkipping Download...")
        
    if process_data == True:
        print(f"WOOF-NAM Data Processing...")
        
        ds = _woof_nam_post_processing(path,
                                       level_type)
        
        if convert_temperature == True:
                ds = _convert_temperature_units(ds, 
                                            convert_to)
                
        else:
            pass
        
        print(f"WOOF-NAM Data Processing Complete.")
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