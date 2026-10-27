---
title: National Weather Service Gridded Forecast (NDFD)
---
# National Weather Service Gridded Forecast (NDFD)

```python
def get_ndfd_grids(parameter, 
                    state,
                    proxies=None,
                    chunk_size=8192,
                    notifications='on',
                    clear_recycle_bin=False,
                    include_extended_grids=True,
                    source='noaa',
                    return_values=True):
```
This function retrieves the latest NWS Forecast (NDFD) files from the NWS FTP Server. 

Data Source: NOAA/NWS/NDFD (tgftp.nws.noaa.gov)

Required Arguments: 

1) parameter (String) - The parameter that the user wishes to download. 

2) state (String) - The two letter state identifier (US States).

Optional Arguments:

1) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

```python
proxies=None ---> proxies={
                           'http':'http://your-proxy-address:port',
                           'https':'http://your-proxy-address:port'
                           }
```

2) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.

3) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}

4) clear_recycle_bin (Boolean) - (Default=False). Set to True to clear your recycle bin. 
  
5) include_extended_grids (Boolean) - Default=True. Most NOAA/NWS products have extended grids. However, SPC products do not have extended grids.
  When downloading SPC plots or if the user does not wish to include the extended grids, set include_extended_grids=False.
  
6) source (String) - Default='noaa'. The data server the user wants to connect the client to.

  ***Server List***
  
  i) NOAA/NWS/FTP - `source='noaa'`
  
  ii) Amazon AWS - `source='aws'`
          
  *If the client is unable to connect to the server the user specified, it will rotate to the next server and try to 
  establish a connection there.*
  
7) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned. 
  
***Parameters***

```python
'maximum_relative_humidity'
'mainimum_relative_humidity'
'maximum_temperature'
'minimum_temperature'
'relative_humidity'
'temperature'
'apparent_temperature'
'wind_speed'
'wind_gust'
'wind_direction'
'spc_critical_fire_weather_forecast'
'spc_dry_lightning_forecast'
'spc_convective_outlook'
'ice_accumulation'
'probability_of_hail'
'12_hour_probability_of_precipitation'
'probability_of_extreme_tornadoes'
'total_probability_of_severe_thunderstorms'
'total_probability_of_extreme_severe_thunderstorms'
'probability_of_extreme_thunderstorm_winds'
'probability_of_extreme_hail'
'probability_of_extreme_tornadoes'
'probability_of_damaging_thunderstorm_winds'
'quantitative_precipitation_forecast'
'sky_cover'
'snow_amount'
'snow_level'
'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_cumulative'
'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_incremental'
'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_cumulative'
'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_incremental'
'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_cumulative'
'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_incremental'
'dew_point'
'visibility'
'significant_wave_height'
'warnings'
'weather'
```

**Returns**

An xarray.data array of the latest NWS/SPC Forecast data.

Variable names are also changed from their origional key value into plain language.

  ***Plain Language Variable Key List***

  ```python
  'maximum_relative_humidity'
  'mainimum_relative_humidity'
  'maximum_temperature'
  'minimum_temperature'
  'relative_humidity'
  'temperature'
  'apparent_temperature'
  'wind_speed'
  'wind_gust'
  'wind_direction'
  'spc_critical_fire_weather_forecast'
  'spc_dry_lightning_forecast'
  'spc_convective_outlook'
  'ice_accumulation'
  'probability_of_hail'
  '12_hour_probability_of_precipitation'
  'probability_of_extreme_tornadoes'
  'total_probability_of_severe_thunderstorms'
  'total_probability_of_extreme_severe_thunderstorms'
  'probability_of_extreme_thunderstorm_winds'
  'probability_of_extreme_hail'
  'probability_of_extreme_tornadoes'
  'probability_of_damaging_thunderstorm_winds'
  'quantitative_precipitation_forecast'
  'sky_cover'
  'snow_amount'
  'snow_level'
  'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_cumulative'
  'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_incremental'
  'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_cumulative'
  'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_incremental'
  'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_cumulative'
  'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_incremental'
  'dew_point'
  'visibility'
  'significant_wave_height'
  'warnings'
  'weather'
```  
