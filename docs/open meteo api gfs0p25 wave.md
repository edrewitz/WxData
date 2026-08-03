---
title: Open-Meteo API GFS0P25 Wave Forecasts
---
[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)
# Open-Meteo API GFS0P25 Wave Forecasts

```python
def gfs_wave_0p25(latitude,
            longitude,
            days=7,
            variables=['wave_height',
                        'wave_direction',
                        'wave_period',
                        'wind_wave_height',
                        'wind_wave_direction',
                        'wind_wave_period',
                        'swell_wave_height',
                        'swell_wave_direction',
                        'swell_wave_period',
                        'secondary_swell_wave_height',
                        'secondary_swell_wave_period',
                        'secondary_swell_wave_direction',
                        'tertiary_swell_wave_height',
                        'tertiary_swell_wave_period',
                        'tertiary_swell_wave_direction'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/Marine Forecasts/NOAA",
            filename=f"GFS_0P25.csv"):
```

This function retrieves the GFS Wave 0.25 Degree forecast from the Open-Meteo API for a given point of latitude/longitude.
    
Required Arguments:

1) latitude (Float or Integer) - Latitude in decimal degrees.

2) longitude (Float or Integer) - Longitude in decimal degrees.

Optional Arguments:

1) days (Integer) - Default=7. Amount of days to go out for the forecast. Maximum is 16.
    
2) variables (String List) - Default=['wave_height',
                                        'wave_direction',
                                        'wave_period',
                                        'wind_wave_height',
                                        'wind_wave_direction',
                                        'wind_wave_period',
                                        'swell_wave_height',
                                        'swell_wave_direction',
                                        'swell_wave_period',
                                        'secondary_swell_wave_height',
                                        'secondary_swell_wave_period',
                                        'secondary_swell_wave_direction',
                                        'tertiary_swell_wave_height',
                                        'tertiary_swell_wave_period',
                                        'tertiary_swell_wave_direction']

            
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

A `Pandas.DataFrame` of the GFS Wave 0.25 Degree forecast for a given point of latitude/longitude. 
