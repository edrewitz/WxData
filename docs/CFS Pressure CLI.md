---
title: CFS Pressure CLI
---

# Climate Forecast System Pressure Variables & Levels

***Archived Required Commands***

-d = Date. The date of the model run in the format of YYYY-mm-dd.

    (i.e. December 25th, 2025 should be entered as -d 2025-12-25)
    
-r = Run. The model runtime in UTC (0, 6, 12, 18). 

    (i.e. for the 12z run set -r 12)


***Globally Valid Commands (valid for both "latest" and "archived")***

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

-v = Variable. Default="geopotential_height".

   ***Variable List***
   
  'best lifted index'
  
  '5 wave geopotential height anomaly'
  
  '5 wave geopotential height'
  
  'absolute vorticity'
  
  'convective precipitation'
  
  'total precipitation'
  
  'convective available potential energy'
  
  'categorical freezing rain'
  
  'categorical ice pellets'
  
  'convective inhibition'
  
  'cloud mixing ratio'
  
  'categorical rain'
  
  'categorical snow'
  
  'cloud water'
  
  'dew point'
  
  'geopotential height anomaly'
  
  'geopotential height'
  
  'storm relative helicity'
  
  'surface lifted index'
  
  'large scale non-convective precipitation'
  
  'ozone mixing ratio'
  
  'parcel lifted index'
  
  'potential temperature'
  
  'pressure'
  
  'mean sea level pressure'
  
  'precipitable water'
  
  'relative humidity'
  
  'specific humidity'
  
  'stream function'
  
  'temperature'
  
  'total ozone'
  
  'u-component of wind'
  
  'u-component of storm motion'
  
  'v-component of wind'
  
  'velocity potential'
  
  'v-component of storm motion'
  
  'vertical velocity'
  
  'vertical speed shear'
    
-l = Levels (Default=[1000, 925, 850, 700, 500, 400, 300, 250])

***Available Levels***


1000
975
925
900
875
850
825
800
775
750
700
650
600
550
500
450
400
350
300
250
225
200
175
150
125
100
70
50
30
20
10
7
5
3
2
1


-ct = Convert Temperature (Default=True).

When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.

-tu = Temperature Units (Default=Celsius).

When -ct True this is where you declare the units for temperature to be converted to. 

-lt = Level Type (Default=pressure).

This corresponds to the type of level.

***Level Types***

'pressure'

'surface'

'height above ground'

'entire atmosphere'

'mean sea level'

'tropopause'

'height above sea level'

'isothermal'

'highest tropospheric freezing level'

'pressure above ground'

'sigma layer'

'sigma level'

'potential vorticity surface'

--process = Process Data. This flag when set to True will process the data in addition to downloading the data. (Default=True)

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`

--netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.

***Additional Relevant Flags when --netcdf True***

--ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=CFS/PRESSURE/NETCDF). 

--ncfname = Defines the filename for the netCDF (.nc) file. (Default=cfs_pressure.nc)

***Commands Only Valid for "latest"***

-cd = Clear Data (Default=False). *Only for wxdata-cfs pressure latest*

***Archived Clients Automatically Clear Old Data***

When set to False the scanner safeguard that prevents repetative downloads is enabled.
Set -cd False to disable this safety feature.

WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
retry downloading the data. 

***Complex Example***

1) Download the latest CFS forecast for 500mb Geopotential Height from NCEP/NOMADS
 
    - Use a proxy server of address: `https://proxy-server-address:proxy-server-port` 
    
    - Use the default `final_forecast_hour` of hour 720 (1-month). 
            
2) Subset the data to reflect CONUS [-130, -65, 50, 20] = [west, east, north, south]
    
3) Create a netCDF (.nc) file of the data called `cfs_500_gph.nc` saved at Weather_Data/CFS/GPH/500/NETCDF.

Linux Shell:
```shell
wxdata-cfs pressure latest -lt pressure -l 500 -v geopotential_height \
-s noaa -wb -130 -eb -65 -nb 50 -sb 20 \
--netcdf True --ncdir Weather_Data/CFS/GPH/500/NETCDF --ncfname cfs_500_gph.nc \ 
--proxy https://proxy-server-address:proxy-server-port
```
        
Windows Powershell:
```powershell
wxdata-cfs pressure latest -lt pressure -l 500 -v geopotential_height `
-s noaa -wb -130 -eb -65 -nb 50 -sb 20 `
--netcdf True --ncdir Weather_Data/CFS/GPH/500/NETCDF --ncfname cfs_500_gph.nc ` 
--proxy https://proxy-server-address:proxy-server-port
```
