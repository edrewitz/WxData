"""
This file hosts the clients that download and process the following types of data from the USDA/FEMS Database.

1) Observed RAWS station fuels data - Single Station.
2) Observed RAWS station fuels data - Multi Station.
3) Current observed RAWS station fuels data - Multi Station.
4) 7-Day NFDRS Forecast for a RAWS station - Single Station.
5) 7-Day NFDRS Forecast for a group of RAWS stations - Multi Station. 

(C) Eric J. Drewitz 2025-2026
"""

import pandas as _pd
import os as _os
import glob as _glob
import wxdata.client.client as _client

from wxdata.fems.meta_data import(
    get_single_raws_station_meta_data as _get_single_raws_station_meta_data,
    get_multi_raws_station_meta_data as _get_multi_raws_station_meta_data
)

try:
    from datetime import(
        datetime as _datetime, 
        timedelta as _timedelta, 
        UTC as _UTC
    )
except Exception as e:
    from datetime import(
        datetime as _datetime, 
        timedelta as _timedelta
    )
    
try:
    utc_time = _datetime.now(_UTC)
except Exception as e:
    utc_time = _datetime.utcnow()
    
folder = _os.getcwd()
folder_modified = folder.replace("\\", "/")  

def _clear_data(path):
    
    """
    This function clears the directory.
    
    Required Arguments: 
    
    1) path (String) - The path to the directory.
    
    Optional Arguments: None
    
    Returns
    -------
    
    A cleared directory. 
    """
    
    try:
        for file in _os.listdir(f"{path}"):
            _os.remove(f"{path}/{file}")
    except Exception as e:
        pass


def get_single_raws_station_weather_observations(station_id, 
                                        number_of_days=7, 
                                        start_date=None, 
                                        end_date=None, 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Single Station/Observations/Weather',
                                        proxies=None,
                                        clear_data=True):

    """
    This function retrieves the observed weather data for a user-specified single RAWS station for a 
    user-specified period of time. 

    Required Arguments:

    1) station_id (Integer) - The RAWS ID of the station. 

    Optional Arguments:
    
    1) number_of_days (Integer or String) - Default=7. How many days the user wants the summary for (90 for 90 days).
        If the user wants to use a custom date range enter 'Custom' or 'custom' in this field. 

    2) start_date (String) - Default = None. The start date if the user wants to define a custom period. Enter as a string
        in the following format 'YYYY-mm-dd'

    3) end_date (String) - Default = None. The end date if the user wants to define a custom period. Enter as a string
        in the following format 'YYYY-mm-dd'

    4) fuel_model (String) - Default = 'Y'. The fuel model being used. 
        Fuel Models List:

        Y - Timber
        X - Brush
        W - Grass/Shrub
        V - Grass
        Z - Slash
    
    5) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    6) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/Observations'. The directory the data will be saved to. 
        
    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    Returns
    -------
    
    A Pandas DataFrame of observed weather data for a user-specified single RAWS station for a user-specified time.          
    """
    
    if clear_data is True:
        _clear_data(path)
    
    try:
        number_of_days = number_of_days.lower()
    except Exception as e:
        pass
    
    
    fname = f"{station_id} Weather Observations.csv"

    if number_of_days == 'custom':

        df = _client.get_csv_data(f"https://fems.fs2c.usda.gov/api/ext-climatology/download-weather?"
                                  f"stationIds={station_id}&startDate={start_date}Z&endDate={end_date}Z&"
                                  f"dataset=observation&dataFormat=csv&dataIncrement=hourly",
                            path,
                            fname,
                            proxies=proxies,
                            notifications='off',
                            clear_recycle_bin=clear_recycle_bin)
            
    else:

        try:
            now = _datetime.now(_UTC)
        except Exception as e:
            now = _datetime.utcnow()
            
        start = now - _timedelta(days=number_of_days)

        df = _client.get_csv_data(f"https://fems.fs2c.usda.gov/api/ext-climatology/download-weather?"
                                  f"stationIds={station_id}&startDate={start.strftime('%Y-%m-%dT%H:%M:%S')}Z&endDate={now.strftime('%Y-%m-%dT%H:%M:%S')}Z&"
                                  f"dataset=observation&dataFormat=csv&dataIncrement=hourly",
                                path,
                                fname,
                                proxies=proxies,
                                notifications='off',
                                clear_recycle_bin=clear_recycle_bin)
    
    return df

