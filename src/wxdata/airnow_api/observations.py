"""
This file returns the current air-quality observations from airnow.gov

In order to use this web service, you must create a free account at: https://docs.airnowapi.org/ for an API Key. 

(C) Eric J. Drewitz 2025-2026
"""

import requests as _requests
import pandas as _pd
import sys as _sys
from io import StringIO as _StringIO
from time import sleep as _sleep

try:
    from datetime import(
        datetime,
        timedelta,
        UTC
    )
except Exception as e:
    from datetime import(
        datetime,
        timedelta
    )
from wxdata.utils.api import df_to_csv as _df_to_csv

try:
    now = datetime.now(UTC)
except Exception as e:
    now = datetime.utcnow()
    
t1_hour = now - timedelta(hours=1)

if now.hour >= 10:
    now_hour = now.hour
    
else:
    now_hour = f"0{now.hour}"
    
if t1_hour.hour >= 10:
    t1_hr = t1_hour.hour
    
else:
    t1_hr = f"0{t1_hour.hour}"
    
def _error_message():
    
    """
    Returns an error message when rate limited    
    """
    
    print(f"Error: Too Many Requests")
    print(f"The Air-Now API allows for up to 500 calls per hour.")
    print(f"Please try again later.")
    
def get_current_data_bounding_box(api_key,
                                  parameter='pm25',
                                  western_bound=-124.205070,
                                  eastern_bound=-75.337882,
                                  southern_bound=28.716781,
                                  northern_bound=45.419415,
                                  proxies=None,
                                  to_csv=False,
                                  path=f"Air Now Data/{now.strftime('%Y_%m_%d')}_{now_hour}"):
    
    """
    This function retrieves air-quality data from the airnow API.
    
    Required Arguments:
    
    1) api_key (String) - The API Key to access the data. 
    
        To get an API Key create a free account at: https://docs.airnowapi.org/
        
    Optional Arguments:
    
    1) parameter (String) - Default='pm25'.
    
        Parameters
        ----------
        
        'pm25' - PM 2.5
        'pm10' - PM 10
        'ozone' - Ozone (O3)
        'no2' - Nitrogen Dioxide (NO2)
        'co' - Carbon Monoxide (CO)
        'so2' - Sulfur Dioxide (SO2)
        
    2) western_bound (Float or Integer) - Default=-124.205070. 
    
    3) eastern_bound (Float or Integer) - Default=-75.337882. 
    
    4) southern_bound (Float or Integer) - Default=28.716781. 
    
    5) northern_bound (Float or Integer) - Default=45.419415. 
    
    6) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    7) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} wth {filename}
    
    8) path (String) - The path where the CSV file is saved to.
    
    Returns
    -------
    
    A Pandas.DataFrame of all the current air quality observations within the bounding box.     
    """
    
    
    if proxies == None:
        response = _requests.get(f"https://www.airnowapi.org/aq/data/?"
                                 f"startDate={t1_hour.strftime('%Y-%m-%d')}T{t1_hr}&endDate={now.strftime('%Y-%m-%d')}T{now_hour}"
                                 f"&parameters={parameter.upper()}"
                                 f"&BBOX={western_bound},{southern_bound},{eastern_bound},{northern_bound}"
                                 f"&dataType=B&format=application/json&API_KEY={api_key}")
    else:
        response = _requests.get(f"https://www.airnowapi.org/aq/data/?"
                                 f"startDate={t1_hour.strftime('%Y-%m-%d')}T{t1_hr}&endDate={now.strftime('%Y-%m-%d')}T{now_hour}"
                                 f"&parameters={parameter.upper()}"
                                 f"&BBOX={western_bound},{southern_bound},{eastern_bound},{northern_bound}"
                                 f"&dataType=B&format=application/json&API_KEY={api_key}",
                                 proxies=proxies)
    if response.status_code != 200:
        if response.status_code == 429:
            _error_message()
            _sleep(3600)
            df = get_current_data_bounding_box(api_key,
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