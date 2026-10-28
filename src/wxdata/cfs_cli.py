"""
This file hosts the WxData Command Line Interface for retrieving Climate Forecast System (CFS) Data.

Command Line Use: `wxdata-cfs **args`

(C) Eric J. Drewitz 2025-2026
"""
import click as _click
import sys as _sys
import platform as _platform
import datetime as _datetime
current_os = _platform.system()

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
@cfs_data.group(name='fetch')
def cfs():
    
    r"""
    Climate Forecast System (CFS) Command Line Interface
    
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
    
    
    
    """