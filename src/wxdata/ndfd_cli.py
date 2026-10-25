"""
This file hosts the WxData Command Line Interface for retrieving the National Weather Service NDFD Gridded Forecast

Command Line Use: `wxdata-ndfd **args`

(C) Eric J. Drewitz 2025-2026
"""

import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()

from wxdata.gridded_forecasts.noaa.nws import get_ndfd_grids as _get_ndfd_grids

def _command_error_message(parameter):
    
    """Error Message For Invalid Commands"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"parameter: {parameter}")
    print(f"Please run `wxdata-ndfd -h to view the help documentation.")
    print(f"Please visit: https://github.com/edrewitz/WxData/wiki#ecmwf-open-data for full detailed documentation.")
    
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
def ndfd_data():
    """NDFD command line utilities."""
    pass

# ---------------------------------------------------------------------
# ECMWF IFS Commands
# ---------------------------------------------------------------------
@ndfd_data.group(name='ifs')
def fetch_ndfd():
    """_summary_
    """