---
title: Real-Time Mesoscale Analysis (RTMA) Comparison
---
[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)
# Real-Time Mesoscale Analysis (RTMA) Comparison
```python
def rtma_comparison(model='rtma', 
         cat='analysis', 
         hours=24,
         proxies=None,
         process_data=True,
         clear_recycle_bin=False,
         clear_data=False,
         convert_temperature=True,
         convert_to='fahrenheit',
         custom_directory=None,
         chunk_size=8192,
         notifications='off',
         source='noaa',
        to_netcdf=False,
        netcdf_path=f"RTMA COMPARISON/NETCDF",
        netcdf_filename_1=f"rtma_data_1.nc",
        netcdf_filename_2=f"rtma_data_2.nc",
        delete_previous_netcdf_file=True,
        return_values=True):
```
This function downloads the latest RTMA Dataset and the RTMA dataset from 24 hours prior to the current RTMA dataset and returns it as two xarray data arrays. 

Required Arguments: None

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

3) hours (Integer) - Default=24. The amount of hours previous to the current dataset for the comparison dataset. 

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

7) clear_data (Boolean) - Default=False. When set to True, the current data in the folder is deleted
and new data is downloaded automatically with each run. 
This setting is recommended for users who wish to use a medley of different comparisons. 

8) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
either Celsius or Fahrenheit. When False, this data remains in Kelvin.

9) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
Set convert_to='fahrenheit' for Fahrenheit. 

10 custom_directory (String or None) - Default=None. The directory path where the RTMA files will be saved to.

11) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.

12) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}

13) source (String) - Default='noaa'. The data server the client will try first.

***Server List***

i) NCEP/NOMADS - `source='noaa'`

ii) Amazon AWS - `source='aws'`

*If the client is unable to connect to the server the user specified, it will rotate to the next server and try to 
establish a connection there.*

14) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.

15) netcdf_path (String) - Default='RTMA/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.

16) netcdf_filename_1 (String) - Default='rtma_data_1.nc'. The name of the first netCDF (.nc) file. 

17) netcdf_filename_2 (String) - Default='rtma_data_2.nc'. The name of the second (comparison) netCDF (.nc) file. 

18) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
new netCDF file. For users who want to archive all data set this to False. 

19) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned. 

**Returns**

1) ds - The current RTMA dataset

2) ds_dt - The RTMA comparison dataset from a user specified amount of hours prior to the current dataset. 

All with variable keys converted from the GRIB format to a Plain Language format. 

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
