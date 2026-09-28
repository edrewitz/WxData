"""
This file hosts the functions the user interacts with to download GFS data. 

1) gfs_0p25
2) gfs_0p25_secondary_parameters
3) gfs_0p50

(C) Eric J. Drewitz 2025-2026
"""
import sys as _sys
import os as _os
import warnings as _warnings
import wxdata.post_processors.gfs_post_processing as _gfs_post_processing
_warnings.filterwarnings('ignore')

from wxdata.client.client import byte_range_request as _byte_range_request
from wxdata.utils.transforms import grib_to_netcdf as _grib_to_netcdf
from wxdata.model_data.noaa.gfs.paths import build_directory as _build_directory
from wxdata.archived_data.model_data.noaa.gfs.url_scanners import(
    gfs_0p50_url_scanner as _gfs_0p50_url_scanner,
    gfs_0p25_url_scanner as _gfs_0p25_url_scanner,
    gfs_0p25_secondary_parameters_url_scanner as _gfs_0p25_secondary_parameters_url_scanner
)

from wxdata.utils.warnings import(
    eccodes_warning as _eccodes_warning,
    version_warning as _version_warning
)
from datetime import datetime as _datetime
from wxdata.utils.file_funcs import clear_old_data as _clear_old_data
from wxdata.calc.unit_conversion import convert_temperature_units as _convert_temperature_units
from wxdata.utils.file_scanner import local_file_scanner as _local_file_scanner
from wxdata.utils.recycle_bin import(
    clear_recycle_bin_windows as _clear_recycle_bin_windows,
    clear_trash_bin_mac as _clear_trash_bin_mac,
    clear_trash_bin_linux as _clear_trash_bin_linux
)

start = _datetime.strptime("2021-01-01:00", "%Y-%m-%d:%H")


_eccodes_warning()

def _gfs_0p25_client(
            date,
            run,
            final_forecast_hour=384, 
            western_bound=-180, 
            eastern_bound=180, 
            northern_bound=90, 
            southern_bound=-90, 
            step=3,
            process_data=True,
            proxies=None, 
            variables=['geopotential height',
                       'temperature',
                       'relative humidity',
                       'u-component of wind',
                       'v-component of wind'],
            clear_recycle_bin=False,
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
                    10],
            path=f"GFS0P25/Archive"):
    
    """
    This function downloads GFS0P25 data and saves it to a folder. 
    
    Required Argumemnts: 
    
    1) date (String or datetime) - The date of the model run.
    
    2) run (Integer) - The model runtime in UTC (0, 6, 12, 18).
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GFS0P25
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 6 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. Set to 3 for 3hr increments and 6 for 6hrly increments.
    
    7) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
       
    9) variables (String List) - Default=['geopotential height',
                                            'temperature',
                                            'relative humidity',
                                            'u-component of wind',
                                            'v-component of wind']
                       
        The variables the user wishes to query.
    
        Variables
        ---------
        
        'best lifted index'
        'absolute vorticity'
        'convective precipitation'
        'albedo'
        'total precipitation'
        'convective available potential energy'
        'categorical freezing rain'
        'categorical ice pellets'
        'convective inhibition'
        'cloud mixing ratio'
        'plant canopy surface water'
        'percent frozen precipitaion'
        'convective precipitation rate'
        'categorical rain'
        'categorical snow'
        'cloud water'
        'cloud work function'
        'downward longwave radiation flux'
        'dew point'
        'downward shortwave radiation flux'
        'vertical velocity (height)'
        'field capacity'
        'surface friction velocity'
        'ground heat flux'
        'graupel'
        'wind gust'
        'high cloud cover'
        'geopotential height'
        'haines index'
        'storm relative helicity'
        'planetary boundary layer height'
        'icao standard atmosphere reference height'
        'ice cover'
        'ice growth rate'
        'ice thickness'
        'ice temperature'
        'ice water mixing ratio'
        'land cover'
        'low cloud cover'
        'surface lifted index'
        'latent heat net flux'
        'middle cloud cover'
        'mslp (eta model reduction)'
        'ozone mixing ratio'
        'potential evaporation rate'
        'pressure level from which parcel was lifted'
        'potential temperature'
        'precipitation rate'
        'pressure'
        'mean sea level pressure'
        'precipitable water'
        'composite reflectivity'
        'reflectivity'
        'relative humidity'
        'rain mixing ratio'
        'surface roughness'
        'sensible heat net flux'
        'snow mixing ratio'
        'snow depth'
        'liquid volumetric soil moisture (non-frozen)'
        'volumetric soil moisture content'
        'soil type'
        'specific humidity'
        'sunshine duration'
        'total cloud cover'
        'maximum temperature'
        'minimum temperature'
        'temperature'
        'total ozone'
        'soil temperature'
        'momentum flux (u-component)'
        'u-component of wind'
        'zonal flux of gravity wave stress'
        'upward longwave radiation flux'
        'u-component of storm motion'
        'upward shortwave radiation flux'
        'vegetation'
        'momentum flux (v-component)'
        'v-component of wind'
        'meridional flux of gravity wave stress'
        'visibility'
        'ventilation rate'
        'v-component of storm motion'
        'vertical velocity (pressure)'
        'vertical speed shear'
        'water runoff'
        'water equivalent of accumulated snow depth'
        'wilting point'          
        
    10) path (String) - Default="GFS0P25/Archive". The local directory where the archived GFS data will be stored. 
    
    11) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    12) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    13) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    14) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    15) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
        
    16) source (String) - Default='aws'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) Amazon AWS - source='aws'
        2) Google Cloud - source='google'
        
    17) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'mean sea level'
        'hybrid'
        'entire atmosphere'
        'boundary layer'
        'low cloud layer'
        'middle cloud layer'
        'high cloud layer'
        'convective cloud bottom level'
        'low cloud bottom level'
        'middle cloud bottom level'
        'high cloud bottom level'
        'convective cloud top level'
        'low cloud top level'
        'middle cloud top level'
        'high cloud top level'
        'convective cloud layer'
        'tropopause'
        'max wind'
        'isothermal'
        'highest tropospheric freezing level'
        'height above ground'
        'surface'
        'height below ground'
        'sigma layer'
        'sigma level'
        'entire atmosphere (considered as a single layer)'
        'pressure above ground'
        'potential vorticity surface'
        
    18) levels (String, Integer or Float List) - Default=[1000,
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
    
    An xarray.array dataset of the most recent GFS0P25 run. 
    
    Post-processed Variable Key List
    --------------------------------
    
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
    'surface_visibility'
    'surface_wind_gust'
    'percent_frozen_precipitation'
    'convective_available_potential_energy'
    'convective_inhibition'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    '2m_dew_point'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'mixed_layer_cape'
    'mixed_layer_cin'
    '3km_helicity'
    
    """
    
    if type(date) == type(start):
        date = date
    else:
        date = f"{date[0:4]}{date[5:7]}{date[8:10]}"
        date = _datetime.strptime(date, "%Y%m%d")
    
    if run == 18 or run == '18':
        run = '18'
    elif run == 12 or run == '12':
        run = '12'
    elif run == 6 or run == '06':
        run = '06'
    else:
        run = '00'
    
    source = source.lower()
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass

    _clear_old_data(f"{path}/{date.strftime('%Y%m%d')}/{run}")
        
    try:
        url = _gfs_0p25_url_scanner(date,
                        run,
                        final_forecast_hour, 
                        proxies, 
                        source)
    except Exception as e:
        print(f"Error: Data not found on {source.upper()} server OR {source.upper()} server could be down.")
        if source == 'aws':
            print(f"Rotating to Google Cloud and Retrying.")
            try:
                url = _gfs_0p25_url_scanner(date,
                                            run,
                                            final_forecast_hour, 
                                            proxies, 
                                            'google')
            except Exception as e:
                print(f"Error: Client is unable to connect to either server.")
                print(f"Tip: Double check the date for typos. Record begins at: {start.strftime('%Y%m%d')} 00z")
                print("System Exit")
                _sys.exit(1)
                
        else:
            print(f"Rotating to AWS and Retrying.")
            try:
                url = _gfs_0p25_url_scanner(date,
                                            run,
                                            final_forecast_hour, 
                                            proxies, 
                                            'aws')
            except Exception as e:
                print(f"Error: Client is unable to connect to either server.")
                print(f"Tip: Double check the date for typos. Record begins at: {start.strftime('%Y%m%d')} 00z")
                print("System Exit")
                _sys.exit(1)
                
    print(f"Downloading GFS0P25 data for {date.strftime('%Y%m%d')} {run}z")
                
    for i in range(0, final_forecast_hour + step, step):
        if i < 10:
            _byte_range_request(f"{url}gfs.t{run}z.pgrb2.0p25.f00{i}",
                                        f"{url}gfs.t{run}z.pgrb2.0p25.f00{i}.idx",
                                        variables,
                                        levels,
                                        level_type,
                                        f"{path}/{date.strftime('%Y%m%d')}/{run}",
                                        f"gfs.t{run}z.pgrb2.0p25.f00{i}.grib2",
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin) 
            
        elif i >= 10 and i < (99 + step):
            _byte_range_request(f"{url}gfs.t{run}z.pgrb2.0p25.f0{i}",
                                        f"{url}gfs.t{run}z.pgrb2.0p25.f0{i}.idx",
                                        variables,
                                        levels,
                                        level_type,
                                        f"{path}/{date.strftime('%Y%m%d')}/{run}",
                                        f"gfs.t{run}z.pgrb2.0p25.f0{i}.grib2",
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin)   
            
        elif i >= 102 and i < (240 + step):
            _byte_range_request(f"{url}gfs.t{run}z.pgrb2.0p25.f{i}",
                                        f"{url}gfs.t{run}z.pgrb2.0p25.f{i}.idx",
                                        variables,
                                        levels,
                                        level_type,
                                        f"{path}/{date.strftime('%Y%m%d')}/{run}",
                                        f"gfs.t{run}z.pgrb2.0p25.f{i}.grib2",
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin)    
            
        else:
            cont = True
            break
        
    if cont == True:
        for i in range(240, final_forecast_hour + 6, 6):
            _byte_range_request(f"{url}gfs.t{run}z.pgrb2.0p25.f{i}",
                                        f"{url}gfs.t{run}z.pgrb2.0p25.f{i}.idx",
                                        variables,
                                        levels,
                                        level_type,
                                        f"{path}/{date.strftime('%Y%m%d')}/{run}",
                                        f"gfs.t{run}z.pgrb2.0p25.f{i}.grib2",
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin) 
    else:
        pass      
    
    print(f"GFS0P25 Download Complete for {date.strftime('%Y%m%d')} {run}z") 
            
    if process_data == True:
        print(f"GFS0P25 Data Processing...")
        
        ds = _gfs_post_processing.primary_gfs_post_processing(f"{path}/{date.strftime('%Y%m%d')}/{run}",
                                                              western_bound,
                                                              eastern_bound,
                                                              southern_bound,
                                                              northern_bound)
        
        if convert_temperature == True:
                ds = _convert_temperature_units(ds, 
                                            convert_to)
                
        else:
            pass
        
        print(f"GFS0P25 Data Processing Complete for {date.strftime('%Y%m%d')} {run}z.")
        return ds
    
    else:
        pass        
    
    
    
