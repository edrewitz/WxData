---
title: Canadian Meteorological Centre GDPS
---

[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)

# Canadian Meteorological Centre: GDPS

```python
def gdps(final_forecast_hour=240, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             step=1,
             path=f"GDPS",
             proxies=None, 
             clear_recycle_bin=False,
             process_data=True,
             convert_temperature=True,
             convert_to='celsius',
             chunk_size=8192,
             notifications='off',
             level_type='pressure',
             clear_data=False,
            variable='geopotential height',
            level=500,
            layer=[1000, 500]):
```

This function retrieves the latest GDPS data from *https://dd.weather.gc.ca/* and returns an xarray.array of specified data.

Required Arguments: None

Optional Arguments:

1) final_forecast_hour (Integer) - Default = 240. The final forecast hour the user wishes to download. The GDPS
  goes out to 240 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
  240 by the nereast increment of 6 hours. 

2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

6) step (Integer) - Default=1. Increment in forecast hours (Default=1hrly).

7) path (String) - Default='GDPS'. The parent directory for the GRIB2 files on the local machine.

8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

```python
 proxies=None ---> proxies={
                         'http':'http://your-proxy-address:port',
                         'https':'http://your-proxy-address:port'
                         }
```                    
9) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
  with each run of the program you are calling WxData. This setting is to help preserve memory on the machine.
  
10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
 data via their own external method, set process_data=False which means the data will be downloaded but not processed and no values
 returned to the user.
 
11) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
  either Celsius or Fahrenheit. When False, this data remains in Kelvin.
  
12) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
  Set convert_to='fahrenheit' for Fahrenheit. 
  
13) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.

14) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}

15) level_type (String) - Default='pressure'. The type of level for the variable.

  ***Level Types***

```python
'pressure'
'height above ground'
'potential vorticity surface'
'pressure layer'
'depth below surface'
'surface'
'mean sea level'
'nominal top'
'entire atmosphere'
```
        
16) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
    When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
17) variable (String) - Default='geopotential height'. The variable the user wishes to download.

18) level (Integer or Float) - Default=500. For parameters that have multiple levels, here is where you select the level to 
    download. Default is 500mb. An example of where this can be a floating point is 1.5 for 1.5 PVU. 
    
19) layer (Integer List) - Default=[1000, 500]. For level types that correspond to a layer (i.e. 'pressure layer' & 'depth below surface')
    here is where you define the layer. Layers are in the following format for each level_type:
    
    level_type='pressure layer': -> layer=[lower level, upper level] (i.e. layer=[1000, 500] for 1000mb to 500mb layer).
    
    level_type='depth below surface': -> layer=[upper level, lower level] (i.e. layer=[0, 10] for 0cm to 10cm below the surface).
    
    
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
    
'sensible heat net flux'
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)
    
'showalter index':
    valid level type(s) = 'pressure'.
    valid levels:
        level_type='pressure' (hPa): 500.  
        
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
```          
**Returns**

An `xarray.array` of the latest GDPS forecast data for a user-specified variable, `level`/`layer` and `level_type`.

GDPS files are saved to directory `{path}` 
