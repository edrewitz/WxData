# NEXRAD II Multi-Radar

***def download_current_multi_station_nexrad2_radar_data(site_ids,
                                                        hours=3,
                                                        path=f"Radar Data",
                                                        proxies=None,
                                                        clear_recycle_bin=False,
                                                        mode='precipitation',
                                                        notifications='off'):***

    This function downloads the latest NEXRAD2 Radar Data from NOAAs Open Data Amazon AWS Server and returns
    a list of Py-ART objects for a user-specified list of site IDs and user-specified period of time.
    
    Required Arguments:
    
    1) site_ids (String List) - A list of the 4-letter IDs of the radar sites.
    
    Optional Arguments:
    
    1) hours (Integer) - Default=3. The amount of hours to query (hours=3 --> current to current -3 hours).
    
    2) path (String) - Default="Radar Data". The parent directory of the radar data on the local computer.
    
    3) proxies (String or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies="http://your-proxy-address:port" ---> download_current_single_station_nexrad2_radar_data(bucket,
                                                                                                                            key,
                                                                                                                            path,
                                                                                                                            filenames,
                                                                                                                            proxies=proxies)
    
    4) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    5) mode (String) - Default='precipitation'. When in 'precipitation' mode, data querying is based on 10 scans per hour.
        When in 'clear air' mode, data querying is based on 7 scans per hour.
        
    6) notifications (String) - Default='on'. When set to 'on' a print statement to the user will tell the user their file saved to the path
        they specified. 
        
    Returns
    -------
    
    A list of Py-ART Radar Objects for a user-specified list of stations and for a user-specified period of time.
    The user-specified period of time is the same for both stations. 
