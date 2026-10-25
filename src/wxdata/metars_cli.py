"""
This file hosts the WxData Command Line Interface for retrieving METAR Observations from https://aviationweather.gov.

Command Line Use: `wxdata-metars **args`

(C) Eric J. Drewitz 2025-2026
"""
import click as _click
import os as _os
import sys as _sys
import platform as _platform
current_os = _platform.system()

from wxdata.observational_data.metars.metar_obs import download_metar_data as _fetch_metars

cwd = _os.getcwd()

if current_os == "Windows":
    cwd = cwd.replace('/', '\\')
    cwd = rf"{cwd}\METAR_Data\metars.csv"
else:
    cwd = f"{cwd}/METAR_Data/metars.csv"



def _command_error_message():
    
    """Error Message For Invalid Commands OR No Data Available"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"Please run `wxdata-metars fetch -h to view the help documentation.")
    print(f"Please visit: https://edrewitz.github.io/WxData/metars for full detailed documentation.")

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
def metar_data():
    """METAR Observation command line utilities."""
    pass

# ---------------------------------------------------------------------
# METAR CLI Commands
# ---------------------------------------------------------------------
@metar_data.group(name='fetch')
def metars():
    """
    METAR Observations Soundings Client
    
    ***Valid Commands***
    
    -cr = Clear Recycle Bin (Default=False).
    
    For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
    Setting -cr True clears your recycle bin with each run of the script. 
    This ensures if any old files are moved to the recycle bin are deleted if they are not already.
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    Example: 
    
    `wxdata-metars fetch latest --proxy https://proxy-server-address:proxy-server-port`
    
    """
@metars.command("latest")
@_click.option(
    "--clear_recycle_bin",
    "-cr",
    default=False,
    show_default=True,
    type=bool,
    help="To clear your recycle bin with each run of the script set to True."
)


@_click.option(
    "--proxy",
    default=None,
    callback=lambda _, __, v: _parse_proxy(v),
    show_default=True,
    help="Proxy URL (e.g., https://address:port). Default: no proxy.",
)


def metar_fetch(clear_recycle_bin,
                proxy):
    
    """Downloads Latest METAR Observations from https://aviationweather.gov"""
    
    try:
        _fetch_metars(clear_recycle_bin=clear_recycle_bin,
                    proxies=proxy)
        
        print(f"METAR Data Saved to: {cwd}")
    except Exception as e:
        _command_error_message()
        _sys.exit(1)

# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    metar_data()
    
if __name__ == "__main__":
    main()