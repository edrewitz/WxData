"""
This file hosts the WxData Command Line Interface for retrieving Climate Forecast System (CFS) Data.

Command Line Use: `wxdata-cfs **args`

(C) Eric J. Drewitz 2025-2026
"""
import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()

from datetime import datetime as _datetime
from wxdata.model_data.noaa.cfs.cfs import(
    cfs_flux as _fetch_cfs_flux,
    cfs_pressure as _fetch_cfs_pressure
)

from wxdata.archived_data.model_data.noaa.cfs.cfs import(
    get_archived_cfs_flux as _fetch_archived_cfs_flux,
    get_archived_cfs_pressure as _fetch_archived_cfs_pressure
)

def _command_error_message(model):
    
    """Error Message For Invalid Commands"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"Model: {model.upper()}")
    print(f"Please run `wxdata-cfs -h to view the help documentation.")
    print(f"Please visit: https://edrewitz.github.io/WxData/AI%20GFS%20CLI for full detailed documentation.")

def _parse_proxy(value):
    if value is None:
        return None

    else:
        # Accept either http://host:port or https://host:port
        return {
            "http": value,
            "https": value,
        }
        
def _parse_date(date):
    
    """Parses String Date Into DateTime Object"""
    
    if type(date) == type(_datetime.now()):
        date = date
    else:
        date = f"{date[0:4]}{date[5:7]}{date[8:10]}"
        date = _datetime.strptime(date, "%Y%m%d")
        
    return date

# ---------------------------------------------------------------------
# Top-level CLI group
# ---------------------------------------------------------------------
@_click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cfs_data():
    """CFS command line utilities."""
    pass

# ---------------------------------------------------------------------
# CFS Commands
# ---------------------------------------------------------------------
@cfs_data.group(name='pressure')
def cfs_pressure():
    
    r"""
    Climate Forecast System (CFS) Pressure Variables & Levels Command Line Interface
    
    ***Archived Required Commands***
    
    -d = Date. The date of the model run in the format of YYYY-mm-dd.
    
        (i.e. December 25th, 2025 should be entered as -d 2025-12-25)
        
    -r = Run. The model runtime in UTC (0, 6, 12, 18). 
    
        (i.e. for the 12z run set -r 12)
    
    
    ***Globally Valid Commands (valid for both "latest" and "archived")***
        
    -t = Type (Default=primary).
    
    This determines the type of variables and levels.
    
    -f = Final Forecast Hour (Default=720).
     
    The last hour the user wishes to download in the dataset. GFS0P25 has 384 forecast hours.
    
    -s = Source (Default=noaa). 
    
    Selects the primary data server to use.
    If the primary server is unavailable the client will rotate and try other servers.
    
    ***Server Choices For Latest Data***
    
    noaa - NCEP/NOMADS
    
    aws - Amazon Web Services
        
    ***Server Choices For Archived Data***
    
    aws - Amazon Web Services
        
    -cdir = Custom Directory (Default=None).
    
    If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
    
    -cr = Clear Recycle Bin (Default=False).
    
    For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
    Setting -cr True clears your recycle bin with each run of the script. 
    This ensures if any old files are moved to the recycle bin are deleted if they are not already.
    
    -wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)
    
    -eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)
    
    -nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)
    
    -sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)
    
    -v = Variable. Default="geopotential_height".
    
       ***Variable List***
       
        'best lifted index'
        
        '5 wave geopotential height anomaly'
        
        '5 wave geopotential height'
        
        'absolute vorticity'
        
        'convective precipitation'
        
        'total precipitation'
        
        'convective available potential energy'
        
        'categorical freezing rain'
        
        'categorical ice pellets'
        
        'convective inhibition'
        
        'cloud mixing ratio'
        
        'categorical rain'
        
        'categorical snow'
        
        'cloud water'
        
        'dew point'
        
        'geopotential height anomaly'
        
        'geopotential height'
        
        'storm relative helicity'
        
        'surface lifted index'
        
        'large scale non-convective precipitation'
        
        'ozone mixing ratio'
        
        'parcel lifted index'
        
        'potential temperature'
        
        'pressure'
        
        'mean sea level pressure'
        
        'precipitable water'
        
        'relative humidity'
        
        'specific humidity'
        
        'stream function'
        
        'temperature'
        
        'total ozone'
        
        'u-component of wind'
        
        'u-component of storm motion'
        
        'v-component of wind'
        
        'velocity potential'
        
        'v-component of storm motion'
        
        'vertical velocity'
        
        'vertical speed shear'
        
    -l = Levels (Default=[1000, 925, 850, 700, 500, 400, 300, 250])
    
    ***Available Levels***
    
    
    1000
    975
    925
    900
    875
    850
    825
    800
    775
    750
    700
    650
    600
    550
    500
    450
    400
    350
    300
    250
    225
    200
    175
    150
    125
    100
    70
    50
    30
    20
    10
    7
    5
    3
    2
    1
    
    
    -ct = Convert Temperature (Default=True).
    
    When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.
    
    -tu = Temperature Units (Default=Celsius).
    
    When -ct True this is where you declare the units for temperature to be converted to. 
    
    -lt = Level Type (Default=pressure).
    
    This corresponds to the type of level.
    
    ***Level Types***
    
    'pressure'
    
    'surface'
    
    'height above ground'
    
    'entire atmosphere'
    
    'mean sea level'
    
    'tropopause'
    
    'height above sea level'
    
    'isothermal'
    
    'highest tropospheric freezing level'
    
    'pressure above ground'
    
    'sigma layer'
    
    'sigma level'
    
    'potential vorticity surface'
    
    --process = Process Data. This flag when set to True will process the data in addition to downloading the data. (Default=True)
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    --netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.
    
    ***Additional Relevant Flags when --netcdf True***
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=CFS/PRESSURE/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=cfs_pressure.nc)
    
    ***Commands Only Valid for "latest"***
    
    -cd = Clear Data (Default=False).
    
    ***Only for wxdata-cfs pressure latest***
    
    ***Archived Clients Automatically Clear Old Data***
    
    When set to False the scanner safeguard that prevents repetative downloads is enabled.
    Set -cd False to disable this safety feature.
    
    WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
    being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
    retry downloading the data. 
    
    ***Complex Example***
    
    1) Download the latest CFS forecast for 500mb Geopotential Height from NCEP/NOMADS
     
        - Use a proxy server of address: https://proxy-server-address:proxy-server-port 
        
        - Use the default `final_forecast_hour` of hour 720 (1-month). 
                
    2) Subset the data to reflect CONUS [-130, -65, 50, 20] = [west, east, north, south]
        
    3) Create a netCDF (.nc) file of the data called `cfs_500_gph.nc` saved at Weather_Data/CFS/GPH/500/NETCDF.
    
    Linux Shell:
        ```wxdata-cfs pressure latest -lt pressure -l 500 -v geopotential_height \
            -s noaa -wb -130 -eb -65 -nb 50 -sb 20 \
            --netcdf True --ncdir Weather_Data/CFS/GPH/500/NETCDF --ncfname cfs_500_gph.nc \ 
            --proxy https://proxy-server-address:proxy-server-port```
            
    Windows Powershell:
        ```wxdata-cfs pressure latest -lt pressure -l 500 -v geopotential_height `
            -s noaa -wb -130 -eb -65 -nb 50 -sb 20 `
            --netcdf True --ncdir Weather_Data/CFS/GPH/500/NETCDF --ncfname cfs_500_gph.nc ` 
            --proxy https://proxy-server-address:proxy-server-port```
    
    """
    
@cfs_pressure.command("latest")
@_click.option(
    "--final_forecast_hour",
    "-f",
    default=720,
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
    help="To bypass the safety scanner set --clear data to False: -cd False."
)

@_click.option(
    "--source",
    "-s",
    default="noaa",
    show_default=True,
    type=str,
    help="Default noaa is for NCEP/NOMADS - set to aws to switch to Amazon Web Services or google to switch to Google Cloud"
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
                  
                  See https://edrewitz.github.io/WxData/GFS0P25 for available variables."""
                  
                  )
)

