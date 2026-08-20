---
title: Canadian Meteorological Centre HRDPS
---

[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)

# Canadian High Resolution Deterministic Prediction System (HRDPS)

```python
def hrdps(final_forecast_hour=48, 
             step=1,
             path=f"HRDPS",
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

This function retrieves the latest HRDPS data from `https://dd.weather.gc.ca/` and returns an `xarray.array` of specified data.

Required Arguments: None

Optional Arguments:

1) final_forecast_hour (Integer) - Default = 48. The final forecast hour the user wishes to download. The HRDPS
    goes out to 48 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    48 by the nereast increment of 1 hour. 

2) step (Integer) - Default=1. Increment in forecast hours (Default=1hrly).

3) path (String) - Default='HRDPS'. The parent directory for the GRIB2 files on the local machine.

4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

  ```python
   proxies=None ---> proxies={
                           'http':'http://your-proxy-address:port',
                           'https':'http://your-proxy-address:port'
                           }
  ```

5) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
    with each run of the program you are calling WxData. This setting is to help preserve memory on the machine.
    
6) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
   data via their own external method, set process_data=False which means the data will be downloaded but not processed and no values
   returned to the user.
   
7) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
    either Celsius or Fahrenheit. When False, this data remains in Kelvin.
    
8) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
    Set convert_to='fahrenheit' for Fahrenheit. 
    
9) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.

10) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}

11) level_type (String) - Default='pressure'. The type of level for the variable.

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
'eta'
```
    
12) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
    When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
13) variable (String) - Default='geopotential height'. The variable the user wishes to download.

14) level (Integer or Float) - Default=500. For parameters that have multiple levels, here is where you select the level to 
    download. Default is 500mb. An example of where this can be a floating point is 1.5 for 1.5 PVU. 
    
15) layer (Integer List) - Default=[1000, 500]. For level types that correspond to a layer (i.e. 'pressure layer' & 'depth below surface')
    here is where you define the layer. Layers are in the following format for each level_type:
    
    level_type='pressure layer': -> layer=[lower level, upper level] (i.e. layer=[1000, 500] for 1000mb to 500mb layer).
    
    level_type='depth below surface': -> layer=[upper level, lower level] (i.e. layer=[0, 10] for 0cm to 10cm below the surface).


***Variables & Proper level_type & level***

Any area where valid_levels = None -> Users do not need to edit the optional argument `level`

```python
'air density':
    valid level type(s) = 'height above ground', 'surface'.
    valid levels:
        level_type='height above ground' (m): 40, 80, 120 
        
        level_type='surface': None (level_type='surface' -> 'surface' is the only level) 


'absolute vorticity':
    valid level type(s): 'pressure'
    valid levels: 
        level_type='pressure' (hPa): 1000, 850, 700, 500, 250


'albedo':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'blowing snow':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'boundary layer height':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'cape':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'character of precipitation':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'cloud water':
    valid level type(s): 'entire atmosphere'
    valid levels: None (level_type='entire atmosphere' -> 'entire atmosphere' is the only level)  


'conditional freezing precipitation':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'conditional amount of liquid precipitation':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'conditional amount of solid ice pellets':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'conditional amount of solid snow':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'conditional precipitation rate':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'convective precipitation':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'dew point depression':
    valid level type(s) = 'pressure', 'height above ground'.
    valid levels:
        level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                            350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                            
        level_type='height above ground' (m): 2, 40, 80, 120


'dew point':
    valid level type(s) = 'height above ground', 'surface'.
    valid levels:                      
        level_type='height above ground' (m): 2, 40, 80, 120
        
        level_type='surface': None (level_type='surface' -> 'surface' is the only level) 


'dominant precipitation type':
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
    valid levels: (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                               350, 300, 275, 250, 225, 200, 175, 150, 100, 50.   

'latent heat net flux':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)   


'lifted index':
    valid level type(s) = 'pressure'.
    valid levels:
        level_type='pressure' (hPa): 500.


'mean sea level pressure':
    valid level type(s): 'mean sea level'.
    valid_levels: None (level_type='mean sea level' -> 'mean sea level' is the only level) 

'net longwave radiation flux':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'net shortwave radiation flux':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'snow level height':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'humidex':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'orography':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'precipitation rate':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'precipitation type':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'pressure':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'probability of blowing snow':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'probability of drizzle':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'probability of freezing drizzle':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'probability of freezing precipitation':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'probability of freezing rain':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'probability of ice pellets':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'probability of liquid precipitation':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'probability of precipitation':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'probability of rain':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'probability of snow squalls':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'probability of snow':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'probability of thunderstorms':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'relative humidity':
    valid level type(s) = 'pressure', 'height above ground'.
    valid levels:
        level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                            350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                            
        level_type='height above ground' (m): 2, 40, 80, 120

'sea ice fraction':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'secondary precipitation type':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'sensible heat net flux':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'showalter index':
    valid level type(s) = 'pressure'.
    valid levels:
        level_type='pressure' (hPa): 500.

'skin temperature':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'sky state':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'snow density':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'snow depth water equivalent':
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
        

'specific humidity':
    valid level type(s) = 'pressure', 'height above ground', 'surface'.
    valid levels:
        level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                               350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                               
        level_type='height above ground' (m): 2, 40, 80, 120
        
        level_type='surface': None (level_type='surface' -> 'surface' is the only level) 

'storm relative helicity':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'surface runoff':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'sweat index':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'temperature':
    valid level type(s) = 'pressure', 'height above ground'.
    valid levels:
        level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                               350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                               
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


'total precipitation intensity index':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'total precipitation':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)


'upward longwave radiation flux':
    valid level type(s): 'nominal top'
    valid levels: None (level_type='nominal top' -> 'nominal top' is the only level)


'upward shortwave radiation flux':
    valid level type(s): 'nominal top'
    valid levels: None (level_type='nominal top' -> 'nominal top' is the only level)


'uv index':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'uv index (clear sky)':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'ventilation index':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'vertical wind shear':
    valid level type(s): 'eta'
    valid levels: None (level_type='eta' -> 'eta' is the only level) 

'vertical velocity':
    valid level type(s): 'pressure'
    valid levels: 
        level_type='pressure' (hPa): 1000, 850, 700, 500, 250

'visibility through ice fog':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'visibility through liquid fog':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'land sea mask':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'wind chill':
    valid level type(s): 'surface'
    valid levels: None (level_type='surface' -> 'surface' is the only level)

'wind direction':
    valid level type(s) = 'pressure', 'height above ground'.
    valid levels:
        level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                               350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                               
        level_type='height above ground' (m): 10, 40, 80, 120

'wind gust':
    valid level type(s) = 'pressure', 'height above ground'.
    valid levels:
        level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                               350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                               
        level_type='height above ground' (m): 10, 40, 80, 120

'wind speed':
    valid level type(s) = 'pressure', 'height above ground'.
    valid levels:
        level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                               350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                               
        level_type='height above ground' (m): 10, 40, 80, 120

'u-wind component':
    valid level type(s) = 'pressure', 'height above ground'.
    valid levels:
        level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                               350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                               
        level_type='height above ground' (m): 10, 40, 80, 120

'v-wind component':
    valid level type(s) = 'pressure', 'height above ground'.
    valid levels:
        level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                               350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                               
        level_type='height above ground' (m): 10, 40, 80, 120

```
**Returns**
    
An `xarray.array` of the latest HRDPS forecast data for a user-specified variable, `level`/`layer` and `level_type`.

HRDPS files are saved to directory {path}  
