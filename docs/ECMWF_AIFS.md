---
title: ECMWF AIFS
---
[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)
# ECMWF AIFS

```python
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
                    level_type='pressure',
                    clear_data=False,
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
                to_netcdf=False,
                netcdf_path=f"ECMWF AIFS/NETCDF",
                netcdf_filename=f"ecmwf_aifs.nc",
                delete_previous_netcdf_file=True,
                return_values=True):
```
This function is the main client that downloads and processes ECMWF AIFS data. 

***This client can do the following:***

1) Download ECMWF AIFS data from ECMWF Open-Data, Amazon Web Services and Google Cloud servers.

2) Query your download by downloading only the variables and levels needed. 

3) Subset the GRIB data into a user-specified bounding box and decode the GRIB2 keys into plain-language.

4) Convert temperature fields to user-specified units (Kelvin -> Celsius & Kelvin -> Fahrenheit)

5) Convert the xarray.array of decoded GRIB2 data into a NETCDF (.nc) file. 

6) Manages the ECMWF AIFS files in the local directory.    

7) Handle user-specified proxy-server protocol - Useful for users working on VPN connections and behind firewalls.  

8) Automatically Rotate between ECMWF Open-Data, Amazon Web Services and Google Cloud in the event of significant server connection issues.

9) Validates the download and helps the user troubleshoot if needed. 

These ECMWF end-to-end clients can download ECMWF data from the following sources: 

    i) ECMWF Open-Data Server
    
    ii) Amazon AWS Server
    
    iii) Google Cloud Server
        
***If the server of your choice is down, the client will rotate to another one and try scanning for data and downloading there.***
***If the client cannot connect to any of the servers, the system will exit.***

1) final_forecast_hour (Integer) - Default = 360. The maximum forecast hour. 
    
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
   
8) clear_recycle_bin (Boolean) - (Default=False). Set to True to clear your recycle bin. 
    
9) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
    either Celsius or Fahrenheit. When False, this data remains in Kelvin.
    
10) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
    Set convert_to='fahrenheit' for Fahrenheit. 
    
11) custom_directory (String or None) - Default=None. The directory path where the ECMWF AIFS files will be saved to. 
    When set to None, the path will be: "ECMWF/AIFS/DETERMINISTIC/"

12) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}

13) source (String) - Default='ecmwf'. The data server choice. 

    ***Data Sources***
    
     i) ECMWF Open-Data Server = 'ecmwf'
     
     i) Amazon AWS Server = 'aws'
      
     iii) Google Cloud Server = 'google'
   
    *If the client is unable to connect to the server the user specified, it will rotate to the next server and try to 
    establish a connection there.*
    
14) level_type (String) - Default='pressure'. The level of the parameters being queried. 

    ***level_types***
    
    i) 'surface'
    
    ii) 'pressure'
    
    iii) 'soil

15) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
    When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
16) variables (String List) - Default=['geopotential height',
                                        'specific humidity',
                                        'relative humidity',
                                        'temperature',
                                        'u-wind component',
                                        'v-wind component']. 
                            
    The list of variable names in plain-language. 

    ***Variables***

    ```python
    'geopotential'
    'total column water'
    'mean sea level pressure'
    'standard deviation of sub-gridscale orography'
    'slope of sub-gridscale orography'
    '10-meter u-wind component'
    '10-meter v-wind component'
    '2-meter temperature'
    '2-meter dew point'
    'surface shortwave radiation downward'
    'land sea mask'
    'surface longwave radiation downward'
    'low cloud cover'
    'mid-level cloud cover'
    'high cloud cover'
    'runoff water equivalent'
    'convective precipitation'
    'snowfall water equivalent'
    'total cloud cover'
    'total precipitation'
    '100-meter u-wind component'
    '100-meter v-wind component'
    'skin temperature'
    'surface pressure'
    'specific humidity'
    'relative humidity'
    'temperature'
    'u-wind component'
    'v-wind component'
    'vertical velocity'
    'volumetric soil moisture content'
    'soil temperature'
    ```
    
17) levels (Integer List or None) - Default=[1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50]. 
    When level_type='pressure', this is the list of the pressure levels. 
    
    Example: User wants only the 500 mb level: levels=[500]
    
18) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.

19) netcdf_path (String) - Default='ECMWF AIFS/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.

20) netcdf_filename (String) - Default='ecmwf_aifs.nc'. The name of the netCDF (.nc) file. A good practice is to 
    name this netCDF file using the variable name. 
    
21) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
    new netCDF file. For users who want to archive all data set this to False. 
    
22) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned. 
    
**Returns**

An xarray data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys

***Plain Language ECMWF AIFS Variable Keys (After Post-Processing)***

```python
'volumetric_soil_moisture_content'
'soil_temperature'
'geopotential'
'specific_humidity'
'u_wind_component'
'v_wind_component'
'air_temperature'
'vertical velocity'
'100m_u_wind_component'
'100m_v_wind_component'
'10m_u_wind_component'
'10m_v_wind_component'
'2m_temperature'
'2m_dew_point'
'2m_relative_humidity'
'2m_dew_point_depression'
'water_runoff' 
'surface_geopotential_height'
'skin_temperature'
'surface_pressure'
'standard_deviation_of_sub_gridscale_orography'
'slope_of_sub_gridscale_orography'
'surface_shortwave_radiation_downward'
'land_sea_mask'
'surface_longwave_radiation_downward'
'convective_precipitation'
'snowfall_water_equivalent'
'total_precipitation'
'low_cloud_cover'
'middle_cloud_cover'
'high_cloud_cover'
'total_column_water'
'total_cloud_cover'
'mslp'
```
