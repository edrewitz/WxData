"""
This file hosts the WxData Command Line Interface for retrieving NEXRAD II Radar Data from Amazon Web Services (AWS)

Command Line Use: `wxdata-nexrad2 **args`

(C) Eric J. Drewitz 2025-2026
"""
import click as _click
import os as _os
import sys as _sys
import platform as _platform
current_os = _platform.system()

from wxdata.observational_data.radar.nexrad2 import download_current_single_station_nexrad2_radar_data as _fetch_nexrad2
from wxdata.archived_data.radar_data.nexrad2 import download_archived_single_station_nexrad2_radar_data as _fetch_archived_nexrad2

def _command_error_message():
    
    """Error Message For Invalid Commands OR No Data Available"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"Please run `wxdata-nexrad2 fetch latest -h` or `wxdata-nexrad2 fetch archived -h` to view the help documentation.")
    print(f"Please visit: https://edrewitz.github.io/WxData/nexrad2_single for full detailed documentation.")

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
def nexrad2_data():
    """NEXRAD2 command line utilities."""
    pass

# ---------------------------------------------------------------------
# NEXRAD2 CLI Commands
# ---------------------------------------------------------------------
@nexrad2_data.group(name='fetch')
def nexrad2():
    
    """
    NEXRAD II Radar Data Client
    
    **Globally Valid Commands**
    
    -sid = Site ID. The ID for the NEXRAD II Radar site.
    
    -hr = Hours. Default=3. The amount of hours to query (hours=3 --> current to current -3 hours).
    
    -m = Mode. Default='precipitation'. 
    
    When in 'precipitation' mode, data querying is based on 10 scans per hour.
        
    When in 'clear air' mode, data querying is based on 7 scans per hour.
               
    -cdir = Custom Directory. If you want to save the files in a custom directory - enter the full path here.
    
    -cr = Clear Recycle Bin. To clear your recycle bin with each run of the script set to True. (Default=False)
    
    **Additional Required Field For Archived Data**
    
    -st = Start Time. The time in 'YYYY-mm-dd:HH' of the last scan in the set.
        
    Example: start_time='2025-08-01:18' & hours = 3 = Radar scans from 2025-08-01:15 - 2025-08-01:18. 
    
    """

    @nexrad2_data.command("latest")
    @_click.option(
        "--site_id",
        "-sid",
        type=str,
        help="The ID for the NEXRAD II Radar site."
    )

    @_click.option(
        "--hours",
        "-hr",
        default=3,
        show_default=True,
        type=int,
        help="Default=3. The amount of hours to query (hours=3 --> current to current -3 hours)."
    )

    @_click.option(
        "--mode",
        "-m",
        default='precipitation',
        show_default=True,
        type=str,
        help=("""Default='precipitation'. 
        
                When in 'precipitation' mode, data querying is based on 10 scans per hour.
            
                When in 'clear air' mode, data querying is based on 7 scans per hour.
            
            """)
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

    def fetch_latest_nexrad2_data(site_id,
                                hours,
                                mode,
                                custom_directory,
                                clear_recycle_bin,
                                proxy):
        
        
        try:
            if custom_directory.lower() == "none":
                custom_directory = f"Radar Data/Latest"
            else:
                custom_directory = custom_directory
                if current_os == "Windows":
                    custom_directory = custom_directory.replace('/', '\\')
                else:
                    pass
                
            _fetch_nexrad2(
                        site_id,
                        hours=hours,
                        path=custom_directory,
                        proxies=proxy,
                        clear_recycle_bin=clear_recycle_bin,
                        mode=mode
                        )
            
            if custom_directory != "none" and custom_directory != None:
                _click.echo(f"{site_id.upper()} NEXRAD II data saved to {custom_directory}")
            else:
                if current_os != "Windows":
                    _click.echo(f"Latest {site_id.upper()} NEXRAD II data saved to Radar Data/Latest")
                else:
                    _click.echo(rf"Latest {site_id.upper()} NEXRAD II data saved to Radar Data\Latest")

        except SystemExit as e:
            _command_error_message()
            _sys.exit(1)
            
            
    @nexrad2_data.command("archived")
    @_click.option(
        "--site_id",
        "-sid",
        type=str,
        help="The ID for the NEXRAD II Radar site."
    )

    @_click.option(
        "--start_time",
        "-st",
        type=str,
        help=("""The time in 'YYYY-mm-dd:HH' of the last scan in the set.
            
                Example: start_time='2025-08-01:18' & hours = 3 = Radar scans from 2025-08-01:15 - 2025-08-01:18. 
            
            """)
    )

    @_click.option(
        "--hours",
        "-hr",
        default=3,
        show_default=True,
        type=int,
        help="Default=3. The amount of hours to query (hours=3 --> current to current -3 hours)."
    )

    @_click.option(
        "--mode",
        "-m",
        default='precipitation',
        show_default=True,
        type=str,
        help=("""Default='precipitation'. 
        
                When in 'precipitation' mode, data querying is based on 10 scans per hour.
            
                When in 'clear air' mode, data querying is based on 7 scans per hour.
            
            """)
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

    def fetch_archived_nexrad2_data(site_id,
                                    start_time,
                                    hours,
                                    mode,
                                    custom_directory,
                                    clear_recycle_bin,
                                    proxy):
        
        
        try:
            if custom_directory.lower() == "none":
                custom_directory = f"Radar Data/Archive"
            else:
                custom_directory = custom_directory
                if current_os == "Windows":
                    custom_directory = custom_directory.replace('/', '\\')
                else:
                    pass
                
            _fetch_archived_nexrad2(
                        site_id,
                        start_time,
                        hours=hours,
                        path=custom_directory,
                        proxies=proxy,
                        clear_recycle_bin=clear_recycle_bin,
                        mode=mode
                        )
            
            if custom_directory != "none" and custom_directory != None:
                _click.echo(f"{site_id.upper()} NEXRAD II data for {start_time} saved to {custom_directory}")
            else:
                if current_os != "Windows":
                    _click.echo(f"{site_id.upper()} NEXRAD II data for {start_time}  saved to Radar Data/Archive")
                else:
                    _click.echo(rf"{site_id.upper()} NEXRAD II data for {start_time}  saved to Radar Data\Archive")

        except SystemExit as e:
            _command_error_message()
            _sys.exit(1)
        
# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    nexrad2_data()
    
if __name__ == "__main__":
    main()