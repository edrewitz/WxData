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
def get_cansips_forecast():
    
    """
    
    """