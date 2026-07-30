"""
This file hosts air quality monitoring and forecast data.

All data comes from the CAMS Model.

(C) Eric J. Drewitz 2025-2026
"""
import requests as _requests
import pandas as _pd
from wxdata.utils.api import(
    json_to_pandas as _json_to_pandas,
    server_response as _server_response,
    df_to_csv as _df_to_csv
)

def cams_forecast(latitude,
            longitude,
            days=5,
            variables=['pm10',
                        'pm2_5',
                        'carbon_monoxide',
                        'carbon_dioxide',
                        'nitrogen_dioxide',
                        'sulphur_dioxide',
                        'ozone',
                        'aerosol_optical_depth',
                        'dust',
                        'uv_index',
                        'uv_index_clear_sky',
                        'ammonia',
                        'methane',
                        'alder_pollen',
                        'birch_pollen',
                        'mugwort_pollen',
                        'grass_pollen',
                        'olive_pollen',
                        'ragweed_pollen',
                        'european_aqi',
                        'european_aqi_pm2_5',
                        'european_aqi_pm10',
                        'european_aqi_nitrogen_dioxide',
                        'european_aqi_ozone',
                        'european_aqi_sulphur_dioxide',
                        'us_aqi',
                        'us_aqi_pm2_5',
                        'us_aqi_pm10',
                        'us_aqi_nitrogen_dioxide',
                        'us_aqi_carbon_monoxide',
                        'us_aqi_ozone',
                        'us_aqi_sulphur_dioxide',
                        'formaldehyde',
                        'glyoxal',
                        'peroxyacyl_nitrates',
                        'sea_salt_aerosol',
                        'nitrogen_monoxide'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/Air Quality/Forecasts",
            filename=f"CAMS_Forecast.csv"):
    
    """
    This function retrieves the CAMS Air Quality forecast from the Open-Meteo API for a given point of latitude/longitude.
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) days (Integer) - Default=5. Amount of days to go out for the forecast. Maximum is 7.
        
    2) variables (String List) - Default=['pm10',
                                            'pm2_5',
                                            'carbon_monoxide',
                                            'carbon_dioxide',
                                            'nitrogen_dioxide',
                                            'sulphur_dioxide',
                                            'ozone',
                                            'aerosol_optical_depth',
                                            'dust',
                                            'uv_index',
                                            'uv_index_clear_sky',
                                            'ammonia',
                                            'methane',
                                            'alder_pollen',
                                            'birch_pollen',
                                            'mugwort_pollen',
                                            'grass_pollen',
                                            'olive_pollen',
                                            'ragweed_pollen',
                                            'european_aqi',
                                            'european_aqi_pm2_5',
                                            'european_aqi_pm10',
                                            'european_aqi_nitrogen_dioxide',
                                            'european_aqi_ozone',
                                            'european_aqi_sulphur_dioxide',
                                            'us_aqi',
                                            'us_aqi_pm2_5',
                                            'us_aqi_pm10',
                                            'us_aqi_nitrogen_dioxide',
                                            'us_aqi_carbon_monoxide',
                                            'us_aqi_ozone',
                                            'us_aqi_sulphur_dioxide',
                                            'formaldehyde',
                                            'glyoxal',
                                            'peroxyacyl_nitrates',
                                            'sea_salt_aerosol',
                                            'nitrogen_monoxide']

                                            
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
    
    A Pandas.DataFrame of the CAMS Air Quality forecast for a given point of latitude/longitude. 
    """
    
    if days > 7:
        print(f"The maximum number of days that can be retrieved is 7 for the CAMS Air Quality Forecast. Setting 'days' to 7.")
        days = 7
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://air-quality-api.open-meteo.com/v1/air-quality?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}"
                             f"&forecast_days={days}")
        
        
        
    else:
        response = _requests.get(f"https://air-quality-api.open-meteo.com/v1/air-quality?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}"
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