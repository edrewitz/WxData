"""
This file hosts functions that download various types of GEFS Data.

1) gefs_0p50
2) gefs_0p50_secondary_parameters
3) gefs_0p25

(C) Eric J. Drewitz 2025-2026
"""
import os as _os
import sys as _sys
import warnings as _warnings
import wxdata.post_processors.gefs_post_processing as _gefs_post_processing
_warnings.filterwarnings('ignore')

from wxdata.client.client import byte_range_request
from wxdata.archived_data.model_data.noaa.gefs.url_scanner import(
    gefs_0p50_url_scanner as _gefs_0p50_url_scanner,
    gefs_0p50_secondary_parameters_url_scanner as _gefs_0p50_secondary_parameters_url_scanner,
    gefs_0p25_url_scanner as _gefs_0p25_url_scanner
)

from wxdata.utils.warnings import(
    eccodes_warning as _eccodes_warning,
    version_warning as _version_warning
)
from wxdata.calc.unit_conversion import convert_temperature_units as _convert_temperature_units
from wxdata.utils.recycle_bin import(
    clear_recycle_bin_windows as _clear_recycle_bin_windows,
    clear_trash_bin_mac as _clear_trash_bin_mac,
    clear_trash_bin_linux as _clear_trash_bin_linux
)

_eccodes_warning()

