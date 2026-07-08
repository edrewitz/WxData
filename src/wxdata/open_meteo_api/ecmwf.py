"""
This file hosts the interface for the Open-Meteo API for ECMWF data.

(C) Eric J. Drewitz 2025-2026
"""
import requests as _requests
from wxdata.open_meteo_api.utils import(
    json_to_pandas as _json_to_pandas,
    server_response as _server_response
)

def ifs_point_forecast(latitude,
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
                        'showers',
                        'snowfall',
                        'runoff',
                        'visibility',
                        'weather_code',
                        'pressure_msl',
                        'surface_pressure',
                        'cloud_cover',
                        'cloud_cover_low',
                        'cloud_cover_mid',
                        'cloud_cover_high',
                        'sunshine_duration',
                        'potential_evapotranspiration',
                        'et0_fao_evapotranspiration',
                        'wind_speed_10m',
                        'wind_speed_100m',
                        'wind_speed_200m',
                        'wind_direction_10m',
                        'wind_direction_100m',
                        'wind_direction_200m',
                        'wind_gusts_10m',
                        'cape',
                        'convective_inhibition',
                        'total_column_integrated_water_vapour',
                        'vapour_pressure_deficit',
                        'surface_temperature',
                        'soil_temperature_0_to_7cm',
                        'soil_temperature_7_to_28cm',
                        'soil_temperature_28_to_100cm',
                        'soil_temperature_100_to_255cm',
                        'soil_moisture_0_to_7cm',
                        'soil_moisture_28_to_100cm',
                        'soil_moisture_7_to_28cm',
                        'soil_moisture_100_to_255cm',
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
                        'vertical_velocity_1000hPa',
                        'vertical_velocity_925hPa',
                        'vertical_velocity_850hPa',
                        'vertical_velocity_700hPa',
                        'vertical_velocity_600hPa',
                        'vertical_velocity_500hPa',
                        'vertical_velocity_400hPa',
                        'vertical_velocity_300hPa',
                        'vertical_velocity_250hPa',
                        'vertical_velocity_200hPa',
                        'vertical_velocity_150hPa',
                        'vertical_velocity_100hPa',
                        'vertical_velocity_50hPa',
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
                        'geopotential_height_50hPa'],
            proxies=None):
    
    """
    This function retrieves ECMWF IFS time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
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
                                            'showers',
                                            'snowfall',
                                            'runoff',
                                            'visibility',
                                            'weather_code',
                                            'pressure_msl',
                                            'surface_pressure',
                                            'cloud_cover',
                                            'cloud_cover_low',
                                            'cloud_cover_mid',
                                            'cloud_cover_high',
                                            'sunshine_duration',
                                            'potential_evapotranspiration',
                                            'et0_fao_evapotranspiration',
                                            'wind_speed_10m',
                                            'wind_speed_100m',
                                            'wind_speed_200m',
                                            'wind_direction_10m',
                                            'wind_direction_100m',
                                            'wind_direction_200m',
                                            'wind_gusts_10m',
                                            'cape',
                                            'convective_inhibition',
                                            'total_column_integrated_water_vapour',
                                            'vapour_pressure_deficit',
                                            'surface_temperature',
                                            'soil_temperature_0_to_7cm',
                                            'soil_temperature_7_to_28cm',
                                            'soil_temperature_28_to_100cm',
                                            'soil_temperature_100_to_255cm',
                                            'soil_moisture_0_to_7cm',
                                            'soil_moisture_28_to_100cm',
                                            'soil_moisture_7_to_28cm',
                                            'soil_moisture_100_to_255cm',
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
                                            'vertical_velocity_1000hPa',
                                            'vertical_velocity_925hPa',
                                            'vertical_velocity_850hPa',
                                            'vertical_velocity_700hPa',
                                            'vertical_velocity_600hPa',
                                            'vertical_velocity_500hPa',
                                            'vertical_velocity_400hPa',
                                            'vertical_velocity_300hPa',
                                            'vertical_velocity_250hPa',
                                            'vertical_velocity_200hPa',
                                            'vertical_velocity_150hPa',
                                            'vertical_velocity_100hPa',
                                            'vertical_velocity_50hPa',
                                            'geopotential_height_1000hPa',
                                            'geopotential_heighty_925hPa',
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
                                            'geopotential_height_50hPa']
                                            
                The list of variables to choose from.
                
    6) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
                    
    Returns
    -------
    
    A Pandas.DataFrame of the ECMWF IFS time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 14:
        print(f"The maximum number of days that can be retrieved is 14. Setting 'days' to 14.")
        days = 14
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ecmwf_ifs025"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
        
    else:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ecmwf_ifs025"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}",
                             proxies=proxies)
        
    _server_response(response)
        
    data = response.json()
    
    df = _json_to_pandas(data)
    
    return df

def aifs_point_forecast(latitude,
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
                        'showers',
                        'snowfall',
                        'runoff',
                        'visibility',
                        'weather_code',
                        'pressure_msl',
                        'surface_pressure',
                        'cloud_cover',
                        'cloud_cover_low',
                        'cloud_cover_mid',
                        'cloud_cover_high',
                        'sunshine_duration',
                        'potential_evapotranspiration',
                        'et0_fao_evapotranspiration',
                        'wind_speed_10m',
                        'wind_speed_100m',
                        'wind_speed_200m',
                        'wind_direction_10m',
                        'wind_direction_100m',
                        'wind_direction_200m',
                        'wind_gusts_10m',
                        'cape',
                        'convective_inhibition',
                        'total_column_integrated_water_vapour',
                        'vapour_pressure_deficit',
                        'surface_temperature',
                        'soil_temperature_0_to_7cm',
                        'soil_temperature_7_to_28cm',
                        'soil_temperature_28_to_100cm',
                        'soil_temperature_100_to_255cm',
                        'soil_moisture_0_to_7cm',
                        'soil_moisture_28_to_100cm',
                        'soil_moisture_7_to_28cm',
                        'soil_moisture_100_to_255cm',
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
                        'vertical_velocity_1000hPa',
                        'vertical_velocity_925hPa',
                        'vertical_velocity_850hPa',
                        'vertical_velocity_700hPa',
                        'vertical_velocity_600hPa',
                        'vertical_velocity_500hPa',
                        'vertical_velocity_400hPa',
                        'vertical_velocity_300hPa',
                        'vertical_velocity_250hPa',
                        'vertical_velocity_200hPa',
                        'vertical_velocity_150hPa',
                        'vertical_velocity_100hPa',
                        'vertical_velocity_50hPa',
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
                        'geopotential_height_50hPa'],
            proxies=None):
    
    """
    This function retrieves ECMWF AIFS time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
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
                                            'showers',
                                            'snowfall',
                                            'runoff',
                                            'visibility',
                                            'weather_code',
                                            'pressure_msl',
                                            'surface_pressure',
                                            'cloud_cover',
                                            'cloud_cover_low',
                                            'cloud_cover_mid',
                                            'cloud_cover_high',
                                            'sunshine_duration',
                                            'potential_evapotranspiration',
                                            'et0_fao_evapotranspiration',
                                            'wind_speed_10m',
                                            'wind_speed_100m',
                                            'wind_speed_200m',
                                            'wind_direction_10m',
                                            'wind_direction_100m',
                                            'wind_direction_200m',
                                            'wind_gusts_10m',
                                            'cape',
                                            'convective_inhibition',
                                            'total_column_integrated_water_vapour',
                                            'vapour_pressure_deficit',
                                            'surface_temperature',
                                            'soil_temperature_0_to_7cm',
                                            'soil_temperature_7_to_28cm',
                                            'soil_temperature_28_to_100cm',
                                            'soil_temperature_100_to_255cm',
                                            'soil_moisture_0_to_7cm',
                                            'soil_moisture_28_to_100cm',
                                            'soil_moisture_7_to_28cm',
                                            'soil_moisture_100_to_255cm',
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
                                            'vertical_velocity_1000hPa',
                                            'vertical_velocity_925hPa',
                                            'vertical_velocity_850hPa',
                                            'vertical_velocity_700hPa',
                                            'vertical_velocity_600hPa',
                                            'vertical_velocity_500hPa',
                                            'vertical_velocity_400hPa',
                                            'vertical_velocity_300hPa',
                                            'vertical_velocity_250hPa',
                                            'vertical_velocity_200hPa',
                                            'vertical_velocity_150hPa',
                                            'vertical_velocity_100hPa',
                                            'vertical_velocity_50hPa',
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
                                            'geopotential_height_50hPa']
                                            
                The list of variables to choose from.
                
    6) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
                    
    Returns
    -------
    
    A Pandas.DataFrame of the ECMWF AIFS time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 14:
        print(f"The maximum number of days that can be retrieved is 14. Setting 'days' to 14.")
        days = 14
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ecmwf_aifs025_single"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
        
    else:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ecmwf_aifs025_single"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}",
                             proxies=proxies)
        
    _server_response(response)
        
    data = response.json()
    
    df = _json_to_pandas(data)
    
    return df

