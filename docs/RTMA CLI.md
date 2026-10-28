---
title: RTMA CLI
---

# Real-Time Mesoscale Analysis (RTMA) Command Line Interface    
    
***Archived Required Commands***

-d = Date. The date of the model run in the format of YYYY-mm-dd.

    (i.e. December 25th, 2025 should be entered as -d 2025-12-25)
    
-r = Run. The model runtime in UTC (0, 6, 12, 18). 

    (i.e. for the 12z run set -r 12)


***Globally Valid Commands (valid for both "latest" and "archived")***

-loc = Location (Default='conus'). Locations: 1) `conus`, 2) `ak` (Alaska), 3) `hi` (Hawaii), 4) `pr` (Puerto Rico), 5) `gu` (Guam).

-c = Category (Default='analysis'). Category choices: 

1) `analysis` - RTMA Analysis

2) `error` - RTMA Error

3) `forecast` - RTMA 1-Hour Forecast

-cr = Clear Recycle Bin (Default=False).

For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
Setting -cr True clears your recycle bin with each run of the script. 
This ensures if any old files are moved to the recycle bin are deleted if they are not already.

-cdir = Custom Directory (Default=None).

If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
The default path is f:RTMA/ANALYSIS. 

-ct = Convert Temperature (Default=True).

When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.

-tu = Temperature Units (Default=Celsius).

When -ct True this is where you declare the units for temperature to be converted to. 

--process This flag when set to True will process the data in addition to downloading the data. (Default=True)

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`

Example: 

`wxdata-rtma fetch latest --proxy https://proxy-server-address:proxy-server-port`

--netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.

***Additional Relevant Flags when --netcdf True***

--ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=RTMA/NETCDF). 

--ncfname = Defines the filename for the netCDF (.nc) file. (Default=rtma.nc)


**Commands Only Valid for "latest"**

-s = Source (Default=noaa). 

Selects the primary data server to use.
If the primary server is unavailable the client will rotate and try other servers.

***Server Choices For Latest Data***

noaa - NCEP/NOMADS

aws - Amazon Web Services

-cd = Clear Data (Default=False). *Only for wxdata-rtma latest*

***Archived Clients Automatically Clear Old Data***

When set to False the scanner safeguard that prevents repetative downloads is enabled.
Set -cd False to disable this safety feature.

WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
retry downloading the data. 
