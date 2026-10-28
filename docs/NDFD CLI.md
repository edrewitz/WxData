---
title: NDFD CLI
---

# NOAA/NWS NDFD Grids Command Line Interface
    
***Valid Commands***

-v = Variable. 

Select the variable you would like to download.

***Variables***

maximum_relative_humidity

mainimum_relative_humidity

maximum_temperature

minimum_temperature

relative_humidity

temperature

apparent_temperature

wind_speed

wind_gust

wind_direction

spc_critical_fire_weather_forecast

spc_dry_lightning_forecast

spc_convective_outlook

ice_accumulation

probability_of_hail

12_hour_probability_of_precipitation

probability_of_extreme_tornadoes

total_probability_of_severe_thunderstorms

total_probability_of_extreme_severe_thunderstorms

probability_of_extreme_thunderstorm_winds

probability_of_extreme_hail

probability_of_extreme_tornadoes

probability_of_damaging_thunderstorm_winds

quantitative_precipitation_forecast

sky_cover

snow_amount

snow_level

probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_cumulative

probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_incremental

probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_cumulative

probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_incremental

probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_cumulative

probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_incremental

dew_point

visibility

significant_wave_height

warnings

weather  

-r = Region. 

This is the region the data is in.
    
Use the 2-letter state identifier or use conus for CONUS.

Defaults to CONUS.

-s = Source. 

Default=noaa which is for NOAA/NWS/FTP - set to aws to switch to Amazon Web Services.

-cr = Clear Recycle Bin. (Default=False)

To clear your recycle bin with each run of the script set to True.

-e = Include Extended Forecast Grids. (Default=True)

Set to True to include the grids for the extended forecast. 
    
Set to False for SPC Outlooks where there are no external forecast grids. 

-n = Notifications. (Default="on")

Set to "on" to recieve notifications about your download. 
    
To turn off set -n off

--proxy = Proxy URL (e.g., `https://proxy-address:proxy-port`). Default: no proxy.

***Examples***

1) Download the maximum temperature forecast for CONUS. 

`wxdata-ndfd fetch latest -v maximum_temperature`

2) Download the maximum temperature forecast for Alaska through a proxy server of `https://proxy-address:proxy-port`.

`wxdata-ndfd fetch latest -v maximum_relative_humidity -r ak --proxy https://proxy-address:proxy-port`

3) Download the SPC Convective Outlook

`wxdata-ndfd fetch latest -v spc_convective_outlook -e False`
