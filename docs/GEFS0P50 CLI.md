---
title: GEFS0P50 CLI
---


# Global Ensemble Forecast System (GEFS) 0.50x0.50 Command Line Interface.
    
***Archived Required Commands***

-d = Date. The date of the model run in the format of YYYY-mm-dd.

    (i.e. December 25th, 2025 should be entered as -d 2025-12-25)
    
-r = Run. The model runtime in UTC (0, 6, 12, 18). 

    (i.e. for the 12z run set -r 12)


***Globally Valid Commands (valid for both "latest" and "archived")***

-t = type (Default=primary).

This determines the type of variables and levels.

***Types***

1) primary

2) secondary

-c = Category (Default='mean')

This determines the category of ensemble data 

***Categories***

1) mean

2) members

3) spread

4) control

-f = Final Forecast Hour (Default=384).
 
The last hour the user wishes to download in the dataset. GEFS0P50 has 384 forecast hours.

-s = Source (Default=noaa). 

Selects the primary data server to use.
If the primary server is unavailable the client will rotate and try other servers.

***Server Choices For Latest Data***

noaa - NCEP/NOMADS

aws - Amazon Web Services

google - Google Cloud Servers

***Server Choices For Archived Data***

aws - Amazon Web Services

google - Google Cloud Servers

-cdir = Custom Directory (Default=None).

If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
The default path is f:GEFS0P50/{CATEGORY}. 

-cr = Clear Recycle Bin (Default=False).

For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
Setting -cr True clears your recycle bin with each run of the script. 
This ensures if any old files are moved to the recycle bin are deleted if they are not already.

-wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)

-eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)

-nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)

-sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)

-m = Ensemble Members. (Default is all 30 members).

