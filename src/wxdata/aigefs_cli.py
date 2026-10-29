"""
This file hosts the WxData Command Line Interface for retrieving AI Global Ensemble Forecast System (AIGEFS) Data.

Command Line Use: `wxdata-aigefs **args`

(C) Eric J. Drewitz 2025-2026
"""
import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()

from wxdata.model_data.noaa.aigefs import(
    aigefs_single as _fetch_aigefs_single,
    aigefs_pressure_members as _fetch_aigefs_pressure_members,
    aigefs_surface_members as _fetch_aigefs_surface_members
)

def _command_error_message(model):
    
    """Error Message For Invalid Commands"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"Model: {model.upper()}")
    print(f"Please run `wxdata-aigefs -h to view the help documentation.")
    print(f"Please visit: https://edrewitz.github.io/WxData/AI%20GEFS%20CLI for full detailed documentation.")

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
def aigefs_data():
    """AIGEFS command line utilities."""
    pass

# ---------------------------------------------------------------------
# AIGEFS Commands
# ---------------------------------------------------------------------
@aigefs_data.group(name="fetch")
def aigefs():
    r"""
    AI Global Ensemble Forecast System (AIGEFS) Client
    
    ***Valid Commands***
    
    -c = Category (Default=mean).
    
        ***Valid categories***
        
        1) mean
        
        2) members
        
        3) spread
        
    -f = Final Forecast Hour (Default=384).
    
    -m = Members.
    
        The individual ensemble members to select. Defaults to all 30 members.
        
        This is only necessary when category=members -> `-c members`
        
    -cr = Clear Recycle Bin. (Default=False)
    
    To clear your recycle bin with each run of the script set to True.
    
    -cdir = Custom Directory (Default=None).
    
    When set to None, the default file path is used. 
    
    Change this if you want your directories set up differently.
    
    -cd = Clear Data (Default=False).
            
    When set to False the scanner safeguard that prevents repetative downloads is enabled.
    Set -cd False to disable this safety feature.
    
    WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
    being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
    retry downloading the data. 
    
    -s = Source (Default=noaa). 
    
    Selects the primary data server to use.
    If the primary server is unavailable the client will rotate and try other servers.
    
    ***Server Choices***
    
    noaa - NCEP/NOMADS
    
    aws - Amazon Web Services
    
    -ct = Convert Temperature (Default=True).
    
    When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.
    
    -tu = Temperature Units (Default=Celsius).
    
    When -ct True this is where you declare the units for temperature to be converted to. 
    
    -lt = Level Type (Default=pressure).
    
    This corresponds to the type of level.
    
    ***Level Types***
    
    i) pressure
    
    ii) surface
    
    iii) height_above_ground
    
    -l = Levels (hPa) (Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10])
    
    -wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)
    
    -eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)
    
    -nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)
    
    -sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)
    
    -v = Variables(Default=['geopotential_height', 'specific humidity', 'temperature', 'u-component_of_wind', 'v-component_of_wind', 'vertical_velocity']) 
                       
    The list of variables the user wants to query.
    
    ***Variables By Level Type***
    
    *pressure*
    
    'geopotential_height'
    
    'specific_humidity'
    
    'temperature'
    
    'u-component_of_wind'
    
    'v-component_of_wind'
    
    'vertical_velocity'
    
    *height_above_ground*
    
    'u-component_of_wind' - 10m
    
    'v-component_of_wind' - 10m
    
    'temperature' - 2m
    
    *mean_sea_level*
    
    'mean_sea_level_pressure'
    
    *surface*
    
    'total_precipitation'
    
    ***Pressure-Level Plain Language Variable Keys***
    
    'geopotential_height'
    
    'specific_humidity'
    
    'air_temperature'
    
    'u_wind_component'
    
    'v_wind_component'
    
    'vertical_velocity'
    
    ***Surface-Level Plain Language Variable Keys***
    
    '10m_u_wind_component'
    
    '10m_v_wind_component'
    
    'mslp'
    
    '2m_temperature'
    
    --process This flag when set to True will process the data in addition to downloading the data. (Default=True)
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    --netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.
    
    ***Additional Relevant Flags when --netcdf True***
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=AIGEFS/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=aigefs.nc)
    
    ***Complex Example***
    
    *Important*: Any parameter of the command not explicitly stated results in the default value being used.
    
    1) Download the latest AIGEFS Ensemble Spread for 500mb Geopotential Height from Amazon Web Services
     
        - Use a proxy server of address: https://proxy-server-address:proxy-server-port 
                
    2) Subset the data to reflect Northern Hemisphere [-180, 180, 90, 0] = [west, east, north, south]
        
    3) Create a netCDF (.nc) file of the data called `aigefs_spread_gph.nc` saved at Weather_Data/AIGEFS/NETCDF.
    
    Linux Shell:
        ```wxdata-aigefs fetch latest -c spread -v geopotential_height -l 500 \
            -s aws -wb -180 -eb 180 -nb 90 -sb 0 \
            --netcdf True --ncdir Weather_Data/AIGEFS/NETCDF --ncfname aigefs_spread_gph.nc \ 
            --proxy https://proxy-server-address:proxy-server-port```
            
    Windows Powershell:
        ```wxdata-aigefs fetch latest -c spread -v geopotential_height -l 500 `
            -s aws -wb -180 -eb 180 -nb 90 -sb 0 `
            --netcdf True --ncdir Weather_Data/AIGEFS/NETCDF --ncfname aigefs_spread_gph.nc ` 
            --proxy https://proxy-server-address:proxy-server-port```
    
    """
@aigefs.command("latest")
@_click.option(
    "--category",
    "-c",
    default="mean",
    type=str,
    show_default=True,
    help=("""The category of the ensemble data. Default='mean'.  
    
            ***Valid categories***
            
            1) mean
            
            2) members
            
            3) spread
                
          """
    )
)

@_click.option(
    "--final_forecast_hour",
    "-f",
    default=384,
    show_default=True,
    type=int,
    help="This is the final forecast hour requested in the dataset."
)

@_click.option(
    "--members",
    "-m",
    default=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    show_default=True,
    multiple=True,
    type=int,
    help="""The individual ensemble members to select. Defaults to all 30 members.
    
            This is only necessary when category=members -> `-c members`
    
    """
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

@_click.option('--variables', 
              '-v', 
              default=['geopotential_height',
                       'specific_humidity',
                       'temperature',
                       'u-component_of_wind',
                       'v-component_of_wind',
                       'vertical_velocity'],
              multiple=True, 
              type=str,
              help=(
                  """Variables to pass into the function. 
                  
                  Default=['geopotential_height', 'specific humidity', 'temperature', 'u-component_of_wind', 'v-component_of_wind', 'vertical velocity']
                  
                  See https://edrewitz.github.io/WxData/AI%20GEFS%20CLI for available variables."""
                  
                  )
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="pressure",
    type=str,
    show_default=True,
    help=("""Type of level.
        
          Default='pressure'.
          
          ***Types of Levels***
          
          1) pressure => -lt pressure
          
          2) surface => -lt surface
          
          3) height above ground => -lt height_above_ground
                    
          """)
)