@_click.option(
    '--levels', 
    '-l', 
    default=[1000, 
                925, 
                850, 
                700, 
                500, 
                300, 
                250],
    multiple=True, 
    type=int,  
    help=("""Levels for pressure, height, PVU etc. 
          
          Pressure (hPa)
          
          Default=[1000, 925, 850, 700, 500, 400, 300, 250]
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available levels.
          
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
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available level types.
          
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
    default=f"CFS/PRESSURE/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"cfs_pressure.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def cfs_pressure_fetch(final_forecast_hour,
                  proxy,
                  clear_recycle_bin,
                  custom_directory,
                  clear_data,
                  source,
                  variable,
                  levels,
                  level_type,
                  netcdf,
                  ncdir,
                  ncfname,
                  process,
                  western_bound,
                  eastern_bound,
                  northern_bound,
                  southern_bound,
                  convert_temperature,
                  convert_to):
    
    """Downloads Latest CFS Data"""
    
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
        if variable == "parcel lifted index":
            variable = "parcel lifted index (to 500mb)"
        elif variable == "vertical velocity":
            variable = "vertical velocity (pressure)"
        else:
            pass
        
        variable = variable.replace('_', ' ')
            
        level_type = level_type.replace('_', ' ')
        
        convert_to = convert_to.lower()
        
        if custom_directory == None:
            path = f"CFS/PRESSURE"
        else:
            path = custom_directory
        
        _fetch_cfs_pressure(final_forecast_hour=final_forecast_hour,
                        western_bound=western_bound,
                        eastern_bound=eastern_bound,
                        southern_bound=southern_bound,
                        northern_bound=northern_bound,
                        variable=variable,
                        levels=levels,
                        level_type=level_type,
                        convert_temperature=convert_temperature,
                        convert_to=convert_to,
                        source=source,
                        proxies=proxy,
                        clear_recycle_bin=clear_recycle_bin,
                        clear_data=clear_data,
                        path=path,
                        process_data=process,
                        to_netcdf=netcdf,
                        netcdf_path=ncdir,
                        netcdf_filename=ncfname,
                        return_values=False)
        
    except Exception as e:
        if custom_directory != "none" and custom_directory != None:
            _click.echo(f"CFS Pressure latest download complete, data files saved to {path}")
        else:
            if current_os != "Windows":
                _click.echo(f"CFS Pressure latest download complete, data files saved to CFS/PRESSURE")
            else:
                _click.echo(rf"CFS Pressure latest download complete, data files saved to CFS\PRESSURE")
            
    except SystemExit as e:
        _command_error_message('cfs pressure')
        _sys.exit(1)

        
@cfs_pressure.command("archived")
@_click.option(
    "--date",
    "-d",
    type=str,
    help=("""This is a mandatory field. The date must be entered in the form of YYYY-mm-dd
          
          (i.e. December 25th, 2025 is 2025-12-25)
          
          """
    )
)

@_click.option(
    "--run",
    "-r",
    type=int,
    help=("""This is a mandatory field. The the model runtime must be entered as an integer corresponding to the run in UTC (0, 6, 12, 18)
                    
          """
    )
)

@_click.option(
    "--final_forecast_hour",
    "-f",
    default=720,
    show_default=True,
    type=int,
    help="This is the final forecast hour requested in the dataset."
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
                  
                  See https://edrewitz.github.io/WxData/GFS0P25 for available variables."""
                  
                  )
)

