---
title: GEPS CLI
---

# Canadian Global Ensemble Prediction System (GEPS) Command Line Interface

Canadian Global Ensemble Prediction System (GEPS) Command Line Interface

***Valid Commands***

-f = Final Forecast Hour. Default=384.

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

-cdir = Custom Directory (Default=None).

If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.

-ct = Convert Temperature (Default=True).

When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.

-tu = Temperature Units (Default=Celsius).

When -ct True this is where you declare the units for temperature to be converted to. 

-wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)

-eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)

-nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)

-sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)

-v = Variable. Variable to pass into the function. 
    
  Default='geopotential_height'
  
  ***Variables & Proper level_type & level***
  
  Any area where valid_levels = None -> Users do not need to edit the optional argument `level`

  ```python
  'temperature': 
      valid level type(s) = 'pressure', 'height above ground'.
      valid levels:
          level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                              
          level_type='height above ground' (m): 2, 40, 80, 120
      
  'cape':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'cin':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
          
  'downward longwave radiation flux':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
      
  'downward shortwave radiation flux':
      valid level type(s): 'surface', 'nominal top'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
                                              OR 
                      (level_type='nominal top' -> 'nominal top' is the only level)              
                      
  'geopotential height':
      valid level type(s) = 'pressure'.
      valid levels:
          level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10. 
                                              
  'ice pellets accumulation':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)   
      
  'total convective precipitation':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)   

  'freezing rain accumulation':  
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
      
  'rain accumulation':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
  
  'snow accumulation':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
      
  'latent heat net flux':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
      
  'outgoing longwave radiation':
      valid level type(s): 'nominal top'
      valid levels: None (level_type='nominal top' -> 'nominal top' is the only level) 
      
  'sea ice thickness':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
      
  'pressure':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
      
  'mean sea level pressure':
      valid level type(s): 'mean sea level'
      valid levels: None (level_type='mean sea level' -> 'mean sea level' is the only level) 
      
  'precipitable water':
      valid level type(s): 'entire atmosphere'
      valid levels: None (level_type='entire atmosphere' -> 'entire atmosphere' is the only level) 
      
  'relative humidity':
      valid level type(s) = 'pressure', 'height above ground'.
      valid levels:
          level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                              
          level_type='height above ground' (m): 2
          
  'surface runoff':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
      
  'sensible heat net flux':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
      
  'snow depth':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
      
  'specific humidity':
      valid level type(s) = 'height above ground'.
      valid levels:
          level_type='height above ground' (m): 2, 40, 80, 120.
  
  'soil moisture':
      valid level type(s) = 'depth below surface'.
      valid levels:
          level_type='height above ground' (cm): 10.
          
  'total cloud cover':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
      
  'maximum temperature':
      valid level type(s) = 'height above ground'.
      valid levels:
          level_type='height above ground' (m): 2.
          
  'minimum temperature':
      valid level type(s) = 'height above ground'.
      valid levels:
          level_type='height above ground' (m): 2.
          
  'soil temperature':
      valid level type(s) = 'depth below surface'.
      valid levels:
          level_type='height above ground' (cm): 10.
          
  'u-wind component':
      valid level type(s) = 'pressure', 'height above ground'.
      valid levels:
          level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                              
          level_type='height above ground' (m): 10.
          
  'v-wind component':
      valid level type(s) = 'pressure', 'height above ground'.
      valid levels:
          level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                              
          level_type='height above ground' (m): 10.
          
  'upward longwave radiation flux':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
      
  'upward shortwave radiation flux':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
      
  'vertical velocity':
      valid level type(s) = 'pressure'.
      valid levels:
          level_type='pressure' (hPa): 850.
          
  'wind speed':
      valid level type(s) = 'height above ground'.
      valid levels:
          level_type='height above ground' (m): 2, 40, 80, 120.   
  ```
            
-l = Level. The pressure level in hPa or height above ground in meters.
                
  Default=500 hPa     
    
-lt = Level Type. Type of level (i.e. pressure, height above ground etc.). 
    
  Default='pressure'.
  
  ***Level Types***

  'pressure'
  
  'height above ground'
  
  'depth below surface'
  
  'surface'
  
  'mean sea level'
  
  'nominal top'
  
  'entire atmosphere'
    
--process This flag when set to True will process the data in addition to downloading the data. (Default=True)

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`

--netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.

***Additional Relevant Flags when --netcdf True***

--ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=GEPS/NETCDF). 

--ncfname = Defines the filename for the netCDF (.nc) file. (Default=geps.nc)

***Complex Example***

1) Download the latest GEPS for 2-meter temperature 
 
- Use a proxy server of address: `https://proxy-server-address:proxy-server-port` 
            
2) Subset the data to reflect CONUS [-130, -65, 50, 20] = [west, east, north, south]
    
3) Create a netCDF (.nc) file of the data called `geps_t2m.nc` saved at Weather_Data/GEPS/NETCDF.

Linux Shell:
```shell
# Define our coordinates so we don't pass in negative numbers into the command
western_bound=-130
eastern_bound=-65
northern_bound=50
southern_bound=20

wxdata-geps fetch latest -lt height_above_ground -l 2 -v temperature \
-wb=$western_bound -eb=$eastern_bound -nb=$northern_bound -sb=$southern_bound \
--netcdf True --ncdir Weather_Data/GEPS/NETCDF --ncfname geps_t2m.nc \ 
--proxy https://proxy-server-address:proxy-server-port
```
        
Windows Powershell:
```powershell
# Define our coordinates so we don't pass in negative numbers into the command
$WESTERN_BOUND=-130
$EASTERN_BOUND=-65
$NORTHERN_BOUND=50
$SOUTHERN_BOUND=20

wxdata-geps fetch latest -lt height_above_ground -l 2 -v temperature `
-wb=$WESTERN_BOUND -eb=$EASTERN_BOUND -nb=$NORTHERN_BOUND -sb=$SOUTHERN_BOUND `
--netcdf True --ncdir Weather_Data/GEPS/NETCDF --ncfname geps_t2m.nc ` 
--proxy https://proxy-server-address:proxy-server-port
```
