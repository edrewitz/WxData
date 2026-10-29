---
title: Climate Forecast System (CFS) Pressure
---
# Climate Forecast System (CFS) Pressure
```python
def cfs_pressure(western_bound=-180, 
            eastern_bound=180, 
            northern_bound=90, 
            southern_bound=-90, 
            final_forecast_hour=720,
            proxies=None, 
            clear_recycle_bin=False,
            clear_data=False,
            chunk_size=8192,
            notifications='off',
            path=f"CFS/PRESSURE",
            process_data=True,
            convert_temperature=True,
            convert_to='celsius',
            source='aws',
            level_type='pressure',
            variable=['geopotential height'],
            levels=[1000, 
                    925, 
                    850, 
                    700, 
                    500, 
                    300, 
                    250],
            to_netcdf=False,
            netcdf_path=f"CFS PRESSURE/NETCDF",
            netcdf_filename=f"cfs_pressure.nc",
            delete_previous_netcdf_file=True,
            return_values=True):
```
This function is an end-to-end client that downloads, pre-processes, post-processes CFS Pressure data.
Post-processing remaps the variable keys from the coded GRIB format into a decoded Plain-Language Format

Required Arguments: None.

Optional Arguments:

1) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

2) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

3) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

4) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

5) final_forecast_hour (Integer) - Default=720 (30-Days). The last forecast timestep the user wishes to download.
The CFS outputs 6 hourly data for the span of several months. Note that if the user wishes to download
6 hourly data for several months, processing times may be long. Must be a multiple of 6. 

6) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

```python
proxies=None ---> proxies={
                        'http':'http://your-proxy-address:port',
                        'https':'http://your-proxy-address:port'
                        }
```

7) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be 
deleted with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 

8) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 

9) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.

10) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}

11) path (String) - Default="CFS/PRESSURE". The path of the local directory where the files will be stored.

12) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
data via their own external method, set process_data=False which means the data will be downloaded but not processed. 

13) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
either Celsius or Fahrenheit. When False, this data remains in Kelvin.

14) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
Set convert_to='fahrenheit' for Fahrenheit. 

15) source (String) - Default='aws'. The servers to pull the data from.

***Server Choices***

i) NOAA/NCEP/NOMADS - `source='noaa'`

ii) Amazon AWS - `source='aws'`

*If the client is unable to connect to the server the user specified, it will rotate to the next server and try to 
establish a connection there.*

16) level_type (String) - Default='pressure'. The type of vertical coordinates for the list of variables.

***Level Types***

```python
'pressure'
'surface'
'height above ground'
'entire atmosphere'
'mean sea level'
'tropopause'
'height above sea level'
'isothermal'
'highest tropospheric freezing level'
'pressure above ground'
'sigma layer'
'sigma level'
'potential vorticity surface'
```

17) variable (String) - Default=['geopotential height'].

The variable the user selects to download.

***Variable Name List for CFS Pressure Data***

```python
'best lifted index'
'5 wave geopotential height anomaly'
'5 wave geopotential height'
'absolute vorticity'
'convective precipitation'
'total precipitation'
'convective available potential energy'
'categorical freezing rain'
'categorical ice pellets'
'convective inhibition'
'cloud mixing ratio'
'categorical rain'
'categorical snow'
'cloud water'
'dew point'
'geopotential height anomaly'
'geopotential height'
'storm relative helicity'
'surface lifted index'
'large scale non-convective precipitation'
'ozone mixing ratio'
'parcel lifted index (to 500mb)'
'potential temperature'
'pressure'
'mean sea level pressure'
'precipitable water'
'relative humidity'
'specific humidity'
'stream function'
'temperature'
'total ozone'
'u-component of wind'
'u-component of storm motion'
'v-component of wind'
'velocity potential'
'v-component of storm motion'
'vertical velocity (pressure)'
'vertical speed shear'
```

18) levels (Integer List) - Default=[1000, 925, 850, 700, 500, 300, 250]

***Available Levels***

1000
975
925
900
875
850
825
800
775
750
700
650
600
550
500
450
400
350
300
250
225
200
175
150
125
100
70
50
30
20
10
7
5
3
2
1

19) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.

20) netcdf_path (String) - Default='CFS PRESSURE/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.

21) netcdf_filename (String) - Default='cfs_pressure.nc'. The name of the netCDF (.nc) file. A good practice is to 
name this netCDF file using the variable name. 

22) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
new netCDF file. For users who want to archive all data set this to False. 

23) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned. 

**Returns**

A post-processes xarray.array where the GRIB variable keys are decoded into a plain-language format.

***CFS Pressure Data Variables In Plain-Language Format***

```python
'mslp'
'geopotential_height'
'air_temperature'
'relative_humidity'
'specific_humidity'
'vertical_velocity'
'u_wind_component'
'v_wind_component'
'absolute_vorticity'
'ozone_mixing_ratio'
'stream_function'
'velocity_potential'
'5_wave_geopotential_height'
'geopotential_height_anomaly'
'5_wave_geopotential_height_anomaly'
'2m_dew_point'
'2m_relative_humidity'
'total_precipitation'
'total_convective_precipitation'
'total_non_convective_precipitation'
'categorical_snow'
'categorical_ice_pellets'
'categorical_freezing_rain'
'categorical_rain'
'surface_lifted_index'
'best_4_layer_lifted_index'
'surface_cape'
'surface_cin'
'cloud_water'
'entire_atmosphere_relative_humidity'
'total_ozone'
'storm_relative_helicity'
'u_component_of_storm_motion'
'v_component_of_storm_motion'
'tropopause_pressure'
'tropopause_height'
'tropopause_u_wind_component'
'tropopause_v_wind_component'
'tropopause_temperature'
'tropopause_vertical_speed_shear'
'max_wind_u_component'
'max_wind_v_component'
'max_wind_geopotential_height'
'max_wind_pressure'
'max_wind_temperature'
'temperature_height_above_sea'
'u_wind_component_height_above_sea'
'v_wind_component_height_above_sea'
'zero_deg_c_isotherm_geopotential_height'
'zero_deg_c_isotherm_relative_humidity'
'highest_tropospheric_freezing_level_geopotential_height'
'highest_tropospheric_freezing_level_relative_humidity'
'mixed_layer_temperature'
'mixed_layer_relative_humidity'
'mixed_layer_specific_humidity'
'mixed_layer_u_wind_component'
'mixed_layer_v_wind_component'
'mixed_layer_dew_point'
'mixed_layer_precipitable_water'
'parcel_lifted_index'
'mixed_layer_cape'
'mixed_layer_cin'
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
```      
