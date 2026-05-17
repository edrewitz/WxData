"""
This file hosts functions that download various types of GEFS Data.

1) gefs_0p50
2) gefs_0p50_secondary_parameters
3) gefs_0p25

(C) Eric J. Drewitz 2025-2026
"""
import sys as _sys
import wxdata.client.client as _client
import warnings as _warnings
import wxdata.post_processors.gefs_post_processing as _gefs_post_processing
_warnings.filterwarnings('ignore')

from wxdata.gefs.file_funcs import(
    build_directory as _build_directory,
    clear_idx_files as _clear_idx_files,
    clear_empty_files as _clear_empty_files
    
)
from wxdata.gefs.url_scanners import(
    gefs_0p50_url_scanner as _gefs_0p50_url_scanner,
    gefs_0p50_secondary_parameters_url_scanner as _gefs_0p50_secondary_parameters_url_scanner,
    gefs_0p25_url_scanner as _gefs_0p25_url_scanner
)

from wxdata.utils.file_funcs import(
     custom_branch as _custom_branch,
     custom_branches as _custom_branches,
     clear_gefs_idx_files as _clear_gefs_idx_files,
     clear_old_ensemble_data as _clear_old_ensemble_data
)

from wxdata.calc.unit_conversion import convert_temperature_units as _convert_temperature_units
from wxdata.utils.file_scanner import local_file_scanner as _local_file_scanner
from wxdata.utils.recycle_bin import(
    clear_recycle_bin_windows as _clear_recycle_bin_windows,
    clear_trash_bin_mac as _clear_trash_bin_mac,
    clear_trash_bin_linux as _clear_trash_bin_linux
)

