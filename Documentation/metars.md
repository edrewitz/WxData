# METAR Observations

***def download_metar_data(clear_recycle_bin=False)***

Downloads the latest METAR Data from NOAA/AWC and returns a Pandas DataFrame.

Required Arguments: None

Optional Arguments:

1) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 

Returns:        
pd.DataFrame: A DataFrame containing the METAR data.
