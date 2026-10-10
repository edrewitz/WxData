"""
This file hosts the WxData Command Line Interface for retrieving Real-Time Mesoscale Analysis (RTMA) Data.

Command Line Use: `wxdata-rtma **args`

(C) Eric J. Drewitz 2025-2026
"""

import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()

from wxdata.model_data.noaa.rtma.rtma import rtma as _fetch_rtma
from wxdata.archived_data.model_data.noaa.rtma.rtma import rtma as _fetch_archived_rtma
from datetime import datetime as _datetime

def _parse_date(date):
    
    """Parses String Date Into DateTime Object"""
    
    if type(date) == type(_datetime.now()):
        date = date
    else:
        date = f"{date[0:4]}{date[5:7]}{date[8:10]}"
        date = _datetime.strptime(date, "%Y%m%d")
        
    return date

def _command_error_message(model):
    
    """Error Message For Invalid Commands"""
    
    print(f"Invalid Command Error: User Entered An Invalid Command.")
    print(f"Please run `rtma {model.lower()} -h to view the help documentation.")

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
def realtime_mesoscale_analysis():
    """Real Time Mesoscale Analysis command line utilities."""
    pass

# ---------------------------------------------------------------------
# RTMA Commands
# ---------------------------------------------------------------------
@realtime_mesoscale_analysis.group()
def rtma():
    """Real Time Mesoscale Analysis Client.
    
    
    Archived Required Commands
    --------------------------
    
    -d = Date. The date of the model run in the format of YYYY-mm-dd.
    
        (i.e. December 25th, 2025 should be entered as -d 2025-12-25)
        
    -r = Run. The model runtime in UTC (0, 6, 12, 18). 
    
        (i.e. for the 12z run set -r 12)
    
    
    Globally Valid Commands (valid for both "latest" and "archived")
    
    -------------------------------------------------------
    
    -loc = Location (Default='conus'). Locations: 1) `conus`, 2) `ak` (Alaska), 3) `hi` (Hawaii), 4) `pr` (Puerto Rico), 5) `gu` (Guam).
    
    -c = Category (Default='analysis'). Category choices: 
    
    1) `analysis` - RTMA Analysis
    
    2) `error` - RTMA Error
    
    3) `forecast` - RTMA 1-Hour Forecast
    
    -cr = Clear Recycle Bin (Default=False).
    
    For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
    Setting -cr True clears your recycle bin with each run of the script. 
    This ensures if any old files are moved to the recycle bin are deleted if they are not already.
    
    -cdir = Custom Directory (Default=None).
    
    If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
    The default path is f:RTMA/ANALYSIS. 
    
    --process This flag when set to True will process the data in addition to downloading the data. (Default=True)
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    Example: 
    
    `wxdata-rtma latest --proxy https://proxy-server-address:proxy-server-port`
    
    --netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.
    
    **Additional Relevant Flags when --netcdf True**
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=RTMA/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=rtma.nc)
    
    
    Commands Only Valid for "latest"
    --------------------------------
    
    -s = Source (Default=noaa). 
    
    Selects the primary data server to use.
    If the primary server is unavailable the client will rotate and try other servers.
    
    ***Server Choices For Latest Data***
    
    noaa - NCEP/NOMADS
    
    aws - Amazon Web Services
    
    -cd = Clear Data (Default=False).
    
    ***Only for wxdata-rtma latest***
    
    ***Archived Clients Automatically Clear Old Data***
    
    When set to False the scanner safeguard that prevents repetative downloads is enabled.
    Set -cd False to disable this safety feature.
    
    WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
    being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
    retry downloading the data. 
    
    """
    pass


@realtime_mesoscale_analysis.command("latest")
@_click.option(
    "--location",
    "-loc",
    default="conus",
    show_default=True,
    help="Enter the abbreviation of the region: 1) conus, 2) ak (Alaska), 3) hi (Hawaii), 4) pr (Puerto Rico), 5) gu (Guam)"
)

@_click.option(
    "--category",
    "-c",
    default="analysis",
    show_default=True,
    help="analysis - Latest RTMA Analysis | error - Latest RTMA Error | forecast - RTMA Surface 1 Hour Forecast."
)


@_click.option(
    "--clear_recycle_bin",
    "-cr",
    default=False,
    show_default=True,
    help="To clear your recycle bin with each run of the script set to True."
)

@_click.option(
    "--custom_directory",
    "-cdir",
    default="none",
    type=str,
    show_default=True,
    help="If you want to save the files in a custom directory - enter the full path here."
)

@_click.option(
    "--clear_data",
    "-cd",
    default=False,
    show_default=True,
    help="To bypass the safety scanner set --clear data to False: -cd False."
)