def _gefs_0p50_client(cat='mean', 
             final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=False,
             variables=['total precipitation',
                        'convective available potential energy',
                        'categorical freezing rain',
                        'categorical ice pellets',
                        'categorical rain',
                        'categorical snow',
                        'convective inhibition',
                        'downward longwave radiation flux',
                        'downward shortwave radiation flux',
                        'geopotential height',
                        'ice thickness',
                        'latent heat net flux',
                        'pressure',
                        'mean sea level pressure',
                        'precipitable water',
                        'relative humidity',
                        'sensible heat net flux',
                        'snow depth',
                        'volumetric soil moisture content',
                        'total cloud cover',
                        'maximum temperature',
                        'minimum temperature',
                        'temperature',
                        'soil temperature',
                        'u-component of wind',
                        'upward longwave radiation flux',
                        'upward shortwave radiation flux',
                        'v-component of wind',
                        'vertical velocity',
                        'water equivalent of accumulated snow depth'],
            convert_temperature=True,
            convert_to='celsius',
            custom_directory=None,
            chunk_size=8192,
            notifications='off',
            clear_data=False,
            source='noaa',
            level_type='pressure',
            levels=[1000,
                    925,
                    850,
                    700,
                    500,
                    400,
                    300,
                    250,
                    200,
                    100,
                    50,
                    10]):
    
    """
    This function downloads the latest GEFS0P50 data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='mean'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    7) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    9) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    12) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50
        -------------------------------
        
			'total precipitation'
            'convective available potential energy'
            'categorical freezing rain'
            'categorical ice pellets'
            'categorical rain'
            'categorical snow'
            'convective inhibition'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'geopotential height'
            'ice thickness'
            'latent heat net flux'
            'pressure'
            'mean sea level pressure'
            'precipitable water'
            'relative humidity'
            'sensible heat net flux'
            'snow depth'
            'volumetric soil moisture content'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'soil temperature'
            'u-component of wind'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'v-component of wind'
            'vertical velocity'
            'water equivalent of accumulated snow depth'
            
    13) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.
    
    14) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    15) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    16) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    17) custom_directory (String or None) - Default=None. The directory path where the GEFS0P50 files will be saved to.
        
    18) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    19) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    20) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
        
    21) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    22) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'height above ground'
        'surface'
        'height below ground'
        'entire atmosphere (considered as a single layer)'
        'pressure above ground'
        
    23) levels (String, Integer or Float List) - Default=[1000,
                                                            925,
                                                            850,
                                                            700,
                                                            500,
                                                            400,
                                                            300,
                                                            250,
                                                            200,
                                                            100,
                                                            50,
                                                            10]    
                                                            
        The pressure, height or depth levels. 
    
    Returns
    -------
    
    An xarray data array of the GEFS0P50 data specified to the coordinate boundaries and variable list the user specifies. 
    
    GEFS0P50 files are saved to f:GEFS0P50/{cat} or in the case of ensemble members f:GEFS0P50/{cat}/{member}
    
    Variables
    ---------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'convective_available_potential_energy'
    'convective_inhibition'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'u_wind_component'
    'v_wind_component'
    
    """
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass    
    
    
    cat = cat.lower()
    if custom_directory == None:
        
        paths = _build_directory('gefs0p50', 
                                cat, 
                                members)

        _clear_idx_files('gefs0p50', 
                        cat, 
                        members)
    
    else:
        if cat == 'members':
            paths = _custom_branches(custom_directory)
            
        else:
            paths = _custom_branch(custom_directory)
        
        _clear_gefs_idx_files(paths)
        
    if clear_data == True:
        _clear_old_ensemble_data(paths)
    else:
        pass
    
    if source == 'noaa':
        try:
            url, filename, run = _gefs_0p50_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    source)
        except Exception as e:
            filename = None
            
        if filename == None:
            print("NCEP/NOMADS Server Is Down.")
            print("Rotating to Amazon AWS Server.")
            try:
                url, filename, run = _gefs_0p50_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'aws')
                print("Amazon AWS Server Online - Connected.")
            except Exception as e:
                filename = None
                
            if filename == None:
                print("Amazon AWS Server Is Down.")
                print("Rotating to Google Cloud Server.")
                try:
                    url, filename, run = _gefs_0p50_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'google')
                    print("Google Cloud Server Online - Connected.")
                except Exception as e:
                    print("Error: All Servers Appear Down.")
                    print("System Exit")
                    _sys.exit(1)
            else:
                pass
        
        else:
            pass
        
    if source == 'aws':
        try:
            url, filename, run = _gefs_0p50_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    source)
        except Exception as e:
            filename = None
            
        if filename == None:
            print("NCEP/NOMADS Server Is Down.")
            print("Rotating to NCEP/NOMADS Server.")
            try:
                url, filename, run = _gefs_0p50_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'noaa')
                print("NCEP/NOMADS Server Online - Connected.")
            except Exception as e:
                filename = None
                
            if filename == None:
                print("Amazon NCEP/NOMADS Is Down.")
                print("Rotating to Google Cloud Server.")
                try:
                    url, filename, run = _gefs_0p50_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'google')
                    print("Google Cloud Server Online - Connected.")
                except Exception as e:
                    print("Error: All Servers Appear Down.")
                    print("System Exit")
                    _sys.exit(1)
            else:
                pass
        
        else:
            pass
        
    
    if source == 'google':
        try:
            url, filename, run = _gefs_0p50_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    source)
        except Exception as e:
            filename = None
            
        if filename == None:
            print("Google Cloud Server Is Down.")
            print("Rotating to NCEP/NOMADS Server.")
            try:
                url, filename, run = _gefs_0p50_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'noaa')
                print("Google Cloud Server Online - Connected.")
            except Exception as e:
                filename = None
                
            if filename == None:
                print("Amazon NCEP/NOMADS Is Down.")
                print("Rotating to Amazon AWS Server.")
                try:
                    url, filename, run = _gefs_0p50_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'aws')
                    print("Amazon AWS Server Online - Connected.")
                except Exception as e:
                    print("Error: All Servers Appear Down.")
                    print("System Exit")
                    _sys.exit(1)
            else:
                pass
        
        else:
            pass        
    
    download = _local_file_scanner(paths[-1], 
                                        filename,
                                        'nomads',
                                        run)     
    
    if download == True:
        print(f"Downloading GEFS0P50 {cat.upper()}...")
        
        if run < 10:
            run = f"0{run}"
        else:
            run = run
        
        _clear_old_ensemble_data(paths)
        cont = False
        if cat != 'members':
            if cat == 'mean':
                aa = 'avg'
            elif cat == 'control':
                aa = 'c00'
            else:
                aa = 'spr'
            for path in paths:
                for i in range(0, final_forecast_hour + step, step):
                    if i < 10:
                        _client.byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f00{i}",
                                                    f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f00{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{aa}.t{run}z.pgrb2a.0p50.f00{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin) 
                        
                    elif i >= 10 and i < (99 + step):
                        _client.byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f0{i}",
                                                    f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f0{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{aa}.t{run}z.pgrb2a.0p50.f0{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin)   
                        
                    elif i >= 102 and i < (240 + step):
                        _client.byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f{i}",
                                                    f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{aa}.t{run}z.pgrb2a.0p50.f{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin)    
                        
                    else:
                        cont = True
                        break
                    
                if cont == True:
                    for i in range(240, final_forecast_hour + 6, 6):
                        _client.byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f{i}",
                                                    f"{url}ge{aa}.t{run}z.pgrb2a.0p50.f{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{aa}.t{run}z.pgrb2a.0p50.f{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin) 
                else:
                    pass                                                                
                            
        else:
            aa = []
            for member in members:
                if member < 10:
                    m = f"p0{member}"
                else:
                    m = f"p{member}"
                aa.append(m)
                
            for path, a in zip(paths, aa):
                for i in range(0, final_forecast_hour + step, step):
                    if i < 10:
                        _client.byte_range_request(f"{url}ge{a}.t{run}z.pgrb2a.0p50.f00{i}",
                                                    f"{url}ge{a}.t{run}z.pgrb2a.0p50.f00{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{a}.t{run}z.pgrb2a.0p50.f00{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin) 
                        
                    elif i >= 10 and i < (99 + step):
                        _client.byte_range_request(f"{url}ge{a}.t{run}z.pgrb2a.0p50.f0{i}",
                                                    f"{url}ge{a}.t{run}z.pgrb2a.0p50.f0{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{a}.t{run}z.pgrb2a.0p50.f0{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin)   
                        
                    elif i >= 102 and i < (240 + step):
                        _client.byte_range_request(f"{url}ge{a}.t{run}z.pgrb2a.0p50.f{i}",
                                                    f"{url}ge{a}.t{run}z.pgrb2a.0p50.f{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{a}.t{run}z.pgrb2a.0p50.f{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin)    
                        
                    else:
                        cont = True
                        break
                    
                if cont == True:
                    for i in range(240, final_forecast_hour + 6, 6):
                        _client.byte_range_request(f"{url}ge{a}.t{run}z.pgrb2a.0p50.f{i}",
                                                    f"{url}ge{a}.t{run}z.pgrb2a.0p50.f{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{a}.t{run}z.pgrb2a.0p50.f{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin) 
                else:
                    pass  
                        
        print(f"GEFS0P50 {cat.upper()} Download Complete.")        
    else:
        print(f"GEFS0P50 {cat.upper()} Data is up to date. Skipping download...") 
        
    if process_data == True:
        print(f"GEFS0P50 {cat.upper()} Data Processing...")
        _clear_empty_files(paths)
        
        ds = _gefs_post_processing.primary_gefs_post_processing(paths,
                                                                western_bound,
                                                                eastern_bound,
                                                                southern_bound,
                                                                northern_bound)
            
        if convert_temperature == True:
            ds = _convert_temperature_units(ds, 
                                            convert_to,
                                            cat=cat)
                
        else:
            pass
            
        print(f"GEFS0P50 {cat.upper()} Data Processing Complete.")
        return ds
    else:
        pass

def _gefs_0p50_secondary_parameters_client(cat='mean', 
             final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=False,
             variables=['best lifted index',
                        '5 wave geopotential height',
                        'absolute vorticity',
                        'temperature',
                        'dew point',
                        'convective precipitation',
                        'albedo',
                        'apparent temperature',
                        'brightness temperature',
                        'convective available potential energy',
                        'clear sky uv-b downward solar flux',
                        'convective inhibition',
                        'cloud mixing ratio',
                        'plant canopy surface water',
                        'percent frozen precipitaion',
                        'convective precipitation rate',
                        'cloud water',
                        'cloud work function',
                        'uv-b downward solar flux',
                        'field capacity',
                        'surface friction velocity',
                        'ground heat flux',
                        'wind gust',
                        'geopotential height',
                        'haines index',
                        'storm relative helicity',
                        'planetary boundary layer height',
                        'icao standard atmosphere reference height',
                        'ice cover',
                        'icing',
                        'icing severity',
                        'land cover',
                        'surface lifted index',
                        'montgomery stream function',
                        'mslp (eta model reduction)',
                        'large scale non-convective precipitation',
                        'ozone mixing ratio',
                        'potential evaporation rate',
                        'parcel lifted index (to 500mb)',
                        'pressure level from which parcel was lifted',
                        'potential temperature',
                        'precipitation rate',
                        'pressure',
                        'potential vorticity',
                        'precipitable water',
                        'relative humidity',
                        'surface roughness',
                        'snow phase-change heat flux',
                        'snow cover',
                        'liquid volumetric soil moisture (non-frozen)',
                        'volumetric soil moisture content',
                        'specific humidity',
                        'sunshine duration',
                        'total cloud cover',
                        'total ozone',
                        'soil temperature',
                        'momentum flux (u-component)',
                        'u-component of wind',
                        'zonal flux of gravity wave stress',
                        'u-component of storm motion',
                        'upward shortwave radiation flux',
                        'momentum flux (v-component)',
                        'v-component of wind',
                        'meridional flux of gravity wave stress',
                        'visibility',
                        'ventilation rate',
                        'v-component of storm motion',
                        'vertical velocity',
                        'vertical speed shear',
                        'water runoff',
                        'wilting point'],
             convert_temperature=True,
             convert_to='celsius',
            custom_directory=None,
            chunk_size=8192,
            notifications='off',
            clear_data=False,
            source='noaa',
            level_type='pressure',
            levels=[1000,
                    925,
                    850,
                    700,
                    500,
                    400,
                    300,
                    250,
                    200,
                    100,
                    50,
                    10]):
                        
    
    """
    This function downloads the latest GEFS0P50 SECONDARY PARAMETERS data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='control'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50 SECONDARY PARAMETERS
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    7) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    9) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    12) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50 SECONDARY PARAMETERS
        ----------------------------------------------------
        
        'best lifted index'
        '5 wave geopotential height'
        'absolute vorticity'
        'temperature'
        'dew point'
        'convective precipitation'
        'albedo'
        'apparent temperature'
        'brightness temperature'
        'convective available potential energy'
        'clear sky uv-b downward solar flux'
        'convective inhibition'
        'cloud mixing ratio'
        'plant canopy surface water'
        'percent frozen precipitaion'
        'convective precipitation rate'
        'cloud water'
        'cloud work function'
        'uv-b downward solar flux'
        'field capacity'
        'surface friction velocity'
        'ground heat flux'
        'wind gust'
        'geopotential height'
        'haines index'
        'storm relative helicity'
        'planetary boundary layer height'
        'icao standard atmosphere reference height'
        'ice cover'
        'icing'
        'icing severity'
        'land cover'
        'surface lifted index'
        'montgomery stream function'
        'mslp (eta model reduction)'
        'large scale non-convective precipitation'
        'ozone mixing ratio'
        'potential evaporation rate'
        'parcel lifted index (to 500mb)'
        'pressure level from which parcel was lifted'
        'potential temperature'
        'precipitation rate'
        'pressure'
        'potential vorticity'
        'precipitable water'
        'relative humidity'
        'surface roughness'
        'snow phase-change heat flux'
        'snow cover'
        'liquid volumetric soil moisture (non-frozen)'
        'volumetric soil moisture content'
        'specific humidity'
        'sunshine duration'
        'total cloud cover'
        'total ozone'
        'soil temperature'
        'momentum flux (u-component)'
        'u-component of wind'
        'zonal flux of gravity wave stress'
        'u-component of storm motion'
        'upward shortwave radiation flux'
        'momentum flux (v-component)'
        'v-component of wind'
        'meridional flux of gravity wave stress'
        'visibility'
        'ventilation rate'
        'v-component of storm motion'
        'vertical velocity'
        'vertical speed shear'
        'water runoff'
        'wilting point'
        
    13) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.
    
    14) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    15) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    16) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    17) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
        
    18) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    19) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    20) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
    21) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    22) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'height above ground'
        'surface'
        'height below ground'
        'entire atmosphere (considered as a single layer)'
        'pressure above ground'
        
    23) levels (String, Integer or Float List) - Default=[1000,
                                                            925,
                                                            850,
                                                            700,
                                                            500,
                                                            400,
                                                            300,
                                                            250,
                                                            200,
                                                            100,
                                                            50,
                                                            10]    
                                                            
        The pressure, height or depth levels.
    
    Returns
    -------
    
    An xarray data array of the GEFS0P50 SECONDARY PARAMETERS data specified to the coordinate boundaries and variable list the user specifies. 
    
    GEFS0P50 SECONDARY PARAMETERS files are saved to f:GEFS0P50 SECONDARY PARAMETERS/{cat} or in the case of ensemble members f:GEFS0P50 SECONDARY PARAMETERS/{cat}/{member}
    
    Variables
    ---------
    
    'temperature'
    'surface_visibility'
    'surface_wind_gust'
    'haines_index'
    'plant_canopy_surface_water'
    'snow_cover'
    'percent_frozen_precipitation'
    'snow_phase_change_heat_flux'
    'surface_roughness'
    'frictional_velocity'
    'wilting_point'
    'field_capacity'
    'sunshine_duration'
    'surface_lifted_index'
    'best_4_layer_lifted_index'
    'land_sea_mask'
    'sea_ice_area_fraction'
    'orography'
    'convective_precipitation_rate'
    'precipitation_rate'
    'total_convective_precipitation'
    'total_non_convective_precipitation'
    'total_precipitation'
    'water_runoff'
    'ground_heat_flux'
    'time_mean_u_component_of_atmospheric_surface_momentum_flux'
    'time_mean_v_component_of_atmospheric_surface_momentum_flux'
    'instantaneous_eastward_gravity_wave_surface_flux'
    'instantaneous_northward_gravity_wave_surface_flux'
    'uv_b_downward_solar_flux'
    'clear_sky_uv_b_downward_solar_flux'
    'average_surface_albedo'
    'mslp'
    'mslp_eta_reduction'  
    'ventilation_rate'
    'geopotential_height'
    'vertical_velocity'
    'u_wind_component'
    'v_wind_component'
    'ozone_mixing_ratio'
    'absolute_vorticity'
    'cloud_mixing_ratio'
    'icing_severity'
    'total_cloud_cover'
    'relative_humidity'
    'liquid_volumetric_soil_moisture_non_frozen'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_specific_humidity'
    '2m_dew_point'
    '2m_apparent_temperature'
    'specific_humidity'
    'pressure'
    'cloud_water'
    'total_ozone'
    'brightness_temperature'
    '3km_helicity'
    'u_component_of_storm_motion'
    'v_component_of_storm_motion'
    'pressure'
    'tropopause_standard_atmosphere_reference_height'
    '995_sigma_theta'
    'potential_vorticity'
    'vertical_speed_shear'
    'theta_level_montgomery_potential'
    'potential_vorticity_level_vertical_speed_shear'
    'mixed_layer_dew_point'
    'mixed_layer_precipitable_water'
    'parcel_lifted_index_to_500hPa'
    'convective_available_potential_energy'
    'convective_inhibition'
    'pressure_level_from_which_a_parcel_was_lifted'
       
    """
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    cat = cat.lower()
    
    if custom_directory == None:
        paths = _build_directory('gefs0p50 secondary parameters', 
                                cat, 
                                members)

        _clear_idx_files('gefs0p50 secondary parameters', 
                        cat, 
                        members)
        
    else:
        if cat == 'members':
            paths = _custom_branches(custom_directory)
            
        else:
            paths = _custom_branch(custom_directory)
        
        _clear_gefs_idx_files(paths)
        
    if clear_data == True:
        _clear_old_ensemble_data(paths)
    else:
        pass
    
    if source == 'noaa':
        try:
            url, filename, run = _gefs_0p50_secondary_parameters_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    source)
        except Exception as e:
            filename = None
            
        if filename == None:
            print("NCEP/NOMADS Server Is Down.")
            print("Rotating to Amazon AWS Server.")
            try:
                url, filename, run = _gefs_0p50_secondary_parameters_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'aws')
                print("Amazon AWS Server Online - Connected.")
            except Exception as e:
                filename = None
                
            if filename == None:
                print("Amazon AWS Server Is Down.")
                print("Rotating to Google Cloud Server.")
                try:
                    url, filename, run = _gefs_0p50_secondary_parameters_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'google')
                    print("Google Cloud Server Online - Connected.")
                except Exception as e:
                    print("Error: All Servers Appear Down.")
                    print("System Exit")
                    _sys.exit(1)
            else:
                pass
        
        else:
            pass
        
    if source == 'aws':
        try:
            url, filename, run = _gefs_0p50_secondary_parameters_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    source)
        except Exception as e:
            filename = None
            
        if filename == None:
            print("NCEP/NOMADS Server Is Down.")
            print("Rotating to NCEP/NOMADS Server.")
            try:
                url, filename, run = _gefs_0p50_secondary_parameters_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'noaa')
                print("NCEP/NOMADS Server Online - Connected.")
            except Exception as e:
                filename = None
                
            if filename == None:
                print("Amazon NCEP/NOMADS Is Down.")
                print("Rotating to Google Cloud Server.")
                try:
                    url, filename, run = _gefs_0p50_secondary_parameters_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'google')
                    print("Google Cloud Server Online - Connected.")
                except Exception as e:
                    print("Error: All Servers Appear Down.")
                    print("System Exit")
                    _sys.exit(1)
            else:
                pass
        
        else:
            pass
        
    
    if source == 'google':
        try:
            url, filename, run = _gefs_0p50_secondary_parameters_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    source)
        except Exception as e:
            filename = None
            
        if filename == None:
            print("Google Cloud Server Is Down.")
            print("Rotating to NCEP/NOMADS Server.")
            try:
                url, filename, run = _gefs_0p50_secondary_parameters_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'noaa')
                print("Google Cloud Server Online - Connected.")
            except Exception as e:
                filename = None
                
            if filename == None:
                print("Amazon NCEP/NOMADS Is Down.")
                print("Rotating to Amazon AWS Server.")
                try:
                    url, filename, run = _gefs_0p50_secondary_parameters_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'aws')
                    print("Amazon AWS Server Online - Connected.")
                except Exception as e:
                    print("Error: All Servers Appear Down.")
                    print("System Exit")
                    _sys.exit(1)
            else:
                pass
        
        else:
            pass   
    
    download = _local_file_scanner(paths[-1], 
                                        filename,
                                        'nomads',
                                        run)     
    
    if download == True:
        print(f"Downloading GEFS0P50 {cat.upper()}...")
        
        if run < 10:
            run = f"0{run}"
        else:
            run = run
        
        _clear_old_ensemble_data(paths)
        cont = False
        if cat == 'control':
            aa = 'c00'
            for path in paths:
                for i in range(0, final_forecast_hour + step, step):
                    if i < 10:
                        _client.byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f00{i}",
                                                    f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f00{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{aa}.t{run}z.pgrb2b.0p50.f00{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin) 
                        
                    elif i >= 10 and i < (99 + step):
                        _client.byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f0{i}",
                                                    f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f0{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{aa}.t{run}z.pgrb2b.0p50.f0{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin)   
                        
                    elif i >= 102 and i < (240 + step):
                        _client.byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f{i}",
                                                    f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{aa}.t{run}z.pgrb2b.0p50.f{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin)    
                        
                    else:
                        cont = True
                        break
                    
                if cont == True:
                    for i in range(240, final_forecast_hour + 6, 6):
                        _client.byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f{i}",
                                                    f"{url}ge{aa}.t{run}z.pgrb2b.0p50.f{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{aa}.t{run}z.pgrb2b.0p50.f{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin) 
                else:
                    pass                                                                
                            
        else:
            aa = []
            for member in members:
                if member < 10:
                    m = f"p0{member}"
                else:
                    m = f"p{member}"
                aa.append(m)
                
            for path, a in zip(paths, aa):
                for i in range(0, final_forecast_hour + step, step):
                    if i < 10:
                        _client.byte_range_request(f"{url}ge{a}.t{run}z.pgrb2b.0p50.f00{i}",
                                                    f"{url}ge{a}.t{run}z.pgrb2b.0p50.f00{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{a}.t{run}z.pgrb2b.0p50.f00{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin) 
                        
                    elif i >= 10 and i < (99 + step):
                        _client.byte_range_request(f"{url}ge{a}.t{run}z.pgrb2b.0p50.f0{i}",
                                                    f"{url}ge{a}.t{run}z.pgrb2b.0p50.f0{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{a}.t{run}z.pgrb2b.0p50.f0{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin)   
                        
                    elif i >= 102 and i < (240 + step):
                        _client.byte_range_request(f"{url}ge{a}.t{run}z.pgrb2b.0p50.f{i}",
                                                    f"{url}ge{a}.t{run}z.pgrb2b.0p50.f{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{a}.t{run}z.pgrb2b.0p50.f{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin)    
                        
                    else:
                        cont = True
                        break
                    
                if cont == True:
                    for i in range(240, final_forecast_hour + 6, 6):
                        _client.byte_range_request(f"{url}ge{a}.t{run}z.pgrb2b.0p50.f{i}",
                                                    f"{url}ge{a}.t{run}z.pgrb2b.0p50.f{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{a}.t{run}z.pgrb2b.0p50.f{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin) 
                else:
                    pass  
                           
        print(f"GEFS0P50 {cat.upper()} Secondary Parameters Download Complete.")        
    else:
        print(f"GEFS0P50 {cat.upper()} Secondary Parameters Data is up to date. Skipping download...") 
    
    if process_data == True:
        print(f"GEFS0P50 {cat.upper()} Secondary Parameters Data Processing...")
        
        ds = _gefs_post_processing.secondary_gefs_post_processing(paths,
                                                                  western_bound,
                                                                  eastern_bound,
                                                                  southern_bound,
                                                                  northern_bound)
                    
        if convert_temperature == True:
            ds = _convert_temperature_units(ds, 
                                           convert_to, 
                                           cat=cat)
                
        
        print(f"GEFS0P50 {cat.upper()} Secondary Parameters Data Processing Complete.")
        return ds
    else:
        pass
    
def _gefs_0p25_client(cat='mean', 
             final_forecast_hour=240, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=False,
             variables=['total precipitation',
                        'convective available potential energy',
                        'categorical freezing rain',
                        'categorical ice pellets',
                        'convective inhibition',
                        'percent frozen precipitaion',
                        'categorical rain',
                        'categorical snow',
                        'downward longwave radiation flux',
                        'downward shortwave radiation flux',
                        'dew point',
                        'wind gust',
                        'geopotential height',
                        'storm relative helicity',
                        'ice thickness',
                        'latent heat net flux',
                        'pressure',
                        'mean sea level pressure',
                        'precipitable water',
                        'relative humidity',
                        'sensible heat net flux',
                        'snow depth',
                        'volumetric soil moisture content',
                        'total cloud cover',
                        'maximum temperature',
                        'minimum temperature',
                        'temperature',
                        'soil temperature',
                        'u-component of wind',
                        'upward longwave radiation flux',
                        'upward shortwave radiation flux',
                        'v-component of wind',
                        'visibility',
                        'water equivalent of accumulated snow depth'],
             convert_temperature=True,
             convert_to='celsius',
             custom_directory=None,
             chunk_size=8192,
             notifications='off',
             clear_data=False,
            source='noaa',
            level_type='pressure',
            levels=[1000,
                    925,
                    850,
                    700,
                    500,
                    400,
                    300,
                    250,
                    200,
                    100,
                    50,
                    10]):
    
    """
    This function downloads the latest GEFS0P25 data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='mean'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - Default = 240. The final forecast hour the user wishes to download. The GEFS0P25
    goes out to 240 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    240 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    8) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 
    
    9) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    12) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P25
        -------------------------------
        
        'total precipitation'
        'convective available potential energy'
        'categorical freezing rain'
        'categorical ice pellets'
        'convective inhibition'
        'percent frozen precipitaion'
        'categorical rain'
        'categorical snow'
        'downward longwave radiation flux'
        'downward shortwave radiation flux'
        'dew point'
        'wind gust'
        'geopotential height'
        'storm relative helicity'
        'ice thickness'
        'latent heat net flux'
        'pressure'
        'mean sea level pressure'
        'precipitable water'
        'relative humidity'
        'sensible heat net flux'
        'snow depth'
        'volumetric soil moisture content'
        'total cloud cover'
        'maximum temperature'
        'minimum temperature'
        'temperature'
        'soil temperature'
        'u-component of wind'
        'upward longwave radiation flux'
        'upward shortwave radiation flux'
        'v-component of wind'
        'visibility'
        'water equivalent of accumulated snow depth'
        
    13) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.
    
    14) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    15) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    16) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    17) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
        
    18) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    19) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    20) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
    21) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    22) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'height above ground'
        'surface'
        'height below ground'
        'entire atmosphere (considered as a single layer)'
        'pressure above ground'
        
    23) levels (String, Integer or Float List) - Default=[1000,
                                                            925,
                                                            850,
                                                            700,
                                                            500,
                                                            400,
                                                            300,
                                                            250,
                                                            200,
                                                            100,
                                                            50,
                                                            10]    
                                                            
        The pressure, height or depth levels.
    
    Returns
    -------
    
    An xarray data array of the GEFS0P25 data specified to the coordinate boundaries and variable list the user specifies. 
    
    GEFS0P25 files are saved to f:GEFS0P25/{cat} or in the case of ensemble members f:GEFS0P25/{cat}/{member}
    
    Variables
    ---------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'surface_visibility'
    'surface_wind_gust'
    'percent_frozen_precipitation'
    'convective_available_potential_energy'
    'convective_inhibition'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    '2m_dew_point'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'mixed_layer_cape'
    'mixed_layer_cin'
    '3km_helicity'
    
    """
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass    
    
    cat = cat.lower()
    
    if custom_directory == None:
        paths = _build_directory('gefs0p25', 
                                cat, 
                                members)

        _clear_idx_files('gefs0p25', 
                        cat, 
                        members)
        
    else:
        if cat == 'members':
            paths = _custom_branches(custom_directory)
            
        else:
            paths = _custom_branch(custom_directory)
        
        _clear_gefs_idx_files(paths)
        
    if clear_data == True:
        _clear_old_ensemble_data(paths)
    else:
        pass
    
    if source == 'noaa':
        try:
            url, filename, run = _gefs_0p25_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    source)
        except Exception as e:
            filename = None
            
        if filename == None:
            print("NCEP/NOMADS Server Is Down.")
            print("Rotating to Amazon AWS Server.")
            try:
                url, filename, run = _gefs_0p25_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'aws')
                print("Amazon AWS Server Online - Connected.")
            except Exception as e:
                filename = None
                
            if filename == None:
                print("Amazon AWS Server Is Down.")
                print("Rotating to Google Cloud Server.")
                try:
                    url, filename, run = _gefs_0p25_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'google')
                    print("Google Cloud Server Online - Connected.")
                except Exception as e:
                    print("Error: All Servers Appear Down.")
                    print("System Exit")
                    _sys.exit(1)
            else:
                pass
        
        else:
            pass
        
    if source == 'aws':
        try:
            url, filename, run = _gefs_0p25_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    source)
        except Exception as e:
            filename = None
            
        if filename == None:
            print("NCEP/NOMADS Server Is Down.")
            print("Rotating to NCEP/NOMADS Server.")
            try:
                url, filename, run = _gefs_0p25_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'noaa')
                print("NCEP/NOMADS Server Online - Connected.")
            except Exception as e:
                filename = None
                
            if filename == None:
                print("Amazon NCEP/NOMADS Is Down.")
                print("Rotating to Google Cloud Server.")
                try:
                    url, filename, run = _gefs_0p25_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'google')
                    print("Google Cloud Server Online - Connected.")
                except Exception as e:
                    print("Error: All Servers Appear Down.")
                    print("System Exit")
                    _sys.exit(1)
            else:
                pass
        
        else:
            pass
        
    
    if source == 'google':
        try:
            url, filename, run = _gefs_0p25_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    source)
        except Exception as e:
            filename = None
            
        if filename == None:
            print("Google Cloud Server Is Down.")
            print("Rotating to NCEP/NOMADS Server.")
            try:
                url, filename, run = _gefs_0p25_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'noaa')
                print("Google Cloud Server Online - Connected.")
            except Exception as e:
                filename = None
                
            if filename == None:
                print("Amazon NCEP/NOMADS Is Down.")
                print("Rotating to Amazon AWS Server.")
                try:
                    url, filename, run = _gefs_0p25_url_scanner(cat, 
                                                    final_forecast_hour,
                                                    proxies, 
                                                    members,
                                                    'aws')
                    print("Amazon AWS Server Online - Connected.")
                except Exception as e:
                    print("Error: All Servers Appear Down.")
                    print("System Exit")
                    _sys.exit(1)
            else:
                pass
        
        else:
            pass   
    
    download = _local_file_scanner(paths[-1], 
                                        filename,
                                        'nomads',
                                        run)     
    
    if download == True:
        print(f"Downloading GEFS0P25 {cat.upper()}...")
        
        if run < 10:
            run = f"0{run}"
        else:
            run = run

        _clear_old_ensemble_data(paths)
        
        cont = False
        if cat != 'members':
            if cat == 'mean':
                aa = 'avg'
            elif cat == 'control':
                aa = 'c00'
            else:
                aa = 'spr'
            for path in paths:
                for i in range(0, final_forecast_hour + step, step):
                    if i < 10:
                        _client.byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f00{i}",
                                                    f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f00{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{aa}.t{run}z.pgrb2s.0p25.f00{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin) 
                        
                    elif i >= 10 and i < (99 + step):
                        _client.byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f0{i}",
                                                    f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f0{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{aa}.t{run}z.pgrb2s.0p25.f0{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin)   
                        
                    elif i >= 102 and i < (240 + step):
                        _client.byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f{i}",
                                                    f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{aa}.t{run}z.pgrb2s.0p25.f{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin)    
                        
                    else:
                        cont = True
                        break
                    
                if cont == True:
                    for i in range(240, final_forecast_hour + 6, 6):
                        _client.byte_range_request(f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f{i}",
                                                    f"{url}ge{aa}.t{run}z.pgrb2s.0p25.f{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{aa}.t{run}z.pgrb2s.0p25.f{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin) 
                else:
                    pass                                                                
                            
        else:
            aa = []
            for member in members:
                if member < 10:
                    m = f"p0{member}"
                else:
                    m = f"p{member}"
                aa.append(m)
                
            for path, a in zip(paths, aa):
                for i in range(0, final_forecast_hour + step, step):
                    if i < 10:
                        _client.byte_range_request(f"{url}ge{a}.t{run}z.pgrb2s.0p25.f00{i}",
                                                    f"{url}ge{a}.t{run}z.pgrb2s.0p25.f00{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{a}.t{run}z.pgrb2s.0p25.f00{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin) 
                        
                    elif i >= 10 and i < (99 + step):
                        _client.byte_range_request(f"{url}ge{a}.t{run}z.pgrb2s.0p25.f0{i}",
                                                    f"{url}ge{a}.t{run}z.pgrb2s.0p25.f0{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{a}.t{run}z.pgrb2s.0p25.f0{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin)   
                        
                    elif i >= 102 and i < (240 + step):
                        _client.byte_range_request(f"{url}ge{a}.t{run}z.pgrb2s.0p25.f{i}",
                                                    f"{url}ge{a}.t{run}z.pgrb2s.0p25.f{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{a}.t{run}z.pgrb2s.0p25.f{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin)    
                        
                    else:
                        cont = True
                        break
                    
                if cont == True:
                    for i in range(240, final_forecast_hour + 6, 6):
                        _client.byte_range_request(f"{url}ge{a}.t{run}z.pgrb2s.0p25.f{i}",
                                                    f"{url}ge{a}.t{run}z.pgrb2s.0p25.f{i}.idx",
                                                    variables,
                                                    levels,
                                                    level_type,
                                                    path,
                                                    f"ge{a}.t{run}z.pgrb2s.0p25.f{i}.grib2",
                                                    proxies=proxies,
                                                    chunk_size=chunk_size,
                                                    notifications=notifications,
                                                    clear_recycle_bin=clear_recycle_bin) 
                else:
                    pass     
        print(f"GEFS0P25 {cat.upper()} Download Complete.")        
    else:
        print(f"GEFS0P25 {cat.upper()} Data is up to date. Skipping download...") 
        
    if process_data == True:
        print(f"GEFS0P25 {cat.upper()} Data Processing...")
        
        _clear_empty_files(paths)
        
        ds = _gefs_post_processing.primary_gefs_post_processing(paths,
                                                                western_bound,
                                                                eastern_bound,
                                                                southern_bound,
                                                                northern_bound)
                    
        if convert_temperature == True:
            ds = _convert_temperature_units(ds, 
                                           convert_to,
                                           cat=cat)
            
        
        print(f"GEFS0P25 {cat.upper()} Data Processing Complete.")
        return ds
    else:
        pass
    
        

    
    
def gefs_0p50(cat='mean', 
             final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=False,
             variables=['geopotential height'],
            convert_temperature=True,
            convert_to='celsius',
            custom_directory=None,
            chunk_size=8192,
            notifications='off',
            clear_data=False,
            source='noaa',
            level_type='pressure',
            levels=[1000,
                    925,
                    850,
                    700,
                    500,
                    400,
                    300,
                    250,
                    200,
                    100,
                    50,
                    10]):
    
    """
    This function downloads the latest GEFS0P50 data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='mean'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    7) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    9) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    12) variables (List) - Default=['geopotential height'].
    
        A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50
        -------------------------------
        
			'total precipitation'
            'convective available potential energy'
            'categorical freezing rain'
            'categorical ice pellets'
            'categorical rain'
            'categorical snow'
            'convective inhibition'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'geopotential height'
            'ice thickness'
            'latent heat net flux'
            'pressure'
            'mean sea level pressure'
            'precipitable water'
            'relative humidity'
            'sensible heat net flux'
            'snow depth'
            'volumetric soil moisture content'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'soil temperature'
            'u-component of wind'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'v-component of wind'
            'vertical velocity'
            'water equivalent of accumulated snow depth'
            
    13) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.
    
    14) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    15) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    16) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    17) custom_directory (String or None) - Default=None. The directory path where the GEFS0P50 files will be saved to.
        
    18) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    19) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    20) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
    21) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    22) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'height below ground'
        'surface'
        'height above ground'
        'top of atmosphere'
        'pressure above ground'
        'mean sea level'
        
        
        
    23) levels (String, Integer or Float List) - Default==[1000,
                                                            925,
                                                            850,
                                                            700,
                                                            500,
                                                            400,
                                                            300,
                                                            250,
                                                            200,
                                                            100,
                                                            50,
                                                            10]  
                                                            
        The pressure, height or depth levels.
    
    Returns
    -------
    
    An xarray data array of the GEFS0P50 data specified to the coordinate boundaries and variable list the user specifies. 
    
    GEFS0P50 files are saved to f:GEFS0P50/{cat} or in the case of ensemble members f:GEFS0P50/{cat}/{member}
    
    Variables
    ---------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'convective_available_potential_energy'
    'convective_inhibition'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'u_wind_component'
    'v_wind_component'
    
    """
    
    source = source.lower()
    
    try:
        ds = _gefs_0p50_client(cat=cat, 
             final_forecast_hour=final_forecast_hour, 
             western_bound=western_bound, 
             eastern_bound=eastern_bound, 
             northern_bound=northern_bound, 
             southern_bound=southern_bound, 
             proxies=proxies, 
             step=step, 
             members=members,
             process_data=process_data,
             clear_recycle_bin=clear_recycle_bin,
             variables=variables,
            convert_temperature=convert_temperature,
            convert_to=convert_to,
            custom_directory=custom_directory,
            chunk_size=chunk_size,
            notifications=notifications,
            clear_data=clear_data,
            source=source,
            level_type=level_type,
            levels=levels)
        
        rotate = False
    except Exception as e:
        rotate = True
        
    if rotate == True:
        if source == 'noaa':
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to Amazon AWS Server.")
            
            try:
                ds = _gefs_0p50_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='aws',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                rotate = True
                
        if source == 'aws':
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to NOAA/NCEP/NOMADS Server.")
            
            try:
                ds = _gefs_0p50_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='noaa',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                rotate = True
                
        else:
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to NOAA/NCEP/NOMADS Server.")
            
            try:
                ds = _gefs_0p50_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='noaa',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                rotate = True
    
    else:
        pass
    
    if rotate == True:
        if source == 'noaa':
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to Google Cloud Server.")
            
            try:
                ds = _gefs_0p50_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='google',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                rotate = True
                
        if source == 'aws':
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to Google Cloud Server.")
            
            try:
                ds = _gefs_0p50_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='google',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                rotate = True
                
        else:
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to Amazon AWS Server.")
            
            try:
                ds = _gefs_0p50_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='aws',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                print("Client cannot connect to any server.")
                print("System Exit.")
                _sys.exit(1)
    
    else:
        pass
    
    return ds


def gefs_0p50_secondary_parameters(cat='control', 
             final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=False,
             variables=['pressure'],
             convert_temperature=True,
             convert_to='celsius',
            custom_directory=None,
            chunk_size=8192,
            notifications='off',
            clear_data=False,
            source='noaa',
            level_type='mean sea level',
            levels=None):
                        
    
    """
    This function downloads the latest GEFS0P50 SECONDARY PARAMETERS data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='control'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50 SECONDARY PARAMETERS
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    7) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    9) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    12) variables (List) - Default=['pressure']. A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50 SECONDARY PARAMETERS
        ----------------------------------------------------
        
        'best lifted index'
        '5 wave geopotential height'
        'absolute vorticity'
        'temperature'
        'dew point'
        'convective precipitation'
        'albedo'
        'apparent temperature'
        'brightness temperature'
        'convective available potential energy'
        'clear sky uv-b downward solar flux'
        'convective inhibition'
        'cloud mixing ratio'
        'plant canopy surface water'
        'percent frozen precipitaion'
        'convective precipitation rate'
        'cloud water'
        'cloud work function'
        'uv-b downward solar flux'
        'field capacity'
        'surface friction velocity'
        'ground heat flux'
        'wind gust'
        'geopotential height'
        'haines index'
        'storm relative helicity'
        'planetary boundary layer height'
        'icao standard atmosphere reference height'
        'ice cover'
        'icing'
        'icing severity'
        'land cover'
        'surface lifted index'
        'montgomery stream function'
        'mslp (eta model reduction)'
        'large scale non-convective precipitation'
        'ozone mixing ratio'
        'potential evaporation rate'
        'parcel lifted index (to 500mb)'
        'pressure level from which parcel was lifted'
        'potential temperature'
        'precipitation rate'
        'pressure'
        'potential vorticity'
        'precipitable water'
        'relative humidity'
        'surface roughness'
        'snow phase-change heat flux'
        'snow cover'
        'liquid volumetric soil moisture (non-frozen)'
        'volumetric soil moisture content'
        'specific humidity'
        'sunshine duration'
        'total cloud cover'
        'total ozone'
        'soil temperature'
        'momentum flux (u-component)'
        'u-component of wind'
        'zonal flux of gravity wave stress'
        'u-component of storm motion'
        'upward shortwave radiation flux'
        'momentum flux (v-component)'
        'v-component of wind'
        'meridional flux of gravity wave stress'
        'visibility'
        'ventilation rate'
        'v-component of storm motion'
        'vertical velocity'
        'vertical speed shear'
        'water runoff'
        'wilting point'
        
    13) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.
    
    14) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    15) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    16) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    17) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
        
    18) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    19) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    20) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
    21) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    22) level_type (String) - Default='mean sea level'. The type of level for the variable.
    
        Level Types
        -----------
        
        'mean sea level'
        'hybrid'
        'surface'
        'boundary layer'
        'pressure'
        'height below ground'
        'height above ground'
        'entire atmosphere (considered as a single layer)'
        'cloud ceiling'
        'top of atmosphere'
        'tropopause'
        'max wind'
        'height above sea level'
        'isothermal'
        'highest tropospheric freezing level'
        'sigma layer'
        'sigma level'
        'isentropic level'
        'potential vorticity surface'
        
    23) levels (String, Integer or Float List or None) - Default=None. 
                                                            
        The pressure, height or depth levels. Set to None when the level_type only has one level (i.e. 'surface').
    
    Returns
    -------
    
    An xarray data array of the GEFS0P50 SECONDARY PARAMETERS data specified to the coordinate boundaries and variable list the user specifies. 
    
    GEFS0P50 SECONDARY PARAMETERS files are saved to f:GEFS0P50 SECONDARY PARAMETERS/{cat} or in the case of ensemble members f:GEFS0P50 SECONDARY PARAMETERS/{cat}/{member}
    
    Variables
    ---------
    
    'temperature'
    'surface_visibility'
    'surface_wind_gust'
    'haines_index'
    'plant_canopy_surface_water'
    'snow_cover'
    'percent_frozen_precipitation'
    'snow_phase_change_heat_flux'
    'surface_roughness'
    'frictional_velocity'
    'wilting_point'
    'field_capacity'
    'sunshine_duration'
    'surface_lifted_index'
    'best_4_layer_lifted_index'
    'land_sea_mask'
    'sea_ice_area_fraction'
    'orography'
    'convective_precipitation_rate'
    'precipitation_rate'
    'total_convective_precipitation'
    'total_non_convective_precipitation'
    'total_precipitation'
    'water_runoff'
    'ground_heat_flux'
    'time_mean_u_component_of_atmospheric_surface_momentum_flux'
    'time_mean_v_component_of_atmospheric_surface_momentum_flux'
    'instantaneous_eastward_gravity_wave_surface_flux'
    'instantaneous_northward_gravity_wave_surface_flux'
    'uv_b_downward_solar_flux'
    'clear_sky_uv_b_downward_solar_flux'
    'average_surface_albedo'
    'mslp'
    'mslp_eta_reduction'  
    'ventilation_rate'
    'geopotential_height'
    'vertical_velocity'
    'u_wind_component'
    'v_wind_component'
    'ozone_mixing_ratio'
    'absolute_vorticity'
    'cloud_mixing_ratio'
    'icing_severity'
    'total_cloud_cover'
    'relative_humidity'
    'liquid_volumetric_soil_moisture_non_frozen'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_specific_humidity'
    '2m_dew_point'
    '2m_apparent_temperature'
    'specific_humidity'
    'pressure'
    'cloud_water'
    'total_ozone'
    'brightness_temperature'
    '3km_helicity'
    'u_component_of_storm_motion'
    'v_component_of_storm_motion'
    'pressure'
    'tropopause_standard_atmosphere_reference_height'
    '995_sigma_theta'
    'potential_vorticity'
    'vertical_speed_shear'
    'theta_level_montgomery_potential'
    'potential_vorticity_level_vertical_speed_shear'
    'mixed_layer_dew_point'
    'mixed_layer_precipitable_water'
    'parcel_lifted_index_to_500hPa'
    'convective_available_potential_energy'
    'convective_inhibition'
    'pressure_level_from_which_a_parcel_was_lifted'
       
    """
    
    source = source.lower()
    
    try:
        ds = _gefs_0p50_secondary_parameters_client(cat=cat, 
             final_forecast_hour=final_forecast_hour, 
             western_bound=western_bound, 
             eastern_bound=eastern_bound, 
             northern_bound=northern_bound, 
             southern_bound=southern_bound, 
             proxies=proxies, 
             step=step, 
             members=members,
             process_data=process_data,
             clear_recycle_bin=clear_recycle_bin,
             variables=variables,
            convert_temperature=convert_temperature,
            convert_to=convert_to,
            custom_directory=custom_directory,
            chunk_size=chunk_size,
            notifications=notifications,
            clear_data=clear_data,
            source=source,
            level_type=level_type,
            levels=levels)
        
        rotate = False
    except Exception as e:
        rotate = True
        
    if rotate == True:
        if source == 'noaa':
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to Amazon AWS Server.")
            
            try:
                ds = _gefs_0p50_secondary_parameters_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='aws',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                rotate = True
                
        if source == 'aws':
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to NOAA/NCEP/NOMADS Server.")
            
            try:
                ds = _gefs_0p50_secondary_parameters_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='noaa',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                rotate = True
                
        else:
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to NOAA/NCEP/NOMADS Server.")
            
            try:
                ds = _gefs_0p50_secondary_parameters_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='noaa',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                rotate = True
    
    else:
        pass
    
    if rotate == True:
        if source == 'noaa':
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to Google Cloud Server.")
            
            try:
                ds = _gefs_0p50_secondary_parameters_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='google',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                rotate = True
                
        if source == 'aws':
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to Google Cloud Server.")
            
            try:
                ds = _gefs_0p50_secondary_parameters_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='google',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                rotate = True
                
        else:
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to Amazon AWS Server.")
            
            try:
                ds = _gefs_0p50_secondary_parameters_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='aws',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                print("Client cannot connect to any server.")
                print("System Exit.")
                _sys.exit(1)
    
    else:
        pass
    
    return ds


def gefs_0p25(cat='mean', 
             final_forecast_hour=240, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=False,
             variables=['temperature'],
             convert_temperature=True,
             convert_to='celsius',
             custom_directory=None,
             chunk_size=8192,
             notifications='off',
             clear_data=False,
            source='noaa',
            level_type='height above ground',
            levels=[2]):
    
    """
    This function downloads the latest GEFS0P25 data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='mean'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - Default = 240. The final forecast hour the user wishes to download. The GEFS0P25
    goes out to 240 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    240 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    8) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 
    
    9) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    12) variables (List) - Default=['temperature']. A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P25
        -------------------------------
        
        'total precipitation'
        'convective available potential energy'
        'categorical freezing rain'
        'categorical ice pellets'
        'convective inhibition'
        'percent frozen precipitaion'
        'categorical rain'
        'categorical snow'
        'downward longwave radiation flux'
        'downward shortwave radiation flux'
        'dew point'
        'wind gust'
        'geopotential height'
        'storm relative helicity'
        'ice thickness'
        'latent heat net flux'
        'pressure'
        'mean sea level pressure'
        'precipitable water'
        'relative humidity'
        'sensible heat net flux'
        'snow depth'
        'volumetric soil moisture content'
        'total cloud cover'
        'maximum temperature'
        'minimum temperature'
        'temperature'
        'soil temperature'
        'u-component of wind'
        'upward longwave radiation flux'
        'upward shortwave radiation flux'
        'v-component of wind'
        'visibility'
        'water equivalent of accumulated snow depth'
        
    13) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.
    
    14) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    15) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    16) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    17) custom_directory (String or None) - Default=None. The directory path where the GEFS0P25 files will be saved to.
        
    18) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    19) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    20) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
    21) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    22) level_type (String) - Default='height above ground'. The type of level for the variable.
    
        Level Types
        -----------
        
        'surface'
        'mean sea level'
        'height above ground'
        'height below ground'
        'entire atmosphere (considered as a single layer)'
        'cloud ceiling'
        'pressure above ground'
        
    23) levels (String, Integer or Float List) - Default=[2] 
                                                            
        The pressure, height or depth levels.
    
    
    Returns
    -------
    
    An xarray data array of the GEFS0P25 data specified to the coordinate boundaries and variable list the user specifies. 
    
    GEFS0P25 files are saved to f:GEFS0P25/{cat} or in the case of ensemble members f:GEFS0P25/{cat}/{member}
    
    Variables
    ---------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'surface_visibility'
    'surface_wind_gust'
    'percent_frozen_precipitation'
    'convective_available_potential_energy'
    'convective_inhibition'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    '2m_dew_point'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'mixed_layer_cape'
    'mixed_layer_cin'
    '3km_helicity'
    
    """
    
    if final_forecast_hour > 240:
        final_forecast_hour = 240
    
    try:
        ds = _gefs_0p25_client(cat=cat, 
             final_forecast_hour=final_forecast_hour, 
             western_bound=western_bound, 
             eastern_bound=eastern_bound, 
             northern_bound=northern_bound, 
             southern_bound=southern_bound, 
             proxies=proxies, 
             step=step, 
             members=members,
             process_data=process_data,
             clear_recycle_bin=clear_recycle_bin,
             variables=variables,
            convert_temperature=convert_temperature,
            convert_to=convert_to,
            custom_directory=custom_directory,
            chunk_size=chunk_size,
            notifications=notifications,
            clear_data=clear_data,
            source=source,
            level_type=level_type,
            levels=levels)
        
        rotate = False
    except Exception as e:
        rotate = True
        
    if rotate == True:
        if source == 'noaa':
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to Amazon AWS Server.")
            
            try:
                ds = _gefs_0p25_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='aws',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                rotate = True
                
        if source == 'aws':
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to NOAA/NCEP/NOMADS Server.")
            
            try:
                ds = _gefs_0p25_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='noaa',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                rotate = True
                
        else:
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to NOAA/NCEP/NOMADS Server.")
            
            try:
                ds = _gefs_0p25_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='noaa',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                rotate = True
    
    else:
        pass
    
    if rotate == True:
        if source == 'noaa':
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to Google Cloud Server.")
            
            try:
                ds = _gefs_0p25_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='google',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                rotate = True
                
        if source == 'aws':
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to Google Cloud Server.")
            
            try:
                ds = _gefs_0p25_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='google',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                rotate = True
                
        else:
            print("Error: Corrupted File Cannot Process.")
            print("Clearing Out Data.")
            print("Rotating to Amazon AWS Server.")
            
            try:
                ds = _gefs_0p25_client(cat=cat, 
                                    final_forecast_hour=final_forecast_hour, 
                                    western_bound=western_bound, 
                                    eastern_bound=eastern_bound, 
                                    northern_bound=northern_bound, 
                                    southern_bound=southern_bound, 
                                    proxies=proxies, 
                                    step=step, 
                                    members=members,
                                    process_data=process_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    variables=variables,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    custom_directory=custom_directory,
                                    chunk_size=chunk_size,
                                    notifications=notifications,
                                    clear_data=clear_data,
                                    source='aws',
                                    level_type=level_type,
                                    levels=levels)
                rotate = False
            except Exception as e:
                print("Client cannot connect to any server.")
                print("System Exit.")
                _sys.exit(1)
    
    else:
        pass
    
    return ds