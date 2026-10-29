---
title: CFS Flux CLI
---

# Climate Forecast System Flux Variables & Levels

***Archived Required Commands***

-d = Date. The date of the model run in the format of YYYY-mm-dd.

    (i.e. December 25th, 2025 should be entered as -d 2025-12-25)
    
-r = Run. The model runtime in UTC (0, 6, 12, 18). 

    (i.e. for the 12z run set -r 12)


***Globally Valid Commands (valid for both "latest" and "archived")***
    
-t = Type (Default=primary).

This determines the type of variables and levels.

-f = Final Forecast Hour (Default=720).
 
The last hour the user wishes to download in the dataset. GFS0P25 has 384 forecast hours.

-s = Source (Default=noaa). 

Selects the primary data server to use.
If the primary server is unavailable the client will rotate and try other servers.

***Server Choices For Latest Data***

noaa - NCEP/NOMADS

aws - Amazon Web Services
    
***Server Choices For Archived Data***

aws - Amazon Web Services
    
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

-v = Variable. Default="temperature".

   ***Variable List***
   
'aerodynamic conductance'

'albedo'

'clear sky uv-b downward solar flux'

'plant canopy surface water'

'convective precipitation rate'

'categorical rain'

'clear sky downward longwave flux'

'clear sky downward solar flux (surface)'

'clear sky downward solar flux (top of the atmosphere)'

'clear sky upward solar flux'

'cloud work function'

'downward longwave radiation flux'

'downward shortwave radiation flux'

'clear sky uv-b downward solar flux'

'direct evaporation from bare soil'

'canopy water evaporation'

'surface friction velocity'

'ground heat flux'

'geopotential height'

'planetary boundary layer height'

'ice cover'

'ice thickness'

'land cover'

'latent heat net flux'

'near ir beam downward solar flux'

'near ir diffuse downward solar flux'

'potential evaporation rate'

'precipitation rate'

'pressure'

'precipitable water'

'2-meter maximum specific humidity'

'2-meter minimum specific humidity'

'sublimation (evaporation from snow)'

'surface roughness'

'sedimentation mass flux'

'sensible heat net flux'

'surface slope type'

'snow depth'

'snow phase-change heat flux'

'snow cover'

'liquid volumetric soil moisture (non-frozen)'

'soil moisture content'

'volumetric soil moisture content'

'soil type'

'specific humidity'

'snowfall rate water equivalent'

'storm surface runoff (non-infiltrating)'

'total cloud cover'

'maximum temperature'

'minimum temperature'

'temperature'

'transpiration'

'momentum flux (u-component)'

'u-component of wind'

'zonal flux of gravity wave stress'

'upward longwave radiation flux'

'upward shortwave radiation flux'

'visible beam downward solar flux'

'vegetation'

'momentum flux (v-component)'

'v-component of wind'

'vegetation type'

'meridional flux of gravity wave stress'

'water runoff'

'water equivalent of accumulated snow depth'
    
-l = Levels (Default=[2])
    
***Available Levels***

*height above ground*

m above ground

[2, 10]

*height below ground*

m below ground

[0-0.1, 0.1-0.4, 0.4-1, 0.1-0.4, 1-2, 0-2]

*hybrid*

[1]

-ct = Convert Temperature (Default=True).

When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.

-tu = Temperature Units (Default=Celsius).

When -ct True this is where you declare the units for temperature to be converted to. 

-lt = Level Type (Default=height_above_ground).

This corresponds to the type of level.

***Level Types***

'surface'

'height_above_ground'

'height_below_ground'

'entire_atmosphere'

'top_of_atmosphere'

'high_cloud_top_level'

'middle_cloud_top_level'

'low_cloud_top_level'

'high_cloud_bottom_level'

'middle_cloud_bottom_level'

'low_cloud_bottom_level'

'convective_cloud_layer'

'boundary_layer_cloud_layer'

'height_above_sea_level'

'hybrid'

--process = Process Data. This flag when set to True will process the data in addition to downloading the data. (Default=True)

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`

--netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.

***Additional Relevant Flags when --netcdf True***

--ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=CFS/Flux/NETCDF). 

--ncfname = Defines the filename for the netCDF (.nc) file. (Default=cfs_flux.nc)

***Commands Only Valid for "latest"***

-cd = Clear Data (Default=False).

***Only for wxdata-cfs pressure latest***

***Archived Clients Automatically Clear Old Data***

When set to False the scanner safeguard that prevents repetative downloads is enabled.
Set -cd False to disable this safety feature.

WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
retry downloading the data. 

***Complex Example***

1) Download the latest CFS forecast for 2-meter temperature from NCEP/NOMADS
 
    - Use a proxy server of address: `https://proxy-server-address:proxy-server-port` 
    
    - Use the default `final_forecast_hour` of hour 720 (1-month). 
            
2) Subset the data to reflect CONUS [-130, -65, 50, 20] = [west, east, north, south]
    
3) Create a netCDF (.nc) file of the data called `cfs_t2m_gph.nc` saved at Weather_Data/CFS/TMP/2/NETCDF.

Linux Shell:
```shell
wxdata-cfs flux latest -lt height_above_ground -l 2 -v temperature \
-s noaa -wb -130 -eb -65 -nb 50 -sb 20 \
--netcdf True --ncdir Weather_Data/CFS/TMP/2/NETCDF --ncfname cfs_t2m_gph.nc \ 
--proxy https://proxy-server-address:proxy-server-port
```
        
Windows Powershell:
```powershell
wxdata-cfs flux latest -lt height_above_ground -l 2 -v temperature `
-s noaa -wb -130 -eb -65 -nb 50 -sb 20 `
--netcdf True --ncdir Weather_Data/CFS/TMP/2/NETCDF --ncfname cfs_t2m_gph.nc ` 
--proxy https://proxy-server-address:proxy-server-port
```