def _gfs_0p25_secondary_parameters_client(
            date,
            run,
            final_forecast_hour=384, 
            western_bound=-180, 
            eastern_bound=180, 
            northern_bound=90, 
            southern_bound=-90, 
            step=3,
            process_data=True,
            proxies=None, 
            variables=['geopotential height',
                       'temperature',
                       'relative humidity',
                       'u-component of wind',
                       'v-component of wind'],
            clear_recycle_bin=False,
            convert_temperature=True,
            convert_to='celsius',
            chunk_size=8192,
            notifications='off',
            source='aws',
            level_type='pressure',
            levels=[875,
                    825,
                    775,
                    725,
                    675,
                    625,
                    575,
                    525,
                    475,
                    425,
                    375,
                    325,
                    275,
                    225,
                    175,
                    125,
                    7,
                    5,
                    3,
                    2,
                    1],
            path=f"GFS0P25 SECONDARY PARAMETERS/Archive"):
    
    """
    This function downloads GFS0P25 SECONDARY PARAMETERS data and saves it to a folder. 
    
    Required Arguments:
    
    1) date (String or datetime) - The date of the model run.
    
    2) run (Integer) - The model runtime in UTC (0, 6, 12, 18).
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GFS0P25
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 6 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. Set to 3 for 3hr increments and 6 for 6hrly increments.
    
    7) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
       
    9) variables (String List) - Default=['geopotential height',
                                            'temperature',
                                            'relative humidity',
                                            'u-component of wind',
                                            'v-component of wind']
                       
        The variables the user wishes to query.
    
        Variables
        ---------
        
        'absolute vorticity'
        'clear sky uv-b downward solar flux'
        'cloud mixing ratio'
        'plant canopy surface water'
        'uv-b downward solar flux'
        'vertical velocity (height)'
        'graupel'
        'geopotential height'
        'ice thickness'
        'ice water mixing ratio'
        'ozone mixing ratio'
        'pressure'
        'relative humidity'
        'rain mixing ratio'
        'snow mixing ratio'
        'liquid volumetric soil moisture (non-frozen)'
        'specific humidity'
        'total cloud cover'
        'temperature'
        'u-component of wind'
        'v-component of wind'
        'vertical velocity (pressure)'
        'vertical speed shear'      
    
    10) path (String) - Default="GFS0P25 SECONDARY PARAMETERS/Archive". The local directory where the archived GFS data will be stored. 
    
    11) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    12) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    13) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    14) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    15) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    16) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) Amazon AWS - source='aws'
        2) Google Cloud - source='google'
        
    17) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'height below ground'
        'surface'
        'height above ground'
        'height above sea level'
        'pressure above ground'
        'potential vorticity surface'
        
    18) levels (String, Integer or Float List) - Default=[875,
                                                            825,
                                                            775,
                                                            725,
                                                            675,
                                                            625,
                                                            575,
                                                            525,
                                                            475,
                                                            425,
                                                            375,
                                                            325,
                                                            275,
                                                            225,
                                                            175,
                                                            125,
                                                            7,
                                                            5,
                                                            3,
                                                            2,
                                                            1]
                                                            
        The pressure, height or depth levels.
    
    Returns
    -------
    
    An xarray.array dataset of the most recent GFS0P25 run. 
    
    Post-processed Variable Key List
    --------------------------------
    
    'u_wind_component'
    'v_wind_component'
    'air_temperature'
    'relative_humidity'
    'absolute_vorticity'
    'geopotential_height'
    'ozone_mixing_ratio'
    'total_cloud_cover'
    'cloud_mixing_ratio'
    'ice_water_mixing_ratio'
    'rain_water_mixing_ratio'
    'snow_mixing_ratio'
    'graupel'
    'vertical_velocity'
    'geometric_vertical_velocity'
    'liquid_volumetric_soil_moisture_non_frozen'
    'plant_canopy_surface_water'
    'sea_ice_thickness'
    'temperature_height_above_sea'
    'u_wind_component_height_above_sea'
    'v_wind_component_height_above_sea'
    'mixed_layer_temperature'
    'mixed_layer_relative_humidity'
    'mixed_layer_specific_humidity'
    'mixed_layer_u_wind_component'
    'mixed_layer_v_wind_component'
    'potential_vorticity_level_u_wind_component'
    'potential_vorticity_level_v_wind_component'
    'potential_vorticity_level_temperature'
    'potential_vorticity_level_geopotential_height'
    'potential_vorticity_level_air_pressure'
    'potential_vorticity_level_vertical_speed_shear' 
    
    """
    if type(date) == type(start):
        date = date
    else:
        date = f"{date[0:4]}{date[5:7]}{date[8:10]}"
        date = _datetime.strptime(date, "%Y%m%d")
    
    if run == 18 or run == '18':
        run = '18'
    elif run == 12 or run == '12':
        run = '12'
    elif run == 6 or run == '06':
        run = '06'
    else:
        run = '00'
    
    source = source.lower()
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
        
    _clear_old_data(f"{path}/{date.strftime('%Y%m%d')}/{run}")

        
    try:
        url = _gfs_0p25_secondary_parameters_url_scanner(date,
                        run,
                        final_forecast_hour, 
                        proxies, 
                        source)
    except Exception as e:
        print(f"Error: Data not found on {source.upper()} server OR {source.upper()} server could be down.")
        if source == 'aws':
            print(f"Rotating to Google Cloud and Retrying.")
            try:
                url = _gfs_0p25_secondary_parameters_url_scanner(date,
                                            run,
                                            final_forecast_hour, 
                                            proxies, 
                                            'google')
            except Exception as e:
                print(f"Error: Client is unable to connect to either server.")
                print(f"Tip: Double check the date for typos. Record begins at: {start.strftime('%Y%m%d')} 00z")
                print("System Exit")
                _sys.exit(1)
                
        else:
            print(f"Rotating to AWS and Retrying.")
            try:
                url = _gfs_0p25_secondary_parameters_url_scanner(date,
                                            run,
                                            final_forecast_hour, 
                                            proxies, 
                                            'aws')
            except Exception as e:
                print(f"Error: Client is unable to connect to either server.")
                print(f"Tip: Double check the date for typos. Record begins at: {start.strftime('%Y%m%d')} 00z")
                print("System Exit")
                _sys.exit(1)
                
    print(f"Downloading GFS0P25 SECONDARY PARAMETERS data for {date.strftime('%Y%m%d')} {run}z")

    for i in range(0, final_forecast_hour + step, step):
        if i < 10:
            _byte_range_request(f"{url}gfs.t{run}z.pgrb2b.0p25.f00{i}",
                                        f"{url}gfs.t{run}z.pgrb2b.0p25.f00{i}.idx",
                                        variables,
                                        levels,
                                        level_type,
                                        f"{path}/{date.strftime('%Y%m%d')}/{run}",
                                        f"gfs.t{run}z.pgrb2b.0p25.f00{i}.grib2",
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin) 
            
        elif i >= 10 and i < (99 + step):
            _byte_range_request(f"{url}gfs.t{run}z.pgrb2b.0p25.f0{i}",
                                        f"{url}gfs.t{run}z.pgrb2b.0p25.f0{i}.idx",
                                        variables,
                                        levels,
                                        level_type,
                                        f"{path}/{date.strftime('%Y%m%d')}/{run}",
                                        f"gfs.t{run}z.pgrb2b.0p25.f0{i}.grib2",
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin)   
            
        elif i >= 102 and i < (240 + step):
            _byte_range_request(f"{url}gfs.t{run}z.pgrb2b.0p25.f{i}",
                                        f"{url}gfs.t{run}z.pgrb2b.0p25.f{i}.idx",
                                        variables,
                                        levels,
                                        level_type,
                                        f"{path}/{date.strftime('%Y%m%d')}/{run}",
                                        f"gfs.t{run}z.pgrb2b.0p25.f{i}.grib2",
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin)    
            
        else:
            cont = True
            break
        
    if cont == True:
        for i in range(240, final_forecast_hour + 6, 6):
            _byte_range_request(f"{url}gfs.t{run}z.pgrb2b.0p25.f{i}",
                                        f"{url}gfs.t{run}z.pgrb2b.0p25.f{i}.idx",
                                        variables,
                                        levels,
                                        level_type,
                                        f"{path}/{date.strftime('%Y%m%d')}/{run}",
                                        f"gfs.t{run}z.pgrb2b.0p25.f{i}.grib2",
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin) 
    else:
        pass      
        
    print(f"GFS0P25 Secondary Parameters Download Complete for {date.strftime('%Y%m%d')} {run}z") 
    
    if process_data == True:
        print(f"GFS0P25 Secondary Parameters Data Processing...")
        
        ds = _gfs_post_processing.secondary_gfs_post_processing(f"{path}/{date.strftime('%Y%m%d')}/{run}",
                                                                western_bound,
                                                                eastern_bound,
                                                                southern_bound,
                                                                northern_bound)
        
        if convert_temperature == True:
                ds = _convert_temperature_units(ds, 
                                            convert_to)
                
        else:
            pass
        
        print(f"GFS0P25 SECONDARY PARAMETERS Data Processing Complete.")
        return ds
    
    else:
        pass        
    
        
        
