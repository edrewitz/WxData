---
title: RDPS CLI
---

# Canadian Global Regional Prediction System (RDPS) Command Line Interface

***Valid Commands***
    
-f = Final Forecast Hour. Default=84.

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

-v = Variable. Variable to pass into the function. 
    
  Default='geopotential_height'
  
  ***Variables & Proper level_type & level***

  Any area where valid_levels = None -> Users do not need to edit the optional argument `level`

  ```python
  'absolute vorticity': 
      valid level type(s): 'pressure'
      valid levels: 
          level_type='pressure' (hPa): 850, 700, 500, 250, 200
      
  'temperature': 
      valid level type(s) = 'pressure', 'height above ground'.
      valid levels:
          level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                              350, 300, 275, 250, 225, 200, 175, 150, 100, 50, 30, 20, 10, 5, 1.
                              
          level_type='height above ground' (m): 2, 40, 80, 120
          
  'albedo':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'cape':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'cin':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
      
  'cloud water':
      valid level type(s): 'entire atmosphere'
      valid levels: None (level_type='entire atmosphere' -> 'entire atmosphere' is the only level)  
      
  'total convective precipitation':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
      
  'dew point depression':
      valid level type(s) = 'pressure', 'height above ground'.
      valid levels:
          level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                              350, 300, 275, 250, 225, 200, 175, 150, 100, 50, 30, 20, 10, 5, 1.
                              
          level_type='height above ground' (m): 2
          
  'dew point':   
      valid level type(s) = 'height above ground'.
      valid levels:                      
          level_type='height above ground' (m): 2
          
  'downward longwave radiation flux':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
      
  'downward shortwave radiation flux':
      valid level type(s): 'surface', 'nominal top'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
                                              OR 
                      (level_type='nominal top' -> 'nominal top' is the only level)  
                      
  'freezing rain accumulation 12hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
      
  'freezing rain accumulation 1hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)   
      
  'freezing rain accumulation 24hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)   
      
  'freezing rain accumulation 3hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
      
  'freezing rain accumulation 6hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
      
  'freezing rain accumulation total':  
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)              
                      
  'geopotential height':
      valid level type(s) = 'pressure', 'surface'.
      valid levels:
          level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                              350, 300, 275, 250, 225, 200, 175, 150, 100, 50, 30, 20, 10, 5, 1.   
                              
          level_type='surface' (surface elevation): None (level_type='surface' -> 'surface' is the only level) 
          
  'humidex':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'ice pellets accumulation 12hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
      
  'ice pellets accumulation 1hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)   
      
  'ice pellets accumulation 24hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)   
      
  'ice pellets accumulation 3hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
      
  'ice pellets accumulation 6hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
      
  'ice pellets accumulation total':  
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)    
      
  'k index':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'land water proportion':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'latent heat net flux'
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'lifted index'
      valid level type(s) = 'pressure'.
      valid levels:
          level_type='pressure' (hPa): 500.
          
  'maximum wind gust':
      valid level type(s) = 'height above ground'.
      valid levels:
          level_type='height above ground' (m): 10 
          
  'minimum wind gust':
      valid level type(s) = 'height above ground'.
      valid levels:
          level_type='height above ground' (m): 10    
          
  'net longwave radiation flux':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'net shortwave radiation flux'  
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'ozone mixing ratio':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'ozone':
      valid level type(s): 'entire atmosphere'
      valid levels: None (level_type='entire atmosphere' -> 'entire atmosphere' is the only level) 
      
  'boundary layer height':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'precipitation type':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'pressure':
      valid level type(s): 'mean sea level', 'potential vorticity surface', 'surface'
      valid_levels: 
          level_type='mean sea level': None (level_type='mean sea level' -> 'mean sea level' is the only level) 
          
          level_type='potential vorticity surface' (PVU): 1, 1.5, 2
          
          level_type='surface': None (level_type='surface' -> 'surface' is the only level) 
          
  'radiative temperature':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'rain accumulation 12hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
      
  'rain accumulation 1hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)   
      
  'rain accumulation 24hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)   
      
  'rain accumulation 3hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
      
  'rain accumulation 6hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
      
  'rain accumulation total':  
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)   
      
  'relative humidity':    
      valid level type(s) = 'pressure', 'height above ground'.
      valid levels:
          level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                              350, 300, 275, 250, 225, 200, 175, 150, 100, 50, 30, 20, 10, 5, 1.
                              
          level_type='height above ground' (m): 2
          
  'relative vorticity': 
      valid level type(s): 'pressure'
      valid levels: 
          level_type='pressure' (hPa): 850, 700, 500, 250, 200
          
  'surface runoff':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'sea ice fraction'
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'sea surface temperature'
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'seeing index':
      valid level type(s): 'entire atmosphere'
      valid levels: None (level_type='entire atmosphere' -> 'entire atmosphere' is the only level) 
      
  'sensible heat net flux'
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'showalter index':
      valid level type(s) = 'pressure'.
      valid levels:
          level_type='pressure' (hPa): 500. 
          
  'sky transparency index': 
      valid level type(s): 'entire atmosphere'
      valid levels: None (level_type='entire atmosphere' -> 'entire atmosphere' is the only level) 
          
  'snow accumulation 12hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
      
  'snow accumulation 1hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)   
      
  'snow accumulation 24hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)   
      
  'snow accumulation 3hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
      
  'snow accumulation 6hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
      
  'snow accumulation total':  
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)   
          
  'snow density':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'snow depth':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'soil temperature':
      valid level type(s): 'surface', 'depth below surface'.
      valid_levels:
          level_type='depth below surface' (cm):
              layers=[0, 10] -> 0cm to 10cm below the surface.
              
          level_type='surface': None (level_type='surface' -> 'surface' is the only level) 
          
  'soil volumetric ice content':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'soil volumetric water content'     
      valid level type(s): 'depth below surface'.
      valid_levels:
          level_type='depth below surface' (cm):
              layers=[0, 10] -> 0cm to 10cm below the surface.
              layers=[0, 1] -> 0cm to 1cm below the surface.
              
  'specific humidity':
      valid level type(s) = 'pressure', 'height above ground'.
      valid levels:
          level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                              350, 300, 275, 250, 225, 200, 175, 150, 100, 50, 30, 20, 10, 5, 1.
                              
          level_type='height above ground' (m): 2, 40, 80, 120
          
  'storm relative helicity':
      valid level type(s): 'eta'
      valid levels: None (level_type='eta' -> 'eta' is the only level)    
      
  'storm severity index':
      valid level type(s): 'eta'
      valid levels: None (level_type='eta' -> 'eta' is the only level)      
  
  'sweat index':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
          
  'thickness':
      valid level type(s): 'pressure layer'.
      valid_levels:
          level_type='pressure layer' (hPa):
              layers=[1000, 500] -> 1000mb to 500mb layer.
              layers=[850, 700] -> 850mb to 700mb layer. 
              layers=[1000, 850] -> 1000mb to 850mb layer. 
              
  'total cloud cover':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'total precitation 12hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level) 
      
  'total precitation 1hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)   
      
  'total precitation 24hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)   
      
  'total precitation 3hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
      
  'total precitation 6hr':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)  
      
  'total precitation total':  
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)   
      
  'total totals index':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'uv index (clear sky)':                  
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'uv index':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'upward longwave radiation flux':
      valid level type(s): 'nominal top'
      valid levels: None (level_type='nominal top' -> 'nominal top' is the only level)
      
  'upward shortwave radiation flux':
      valid level type(s): 'nominal top'
      valid levels: None (level_type='nominal top' -> 'nominal top' is the only level)
      
  'vertical velocity':
      valid level type(s): 'pressure'
      valid levels: 
          level_type='pressure' (hPa): 850, 700, 500, 250, 200
          
  'wind chill':
      valid level type(s): 'surface'
      valid levels: None (level_type='surface' -> 'surface' is the only level)
      
  'wind direction':
      valid level type(s) = 'pressure', 'height above ground'.
      valid levels:
          level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                              350, 300, 275, 250, 225, 200, 175, 150, 100, 50, 30, 20, 10, 5, 1.
                              
          level_type='height above ground' (m): 10, 40, 80, 120
          
  'wind gust':
      valid level type(s) = 'height above ground'.
      valid levels:
          level_type='height above ground' (m): 10 
          
  'wind speed':
      valid level type(s) = 'pressure', 'height above ground'.
      valid levels:
          level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                              350, 300, 275, 250, 225, 200, 175, 150, 100, 50, 30, 20, 10, 5, 1.
                              
          level_type='height above ground' (m): 10, 40, 80, 120
          
  'u-component of wind':
      valid level type(s) = 'pressure', 'height above ground'.
      valid levels:
          level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                              350, 300, 275, 250, 225, 200, 175, 150, 100, 50, 30, 20, 10, 5, 1.
                              
          level_type='height above ground' (m): 10, 40, 80, 120
          
  'v-component of wind':
      valid level type(s) = 'pressure', 'height above ground'.
      valid levels:
          level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                              350, 300, 275, 250, 225, 200, 175, 150, 100, 50, 30, 20, 10, 5, 1.
                              
          level_type='height above ground' (m): 10, 40, 80, 120
          
  'vertical wind shear':
      valid level type(s): 'eta'
      valid levels: None (level_type='eta' -> 'eta' is the only level)     
  ```
            
