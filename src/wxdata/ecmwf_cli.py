"""
This file hosts the WxData Command Line Interface for retrieving European Centre for Medium-Range Weather Forecasts (ECMWF) Data.

Command Line Use: `wxdata-ecmwf **args`

(C) Eric J. Drewitz 2025-2026
"""

import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()

from wxdata.model_data.ecmwf.ecmwf import(
    ecmwf_ifs as _fetch_ecmwf_ifs,
    ecmwf_ifs_ens as _fetch_ecmwf_ifs_ens,
    ecmwf_aifs as _fetch_ecmwf_aifs,
    ecmwf_aifs_ens as _fetch_ecmwf_aifs_ens,
    ecmwf_ifs_wave as _fetch_ecmwf_ifs_wave,
    ecmwf_ifs_wave_ens as _fetch_ecmwf_ifs_wave_ens
)


def _command_error_message(model):
    
    """Error Message For Invalid Commands"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"Model: {model.upper()}")
    print(f"Please run `wxdata-gfs -h to view the help documentation.")
    print(f"Please visit: https://github.com/edrewitz/WxData/wiki#ecmwf-open-data for full detailed documentation.")
    
# ---------------------------------------------------------------------
# Top-level CLI group
# ---------------------------------------------------------------------
@_click.group(context_settings={"help_option_names": ["-h", "--help"]})
def ecmwf_data():
    """GFS command line utilities."""
    pass

# ---------------------------------------------------------------------
# ECMWF Commands
# ---------------------------------------------------------------------
@ecmwf_data.group(name='ifs')
def ifs():
    
    """
    
    """
    
@ifs.command("latest")
@_click.option(
    "--final_forecast_hour",
    "-f",
    default=360,
    show_default=True,
    type=int,
    help=("""This is the final forecast hour requested in the dataset. Default=360.
          
            00z & 12z Runs Have 360 hours
            
            06z & 18z Runs Have 144 hours
          
          """)
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
    default="ecmwf",
    show_default=True,
    type=str,
    help="Default ecmwf is for ECMWF Open-Data - set to aws to switch to Amazon Web Services or google to switch to Google Cloud"
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
              default=['geopotential height',
                        'specific humidity',
                        'relative humidity',
                        'temperature',
                        'u-wind component',
                        'v-wind component'],
              multiple=True, 
              type=str,
              help=(
                  """Variables to pass into the function. 
                  
                  Default=['geopotential_height', 'specific humidity', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']
                  
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
            600, 
            500, 
            400, 
            300, 
            250, 
            200, 
            150, 
            100, 
            50],
    multiple=True, 
    type=int,  
    help=("""Levels for pressure, height, PVU etc. 
          
          Pressure (hPa)
          
          Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 50]
          
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
    default="none",
    show_default=True,
    type=str,
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
    default=f"ECMWF IFS/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"ecmwf_ifs.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def fetch_ifs(final_forecast_hour,
                  proxy,
                  clear_recycle_bin,
                  custom_directory,
                  clear_data,
                  source,
                  variables,
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
    
    if proxy == "none":
        proxy = None
    else:
        proxy = proxy
    
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
        vars_fixed.append(v)
        
    level_type = level_type.replace('_', ' ')
    
    try:
        _fetch_ecmwf_ifs(final_forecast_hour=final_forecast_hour,
                         western_bound=western_bound,
                         eastern_bound=eastern_bound,
                         northern_bound=northern_bound,
                         southern_bound=southern_bound,
                         clear_data=clear_data,
                         clear_recycle_bin=clear_recycle_bin,
                         proxies=proxy,
                         source=source,
                         level_type=level_type,
                         levels=levels,
                         convert_temperature=convert_temperature,
                         convert_to=convert_to,
                         to_netcdf=netcdf,
                         netcdf_path=ncdir,
                         netcdf_filename=ncfname,
                         process_data=process,
                         return_values=False,
                         variables=vars_fixed)
        
        if custom_directory != "none" and custom_directory != None:
            _click.echo(f"ECMWF IFS latest download complete, data files saved to {custom_directory}")
        else:
            if current_os != "Windows":
                _click.echo(f"ECMWF IFS latest download complete, data files saved to ECMWF/IFS")
            else:
                _click.echo(rf"ECMWF IFS latest download complete, data files saved to ECMWF\IFS")
            
    except SystemExit as e:
        _command_error_message('ecmwf ifs')
        _sys.exit(1)
    
    
    

# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    ecmwf_data()
    
if __name__ == "__main__":
    main()
    