"""
This file hosts the client that retrieves archived ECMWF IFS data from Amazon Web Services (AWS) or Google Cloud data archives. 

(C) Eric J. Drewitz 2025-2026
"""

import os as _os
import contextlib as _contextlib
import io as _io
import warnings as _warnings
_warnings.filterwarnings('ignore')
import time as _time
import sys as _sys
import wxdata.post_processors.ecmwf_post_processing as _ecmwf_post_processing

from datetime import datetime as _datetime
from wxdata.calc.unit_conversion import convert_temperature_units as _convert_temperature_units
from wxdata.utils.transforms import grib_to_netcdf as _grib_to_netcdf
from ecmwf.opendata import Client as _Client
from wxdata.model_data.ecmwf.keys import(
    get_levels as _get_levels,
    ifs_var_keys as _ifs_var_keys,
)

from wxdata.utils.warnings import eccodes_warning as _eccodes_warning

from wxdata.utils.file_funcs import clear_idx_files_in_path as _clear_idx_files_in_path
from wxdata.utils.recycle_bin import(
        clear_recycle_bin_windows as _clear_recycle_bin_windows,
        clear_trash_bin_mac as _clear_trash_bin_mac,
        clear_trash_bin_linux as _clear_trash_bin_linux
)

_eccodes_warning()

now = _datetime.now()
original_stdout = _sys.stdout

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

