---
title: ECMWF AIFS Wave Ensemble
---
# ECMWF AIFS Wave Ensemble

```python
def ecmwf_aifs_wave_ens(final_forecast_hour=360,
                    western_bound=-180,
                    eastern_bound=180,
                    northern_bound=90,
                    southern_bound=-90,
                    proxies=None,
                    process_data=True,
                    clear_recycle_bin=False,
                    custom_directory=None,
                    notifications='off',
                    source='ecmwf',
                    clear_data=False,
                    cat='control',
                    variables=['mean zero-crossing wave period',
                               'significant wave height',
                                'mean wave direction',
                                'mean wave period',
                                'peak wave period'],
                    members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                      31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
                      41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
                to_netcdf=False,
                netcdf_path=f"ECMWF AIFS WAVE ENSEMBLE/NETCDF",
                netcdf_filename=f"ecmwf_aifs_wave_ensemble.nc",
                delete_previous_netcdf_file=True,
                return_values=True):
```

This function is the main client that downloads and processes ECMWF AIFS Wave Ensemble data. 

***This client can do the following:***

1) Download ECMWF AIFS Wave Ensemble data from ECMWF Open-Data, Amazon Web Services and Google Cloud servers.

2) Query your download by downloading only the variables, levels and ensemble members needed. 

3) Subset the GRIB data into a user-specified bounding box and decode the GRIB2 keys into plain-language.
    
4) Convert the xarray.array of decoded GRIB2 data into a NETCDF (.nc) file. 

5) Manages the ECMWF AIFS Wave Ensemble files in the local directory.    

6) Handle user-specified proxy-server protocol - Useful for users working on VPN connections and behind firewalls.  

7) Automatically Rotate between ECMWF Open-Data, Amazon Web Services and Google Cloud in the event of significant server connection issues.

8) Validates the download and helps the user troubleshoot if needed. 

These ECMWF end-to-end clients can download ECMWF data from the following sources: 

  i) ECMWF Open-Data Server
  
  ii) Amazon AWS Server
  
  iii) Google Cloud Server
        
***If the server of your choice is down, the client will rotate to another one and try scanning for data and downloading there.***
***If the client cannot connect to any of the servers, the system will exit.***

1) final_forecast_hour (Integer) - Default = 360. The maximum forecast hour. 
    
2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

6) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

  ```python
   proxies=None ---> proxies={
                           'http':'http://your-proxy-address:port',
                           'https':'http://your-proxy-address:port'
                           }
  ```

8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
   data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
   
9) clear_recycle_bin (Boolean) - (Default=False). Set to True to clear your recycle bin. 
    
10) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
    either Celsius or Fahrenheit. When False, this data remains in Kelvin.
    
11) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
    Set convert_to='fahrenheit' for Fahrenheit. 
    
12) custom_directory (String or None) - Default=None. The directory path where the ECMWF AIFS Wave files will be saved to.
    Default = "ECMWF/AIFS/WAVE ENSEMBLE"

13) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}

14) source (String) - Default='ecmwf'. The data server choice. 

  ***Data Sources***
  
  i) ECMWF Open-Data Server = 'ecmwf'
  
  i) Amazon AWS Server = 'aws'
  
  iii) Google Cloud Server = 'google'
 
  *If the client is unable to connect to the server the user specified, it will rotate to the next server and try to 
  establish a connection there.*
    
15) cat (String) - Default='control'. The type of ensemble run. 

  Control Run - `cat='control'`
  
  Ensemble Members - `cat='members'`
    
16) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
    When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 

17) variables (String List) - Default is all variables. The list of variable names in plain-language. 

  ***Variables***

  ```python
  'significant wave height'
  'mean wave direction'
  'mean wave period'
  ```
    
17) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.

18) netcdf_path (String) - Default='ECMWF AIFS WAVE ENSEMBLE/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.

19) netcdf_filename (String) - Default='ecmwf_aifs_wave_ensemble.nc'. The name of the netCDF (.nc) file. A good practice is to 
    name this netCDF file using the variable name. 
    
20) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
    new netCDF file. For users who want to archive all data set this to False. 
    
21) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned. 
    
**Returns**

An xarray.data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys

***Plain Language ECMWF AIFS Wave Ensemble Variable Keys (After Post-Processing)***

```python
'significant_height_of_combined_waves_and_swell'
'mean_wave_direction'
'mean_wave_period'
```
