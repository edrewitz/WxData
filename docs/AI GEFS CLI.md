---
title: AIGEFS CLI
---

# AI Global Ensemble Forecast System (AIGEFS) Command Line Interface

***Valid Commands***

-c = Category (Default=mean).

  ***Valid categories***
  
  1) mean
  
  2) members
  
  3) spread
  
-f = Final Forecast Hour (Default=384).

-m = Members.

  The individual ensemble members to select. Defaults to all 30 members.
  
  This is only necessary when category=members -> `-c members`
  
-cr = Clear Recycle Bin. (Default=False)

To clear your recycle bin with each run of the script set to True.

-cdir = Custom Directory (Default=None).

When set to None, the default file path is used. 

Change this if you want your directories set up differently.

-cd = Clear Data (Default=False).
  
When set to False the scanner safeguard that prevents repetative downloads is enabled.
Set -cd False to disable this safety feature.

WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
retry downloading the data. 

-s = Source (Default=noaa). 

Selects the primary data server to use.
If the primary server is unavailable the client will rotate and try other servers.

***Server Choices***

noaa - NCEP/NOMADS

aws - Amazon Web Services

-ct = Convert Temperature (Default=True).

When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.

-tu = Temperature Units (Default=Celsius).

When -ct True this is where you declare the units for temperature to be converted to. 

-lt = Level Type (Default=pressure).

This corresponds to the type of level.

***Level Types***

i) pressure

ii) surface

iii) height_above_ground

iv) mean sea level

-l = Levels (hPa) (Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10])

-wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)

-eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)

-nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)

-sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)

-v = Variables(Default=['geopotential_height', 'specific humidity', 'temperature', 'u-component_of_wind', 'v-component_of_wind', 'vertical_velocity']) 
                    
The list of variables the user wants to query.
 
***Variables By Level Type***

*pressure*

'geopotential_height'

'specific_humidity'

'temperature'

'u-component_of_wind'

'v-component_of_wind'

'vertical_velocity'

*height_above_ground*

'u-component_of_wind' - 10m

'v-component_of_wind' - 10m

'temperature' - 2m

*mean_sea_level*

'mean_sea_level_pressure'

*surface*

'total_precipitation'

***Pressure-Level Plain Language Variable Keys***

'geopotential_height'

'specific_humidity'

'air_temperature'

'u_wind_component'

'v_wind_component'

'vertical_velocity'

***Surface-Level Plain Language Variable Keys***

'10m_u_wind_component'

'10m_v_wind_component'

'mslp'

'2m_temperature'

--process This flag when set to True will process the data in addition to downloading the data. (Default=True)

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`

--netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.

***Additional Relevant Flags when --netcdf True***

--ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=AIGEFS/NETCDF). 

--ncfname = Defines the filename for the netCDF (.nc) file. (Default=aigefs.nc)

***Complex Example***

*Important*: Any parameter of the command not explicitly stated results in the default value being used.

1) Download the latest AIGEFS Ensemble Spread for 500mb Geopotential Height from Amazon Web Services

  - Use a proxy server of address: `https://proxy-server-address:proxy-server-port`
          
2) Subset the data to reflect Northern Hemisphere [-180, 180, 90, 0] = [west, east, north, south]
  
3) Create a netCDF (.nc) file of the data called `aigefs_spread_gph.nc` saved at Weather_Data/AIGEFS/NETCDF.

Linux Shell:
```shell
# Define our coordinates so we don't pass in negative numbers into the command
western_bound=-180
eastern_bound=180
northern_bound=90
southern_bound=0

wxdata-aigefs fetch latest -c spread -v geopotential_height -l 500 \
-s aws -wb=$western_bound -eb=$eastern_bound -nb=$northern_bound -sb=$southern_bound \
--netcdf True --ncdir Weather_Data/AIGEFS/NETCDF --ncfname aigefs_spread_gph.nc \ 
--proxy https://proxy-server-address:proxy-server-port
```
      
Windows Powershell:
```powershell
# Define our coordinates so we don't pass in negative numbers into the command
$WESTERN_BOUND=-180
$EASTERN_BOUND=180
$NORTHERN_BOUND=90
$SOUTHERN_BOUND=0

wxdata-aigefs fetch latest -c spread -v geopotential_height -l 500 `
-s aws -wb=$WESTERN_BOUND -eb=$EASTERN_BOUND -nb=$NORTHERN_BOUND -sb=$SOUTHERN_BOUND `
--netcdf True --ncdir Weather_Data/AIGEFS/NETCDF --ncfname aigefs_spread_gph.nc ` 
--proxy https://proxy-server-address:proxy-server-port
```


