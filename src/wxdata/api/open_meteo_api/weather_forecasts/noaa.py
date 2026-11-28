"""
This file hosts the interface for the Open-Meteo API for NOAA data.

(C) Eric J. Drewitz 2025-2026
"""
import requests as _requests
import pandas as _pd
from wxdata.utils.api import(
    json_to_pandas as _json_to_pandas,
    server_response as _server_response,
    df_to_csv as _df_to_csv
)

def gfs_hourly_point_forecast(latitude,
            longitude,
            days=7,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m',
                        'relative_humidity_2m',
                        'dew_point_2m',
                        'apparent_temperature',
                        'cape',
                        'precipitation',
                        'rain',
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
                        'weather_code',
                        'showers',
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
                        'cloud_cover_10hPa',
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
                        'vertical_velocity_30hPa',
                        'vertical_velocity_20hPa',
                        'vertical_velocity_10hPa'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/NOAA/GFS",
            filename=f"GFS_Data.csv"):
    
    """
    This function retrieves GFS time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
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
                                            'cape',
                                            'precipitation',
                                            'rain',
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
                                            'weather_code',
                                            'showers',
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
                                            'cloud_cover_10hPa',
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
                                            'vertical_velocity_30hPa',
                                            'vertical_velocity_20hPa',
                                            'vertical_velocity_10hPa']
                                            
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
    
    A Pandas.DataFrame of the GFS time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 16:
        print(f"The maximum number of days that can be retrieved is 16. Setting 'days' to 16.")
        days = 16
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=gfs_seamless"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
        
    else:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=gfs_seamless"
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


def aigfs_hourly_point_forecast(latitude,
            longitude,
            days=7,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m',
                        'cloud_cover',
                        'cloud_cover_low',
                        'cloud_cover_mid',
                        'cloud_cover_high',
                        'precipitation',
                        'pressure_msl',
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
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/NOAA/AIGFS",
            filename=f"AIGFS_Data.csv"):
    
    """
    This function retrieves AI GFS time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
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
                                            'cloud_cover',
                                            'cloud_cover_low',
                                            'cloud_cover_mid',
                                            'cloud_cover_high',
                                            'precipitation',
                                            'pressure_msl',
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
    
    7) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}
    
    8) path (String) - The path where the CSV file is saved to.
    
    9) filename (String) - The filename for the CSV file.                      
                    
    Returns
    -------
    
    A Pandas.DataFrame of the AI GFS time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 16:
        print(f"The maximum number of days that can be retrieved is 16. Setting 'days' to 16.")
        days = 16
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_aigfs025"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
    else:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_aigfs025"
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

def hgefs_hourly_point_forecast(latitude,
            longitude,
            days=7,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m',
                        'cloud_cover',
                        'cloud_cover_low',
                        'cloud_cover_mid',
                        'cloud_cover_high',
                        'precipitation',
                        'pressure_msl',
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
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/NOAA/HGEFS",
            filename=f"HGEFS_Data.csv"):
    
    """
    This function retrieves HGEFS time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
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
                                            'cloud_cover',
                                            'cloud_cover_low',
                                            'cloud_cover_mid',
                                            'cloud_cover_high',
                                            'precipitation',
                                            'pressure_msl',
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
    
    7) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}
    
    8) path (String) - The path where the CSV file is saved to.
    
    9) filename (String) - The filename for the CSV file.                      
                    
    Returns
    -------
    
    A Pandas.DataFrame of the HGEFS time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 16:
        print(f"The maximum number of days that can be retrieved is 16. Setting 'days' to 16.")
        days = 16
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_aigfs025"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
                
    else:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_aigfs025"
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

def nbm_hourly_point_forecast(latitude,
            longitude,
            days=7,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m',
                        'cape',
                        'precipitation',
                        'snowfall',
                        'surface_pressure',
                        'visibility',
                        'wind_speed_10m',
                        'wind_speed_80m',
                        'wind_direction_10m',
                        'wind_direction_80m'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/NOAA/NBM",
            filename=f"NBM_Data.csv"):
    
    """
    This function retrieves NBM time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
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
                                            'cape',
                                            'precipitation',
                                            'snowfall',
                                            'surface_pressure',
                                            'visibility',
                                            'wind_speed_10m',
                                            'wind_speed_80m',
                                            'wind_direction_10m',
                                            'wind_direction_80m']
                                            
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
    
    A Pandas.DataFrame of the NBM time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 16:
        print(f"The maximum number of days that can be retrieved is 16. Setting 'days' to 16.")
        days = 16
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_nbm_conus"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
                
    else:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_nbm_conus"
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


