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
    default="noaa",
    show_default=True,
    type=str,
    help="Default noaa is for NCEP/NOMADS - set to aws to switch to Amazon Web Services or google to switch to Google Cloud"
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
                       'temperature',
                       'relative_humidity',
                       'u-component_of_wind'
                       'v-component_of_wind'],
              multiple=True, 
              type=str,
              help=(
                  """Variables to pass into the function. 
                  
                  Default=['geopotential_height', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']
                  
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
            400,
            300,
            250,
            200,
            100,
            50,
            10],
    multiple=True, 
    type=int,  
    help=("""Levels for pressure, height, PVU etc. 
          
          Pressure (hPa)
          
          Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10]
          
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
    default=f"GFS0P25/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"gfs_0p25.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)