@_click.option(
    '--levels', 
    '-l', 
    default=[1000, 
                925, 
                850, 
                700, 
                500, 
                300, 
                250],
    multiple=True, 
    type=int,  
    help=("""Levels for pressure, height, PVU etc. 
          
          Pressure (hPa)
          
          Default=[1000, 925, 850, 700, 500, 400, 300, 250]
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available levels.
          
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
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available level types.
          
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
    default=f"CFS/PRESSURE/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"cfs_pressure.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def cfs_pressure_fetch(date,
                  run,
                  final_forecast_hour,
                  proxy,
                  custom_directory,
                  variable,
                  levels,
                  level_type,
                  netcdf,
                  ncdir,
                  ncfname,
                  process,
                  western_bound,
                  eastern_bound,
                  northern_bound,
                  southern_bound,
                  convert_temperature,
                  convert_to):
    
    """Downloads Archived CFS Data"""
    
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
            path = f"CFS Pressure/Archive"
        else:
            path = custom_directory
        
        _fetch_archived_cfs_pressure(date,
                        run,
                        final_forecast_hour=final_forecast_hour,
                        western_bound=western_bound,
                        eastern_bound=eastern_bound,
                        southern_bound=southern_bound,
                        northern_bound=northern_bound,
                        variable=variable,
                        levels=levels,
                        level_type=level_type,
                        convert_temperature=convert_temperature,
                        convert_to=convert_to,
                        proxies=proxy,
                        path=path,
                        process_data=process,
                        to_netcdf=netcdf,
                        netcdf_path=ncdir,
                        netcdf_filename=ncfname,
                        return_values=False)
        
        d = _parse_date(date)
        _click.echo(f"CFS Pressure download for {d.strftime('%Y-%m-%d')} {run}z complete, data files saved to {path}")
    except SystemExit as e:
        _command_error_message('cfs pressure')
        _sys.exit(1)
        
@cfs_data.group(name='flux')
def cfs_flux():
    
    r"""
    Climate Forecast System (CFS) Flux Variables & Levels Command Line Interface
    
    ***Archived Required Commands***
    
    -d = Date. The date of the model run in the format of YYYY-mm-dd.
    
        (i.e. December 25th, 2025 should be entered as -d 2025-12-25)
        
    -r = Run. The model runtime in UTC (0, 6, 12, 18). 
    
        (i.e. for the 12z run set -r 12)
    
    
    ***Globally Valid Commands (valid for both "latest" and "archived")***
        
    -t = Type (Default=primary).
    
    This determines the type of variables and levels.
    
    -f = Final Forecast Hour (Default=720).
     
    The last hour the user wishes to download in the dataset. GFS0P25 has 384 forecast hours.
    
    -s = Source (Default=noaa). 
    
    Selects the primary data server to use.
    If the primary server is unavailable the client will rotate and try other servers.
    
    ***Server Choices For Latest Data***
    
    noaa - NCEP/NOMADS
    
    aws - Amazon Web Services
        
    ***Server Choices For Archived Data***
    
    aws - Amazon Web Services
        
    -cdir = Custom Directory (Default=None).
    
    If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
    
    -cr = Clear Recycle Bin (Default=False).
    
    For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
    Setting -cr True clears your recycle bin with each run of the script. 
    This ensures if any old files are moved to the recycle bin are deleted if they are not already.
    
    -wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)
    
    -eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)
    
    -nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)
    
    -sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)
    
    -v = Variable. Default="temperature".
    
       ***Variable List***
       
    'aerodynamic conductance'
    
    'albedo'
    
    'clear sky uv-b downward solar flux'
    
    'plant canopy surface water'
    
    'convective precipitation rate'
    
    'categorical rain'
    
    'clear sky downward longwave flux'
    
    'clear sky downward solar flux (surface)'
    
    'clear sky downward solar flux (top of the atmosphere)'
    
    'clear sky upward solar flux'
    
    'cloud work function'
    
    'downward longwave radiation flux'
    
    'downward shortwave radiation flux'
    
    'clear sky uv-b downward solar flux'
    
    'direct evaporation from bare soil'
    
    'canopy water evaporation'
    
    'surface friction velocity'
    
    'ground heat flux'
    
    'geopotential height'
    
    'planetary boundary layer height'
    
    'ice cover'
    
    'ice thickness'
    
    'land cover'
    
    'latent heat net flux'
    
    'near ir beam downward solar flux'
    
    'near ir diffuse downward solar flux'
    
    'potential evaporation rate'
    
    'precipitation rate'
    
    'pressure'
    
    'precipitable water'
    
    '2-meter maximum specific humidity'
    
    '2-meter minimum specific humidity'
    
    'sublimation (evaporation from snow)'
    
    'surface roughness'
    
    'sedimentation mass flux'
    
    'sensible heat net flux'
    
    'surface slope type'
    
    'snow depth'
    
    'snow phase-change heat flux'
    
    'snow cover'
    
    'liquid volumetric soil moisture (non-frozen)'
    
    'soil moisture content'
    
    'volumetric soil moisture content'
    
    'soil type'
    
    'specific humidity'
    
    'snowfall rate water equivalent'
    
    'storm surface runoff (non-infiltrating)'
    
    'total cloud cover'
    
    'maximum temperature'
    
    'minimum temperature'
    
    'temperature'
    
    'transpiration'
    
    'momentum flux (u-component)'
    
    'u-component of wind'
    
    'zonal flux of gravity wave stress'
    
    'upward longwave radiation flux'
    
    'upward shortwave radiation flux'
    
    'visible beam downward solar flux'
    
    'vegetation'
    
    'momentum flux (v-component)'
    
    'v-component of wind'
    
    'vegetation type'
    
    'meridional flux of gravity wave stress'
    
    'water runoff'
    
    'water equivalent of accumulated snow depth'
        
    -l = Levels (Default=[2])
        
    ***Available Levels***
    
    *height above ground*
    
    m above ground
    
    [2, 10]
    
    *height below ground*
    
    m below ground
    
    [0-0.1, 0.1-0.4, 0.4-1, 0.1-0.4, 1-2, 0-2]
    
    *hybrid*
    
    [1]
    
    -ct = Convert Temperature (Default=True).
    
    When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.
    
    -tu = Temperature Units (Default=Celsius).
    
    When -ct True this is where you declare the units for temperature to be converted to. 
    
    -lt = Level Type (Default=height_above_ground).
    
    This corresponds to the type of level.
    
    ***Level Types***
    
    'surface'
    
    'height_above_ground'
    
    'height_below_ground'
    
    'entire_atmosphere'
    
    'top_of_atmosphere'
    
    'high_cloud_top_level'
    
    'middle_cloud_top_level'
    
    'low_cloud_top_level'
    
    'high_cloud_bottom_level'
    
    'middle_cloud_bottom_level'
    
    'low_cloud_bottom_level'
    
    'convective_cloud_layer'
    
    'boundary_layer_cloud_layer'
    
    'height_above_sea_level'
    
    'hybrid'
    
    --process = Process Data. This flag when set to True will process the data in addition to downloading the data. (Default=True)
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    --netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.
    
    ***Additional Relevant Flags when --netcdf True***
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=CFS/Flux/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=cfs_flux.nc)
    
    ***Commands Only Valid for "latest"***
    
    -cd = Clear Data (Default=False).
    
    ***Only for wxdata-cfs pressure latest***
    
    ***Archived Clients Automatically Clear Old Data***
    
    When set to False the scanner safeguard that prevents repetative downloads is enabled.
    Set -cd False to disable this safety feature.
    
    WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
    being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
    retry downloading the data. 
    
    ***Complex Example***
    
    1) Download the latest CFS forecast for 2-meter temperature from NCEP/NOMADS
     
        - Use a proxy server of address: https://proxy-server-address:proxy-server-port 
        
        - Use the default `final_forecast_hour` of hour 720 (1-month). 
                
    2) Subset the data to reflect CONUS [-130, -65, 50, 20] = [west, east, north, south]
        
    3) Create a netCDF (.nc) file of the data called `cfs_t2m_gph.nc` saved at Weather_Data/CFS/TMP/2/NETCDF.
    
    Linux Shell:
        ```wxdata-cfs flux latest -lt height_above_ground -l 2 -v temperature \
            -s noaa -wb -130 -eb -65 -nb 50 -sb 20 \
            --netcdf True --ncdir Weather_Data/CFS/TMP/2/NETCDF --ncfname cfs_t2m_gph.nc \ 
            --proxy https://proxy-server-address:proxy-server-port```
            
    Windows Powershell:
        ```wxdata-cfs flux latest -lt height_above_ground -l 2 -v temperature `
            -s noaa -wb -130 -eb -65 -nb 50 -sb 20 `
            --netcdf True --ncdir Weather_Data/CFS/TMP/2/NETCDF --ncfname cfs_t2m_gph.nc ` 
            --proxy https://proxy-server-address:proxy-server-port```
    
    """
    
@cfs_flux.command("latest")
@_click.option(
    "--final_forecast_hour",
    "-f",
    default=720,
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
    help="To bypass the safety scanner set --clear data to False: -cd False."
)

@_click.option(
    "--source",
    "-s",
    default="noaa",
    show_default=True,
    type=str,
    help="Default noaa is for NCEP/NOMADS - set to aws to switch to Amazon Web Services or google to switch to Google Cloud"
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
              default='temperature',
              type=str,
              help=(
                  """Variable to pass into the function. 
                  
                  Default='geopotential_height'
                  
                  See https://edrewitz.github.io/WxData/GFS0P25 for available variables."""
                  
                  )
)