def gefs_hourly_point_forecast(latitude,
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
                        'snow_depth',
                        'snowfall',
                        'weather_code',
                        'pressure_msl',
                        'surface_pressure',
                        'cloud_cover',
                        'visibility',
                        'et0_fao_evapotranspiration',
                        'vapour_pressure_deficit',
                        'wind_speed_10m',
                        'wind_speed_80m',
                        'wind_speed_100m',
                        'wind_speed_120m',
                        'wind_direction_10m',
                        'wind_direction_80m',
                        'wind_direction_100m',
                        'wind_direction_120m',
                        'wind_gusts_10m',
                        'temperature_80m',
                        'temperature_120m',
                        'surface_temperature',
                        'soil_temperature_0_to_10cm',
                        'soil_temperature_10_to_40cm',
                        'soil_temperature_40_to_100cm',
                        'soil_temperature_100_to_200cm',
                        'soil_moisture_0_to_10cm',
                        'soil_moisture_10_to_40cm',
                        'soil_moisture_40_to_100cm',
                        'soil_moisture_100_to_200cm',
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
                        'relative_humidity_700hPa',
                        'relative_humidity_850hPa',
                        'relative_humidity_600hPa',
                        'relative_humidity_500hPa',
                        'relative_humidity_400hPa',
                        'relative_humidity_300hPa',
                        'relative_humidity_250hPa',
                        'relative_humidity_200hPa',
                        'relative_humidity_150hPa',
                        'relative_humidity_100hPa',
                        'relative_humidity_50hPa',
                        'dew_point_1000hPa',
                        'dew_point_925hPa',
                        'dew_point_850hPa',
                        'dew_point_700hPa',
                        'dew_point_600hPa',
                        'dew_point_500hPa',
                        'dew_point_400hPa',
                        'dew_point_300hPa',
                        'dew_point_200hPa',
                        'dew_point_250hPa',
                        'dew_point_150hPa',
                        'dew_point_100hPa',
                        'dew_point_50hPa',
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
                        'wind_direction_925hPa',
                        'wind_direction_1000hPa',
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
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/NOAA/GEFS",
            filename=f"GEFS_Data.csv"):
    
    """
    This function retrieves GEFS time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
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
                                            'snow_depth',
                                            'snowfall',
                                            'weather_code',
                                            'pressure_msl',
                                            'surface_pressure',
                                            'cloud_cover',
                                            'visibility',
                                            'et0_fao_evapotranspiration',
                                            'vapour_pressure_deficit',
                                            'wind_speed_10m',
                                            'wind_speed_80m',
                                            'wind_speed_100m',
                                            'wind_speed_120m',
                                            'wind_direction_10m',
                                            'wind_direction_80m',
                                            'wind_direction_100m',
                                            'wind_direction_120m',
                                            'wind_gusts_10m',
                                            'temperature_80m',
                                            'temperature_120m',
                                            'surface_temperature',
                                            'soil_temperature_0_to_10cm',
                                            'soil_temperature_10_to_40cm',
                                            'soil_temperature_40_to_100cm',
                                            'soil_temperature_100_to_200cm',
                                            'soil_moisture_0_to_10cm',
                                            'soil_moisture_10_to_40cm',
                                            'soil_moisture_40_to_100cm',
                                            'soil_moisture_100_to_200cm',
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
                                            'relative_humidity_700hPa',
                                            'relative_humidity_850hPa',
                                            'relative_humidity_600hPa',
                                            'relative_humidity_500hPa',
                                            'relative_humidity_400hPa',
                                            'relative_humidity_300hPa',
                                            'relative_humidity_250hPa',
                                            'relative_humidity_200hPa',
                                            'relative_humidity_150hPa',
                                            'relative_humidity_100hPa',
                                            'relative_humidity_50hPa',
                                            'dew_point_1000hPa',
                                            'dew_point_925hPa',
                                            'dew_point_850hPa',
                                            'dew_point_700hPa',
                                            'dew_point_600hPa',
                                            'dew_point_500hPa',
                                            'dew_point_400hPa',
                                            'dew_point_300hPa',
                                            'dew_point_200hPa',
                                            'dew_point_250hPa',
                                            'dew_point_150hPa',
                                            'dew_point_100hPa',
                                            'dew_point_50hPa',
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
                                            'wind_direction_925hPa',
                                            'wind_direction_1000hPa',
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
    
    7) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}
    
    8) path (String) - The path where the CSV file is saved to.
    
    9) filename (String) - The filename for the CSV file.                      
                    
    Returns
    -------
    
    A Pandas.DataFrame of the GEFS time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 36:
        print(f"The maximum number of days that can be retrieved is 36. Setting 'days' to 36.")
        days = 36
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://ensemble-api.open-meteo.com/v1/ensemble?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_gefs_seamless"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
                
    else:
        response = _requests.get(f"https://ensemble-api.open-meteo.com/v1/ensemble?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_gefs_seamless"
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

def aigefs_hourly_point_forecast(latitude,
            longitude,
            days=7,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m',
                        'precipitation',
                        'rain',
                        'snowfall',
                        'weather_code',
                        'pressure_msl',
                        'surface_pressure',
                        'cloud_cover',
                        'cloud_cover_low',
                        'cloud_cover_mid',
                        'cloud_cover_high',
                        'wind_speed_10m',
                        'wind_direction_10m',
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
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/NOAA/AIGEFS",
            filename=f"AIGEFS_Data.csv"):
    
    """
    This function retrieves AIGEFS time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
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
                                            'precipitation',
                                            'rain',
                                            'snowfall',
                                            'weather_code',
                                            'pressure_msl',
                                            'surface_pressure',
                                            'cloud_cover',
                                            'cloud_cover_low',
                                            'cloud_cover_mid',
                                            'cloud_cover_high',
                                            'wind_speed_10m',
                                            'wind_direction_10m',
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
    
    7) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}
    
    8) path (String) - The path where the CSV file is saved to.
    
    9) filename (String) - The filename for the CSV file.                      
                    
    Returns
    -------
    
    A Pandas.DataFrame of the AIGEFS time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 36:
        print(f"The maximum number of days that can be retrieved is 36. Setting 'days' to 36.")
        days = 36
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://ensemble-api.open-meteo.com/v1/ensemble?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_aigefs025"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
                
    else:
        response = _requests.get(f"https://ensemble-api.open-meteo.com/v1/ensemble?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_aigefs025"
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


def rrfs_north_america_hourly_point_forecast(latitude,
            longitude,
            days=4,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables = [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "dew_point_2m",
                "precipitation_probability",
                "precipitation",
                "wind_speed_10m",
                "wind_direction_10m",
                "wind_gusts_10m",
            ],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/NOAA/RRFS North America",
            filename=f"RRFS_North_America_Data.csv"):
    
    """
    This function retrieves RRFS North America time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) days (Integer) - Default=4. Amount of days to go out for the forecast. Maximum is 4.
    
    2) temperature_units (String) - Default='fahrenheit'. The units for temperature.
    
        ***Valid Temperature Units***
        
        1) fahrenheit
        2) celsius
        
    3) wind_speed_units (String) - Default='mph'. The units for wind speed. 
    
        ***Valid Wind Speed Units***
        
        1) mph - miles per hour
        2) kmh - kilometers per hour
        3) ms - meters per second
        4) kn - knots
        
    4) precipitation_units (String) - Default='inch'. The units for precipitation amounts.
    
        ***Valid Precipitation Units***
        
        1) inch - inches
        2) mm - millimeters
        
    5) variables (String List) -  default = [
                                            "temperature_2m",
                                            "relative_humidity_2m",
                                            "apparent_temperature",
                                            "dew_point_2m",
                                            "precipitation_probability",
                                            "precipitation",
                                            "wind_speed_10m",
                                            "wind_direction_10m",
                                            "wind_gusts_10m",
                                        ],
                                            
        ***Variable List***
        
        "temperature_2m"
        "relative_humidity_2m"
        "apparent_temperature"
        "dew_point_2m"
        "precipitation_probability"
        "precipitation"
        "rain"
        "showers"
        "snowfall"
        "snow_depth"
        "pressure_msl"
        "surface_pressure"
        "cloud_cover"
        "cloud_cover_low"
        "cloud_cover_mid"
        "cloud_cover_high"
        "visibility"
        "evapotranspiration"
        "vapour_pressure_deficit"
        "et0_fao_evapotranspiration"
        "wind_speed_10m"
        "wind_speed_80m"
        "wind_direction_10m"
        "wind_direction_80m"
        "wind_gusts_10m"
        "temperature_80m"
        "surface_temperature"
        "soil_temperature_0_to_10cm"
        "soil_temperature_10_to_40cm"
        "soil_temperature_40_to_100cm"
        "soil_temperature_100_to_200cm"
        "soil_moisture_0_to_10cm"
        "soil_moisture_10_to_40cm"
        "soil_moisture_40_to_100cm"
        "soil_moisture_100_to_200cm"
        "uv_index"
        "uv_index_clear_sky"
        "wet_bulb_temperature_2m"
        "sunshine_duration"
        "total_column_integrated_water_vapour"
        "thunderstorm_probability"
        "rain_probability"
        "snowfall_probability"
        "freezing_rain_probability"
        "ice_pellets_probability"
        "cape"
        "lifted_index"
        "convective_inhibition"
        "freezing_level_height"
        "boundary_layer_height"
        "mass_density_8m"
        "temperature_1000hPa"
        "temperature_975hPa"
        "temperature_950hPa"
        "temperature_925hPa"
        "temperature_900hPa"
        "temperature_875hPa"
        "temperature_850hPa"
        "temperature_825hPa"
        "temperature_800hPa"
        "temperature_775hPa"
        "temperature_750hPa"
        "temperature_725hPa"
        "temperature_700hPa"
        "temperature_675hPa"
        "temperature_650hPa"
        "temperature_625hPa"
        "temperature_600hPa"
        "temperature_575hPa"
        "temperature_550hPa"
        "temperature_525hPa"
        "temperature_500hPa"
        "temperature_475hPa"
        "temperature_450hPa"
        "temperature_425hPa"
        "temperature_400hPa"
        "temperature_375hPa"
        "temperature_350hPa"
        "temperature_325hPa"
        "temperature_300hPa"
        "temperature_275hPa"
        "temperature_250hPa"
        "temperature_225hPa"
        "temperature_200hPa"
        "temperature_175hPa"
        "temperature_150hPa"
        "temperature_125hPa"
        "temperature_100hPa"
        "temperature_70hPa"
        "temperature_50hPa"
        "temperature_40hPa"
        "temperature_30hPa"
        "temperature_20hPa"
        "temperature_15hPa"
        "temperature_10hPa"
        "dew_point_1000hPa"
        "dew_point_975hPa"
        "dew_point_950hPa"
        "dew_point_925hPa"
        "dew_point_900hPa"
        "dew_point_875hPa"
        "dew_point_850hPa"
        "dew_point_825hPa"
        "dew_point_800hPa"
        "dew_point_775hPa"
        "dew_point_750hPa"
        "dew_point_725hPa"
        "dew_point_700hPa"
        "dew_point_675hPa"
        "dew_point_650hPa"
        "dew_point_625hPa"
        "dew_point_600hPa"
        "dew_point_575hPa"
        "dew_point_550hPa"
        "dew_point_525hPa"
        "dew_point_500hPa"
        "dew_point_475hPa"
        "dew_point_450hPa"
        "dew_point_425hPa"
        "dew_point_400hPa"
        "dew_point_375hPa"
        "dew_point_350hPa"
        "dew_point_325hPa"
        "dew_point_300hPa"
        "dew_point_275hPa"
        "dew_point_250hPa"
        "dew_point_225hPa"
        "dew_point_200hPa"
        "dew_point_175hPa"
        "dew_point_150hPa"
        "dew_point_125hPa"
        "dew_point_100hPa"
        "dew_point_70hPa"
        "dew_point_50hPa"
        "dew_point_40hPa"
        "dew_point_30hPa"
        "dew_point_20hPa"
        "dew_point_15hPa"
        "dew_point_10hPa"
        "relative_humidity_1000hPa"
        "relative_humidity_975hPa"
        "relative_humidity_950hPa"
        "relative_humidity_925hPa"
        "relative_humidity_900hPa"
        "relative_humidity_850hPa"
        "relative_humidity_875hPa"
        "relative_humidity_825hPa"
        "relative_humidity_800hPa"
        "relative_humidity_775hPa"
        "relative_humidity_750hPa"
        "relative_humidity_725hPa"
        "relative_humidity_700hPa"
        "relative_humidity_675hPa"
        "relative_humidity_650hPa"
        "relative_humidity_625hPa"
        "relative_humidity_600hPa"
        "relative_humidity_575hPa"
        "relative_humidity_550hPa"
        "relative_humidity_525hPa"
        "relative_humidity_500hPa"
        "relative_humidity_475hPa"
        "relative_humidity_450hPa"
        "relative_humidity_425hPa"
        "relative_humidity_400hPa"
        "relative_humidity_375hPa"
        "relative_humidity_350hPa"
        "relative_humidity_325hPa"
        "relative_humidity_300hPa"
        "relative_humidity_275hPa"
        "relative_humidity_250hPa"
        "relative_humidity_225hPa"
        "relative_humidity_200hPa"
        "relative_humidity_175hPa"
        "relative_humidity_150hPa"
        "relative_humidity_125hPa"
        "relative_humidity_100hPa"
        "relative_humidity_70hPa"
        "relative_humidity_50hPa"
        "relative_humidity_40hPa"
        "relative_humidity_30hPa"
        "relative_humidity_20hPa"
        "relative_humidity_15hPa"
        "relative_humidity_10hPa"
        "cloud_cover_1000hPa"
        "cloud_cover_975hPa"
        "cloud_cover_950hPa"
        "cloud_cover_925hPa"
        "cloud_cover_900hPa"
        "cloud_cover_875hPa"
        "cloud_cover_850hPa"
        "cloud_cover_825hPa"
        "cloud_cover_800hPa"
        "cloud_cover_775hPa"
        "cloud_cover_750hPa"
        "cloud_cover_725hPa"
        "cloud_cover_700hPa"
        "cloud_cover_675hPa"
        "cloud_cover_650hPa"
        "cloud_cover_625hPa"
        "cloud_cover_600hPa"
        "cloud_cover_575hPa"
        "cloud_cover_550hPa"
        "cloud_cover_525hPa"
        "cloud_cover_500hPa"
        "cloud_cover_475hPa"
        "cloud_cover_450hPa"
        "cloud_cover_425hPa"
        "cloud_cover_400hPa"
        "cloud_cover_375hPa"
        "cloud_cover_350hPa"
        "cloud_cover_325hPa"
        "cloud_cover_300hPa"
        "cloud_cover_275hPa"
        "cloud_cover_250hPa"
        "cloud_cover_225hPa"
        "cloud_cover_200hPa"
        "cloud_cover_175hPa"
        "cloud_cover_150hPa"
        "cloud_cover_125hPa"
        "cloud_cover_100hPa"
        "cloud_cover_70hPa"
        "cloud_cover_50hPa"
        "cloud_cover_40hPa"
        "cloud_cover_30hPa"
        "cloud_cover_20hPa"
        "cloud_cover_15hPa"
        "cloud_cover_10hPa"
        "wind_speed_1000hPa"
        "wind_speed_975hPa"
        "wind_speed_950hPa"
        "wind_speed_925hPa"
        "wind_speed_900hPa"
        "wind_speed_875hPa"
        "wind_speed_850hPa"
        "wind_speed_825hPa"
        "wind_speed_800hPa"
        "wind_speed_775hPa"
        "wind_speed_750hPa"
        "wind_speed_725hPa"
        "wind_speed_700hPa"
        "wind_speed_675hPa"
        "wind_speed_650hPa"
        "wind_speed_625hPa"
        "wind_speed_600hPa"
        "wind_speed_575hPa"
        "wind_speed_550hPa"
        "wind_speed_525hPa"
        "wind_speed_500hPa"
        "wind_speed_475hPa"
        "wind_speed_450hPa"
        "wind_speed_425hPa"
        "wind_speed_400hPa"
        "wind_speed_375hPa"
        "wind_speed_350hPa"
        "wind_speed_325hPa"
        "wind_speed_300hPa"
        "wind_speed_275hPa"
        "wind_speed_250hPa"
        "wind_speed_225hPa"
        "wind_speed_200hPa"
        "wind_speed_175hPa"
        "wind_speed_150hPa"
        "wind_speed_125hPa"
        "wind_speed_100hPa"
        "wind_speed_70hPa"
        "wind_speed_50hPa"
        "wind_speed_40hPa"
        "wind_speed_30hPa"
        "wind_speed_20hPa"
        "wind_speed_15hPa"
        "wind_speed_10hPa"
        "wind_direction_1000hPa"
        "wind_direction_975hPa"
        "wind_direction_950hPa"
        "wind_direction_925hPa"
        "wind_direction_900hPa"
        "wind_direction_850hPa"
        "wind_direction_875hPa"
        "wind_direction_825hPa"
        "wind_direction_800hPa"
        "wind_direction_775hPa"
        "wind_direction_750hPa"
        "wind_direction_725hPa"
        "wind_direction_700hPa"
        "wind_direction_675hPa"
        "wind_direction_650hPa"
        "wind_direction_625hPa"
        "wind_direction_600hPa"
        "wind_direction_575hPa"
        "wind_direction_550hPa"
        "wind_direction_525hPa"
        "wind_direction_500hPa"
        "wind_direction_475hPa"
        "wind_direction_450hPa"
        "wind_direction_425hPa"
        "wind_direction_400hPa"
        "wind_direction_375hPa"
        "wind_direction_350hPa"
        "wind_direction_325hPa"
        "wind_direction_300hPa"
        "wind_direction_275hPa"
        "wind_direction_250hPa"
        "wind_direction_225hPa"
        "wind_direction_200hPa"
        "wind_direction_175hPa"
        "wind_direction_150hPa"
        "wind_direction_125hPa"
        "wind_direction_100hPa"
        "wind_direction_70hPa"
        "wind_direction_50hPa"
        "wind_direction_40hPa"
        "wind_direction_30hPa"
        "wind_direction_20hPa"
        "wind_direction_15hPa"
        "wind_direction_10hPa"
        "vertical_velocity_1000hPa"
        "vertical_velocity_975hPa"
        "vertical_velocity_950hPa"
        "vertical_velocity_925hPa"
        "vertical_velocity_900hPa"
        "vertical_velocity_875hPa"
        "vertical_velocity_850hPa"
        "vertical_velocity_825hPa"
        "vertical_velocity_800hPa"
        "vertical_velocity_775hPa"
        "vertical_velocity_750hPa"
        "vertical_velocity_725hPa"
        "vertical_velocity_700hPa"
        "vertical_velocity_675hPa"
        "vertical_velocity_650hPa"
        "vertical_velocity_625hPa"
        "vertical_velocity_600hPa"
        "vertical_velocity_575hPa"
        "vertical_velocity_550hPa"
        "vertical_velocity_525hPa"
        "vertical_velocity_500hPa"
        "vertical_velocity_475hPa"
        "vertical_velocity_450hPa"
        "vertical_velocity_425hPa"
        "vertical_velocity_400hPa"
        "vertical_velocity_375hPa"
        "vertical_velocity_350hPa"
        "vertical_velocity_325hPa"
        "vertical_velocity_300hPa"
        "vertical_velocity_275hPa"
        "vertical_velocity_250hPa"
        "vertical_velocity_225hPa"
        "vertical_velocity_200hPa"
        "vertical_velocity_175hPa"
        "vertical_velocity_150hPa"
        "vertical_velocity_125hPa"
        "vertical_velocity_100hPa"
        "vertical_velocity_70hPa"
        "vertical_velocity_50hPa"
        "vertical_velocity_40hPa"
        "vertical_velocity_30hPa"
        "vertical_velocity_20hPa"
        "vertical_velocity_15hPa"
        "vertical_velocity_10hPa"
        "geopotential_height_1000hPa"
        "geopotential_height_975hPa"
        "geopotential_height_950hPa"
        "geopotential_height_925hPa"
        "geopotential_height_900hPa"
        "geopotential_height_875hPa"
        "geopotential_height_850hPa"
        "geopotential_height_825hPa"
        "geopotential_height_800hPa"
        "geopotential_height_775hPa"
        "geopotential_height_750hPa"
        "geopotential_height_725hPa"
        "geopotential_height_700hPa"
        "geopotential_height_675hPa"
        "geopotential_height_650hPa"
        "geopotential_height_625hPa"
        "geopotential_height_600hPa"
        "geopotential_height_575hPa"
        "geopotential_height_550hPa"
        "geopotential_height_525hPa"
        "geopotential_height_500hPa"
        "geopotential_height_475hPa"
        "geopotential_height_450hPa"
        "geopotential_height_425hPa"
        "geopotential_height_400hPa"
        "geopotential_height_375hPa"
        "geopotential_height_350hPa"
        "geopotential_height_325hPa"
        "geopotential_height_300hPa"
        "geopotential_height_275hPa"
        "geopotential_height_250hPa"
        "geopotential_height_225hPa"
        "geopotential_height_200hPa"
        "geopotential_height_175hPa"
        "geopotential_height_150hPa"
        "geopotential_height_125hPa"
        "geopotential_height_100hPa"
        "geopotential_height_70hPa"
        "geopotential_height_50hPa"
        "geopotential_height_40hPa"
        "geopotential_height_30hPa"
        "geopotential_height_20hPa"
        "geopotential_height_15hPa"
        "geopotential_height_10hPa"

                
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
    
    A Pandas.DataFrame of the RRFS North America time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 4:
        print(f"The maximum number of days that can be retrieved is 4. Setting 'days' to 4.")
        days = 4
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_rrfs_north_america"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
                
    else:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_rrfs_north_america"
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

def rrfs_conus_hourly_point_forecast(latitude,
            longitude,
            days=4,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables = [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "dew_point_2m",
                "precipitation_probability",
                "precipitation",
                "wind_speed_10m",
                "wind_direction_10m",
                "wind_gusts_10m",
            ],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/NOAA/RRFS CONUS",
            filename=f"RRFS_CONUS_Data.csv"):
    
    """
    This function retrieves RRFS North America time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) days (Integer) - Default=4. Amount of days to go out for the forecast. Maximum is 4.
    
    2) temperature_units (String) - Default='fahrenheit'. The units for temperature.
    
        ***Valid Temperature Units***
        
        1) fahrenheit
        2) celsius
        
    3) wind_speed_units (String) - Default='mph'. The units for wind speed. 
    
        ***Valid Wind Speed Units***
        
        1) mph - miles per hour
        2) kmh - kilometers per hour
        3) ms - meters per second
        4) kn - knots
        
    4) precipitation_units (String) - Default='inch'. The units for precipitation amounts.
    
        ***Valid Precipitation Units***
        
        1) inch - inches
        2) mm - millimeters
        
    5) variables (String List) -  default = [
                                            "temperature_2m",
                                            "relative_humidity_2m",
                                            "apparent_temperature",
                                            "dew_point_2m",
                                            "precipitation_probability",
                                            "precipitation",
                                            "wind_speed_10m",
                                            "wind_direction_10m",
                                            "wind_gusts_10m",
                                        ],
                                            
        ***Variable List***
        
        "temperature_2m"
        "relative_humidity_2m"
        "apparent_temperature"
        "dew_point_2m"
        "precipitation_probability"
        "precipitation"
        "rain"
        "showers"
        "snowfall"
        "snow_depth"
        "pressure_msl"
        "surface_pressure"
        "cloud_cover"
        "cloud_cover_low"
        "cloud_cover_mid"
        "cloud_cover_high"
        "visibility"
        "evapotranspiration"
        "vapour_pressure_deficit"
        "et0_fao_evapotranspiration"
        "wind_speed_10m"
        "wind_speed_80m"
        "wind_direction_10m"
        "wind_direction_80m"
        "wind_gusts_10m"
        "temperature_80m"
        "surface_temperature"
        "soil_temperature_0_to_10cm"
        "soil_temperature_10_to_40cm"
        "soil_temperature_40_to_100cm"
        "soil_temperature_100_to_200cm"
        "soil_moisture_0_to_10cm"
        "soil_moisture_10_to_40cm"
        "soil_moisture_40_to_100cm"
        "soil_moisture_100_to_200cm"
        "uv_index"
        "uv_index_clear_sky"
        "wet_bulb_temperature_2m"
        "sunshine_duration"
        "total_column_integrated_water_vapour"
        "thunderstorm_probability"
        "rain_probability"
        "snowfall_probability"
        "freezing_rain_probability"
        "ice_pellets_probability"
        "cape"
        "lifted_index"
        "convective_inhibition"
        "freezing_level_height"
        "boundary_layer_height"
        "mass_density_8m"
        "temperature_1000hPa"
        "temperature_975hPa"
        "temperature_950hPa"
        "temperature_925hPa"
        "temperature_900hPa"
        "temperature_875hPa"
        "temperature_850hPa"
        "temperature_825hPa"
        "temperature_800hPa"
        "temperature_775hPa"
        "temperature_750hPa"
        "temperature_725hPa"
        "temperature_700hPa"
        "temperature_675hPa"
        "temperature_650hPa"
        "temperature_625hPa"
        "temperature_600hPa"
        "temperature_575hPa"
        "temperature_550hPa"
        "temperature_525hPa"
        "temperature_500hPa"
        "temperature_475hPa"
        "temperature_450hPa"
        "temperature_425hPa"
        "temperature_400hPa"
        "temperature_375hPa"
        "temperature_350hPa"
        "temperature_325hPa"
        "temperature_300hPa"
        "temperature_275hPa"
        "temperature_250hPa"
        "temperature_225hPa"
        "temperature_200hPa"
        "temperature_175hPa"
        "temperature_150hPa"
        "temperature_125hPa"
        "temperature_100hPa"
        "temperature_70hPa"
        "temperature_50hPa"
        "temperature_40hPa"
        "temperature_30hPa"
        "temperature_20hPa"
        "temperature_15hPa"
        "temperature_10hPa"
        "dew_point_1000hPa"
        "dew_point_975hPa"
        "dew_point_950hPa"
        "dew_point_925hPa"
        "dew_point_900hPa"
        "dew_point_875hPa"
        "dew_point_850hPa"
        "dew_point_825hPa"
        "dew_point_800hPa"
        "dew_point_775hPa"
        "dew_point_750hPa"
        "dew_point_725hPa"
        "dew_point_700hPa"
        "dew_point_675hPa"
        "dew_point_650hPa"
        "dew_point_625hPa"
        "dew_point_600hPa"
        "dew_point_575hPa"
        "dew_point_550hPa"
        "dew_point_525hPa"
        "dew_point_500hPa"
        "dew_point_475hPa"
        "dew_point_450hPa"
        "dew_point_425hPa"
        "dew_point_400hPa"
        "dew_point_375hPa"
        "dew_point_350hPa"
        "dew_point_325hPa"
        "dew_point_300hPa"
        "dew_point_275hPa"
        "dew_point_250hPa"
        "dew_point_225hPa"
        "dew_point_200hPa"
        "dew_point_175hPa"
        "dew_point_150hPa"
        "dew_point_125hPa"
        "dew_point_100hPa"
        "dew_point_70hPa"
        "dew_point_50hPa"
        "dew_point_40hPa"
        "dew_point_30hPa"
        "dew_point_20hPa"
        "dew_point_15hPa"
        "dew_point_10hPa"
        "relative_humidity_1000hPa"
        "relative_humidity_975hPa"
        "relative_humidity_950hPa"
        "relative_humidity_925hPa"
        "relative_humidity_900hPa"
        "relative_humidity_850hPa"
        "relative_humidity_875hPa"
        "relative_humidity_825hPa"
        "relative_humidity_800hPa"
        "relative_humidity_775hPa"
        "relative_humidity_750hPa"
        "relative_humidity_725hPa"
        "relative_humidity_700hPa"
        "relative_humidity_675hPa"
        "relative_humidity_650hPa"
        "relative_humidity_625hPa"
        "relative_humidity_600hPa"
        "relative_humidity_575hPa"
        "relative_humidity_550hPa"
        "relative_humidity_525hPa"
        "relative_humidity_500hPa"
        "relative_humidity_475hPa"
        "relative_humidity_450hPa"
        "relative_humidity_425hPa"
        "relative_humidity_400hPa"
        "relative_humidity_375hPa"
        "relative_humidity_350hPa"
        "relative_humidity_325hPa"
        "relative_humidity_300hPa"
        "relative_humidity_275hPa"
        "relative_humidity_250hPa"
        "relative_humidity_225hPa"
        "relative_humidity_200hPa"
        "relative_humidity_175hPa"
        "relative_humidity_150hPa"
        "relative_humidity_125hPa"
        "relative_humidity_100hPa"
        "relative_humidity_70hPa"
        "relative_humidity_50hPa"
        "relative_humidity_40hPa"
        "relative_humidity_30hPa"
        "relative_humidity_20hPa"
        "relative_humidity_15hPa"
        "relative_humidity_10hPa"
        "cloud_cover_1000hPa"
        "cloud_cover_975hPa"
        "cloud_cover_950hPa"
        "cloud_cover_925hPa"
        "cloud_cover_900hPa"
        "cloud_cover_875hPa"
        "cloud_cover_850hPa"
        "cloud_cover_825hPa"
        "cloud_cover_800hPa"
        "cloud_cover_775hPa"
        "cloud_cover_750hPa"
        "cloud_cover_725hPa"
        "cloud_cover_700hPa"
        "cloud_cover_675hPa"
        "cloud_cover_650hPa"
        "cloud_cover_625hPa"
        "cloud_cover_600hPa"
        "cloud_cover_575hPa"
        "cloud_cover_550hPa"
        "cloud_cover_525hPa"
        "cloud_cover_500hPa"
        "cloud_cover_475hPa"
        "cloud_cover_450hPa"
        "cloud_cover_425hPa"
        "cloud_cover_400hPa"
        "cloud_cover_375hPa"
        "cloud_cover_350hPa"
        "cloud_cover_325hPa"
        "cloud_cover_300hPa"
        "cloud_cover_275hPa"
        "cloud_cover_250hPa"
        "cloud_cover_225hPa"
        "cloud_cover_200hPa"
        "cloud_cover_175hPa"
        "cloud_cover_150hPa"
        "cloud_cover_125hPa"
        "cloud_cover_100hPa"
        "cloud_cover_70hPa"
        "cloud_cover_50hPa"
        "cloud_cover_40hPa"
        "cloud_cover_30hPa"
        "cloud_cover_20hPa"
        "cloud_cover_15hPa"
        "cloud_cover_10hPa"
        "wind_speed_1000hPa"
        "wind_speed_975hPa"
        "wind_speed_950hPa"
        "wind_speed_925hPa"
        "wind_speed_900hPa"
        "wind_speed_875hPa"
        "wind_speed_850hPa"
        "wind_speed_825hPa"
        "wind_speed_800hPa"
        "wind_speed_775hPa"
        "wind_speed_750hPa"
        "wind_speed_725hPa"
        "wind_speed_700hPa"
        "wind_speed_675hPa"
        "wind_speed_650hPa"
        "wind_speed_625hPa"
        "wind_speed_600hPa"
        "wind_speed_575hPa"
        "wind_speed_550hPa"
        "wind_speed_525hPa"
        "wind_speed_500hPa"
        "wind_speed_475hPa"
        "wind_speed_450hPa"
        "wind_speed_425hPa"
        "wind_speed_400hPa"
        "wind_speed_375hPa"
        "wind_speed_350hPa"
        "wind_speed_325hPa"
        "wind_speed_300hPa"
        "wind_speed_275hPa"
        "wind_speed_250hPa"
        "wind_speed_225hPa"
        "wind_speed_200hPa"
        "wind_speed_175hPa"
        "wind_speed_150hPa"
        "wind_speed_125hPa"
        "wind_speed_100hPa"
        "wind_speed_70hPa"
        "wind_speed_50hPa"
        "wind_speed_40hPa"
        "wind_speed_30hPa"
        "wind_speed_20hPa"
        "wind_speed_15hPa"
        "wind_speed_10hPa"
        "wind_direction_1000hPa"
        "wind_direction_975hPa"
        "wind_direction_950hPa"
        "wind_direction_925hPa"
        "wind_direction_900hPa"
        "wind_direction_850hPa"
        "wind_direction_875hPa"
        "wind_direction_825hPa"
        "wind_direction_800hPa"
        "wind_direction_775hPa"
        "wind_direction_750hPa"
        "wind_direction_725hPa"
        "wind_direction_700hPa"
        "wind_direction_675hPa"
        "wind_direction_650hPa"
        "wind_direction_625hPa"
        "wind_direction_600hPa"
        "wind_direction_575hPa"
        "wind_direction_550hPa"
        "wind_direction_525hPa"
        "wind_direction_500hPa"
        "wind_direction_475hPa"
        "wind_direction_450hPa"
        "wind_direction_425hPa"
        "wind_direction_400hPa"
        "wind_direction_375hPa"
        "wind_direction_350hPa"
        "wind_direction_325hPa"
        "wind_direction_300hPa"
        "wind_direction_275hPa"
        "wind_direction_250hPa"
        "wind_direction_225hPa"
        "wind_direction_200hPa"
        "wind_direction_175hPa"
        "wind_direction_150hPa"
        "wind_direction_125hPa"
        "wind_direction_100hPa"
        "wind_direction_70hPa"
        "wind_direction_50hPa"
        "wind_direction_40hPa"
        "wind_direction_30hPa"
        "wind_direction_20hPa"
        "wind_direction_15hPa"
        "wind_direction_10hPa"
        "vertical_velocity_1000hPa"
        "vertical_velocity_975hPa"
        "vertical_velocity_950hPa"
        "vertical_velocity_925hPa"
        "vertical_velocity_900hPa"
        "vertical_velocity_875hPa"
        "vertical_velocity_850hPa"
        "vertical_velocity_825hPa"
        "vertical_velocity_800hPa"
        "vertical_velocity_775hPa"
        "vertical_velocity_750hPa"
        "vertical_velocity_725hPa"
        "vertical_velocity_700hPa"
        "vertical_velocity_675hPa"
        "vertical_velocity_650hPa"
        "vertical_velocity_625hPa"
        "vertical_velocity_600hPa"
        "vertical_velocity_575hPa"
        "vertical_velocity_550hPa"
        "vertical_velocity_525hPa"
        "vertical_velocity_500hPa"
        "vertical_velocity_475hPa"
        "vertical_velocity_450hPa"
        "vertical_velocity_425hPa"
        "vertical_velocity_400hPa"
        "vertical_velocity_375hPa"
        "vertical_velocity_350hPa"
        "vertical_velocity_325hPa"
        "vertical_velocity_300hPa"
        "vertical_velocity_275hPa"
        "vertical_velocity_250hPa"
        "vertical_velocity_225hPa"
        "vertical_velocity_200hPa"
        "vertical_velocity_175hPa"
        "vertical_velocity_150hPa"
        "vertical_velocity_125hPa"
        "vertical_velocity_100hPa"
        "vertical_velocity_70hPa"
        "vertical_velocity_50hPa"
        "vertical_velocity_40hPa"
        "vertical_velocity_30hPa"
        "vertical_velocity_20hPa"
        "vertical_velocity_15hPa"
        "vertical_velocity_10hPa"
        "geopotential_height_1000hPa"
        "geopotential_height_975hPa"
        "geopotential_height_950hPa"
        "geopotential_height_925hPa"
        "geopotential_height_900hPa"
        "geopotential_height_875hPa"
        "geopotential_height_850hPa"
        "geopotential_height_825hPa"
        "geopotential_height_800hPa"
        "geopotential_height_775hPa"
        "geopotential_height_750hPa"
        "geopotential_height_725hPa"
        "geopotential_height_700hPa"
        "geopotential_height_675hPa"
        "geopotential_height_650hPa"
        "geopotential_height_625hPa"
        "geopotential_height_600hPa"
        "geopotential_height_575hPa"
        "geopotential_height_550hPa"
        "geopotential_height_525hPa"
        "geopotential_height_500hPa"
        "geopotential_height_475hPa"
        "geopotential_height_450hPa"
        "geopotential_height_425hPa"
        "geopotential_height_400hPa"
        "geopotential_height_375hPa"
        "geopotential_height_350hPa"
        "geopotential_height_325hPa"
        "geopotential_height_300hPa"
        "geopotential_height_275hPa"
        "geopotential_height_250hPa"
        "geopotential_height_225hPa"
        "geopotential_height_200hPa"
        "geopotential_height_175hPa"
        "geopotential_height_150hPa"
        "geopotential_height_125hPa"
        "geopotential_height_100hPa"
        "geopotential_height_70hPa"
        "geopotential_height_50hPa"
        "geopotential_height_40hPa"
        "geopotential_height_30hPa"
        "geopotential_height_20hPa"
        "geopotential_height_15hPa"
        "geopotential_height_10hPa"

                
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
    
    A Pandas.DataFrame of the RRFS CONUS time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 4:
        print(f"The maximum number of days that can be retrieved is 4. Setting 'days' to 4.")
        days = 4
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_rrfs_conus"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
                
    else:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_rrfs_conus"
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