def get_single_raws_station_fuels_observations(station_id, 
                                        number_of_days=7, 
                                        start_date=None, 
                                        end_date=None, 
                                        fuel_model='Y', 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Single Station/Observations/Fuels',
                                        proxies=None,
                                        clear_data=True):

    """
    This function retrieves the observed weather data for a user-specified single RAWS station for a 
    user-specified period of time. 

    Required Arguments:

    1) station_id (Integer) - The RAWS ID of the station. 

    Optional Arguments:
    
    1) number_of_days (Integer or String) - Default=7. How many days the user wants the summary for (90 for 90 days).
        If the user wants to use a custom date range enter 'Custom' or 'custom' in this field. 

    2) start_date (String) - Default = None. The start date if the user wants to define a custom period. Enter as a string
        in the following format 'YYYY-mm-dd'

    3) end_date (String) - Default = None. The end date if the user wants to define a custom period. Enter as a string
        in the following format 'YYYY-mm-dd'

    4) fuel_model (String) - Default = 'Y'. The fuel model being used. 
        Fuel Models List:

        Y - Timber
        X - Brush
        W - Grass/Shrub
        V - Grass
        Z - Slash
    
    5) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    6) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/Observations'. The directory the data will be saved to. 
        
    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    Returns
    -------
    
    A Pandas DataFrame of observed weather data for a user-specified single RAWS station for a user-specified time.          
    """
    
    if clear_data is True:
        _clear_data(path)
    
    try:
        number_of_days = number_of_days.lower()
    except Exception as e:
        pass
    
    fuel_model = fuel_model.upper()
    
    fname = f"{station_id} Fuels Observations Fuel Model {fuel_model}.csv"

    if number_of_days == 'custom':

        df = _client.get_csv_data(f"https://fems.fs2c.usda.gov/api/ext-climatology/download-nfdr?"
                            f"stationIds={str(station_id)}&endDate={end_date}Z&startDate={start_date}Z&"
                            f"dataFormat=csv&dataset=all&fuelModels={fuel_model}&dateTimeFormat=UTC",
                            path,
                            fname,
                            proxies=proxies,
                            notifications='off',
                            clear_recycle_bin=clear_recycle_bin)
            
    else:

        try:
            now = _datetime.now(_UTC)
        except Exception as e:
            now = _datetime.utcnow()
            
        start = now - _timedelta(days=number_of_days)

        df = _client.get_csv_data(f"https://fems.fs2c.usda.gov/api/ext-climatology/download-nfdr?"
                                 f"stationIds={str(station_id)}&endDate={now.strftime(f'%Y-%m-%d')}T{now.strftime(f'%H:%M:%S')}Z&"
                                 f"startDate={start.strftime(f'%Y-%m-%d')}T{start.strftime(f'%H:%M:%S')}Z&"
                                 f"dataFormat=csv&dataset=all&fuelModels={fuel_model}&dateTimeFormat=UTC",
                                path,
                                fname,
                                proxies=proxies,
                                notifications='off',
                                clear_recycle_bin=clear_recycle_bin)
    
    return df

