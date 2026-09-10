---
title: Canadian Meteorological Centre GEPS
---

[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)

# Canadian Global Ensemble Prediction System (GEPS)

```python
def geps(final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             step=1,
             path=f"GEPS",
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
             cat='members'):
```

This function retrieves the latest GEPS data from `https://dd.weather.gc.ca/` and returns an `xarray.array` of specified data.

Required Arguments: None

Optional Arguments:

1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEPS
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 1 hour. 

2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

6) step (Integer) - Default=1. Increment in forecast hours (Default=1hrly).

7) path (String) - Default='GEPS'. The parent directory for the GRIB2 files on the local machine.

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
   data via their own external method, set `process_data=False` which means the data will be downloaded but not processed and no values
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
'depth below surface'
'surface'
'mean sea level'
'nominal top'
'entire atmosphere'
```
    
16) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
    When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
17) variable (String) - Default='geopotential height'. The variable the user wishes to download.

18) level (Integer) - Default=500. For parameters that have multiple levels, here is where you select the level to 
    download. Default is 500mb. Units for height above ground are (m) and depth below surface (cm). 
    
19) cat (String) - Default='members'. Set `cat='members'` for all ensemble members OR set `cat='control'` for control run.
    

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

**Returns**

An `xarray.array` of the latest GEPS forecast data for a user-specified variable, `level`/`layer` and `level_type`.

GEPS files are saved to directory {path}  
