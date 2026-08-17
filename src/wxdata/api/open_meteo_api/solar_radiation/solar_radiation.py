"""
This file hosts solar radiation forecast data client interface with Open-Meteo API.

(C) Eric J. Drewitz 2025-2026
"""
import requests as _requests
import pandas as _pd
import numpy as _np
from wxdata.utils.api import(
    json_to_pandas as _json_to_pandas,
    server_response as _server_response,
    df_to_csv as _df_to_csv
)
from wxdata.api.open_meteo_api.solar_radiation.models import model_selection as _model_selection

def solar_radiation_forecast(latitude,
            longitude,
            model='automatic selection',
            variables=['shortwave_radiation',
                        'direct_radiation',
                        'diffuse_radiation',
                        'direct_normal_irradiance',
                        'shortwave_radiation_clear_sky',
                        'global_tilted_irradiance',
                        'terrestrial_radiation',
                        'shortwave_radiation_instant',
                        'direct_radiation_instant',
                        'diffuse_radiation_instant',
                        'direct_normal_irradiance_instant',
                        'shortwave_radiation_clear_sky_instant',
                        'global_tilted_irradiance_instant',
                        'terrestrial_radiation_instant'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/Solar Radiation/Forecasts",
            filename=f"Solar_Radiation_Forecast.csv"):
    
    """
    This function retrieves the solar radiation forecast from the Open-Meteo API for a given point of latitude/longitude using a given model.
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) model (String) - Default='best match'. The model the user wishes to select.
    
        ***IMPORTANT***
        
        1) Some models are regional and thus do not cover the globe resulting in areas outside of the domain to be invalid.
        
        2) Some models do not have the full list of variables.
        
        ***Model Selection***
        
        'automatic selection'
        'best match'
        'dwd eumetsat mtg'
        'eumetsat msg'
        'eumetsat iodc'
        'eumetsat sarah3'
        'jma jaxa eumetsat mtg'
        'ecmwf ifs hres 9km'
        'ecmwf ifs 0.25'
        'ecmwf aifs 0.25 single'
        'cma grapes global'
        'bom access global'
        'dwd icon seamless'
        'dwd icon global'
        'dwd icon eu'
        'dwd icon d2'
        'met norway nordic seamless (with ecmwf)'
        'met norway nordic'
        'geosphere seamless (with ecmwf)'
        'geosphere arome austria'
        'ncep gfs seamless'
        'ncep gfs global 0.11/0.25'
        'ncep hrrr us conus'
        'ncep nbm us conus'
        'ncep aigfs 0.25'
        'ncep hgefs 0.25 ensemble mean'
        'gem seamless'
        'gem global'
        'gem regional'
        'gem hrdps continental'
        'gem hrdps west'
        'knmi seamless (with ecmwf)'
        'knmi harmonie arome europe'
        'knmi harmonie arome netherlands'
        'dmi seamless (with ecmwf)'
        'dmi harmonie arome europe'
        'chmi aladin seamless'
        'chmi aladin central europe 2km'
        'chmi aladin cz 1km'
        'jma seamless'
        'jma msm'
        'jma_gsm'
        'meteo-france seamless'
        'meteo-france arpege world'
        'meteo-france arpege europe'
        'meteo-france arome france'
        'meteo-france arome france hd'
        'uk met office seamless'
        'uk met office global 10km'
        'uk met office uk 2km'
        'era-5 seamless'
        'era-5'
        'era-5 land'
        'era-5 ensemble'
        'cerra':'cerra',
        'kma seamless'
        'kma ldps'
        'kma gdps'
        'italianmeteo arpae icon 2i'
        'meteoswiss icon seamless'
        'meteoswiss icon ch1'
        'meteoswiss icon ch2'
        
        
        *Important Distinction*
        
        'automatic selection' - Best Match of Solar Radiation Models for location[lat,lon]
        
        'best match' - Best Match of Weather Models for location[lat,lon]
        
    2) variables (String List) - Default=['shortwave_radiation',
                                        'direct_radiation',
                                        'diffuse_radiation',
                                        'direct_normal_irradiance',
                                        'shortwave_radiation_clear_sky',
                                        'global_tilted_irradiance',
                                        'terrestrial_radiation',
                                        'shortwave_radiation_instant',
                                        'direct_radiation_instant',
                                        'diffuse_radiation_instant',
                                        'direct_normal_irradiance_instant',
                                        'shortwave_radiation_clear_sky_instant',
                                        'global_tilted_irradiance_instant',
                                        'terrestrial_radiation_instant']

                                            
                
        ***Variables By Model***
        
        | ***Model*** | shortwave_radiation | direct_radiation | diffuse_radiation | direct_normal_irradiance | shortwave_radiation_clear_sky | global_tilted_irradiance | terrestrial_radiation | shortwave_radiation_instant | diffuse_radiation_instant | direct_normal_irradiance_instant | direct_normal_irradiance_instant | shortwave_radiation_clear_sky_instant | global_tilted_irradiance_instant | terrestrial_radiation_instant |
        | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
        | Best Match | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | ECMWF IFS HRES 9km | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | ECMWF IFS 0.25° | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | ECMWF AIFS 0.25° Single | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | CMA GRAPES Global | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | BOM ACCESS Global |  |  |  |  |  |  | x |  |  |  |  |  |  | x | 
        | DWD ICON Seamless | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | DWD ICON Global | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | DWD ICON EU | x | x | x | x | x | x | x | x | x | x | x | x | x | x | 
        | DWD ICON D2 | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | MET Norway Nordic Seamless (with ECMWF) | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | MET Norway Nordic | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | GeoSphere Seamless (with ECMWF) | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | GeoSphere AROME Austria |  |  |  |  |  |  | x |  |  |  |  |  |  | x | 
        | NCEP GFS Seamless | x | x | x | x | x | x | x | x | x | x | x | x | x | x | 
        | NCEP GFS Global 0.11°/0.25° | x | x | x | x | x | x | x | x | x | x | x | x | x | x | 
        | NCEP HRRR U.S. Conus | x | x | x | x | x | x | x | x | x | x | x | x | x | x | 
        | NCEP NBM U.S. Conus | x | x | x | x | x | x | x | x | x | x | x | x | x | x | 
        | NCEP AIGFS 0.25° |  |  |  |  |  |  | x |  |  |  |  |  |  | x | 
        | NCEP HGEFS 0.25° Ensemble Mean |  |  |  |  |  |  | x |  |  |  |  |  |  | x | 
        | GEM Seamless | x | x | x | x | x | x | x | x | x | x | x | x | x | x | 
        | GEM Global |  |  |  |  |  |  | x |  |  |  |  |  |  | x | 
        | GEM Regional |  |  |  |  |  |  | x |  |  |  |  |  |  | x | 
        | GEM HRDPS Continental | x | x | x | x | x | x | x | x | x | x | x | x | x | x | 
        | GEM HRDPS West |  |  |  |  |  |  | x |  |  |  |  |  |  | x | 
        | KNMI Seamless (with ECMWF) | x | x | x | x | x | x | x | x | x | x | x | x | x | x | 
        | KNMI Harmonie AROME Europe | x | x | x | x | x | x | x | x | x | x | x | x | x | x | 
        | KNMI Harmonie AROME Netherlands | x | x | x | x | x | x | x | x | x | x | x | x | x | x | 
        | DMI Seamless (with ECMWF) | x | x | x | x | x | x | x | x | x | x | x | x | x | x | 
        | DMI Harmonie AROME Europe | x | x | x | x | x | x | x | x | x | x | x | x | x | x | 
        | CHMI Aladin Seamless |  |  |  |  |  |  | x |  |  |  |  |  |  | x | 
        | CHMI Aladin Central Europe 2km |  |  |  |  |  |  | x |  |  |  |  |  |  | x | 
        | CHMI Aladin CZ 1km |  |  |  |  |  |  | x |  |  |  |  |  |  | x | 
        | JMA Seamless | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | JMA MSM | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | JMA GSM |  |  |  |  |  |  | x |  |  |  |  |  |  | x |
        | Météo-France Seamless | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | Météo-France ARPEGE World | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | Météo-France ARPEGE Europe | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | Météo-France AROME France | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | Météo-France AROME France HD |  |  |  |  |  |  | x |  |  |  |  |  |  | x |
        | UK Met Office Seamless | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | UK Met Office Global 10km | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | UK Met Office UK 2km | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | ERA5-Seamless |  |  |  |  |  |  | x |  |  |  |  |  |  | x |
        | ERA5 |  |  |  |  |  |  | x |  |  |  |  |  |  | x |
        | ERA5-Land |  |  |  |  |  |  | x |  |  |  |  |  |  | x |
        | ERA5-Ensemble |  |  |  |  |  |  | x |  |  |  |  |  |  | x |
        | CERRA |  |  |  |  |  |  | x |  |  |  |  |  |  | x |
        | KMA Seamless |  |  |  |  |  |  | x |  |  |  |  |  |  | x |
        | KMA LDPS |  |  |  |  |  |  | x |  |  |  |  |  |  | x |
        | KMA GDPS |  |  |  |  |  |  | x |  |  |  |  |  |  | x |
        | ItaliaMeteo ARPAE ICON 2I | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | MeteoSwiss ICON Seamless | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | MeteoSwiss ICON CH1 | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | MeteoSwiss ICON CH2 | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | DWD EUMETSAT MTG | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | EUMETSAT MSG | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | EUMETSAT IODC | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
        | EUMETSAT Sarah3 |  |  |  |  |  |  | x |  |  |  |  |  |  | x |
        | JMA JAXA EUMETSAT MTG |  |  |  |  |  |  | x |  |  |  |  |  |  | x |
                
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
    
    A Pandas.DataFrame of the solar radiation forecast for a given point of latitude/longitude using a given model. 
    """
    
    model = _model_selection(model)
    
    if proxies == None:
        response = _requests.get(f"https://satellite-api.open-meteo.com/v1/archive?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models={model}"
                             f"&temporal_resolution=native")
        
        
        
    else:
        response = _requests.get(f"https://satellite-api.open-meteo.com/v1/archive?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&hourly={','.join(variables)}&models={model}"
                             f"&temporal_resolution=native",
                             proxies=proxies)
        
    _server_response(response)
        
    data = response.json()
    
    df = _json_to_pandas(data)
    
    df['time'] = _pd.to_datetime(df['time'])
    
    df = df.replace({None: _np.nan})
    
    df.dropna(how='all', axis=1, inplace=True)
    
    if to_csv == True:
        _df_to_csv(df,
                   path,
                   filename)
    
    return df