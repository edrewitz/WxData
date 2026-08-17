"""
This file hosts Deutscher Wetterdienst (DWD) Marine Forecasts

(C) Eric J. Drewitz 2025-2026
"""
import requests as _requests
import pandas as _pd
from wxdata.utils.api import(
    json_to_pandas as _json_to_pandas,
    server_response as _server_response,
    df_to_csv as _df_to_csv
)

def ewam(latitude,
            longitude,
            days=3,
            variables=['wave_height',
                        'wave_direction',
                        'wave_period',
                        'wind_wave_height',
                        'wind_wave_direction',
                        'wind_wave_period',
                        'wind_wave_peak_period',
                        'swell_wave_height',
                        'swell_wave_direction',
                        'swell_wave_period',
                        'swell_wave_peak_period'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/Marine Forecasts/DWD",
            filename=f"EWAM.csv"):
    
    """
    This function retrieves the DWD EWAM forecast from the Open-Meteo API for a given point of latitude/longitude.
    
    **This DWD EWAM Domain is Europe Only**
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) days (Integer) - Default=3. Amount of days to go out for the forecast. Maximum is 3.
        
    2) variables (String List) - Default=['wave_height',
                                            'wave_direction',
                                            'wave_period',
                                            'wind_wave_height',
                                            'wind_wave_direction',
                                            'wind_wave_period',
                                            'wind_wave_peak_period',
                                            'swell_wave_height',
                                            'swell_wave_direction',
                                            'swell_wave_period',
                                            'swell_wave_peak_period']


                                            
                The list of variables to choose from.
                
    3) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    4) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}
    
    5) path (String) - The path where the CSV file is saved to.
    
    6) filename (String) - The filename for the CSV file.                     
                    
    Returns
    -------
    
    A Pandas.DataFrame of the DWD EWAM forecast for a given point of latitude/longitude. 
    """
    
    if days > 3:
        print(f"The maximum number of days that can be retrieved is 3. Setting 'days' to 3.")
        days = 3
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://marine-api.open-meteo.com/v1/marine?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ewam"
                             f"&forecast_days={days}")
        
        
        
    else:
        response = _requests.get(f"https://marine-api.open-meteo.com/v1/marine?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ewam"
                             f"&forecast_days={days}",
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

def gwam(latitude,
            longitude,
            days=7,
            variables=['wave_height',
                        'wave_direction',
                        'wave_period',
                        'wind_wave_height',
                        'wind_wave_direction',
                        'wind_wave_period',
                        'wind_wave_peak_period',
                        'swell_wave_height',
                        'swell_wave_direction',
                        'swell_wave_period',
                        'swell_wave_peak_period'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/Marine Forecasts/DWD",
            filename=f"GWAM.csv"):
    
    """
    This function retrieves the DWD GWAM forecast from the Open-Meteo API for a given point of latitude/longitude.
        
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) days (Integer) - Default=7. Amount of days to go out for the forecast. Maximum is 8.
        
    2) variables (String List) - Default=['wave_height',
                                            'wave_direction',
                                            'wave_period',
                                            'wind_wave_height',
                                            'wind_wave_direction',
                                            'wind_wave_period',
                                            'wind_wave_peak_period',
                                            'swell_wave_height',
                                            'swell_wave_direction',
                                            'swell_wave_period',
                                            'swell_wave_peak_period']


                                            
                The list of variables to choose from.
                
    3) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    4) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}
    
    5) path (String) - The path where the CSV file is saved to.
    
    6) filename (String) - The filename for the CSV file.                     
                    
    Returns
    -------
    
    A Pandas.DataFrame of the DWD GWAM forecast for a given point of latitude/longitude. 
    """
    
    if days > 8:
        print(f"The maximum number of days that can be retrieved is 8. Setting 'days' to 8.")
        days = 8
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://marine-api.open-meteo.com/v1/marine?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=gwam"
                             f"&forecast_days={days}")
        
        
        
    else:
        response = _requests.get(f"https://marine-api.open-meteo.com/v1/marine?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=gwam"
                             f"&forecast_days={days}",
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