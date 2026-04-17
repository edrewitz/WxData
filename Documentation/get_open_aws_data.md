# Get Open AWS Data

***def get_open_aws_data(bucket,
                      key,
                      path,
                      filenames,
                      proxies=None,
                      notifications='off',
                      clear_recycle_bin=False,
                      clear_data=True):***

    This function downloads open data from Amazon AWS.
    
    Required Arguments:
    
    1) bucket (String) - The Amazon AWS Bucket Name.
    
    2) key (String) - The directory inside of the bucket that the file is in. 
    
    3) path (String) - The local directory where the file will be saved to
    
    4) filenames (String List) - The names of the files being downloaded
    
    Optional Arguments:
    
    1) proxies (String or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies="http://your-proxy-address:port" ---> get_open_aws_data(bucket,
                                                                                            key,
                                                                                            path,
                                                                                            filenames,
                                                                                            proxies=proxies)

    2) notifications (String) - Default='on'. When set to 'on' a print statement to the user will tell the user their file saved to the path
        they specified. 
    
    3) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
                                                                                            
    4) clear_data (Boolean) - Default=True. When set to True, the files in {path} will be cleared. 
                                                                                            
    Returns
    -------
    
    Open data from Amazon AWS downloaded to the local computer.