@_click.option(
    '--levels', 
    '-l', 
    default=[1000,
            925,
            850,
            700,
            600,
            500,
            400,
            300,
            250,
            150,
            100,
            50],
    multiple=True, 
    type=int,  
    help=("""Levels for pressure. 
          
          Pressure (hPa)
          
          Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10]
          
          See https://edrewitz.github.io/WxData/AI%20GEFS%20CLI for available levels.
          
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
    default=f"AIGEFS/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"aigefs.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def aigefs_fetch(final_forecast_hour,
                  proxy,
                  clear_recycle_bin,
                  custom_directory,
                  clear_data,
                  source,
                  variables,
                  levels,
                  level_type,
                  category,
                  members,
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
    
    """Downloads Latest AIGEFS Data"""
    
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
        
        vars_fixed = []
        for v in variables:
            v = v.replace('_', ' ')
            if v == "vertical velocity":
                v = "vertical velocity (pressure)"
            else:
                pass
            vars_fixed.append(v)
            
        level_type = level_type.replace('_', ' ')
        
        category = category.lower()
        convert_to = convert_to.lower()
        
        if category == "members":
            if level_type == "pressure":
                _fetch_aigefs_pressure_members(final_forecast_hour=final_forecast_hour,
                                               western_bound=western_bound,
                                               eastern_bound=eastern_bound,
                                               northern_bound=northern_bound,
                                               southern_bound=southern_bound,
                                               proxies=proxy,
                                               members=members,
                                               process_data=process,
                                               clear_recycle_bin=clear_recycle_bin,
                                               clear_data=clear_data,
                                               convert_temperature=convert_temperature,
                                               convert_to=convert_to,
                                               custom_directory=custom_directory,
                                               variables=vars_fixed,
                                               levels=levels,
                                               source=source,
                                               to_netcdf=netcdf,
                                               netcdf_path=ncdir,
                                               netcdf_filename=ncfname,
                                               return_values=False)
                
                if custom_directory != "none" and custom_directory != None:
                    _click.echo(f"AIGEFS {category.upper()} latest download complete, data files saved to {custom_directory}")
                else:
                    if current_os != "Windows":
                        _click.echo(f"AIGEFS {category.upper()} latest download complete, data files saved to AIGEFS/PRESSURE/[Member]")
                    else:
                        _click.echo(rf"AIGEFS {category.upper()} latest download complete, data files saved to AIGEFS\PRESSURE\[Member]")
                        
            else:
                _fetch_aigefs_surface_members(final_forecast_hour=final_forecast_hour,
                                            western_bound=western_bound,
                                            eastern_bound=eastern_bound,
                                            northern_bound=northern_bound,
                                            southern_bound=southern_bound,
                                            proxies=proxy,
                                            members=members,
                                            levels=levels,
                                            variables=vars_fixed,
                                            level_type=level_type,
                                            process_data=process,
                                            clear_recycle_bin=clear_recycle_bin,
                                            clear_data=clear_data,
                                            convert_temperature=convert_temperature,
                                            convert_to=convert_to,
                                            custom_directory=custom_directory,
                                            source=source,
                                            to_netcdf=netcdf,
                                            netcdf_path=ncdir,
                                            netcdf_filename=ncfname,
                                            return_values=False)
                
                if custom_directory != "none" and custom_directory != None:
                    _click.echo(f"AIGEFS {category.upper()} latest download complete, data files saved to {custom_directory}")
                else:
                    if current_os != "Windows":
                        _click.echo(f"AIGEFS {category.upper()} latest download complete, data files saved to AIGEFS/{level_type.upper()}/[Member]")
                    else:
                        _click.echo(rf"AIGEFS {category.upper()} latest download complete, data files saved to AIGEFS\{level_type.upper()}\[Member]")
                        
        else:
            _fetch_aigefs_single(final_forecast_hour=final_forecast_hour,
                                western_bound=western_bound,
                                eastern_bound=eastern_bound,
                                northern_bound=northern_bound,
                                southern_bound=southern_bound,
                                proxies=proxy,
                                process_data=process,
                                clear_recycle_bin=clear_recycle_bin,
                                clear_data=clear_data,
                                convert_temperature=convert_temperature,
                                convert_to=convert_to,
                                custom_directory=custom_directory,
                                cat=category,
                                level_type=level_type,
                                variables=vars_fixed,
                                levels=levels,
                                to_netcdf=netcdf,
                                netcdf_path=ncdir,
                                netcdf_filename=ncfname,
                                return_values=False)
            
            if custom_directory != "none" and custom_directory != None:
                _click.echo(f"AIGEFS {category.upper()} latest download complete, data files saved to {custom_directory}")
            else:
                if current_os != "Windows":
                    _click.echo(f"AIGEFS {category.upper()} latest download complete, data files saved to AIGEFS/{level_type.upper()}/{category.upper()}")
                else:
                    _click.echo(rf"AIGEFS {category.upper()} latest download complete, data files saved to AIGEFS\{level_type.upper()}\{category.upper()}")
                    
    except SystemExit as e:
        _command_error_message('aigefs')
        _sys.exit(1)

# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    aigefs_data()
    
if __name__ == "__main__":
    main()