---
title: Open-Meteo API Meteo-France Ocean Currents
---
[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)

# Open-Meteo API Meteo-France Ocean Currents

```python
def meteo_france_ocean_currents(latitude,
            longitude,
            days=7,
            variables=['sea_level_height_msl',
                        'sea_surface_temperature',
                        'ocean_current_velocity',
                        'ocean_current_direction'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/Marine Forecasts/Meteo France",
            filename=f"Meteo_France_Ocean_Currents.csv"):
```

This function retrieves the Meteo-France Ocean Currents forecast from the Open-Meteo API for a given point of latitude/longitude.

Required Arguments:

1) latitude (Float or Integer) - Latitude in decimal degrees.

2) longitude (Float or Integer) - Longitude in decimal degrees.

Optional Arguments:

1) days (Integer) - Default=7. Amount of days to go out for the forecast. Maximum is 16.
    
2) variables (String List) - Default=['sea_level_height_msl',
                                        'sea_surface_temperature',
                                        'ocean_current_velocity',
                                        'ocean_current_direction']

            
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

A `Pandas.DataFrame` of the Meteo-France Ocean Currents forecast for a given point of latitude/longitude. 
