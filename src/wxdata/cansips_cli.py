"""
This file hosts the WxData Command Line Interface for retrieving Canadian Seasonal to Inter-annual Prediction System (CanSIPS) Data.

Command Line Use: `wxdata-cansips **args`

(C) Eric J. Drewitz 2025-2026
"""
import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()

from wxdata.model_data.cmc.cansips.forecast.cansips_forecast import cansips_forecast as _fetch_cansips_forecast
from wxdata.model_data.cmc.cansips.hindcast.cansips_hindcast import cansips_hindcast as _fetch_cansips_hindcast

def _command_error_message(model):
    
    """Error Message For Invalid Commands"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"Model: {model.upper()}")
    print(f"Please run `wxdata-cfs -h to view the help documentation.")
    if model.lower() == "cansips forecast":
        print(f"Please visit: https://edrewitz.github.io/WxData/CFS%20Flux%20CLI for full detailed documentation.")
    else:
        print(f"Please visit: https://edrewitz.github.io/WxData/CFS%20Pressure%20CLI for full detailed documentation.")

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
def cansips_data():
    """CanSIPS command line utilities."""
    pass

# ---------------------------------------------------------------------
# CFS Commands
# ---------------------------------------------------------------------
@cansips_data.group(name='fetch')
def get_cansips_data():
    
    """
    CanSIPS Command Line Interface
    
    ***Valid Commands***
        

    """
@get_cansips_data.command("latest")
@_click.option(
    "--type",
    "-t",
    default="forecast",
    type=str,
    show_default=True,
    help=("""This determines whether the user downloads the forecast or hindcast
          
          -t forecast => CanSIPS Forecasts
          
          -t hindcast => CanSIPS Hindcast
          
          """
    )
)

@_click.option(
    "--category",
    "-c",
    default="none",
    type=str,
    show_default=True,
    help=("""The type of probabilistic category. If not requesting a probabilistic forecast set this to none.
    
    ***Category List***
    
    'probability above normal'
    
    'probability below normal'
    
    'probability near normal'
    
    'probability > 10th percentile'
    
    'probability > 20th percentile'
    
    'probability > 30th percentile'
    
    'probability > 40th percentile'
    
    'probability > 50th percentile'
    
    'probability > 60th percentile'
    
    'probability > 70th percentile'
    
    'probability > 80th percentile'
    
    'probability > 90th percentile'
          """
    )
)

@_click.option(
    "--period",
    "-p",
    default="monthly",
    show_default=True,
    type=str,
    help="The forecast increment (monthly or seasonal [3-month])"
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
    help="To bypass the safety scanner set --clear data to False: -cd False."
)

@_click.option('--variable', 
              '-v', 
              default='geopotential_height',
              type=str,
              help=(
                  """Variable to pass into the function. 
                  
                  Default='geopotential_height'
                  
                  See https://edrewitz.github.io/WxData/CFS%20Pressure%20CLI for available variables."""
                  
                  )
)

@_click.option(
    '--level', 
    '-l', 
    default=500,
    type=int,  
    help=("""Level in the units of level_type
                    
          Default=500 hPa
          
          See https://edrewitz.github.io/WxData/GFS0P25%20CLI for available levels.
          
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
        
            'height above ground'
            
            'pressure'
            
            'surface'
            
            'geoid'
            
            'mean sea level'
          
          See https://edrewitz.github.io/WxData/GFS0P25%20CLI for available level types.
          
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
    default=f"CanSIPS/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"cansips_forecast.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def fetch_cansips(type,
                  category,
                  period,
                  convert_temperature,
                  convert_to,
                  western_bound,
                  eastern_bound,
                  southern_bound,
                  northern_bound,
                  clear_recycle_bin,
                  clear_data,
                  custom_directory,
                  variable,
                  level,
                  level_type,
                  proxy,
                  process,
                  netcdf,
                  ncdir,
                  ncfname):
    
    """Downloads Latest CanSIPS Data"""
    
    try:
        if category.lower() == "none":
            category = None
        else:
            pass
        
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
        
        variable = variable.replace('_', ' ')
        level_type = level_type.replace('_', ' ')
        
        type = type.lower()
        convert_to = convert_to.lower()
        
        if type == "forecast":
            if custom_directory == None:
                path = f"CanSIPS/Forecast/Geopotential Height/500mb/Monthly"
            else:
                path = custom_directory
            
            _fetch_cansips_forecast(western_bound=western_bound,
                                    eastern_bound=eastern_bound,
                                    southern_bound=southern_bound,
                                    northern_bound=northern_bound,
                                    variable=variable,
                                    level=level,
                                    level_type=level_type,
                                    period=period,
                                    category=category,
                                    proxies=proxy,
                                    path=path,
                                    clear_data=clear_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    process_data=process,
                                    to_netcdf=netcdf,
                                    netcdf_path=ncdir,
                                    netcdf_filename=ncfname,
                                    return_values=False)
            
        else:
            if custom_directory == None:
                path = f"CanSIPS/Hindcast/Geopotential Height/500mb/Monthly"
            else:
                path = custom_directory
            
            _fetch_cansips_hindcast(western_bound=western_bound,
                                    eastern_bound=eastern_bound,
                                    southern_bound=southern_bound,
                                    northern_bound=northern_bound,
                                    variable=variable,
                                    level=level,
                                    level_type=level_type,
                                    category=category,
                                    proxies=proxy,
                                    path=path,
                                    clear_data=clear_data,
                                    clear_recycle_bin=clear_recycle_bin,
                                    convert_temperature=convert_temperature,
                                    convert_to=convert_to,
                                    process_data=process,
                                    to_netcdf=netcdf,
                                    netcdf_path=ncdir,
                                    netcdf_filename=ncfname,
                                    return_values=False)
            

        if current_os != "Windows":
            _click.echo(f"CanSIPS {type.upper()} latest download complete, data files saved to {path}")
        else:
            _click.echo(rf"CanSIPS {type.upper()} latest download complete, data files saved to {path.replace('/', '\\')}")
            
    except SystemExit as e:
        _command_error_message('cansips')
        _sys.exit(1)
            
            