def get_multi_raws_station_weather_observations(station_ids, 
                                        number_of_days=7, 
                                        start_date=None, 
                                        end_date=None, 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Multi Station/Observations/Weather',
                                        proxies=None,
                                        clear_data=True):

    """
    This function retrieves the observed weather data for a user-specified single RAWS station for a 
    user-specified period of time. 

    Required Arguments:

    1) station_id (Integer) - The RAWS ID of the station. 

    Optional Arguments:
    
    1) number_of_days (Integer or String) - Default=7. How many days the user wants the summary for (90 for 90 days).
        If the user wants to use a custom date range enter 'Custom' or 'custom' in this field. 

    2) start_date (String) - Default = None. The start date if the user wants to define a custom period. Enter as a string
        in the following format 'YYYY-mm-dd'

    3) end_date (String) - Default = None. The end date if the user wants to define a custom period. Enter as a string
        in the following format 'YYYY-mm-dd'

    4) fuel_model (String) - Default = 'Y'. The fuel model being used. 
        Fuel Models List:

        Y - Timber
        X - Brush
        W - Grass/Shrub
        V - Grass
        Z - Slash
    
    5) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    6) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/Observations'. The directory the data will be saved to. 
        
    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    Returns
    -------
    
    A Pandas DataFrame of observed weather data for a user-specified single RAWS station for a user-specified time.          
    """
    
    if clear_data is True:
        _clear_data(path)
    
    try:
        number_of_days = number_of_days.lower()
    except Exception as e:
        pass
    
    for station_id in station_ids:
    
        fname = f"{station_id} Weather Observations.csv"

        if number_of_days == 'custom':

            df = _client.get_csv_data(f"https://fems.fs2c.usda.gov/api/ext-climatology/download-weather?"
                                    f"stationIds={station_id}&startDate={start_date}Z&endDate={end_date}Z&"
                                    f"dataset=observation&dataFormat=csv&dataIncrement=hourly",
                                path,
                                fname,
                                proxies=proxies,
                                notifications='off',
                                clear_recycle_bin=clear_recycle_bin)
                
        else:

            try:
                now = _datetime.now(_UTC)
            except Exception as e:
                now = _datetime.utcnow()
                
            start = now - _timedelta(days=number_of_days)

            df = _client.get_csv_data(f"https://fems.fs2c.usda.gov/api/ext-climatology/download-weather?"
                                    f"stationIds={station_id}&startDate={start.strftime('%Y-%m-%dT%H:%M:%S')}Z&endDate={now.strftime('%Y-%m-%dT%H:%M:%S')}Z&"
                                    f"dataset=observation&dataFormat=csv&dataIncrement=hourly",
                                    path,
                                    fname,
                                    proxies=proxies,
                                    notifications='off',
                                    clear_recycle_bin=clear_recycle_bin)
    
    file_list = _glob.glob(f"{path}/*.csv")
            
    df_list = [_pd.read_csv(file) for file in file_list]
    
    df = _pd.concat(df_list, ignore_index=True)
    
    return df