def _gfs_0p50_client(
            date,
            run,
            final_forecast_hour=384, 
            western_bound=-180, 
            eastern_bound=180, 
            northern_bound=90, 
            southern_bound=-90, 
            step=3,
            process_data=True,
            proxies=None, 
            variables=['geopotential height',
                       'temperature',
                       'relative humidity',
                       'u-component of wind',
                       'v-component of wind'],
            clear_recycle_bin=False,
            convert_temperature=True,
            convert_to='celsius',
            chunk_size=8192,
            notifications='off',
            source='noaa',
            level_type='pressure',
            levels=[1000,
                    975,
                    950,
                    925,
                    900,
                    850,
                    800,
                    750,
                    700,
                    650,
                    600,
                    550,
                    500,
                    450,
                    400,
                    350,
                    300,
                    250,
                    200,
                    150,
                    100,
                    70,
                    50,
                    40,
                    30,
                    20,
                    15,
                    10,
                    7,
                    5,
                    3,
                    2,
                    1],
            path=f"GFS0P50/Archive"):
    
    """
    This function downloads GFS0P50 data and saves it to a folder. 
    
    Required Arguments:
    
    1) date (String or datetime) - The date of the model run.
    
    2) run (Integer) - The model runtime in UTC (0, 6, 12, 18).
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 6 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. Set to 3 for 3hr increments and 6 for 6hrly increments.
    
    7) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
       
    9) variables (String List) - Default=['geopotential height',
                                            'temperature',
                                            'relative humidity',
                                            'u-component of wind',
                                            'v-component of wind']
                       
        The variables the user wishes to query.
    
        Variables
        ---------
        
        'best lifted index'
        'absolute vorticity'
        'convective precipitation'
        'albedo'
        'total precipitation'
        'convective available potential energy'
        'categorical freezing rain'
        'categorical ice pellets'
        'convective inhibition'
        'cloud mixing ratio'
        'plant canopy surface water'
        'percent frozen precipitaion'
        'convective precipitation rate'
        'categorical rain'
        'categorical snow'
        'cloud water'
        'cloud work function'
        'downward longwave radiation flux'
        'dew point'
        'downward shortwave radiation flux'
        'vertical velocity (height)'
        'field capacity'
        'surface friction velocity'
        'ground heat flux'
        'graupel'
        'wind gust'
        'high cloud cover'
        'geopotential height'
        'haines index'
        'storm relative helicity'
        'planetary boundary layer height'
        'icao standard atmosphere reference height'
        'ice cover'
        'ice growth rate'
        'ice thickness'
        'ice temperature'
        'ice water mixing ratio'
        'land cover'
        'low cloud cover'
        'surface lifted index'
        'latent heat net flux'
        'middle cloud cover'
        'mslp (eta model reduction)'
        'ozone mixing ratio'
        'potential evaporation rate'
        'pressure level from which parcel was lifted'
        'potential temperature'
        'precipitation rate'
        'pressure'
        'mean sea level pressure'
        'precipitable water'
        'composite reflectivity'
        'reflectivity'
        'relative humidity'
        'rain mixing ratio'
        'surface roughness'
        'sensible heat net flux'
        'snow mixing ratio'
        'snow depth'
        'liquid volumetric soil moisture (non-frozen)'
        'volumetric soil moisture content'
        'soil type'
        'specific humidity'
        'sunshine duration'
        'total cloud cover'
        'maximum temperature'
        'minimum temperature'
        'temperature'
        'total ozone'
        'soil temperature'
        'momentum flux (u-component)'
        'u-component of wind'
        'zonal flux of gravity wave stress'
        'upward longwave radiation flux'
        'u-component of storm motion'
        'upward shortwave radiation flux'
        'vegetation'
        'momentum flux (v-component)'
        'v-component of wind'
        'meridional flux of gravity wave stress'
        'visibility'
        'ventilation rate'
        'v-component of storm motion'
        'vertical velocity (pressure)'
        'vertical speed shear'
        'water runoff'
        'water equivalent of accumulated snow depth'
        'wilting point'
        'clear sky uv-b downward solar flux'
        'uv-b downward solar flux'       
    
    10) path (String) - Default="GFS0P50/Archive". The local directory where the archived GFS data will be stored. 
    
    11) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    12) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    13) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    14) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    15) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    16) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    17) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'mean sea level'
        'hybrid'
        'entire atmosphere'
        'boundary layer'
        'low cloud layer'
        'middle cloud layer'
        'high cloud layer'
        'convective cloud bottom level'
        'low cloud bottom level'
        'middle cloud bottom level'
        'high cloud bottom level'
        'convective cloud top level'
        'low cloud top level'
        'middle cloud top level'
        'high cloud top level'
        'convective cloud layer'
        'tropopause'
        'max wind'
        'isothermal'
        'highest tropospheric freezing level'
        'height above ground'
        'surface'
        'height below ground'
        'sigma layer'
        'sigma level'
        'entire atmosphere (considered as a single layer)'
        'pressure above ground'
        'potential vorticity surface'
        
        
    18) levels (String, Integer or Float List) - Default=levels=[1000,
                                                                    975,
                                                                    950,
                                                                    925,
                                                                    900,
                                                                    850,
                                                                    800,
                                                                    750,
                                                                    700,
                                                                    650,
                                                                    600,
                                                                    550,
                                                                    500,
                                                                    450,
                                                                    400,
                                                                    350,
                                                                    300,
                                                                    250,
                                                                    200,
                                                                    150,
                                                                    100,
                                                                    70,
                                                                    50,
                                                                    40,
                                                                    30,
                                                                    20,
                                                                    15,
                                                                    10,
                                                                    7,
                                                                    5,
                                                                    3,
                                                                    2,
                                                                    1]
                                                            
        The pressure, height or depth levels.
    
    Returns
    -------
    
    An xarray.array dataset of the most recent GFS0P50 run. 
    
    Post-processed Variable Key List
    --------------------------------
    
    'mslp'
    'mslp_eta_reduction'
    'hybrid_level_cloud_mixing_ratio'
    'hybrid_level_ice_water_mixing_ratio'
    'hybrid_level_rain_mixing_ratio'
    'hybrid_level_snow_mixing_ratio'
    'hybrid_level_graupel'
    'hybrid_level_derived_radar_reflectivity'
    'boundary_layer_wind_u_component'
    'boundary_layer_wind_v_component'
    'ventilation_rate'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'vertical_velocity'
    'geometric_vertical_velocity'
    'u_wind_component'
    'v_wind_component'
    'absolute_vorticity'
    'total_cloud_cover'
    'ice_water_mixing_ratio'
    'rain_mixing_ratio'
    'cloud_mixing_ratio'
    'snow_mixing_ratio'
    'graupel'
    'derived_radar_reflectivity'
    '2m_temperature'
    '2m_specific_humidity'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_dew_point_depression'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'low_level_u_wind_component'
    'low_level_v_wind_component'
    'low_level_temperature'
    'low_level_specific_humidity'
    'pressure_height_above_ground'
    '100m_u_wind_component'
    '100m_v_wind_component'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    'liquid_volumetric_soil_moisture_non_frozen'
    'temperature_height_above_sea'
    'u_wind_component_height_above_sea'
    'v_wind_component_height_above_sea'
    'precipitable_water'
    'cloud_water'
    'entire_atmosphere_relative_humidity'
    'total_ozone'
    'low_cloud_cover'
    'middle_cloud_cover'
    'high_cloud_cover'
    'cloud_ceiling_height'
    'storm_relative_helicity'
    'u_component_of_storm_motion'
    'v_component_of_storm_motion'
    'tropopause_pressure'
    'tropopause_standard_atmosphere_reference_height'
    'tropopause_height'
    'tropopause_u_wind_component'
    'tropopause_v_wind_component'
    'tropopause_temperature'
    'tropopause_vertical_speed_shear'
    'max_wind_u_component'
    'max_wind_v_component'
    'zero_deg_c_isotherm_geopotential_height'
    'zero_deg_c_isotherm_relative_humidity'
    'highest_tropospheric_freezing_level_geopotential_height'
    'highest_tropospheric_freezing_level_relative_humidity'
    'mixed_layer_temperature'
    'mixed_layer_relative_humidity'
    'mixed_layer_specific_humidity'
    'mixed_layer_u_wind_component'
    'mixed_layer_v_wind_component'
    'mixed_layer_cape'
    'mixed_layer_cin'
    'pressure_level_from_which_a_parcel_was_lifted'
    'sigma_layer_relative_humidity'
    '995_sigma_temperature'
    '995_sigma_theta'
    '995_sigma_relative_humdity'
    '995_u_wind_component'
    '995_v_wind_component'
    '995_vertical_velocity'
    'potential_vorticity_level_u_wind_component'
    'potential_vorticity_level_v_wind_component'
    'potential_vorticity_level_temperature'
    'potential_vorticity_level_geopotential_height'
    'potential_vorticity_level_air_pressure'
    'potential_vorticity_level_vertical_speed_shear'
    
    """
    if type(date) == type(start):
        date = date
    else:
        date = f"{date[0:4]}{date[5:7]}{date[8:10]}"
        date = _datetime.strptime(date, "%Y%m%d")
    
    if run == 18 or run == '18':
        run = '18'
    elif run == 12 or run == '12':
        run = '12'
    elif run == 6 or run == '06':
        run = '06'
    else:
        run = '00'
    
    source = source.lower()
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
        
    _clear_old_data(f"{path}/{date.strftime('%Y%m%d')}/{run}")

        
    try:
        url = _gfs_0p50_url_scanner(date,
                        run,
                        final_forecast_hour, 
                        proxies, 
                        source)
    except Exception as e:
        print(f"Error: Data not found on {source.upper()} server OR {source.upper()} server could be down.")
        if source == 'aws':
            print(f"Rotating to Google Cloud and Retrying.")
            try:
                url = _gfs_0p50_url_scanner(date,
                                            run,
                                            final_forecast_hour, 
                                            proxies, 
                                            'google')
            except Exception as e:
                print(f"Error: Client is unable to connect to either server.")
                print(f"Tip: Double check the date for typos. Record begins at: {start.strftime('%Y%m%d')} 00z")
                print("System Exit")
                _sys.exit(1)
                
        else:
            print(f"Rotating to AWS and Retrying.")
            try:
                url = _gfs_0p50_url_scanner(date,
                                            run,
                                            final_forecast_hour, 
                                            proxies, 
                                            'aws')
            except Exception as e:
                print(f"Error: Client is unable to connect to either server.")
                print(f"Tip: Double check the date for typos. Record begins at: {start.strftime('%Y%m%d')} 00z")
                print("System Exit")
                _sys.exit(1)
                
    print(f"Downloading GFS0P50 data for {date.strftime('%Y%m%d')} {run}z")

    for i in range(0, final_forecast_hour + step, step):
        if i < 10:
            _byte_range_request(f"{url}gfs.t{run}z.pgrb2full.0p50.f00{i}",
                                        f"{url}gfs.t{run}z.pgrb2full.0p50.f00{i}.idx",
                                        variables,
                                        levels,
                                        level_type,
                                        f"{path}/{date.strftime('%Y%m%d')}/{run}",
                                        f"gfs.t{run}z.pgrb2full.0p50.f00{i}.grib2",
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin) 
            
        elif i >= 10 and i < (99 + step):
            _byte_range_request(f"{url}gfs.t{run}z.pgrb2full.0p50.f0{i}",
                                        f"{url}gfs.t{run}z.pgrb2full.0p50.f0{i}.idx",
                                        variables,
                                        levels,
                                        level_type,
                                        f"{path}/{date.strftime('%Y%m%d')}/{run}",
                                        f"gfs.t{run}z.pgrb2full.0p50.f0{i}.grib2",
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin)   
            
        elif i >= 102 and i < (240 + step):
            _byte_range_request(f"{url}gfs.t{run}z.pgrb2full.0p50.f{i}",
                                        f"{url}gfs.t{run}z.pgrb2full.0p50.f{i}.idx",
                                        variables,
                                        levels,
                                        level_type,
                                        f"{path}/{date.strftime('%Y%m%d')}/{run}",
                                        f"gfs.t{run}z.pgrb2full.0p50.f{i}.grib2",
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin)    
            
        else:
            cont = True
            break
        
    if cont == True:
        for i in range(240, final_forecast_hour + 6, 6):
            _byte_range_request(f"{url}gfs.t{run}z.pgrb2full.0p50.f{i}",
                                        f"{url}gfs.t{run}z.pgrb2full.0p50.f{i}.idx",
                                        variables,
                                        levels,
                                        level_type,
                                        f"{path}/{date.strftime('%Y%m%d')}/{run}",
                                        f"gfs.t{run}z.pgrb2full.0p50.f{i}.grib2",
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin) 
    else:
        pass      
        
    print(f"GFS0P50 Download Complete for {date.strftime('%Y%m%d')} {run}z") 
    
    if process_data == True:
        print(f"GFS0P50 Data Processing...")
        
        ds = _gfs_post_processing.primary_gfs_post_processing(f"{path}/{date.strftime('%Y%m%d')}/{run}",
                                                                western_bound,
                                                                eastern_bound,
                                                                southern_bound,
                                                                northern_bound)
        
        if convert_temperature == True:
                ds = _convert_temperature_units(ds, 
                                            convert_to)
                
        else:
            pass
        
        print(f"GFS0P50 Data Processing Complete.")
        return ds
    
    else:
        pass      
    

