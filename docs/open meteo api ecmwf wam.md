---
title: Open-Meteo API ECMWF WAM
---
[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)
# Open-Meteo API ECMWF WAM

```python
def ecmwf_wam(latitude,
            longitude,
            days=7,
            variables=['wave_height',
                        'wave_direction',
                        'wave_period',
                        'wave_peak_period'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/Marine Forecasts/ECMWF",
            filename=f"ECMWF_WAM.csv"):
```

This function retrieves the ECMWF WAM forecast from the Open-Meteo API for a given point of latitude/longitude.
    
Required Arguments:

1) latitude (Float or Integer) - Latitude in decimal degrees.

2) longitude (Float or Integer) - Longitude in decimal degrees.

Optional Arguments:

1) days (Integer) - Default=7. Amount of days to go out for the forecast. Maximum is 16.
    
2) variables (String List) - Default=['wave_height',
                                        'wave_direction',
                                        'wave_period',
                                        'wave_peak_period']
            
3) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:
  ```python
    proxies=None ---> proxies={
                           'http':'http://your-proxy-address:port',
                           'https':'http://your-proxy-address:port'
                           }
  ```
4) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}

5) path (String) - The path where the CSV file is saved to.

6) filename (String) - The filename for the CSV file.                     
                
**Returns**

A `Pandas.DataFrame` of the ECMWF WAM forecast for a given point of latitude/longitude. 