def rrfs_conus_15_minute_point_forecast(latitude,
            longitude,
            days=1,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables = [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "dew_point_2m",
                "precipitation_probability",
                "precipitation",
                "wind_speed_10m",
                "wind_direction_10m",
                "wind_gusts_10m",
            ],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/NOAA/RRFS CONUS 15 Minute",
            filename=f"RRFS_CONUS_15_Minute_Data.csv"):
    
    """
    This function retrieves RRFS CONUS 15 Minute time series forecast from the Open-Meteo API for a given point of latitude/longitude.
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) days (Integer) - Default=1. Amount of days to go out for the forecast. Maximum is 1.
    
    2) temperature_units (String) - Default='fahrenheit'. The units for temperature.
    
        ***Valid Temperature Units***
        
        1) fahrenheit
        2) celsius
        
    3) wind_speed_units (String) - Default='mph'. The units for wind speed. 
    
        ***Valid Wind Speed Units***
        
        1) mph - miles per hour
        2) kmh - kilometers per hour
        3) ms - meters per second
        4) kn - knots
        
    4) precipitation_units (String) - Default='inch'. The units for precipitation amounts.
    
        ***Valid Precipitation Units***
        
        1) inch - inches
        2) mm - millimeters
        
    5) variables (String List) -  default = [
                                            "temperature_2m",
                                            "relative_humidity_2m",
                                            "apparent_temperature",
                                            "dew_point_2m",
                                            "precipitation_probability",
                                            "precipitation",
                                            "wind_speed_10m",
                                            "wind_direction_10m",
                                            "wind_gusts_10m",
                                        ],
                                            
        ***Variable List***
        
        "temperature_2m"
        "relative_humidity_2m"
        "apparent_temperature"
        "dew_point_2m"
        "precipitation_probability"
        "precipitation"
        "rain"
        "showers"
        "snowfall"
        "snow_depth"
        "pressure_msl"
        "surface_pressure"
        "cloud_cover"
        "cloud_cover_low"
        "cloud_cover_mid"
        "cloud_cover_high"
        "visibility"
        "evapotranspiration"
        "vapour_pressure_deficit"
        "et0_fao_evapotranspiration"
        "wind_speed_10m"
        "wind_speed_80m"
        "wind_direction_10m"
        "wind_direction_80m"
        "wind_gusts_10m"
        "temperature_80m"
        "surface_temperature"
        "soil_temperature_0_to_10cm"
        "soil_temperature_10_to_40cm"
        "soil_temperature_40_to_100cm"
        "soil_temperature_100_to_200cm"
        "soil_moisture_0_to_10cm"
        "soil_moisture_10_to_40cm"
        "soil_moisture_40_to_100cm"
        "soil_moisture_100_to_200cm"
        "uv_index"
        "uv_index_clear_sky"
        "wet_bulb_temperature_2m"
        "sunshine_duration"
        "total_column_integrated_water_vapour"
        "thunderstorm_probability"
        "rain_probability"
        "snowfall_probability"
        "freezing_rain_probability"
        "ice_pellets_probability"
        "cape"
        "lifted_index"
        "convective_inhibition"
        "freezing_level_height"
        "boundary_layer_height"
        "mass_density_8m"
        "temperature_1000hPa"
        "temperature_975hPa"
        "temperature_950hPa"
        "temperature_925hPa"
        "temperature_900hPa"
        "temperature_875hPa"
        "temperature_850hPa"
        "temperature_825hPa"
        "temperature_800hPa"
        "temperature_775hPa"
        "temperature_750hPa"
        "temperature_725hPa"
        "temperature_700hPa"
        "temperature_675hPa"
        "temperature_650hPa"
        "temperature_625hPa"
        "temperature_600hPa"
        "temperature_575hPa"
        "temperature_550hPa"
        "temperature_525hPa"
        "temperature_500hPa"
        "temperature_475hPa"
        "temperature_450hPa"
        "temperature_425hPa"
        "temperature_400hPa"
        "temperature_375hPa"
        "temperature_350hPa"
        "temperature_325hPa"
        "temperature_300hPa"
        "temperature_275hPa"
        "temperature_250hPa"
        "temperature_225hPa"
        "temperature_200hPa"
        "temperature_175hPa"
        "temperature_150hPa"
        "temperature_125hPa"
        "temperature_100hPa"
        "temperature_70hPa"
        "temperature_50hPa"
        "temperature_40hPa"
        "temperature_30hPa"
        "temperature_20hPa"
        "temperature_15hPa"
        "temperature_10hPa"
        "dew_point_1000hPa"
        "dew_point_975hPa"
        "dew_point_950hPa"
        "dew_point_925hPa"
        "dew_point_900hPa"
        "dew_point_875hPa"
        "dew_point_850hPa"
        "dew_point_825hPa"
        "dew_point_800hPa"
        "dew_point_775hPa"
        "dew_point_750hPa"
        "dew_point_725hPa"
        "dew_point_700hPa"
        "dew_point_675hPa"
        "dew_point_650hPa"
        "dew_point_625hPa"
        "dew_point_600hPa"
        "dew_point_575hPa"
        "dew_point_550hPa"
        "dew_point_525hPa"
        "dew_point_500hPa"
        "dew_point_475hPa"
        "dew_point_450hPa"
        "dew_point_425hPa"
        "dew_point_400hPa"
        "dew_point_375hPa"
        "dew_point_350hPa"
        "dew_point_325hPa"
        "dew_point_300hPa"
        "dew_point_275hPa"
        "dew_point_250hPa"
        "dew_point_225hPa"
        "dew_point_200hPa"
        "dew_point_175hPa"
        "dew_point_150hPa"
        "dew_point_125hPa"
        "dew_point_100hPa"
        "dew_point_70hPa"
        "dew_point_50hPa"
        "dew_point_40hPa"
        "dew_point_30hPa"
        "dew_point_20hPa"
        "dew_point_15hPa"
        "dew_point_10hPa"
        "relative_humidity_1000hPa"
        "relative_humidity_975hPa"
        "relative_humidity_950hPa"
        "relative_humidity_925hPa"
        "relative_humidity_900hPa"
        "relative_humidity_850hPa"
        "relative_humidity_875hPa"
        "relative_humidity_825hPa"
        "relative_humidity_800hPa"
        "relative_humidity_775hPa"
        "relative_humidity_750hPa"
        "relative_humidity_725hPa"
        "relative_humidity_700hPa"
        "relative_humidity_675hPa"
        "relative_humidity_650hPa"
        "relative_humidity_625hPa"
        "relative_humidity_600hPa"
        "relative_humidity_575hPa"
        "relative_humidity_550hPa"
        "relative_humidity_525hPa"
        "relative_humidity_500hPa"
        "relative_humidity_475hPa"
        "relative_humidity_450hPa"
        "relative_humidity_425hPa"
        "relative_humidity_400hPa"
        "relative_humidity_375hPa"
        "relative_humidity_350hPa"
        "relative_humidity_325hPa"
        "relative_humidity_300hPa"
        "relative_humidity_275hPa"
        "relative_humidity_250hPa"
        "relative_humidity_225hPa"
        "relative_humidity_200hPa"
        "relative_humidity_175hPa"
        "relative_humidity_150hPa"
        "relative_humidity_125hPa"
        "relative_humidity_100hPa"
        "relative_humidity_70hPa"
        "relative_humidity_50hPa"
        "relative_humidity_40hPa"
        "relative_humidity_30hPa"
        "relative_humidity_20hPa"
        "relative_humidity_15hPa"
        "relative_humidity_10hPa"
        "cloud_cover_1000hPa"
        "cloud_cover_975hPa"
        "cloud_cover_950hPa"
        "cloud_cover_925hPa"
        "cloud_cover_900hPa"
        "cloud_cover_875hPa"
        "cloud_cover_850hPa"
        "cloud_cover_825hPa"
        "cloud_cover_800hPa"
        "cloud_cover_775hPa"
        "cloud_cover_750hPa"
        "cloud_cover_725hPa"
        "cloud_cover_700hPa"
        "cloud_cover_675hPa"
        "cloud_cover_650hPa"
        "cloud_cover_625hPa"
        "cloud_cover_600hPa"
        "cloud_cover_575hPa"
        "cloud_cover_550hPa"
        "cloud_cover_525hPa"
        "cloud_cover_500hPa"
        "cloud_cover_475hPa"
        "cloud_cover_450hPa"
        "cloud_cover_425hPa"
        "cloud_cover_400hPa"
        "cloud_cover_375hPa"
        "cloud_cover_350hPa"
        "cloud_cover_325hPa"
        "cloud_cover_300hPa"
        "cloud_cover_275hPa"
        "cloud_cover_250hPa"
        "cloud_cover_225hPa"
        "cloud_cover_200hPa"
        "cloud_cover_175hPa"
        "cloud_cover_150hPa"
        "cloud_cover_125hPa"
        "cloud_cover_100hPa"
        "cloud_cover_70hPa"
        "cloud_cover_50hPa"
        "cloud_cover_40hPa"
        "cloud_cover_30hPa"
        "cloud_cover_20hPa"
        "cloud_cover_15hPa"
        "cloud_cover_10hPa"
        "wind_speed_1000hPa"
        "wind_speed_975hPa"
        "wind_speed_950hPa"
        "wind_speed_925hPa"
        "wind_speed_900hPa"
        "wind_speed_875hPa"
        "wind_speed_850hPa"
        "wind_speed_825hPa"
        "wind_speed_800hPa"
        "wind_speed_775hPa"
        "wind_speed_750hPa"
        "wind_speed_725hPa"
        "wind_speed_700hPa"
        "wind_speed_675hPa"
        "wind_speed_650hPa"
        "wind_speed_625hPa"
        "wind_speed_600hPa"
        "wind_speed_575hPa"
        "wind_speed_550hPa"
        "wind_speed_525hPa"
        "wind_speed_500hPa"
        "wind_speed_475hPa"
        "wind_speed_450hPa"
        "wind_speed_425hPa"
        "wind_speed_400hPa"
        "wind_speed_375hPa"
        "wind_speed_350hPa"
        "wind_speed_325hPa"
        "wind_speed_300hPa"
        "wind_speed_275hPa"
        "wind_speed_250hPa"
        "wind_speed_225hPa"
        "wind_speed_200hPa"
        "wind_speed_175hPa"
        "wind_speed_150hPa"
        "wind_speed_125hPa"
        "wind_speed_100hPa"
        "wind_speed_70hPa"
        "wind_speed_50hPa"
        "wind_speed_40hPa"
        "wind_speed_30hPa"
        "wind_speed_20hPa"
        "wind_speed_15hPa"
        "wind_speed_10hPa"
        "wind_direction_1000hPa"
        "wind_direction_975hPa"
        "wind_direction_950hPa"
        "wind_direction_925hPa"
        "wind_direction_900hPa"
        "wind_direction_850hPa"
        "wind_direction_875hPa"
        "wind_direction_825hPa"
        "wind_direction_800hPa"
        "wind_direction_775hPa"
        "wind_direction_750hPa"
        "wind_direction_725hPa"
        "wind_direction_700hPa"
        "wind_direction_675hPa"
        "wind_direction_650hPa"
        "wind_direction_625hPa"
        "wind_direction_600hPa"
        "wind_direction_575hPa"
        "wind_direction_550hPa"
        "wind_direction_525hPa"
        "wind_direction_500hPa"
        "wind_direction_475hPa"
        "wind_direction_450hPa"
        "wind_direction_425hPa"
        "wind_direction_400hPa"
        "wind_direction_375hPa"
        "wind_direction_350hPa"
        "wind_direction_325hPa"
        "wind_direction_300hPa"
        "wind_direction_275hPa"
        "wind_direction_250hPa"
        "wind_direction_225hPa"
        "wind_direction_200hPa"
        "wind_direction_175hPa"
        "wind_direction_150hPa"
        "wind_direction_125hPa"
        "wind_direction_100hPa"
        "wind_direction_70hPa"
        "wind_direction_50hPa"
        "wind_direction_40hPa"
        "wind_direction_30hPa"
        "wind_direction_20hPa"
        "wind_direction_15hPa"
        "wind_direction_10hPa"
        "vertical_velocity_1000hPa"
        "vertical_velocity_975hPa"
        "vertical_velocity_950hPa"
        "vertical_velocity_925hPa"
        "vertical_velocity_900hPa"
        "vertical_velocity_875hPa"
        "vertical_velocity_850hPa"
        "vertical_velocity_825hPa"
        "vertical_velocity_800hPa"
        "vertical_velocity_775hPa"
        "vertical_velocity_750hPa"
        "vertical_velocity_725hPa"
        "vertical_velocity_700hPa"
        "vertical_velocity_675hPa"
        "vertical_velocity_650hPa"
        "vertical_velocity_625hPa"
        "vertical_velocity_600hPa"
        "vertical_velocity_575hPa"
        "vertical_velocity_550hPa"
        "vertical_velocity_525hPa"
        "vertical_velocity_500hPa"
        "vertical_velocity_475hPa"
        "vertical_velocity_450hPa"
        "vertical_velocity_425hPa"
        "vertical_velocity_400hPa"
        "vertical_velocity_375hPa"
        "vertical_velocity_350hPa"
        "vertical_velocity_325hPa"
        "vertical_velocity_300hPa"
        "vertical_velocity_275hPa"
        "vertical_velocity_250hPa"
        "vertical_velocity_225hPa"
        "vertical_velocity_200hPa"
        "vertical_velocity_175hPa"
        "vertical_velocity_150hPa"
        "vertical_velocity_125hPa"
        "vertical_velocity_100hPa"
        "vertical_velocity_70hPa"
        "vertical_velocity_50hPa"
        "vertical_velocity_40hPa"
        "vertical_velocity_30hPa"
        "vertical_velocity_20hPa"
        "vertical_velocity_15hPa"
        "vertical_velocity_10hPa"
        "geopotential_height_1000hPa"
        "geopotential_height_975hPa"
        "geopotential_height_950hPa"
        "geopotential_height_925hPa"
        "geopotential_height_900hPa"
        "geopotential_height_875hPa"
        "geopotential_height_850hPa"
        "geopotential_height_825hPa"
        "geopotential_height_800hPa"
        "geopotential_height_775hPa"
        "geopotential_height_750hPa"
        "geopotential_height_725hPa"
        "geopotential_height_700hPa"
        "geopotential_height_675hPa"
        "geopotential_height_650hPa"
        "geopotential_height_625hPa"
        "geopotential_height_600hPa"
        "geopotential_height_575hPa"
        "geopotential_height_550hPa"
        "geopotential_height_525hPa"
        "geopotential_height_500hPa"
        "geopotential_height_475hPa"
        "geopotential_height_450hPa"
        "geopotential_height_425hPa"
        "geopotential_height_400hPa"
        "geopotential_height_375hPa"
        "geopotential_height_350hPa"
        "geopotential_height_325hPa"
        "geopotential_height_300hPa"
        "geopotential_height_275hPa"
        "geopotential_height_250hPa"
        "geopotential_height_225hPa"
        "geopotential_height_200hPa"
        "geopotential_height_175hPa"
        "geopotential_height_150hPa"
        "geopotential_height_125hPa"
        "geopotential_height_100hPa"
        "geopotential_height_70hPa"
        "geopotential_height_50hPa"
        "geopotential_height_40hPa"
        "geopotential_height_30hPa"
        "geopotential_height_20hPa"
        "geopotential_height_15hPa"
        "geopotential_height_10hPa"

                
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
    
    A Pandas.DataFrame of the RRFS CONUS 15 Minute time series forecast for a given point of latitude/longitude. 
    """
    
    if days > 1:
        print(f"The maximum number of days that can be retrieved is 1. Setting 'days' to 1.")
        days = 1
    else:
        pass
    
    if proxies == None:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_rrfs_conus_15min"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
                
    else:
        response = _requests.get(f"https://api.open-meteo.com/v1/forecast?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models=ncep_rrfs_conus_15min"
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
    
    