-v = Variables(Default=['geopotential_height', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']) 
                   
The list of variables the user wants to query.

Here is a sample of how to query geopotential height and temperature `gefs 0p25 latest -v geopotential_height -v temperature`

***Primary Variables***

'total_precipitation'

'convective_available_potential_energy'

'categorical_freezing_rain'

'categorical_ice_pellets'

'categorical_rain'

'categorical_snow'

'convective_inhibition'

'downward_longwave_radiation_flux'

'downward_shortwave_radiation_flux'

'geopotential_height'

'ice_thickness'

'latent_heat_net_flux'

'pressure'

'mean_sea_level_pressure'

'precipitable_water'

'relative_humidity'

'sensible_heat_net_flux'

'snow_depth'

'volumetric_soil_moisture_content'

'total_cloud_cover'

'maximum_temperature'

'minimum_temperature'

'temperature'

'soil_temperature'

'u-component_of_wind'

'upward_longwave_radiation_flux'

'upward_shortwave_radiation_flux'

'v-component_of_wind'

'vertical_velocity'

'water_equivalent_of_accumulated_snow_depth'

***Secondary_Variables***

'best_lifted_index'

'5_wave_geopotential_height'

'absolute_vorticity'

'temperature'

'dew_point'

'convective_precipitation'

'albedo'

'apparent_temperature'

'brightness_temperature'

'convective_available_potential_energy'

'clear_sky_uv-b_downward_solar_flux'

'convective_inhibition'

'cloud_mixing_ratio'

'plant_canopy_surface_water'

'percent_frozen_precipitaion'

'convective_precipitation_rate'

'cloud_water'

'cloud_work_function'

'uv-b_downward_solar_flux'

'field_capacity'

'surface_friction_velocity'

'ground_heat_flux'

'wind_gust'

'geopotential_height'

'haines_index'

'storm_relative_helicity'

'planetary_boundary_layer_height'

'icao_standard_atmosphere_reference_height'

'ice_cover'

'icing'

'icing_severity'

'land_cover'

'surface_lifted_index'

'montgomery_stream_function'

'mslp_(eta_model_reduction)'

'large_scale_non-convective_precipitation'

'ozone_mixing_ratio'

'potential_evaporation_rate'

'parcel_lifted_index_(to_500mb)'

'pressure_level_from_which_parcel_was_lifted'

'potential_temperature'

'precipitation_rate'

'pressure'

'potential_vorticity'

'precipitable_water'

'relative_humidity'

'surface_roughness'

'snow_phase-change_heat_flux'

'snow_cover'

'liquid_volumetric_soil_moisture_(non-frozen)'

'volumetric_soil_moisture_content'

'specific_humidity'

'sunshine_duration'

'total_cloud_cover'

'total_ozone'

'soil_temperature'

'momentum_flux_(u-component)'

'u-component_of_wind'

'zonal_flux_of_gravity_wave_stress'

'u-component_of_storm_motion'

'upward_shortwave_radiation_flux'

'momentum_flux_(v-component)'

'v-component_of_wind'

'meridional_flux_of_gravity_wave_stress'

'visibility'

'ventilation_rate'

'v-component_of_storm_motion'

'vertical_velocity'

'vertical_speed_shear'

'water_runoff'

'wilting_point'

-l = Levels (Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10])
                        
Here is a sample of how to query geopotential height and temperature at 850 and 500mb 

`wxdata-gefs 0p50 latest -v geopotential_height -v temperature -l 850 -l 500`

The default setting of levels assume pressure levels are being used and that the category is set to primary.

-lt = Level Type (Default=pressure).

This corresponds to the type of level.

Primary Levels: 1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10

Secondary Levels: Default=None -> level_type='surface'. 

Example: level_type='height above ground' & levels=2 -> 2-meter above ground

-ct = Convert Temperature (Default=True).

When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.

-tu = Temperature Units (Default=Celsius).

When -ct True this is where you declare the units for temperature to be converted to. 
                                                            
**Level Types**

'pressure'

'height below ground'

'surface'

'height above ground'

'top of atmosphere'

'pressure above ground'

'mean sea level'

--process This flag when set to True will process the data in addition to downloading the data. (Default=True)

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`

--netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.

***Additional Relevant Flags when --netcdf True***

--ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=GEFS0P50/NETCDF). 

--ncfname = Defines the filename for the netCDF (.nc) file. (Default=gefs_0p50.nc)

***Commands Only Valid for "latest"***

-cd = Clear Data (Default=False).

***Only for wxdata-gefs 0p50 latest***

***Archived Clients Automatically Clear Old Data***

When set to False the scanner safeguard that prevents repetative downloads is enabled.
Set -cd False to disable this safety feature.

WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
retry downloading the data.  

***Complex Example***

1) Download the latest GEFS0P50 for 2-meter temperature and 2-meter relative humidity from Amazon Web Services
 
- Use a proxy server of address: `https://proxy-server-address:proxy-server-port` 

- Download only members 1-5
    
2) Subset the data to reflect CONUS [-130, -65, 50, 20] = [west, east, north, south]
    
3) Create a netCDF (.nc) file of the data called `gefs0p50_members_t2m_rh.nc` saved at Weather_Data/GEFS0P50/NETCDF.

Linux Shell:
```shell
# Define our coordinates so we don't pass in negative numbers into the command
western_bound=-130
eastern_bound=-65
northern_bound=50
southern_bound=20

wxdata-gefs 0p50 latest -c members -lt height_above_ground -l 2 -v temperature -v relative_humidity \
-m 1 -m 2 -m 3 -m 4 -m 5 -s aws -wb=$western_bound -eb=$eastern_bound -nb=$northern_bound -sb=$southern_bound \
--netcdf True --ncdir Weather_Data/GEFS0P50/NETCDF --ncfname gefs0p50_members_t2m_rh.nc \ 
--proxy https://proxy-server-address:proxy-server-port
```
        
Windows Powershell:
```powershell
# Define our coordinates so we don't pass in negative numbers into the command
$WESTERN_BOUND=-130
$EASTERN_BOUND=-65
$NORTHERN_BOUND=50
$SOUTHERN_BOUND=20

wxdata-gefs 0p50 latest -c members -lt height_above_ground -l 2 -v temperature -v relative_humidity `
-m 1 -m 2 -m 3 -m 4 -m 5 -s aws -wb=$WESTERN_BOUND -eb=$EASTERN_BOUND -nb=$NORTHERN_BOUND -sb=$SOUTHERN_BOUND `
--netcdf True --ncdir Weather_Data/GEFS0P50/NETCDF --ncfname gefs0p50_members_t2m_rh.nc ` 
--proxy https://proxy-server-address:proxy-server-port
``` 
