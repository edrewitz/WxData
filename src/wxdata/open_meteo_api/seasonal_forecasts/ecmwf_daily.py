"""
This file hosts the ECMWF EC46 & SEAS5 Seasonal Froecasts from Open-Meteo API.

(C) Eric J. Drewitz 2025-2026
"""
import requests as _requests
import pandas as _pd
from wxdata.utils.api import(
    json_to_pandas as _json_to_pandas,
    server_response as _server_response,
    df_to_csv as _df_to_csv
)

def ec46_seas5_daily_point_forecast_all_members(latitude,
            longitude,
            days=46,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m_max',
                        'temperature_2m_min',
                        'temperature_2m_mean',
                        'apparent_temperature_min',
                        'apparent_temperature_mean',
                        'apparent_temperature_max',
                        'relative_humidity_2m_min',
                        'relative_humidity_2m_mean',
                        'relative_humidity_2m_max',
                        'dew_point_2m_min',
                        'dew_point_2m_mean',
                        'dew_point_2m_max',
                        'precipitation_sum',
                        'rain_sum',
                        'showers_sum',
                        'snowfall_sum',
                        'snowfall_water_equivalent_sum',
                        'surface_pressure_min',
                        'pressure_msl_min',
                        'pressure_msl_mean',
                        'pressure_msl_max',
                        'surface_pressure_max',
                        'surface_pressure_mean',
                        'sea_surface_temperature_mean',
                        'sea_surface_temperature_max',
                        'sea_surface_temperature_min',
                        'cloud_cover_min',
                        'cloud_cover_mean',
                        'cloud_cover_max',
                        'et0_fao_evapotranspiration_sum',
                        'shortwave_radiation_sum',
                        'sunrise',
                        'sunset',
                        'weather_code',
                        'wet_bulb_temperature_2m_min',
                        'wet_bulb_temperature_2m_mean',
                        'wet_bulb_temperature_2m_max',
                        'wind_speed_10m_mean',
                        'wind_speed_10m_min',
                        'wind_speed_10m_max',
                        'wind_speed_100m_mean',
                        'wind_speed_100m_min',
                        'wind_speed_100m_max',
                        'wind_speed_200m_max',
                        'wind_speed_200m_mean',
                        'wind_speed_200m_min',
                        'wind_gusts_10m_min',
                        'wind_gusts_10m_mean',
                        'wind_gusts_10m_max',
                        'wind_direction_10m_dominant',
                        'wind_direction_100m_dominant',
                        'wind_direction_200m_dominant',
                        'soil_temperature_0_to_7cm_mean',
                        'soil_temperature_7_to_28cm_mean',
                        'soil_temperature_28_to_100cm_mean',
                        'soil_temperature_100_to_255cm_mean',
                        'soil_moisture_0_to_7cm_mean',
                        'soil_moisture_7_to_28cm_mean',
                        'soil_moisture_28_to_100cm_mean',
                        'soil_moisture_100_to_255cm_mean'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/ECMWF/Seamless Blend/Daily",
            filename=f"EC46_SEAS5_Members_Data.csv"):
    
    """
    This function retrieves ECMWF Seasonal Forecast (EC46 + SEAS5) time series all ensemble members forecast from the Open-Meteo API for a given point of latitude/longitude.
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) days (Integer) - Default=46. Amount of days to go out for the forecast. Maximum is 46.
    
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
        
    5) variables (String List) - Default=['temperature_2m_max',
                                            'temperature_2m_min',
                                            'temperature_2m_mean',
                                            'apparent_temperature_min',
                                            'apparent_temperature_mean',
                                            'apparent_temperature_max',
                                            'relative_humidity_2m_min',
                                            'relative_humidity_2m_mean',
                                            'relative_humidity_2m_max',
                                            'dew_point_2m_min',
                                            'dew_point_2m_mean',
                                            'dew_point_2m_max',
                                            'precipitation_sum',
                                            'rain_sum',
                                            'showers_sum',
                                            'snowfall_sum',
                                            'snowfall_water_equivalent_sum',
                                            'surface_pressure_min',
                                            'pressure_msl_min',
                                            'pressure_msl_mean',
                                            'pressure_msl_max',
                                            'surface_pressure_max',
                                            'surface_pressure_mean',
                                            'sea_surface_temperature_mean',
                                            'sea_surface_temperature_max',
                                            'sea_surface_temperature_min',
                                            'cloud_cover_min',
                                            'cloud_cover_mean',
                                            'cloud_cover_max',
                                            'et0_fao_evapotranspiration_sum',
                                            'shortwave_radiation_sum',
                                            'sunrise',
                                            'sunset',
                                            'weather_code',
                                            'wet_bulb_temperature_2m_min',
                                            'wet_bulb_temperature_2m_mean',
                                            'wet_bulb_temperature_2m_max',
                                            'wind_speed_10m_mean',
                                            'wind_speed_10m_min',
                                            'wind_speed_10m_max',
                                            'wind_speed_100m_mean',
                                            'wind_speed_100m_min',
                                            'wind_speed_100m_max',
                                            'wind_speed_200m_max',
                                            'wind_speed_200m_mean',
                                            'wind_speed_200m_min',
                                            'wind_gusts_10m_min',
                                            'wind_gusts_10m_mean',
                                            'wind_gusts_10m_max',
                                            'wind_direction_10m_dominant',
                                            'wind_direction_100m_dominant',
                                            'wind_direction_200m_dominant',
                                            'soil_temperature_0_to_7cm_mean',
                                            'soil_temperature_7_to_28cm_mean',
                                            'soil_temperature_28_to_100cm_mean',
                                            'soil_temperature_100_to_255cm_mean',
                                            'soil_moisture_0_to_7cm_mean',
                                            'soil_moisture_7_to_28cm_mean',
                                            'soil_moisture_28_to_100cm_mean',
                                            'soil_moisture_100_to_255cm_mean']

                                            
                The list of variables to choose from.
                
    6) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    7) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}
    
    8) path (String) - The path where the CSV file is saved to.
    
    9) filename (String) - The filename for the CSV file.                     
                    
    Returns
    -------
    
    A Pandas.DataFrame of the ECMWF Seasonal Forecast (EC46 + SEAS5) time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 46:
        print(f"The maximum number of days that can be retrieved is 46 for the EC46 + SEAS5 combination. Setting 'days' to 46.")
        days = 46
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://seasonal-api.open-meteo.com/v1/seasonal?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&daily={','.join(variables)}&models=ecmwf_seasonal_seamless"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
        
    else:
        response = _requests.get(f"https://seasonal-api.open-meteo.com/v1/seasonal?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&daily={','.join(variables)}&ecmwf_seasonal_seamless"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}",
                             proxies=proxies)
        
    _server_response(response)
        
    data = response.json()
    
    df = _json_to_pandas(data,
                         field='daily')
    
    df['time'] = _pd.to_datetime(df['time'])
    
    if to_csv == True:
        _df_to_csv(df,
                   path,
                   filename)
    
    return df

def ec46_daily_point_forecast_all_members(latitude,
            longitude,
            days=46,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m_max',
                        'temperature_2m_min',
                        'temperature_2m_mean',
                        'apparent_temperature_min',
                        'apparent_temperature_mean',
                        'apparent_temperature_max',
                        'relative_humidity_2m_min',
                        'relative_humidity_2m_mean',
                        'relative_humidity_2m_max',
                        'dew_point_2m_min',
                        'dew_point_2m_mean',
                        'dew_point_2m_max',
                        'precipitation_sum',
                        'rain_sum',
                        'showers_sum',
                        'snowfall_sum',
                        'snowfall_water_equivalent_sum',
                        'surface_pressure_min',
                        'pressure_msl_min',
                        'pressure_msl_mean',
                        'pressure_msl_max',
                        'surface_pressure_max',
                        'surface_pressure_mean',
                        'sea_surface_temperature_mean',
                        'sea_surface_temperature_max',
                        'sea_surface_temperature_min',
                        'cloud_cover_min',
                        'cloud_cover_mean',
                        'cloud_cover_max',
                        'et0_fao_evapotranspiration_sum',
                        'shortwave_radiation_sum',
                        'sunrise',
                        'sunset',
                        'weather_code',
                        'wet_bulb_temperature_2m_min',
                        'wet_bulb_temperature_2m_mean',
                        'wet_bulb_temperature_2m_max',
                        'wind_speed_10m_mean',
                        'wind_speed_10m_min',
                        'wind_speed_10m_max',
                        'wind_speed_100m_mean',
                        'wind_speed_100m_min',
                        'wind_speed_100m_max',
                        'wind_speed_200m_max',
                        'wind_speed_200m_mean',
                        'wind_speed_200m_min',
                        'wind_gusts_10m_min',
                        'wind_gusts_10m_mean',
                        'wind_gusts_10m_max',
                        'wind_direction_10m_dominant',
                        'wind_direction_100m_dominant',
                        'wind_direction_200m_dominant',
                        'soil_temperature_0_to_7cm_mean',
                        'soil_temperature_7_to_28cm_mean',
                        'soil_temperature_28_to_100cm_mean',
                        'soil_temperature_100_to_255cm_mean',
                        'soil_moisture_0_to_7cm_mean',
                        'soil_moisture_7_to_28cm_mean',
                        'soil_moisture_28_to_100cm_mean',
                        'soil_moisture_100_to_255cm_mean'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/ECMWF/EC46/Daily",
            filename=f"EC46_Members_Data.csv"):
    
    """
    This function retrieves ECMWF EC46 Seasonal Forecast time series all ensemble members forecast from the Open-Meteo API for a given point of latitude/longitude.
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) days (Integer) - Default=46. Amount of days to go out for the forecast. Maximum is 46.
    
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
        
    5) variables (String List) - Default=['temperature_2m_max',
                                            'temperature_2m_min',
                                            'temperature_2m_mean',
                                            'apparent_temperature_min',
                                            'apparent_temperature_mean',
                                            'apparent_temperature_max',
                                            'relative_humidity_2m_min',
                                            'relative_humidity_2m_mean',
                                            'relative_humidity_2m_max',
                                            'dew_point_2m_min',
                                            'dew_point_2m_mean',
                                            'dew_point_2m_max',
                                            'precipitation_sum',
                                            'rain_sum',
                                            'showers_sum',
                                            'snowfall_sum',
                                            'snowfall_water_equivalent_sum',
                                            'surface_pressure_min',
                                            'pressure_msl_min',
                                            'pressure_msl_mean',
                                            'pressure_msl_max',
                                            'surface_pressure_max',
                                            'surface_pressure_mean',
                                            'sea_surface_temperature_mean',
                                            'sea_surface_temperature_max',
                                            'sea_surface_temperature_min',
                                            'cloud_cover_min',
                                            'cloud_cover_mean',
                                            'cloud_cover_max',
                                            'et0_fao_evapotranspiration_sum',
                                            'shortwave_radiation_sum',
                                            'sunrise',
                                            'sunset',
                                            'weather_code',
                                            'wet_bulb_temperature_2m_min',
                                            'wet_bulb_temperature_2m_mean',
                                            'wet_bulb_temperature_2m_max',
                                            'wind_speed_10m_mean',
                                            'wind_speed_10m_min',
                                            'wind_speed_10m_max',
                                            'wind_speed_100m_mean',
                                            'wind_speed_100m_min',
                                            'wind_speed_100m_max',
                                            'wind_speed_200m_max',
                                            'wind_speed_200m_mean',
                                            'wind_speed_200m_min',
                                            'wind_gusts_10m_min',
                                            'wind_gusts_10m_mean',
                                            'wind_gusts_10m_max',
                                            'wind_direction_10m_dominant',
                                            'wind_direction_100m_dominant',
                                            'wind_direction_200m_dominant',
                                            'soil_temperature_0_to_7cm_mean',
                                            'soil_temperature_7_to_28cm_mean',
                                            'soil_temperature_28_to_100cm_mean',
                                            'soil_temperature_100_to_255cm_mean',
                                            'soil_moisture_0_to_7cm_mean',
                                            'soil_moisture_7_to_28cm_mean',
                                            'soil_moisture_28_to_100cm_mean',
                                            'soil_moisture_100_to_255cm_mean']

                                            
                The list of variables to choose from.
                
    6) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    7) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}
    
    8) path (String) - The path where the CSV file is saved to.
    
    9) filename (String) - The filename for the CSV file.                     
                    
    Returns
    -------
    
    A Pandas.DataFrame of the ECMWF EC46 Seasonal Forecast time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 46:
        print(f"The maximum number of days that can be retrieved is 46 for the EC46. Setting 'days' to 46.")
        days = 46
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://seasonal-api.open-meteo.com/v1/seasonal?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&daily={','.join(variables)}&models=ecmwf_ec46"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
        
    else:
        response = _requests.get(f"https://seasonal-api.open-meteo.com/v1/seasonal?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&daily={','.join(variables)}&ecmwf_ec46"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}",
                             proxies=proxies)
        
    _server_response(response)
        
    data = response.json()
    
    df = _json_to_pandas(data,
                         field='daily')
    
    df['time'] = _pd.to_datetime(df['time'])
    
    if to_csv == True:
        _df_to_csv(df,
                   path,
                   filename)
    
    return df

