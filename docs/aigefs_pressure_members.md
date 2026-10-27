---
title: AIGEFS Members (Pressure Parameters)
---
[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)

# AIGEFS Members (Pressure Parameters)
```python
def aigefs_pressure_members(final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             members=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
            process_data=True,
            clear_recycle_bin=False,
            convert_temperature=True,
            convert_to='celsius',
            custom_directory=None,
            chunk_size=8192,
            notifications='off',
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
            netcdf_path=f"AIGEFS PRESSURE MEMBERS/NETCDF",
            netcdf_filename=f"aigefs_pressure_members.nc",
            delete_previous_netcdf_file=True,
            return_values=True):
```

This function downloads, pre-processes and post-processes the latest pressure parameter dataset of the AIGEFS and bins the files to specific folders based on ensemble number.
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

7) members (List) - Default=All 30 ensemble members + control. The individual ensemble members. There are 30 members in this ensemble.  

8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
   data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
   
9) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
    the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
    This setting is to help preserve memory on the machine. 
        
10) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
    the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
    be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.

11) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
    of the program you are calling WxData. This setting is to help preserve memory on the machine. 
    
12) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
    either Celsius or Fahrenheit. When False, this data remains in Kelvin.
    
13) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
    Set convert_to='fahrenheit' for Fahrenheit. 
    
14) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.

16) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}

15) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
    When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
16) variables (String List) Default=['geopotential height',
                                    'specific humidity',
                                    'temperature',
                                    'u-component of wind',
                                    'v-component of wind',
                                    'vertical velocity (pressure)']
                   
    
17) levels (Integer List) - Default=[1000,
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
                                    
18) source (String) - Default='noaa'. The servers to pull the data from.

  ***Server Choices***
  
  i) NOAA/NCEP/NOMADS - `source='noaa'`
  
  ii) Amazon AWS - `source='aws'`
            
*If the client is unable to connect to the server the user specified, it will rotate to the next server and try to 
establish a connection there.*

19) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.

20) netcdf_path (String) - Default='AIGEFS PRESSURE MEMBERS/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.

21) netcdf_filename (String) - Default='aigefs_pressure_members.nc'. The name of the netCDF (.nc) file. A good practice is to 
    name this netCDF file using the variable name. 
    
22) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
    new netCDF file. For users who want to archive all data set this to False. 
    
23) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned. 

**Returns**

An xarray data array of the AIGEFS Pressure Parameter data specified to the coordinate boundaries and variable list the user specifies. 

***Pressure-Level Plain Language Variable Keys***

```python
'geopotential_height'
'specific_humidity'
'air_temperature'
'u_wind_component'
'v_wind_component'
'vertical_velocity'
```
