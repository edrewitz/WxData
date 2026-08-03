---
title: Air Now API Observations
---
[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)
# Air Now API Observations

```python
def get_current_data_bounding_box(api_key=None,
                                  read_in_key_from_path=True,
                                  parameter='pm25',
                                  western_bound=-124.205070,
                                  eastern_bound=-75.337882,
                                  southern_bound=28.716781,
                                  northern_bound=45.419415,
                                  proxies=None,
                                  to_csv=False,
                                  path=f"Air Now Data/{now.strftime('%Y_%m_%d')}_{now_hour}"):
```

This function retrieves air-quality data from the airnow API.

Required Arguments: None
    
Optional Arguments:

1) api_key (String) - Default=None. 

    The user needs to either pass in an API Key or a path to a .txt file where the API Key is stored. 
    
    It is strongly recommended to not put the API Key itself in your code. It is recommended to store the key
    in a file and read that key into the code.
    
    The easiest way is to create a text (.txt) file with a single element inside of it that is your API Key for Air Now.
    
    If the user wishes to follow this method - set `read_in_key_from_path=True` which is the default setting.
    The user will then set `api_key={path to api key text file}`
    
    If the user wishes to use their own methods of ingesting the API Key, then set `api_key=your_api_key_variable`.

    To get an API Key create a free account at: https://docs.airnowapi.org/

2) read_in_key_from_path (Boolean) - Default=True. When set to True, the API Key is read in from a text file (.txt) at
    the path specified in `api_key`. Set `read_in_key_from_path=False` if the user wishes to use their own method for
    ingesting their Air Now API Key. 


3) parameter (String) - Default='pm25'.

    ***Parameters***
    
        'pm25' - PM 2.5
        'pm10' - PM 10
        'ozone' - Ozone (O3)
        'no2' - Nitrogen Dioxide (NO2)
        'co' - Carbon Monoxide (CO)
        'so2' - Sulfur Dioxide (SO2)
    
4) western_bound (Float or Integer) - Default=-124.205070. 

5) eastern_bound (Float or Integer) - Default=-75.337882. 

6) southern_bound (Float or Integer) - Default=28.716781. 

7) northern_bound (Float or Integer) - Default=45.419415. 

8) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:
    ```python
    proxies=None ---> proxies={
                           'http':'http://your-proxy-address:port',
                           'https':'http://your-proxy-address:port'
                           }
    ```
9) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}

10) path (String) - The path where the CSV file is saved to.

**Returns**

A `Pandas.DataFrame` of all the current air quality observations within the bounding box.     
