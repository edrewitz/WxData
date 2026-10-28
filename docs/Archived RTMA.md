---
title: Archived Real-Time Mesoscale Analysis (RTMA)
---
# Archived Real-Time Mesoscale Analysis (RTMA)

```python
def get_archived_rtma(date,
         run,
         model='rtma', 
         cat='analysis',
         path=f"RTMA/Archive", 
         proxies=None,
         process_data=True,
         clear_recycle_bin=False,
         convert_temperature=True,
         convert_to='fahrenheit',
         chunk_size=8192,
         notifications='off',
        to_netcdf=False,
        netcdf_path=f"RTMA/Archive/NETCDF",
        netcdf_filename=f"rtma.nc",
        delete_previous_netcdf_file=True,
        return_values=True):
```

This function downloads the archived RTMA Dataset and returns it as an xarray data array. 

Required Arguments: 

1) date (String or datetime) - The date of the model run.

2) run (Integer) - The model runtime in UTC (0 to 23).

Optional Arguments:

1) model (String) - Default='rtma'. The RTMA model being used:

    ***RTMA Models***
    
    i) CONUS = 'rtma'
    
    ii) Alaska = 'ak rtma'
    
    iii) Hawaii = 'hi rtma'
    
    iv) Puerto Rico = 'pr rtma'
    
    v) Guam = 'gu rtma'

2) cat (String) - Default='analysis'. The category of the RTMA dataset. 

   ***RTMA Categories***

   i) analysis - Latest RTMA Analysis

   ii) error - Latest RTMA Error

   iii) surface 1 hour forecast - RTMA Surface 1 Hour Forecast

3) path (String) - Default='RTMA/Archive'. The local directory where the data will be stored. 

4) proxies (dict or None) - If the user is using a proxy server, the user must change the following:

```python
proxies=None ---> proxies={
                           'http':'http://your-proxy-address:port',
                           'https':'http://your-proxy-address:port'
                           }
```

5) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
   data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
   
6) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
    the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
    This setting is to help preserve memory on the machine. 

7) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
    either Celsius or Fahrenheit. When False, this data remains in Kelvin.
    
8) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
    Set convert_to='fahrenheit' for Fahrenheit. 
            
9) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.

10) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}.
    
11) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.

12) netcdf_path (String) - Default='RTMA/Archive/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.

13) netcdf_filename (String) - Default='rtma.nc'. The name of the netCDF (.nc) file. A good practice is to 
    name this netCDF file using the variable name. 
    
14) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
    new netCDF file. For users who want to archive all data set this to False. 
    
15) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned. 
    
*If the client is unable to connect to the server the user specified, it will rotate to the next server and try to 
    establish a connection there.*

**Returns**

An xarray data array of the RTMA Dataset with variable keys converted from the GRIB format to a Plain Language format. 

***Variable Keys***

```python
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
```
