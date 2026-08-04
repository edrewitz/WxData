"""
This file returns the current air-quality observations from airnow.gov

In order to use this web service, you must create a free account at: https://docs.airnowapi.org/ for an API Key. 

(C) Eric J. Drewitz 2025-2026
"""

import requests as _requests
import pandas as _pd
import sys as _sys
import wxdata.airnow_api._errors as _errors
from io import StringIO as _StringIO
from time import sleep as _sleep

try:
    from datetime import(
        datetime as _datetime,
        UTC as _UTC
    )
except Exception as e:
    from datetime import datetime as _datetime
    
from wxdata.utils.api import df_to_csv as _df_to_csv

try:
    _now = _datetime.now(_UTC)
except Exception as e:
    _now = _datetime.utcnow()
    

if _now.hour >= 10:
    _now_hour = _now.hour
    
else:
    _now_hour = f"0{_now.hour}"
    
    
def get_current_data_bounding_box(api_key=None,
                                  read_in_key_from_path=True,
                                  parameter='pm25',
                                  western_bound=-124.205070,
                                  eastern_bound=-75.337882,
                                  southern_bound=28.716781,
                                  northern_bound=45.419415,
                                  proxies=None,
                                  to_csv=False,
                                  path=f"Air Now Observations/{_now.strftime('%Y_%m_%d')}_{_now_hour}"):
    
    """
    This function retrieves air-quality observations from the airnow API.
    
    Required Arguments: None
        
    Optional Arguments:
    
    1) api_key (String) - Default=None. 
    
        The user needs to either pass in an API Key or a path to a .txt file where the API Key is stored. 
        
        It is strongly recommended to not put the API Key itself in your code. It is recommended to store the key
        in a file and read that key into the code.
        
        The easiest way is to create a text (.txt) file with a single element inside of it that is your API Key for Air Now.
        
        If the user wishes to follow this method - set `read_in_key_from_path=True` which is the default setting.
        The user will then set `api_key={path to api key text file}`
        
        If the user wishes to use their own methods of ingesting the API Key, then set `api_key=your_api_key_variable`.

        To get an API Key create a free account at: https://docs.airnowapi.org/
    
    2) read_in_key_from_path (Boolean) - Default=True. When set to True, the API Key is read in from a text file (.txt) at
        the path specified in `api_key`. Set `read_in_key_from_path=False` if the user wishes to use their own method for
        ingesting their Air Now API Key. 

    
    3) parameter (String) - Default='pm25'.
    
        Parameters
        ----------
        
        'pm25' - PM 2.5
        'pm10' - PM 10
        'ozone' - Ozone (O3)
        'no2' - Nitrogen Dioxide (NO2)
        'co' - Carbon Monoxide (CO)
        'so2' - Sulfur Dioxide (SO2)
        
    4) western_bound (Float or Integer) - Default=-124.205070. 
    
    5) eastern_bound (Float or Integer) - Default=-75.337882. 
    
    6) southern_bound (Float or Integer) - Default=28.716781. 
    
    7) northern_bound (Float or Integer) - Default=45.419415. 
    
    8) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    9) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}
    
    10) path (String) - The path where the CSV file is saved to.
    
    Returns
    -------
    
    A Pandas.DataFrame of all the current air quality observations within the bounding box.     
    """    
    try:
        if read_in_key_from_path == True:
            with open(api_key, "r", encoding="utf-8") as file:
                api_key = file.read()
        else:
            api_key = api_key
            
            if api_key == None:
               _errors.missing_api_key()
               _sys.exit(1) 
            else:
                pass
    except Exception as e:
        _errors.missing_api_key()
        _sys.exit(1)
    
    
    if proxies == None:
        response = _requests.get(f"https://www.airnowapi.org/aq/data/?"
                                 f"startDate={_now.strftime('%Y-%m-%d')}T{_now_hour}&endDate={_now.strftime('%Y-%m-%d')}T{_now_hour}"
                                 f"&parameters={parameter.upper()}"
                                 f"&BBOX={western_bound},{southern_bound},{eastern_bound},{northern_bound}"
                                 f"&dataType=B&format=application/json&API_KEY={api_key}")
    else:
        response = _requests.get(f"https://www.airnowapi.org/aq/data/?"
                                 f"startDate={_now.strftime('%Y-%m-%d')}T{_now_hour}&endDate={_now.strftime('%Y-%m-%d')}T{_now_hour}"
                                 f"&parameters={parameter.upper()}"
                                 f"&BBOX={western_bound},{southern_bound},{eastern_bound},{northern_bound}"
                                 f"&dataType=B&format=application/json&API_KEY={api_key}",
                                 proxies=proxies)
    if response.status_code != 200:
        if response.status_code == 429:
            _errors.rate_limit_error_message()
            _sleep(3600)
            df = get_current_data_bounding_box(api_key=api_key,
                                  read_in_key_from_path=read_in_key_from_path,
                                  parameter=parameter,
                                  western_bound=western_bound,
                                  eastern_bound=eastern_bound,
                                  southern_bound=southern_bound,
                                  northern_bound=northern_bound,
                                  proxies=proxies,
                                  to_csv=to_csv,
                                  path=path)
            
            return df
        else:
            print(f"Another exception occurred\nHTTP Status Code: {response.status_code} Reason: {response.reason}")
            _sys.exit(1)
    else:
        pass
                
    df = _pd.read_json(_StringIO(response.text))
    try:
        df = df.drop('Parameter', axis=1)
    except Exception as e:
        pass
    df = df.rename(columns={'Value':f'{parameter.upper()}'})
    
    df['time'] = _pd.to_datetime(df['UTC'])
    df = df.drop('UTC', axis=1)
        
    if to_csv == True:
        _df_to_csv(df,
                    path,
                    parameter)
    
    return df


