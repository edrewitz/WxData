# FEMS: RAWS Station Current Weather Observations By State

***def get_current_all_raws_station_weather_observations(state='all', 
                                                clear_recycle_bin=False,
                                                path=f'{folder_modified}/FEMS Data/Current Multi Station/Observations/Weather',
                                                proxies=None,
                                                clear_data=True,
                                                meta_path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                                sheet_name='Sheet1'):***


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
