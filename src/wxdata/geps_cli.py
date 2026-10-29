"""
This file hosts the WxData Command Line Interface for retrieving Canadian Global Ensemle Prediction System (GEPS) Data.

Command Line Use: `wxdata-geps **args`

(C) Eric J. Drewitz 2025-2026
"""
import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()

from wxdata.model_data.cmc.geps.geps import geps as _fetch_geps

def _command_error_message(model):
    
    """Error Message For Invalid Commands"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"Model: {model.upper()}")
    print(f"Please run `wxdata-geps -h to view the help documentation.")
    print(f"Please visit: https://edrewitz.github.io/WxData/GEPS%20CLI for full detailed documentation.")

def _parse_proxy(value):
    if value is None:
        return None

    else:
        # Accept either http://host:port or https://host:port
        return {
            "http": value,
            "https": value,
        }
        
# ---------------------------------------------------------------------
# Top-level CLI group
# ---------------------------------------------------------------------
@_click.group(context_settings={"help_option_names": ["-h", "--help"]})
def geps_data():
    """GEPS command line utilities."""
    pass

# ---------------------------------------------------------------------
# GEPS Commands
# ---------------------------------------------------------------------
@geps_data.group(name='fetch')
def fetch_geps_data():
    
    r"""
    
    Canadian Global Ensemble Prediction System (GEPS) Command Line Interface
    
    ***Valid Commands***
    
    -f = Final Forecast Hour. Default=384.
    
    -cr = Clear Recycle Bin (Default=False).
    
    For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
    Setting -cr True clears your recycle bin with each run of the script. 
    This ensures if any old files are moved to the recycle bin are deleted if they are not already.
    
    -cd = Clear Data (Default=False).
    
    When set to False the scanner safeguard that prevents repetative downloads is enabled.
    Set -cd False to disable this safety feature.
    
    WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
    being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
    retry downloading the data.  
    
    -cdir = Custom Directory (Default=None).
    
    If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.

    -ct = Convert Temperature (Default=True).
    
    When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.
    
    -tu = Temperature Units (Default=Celsius).
    
    When -ct True this is where you declare the units for temperature to be converted to. 
    
    -wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)
    
    -eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)
    
    -nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)
    
    -sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)
    
    -v = Variable. Variable to pass into the function. 
        
        Default='geopotential_height'
        
        ***Variables & Proper level_type & level***
    
        Any area where valid_levels = None -> Users do not need to edit the optional argument `level`
        
        'temperature': 
            valid level type(s) = 'pressure', 'height above ground'.
            valid levels:
                level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                    
                level_type='height above ground' (m): 2, 40, 80, 120
            
        'cape':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
            
        'cin':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)  
                
        'downward longwave radiation flux':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level) 
            
        'downward shortwave radiation flux':
            valid level type(s): 'surface', 'nominal top'
            valid levels: None (level_type='surface' -> 'surface' is the only level) 
                                                    OR 
                            (level_type='nominal top' -> 'nominal top' is the only level)              
                            
        'geopotential height':
            valid level type(s) = 'pressure'.
            valid levels:
                level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10. 
                                                    
        'ice pellets accumulation':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)   
            
        'total convective precipitation':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)   

        'freezing rain accumulation':  
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)  
            
        'rain accumulation':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)  
        
        'snow accumulation':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)  
            
        'latent heat net flux':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)  
            
        'outgoing longwave radiation':
            valid level type(s): 'nominal top'
            valid levels: None (level_type='nominal top' -> 'nominal top' is the only level) 
            
        'sea ice thickness':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level) 
            
        'pressure':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level) 
            
        'mean sea level pressure':
            valid level type(s): 'mean sea level'
            valid levels: None (level_type='mean sea level' -> 'mean sea level' is the only level) 
            
        'precipitable water':
            valid level type(s): 'entire atmosphere'
            valid levels: None (level_type='entire atmosphere' -> 'entire atmosphere' is the only level) 
            
        'relative humidity':
            valid level type(s) = 'pressure', 'height above ground'.
            valid levels:
                level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                    
                level_type='height above ground' (m): 2
                
        'surface runoff':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level) 
            
        'sensible heat net flux':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level) 
            
        'snow depth':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level) 
            
        'specific humidity':
            valid level type(s) = 'height above ground'.
            valid levels:
                level_type='height above ground' (m): 2, 40, 80, 120.
        
        'soil moisture':
            valid level type(s) = 'depth below surface'.
            valid levels:
                level_type='height above ground' (cm): 10.
                
        'total cloud cover':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level) 
            
        'maximum temperature':
            valid level type(s) = 'height above ground'.
            valid levels:
                level_type='height above ground' (m): 2.
                
        'minimum temperature':
            valid level type(s) = 'height above ground'.
            valid levels:
                level_type='height above ground' (m): 2.
                
        'soil temperature':
            valid level type(s) = 'depth below surface'.
            valid levels:
                level_type='height above ground' (cm): 10.
                
        'u-wind component':
            valid level type(s) = 'pressure', 'height above ground'.
            valid levels:
                level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                    
                level_type='height above ground' (m): 10.
                
        'v-wind component':
            valid level type(s) = 'pressure', 'height above ground'.
            valid levels:
                level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                    
                level_type='height above ground' (m): 10.
                
        'upward longwave radiation flux':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level) 
            
        'upward shortwave radiation flux':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level) 
            
        'vertical velocity':
            valid level type(s) = 'pressure'.
            valid levels:
                level_type='pressure' (hPa): 850.
                
        'wind speed':
            valid level type(s) = 'height above ground'.
            valid levels:
                level_type='height above ground' (m): 2, 40, 80, 120.   
                
                
    -l = Level. The pressure level in hPa or height above ground in meters.
                    
          Default=500 hPa     
        
    -lt = Level Type. Type of level (i.e. pressure, height above ground etc.). 
        
        Default='pressure'.
        
        ***Level Types***
    
        'pressure'
        
        'height above ground'
        
        'depth below surface'
        
        'surface'
        
        'mean sea level'
        
        'nominal top'
        
        'entire atmosphere'
        
    --process This flag when set to True will process the data in addition to downloading the data. (Default=True)
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    --netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.
    
    ***Additional Relevant Flags when --netcdf True***
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=GDPS/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=gfs_0p50.nc)
    
    ***Complex Example***
    
    1) Download the latest GEPS for 2-meter temperature 
     
    - Use a proxy server of address: https://proxy-server-address:proxy-server-port 
                
    2) Subset the data to reflect CONUS [-130, -65, 50, 20] = [west, east, north, south]
        
    3) Create a netCDF (.nc) file of the data called `geps_t2m.nc` saved at Weather_Data/GEPS/NETCDF.
    
    Linux Shell:
        ```wxdata-geps fetch latest -lt height_above_ground -l 2 -v temperature \
            -wb -130 -eb -65 -nb 50 -sb 20 \
            --netcdf True --ncdir Weather_Data/GEPS/NETCDF --ncfname geps_t2m.nc \ 
            --proxy https://proxy-server-address:proxy-server-port```
            
    Windows Powershell:
        ```wxdata-geps fetch latest -lt height_above_ground -l 2 -v temperature `
            -wb -130 -eb -65 -nb 50 -sb 20 `
            --netcdf True --ncdir Weather_Data/GEPS/NETCDF --ncfname geps_t2m.nc ` 
            --proxy https://proxy-server-address:proxy-server-port```
    
    """
    
@fetch_geps_data.command("latest")
@_click.option(
    "--final_forecast_hour",
    "-f",
    default=384,
    show_default=True,
    type=int,
    help="This is the final forecast hour requested in the dataset."
)

@_click.option(
    "--clear_recycle_bin",
    "-cr",
    default=False,
    show_default=True,
    type=bool,
    help="To clear your recycle bin with each run of the script set to True."
)

@_click.option(
    "--custom_directory",
    "-cdir",
    default="none",
    show_default=True,
    type=str,
    help="If you want to save the files in a custom directory - enter the full path here."
)

@_click.option(
    "--clear_data",
    "-cd",
    default=False,
    show_default=True,
    type=bool,
    help="To bypass the safety scanner set --clear data to False."
)


@_click.option(
    "--convert_temperature",
    "-ct",
    default=True,
    show_default=True,
    type=bool,
    help="When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit."
)

@_click.option(
    "--convert_to",
    "-tu",
    default='celsius',
    show_default=True,
    type=str,
    help="When -ct True this is where you declare the units for temperature to be converted to."
)

@_click.option(
    "--western_bound",
    "-wb",
    default=-180,
    show_default=True,
    type=int,
    help="Western Bound for subsetting the data. Range: -180 to 180 in Degrees Longitude. Default=-180."
)

@_click.option(
    "--eastern_bound",
    "-eb",
    default=180,
    show_default=True,
    type=int,
    help="Eastern Bound for subsetting the data. Range: -180 to 180 in Degrees Longitude. Default=180."
)

@_click.option(
    "--northern_bound",
    "-nb",
    default=90,
    show_default=True,
    type=int,
    help="Northern Bound for subsetting the data. Range: -90 to 90 in Degrees Latitude. Default=90."
)

@_click.option(
    "--southern_bound",
    "-sb",
    default=-90,
    show_default=True,
    type=int,
    help="Southern Bound for subsetting the data. Range: -90 to 90 in Degrees Latitude. Default=-90."
)
        
@_click.option('--variable', 
              '-v', 
              default='geopotential_height',
              type=str,
              help=(
                  """Variable to pass into the function. 
                  
                  Default='geopotential_height'
                  
                    ***Variables & Proper level_type & level***
                
                    Any area where valid_levels = None -> Users do not need to edit the optional argument `level`
                    
                    'temperature': 
                        valid level type(s) = 'pressure', 'height above ground'.
                        valid levels:
                            level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                                
                            level_type='height above ground' (m): 2, 40, 80, 120
                        
                    'cape':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                        
                    'cin':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)  
                            
                    'downward longwave radiation flux':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level) 
                        
                    'downward shortwave radiation flux':
                        valid level type(s): 'surface', 'nominal top'
                        valid levels: None (level_type='surface' -> 'surface' is the only level) 
                                                                OR 
                                        (level_type='nominal top' -> 'nominal top' is the only level)              
                                        
                    'geopotential height':
                        valid level type(s) = 'pressure'.
                        valid levels:
                            level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10. 
                                                                
                    'ice pellets accumulation':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)   
                        
                    'total convective precipitation':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)   

                    'freezing rain accumulation':  
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)  
                        
                    'rain accumulation':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)  
                    
                    'snow accumulation':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)  
                        
                    'latent heat net flux':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)  
                        
                    'outgoing longwave radiation':
                        valid level type(s): 'nominal top'
                        valid levels: None (level_type='nominal top' -> 'nominal top' is the only level) 
                        
                    'sea ice thickness':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level) 
                        
                    'pressure':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level) 
                        
                    'mean sea level pressure':
                        valid level type(s): 'mean sea level'
                        valid levels: None (level_type='mean sea level' -> 'mean sea level' is the only level) 
                        
                    'precipitable water':
                        valid level type(s): 'entire atmosphere'
                        valid levels: None (level_type='entire atmosphere' -> 'entire atmosphere' is the only level) 
                        
                    'relative humidity':
                        valid level type(s) = 'pressure', 'height above ground'.
                        valid levels:
                            level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                                
                            level_type='height above ground' (m): 2
                            
                    'surface runoff':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level) 
                        
                    'sensible heat net flux':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level) 
                        
                    'snow depth':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level) 
                        
                    'specific humidity':
                        valid level type(s) = 'height above ground'.
                        valid levels:
                            level_type='height above ground' (m): 2, 40, 80, 120.
                    
                    'soil moisture':
                        valid level type(s) = 'depth below surface'.
                        valid levels:
                            level_type='height above ground' (cm): 10.
                            
                    'total cloud cover':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level) 
                        
                    'maximum temperature':
                        valid level type(s) = 'height above ground'.
                        valid levels:
                            level_type='height above ground' (m): 2.
                            
                    'minimum temperature':
                        valid level type(s) = 'height above ground'.
                        valid levels:
                            level_type='height above ground' (m): 2.
                            
                    'soil temperature':
                        valid level type(s) = 'depth below surface'.
                        valid levels:
                            level_type='height above ground' (cm): 10.
                            
                    'u-wind component':
                        valid level type(s) = 'pressure', 'height above ground'.
                        valid levels:
                            level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                                
                            level_type='height above ground' (m): 10.
                            
                    'v-wind component':
                        valid level type(s) = 'pressure', 'height above ground'.
                        valid levels:
                            level_type='pressure' (hPa): 1000, 925, 850, 700, 500, 250, 200, 100, 50, 10.
                                                
                            level_type='height above ground' (m): 10.
                            
                    'upward longwave radiation flux':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level) 
                        
                    'upward shortwave radiation flux':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level) 
                        
                    'vertical velocity':
                        valid level type(s) = 'pressure'.
                        valid levels:
                            level_type='pressure' (hPa): 850.
                            
                    'wind speed':
                        valid level type(s) = 'height above ground'.
                        valid levels:
                            level_type='height above ground' (m): 2, 40, 80, 120.   
                  
                  See https://edrewitz.github.io/WxData/GEPS%20CLI for available variables."""
                  
                  )
)

