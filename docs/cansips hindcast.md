---
title: Canadian Meteorological Centre CanSIPS Hindcast
---

[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)

# Canadian Seasonal to Inter-annual Prediction System (CanSIPS) Hindcast

```python
def cansips_hindcast(western_bound=-180,
                     eastern_bound=180,
                     northern_bound=90,
                     southern_bound=-90,
                     level_type='pressure',
                     level=500,
                     variable='geopotential height',
                     proxies=None,
                     clear_recycle_bin=False,
                     convert_temperature=True,
                     convert_to='celsius',
                     process_data=True,
                     path=f"CanSIPS/Hindcast",
                     chunk_size=8192,
                     notifications='off',
                     clear_data=False):
```

This function is a client that retrieves the CanSIPS Hindcast Data for the current month and calculates the
30-year ensemble mean (40 ensemble members) to find anomalies when comparing to the CanSIPS forecast as described [here](https://eccc-msc.github.io/open-data/msc-data/nwp_cansips/readme_cansips-datamart_en/)

TLDR Process for calculating 30-year mean:

1) Find the ensemble mean for each year of the CanSIPS Hindcast data.

2) Find the time mean from all 30 ensemble means.

Required Arguments: None

Optional Arguments:

1) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

2) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

3) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

4) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

5) level_type (String) - The type of level surface for the variable.

***Level Types***

```python
'height above ground'
'pressure'
'surface'
'geoid'
'mean sea level'
```
    
6) level (Integer) - The pressure level in hPa or height above ground in meters.

7) variable (String) - Variable the user is requesting.

***Variable List***

```python
'temperature'
'geopotential height'
'precipitation rate'
'pressure'
'sea surface height'
'sea surface temperature'
'u-wind component'
'v-wind component'
```
    
8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

  ```python
   proxies=None ---> proxies={
                           'http':'http://your-proxy-address:port',
                           'https':'http://your-proxy-address:port'
                           }
  ```                           
9) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
    with each run of the program you are calling WxData. This setting is to help preserve memory on the machine.
    
10) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
    either Celsius or Fahrenheit. When False, this data remains in Kelvin.
    
11) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
    Set convert_to='fahrenheit' for Fahrenheit. 
    
12) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
   data via their own external method, set process_data=False which means the data will be downloaded but not processed and no values
   returned to the user.
   
13) path (String) - Default="CanSIPS/Hindcast". 
   The parent directory for the GRIB2 files on the local machine.
   
14) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.

15) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}

16) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
    When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
***Variables & Proper level_type & level & category & period***

```python
'temperature':
    valid level type(s): 'pressure', 'height above ground'.
    valid levels:
        level_type='pressure' (hPa): 850.                              
        level_type='height above ground' (m): 2.
    
'geopotential height':
    valid level type(s): 'pressure'.
    valid_levels: 500 (hPa)

'precipitation rate':    
    valid level type(s): 'surface'.
    valid levels: N/A - User does not need to change around anything here as the only level is surface.
    
'pressure':
    valid level type(s): 'mean sea level'.
    valid levels: N/A - User does not need to change around anything here as the only level is mean sea level.
    
'sea surface height':        
    valid level type(s): 'geoid'.
    valid levels: N/A - User does not need to change around anything here as the only level is geoid.
    
'sea surface temperature':
    valid level type(s): 'surface'.
    valid levels: N/A - User does not need to change around anything here as the only level is surface.
    
'u-wind component':
    valid level type(s): 'pressure'.
    valid levels: 850, 200 (hPa).
    
'v-wind component':
    valid level type(s): 'pressure'.
    valid levels: 850, 200 (hPa).
```

**Returns**

An `xarray.array` of the 30-year mean of the CanSIPS Hindcast data that corresponds to the month of the current
CanSIPS Forecast for the purpose of finding anomalies in the forecast data.   
