# METAR Observations

***def download_metar_data(clear_recycle_bin=False,
                        proxies=None):***

    Downloads the latest METAR Data from NOAA/AWC and returns a Pandas DataFrame.
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    2) proxies (String or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies="http://your-proxy-address:port" ---> ds = download_metar_data(proxies=proxies)
        

    Returns
    -------
    
    pd.DataFrame: A DataFrame containing the METAR data.