def gfs_0p25(date,
             run,
            path=f"GFS0P25/Archive",
            final_forecast_hour=384, 
            western_bound=-180, 
            eastern_bound=180, 
            northern_bound=90, 
            southern_bound=-90, 
            step=3,
            process_data=True,
            proxies=None, 
            variables=['geopotential height',
                       'temperature',
                       'relative humidity',
                       'u-component of wind',
                       'v-component of wind'],
            clear_recycle_bin=False,
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
                    10],
            to_netcdf=False,
            netcdf_path=f"GFS0P25/Archive/NETCDF",
            netcdf_filename=f"gfs_0p25.nc",
            delete_previous_netcdf_file=True,
            return_values=True):
    
    """
    This function downloads GFS0P25 data and saves it to a folder. 
    
    Required Argumemnts: 
    
    1) date (String or datetime) - The date of the model run.
    
    2) run (Integer) - The model runtime in UTC (0, 6, 12, 18).
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GFS0P25
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 6 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. Set to 3 for 3hr increments and 6 for 6hrly increments.
    
    7) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
       
    9) variables (String List) - Default=['geopotential height',
                                            'temperature',
                                            'relative humidity',
                                            'u-component of wind',
                                            'v-component of wind']
                       
        The variables the user wishes to query.
    
        Variables
        ---------
        
        'best lifted index'
        'absolute vorticity'
        'convective precipitation'
        'albedo'
        'total precipitation'
        'convective available potential energy'
        'categorical freezing rain'
        'categorical ice pellets'
        'convective inhibition'
        'cloud mixing ratio'
        'plant canopy surface water'
        'percent frozen precipitaion'
        'convective precipitation rate'
        'categorical rain'
        'categorical snow'
        'cloud water'
        'cloud work function'
        'downward longwave radiation flux'
        'dew point'
        'downward shortwave radiation flux'
        'vertical velocity (height)'
        'field capacity'
        'surface friction velocity'
        'ground heat flux'
        'graupel'
        'wind gust'
        'high cloud cover'
        'geopotential height'
        'haines index'
        'storm relative helicity'
        'planetary boundary layer height'
        'icao standard atmosphere reference height'
        'ice cover'
        'ice growth rate'
        'ice thickness'
        'ice temperature'
        'ice water mixing ratio'
        'land cover'
        'low cloud cover'
        'surface lifted index'
        'latent heat net flux'
        'middle cloud cover'
        'mean sea level pressure'
        'mslp (eta model reduction)'
        'ozone mixing ratio'
        'potential evaporation rate'
        'pressure level from which parcel was lifted'
        'potential temperature'
        'precipitation rate'
        'pressure'
        'mean sea level pressure'
        'precipitable water'
        'composite reflectivity'
        'reflectivity'
        'relative humidity'
        'rain mixing ratio'
        'surface roughness'
        'sensible heat net flux'
        'snow mixing ratio'
        'snow depth'
        'liquid volumetric soil moisture (non-frozen)'
        'volumetric soil moisture content'
        'soil type'
        'specific humidity'
        'sunshine duration'
        'total cloud cover'
        'maximum temperature'
        'minimum temperature'
        'temperature'
        'total ozone'
        'soil temperature'
        'momentum flux (u-component)'
        'u-component of wind'
        'zonal flux of gravity wave stress'
        'upward longwave radiation flux'
        'u-component of storm motion'
        'upward shortwave radiation flux'
        'vegetation'
        'momentum flux (v-component)'
        'v-component of wind'
        'meridional flux of gravity wave stress'
        'visibility'
        'ventilation rate'
        'v-component of storm motion'
        'vertical velocity (pressure)'
        'vertical speed shear'
        'water runoff'
        'water equivalent of accumulated snow depth'
        'wilting point'          
    
    10) path (String) - Default="GFS0P25/Archive". The local directory where the archived GFS data will be stored. 
    
    11) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    12) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    13) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    14) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    15) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
        
    16) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) Amazon AWS - source='aws'
        2) Google Cloud - source='google'
        
    17) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'mean sea level'
        'hybrid'
        'entire atmosphere'
        'boundary layer'
        'low cloud layer'
        'middle cloud layer'
        'high cloud layer'
        'convective cloud bottom level'
        'low cloud bottom level'
        'middle cloud bottom level'
        'high cloud bottom level'
        'convective cloud top level'
        'low cloud top level'
        'middle cloud top level'
        'high cloud top level'
        'convective cloud layer'
        'tropopause'
        'max wind'
        'isothermal'
        'highest tropospheric freezing level'
        'height above ground'
        'surface'
        'height below ground'
        'sigma layer'
        'sigma level'
        'entire atmosphere (considered as a single layer)'
        'pressure above ground'
        'potential vorticity surface'
        
    18) levels (String, Integer or Float List) - Default=[1000,
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
        
    19) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.
    
    20) netcdf_path (String) - Default='GFS0P25/Archive/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.
    
    21) netcdf_filename (String) - Default='gfs_0p25.nc'. The name of the netCDF (.nc) file. A good practice is to 
        name this netCDF file using the variable name. 
        
    22) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
        new netCDF file. For users who want to archive all data set this to False. 
        
    23) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned.
    
    Returns
    -------
    
    An xarray.array dataset of the most recent GFS0P25 run. 
    
    Post-processed Variable Key List
    --------------------------------
    
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
    'surface_visibility'
    'surface_wind_gust'
    'percent_frozen_precipitation'
    'convective_available_potential_energy'
    'convective_inhibition'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    '2m_dew_point'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'mixed_layer_cape'
    'mixed_layer_cin'
    '3km_helicity'
    
    """
    
    try:
        if process_data == True:
            ds = _gfs_0p25_client(date,
                                  run,
                                  final_forecast_hour=final_forecast_hour, 
                                western_bound=western_bound, 
                                eastern_bound=eastern_bound, 
                                northern_bound=northern_bound, 
                                southern_bound=southern_bound, 
                                step=step,
                                process_data=process_data,
                                proxies=proxies, 
                                variables=variables,
                                path=path,
                                clear_recycle_bin=clear_recycle_bin,
                                convert_temperature=convert_temperature,
                                convert_to=convert_to,
                                chunk_size=chunk_size,
                                notifications=notifications,
                                source=source,
                                level_type=level_type,
                                levels=levels)
        else:
            _gfs_0p25_client(date,
                                run,
                                final_forecast_hour=final_forecast_hour, 
                                western_bound=western_bound, 
                                eastern_bound=eastern_bound, 
                                northern_bound=northern_bound, 
                                southern_bound=southern_bound, 
                                step=step,
                                process_data=process_data,
                                proxies=proxies, 
                                variables=variables,
                                path=path,
                                clear_recycle_bin=clear_recycle_bin,
                                convert_temperature=convert_temperature,
                                convert_to=convert_to,
                                chunk_size=chunk_size,
                                notifications=notifications,
                                source=source,
                                level_type=level_type,
                                levels=levels)
        
    except Exception as e:
        
        print(f"Error: Client lost connection to {source.upper()} Server.")
        
        if source == 'aws':
            print(f"Rotating to Google Cloud server.")
            try:
                if process_data == True:
                    ds = _gfs_0p25_client(date,
                                        run,
                                        final_forecast_hour=final_forecast_hour, 
                                        western_bound=western_bound, 
                                        eastern_bound=eastern_bound, 
                                        northern_bound=northern_bound, 
                                        southern_bound=southern_bound, 
                                        step=step,
                                        process_data=process_data,
                                        proxies=proxies, 
                                        variables=variables,
                                        path=path,
                                        clear_recycle_bin=clear_recycle_bin,
                                        convert_temperature=convert_temperature,
                                        convert_to=convert_to,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        source='google',
                                        level_type=level_type,
                                        levels=levels)
                else:
                    _gfs_0p25_client(date,
                                run,
                                final_forecast_hour=final_forecast_hour, 
                                western_bound=western_bound, 
                                eastern_bound=eastern_bound, 
                                northern_bound=northern_bound, 
                                southern_bound=southern_bound, 
                                step=step,
                                process_data=process_data,
                                proxies=proxies, 
                                variables=variables,
                                path=path,
                                clear_recycle_bin=clear_recycle_bin,
                                convert_temperature=convert_temperature,
                                convert_to=convert_to,
                                chunk_size=chunk_size,
                                notifications=notifications,
                                source='google',
                                level_type=level_type,
                                levels=levels)
            except Exception as e:
                print(f"Error: Client is unable to establish a connection to either server.")
                print(f"Tip: Try double checking the date and run for typos. Data record begins at: {start.strftime('%Y%m%d')} 00z.")
                _version_warning()
                print("System Exit")
                _sys.exit(1)

                
        else:
            print(f"Rotating to AWS server.")
            try:
                if process_data == True:
                    ds = _gfs_0p25_client(date,
                                        run,
                                        final_forecast_hour=final_forecast_hour, 
                                        western_bound=western_bound, 
                                        eastern_bound=eastern_bound, 
                                        northern_bound=northern_bound, 
                                        southern_bound=southern_bound, 
                                        step=step,
                                        process_data=process_data,
                                        proxies=proxies, 
                                        variables=variables,
                                        path=path,
                                        clear_recycle_bin=clear_recycle_bin,
                                        convert_temperature=convert_temperature,
                                        convert_to=convert_to,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        source='aws',
                                        level_type=level_type,
                                        levels=levels)
                else:
                    _gfs_0p25_client(date,
                                run,
                                final_forecast_hour=final_forecast_hour, 
                                western_bound=western_bound, 
                                eastern_bound=eastern_bound, 
                                northern_bound=northern_bound, 
                                southern_bound=southern_bound, 
                                step=step,
                                process_data=process_data,
                                proxies=proxies, 
                                variables=variables,
                                path=path,
                                clear_recycle_bin=clear_recycle_bin,
                                convert_temperature=convert_temperature,
                                convert_to=convert_to,
                                chunk_size=chunk_size,
                                notifications=notifications,
                                source='aws',
                                level_type=level_type,
                                levels=levels)
            except Exception as e:
                print(f"Error: Client is unable to establish a connection to either server.")
                print(f"Tip: Try double checking the date and run for typos. Data record begins at: {start.strftime('%Y%m%d')} 00z.")
                print("System Exit")
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