def _gefs_0p50_client(date,
            run,
            cat='mean', 
            path=f'GEFS0P50/Archive',
             final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=False,
             variables=['geopotential height'],
            convert_temperature=True,
            convert_to='celsius',
            chunk_size=8192,
            notifications='off',
            source='aws',
            level_type='pressure',
            levels=[1000,
                    925,
                    850,
                    700,
                    500,
                    400,
                    300,
                    250,
                    200,
                    100,
                    50,
                    10]):
    
    """
    This function downloads the latest GEFS0P50 data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='mean'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    7) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    9) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    12) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50
        -------------------------------
        
			'total precipitation'
            'convective available potential energy'
            'categorical freezing rain'
            'categorical ice pellets'
            'categorical rain'
            'categorical snow'
            'convective inhibition'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'geopotential height'
            'ice thickness'
            'latent heat net flux'
            'pressure'
            'mean sea level pressure'
            'precipitable water'
            'relative humidity'
            'sensible heat net flux'
            'snow depth'
            'volumetric soil moisture content'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'soil temperature'
            'u-component of wind'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'v-component of wind'
            'vertical velocity'
            'water equivalent of accumulated snow depth'
            
    13) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.
    
    14) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    15) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    16) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    17) custom_directory (String or None) - Default=None. The directory path where the GEFS0P50 files will be saved to.
        
    18) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    19) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    20) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
        
    21) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    22) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'height above ground'
        'surface'
        'height below ground'
        'entire atmosphere (considered as a single layer)'
        'pressure above ground'
        
    23) levels (String, Integer or Float List) - Default=[1000,
                                                            925,
                                                            850,
                                                            700,
                                                            500,
                                                            400,
                                                            300,
                                                            250,
                                                            200,
                                                            100,
                                                            50,
                                                            10]    
                                                            
        The pressure, height or depth levels. 
    
    Returns
    -------
    
    An xarray data array of the GEFS0P50 data specified to the coordinate boundaries and variable list the user specifies. 
    
    GEFS0P50 files are saved to f:GEFS0P50/{cat} or in the case of ensemble members f:GEFS0P50/{cat}/{member}
    
    Variables
    ---------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'convective_available_potential_energy'
    'convective_inhibition'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'u_wind_component'
    'v_wind_component'
    
    """
    
    if run == 18 or run == '18':
        run = '18'
    elif run == 12 or run == '12':
        run = '12'
    elif run == 6 or run == '06':
        run = '06'
    else:
        run = '00'
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass    
    
    
    cat = cat.lower()
        
    try:
        url, date = _gefs_0p50_url_scanner(date,
                                        run,
                                        cat, 
                                        final_forecast_hour,
                                        proxies, 
                                        members,
                                        source)
    except Exception as e:
        print(f"Error: Client unable to connect to {source.upper()} Server.")
        if source == 'aws':
            print(f"Rotating to Google Cloud.")
            try:
                url, date = _gefs_0p50_url_scanner(date,
                                                run,
                                                cat, 
                                                final_forecast_hour,
                                                proxies, 
                                                members,
                                                'google')
            except Exception as e:
                print(f"Error: Client unable to establish a connection to either server. - System Exit.")
                _sys.exit(1)
        else:
            print(f"Rotating to AWS.")
            try:
                url, date = _gefs_0p50_url_scanner(date,
                                                run,
                                                cat, 
                                                final_forecast_hour,
                                                proxies, 
                                                members,
                                                'aws')
            except Exception as e:
                print(f"Error: Client unable to establish a connection to either server. - System Exit.")
                _sys.exit(1)

    if cat != 'members':
        if cat == 'mean':
            aa = 'avg'
        elif cat == 'control':
            aa = 'c00'
        else:
            aa = 'spr'
                        
        path = f"{path}/{date.strftime('%Y%m%d')}/{run}/{cat.upper()}"
        paths = [path]
        for path in paths:
            try:
                for file in _os.listdir(f"{path}"):
                    _os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            for i in range(0, final_forecast_hour + step, step):
                if i < 10:
                    byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f00{i}",
                                                f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f00{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{aa}.t{run}z.pgrb2a.0p50.f00{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin) 
                    
                elif i >= 10 and i < (99 + step):
                    byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f0{i}",
                                                f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f0{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{aa}.t{run}z.pgrb2a.0p50.f0{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin)   
                    
                elif i >= 102 and i < (240 + step):
                    byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f{i}",
                                                f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{aa}.t{run}z.pgrb2a.0p50.f{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin)    
                    
                else:
                    cont = True
                    break
                
            if cont == True:
                for i in range(240, final_forecast_hour + 6, 6):
                    byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f{i}",
                                                f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{aa}.t{run}z.pgrb2a.0p50.f{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin) 
            else:
                pass                                                                
                            
    else:
        aa = []
        for member in members:
            if member < 10:
                m = f"p0{member}"
            else:
                m = f"p{member}"
            aa.append(m)
        
        paths = []
        for member in members:
            fpath = f"{path}/{date.strftime('%Y%m%d')}/{run}/{cat.upper()}/{member}" 
            paths.append(fpath)   
        
        for path, a in zip(paths, aa):
            try:
                for file in _os.listdir(f"{path}"):
                    _os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            for i in range(0, final_forecast_hour + step, step):
                if i < 10:
                    byte_range_request(f"{url}ge{a}.t{run}z.pgrb2a.0p50.f00{i}",
                                                f"{url}ge{a}.t{run}z.pgrb2a.0p50.f00{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{a}.t{run}z.pgrb2a.0p50.f00{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin) 
                    
                elif i >= 10 and i < (99 + step):
                    byte_range_request(f"{url}ge{a}.t{run}z.pgrb2a.0p50.f0{i}",
                                                f"{url}ge{a}.t{run}z.pgrb2a.0p50.f0{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{a}.t{run}z.pgrb2a.0p50.f0{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin)   
                    
                elif i >= 102 and i < (240 + step):
                    byte_range_request(f"{url}ge{a}.t{run}z.pgrb2a.0p50.f{i}",
                                                f"{url}ge{a}.t{run}z.pgrb2a.0p50.f{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{a}.t{run}z.pgrb2a.0p50.f{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin)    
                    
                else:
                    cont = True
                    break
                
            if cont == True:
                for i in range(240, final_forecast_hour + 6, 6):
                    byte_range_request(f"{url}ge{a}.t{run}z.pgrb2a.0p50.f{i}",
                                                f"{url}ge{a}.t{run}z.pgrb2a.0p50.f{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{a}.t{run}z.pgrb2a.0p50.f{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin) 
            else:
                pass  
                        
        print(f"GEFS0P50 {cat.upper()} Download Complete.")        
        
    if process_data == True:
        print(f"GEFS0P50 {cat.upper()} Data Processing...")
        
        ds = _gefs_post_processing.primary_gefs_post_processing(paths,
                                                                western_bound,
                                                                eastern_bound,
                                                                southern_bound,
                                                                northern_bound)
            
        if convert_temperature == True:
            ds = _convert_temperature_units(ds, 
                                            convert_to,
                                            cat=cat)
                
        else:
            pass
            
        print(f"GEFS0P50 {cat.upper()} Data Processing Complete.")
        return ds
    else:
        pass

def _gefs_0p50_secondary_parameters_client(date,
            run,
            cat='mean', 
            path=f'GEFS0P50 SECONDARY PARAMETERS/Archive',
             final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=False,
             variables=['temperature'],
            convert_temperature=True,
            convert_to='celsius',
            chunk_size=8192,
            notifications='off',
            source='aws',
            level_type='pressure',
            levels=[750]):
    
    """
    This function downloads the latest GEFS0P50 data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='mean'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    7) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    9) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    12) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50
        -------------------------------
        
			'total precipitation'
            'convective available potential energy'
            'categorical freezing rain'
            'categorical ice pellets'
            'categorical rain'
            'categorical snow'
            'convective inhibition'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'geopotential height'
            'ice thickness'
            'latent heat net flux'
            'pressure'
            'mean sea level pressure'
            'precipitable water'
            'relative humidity'
            'sensible heat net flux'
            'snow depth'
            'volumetric soil moisture content'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'soil temperature'
            'u-component of wind'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'v-component of wind'
            'vertical velocity'
            'water equivalent of accumulated snow depth'
            
    13) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.
    
    14) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    15) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    16) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    17) custom_directory (String or None) - Default=None. The directory path where the GEFS0P50 files will be saved to.
        
    18) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    19) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    20) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
        
    21) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    22) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'height above ground'
        'surface'
        'height below ground'
        'entire atmosphere (considered as a single layer)'
        'pressure above ground'
        
    23) levels (String, Integer or Float List) - Default=[1000,
                                                            925,
                                                            850,
                                                            700,
                                                            500,
                                                            400,
                                                            300,
                                                            250,
                                                            200,
                                                            100,
                                                            50,
                                                            10]    
                                                            
        The pressure, height or depth levels. 
    
    Returns
    -------
    
    An xarray data array of the GEFS0P50 data specified to the coordinate boundaries and variable list the user specifies. 
    
    GEFS0P50 files are saved to f:GEFS0P50/{cat} or in the case of ensemble members f:GEFS0P50/{cat}/{member}
    
    Variables
    ---------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'convective_available_potential_energy'
    'convective_inhibition'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'u_wind_component'
    'v_wind_component'
    
    """
    
    if run == 18 or run == '18':
        run = '18'
    elif run == 12 or run == '12':
        run = '12'
    elif run == 6 or run == '06':
        run = '06'
    else:
        run = '00'
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass    
    
    
    cat = cat.lower()
        
    try:
        url, date = _gefs_0p50_secondary_parameters_url_scanner(date,
                                        run,
                                        cat, 
                                        final_forecast_hour,
                                        proxies, 
                                        members,
                                        source)
    except Exception as e:
        print(f"Error: Client unable to connect to {source.upper()} Server.")
        if source == 'aws':
            print(f"Rotating to Google Cloud.")
            try:
                url, date = _gefs_0p50_secondary_parameters_url_scanner(date,
                                                run,
                                                cat, 
                                                final_forecast_hour,
                                                proxies, 
                                                members,
                                                'google')
            except Exception as e:
                print(f"Error: Client unable to establish a connection to either server. - System Exit.")
                _sys.exit(1)
        else:
            print(f"Rotating to AWS.")
            try:
                url, date = _gefs_0p50_secondary_parameters_url_scanner(date,
                                                run,
                                                cat, 
                                                final_forecast_hour,
                                                proxies, 
                                                members,
                                                'aws')
            except Exception as e:
                print(f"Error: Client unable to establish a connection to either server. - System Exit.")
                _sys.exit(1)

    if cat != 'members':
        if cat == 'mean':
            aa = 'avg'
        elif cat == 'control':
            aa = 'c00'
        else:
            aa = 'spr'
                        
        path = f"{path}/{date.strftime('%Y%m%d')}/{run}/{cat.upper()}"
        paths = [path]
        for path in paths:
            try:
                for file in _os.listdir(f"{path}"):
                    _os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            for i in range(0, final_forecast_hour + step, step):
                if i < 10:
                    byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f00{i}",
                                                f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f00{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{aa}.t{run}z.pgrb2b.0p50.f00{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin) 
                    
                elif i >= 10 and i < (99 + step):
                    byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f0{i}",
                                                f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f0{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{aa}.t{run}z.pgrb2b.0p50.f0{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin)   
                    
                elif i >= 102 and i < (240 + step):
                    byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f{i}",
                                                f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{aa}.t{run}z.pgrb2b.0p50.f{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin)    
                    
                else:
                    cont = True
                    break
                
            if cont == True:
                for i in range(240, final_forecast_hour + 6, 6):
                    byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f{i}",
                                                f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{aa}.t{run}z.pgrb2b.0p50.f{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin) 
            else:
                pass                                                                
                            
    else:
        aa = []
        for member in members:
            if member < 10:
                m = f"p0{member}"
            else:
                m = f"p{member}"
            aa.append(m)
        
        paths = []
        for member in members:
            fpath = f"{path}/{date.strftime('%Y%m%d')}/{run}/{cat.upper()}/{member}" 
            paths.append(fpath)   
        
        for path, a in zip(paths, aa):
            try:
                for file in _os.listdir(f"{path}"):
                    _os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            for i in range(0, final_forecast_hour + step, step):
                if i < 10:
                    byte_range_request(f"{url}ge{a}.t{run}z.pgrb2b.0p50.f00{i}",
                                                f"{url}ge{a}.t{run}z.pgrb2b.0p50.f00{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{a}.t{run}z.pgrb2b.0p50.f00{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin) 
                    
                elif i >= 10 and i < (99 + step):
                    byte_range_request(f"{url}ge{a}.t{run}z.pgrb2b.0p50.f0{i}",
                                                f"{url}ge{a}.t{run}z.pgrb2b.0p50.f0{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{a}.t{run}z.pgrb2b.0p50.f0{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin)   
                    
                elif i >= 102 and i < (240 + step):
                    byte_range_request(f"{url}ge{a}.t{run}z.pgrb2b.0p50.f{i}",
                                                f"{url}ge{a}.t{run}z.pgrb2b.0p50.f{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{a}.t{run}z.pgrb2b.0p50.f{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin)    
                    
                else:
                    cont = True
                    break
                
            if cont == True:
                for i in range(240, final_forecast_hour + 6, 6):
                    byte_range_request(f"{url}ge{a}.t{run}z.pgrb2b.0p50.f{i}",
                                                f"{url}ge{a}.t{run}z.pgrb2b.0p50.f{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{a}.t{run}z.pgrb2a.0p50.f{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin) 
            else:
                pass  
                        
        print(f"GEFS0P50 SECONDARY PARAMETERS {cat.upper()} Download Complete.")        
        
    if process_data == True:
        print(f"GEFS0P50 SECONDARY PARAMETERS {cat.upper()} Data Processing...")
        
        ds = _gefs_post_processing.secondary_gefs_post_processing(paths,
                                                                western_bound,
                                                                eastern_bound,
                                                                southern_bound,
                                                                northern_bound)
            
        if convert_temperature == True:
            ds = _convert_temperature_units(ds, 
                                            convert_to,
                                            cat=cat)
                
        else:
            pass
            
        print(f"GEFS0P50 SECONDARY PARAMETERS {cat.upper()} Data Processing Complete.")
        return ds
    else:
        pass
    
def _gefs_0p25_client(date,
            run,
            cat='mean', 
            path=f'GEFS0P25/Archive',
             final_forecast_hour=240, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=False,
             variables=['temperature'],
            convert_temperature=True,
            convert_to='celsius',
            chunk_size=8192,
            notifications='off',
            source='aws',
            level_type='height above ground',
            levels=[2]):
    
    """
    This function downloads the latest GEFS0P50 data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='mean'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    7) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    9) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    12) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50
        -------------------------------
        
			'total precipitation'
            'convective available potential energy'
            'categorical freezing rain'
            'categorical ice pellets'
            'categorical rain'
            'categorical snow'
            'convective inhibition'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'geopotential height'
            'ice thickness'
            'latent heat net flux'
            'pressure'
            'mean sea level pressure'
            'precipitable water'
            'relative humidity'
            'sensible heat net flux'
            'snow depth'
            'volumetric soil moisture content'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'soil temperature'
            'u-component of wind'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'v-component of wind'
            'vertical velocity'
            'water equivalent of accumulated snow depth'
            
    13) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.
    
    14) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    15) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    16) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    17) custom_directory (String or None) - Default=None. The directory path where the GEFS0P50 files will be saved to.
        
    18) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    19) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    20) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
        
    21) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    22) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'height above ground'
        'surface'
        'height below ground'
        'entire atmosphere (considered as a single layer)'
        'pressure above ground'
        
    23) levels (String, Integer or Float List) - Default=[1000,
                                                            925,
                                                            850,
                                                            700,
                                                            500,
                                                            400,
                                                            300,
                                                            250,
                                                            200,
                                                            100,
                                                            50,
                                                            10]    
                                                            
        The pressure, height or depth levels. 
    
    Returns
    -------
    
    An xarray data array of the GEFS0P50 data specified to the coordinate boundaries and variable list the user specifies. 
    
    GEFS0P50 files are saved to f:GEFS0P50/{cat} or in the case of ensemble members f:GEFS0P50/{cat}/{member}
    
    Variables
    ---------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'convective_available_potential_energy'
    'convective_inhibition'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'u_wind_component'
    'v_wind_component'
    
    """
    
    if run == 18 or run == '18':
        run = '18'
    elif run == 12 or run == '12':
        run = '12'
    elif run == 6 or run == '06':
        run = '06'
    else:
        run = '00'
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass    
    
    
    cat = cat.lower()
        
    try:
        url, date = _gefs_0p25_url_scanner(date,
                                        run,
                                        cat, 
                                        final_forecast_hour,
                                        proxies, 
                                        members,
                                        source)
    except Exception as e:
        print(f"Error: Client unable to connect to {source.upper()} Server.")
        if source == 'aws':
            print(f"Rotating to Google Cloud.")
            try:
                url, date = _gefs_0p25_url_scanner(date,
                                                run,
                                                cat, 
                                                final_forecast_hour,
                                                proxies, 
                                                members,
                                                'google')
            except Exception as e:
                print(f"Error: Client unable to establish a connection to either server. - System Exit.")
                _sys.exit(1)
        else:
            print(f"Rotating to AWS.")
            try:
                url, date = _gefs_0p25_url_scanner(date,
                                                run,
                                                cat, 
                                                final_forecast_hour,
                                                proxies, 
                                                members,
                                                'aws')
            except Exception as e:
                print(f"Error: Client unable to establish a connection to either server. - System Exit.")
                _sys.exit(1)

    if cat != 'members':
        if cat == 'mean':
            aa = 'avg'
        elif cat == 'control':
            aa = 'c00'
        else:
            aa = 'spr'
                        
        path = f"{path}/{date.strftime('%Y%m%d')}/{run}/{cat.upper()}"
        paths = [path]
        for path in paths:
            try:
                for file in _os.listdir(f"{path}"):
                    _os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            for i in range(0, final_forecast_hour + step, step):
                if i < 10:
                    byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f00{i}",
                                                f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f00{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{aa}.t{run}z.pgrb2s.0p25.f00{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin) 
                    
                elif i >= 10 and i < (99 + step):
                    byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f0{i}",
                                                f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f0{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{aa}.t{run}z.pgrb2s.0p25.f0{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin)   
                    
                elif i >= 102 and i < (240 + step):
                    byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f{i}",
                                                f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{aa}.t{run}z.pgrb2s.0p25.f{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin)    
                    
                else:
                    cont = True
                    break
                
            if cont == True:
                for i in range(240, final_forecast_hour + 6, 6):
                    byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f{i}",
                                                f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{aa}.t{run}z.pgrb2s.0p25.f{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin) 
            else:
                pass                                                                
                            
    else:
        aa = []
        for member in members:
            if member < 10:
                m = f"p0{member}"
            else:
                m = f"p{member}"
            aa.append(m)
        
        paths = []
        for member in members:
            fpath = f"{path}/{date.strftime('%Y%m%d')}/{run}/{cat.upper()}/{member}" 
            paths.append(fpath)   
        
        for path, a in zip(paths, aa):
            try:
                for file in _os.listdir(f"{path}"):
                    _os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            for i in range(0, final_forecast_hour + step, step):
                if i < 10:
                    byte_range_request(f"{url}ge{a}.t{run}z.pgrb2s.0p25.f00{i}",
                                                f"{url}ge{a}.t{run}z.pgrb2s.0p25.f00{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{a}.t{run}z.pgrb2s.0p25.f00{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin) 
                    
                elif i >= 10 and i < (99 + step):
                    byte_range_request(f"{url}ge{a}.t{run}z.pgrb2s.0p25.f0{i}",
                                                f"{url}ge{a}.t{run}z.pgrb2s.0p25.f0{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{a}.t{run}z.pgrb2s.0p25.f0{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin)   
                    
                elif i >= 102 and i < (240 + step):
                    byte_range_request(f"{url}ge{a}.t{run}z.pgrb2s.0p25.f{i}",
                                                f"{url}ge{a}.t{run}z.pgrb2s.0p25.f{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{a}.t{run}z.pgrb2s.0p25.f{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin)    
                    
                else:
                    cont = True
                    break
                
            if cont == True:
                for i in range(240, final_forecast_hour + 6, 6):
                    byte_range_request(f"{url}ge{a}.t{run}z.pgrb2s.0p25.f{i}",
                                                f"{url}ge{a}.t{run}z.pgrb2s.0p25.f{i}.idx",
                                                variables,
                                                levels,
                                                level_type,
                                                path,
                                                f"ge{a}.t{run}z.pgrb2s.0p25.f{i}.grib2",
                                                proxies=proxies,
                                                chunk_size=chunk_size,
                                                notifications=notifications,
                                                clear_recycle_bin=clear_recycle_bin) 
            else:
                pass  
                        
        print(f"GEFS0P25 {cat.upper()} Download Complete.")        
        
    if process_data == True:
        print(f"GEFS0P25 {cat.upper()} Data Processing...")
        
        ds = _gefs_post_processing.primary_gefs_post_processing(paths,
                                                                western_bound,
                                                                eastern_bound,
                                                                southern_bound,
                                                                northern_bound)
            
        if convert_temperature == True:
            ds = _convert_temperature_units(ds, 
                                            convert_to,
                                            cat=cat)
                
        else:
            pass
            
        print(f"GEFS0P25 {cat.upper()} Data Processing Complete.")
        return ds
    else:
        pass

    
    
def gefs_0p50(date,
              run,
             cat='mean', 
             final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=False,
             variables=['geopotential height'],
            convert_temperature=True,
            convert_to='celsius',
            chunk_size=8192,
            notifications='off',
            source='aws',
            level_type='pressure',
            levels=[500]):
    
    """
    This function downloads the latest GEFS0P50 data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='mean'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    7) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    9) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    12) variables (List) - Default=['geopotential height'].
    
        A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50
        -------------------------------
        
			'total precipitation'
            'convective available potential energy'
            'categorical freezing rain'
            'categorical ice pellets'
            'categorical rain'
            'categorical snow'
            'convective inhibition'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'geopotential height'
            'ice thickness'
            'latent heat net flux'
            'pressure'
            'mean sea level pressure'
            'precipitable water'
            'relative humidity'
            'sensible heat net flux'
            'snow depth'
            'volumetric soil moisture content'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'soil temperature'
            'u-component of wind'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'v-component of wind'
            'vertical velocity'
            'water equivalent of accumulated snow depth'
            
    13) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.
    
    14) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    15) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    16) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    17) custom_directory (String or None) - Default=None. The directory path where the GEFS0P50 files will be saved to.
        
    18) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    19) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    20) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
    21) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    22) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'height below ground'
        'surface'
        'height above ground'
        'top of atmosphere'
        'pressure above ground'
        'mean sea level'
        
        
        
    23) levels (String, Integer or Float List) - Default==[1000,
                                                            925,
                                                            850,
                                                            700,
                                                            500,
                                                            400,
                                                            300,
                                                            250,
                                                            200,
                                                            100,
                                                            50,
                                                            10]  
                                                            
        The pressure, height or depth levels.
    
    Returns
    -------
    
    An xarray data array of the GEFS0P50 data specified to the coordinate boundaries and variable list the user specifies. 
    
    GEFS0P50 files are saved to f:GEFS0P50/{cat} or in the case of ensemble members f:GEFS0P50/{cat}/{member}
    
    Variables
    ---------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'convective_available_potential_energy'
    'convective_inhibition'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'u_wind_component'
    'v_wind_component'
    
    """
    if run == 18 or run == '18':
        run = '18'
    elif run == 12 or run == '12':
        run = '12'
    elif run == 6 or run == '06':
        run = '06'
    else:
        run = '00'
    
    source = source.lower()
    
    try:
        if process_data == True:
            ds = _gefs_0p50_client(date,
                                    run,
                                    cat=cat, 
                final_forecast_hour=final_forecast_hour, 
                western_bound=western_bound, 
                eastern_bound=eastern_bound, 
                northern_bound=northern_bound, 
                southern_bound=southern_bound, 
                proxies=proxies, 
                step=step, 
                members=members,
                process_data=process_data,
                clear_recycle_bin=clear_recycle_bin,
                variables=variables,
                convert_temperature=convert_temperature,
                convert_to=convert_to,
                chunk_size=chunk_size,
                notifications=notifications,
                source=source,
                level_type=level_type,
                levels=levels)
            
        else:
            _gefs_0p50_client(date,
                              run,
                              cat=cat, 
                final_forecast_hour=final_forecast_hour, 
                western_bound=western_bound, 
                eastern_bound=eastern_bound, 
                northern_bound=northern_bound, 
                southern_bound=southern_bound, 
                proxies=proxies, 
                step=step, 
                members=members,
                process_data=process_data,
                clear_recycle_bin=clear_recycle_bin,
                variables=variables,
                convert_temperature=convert_temperature,
                convert_to=convert_to,
                chunk_size=chunk_size,
                notifications=notifications,
                source=source,
                level_type=level_type,
                levels=levels)
    except Exception as e:
        print(f"Error: Client lost connection with {source.upper()} server and is unable to reconnect.")
        if source == 'aws':
            print(f"Rotating to Google Cloud.")
            try:
                if process_data == True:
                    ds = _gefs_0p50_client(date,
                                            run,
                                            cat=cat, 
                        final_forecast_hour=final_forecast_hour, 
                        western_bound=western_bound, 
                        eastern_bound=eastern_bound, 
                        northern_bound=northern_bound, 
                        southern_bound=southern_bound, 
                        proxies=proxies, 
                        step=step, 
                        members=members,
                        process_data=process_data,
                        clear_recycle_bin=clear_recycle_bin,
                        variables=variables,
                        convert_temperature=convert_temperature,
                        convert_to=convert_to,
                        chunk_size=chunk_size,
                        notifications=notifications,
                        source='google',
                        level_type=level_type,
                        levels=levels)
                else:
                    _gefs_0p50_client(date,
                                        run,
                                        cat=cat, 
                        final_forecast_hour=final_forecast_hour, 
                        western_bound=western_bound, 
                        eastern_bound=eastern_bound, 
                        northern_bound=northern_bound, 
                        southern_bound=southern_bound, 
                        proxies=proxies, 
                        step=step, 
                        members=members,
                        process_data=process_data,
                        clear_recycle_bin=clear_recycle_bin,
                        variables=variables,
                        convert_temperature=convert_temperature,
                        convert_to=convert_to,
                        chunk_size=chunk_size,
                        notifications=notifications,
                        source='google',
                        level_type=level_type,
                        levels=levels)
            except Exception as e:
                try:
                    print(f"Error: Data unavailible for {date.strftime('%Y%m%d')} {run}z. - System Exit.")
                except Exception as e:
                    print(f"Error: Data unavailible for {date} {run}z. - System Exit.")
                _sys.exit(1)
                
        else:
            print(f"Rotating to AWS.")
            try:
                if process_data == True:
                    ds = _gefs_0p50_client(date,
                                            run,
                                            cat=cat, 
                        final_forecast_hour=final_forecast_hour, 
                        western_bound=western_bound, 
                        eastern_bound=eastern_bound, 
                        northern_bound=northern_bound, 
                        southern_bound=southern_bound, 
                        proxies=proxies, 
                        step=step, 
                        members=members,
                        process_data=process_data,
                        clear_recycle_bin=clear_recycle_bin,
                        variables=variables,
                        convert_temperature=convert_temperature,
                        convert_to=convert_to,
                        chunk_size=chunk_size,
                        notifications=notifications,
                        source='aws',
                        level_type=level_type,
                        levels=levels)
                else:
                    _gefs_0p50_client(date,
                                        run,
                                        cat=cat, 
                        final_forecast_hour=final_forecast_hour, 
                        western_bound=western_bound, 
                        eastern_bound=eastern_bound, 
                        northern_bound=northern_bound, 
                        southern_bound=southern_bound, 
                        proxies=proxies, 
                        step=step, 
                        members=members,
                        process_data=process_data,
                        clear_recycle_bin=clear_recycle_bin,
                        variables=variables,
                        convert_temperature=convert_temperature,
                        convert_to=convert_to,
                        chunk_size=chunk_size,
                        notifications=notifications,
                        source='aws',
                        level_type=level_type,
                        levels=levels)
            except Exception as e:
                try:
                    print(f"Error: Data unavailible for {date.strftime('%Y%m%d')} {run}z. - System Exit.")
                except Exception as e:
                    print(f"Error: Data unavailible for {date} {run}z. - System Exit.")
                _sys.exit(1)
                
                
    if process_data == True:
        return ds
    else:
        pass
        


def gefs_0p50_secondary_parameters(date,
              run,
             cat='mean', 
             final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=False,
             variables=['temperature'],
            convert_temperature=True,
            convert_to='celsius',
            chunk_size=8192,
            notifications='off',
            source='aws',
            level_type='pressure',
            levels=[750]):
    
    """
    This function downloads the latest GEFS0P50 data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='mean'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    7) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    9) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    12) variables (List) - Default=['geopotential height'].
    
        A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50
        -------------------------------
        
			'total precipitation'
            'convective available potential energy'
            'categorical freezing rain'
            'categorical ice pellets'
            'categorical rain'
            'categorical snow'
            'convective inhibition'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'geopotential height'
            'ice thickness'
            'latent heat net flux'
            'pressure'
            'mean sea level pressure'
            'precipitable water'
            'relative humidity'
            'sensible heat net flux'
            'snow depth'
            'volumetric soil moisture content'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'soil temperature'
            'u-component of wind'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'v-component of wind'
            'vertical velocity'
            'water equivalent of accumulated snow depth'
            
    13) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.
    
    14) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    15) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    16) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    17) custom_directory (String or None) - Default=None. The directory path where the GEFS0P50 files will be saved to.
        
    18) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    19) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    20) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
    21) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    22) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'height below ground'
        'surface'
        'height above ground'
        'top of atmosphere'
        'pressure above ground'
        'mean sea level'
        
        
        
    23) levels (String, Integer or Float List) - Default==[1000,
                                                            925,
                                                            850,
                                                            700,
                                                            500,
                                                            400,
                                                            300,
                                                            250,
                                                            200,
                                                            100,
                                                            50,
                                                            10]  
                                                            
        The pressure, height or depth levels.
    
    Returns
    -------
    
    An xarray data array of the GEFS0P50 data specified to the coordinate boundaries and variable list the user specifies. 
    
    GEFS0P50 files are saved to f:GEFS0P50/{cat} or in the case of ensemble members f:GEFS0P50/{cat}/{member}
    
    Variables
    ---------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'convective_available_potential_energy'
    'convective_inhibition'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'u_wind_component'
    'v_wind_component'
    
    """
    if run == 18 or run == '18':
        run = '18'
    elif run == 12 or run == '12':
        run = '12'
    elif run == 6 or run == '06':
        run = '06'
    else:
        run = '00'
    
    source = source.lower()
    
    try:
        if process_data == True:
            ds = _gefs_0p50_secondary_parameters_client(
                date,
                run,
                cat=cat, 
                final_forecast_hour=final_forecast_hour, 
                western_bound=western_bound, 
                eastern_bound=eastern_bound, 
                northern_bound=northern_bound, 
                southern_bound=southern_bound, 
                proxies=proxies, 
                step=step, 
                members=members,
                process_data=process_data,
                clear_recycle_bin=clear_recycle_bin,
                variables=variables,
                convert_temperature=convert_temperature,
                convert_to=convert_to,
                chunk_size=chunk_size,
                notifications=notifications,
                source=source,
                level_type=level_type,
                levels=levels
                )
            
        else:
            _gefs_0p50_secondary_parameters_client(
                date,
                run,
                cat=cat, 
                final_forecast_hour=final_forecast_hour, 
                western_bound=western_bound, 
                eastern_bound=eastern_bound, 
                northern_bound=northern_bound, 
                southern_bound=southern_bound, 
                proxies=proxies, 
                step=step, 
                members=members,
                process_data=process_data,
                clear_recycle_bin=clear_recycle_bin,
                variables=variables,
                convert_temperature=convert_temperature,
                convert_to=convert_to,
                chunk_size=chunk_size,
                notifications=notifications,
                source=source,
                level_type=level_type,
                levels=levels
                )
    except Exception as e:
        print(f"Error: Client lost connection with {source.upper()} server and is unable to reconnect.")
        if source == 'aws':
            print(f"Rotating to Google Cloud.")
            try:
                if process_data == True:
                    ds = _gefs_0p50_secondary_parameters_client(
                                    date,
                                    run,
                                    cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    source='google',
                                    level_type=level_type,
                                    levels=levels
                                    )
                else:
                    _gefs_0p50_secondary_parameters_client(
                                    date,
                                    run,
                                    cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    source='google',
                                    level_type=level_type,
                                    levels=levels
                                    )
            except Exception as e:
                try:
                    print(f"Error: Data unavailible for {date.strftime('%Y%m%d')} {run}z. - System Exit.")
                except Exception as e:
                    print(f"Error: Data unavailible for {date} {run}z. - System Exit.")
                _sys.exit(1)
                
        else:
            print(f"Rotating to AWS.")
            try:
                if process_data == True:
                    ds = _gefs_0p50_secondary_parameters_client(
                                    date,
                                    run,
                                    cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    source='aws',
                                    level_type=level_type,
                                    levels=levels
                                    )
                else:
                    _gefs_0p50_secondary_parameters_client(
                                    date,
                                    run,
                                    cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    source='aws',
                                    level_type=level_type,
                                    levels=levels
                                    )
            except Exception as e:
                try:
                    print(f"Error: Data unavailible for {date.strftime('%Y%m%d')} {run}z. - System Exit.")
                except Exception as e:
                    print(f"Error: Data unavailible for {date} {run}z. - System Exit.")
                _sys.exit(1)
                
                
    if process_data == True:
        return ds
    else:
        pass
        


def gefs_0p25(date,
              run,
             cat='mean', 
             final_forecast_hour=240, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=False,
             variables=['temperature'],
            convert_temperature=True,
            convert_to='celsius',
            chunk_size=8192,
            notifications='off',
            source='aws',
            level_type='height above ground',
            levels=[2]):
    
    """
    This function downloads the latest GEFS0P50 data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='mean'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    7) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    9) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    12) variables (List) - Default=['geopotential height'].
    
        A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50
        -------------------------------
        
			'total precipitation'
            'convective available potential energy'
            'categorical freezing rain'
            'categorical ice pellets'
            'categorical rain'
            'categorical snow'
            'convective inhibition'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'geopotential height'
            'ice thickness'
            'latent heat net flux'
            'pressure'
            'mean sea level pressure'
            'precipitable water'
            'relative humidity'
            'sensible heat net flux'
            'snow depth'
            'volumetric soil moisture content'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'soil temperature'
            'u-component of wind'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'v-component of wind'
            'vertical velocity'
            'water equivalent of accumulated snow depth'
            
    13) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.
    
    14) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    15) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    16) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    17) custom_directory (String or None) - Default=None. The directory path where the GEFS0P50 files will be saved to.
        
    18) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    19) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    20) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
    21) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    22) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'height below ground'
        'surface'
        'height above ground'
        'top of atmosphere'
        'pressure above ground'
        'mean sea level'
        
        
        
    23) levels (String, Integer or Float List) - Default==[1000,
                                                            925,
                                                            850,
                                                            700,
                                                            500,
                                                            400,
                                                            300,
                                                            250,
                                                            200,
                                                            100,
                                                            50,
                                                            10]  
                                                            
        The pressure, height or depth levels.
    
    Returns
    -------
    
    An xarray data array of the GEFS0P50 data specified to the coordinate boundaries and variable list the user specifies. 
    
    GEFS0P50 files are saved to f:GEFS0P50/{cat} or in the case of ensemble members f:GEFS0P50/{cat}/{member}
    
    Variables
    ---------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'convective_available_potential_energy'
    'convective_inhibition'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'u_wind_component'
    'v_wind_component'
    
    """
    if run == 18 or run == '18':
        run = '18'
    elif run == 12 or run == '12':
        run = '12'
    elif run == 6 or run == '06':
        run = '06'
    else:
        run = '00'
    
    source = source.lower()
    
    #try:
    if process_data == True:
        ds = _gefs_0p25_client(date,
                                run,
                                cat=cat, 
            final_forecast_hour=final_forecast_hour, 
            western_bound=western_bound, 
            eastern_bound=eastern_bound, 
            northern_bound=northern_bound, 
            southern_bound=southern_bound, 
            proxies=proxies, 
            step=step, 
            members=members,
            process_data=process_data,
            clear_recycle_bin=clear_recycle_bin,
            variables=variables,
            convert_temperature=convert_temperature,
            convert_to=convert_to,
            chunk_size=chunk_size,
            notifications=notifications,
            source=source,
            level_type=level_type,
            levels=levels)
    """
            
        else:
            _gefs_0p25_client(date,
                              run,
                              cat=cat, 
                final_forecast_hour=final_forecast_hour, 
                western_bound=western_bound, 
                eastern_bound=eastern_bound, 
                northern_bound=northern_bound, 
                southern_bound=southern_bound, 
                proxies=proxies, 
                step=step, 
                members=members,
                process_data=process_data,
                clear_recycle_bin=clear_recycle_bin,
                variables=variables,
                convert_temperature=convert_temperature,
                convert_to=convert_to,
                chunk_size=chunk_size,
                notifications=notifications,
                source=source,
                level_type=level_type,
                levels=levels)
    except Exception as e:
        print(f"Error: Client lost connection with {source.upper()} server and is unable to reconnect.")
        if source == 'aws':
            print(f"Rotating to Google Cloud.")
            try:
                if process_data == True:
                    ds = _gefs_0p25_client(date,
                                            run,
                                            cat=cat, 
                        final_forecast_hour=final_forecast_hour, 
                        western_bound=western_bound, 
                        eastern_bound=eastern_bound, 
                        northern_bound=northern_bound, 
                        southern_bound=southern_bound, 
                        proxies=proxies, 
                        step=step, 
                        members=members,
                        process_data=process_data,
                        clear_recycle_bin=clear_recycle_bin,
                        variables=variables,
                        convert_temperature=convert_temperature,
                        convert_to=convert_to,
                        chunk_size=chunk_size,
                        notifications=notifications,
                        source='google',
                        level_type=level_type,
                        levels=levels)
                else:
                    _gefs_0p25_client(date,
                                        run,
                                        cat=cat, 
                        final_forecast_hour=final_forecast_hour, 
                        western_bound=western_bound, 
                        eastern_bound=eastern_bound, 
                        northern_bound=northern_bound, 
                        southern_bound=southern_bound, 
                        proxies=proxies, 
                        step=step, 
                        members=members,
                        process_data=process_data,
                        clear_recycle_bin=clear_recycle_bin,
                        variables=variables,
                        convert_temperature=convert_temperature,
                        convert_to=convert_to,
                        chunk_size=chunk_size,
                        notifications=notifications,
                        source='google',
                        level_type=level_type,
                        levels=levels)
            except Exception as e:
                try:
                    print(f"Error: Data unavailible for {date.strftime('%Y%m%d')} {run}z. - System Exit.")
                except Exception as e:
                    print(f"Error: Data unavailible for {date} {run}z. - System Exit.")
                _sys.exit(1)
                
        else:
            print(f"Rotating to AWS.")
            try:
                if process_data == True:
                    ds = _gefs_0p25_client(date,
                                            run,
                                            cat=cat, 
                        final_forecast_hour=final_forecast_hour, 
                        western_bound=western_bound, 
                        eastern_bound=eastern_bound, 
                        northern_bound=northern_bound, 
                        southern_bound=southern_bound, 
                        proxies=proxies, 
                        step=step, 
                        members=members,
                        process_data=process_data,
                        clear_recycle_bin=clear_recycle_bin,
                        variables=variables,
                        convert_temperature=convert_temperature,
                        convert_to=convert_to,
                        chunk_size=chunk_size,
                        notifications=notifications,
                        source='aws',
                        level_type=level_type,
                        levels=levels)
                else:
                    _gefs_0p25_client(date,
                                        run,
                                        cat=cat, 
                        final_forecast_hour=final_forecast_hour, 
                        western_bound=western_bound, 
                        eastern_bound=eastern_bound, 
                        northern_bound=northern_bound, 
                        southern_bound=southern_bound, 
                        proxies=proxies, 
                        step=step, 
                        members=members,
                        process_data=process_data,
                        clear_recycle_bin=clear_recycle_bin,
                        variables=variables,
                        convert_temperature=convert_temperature,
                        convert_to=convert_to,
                        chunk_size=chunk_size,
                        notifications=notifications,
                        source='aws',
                        level_type=level_type,
                        levels=levels)
            except Exception as e:
                try:
                    print(f"Error: Data unavailible for {date.strftime('%Y%m%d')} {run}z. - System Exit.")
                except Exception as e:
                    print(f"Error: Data unavailible for {date} {run}z. - System Exit.")
                _sys.exit(1)
                
    """
    if process_data == True:
        return ds
    else:
        pass