@_click.option(
    '--levels', 
    '-l', 
    default=[2],
    multiple=True, 
    type=int,  
    help=("""Levels for pressure, height, PVU etc. 
          
          Height (m above ground)
          
          Default=[2]
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available levels.
          
          """)
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="height above ground",
    type=str,
    show_default=True,
    help=("""Type of level (i.e. pressure, height above ground etc.). 
        
          Default='pressure'.
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available level types.
          
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
    default=f"CFS/FLUX/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"cfs_flux.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def cfs_flux_fetch(final_forecast_hour,
                  proxy,
                  clear_recycle_bin,
                  custom_directory,
                  clear_data,
                  source,
                  variable,
                  levels,
                  level_type,
                  netcdf,
                  ncdir,
                  ncfname,
                  process,
                  western_bound,
                  eastern_bound,
                  northern_bound,
                  southern_bound,
                  convert_temperature,
                  convert_to):
    
    """Downloads Latest CFS Data"""
    
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
            path = f"CFS/FLUX"
        else:
            path = custom_directory
        
        _fetch_cfs_flux(final_forecast_hour=final_forecast_hour,
                        western_bound=western_bound,
                        eastern_bound=eastern_bound,
                        southern_bound=southern_bound,
                        northern_bound=northern_bound,
                        variable=variable,
                        levels=levels,
                        level_type=level_type,
                        convert_temperature=convert_temperature,
                        convert_to=convert_to,
                        source=source,
                        proxies=proxy,
                        clear_recycle_bin=clear_recycle_bin,
                        clear_data=clear_data,
                        path=path,
                        process_data=process,
                        to_netcdf=netcdf,
                        netcdf_path=ncdir,
                        netcdf_filename=ncfname,
                        return_values=False)
        
    except Exception as e:
        if custom_directory != "none" and custom_directory != None:
            _click.echo(f"CFS Flux latest download complete, data files saved to {path}")
        else:
            if current_os != "Windows":
                _click.echo(f"CFS Flux latest download complete, data files saved to CFS/FLUX")
            else:
                _click.echo(rf"CFS Flux latest download complete, data files saved to CFS\FLUX")
            
    except SystemExit as e:
        _command_error_message('cfs flux')
        _sys.exit(1)

        
@cfs_flux.command("archived")
@_click.option(
    "--date",
    "-d",
    type=str,
    help=("""This is a mandatory field. The date must be entered in the form of YYYY-mm-dd
          
          (i.e. December 25th, 2025 is 2025-12-25)
          
          """
    )
)

@_click.option(
    "--run",
    "-r",
    type=int,
    help=("""This is a mandatory field. The the model runtime must be entered as an integer corresponding to the run in UTC (0, 6, 12, 18)
                    
          """
    )
)

@_click.option(
    "--final_forecast_hour",
    "-f",
    default=720,
    show_default=True,
    type=int,
    help="This is the final forecast hour requested in the dataset."
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
              default='temperature',
              type=str,
              help=(
                  """Variable to pass into the function. 
                  
                  Default='temperature'
                  
                  See https://edrewitz.github.io/WxData/GFS0P25 for available variables."""
                  
                  )
)