def get_data_bounding_box(start,
                            end,
                            api_key=None,
                            read_in_key_from_path=True,
                            parameter='pm25',
                            western_bound=-124.205070,
                            eastern_bound=-75.337882,
                            southern_bound=28.716781,
                            northern_bound=45.419415,
                            proxies=None,
                            to_csv=False,
                            path=f"Air Now Observations/Historical/historical_air_quality_data.csv"):
    
    """
    This function retrieves historical air-quality observations from the airnow API.
    
    Required Arguments:
        
    1) start (String) - The start time in the following format: 'YYYY-mm-ddTHH'
    
    2) end (String) - The end time in the following format: 'YYYY-mm-ddTHH'
        
    Optional Arguments:
    
    1) api_key (String) - Default=None. 
    
        The user needs to either pass in an API Key or a path to a .txt file where the API Key is stored. 
        
        It is strongly recommended to not put the API Key itself in your code. It is recommended to store the key
        in a file and read that key into the code.
        
        The easiest way is to create a text (.txt) file with a single element inside of it that is your API Key for Air Now.
        
        If the user wishes to follow this method - set `read_in_key_from_path=True` which is the default setting.
        The user will then set `api_key={path to api key text file}`
        
        If the user wishes to use their own methods of ingesting the API Key, then set `api_key=your_api_key_variable`.

        To get an API Key create a free account at: https://docs.airnowapi.org/
    
    2) read_in_key_from_path (Boolean) - Default=True. When set to True, the API Key is read in from a text file (.txt) at
        the path specified in `api_key`. Set `read_in_key_from_path=False` if the user wishes to use their own method for
        ingesting their Air Now API Key. 
    
    3) parameter (String) - Default='pm25'.
    
        Parameters
        ----------
        
        'pm25' - PM 2.5
        'pm10' - PM 10
        'ozone' - Ozone (O3)
        'no2' - Nitrogen Dioxide (NO2)
        'co' - Carbon Monoxide (CO)
        'so2' - Sulfur Dioxide (SO2)
        
    4) western_bound (Float or Integer) - Default=-124.205070. 
    
    5) eastern_bound (Float or Integer) - Default=-75.337882. 
    
    6) southern_bound (Float or Integer) - Default=28.716781. 
    
    7) northern_bound (Float or Integer) - Default=45.419415. 
    
    8) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    9) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} wth {filename}
    
    10) path (String) - The path where the CSV file is saved to.
    
    Returns
    -------
    
    A Pandas.DataFrame of all the historical air quality observations within the bounding box and time bounds.     
    """
    
    try:
        if read_in_key_from_path == True:
            with open(api_key, "r", encoding="utf-8") as file:
                api_key = file.read()
        else:
            api_key = api_key
            
            if api_key == None:
               _errors.missing_api_key()
               _sys.exit(1) 
            else:
                pass
    except Exception as e:
        _errors.missing_api_key()
        _sys.exit(1)
    
    
    if proxies == None:
        response = _requests.get(f"https://www.airnowapi.org/aq/data/?"
                                 f"startDate={start}&endDate={end}"
                                 f"&parameters={parameter.upper()}"
                                 f"&BBOX={western_bound},{southern_bound},{eastern_bound},{northern_bound}"
                                 f"&dataType=B&format=application/json&API_KEY={api_key}")
    else:
        response = _requests.get(f"https://www.airnowapi.org/aq/data/?"
                                 f"startDate={start}&endDate={end}"
                                 f"&parameters={parameter.upper()}"
                                 f"&BBOX={western_bound},{southern_bound},{eastern_bound},{northern_bound}"
                                 f"&dataType=B&format=application/json&API_KEY={api_key}",
                                 proxies=proxies)
    if response.status_code != 200:
        if response.status_code == 429:
            _errors.rate_limit_error_message()
            _sleep(3600)
            df = get_data_bounding_box(start,
                                        end,
                                        api_key=api_key,
                                        read_in_key_from_path=read_in_key_from_path,
                                        parameter=parameter,
                                        western_bound=western_bound,
                                        eastern_bound=eastern_bound,
                                        southern_bound=southern_bound,
                                        northern_bound=northern_bound,
                                        proxies=proxies,
                                        to_csv=to_csv,
                                        path=path)
            
            return df
        else:
            print(f"Another exception occurred\nHTTP Status Code: {response.status_code} Reason: {response.reason}")
            _sys.exit(1)
    else:
        pass
                
    df = _pd.read_json(_StringIO(response.text))
    
    df = df.drop('Parameter', axis=1)
    df = df.rename(columns={'Value':f'{parameter.upper()}'})
    
    df['time'] = _pd.to_datetime(df['UTC'])
    df = df.drop('UTC', axis=1)
        
    if to_csv == True:
        _df_to_csv(df,
                    path,
                    parameter)
    
    return df
