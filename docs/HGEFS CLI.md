---
title: HGEFS CLI
---
    
# Hybrid Global Ensemble Forecast System (HGEFS) Command Line Interface
    
***Valid Commands***

-c = Category (Default='mean')

This determines the category of ensemble data 

***Categories***

1) mean
    
2) spread
    
-f = Final Forecast Hour (Default=240).
 
The last hour the user wishes to download in the dataset. GEFS0P25 has 240 forecast hours.

-cdir = Custom Directory (Default=None).

If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
The default path is f:HGEFS/{CATEGORY}. 

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

-wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)

-eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)

-nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)

-sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)

-v = Variables(Default=['geopotential height',
                   'specific humidity',
                   'temperature',
                   'u-component of_wind',
                   'v-component of_wind',
                   'vertical velocity']) 
                   
The list of variables the user wants to query.

***Variables***

'geopotential height'

'specific humidity'

'temperature'

'u-component of_wind'

'v-component of_wind'

'vertical velocity'

-l = Levels (Default=[1000,
                        925,
                        850,
                        700,
                        600,
                        500,
                        400,
                        300,
                        250,
                        150,
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

'surface'

'pressure'

--process This flag when set to True will process the data in addition to downloading the data. (Default=True)

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`

--netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.

***Additional Relevant Flags when --netcdf True***

--ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=HGEFS/NETCDF). 

--ncfname = Defines the filename for the netCDF (.nc) file. (Default=hgefs.nc)

***Complex Example***

*Important*: Any parameter of the command not explicitly stated results in the default value being used. 

1) Download the latest HGEFS Ensemble Mean for 500mb Geopotential Height
 
    - Use a proxy server of address: `https://proxy-server-address:proxy-server-port` 
            
2) Subset the data to reflect CONUS [-130, -65, 50, 20] = [west, east, north, south]
    
3) Create a netCDF (.nc) file of the data called `hgefs_mean_gph_500.nc` saved at Weather_Data/HGEFS/NETCDF.

Linux Shell:
```shell
# Define our coordinates so we don't pass in negative numbers into the command
western_bound=-130
eastern_bound=-65
northern_bound=50
southern_bound=20

wxdata-hgefs fetch latest -v geopotential_height -l 500 \
-wb=$western_bound -eb=$eastern_bound -nb=$northern_bound -sb=$southern_bound \
--netcdf True --Weather_Data/HGEFS/NETCDF --ncfname hgefs_mean_gph_500.nc \ 
--proxy https://proxy-server-address:proxy-server-port
```
        
Windows Powershell:
```powershell
# Define our coordinates so we don't pass in negative numbers into the command
$WESTERN_BOUND=-130
$EASTERN_BOUND=-65
$NORTHERN_BOUND=50
$SOUTHERN_BOUND=20

wxdata-hgefs fetch latest -v geopotential_height -l 500 `
-wb=$WESTERN_BOUND -eb=$EASTERN_BOUND -nb=$NORTHERN_BOUND -sb=$SOUTHERN_BOUND `
--netcdf True --Weather_Data/HGEFS/NETCDF --ncfname hgefs_mean_gph_500.nc ` 
--proxy https://proxy-server-address:proxy-server-port
```