@_click.option(
    '--level', 
    '-l', 
    default=500,
    type=int,  
    help=("""The pressure level in hPa or height above ground in meters.
                    
          Default=500 hPa
          
          See https://edrewitz.github.io/WxData/GEPS%20CLI for available levels.
          
          """)
)


@_click.option(
    '--level_type', 
    '-lt', 
    default="pressure",
    type=str,
    show_default=True,
    help=("""Type of level (i.e. pressure, height above ground etc.). 
        
          Default='pressure'.
          
          ***Level Types***
        
            'pressure'
            
            'height above ground'
            
            'depth below surface'
            
            'surface'
            
            'mean sea level'
            
            'nominal top'
            
            'entire atmosphere'
          
          See https://edrewitz.github.io/WxData/GEPS%20CLI for available level types.
          
          """)
)

@_click.option(
    "--proxy",
    default=None,
    callback=lambda _, __, v: _parse_proxy(v),
    show_default=True,
    help="Proxy URL (e.g., https://address:port). Default: no proxy.",
)

@_click.option(
    "--process",
    default=True,
    type=bool,
    show_default=True,
    help=("""This flag when set to True will process the data in addition to downloading the data. (Default=True)
          """),
)

@_click.option(
    "--netcdf",
    default=False,
    type=bool,
    show_default=True,
    help=("""This flag when set to True will create a netCDF (.nc) file for all the data ingested from the GRIB files.
          """),
)

