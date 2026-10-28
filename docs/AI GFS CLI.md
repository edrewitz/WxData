---
title: AIGFS CLI
---

# AI Global Forecast System (AIGFS) Command Line Interface

***Valid Commands***
    
-f = Final Forecast Hour (Default=384).
    
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

-l = Levels (hPa) (Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10])

-wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)

-eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)

-nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)

-sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)

-v = Variables(Default=['geopotential_height', 'specific humidity', 'temperature', 'u-component_of_wind', 'v-component_of_wind', 'vertical velocity']) 
                   
The list of variables the user wants to query.

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

--ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=AIGFS/NETCDF). 

--ncfname = Defines the filename for the netCDF (.nc) file. (Default=aigfs.nc)

***Complex Example***

*Important*: Any parameter of the command not explicitly stated results in the default value being used.

1) Download the latest AIGFS for 500mb Geopotential Height from Amazon Web Services
 
    - Use a proxy server of address: `https://proxy-server-address:proxy-server-port`
            
2) Subset the data to reflect Northern Hemisphere [-180, 180, 90, 0] = [west, east, north, south]
    
3) Create a netCDF (.nc) file of the data called `aigfs_gph.nc` saved at Weather_Data/AIGFS/NETCDF.

Linux Shell:
```shell
wxdata-aigfs fetch latest -v geopotential_height -l 500 \
-s aws -wb -180 -eb 180 -nb 90 -sb 0 \
--netcdf True --ncdir Weather_Data/AIGFS/NETCDF --ncfname aigfs_gph.nc \ 
--proxy https://proxy-server-address:proxy-server-port
```
        
Windows Powershell:
```powershell
wxdata-aigfs fetch latest -v geopotential_height -l 500 `
-s aws -wb -180 -eb 180 -nb 90 -sb 0 `
--netcdf True --ncdir Weather_Data/AIGFS/NETCDF --ncfname aigfs_gph.nc ` 
--proxy https://proxy-server-address:proxy-server-port
```
    
