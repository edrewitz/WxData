---
title: ECMWF AIFS CLI
---


# European Centre for Medium-Range Weather Forecasts (ECMWF) AIFS Command Line Interface
    
***Valid Commands***

-t = Type of ECMWF AIFS Data. (Default='d').

***Here are the various commands for the different ECMWF AIFS Model Options***

-d = Deterministic AIFS (0.25x0.25 Degree)

-e = AIFS Ensemble (0.25x0.25 Degree)

-wd = AIFS Wave Deterministic (0.25x0.25 Degree)

-we = AIFS Wave Ensemble (0.25x0.25 Degree)

-c = Category. (Default="control").

***Valid Categories***

1) control

2) members

-f = Final Forecast Hour (Default=360).

Maximum forecast hour is 360 hours. 

-s = Source (Default=ecmwf). 

Selects the primary data server to use.
If the primary server is unavailable the client will rotate and try other servers.

***Server Choices***

ecmwf - ECMWF Open-Data

aws - Amazon Web Services

google - Google Cloud Servers

-cdir = Custom Directory (Default=None).

If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.

-cr = Clear Recycle Bin (Default=False).

For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
Setting -cr True clears your recycle bin with each run of the script. 
This ensures if any old files are moved to the recycle bin are deleted if they are not already.

-wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)

-eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)

-nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)

-sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)

-v = Variables(Default=['geopotential_height', 'specific humidity', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']) 
                 
The list of variables the user wants to query.

Here is a sample of how to query geopotential height and temperature at 500mb `wxdata-ecmwf ifs latest -v geopotential_height -v temperature -l 500`

***Variable List (All Except for ECMWF AIFS Wave/AIFS Wave Ensemble Data)***

'10-meter_u-wind_component'

'10-meter_v-wind_component'

'100-meter_u-wind_component'

'100-meter_v-wind_component'

'maximum_10-meter_wind_gust_step_0'

'maximum_10-meter_wind_gust_steps_3-144'

'2-meter_temperature'

'2-meter_dewpoint_temperature'

'mean_sea_level_pressure'

'mean_zero-crossing_wave_period'

'mean_wave_direction'

'mean_wave_period'

'peak_wave_period'

'significant_wave_height'

'runoff'

'total_precipitation'

'surface_pressure'

'total_column_vertically_integrated_water_vapor'

'total_cloud_cover'

'snow_depth_water_equivalent'

'snowfall_water_equivalent'

'land_sea_mask'

'volumetric_soil_moisture_content'

'soil_temperature'

'most_unstable_cape'

'snow_albedo'

'3-hour_minimum_2-meter_temperature'

'3-hour_maximum_2-meter_temperature'

'6-hour_minimum_2-meter_temperature'

'6-hour_maximum_2-meter_temperature'

'total_precipitation_rate'

'precipitation_type'

'top_net_longwave_thermal_radiation'

'snow_density'

'surface_net_longwave_thermal_radiation'

'surface_net_shortwave_solar_radiation'

'surface_shortwave_radiation_downward'

'surface_longwave_radiation_downward'

'northward_turbulent_surface_stress'

'eastward_turbulent_surface_stress'

'eastward_surface_sea_water_velocity'

'northward_surface_sea_water_velocity'

'sea_ice_thickness'

'sea_surface_height'

'divergence'

'geopotential_height'

'specific_humidity'

'relative_humidity'

'temperature'

'u-wind_component'

'v-wind_component'

'vertical_velocity'

'relative_vorticity'

***Variable List (For ECMWF AIFS Wave/AIFS Wave Ensemble Data)***

'significant_height_of_combined_waves_and_swell'

'mean_wave_direction'

'mean_wave_period'
  
-ct = Convert Temperature (Default=True).

When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.

-tu = Temperature Units (Default=Celsius).

When -ct True this is where you declare the units for temperature to be converted to. 

-l = Levels (Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 1150, 100, 50])
                      
Here is a sample of how to query geopotential height and temperature at 850 and 500mb 

`wxdata-ecmwf ifs latest -v geopotential_height -v temperature -l 850 -l 500`

-lt = Level Type (Default=pressure).

This corresponds to the type of level.

***Level Types***

pressure

surface

soil

--process This flag when set to True will process the data in addition to downloading the data. (Default=True)

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`
  
--netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.

**Additional Relevant Flags when --netcdf True**

--ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=ECMWF AIFS/NETCDF). 

--ncfname = Defines the filename for the netCDF (.nc) file. (Default=ecmwf_aifs.nc)

***Complex Example***

*Important*: Any parameter of the command not explicitly stated results in the default value being used.

1) Download the latest AIFS Ensemble for 2-meter temperature from Amazon Web Services

  - Use a proxy server of address: `https://proxy-server-address:proxy-server-port` 
  
  - Download only members 1-5
  
2) Subset the data to reflect CONUS [-130, -65, 50, 20] = [west, east, north, south]
  
3) Create a netCDF (.nc) file of the data called `aifs_members_t2m.nc` saved at Weather_Data/AIFS/NETCDF.

Linux Shell:
```shell
wxdata-ecmwf aifs latest -t e -c members -lt surface -v 2-meter_temperature \
-m 1 -m 2 -m 3 -m 4 -m 5 -s aws -wb -130 -eb -65 -nb 50 -sb 20 \
--netcdf True --ncdir Weather_Data/AIFS/NETCDF --ncfname aifs_members_t2m.nc \ 
--proxy https://proxy-server-address:proxy-server-port
```
      
Windows Powershell:
```powershell
wxdata-ecmwf aifs latest -t e -c members -lt surface -v 2-meter_temperature `
-m 1 -m 2 -m 3 -m 4 -m 5 -s aws -wb -130 -eb -65 -nb 50 -sb 20 `
--netcdf True --ncdir Weather_Data/AIFS/NETCDF --ncfname aifs_members_t2m.nc ` 
--proxy https://proxy-server-address:proxy-server-port
```
    