def get_multi_raws_station_fuels_observations(station_ids, 
                                        number_of_days=7, 
                                        start_date=None, 
                                        end_date=None, 
                                        fuel_model='Y', 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Multi Station/Observations/Fuels',
                                        proxies=None,
                                        clear_data=True):

    """
    This function retrieves the observed weather data for a user-specified list of RAWS stations for a 
    user-specified period of time. 

    Required Arguments:

    1) station_ids (Integer List) - An integer list of all the RAWS IDs for each RAWS station the user wants in the dataset.

    Optional Arguments:
    
    1) number_of_days (Integer or String) - Default=7. How many days the user wants the summary for (90 for 90 days).
        If the user wants to use a custom date range enter 'Custom' or 'custom' in this field. 

    2) start_date (String) - Default = None. The start date if the user wants to define a custom period. Enter as a string
        in the following format 'YYYY-mm-dd'

    3) end_date (String) - Default = None. The end date if the user wants to define a custom period. Enter as a string
        in the following format 'YYYY-mm-dd'

    4) fuel_model (String) - Default = 'Y'. The fuel model being used. 
        Fuel Models List:

        Y - Timber
        X - Brush
        W - Grass/Shrub
        V - Grass
        Z - Slash
    
    5) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    6) path (String) - Default=f'{folder_modified}/FEMS Data/Multi Station/Observations'. The directory the data will be saved to.
        
    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    Returns
    -------
    
    A Pandas DataFrame of observed weather data for a user-specified list of RAWS stations for a user-specified time.                     
    """
    
    if clear_data is True:
        _clear_data(path)
    
    try:
        number_of_days = number_of_days.lower()
    except Exception as e:
        pass
    
    fuel_model = fuel_model.upper()
    
    for station_id in station_ids:
    
        fname = f"{station_id} Fuels Observations Fuel Model {fuel_model}.csv"

        if number_of_days == 'custom':

            _client.get_csv_data(f"https://fems.fs2c.usda.gov/api/ext-climatology/download-nfdr?"
                                f"stationIds={str(station_id)}&endDate={end_date}Z&startDate={start_date}Z&"
                                f"dataFormat=csv&dataset=all&fuelModels={fuel_model}&dateTimeFormat=UTC",
                                path,
                                fname,
                                proxies=proxies,
                                notifications='off',
                                clear_recycle_bin=clear_recycle_bin,
                                return_pandas_df=False)
                
        else:

            try:
                now = _datetime.now(_UTC)
            except Exception as e:
                now = _datetime.utcnow()
                
            start = now - _timedelta(days=number_of_days)

            _client.get_csv_data(f"https://fems.fs2c.usda.gov/api/ext-climatology/download-nfdr?"
                                    f"stationIds={str(station_id)}&endDate={now.strftime(f'%Y-%m-%d')}T{now.strftime(f'%H:%M:%S')}Z&"
                                    f"startDate={start.strftime(f'%Y-%m-%d')}T{start.strftime(f'%H:%M:%S')}Z&"
                                    f"dataFormat=csv&dataset=all&fuelModels={fuel_model}&dateTimeFormat=UTC",
                                    path,
                                    fname,
                                    proxies=proxies,
                                    notifications='off',
                                    clear_recycle_bin=clear_recycle_bin,
                                    return_pandas_df=False)
            
    file_list = _glob.glob(f"{path}/*.csv")
            
    df_list = [_pd.read_csv(file) for file in file_list]
    
    df = _pd.concat(df_list, ignore_index=True)
    
    return df

def get_current_multi_raws_station_weather_observations(station_ids, 
                                                clear_recycle_bin=False,
                                                path=f'{folder_modified}/FEMS Data/Current Multi Station/Observations/Weather',
                                                proxies=None,
                                                clear_data=True,
                                                meta_path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                                sheet_name='Sheet1'):

    """
    This function retrieves the observed weather data for a user-specified single RAWS station for a 
    user-specified period of time. 

    Required Arguments:

    1) station_id (Integer) - The RAWS ID of the station. 

    Optional Arguments:
    
    1) number_of_days (Integer or String) - Default=7. How many days the user wants the summary for (90 for 90 days).
        If the user wants to use a custom date range enter 'Custom' or 'custom' in this field. 

    2) start_date (String) - Default = None. The start date if the user wants to define a custom period. Enter as a string
        in the following format 'YYYY-mm-dd'

    3) end_date (String) - Default = None. The end date if the user wants to define a custom period. Enter as a string
        in the following format 'YYYY-mm-dd'

    4) fuel_model (String) - Default = 'Y'. The fuel model being used. 
        Fuel Models List:

        Y - Timber
        X - Brush
        W - Grass/Shrub
        V - Grass
        Z - Slash
    
    5) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    6) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/Observations'. The directory the data will be saved to. 
        
    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    Returns
    -------
    
    A Pandas DataFrame of observed weather data for a user-specified single RAWS station for a user-specified time.          
    """
    number_of_days = 1 
    if clear_data is True:
        _clear_data(path)
    
    for station_id in station_ids:
    
        fname = f"{station_id} Weather Observations.csv"

        try:
            now = _datetime.now(_UTC)
        except Exception as e:
            now = _datetime.utcnow()
            
        start = now - _timedelta(days=number_of_days)

        df = _client.get_csv_data(f"https://fems.fs2c.usda.gov/api/ext-climatology/download-weather?"
                                f"stationIds={station_id}&startDate={start.strftime('%Y-%m-%dT%H:%M:%S')}Z&endDate={now.strftime('%Y-%m-%dT%H:%M:%S')}Z&"
                                f"dataset=observation&dataFormat=csv&dataIncrement=hourly",
                                path,
                                fname,
                                proxies=proxies,
                                notifications='off',
                                clear_recycle_bin=clear_recycle_bin)
    
    file_list = _glob.glob(f"{path}/*.csv")
            
    df_list = [_pd.read_csv(file) for file in file_list]
    
    df = _pd.concat(df_list, ignore_index=True)
    
    keys = df.columns.tolist()
    
    df = df.groupby(keys[0]).tail(1)
    
    meta = _get_multi_raws_station_meta_data(station_ids, 
                                        sheet_name=sheet_name,
                                        clear_recycle_bin=False,
                                        path=meta_path,
                                        proxies=proxies)
    
    meta_keys = meta.columns.tolist()
    
    df = df.sort_values(by=keys[0], ascending=False)
    meta = meta.sort_values(by=meta_keys[6], ascending=False)
    df[meta_keys[9]] = meta[meta_keys[9]].values
    df[meta_keys[10]] = meta[meta_keys[10]].values
    
    return df

