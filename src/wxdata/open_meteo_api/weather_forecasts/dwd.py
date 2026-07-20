"""
This file hosts the interface for the Open-Meteo API for DWD data.

(C) Eric J. Drewitz 2025-2026
"""
import requests as _requests
import pandas as _pd
from wxdata.open_meteo_api.utils import(
    json_to_pandas as _json_to_pandas,
    server_response as _server_response,
    df_to_csv as _df_to_csv
)

def icon_hourly_point_forecast(latitude,
            longitude,
            days=7,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m',
                        'relative_humidity_2m',
                        'apparent_temperature',
                        'precipitation',
                        'snowfall',
                        'snow_depth',
                        'pressure_msl',
                        'surface_pressure',
                        'cloud_cover',
                        'cloud_cover_low',
                        'cloud_cover_mid',
                        'cloud_cover_high',
                        'visibility',
                        'evapotranspiration',
                        'et0_fao_evapotranspiration',
                        'vapour_pressure_deficit',
                        'wind_speed_10m',
                        'wind_speed_80m',
                        'wind_speed_120m',
                        'wind_speed_180m',
                        'wind_direction_10m',
                        'wind_direction_80m',
                        'wind_direction_120m',
                        'wind_direction_180m',
                        'temperature_80m',
                        'wind_gusts_10m',
                        'temperature_120m',
                        'temperature_180m',
                        'soil_temperature_0cm',
                        'soil_temperature_6cm',
                        'soil_temperature_18cm',
                        'soil_temperature_54cm',
                        'soil_moisture_0_to_1cm',
                        'soil_moisture_1_to_3cm',
                        'soil_moisture_3_to_9cm',
                        'soil_moisture_9_to_27cm',
                        'soil_moisture_27_to_81cm',
                        'temperature_1000hPa',
                        'temperature_975hPa',
                        'temperature_950hPa',
                        'temperature_925hPa',
                        'temperature_900hPa',
                        'temperature_850hPa',
                        'temperature_800hPa',
                        'temperature_700hPa',
                        'temperature_600hPa',
                        'temperature_500hPa',
                        'temperature_400hPa',
                        'temperature_300hPa',
                        'temperature_250hPa',
                        'temperature_200hPa',
                        'temperature_150hPa',
                        'temperature_100hPa',
                        'temperature_70hPa',
                        'temperature_50hPa',
                        'temperature_30hPa',
                        'relative_humidity_1000hPa',
                        'relative_humidity_975hPa',
                        'relative_humidity_950hPa',
                        'relative_humidity_925hPa',
                        'relative_humidity_900hPa',
                        'relative_humidity_850hPa',
                        'relative_humidity_800hPa',
                        'relative_humidity_700hPa',
                        'relative_humidity_600hPa',
                        'relative_humidity_500hPa',
                        'relative_humidity_400hPa',
                        'relative_humidity_300hPa',
                        'relative_humidity_250hPa',
                        'relative_humidity_200hPa',
                        'relative_humidity_150hPa',
                        'relative_humidity_100hPa',
                        'relative_humidity_70hPa',
                        'relative_humidity_50hPa',
                        'relative_humidity_30hPa',
                        'cloud_cover_1000hPa',
                        'cloud_cover_975hPa',
                        'cloud_cover_950hPa',
                        'cloud_cover_925hPa',
                        'cloud_cover_900hPa',
                        'cloud_cover_850hPa',
                        'cloud_cover_800hPa',
                        'cloud_cover_700hPa',
                        'cloud_cover_600hPa',
                        'cloud_cover_500hPa',
                        'cloud_cover_400hPa',
                        'cloud_cover_300hPa',
                        'cloud_cover_250hPa',
                        'cloud_cover_200hPa',
                        'cloud_cover_150hPa',
                        'cloud_cover_100hPa',
                        'cloud_cover_70hPa',
                        'cloud_cover_50hPa',
                        'cloud_cover_30hPa',
                        'wind_speed_1000hPa',
                        'wind_speed_975hPa',
                        'wind_speed_950hPa',
                        'wind_speed_925hPa',
                        'wind_speed_900hPa',
                        'wind_speed_850hPa',
                        'wind_speed_800hPa',
                        'wind_speed_700hPa',
                        'wind_speed_600hPa',
                        'wind_speed_500hPa',
                        'wind_speed_400hPa',
                        'wind_speed_300hPa',
                        'wind_speed_250hPa',
                        'wind_speed_200hPa',
                        'wind_speed_150hPa',
                        'wind_speed_100hPa',
                        'wind_speed_70hPa',
                        'wind_speed_50hPa',
                        'wind_speed_30hPa',
                        'wind_direction_1000hPa',
                        'wind_direction_975hPa',
                        'wind_direction_950hPa',
                        'wind_direction_925hPa',
                        'wind_direction_900hPa',
                        'wind_direction_850hPa',
                        'wind_direction_800hPa',
                        'wind_direction_700hPa',
                        'wind_direction_600hPa',
                        'wind_direction_500hPa',
                        'wind_direction_400hPa',
                        'wind_direction_300hPa',
                        'wind_direction_250hPa',
                        'wind_direction_200hPa',
                        'wind_direction_150hPa',
                        'wind_direction_100hPa',
                        'wind_direction_70hPa',
                        'wind_direction_50hPa',
                        'wind_direction_30hPa',
                        'geopotential_height_1000hPa',
                        'geopotential_height_975hPa',
                        'geopotential_height_950hPa',
                        'geopotential_height_925hPa',
                        'geopotential_height_900hPa',
                        'geopotential_height_850hPa',
                        'geopotential_height_800hPa',
                        'geopotential_height_700hPa',
                        'geopotential_height_600hPa',
                        'geopotential_height_500hPa',
                        'geopotential_height_400hPa',
                        'geopotential_height_300hPa',
                        'geopotential_height_250hPa',
                        'geopotential_height_200hPa',
                        'geopotential_height_150hPa',
                        'geopotential_height_100hPa',
                        'geopotential_height_70hPa',
                        'geopotential_height_50hPa',
                        'geopotential_height_30hPa'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/DWD/ICON",
            filename=f"ICON_Data.csv"):
    
    """
    This function retrieves DWD ICON time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
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
                                            'relative_humidity_2m',
                                            'apparent_temperature',
                                            'precipitation',
                                            'snowfall',
                                            'snow_depth',
                                            'pressure_msl',
                                            'surface_pressure',
                                            'cloud_cover',
                                            'cloud_cover_low',
                                            'cloud_cover_mid',
                                            'cloud_cover_high',
                                            'visibility',
                                            'evapotranspiration',
                                            'et0_fao_evapotranspiration',
                                            'vapour_pressure_deficit',
                                            'wind_speed_10m',
                                            'wind_speed_80m',
                                            'wind_speed_120m',
                                            'wind_speed_180m',
                                            'wind_direction_10m',
                                            'wind_direction_80m',
                                            'wind_direction_120m',
                                            'wind_direction_180m',
                                            'temperature_80m',
                                            'wind_gusts_10m',
                                            'temperature_120m',
                                            'temperature_180m',
                                            'soil_temperature_0cm',
                                            'soil_temperature_6cm',
                                            'soil_temperature_18cm',
                                            'soil_temperature_54cm',
                                            'soil_moisture_0_to_1cm',
                                            'soil_moisture_1_to_3cm',
                                            'soil_moisture_3_to_9cm',
                                            'soil_moisture_9_to_27cm',
                                            'soil_moisture_27_to_81cm',
                                            'temperature_1000hPa',
                                            'temperature_975hPa',
                                            'temperature_950hPa',
                                            'temperature_925hPa',
                                            'temperature_900hPa',
                                            'temperature_850hPa',
                                            'temperature_800hPa',
                                            'temperature_700hPa',
                                            'temperature_600hPa',
                                            'temperature_500hPa',
                                            'temperature_400hPa',
                                            'temperature_300hPa',
                                            'temperature_250hPa',
                                            'temperature_200hPa',
                                            'temperature_150hPa',
                                            'temperature_100hPa',
                                            'temperature_70hPa',
                                            'temperature_50hPa',
                                            'temperature_30hPa',
                                            'relative_humidity_1000hPa',
                                            'relative_humidity_975hPa',
                                            'relative_humidity_950hPa',
                                            'relative_humidity_925hPa',
                                            'relative_humidity_900hPa',
                                            'relative_humidity_850hPa',
                                            'relative_humidity_800hPa',
                                            'relative_humidity_700hPa',
                                            'relative_humidity_600hPa',
                                            'relative_humidity_500hPa',
                                            'relative_humidity_400hPa',
                                            'relative_humidity_300hPa',
                                            'relative_humidity_250hPa',
                                            'relative_humidity_200hPa',
                                            'relative_humidity_150hPa',
                                            'relative_humidity_100hPa',
                                            'relative_humidity_70hPa',
                                            'relative_humidity_50hPa',
                                            'relative_humidity_30hPa',
                                            'cloud_cover_1000hPa',
                                            'cloud_cover_975hPa',
                                            'cloud_cover_950hPa',
                                            'cloud_cover_925hPa',
                                            'cloud_cover_900hPa',
                                            'cloud_cover_850hPa',
                                            'cloud_cover_800hPa',
                                            'cloud_cover_700hPa',
                                            'cloud_cover_600hPa',
                                            'cloud_cover_500hPa',
                                            'cloud_cover_400hPa',
                                            'cloud_cover_300hPa',
                                            'cloud_cover_250hPa',
                                            'cloud_cover_200hPa',
                                            'cloud_cover_150hPa',
                                            'cloud_cover_100hPa',
                                            'cloud_cover_70hPa',
                                            'cloud_cover_50hPa',
                                            'cloud_cover_30hPa',
                                            'wind_speed_1000hPa',
                                            'wind_speed_975hPa',
                                            'wind_speed_950hPa',
                                            'wind_speed_925hPa',
                                            'wind_speed_900hPa',
                                            'wind_speed_850hPa',
                                            'wind_speed_800hPa',
                                            'wind_speed_700hPa',
                                            'wind_speed_600hPa',
                                            'wind_speed_500hPa',
                                            'wind_speed_400hPa',
                                            'wind_speed_300hPa',
                                            'wind_speed_250hPa',
                                            'wind_speed_200hPa',
                                            'wind_speed_150hPa',
                                            'wind_speed_100hPa',
                                            'wind_speed_70hPa',
                                            'wind_speed_50hPa',
                                            'wind_speed_30hPa',
                                            'wind_direction_1000hPa',
                                            'wind_direction_975hPa',
                                            'wind_direction_950hPa',
                                            'wind_direction_925hPa',
                                            'wind_direction_900hPa',
                                            'wind_direction_850hPa',
                                            'wind_direction_800hPa',
                                            'wind_direction_700hPa',
                                            'wind_direction_600hPa',
                                            'wind_direction_500hPa',
                                            'wind_direction_400hPa',
                                            'wind_direction_300hPa',
                                            'wind_direction_250hPa',
                                            'wind_direction_200hPa',
                                            'wind_direction_150hPa',
                                            'wind_direction_100hPa',
                                            'wind_direction_70hPa',
                                            'wind_direction_50hPa',
                                            'wind_directions_30hPa',
                                            'geopotential_height_1000hPa',
                                            'geopotential_height_975hPa',
                                            'geopotential_height_950hPa',
                                            'geopotential_height_925hPa',
                                            'geopotential_height_900hPa',
                                            'geopotential_height_850hPa',
                                            'geopotential_height_800hPa',
                                            'geopotential_height_700hPa',
                                            'geopotential_height_600hPa',
                                            'geopotential_height_500hPa',
                                            'geopotential_height_400hPa',
                                            'geopotential_height_300hPa',
                                            'geopotential_height_250hPa',
                                            'geopotential_height_200hPa',
                                            'geopotential_height_150hPa',
                                            'geopotential_height_100hPa',
                                            'geopotential_height_70hPa',
                                            'geopotential_height_50hPa',
                                            'geopotential_height_30hPa']
                                            
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
    
    A Pandas.DataFrame of the DWD ICON time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 7:
        print(f"The maximum number of days that can be retrieved is 7. Setting 'days' to 7.")
        days = 7
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=icon_seamless"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
        
    else:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=icon_seamless"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}",
                             proxies=proxies)
        
    _server_response(response)
        
    data = response.json()
    
    df = _json_to_pandas(data)
    
    if to_csv == True:
        _df_to_csv(df,
                   path,
                   filename)
    
    return df

def icon_eps_point_forecast(latitude,
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
                        'weather_code',
                        'pressure_msl',
                        'surface_pressure',
                        'cloud_cover',
                        'et0_fao_evapotranspiration',
                        'vapour_pressure_deficit',
                        'wind_speed_10m',
                        'wind_speed_80m',
                        'wind_direction_10m',
                        'wind_direction_80m',
                        'wind_gusts_10m',
                        'temperature_80m'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/NOAA/DWD",
            filename=f"ICON_EPS_Data.csv"):
    
    """
    This function retrieves DWD ICON EPS time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
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
                                            'relative_humidity_2m',
                                            'dew_point_2m',
                                            'apparent_temperature',
                                            'precipitation',
                                            'rain',
                                            'snowfall',
                                            'weather_code',
                                            'pressure_msl',
                                            'surface_pressure',
                                            'cloud_cover',
                                            'et0_fao_evapotranspiration',
                                            'vapour_pressure_deficit',
                                            'wind_speed_10m',
                                            'wind_speed_80m',
                                            'wind_direction_10m',
                                            'wind_direction_80m',
                                            'wind_gusts_10m',
                                            'temperature_80m']
                                            
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
    
    A Pandas.DataFrame of the DWD ICON EPS time series forecast for a given point of latitude/longitude. 
 
          variable naming convention
          ---------------------------
          
          Control Run (Example 2-Meter Temperature): data['temperature_2m']
          Ensemble Member 1 (Example 2-Meter Temperature): data['temperature_2m_member01'] -> data['temperature_2m_member39'] (40 total members [39 members + 1 control])
    """
    
    if days > 7:
        print(f"The maximum number of days that can be retrieved is 7. Setting 'days' to 7.")
        days = 7
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=icon_seamless_eps"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
        
    else:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=icon_seamless_eps"
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