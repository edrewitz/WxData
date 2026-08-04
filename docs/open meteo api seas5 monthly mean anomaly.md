---
title: Open-Meteo API ECMWF SEAS5 Monthly Mean & Anomaly
---
[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)
# Open-Meteo API ECMWF SEAS5 Monthly Mean & Anomaly

```python
def seas5_mean_anomaly(latitude,
            longitude,
            days=183,
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m_mean',
                        'temperature_2m_anomaly',
                        'temperature_max24h_2m_anomaly',
                        'temperature_min24h_2m_mean',
                        'temperature_max24h_2m_mean',
                        'dew_point_2m_mean',
                        'precipitation_mean',
                        'showers_mean',
                        'snowfall_mean',
                        'snow_depth_mean',
                        'cloud_cover_mean',
                        'shortwave_radiation_mean',
                        'sunshine_duration_mean',
                        'cloud_cover_low_mean',
                        'temperature_min24h_2m_anomaly',
                        'dew_point_2m_anomaly',
                        'precipitation_anomaly',
                        'showers_anomaly',
                        'snow_depth_anomaly',
                        'snowfall_anomaly',
                        'cloud_cover_anomaly',
                        'cloud_cover_low_anomaly',
                        'sunshine_duration_anomaly',
                        'shortwave_radiation_anomaly',
                        'pressure_msl_mean',
                        'sea_surface_temperature_mean',
                        'wind_speed_10m_mean',
                        'wind_gusts_10m_anomaly',
                        'wind_speed_10m_anomaly',
                        'sea_surface_temperature_anomaly',
                        'pressure_msl_anomaly',
                        'soil_temperature_0_to_7cm_mean',
                        'soil_temperature_0_to_7cm_anomaly',
                        'soil_temperature_7_to_28cm_mean',
                        'soil_temperature_7_to_28cm_anomaly',
                        'soil_temperature_28_to_100cm_mean',
                        'soil_temperature_28_to_100cm_anomaly',
                        'soil_temperature_100_to_255cm_mean',
                        'soil_moisture_0_to_7cm_mean',
                        'soil_moisture_7_to_28cm_mean',
                        'soil_moisture_28_to_100cm_mean',
                        'soil_moisture_100_to_255cm_mean',
                        'soil_temperature_100_to_255cm_anomaly',
                        'soil_moisture_0_to_7cm_anomaly',
                        'soil_moisture_7_to_28cm_anomaly',
                        'soil_moisture_28_to_100cm_anomaly',
                        'soil_moisture_100_to_255cm_anomaly',
                        'runoff_mean',
                        'evapotranspiration_mean',
                        'snow_density_mean',
                        'snow_depth_water_equivalent_mean',
                        'total_column_integrated_water_vapour_mean',
                        'sea_ice_cover_mean',
                        'runoff_anomaly',
                        'snow_density_anomaly',
                        'evapotranspiration_anomaly',
                        'snow_depth_water_equivalent_anomaly',
                        'total_column_integrated_water_vapour_anomaly',
                        'sea_ice_cover_anomaly',
                        'longwave_radiation_mean',
                        'snowfall_water_equivalent_mean',
                        'albedo_mean',
                        'latent_heat_flux_mean',
                        'sensible_heat_flux_mean',
                        'longwave_radiation_anomaly',
                        'snowfall_water_equivalent_anomaly',
                        'albedo_anomaly',
                        'latent_heat_flux_anomaly',
                        'sensible_heat_flux_anomaly'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/ECMWF/SEAS5/Monthly",
            filename=f"SEAS5_Forecast_Monthly.csv"):
```

This function retrieves ECMWF SEAS5 Seasonal Forecast time series at monthly interval from the Open-Meteo API for a given point of latitude/longitude.

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
    
5) variables (String List) - Default=['temperature_2m_mean',
                                    'temperature_2m_anomaly',
                                    'temperature_max24h_2m_anomaly',
                                    'temperature_min24h_2m_mean',
                                    'temperature_max24h_2m_mean',
                                    'dew_point_2m_mean',
                                    'precipitation_mean',
                                    'showers_mean',
                                    'snowfall_mean',
                                    'snow_depth_mean',
                                    'cloud_cover_mean',
                                    'shortwave_radiation_mean',
                                    'sunshine_duration_mean',
                                    'cloud_cover_low_mean',
                                    'temperature_min24h_2m_anomaly',
                                    'dew_point_2m_anomaly',
                                    'precipitation_anomaly',
                                    'showers_anomaly',
                                    'snow_depth_anomaly',
                                    'snowfall_anomaly',
                                    'cloud_cover_anomaly',
                                    'cloud_cover_low_anomaly',
                                    'sunshine_duration_anomaly',
                                    'shortwave_radiation_anomaly',
                                    'pressure_msl_mean',
                                    'sea_surface_temperature_mean',
                                    'wind_speed_10m_mean',
                                    'wind_gusts_10m_anomaly',
                                    'wind_speed_10m_anomaly',
                                    'sea_surface_temperature_anomaly',
                                    'pressure_msl_anomaly',
                                    'soil_temperature_0_to_7cm_mean',
                                    'soil_temperature_0_to_7cm_anomaly',
                                    'soil_temperature_7_to_28cm_mean',
                                    'soil_temperature_7_to_28cm_anomaly',
                                    'soil_temperature_28_to_100cm_mean',
                                    'soil_temperature_28_to_100cm_anomaly',
                                    'soil_temperature_100_to_255cm_mean',
                                    'soil_moisture_0_to_7cm_mean',
                                    'soil_moisture_7_to_28cm_mean',
                                    'soil_moisture_28_to_100cm_mean',
                                    'soil_moisture_100_to_255cm_mean',
                                    'soil_temperature_100_to_255cm_anomaly',
                                    'soil_moisture_0_to_7cm_anomaly',
                                    'soil_moisture_7_to_28cm_anomaly',
                                    'soil_moisture_28_to_100cm_anomaly',
                                    'soil_moisture_100_to_255cm_anomaly',
                                    'runoff_mean',
                                    'evapotranspiration_mean',
                                    'snow_density_mean',
                                    'snow_depth_water_equivalent_mean',
                                    'total_column_integrated_water_vapour_mean',
                                    'sea_ice_cover_mean',
                                    'runoff_anomaly',
                                    'snow_density_anomaly',
                                    'evapotranspiration_anomaly',
                                    'snow_depth_water_equivalent_anomaly',
                                    'total_column_integrated_water_vapour_anomaly',
                                    'sea_ice_cover_anomaly',
                                    'longwave_radiation_mean',
                                    'snowfall_water_equivalent_mean',
                                    'albedo_mean',
                                    'latent_heat_flux_mean',
                                    'sensible_heat_flux_mean',
                                    'longwave_radiation_anomaly',
                                    'snowfall_water_equivalent_anomaly',
                                    'albedo_anomaly',
                                    'latent_heat_flux_anomaly',
                                    'sensible_heat_flux_anomaly']   

            
6) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:
  ```python
    proxies=None ---> proxies={
                           'http':'http://your-proxy-address:port',
                           'https':'http://your-proxy-address:port'
                           }
  ```
7) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}

8) path (String) - The path where the CSV file is saved to.

9) filename (String) - The filename for the CSV file.                     
                
**Returns**

A Pandas.DataFrame of the ECMWF SEAS5 Seasonal Forecast monthly time series forecast for a given point of latitude/longitude. 