def get_current_multi_raws_station_fuels_observations(station_ids, 
                                                fuel_model='Y', 
                                                clear_recycle_bin=False,
                                                path=f'{folder_modified}/FEMS Data/Current Multi Station/Observations/Fuels',
                                                proxies=None,
                                                clear_data=True,
                                                meta_path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                                sheet_name='Sheet1'):

    """
    This function retrieves the latest observed weather data for a user-specified list of RAWS stations. 

    Required Arguments:

    1) station_ids (Integer List) - An integer list of all the RAWS IDs for each RAWS station the user wants in the dataset.

    Optional Arguments:

    1) fuel_model (String) - Default = 'Y'. The fuel model being used. 
        Fuel Models List:

        Y - Timber
        X - Brush
        W - Grass/Shrub
        V - Grass
        Z - Slash
    
    2) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    3) path (String) - Default=f'{folder_modified}/FEMS Data/Current Multi Station/Observations'. The directory the data will be saved to.
        
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }

    Returns
    -------
    
    A Pandas DataFrame of the latest observed weather data for a user-specified list of RAWS stations.                 
    """
    if clear_data is True:
        _clear_data(path)
    
    number_of_days = 1 
    
    fuel_model = fuel_model.upper()
    
    try:
        now = _datetime.now(_UTC)
    except Exception as e:
        now = _datetime.utcnow()
            
    start = now - _timedelta(days=number_of_days)
    
    for station_id in station_ids:
    
        fname = f"{station_id} Fuels Observations Fuel Model {fuel_model}.csv"

        _client.get_csv_data(f"https://fems.fs2c.usda.gov/api/ext-climatology/download-nfdr?"
                                f"stationIds={str(station_id)}&endDate={now.strftime(f'%Y-%m-%d')}T{now.strftime(f'%H:%M:%S')}Z&"
                                f"startDate={start.strftime(f'%Y-%m-%d')}T{start.strftime(f'%H:%M:%S')}Z&"
                                f"dataFormat=csv&dataset=all&fuelModels={fuel_model}&dateTimeFormat=UTC",
                                path,
                                fname,
                                proxies=proxies,
                                notifications='off',
                                clear_recycle_bin=clear_recycle_bin,
                                return_pandas_df=False)
            
    file_list = _glob.glob(f"{path}/*.csv")
            
    df_list = [_pd.read_csv(file) for file in file_list]
    
    df = _pd.concat(df_list, ignore_index=True)
    
    keys = df.columns.tolist()
    
    df = df.groupby(keys[0]).tail(1)
    
    meta = _get_multi_raws_station_meta_data(station_ids, 
                                        sheet_name=sheet_name,
                                        clear_recycle_bin=False,
                                        path=meta_path,
                                        proxies=proxies)
    
    meta_keys = meta.columns.tolist()
    
    df = df.sort_values(by=keys[0], ascending=False)
    meta = meta.sort_values(by=meta_keys[6], ascending=False)
    df[meta_keys[9]] = meta[meta_keys[9]].values
    df[meta_keys[10]] = meta[meta_keys[10]].values
    
    return df