def seas5_daily_point_forecast_all_members(latitude,
            longitude,
            days=183,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m_max',
                        'temperature_2m_min',
                        'temperature_2m_mean',
                        'apparent_temperature_min',
                        'apparent_temperature_mean',
                        'apparent_temperature_max',
                        'relative_humidity_2m_min',
                        'relative_humidity_2m_mean',
                        'relative_humidity_2m_max',
                        'dew_point_2m_min',
                        'dew_point_2m_mean',
                        'dew_point_2m_max',
                        'precipitation_sum',
                        'rain_sum',
                        'showers_sum',
                        'snowfall_sum',
                        'snowfall_water_equivalent_sum',
                        'surface_pressure_min',
                        'pressure_msl_min',
                        'pressure_msl_mean',
                        'pressure_msl_max',
                        'surface_pressure_max',
                        'surface_pressure_mean',
                        'sea_surface_temperature_mean',
                        'sea_surface_temperature_max',
                        'sea_surface_temperature_min',
                        'cloud_cover_min',
                        'cloud_cover_mean',
                        'cloud_cover_max',
                        'et0_fao_evapotranspiration_sum',
                        'shortwave_radiation_sum',
                        'sunrise',
                        'sunset',
                        'weather_code',
                        'wet_bulb_temperature_2m_min',
                        'wet_bulb_temperature_2m_mean',
                        'wet_bulb_temperature_2m_max',
                        'wind_speed_10m_mean',
                        'wind_speed_10m_min',
                        'wind_speed_10m_max',
                        'wind_speed_100m_mean',
                        'wind_speed_100m_min',
                        'wind_speed_100m_max',
                        'wind_speed_200m_max',
                        'wind_speed_200m_mean',
                        'wind_speed_200m_min',
                        'wind_gusts_10m_min',
                        'wind_gusts_10m_mean',
                        'wind_gusts_10m_max',
                        'wind_direction_10m_dominant',
                        'wind_direction_100m_dominant',
                        'wind_direction_200m_dominant',
                        'soil_temperature_0_to_7cm_mean',
                        'soil_temperature_7_to_28cm_mean',
                        'soil_temperature_28_to_100cm_mean',
                        'soil_temperature_100_to_255cm_mean',
                        'soil_moisture_0_to_7cm_mean',
                        'soil_moisture_7_to_28cm_mean',
                        'soil_moisture_28_to_100cm_mean',
                        'soil_moisture_100_to_255cm_mean'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/ECMWF/SEAS5/Daily",
            filename=f"SEAS5_Members_Data.csv"):
    
    """
    This function retrieves ECMWF SEAS5 Seasonal Forecast time series all ensemble members forecast from the Open-Meteo API for a given point of latitude/longitude.
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) days (Integer) - Default=183 (6-months). Amount of days to go out for the forecast. Maximum is 217.
    
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
        
    5) variables (String List) - Default=['temperature_2m_max',
                                            'temperature_2m_min',
                                            'temperature_2m_mean',
                                            'apparent_temperature_min',
                                            'apparent_temperature_mean',
                                            'apparent_temperature_max',
                                            'relative_humidity_2m_min',
                                            'relative_humidity_2m_mean',
                                            'relative_humidity_2m_max',
                                            'dew_point_2m_min',
                                            'dew_point_2m_mean',
                                            'dew_point_2m_max',
                                            'precipitation_sum',
                                            'rain_sum',
                                            'showers_sum',
                                            'snowfall_sum',
                                            'snowfall_water_equivalent_sum',
                                            'surface_pressure_min',
                                            'pressure_msl_min',
                                            'pressure_msl_mean',
                                            'pressure_msl_max',
                                            'surface_pressure_max',
                                            'surface_pressure_mean',
                                            'sea_surface_temperature_mean',
                                            'sea_surface_temperature_max',
                                            'sea_surface_temperature_min',
                                            'cloud_cover_min',
                                            'cloud_cover_mean',
                                            'cloud_cover_max',
                                            'et0_fao_evapotranspiration_sum',
                                            'shortwave_radiation_sum',
                                            'sunrise',
                                            'sunset',
                                            'weather_code',
                                            'wet_bulb_temperature_2m_min',
                                            'wet_bulb_temperature_2m_mean',
                                            'wet_bulb_temperature_2m_max',
                                            'wind_speed_10m_mean',
                                            'wind_speed_10m_min',
                                            'wind_speed_10m_max',
                                            'wind_speed_100m_mean',
                                            'wind_speed_100m_min',
                                            'wind_speed_100m_max',
                                            'wind_speed_200m_max',
                                            'wind_speed_200m_mean',
                                            'wind_speed_200m_min',
                                            'wind_gusts_10m_min',
                                            'wind_gusts_10m_mean',
                                            'wind_gusts_10m_max',
                                            'wind_direction_10m_dominant',
                                            'wind_direction_100m_dominant',
                                            'wind_direction_200m_dominant',
                                            'soil_temperature_0_to_7cm_mean',
                                            'soil_temperature_7_to_28cm_mean',
                                            'soil_temperature_28_to_100cm_mean',
                                            'soil_temperature_100_to_255cm_mean',
                                            'soil_moisture_0_to_7cm_mean',
                                            'soil_moisture_7_to_28cm_mean',
                                            'soil_moisture_28_to_100cm_mean',
                                            'soil_moisture_100_to_255cm_mean']

                                            
                The list of variables to choose from.
                
    6) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    7) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}
    
    8) path (String) - The path where the CSV file is saved to.
    
    9) filename (String) - The filename for the CSV file.                     
                    
    Returns
    -------
    
    A Pandas.DataFrame of the ECMWF SEAS5 Seasonal Forecast time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 217:
        print(f"The maximum number of days that can be retrieved is 217 (7-months) for the SEAS5. Setting 'days' to 217.")
        days = 217
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://seasonal-api.open-meteo.com/v1/seasonal?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&daily={','.join(variables)}&models=ecmwf_seas5"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
        
    else:
        response = _requests.get(f"https://seasonal-api.open-meteo.com/v1/seasonal?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&daily={','.join(variables)}&ecmwf_seas5"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}",
                             proxies=proxies)
        
    _server_response(response)
        
    data = response.json()
    
    df = _json_to_pandas(data,
                         field='daily')
    
    df['time'] = _pd.to_datetime(df['time'])
    
    if to_csv == True:
        _df_to_csv(df,
                   path,
                   filename)
    
    return df

def ec46_seas5_daily_point_forecast_ensemble_mean(latitude,
            longitude,
            days=46,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m_max',
                        'temperature_2m_min',
                        'temperature_2m_mean',
                        'apparent_temperature_min',
                        'apparent_temperature_mean',
                        'apparent_temperature_max',
                        'relative_humidity_2m_min',
                        'relative_humidity_2m_mean',
                        'relative_humidity_2m_max',
                        'dew_point_2m_min',
                        'dew_point_2m_mean',
                        'dew_point_2m_max',
                        'precipitation_sum',
                        'rain_sum',
                        'showers_sum',
                        'snowfall_sum',
                        'snowfall_water_equivalent_sum',
                        'surface_pressure_min',
                        'pressure_msl_min',
                        'pressure_msl_mean',
                        'pressure_msl_max',
                        'surface_pressure_max',
                        'surface_pressure_mean',
                        'sea_surface_temperature_mean',
                        'sea_surface_temperature_max',
                        'sea_surface_temperature_min',
                        'cloud_cover_min',
                        'cloud_cover_mean',
                        'cloud_cover_max',
                        'et0_fao_evapotranspiration_sum',
                        'shortwave_radiation_sum',
                        'sunrise',
                        'sunset',
                        'weather_code',
                        'wet_bulb_temperature_2m_min',
                        'wet_bulb_temperature_2m_mean',
                        'wet_bulb_temperature_2m_max',
                        'wind_speed_10m_mean',
                        'wind_speed_10m_min',
                        'wind_speed_10m_max',
                        'wind_speed_100m_mean',
                        'wind_speed_100m_min',
                        'wind_speed_100m_max',
                        'wind_speed_200m_max',
                        'wind_speed_200m_mean',
                        'wind_speed_200m_min',
                        'wind_gusts_10m_min',
                        'wind_gusts_10m_mean',
                        'wind_gusts_10m_max',
                        'wind_direction_10m_dominant',
                        'wind_direction_100m_dominant',
                        'wind_direction_200m_dominant',
                        'soil_temperature_0_to_7cm_mean',
                        'soil_temperature_7_to_28cm_mean',
                        'soil_temperature_28_to_100cm_mean',
                        'soil_temperature_100_to_255cm_mean',
                        'soil_moisture_0_to_7cm_mean',
                        'soil_moisture_7_to_28cm_mean',
                        'soil_moisture_28_to_100cm_mean',
                        'soil_moisture_100_to_255cm_mean'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/ECMWF/Seamless Blend/Daily",
            filename=f"EC46_SEAS5_Ensemble_Mean_Data.csv"):
    
    """
    This function retrieves ECMWF Seasonal Forecast (EC46 + SEAS5) time series ensemble mean forecast from the Open-Meteo API for a given point of latitude/longitude.
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) days (Integer) - Default=46. Amount of days to go out for the forecast. Maximum is 46.
    
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
        
    5) variables (String List) - Default=['temperature_2m_max',
                                            'temperature_2m_min',
                                            'temperature_2m_mean',
                                            'apparent_temperature_min',
                                            'apparent_temperature_mean',
                                            'apparent_temperature_max',
                                            'relative_humidity_2m_min',
                                            'relative_humidity_2m_mean',
                                            'relative_humidity_2m_max',
                                            'dew_point_2m_min',
                                            'dew_point_2m_mean',
                                            'dew_point_2m_max',
                                            'precipitation_sum',
                                            'rain_sum',
                                            'showers_sum',
                                            'snowfall_sum',
                                            'snowfall_water_equivalent_sum',
                                            'surface_pressure_min',
                                            'pressure_msl_min',
                                            'pressure_msl_mean',
                                            'pressure_msl_max',
                                            'surface_pressure_max',
                                            'surface_pressure_mean',
                                            'sea_surface_temperature_mean',
                                            'sea_surface_temperature_max',
                                            'sea_surface_temperature_min',
                                            'cloud_cover_min',
                                            'cloud_cover_mean',
                                            'cloud_cover_max',
                                            'et0_fao_evapotranspiration_sum',
                                            'shortwave_radiation_sum',
                                            'sunrise',
                                            'sunset',
                                            'weather_code',
                                            'wet_bulb_temperature_2m_min',
                                            'wet_bulb_temperature_2m_mean',
                                            'wet_bulb_temperature_2m_max',
                                            'wind_speed_10m_mean',
                                            'wind_speed_10m_min',
                                            'wind_speed_10m_max',
                                            'wind_speed_100m_mean',
                                            'wind_speed_100m_min',
                                            'wind_speed_100m_max',
                                            'wind_speed_200m_max',
                                            'wind_speed_200m_mean',
                                            'wind_speed_200m_min',
                                            'wind_gusts_10m_min',
                                            'wind_gusts_10m_mean',
                                            'wind_gusts_10m_max',
                                            'wind_direction_10m_dominant',
                                            'wind_direction_100m_dominant',
                                            'wind_direction_200m_dominant',
                                            'soil_temperature_0_to_7cm_mean',
                                            'soil_temperature_7_to_28cm_mean',
                                            'soil_temperature_28_to_100cm_mean',
                                            'soil_temperature_100_to_255cm_mean',
                                            'soil_moisture_0_to_7cm_mean',
                                            'soil_moisture_7_to_28cm_mean',
                                            'soil_moisture_28_to_100cm_mean',
                                            'soil_moisture_100_to_255cm_mean']

                                            
                The list of variables to choose from.
                
    6) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    7) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}
    
    8) path (String) - The path where the CSV file is saved to.
    
    9) filename (String) - The filename for the CSV file.                     
                    
    Returns
    -------
    
    A Pandas.DataFrame of the ECMWF Seasonal Forecast (EC46 + SEAS5) time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 46:
        print(f"The maximum number of days that can be retrieved is 46 for the EC46 + SEAS5 combination. Setting 'days' to 46.")
        days = 46
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://seasonal-api.open-meteo.com/v1/seasonal?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&daily={','.join(variables)}&models=ecmwf_seasonal_ensemble_mean_seamless"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
        
    else:
        response = _requests.get(f"https://seasonal-api.open-meteo.com/v1/seasonal?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&daily={','.join(variables)}&ecmwf_seasonal_ensemble_mean_seamless"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}",
                             proxies=proxies)
        
    _server_response(response)
        
    data = response.json()
    
    df = _json_to_pandas(data,
                         field='daily')
    
    df['time'] = _pd.to_datetime(df['time'])
    
    if to_csv == True:
        _df_to_csv(df,
                   path,
                   filename)
    
    return df