@_click.option(
    "--ncdir",
    default=f"GEPS/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"geps.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def get_geps(final_forecast_hour,
             clear_recycle_bin,
             custom_directory,
             clear_data,
             convert_temperature,
             convert_to,
             western_bound,
             eastern_bound,
             southern_bound,
             northern_bound,
             variable,
             level,
             level_type,
             proxy,
             process,
             netcdf,
             ncdir,
             ncfname):
    
    """Downloads Latest GEPS Data"""
    
    try:
        if custom_directory.lower() == "none":
            custom_directory = None
        else:
            custom_directory = custom_directory
            if current_os == "Windows":
                custom_directory = custom_directory.replace('/', '\\')
            else:
                pass
        
        if netcdf == True:
            if current_os == "Windows":
                ncdir = ncdir.replace('/', '\\')
            else:
                pass
        
        variable = variable.lower()
        variable = variable.replace('_', ' ')
            
        level_type = level_type.replace('_', ' ')
        convert_to = convert_to.lower()
        
        if custom_directory == None:
            path = f"GEPS"
        else:
            path = custom_directory
        
        _fetch_geps(final_forecast_hour=final_forecast_hour,
                    clear_recycle_bin=clear_recycle_bin,
                    path=path,
                    clear_data=clear_data,
                    convert_temperature=convert_temperature,
                    convert_to=convert_to,
                    western_bound=western_bound,
                    eastern_bound=eastern_bound,
                    southern_bound=southern_bound,
                    northern_bound=northern_bound,
                    variable=variable,
                    level=level,
                    level_type=level_type,
                    proxies=proxy,
                    process_data=process,
                    to_netcdf=netcdf,
                    netcdf_path=ncdir,
                    netcdf_filename=ncfname,
                    return_values=False)
        
        if current_os != "Windows":
            _click.echo(f"GEPS latest download complete, data files saved to {path}")
        else:
            path = path.replace('/', '\\')
            _click.echo(rf"GEPS latest download complete, data files saved to {path}")
            
    except SystemExit as e:
        _command_error_message('geps')
        _sys.exit(1)
            
# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    geps_data()
    
if __name__ == "__main__":
    main()
    