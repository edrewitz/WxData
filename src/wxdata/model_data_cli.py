import click

from wxdata.model_data.noaa.gfs.gfs import(
    gfs_0p25 as _fetch_gfs_0p25,
    gfs_0p25_secondary_parameters as _fetch_gfs_0p25_secondary_parameters,
    gfs_0p50 as _fetch_gfs_0p50
)

from wxdata.model_data.noaa.aigfs.aigfs import aigfs
from wxdata.model_data.noaa.hgefs.hgefs import hgefs_mean_spread
from wxdata.model_data.noaa.gefs.gefs import(
    gefs_0p50,
    gefs_0p50_secondary_parameters,
    gefs_0p25
)

from wxdata.model_data.noaa.cfs.cfs import(
    cfs_flux,
    cfs_pressure
)

from wxdata.model_data.noaa.aigefs.aigefs import(
    aigefs_pressure_members,
    aigefs_surface_members,
    aigefs_single
)

from wxdata.model_data.noaa.rtma.rtma import(
    rtma as _fetch_rtma, 
    rtma_comparison
)

from wxdata.model_data.ecmwf.ecmwf import(
    ecmwf_ifs,
    ecmwf_ifs_ens,
    ecmwf_aifs,
    ecmwf_aifs_ens,
    ecmwf_ifs_wave,
    ecmwf_ifs_wave_ens
)

from wxdata.model_data.cmc.gdps.gdps import gdps
from wxdata.model_data.cmc.rdps.rdps import rdps
from wxdata.model_data.cmc.hrdps.hrdps import hrdps
from wxdata.model_data.cmc.geps.geps import geps
from wxdata.model_data.cmc.cansips.forecast.cansips_forecast import cansips_forecast
from wxdata.model_data.cmc.cansips.hindcast.cansips_hindcast import cansips_hindcast



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
def wx():
    """WxData command line utilities."""
    pass

# ---------------------------------------------------------------------
# RTMA Commands
# ---------------------------------------------------------------------
@wx.group()
def rtma():
    """RTMA utilities."""
    pass


@rtma.command("rtma")
@click.option(
    "--model",
    default="rtma",
    show_default=True,
    help="rtma (CONUS) | akrtma (Alaska) | hi rtma (Hawaii) | pr rtma (Puerto Rico) | gu rtma (Guam)"
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

def rtma_fetch(model, cat, proxy, clear_recycle_bin, custom_directory, clear_data, source):
    """Download and decode RTMA GRIB2 data."""

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
        click.echo(f"RTMA fetch complete for model={model}, category={cat}, saved to {custom_directory}")
    else:
        click.echo(f"RTMA fetch complete for model={model}, category={cat}, saved to {model.upper()}/{cat.upper()}")
        

# ---------------------------------------------------------------------
# GFS 0.25x0.25 Commands
# ---------------------------------------------------------------------
"""
@wx.group()
def gfs_0p25():
    GFS 0.25x0.25 utilities.
    pass

@gfs_0p25.command("gfs0p25")
@click.option(
    "--final_forecast_hour",
    default=384,
    show_default=True,
    help="This is the final forecast hour requested in the dataset."
)
"""
        
# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    wx()
    
if __name__ == "__main__":
    main()