def get_single_raws_station_nfdrs_forecast(station_id, 
                                        fuel_model='Y', 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Single Station/NFDRS Forecasts',
                                        proxies=None,
                                        clear_data=True):

    """
    This function retrieves the 7-Day NFDRS forecast for a user-specified single RAWS station. 

    Required Arguments:

    1) station_id (Integer) - The RAWS ID of the station. 

    Optional Arguments:

    1) fuel_model (String) - Default = 'Y'. The fuel model being used. 
        Fuel Models List:

        Y - Timber
        X - Brush
        W - Grass/Shrub
        V - Grass
        Z - Slash
    
    2) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    3) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/Forecasts'. The directory the data will be saved to. 
        
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    Returns
    -------
    
    A Pandas DataFrame of the 7-Day NFDRS forecast for a user-specified RAWS station.           
    """
    if clear_data is True:
        _clear_data(path)
    
    fuel_model = fuel_model.upper()
    
    fname = f"{station_id} 7 Day Fuels Forecast Fuel Model {fuel_model}.csv"

    try:
        start = _datetime.now(_UTC)
    except Exception as e:
        start = _datetime.utcnow()
        
    end = start + _timedelta(days=7)

    df = _client.get_csv_data(f"https://fems.fs2c.usda.gov/api/ext-climatology/download-nfdr"
                              f"?stationIds={station_id}&endDate={end.strftime('%Y-%m-%dT%H:%M:%S')}Z&startDate={start.strftime('%Y-%m-%dT%H:%M:%S')}Z&"
                              f"dataFormat=csv&dataset=forecast&fuelModels={fuel_model}&dateTimeFormat=UTC",
                            path,
                            fname,
                            proxies=proxies,
                            notifications='off',
                            clear_recycle_bin=clear_recycle_bin)
    
    return df

def get_multi_raws_station_nfdrs_forecast(station_ids, 
                                        fuel_model='Y', 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Multi Station/NFDRS Forecasts',
                                        proxies=None,
                                        clear_data=True):

    """
    This function retrieves the 7-Day NFDRS forecast for a user-specified list of RAWS stations. 

    Required Arguments:

    1) station_ids (Integer List) - An integer list of all the RAWS IDs for each RAWS station the user wants in the dataset.

    Optional Arguments:

    1) fuel_model (String) - Default = 'Y'. The fuel model being used. 
        Fuel Models List:

        Y - Timber
        X - Brush
        W - Grass/Shrub
        V - Grass
        Z - Slash
    
    2) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    3) path (String) - Default=f'{folder_modified}/FEMS Data/Multi Station/Forecasts'. The directory the data will be saved to. 
        
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    Returns
    -------
    
    A Pandas DataFrame of the 7-Day NFDRS forecast for a user-specified list of RAWS stations.   
    """
    
    if clear_data is True:
        _clear_data(path)
    
    fuel_model = fuel_model.upper()
    
    try:
        start = _datetime.now(_UTC)
    except Exception as e:
        start = _datetime.utcnow()
        
    end = start + _timedelta(days=7)
    
    for station_id in station_ids:
    
        fname = f"{station_id} 7 Day Fuels Forecast Fuel Model {fuel_model}.csv"

        df = _client.get_csv_data(f"https://fems.fs2c.usda.gov/api/ext-climatology/download-nfdr"
                                f"?stationIds={station_id}&endDate={end.strftime('%Y-%m-%dT%H:%M:%S')}Z&startDate={start.strftime('%Y-%m-%dT%H:%M:%S')}Z&"
                                f"dataFormat=csv&dataset=forecast&fuelModels={fuel_model}&dateTimeFormat=UTC",
                                path,
                                fname,
                                proxies=proxies,
                                notifications='off',
                                clear_recycle_bin=clear_recycle_bin)
    
    file_list = _glob.glob(f"{path}/*.csv")
            
    df_list = [_pd.read_csv(file) for file in file_list]
    
    df = _pd.concat(df_list, ignore_index=True)
    
    return df