@_click.option(
    "--source",
    default="noaa",
    show_default=True,
    help="Default noaa is for NCEP/NOMADS - set to aws to switch to Amazon Web Services"
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
    "--proxy",
    default=None,
    callback=lambda _, __, v: _parse_proxy(v),
    show_default=True,
    help="Proxy URL (e.g., https://address:port). Default: no proxy.",
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
    default=f"RTMA/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"rtma.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def rtma_fetch(location, 
               category, 
               proxy, 
               clear_recycle_bin, 
               custom_directory, 
               clear_data, 
               source,
               process,
               netcdf,
               ncdir,
               ncfname):
    """Download Latest Real Time Mesoscale Analysis."""
    
    location = location.lower()
    category = category.lower()
    if category == 'forecast':
        category = 'surface 1 hour forecast'
    else:
        category = category
    
    if location == 'conus':
        model = 'rtma'
    elif location == 'ak':
        model = 'ak rtma'
    elif location == 'pr':
        model = 'pr rtma'
    elif location == 'hi':
        model = 'hi rtma'
    elif location == 'gu':
        model = 'gu rtma'
    else:
        model = 'rtma'

    try:
        _fetch_rtma(
            model=model,
            cat=category,
            proxies=proxy,
            clear_recycle_bin=clear_recycle_bin,
            custom_directory=custom_directory,
            clear_data=clear_data,
            source=source,
            process_data=process,
            to_netcdf=netcdf,
            netcdf_path=ncdir,
            netcdf_filename=ncfname,
            return_values=False
        )

        if custom_directory != "none":
            if current_os != "Windows":
                _click.echo(f"RTMA {location.upper()} fetch complete for model={model}, category={category}, saved to {custom_directory}")
            else:
                _click.echo(rf"RTMA {location.upper()} fetch complete for model={model}, category={category}, saved to {custom_directory}")
        else:
            if current_os != "Windows":
                _click.echo(f"RTMA {location.upper()} fetch complete for model={model}, category={category}, saved to {model.upper()}/{category.upper()}")
            else:
                _click.echo(rf"RTMA {location.upper()} fetch complete for model={model}, category={category}, saved to {model.upper()}\{category.upper()}")
    except Exception as e:
        _command_error_message(model)
        _sys.exit(1)
        
@realtime_mesoscale_analysis.command("archived")
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
    "--location",
    "-loc",
    default="conus",
    show_default=True,
    help="Enter the abbreviation of the region: 1) conus, 2) ak (Alaska), 3) hi (Hawaii), 4) pr (Puerto Rico), 5) gu (Guam)"
)

@_click.option(
    "--category",
    "-c",
    default="analysis",
    show_default=True,
    help="analysis - Latest RTMA Analysis | error - Latest RTMA Error | forecast - RTMA Surface 1 Hour Forecast."
)


@_click.option(
    "--clear_recycle_bin",
    "-cr",
    default=False,
    show_default=True,
    help="To clear your recycle bin with each run of the script set to True."
)

@_click.option(
    "--custom_directory",
    "-cdir",
    default=None,
    show_default=True,
    help="If you want to save the files in a custom directory - enter the full path here."
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
    "--proxy",
    default=None,
    callback=lambda _, __, v: _parse_proxy(v),
    show_default=True,
    help="Proxy URL (e.g., https://address:port). Default: no proxy.",
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
    default=f"RTMA/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"rtma.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def archived_rtma_fetch(
               date,
               run,
               location, 
               category, 
               proxy, 
               clear_recycle_bin, 
               custom_directory, 
               process,
               netcdf,
               ncdir,
               ncfname):
    """Download Archived Real Time Mesoscale Analysis."""
    
    location = location.lower()
    category = category.lower()
    if category == 'forecast':
        category = 'surface 1 hour forecast'
    else:
        category = category
    
    if location == 'conus':
        model = 'rtma'
    elif location == 'ak':
        model = 'ak rtma'
    elif location == 'pr':
        model = 'pr rtma'
    elif location == 'hi':
        model = 'hi rtma'
    elif location == 'gu':
        model = 'gu rtma'
    else:
        model = 'rtma'

    try:
        _fetch_archived_rtma(
            date,
            run,
            model=model,
            cat=category,
            proxies=proxy,
            clear_recycle_bin=clear_recycle_bin,
            path=custom_directory,
            process_data=process,
            to_netcdf=netcdf,
            netcdf_path=ncdir,
            netcdf_filename=ncfname,
            return_values=False
        )
        
        d =  _parse_date(date)
        if current_os != "Windows":
            _click.echo(f"RTMA {location.upper()} fetch complete for model={model} for {d.strftime('%Y-%m-%d')} {run}z, category={category}, saved to {custom_directory}")
        else:
            _click.echo(rf"RTMA {location.upper()} fetch complete for model={model} for {d.strftime('%Y-%m-%d')} {run}z, category={category}, saved to {custom_directory}")
    except Exception as e:
        _command_error_message(model)
        _sys.exit(1)

        
# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    realtime_mesoscale_analysis()
    
if __name__ == "__main__":
    main()