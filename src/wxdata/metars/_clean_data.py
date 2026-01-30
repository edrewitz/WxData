import pandas as pd

def clean_data(df):
    
    """
    This function will clean the METAR Data into a more use-able format. 
    
    Required Arguments:
    
    1) df (Pandas.DataFrame) - The Pandas.DataFrame of the METAR Data.
    
    Optional Arguments: None
    
    Returns
    -------
    
    A cleaned up Pandas.DataFrame of the METAR observations    
    """
    
    new_df = pd.DataFrame()
    
    new_df['station_id'] = df['station_id']
    new_df['observation_time'] = pd.to_datetime(df['observation_time'])
    new_df['latitude'] = pd.to_numeric(df['latitude'])
    new_df['longitude'] = pd.to_numeric(df['longitude'])
    new_df['temperature'] = pd.to_numeric(df['temp_c'])
    new_df['dew_point'] = pd.to_numeric(df['dewpoint_c'])
    new_df['wind_direction'] = pd.to_numeric(df['wind_dir_degrees'])
    new_df['wind_speed'] = pd.to_numeric(df['wind_speed_kt'])
    new_df['wind_gust'] = pd.to_numeric(df['wind_gust_kt'])
    
    df['visibility_statute_mi'] = df['visibility_statute_mi'].str.replace('+', '', regex=False)
    new_df['visibility'] = pd.to_numeric(df['visibility_statute_mi'])
    new_df['observation_type'] = df['metar_type']
    new_df['elevation'] = pd.to_numeric(df['elevation_m'])
    
    return new_df