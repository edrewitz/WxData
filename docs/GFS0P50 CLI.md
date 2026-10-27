---
title: GFS0P50 CLI
---

[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)

# Global Forecast System (GEFS) 0.50x0.50 Command Line Interface.

 ***Archived Required Commands***

-d = Date. The date of the model run in the format of YYYY-mm-dd.

    (i.e. December 25th, 2025 should be entered as -d 2025-12-25)
    
-r = Run. The model runtime in UTC (0, 6, 12, 18). 

    (i.e. for the 12z run set -r 12)


***Globally Valid Commands (valid for both "latest" and "archived")***

-f = Final Forecast Hour (Default=384).
 
The last hour the user wishes to download in the dataset. GFS0P50 has 384 forecast hours.

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

-cd = Clear Data (Default=False).

***Only for wxdata-gfs 0p50 latest***

***Archived Clients Automatically Clear Old Data***

When set to False the scanner safeguard that prevents repetative downloads is enabled.
Set -cd False to disable this safety feature.

WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
retry downloading the data. 

-cdir = Custom Directory (Default=None).

If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
The default path is f:GFS0P50/ATMOSPHERIC. 

-cr = Clear Recycle Bin (Default=False).

For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
Setting -cr True clears your recycle bin with each run of the script. 
This ensures if any old files are moved to the recycle bin are deleted if they are not already.

-wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)

-eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)

-nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)

-sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)

-v = Variables(Default=['geopotential_height', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']) 

***Variables***

best_lifted_index

absolute_vorticity

convective_precipitation

albedo

total_precipitation

convective_available_potential_energy

categorical_freezing_rain

categorical_ice_pellets

convective_inhibition

cloud_mixing_ratio

plant_canopy_surface_water

percent_frozen_precipitaion

convective_precipitation_rate

categorical_rain

categorical_snow

cloud_water

cloud_work_function

downward_longwave_radiation_flux

dew_point

downward_shortwave_radiation_flux

vertical_velocity_(height)

field_capacity

surface_friction_velocity

ground_heat_flux

graupel

wind_gust

high_cloud_cover

geopotential_height

haines_index

storm_relative_helicity

planetary_boundary_layer_height

icao_standard_atmosphere_reference_height

ice_cover

ice_growth_rate

ice_thickness

ice_temperature

ice_water_mixing_ratio

land_cover

low_cloud_cover

surface_lifted_index

latent_heat_net_flux

middle_cloud_cover

mean_sea_level_pressure

mslp_(eta_model_reduction)

ozone_mixing_ratio

potential_evaporation_rate

pressure_level_from_which_parcel_was_lifted

potential_temperature

precipitation_rate

pressure

mean_sea_level_pressure

precipitable_water

composite_reflectivity

reflectivity

relative_humidity

rain_mixing_ratio

surface_roughness

sensible_heat_net_flux

snow_mixing_ratio

snow_depth

liquid_volumetric_soil_moisture_(non-frozen)

volumetric_soil_moisture_content

soil_type

specific_humidity

sunshine_duration

total_cloud_cover

maximum_temperature

minimum_temperature

temperature

total_ozone

soil_temperature

momentum_flux_(u-component)

u-component_of_wind

zonal_flux_of_gravity_wave_stress

upward_longwave_radiation_flux

u-component_of_storm_motion

upward_shortwave_radiation_flux

vegetation

momentum_flux_(v-component)

v-component_of_wind

meridional_flux_of_gravity_wave_stress

visibility

ventilation_rate

v-component_of_storm_motion

vertical_velocity_(pressure)

vertical_speed_shear

water_runoff

lated_snow_depth

wilting_point

-l = Levels (Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10])          

The default setting of levels assume pressure levels are being used and that the category is set to primary.

-ct = Convert Temperature (Default=True).

When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.

-tu = Temperature Units (Default=Celsius).

When -ct True this is where you declare the units for temperature to be converted to. 

-lt = Level Type (Default=pressure).

This corresponds to the type of level.

Levels: 1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10

***Level Types***

pressure

mean_sea_level

hybrid

entire_atmosphere

boundary_layer

low_cloud_layer

middle_cloud_layer

high_cloud_layer

convective_cloud_bottom_level

--process This flag when set to True will process the data in addition to downloading the data. (Default=True)

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`

--netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.

***Additional Relevant Flags when --netcdf True***

--ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=GFS0P50/NETCDF). 

--ncfname = Defines the filename for the netCDF (.nc) file. (Default=gfs_0p50.nc)

***Complex Example***

1) Download the latest GFS0P50 for 2-meter temperature and 2-meter relative humidity from Amazon Web Services
 
    - Use a proxy server of address: `https://proxy-server-address:proxy-server-port` 
            
2) Subset the data to reflect CONUS [-130, -65, 50, 20] = [west, east, north, south]
    
3) Create a netCDF (.nc) file of the data called `gfs0p50_t2m_rh.nc` saved at Weather_Data/GFS0P50/NETCDF.

Linux Shell:
```shell
wxdata-gfs 0p50 latest -lt height_above_ground -l 2 -v temperature -v relative_humidity \
-m 1 -m 2 -m 3 -m 4 -m 5 -s aws -wb -130 -eb -65 -nb 50 -sb 20 \
--netcdf True --ncdir Weather_Data/GFS0P50/NETCDF --ncfname gfs0p50_t2m_rh.nc \ 
--proxy https://proxy-server-address:proxy-server-port
```
        
Windows Powershell:
```powershell
wxdata-gfs 0p50 latest -lt height_above_ground -l 2 -v temperature -v relative_humidity `
-m 1 -m 2 -m 3 -m 4 -m 5 -s aws -wb -130 -eb -65 -nb 50 -sb 20 `
--netcdf True --ncdir Weather_Data/GFS0P50/NETCDF --ncfname gfs0p50_t2m_rh.nc ` 
--proxy https://proxy-server-address:proxy-server-port
```
