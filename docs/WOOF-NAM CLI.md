---
title: WOOF-NAM CLI
---

# WOOF-NAM Command Line Interface

WOOF-NAM Client.

***Valid Commands***
    
-f = Final Forecast Hour (Default=84).
 
The last hour the user wishes to download in the dataset. WOOF-NAM has 84 forecast hours.

-cdir = Custom Directory (Default=None).

If the user wishes to build their own directory to hold the data files set -cdir directory_branch_path.
The default path is f:WOOF-NAM. 

-cr = Clear Recycle Bin (Default=False).

For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
Setting -cr True clears your recycle bin with each run of the script. 
This ensures if any old files are moved to the recycle bin are deleted if they are not already.

-cd = Clear Data (Default=False).

When set to False the scanner safeguard that prevents repetative downloads is enabled.
Set -cd False to disable this safety feature.

WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
retry downloading the data.   

-v = Variables(Default=['geopotential height',
                    'absolute vorticity',
                    'temperature',
                    'relative humidity',
                    'vertical velocity (pressure)',
                    'vertical velocity (height)',
                    'u-component of wind',
                    'v-component of wind',
                    'turbulent kinetic energy']) 
                   
The list of variables the user wants to query.

***Variables***

'mean_sea_level_pressure'

'reflectivity'

'composite_reflectivity'

'visibility'

'geopotential_height'

'u-component_of_wind'

'v-component_of_wind'

'temperature'

'ventilation_rate'

'wind_gust'

'radar_echo_top_height'

'vertical_velocity_height'

'relative_humidity'

'specific_humidity'

'vertical_velocity_pressure'

'turbulent_kinetic_energy'

'mslp_eta_reduction'

'soil_temperature'

'volumetric_soil_moisture_content'

'liquid_volumetric_soil_moisture_non-frozen'

'soil_moisture_content'

'soil_porosity'

'number_of_soil_layers'

'haines_index'

'absolute_vorticity'

'moisture_availability'

'plant_canopy_surface_water'

'water_equivalent_of_accumulated_snow_depth'

'snow_cover'

'snow_depth'

'direct_evaporation_cease'

'dew_point'

'total_precipitation'

'convective_precipitation'

'water_equivalent_of_accumulated_snow_depth'

'categorical_snow'

'categorical_ice_pellets'

'categorical_freezing_rain'

'categorical_rain'

'surface_roughness'

'surface_friction_velocity'

'drag_coefficient'

'vegetation'

'vegetation_type'

'wilting_point'

'transpiration_stress_onset'

'surface_lifted_index'

'best_lifted_index'

'convective_available_potential_energy'

'convective_inhibition'

'storm_relative_helicity'

'vertical_shear_u-component'

'vertical_shear_v-component'

'pressure'

'parcel_lifted_index'

'planetary_boundary_layer_height'

'land_cover'

'ice_cover'

'albedo'

'sensible_heat_net_flux'

'latent_heat_net_flux'

'total_cloud_cover'

'downward_shortwave_radiation_flux'

'downward_longwave_radiation_flux'

'upward_shortwave_radiation_flux'

'upward_longwave_radiation_flux'

-l = Levels (Default=[1000,
                        925,
                        850,
                        700,
                        500,
                        300,
                        250,
                        100,
                        50])

The default setting of levels assume height above ground levels are being used and that the category is set to primary.

-ct = Convert Temperature (Default=True).

When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.

-tu = Temperature Units (Default=Celsius).

When -ct True this is where you declare the units for temperature to be converted to. 

-lt = Level Type (Default=height above ground).

This corresponds to the type of level.
                                                            
***Level Types***

'mean_sea_level'

'hybrid'

'entire_atmosphere_single_layer'

'surface'

'boundary_layer'

'pressure'

'height_above_ground'

'depth_below_land_layer'

'height_below_ground'

'lowest_level_wetbulb_zero'

'isobaric_layer'

'cloud_base'

'height_above_ground_layer_helicity'

'height_above_ground_layer_shear'

'tropopause'

'max_wind'

'isothermal'

'pressure_above_ground'

'sigma_layer'

--process This flag when set to True will process the data in addition to downloading the data. (Default=True)

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`

--netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.

***Additional Relevant Flags when --netcdf True***

--ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=WOOF-NAM/NETCDF). 

--ncfname = Defines the filename for the netCDF (.nc) file. (Default=woof_nam.nc)

***Complex Example***

*Important*: Any parameter of the command not explicitly stated results in the default value being used. 

1) Download the latest WOOF-NAM for 500mb Geopotential Height
 
    - Use a proxy server of address: `https://proxy-server-address:proxy-server-port` 
                    
2) Create a netCDF (.nc) file of the data called `woof_nam_gph_500.nc` saved at Weather_Data/WOOF-NAM/NETCDF.

Linux Shell:
```shell
wxdata-woof-nam fetch latest -v geopotential_height -l 500 \
--netcdf True --ncdir Weather_Data/WOOF-NAM/NETCDF --woof_nam_gph_500.nc \ 
--proxy https://proxy-server-address:proxy-server-port
```
        
Windows Powershell:
```powershell
wxdata-woof-nam fetch latest -v geopotential_height -l 500 `
--netcdf True --ncdir Weather_Data\WOOF-NAM\NETCDF --ncfname woof_nam_gph_500.nc ` 
--proxy https://proxy-server-address:proxy-server-port
```
