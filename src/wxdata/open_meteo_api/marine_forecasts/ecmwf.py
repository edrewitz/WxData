"""
This file hosts ECMWF Marine Forecasts

(C) Eric J. Drewitz 2025-2026
"""
import requests as _requests
import pandas as _pd
from wxdata.utils.api import(
    json_to_pandas as _json_to_pandas,
    server_response as _server_response,
    df_to_csv as _df_to_csv
)

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
    
    """
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
    
    A Pandas.DataFrame of the ECMWF WAM forecast for a given point of latitude/longitude. 
    """
    
    if days > 16:
        print(f"The maximum number of days that can be retrieved is 16. Setting 'days' to 16.")
        days = 16
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://marine-api.open-meteo.com/v1/marine?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ecmwf_wam"
                             f"&forecast_days={days}")
        
        
        
    else:
        response = _requests.get(f"https://marine-api.open-meteo.com/v1/marine?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ecmwf_wam"
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


def ecmwf_wam_0p25(latitude,
            longitude,
            days=7,
            variables=['wave_height',
                        'wave_direction',
                        'wave_period',
                        'wave_peak_period'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/Marine Forecasts/ECMWF",
            filename=f"ECMWF_WAM_P25.csv"):
    
    """
    This function retrieves the ECMWF WAM 0.25 Degree forecast from the Open-Meteo API for a given point of latitude/longitude.
        
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) days (Integer) - Default=7. Amount of days to go out for the forecast. Maximum is 16.
        
    2) variables (String List) - Default=['wave_height',
                                            'wave_direction',
                                            'wave_period',
                                            'wave_peak_period']
                                            
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
    
    A Pandas.DataFrame of the ECMWF WAM 0.25 Degree forecast for a given point of latitude/longitude. 
    """
    
    if days > 16:
        print(f"The maximum number of days that can be retrieved is 16. Setting 'days' to 16.")
        days = 16
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://marine-api.open-meteo.com/v1/marine?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ecmwf_wam025"
                             f"&forecast_days={days}")
        
        
        
    else:
        response = _requests.get(f"https://marine-api.open-meteo.com/v1/marine?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ecmwf_wam025"
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