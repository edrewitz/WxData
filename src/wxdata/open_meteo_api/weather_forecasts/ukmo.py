"""
This file hosts the interface for the Open-Meteo API for UK Met Office (UKMO) data.

(C) Eric J. Drewitz 2025-2026
"""

import requests as _requests
import pandas as _pd
from wxdata.open_meteo_api.utils import(
    json_to_pandas as _json_to_pandas,
    server_response as _server_response,
    df_to_csv as _df_to_csv
)

def ukmo_global_hourly_ensemble_point_forecast(latitude,
            longitude,
            days=7,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m',
                        'relative_humidity_2m',
                        'dew_point_2m',
                        'apparent_temperature',
                        'snowfall',
                        'rain',
                        'precipitation',
                        'weather_code',
                        'pressure_msl',
                        'surface_pressure',
                        'cloud_cover',
                        'visibility',
                        'et0_fao_evapotranspiration',
                        'vapour_pressure_deficit',
                        'wind_speed_10m',
                        'wind_direction_10m',
                        'wind_gusts_10m',
                        'surface_temperature'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/UKMO/UKMO Global Ensemble",
            filename=f"UKMO_Global_Ensemble_Data.csv"):
    
    """
    This function retrieves UKMO Global Ensemble time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
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
                                            'snowfall',
                                            'rain',
                                            'precipitation',
                                            'weather_code',
                                            'pressure_msl',
                                            'surface_pressure',
                                            'cloud_cover',
                                            'visibility',
                                            'et0_fao_evapotranspiration',
                                            'vapour_pressure_deficit',
                                            'wind_speed_10m',
                                            'wind_direction_10m',
                                            'wind_gusts_10m',
                                            'surface_temperature']
                                            
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
    
    A Pandas.DataFrame of the UKMO Global Ensemble time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 36:
        print(f"The maximum number of days that can be retrieved is 36. Setting 'days' to 36.")
        days = 36
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://ensemble-api.open-meteo.com/v1/ensemble?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ukmo_global_ensemble_20km"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
                
    else:
        response = _requests.get(f"https://ensemble-api.open-meteo.com/v1/ensemble?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ukmo_global_ensemble_20km"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}",
                             proxies=proxies)
        
    _server_response(response)
    
    data = response.json()
    
    df = _json_to_pandas(data)
    df['time'] = _pd.to_datetime(df['time'])
    
    if to_csv == True:
        _df_to_csv(df,
                   path,
                   filename)
    
    return df