-l = Level. The pressure level in hPa or height above ground in meters.
                
  Default=500 hPa
      
-la = Layer. Default=[1000, 500]. 
      
    For level types that correspond to a layer (i.e. 'pressure layer' & 'depth below surface')
    here is where you define the layer. Layers are in the following format for each level_type:
    
level_type='pressure layer': -> layer=[lower level, upper level] (i.e. layer=[1000, 500] for 1000mb to 500mb layer).

level_type='depth below surface': -> layer=[upper level, lower level] (i.e. layer=[0, 10] for 0cm to 10cm below the surface).          
    
-lt = Level Type. Type of level (i.e. pressure, height above ground etc.). 
    
  Default='pressure'.
    
  ***Level Types***

  'pressure'
  
  'height above ground'
  
  'potential vorticity surface'
  
  'pressure layer'
  
  'depth below surface'
  
  'surface'
  
  'mean sea level'
  
  'nominal top'
  
  'entire atmosphere'
  
  'eta'
    
--process This flag when set to True will process the data in addition to downloading the data. (Default=True)

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`

--netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.

***Additional Relevant Flags when --netcdf True***

--ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=RDPS/NETCDF). 

--ncfname = Defines the filename for the netCDF (.nc) file. (Default=rdps.nc)

***Complex Example***

1) Download the latest RDPS for 2-meter temperature 
 
  - Use a proxy server of address: `https://proxy-server-address:proxy-server-port` 
                
2) Create a netCDF (.nc) file of the data called `rdps_t2m.nc` saved at Weather_Data/RDPS/NETCDF.

Linux Shell:
```shell
wxdata-rdps fetch latest -lt height_above_ground -l 2 -v temperature \
--netcdf True --ncdir Weather_Data/RDPS/NETCDF --ncfname rdps_t2m.nc \ 
--proxy https://proxy-server-address:proxy-server-port
```
        
Windows Powershell:
```powershell
wxdata-rdps fetch latest -lt height_above_ground -l 2 -v temperature `
--netcdf True --ncdir Weather_Data/RDPS/NETCDF --ncfname rdps_t2m.nc ` 
--proxy https://proxy-server-address:proxy-server-port
```
