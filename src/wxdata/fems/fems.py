"""
This file hosts the clients that download and process the following types of data from the USDA/FEMS Database.

1) get_single_raws_station_weather_observations
2) get_single_raws_station_fuels_observations
3) get_multi_raws_station_weather_observations
4) get_multi_raws_station_fuels_observations
5) get_current_multi_raws_station_weather_observations
6) get_current_multi_raws_station_fuels_observations
7) get_current_all_raws_station_weather_observations
8) get_current_all_raws_station_fuels_observations
9) get_single_raws_station_nfdrs_forecast
10) get_multi_raws_station_nfdrs_forecast
11) get_single_raws_station_weather_forecast
12) get_multi_raws_station_weather_forecast

(C) Eric J. Drewitz 2025-2026
"""

import pandas as _pd
import os as _os
import glob as _glob
import wxdata.client.client as _client
import shutil as _shutil
import numpy as _np

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

def _clear_jupyter_checkpoints(path):
    
    """
    This function clears the jupyter notebook checkpoints folder if it is created in the data directory.
    
    Required Arguments:
    
    1) path (String) - The path to the directory.
    
    Optional Arguments: None
    
    Returns
    -------
    
    Clears the Jupyter Notebook checkpoints directory if it is created to prevent it from corrupting the clearing out of old files.    
    """
    
    try:
        _shutil.rmtree(f"{path}/.ipynb_checkpoints")
    except Exception as e:
        pass

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
    
    4) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    5) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/Observations/Weather'. 
        The directory the data will be saved to. 
        
    6) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    7) clear_data (Boolean) - Default=True. When set to True, the data directory clears out and new data is downloaded.
    
    8) meta_path (String) - Default=f'{folder_modified}/FEMS Data/Station Meta Data'. 
        The path to where the RAWS station meta data excel file will be saved to. 
        
    9) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame.
    
    Returns
    -------
    
    1) A Pandas DataFrame of observed weather data for a user-specified single RAWS station for a user-specified time.   
    2) A Pandas DataFrame of the RAWS Station Meta-Data.        
    """
    
    if clear_data is True:
        _clear_jupyter_checkpoints(path)
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
    
    meta = _get_single_raws_station_meta_data(station_id, 
                                        sheet_name=sheet_name,
                                        clear_recycle_bin=False,
                                        path=meta_path,
                                        proxies=proxies)
    
    keys = df.columns.tolist()
    meta_keys = meta.columns.tolist()
    
    df = df.sort_values(by=keys[0], ascending=False)
    meta = meta.sort_values(by=meta_keys[6], ascending=False)
    
    return df, meta

def get_single_raws_station_fuels_observations(station_id, 
                                        number_of_days=7, 
                                        start_date=None, 
                                        end_date=None, 
                                        fuel_model='Y', 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Single Station/Observations/Fuels',
                                        proxies=None,
                                        clear_data=True,
                                        meta_path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                        sheet_name='Sheet1'):

    """
    This function retrieves the observed fuels data for a user-specified single RAWS station for a 
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
        
    6) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/Observations/Fuels'. 
        The directory the data will be saved to. 
        
    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    8) clear_data (Boolean) - Default=True. When set to True, the data directory clears out and new data is downloaded.
    
    9) meta_path (String) - Default=f'{folder_modified}/FEMS Data/Station Meta Data'. 
        The path to where the RAWS station meta data excel file will be saved to. 
        
    10) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame.
    
    Returns
    -------
    
    1) A Pandas DataFrame of observed fuels data for a user-specified single RAWS station for a user-specified time. 
    2) A Pandas DataFrame of the RAWS Station Meta-Data.     
    """
    
    if clear_data is True:
        _clear_jupyter_checkpoints(path)
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
    
    meta = _get_single_raws_station_meta_data(station_id, 
                                        sheet_name=sheet_name,
                                        clear_recycle_bin=False,
                                        path=meta_path,
                                        proxies=proxies)
    
    keys = df.columns.tolist()
    meta_keys = meta.columns.tolist()
    
    df = df.sort_values(by=keys[0], ascending=False)
    meta = meta.sort_values(by=meta_keys[6], ascending=False)
    
    return df, meta

def get_multi_raws_station_weather_observations(station_ids, 
                                        number_of_days=7, 
                                        start_date=None, 
                                        end_date=None, 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Multi Station/Observations/Weather',
                                        proxies=None,
                                        clear_data=True,
                                        meta_path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                        sheet_name='Sheet1'):

    """
    This function retrieves the observed weather data for a user-specified list of RAWS stations for a 
    user-specified period of time. 

    Required Arguments:

    1) station_ids (Integer List) - The list of RAWS station IDs. 

    Optional Arguments:
    
    1) number_of_days (Integer or String) - Default=7. How many days the user wants the summary for (90 for 90 days).
        If the user wants to use a custom date range enter 'Custom' or 'custom' in this field. 

    2) start_date (String) - Default = None. The start date if the user wants to define a custom period. Enter as a string
        in the following format 'YYYY-mm-dd'

    3) end_date (String) - Default = None. The end date if the user wants to define a custom period. Enter as a string
        in the following format 'YYYY-mm-dd'
    
    4) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    5) path (String) - Default=f'{folder_modified}/FEMS Data/Multi Station/Observations/Weather'. 
        The directory the data will be saved to. 
        
    6) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    7) clear_data (Boolean) - Default=True. When set to True, the data directory clears out and new data is downloaded.
    
    8) meta_path (String) - Default=f'{folder_modified}/FEMS Data/Station Meta Data'. 
        The path to where the RAWS station meta data excel file will be saved to. 
        
    9) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame.
    
    Returns
    -------
    
    1) A Pandas DataFrame of observed weather data for a user-specified list of RAWS stations for a user-specified time period.    
    2) A Pandas DataFrame of the RAWS Station Meta-Data.      
    """
    
    if clear_data is True:
        _clear_jupyter_checkpoints(path)
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
    
    meta = _get_multi_raws_station_meta_data(station_ids, 
                                        sheet_name=sheet_name,
                                        clear_recycle_bin=False,
                                        path=meta_path,
                                        proxies=proxies)
    
    
    file_list = _glob.glob(f"{path}/*.csv")
            
    df_list = [_pd.read_csv(file) for file in file_list]
    
    df = _pd.concat(df_list, ignore_index=True)
    
    keys = df.columns.tolist()
    meta_keys = meta.columns.tolist()
    
    df = df.sort_values(by=keys[0], ascending=False)
    meta = meta.sort_values(by=meta_keys[6], ascending=False)
    
    return df, meta

def get_multi_raws_station_fuels_observations(station_ids, 
                                        number_of_days=7, 
                                        start_date=None, 
                                        end_date=None, 
                                        fuel_model='Y', 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Multi Station/Observations/Fuels',
                                        proxies=None,
                                        clear_data=True,
                                        meta_path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                        sheet_name='Sheet1'):

    """
    This function retrieves the observed fuels data for a user-specified list of RAWS stations for a 
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
        
    6) path (String) - Default=f'{folder_modified}/FEMS Data/Multi Station/Observations/Fuels'. 
        The directory the data will be saved to.
        
    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    8) clear_data (Boolean) - Default=True. When set to True, the data directory clears out and new data is downloaded.
    
    9) meta_path (String) - Default=f'{folder_modified}/FEMS Data/Station Meta Data'. 
        The path to where the RAWS station meta data excel file will be saved to. 
        
    10) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame.
    
    Returns
    -------
    
    1) A Pandas DataFrame of observed fuels data for a user-specified list of RAWS stations for a user-specified time period.      
    2) A Pandas DataFrame of the RAWS Station Meta-Data.               
    """
    
    if clear_data is True:
        _clear_jupyter_checkpoints(path)
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
            
    meta = _get_multi_raws_station_meta_data(station_ids, 
                                        sheet_name=sheet_name,
                                        clear_recycle_bin=False,
                                        path=meta_path,
                                        proxies=proxies)
    
    
    file_list = _glob.glob(f"{path}/*.csv")
            
    df_list = [_pd.read_csv(file) for file in file_list]
    
    df = _pd.concat(df_list, ignore_index=True)
    
    keys = df.columns.tolist()
    meta_keys = meta.columns.tolist()
    
    df = df.sort_values(by=keys[0], ascending=False)
    meta = meta.sort_values(by=meta_keys[6], ascending=False)
    
    return df, meta

def get_current_multi_raws_station_weather_observations(station_ids, 
                                                clear_recycle_bin=False,
                                                path=f'{folder_modified}/FEMS Data/Current Multi Station/Observations/Weather',
                                                proxies=None,
                                                clear_data=True,
                                                meta_path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                                sheet_name='Sheet1'):

    """
    This function retrieves the current weather observations for a user-specified list of RAWS Stations. 

    Required Arguments:

    1) station_ids (Integer List) - An integer list of all the RAWS IDs for each RAWS station the user wants in the dataset.

    Optional Arguments:
    
    1) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    2) path (String) - Default=f'{folder_modified}/FEMS Data/Current Multi Station/Observations/Weather'. 
        The directory the data will be saved to. 
        
    3) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    4) clear_data (Boolean) - Default=True. When set to True, the data directory clears out and new data is downloaded.
    
    5) meta_path (String) - Default=f'{folder_modified}/FEMS Data/Station Meta Data'. 
        The path to where the RAWS station meta data excel file will be saved to. 
        
    6) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame.
    
    Returns
    -------
    
    A Pandas DataFrame of current observed weather data with lat/lon coordinates for each station merged from the meta-data file.         
    """
    if clear_data is True:
        _clear_jupyter_checkpoints(path)
        _clear_data(path)
    
    for station_id in station_ids:
    
        fname = f"{station_id} Weather Observations.csv"

        try:
            now = _datetime.now(_UTC)
        except Exception as e:
            now = _datetime.utcnow()
            
        start = now - _timedelta(hours=3)

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
    This function retrieves the current fuels observations for a user-specified list of RAWS Stations. 

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
        
    3) path (String) - Default=f'{folder_modified}/FEMS Data/Current Multi Station/Observations/Fuels'. 
        The directory the data will be saved to.
        
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    5) clear_data (Boolean) - Default=True. When set to True, the data directory clears out and new data is downloaded.
    
    6) meta_path (String) - Default=f'{folder_modified}/FEMS Data/Station Meta Data'. 
        The path to where the RAWS station meta data excel file will be saved to. 
        
    7) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame.
    
    Returns
    -------
    
    A Pandas DataFrame of current observed fuels data with lat/lon coordinates for each station merged from the meta-data file.             
    """
    if clear_data is True:
        _clear_jupyter_checkpoints(path)
        _clear_data(path)
    
    fuel_model = fuel_model.upper()
    
    try:
        now = _datetime.now(_UTC)
    except Exception as e:
        now = _datetime.utcnow()
            
    start = now - _timedelta(hours=3)
    
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

