# Open-Meteo API HGEFS

```python
def hgefs_hourly_point_forecast(latitude,
            longitude,
            days=7,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m',
                        'cloud_cover',
                        'cloud_cover_low',
                        'cloud_cover_mid',
                        'cloud_cover_high',
                        'precipitation',
                        'pressure_msl',
                        'temperature_1000hPa',
                        'temperature_925hPa',
                        'temperature_850hPa',
                        'temperature_700hPa',
                        'temperature_600hPa',
                        'temperature_500hPa',
                        'temperature_400hPa',
                        'temperature_300hPa',
                        'temperature_250hPa',
                        'temperature_200hPa',
                        'temperature_150hPa',
                        'temperature_100hPa',
                        'temperature_50hPa',
                        'dew_point_1000hPa',
                        'dew_point_925hPa',
                        'dew_point_850hPa',
                        'dew_point_700hPa',
                        'dew_point_600hPa',
                        'dew_point_500hPa',
                        'dew_point_400hPa',
                        'dew_point_300hPa',
                        'dew_point_250hPa',
                        'dew_point_200hPa',
                        'dew_point_150hPa',
                        'dew_point_100hPa',
                        'dew_point_50hPa',
                        'relative_humidity_1000hPa',
                        'relative_humidity_925hPa',
                        'relative_humidity_850hPa',
                        'relative_humidity_700hPa',
                        'relative_humidity_600hPa',
                        'relative_humidity_500hPa',
                        'relative_humidity_400hPa',
                        'relative_humidity_300hPa',
                        'relative_humidity_250hPa',
                        'relative_humidity_200hPa',
                        'relative_humidity_150hPa',
                        'relative_humidity_100hPa',
                        'relative_humidity_50hPa',
                        'wind_speed_1000hPa',
                        'wind_speed_925hPa',
                        'wind_speed_850hPa',
                        'wind_speed_700hPa',
                        'wind_speed_600hPa',
                        'wind_speed_500hPa',
                        'wind_speed_400hPa',
                        'wind_speed_300hPa',
                        'wind_speed_250hPa',
                        'wind_speed_200hPa',
                        'wind_speed_150hPa',
                        'wind_speed_100hPa',
                        'wind_speed_50hPa',
                        'wind_direction_1000hPa',
                        'wind_direction_925hPa',
                        'wind_direction_850hPa',
                        'wind_direction_700hPa',
                        'wind_direction_600hPa',
                        'wind_direction_500hPa',
                        'wind_direction_400hPa',
                        'wind_direction_300hPa',
                        'wind_direction_250hPa',
                        'wind_direction_200hPa',
                        'wind_direction_150hPa',
                        'wind_direction_100hPa',
                        'wind_direction_50hPa',
                        'vertical_velocity_1000hPa',
                        'vertical_velocity_925hPa',
                        'vertical_velocity_850hPa',
                        'vertical_velocity_700hPa',
                        'vertical_velocity_600hPa',
                        'vertical_velocity_500hPa',
                        'vertical_velocity_400hPa',
                        'vertical_velocity_300hPa',
                        'vertical_velocity_250hPa',
                        'vertical_velocity_200hPa',
                        'vertical_velocity_150hPa',
                        'vertical_velocity_100hPa',
                        'vertical_velocity_50hPa',
                        'geopotential_height_1000hPa',
                        'geopotential_height_925hPa',
                        'geopotential_height_850hPa',
                        'geopotential_height_700hPa',
                        'geopotential_height_600hPa',
                        'geopotential_height_500hPa',
                        'geopotential_height_400hPa',
                        'geopotential_height_300hPa',
                        'geopotential_height_250hPa',
                        'geopotential_height_200hPa',
                        'geopotential_height_150hPa',
                        'geopotential_height_100hPa',
                        'geopotential_height_50hPa'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/NOAA/HGEFS",
            filename=f"HGEFS_Data.csv"):
```

    This function retrieves HGEFS time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
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
                                            'cloud_cover',
                                            'cloud_cover_low',
                                            'cloud_cover_mid',
                                            'cloud_cover_high',
                                            'precipitation',
                                            'pressure_msl',
                                            'temperature_1000hPa',
                                            'temperature_925hPa',
                                            'temperature_850hPa',
                                            'temperature_700hPa',
                                            'temperature_600hPa',
                                            'temperature_500hPa',
                                            'temperature_400hPa',
                                            'temperature_300hPa',
                                            'temperature_250hPa',
                                            'temperature_200hPa',
                                            'temperature_150hPa',
                                            'temperature_100hPa',
                                            'temperature_50hPa',
                                            'dew_point_1000hPa',
                                            'dew_point_925hPa',
                                            'dew_point_850hPa',
                                            'dew_point_700hPa',
                                            'dew_point_600hPa',
                                            'dew_point_500hPa',
                                            'dew_point_400hPa',
                                            'dew_point_300hPa',
                                            'dew_point_250hPa',
                                            'dew_point_200hPa',
                                            'dew_point_150hPa',
                                            'dew_point_100hPa',
                                            'dew_point_50hPa',
                                            'relative_humidity_1000hPa',
                                            'relative_humidity_925hPa',
                                            'relative_humidity_850hPa',
                                            'relative_humidity_700hPa',
                                            'relative_humidity_600hPa',
                                            'relative_humidity_500hPa',
                                            'relative_humidity_400hPa',
                                            'relative_humidity_300hPa',
                                            'relative_humidity_250hPa',
                                            'relative_humidity_200hPa',
                                            'relative_humidity_150hPa',
                                            'relative_humidity_100hPa',
                                            'relative_humidity_50hPa',
                                            'wind_speed_1000hPa',
                                            'wind_speed_925hPa',
                                            'wind_speed_850hPa',
                                            'wind_speed_700hPa',
                                            'wind_speed_600hPa',
                                            'wind_speed_500hPa',
                                            'wind_speed_400hPa',
                                            'wind_speed_300hPa',
                                            'wind_speed_250hPa',
                                            'wind_speed_200hPa',
                                            'wind_speed_150hPa',
                                            'wind_speed_100hPa',
                                            'wind_speed_50hPa',
                                            'wind_direction_1000hPa',
                                            'wind_direction_925hPa',
                                            'wind_direction_850hPa',
                                            'wind_direction_700hPa',
                                            'wind_direction_600hPa',
                                            'wind_direction_500hPa',
                                            'wind_direction_400hPa',
                                            'wind_direction_300hPa',
                                            'wind_direction_250hPa',
                                            'wind_direction_200hPa',
                                            'wind_direction_150hPa',
                                            'wind_direction_100hPa',
                                            'wind_direction_50hPa',
                                            'vertical_velocity_1000hPa',
                                            'vertical_velocity_925hPa',
                                            'vertical_velocity_850hPa',
                                            'vertical_velocity_700hPa',
                                            'vertical_velocity_600hPa',
                                            'vertical_velocity_500hPa',
                                            'vertical_velocity_400hPa',
                                            'vertical_velocity_300hPa',
                                            'vertical_velocity_250hPa',
                                            'vertical_velocity_200hPa',
                                            'vertical_velocity_150hPa',
                                            'vertical_velocity_100hPa',
                                            'vertical_velocity_50hPa',
                                            'geopotential_height_1000hPa',
                                            'geopotential_height_925hPa',
                                            'geopotential_height_850hPa',
                                            'geopotential_height_700hPa',
                                            'geopotential_height_600hPa',
                                            'geopotential_height_500hPa',
                                            'geopotential_height_400hPa',
                                            'geopotential_height_300hPa',
                                            'geopotential_height_250hPa',
                                            'geopotential_height_200hPa',
                                            'geopotential_height_150hPa',
                                            'geopotential_height_100hPa',
                                            'geopotential_height_50hPa']
                                            
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
    
    A Pandas.DataFrame of the HGEFS time series forecast for a given point of latitude/longitude. 
