import click
import sys

from wxdata.model_data.noaa.rtma.rtma import(
    rtma as _fetch_rtma, 
    rtma_comparison
)


def _command_error_message(model):
    
    """Error Message For Invalid Commands"""
    
    print(f"Invalid Command Error: User Entered An Invalid Command.")
    print(f"Please run `model {model.lower()} -h to view the help documentation.")

def _parse_proxy(value):
    if value is None:
        return None

    # Accept either http://host:port or https://host:port
    return {
        "http": value,
        "https": value,
    }

# ---------------------------------------------------------------------
# Top-level CLI group
# ---------------------------------------------------------------------
@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def realtime_mesoscale_analysis():
    """RTMA command line utilities."""
    pass

# ---------------------------------------------------------------------
# RTMA Commands
# ---------------------------------------------------------------------
@realtime_mesoscale_analysis.group()
def rtma():
    """RTMA utilities."""
    pass


@rtma.command("latest")
@click.option(
    "--region",
    default="conus",
    show_default=True,
    help="Enter the abbreviation of the region: 1) conus, 2) ak (Alaska), 3) hi (Hawaii), 4) pr (Puerto Rico), 5) gu (Guam)"
)

@click.option(
    "--cat",
    default="analysis",
    show_default=True,
    help="analysis - Latest RTMA Analysis | error - Latest RTMA Error | surface 1 hour forecast - RTMA Surface 1 Hour Forecast."
)

@click.option(
    "--proxy",
    default=None,
    callback=lambda _, __, v: _parse_proxy(v),
    help="Proxy URL (e.g., https://address:port). Default: no proxy.",
    show_default=True,
)

@click.option(
    "--clear_recycle_bin",
    default=False,
    show_default=True,
    help="To clear your recycle bin with each run of the script set to True."
)

@click.option(
    "--custom_directory",
    default=None,
    show_default=True,
    help="If you want to save the files in a custom directory - enter the full path here."
)

@click.option(
    "--clear_data",
    default=False,
    show_default=True,
    help="To bypass the safety scanner set --clear data to False."
)

@click.option(
    "--source",
    default="noaa",
    show_default=True,
    help="Default noaa is for NCEP/NOMADS - set to aws to switch to Amazon Web Services"
)

def rtma_fetch(region, 
               cat, 
               proxy, 
               clear_recycle_bin, 
               custom_directory, 
               clear_data, 
               source):
    """Download RTMA GRIB2 data."""
    
    region = region.lower()
    
    if region == 'conus':
        model = 'rtma'
    elif region == 'ak':
        model = 'ak rtma'
    elif region == 'pr':
        model = 'pr rtma'
    elif region == 'hi':
        model = 'hi rtma'
    elif region == 'gu':
        model = 'gu rtma'
    else:
        model = 'rtma'

    _fetch_rtma(
        model=model,
        cat=cat,
        proxies=proxy,
        clear_recycle_bin=clear_recycle_bin,
        custom_directory=custom_directory,
        clear_data=clear_data,
        source=source,
        process_data=False
    )

    if custom_directory == True:
        click.echo(f"RTMA {region.upper()} fetch complete for model={model}, category={cat}, saved to {custom_directory}")
    else:
        click.echo(f"RTMA {region.upper()} fetch complete for model={model}, category={cat}, saved to {model.upper()}/{cat.upper()}")
        
# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    realtime_mesoscale_analysis()
    
if __name__ == "__main__":
    main()