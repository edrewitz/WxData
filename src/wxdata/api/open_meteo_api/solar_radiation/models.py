"""
This file hosts the functions for selecting a model option.

(C) Eric J. Drewitz 2025-2026
"""

def model_selection(model):
    
    """
    This function returns the abbreviation for each model for the URL API request.
    
    Required Arguments:
    
    1) model (String) - Model the user wishes to select.
    
    ***Model Selection***
    
        'automatic selection'
        'best match'
        'dwd eumetsat mtg'
        'eumetsat msg'
        'eumetsat iodc'
        'eumetsat sarah3'
        'jma jaxa eumetsat mtg'
        'ecmwf ifs hres 9km'
        'ecmwf ifs 0.25'
        'ecmwf aifs 0.25 single'
        'cma grapes global'
        'bom access global'
        'dwd icon seamless'
        'dwd icon global'
        'dwd icon eu'
        'dwd icon d2'
        'met norway nordic seamless (with ecmwf)'
        'met norway nordic'
        'geosphere seamless (with ecmwf)'
        'geosphere arome austria'
        'ncep gfs seamless'
        'ncep gfs global 0.11/0.25'
        'ncep hrrr us conus'
        'ncep nbm us conus'
        'ncep aigfs 0.25'
        'ncep hgefs 0.25 ensemble mean'
        'gem seamless'
        'gem global'
        'gem regional'
        'gem hrdps continental'
        'gem hrdps west'
        'knmi seamless (with ecmwf)'
        'knmi harmonie arome europe'
        'knmi harmonie arome netherlands'
        'dmi seamless (with ecmwf)'
        'dmi harmonie arome europe'
        'chmi aladin seamless'
        'chmi aladin central europe 2km'
        'chmi aladin cz 1km'
        'jma seamless'
        'jma msm'
        'jma_gsm'
        'meteo-france seamless'
        'meteo-france arpege world'
        'meteo-france arpege europe'
        'meteo-france arome france'
        'meteo-france arome france hd'
        'uk met office seamless'
        'uk met office global 10km'
        'uk met office uk 2km'
        'era-5 seamless'
        'era-5'
        'era-5 land'
        'era-5 ensemble'
        'cerra':'cerra',
        'kma seamless'
        'kma ldps'
        'kma gdps'
        'italianmeteo arpae icon 2i'
        'meteoswiss icon seamless'
        'meteoswiss icon ch1'
        'meteoswiss icon ch2'
    
    Optional Arguments: None
    
    Returns
    -------
    
    The abbreviation for the model to be used in the URL API request.
    """
    
    model = model.lower()
    
    models = {
        
        'automatic selection':'satellite_radiation_seamless',
        'best match':'best_match',
        'dwd eumetsat mtg':'dwd_sis_europe_africa_v4',
        'eumetsat msg':'eumetsat_lsa_saf_msg',
        'eumetsat iodc':'eumetsat_lsa_saf_iodc',
        'eumetsat sarah3':'eumetsat_sarah3',
        'jma jaxa eumetsat mtg':'jma_jaxa_mtg_fci',
        'ecmwf ifs hres 9km':'ecmwf_ifs',
        'ecmwf ifs 0.25':'ecmwf_ifs025',
        'ecmwf aifs 0.25 single':'ecmwf_aifs025_single',
        'cma grapes global':'cma_grapes_global',
        'bom access global':'bom_access_global',
        'dwd icon seamless':'dwd_icon_seamless',
        'dwd icon global':'dwd_icon_global',
        'dwd icon eu':'dwd_icon_eu',
        'dwd icon d2':'dwd_icon_d2',
        'met norway nordic seamless (with ecmwf)':'metno_seamless',
        'met norway nordic':'metno_nordic',
        'geosphere seamless (with ecmwf)':'geosphere_seamless',
        'geosphere arome austria':'geosphere_arome_austria',
        'ncep gfs seamless':'ncep_gfs_seamless',
        'ncep gfs global 0.11/0.25':'ncep_gfs_global',
        'ncep hrrr us conus':'ncep_hrrr_conus',
        'ncep nbm us conus':'ncep_nbm_conus',
        'ncep aigfs 0.25':'ncep_aigfs025',
        'ncep hgefs 0.25 ensemble mean':'ncep_hgefs025_ensemble_mean',
        'gem seamless':'cmc_gem_seamless',
        'gem global':'cmc_gem_gdps',
        'gem regional':'cmc_gem_rdps',
        'gem hrdps continental':'cmc_gem_hrdps',
        'gem hrdps west':'cmc_gem_hrdps_west',
        'knmi seamless (with ecmwf)':'knmi_seamless',
        'knmi harmonie arome europe':'knmi_harmonie_arome_europe',
        'knmi harmonie arome netherlands':'knmi_harmonie_arome_netherlands',
        'dmi seamless (with ecmwf)':'dmi_seamless',
        'dmi harmonie arome europe':'dmi_harmonie_arome_europe',
        'chmi aladin seamless':'chmi_aladin_seamless',
        'chmi aladin central europe 2km':'chmi_aladin_central_europe_2km',
        'chmi aladin cz 1km':'chmi_aladin_cz_1km',
        'jma seamless':'jma_seamless',
        'jma msm':'jma_msm',
        'jma_gsm':'jma_gsm',
        'meteo-france seamless':'meteofrance_seamless',
        'meteo-france arpege world':'meteofrance_arpege_world',
        'meteo-france arpege europe':'meteofrance_arpege_europe',
        'meteo-france arome france':'meteofrance_arome_france',
        'meteo-france arome france hd':'meteofrance_arome_france_hd',
        'uk met office seamless':'ukmo_seamless',
        'uk met office global 10km':'ukmo_global_deterministic_10km',
        'uk met office uk 2km':'ukmo_uk_deterministic_2km',
        'era-5 seamless':'era5_seamless',
        'era-5':'era5',
        'era-5 land':'era5_land',
        'era-5 ensemble':'era5_ensemble',
        'cerra':'cerra',
        'kma seamless':'kma_seamless',
        'kma ldps':'kma_ldps',
        'kma gdps':'kma_gdps',
        'italianmeteo arpae icon 2i':'italia_meteo_arpae_icon_2i',
        'meteoswiss icon seamless':'meteoswiss_icon_seamless',
        'meteoswiss icon ch1':'meteoswiss_icon_ch1',
        'meteoswiss icon ch2':'meteoswiss_icon_ch2'
    }
    
    return models[model]