@_click.option(
    '--levels', 
    '-l', 
    default=[2],
    multiple=True, 
    type=int,  
    help=("""Levels for pressure, height, PVU etc. 
          
          Height (m above ground)
          
          Default=[2]
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available levels.
          
          """)
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="height above ground",
    type=str,
    show_default=True,
    help=("""Type of level (i.e. pressure, height above ground etc.). 
        
          Default='pressure'.
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available level types.
          
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
    default=f"CFS/Flux/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"cfs_flux.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def cfs_archived_flux_fetch(date,
                  run,
                  final_forecast_hour,
                  proxy,
                  custom_directory,
                  variable,
                  levels,
                  level_type,
                  netcdf,
                  ncdir,
                  ncfname,
                  process,
                  western_bound,
                  eastern_bound,
                  northern_bound,
                  southern_bound,
                  convert_temperature,
                  convert_to):
    
    """Downloads Archived CFS Data"""
    
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
            path = f"CFS Flux/Archive"
        else:
            path = custom_directory
        
        _fetch_archived_cfs_flux(date,
                        run,
                        final_forecast_hour=final_forecast_hour,
                        western_bound=western_bound,
                        eastern_bound=eastern_bound,
                        southern_bound=southern_bound,
                        northern_bound=northern_bound,
                        variable=variable,
                        levels=levels,
                        level_type=level_type,
                        convert_temperature=convert_temperature,
                        convert_to=convert_to,
                        proxies=proxy,
                        path=path,
                        process_data=process,
                        to_netcdf=netcdf,
                        netcdf_path=ncdir,
                        netcdf_filename=ncfname,
                        return_values=False)
        
        d = _parse_date(date)
        _click.echo(f"CFS Pressure download for {d.strftime('%Y-%m-%d')} {run}z complete, data files saved to {path}")
    except SystemExit as e:
        _command_error_message('cfs flux')
        _sys.exit(1)
        
        
# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    cfs_data()
    
if __name__ == "__main__":
    main()