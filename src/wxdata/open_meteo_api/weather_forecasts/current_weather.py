"""
This file hosts the interface for the Open-Meteo API for Current Weather data.

(C) Eric J. Drewitz 2025-2026
"""
import requests as _requests
import pandas as _pd
from wxdata.open_meteo_api.utils import(
    json_to_pandas as _json_to_pandas,
    server_response as _server_response
)

def point_data(latitude,
            longitude,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m',
                        'relative_humidity_2m',
                        'apparent_temperature',
                        'precipitation',
                        'snowfall',
                        'cloud_cover',
                        'pressure_msl',
                        'surface_pressure',
                        'wind_speed_10m',
                        'wind_direction_10m',
                        'wind_gusts_10m',
                        'weather_code',
                        'rain',
                        'showers'],
            proxies=None):
    
    """
    This function retrieves current weather (model mosaic) conditions from the Open-Meteo API for a given point of latitude/longitude.
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
        
    1) temperature_units (String) - Default='fahrenheit'. The units for temperature.
    
        Valid Temperature Units
        -----------------------
        
        1) fahrenheit
        2) celsius
        
    2) wind_speed_units (String) - Default='mph'. The units for wind speed. 
    
        Valid Wind Speed Units
        ----------------------
        
        1) mph - miles per hour
        2) kmh - kilometers per hour
        3) ms - meters per second
        4) kn - knots
        
    3) precipitation_units (String) - Default='inch'. The units for precipitation amounts.
    
        Valid Precipitation Units
        -------------------------
        
        1) inch - inches
        2) mm - millimeters
        
    4) variables (String List) - Default=['temperature_2m',
                                            'relative_humidity_2m',
                                            'apparent_temperature',
                                            'precipitation',
                                            'snowfall',
                                            'cloud_cover',
                                            'pressure_msl',
                                            'surface_pressure',
                                            'wind_speed_10m',
                                            'wind_direction_10m',
                                            'wind_gusts_10m',
                                            'weather_code',
                                            'rain',
                                            'showers']
                                            
                The list of variables to choose from.
                
    5) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
                    
    Returns
    -------
    
    A Pandas.DataFrame of the current weather (model mosaic) conditions for a given point of latitude/longitude. 
    """
    
    if proxies == None:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&" 
          f"current={','.join(variables)}" 
          f"&wind_speed_unit={wind_speed_units}&temperature_unit={temperature_units}&precipitation_unit={precipitation_units}")
        
        
        
    else:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&" 
          f"current={','.join(variables)}" 
          f"&wind_speed_unit={wind_speed_units}&temperature_unit={temperature_units}&precipitation_unit={precipitation_units}",
                             proxies=proxies)
        
    _server_response(response)
        
    data = response.json()
    
    df = _json_to_pandas(data,
                         field='current')
    
    df['time'] = _pd.to_datetime(df['time'])
    
    df = df.drop(columns='interval')
    
    return df