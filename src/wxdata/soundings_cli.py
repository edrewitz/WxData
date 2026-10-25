"""
This file hosts the WxData Command Line Interface for retrieving Observed Upper-Air Sounding Data from the University of Wyoming Database.

Command Line Use: `wxdata-soundings **args`

(C) Eric J. Drewitz 2025-2026
"""
import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()

from wxdata.observational_data.soundings.wyoming_soundings import get_observed_sounding_data as _fetch_sounding

def _command_error_message():
    
    """Error Message For Invalid Commands OR No Data Available"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"Please run `wxdata-soundings fetch -h to view the help documentation.")
    print(f"Please visit: https://edrewitz.github.io/WxData/wyoming_soundings for full detailed documentation.")
    print(f"There is also a chance there is no data available for this time. Please visit: https://weather.uwyo.edu/upperair/sounding.shtml for more information.")

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
def soundings_data():
    """Observed sounding command line utilities."""
    pass

# ---------------------------------------------------------------------
# Sounding CLI Commands
# ---------------------------------------------------------------------
@soundings_data.group(name='fetch')
def sounding():
    """
    Observed Upper-Air Soundings Client
    
    ***Globally Valid Commands***
    
    -stid = Station ID. The station ID for the observed sounding site.
    
    -cdir = Custom Directory (Default=None).
    
    If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
    The default path is f:Observed Sounding/{STATION_ID_datetime.csv}. 
    
    -cr = Clear Recycle Bin (Default=False).
    
    For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
    Setting -cr True clears your recycle bin with each run of the script. 
    This ensures if any old files are moved to the recycle bin are deleted if they are not already.
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    Example: 
    
    `wxdata-soundings fetch latest -stid okx --proxy https://proxy-server-address:proxy-server-port`
    
    ***Extra Commands For Downloading Archived Data***
    
    -d = Datetime. The date and time of the observed sounding in the format 'YYYY-mm-dd:HH'
    
    Example: Let's use the WxData CLI to download the observed upper-air sounding for the El Reno Tornado
    
    *No Proxy*
    
    `wxdata-soundings fetch archived -stid oun -d 2013-05-31:18`
    
    *Proxy*
    
    `wxdata-soundings fetch archived -stid oun -d 2013-05-31:18 --proxy https://proxy-server-address:proxy-server-port`
    
    """
@sounding.command("latest")
@_click.option(
    "--station_id",
    "-stid",
    type=str,
    help="The station ID for the observed sounding site."
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
    "--proxy",
    default=None,
    callback=lambda _, __, v: _parse_proxy(v),
    show_default=True,
    help="Proxy URL (e.g., https://address:port). Default: no proxy.",
)


def sounding_fetch(station_id,
                   clear_recycle_bin,
                   custom_directory,
                   proxy):
    
    """Downloads Latest Observed Sounding Data for a Specified Station ID"""
    
    try:
        if custom_directory.lower() == "none":
            custom_directory = f"Observed Soundings"
        else:
            custom_directory = custom_directory
            if current_os == "Windows":
                custom_directory = custom_directory.replace('/', '\\')
            else:
                pass
                    
        _fetch_sounding(station_id,
                        proxies=proxy,
                        clear_recycle_bin=clear_recycle_bin,
                        to_csv=True,
                        path=custom_directory,
                        return_pandas_df=False)
        
        if custom_directory != "none" and custom_directory != None:
            _click.echo(f"{station_id.upper()} latest sounding data saved to {custom_directory}")
        else:
            _click.echo(f"{station_id.upper()} latest sounding data saved to Observed Soundings")

    except SystemExit as e:
        _command_error_message()
        _sys.exit(1)
        
@sounding.command("archived")
@_click.option(
    "--station_id",
    "-stid",
    type=str,
    help="The station ID for the observed sounding site."
)

@_click.option(
    "--datetime",
    "-d",
    type=str,
    help="The date and time of the observed sounding in the format 'YYYY-mm-dd:HH'"
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
    "--proxy",
    default=None,
    callback=lambda _, __, v: _parse_proxy(v),
    show_default=True,
    help="Proxy URL (e.g., https://address:port). Default: no proxy.",
)


def archived_sounding_fetch(station_id,
                   datetime,
                   clear_recycle_bin,
                   custom_directory,
                   proxy):
    
    """Downloads Latest Observed Sounding Data for a Specified Station ID for a specified date and time"""
    
    try:
        if custom_directory.lower() == "none":
            custom_directory = f"Observed Soundings"
        else:
            custom_directory = custom_directory
            if current_os == "Windows":
                custom_directory = custom_directory.replace('/', '\\')
            else:
                pass
                    
        _fetch_sounding(station_id,
                        current=False,
                        custom_time=datetime,
                        proxies=proxy,
                        clear_recycle_bin=clear_recycle_bin,
                        to_csv=True,
                        path=custom_directory,
                        return_pandas_df=False)
        
        if custom_directory != "none" and custom_directory != None:
            _click.echo(f"{station_id.upper()} sounding for {datetime} data saved to {custom_directory}")
        else:
            _click.echo(f"{station_id.upper()} sounding for {datetime} data saved to Observed Soundings")

    except SystemExit as e:
        _command_error_message()
        _sys.exit(1)
        

# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    soundings_data()
    
if __name__ == "__main__":
    main()