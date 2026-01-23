# Get CSV Data

***def get_csv_data(url,
                 path,
                 filename,
                 proxies=None,
                 notifications='on',
                 return_pandas_df=True,
                 clear_recycle_bin=False):***

    This function is the client that retrieves CSV files from the web.
    This client supports VPN/PROXY connections. 
    User also has the ability to read the CSV file and return a Pandas.DataFrame()
    
    Required Arguments:
    
    1) url (String) - The download URL to the file. 
    
    2) path (String) - The directory where the file is saved to. 
    
    3) filename (String) - The name the user wishes to save the file as. 
    
    Optional Arguments:
    
    1) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        } 
    
    2) notifications (String) - Default='on'. Notification when a file is downloaded and saved to {path}
    
    3) return_pandas_df (Boolean) - Default=True. When set to True, a Pandas.DataFrame() of the data inside the CSV file will be returned to the user. 
    
    4) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
    
    
    Returns
    -------
    
    A CSV file saved to {path}
    
    if return_pandas_df=True - A Pandas.DataFrame()