def get_current_all_raws_station_weather_observations(state='all', 
                                                clear_recycle_bin=False,
                                                path=f'{folder_modified}/FEMS Data/Current Multi Station/Observations/Weather',
                                                proxies=None,
                                                clear_data=True,
                                                meta_path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                                sheet_name='Sheet1'):

    """
    This function retrieves all current weather observations for all RAWS Stations of a given state.

    Required Arguments: None

    Optional Arguments:
    
    1) state (String) - Default='all'. The 2-letter state identifier. Defaults to the entire U.S. 
    
    2) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    3) path (String) - Default=f'{folder_modified}/FEMS Data/Current Multi Station/Observations/Weather'. 
        The directory the data will be saved to. 
        
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    5) clear_data (Boolean) - Default=True. When set to True, the data directory clears out and new data is downloaded.
    
    6) meta_path (String) - Default=f'{folder_modified}/FEMS Data/Station Meta Data'. 
        The path to where the RAWS station meta data excel file will be saved to. 
        
    7) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame.
    
    Returns
    -------
    
    A Pandas DataFrame of current observed weather data with lat/lon coordinates for each station merged from the meta-data file.         
    """
    if clear_data is True:
        _clear_jupyter_checkpoints(path)
        _clear_data(path)
        
    meta = _client.get_excel_data(f"https://wildfireweb-prod-media-bucket.s3.us-gov-west-1.amazonaws.com/s3fs-public/2025-07/FEMS_3.0_RAWS_Master_Station_List_and_Metadata.xlsx",
                        meta_path,
                        f"RAWS Meta Data.xlsx",
                        sheet_name,
                        proxies=proxies,
                        notifications='off',
                        clear_recycle_bin=clear_recycle_bin)
    
    try:
        now = _datetime.now(_UTC)
    except Exception as e:
        now = _datetime.utcnow()
            
    start = now - _timedelta(hours=3)
    
    meta_keys = meta.columns.tolist()
    if state == 'all':
        station_ids = meta[meta_keys[1]]
    else:
        state = state.upper()
        meta = meta[meta[meta_keys[7]] == state]
        station_ids = meta[meta_keys[1]]
    
    for station_id in station_ids:
    
        fname = f"{station_id} Weather Observations.csv"

        _client.get_csv_data(f"https://fems.fs2c.usda.gov/api/ext-climatology/download-weather?"
                                f"stationIds={station_id}&startDate={start.strftime('%Y-%m-%dT%H:%M:%S')}Z&endDate={now.strftime('%Y-%m-%dT%H:%M:%S')}Z&"
                                f"dataset=observation&dataFormat=csv&dataIncrement=hourly",
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
    
    df[keys[0]] = df[keys[0]].str.strip().replace('', _np.nan)
    df = df[df[keys[0]].notna()]
    meta = _pd.read_excel(f"{meta_path}/RAWS Meta Data.xlsx", sheet_name=sheet_name)
    
    stations = df[keys[0]]
    meta = meta[meta[meta_keys[7]] == state.upper()]
    meta = meta[meta[meta_keys[6]].isin(stations)]
    
    df = df.groupby(keys[0]).tail(1)
    
    df = df.sort_values(by=keys[0], ascending=True)
    meta = meta.sort_values(by=meta_keys[6], ascending=True)
    df[meta_keys[9]] = meta[meta_keys[9]].values
    df[meta_keys[10]] = meta[meta_keys[10]].values
    
    return df

def get_current_all_raws_station_fuels_observations(state='all',
                                                fuel_model='Y', 
                                                clear_recycle_bin=False,
                                                path=f'{folder_modified}/FEMS Data/Current Multi Station/Observations/Fuels',
                                                proxies=None,
                                                clear_data=True,
                                                meta_path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                                sheet_name='Sheet1'):

    """
    This function retrieves all current fuels observations for all RAWS Stations of a given state.

    Required Arguments: None

    Optional Arguments:
    
    1) state (String) - Default='all'. The 2-letter state identifier. Defaults to the entire U.S. 

    2) fuel_model (String) - Default = 'Y'. The fuel model being used. 
        Fuel Models List:

        Y - Timber
        X - Brush
        W - Grass/Shrub
        V - Grass
        Z - Slash
    
    3) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    4) path (String) - Default=f'{folder_modified}/FEMS Data/Current Multi Station/Observations/Fuels'. 
        The directory the data will be saved to.
        
    5) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }

    5) clear_data (Boolean) - Default=True. When set to True, the data directory clears out and new data is downloaded.
    
    6) meta_path (String) - Default=f'{folder_modified}/FEMS Data/Station Meta Data'. 
        The path to where the RAWS station meta data excel file will be saved to. 
        
    7) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame.
    
    Returns
    -------
    
    A Pandas DataFrame of current observed fuels data with lat/lon coordinates for each station merged from the meta-data file.                   
    """
    if clear_data is True:
        _clear_jupyter_checkpoints(path)
        _clear_data(path)
    
    fuel_model = fuel_model.upper()
    
    try:
        now = _datetime.now(_UTC)
    except Exception as e:
        now = _datetime.utcnow()
            
    start = now - _timedelta(hours=3)
        
    meta = _client.get_excel_data(f"https://wildfireweb-prod-media-bucket.s3.us-gov-west-1.amazonaws.com/s3fs-public/2025-07/FEMS_3.0_RAWS_Master_Station_List_and_Metadata.xlsx",
                            meta_path,
                            f"RAWS Meta Data.xlsx",
                            sheet_name,
                            proxies=proxies,
                            notifications='off',
                            clear_recycle_bin=clear_recycle_bin)
    
    
    meta_keys = meta.columns.tolist()
    if state == 'all':
        station_ids = meta[meta_keys[1]]
    else:
        state = state.upper()
        meta = meta[meta[meta_keys[7]] == state]
        station_ids = meta[meta_keys[1]]
    
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
    
    df[keys[0]] = df[keys[0]].str.strip().replace('', _np.nan)
    df = df[df[keys[0]].notna()]
    meta = _pd.read_excel(f"{meta_path}/RAWS Meta Data.xlsx", sheet_name=sheet_name)
    
    stations = df[keys[0]]
    meta = meta[meta[meta_keys[7]] == state.upper()]
    meta = meta[meta[meta_keys[6]].isin(stations)]
    
    df = df.groupby(keys[0]).tail(1)
    
    df = df.sort_values(by=keys[0], ascending=True)
    meta = meta.sort_values(by=meta_keys[6], ascending=True)
    df[meta_keys[9]] = meta[meta_keys[9]].values
    df[meta_keys[10]] = meta[meta_keys[10]].values
    
    return df

def get_single_raws_station_weather_forecast(station_id, 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Single Station/Weather Forecasts',
                                        proxies=None,
                                        clear_data=True,
                                        meta_path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                        sheet_name='Sheet1'):

    """
    This function retrieves the 7-Day weather forecast for a user-specified single RAWS station. 

    Required Arguments:

    1) station_id (Integer) - The RAWS ID of the station. 

    Optional Arguments:
    
    1) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    2) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/Weather Forecasts'. 
        The directory the data will be saved to. 
        
    3) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    4) clear_data (Boolean) - Default=True. When set to True, the data directory clears out and new data is downloaded.
    
    5) meta_path (String) - Default=f'{folder_modified}/FEMS Data/Station Meta Data'. 
        The path to where the RAWS station meta data excel file will be saved to. 
        
    6) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame.
    
    Returns
    -------
    
    1) A Pandas DataFrame of 7-Day weather forecast data for a user-specified single RAWS station.   
    2) A Pandas DataFrame of the RAWS Station Meta-Data.            
    """
    if clear_data is True:
        _clear_jupyter_checkpoints(path)
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
    
    meta = _get_single_raws_station_meta_data(station_id, 
                                        sheet_name=sheet_name,
                                        clear_recycle_bin=False,
                                        path=meta_path,
                                        proxies=proxies)
    
    keys = df.columns.tolist()
    meta_keys = meta.columns.tolist()
    
    df = df.sort_values(by=keys[0], ascending=False)
    meta = meta.sort_values(by=meta_keys[6], ascending=False)
    
    return df, meta

def get_single_raws_station_nfdrs_forecast(station_id, 
                                        fuel_model='Y', 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Single Station/NFDRS Forecasts',
                                        proxies=None,
                                        clear_data=True,
                                        meta_path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                        sheet_name='Sheet1'):

    """
    This function retrieves the 7-Day NFDRS (fuels) forecast for a user-specified single RAWS station. 

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
        
    3) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/NFDRS Forecasts'. 
        The directory the data will be saved to. 
        
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    5) clear_data (Boolean) - Default=True. When set to True, the data directory clears out and new data is downloaded.
    
    6) meta_path (String) - Default=f'{folder_modified}/FEMS Data/Station Meta Data'. 
        The path to where the RAWS station meta data excel file will be saved to. 
        
    7) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame.
    
    Returns
    -------
    
    1) A Pandas DataFrame of 7-Day NFDRS (fuels) forecast data for a user-specified single RAWS station.   
    2) A Pandas DataFrame of the RAWS Station Meta-Data.           
    """
    if clear_data is True:
        _clear_jupyter_checkpoints(path)
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
    
    meta = _get_single_raws_station_meta_data(station_id, 
                                        sheet_name=sheet_name,
                                        clear_recycle_bin=False,
                                        path=meta_path,
                                        proxies=proxies)
    
    keys = df.columns.tolist()
    meta_keys = meta.columns.tolist()
    
    df = df.sort_values(by=keys[0], ascending=False)
    meta = meta.sort_values(by=meta_keys[6], ascending=False)
    
    return df, meta

def get_multi_raws_station_nfdrs_forecast(station_ids, 
                                        fuel_model='Y', 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Multi Station/NFDRS Forecasts',
                                        proxies=None,
                                        clear_data=True,
                                        meta_path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                        sheet_name='Sheet1'):

    """
    This function retrieves the 7-Day NFDRS (fuels) forecast for a user-specified list of RAWS stations. 

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
        
    3) path (String) - Default=f'{folder_modified}/FEMS Data/Multi Station/NFDRS Forecasts'. 
        The directory the data will be saved to. 
        
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    5) clear_data (Boolean) - Default=True. When set to True, the data directory clears out and new data is downloaded.
    
    6) meta_path (String) - Default=f'{folder_modified}/FEMS Data/Station Meta Data'. 
        The path to where the RAWS station meta data excel file will be saved to. 
        
    7) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame.
    
    Returns
    -------
    
    1) A Pandas DataFrame of 7-Day NFDRS (fuels) forecast data for a user-specified list of RAWS stations.   
    2) A Pandas DataFrame of the RAWS Station Meta-Data.     
    """
    
    if clear_data is True:
        _clear_jupyter_checkpoints(path)
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
    
    meta = _get_multi_raws_station_meta_data(station_ids, 
                                        sheet_name=sheet_name,
                                        clear_recycle_bin=False,
                                        path=meta_path,
                                        proxies=proxies)
    
    
    file_list = _glob.glob(f"{path}/*.csv")
            
    df_list = [_pd.read_csv(file) for file in file_list]
    
    df = _pd.concat(df_list, ignore_index=True)
    
    keys = df.columns.tolist()
    meta_keys = meta.columns.tolist()
    
    df = df.sort_values(by=keys[0], ascending=False)
    meta = meta.sort_values(by=meta_keys[6], ascending=False)
    
    return df, meta

def get_multi_raws_station_weather_forecast(station_ids, 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Multi Station/Weather Forecasts',
                                        proxies=None,
                                        clear_data=True,
                                        meta_path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                        sheet_name='Sheet1'):

    """
    This function retrieves the 7-Day weather forecast for a user-specified list of RAWS stations. 

    Required Arguments:

    1) station_ids (Integer List) - An integer list of all the RAWS IDs for each RAWS station the user wants in the dataset.

    Optional Arguments:
    
    1) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    2) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/Forecasts'. 
        The directory the data will be saved to. 
        
    3) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    4) clear_data (Boolean) - Default=True. When set to True, the data directory clears out and new data is downloaded.
    
    5) meta_path (String) - Default=f'{folder_modified}/FEMS Data/Station Meta Data'. 
        The path to where the RAWS station meta data excel file will be saved to. 
        
    6) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame.
    
    Returns
    -------
    
    1) A Pandas DataFrame of 7-Day weather forecast data for a user-specified list of RAWS stations.   
    2) A Pandas DataFrame of the RAWS Station Meta-Data.             
    """
    if clear_data is True:
        _clear_jupyter_checkpoints(path)
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
        
    meta = _get_multi_raws_station_meta_data(station_ids, 
                                        sheet_name=sheet_name,
                                        clear_recycle_bin=False,
                                        path=meta_path,
                                        proxies=proxies)
    
    
    file_list = _glob.glob(f"{path}/*.csv")
            
    df_list = [_pd.read_csv(file) for file in file_list]
    
    df = _pd.concat(df_list, ignore_index=True)
    
    keys = df.columns.tolist()
    meta_keys = meta.columns.tolist()
    
    df = df.sort_values(by=keys[0], ascending=False)
    meta = meta.sort_values(by=meta_keys[6], ascending=False)
    
    return df, meta
