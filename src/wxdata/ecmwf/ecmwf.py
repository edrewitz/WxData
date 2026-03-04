"""
This file hosts the functions the user has to download ECMWF model data. 

(C) Eric J. Drewitz 2025-2026
"""

import os as _os
import contextlib as _contextlib
import io as _io
import warnings as _warnings
import time as _time
import sys as _sys
import wxdata.post_processors.ecmwf_post_processing as _ecmwf_post_processing
_warnings.filterwarnings('ignore')

from ecmwf.opendata import Client as _Client
from wxdata.ecmwf.url_scanners import(
    ecmwf_ifs_url_scanner as _ecmwf_ifs_url_scanner, 
    ecmwf_ifs_ens_url_scanner as _ecmwf_ifs_ens_url_scanner,
    ecmwf_aifs_url_scanner as _ecmwf_aifs_url_scanner,
    ecmwf_aifs_ens_url_scanner as _ecmwf_aifs_ens_url_scanner,
    ecmwf_ifs_wave_url_scanner as _ecmwf_ifs_wave_url_scanner,
    ecmwf_ifs_wave_ens_url_scanner as _ecmwf_ifs_wave_ens_url_scanner
)

from wxdata.ecmwf.file_funcs import(
    build_directory as _build_directory,
    clear_idx_files as _clear_idx_files,
    parse_filename as _parse_filename
)

from wxdata.ecmwf.keys import(
    get_levels as _get_levels,
    ifs_var_keys as _ifs_var_keys,
    aifs_var_keys as _aifs_var_keys
)

from wxdata.ecmwf.parsers import parse_date as _parse_date
from wxdata.calc.unit_conversion import convert_temperature_units as _convert_temperature_units
from wxdata.utils.file_scanner import local_file_scanner as _local_file_scanner
from wxdata.ecmwf.paths import ecmwf_branch_paths as _ecmwf_branch_paths
from wxdata.utils.file_funcs import(
    custom_branch as _custom_branch,
    clear_idx_files_in_path as _clear_idx_files_in_path,
    clear_old_data as _clear_old_data
)
from wxdata.utils.recycle_bin import(
        clear_recycle_bin_windows as _clear_recycle_bin_windows,
        clear_trash_bin_mac as _clear_trash_bin_mac,
        clear_trash_bin_linux as _clear_trash_bin_linux
)

original_stdout = _sys.stdout

def _check_forecast_hour(stream,
                         final_forecast_hour):
    
    """
    This function checks to make sure the final_forecast_hour is valid.
    
    The 00z and 12z runs are in steps of 3 hours between 0 and 144 hours then 6 hour steps from 144 to 360 hours.
    
    The 06z and 18z runs are in steps of 3 hours between 0 and 144 hours. These runs only go out to 144 hours.
    
    Required Arguments:
    
    1) stream (String) - 'oper' for 00z and 12z runs and 'scda' for 06z and 18z runs.
    
    2) final_forecast_hour (Integer) - The last forecast hour the user wishes to download. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    A corrected final_forecast_hour if necessary.
    """
    
    if stream == 'oper' or stream == 'wave':
        final_forecast_hour = final_forecast_hour
    else:
        if final_forecast_hour <= 144:
            final_forecast_hour = final_forecast_hour
        else:
            final_forecast_hour = 144
            print(f"User has a final_forecast_hour > 144. The 06z and 18z runs only have the first 144 hours. Defaulting to 144.")
            
    return final_forecast_hour

def _get_stream(model,
                run):
    
    """
    This function returns the value for stream based on the model runtime
    
    Required Arguments:
    
    1) model (String) - The model being used.
    
    2) run (Integer) - The model run time (0, 6, 12, 18)
    
    Optional Arguments: None
    
    Returns
    -------
    
    The value for stream needed for the ecmwf-opendata client    
    """
    
    if model == 'ifs':
        if run == 0 or run == 12:
            stream = 'oper'
        else:
            stream = 'scda'
    
    if model == 'ifs-wave':
        if run == 0 or run == 12:
            stream = 'wave'
        else:
            stream = 'scwv'
    
    if model == 'ifs-ensemble':
        stream = 'enfo'
        
    return stream

def _get_level_type(level_type):
    
    """
    This function returns the level type required to be passed into the ecmwf-opendata client
    
    Required Arguments:
    
    1) level_type (String) - The type of level the variable is.
    
    Level Types:
    ------------
    
    1) pressure
    2) surface
    3) soil
    
    """
    
    level_type = level_type.lower()
    
    level_types = {
        'pressure':'pl',
        'surface':'sfc',
        'soil':'sol'
    }
    
    return level_types[level_type]

