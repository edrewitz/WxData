import click

from wxdata.model_data.noaa.gfs.gfs import(
    gfs_0p25,
    gfs_0p25_secondary_parameters,
    gfs_0p50
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
from wxdata.fuels_data.fems.observations import(
    get_single_raws_station_weather_observations,
    get_single_raws_station_fuels_observations,
    get_multi_raws_station_weather_observations,
    get_multi_raws_station_fuels_observations,
    get_current_multi_raws_station_weather_observations,
    get_current_multi_raws_station_fuels_observations,
    get_current_all_raws_station_weather_observations,
    get_current_all_raws_station_fuels_observations,
    get_single_raws_station_nfdrs_forecast,
    get_multi_raws_station_nfdrs_forecast,
    get_single_raws_station_weather_forecast,
    get_multi_raws_station_weather_forecast
)

from wxdata.fuels_data.fems.meta_data import(
    get_single_raws_station_meta_data,
    get_multi_raws_station_meta_data
)

from wxdata.gridded_forecasts.noaa.nws.nws import(
    get_ndfd_grids,
    get_cpc_outlook
)

from wxdata.observational_data.metars.metar_obs import download_metar_data
from wxdata.observational_data.radar.nexrad2 import(
    download_current_single_station_nexrad2_radar_data,
    download_current_multi_station_nexrad2_radar_data
)

import wxdata.api.open_meteo_api.weather_forecasts.noaa as open_meteo_api_noaa
import wxdata.api.open_meteo_api.weather_forecasts.ecmwf as open_meteo_api_ecmwf
import wxdata.api.open_meteo_api.weather_forecasts.dwd as open_meteo_api_dwd
import wxdata.api.open_meteo_api.weather_forecasts.meteo_france as open_meteo_api_meteo_france
import wxdata.api.open_meteo_api.weather_forecasts.cmc as open_meteo_api_cmc
import wxdata.api.open_meteo_api.weather_forecasts.jma as open_meteo_api_jma
import wxdata.api.open_meteo_api.weather_forecasts.ukmo as open_meteo_api_ukmo
import wxdata.api.open_meteo_api.weather_forecasts.current_weather as open_meteo_api_current_weather
import wxdata.api.open_meteo_api.weather_forecasts.google as open_meteo_api_google
import wxdata.api.open_meteo_api.seasonal_forecasts.ecmwf_daily as open_meteo_api_ecmwf_seasonal_forecasts_daily
import wxdata.api.open_meteo_api.seasonal_forecasts.ecmwf_weekly as open_meteo_api_ecmwf_seasonal_forecasts_weekly
import wxdata.api.open_meteo_api.seasonal_forecasts.ecmwf_monthly as open_meteo_api_ecmwf_seasonal_forecasts_monthly
import wxdata.api.open_meteo_api.climate.climate_data as open_meteo_api_climate_data
import wxdata.api.open_meteo_api.air_quality.cams as open_meteo_api_air_quality
import wxdata.api.open_meteo_api.marine_forecasts.meteo_france as open_meteo_api_meteo_france_marine
import wxdata.api.open_meteo_api.marine_forecasts.dwd as open_meteo_api_dwd_marine
import wxdata.api.open_meteo_api.marine_forecasts.ecmwf as open_meteo_api_ecmwf_marine
import wxdata.api.open_meteo_api.marine_forecasts.noaa as open_meteo_api_noaa_marine
import wxdata.api.open_meteo_api.solar_radiation.solar_radiation as open_meteo_api_solar_radiation
import wxdata.api.airnow_api.observations as air_now_observations


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
def wxdata():
    """WxData command line utilities."""
    pass

# ---------------------------------------------------------------------
# RTMA Commands
# ---------------------------------------------------------------------
@wxdata.group()
def rtma():
    """RTMA utilities."""
    pass


@rtma.command("rtma")
@click.option(
    "--model",
    default="rtma",
    show_default=True,
    required=True,
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
    help="Proxy URL (e.g., http://user:pass@host:port). Default: no proxy.",
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
# Entry point
# ---------------------------------------------------------------------
def main():
    wxdata()
    
if __name__ == "__main__":
    main()