# Open-Meteo API GEM Ensemble

```python
def gem_hourly_ensemble_point_forecast(latitude,
            longitude,
            days=7,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m',
                        'relative_humidity_2m',
                        'dew_point_2m',
                        'apparent_temperature',
                        'precipitation',
                        'rain',
                        'snowfall',
                        'snow_depth',
                        'weather_code',
                        'pressure_msl',
                        'cloud_cover',
                        'surface_pressure',
                        'et0_fao_evapotranspiration',
                        'vapour_pressure_deficit',
                        'wind_speed_10m',
                        'wind_direction_10m',
                        'temperature_850hPa',
                        'temperature_500hPa',
                        'geopotential_height_850hPa',
                        'geopotential_height_500hPa'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/CMC/GEM Ensemble",
            filename=f"GEM_Ensemble_Data.csv"):
```

    This function retrieves GEM Ensemble time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) days (Integer) - Default=7. Amount of days to go out for the forecast. Maximum is 36.
    
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
                                            'relative_humidity_2m',
                                            'dew_point_2m',
                                            'apparent_temperature',
                                            'precipitation',
                                            'rain',
                                            'snowfall',
                                            'snow_depth',
                                            'weather_code',
                                            'pressure_msl',
                                            'cloud_cover',
                                            'surface_pressure',
                                            'et0_fao_evapotranspiration',
                                            'vapour_pressure_deficit',
                                            'wind_speed_10m',
                                            'wind_direction_10m',
                                            'temperature_850hPa',
                                            'temperature_500hPa',
                                            'geopotential_height_850hPa',
                                            'geopotential_height_500hPa']
                                            
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
    
    A Pandas.DataFrame of the GEM Ensemble time series forecast for a given point of latitude/longitude. 
