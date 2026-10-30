---
title: CanSIPS CLI
---

# Canadian Seasonal to Inter-annual Prediction System (CanSIPS) Command Line Interface

***Valid Commands***

-t = Type of CanSIPS Data. (Default=forecasts).

***Types of CanSIPS Data***

i) forecast

ii) hindcast

-c = Category. (Default=none).

The type of probabilistic category. If not requesting a probabilistic forecast set this to none.
    
  ***Category List***
  
  'probability above normal'
  
  'probability below normal'
  
  'probability near normal'
  
  'probability > 10th percentile'
  
  'probability > 20th percentile'
  
  'probability > 30th percentile'
  
  'probability > 40th percentile'
  
  'probability > 50th percentile'
  
  'probability > 60th percentile'
  
  'probability > 70th percentile'
  
  'probability > 80th percentile'
  
  'probability > 90th percentile' 
    
-p = Period. The forecast increment (monthly or seasonal [3-month]). Default=monthly.
    
-cd = Clear Data (Default=False).

When set to False the scanner safeguard that prevents repetative downloads is enabled.
Set -cd False to disable this safety feature.

WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
retry downloading the data. 

-cdir = Custom Directory (Default=none).

If the user wishes to build their own directory to hold the data files set -cd directory_branch_path. 

-cr = Clear Recycle Bin (Default=False).

For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
Setting -cr True clears your recycle bin with each run of the script. 
This ensures if any old files are moved to the recycle bin are deleted if they are not already.

-wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)

-eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)

-nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)

-sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)

-v = Variable(Default=geopotential_height) 

***Variable List***

'temperature'

'geopotential_height'

'precipitation'

'precipitation rate'

'pressure'

'sea_surface_height'

'sea_surface_temperature'

'u-wind_component'

'v-wind_component'

-l = Level (Default=500). The pressure level in hPa or height above ground in meters.         
    
-ct = Convert Temperature (Default=True).

When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.

-tu = Temperature Units (Default=Celsius).

When -ct True this is where you declare the units for temperature to be converted to. 

-lt = Level Type. Type of level (i.e. pressure, height above ground etc.). 
    
Default='pressure'.

***Level Types***

'height_above_ground'

'pressure'

'surface'

'geoid'

'mean_sea_level'

--process = Process Data. This flag when set to True will process the data in addition to downloading the data. (Default=True)

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`

--netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.

***Additional Relevant Flags when --netcdf True***

--ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=CanSIPS/Forecast/NETCDF). 

--ncfname = Defines the filename for the netCDF (.nc) file. (Default=cansips_forecast.nc)

***Complex Example***

1) Download the latest CanSIPS 500mb Geopotential Height Forecast
 
- Use a proxy server of address: `https://proxy-server-address:proxy-server-port` 
            
2) Subset the data to reflect CONUS [-130, -65, 50, 20] = [west, east, north, south]
    
3) Create a netCDF (.nc) file of the data called `cansips_gph_500.nc` saved at Weather_Data/CanSIPS/Forecast/NETCDF.

Linux Shell:
```shell
# Define our coordinates so we don't pass in negative numbers into the command
western_bound=-130
eastern_bound=-65
northern_bound=50
southern_bound=20

wxdata-cansips fetch latest -t forecast -lt pressure -l 500 -v geopotential_height \
-wb=$western_bound -eb=$eastern_bound -nb=$northern_bound -sb=$southern_bound \
--netcdf True --ncdir Weather_Data/CanSIPS/Forecast/NETCDF --ncfname cansips_gph_500.nc \ 
--proxy https://proxy-server-address:proxy-server-port
```
        
Windows Powershell:
```powershell
# Define our coordinates so we don't pass in negative numbers into the command
$WESTERN_BOUND=-130
$EASTERN_BOUND=-65
$NORTHERN_BOUND=50
$SOUTHERN_BOUND=20

wxdata-cansips fetch latest -t forecast -lt pressure -l 500 -v geopotential_height `
-wb=$WESTERN_BOUND -eb=$EASTERN_BOUND -nb=$NORTHERN_BOUND -sb=$SOUTHERN_BOUND `
--netcdf True --ncdir Weather_Data/CanSIPS/Forecast/NETCDF --ncfname cansips_gph_500.nc `
--proxy https://proxy-server-address:proxy-server-port
```
