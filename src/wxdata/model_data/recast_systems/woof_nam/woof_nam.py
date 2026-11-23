"""
This file hosts the client that downloads WOOF-NAM CONUS data from Recast Systems.

(C) Eric J. Drewitz 2025-2026
"""
import wxdata.client.client as _client
import os as _os
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.post_processors.woof_nam_post_processing import woof_nam_post_processing as _woof_nam_post_processing
from wxdata.model_data.recast_systems.woof_nam.url_scanner import woof_nam_url_scanner as _woof_nam_url_scanner
from wxdata.utils.transforms import grib_to_netcdf as _grib_to_netcdf
from wxdata.utils.warnings import eccodes_warning as _eccodes_warning
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
    This client retrieves and processes the latest open-source WOOF-NAM CONUS data from Recast Systems.
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default=84. This affects the length of the forecast the user wants to download.
        Maximum value is 84 as the WOOF-NAM goes out 84 hours.
        
    2) path (String) - This is the path of the local directory where the WOOF-NAM data will be saved.
    
    3) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    4) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
        
    5) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine.
        
    6) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    7) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed and no values
       returned to the user.
       
    9) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    10) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    11) level_type (String) - The type of level surface for the set of variables.
    
        ***Level Types***
        
        'mean sea level'
        'hybrid'
        'entire atmosphere single layer'
        'surface'
        'boundary layer'
        'pressure'
        'height above ground'
        'depth below land layer'
        'height below ground'
        'lowest level wetbulb zero'
        'isobaric layer'
        'cloud base'
        'height above ground layer (helicity)'
        'height above ground layer (shear)'
        'tropopause'
        'max wind'
        'isothermal'
        'pressure above ground'
        'sigma layer'
        
    12) variables (String List) - The list of variables at a given level_type for the query.
    
        Default=['geopotential height',
                'temperature',
                'relative humidity',
                'vertical velocity (pressure)',
                'vertical velocity (height)',
                'u-component of wind',
                'v-component of wind',
                'turbulent kinetic energy']
                
        ***Variable List***
        
        'mean sea level pressure'
        'reflectivity'
        'composite reflectivity'
        'visibility'
        'geopotential height'
        'u-component of wind'
        'v-component of wind'
        'temperature'
        'ventilation rate'
        'wind gust'
        'radar echo top height'
        'vertical velocity (height)'
        'relative humidity'
        'specific humidity'
        'vertical velocity (pressure)'
        'turbulent kinetic energy'
        'mslp (eta model reduction)'
        'soil temperature'
        'volumetric soil moisture content'
        'liquid volumetric soil moisture (non-frozen)'
        'soil moisture content'
        'soil porosity'
        'number of soil layers'
        'haines index'
        'absolute vorticity'
        'moisture availability'
        'plant canopy surface water'
        'water equivalent of accumulated snow depth'
        'snow cover'
        'snow depth'
        'direct evaporation cease'
        'dew point'
        'total precipitation'
        'convective precipitation'
        'water equivalent of accumulated snow depth'
        'categorical snow'
        'categorical ice pellets'
        'categorical freezing rain'
        'categorical rain'
        'surface roughness'
        'surface friction velocity'
        'drag coefficient'
        'vegetation'
        'vegetation type'
        'wilting point'
        'transpiration stress onset'
        'surface lifted index'
        'best lifted index'
        'convective available potential energy'
        'convective inhibition'
        'storm relative helicity'
        'vertical shear u-component'
        'vertical shear v-component'
        'pressure'
        'parcel lifted index (to 500mb)'
        'planetary boundary layer height'
        'land cover'
        'ice cover'
        'albedo'
        'sensible heat net flux'
        'latent heat net flux'
        'total cloud cover'
        'downward shortwave radiation flux'
        'downward longwave radiation flux'
        'upward shortwave radiation flux'
        'upward longwave radiation flux'
        
    13) levels (String, Integer or Float List) - Default=[1000,
                                                        925,
                                                        850,
                                                        700,
                                                        500,
                                                        300,
                                                        250,
                                                        100,
                                                        50]
                                                        
        ***Available Levels***
        
        level_type="pressure":
            (hPa) [1000, 975, 925, 900, 875, 850, 825, 800, 775, 750, 725, 700, 675, 650, 625, 600,
            575, 550, 525, 500, 475, 450, 425, 400, 375, 350, 325, 300, 375, 250, 225, 200,
            175, 150, 125, 100, 75, 50, 20, 10, 5]
            
        level_type="height above ground":
            (m) [2, 10, 80, 1000, 4000]
            
        level_type="depth below land layer":
            (m) [0-0.1, 0.1-0.4, 0.4-1, 1-2, 0-1, 0-2]
            
        level_type="height below ground":
            (m) [3]
            
        level_type="pressure above ground":
            (hPa) [30-0, 60-30, 90-60, 120-90, 150-120, 180-150, 180-0]
            
        level_type="sigma layer":
            (sigma) [0.33-1]
            
        level_type="hybrid":
            (hybrid) [1]
        
    14) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.
    
    15) netcdf_path (String) - Default='WOOF-NAM/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.
    
    16) netcdf_filename (String) - Default='woof_nam.nc'. The name of the netCDF (.nc) file. A good practice is to 
        name this netCDF file using the variable name. 
        
    17) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
        new netCDF file. For users who want to archive all data set this to False. 
        
    18) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned.
    
    **Returns**
    
    An xarray.array of the latest WOOF-NAM CONUS data.    
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
