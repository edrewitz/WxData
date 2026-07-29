"""
This file hosts the ECMWF EC46 & SEAS5 Seasonal Forecasts at Weekly intervals from Open-Meteo API.

(C) Eric J. Drewitz 2025-2026
"""
import requests as _requests
import pandas as _pd
from wxdata.utils.api import(
    json_to_pandas as _json_to_pandas,
    server_response as _server_response,
    df_to_csv as _df_to_csv
)

def ec46_mean_anomaly(latitude,
            longitude,
            days=46,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m_mean',
                        'temperature_2m_anomaly',
                        'temperature_max6h_2m_mean',
                        'temperature_max6h_2m_anomaly',
                        'temperature_min6h_2m_mean',
                        'temperature_min6h_2m_anomaly',
                        'dew_point_2m_mean',
                        'dew_point_2m_anomaly',
                        'soil_temperature_0_to_7cm_mean',
                        'soil_temperature_0_to_7cm_anomaly',
                        'precipitation_mean',
                        'precipitation_anomaly',
                        'snowfall_mean',
                        'snowfall_anomaly',
                        'snow_depth_mean',
                        'snow_depth_anomaly',
                        'pressure_msl_mean',
                        'pressure_msl_anomaly',
                        'sea_surface_temperature_mean',
                        'sea_surface_temperature_anomaly',
                        'sunshine_duration_mean',
                        'sunshine_duration_anomaly',
                        'cloud_cover_mean',
                        'cloud_cover_anomaly',
                        'wind_speed_10m_mean',
                        'wind_speed_10m_anomaly',
                        'wind_speed_100m_mean',
                        'wind_speed_100m_anomaly',
                        'wind_direction_10m_mean',
                        'wind_direction_10m_anomaly',
                        'wind_direction_100m_mean',
                        'wind_direction_100m_anomaly',
                        'snow_density_mean',
                        'snow_density_anomaly',
                        'snow_depth_water_equivalent_mean',
                        'snow_depth_water_equivalent_anomaly',
                        'snowfall_water_equivalent_mean',
                        'snowfall_water_equivalent_anomaly',
                        'total_column_integrated_water_vapour_mean',
                        'total_column_integrated_water_vapour_anomaly',
                        'temperature_2m_efi',
                        'temperature_2m_sot10',
                        'temperature_2m_sot90',
                        'temperature_2m_anomaly_gt0',
                        'temperature_2m_anomaly_gt1',
                        'temperature_2m_anomaly_gt2',
                        'temperature_2m_anomaly_ltm1',
                        'temperature_2m_anomaly_ltm2',
                        'precipitation_efi',
                        'precipitation_sot90',
                        'precipitation_anomaly_gt0',
                        'precipitation_anomaly_gt10',
                        'precipitation_anomaly_gt20',
                        'pressure_msl_anomaly_gt0',
                        'surface_temperature_anomaly_gt0'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/ECMWF/EC46/Weekly",
            filename=f"EC46_Forecast_Weekly.csv"):
    
    """
    This function retrieves ECMWF EC46 Seasonal Forecast time series at weekly interval from the Open-Meteo API for a given point of latitude/longitude.
    
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
        
    5) variables (String List) - Default=['temperature_2m_mean',
                                            'temperature_2m_anomaly',
                                            'temperature_max6h_2m_mean',
                                            'temperature_max6h_2m_anomaly',
                                            'temperature_min6h_2m_mean',
                                            'temperature_min6h_2m_anomaly',
                                            'dew_point_2m_mean',
                                            'dew_point_2m_anomaly',
                                            'soil_temperature_0_to_7cm_mean',
                                            'soil_temperature_0_to_7cm_anomaly',
                                            'precipitation_mean',
                                            'precipitation_anomaly',
                                            'snowfall_mean',
                                            'snowfall_anomaly',
                                            'snow_depth_mean',
                                            'snow_depth_anomaly',
                                            'pressure_msl_mean',
                                            'pressure_msl_anomaly',
                                            'sea_surface_temperature_mean',
                                            'sea_surface_temperature_anomaly',
                                            'sunshine_duration_mean',
                                            'sunshine_duration_anomaly',
                                            'cloud_cover_mean',
                                            'cloud_cover_anomaly',
                                            'wind_speed_10m_mean',
                                            'wind_speed_10m_anomaly',
                                            'wind_speed_100m_mean',
                                            'wind_speed_100m_anomaly',
                                            'wind_direction_10m_mean',
                                            'wind_direction_10m_anomaly',
                                            'wind_direction_100m_mean',
                                            'wind_direction_100m_anomaly',
                                            'snow_density_mean',
                                            'snow_density_anomaly',
                                            'snow_depth_water_equivalent_mean',
                                            'snow_depth_water_equivalent_anomaly',
                                            'snowfall_water_equivalent_mean',
                                            'snowfall_water_equivalent_anomaly',
                                            'total_column_integrated_water_vapour_mean',
                                            'total_column_integrated_water_vapour_anomaly',
                                            'temperature_2m_efi',
                                            'temperature_2m_sot10',
                                            'temperature_2m_sot90',
                                            'temperature_2m_anomaly_gt0',
                                            'temperature_2m_anomaly_gt1',
                                            'temperature_2m_anomaly_gt2',
                                            'temperature_2m_anomaly_ltm1',
                                            'temperature_2m_anomaly_ltm2',
                                            'precipitation_efi',
                                            'precipitation_sot90',
                                            'precipitation_anomaly_gt0',
                                            'precipitation_anomaly_gt10',
                                            'precipitation_anomaly_gt20',
                                            'pressure_msl_anomaly_gt0',
                                            'surface_temperature_anomaly_gt0']


                                            
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
                             f"&weekly={','.join(variables)}&models=ecmwf_ec46"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
        
    else:
        response = _requests.get(f"https://seasonal-api.open-meteo.com/v1/seasonal?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&weekly={','.join(variables)}&ecmwf_ec46"
                             f"&forecast_days={days}&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}",
                             proxies=proxies)
        
    _server_response(response)
        
    data = response.json()
    
    df = _json_to_pandas(data,
                         field='weekly')
    
    df['time'] = _pd.to_datetime(df['time'])
    
    df = df.dropna()
    
    if to_csv == True:
        _df_to_csv(df,
                   path,
                   filename)
    
    return df