---
title: WOOF-NAM
---

# WOOF-NAM

```python
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
```

This client retrieves and processes the latest open-source WOOF-NAM CONUS data from Recast Systems.

Required Arguments: None

Optional Arguments:

1) final_forecast_hour (Integer) - Default=84. This affects the length of the forecast the user wants to download.
    Maximum value is 84 as the WOOF-NAM goes out 84 hours.
    
2) path (String) - This is the path of the local directory where the WOOF-NAM data will be saved.

3) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

  ```python
   proxies=None ---> proxies={
                           'http':'http://your-proxy-address:port',
                           'https':'http://your-proxy-address:port'
                           }
  ```
                    
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

    ```python
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
    ```
    
12) variables (String List) - The list of variables at a given level_type for the query.

  ```python
  Default=['geopotential height',
          'absolute vorticity',
          'temperature',
          'relative humidity',
          'vertical velocity (pressure)',
          'vertical velocity (height)',
          'u-component of wind',
          'v-component of wind',
          'turbulent kinetic energy']
  ```
 
  ***Variable List***

  ```python
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
  ```
    
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

```python
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
```
    
13) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.

14) netcdf_path (String) - Default='WOOF-NAM/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.

15) netcdf_filename (String) - Default='woof_nam.nc'. The name of the netCDF (.nc) file. A good practice is to 
    name this netCDF file using the variable name. 
    
16) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
    new netCDF file. For users who want to archive all data set this to False. 
    
17) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned.

**Returns**

An xarray.array of the latest WOOF-NAM CONUS data.    
