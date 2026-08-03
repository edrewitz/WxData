---
title: Open-Meteo API Air Quality Forecasts
---
[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)
# Open-Meteo API Air Quality Forecasts

```python
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
```

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

3) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:
  ```python
    proxies=None ---> proxies={
                           'http':'http://your-proxy-address:port',
                           'https':'http://your-proxy-address:port'
                           }
  ```
4) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}

5) path (String) - The path where the CSV file is saved to.

6) filename (String) - The filename for the CSV file.                     
                
**Returns**

A `Pandas.DataFrame` of the CAMS Air Quality forecast for a given point of latitude/longitude. 
