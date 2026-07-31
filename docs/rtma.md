---
title: Real-Time Mesoscale Analysis (RTMA)
---
[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)
# Real-Time Mesoscale Analysis (RTMA)
```python
def rtma(model='rtma', 
         cat='analysis', 
         proxies=None,
         process_data=True,
         clear_recycle_bin=False,
         convert_temperature=True,
         convert_to='fahrenheit',
         custom_directory=None,
         clear_data=False,
         chunk_size=8192,
         notifications='off',
         source='noaa'):
```

This function downloads the latest RTMA Dataset and returns it as an xarray data array. 

Required Arguments: None

Optional Arguments:

1) model (String) - Default='rtma'. The RTMA model being used:

         RTMA Models
         -----------
         
         CONUS = 'rtma'
         Alaska = 'ak rtma'
         Hawaii = 'hi rtma'
         Puerto Rico = 'pr rtma'
         Guam = 'gu rtma'

2) cat (String) - Default='analysis'. The category of the RTMA dataset. 

         RTMA Categories
         ---------------
         
         analysis - Latest RTMA Analysis
         error - Latest RTMA Error
         surface 1 hour forecast - RTMA Surface 1 Hour Forecast

3) proxies (dict or None) - If the user is using a proxy server, the user must change the following:
```python
proxies=None ---> proxies={
                      'http':'http://your-proxy-address:port',
                      'https':'http://your-proxy-address:port'
                      }
```               
4) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
data via their own external method, set process_data=False which means the data will be downloaded but not processed. 

5) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
This setting is to help preserve memory on the machine. 

6) clear_data (Boolean) - Default=False. When set to True, the current data in the folder is deleted
and new data is downloaded automatically with each run. 

7) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
either Celsius or Fahrenheit. When False, this data remains in Kelvin.

8) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
Set convert_to='fahrenheit' for Fahrenheit. 

9) custom_directory (String or None) - Default=None. The directory path where the RTMA files will be saved to.

10) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.

11) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}.

12) source (String) - Default='noaa'. The data server the client will try first.

         Server List
         -----------
         
         1) NCEP/NOMADS - source='noaa'
         2) Amazon AWS - source='aws'

***If the client is unable to connect to the server the user specified, it will rotate to the next server and try to 
establish a connection there.***

**Returns**

An xarray data array of the RTMA Dataset with variable keys converted from the GRIB format to a Plain Language format. 
    
    Variable Keys
    -------------
    
    'orography'
    'surface_pressure'
    '2m_temperature'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_specific_humidity'
    'surface_visibility'
    'cloud_ceiling_height'
    'total_cloud_cover'
    '10m_u_wind_component'
    '10m_v_wind_component'
    '10m_wind_direction'
    '10m_wind_speed'
    '10m_wind_gust'
    '2m_apparent_temperature'
    '2m_dew_point_depression'