def gfs_0p50(
            date,
            run,
            path=f"GFS0P50/Archive",
            final_forecast_hour=384, 
            western_bound=-180, 
            eastern_bound=180, 
            northern_bound=90, 
            southern_bound=-90, 
            step=3,
            process_data=True,
            proxies=None, 
            variables=['geopotential height',
                       'temperature',
                       'relative humidity',
                       'u-component of wind',
                       'v-component of wind'],
            clear_recycle_bin=False,
            convert_temperature=True,
            convert_to='celsius',
            chunk_size=8192,
            notifications='off',
            source='aws',
            level_type='pressure',
            levels=[1000,
                    975,
                    950,
                    925,
                    900,
                    850,
                    800,
                    750,
                    700,
                    650,
                    600,
                    550,
                    500,
                    450,
                    400,
                    350,
                    300,
                    250,
                    200,
                    150,
                    100,
                    70,
                    50,
                    40,
                    30,
                    20,
                    15,
                    10,
                    7,
                    5,
                    3,
                    2,
                    1],
            to_netcdf=False,
            netcdf_path=f"GFS0P50/Archive/NETCDF",
            netcdf_filename=f"gfs_0p50.nc",
            delete_previous_netcdf_file=True,
            return_values=True):
    
    """
    This function downloads GFS0P50 data and saves it to a folder. 
    
    Required Arguments:
    
    1) date (String or datetime) - The date of the model run.
    
    2) run (Integer) - The model runtime in UTC (0, 6, 12, 18).
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 6 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. Set to 3 for 3hr increments and 6 for 6hrly increments.
    
    7) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
       
    9) variables (String List) - Default=['geopotential height',
                                            'temperature',
                                            'relative humidity',
                                            'u-component of wind',
                                            'v-component of wind']
                       
        The variables the user wishes to query.
    
        Variables
        ---------
        
        'best lifted index'
        'absolute vorticity'
        'convective precipitation'
        'albedo'
        'total precipitation'
        'convective available potential energy'
        'categorical freezing rain'
        'categorical ice pellets'
        'convective inhibition'
        'cloud mixing ratio'
        'plant canopy surface water'
        'percent frozen precipitaion'
        'convective precipitation rate'
        'categorical rain'
        'categorical snow'
        'cloud water'
        'cloud work function'
        'downward longwave radiation flux'
        'dew point'
        'downward shortwave radiation flux'
        'vertical velocity (height)'
        'field capacity'
        'surface friction velocity'
        'ground heat flux'
        'graupel'
        'wind gust'
        'high cloud cover'
        'geopotential height'
        'haines index'
        'storm relative helicity'
        'planetary boundary layer height'
        'icao standard atmosphere reference height'
        'ice cover'
        'ice growth rate'
        'ice thickness'
        'ice temperature'
        'ice water mixing ratio'
        'land cover'
        'low cloud cover'
        'surface lifted index'
        'latent heat net flux'
        'middle cloud cover'
        'mslp (eta model reduction)'
        'ozone mixing ratio'
        'potential evaporation rate'
        'pressure level from which parcel was lifted'
        'potential temperature'
        'precipitation rate'
        'pressure'
        'mean sea level pressure'
        'precipitable water'
        'composite reflectivity'
        'reflectivity'
        'relative humidity'
        'rain mixing ratio'
        'surface roughness'
        'sensible heat net flux'
        'snow mixing ratio'
        'snow depth'
        'liquid volumetric soil moisture (non-frozen)'
        'volumetric soil moisture content'
        'soil type'
        'specific humidity'
        'sunshine duration'
        'total cloud cover'
        'maximum temperature'
        'minimum temperature'
        'temperature'
        'total ozone'
        'soil temperature'
        'momentum flux (u-component)'
        'u-component of wind'
        'zonal flux of gravity wave stress'
        'upward longwave radiation flux'
        'u-component of storm motion'
        'upward shortwave radiation flux'
        'vegetation'
        'momentum flux (v-component)'
        'v-component of wind'
        'meridional flux of gravity wave stress'
        'visibility'
        'ventilation rate'
        'v-component of storm motion'
        'vertical velocity (pressure)'
        'vertical speed shear'
        'water runoff'
        'water equivalent of accumulated snow depth'
        'wilting point'
        'clear sky uv-b downward solar flux'
        'uv-b downward solar flux'       
    
    10) path (String) - Default="GFS0P25/Archive". The local directory where the archived GFS data will be stored.
    
    11) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    12) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    13) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    14) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    15) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    16) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    17) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'mean sea level'
        'hybrid'
        'entire atmosphere'
        'boundary layer'
        'low cloud layer'
        'middle cloud layer'
        'high cloud layer'
        'convective cloud bottom level'
        'low cloud bottom level'
        'middle cloud bottom level'
        'high cloud bottom level'
        'convective cloud top level'
        'low cloud top level'
        'middle cloud top level'
        'high cloud top level'
        'convective cloud layer'
        'tropopause'
        'max wind'
        'isothermal'
        'highest tropospheric freezing level'
        'height above ground'
        'surface'
        'height below ground'
        'sigma layer'
        'sigma level'
        'entire atmosphere (considered as a single layer)'
        'pressure above ground'
        'potential vorticity surface'
        
        
    18) levels (String, Integer or Float List) - Default=levels=[1000,
                                                                    975,
                                                                    950,
                                                                    925,
                                                                    900,
                                                                    850,
                                                                    800,
                                                                    750,
                                                                    700,
                                                                    650,
                                                                    600,
                                                                    550,
                                                                    500,
                                                                    450,
                                                                    400,
                                                                    350,
                                                                    300,
                                                                    250,
                                                                    200,
                                                                    150,
                                                                    100,
                                                                    70,
                                                                    50,
                                                                    40,
                                                                    30,
                                                                    20,
                                                                    15,
                                                                    10,
                                                                    7,
                                                                    5,
                                                                    3,
                                                                    2,
                                                                    1]
                                                            
        The pressure, height or depth levels.
        
    19) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.
    
    20) netcdf_path (String) - Default='GFS0P50/Archive/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.
    
    21) netcdf_filename (String) - Default='gfs_0p50.nc'. The name of the netCDF (.nc) file. A good practice is to 
        name this netCDF file using the variable name. 
        
    22) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
        new netCDF file. For users who want to archive all data set this to False. 
        
    23) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned.
    
    Returns
    -------
    
    An xarray.array dataset of the most recent GFS0P50 run. 
    
    Post-processed Variable Key List
    --------------------------------
    
    'mslp'
    'mslp_eta_reduction' 
    'cloud_mixing_ratio'
    'ice_water_mixing_ratio' 
    'rain_mixing_ratio'
    'snow_mixing_ratio'
    'graupel'
    'derived_radar_reflectivity'
    'maximum_composite_reflectivity'
    'total_cloud_cover'
    'visibility'
    'wind_gust'
    'haines_index'
    'surface_pressure'
    'orography'
    'temperature'
    'plant_canopy_surface_water'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'percent_frozen_precipitation'
    'precipitation_rate'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'surface_roughness'
    'frictional_velocity'
    'vegetation'
    'soil_type'
    'wilting_point'
    'field_capacity'
    'sunshine_duration'
    'surface_lifted_index'
    'best_4_layer_lifted_index'
    'sea_ice_area_fraction'
    'sea_ice_temperature'
    'geopotential_height'
    'relative_humidity'
    'specific_humidity'
    'vertical_velocity'
    'geometric_vertical_velocity'
    'u_wind_component'
    'v_wind_component'
    'absolute_vorticity'
    'ozone_mixing_ratio'
    'derived_radar_reflectivity'
    '2m_temperature'
    '2m_specific_humidity'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_dew_point_depression'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'pressure'
    '100m_u_wind_component'
    '100m_v_wind_component'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    'liquid_volumetric_soil_moisture_non_frozen'
    'precipitable_water'
    'cloud_water'
    'total_ozone'
    'low_cloud_cover'
    'middle_cloud_cover'
    'high_cloud_cover'
    'storm_relative_helicity'
    'u_component_of_storm_motion'
    'v_component_of_storm_motion'
    'tropopause_pressure'
    'tropopause_standard_atmosphere_reference_height'
    'vertical_speed_shear'
    'convective_available_potential_energy'
    'convective_inhibition'
    'pressure_level_from_which_a_parcel_was_lifted'
    '995_sigma_theta'
    
    """
    
    try:
        if process_data == True:
            ds = _gfs_0p50_client(date,
                                  run,
                                  final_forecast_hour=final_forecast_hour, 
                                western_bound=western_bound, 
                                eastern_bound=eastern_bound, 
                                northern_bound=northern_bound, 
                                southern_bound=southern_bound, 
                                step=step,
                                process_data=process_data,
                                proxies=proxies, 
                                variables=variables,
                                path=path,
                                clear_recycle_bin=clear_recycle_bin,
                                convert_temperature=convert_temperature,
                                convert_to=convert_to,
                                chunk_size=chunk_size,
                                notifications=notifications,
                                source=source,
                                level_type=level_type,
                                levels=levels)
        else:
            _gfs_0p50_client(date,
                                run,
                                final_forecast_hour=final_forecast_hour, 
                                western_bound=western_bound, 
                                eastern_bound=eastern_bound, 
                                northern_bound=northern_bound, 
                                southern_bound=southern_bound, 
                                step=step,
                                process_data=process_data,
                                proxies=proxies, 
                                variables=variables,
                                path=path,
                                clear_recycle_bin=clear_recycle_bin,
                                convert_temperature=convert_temperature,
                                convert_to=convert_to,
                                chunk_size=chunk_size,
                                notifications=notifications,
                                source=source,
                                level_type=level_type,
                                levels=levels)
        
    except Exception as e:
        
        print(f"Error: Client lost connection to {source.upper()} Server.")
        
        if source == 'aws':
            print(f"Rotating to Google Cloud server.")
            try:
                if process_data == True:
                    ds = _gfs_0p50_client(date,
                                        run,
                                        final_forecast_hour=final_forecast_hour, 
                                        western_bound=western_bound, 
                                        eastern_bound=eastern_bound, 
                                        northern_bound=northern_bound, 
                                        southern_bound=southern_bound, 
                                        step=step,
                                        process_data=process_data,
                                        proxies=proxies, 
                                        variables=variables,
                                        path=path,
                                        clear_recycle_bin=clear_recycle_bin,
                                        convert_temperature=convert_temperature,
                                        convert_to=convert_to,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        source='google',
                                        level_type=level_type,
                                        levels=levels)
                else:
                    _gfs_0p50_client(date,
                                run,
                                final_forecast_hour=final_forecast_hour, 
                                western_bound=western_bound, 
                                eastern_bound=eastern_bound, 
                                northern_bound=northern_bound, 
                                southern_bound=southern_bound, 
                                step=step,
                                process_data=process_data,
                                proxies=proxies, 
                                variables=variables,
                                path=path,
                                clear_recycle_bin=clear_recycle_bin,
                                convert_temperature=convert_temperature,
                                convert_to=convert_to,
                                chunk_size=chunk_size,
                                notifications=notifications,
                                source='google',
                                level_type=level_type,
                                levels=levels)
            except Exception as e:
                print(f"Error: Client is unable to establish a connection to either server.")
                print(f"Tip: Try double checking the date and run for typos. Data record begins at: {start.strftime('%Y%m%d')} 00z.")
                _version_warning()
                print("System Exit")
                _sys.exit(1)

                
        else:
            print(f"Rotating to AWS server.")
            try:
                if process_data == True:
                    ds = _gfs_0p50_client(date,
                                        run,
                                        final_forecast_hour=final_forecast_hour, 
                                        western_bound=western_bound, 
                                        eastern_bound=eastern_bound, 
                                        northern_bound=northern_bound, 
                                        southern_bound=southern_bound, 
                                        step=step,
                                        process_data=process_data,
                                        proxies=proxies, 
                                        variables=variables,
                                        path=path,
                                        clear_recycle_bin=clear_recycle_bin,
                                        convert_temperature=convert_temperature,
                                        convert_to=convert_to,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        source='aws',
                                        level_type=level_type,
                                        levels=levels)
                else:
                    _gfs_0p50_client(date,
                                run,
                                final_forecast_hour=final_forecast_hour, 
                                western_bound=western_bound, 
                                eastern_bound=eastern_bound, 
                                northern_bound=northern_bound, 
                                southern_bound=southern_bound, 
                                step=step,
                                process_data=process_data,
                                proxies=proxies, 
                                variables=variables,
                                path=path,
                                clear_recycle_bin=clear_recycle_bin,
                                convert_temperature=convert_temperature,
                                convert_to=convert_to,
                                chunk_size=chunk_size,
                                notifications=notifications,
                                source='aws',
                                level_type=level_type,
                                levels=levels)
            except Exception as e:
                print(f"Error: Client is unable to establish a connection to either server.")
                print(f"Tip: Try double checking the date and run for typos. Data record begins at: {start.strftime('%Y%m%d')} 00z.")
                print("System Exit")
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