def get_single_raws_station_weather_forecast(station_id, 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Single Station/Weather Forecasts',
                                        proxies=None,
                                        clear_data=True):

    """
    This function retrieves the 7-Day NFDRS forecast for a user-specified single RAWS station. 

    Required Arguments:

    1) station_id (Integer) - The RAWS ID of the station. 

    Optional Arguments:

    1) fuel_model (String) - Default = 'Y'. The fuel model being used. 
        Fuel Models List:

        Y - Timber
        X - Brush
        W - Grass/Shrub
        V - Grass
        Z - Slash
    
    2) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    3) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/Forecasts'. The directory the data will be saved to. 
        
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    Returns
    -------
    
    A Pandas DataFrame of the 7-Day NFDRS forecast for a user-specified RAWS station.           
    """
    if clear_data is True:
        _clear_data(path)
    
    
    fname = f"{station_id} 7 Day Weather Forecast.csv"

    try:
        start = _datetime.now(_UTC)
    except Exception as e:
        start = _datetime.utcnow()
        
    end = start + _timedelta(days=7)

    df = _client.get_csv_data(f"https://fems.fs2c.usda.gov/api/ext-climatology/download-weather"
                              f"?stationIds={station_id}&startDate={start.strftime('%Y-%m-%dT%H:%M:%S')}Z&endDate={end.strftime('%Y-%m-%d')}T23:29:59Z&dataset=forecast&"
                              f"dataFormat=csv&dataIncrement=hourly",
                            path,
                            fname,
                            proxies=proxies,
                            notifications='off',
                            clear_recycle_bin=clear_recycle_bin)
    
    return df

def get_multi_raws_station_weather_forecast(station_ids, 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Multi Station/Weather Forecasts',
                                        proxies=None,
                                        clear_data=True):

    """
    This function retrieves the 7-Day NFDRS forecast for a user-specified single RAWS station. 

    Required Arguments:

    1) station_id (Integer) - The RAWS ID of the station. 

    Optional Arguments:

    1) fuel_model (String) - Default = 'Y'. The fuel model being used. 
        Fuel Models List:

        Y - Timber
        X - Brush
        W - Grass/Shrub
        V - Grass
        Z - Slash
    
    2) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    3) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/Forecasts'. The directory the data will be saved to. 
        
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    Returns
    -------
    
    A Pandas DataFrame of the 7-Day NFDRS forecast for a user-specified RAWS station.           
    """
    if clear_data is True:
        _clear_data(path)
    
    for station_id in station_ids:
        fname = f"{station_id} 7 Day Weather Forecast.csv"

        try:
            start = _datetime.now(_UTC)
        except Exception as e:
            start = _datetime.utcnow()
            
        end = start + _timedelta(days=7)

        df = _client.get_csv_data(f"https://fems.fs2c.usda.gov/api/ext-climatology/download-weather"
                                f"?stationIds={station_id}&startDate={start.strftime('%Y-%m-%dT%H:%M:%S')}Z&endDate={end.strftime('%Y-%m-%d')}T23:29:59Z&dataset=forecast&"
                                f"dataFormat=csv&dataIncrement=hourly",
                                path,
                                fname,
                                proxies=proxies,
                                notifications='off',
                                clear_recycle_bin=clear_recycle_bin)
    
    
    file_list = _glob.glob(f"{path}/*.csv")
            
    df_list = [_pd.read_csv(file) for file in file_list]
    
    df = _pd.concat(df_list, ignore_index=True)
    return df