def ecmwf_ifs(final_forecast_hour=144,
              western_bound=-180,
              eastern_bound=180,
              northern_bound=90,
              southern_bound=-90,
              step=3,
              proxies=None,
              process_data=True,
              clear_recycle_bin=False,
              convert_temperature=True,
              convert_to='celsius',
              custom_directory=None,
              notifications='off',
              source='ecmwf',
              level_type='surface',
              clear_data=False,
              variables=['Geopotential (step 0)',
                        'Standard deviation of sub-gridscale orography (step 0)',
                        '10-meter u-wind component',
                        '10-meter v-wind component',
                        '100-meter u-wind component',
                        '100-meter v-wind component',
                        'maximum 10-meter wind gust step 0',
                        'maximum 10-meter wind gust steps 3-144',
                        '2-meter temperature',
                        '2-meter dewpoint temperature',
                        'mean sea level pressure',
                        'mean zero-crossing wave period',
                        'mean wave direction',
                        'mean wave period',
                        'peak wave period',
                        'significant wave height',
                        'runoff',
                        'total precipitation',
                        'surface pressure',
                        'total column vertically integrated water vapor',
                        'total cloud cover',
                        'snow depth water equivalent',
                        'snowfall water equivalent',
                        'land sea mask',
                        'volumetric soil moisture content',
                        'soil temperature',
                        'most unstable cape',
                        'snow albedo',
                        '3-hour minimum 2-meter temperature',
                        '3-hour maximum 2-meter temperature',
                        '6-hour minimum 2-meter temperature',
                        '6-hour maximum 2-meter temperature',
                        'total precipitation rate',
                        'precipitation type',
                        'top net longwave thermal radiation',
                        'snow density',
                        'surface net longwave thermal radiation',
                        'surface net shortwave solar radiation',
                        'surface shortwave radiation downward',
                        'surface longwave radiation downward',
                        'northward turbulent surface stress',
                        'eastward turbulent surface stress',
                        'eastward surface sea water velocity',
                        'northward surface sea water velocity',
                        'sea ice thickness',
                        'sea surface height',
                        'divergence',
                        'geopotential height',
                        'specific humidity',
                        'relative humidity',
                        'temperature',
                        'u-wind component',
                        'v-wind component',
                        'vertical velocity',
                        'relative vorticity'],
              levels=[1000, 
                      925, 
                      850, 
                      700, 
                      600, 
                      500, 
                      400, 
                      300, 
                      250, 
                      200, 
                      150, 
                      100, 
                      50]):
    
    """
    This function scans for the latest ECMWF IFS dataset. If the dataset on the computer is old, the old data will be deleted
    and the new data will be downloaded. 
    
    1) final_forecast_hour (Integer) - Default = 360. The final forecast hour the user wishes to download. The ECMWF IFS
    goes out to 360 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    360 by the nereast increment of 3 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    7) proxies (String or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies="http://your-proxy-address:port" ---> ds = ecmwf_ifs(proxies=proxies)
    
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    9) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    10) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    11) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    12) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
    
    13) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    14) source (String) - Default='ecmwf'. The data server choice. When set to 'ecmwf' data is pulled from ecmwf-opendata.
        To switch to Amazon AWS, switch source='aws'. 
        
    15) level_type (String) - Default='surface'. The level of the parameters being queried. 
    
        level_types
        -----------
        
        1) 'surface'
        2) 'pressure'
        3) 'soil
    
    16) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
        
    17) variables (String List) - Default is all variables. The list of variable names in plain-language. 
    
        variables
        ---------
        
        'Geopotential (step 0)'
        'Standard deviation of sub-gridscale orography (step 0)'
        '10-meter u-wind component'
        '10-meter v-wind component'
        '100-meter u-wind component'
        '100-meter v-wind component'
        'maximum 10-meter wind gust step 0'
        'maximum 10-meter wind gust steps 3-144'
        '2-meter temperature'
        '2-meter dewpoint temperature'
        'mean sea level pressure'
        'mean zero-crossing wave period'
        'mean wave direction'
        'mean wave period'
        'peak wave period'
        'significant wave height'
        'runoff'
        'total precipitation'
        'surface pressure'
        'total column vertically integrated water vapor'
        'total cloud cover'
        'snow depth water equivalent'
        'snowfall water equivalent'
        'land sea mask'
        'volumetric soil moisture content'
        'soil temperature'
        'most unstable cape'
        'snow albedo'
        '3-hour minimum 2-meter temperature'
        '3-hour maximum 2-meter temperature'
        '6-hour minimum 2-meter temperature'
        '6-hour maximum 2-meter temperature'
        'total precipitation rate'
        'precipitation type'
        'top net longwave thermal radiation'
        'snow density'
        'surface net longwave thermal radiation'
        'surface net shortwave solar radiation'
        'surface shortwave radiation downward'
        'surface longwave radiation downward'
        'northward turbulent surface stress'
        'eastward turbulent surface stress'
        'eastward surface sea water velocity'
        'northward surface sea water velocity'
        'sea ice thickness'
        'sea surface height'
        'divergence'
        'geopotential height'
        'specific humidity'
        'relative humidity'
        'temperature'
        'u-wind component'
        'v-wind component'
        'vertical velocity'
        'relative vorticity'
        
    18) levels (Integer List) - Default=[1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50]. 
        When level_type='pressure', this is the list of the pressure levels. 
        
        Example: User wants only the 500 mb level: levels=[500]
        
    Returns
    -------
    
    An xarray.data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys
    
    Plain Language ECMWF IFS Variable Keys (After Post-Processing)
    --------------------------------------------------------------
    
    'total_column_water'
    'total_column_vertically_integrated_water_vapor'
    'snow_albedo'
    'land_sea_mask'
    'specific_humidity'
    'volumetric_soil_moisture_content'
    'sea_ice_thickness'
    'soil_temperature'
    'surface_longwave_radiation_downward'
    'surface_net_shortwave_solar_radiation'
    'surface_net_longwave_thermal_radiation'
    'top_net_longwave_thermal_radiation'
    '10m_max_wind_gust'
    'vertical_velocity'
    'relative_vorticity'
    'relative_humidity'
    'geopotential_height'
    'eastward_turbulent_surface_stress'
    'u_wind_component'
    'divergence'
    'northward_turbulent_surface_stress'
    'v_wind_component'
    'air_temperature'
    'water_runoff'
    'total_precipitation'
    'mslp'
    'eastward_surface_sea_water_velocity'
    'most_unstable_cape'
    'northward_surface_sea_water_velocity'
    'sea_surface_height'
    'standard_deviation_of_sub_gridscale_orography'
    'skin_temperature'
    'slope_of_sub_gridscale_orography'
    '10m_u_wind_component'
    'precipitation_type'
    '10m_v_wind_component'
    'total_precipitation_rate'
    'surface_shortwave_radiation_downward'
    'geopotential'
    'surface_pressure'
    '2m_temperature'
    '100m_u_wind_component'
    '100m_v_wind_component'
    '2m_dew_point'
    '2m_relative_humidity'
    
    """
    
    level_type = _get_level_type(level_type)
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    if proxies == None:
        pass
    else:
        _os.environ['http_proxy'] = proxies
        _os.environ['https_proxy'] = proxies
    
    if custom_directory == None:
        _build_directory('ifs', 
                        'operational')
        
        path = _ecmwf_branch_paths('ifs', 
                        'operational')
        
    else:
        path = _custom_branch(custom_directory)
        
    if clear_data == True:
        _clear_old_data(path)
    else:
        pass
    
    _clear_idx_files(path)
    
    url, filename, run = _ecmwf_ifs_url_scanner(final_forecast_hour)
    
    
    stream = _get_stream('ifs',
                         run)
    
    final_forecast_hour = _check_forecast_hour(stream,
                                                final_forecast_hour)
    valid_date = _parse_date(url,
                             'ifs')
    
    params = _ifs_var_keys(variables)

    download = _local_file_scanner(path, 
                                  filename,
                                  'ecmwf',
                                  run,
                                  model='operational ifs')
    

    date = _parse_filename(filename)
    
    levels = _get_levels(levels)
    
    client = _Client(source=source,
                     model='ifs')
    if download == True:
        print(f"Downloading ECMWF IFS...\n")
        print(f"By downloading data from the ECMWF open data dataset, you agree to the terms: Attribution 4.0 International (CC BY 4.0).\nPlease attribute ECMWF when downloading this data.")
        _clear_old_data(path)
        
        if final_forecast_hour <= 144:
            for i in range(0, final_forecast_hour + step, step):
                f = _io.StringIO()
                with _contextlib.redirect_stdout(f):
                    if level_type == 'pl':
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="fc",
                                            levtype=level_type,
                                            param=params,
                                            levelist=levels,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                        except Exception as e:
                            for k in range(0, 100, 1):
                                print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                _time.sleep(60)
                                try:
                                    client.retrieve(date=valid_date,
                                                time=run,
                                                step=i,
                                                stream=stream,
                                                type="fc",
                                                levtype=level_type,
                                                param=params,
                                                levelist=levels,
                                                target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                                    break
                                except Exception as e:
                                    k = k
                                    if k >= 99:
                                        print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                        _sys.exit(1)
                                    else:
                                        pass
                                
                                
                    else:
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="fc",
                                            levtype=level_type,
                                            param=params,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                        except Exception as e:
                            for k in range(0, 100, 1):
                                print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                _time.sleep(60)
                                try:
                                    client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="fc",
                                            levtype=level_type,
                                            param=params,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                                    break
                                except Exception as e:
                                    k = k
                                    if k >= 99:
                                        print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                        _sys.exit(1)
                                    else:
                                        pass
                            
                    if notifications == True:
                        print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2 saved to {path}", file=original_stdout)
                    else:
                        pass
        else:
            for i in range(0, 144 + step, step):
                f = _io.StringIO()
                with _contextlib.redirect_stdout(f):
                    if level_type == 'pl':
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="fc",
                                            levtype=level_type,
                                            param=params,
                                            levelist=levels,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                        except Exception as e:
                            for k in range(0, 100, 1):
                                print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                _time.sleep(60)
                                try:
                                    client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="fc",
                                            levtype=level_type,
                                            param=params,
                                            levelist=levels,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                                    break
                                except Exception as e:
                                    k = k
                                    if k >= 99:
                                        print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                        _sys.exit(1)
                                    else:
                                        pass
                    else:
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="fc",
                                            levtype=level_type,
                                            param=params,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                        except Exception as e:
                            for k in range(0, 100, 1):
                                print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                _time.sleep(60)
                                try:
                                    client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="fc",
                                            levtype=level_type,
                                            param=params,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                                    break
                                except Exception as e:
                                    k = k
                                    if k >= 99:
                                        print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                        _sys.exit(1)   
                                    else:
                                        pass                         
                    if notifications == True:
                        print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2 saved to {path}", file=original_stdout)
                    else:
                        pass
                                
            for i in range(144, final_forecast_hour + 6, 6):
                f = _io.StringIO()
                with _contextlib.redirect_stdout(f):
                    if level_type == 'pl':
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="fc",
                                            levtype=level_type,
                                            param=params,
                                            levelist=levels,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                        except Exception as e:
                            for k in range(0, 100, 1):
                                print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                _time.sleep(60)
                                try:
                                    client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="fc",
                                            levtype=level_type,
                                            param=params,
                                            levelist=levels,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                                    break
                                except Exception as e:
                                    k = k
                                    if k >= 99:
                                        print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                        _sys.exit(1)   
                                    else:
                                        pass                       
                    else:
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="fc",
                                            levtype=level_type,
                                            param=params,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                        except Exception as e:
                            for k in range(0, 100, 1):
                                print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                _time.sleep(60)
                                try:
                                    client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="fc",
                                            levtype=level_type,
                                            param=params,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                                    break
                                except Exception as e:
                                    k = k
                                    if k >= 99:
                                        print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                        _sys.exit(1) 
                                    else:
                                        pass                           
                    if notifications == True:
                        print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2 saved to {path}", file=original_stdout)
                    else:
                        pass

        
        print(f"ECMWF IFS Download Complete.")    
        
    else:
        print(f"ECMWF IFS Data is up to date. Skipping download...")    

    if process_data == True:
        print(f"ECMWF IFS Data Processing...")
        
        ds = _ecmwf_post_processing.ecmwf_ifs_post_processing(path,
                                                            western_bound, 
                                                            eastern_bound, 
                                                            northern_bound, 
                                                            southern_bound)
        
        _clear_idx_files_in_path(path)
            
        if convert_temperature == True:
                ds = _convert_temperature_units(ds, 
                                            convert_to)
                
        else:
            pass
        
        print(f"ECMWF IFS Data Processing Complete.")
        
        return ds
    
    else:
        pass
    
    
def ecmwf_ifs_ens(final_forecast_hour=144,
              western_bound=-180,
              eastern_bound=180,
              northern_bound=90,
              southern_bound=-90,
              step=3,
              proxies=None,
              process_data=True,
              clear_recycle_bin=False,
              convert_temperature=True,
              convert_to='celsius',
              custom_directory=None,
              notifications='off',
              source='ecmwf',
              level_type='surface',
              clear_data=False,
              variables=['Geopotential (step 0)',
                        'Standard deviation of sub-gridscale orography (step 0)',
                        '10-meter u-wind component',
                        '10-meter v-wind component',
                        '100-meter u-wind component',
                        '100-meter v-wind component',
                        'maximum 10-meter wind gust step 0',
                        'maximum 10-meter wind gust steps 3-144',
                        '2-meter temperature',
                        '2-meter dewpoint temperature',
                        'mean sea level pressure',
                        'mean zero-crossing wave period',
                        'mean wave direction',
                        'mean wave period',
                        'peak wave period',
                        'significant wave height',
                        'runoff',
                        'total precipitation',
                        'surface pressure',
                        'total column vertically integrated water vapor',
                        'total cloud cover',
                        'snow depth water equivalent',
                        'snowfall water equivalent',
                        'land sea mask',
                        'volumetric soil moisture content',
                        'soil temperature',
                        'most unstable cape',
                        'snow albedo',
                        '3-hour minimum 2-meter temperature',
                        '3-hour maximum 2-meter temperature',
                        '6-hour minimum 2-meter temperature',
                        '6-hour maximum 2-meter temperature',
                        'total precipitation rate',
                        'precipitation type',
                        'top net longwave thermal radiation',
                        'snow density',
                        'surface net longwave thermal radiation',
                        'surface net shortwave solar radiation',
                        'surface shortwave radiation downward',
                        'surface longwave radiation downward',
                        'northward turbulent surface stress',
                        'eastward turbulent surface stress',
                        'eastward surface sea water velocity',
                        'northward surface sea water velocity',
                        'sea ice thickness',
                        'sea surface height',
                        'divergence',
                        'geopotential height',
                        'specific humidity',
                        'relative humidity',
                        'temperature',
                        'u-wind component',
                        'v-wind component',
                        'vertical velocity',
                        'relative vorticity'],
              levels=[1000, 
                      925, 
                      850, 
                      700, 
                      600, 
                      500, 
                      400, 
                      300, 
                      250, 
                      200, 
                      150, 
                      100, 
                      50],
                members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                      31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
                      41, 42, 43, 44, 45, 46, 47, 48, 49, 50]):
    
    """
    This function scans for the latest ECMWF IFS dataset. If the dataset on the computer is old, the old data will be deleted
    and the new data will be downloaded. 
    
    1) final_forecast_hour (Integer) - Default = 360. The final forecast hour the user wishes to download. The ECMWF IFS
    goes out to 360 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    360 by the nereast increment of 3 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    7) proxies (String or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies="http://your-proxy-address:port"
    
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    9) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    10) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    11) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    12) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
    
    13) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    14) source (String) - Default='ecmwf'. The data server choice. When set to 'ecmwf' data is pulled from ecmwf-opendata.
        To switch to Amazon AWS, switch source='aws'. 
        
    15) level_type (String) - Default='surface'. The level of the parameters being queried. 
    
        level_types
        -----------
        
        1) 'surface'
        2) 'pressure'
        3) 'soil
    
    16) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
        
    17) variables (String List) - Default is all variables. The list of variable names in plain-language. 
    
        variables
        ---------
        
        'Geopotential (step 0)'
        'Standard deviation of sub-gridscale orography (step 0)'
        '10-meter u-wind component'
        '10-meter v-wind component'
        '100-meter u-wind component'
        '100-meter v-wind component'
        'maximum 10-meter wind gust step 0'
        'maximum 10-meter wind gust steps 3-144'
        '2-meter temperature'
        '2-meter dewpoint temperature'
        'mean sea level pressure'
        'mean zero-crossing wave period'
        'mean wave direction'
        'mean wave period'
        'peak wave period'
        'significant wave height'
        'runoff'
        'total precipitation'
        'surface pressure'
        'total column vertically integrated water vapor'
        'total cloud cover'
        'snow depth water equivalent'
        'snowfall water equivalent'
        'land sea mask'
        'volumetric soil moisture content'
        'soil temperature'
        'most unstable cape'
        'snow albedo'
        '3-hour minimum 2-meter temperature'
        '3-hour maximum 2-meter temperature'
        '6-hour minimum 2-meter temperature'
        '6-hour maximum 2-meter temperature'
        'total precipitation rate'
        'precipitation type'
        'top net longwave thermal radiation'
        'snow density'
        'surface net longwave thermal radiation'
        'surface net shortwave solar radiation'
        'surface shortwave radiation downward'
        'surface longwave radiation downward'
        'northward turbulent surface stress'
        'eastward turbulent surface stress'
        'eastward surface sea water velocity'
        'northward surface sea water velocity'
        'sea ice thickness'
        'sea surface height'
        'divergence'
        'geopotential height'
        'specific humidity'
        'relative humidity'
        'temperature'
        'u-wind component'
        'v-wind component'
        'vertical velocity'
        'relative vorticity'
        
    18) levels (Integer List) - Default=[1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50]. 
        When level_type='pressure', this is the list of the pressure levels. 
        
        Example: User wants only the 500 mb level: levels=[500]
        
    19) members (Integer List) - Default=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                          11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                          21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                                          31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
                                          41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
                                          
        The ECMWF IFS Ensemble consists of 50 members. 
        
        Example: User wants only the first 5 members: members=[1,2,3,4,5]
            
    Returns
    -------
    
    An xarray.data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys
    
    Plain Language ECMWF IFS Variable Keys (After Post-Processing)
    --------------------------------------------------------------
    
    'total_column_water'
    'total_column_vertically_integrated_water_vapor'
    'snow_albedo'
    'land_sea_mask'
    'specific_humidity'
    'volumetric_soil_moisture_content'
    'sea_ice_thickness'
    'soil_temperature'
    'surface_longwave_radiation_downward'
    'surface_net_shortwave_solar_radiation'
    'surface_net_longwave_thermal_radiation'
    'top_net_longwave_thermal_radiation'
    '10m_max_wind_gust'
    'vertical_velocity'
    'relative_vorticity'
    'relative_humidity'
    'geopotential_height'
    'eastward_turbulent_surface_stress'
    'u_wind_component'
    'divergence'
    'northward_turbulent_surface_stress'
    'v_wind_component'
    'air_temperature'
    'water_runoff'
    'total_precipitation'
    'mslp'
    'eastward_surface_sea_water_velocity'
    'most_unstable_cape'
    'northward_surface_sea_water_velocity'
    'sea_surface_height'
    'standard_deviation_of_sub_gridscale_orography'
    'skin_temperature'
    'slope_of_sub_gridscale_orography'
    '10m_u_wind_component'
    'precipitation_type'
    '10m_v_wind_component'
    'total_precipitation_rate'
    'surface_shortwave_radiation_downward'
    'geopotential'
    'surface_pressure'
    '2m_temperature'
    '100m_u_wind_component'
    '100m_v_wind_component'
    '2m_dew_point'
    '2m_relative_humidity'
    '3_hr_maximum_2m_temperature'
    '3_hr_minimum_2m_temperature'
    
    """
    
    level_type = _get_level_type(level_type)
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    if proxies == None:
        pass
    else:
        _os.environ['http_proxy'] = proxies
        _os.environ['https_proxy'] = proxies
    
    if custom_directory == None:
        _build_directory('ifs', 
                        'ensemble')
        
        path = _ecmwf_branch_paths('ifs', 
                        'ensemble')
        
    else:
        path = _custom_branch(custom_directory)
        
    if clear_data == True:
        _clear_old_data(path)
    else:
        pass
    
    _clear_idx_files(path)
    
    url, filename, run = _ecmwf_ifs_ens_url_scanner(final_forecast_hour)
    
    
    stream = _get_stream('ifs-ensemble',
                         run)
    
    final_forecast_hour = _check_forecast_hour(stream,
                                                final_forecast_hour)
    valid_date = _parse_date(url,
                             'ifs-ensemble')
    
    params = _ifs_var_keys(variables)

    download = _local_file_scanner(path, 
                                  filename,
                                  'ecmwf',
                                  run,
                                  model='ifs-ensemble')
    

    date = _parse_filename(filename)
    
    levels = _get_levels(levels)
    
    client = _Client(source=source,
                     model='ifs')
    if download == True:
        print(f"Downloading ECMWF IFS ENSEMBLE...\n")
        print(f"By downloading data from the ECMWF open data dataset, you agree to the terms: Attribution 4.0 International (CC BY 4.0).\nPlease attribute ECMWF when downloading this data.")
        _clear_old_data(path)
        
        if final_forecast_hour <= 144:
            for i in range(0, final_forecast_hour + step, step):
                f = _io.StringIO()
                with _contextlib.redirect_stdout(f):
                    if level_type == 'pl':
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="ef",
                                            levtype=level_type,
                                            param=params,
                                            levelist=levels,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-ef.grib2")
                        except Exception as e:
                            for k in range(0, 100, 1):
                                print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                _time.sleep(60)
                                try:
                                    client.retrieve(date=valid_date,
                                                time=run,
                                                step=i,
                                                stream=stream,
                                                type="ef",
                                                levtype=level_type,
                                                param=params,
                                                levelist=levels,
                                                number=members,
                                                target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-ef.grib2")
                                    break
                                except Exception as e:
                                    k = k
                                    if k >= 99:
                                        print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                        _sys.exit(1)
                                    else:
                                        pass
                                
                                
                    else:
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="ef",
                                            levtype=level_type,
                                            param=params,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-ef.grib2")
                        except Exception as e:
                            for k in range(0, 100, 1):
                                print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                _time.sleep(60)
                                try:
                                    client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="ef",
                                            levtype=level_type,
                                            param=params,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-ef.grib2")
                                    break
                                except Exception as e:
                                    k = k
                                    if k >= 99:
                                        print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                        _sys.exit(1)
                                    else:
                                        pass
                            
                    if notifications == True:
                        print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2 saved to {path}", file=original_stdout)
                    else:
                        pass
        else:
            for i in range(0, 144 + step, step):
                f = _io.StringIO()
                with _contextlib.redirect_stdout(f):
                    if level_type == 'pl':
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="ef",
                                            levtype=level_type,
                                            param=params,
                                            levelist=levels,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-ef.grib2")
                        except Exception as e:
                            for k in range(0, 100, 1):
                                print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                _time.sleep(60)
                                try:
                                    client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="ef",
                                            levtype=level_type,
                                            param=params,
                                            levelist=levels,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-ef.grib2")
                                    break
                                except Exception as e:
                                    k = k
                                    if k >= 99:
                                        print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                        _sys.exit(1)
                                    else:
                                        pass
                    else:
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="ef",
                                            levtype=level_type,
                                            param=params,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-ef.grib2")
                        except Exception as e:
                            for k in range(0, 100, 1):
                                print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                _time.sleep(60)
                                try:
                                    client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="ef",
                                            levtype=level_type,
                                            param=params,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-ef.grib2")
                                    break
                                except Exception as e:
                                    k = k
                                    if k >= 99:
                                        print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                        _sys.exit(1)   
                                    else:
                                        pass                         
                    if notifications == True:
                        print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2 saved to {path}", file=original_stdout)
                    else:
                        pass
                                
            for i in range(144, final_forecast_hour + 6, 6):
                f = _io.StringIO()
                with _contextlib.redirect_stdout(f):
                    if level_type == 'pl':
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="ef",
                                            levtype=level_type,
                                            param=params,
                                            levelist=levels,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-ef.grib2")
                        except Exception as e:
                            for k in range(0, 100, 1):
                                print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                _time.sleep(60)
                                try:
                                    client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="ef",
                                            levtype=level_type,
                                            param=params,
                                            levelist=levels,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-ef.grib2")
                                    break
                                except Exception as e:
                                    k = k
                                    if k >= 99:
                                        print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                        _sys.exit(1)   
                                    else:
                                        pass                       
                    else:
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="ef",
                                            levtype=level_type,
                                            param=params,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-ef.grib2")
                        except Exception as e:
                            for k in range(0, 100, 1):
                                print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                _time.sleep(60)
                                try:
                                    client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="ef",
                                            levtype=level_type,
                                            param=params,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-ef.grib2")
                                    break
                                except Exception as e:
                                    k = k
                                    if k >= 99:
                                        print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                        _sys.exit(1) 
                                    else:
                                        pass                           
                    if notifications == True:
                        print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2 saved to {path}", file=original_stdout)
                    else:
                        pass

        
        print(f"ECMWF IFS ENSEMBLE Download Complete.")    
        
    else:
        print(f"ECMWF IFS ENSEMBLE Data is up to date. Skipping download...")    

    if process_data == True:
        print(f"ECMWF IFS ENSEMBLE Data Processing...")
        
        ds = _ecmwf_post_processing.ecmwf_ifs_post_processing(path,
                                                            western_bound, 
                                                            eastern_bound, 
                                                            northern_bound, 
                                                            southern_bound)
        
        _clear_idx_files_in_path(path)
            
        if convert_temperature == True:
                ds = _convert_temperature_units(ds, 
                                            convert_to)
                
        else:
            pass
        
        print(f"ECMWF IFS ENSEMBLE Data Processing Complete.")
        
        return ds
    
    else:
        pass
    

def ecmwf_aifs(final_forecast_hour=360,
                    western_bound=-180,
                    eastern_bound=180,
                    northern_bound=90,
                    southern_bound=-90,
                    proxies=None,
                    process_data=True,
                    clear_recycle_bin=False,
                    convert_temperature=True,
                    convert_to='celsius',
                    custom_directory=None,
                    notifications='off',
                    source='ecmwf',
                    level_type='surface',
                    clear_data=False,
                    variables=['geopotential',
                                'total column water',
                                'mean sea level pressure',
                                'standard deviation of sub-gridscale orography',
                                'slope of sub-gridscale orography',
                                '10-meter u-wind component',
                                '10-meter v-wind component',
                                '2-meter temperature',
                                '2-meter dew point',
                                'surface shortwave radiation downward',
                                'land sea mask',
                                'surface longwave radiation downward',
                                'low cloud cover',
                                'mid-level cloud cover',
                                'high cloud cover',
                                'runoff water equivalent',
                                'convective precipitation',
                                'snowfall water equivalent',
                                'total cloud cover',
                                'total precipitation',
                                '100-meter u-wind component',
                                '100-meter v-wind component',
                                'skin temperature',
                                'surface pressure',
                                'specific humidity',
                                'relative humidity',
                                'temperature',
                                'u-wind component',
                                'v-wind component',
                                'vertical velocity',
                                'volumetric soil moisture content',
                                'soil temperature'],
                    levels=[1000, 
                            925, 
                            850, 
                            700, 
                            600, 
                            500, 
                            400, 
                            300, 
                            250, 
                            200, 
                            150, 
                            100, 
                            50]):

    """
    This function scans for the latest ECMWF IFS dataset. If the dataset on the computer is old, the old data will be deleted
    and the new data will be downloaded. 
    
    1) final_forecast_hour (Integer) - Default = 360. The final forecast hour the user wishes to download. The ECMWF IFS
    goes out to 360 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    360 by the nereast increment of 3 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        } 
    
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    9) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    10) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    11) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    12) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
    
    13) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
        
    Returns
    -------
    
    An xarray data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys
    
    Plain Language ECMWF IFS Variable Keys (After Post-Processing)
    --------------------------------------------------------------
    
    'total_column_water'
    'total_column_vertically_integrated_water_vapor'
    'snow_albedo'
    'land_sea_mask'
    'specific_humidity'
    'volumetric_soil_moisture_content'
    'sea_ice_thickness'
    'soil_temperature'
    'surface_longwave_radiation_downward'
    'surface_net_shortwave_solar_radiation'
    'surface_net_longwave_thermal_radiation'
    'top_net_longwave_thermal_radiation'
    '10m_max_wind_gust'
    'vertical_velocity'
    'relative_vorticity'
    'relative_humidity'
    'geopotential_height'
    'eastward_turbulent_surface_stress'
    'u_wind_component'
    'divergence'
    'northward_turbulent_surface_stress'
    'v_wind_component'
    'air_temperature'
    'water_runoff'
    'total_precipitation'
    'mslp'
    'eastward_surface_sea_water_velocity'
    'most_unstable_cape'
    'northward_surface_sea_water_velocity'
    'sea_surface_height'
    'standard_deviation_of_sub_gridscale_orography'
    'skin_temperature'
    'slope_of_sub_gridscale_orography'
    '10m_u_wind_component'
    'precipitation_type'
    '10m_v_wind_component'
    'total_precipitation_rate'
    'surface_shortwave_radiation_downward'
    'geopotential'
    'surface_pressure'
    '2m_temperature'
    '100m_u_wind_component'
    '100m_v_wind_component'
    '2m_dew_point'
    '2m_relative_humidity'
    
    """
    
    level_type = _get_level_type(level_type)
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    if proxies == None:
        pass
    else:
        _os.environ['http_proxy'] = proxies
        _os.environ['https_proxy'] = proxies
    
    if custom_directory == None:
        _build_directory('aifs', 
                        'operational')
        
        path = _ecmwf_branch_paths('aifs', 
                        'operational')
        
    else:
        path = _custom_branch(custom_directory)
        
    if clear_data == True:
        _clear_old_data(path)
    else:
        pass
    
    _clear_idx_files(path)
    
    url, filename, run = _ecmwf_aifs_url_scanner(final_forecast_hour)
    
    
    valid_date = _parse_date(url,
                             'aifs-single')
    
    params = _aifs_var_keys(variables)

    download = _local_file_scanner(path, 
                                  filename,
                                  'ecmwf',
                                  run)
    

    date = _parse_filename(filename)
    
    levels = _get_levels(levels)
    
    client = _Client(source=source,
                     model='aifs-single')
    if download == True:
        print(f"Downloading ECMWF AIFS...\n")
        print(f"By downloading data from the ECMWF open data dataset, you agree to the terms: Attribution 4.0 International (CC BY 4.0).\nPlease attribute ECMWF when downloading this data.")
        _clear_old_data(path)
        
        for i in range(0, final_forecast_hour + 6, 6):
            f = _io.StringIO()
            with _contextlib.redirect_stdout(f):
                if level_type == 'pl':
                    try:
                        client.retrieve(date=valid_date,
                                        time=run,
                                        step=i,
                                        stream='oper',
                                        type="fc",
                                        levtype=level_type,
                                        param=params,
                                        levelist=levels,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2")
                    except Exception as e:
                            for k in range(0, 100, 1):
                                print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                _time.sleep(60)
                                try:
                                    client.retrieve(date=valid_date,
                                        time=run,
                                        step=i,
                                        stream='oper',
                                        type="fc",
                                        levtype=level_type,
                                        param=params,
                                        levelist=levels,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2")
                                    break
                                except Exception as e:
                                    k = k
                                    if k >= 99:
                                        print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                        _sys.exit(1)  
                                    else:
                                        pass                       
                else:
                    try:
                        client.retrieve(date=valid_date,
                                        time=run,
                                        step=i,
                                        stream='oper',
                                        type="fc",
                                        levtype=level_type,
                                        param=params,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2")
                    except Exception as e:
                        for k in range(0, 100, 1):
                                print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                _time.sleep(60)
                                try:
                                    client.retrieve(date=valid_date,
                                        time=run,
                                        step=i,
                                        stream='oper',
                                        type="fc",
                                        levtype=level_type,
                                        param=params,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2")
                                    break
                                except Exception as e:
                                    k = k
                                    if k >= 99:
                                        print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                        _sys.exit(1)
                                    else:
                                        pass
                if notifications == True:
                    print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2 saved to {path}", file=original_stdout)
                else:
                    pass

        print(f"ECMWF AIFS Download Complete.")    
        
    else:
        print(f"ECMWF AIFS Data is up to date. Skipping download...")    
        
    if process_data == True:
        print(f"ECMWF AIFS Data Processing...")
        
        ds = _ecmwf_post_processing.ecmwf_aifs_post_processing(path,
                                                            western_bound, 
                                                            eastern_bound, 
                                                            northern_bound, 
                                                            southern_bound)
        
        _clear_idx_files_in_path(path)
            
        if convert_temperature == True:
            ds = _convert_temperature_units(ds, 
                                        convert_to)

                
        else:
            pass
        
        print(f"ECMWF AIFS Data Processing Complete.")
        return ds
    
    else:
        pass
    
    
def ecmwf_aifs_ens(final_forecast_hour=360,
                    western_bound=-180,
                    eastern_bound=180,
                    northern_bound=90,
                    southern_bound=-90,
                    proxies=None,
                    process_data=True,
                    clear_recycle_bin=False,
                    convert_temperature=True,
                    convert_to='celsius',
                    custom_directory=None,
                    notifications='off',
                    source='ecmwf',
                    level_type='surface',
                    cat='control',
                    clear_data=False,
                    variables=['geopotential',
                                'total column water',
                                'mean sea level pressure',
                                'standard deviation of sub-gridscale orography',
                                'slope of sub-gridscale orography',
                                '10-meter u-wind component',
                                '10-meter v-wind component',
                                '2-meter temperature',
                                '2-meter dew point',
                                'surface shortwave radiation downward',
                                'land sea mask',
                                'surface longwave radiation downward',
                                'low cloud cover',
                                'mid-level cloud cover',
                                'high cloud cover',
                                'runoff water equivalent',
                                'convective precipitation',
                                'snowfall water equivalent',
                                'total cloud cover',
                                'total precipitation',
                                '100-meter u-wind component',
                                '100-meter v-wind component',
                                'skin temperature',
                                'surface pressure',
                                'specific humidity',
                                'relative humidity',
                                'temperature',
                                'u-wind component',
                                'v-wind component',
                                'vertical velocity',
                                'volumetric soil moisture content',
                                'soil temperature'],
                    levels=[1000, 
                            925, 
                            850, 
                            700, 
                            600, 
                            500, 
                            400, 
                            300, 
                            250, 
                            200, 
                            150, 
                            100, 
                            50],
                    members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                      31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
                      41, 42, 43, 44, 45, 46, 47, 48, 49, 50]):

    """
    This function scans for the latest ECMWF IFS dataset. If the dataset on the computer is old, the old data will be deleted
    and the new data will be downloaded. 
    
    1) final_forecast_hour (Integer) - Default = 360. The final forecast hour the user wishes to download. The ECMWF IFS
    goes out to 360 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    360 by the nereast increment of 3 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        } 
    
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    9) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    10) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    11) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    12) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
    
    13) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
        
    Returns
    -------
    
    An xarray data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys
    
    Plain Language ECMWF IFS Variable Keys (After Post-Processing)
    --------------------------------------------------------------
    
    'total_column_water'
    'total_column_vertically_integrated_water_vapor'
    'snow_albedo'
    'land_sea_mask'
    'specific_humidity'
    'volumetric_soil_moisture_content'
    'sea_ice_thickness'
    'soil_temperature'
    'surface_longwave_radiation_downward'
    'surface_net_shortwave_solar_radiation'
    'surface_net_longwave_thermal_radiation'
    'top_net_longwave_thermal_radiation'
    '10m_max_wind_gust'
    'vertical_velocity'
    'relative_vorticity'
    'relative_humidity'
    'geopotential_height'
    'eastward_turbulent_surface_stress'
    'u_wind_component'
    'divergence'
    'northward_turbulent_surface_stress'
    'v_wind_component'
    'air_temperature'
    'water_runoff'
    'total_precipitation'
    'mslp'
    'eastward_surface_sea_water_velocity'
    'most_unstable_cape'
    'northward_surface_sea_water_velocity'
    'sea_surface_height'
    'standard_deviation_of_sub_gridscale_orography'
    'skin_temperature'
    'slope_of_sub_gridscale_orography'
    '10m_u_wind_component'
    'precipitation_type'
    '10m_v_wind_component'
    'total_precipitation_rate'
    'surface_shortwave_radiation_downward'
    'geopotential'
    'surface_pressure'
    '2m_temperature'
    '100m_u_wind_component'
    '100m_v_wind_component'
    '2m_dew_point'
    '2m_relative_humidity'
    
    """
    
    level_type = _get_level_type(level_type)
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    if proxies == None:
        pass
    else:
        _os.environ['http_proxy'] = proxies
        _os.environ['https_proxy'] = proxies
    
    if custom_directory == None:
        cat = cat.lower()
        if cat == 'control':
            dir = 'ensemble control'
        else:
            dir = 'ensemble members'
        
        _build_directory('aifs', 
                        dir)
        
        path = _ecmwf_branch_paths('aifs', 
                        dir)
        
    else:
        path = _custom_branch(custom_directory)
    
    _clear_idx_files(path)
    
    url, filename, run, cat = _ecmwf_aifs_ens_url_scanner(final_forecast_hour,
                                                          cat)
    
    
    valid_date = _parse_date(url,
                             'aifs-ens')
    
    params = _aifs_var_keys(variables)

    download = _local_file_scanner(path, 
                                  filename,
                                  'ecmwf',
                                  run)
    
    if clear_data == True:
        download = True
    else:
        pass
    
    date = _parse_filename(filename)
    
    levels = _get_levels(levels)
    
    client = _Client(source=source,
                     model='aifs-ens')
    if download == True:
        print(f"Downloading ECMWF AIFS ENSEMBLE {cat.upper()}...\n")
        print(f"By downloading data from the ECMWF open data dataset, you agree to the terms: Attribution 4.0 International (CC BY 4.0).\nPlease attribute ECMWF when downloading this data.")
        _clear_old_data(path)
        
        if cat == 'cf':        
            for i in range(0, final_forecast_hour + 6, 6):
                f = _io.StringIO()
                with _contextlib.redirect_stdout(f):
                    if level_type == 'pl':
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream='enfo',
                                            type=cat,
                                            levtype=level_type,
                                            param=params,
                                            levelist=levels,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-enfo-{cat}.grib2")
                        except Exception as e:
                                for k in range(0, 100, 1):
                                    print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                    print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                    _time.sleep(60)
                                    try:
                                        client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream='enfo',
                                            type=cat,
                                            levtype=level_type,
                                            param=params,
                                            levelist=levels,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-enfo-{cat}.grib2")
                                        break
                                    except Exception as e:
                                        k = k
                                        if k >= 99:
                                            print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                            _sys.exit(1)  
                                        else:
                                            pass                       
                    else:
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream='enfo',
                                            type=cat,
                                            levtype=level_type,
                                            param=params,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-enfo-{cat}.grib2")
                        except Exception as e:
                            for k in range(0, 100, 1):
                                    print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                    print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                    _time.sleep(60)
                                    try:
                                        client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream='enfo',
                                            type=cat,
                                            levtype=level_type,
                                            param=params,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-enfo-{cat}.grib2")
                                        break
                                    except Exception as e:
                                        k = k
                                        if k >= 99:
                                            print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                            _sys.exit(1)
                                        else:
                                            pass
                    if notifications == True:
                        print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-enfo-{cat}.grib2 saved to {path}", file=original_stdout)
                    else:
                        pass
                    
        else:        
            for i in range(0, final_forecast_hour + 6, 6):
                f = _io.StringIO()
                with _contextlib.redirect_stdout(f):
                    if level_type == 'pl':
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream='enfo',
                                            type=cat,
                                            levtype=level_type,
                                            param=params,
                                            levelist=levels,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-enfo-{cat}.grib2")
                        except Exception as e:
                                for k in range(0, 100, 1):
                                    print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                    print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                    _time.sleep(60)
                                    try:
                                        client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream='enfo',
                                            type=cat,
                                            levtype=level_type,
                                            param=params,
                                            levelist=levels,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-enfo-{cat}.grib2")
                                        break
                                    except Exception as e:
                                        k = k
                                        if k >= 99:
                                            print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                            _sys.exit(1)  
                                        else:
                                            pass                       
                    else:
                        try:
                            client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream='enfo',
                                            type=cat,
                                            levtype=level_type,
                                            param=params,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-enfo-{cat}.grib2")
                        except Exception as e:
                            for k in range(0, 100, 1):
                                    print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                                    print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                                    _time.sleep(60)
                                    try:
                                        client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream='enfo',
                                            type=cat,
                                            levtype=level_type,
                                            param=params,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-enfo-{cat}.grib2")
                                        break
                                    except Exception as e:
                                        k = k
                                        if k >= 99:
                                            print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                            _sys.exit(1)
                                        else:
                                            pass
                    if notifications == True:
                        print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-enfo-{cat}.grib2 saved to {path}", file=original_stdout)
                    else:
                        pass

        print(f"ECMWF AIFS ENSEMBLE {cat.upper()} Download Complete.")    
        
    else:
        print(f"ECMWF AIFS ENSEMBLE {cat.upper()} Data is up to date. Skipping download...")    
        
    if process_data == True:
        print(f"ECMWF AIFS ENSEMBLE {cat.upper()} Data Processing...")
        
        ds = _ecmwf_post_processing.ecmwf_aifs_post_processing(path,
                                                            western_bound, 
                                                            eastern_bound, 
                                                            northern_bound, 
                                                            southern_bound)
        
        _clear_idx_files_in_path(path)
            
        if convert_temperature == True:
            ds = _convert_temperature_units(ds, 
                                        convert_to)
                
        else:
            pass
        
        print(f"ECMWF AIFS ENSEMBLE {cat.upper()} Data Processing Complete.")
        return ds
    
    else:
        pass
    
def ecmwf_ifs_wave(final_forecast_hour=144,
                    western_bound=-180,
                    eastern_bound=180,
                    northern_bound=90,
                    southern_bound=-90,
                    step=3,
                    proxies=None,
                    process_data=True,
                    clear_recycle_bin=False,
                    custom_directory=None,
                    notifications='off',
                    source='ecmwf',
                    clear_data=False,
                    variables=['mean zero-crossing wave period',
                                'mean wave direction',
                                'mean wave period',
                                'peak wave period']):
    
    """
    This function scans for the latest ECMWF IFS dataset. If the dataset on the computer is old, the old data will be deleted
    and the new data will be downloaded. 
    
    1) final_forecast_hour (Integer) - Default = 360. The final forecast hour the user wishes to download. The ECMWF IFS
    goes out to 360 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    360 by the nereast increment of 3 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    7) proxies (String or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies="http://your-proxy-address:port"
    
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    9) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    10) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    11) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    12) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
    
    13) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    14) source (String) - The data server choice. Default='ecmwf'. When set to 'ecmwf' data is pulled from ecmwf-opendata.
        To switch to Amazon AWS, switch source='aws'. 
        
    15) 
    
    16) 
        
    Returns
    -------
    
    An xarray.data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys
    
    Plain Language ECMWF IFS Variable Keys (After Post-Processing)
    --------------------------------------------------------------
    
    'total_column_water'
    'total_column_vertically_integrated_water_vapor'
    'snow_albedo'
    'land_sea_mask'
    'specific_humidity'
    'volumetric_soil_moisture_content'
    'sea_ice_thickness'
    'soil_temperature'
    'surface_longwave_radiation_downward'
    'surface_net_shortwave_solar_radiation'
    'surface_net_longwave_thermal_radiation'
    'top_net_longwave_thermal_radiation'
    '10m_max_wind_gust'
    'vertical_velocity'
    'relative_vorticity'
    'relative_humidity'
    'geopotential_height'
    'eastward_turbulent_surface_stress'
    'u_wind_component'
    'divergence'
    'northward_turbulent_surface_stress'
    'v_wind_component'
    'air_temperature'
    'water_runoff'
    'total_precipitation'
    'mslp'
    'eastward_surface_sea_water_velocity'
    'most_unstable_cape'
    'northward_surface_sea_water_velocity'
    'sea_surface_height'
    'standard_deviation_of_sub_gridscale_orography'
    'skin_temperature'
    'slope_of_sub_gridscale_orography'
    '10m_u_wind_component'
    'precipitation_type'
    '10m_v_wind_component'
    'total_precipitation_rate'
    'surface_shortwave_radiation_downward'
    'geopotential'
    'surface_pressure'
    '2m_temperature'
    '100m_u_wind_component'
    '100m_v_wind_component'
    '2m_dew_point'
    '2m_relative_humidity'
    
    """
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    if proxies == None:
        pass
    else:
        _os.environ['http_proxy'] = proxies
        _os.environ['https_proxy'] = proxies
    
    if custom_directory == None:
        _build_directory('ifs', 
                        'wave')
        
        path = _ecmwf_branch_paths('ifs', 
                        'wave')
        
    else:
        path = _custom_branch(custom_directory)
        
    if clear_data == True:
        _clear_old_data(path)
    else:
        pass
    
    _clear_idx_files(path)
    
    url, filename, run = _ecmwf_ifs_wave_url_scanner(final_forecast_hour)
    
    
    stream = _get_stream('ifs-wave',
                         run)
    
    final_forecast_hour = _check_forecast_hour(stream,
                                                final_forecast_hour)
    valid_date = _parse_date(url,
                             'ifs-wave')
    
    params = _ifs_var_keys(variables)

    download = _local_file_scanner(path, 
                                  filename,
                                  'ecmwf',
                                  run)
    

    date = _parse_filename(filename)
    
    client = _Client(source=source,
                     model='ifs')
    if download == True:
        print(f"Downloading ECMWF IFS-WAVE...\n")
        print(f"By downloading data from the ECMWF open data dataset, you agree to the terms: Attribution 4.0 International (CC BY 4.0).\nPlease attribute ECMWF when downloading this data.")
        _clear_old_data(path)
        
        if final_forecast_hour <= 144:
            for i in range(0, final_forecast_hour + step, step):
                f = _io.StringIO()
                with _contextlib.redirect_stdout(f):
                    try:
                        client.retrieve(date=valid_date,
                                        time=run,
                                        step=i,
                                        stream=stream,
                                        type="fc",
                                        param=params,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                    except Exception as e:
                        for k in range(0, 100, 1):
                            print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                            print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                            _time.sleep(60)
                            try:
                                client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream=stream,
                                            type="fc",
                                            param=params,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                                break
                            except Exception as e:
                                k = k
                                if k >= 99:
                                    print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                    _sys.exit(1)
                                else:
                                    pass  
                if notifications == True:
                    print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2 saved to {path}", file=original_stdout)
                else:
                    pass                        
                                
        else:
            for i in range(0, 144 + step, step):
                f = _io.StringIO()
                with _contextlib.redirect_stdout(f):
                    try:
                        client.retrieve(date=valid_date,
                                        time=run,
                                        step=i,
                                        stream=stream,
                                        type="fc",
                                        param=params,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                    except Exception as e:
                        for k in range(0, 100, 1):
                            print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                            print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                            _time.sleep(60)
                            try:
                                client.retrieve(date=valid_date,
                                        time=run,
                                        step=i,
                                        stream=stream,
                                        type="fc",
                                        param=params,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                                break
                            except Exception as e:
                                k = k
                                if k >= 99:
                                    print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                    _sys.exit(1)
                                else:
                                    pass
                            
            for i in range(144, final_forecast_hour + 6, 6):
                f = _io.StringIO()
                with _contextlib.redirect_stdout(f):
                    try:
                        client.retrieve(date=valid_date,
                                        time=run,
                                        step=i,
                                        stream=stream,
                                        type="fc",
                                        param=params,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                    except Exception as e:
                        for k in range(0, 100, 1):
                            print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                            print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                            _time.sleep(60)
                            try:
                                client.retrieve(date=valid_date,
                                        time=run,
                                        step=i,
                                        stream=stream,
                                        type="fc",
                                        param=params,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                                break
                            except Exception as e:
                                k = k
                                if k >= 99:
                                    print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                    _sys.exit(1)   
                                else:
                                    pass                                            
                    if notifications == True:
                        print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2 saved to {path}", file=original_stdout)
                    else:
                        pass

        
        print(f"ECMWF IFS-WAVE Download Complete.")    
        
    else:
        print(f"ECMWF IFS-WAVE Data is up to date. Skipping download...")    
        
    if process_data == True:
        print(f"ECMWF IFS-WAVE Data Processing...")
        
        ds = _ecmwf_post_processing.ecmwf_ifs_wave_post_processing(path,
                                                            western_bound, 
                                                            eastern_bound, 
                                                            northern_bound, 
                                                            southern_bound)
        
        _clear_idx_files_in_path(path)
        
        print(f"ECMWF IFS-WAVE Data Processing Complete.")
        return ds
    
    else:
        pass
    
def ecmwf_ifs_wave_ens(final_forecast_hour=144,
                    western_bound=-180,
                    eastern_bound=180,
                    northern_bound=90,
                    southern_bound=-90,
                    step=3,
                    proxies=None,
                    process_data=True,
                    clear_recycle_bin=False,
                    custom_directory=None,
                    notifications='off',
                    source='ecmwf',
                    clear_data=False,
                    variables=['mean zero-crossing wave period',
                                'mean wave direction',
                                'mean wave period',
                                'peak wave period'],
                    members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                      31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
                      41, 42, 43, 44, 45, 46, 47, 48, 49, 50]):
    
    """
    This function scans for the latest ECMWF IFS dataset. If the dataset on the computer is old, the old data will be deleted
    and the new data will be downloaded. 
    
    1) final_forecast_hour (Integer) - Default = 360. The final forecast hour the user wishes to download. The ECMWF IFS
    goes out to 360 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    360 by the nereast increment of 3 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    7) proxies (String or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies="http://your-proxy-address:port"
    
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    9) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    10) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    11) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    12) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
    
    13) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    14) source (String) - The data server choice. Default='ecmwf'. When set to 'ecmwf' data is pulled from ecmwf-opendata.
        To switch to Amazon AWS, switch source='aws'. 
        
    15) 
    
    16) 
        
    Returns
    -------
    
    An xarray.data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys
    
    Plain Language ECMWF IFS Variable Keys (After Post-Processing)
    --------------------------------------------------------------
    
    'total_column_water'
    'total_column_vertically_integrated_water_vapor'
    'snow_albedo'
    'land_sea_mask'
    'specific_humidity'
    'volumetric_soil_moisture_content'
    'sea_ice_thickness'
    'soil_temperature'
    'surface_longwave_radiation_downward'
    'surface_net_shortwave_solar_radiation'
    'surface_net_longwave_thermal_radiation'
    'top_net_longwave_thermal_radiation'
    '10m_max_wind_gust'
    'vertical_velocity'
    'relative_vorticity'
    'relative_humidity'
    'geopotential_height'
    'eastward_turbulent_surface_stress'
    'u_wind_component'
    'divergence'
    'northward_turbulent_surface_stress'
    'v_wind_component'
    'air_temperature'
    'water_runoff'
    'total_precipitation'
    'mslp'
    'eastward_surface_sea_water_velocity'
    'most_unstable_cape'
    'northward_surface_sea_water_velocity'
    'sea_surface_height'
    'standard_deviation_of_sub_gridscale_orography'
    'skin_temperature'
    'slope_of_sub_gridscale_orography'
    '10m_u_wind_component'
    'precipitation_type'
    '10m_v_wind_component'
    'total_precipitation_rate'
    'surface_shortwave_radiation_downward'
    'geopotential'
    'surface_pressure'
    '2m_temperature'
    '100m_u_wind_component'
    '100m_v_wind_component'
    '2m_dew_point'
    '2m_relative_humidity'
    
    """
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    if proxies == None:
        pass
    else:
        _os.environ['http_proxy'] = proxies
        _os.environ['https_proxy'] = proxies
    
    if custom_directory == None:
        _build_directory('ifs', 
                        'wave ensemble')
        
        path = _ecmwf_branch_paths('ifs', 
                        'wave ensemble')
        
    else:
        path = _custom_branch(custom_directory)
        
    if clear_data == True:
        _clear_old_data(path)
    else:
        pass
    
    _clear_idx_files(path)
    
    url, filename, run = _ecmwf_ifs_wave_ens_url_scanner(final_forecast_hour)
    
    valid_date = _parse_date(url,
                             'ifs-wave')
    
    params = _ifs_var_keys(variables)

    download = _local_file_scanner(path, 
                                  filename,
                                  'ecmwf',
                                  run)
    

    date = _parse_filename(filename)
    
    client = _Client(source=source,
                     model='ifs')
    if download == True:
        print(f"Downloading ECMWF IFS-WAVE ENSEMBLE...\n")
        print(f"By downloading data from the ECMWF open data dataset, you agree to the terms: Attribution 4.0 International (CC BY 4.0).\nPlease attribute ECMWF when downloading this data.")
        _clear_old_data(path)
        
        if final_forecast_hour <= 144:
            for i in range(0, final_forecast_hour + step, step):
                f = _io.StringIO()
                with _contextlib.redirect_stdout(f):
                    try:
                        client.retrieve(date=valid_date,
                                        time=run,
                                        step=i,
                                        stream='waef',
                                        type="ef",
                                        param=params,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-waef-ef.grib2")
                    except Exception as e:
                        for k in range(0, 100, 1):
                            print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                            print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                            _time.sleep(60)
                            try:
                                client.retrieve(date=valid_date,
                                            time=run,
                                            step=i,
                                            stream='waef',
                                            type="ef",
                                            param=params,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-waef-ef.grib2")
                                break
                            except Exception as e:
                                k = k
                                if k >= 99:
                                    print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                    _sys.exit(1)
                                else:
                                    pass    
                                
                    if notifications == 'on':
                        print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-waef-fc.grib2 saved to {path}", file=original_stdout)
                    else:
                        pass                      
                                
        else:
            for i in range(0, 144 + step, step):
                f = _io.StringIO()
                with _contextlib.redirect_stdout(f):
                    try:
                        client.retrieve(date=valid_date,
                                        time=run,
                                        step=i,
                                        stream='waef',
                                        type="ef",
                                        param=params,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-waef-ef.grib2")
                    except Exception as e:
                        for k in range(0, 100, 1):
                            print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                            print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                            _time.sleep(60)
                            try:
                                client.retrieve(date=valid_date,
                                        time=run,
                                        step=i,
                                        stream='waef',
                                        type="ef",
                                        param=params,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-waef-ef.grib2")
                                break
                            except Exception as e:
                                k = k
                                if k >= 99:
                                    print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                    _sys.exit(1)
                                else:
                                    pass
                            
            for i in range(144, final_forecast_hour + 6, 6):
                f = _io.StringIO()
                with _contextlib.redirect_stdout(f):
                    try:
                        client.retrieve(date=valid_date,
                                        time=run,
                                        step=i,
                                        stream='waef',
                                        type="ef",
                                        param=params,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-waef-ef.grib2")
                    except Exception as e:
                        for k in range(0, 100, 1):
                            print(f"Server Connection Unstable - Waiting 60 seconds and retrying", file=original_stdout)
                            print(f"Remaining Attempts: {100 - k}", file=original_stdout)
                            _time.sleep(60)
                            try:
                                client.retrieve(date=valid_date,
                                        time=run,
                                        step=i,
                                        stream='waef',
                                        type="ef",
                                        param=params,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-waef-ef.grib2")
                                break
                            except Exception as e:
                                k = k
                                if k >= 99:
                                    print(f"Cannot re-establish connection - System Exiting.", file=original_stdout)
                                    _sys.exit(1)   
                                else:
                                    pass                                            
                    if notifications == 'on':
                        print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-waef-fc.grib2 saved to {path}", file=original_stdout)
                    else:
                        pass

        
        print(f"ECMWF IFS-WAVE ENSEMBLE Download Complete.")    
        
    else:
        print(f"ECMWF IFS-WAVE ENSEMBLE Data is up to date. Skipping download...")    
        
    if process_data == True:
        print(f"ECMWF IFS-WAVE ENSEMBLE Data Processing...")
        
        ds = _ecmwf_post_processing.ecmwf_ifs_wave_post_processing(path,
                                                            western_bound, 
                                                            eastern_bound, 
                                                            northern_bound, 
                                                            southern_bound)
        
        _clear_idx_files_in_path(path)
        
        print(f"ECMWF IFS-WAVE Data Processing Complete.")
        return ds
    
    else:
        pass