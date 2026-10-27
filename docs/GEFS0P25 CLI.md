---
title: GEFS0P25 CLI
---

[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)

# Global Ensemble Forecast System (GEFS) 0.25x0.25 Command Line Interface.

***Archived Required Commands***

-d = Date. The date of the model run in the format of YYYY-mm-dd.

    (i.e. December 25th, 2025 should be entered as -d 2025-12-25)
    
-r = Run. The model runtime in UTC (0, 6, 12, 18). 

    (i.e. for the 12z run set -r 12)


***Globally Valid Commands (valid for both "latest" and "archived")***

-c = Category (Default='mean')

This determines the category of ensemble data 

***Categories***

1) mean

2) members

3) spread

4) control

-f = Final Forecast Hour (Default=240).
 
The last hour the user wishes to download in the dataset. GEFS0P25 has 240 forecast hours.

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
The default path is f:GEFS0P25/{CATEGORY}. 

-cr = Clear Recycle Bin (Default=False).

For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
Setting -cr True clears your recycle bin with each run of the script. 
This ensures if any old files are moved to the recycle bin are deleted if they are not already.

-wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)

-eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)

-nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)

-sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)

-m = Ensemble Members. (Default is all 30 members).

-v = Variables(Default=['temperature']) 
                   
The list of variables the user wants to query.

Here is a sample of how to query ensemble members 2-meter temperature and relative humidity and create a netCDF file:

`wxdata-gefs 0p25 latest -c members -v geopotential_height -v temperature -l 2 --netcdf True --ncdir GEFS0P25/Members/NETCDF --ncfname gefs_t_rh.nc`

**Variables**

'total_precipitation'

'convective_available_potential_energy'

'categorical_freezing_rain'

'categorical_ice_pellets'

'convective_inhibition'

'percent_frozen_precipitaion'

'categorical_rain'

'categorical_snow'

'downward_longwave_radiation_flux'

'downward_shortwave_radiation_flux'

'dew_point'

'wind_gust'

'geopotential_height'

'storm_relative_helicity'

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

'visibility'

'water_equivalent_of_accumulated_snow_depth'

-l = Levels (Default=[2])

The default setting of levels assume height above ground levels are being used and that the category is set to primary.

-ct = Convert Temperature (Default=True).

When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.

-tu = Temperature Units (Default=Celsius).

When -ct True this is where you declare the units for temperature to be converted to. 

-lt = Level Type (Default=height above ground).

This corresponds to the type of level.
                                                            
**Level Types**

'surface'

'mean sea level'

'height above ground'

'height below ground'

'entire atmosphere (considered as a single layer)'

'cloud ceiling'

'pressure above ground'

--process This flag when set to True will process the data in addition to downloading the data. (Default=True)

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`

--netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.

**Additional Relevant Flags when --netcdf True**

--ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=GEFS0P25/NETCDF). 

--ncfname = Defines the filename for the netCDF (.nc) file. (Default=gefs_0p25.nc)

**Commands Only Valid for "latest"**

-cd = Clear Data (Default=False).

***Only for wxdata-gefs 0p25 latest***

***Archived Clients Automatically Clear Old Data***

When set to False the scanner safeguard that prevents repetative downloads is enabled.
Set -cd False to disable this safety feature.

WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
retry downloading the data.  

***Complex Example***

*Important*: Any parameter of the command not explicitly stated results in the default value being used.

1) Download the latest GEFS0P25 for 2-meter temperature and 2-meter relative humidity from Amazon Web Services
 
    - Use a proxy server of address: `https://proxy-server-address:proxy-server-port` 
    
    - Download only members 1-5
    
2) Subset the data to reflect CONUS [-130, -65, 50, 20] = [west, east, north, south]
    
3) Create a netCDF (.nc) file of the data called `gefs0p25_members_t2m_rh.nc` saved at Weather_Data/GEFS0P25/NETCDF.

Linux Shell:
```shell
wxdata-gefs 0p25 latest -c members -lt height_above_ground -l 2 -v temperature -v relative_humidity \
-m 1 -m 2 -m 3 -m 4 -m 5 -s aws -wb -130 -eb -65 -nb 50 -sb 20 \
--netcdf True --ncdir Weather_Data/GEFS0P25/NETCDF --ncfname gefs0p50_members_t2m_rh.nc \ 
--proxy https://proxy-server-address:proxy-server-port
```
        
Windows Powershell:
```powershell
wxdata-gefs 0p25 latest -c members -lt height_above_ground -l 2 -v temperature -v relative_humidity `
-m 1 -m 2 -m 3 -m 4 -m 5 -s aws -wb -130 -eb -65 -nb 50 -sb 20 `
--netcdf True --ncdir Weather_Data/GEFS0P25/NETCDF --ncfname gefs0p25_members_t2m_rh.nc ` 
--proxy https://proxy-server-address:proxy-server-port
```
    
