# Open-Meteo API NBM

```python
def nbm_hourly_point_forecast(latitude,
            longitude,
            days=7,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m',
                        'cape',
                        'precipitation',
                        'snowfall',
                        'surface_pressure',
                        'visibility',
                        'wind_speed_10m',
                        'wind_speed_80m',
                        'wind_direction_10m',
                        'wind_direction_80m'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/NOAA/NBM",
            filename=f"NBM_Data.csv"):
```

    This function retrieves NBM time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) days (Integer) - Default=7. Amount of days to go out for the forecast. Maximum is 16.
    
    2) temperature_units (String) - Default='fahrenheit'. The units for temperature.
    
        Valid Temperature Units
        -----------------------
        
        1) fahrenheit
        2) celsius
        
    3) wind_speed_units (String) - Default='mph'. The units for wind speed. 
    
        Valid Wind Speed Units
        ----------------------
        
        1) mph - miles per hour
        2) kmh - kilometers per hour
        3) ms - meters per second
        4) kn - knots
        
    4) precipitation_units (String) - Default='inch'. The units for precipitation amounts.
    
        Valid Precipitation Units
        -------------------------
        
        1) inch - inches
        2) mm - millimeters
        
    5) variables (String List) - Default=['temperature_2m',
                                            'cape',
                                            'precipitation',
                                            'snowfall',
                                            'surface_pressure',
                                            'visibility',
                                            'wind_speed_10m',
                                            'wind_speed_80m',
                                            'wind_direction_10m',
                                            'wind_direction_80m']
                                            
                The list of variables to choose from.
                
    6) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    7) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} wth {filename}
    
    8) path (String) - The path where the CSV file is saved to.
    
    9) filename (String) - The filename for the CSV file.                      
                    
    Returns
    -------
    
    A Pandas.DataFrame of the NBM time series forecast for a given point of latitude/longitude. 