def ifs_hres_point_forecast(latitude,
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
                        'showers',
                        'snowfall',
                        'runoff',
                        'visibility',
                        'weather_code',
                        'pressure_msl',
                        'surface_pressure',
                        'cloud_cover',
                        'cloud_cover_low',
                        'cloud_cover_mid',
                        'cloud_cover_high',
                        'sunshine_duration',
                        'potential_evapotranspiration',
                        'et0_fao_evapotranspiration',
                        'wind_speed_10m',
                        'wind_speed_100m',
                        'wind_speed_200m',
                        'wind_direction_10m',
                        'wind_direction_100m',
                        'wind_direction_200m',
                        'wind_gusts_10m',
                        'cape',
                        'convective_inhibition',
                        'total_column_integrated_water_vapour',
                        'vapour_pressure_deficit',
                        'surface_temperature',
                        'soil_temperature_0_to_7cm',
                        'soil_temperature_7_to_28cm',
                        'soil_temperature_28_to_100cm',
                        'soil_temperature_100_to_255cm',
                        'soil_moisture_0_to_7cm',
                        'soil_moisture_28_to_100cm',
                        'soil_moisture_7_to_28cm',
                        'soil_moisture_100_to_255cm',
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
                        'vertical_velocity_1000hPa',
                        'vertical_velocity_925hPa',
                        'vertical_velocity_850hPa',
                        'vertical_velocity_700hPa',
                        'vertical_velocity_600hPa',
                        'vertical_velocity_500hPa',
                        'vertical_velocity_400hPa',
                        'vertical_velocity_300hPa',
                        'vertical_velocity_250hPa',
                        'vertical_velocity_200hPa',
                        'vertical_velocity_150hPa',
                        'vertical_velocity_100hPa',
                        'vertical_velocity_50hPa',
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
                        'geopotential_height_50hPa'],
            proxies=None):
    
    """
    This function retrieves ECMWF IFS Medium-range Control forecast time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
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
                                            'showers',
                                            'snowfall',
                                            'runoff',
                                            'visibility',
                                            'weather_code',
                                            'pressure_msl',
                                            'surface_pressure',
                                            'cloud_cover',
                                            'cloud_cover_low',
                                            'cloud_cover_mid',
                                            'cloud_cover_high',
                                            'sunshine_duration',
                                            'potential_evapotranspiration',
                                            'et0_fao_evapotranspiration',
                                            'wind_speed_10m',
                                            'wind_speed_100m',
                                            'wind_speed_200m',
                                            'wind_direction_10m',
                                            'wind_direction_100m',
                                            'wind_direction_200m',
                                            'wind_gusts_10m',
                                            'cape',
                                            'convective_inhibition',
                                            'total_column_integrated_water_vapour',
                                            'vapour_pressure_deficit',
                                            'surface_temperature',
                                            'soil_temperature_0_to_7cm',
                                            'soil_temperature_7_to_28cm',
                                            'soil_temperature_28_to_100cm',
                                            'soil_temperature_100_to_255cm',
                                            'soil_moisture_0_to_7cm',
                                            'soil_moisture_28_to_100cm',
                                            'soil_moisture_7_to_28cm',
                                            'soil_moisture_100_to_255cm',
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
                                            'vertical_velocity_1000hPa',
                                            'vertical_velocity_925hPa',
                                            'vertical_velocity_850hPa',
                                            'vertical_velocity_700hPa',
                                            'vertical_velocity_600hPa',
                                            'vertical_velocity_500hPa',
                                            'vertical_velocity_400hPa',
                                            'vertical_velocity_300hPa',
                                            'vertical_velocity_250hPa',
                                            'vertical_velocity_200hPa',
                                            'vertical_velocity_150hPa',
                                            'vertical_velocity_100hPa',
                                            'vertical_velocity_50hPa',
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
                                            'geopotential_height_50hPa']
                                            
                The list of variables to choose from.
                
    6) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
                    
    Returns
    -------
    
    A Pandas.DataFrame of the ECMWF IFS Medium-range Control forecast time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 14:
        print(f"The maximum number of days that can be retrieved is 14. Setting 'days' to 14.")
        days = 14
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ecmwf_ifs025"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
        
    else:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ecmwf_ifs025"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}",
                             proxies=proxies)
        
    _server_response(response)
        
    data = response.json()
    
    df = _json_to_pandas(data)
    
    return df