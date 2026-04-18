# Get AWS Open Data

***def get_aws_open_data(url,
                    path,
                    filename,
                    proxies=None,
                    chunk_size=8192,
                    notifications='on',
                    clear_recycle_bin=False):***

    This function is the client that retrieves Open Data from Amazon AWS Servers. 
    This client supports VPN/PROXY connections. 
    
    Required Arguments:
    
    1) url (String) - The download URL to the file. 
    
    2) path (String) - The directory where the file is saved to. 
    
    3) filename (String) - The name the user wishes to save the file as. 
    
    Optional Arguments:
    
    1) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    2) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    3) notifications (String) - Default='on'. Notification when a file is downloaded and saved to {path}
    
    4) clear_recycle_bin (Boolean) - Default=False. When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
    
    Returns
    -------
    
    Files from AWS Open Data.  