def gfs_0p25_secondary_parameters(
            date,
            run,
            path=f"GFS0P25 SECONDARY PARAMETERS/Archive",
            final_forecast_hour=384, 
            western_bound=-180, 
            eastern_bound=180, 
            northern_bound=90, 
            southern_bound=-90, 
            step=3,
            process_data=True,
            proxies=None, 
            variables=['geopotential height',
                       'temperature',
                       'relative humidity',
                       'u-component of wind',
                       'v-component of wind'],
            clear_recycle_bin=False,
            convert_temperature=True,
            convert_to='celsius',
            chunk_size=8192,
            notifications='off',
            source='noaa',
            level_type='pressure',
            levels=[875,
                    825,
                    775,
                    725,
                    675,
                    625,
                    575,
                    525,
                    475,
                    425,
                    375,
                    325,
                    275,
                    225,
                    175,
                    125,
                    7,
                    5,
                    3,
                    2,
                    1],
            to_netcdf=False,
            netcdf_path=f"GFS0P25 SECONDARY PARAMETERS/Archive/NETCDF",
            netcdf_filename=f"gfs_0p25_secondary_parameters.nc",
            delete_previous_netcdf_file=True,
            return_values=True):
    
    """
    This function downloads GFS0P25 SECONDARY PARAMETERS data and saves it to a folder. 
    
    Required Arguments:
    
    1) date (String or datetime) - The date of the model run.
    
    2) run (Integer) - The model runtime in UTC (0, 6, 12, 18).
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GFS0P25
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 6 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. Set to 3 for 3hr increments and 6 for 6hrly increments.
    
    7) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
       
    9) variables (String List) - Default=['geopotential height',
                                            'temperature',
                                            'relative humidity',
                                            'u-component of wind',
                                            'v-component of wind']
                       
        The variables the user wishes to query.
    
        Variables
        ---------
        
        'absolute vorticity'
        'clear sky uv-b downward solar flux'
        'cloud mixing ratio'
        'plant canopy surface water'
        'uv-b downward solar flux'
        'vertical velocity (height)'
        'graupel'
        'geopotential height'
        'ice thickness'
        'ice water mixing ratio'
        'ozone mixing ratio'
        'pressure'
        'relative humidity'
        'rain mixing ratio'
        'snow mixing ratio'
        'liquid volumetric soil moisture (non-frozen)'
        'specific humidity'
        'total cloud cover'
        'temperature'
        'u-component of wind'
        'v-component of wind'
        'vertical velocity (pressure)'
        'vertical speed shear'      
    
    10) path (String) - Default="GFS0P25 SECONDARY PARAMETERS/Archive". The local directory where the archived GFS data will be stored. 
    
    11) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    12) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    13) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    14) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    15) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    16) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    17) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'height below ground'
        'surface'
        'height above ground'
        'height above sea level'
        'pressure above ground'
        'potential vorticity surface'
        
    18) levels (String, Integer or Float List) - Default=[875,
                                                            825,
                                                            775,
                                                            725,
                                                            675,
                                                            625,
                                                            575,
                                                            525,
                                                            475,
                                                            425,
                                                            375,
                                                            325,
                                                            275,
                                                            225,
                                                            175,
                                                            125,
                                                            7,
                                                            5,
                                                            3,
                                                            2,
                                                            1]
                                                            
        The pressure, height or depth levels.
        
    19) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.
    
    20) netcdf_path (String) - Default='GFS0P25 SECONDARY PARAMETERS/Archive/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.
    
    21) netcdf_filename (String) - Default='gfs_0p25_secondary_parameters.nc'. The name of the netCDF (.nc) file. A good practice is to 
        name this netCDF file using the variable name. 
        
    22) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
        new netCDF file. For users who want to archive all data set this to False. 
        
    23) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned.
    
    Returns
    -------
    
    An xarray.array dataset of the most recent GFS0P25 run. 
    
    Post-processed Variable Key List
    --------------------------------
    
    'u_wind_component'
    'v_wind_component'
    'air_temperature'
    'relative_humidity'
    'absolute_vorticity'
    'geopotential_height'
    'ozone_mixing_ratio'
    'total_cloud_cover'
    'cloud_mixing_ratio'
    'ice_water_mixing_ratio'
    'rain_water_mixing_ratio'
    'snow_mixing_ratio'
    'graupel'
    'vertical_velocity'
    'geometric_vertical_velocity'
    'liquid_volumetric_soil_moisture_non_frozen'
    'plant_canopy_surface_water'
    'sea_ice_thickness'
    'temperature_height_above_sea'
    'u_wind_component_height_above_sea'
    'v_wind_component_height_above_sea'
    'mixed_layer_temperature'
    'mixed_layer_relative_humidity'
    'mixed_layer_specific_humidity'
    'mixed_layer_u_wind_component'
    'mixed_layer_v_wind_component'
    'potential_vorticity_level_u_wind_component'
    'potential_vorticity_level_v_wind_component'
    'potential_vorticity_level_temperature'
    'potential_vorticity_level_geopotential_height'
    'potential_vorticity_level_air_pressure'
    'potential_vorticity_level_vertical_speed_shear' 
    
    """
    
    try:
        if process_data == True:
            ds = _gfs_0p25_secondary_parameters_client(date,
                                  run,
                                  final_forecast_hour=final_forecast_hour, 
                                western_bound=western_bound, 
                                eastern_bound=eastern_bound, 
                                northern_bound=northern_bound, 
                                southern_bound=southern_bound, 
                                step=step,
                                process_data=process_data,
                                proxies=proxies, 
                                variables=variables,
                                path=path,
                                clear_recycle_bin=clear_recycle_bin,
                                convert_temperature=convert_temperature,
                                convert_to=convert_to,
                                chunk_size=chunk_size,
                                notifications=notifications,
                                source=source,
                                level_type=level_type,
                                levels=levels)
        else:
            _gfs_0p25_secondary_parameters_client(date,
                                run,
                                final_forecast_hour=final_forecast_hour, 
                                western_bound=western_bound, 
                                eastern_bound=eastern_bound, 
                                northern_bound=northern_bound, 
                                southern_bound=southern_bound, 
                                step=step,
                                process_data=process_data,
                                proxies=proxies, 
                                variables=variables,
                                path=path,
                                clear_recycle_bin=clear_recycle_bin,
                                convert_temperature=convert_temperature,
                                convert_to=convert_to,
                                chunk_size=chunk_size,
                                notifications=notifications,
                                source=source,
                                level_type=level_type,
                                levels=levels)
        
    except Exception as e:
        
        print(f"Error: Client lost connection to {source.upper()} Server.")
        
        if source == 'aws':
            print(f"Rotating to Google Cloud server.")
            try:
                if process_data == True:
                    ds = _gfs_0p25_secondary_parameters_client(date,
                                        run,
                                        final_forecast_hour=final_forecast_hour, 
                                        western_bound=western_bound, 
                                        eastern_bound=eastern_bound, 
                                        northern_bound=northern_bound, 
                                        southern_bound=southern_bound, 
                                        step=step,
                                        process_data=process_data,
                                        proxies=proxies, 
                                        variables=variables,
                                        path=path,
                                        clear_recycle_bin=clear_recycle_bin,
                                        convert_temperature=convert_temperature,
                                        convert_to=convert_to,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        source='google',
                                        level_type=level_type,
                                        levels=levels)
                else:
                    _gfs_0p25_secondary_parameters_client(date,
                                run,
                                final_forecast_hour=final_forecast_hour, 
                                western_bound=western_bound, 
                                eastern_bound=eastern_bound, 
                                northern_bound=northern_bound, 
                                southern_bound=southern_bound, 
                                step=step,
                                process_data=process_data,
                                proxies=proxies, 
                                variables=variables,
                                path=path,
                                clear_recycle_bin=clear_recycle_bin,
                                convert_temperature=convert_temperature,
                                convert_to=convert_to,
                                chunk_size=chunk_size,
                                notifications=notifications,
                                source='google',
                                level_type=level_type,
                                levels=levels)
            except Exception as e:
                print(f"Error: Client is unable to establish a connection to either server.")
                print(f"Tip: Try double checking the date and run for typos. Data record begins at: {start.strftime('%Y%m%d')} 00z.")
                _version_warning()
                print("System Exit")
                _sys.exit(1)

                
        else:
            print(f"Rotating to AWS server.")
            try:
                if process_data == True:
                    ds = _gfs_0p25_secondary_parameters_client(date,
                                        run,
                                        final_forecast_hour=final_forecast_hour, 
                                        western_bound=western_bound, 
                                        eastern_bound=eastern_bound, 
                                        northern_bound=northern_bound, 
                                        southern_bound=southern_bound, 
                                        step=step,
                                        process_data=process_data,
                                        proxies=proxies, 
                                        variables=variables,
                                        path=path,
                                        clear_recycle_bin=clear_recycle_bin,
                                        convert_temperature=convert_temperature,
                                        convert_to=convert_to,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        source='aws',
                                        level_type=level_type,
                                        levels=levels)
                else:
                    _gfs_0p25_secondary_parameters_client(date,
                                run,
                                final_forecast_hour=final_forecast_hour, 
                                western_bound=western_bound, 
                                eastern_bound=eastern_bound, 
                                northern_bound=northern_bound, 
                                southern_bound=southern_bound, 
                                step=step,
                                process_data=process_data,
                                proxies=proxies, 
                                variables=variables,
                                path=path,
                                clear_recycle_bin=clear_recycle_bin,
                                convert_temperature=convert_temperature,
                                convert_to=convert_to,
                                chunk_size=chunk_size,
                                notifications=notifications,
                                source='aws',
                                level_type=level_type,
                                levels=levels)
            except Exception as e:
                print(f"Error: Client is unable to establish a connection to either server.")
                print(f"Tip: Try double checking the date and run for typos. Data record begins at: {start.strftime('%Y%m%d')} 00z.")
                print("System Exit")
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