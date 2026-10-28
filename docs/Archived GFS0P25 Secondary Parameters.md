---
title: Archived GFS0P25 Secondary Parameters & Levels
---
# Archived Global Forecast System (GFS) 0.25x0.25 Degree Secondary Parameters & Levels

```python
def get_archived_gfs_0p25_secondary_parameters(
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
```

This function downloads archived GFS0P25 SECONDARY PARAMETERS data and saves it to a folder. 

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

   ```python
   proxies=None ---> proxies={
                           'http':'http://your-proxy-address:port',
                           'https':'http://your-proxy-address:port'
                           }
   ```

9) variables (String List) - Default=['geopotential height',
                                        'temperature',
                                        'relative humidity',
                                        'u-component of wind',
                                        'v-component of wind']
                   
    The variables the user wishes to query.

  ***Variables***

  ```python
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
  ```     

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

    ***Server List***
    
    i) Google Cloud - `source='google'`
    
    ii) Amazon AWS - `source='aws'`
    
    *If the client is unable to connect to the server the user specified, it will rotate to the next server and try to 
    establish a connection there.*
    
17) level_type (String) - Default='pressure'. The type of level for the variable.

  ***Level Types***

  ```python
  'pressure'
  'height below ground'
  'surface'
  'height above ground'
  'height above sea level'
  'pressure above ground'
  'potential vorticity surface'
  ```
    
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

**Returns**

An xarray.array dataset of the most recent GFS0P25 run. 

***Post-processed Variable Key List***

```python
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
```