def ec46_daily_point_forecast_ensemble_mean(latitude,
            longitude,
            days=46,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m_max',
                        'temperature_2m_min',
                        'temperature_2m_mean',
                        'apparent_temperature_min',
                        'apparent_temperature_mean',
                        'apparent_temperature_max',
                        'relative_humidity_2m_min',
                        'relative_humidity_2m_mean',
                        'relative_humidity_2m_max',
                        'dew_point_2m_min',
                        'dew_point_2m_mean',
                        'dew_point_2m_max',
                        'precipitation_sum',
                        'rain_sum',
                        'showers_sum',
                        'snowfall_sum',
                        'snowfall_water_equivalent_sum',
                        'surface_pressure_min',
                        'pressure_msl_min',
                        'pressure_msl_mean',
                        'pressure_msl_max',
                        'surface_pressure_max',
                        'surface_pressure_mean',
                        'sea_surface_temperature_mean',
                        'sea_surface_temperature_max',
                        'sea_surface_temperature_min',
                        'cloud_cover_min',
                        'cloud_cover_mean',
                        'cloud_cover_max',
                        'et0_fao_evapotranspiration_sum',
                        'shortwave_radiation_sum',
                        'sunrise',
                        'sunset',
                        'weather_code',
                        'wet_bulb_temperature_2m_min',
                        'wet_bulb_temperature_2m_mean',
                        'wet_bulb_temperature_2m_max',
                        'wind_speed_10m_mean',
                        'wind_speed_10m_min',
                        'wind_speed_10m_max',
                        'wind_speed_100m_mean',
                        'wind_speed_100m_min',
                        'wind_speed_100m_max',
                        'wind_speed_200m_max',
                        'wind_speed_200m_mean',
                        'wind_speed_200m_min',
                        'wind_gusts_10m_min',
                        'wind_gusts_10m_mean',
                        'wind_gusts_10m_max',
                        'wind_direction_10m_dominant',
                        'wind_direction_100m_dominant',
                        'wind_direction_200m_dominant',
                        'soil_temperature_0_to_7cm_mean',
                        'soil_temperature_7_to_28cm_mean',
                        'soil_temperature_28_to_100cm_mean',
                        'soil_temperature_100_to_255cm_mean',
                        'soil_moisture_0_to_7cm_mean',
                        'soil_moisture_7_to_28cm_mean',
                        'soil_moisture_28_to_100cm_mean',
                        'soil_moisture_100_to_255cm_mean'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/ECMWF/EC46/Daily",
            filename=f"EC46_Ensemble_Mean_Data.csv"):
    
    """
    This function retrieves ECMWF EC46 Seasonal Forecast time series ensemble mean forecast from the Open-Meteo API for a given point of latitude/longitude.
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) days (Integer) - Default=46. Amount of days to go out for the forecast. Maximum is 46.
    
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
        
    5) variables (String List) - Default=['temperature_2m_max',
                                            'temperature_2m_min',
                                            'temperature_2m_mean',
                                            'apparent_temperature_min',
                                            'apparent_temperature_mean',
                                            'apparent_temperature_max',
                                            'relative_humidity_2m_min',
                                            'relative_humidity_2m_mean',
                                            'relative_humidity_2m_max',
                                            'dew_point_2m_min',
                                            'dew_point_2m_mean',
                                            'dew_point_2m_max',
                                            'precipitation_sum',
                                            'rain_sum',
                                            'showers_sum',
                                            'snowfall_sum',
                                            'snowfall_water_equivalent_sum',
                                            'surface_pressure_min',
                                            'pressure_msl_min',
                                            'pressure_msl_mean',
                                            'pressure_msl_max',
                                            'surface_pressure_max',
                                            'surface_pressure_mean',
                                            'sea_surface_temperature_mean',
                                            'sea_surface_temperature_max',
                                            'sea_surface_temperature_min',
                                            'cloud_cover_min',
                                            'cloud_cover_mean',
                                            'cloud_cover_max',
                                            'et0_fao_evapotranspiration_sum',
                                            'shortwave_radiation_sum',
                                            'sunrise',
                                            'sunset',
                                            'weather_code',
                                            'wet_bulb_temperature_2m_min',
                                            'wet_bulb_temperature_2m_mean',
                                            'wet_bulb_temperature_2m_max',
                                            'wind_speed_10m_mean',
                                            'wind_speed_10m_min',
                                            'wind_speed_10m_max',
                                            'wind_speed_100m_mean',
                                            'wind_speed_100m_min',
                                            'wind_speed_100m_max',
                                            'wind_speed_200m_max',
                                            'wind_speed_200m_mean',
                                            'wind_speed_200m_min',
                                            'wind_gusts_10m_min',
                                            'wind_gusts_10m_mean',
                                            'wind_gusts_10m_max',
                                            'wind_direction_10m_dominant',
                                            'wind_direction_100m_dominant',
                                            'wind_direction_200m_dominant',
                                            'soil_temperature_0_to_7cm_mean',
                                            'soil_temperature_7_to_28cm_mean',
                                            'soil_temperature_28_to_100cm_mean',
                                            'soil_temperature_100_to_255cm_mean',
                                            'soil_moisture_0_to_7cm_mean',
                                            'soil_moisture_7_to_28cm_mean',
                                            'soil_moisture_28_to_100cm_mean',
                                            'soil_moisture_100_to_255cm_mean']

                                            
                The list of variables to choose from.
                
    6) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    7) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}
    
    8) path (String) - The path where the CSV file is saved to.
    
    9) filename (String) - The filename for the CSV file.                     
                    
    Returns
    -------
    
    A Pandas.DataFrame of the ECMWF EC46 Seasonal Forecast time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 46:
        print(f"The maximum number of days that can be retrieved is 46 for the EC46. Setting 'days' to 46.")
        days = 46
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://seasonal-api.open-meteo.com/v1/seasonal?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&daily={','.join(variables)}&models=ecmwf_ec46_ensemble_mean"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
        
    else:
        response = _requests.get(f"https://seasonal-api.open-meteo.com/v1/seasonal?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&daily={','.join(variables)}&ecmwf_ec46_ensemble_mean"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}",
                             proxies=proxies)
        
    _server_response(response)
        
    data = response.json()
    
    df = _json_to_pandas(data,
                         field='daily')
    
    df['time'] = _pd.to_datetime(df['time'])
    
    if to_csv == True:
        _df_to_csv(df,
                   path,
                   filename)
    
    return df

def seas5_daily_point_forecast_ensemble_mean(latitude,
            longitude,
            days=183,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m_max',
                        'temperature_2m_min',
                        'temperature_2m_mean',
                        'apparent_temperature_min',
                        'apparent_temperature_mean',
                        'apparent_temperature_max',
                        'relative_humidity_2m_min',
                        'relative_humidity_2m_mean',
                        'relative_humidity_2m_max',
                        'dew_point_2m_min',
                        'dew_point_2m_mean',
                        'dew_point_2m_max',
                        'precipitation_sum',
                        'rain_sum',
                        'showers_sum',
                        'snowfall_sum',
                        'snowfall_water_equivalent_sum',
                        'surface_pressure_min',
                        'pressure_msl_min',
                        'pressure_msl_mean',
                        'pressure_msl_max',
                        'surface_pressure_max',
                        'surface_pressure_mean',
                        'sea_surface_temperature_mean',
                        'sea_surface_temperature_max',
                        'sea_surface_temperature_min',
                        'cloud_cover_min',
                        'cloud_cover_mean',
                        'cloud_cover_max',
                        'et0_fao_evapotranspiration_sum',
                        'shortwave_radiation_sum',
                        'sunrise',
                        'sunset',
                        'weather_code',
                        'wet_bulb_temperature_2m_min',
                        'wet_bulb_temperature_2m_mean',
                        'wet_bulb_temperature_2m_max',
                        'wind_speed_10m_mean',
                        'wind_speed_10m_min',
                        'wind_speed_10m_max',
                        'wind_speed_100m_mean',
                        'wind_speed_100m_min',
                        'wind_speed_100m_max',
                        'wind_speed_200m_max',
                        'wind_speed_200m_mean',
                        'wind_speed_200m_min',
                        'wind_gusts_10m_min',
                        'wind_gusts_10m_mean',
                        'wind_gusts_10m_max',
                        'wind_direction_10m_dominant',
                        'wind_direction_100m_dominant',
                        'wind_direction_200m_dominant',
                        'soil_temperature_0_to_7cm_mean',
                        'soil_temperature_7_to_28cm_mean',
                        'soil_temperature_28_to_100cm_mean',
                        'soil_temperature_100_to_255cm_mean',
                        'soil_moisture_0_to_7cm_mean',
                        'soil_moisture_7_to_28cm_mean',
                        'soil_moisture_28_to_100cm_mean',
                        'soil_moisture_100_to_255cm_mean'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/ECMWF/SEAS5/Daily",
            filename=f"SEAS5_Ensemble_Mean_Data.csv"):
    
    """
    This function retrieves ECMWF SEAS5 Seasonal Forecast time series ensemble mean forecast from the Open-Meteo API for a given point of latitude/longitude.
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) days (Integer) - Default=183 (6-months). Amount of days to go out for the forecast. Maximum is 217.
    
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
        
    5) variables (String List) - Default=['temperature_2m_max',
                                            'temperature_2m_min',
                                            'temperature_2m_mean',
                                            'apparent_temperature_min',
                                            'apparent_temperature_mean',
                                            'apparent_temperature_max',
                                            'relative_humidity_2m_min',
                                            'relative_humidity_2m_mean',
                                            'relative_humidity_2m_max',
                                            'dew_point_2m_min',
                                            'dew_point_2m_mean',
                                            'dew_point_2m_max',
                                            'precipitation_sum',
                                            'rain_sum',
                                            'showers_sum',
                                            'snowfall_sum',
                                            'snowfall_water_equivalent_sum',
                                            'surface_pressure_min',
                                            'pressure_msl_min',
                                            'pressure_msl_mean',
                                            'pressure_msl_max',
                                            'surface_pressure_max',
                                            'surface_pressure_mean',
                                            'sea_surface_temperature_mean',
                                            'sea_surface_temperature_max',
                                            'sea_surface_temperature_min',
                                            'cloud_cover_min',
                                            'cloud_cover_mean',
                                            'cloud_cover_max',
                                            'et0_fao_evapotranspiration_sum',
                                            'shortwave_radiation_sum',
                                            'sunrise',
                                            'sunset',
                                            'weather_code',
                                            'wet_bulb_temperature_2m_min',
                                            'wet_bulb_temperature_2m_mean',
                                            'wet_bulb_temperature_2m_max',
                                            'wind_speed_10m_mean',
                                            'wind_speed_10m_min',
                                            'wind_speed_10m_max',
                                            'wind_speed_100m_mean',
                                            'wind_speed_100m_min',
                                            'wind_speed_100m_max',
                                            'wind_speed_200m_max',
                                            'wind_speed_200m_mean',
                                            'wind_speed_200m_min',
                                            'wind_gusts_10m_min',
                                            'wind_gusts_10m_mean',
                                            'wind_gusts_10m_max',
                                            'wind_direction_10m_dominant',
                                            'wind_direction_100m_dominant',
                                            'wind_direction_200m_dominant',
                                            'soil_temperature_0_to_7cm_mean',
                                            'soil_temperature_7_to_28cm_mean',
                                            'soil_temperature_28_to_100cm_mean',
                                            'soil_temperature_100_to_255cm_mean',
                                            'soil_moisture_0_to_7cm_mean',
                                            'soil_moisture_7_to_28cm_mean',
                                            'soil_moisture_28_to_100cm_mean',
                                            'soil_moisture_100_to_255cm_mean']

                                            
                The list of variables to choose from.
                
    6) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    7) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}
    
    8) path (String) - The path where the CSV file is saved to.
    
    9) filename (String) - The filename for the CSV file.                     
                    
    Returns
    -------
    
    A Pandas.DataFrame of the ECMWF SEAS5 Seasonal Forecast time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 217:
        print(f"The maximum number of days that can be retrieved is 217 (7-months) for the SEAS5. Setting 'days' to 217.")
        days = 217
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://seasonal-api.open-meteo.com/v1/seasonal?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&daily={','.join(variables)}&models=ecmwf_seas5_ensemble_mean"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
        
    else:
        response = _requests.get(f"https://seasonal-api.open-meteo.com/v1/seasonal?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&daily={','.join(variables)}&ecmwf_seas5_ensemble_mean"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}",
                             proxies=proxies)
        
    _server_response(response)
        
    data = response.json()
    
    df = _json_to_pandas(data,
                         field='daily')
    
    df['time'] = _pd.to_datetime(df['time'])
    
    if to_csv == True:
        _df_to_csv(df,
                   path,
                   filename)
    
    return df
