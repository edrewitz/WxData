---
title: AIGFS
---
# AIGFS

```python
def aigfs(final_forecast_hour=384, 
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
             chunk_size=8192,
             notifications='off',
             level_type='pressure',
             clear_data=False,
            variables=['geopotential height',
                       'specific humidity',
                       'temperature',
                       'u-component of wind',
                       'v-component of wind',
                       'vertical velocity (pressure)'],
            levels=[1000,
                    925,
                    850,
                    700,
                    600,
                    500,
                    400,
                    300,
                    250,
                    150,
                    100,
                    50],
            source='noaa',
            to_netcdf=False,
            netcdf_path=f"AIGFS/NETCDF",
            netcdf_filename=f"aigfs.nc",
            delete_previous_netcdf_file=True,
            return_values=True):
```

This function downloads, pre-processes and post-processes the latest AIGFS Data. 
Users can also enter a list of paths for custom_directory if they do not wish to use the default directory.

Required Arguments: None

Optional Arguments:

1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The AIGEFS
goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
384 by the nereast increment of 6 hours. 

2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

6) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

  ```python
   proxies=None ---> proxies={
                           'http':'http://your-proxy-address:port',
                           'https':'http://your-proxy-address:port'
                           }
  ```

7) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
   data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
   
8) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
    of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
9) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
    the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
    be used. 

10) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
    the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
    This setting is to help preserve memory on the machine. 
    
11) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
    either Celsius or Fahrenheit. When False, this data remains in Kelvin.
    
12) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
    Set convert_to='fahrenheit' for Fahrenheit. 
    
13) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.

14) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}

15) level_type (String) - Default='pressure'. The type of level the data is in.

    ***Types of Levels***
    
    1) pressure
    
    2) surface

16) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
    When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
17) variables (String List) **level_type='pressure'** - Default=['geopotential height',
                                                                    'specific humidity',
                                                                    'temperature',
                                                                    'u-component of wind',
                                                                    'v-component of wind',
                                                                    'vertical velocity (pressure)']
                   
    When the level_type = 'pressure', the user can filter by variable to the variable they want. (Surface level files are very small 
    compared to pressure level files).
    
18) levels (Integer List) **level_type='pressure'** - Default=[1000,
                                                                    925,
                                                                    850,
                                                                    700,
                                                                    600,
                                                                    500,
                                                                    400,
                                                                    300,
                                                                    250,
                                                                    150,
                                                                    100,
                                                                    50]
                                                                    
    When the level_type = 'pressure', the user can filter by level to the level they want. (Surface level files are very small 
    compared to pressure level files).
    
19) source (String) - Default='noaa'. The servers to pull the data from.

    ***Server Choices***
    
    i) NOAA/NCEP/NOMADS - `source='noaa'`
    
    ii) Amazon AWS - `source='aws'`
    
    *If the client is unable to connect to the server the user specified, it will rotate to the next server and try to 
    establish a connection there.*
    
20) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.

21) netcdf_path (String) - Default='AIGFS/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.

22) netcdf_filename (String) - Default='aigfs.nc'. The name of the netCDF (.nc) file. A good practice is to 
    name this netCDF file using the variable name. 
    
23) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
    new netCDF file. For users who want to archive all data set this to False. 
    
24) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned. 

**Returns**

An xarray data array of the AIGEFS data specified to the coordinate boundaries and variable list the user specifies. 

***Pressure-Level Plain Language Variable Keys***

```python
'geopotential_height'
'specific_humidity'
'air_temperature'
'u_wind_component'
'v_wind_component'
'vertical_velocity'
```

***Surface-Level Plain Language Variable Keys***

```python
'10m_u_wind_component'
'10m_v_wind_component'
'mslp'
'2m_temperature'
```
