"""
This file hosts the interface for the Open-Meteo API for CMC data.

(C) Eric J. Drewitz 2025-2026
"""
import requests as _requests
import pandas as _pd
from wxdata.utils.api import(
    json_to_pandas as _json_to_pandas,
    server_response as _server_response,
    df_to_csv as _df_to_csv
)

def gem_hourly_point_forecast(latitude,
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
                        'pressure_msl',
                        'surface_pressure',
                        'cloud_cover',
                        'cloud_cover_low',
                        'cloud_cover_mid',
                        'cloud_cover_high',
                        'et0_fao_evapotranspiration',
                        'vapour_pressure_deficit',
                        'weather_code',
                        'showers',
                        'wind_speed_10m',
                        'wind_speed_40m',
                        'wind_speed_80m',
                        'wind_speed_120m',
                        'wind_direction_10m',
                        'wind_direction_40m',
                        'wind_direction_80m',
                        'wind_direction_120m',
                        'temperature_40m',
                        'temperature_80m',
                        'temperature_120m',
                        'wind_gusts_10m',
                        'soil_temperature_0_to_10cm',
                        'soil_moisture_0_to_10cm',
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
                        'temperature_30hPa',
                        'temperature_20hPa',
                        'temperature_10hPa',
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
                        'dew_point_30hPa',
                        'dew_point_20hPa',
                        'dew_point_10hPa',
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
                        'relative_humidity_30hPa',
                        'relative_humidity_20hPa',
                        'relative_humidity_10hPa',
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
                        'wind_speed_30hPa',
                        'wind_speed_20hPa',
                        'wind_speed_10hPa',
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
                        'wind_direction_30hPa',
                        'wind_direction_20hPa',
                        'wind_direction_10hPa',
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
                        'geopotential_height_50hPa',
                        'geopotential_height_30hPa',
                        'geopotential_height_20hPa',
                        'geopotential_height_10hPa',
                        'cloud_cover_1000hPa',
                        'cloud_cover_925hPa',
                        'cloud_cover_850hPa',
                        'cloud_cover_700hPa',
                        'cloud_cover_600hPa',
                        'cloud_cover_500hPa',
                        'cloud_cover_400hPa',
                        'cloud_cover_300hPa',
                        'cloud_cover_250hPa',
                        'cloud_cover_200hPa',
                        'cloud_cover_150hPa',
                        'cloud_cover_100hPa',
                        'cloud_cover_50hPa',
                        'cloud_cover_30hPa',
                        'cloud_cover_20hPa',
                        'cloud_cover_10hPa'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/CMC/GEM",
            filename=f"GEM_Data.csv"):
    
    """
    This function retrieves CMC GEM time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
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
                                            'snow',
                                            'snowfall',
                                            'pressure_msl',
                                            'surface_pressure',
                                            'cloud_cover',
                                            'cloud_cover_low',
                                            'cloud_cover_mid',
                                            'cloud_cover_high',
                                            'et0_fao_evapotranspiration',
                                            'vapour_pressure_deficit',
                                            'weather_code',
                                            'showers',
                                            'wind_speed_10m',
                                            'wind_speed_40m',
                                            'wind_speed_80m',
                                            'wind_speed_120m',
                                            'wind_direction_10m',
                                            'wind_direction_40m',
                                            'wind_direction_80m',
                                            'wind_direction_120m',
                                            'temperature_40m',
                                            'temperature_80m',
                                            'temperature_120m',
                                            'wind_gusts_10m',
                                            'soil_temperature_0_to_10cm',
                                            'soil_moisture_0_to_10cm',
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
                                            'temperature_30hPa',
                                            'temperature_20hPa',
                                            'temperature_10hPa',
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
                                            'dew_point_30hPa',
                                            'dew_point_20hPa',
                                            'dew_point_10hPa',
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
                                            'relative_humidity_30hPa',
                                            'relative_humidity_20hPa',
                                            'relative_humidity_10hPa',
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
                                            'wind_speed_30hPa',
                                            'wind_speed_20hPa',
                                            'wind_speed_10hPa',
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
                                            'wind_direction_30hPa',
                                            'wind_direction_20hPa',
                                            'wind_direction_10hPa',
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
                                            'geopotential_height_50hPa',
                                            'geopotential_height_30hPa',
                                            'geopotential_height_20hPa',
                                            'geopotential_height_10hPa',
                                            'cloud_cover_1000hPa',
                                            'cloud_cover_925hPa',
                                            'cloud_cover_850hPa',
                                            'cloud_cover_700hPa',
                                            'cloud_cover_600hPa',
                                            'cloud_cover_500hPa',
                                            'cloud_cover_400hPa',
                                            'cloud_cover_300hPa',
                                            'cloud_cover_250hPa',
                                            'cloud_cover_200hPa',
                                            'cloud_cover_150hPa',
                                            'cloud_cover_100hPa',
                                            'cloud_cover_50hPa',
                                            'cloud_cover_30hPa',
                                            'cloud_cover_20hPa',
                                            'cloud_cover_10hPa']
                                            
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
    
    A Pandas.DataFrame of the CMC GEM time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 10:
        print(f"The maximum number of days that can be retrieved is 10. Setting 'days' to 10.")
        days = 10
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=gem_seamless"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
        
    else:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=gem_seamless"
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
    
    """
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
    """
    
    if days > 36:
        print(f"The maximum number of days that can be retrieved is 36. Setting 'days' to 36.")
        days = 36
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://ensemble-api.open-meteo.com/v1/ensemble?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=gem_global_ensemble"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
                
    else:
        response = _requests.get(f"https://ensemble-api.open-meteo.com/v1/ensemble?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=gem_global_ensemble"
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