def _ecmwf_ifs_ens_client(date,
                      run,
                      final_forecast_hour=144,
              western_bound=-180,
              eastern_bound=180,
              northern_bound=90,
              southern_bound=-90,
              step=3,
              path=f"ECMWF IFS/Archive",
              proxies=None,
              process_data=True,
              clear_recycle_bin=False,
              convert_temperature=True,
              convert_to='celsius',
              notifications='off',
              source='aws',
              level_type='surface',
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
    
    These ECMWF end-to-end clients can download ECMWF data from the following sources: 
    
            1) ECMWF Open-Data Server
            2) Amazon AWS Server
            3) Google Cloud Server
            
    ***If the server of your choice is down, the client will rotate to another one and try scanning for data and downloading there.***
    ***If the client cannot connect to any of the servers, the system will exit.***
    
    1) final_forecast_hour (Integer) - Default = 144.

        00z and 12z ECMWF IFS Runs
        --------------------------
        
        3-Hourly Increments from hour 0 to hour 144.
        6-Hourly Increments from hour 144 to hour 360
        
        06z and 18z ECMWF IFS Runs
        --------------------------
        
        3-Hourly Increments from hour 0 to hour 144. 
    
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
        
    12) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS files will be saved to. 
        When set to None, the path will be: "ECMWF/IFS/OPERATIONAL/"
    
    13) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    14) source (String) - Default='ecmwf'. The data server choice. 
    
        Data Sources
        ------------
        
        - ECMWF Open-Data Server = 'ecmwf'
        - Amazon AWS Server = 'aws'
        - Google Cloud Server = 'google'
    
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
        
    if type(date) != type(now):
        date = f"{date[0:4]}{date[5:7]}{date[8:10]}:{run}"
        date = _datetime.strptime(date, "%Y%m%d:%H")
    else:
        date = date
    
    if run == 18 or run == '18':
        run = '18'
    elif run == 12 or run == '12':
        run = '12'
    elif run == 6 or run == '06':
        run = '06'
    else:
        run = '00'
        
    stream = 'enfo'
        
    path = f"{path}/{date.strftime('%Y%m%d')}/{run}"
    
    _os.makedirs(path, exist_ok=True)
    
    try:
        for file in _os.listdir(path):
            _os.remove(f"{path}/{file}")
    except Exception as e:
        pass

    
    source = source.lower()
    
    if source == 'aws':
        source = 'aws'
    else:
        source = 'google'
    
    levels = _get_levels(levels)
    level_type = _get_level_type(level_type)
    params = _ifs_var_keys(variables)
    
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
    
    client = _Client(source, beta=False)

    if final_forecast_hour <= 144:
        for i in range(0, final_forecast_hour + step, step):
            f = _io.StringIO()
            with _contextlib.redirect_stdout(f):
                if level_type == 'pl':
                    try:
                        client.retrieve(date=date,
                                        time=int(run),
                                        step=i,
                                        stream=stream,
                                        type="ef",
                                        model='ifs',
                                        levtype=level_type,
                                        param=params,
                                        levelist=levels,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                        success = True
                    except Exception as e:
                        for k in range(0, 3, 1):
                            print(f"Server Connection Unstable - Retrying.", file=original_stdout)
                            print(f"Remaining Attempts: {3 - k}", file=original_stdout)
                            _time.sleep(3)
                            try:
                                client.retrieve(date=date,
                                            time=int(run),
                                            step=i,
                                            stream=stream,
                                            model='ifs',
                                            type="ef",
                                            levtype=level_type,
                                            param=params,
                                            levelist=levels,
                                            number=members,
                                            target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                                success = True
                                break
                            except Exception as e:
                                k = k
                                if k >= 2:
                                    success = False
                                    pass
    
                else:
                    try:
                        client.retrieve(date=date,
                                        time=int(run),
                                        step=i,
                                        stream=stream,
                                        model='ifs',
                                        type="ef",
                                        levtype=level_type,
                                        param=params,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                        success = True
                    except Exception as e:
                        for k in range(0, 3, 1):
                            print(f"Server Connection Unstable - Retrying.", file=original_stdout)
                            print(f"Remaining Attempts: {3 - k}", file=original_stdout)
                            _time.sleep(3)
                            try:
                                client.retrieve(date=date,
                                        time=int(run),
                                        step=i,
                                        stream=stream,
                                        model='ifs',
                                        type="ef",
                                        levtype=level_type,
                                        param=params,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                                success = True
                                break
                            except Exception as e:
                                k = k
                                if k >= 2:
                                    success = False
                                    pass
                        
            if success == True:
                if notifications == True:
                    print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2 saved to {path}", file=original_stdout)
                else:
                    pass
            else:
                break
    else:
        for i in range(0, 144 + step, step):
            f = _io.StringIO()
            with _contextlib.redirect_stdout(f):
                if level_type == 'pl':
                    try:
                        client.retrieve(date=date,
                                        time=int(run),
                                        step=i,
                                        stream=stream,
                                        model='ifs',
                                        type="ef",
                                        levtype=level_type,
                                        param=params,
                                        levelist=levels,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                        success = False
                    except Exception as e:
                        for k in range(0, 3, 1):
                            print(f"Server Connection Unstable - Retrying.", file=original_stdout)
                            print(f"Remaining Attempts: {3 - k}", file=original_stdout)
                            _time.sleep(3)
                            try:
                                client.retrieve(date=date,
                                        time=int(run),
                                        step=i,
                                        stream=stream,
                                        model='ifs',
                                        type="ef",
                                        levtype=level_type,
                                        param=params,
                                        levelist=levels,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                                success = False
                                break
                            except Exception as e:
                                k = k
                                if k >= 2:
                                    success = False
                                    break
                                    
                else:
                    try:
                        client.retrieve(date=date,
                                        time=int(run),
                                        step=i,
                                        stream=stream,
                                        model='ifs',
                                        type="ef",
                                        levtype=level_type,
                                        param=params,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                        success = True
                    except Exception as e:
                        for k in range(0, 3, 1):
                            print(f"Server Connection Unstable - Retrying.", file=original_stdout)
                            print(f"Remaining Attempts: {3 - k}", file=original_stdout)
                            _time.sleep(3)
                            try:
                                client.retrieve(date=date,
                                        time=int(run),
                                        step=i,
                                        stream=stream,
                                        model='ifs',
                                        type="ef",
                                        levtype=level_type,
                                        param=params,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                                success = True
                                break
                            except Exception as e:
                                k = k
                                if k >= 2:
                                    success = False
                                    break
            if success == True:                              
                if notifications == True:
                    print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2 saved to {path}", file=original_stdout)
                else:
                    pass
            else:
                break
                            
        for i in range(144, final_forecast_hour + 6, 6):
            f = _io.StringIO()
            with _contextlib.redirect_stdout(f):
                if level_type == 'pl':
                    try:
                        client.retrieve(date=date,
                                        time=int(run),
                                        step=i,
                                        stream=stream,
                                        model='ifs',
                                        type="ef",
                                        levtype=level_type,
                                        param=params,
                                        levelist=levels,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                        success = True
                    except Exception as e:
                        for k in range(0, 3, 1):
                            print(f"Server Connection Unstable - Retrying.", file=original_stdout)
                            print(f"Remaining Attempts: {3 - k}", file=original_stdout)
                            _time.sleep(3)
                            try:
                                client.retrieve(date=date,
                                        time=int(run),
                                        step=i,
                                        stream=stream,
                                        model='ifs',
                                        type="ef",
                                        levtype=level_type,
                                        param=params,
                                        levelist=levels,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                                success = True
                                break
                            except Exception as e:
                                k = k
                                if k >= 2:
                                    success = False
                                    break                       
                else:
                    try:
                        client.retrieve(date=date,
                                        time=int(run),
                                        step=i,
                                        stream=stream,
                                        model='ifs',
                                        type="ef",
                                        levtype=level_type,
                                        param=params,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                        success = True
                    except Exception as e:
                        for k in range(0, 3, 1):
                            print(f"Server Connection Unstable - Retrying.", file=original_stdout)
                            print(f"Remaining Attempts: {3 - k}", file=original_stdout)
                            _time.sleep(3)
                            try:
                                client.retrieve(date=date,
                                        time=int(run),
                                        step=i,
                                        stream=stream,
                                        model='ifs',
                                        type="ef",
                                        levtype=level_type,
                                        param=params,
                                        number=members,
                                        target=f"{path}/{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2")
                                success = True
                                break
                            except Exception as e:
                                k = k
                                if k >= 2:
                                    success = False
                                    break
            
            if success == True:                       
                if notifications == True:
                    print(f"{date.strftime('%Y%m%d%H')}0000-{i}h-{stream}-fc.grib2 saved to {path}", file=original_stdout)
                else:
                    pass
            else:
                break

    if success == True:
        print(f"ECMWF IFS Download Complete.")   
    else:
        pass 
        

    if process_data == True:
        if success == True:
            print(f"ECMWF IFS Data Processing...")
        else:
            pass
        
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
    
    
def ecmwf_ifs_ens(
    date,
    run,
    final_forecast_hour=144,
    western_bound=-180,
    eastern_bound=180,
    northern_bound=90,
    southern_bound=-90,
    step=3,
    path=f"ECMWF IFS ENSEMBLE/Archive",
    proxies=None,
    process_data=True,
    clear_recycle_bin=False,
    convert_temperature=True,
    convert_to='celsius',
    notifications='off',
    source='aws',
    level_type='surface',
    variables=['geopotential height',
                'specific humidity',
                'relative humidity',
                'temperature',
                'u-wind component',
                'v-wind component'],
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
                          41, 42, 43, 44, 45, 46, 47, 48, 49, 50],        
    to_netcdf=False,
    netcdf_path=f"ECMWF IFS ENSEMBLE/Archive/NETCDF",
    netcdf_filename=f"ecmwf_ifs.nc",
    delete_previous_netcdf_file=True,
    return_values=True                  
    ):
    
    """
    This client downloads archived ECMWF IFS data requested by the user. 
    
    These ECMWF end-to-end clients can download ECMWF data from the following sources: 
    
            1) Amazon AWS Server
            2) Google Cloud Server
            
    ***If the server of your choice is down, the client will rotate to another one and try scanning for data and downloading there.***
    ***If the client cannot connect to any of the servers, the system will exit.***
    
    Required Arguments:
    
    1) date (String) - The date the user requests. 
    
    ***Important Note***: Data archive begins in the spring of 2024. 
    
    2) run (Integer) - The model runtime (0, 6, 12, 18) UTC.
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default = 144.

        00z and 12z ECMWF IFS Runs
        --------------------------
        
        3-Hourly Increments from hour 0 to hour 144.
        6-Hourly Increments from hour 144 to hour 360
        
        06z and 18z ECMWF IFS Runs
        --------------------------
        
        3-Hourly Increments from hour 0 to hour 144. 
    
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
        
    12) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS files will be saved to. 
        When set to None, the path will be: "ECMWF/IFS/OPERATIONAL/"
    
    13) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    14) source (String) - Default='aws'. The data server choice. 
    
        Data Sources
        ------------
        
        - Amazon AWS Server = 'aws'
        - Google Cloud Server = 'google'
    
    15) level_type (String) - Default='surface'. The level of the parameters being queried. 
    
        level_types
        -----------
        
        1) 'surface'
        2) 'pressure'
        3) 'soil
    
    16) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
        
    17) variables (String List) - Default=['geopotential height',
                                            'specific humidity',
                                            'relative humidity',
                                            'temperature',
                                            'u-wind component',
                                            'v-wind component'] 
                
        The list of variable names in plain-language. 
    
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
        
    19) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.
    
    20) netcdf_path (String) - Default='ECMWF IFS/Archive/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.
    
    21) netcdf_filename (String) - Default='ecmwf_ifs.nc'. The name of the netCDF (.nc) file. A good practice is to 
        name this netCDF file using the variable name. 
        
    22) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
        new netCDF file. For users who want to archive all data set this to False. 
        
    23) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned.
        
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
    
    source = source.lower()

    
    try:
        if process_data == True:
            ds = _ecmwf_ifs_ens_client(
                date,
                run,
                final_forecast_hour=final_forecast_hour,
              western_bound=western_bound,
              eastern_bound=eastern_bound,
              northern_bound=northern_bound,
              southern_bound=southern_bound,
              step=step,
              path=path,
              proxies=proxies,
              process_data=process_data,
              clear_recycle_bin=clear_recycle_bin,
              convert_temperature=convert_temperature,
              convert_to=convert_to,
              notifications=notifications,
              source=source,
              level_type=level_type,
              variables=variables,
              levels=levels,
              members=members
            )
        else:
            _ecmwf_ifs_ens_client(
                date,
                run,
                final_forecast_hour=final_forecast_hour,
              western_bound=western_bound,
              eastern_bound=eastern_bound,
              northern_bound=northern_bound,
              southern_bound=southern_bound,
              step=step,
              path=path,
              proxies=proxies,
              process_data=process_data,
              clear_recycle_bin=clear_recycle_bin,
              convert_temperature=convert_temperature,
              convert_to=convert_to,
              notifications=notifications,
              source=source,
              level_type=level_type,
              variables=variables,
              levels=levels,
              members=members
            )
            
    except Exception as e:
        print(f"Error: Client lost connection to {source.upper()} server.")
        if source == 'aws':
            print(f"Rotating to Google Cloud.")
            try:
                if process_data == True:
                    ds = _ecmwf_ifs_ens_client(
                        date,
                        run,
                        final_forecast_hour=final_forecast_hour,
                    western_bound=western_bound,
                    eastern_bound=eastern_bound,
                    northern_bound=northern_bound,
                    southern_bound=southern_bound,
                    step=step,
                    path=path,
                    proxies=proxies,
                    process_data=process_data,
                    clear_recycle_bin=clear_recycle_bin,
                    convert_temperature=convert_temperature,
                    convert_to=convert_to,
                    notifications=notifications,
                    source='google',
                    level_type=level_type,
                    variables=variables,
                    levels=levels,
                    members=members
                    )
                else:
                    _ecmwf_ifs_ens_client(
                        date,
                        run,
                        final_forecast_hour=final_forecast_hour,
                    western_bound=western_bound,
                    eastern_bound=eastern_bound,
                    northern_bound=northern_bound,
                    southern_bound=southern_bound,
                    step=step,
                    path=path,
                    proxies=proxies,
                    process_data=process_data,
                    clear_recycle_bin=clear_recycle_bin,
                    convert_temperature=convert_temperature,
                    convert_to=convert_to,
                    notifications=notifications,
                    source='google',
                    level_type=level_type,
                    variables=variables,
                    levels=levels,
                    members=members
                    )
            except Exception as e:
                print(f"Error: Client unable to connect to either server.")
                print(f"Try double checking for typos in the date or run.")
                print("System Exit.")
                _sys.exit(1)
                
        else:
            print(f"Rotating to AWS.")
            try:
                if process_data == True:
                    ds = _ecmwf_ifs_ens_client(
                        date,
                        run,
                        final_forecast_hour=final_forecast_hour,
                    western_bound=western_bound,
                    eastern_bound=eastern_bound,
                    northern_bound=northern_bound,
                    southern_bound=southern_bound,
                    step=step,
                    path=path,
                    proxies=proxies,
                    process_data=process_data,
                    clear_recycle_bin=clear_recycle_bin,
                    convert_temperature=convert_temperature,
                    convert_to=convert_to,
                    notifications=notifications,
                    source='aws',
                    level_type=level_type,
                    variables=variables,
                    levels=levels,
                    members=members
                    )
                else:
                    _ecmwf_ifs_ens_client(
                        date,
                        run,
                        final_forecast_hour=final_forecast_hour,
                    western_bound=western_bound,
                    eastern_bound=eastern_bound,
                    northern_bound=northern_bound,
                    southern_bound=southern_bound,
                    step=step,
                    path=path,
                    proxies=proxies,
                    process_data=process_data,
                    clear_recycle_bin=clear_recycle_bin,
                    convert_temperature=convert_temperature,
                    convert_to=convert_to,
                    notifications=notifications,
                    source='aws',
                    level_type=level_type,
                    variables=variables,
                    levels=levels,
                    members=members
                    )
            except Exception as e:
                print(f"Error: Client unable to connect to either server.")
                print(f"Try double checking for typos in the date or run.")
                print("System Exit.")
                _sys.exit(1)
                
    if process_data == True:
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
                
            