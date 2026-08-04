---
title: Open-Meteo API MPI_ESM1_2_XR Climate Reanalysis & Forecasts
---
[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)
# Open-Meteo API MPI_ESM1_2_XR Climate Reanalysis & Forecasts

```python
def mpi_esm1_2_xr(latitude,
            longitude,
            start_date='1950-01-01',
            end_date='2050-12-31',
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m_max',
                        'temperature_2m_mean',
                        'temperature_2m_min',
                        'wind_speed_10m_mean',
                        'wind_speed_10m_max',
                        'cloud_cover_mean',
                        'shortwave_radiation_sum',
                        'relative_humidity_2m_mean',
                        'dew_point_2m_mean',
                        'precipitation_sum',
                        'rain_sum',
                        'snowfall_sum',
                        'pressure_msl_mean'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/Climate/MPI_ESM1_2_XR",
            filename=f"MPI_ESM1_2_XR.csv"):
```

This function retrieves daily MPI_ESM1_2_XR climate data from the Open-Meteo API for a given point of latitude/longitude.

Required Arguments:

1) latitude (Float or Integer) - Latitude in decimal degrees.

2) longitude (Float or Integer) - Longitude in decimal degrees.

Optional Arguments:

1) start_date (String) - Default='1950-01-01'. Start date in the format of 'YYYY-mm-dd'. Record begins at 1950-01-01.

2) end_date (String) - Default='2050-12-31'. End date in the format of 'YYYY-mm-dd'. Record ends at 2050-12-31.

3) temperature_units (String) - Default='fahrenheit'. The units for temperature.

        Valid Temperature Units
        -----------------------
        
        1) fahrenheit
        2) celsius
    
4) wind_speed_units (String) - Default='mph'. The units for wind speed. 

        Valid Wind Speed Units
        ----------------------
        
        1) mph - miles per hour
        2) kmh - kilometers per hour
        3) ms - meters per second
        4) kn - knots
    
5) precipitation_units (String) - Default='inch'. The units for precipitation amounts.

        Valid Precipitation Units
        -------------------------
        
        1) inch - inches
        2) mm - millimeters
    
6) variables (String List) - Default=['temperature_2m_max',
                                        'temperature_2m_mean',
                                        'temperature_2m_min',
                                        'wind_speed_10m_mean',
                                        'wind_speed_10m_max',
                                        'cloud_cover_mean',
                                        'shortwave_radiation_sum',
                                        'relative_humidity_2m_mean',
                                        'dew_point_2m_mean',
                                        'precipitation_sum',
                                        'rain_sum',
                                        'snowfall_sum',
                                        'pressure_msl_mean']

7) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:
  ```python
    proxies=None ---> proxies={
                           'http':'http://your-proxy-address:port',
                           'https':'http://your-proxy-address:port'
                           }
  ```
8) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}

9) path (String) - The path where the CSV file is saved to.

10) filename (String) - The filename for the CSV file.                     
                
**Returns**

A `Pandas.DataFrame` of the MPI_ESM1_2_XR time series for point latitude/longitude. 
