---
title: Canadian Meteorological Centre CanSIPS
---

[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)

# Canadian Seasonal to Inter-annual Prediction System (CanSIPS)

```python
def cansips(western_bound=-180,
            eastern_bound=180,
            northern_bound=90,
            southern_bound=-90,
            variable='geopotential height',
            level=500,
            level_type='pressure',
            period='monthly',
            category=None,
            proxies=None,
            path=f"CanSIPS/Geopotential Height/500mb/Monthly",
            chunk_size=8192,
            notifications='off',
            clear_data=False,
            clear_recycle_bin=False,
            convert_temperature=True,
            convert_to='celsius',
            process_data=True):
```

This function retrieves the latest CanSIPS data from `https://dd.weather.gc.ca/` and returns an `xarray.array` of specified data.

Required Arguments: None

Optional Arguments:

1) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

2) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

3) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

4) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

5) variable (String) - Variable the user is requesting.

***Variable List***

```python
'temperature'
'geopotential height'
'precipitation'
'precipitation rate'
'pressure'
'sea surface height'
'sea surface temperature'
'u-wind component'
'v-wind component'
```
    
6) level (Integer) - The pressure level in hPa or height above ground in meters.

7) level_type (String) - The type of level surface for the variable.

***Level Types***

```python
'height above ground'
'pressure'
'surface'
'geoid'
'mean sea level'
```
    
8) period (String) - The forecast increment (monthly or seasonal [3-month])

9) category (String or None) - The type of probabilistic category. If not requesting a probabilistic forecast set this to None.

***Category List***

```python
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
```

10) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

  ```python
   proxies=None ---> proxies={
                           'http':'http://your-proxy-address:port',
                           'https':'http://your-proxy-address:port'
                           }
  ```

11) path (String) - Default="CanSIPS/Geopotential Height/500mb/Monthly". 
   The parent directory for the GRIB2 files on the local machine.
   
12) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.

13) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}

14) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
    When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
15) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
    with each run of the program you are calling WxData. This setting is to help preserve memory on the machine.
    
16) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
    either Celsius or Fahrenheit. When False, this data remains in Kelvin.
    
17) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
    Set convert_to='fahrenheit' for Fahrenheit. 
    
18) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
   data via their own external method, set process_data=False which means the data will be downloaded but not processed and no values
   returned to the user.
   
***Variables & Proper level_type & level & category & period***

```python
'temperature':
    valid level type(s): 'pressure', 'height above ground'.
    valid levels:
        level_type='pressure' (hPa): 850.                              
        level_type='height above ground' (m): 2.
    valid categories: 
        level_type='height above ground':
            1)  'probability above normal'
            2)  'probability below normal'
            3)  'probability near normal'
            4)   'probability > 10th percentile'
            5)   'probability > 20th percentile'
            6)   'probability > 30th percentile'
            7)   'probability > 40th percentile'
            8)   'probability > 50th percentile'
            9)   'probability > 60th percentile'
            10)  'probability > 70th percentile'
            11)  'probability > 80th percentile'
            12)  'probability > 90th percentile'
        
        level_type='pressure':
            1) None (There are no probabilistic forecasts for this level_type)
    valid_period(s): 'seasonal', 'monthly'.
    
'geopotential height':
    valid level type(s): 'pressure'.
    valid_levels: 500 (hPa)
    valid categories: None (There are no probabilistic forecasts for this level_type)
    valid period(s): 'monthly'. 
    
'precipitation':
    valid level type(s): 'surface'.
    valid levels: N/A - User does not need to change around anything here as the only level is surface.
    valid categories: 
        1)  'probability above normal'
        2)  'probability below normal'
        3)  'probability near normal'
        4)   'probability > 10th percentile'
        5)   'probability > 20th percentile'
        6)   'probability > 30th percentile'
        7)   'probability > 40th percentile'
        8)   'probability > 50th percentile'
        9)   'probability > 60th percentile'
        10)  'probability > 70th percentile'
        11)  'probability > 80th percentile'
        12)  'probability > 90th percentile'
        
    valid_period(s): 'seasonal', 'monthly'.

'precipitation rate':    
    valid level type(s): 'surface'.
    valid levels: N/A - User does not need to change around anything here as the only level is surface.
    valid categories: None (There are no probabilistic forecasts for this level_type)
    valid period(s): 'monthly'. 
    
'pressure':
    valid level type(s): 'surface'.
    valid levels: N/A - User does not need to change around anything here as the only level is surface.
    valid categories: None (There are no probabilistic forecasts for this level_type)
    valid period(s): 'monthly'. 
    
'sea surface height':        
    valid level type(s): 'geoid'.
    valid levels: N/A - User does not need to change around anything here as the only level is geoid.
    valid categories: None (There are no probabilistic forecasts for this level_type)
    valid period(s): 'monthly'. 
    
'sea surface temperature':
    valid level type(s): 'surface'.
    valid levels: N/A - User does not need to change around anything here as the only level is surface.
    valid categories: None (There are no probabilistic forecasts for this level_type)
    valid period(s): 'monthly'. 
    
'u-wind component':
    valid level type(s): 'pressure'.
    valid levels: 850, 200 (hPa).
    valid categories: None (There are no probabilistic forecasts for this level_type)
    valid period(s): 'monthly'.  
    
'v-wind component':
    valid level type(s): 'pressure'.
    valid levels: 850, 200 (hPa).
    valid categories: None (There are no probabilistic forecasts for this level_type)
    valid period(s): 'monthly'. 
```

**Returns**

An `xarray.array` of the requested CanSIPS data.    
